# Dataset profile — `dev_set.csv`

- **Items:** 300
- **Categories present:** 39 / 56 substantive (+ uncoded option not used in gold)
- **Text length (whitespace tokens):** median 15, mean 16.3, min 2, max 52

## Domain distribution

| Domain | Items | % |
|---|---:|---:|
| Economy | 69 | 23.0 |
| Welfare and Quality of Life | 66 | 22.0 |
| Fabric of Society | 65 | 21.7 |
| Political System | 52 | 17.3 |
| External Relations | 25 | 8.3 |
| Social Groups | 15 | 5.0 |
| Freedom and Democracy | 8 | 2.7 |

## Class imbalance

- Per-category counts (present only): min 1, median 4, max 46
- Categories with a single example: 12
- **Most frequent:** 305 (46), 601 (36), 503 (30), 504 (20), 410 (15), 506 (14), 110 (14), 605 (13)

## Most frequent categories

| Code | Title | Count | % |
|---|---|---:|---:|
| 305 | Political Authority | 46 | 15.3 |
| 601 | National Way of Life: Positive | 36 | 12.0 |
| 503 | Equality: Positive | 30 | 10.0 |
| 504 | Welfare State Expansion | 20 | 6.7 |
| 410 | Economic Growth: Positive | 15 | 5.0 |
| 506 | Education Expansion | 14 | 4.7 |
| 110 | European Community/Union: Negative | 14 | 4.7 |
| 605 | Law and Order: Positive | 13 | 4.3 |
| 403 | Market Regulation | 12 | 4.0 |
| 408 | Economic Goals | 11 | 3.7 |
| 607 | Multiculturalism: Positive | 9 | 3.0 |
| 701 | Labour Groups: Positive | 9 | 3.0 |

## Absent substantive categories (17)

101 Foreign Special Relationships: Positive, 102 Foreign Special Relationships: Negative, 103 Anti-Imperialism, 109 Internationalism: Negative, 203 Constitutionalism: Positive, 204 Constitutionalism: Negative, 302 Centralisation, 304 Political Corruption, 409 Keynesian Demand Management, 502 Culture: Positive, 507 Education Limitation, 602 National Way of Life: Negative, 604 Traditional Morality: Negative, 608 Multiculturalism: Negative, 702 Labour Groups: Negative, 703 Agriculture and Farmers: Positive, 705 Underprivileged Minority Groups

## Valence-pair representation (error type E2)

Both members must appear for a valence *flip* to be observable.

| Pair | + code (n) | − code (n) | flip observable? |
|---|---|---|:--:|
| Foreign Special Relationships | 101 (0) | 102 (0) | no |
| Military | 104 (4) | 105 (1) | yes |
| European Community/Union | 108 (1) | 110 (14) | yes |
| Constitutionalism | 203 (0) | 204 (0) | no |
| Protectionism | 406 (3) | 407 (2) | yes |
| Welfare State | 504 (20) | 505 (1) | yes |
| Education | 506 (14) | 507 (0) | no |
| National Way of Life | 601 (36) | 602 (0) | no |
| Traditional Morality | 603 (3) | 604 (0) | no |
| Multiculturalism | 607 (9) | 608 (0) | no |
| Labour Groups | 701 (9) | 702 (0) | no |

## Catch-all categories (error type E5)

Catch-all codes: ['000', '303', '305', '408', '705', '706']. Gold items sitting in a catch-all category: 59 (19.7%). Note 000 never appears in gold, so any 000 prediction is over-abstention.

## Power note

Condition comparisons are paired McNemar tests over 300 items. McNemar's power depends only on the *discordant* pairs (items where two conditions disagree). Rough guide at n=300, α=.05, power≈.8: you can detect a difference if roughly ≥25–35 items flip net one way. Per-*category* effects will be underpowered (12 categories have a single example); the well-powered tests are on **overall accuracy and compliance** per condition.
