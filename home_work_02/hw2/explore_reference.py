"""Generic Python reference for the V2 Exploratory run (Spec V2 「通用 Python 參照」; #74 V2-T1: All-in).

**Test-only.** This module produces reference results for the Node tests of the browser engine
(``assets/explore_engine.js``, ``assets/explore_load.js``). Nothing on the formal analysis path
imports it: not the notebook, not any other ``hw2`` module, not the report or the packaging
(``tests/test_explore_static.py`` checks this). It never reads ``model_data`` and depends on no JS
result: it re-implements the load contract, the split, the three-layer preprocessing boundary and
the All-in candidate from the Spec, and reuses the formal package's group-generic mathematics
instead of writing them again:

- :func:`hw2.ols.fit_ols` — OLS on ``[1, X]`` with the actual rank (column-pivoted QR of the
  column-equilibrated design), ``(XᵀX)⁻¹``, ``s²``, ``df_resid``, ``R²``, Adjusted ``R²`` with the
  actual rank, ``t(0.975, df_resid)``; raises :class:`hw2.ols.RankDeficientError`;
- :func:`hw2.ols.log_interval` — ``ŷ ± t·√(s²(1 + x₀ᵀ(XᵀX)⁻¹x₀))``; despite its name it evaluates
  the formula on whatever scale ``y`` has; the Exploratory run models the original target (no log,
  no exp), so its output is used as is;
- :func:`hw2.metrics.usd_metrics` and :func:`hw2.metrics.coverage_stats` — MAE, MSE, RMSE, R² and
  the closed-interval coverage, unit-free despite the name.

No King County specific function (CSV schema, derived features, ln(price), grouped split) is used.

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
   the first one is the baseline (no column); unseen levels are the baseline and counted.
5. **A-1**: full rank and ``df_resid ≥ 3`` on every fold's training rows and on the whole training
   set, else ``INVALID_MODEL`` with the rule and the fold.
6. **CV**: arithmetic mean of the five fold metrics, sample standard deviation (ddof
   :data:`CV_STD_DDOF`, equal to :data:`hw2.models.CV_STD_DDOF`).
7. **Test**: read only after the winners are fixed, only for the winners' canonical fits.
"""
from __future__ import annotations

import hashlib
import math
import re

import numpy as np

from . import metrics, ols

REFERENCE_VERSION = "explore-reference 1 (V2-T1: All-in)"
SEED = 42
TEST_FRACTION = 0.2
N_FOLDS = 5
MAX_LEVELS = 20
MIN_DF_RESID = 3
PI_LEVEL = 0.95
CV_STD_DDOF = 1
LIMITS = {"max_rows": 50000, "max_columns": 60, "min_rows": 20}
METRICS = ("mae", "mse", "rmse", "r2")

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


def evaluate_allin(load: dict, groups, split: dict) -> dict:
    names = [g["name"] for g in groups]
    if not groups:
        return {"key": "allin", "method": "allin", "k": 0, "status": "INVALID_MODEL",
                "reasons": [{"rule": "no_feature_groups", "scope": "training_set", "fold": None}],
                "folds": [], "cv": None, "canonical_groups": [], "fit": None}
    folds, reasons = [], []
    for f in range(N_FOLDS):
        train_rows = [r for r, fo in zip(split["train"], split["folds"]) if fo != f]
        valid_rows = [r for r, fo in zip(split["train"], split["folds"]) if fo == f]
        enc = fit_encoding(load, groups, train_rows)
        X, _, _ = encode_rows(load, enc, train_rows)
        res = _fit(X, _target(load, train_rows), _names(enc))
        rec = {"fold": f, "n_train": len(train_rows), "n_valid": len(valid_rows),
               "groups": list(names), "levels": _levels(enc), "n_columns": res["n_columns"],
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
    c_enc = fit_encoding(load, groups, split["train"])
    Xc, _, _ = encode_rows(load, c_enc, split["train"])
    c_res = _fit(Xc, _target(load, split["train"]), _names(c_enc))
    if not c_res["ok"]:
        reasons.append({"rule": c_res["rule"], "scope": "training_set", "fold": None,
                        "rank": c_res["rank"], "n_columns": c_res["n_columns"],
                        "df_resid": c_res["df_resid"]})
    status = "INVALID_MODEL" if reasons else "VALID"
    cv, fit_out = None, None
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
        fit = c_res["fit"]
        inputs = {}
        for g in c_enc["groups"]:
            if g["type"] == "numeric":
                v = np.asarray([load["rows"][r][g["index"]] for r in split["train"]], dtype=float)
                inputs[g["name"]] = {"min": float(v.min()), "max": float(v.max()),
                                     "median": float(np.median(v))}
        fit_out = {
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
    return {"key": "allin", "method": "allin", "k": len(groups), "status": status,
            "reasons": reasons, "folds": folds, "cv": cv, "canonical_groups": list(names),
            "fit": fit_out}


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


def run(load: dict, seed: int = SEED, split: dict | None = None, problem=None,
        source=None) -> dict:
    """LoadResult -> ExploratoryResult (deterministic part; no timing)."""
    if not load.get("ok"):
        raise ValueError("run needs an accepted LoadResult")
    n = len(load["rows"])
    sp = make_split(n, seed) if split is None else {k: list(split[k]) for k in ("train", "test", "folds")}
    decided = train_decisions(load, sp["train"])
    result = {
        "meta": {"reference_version": REFERENCE_VERSION, "problem": problem, "source": source,
                 "sha256": load["sha256"], "target": load["target"]["name"],
                 "n_rows_read": load["n_rows_read"], "n_rows": n,
                 "n_rows_dropped_missing": load["n_rows_dropped_missing"], "seed": seed,
                 "split_injected": split is not None, "pi_level": PI_LEVEL,
                 "max_levels": MAX_LEVELS, "min_df_resid": MIN_DF_RESID,
                 "cv_std_ddof": CV_STD_DDOF},
        "columns": decided["columns"],
        "groups": decided["groups"],
        "split": {**sp, "n_folds": N_FOLDS},
    }
    allin = evaluate_allin(load, decided["groups"], sp)
    candidates = [allin]
    if not any(c["status"] == "VALID" for c in candidates):
        result["run"] = {"status": "REJECTED", "reason": "ALL_CANDIDATES_INVALID",
                         "invalid_candidates": [{"key": c["key"], "status": c["status"],
                                                 "reasons": c["reasons"]} for c in candidates]}
        return result
    # winners fixed here; the test rows are read only after this point
    winners = {"method_winners": {}, "overall": {"method": "allin", "key": "allin",
                                                 "k": allin["k"]}, "test_keys": ["allin"]}
    test = {key: evaluate_test(load, next(c for c in candidates if c["key"] == key), sp["test"])
            for key in winners["test_keys"]}
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
