# Pilot-3 — task ambiguity as the denominator: do LLMs fail where humans disagree?

A self-contained pilot that pivots the question behind [`../pilot-1`](../pilot-1) and
[`../pilot-2`](../pilot-2). See also [`../docs/error_as_spine.md`](../docs/error_as_spine.md)
and [`../docs/messy-draft.txt`](../docs/messy-draft.txt).

> **Status:** planning / refinement. No runs yet. The design below is a candidate —
> the point of writing it now is to make the refinement concrete. Sections marked
> **OPEN** are the decisions we still need to make.

## The turn

Pilots 1–2 chased the field's reflex: **accuracy**. Both found that the levers we pull
(prompt structure, document context) move the *rate* of errors a little but barely
touch their *structure* — and the dominant error type (cross-domain, ~65% of all
errors) is sticky across every condition and every model.

Accuracy treats **every disagreement with the gold label as a model failure**. But the
Manifesto scheme is a task where *trained human coders agree only ~50% of the time at
the code level* (Mikhaylov et al. 2012). So a large share of what we score as "LLM
error" may not be model deficiency at all — it may be **irreducible task ambiguity**:
category boundaries that even expert humans cross. If that's true, the right question
isn't "how close to 100% is the model" but **"how close to the human ceiling is it, and
does it fail on the same things humans find hard?"**

**Central question.** *Does the structure of LLM error align with the structure of
human coder disagreement?* Two outcomes, both publishable, decided in advance:

