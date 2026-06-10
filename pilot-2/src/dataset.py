"""Load the corpus, reconstruct each manifesto in document order, and draw a
reproducible stratified sample of target sentences.

Unlike pilot-1 (which scored every row of a small flat sample), pilot-2 reads a
large multi-manifesto corpus and:

  1. groups rows by manifesto and orders them by `pos` (document order);
  2. draws N_PER_MANIFESTO target sentences per manifesto, stratified by gold
     policy domain with proportional (largest-remainder) allocation, using a
     seeded RNG so the draw is identical on every run and across every
     model x condition cell;
  3. attaches to each target the *whole* ordered manifesto (shared, not copied)
     plus the target's index, so the WINDOW and FULLDOC conditions can render
     local / document-wide context without re-reading the CSV.

Required columns are named in config.COLUMNS: text, gold_code, manifesto, pos.
The gold domain is derived from the gold code via the codebook.
"""

import csv
import random
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

csv.field_size_limit(min(sys.maxsize, 2**31 - 1))


@dataclass
class Item:
    id: str
    text: str                       # the target quasi-sentence
    gold_code: str
    gold_domain_code: int
    gold_domain_name: str
    manifesto_id: str
    pos: int
    # The full manifesto in document order as (pos, text) pairs. This list object
    # is SHARED by every Item from the same manifesto -- it is not copied per item
    # -- so holding the whole corpus in memory stays cheap even for FULLDOC.
    lines: list = field(default_factory=list, repr=False)
    target_idx: int = -1            # index of this item's sentence within `lines`


def _to_int(value, default=0):
    try:
        return int(str(value).strip())
    except (ValueError, TypeError):
        return default


def _allocate(domain_counts, n):
    """Proportional (largest-remainder) allocation of n draws across strata.

    Returns {domain_code: k}, summing to min(n, total available), with each k
    capped at the domain's available count.
    """
    total = sum(domain_counts.values())
    if total <= n:                                  # take everything
        return dict(domain_counts)
    quotas = {d: n * c / total for d, c in domain_counts.items()}
    alloc = {d: int(q) for d, q in quotas.items()}
    leftover = n - sum(alloc.values())
    # hand out the remaining seats to the largest fractional remainders
    order = sorted(domain_counts,
                   key=lambda d: (quotas[d] - alloc[d], domain_counts[d], d),
                   reverse=True)
    i = 0
    while leftover > 0 and order:
        d = order[i % len(order)]
        if alloc[d] < domain_counts[d]:
            alloc[d] += 1
            leftover -= 1
        i += 1
        if i > len(order) * n:                      # safety against pathological input
            break
    return alloc


def _sample_manifesto(rows, codebook, n, seed_key):
    """rows: list of (pos:int, text:str, code:str) in document order.

    Returns the list of selected indices into `rows`, stratified by gold domain.
    """
    by_domain = defaultdict(list)
    for idx, (_, _, code) in enumerate(rows):
        dc, _ = codebook.domain_of(code)
        by_domain[dc if dc is not None else -1].append(idx)
    counts = {d: len(idxs) for d, idxs in by_domain.items()}
    alloc = _allocate(counts, n)
    rng = random.Random(seed_key)
    chosen = []
    for d in sorted(by_domain):                     # deterministic stratum order
        k = alloc.get(d, 0)
        if k <= 0:
            continue
        chosen.extend(rng.sample(by_domain[d], k))  # sample without replacement
    return sorted(chosen)                           # back into document order


def load_items(input_csv: Path, columns: dict, id_columns, codebook,
               n_per_manifesto=None, seed=0) -> list:
    text_col = columns["text"]
    code_col = columns["gold_code"]
    mani_col = columns["manifesto"]
    pos_col = columns["pos"]

    # 1. read every row, grouped by manifesto, remembering original row order
    grouped = defaultdict(list)                     # manifesto_id -> list[(pos, text, code)]
    unknown = set()
    with open(input_csv, newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            code = r[code_col].strip()
            if codebook.domain_of(code)[0] is None:
                unknown.add(code)
            grouped[r[mani_col].strip()].append(
                (_to_int(r[pos_col]), r[text_col].strip(), code))
    if unknown:
        print(f"WARNING: {len(unknown)} gold code(s) not in codebook: {sorted(unknown)}",
              file=sys.stderr)

    # 2. per manifesto: order by pos, sample, build shared `lines`, emit Items
    items = []
    for manifesto_id in sorted(grouped):
        rows = sorted(grouped[manifesto_id], key=lambda t: t[0])
        lines = [(pos, text) for pos, text, _ in rows]   # shared context object
        if n_per_manifesto is None:
            picks = range(len(rows))
        else:
            picks = _sample_manifesto(rows, codebook, n_per_manifesto,
                                      seed_key=f"{seed}:{manifesto_id}")
        for idx in picks:
            pos, text, code = rows[idx]
            dc, dn = codebook.domain_of(code)
            items.append(Item(
                id=f"{manifesto_id}-{pos}",
                text=text,
                gold_code=code,
                gold_domain_code=dc if dc is not None else -1,
                gold_domain_name=dn if dn is not None else "UNKNOWN",
                manifesto_id=manifesto_id,
                pos=pos,
                lines=lines,
                target_idx=idx,
            ))

    if len({it.id for it in items}) != len(items):
        print("WARNING: item ids are not unique; falling back to row index.", file=sys.stderr)
        for i, it in enumerate(items):
            it.id = str(i)
    print(f"sampled {len(items)} items from {len(grouped)} manifestos", file=sys.stderr)
    return items
