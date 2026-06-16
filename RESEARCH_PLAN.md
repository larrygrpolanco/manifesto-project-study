# When models agree, who is right? Inter-model consensus and human disagreement in ambiguous text coding

**A matched, item-level study on CMP/Manifesto coding.**

_Working research plan — design phase. Human side computed and validated (Step 0 complete); no LLM runs yet. A small LLM pilot is the next action. Read the Open Decisions at the end before collection begins; the two blocking ones that shaped the human data are now resolved with numbers attached._

---

## 0. What this paper is, in plain terms

People are starting to use AI models to do a job humans used to do by hand: read political texts one sentence at a time and tag each sentence with a category from a fixed scheme. When several models tag a sentence the same way, it is tempting to trust that — agreement feels like correctness, the way we trust a measurement two instruments agree on. This paper shows that trust is misplaced on a task that is _genuinely ambiguous_, because on such a task even trained human experts disagree constantly. When models all agree on a sentence that humans split on, the agreement is not evidence the models are right — it can be the models sharing a blind spot. We have a rare dataset where the same sentences were coded by many humans, so we can put human disagreement and model disagreement side by side, sentence by sentence, and catch consensus that is _manufactured_ rather than valid.

The one sentence to walk away with: **inter-model agreement is not a safe validity signal on ambiguous coding tasks — and on the one dataset where human disagreement is known per sentence, we can show exactly where the agreement check fails.**

This is a **methods paper**. The intended home is the methods/applied-linguistics methodology space (e.g. _Research Methods in Applied Linguistics_), with higher-impact venues attempted first. The audience is the researcher _deciding whether to use LLMs as coders_ — not the political scientist who cares about manifesto substance. That framing decides what is in and what is out (see §3 note on scope).

---

## 1. The problem, stated plainly

Researchers are beginning to use large language models as coders — including in medicine, to read and abstract data from unstructured clinical notes, and across other fields [literature to cite]: hand a model a coding scheme and a corpus, get back categorized text at a scale no human team could match. The appeal is obvious and the practice is spreading faster than its validation. The implicit safety check most people reach for is **agreement** — if several models independently return the same code, the coding "must" be right, the same way we trust a measurement two instruments agree on.

This plan is built around the observation that **the agreement check is not safe on tasks that are genuinely ambiguous**, and that political-text coding is exactly such a task. Two facts collide:

