"""Schemas of ``model_data`` sections and their validation.

:func:`validate_model_data` checks the contract invariants of Spec rev 5 that hold at every stage:
no test field under ``methods`` or ``baselines``; ``baselines.allin`` is the single OLS on all 18
groups; every valid entry has ``cv`` (USD) and ``fit`` (log scale, full rank, (XᵀX)⁻¹ of the right
size); ``winners`` names valid entries only and never a metric-only model; ``test`` has
``ols_subset`` keys equal to the authorized set and ``metric_only`` entries for exactly Ridge and Lasso, with
per-row fields, ``covered``, coverage and mean width consistent with ``test_inputs``.

``test_inputs`` (Spec rev 5 SR-02, SR-08): one row per test sale with the row identifiers
(CSV row position, house ``id``, sale ``date``), the raw values of all 18 modeled source features
and ``actual_price``; plus the number of test houses and repeat sales. Rows are stored as arrays in
:data:`TEST_INPUT_FIELDS` order.

Test-data isolation (DA TR-01): the official rows are written only by the test-evaluation export
(#63, behind the G-3 gate). Until then the tracked ``model_data`` carries
:func:`empty_test_inputs` (the schema with no rows) and no ``test`` section.
"""
import re

import numpy as np
import pandas as pd

from .preprocess import FEATURE_GROUPS, parse_sale_date

TEST_INPUTS_SCHEMA_VERSION = 1
# Row identifiers, then the 18 modeled source features in canonical order (``date`` is both an
# identifier and a source feature, so it appears once), then the target in USD.
TEST_INPUT_FIELDS = ("row", "id", "date",
                     *[g for g in FEATURE_GROUPS if g != "date"],
                     "actual_price")
TEXT_FIELDS = ("id", "date", "zipcode")
_ID = re.compile(r"^\d{1,12}$")
_ZIP = re.compile(r"^\d{5}$")


class ContractError(ValueError):
    """A model_data section does not match its schema."""


def empty_test_inputs() -> dict:
    """The ``test_inputs`` schema with no rows (the tracked state before #63)."""
    return {
        "schema_version": TEST_INPUTS_SCHEMA_VERSION,
        "fields": list(TEST_INPUT_FIELDS),
        "written": False,
        "rows": [],
        "n_rows": 0,
        "n_houses": None,
        "n_repeat_sales": None,
        "n_unseen_zipcode": None,
        "note": ("Rows are written only by the one-time test-evaluation export behind the test "
                 "gate, in the same run as the test results (DA TR-01)."),
    }


def build_test_inputs(rows: pd.DataFrame, training_zipcodes) -> dict:
    """``test_inputs`` with rows, from a frame holding 'row', the raw CSV columns and 'price'.

    Callers pass only rows they are entitled to: the official test rows behind the test gate
    (#63) or synthetic fixture rows in tests. With `training_zipcodes` (the zipcode categories of
    the training set, which every whole-training fit uses; required), ``n_unseen_zipcode`` counts the rows
    whose zipcode is not among them and is therefore encoded as the baseline category (SR-07).
    """
    missing = [c for c in ("row", "id", "price", *FEATURE_GROUPS) if c not in rows.columns]
    if missing:
        raise ContractError(f"rows lack columns {missing}")
    ordered = rows.sort_values("row", kind="stable")
    out_rows = []
    for record in ordered.itertuples(index=False):
        values = record._asdict()
        out = []
        for field in TEST_INPUT_FIELDS:
            source = "price" if field == "actual_price" else field
            value = values[source]
            if field in TEXT_FIELDS:
                out.append(str(value))
            elif field == "row":
                out.append(int(value))
            else:
                out.append(_json_number(value))
        out_rows.append(out)
    n_houses = int(ordered["id"].astype(str).nunique())
    obj = empty_test_inputs()
    obj.update(written=True, rows=out_rows, n_rows=len(out_rows), n_houses=n_houses,
               n_repeat_sales=len(out_rows) - n_houses)
    known = {str(z) for z in training_zipcodes}
    obj["n_unseen_zipcode"] = int(sum(1 for z in ordered["zipcode"].astype(str) if z not in known))
    obj["unseen_zipcode_rule"] = ("test rows whose zipcode is not among the zipcode categories of "
                                  "the training set; every whole-training fit encodes them as the "
                                  "baseline category")
    obj.pop("note")
    return obj


