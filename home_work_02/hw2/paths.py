"""Unit paths, the seed, and the untracked local locations (home_work_02/)."""
from pathlib import Path

UNIT_DIR = Path(__file__).resolve().parent.parent          # home_work_02/

DATA_CSV = UNIT_DIR / "data" / "kc_house_data.csv"

RESULTS_DIR = UNIT_DIR / "results"
ASSETS_DIR = UNIT_DIR / "assets"
DASHBOARD_HTML = UNIT_DIR / "index.html"

# The official model_data contract: one JSON object, and the same object wrapped as a JS global
# so that index.html can load it from file:// (browsers block fetch() of local JSON there).
MODEL_DATA_JSON = RESULTS_DIR / "model_data.json"
MODEL_DATA_JS = ASSETS_DIR / "model_data.js"
MODEL_DATA_JS_GLOBAL = "MODEL_DATA"

# Per-row split record (identifiers and fold numbers only; no features, no price).
SPLIT_ASSIGNMENT_CSV = RESULTS_DIR / "split" / "split_assignment.csv"

# Diagnostics and model explanation of the final model (training rows only; DA TK-2): figures (PNG)
# and tables (CSV). The Deployment demonstration pickle is not part of the dashboard contract.
FIGURES_DIR = RESULTS_DIR / "figures"
TABLES_DIR = RESULTS_DIR / "tables"
DEPLOYMENT_DIR = RESULTS_DIR / "deployment"
FINAL_MODEL_PICKLE = DEPLOYMENT_DIR / "final_model.pkl"

# Untracked local locations (all listed in home_work_02/.gitignore; BR-03, H-1):
LOCAL_DIR = UNIT_DIR / ".local"
# Packaging configuration holding the real student id: {"student_id": "<學號>"}.
PACKAGING_CONFIG = LOCAL_DIR / "packaging.json"
# Acceptor materials (ChatGPT conversation PDF, NotebookLM output and source list).
ACCEPTOR_MATERIALS_DIR = UNIT_DIR / "acceptor_materials"
# Packaging output (<學號>_hw2.ipynb, <學號>_hw2.zip, report PDF build).
DIST_DIR = UNIT_DIR / "dist"

# One fixed seed for the whole analysis. The split and the folds draw from separate streams
# derived from it (numpy SeedSequence entropy [SEED, 0] and [SEED, 1]).
SEED = 42
TEST_FRACTION = 0.2
N_FOLDS = 5
