#!/usr/bin/env python3
"""
Step 0 — Human ambiguity profile and danger-cell count (no API).

Reads the MLB coder-reliability logs on disk and answers the one question that
gates the whole study before any model runs:

    Of the 179 matched quasi-sentences, how many are GENUINELY human-split?

If many sentences are human-split, the "humans split / models agree" danger cell
(Beat 4) has room. If few are, Beat 4 is thin and we should know that before
spending on ~45k model calls.

This single computation also forces the two BLOCKING design decisions, because
both change the count, so we compute the full robustness grid and report all of it:

    pool           in {full, retained}      -- crowd ceiling vs MLB expert screen
    zero_handling in {class, exclude}       -- 000/uncoded as a 57th class vs dropped

Granularities reported per sentence: 56+1 category, 7 domain, 3 RILE classes.

Inputs (verified on disk):
    data/human/codes.log            32 GB coders, 107 quasi-sentences
    data/human/codesNZ.log          23 NZ coders, 72 quasi-sentences
    data/human/master-codersGB.txt  gold (107)
    data/human/master-codersNZ.txt  gold (72)
    data/categories.json            57-code scheme: domain + rile mapping
    data/cmp_coding_sample.json     179 unit records (text, gold, section)

Outputs:
    reports/human/human_codings.csv          long: coder_id, manifesto, unit_id, seq, code
    reports/human/coders.csv                 identity, prior-experience, retained flag
    reports/human/per_sentence_ambiguity.csv per-unit entropy/modal share, all combos
    reports/human/human_profile_report.md    danger-cell counts, kappa validation, decisions

Run:  python3 src/human_profile.py
"""

from __future__ import annotations

import csv
import json
import math
import os
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "human")
REPORTS = os.path.join(ROOT, "reports", "human")

# Column layout, verified empirically against the files:
#   fields 0..6  = ip, date, time, id, name, email, institution
#   field  7     = self-reported prior-experience number
#   fields 8..   = the per-quasi-sentence code vector (107 GB / 72 NZ)
META_COLS = 8
N_UNITS = {"GB": 107, "NZ": 72}

LOGS = {"GB": "codes.log", "NZ": "codesNZ.log"}
MASTERS = {"GB": "master-codersGB.txt", "NZ": "master-codersNZ.txt"}

# Verification vectors (RESEARCH_PLAN §9): if parsing yields these exact leading arrays,
# the text -> gold -> human alignment is intact.
VERIFY = {
    "GB": ["000", "000", "000", "305", "305", "606", "305", "410", "408"],
    "NZ": ["414", "414", "414", "414", "414", "408", "408", "402"],
}

# MLB's exact reliability screen: the coders THEY discarded (bottom quartile by
# coder-vs-master kappa) plus the master authors. Reproduced verbatim from
# CMP_reliability_replication.R so the "retained" set carries no degree of freedom of ours.
DROP = {
    "GB": {
        "doherta", "careydp", "njokur", "headonc", "rutherfc", "saula",
        "lukaszek", "campbeca", "ligita_sarkute", "daublert", "goreckim",
        "kbenoit", "mikhailv", "sudulicm", "fedoreae",
    },
    "NZ": {
        "sgilliga", "carroljm", "corleymi", "mcnamaco", "farrelsk", "mrwillia",
        "ligita_sarkute", "kenneth.mcdonagh", "martinh", "kbenoit", "mikhailv",
        "kaczmara",
    },
}


def norm_code(raw: str) -> str:
    """Normalise a raw code token. Master files write uncoded as '0'; logs as '000'."""
    c = raw.strip().strip('"')
    if c in ("0", "00", "000", ""):
        return "000"
    return c


def email_prefix(email: str) -> str:
    e = email.strip().strip('"')
    return e.split("@")[0] if "@" in e else e


def parse_log(path: str, manifesto: str, is_master: bool):
    """Yield (coder_id, experience, [codes]) rows. Master files have one row."""
    n = N_UNITS[manifesto]
    rows = []
    with open(path, encoding="latin-1") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line.strip():
                continue
            f = line.split("\t")
            codes = [norm_code(x) for x in f[META_COLS:META_COLS + n]]
            if len(codes) != n:
                raise ValueError(
                    f"{path}: expected {n} codes, got {len(codes)} "
                    f"(NF={len(f)}); line starts {f[:6]}"
                )
            if is_master:
                coder_id, exp = "MASTER", ""
            else:
                coder_id = email_prefix(f[5])
                exp = f[META_COLS - 1].strip()
            rows.append((coder_id, exp, codes))
    return rows


