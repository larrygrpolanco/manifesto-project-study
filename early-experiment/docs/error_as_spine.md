# Error-as-Spine: Working Document

**Purpose.** A scratchpad for restructuring the manifesto/LLM paper around error structure as the dependent variable. This is the planning document, not the draft. It exists to make the next round of revisions mechanical instead of conceptual.

**Status.** Draft 1, conceptual stage. No experiments run. The taxonomy and downstream mapping below are *candidates* — some will survive contact with a pilot, some won't. That's the point of writing them down now.

---

## Part 1: Revision notes — what changes in the existing draft

These are categorized by amount of work. Tackle in roughly this order so each round of edits has a clear stopping point.

### Cut entirely

- **Section 4.4 (CoT diagnostic).** Already downgraded from centerpiece to supplementary in the previous revision. Now cut. Faithfulness concerns mean CoT can't bear interpretive weight, and the paper no longer needs it to answer RQ3.
- **The "applied linguistics perspective" paragraph in Section 1** (the one ending the introduction). It's decorative. The framing it tries to set up is paid for elsewhere or doesn't get paid for at all.
- **The Swales / Biber / Cotos / Eguchi & Kyle thread at the end of Section 2.3.** The move-step analogy is shallow and gets invoked twice without doing analytical work. Cut.

### Compress to one paragraph

