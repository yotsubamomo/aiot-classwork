"""OLS candidates on feature-group subsets: grouped CV in USD, the canonical fit, the rank-deficiency
semantics, the All-in baseline and the CV winners (Spec rev 5 「分割與交叉驗證」「特徵選擇與模型」
「指標與推論」).

A **candidate** is one (method, k) with its canonical subset (computed on the whole training set)
and, per fold, that fold's subset (computed on the fold's training rows; for the All-in baseline
every subset is all 18 groups). For each fold the preprocessing is fitted on the fold's training
rows only, OLS is fitted on them on the log scale, and the validation rows are scored in USD.

Rank deficiency (SR-04, SR-10), never handled by dropping columns, merging categories or changing
the encoding:

1. **Legal encoding result** — a zipcode absent from a fold's training rows has no column in that
   fold; validation rows with it are encoded as the baseline. Each fit records its categories and
   the number of rows encoded as the baseline because their zipcode was unseen.
2. **Invalid candidate** — the design (intercept included) is rank deficient on a fold's training
   rows (that fold is invalid, with the reason), or on the whole training set for the canonical
   fit (``canonical_rank_deficient``, no ``fit``). An invalid candidate takes no part in the CV
   winners and offers no live prediction.
3. **Experiment-level failure** — the All-in baseline is invalid, a method has no valid
   candidate, or the overall CV winner cannot be determined: :class:`ExperimentFailure` stops the
   run and lists every invalid candidate with its reason.
"""
import time
from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from . import metrics, ols, preprocess

ALLIN = "allin"
PATH_METHODS = ("forward_sfs", "backward_sfs", "rfe", "lasso_path")
METHOD_ORDER = (ALLIN, *PATH_METHODS)          # fixed tie-break order (Brief §5: A, B, C, D, E)
METHOD_LABELS = {
    ALLIN: "All-in baseline",
    "forward_sfs": "Forward SFS",
    "backward_sfs": "Backward SFS",
    "rfe": "RFE",
    "lasso_path": "Lasso 路徑排序",
}
CV_METRICS = ("mae", "mse", "rmse", "r2")
CV_STD_DDOF = 1


class ExperimentFailure(RuntimeError):
    """Structural failure of the experiment (SR-04 third class): stop and route to the acceptor."""

    def __init__(self, message: str, invalid_candidates: list):
        lines = [message] + [f"  - {c['model_key']}: {c['reason']}" for c in invalid_candidates]
        super().__init__("\n".join(lines))
        self.invalid_candidates = invalid_candidates


def model_key(method: str, k: int) -> str:
    """Identifier of an OLS subset model: ``allin`` or ``<method>_k<k>``."""
    return ALLIN if method == ALLIN else f"{method}_k{k:02d}"


@dataclass(frozen=True)
class OLSModel:
    """An OLS subset model fitted on some rows: its fitted preprocessing and its fit."""
    groups: tuple[str, ...]
    preprocessor: preprocess.Preprocessor
    fit: ols.OLSFit

    def transform(self, rows: pd.DataFrame) -> preprocess.TransformResult:
        return self.preprocessor.transform(rows)

    def predict_usd(self, rows: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, np.ndarray, int]:
        """(point, lower, upper, n_unseen_zipcode) in USD for raw rows."""
        tr = self.transform(rows)
        point, lower, upper = ols.usd_interval(self.fit, tr.X)
        return point, lower, upper, tr.n_unseen_zipcode

    def to_fit_dict(self) -> dict:
        """``fit`` of the contract: log-scale statistics and everything the PI needs."""
        f = self.fit
        pre = self.preprocessor
        return {
            "scale": "log",
            "target": "ln(price)",
            "n_train": f.n,
            "n_columns": f.n_columns,
            "rank": f.rank,
            "df_resid": f.df_resid,
            "r2_log": f.r2,
            "adj_r2_log": f.adj_r2,
            "s2": f.s2,
            "pi_level": ols.PI_LEVEL,
            "t_crit": f.t_crit,
            "groups": list(self.groups),
            "uses_source_features": source_features_of(self.groups),
            "encoded_columns": list(pre.columns),
            "coef_names": list(f.column_names),
            "coef": [float(v) for v in f.coef],
            "xtx_inv": [[float(v) for v in row] for row in f.xtx_inv],
            "zipcode_categories": list(pre.zipcode_categories),
            "zipcode_baseline": pre.zipcode_baseline,
        }


def source_features_of(groups) -> list:
    """Raw source features needed to encode the groups (``yr_renovated`` also uses ``yr_built``)."""
    out = []
    for g in groups:
        for f in ((g, "yr_built") if g == "yr_renovated" else (g,)):
            if f not in out:
                out.append(f)
    return [f for f in preprocess.SOURCE_FEATURES if f in out]


