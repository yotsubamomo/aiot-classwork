"""Feature-group selection paths k = 1…18 for the four path methods (Spec rev 5 「特徵選擇與模型」,
「分割與交叉驗證」 SR-01).

Every method works on **the rows it is given and nothing else** and returns one subset of feature
groups per k = 1…18 (index k − 1), in canonical order. The unit of selection is the feature group:
every step adds or removes a whole group, so consecutive subsets differ by exactly one group.

- **Forward SFS** (:func:`forward_path`): start empty; at each step add the group whose addition
  gives the smallest residual sum of squares (RSS) of the OLS on ln(price) over the given rows.
- **Backward SFS** (:func:`backward_path`): start with all 18 groups; at each step remove the group
  whose removal gives the smallest RSS.
- **RFE** (:func:`rfe_path`): start with all 18 groups; at each step fit the OLS on the current
  groups and remove the least important group. **Group importance** (the aggregation rule the Spec
  leaves to the implementation) is the standard deviation, over the given rows, of the group's
  contribution to the fitted ln(price), ``sd(X_g β_g)``. It is invariant to the scale of the
  columns, equals ``|β|·sd(x)`` (the standardized coefficient) for a one-column group, and treats
  the 69 zipcode columns or the two renovation columns as one block.
- **Lasso path ranking** (:func:`lasso_path_order`): on the Ridge/Lasso standardization of
  :func:`hw2.preprocess.fit_preprocessor` (fitted on the given rows), compute the exact Lasso path
  by LARS; a group enters when any of its columns first has a non-zero coefficient. Groups are
  ranked by entry (earlier entry, i.e. larger alpha, first) and the subset for k is the first k
  groups. A group that never enters ranks after every group that does.

The k used for each method is chosen afterwards by the grouped 5-fold CV RMSE in USD
(:func:`hw2.models.determine_winners`); the in-sample criteria above only order the groups.

**Ties** (equal criterion values within a relative tolerance of :data:`TIE_RTOL`, equal Lasso entry,
or groups that never enter) follow the canonical order (CSV column order): it decides which group is
added first (forward, Lasso) and which is kept longer (backward, RFE remove the later group).

**Rank deficiency** does not stop or skip a selection step (SR-04): the criteria use the
minimum-norm least-squares solution, so a group whose columns are constant or collinear on the
given rows is simply worth nothing. Whether a selected subset can be fitted is decided later by
:func:`hw2.models.evaluate_candidate` (invalid candidate) or :func:`hw2.models.fit_allin`
(experiment-level failure).

**Selection boundary** (:func:`method_paths`): for each fold the path is computed on that fold's
training rows only (the rows of the other folds), so the validation rows never take part in
choosing a subset; the **canonical** path is computed once on the whole training set. A method's
subsets for the same k may therefore differ between folds and from the canonical subset.
"""
import time
import warnings
from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import lars_path

from . import models, preprocess

GROUPS = preprocess.FEATURE_GROUPS
N_GROUPS = len(GROUPS)
_RANK = {g: i for i, g in enumerate(GROUPS)}
TIE_RTOL = 1e-12            # relative tolerance under which two criterion values are a tie

