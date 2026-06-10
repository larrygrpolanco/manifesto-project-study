# Pilot-2 — document context on the Manifesto coding scheme

A small, self-contained pilot that builds on [`../pilot-1`](../pilot-1) to probe a
sharper question, before committing to the full study (see
[`../docs/error_as_spine.md`](../docs/error_as_spine.md) and
[`../docs/messy-draft.txt`](../docs/messy-draft.txt)).

Pilot-1 manipulated **codebook presentation** (flat vs. by-domain vs. two-call) and
found that prompt *structure* moved accuracy little except for the smallest model.
Pilot-2 changes the question: instead of *how the codebook is shown*, it varies
**how much of the surrounding document the model sees**, and asks whether document
context changes the **structure of errors** — not just their rate. The stance stays
inferential: do the conditions produce *significantly different* behavior, and does
it hold across models?

## Design

**3 conditions.** The codebook block is held constant (the by-domain "pick domain
then category" block from pilot-1's `HIER1`). The **only** thing that changes is the
amount of document context around the target sentence.

| Condition | Context shown around the target sentence |
|---|---|
| `BASE`    | none — the target sentence alone (this is pilot-1's `HIER1`) |
| `WINDOW`  | the ± `WINDOW_RADIUS` (=10) neighbouring quasi-sentences |
| `FULLDOC` | the **entire manifesto** |

- **Context axis:** `BASE` → `WINDOW` → `FULLDOC`. `BASE vs WINDOW` isolates local
  context; `WINDOW vs FULLDOC` isolates document-wide context; `BASE vs FULLDOC` is
  the full effect of handing the model the document.
- In every condition the model assigns exactly **one code to the target sentence**;
  context is rendered as `pos: text` lines (document order) and the target is quoted
  in the question. Because the context block doesn't change with the question, a
  manifesto's `FULLDOC` prefix is identical across its sampled sentences
  (cache-friendly).
- **Label space:** the 56 substantive categories **+ `000`** ("no other category
  applies"). No gold item is `000`, so any `000` prediction scores as wrong but is
  tracked as over-abstention (E5).
- **Models:** 2 models via **OpenRouter** (`config.MODELS`): `google/gemma-4-26b-a4b-it`
  (256k ctx) and `deepseek/deepseek-v4-flash` (1M ctx). Both fit the largest
  manifesto (~78k tokens) in `FULLDOC`.
- **Output:** JSON mode, schema `{"code": ...}`. Compliance = a valid in-scheme code
  was returned.
- **Runs:** temperature 0, single call per (item × condition × model). Prior work
  (Grullon-Polanco 2026) settled that T=0 is the right setting.

## Sampling

The corpus is large (~18k quasi-sentences across **12 manifestos**, 4 parties × 3
elections), so we do **not** score every row. We draw a **stratified random sample
of `N_PER_MANIFESTO` (=50) sentences per manifesto** → **600 target items**,
stratified by **policy domain** with **proportional (largest-remainder) allocation**
so each manifesto's natural domain mix is preserved and small domains aren't dropped
by chance. The draw is fully determined by `SEED`, so it's reproducible and
identical across every model × condition cell. For the `WINDOW`/`FULLDOC` conditions,
each sampled sentence still carries its **whole** manifesto (shared in memory) so the
surrounding context can be reconstructed.

> Switching to **equal** per-domain allocation (to guarantee coverage of rare
> domains) is a one-line change in `dataset.py`. Changing the sample means you must
> `rm -rf results/raw/*` first, since the cache and `predictions.csv` key on item id.

## Layout

```
pilot-2/
  config.py              # the only thing you edit between runs: models, conditions, sampling, params
  requirements.txt
  data/
    manifesto-pilot-dataset_english_dev-train-4x3.csv   # ~18k rows, 12 manifestos
    codebook.csv         # MPDS2020a category codebook (57 main rows)
    valence_pairs.csv    # E2 valence-pair lookup
  src/
    codebook.py          # parse codebook -> the by-domain prompt block (shared by all conditions)
    dataset.py           # group by manifesto, order by pos, seeded stratified sample, attach context
    prompts.py           # message construction per condition (BASE / WINDOW / FULLDOC)
    profile_dataset.py   # standalone profile of the sampled items (no API)
    run_experiment.py    # OpenRouter runner: resumable cache, JSON mode, async
    evaluate.py          # metrics + E1/E2/E5 taxonomy + Cochran's Q / McNemar
  results/
    raw/                 # cached raw API responses, one JSONL per model×condition (gitignored)
    predictions.csv      # tidy parsed predictions, rebuilt from the cache (tracked)
  reports/               # profile, metrics, confusion matrices, stats, summary.md (tracked)
```

## Setup

```bash
cd pilot-2
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# OPENROUTER_API_KEY is read from the repo-root .env automatically,
# or export it: export OPENROUTER_API_KEY=...   # https://openrouter.ai/keys
```

## Run

```bash
# 1. Profile the sampled items (no API needed) -> reports/dataset_profile.md
python src/profile_dataset.py

# 2. (optional) eyeball the exact codebook prompt block -> reports/prompt_blocks_preview.md
python src/codebook.py

# 3. Smoke test: a couple of items, before spending on the full sweep
python src/run_experiment.py --limit 2

# 4. Full sweep — 600 items × 3 conditions × 2 models = 3,600 calls
#    (resumable — safe to interrupt and rerun; FULLDOC's big prompts dominate runtime)
python src/run_experiment.py

# 5. Evaluate -> reports/metrics.csv, stats_*.csv, confusion/, summary.md
python src/evaluate.py
```

Subset a run with `--models deepseek/deepseek-v4-flash` and/or
`--conditions BASE WINDOW`. The cache means reruns only call the API for missing
(model, condition, item) cells.

## What you get

- **`reports/dataset_profile.md`** — category/domain distribution of the 600 sampled
  items, absent categories, valence-pair observability, catch-all share, length,
  power note.
- **`reports/metrics.csv`** — per model×condition: compliance, accuracy,
  accuracy|compliant, domain accuracy, weighted F1, and error-taxonomy rates.
- **Error taxonomy (mechanical):** `E1` cross-domain, `E2` valence flip,
  `E5` catch-all absorption, plus residual. Errors are flagged for *all* applicable
  types (an error can be both E1 and E5).
- **`reports/stats_cochran.csv`** — omnibus test that the 3 conditions differ
  (per model).
- **`reports/stats_mcnemar.csv`** — Holm-corrected pairwise tests for the comparisons
  in `config.COMPARISONS`.
- **`reports/stats_direction_consistency.csv`** — whether an effect points the same
  way across models (a one-model result is not an effect).

## Caveats baked into the design

- **`FULLDOC` confounds context with prompt length.** A `BASE`→`FULLDOC` difference
  could be "the model used document context" *or* "a ~40–78k-token prompt degrades
  attention." `WINDOW` is the control: local context without the length blowup.
- **Stratification is a researcher degree-of-freedom** (proportional vs. equal
  allocation; see Sampling above). Documented and seeded so it's auditable.
- Category **presentation order** is fixed (codebook order). Order-sensitivity
  (Halterman & Keith 2026) is held constant here, out of scope.
- `E3` (exclusion-criterion violations) and `E4` (lexical-trigger pull) are **not**
  computed — they need a refined lookup/trigger-token pass and belong to a later,
  taxonomy-focused pilot.
- Two models is enough to check **direction consistency** but not to characterize a
  model-size interaction; that's for the full study.
