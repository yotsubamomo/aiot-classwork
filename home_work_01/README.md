# HW10 — Taiwan Weather Forecast (`home_work_01`)

A one-week temperature forecast for six Taiwan Regions, **derived from CWA
county-level open data** (not a CWA-published six-region product — see
[Data source and labeling](#data-source-and-labeling-please-read)), persisted to
SQLite, and shown in a web app.

> **Scope of this README.** This document covers the whole project end to end: the
> **ingestion** stage (fetch → derive → persist), the **Streamlit Grading App**
> (`app.py` + the shared query module `weather_query.py`), the **Flask dashboard**
> (`server.py`, the `/api/` JSON API and the static frontend under `static/`) with its
> ENHANCED **`Select Date` control and interactive Taiwan Map** (see
> [Taiwan Map and `Select Date`](#taiwan-map-and-select-date-dashboard-enhanced)), the
> **automated CI** ([Continuous integration](#continuous-integration-github-actions))
> and the **Vercel deployment** with its smoke check
> ([Deploy to Vercel](#deploy-to-vercel-public-url--smoke-check)).

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
- Dependencies pinned in [`requirements.txt`](requirements.txt): `requests`,
  `pytest`, `streamlit`, `flask`. The interactive Taiwan Map uses a **vendored
  JavaScript** library (Leaflet, under [`static/vendor/`](static/vendor/)), which is
  **not** a Python dependency; `folium` / `streamlit-folium` are intentionally excluded
  so the MVM apps do not depend on them (Spec R-ENV-1, R-GA-9).

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

This fetches `F-D0047-091` with your key, records the **acquisition time** (the
moment the fetch succeeded), saves the complete, indented raw JSON to
[`data/raw/F-D0047-091.json`](data/raw/F-D0047-091.json) with a **provenance
sidecar** next to it (see below), prints a fetch summary (county count,
weather-element names, period count) and the 42-row derived snapshot preview, then
writes the snapshot into [`data.db`](data.db). The acquisition time is stored as
`IngestionMetadata.ingestedAt` and is what the app shows as "last updated".

**Offline (rebuild `data.db` from the saved JSON — no network, no key):**

```bash
python -m ingestion --from-json data/raw/F-D0047-091.json
```

The offline rebuild reads the acquisition time **from the provenance sidecar** (or
from an explicit `--acquired-at` value); it never reads the clock, so rebuilding an
old response does **not** make its "last updated" time look newer. Both the
committed raw JSON and its provenance sidecar are checked in, so a clean checkout
reproduces the committed `data.db` (same `ingestedAt`). If neither a sidecar nor
`--acquired-at` is available, the rebuild **fails closed** (clear message, non-zero
exit, no database write).

Useful CLI options: `--from-json PATH` (offline source), `--raw-out PATH`
(where the online run saves the raw JSON), `--env PATH` (the `.env`), `--db PATH`
(the SQLite file to write), `--acquired-at ISO8601` (offline: acquisition time to
record, overriding the sidecar).

### Acquisition-time provenance sidecar

Because the F-D0047-091 response carries no acquisition or publish time, the online
run writes a small key-free JSON sidecar next to the raw JSON:

- Location: [`data/raw/F-D0047-091.meta.json`](data/raw/F-D0047-091.meta.json)
  (`<raw>.json` → `<raw>.meta.json`), inside the unit directory.
- Content: `sourceDatasetId`, `acquiredAt` (ISO 8601 `+08:00`), and the raw JSON
  filename. It never contains the key or any request header, and it does not modify
  the raw JSON (which stays byte-complete).
- `IngestionMetadata.ingestedAt` means this **acquisition time** — the time the data
  was fetched from CWA — not the time the snapshot rows were (re)built.

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

## Run the Grading App (`streamlit run app.py`)

From the unit directory, with the virtual environment active and `data.db`
present (run ingestion first):

```bash
cd home_work_01
streamlit run app.py
```

The page opens `Taiwan Weather Forecast` with a `Select Region` dropdown (the six
Regions in the fixed order: 北部地區, 中部地區, 南部地區, 東北部地區, 東部地區,
東南部地區). Choosing a Region shows a `MaxT` / `MinT` line chart over the seven
Forecast Days and a `Date` / `MinT` / `MaxT` table (seven rows, ascending, equal
to `data.db`), together with the snapshot's acquisition time — when the data was
fetched from CWA (see the provenance sidecar above), not a render time. If
`data.db` is missing or empty the page shows a clear message telling you to run
ingestion; an incomplete snapshot shows a warning.

All data is read through the shared query module
[`weather_query.py`](weather_query.py), the single place that holds the SQL and
the forecast business logic; `app.py` contains no SQL and never calls CWA.

### About the Grading App (Streamlit) vs. the deployed Dashboard

`app.py` is the genuine Streamlit application named by the homework and is the
**required grading artefact** for the interactive-web-app item — it carries the
complete graded (MVM) behaviour and is run locally with `streamlit run app.py`. It
is **not** the deployed runtime: the public deployment target (Vercel) cannot run
a Streamlit server, so the same `data.db` and the same query semantics are served
by the Flask + static dashboard below (deployed publicly to Vercel — see
[Deploy to Vercel](#deploy-to-vercel-public-url--smoke-check)). Streamlit being
local rather than deployed is a compatibility accommodation forced by that hosting
constraint, **not** a sign that Streamlit was outside the assignment. The Grading
App deliberately has **no** Taiwan Map and **no** `Select Date`; those are
enhanced, dashboard-only features.

## Run the dashboard (Flask) locally

The deployed presentation layer is a Flask app that serves both the dashboard
**page** and a JSON **API**, structured to deploy to Vercel as a single Python
function (see [Deploy to Vercel](#deploy-to-vercel-public-url--smoke-check)). Run
it locally from the unit directory with `data.db` present:

```bash
cd home_work_01
python server.py            # serves http://127.0.0.1:5000/
# or, equivalently:
flask --app server run
```

Open <http://127.0.0.1:5000/>. The page is the same MVM experience as the
Grading App — `Taiwan Weather Forecast`, a `Select Region` control over the six
Regions in the fixed order, and, for the selected Region, a `MaxT` / `MinT`
seven-day line chart and a `Date` / `MinT` / `MaxT` table equal to `data.db`,
plus the snapshot's acquisition time. It is a static HTML/CSS/JS frontend (no
build step) whose chart is drawn with plain inline SVG (no chart library, no key).
Add `?region=<name>` to deep-link a Region (for example `?region=中部地區`). If the
data is unavailable the page shows a clear message instead of a blank page.

All data comes from this application's own JSON API under the `/api/` prefix; the
browser never calls CWA and holds no key. The backend reads `data.db` only through
the shared module [`weather_query.py`](weather_query.py) and imports no HTTP client.

### `/api/` endpoints

| Method & path | Returns | On error |
| --- | --- | --- |
| `GET /` | The dashboard HTML page (contains `Taiwan Weather Forecast`). | — |
| `GET /api/health` | `200` JSON `{ status: "ok", region_count: 6, forecast_day_count: 7, ingestion_time }` when the snapshot is a complete six-Region × seven-day snapshot. | `503` JSON `{ status: "unavailable", reason, error }` when the snapshot is missing / empty / incomplete. |
| `GET /api/regions` | `200` JSON `{ regions: [...] }` — the six Region names in the fixed order. | `503` (snapshot unavailable). |
| `GET /api/regions/<region>/series` | `200` JSON `{ region, series: [{ dataDate, mint, maxt }, ...] }` — seven rows, ascending, equal to `data.db`. | `404` JSON `{ error }` for an unknown Region; `503` when unavailable. |
| `GET /api/days` | `200` JSON `{ days: [...] }` — the seven Forecast Day dates, ascending. | `503` (snapshot unavailable). |
| `GET /api/days/<date>` | `200` JSON `{ date, values: [{ regionName, mint, maxt, derivedMapTemperature, colourBand }, ...] }` — the six Regions for that day, incl. the Derived Map Temperature. | `404` JSON `{ error }` for an unknown date; `503` when unavailable. |

Every error response is JSON carrying a human-readable `error` message. The Vercel
structure lives beside the code — `server.py` (the app), `api/index.py` (the
serverless entry that imports `app`), `vercel.json` (routes every request to that
one function) and `requirements.txt`; `data.db` is packaged next to the code and
opened read-only, and no environment variable or secret is needed at runtime.

### Taiwan Map and `Select Date` (dashboard, ENHANCED)

The dashboard integrates a **`Select Date`** control and an interactive **Taiwan
Map** on the same page (the "Taiwan Weather Dashboard"), alongside the Region
chart/table/summary. These are **enhanced, dashboard-only** features — the
Streamlit Grading App deliberately has neither.

- **`Select Date`** lists the snapshot's seven Forecast Days in ascending order and
  defaults to the first day. It lives **inside the Taiwan Map's floating info panel**
  (top-left on wide screens; a row above the map on phones). Changing it recolours the
  map markers and updates the panel to that day's values **without resetting the map
  view** (data from `GET /api/days` and `GET /api/days/<date>`). The Region
  chart/table's own **`Select Region`** control stays in the controls card below the
  map — the two presentations remain on one page.
- **Taiwan Map** is drawn with **Leaflet** (vendored locally under
  [`static/vendor/`](static/vendor/), pinned to version 1.9.4) on a **vendored vector
  basemap** loaded from [`static/data/basemap.js`](static/data/basemap.js) as a
  same-origin `<script>` global (`window.TAIWAN_BASEMAP`) — **not** fetched. There is
  **no external tile server**, so the map makes **no external request at runtime** and
  needs **no key, account or payment**; the browser only ever calls this app's own
  same-origin `/static/` and `/api/` URLs. The map area is dark in both light and dark
  colour schemes.
  - **Basemap sources and licences** (acquired 2026-09-24 at build time — both free,
    no account, no payment; the geometry is simplified and carries no attributes, so it
    is a backdrop only, not a data layer):
    - Surrounding coastlines: **Natural Earth** 1:50m Admin 0 Countries
      (`ne_50m_admin_0_countries`), **public domain**. Filtered to CHN/TWN/PHL/JPN/VNM/
      HKG/MAC, bbox-clipped and Visvalingam-simplified.
    - Taiwan county polygons: **內政部 (Ministry of the Interior) 直轄市、縣市界線
      (TWD97經緯度)** open data, version 1140318 (2025-03-18), under the **Open
      Government Data License (政府資料開放授權條款)** — attribution shown in the map's
      attribution control. bbox-clipped and Visvalingam-simplified.
  - Total vendored basemap ≤ 300 KB.
- The map shows **six Region markers** as temperature **pills** at **project-defined
  representative points** (their latitude/longitude are a project layout choice — a
  single point standing in for each Region, within that Region's member counties —
  **not** a CWA-published location or boundary). The northern and north-eastern points
  are `北部地區 [25.12, 121.38]` and `東北部地區 [24.66, 121.80]` (nudged apart from
  #24's `[25.03, 121.50]` / `[24.72, 121.74]` so the two pills never overlap at the
  375px view); the other four are unchanged. Each pill's **text** is the selected day's
  Derived Map Temperature (one decimal) and its **colour** is that day's band; a
  hover tooltip and the panel's selected-Region block show the Region, `Date`, `Min`,
  `Max` and the derived average.
- **Derived Map Temperature** is a **derived value**: `(MinT + MaxT) / 2`, rounded
  half-up to one decimal place. It is **not** an observed daily mean. The colour
  bands (by the displayed one-decimal value) are `< 20` blue, `20 – < 25` green,
  `25 – < 30` yellow and `≥ 30` red, and the legend states the "derived, not
  observed" caveat. The value and its band are computed **once** in the shared
  module ([`weather_query.py`](weather_query.py)) and returned by
  `GET /api/days/<date>`; the frontend colours directly by that band and re-derives
  nothing.

## Deploy to Vercel (public URL & smoke check)

The dashboard deploys to Vercel as a **single Python serverless function** that
serves both the page and the `/api/` JSON. Everything the deployment needs lives
inside this unit directory: `vercel.json` (one `@vercel/python` build of
`api/index.py`, every route sent to it, `data.db` packaged with `includeFiles`),
`requirements.txt`, `data.db` (packaged and opened read-only), and
[`.python-version`](.python-version) which **pins Python `3.12`** so the local
environment, CI and the Vercel runtime all use the same interpreter. The running
function needs **no environment variable and no secret** — the CWA key is never
part of the deployment.

**Acceptor-only setup (one-time).** Creating the Vercel project, linking it to
`yotsubamomo/aiot-classwork`, setting the project **Root Directory = `home_work_01`**,
and making the deployment **publicly reachable without login** (pointing the
production branch at the topic branch, or turning off Deployment Protection for
previews) are performed by the repository owner in the Vercel dashboard — they
touch billing/account settings outside an agent's authority. No repository files
change for this.

**Production vs preview.** Pushing the topic branch makes Vercel build a
**preview** automatically; the branch-preview alias is a public, no-login URL that
serves the branch's most recent **successful** build (Vercel moves the alias when a
build succeeds; a failed build leaves it on the previous commit), so it verifies
the audited commit once that commit's build is ready — confirm the served
deployment id matches the commit rather than assuming it.
The **production** URL updates only when the branch is merged into `main` — that
merge is a release action, so re-running the smoke check against production after
merge is release evidence, not a completion condition for the deployment work.

| | URL |
| --- | --- |
| Public preview (audited commit; no login) | `https://aiot-hw01-weather-git-homework01-hw10-im-8efc12-nchu-aiot-class.vercel.app` |
| Production (updates on merge to `main`) | `https://aiot-hw01-weather.vercel.app` |

**Smoke check.** [`smoke.py`](smoke.py) verifies the public deployment: `GET /`
returns 200 containing `Taiwan Weather Forecast` and `GET /api/health` returns 200
with `status: "ok"`, retrying for up to 90 s of warm-up and exiting non-zero on
failure. Run it from this directory with the URL as an argument, or via the
`HW01_DEPLOY_URL` environment variable (the repository variable the smoke workflow
injects):

```bash
cd home_work_01
python smoke.py https://aiot-hw01-weather-git-homework01-hw10-im-8efc12-nchu-aiot-class.vercel.app
# or, reading the URL from the environment / repository variable:
HW01_DEPLOY_URL=https://<public-host> python smoke.py
```

It is standard-library only (no dependency to install) and is reused unchanged by
the `workflow_dispatch` smoke workflow (Issue #22).

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
acquisition time (ISO 8601, `+08:00`; see the provenance sidecar above) and source
dataset id are stored in a separate `IngestionMetadata` table, so
`TemperatureForecasts` itself never changes shape.

## Run the tests (offline)

```bash
pytest
```

The suite is fully offline: it never calls the network and never reads `.env`
(HTTP failures are mocked). It covers the derivation (positive values hand-computed
from county numbers, plus the five failure cases), the DDL and verification SQL,
idempotent snapshot replacement, the ingestion metadata, and a secret scan of the
committed JSON artifacts. For the Grading App (Issue #19) it also covers the shared
query module (the six read-side semantics, read-only / source-relative /
overridable database opening, and the Derived Map Temperature colour bands) and the
Streamlit app via `AppTest` (title, `Select Region` options and order, the chart
and table for a selected Region, the error/empty/incomplete states, and the
displayed ingestion time). For the Flask dashboard (Issue #20) it covers the
backend via the Flask test client (`GET /` with the page text, `/api/health` 200
and 503, and every data endpoint's normal / 404 / 503 responses) and the INV-2
comparison that the API's series equals the shared module for all six Regions.
Static checks confirm the Streamlit app and the Flask backend hold no SQL, import
no HTTP client (dotted forms such as `from urllib import request` included), and
carry no CWA URL / key, and that the frontend's data requests target only `/api/`;
`app.py` also carries no map / `Select Date` / folium. (The browser-level check
that the dashboard shows a visible message when `/series` fails on first load,
[`tests/check_series_error_visible.py`](tests/check_series_error_visible.py), needs
a real Chrome and so runs separately from the offline `pytest` suite.) The test fixture
[`tests/fixtures/F-D0047-091_sample.json`](tests/fixtures/F-D0047-091_sample.json)
is a **real** `F-D0047-091` response captured **2026-09-24**, **reduced** to the two
temperature weather elements per county (structure preserved); the negative cases
are derived from it.

## Continuous integration (GitHub Actions)

Two workflows live in the repository-root `.github/workflows/` directory — the one
place outside this unit that holds `home_work_01` files, under the acceptor's
scoped RB-5 authorization (Outcome Contract §8.2). Each serves **only this unit**.

**CI — [`home_work_01-ci.yml`](../.github/workflows/home_work_01-ci.yml).** Runs on
every **push**, and on pull requests, but only when the change touches
`home_work_01/**` or the CI workflow file itself: the `paths` filter means a change
to root files, another unit, or the smoke workflow does **not** run it. The job
sets up **Python 3.12**, installs [`requirements.txt`](requirements.txt), runs the
full offline `pytest` suite, and then runs the credential mechanical checks
(`python -m tools.credential_scan`): `git ls-files` tracks no `.env` (only
`.env.example`); no tracked file and no committed diff in history contains a
CWA-key-format string (the ignored local `.env` is excluded); and the fixture and
saved raw JSON hold no `Authorization` value. The check prints only findings, never
a secret. The whole run needs no network, no `.env` and no secret.

**Smoke — [`home_work_01-smoke.yml`](../.github/workflows/home_work_01-smoke.yml).**
Runs on demand only (**`workflow_dispatch`**); it never runs on push. It reuses
[`smoke.py`](smoke.py) unchanged, so CI and a local run perform the same check. The
public URL comes from the **`HW01_DEPLOY_URL`** repository variable — the documented
default source, set by the repository owner (RB-3). The workflow also accepts an
optional **`url`** input that **overrides** the variable when non-empty (it defaults
to the variable when the input is left empty); if neither yields a URL the run fails
with a clear message. GitHub only dispatches a `workflow_dispatch` workflow that
exists on the **default branch** (`main`); this workflow lives only on the topic
branch until the reserved merge to `main` (RB-1), so it **cannot be dispatched
before that merge** — run the identical check locally with
`python smoke.py <preview-url>` meanwhile. After the merge, the default dispatch
uses the production `HW01_DEPLOY_URL` variable and is **release evidence**
(DR-12, DR-18); the `url` input then lets you smoke-check any other URL.

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
| `app.py` (Streamlit) | [`app.py`](app.py) — the Grading App (Issue #19), reading through [`weather_query.py`](weather_query.py) |
| (deployed web app) | [`server.py`](server.py) + [`static/`](static/) + [`api/index.py`](api/index.py) + [`vercel.json`](vercel.json) — the Flask dashboard (Issue #20), also reading through [`weather_query.py`](weather_query.py) |
| `weather_data.csv` (optional) | not used |
