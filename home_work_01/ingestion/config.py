"""Contract-fixed constants for the ingestion pipeline.

Every value here is load-bearing for grading or for the compatibility derivation
(high-risk categories H-2 and H-3). Changing any of them changes an accepted
semantic and must go through the Design Authority, not the Executor.
"""

from __future__ import annotations

from pathlib import Path

# --- CWA endpoint (Spec R-ING-1, R-ING-3) --------------------------------------
# Only the ingestion fetch stage ever references these. The dataset id is the
# teacher-named identifier the response must echo back.
RESOURCE_ID = "F-D0047-091"
CWA_DATASTORE_URL = (
    "https://opendata.cwa.gov.tw/api/v1/rest/datastore/" + RESOURCE_ID
)
REQUEST_PARAMS = {"format": "JSON"}
REQUEST_TIMEOUT_SECONDS = 30
ENV_KEY_NAME = "CWA_API_KEY"

# --- Region mapping (Spec R-DER-5, project-defined) ----------------------------
# Ordered by the upper contract (REQUIREMENTS A1-3 / DR-8). County names are
# matched verbatim against the response ``LocationName`` (臺, not 台). Insertion
# order is the canonical Region display order (R-SHR-2(b)).
REGION_MEMBERS: dict[str, tuple[str, ...]] = {
    "北部地區": ("基隆市", "臺北市", "新北市", "桃園市", "新竹市", "新竹縣", "苗栗縣"),
    "中部地區": ("臺中市", "彰化縣", "南投縣", "雲林縣", "嘉義市", "嘉義縣"),
    "南部地區": ("臺南市", "高雄市", "屏東縣"),
    "東北部地區": ("宜蘭縣",),
    "東部地區": ("花蓮縣",),
    "東南部地區": ("臺東縣",),
}
# Counties that belong to no Region (澎湖縣, 金門縣, 連江縣) are simply absent above.

REGION_ORDER: tuple[str, ...] = tuple(REGION_MEMBERS.keys())
FORECAST_DAYS_REQUIRED = 7
REGION_COUNT = len(REGION_MEMBERS)  # 6

# --- CWA element and field names (Spec R-DER-1; brief 4.5) ----------------------
ELEMENT_MAX = "最高溫度"
ELEMENT_MIN = "最低溫度"
FIELD_MAX = "MaxTemperature"
FIELD_MIN = "MinTemperature"

# --- Invalid-value handling (Spec R-DER-4, DR-16; brief B10) --------------------
# A county-day value equal to one of these (or otherwise unparseable) makes that
# county-day incomplete, which is an error — never a silent denominator change.
DEFAULT_INVALID_VALUES: frozenset[str] = frozenset(
    {"", "-", "X", "NA", "N/A", "null", "None", "-99", "-999"}
)

# --- Persistence (Spec R-DB-1, R-DB-5) -----------------------------------------
UNIT_DIR = Path(__file__).resolve().parent.parent
DB_PATH = UNIT_DIR / "data.db"

FORECAST_TABLE = "TemperatureForecasts"
# Teacher DDL, verbatim (H-2). Must not gain indexes/constraints or change casing.
FORECAST_TABLE_DDL = (
    "CREATE TABLE TemperatureForecasts (\n"
    "  id INTEGER PRIMARY KEY,\n"
    "  regionName TEXT,\n"
    "  dataDate TEXT,\n"
    "  mint REAL,\n"
    "  maxt REAL\n"
    ");"
)
# Ingestion metadata lives in a separate table so TemperatureForecasts stays
# exactly as the teacher specified (DR-2, R-DB-5).
METADATA_TABLE = "IngestionMetadata"
METADATA_TABLE_DDL = (
    "CREATE TABLE IF NOT EXISTS IngestionMetadata (\n"
    "  id INTEGER PRIMARY KEY CHECK (id = 1),\n"
    "  ingestedAt TEXT NOT NULL,\n"
    "  sourceDatasetId TEXT NOT NULL\n"
    ");"
)
