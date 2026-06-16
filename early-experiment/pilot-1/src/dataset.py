"""Load the input sample as a list of items, independent of the source CSV's schema.

Only a text column and a gold main-code column are required (see config.COLUMNS).
The gold domain is derived from the gold code via the codebook, so a bare
text+code CSV works without further mapping. A stable per-row id is composed from
config.ID_COLUMNS (falling back to the row index) so caching survives reordering.
"""

import csv
import sys
from dataclasses import dataclass
from pathlib import Path

csv.field_size_limit(min(sys.maxsize, 2**31 - 1))


@dataclass
class Item:
    id: str
    text: str
    gold_code: str
    gold_domain_code: int
    gold_domain_name: str


def load_items(input_csv: Path, columns: dict, id_columns, codebook) -> list:
    text_col = columns["text"]
    code_col = columns["gold_code"]
    items, unknown = [], set()
    with open(input_csv, newline="") as f:
        reader = csv.DictReader(f)
        have_id = id_columns and all(c in reader.fieldnames for c in id_columns)
        for i, r in enumerate(reader):
            code = r[code_col].strip()
            dc, dn = codebook.domain_of(code)
            if dc is None:
                unknown.add(code)
            rid = "-".join(str(r[c]).strip() for c in id_columns) if have_id else str(i)
            items.append(Item(
                id=rid,
                text=r[text_col].strip(),
                gold_code=code,
                gold_domain_code=dc if dc is not None else -1,
                gold_domain_name=dn if dn is not None else "UNKNOWN",
            ))
    if unknown:
        print(f"WARNING: {len(unknown)} gold code(s) not in codebook: {sorted(unknown)}",
              file=sys.stderr)
    if len({it.id for it in items}) != len(items):
        print("WARNING: item ids are not unique; falling back to row index.", file=sys.stderr)
        for i, it in enumerate(items):
            it.id = str(i)
    return items