def _json_number(value):
    value = float(value)
    if not np.isfinite(value):
        raise ContractError(f"non-finite value {value}")
    return int(value) if value.is_integer() else value


def validate_test_inputs(obj: dict, n_test: int | None = None) -> None:
    """Raise ContractError unless `obj` matches the ``test_inputs`` schema.

    With rows, every row has one value per field with the field's type, CSV row positions are
    unique, ``actual_price > 0``, ``n_rows`` equals the row count (and ``n_test`` when given),
    ``n_houses`` equals the number of distinct ids and ``n_repeat_sales = n_rows - n_houses``.
    """
    if not isinstance(obj, dict):
        raise ContractError("test_inputs must be an object")
    if obj.get("schema_version") != TEST_INPUTS_SCHEMA_VERSION:
        raise ContractError(f"test_inputs.schema_version must be {TEST_INPUTS_SCHEMA_VERSION}")
    if obj.get("fields") != list(TEST_INPUT_FIELDS):
        raise ContractError(f"test_inputs.fields must be {list(TEST_INPUT_FIELDS)}")
    rows = obj.get("rows")
    if not isinstance(rows, list):
        raise ContractError("test_inputs.rows must be a list")
    if obj.get("n_rows") != len(rows):
        raise ContractError(f"test_inputs.n_rows {obj.get('n_rows')} != {len(rows)} rows")
    if not obj.get("written"):
        if rows or obj.get("n_houses") is not None or obj.get("n_repeat_sales") is not None                 or obj.get("n_unseen_zipcode") is not None:
            raise ContractError("unwritten test_inputs must have no rows and null counts")
        return
    unseen = obj.get("n_unseen_zipcode")
    if not isinstance(unseen, int) or isinstance(unseen, bool) or not 0 <= unseen <= len(rows):
        raise ContractError("test_inputs.n_unseen_zipcode must count the rows encoded as the "
                            "baseline zipcode (SR-07)")
    if n_test is not None and len(rows) != n_test:
        raise ContractError(f"test_inputs has {len(rows)} rows, n_test is {n_test}")
    width = len(TEST_INPUT_FIELDS)
    positions, ids = set(), set()
    for i, row in enumerate(rows):
        if not isinstance(row, list) or len(row) != width:
            raise ContractError(f"test_inputs.rows[{i}] must have {width} values")
        for field, value in zip(TEST_INPUT_FIELDS, row):
            _check_value(i, field, value)
        position = row[0]
        if position in positions:
            raise ContractError(f"test_inputs.rows[{i}]: duplicate row position {position}")
        positions.add(position)
        ids.add(row[1])
    if obj.get("n_houses") != len(ids):
        raise ContractError(f"test_inputs.n_houses {obj.get('n_houses')} != {len(ids)} ids")
    if obj.get("n_repeat_sales") != len(rows) - len(ids):
        raise ContractError("test_inputs.n_repeat_sales must equal n_rows - n_houses")


def _check_value(i: int, field: str, value) -> None:
    where = f"test_inputs.rows[{i}].{field}"
    if field == "row":
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ContractError(f"{where} must be a non-negative integer")
    elif field == "id":
        if not isinstance(value, str) or not _ID.match(value):
            raise ContractError(f"{where} must be the id text")
    elif field == "date":
        if not isinstance(value, str):
            raise ContractError(f"{where} must be the CSV date text")
        try:
            parse_sale_date(value)
        except ValueError as exc:
            raise ContractError(f"{where}: {exc}") from exc
    elif field == "zipcode":
        if not isinstance(value, str) or not _ZIP.match(value):
            raise ContractError(f"{where} must be a 5-digit zipcode text")
    else:
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not np.isfinite(value):
            raise ContractError(f"{where} must be a finite number")
        if field == "actual_price" and value <= 0:
            raise ContractError(f"{where} must be > 0")


# --- model entries, winners and test (Spec rev 5 「`model_data` 契約」; SR-03, SR-05) ----------

INTERCEPT = "(intercept)"
METRIC_ONLY_KEYS = ("ridge", "lasso")
# Keys that belong to test results; none may appear anywhere under `methods` or `baselines`.
TEST_FIELD_NAMES = {"test", "test_inputs", "predicted", "lower", "upper", "covered", "coverage",
                    "n_covered", "mean_width", "coverage_uncertainty", "actual_price", "n_test"}
ENTRY_KEYS = {"model_key", "method", "k", "canonical_groups", "fold_groups", "folds_agree",
              "status", "cv", "fit", "is_method_winner"}
