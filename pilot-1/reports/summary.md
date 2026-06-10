# Pilot-1 evaluation summary

## Metrics (per model × condition)

| model                   | condition   |   n |   compliance |   accuracy |   accuracy\|compliant |   domain_accuracy |   weighted_f1 |   n_errors |   E1_cross_domain |   E2_valence_flip |   E5_catch_all |   residual |
|:------------------------|:------------|----:|-------------:|-----------:|----------------------:|------------------:|--------------:|-----------:|------------------:|------------------:|---------------:|-----------:|
| llama-3.1-8b-instant    | FULL        |  50 |         1    |       0.18 |                 0.18  |              0.36 |         0.208 |         41 |             0.78  |             0     |          0.098 |      0.146 |
| llama-3.1-8b-instant    | HIER1       |  50 |         1    |       0.14 |                 0.14  |              0.34 |         0.159 |         43 |             0.767 |             0     |          0     |      0.233 |
| llama-3.1-8b-instant    | HIER2       |  50 |         1    |       0.24 |                 0.24  |              0.52 |         0.259 |         38 |             0.632 |             0     |          0.105 |      0.316 |
| llama-3.1-8b-instant    | LABELS      |  50 |         1    |       0.24 |                 0.24  |              0.42 |         0.267 |         38 |             0.763 |             0.026 |          0.105 |      0.158 |
| llama-3.3-70b-versatile | FULL        |  50 |         1    |       0.26 |                 0.26  |              0.44 |         0.282 |         37 |             0.757 |             0     |          0.243 |      0.162 |
| llama-3.3-70b-versatile | HIER1       |  50 |         1    |       0.24 |                 0.24  |              0.44 |         0.272 |         38 |             0.737 |             0     |          0.105 |      0.211 |
| llama-3.3-70b-versatile | HIER2       |  50 |         1    |       0.3  |                 0.3   |              0.54 |         0.313 |         35 |             0.657 |             0     |          0.171 |      0.286 |
| llama-3.3-70b-versatile | LABELS      |  50 |         1    |       0.26 |                 0.26  |              0.42 |         0.271 |         37 |             0.784 |             0.027 |          0.405 |      0.081 |
| openai/gpt-oss-120b     | FULL        |  50 |         0.96 |       0.28 |                 0.292 |              0.46 |         0.333 |         34 |             0.735 |             0     |          0.294 |      0.147 |
| openai/gpt-oss-120b     | HIER1       |  50 |         0.96 |       0.34 |                 0.354 |              0.56 |         0.372 |         31 |             0.645 |             0     |          0.161 |      0.226 |
| openai/gpt-oss-120b     | HIER2       |  50 |         1    |       0.32 |                 0.32  |              0.54 |         0.322 |         34 |             0.676 |             0     |          0.324 |      0.176 |
| openai/gpt-oss-120b     | LABELS      |  50 |         0.98 |       0.34 |                 0.347 |              0.48 |         0.348 |         32 |             0.781 |             0     |          0.062 |      0.188 |
| openai/gpt-oss-20b      | FULL        |  50 |         0.7  |       0.22 |                 0.314 |              0.32 |         0.254 |         24 |             0.792 |             0     |          0.292 |      0.167 |
| openai/gpt-oss-20b      | HIER1       |  50 |         0.76 |       0.2  |                 0.263 |              0.34 |         0.249 |         28 |             0.75  |             0     |          0.107 |      0.214 |
| openai/gpt-oss-20b      | HIER2       |  50 |         0.82 |       0.26 |                 0.317 |              0.42 |         0.292 |         28 |             0.714 |             0     |          0.321 |      0.179 |
| openai/gpt-oss-20b      | LABELS      |  50 |         0.82 |       0.24 |                 0.293 |              0.34 |         0.254 |         29 |             0.828 |             0     |          0     |      0.172 |
| qwen/qwen3-32b          | FULL        |  50 |         1    |       0.34 |                 0.34  |              0.48 |         0.362 |         33 |             0.788 |             0     |          0.273 |      0.152 |
| qwen/qwen3-32b          | HIER1       |  50 |         1    |       0.36 |                 0.36  |              0.58 |         0.393 |         32 |             0.656 |             0     |          0.062 |      0.312 |
| qwen/qwen3-32b          | HIER2       |  50 |         0.98 |       0.3  |                 0.306 |              0.46 |         0.355 |         34 |             0.765 |             0     |          0.088 |      0.176 |
| qwen/qwen3-32b          | LABELS      |  50 |         1    |       0.3  |                 0.3   |              0.5  |         0.294 |         35 |             0.714 |             0.029 |          0.229 |      0.171 |

## Cochran's Q (omnibus across conditions, per model)

| model                   |   n_items |   k_conditions |      Q |   df |      p |
|:------------------------|----------:|---------------:|-------:|-----:|-------:|
| llama-3.1-8b-instant    |        50 |              4 | 4.6957 |    3 | 0.1955 |
| llama-3.3-70b-versatile |        50 |              4 | 1.3902 |    3 | 0.7078 |
| openai/gpt-oss-120b     |        50 |              4 | 1.6364 |    3 | 0.6512 |
| openai/gpt-oss-20b      |        50 |              4 | 1.1111 |    3 | 0.7744 |
| qwen/qwen3-32b          |        50 |              4 | 1.5882 |    3 | 0.6621 |

## Pairwise McNemar (Holm-corrected, exact-category correctness)

