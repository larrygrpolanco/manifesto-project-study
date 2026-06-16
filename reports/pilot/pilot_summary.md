# Pilot summary

Feasibility readout, mapped to RESEARCH_PLAN §4.4 pre-committed reads. Numbers are reported; the merge/reshape/park call is the researcher's.

## 1. Q1 pulse (model spread vs RETAINED human spread)

Per-config correlation of model spread (1-modal) with retained human spread. **Signal we want: LOW/negative-ish or flat on hard items — model spread NOT tracking human spread** (see q1_scatter.png coin-flip corner).

| config | n | r(model,retained) | r(model,full) | mean model 1-modal | mean human 1-modal |
|---|---|---|---|---|---|
| anthropic__claude-3.5-haiku__off | 34 | 0.441 | 0.541 | 0.171 | 0.418 |
| anthropic__claude-haiku-4.5__off | 34 | 0.252 | 0.326 | 0.124 | 0.418 |
| anthropic__claude-haiku-4.5__on | 34 | 0.468 | 0.525 | 0.197 | 0.418 |
| deepseek__deepseek-v4-flash__off | 34 | 0.375 | 0.368 | 0.259 | 0.418 |
| deepseek__deepseek-v4-flash__on | 34 | 0.414 | 0.458 | 0.147 | 0.418 |
| deepseek__deepseek-v4-pro__on | 34 | 0.562 | 0.594 | 0.221 | 0.418 |
| google__gemma-4-26b-a4b-it__off | 34 | 0.300 | 0.323 | 0.038 | 0.418 |
| google__gemma-4-26b-a4b-it__on | 34 | 0.584 | 0.600 | 0.185 | 0.418 |
| google__gemma-4-31b-it__off | 34 | 0.461 | 0.444 | 0.062 | 0.418 |
| google__gemma-4-31b-it__on | 34 | 0.451 | 0.396 | 0.147 | 0.418 |
| qwen__qwen3.6-35b-a3b__off | 34 | 0.548 | 0.577 | 0.224 | 0.418 |
| qwen__qwen3.6-35b-a3b__on | 34 | 0.611 | 0.595 | 0.232 | 0.418 |
| qwen__qwen3.6-plus__off | 34 | 0.594 | 0.633 | 0.215 | 0.418 |
| qwen__qwen3.6-plus__on | 34 | 0.636 | 0.620 | 0.176 | 0.418 |

## 2. Resolution check (KEY) — spread movement 10 -> 5 -> 3 runs

Mean |spread(k) - spread(10)| across sentences. Small = 10 runs is plenty (could go cheaper); large = full study needs deeper sampling.

| config | abs-Δ(1-modal) 10v5 | 10v3 | abs-Δ(Hnorm) 10v5 | 10v3 |
|---|---|---|---|---|
| anthropic__claude-3.5-haiku__off | 0.053 | 0.075 | 0.087 | 0.112 |
| anthropic__claude-haiku-4.5__off | 0.047 | 0.057 | 0.056 | 0.106 |
| anthropic__claude-haiku-4.5__on | 0.056 | 0.070 | 0.079 | 0.166 |
| deepseek__deepseek-v4-flash__off | 0.088 | 0.145 | 0.119 | 0.229 |
| deepseek__deepseek-v4-flash__on | 0.071 | 0.076 | 0.080 | 0.147 |
| deepseek__deepseek-v4-pro__on | 0.056 | 0.103 | 0.071 | 0.195 |
| google__gemma-4-26b-a4b-it__off | 0.021 | 0.034 | 0.027 | 0.057 |
| google__gemma-4-26b-a4b-it__on | 0.062 | 0.107 | 0.090 | 0.172 |
| google__gemma-4-31b-it__off | 0.026 | 0.034 | 0.037 | 0.072 |
| google__gemma-4-31b-it__on | 0.059 | 0.090 | 0.082 | 0.138 |
| qwen__qwen3.6-35b-a3b__off | 0.065 | 0.106 | 0.091 | 0.143 |
| qwen__qwen3.6-35b-a3b__on | 0.056 | 0.097 | 0.078 | 0.150 |
| qwen__qwen3.6-plus__off | 0.062 | 0.085 | 0.064 | 0.117 |
| qwen__qwen3.6-plus__on | 0.053 | 0.067 | 0.087 | 0.122 |

## 3. Q2 confusion cells

- human confusion pairs (full): 153 (retained: 87)
- model confusion pairs (pooled): 137
- overlap (both): 84
- model-only (candidate ALIEN): 53
- human-only: 69

Decision input: enough non-empty overlapping cells -> Q2 can be a headline; sparse -> Q2 is a discussion illustration (pre-authorised).

## 4. Reasoning contrast

6 toggleable model(s); see reasoning_contrast.csv (spread on vs off, per config).

## 5. Exemplars

See exemplars.md — three sentences read with the 32-coder receipts.

## Map to §4.4

- Q1 signal present (human spread varies, model spread stays narrow) -> merge; Q1 headline; scale up.
- Q1 signal absent (model tracks human) -> finding, reshape toward Q2 / oracle.
- Resolution bad at 10 -> full study needs deeper per-model sampling; recost.
- Q2 cells empty -> Q2 demotes to illustration.
- Exemplars flat -> reconsider mixed-methods selling point.
