"""Pilot analysis -> reports/pilot/.

Five looks, matching PILOT_PLAN.md §Analysis (which maps to parent plan §4.3/§4.4):

  1. Q1 pulse        per (config, sentence) model spread vs RETAINED human spread
                     (full-pool overlay = robustness); single correlation per config.
  2. Resolution      recompute model spread at 10 -> 5 -> 3 runs; report movement.
                     *The key feasibility output — sets runs-per-model for the full study.*
  3. Q2 cells        model confusion pairs vs human confusion pairs (same sentences);
                     count non-empty cells -> Q2 headline or illustration.
  4. Reasoning       toggleable models: spread on vs off (per config, never pooled).
  5. Exemplars       2-3 sentences read with the 32-coder receipts.

Spread metric matches the human side exactly (human_profile.ambiguity):
1 - modal_share, and H_norm = H_bits / log2(n). Off-scheme predictions are kept
as their own "OFF" category in the model vote list (mirrors human 000/off-gold).

Pure stdlib; a scatter PNG is written only if matplotlib is importable.

    python -m src.pilot.analyze
"""

import csv
import json
from collections import Counter, defaultdict
from math import log2

from . import config

OFF = "OFF"     # pseudo-code for an off-scheme / refusal / multi-code output


# --- metrics ----------------------------------------------------------------
def spread(votes):
    """Disagreement summary for a vote list — matches human_profile.ambiguity."""
    n = len(votes)
    if n == 0:
        return dict(n=0, distinct=0, modal=None, modal_share=float("nan"),
                    one_minus_modal=float("nan"), Hnorm=float("nan"))
    cnt = Counter(votes)
    modal, modal_n = cnt.most_common(1)[0]
    H = -sum((c / n) * log2(c / n) for c in cnt.values() if c)
    Hnorm = H / log2(n) if n > 1 else 0.0
    return dict(n=n, distinct=len(cnt), modal=modal, modal_share=modal_n / n,
                one_minus_modal=1 - modal_n / n, Hnorm=Hnorm)


def pearson(xs, ys):
    pairs = [(x, y) for x, y in zip(xs, ys) if x == x and y == y]   # drop NaN
    n = len(pairs)
    if n < 2:
        return float("nan"), n
    mx = sum(x for x, _ in pairs) / n
    my = sum(y for _, y in pairs) / n
    cov = sum((x - mx) * (y - my) for x, y in pairs)
    vx = sum((x - mx) ** 2 for x, _ in pairs)
    vy = sum((y - my) ** 2 for _, y in pairs)
    if vx == 0 or vy == 0:
        return float("nan"), n
    return cov / (vx ** 0.5 * vy ** 0.5), n


# --- loaders ----------------------------------------------------------------
def load_predictions():
    """(config_id, unit_id) -> list[(run_idx, vote)]; plus config + sentence meta."""
    by_cell = defaultdict(list)
    cfg_meta, sent_meta = {}, {}
    with open(config.PREDICTIONS_CSV, newline="") as f:
        for r in csv.DictReader(f):
            off = r["off_scheme"] == "True" or not r["pred_code"]
            vote = OFF if off else r["pred_code"]
            cell = (r["config_id"], r["unit_id"])
            by_cell[cell].append((int(r["run_idx"]), vote))
            cfg_meta[r["config_id"]] = {
                "model": r["model"], "reasoning_mode": r["reasoning_mode"],
                "capability": r["capability"]}
            sent_meta[r["unit_id"]] = {
                "manifesto": r["manifesto"], "bucket": r["bucket"],
                "master_code": r["master_code"]}
    for cell in by_cell:
        by_cell[cell].sort()        # by run_idx
    return by_cell, cfg_meta, sent_meta


def load_manifest():
    with open(config.SENTENCE_MANIFEST, newline="") as f:
        return {r["unit_id"]: r for r in csv.DictReader(f)}


def load_human_codings():
    """unit_id -> list[(code, retained_bool)] using coders.csv retention flag."""
    retained = {}
    with open(config.CODERS_CSV, newline="") as f:
        for r in csv.DictReader(f):
            retained[(r["coder_id"], r["manifesto"])] = r["mlb_retained"] == "1"
    by_unit = defaultdict(list)
    with open(config.HUMAN_CODINGS_CSV, newline="") as f:
        for r in csv.DictReader(f):
            key = (r["coder_id"], r["manifesto"])
            by_unit[r["unit_id"]].append((r["code"], retained.get(key, False)))
    return by_unit