METHOD_NOTES = {
    "forward_sfs": {
        "label": models.METHOD_LABELS["forward_sfs"],
        "start": "no group",
        "step": "add the group whose addition gives the smallest in-sample RSS of the OLS on "
                "ln(price) over the given rows",
        "tie_break": "the group earlier in canonical (CSV column) order is added first",
    },
    "backward_sfs": {
        "label": models.METHOD_LABELS["backward_sfs"],
        "start": "all 18 groups",
        "step": "remove the group whose removal gives the smallest in-sample RSS of the OLS on "
                "ln(price) over the given rows",
        "tie_break": "the group later in canonical order is removed first",
    },
    "rfe": {
        "label": models.METHOD_LABELS["rfe"],
        "start": "all 18 groups",
        "step": "fit the OLS on ln(price) with the current groups over the given rows and remove "
                "the least important group",
        "group_importance": "standard deviation over the given rows of the group's contribution "
                            "X_g b_g to the fitted ln(price) (scale invariant; |b|*sd(x) for a "
                            "one-column group; the zipcode and renovation columns count as one "
                            "block)",
        "tie_break": "the group later in canonical order is removed first",
    },
    "lasso_path": {
        "label": models.METHOD_LABELS["lasso_path"],
        "start": "exact Lasso path by LARS on the Ridge/Lasso standardization fitted on the given "
                 "rows (numeric columns standardized, zipcode one-hot columns 0/1), all columns "
                 "and ln(price) centered",
        "step": "a group enters at the largest alpha at which any of its columns has a non-zero "
                "coefficient; the subset for k is the first k groups to enter",
        "tie_break": "groups entering at the same alpha, and groups that never enter (ranked "
                     "last), follow canonical order",
    },
}
COMMON_NOTE = ("Each path method runs on the training rows of each CV fold (fold-internal "
               "selection; the validation rows never choose a subset) and once on the whole "
               "training set (the canonical subsets shown by the dashboard, used by the live "
               "predictor and, for CV winners, scored on the test set). Every step changes exactly "
               "one feature group. The CV metrics estimate the method's procedure at k, not the "
               "canonical subset itself; k is chosen by the grouped 5-fold CV RMSE in USD.")


def canonical(groups) -> tuple:
    """Groups in canonical order."""
    chosen = set(groups)
    return tuple(g for g in GROUPS if g in chosen)


def _pick(scores: list, prefer_late: bool) -> str:
    """The group with the smallest score; ties (within TIE_RTOL) by canonical order.

    `scores` holds (value, group). With `prefer_late` the tie goes to the group later in canonical
    order (used when removing, so that earlier groups are kept longer)."""
    best = min(v for v, _ in scores)
    tol = TIE_RTOL * max(abs(best), 1.0)
    tied = [g for v, g in scores if v <= best + tol]
    return max(tied, key=_RANK.get) if prefer_late else min(tied, key=_RANK.get)


class GroupGram:
    """Least-squares quantities of the OLS on ln(price) for any union of feature groups, computed
    from the given rows only.

    The encoded columns (zipcode categories fitted on these rows) and ln(price) are centered, which
    accounts for the intercept, and each column is scaled to unit norm, which changes neither the
    RSS nor the fitted contributions. A column that is constant on the rows becomes zero and is
    worth nothing; solutions are minimum-norm, so rank deficiency never raises.
    """

    def __init__(self, rows: pd.DataFrame):
        pre = preprocess.fit_preprocessor(rows, GROUPS)
        X = pre.transform(rows).X
        y = np.log(rows["price"].to_numpy(dtype=float))
        Xc = X - X.mean(axis=0)
        yc = y - y.mean()
        norms = np.linalg.norm(Xc, axis=0)
        Z = Xc / np.where(norms > 0, norms, 1.0)
        self.n = len(rows)
        self.G = Z.T @ Z
        self.b = Z.T @ yc
        self.yy = float(yc @ yc)
        self.columns = {g: np.array([j for j, c in enumerate(pre.columns)
                                     if pre.group_of_column[c] == g], dtype=int) for g in GROUPS}

    def _solve(self, groups):
        idx = np.concatenate([self.columns[g] for g in groups]) if groups else np.array([], int)
        if idx.size == 0:
            return idx, np.zeros(0)
        beta = np.linalg.lstsq(self.G[np.ix_(idx, idx)], self.b[idx], rcond=None)[0]
        return idx, beta

    def rss(self, groups) -> float:
        idx, beta = self._solve(list(groups))
        if idx.size == 0:
            return self.yy
        return max(self.yy - float(self.b[idx] @ beta), 0.0)

    def importance(self, groups) -> dict:
        """{group: sd over the rows of the group's contribution to the fitted ln(price)}."""
        groups = list(groups)
        idx, beta = self._solve(groups)
        out, start = {}, 0
        for g in groups:
            width = self.columns[g].size
            bg = beta[start:start + width]
            cols = self.columns[g]
            var = float(bg @ self.G[np.ix_(cols, cols)] @ bg) / self.n if width else 0.0
            out[g] = float(np.sqrt(max(var, 0.0)))
            start += width
        return out


