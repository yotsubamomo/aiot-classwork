"""Shared paths, data preparation and train/test split for the DIC-02 analysis scripts.

CRISP-DM steps 2-3 (data understanding / preparation) live here so every script uses
exactly the same 50 Startups features and the same 80/20 split.
"""
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

UNIT_DIR = Path(__file__).resolve().parent.parent          # week06/
DATA_CSV = UNIT_DIR / 'data' / '50_Startups.csv'
RESULTS_DIR = UNIT_DIR / 'results'
WEB_DATA_JS = UNIT_DIR / 'assets' / 'model_data.js'       # read by index.html

SEED = 42
TEST_SIZE = 0.2
STATES = {'California', 'Florida', 'New York'}            # California is the reference category
FEATURES = ['R&D Spend', 'Administration', 'Marketing Spend', 'State_Florida', 'State_New York']
TARGET = 'Profit'


def load_raw():
    """The CSV with stripped column names and State values."""
    df = pd.read_csv(DATA_CSV)
    df.columns = df.columns.str.strip()
    df['State'] = df['State'].str.strip()
    assert set(df['State'].unique()) <= STATES, 'Unexpected State category'
    return df


def load_data():
    """X with the 5 model features (State one-hot, California = reference) and y = Profit."""
    df = load_raw()
    X = df[['R&D Spend', 'Administration', 'Marketing Spend']].astype(float)
    X['State_Florida'] = (df['State'] == 'Florida').astype(float)
    X['State_New York'] = (df['State'] == 'New York').astype(float)
    return X[FEATURES], df[TARGET].astype(float)


def split(X, y):
    """The 80/20 train/test split used by every DIC-02 script."""
    return train_test_split(X, y, test_size=TEST_SIZE, random_state=SEED)


def results_dir(name):
    """results/<name>/, created on demand."""
    path = RESULTS_DIR / name
    path.mkdir(parents=True, exist_ok=True)
    return path
