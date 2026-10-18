"""HW2 King County multiple linear regression: analysis package.

The notebook ``hw2.ipynb`` is the main program; it calls the public functions of these modules.

- ``paths``: unit paths, the seed and the untracked local configuration locations.
- ``data``: loading and structural validation of the King County CSV.
- ``preprocess``: fixed row-wise transforms and the training-only fitted encoding.
- ``split``: the grouped 80/20 train/test split and the grouped CV folds.
- ``ols``: OLS on ln(price) with the actual model rank, and the parametric 95% PI.
- ``metrics``: USD metrics and prediction-interval coverage.
- ``models``: OLS candidates (grouped CV and canonical fit), rank-deficiency semantics, the
  All-in baseline and the CV winners.
- ``selection``: the four feature-group selection paths (Forward SFS, Backward SFS, RFE, Lasso
  path ranking), fold-internal on each fold's training rows and canonical on the training set.
- ``comparison``: the metric-only Ridge and Lasso (training-CV alpha) and the lecture's p-value
  backward elimination (comparison rows only).
- ``testgate``: the one-time test-evaluation gate (G-3; opened for the official data in #63).
- ``contract``: the ``model_data`` section schemas and their invariants.
- ``export``: building and writing ``model_data`` (``.json`` and ``.js``).
- ``fixture``: synthetic fixtures run through the same code path (never written inside the unit).
- ``offline_scan``: the static scan for external resource references in the dashboard.
- ``local_config``: reading the untracked packaging configuration (student id).
"""
