# Manifesto coding: inter-model consensus vs. human disagreement

A matched, item-level study on CMP/Manifesto coding. The design, narrative, and
open decisions live in **[RESEARCH_PLAN.md](RESEARCH_PLAN.md)** — start there.

Status: human side computed and validated (Step 0 done). LLM pilot is next.

## Layout

```text
data/                     # INPUTS (canonical, read-mostly)
  human/                  #   raw MLB reliability data: codes.log, masters, .dta, R repl
  categories.json         #   the 56-cat + uncoded scheme (domain + RILE map)
  cmp_coding_sample.json  #   179 quasi-sentence unit records (text, gold, section)

src/                      # CODE
  human_profile.py        #   Beat 1: per-sentence entropy, kappa, confusion (DONE)
  prompts/                #   coding_instrument.md — model prompt (instruction-parity)
  onetime/                #   one-shot build scripts (kept for provenance)
                          #   to build: run_llms.py (collect), alignment.py (RQ-A/RQ-B)

runs/                     # LLM COLLECTION OUTPUT (scales with data collection)
  raw/                    #   gitignored: one cached file per API call
  predictions.csv         #   tidy long table; same schema as reports/human/human_codings.csv

reports/                  # ANALYSIS OUTPUTS
  human/                  #   human profile: report + 3 csv tables (DONE)
  llm/                    #   to come

refs/                     # READING (source documents, not code or data)
  handbook/               #   Werner & Volkens 2010 coding instructions (the instrument)
  mlb/                    #   Mikhaylov/Laver/Benoit coder-reliability papers
  literature/             #   LLM-as-coder / manifesto literature

archive/                  # prior pilots and drafts (early-experiment/)
```

## Reproduce the human profile

```sh
python3 src/human_profile.py   # reads data/, writes reports/human/
```
