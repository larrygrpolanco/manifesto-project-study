# When models agree, who is right? Inter-model consensus, human disagreement, and the silent capture of a political index

**A matched, item-level study on CMP/Manifesto coding.**

*Working research plan — design phase. Data verified on disk; no LLM runs yet. Read the Open Decisions at the end before collection begins; two of them shape the data and must be settled first.*

---

## 1. The problem, stated plainly

Researchers are beginning to use large language models as coders: hand a model a coding scheme and a corpus, get back categorized text at a scale no human team could match. The appeal is obvious and the practice is spreading faster than its validation. The implicit safety check most people reach for is **agreement** — if several models independently return the same code, the coding "must" be right, the same way we trust a measurement two instruments agree on.

This plan is built around the observation that **the agreement check is not safe on tasks that are genuinely ambiguous**, and that political-text coding is exactly such a task. Two facts collide:

1. **The human ceiling is low and known.** On the Manifesto coding scheme, trained expert coders disagree constantly. Mikhaylov, Laver & Benoit report category-level Fleiss's κ in the low 0.3s and median coder-vs-gold Cohen's κ around 0.43–0.54. The "gold standard" is itself one draw from a distribution of expert opinion, not ground truth. A large share of what any accuracy metric scores as model *error* may be irreducible *task* ambiguity — boundaries that expert humans themselves cross.

2. **Models can agree with each other for reasons that have nothing to do with being right.** Models drawn from overlapping training corpora and shared post-training lineages can correlate their *outputs* — and their *errors* — without independently perceiving anything in the text. When that happens, inter-model agreement is not evidence of a real construct. It is shared bias wearing the costume of consensus.

Put those together and a specific danger appears, one that does not require us to decide in advance whether LLMs are "good" or "bad" at the task:

> **When models agree confidently on a sentence that humans split on, the consensus is manufactured.** A researcher trusting model agreement would record that sentence as settled, when in truth it is one of the contested cases — and they would do so *systematically*, in whatever direction the models happen to lean.

The contribution of this study is to make that danger **measurable**, using the one body of data in the CMP world where it can be measured cleanly, and to follow it through to a consequence political scientists actually care about: **distortion of a derived index (RILE)**.

---

## 2. Why this data, and why it is the only data that works

This is a *matched, paired* design: the same sentences, coded by many humans and by many models, compared item by item. The matching is what gives the study its teeth — every claim is about the *same sentence* on both sides, so "where humans disagree" and "where models disagree" are directly comparable rather than rhymed across unrelated corpora.

The human side is the rare asset. In the Mikhaylov–Laver–Benoit reliability experiment, ~30 GB coders and ~23 NZ coders coded the **same** quasi-sentences. That means every sentence carries a full **distribution** of human codes — a per-sentence ambiguity score (entropy / modal share), not merely an aggregate reliability number. This per-item human disagreement signal is **not reproducible from any other CMP data** and is precisely the referee the central question needs.

**Verified on disk (already in hand):**

| document | sentences | human coders (raw) | aligned to gold |
|---|---:|---:|---|
| GB: Liberal/SDP Alliance 1983 | 107 | 32 | yes |
| NZ: National Party 1972 | 72 | 23 | yes |

The aligned unit records (`cmp_coding_sample.json`) carry, per quasi-sentence: text, master (gold) code, master label, and RILE position. The two logs (`codes.log`, `codesNZ.log`) carry every coder's full code vector, column-aligned to the 107/72 units and verified position-by-position against the master files. Coder identity is unique (email) in both files, so the per-coder layer needed for the coder-quality screen is intact.

**Coding scheme — period-correct by construction.** These human coders worked under the **3rd fully revised edition** of the Manifesto Coding Instructions (Werner & Volkens 2010, MARPOR/WZB), the CMP 56-category + uncoded scheme. We use *that* edition because it is the instrument the humans actually used; sourcing categories or definitions from any other release would compare model output against a codebook the humans never saw. The JSON already documents three handbook-vs-master divergences for transparency; the unit records use the master coding throughout.

