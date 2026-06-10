# Dataset profile — `dev_set.csv`

- **Items:** 50
- **Categories present:** 15 / 56 substantive (+ uncoded option not used in gold)
- **Text length (whitespace tokens):** median 12, mean 13.9, min 3, max 52

## Domain distribution

| Domain | Items | % |
|---|---:|---:|
| Economy | 16 | 32.0 |
| Fabric of Society | 16 | 32.0 |
| Welfare and Quality of Life | 9 | 18.0 |
| Political System | 5 | 10.0 |
| Social Groups | 3 | 6.0 |
| External Relations | 1 | 2.0 |

## Class imbalance

- Per-category counts (present only): min 1, median 2, max 14
- Categories with a single example: 7
- **Most frequent:** 601 (14), 403 (7), 503 (6), 305 (5), 408 (4), 410 (3), 607 (2), 701 (2)

## Most frequent categories

| Code | Title | Count | % |
|---|---|---:|---:|
| 601 | National Way of Life: Positive | 14 | 28.0 |
| 403 | Market Regulation | 7 | 14.0 |
| 503 | Equality: Positive | 6 | 12.0 |
| 305 | Political Authority | 5 | 10.0 |
| 408 | Economic Goals | 4 | 8.0 |
| 410 | Economic Growth: Positive | 3 | 6.0 |
| 607 | Multiculturalism: Positive | 2 | 4.0 |
| 701 | Labour Groups: Positive | 2 | 4.0 |
| 104 | Military: Positive | 1 | 2.0 |
| 506 | Education Expansion | 1 | 2.0 |
| 704 | Middle Class and Professional Groups | 1 | 2.0 |
| 402 | Incentives: Positive | 1 | 2.0 |

## Absent substantive categories (41)

101 Foreign Special Relationships: Positive, 102 Foreign Special Relationships: Negative, 103 Anti-Imperialism, 105 Military: Negative, 106 Peace, 107 Internationalism: Positive, 108 European Community/Union: Positive, 109 Internationalism: Negative, 110 European Community/Union: Negative, 201 Freedom and Human Rights, 202 Democracy, 203 Constitutionalism: Positive, 204 Constitutionalism: Negative, 301 Decentralization, 302 Centralisation, 303 Governmental and Administrative Efficiency, 304 Political Corruption, 404 Economic Planning, 405 Corporatism/Mixed Economy, 406 Protectionism: Positive, 407 Protectionism: Negative, 409 Keynesian Demand Management, 411 Technology and Infrastructure: Positive, 412 Controlled Economy, 413 Nationalisation, 414 Economic Orthodoxy, 415 Marxist Analysis, 416 Anti-Growth Economy: Positive, 502 Culture: Positive, 505 Welfare State Limitation, 507 Education Limitation, 602 National Way of Life: Negative, 603 Traditional Morality: Positive, 604 Traditional Morality: Negative, 605 Law and Order: Positive, 606 Civic Mindedness: Positive, 608 Multiculturalism: Negative, 702 Labour Groups: Negative, 703 Agriculture and Farmers: Positive, 705 Underprivileged Minority Groups, 706 Non-economic Demographic Groups

## Valence-pair representation (error type E2)

Both members must appear for a valence *flip* to be observable.

| Pair | + code (n) | − code (n) | flip observable? |
|---|---|---|:--:|
| Foreign Special Relationships | 101 (0) | 102 (0) | no |
| Military | 104 (1) | 105 (0) | no |
| European Community/Union | 108 (0) | 110 (0) | no |
| Constitutionalism | 203 (0) | 204 (0) | no |
| Protectionism | 406 (0) | 407 (0) | no |
| Welfare State | 504 (1) | 505 (0) | no |
| Education | 506 (1) | 507 (0) | no |
| National Way of Life | 601 (14) | 602 (0) | no |
| Traditional Morality | 603 (0) | 604 (0) | no |
| Multiculturalism | 607 (2) | 608 (0) | no |
| Labour Groups | 701 (2) | 702 (0) | no |

## Catch-all categories (error type E5)

Catch-all codes: ['000', '303', '305', '408', '705', '706']. Gold items sitting in a catch-all category: 9 (18.0%). Note 000 never appears in gold, so any 000 prediction is over-abstention.

## Power note

Condition comparisons are paired McNemar tests over 50 items. McNemar's power depends only on the *discordant* pairs (items where two conditions disagree). Rough guide at n=50, α=.05, power≈.8: you can detect a difference if roughly ≥25–35 items flip net one way. Per-*category* effects will be underpowered (7 categories have a single example); the well-powered tests are on **overall accuracy and compliance** per condition.