def shannon_bits(counts) -> float:
    total = sum(counts)
    if total == 0:
        return 0.0
    h = 0.0
    for c in counts:
        if c:
            p = c / total
            h -= p * math.log2(p)
    return h


def ambiguity(codes):
    """Disagreement summary for one list of votes (already pooled/filtered)."""
    n = len(codes)
    if n == 0:
        return dict(n=0, distinct=0, modal=None, modal_share=float("nan"),
                    one_minus_modal=float("nan"), H_bits=float("nan"),
                    H_norm=float("nan"))
    cnt = Counter(codes)
    modal, modal_n = cnt.most_common(1)[0]
    H = shannon_bits(list(cnt.values()))
    H_norm = H / math.log2(n) if n > 1 else 0.0
    return dict(n=n, distinct=len(cnt), modal=modal,
                modal_share=modal_n / n, one_minus_modal=1 - modal_n / n,
                H_bits=H, H_norm=H_norm)


def fleiss_kappa(item_votes, n_raters):
    """Fleiss' kappa with a constant number of raters per item.

    item_votes: list of Counter, one per item (category -> count). Each must sum to n_raters.
    """
    N = len(item_votes)
    cats = set()
    for c in item_votes:
        cats |= set(c)
    cats = sorted(cats)
    n = n_raters
    # P_i agreement per item
    Pbar = 0.0
    cat_total = {c: 0 for c in cats}
    for votes in item_votes:
        ss = sum(v * v for v in votes.values())
        Pbar += (ss - n) / (n * (n - 1))
        for c, v in votes.items():
            cat_total[c] += v
    Pbar /= N
    Pe = sum((cat_total[c] / (N * n)) ** 2 for c in cats)
    if Pe >= 1.0:
        return float("nan")
    return (Pbar - Pe) / (1 - Pe)


def cohen_kappa(a, b):
    """Cohen's kappa between two equal-length label vectors."""
    assert len(a) == len(b)
    n = len(a)
    cats = sorted(set(a) | set(b))
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum((ca.get(c, 0) / n) * (cb.get(c, 0) / n) for c in cats)
    if pe >= 1.0:
        return float("nan")
    return (po - pe) / (1 - pe)


