"""Source features, feature groups, fixed row-wise transforms and the training-only fitted encoding.

Two kinds of preprocessing (Spec rev 5 「資料、計數與前處理」):

- **Fixed row-wise transforms** (no fit, identical for every candidate): ``date`` -> ``sale_days``
  (days since :data:`BASE_DATE`); ``yr_renovated`` -> ``is_renovated`` and
  ``yr_renovated_effective`` (``yr_built`` when never renovated); ``zipcode`` is nominal; the other
  modeled features keep their values; ``sqft_basement`` is not modeled.
- **Fitted preprocessing** (:func:`fit_preprocessor`, fitted on the rows it is given, which callers
  restrict to the current training rows): the ``zipcode`` one-hot categories (training categories,
  the first sorted category is the baseline and is dropped, an unseen category is encoded as the
  baseline) and, only for Ridge/Lasso, the standardization statistics.
"""
import re
from dataclasses import dataclass
from datetime import date, timedelta

import numpy as np
import pandas as pd

from .data import EXPECTED_COLUMNS

SOURCE_FEATURES = tuple(c for c in EXPECTED_COLUMNS if c not in ("id", "price"))      # 19
EXCLUDED_SOURCE_FEATURES = {
    "sqft_basement": ("sqft_living = sqft_above + sqft_basement on every row, so the three columns "
                      "are perfectly collinear; sqft_basement is dropped and the other two stay"),
}
FEATURE_GROUPS = tuple(c for c in SOURCE_FEATURES if c not in EXCLUDED_SOURCE_FEATURES)  # 18
NOMINAL_GROUPS = ("zipcode",)

BASE_DATE = date(2014, 1, 1)
_DATE_TEXT = re.compile(r"^(\d{4})(\d{2})(\d{2})T000000$")

# Encoded columns of each group whose columns do not depend on a fit.
FIXED_GROUP_COLUMNS = {
    "date": ("sale_days",),
    "yr_renovated": ("is_renovated", "yr_renovated_effective"),
}
ZIPCODE_PREFIX = "zipcode_"


class PreprocessError(ValueError):
    """An input value cannot be transformed (for example a malformed date)."""


def parse_sale_date(text: str) -> date:
    """``'20141013T000000'`` -> ``date(2014, 10, 13)``."""
    match = _DATE_TEXT.match(str(text))
    if not match:
        raise PreprocessError(f"date {text!r} is not in the CSV format YYYYMMDDT000000")
    try:
        return date(*map(int, match.groups()))
    except ValueError as exc:
        raise PreprocessError(f"date {text!r} is not a calendar date") from exc


def sale_days(dates) -> np.ndarray:
    """Days from BASE_DATE to each sale date (CSV text), as int64."""
    return np.array([(parse_sale_date(d) - BASE_DATE).days for d in dates], dtype=np.int64)


def days_to_iso(days: float) -> str:
    """A day count back to an ISO date (fractional medians are rounded down)."""
    return (BASE_DATE + timedelta(days=int(np.floor(days)))).isoformat()


def renovation_columns(yr_renovated, yr_built) -> tuple[np.ndarray, np.ndarray]:
    """(``is_renovated``, ``yr_renovated_effective``): flag 1 and the renovation year when
    ``yr_renovated > 0``; otherwise flag 0 and ``yr_built``."""
    renovated = np.asarray(yr_renovated, dtype=np.int64)
    built = np.asarray(yr_built, dtype=np.int64)
    if (renovated < 0).any():
        raise PreprocessError("yr_renovated must be 0 (never renovated) or a year")
    flag = (renovated > 0).astype(np.int64)
    return flag, np.where(flag == 1, renovated, built)


def group_columns(group: str, zipcode_columns=()) -> tuple[str, ...]:
    if group == "zipcode":
        return tuple(zipcode_columns)
    return FIXED_GROUP_COLUMNS.get(group, (group,))


def zipcode_column(category: str) -> str:
    return f"{ZIPCODE_PREFIX}{category}"


@dataclass(frozen=True)
class TransformResult:
    X: np.ndarray                 # float64, columns in `columns` order (no intercept)
    columns: tuple[str, ...]
    unseen_zipcode: np.ndarray    # bool per row: zipcode not among the fitted categories
    @property
    def n_unseen_zipcode(self) -> int:
        return int(self.unseen_zipcode.sum())


