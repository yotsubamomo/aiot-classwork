"""Grouped split and grouped folds (Spec rev 5 次 seam「分割」; Brief §4, §10)."""
import itertools

import numpy as np
import pandas as pd
import pytest

from hw2 import data, split
from hw2.paths import N_FOLDS, SEED


@pytest.fixture(scope="module")
def real_ids():
    if not data.DATA_CSV.is_file():
        pytest.skip("data file missing")
    data.verify_sha256(data.DATA_CSV)
    # Only the id column: the split needs nothing else.
    return pd.read_csv(data.DATA_CSV, usecols=["id"], dtype={"id": "str"})["id"].to_numpy()


def test_train_and_test_share_no_house(real_ids):
    train, test = split.group_train_test_split(real_ids, 0.2, SEED)
    assert set(real_ids[train]).isdisjoint(real_ids[test])


def test_train_and_test_cover_every_row_once(real_ids):
    train, test = split.group_train_test_split(real_ids, 0.2, SEED)
    assert np.array_equal(np.sort(np.concatenate([train, test])), np.arange(real_ids.size))


def test_same_seed_reproduces_and_another_seed_differs(real_ids):
    a = split.group_train_test_split(real_ids, 0.2, SEED)
    b = split.group_train_test_split(real_ids, 0.2, SEED)
    c = split.group_train_test_split(real_ids, 0.2, SEED + 1)
    assert np.array_equal(a[0], b[0]) and np.array_equal(a[1], b[1])
    assert not np.array_equal(a[1], c[1])


def test_split_is_about_80_20(real_ids):
    _, test = split.group_train_test_split(real_ids, 0.2, SEED)
    assert abs(test.size / real_ids.size - 0.2) < 0.005


def test_folds_are_pairwise_disjoint_by_house_and_cover_training(real_ids):
    train, _ = split.group_train_test_split(real_ids, 0.2, SEED)
    train_ids = real_ids[train]
    folds = split.group_kfold(train_ids, N_FOLDS, SEED)
    assert set(np.unique(folds)) == set(range(N_FOLDS))
    houses = [set(train_ids[folds == f]) for f in range(N_FOLDS)]
    for a, b in itertools.combinations(houses, 2):
        assert a.isdisjoint(b)
    assert set().union(*houses) == set(train_ids)
    counts = np.bincount(folds)
    assert counts.max() - counts.min() < 0.01 * counts.mean()


def test_folds_reproduce_with_the_same_seed(real_ids):
    a = split.group_kfold(real_ids, N_FOLDS, SEED)
    b = split.group_kfold(real_ids, N_FOLDS, SEED)
    assert np.array_equal(a, b)
    assert not np.array_equal(a, split.group_kfold(real_ids, N_FOLDS, SEED + 1))


def test_repeat_sales_stay_together(synthetic_frame):
    ids = synthetic_frame["id"].to_numpy()
    assert len(set(ids)) < ids.size                      # the fixture has repeat sales
    train, test = split.group_train_test_split(ids, 0.25, 3)
    side = {}
    for pos in train:
        side.setdefault(ids[pos], set()).add("train")
    for pos in test:
        side.setdefault(ids[pos], set()).add("test")
    assert all(len(s) == 1 for s in side.values())
    folds = split.group_kfold(ids, 4, 3)
    for house in set(ids):
        assert len(set(folds[ids == house])) == 1


def test_fold_assignment_does_not_depend_on_row_order(synthetic_frame):
    ids = synthetic_frame["id"].to_numpy()
    perm = np.random.default_rng(0).permutation(ids.size)
    folds = split.group_kfold(ids, 4, 3)
    folds_perm = split.group_kfold(ids[perm], 4, 3)
    assert np.array_equal(folds[perm], folds_perm)


@pytest.mark.parametrize("fraction", [0.0, 1.0, -0.1, 1.5])
def test_invalid_test_fraction(fraction):
    with pytest.raises(ValueError):
        split.group_train_test_split(["a", "b", "c"], fraction)


def test_too_many_folds():
    with pytest.raises(ValueError):
        split.group_kfold(["a", "b", "a"], 3)


def test_real_data_stage_uses_the_split_and_folds(prepared_real, real_ids):
    train, test = split.group_train_test_split(real_ids, prepared_real.test_fraction,
                                               prepared_real.seed)
    assert np.array_equal(prepared_real.training["row"].to_numpy(), train)
    assert np.array_equal(prepared_real.test_rows, test)
    expected_folds = split.group_kfold(real_ids[train], prepared_real.n_folds, prepared_real.seed)
    assert np.array_equal(prepared_real.training["fold"].to_numpy(), expected_folds)
    assert prepared_real.n_train + prepared_real.n_test == 21613