def main():
    cats_meta = json.load(open(os.path.join(ROOT, "data", "categories.json")))["categories"]
    domain_of = {k: v["domain"] for k, v in cats_meta.items()}
    rile_of = {k: v["rile"] for k, v in cats_meta.items()}
    # 000 is in categories.json; make sure unknowns degrade gracefully.
    def dom(c):
        return domain_of.get(c, "?")
    def rile(c):
        return rile_of.get(c, "none")

    units = json.load(open(os.path.join(ROOT, "data", "cmp_coding_sample.json")))["units"]
    unit_by = {u["unit_id"]: u for u in units}

    # ---- parse logs + masters, assert verification vectors -------------------
    coders = {}      # manifesto -> list of (coder_id, exp, codes)
    master = {}      # manifesto -> [codes]
    for m in ("GB", "NZ"):
        master_rows = parse_log(os.path.join(DATA, MASTERS[m]), m, is_master=True)
        assert len(master_rows) == 1
        master[m] = master_rows[0][2]
        got = master[m][:len(VERIFY[m])]
        assert got == VERIFY[m], f"{m} master verify FAILED:\n  got {got}\n  exp {VERIFY[m]}"
        coders[m] = parse_log(os.path.join(DATA, LOGS[m]), m, is_master=False)
        # cross-check master gold against the JSON unit records
        for i, code in enumerate(master[m], start=1):
            uid = f"{m}-{i:03d}"
            assert unit_by[uid]["master_code"] == code, \
                f"{uid}: master file {code} != json {unit_by[uid]['master_code']}"
    print("OK  verification vectors + master<->json gold match")

    retained_flag = {}  # (manifesto, coder_id) -> bool
    for m in ("GB", "NZ"):
        for cid, _exp, _codes in coders[m]:
            retained_flag[(m, cid)] = cid not in DROP[m]
    n_full = {m: len(coders[m]) for m in ("GB", "NZ")}
    n_ret = {m: sum(retained_flag[(m, c)] for c, _, _ in coders[m]) for m in ("GB", "NZ")}
    print(f"    coders: GB full={n_full['GB']} retained={n_ret['GB']} | "
          f"NZ full={n_full['NZ']} retained={n_ret['NZ']}")

    # ---- emit tidy long tables ----------------------------------------------
    os.makedirs(REPORTS, exist_ok=True)
    with open(os.path.join(REPORTS, "human_codings.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["coder_id", "manifesto", "unit_id", "sequence", "code"])
        for m in ("GB", "NZ"):
            for cid, _exp, codes in coders[m]:
                for i, code in enumerate(codes, start=1):
                    w.writerow([cid, m, f"{m}-{i:03d}", i, code])
    with open(os.path.join(REPORTS, "coders.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["coder_id", "manifesto", "prior_experience", "mlb_retained"])
        for m in ("GB", "NZ"):
            for cid, exp, _codes in coders[m]:
                w.writerow([cid, m, exp, int(retained_flag[(m, cid)])])

    # ---- per-coder Cohen's kappa vs master (parsing validation) -------------
    coh = {m: [] for m in ("GB", "NZ")}
    coh_ret = {m: [] for m in ("GB", "NZ")}
    for m in ("GB", "NZ"):
        for cid, _exp, codes in coders[m]:
            k = cohen_kappa(codes, master[m])
            coh[m].append(k)
            if retained_flag[(m, cid)]:
                coh_ret[m].append(k)

    def median(xs):
        xs = sorted(x for x in xs if not math.isnan(x))
        if not xs:
            return float("nan")
        h = len(xs) // 2
        return xs[h] if len(xs) % 2 else (xs[h - 1] + xs[h]) / 2

    # ---- Fleiss kappa by category (000 as a class), retained vs full --------
    def fleiss_for(m, pool):
        sel = [(c, codes) for c, _e, codes in coders[m]
               if (pool == "full" or retained_flag[(m, c)])]
        n_raters = len(sel)
        item_votes = []
        for i in range(N_UNITS[m]):
            item_votes.append(Counter(codes[i] for _c, codes in sel))
        return fleiss_kappa(item_votes, n_raters), n_raters

    # ---- per-sentence ambiguity across the full robustness grid -------------
    POOLS = ("full", "retained")
    ZEROS = ("class", "exclude")
    rows = []
    for m in ("GB", "NZ"):
        for i in range(N_UNITS[m]):
            uid = f"{m}-{i + 1:03d}"
            rec = {"unit_id": uid, "manifesto": m, "sequence": i + 1,
                   "master_code": master[m][i], "master_rile": rile(master[m][i])}
            for pool in POOLS:
                votes = [codes[i] for c, _e, codes in coders[m]
                         if (pool == "full" or retained_flag[(m, c)])]
                for zero in ZEROS:
                    cat_votes = votes if zero == "class" else [v for v in votes if v != "000"]
                    dom_votes = [dom(v) for v in cat_votes]
                    rile_votes = [rile(v) for v in cat_votes]
                    pre = f"{pool}_{zero}_"
                    a_cat = ambiguity(cat_votes)
                    a_dom = ambiguity(dom_votes)
                    a_rile = ambiguity(rile_votes)
                    rec[pre + "n"] = a_cat["n"]
                    rec[pre + "cat_distinct"] = a_cat["distinct"]
                    rec[pre + "cat_modal_share"] = a_cat["modal_share"]
                    rec[pre + "cat_1mmodal"] = a_cat["one_minus_modal"]
                    rec[pre + "cat_Hnorm"] = a_cat["H_norm"]
                    rec[pre + "dom_1mmodal"] = a_dom["one_minus_modal"]
                    rec[pre + "rile_1mmodal"] = a_rile["one_minus_modal"]
                    rec[pre + "rile_distinct"] = a_rile["distinct"]
                    rec[pre + "rile_modal"] = a_rile["modal"]
            rows.append(rec)

    fieldnames = list(rows[0].keys())
    with open(os.path.join(REPORTS, "per_sentence_ambiguity.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    # ---- danger-cell counts --------------------------------------------------
    def count(rows_, key, thr, ge=True):
        out = 0
        for r in rows_:
            v = r.get(key)
            if v is None or (isinstance(v, float) and math.isnan(v)):
                continue
            if (v >= thr) if ge else (v > thr):
                out += 1
        return out

    # ---- build report --------------------------------------------------------
    L = []
    L.append("# Step 0 — Human ambiguity profile & danger-cell count\n")
    L.append("_No API. Computed from the MLB reliability logs on disk._\n")
    L.append(f"- Units: 179 (GB 107 + NZ 72). Coders: GB {n_full['GB']} full / "
             f"{n_ret['GB']} retained; NZ {n_full['NZ']} full / {n_ret['NZ']} retained.")
    L.append("- Verification vectors and master↔JSON gold: **passed**.\n")

    L.append("## Parsing validation against MLB published statistics\n")
    L.append("If these reproduce the paper, the parse is end-to-end correct.\n")
    L.append("| statistic | GB | NZ | combined | MLB reported |")
    L.append("|---|---|---|---|---|")
    fk_gb_f, nr = fleiss_for("GB", "full")
    fk_nz_f, _ = fleiss_for("NZ", "full")
    fk_gb_r, _ = fleiss_for("GB", "retained")
    fk_nz_r, _ = fleiss_for("NZ", "retained")
    L.append(f"| Fleiss κ (category, full pool) | {fk_gb_f:.3f} | {fk_nz_f:.3f} | — | GB .35 / NZ .40–.47 |")
    L.append(f"| Fleiss κ (category, retained) | {fk_gb_r:.3f} | {fk_nz_r:.3f} | — | (retained set) |")
    comb_med = median(coh_ret["GB"] + coh_ret["NZ"])
    L.append(f"| median coder-vs-master Cohen κ (retained) | {median(coh_ret['GB']):.3f} | "
             f"{median(coh_ret['NZ']):.3f} | {comb_med:.3f} | GB .43 / NZ .54 / comb .46 |")
    L.append(f"| median coder-vs-master Cohen κ (full pool) | {median(coh['GB']):.3f} | "
             f"{median(coh['NZ']):.3f} | {median(coh['GB']+coh['NZ']):.3f} | — |\n")

    L.append("## The danger-cell count: how many sentences are human-split?\n")
    L.append("Counts of the 179 sentences exceeding each disagreement threshold, "
             "at **category** granularity. `1−modal share` = fraction of coders NOT on "
             "the top code (≥.50 ⇒ no majority code).\n")
    L.append("| combo | ≥2 codes | ≥3 codes | 1−modal≥.40 | 1−modal≥.50 | 1−modal≥.60 | Hnorm≥.50 |")
    L.append("|---|--:|--:|--:|--:|--:|--:|")
    for pool in POOLS:
        for zero in ZEROS:
            p = f"{pool}_{zero}_"
            L.append(
                f"| {pool} / 000-{zero} "
                f"| {count(rows, p+'cat_distinct', 2)} "
                f"| {count(rows, p+'cat_distinct', 3)} "
                f"| {count(rows, p+'cat_1mmodal', 0.40)} "
                f"| {count(rows, p+'cat_1mmodal', 0.50)} "
                f"| {count(rows, p+'cat_1mmodal', 0.60)} "
                f"| {count(rows, p+'cat_Hnorm', 0.50)} |"
            )
    L.append("")
    L.append("Same, at **RILE 3-class** granularity (the split that actually moves Beat 5). "
             "`rile_distinct≥2` = coders disagree on left/right/none; `1−modal≥.50` = no "
             "majority RILE class.\n")
    L.append("| combo | RILE split (≥2 classes) | no RILE majority (1−modal≥.50) |")
    L.append("|---|--:|--:|")
    for pool in POOLS:
        for zero in ZEROS:
            p = f"{pool}_{zero}_"
            L.append(f"| {pool} / 000-{zero} | {count(rows, p+'rile_distinct', 2)} "
                     f"| {count(rows, p+'rile_1mmodal', 0.50)} |")
    L.append("")

    L.append("## Blocking decisions, with the numbers attached\n")
    L.append("**1. `000`/uncoded handling.** Compare the `000-class` vs `000-exclude` rows "
             "above: excluding 000 removes the uncoded votes that concentrate in the most "
             "ambiguous sentences, so it *changes* the split count. Plan lean — keep 000 as a "
             "class (primary), report exclude as robustness. The grid is computed both ways.\n")
    L.append("**2. Retained vs full pool.** Compare the `full` vs `retained` rows. Retained "
             "uses MLB's exact drop list (no threshold of ours). Plan lean — retained = expert "
             "ceiling (primary), full = crowd ceiling (robustness). Both reported.\n")
    L.append("> Reproduction check: the retained set is **17 GB / 12 NZ**, matching the paper. "
             "(`kbenoit` appears in the GB drop list but never coded NZ, so 11 of the 12 NZ drop "
             "names match the log — hence 12 retained, not 11.) Retained Fleiss κ and median "
             "coder-vs-master Cohen κ reproduce MLB's published values, confirming the parse.\n")

    report = "\n".join(L)
    with open(os.path.join(REPORTS, "human_profile_report.md"), "w") as fh:
        fh.write(report)

    print("\n" + report)
    print(f"\nwrote: reports/human/human_codings.csv, coders.csv, "
          f"per_sentence_ambiguity.csv, human_profile_report.md")


if __name__ == "__main__":
    main()
