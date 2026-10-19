"""Data loading and structural validation (Spec rev 5 「資料、計數與前處理」)."""
import numpy as np
import pandas as pd
import pytest

from hw2 import data


def _load(path, frame, sha):
    return data.load_and_split(path, expected_sha256=sha, expected_rows=len(frame),
                               expected_unique_ids=frame["id"].nunique(), n_folds=3)


def test_real_csv_matches_the_pinned_sha256(real_csv_present):
    assert data.verify_sha256(real_csv_present) == data.EXPECTED_SHA256


def test_real_csv_structure(real_csv_present):
    facts = data.structural_facts(real_csv_present)
    assert facts == {"n_rows": 21613, "n_columns": 21, "n_unique_ids": 21436,
                     "n_repeat_sales": 177, "sqft_identity_holds": True}


def test_sha256_mismatch_stops_with_expected_and_actual(tmp_path, real_csv_present):
    copy = tmp_path / "kc_house_data.csv"
    raw = bytearray(real_csv_present.read_bytes())
    raw[-2] = ord("8") if raw[-2] != ord("8") else ord("9")
    copy.write_bytes(bytes(raw))
    actual = data.file_sha256(copy)
    with pytest.raises(data.DataIntegrityError) as err:
        data.load_and_split(copy)
    assert data.EXPECTED_SHA256 in str(err.value) and actual in str(err.value)


def test_sha256_is_checked_before_parsing(tmp_path):
    bad = tmp_path / "not_a_csv.csv"
    bad.write_bytes(b"\x00\x01 not csv")
    with pytest.raises(data.DataIntegrityError, match="sha256 mismatch"):
        data.load_and_split(bad)


@pytest.mark.parametrize("mutate, message", [
    (lambda f: f[list(reversed(f.columns))], "schema mismatch"),
    (lambda f: f.drop(columns=["sqft_lot15"]), "schema mismatch"),
    (lambda f: f.iloc[:-1], "row count mismatch"),
    (lambda f: f.assign(id=f["id"].iloc[0]), "unique id count mismatch"),
    (lambda f: f.assign(sqft_living=f["sqft_living"] + (np.arange(len(f)) == 3)), "sqft_living"),
    (lambda f: f.assign(grade=f["grade"].where(np.arange(len(f)) != 5)), "missing values"),
])
def test_structural_violations_stop(synthetic_frame, mutate, message):
    expected_rows = len(synthetic_frame)
    expected_ids = synthetic_frame["id"].nunique()
    with pytest.raises(data.DataIntegrityError, match=message):
        data.validate_structure(mutate(synthetic_frame.copy()), expected_rows, expected_ids)


def test_load_and_split_returns_training_rows_and_test_identifiers_only(synthetic_csv):
    path, frame, sha = synthetic_csv
    prepared = _load(path, frame, sha)
    # Training rows carry the raw columns; the test side is identifiers only.
    assert list(prepared.training.columns) == ["row", *data.EXPECTED_COLUMNS, "fold"]
    assert prepared.test_rows.dtype.kind == "i" and prepared.test_ids.ndim == 1
    assert not set(prepared.training["row"]) & set(prepared.test_rows.tolist())
    assert prepared.n_train + prepared.n_test == len(frame)
    np.testing.assert_array_equal(prepared.test_ids, frame["id"].to_numpy()[prepared.test_rows])
    # No attribute of the result holds a test row's features or price.
    for name, value in vars(prepared).items():
        if isinstance(value, pd.DataFrame):
            assert set(value["row"]).isdisjoint(prepared.test_rows.tolist()), name
    assert prepared.timings_s.keys() == {"data_load_validate", "split_and_folds"}


def test_training_rows_keep_the_csv_values(synthetic_csv):
    path, frame, sha = synthetic_csv
    prepared = _load(path, frame, sha)
    original = frame.iloc[prepared.training["row"].to_numpy()].reset_index(drop=True)
    pd.testing.assert_frame_equal(
        prepared.training[list(data.EXPECTED_COLUMNS)].reset_index(drop=True),
        original.astype({"id": "str", "date": "str", "zipcode": "str"}),
        check_dtype=False)


def test_no_public_function_returns_the_parsed_file():
    """#60 R1 F-3: the full frame (which holds the test rows) is private to the data module."""
    assert not hasattr(data, "read_csv")
    public = [name for name in dir(data) if not name.startswith("_")]
    assert "structural_facts" in public and "_read_csv" not in public