**Coverage is a boundary condition, not a caveat.** The two texts exercise ~21 of the scheme's categories (verified present in the data), with a RILE split of 50 left / 59 right / 70 none across the 179 units. Per-category claims live or die on those ~21 categories, and RILE is genuinely exercised — both stated up front, not buried.

---

## 3. The narrative spine

The paper moves in five beats. Each beat is a question with a number attached, and the beats are ordered so that each one earns the next. Crucially, **none of the beats requires us to have pre-decided the paper's verdict** — the data picks the verdict, not us.

**Beat 1 — The task is stochastic, even for experts.**
We open by re-establishing, on our own item-level data, that human coders do not agree: a per-sentence human disagreement profile. This reframes the entire enterprise. On this task, "the right code" is often not a point but a distribution. *This is the ground the whole argument stands on, and it is the honest version of the field's discomfort: we routinely compare models to a human standard that is itself unstable.*

**Beat 2 — Models are individually consistent. So what?**
A brief, deliberately deflationary result: within a single model, re-runs agree (especially at low temperature). The naïve reader takes this as "the task is solved." We show self-consistency is **uninformative about validity** — a model can be perfectly consistent and consistently wrong. This beat exists to disarm the most common false comfort and then move on. It is one paragraph and one figure, not a section.

**Beat 3 — Models agree with *each other*. Is that signal or bias?**
The first novel measurement: cross-model disagreement per sentence — the machine analogue of inter-coder reliability — set beside the human cross-coder disagreement on the same sentences. Then the mechanism probe that decides what the agreement *means*:

> Does inter-model agreement cluster **by company** (shared lineage → bias), **by size** (shared capability → a scaling story), or by **neither** (convergence on something real in the text)?

This single cut is the hinge of the paper. It is why the model roster must be a balanced **company × size grid** rather than a convenience sample: the question is only answerable if the cells fill.

**Beat 4 — The referee: does model disagreement track human disagreement?**
The cleanest form of the central question, and the one that needs no privileged gold: correlate per-sentence model entropy with per-sentence human entropy. Then examine the **signed residual** — the sentences where the two diverge:

- Humans split, models agree → **manufactured consensus** (the danger zone).
- Humans agree, models split → models inject noise where the task is actually clear.
- Both agree / both split → the task's real easy and hard cases.

The 2×2 that organizes the finding:

| | Humans agree | Humans split |
|---|---|---|
| **Models agree** | construct is real | **false consensus — the danger** |
| **Models split** | models add noise | shared, honest difficulty |

**Beat 5 — The consequence: a captured index.**
The payoff that makes a methodologist's warning matter to a substantive researcher. CMP's RILE index is a signed aggregate (right categories minus left, over a document). A *systematic* lean in how models resolve ambiguous quasi-sentences does not cancel on aggregation — it **accumulates directionally** into a RILE shift. We already hold a concrete, non-hypothetical instance: unit GB-067, a single quasi-sentence whose coding flips RILE *sign* between two defensible readings (handbook 201, Freedom/Human Rights, rile-right vs master 701, Labour Groups, rile-left). If models systematically resolve a *class* of such boundaries one way where humans are split, that is a RILE bias **with a mechanism**, not a correlation — a worked demonstration of how trusting model consensus silently moves a number that political scientists treat as data.

The landing: *agreement among models is not validity. On ambiguous coding tasks, treating it as validity imports model-specific structure into downstream measures — and we can show the import happening, sentence by sentence, all the way up to the index.*

---

## 4. Research questions

Stance-neutral by design. Each maps to a quantity we must collect, and all are computed from one shared collection — so the center of gravity can stay unchosen until the data is in.

- **RQ1 (reliability — control, not headline).** How self-consistent is a model across re-runs, as a function of temperature? *Expected near-ceiling; reported to neutralize the "task is solved" reflex.*
- **RQ2 (inter-model structure).** How much do models agree with one another per sentence, and **does that agreement cluster by company, by size, or neither?**
- **RQ3 (validity of the disagreement structure).** Does per-sentence model disagreement track per-sentence human disagreement? Where, and in which signed direction, does it diverge?
- **RQ4 (downstream consequence).** Do the per-sentence patterns aggregate into systematic distortion of RILE at the document level, relative to the human-gold RILE?

