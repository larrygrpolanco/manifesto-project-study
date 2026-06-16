# Branch: "Does the model know when the question is hard?"

_A candidate reframe of the main research plan. This is a **branch**, not a commitment —
the point is to run a small pilot, get base data, and then decide whether to merge it
into the main plan or set it aside. Nothing here is final._

_Status: design only. No LLM runs yet. Human side (Step 0) is done and validated._

---

## 0. The one thing this branch is about, in plain words

We have something almost nobody else has: for each of 179 manifesto sentences, we know
**exactly how a room full of trained experts split** when they coded it. Not just "the
right answer" — the whole disagreement. Some sentences, all 32 experts agree. Some, they
split 16–16. We know which is which, sentence by sentence.

That lets us ask a question you cannot ask any other way:

> **When a sentence is genuinely a coin-flip for human experts, does the model also
> treat it like a coin-flip — or does it confidently slam down one answer?**

And a companion question:

> **When the model gets one wrong, does it trip on the same things humans trip on,
> or on something weird no human would?**

That's the whole paper, in two sentences a normal person can follow. Everything technical
below is in service of those two questions and nothing else.

---

## 1. What we've decided (taking stock)

These are the things we've actually settled on in conversation. Writing them down so we
stop re-litigating them.

**Decided — the framing.**
- The paper's engine is the **per-sentence human disagreement distribution** — the full
  shape of how experts split, not a single ambiguity number. This is the asset H&K (and
  everyone comparing models to one gold label) structurally cannot use. It is our wedge.
- Two questions carry the paper:
  - **Q1 — "Does the model know it's hard?"** Where experts are split, is the model also
    split (run it many times, does it waver), or does it fake confidence?
  - **Q2 — "Is the model wrong in a human way or an alien way?"** When the model errs,
    are its confusions the same category-pairs humans confuse (e.g. 503↔504), or pairs
    no human would confuse?
- Q1 is the headline (fastest "why I should care"). Q2 is the mechanism underneath it.

**Decided — within/between-model reliability is demoted.**
- Self-consistency and between-model agreement are now a **one-figure control**, not a
  research question. Reason: H&K essentially already did both (their Test IV). We do not
  build narrative on ground someone else has covered.

**Decided — mixed methods, with qualitative exemplars as load-bearing.**
- Every claim here is ultimately about *individual sentences*. The statistics prove the
  pattern holds across all 179; the **close-read exemplars prove it's real and make the
  reader care.** The exemplars are not decoration.
- Our exemplars come with their own receipts: we don't *assert* a sentence is hard, we
  *show* 32 experts already argued about it. That's a rare luxury and we lean on it.
- Open question (not yet decided): exemplars **interleaved** (each claim followed by its
  worked sentence) vs **gathered** (one close-reading section). Leaning interleaved for
  reader-grip, but deferring until we see how rich the close reads actually are.