FIT_KEYS = {"scale", "target", "n_train", "n_columns", "rank", "df_resid", "r2_log", "adj_r2_log",
            "s2", "pi_level", "t_crit", "groups", "uses_source_features", "encoded_columns",
            "coef_names", "coef", "xtx_inv", "zipcode_categories", "zipcode_baseline"}
CV_METRIC_KEYS = ("mae", "mse", "rmse", "r2")
OLS_TEST_KEYS = {"kind", "model_key", "scale", "n_test", "mae", "mse", "rmse", "r2", "coverage",
                 "n_covered", "mean_width", "coverage_uncertainty", "pi_level",
                 "n_unseen_zipcode", "predicted", "lower", "upper", "covered"}
METRIC_ONLY_TEST_KEYS = {"kind", "model_key", "scale", "alpha", "n_test", "mae", "mse", "rmse",
                         "r2"}


def test_field_paths(obj, path: str = "") -> list:
    """Paths of every key in `obj` (recursively) that names a test field."""
    found = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            here = f"{path}.{key}" if path else str(key)
            if key in TEST_FIELD_NAMES or str(key).startswith("test"):
                found.append(here)
            found.extend(test_field_paths(value, here))
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            found.extend(test_field_paths(value, f"{path}[{i}]"))
    return found


def model_entries(md: dict) -> dict:
    """{model_key: entry} over ``baselines.allin`` and every ``methods`` item."""
    out = {}
    allin = (md.get("baselines") or {}).get("allin")
    if allin is not None:
        out[allin["model_key"]] = allin
    for items in (md.get("methods") or {}).values():
        for entry in items:
            out[entry["model_key"]] = entry
    return out


def validate_entry(entry: dict, where: str, n_folds: int | None = None) -> None:
    missing = ENTRY_KEYS - set(entry)
    if missing:
        raise ContractError(f"{where} lacks {sorted(missing)}")
    status = entry["status"]
    if status.get("state") not in ("valid", "invalid"):
        raise ContractError(f"{where}.status.state must be valid or invalid")
    if status["state"] == "invalid":
        if not status.get("reason"):
            raise ContractError(f"{where} is invalid without a reason")
        if entry["is_method_winner"]:
            raise ContractError(f"{where} is invalid and cannot be a CV winner")
    if len(entry["canonical_groups"]) != entry["k"]:
        raise ContractError(f"{where}: canonical groups do not number k")
    if any(len(g) != entry["k"] for g in entry["fold_groups"]):
        raise ContractError(f"{where}: a fold subset does not have k groups")
    for groups in [entry["canonical_groups"], *entry["fold_groups"]]:
        if list(groups) != [g for g in FEATURE_GROUPS if g in set(groups)] \
                or len(set(groups)) != len(groups):
            raise ContractError(f"{where}: subsets must be feature groups in canonical order")
    cv = entry["cv"]
    if cv.get("scale") != "USD":
        raise ContractError(f"{where}.cv must be on the USD scale")
    if len(cv["folds"]) != cv["n_folds"] or len(entry["fold_groups"]) != cv["n_folds"]:
        raise ContractError(f"{where}.cv: fold records and fold subsets differ from n_folds")
    if n_folds is not None and cv["n_folds"] != n_folds:
        # every method, k and model uses the same folds (#61 R1 F-2)
        raise ContractError(f"{where}.cv.n_folds {cv['n_folds']} != meta.cv.n_folds {n_folds}")
    for record, groups in zip(cv["folds"], entry["fold_groups"]):
        if list(record.get("groups", groups)) != list(groups):
            raise ContractError(f"{where}: fold {record.get('fold')} record groups differ from "
                                "fold_groups")
    agree = sum(1 for g in entry["fold_groups"] if list(g) == list(entry["canonical_groups"]))
    if entry["folds_agree"] != agree:
        raise ContractError(f"{where}.folds_agree {entry['folds_agree']} != {agree}")
    if status["state"] == "valid":
        if cv["mean"] is None or entry["fit"] is None:
            raise ContractError(f"{where}: a valid entry needs cv.mean and fit")
        for m in CV_METRIC_KEYS:
            values = [f[m] for f in cv["folds"]]
            if not np.isclose(np.mean(values), cv["mean"][m], rtol=1e-12, atol=1e-9):
                raise ContractError(f"{where}.cv.mean.{m} is not the mean of the folds")
        validate_fit(entry["fit"], f"{where}.fit", entry["canonical_groups"])
    elif status.get("reason") == "canonical_rank_deficient" and entry["fit"] is not None:
        raise ContractError(f"{where}: canonical_rank_deficient entries have no fit")
    paths = test_field_paths(entry)
    if paths:
        raise ContractError(f"{where} holds test fields {paths[:5]}")