def _f(row, col):
    try:
        return float(row[col])
    except (KeyError, ValueError, TypeError):
        return float("nan")


# --- 1. Q1 pulse ------------------------------------------------------------
def q1_pulse(by_cell, cfg_meta, manifest, out_dir):
    rows = []
    for (config_id, unit_id), votes in by_cell.items():
        m = spread([v for _, v in votes])
        man = manifest.get(unit_id, {})
        rows.append({
            "config_id": config_id, "model": cfg_meta[config_id]["model"],
            "reasoning_mode": cfg_meta[config_id]["reasoning_mode"],
            "unit_id": unit_id, "bucket": man.get("bucket", ""),
            "n_runs": m["n"], "model_1mmodal": m["one_minus_modal"],
            "model_Hnorm": m["Hnorm"], "model_modal": m["modal"],
            "model_distinct": m["distinct"],
            "human_ret_1mmodal": _f(man, "retained_class_cat_1mmodal"),
            "human_ret_Hnorm": _f(man, "retained_class_cat_Hnorm"),
            "human_full_1mmodal": _f(man, "full_class_cat_1mmodal"),
            "human_full_Hnorm": _f(man, "full_class_cat_Hnorm"),
            "master_code": man.get("master_code", ""),
        })
    rows.sort(key=lambda r: (r["config_id"], r["unit_id"]))
    _write_csv(out_dir / "q1_pulse.csv", rows)

    # per-config correlations: model spread vs retained (primary) and full (robustness)
    summary = []
    for config_id in sorted({r["config_id"] for r in rows}):
        sub = [r for r in rows if r["config_id"] == config_id]
        r_ret, n = pearson([r["model_1mmodal"] for r in sub],
                           [r["human_ret_1mmodal"] for r in sub])
        r_full, _ = pearson([r["model_1mmodal"] for r in sub],
                            [r["human_full_1mmodal"] for r in sub])
        rh_ret, _ = pearson([r["model_Hnorm"] for r in sub],
                            [r["human_ret_Hnorm"] for r in sub])
        summary.append({
            "config_id": config_id, "n_sentences": n,
            "r_1mmodal_vs_retained": r_ret, "r_1mmodal_vs_full": r_full,
            "r_Hnorm_vs_retained": rh_ret,
            "mean_model_1mmodal": _mean([r["model_1mmodal"] for r in sub]),
            "mean_human_ret_1mmodal": _mean([r["human_ret_1mmodal"] for r in sub]),
        })
    _write_csv(out_dir / "q1_correlations.csv", summary)
    _scatter(rows, out_dir)
    return rows, summary


# --- 2. Resolution check ----------------------------------------------------
def resolution(by_cell, cfg_meta, out_dir):
    ks = [10, 5, 3]
    per = []
    for (config_id, unit_id), votes in by_cell.items():
        ordered = [v for _, v in votes]
        rec = {"config_id": config_id, "unit_id": unit_id}
        for k in ks:
            s = spread(ordered[:k])
            rec[f"1mmodal_at{k}"] = s["one_minus_modal"]
            rec[f"Hnorm_at{k}"] = s["Hnorm"]
        per.append(rec)
    per.sort(key=lambda r: (r["config_id"], r["unit_id"]))
    _write_csv(out_dir / "resolution_per_sentence.csv", per)

    # movement: mean |spread(k) - spread(10)| across sentences, per config
    summary = []
    for config_id in sorted({r["config_id"] for r in per}):
        sub = [r for r in per if r["config_id"] == config_id]
        row = {"config_id": config_id, "n_sentences": len(sub)}
        for k in (5, 3):
            row[f"mean_abs_d_1mmodal_10v{k}"] = _mean(
                [abs(r["1mmodal_at10"] - r[f"1mmodal_at{k}"]) for r in sub])
            row[f"mean_abs_d_Hnorm_10v{k}"] = _mean(
                [abs(r["Hnorm_at10"] - r[f"Hnorm_at{k}"]) for r in sub])
        summary.append(row)
    _write_csv(out_dir / "resolution_summary.csv", summary)
    return summary


