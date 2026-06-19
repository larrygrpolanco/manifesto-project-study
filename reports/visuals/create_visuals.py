#!/usr/bin/env python3
"""
Generate key visualizations from the human profile data and pilot results.
Each chart is designed to tell one part of the story.
"""

import csv
import os
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import numpy as np
from collections import Counter, defaultdict

OUT = os.path.join(os.path.dirname(__file__))
os.makedirs(OUT, exist_ok=True)

PALETTE = {
    "easy": "#2ecc71",
    "mid": "#f39c12",
    "hard": "#e74c3c",
    "human": "#3498db",
    "model": "#e74c3c",
    "between": "#9b59b6",
    "bg": "#fafafa",
    "ink": "#2c3e50",
    "grid": "#ecf0f1",
    "danger": "#c0392b",
}
plt.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.size": 10,
        "axes.titlesize": 13,
        "axes.labelsize": 11,
        "figure.facecolor": "white",
        "axes.facecolor": PALETTE["bg"],
        "axes.edgecolor": PALETTE["ink"],
        "axes.grid": True,
        "grid.alpha": 0.3,
        "grid.color": PALETTE["grid"],
    }
)


def load_csv(path):
    with open(path) as f:
        return list(csv.DictReader(f))


# ─── load data ────────────────────────────────────────────────────────
repo = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
human_amb = load_csv(os.path.join(repo, "reports/human/per_sentence_ambiguity.csv"))
q1_wb = load_csv(os.path.join(repo, "reports/pilot/q1_within_between.csv"))
q1_bucket = load_csv(os.path.join(repo, "reports/pilot/q1_by_bucket.csv"))
q1_corr = load_csv(os.path.join(repo, "reports/pilot/q1_correlations.csv"))

# Build sentence lookup for the 30 pilot sentences
pilot_ids = {r["unit_id"] for r in q1_wb}
human_pilot_map = {}
for r in human_amb:
    if r["unit_id"] in pilot_ids:
        human_pilot_map[r["unit_id"]] = {
            "h_ret_1m": float(r["retained_class_cat_1mmodal"]),
            "h_ret_Hnorm": float(r["retained_class_cat_Hnorm"]),
            "h_full_1m": float(r["full_class_cat_1mmodal"]),
            "h_full_Hnorm": float(r["full_class_cat_Hnorm"]),
            "master_code": r["master_code"],
        }

# Within-between data
wb_by_id = {}
for r in q1_wb:
    wb_by_id[r["unit_id"]] = {
        "bucket": r["bucket"],
        "within": float(r["within_model_1mmodal"]),
        "between": float(r["between_model_1mmodal"]),
    }

# Merge for pilot sentences
pilot_sentences = []
for uid in pilot_ids:
    h = human_pilot_map.get(uid, {})
    w = wb_by_id.get(uid, {})
    pilot_sentences.append(
        {
            "uid": uid,
            "bucket": w.get("bucket", "unknown"),
            "h_1m": h.get("h_ret_1m", 0),
            "m_1m": w.get("within", 0),
            "m_between": w.get("between", 0),
        }
    )

# Sort all 179 sentences by human entropy for the landscape
all_sentences = []
for r in human_amb:
    all_sentences.append(
        {
            "uid": r["unit_id"],
            "h_1m": float(r["retained_class_cat_1mmodal"]),
            "h_Hnorm": float(r["retained_class_cat_Hnorm"]),
        }
    )
all_sentences.sort(key=lambda x: x["h_1m"])