**Decided — the writing rule.**
- If a smart general reader gets lost, that's our fault, not the idea's. But "simple"
  means *every hard idea earns its difficulty* — not short sentences, and not dumbing
  down. Kill words that add difficulty without adding meaning ("calibration" → "does the
  model know when it's guessing"). Keep difficulty only where the idea genuinely needs it,
  and when it does, walk in through an example.

**Decided — what stays from the old plan.**
- Step 0 human profile (done, validated against MLB to rounding).
- The instruction-parity prompt principle (model gets the same instrument the humans got:
  full 56 + `000`, decision rules, pre-unitised sentences, no answer key).
- `000` kept as a class (primary), reported with/without as robustness.
- Retained subset (17 GB / 12 NZ) as the expert reference (primary), full pool as
  robustness.
- In-context (human parity) as the primary condition for any human-vs-model comparison.

**Parked (kept as open questions until the pilot tells us more).**
- Interleaved vs gathered exemplars (above).
- Whether Q2's confusion-structure comparison survives sparse per-category cells.
- Whether to also pursue "human disagreement as a free difficulty oracle for routing"
  (the practical-payoff idea) — promising, but needs Q1 to land first.
- Center of gravity / final RQ wording — set after we see pilot data, not before.

---

## 2. Why this beats the version we had

Plain version: the old three-act story (within-model → between-model → human) was smooth
*because* the first two acts were familiar — and familiar means H&K already did them. We'd
be telling a satisfying story whose first two-thirds a reviewer has read before, with the
only new part stuck at the end carrying all the weight.

The new spine is novel in **every** act, because every act needs the human *distribution*,
which is the thing nobody else has:
- Q1 (does the model know it's hard) needs the human split per sentence.
- Q2 (human vs alien errors) needs the human *confusion shape* per category.

So we're not competing with H&K on their turf. We're using the one asset they didn't have.

---

## 3. The two questions, stated so we can't drift

**Q1 — Does the model sense the difficulty?**
Take the sentences where experts genuinely split. Run each model on each sentence many
times. Does the model's spread of answers widen on exactly those sentences (it "knows"
it's hard), or does it stay pinned on one code (fake confidence)?
- The honest, gold-free comparison: per-sentence *human spread* vs per-sentence
  *model spread*. No need to declare any answer "correct."
- The danger we expect to find and show: experts split, model pins. That's the invisible
  hard case — run once, you'd never know it was a coin-flip.

**Q2 — Are the model's mistakes human-shaped?**
For each category, humans have a known confusion pattern (when they miss 503, what do they
call it instead?). Build the same confusion pattern for each model. Ask: do models trip on
the *same* category-pairs humans trip on, or on different ones?
- Same pairs → the model has internalized something like the real category geometry.
- Different pairs, *shared across models* → the strongest possible version of "manufactured
  consensus": models agreeing on a confusion no human makes. Shared structure, not construct.

---

## 4. The pilot — purpose and shape

### 4.1 What the pilot is FOR (and not for)

The pilot is **not** trying to answer Q1 or Q2. It's trying to answer:
**"Is this study even runnable, and where are the cliffs?"** Specifically:

1. **Signal-exists check (Q1):** On the sentences where humans are most split, do models
   actually pin to one answer? If even the pilot shows model-spread is flat while
   human-spread varies, Q1 has a pulse. If model-spread just tracks human-spread already,
   that's also informative (and would reshape the paper).
2. **Resolution check (the real feasibility risk):** Can ~N repeated runs per model even
   produce a usable "model spread" to compare against a 32-coder human spread? If 5 runs
   gives garbage resolution, we learn the full run needs more runs-per-model, not more
   models. **This is the most important thing the pilot buys us.**
3. **Confusion-cell check (Q2):** Do the model errors land in enough distinct
   category-pairs to make a confusion comparison meaningful, or are cells hopelessly empty
   at pilot scale? Tells us whether Q2 is a headline or a discussion-section illustration.
4. **Plumbing:** prompt parity actually works; output parses; `000` is usable; logprobs
   collected opportunistically where the provider returns them (≈1 in 4 endpoints — bonus
   only, not relied on).

### 4.2 The pilot grid (small, fully crossed)

Keep it tiny and structured. Massive-but-confounded is the amateur move.

- **Models: 4.** Two companies, two size tiers each (e.g. a small + a mid open-weight from
  two different families). Enough to see whether "model spread" and "confusion shape" look
  model-specific or shared. Not enough to claim anything — by design.
- **Sentences: a purposive ~30, not random.** Three buckets, chosen from Step 0:
  - ~10 **high human-split** sentences (the coin-flips — incl. the 4 balanced L/R ones).
  - ~10 **high human-agreement** sentences (the easy cases — control).
  - ~10 **mid-split** sentences (to see if the relationship is graded, not just hi/lo).
  Purposive because the pilot is a feasibility probe, not an estimate; we want the
  informative items, not a representative sample yet.
- **Context: in-context only** (human parity). Sentence-only is a main-study contrast;
  the pilot doesn't need it.
- **Temperature: 1 only.** We need a *spread* to measure; temp 1 is where spread lives.
  (Temp 0 is a main-study control for the reliability figure; skip it in the pilot.)
- **Runs per (model × sentence): 10.** Enough to see whether a spread exists and to
  eyeball how stable the spread estimate is as we subsample 10→5. That subsampling
  analysis is how we answer the resolution check above.

**Volume:** 4 models × 30 sentences × 10 runs = **1,200 calls.** Trivial cost, fast,
mostly cheap open-weight models. That's the point.

### 4.3 What we compute from the pilot

For each sentence, two spreads side by side:
- **Human spread** (already in hand from Step 0): the expert distribution over codes.
- **Model spread** (new): across the 10 runs, the distribution over codes, per model and
  pooled.

Then three quick looks, matching the three checks:

1. **Q1 pulse:** plot model spread vs human spread across the 30 sentences. Do the
   coin-flip sentences show wide human spread but narrow model spread? Eyeball + a single
   correlation. (Pilot answer is "is there a signal," not "how big.")
2. **Resolution:** recompute model spread using 10 runs, then 5, then 3. How much does the
   per-sentence spread estimate move? This sets runs-per-model for the full study.
3. **Q2 cells:** tally which category-pairs the model errors fall into; compare against the
   human confusion pairs for those same categories. Count non-empty cells. Decide if Q2 is
   a headline or an illustration.

Plus: **pull 2–3 exemplar sentences and actually read them.** Pick one coin-flip where the
model pins, one where model and humans both waver, ideally one alien-confusion case. This
is a dry run of the mixed-methods close reading — does the qualitative layer actually say
something, or does it fall flat? If it sings even at pilot scale, that decides
interleaved-vs-gathered and tells us how much room to give it.

### 4.4 What would change our mind (pre-committed reads)

Honesty guardrail: deciding in advance what each outcome means, so we don't rationalize.

- **Q1 signal present** (human spread varies, model spread stays narrow on hard items)
  → merge the branch; Q1 is the headline. Proceed to scale up (more models, more runs as
  resolution check dictates, both contexts, full 179).
- **Q1 signal absent** (model spread already tracks human spread) → that's a *finding*, not
  a failure: "models are better calibrated to task ambiguity than expected." Reshapes the
  paper toward Q2 and the difficulty-oracle idea. Still mergeable, different headline.
- **Resolution bad at 10 runs** → full study needs deeper per-model sampling; recost before
  committing. Cheaper to learn now than after 45k calls.
- **Q2 cells hopelessly empty** → Q2 demotes to a discussion illustration (worked
  exemplars only), Q1 carries alone. Pre-authorized, not a failure.
- **Exemplar close-reads fall flat** → reconsider whether the mixed-methods selling point
  is real, or whether this is a quant-only paper.

---

## 5. Immediate next steps (in order)

1. **Pick the 4 pilot models** — 2 companies × 2 sizes, open-weight, confirmed reachable on
   OpenRouter. Note which return logprobs (bonus signal).
2. **Pick the ~30 pilot sentences** from Step 0 buckets (10 high-split incl. the 4 balanced,
   10 high-agreement, 10 mid). Freeze the list.
3. **Build the parity prompt** (full 56 + `000`, decision rules, pre-unitised, no key;
   in-context block included). Same instrument the humans got.
4. **Run 1,200 calls** (4 × 30 × 10, temp 1, in-context).
5. **Three checks + 3 exemplar close-reads** (§4.3).
6. **Decide:** merge / reshape / park — using the pre-committed reads in §4.4.

---

## 6. Things we are deliberately NOT deciding yet

- Final RQ wording and which of Q1/Q2 is the formal headline.
- Interleaved vs gathered exemplars.
- Whether the difficulty-oracle (routing) idea becomes a third act.
- Full-study model roster, run counts, temp grid — all set by pilot resolution data.
- Stance toward "LLMs can replace coders" (warning vs recipe) — post-analysis.

The pilot exists precisely so these get decided on data, not vibes.
