"""HW2 King County multiple linear regression: analysis package.

The notebook ``hw2.ipynb`` is the main program; it calls the public functions of these modules.

- ``paths``: unit paths, the seed and the untracked local configuration locations.
- ``data``: loading and structural validation of the King County CSV.
- ``preprocess``: fixed row-wise transforms and the training-only fitted encoding.
- ``split``: the grouped 80/20 train/test split and the grouped CV folds.
- ``contract``: the ``model_data`` section schemas (``test_inputs``) and their validation.
- ``export``: building and writing ``model_data`` (``.json`` and ``.js``).
- ``offline_scan``: the static scan for external resource references in the dashboard.
- ``local_config``: reading the untracked packaging configuration (student id).
"""