@dataclass(frozen=True)
class Preprocessor:
    """Fitted preprocessing for one set of training rows and one set of feature groups."""
    groups: tuple[str, ...]
    zipcode_categories: tuple[str, ...]     # sorted training categories (empty if not modeled)
    zipcode_baseline: str | None            # first sorted category; dropped
    columns: tuple[str, ...]                # encoded columns in canonical order
    group_of_column: dict
    center: tuple[float, ...] | None = None  # standardization (Ridge/Lasso only)
    scale: tuple[float, ...] | None = None

    @property
    def standardized(self) -> bool:
        return self.center is not None

    def transform(self, frame: pd.DataFrame) -> TransformResult:
        """Encode rows that carry the raw CSV columns of `groups`."""
        n = len(frame)
        parts = []
        unseen = np.zeros(n, dtype=bool)
        for group in self.groups:
            if group == "date":
                parts.append(sale_days(frame["date"]).astype(float)[:, None])
            elif group == "yr_renovated":
                flag, effective = renovation_columns(frame["yr_renovated"], frame["yr_built"])
                parts.append(np.column_stack([flag, effective]).astype(float))
            elif group == "zipcode":
                codes = frame["zipcode"].astype(str).to_numpy()
                known = np.isin(codes, np.asarray(self.zipcode_categories, dtype=object))
                unseen = ~known
                dummies = [zc for zc in self.zipcode_categories if zc != self.zipcode_baseline]
                block = np.zeros((n, len(dummies)))
                for j, category in enumerate(dummies):
                    block[:, j] = codes == category
                parts.append(block)
            else:
                parts.append(frame[group].to_numpy(dtype=float)[:, None])
        X = np.hstack(parts) if parts else np.zeros((n, 0))
        if self.standardized:
            X = (X - np.asarray(self.center)) / np.asarray(self.scale)
        return TransformResult(X=X, columns=self.columns, unseen_zipcode=unseen)

    def to_dict(self) -> dict:
        return {
            "groups": list(self.groups),
            "encoded_columns": list(self.columns),
            "group_columns": {g: [c for c in self.columns if self.group_of_column[c] == g]
                              for g in self.groups},
            "zipcode_categories": list(self.zipcode_categories),
            "zipcode_baseline": self.zipcode_baseline,
            "standardized": self.standardized,
        }


def fit_preprocessor(train_rows: pd.DataFrame, groups=FEATURE_GROUPS,
                     standardize: bool = False) -> Preprocessor:
    """Fit on `train_rows` only: zipcode categories, and standardization statistics if asked.

    Standardization (Ridge/Lasso only) centers and scales every encoded column except the zipcode
    one-hot columns with the training mean and population standard deviation; a column that is
    constant on the training rows keeps scale 1.
    """
    groups = tuple(groups)
    unknown = [g for g in groups if g not in FEATURE_GROUPS]
    if unknown:
        raise PreprocessError(f"unknown feature groups {unknown}")
    if len(train_rows) == 0:
        raise PreprocessError("cannot fit on zero training rows")
    groups = tuple(g for g in FEATURE_GROUPS if g in groups)        # canonical order
    categories: tuple[str, ...] = ()
    baseline = None
    if "zipcode" in groups:
        categories = tuple(sorted(train_rows["zipcode"].astype(str).unique()))
        baseline = categories[0]
    zip_cols = tuple(zipcode_column(c) for c in categories if c != baseline)
    columns, owner = [], {}
    for group in groups:
        for column in group_columns(group, zip_cols):
            columns.append(column)
            owner[column] = group
    pre = Preprocessor(groups=groups, zipcode_categories=categories, zipcode_baseline=baseline,
                       columns=tuple(columns), group_of_column=owner)
    if not standardize:
        return pre
    X = pre.transform(train_rows).X
    center = X.mean(axis=0)
    scale = X.std(axis=0)
    is_dummy = np.array([c.startswith(ZIPCODE_PREFIX) for c in columns], dtype=bool)
    center[is_dummy] = 0.0
    scale[is_dummy] = 1.0
    scale[scale == 0.0] = 1.0
    return Preprocessor(groups=groups, zipcode_categories=categories, zipcode_baseline=baseline,
                        columns=tuple(columns), group_of_column=owner,
                        center=tuple(float(v) for v in center),
                        scale=tuple(float(v) for v in scale))


