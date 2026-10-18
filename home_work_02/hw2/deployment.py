"""The final model, ``predict_price()`` and the pickle demonstration (Deployment).

Spec rev 5 「特徵選擇與模型」: the **final model** is the overall CV winner refitted on the whole
training set; it serves the Deployment prediction function, the pickle demonstration, the
diagnostics and the report's main results. Brief §8 (Q24, Q25): ``predict_price()`` predicts new
samples given in the raw CSV schema; the pickled pipeline is a demonstration only and is **not**
part of the dashboard contract (``model_data``).

- **Training rows only** (H-3; DA TR-01): every function here takes the
  :class:`~hw2.data.PreparedData` of the data stage, which holds the training rows and only the
  identifiers of the test rows (never their features or price), and checks that no test row
  position is among the rows it uses (:func:`training_rows`). Nothing here opens the test gate.
- **Identity** (DA ``decision-20261018-issue62-shared-subset-test-key.md`` D-2): the final model is
  presented as the overall CV winner (its method and k); the other CV winners with the same
  canonical subset are the same fitted model and are listed in :attr:`PricePipeline.shared_with`.
- **Prediction**: the fitted preprocessing of the final model (zipcode categories of the training
  rows; an unseen zipcode is encoded as the baseline) and the OLS fit on ln(price); the point is
  exp(ŷ_log) (a conditional-median estimate, not the conditional mean) and the 95% PI is
  ŷ ± t·√(s²(1 + x₀ᵀ(XᵀX)⁻¹x₀)) on the log scale, then exp (:func:`hw2.ols.usd_interval`).
- **Pickle**: :func:`save_pipeline` / :func:`load_pipeline`. A pickle file runs code when it is
  loaded, so load only the file produced by this repository's notebook.
"""
import pickle
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from . import data, models, ols, preprocess
from .paths import FINAL_MODEL_PICKLE, UNIT_DIR

PIPELINE_VERSION = 1
PICKLE_PROTOCOL = 4
OUTPUT_COLUMNS = ("predicted_price", "pi_lower", "pi_upper", "pi_level", "unseen_zipcode",
                  "out_of_training_range")


class DeploymentError(ValueError):
    """The final model cannot be built, or an input cannot be predicted."""


def training_rows(prepared: data.PreparedData) -> pd.DataFrame:
    """The training rows of the data stage, checked to hold no test row (DA TR-01, H-3)."""
    training = prepared.training
    if "row" not in training or "fold" not in training:
        raise DeploymentError("expected the training rows of hw2.data.load_and_split "
                              "(with their CSV position 'row' and CV 'fold')")
    if np.isin(training["row"].to_numpy(), np.asarray(prepared.test_rows)).any():
        raise DeploymentError("a test row is among the rows given as training rows")
    return training


def is_official_data(prepared: data.PreparedData) -> bool:
    """Whether `prepared` comes from the official data file (only then are results written inside
    the unit). Same rule as the test gate's identification; nothing here touches the gate."""
    from .testgate import is_official
    return is_official(prepared)


def is_inside_unit(path: Path) -> bool:
    path = Path(path).resolve()
    unit = UNIT_DIR.resolve()
    return path == unit or unit in path.parents


