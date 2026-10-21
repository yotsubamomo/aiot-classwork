"""Generic Python reference for the V2 Exploratory run (Spec V2 「通用 Python 參照」; #74 V2-T1:
All-in; #75 V2-T2: the four path methods, winners, Lasso degeneracy and the dependency diagnostic).

**Test-only.** This module produces reference results for the Node tests of the browser engine
(``assets/explore_engine.js``, ``assets/explore_load.js``). Nothing on the formal analysis path
imports it: not the notebook, not any other ``hw2`` module, not the report or the packaging
(``tests/test_explore_static.py`` checks this). It never reads ``model_data`` and depends on no JS
result: it re-implements the load contract, the split, the three-layer preprocessing boundary and
the candidates from the Spec, and reuses the formal package's group-generic mathematics instead of
writing them again:

- :func:`hw2.ols.fit_ols` — OLS on ``[1, X]`` with the actual rank (column-pivoted QR of the
  column-equilibrated design), ``(XᵀX)⁻¹``, ``s²``, ``df_resid``, ``R²``, Adjusted ``R²`` with the
  actual rank, ``t(0.975, df_resid)``; raises :class:`hw2.ols.RankDeficientError`;
- :func:`hw2.ols.log_interval` — ``ŷ ± t·√(s²(1 + x₀ᵀ(XᵀX)⁻¹x₀))``; despite its name it evaluates
  the formula on whatever scale ``y`` has; the Exploratory run models the original target (no log,
  no exp), so its output is used as is;
- :func:`hw2.metrics.usd_metrics` and :func:`hw2.metrics.coverage_stats` — MAE, MSE, RMSE, R² and
  the closed-interval coverage, unit-free despite the name;
- :class:`hw2.selection.GroupGram` — its ``rss`` (the RSS step of Forward / Backward SFS) and
  ``importance`` (RFE's ``sd(X_g β_g)``) methods, on a Gram object built here from any encoded
  table (the formal constructor reads King County rows, so only the constructor is re-expressed);
  :data:`hw2.selection.TIE_RTOL` for ties;
- the formal Lasso path engine, :func:`sklearn.linear_model.lars_path` with ``method="lasso"`` on
  the formal standardization rule (numeric columns centred and scaled by the population standard
  deviation, one-hot columns 0/1, then every column centred; :func:`hw2.preprocess.fit_preprocessor`)
  and the formal entry rule (a group enters at the knot alpha before its first non-zero coefficient;
  :func:`hw2.selection.lasso_entry`);
- :data:`hw2.models.METHOD_ORDER`, :data:`hw2.models.PATH_METHODS`, :func:`hw2.models.model_key`
  and the winner rules of :func:`hw2.models.determine_winners` (method winner: lowest CV RMSE, ties
  to the smaller k; overall: lowest CV RMSE among the method winners and All-in, ties in method
  order; winners with the same canonical subset are one model, scored once).

No King County specific function (CSV schema, derived features, ln(price), grouped split) is used;
:func:`canonical_paths` takes a ready encoded table so that ``tests/test_explore_kc_consistency.py``
can feed it the formal King County training table.

Rules (the same as the JS files; see their headers for the full text):

1. **Load contract** (:func:`load_csv`): CSV structure only, any row; no distribution, distinct
   count or variance of a column; no kept / excluded state.
2. **Split** (:func:`make_split`): mulberry32 with Fisher–Yates; ``mulberry32(seed)`` for the
   80/20 split (``n_test = floor(0.2 n + 0.5)`` clamped to ``[1, n − 1]``; the first ``n_test``
   shuffled rows are the test rows), ``mulberry32(seed + 1)`` for the folds of the training rows
   (shuffled position ``q`` → fold ``q mod 5``).
3. **Training-set layer** (:func:`train_decisions`): on the training rows only, a categorical
   column with more than 20 distinct values → ``EXCLUDED_TOO_MANY_LEVELS``, one distinct value →
   ``EXCLUDED_CONSTANT``; kept columns in CSV order are the feature groups.
4. **Fold layer** (:func:`fit_encoding`): levels in first-appearance order over the given rows,
   the first one is the baseline (no column); unseen levels are the baseline and counted. Every
   path method runs on each fold's training rows (fold-internal selection) and once on the whole
   training set (canonical paths); the Lasso standardization is fitted on the same rows.
5. **A-1**: full rank and ``df_resid ≥ 3`` on every fold's training rows and on the whole training
   set, else ``INVALID_MODEL`` with the rule and the fold.
6. **A-2**: the Lasso path stops at the first active-set degeneracy (an entering column whose
   residual on the active columns is below :data:`LARS_DEGENERATE_RTOL` of its norm, or below
   sklearn's own pivot limit :data:`LARS_PIVOT_ATOL`), or ends with groups that never entered; the
   groups that entered before are the actual path, the others are shown after them in CSV order
   only, and every k beyond the entered groups is ``INVALID_MODEL`` / ``lasso_path_degenerate``.
7. **A-3** (:func:`dependency_groups`): the All-in design of the whole training set (intercept
   first, then the encoded columns in canonical order), equilibrated, is scanned in that order; a
   column within :data:`DEPENDENCY_TOL` of the span of the earlier independent columns closes one
   linear relation, reported with every column it involves and their feature groups.
8. **CV**: arithmetic mean of the five fold metrics, sample standard deviation (ddof
   :data:`CV_STD_DDOF`, equal to :data:`hw2.models.CV_STD_DDOF`).
9. **Test**: read only after the winners are fixed, only for the winners' canonical fits.
"""
from __future__ import annotations

