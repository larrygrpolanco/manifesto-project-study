"""Execute the pilot grid: configs x sentences x N_RUNS at temp 1, no seed.

Ported from archive/early-experiment/pilot-2/run_experiment.py: resumable
per-config JSONL cache, threaded worker pool with retry/backoff, <think>-tag
stripping + 3-digit parser. The DESIGN differs from pilot-2 — here we WANT the
runs to vary (temp 1, NO seed), so each of the N_RUNS calls is independent.

Configs come from runs/pilot/run_grid.json (run probe_models.py first).
Sentences come from runs/pilot/sentence_manifest.csv (run select_sentences.py
first). Each call captures: pred_code, raw_text, off_scheme, reasoning_present,
prompt/completion tokens, and logprobs opportunistically. Off-scheme / refusal /
multi-code outputs are logged raw and kept as their own bucket — never dropped.

    python -m src.pilot.run --limit 5     # smoke: cache writes, parser, resume
    python -m src.pilot.run               # full run
"""

import argparse
import csv
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from . import config
from .codebook import load_codebook
from .prompt import Corpus, build_messages

# --- output parsing ---------------------------------------------------------
_THINK = re.compile(r"<think>.*?</think>", re.S | re.I)


def parse_code(text, allowed):
    """Return a valid in-scheme 3-digit code, or None (off-scheme).

    Strips <think> traces, then: an exact bare code wins; otherwise take the LAST
    valid 3-digit token (a reasoning leak puts the final answer last). None means
    off-scheme — logged raw and counted as its own bucket, not silently dropped.
    """
    if not text:
        return None
    cleaned = _THINK.sub("", text).strip()
    if cleaned in allowed:
        return cleaned
    valid = [t for t in re.findall(r"\d{3}", cleaned) if t in allowed]
    return valid[-1] if valid else None


# --- API call with retry/backoff -------------------------------------------
def call(client, model, messages, reasoning_param):
    """One API call at temp 1 (no seed). Returns the raw response object. Retries transient errors."""
    base = dict(model=model, messages=messages, temperature=config.TEMPERATURE,
                max_tokens=config.MAX_TOKENS)
    extra = {"reasoning": reasoning_param} if reasoning_param is not None else None
    last = None
    for attempt in range(config.MAX_RETRIES):
        try:
            kwargs = dict(base)
            if extra:
                kwargs["extra_body"] = extra
            try:                                    # logprobs is a bonus; drop it if rejected
                kwargs["logprobs"] = True
                return client.chat.completions.create(**kwargs)
            except Exception:
                kwargs.pop("logprobs", None)
                return client.chat.completions.create(**kwargs)
        except Exception as e:
            last = e
            time.sleep(min(2 ** attempt, 30))
    raise last


def _reasoning_present(resp):
    msg = resp.choices[0].message
    for attr in ("reasoning", "reasoning_details"):
        if getattr(msg, attr, None):
            return True
    extra = getattr(msg, "model_extra", None) or {}
    return bool(extra.get("reasoning") or extra.get("reasoning_details"))


def _logprobs_obj(resp):
    lp = getattr(resp.choices[0], "logprobs", None)
    if not lp:
        return None
    try:
        return lp.model_dump() if hasattr(lp, "model_dump") else None
    except Exception:
        return None


def classify(client, cfg, sentence, run_idx, messages, allowed):
    """Run one (sentence, run_idx) through one config; return a cache record."""
    rec = {"config_id": cfg["config_id"], "model": cfg["model"],
           "reasoning_mode": cfg["reasoning_mode"], "capability": cfg["capability"],
           "unit_id": sentence["unit_id"], "run_idx": run_idx,
           "manifesto": sentence["manifesto"], "bucket": sentence["bucket"],
           "master_code": sentence["master_code"],
           "pred_code": None, "raw_text": "", "off_scheme": True,
           "reasoning_present": False, "prompt_tokens": None,
           "completion_tokens": None, "has_logprobs": False,
           "logprobs": None, "error": ""}
    try:
        resp = call(client, cfg["model"], messages, cfg["reasoning_param"])
        raw = resp.choices[0].message.content or ""
        rec["raw_text"] = raw
        code = parse_code(raw, allowed)
        rec["pred_code"] = code
        rec["off_scheme"] = code is None
        rec["reasoning_present"] = _reasoning_present(resp)
        usage = getattr(resp, "usage", None)
        if usage:
            rec["prompt_tokens"] = getattr(usage, "prompt_tokens", None)
            rec["completion_tokens"] = getattr(usage, "completion_tokens", None)
        lp = _logprobs_obj(resp)
        if lp:
            rec["has_logprobs"] = True
            rec["logprobs"] = lp
    except Exception as e:
        rec["error"] = f"{type(e).__name__}: {e}"
    return rec


