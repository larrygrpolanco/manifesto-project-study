# Dataset profile — `manifesto-pilot-dataset_english_dev-train-4x3.csv`

- **Items:** 600
- **Categories present:** 49 / 56 substantive (+ uncoded option not used in gold)
- **Text length (whitespace tokens):** median 17, mean 17.9, min 2, max 68

## Domain distribution

| Domain | Items | % |
|---|---:|---:|
| Welfare and Quality of Life | 148 | 24.7 |
| Economy | 144 | 24.0 |
| Fabric of Society | 90 | 15.0 |
| External Relations | 81 | 13.5 |
| Social Groups | 52 | 8.7 |
| Political System | 49 | 8.2 |
| Freedom and Democracy | 36 | 6.0 |

## Class imbalance

- Per-category counts (present only): min 1, median 9, max 45
- Categories with a single example: 5
- **Most frequent:** 504 (45), 503 (39), 411 (36), 605 (36), 403 (32), 506 (30), 104 (26), 601 (23)

## Most frequent categories

| Code | Title | Count | % |
|---|---|---:|---:|
| 504 | Welfare State Expansion | 45 | 7.5 |
| 503 | Equality: Positive | 39 | 6.5 |
| 411 | Technology and Infrastructure: Positive | 36 | 6.0 |
| 605 | Law and Order: Positive | 36 | 6.0 |
| 403 | Market Regulation | 32 | 5.3 |
| 506 | Education Expansion | 30 | 5.0 |
| 104 | Military: Positive | 26 | 4.3 |
| 601 | National Way of Life: Positive | 23 | 3.8 |
| 501 | Environmental Protection | 21 | 3.5 |
| 202 | Democracy | 21 | 3.5 |
| 107 | Internationalism: Positive | 20 | 3.3 |
| 305 | Political Authority | 18 | 3.0 |

## Absent substantive categories (7)

103 Anti-Imperialism, 204 Constitutionalism: Negative, 302 Centralisation, 409 Keynesian Demand Management, 413 Nationalisation, 415 Marxist Analysis, 507 Education Limitation

## Valence-pair representation (error type E2)

Both members must appear for a valence *flip* to be observable.

| Pair | + code (n) | − code (n) | flip observable? |
|---|---|---|:--:|
| Foreign Special Relationships | 101 (10) | 102 (3) | yes |
| Military | 104 (26) | 105 (3) | yes |
| European Community/Union | 108 (2) | 110 (10) | yes |
| Constitutionalism | 203 (6) | 204 (0) | no |
| Protectionism | 406 (2) | 407 (1) | yes |
| Welfare State | 504 (45) | 505 (6) | yes |
| Education | 506 (30) | 507 (0) | no |
| National Way of Life | 601 (23) | 602 (1) | yes |
| Traditional Morality | 603 (11) | 604 (1) | yes |
| Multiculturalism | 607 (9) | 608 (3) | yes |
| Labour Groups | 701 (16) | 702 (1) | yes |

## Catch-all categories (error type E5)

Catch-all codes: ['000', '303', '305', '408', '705', '706']. Gold items sitting in a catch-all category: 67 (11.2%). Note 000 never appears in gold, so any 000 prediction is over-abstention.

## Power note

Condition comparisons are paired McNemar tests over 600 items. McNemar's power depends only on the *discordant* pairs (items where two conditions disagree). Rough guide at n=600, α=.05, power≈.8: you can detect a difference if roughly ≥25–35 items flip net one way. Per-*category* effects will be underpowered (5 categories have a single example); the well-powered tests are on **overall accuracy and compliance** per condition.