def training_input_ranges(train_rows: pd.DataFrame) -> dict:
    """``model_data.inputs``: per source feature, the training min, max and median (raw values).

    ``date`` is reported as ISO dates (median on the day count); ``zipcode`` as its training
    categories and the most frequent one; ``yr_renovated`` adds the range of renovated rows.
    """
    out = {}
    for feature in SOURCE_FEATURES:
        entry = {"modeled": feature in FEATURE_GROUPS}
        if feature == "date":
            days = sale_days(train_rows["date"])
            entry.update(kind="date", min=days_to_iso(days.min()), max=days_to_iso(days.max()),
                         median=days_to_iso(np.median(days)))
        elif feature == "zipcode":
            codes = train_rows["zipcode"].astype(str)
            counts = codes.value_counts()
            mode = sorted(counts[counts == counts.max()].index)[0]
            entry.update(kind="nominal", categories=sorted(codes.unique()), mode=mode)
        else:
            values = train_rows[feature].to_numpy(dtype=float)
            entry.update(kind="numeric", min=_num(values.min()), max=_num(values.max()),
                         median=_num(np.median(values)))
            if feature == "yr_renovated":
                renovated = values[values > 0]
                entry["note"] = "0 means never renovated (未整修)"
                entry["renovated_min"] = _num(renovated.min()) if renovated.size else None
                entry["renovated_max"] = _num(renovated.max()) if renovated.size else None
        out[feature] = entry
    days = sale_days(train_rows["date"])
    out_dates = {"min": days_to_iso(days.min()), "max": days_to_iso(days.max())}
    return {"features": out, "zipcode_categories": out["zipcode"]["categories"],
            "date_range": out_dates, "n_rows": int(len(train_rows))}


def _num(value: float):
    value = float(value)
    return int(value) if value.is_integer() else value


def preprocess_rules() -> dict:
    """``model_data.preprocess``: everything JS needs to redo the fixed transforms."""
    return {
        "source_features": list(SOURCE_FEATURES),
        "feature_groups": list(FEATURE_GROUPS),
        "excluded_source_features": [{"name": k, "reason": v}
                                     for k, v in EXCLUDED_SOURCE_FEATURES.items()],
        "date": {
            "source_format": "YYYYMMDDT000000 (CSV text)",
            "encoded_column": "sale_days",
            "base_date": BASE_DATE.isoformat(),
            "definition": "sale_days = (sale date - base_date) in whole days",
        },
        "yr_renovated": {
            "encoded_columns": ["is_renovated", "yr_renovated_effective"],
            "definition": ("is_renovated = 1 if yr_renovated > 0 else 0; "
                           "yr_renovated_effective = yr_renovated if yr_renovated > 0 "
                           "else yr_built"),
            "uses_source_features": ["yr_renovated", "yr_built"],
        },
        "zipcode": {
            "kind": "nominal (CSV text)",
            "encoding": ("one-hot over the categories of the training rows of each fit; the first "
                         "sorted category is the baseline and has no column; a category not among "
                         "the fitted ones is encoded as the baseline (all zipcode columns 0)"),
            "column_name": f"{ZIPCODE_PREFIX}<category>",
        },
        "passthrough": [g for g in FEATURE_GROUPS
                        if g not in FIXED_GROUP_COLUMNS and g not in NOMINAL_GROUPS],
        "group_columns_fixed": {g: list(c) for g, c in FIXED_GROUP_COLUMNS.items()},
        "encoded_column_order": ("feature groups in canonical order (CSV column order); within a "
                                 "group: date -> sale_days; yr_renovated -> is_renovated, "
                                 "yr_renovated_effective; zipcode -> zipcode_<category> in sorted "
                                 "category order without the baseline"),
        "standardization": ("only for Ridge/Lasso: every encoded column except the zipcode one-hot "
                            "columns is centered and scaled with the training mean and population "
                            "standard deviation of that fit; OLS subset models use raw scale"),
        "target": {"model_scale": "ln(price)", "report_scale": "USD",
                   "point_prediction": "exp(f(x)), no bias correction (a conditional-median "
                                       "estimate, not the conditional mean)"},
    }
