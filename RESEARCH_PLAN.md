# When models disagree, who is right? Expert disagreement as a referee for LLM (dis)agreement in ambiguous text coding

**A matched, item-level study on CMP/Manifesto coding.**

_Single canonical plan. Supersedes and consolidates the former `RESEARCH_PLAN.md`,
`RESEARCH_PLAN_branch_human_distribution.md`, `PILOT_PLAN.md`, and
`literature_review_and_revised_plan.md`. Human side computed and validated (Step 0
done). Pilot 1 run and analyzed (8 model IDs, 14 configs, 30 sentences, 10 runs). Full
collection not yet run._

> **Reframe note (2026-06).** An earlier version of this plan headlined **"manufactured
> consensus"** — humans split, models all agree on the wrong answer (the 2×2 "danger
> cell"). The pilot data contradict that headline: on hard items models do **not** agree
> with each other (between-model spread > within-model spread), and the pooled "consensus"
> is an artifact of whichever model pinned hardest. The honest, better-supported, and
> less-occupied headline is the opposite — **individually confident, collectively
> incoherent** — and it is worse news for the practitioner. The 2×2 is retained as a
> _populated result_, not a thesis. See §1 and §4.

---

## 0. What this paper is, in plain terms

People are starting to use AI models to do a job humans used to do by hand: read political
text one sentence at a time and tag each sentence with a category from a fixed scheme. The
implicit safety check most people reach for is **agreement** — if a model is consistent
across re-runs, or several models independently return the same code, the coding "must" be
right, the way we trust a measurement two instruments agree on.

This paper shows that check is unsafe on a task that is _genuinely ambiguous_, because on
such a task even trained human experts disagree constantly. We have a rare dataset where
the **same** sentences were each coded by 23–32 trained expert coders, so for every
sentence we know the full **distribution** of expert codes — not just a gold label. That
lets us put three disagreement profiles side by side, sentence by sentence:

- **the experts** — how a room of trained coders splits;
- **a single model across re-runs** — does it waver, or pin one answer?
- **the models against each other** — do they converge, and on what?

The one finding to walk away with: **on genuinely ambiguous coding, inter-model
(dis)agreement is decoupled from expert disagreement.** Each model is over-confident on
its own (it pins where experts split); the models are confidently incoherent with one
another (they pin on _different_ codes, sometimes codes no expert chose); and where model
disagreement is widest it does **not** track where the task is actually hard for humans. So
neither single-model confidence nor multi-model agreement recovers validity here — and the
multi-model case is _worse_ than the naïve fear, because there is often no majority to
trust, just a pile of confident, mutually contradictory answers.

This is a **methods paper** for the researcher _deciding whether to use LLMs as coders_ —
not the political scientist who cares about manifesto substance. That framing decides what
is in and what is out.

---

## 1. The claim, stated plainly

Two facts collide.

1. **The human ceiling is low and known.** On the Manifesto scheme, trained expert coders
   disagree constantly: category-level Fleiss's κ in the low 0.3s, median coder-vs-gold
   Cohen's κ ≈ 0.43–0.54 (Mikhaylov, Laver & Benoit 2012; reproduced in Step 0). The "gold
   standard" is itself one draw from a distribution of expert opinion, not ground truth. A
   large share of what any accuracy metric scores as model _error_ is irreducible _task_
   ambiguity — boundaries expert humans themselves cross.

2. **Models' (dis)agreement is not a window onto truth.** A model can be perfectly
   self-consistent and consistently wrong. Models from overlapping training corpora and
   shared lineages can correlate their _errors_ (Kim et al. 2025; Goel et al. 2025). And
   when many models disagree, the disagreement need not track real difficulty — it can be
   per-model idiosyncrasy.

Put together, the pilot points at a specific, measurable failure with three legs (all
gold-free — they compare two distributions on the same items, no "correct" answer needed):

- **Leg 1 — under-dispersion.** Each model's spread over re-runs is far narrower than the
  expert spread, and the compression is _worst on the hardest items_. The model pins where
  experts waver. (Pilot §1a: model/human spread ratio 0.26–0.50, worst on high-split.)
- **Leg 2 — incoherence between models.** On hard items, between-model spread exceeds
  within-model spread: each model pins confidently, but on _different_ codes — frequently
  codes outside the human support set ("alien"). Pooling models manufactures an apparent
  "consensus" that is really one model's pin. (Pilot §1c; exemplars GB-033, GB-016.)
- **Leg 3 — no recovery of difficulty.** Per-sentence model entropy barely tracks
  per-sentence human entropy once the easy anchor is removed (pooled r 0.46 → 0.19 on
  hard+mid). Model disagreement is uninformative about human disagreement exactly where it
  would be useful. (Pilot §1b.)

> **The 2×2 is a result, not a thesis.** We still cross human (dis)agreement × model
> (dis)agreement and report all four cell counts. But which cells fill is an _empirical
> finding_, not a pre-committed claim. The pilot suggests the "models agree where humans
> split" cell (the old headline "false consensus") is **sparse**, and that the populated
> cells are "models split — incoherently or alien" — itself the result. We do not need any
> particular cell to be full.

