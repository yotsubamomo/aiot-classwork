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
        "note": ("Rows are written only by the one-time test-evaluation export behind the test "
                 "gate, in the same run as the test results (DA TR-01)."),
    }


def build_test_inputs(rows: pd.DataFrame) -> dict:
    """``test_inputs`` with rows, from a frame holding 'row', the raw CSV columns and 'price'.

    Callers pass only rows they are entitled to: the official test rows behind the test gate
    (#63) or synthetic fixture rows in tests.
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
        if rows or obj.get("n_houses") is not None or obj.get("n_repeat_sales") is not None:
            raise ContractError("unwritten test_inputs must have no rows and null counts")
        return
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


def validate_entry(entry: dict, where: str) -> None:
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
    cv = entry["cv"]
    if cv.get("scale") != "USD":
        raise ContractError(f"{where}.cv must be on the USD scale")
    if len(cv["folds"]) != cv["n_folds"]:
        raise ContractError(f"{where}.cv: fold records differ from n_folds")
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


def validate_winners(winners: dict, entries: dict) -> None:
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
    for method, w in winners.get("method_winners", {}).items():
        entry = entries.get(w["model_key"])
        if entry is None or not entry["is_method_winner"] or entry["method"] != method:
            raise ContractError(f"method winner {w['model_key']} does not match its entry")
    if winners.get("complete"):
        if winners.get("overall") is None or winners["overall"]["model_key"] not in authorized:
            raise ContractError("complete winners need an authorized overall CV winner")
    elif winners.get("overall") is not None:
        raise ContractError("incomplete winners cannot name an overall CV winner")


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
    for key in metric_keys:
        if set(test[key]) != METRIC_ONLY_TEST_KEYS:
            raise ContractError(f"test.{key} (metric_only) has keys {sorted(test[key])}")
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
    allin = (md.get("baselines") or {}).get("allin")
    if allin is not None:
        validate_entry(allin, "baselines.allin")
        if allin["method"] != "allin" or allin["k"] != len(FEATURE_GROUPS) \
                or allin["canonical_groups"] != list(FEATURE_GROUPS):
            raise ContractError("baselines.allin must be the single OLS on all 18 feature groups")
        if allin["status"]["state"] != "valid":
            raise ContractError("an invalid All-in baseline is an experiment-level failure")
    for method, items in (md.get("methods") or {}).items():
        for i, entry in enumerate(items):
            validate_entry(entry, f"methods.{method}[{i}]")
    if "winners" in md:
        validate_winners(md["winners"], model_entries(md))
    if "test" in md:
        validate_test(md)
    elif md["test_inputs"].get("written"):
        raise ContractError("test_inputs rows are written only together with test")
