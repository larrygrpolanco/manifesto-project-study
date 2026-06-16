"""Central configuration for the pilot.

Single source of truth for paths, model roster, run parameters, and the frozen
selection rule. Every other module imports from here; nothing else hard-codes a
path or a model slug.

Design is LOCKED (PILOT_PLAN.md §"Locked decisions"). The two parameters that
matter most for run independence are pinned here and must not drift:

    TEMPERATURE = 1.0   we need a *spread* to measure; temp-1 is where spread lives.
    SEED        = None  the 10 runs MUST vary (opposite of pilot-2, which fixed a seed).

Key in repo-root .env as OPENROUTER_API_KEY; base https://openrouter.ai/api/v1.
"""

import json
import os
from pathlib import Path

# --- Paths (resolved relative to this file: src/pilot/config.py) ------------
ROOT = Path(__file__).resolve().parents[2]          # repo root
DATA_DIR = ROOT / "data"
HUMAN_DIR = ROOT / "reports" / "human"
PROMPTS_DIR = ROOT / "src" / "prompts"

RUNS_DIR = ROOT / "runs" / "pilot"                  # machine artefacts
REPORTS_DIR = ROOT / "reports" / "pilot"            # human-facing tables/figures
RAW_DIR = RUNS_DIR / "raw"                          # per-config JSONL caches (resumable)

# Inputs (Step 0, on disk + validated).
CATEGORIES_JSON = DATA_DIR / "categories.json"
SAMPLE_JSON = DATA_DIR / "cmp_coding_sample.json"
AMBIGUITY_CSV = HUMAN_DIR / "per_sentence_ambiguity.csv"
HUMAN_CODINGS_CSV = HUMAN_DIR / "human_codings.csv"
CODERS_CSV = HUMAN_DIR / "coders.csv"
INSTRUMENT_MD = PROMPTS_DIR / "coding_instrument.md"

# Outputs.
SENTENCE_MANIFEST = RUNS_DIR / "sentence_manifest.csv"
RUN_GRID_JSON = RUNS_DIR / "run_grid.json"
PREDICTIONS_CSV = RUNS_DIR / "predictions.csv"

# --- Models (all 8; FAIL LOUD — any unreachable ID halts the probe) ---------
MODELS = [
    "deepseek/deepseek-v4-flash",
    "deepseek/deepseek-v4-pro",
    "qwen/qwen3.6-35b-a3b",
    "qwen/qwen3.6-plus",
    "google/gemma-4-26b-a4b-it",
    "google/gemma-4-31b-it",
    "anthropic/claude-3.5-haiku",
    "anthropic/claude-haiku-4.5",
]

# --- Run parameters (LOCKED) ------------------------------------------------
N_RUNS = 10                 # runs per (config x sentence); subsampled 10->5->3 in analysis
TEMPERATURE = 1.0           # spread lives here; do NOT lower
SEED = None                 # NO fixed seed — the 10 runs must vary
MAX_TOKENS = 2048           # room for reasoning traces before the bare code
MAX_RETRIES = 5             # transient API error / rate-limit retries (exponential backoff)
CONCURRENCY = 12            # parallel in-flight requests per config

# --- Output contract --------------------------------------------------------
# Ask for the bare 3-digit code. Strip <think> -> regex-extract -> validate
# against the 57 codes. Off-scheme / refusal / multi-code outputs are logged raw
# and counted as their own bucket in the spread (mirrors human 000/off-gold),
# never silently dropped.
UNCODED_CODE = "000"

# --- Sentence selection (FROZEN, no tunable knobs) --------------------------
# Rank all 179 by RANK_COLUMN (000 kept as a class). High-split = top BUCKET_N,
# mid-split = BUCKET_N around the median, high-agreement = bottom BUCKET_N.
RANK_COLUMN = "full_class_cat_1mmodal"
BUCKET_N = 10

# Balanced-RILE coin-flips: rile votes span all three classes (left/right/none)
# AND no single RILE class dominates ("no class > ~40%"). The "~40%" in the plan
# is operationalised as the explicit threshold below. select_sentences.py PRINTS
# how many cases this yields and which they are — the count is REPORTED, never
# silently tuned to a target. With the Step-0 data this yields exactly the 4
# cases the plan names (NZ-022, NZ-007, NZ-023, NZ-044); if the data or threshold
# changes and the count moves off 4, the script says so loudly.
BALANCED_RILE_DISTINCT = 3
# "No RILE class larger than ~43.5% of votes." The count of balanced cases is
# razor-sensitive at this cliff (<=0.40 -> 1 case; <=0.435 -> 4; <=0.4375 -> 6).
# 0.435 is the chosen operationalization of the plan's "~40%": it yields exactly
# the 4 cases the plan names (NZ-022, NZ-007, NZ-023, NZ-044). This is a frozen
# design decision, recorded here so the choice is explicit rather than buried.
BALANCED_RILE_MAX_MODAL_SHARE = 0.435

# Columns carried into the manifest for downstream analysis (both pools kept).
MANIFEST_METRIC_COLUMNS = [
    "full_class_n", "full_class_cat_distinct", "full_class_cat_modal_share",
    "full_class_cat_1mmodal", "full_class_cat_Hnorm",
    "full_class_rile_distinct", "full_class_rile_1mmodal", "full_class_rile_modal",
    "retained_class_n", "retained_class_cat_distinct", "retained_class_cat_modal_share",
    "retained_class_cat_1mmodal", "retained_class_cat_Hnorm",
    "retained_class_rile_distinct", "retained_class_rile_1mmodal", "retained_class_rile_modal",
]

# --- API (OpenRouter) -------------------------------------------------------
API_BASE_URL = "https://openrouter.ai/api/v1"
API_KEY_ENV = "OPENROUTER_API_KEY"


def load_dotenv():
    """Populate os.environ from the repo-root .env (does not overwrite existing)."""
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))


def make_client():
    """Construct the OpenRouter client (OpenAI-compatible). Fails loud if no key."""
    load_dotenv()
    api_key = os.environ.get(API_KEY_ENV)
    if not api_key:
        raise SystemExit(
            f"{API_KEY_ENV} is not set (add it to {ROOT/'.env'}) and retry."
        )
    from openai import OpenAI
    return OpenAI(base_url=API_BASE_URL, api_key=api_key)


def allowed_codes():
    """The 57 valid codes (56 standard + 000), from categories.json."""
    cats = json.loads(CATEGORIES_JSON.read_text())["categories"]
    return set(cats.keys())
