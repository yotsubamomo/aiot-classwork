"""Comparison models: Ridge and Lasso (metric-only, CC-1) and the lecture's p-value backward
elimination (Spec rev 5 「特徵選擇與模型」 對照模型與講義方法對照).

**Ridge and Lasso** (:func:`select_alpha`, :func:`fit_metric_only`)

- All 18 feature groups, on the Ridge/Lasso standardization of
  :func:`hw2.preprocess.fit_preprocessor` (numeric columns centered and scaled with the mean and
  population standard deviation of the rows the fit sees, zipcode one-hot columns kept 0/1), with
  ln(price) as the target and an unpenalized intercept.
- The alpha is chosen **only by training CV**: on the same grouped folds as every other model
  (``training['fold']``), for each fold the standardization and the model are fitted on the
  fold's training rows and the validation rows are scored in USD (exp of the log prediction).
  The selected alpha has the lowest mean CV RMSE (USD) over the grid; ties go to the larger alpha.
  The grid and the whole CV curve are recorded. Test rows are never involved (CC-1 (1)).
- The final model is refitted on the whole training set with the selected alpha. It is a
  **metric-only** model: no prediction interval, no coverage, no live prediction, and its
  coefficients are not exported (so nothing outside the one-time evaluation can score it).
- Ridge minimizes ``‖y − b0 − Xw‖² + alpha·‖w‖²`` (scikit-learn ``Ridge``). Lasso minimizes
  ``(1/2n)‖y − b0 − Xw‖² + alpha·‖w‖₁`` (scikit-learn ``lasso_path`` on centered data with the
  Gram matrix, warm-started down the grid; :data:`LASSO_TOL`).
- Neither takes part in the CV winners (CC-1 (2)); both are scored once by the test gate.

**p-value backward elimination** (:func:`pvalue_backward`, :func:`evaluate_pvalue_backward`)

- The lecture's method, kept as a comparison row only: it yields a **single subset** (no k path),
  is never a CV winner and is never scored on the test set.
- Start with all 18 groups. At each step fit the OLS on ln(price) over the given rows and, for
  every group in the model, compute the **group partial F test** of dropping it
  (``F = ((RSS_without − RSS_with)/q) / (RSS_with/df)``, ``q`` the rank the group adds,
  ``df = n − rank`` of the current model); remove the group with the largest p-value if it exceeds
  :data:`PVALUE_THRESHOLD`; stop when every p-value is ≤ the threshold. Ties (within the
  selection's tie tolerance) remove the group later in canonical order.
- Same selection boundary as the path methods (SR-11): each fold's subset is chosen on that fold's
  training rows only and scored on its validation rows (USD); the canonical subset is chosen once
  on the whole training set (for display). Fold subsets may differ from each other in size.
"""
import time
import warnings
from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import Ridge, lasso_path

from . import metrics, models, ols, preprocess, selection

METRIC_ONLY = ("ridge", "lasso")
LABELS = {"ridge": "Ridge", "lasso": "Lasso", "pvalue_backward": "p-value backward（講義對照）"}
# Grids (Brief §12 HOW: recorded). Four points per decade.
RIDGE_ALPHAS = tuple(float(v) for v in np.logspace(-4, 5, 37))
LASSO_ALPHAS = tuple(float(v) for v in np.logspace(-8, -1, 29))
GRIDS = {"ridge": RIDGE_ALPHAS, "lasso": LASSO_ALPHAS}
LASSO_TOL = 1e-10
LASSO_MAX_ITER = 200_000
PVALUE_THRESHOLD = 0.05
PVALUE_KEY = "pvalue_backward"

OBJECTIVES = {
    "ridge": "||y - b0 - Xw||^2 + alpha*||w||^2 (scikit-learn Ridge)",
    "lasso": "(1/2n)*||y - b0 - Xw||^2 + alpha*||w||_1 (scikit-learn lasso_path, Gram matrix, "
             f"warm start down the grid, tol {LASSO_TOL})",
}
ALPHA_RULE = ("the alpha with the lowest mean CV RMSE (USD) over the grid, on the same grouped "
              "folds of the training set as every other model; ties go to the larger alpha; "
              "test rows never take part")


class ComparisonError(RuntimeError):
    pass


# --- Ridge and Lasso ------------------------------------------------------------------------

def _design(rows: pd.DataFrame, pre: preprocess.Preprocessor):
    X = pre.transform(rows).X
    y = np.log(rows["price"].to_numpy(dtype=float))
    return X, y


