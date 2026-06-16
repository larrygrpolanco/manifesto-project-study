# When models agree, who is right? Inter-model consensus, human disagreement, and the silent capture of a political index

**A matched, item-level study on CMP/Manifesto coding.**

_Working research plan — design phase. Data verified on disk; no LLM runs yet. Read the Open Decisions at the end before collection begins; two of them shape the data and must be settled first._

---

## 1. The problem, stated plainly

Researchers are beginning to use large language models as coders (even in medicine to read and abstract data from un structured notes, find these citations and then this in other fields): hand a model a coding scheme and a corpus, get back categorized text at a scale no human team could match. The appeal is obvious and the practice is spreading faster than its validation. The implicit safety check most people reach for is **agreement** — if several models independently return the same code, the coding "must" be right, the same way we trust a measurement two instruments agree on.

This plan is built around the observation that **the agreement check is not safe on tasks that are genuinely ambiguous**, and that political-text coding is exactly such a task. Two facts collide:

1. **The human ceiling is low and known.** On the Manifesto coding scheme, trained expert coders disagree constantly. Mikhaylov, Laver & Benoit report category-level Fleiss's κ in the low 0.3s and median coder-vs-gold Cohen's κ around 0.43–0.54. The "gold standard" is itself one draw from a distribution of expert opinion, not ground truth. A large share of what any accuracy metric scores as model _error_ may be irreducible _task_ ambiguity — boundaries that expert humans themselves cross. - Review the literature on this. Is a low human ceiling really the norm, i don't think so, something i can report on and find literature on is poor inter-coder agreement practices.

2. **Models can agree with each other for reasons that have nothing to do with being right.** Models drawn from overlapping training corpora and shared post-training lineages (does distilling play a part in this? Check it) can correlate their _outputs_ — and their _errors_ — without independently perceiving anything in the text. When that happens, inter-model agreement is not evidence of a real construct. It is shared bias wearing the costume of consensus. When LLMs are used to abstract variables or identify constructs, how they are used for other downstream analysis can create a compounding bias.

Put those together and a specific danger appears, one that does not require us to decide in advance whether LLMs are "good" or "bad" at the task:

> **When models agree confidently on a sentence that humans split on, the consensus is manufactured.** A researcher trusting model agreement would record that sentence as settled, when in truth it is one of the contested cases — and they would do so _systematically_, in whatever direction the models happen to lean.

The contribution of this study is to make that danger **measurable**, using the one body of data in the CMP world where it can be measured cleanly, and to follow it through to a consequence political scientists actually care about: **distortion of a derived index (RILE)**.

---

## 2. Why this data, and why it is the only data that works

This is a _matched, paired_ design: the same sentences, coded by many humans and by many models, compared item by item. The matching is what gives the study its teeth — every claim is about the _same sentence_ on both sides, so "where humans disagree" and "where models disagree" are directly comparable rather than rhymed across unrelated corpora.

The human side is the rare asset. In the Mikhaylov–Laver–Benoit reliability experiment, ~30 GB coders and ~23 NZ coders coded the **same** quasi-sentences. That means every sentence carries a full **distribution** of human codes — a per-sentence ambiguity score (entropy / modal share), not merely an aggregate reliability number. This per-item human disagreement signal is **not reproducible from any other CMP data** and is precisely the referee the central question needs.

**Verified on disk (already in hand):**

| document                      | sentences | human coders (raw) | aligned to gold |
| ----------------------------- | --------: | -----------------: | --------------- |
| GB: Liberal/SDP Alliance 1983 |       107 |                 32 | yes             |
| NZ: National Party 1972       |        72 |                 23 | yes             |

The aligned unit records (`cmp_coding_sample.json`) carry, per quasi-sentence: text, master (gold) code, master label, and RILE position. The two logs (`codes.log`, `codesNZ.log`) carry every coder's full code vector, column-aligned to the 107/72 units and verified position-by-position against the master files. Coder identity is unique (email) in both files, so the per-coder layer needed for the coder-quality screen is intact.

