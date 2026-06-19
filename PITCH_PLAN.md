# PITCH_PLAN

_A living planning doc with two jobs:_

1. **Plan the work to do *before* I pitch** — the bones (clean data), a two-model
   end-to-end run, owning the metrics, visuals, and exemplars.
2. **Hold the pitch itself**, which gets written **last**, once that work is done and I
   can actually stand behind it.

**Operating principle.** The dense `RESEARCH_PLAN.md` was substantially model-driven — it
ran ahead of my own understanding, and a lot of it is over my head precisely because I
never set out to commit to all of it. That's fine; it's a good thinking artifact and I'll
keep it. But **this file is where I take the wheel.** Rule of thumb: I shouldn't put
anything in the pitch I can't explain at a whiteboard in five minutes without notes. The
important choices get made by **me and my collaborator**, not pre-baked here.

The pitch deliberately stays *loose* on the research questions. A peer wants a compelling
asset, an honest hint of a finding, and real open problems — not a finished spec to execute.

---

# Part 1 — The pitch _(skeleton — fill in LAST)_

> Target length: ~2 pages. Lead with the asset and the question; end with what's open.

### Hook _(one paragraph — to write)_
People are starting to let AI models do a job humans used to do by hand: read political
text sentence by sentence and tag each with a category. The usual safety check is
*agreement* — if a model is consistent, or several models agree, the coding "must" be
right. On a genuinely ambiguous task, that check may not hold. I have a rare dataset that
lets me test it directly.

### The asset _(the real reason to collaborate)_
The **same** sentences coded by **23–32 trained expert coders each** — so every sentence
carries a full *distribution* of expert opinion, not just one "gold" answer. This per-item
expert-disagreement signal does not exist anywhere else for a real codebook task. It's the
referee. _(GB: 107 sentences / 32 coders; NZ: 72 sentences / 23 coders.)_

### What the pilot hints _(state small and honest)_
A 30-sentence, 8-model pilot suggests models pin confident answers where experts split, and
disagree with *each other* on hard items — but it's small and I don't fully trust it yet.
The two-model end-to-end run (Part 2) and the full collection are what turn this from a hint
into a finding.

### What I bring / what's open _(questions for a collaborator)_
- The dataset and the framing instinct; a working pipeline (after Part 2).
- **Open:** Is "disagreement-as-broken-signal" the right frame, or something better?
- **Open:** What's the cleanest, most defensible set of metrics? (see Part 2, Step 3)
- **Open:** How much of this should be discourse analysis vs. statistics? _(this is where an
  applied-linguistics / discourse-analysis collaborator reshapes the paper — the current
  plan counts disagreement but doesn't explain it.)_
- **Open:** Does it replicate at scale?

---

# Part 2 — What to do before pitching _(ordered by dependency)_

The point of all of this is twofold: produce **honest, clear, replicable data** that
supports a *cone* of questions (not just one pre-chosen answer), and bring my own
understanding up to where I can lead the project.

## Step 1 — The bones: clean, honest, replicable data _(question-agnostic)_
Get the foundation right *before* worrying about which question we ask. The data should be
honest and clear no matter what we end up looking at.

- **One schema, shared with humans.** Keep the long format
  (`coder_id, manifesto, unit_id, sequence, code`) so model rows and human rows run through
  the *same* entropy/agreement code. This already exists — protect it.
- **Raw cache, regenerable, fail-loud.** One cached file per API call; gitignored raw;
  crash loudly on any unreachable model. No silent gaps.
- **Store everything, clean transparently.** Keep raw model output *including* off-scheme
  text and nulls, so cleaning is visible and auditable — not baked in. (Carry over the one
  known pilot fix: raise the generation token budget above 2048 for reasoning-on models so
  they don't get cut off before emitting a code.)
- **Question-agnostic.** The data layout shouldn't assume RQ1. If we later want a different
  slice, the same files should answer it.

## Step 2 — Run the whole experiment end-to-end with three models
Not for the science yet — to **force the code into place** and get something real to look
at, compare, and share.

- Pick **three clearly different models** (different company/lineage) so "between-model"
  means something even at n=3.
- Run the full pipeline: prompt → collect → cache → parse → into the shared schema →
  metrics → a few charts.
- Deliverable: a small, real dataset I can eyeball and a couple of rough visuals. Three models
  is a toy for between-model spread, but plenty to prove the plumbing and see the shape.

## Step 3 — Own the metrics _(pick 3–5 the reader can understand and apply)_
A good paper has a few solid metrics, not a pile. I need to *understand* each before I can
chart it well. Starting definitions below — the task is to make these mine, sanity-check
them on the two-model data, and keep the 3–5 that survive.

- **Per-sentence entropy** — how scattered the codes are for one sentence. Low = everyone
  lands together; high = all over the place. The core ambiguity measure.
- **Modal share / (1 − modal share)** — what fraction picked the single most common code.
  Simpler and more intuitive than entropy; maybe the more *readable* twin. _(candidate to
  lead with.)_
- **Within-model spread** — how much *one* model wavers across re-runs of the same sentence.
  Its self-consistency.
- **Between-model spread** — how much *different* models disagree with each other on the
  same sentence.
- **Dispersion / under-dispersion** — model spread compared to human spread (e.g. a ratio).
  The "models pin where humans waver" idea, made into a number.

> Goal: 3–5 of these, each one I can define in a sentence and a reader can apply themselves.
> Decide *which* survive on the two-model data, not in the abstract.

## Step 4 — Visualizations _(play, then polish)_
A lot of the confusing parts of this clear up with one good chart — and you can't make a
good chart for a metric you don't understand, so this rides on Step 3.

- One chart per surviving metric, first for comprehension (mine), then for the reader.
- Collect the data somewhere stable first, then experiment freely with views.
- Likely candidates: human vs. model entropy per sentence; within- vs. between-model spread;
  a confusion view (where the codes land). Don't commit to final figures yet — explore.

## Step 5 — Exemplars _(definitely want these)_
Not a full analysis — a handful of concrete sentences that make the pattern real.

- Pick a few sentences spanning easy → hard.
- For each: **how the humans performed** (the distribution, top codes) and **how the
  model(s) performed** (converge? scatter? on a human code or one no human chose?).
- **Say why each was picked and how they connect** — to each other and to the metrics.
- This is also a comprehension tool for *me*: if I can narrate three sentences clearly, I
  understand the whole thing.

---

# Carrying list — for me and my collaborator to decide later
Not settling these now, on purpose.

- The framing: disagreement-as-broken-signal vs. an alternative.
- Final 3–5 metrics.
- How much discourse-analysis depth (the natural place for the applied-linguistics
  collaborator).
- Gold's status — report against gold, gold-free, or both.
- Center of gravity: the recovery-of-difficulty result vs. the geometry/exemplars.