import contextlib
import hashlib
import io
import math
import re
import warnings

import numpy as np
from scipy import linalg
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import lars_path

from . import metrics, models, ols, selection

REFERENCE_VERSION = "explore-reference 2 (V2-T2: five methods)"
SEED = 42
TEST_FRACTION = 0.2
N_FOLDS = 5
MAX_LEVELS = 20
MIN_DF_RESID = 3
PI_LEVEL = 0.95
CV_STD_DDOF = 1
LIMITS = {"max_rows": 50000, "max_columns": 60, "min_rows": 20}
METRICS = ("mae", "mse", "rmse", "r2")
METHOD_ORDER = models.METHOD_ORDER            # allin, forward_sfs, backward_sfs, rfe, lasso_path
PATH_METHODS = models.PATH_METHODS
TIE_RTOL = selection.TIE_RTOL
LARS_MAX_ITER = 500                           # sklearn's lars_path default, as the formal call uses
LARS_DEGENERATE_RTOL = 1e-6                   # entering column: residual / norm on the active set
LARS_PIVOT_ATOL = 1e-7                        # sklearn's own Cholesky pivot limit (absolute)
EPS = float(np.finfo(float).eps)
RELATION_ZERO = 1e-9                          # a normalised relation coefficient below this is 0

_NUMBER = re.compile(r"[+-]?(?:[0-9]+\.?[0-9]*|\.[0-9]+)(?:[eE][+-]?[0-9]+)?")
_SPACE = " \t\r\n\f\v"
_M32 = 0xFFFFFFFF


def trim(cell: str) -> str:
    return cell.strip(_SPACE)


def is_number_literal(cell: str) -> bool:
    return _NUMBER.fullmatch(cell) is not None and math.isfinite(float(cell))


def _reject(reason: str, detail: dict, sha: str | None) -> dict:
    return {"ok": False, "reason": reason, "detail": detail, "sha256": sha}


def _read_records(text: str, max_rows: int):
    """RFC 4180 records (same rules as readRecords in assets/explore_load.js)."""
    records: list[list[str]] = []
    record: list[tuple[str, bool]] = []
    field: list[str] = []
    quoted = after_quote = False
    at_start = True
    non_blank = 0
    i, n = 0, len(text)

    def end_field():
        nonlocal field, quoted, at_start, after_quote
        record.append(("".join(field), quoted))
        field, quoted, at_start, after_quote = [], False, True, False

    def end_record() -> bool:
        nonlocal record, non_blank
        end_field()
        blank = len(record) == 1 and not record[0][1] and trim(record[0][0]) == ""
        if not blank:
            records.append([f for f, _ in record])
            non_blank += 1
        record = []
        return non_blank - 1 > max_rows

    while i < n:
        ch = text[i]
        if quoted and not after_quote:
            if ch == '"':
                if i + 1 < n and text[i + 1] == '"':
                    field.append('"')
                    i += 2
                    continue
                after_quote = True
                i += 1
                continue
            field.append(ch)
            i += 1
            continue
        if ch == ",":
            end_field()
            i += 1
            continue
        if ch in "\r\n":
            if ch == "\r" and i + 1 < n and text[i + 1] == "\n":
                i += 1
            i += 1
            if end_record():
                return None, ("TOO_LARGE", {"rows_over": max_rows})
            continue
        if after_quote:
            if ch in " \t":
                i += 1
                continue
            return None, ("NOT_CSV", {"problem": "text_after_closing_quote", "offset": i})
        if at_start and ch == '"':
            quoted, at_start = True, False
            i += 1
            continue
        at_start = False
        field.append(ch)
        i += 1
    if quoted and not after_quote:
        return None, ("NOT_CSV", {"problem": "unterminated_quoted_field"})
    if field or quoted or record:
        if end_record():
            return None, ("TOO_LARGE", {"rows_over": max_rows})
    return records, None