1. **The human ceiling is low and known.** On the Manifesto coding scheme, trained expert coders disagree constantly. Mikhaylov, Laver & Benoit (MLB) report category-level Fleiss's κ in the low 0.3s and median coder-vs-gold Cohen's κ around 0.43–0.54. The "gold standard" is itself one draw from a distribution of expert opinion, not ground truth. A large share of what any accuracy metric scores as model _error_ may be irreducible _task_ ambiguity — boundaries that expert humans themselves cross. _[To develop in the lit review: is a low human ceiling really the norm across coding tasks, or is this scheme unusually noisy? A reportable angle is the field's poor inter-coder-agreement practices — under-reporting of reliability, reliance on association (correlation) rather than agreement (κ), single-coder production data.]_

2. **Models can agree with each other for reasons that have nothing to do with being right.** Models drawn from overlapping training corpora and shared post-training lineages (distillation may contribute — _to check and cite_) can correlate their _outputs_ — and their _errors_ — without independently perceiving anything in the text. When that happens, inter-model agreement is not evidence of a real construct; it is shared structure wearing the costume of consensus. When LLMs are used downstream to abstract variables or identify constructs, this can compound into systematic bias.

Put those together and a specific danger appears, one that does not require us to decide in advance whether LLMs are "good" or "bad" at the task:

> **When models agree confidently on a sentence that humans split on, the consensus is manufactured.** A researcher trusting model agreement would record that sentence as settled, when in truth it is one of the contested cases — and would do so _systematically_, in whatever direction the models happen to lean.

The contribution of this study is to make that danger **measurable**, using the one body of data in the CMP world where it can be measured cleanly: the same sentences carrying a full distribution of expert human codes _and_ codeable by many models, compared item by item.

---

## 2. Why this data, and why it is the only data that works

This is a _matched, paired_ design: the same sentences, coded by many humans and by many models, compared item by item. The matching is what gives the study its teeth — every claim is about the _same sentence_ on both sides, so "where humans disagree" and "where models disagree" are directly comparable rather than rhymed across unrelated corpora.

The human side is the rare asset. In the MLB reliability experiment, ~32 GB coders and ~23 NZ coders coded the **same** quasi-sentences. That means every sentence carries a full **distribution** of human codes — a per-sentence ambiguity score (entropy / modal share), not merely an aggregate reliability number. This per-item human disagreement signal is **not reproducible from any other CMP data** and is precisely the referee the central question needs.

**Verified on disk (already in hand):**

| document                      | sentences | human coders (raw) | aligned to gold |
| ----------------------------- | --------: | -----------------: | --------------- |
| GB: Liberal/SDP Alliance 1983 |       107 |                 32 | yes             |
| NZ: National Party 1972       |        72 |                 23 | yes             |

The aligned unit records (`cmp_coding_sample.json`) carry, per quasi-sentence: text, master (gold) code, master label, and RILE position. The two logs (`codes.log`, `codesNZ.log`) carry every coder's full code vector, column-aligned to the 107/72 units and verified position-by-position against the master files. Coder identity is unique (email) in both files, so the per-coder layer needed for the coder-quality screen is intact.

**Coding scheme — period-correct by construction.** These human coders worked under the **3rd fully revised edition** of the Manifesto Coding Instructions (Werner & Volkens 2010, MARPOR/WZB), the CMP 56-category + uncoded scheme. We use _that_ edition because it is the instrument the humans actually used; sourcing categories or definitions from any other release would compare model output against a codebook the humans never saw. The JSON already documents three handbook-vs-master divergences for transparency; the unit records use the master coding throughout.

**Coverage is a boundary condition, not a caveat.** The two texts exercise ~21 of the scheme's categories (verified present in the gold coding), with a RILE split of 50 left / 59 right / 70 none across the 179 units. Per-category claims live or die on those ~21 categories — stated up front, not buried. (Coders and models choose from the _full_ 56 + uncoded scheme; the ~21 is gold coverage, not the option space.)

**These are the manual's teaching texts, not typical ones.** Both documents are the coding manual's own instructional examples (Werner & Volkens 2010, §5; Klingemann et al. 2006, Appendix II), hand-picked for clarity and codeability to teach the scheme. That they _still_ produced category-level Fleiss's κ ≈ 0.35 and median coder-vs-gold Cohen's κ ≈ 0.46 is a floor-raising fact: if the pedagogical best case is this noisy, production manifestos are noisier. Stated as a boundary on the human ceiling, not buried.

---

## 3. The narrative spine

The paper moves in three beats plus a deflationary setup move. Each beat is a question the data answers; the beats are ordered so each earns the next. Crucially, **none of the beats requires us to have pre-decided the paper's verdict** — the data picks the verdict.

**Setup move (formerly a standalone "reliability" question) — Models are individually consistent. So what?**
A brief, deliberately deflationary result, used to clear the ground before the real questions: within a single model, re-runs agree (especially at low temperature). The naïve reader takes this as "the task is solved." We show self-consistency is **uninformative about validity** — a model can be perfectly consistent and consistently wrong. This is one paragraph and one figure motivating the beats below; it is **not** a research question of its own.

**Beat 1 — The task is stochastic, even for experts.**
We open on our own item-level data: a per-sentence human disagreement profile (Step 0, already computed). This reframes the enterprise. On this task, "the right code" is often not a point but a distribution. _This is the ground the whole argument stands on, and the honest version of the field's discomfort: we routinely compare models to a human standard that is itself unstable._

**Beat 2 — Models agree with _each other_. Is that signal or shared structure? (→ RQ-A)**
The first novel measurement: cross-model disagreement per sentence — the machine analogue of inter-coder reliability — set beside the human cross-coder disagreement on the same sentences. Then the structure probe: **does inter-model agreement map onto recorded model attributes** (company/lineage, size/capability tier, and additional descriptors), or onto none of them (convergence on something real in the text)? This is run as **explicitly staged exploration**, not a confirmatory cluster claim — see §4 (RQ-A) for the anti-fishing guardrails.

**Beat 3 — The referee: does model disagreement track human disagreement? (→ RQ-B)**
The cleanest form of the central question, and the one that needs no privileged gold: correlate per-sentence model entropy with per-sentence human entropy. Then examine the **signed residual** — the sentences where the two diverge:

- Humans split, models agree → **manufactured consensus** (the danger zone).
- Humans agree, models split → models inject noise where the task is actually clear.
- Both agree / both split → the task's real easy and hard cases.

The 2×2 that organizes the finding:

|                  | Humans agree      | Humans split                     |
| ---------------- | ----------------- | -------------------------------- |
| **Models agree** | construct is real | **false consensus — the danger** |
| **Models split** | models add noise  | shared, honest difficulty        |

The landing: _agreement among models is not validity. On ambiguous coding tasks, treating it as validity imports model-specific structure into downstream measures — and we can show the import happening, sentence by sentence._

> **Scope note — what we deliberately do not claim (the RILE cut).** An earlier version carried a fifth beat: that systematic model lean on ambiguous sentences accumulates directionally into a shift in CMP's RILE left–right index. **Step 0 retired this as a headline.** Of the 179 units, only ~16 have no majority RILE class, and of those only **4** are genuinely balanced left-vs-right (NZ-022 5L/5R, GB-041 4L/5R, NZ-045 4L/4R, NZ-007 3L/3R); ~6 are weak two-sided leans, and ~6 are category-vs-uncoded splits that produce **centrist attenuation** — the symmetric flattening MLB already documented — not directional capture. With two documents and four directional sentences, there is no _rate_ to report. **RILE distortion is therefore out of the spine and out of the RQs.** It survives only as a discussion-section illustration of _why the methods point matters downstream_ — using GB-067, correctly relabeled: on GB-067 the retained humans are not split (11 left / 5 none / 1 right); the sign-flip there is **handbook-vs-gold**, i.e. a model applying the 2010 codebook strictly could pick 201 (Freedom/Human Rights, rile-right) where humans and gold landed on 701 (Labour Groups, rile-left). GB-067 is thus a _model-vs-human, codebook-literal_ divergence example, not a member of the human danger cell. Stated precisely so the paper never conflates the two mechanisms.

---

## 4. Research questions

Two research questions, both honestly staged, both computed from one shared collection. (A third, self-consistency/reliability, has been **demoted** to the deflationary setup move above — it is a control, not a question.) The center of gravity between RQ-A and RQ-B is **left unsettled for now** — leaning toward co-equal-but-both-honestly-staged — to be fixed after the pilot rather than before, so collection is not biased toward a foregone conclusion.

- **RQ-A (inter-model structure — exploratory, staged).** How much do models agree with one another per sentence, and does that agreement map onto recorded model attributes? Attributes split into two tiers:
  - **Theory-motivated (foreground):** shared **company / post-training lineage** (prior: shared lineage → correlated outputs and errors) and shared **size / capability tier** (prior: convergent competence → a scaling story).
  - **Recorded-and-explored (background, no prior mechanism):** country of origin, training-data cutoff / release date, architecture family, open- vs closed-weight, and any other cheap-to-record descriptor.

  **Anti-fishing guardrails (binding):** (1) **report the whole map, not the winner** — every attribute examined is shown, including the null ones; (2) **frame output as "what to confirm at scale," not "what is true"** — the pilot identifies which attribute _merits_ a powered confirmatory study, it does not confirm anything; (3) **foreground vs background separation is declared in advance** — theory-motivated attributes are presented as structure we expected to look for; the rest as descriptive exploration. Labeled this way, RQ-A is legitimate exploratory structure-mapping, not fishing.

- **RQ-B (validity of the disagreement structure — confirmatory headline).** Does per-sentence model disagreement track per-sentence human disagreement? Where, and in which signed direction, does it diverge — i.e. where is consensus manufactured? This is the bedrock claim and the sentence readers should repeat.

The dependent construct throughout is **the structure of agreement/disagreement and its alignment with human disagreement** — not raw accuracy against gold.

**Load order (honest staging).** RQ-B is bedrock; it needs the full apparatus (human distributions, model distributions, matched comparison, enough sentences in the danger cell) and the small pilot mainly tests its _feasibility_ — do models converge on the 4 balanced sentences? does the entropy-vs-entropy signal exist at all? RQ-A is what a small pilot can produce a real first result for, because attribute-mapping is answerable descriptively at any scale. If, at pilot scale, the attribute structure does not separate, RQ-A is reported as the exploratory companion rather than a co-headline; that downgrade is pre-authorized and is not a failure.

---

## 5. Design

### 5.1 Principle: a marvel is fully-crossed, not massive

"Systematic" means _structured_, not _large_. The collection is sized so that every axis varied is one we can later hold fixed to isolate its effect, and every axis held constant is one we can defend. Massive-but-confounded is the amateur signature; modest-but-fully-crossed is the goal. Each call is attributable to a named cell.

### 5.2 The grid

- **Models (independent variable):** ~15, accessed via OpenRouter, deliberately spread across **company × size**, with the broader **attribute set recorded per model** for RQ-A (company/lineage, size tier, country of origin, release/cutoff date, architecture family, open/closed weight). Emphasis on open-weight families (the population most likely to be used for cheap at-scale coding, hence where any warning bites hardest), plus one or two frontier models as reader reference points. For RQ-A to have any traction the roster should span at least 2–3 companies at 2–3 matched size tiers each. _Roster construction is a near-term artifact (see §7); budget and time are not constraints, so the grid can be filled rather than approximated._
- **Context (within-item condition):** in-document-context (human-parity) vs sentence-only (degraded). The MLB coders coded each quasi-sentence with the whole unitised extract — section headings included — in front of them, and the manual _requires_ reading the surrounding paragraph and using section headings to resolve ambiguous units (Decision Rules 2 and 11). In-context therefore reproduces the human task and is the **primary condition for the human-vs-model comparison (RQ-B)**; sentence-only is the contrast that isolates how much model ambiguity is missing-context rather than genuine category ambiguity, and it mirrors the cheap chunked pipelines where the warning bites hardest. Context — including the unit's section heading — is carried in the unit records (`cmp_coding_sample.json`).
- **Temperature:** **0** (the replicable/"ideal" anchor) and **1** (the setting most users actually run). These answer different questions and are kept in separate columns: temp 0 is the _agreement_ condition; temp 1 is the _disagreement_ condition where a per-sentence distribution exists to compare against the human distribution. **RQ-B's human-vs-model comparison runs on temp-1 data.** _VITAL NOTE: temp 0 does not mean the output is deterministic — for several backend reasons models still behave stochastically at temp 0._
- **Sentences:** all 179, fixed. **The 4 balanced left-vs-right sentences (NZ-022, GB-041, NZ-045, NZ-007) are designated highest-value pilot items and over-sampled** — they are where RQ-B's sharpest claim lives or dies (do models manufacture consensus there, or split honestly as humans do?).
- **Samples per cell:** ~2 at temp 0 (enough to catch backend non-determinism), ~5 at temp 1. Coarse per-model _by design_: the inter-model distribution at each sentence pools to ~75 draws per context (15 models × 5), a comfortable comparison against 32/23 human coders. Precise single-model per-sentence entropy is **not** needed anywhere in the main argument (reliability is demoted), which keeps the budget lean.

**Approximate volume (full run, indicative):** ~10.7k calls at temp 0 + ~26.9k at temp 1 + a small self-consistency sub-study ≈ **~45k calls total**. Tractable, mostly on cheap open-weight models.

### 5.3 The temperature-access confound (must be handled, not noted)

Some frontier models on OpenRouter do not honor `temperature`/`top_p` — and a provider may _accept_ a parameter while a backend silently _ignores_ it. Untreated, this confounds temperature with model identity for those models. Treatment:

1. **Pre-flight audit.** Before main collection, test every roster model for whether temp/top_p are actually respected (not merely accepted). Result goes in a methods table.
2. **Quarantine.** Temperature-locked models enter only the analyses where temperature is held constant anyway (inter-model agreement at a single setting). They never appear in any claim that _varies_ temperature.

This keeps frontier reference points in the paper without poisoning any temperature comparison.

### 5.4 The self-consistency sub-study (the deflationary setup move)

A small, deep probe — ~4 models, temp 1, one context, ~10 re-runs per sentence — sufficient to establish self-consistency as near-ceiling and set it aside as uninformative about validity. Deliberately _not_ run across all 15 models: precise single-model entropy is not needed anywhere in the main argument. This supplies the one figure for the setup move; it is not a research question.

---

## 6. Analysis plan (paired, item-level, on the matched 179)

1. **Human ambiguity profile (no API; data in hand — Step 0 DONE).** Per-sentence human distribution over categories and over the 7 domains; per-sentence ambiguity (normalized Shannon entropy and 1 − modal share, both reported); per-category human agreement / Fleiss's κ (the achievable human ceiling, category by category); human coder→gold confusion at category, domain, and reduced 3×3 RILE levels. Computed **twice** — full pool (a realistic "crowd" ceiling) and the trained/retained subset per the MLB coder-quality screen (the expert ceiling) — and both reported. **Validation passed:** reproduces MLB to within rounding (Fleiss κ retained GB/NZ = 0.349/0.397 vs published .35/.40; median coder-vs-master Cohen κ GB/NZ/combined = .429/.536/.459 vs published .43/.54/.46; retained set 17 GB / 12 NZ via MLB's exact drop list).
2. **Model disagreement profile.** The same per-sentence entropy machinery applied to the pooled model distributions (temp 1), per context.
3. **RQ-A — inter-model structure (exploratory, staged).** Cross-model agreement per sentence; descriptive mapping of agreement structure onto the recorded attribute set, foreground (company, size) then background (country, date, architecture, weights). Full attribute map reported including nulls; output framed as candidates for a powered confirmatory study, per §4 guardrails.
4. **RQ-B — alignment (confirmatory headline).** Correlation of per-sentence model entropy with human entropy; the signed residual map locating the four 2×2 cells; logistic model of model-error (vs gold) on human entropy with model and context effects (aligned ⇒ positive slope), reported as a _supporting_ view, since the gold-free entropy-vs-entropy comparison is the honest center. The headline comparison runs on the **in-context, temp-1 cell** (human parity); sentence-only enters only as the degraded contrast. The **4 balanced sentences** get their own close read.
5. **Human-ceiling-relative scoring.** Per-category model accuracy reported against the _human agreement rate_ for that category, never against 100%.
6. **Downstream-consequence illustration (discussion only, not a result).** GB-067 as a worked _model-vs-codebook_ sign-flip on the RILE axis, used to motivate why manufactured consensus matters when codes feed derived indices. Explicitly an illustration of stakes, not an estimate of prevalence.

