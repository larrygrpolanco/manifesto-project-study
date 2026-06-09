# Manifesto Project Study

Research on task decomposition (hierarchical vs. flat prompting) and the
*structure* of LLM classification errors on the Manifesto Project coding scheme.
See [docs/](docs/) for the working draft and planning notes.

## Layout

```
data/          # gitignored — not in version control (large / raw)
  raw/         # original downloads: pilot dataset (csv/rds), MPDS documents
  codebook/    # codebook source files (xlsx, category csv)
  subsets/     # derived subsets, e.g. by_language/ (one csv per language)
code/
  R/           # data download + pilot prep (manifestoR)
  python/      # dataset subsetting and (later) experiment code
docs/          # paper draft, planning documents
literature/    # reference PDFs
```

`data/` is intentionally excluded from git — the raw pilot dataset alone is
~750 MB. Regenerate it locally (see below) or drop the files into `data/raw/`.

## Setup

### API key
Data download uses the Manifesto Project API. Get a key from
<https://manifesto-project.wzb.eu/> and place it in a gitignored file:

```bash
cp code/R/manifesto_apikey.txt.example code/R/manifesto_apikey.txt
# then paste your key into code/R/manifesto_apikey.txt
```

### Download / prep the data (R)
```bash
cd code/R && Rscript manifesto-pilot-data.R
```

### Subset the dataset by language (Python)
```bash
python3 code/python/split_by_language.py
# options:
python3 code/python/split_by_language.py --languages english spanish german
python3 code/python/split_by_language.py --input data/raw/manifesto-pilot-dataset.csv --outdir data/subsets/by_language
```
