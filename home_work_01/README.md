# HW10 — Taiwan Weather Forecast (`home_work_01`)

A one-week temperature forecast for six Taiwan Regions, taken from CWA open data,
persisted to SQLite, and (in later tickets) shown in a web app.

> **Scope of this README section.** This document currently covers the **ingestion**
> stage (Issue #18): fetch → derive → persist. The Streamlit grading app, the
> deployed Flask dashboard, the Taiwan map, automated CI and Vercel deployment are
> added by later tickets and will extend this README.

## Data source and labeling (please read)

This project's data does **not** come straight from a CWA six-region product.
The values are **project-derived compatibility values**; the numbers you see are
computed by this project, not published by CWA.

- **Originally assigned dataset:** CWA `F-A0010-001` (一週農業氣象預報), the six-region
  weekly forecast named by the homework poster. **CWA delisted it on 2026-07-01**
  (a query with a valid key now returns HTTP 404). This is an external constraint,
  not a project choice; the assignment is kept on record as the original requirement.
- **Compatibility replacement:** CWA `F-D0047-091`
  (臺灣各縣市鄉鎮未來1週逐12小時天氣預報), a **county-level** dataset. Using it is a
  **project compatibility decision**, not a teacher instruction.
- **Forecast Day (W1 window):** each 12-hour period is grouped by the local date `D`
  of its `StartTime`. A **Forecast Day D** = the `D 06:00–18:00` period plus the
  `D 18:00–(D+1) 06:00` period. It is a **compatibility window, not a calendar day**,
  and a Forecast Day is *complete* only when both periods are present. A leading
  `00:00–06:00` partial period (present when the response is captured after midnight)
  is not part of any Forecast Day and is ignored.
- **Region mapping is project-defined**, not an authoritative CWA grouping:
  | Region | Member counties |
  | --- | --- |
  | 北部地區 | 基隆市, 臺北市, 新北市, 桃園市, 新竹市, 新竹縣, 苗栗縣 |
  | 中部地區 | 臺中市, 彰化縣, 南投縣, 雲林縣, 嘉義市, 嘉義縣 |
  | 南部地區 | 臺南市, 高雄市, 屏東縣 |
  | 東北部地區 | 宜蘭縣 |
  | 東部地區 | 花蓮縣 |
  | 東南部地區 | 臺東縣 |
  澎湖縣, 金門縣, 連江縣 belong to no Region. County names are matched verbatim
  against the response `LocationName` (臺, never 台).
- **Region MinT / MaxT are `PROJECT-DERIVED COMPATIBILITY VALUES`.** For each Region
  and Forecast Day: county-day MinT = the minimum of the day's period minima,
  county-day MaxT = the maximum of the day's period maxima, then the **arithmetic
  mean across the Region's member counties**, rounded **half-up to one decimal**.
  They are **never** a CWA-issued six-region forecast, and the mapping above is
  **never** an authoritative CWA regional division.

## Requirements

- **Python 3.12** (the deployment target does not offer 3.11). Verify with
  `python --version`.
- Dependencies pinned in [`requirements.txt`](requirements.txt): `requests`, `pytest`.
  `folium` / `streamlit-folium` are intentionally excluded.

## Setup

```bash
cd home_work_01

# Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # macOS / Linux

pip install -r requirements.txt
```

(This repository was developed with [`uv`](https://docs.astral.sh/uv/):
`uv venv --python 3.12 .venv` then `uv pip install -r requirements.txt`.)

## Get a CWA key and create `.env`

1. Register at <https://opendata.cwa.gov.tw/> and obtain your own API key.
   You **must** use your own key (poster note 1); never commit it.
2. Copy the template and paste your key:

   ```bash
   cp .env.example .env      # copy .env.example to .env
   # then edit .env and set CWA_API_KEY=<your key>
   ```

   `.env` is git-ignored (root `.gitignore`); only `.env.example` (variable name
   only) is committed. The key is read solely by the ingestion fetch stage and is
   never printed, logged, or written to any tracked file.

## Run ingestion

**Online (fetch once, then derive and persist):**

```bash
python -m ingestion
```

This fetches `F-D0047-091` with your key, saves the complete, indented raw JSON to
[`data/raw/F-D0047-091.json`](data/raw/F-D0047-091.json), prints a fetch summary
(county count, weather-element names, period count) and the 42-row derived
snapshot preview, then writes the snapshot into [`data.db`](data.db).

**Offline (rebuild `data.db` from the saved JSON — no network, no key):**

```bash
python -m ingestion --from-json data/raw/F-D0047-091.json
```

Useful CLI options: `--from-json PATH` (offline source), `--raw-out PATH`
(where the online run saves the raw JSON), `--env PATH` (the `.env`), `--db PATH`
(the SQLite file to write).

Any validation failure (missing member county, missing half-day, unparseable
value, fewer than seven / non-consecutive complete days, or an HTTP/JSON failure)
aborts with a message naming the problem, a **non-zero exit code**, and **no
database write** — the previous `data.db` snapshot is left unchanged.

### Observation artifacts (the "observe JSON / observe data" grading items)

- **Raw JSON:** [`data/raw/F-D0047-091.json`](data/raw/F-D0047-091.json) — the
  complete response, indented (`json.dumps(..., indent=2, ensure_ascii=False)`),
  with no key. Captured **2026-09-24**.
- **Response structure of `F-D0047-091`:**

  ```text
  success: "true"
  result.resource_id: "F-D0047-091"
  records.Locations[0].Location[]            (22 counties)
    .LocationName                            (縣市 name)
    .WeatherElement[]  where ElementName ∈ { 最高溫度, 最低溫度, ... }
      .Time[]                                (15 periods per temperature element)
        .StartTime / .EndTime                (ISO 8601, +08:00)
        .ElementValue[0].MaxTemperature | .MinTemperature   (string, e.g. "26")
  ```

- **Derived snapshot preview:** printed to the terminal by every ingestion run
  (42 rows of `regionName / dataDate / mint / maxt`, plus the Region count and
  date range).

## Verify the database

```sql
-- 1. list all Region names  -> six rows
SELECT DISTINCT regionName FROM TemperatureForecasts;

-- 2. one Region's week       -> seven rows, dataDate as YYYY-MM-DD
SELECT * FROM TemperatureForecasts WHERE regionName = '中部地區';
```

The table is created with the teacher DDL verbatim:

```sql
CREATE TABLE TemperatureForecasts (
  id INTEGER PRIMARY KEY,
  regionName TEXT,
  dataDate TEXT,
  mint REAL,
  maxt REAL
);
```

`TemperatureForecasts` holds either 0 rows or exactly **42** (six Regions × seven
Forecast Days); it never contains a partial write. Re-running ingestion **replaces
the whole snapshot in a single transaction**, so it never duplicates rows. The
ingestion time (ISO 8601, `+08:00`) and source dataset id are stored in a separate
`IngestionMetadata` table, so `TemperatureForecasts` itself never changes shape.

## Run the tests (offline)

```bash
pytest
```

The suite is fully offline: it never calls the network and never reads `.env`
(HTTP failures are mocked). It covers the derivation (positive values hand-computed
from county numbers, plus the five failure cases), the DDL and verification SQL,
idempotent snapshot replacement, the ingestion metadata, and a secret scan of the
committed JSON artifacts. The test fixture
[`tests/fixtures/F-D0047-091_sample.json`](tests/fixtures/F-D0047-091_sample.json)
is a **real** `F-D0047-091` response captured **2026-09-24**, **reduced** to the two
temperature weather elements per county (structure preserved); the negative cases
are derived from it.

## Correspondence to the poster `HW10_Weather/` structure

The poster suggests a flat set of scripts; this project keeps the teacher-named
files (`app.py`, `data.db`, `requirements.txt`, `README.md`) and groups the three
ingestion stages into a clearly named `ingestion` package.

| Poster `HW10_Weather/` | This project |
| --- | --- |
| `fetch_weather.py` (取得 CWA API 資料) | [`ingestion/fetch.py`](ingestion/fetch.py) — fetch stage |
| `parse_weather.py` (分析 JSON，提取氣溫) | [`ingestion/derive.py`](ingestion/derive.py) — parse/derive stage |
| `database.py` (儲存到 SQLite) | [`ingestion/persist.py`](ingestion/persist.py) — database stage |
| (runner) | [`ingestion/pipeline.py`](ingestion/pipeline.py) — `python -m ingestion` |
| `data.db` | [`data.db`](data.db) |
| `requirements.txt` | [`requirements.txt`](requirements.txt) |
| `README.md` | this file |
| `app.py` (Streamlit) | later ticket |
| `weather_data.csv` (optional) | not used |