---

## 7. Immediate next steps

1. **The coding instrument (instruction-parity artifact).** Build the model prompt to match what the MLB coders received, so any human–model gap is about coding, not about being handed a different instrument. Faithful commitments: (a) the model is offered the **full 56 standard categories + `000` uncoded**, with the handbook's definitions and the scoring decision rules (DR6–DR11: policy goal beats means; specific position beats 303, 305, 408; group politics yields to specific positions except 703 Agriculture; code the manifest statement, not latent intent; one and only one code) — never the reduced ~21-category gold subset, which would foreclose the off-target errors the study measures; (b) quasi-sentences are pre-unitised (given), as for the coders — the model never unitises; (c) `000` is a live option, as on the coders' menu; (d) the worked answer key printed in the manual (Appendix II margin codes) is excluded. The one parity we cannot grant — and state as a limitation — is _training_: the humans had prior CMP training and a Berlin supervisor; the model has the handbook in context only. The asymmetry favours the human, which only sharpens a finding that models manufacture agreement where trained humans split. _Artifacts: `categories.json` (full scheme + definitions + rile) and `coding_instrument.md` (prompt template; sentence-only and in-context share it and differ only in the context block)._
2. **Human ambiguity profile — DONE (Step 0).** Reference layer every later beat depends on; both blocking decisions resolved with the full robustness grid; danger-cell counts in hand (category-level: 72 primary / 103 full pool / 27 strict — Beat 3/RQ-B well-populated; RILE-directional: 4 balanced, ~10 any-two-sided — RILE confirmed illustration-only). Artifacts in `reports/human/`: `human_codings.csv`, `coders.csv`, `per_sentence_ambiguity.csv`, `human_profile_report.md`; script `src/human_profile.py`.
3. **Merge the human logs into tidy tables (not into the unit records) — DONE as part of Step 0.** `human_codings.csv` (long: coder_id, manifesto, unit_id, code) and `coders.csv` (identity, prior-experience, MLB retained-flag) reference the unit records and `categories.json` rather than nesting distributions inside the stimulus. `000` and every off-gold code kept raw; full-pool-vs-retained and include/exclude stay downstream flags; distributions/entropy computed, never hand-stored. This shared long schema is also the shape model output appends to, so one entropy routine serves humans and models alike (RQ-B).
4. **Model roster as an explicit attribute grid.** Map real model names to company × size tiers **plus** the recorded background attributes (country, release/cutoff date, architecture, weights) with a temperature-access column to fill from the pre-flight audit, and verify the cells actually fill _before_ committing — turning "15 balanced models" from aspiration into a checked invariant.
5. **Run the small LLM pilot.** A handful of models across ≥2 companies, temp 1, focused on the high-human-entropy sentences and especially the **4 balanced** ones. Purpose: (a) confirm the entropy-vs-entropy signal for RQ-B exists and that the danger cell is reachable; (b) produce the first exploratory attribute map for RQ-A; (c) validate the ~75-draw pooled-entropy stability assumption before committing the full run.

