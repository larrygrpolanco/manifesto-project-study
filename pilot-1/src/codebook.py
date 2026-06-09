"""Parse the Manifesto codebook and render the per-condition prompt blocks.

This is the single source of truth for *what codebook text the model sees* in
each condition. Keeping it here (rather than inline in the runner) makes the
information/structure manipulation auditable: run this file directly to dump the
exact blocks to reports/ and eyeball them.

    python src/codebook.py            # writes reports/prompt_blocks_preview.md

Conditions:
    LABELS  flat, "code: title" only                       (information: minimal)
    FULL    flat, "code: title" + full description          (information: full)
    HIER1   full descriptions grouped under domain headers  (structure: presentation)
    HIER2   two stages -> render_domain_menu() then          (structure: decomposition)
            render_domain_categories(domain_code)
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

    def domain_name(self, domain_code):
        for dc, dn in self.domains:
            if dc == domain_code:
                return dn
        return None

    # --- prompt blocks ------------------------------------------------------
    def render_labels(self):
        """LABELS condition: code + title only."""
        return "\n".join(f"{c.code}: {c.title}" for c in self.categories)

    def render_full(self):
        """FULL condition: code + title + full description, flat."""
        return "\n\n".join(self._entry(c) for c in self.categories)

    def render_hier1(self):
        """HIER1: full descriptions grouped under domain headers (single call)."""
        blocks = []
        for dc, dn in self.domains:
            cats = self.categories_in_domain(dc)
            header = f"### DOMAIN {dc} — {dn}"
            body = "\n\n".join(self._entry(c, indent="  ") for c in cats)
            blocks.append(f"{header}\n{body}")
        return "\n\n".join(blocks)

    def render_domain_menu(self):
        """HIER2 stage 1: each domain as code + name + its category titles."""
        lines = []
        for dc, dn in self.domains:
            titles = "; ".join(c.title for c in self.categories_in_domain(dc))
            lines.append(f"{dc} — {dn}: {titles}")
        return "\n".join(lines)

    def render_domain_categories(self, domain_code):
        """HIER2 stage 2: full entries for one domain's categories."""
        cats = self.categories_in_domain(domain_code)
        return "\n\n".join(self._entry(c) for c in cats)

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
    parts = [
        "# Prompt block preview\n",
        f"{len(cb.categories)} categories, {len(cb.domains)} domains, "
        f"{len(cb.valence_pairs)} valence pairs.\n",
        "## LABELS\n```\n" + cb.render_labels() + "\n```",
        "## FULL (first 2 entries)\n```\n"
        + "\n\n".join(cb._entry(c) for c in cb.categories[:2]) + "\n```",
        "## HIER2 stage-1 domain menu\n```\n" + cb.render_domain_menu() + "\n```",
    ]
    out.write_text("\n\n".join(parts))
    print(f"wrote {out}")


if __name__ == "__main__":
    _preview()
