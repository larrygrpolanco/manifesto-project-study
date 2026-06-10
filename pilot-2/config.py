"""Central configuration for pilot-2.

Everything that changes between runs lives here: which input sample to score,
which models to call, which conditions to test, and run parameters. The scripts
in src/ import this module; nothing else hard-codes paths or model names.

Pilot-2 holds the codebook presentation constant (the HIER1 "by domain" block in
every condition) and manipulates a single variable: how much *document context*
the model sees around the target sentence.
    BASE     target sentence only (this is pilot-1's HIER1).
    WINDOW   the +/- WINDOW_RADIUS neighbouring quasi-sentences as context.
    FULLDOC  the entire manifesto as context.
In every condition the model still assigns exactly one code to the target
sentence; only the surrounding context changes. The input is a large multi-
manifesto corpus, so we score a stratified random sample of N_PER_MANIFESTO
sentences per manifesto (see src/dataset.py) rather than every row.

Calls go through OpenRouter (OpenAI-compatible API); set OPENROUTER_API_KEY.
"""

from pathlib import Path

# --- Paths ------------------------------------------------------------------
# All paths are resolved relative to this file so the pilot is location-independent.
PILOT_DIR = Path(__file__).resolve().parent
DATA_DIR = PILOT_DIR / "data"
RESULTS_DIR = PILOT_DIR / "results"
RAW_DIR = RESULTS_DIR / "raw"            # cached raw API responses (gitignored)
REPORTS_DIR = PILOT_DIR / "reports"      # human-facing tables/figures (tracked)

INPUT_CSV = DATA_DIR / "manifesto-pilot-dataset_english_dev-train-4x3.csv"
CODEBOOK_CSV = DATA_DIR / "codebook.csv"
VALENCE_PAIRS_CSV = DATA_DIR / "valence_pairs.csv"

PREDICTIONS_CSV = RESULTS_DIR / "predictions.csv"   # parsed, tidy, one row per call

# --- Input column mapping ---------------------------------------------------
# Logical name -> column in INPUT_CSV. TEXT and GOLD_CODE are required; the gold
# domain is always derived from the gold code via the codebook. MANIFESTO and POS
# are required in pilot-2 because the context conditions need to reconstruct each
# manifesto in document order and stratified sampling groups by manifesto.
COLUMNS = {
    "text": "text",
    "gold_code": "main_code",
    "manifesto": "manifesto_id",
    "pos": "pos",
}
# Columns combined (in order) to form a stable per-row id. If any are missing,
# the row index is used instead. (manifesto_id + pos is unique per quasi-sentence.)
ID_COLUMNS = ["manifesto_id", "pos"]

# --- Sampling ---------------------------------------------------------------
# The corpus has ~18k rows across 12 manifestos. We score a stratified random
# sample of N_PER_MANIFESTO sentences from each manifesto, stratified by policy
# domain with proportional (largest-remainder) allocation so each manifesto's
# natural domain mix is preserved and small domains are not dropped by chance.
# The same sampled sentences are scored in every model x condition cell; the
# draw is fully determined by SEED, so the sample is reproducible.
N_PER_MANIFESTO = 50
STRATIFY_BY = "domain"        # stratum = gold domain (codebook-derived)
WINDOW_RADIUS = 10            # WINDOW condition: +/- this many neighbouring sentences

# --- Label space ------------------------------------------------------------
# The model chooses among the 56 substantive categories plus 000 ("no other
# category applies"). 000 never appears as a gold label, so any 000 prediction
# scores as wrong -- but is tracked as over-abstention (error type E5).
INCLUDE_UNCODED = True
UNCODED_CODE = "000"

# Documented catch-all / generic categories (error type E5: catch-all absorption).
CATCH_ALL_CODES = {"000", "408", "303", "305", "705", "706"}

# --- Models (OpenRouter) ----------------------------------------------------
# Exact OpenRouter model slugs. Edit freely; the pipeline loops over whatever is
# listed. Both have large context windows (gemma 256k, deepseek 1M), so the
# FULLDOC condition fits even the largest manifesto (~65k tokens).
MODELS = [
    "google/gemma-4-26b-a4b-it",      # paid twin of :free (no daily cap), ~$0.06/M in
    "deepseek/deepseek-v4-flash",     # 1M context, ~$0.10/M in
]

# --- Conditions -------------------------------------------------------------
# Codebook presentation is held constant (the HIER1 "by domain" block) in every
# condition; the only thing that changes is how much surrounding document context
# the model sees for the target sentence.
#   BASE     target sentence alone (== pilot-1's HIER1).
#   WINDOW   +/- WINDOW_RADIUS neighbouring sentences as context.
#   FULLDOC  the entire manifesto as context.
# BASE vs WINDOW isolates local context; WINDOW vs FULLDOC isolates document-wide
# context; BASE vs FULLDOC is the full effect of giving the model the document.
CONDITIONS = ["BASE", "WINDOW", "FULLDOC"]

# Pairwise comparisons the significance tests focus on (label, a, b).
COMPARISONS = [
    ("context: BASE vs WINDOW", "BASE", "WINDOW"),
    ("context: WINDOW vs FULLDOC", "WINDOW", "FULLDOC"),
    ("context: BASE vs FULLDOC", "BASE", "FULLDOC"),
]

# --- Run parameters ---------------------------------------------------------
TEMPERATURE = 0.0          # prior work (Grullon-Polanco 2026): T=0 maximizes reliability
MAX_TOKENS = 512           # generous; leaves room before the JSON answer
MAX_RETRIES = 5            # transient API error / rate-limit retries (exponential backoff)
CONCURRENCY = 16           # parallel in-flight requests per (model, condition)
SEED = 0                   # fixes the sample draw; also passed to the API where supported

# --- API (OpenRouter) -------------------------------------------------------
API_BASE_URL = "https://openrouter.ai/api/v1"
API_KEY_ENV = "OPENROUTER_API_KEY"