- **Aligned** → LLM errors concentrate where humans disagree. The "low accuracy" is
  largely a property of the *instrument* (the codebook's porous boundaries), not the
  model. This is a measurement-validity finding, and it ages independently of which
  model is current. It reframes the whole codebook-LLM literature's accuracy obsession.
- **Misaligned** → LLMs fail in places humans agree. That residual is genuine model
  defect, and it's the part prompting/fine-tuning should target. Equally useful, and it
  tells you *where* to spend effort.

Either way, the dependent variable stops being accuracy and becomes **error structure
and its alignment with human disagreement.** That's the thread worth scaling.

## The data we already have

The replication archive for Mikhaylov, Laver & Benoit (2012) is in
[`../data/codebook/coder_reliability/`](../data/codebook/coder_reliability) — the raw
human coding experiment, **full 56-category scheme, English**:

| document | coders | sentences | (coder→gold) pairs |
|---|---:|---:|---:|
| Britain (`codes.log` + `master-codersGB.txt`)    | 32 | 107 | ~3,400 |
| New Zealand (`codesNZ.log` + `master-codersNZ.txt`) | 23 | 72  | ~1,650 |

Each `*.log` row is one coder: columns 1–8 are metadata (ip, date, time, id, name,
email, institution, experience), **columns 9+ are the code that coder gave to
quasi-sentence 1, 2, 3, …** in fixed order. The `master-*.txt` files hold the gold
("MASTER") code for the same sentence sequence. `CMP_reliability_replication.R` is the
original recipe (incl. which low-quality coders the authors dropped).

**The crown jewel:** because ~30/~23 coders coded *the same* 179 sentences, every
sentence has a **distribution of human codes** → a measurable **per-sentence ambiguity
score** (entropy / disagreement), not just an aggregate reliability number.

## Two phases

### Phase A — structural, no API, data in hand (answers "is this real?")

Build, from the reliability archive alone:

1. **Human confusion matrix** (coder→gold) at 56-category and 7-domain levels.
2. **Human inter-coder agreement** (coder→coder): pairwise agreement and Krippendorff's
   α overall and per category — the achievable ceiling per category.
3. **Per-sentence human ambiguity**: entropy / modal-share of the ~30 human codes on
   each of the 179 sentences.
4. **Per-category reliability ranking**: which categories humans themselves can't
   apply consistently, and which cells absorb the disagreement (do humans also dump
   into 408 / 305 / 606?).

Then compare the *geometry* of the human confusion matrix to the **LLM confusion
matrices we already have** from pilots 1–2 (different sentences, so this is a
distributional comparison, not item-level):

- cross-domain share of off-diagonal mass — human vs LLM (is the human number also ~65%?)
- correlation of per-category recall: do LLMs and humans struggle on the same categories?
- do the heavy off-diagonal cells coincide (cosine / correlation of off-diagonal mass)?

If the geometries already look alike, the avenue is real and we commit to Phase B.

### Phase B — matched, item-level (the strong test; needs the sentence texts)

Run the same models/conditions over **the exact 179 GB/NZ sentences** the humans coded,
giving a paired design:

- **Item-level alignment:** is the LLM more likely to err on high-human-entropy
  sentences? (logit of LLM-error on human-disagreement, per item.)
- **Disagreement vs disagreement:** does *cross-model* LLM disagreement track
  *cross-coder* human disagreement on the same sentence? (Do machines and humans find
  the same sentences hard?)
- **Human-ceiling-relative scoring:** report LLM accuracy *against the human agreement
  rate per category*, not against 100%.

This requires locating the 179 sentence **texts**, which the logs don't contain — see
Data wrangling below.

## Data wrangling (the "take a while" part)

- The logs give codes, not text, and don't name the manifesto/election. We need to
  identify **which** British and NZ manifestos these are (MLB 2012 used specific test
  documents) and pull their quasi-sentence text **in coding order** to align with the
  107/72 columns.
- The full corpus CSV is **~1.8M rows** — do **not** load it whole. Filter to the
  candidate country/party/date first, then match on sentence order/count (107 and 72
  are strong fingerprints). Confirm alignment by spot-checking a few sentences against
  their gold codes.
- **OPEN:** confirm the exact source documents before any extraction. Until matched,
  Phase A stands on its own.

## Metrics (candidate — needs refinement)

- **Ambiguity score per sentence:** normalized Shannon entropy of human codes, and/or
  (1 − modal share). **OPEN:** which, and how to handle the `000`/uncoded codes.
- **Reference for "truth":** the `master` gold is itself one authority's coding, *not*
  ground truth. **OPEN:** treat gold as the reference (accuracy framing), or treat
  coder-vs-coder agreement as the ambiguity measure and drop the privileged gold? Lean:
  report both — gold-relative for comparability with the literature, coder-consensus for
  the honest ambiguity story.
- **Matrix comparison:** per-category recall correlation (human vs LLM); off-diagonal
  cosine; cross-domain off-diagonal share.
- **Alignment (Phase B):** item-level error ~ human entropy; model-disagreement ~
  coder-disagreement.

## Caveats baked in

- **Two English manifestos, one era.** Small and unrepresentative — fine for a pilot
  that asks whether the *relationship* exists, not to estimate its size for the field.
- **Gold is not ground truth.** It's one expert's codes; "accuracy against gold"
  inherits gold's own errors. This is exactly why the human-disagreement framing is the
  point, not a nuisance.
- **Coder pool quality.** The archive mixes trained coders and trainees; MLB dropped
  some. **OPEN:** compute everything both with all coders (a realistic "crowd" ceiling)
  and with their trained subset (the expert ceiling).
- **Phase A is unmatched** (different sentences than pilots 1–2). It can show the
  geometries rhyme; only Phase B can show item-level alignment.

## Planned layout

```
pilot-3/
  README.md              # this plan
  config.py              # models/conditions reused from pilot-2; ambiguity + matching params
  data/
    human_reliability/   # copied from ../data/codebook/coder_reliability (self-contained)
    codebook.csv         # 56-category codebook + domain map (shared with pilot-2)
  src/
    human_matrix.py      # Phase A: parse logs -> human confusion, α, per-sentence entropy
    compare_matrices.py  # Phase A: human-vs-LLM geometry (uses pilot-1/2 confusion outputs)
    match_sentences.py   # Phase B: locate + align the 179 texts from the 1.8M-row corpus
    run_experiment.py    # Phase B: reuse pilot-2 runner over the matched sentences
    evaluate_alignment.py# Phase B: item-level error ~ human disagreement
  reports/               # human reliability profile, geometry comparison, alignment, summary.md
```

## Immediate next step

Build `src/human_matrix.py` (Phase A, step 1–4) and the geometry comparison against the
pilot-1/2 confusion matrices. That's an evening on data already on disk, and it tells us
whether the alignment thread is real **before** we spend any compute or go hunting
through 1.8M rows for sentence texts.
