"""Evaluate predictions: standard metrics, the mechanical error taxonomy, and the
paired significance tests for condition differences.

Reads results/predictions.csv. Writes a set of tables to reports/ plus a
human-readable reports/summary.md.

    python src/evaluate.py

Per (model, condition):
    compliance, accuracy, accuracy|compliant, domain accuracy, weighted F1,
    and error-taxonomy rates E1 (cross-domain), E2 (valence flip),
    E5 (catch-all absorption), residual.

Significance (per model, outcome = exact-category correct/incorrect, paired over
items): Cochran's Q omnibus across the 4 conditions, then pairwise McNemar
(Holm-corrected) for the comparisons in config.COMPARISONS. Direction consistency
across models is reported so a one-model fluke isn't mistaken for an effect.
"""

import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import f1_score
from statsmodels.stats.contingency_tables import cochrans_q, mcnemar
from statsmodels.stats.multitest import multipletests

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

import config
from codebook import load_codebook


def classify_error(row, cb):
    """Return error type for a wrong, compliant prediction; '' if correct/non-compliant."""
    if not row["compliant"] or row["pred_code"] == row["gold_code"]:
        return ""
    true, pred = row["gold_code"], row["pred_code"]
    tags = []
    if cb.domain_of(true)[0] != cb.domain_of(pred)[0]:
        tags.append("E1")                                  # cross-domain
    if cb.is_valence_flip(true, pred):
        tags.append("E2")                                  # valence flip
    if pred in config.CATCH_ALL_CODES and true not in config.CATCH_ALL_CODES:
        tags.append("E5")                                  # catch-all absorption
    return "+".join(tags) if tags else "residual"


def load_predictions(cb):
    if not config.PREDICTIONS_CSV.exists():
        sys.exit(f"no predictions at {config.PREDICTIONS_CSV} -- run run_experiment.py first")
    df = pd.read_csv(config.PREDICTIONS_CSV, dtype=str).fillna("")
    df["compliant"] = df["compliant"].astype(str).str.lower().isin(("true", "1"))
    df["correct"] = df["compliant"] & (df["pred_code"] == df["gold_code"])
    df["error_type"] = df.apply(lambda r: classify_error(r, cb), axis=1)
    return df


def metrics_table(df, cb):
    rows = []
    conf_dir = config.REPORTS_DIR / "confusion"
    conf_dir.mkdir(parents=True, exist_ok=True)
    for (model, cond), g in df.groupby(["model", "condition"]):
        n = len(g)
        comp = g["compliant"]
        errs = g[(g["correct"] == False) & comp]          # wrong & compliant
        et = errs["error_type"]
        y_true = g["gold_code"].tolist()
        y_pred = [p if c else "NONE" for p, c in zip(g["pred_code"], comp)]
        wf1 = f1_score(y_true, y_pred, average="weighted", zero_division=0)
        # domain accuracy: compliant & predicted domain == gold domain
        dom_ok = sum(1 for _, r in g.iterrows()
                     if r["compliant"] and str(cb.domain_of(r["pred_code"])[0])
                     == str(r["gold_domain_code"]))
        rows.append({
            "model": model, "condition": cond, "n": n,
            "compliance": comp.mean(),
            "accuracy": g["correct"].mean(),
            "accuracy|compliant": g["correct"].sum() / comp.sum() if comp.sum() else 0.0,
            "domain_accuracy": dom_ok / n,
            "weighted_f1": wf1,
            "n_errors": len(errs),
            "E1_cross_domain": et.str.contains("E1").sum() / len(errs) if len(errs) else 0.0,
            "E2_valence_flip": et.str.contains("E2").sum() / len(errs) if len(errs) else 0.0,
            "E5_catch_all": et.str.contains("E5").sum() / len(errs) if len(errs) else 0.0,
            "residual": (et == "residual").sum() / len(errs) if len(errs) else 0.0,
        })
        # confusion matrix (counts) saved long+wide
        ct = pd.crosstab(g["gold_code"], y_pred)
        ct.to_csv(conf_dir / f"{model.replace('/', '__')}__{cond}.csv")
    return pd.DataFrame(rows).sort_values(["model", "condition"])


def correctness_matrix(df_model):
    """items x conditions binary-correct matrix, on items present in ALL conditions."""
    conds = config.CONDITIONS
    piv = df_model.pivot_table(index="item_id", columns="condition",
                               values="correct", aggfunc="first")
    piv = piv.reindex(columns=conds).dropna()
    return piv.astype(int)