---

## 8. Open decisions

### Resolved (were blocking; settled with numbers in Step 0)

- **`000` / uncoded handling — RESOLVED: keep as a class (primary), report with/without as robustness.** It is common, substantively interesting (flagged as especially unreliable), and concentrated in the most ambiguous sentences. Parity reinforces the choice: `000` was a selectable option on the coders' menu and the manual gives it its own decision procedure (§4.2.3.1), so the model must be offered it and the analysis keeps it as a class. Full robustness grid computed both ways.
- **Coder-quality screen as the human reference — RESOLVED: retained subset primary (17 GB / 12 NZ, the expert ceiling), full pool as robustness (the crowd ceiling), both reported.** Computed both ways so neither is a buried researcher choice; retained set derived from MLB's exact drop list, not a self-chosen threshold.

### Non-blocking — settle before their step

- **Gold's status.** Gold is one authority, not ground truth. Report alignment both gold-relative (comparable to the literature) and gold-free (human-consensus vs model-consensus, RQ-B), and treat the gold-free version as the honest headline.
- **Center of gravity between RQ-A and RQ-B.** **Left open on purpose**, leaning co-equal-but-both-honestly-staged. Decided _after_ the pilot, not before, to avoid biasing collection. RQ-B is bedrock regardless; RQ-A's status (co-headline vs exploratory companion) is set by whether the attribute structure separates at pilot scale.
- **Stance toward the "LLMs can replace coders" position.** Warning, even-handed map, or constructive recipe? Deferred to post-analysis. The task-ambiguity framing — that some tasks elicit a stochastic answer even from expert humans — is the neutral entry point that does not require pre-committing.
- **Sampling-budget validation.** The ~5/temp-1 per-model figure is a "coarse-per-model, rich-in-aggregate" choice. The pilot confirms the _pooled_ per-sentence model entropy is stable at ~75 draws before the full run commits.