def validate_fit(fit: dict, where: str, groups) -> None:
    missing = FIT_KEYS - set(fit)
    if missing:
        raise ContractError(f"{where} lacks {sorted(missing)}")
    p = fit["n_columns"]
    if fit["scale"] != "log":
        raise ContractError(f"{where}.scale must be log")
    if fit["coef_names"][0] != INTERCEPT or fit["coef_names"][1:] != fit["encoded_columns"]:
        raise ContractError(f"{where}: coef_names must be the intercept then encoded_columns")
    if len(fit["coef"]) != p or len(fit["xtx_inv"]) != p or \
            any(len(r) != p for r in fit["xtx_inv"]):
        raise ContractError(f"{where}: coef and xtx_inv must match n_columns")
    if fit["rank"] != p:
        raise ContractError(f"{where}: rank {fit['rank']} != n_columns {p} (rank deficient fit)")
    if fit["df_resid"] != fit["n_train"] - fit["rank"]:
        raise ContractError(f"{where}: df_resid != n_train - rank")
    if list(fit["groups"]) != list(groups):
        raise ContractError(f"{where}: groups differ from the canonical subset")
    if not fit["s2"] > 0 or not fit["t_crit"] > 0:
        raise ContractError(f"{where}: s2 and t_crit must be positive")
    if "zipcode" in groups:
        cats = fit["zipcode_categories"]
        if not cats or fit["zipcode_baseline"] != cats[0]:
            raise ContractError(f"{where}: zipcode baseline must be the first category")
        expected = [f"zipcode_{c}" for c in cats[1:]]
        if [c for c in fit["encoded_columns"] if c.startswith("zipcode_")] != expected:
            raise ContractError(f"{where}: zipcode columns differ from the categories")


PATH_METHODS = ("forward_sfs", "backward_sfs", "rfe", "lasso_path")
METHOD_ORDER = ("allin", *PATH_METHODS)           # overall tie-break order (Brief §5: A…E)
N_K = len(FEATURE_GROUPS)


def path_model_key(method: str, k: int) -> str:
    return f"{method}_k{k:02d}"


def validate_methods(methods: dict, n_folds: int | None) -> None:
    """Each path method has exactly k = 1…18 in order, with its own keys; every step of the
    canonical path and of each fold's path changes exactly one feature group."""
    unknown = set(methods) - set(PATH_METHODS)
    if unknown:
        raise ContractError(f"unknown path methods {sorted(unknown)} (metric-only models and "
                            "baselines are not path methods)")
    for method, items in methods.items():
        if [e.get("k") for e in items] != list(range(1, N_K + 1)):
            raise ContractError(f"methods.{method} must hold k = 1…{N_K} once each, in order")
        for i, entry in enumerate(items):
            where = f"methods.{method}[{i}]"
            if entry["method"] != method or entry["model_key"] != path_model_key(method, i + 1):
                raise ContractError(f"{where}: method or model_key does not match")
            validate_entry(entry, where, n_folds)
            if i:
                prev = items[i - 1]
                paths = [(prev["canonical_groups"], entry["canonical_groups"])] + list(
                    zip(prev["fold_groups"], entry["fold_groups"]))
                if any(not set(a) < set(b) for a, b in paths):
                    raise ContractError(f"{where}: the step from k={i} to k={i + 1} must add "
                                        "exactly one group (canonical and every fold)")


def _cv_rmse(entry):
    return entry["cv"]["mean"]["rmse"] if entry["status"]["state"] == "valid" else None