|                  | Humans agree      | Humans split                          |
| ---------------- | ----------------- | ------------------------------------- |
| **Models agree** | construct is real | false consensus _(pilot: likely rare)_|
| **Models split** | models add noise  | honest difficulty **or** alien scatter|

The landing: _agreement among models is not validity, and disagreement among models is not
a clean difficulty signal, on genuinely ambiguous coding tasks. We can show the decoupling
sentence by sentence against a real expert distribution._

---

## 2. Why this data, and why it is the only data that works

A _matched, paired_ design: the same sentences, coded by many humans and by many models,
compared item by item. The matching is the teeth — every claim is about the _same
sentence_ on both sides.

The human side is the rare asset. In the MLB reliability experiment, ~32 GB and ~23 NZ
coders coded the **same** quasi-sentences, so every sentence carries a full **distribution**
of expert codes — a per-sentence ambiguity score (entropy / modal share), not an aggregate
reliability number. This per-item human-disagreement signal is **not reproducible from any
other CMP data** and is precisely the referee the central question needs.

**Verified on disk (in hand):**

| document                      | sentences | human coders (raw) | aligned to gold |
| ----------------------------- | --------: | -----------------: | --------------- |
| GB: Liberal/SDP Alliance 1983 |       107 |                 32 | yes             |
| NZ: National Party 1972       |        72 |                 23 | yes             |

- **Coding scheme — period-correct by construction.** Coders worked under the **3rd fully
  revised edition** of the Manifesto Coding Instructions (Werner & Volkens 2010, MARPOR/WZB),
  the CMP 56-category + uncoded scheme. We use _that_ edition because it is the instrument
  the humans actually used.
- **Coverage is a boundary condition, not a caveat.** The two texts exercise ~21 of the
  scheme's categories in the gold coding (RILE split 50 left / 59 right / 70 none across
  179 units). Coders and models choose from the _full_ 56 + uncoded; ~21 is gold coverage,
  not the option space. Per-category claims live or die on those ~21 — stated up front.
- **These are the manual's teaching texts.** Both documents are the coding manual's own
  instructional examples, hand-picked for clarity. That they _still_ produced Fleiss's
  κ ≈ 0.35 and median coder-vs-gold Cohen's κ ≈ 0.46 is a floor-raising fact: if the
  pedagogical best case is this noisy, production manifestos are noisier. **Magnitudes are
  therefore a boundary condition — the _phenomenon_ and the _method_ generalize, the
  numbers do not.** Said up front, not buried.

---

# Part I — Literature review

The study sits at the intersection of four conversations: (1) the human ceiling on complex
coding; (2) LLMs as coders and how they are validated; (3) inter-model (dis)agreement and
correlated error; and (4) human label variation and calibration to a human _distribution_.
The contribution lands at the seam of (3) and (4): we are the boundary condition that
breaks "disagreement-as-usable-signal," demonstrated on the first _expert_ per-item
distribution for a real codebook task.

> **Citation hygiene.** Every entry below was checked against arXiv / ACL Anthology /
> publisher pages on 2026-06-19. Verification status is tagged per entry and summarized in
> the appendix. The prior draft of this review carried several LLM-garbled author strings
> and one fabricated paper ("12 Angry LLMs … Divergence from Deliberation as Signal");
> those are corrected or removed here. **Re-pull every string before submission.**

## L1. The human ceiling: CMP coder reliability

**Mikhaylov, Laver & Benoit (2012).** "Coder Reliability and Misclassification in the Human
Coding of Party Manifestos." _Political Analysis_ 20(1), 78–91. _[VERIFIED]_
The foundational reference for task and data. Multi-coder reliability experiment whose
replication materials supply our 179 sentences. Category-level Fleiss's κ ≈ 0.35; median
coder-vs-gold Cohen's κ ≈ 0.43 (GB)/0.54 (NZ) for retained coders; misclassification is
_systematic_ — concentrated in cross-domain confusions (e.g. 408 vs 410) and catch-alls
(000, 303, 305, 408); it propagates into RILE as centrist attenuation.
**Use:** establishes the low, known human ceiling; supplies the per-item expert
distribution that is our referee. We reproduce their κ as a validation check (Step 0 done).

**Benoit, Laver & Mikhaylov (2009).** "Treating Words as Data with Error: Uncertainty in
Text Statements of Policy Positions." _AJPS_ 53(2), 495–513. _[VERIFIED]_
Introduced the measurement-error framework for CMP data: text-as-data methods must model
coding uncertainty.
**Use:** conceptual license for treating the human _distribution_, not the gold label, as
the reference for what a sentence "means" under the scheme — extended here to the LLM case.

## L2. LLMs as coders: accuracy and validation