def fit_model(rows: pd.DataFrame, groups) -> OLSModel:
    """Fit preprocessing and OLS on `rows` only. Raises ols.RankDeficientError."""
    pre = preprocess.fit_preprocessor(rows, groups)
    tr = pre.transform(rows)
    fit = ols.fit_ols(tr.X, np.log(rows["price"].to_numpy(dtype=float)), pre.columns)
    return OLSModel(groups=pre.groups, preprocessor=pre, fit=fit)


@dataclass
class Candidate:
    method: str
    k: int
    canonical_groups: tuple[str, ...]
    fold_groups: list                     # per fold, the groups used in that fold
    folds: list                           # per-fold records (dicts)
    model: OLSModel | None                # canonical fit on the whole training set
    status: dict
    is_method_winner: bool = False
    timing_s: dict = field(default_factory=dict)

    @property
    def key(self) -> str:
        return model_key(self.method, self.k)

    @property
    def valid(self) -> bool:
        return self.status["state"] == "valid"

    @property
    def cv_rmse(self) -> float | None:
        return self.cv()["mean"]["rmse"] if self.valid else None

    def cv(self) -> dict:
        valid = all(f["valid"] for f in self.folds)
        out = {"scale": "USD", "n_folds": len(self.folds), "std_ddof": CV_STD_DDOF,
               "folds": self.folds, "mean": None, "std": None}
        if valid:
            table = {m: np.array([f[m] for f in self.folds], dtype=float) for m in CV_METRICS}
            out["mean"] = {m: float(v.mean()) for m, v in table.items()}
            out["std"] = {m: float(v.std(ddof=CV_STD_DDOF)) for m, v in table.items()}
        return out

    def to_entry(self) -> dict:
        """One item of ``methods`` (or ``baselines.allin``): groups, status, ``cv``, ``fit``."""
        canonical = list(self.canonical_groups)
        return {
            "model_key": self.key,
            "method": self.method,
            "k": self.k,
            "canonical_groups": canonical,
            "fold_groups": [list(g) for g in self.fold_groups],
            "folds_agree": sum(1 for g in self.fold_groups if list(g) == canonical),
            "status": dict(self.status),
            "cv": self.cv(),
            "fit": self.model.to_fit_dict() if self.model is not None else None,
            "is_method_winner": self.is_method_winner,
        }


def evaluate_candidate(training: pd.DataFrame, method: str, k: int, canonical_groups,
                       fold_groups=None) -> Candidate:
    """Grouped CV in USD with the given per-fold subsets, plus the canonical fit.

    `training` holds the training rows with their ``fold``; `fold_groups[f]` is fold f's subset
    (default: the canonical subset in every fold). Never raises for rank deficiency: the
    candidate is returned with ``status = invalid`` and the reason.
    """
    t0 = time.perf_counter()
    canonical = tuple(g for g in preprocess.FEATURE_GROUPS if g in set(canonical_groups))
    fold_ids = sorted(int(f) for f in training["fold"].unique())
    if fold_groups is None:
        fold_groups = [canonical] * len(fold_ids)
    fold_groups = [tuple(g for g in preprocess.FEATURE_GROUPS if g in set(gs))
                   for gs in fold_groups]
    folds = []
    for fold, groups in zip(fold_ids, fold_groups):
        is_valid = (training["fold"] == fold).to_numpy()
        train_rows, valid_rows = training[~is_valid], training[is_valid]
        record = {"fold": fold, "n_train": int(len(train_rows)), "n_valid": int(len(valid_rows)),
                  "groups": list(groups)}
        try:
            model = fit_model(train_rows, groups)
        except ols.RankDeficientError as err:
            record.update(valid=False, reason=f"fold_rank_deficient: {err}",
                          rank=err.rank, n_columns=err.n_columns,
                          **{m: None for m in CV_METRICS})
            folds.append(record)
            continue
        point, _, _, n_unseen = model.predict_usd(valid_rows)
        record.update(valid=True, reason=None, rank=model.fit.rank,
                      n_columns=model.fit.n_columns,
                      zipcode_categories=list(model.preprocessor.zipcode_categories),
                      zipcode_baseline=model.preprocessor.zipcode_baseline,
                      n_valid_unseen_zipcode=n_unseen,
                      **metrics.usd_metrics(valid_rows["price"].to_numpy(dtype=float), point))
        folds.append(record)
    t1 = time.perf_counter()
    status = {"state": "valid", "reason": None}
    model = None
    bad = [f["fold"] for f in folds if not f["valid"]]
    if bad:
        status = {"state": "invalid", "reason": "fold_rank_deficient", "folds": bad}
    try:
        model = fit_model(training, canonical)
    except ols.RankDeficientError as err:
        reason = {"state": "invalid", "reason": "canonical_rank_deficient", "detail": str(err)}
        if bad:
            reason["folds"] = bad
        status = reason
    t2 = time.perf_counter()
    return Candidate(method=method, k=k, canonical_groups=canonical, fold_groups=fold_groups,
                     folds=folds, model=model, status=status,
                     timing_s={"cv": round(t1 - t0, 4), "canonical_fit": round(t2 - t1, 4)})