# ─── CHART 1: The Human Ambiguity Landscape ─────────────────────────────
def chart_human_landscape():
    """All 179 sentences sorted by human disagreement (1-modal share).
    Shows how often even trained experts disagree."""
    fig, ax = plt.subplots(figsize=(14, 5))

    x = range(len(all_sentences))
    y = [s["h_1m"] for s in all_sentences]

    colors = [
        PALETTE["easy"] if v < 0.3 else PALETTE["mid"] if v < 0.5 else PALETTE["hard"]
        for v in y
    ]
    ax.bar(x, y, color=colors, width=1.0, edgecolor="none")

    ax.axhline(y=0.30, color=PALETTE["easy"], linestyle="--", alpha=0.5)
    ax.axhline(y=0.50, color=PALETTE["hard"], linestyle="--", alpha=0.5)

    # Annotate a few anchor sentences
    for s in all_sentences:
        if s["uid"] in ("GB-056", "GB-033", "NZ-008", "GB-074"):
            idx = next(i for i, ss in enumerate(all_sentences) if ss["uid"] == s["uid"])
            ax.annotate(
                s["uid"],
                (idx, s["h_1m"]),
                textcoords="offset points",
                xytext=(0, 8),
                ha="center",
                fontsize=7,
                color=PALETTE["ink"],
            )

    ax.set_ylabel("Human Disagreement (1 − modal share)")
    ax.set_xlabel("Sentences (179 total, sorted easiest → hardest)")
    ax.set_title(
        "The Human Ceiling: Even Trained Experts Disagree Constantly\n"
        "72/179 sentences have no majority code (1−modal ≥ 0.50, retained coders)",
        fontweight="bold",
    )

    # Legend
    easy_patch = mpatches.Patch(color=PALETTE["easy"], label="High agreement (<0.30)")
    mid_patch = mpatches.Patch(color=PALETTE["mid"], label="Mid-split (0.30–0.50)")
    hard_patch = mpatches.Patch(color=PALETTE["hard"], label="High-split (≥0.50)")
    ax.legend(handles=[easy_patch, mid_patch, hard_patch], loc="upper left", fontsize=9)

    ax.set_ylim(0, 1.05)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "01_human_landscape.png"), dpi=200)
    plt.close(fig)


# ─── CHART 2: The Pin vs The Split (Under-dispersion) ──────────────────
def chart_underdispersion():
    """Scatter: human 1-modal vs model within-model spread on 30 pilot sentences.
    The y=x line is the equality line. Points below it = models pinning more than humans."""
    fig, ax = plt.subplots(figsize=(7, 7))

    bucket_order = {"high-agreement": 0, "mid-split": 1, "high-split": 2}
    pilot_sorted = sorted(pilot_sentences, key=lambda s: bucket_order.get(s["bucket"], 99))

    for s in pilot_sorted:
        bkt = s["bucket"]
        color = {
            "high-agreement": PALETTE["easy"],
            "mid-split": PALETTE["mid"],
            "high-split": PALETTE["hard"],
        }.get(bkt, "gray")
        ax.scatter(s["h_1m"], s["m_1m"], c=color, s=70, edgecolors="white", linewidth=0.5, zorder=5)
        # label the most notable ones
        if s["uid"] in ("NZ-006", "GB-033", "GB-016", "GB-056", "NZ-008"):
            ax.annotate(
                s["uid"],
                (s["h_1m"], s["m_1m"]),
                textcoords="offset points",
                xytext=(6, 4),
                fontsize=7,
                color=PALETTE["ink"],
            )

    # y = x line
    lim = max(max(s["h_1m"] for s in pilot_sorted), max(s["m_1m"] for s in pilot_sorted)) + 0.05
    ax.plot([0, lim], [0, lim], "k--", alpha=0.3, linewidth=1, label="Models = Humans (y=x)")

    ax.set_xlabel("Human Disagreement (1 − modal share, retained coders)")
    ax.set_ylabel("Model Within-Model Disagreement (1 − modal share)")
    ax.set_title(
        "The Pin vs. The Split: Models Pin Where Humans Waver\n"
        "Under-dispersion ratio = 0.26 (easy) / 0.50 (mid) / 0.39 (hard)",
        fontweight="bold",
    )

    # Legend
    for label, color in [
        ("High agreement", PALETTE["easy"]),
        ("Mid-split", PALETTE["mid"]),
        ("High-split", PALETTE["hard"]),
    ]:
        ax.scatter([], [], c=color, s=50, label=label, edgecolors="white", linewidth=0.5)
    ax.legend(loc="upper left", fontsize=9)
    ax.set_xlim(-0.02, lim)
    ax.set_ylim(-0.02, lim)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "02_underdispersion.png"), dpi=200)
    plt.close(fig)


