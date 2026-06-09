"""Run the classification experiment: every model x condition x item.

Calls the Groq API at temperature 0 in JSON mode. Results are cached per
(model, condition) as JSONL in results/raw/, so the run is resumable -- rerunning
skips items already cached and only calls the API for what's missing. After all
calls, a tidy results/predictions.csv is rebuilt from the cache for evaluation.

    export GROQ_API_KEY=...
    python src/run_experiment.py                     # full sweep
    python src/run_experiment.py --limit 5           # smoke test: first 5 items
    python src/run_experiment.py --models llama-3.1-8b-instant --conditions LABELS FULL
    python src/run_experiment.py --input ../some_other_sample.csv

HIER2 uses two calls (pick domain, then pick category within it); all other
conditions use one. Compliance = a valid in-scheme code was recovered.
"""

import argparse
import csv
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

import config
from codebook import load_codebook
from dataset import load_items
import prompts


# --- output parsing ---------------------------------------------------------
_THINK = re.compile(r"<think>.*?</think>", re.S | re.I)
_OBJ = re.compile(r"\{.*\}", re.S)


def _parse_json(text):
    if not text:
        return None
    text = _THINK.sub("", text).strip()
    for candidate in (text, (_OBJ.search(text) or [None]) and _OBJ.search(text)):
        if not candidate:
            continue
        raw = candidate if isinstance(candidate, str) else candidate.group()
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            continue
    return None


def _code_in(cand, allowed):
    cand = str(cand).strip()
    if cand in allowed:
        return cand
    m = re.search(r"\d{3}", cand)
    return m.group() if m and m.group() in allowed else None


def parse_code(text, allowed):
    """Return a valid in-scheme code or None (non-compliant).

    Trusts a parseable JSON object's "code" key. Only if NO JSON parsed at all
    does it fall back to scanning the raw text -- so a valid-but-wrong-shaped JSON
    counts as non-compliant rather than being mined for a stray number.
    """
    obj = _parse_json(text)
    if isinstance(obj, dict):
        return _code_in(obj["code"], allowed) if "code" in obj else None
    if text:  # no JSON parsed: lenient fallback to a 3-digit token
        m = re.search(r"\b\d{3}\b", _THINK.sub("", text))
        if m and m.group() in allowed:
            return m.group()
    return None


def parse_domain(text, domain_codes):
    obj = _parse_json(text)
    if isinstance(obj, dict):
        if "domain" not in obj:
            return None
        try:
            d = int(str(obj["domain"]).strip())
            return d if d in domain_codes else None
        except ValueError:
            return None
    if text:  # no JSON parsed: lenient fallback
        for tok in re.findall(r"-?\d+", _THINK.sub("", text)):
            if int(tok) in domain_codes:
                return int(tok)
    return None


# --- API call with retry ----------------------------------------------------
def call(client, model, messages):
    last = None
    for attempt in range(config.MAX_RETRIES):
        try:
            kwargs = dict(model=model, messages=messages,
                          temperature=config.TEMPERATURE, max_tokens=config.MAX_TOKENS,
                          response_format={"type": "json_object"})
            try:
                kwargs["seed"] = config.SEED
                resp = client.chat.completions.create(**kwargs)
            except Exception:
                kwargs.pop("seed", None)              # some models reject seed
                resp = client.chat.completions.create(**kwargs)
            return resp.choices[0].message.content or ""
        except Exception as e:  # transient: rate limit / 5xx / json_format unsupported
            last = e
            msg = str(e).lower()
            if "response_format" in msg or "json" in msg:
                # retry once without JSON mode (rely on lenient parsing)
                try:
                    resp = client.chat.completions.create(
                        model=model, messages=messages,
                        temperature=config.TEMPERATURE, max_tokens=config.MAX_TOKENS)
                    return resp.choices[0].message.content or ""
                except Exception as e2:
                    last = e2
            time.sleep(min(2 ** attempt, 30))
    raise last