| model                   | comparison                | a      | b     |   acc_a |   acc_b |   delta(b-a) |   b_fixed |   a_kept(b_broke) |   discordant |   statistic |   p_raw |   p_holm | sig_.05   |
|:------------------------|:--------------------------|:-------|:------|--------:|--------:|-------------:|----------:|------------------:|-------------:|------------:|--------:|---------:|:----------|
| llama-3.1-8b-instant    | info: LABELS vs FULL      | LABELS | FULL  |    0.24 |    0.18 |        -0.06 |         1 |                 4 |            5 |           1 |  0.375  |      1   | False     |
| llama-3.1-8b-instant    | structure: FULL vs HIER1  | FULL   | HIER1 |    0.18 |    0.14 |        -0.04 |         2 |                 4 |            6 |           2 |  0.6875 |      1   | False     |
| llama-3.1-8b-instant    | structure: FULL vs HIER2  | FULL   | HIER2 |    0.18 |    0.24 |         0.06 |         6 |                 3 |            9 |           3 |  0.5078 |      1   | False     |
| llama-3.1-8b-instant    | structure: HIER1 vs HIER2 | HIER1  | HIER2 |    0.14 |    0.24 |         0.1  |         6 |                 1 |            7 |           1 |  0.125  |      0.5 | False     |
| llama-3.3-70b-versatile | info: LABELS vs FULL      | LABELS | FULL  |    0.26 |    0.26 |         0    |         3 |                 3 |            6 |           3 |  1      |      1   | False     |
| llama-3.3-70b-versatile | structure: FULL vs HIER1  | FULL   | HIER1 |    0.26 |    0.24 |        -0.02 |         1 |                 2 |            3 |           1 |  1      |      1   | False     |
| llama-3.3-70b-versatile | structure: FULL vs HIER2  | FULL   | HIER2 |    0.26 |    0.3  |         0.04 |         6 |                 4 |           10 |           4 |  0.7539 |      1   | False     |
| llama-3.3-70b-versatile | structure: HIER1 vs HIER2 | HIER1  | HIER2 |    0.24 |    0.3  |         0.06 |         5 |                 2 |            7 |           2 |  0.4531 |      1   | False     |
| openai/gpt-oss-120b     | info: LABELS vs FULL      | LABELS | FULL  |    0.34 |    0.28 |        -0.06 |         2 |                 5 |            7 |           2 |  0.4531 |      1   | False     |
| openai/gpt-oss-120b     | structure: FULL vs HIER1  | FULL   | HIER1 |    0.28 |    0.34 |         0.06 |         3 |                 0 |            3 |           0 |  0.25   |      1   | False     |
| openai/gpt-oss-120b     | structure: FULL vs HIER2  | FULL   | HIER2 |    0.28 |    0.32 |         0.04 |         6 |                 4 |           10 |           4 |  0.7539 |      1   | False     |
| openai/gpt-oss-120b     | structure: HIER1 vs HIER2 | HIER1  | HIER2 |    0.34 |    0.32 |        -0.02 |         4 |                 5 |            9 |           4 |  1      |      1   | False     |
| openai/gpt-oss-20b      | info: LABELS vs FULL      | LABELS | FULL  |    0.24 |    0.22 |        -0.02 |         4 |                 5 |            9 |           4 |  1      |      1   | False     |
| openai/gpt-oss-20b      | structure: FULL vs HIER1  | FULL   | HIER1 |    0.22 |    0.2  |        -0.02 |         2 |                 3 |            5 |           2 |  1      |      1   | False     |
| openai/gpt-oss-20b      | structure: FULL vs HIER2  | FULL   | HIER2 |    0.22 |    0.26 |         0.04 |         6 |                 4 |           10 |           4 |  0.7539 |      1   | False     |
| openai/gpt-oss-20b      | structure: HIER1 vs HIER2 | HIER1  | HIER2 |    0.2  |    0.26 |         0.06 |         6 |                 3 |            9 |           3 |  0.5078 |      1   | False     |
| qwen/qwen3-32b          | info: LABELS vs FULL      | LABELS | FULL  |    0.3  |    0.34 |         0.04 |         6 |                 4 |           10 |           4 |  0.7539 |      1   | False     |
| qwen/qwen3-32b          | structure: FULL vs HIER1  | FULL   | HIER1 |    0.34 |    0.36 |         0.02 |         4 |                 3 |            7 |           3 |  1      |      1   | False     |
| qwen/qwen3-32b          | structure: FULL vs HIER2  | FULL   | HIER2 |    0.34 |    0.3  |        -0.04 |         3 |                 5 |            8 |           3 |  0.7266 |      1   | False     |
| qwen/qwen3-32b          | structure: HIER1 vs HIER2 | HIER1  | HIER2 |    0.36 |    0.3  |        -0.06 |         3 |                 6 |            9 |           3 |  0.5078 |      1   | False     |

## Direction consistency across models

`b>a` = how many models scored the second condition higher. An effect you trust shows the same direction across most models *and* significance.

| comparison                |   models |   b>a |   b<a |   significant(Holm) |
|:--------------------------|---------:|------:|------:|--------------------:|
| info: LABELS vs FULL      |        5 |     1 |     3 |                   0 |
| structure: FULL vs HIER1  |        5 |     2 |     3 |                   0 |
| structure: FULL vs HIER2  |        5 |     4 |     1 |                   0 |
| structure: HIER1 vs HIER2 |        5 |     3 |     2 |                   0 |