# ─── CHART 3: Within vs Between Model Spread ───────────────────────────
def chart_within_vs_between():
    """Dumbbell chart: within-model vs between-model spread per sentence."""
    fig, ax = plt.subplots(figsize=(14, 6))

    bucket_order = {"high-agreement": 0, "mid-split": 1, "high-split": 2}
    pilot_sorted = sorted(pilot_sentences, key=lambda s: bucket_order.get(s["bucket"], 99))

    uids = [s["uid"] for s in pilot_sorted]
    x = range(len(uids))

    for i, s in enumerate(pilot_sorted):
        w = s["m_1m"]  # within-model
        b = s["m_between"]  # between-model
        
        # Draw dumbbell
        ax.plot([i, i], [w, b], color="gray", alpha=0.3, linewidth=1.5, zorder=1)
        
        # Within (red dot)
        ax.scatter(i, w, c=PALETTE["model"], s=60, zorder=5, edgecolors="white", linewidth=0.5)
        # Between (purple dot)
        ax.scatter(i, b, c=PALETTE["between"], s=60, zorder=5, edgecolors="white", linewidth=0.5)

    ax.set_xticks(x)
    ax.set_xticklabels(uids, rotation=90, fontsize=6)
    ax.set_ylabel("1 − modal share")
    ax.set_title(
        "Individually Confident, Collectively Incoherent\n"
        "Red = within-model spread (one model's 10 re-runs). Purple = between-model spread.\n"
        "On hard items, between >> within: each model pins, but on different codes.",
        fontweight="bold",
    )

    # Legend
    ax.scatter([], [], c=PALETTE["model"], s=50, label="Within-model spread (single model consistency)", edgecolors="white", linewidth=0.5)
    ax.scatter([], [], c=PALETTE["between"], s=50, label="Between-model spread (models disagree with each other)", edgecolors="white", linewidth=0.5)
    ax.legend(loc="upper left", fontsize=8)
    ax.set_ylim(-0.02, 0.85)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "03_within_vs_between.png"), dpi=200)
    plt.close(fig)


