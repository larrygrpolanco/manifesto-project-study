# Visual Guide: What These Charts Are Showing (and Why It Matters)

All charts live in `reports/visuals/`. Open them in order — they build on each other.

---

## Chart 1 — The Human Ambiguity Landscape (`01_human_landscape.png`)

**What you're looking at:** Every sentence (179 total) sorted from easiest to hardest,
based on how much human experts disagreed.

The height of each bar = **1 − modal share** — the fraction of expert coders who did NOT
pick the most popular code. A tall bar means "the experts split their votes across many
different codes."

**Colors:**

- 🟢 Green = high agreement (barely any expert disagreement)
- 🟡 Yellow = mid-split (moderate disagreement)
- 🔴 Red = high-split (no majority code — the experts are deeply divided)

**Why this matters:** This is the "human ceiling." It answers the foundational question:
_how noisy is this task even for trained humans?_ 72 out of 179 sentences have no majority
code. Fleiss's κ ≈ 0.35. The "gold standard" is itself one draw from a distribution. Any
model evaluation that compares to a single gold label is scoring irreducible task ambiguity
as "error."

**Things to notice:**

- The right side of the chart is dramatically taller than the left — there are genuinely
  easy sentences and genuinely hard ones.
- GB-056 ("Socialist Britain is not nationalization…") gets near-unanimous agreement from
  all 32 coders. GB-033 ("civil war in British industry…") scatters across 15 different
  codes.
- This variation is the referee we use throughout: every claim compares model behavior to
  _this_ per-sentence human disagreement.

---

## Chart 2 — The Pin vs. The Split (`02_underdispersion.png`)

**What you're looking at:** Each dot is one of the 30 pilot sentences. The x-axis is how
much _humans_ disagreed on it. The y-axis is how much a single _model_ wavers across 10
re-runs of the same sentence.

The dashed line is y=x — if models and humans had the same level of disagreement, all dots
would sit on that line.

**What you should see:** Nearly every dot falls well _below_ the line. Models pin an answer
far more consistently than the experts do. The red dots (hard sentences) are particularly
far below — the compression is worst where the task is hardest.

**Key numbers:**

- Model/human spread ratio: **0.26** (easy), **0.50** (mid), **0.39** (hard)
- NZ-006 is the extreme case: humans split across 6 codes with 1−modal = 0.50, while 13 of
  14 model configs unanimously said "408" with 1−modal ≈ 0.01.

**Why this matters:** This is under-dispersion — each model behaves as if the task is far
more certain than the expert distribution says it is. The model doesn't "flip a coin" on an
ambiguous sentence; it slams down a single answer. This is the first leg of the argument.

---

## Chart 3 — Within vs. Between Model Spread (`03_within_vs_between.png`)

**What you're looking at:** Same 30 pilot sentences. For each sentence, two numbers:

