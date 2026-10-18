"""Grouped train/test split and grouped CV folds (the group is the house ``id``).

All sales of one house land on the same side of the train/test split and in the same CV fold.
Both functions take only the ids, so they never see features or prices.
"""
from collections.abc import Sequence

import numpy as np


def _groups(ids: Sequence) -> tuple[np.ndarray, np.ndarray]:
    """Sorted unique ids and, for each row, the index of its id in that array."""
    unique, inverse = np.unique(np.asarray(ids), return_inverse=True)
    return unique, inverse


def group_train_test_split(ids: Sequence, test_fraction: float = 0.2,
                           seed: int = 42) -> tuple[np.ndarray, np.ndarray]:
    """Row positions (ascending) of the training and test rows.

    The sorted unique ids are permuted with ``numpy.random.default_rng([seed, 0])`` and the first
    ``round(test_fraction * n_houses)`` houses form the test set. The row share is therefore
    approximately ``test_fraction``.
    """
    if not 0.0 < test_fraction < 1.0:
        raise ValueError(f"test_fraction must be in (0, 1), got {test_fraction}")
    unique, inverse = _groups(ids)
    if unique.size < 2:
        raise ValueError("need at least two houses to split")
    perm = np.random.default_rng([seed, 0]).permutation(unique.size)
    n_test_groups = int(round(test_fraction * unique.size))
    n_test_groups = min(max(n_test_groups, 1), unique.size - 1)
    is_test_group = np.zeros(unique.size, dtype=bool)
    is_test_group[perm[:n_test_groups]] = True
    is_test_row = is_test_group[inverse]
    return np.flatnonzero(~is_test_row), np.flatnonzero(is_test_row)


def group_kfold(ids: Sequence, n_folds: int = 5, seed: int = 42) -> np.ndarray:
    """Fold number (0 .. n_folds-1) for each row.

    The sorted unique ids are permuted with ``numpy.random.default_rng([seed, 1])`` and dealt to
    the folds in turn, so the folds hold equal numbers of houses (within one).
    """
    unique, inverse = _groups(ids)
    if n_folds < 2 or unique.size < n_folds:
        raise ValueError(f"need 2 <= n_folds <= number of houses, got {n_folds} for {unique.size}")
    perm = np.random.default_rng([seed, 1]).permutation(unique.size)
    group_fold = np.empty(unique.size, dtype=np.int64)
    group_fold[perm] = np.arange(unique.size) % n_folds
    return group_fold[inverse]