def load_csv(data: bytes | str, target=None, limits: dict | None = None) -> dict:
    """CSV bytes or text -> LoadResult (the same dict as loadCsv in assets/explore_load.js)."""
    lim = {**LIMITS, **(limits or {})}
    if isinstance(data, str):
        text, raw = data, data.encode("utf-8")
    else:
        raw = bytes(data)
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            return _reject("ENCODING", {"problem": "not_utf8"}, hashlib.sha256(raw).hexdigest())
    sha = hashlib.sha256(raw).hexdigest()
    if text.startswith("﻿"):
        text = text[1:]
    if "�" in text or "\x00" in text:
        return _reject("ENCODING", {"problem": "nul_character" if "\x00" in text
                                    else "replacement_character"}, sha)
    if trim(text) == "":
        return _reject("NOT_CSV", {"problem": "empty"}, sha)
    records, err = _read_records(text, lim["max_rows"])
    if err:
        return _reject(err[0], err[1], sha)
    if not records:
        return _reject("NOT_CSV", {"problem": "empty"}, sha)
    header = [trim(h) for h in records[0]]
    ncol = len(header)
    if ncol < 2:
        return _reject("NOT_CSV", {"problem": "fewer_than_two_columns", "columns": ncol}, sha)
    if ncol > lim["max_columns"]:
        return _reject("TOO_LARGE", {"columns": ncol, "max_columns": lim["max_columns"]}, sha)
    if "" in header:
        return _reject("NO_HEADER", {"problem": "empty_column_name", "column": header.index("")}, sha)
    if all(is_number_literal(h) for h in header):
        return _reject("NO_HEADER", {"problem": "numeric_header"}, sha)
    seen: dict[str, int] = {}
    for c, name in enumerate(header):
        if name in seen:
            return _reject("DUPLICATE_COLUMN", {"name": name, "columns": [seen[name], c]}, sha)
        seen[name] = c
    data_rows = records[1:]
    for r, row in enumerate(data_rows):
        if len(row) != ncol:
            return _reject("RAGGED_ROWS", {"record": r + 1, "expected": ncol, "found": len(row)}, sha)
    if len(data_rows) > lim["max_rows"]:
        return _reject("TOO_LARGE", {"rows": len(data_rows), "max_rows": lim["max_rows"]}, sha)
    cells = [[trim(v) for v in row] for row in data_rows]
    types = []
    for c in range(ncol):
        values = [row[c] for row in cells if row[c] != ""]
        types.append("numeric" if values and all(is_number_literal(v) for v in values)
                     else "categorical")
    kept, dropped = [], 0
    for row in cells:
        if "" in row:
            dropped += 1
            continue
        kept.append([float(v) if types[j] == "numeric" else v for j, v in enumerate(row)])
    if len(kept) < lim["min_rows"]:
        return _reject("TOO_FEW_ROWS", {"rows": len(kept), "min_rows": lim["min_rows"],
                                        "dropped_missing": dropped}, sha)
    if target is None:
        t = ncol - 1
    elif isinstance(target, int):
        t = target
    else:
        t = header.index(str(target))
    if types[t] != "numeric":
        return _reject("TARGET_NOT_NUMERIC", {"target": header[t], "index": t}, sha)
    return {
        "ok": True,
        "sha256": sha,
        "columns": [{"name": name, "index": j, "type": types[j]} for j, name in enumerate(header)],
        "target": {"name": header[t], "index": t},
        "rows": kept,
        "n_rows_read": len(data_rows),
        "n_rows_dropped_missing": dropped,
        "n_rows": len(kept),
        "limits": {"maxRows": lim["max_rows"], "maxColumns": lim["max_columns"],
                   "minRows": lim["min_rows"]},
    }


# ---- PRNG, split, folds ------------------------------------------------------------------------

def _imul(a: int, b: int) -> int:
    return (a * b) & _M32


def mulberry32(seed: int):
    """The mulberry32 generator on unsigned 32-bit integers (same output as the JS version)."""
    state = seed & _M32

    def nxt() -> int:
        nonlocal state
        state = (state + 0x6D2B79F5) & _M32
        t = state
        t = _imul(t ^ (t >> 15), t | 1)
        t ^= (t + _imul(t ^ (t >> 7), t | 61)) & _M32
        return (t ^ (t >> 14)) & _M32

    return nxt


def shuffled_indices(n: int, nxt) -> list[int]:
    a = list(range(n))
    for i in range(n - 1, 0, -1):
        j = math.floor((nxt() / 4294967296) * (i + 1))
        a[i], a[j] = a[j], a[i]
    return a


def make_split(n: int, seed: int = SEED) -> dict:
    perm = shuffled_indices(n, mulberry32(seed))
    n_test = min(max(math.floor(TEST_FRACTION * n + 0.5), 1), n - 1)
    test = sorted(perm[:n_test])
    train = sorted(perm[n_test:])
    order = shuffled_indices(len(train), mulberry32((seed + 1) & _M32))
    folds = [0] * len(train)
    for q, pos in enumerate(order):
        folds[pos] = q % N_FOLDS
    return {"train": train, "test": test, "folds": folds}


# ---- the three-layer preprocessing boundary ----------------------------------------------------

def train_decisions(load: dict, train_rows) -> dict:
    columns, groups = [], []
    t = load["target"]["index"]
    for col in load["columns"]:
        if col["index"] == t:
            columns.append({**col, "role": "target", "status": "TARGET"})
            continue
        distinct = {load["rows"][r][col["index"]] for r in train_rows}
        status = "KEPT"
        if len(distinct) <= 1:
            status = "EXCLUDED_CONSTANT"
        elif col["type"] == "categorical" and len(distinct) > MAX_LEVELS:
            status = "EXCLUDED_TOO_MANY_LEVELS"
        columns.append({**col, "role": "feature", "status": status,
                        "n_distinct_train": len(distinct)})
        if status == "KEPT":
            groups.append({"name": col["name"], "index": col["index"], "type": col["type"]})
    return {"columns": columns, "groups": groups}


def fit_encoding(load: dict, groups, rows) -> dict:
    enc_groups, columns = [], []
    for g in groups:
        if g["type"] == "numeric":
            enc_groups.append({**g})
            columns.append({"group": g["name"], "level": None})
            continue
        levels: list[str] = []
        for r in rows:
            v = load["rows"][r][g["index"]]
            if v not in levels:
                levels.append(v)
        enc_groups.append({**g, "levels": levels, "baseline": levels[0] if levels else None})
        columns.extend({"group": g["name"], "level": lv} for lv in levels[1:])
    return {"groups": enc_groups, "columns": columns}


