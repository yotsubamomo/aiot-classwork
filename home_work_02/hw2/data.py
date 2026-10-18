"""Loading and structural validation of the King County House Sales CSV.

Test-data isolation (DA TR-01, ``derivation-SPEC.md`` §9.6): the whole file is read only for the
structural checks (sha256, schema, row count, unique ``id`` count, the ``sqft`` identity) and for
the split, which needs only the ``id`` column. :func:`load_and_split` then returns the training rows
and the test-row identifiers (row positions, ``id``) with n_test; it never returns the features or
``price`` of a test row. Distributions and extreme values are computed from training rows only
(B-14).
"""
import hashlib
import time
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

from . import split as split_mod
from .paths import DATA_CSV, N_FOLDS, SEED, TEST_FRACTION

EXPECTED_SHA256 = "d0875baa0251b21d4bdc9d2ae940a4fe0bb6009824f23dd0e2a5b2bf04557b7e"
EXPECTED_COLUMNS = (
    "id", "date", "price", "bedrooms", "bathrooms", "sqft_living", "sqft_lot", "floors",
    "waterfront", "view", "condition", "grade", "sqft_above", "sqft_basement", "yr_built",
    "yr_renovated", "zipcode", "lat", "long", "sqft_living15", "sqft_lot15",
)
EXPECTED_ROWS = 21613
EXPECTED_UNIQUE_IDS = 21436

DATASET = {
    "name": "House Sales in King County, USA",
    "kaggle_slug": "harlfoxem/housesalesprediction",
    "url": "https://www.kaggle.com/datasets/harlfoxem/housesalesprediction",
    "license": "CC0: Public Domain (CC0-1.0)",
    "file": "data/kc_house_data.csv",
    "acquired_from": ("GitHub mirror of the Kaggle file provided by the acceptor on 2026-10-18; "
                      "its sha256 equals the value pinned in the Brief (§4), so no re-pin"),
}

# Identifiers and nominal codes keep their exact CSV text (ids are zero-padded to 10 digits).
_TEXT_COLUMNS = {"id": "str", "date": "str", "zipcode": "str"}


class DataIntegrityError(ValueError):
    """The data file does not match the pinned file or the expected structure."""


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_sha256(path: Path, expected: str = EXPECTED_SHA256) -> str:
    """The file's sha256; raises DataIntegrityError naming both values when it differs."""
    actual = file_sha256(path)
    if actual != expected:
        raise DataIntegrityError(
            f"sha256 mismatch for {path}: expected {expected}, actual {actual}. "
            "If the file was re-downloaded on purpose, record a re-pin (Brief §4) before use.")
    return actual


def read_csv(path: Path) -> pd.DataFrame:
    """Parse the CSV (call :func:`verify_sha256` first)."""
    return pd.read_csv(path, dtype=_TEXT_COLUMNS)


def validate_structure(df: pd.DataFrame, expected_rows: int = EXPECTED_ROWS,
                       expected_unique_ids: int = EXPECTED_UNIQUE_IDS) -> dict:
    """Structural checks only; returns the structural facts. Raises DataIntegrityError."""
    columns = tuple(df.columns)
    if columns != EXPECTED_COLUMNS:
        raise DataIntegrityError(
            f"schema mismatch: expected {len(EXPECTED_COLUMNS)} columns {list(EXPECTED_COLUMNS)}, "
            f"actual {len(columns)} columns {list(columns)}")
    if len(df) != expected_rows:
        raise DataIntegrityError(f"row count mismatch: expected {expected_rows}, actual {len(df)}")
    n_ids = int(df["id"].nunique())
    if n_ids != expected_unique_ids:
        raise DataIntegrityError(
            f"unique id count mismatch: expected {expected_unique_ids}, actual {n_ids}")
    if df.isna().any().any():
        missing = df.columns[df.isna().any()].tolist()
        raise DataIntegrityError(f"missing values in columns {missing}")
    identity = df["sqft_living"] == df["sqft_above"] + df["sqft_basement"]
    if not bool(identity.all()):
        bad = np.flatnonzero(~identity.to_numpy())
        raise DataIntegrityError(
            f"sqft_living != sqft_above + sqft_basement on {bad.size} rows "
            f"(first row positions {bad[:5].tolist()})")
    return {
        "n_rows": int(len(df)),
        "n_columns": len(columns),
        "n_unique_ids": n_ids,
        "n_repeat_sales": int(len(df)) - n_ids,
        "sqft_identity_holds": True,
    }


@dataclass(frozen=True)
class PreparedData:
    """Result of the data stage: training rows plus test identifiers only."""
    sha256: str
    facts: dict                      # full-data structural facts (validate_structure)
    training: pd.DataFrame           # training rows: raw CSV columns + 'row' (CSV position) + 'fold'
    test_rows: np.ndarray            # CSV row positions (0-based) of the test sales
    test_ids: np.ndarray             # their house ids (text, as in the CSV)
    seed: int
    test_fraction: float
    n_folds: int
    timings_s: dict = field(default_factory=dict)

    @property
    def n_train(self) -> int:
        return int(len(self.training))

    @property
    def n_test(self) -> int:
        return int(self.test_rows.size)


def load_and_split(path: Path = DATA_CSV, expected_sha256: str = EXPECTED_SHA256,
                   seed: int = SEED, test_fraction: float = TEST_FRACTION,
                   n_folds: int = N_FOLDS, expected_rows: int = EXPECTED_ROWS,
                   expected_unique_ids: int = EXPECTED_UNIQUE_IDS) -> PreparedData:
    """sha256 -> parse -> structural checks -> grouped split -> grouped folds on training rows.

    The full frame stays local to this function; only training rows and test identifiers leave.
    """
    t0 = time.perf_counter()
    sha = verify_sha256(path, expected_sha256)
    full = read_csv(path)
    facts = validate_structure(full, expected_rows, expected_unique_ids)
    t1 = time.perf_counter()

    ids = full["id"].to_numpy()
    train_pos, test_pos = split_mod.group_train_test_split(ids, test_fraction, seed)
    training = full.iloc[train_pos].copy()
    training.insert(0, "row", train_pos)
    training["fold"] = split_mod.group_kfold(training["id"].to_numpy(), n_folds, seed)
    training = training.reset_index(drop=True)
    test_ids = ids[test_pos].copy()
    del full, ids
    t2 = time.perf_counter()

    return PreparedData(sha256=sha, facts=facts, training=training, test_rows=test_pos,
                        test_ids=test_ids, seed=seed, test_fraction=test_fraction,
                        n_folds=n_folds,
                        timings_s={"data_load_validate": round(t1 - t0, 4),
                                   "split_and_folds": round(t2 - t1, 4)})