# ─── CHART 4: The Correlation Trap ─────────────────────────────────────
def chart_correlation_trap():
    """Two-panel: pooled r vs hard+mid r to show the easy-anchor artifact."""
    # We need per-sentence model spread. Use the 30 pilot sentences.
    # For each pilot sentence, we have human 1-modal (retained) and model within 1-modal.
    # We can compute the pooled correlation and the hard+mid correlation.
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    all_x = [s["h_1m"] for s in pilot_sentences]
    all_y = [s["m_1m"] for s in pilot_sentences]
    
    easy = [(s["h_1m"], s["m_1m"]) for s in pilot_sentences if s["bucket"] == "high-agreement"]
    hard_mid = [(s["h_1m"], s["m_1m"]) for s in pilot_sentences if s["bucket"] != "high-agreement"]

    # Panel 1: All sentences
    for s in pilot_sentences:
        bkt = s["bucket"]
        color = {"high-agreement": PALETTE["easy"], "mid-split": PALETTE["mid"], "high-split": PALETTE["hard"]}.get(bkt, "gray")
        ax1.scatter(s["h_1m"], s["m_1m"], c=color, s=70, edgecolors="white", linewidth=0.5, zorder=5)

    # Trendline for all
    if len(all_x) > 2:
        z_all = np.polyfit(all_x, all_y, 1)
        p_all = np.poly1d(z_all)
        ax1.plot([0, 0.9], [p_all(0), p_all(0.9)], "k-", alpha=0.5, linewidth=1.5)

    ax1.set_xlabel("Human Disagreement (1 − modal share)")
    ax1.set_ylabel("Model Disagreement (1 − modal share)")
    ax1.set_title(
        f"ALL sentences (n=30)\n"
        f"r ≈ 0.46 ← looks like models track difficulty!",
        fontweight="bold",
        color=PALETTE["easy"],
    )
    ax1.set_xlim(-0.02, 0.9)
    ax1.set_ylim(-0.02, 0.9)

    # Panel 2: Hard + mid only (drop the easy anchor)
    for s in pilot_sentences:
        if s["bucket"] == "high-agreement":
            # Show easy points faded
            ax2.scatter(s["h_1m"], s["m_1m"], c=PALETTE["easy"], s=30, alpha=0.2, edgecolors="none")
        else:
            bkt = s["bucket"]
            color = {"mid-split": PALETTE["mid"], "high-split": PALETTE["hard"]}.get(bkt, "gray")
            ax2.scatter(s["h_1m"], s["m_1m"], c=color, s=70, edgecolors="white", linewidth=0.5, zorder=5)

    hm_x = [s[0] for s in hard_mid]
    hm_y = [s[1] for s in hard_mid]
    if len(hm_x) > 2:
        z_hm = np.polyfit(hm_x, hm_y, 1)
        p_hm = np.poly1d(z_hm)
        ax2.plot([0.2, 0.9], [p_hm(0.2), p_hm(0.9)], "k-", alpha=0.5, linewidth=1.5)

    ax2.set_xlabel("Human Disagreement (1 − modal share)")
    ax2.set_ylabel("Model Disagreement (1 − modal share)")
    ax2.set_title(
        f"Hard + Mid ONLY (n=24)\n"
        f"r ≈ 0.19 ← the signal collapses!",
        fontweight="bold",
        color=PALETTE["hard"],
    )
    ax2.set_xlim(-0.02, 0.9)
    ax2.set_ylim(-0.02, 0.9)

    fig.suptitle("The Correlation Trap: Easy Sentences Drive the Entire Relationship", fontsize=14, fontweight="bold", y=1.02)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "04_correlation_trap.png"), dpi=200)
    plt.close(fig)


# ─── CHART 5: The 2×2 Danger Grid ─────────────────────────────────────
def chart_2x2_grid():
    """The populated 2×2: human agreement × model agreement, with sentence counts."""
    # We classify each pilot sentence:
    # Human split: retained 1-modal >= 0.50
    # Model split: between-model 1-modal >= 0.20 (loose threshold)
    
    cells = {"HA_MA": [], "HA_MS": [], "HS_MA": [], "HS_MS": []}
    
    for s in pilot_sentences:
        h_split = s["h_1m"] >= 0.50
        m_split = s["m_between"] >= 0.20
        
        if h_split and m_split:
            cells["HS_MS"].append(s["uid"])
        elif h_split and not m_split:
            cells["HS_MA"].append(s["uid"])
        elif not h_split and m_split:
            cells["HA_MS"].append(s["uid"])
        else:
            cells["HA_MA"].append(s["uid"])

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.set_xlim(-0.5, 2.5)
    ax.set_ylim(-0.5, 2.5)

    # Draw the grid
    cell_data = [
        ("Models Agree", "Humans Agree", cells["HA_MA"], PALETTE["easy"], "Construct\nis real"),
        ("Models Split", "Humans Agree", cells["HA_MS"], PALETTE["mid"], "Models add\nnoise"),
        ("Models Agree", "Humans Split", cells["HS_MA"], PALETTE["hard"], "False consensus\n(PILOT: RARE)"),
        ("Models Split", "Humans Split", cells["HS_MS"], PALETTE["danger"], "Honest difficulty\nOR alien scatter\n(PILOT: POPULATED)"),
    ]

    positions = [(0, 1), (1, 1), (0, 0), (1, 0)]  # row,col → x,y (top-left to bottom-right)

    for (m_label, h_label, uids, color, note), (x, y) in zip(cell_data, positions):
        rect = mpatches.FancyBboxPatch(
            (x - 0.45, y - 0.45), 0.9, 0.9,
            boxstyle="round,pad=0.02",
            facecolor=color,
            alpha=0.2,
            edgecolor=color,
            linewidth=2,
        )
        ax.add_patch(rect)
        ax.text(x, y + 0.29, m_label, ha="center", fontsize=9, fontweight="bold", color=color)
        ax.text(x, y + 0.17, h_label, ha="center", fontsize=8)
        ax.text(x, y - 0.05, f"n = {len(uids)}", ha="center", fontsize=11, fontweight="bold", color=PALETTE["ink"])
        ax.text(x, y - 0.28, note, ha="center", fontsize=7, color=PALETTE["ink"])

    ax.set_title(
        "The 2×2: Human × Model Agreement on 30 Pilot Sentences\n"
        "(Pilot finding — the \"danger\" cell is populated, the \"false consensus\" cell is sparse)",
        fontweight="bold",
        fontsize=12,
    )
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("   ← Human Disagreement   |   Human Agreement →   ", fontsize=10, color=PALETTE["ink"])
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "05_2x2_grid.png"), dpi=200)
    plt.close(fig)