def encode_rows(load: dict, enc: dict, rows) -> tuple[np.ndarray, int, dict]:
    X, unseen_rows, unseen_by_group = [], 0, {}
    for r in rows:
        src, x, unseen = load["rows"][r], [], False
        for g in enc["groups"]:
            v = src[g["index"]]
            if g["type"] == "numeric":
                x.append(float(v))
                continue
            if v not in g["levels"]:
                unseen = True
                unseen_by_group[g["name"]] = unseen_by_group.get(g["name"], 0) + 1
            x.extend(1.0 if v == lv else 0.0 for lv in g["levels"][1:])
        unseen_rows += unseen
        X.append(x)
    width = len(enc["columns"])
    return np.asarray(X, dtype=float).reshape(len(rows), width), unseen_rows, unseen_by_group


def _target(load: dict, rows) -> np.ndarray:
    t = load["target"]["index"]
    return np.asarray([load["rows"][r][t] for r in rows], dtype=float)


def _fit(X: np.ndarray, y: np.ndarray, names) -> dict:
    """hw2.ols.fit_ols plus the A-1 residual-degrees-of-freedom rule."""
    p = X.shape[1] + 1
    try:
        fit = ols.fit_ols(X, y, names)
    except ols.RankDeficientError as err:
        if err.rank < err.n_columns:
            return {"ok": False, "rule": "rank_deficient", "rank": err.rank, "n_columns": p,
                    "df_resid": len(y) - err.rank}
        return {"ok": False, "rule": "df_resid_lt_3", "rank": err.rank, "n_columns": p,
                "df_resid": len(y) - err.rank}
    if fit.df_resid < MIN_DF_RESID:
        return {"ok": False, "rule": "df_resid_lt_3", "rank": fit.rank, "n_columns": p,
                "df_resid": fit.df_resid}
    return {"ok": True, "fit": fit, "rank": fit.rank, "n_columns": p, "df_resid": fit.df_resid}


def _levels(enc: dict) -> dict:
    return {g["name"]: {"levels": list(g["levels"]), "baseline": g["baseline"]}
            for g in enc["groups"] if g["type"] == "categorical"}


def _metrics(actual, predicted) -> dict:
    return {k: (None if v is None else float(v))
            for k, v in metrics.usd_metrics(actual, predicted).items()}


def _finite(v) -> float | None:
    """R² is undefined (None, as in the JS engine) when the target is constant on the rows."""
    return float(v) if math.isfinite(v) else None


def _names(enc: dict) -> list[str]:
    return [c["group"] if c["level"] is None else f"{c['group']}={c['level']}"
            for c in enc["columns"]]




# ---- one candidate: CV on the folds (each with its own subset) and the canonical fit -----------

def _subset_groups(groups, names) -> list:
    chosen = set(names)
    return [g for g in groups if g["name"] in chosen]


def _fit_record(load: dict, c_enc: dict, train_rows, fit) -> dict:
    inputs = {}
    for g in c_enc["groups"]:
        if g["type"] == "numeric":
            v = np.asarray([load["rows"][r][g["index"]] for r in train_rows], dtype=float)
            inputs[g["name"]] = {"min": float(v.min()), "max": float(v.max()),
                                 "median": float(np.median(v))}
    return {
        "n_train": fit.n, "n_columns": fit.n_columns, "rank": fit.rank,
        "df_resid": fit.df_resid, "s2": float(fit.s2), "r2_train": _finite(fit.r2),
        "adj_r2_train": _finite(fit.adj_r2), "t_crit": float(fit.t_crit), "pi_level": PI_LEVEL,
        "groups": [g["name"] for g in c_enc["groups"]],
        "encoded_columns": c_enc["columns"],
        "coef": [float(v) for v in fit.coef],
        "xtx_inv": [[float(v) for v in row] for row in fit.xtx_inv],
        "levels": _levels(c_enc), "inputs": inputs,
        "_fit": fit, "_encoding": c_enc,
    }


def _missing_reason(scope: str, fold, info: dict) -> dict:
    """The Lasso path of these rows stopped before reaching k groups (A-2)."""
    return {"rule": "lasso_path_degenerate", "scope": scope, "fold": fold,
            "n_groups_entered": info["n_entered"], "cause": info["cause"]}