# --- cache + orchestration --------------------------------------------------
def cache_path(config_id):
    return config.RAW_DIR / f"{config_id}.jsonl"


def _key(unit_id, run_idx):
    return f"{unit_id}#{run_idx}"


def load_done(path):
    done = {}
    if path.exists():
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line:
                    r = json.loads(line)
                    done[_key(r["unit_id"], r["run_idx"])] = r
    return done


def run_config(client, cfg, sentences, allowed, corpus, codebook):
    path = cache_path(cfg["config_id"])
    done = load_done(path)
    # Pre-render each sentence's prompt once (identical across the N_RUNS).
    todo = [(s, i) for s in sentences for i in range(config.N_RUNS)
            if _key(s["unit_id"], i) not in done]
    if not todo:
        print(f"  {cfg['config_id']}: {len(done)} cached, nothing to do")
        return
    print(f"  {cfg['config_id']}: {len(done)} cached, {len(todo)} to run")
    msg_cache = {}

    def messages_for(unit_id):
        if unit_id not in msg_cache:
            msg_cache[unit_id] = build_messages(unit_id, codebook, corpus)
        return msg_cache[unit_id]

    with open(path, "a") as fh, \
            ThreadPoolExecutor(max_workers=config.CONCURRENCY) as ex:
        futs = {ex.submit(classify, client, cfg, s, i,
                          messages_for(s["unit_id"]), allowed): (s, i)
                for s, i in todo}
        for n, fut in enumerate(as_completed(futs), 1):
            rec = fut.result()
            fh.write(json.dumps(rec) + "\n")
            fh.flush()
            if n % 25 == 0 or n == len(todo):
                print(f"    {n}/{len(todo)}")


# tidy predictions.csv: one row per call, logprobs kept only in the JSONL cache.
PRED_FIELDS = ["config_id", "model", "reasoning_mode", "capability", "unit_id",
               "manifesto", "bucket", "run_idx", "master_code", "pred_code",
               "off_scheme", "reasoning_present", "prompt_tokens",
               "completion_tokens", "has_logprobs", "error"]


def rebuild_predictions():
    config.PREDICTIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with open(config.PREDICTIONS_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=PRED_FIELDS)
        w.writeheader()
        for path in sorted(config.RAW_DIR.glob("*.jsonl")):
            for r in load_done(path).values():
                w.writerow({k: r.get(k, "") for k in PRED_FIELDS})
                n += 1
    print(f"wrote {config.PREDICTIONS_CSV} ({n} rows)")


def load_sentences():
    if not config.SENTENCE_MANIFEST.exists():
        sys.exit("No sentence_manifest.csv — run `python -m src.pilot.select_sentences` first.")
    with open(config.SENTENCE_MANIFEST, newline="") as f:
        return list(csv.DictReader(f))


def load_grid():
    if not config.RUN_GRID_JSON.exists():
        sys.exit("No run_grid.json — run `python -m src.pilot.probe_models` first.")
    return json.loads(config.RUN_GRID_JSON.read_text())["configs"]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--limit", type=int, default=None,
                    help="only first N sentences (smoke test)")
    ap.add_argument("--configs", nargs="+", default=None,
                    help="restrict to these config_ids")
    args = ap.parse_args()

    sentences = load_sentences()
    if args.limit:
        sentences = sentences[:args.limit]
    configs = load_grid()
    if args.configs:
        configs = [c for c in configs if c["config_id"] in set(args.configs)]
        if not configs:
            sys.exit("no matching config_ids in run_grid.json")

    client = config.make_client()
    allowed = config.allowed_codes()
    codebook = load_codebook()
    corpus = Corpus()
    config.RAW_DIR.mkdir(parents=True, exist_ok=True)

    total = len(configs) * len(sentences) * config.N_RUNS
    print(f"{len(configs)} configs x {len(sentences)} sentences x {config.N_RUNS} "
          f"runs = {total} calls (temp={config.TEMPERATURE}, seed={config.SEED})")
    for cfg in configs:
        print(cfg["config_id"])
        run_config(client, cfg, sentences, allowed, corpus, codebook)
    rebuild_predictions()


if __name__ == "__main__":
    main()