# ─── CHART 6: Under-dispersion Bucket Summary ───────────────────────────
def chart_underdispersion_buckets():
    """Grouped bar: human vs model spread by difficulty bucket."""
    fig, ax = plt.subplots(figsize=(8, 5))

    buckets = ["high-agreement", "mid-split", "high-split"]
    bucket_labels = ["High Agreement\n(easy)", "Mid-Split\n(medium)", "High-Split\n(hard)"]
    human_vals = [0.100, 0.420, 0.643]  # from pilot summary, retained
    model_vals = [0.026, 0.209, 0.248]
    ratio_vals = [0.26, 0.50, 0.39]

    x = np.arange(len(buckets))
    width = 0.3

    bars1 = ax.bar(x - width / 2, human_vals, width, label="Human Experts (retained)", color=PALETTE["human"], edgecolor="white")
    bars2 = ax.bar(x + width / 2, model_vals, width, label="Models (within-model)", color=PALETTE["model"], edgecolor="white")

    # Add ratio annotations
    for i, ratio in enumerate(ratio_vals):
        ax.text(i, max(human_vals[i], model_vals[i]) + 0.04, f"×{ratio:.2f}", ha="center", fontsize=10, fontweight="bold", color=PALETTE["danger"])

    ax.set_xticks(x)
    ax.set_xticklabels(bucket_labels, fontsize=10)
    ax.set_ylabel("Disagreement (1 − modal share)")
    ax.set_title("Under-Dispersion: Models Pin Where Humans Waver\nModel spread = 0.26–0.50 × human spread, worst on the hardest items", fontweight="bold")
    ax.legend(loc="upper left", fontsize=9)
    ax.set_ylim(0, 0.85)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "06_underdispersion_buckets.png"), dpi=200)
    plt.close(fig)


