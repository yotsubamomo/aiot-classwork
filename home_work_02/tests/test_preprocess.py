"""Fixed transforms and training-only fitted preprocessing (Spec rev 5 次 seam「前處理」)."""
import numpy as np
import pandas as pd
import pytest

from hw2 import data, preprocess as pp


def test_feature_counts_and_canonical_order():
    assert len(pp.SOURCE_FEATURES) == 19 and len(pp.FEATURE_GROUPS) == 18
    assert "id" not in pp.SOURCE_FEATURES and "price" not in pp.SOURCE_FEATURES
    assert "sqft_basement" in pp.SOURCE_FEATURES and "sqft_basement" not in pp.FEATURE_GROUPS
    order = [c for c in data.EXPECTED_COLUMNS if c in pp.FEATURE_GROUPS]
    assert list(pp.FEATURE_GROUPS) == order


@pytest.mark.parametrize("text, days", [
    ("20140101T000000", 0),
    ("20140102T000000", 1),
    ("20141013T000000", 285),     # 273 days to Oct 1 + 12
    ("20150101T000000", 365),
    ("20150527T000000", 511),     # 365 + 146
])
def test_sale_days(text, days):
    assert pp.sale_days([text])[0] == days


@pytest.mark.parametrize("text", ["2014-10-13", "20141013", "20141332T000000", "20140230T000000"])
def test_sale_days_rejects_malformed_dates(text):
    with pytest.raises(pp.PreprocessError):
        pp.sale_days([text])


def test_days_to_iso_inverts_sale_days():
    assert pp.days_to_iso(285) == "2014-10-13"
    assert pp.days_to_iso(285.5) == "2014-10-13"


@pytest.mark.parametrize("renovated, built, flag, effective", [
    (0, 1955, 0, 1955),
    (1991, 1951, 1, 1991),
    (2015, 2015, 1, 2015),
])
def test_renovation_columns(renovated, built, flag, effective):
    f, e = pp.renovation_columns([renovated], [built])
    assert (f[0], e[0]) == (flag, effective)


def test_renovation_rejects_negative_years():
    with pytest.raises(pp.PreprocessError):
        pp.renovation_columns([-1], [1950])


def _split_mask(frame, seed=1):
    return np.random.default_rng(seed).random(len(frame)) < 0.7


def _mutate_other_rows(frame, mask):
    other = frame.copy()
    rows = ~mask
    other.loc[rows, "zipcode"] = "99999"
    other.loc[rows, "sqft_living"] = 10**6
    other.loc[rows, "grade"] = 99
    other.loc[rows, "date"] = "20200101T000000"
    return other


def test_fit_uses_only_the_training_rows(synthetic_frame):
    mask = _split_mask(synthetic_frame)
    before = pp.fit_preprocessor(synthetic_frame[mask], standardize=True)
    after = pp.fit_preprocessor(_mutate_other_rows(synthetic_frame, mask)[mask], standardize=True)
    assert before == after
    assert before.zipcode_categories == tuple(sorted(synthetic_frame.loc[mask, "zipcode"].unique()))
    assert before.zipcode_baseline == before.zipcode_categories[0]


def test_categories_come_from_training_rows_only(synthetic_frame):
    mask = synthetic_frame["zipcode"] != "98178"
    pre = pp.fit_preprocessor(synthetic_frame[mask])
    assert "98178" not in pre.zipcode_categories
    assert pp.zipcode_column("98178") not in pre.columns


def test_unseen_zipcode_is_encoded_as_the_baseline(synthetic_frame):
    mask = synthetic_frame["zipcode"] != "98178"
    pre = pp.fit_preprocessor(synthetic_frame[mask])
    held = synthetic_frame[~mask]
    out = pre.transform(held)
    zip_idx = [i for i, c in enumerate(out.columns) if c.startswith(pp.ZIPCODE_PREFIX)]
    assert out.n_unseen_zipcode == len(held) > 0
    assert np.all(out.X[:, zip_idx] == 0)
    baseline_rows = synthetic_frame[synthetic_frame["zipcode"] == pre.zipcode_baseline]
    assert np.all(pre.transform(baseline_rows).X[:, zip_idx] == 0)
    assert pre.transform(baseline_rows).n_unseen_zipcode == 0