def _fit_coefs(name: str, X: np.ndarray, y: np.ndarray, alphas) -> list:
    """[(intercept, coef)] for each alpha in `alphas` (any order), fitted on (X, y)."""
    if name == "ridge":
        out = []
        for a in alphas:
            model = Ridge(alpha=float(a)).fit(X, y)
            out.append((float(model.intercept_), np.asarray(model.coef_, dtype=float)))
        return out
    if name != "lasso":
        raise ComparisonError(f"unknown metric-only model {name}")
    order = np.argsort(np.asarray(alphas, dtype=float))[::-1]          # descending for warm start
    desc = np.asarray(alphas, dtype=float)[order]
    xm, ym = X.mean(axis=0), float(y.mean())
    Xc, yc = X - xm, y - ym
    gram = Xc.T @ Xc
    xy = Xc.T @ yc
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always", ConvergenceWarning)
        _, coefs, _ = lasso_path(Xc, yc, alphas=desc, precompute=gram, Xy=xy,
                                 max_iter=LASSO_MAX_ITER, tol=LASSO_TOL)
    if any(issubclass(w.category, ConvergenceWarning) for w in caught):
        raise ComparisonError("the Lasso did not converge on the alpha grid")
    by_alpha = {}
    for j, a in enumerate(desc):
        w = np.asarray(coefs[:, j], dtype=float)
        by_alpha[float(a)] = (ym - float(xm @ w), w)
    return [by_alpha[float(a)] for a in alphas]


@dataclass(frozen=True)
class MetricOnlyModel:
    """Ridge or Lasso on all 18 groups, fitted on the whole training set with the CV alpha.

    Metric-only (CC-1 (5)): it predicts point values for the one-time test evaluation only; it has
    no interval and offers no live prediction. Its coefficients stay in memory (not exported)."""
    name: str
    alpha: float
    preprocessor: preprocess.Preprocessor
    intercept: float
    coef: np.ndarray

    def predict_usd(self, rows: pd.DataFrame) -> np.ndarray:
        X = self.preprocessor.transform(rows).X
        return np.exp(self.intercept + X @ self.coef)


def fit_metric_only(training: pd.DataFrame, name: str, alpha: float) -> MetricOnlyModel:
    """Refit on the whole training set (all 18 groups, standardized) with the given alpha."""
    pre = preprocess.fit_preprocessor(training, preprocess.FEATURE_GROUPS, standardize=True)
    X, y = _design(training, pre)
    if name == "lasso":
        grid = [a for a in LASSO_ALPHAS if a >= alpha] or [alpha]
        if alpha not in grid:
            grid.append(alpha)
        intercept, coef = _fit_coefs(name, X, y, grid)[grid.index(alpha)]
    else:
        intercept, coef = _fit_coefs(name, X, y, [alpha])[0]
    return MetricOnlyModel(name=name, alpha=float(alpha), preprocessor=pre,
                           intercept=float(intercept), coef=coef)


@dataclass
class AlphaSelection:
    """Training-CV alpha selection of one metric-only model."""
    name: str
    grid: tuple
    folds: list                 # per fold: {fold, n_train, n_valid, per-alpha metrics}
    cv_by_alpha: list           # per grid point: mean MAE, MSE, RMSE, R² (USD)
    alpha: float
    timing_s: dict

    def cv(self) -> dict:
        """``cv`` at the selected alpha (USD; same layout as the OLS entries)."""
        i = self.grid.index(self.alpha)
        records = [{"fold": f["fold"], "n_train": f["n_train"], "n_valid": f["n_valid"],
                    "valid": True, "reason": None, **f["metrics"][i]} for f in self.folds]
        table = {m: np.array([r[m] for r in records], dtype=float) for m in models.CV_METRICS}
        return {"scale": "USD", "n_folds": len(records), "std_ddof": models.CV_STD_DDOF,
                "folds": records,
                "mean": {m: float(v.mean()) for m, v in table.items()},
                "std": {m: float(v.std(ddof=models.CV_STD_DDOF)) for m, v in table.items()}}

    @property
    def at_grid_edge(self) -> str | None:
        if self.alpha == min(self.grid):
            return "lower"
        if self.alpha == max(self.grid):
            return "upper"
        return None

    def to_entry(self) -> dict:
        """One ``baselines`` item: ``cv`` and the alpha; no ``fit`` (no PI fields, no coefficients)."""
        return {
            "model_key": self.name,
            "method": self.name,
            "kind": "metric_only",
            "label": LABELS[self.name],
            "groups": list(preprocess.FEATURE_GROUPS),
            "standardized": True,
            "target": "ln(price)",
            "objective": OBJECTIVES[self.name],
            "alpha": self.alpha,
            "alpha_grid": list(self.grid),
            "alpha_rule": ALPHA_RULE,
            "alpha_at_grid_edge": self.at_grid_edge,
            "cv_by_alpha": self.cv_by_alpha,
            "cv": self.cv(),
            "adj_r2_log": None,
            "adj_r2_note": ("not applicable: the classical Adjusted R² is computed only for OLS "
                            "subset models on the log scale (Spec 「指標與推論」)"),
            "offers": {"prediction_interval": False, "coverage_statistics": False,
                   "live_prediction": False},
            "is_cv_winner_candidate": False,
        }