# ─── CHART 7: Exemplar Sentence Receipts ───────────────────────────────
def chart_exemplar_receipt():
    """For NZ-006 and GB-033, show the human code distribution vs model distribution side by side.
    This is the 'sentence with graph' idea."""
    
    # Hard-coded from the exemplars.md data
    exemplars = [
        {
            "uid": "NZ-006",
            "text": '"restoring New Zealand\'s shattered economy"',
            "sentence": "The first three years of the coming National Government will be\nvery largely devoted to restoring New Zealand's shattered economy.",
            "bucket": "mid-split",
            "human": {"408": 11, "404": 5, "305": 4, "414": 1, "412": 1, "303": 1},
            "model": {"408": 138, "414": 1},  # 14 configs × 10 runs = 140 total
            "insight": "Humans split 4 ways. Models: near-unanimous on 408.\nSpecificity error: models ignore the policy-instrument frame."
        },
        {
            "uid": "GB-033",
            "text": '"civil war in British industry…"',
            "sentence": "Much of the present unemployment is a direct result of the\ncivil war in British industry, of restrictive practices and low investment.",
            "bucket": "high-split",
            "human": {"405": 5, "408": 4, "401": 3, "407": 3, "410": 3, "403": 2, "409": 2, "402": 2, "305": 2, "411": 1, "701": 1, "000": 1, "304": 1, "414": 1, "404": 1},
            "model": {"408": 39, "702": 31, "410": 23, "701": 10, "703": 5, "606": 10, "403": 3, "405": 3, "305": 3, "401": 2, "409": 3, "503": 2, "506": 1, "502": 1, "607": 1, "705": 1, "402": 1, "OFF": 1},
            "insight": "Humans scatter across 15 codes (max 5/32).\nModel pooled modal = 702 (a code only 1/32 humans chose).\n'Incoherence + alien' — the textbook case."
        }
    ]

    for ex in exemplars:
        fig = plt.figure(figsize=(14, 7))
        gs = GridSpec(2, 2, figure=fig, height_ratios=[1, 3], hspace=0.35, wspace=0.3)

        # Top row: sentence text spanning full width
        ax_text = fig.add_subplot(gs[0, :])
        ax_text.axis("off")
        bucket_color = {"mid-split": PALETTE["mid"], "high-split": PALETTE["hard"]}[ex["bucket"]]
        ax_text.text(
            0.5, 0.6, ex["sentence"],
            ha="center", va="center", fontsize=12, fontstyle="italic",
            wrap=True, color=PALETTE["ink"],
            bbox=dict(boxstyle="round,pad=0.5", facecolor=bucket_color, alpha=0.1, edgecolor=bucket_color, linewidth=1)
        )
        ax_text.text(0.5, 0.1, f"{ex['uid']}  |  {ex['bucket']}  |  gold/master code annotated after text", ha="center", fontsize=8, color="gray")

        # Left: human distribution
        ax_h = fig.add_subplot(gs[1, 0])
        h_codes = sorted(ex["human"].keys())
        h_vals = [ex["human"][c] for c in h_codes]
        h_total = sum(h_vals)
        h_pcts = [v / h_total * 100 for v in h_vals]
        
        bars_h = ax_h.barh(range(len(h_codes)), h_pcts, color=PALETTE["human"], edgecolor="white", height=0.7)
        ax_h.set_yticks(range(len(h_codes)))
        ax_h.set_yticklabels(h_codes, fontsize=8)
        ax_h.set_xlabel("% of coders")
        ax_h.set_title(f"Human Experts (32 GB / 23 NZ coders)", fontweight="bold", color=PALETTE["human"], fontsize=11)
        ax_h.invert_yaxis()
        
        # Add % labels on bars
        for i, (v, p) in enumerate(zip(h_vals, h_pcts)):
            if p > 5:
                ax_h.text(p + 1, i, f"{v}/{h_total}", va="center", fontsize=7, color=PALETTE["ink"])

        # Right: model distribution
        ax_m = fig.add_subplot(gs[1, 1])
        m_codes = sorted(ex["model"].keys())
        m_vals = [ex["model"][c] for c in m_codes]
        m_total = sum(m_vals)
        m_pcts = [v / m_total * 100 for v in m_vals]
        
        bars_m = ax_m.barh(range(len(m_codes)), m_pcts, color=PALETTE["model"], edgecolor="white", height=0.7)
        ax_m.set_yticks(range(len(m_codes)))
        ax_m.set_yticklabels(m_codes, fontsize=8)
        ax_m.set_xlabel("% of model runs")
        ax_m.set_title(f"Models (14 configs × 10 runs = {m_total})", fontweight="bold", color=PALETTE["model"], fontsize=11)
        ax_m.invert_yaxis()
        
        for i, (v, p) in enumerate(zip(m_vals, m_pcts)):
            if p > 3:
                ax_m.text(p + 0.5, i, f"{v}", va="center", fontsize=7, color=PALETTE["ink"])

        # Add insight annotation
        fig.text(0.5, 0.02, ex["insight"], ha="center", fontsize=10, fontweight="bold", color=PALETTE["danger"],
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="#fff3cd", edgecolor=PALETTE["mid"], alpha=0.8))

        fig.suptitle(f"Exemplar: {ex['uid']} — {ex['text']}", fontsize=13, fontweight="bold", y=1.01)
        fig.tight_layout(rect=(0, 0.08, 1, 0.97))
        fig.savefig(os.path.join(OUT, f"07_exemplar_{ex['uid'].replace('-', '_')}.png"), dpi=200)
        plt.close(fig)