**Coding scheme — period-correct by construction.** These human coders worked under the **3rd fully revised edition** of the Manifesto Coding Instructions (Werner & Volkens 2010, MARPOR/WZB), the CMP 56-category + uncoded scheme. We use _that_ edition because it is the instrument the humans actually used; sourcing categories or definitions from any other release would compare model output against a codebook the humans never saw. The JSON already documents three handbook-vs-master divergences for transparency; the unit records use the master coding throughout.

**Coverage is a boundary condition, not a caveat.** The two texts exercise ~21 of the scheme's categories (verified present in the gold coding), with a RILE split of 50 left / 59 right / 70 none across the 179 units. Per-category claims live or die on those ~21 categories, and RILE is genuinely exercised — both stated up front, not buried. (Coders, and the models, choose from the _full_ 56 + uncoded scheme; the ~21 is gold coverage, not the option space.)

**These are the manual's teaching texts, not typical ones.** Both documents are the coding manual's own instructional examples (Werner & Volkens 2010, §5; Klingemann et al. 2006, Appendix II), hand-picked for clarity and codeability to teach the scheme. That they _still_ produced category-level Fleiss's κ ≈ 0.35 and median coder-vs-gold Cohen's κ ≈ 0.46 is a floor-raising fact for Beat 1: if the pedagogical best case is this noisy, production manifestos are noisier. Stated as a boundary on the human ceiling, not buried.

---

## 3. The narrative spine

The paper moves in five beats. Each beat is a question with a number attached, and the beats are ordered so that each one earns the next. Crucially, **none of the beats requires us to have pre-decided the paper's verdict** — the data picks the verdict, not us.

**Beat 1 — The task is stochastic, even for experts.**
We open by re-establishing, on our own item-level data, that human coders do not agree: a per-sentence human disagreement profile. This reframes the entire enterprise. On this task, "the right code" is often not a point but a distribution. _This is the ground the whole argument stands on, and it is the honest version of the field's discomfort: we routinely compare models to a human standard that is itself unstable._

**Beat 2 — Models are individually consistent. So what?**
A brief, deliberately deflationary result: within a single model, re-runs agree (especially at low temperature). The naïve reader takes this as "the task is solved." We show self-consistency is **uninformative about validity** — a model can be perfectly consistent and consistently wrong. This beat exists to disarm the most common false comfort and then move on. It is one paragraph and one figure, not a section.

**Beat 3 — Models agree with _each other_. Is that signal or bias?**
The first novel measurement: cross-model disagreement per sentence — the machine analogue of inter-coder reliability — set beside the human cross-coder disagreement on the same sentences. Then the mechanism probe that decides what the agreement _means_:

> Does inter-model agreement cluster **by company** (shared lineage → bias), **by size** (shared capability → a scaling story), or by **neither** (convergence on something real in the text)?

This single cut is the hinge of the paper. It is why the model roster must be a balanced **company × size grid** rather than a convenience sample: the question is only answerable if the cells fill.

**Beat 4 — The referee: does model disagreement track human disagreement?**
The cleanest form of the central question, and the one that needs no privileged gold: correlate per-sentence model entropy with per-sentence human entropy. Then examine the **signed residual** — the sentences where the two diverge:

- Humans split, models agree → **manufactured consensus** (the danger zone).
- Humans agree, models split → models inject noise where the task is actually clear.
- Both agree / both split → the task's real easy and hard cases.

The 2×2 that organizes the finding:

|                  | Humans agree      | Humans split                     |
| ---------------- | ----------------- | -------------------------------- |
| **Models agree** | construct is real | **false consensus — the danger** |
| **Models split** | models add noise  | shared, honest difficulty        |

