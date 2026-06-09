"""Central configuration for pilot-1.

Everything that changes between runs lives here: which input sample to score,
which models to call, which conditions to test, and run parameters. The scripts
in src/ import this module; nothing else hard-codes paths or model names.

To run a *different* sample, point INPUT_CSV at another file and (if its columns
differ) adjust the COLUMNS mapping. The codebook, conditions, and eval logic stay
the same. This is why the pilot works on the 300-row dev set today and on a much
larger sample tomorrow with a one-line change.
"""

from pathlib import Path

# --- Paths ------------------------------------------------------------------
# All paths are resolved relative to this file so the pilot is location-independent.
PILOT_DIR = Path(__file__).resolve().parent
DATA_DIR = PILOT_DIR / "data"
RESULTS_DIR = PILOT_DIR / "results"
RAW_DIR = RESULTS_DIR / "raw"            # cached raw API responses (gitignored)
REPORTS_DIR = PILOT_DIR / "reports"      # human-facing tables/figures (tracked)

INPUT_CSV = DATA_DIR / "dev_set.csv"     # <- swap this to score a different sample
CODEBOOK_CSV = DATA_DIR / "codebook.csv"
VALENCE_PAIRS_CSV = DATA_DIR / "valence_pairs.csv"

PREDICTIONS_CSV = RESULTS_DIR / "predictions.csv"   # parsed, tidy, one row per call

# --- Input column mapping ---------------------------------------------------
# Logical name -> column in INPUT_CSV. Only TEXT and GOLD_CODE are required;
# the gold domain is always derived from the gold code via the codebook, so any
# CSV with a text column and a Manifesto main-code column will work.
COLUMNS = {
    "text": "text",
    "gold_code": "main_code",
}
# Columns combined (in order) to form a stable per-row id. If any are missing,
# the row index is used instead. (manifesto_id + pos is unique per quasi-sentence.)
ID_COLUMNS = ["manifesto_id", "pos"]

# --- Label space ------------------------------------------------------------
# The model chooses among the 56 substantive categories plus 000 ("no other
# category applies"). 000 never appears as a gold label, so any 000 prediction
# scores as wrong -- but is tracked as over-abstention (error type E5).
INCLUDE_UNCODED = True
UNCODED_CODE = "000"

# Documented catch-all / generic categories (error type E5: catch-all absorption).
CATCH_ALL_CODES = {"000", "408", "303", "305", "705", "706"}

# --- Models (Groq) ----------------------------------------------------------
# Exact Groq model IDs. Edit freely; the pipeline loops over whatever is listed.
MODELS = [
    "llama-3.1-8b-instant",
    "openai/gpt-oss-20b",
    "qwen/qwen3-32b",
    "llama-3.3-70b-versatile",
    "openai/gpt-oss-120b",
]

# --- Conditions -------------------------------------------------------------
# Four conditions. Information axis: LABELS vs FULL. Structure axis (at full
# information): FULL vs HIER1 vs HIER2. Each comparison changes exactly one thing.
CONDITIONS = ["LABELS", "FULL", "HIER1", "HIER2"]

# Pairwise comparisons the significance tests focus on (label, a, b).
COMPARISONS = [
    ("info: LABELS vs FULL", "LABELS", "FULL"),
    ("structure: FULL vs HIER1", "FULL", "HIER1"),
    ("structure: FULL vs HIER2", "FULL", "HIER2"),
    ("structure: HIER1 vs HIER2", "HIER1", "HIER2"),
]

# --- Run parameters ---------------------------------------------------------
TEMPERATURE = 0.0          # prior work (Grullon-Polanco 2026): T=0 maximizes reliability
MAX_TOKENS = 512           # generous; reasoning models (qwen3) may emit more before the JSON
MAX_RETRIES = 4            # transient API error / rate-limit retries (exponential backoff)
CONCURRENCY = 8            # parallel in-flight requests per (model, condition)
SEED = 0                   # passed to the API where supported; also fixes any sampling here
