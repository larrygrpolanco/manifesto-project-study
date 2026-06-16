"""Pilot package — "Does the model know when the question is hard?"

Feasibility probe for the per-sentence human-disagreement branch. See
PILOT_PLAN.md (build/run/analysis contract) and
RESEARCH_PLAN_branch_human_distribution.md (parent design).

Mechanics (OpenRouter client, resumable JSONL cache, threaded pool, <think>
stripping + 3-digit parser, codebook rendering) are PORTED from
archive/early-experiment/pilot-2/, not imported across the archive boundary.
Pilot-2's *design* (temp-0, context-as-manipulation, stratified-random sampling)
is deliberately NOT reused.
"""
