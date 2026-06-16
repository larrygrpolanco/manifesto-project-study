"""Render the instruction-parity prompt the model codes from.

The instrument text below is the canonical wording from
src/prompts/coding_instrument.md (system block + scoring rules); the category
list is injected verbatim from categories.json via codebook.render_categories();
the context block is the FULL manifesto extract (locked decision 4): every unit
in sequence order, section headings shown, the target quasi-sentence delimited
»«. The prompt is IDENTICAL across the 10 runs of a sentence — only sampling
temperature varies the output.

    python -m src.pilot.prompt --unit GB-004    # eyeball one rendered prompt
"""

import argparse
import json

from . import config
from .codebook import load_codebook

# --- Canonical instrument text (mirrors src/prompts/coding_instrument.md) ----
_INSTRUCTIONS = (
    "You are coding a single quasi-sentence from a party election manifesto using "
    "the Comparative Manifesto Project (CMP) standard scheme. Assign one and only "
    "one category. Code the manifest statement — what it says — not latent intent "
    "or what you think it will lead to."
)

_SCORING_RULES = (
    "Scoring rules (apply in this spirit):\n"
    "- Read the surrounding paragraph before coding; the context and the section "
    "heading are cues for an otherwise ambiguous argument. (Decision Rules 2, 11)\n"
    "- Code if at all possible; use 000 only when no category applies after "
    "checking the relevant policy domains. (Decision Rule 4)\n"
    "- A connecting / linking sentence with no content of its own takes the "
    "category of the surrounding argument. (Decision Rule 5)\n"
    "- A policy goal beats the policy means used to reach it. (Decision Rule 6)\n"
    "- A specific policy position beats general categories 303 (Efficiency), "
    "305 (Political Authority), and 408 (Economic Goals). (Decision Rules 7, 8, 10)\n"
    "- A specific policy position beats social-group categories (Domain 7) — "
    "except 703: every quasi-sentence about agriculture/farmers is 703, even when "
    "an incentive (402) or growth (410) framing is used. (Decision Rule 9)"
)

_OUTPUT = "Output: the three-digit code only — nothing else."

# Delimiters that mark the target quasi-sentence inside the full extract.
OPEN, CLOSE = "»", "«"


class Corpus:
    """The coding sample indexed for prompt rendering (units + section spans)."""

    def __init__(self):
        data = json.loads(config.SAMPLE_JSON.read_text())
        self.units_by_id = {u["unit_id"]: u for u in data["units"]}
        # manifesto id -> ordered units; and -> ordered sections
        self.units_by_manifesto = {}
        self.sections_by_manifesto = {}
        self.manifesto_name = {}
        for u in data["units"]:
            self.units_by_manifesto.setdefault(u["manifesto"], []).append(u)
        for v in self.units_by_manifesto.values():
            v.sort(key=lambda u: u["sequence"])
        for m in data["metadata"]["manifestos"]:
            self.sections_by_manifesto[m["id"]] = m["sections"]
            self.manifesto_name[m["id"]] = m["name"]

    def render_extract(self, unit_id):
        """Full manifesto extract: section headings + prose, target marked »«."""
        target = self.units_by_id[unit_id]
        mid = target["manifesto"]
        units = self.units_by_manifesto[mid]
        by_id = {u["unit_id"]: u for u in units}
        lines = []
        for sec in self.sections_by_manifesto[mid]:
            # collect this section's units by the first/last span
            span = [u for u in units
                    if sec["first_unit"] <= u["unit_id"] <= sec["last_unit"]]
            if not span:
                continue
            lines.append(f"## {sec['heading']}")
            pieces = []
            for u in span:
                txt = u["text"]
                if u["unit_id"] == unit_id:
                    txt = f"{OPEN}{txt}{CLOSE}"
                pieces.append(txt)
            lines.append(" ".join(pieces))
        return mid, self.manifesto_name[mid], target, "\n\n".join(lines)


def build_messages(unit_id, codebook=None, corpus=None):
    """Return the [system, user] message list for one target unit."""
    cb = codebook or load_codebook()
    corp = corpus or Corpus()
    mid, mname, target, extract = corp.render_extract(unit_id)

    system = "\n\n".join([
        _INSTRUCTIONS,
        "Categories (code — label — definition):\n" + cb.render_categories(),
        _SCORING_RULES,
        _OUTPUT,
    ])
    user = (
        f"Manifesto: {mname}\n"
        f"Section: {target['section']}\n\n"
        "Full extract (the quasi-sentence to code is marked "
        f"{OPEN} {CLOSE}):\n{extract}\n\n"
        f"Quasi-sentence to code: {target['text']}"
    )
    return [{"role": "system", "content": system},
            {"role": "user", "content": user}]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--unit", default="GB-004", help="unit_id to render (e.g. GB-004)")
    args = ap.parse_args()
    msgs = build_messages(args.unit)
    for m in msgs:
        print("=" * 80)
        print(f"[{m['role'].upper()}]  ({len(m['content'])} chars, "
              f"~{len(m['content'])//4} tokens)")
        print("=" * 80)
        print(m["content"])
        print()


if __name__ == "__main__":
    main()