def _invalid_list(candidates) -> list:
    return [{"model_key": c.key, "reason": c.status.get("reason"),
             "detail": c.status.get("detail"), "folds": c.status.get("folds")}
            for c in candidates if not c.valid]


def fit_allin(training: pd.DataFrame) -> Candidate:
    """The All-in baseline: one OLS on all 18 feature groups (no k path; k = 18).

    Rank deficiency of the All-in baseline in any fold or on the whole training set is an
    experiment-level failure (SR-04): it means the data or the fixed preprocessing is broken (for
    example ``sqft_basement`` entering the model). Raises :class:`ExperimentFailure`.
    """
    allin = evaluate_candidate(training, ALLIN, len(preprocess.FEATURE_GROUPS),
                               preprocess.FEATURE_GROUPS)
    if not allin.valid:
        raise ExperimentFailure("the All-in baseline is rank deficient (experiment-level "
                                "failure; route to the acceptor, do not drop any feature group)",
                                _invalid_list([allin]))
    allin.is_method_winner = True                 # the All-in baseline is its own CV winner
    return allin


def determine_winners(allin: Candidate, path_candidates: dict) -> dict:
    """``winners``: method CV winners, the overall CV winner and the authorized test set.

    `path_candidates` maps a path method to its candidates (k = 1…18 once #62 exists). A method
    CV winner is the valid candidate with the lowest CV RMSE (ties: smaller k). The overall CV
    winner is the lowest CV RMSE among the method winners and the All-in baseline (ties: the fixed
    order of :data:`METHOD_ORDER`). Metric-only models (Ridge, Lasso) never compete.

    Until every path method is present the result is ``complete: false`` with ``overall: null``;
    the test gate refuses an incomplete selection. Raises :class:`ExperimentFailure` when a
    present method has no valid candidate or the overall winner cannot be determined.
    """
    unknown = set(path_candidates) - set(PATH_METHODS)
    if unknown:
        raise ValueError(f"unknown path methods {sorted(unknown)}")
    if not allin.valid:
        raise ExperimentFailure("the All-in baseline is invalid", _invalid_list([allin]))
    method_winners = {}
    for method in PATH_METHODS:
        if method not in path_candidates:
            continue
        candidates = path_candidates[method]
        for c in candidates:
            c.is_method_winner = False
        valid = [c for c in candidates if c.valid]
        if not valid:
            raise ExperimentFailure(f"method {method} has no valid candidate, so no CV winner",
                                    _invalid_list([c for m in path_candidates.values()
                                                   for c in m]))
        winner = min(valid, key=lambda c: (c.cv_rmse, c.k))
        winner.is_method_winner = True
        method_winners[method] = {"model_key": winner.key, "k": winner.k,
                                  "cv_rmse": winner.cv_rmse}
    complete = len(method_winners) == len(PATH_METHODS)
    overall = None
    if complete:
        pool = [(ALLIN, allin.key, allin.cv_rmse)] + [
            (m, w["model_key"], w["cv_rmse"]) for m, w in method_winners.items()]
        if any(r is None or not np.isfinite(r) for _, _, r in pool):
            raise ExperimentFailure("the overall CV winner cannot be determined (missing CV RMSE)",
                                    _invalid_list([c for m in path_candidates.values()
                                                   for c in m]))
        method, key, rmse = min(pool, key=lambda t: (t[2], METHOD_ORDER.index(t[0])))
        overall = {"model_key": key, "method": method, "cv_rmse": rmse}
    authorized = [allin.key] + [w["model_key"] for w in method_winners.values()]
    if overall is not None:
        authorized.append(overall["model_key"])
    authorized = sorted(set(authorized), key=lambda k: authorized.index(k))
    return {
        "complete": complete,
        "selection_metric": "CV RMSE (USD), grouped 5-fold on the training set",
        "tie_break": {"method_winner": "smaller k",
                      "overall": "fixed method order " + " > ".join(METHOD_ORDER)},
        "allin": {"model_key": allin.key, "cv_rmse": allin.cv_rmse},
        "method_winners": method_winners,
        "pending_methods": [m for m in PATH_METHODS if m not in method_winners],
        "overall": overall,
        "authorized_test_models": authorized,
        "note": ("Test evaluation is authorized only for these OLS subset models (each scored "
                 "once) plus the metric-only Ridge and Lasso (CC-1); no other model is scored on "
                 "the test set, and test results never change these winners."),
    }
