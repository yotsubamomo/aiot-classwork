"""Shared fixtures. Synthetic rows only: no test uses the features or price of an official test row
(DA TR-01). Tests on the real CSV read it for structural checks, ids (split) or training rows."""
from datetime import date, timedelta

import numpy as np
import pandas as pd
import pytest

from hw2 import data

ZIPCODES = ("98001", "98004", "98052", "98103", "98178")


def make_synthetic_frame(n_houses: int = 60, n_repeats: int = 8, seed: int = 7) -> pd.DataFrame:
    """A frame with the 21 CSV columns, valid values and some repeat sales of the same house."""
    rng = np.random.default_rng(seed)
    ids = [f"{v:010d}" for v in rng.choice(10**9, size=n_houses, replace=False)]
    ids = ids + list(rng.choice(ids, size=n_repeats, replace=True))
    n = len(ids)
    start = date(2014, 5, 2)
    dates = [(start + timedelta(days=int(d))).strftime("%Y%m%dT000000")
             for d in rng.integers(0, 390, size=n)]
    above = rng.integers(500, 4000, size=n)
    basement = np.where(rng.random(n) < 0.4, rng.integers(100, 1500, size=n), 0)
    built = rng.integers(1900, 2015, size=n)
    renovated = np.where(rng.random(n) < 0.2, np.minimum(built + rng.integers(5, 60, size=n), 2015), 0)
    frame = pd.DataFrame({
        "id": ids,
        "date": dates,
        "price": np.round(rng.lognormal(13.0, 0.5, size=n), 0),
        "bedrooms": rng.integers(1, 7, size=n),
        "bathrooms": rng.choice([1.0, 1.5, 2.0, 2.25, 2.5, 3.0], size=n),
        "sqft_living": above + basement,
        "sqft_lot": rng.integers(1000, 20000, size=n),
        "floors": rng.choice([1.0, 1.5, 2.0, 3.0], size=n),
        "waterfront": (rng.random(n) < 0.05).astype(int),
        "view": rng.integers(0, 5, size=n),
        "condition": rng.integers(1, 6, size=n),
        "grade": rng.integers(4, 13, size=n),
        "sqft_above": above,
        "sqft_basement": basement,
        "yr_built": built,
        "yr_renovated": renovated,
        "zipcode": rng.choice(ZIPCODES, size=n),
        "lat": np.round(rng.uniform(47.15, 47.78, size=n), 4),
        "long": np.round(rng.uniform(-122.52, -121.31, size=n), 3),
        "sqft_living15": rng.integers(600, 4000, size=n),
        "sqft_lot15": rng.integers(1000, 20000, size=n),
    })
    assert tuple(frame.columns) == data.EXPECTED_COLUMNS
    return frame


@pytest.fixture
def synthetic_frame() -> pd.DataFrame:
    return make_synthetic_frame()


@pytest.fixture
def synthetic_csv(tmp_path, synthetic_frame):
    """The synthetic frame written as a CSV; returns (path, frame, sha256)."""
    path = tmp_path / "synthetic.csv"
    synthetic_frame.to_csv(path, index=False)
    return path, synthetic_frame, data.file_sha256(path)


@pytest.fixture(scope="session")
def real_csv_present():
    if not data.DATA_CSV.is_file():
        pytest.skip(f"{data.DATA_CSV} is missing")
    return data.DATA_CSV


@pytest.fixture(scope="session")
def prepared_real(real_csv_present):
    """The real data stage: training rows and test identifiers only."""
    return data.load_and_split()


@pytest.fixture(scope="session")
def fixture_run(tmp_path_factory):
    """One synthetic run through the official code path, test evaluation included (hw2.fixture).

    Synthetic data only (DA TR-01); its model_data lives in a pytest temporary directory."""
    from hw2 import fixture
    return fixture.run_fixture(tmp_path_factory.mktemp("fixture_run"), n_houses=1500,
                               n_repeats=40)


@pytest.fixture(scope="session")
def fixture_model_data(fixture_run, tmp_path_factory):
    """The fixture model_data as written to disk and read back from the .json file."""
    import json
    from hw2 import fixture
    out = tmp_path_factory.mktemp("fixture_md")
    json_path, _ = fixture.write_fixture(fixture_run["model_data"], out)
    return json.loads(json_path.read_text(encoding="utf-8")), json_path
