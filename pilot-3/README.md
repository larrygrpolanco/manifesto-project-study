# Does LLM error track human disagreement? A matched item-level test on CMP coding

A self-contained study built on the one place in the Manifesto/CMP world where the
same sentences were coded by many humans: the Mikhaylov, Laver & Benoit (2012)
reliability experiment. Every sentence in that experiment carries a *distribution* of
human codes, which means it carries a measurable **ambiguity score**. We run current
LLMs over the exact same sentences and ask one question.

> **Status:** design locked, data verified on disk, no LLM runs yet. The human side is
> fully in hand (texts + gold + per-sentence human distributions, alignment confirmed).
> The next step is the LLM collection described below.

## The question

The Manifesto coding scheme is a task where trained human coders disagree constantly:
Mikhaylov, Laver & Benoit (2012) report Fleiss's κ of **0.31–0.36** at the category
level and median coder-vs-gold Cohen's κ of **0.43–0.54**. A large share of what any
accuracy metric scores as "LLM error" on this task may therefore be **irreducible task
ambiguity** — category boundaries that expert humans themselves cross — rather than
model deficiency.

**Central question.** *Does the structure of LLM error align, sentence by sentence,
with the structure of human coder disagreement?*

The unit of analysis is the **sentence**. For each of the 179 experiment sentences we
have, from the human side, a distribution over codes (hence an entropy / disagreement
score), and from the LLM side, a distribution over codes across models and runs. The
two distributions are directly comparable because they describe the *same sentence*.

Two outcomes, both publishable, fixed in advance:

- **Aligned** → LLMs err where humans disagree. The low headline accuracy is largely a
  property of the *instrument* (porous codebook boundaries), not the models. This is a
  measurement-validity result that ages independently of which model is current.
- **Misaligned** → LLMs fail on sentences humans agree on. That residual is genuine
  model defect and is exactly where prompting / fine-tuning effort should go.

The dependent variable is **error structure and its alignment with human disagreement**,
not accuracy against gold.

## Why this design (and what it drops)

This is a *matched, paired* design from the start: same sentences, human and machine.
We deliberately do **not** compare against earlier unmatched confusion matrices from
unrelated runs — different sentences, different setup, and different category coverage
make any geometric "rhyme" between them unfalsifiable. The paired item-level test is
the contribution, so it is the whole study.

## The data (verified on disk)

The source for the sentence texts is **Volkens (2002), *Manifesto Coding Instructions
(Second Revised Edition)*, WZB Discussion Paper FS III 02-201**, Section 5 ("Coding
Exercise"), pp. 19–24. Both experiment texts appear there fully unitized (quasi-sentence
boundaries marked with `/`) with the gold CMP code printed against each quasi-sentence.

| document | source (pp.) | sentences | human coders (raw) | (coder→gold) pairs |
|---|---|---:|---:|---:|
| GB: Liberal/SDP Alliance 1983, "Working together for Britain" | App. §5, pp. 19–20 | 107 | 32 | 3,424 |
| NZ: National Party 1972 | App. §5, pp. 20–24 | 72 | 23 | 1,656 |

Verification done: the gold vectors in `master-codersGB.txt` (107 codes, leading
`0 0 0 305 305 606 305 410 408 …`) and `master-codersNZ.txt` (72 codes,
`414 414 414 414 414 408 408 402 …`) match the printed appendix codes in coding order,
and every coder row in `codes.log` (32 coders) and `codesNZ.log` (23 coders) has exactly
107 / 72 code columns. Alignment of text → gold → human distribution is therefore
mechanical, not inferred.

**The crown jewel.** Because ~30 / ~23 coders coded the *same* sentences, every sentence
carries a full distribution of human codes → a per-sentence ambiguity score (entropy /
modal-share), not just an aggregate reliability number. This is what makes the item-level
test possible and is not reproducible from any other CMP data.

### Coding scheme: use the period-correct 56-category frame

The texts were coded under the original **56-category (v1–v4) frame**, which is the frame
the Volkens (2002) handbook documents in full (Table 1 + §7 definitions). Do **not**
source codes or a codebook from the current MARPOR corpus: version 5 split several
categories (e.g. 202→202/202_2, 605→605/605_2, 703→703/703_2) and the modern releases
recombine them for back-comparability. Sourcing from anywhere but the contemporaneous
handbook risks v5-split codes that do not line up with the 2008-era gold. The handbook's
56-category list and definitions go straight into `data/codebook.csv` with the 7-domain
map.

### Coverage is a boundary condition, not a caveat

The two texts exercise only ~20 of 57 categories (19 in GB, +1 unique in NZ). This is the
full extent of the only multiply-coded CMP data in existence; it bounds the study to those
categories and we state that up front. Per-category claims live or die on those ~20.

### The codebook already predicts where ambiguity lives