def select_alpha(training: pd.DataFrame, name: str, grid=None) -> AlphaSelection:
    """Training CV over the grid on the shared grouped folds; returns the selection."""
    grid = tuple(float(a) for a in (GRIDS[name] if grid is None else grid))
    t0 = time.perf_counter()
    fold_ids = sorted(int(f) for f in training["fold"].unique())
    folds = []
    for f in fold_ids:
        is_valid = (training["fold"] == f).to_numpy()
        train_rows, valid_rows = training[~is_valid], training[is_valid]
        pre = preprocess.fit_preprocessor(train_rows, preprocess.FEATURE_GROUPS, standardize=True)
        X, y = _design(train_rows, pre)
        Xv = pre.transform(valid_rows).X
        actual = valid_rows["price"].to_numpy(dtype=float)
        per_alpha = []
        for intercept, coef in _fit_coefs(name, X, y, grid):
            per_alpha.append(metrics.usd_metrics(actual, np.exp(intercept + Xv @ coef)))
        folds.append({"fold": f, "n_train": int(len(train_rows)), "n_valid": int(len(valid_rows)),
                      "metrics": per_alpha})
    cv_by_alpha = []
    for i, a in enumerate(grid):
        row = {"alpha": a}
        for m in models.CV_METRICS:
            row[m] = float(np.mean([f["metrics"][i][m] for f in folds]))
        cv_by_alpha.append(row)
    best = min(cv_by_alpha, key=lambda r: (r["rmse"], -r["alpha"]))
    return AlphaSelection(name=name, grid=grid, folds=folds, cv_by_alpha=cv_by_alpha,
                          alpha=best["alpha"],
                          timing_s={"cv": round(time.perf_counter() - t0, 4)})


def run_metric_only(training: pd.DataFrame) -> tuple[dict, dict, dict]:
    """(selections, models, timing) for Ridge and Lasso: CV alpha, then the whole-training refit."""
    selections, fitted, timing = {}, {}, {}
    for name in METRIC_ONLY:
        t0 = time.perf_counter()
        sel = select_alpha(training, name)
        t1 = time.perf_counter()
        fitted[name] = fit_metric_only(training, name, sel.alpha)
        t2 = time.perf_counter()
        selections[name] = sel
        timing[name] = {"cv": round(t1 - t0, 4), "refit": round(t2 - t1, 4),
                        "total": round(t2 - t0, 4)}
    return selections, fitted, timing


# --- p-value backward elimination ---------------------------------------------------------------

def _rank(gram: selection.GroupGram, groups) -> int:
    if not groups:
        return 0
    idx = np.concatenate([gram.columns[g] for g in groups])
    return int(np.linalg.matrix_rank(gram.G[np.ix_(idx, idx)])) if idx.size else 0


def group_f_tests(gram: selection.GroupGram, groups) -> dict:
    """{group: {f, df_num, df_den, p_value}} for dropping each group from the OLS on `groups`."""
    groups = list(groups)
    rss_full = gram.rss(groups)
    rank_full = _rank(gram, groups)
    df = gram.n - 1 - rank_full                     # the centered design accounts for the intercept
    out = {}
    for g in groups:
        rest = [h for h in groups if h != g]
        q = rank_full - _rank(gram, rest)
        if q <= 0 or df <= 0:
            out[g] = {"f": 0.0, "df_num": int(q), "df_den": int(df), "p_value": 1.0}
            continue
        f = ((gram.rss(rest) - rss_full) / q) / (rss_full / df)
        f = max(float(f), 0.0)
        out[g] = {"f": f, "df_num": int(q), "df_den": int(df),
                  "p_value": float(stats.f.sf(f, q, df))}
    return out


@dataclass
class PValuePath:
    subset: tuple
    steps: list                 # per removal: group, F, df, p-value
    final_tests: dict           # F tests of the groups left