def test_known_zipcode_sets_exactly_its_column(synthetic_frame):
    pre = pp.fit_preprocessor(synthetic_frame)
    row = synthetic_frame[synthetic_frame["zipcode"] == "98052"].head(1)
    out = pre.transform(row)
    zip_cols = {c: out.X[0, i] for i, c in enumerate(out.columns) if c.startswith(pp.ZIPCODE_PREFIX)}
    assert zip_cols.pop("zipcode_98052") == 1.0
    assert all(v == 0.0 for v in zip_cols.values())


def test_encoded_columns_in_canonical_order(synthetic_frame):
    pre = pp.fit_preprocessor(synthetic_frame, groups=["zipcode", "yr_renovated", "date", "grade"])
    assert pre.groups == ("date", "grade", "yr_renovated", "zipcode")
    zips = [pp.zipcode_column(c) for c in pre.zipcode_categories[1:]]
    assert pre.columns == ("sale_days", "grade", "is_renovated", "yr_renovated_effective", *zips)


def test_transform_values_for_fixed_columns(synthetic_frame):
    pre = pp.fit_preprocessor(synthetic_frame, groups=["date", "yr_renovated", "bathrooms"])
    out = pre.transform(synthetic_frame)
    flag, eff = pp.renovation_columns(synthetic_frame["yr_renovated"], synthetic_frame["yr_built"])
    np.testing.assert_array_equal(out.X[:, 0], pp.sale_days(synthetic_frame["date"]))
    np.testing.assert_array_equal(out.X[:, 1], synthetic_frame["bathrooms"])
    np.testing.assert_array_equal(out.X[:, 2], flag)
    np.testing.assert_array_equal(out.X[:, 3], eff)


def test_unknown_group_and_empty_fit_are_rejected(synthetic_frame):
    with pytest.raises(pp.PreprocessError):
        pp.fit_preprocessor(synthetic_frame, groups=["sqft_basement"])
    with pytest.raises(pp.PreprocessError):
        pp.fit_preprocessor(synthetic_frame.iloc[0:0])


def test_standardization_statistics_are_training_statistics(synthetic_frame):
    mask = _split_mask(synthetic_frame)
    train = synthetic_frame[mask].copy()
    train["waterfront"] = 0                              # constant on the training rows
    pre = pp.fit_preprocessor(train, standardize=True)
    raw = pp.fit_preprocessor(train).transform(train).X
    for i, column in enumerate(pre.columns):
        if column.startswith(pp.ZIPCODE_PREFIX):
            assert (pre.center[i], pre.scale[i]) == (0.0, 1.0)
        elif column == "waterfront":
            assert pre.scale[i] == 1.0
        else:
            assert pre.center[i] == pytest.approx(raw[:, i].mean())
            assert pre.scale[i] == pytest.approx(raw[:, i].std())
    z = pre.transform(train).X
    non_dummy = [i for i, c in enumerate(pre.columns)
                 if not c.startswith(pp.ZIPCODE_PREFIX) and c != "waterfront"]
    np.testing.assert_allclose(z[:, non_dummy].mean(axis=0), 0, atol=1e-9)


def test_input_ranges_come_from_training_rows_only(synthetic_frame):
    mask = _split_mask(synthetic_frame)
    a = pp.training_input_ranges(synthetic_frame[mask])
    b = pp.training_input_ranges(_mutate_other_rows(synthetic_frame, mask)[mask])
    assert a == b
    train = synthetic_frame[mask]
    grade = a["features"]["grade"]
    assert (grade["min"], grade["max"]) == (train["grade"].min(), train["grade"].max())
    assert grade["median"] == np.median(train["grade"])
    assert a["zipcode_categories"] == sorted(train["zipcode"].unique())
    assert a["features"]["sqft_basement"]["modeled"] is False
    assert set(a["features"]) == set(pp.SOURCE_FEATURES)
    days = pp.sale_days(train["date"])
    assert a["date_range"] == {"min": pp.days_to_iso(days.min()), "max": pp.days_to_iso(days.max())}


def test_real_training_fit_has_the_expected_encoding(prepared_real):
    pre = pp.fit_preprocessor(prepared_real.training)
    cats = sorted(prepared_real.training["zipcode"].unique())
    assert pre.zipcode_categories == tuple(cats)
    assert len(pre.columns) == 1 + 15 + 2 + (len(cats) - 1)