The dependent construct throughout is **the structure of agreement/error and its alignment with human disagreement** — not raw accuracy against gold.

---

## 5. Design

### 5.1 Principle: a marvel is fully-crossed, not massive

"Systematic" means *structured*, not *large*. The collection is sized so that every axis varied is one we can later hold fixed to isolate its effect, and every axis held constant is one we can defend. Massive-but-confounded is the amateur signature; modest-but-fully-crossed is the goal. Each call is attributable to a named cell.

### 5.2 The grid

- **Models (independent variable):** ~15, accessed via OpenRouter, deliberately **balanced across company × size**. Emphasis on open-weight families (the population most likely to be used for cheap at-scale coding, hence where any warning bites hardest), plus one or two frontier models as reader reference points. The roster must fill a company × size grid — at least 2–3 companies at 2–3 matched size tiers each — or Beat 3 has empty cells and dies. *Roster construction is the next artifact (see §7).*
- **Context (within-item condition):** sentence-only vs sentence-in-document-context. Context is exactly what a human coder uses to resolve an ambiguous quasi-sentence, so this condition mirrors the human task and lets us ask whether context resolves or merely shifts model ambiguity.
- **Temperature:** **0** (the replicable/"ideal" anchor) and **1** (the setting most users actually run). These answer different questions and are kept in separate columns: temp 0 is the *agreement* condition; temp 1 is the *disagreement* condition where a per-sentence distribution exists to compare against the human distribution. **RQ3's human-vs-model comparison runs on temp-1 data**, because at temp 0 the model collapses to a point and there is no distribution to compare.
- **Sentences:** all 179, fixed.
- **Samples per cell:** ~2 at temp 0 (enough to catch backend non-determinism), ~5 at temp 1. Coarse per-model *by design*: the inter-model distribution at each sentence pools to ~75 draws per context (15 models × 5), a comfortable comparison against 32/23 human coders. We do **not** need precise single-model per-sentence entropy, because RQ1 is a control, not a headline — this is the choice that keeps the budget lean.

**Approximate volume:** ~10.7k calls at temp 0 + ~26.9k at temp 1 + ~7.2k for a small 4-model reliability sub-study ≈ **45k calls total**. Tractable, mostly on cheap open-weight models.

### 5.3 The temperature-access confound (must be handled, not noted)

Some frontier models on OpenRouter do not honor `temperature`/`top_p` — and a provider may *accept* a parameter while a backend silently *ignores* it. Untreated, this confounds temperature with model identity for those models. Treatment:

1. **Pre-flight audit.** Before main collection, test every roster model for whether temp/top_p are actually respected (not merely accepted). Result goes in a methods table.
2. **Quarantine.** Temperature-locked models enter only the analyses where temperature is held constant anyway (inter-model agreement, company × size at a single setting). They never appear in any claim that *varies* temperature.

This keeps frontier reference points in the paper without poisoning the variance decomposition.

### 5.4 The reliability sub-study (Beat 2)

A small, deep probe — ~4 models, temp 1, one context, ~10 re-runs per sentence — sufficient to establish self-consistency as near-floor and set it aside. Deliberately *not* run across all 15 models: precise single-model entropy is not needed anywhere in the main argument.

---

## 6. Analysis plan (paired, item-level, on the matched 179)

1. **Human ambiguity profile (no API; data in hand).** Per-sentence human distribution over categories and over the 7 domains; per-sentence ambiguity (normalized Shannon entropy and 1 − modal share, both reported); per-category human agreement / Fleiss's κ (the achievable human ceiling, category by category); human coder→gold confusion at category, domain, and reduced 3×3 RILE levels. Computed **twice** — full pool (a realistic "crowd" ceiling) and the trained/retained subset per the MLB coder-quality screen (the expert ceiling) — and both reported.
2. **Model disagreement profile.** The same per-sentence entropy machinery applied to the pooled model distributions (temp 1), per context.
3. **RQ2 — inter-model structure.** Cross-model agreement per sentence; cluster/variance decomposition of agreement by **company** vs **size**. This is the bias-vs-signal test.
4. **RQ3 — alignment.** Correlation of per-sentence model entropy with human entropy; the signed residual map locating the four 2×2 cells; logistic model of model-error (vs gold) on human entropy with model and context effects (aligned ⇒ positive slope), reported as a supporting view rather than the headline, since the gold-free entropy-vs-entropy comparison is the honest center.
5. **RQ4 — RILE consequence.** Document-level RILE under human-gold vs each model and the model consensus; decomposition of any shift into the ambiguous-sentence classes driving it; GB-067 as the worked sign-flip illustration. Where do models send their off-diagonal mass, and is it directional on the RILE axis?
6. **Human-ceiling-relative scoring.** Per-category model accuracy reported against the *human agreement rate* for that category, never against 100%.