@dataclass(frozen=True)
class PricePipeline:
    """The final model as a self-contained prediction pipeline (raw CSV schema in, USD out)."""
    model_key: str                       # the overall CV winner (its own identity; D-2)
    method: str
    k: int
    label: str                           # e.g. "Lasso 路徑排序 · k = 17"
    test_model_key: str                  # the key under which this model was scored once
    shared_with: tuple                   # labels of the other CV winners that are the same model
    groups: tuple                        # canonical subset (feature groups, canonical order)
    uses_source_features: tuple          # raw CSV columns the pipeline needs
    preprocessor: preprocess.Preprocessor
    fit: ols.OLSFit
    input_ranges: dict                   # training min / max / median of each used feature
    data_sha256: str
    n_train: int
    version: int = PIPELINE_VERSION

    @property
    def model(self) -> models.OLSModel:
        return models.OLSModel(groups=self.groups, preprocessor=self.preprocessor, fit=self.fit)

    def fit_dict(self) -> dict:
        """The model's ``fit`` in the ``model_data`` layout (log scale; coefficients raw scale)."""
        return self.model.to_fit_dict()

    def predict_price(self, rows) -> pd.DataFrame:
        """Point prediction and 95% PI (USD) for rows in the raw CSV schema; see
        :func:`predict_price`."""
        frame = _as_frame(rows, self.uses_source_features)
        point, lower, upper, _ = self.model.predict_usd(frame)
        unseen = (self.preprocessor.transform(frame).unseen_zipcode
                  if "zipcode" in self.groups else np.zeros(len(frame), dtype=bool))
        out = pd.DataFrame({"predicted_price": point, "pi_lower": lower, "pi_upper": upper,
                            "pi_level": ols.PI_LEVEL, "unseen_zipcode": unseen,
                            "out_of_training_range": self._out_of_range(frame)},
                           index=frame.index)
        return out[list(OUTPUT_COLUMNS)]

    def _out_of_range(self, frame: pd.DataFrame) -> list:
        """Per row, the used features outside the training range (still predicted: extrapolation)."""
        flags = [[] for _ in range(len(frame))]
        for name in self.uses_source_features:
            info = self.input_ranges.get(name, {})
            if info.get("kind") == "nominal":
                continue
            if info.get("kind") == "date":
                days = preprocess.sale_days(frame["date"])
                lo = preprocess.sale_days([_csv_date(info["min"])])[0]
                hi = preprocess.sale_days([_csv_date(info["max"])])[0]
                outside = (days < lo) | (days > hi)
            elif name == "yr_renovated":
                values = frame[name].to_numpy(dtype=float)
                lo, hi = info.get("renovated_min"), info.get("renovated_max")
                if lo is None or hi is None:
                    outside = values > 0             # no renovated training row at all
                else:
                    outside = (values > 0) & ((values < lo) | (values > hi))
            else:
                values = frame[name].to_numpy(dtype=float)
                outside = (values < info["min"]) | (values > info["max"])
            for i in np.flatnonzero(outside):
                flags[i].append(name)
        return [", ".join(f) for f in flags]


def _csv_date(value) -> str:
    """CSV date text ``YYYYMMDDT000000`` from CSV text or ISO ``YYYY-MM-DD``."""
    text = str(value)
    if len(text) == 10 and text[4] == "-" and text[7] == "-":
        return text.replace("-", "") + "T000000"
    return text


def _as_frame(rows, required) -> pd.DataFrame:
    """A DataFrame of raw CSV-schema rows (a DataFrame, one dict, or a list of dicts)."""
    if isinstance(rows, pd.DataFrame):
        frame = rows.copy()
    elif isinstance(rows, dict):
        frame = pd.DataFrame([rows])
    else:
        frame = pd.DataFrame(list(rows))
    missing = [c for c in required if c not in frame.columns]
    if missing:
        raise DeploymentError(f"missing raw input columns {missing} (raw CSV schema; the model "
                              f"uses {list(required)})")
    if len(frame) == 0:
        raise DeploymentError("no rows to predict")
    used = frame[list(required)]
    if used.isna().any().any():
        bad = used.columns[used.isna().any()].tolist()
        raise DeploymentError(f"missing values in {bad}")
    if "date" in required:
        frame["date"] = [_csv_date(v) for v in frame["date"]]
    if "zipcode" in required:
        frame["zipcode"] = frame["zipcode"].astype(str)
    return frame