**Beat 5 — The consequence: a captured index.**
The payoff that makes a methodologist's warning matter to a substantive researcher. CMP's RILE index is a signed aggregate (right categories minus left, over a document). A _systematic_ lean in how models resolve ambiguous quasi-sentences does not cancel on aggregation — it **accumulates directionally** into a RILE shift. We already hold a concrete, non-hypothetical instance: unit GB-067, a single quasi-sentence whose coding flips RILE _sign_ between two defensible readings (handbook 201, Freedom/Human Rights, rile-right vs master 701, Labour Groups, rile-left). If models systematically resolve a _class_ of such boundaries one way where humans are split, that is a RILE bias **with a mechanism**, not a correlation — a worked demonstration of how trusting model consensus silently moves a number that political scientists treat as data.

The landing: _agreement among models is not validity. On ambiguous coding tasks, treating it as validity imports model-specific structure into downstream measures — and we can show the import happening, sentence by sentence, all the way up to the index._

---

## 4. Research questions

Stance-neutral by design. Each maps to a quantity we must collect, and all are computed from one shared collection — so the center of gravity can stay unchosen until the data is in.

- **RQ1 (reliability — control, not headline).** How self-consistent is a model across re-runs, as a function of temperature? _Expected near-ceiling; reported to neutralize the "task is solved" reflex._
- **RQ2 (inter-model structure).** How much do models agree with one another per sentence, and **does that agreement cluster by company, by size, or neither?**
- **RQ3 (validity of the disagreement structure).** Does per-sentence model disagreement track per-sentence human disagreement? Where, and in which signed direction, does it diverge?
- **RQ4 (downstream consequence).** Do the per-sentence patterns aggregate into systematic distortion of RILE at the document level, relative to the human-gold RILE?

The dependent construct throughout is **the structure of agreement/error and its alignment with human disagreement** — not raw accuracy against gold.

---

## 5. Design

### 5.1 Principle: a marvel is fully-crossed, not massive

"Systematic" means _structured_, not _large_. The collection is sized so that every axis varied is one we can later hold fixed to isolate its effect, and every axis held constant is one we can defend. Massive-but-confounded is the amateur signature; modest-but-fully-crossed is the goal. Each call is attributable to a named cell.

### 5.2 The grid

- **Models (independent variable):** ~15, accessed via OpenRouter, deliberately **balanced across company × size**. Emphasis on open-weight families (the population most likely to be used for cheap at-scale coding, hence where any warning bites hardest), plus one or two frontier models as reader reference points. The roster must fill a company × size grid — at least 2–3 companies at 2–3 matched size tiers each — or Beat 3 has empty cells and dies. _Roster construction is the next artifact (see §7)._
- **Context (within-item condition):** in-document-context (human-parity) vs sentence-only (degraded). The MLB coders coded each quasi-sentence with the whole unitised extract — section headings included — in front of them, and the manual _requires_ reading the surrounding paragraph and using section headings to resolve ambiguous units (Decision Rules 2 and 11). In-context therefore reproduces the human task and is the **primary condition for the human-vs-model comparison (RQ3)**; sentence-only is the contrast that isolates how much model ambiguity is missing-context rather than genuine category ambiguity, and it mirrors the cheap chunked pipelines where the warning bites hardest. Context — including the unit's section heading — is carried in the unit records (`cmp_coding_sample.json`).
- **Temperature:** **0** (the replicable/"ideal" anchor) and **1** (the setting most users actually run). These answer different questions and are kept in separate columns: temp 0 is the _agreement_ condition; temp 1 is the _disagreement_ condition where a per-sentence distribution exists to compare against the human distribution. **RQ3's human-vs-model comparison runs on temp-1 data**, VITAL NOTE: temp 0 does not mean the output is deterministic, for various complicated reasons models still perform stochasticly at temp 0!
- **Sentences:** all 179, fixed.
- **Samples per cell:** ~2 at temp 0 (enough to catch backend non-determinism), ~5 at temp 1. Coarse per-model _by design_: the inter-model distribution at each sentence pools to ~75 draws per context (15 models × 5), a comfortable comparison against 32/23 human coders. We do **not** need precise single-model per-sentence entropy, because RQ1 is a control, not a headline — this is the choice that keeps the budget lean.

