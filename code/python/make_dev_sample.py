"""Build the development sample: whole manifestos from selected parties.

Unlike a random scatter of quasi-sentences, this keeps *entire manifestos* intact
so that (a) manifesto-level downstream measures (RILE, domain/category salience —
see docs/error_as_spine.md) can actually be computed, and (b) the full sequential
context of each document is preserved for context-sensitivity experiments.

The default selection is a 2x2 design — two countries, each with a left/right
party pair — drawn from the TRAIN split so that val and test stay sealed as clean
evaluation sets:

    61320  US Democratic  (left)     61620  US Republican   (right)
    51320  UK Labour      (left)     51620  UK Conservative  (right)

Within each party, manifestos are spread across the available date range to give a
time series. Output rows are ordered (party, date, pos) so each manifesto is
contiguous and in reading order.

Usage:
    python code/python/make_dev_sample.py
    python code/python/make_dev_sample.py --per-party 3
    python code/python/make_dev_sample.py --parties 61320 61620 51320 51620
    python code/python/make_dev_sample.py --split train --select random --seed 42
"""

import argparse
import csv
import random
import sys
from collections import defaultdict
from pathlib import Path

# Some rows contain very long translated text; lift csv's field-size limit.
csv.field_size_limit(min(sys.maxsize, 2**31 - 1))

DEFAULT_INPUT = Path("data/subsets/by_language/manifesto-pilot-dataset_english.csv")
DEFAULT_OUTDIR = Path("data/subsets/dev_sample")
DEFAULT_PARTIES = ["61320", "61620", "51320", "51620"]

# For human-readable reporting only; arbitrary --parties still work.
PARTY_NAMES = {
    "61320": "US Democratic (left)",
    "61620": "US Republican (right)",
    "51320": "UK Labour (left)",
    "51620": "UK Conservative (right)",
}


def spread_indices(count: int, k: int) -> list[int]:
    """Pick ``k`` indices evenly spaced across ``range(count)``, endpoints included.

    Deterministic; used to spread a party's chosen manifestos across its date range
    (e.g. earliest, middle, latest) rather than clustering them in time.
    """
    if k >= count:
        return list(range(count))
    if k == 1:
        return [count // 2]
    return [round(i * (count - 1) / (k - 1)) for i in range(k)]


def select_manifestos(
    manifestos: list[tuple[str, str]], party: str, k: int, select: str, rng: random.Random
) -> list[str]:
    """Return up to ``k`` manifesto ids for one party, sorted by date.

    ``manifestos`` is a list of (date, manifesto_id) for the party in the target
    split. ``select`` is 'spread' (even temporal coverage) or 'random' (seeded).
    """
    ordered = sorted(manifestos)  # by date, then id
    if len(ordered) < k:
        print(f"  WARNING: party {party} has only {len(ordered)} manifesto(s) in "
              f"split (requested {k}); taking all.", file=sys.stderr)
        return [mid for _, mid in ordered]
    if select == "random":
        chosen = rng.sample(ordered, k)
        return [mid for _, mid in sorted(chosen)]
    return [ordered[i][1] for i in spread_indices(len(ordered), k)]


def make_dev_sample(
    input_path: Path, outdir: Path, parties: list[str], split: str,
    per_party: int, select: str, seed: int,
) -> Path:
    if not input_path.exists():
        sys.exit(f"Input file not found: {input_path}")

    # --- Pass 1: collect manifesto-level metadata for the requested parties ---
    with input_path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        for col in ("party", "split", "date", "manifesto_id", "pos"):
            if col not in header:
                sys.exit(f"No '{col}' column found. Columns: {header}")
        ix = {c: header.index(c) for c in ("party", "split", "date", "manifesto_id", "pos")}

        want = set(parties)
        # party -> {manifesto_id -> date}
        party_mans: dict[str, dict[str, str]] = defaultdict(dict)
        for row in reader:
            if not row or row[ix["split"]] != split or row[ix["party"]] not in want:
                continue
            party_mans[row[ix["party"]]][row[ix["manifesto_id"]]] = row[ix["date"]]

    # --- Choose manifestos per party ---
    rng = random.Random(seed)
    selected: set[str] = set()
    plan: list[tuple[str, str, str]] = []  # (party, date, manifesto_id)
    for party in parties:
        mans = [(d, m) for m, d in party_mans.get(party, {}).items()]
        if not mans:
            print(f"  WARNING: no manifestos for party {party} in split '{split}'.",
                  file=sys.stderr)
            continue
        for mid in select_manifestos(mans, party, per_party, select, rng):
            selected.add(mid)
            plan.append((party, party_mans[party][mid], mid))

    if not selected:
        sys.exit("No manifestos selected — check --parties and --split.")

    # --- Pass 2: gather all rows for the selected manifestos ---
    rows_by_man: dict[str, list[list[str]]] = defaultdict(list)
    with input_path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row and row[ix["manifesto_id"]] in selected:
                rows_by_man[row[ix["manifesto_id"]]].append(row)

    # Order: by party, date, manifesto; within a manifesto, by pos (reading order).
    def pos_key(row: list[str]) -> tuple:
        raw = row[ix["pos"]]
        try:
            return (0, float(raw))
        except ValueError:
            return (1, raw)  # non-numeric pos sorts after, stably

    outdir.mkdir(parents=True, exist_ok=True)
    out_path = outdir / f"{input_path.stem}_dev-{split}-{len(parties)}x{per_party}.csv"
    with out_path.open("w", newline="", encoding="utf-8") as out:
        writer = csv.writer(out)
        writer.writerow(header)
        for _party, _date, mid in plan:
            for row in sorted(rows_by_man[mid], key=pos_key):
                writer.writerow(row)

    _report(out_path, split, select, plan, rows_by_man)
    return out_path


def _report(out_path, split, select, plan, rows_by_man) -> None:
    total = sum(len(rows_by_man[m]) for _, _, m in plan)
    print(f"Wrote {len(plan)} manifestos / {total:,} quasi-sentences -> {out_path}")
    print(f"  source split: {split}   selection: {select}\n")
    current = None
    for party, date, mid in plan:
        if party != current:
            print(f"  {party}  {PARTY_NAMES.get(party, '')}")
            current = party
        print(f"     {date}  {mid:<16} {len(rows_by_man[mid]):>5} qs")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT,
                        help="Source CSV (default: %(default)s)")
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR,
                        help="Output directory (default: %(default)s)")
    parser.add_argument("--parties", nargs="+", default=DEFAULT_PARTIES,
                        help="CMP party codes (default: %(default)s)")
    parser.add_argument("--split", default="train", choices=["train", "val", "test"],
                        help="Which split to draw from (default: %(default)s)")
    parser.add_argument("--per-party", type=int, default=3,
                        help="Manifestos per party (default: %(default)s)")
    parser.add_argument("--select", default="spread", choices=["spread", "random"],
                        help="How to pick when a party has more than --per-party "
                             "(default: %(default)s = even temporal spread)")
    parser.add_argument("--seed", type=int, default=42,
                        help="Seed for --select random (default: %(default)s)")
    args = parser.parse_args()

    if args.split == "test":
        print("WARNING: drawing from the TEST split. Keep test sealed until the "
              "taxonomy is locked; use 'train' for development.\n", file=sys.stderr)

    make_dev_sample(args.input, args.outdir, args.parties, args.split,
                    args.per_party, args.select, args.seed)


if __name__ == "__main__":
    main()