**Manifesto Project — manifestoberta.** Fine-tuned XLM-RoBERTa (context model, 56 topics),
trained on >1.7M annotated statements; ~64% top-1 / ~88% top-3 on held-out data.
_[VERIFIED — perf report in `refs/literature/`]_
**Use:** even with massive supervised training on this exact scheme, accuracy plateaus near
64% — a ceiling set partly by irreducible ambiguity. Our zero-shot models score lower; that
is beside the point, since our interest is agreement _structure_, not beating a baseline.

**Atreja, Ashkinaze, Li, Mendelsohn & Hemphill (2025).** "Codebook-LLMs: Evaluating LLMs as
Measurement Tools for Political Science Concepts." _Political Analysis_ (PDF in
`refs/literature/`). _[VERIFIED — in refs]_
Five-stage framework for codebook-LLM measurement; on a Manifesto split, zero-shot weighted
F1 with 7–12B open-weight models ≈ 0.21; structured codebook format helps modestly.
**Use:** confirms CMP coding is genuinely hard for zero-shot LLMs; their error-analysis
stage motivates our qualitative close-reads. We add the _multi-model, human-referenced_
dimension they lack.

**Bavaresco, Bernardi, Bertolazzi, Elliott, Fernández, … Plank, Schlangen, et al. (2024).**
"LLMs instead of Human Judges? A Large-Scale Empirical Study across 20 NLP Evaluation
Tasks" (JUDGE-BENCH). arXiv:2406.18403. _[VERIFIED — 20 authors]_
11 LLMs across 20 human-annotated datasets; reliability varies sharply by property, judge
expertise, and human-vs-model language; "not yet ready to systematically replace human
judges."
**Use:** validation must be per-task, per-scheme — aggregate "LLMs-as-annotators" claims
mislead. Our study is exactly that validation for one hard scheme.

**Gilardi, Alizadeh & Kubli (2023).** "ChatGPT Outperforms Crowd Workers for Text-Annotation
Tasks." _PNAS_ 120(30). _[VERIFIED]_
The optimistic pole: ChatGPT beat MTurk crowdworkers on stance/topic tasks with _few_
categories and _high_ human agreement.
**Use:** our task is the opposite regime (57 categories, low human agreement). We are a
boundary condition on Gilardi optimism — specifying _when_ it holds, not contradicting it.