def validate_winners(winners: dict, entries: dict, methods: dict | None = None) -> None:
    """Winners are the recomputable CV winners; the authorized set is their union (shared models
    once) and never holds a metric-only model (G-2; #61 R1 F-3)."""
    authorized = winners.get("authorized_test_models")
    if not authorized or "allin" not in authorized:
        raise ContractError("winners.authorized_test_models must include allin")
    if len(set(authorized)) != len(authorized):
        raise ContractError("winners.authorized_test_models has duplicates")
    if set(authorized) & set(METRIC_ONLY_KEYS):
        raise ContractError("metric-only models are never CV winners")
    for key in authorized:
        if key not in entries:
            raise ContractError(f"authorized model {key} has no entry")
        if entries[key]["status"]["state"] != "valid":
            raise ContractError(f"authorized model {key} is invalid")
    method_winners = winners.get("method_winners", {})
    if set(method_winners) - set(PATH_METHODS):
        raise ContractError(f"method winners only for path methods, not "
                            f"{sorted(set(method_winners) - set(PATH_METHODS))} (G-2)")
    flagged = {e["model_key"] for e in entries.values()
               if e["is_method_winner"] and e["method"] != "allin"}
    if flagged != {w["model_key"] for w in method_winners.values()}:
        raise ContractError("is_method_winner flags differ from winners.method_winners")
    for method, w in method_winners.items():
        entry = entries.get(w["model_key"])
        if entry is None or not entry["is_method_winner"] or entry["method"] != method:
            raise ContractError(f"method winner {w['model_key']} does not match its entry")
        if methods is not None and method in methods:
            valid = [e for e in methods[method] if e["status"]["state"] == "valid"]
            best = min(valid, key=lambda e: (_cv_rmse(e), e["k"])) if valid else None
            if best is None or best["model_key"] != w["model_key"] or w["k"] != best["k"]:
                raise ContractError(f"method winner of {method} is not the valid entry with the "
                                    "lowest CV RMSE (ties: smaller k)")
    if methods is not None and set(methods) != set(method_winners):
        raise ContractError("every path method in methods needs its CV winner")
    if winners.get("complete"):
        overall = winners.get("overall")
        if overall is None or set(method_winners) != set(PATH_METHODS):
            raise ContractError("complete winners need every method winner and the overall one")
        pool = [("allin", "allin")] + [(m, method_winners[m]["model_key"])
                                       for m in PATH_METHODS]
        method, key = min(pool, key=lambda t: (_cv_rmse(entries[t[1]]), METHOD_ORDER.index(t[0])))
        if overall["model_key"] != key or overall.get("method") != method:
            raise ContractError("overall CV winner is not the lowest CV RMSE among the method "
                                "winners and All-in (ties: fixed method order)")
    elif winners.get("overall") is not None:
        raise ContractError("incomplete winners cannot name an overall CV winner")
    # authorized = {All-in} ∪ method winners ∪ {overall}, a shared model (same canonical subset)
    # once under its test_model_key (#61 R1 F-3)
    named = [("allin", (winners.get("allin") or {}).get("test_model_key", "allin"))]
    named += [(w["model_key"], w.get("test_model_key", w["model_key"]))
              for w in method_winners.values()]
    if winners.get("overall") is not None:
        o = winners["overall"]
        named.append((o["model_key"], o.get("test_model_key", o["model_key"])))
    for key, tkey in named:
        if tkey not in authorized or key not in entries or tkey not in entries:
            raise ContractError(f"winner {key} is scored under {tkey}, which is not authorized")
        if list(entries[key]["canonical_groups"]) != list(entries[tkey]["canonical_groups"]):
            raise ContractError(f"winner {key} and its test model {tkey} are different models")
    if set(authorized) != {t for _, t in named}:
        raise ContractError(f"authorized set {sorted(authorized)} differs from All-in, the "
                            f"method winners and the overall winner {sorted({t for _, t in named})}")
    subsets = [tuple(entries[k]["canonical_groups"]) for k in authorized]
    if len(set(subsets)) != len(subsets):
        raise ContractError("the authorized set scores one model (canonical subset) twice")


# --- comparison models in ``baselines`` (Spec rev 5 「對照模型」; CC-1; SR-11) -------------------

BASELINE_KEYS = ("allin", "ridge", "lasso", "pvalue_backward")
PVALUE_KEY = "pvalue_backward"
METRIC_ONLY_ENTRY_KEYS = {"model_key", "method", "kind", "label", "groups", "standardized",
                          "target", "objective", "alpha", "alpha_grid", "alpha_rule",
                          "alpha_at_grid_edge", "cv_by_alpha", "cv", "adj_r2_log", "adj_r2_note",
                          "offers", "is_cv_winner_candidate"}
