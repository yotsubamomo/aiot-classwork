"""Explanation of the final model (Deployment; Brief §8 Q25, Spec rev 5 「診斷與解釋」).

Training rows only (H-3; DA TR-01, I-1: 「Fit」 means the training set). Two parts:

- **Coefficients** (依老師補充建議): the OLS is fitted on ln(price) with raw-scale features, so a
  coefficient b is read as ``100·(exp(b) − 1)`` percent change of the predicted price (the
  conditional-median estimate exp(ŷ_log)) per one unit of the feature, the other columns held
  fixed. A zipcode one-hot coefficient is the percent difference from the **baseline zipcode**
  (the first sorted training category, which has no column). The *standardized reading* is the
  percent change per one **training standard deviation** of the column, ``100·(exp(b·sd) − 1)``,
  which makes features with different units comparable (the OLS itself is not standardized; the
  Ridge/Lasso standardization is not used here). Standard errors are the classical OLS ones,
  √(s²·[(XᵀX)⁻¹]_jj); they assume the classical assumptions (see the diagnostics) and ignore the
  feature-selection step, so they are descriptive.
- **Permutation importance** (專案延伸; only to explain, never to select features — DA B-6,
  Brief §3.4): for each feature group, the group's encoded columns are permuted together across
  the training rows (one permutation of the row order per repeat), and the increase of the
  in-sample RMSE on the **log scale** (ln(price), the scale the OLS is fitted on) over the
  unpermuted model is recorded; groups are ranked by it. The increase of the in-sample RMSE in USD
  (exp of the log prediction) is reported alongside for reference: the OLS does not minimize the
  USD error, so a permutation can lower it (a negative value) and it is not used for the ranking.
  :data:`N_REPEATS` repeats from a fixed random stream (``SeedSequence([SEED, 2])``; the split and
  the folds use ``[SEED, 0]`` and ``[SEED, 1]``). It measures how much the fitted model relies on a
  group on the training rows; correlated groups share importance, and it is not a causal effect.
"""
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from . import data, deployment, metrics, ols, preprocess
from .diagnostics import FIGURE_DPI, check_output_dir, new_figure, write_csv
from .paths import FIGURES_DIR, SEED, TABLES_DIR

N_REPEATS = 10
PERMUTATION_STREAM = 2
FIGURE_FILES = {"coefficients": "explain_coefficients_percent_effects.png",
                "permutation": "explain_permutation_importance.png"}
TABLE_FILES = {"coefficients": "final_model_coefficients.csv",
               "permutation": "permutation_importance_training.csv"}


def coefficient_table(prepared: data.PreparedData, pipeline) -> pd.DataFrame:
    """Every coefficient of the final model with its percent readings (training rows only)."""
    training = deployment.training_rows(prepared)
    fit = pipeline.fit
    X = pipeline.preprocessor.transform(training).X
    owner = pipeline.preprocessor.group_of_column
    se = np.sqrt(fit.s2 * np.diag(fit.xtx_inv))
    t = fit.coef / se
    p = 2 * stats.t.sf(np.abs(t), fit.df_resid)
    rows = []
    for j, name in enumerate(fit.column_names):
        b, s = float(fit.coef[j]), float(se[j])
        if j == 0:
            kind, group, sd = "intercept", "", None
        else:
            col = X[:, j - 1]
            group = owner[name]
            if name.startswith(preprocess.ZIPCODE_PREFIX):
                kind, sd = "one-hot vs baseline zipcode " + str(pipeline.preprocessor.zipcode_baseline), None
            elif name == "is_renovated":
                kind, sd = "flag (0/1)", None
            else:
                kind, sd = "numeric", float(col.std())
        lo, hi = b - fit.t_crit * s, b + fit.t_crit * s
        rows.append({
            "column": name, "group": group, "kind": kind, "coef_log": b, "std_error": s,
            "t": float(t[j]), "p_value": float(p[j]),
            "pct_per_unit": None if j == 0 else 100 * float(np.expm1(b)),
            "pct_per_unit_ci95_low": None if j == 0 else 100 * float(np.expm1(lo)),
            "pct_per_unit_ci95_high": None if j == 0 else 100 * float(np.expm1(hi)),
            "train_sd": sd,
            "pct_per_train_sd": None if sd is None else 100 * float(np.expm1(b * sd)),
        })
    return pd.DataFrame(rows)