def evaluate_candidate(load: dict, groups, split: dict, method: str, k: int, fold_subsets,
                       canonical_subset, fold_lasso=None, canonical_lasso=None) -> dict:
    """Candidate (method, k): fold f is fitted on its training rows with ``fold_subsets[f]``
    (``None``: that fold's Lasso path stopped before k groups), the canonical fit on the whole
    training set with ``canonical_subset``. A-1 and A-2 decide the status; every reason is kept."""
    key = models.model_key(method, k)
    folds, reasons = [], []
    for f in range(N_FOLDS):
        train_rows = [r for r, fo in zip(split["train"], split["folds"]) if fo != f]
        valid_rows = [r for r, fo in zip(split["train"], split["folds"]) if fo == f]
        subset = fold_subsets[f]
        if subset is None:
            folds.append({"fold": f, "n_train": len(train_rows), "n_valid": len(valid_rows),
                          "groups": None, "levels": None, "n_columns": None, "rank": None,
                          "df_resid": None, "status": "invalid", "rule": "lasso_path_degenerate",
                          "metrics": None})
            reasons.append(_missing_reason("fold", f, fold_lasso[f]))
            continue
        enc = fit_encoding(load, _subset_groups(groups, subset), train_rows)
        X, _, _ = encode_rows(load, enc, train_rows)
        res = _fit(X, _target(load, train_rows), _names(enc))
        rec = {"fold": f, "n_train": len(train_rows), "n_valid": len(valid_rows),
               "groups": list(subset), "levels": _levels(enc), "n_columns": res["n_columns"],
               "rank": res["rank"], "df_resid": res["df_resid"]}
        if not res["ok"]:
            rec.update(status="invalid", rule=res["rule"], metrics=None)
            reasons.append({"rule": res["rule"], "scope": "fold", "fold": f, "rank": res["rank"],
                            "n_columns": res["n_columns"], "df_resid": res["df_resid"]})
        else:
            Xv, unseen, _ = encode_rows(load, enc, valid_rows)
            pred = ols.design(Xv) @ res["fit"].coef
            rec.update(status="ok", rule=None, coef=[float(v) for v in res["fit"].coef],
                       metrics=_metrics(_target(load, valid_rows), pred), n_valid_unseen=unseen)
        folds.append(rec)
    fit_out = None
    c_res = None
    if canonical_subset is None:
        reasons.append(_missing_reason("training_set", None, canonical_lasso))
    else:
        c_enc = fit_encoding(load, _subset_groups(groups, canonical_subset), split["train"])
        Xc, _, _ = encode_rows(load, c_enc, split["train"])
        c_res = _fit(Xc, _target(load, split["train"]), _names(c_enc))
        if not c_res["ok"]:
            reasons.append({"rule": c_res["rule"], "scope": "training_set", "fold": None,
                            "rank": c_res["rank"], "n_columns": c_res["n_columns"],
                            "df_resid": c_res["df_resid"]})
    status = "INVALID_MODEL" if reasons else "VALID"
    cv = None
    if status == "VALID":
        cv = {"n_folds": N_FOLDS, "std_ddof": CV_STD_DDOF, "mean": {}, "std": {}}
        for m in METRICS:
            vals = [rec["metrics"][m] for rec in folds]
            if any(v is None for v in vals):
                cv["mean"][m] = cv["std"][m] = None
                continue
            arr = np.asarray(vals, dtype=float)
            cv["mean"][m] = float(arr.mean())
            cv["std"][m] = float(arr.std(ddof=CV_STD_DDOF))
        fit_out = _fit_record(load, c_enc, split["train"], c_res["fit"])
    return {"key": key, "method": method, "k": k, "status": status, "reasons": reasons,
            "folds": folds, "cv": cv,
            "canonical_groups": None if canonical_subset is None else list(canonical_subset),
            "fit": fit_out}


def evaluate_allin(load: dict, groups, split: dict) -> dict:
    """The All-in baseline: every feature group in every fold and on the training set."""
    if not groups:
        return {"key": "allin", "method": "allin", "k": 0, "status": "INVALID_MODEL",
                "reasons": [{"rule": "no_feature_groups", "scope": "training_set", "fold": None}],
                "folds": [], "cv": None, "canonical_groups": [], "fit": None}
    names = [g["name"] for g in groups]
    return evaluate_candidate(load, groups, split, models.ALLIN, len(groups), [names] * N_FOLDS,
                              names)


# ---- the selection paths (fold-internal and canonical) ------------------------------------------

def group_gram(X: np.ndarray, y: np.ndarray, column_groups, groups) -> selection.GroupGram:
    """A :class:`hw2.selection.GroupGram` for any encoded table: the same centred, unit-norm
    columns and centred target as the formal constructor, so that ``rss`` and ``importance`` are
    the formal criteria."""
    gram = object.__new__(selection.GroupGram)
    Xc = X - X.mean(axis=0)
    yc = y - y.mean()
    norms = np.linalg.norm(Xc, axis=0)
    Z = Xc / np.where(norms > 0, norms, 1.0)
    gram.n = len(y)
    gram.G = Z.T @ Z
    gram.b = Z.T @ yc
    gram.yy = float(yc @ yc)
    gram.columns = {g: np.array([j for j, cg in enumerate(column_groups) if cg == g], dtype=int)
                    for g in groups}
    return gram


def _pick(scores, rank: dict, prefer_late: bool):
    """:func:`hw2.selection._pick` with the canonical order of these groups (the formal one is
    bound to the 18 King County groups)."""
    best = min(v for v, _ in scores)
    tol = TIE_RTOL * max(abs(best), 1.0)
    tied = [g for v, g in scores if v <= best + tol]
    return max(tied, key=rank.get) if prefer_late else min(tied, key=rank.get)


def _canon(names, subset) -> list:
    chosen = set(subset)
    return [g for g in names if g in chosen]


def forward_path(gram, names) -> list:
    rank = {g: i for i, g in enumerate(names)}
    selected, remaining, subsets = [], list(names), []
    while remaining:
        scores = [(gram.rss(_canon(names, selected + [g])), g) for g in remaining]
        g = _pick(scores, rank, prefer_late=False)
        selected.append(g)
        remaining.remove(g)
        subsets.append(_canon(names, selected))
    return subsets


