# Pilot-1 — zero-shot prompting on the Manifesto coding scheme

A small, self-contained pilot to understand **the dataset** and **the study design**
before committing to the full study (see [`../docs/error_as_spine.md`](../docs/error_as_spine.md)
and [`../docs/messy-draft.txt`](../docs/messy-draft.txt)).

It is **not** the full study. No few-shot, no fine-tuning, no downstream-measure
analysis. The question here is narrow and inferential: **do different zero-shot
prompting conditions produce *significantly* different classification behavior**,
and does that hold across models? The goal is to learn the design, not to chase
maximum accuracy.

## Design

**4 conditions.** Each comparison changes exactly one thing.

| Condition | Information shown | Structure |
|---|---|---|
| `LABELS` | code + title only | flat, all 57 at once |
| `FULL`   | full codebook entry (definition + exclusions) | flat, all 57 at once |
| `HIER1`  | full codebook | single call, entries **grouped by domain**, "pick domain then category" |
| `HIER2`  | full codebook | **two calls**: pick domain → pick category within that domain |

- **Information axis:** `LABELS` vs `FULL`.
- **Structure axis (information held at full):** `FULL` vs `HIER1` vs `HIER2`.
- **Label space:** the 56 substantive categories **+ `000`** ("no other category
  applies"). No gold item is `000`, so any `000` prediction scores as wrong but is
  tracked as over-abstention.
- **Models:** 5 open-weight models via the **Groq** API (`config.MODELS`).
- **Output:** JSON mode, schema `{"code": ...}` (extensible to add a `reasoning`
  field for a future condition). Compliance = a valid in-scheme code was returned.
- **Runs:** temperature 0, single pass per (item × condition × model). Prior work
  (Grullon-Polanco 2026) settled that T=0 is the right setting.

## Layout

```
pilot-1/
  config.py              # the only thing you edit between runs: input, models, params
  requirements.txt
  data/
    dev_set.csv          # the sample to score (300 quasi-sentences, 12 manifestos)
    codebook.csv         # MPDS2020a category codebook (57 main rows)
    valence_pairs.csv    # E2 valence-pair lookup
  src/
    codebook.py          # parse codebook -> per-condition prompt blocks
    dataset.py           # load any text+code CSV into items (schema-agnostic)
    prompts.py           # message construction per condition
    profile_dataset.py   # standalone dataset profile (no API)
    run_experiment.py    # Groq runner: resumable cache, JSON mode, async
    evaluate.py          # metrics + E1/E2/E5 taxonomy + Cochran's Q / McNemar
  results/
    raw/                 # cached raw API responses, one JSONL per model×condition (gitignored)
    predictions.csv      # tidy parsed predictions, rebuilt from the cache (tracked)
  reports/               # profile, metrics, confusion matrices, stats, summary.md (tracked)
```

## Setup

```bash
cd pilot-1
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export GROQ_API_KEY=...        # https://console.groq.com/keys
```

## Run

```bash
# 1. Profile the data (no API needed) -> reports/dataset_profile.md
python src/profile_dataset.py

# 2. (optional) eyeball the exact prompt blocks -> reports/prompt_blocks_preview.md
python src/codebook.py

# 3. Smoke test: 5 items only, before spending on the full sweep
python src/run_experiment.py --limit 5

# 4. Full sweep (resumable — safe to interrupt and rerun)
python src/run_experiment.py

# 5. Evaluate -> reports/metrics.csv, stats_*.csv, confusion/, summary.md
python src/evaluate.py
```

Subset a run with `--models llama-3.1-8b-instant` and/or
`--conditions LABELS FULL`. The cache means reruns only call the API for missing
(model, condition, item) cells.

## Running a different / larger sample

The pipeline is sample-agnostic. To score another CSV:

```bash
python src/profile_dataset.py --input path/to/sample.csv
python src/run_experiment.py  --input path/to/sample.csv
```

Only a **text** column and a **gold main-code** column are required. If their
names differ from the defaults, edit `COLUMNS` in `config.py`; the gold domain is
always derived from the code via the codebook. A stable per-row id is built from
`ID_COLUMNS` (default `manifesto_id` + `pos`), falling back to the row index.

## What you get

- **`reports/dataset_profile.md`** — category/domain distribution, absent
  categories, valence-pair observability, catch-all share, length, power note.
- **`reports/metrics.csv`** — per model×condition: compliance, accuracy,
  accuracy|compliant, domain accuracy, weighted F1, and error-taxonomy rates.
- **Error taxonomy (mechanical):** `E1` cross-domain, `E2` valence flip,
  `E5` catch-all absorption, plus residual. Errors are flagged for *all*
  applicable types (an error can be both E1 and E5).
- **`reports/stats_cochran.csv`** — omnibus test that the 4 conditions differ
  (per model).
- **`reports/stats_mcnemar.csv`** — Holm-corrected pairwise tests for the
  comparisons in `config.COMPARISONS`.
- **`reports/stats_direction_consistency.csv`** — whether an effect points the
  same way across models (a one-model result is not an effect).

## Caveats baked into the design

- With n=300 and skewed classes, **per-category** tests are underpowered; the
  trustworthy tests are on **overall accuracy and compliance**. The profile
  quantifies this.
- Category **presentation order** is fixed (codebook order). Order-sensitivity
  (Halterman & Keith 2026) is a known effect held constant here, out of scope.
- `E3` (exclusion-criterion violations) and `E4` (lexical-trigger pull) are
  **not** computed — they need a refined lookup/trigger-token pass and belong to
  a later, taxonomy-focused pilot.