# --- 3. Q2 confusion cells --------------------------------------------------
def q2_cells(by_cell, sent_meta, human_codings, manifest, out_dir):
    units = set(manifest)
    # human confusion pairs (master_code, coder_code) on the selected sentences
    human_pairs = Counter()
    human_pairs_ret = Counter()
    for unit_id in units:
        master = manifest[unit_id]["master_code"]
        for code, ret in human_codings.get(unit_id, []):
            if code != master:
                human_pairs[(master, code)] += 1
                if ret:
                    human_pairs_ret[(master, code)] += 1
    # model confusion pairs (master_code, pred_code), pooled + per config
    model_pairs = Counter()
    model_pairs_by_cfg = defaultdict(Counter)
    for (config_id, unit_id), votes in by_cell.items():
        master = sent_meta[unit_id]["master_code"]
        for _, v in votes:
            if v != OFF and v != master:
                model_pairs[(master, v)] += 1
                model_pairs_by_cfg[config_id][(master, v)] += 1

    all_pairs = sorted(set(human_pairs) | set(model_pairs))
    rows = [{
        "master_code": a, "pred_or_coder_code": b,
        "human_count": human_pairs[(a, b)],
        "human_retained_count": human_pairs_ret[(a, b)],
        "model_count_pooled": model_pairs[(a, b)],
        "in_human": human_pairs[(a, b)] > 0,
        "in_model": model_pairs[(a, b)] > 0,
    } for a, b in all_pairs]
    rows.sort(key=lambda r: (-r["model_count_pooled"], -r["human_count"]))
    _write_csv(out_dir / "q2_confusion_pairs.csv", rows)

    overlap = sum(1 for a, b in all_pairs
                  if human_pairs[(a, b)] and model_pairs[(a, b)])
    summary = {
        "n_human_pairs": len(human_pairs),
        "n_human_retained_pairs": len(human_pairs_ret),
        "n_model_pairs_pooled": len(model_pairs),
        "n_overlap_pairs": overlap,
        "n_model_only_pairs": sum(1 for a, b in all_pairs
                                  if model_pairs[(a, b)] and not human_pairs[(a, b)]),
        "n_human_only_pairs": sum(1 for a, b in all_pairs
                                  if human_pairs[(a, b)] and not model_pairs[(a, b)]),
    }
    return summary, human_pairs, model_pairs_by_cfg


# --- 4. Reasoning contrast --------------------------------------------------
def reasoning_contrast(by_cell, cfg_meta, out_dir):
    # group toggleable models -> their on/off config_ids
    by_model = defaultdict(dict)
    for config_id, meta in cfg_meta.items():
        if meta["capability"] == "toggleable":
            by_model[meta["model"]][meta["reasoning_mode"]] = config_id
    rows = []
    for model, modes in by_model.items():
        if "on" not in modes or "off" not in modes:
            continue
        on_id, off_id = modes["on"], modes["off"]
        units = {u for (c, u) in by_cell if c == on_id}
        for unit_id in sorted(units):
            on = spread([v for _, v in by_cell.get((on_id, unit_id), [])])
            off = spread([v for _, v in by_cell.get((off_id, unit_id), [])])
            rows.append({
                "model": model, "unit_id": unit_id,
                "on_1mmodal": on["one_minus_modal"], "off_1mmodal": off["one_minus_modal"],
                "delta_1mmodal": on["one_minus_modal"] - off["one_minus_modal"],
                "on_Hnorm": on["Hnorm"], "off_Hnorm": off["Hnorm"],
            })
    if rows:
        _write_csv(out_dir / "reasoning_contrast.csv", rows)
    return rows


