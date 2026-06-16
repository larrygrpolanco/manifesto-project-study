# Pilot Plan — "Does the model know when the question is hard?"

> **Handoff doc.** Self-contained build/run/analysis plan for the pilot. A fresh chat
> should be able to execute from this file alone. Parent design:
> [RESEARCH_PLAN_branch_human_distribution.md](RESEARCH_PLAN_branch_human_distribution.md).
> Status: design locked, **no LLM runs yet**.

## What this pilot is for

A **feasibility probe** for the research branch whose wedge is the **per-sentence human
disagreement distribution**: for each of 179 manifesto quasi-sentences we know exactly how
trained expert coders split when coding it. The pilot does **not** try to answer the
research questions — it asks "is this study runnable, and where are the cliffs?":

- **Q1 pulse** — where experts genuinely split, does the model also waver, or pin one answer with fake confidence?
- **Resolution** — do 10 runs per model give a usable model-spread estimate? *(most important feasibility output)*
- **Q2 cells** — do model errors land in enough distinct category-pairs to compare against human confusion pairs?
- **Plumbing** — parity prompt works, output parses, `000` usable, logprobs captured where available.

## Inputs already on disk (Step 0, done + validated)

- [reports/human/per_sentence_ambiguity.csv](reports/human/per_sentence_ambiguity.csv) — 179 sentences × 40 disagreement metrics. Columns are 4 combos `{full,retained}`×`{class,exclude}` of: `n, cat_distinct, cat_modal_share, cat_1mmodal, cat_Hnorm, dom_1mmodal, rile_1mmodal, rile_distinct, rile_modal`. Keyed by `unit_id`. `full` = all coders (32 GB / 23 NZ); `retained` = MLB expert screen (17 GB / 12 NZ); `class` = 000 as a code; `exclude` = drop uncoded votes.
- [data/cmp_coding_sample.json](data/cmp_coding_sample.json) — `{metadata, categories, units}`. 179 units, **complete contiguous extracts** (GB seq 1–107 / 9 sections; NZ seq 1–72 / 3 sections). Each unit: `unit_id, manifesto, sequence, text, master_code, master_label, master_rile, section`.
- [data/categories.json](data/categories.json) — 56 standard categories + `000`, each with `label, domain, rile, definition`. RILE: 13 left / 13 right / 31 none.
- [reports/human/human_codings.csv](reports/human/human_codings.csv) — long form `coder_id, manifesto, unit_id, sequence, code` (5,080 rows). Raw material for human confusion pairs (Q2).
- [reports/human/coders.csv](reports/human/coders.csv) — `coder_id, manifesto, prior_experience, mlb_retained` (the retention flag).
- [src/prompts/coding_instrument.md](src/prompts/coding_instrument.md) — parity-prompt draft (system block, parity commitments, decision rules, context-block template).
- **Reusable code** in [archive/early-experiment/pilot-2/src/](archive/early-experiment/pilot-2/src/): OpenRouter client init + `.env` dotenv loader, resumable per-config JSONL cache, threaded worker pool with retry/backoff, `<think>`-tag stripping + regex 3-digit parser, codebook renderer (`codebook.py`). **Port these; do not import across the archive boundary.** Pilot-2 was built for a different design (temp-0, context-as-manipulation, stratified-random sampling) — reuse mechanics, not design.

## Locked decisions

1. **Scope:** build + run + analysis + exemplar close-reads, end to end.
2. **Models (all 8; FAIL LOUD — any unreachable ID halts the run):**
   `deepseek/deepseek-v4-flash`, `deepseek/deepseek-v4-pro`,
   `qwen/qwen3.6-35b-a3b`, `qwen/qwen3.6-plus`,
   `google/gemma-4-26b-a4b-it`, `google/gemma-4-31b-it`,
   `anthropic/claude-3.5-haiku`, `anthropic/claude-haiku-4.5`.
   OpenRouter, key in repo-root `.env` as `OPENROUTER_API_KEY`, base `https://openrouter.ai/api/v1`, `openai` SDK.
3. **Sentence selection (frozen, no tunable knobs):** rank all 179 by `full_class_cat_1mmodal` (000 kept as a class). **High-split = top 10, mid-split = 10 around the median, high-agreement = bottom 10.** Identify the 4 balanced-RILE coin-flips (`full_class_rile_distinct == 3` with no RILE class > ~40%) and force-include them in high-split *only if* they aren't already there. Report the GB/NZ split (don't quota it). Keep `retained_class_*` columns in the manifest for downstream analysis. Freeze to `runs/pilot/sentence_manifest.csv`.
4. **Context block = full extract.** Give the model the entire manifesto extract (all units in sequence order, section headings shown), target quasi-sentence delimited »«. True MLB parity; cheap. Identical prompt across the 10 runs.
5. **Output contract:** ask for the bare 3-digit code. Strip `<think>` tags → regex-extract → validate against the 57 codes. Off-scheme / refusal / multi-code outputs are **logged raw and counted as their own bucket** in the spread (mirrors human `000`/off-gold), never silently dropped.
6. **Run independence:** temp = 1, **NO fixed seed** (the 10 runs must vary — opposite of pilot-2). Capture logprobs opportunistically where the provider returns them (bonus only).
7. **Reasoning = secondary variable.** Probe each model: if reasoning is **toggleable** → run both `on` and `off` as two configs; if fixed → run once in its fixed mode. Grid emerges from the probe, reported before spend. Model spread computed **per config**, never pooled across reasoning modes.
8. **Q1 denominator:** headline compares model spread vs **retained** (expert) human spread; **full** pool reported as a one-line robustness check. Same metric both sides: 1−modal-share + normalized entropy (Hnorm).
9. **Code layout:** fresh package `src/pilot/`; outputs to `runs/pilot/` and `reports/pilot/`. Archive stays frozen.