**Approximate volume:** ~10.7k calls at temp 0 + ~26.9k at temp 1 + ~7.2k for a small 4-model reliability sub-study ≈ **45k calls total**. Tractable, mostly on cheap open-weight models.

### 5.3 The temperature-access confound (must be handled, not noted)

Some frontier models on OpenRouter do not honor `temperature`/`top_p` — and a provider may _accept_ a parameter while a backend silently _ignores_ it. Untreated, this confounds temperature with model identity for those models. Treatment:

1. **Pre-flight audit.** Before main collection, test every roster model for whether temp/top_p are actually respected (not merely accepted). Result goes in a methods table.
2. **Quarantine.** Temperature-locked models enter only the analyses where temperature is held constant anyway (inter-model agreement, company × size at a single setting). They never appear in any claim that _varies_ temperature.

This keeps frontier reference points in the paper without poisoning the variance decomposition.

### 5.4 The reliability sub-study (Beat 2)

A small, deep probe — ~4 models, temp 1, one context, ~10 re-runs per sentence — sufficient to establish self-consistency as near-floor and set it aside. Deliberately _not_ run across all 15 models: precise single-model entropy is not needed anywhere in the main argument.

---

## 6. Analysis plan (paired, item-level, on the matched 179)

1. **Human ambiguity profile (no API; data in hand).** Per-sentence human distribution over categories and over the 7 domains; per-sentence ambiguity (normalized Shannon entropy and 1 − modal share, both reported); per-category human agreement / Fleiss's κ (the achievable human ceiling, category by category); human coder→gold confusion at category, domain, and reduced 3×3 RILE levels. Computed **twice** — full pool (a realistic "crowd" ceiling) and the trained/retained subset per the MLB coder-quality screen (the expert ceiling) — and both reported.
2. **Model disagreement profile.** The same per-sentence entropy machinery applied to the pooled model distributions (temp 1), per context.
3. **RQ2 — inter-model structure.** Cross-model agreement per sentence; cluster/variance decomposition of agreement by **company** vs **size**. This is the bias-vs-signal test.
4. **RQ3 — alignment.** Correlation of per-sentence model entropy with human entropy; the signed residual map locating the four 2×2 cells; logistic model of model-error (vs gold) on human entropy with model and context effects (aligned ⇒ positive slope), reported as a supporting view rather than the headline, since the gold-free entropy-vs-entropy comparison is the honest center. The headline comparison runs on the **in-context, temp-1 cell** (human parity); sentence-only enters only as the degraded contrast.
5. **RQ4 — RILE consequence.** Document-level RILE under human-gold vs each model and the model consensus; decomposition of any shift into the ambiguous-sentence classes driving it; GB-067 as the worked sign-flip illustration. Where do models send their off-diagonal mass, and is it directional on the RILE axis?
6. **Human-ceiling-relative scoring.** Per-category model accuracy reported against the _human agreement rate_ for that category, never against 100%.

---

## 7. Immediate next steps (no API required)

