"""The actual vs predicted figure with every test row's 95% prediction interval, drawn from the
exported results only (#65; DA ``decision-20261019-issue65-labels-figures.md`` F-1 to F-5).

The input is a ``model_data`` object and nothing else: for each authorized OLS-subset model, the
exported per-row ``predicted``, ``lower``, ``upper`` and ``covered`` of ``test[key]``, its
``coverage``, ``n_covered`` and ``n_test``, and ``actual_price`` of ``test_inputs``. Nothing is
fitted, scored or loaded here: the test gate is not touched, the data CSV is not read and no
metric is recomputed; the figure only draws the numbers of the one formal test evaluation, the
same way the dashboard reads them. The encoding is the accepted Q43 one: x = predicted, y =
actual, log scales, the y = x reference line, one vertical PI segment per test row coloured by
``covered``, every one of the ``n_test`` rows (no sampling, no aggregation).

Writing inside the unit (``results/figures/``) is refused for fixture or unofficial results: the
``result_digest`` of the given ``model_data`` must equal the one formal evaluation (TR-01;
DA §9.3 condition 4). Labels are English (no CJK font dependency in the PNG)."""
from __future__ import annotations

from pathlib import Path

import numpy as np

from .paths import FIGURES_DIR, UNIT_DIR

FIGURE_FILE = "eval_actual_vs_predicted_pi.png"
FIGURE_DPI = 110
# The one formal test evaluation (#63; doc/governance/worklog/issue-63.md §5).
FORMAL_RESULT_DIGEST = "b53ff286ae0734add8b272089aba904a1cb7f5aca444a62d356420b25dc3cfc6"
COVERED_COLOR = "#2f4fb0"
MISSED_COLOR = "#c2560e"
ENGLISH_LABELS = {"allin": "All-in baseline", "forward_sfs": "Forward SFS",
                  "backward_sfs": "Backward SFS", "rfe": "RFE", "lasso_path": "Lasso path ranking"}
METHOD_ORDER = ("forward_sfs", "backward_sfs", "rfe", "lasso_path")


class PredictionPlotError(RuntimeError):
    """The model_data cannot be drawn or must not be written where asked."""


def _label(method: str, k) -> str:
    return ENGLISH_LABELS[method] + ("" if method == "allin" else f" k={k}")


def winners_by_test_key(model_data: dict) -> dict[str, list[str]]:
    """{test_model_key: [labels of the CV winners scored as that one model]} (DA D-2)."""
    w = model_data["winners"]
    out: dict[str, list[str]] = {}
    out.setdefault(w["allin"]["test_model_key"], []).append(_label("allin", None))
    for method in METHOD_ORDER:
        mw = w["method_winners"][method]
        out.setdefault(mw["test_model_key"], []).append(_label(method, mw["k"]))
    return out


def panel_data(model_data: dict) -> list[dict]:
    """The exported per-row values of every authorized OLS-subset model (no recomputation)."""
    ti = model_data["test_inputs"]
    actual_col = ti["fields"].index("actual_price")
    actual = np.array([row[actual_col] for row in ti["rows"]], dtype=float)
    shared = winners_by_test_key(model_data)
    overall = model_data["winners"]["overall"]
    overall_label = (_label("allin", None) if overall["method"] == "allin" else
                     _label(overall["method"], model_data["winners"]["method_winners"][overall["method"]]["k"]))
    panels = []
    for key in model_data["winners"]["authorized_test_models"]:
        entry = model_data["test"][key]
        if entry["kind"] != "ols_subset":
            raise PredictionPlotError(f"{key}: not an OLS-subset test entry")
        n = entry["n_test"]
        cols = {c: np.array(entry[c], dtype=float) for c in ("predicted", "lower", "upper")}
        covered = np.array(entry["covered"], dtype=bool)
        if not (len(actual) == n and all(len(v) == n for v in cols.values()) and len(covered) == n):
            raise PredictionPlotError(f"{key}: per-row arrays do not have n_test = {n} rows")
        if np.any(actual <= 0) or any(np.any(v <= 0) for v in cols.values()):
            raise PredictionPlotError(f"{key}: log scales need positive values")
        panels.append({"key": key, "winners": shared.get(key, []),
                       "is_overall": overall["test_model_key"] == key,
                       "overall": overall_label,
                       "actual": actual, "covered": covered, "n_test": n,
                       "coverage": entry["coverage"], "n_covered": entry["n_covered"],
                       "pi_level": entry["pi_level"], **cols})
    return panels