def predict_price(rows, pipeline: PricePipeline) -> pd.DataFrame:
    """Predict prices for rows in the raw CSV schema with the final model.

    `rows`: a DataFrame, one dict or a list of dicts holding at least the raw source features the
    model uses (``pipeline.uses_source_features``; other columns such as ``id`` or ``price`` are
    ignored). ``date`` is the CSV text ``YYYYMMDDT000000`` or ISO ``YYYY-MM-DD``; ``yr_renovated``
    is 0 for never renovated; ``zipcode`` is the 5-digit text. Returns, per row,
    ``predicted_price`` (exp of the log prediction; a conditional-median estimate),
    ``pi_lower``/``pi_upper`` (95% PI in USD), ``pi_level``, ``unseen_zipcode`` (encoded as the
    baseline category) and ``out_of_training_range`` (the features outside the training range;
    the row is still predicted — extrapolation)."""
    return pipeline.predict_price(rows)


def final_model(prepared: data.PreparedData, winners: dict, allin: models.Candidate,
                path_candidates: dict) -> PricePipeline:
    """The overall CV winner refitted on the whole training set, as a :class:`PricePipeline`.

    The refit uses the training rows only and must reproduce the candidate's canonical fit (the
    same rows and groups), which is checked bit for bit."""
    training = training_rows(prepared)
    overall = (winners or {}).get("overall")
    if not overall or not winners.get("complete"):
        raise DeploymentError("the overall CV winner is not determined (complete winners needed)")
    by_key = {allin.key: allin}
    by_key.update({c.key: c for cands in path_candidates.values() for c in cands})
    key = overall["model_key"]
    candidate = by_key[key]
    if not candidate.valid or candidate.model is None:
        raise DeploymentError(f"the overall CV winner {key} has no valid canonical fit")
    model = models.fit_model(training, candidate.canonical_groups)
    reference = candidate.model.fit
    if not (np.array_equal(model.fit.coef, reference.coef)
            and np.array_equal(model.fit.xtx_inv, reference.xtx_inv)
            and model.fit.s2 == reference.s2 and model.fit.column_names == reference.column_names):
        raise DeploymentError(f"the refit of {key} differs from its canonical fit")
    test_key = overall.get("test_model_key", key)
    shared = []
    allin_w = winners.get("allin") or {}
    if allin_w.get("test_model_key", allin.key) == test_key and allin.key != key:
        shared.append(models.METHOD_LABELS[models.ALLIN])
    for method, w in winners.get("method_winners", {}).items():
        if w.get("test_model_key", w["model_key"]) == test_key and w["model_key"] != key:
            shared.append(f"{models.METHOD_LABELS[method]} · k = {w['k']}")
    features = models.source_features_of(model.groups)
    ranges = preprocess.training_input_ranges(training)["features"]
    return PricePipeline(
        model_key=key, method=candidate.method, k=candidate.k,
        label=f"{models.METHOD_LABELS[candidate.method]} · k = {candidate.k}",
        test_model_key=test_key, shared_with=tuple(shared), groups=tuple(model.groups),
        uses_source_features=tuple(features), preprocessor=model.preprocessor, fit=model.fit,
        input_ranges={f: dict(ranges[f]) for f in features}, data_sha256=prepared.sha256,
        n_train=int(len(training)))


def save_pipeline(pipeline: PricePipeline, path: Path = FINAL_MODEL_PICKLE,
                  official: bool = False) -> Path:
    """Pickle the pipeline. Only the official run writes inside the unit directory (a fixture or
    test pipeline never reaches the tracked result paths)."""
    path = Path(path)
    if not official and is_inside_unit(path):
        raise DeploymentError("a non-official pipeline must not be written inside the unit")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(pickle.dumps(pipeline, protocol=PICKLE_PROTOCOL))
    return path


def load_pipeline(path: Path = FINAL_MODEL_PICKLE) -> PricePipeline:
    """Load a pickled :class:`PricePipeline` (only files produced by this repository)."""
    obj = pickle.loads(Path(path).read_bytes())
    if not isinstance(obj, PricePipeline) or obj.version != PIPELINE_VERSION:
        raise DeploymentError(f"{path} does not hold a PricePipeline v{PIPELINE_VERSION}")
    return obj
