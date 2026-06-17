# Pilot summary

Feasibility readout, mapped to RESEARCH_PLAN §4.4 pre-committed reads. Numbers are reported; the merge/reshape/park call is the researcher's.

## 1. Q1 pulse — read the decomposition, NOT the single correlation

A per-config Pearson r (table 1d) conflates three different things. Taken alone it shows positive r and reads as 'model tracks human difficulty -> signal absent'. The decomposition below shows that read is an artifact of the easy sentences.

### 1a. Under-dispersion — model spread vs human spread, per bucket

Model spread is compressed relative to humans, and the compression is worst on the hard items. ratio = mean model 1-modal / mean human (retained) 1-modal; <1 means the model wavers less than the experts.

| bucket | n | model 1-modal | human ret | human full | model/human ratio |
|---|---|---|---|---|---|
| high-agreement | 140 | 0.026 | 0.100 | 0.132 | 0.26 |
| mid-split | 140 | 0.209 | 0.420 | 0.527 | 0.50 |
| high-split | 196 | 0.248 | 0.643 | 0.724 | 0.39 |

### 1b. The correlation trap — pooled r, all sentences vs hard-only

Most of the apparent tracking is the easy anchor (easy-for-both). Drop the high-agreement bucket and the relationship inside the range that matters nearly vanishes.

- pooled r(model, human retained), **all buckets**: 0.461 (n=476)
- pooled r(model, human retained), **hard+mid only**: 0.191 (n=336)

### 1c. Within- vs between-model spread, per bucket

Within = one model's 10 runs (does it waver?). Between = do the models agree with EACH OTHER? On hard items each model pins fairly hard by itself while disagreeing across models -> manufactured consensus is per-model, not shared.

| bucket | n | within-model | between-model |
|---|---|---|---|
| high-agreement | 10 | 0.026 | 0.000 |
| mid-split | 10 | 0.209 | 0.314 |
| high-split | 14 | 0.248 | 0.418 |

### 1d. Per-config correlation (demoted — see 1b for why)

| config | n | r(model,retained) | r(model,full) | mean model 1-modal | off-scheme |
|---|---|---|---|---|---|
| anthropic__claude-3.5-haiku__off | 34 | 0.441 | 0.541 | 0.171 | 0.0% |
| anthropic__claude-haiku-4.5__off | 34 | 0.252 | 0.326 | 0.124 | 0.0% |
| anthropic__claude-haiku-4.5__on | 34 | 0.468 | 0.525 | 0.197 | 0.0% |
| deepseek__deepseek-v4-flash__off | 34 | 0.375 | 0.368 | 0.259 | 0.0% |
| deepseek__deepseek-v4-flash__on | 34 | 0.414 | 0.458 | 0.147 | 1.8% |
| deepseek__deepseek-v4-pro__on | 34 | 0.562 | 0.594 | 0.221 | 3.5% |
| google__gemma-4-26b-a4b-it__off | 34 | 0.300 | 0.323 | 0.038 | 0.0% |
| google__gemma-4-26b-a4b-it__on | 34 | 0.584 | 0.600 | 0.185 | 33.8% |
| google__gemma-4-31b-it__off | 34 | 0.461 | 0.444 | 0.062 | 0.0% |
| google__gemma-4-31b-it__on | 34 | 0.451 | 0.396 | 0.147 | 10.9% |
| qwen__qwen3.6-35b-a3b__off | 34 | 0.548 | 0.577 | 0.224 | 0.3% |
| qwen__qwen3.6-35b-a3b__on | 34 | 0.611 | 0.595 | 0.232 | 15.3% |
| qwen__qwen3.6-plus__off | 34 | 0.594 | 0.633 | 0.215 | 0.0% |
| qwen__qwen3.6-plus__on | 34 | 0.636 | 0.620 | 0.176 | 0.0% |

**Off-scheme contamination (>5%) — these configs' spread is partly parsing failure, not uncertainty; treat their Q1 numbers as unreliable until the parser/reasoning handling is fixed:**
- google__gemma-4-26b-a4b-it__on: 33.8%
- google__gemma-4-31b-it__on: 10.9%
- qwen__qwen3.6-35b-a3b__on: 15.3%

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

Read §1a-1c together, not the raw correlation in §1d. The signal is not the clean present/absent dichotomy §4.4 anticipated:
- **Under-dispersion (1a):** model spread compressed vs humans, worst on hard items -> the §4.4 'model fakes confidence' outcome, quantified.
- **Flattening + correlation trap (1a/1b):** models separate easy from hard but barely separate hard from coin-flip; the pooled r is mostly the easy anchor. Headline = 'sharply under-dispersed, barely discriminates difficulty', NOT 'tracks human difficulty'.
- **Between > within (1c):** per-model overconfidence on DIFFERENT answers -> manufactured consensus is per-model, not shared.
- These lean **merge; Q1 headline; scale up** — with the framing above.
- Resolution bad at 10 -> full study needs deeper per-model sampling; recost.
- Q2 cells empty -> Q2 demotes to illustration (note: confusion is still defined vs master_code; redefine vs the human distribution before trusting the alien count).
- Exemplars flat -> reconsider mixed-methods selling point.


Plain-language meaning: when a sentence is a coin-flip for human experts, a model doesn't flip a coin — it slams down an answer with ~3× the confidence the humans had, can't distinguish that case from a merely-hard one, and a different model slams down a different answer just as confidently. That is a genuine, novel, publishable result, and it leans toward merge / Q1 as headline — but the headline is "models are sharply under-dispersed and barely discriminate difficulty," not the naive "model tracks human difficulty" the raw correlation implied.