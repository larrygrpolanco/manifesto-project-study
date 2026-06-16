"""Apply the frozen selection rule and freeze runs/pilot/sentence_manifest.csv.

Rule (PILOT_PLAN.md, locked decision 3):
  - Rank all 179 sentences by full_class_cat_1mmodal (000 kept as a class).
  - high-split      = top BUCKET_N
  - mid-split       = BUCKET_N around the median
  - high-agreement  = bottom BUCKET_N
  - Identify the balanced-RILE coin-flips (rile votes span all three classes
    AND no single class > ~43% of votes) and force-include them in high-split
    *only if* they aren't already there.

No tunable knobs at call time — every parameter is a named constant in config.
The balanced-RILE count and the resulting bucket sizes are PRINTED, not assumed:
if force-include pushes high-split past BUCKET_N (it does with the Step-0 data —
the 4 balanced cases sit just below the top-10 cliff), the total exceeds 30 and
the script says so rather than silently trimming.

    python -m src.pilot.select_sentences
"""

import csv
import json

from . import config


def _read_ambiguity():
    with open(config.AMBIGUITY_CSV, newline="") as f:
        return list(csv.DictReader(f))


def _sample_text_section():
    """unit_id -> (text, section) from the coding sample."""
    units = json.loads(config.SAMPLE_JSON.read_text())["units"]
    return {u["unit_id"]: (u["text"], u["section"]) for u in units}


def _bucket_ranges(ranked):
    """Return (high, mid, low) lists of rows by the frozen rank rule."""
    n = len(ranked)
    high = ranked[: config.BUCKET_N]
    low = ranked[-config.BUCKET_N:]
    mid_start = (n // 2) - (config.BUCKET_N // 2)
    mid = ranked[mid_start: mid_start + config.BUCKET_N]
    return high, mid, low


def _balanced_rile(rows):
    """Rows whose RILE votes span all 3 classes with no class > ~max-share."""
    out = []
    for r in rows:
        distinct = int(r["full_class_rile_distinct"])
        modal_share = 1.0 - float(r["full_class_rile_1mmodal"])
        if (distinct == config.BALANCED_RILE_DISTINCT
                and modal_share <= config.BALANCED_RILE_MAX_MODAL_SHARE):
            out.append(r)
    # Most-balanced first (smallest modal share).
    return sorted(out, key=lambda r: 1.0 - float(r["full_class_rile_1mmodal"]))


def select():
    rows = _read_ambiguity()
    # Deterministic rank: by metric desc, unit_id asc to break ties stably.
    ranked = sorted(rows, key=lambda r: (-float(r[config.RANK_COLUMN]), r["unit_id"]))
    high, mid, low = _bucket_ranges(ranked)

    high_ids = {r["unit_id"] for r in high}
    mid_ids = {r["unit_id"] for r in mid}
    low_ids = {r["unit_id"] for r in low}

    balanced = _balanced_rile(rows)
    forced = [r for r in balanced if r["unit_id"] not in high_ids]

    print(f"balanced-RILE coin-flips (rile_distinct=={config.BALANCED_RILE_DISTINCT}, "
          f"modal_share<={config.BALANCED_RILE_MAX_MODAL_SHARE}): {len(balanced)} found")
    for r in balanced:
        share = 1.0 - float(r["full_class_rile_1mmodal"])
        where = "in top-10" if r["unit_id"] in high_ids else "FORCED into high-split"
        print(f"    {r['unit_id']}  rile modal_share={share:.2f}  "
              f"cat_1mmodal={float(r[config.RANK_COLUMN]):.2f}  [{where}]")
    if len(balanced) != 4:
        print(f"  NOTE: plan names 4 balanced-RILE cases; data yields {len(balanced)}. "
              f"Threshold is config.BALANCED_RILE_MAX_MODAL_SHARE — adjust deliberately, "
              f"not to hit a target.")

    # Assemble buckets. Force-included balanced rows extend high-split (the plan
    # says force-include, not replace), so high-split may exceed BUCKET_N.
    high_full = high + forced
    selected, seen = [], set()
    for bucket, group in (("high-split", high_full), ("mid-split", mid),
                          ("high-agreement", low)):
        for r in group:
            if r["unit_id"] in seen:        # a row only ever lands in one bucket
                continue
            seen.add(r["unit_id"])
            selected.append((bucket, r))
    return selected


def write_manifest(selected):
    text_section = _sample_text_section()
    config.SENTENCE_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = (["unit_id", "bucket", "manifesto", "sequence", "section", "text",
                   "master_code", "master_rile"] + config.MANIFEST_METRIC_COLUMNS)
    with open(config.SENTENCE_MANIFEST, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for bucket, r in selected:
            text, section = text_section[r["unit_id"]]
            row = {"unit_id": r["unit_id"], "bucket": bucket,
                   "manifesto": r["manifesto"], "sequence": r["sequence"],
                   "section": section, "text": text,
                   "master_code": r["master_code"], "master_rile": r["master_rile"]}
            for col in config.MANIFEST_METRIC_COLUMNS:
                row[col] = r[col]
            w.writerow(row)
    return fieldnames


def main():
    selected = select()
    write_manifest(selected)

    # Report bucket sizes and GB/NZ split (reported, never quota'd).
    from collections import Counter
    buckets = Counter(b for b, _ in selected)
    manifestos = Counter(r["manifesto"] for _, r in selected)
    print()
    print(f"wrote {config.SENTENCE_MANIFEST}")
    print(f"  total sentences: {len(selected)}")
    for b in ("high-split", "mid-split", "high-agreement"):
        print(f"    {b}: {buckets[b]}")
    print(f"  GB/NZ split: " + ", ".join(f"{m}={c}" for m, c in sorted(manifestos.items())))
    if len(selected) != 30:
        print(f"  NOTE: total is {len(selected)}, not 30 — force-included balanced-RILE "
              f"cases sit below the top-{config.BUCKET_N} cliff, so high-split is larger. "
              f"This is faithful to the locked rule (force-include, don't trim).")


if __name__ == "__main__":
    main()