def run_stats(df):
    cochran_rows, mcnemar_rows = [], []
    for model, gm in df.groupby("model"):
        mat = correctness_matrix(gm)
        if mat.shape[0] < 2 or mat.shape[1] < 2:
            continue
        q = cochrans_q(mat.values)
        cochran_rows.append({"model": model, "n_items": mat.shape[0],
                             "k_conditions": mat.shape[1],
                             "Q": q.statistic, "df": mat.shape[1] - 1, "p": q.pvalue})
        pvals, recs = [], []
        for label, a, b in config.COMPARISONS:
            if a not in mat.columns or b not in mat.columns:
                continue
            va, vb = mat[a].values, mat[b].values
            both = int(((va == 1) & (vb == 1)).sum())
            a_only = int(((va == 1) & (vb == 0)).sum())   # a correct, b wrong (b broke it)
            b_only = int(((va == 0) & (vb == 1)).sum())   # b correct, a wrong (b fixed it)
            neither = int(((va == 0) & (vb == 0)).sum())
            disc = a_only + b_only
            table = [[both, a_only], [b_only, neither]]
            res = mcnemar(table, exact=(disc < 25), correction=True)
            recs.append({"model": model, "comparison": label, "a": a, "b": b,
                         "acc_a": va.mean(), "acc_b": vb.mean(),
                         "delta(b-a)": vb.mean() - va.mean(),
                         "b_fixed": b_only, "a_kept(b_broke)": a_only, "discordant": disc,
                         "statistic": res.statistic, "p_raw": res.pvalue})
            pvals.append(res.pvalue)
        if pvals:
            holm = multipletests(pvals, method="holm")[1]
            for r, ph in zip(recs, holm):
                r["p_holm"] = ph
                r["sig_.05"] = ph < 0.05
            mcnemar_rows += recs
    return pd.DataFrame(cochran_rows), pd.DataFrame(mcnemar_rows)


def direction_consistency(mc):
    """For each comparison, count how many models show b>a vs b<a (among sig + all)."""
    rows = []
    for comp, g in mc.groupby("comparison"):
        better = (g["delta(b-a)"] > 0).sum()
        worse = (g["delta(b-a)"] < 0).sum()
        sig = g["sig_.05"].sum()
        rows.append({"comparison": comp, "models": len(g),
                     "b>a": int(better), "b<a": int(worse),
                     "significant(Holm)": int(sig)})
    return pd.DataFrame(rows)


def write_summary(metrics, cochran, mc, consist):
    L = ["# Pilot-1 evaluation summary\n"]
    L.append("## Metrics (per model × condition)\n")
    L.append(metrics.round(3).to_markdown(index=False))
    L.append("\n## Cochran's Q (omnibus across conditions, per model)\n")
    L.append(cochran.round(4).to_markdown(index=False) if len(cochran) else "_n/a_")
    L.append("\n## Pairwise McNemar (Holm-corrected, exact-category correctness)\n")
    L.append(mc.round(4).to_markdown(index=False) if len(mc) else "_n/a_")
    L.append("\n## Direction consistency across models\n")
    L.append("`b>a` = how many models scored the second condition higher. An effect "
             "you trust shows the same direction across most models *and* significance.\n")
    L.append(consist.to_markdown(index=False) if len(consist) else "_n/a_")
    (config.REPORTS_DIR / "summary.md").write_text("\n".join(L) + "\n")


def main():
    cb = load_codebook(config.CODEBOOK_CSV, config.VALENCE_PAIRS_CSV)
    df = load_predictions(cb)
    config.REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    metrics = metrics_table(df, cb)
    metrics.to_csv(config.REPORTS_DIR / "metrics.csv", index=False)

    cochran, mc = run_stats(df)
    cochran.to_csv(config.REPORTS_DIR / "stats_cochran.csv", index=False)
    mc.to_csv(config.REPORTS_DIR / "stats_mcnemar.csv", index=False)
    consist = direction_consistency(mc) if len(mc) else pd.DataFrame()
    if len(consist):
        consist.to_csv(config.REPORTS_DIR / "stats_direction_consistency.csv", index=False)

    write_summary(metrics, cochran, mc, consist)
    print(metrics.round(3).to_string(index=False))
    print(f"\nwrote tables + summary to {config.REPORTS_DIR}")


if __name__ == "__main__":
    main()