# --- 5. Exemplar close-reads ------------------------------------------------
def exemplars(q1_rows, by_cell, cfg_meta, manifest, human_codings, human_pairs, out_dir):
    # pooled model spread per unit (across all configs) for picking
    pooled = defaultdict(list)
    for (config_id, unit_id), votes in by_cell.items():
        pooled[unit_id].extend(v for _, v in votes)
    pooled_spread = {u: spread(vs) for u, vs in pooled.items()}

    def human_ret(u):
        return _f(manifest[u], "retained_class_cat_1mmodal")

    units = [u for u in manifest if u in pooled_spread]
    picks = {}
    chosen = set()

    def pick(tag, key):
        pool = [u for u in units if u not in chosen] or units
        u = max(pool, key=key)
        picks[tag] = u
        chosen.add(u)

    # (a) coin-flip where the model PINS: high human spread, low model spread
    pick("model_pins_on_coinflip",
         lambda u: human_ret(u) - pooled_spread[u]["one_minus_modal"])
    # (b) both waver: high human AND high model spread
    pick("both_waver",
         lambda u: min(human_ret(u), pooled_spread[u]["one_minus_modal"]))
    # (c) alien confusion: model's modal pred != master and that pair is NOT a human pair
    def alien_score(u):
        master = manifest[u]["master_code"]
        modal = pooled_spread[u]["modal"]
        if modal in (None, OFF, master):
            return -1
        return 0 if (master, modal) in human_pairs else pooled[u].count(modal)
    pick("alien_confusion", alien_score)

    lines = ["# Pilot exemplar close-reads\n",
             "Three sentences read with the human receipts. Picked mechanically "
             "from pooled model spread vs retained human spread — see criteria per "
             "section.\n"]
    for tag, unit_id in picks.items():
        man = manifest[unit_id]
        # human distributions
        full_codes = [c for c, _ in human_codings.get(unit_id, [])]
        ret_codes = [c for c, r in human_codings.get(unit_id, []) if r]
        lines.append(f"## {tag} — {unit_id} ({man['bucket']})\n")
        lines.append(f"> {man['text']}\n")
        lines.append(f"- master (gold): {man['master_code']} | "
                     f"section: {man['section']}")
        lines.append(f"- human FULL ({len(full_codes)} coders): "
                     f"{dict(Counter(full_codes).most_common())}")
        lines.append(f"- human RETAINED ({len(ret_codes)} coders): "
                     f"{dict(Counter(ret_codes).most_common())}")
        ps = pooled_spread[unit_id]
        lines.append(f"- model POOLED spread: 1-modal={ps['one_minus_modal']:.2f}, "
                     f"Hnorm={ps['Hnorm']:.2f}, modal={ps['modal']}")
        for config_id in sorted(c for (c, u) in by_cell if u == unit_id):
            votes = Counter(v for _, v in by_cell[(config_id, unit_id)])
            lines.append(f"    - {config_id}: {dict(votes.most_common())}")
        lines.append("")
    (out_dir / "exemplars.md").write_text("\n".join(lines))
    return picks


# --- helpers ----------------------------------------------------------------
def _mean(xs):
    xs = [x for x in xs if x == x]
    return sum(xs) / len(xs) if xs else float("nan")