The handbook's own tie-break rules (§4.2.2) tell us in advance which boundaries are porous
— a prior we test against both the human distributions and the LLM distributions:
- **DR5:** specific policy beats Domain-7 group codes (except 703) → group codes bleed.
- **DR6:** specific policy beats 305 (Political Authority) → 305 is a dumping ground.
- **DR7:** specific policy beats 408 (General Economic Goals) → 408 is a dumping ground.
These are testable predictions about *where* both humans and models should scatter.

## Plan

### Step 1 — Human ambiguity profile (no API; data in hand)

From the logs + gold alone, build the reference layer every later step depends on:

1. **Per-sentence human distribution** over the 56 categories and over the 7 domains,
   for all 179 sentences.
2. **Per-sentence ambiguity score:** normalized Shannon entropy of the human codes, and
   (1 − modal share). Report both; decide `000`/uncoded handling explicitly (see Open).
3. **Per-category human reliability:** Fleiss's κ per category, and raw human agreement
   per category — the achievable human ceiling, category by category.
4. **Human confusion matrix** (coder→gold) at 56-category and 7-domain levels, plus the
   reduced 3×3 Rile matrix, to characterize *where* humans send their disagreement.

Apply the MLB coder-quality screen so results are comparable to the paper: the original
`CMP_reliability_replication.R` lists exactly which coders were dropped (17 retained GB,
12 retained NZ). Compute everything **twice** — full pool (a realistic "crowd" ceiling)
and the trained/retained subset (the expert ceiling) — and report both.

### Step 2 — Fresh LLM collection over the same 179 sentences

Run current models over the exact 179 GB/NZ sentences, producing, per sentence, a
distribution of LLM codes across models × runs (multiple samples per model so the
machine side has its own *disagreement* measure, mirroring the humans).

- **Conditions:** hold the prompt design fixed and vary only what the question needs —
  at minimum sentence-only vs sentence-in-document-context, since context is exactly what
  a human coder uses to resolve an ambiguous quasi-sentence (handbook §4.2.2c).
- **Sampling:** N samples per (model, sentence, condition) at non-zero temperature, to
  estimate cross-run model disagreement per sentence.
- **Models:** a current frontier set; record exact model strings + dates for reproducibility.

### Step 3 — Alignment tests (the paper)

Paired, item-level, on the matched 179:

1. **Error ~ human ambiguity.** Logistic regression of LLM-error (vs gold) on per-sentence
   human entropy, with model + condition effects. Aligned ⇒ positive slope.
2. **Disagreement ~ disagreement.** Does *cross-model* LLM disagreement track *cross-coder*
   human disagreement on the same sentence? (Correlation of the two per-sentence entropies.)
   This is the cleanest version of the question and needs no privileged gold.
3. **Human-ceiling-relative scoring.** Report LLM accuracy per category against the *human
   agreement rate* for that category, not against 100%.
4. **Where the mass goes.** Do LLMs dump off-diagonal into the same cells humans do
   (305 / 408 / group codes, per DR5–7)? Compare off-diagonal structure of the human and
   LLM confusion matrices on the shared ~20 categories.

## Open decisions

- **`000`/uncoded.** Treat as a 57th class, or exclude? It is both common and unreliable
  in the human data (the paper flags β≈0.55 for uncoded), so it is substantively
  interesting — lean toward keeping it as a class and reporting with/without.
- **Gold is one authority, not ground truth.** Report alignment tests both gold-relative
  (comparable to the literature) and gold-free (coder-consensus vs model-consensus, test 2
  above), and treat the gold-free version as the honest headline.
- **Sampling budget.** N per (model, sentence, condition) — pick N so the per-sentence LLM
  entropy is stable; pilot a few sentences first.

## Layout

```
study/
  README.md              # this plan
  config.py              # models, conditions, sampling N, codebook + scheme params
  data/
    human/               # codes.log, codesNZ.log, master-codersGB.txt, master-codersNZ.txt
    sentences.csv        # 179 quasi-sentence texts + gold, aligned (from handbook §5)
    codebook.csv         # 56-category frame + 7-domain map (from handbook §7)
  src/
    extract_sentences.py # parse handbook §5 -> sentences.csv; assert match to gold vectors
    human_profile.py     # Step 1: per-sentence entropy, per-category κ, human confusion
    run_llms.py          # Step 2: collect LLM code distributions over the 179
    alignment.py         # Step 3: error~entropy, disagreement~disagreement, ceiling scoring
  reports/               # human profile, alignment results, summary.md
```

## Immediate next step

Two things that need no API and unblock everything:
1. `extract_sentences.py` — pull the 179 quasi-sentences from the handbook §5 text, pair
   each to its gold code, and **assert** the resulting gold vector equals the master files
   (length 107 / 72, exact order). This makes the text→gold→human alignment a checked
   invariant rather than a trust.
2. `human_profile.py` — Step 1 in full. It is an evening on data already on disk and tells
   us the shape of human ambiguity (and the DR5–7 dumping-ground prediction) *before* any
   compute is spent on LLM runs.