@dataclass
class Path:
    """One method's path on one set of rows: ``subsets[k - 1]`` has k groups."""
    method: str
    subsets: list
    steps: list = field(default_factory=list)       # per step: the group and its criterion value
    note: dict = field(default_factory=dict)


def forward_path(rows: pd.DataFrame) -> Path:
    gram = GroupGram(rows)
    selected, remaining, subsets, steps = [], list(GROUPS), [], []
    while remaining:
        scores = [(gram.rss(canonical(selected + [g])), g) for g in remaining]
        g = _pick(scores, prefer_late=False)
        selected.append(g)
        remaining.remove(g)
        subsets.append(canonical(selected))
        steps.append({"k": len(selected), "added": g, "rss_log": dict((s[1], s[0]) for s in scores)[g]})
    return Path("forward_sfs", subsets, steps)


def backward_path(rows: pd.DataFrame) -> Path:
    gram = GroupGram(rows)
    current = list(GROUPS)
    subsets = {N_GROUPS: canonical(current)}
    steps = [{"k": N_GROUPS, "removed": None, "rss_log": gram.rss(current)}]
    while len(current) > 1:
        scores = [(gram.rss([h for h in current if h != g]), g) for g in current]
        g = _pick(scores, prefer_late=True)
        current.remove(g)
        subsets[len(current)] = canonical(current)
        steps.append({"k": len(current), "removed": g,
                      "rss_log": dict((s[1], s[0]) for s in scores)[g]})
    return Path("backward_sfs", [subsets[k] for k in range(1, N_GROUPS + 1)], steps)


def rfe_path(rows: pd.DataFrame) -> Path:
    gram = GroupGram(rows)
    current = list(GROUPS)
    subsets = {N_GROUPS: canonical(current)}
    steps = []
    while len(current) > 1:
        imp = gram.importance(current)
        g = _pick([(v, h) for h, v in imp.items()], prefer_late=True)
        current.remove(g)
        subsets[len(current)] = canonical(current)
        steps.append({"k": len(current), "removed": g, "importance": imp[g]})
    return Path("rfe", [subsets[k] for k in range(1, N_GROUPS + 1)], steps)


def lasso_entry(rows: pd.DataFrame) -> dict:
    """{group: (first path index with a non-zero coefficient, entry alpha)}; never → (inf, None).

    The exact Lasso path (LARS with the Lasso modification) on the standardized, centered columns
    of the given rows. ``alpha`` is sklearn's scale (objective (1/2n)·RSS + alpha·‖w‖₁)."""
    pre = preprocess.fit_preprocessor(rows, GROUPS, standardize=True)
    X = pre.transform(rows).X
    X = X - X.mean(axis=0)
    y = np.log(rows["price"].to_numpy(dtype=float))
    y = y - y.mean()
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always", ConvergenceWarning)
        alphas, _, coefs = lars_path(X, y, method="lasso")
    nonzero = coefs != 0.0                                  # (columns, path points)
    first_col = np.where(nonzero.any(axis=1), nonzero.argmax(axis=1), np.iinfo(np.int64).max)
    out = {}
    for g in GROUPS:
        cols = [j for j, c in enumerate(pre.columns) if pre.group_of_column[c] == g]
        first = int(min((first_col[j] for j in cols), default=np.iinfo(np.int64).max))
        if first == np.iinfo(np.int64).max:
            out[g] = (float("inf"), None)
        else:
            out[g] = (first, float(alphas[first - 1]) if first >= 1 else float(alphas[0]))
    out["_warnings"] = [str(w.message) for w in caught]
    return out


