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

# Domain-level scope statements for HIER2 stage 1. The first hierarchical call
# decides a domain, and in HIER2 a cross-domain error (E1) can ONLY originate
# here -- so this call must be an informed semantic decision, not a match on
# category titles alone. These describe each domain's scope and flag the known
# cross-domain confusions (e.g. education -> Welfare, not Economy). Keyed by
# domain_code; sourced from the MARPOR domain definitions.
DOMAIN_DESCRIPTIONS = {
    1: ("Foreign policy and the country's relations with the outside world: "
        "military and defense, war and peace, foreign alliances and special "
        "relationships, internationalism, the European Union, anti-imperialism, "
        "and foreign aid."),
    2: ("Civil liberties, human rights, democratic institutions and procedures, "
        "and the constitutional framework -- including freedom from state "
        "coercion and arguments for or against the existing constitution."),
    3: ("How domestic government is structured and run: centralization versus "
        "decentralization of power, governmental and administrative efficiency, "
        "political corruption, and the authority and stability of government."),
    4: ("Economic policy and management: free markets and incentives, "
        "regulation, planning, nationalisation, protectionism versus free trade, "
        "economic growth and goals, technology and infrastructure, and the "
        "controlled economy. (Education and the welfare state belong to Welfare, "
        "not here; technical/vocational training for the economy does belong "
        "here.)"),
    5: ("Social services and quality of life: the welfare state and social "
        "services, health care, education, the environment, culture, and social "
        "equality."),
    6: ("National identity and social cohesion: the national way of life, "
        "traditional morality, law and order, civic-mindedness and social "
        "solidarity, and multiculturalism."),
    7: ("Appeals to or statements about specific social and demographic groups: "
        "labour, agriculture and farmers, the middle class and professional "
        "groups, minorities, and other non-economic demographic groups such as "
        "those defined by age, gender, or region."),
    UNCODED_DOMAIN_CODE: ("None of the substantive domains applies -- purely "
                          "procedural, ambiguous, or off-topic statements."),
}


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

    def domain_description(self, domain_code):
        return DOMAIN_DESCRIPTIONS.get(domain_code, "")

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
        """HIER2 stage 1: each domain as code + name + scope definition, with its
        category titles as concrete examples. Leading with the definition makes
        the domain choice a semantic decision rather than a title match."""
        blocks = []
        for dc, dn in self.domains:
            titles = "; ".join(c.title for c in self.categories_in_domain(dc))
            desc = self.domain_description(dc)
            head = f"{dc} — {dn}: {desc}" if desc else f"{dc} — {dn}"
            blocks.append(f"{head}\n   Includes: {titles}")
        return "\n\n".join(blocks)

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
