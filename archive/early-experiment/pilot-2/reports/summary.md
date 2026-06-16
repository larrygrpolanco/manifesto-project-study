# Pilot-2 evaluation summary

## Metrics (per model × condition)

| model                      | condition   |   n |   compliance |   accuracy |   accuracy\|compliant |   domain_accuracy |   weighted_f1 |   n_errors |   E1_cross_domain |   E2_valence_flip |   E5_catch_all |   residual |
|:---------------------------|:------------|----:|-------------:|-----------:|----------------------:|------------------:|--------------:|-----------:|------------------:|------------------:|---------------:|-----------:|
| deepseek/deepseek-v4-flash | BASE        | 600 |        0.992 |      0.397 |                 0.4   |             0.602 |         0.391 |        357 |             0.655 |             0.048 |          0.171 |      0.283 |
| deepseek/deepseek-v4-flash | FULLDOC     | 600 |        0.987 |      0.453 |                 0.459 |             0.633 |         0.436 |        320 |             0.662 |             0.044 |          0.141 |      0.284 |
| deepseek/deepseek-v4-flash | WINDOW      | 600 |        0.98  |      0.442 |                 0.451 |             0.635 |         0.426 |        323 |             0.641 |             0.034 |          0.139 |      0.313 |
| google/gemma-4-26b-a4b-it  | BASE        | 600 |        1     |      0.43  |                 0.43  |             0.602 |         0.447 |        342 |             0.699 |             0.038 |          0.26  |      0.251 |
| google/gemma-4-26b-a4b-it  | FULLDOC     | 600 |        0.925 |      0.437 |                 0.472 |             0.61  |         0.433 |        293 |             0.645 |             0.031 |          0.126 |      0.311 |
| google/gemma-4-26b-a4b-it  | WINDOW      | 600 |        0.998 |      0.48  |                 0.481 |             0.652 |         0.474 |        311 |             0.669 |             0.026 |          0.18  |      0.283 |

## Cochran's Q (omnibus across conditions, per model)

| model                      |   n_items |   k_conditions |       Q |   df |      p |
|:---------------------------|----------:|---------------:|--------:|-----:|-------:|
| deepseek/deepseek-v4-flash |       600 |              3 | 11.3765 |    2 | 0.0034 |
| google/gemma-4-26b-a4b-it  |       600 |              3 |  9.95   |    2 | 0.0069 |

## Pairwise McNemar (Holm-corrected, exact-category correctness)

| model                      | comparison                 | a      | b       |   acc_a |   acc_b |   delta(b-a) |   b_fixed |   a_kept(b_broke) |   discordant |   statistic |   p_raw |   p_holm | sig_.05   |
|:---------------------------|:---------------------------|:-------|:--------|--------:|--------:|-------------:|----------:|------------------:|-------------:|------------:|--------:|---------:|:----------|
| deepseek/deepseek-v4-flash | context: BASE vs WINDOW    | BASE   | WINDOW  |  0.3967 |  0.4417 |       0.045  |        67 |                40 |          107 |      6.3178 |  0.012  |   0.0239 | True      |
| deepseek/deepseek-v4-flash | context: WINDOW vs FULLDOC | WINDOW | FULLDOC |  0.4417 |  0.4533 |       0.0117 |        59 |                52 |          111 |      0.3243 |  0.569  |   0.569  | False     |
| deepseek/deepseek-v4-flash | context: BASE vs FULLDOC   | BASE   | FULLDOC |  0.3967 |  0.4533 |       0.0567 |        78 |                44 |          122 |      8.9262 |  0.0028 |   0.0084 | True      |
| google/gemma-4-26b-a4b-it  | context: BASE vs WINDOW    | BASE   | WINDOW  |  0.43   |  0.48   |       0.05   |        65 |                35 |          100 |      8.41   |  0.0037 |   0.0112 | True      |
| google/gemma-4-26b-a4b-it  | context: WINDOW vs FULLDOC | WINDOW | FULLDOC |  0.48   |  0.4367 |      -0.0433 |        33 |                59 |           92 |      6.7935 |  0.0091 |   0.0183 | True      |
| google/gemma-4-26b-a4b-it  | context: BASE vs FULLDOC   | BASE   | FULLDOC |  0.43   |  0.4367 |       0.0067 |        66 |                62 |          128 |      0.0703 |  0.7909 |   0.7909 | False     |

## Direction consistency across models

`b>a` = how many models scored the second condition higher. An effect you trust shows the same direction across most models *and* significance.

| comparison                 |   models |   b>a |   b<a |   significant(Holm) |
|:---------------------------|---------:|------:|------:|--------------------:|
| context: BASE vs FULLDOC   |        2 |     2 |     0 |                   1 |
| context: BASE vs WINDOW    |        2 |     2 |     0 |                   2 |
| context: WINDOW vs FULLDOC |        2 |     1 |     1 |                   1 |