def backward_path(gram, names) -> list:
    rank = {g: i for i, g in enumerate(names)}
    current = list(names)
    subsets = {len(names): _canon(names, current)}
    while len(current) > 1:
        scores = [(gram.rss([h for h in current if h != g]), g) for g in current]
        g = _pick(scores, rank, prefer_late=True)
        current.remove(g)
        subsets[len(current)] = _canon(names, current)
    return [subsets[k] for k in range(1, len(names) + 1)]


def rfe_path(gram, names) -> list:
    rank = {g: i for i, g in enumerate(names)}
    current = list(names)
    subsets = {len(names): _canon(names, current)}
    while len(current) > 1:
        imp = gram.importance(current)
        g = _pick([(imp[h], h) for h in current], rank, prefer_late=True)
        current.remove(g)
        subsets[len(current)] = _canon(names, current)
    return [subsets[k] for k in range(1, len(names) + 1)]


def lasso_design(X: np.ndarray, dummy) -> np.ndarray:
    """The formal Ridge/Lasso standardization (hw2.preprocess.fit_preprocessor(standardize=True))
    on these rows, then every column centred (hw2.selection.lasso_entry)."""
    dummy = np.asarray(dummy, dtype=bool)
    center = X.mean(axis=0)
    scale = X.std(axis=0)
    center[dummy] = 0.0
    scale[dummy] = 1.0
    scale[scale == 0.0] = 1.0
    Xs = (X - center) / scale
    return Xs - Xs.mean(axis=0)


_DEGENERATE_WARNING = re.compile(r"Regressors in active set degenerate.*?after (\d+) iterations",
                                 re.S)


def _degenerate(G: np.ndarray, active, j: int) -> bool:
    """A-2: the column entering the active set is (numerically) in the span of the active ones."""
    c = float(G[j, j])
    v = 0.0
    if active:
        L = np.linalg.cholesky(G[np.ix_(active, active)])
        w = linalg.solve_triangular(L, G[active, j], lower=True)
        v = float(w @ w)
    diag = max(math.sqrt(abs(c - v)), EPS)
    return diag < LARS_PIVOT_ATOL or diag <= LARS_DEGENERATE_RTOL * math.sqrt(c)


def lars_segment(Xs: np.ndarray, yc: np.ndarray) -> dict:
    """The exact Lasso path (sklearn's lars_path, method="lasso"), cut at the first active-set
    degeneracy (A-2). sklearn's own log (verbose=2) names every column it adds or drops, so the
    active set before each addition is known exactly; sklearn's own pivot warning names the
    iteration of a degeneracy it caught itself (it then skips the column, which A-2 does not)."""
    out = io.StringIO()
    with warnings.catch_warnings(record=True) as caught, contextlib.redirect_stdout(out):
        warnings.simplefilter("always", ConvergenceWarning)
        alphas, _, coefs = lars_path(Xs, yc, method="lasso", max_iter=LARS_MAX_ITER, verbose=2)
    end, cause, attempted = len(alphas) - 1, None, None
    for w in caught:
        m = _DEGENERATE_WARNING.search(str(w.message))
        if m and int(m.group(1)) < end:
            end, cause, attempted = int(m.group(1)), "active_set_degenerate", None
    G = Xs.T @ Xs
    active: list[int] = []
    for line in out.getvalue().splitlines()[1:]:          # the first line is sklearn's header
        parts = line.split("\t\t")
        step = int(parts[0])
        if parts[1] != "":                                 # an addition in iteration `step`
            if step >= end:                                # beyond the segment
                break
            j = int(parts[1])
            if _degenerate(G, active, j):
                end, cause, attempted = step, "active_set_degenerate", j
                break
            active.append(j)
        else:                                              # a drop (printed after the increment)
            for v in re.findall(r"(?:np\.int\d+\()?(\d+)", parts[2]):
                active.remove(int(v))
    return {"alphas": alphas[:end + 1], "coefs": coefs[:, :end + 1], "end": end, "cause": cause,
            "attempted": attempted}


def lasso_order(X: np.ndarray, y: np.ndarray, column_groups, dummy, names) -> dict:
    """Groups by Lasso entry on these rows: entry alpha descending, ties (TIE_RTOL) in CSV order.
    A group enters at the knot alpha before its first non-zero coefficient within the path segment
    before any degeneracy (A-2)."""
    seg = lars_segment(lasso_design(X, dummy), y - y.mean())
    nonzero = seg["coefs"] != 0.0
    first_col = np.where(nonzero.any(axis=1), nonzero.argmax(axis=1), -1)
    alpha = {}
    for g in names:
        firsts = [int(first_col[j]) for j, cg in enumerate(column_groups)
                  if cg == g and first_col[j] >= 1]
        if firsts:
            alpha[g] = float(seg["alphas"][min(firsts) - 1])
    rank = {g: i for i, g in enumerate(names)}
    order = sorted(alpha, key=lambda g: (-alpha[g], rank[g]))
    clustered, i = [], 0
    while i < len(order):                                  # tie clusters by TIE_RTOL, CSV order
        j = i + 1
        while j < len(order) and (alpha[order[j - 1]] - alpha[order[j]]
                                  <= TIE_RTOL * max(abs(alpha[order[j - 1]]), 1.0)):
            j += 1
        clustered.extend(sorted(order[i:j], key=rank.get))
        i = j
    n_entered = len(clustered)
    not_entered = [g for g in names if g not in alpha]
    cause = seg["cause"] if n_entered < len(names) else None
    if n_entered < len(names) and cause is None:
        cause = "path_ended"
    return {
        "entries": [{"group": g, "entry_alpha": alpha[g]} for g in clustered],
        "not_entered": not_entered,
        "n_entered": n_entered,
        "degenerate": n_entered < len(names),
        "first_invalid_k": n_entered + 1 if n_entered < len(names) else None,
        "cause": cause,
        "subsets": [_canon(names, clustered[:k]) if k <= n_entered else None
                    for k in range(1, len(names) + 1)],
    }


