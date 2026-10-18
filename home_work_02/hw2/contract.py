"""Schemas of ``model_data`` sections and their validation.

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
