"""Parse the Manifesto codebook and render the codebook block the model sees.

This is the single source of truth for *what codebook text the model sees*.
Pilot-2 holds the codebook presentation constant across every condition: the
model always sees the full set of MARPOR main categories grouped by policy
domain (render_hier1), each with its full definition. Only the document context
around the target sentence changes between conditions (see config.py). Keeping
the block here (rather than inline in the runner) makes it auditable: run this
file directly to dump the exact block to reports/ and eyeball it.

    python src/codebook.py            # writes reports/prompt_blocks_preview.md
"""

import csv
import sys
from dataclasses import dataclass
from pathlib import Path

csv.field_size_limit(min(sys.maxsize, 2**31 - 1))

# Order domains by code 1..7, then the uncoded "domain" (code 0) last.
UNCODED_DOMAIN_CODE = 0


@dataclass
class Category:
    code: str            # "504", "000"
    title: str           # "Welfare State Expansion"
    domain_code: int     # 0..7
    domain_name: str     # "Welfare and Quality of Life" ("Uncoded" for 000)
    description: str      # cleaned full description_md


def _clean(md: str) -> str:
    """Light cleanup of description_md for prompting: unescape \\_ \\* and trim."""
    return md.replace("\\_", "_").replace("\\*", "*").strip()


class Codebook:
    def __init__(self, categories, valence_pairs):
        self.categories = categories                       # list[Category], file order
        self.by_code = {c.code: c for c in categories}
        self.valence_pairs = valence_pairs                 # list[(pos, neg, label)]
        # set of frozenset({a, b}) for O(1) valence-flip lookup
        self._valence_sets = {frozenset((p, n)) for p, n, _ in valence_pairs}
        # ordered list of (domain_code, domain_name)
        seen = {}
        for c in categories:
            seen.setdefault(c.domain_code, c.domain_name)
        self.domains = sorted(seen.items(),
                              key=lambda kv: (kv[0] == UNCODED_DOMAIN_CODE, kv[0]))

    # --- lookups ------------------------------------------------------------
    @property
    def allowed_codes(self):
        return set(self.by_code)

    def domain_of(self, code):
        c = self.by_code.get(code)
        return (c.domain_code, c.domain_name) if c else (None, None)

    def is_valence_flip(self, true_code, pred_code):
        return frozenset((true_code, pred_code)) in self._valence_sets

    def categories_in_domain(self, domain_code):
        return [c for c in self.categories if c.domain_code == domain_code]

    # --- prompt block -------------------------------------------------------
    def render_hier1(self):
        """The codebook block: full descriptions grouped under domain headers."""
        blocks = []
        for dc, dn in self.domains:
            cats = self.categories_in_domain(dc)
            header = f"### DOMAIN {dc} — {dn}"
            body = "\n\n".join(self._entry(c, indent="  ") for c in cats)
            blocks.append(f"{header}\n{body}")
        return "\n\n".join(blocks)

    @staticmethod
    def _entry(c: Category, indent=""):
        head = f"{indent}{c.code}: {c.title}"
        desc = c.description.replace("\n", "\n" + indent) if indent else c.description
        return f"{head}\n{indent}{desc}" if desc else head


def load_codebook(codebook_csv: Path, valence_csv: Path) -> Codebook:
    cats = []
    with open(codebook_csv, newline="") as f:
        for r in csv.DictReader(f):
            if r["type"] != "main":
                continue
            dc = int(r["domain_code"])
            dn = r["domain_name"]
            if dn in ("", "NA"):
                dn = "Uncoded"
            cats.append(Category(
                code=r["code"].strip(),
                title=r["title"].strip(),
                domain_code=dc,
                domain_name=dn,
                description=_clean(r["description_md"]),
            ))
    pairs = []
    with open(valence_csv, newline="") as f:
        for r in csv.DictReader(f):
            pairs.append((r["pos_code"].strip(), r["neg_code"].strip(), r["label"]))
    return Codebook(cats, pairs)


def _preview():
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    import config
    cb = load_codebook(config.CODEBOOK_CSV, config.VALENCE_PAIRS_CSV)
    out = config.REPORTS_DIR / "prompt_blocks_preview.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    block = cb.render_hier1()
    parts = [
        "# Prompt block preview\n",
        f"{len(cb.categories)} categories, {len(cb.domains)} domains, "
        f"{len(cb.valence_pairs)} valence pairs. "
        f"Codebook block: {len(block)} chars (~{len(block) // 4} tokens).\n",
        "## CATEGORIES BY DOMAIN (the constant block shown in every condition)\n"
        "```\n" + block + "\n```",
    ]
    out.write_text("\n\n".join(parts))
    print(f"wrote {out}")


if __name__ == "__main__":
    _preview()
