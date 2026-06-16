"""Load the CMP category scheme and render the category block the model sees.

Ported from archive/early-experiment/pilot-2/codebook.py, but reads the newer
data/categories.json (the authoritative 56 + 000 option space with rile mapping)
instead of pilot-2's codebook.csv. This is the single source of truth for *what
category text the model sees* — the block is injected verbatim into the parity
prompt so the list, labels, definitions, and rile mapping never drift.

    python -m src.pilot.codebook        # dump the rendered block to eyeball it
"""

import json
from dataclasses import dataclass

from . import config


@dataclass
class Category:
    code: str            # "504", "000"
    label: str           # "Welfare State Expansion"
    domain: int          # 0..7 (0 = Uncoded / 000)
    rile: str            # "left" | "right" | "none"
    definition: str


class Codebook:
    def __init__(self, categories, domain_names):
        self.categories = categories                 # list[Category], file order
        self.by_code = {c.code: c for c in categories}
        self.domain_names = domain_names             # {int: str}

    @property
    def allowed_codes(self):
        return set(self.by_code)

    def rile_of(self, code):
        c = self.by_code.get(code)
        return c.rile if c else None

    def domain_of(self, code):
        c = self.by_code.get(code)
        return c.domain if c else None

    def label_of(self, code):
        c = self.by_code.get(code)
        return c.label if c else None

    def _domain_order(self):
        """Domains 1..7 in numeric order, then domain 0 (Uncoded / 000) last."""
        present = sorted({c.domain for c in self.categories})
        return sorted(present, key=lambda d: (d == 0, d))

    def render_categories(self):
        """The category block: `code — label — definition`, grouped by domain.

        Matches the coding_instrument.md contract: all 56 standard categories
        + 000, with handbook definitions, single-sourced from categories.json.
        """
        blocks = []
        for d in self._domain_order():
            name = self.domain_names.get(d, "Uncoded" if d == 0 else f"Domain {d}")
            header = f"### Domain {d} — {name}"
            entries = [
                f"{c.code} — {c.label} — {c.definition}"
                for c in self.categories if c.domain == d
            ]
            blocks.append(header + "\n" + "\n".join(entries))
        return "\n\n".join(blocks)


def load_codebook(path=None) -> Codebook:
    data = json.loads((path or config.CATEGORIES_JSON).read_text())
    domain_names = {int(k): v for k, v in data["metadata"]["domains"].items()}
    domain_names.setdefault(0, "Uncoded")
    cats = [
        Category(code=code, label=c["label"], domain=int(c["domain"]),
                 rile=c["rile"], definition=c["definition"].strip())
        for code, c in data["categories"].items()
    ]
    return Codebook(cats, domain_names)


if __name__ == "__main__":
    cb = load_codebook()
    block = cb.render_categories()
    print(f"# {len(cb.categories)} categories across "
          f"{len(cb._domain_order())} domain groups; "
          f"block is {len(block)} chars (~{len(block)//4} tokens)\n")
    print(block)