# Fields that would let anything outside the one-time evaluation score a metric-only model, or
# that belong to the OLS prediction interval (CC-1 (5); DA §11: Ridge/Lasso have no ``fit``).
METRIC_ONLY_FORBIDDEN = {"fit", "coef", "coef_names", "intercept", "xtx_inv", "s2", "t_crit",
                         "df_resid", "center", "encoded_columns"}
PVALUE_ENTRY_KEYS = {"model_key", "method", "label", "role", "criterion", "threshold", "k",
                     "canonical_groups", "fold_groups", "folds_agree", "status", "cv",
                     "fit_summary", "elimination", "final_p_values", "is_cv_winner_candidate",
                     "timing_s"}


def _check_cv_layout(cv: dict, where: str, n_folds: int | None) -> None:
    if cv.get("scale") != "USD":
        raise ContractError(f"{where}.cv must be on the USD scale")
    if len(cv.get("folds", [])) != cv.get("n_folds"):
        raise ContractError(f"{where}.cv: fold records differ from n_folds")
    if n_folds is not None and cv["n_folds"] != n_folds:
        raise ContractError(f"{where}.cv.n_folds {cv['n_folds']} != meta.cv.n_folds {n_folds}")
    if cv.get("mean") is not None:
        for m in CV_METRIC_KEYS:
            values = [f[m] for f in cv["folds"]]
            if not np.isclose(np.mean(values), cv["mean"][m], rtol=1e-12, atol=1e-9):
                raise ContractError(f"{where}.cv.mean.{m} is not the mean of the folds")


def validate_metric_only_entry(entry: dict, name: str, n_folds: int | None) -> None:
    """Ridge/Lasso: ``cv`` (USD) and the training-CV alpha only; no fit, no PI fields (CC-1)."""
    where = f"baselines.{name}"
    forbidden = METRIC_ONLY_FORBIDDEN & set(entry)
    if forbidden:
        raise ContractError(f"{where} must not hold {sorted(forbidden)} (metric-only)")
    if set(entry) != METRIC_ONLY_ENTRY_KEYS:
        raise ContractError(f"{where} keys differ: {sorted(set(entry) ^ METRIC_ONLY_ENTRY_KEYS)}")
    if entry["model_key"] != name or entry["method"] != name or entry["kind"] != "metric_only":
        raise ContractError(f"{where}: model_key, method and kind must be {name}/metric_only")
    if entry["groups"] != list(FEATURE_GROUPS) or entry["standardized"] is not True:
        raise ContractError(f"{where}: all 18 feature groups, standardized")
    grid = entry["alpha_grid"]
    alpha = entry["alpha"]
    if not isinstance(alpha, (int, float)) or not np.isfinite(alpha) or alpha <= 0 \
            or alpha not in grid:
        raise ContractError(f"{where}.alpha must be a positive value of its grid")
    curve = entry["cv_by_alpha"]
    if [r["alpha"] for r in curve] != grid:
        raise ContractError(f"{where}.cv_by_alpha must follow alpha_grid")
    best = min(curve, key=lambda r: (r["rmse"], -r["alpha"]))
    if best["alpha"] != alpha:
        raise ContractError(f"{where}.alpha is not the lowest training-CV RMSE of the grid "
                            "(ties: larger alpha)")
    edge = "lower" if alpha == min(grid) else "upper" if alpha == max(grid) else None
    if entry["alpha_at_grid_edge"] != edge:
        raise ContractError(f"{where}.alpha_at_grid_edge must be {edge!r}")
    cv = entry["cv"]
    _check_cv_layout(cv, where, n_folds)
    if cv["mean"] is None:
        raise ContractError(f"{where}.cv needs its mean")
    at = curve[grid.index(alpha)]
    for m in CV_METRIC_KEYS:
        if not np.isclose(at[m], cv["mean"][m], rtol=1e-12, atol=1e-9):
            raise ContractError(f"{where}.cv.mean.{m} differs from cv_by_alpha at the alpha")
    if entry["adj_r2_log"] is not None:
        raise ContractError(f"{where}: Adjusted R² is not applicable to Ridge/Lasso")
    if any(entry["offers"].get(k) for k in ("prediction_interval", "coverage_statistics",
                                            "live_prediction")):
        raise ContractError(f"{where}: metric-only models offer no PI, coverage or prediction")
    if entry["is_cv_winner_candidate"] is not False:
        raise ContractError(f"{where} is never a CV winner candidate (CC-1 (2))")


