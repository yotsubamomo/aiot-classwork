# HW10 — Taiwan Weather Forecast (`home_work_01`)

A one-week temperature forecast for six Taiwan Regions, **derived from CWA
county-level open data** (not a CWA-published six-region product — see
[Data source and labeling](#data-source-and-labeling-please-read)), persisted to
SQLite, and shown in a web app.

> **Scope of this README.** This document covers the whole project end to end: the
> **ingestion** stage (fetch → derive → persist), the **Streamlit Grading App**
> (`app.py` + the shared query module `weather_query.py`), the **Flask dashboard**
> (`server.py`, the `/api/` JSON API and the static frontend under `static/`) with its
> interactive **Taiwan Map** in two modes — the V2 **Now mode** (Latest Observation of
> CWA stations; see [Taiwan Map modes](#taiwan-map-modes-now-mode-and-forecast-mode-v2-core))
> and the **Forecast mode**, which is the Part A bonus six-region map with its ENHANCED
> **`Select Date`** control (see
> [Forecast mode](#forecast-mode--the-part-a-bonus-map-six-region-taiwan-map-and-select-date)), the
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

**Acquisition-time format.** The acquisition time — whether passed via
`--acquired-at`, read from the sidecar `acquiredAt` field, or generated by the
online run — must be exactly `YYYY-MM-DDTHH:MM:SS+08:00` (for example
`2026-09-24T02:24:50+08:00`): an ISO 8601 instant with an uppercase `T`, precision
to the second, and the literal `+08:00` offset. The digits must be ASCII `0`-`9` (a full-width or other
Unicode digit is rejected). Anything else is **rejected**
(fails closed: a message naming the offending value and its source, a non-zero exit,
and no database write) and is never silently normalized or truncated — this
includes an empty value, a date only, a value with no offset, a `Z` (UTC) or any
other offset, fractional seconds, a space (rather than `T`) separator, non-ASCII
digits, and any surrounding whitespace (including a trailing newline). There is
no plausibility or "not in the future" check (that would read the clock, which the
offline path must not do). A malformed `--acquired-at` does **not** fall back to the
sidecar — omit `--acquired-at` to use the sidecar instead.

Useful CLI options: `--from-json PATH` (offline source), `--raw-out PATH`
(where the online run saves the raw JSON), `--env PATH` (the `.env`), `--db PATH`
(the SQLite file to write), `--acquired-at YYYY-MM-DDTHH:MM:SS+08:00` (offline:
acquisition time to record, overriding the sidecar).

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

Open <http://127.0.0.1:5000/>. The Taiwan Map at the top opens in **Now mode**
(see [Taiwan Map modes](#taiwan-map-modes-now-mode-and-forecast-mode-v2-core)); its
**Forecast** button switches to the six-region forecast map. Below the map, the page
is the same MVM experience as the
Grading App — `Taiwan Weather Forecast`, a `Select Region` control over the six
Regions in the fixed order, and, for the selected Region, a `MaxT` / `MinT`
seven-day line chart and a `Date` / `MinT` / `MaxT` table equal to `data.db`,
plus the snapshot's acquisition time. It is a static HTML/CSS/JS frontend (no
build step) whose chart is drawn with plain inline SVG (no chart library, no key).
Add `?region=<name>` to deep-link a Region (for example `?region=中部地區`). If the
forecast data is unavailable the forecast section (and the Forecast mode map) shows a
clear message instead of a blank page, while the Now mode keeps working.

All data comes from this application's own JSON API under the `/api/` prefix; the
browser never calls CWA and holds no key. The forecast endpoints read `data.db` only
through the shared module [`weather_query.py`](weather_query.py) and never call CWA.
The only server-side CWA access is the V2 Latest Observation endpoint (see
[below](#latest-observation-endpoint-v2-core)), implemented in
[`observation.py`](observation.py).

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
opened read-only. The forecast endpoints and `/api/health` need no environment
variable or secret; only the Latest Observation endpoint below reads `CWA_API_KEY`.

### Latest Observation endpoint (V2 Core)

`GET /api/observations/latest` returns the **Latest Observation**: CWA station
observations from the dataset **O-A0001-001** (氣象觀測站-全測站逐時氣象資料;
CWA describes it as hourly station data), fetched **server-side** with the
maintainer's key, then normalised and trimmed. The response never contains the
upstream JSON structure, the upstream URL or the key. Observation values are
**CWA station observations, as published** — not forecasts and not project-derived
values. The browser only ever calls this `/api/` path.

**Success — `200` JSON** (`Cache-Control: no-store`):

| Field | Meaning |
| --- | --- |
| `dataset` | `"O-A0001-001"` |
| `observationTime` | Dataset-level **Observation Time**: the latest `ObsTime` among the valid stations, exactly as CWA published it (for example `2026-09-25T23:00:00+08:00`). |
| `fetchedTime` | **Fetched Time**: the server clock when the upstream fetch succeeded and produced this body — ISO 8601, `+08:00`, to the second. This is not the forecast snapshot's acquisition time shown by the forecast dashboard. |
| `validStationCount` | Number of valid stations in `stations`. |
| `receivedStationCount` | Number of station records CWA returned (diagnostic; includes invalid ones). |
| `stations[]` | One entry per **valid** station: `stationId` (the stable identity — names can repeat), `stationName`, `countyName`, `townName`, `latitude` / `longitude` (WGS84), `observationTime` (that station's `ObsTime`, as published), `airTemperature` (°C). Optional, `null` when missing or a sentinel: `relativeHumidity` (%), `windSpeed` (m/s), `windDirection` (degrees), `airPressure` (hPa), `precipitation` (the dataset's `Now.Precipitation` field: accumulated precipitation for the current day, mm), `weather` (text). |
| `representativeStationIds` | The `stationId` of each county's **representative station** for the Now mode's Taiwan-wide view — at most one per county, in a fixed county order (north to south, east coast, then 澎湖縣, 金門縣, 連江縣); see [Representative station rule](#representative-station-rule). |


Numbers keep the published digits (no rounding, no unit conversion); a sentinel is
never turned into a number.

**Valid station.** A record is valid only if it has a non-empty `StationId`; an
air temperature that is a finite number and not a sentinel; a finite WGS84
latitude and longitude; a `CountyName` that is exactly one of the 22 counties
(the 19 forecast-Region member counties plus 澎湖縣, 金門縣, 連江縣; `臺`, not
`台`); and a published `ObsTime` that parses to a date with hour and minute (an
`ObsTime` without an offset is read as `+08:00` for comparison only). Invalid
records are left out of `stations`, the count and `observationTime`. Zero valid
stations is a failure (`invalid_response`).

**Sentinel codes, per field** (CWA data standard V1.05; matched as text and, for
the numeric ones, by value such as `-99.0`). A code is applied only to the fields
it is defined for; anywhere else the published value is a real reading and is
returned as published — for example a station pressure or rainfall of `990.0`.

| Code | Meaning | Applied to |
| --- | --- | --- |
| `X` | instrument failure | every field |
| `-99` | missing / abnormal | every field (including the WGS84 coordinates) |
| `T` | trace of rain | `precipitation` |
| `-98` | continuous no precipitation | `precipitation` |
| `990` | variable wind direction | `windDirection` |
| all five | — | air-temperature validity (a station with any of them is not valid) |

A code that applies turns an optional field into `null` (shown as "—"), never a
number. The mapping is the `FIELD_SENTINELS` constant in `observation.py` and can
be replaced through `LatestObservationService(field_sentinels=...)`.

**Failure — non-2xx JSON** `{ dataset, reason, error }` with exactly one `reason`:

| `reason` | HTTP | When |
| --- | --- | --- |
| `key_not_configured` | `503` | The server has no `CWA_API_KEY` (no upstream request is made). |
| `upstream_unreachable` | `504` | DNS / connection failure, or the upstream did not finish within the time bound. |
| `upstream_error` | `502` | CWA answered with a non-2xx status (e.g. `401` / `403` auth, `429` quota, `500`); the numeric status is added as `upstreamStatus`. |
| `invalid_response` | `502` | CWA answered 2xx but the body is not JSON, `success` is not `"true"`, the structure or dataset id is wrong, or no station is valid. |

`error` is a fixed human-readable sentence per reason; it and the server log carry
only the reason (and the numeric upstream status) — never the key, the upstream
URL, request headers or the upstream body. The server never answers with old data
after a failure: a response is either a success or a classified failure.

**Time bound and reuse window.** The upstream request uses a 3 s connect timeout
and a 5 s read timeout, and the whole upstream exchange is capped at **8 s**, after
which the answer is `upstream_unreachable` — below Vercel's smallest default
function duration (10 s), so a stalled CWA yields this JSON rather than a platform
error page. The page itself waits at most 20 s for this endpoint and treats no
answer, or a non-JSON / unclassified answer, as a failure (see the Now mode's
**Time bound**). A success is **reused for 300 s** (5 minutes; the contract ceiling is
10 minutes): within that window every request gets the same body, including the
same `observationTime` and `fetchedTime`; after it, the next request fetches again.
Only successes are reused. The cache lives in the function's memory (no persistent
server state). There is no polling and no automatic refresh; with CWA's general
member quota (20,000 requests / day) the reuse window and the time bound are the
only throttles, and an exhausted quota shows up as `upstream_error`.

**Key — local run.** The key is read only from the process environment variable
`CWA_API_KEY`, at request time. Locally its source is the untracked
`home_work_01/.env` (see [Get a CWA key and create `.env`](#get-a-cwa-key-and-create-env)):
`python server.py` copies `CWA_API_KEY` from that file into the environment
before starting (it reads no other file and never prints the value). With
`flask --app server run`, set `CWA_API_KEY` in the environment yourself. Without a
key the endpoint answers `key_not_configured` and every forecast endpoint and
`/api/health` keep working unchanged. On Vercel the same variable name is read from
the project's environment variables, which only the repository owner fills in (the
setup steps are part of the deployment section).

**Sample.** [`tests/fixtures/O-A0001-001_sample.json`](tests/fixtures/O-A0001-001_sample.json)
is one **real** O-A0001-001 response captured **2026-09-26 00:04:56 +08:00**
(observation time 2026-09-25 23:00), **not reduced** (all 876 station records; only
re-serialised as compact JSON). It was checked key-free before it was committed
and is covered by the credential scans. The offline tests derive every
counter-example from it.

### Taiwan Map modes: Now mode and Forecast mode (V2 Core)

The **Taiwan Map** at the top of the dashboard has exactly two modes, switched with
the **Now** and **Forecast** buttons in the map's header (real buttons: click them, or
Tab to them and press Enter or Space; the filled one is the current mode). The page
always opens in **Now mode**, whatever the state of the forecast snapshot. Both modes
are ENHANCED, dashboard-only features; the Streamlit Grading App has neither.

| | **Now mode** (default) | **Forecast mode** (Part A bonus map, [below](#forecast-mode--the-part-a-bonus-map-six-region-taiwan-map-and-select-date)) |
| --- | --- | --- |
| Shows | The **Latest Observation**: CWA station air temperatures, **as published by CWA** | The six-region seven-day forecast: **project-derived** values |
| Data | `GET /api/observations/latest` | `GET /api/days`, `GET /api/days/<date>` |
| Markers | At most one **representative station** per county, a neutral light marker with the station's temperature and name; with a county selected, that county's stations | Six Region pills coloured by the derived band |
| Panel and controls | `Observation Time`, `Fetched Time`, valid-station count, `Refresh`; the county layer, the `County` chooser, the County context, the station list and detail, `Back to Taiwan` | `Select Date`, the `DERIVED` panel, the four-band legend |
| Never shown | `Select Date`, the derived legend, any forecast value | Any observation value, `Refresh` |

- **Two meanings kept apart.** An observation value is a CWA station observation, as
  published — not a forecast, not a project-derived value, and never an average of a
  county. A forecast value is a project-derived compatibility value (see
  [Data source and labeling](#data-source-and-labeling-please-read)). The two modes
  never share a panel, a legend or a colour scale: the Now mode's markers have no
  colour scale at all.
- **`Fetched Time` is not the forecast's "Last updated".** In the Now panel,
  `Fetched Time` is when this server fetched the Latest Observation from CWA. The
  line `Last updated (data fetched from CWA): …` beside `Select Region` below the map
  is the time the **forecast snapshot** was acquired. They are different times, with
  different labels, in different places.
- **Switching keeps your place.** Leaving Now mode remembers its view (zoom and
  position), the selected county and the selected station; coming back restores
  them all — the view is the one you left, not the county's own view. Entering Forecast
  mode keeps the current view when all six Region markers are already visible clear
  of the panels, and otherwise widens it just enough to show them.
- **Independent of the forecast.** The Now mode loads on its own and never waits for
  `/api/health`. If the forecast snapshot is unavailable, the forecast section below
  the map and the Forecast mode map show the forecast's error message (the V1 error
  states, now limited to the forecast part of the page), while the Now mode and the
  mode switch keep working.
- Both modes use the same vendored map and make **no external request**: the page
  only calls this app's own `/static/` and `/api/` URLs.

#### Now mode — Latest Observation

- **Source and cadence.** CWA open data **O-A0001-001** (氣象觀測站-全測站逐時氣象資料),
  which CWA describes as hourly data from its weather stations. The server fetches it
  (see [Latest Observation endpoint](#latest-observation-endpoint-v2-core)); the
  browser never contacts CWA. When CWA publishes a new hour is up to CWA, so the
  **Observation Time** shown is the CWA observation time of the data, not the time
  you are looking at the page.
- **Panel.** The *Latest Observation* panel (tagged `OBSERVED`) shows
  **`Observation Time`** — the latest station `ObsTime` in the data, to the minute,
  with its UTC offset as published — **`Fetched Time`** — when the server fetched the
  data, to the second — the number of **valid stations**, and the **`Refresh`**
  button.
- **`Refresh`.** Only a manual Refresh loads newer data; the page never updates by
  itself. While a Refresh runs, a spinner and "Refreshing the Latest Observation…"
  are shown and further presses are ignored (only one request is ever in flight, and
  only its answer is applied). Every Refresh — and the page's first load — ends in
  exactly one of three results, shown next to the button:
  - **newer** — the answer's Observation Time is the same as or later than the one
    shown and it is a new fetch: the markers, `Observation Time` and `Fetched Time`
    all update together ("Updated to a newer Latest Observation", or "Updated:
    fetched again; the Observation Time is unchanged");
  - **not-newer** — the answer's Observation Time is older than the one shown, or it
    is the very answer already shown (same `Fetched Time`, the server's reuse window):
    nothing changes and the page says "Already the latest". This is not Stale —
    nothing failed. An older Observation Time never replaces a newer one, so the
    Observation Time shown never goes back while the page is open;
  - **failure** — see Stale and Unavailable below.
- **Time bound.** The page waits at most **20 s** for an answer. The server itself
  answers within about 8 s even when CWA stalls (`upstream_unreachable`, see the
  endpoint section), so the page normally gets a classified answer first. If no
  answer arrives in 20 s (the network is down, or the platform holds the request),
  the request is abandoned and the Refresh counts as a failure; an answer that is not
  a usable JSON answer — such as the hosting platform's own HTML error page — counts
  as a failure as soon as it arrives. A Refresh never stays in progress.
- **Stale and Unavailable.** A failed Refresh while data is shown makes the Now mode
  **Stale**: the last successful data stays on the map with its own `Observation Time`
  and `Fetched Time`, a `STALE` label and a "Stale" note with the reason appear in the
  panel and on the map, and the markers are drawn with a dashed border. A failure with
  no data to show (for example on first load) makes it **Unavailable**: the map and the
  county boundaries stay visible, both times show "—", no station value is shown, and
  an `UNAVAILABLE` label and a "Latest Observation unavailable" note give the reason.
  In both, `Refresh` stays usable, the page stays in Now mode (it never switches to
  Forecast mode by itself), and the mode switch, Forecast mode and the forecast
  dashboard below keep working — an observation failure affects only the Now mode's
  observation layer. The next successful Refresh (newer or not-newer) clears Stale or
  Unavailable. Stale is decided **only by a failure, never by the data's age**: data
  that is hours old but was fetched successfully is not Stale.
- **Failure reasons.** The reason is a fixed category text, never a server or CWA
  message: "the server has no CWA API key configured" (`key_not_configured`), "the
  CWA service could not be reached in time" (`upstream_unreachable`), "the CWA
  service answered with an error status" with its HTTP status (`upstream_error`),
  "the CWA response was not usable" (`invalid_response`), and two for answers that
  never got a classified reason: "this site's server did not answer in time or
  could not be reached" and "this site's server gave an unexpected answer" (with the
  HTTP status, e.g. a platform `502` page).
- **Markers.** Each marker shows one representative station's air temperature in °C
  (the published value, shown with at least one decimal). Its station name is shown
  under it when zoomed in; hovering or focusing it shows the station name, county and
  town, its temperature and its Observation Time; clicking it (or pressing Enter)
  selects it and the panel lists that station's values, with "—" for any missing
  value. A marker is always a **station value**: it is never presented as "the
  county's temperature", and no county average is computed.

#### Now mode — Taiwan → County → Station

- **Choosing a county.** Point at a county on the map: its outline and a faint fill
  light up and its name is shown. Click it to select it. Without the map, use the
  **`County`** chooser in the Now panel (Tab to it; the arrow keys pick a county;
  "All of Taiwan" clears the choice). The county shapes react to the pointer only in
  Now mode; they are never coloured by any data value.
- **The county view.** Selecting a county zooms the map to the county and its
  stations and shows **every valid station of the county** as a marker (the
  Taiwan-wide representative markers are replaced; in the county view a marker's
  name label appears on the selected one, and hovering shows every marker's name).
- **County context.** The panel shows the county's name, its number of **valid
  stations** and how many of them are **on the map**, the station with the
  **highest** and the one with the **lowest** air temperature (its value and name),
  and the list of the county's stations with their air temperatures, highest first.
  Every number here is a published **station value** or a count of stations — **no
  county average or any other combined value is computed**. On an equal
  temperature, the station with the smaller `stationId` (character-code order, as in
  the representative rule) is listed first and is the one named as highest or
  lowest. A county with no valid station in the Latest Observation can still be
  selected: it shows `0` stations and "—" for the highest and lowest — that is not an
  error.
- **Station list and detail.** Each station in the list is a button: Tab to it and
  press Enter or Space (or click it, or click its marker) to see the **station
  detail**: its name and `StationId`, county and town, its own `Observation Time`, its
  air temperature, and its relative humidity, wind speed, wind direction (degrees),
  air pressure (hPa), precipitation (the dataset's `Now.Precipitation`: accumulated
  precipitation for the current day, mm) and weather — each "—" when CWA published
  no valid value.
- **`Back to Taiwan`.** The button beside the county's name clears the county and the
  station and returns the map to the Taiwan-wide view it opens with.
- **Stale and Unavailable.** The county shapes, the `County` chooser, the list and
  `Back to Taiwan` keep working when the Latest Observation fails. **Stale**: the
  County context shows the last successful data, marked Stale. **Unavailable**: the
  county's name is shown but every count and value is "—" (never `0`: with no Latest
  Observation there is no station set to count) and no station is listed.
- **Stations outside the map range.** A valid station whose position is outside the
  useful Taiwan map range — latitude **21.2 – 26.7**, longitude **117.6 – 122.9**, the
  same range as the representative rule below (for example 高雄市's **東沙島**,
  `468100`, at longitude 116.73) — is **not placed on the map**, but it **is counted**
  in its county's valid stations (the context shows e.g. "57 (1 not on the map)"),
  **listed** in the county's station list marked **"not on the map"**, and its
  **detail** can be opened from the list.
- **County shapes.** The interactive county shapes are the same vendored 內政部
  county polygons as the basemap (see the Forecast mode section), joined with their
  county names by [`static/data/counties.js`](static/data/counties.js) (a same-origin
  `<script>`, project data: the CWA `CountyName` of each basemap polygon). They are
  drawn transparent over the unchanged backdrop and load no data from anywhere; the
  offline tests check each name against the sample's stations inside the polygon.

#### Representative station rule

The Now mode's Taiwan-wide view shows at most one marker per county. Anyone can
recompute the choice by hand from a `GET /api/observations/latest` response (the
rule is implemented in [`representative.py`](representative.py) and its result is the
response's `representativeStationIds`):

1. **Candidates.** For a county, take the entries of `stations[]` with that
   `countyName` whose `latitude` is within **21.2 – 26.7** and `longitude` within
   **117.6 – 122.9** (the useful Taiwan map range, including 金門, 連江, 澎湖, 蘭嶼 and
   綠島). Every entry of `stations[]` is already a valid station.
2. **Preferred station.** If the county's preferred station is a candidate, it is the
   representative.
3. **Fallback.** Otherwise the candidate with the **smallest `stationId`**, comparing
   the characters by code (digits before capital letters, e.g.
   `"466910" < "466930" < "A0A010" < "C0A980"`), is the representative.
4. **No candidate, no marker.** A county without any candidate has no marker; that
   is not an error.

The preferred stations are **project data, not a contract**: the constant
`PREFERRED_STATION` in `representative.py` names, for each county, a lowland station
in the county's seat or named after the county or its seat — the CWA manned weather
station when there is one (for example 臺北 for 臺北市), otherwise an automatic
station in the seat's town (for example 太保 for 嘉義縣). They are listed only in
that file. Worked examples with the committed sample:

- **臺北市** — the preferred station 臺北 (`466920`) is valid, so it is the marker.
- **臺北市, if 臺北 had an invalid temperature** — the candidates start 鞍部 `466910`,
  陽明山 `466930`, 臺灣大學 `A0A010`, …; the smallest id, 鞍部, would be the marker.
- **高雄市, if its preferred station were invalid** — 東沙島 (`468100`, longitude
  116.73) is outside the map range and never a candidate; the smallest remaining id,
  `72V140` (高改旗南分場), would be the marker.
- **連江縣, if none of its stations were valid** — no marker for 連江縣.

The offline tests ([`tests/test_representative.py`](tests/test_representative.py))
check the rule on the sample and on derived samples (the preferred station of three
counties made invalid, an out-of-range station, a county with no valid station).

### Forecast mode — the Part A bonus map: six-region Taiwan Map and `Select Date`

**Forecast mode** is the V1 six-region seven-day Taiwan Map, unchanged: press
**Forecast** in the map's header to see it. It is the **Part A bonus map**. The
dashboard integrates its **`Select Date`** control and the map on the same page (the
"Taiwan Weather Dashboard"), alongside the Region chart/table/summary. These are
**enhanced, dashboard-only** features — the Streamlit Grading App deliberately has
neither.

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
Static checks confirm the Streamlit app, the shared module and their unit-local
import closure import no HTTP client (dotted forms such as
`from urllib import request` included) and carry no CWA URL / key; that SQL lives
only in the shared module (the Flask backend and `observation.py` hold none); and
that every frontend request form targets only same-origin `/api/` or `/static/`;
`app.py` also carries no map / `Select Date` / folium. For the V2 Latest
Observation endpoint, `tests/test_observation.py` covers normalisation of the real
sample, the valid-station rules and eight derived counter-examples, the four
failure reasons with a sentinel key (asserted absent from responses, logs and
console output), the reuse window with a controllable clock, the time bound
against a stalled or slow loopback server, and the forecast endpoints answering
unchanged with the network blocked and no key. For the Taiwan Map's two modes,
`tests/test_representative.py` checks the representative station rule on the sample
and derived samples, and `tests/test_modes_frontend.py` holds static guards on the
frontend source (the page opens in Now mode; the labelled mode buttons; the Now
mode loads without waiting for `/api/health`; each mode's controls and legend; the
verbatim labels; no colour shared between observation markers and derived bands; the
map size guard on the mode-switch path), and `tests/test_refresh_frontend.py` holds
static guards on the Refresh semantics (the page's time bound between the server's
bound and 30 s; no polling; one Refresh at a time; the not-newer rules; Stale and
Unavailable set only by a failure, with no clock or age test; fixed, distinct texts
for the failure reasons and no response text ever displayed), and
`tests/test_county_frontend.py` holds static guards on Taiwan → County → Station (the
22 county names, one per basemap polygon, each checked against the sample's
stations inside it; the frontend's map range equal to `representative.py`'s; no
aggregate and no data colouring in the county code; "—", never 0, with no Latest
Observation; the list items as buttons, the `County` chooser and the verbatim
`Back to Taiwan`; the mode switch never clearing the county). (Four browser-level
checks need a real Chrome and so run separately from the offline `pytest` suite: the
check that the dashboard shows a visible message when `/series` fails on first load,
[`tests/check_series_error_visible.py`](tests/check_series_error_visible.py); the
Now mode / Forecast mode check
[`tests/check_modes_browser.py`](tests/check_modes_browser.py), which runs the app
on loopback with the sample-fed observation path and the forecast OK or unavailable,
drives both modes at 1280 px and 375 px, and records every browser request; and the
Refresh check [`tests/check_refresh_browser.py`](tests/check_refresh_browser.py),
which drives the three Refresh results, Stale and Unavailable for each failure
reason, a stalled upstream, a platform `502` page and a held request, a page clock
moved two hours ahead, and the rest of the page while the observation fails, with a
sentinel key that must not appear in the page, the console or the server log; and
the county check [`tests/check_county_browser.py`](tests/check_county_browser.py),
which hovers and selects counties on the map and with the keyboard, compares the
County context with values worked out from the `/api/` response, walks the station
list and detail, `Back to Taiwan`, the off-map 東沙島 station, a county with no valid
station, the Now → Forecast → Now round trip, and the county layer under Stale and
Unavailable, at 1280 px and 375 px —
`python tests/check_modes_browser.py`, `python tests/check_refresh_browser.py`,
`python tests/check_county_browser.py`; they also need the `websocket-client`
package.)
The test fixture
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