- 🔴 Red dot = **within-model** spread: how much _one_ model wavers across its 10 re-runs
  (same as Chart 2's y-axis)
- 🟣 Purple dot = **between-model** spread: how much _different_ models disagree with each
  other on the same sentence

The gray line connecting them shows the gap.

**What you should see:** On the right side of the chart (the hardest sentences), the purple
dots are consistently _higher_ than the red dots. Each individual model pins fairly hard
(red is low), but different models pin on _different codes_ (purple is high).

- GB-016: within = 0.42, between = **0.71**. Each model is internally confident, but
  collectively they're all over the place — the pooled modal code (303) was a code _no
  human chose_.

**Why this matters:** This is the "individually confident, collectively incoherent" finding.
It directly contradicts the idea that you can pool multiple models and trust the consensus.
When models disagree, it's not because the sentence is hard in a way they're grappling with
— they're each pinning confidently on contradictory answers.

---

## Chart 4 — The Correlation Trap (`04_correlation_trap.png`)

**What you're looking at:** Two scatterplots side by side, same data, different subsets.

- **Left panel:** ALL 30 sentences. Human disagreement vs. model disagreement. The
  trendline slopes up — looks like models track human difficulty! r ≈ 0.46.
- **Right panel:** Same thing, but we've removed the 10 easy sentences. The green dots are
  still shown, faded, so you can see what was removed. Now the trendline is almost flat.
  r ≈ **0.19**.

**What you should see:** The left panel's correlation is almost entirely driven by the easy
anchor — sentences that are trivially easy for both humans and models. Once you focus on the
range that actually matters (sentences that are ambiguous), model disagreement tells you
almost nothing about human disagreement.

**Why this matters:** This is the most important methodological point in the paper. A naive
analysis would report r ≈ 0.46 and conclude "models track difficulty — they're doing fine."
The decomposition shows the signal collapses exactly where it would be useful. Anyone
evaluating LLMs as coders needs to report correlations _by difficulty bucket_, not just the
pooled number.

---

## Chart 5 — The 2×2 Danger Grid (`05_2x2_grid.png`)

**What you're looking at:** A 2×2 table crossing human (dis)agreement with model
(dis)agreement. Each cell shows the number of pilot sentences that fell into it.

**The four cells:**

| | Humans agree | Humans split |
|---|---|---|
| **Models agree** | 🟢 Construct is real — both humans and models are clear. n=10 | 🔴 False consensus — models agree on an answer experts didn't. Pilot: n=1 (RARE) |
| **Models split** | 🟡 Models add noise — humans are clear but models fight. n=6 | 🔴 Honest difficulty OR alien scatter. Pilot: n=13 (POPULATED) |

**What you should see:** The original narrative (the "manufactured consensus" / false
consensus cell) is nearly empty. The populated danger cell is the bottom-right — both humans
AND models split, but for different reasons. The models' split doesn't recover the humans'
difficulty.

**Why this matters:** This reframes the problem. The worry isn't that models all agree on
the wrong answer (too rare to be the headline). The worry is that models are confidently
incoherent with each other on the hardest sentences — and there's no signal in that for the
practitioner.

---

## Chart 6 — Under-Dispersion by Bucket (`06_underdispersion_buckets.png`)

**What you're looking at:** Grouped bars comparing human vs. model spread across three
difficulty buckets. The red annotation above each pair is the ratio (model/human).

**Key pattern:** The blue bars (human) grow steeply as difficulty increases. The red bars
(model) grow much more slowly. The ratio tells the story: models compress the variation to
¼–½ of what humans show.

**Why this matters:** This is the cleanest single chart for the under-dispersion result. It
shows at a glance that the gap between human and model behavior is systematic and grows with
task difficulty.

---

## Chart 7 — Exemplar Receipts (`07_exemplar_NZ_006.png`, `07_exemplar_GB_033.png`)

**What you're looking at:** Two full "receipts" for the exemplar sentences. Each receipt
shows:

1. **Top:** The actual sentence text (what the experts and models were coding)
2. **Left bars (blue):** The human expert distribution — how 23–32 trained coders split
   their votes across specific CMP codes
3. **Right bars (red):** The model distribution — how 14 model configs × 10 runs split
4. **Bottom (yellow box):** The interpretive insight — what failure mode this exemplifies

**NZ-006 — "restoring New Zealand's shattered economy":**

- Humans split across 6 codes (408/404/305/414/412/303) with no majority
- Models: near-unanimous 408 (138/140 runs). Only ONE run said 414.
- This is **specificity error** — the model latches onto the literal economic policy
  content (408) and ignores the policy-instrument frame that licensed 404 and 305.

**GB-033 — "civil war in British industry":**

- Humans scatter across 15 codes (max 5/32 = 15%)
- Model pooled modal = **702** (labor groups: positive) — a code only **1 of 32 humans
  chose**
- Individual model configs: claude-haiku-4.5 pins 100% on 702, gemma-4-26b pins 100% on
  410, deepseek-v4-pro splits 606/408
- This is **alien error** — the models collectively settle on a code outside the human
  support set, and different models pick different alien codes.

**Why this matters:** These receipts make the statistics real. The reader can see the
actual sentence, see the expert votes, see the model outputs, and understand _why_ the gap
exists. This is what the PITCH_PLAN calls "comprehension tools" — if you can narrate three
sentences, you understand the whole thing.

---

## Chart 8 — Three Sentences, Three Failure Modes (`08_sentence_cards.png`)

**What you're looking at:** A compact side-by-side comparison of all three exemplar
sentences (NZ-006, GB-033, GB-016). For each:

- 🔵 Human experts bar
- 🔴 Model (within) bar — one model's self-consistency
- 🟣 Models (between) bar — cross-model disagreement

**NZ-006 pattern:** Human high, model near zero, between near zero → **pin on consensus**
**GB-033 pattern:** Human very high, model moderate, between very high → **collective incoherence + alien**
**GB-016 pattern:** Human high, model moderate, between very high → **alien error** (pooled modal = code no human chose)

**Why this matters:** Three different sentences, three different failure modes — but all
show the same structure: model disagreement does not map to human disagreement in any clean
way. This is the typology that becomes quantifiable at full scale.

---

## Chart 9 — The Big Summary (`09_big_summary.png`)

**What you're looking at:** A single infographic poster that synthesizes everything:

- **Three big numbers:** 72/179 sentences with no majority code, 0.26–0.50× under-dispersion
  ratio, r: 0.46→0.19 correlation collapse
- **Three legs:** Under-dispersion, collective incoherence, no recovery of difficulty
- **Bottom-line implication:** Neither single-model confidence nor multi-model voting is a
  safe validity check for genuinely ambiguous coding. The 2×2 grid is a diagnostic template
  anyone can apply.

This is designed as the one thing to show a collaborator or drop into a slide deck. It
doesn't replace the detailed charts above, but it gives someone the entire story in one
glance.

---

## How to read these together (the narrative arc)

1. **Start with Chart 1** — establish that the task is genuinely ambiguous even for experts.
   This is the baseline. The "right answer" is a distribution, not a point.

2. **Then Chart 6** — show that models don't reproduce that distribution. They compress it
   sharply. Under-dispersion is the core quantitative finding.

3. **Chart 2 makes that personal** — you can see individual sentences, including the extreme
   ones where models pile onto one answer while experts split six ways.

4. **Chart 3 adds the twist** — models don't all compress the same way. They pin on
   _different_ answers. So you get collective incoherence: each model is confident, but
   together they're a mess.

5. **Chart 4 is the methodological gotcha** — the naive correlation looks good, but it's an
   artifact. This is why every analysis in this space must decompose by difficulty.

6. **Chart 5 frames it** — the 2×2 shows the field isn't what we feared (false consensus is
   rare) but is worse than the naive hope (collective incoherence is common).

7. **Charts 7 and 8 ground it** — the actual sentences, the actual codes, the actual
   receipts. This is where a reader goes from "I see the numbers" to "I understand why."

---

## What these charts are NOT showing (yet — needs the full collection)

- **The full 179-sentence model data** (pilot only covers 30 sentences, n=14 configs)
- **The RQ2 geometry** — human-shaped vs. alien confusion, which needs the code-neighborhood
  definition from `categories.json` and the full collection
- **Between-model attribute clustering** (RQ-A) — which requires the full 15-model roster
- **The per-category breakdown** — which categories produce the most alien errors, etc.

These are the "play, then polish" charts the PITCH_PLAN's Step 4 describes. The ones above
are the comprehension-first versions — designed to make the patterns visible and discussable.