def validate_pvalue_entry(entry: dict, n_folds: int | None) -> None:
    """The lecture's p-value backward comparison: one subset, fold-internal CV, never a winner."""
    where = f"baselines.{PVALUE_KEY}"
    if set(entry) != PVALUE_ENTRY_KEYS:
        raise ContractError(f"{where} keys differ: {sorted(set(entry) ^ PVALUE_ENTRY_KEYS)}")
    if entry["model_key"] != PVALUE_KEY or entry["method"] != PVALUE_KEY:
        raise ContractError(f"{where}: model_key and method must be {PVALUE_KEY}")
    for groups in [entry["canonical_groups"], *entry["fold_groups"]]:
        if list(groups) != [g for g in FEATURE_GROUPS if g in set(groups)] \
                or len(set(groups)) != len(groups):
            raise ContractError(f"{where}: subsets must be feature groups in canonical order")
    if entry["k"] != len(entry["canonical_groups"]):
        raise ContractError(f"{where}.k must be the size of the canonical subset")
    cv = entry["cv"]
    _check_cv_layout(cv, where, n_folds)
    if len(entry["fold_groups"]) != cv["n_folds"]:
        raise ContractError(f"{where}: one subset per fold")
    for record, groups in zip(cv["folds"], entry["fold_groups"]):
        if list(record.get("groups", [])) != list(groups):
            raise ContractError(f"{where}: fold {record.get('fold')} groups differ")
    agree = sum(1 for g in entry["fold_groups"] if list(g) == list(entry["canonical_groups"]))
    if entry["folds_agree"] != agree:
        raise ContractError(f"{where}.folds_agree {entry['folds_agree']} != {agree}")
    if entry["status"]["state"] == "valid":
        if cv["mean"] is None or entry["fit_summary"] is None:
            raise ContractError(f"{where}: a valid entry needs cv.mean and fit_summary")
        f = entry["fit_summary"]
        adj = 1 - (1 - f["r2_log"]) * (f["n_train"] - 1) / (f["n_train"] - f["rank"])
        if f["scale"] != "log" or f["rank"] != f["n_columns"] or \
                not np.isclose(adj, f["adj_r2_log"], rtol=1e-12):
            raise ContractError(f"{where}.fit_summary: log scale, full rank, Adjusted R² with "
                                "the actual rank")
    if not 0 < entry["threshold"] < 1 or entry["is_cv_winner_candidate"] is not False:
        raise ContractError(f"{where}: a threshold in (0, 1); never a CV winner candidate")
    if any(p["p_value"] > entry["threshold"] for p in entry["final_p_values"].values()):
        raise ContractError(f"{where}: a group left in the subset has p > threshold")
    if set(entry["final_p_values"]) != set(entry["canonical_groups"]):
        raise ContractError(f"{where}.final_p_values must cover the canonical subset")


def validate_baselines(baselines: dict, n_folds: int | None) -> None:
    extra = set(baselines) - set(BASELINE_KEYS)
    if extra:
        raise ContractError(f"unknown baselines {sorted(extra)}")
    for name in METRIC_ONLY_KEYS:
        if name in baselines:
            validate_metric_only_entry(baselines[name], name, n_folds)
    if PVALUE_KEY in baselines:
        validate_pvalue_entry(baselines[PVALUE_KEY], n_folds)