def _write_csv(path, rows):
    if not rows:
        path.write_text("")
        return
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def _scatter(rows, out_dir):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        return
    colors = {"high-split": "tab:red", "mid-split": "tab:orange",
              "high-agreement": "tab:green"}
    fig, ax = plt.subplots(figsize=(6, 6))
    for bucket, c in colors.items():
        sub = [r for r in rows if r["bucket"] == bucket]
        ax.scatter([r["human_ret_1mmodal"] for r in sub],
                   [r["model_1mmodal"] for r in sub],
                   s=18, alpha=0.6, color=c, label=bucket)
    ax.plot([0, 1], [0, 1], "k--", lw=0.8, alpha=0.5)
    ax.set_xlabel("retained human spread (1 - modal share)")
    ax.set_ylabel("model spread (1 - modal share)")
    ax.set_title("Q1: model spread vs human spread (all configs)\n"
                 "coin-flip corner = bottom-right (humans split, model pins)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out_dir / "q1_scatter.png", dpi=130)
    plt.close(fig)


def write_summary(out_dir, q1_corr, res_summary, q2_summary, reasoning_rows):
    L = ["# Pilot summary\n",
         "Feasibility readout, mapped to RESEARCH_PLAN §4.4 pre-committed reads. "
         "Numbers are reported; the merge/reshape/park call is the researcher's.\n",
         "## 1. Q1 pulse (model spread vs RETAINED human spread)\n",
         "Per-config correlation of model spread (1-modal) with retained human "
         "spread. **Signal we want: LOW/negative-ish or flat on hard items — model "
         "spread NOT tracking human spread** (see q1_scatter.png coin-flip corner).\n",
         "| config | n | r(model,retained) | r(model,full) | mean model 1-modal | mean human 1-modal |",
         "|---|---|---|---|---|---|"]
    for r in q1_corr:
        L.append(f"| {r['config_id']} | {r['n_sentences']} | "
                 f"{r['r_1mmodal_vs_retained']:.3f} | {r['r_1mmodal_vs_full']:.3f} | "
                 f"{r['mean_model_1mmodal']:.3f} | {r['mean_human_ret_1mmodal']:.3f} |")

    L += ["\n## 2. Resolution check (KEY) — spread movement 10 -> 5 -> 3 runs\n",
          "Mean |spread(k) - spread(10)| across sentences. Small = 10 runs is "
          "plenty (could go cheaper); large = full study needs deeper sampling.\n",
          "| config | abs-Δ(1-modal) 10v5 | 10v3 | abs-Δ(Hnorm) 10v5 | 10v3 |",
          "|---|---|---|---|---|"]
    for r in res_summary:
        L.append(f"| {r['config_id']} | {r['mean_abs_d_1mmodal_10v5']:.3f} | "
                 f"{r['mean_abs_d_1mmodal_10v3']:.3f} | "
                 f"{r['mean_abs_d_Hnorm_10v5']:.3f} | "
                 f"{r['mean_abs_d_Hnorm_10v3']:.3f} |")

    L += ["\n## 3. Q2 confusion cells\n",
          f"- human confusion pairs (full): {q2_summary['n_human_pairs']} "
          f"(retained: {q2_summary['n_human_retained_pairs']})",
          f"- model confusion pairs (pooled): {q2_summary['n_model_pairs_pooled']}",
          f"- overlap (both): {q2_summary['n_overlap_pairs']}",
          f"- model-only (candidate ALIEN): {q2_summary['n_model_only_pairs']}",
          f"- human-only: {q2_summary['n_human_only_pairs']}",
          "\nDecision input: enough non-empty overlapping cells -> Q2 can be a "
          "headline; sparse -> Q2 is a discussion illustration (pre-authorised).\n",
          "## 4. Reasoning contrast\n",
          (f"{len({r['model'] for r in reasoning_rows})} toggleable model(s); "
           "see reasoning_contrast.csv (spread on vs off, per config)."
           if reasoning_rows else
           "No toggleable models in the probed roster — nothing to contrast."),
          "\n## 5. Exemplars\n",
          "See exemplars.md — three sentences read with the 32-coder receipts.\n",
          "## Map to §4.4\n",
          "- Q1 signal present (human spread varies, model spread stays narrow) -> "
          "merge; Q1 headline; scale up.",
          "- Q1 signal absent (model tracks human) -> finding, reshape toward Q2 / oracle.",
          "- Resolution bad at 10 -> full study needs deeper per-model sampling; recost.",
          "- Q2 cells empty -> Q2 demotes to illustration.",
          "- Exemplars flat -> reconsider mixed-methods selling point."]
    (out_dir / "pilot_summary.md").write_text("\n".join(L) + "\n")


def main():
    out_dir = config.REPORTS_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    if not config.PREDICTIONS_CSV.exists():
        raise SystemExit("No predictions.csv — run `python -m src.pilot.run` first.")

    by_cell, cfg_meta, sent_meta = load_predictions()
    manifest = load_manifest()
    human_codings = load_human_codings()

    q1_rows, q1_corr = q1_pulse(by_cell, cfg_meta, manifest, out_dir)
    res_summary = resolution(by_cell, cfg_meta, out_dir)
    q2_summary, human_pairs, _ = q2_cells(by_cell, sent_meta, human_codings,
                                          manifest, out_dir)
    reasoning_rows = reasoning_contrast(by_cell, cfg_meta, out_dir)
    exemplars(q1_rows, by_cell, cfg_meta, manifest, human_codings, human_pairs, out_dir)
    write_summary(out_dir, q1_corr, res_summary, q2_summary, reasoning_rows)

    print(f"wrote analysis to {out_dir}/:")
    for name in ("q1_pulse.csv", "q1_correlations.csv", "q1_scatter.png",
                 "resolution_per_sentence.csv", "resolution_summary.csv",
                 "q2_confusion_pairs.csv", "reasoning_contrast.csv",
                 "exemplars.md", "pilot_summary.md"):
        p = out_dir / name
        print(f"  {'[ok]' if p.exists() else '[--]'} {name}")


if __name__ == "__main__":
    main()