1. **The coding instrument (instruction-parity artifact).** Build the model prompt to match what the MLB coders received, so any human–model gap is about coding, not about being handed a different instrument. Faithful commitments: (a) the model is offered the **full 56 standard categories + `000` uncoded**, with the handbook's definitions and the scoring decision rules (DR6–DR11: policy goal beats means; specific position beats 303, 305, 408; group politics yields to specific positions except 703 Agriculture; code the manifest statement, not latent intent; one and only one code) — never the reduced ~21-category gold subset, which would foreclose the off-target errors the study measures; (b) quasi-sentences are pre-unitised (given), as for the coders — the model never unitises; (c) `000` is a live option, as on the coders' menu; (d) the worked answer key printed in the manual (Appendix II margin codes) is excluded. The one parity we cannot grant — and state as a limitation — is _training_: the humans had prior CMP training and a Berlin supervisor; the model has the handbook in context only. The asymmetry favours the human, which only sharpens a finding that models manufacture agreement where trained humans split. _Artifacts: `categories.json` (full scheme + definitions + rile) and `coding_instrument.md` (prompt template; sentence-only and in-context share it and differ only in the context block)._
2. **Human ambiguity profile.** An evening on data already on disk; produces the reference layer every later beat depends on and tells us the shape of human ambiguity before any compute is spent.
3. **Merge the human logs into tidy tables (not into the unit records).** Emit `human_codings.csv` (long: coder_id, manifesto, unit_id, code) and `coders.csv` (identity, prior-experience, MLB retained-flag), referencing the unit records and `categories.json` rather than nesting distributions inside the stimulus. Keep `000` and every off-gold code raw; full-pool-vs-retained and include/exclude stay downstream flags, not storage decisions; distributions/entropy are computed, never hand-stored. This shared long schema is also the shape model output appends to, so one entropy routine serves humans and models alike (RQ3).
4. **Model roster as an explicit company × size grid.** Map real model names to tiers with a temperature-access column to fill from the pre-flight audit, and verify the cells actually fill _before_ committing — turning "15 balanced models" from aspiration into a checked invariant.

---

## 8. Open decisions — settle before the relevant step

_These are deliberately unresolved. Two of them shape the data itself and must be decided before any entropy is computed; the rest can wait for their step. Bringing these to the top of the next review._

### Blocking — must settle before computing the human profile

- **`000` / uncoded handling.** Treat as a 57th class or exclude? It is common, substantively interesting (the paper flags it as especially unreliable), and concentrated in exactly the most ambiguous sentences — the ones the whole argument rests on. Its handling changes the entropy of those pivotal sentences. _Leaning:_ keep it as a class and report with/without as robustness. Parity reinforces the lean — `000` was a selectable option on the coders' menu and the manual gives it its own decision procedure (§4.2.3.1), so the model must be offered it and the analysis keeps it as a class; with/without stays the robustness check. **Decide before the human profile is computed.**
- **Coder-quality screen as the human reference.** Is the human "distribution" the full pool or the MLB-retained subset (17 GB / 12 NZ)? This changes every human-entropy value and therefore every RQ3 comparison. _Leaning:_ retained subset as primary (the expert ceiling), full pool as robustness (the crowd ceiling), both reported. **Decide before the human profile is computed.**

### Non-blocking — settle before their step

- **Gold's status.** Gold is one authority, not ground truth. Report alignment both gold-relative (comparable to the literature) and gold-free (human-consensus vs model-consensus, RQ3), and treat the gold-free version as the honest headline.
- **Training-data contamination.** These two texts and their gold codes are published in the coding manual and in MLB's replication materials, so they may sit in model pretraining. Mitigating fact: the manual's PDF interleaves margin codes and prose in a layout machines parse poorly (the code column does not line up with sentences), so verbatim recall of the unit→code key is unlikely; still, partial exposure could inflate gold-agreement non-uniformly across model families and confound the company/size cut (RQ2). Treat as a stated threat; probe with a recall check (can a model reproduce the gold for held-out units?) and read RQ2 cautiously if any can. More broadly, memorisation-vs-reading is a standing source of model bias worth flagging in the paper.
- **Sampling budget validation.** The ~5/temp-1 per-model figure is a "coarse-per-model, rich-in-aggregate" choice. Pilot a handful of sentences to confirm the _pooled_ per-sentence model entropy is stable at ~75 draws before committing the full run.
- **Center of gravity / stance.** Left open on purpose. All of Beats 3–5 (false-consensus mechanism, RILE drift, practitioner protocol) are computed from the same collection; which becomes the headline is decided _after_ analysis, not before, to avoid biasing collection toward a foregone conclusion.