**Comparing LLMs and human annotators in latent content analysis (2025).** _Scientific
Reports_ 15, art. 96508 (DOI 10.1038/s41598-025-96508-3; arXiv:2501.02532). _[VERIFIED]_
On _latent_ constructs (sentiment, political leaning, emotional intensity, sarcasm) LLMs
matched or exceeded human reliability (Krippendorff's α 0.75–0.85), but struggled with
sarcasm.
**Use:** sharpens the latent-vs-manifest boundary — LLMs do well on latent constructs and
poorly on manifest codebook constructs like CMP categories.

## L3. Inter-model (dis)agreement and correlated error

**Yang & Wang (2026).** "Benchmark Illusion: Disagreement among LLMs and Its Scientific
Consequences." arXiv:2602.11898. _[VERIFIED — authors Eddie Yang & Dashun Wang; prior draft's
"Yang, Ding, Chou" was wrong]_
Equal-accuracy LLMs disagree on 16–66% of items (16–38% among frontier models); used for
annotation, switching the model can change estimated treatment effects >80% and sometimes
flip sign.
**Use:** establishes the _existence_ and downstream _consequence_ of inter-model
disagreement. We add the per-item _human_ baseline (distinguish "hard task" from "different
blind spots") and the disagreement _geometry_ (where the mass lands).

**Kim, Garg, Peng & Garg (2025).** "Correlated Errors in Large Language Models." ICML 2025;
arXiv:2506.07962. _[VERIFIED — Elliot Kim, Avi Garg, Kenny Peng, Nikhil Garg; prior draft's
"Kim, Auzina" was a cross-contamination from the paper below]_
350+ LLMs; substantial error correlation (on one leaderboard, models agree 60% of the time
when both err); larger/more-accurate models have _more_ correlated errors even across
providers; links to algorithmic-monoculture theory and downstream hiring effects.
**Use:** the mechanism behind any lineage structure we observe — and the reason we
**demote** our own lineage analysis (they did it at a scale we cannot beat; we report ours
descriptively, not as a beat).

**Goel, Struber, Auzina, Chandra, Kumaraguru, Kiela, Prabhu, Bethge & Geiping (2025).**
"Great Models Think Alike and This Undermines AI Oversight." arXiv:2502.04313. _[VERIFIED;
prior draft's "Auzina, Collins" was wrong — Auzina is a middle author, no "Collins"]_
Introduces CAPA (chance-adjusted probabilistic agreement); model mistakes grow _more_
similar with capability; LLM-as-judge favors similar models.
**Use:** high-capability agreement can reflect shared pretraining/RLHF, not convergent
validity — our human baseline is what separates the two.

## L4. Human label variation & calibration to a human distribution

_This is the thread the prior draft missed, and it is the closest conceptual home._

**Baan, Aziz, Plank & Fernández (2022).** "Stop Measuring Calibration When Humans Disagree."
EMNLP 2022; arXiv:2210.16133. _[VERIFIED — the key omission of the prior draft]_
Measuring calibration to the human _majority_ is theoretically wrong when humans inherently
disagree; derive instance-level measures against the full human judgement distribution
(class frequency, ranking, entropy), demonstrated on ChaosNLI.
**Use:** this is our method stated by someone else. We _operationalize Baan on the first
expert per-item distribution for a real 56-way codebook_ — they used crowd NLI (≤5 labels).
We stand on this paper, not beside it.

**Chen, Wang, Peng, Litschko & Plank (2024).** "'Seeing the Big through the Small': Can LLMs
Approximate Human Judgment Distributions on NLI from a Few Explanations?" Findings of EMNLP
2024; arXiv:2406.17600. _[VERIFIED]_
LLMs can approximate human judgment _distributions_ from a few expert labels+explanations.
**Use:** the optimistic counterpoint on _distributional_ alignment — but on NLI, with
crowd/expert HJDs of ≤5 labels. Our null (model entropy ≠ human entropy on hard items) is
the contrasting result on a hard, many-category, expert task.

**Foundational human-label-variation thread** _[⚠ confirm exact strings before citing]_:
Pavlick & Kwiatkowski (2019, TACL, "Inherent Disagreements in Human Textual Inferences");
Nie, Zhou & Bansal (2020, "What Can We Learn from Collective Human Opinions on NLI?"/
ChaosNLI); Plank (2022, EMNLP, "The 'Problem' of Human Label Variation"); Aroyo & Welty
(CrowdTruth). Also the reporting-practices angle: "Who Annotates in NLP? A Large-Scale
Assessment of Human Annotation Reporting 2018–2025" (arXiv:2606.02255). These motivate
"disagreement is signal, not noise"; verify each before inclusion.

## L5. Disagreement-as-signal (the space we must out-position)

**Najera, Moon, Srinivasan & Veeraraghavan (2026).** "When Models Disagree: Rethinking LLM
Evaluation for Public Comment Analysis." arXiv:2605.29025. _[VERIFIED — lead author Najera;
prior draft's "Veeraraghavan, Chen" had wrong lead and a fabricated co-author]_
**The closest methodological kin.** Interpretive Audit Pipeline treats multi-model
disagreement as diagnostic of interpretive complexity; on 1,260 USDA public comments
**"inter-model thematic divergence exceeds within-model prompt variation"** (our §1c
between>within) and "accuracy against a small validated set cannot detect when different
models produce materially different categorizations."
**Use / threat:** they already publish our between>within finding and treat disagreement as
a _usable_ signal. We out-position by (a) a per-item _expert distribution_ (not a small
validated set), (b) a _closed_ 56-way scheme (precise geometry), and (c) showing the signal
**breaks** — model disagreement does _not_ recover human difficulty on the hardest items.

**Zhao et al. (2025).** "Automated Quality Assessment for LLM-Based Complex Qualitative
Coding: A Confidence-Diversity Framework." arXiv:2508.20462 (companion: arXiv:2508.02029).
_[PARTIAL — paper/findings verified; author list not confirmed, tag "et al."]_
Inter-model normalized Shannon entropy as a quality signal; external entropy negatively
associated with accuracy (r −0.18 to −0.27); self-confidence tracks inter-model agreement
(r=0.82 in the companion); explicitly notes LLM _overconfidence_.
**Use / threat:** operationalizes inter-model entropy as a _usable_ quality oracle. We are
the stress test where the oracle fails: at κ≈0.35 human agreement, model entropy stops
tracking accuracy/human difficulty.

**Liu et al. (2026).** "What Is Actually Being Annotated? Inter-Prompt Reliability as a
Measurement Problem in LLM-Based Social-Science Labeling." arXiv:2604.16413. _[VERIFIED —
lead author Jingyuan Liu]_
Inter-Prompt Reliability (IPR): output stability across paraphrased prompts; substantial
stochastic variation on interpretive tasks.
**Use:** supports keeping prompt wording _fixed_ (we vary only context), so prompt
variation never confounds model variation.

_(Removed: "12 Angry LLMs — Divergence from Deliberation as Signal for Complex Stance
Detection." No such paper. The real "12 Angry AI Agents," arXiv:2605.01986, is about
jury-deliberation dynamics and is tangential.)_

## L6. The gap this study fills

| What the literature establishes | What is still open — and this study provides |
|---|---|
| LLMs disagree even at equal accuracy; errors correlate by lineage (Yang & Wang; Kim et al.; Goel et al.) | Whether, on a hard task, that disagreement **recovers expert difficulty** — and we find it does **not** (Leg 3) |
| Inter-model disagreement is a _usable_ diagnostic / quality signal (Najera et al.; Zhao et al.) | The **boundary condition where the signal breaks** — genuinely expert-ambiguous items, shown against a real expert distribution |
| Calibrate to the human _distribution_, not the majority (Baan et al.); LLMs can approximate HJDs on NLI (Chen et al.) | The same, operationalized on the **first expert per-item distribution for a real 56-way codebook** — and a negative result there |
| Humans disagree constantly on CMP coding (MLB 2012) | The **three-population geometry** (expert / within-model / between-model) put side by side, and _where the model mass lands_ relative to the human support set ("alien" vs human-shaped error) |

**The unique asset:** no other study has a per-item _expert_ disagreement distribution
(23–32 coders/item) for a complex real-world codebook. That distribution is the referee
that turns the 2×2 and the geometry comparison from concept into measurement.

---

# Part II — Research design

## 3. Research questions

Reframed around the pilot. RQ1 is the confirmatory headline; RQ2 is the mechanism/geometry
and the home of the qualitative work; the former lineage RQ is demoted to an exploratory
companion (RQ-A), explicitly because Kim et al. / Goel et al. own that question at scale.

- **RQ1 (headline). Does model (dis)agreement recover expert disagreement?** Per-sentence
  model entropy vs human entropy, decomposed by difficulty bucket (not pooled — the pooled
  r is an easy-anchor artifact). The three legs of §1: under-dispersion (within-model),
  incoherence (between-model), and non-recovery of difficulty. _Key number: ρ(model H,
  human H) on hard+mid items._ The dependent construct is the **structure of
  (dis)agreement and its alignment with human disagreement**, never raw accuracy.

- **RQ2 (mechanism — geometry of divergence).** When models diverge from the human
  distribution, **where does the mass land?** Inside the human _semantic neighborhood_
  (human-shaped error — adjacent codes humans also confuse, e.g. 408↔410, 503↔504) or
  outside it ("alien" — codes no expert chose)? Compare the human confusion geometry to the
  per-model and pooled-model confusion geometry on the same items. This is where the
  qualitative close-reads are load-bearing (§7).
  - **Binding prerequisites** (else RQ2 is not reportable): (a) **raise the generation
    token budget for reasoning-on configs** — pilot configs with reasoning "on" showed
    10–34% off-scheme output (§8) because the 2048-token cap truncated them mid-reasoning
    before they emitted a code; reasoning models need a budget well above 2048; (b) define the
    **code neighborhood principled-ly** from `categories.json` (shared domain, RILE class,
    and definition adjacency), not "rare" — otherwise a reviewer reads 702-vs-408 as
    adjacent and the "alien" claim collapses.

- **RQ-A (exploratory companion — _not a beat_).** Does inter-model agreement cluster by
  recorded attributes (company/lineage, size tier; background: country, release/cutoff,
  architecture, open/closed weight)? Reported descriptively, framed as "consistent with /
  candidate for confirmation," with Kim et al./Goel et al. cited as the powered version.
  Guardrails (binding): report the whole attribute map including nulls; frame as "what to
  confirm at scale"; declare foreground (company, size) vs background in advance. If it does
  not separate at 15 models, that is a one-line null, not a failure.

## 4. Design grid

A marvel is _fully-crossed, not massive_. Every axis varied is one we can later hold fixed;
every call is attributable to a named cell.

| Axis | Levels | Notes |
|---|---|---|
| **Sentences** | 179 (GB 107 + NZ 72), fixed | same sentences coded by 32/23 humans; the 4 balanced-RILE coin-flips (NZ-022, GB-041, NZ-045, NZ-007) over-sampled |
| **Models** | ~15, OpenRouter | company × size grid + background attributes recorded per model; emphasis on open-weight (the at-scale-coding population), 1–2 frontier reference points |
| **Context** | in-document (human parity, **primary**) + sentence-only (degraded contrast) | manual requires reading the surrounding paragraph + section headings (Decision Rules 2, 11); in-context reproduces the human task |
| **Temperature** | 0 (agreement anchor) + 1 (disagreement) | RQ1's human-vs-model comparison runs on **temp 1**; temp 0 is the deflationary self-consistency control. _Temp 0 ≠ deterministic._ |
| **Reps/cell** | ~2 (temp 0), ~5 (temp 1) | coarse per model _by design_; pools to ~75 draws/sentence/context (15×5) vs 32/23 human coders. Precise single-model entropy is not needed in the main argument |

**Approximate volume (indicative):** ~10.7k calls @temp 0 + ~26.9k @temp 1 + a small
self-consistency sub-study ≈ **~45k calls**. Tractable, mostly cheap open-weight models.
**Recost after the pilot resolution check** (§8) before committing.

**The temperature-access confound (handle, don't note).** Some models on OpenRouter do not
honor `temperature`/`top_p`, and a provider may _accept_ a parameter a backend silently
ignores. (1) **Pre-flight audit** every roster model for whether temp/top_p are actually
respected; result in a methods table. (2) **Quarantine** temperature-locked models to
single-setting analyses only; they never enter a claim that _varies_ temperature.

**Human reference (Step 0 done, validated to MLB within rounding):**
retained subset 17 GB + 12 NZ (expert ceiling, **primary**); full pool 32 GB + 23 NZ (crowd
ceiling, robustness); Fleiss κ retained GB 0.349 / NZ 0.397; danger-cell count 72 sentences
where retained humans split (1−modal ≥ 0.50, category level); RILE-directional only 4
balanced (RILE distortion is **out** of the spine — discussion illustration only).

## 5. Analysis plan (paired, item-level, on the matched 179)

1. **Human ambiguity profile** — DONE (Step 0). Per-sentence entropy & 1−modal share over
   categories/domains/RILE; per-category Fleiss κ; coder→gold confusion. Computed twice
   (retained primary, full robustness) and both reported; `000` kept as a class (primary),
   with/without as robustness. Validation reproduces MLB.
2. **Model disagreement profile** — same entropy machinery on pooled model distributions
   (temp 1), per context, **per config** (never pooled across reasoning modes).
3. **RQ1 — recovery of difficulty.** Spearman ρ(model H, human H), reported **by bucket**
   (the headline is hard+mid, not pooled); the under-dispersion ratio per bucket; the
   within- vs between-model decomposition. The 2×2 cell counts as a _populated result_.
4. **RQ2 — geometry.** Human vs model confusion structure on shared items; classify
   divergences as human-shaped (in-neighborhood) vs alien (out-of-support), after the §3
   parsing clean-up and neighborhood definition. Per-category model accuracy reported
   against the _human agreement rate_, never 100%.
5. **RQ-A — attribute map (exploratory).** Pairwise model-agreement matrix; clustering;
   attribute mapping with nulls shown. Descriptive only.
6. **Downstream-consequence illustration (discussion only).** GB-067 as a worked
   _model-vs-codebook_ RILE sign-flip (model applying the 2010 codebook strictly could pick
   201 where humans/gold landed on 701) — illustration of stakes, **not** a prevalence
   estimate, and explicitly _not_ a member of the human danger cell.

## 6. The coding instrument (instruction-parity)

Build the model prompt to match what MLB coders received, so any human–model gap is about
coding, not a different instrument. Commitments: (a) full **56 categories + `000`** with
2010-handbook definitions and decision rules DR6–DR11 (policy goal beats means; specific
position beats 303/305/408; group politics yields to specifics except 703; code the
manifest statement; one and only one code) — never the reduced ~21 gold subset; (b)
quasi-sentences pre-unitised (given), model never unitises; (c) `000` a live option; (d)
the manual's worked answer key excluded. The one parity we cannot grant — and state as a
limitation — is _training_ (humans had CMP training + a Berlin supervisor; the model has the
handbook in context only). The asymmetry favours the human, which only sharpens a finding
that models pin where trained humans split. Artifacts: `data/categories.json`,
`src/prompts/coding_instrument.md` (sentence-only and in-context share it, differing only in
the context block).

## 7. Qualitative component (load-bearing, for RQ2)

Every claim is ultimately about individual sentences. The statistics prove the pattern
holds across 179; the close-reads prove it is real and make the reader care — and our
exemplars come with receipts (we don't _assert_ a sentence is hard, we _show_ 32 experts
argued about it).

**Selection.** Purposive, from the populated cells (not only the old "false consensus"
cell): coin-flips where a model pins; cases where models scatter incoherently; alien-code
cases (after parsing clean-up). Span domains, split _types_ (wide vs bimodal vs weak
plurality), and model patterns. Include ≥2 of the 4 balanced-RILE sentences.

**Per-sentence frame.** (1) What the humans see — the distribution, top 2–3 codes, what
licenses each reading. (2) What the models do — converge or scatter? on a human code or an
alien one? (3) Interpretive-move code — literal-vs-tonal, domain confusion, valence flip,
specificity error, codebook-literalism. (4) Why this _looks_ easy to a model.

**Pilot exemplars already demonstrate it (`reports/pilot/exemplars.md`):**
- **NZ-006** ("restoring NZ's shattered economy") — humans split 408/404/305; models
  near-unanimous on 408. _Specificity error / under-dispersion._
- **GB-033** ("civil war in British industry…") — humans split across ~15 codes (max 5/32);
  models scatter to 702/408/410/703 across families, pooled modal **702 = a code 1/32
  humans chose**. _Incoherence + alien; the textbook Leg-2 case._
- **GB-016** ("rundown cities… warped priorities") — humans 606/305/504; models converge on
  303 (and several emit off-scheme). _Literal-vs-tonal — but note the off-scheme rate; clean
  before quantifying._

These show ≥3 distinct failure modes already; at full scale the typology becomes a
quantifiable taxonomy. **Decision still open:** interleaved (each claim followed by its
sentence) vs gathered (one close-reading section) — leaning interleaved; decide on how rich
the full-scale reads are.

## 8. What the pilot established (Pilot 1) — and infrastructure to reuse

**Run:** 8 model IDs, reasoning probed → 14 configs, 30 purposive sentences (10 high-split
incl. the 4 balanced, 10 mid, 10 high-agreement), 10 runs each, temp 1, in-context.
Artifacts in `reports/pilot/`.

**Reads (mapped to the pre-committed decisions):**
- **Leg 1/2/3 confirmed** — under-dispersion (ratio 0.26–0.50, worst on hard), between >
  within on hard items, correlation trap (pooled r 0.46 → 0.19 hard+mid). → _merge; RQ1
  headline; scale up_ — but with the reframed headline, not "models track difficulty."
- **Resolution** — spread estimates move modestly 10→5 runs (abs-Δ 1-modal ~0.02–0.09) but
  meaningfully 10→3. → full study can likely hold ~5–10 temp-1 reps/model; **recost** before
  committing; don't drop below ~5.
- **Q2 cells** — model-only confusion pairs (candidate alien) = 53, overlap with human = 84.
  Enough to attempt RQ2 as a headline-supporting result, **but redefine confusion vs the
  human distribution (not master_code) and clean off-scheme first.**
- **Off-scheme contamination (action item):** reasoning-"on" configs for
  gemma-4-26b (33.8%), qwen3.6-35b (15.3%), gemma-4-31b (10.9%) — these calls hit the
  2048-token cap mid-reasoning and never emitted a code, so their Q1/Q2 numbers are thinned
  by truncated nulls. **Raise the generation token budget above 2048 for reasoning-on
  configs (ideally an explicit reasoning-token budget) and re-run them before the full
  run.**

**Infrastructure to port from `archive/early-experiment/pilot-2/src/` and `src/pilot/`**
(reuse mechanics, not the old design): OpenRouter client + `.env` loader; resumable
per-config JSONL cache; threaded worker pool with retry/backoff; `<think>`-strip + 3-digit
regex parser (raise the generation token budget above 2048 for reasoning-on configs per
above so they don't cap out mid-reasoning); codebook renderer. **Fail loud** on any
unreachable model ID. Run independence at temp 1 with **no fixed seed**.

## 9. Narrative arc

- **Setup (deflationary):** "Models are individually consistent — so what?" One figure:
  temp-0 re-runs agree near-ceiling. Self-consistency is uninformative about validity.
- **Beat 1:** The task is stochastic even for experts — the per-sentence human distribution;
  72 split sentences; κ≈0.35; "the right code" is a distribution, gold is one draw.
- **Beat 2 (RQ1, headline):** Model (dis)agreement does not recover expert disagreement —
  the three legs; the 2×2 populated; the hard-only ρ. Individually confident, collectively
  incoherent.
- **Beat 3 (RQ2, mechanism):** The geometry of divergence — human-shaped vs alien error;
  the close-reads.
- **(Companion, RQ-A):** attribute map, descriptive, nulls shown.
- **Discussion:** for the researcher choosing to use LLMs as coders — neither single-model
  confidence nor multi-model voting is a safe check here; the 2×2 is a diagnostic template
  for anyone with even a small human distribution; the GB-067 downstream illustration.

## 10. Threats, caveats, open decisions

**Binding before the full run / before claims:**
- Raise the generation token budget above 2048 for reasoning-on configs (else they cap out
  mid-reasoning and never emit a code, thinning the off-scheme bucket).
- Define the code neighborhood from `categories.json` before any human-shaped-vs-alien
  claim.
- Pre-flight temperature-access audit; quarantine locked models.
- Recost reps/model from the resolution check.

**Acknowledged limitations (stated, not studied):**
- **Boundary condition:** two teaching texts, ~21 gold categories — _magnitudes do not
  generalize; the phenomenon and the method do._
- **Training-data contamination:** these texts + gold codes are published, so they may sit
  in pretraining. Standard threat-to-validity note (mitigant: the manual's PDF interleaves
  margin codes and prose, so verbatim recall of the unit→code key is unlikely). Not a
  research thread.
- **RILE distortion:** retired from the spine (only 4 balanced sentences); discussion
  illustration only.

**Open decisions (settle on data, not vibes):**
- Center of gravity RQ1 vs RQ2 — RQ1 is bedrock; RQ2's status depends on whether the
  geometry separates after clean-up.
- Interleaved vs gathered exemplars.
- Stance toward "LLMs can replace coders" (warning vs even-handed map vs recipe) —
  post-analysis.
- Gold's status — report both gold-relative (comparable to literature) and gold-free
  (the honest headline).

## 11. Immediate next steps

1. **Raise the generation token budget** above 2048 for reasoning-on configs (ideally an
   explicit reasoning-token budget) so they don't cap out mid-reasoning — unblocks RQ2.
2. **Model roster as an explicit attribute grid** — ~15 real models to company × size +
   background attributes + temperature-access column; verify cells fill _before_ committing.
3. **Finalize the parity instrument** (`coding_instrument.md` + `categories.json`); render
   and eyeball one in-context and one sentence-only prompt.
4. **Define the code-neighborhood** adjacency from `categories.json` (domain/RILE/definition)
   for the RQ2 geometry.
5. **Recost** from the resolution check; pre-flight temperature audit.
6. **Full collection** (~45k calls), then replicate the three legs at full scale, populate
   the 2×2, run the geometry analysis, and select close-reads.

## 12. Implementation & provenance notes

**Primary source & the MARPOR v5 warning.** Source the pedagogical texts and scheme from
**Werner & Volkens 2010 (3rd revised edition)** only. Do **not** source codes from the
current MARPOR corpus: v5 split several categories (202→202/202_2, 605→605/605_2,
703→703/703_2) and modern releases recombine them, which would not line up with the
2008-era gold. Use the strict 56-category (v1–v4) frame.

**Data verification vectors (unit tests).** Alignment text→gold→human must be mechanical:
- GB (107): leading `0 0 0 305 305 606 305 410 408 …` (matches `master-codersGB.txt`)
- NZ (72): leading `414 414 414 414 414 408 408 402 …` (matches `master-codersNZ.txt`)
Step 0 confirms both pass.

**Repository layout.** Five buckets so each kind of thing has one home and the LLM
collection (the part that grows) is isolated:

```text
manifesto-project-study/
  RESEARCH_PLAN.md          # THIS FILE — single canonical plan + lit review
  README.md                 # orientation + how to run

  data/                     # INPUTS (canonical, read-mostly)
    human/                  #   raw MLB data: codes.log, codesNZ.log, masters, .dta, R repl
    categories.json         #   56-cat + uncoded scheme: 7-domain + RILE map (2010 handbook)
    cmp_coding_sample.json  #   179 quasi-sentence unit records: text, gold, label, section, RILE

  src/                      # CODE
    human_profile.py        #   Step 0: per-sentence entropy, per-category κ, confusion (DONE)
    pilot/                  #   Pilot 1: select_sentences, prompt, probe_models, run, analyze
    run_llms.py             #   full-scale collection (to build/scale from pilot)
    alignment.py            #   RQ1/RQ2: recovery, geometry, GB-067 illustration (to build)
    prompts/coding_instrument.md   #   instruction-parity model prompt

  runs/                     # LLM COLLECTION OUTPUT — scales with collection
    raw/                    #   gitignored: one cached file per API call (regenerable)
    pilot/                  #   pilot manifest + predictions
    predictions.csv         #   tidy long; same schema as reports/human/human_codings.csv

  reports/                  # ANALYSIS OUTPUT
    human/                  #   Step 0 profile (DONE)
    pilot/                  #   Pilot 1 results (DONE)
    llm/                    #   full-study results (to come)

  refs/                     # READING — handbook/, mlb/, literature/
  archive/                  # prior pilots and superseded plans
```

The shared long schema (`coder_id, manifesto, unit_id, sequence, code`) is deliberate:
`runs/predictions.csv` appends model rows in the same shape as
`reports/human/human_codings.csv`, so one entropy routine serves humans and models alike.

---

## Appendix — citation verification log (checked 2026-06-19)

| Citation | arXiv / DOI | Status |
|---|---|---|
| MLB 2012, _Political Analysis_ 20(1) | — | VERIFIED (well-established; in `refs/mlb/`) |
| Benoit, Laver & Mikhaylov 2009, _AJPS_ 53(2) | — | VERIFIED |
| manifestoberta | — | VERIFIED (perf report in refs) |
| Atreja et al. 2025, Codebook-LLMs | _Political Analysis_ | VERIFIED (PDF in refs) |
| Bavaresco et al. 2024, JUDGE-BENCH | 2406.18403 | VERIFIED (20 authors) |
| Gilardi, Alizadeh & Kubli 2023 | _PNAS_ 120(30) | VERIFIED |
| Latent content analysis 2025 | 10.1038/s41598-025-96508-3 / 2501.02532 | VERIFIED |
| Yang & Wang 2026, Benchmark Illusion | 2602.11898 | VERIFIED — authors corrected |
| Kim, Garg, Peng & Garg 2025, Correlated Errors | 2506.07962 (ICML'25) | VERIFIED — authors corrected |
| Goel et al. 2025, Great Models Think Alike | 2502.04313 | VERIFIED — authors corrected |
| Baan, Aziz, Plank & Fernández 2022 | 2210.16133 (EMNLP) | VERIFIED — **added** |
| Chen, Wang, Peng, Litschko & Plank 2024 | 2406.17600 (EMNLP Findings) | VERIFIED — added |
| Najera, Moon, Srinivasan & Veeraraghavan 2026 | 2605.29025 | VERIFIED — authors corrected |
| Zhao et al. 2025, Confidence-Diversity | 2508.20462 (+2508.02029) | PARTIAL — authors unconfirmed |
| Liu et al. 2026, IPR | 2604.16413 | VERIFIED |
| "12 Angry LLMs … Divergence from Deliberation" | — | **REMOVED — fabricated** (real 2605.01986 is unrelated) |
| Pavlick & Kwiatkowski 2019; Nie et al. 2020; Plank 2022; Aroyo & Welty; "Who Annotates" 2606.02255 | various | ⚠ confirm exact strings before citing |
