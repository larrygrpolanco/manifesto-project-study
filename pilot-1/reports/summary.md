# Pilot-1 evaluation summary

## Metrics (per model × condition)

| model                | condition   |   n |   compliance |   accuracy |   accuracy\|compliant |   domain_accuracy |   weighted_f1 |   n_errors |   E1_cross_domain |   E2_valence_flip |   E5_catch_all |   residual |
|:---------------------|:------------|----:|-------------:|-----------:|----------------------:|------------------:|--------------:|-----------:|------------------:|------------------:|---------------:|-----------:|
| llama-3.1-8b-instant | FULL        | 300 |        1     |      0.207 |                 0.207 |             0.383 |         0.237 |        238 |             0.777 |             0.013 |          0.084 |      0.172 |
| llama-3.1-8b-instant | HIER1       | 300 |        1     |      0.24  |                 0.24  |             0.46  |         0.265 |        228 |             0.711 |             0.026 |          0.026 |      0.25  |
| llama-3.1-8b-instant | HIER2       | 300 |        1     |      0.377 |                 0.377 |             0.583 |         0.393 |        187 |             0.668 |             0.027 |          0.123 |      0.257 |
| openai/gpt-oss-120b  | FULL        | 300 |        0.95  |      0.407 |                 0.428 |             0.54  |         0.454 |        163 |             0.755 |             0.006 |          0.288 |      0.19  |
| openai/gpt-oss-120b  | HIER1       | 300 |        0.98  |      0.457 |                 0.466 |             0.61  |         0.497 |        157 |             0.707 |             0.019 |          0.248 |      0.204 |
| openai/gpt-oss-120b  | HIER2       | 300 |        0.997 |      0.39  |                 0.391 |             0.543 |         0.411 |        182 |             0.747 |             0.016 |          0.258 |      0.187 |
| qwen/qwen3-32b       | FULL        | 300 |        0.997 |      0.397 |                 0.398 |             0.567 |         0.449 |        180 |             0.717 |             0.006 |          0.283 |      0.206 |
| qwen/qwen3-32b       | HIER1       | 300 |        0.98  |      0.42  |                 0.429 |             0.6   |         0.461 |        168 |             0.679 |             0.018 |          0.208 |      0.244 |
| qwen/qwen3-32b       | HIER2       | 300 |        1     |      0.34  |                 0.34  |             0.547 |         0.376 |        198 |             0.687 |             0.015 |          0.177 |      0.258 |

## Cochran's Q (omnibus across conditions, per model)

| model                |   n_items |   k_conditions |       Q |   df |      p |
|:---------------------|----------:|---------------:|--------:|-----:|-------:|
| llama-3.1-8b-instant |       300 |              3 | 45.6458 |    2 | 0      |
| openai/gpt-oss-120b  |       300 |              3 |  9.1549 |    2 | 0.0103 |
| qwen/qwen3-32b       |       300 |              3 | 12.3514 |    2 | 0.0021 |

## Pairwise McNemar (Holm-corrected, exact-category correctness)

| model                | comparison                | a     | b     |   acc_a |   acc_b |   delta(b-a) |   b_fixed |   a_kept(b_broke) |   discordant |   statistic |   p_raw |   p_holm | sig_.05   |
|:---------------------|:--------------------------|:------|:------|--------:|--------:|-------------:|----------:|------------------:|-------------:|------------:|--------:|---------:|:----------|
| llama-3.1-8b-instant | structure: FULL vs HIER1  | FULL  | HIER1 |  0.2067 |  0.24   |       0.0333 |        25 |                15 |           40 |      2.025  |  0.1547 |   0.1547 | False     |
| llama-3.1-8b-instant | structure: FULL vs HIER2  | FULL  | HIER2 |  0.2067 |  0.3767 |       0.17   |        65 |                14 |           79 |     31.6456 |  0      |   0      | True      |
| llama-3.1-8b-instant | structure: HIER1 vs HIER2 | HIER1 | HIER2 |  0.24   |  0.3767 |       0.1367 |        57 |                16 |           73 |     21.9178 |  0      |   0      | True      |
| openai/gpt-oss-120b  | structure: FULL vs HIER1  | FULL  | HIER1 |  0.4067 |  0.4567 |       0.05   |        26 |                11 |           37 |      5.2973 |  0.0214 |   0.0427 | True      |
| openai/gpt-oss-120b  | structure: FULL vs HIER2  | FULL  | HIER2 |  0.4067 |  0.39   |      -0.0167 |        25 |                30 |           55 |      0.2909 |  0.5896 |   0.5896 | False     |
| openai/gpt-oss-120b  | structure: HIER1 vs HIER2 | HIER1 | HIER2 |  0.4567 |  0.39   |      -0.0667 |        15 |                35 |           50 |      7.22   |  0.0072 |   0.0216 | True      |
| qwen/qwen3-32b       | structure: FULL vs HIER1  | FULL  | HIER1 |  0.3967 |  0.42   |       0.0233 |        24 |                17 |           41 |      0.878  |  0.3487 |   0.3487 | False     |
| qwen/qwen3-32b       | structure: FULL vs HIER2  | FULL  | HIER2 |  0.3967 |  0.34   |      -0.0567 |        18 |                35 |           53 |      4.8302 |  0.028  |   0.0559 | False     |
| qwen/qwen3-32b       | structure: HIER1 vs HIER2 | HIER1 | HIER2 |  0.42   |  0.34   |      -0.08   |        15 |                39 |           54 |      9.7963 |  0.0017 |   0.0052 | True      |

## Direction consistency across models

`b>a` = how many models scored the second condition higher. An effect you trust shows the same direction across most models *and* significance.

| comparison                |   models |   b>a |   b<a |   significant(Holm) |
|:--------------------------|---------:|------:|------:|--------------------:|
| structure: FULL vs HIER1  |        3 |     3 |     0 |                   1 |
| structure: FULL vs HIER2  |        3 |     1 |     2 |                   1 |
| structure: HIER1 vs HIER2 |        3 |     1 |     2 |                   3 |
