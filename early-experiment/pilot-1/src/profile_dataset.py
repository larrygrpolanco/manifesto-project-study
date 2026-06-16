"""Profile the input sample before any model is run.

Answers the 'understand the dataset' goal directly: how the gold labels are
distributed across categories and domains, which categories never appear, how the
valence pairs and catch-all categories are represented, text length, and how much
class imbalance there is. Also a back-of-envelope note on how much statistical
power n items gives the paired condition tests.

    python src/profile_dataset.py
    python src/profile_dataset.py --input ../some_other_sample.csv

Writes reports/dataset_profile.md and reports/category_counts.csv.
"""

import argparse
import csv
import statistics
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

import config
from codebook import load_codebook
from dataset import load_items


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", type=Path, default=config.INPUT_CSV)
    args = ap.parse_args()

    cb = load_codebook(config.CODEBOOK_CSV, config.VALENCE_PAIRS_CSV)
    items = load_items(args.input, config.COLUMNS, config.ID_COLUMNS, cb)
    n = len(items)

    code_counts = Counter(it.gold_code for it in items)
    dom_counts = Counter((it.gold_domain_code, it.gold_domain_name) for it in items)
    lengths = [len(it.text.split()) for it in items]

    substantive = [c for c in cb.categories if c.code != config.UNCODED_CODE]
    present = {c.code for c in substantive if code_counts.get(c.code)}
    absent = [c for c in substantive if not code_counts.get(c.code)]
    catch_in_gold = sum(v for k, v in code_counts.items() if k in config.CATCH_ALL_CODES)

    # category counts csv
    config.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(config.REPORTS_DIR / "category_counts.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["code", "title", "domain", "count", "pct"])
        for c in cb.categories:
            cnt = code_counts.get(c.code, 0)
            w.writerow([c.code, c.title, c.domain_name, cnt, round(100 * cnt / n, 2)])

    L = []
    L.append(f"# Dataset profile — `{args.input.name}`\n")
    L.append(f"- **Items:** {n}")
    L.append(f"- **Categories present:** {len(present)} / {len(substantive)} substantive "
             f"(+ uncoded option not used in gold)")
    L.append(f"- **Text length (whitespace tokens):** median {statistics.median(lengths):.0f}, "
             f"mean {statistics.mean(lengths):.1f}, min {min(lengths)}, max {max(lengths)}\n")

    L.append("## Domain distribution\n")
    L.append("| Domain | Items | % |\n|---|---:|---:|")
    for (dc, dn), cnt in sorted(dom_counts.items(), key=lambda kv: -kv[1]):
        L.append(f"| {dn} | {cnt} | {100*cnt/n:.1f} |")

    counts_present = [code_counts[c] for c in present]
    singletons = sum(1 for c in present if code_counts[c] == 1)
    L.append("\n## Class imbalance\n")
    L.append(f"- Per-category counts (present only): min {min(counts_present)}, "
             f"median {statistics.median(counts_present):.0f}, max {max(counts_present)}")
    L.append(f"- Categories with a single example: {singletons}")
    L.append(f"- **Most frequent:** " + ", ".join(
        f"{c} ({code_counts[c]})" for c, _ in code_counts.most_common(8)))

    L.append("\n## Most frequent categories\n")
    L.append("| Code | Title | Count | % |\n|---|---|---:|---:|")
    for c, cnt in code_counts.most_common(12):
        L.append(f"| {c} | {cb.by_code[c].title} | {cnt} | {100*cnt/n:.1f} |")

    L.append("\n## Absent substantive categories "
             f"({len(absent)})\n")
    L.append(", ".join(f"{c.code} {c.title}" for c in absent) or "_none_")

    L.append("\n## Valence-pair representation (error type E2)\n")
    L.append("Both members must appear for a valence *flip* to be observable.\n")
    L.append("| Pair | + code (n) | − code (n) | flip observable? |\n|---|---|---|:--:|")
    for pos, neg, label in cb.valence_pairs:
        p, q = code_counts.get(pos, 0), code_counts.get(neg, 0)
        L.append(f"| {label} | {pos} ({p}) | {neg} ({q}) | {'yes' if p and q else 'no'} |")

    L.append("\n## Catch-all categories (error type E5)\n")
    L.append(f"Catch-all codes: {sorted(config.CATCH_ALL_CODES)}. "
             f"Gold items sitting in a catch-all category: {catch_in_gold} "
             f"({100*catch_in_gold/n:.1f}%). Note 000 never appears in gold, so any 000 "
             f"prediction is over-abstention.")

    L.append("\n## Power note\n")
    L.append(f"Condition comparisons are paired McNemar tests over {n} items. McNemar's "
             "power depends only on the *discordant* pairs (items where two conditions "
             "disagree). Rough guide at n="
             f"{n}, α=.05, power≈.8: you can detect a difference if roughly ≥25–35 items "
             "flip net one way. Per-*category* effects will be underpowered "
             f"({singletons} categories have a single example); the well-powered tests are "
             "on **overall accuracy and compliance** per condition.")

    out = config.REPORTS_DIR / "dataset_profile.md"
    out.write_text("\n".join(L) + "\n")
    print("\n".join(L))
    print(f"\nwrote {out}\nwrote {config.REPORTS_DIR / 'category_counts.csv'}")


if __name__ == "__main__":
    main()