def classify(client, model, condition, item, cb, domain_codes):
    """Run one item through one condition; return a result record (dict)."""
    rec = {"model": model, "condition": condition, "item_id": item.id,
           "gold_code": item.gold_code, "gold_domain_code": item.gold_domain_code,
           "pred_code": None, "pred_domain_code": None, "stage1_domain": None,
           "compliant": False, "raw1": "", "raw2": "", "error": ""}
    try:
        if condition == "HIER2":
            raw1 = call(client, model, prompts.build_hier2_stage1_messages(item, cb))
            rec["raw1"] = raw1
            d = parse_domain(raw1, domain_codes)
            rec["stage1_domain"] = d
            if d is None:
                return rec  # non-compliant at stage 1; no category
            raw2 = call(client, model, prompts.build_hier2_stage2_messages(item, cb, d))
            rec["raw2"] = raw2
            code = parse_code(raw2, cb.allowed_codes)
        else:
            raw1 = call(client, model, prompts.build_single_messages(condition, item, cb))
            rec["raw1"] = raw1
            code = parse_code(raw1, cb.allowed_codes)
        if code is not None:
            rec["pred_code"] = code
            rec["pred_domain_code"] = cb.domain_of(code)[0]
            rec["compliant"] = True
    except Exception as e:
        rec["error"] = f"{type(e).__name__}: {e}"
    return rec


# --- cache + orchestration --------------------------------------------------
def cache_path(model, condition):
    safe = model.replace("/", "__")
    return config.RAW_DIR / f"{safe}__{condition}.jsonl"


def load_done(path):
    done = {}
    if path.exists():
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line:
                    r = json.loads(line)
                    done[r["item_id"]] = r
    return done


def run_cell(client, model, condition, items, cb, domain_codes):
    path = cache_path(model, condition)
    done = load_done(path)
    todo = [it for it in items if it.id not in done]
    if not todo:
        print(f"  {model} / {condition}: {len(done)} cached, nothing to do")
        return list(done.values())
    print(f"  {model} / {condition}: {len(done)} cached, {len(todo)} to run")
    records = list(done.values())
    with open(path, "a") as fh, ThreadPoolExecutor(max_workers=config.CONCURRENCY) as ex:
        futs = {ex.submit(classify, client, model, condition, it, cb, domain_codes): it
                for it in todo}
        for i, fut in enumerate(as_completed(futs), 1):
            rec = fut.result()
            fh.write(json.dumps(rec) + "\n")
            fh.flush()
            records.append(rec)
            if i % 25 == 0 or i == len(todo):
                print(f"    {i}/{len(todo)}")
    return records


PRED_FIELDS = ["model", "condition", "item_id", "gold_code", "gold_domain_code",
               "pred_code", "pred_domain_code", "stage1_domain", "compliant", "error"]


def rebuild_predictions():
    """Rebuild predictions.csv from every cache file on disk (full state)."""
    config.PREDICTIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with open(config.PREDICTIONS_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=PRED_FIELDS)
        w.writeheader()
        for path in sorted(config.RAW_DIR.glob("*.jsonl")):
            for r in load_done(path).values():
                w.writerow({k: r.get(k, "") for k in PRED_FIELDS})
                n += 1
    print(f"wrote {config.PREDICTIONS_CSV} ({n} rows from {config.RAW_DIR})")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", type=Path, default=config.INPUT_CSV)
    ap.add_argument("--models", nargs="+", default=config.MODELS)
    ap.add_argument("--conditions", nargs="+", default=config.CONDITIONS)
    ap.add_argument("--limit", type=int, default=None, help="only first N items (smoke test)")
    args = ap.parse_args()

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        sys.exit("GROQ_API_KEY is not set. `export GROQ_API_KEY=...` and retry.")
    from groq import Groq
    client = Groq(api_key=api_key)

    cb = load_codebook(config.CODEBOOK_CSV, config.VALENCE_PAIRS_CSV)
    domain_codes = {dc for dc, _ in cb.domains}
    items = load_items(args.input, config.COLUMNS, config.ID_COLUMNS, cb)
    if args.limit:
        items = items[:args.limit]
    print(f"{len(items)} items | {len(args.models)} models | {len(args.conditions)} conditions")
    config.RAW_DIR.mkdir(parents=True, exist_ok=True)

    for model in args.models:
        print(model)
        for condition in args.conditions:
            run_cell(client, model, condition, items, cb, domain_codes)
    rebuild_predictions()


if __name__ == "__main__":
    main()
