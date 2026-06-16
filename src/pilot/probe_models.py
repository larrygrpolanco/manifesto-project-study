"""Probe every model once: reachability, reasoning capability, logprobs support.

FAIL LOUD (locked decision 2): if any model's base call errors, the probe HALTS
— we do not run a partial roster. For each reachable model it detects whether
reasoning is toggleable / always-on / always-off (by trying enabled and disabled
reasoning and seeing whether a reasoning trace appears/disappears) and whether
the provider returns token logprobs (bonus only).

The emitted run_grid.json is the contract run.py executes: one config per
reasoning mode (toggleable -> two configs, fixed -> one). Report it and SIGN OFF
on the call volume BEFORE the big run.

    python -m src.pilot.probe_models
"""

import json

from . import config

# A tiny, cheap probe prompt — content is irrelevant; we only inspect plumbing.
_PROBE_MESSAGES = [
    {"role": "system", "content": "Reply with a single digit and nothing else."},
    {"role": "user", "content": "Output the digit 7."},
]


def _reasoning_text(resp):
    """Best-effort extraction of any reasoning trace OpenRouter surfaced."""
    msg = resp.choices[0].message
    for attr in ("reasoning", "reasoning_details"):
        val = getattr(msg, attr, None)
        if val:
            return val
    extra = getattr(msg, "model_extra", None) or {}
    return extra.get("reasoning") or extra.get("reasoning_details")


def _one_call(client, model, reasoning_param=None, want_logprobs=False):
    """One probe call. Returns (text, reasoning_present, logprobs_present). Raises on API error."""
    kwargs = dict(model=model, messages=_PROBE_MESSAGES,
                  temperature=config.TEMPERATURE, max_tokens=config.MAX_TOKENS)
    if want_logprobs:
        kwargs["logprobs"] = True
        kwargs["top_logprobs"] = 1
    extra = {}
    if reasoning_param is not None:
        extra["reasoning"] = reasoning_param
    if extra:
        kwargs["extra_body"] = extra
    resp = client.chat.completions.create(**kwargs)
    text = resp.choices[0].message.content or ""
    lp = getattr(resp.choices[0], "logprobs", None)
    logprobs_present = bool(lp and getattr(lp, "content", None))
    return text, bool(_reasoning_text(resp)), logprobs_present


def probe_model(client, model):
    """Probe one model. Raises (fail loud) if the base call is unreachable."""
    # 1. Base reachability + logprobs support. No reasoning param.
    _, base_reasoning, logprobs_supported = _one_call(client, model, want_logprobs=True)

    # 2. Try to turn reasoning ON and OFF. If the provider rejects the param,
    #    the model isn't toggleable through it — fall back to base behaviour.
    on_reasoning = off_reasoning = None
    toggle_supported = True
    try:
        _, on_reasoning, _ = _one_call(client, model, reasoning_param={"enabled": True})
        _, off_reasoning, _ = _one_call(client, model, reasoning_param={"enabled": False})
    except Exception as e:  # provider rejected the reasoning param
        toggle_supported = False
        note = f"reasoning param rejected: {type(e).__name__}"
    else:
        note = ""

    if toggle_supported and on_reasoning and not off_reasoning:
        capability = "toggleable"
    elif base_reasoning or on_reasoning:
        capability = "always_on"
    else:
        capability = "always_off"

    return {
        "reachable": True,
        "capability": capability,
        "logprobs_supported": logprobs_supported,
        "base_reasoning": base_reasoning,
        "on_reasoning": on_reasoning,
        "off_reasoning": off_reasoning,
        "note": note,
    }


def configs_for(model, detail):
    """Expand a probed model into run configs (one per reasoning mode)."""
    safe = model.replace("/", "__")
    cap = detail["capability"]
    if cap == "toggleable":
        modes = [("on", {"enabled": True}), ("off", {"enabled": False})]
    elif cap == "always_on":
        modes = [("on", None)]            # fixed; send no param
    else:  # always_off
        modes = [("off", None)]
    return [{
        "config_id": f"{safe}__{mode}",
        "model": model,
        "reasoning_mode": mode,
        "capability": cap,
        "reasoning_param": param,
        "logprobs_supported": detail["logprobs_supported"],
    } for mode, param in modes]


def main():
    client = config.make_client()
    detail, failures = {}, []
    for model in config.MODELS:
        print(f"probing {model} ...", end=" ", flush=True)
        try:
            detail[model] = probe_model(client, model)
            d = detail[model]
            print(f"OK [reasoning={d['capability']}, "
                  f"logprobs={'yes' if d['logprobs_supported'] else 'no'}]"
                  + (f"  ({d['note']})" if d["note"] else ""))
        except Exception as e:
            failures.append((model, f"{type(e).__name__}: {e}"))
            print(f"UNREACHABLE — {type(e).__name__}: {e}")

    if failures:
        print("\nHALT: not all models reachable (fail-loud, locked decision 2):")
        for m, err in failures:
            print(f"  {m}: {err}")
        raise SystemExit(1)

    configs = []
    for model in config.MODELS:
        configs.extend(configs_for(model, detail[model]))

    config.RUN_GRID_JSON.parent.mkdir(parents=True, exist_ok=True)
    config.RUN_GRID_JSON.write_text(json.dumps(
        {"configs": configs, "probe_detail": detail}, indent=2))

    # Report the planned volume for sign-off.
    n_sentences = 30
    if config.SENTENCE_MANIFEST.exists():
        import csv
        n_sentences = sum(1 for _ in csv.DictReader(
            open(config.SENTENCE_MANIFEST, newline="")))
    n_calls = len(configs) * n_sentences * config.N_RUNS
    print(f"\nwrote {config.RUN_GRID_JSON}")
    print(f"  {len(configs)} configs across {len(config.MODELS)} models:")
    for c in configs:
        print(f"    {c['config_id']}  (reasoning={c['reasoning_mode']}, "
              f"{c['capability']})")
    print(f"\nPLANNED VOLUME: {len(configs)} configs x {n_sentences} sentences "
          f"x {config.N_RUNS} runs = {n_calls} calls")
    print("  -> SIGN OFF on this before `python -m src.pilot.run`.")


if __name__ == "__main__":
    main()
