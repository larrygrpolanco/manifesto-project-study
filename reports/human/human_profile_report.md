# Step 0 — Human ambiguity profile & danger-cell count

_No API. Computed from the MLB reliability logs on disk._

- Units: 179 (GB 107 + NZ 72). Coders: GB 32 full / 17 retained; NZ 23 full / 12 retained.
- Verification vectors and master↔JSON gold: **passed**.

## Parsing validation against MLB published statistics

If these reproduce the paper, the parse is end-to-end correct.

| statistic | GB | NZ | combined | MLB reported |
|---|---|---|---|---|
| Fleiss κ (category, full pool) | 0.267 | 0.266 | — | GB .35 / NZ .40–.47 |
| Fleiss κ (category, retained) | 0.349 | 0.397 | — | (retained set) |
| median coder-vs-master Cohen κ (retained) | 0.429 | 0.536 | 0.459 | GB .43 / NZ .54 / comb .46 |
| median coder-vs-master Cohen κ (full pool) | 0.377 | 0.459 | 0.406 | — |

## The danger-cell count: how many sentences are human-split?

Counts of the 179 sentences exceeding each disagreement threshold, at **category** granularity. `1−modal share` = fraction of coders NOT on the top code (≥.50 ⇒ no majority code).

| combo | ≥2 codes | ≥3 codes | 1−modal≥.40 | 1−modal≥.50 | 1−modal≥.60 | Hnorm≥.50 |
|---|--:|--:|--:|--:|--:|--:|
| full / 000-class | 179 | 175 | 132 | 103 | 55 | 53 |
| full / 000-exclude | 179 | 174 | 121 | 97 | 48 | 46 |
| retained / 000-class | 178 | 146 | 102 | 72 | 27 | 43 |
| retained / 000-exclude | 174 | 139 | 95 | 69 | 26 | 43 |

Same, at **RILE 3-class** granularity (the split that actually moves Beat 5). `rile_distinct≥2` = coders disagree on left/right/none; `1−modal≥.50` = no majority RILE class.

| combo | RILE split (≥2 classes) | no RILE majority (1−modal≥.50) |
|---|--:|--:|
| full / 000-class | 178 | 21 |
| full / 000-exclude | 178 | 19 |
| retained / 000-class | 162 | 16 |
| retained / 000-exclude | 158 | 12 |

## Blocking decisions, with the numbers attached

**1. `000`/uncoded handling.** Compare the `000-class` vs `000-exclude` rows above: excluding 000 removes the uncoded votes that concentrate in the most ambiguous sentences, so it *changes* the split count. Plan lean — keep 000 as a class (primary), report exclude as robustness. The grid is computed both ways.

**2. Retained vs full pool.** Compare the `full` vs `retained` rows. Retained uses MLB's exact drop list (no threshold of ours). Plan lean — retained = expert ceiling (primary), full = crowd ceiling (robustness). Both reported.

> Reproduction check: the retained set is **17 GB / 12 NZ**, matching the paper. (`kbenoit` appears in the GB drop list but never coded NZ, so 11 of the 12 NZ drop names match the log — hence 12 retained, not 11.) Retained Fleiss κ and median coder-vs-master Cohen κ reproduce MLB's published values, confirming the parse.