def pvalue_backward(rows: pd.DataFrame, threshold: float = PVALUE_THRESHOLD) -> PValuePath:
    """Backward elimination by group partial F tests on the given rows only."""
    gram = selection.GroupGram(rows)
    current = list(selection.GROUPS)
    steps = []
    while current:
        tests = group_f_tests(gram, current)
        worst = max(v["p_value"] for v in tests.values())
        if worst <= threshold:
            return PValuePath(selection.canonical(current), steps, tests)
        tol = selection.TIE_RTOL * max(abs(worst), 1.0)
        tied = [g for g in current if tests[g]["p_value"] >= worst - tol]
        g = max(tied, key=selection._RANK.get)        # later canonical group first
        steps.append({"removed": g, **tests[g], "k_after": len(current) - 1})
        current.remove(g)
    return PValuePath((), steps, {})


def evaluate_pvalue_backward(training: pd.DataFrame,
                             threshold: float = PVALUE_THRESHOLD) -> dict:
    """The comparison entry: fold-internal subsets scored on the validation rows (USD), the
    canonical subset on the whole training set, and its log-scale fit summary."""
    t0 = time.perf_counter()
    fold_ids = sorted(int(f) for f in training["fold"].unique())
    fold_groups, records = [], []
    for f in fold_ids:
        is_valid = (training["fold"] == f).to_numpy()
        train_rows, valid_rows = training[~is_valid], training[is_valid]
        path = pvalue_backward(train_rows, threshold)
        groups = list(path.subset)
        fold_groups.append(groups)
        record = {"fold": f, "n_train": int(len(train_rows)), "n_valid": int(len(valid_rows)),
                  "groups": groups, "k": len(groups)}
        try:
            model = models.fit_model(train_rows, groups)
        except ols.RankDeficientError as err:
            record.update(valid=False, reason=f"fold_rank_deficient: {err}",
                          **{m: None for m in models.CV_METRICS})
            records.append(record)
            continue
        point, _, _, n_unseen = model.predict_usd(valid_rows)
        record.update(valid=True, reason=None, rank=model.fit.rank,
                      n_columns=model.fit.n_columns, n_valid_unseen_zipcode=n_unseen,
                      **metrics.usd_metrics(valid_rows["price"].to_numpy(dtype=float), point))
        records.append(record)
    t1 = time.perf_counter()
    canonical_path = pvalue_backward(training, threshold)
    canonical = list(canonical_path.subset)
    status = {"state": "valid", "reason": None}
    bad = [r["fold"] for r in records if not r["valid"]]
    if bad:
        status = {"state": "invalid", "reason": "fold_rank_deficient", "folds": bad}
    fit_summary = None
    try:
        fit = models.fit_model(training, canonical).fit
        fit_summary = {"scale": "log", "target": "ln(price)", "n_train": fit.n,
                       "n_columns": fit.n_columns, "rank": fit.rank, "df_resid": fit.df_resid,
                       "r2_log": fit.r2, "adj_r2_log": fit.adj_r2}
    except ols.RankDeficientError as err:
        status = {"state": "invalid", "reason": "canonical_rank_deficient", "detail": str(err)}
    t2 = time.perf_counter()
    cv = {"scale": "USD", "n_folds": len(records), "std_ddof": models.CV_STD_DDOF,
          "folds": records, "mean": None, "std": None}
    if not bad:
        table = {m: np.array([r[m] for r in records], dtype=float) for m in models.CV_METRICS}
        cv["mean"] = {m: float(v.mean()) for m, v in table.items()}
        cv["std"] = {m: float(v.std(ddof=models.CV_STD_DDOF)) for m, v in table.items()}
    return {
        "model_key": PVALUE_KEY,
        "method": PVALUE_KEY,
        "label": LABELS[PVALUE_KEY],
        "role": ("lecture comparison only: a single subset with no k path; never a CV winner "
                 "and never scored on the held-out set"),
        "criterion": "group partial F test of dropping each group from the current OLS on "
                     "ln(price); remove the largest p-value while it exceeds the threshold",
        "threshold": threshold,
        "k": len(canonical),
        "canonical_groups": canonical,
        "fold_groups": fold_groups,
        "folds_agree": sum(1 for g in fold_groups if g == canonical),
        "status": status,
        "cv": cv,
        "fit_summary": fit_summary,
        "elimination": [_jsonable(s) for s in canonical_path.steps],
        "final_p_values": {g: _jsonable(v) for g, v in canonical_path.final_tests.items()},
        "is_cv_winner_candidate": False,
        "timing_s": {"cv": round(t1 - t0, 4), "canonical": round(t2 - t1, 4),
                     "total": round(t2 - t0, 4)},
    }


def _jsonable(d: dict) -> dict:
    return {k: (float(v) if isinstance(v, (float, np.floating)) else v) for k, v in d.items()}