def permutation_importance(prepared: data.PreparedData, pipeline, n_repeats: int = N_REPEATS,
                           seed: int = SEED) -> tuple[pd.DataFrame, dict]:
    """(table, baseline) of the group permutation importance on the training rows.

    The table is ranked by the mean increase of the log-scale RMSE; the USD RMSE increase is a
    reference column. `baseline` holds the unpermuted in-sample RMSE on both scales."""
    training = deployment.training_rows(prepared)
    X = pipeline.preprocessor.transform(training).X
    columns = list(pipeline.preprocessor.columns)
    owner = pipeline.preprocessor.group_of_column
    actual = training["price"].to_numpy(dtype=float)
    y_log = np.log(actual)
    coef = pipeline.fit.coef

    def errors(Xm):
        pred_log = ols.design(Xm) @ coef
        return (float(np.sqrt(np.mean((y_log - pred_log) ** 2))),
                metrics.usd_metrics(actual, np.exp(pred_log))["rmse"])

    base_log, base_usd = errors(X)
    rng = np.random.default_rng(np.random.SeedSequence([seed, PERMUTATION_STREAM]))
    rows = []
    for g in pipeline.groups:
        idx = [j for j, c in enumerate(columns) if owner[c] == g]
        inc_log, inc_usd = [], []
        for _ in range(n_repeats):
            order = rng.permutation(len(X))
            Xp = X.copy()
            Xp[:, idx] = X[order][:, idx]
            e_log, e_usd = errors(Xp)
            inc_log.append(e_log - base_log)
            inc_usd.append(e_usd - base_usd)
        inc_log, inc_usd = np.array(inc_log), np.array(inc_usd)
        ddof = 1 if n_repeats > 1 else 0
        rows.append({"group": g, "n_columns": len(idx), "n_repeats": n_repeats,
                     "log_rmse_increase_mean": float(inc_log.mean()),
                     "log_rmse_increase_std": float(inc_log.std(ddof=ddof)),
                     "log_rmse_increase_pct_of_baseline": float(100 * inc_log.mean() / base_log),
                     "usd_rmse_increase_mean_reference": float(inc_usd.mean()),
                     "usd_rmse_increase_std_reference": float(inc_usd.std(ddof=ddof))})
    table = pd.DataFrame(rows).sort_values("log_rmse_increase_mean", ascending=False,
                                           kind="stable").reset_index(drop=True)
    table.insert(0, "rank", np.arange(1, len(table) + 1))
    return table, {"log_rmse": base_log, "usd_rmse": base_usd, "n_rows": int(len(training))}


def write_tables(coefficients: pd.DataFrame, permutation: pd.DataFrame,
                 out_dir: Path = TABLES_DIR, official: bool = False) -> list:
    out_dir = check_output_dir(out_dir, official)
    return [write_csv(out_dir / TABLE_FILES["coefficients"], coefficients),
            write_csv(out_dir / TABLE_FILES["permutation"], permutation)]


def figures(coefficients: pd.DataFrame, permutation: pd.DataFrame, baseline: dict,
            label: str) -> dict:
    title = label.replace("Lasso 路徑排序", "Lasso path ranking")
    out = {}
    numeric = coefficients[coefficients["pct_per_train_sd"].notna()].copy()
    numeric = numeric.sort_values("pct_per_train_sd")
    zips = coefficients[coefficients["kind"].str.startswith("one-hot")].sort_values("pct_per_unit")
    fig, axes = new_figure(1, 2, figsize=(12, 5.2), gridspec_kw={"width_ratios": [1.1, 1]})
    sd = numeric["train_sd"].to_numpy()
    b = numeric["coef_log"].to_numpy()
    half = np.log1p(numeric["pct_per_unit_ci95_high"].to_numpy() / 100) - b      # t_crit * SE
    lo, hi = 100 * np.expm1((b - half) * sd), 100 * np.expm1((b + half) * sd)
    mid = numeric["pct_per_train_sd"].to_numpy()
    axes[0].barh(numeric["column"], mid, color=["#1E40AF" if v >= 0 else "#B45309" for v in mid])
    axes[0].errorbar(mid, np.arange(len(mid)), xerr=[mid - lo, hi - mid], fmt="none",
                     ecolor="#0F172A", lw=0.8)
    axes[0].axvline(0, color="#0F172A", lw=0.8)
    axes[0].set_xlabel("% change of predicted price per +1 training SD (others fixed)")
    axes[0].set_title("Numeric columns: standardized reading", fontsize=10)
    if len(zips):
        axes[1].bar(np.arange(len(zips)), zips["pct_per_unit"], color="#0E7490")
        axes[1].axhline(0, color="#0F172A", lw=0.8)
        axes[1].set_xticks([])
        axes[1].set_xlabel(f"{len(zips)} zipcode one-hot columns, sorted")
        axes[1].set_ylabel("% difference vs the baseline zipcode")
        axes[1].set_title(f"Zipcode effects relative to the baseline "
                          f"{zips['kind'].iloc[0].split()[-1]}", fontsize=10)
    else:
        axes[1].axis("off")
    fig.suptitle(f"Coefficients of the final model (ln(price), fitted on the training set) - "
                 f"{title}; associations, not causal effects", fontsize=10)
    out["coefficients"] = fig

    fig, ax = new_figure(figsize=(8, 5))
    perm = permutation.sort_values("log_rmse_increase_mean")
    ax.barh(perm["group"], perm["log_rmse_increase_mean"], xerr=perm["log_rmse_increase_std"],
            color="#6D28D9", ecolor="#0F172A")
    ax.set_xlabel(f"increase of the training RMSE of ln(price) when the group is permuted "
                  f"(baseline {baseline['log_rmse']:.4f})")
    ax.set_title(f"Permutation importance on the training set ({int(perm['n_repeats'].iloc[0])} "
                 f"repeats) - {title}\nexplanation only (not used for selection); not causal",
                 fontsize=10)
    out["permutation"] = fig
    return out


def save_figures(figs: dict, out_dir: Path = FIGURES_DIR, official: bool = False) -> list:
    out_dir = check_output_dir(out_dir, official)
    paths = []
    for key, fig in figs.items():
        path = out_dir / FIGURE_FILES[key]
        fig.savefig(path, dpi=FIGURE_DPI, metadata={"Software": None})
        paths.append(path)
    return paths