def validate_test(md: dict) -> None:
    test, ti = md["test"], md["test_inputs"]
    if not ti.get("written"):
        raise ContractError("test results need the test_inputs rows from the same run")
    winners = md.get("winners") or {}
    authorized = set(winners.get("authorized_test_models") or [])
    ols_keys = {k for k, v in test.items() if v.get("kind") == "ols_subset"}
    metric_keys = {k for k, v in test.items() if v.get("kind") == "metric_only"}
    if ols_keys | metric_keys != set(test):
        raise ContractError("every test entry has kind ols_subset or metric_only")
    if ols_keys != authorized:
        raise ContractError(f"ols_subset keys {sorted(ols_keys)} != authorized "
                            f"{sorted(authorized)}")
    if metric_keys != set(METRIC_ONLY_KEYS):
        # CC-1: Ridge and Lasso are each scored once in the same evaluation (#61 R1 F-1, C3).
        raise ContractError(f"metric_only entries {sorted(metric_keys)} must be exactly "
                            f"{list(METRIC_ONLY_KEYS)}")
    n = ti["n_rows"]
    actual = np.array([r[-1] for r in ti["rows"]], dtype=float)
    baselines = md.get("baselines") or {}
    for key in metric_keys:
        if set(test[key]) != METRIC_ONLY_TEST_KEYS:
            raise ContractError(f"test.{key} (metric_only) has keys {sorted(test[key])}")
        if key in baselines and test[key]["alpha"] != baselines[key]["alpha"]:
            # CC-1 (1)(4): the scored model uses the alpha fixed by training CV
            raise ContractError(f"test.{key}.alpha differs from the training-CV alpha")
        if test[key]["n_test"] != ti["n_rows"]:
            raise ContractError(f"test.{key}: n_test differs from the test_inputs rows")
    if PVALUE_KEY in test:
        raise ContractError("the p-value backward comparison is never scored on the test set")
    for key, entry in test.items():
        if entry.get("model_key") != key:
            raise ContractError(f"test.{key}.model_key is {entry.get('model_key')!r}")
    for key in ols_keys:
        entry = test[key]
        if set(entry) != OLS_TEST_KEYS:
            raise ContractError(f"test.{key} (ols_subset) keys differ: "
                                f"{sorted(set(entry) ^ OLS_TEST_KEYS)}")
        if entry["n_test"] != n or any(len(entry[f]) != n
                                      for f in ("predicted", "lower", "upper", "covered")):
            raise ContractError(f"test.{key}: per-row fields must have n_test values")
        lo, pt, hi = (np.array(entry[f], dtype=float) for f in ("lower", "predicted", "upper"))
        if not (np.all(lo > 0) and np.all(lo <= pt) and np.all(pt <= hi)):
            raise ContractError(f"test.{key}: need 0 < lower <= predicted <= upper")
        covered = np.array(entry["covered"], dtype=bool)
        if not np.array_equal(covered, (lo <= actual) & (actual <= hi)):
            raise ContractError(f"test.{key}: covered differs from lower <= actual <= upper")
        if entry["n_covered"] != int(covered.sum()):
            raise ContractError(f"test.{key}: n_covered differs from the covered rows")
        if not np.isclose(entry["coverage"], covered.sum() / n, rtol=0, atol=1e-12):
            raise ContractError(f"test.{key}: coverage != n_covered / n_test")
        if not np.isclose(entry["mean_width"], np.mean(hi - lo), rtol=1e-12):
            raise ContractError(f"test.{key}: mean_width differs from the intervals")
        fit = (model_entries(md).get(key) or {}).get("fit") or {}
        uses_zip = "zipcode" in (fit.get("groups") or [])
        expected = ti.get("n_unseen_zipcode") if uses_zip else 0
        if entry["n_unseen_zipcode"] != expected:
            raise ContractError(f"test.{key}.n_unseen_zipcode {entry['n_unseen_zipcode']} != "
                                f"{expected} (SR-07)")


def validate_model_data(md: dict) -> None:
    """Contract invariants that hold at every stage (sections not yet written are skipped)."""
    allowed = {"meta", "preprocess", "inputs", "test_inputs", "methods", "baselines", "winners",
               "test"}
    extra = set(md) - allowed
    if extra:
        raise ContractError(f"unknown model_data sections {sorted(extra)}")
    validate_test_inputs(md["test_inputs"], n_test=md["meta"].get("split", {}).get("n_test"))
    for section in ("methods", "baselines"):
        if section in md:
            paths = test_field_paths(md[section])
            if paths:
                raise ContractError(f"{section} holds test fields {paths[:5]}")
    n_folds = (md["meta"].get("cv") or {}).get("n_folds")
    if "baselines" in md:
        validate_baselines(md["baselines"], n_folds)
    allin = (md.get("baselines") or {}).get("allin")
    if allin is not None:
        validate_entry(allin, "baselines.allin", n_folds)
        if allin["method"] != "allin" or allin["k"] != len(FEATURE_GROUPS) \
                or allin["canonical_groups"] != list(FEATURE_GROUPS):
            raise ContractError("baselines.allin must be the single OLS on all 18 feature groups")
        if allin["status"]["state"] != "valid":
            raise ContractError("an invalid All-in baseline is an experiment-level failure")
    if "methods" in md:
        validate_methods(md["methods"], n_folds)
    if "winners" in md:
        validate_winners(md["winners"], model_entries(md), md.get("methods"))
    if "test" in md:
        validate_test(md)
    elif md["test_inputs"].get("written"):
        raise ContractError("test_inputs rows are written only together with test")