### Acknowledged limitation (not a research thread)

- **Training-data contamination — single limitations-section note, not studied.** These two texts and their gold codes are published in the manual and in MLB's replication materials, so they may sit in model pretraining. We treat this as a standard, stated threat to validity — as most LLM studies do — not as a research question, and not as a reason to add conditions. (Mitigating fact for the strong form: the manual's PDF interleaves margin codes and prose in a layout that parses poorly, so verbatim recall of the unit→code key is unlikely.) Building the study _around_ contamination was considered and rejected as scope creep that would cost a research-question slot; it is a fine paper, but not this one.

---

## 9. Implementation & Data Provenance Notes

_Technical constraints and verification targets preserved from the design phase to ensure data integrity during execution._

### Primary Source & The MARPOR Version 5 Warning

The primary source for the pedagogical texts and the coding scheme is **Werner & Volkens 2010, Manifesto Coding Instructions (3rd fully revised edition)**.

**CRITICAL:** Do **not** source codes or a codebook from the current MARPOR corpus. Version 5 of the scheme split several categories (e.g., 202 → 202/202_2, 605 → 605/605_2, 703 → 703/703_2), and modern releases recombine them for back-comparability. Sourcing from anywhere but the contemporaneous 2010 handbook risks v5-split codes that do not line up with the 2008-era human gold data. Use the strict 56-category (v1–v4) frame.