### Questions carried in from this design session

1. _Where should the paper's center of gravity sit_ — false-consensus mechanism, RILE drift, or practitioner protocol? **Deferred to post-analysis by decision.**
2. _How adversarial toward the "LLMs can replace coders" position_ — warning, even-handed map, or constructive recipe? **Deferred to post-analysis by decision** (running before taking a stance, to avoid biasing the result; the task-ambiguity framing — that some tasks elicit a stochastic answer even from expert humans — is the neutral entry point).
3. _Roster scope_ — settled: ~15 models, balanced company × size, open-weight emphasis + 1–2 frontier reference points; build and verify the grid next.
4. _Vary prompt/context?_ — settled: sentence-only vs in-document-context.
5. _Temperature plan_ — settled: 0 and 1 for the main collection; temperature-locked models quarantined per §5.3.
6. _Matched size tiers across companies?_ — confirmed available; to be made explicit in the roster grid.

## 9. Implementation & Data Provenance Notes

_The following technical constraints and verification targets are preserved from the initial design phase to ensure data integrity during execution._

### Primary Source & The MARPOR Version 5 Warning

The primary source for the pedagogical texts and the coding scheme is **Werner & Volkens 2010, Manifesto Coding Instructions (3rd fully revised edition)**.

**CRITICAL:** Do **not** source codes or a codebook from the current MARPOR corpus. Version 5 of the scheme split several categories (e.g., 202 → 202/202_2, 605 → 605/605_2, 703 → 703/703_2), and modern releases recombine them for back-comparability. Sourcing from anywhere but the contemporaneous 2010 handbook risks v5-split codes that do not line up with the 2008-era human gold data. Use the strict 56-category (v1–v4) frame.

### Data Verification Vectors (Unit Testing)

The alignment of text → gold → human distribution must be mechanical, not inferred. Use these exact leading arrays to `assert` that the parsed extraction matches the master files exactly:

- **GB (107 codes):** `0 0 0 305 305 606 305 410 408 …` (matches `master-codersGB.txt`)
- **NZ (72 codes):** `414 414 414 414 414 408 408 402 …` (matches `master-codersNZ.txt`)

If the extraction script yields these exact arrays in this exact order, the alignment to the 32/23 human coders in the logs is intact.

### The "Dumping Ground" Hypothesis (Off-Diagonal Mass)

The handbook's own tie-break rules tell us in advance which boundaries are porous. This gives us a testable prior for Beat 5 about _where_ models and humans will scatter their errors:

- **Domain-7 Group Codes:** Specific policies beat Domain-7 group codes (except 703) → expect group codes to bleed.
- **Category 305 (Political Authority):** Specific policies beat 305 → expect 305 to act as a dumping ground.
- **Category 408 (General Economic Goals):** Specific policies beat 408 → expect 408 to act as a dumping ground.

### Repository Layout

```text
study/
  RESEARCH_PLAN.md       # central narrative and design
  config.py              # models, conditions, sampling N, codebook + scheme params
  data/
    human/               # codes.log, codesNZ.log, master-codersGB.txt, master-codersNZ.txt
    sentences.csv        # 179 quasi-sentence texts + gold, aligned (from handbook)
    codebook.csv         # 56-category frame + 7-domain map (from handbook)
  src/
    extract_sentences.py # parse handbook text -> sentences.csv; assert match to gold vectors
    human_profile.py     # Beat 1: per-sentence entropy, per-category κ, human confusion
    run_llms.py          # Beats 2 & 3: collect LLM code distributions over the 179
    alignment.py         # Beats 4 & 5: false-consensus, error~entropy, RILE consequence
  reports/               # human profile, alignment results, summary.md
```
