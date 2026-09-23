# HW10 — Taiwan Weather Forecast

This context defines the concepts used by the Part 5 / HW10 homework: a one-week temperature
forecast for six Taiwan regions, taken from CWA open data, persisted, and shown in a public web
app. Each entry gives the term the project uses, what it means, and the wording to avoid. Terms
are framework-agnostic; implementation choices live in the spec, not here.

## Sources

**Part A**:
The teacher's HW10 poster: the graded homework (six regions × one week, MinT/MaxT, persisted data,
interactive web app) and its grading weights.
_Avoid_: The homework, the PDF (the PDF also contains Part B)

**Part B**:
The teacher's grill-result design ("CWA Temperature Broadcast Visualization with Windy API"), a
separate design/reference source describing a different, station-level system. Elements of it may
be adopted only by explicit decision.
_Avoid_: The design, the real spec

**Course overview**:
The teacher's course-overview image, transcribed; sections 1–21 restate the Part A workflow,
sections 22 onward are reference only.

**Upper contract (上位契約)**:
The teacher-provided documents in `doc/requirement/` — Part A and the course overview §1–21 —
which the MVM must fully satisfy. Read-only for agents.
_Avoid_: The requirements (ambiguous), the assignment (when Part B or the teacher repo is meant)

**Teacher reference repo**:
`huanchen1107/AIoT_L3_CWA_HW1`, the teacher's own implementation found on 2026-09-23. An important
current reference for how the teacher adapted the work after the assigned dataset was delisted; it
is not the upper contract.
_Avoid_: The teacher's assignment, the new spec

## Forecast data

**Assigned dataset**:
CWA `F-A0010-001` (一週農業氣象預報), the dataset the upper contract names. Delisted by CWA on
2026-07-01; it stays documented as the original requirement.
_Avoid_: The old API, the broken dataset

**Replacement source**:
CWA `F-D0047-091` (臺灣各縣市鄉鎮未來1週逐12小時天氣預報), the county-level dataset the project
ingests instead. A project compatibility decision, not a teacher instruction.
_Avoid_: The new assignment, the CWA regional forecast

**County**:
One of the 22 `LocationName` entries of the Replacement source (縣市). Three of them — 澎湖縣,
金門縣, 連江縣 — belong to no Region.
_Avoid_: Location, city (alone), region

**Region**:
One of the six forecast areas the upper contract names: 北部地區, 中部地區, 南部地區, 東北部地區,
東部地區, 東南部地區. In the compatibility model each Region is the project-defined group of
Counties listed under Region mapping; the Chinese name is stored exactly as above.
_Avoid_: Location, area, zone, county, city

**Region mapping**:
The project-defined grouping of Counties into Regions: 北部 = 基隆市 臺北市 新北市 桃園市 新竹市
新竹縣 苗栗縣; 中部 = 臺中市 彰化縣 南投縣 雲林縣 嘉義市 嘉義縣; 南部 = 臺南市 高雄市 屏東縣;
東北部 = 宜蘭縣; 東部 = 花蓮縣; 東南部 = 臺東縣. It is a compatibility choice and is never
described as an authoritative CWA mapping.
_Avoid_: CWA regions, official grouping

**Forecast Day**:
One date label D inside the one-week window, formed by the project's grouping rule: the
06:00–18:00 period of D and the 18:00–06:00 period that starts on D. It is a compatibility window,
not a strict 00:00–24:00 calendar day. A Forecast Day is complete only when both periods are
present; only complete days are retained. Stored as `dataDate`.
_Avoid_: Calendar day, meteorological day, time, period, timestamp

**MinT / MaxT**:
The minimum and maximum air temperature, in °C, for one Region on one Forecast Day. These are
forecasts, never observations. In the compatibility model they are Compatibility values.
_Avoid_: Low/high, current temperature, observed temperature

**Compatibility value**:
A regional MinT or MaxT the project derives from County forecasts: county-day MinT = minimum of the
day's period minima, county-day MaxT = maximum of the day's period maxima, then the arithmetic mean
across the Region's member Counties, rounded to one decimal. Never a CWA-issued six-region forecast.
_Avoid_: CWA regional value, official forecast, average temperature (reserved for the map)

**Forecast Snapshot**:
The currently persisted one-week forecast for all six Regions — exactly six Regions × seven complete
Forecast Days — as last ingested. A new snapshot replaces the previous one entirely; the project
keeps no history of earlier forecasts.
_Avoid_: Forecast log, forecast history, time series of forecasts

**Ingestion**:
The offline process that acquires the Replacement source, derives Compatibility values per Region
and Forecast Day, validates the result, and persists the Forecast Snapshot. Running it again must
not create duplicate logical records; missing County data is an error, never a silent change of the
mean's denominator.
_Avoid_: Sync, ETL job, crawler

**Refresh**:
Running Ingestion again so the persisted Forecast Snapshot becomes a newer one. Optional; the
minimum product ships a prepared snapshot.
_Avoid_: Live data, real-time update

## Application

**Web App**:
The product's user-facing behaviour: read the persisted Forecast Snapshot (never call CWA), let the
user select a Region, and show that Region's one-week MinT/MaxT chart and table. It is delivered by
two presentation layers, the Grading App and the Dashboard, which share the same data and the same
query semantics and must behave identically for every MVM behaviour.
_Avoid_: Frontend, site, backend

**Grading App**:
`app.py`, the genuine Streamlit application the teacher's documents name, run locally with
`streamlit run app.py`. It carries the complete MVM behaviour and no enhanced features. It is not
the deployed runtime; that is a compatibility accommodation forced by the Vercel requirement, not a
statement that Streamlit was outside the assignment.
_Avoid_: Local prototype, demo app, legacy app

**Dashboard**:
The publicly deployed presentation layer on Vercel ("Taiwan Weather Dashboard"): every MVM behaviour
plus the enhanced ones — improved UI/UX, responsive layout, Select Date and the Taiwan Map.
_Avoid_: Web App (when only this layer is meant), homepage, frontend

**Taiwan Map**:
The enhanced view, in the Dashboard only, that places the six Regions on a map of Taiwan, colours
each by its Derived Map Temperature for a selected Forecast Day, and shows that Region's MinT/MaxT
on request.
_Avoid_: Heatmap, station map, weather map

**Derived Map Temperature**:
`(MinT + MaxT) / 2` for one Region on one Forecast Day, shown to one decimal place. It is derived
from the two forecast values because the data model has no measured daily mean; the user-facing map
may call it "average temperature", but it is never an observed meteorological mean. Colour bands are
lower-inclusive: `< 20` blue, `20 – < 25` green, `25 – < 30` yellow, `≥ 30` red.
_Avoid_: Daily mean, observed average, mean temperature

**Select Region / Select Date**:
The two user controls named by the teacher: choosing the Region for the chart and table, and
choosing the Forecast Day for the Taiwan Map.
_Avoid_: Filter, dropdown (as a concept name)

## Scope

**MVM**:
The smallest deployable system that satisfies every graded Part A requirement and is reachable at a
public Vercel URL. It must not depend on anything classified as enhanced or optional.
_Avoid_: MVP, prototype, demo

**Scope class**:
Every material item carries one of four classes: MVM REQUIRED, ENHANCED REQUIRED (part of the final
deliverable but outside the MVM), OPTIONAL (may be built, never required), REFERENCE / FUTURE (not
built unless separately promoted).
_Avoid_: Nice-to-have, stretch goal, phase (as a class name)