- **AL framing overall.** Replace the scattered AL references with a single honest paragraph (probably late in the introduction or early in the method) that says something like: *"This study treats the Manifesto Project codebook as a linguistic artifact whose structural properties — domain hierarchy, valence pairs, explicit exclusion criteria — shape classifier behavior. This approach is informed by content analysis and coding-scheme design traditions in applied linguistics, where the fit between analytical categories and textual features is recognized as a methodological concern."* That's it. No theoretical scaffolding the paper doesn't pay off. Keep one or two AL citations (Cotos & Şenel is the most directly relevant since it's about LLM-assisted hierarchical annotation) but don't build a leg from them.

### Rewrite around the new spine

- **The Thread (top of draft) and abstract-equivalent.** Currently leads with "this paper tests whether task decomposition changes how LLMs classify political text." Rewrite to lead with the *phenomenon* — error structure in LLM classification of codebooks with domain hierarchy and valence pairs — and frame prompting conditions as the probe. Something like: "Not all classification errors are equal. For codebooks like the Manifesto Project, where downstream uses involve aggregation across categories, the *structure* of errors — which categories absorb misclassifications, whether errors cross domains, whether they flip valence — determines whether errors cancel out or compound. This study develops a codebook-derived error taxonomy for the Manifesto scheme and uses prompting conditions as probes to test how decomposition, codebook visibility, and demonstration affect different error types."
- **Research questions.** RQ1 and RQ2 are fine as scaffolding. RQ3 is the one that changes. New RQ3 candidate: *"How are different prompting conditions associated with different error types in the taxonomy, and what are the implications for downstream Manifesto-derived measures?"* This is testable and tied to concrete predictions (Part 2 below).
- **Section 4.3 (prompting conditions).** Keep the four conditions, but rewrite each one's rationale to include a *predicted differential effect on a specific error type*. Each condition becomes a probe targeted at a specific class of error. Draft predictions in Part 2 of this doc.
- **Section 5 (anticipated results).** Rewrite around the error taxonomy predictions.

### Keep largely as-is (light edits only)

- Section 2.1 (LLMs as measurement tools) — trim slightly
- Section 2.2 (Manifesto as classification challenge) — the agreement stats, SVM baseline, and hierarchy observation all still serve the new framing
- Section 2.4 (temperature/reliability)
- Section 2.5 (error structure and downstream validity) — *becomes more central, not less*; Egami et al. 2023 and Knox et al. 2022 should be promoted within this section
- Section 4.1 (dataset), 4.6 (temperature), 4.7 (evaluation metrics for standard part)
- Section 7 (scope and boundaries) — minor adjustments to reflect new framing

### Add new material

- **Section 4.4 (new): Error Taxonomy.** Replaces the cut CoT section. The new heart of the method. Defines each error type, detection method (automated/semi-automated/manual), and predicted associations with prompting conditions.
- **Section 4.5 (revised): Downstream Measurement Analysis.** Commits to specific Manifesto-derived measures and the mechanical relationship between error types and measure distortion. *See Part 3 of this doc — this needs more research before committing.*
- **Section 4.x (new, short): Development Set.** Brief description of the dev-set / pilot plan for refining the taxonomy before running main experiments.

---

## Part 2: Error taxonomy — draft

The taxonomy is derived from the structure of the codebook itself, not from inductive review of model outputs. This is important: it means the taxonomy is *publishable as a contribution in its own right* even before any models are run, because it's a way of thinking about codebook-derived classification errors that future work can use.

### What the codebook actually has (verified against the uploaded codebook)

The MPDS2020a codebook has:
- 7 policy domains (External Relations, Freedom & Democracy, Political System, Economy, Welfare & Quality of Life, Fabric of Society, Social Groups) plus an uncoded/000 category
- 56 main categories distributed unevenly across these domains
- A subset of categories that form explicit **valence pairs** within domains (e.g., 101/102 Foreign Special Relationships +/−; 104/105 Military +/−; 108/110 Europe +/−; 203/204 Constitutionalism +/−; 406/407 Protectionism +/−; 504/505 Welfare State Expansion/Limitation; 506/507 Education Expansion/Limitation; 601/602 National Way of Life +/−; 603/604 Traditional Morality +/−; 607/608 Multiculturalism +/−; 701/702 Labour Groups +/−)
- Several categories with **explicit exclusion criteria** in their definitions that reference other specific categories. Examples directly visible in the codebook:
  - **504 Welfare State Expansion** — "*This category excludes education*" (which is 506/507)
  - **506 Education Expansion** — "*This excludes technical training which is coded under 411*"
  - **411 Technology and Infrastructure** — "Need for training and research within the economy (*This does not imply education in general (see category 506)*)"
  - **705 Underprivileged Minority Groups** — "Only includes favourable statements that cannot be classified in other categories (e.g. 503, 504, 604, 607 etc.)"
  - **706 Non-economic Demographic Groups** — "only if these do not fall under other categories (e.g. 503 or 504)"
  - **601_2 / 602_2 immigration codes** — explicit cross-references to 607_1/608_1 distinguishing "new immigrants" vs. "immigrants already in the country"
- Categories with **lexical-trigger risk** — where the surface label contains a high-frequency content word likely to appear in many quasi-sentences regardless of true category. Candidates: 411 (technology/infrastructure), 501 (environment), 503 (equality), 504 (welfare/health/care), 506 (education), 605 (law/order/police), 701 (labour/workers/unions)
- "Catch-all" or generic categories that absorb errors: 408 Economic Goals, 303 Gov-Admin Efficiency, 305 Political Authority, 705 Minority Groups, 706 Non-economic Demographic Groups

### The taxonomy (5 candidate types, ordered roughly by ease of detection)

**E1: Cross-Domain Error**
- *Definition:* True category is in domain X, predicted category is in domain Y ≠ X.
- *Detection:* Fully automated. Lookup from confusion matrix + domain mapping.
- *Why it matters:* Most consequential for domain-level salience measures and any measure that aggregates within domains.
- *Predictions:* Should drop sharply in Condition 4 (hierarchical) by design. Should also drop somewhat from Condition 1 → 2 if exclusion criteria in the full codebook are doing work. Cross-domain errors that survive in C4 indicate Stage 1 (domain selection) failures.

**E2: Valence Flip**
- *Definition:* True and predicted categories form a documented valence pair within the same domain, with opposite signs (e.g., true = 504 Welfare +, predicted = 505 Welfare −).
- *Detection:* Fully automated. Lookup against a pre-specified list of valence pairs.
- *Why it matters:* Catastrophic for RILE and any directional measure. A welfare-positive sentence misclassified as welfare-negative doesn't just lose information — it pushes the estimate in the wrong direction.
- *Predictions:* Should *not* substantially improve under hierarchical prompting (C4) because both categories live in the same domain. Should improve with few-shot examples (C3 vs. C2) because examples show how to read directionality. If C4 doesn't help here but C3 does, that's an important finding for when to use which strategy.

**E3: Exclusion-Criterion Violation**
- *Definition:* Predicted category has explicit exclusion criteria in its codebook entry that the true category violates (or vice versa). The canonical case: a sentence about education funding classified as 504 Welfare State Expansion despite 504's explicit "excludes education" criterion. Halterman & Keith (2026) flagged this exact example.
- *Detection:* Semi-automated. Requires a pre-built lookup table of categories with exclusion criteria and which other categories they exclude. Buildable from the codebook in a few hours — see the list above as a starting point. The detection then is: "if predicted = X and X has an exclusion criterion against Y, and true = Y, flag as E3."
- *Why it matters:* These are the errors that most directly indicate the model is ignoring codebook content. They're the most theoretically interesting because they distinguish "the model used shortcuts" from "the model misjudged a hard case."
- *Predictions:* Should drop substantially from C1 → C2 (codebook becomes visible). May not drop further from C2 → C3 or C3 → C4. This is the cleanest test of whether providing the codebook actually causes models to attend to it.

**E4: Lexical-Trigger Pull**
- *Definition:* The quasi-sentence contains surface lexical content matching the predicted category's label or definition, but the true category is something else (often a more specific or specialized category that requires reading beyond surface words).
- *Detection:* Semi-automated, and this is the trickiest type to operationalize. Possible approach: for each predicted category, define a small set of "trigger tokens" derived from the category label and definition. Flag an error as E4 if (a) the predicted category is wrong AND (b) the sentence contains trigger tokens for the predicted category. This is imperfect — trigger tokens may legitimately appear in correctly-classified sentences too. **This is the type that most needs a development set to refine.**
- *Why it matters:* This is the shortcut-learning hypothesis made operational. Halterman & Keith argued models rely on lexical overlap; E4 quantifies how often that happens and which conditions reduce it.
- *Predictions:* Should drop from C1 → C2 if codebook engagement increases, but may persist even with full codebook because the shortcut is at the level of attention rather than information.

**E5: Catch-All Absorption**
- *Definition:* True category is a specific code; predicted is a documented catch-all (000 uncoded, 408 Economic Goals, 303 Gov-Admin Efficiency, 305 Political Authority, 705/706 generic groups). The error pattern is "model defaults to vague category when uncertain."
- *Detection:* Fully automated. Lookup against pre-specified catch-all list.
- *Why it matters:* Catch-all absorption distorts salience-by-category (specific categories appear less salient than they are) but is less harmful for RILE than valence flips because catch-alls are usually not on the RILE scale.
- *Predictions:* May *increase* under hierarchical prompting (C4) if Stage 2 within-domain pressure pushes uncertain decisions into the domain's catch-all. Worth watching.

### Notes on the taxonomy as a whole

- Some errors will fall into more than one type (e.g., an education-funding sentence labeled as welfare is both E3 and arguably E4). The taxonomy needs a priority order or a "flag all applicable" rule. Suggest "flag all applicable" for analysis; report each type's prevalence independently.
- Some errors won't fall into any of E1–E5. Those are residual "honest confusions" — semantically related categories where the boundary is genuinely hard. Report the residual rate; it's a useful baseline.
- The taxonomy is *codebook-derived*, not *model-derived*. This is a feature: it means any LLM, any prompting strategy, any future model can be evaluated against the same taxonomy. Other codebooks (legal, medical, social science codebooks more generally) could be analyzed with analogous taxonomies built from their own structural properties.

### What the development set / pilot is for

The pilot is mostly about E4 (lexical-trigger pull). Specifically:
- Run one model under one condition (probably the medium-size model under C2) on ~200 dev quasi-sentences
- Compute initial error labels using the taxonomy
- Manually review a sample of E4 flags and non-flags to refine trigger token lists and check whether the detection rule is over- or under-flagging
- Iterate the trigger token definitions until labels feel right
- Lock the definitions before running the main experiments

The dev set is also a sanity check for E3 — verify the exclusion-criterion lookup table catches the cases it should and doesn't fire on cases it shouldn't.

E1, E2, and E5 are mechanical and don't need a pilot.

---

## Part 3: Downstream measurement mapping — needs more research

This is the section I want to flag as **not yet ready to commit**. Writing the mapping requires understanding the Manifesto-derived measures well enough to specify exactly which error types corrupt which measures and how much. Right now we have intuitions, not a defensible mapping.

### What we know (or think we know)

- **RILE (Right-Left scale, Laver & Budge 1992):** Sum of percentages of categories coded "right" minus sum of categories coded "left." The right and left sets are fixed (13 categories each, drawn from across multiple domains). For RILE specifically:
  - Valence flips (E2) between right-and-left categories are catastrophic — they move estimates in the wrong direction
  - Cross-domain errors (E1) that land outside the RILE set don't affect RILE
  - Cross-domain errors that move a sentence from a RILE-included category to a RILE-excluded category attenuate but don't reverse the signal
  - Catch-all absorption (E5) into 408, 303, 305 mostly removes sentences from the RILE numerator/denominator
  
- **Domain-level salience (proportion of manifesto devoted to a domain):** All seven domain proportions sum to 1. Cross-domain errors (E1) move probability mass between domains and directly distort these proportions. Within-domain errors (E2, E5 within a domain, E3 within a domain) don't affect domain salience.

- **Category-level salience** (proportion devoted to specific categories like 501 environment): Affected by every error type that moves probability mass away from or toward the focal category.

### What we don't know well enough yet

- Whether there are other Manifesto-derived measures that would be more diagnostic. There's a literature on alternatives to RILE (e.g., Lowe et al.'s logit scales, issue-specific scales for immigration/welfare/economy). I should read this before committing.
- The exact composition of the RILE right and left sets and whether they map cleanly onto valence pairs. From memory, RILE includes some valence pairs (e.g., 504/505 welfare is split) but not all. I need to actually look up the canonical RILE definition rather than reconstruct it.
- Whether to use a single downstream measure (RILE) as the headline, or report against multiple measures (RILE + domain salience for 2 high-volume domains + one issue-specific scale).
- How to think about variance across manifestos. The aggregate distortion question can be asked at the level of (a) a single manifesto's RILE estimate, (b) the distribution of RILE across manifestos, or (c) the rank ordering of manifestos. These are different statistical questions.