def paths_on_rows(load: dict, groups, rows) -> dict:
    """Every path method on the given rows only: subsets[k - 1] for k = 1…p."""
    names = [g["name"] for g in groups]
    enc = fit_encoding(load, groups, rows)
    X, _, _ = encode_rows(load, enc, rows)
    y = _target(load, rows)
    column_groups = [c["group"] for c in enc["columns"]]
    dummy = [c["level"] is not None for c in enc["columns"]]
    return canonical_paths(X, y, column_groups, dummy, names)


def canonical_paths(X: np.ndarray, y: np.ndarray, column_groups, dummy, names) -> dict:
    """The four paths on one encoded table (raw encoded columns, target as modelled)."""
    gram = group_gram(np.asarray(X, dtype=float), np.asarray(y, dtype=float), column_groups, names)
    lasso = lasso_order(np.asarray(X, dtype=float), np.asarray(y, dtype=float), column_groups,
                        dummy, names)
    return {"forward_sfs": forward_path(gram, names), "backward_sfs": backward_path(gram, names),
            "rfe": rfe_path(gram, names), "lasso_path": lasso["subsets"], "_lasso": lasso}


def _lasso_public(info: dict) -> dict:
    return {k: v for k, v in info.items() if k != "subsets"}


# ---- winners (hw2.models.determine_winners rules) and the frozen test ---------------------------

def determine_winners(candidates) -> dict:
    """Method CV winner: lowest CV RMSE among the method's VALID candidates, ties → smaller k
    (All-in is its own winner). Overall: lowest CV RMSE among the method winners, ties → the order
    of METHOD_ORDER. Winners with the same canonical subset are one model, scored once under the
    first key in the order All-in, method winners in method order, overall winner."""
    method_winners = {}
    for m in METHOD_ORDER:
        valid = [c for c in candidates if c["method"] == m and c["status"] == "VALID"]
        if not valid:
            method_winners[m] = None
            continue
        w = min(valid, key=lambda c: (c["cv"]["mean"]["rmse"], c["k"]))
        method_winners[m] = {"key": w["key"], "k": w["k"]}
    by_key = {c["key"]: c for c in candidates}
    pool = [(m, w) for m, w in method_winners.items() if w is not None]
    if not pool:
        return None
    m, w = min(pool, key=lambda t: (by_key[t[1]["key"]]["cv"]["mean"]["rmse"],
                                    METHOD_ORDER.index(t[0])))
    overall = {"method": m, "key": w["key"], "k": w["k"]}
    order = [w["key"] for _, w in pool] + [overall["key"]]
    representative, test_keys = {}, []
    for key in order:
        subset = tuple(by_key[key]["canonical_groups"])
        rep = representative.setdefault(subset, key)
        if rep not in test_keys:
            test_keys.append(rep)
    test_key_of = {key: representative[tuple(by_key[key]["canonical_groups"])] for key in order}
    return {"method_winners": method_winners, "overall": overall, "test_keys": test_keys,
            "test_key_of": test_key_of}


def evaluate_test(load: dict, candidate: dict, test_rows) -> dict:
    fit, enc = candidate["fit"]["_fit"], candidate["fit"]["_encoding"]
    X, unseen, unseen_by_group = encode_rows(load, enc, test_rows)
    actual = _target(load, test_rows)
    yhat, lower, upper = ols.log_interval(fit, X)   # the PI formula on the original target scale
    cov = metrics.coverage_stats(actual, lower, upper)
    return {"key": candidate["key"], "rows": list(test_rows), "n_test": len(test_rows),
            "actual": [float(v) for v in actual], "predicted": [float(v) for v in yhat],
            "lower": [float(v) for v in lower], "upper": [float(v) for v in upper],
            "covered": [bool(v) for v in cov["covered"]], "n_covered": cov["n_covered"],
            "coverage": cov["coverage"], "metrics": _metrics(actual, yhat),
            "n_unseen_rows": unseen, "n_unseen_by_group": unseen_by_group}


# ---- A-3: linear dependencies of the All-in design on the training set --------------------------