# ─── CHART 8: The "Sentence Card" Multi-Panel ──────────────────────────
def chart_sentence_cards():
    """For the three exemplar sentences, compact cards showing human spread & model spread as a single row."""
    exemplars_pilot = [
        {
            "uid": "NZ-006",
            "sentence": "…restoring New Zealand's shattered economy.",
            "human_1m": 0.50,  # from human_pilot_map
            "model_1m": 0.007,
            "between_1m": 0.0,
            "bucket": "mid-split",
            "note": "Models converge on 408.\nHumans split 408/404/305.",
        },
        {
            "uid": "GB-033",
            "sentence": "…civil war in British industry, restrictive practices, low investment.",
            "human_1m": 0.765,
            "model_1m": 0.350,
            "between_1m": 0.643,
            "bucket": "high-split",
            "note": "Models scatter to alien codes.\nPooled modal 702 = 1/32 humans chose.",
        },
        {
            "uid": "GB-016",
            "sentence": "…warped sense of priorities by successive governments.",
            "human_1m": 0.588,
            "model_1m": 0.421,
            "between_1m": 0.714,
            "bucket": "high-split",
            "note": "Models scatter — pooled modal 303\n(a code no human chose). Alien error.",
        },
    ]

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    for ax, ex in zip(axes, exemplars_pilot):
        bkt = ex["bucket"]
        color = {"mid-split": PALETTE["mid"], "high-split": PALETTE["hard"]}[bkt]
        
        # Draw three horizontal bars: human, model (within), model (between)
        bars = ["Human\nexperts", "Model\n(within)", "Models\n(between)"]
        values = [ex["human_1m"], ex["model_1m"], ex["between_1m"]]
        bar_colors = [PALETTE["human"], PALETTE["model"], PALETTE["between"]]
        
        y_pos = [0, 1, 2]
        ax.barh(y_pos, values, color=bar_colors, edgecolor="white", height=0.5)
        
        # Value labels
        for i, v in enumerate(values):
            ax.text(v + 0.03, i, f"{v:.2f}", va="center", fontsize=11, fontweight="bold", color=PALETTE["ink"])
        
        ax.set_yticks(y_pos)
        ax.set_yticklabels(bars, fontsize=9)
        ax.set_xlim(0, 1.0)
        ax.set_title(f"{ex['uid']}\n\"{ex['sentence']}\"", fontsize=10, fontweight="bold", color=color, loc="left")
        ax.text(0.5, -0.8, ex["note"], ha="center", fontsize=7.5, color=PALETTE["ink"],
                transform=ax.transAxes)

    fig.suptitle(
        "Three Sentences, Three Failure Modes\n"
        "How humans, a single model (10 re-runs), and different models compare on the same sentence",
        fontweight="bold", fontsize=13, y=1.04
    )
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "08_sentence_cards.png"), dpi=200)
    plt.close(fig)