### Data Verification Vectors (Unit Testing)

The alignment of text → gold → human distribution must be mechanical, not inferred. Use these exact leading arrays to `assert` that the parsed extraction matches the master files exactly:

- **GB (107 codes):** `0 0 0 305 305 606 305 410 408 …` (matches `master-codersGB.txt`)
- **NZ (72 codes):** `414 414 414 414 414 408 408 402 …` (matches `master-codersNZ.txt`)

If the extraction script yields these exact arrays in this exact order, the alignment to the 32/23 human coders in the logs is intact. _(Step 0 confirms these pass.)_

### Repository Layout

Five buckets, so each kind of thing has one home and the LLM collection (the part
that grows) is isolated before data lands: **inputs** (`data/`), **code** (`src/`),
**collection output** (`runs/`), **analysis output** (`reports/`), **reading** (`refs/`).

```text
manifesto-project-study/
  RESEARCH_PLAN.md          # central narrative and design (this file)
  README.md                 # orientation + how to run

  data/                     # INPUTS — canonical, read-mostly
    human/                  #   raw MLB data: codes.log, codesNZ.log, master-codersGB/NZ.txt,
                            #   mds2005f.dta, CMP_reliability_replication.R
    categories.json         #   56-category + uncoded scheme: 7-domain + RILE map (2010 handbook)
    cmp_coding_sample.json  #   179 quasi-sentence unit records: text, gold, label, section, RILE

  src/                      # CODE
    human_profile.py        #   Beat 1: per-sentence entropy, per-category κ, confusion (DONE)
    run_llms.py             #   RQ-A & RQ-B: collect LLM code distributions over the 179 (to build)
    alignment.py            #   RQ-B: false-consensus, error~entropy; GB-067 illustration (to build)
    prompts/
      coding_instrument.md  #   instruction-parity model prompt (sentence-only / in-context)
    onetime/                #   one-shot build scripts kept for provenance (build_add_sections.py)

  runs/                     # LLM COLLECTION OUTPUT — scales with collection
    raw/                    #   gitignored: one cached file per API call (regenerable)
    predictions.csv         #   tidy long; same schema as reports/human/human_codings.csv

  reports/                  # ANALYSIS OUTPUT
    human/                  #   human profile (DONE): report + human_codings/coders/per_sentence csvs
    llm/                    #   alignment results, summary (to come)

  refs/                     # READING — source documents
    handbook/               #   Werner & Volkens 2010 coding instructions (the instrument)
    mlb/                    #   Mikhaylov/Laver/Benoit coder-reliability papers
    literature/             #   LLM-as-coder / manifesto literature

  archive/                  # prior pilots and drafts (early-experiment/)
```

The shared long schema (`coder_id, manifesto, unit_id, seq, code`) is deliberate:
`runs/predictions.csv` appends model rows in the same shape as
`reports/human/human_codings.csv`, so one entropy routine serves humans and models alike (RQ-B).