def dependency_groups(load: dict, groups, rows) -> dict:
    """Linear relations among the columns of the All-in design (intercept + encoded columns, the
    canonical encoding of the whole training set). The equilibrated columns are taken in canonical
    order; a column within DEPENDENCY_TOL (= max(n, p)·eps, the rank tolerance of hw2.ols) of the
    span of the earlier independent ones closes one relation. A relation lists every column with a
    non-zero coefficient (normalised: largest |coefficient| 1, first non-zero positive) and the
    feature groups of those columns; it names no single column as the cause."""
    enc = fit_encoding(load, groups, rows)
    X, _, _ = encode_rows(load, enc, rows)
    D = ols.design(X)
    n, p = D.shape
    cols = [{"intercept": True, "group": None, "level": None}] + [
        {"intercept": False, "group": c["group"], "level": c["level"]} for c in enc["columns"]]
    norms = np.linalg.norm(D, axis=0)
    safe = np.where(norms > 0, norms, 1.0)
    Z = D / safe
    tol = max(n, p) * EPS
    Q, R, basis, relations = [], [], [], []
    for j in range(p):
        v = Z[:, j].copy()
        rj = np.zeros(len(Q))
        for _ in range(2):                                 # Gram–Schmidt, twice
            for i, q in enumerate(Q):
                d = float(q @ v)
                v -= d * q
                rj[i] += d
        r = float(np.linalg.norm(v))
        if r > tol:
            Q.append(v / r)
            R.append(np.append(rj, r))
            basis.append(j)
            continue
        m = len(basis)
        Rb = np.zeros((m, m))
        for col, rc in enumerate(R):
            Rb[:len(rc), col] = rc
        a = linalg.solve_triangular(Rb, rj) if m else np.zeros(0)
        coef = np.zeros(p)
        for l, b in enumerate(basis):
            coef[b] = -a[l] * safe[j] / safe[b]
        coef[j] = 1.0
        coef /= np.abs(coef).max()
        coef[np.abs(coef) <= RELATION_ZERO] = 0.0
        nz = np.flatnonzero(coef)
        if coef[nz[0]] < 0:
            coef = -coef
        members = [{**cols[i], "coef": float(coef[i])} for i in nz]
        feature_groups = [g["name"] for g in groups
                          if any(c["group"] == g["name"] for c in members)]
        relations.append({"columns": members, "feature_groups": feature_groups,
                          "includes_intercept": bool(cols[nz[0]]["intercept"])})
    return {"n_columns": p, "rank": len(basis), "relations": relations}


# ---- the run ------------------------------------------------------------------------------------

def run(load: dict, seed: int = SEED, split: dict | None = None, problem=None,
        source=None) -> dict:
    """LoadResult -> ExploratoryResult (deterministic part; no timing)."""
    if not load.get("ok"):
        raise ValueError("run needs an accepted LoadResult")
    n = len(load["rows"])
    sp = make_split(n, seed) if split is None else {k: list(split[k]) for k in ("train", "test", "folds")}
    decided = train_decisions(load, sp["train"])
    groups = decided["groups"]
    result = {
        "meta": {"reference_version": REFERENCE_VERSION, "problem": problem, "source": source,
                 "sha256": load["sha256"], "target": load["target"]["name"],
                 "n_rows_read": load["n_rows_read"], "n_rows": n,
                 "n_rows_dropped_missing": load["n_rows_dropped_missing"], "seed": seed,
                 "split_injected": split is not None, "pi_level": PI_LEVEL,
                 "max_levels": MAX_LEVELS, "min_df_resid": MIN_DF_RESID,
                 "cv_std_ddof": CV_STD_DDOF},
        "columns": decided["columns"],
        "groups": groups,
        "split": {**sp, "n_folds": N_FOLDS},
        "dependencies": dependency_groups(load, groups, sp["train"]),
        "lasso_path": None,
    }
    candidates = [evaluate_allin(load, groups, sp)]
    if groups:
        fold_rows = [[r for r, fo in zip(sp["train"], sp["folds"]) if fo != f]
                     for f in range(N_FOLDS)]
        fold_paths = [paths_on_rows(load, groups, rows) for rows in fold_rows]
        canon = paths_on_rows(load, groups, sp["train"])
        result["lasso_path"] = {"canonical": _lasso_public(canon["_lasso"]),
                                "folds": [_lasso_public(fp["_lasso"]) for fp in fold_paths]}
        for method in PATH_METHODS:
            for k in range(1, len(groups) + 1):
                candidates.append(evaluate_candidate(
                    load, groups, sp, method, k,
                    [fp[method][k - 1] for fp in fold_paths], canon[method][k - 1],
                    [fp["_lasso"] for fp in fold_paths], canon["_lasso"]))
    if not any(c["status"] == "VALID" for c in candidates):
        result["run"] = {"status": "REJECTED", "reason": "ALL_CANDIDATES_INVALID",
                         "invalid_candidates": [{"key": c["key"], "status": c["status"],
                                                 "reasons": c["reasons"]} for c in candidates]}
        return result
    # winners fixed here; the test rows are read only after this point
    winners = determine_winners(candidates)
    by_key = {c["key"]: c for c in candidates}
    test = {key: evaluate_test(load, by_key[key], sp["test"]) for key in winners["test_keys"]}
    result["run"] = {"status": "COMPLETED", "reason": None}
    result["candidates"] = [_public(c) for c in candidates]
    result["winners"] = winners
    result["test"] = test
    return result


def _public(candidate: dict) -> dict:
    out = dict(candidate)
    if out.get("fit"):
        out["fit"] = {k: v for k, v in out["fit"].items() if not k.startswith("_")}
    return out