### Suggested next step before committing the mapping

A focused reading session — maybe one evening — going through:
1. Volkens et al. or Budge et al. for the canonical RILE formula and right/left category sets
2. Lowe et al. (2011) on logit-based alternatives
3. One paper that critically discusses RILE's limitations
4. Egami et al. 2023 to refresh on what they do about noisy LLM labels in downstream estimation

Outcome: a one-page document mapping each error type (E1–E5) to its predicted effect on each chosen downstream measure, with a simple worked example for at least one measure (e.g., "here's what one valence flip in welfare does to a manifesto's RILE estimate if welfare salience is 10%").

Once that document exists, Section 4.5 of the main paper writes itself.

### A note on scope

It's tempting to bring in Egami et al. 2023's downstream bias correction methods as part of the paper. **Don't.** That's a different paper. This paper's contribution to the downstream question is *diagnostic* — showing how different error types map onto measure distortion. Egami et al.'s correction methods are a downstream user's tool, not part of this paper's argument. Cite them as the natural next step.

---

## Part 4: Loose ends and open questions to revisit

- **Should the four prompting conditions stay at four?** A leaner version drops Condition 1 (label-only) since it's well-established as broken and doesn't differentiate any specific error type from the others in interesting ways. Three conditions = Full codebook flat, Few-shot codebook flat, Few-shot codebook hierarchical. Cleaner story, same key contrast (C3 vs. C4 = same information, different structure). But losing C1 means losing the baseline that shows "label-only fails" — which is rhetorically useful even if it's not surprising. Tentative decision: keep four. Revisit if compute is tight.

- **Few-shot example selection.** Stratified random with a fixed seed for the main run; report variance across 3 seeds as robustness. Don't manipulate example selection — flag as future work per Liu & Shi (2024). This is the right scope discipline.

- **Reasoning models (DeepSeek-R1, Qwen3 thinking, etc.).** Decision point. Including them changes the paper's claim from "prompting structure matters" to "external scaffolding helps even when models can do implicit decomposition." More interesting but adds scope. Tentative: exclude from main analysis, include one reasoning model as an exploratory comparison in an appendix. Avoids scope creep while keeping the option to comment.

- **142 vs. 56 categories.** Stay at 56. Documented decision. Future work extension.

- **Time budget.** This is the constraint everything else has to fit inside. The user said "slow." The temperature paper took two months and produced burnout. If this paper takes 6–9 months at a sustainable pace, what does that mean for scope? Probably: do the taxonomy work and downstream mapping over 4–6 weeks of evening sessions (no compute needed), then evaluate whether to commit to the experiments based on how the conceptual work feels. Treat the conceptual phase as the decision point, not a sunk cost.