def prediction_figure(model_data: dict):
    """(Figure, info): one panel per authorized OLS-subset model. ``info`` lists, per panel, the
    number of PI segments and points drawn and the colour of each segment (for the tests)."""
    from matplotlib.collections import LineCollection
    from matplotlib.figure import Figure
    from matplotlib.lines import Line2D

    panels = panel_data(model_data)
    fig = Figure(figsize=(6.2 * len(panels), 6.4), layout="constrained")
    axes = np.atleast_1d(fig.subplots(1, len(panels), sharex=True, sharey=True))
    lo = min(min(p["lower"].min(), p["actual"].min()) for p in panels) / 1.15
    hi = max(max(p["upper"].max(), p["actual"].max()) for p in panels) * 1.15
    info = []
    for ax, p in zip(axes, panels):
        colors = np.where(p["covered"], COVERED_COLOR, MISSED_COLOR)
        segments = np.stack([np.column_stack([p["predicted"], p["lower"]]),
                             np.column_stack([p["predicted"], p["upper"]])], axis=1)
        lines = LineCollection(segments, colors=colors, linewidths=0.6, alpha=0.35, zorder=1)
        ax.add_collection(lines)
        points = ax.scatter(p["predicted"], p["actual"], c=colors, s=5, linewidths=0, zorder=2)
        ax.plot([lo, hi], [lo, hi], color="#444444", linestyle="--", linewidth=1, zorder=3)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlim(lo, hi)
        ax.set_ylim(lo, hi)
        ax.set_xlabel("Predicted price (USD, log scale)")
        ax.set_ylabel("Actual price (USD, log scale)")
        ax.grid(True, which="major", alpha=0.3)
        title = " = ".join(p["winners"]) if p["winners"] else p["key"]
        note = f"overall CV winner: {p['overall']}\n" if p["is_overall"] else ""
        ax.set_title(f"{title}\n{note}one test model, scored once ({p['key']})", fontsize=9)
        ax.text(0.02, 0.98,
                f"n_test = {p['n_test']:,} (all rows drawn)\n"
                f"{100 * p['pi_level']:.0f}% PI coverage = {100 * p['coverage']:.2f}% "
                f"({p['n_covered']:,}/{p['n_test']:,})",
                transform=ax.transAxes, va="top", ha="left", fontsize=8.5,
                bbox={"boxstyle": "round", "facecolor": "white", "alpha": 0.85, "edgecolor": "#cccccc"})
        info.append({"key": p["key"], "n_segments": len(lines.get_segments()),
                     "n_points": len(points.get_offsets()), "segment_colors": list(colors),
                     "covered": list(p["covered"])})
    legend = [Line2D([0], [0], color=COVERED_COLOR, marker="o", linewidth=0.8, label="actual inside the 95% PI"),
              Line2D([0], [0], color=MISSED_COLOR, marker="o", linewidth=0.8, label="actual outside the 95% PI"),
              Line2D([0], [0], color="#444444", linestyle="--", label="y = x")]
    fig.legend(handles=legend, loc="outside lower center", ncols=3, fontsize=8.5, frameon=False)
    fig.suptitle("Held-out test set: actual vs predicted price with each row's 95% prediction interval",
                 fontsize=10.5)
    return fig, info


def _inside_unit(path: Path) -> bool:
    path, unit = Path(path).resolve(), UNIT_DIR.resolve()
    return path == unit or unit in path.parents


def is_formal(model_data: dict) -> bool:
    """True only for the exported results of the one formal test evaluation."""
    from .export import result_digest
    return not model_data["meta"].get("fixture") and result_digest(model_data) == FORMAL_RESULT_DIGEST


def save_prediction_figure(model_data: dict, out_dir: Path = FIGURES_DIR, fig=None) -> Path:
    """Write the figure (``fig`` from :func:`prediction_figure`, or drawn here). Inside the unit
    only for the formal evaluation's exported results."""
    out_dir = Path(out_dir)
    if _inside_unit(out_dir) and not is_formal(model_data):
        raise PredictionPlotError("fixture or unofficial results must not be written inside the unit")
    out_dir.mkdir(parents=True, exist_ok=True)
    if fig is None:
        fig, _ = prediction_figure(model_data)
    path = out_dir / FIGURE_FILE
    fig.savefig(path, dpi=FIGURE_DPI, metadata={"Software": None})
    return path
