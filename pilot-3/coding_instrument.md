# CMP coding instrument (model prompt) — draft

The model prompt is built to match what the MLB human coders received, so any
human–model gap is about *coding*, not about being handed a different instrument.

**Parity commitments (these are the design, and the rationale belongs in the paper):**

1. **Full option space.** The model is offered all **56 standard categories + `000` uncoded**, with the handbook's definitions (injected from [categories.json](categories.json))
2. **Pre-unitised.** Quasi-sentences are given, as they were to the coders. The model never unitises.
3. **`000` is live.** Uncoded was a selectable option on the coders' menu and has its own decision procedure; the model is offered it too.
4. **No answer key.** The manual prints these exact texts *with* margin codes (Appendix II / section 5). That worked solution is excluded from the prompt.
5. **Decision rules carried.** The scoring rules that tell both sides how to resolve ambiguity travel in the prompt (below).

**The parity we cannot grant — state as a limitation.** The humans had prior CMP
training and a Berlin supervisor to email; the model has the handbook in context
only. The asymmetry favours the human, which only sharpens a finding that models
manufacture agreement where trained humans split.

**Two conditions share this instrument; only the CONTEXT block differs.**
- `in_context` (human-parity, primary for RQ3): the unit's section heading + its surrounding paragraph (and the full extract is available).
- `sentence_only` (degraded contrast): the quasi-sentence alone, no heading, no neighbours.

---

## System / instructions block (identical across conditions)

You are coding a single quasi-sentence from a party election manifesto using the
Comparative Manifesto Project (CMP) standard scheme. Assign **one and only one**
category. Code the **manifest statement — what it says — not latent intent** or
what you think it will lead to.

Categories (code — label — definition): *[injected verbatim from `categories.json`:
all 56 standard categories + `000`]*

Scoring rules (apply in this spirit):
- **Read the surrounding paragraph before coding; the context and the section heading are cues** for an otherwise ambiguous argument. *(Decision Rules 2, 11)*
- **Code if at all possible**; use `000` only when no category applies after checking the relevant policy domains. *(Decision Rule 4)*
- A **connecting / linking sentence** with no content of its own takes the category of the surrounding argument. *(Decision Rule 5)*
- A **policy goal beats the policy means** used to reach it. *(Decision Rule 6)*
- A **specific policy position beats** general categories **303** (Efficiency), **305** (Political Authority), and **408** (Economic Goals). *(Decision Rules 7, 8, 10)*
- A **specific policy position beats social-group categories (Domain 7) — except 703**: every quasi-sentence about agriculture/farmers is **703**, even when an incentive (402) or growth (410) framing is used. *(Decision Rule 9)*

Output: the three-digit code only.

---

## Context block — `in_context`

Manifesto: {manifesto_name}
Section: {section}

Paragraph (the quasi-sentence to code is marked » «):
{paragraph_with_target_marked}

Quasi-sentence to code: {unit_text}

---

## Context block — `sentence_only`

Quasi-sentence to code: {unit_text}

---

## Build notes

- `{section}`, `{unit_text}`, manifesto name, and unit ordering come from [cmp_coding_sample.json](cmp_coding_sample.json) (`section` field per unit; `metadata.manifestos[].sections` for spans).
- `{paragraph_with_target_marked}`: the contiguous run of units sharing the target's `section` (or a tighter paragraph window) presented in unit-sequence order, with the target unit delimited. Open design choice — see RESEARCH_PLAN §5.2 (whole-document vs target-in-context call structure).
- Category block is generated from `categories.json` so the list, labels, and definitions are single-sourced and never drift from the rile mapping.
- The output is parsed to a three-digit string; anything else (refusal, multi-code, prose) is logged raw for the same entropy/“off-scheme” handling applied to human `000`/off-gold codes.