def lasso_path_order(rows: pd.DataFrame) -> Path:
    entry = lasso_entry(rows)
    order = sorted(GROUPS, key=lambda g: (entry[g][0], _RANK[g]))
    subsets = [canonical(order[:k]) for k in range(1, N_GROUPS + 1)]
    steps = [{"k": i + 1, "added": g, "entry_alpha": entry[g][1]} for i, g in enumerate(order)]
    note = {"lars_warnings": len(entry["_warnings"])}
    return Path("lasso_path", subsets, steps, note)


PATH_FUNCTIONS = {
    "forward_sfs": forward_path,
    "backward_sfs": backward_path,
    "rfe": rfe_path,
    "lasso_path": lasso_path_order,
}
assert tuple(PATH_FUNCTIONS) == models.PATH_METHODS


def check_path(subsets) -> None:
    """Raise unless subsets[k-1] has k groups and every step changes exactly one group."""
    if len(subsets) != N_GROUPS:
        raise ValueError(f"a path has {N_GROUPS} subsets, got {len(subsets)}")
    for k, s in enumerate(subsets, 1):
        if len(s) != k or len(set(s)) != k or set(s) - set(GROUPS):
            raise ValueError(f"subset for k={k} is {s}")
        if k > 1 and not set(subsets[k - 2]) < set(s):
            raise ValueError(f"subsets k={k - 1} and k={k} differ by more than one group")


@dataclass
class MethodPaths:
    """A method's canonical path (whole training set) and each fold's path (fold training rows)."""
    method: str
    canonical: Path
    folds: list                    # in ascending fold order
    fold_ids: list
    timing_s: dict

    def fold_groups(self, k: int) -> list:
        return [p.subsets[k - 1] for p in self.folds]


def method_paths(training: pd.DataFrame, method: str) -> MethodPaths:
    """Fold-internal paths (each on its fold's training rows only) and the canonical path.

    `training` holds the training rows with their ``fold``. For fold f the method sees only the
    rows with ``fold != f``; the canonical path sees the whole training set."""
    fn = PATH_FUNCTIONS[method]
    fold_ids = sorted(int(f) for f in training["fold"].unique())
    folds, per_fold = [], []
    for f in fold_ids:
        t0 = time.perf_counter()
        path = fn(training[training["fold"] != f])
        per_fold.append(round(time.perf_counter() - t0, 4))
        check_path(path.subsets)
        folds.append(path)
    t0 = time.perf_counter()
    canonical_path = fn(training)
    t_canonical = round(time.perf_counter() - t0, 4)
    check_path(canonical_path.subsets)
    return MethodPaths(method, canonical_path, folds, fold_ids,
                       {"selection_folds": per_fold, "selection_training": t_canonical})


def evaluate_method(training: pd.DataFrame, paths: MethodPaths) -> list:
    """The candidates k = 1…18: grouped CV with each fold's own subset, plus the canonical fit."""
    return [models.evaluate_candidate(training, paths.method, k, paths.canonical.subsets[k - 1],
                                      paths.fold_groups(k))
            for k in range(1, N_GROUPS + 1)]


def run_path_methods(training: pd.DataFrame, methods=models.PATH_METHODS) -> tuple:
    """(candidates, paths, timing): every method's 18 candidates, its paths and its run time.

    timing[method] = {selection_folds: [s per fold], selection_training, selection, evaluation,
    total} in seconds (Q34: measured and recorded, never used to narrow the methods or k)."""
    candidates, all_paths, timing = {}, {}, {}
    for method in methods:
        t0 = time.perf_counter()
        paths = method_paths(training, method)
        t1 = time.perf_counter()
        candidates[method] = evaluate_method(training, paths)
        t2 = time.perf_counter()
        all_paths[method] = paths
        timing[method] = {**paths.timing_s, "selection": round(t1 - t0, 4),
                          "evaluation": round(t2 - t1, 4), "total": round(t2 - t0, 4)}
    return candidates, all_paths, timing