## Build — `src/pilot/`

- **`config.py`** — model roster, paths, `N_RUNS=10`, `TEMPERATURE=1.0`, no seed, allowed-codes set from `categories.json`, OpenRouter base URL + key from `.env`. *(Port dotenv loader + client pattern from pilot-2 `run_experiment.py`.)*
- **`select_sentences.py`** — apply selection rule to `per_sentence_ambiguity.csv`; identify 4 balanced-RILE cases; write `runs/pilot/sentence_manifest.csv` (`unit_id, bucket, text, section, full_class_*, retained_class_*`); print GB/NZ split.
- **`prompt.py`** — render parity prompt from `coding_instrument.md`: system/instructions + full category list injected verbatim from `categories.json` + decision rules + full-extract context with target delimited. *(Port `codebook.render_*` from pilot-2.)*
- **`probe_models.py`** — one cheap call per model: confirm reachability (**fail loud**), detect reasoning capability (toggleable / always-on / always-off), note logprobs support. Emit `runs/pilot/run_grid.json`; report for sign-off **before** the big run.
- **`run.py`** — execute `configs × 30 × 10` at temp 1, no seed. *(Port pilot-2 resumable JSONL cache + threaded pool + retry/backoff + parser.)* Capture per call: `pred_code, raw_text, off_scheme, reasoning_present, prompt_tok, completion_tok, logprobs?`. Rebuild tidy `runs/pilot/predictions.csv`.
- **`analyze.py`** — the analysis below → `reports/pilot/`.

**Volume:** emergent from probe, ~8–16 configs × 30 × 10 = **2,400–4,800 calls**. Trivial cost. Reported before spend.

## Analysis — `reports/pilot/`

1. **Q1 pulse** — per sentence per config: model spread (distribution over codes across 10 runs; 1−modal-share + Hnorm). Plot model spread vs **retained** human spread across the 30 sentences (full-pool overlay = robustness); single correlation; eyeball coin-flip corner (wide human spread, narrow model spread).
2. **Resolution check** *(key)* — recompute per-sentence model spread at 10 → 5 → 3 runs; report movement. Sets runs-per-model for the full study.
3. **Q2 cells** — model confusion pairs from `predictions.csv` vs human confusion pairs from `human_codings.csv` (same categories); count non-empty cells; decide Q2 = headline or illustration.
4. **Reasoning contrast** *(secondary)* — toggleable models: spread `on` vs `off`.
5. **Exemplar close-reads** — pull 2–3 sentences (one coin-flip where the model pins, one where model+humans both waver, ideally one alien-confusion); read with the 32-coder receipts.

Map results to parent plan §4.4 pre-committed reads (merge / reshape / park).

## Verification

```
python -m src.pilot.select_sentences      # manifest: 30 rows, 3×10 buckets, 4 balanced-RILE present, GB/NZ split printed
python -m src.pilot.prompt --unit GB-004  # eyeball one rendered parity prompt (full extract, target delimited)
python -m src.pilot.probe_models          # all 8 reachable (else HALT); run_grid.json lists configs+reasoning caps -> SIGN OFF before spend
python -m src.pilot.run --limit 5         # smoke: cache writes, parser recovers codes, off-scheme logged, resumes clean on rerun
python -m src.pilot.run                    # full run; predictions.csv rows == grid size; high-split sentence shows code variation
python -m src.pilot.analyze                # 3 checks + exemplars land in reports/pilot/; Q1 plot has expected coin-flip points
```

## Deferred (parent plan §6)

Final RQ wording, interleaved-vs-gathered exemplars, difficulty-oracle act, full-study roster/run-counts/temp grid, "replace coders" stance — all decided on pilot data.


To run it (needs deps + the future model IDs live)

python -m venv .venv && source .venv/bin/activate && pip install -r src/pilot/requirements.txt
python -m src.pilot.prompt --unit NZ-022     # eyeball a rendered parity prompt
python -m src.pilot.probe_models             # FAIL LOUD; prints volume → SIGN OFF before spend
python -m src.pilot.run --limit 5            # smoke: cache/parser/resume
python -m src.pilot.run                      # full run
python -m src.pilot.analyze                  # → reports/pilot/