# ─── CHART 9: The Big Summary — One Infographic ────────────────────────
def chart_big_summary():
    """Single-page summary with key numbers."""
    fig = plt.figure(figsize=(14, 10))
    
    # Title
    fig.text(0.5, 0.96, "When Models Disagree, Who Is Right?", ha="center", fontsize=18, fontweight="bold", color=PALETTE["ink"])
    fig.text(0.5, 0.93, "What 32 Human Experts + 14 AI Models Reveal About Coding Political Text", ha="center", fontsize=12, color="gray")

    # Three big number boxes
    boxes = [
        (0.08, 0.78, "72/179", "sentences have NO\nmajority expert code", "Even the coding manual's own\npedagogical texts split experts.", PALETTE["hard"]),
        (0.39, 0.78, "0.26–0.50×", "model spread vs.\nhuman spread", "Models pin an answer with\n~3× the confidence humans have.", PALETTE["danger"]),
        (0.70, 0.78, "r: 0.46→0.19", "correlation collapses\nwithout easy sentences", "Model disagreement does NOT\ntrack human difficulty on hard items.", PALETTE["between"]),
    ]
    
    for x, y, big, sub, exp, color in boxes:
        rect = mpatches.FancyBboxPatch(
            (x, y), 0.27, 0.12, boxstyle="round,pad=0.02",
            facecolor=color, alpha=0.1, edgecolor=color, linewidth=2, transform=fig.transFigure
        )
        fig.patches.append(rect)
        fig.text(x + 0.135, y + 0.09, big, ha="center", fontsize=24, fontweight="bold", color=color, transform=fig.transFigure)
        fig.text(x + 0.135, y + 0.05, sub, ha="center", fontsize=9, fontweight="bold", color=PALETTE["ink"], transform=fig.transFigure)
        fig.text(x + 0.135, y + 0.01, exp, ha="center", fontsize=7, color=PALETTE["ink"], transform=fig.transFigure)

    # Three legs
    legs = [
        ("LEG 1: Under-Dispersion", "Each model wavers far less than human experts — and the gap is\nworst on the hardest sentences. Model/human spread ratio: 0.26 (easy)\n/ 0.50 (mid) / 0.39 (hard). The model pins where experts waver."),
        ("LEG 2: Collective Incoherence", "On hard items, between-model spread (0.42) exceeds within-model\nspread (0.25). Each model pinning confidently on different codes —\nfrequently codes no human chose. Pooling models creates false consensus."),
        ("LEG 3: No Recovery of Difficulty", "Model disagreement barely tracks human disagreement once easy\nsentences are removed (r: 0.46 → 0.19). The signal that would be\nuseful — identifying genuinely hard sentences — breaks down."),
    ]
    
    for i, (title, body) in enumerate(legs):
        y_pos = 0.60 - i * 0.17
        fig.text(0.08, y_pos, title, fontsize=12, fontweight="bold", color=PALETTE["ink"], transform=fig.transFigure)
        fig.text(0.08, y_pos - 0.045, body, fontsize=9, color=PALETTE["ink"], transform=fig.transFigure, linespacing=1.4)

    # Bottom: implications
    fig.text(0.5, 0.13, "Implication for the practitioner:", ha="center", fontsize=12, fontweight="bold", color=PALETTE["danger"])
    fig.text(0.5, 0.08, "Neither single-model confidence nor multi-model voting is a safe validity check for genuinely ambiguous coding.\nThe 2×2 grid (human agreement × model agreement) is a diagnostic template anyone can apply with even a small human distribution.",
             ha="center", fontsize=9, color=PALETTE["ink"], transform=fig.transFigure)

    fig.text(0.5, 0.02, "Data: Mikhaylov, Laver & Benoit (2012) CMP reliability experiment | 179 sentences | 23–32 experts per sentence | 14 model configs", ha="center", fontsize=7, color="gray")
    
    fig.savefig(os.path.join(OUT, "09_big_summary.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


# ─── Run all ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generating visualizations...")
    chart_human_landscape()
    print("  1/9 Human landscape ✓")
    chart_underdispersion()
    print("  2/9 Under-dispersion scatter ✓")
    chart_within_vs_between()
    print("  3/9 Within vs between ✓")
    chart_correlation_trap()
    print("  4/9 Correlation trap ✓")
    chart_2x2_grid()
    print("  5/9 2×2 grid ✓")
    chart_underdispersion_buckets()
    print("  6/9 Bucket summary ✓")
    chart_exemplar_receipt()
    print("  7/9 Exemplar receipts ✓")
    chart_sentence_cards()
    print("  8/9 Sentence cards ✓")
    chart_big_summary()
    print("  9/9 Big summary ✓")
    print(f"\nAll visuals saved to: {OUT}/")
