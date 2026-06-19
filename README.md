# Manifesto coding: inter-model consensus vs. human disagreement

A matched, item-level study on CMP/Manifesto coding. The literature review, design,
narrative, and open decisions all live in the single canonical plan
**[RESEARCH_PLAN.md](RESEARCH_PLAN.md)** — start there.

Status: human side computed and validated (Step 0 done); Pilot 1 run and analyzed
(`reports/pilot/`). Next: harden the parser, build the ~15-model roster, full collection.

Headline (from the pilot, gold-free): on genuinely ambiguous coding, inter-model
(dis)agreement is decoupled from expert disagreement — each model is over-confident on its
own, the models are incoherent with each other (often on codes no expert chose), and model
disagreement does not track human difficulty where it matters.

## Layout

```text
data/                     # INPUTS (canonical, read-mostly)
  human/                  #   raw MLB reliability data: codes.log, masters, .dta, R repl
  categories.json         #   the 56-cat + uncoded scheme (domain + RILE map)
  cmp_coding_sample.json  #   179 quasi-sentence unit records (text, gold, section)

src/                      # CODE
  human_profile.py        #   Step 0: per-sentence entropy, kappa, confusion (DONE)
  pilot/                  #   Pilot 1: select_sentences, prompt, probe_models, run, analyze
  prompts/                #   coding_instrument.md — model prompt (instruction-parity)
                          #   to build: run_llms.py (collect), alignment.py (RQ1/RQ2)

runs/                     # LLM COLLECTION OUTPUT (scales with data collection)
  raw/                    #   gitignored: one cached file per API call
  pilot/                  #   pilot manifest + predictions
  predictions.csv         #   tidy long table; same schema as reports/human/human_codings.csv

reports/                  # ANALYSIS OUTPUTS
  human/                  #   human profile: report + csv tables (DONE)
  pilot/                  #   Pilot 1 results (DONE)
  llm/                    #   full-study results (to come)

refs/                     # READING (source documents, not code or data)
  handbook/               #   Werner & Volkens 2010 coding instructions (the instrument)
  mlb/                    #   Mikhaylov/Laver/Benoit coder-reliability papers
  literature/             #   LLM-as-coder / manifesto literature

archive/                  # prior pilots and superseded plans (incl. pilot-1-plan.md)
```

## Reproduce the human profile

```sh
python3 src/human_profile.py   # reads data/, writes reports/human/
```