---

## 7. Immediate next steps (no API required)

1. **Human ambiguity profile.** An evening on data already on disk; produces the reference layer every later beat depends on and tells us the shape of human ambiguity before any compute is spent.
2. **Model roster as an explicit company × size grid.** Map real model names to tiers with a temperature-access column to fill from the pre-flight audit, and verify the cells actually fill *before* committing — turning "15 balanced models" from aspiration into a checked invariant.
3. **Merge the human logs into the unit records.** Fold each coder's code into the matching unit (raw per-coder layer + cached distribution), keep a separate `coders` table carrying identity, affiliation, and the retained-flag for the MLB screen. Keep `000`/uncoded in the raw layer; make include/exclude a downstream flag, not a storage decision.

---

## 8. Open decisions — settle before the relevant step

*These are deliberately unresolved. Two of them shape the data itself and must be decided before any entropy is computed; the rest can wait for their step. Bringing these to the top of the next review.*

### Blocking — must settle before computing the human profile

- **`000` / uncoded handling.** Treat as a 57th class or exclude? It is common, substantively interesting (the paper flags it as especially unreliable), and concentrated in exactly the most ambiguous sentences — the ones the whole argument rests on. Its handling changes the entropy of those pivotal sentences. *Leaning:* keep it as a class and report with/without as robustness. **Decide before the human profile is computed.**
- **Coder-quality screen as the human reference.** Is the human "distribution" the full pool or the MLB-retained subset (17 GB / 12 NZ)? This changes every human-entropy value and therefore every RQ3 comparison. *Leaning:* retained subset as primary (the expert ceiling), full pool as robustness (the crowd ceiling), both reported. **Decide before the human profile is computed.**

### Non-blocking — settle before their step

- **Gold's status.** Gold is one authority, not ground truth. Report alignment both gold-relative (comparable to the literature) and gold-free (human-consensus vs model-consensus, RQ3), and treat the gold-free version as the honest headline.
- **Sampling budget validation.** The ~5/temp-1 per-model figure is a "coarse-per-model, rich-in-aggregate" choice. Pilot a handful of sentences to confirm the *pooled* per-sentence model entropy is stable at ~75 draws before committing the full run.
- **Center of gravity / stance.** Left open on purpose. All of Beats 3–5 (false-consensus mechanism, RILE drift, practitioner protocol) are computed from the same collection; which becomes the headline is decided *after* analysis, not before, to avoid biasing collection toward a foregone conclusion.

### Questions carried in from this design session

1. *Where should the paper's center of gravity sit* — false-consensus mechanism, RILE drift, or practitioner protocol? **Deferred to post-analysis by decision.**
2. *How adversarial toward the "LLMs can replace coders" position* — warning, even-handed map, or constructive recipe? **Deferred to post-analysis by decision** (running before taking a stance, to avoid biasing the result; the task-ambiguity framing — that some tasks elicit a stochastic answer even from expert humans — is the neutral entry point).
3. *Roster scope* — settled: ~15 models, balanced company × size, open-weight emphasis + 1–2 frontier reference points; build and verify the grid next.
4. *Vary prompt/context?* — settled: sentence-only vs in-document-context.
5. *Temperature plan* — settled: 0 and 1 for the main collection; temperature-locked models quarantined per §5.3.
6. *Matched size tiers across companies?* — confirmed available; to be made explicit in the roster grid.
