"""Split the large manifesto pilot dataset into per-language CSV subsets.

Streams the source file row by row so memory stays low regardless of file size.
Each output file keeps the original header and is named by language, e.g.
``manifesto-pilot-dataset_english.csv``.

Usage:
    python code/python/split_by_language.py
    python code/python/split_by_language.py --input path/to.csv --outdir out/dir
    python code/python/split_by_language.py --languages english spanish german
"""

import argparse
import csv
import sys
from pathlib import Path

# Some rows contain very long text fields; lift csv's field-size limit.
csv.field_size_limit(min(sys.maxsize, 2**31 - 1))

DEFAULT_INPUT = Path("data/raw/manifesto-pilot-dataset.csv")
DEFAULT_OUTDIR = Path("data/subsets/by_language")
LANGUAGE_COLUMN = "language"


def safe_name(language: str) -> str:
    """Make a language value safe to use in a filename."""
    return "".join(c if c.isalnum() or c in "-_" else "_" for c in language.strip().lower()) or "unknown"


def split_by_language(input_path: Path, outdir: Path, only: set[str] | None) -> None:
    if not input_path.exists():
        sys.exit(f"Input file not found: {input_path}")

    outdir.mkdir(parents=True, exist_ok=True)

    # Map language -> (open file handle, csv.writer). Opened lazily as languages appear.
    writers: dict[str, tuple] = {}
    counts: dict[str, int] = {}

    with input_path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        try:
            lang_idx = header.index(LANGUAGE_COLUMN)
        except ValueError:
            sys.exit(f"No '{LANGUAGE_COLUMN}' column found. Columns: {header}")

        try:
            for row in reader:
                if not row:
                    continue
                language = row[lang_idx]
                if only is not None and language.lower() not in only:
                    continue

                if language not in writers:
                    out_path = outdir / f"{input_path.stem}_{safe_name(language)}.csv"
                    handle = out_path.open("w", newline="", encoding="utf-8")
                    writer = csv.writer(handle)
                    writer.writerow(header)
                    writers[language] = (handle, writer)
                    counts[language] = 0

                writers[language][1].writerow(row)
                counts[language] += 1
        finally:
            for handle, _ in writers.values():
                handle.close()

    print(f"Wrote {len(counts)} language file(s) to {outdir}/:")
    for language in sorted(counts, key=lambda k: counts[k], reverse=True):
        print(f"  {language:<12} {counts[language]:>9,} rows")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="Source CSV (default: %(default)s)")
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR, help="Output directory (default: %(default)s)")
    parser.add_argument(
        "--languages",
        nargs="+",
        default=None,
        help="Only export these languages (case-insensitive). Default: all.",
    )
    args = parser.parse_args()

    only = {lang.lower() for lang in args.languages} if args.languages else None
    split_by_language(args.input, args.outdir, only)


if __name__ == "__main__":
    main()
