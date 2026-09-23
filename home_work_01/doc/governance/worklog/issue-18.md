# Worklog — Issue #18 (Ingestion: derive & persist the Forecast Snapshot)

- **Work item**: GitHub Issue #18 (`yotsubamomo/aiot-classwork`), `home_work_01`, Formal lane.
- **Executing role / binding**: `gov-executor` (Bindings §3.1 mapping: `claude-opus-4-8`,
  effort `high`). Binding verification (agentId + observed model/effort from the harness
  `subagents/` records) is performed and recorded by the dispatching Orchestrator per
  Bindings §3.4; this worklog records the role and the declared mapping.
- **Subject**: branch `home_work_01-hw10-implementation` (BASE `d42b1a7`); commit reported
  in the Executor return for this work item.

## 1. Work performed

Built the ingestion pipeline for `home_work_01` (fetch → derive → persist), captured the
first real `F-D0047-091` response and fixture, generated the committed `data.db` snapshot,
wrote the offline test suite, and wrote the README ingestion section with the R-DOC-2
data-side labeling. Set up the Python 3.12 unit environment.

## 2. Contract reference

- **Ticket**: Issue #18 (Scope class MVM; What to build; checkbox ACs; Traceability; High-risk
  H-1/H-2/H-3; Reserved; Out of scope).
- **Spec**: `doc/spec/SPEC.md` v1.1 — R-ING-1..6, R-DER-1..8, R-DB-1..6, R-SEC-1/2,
  R-TC-1(derive/persist)/2/5, R-ENV-1/2, R-DOC-1(Ingestion)/2(data)/5; §4.1, §5.
  ACs AC-05, AC-06, AC-07(a–d), AC-08, AC-09, AC-11, AC-24(data), AC-25(artifact), AC-27.
  Invariants INV-3, INV-4, INV-5, INV-7(labeling), INV-8.
- **Decisions (authoritative, not reopened)**: `decision-20260923-spec-interpretation-rulings.md`
  DR-3, DR-4, DR-5, DR-6, DR-10, DR-15, DR-16; `decision-20260923-high-risk-categories.md`
  H-1/H-2/H-3 + A-1/A-5.

## 3. Decisions and assumptions (all within accepted contract)

- **Module layout (HOW, R-ING-6 SHOULD)**: `ingestion/` package with `fetch.py` (fetch),
  `derive.py` (parse/derive, pure), `persist.py` (database), `pipeline.py` (`python -m ingestion`),
  plus `config.py` (contract-fixed constants) and `checks.py` (secret scanner). README maps
  these to the poster `HW10_Weather/` `fetch_weather.py` / `parse_weather.py` / `database.py`.
- **Period cadence (observed in the real capture)**: the 2026-09-24 capture (taken after
  midnight) begins with a leading `00:00–06:00` partial period, then day(06:00)+night(18:00)
  segments for 2026-09-24..09-30. Per R-DER-2/DR-5 a Forecast Day uses only the 06:00 and 18:00
  starts; the `00:00–06:00` partial is not a Forecast-Day segment and is ignored. Result: window
  2026-09-24..09-30 = 7 consecutive complete days, matching brief §4.6's W1 prediction exactly.
  This is a direct application of the fixed W1 rule, not a new interpretation.
- **Rounding (DR-4)**: `Decimal` arithmetic, `ROUND_HALF_UP` to one decimal.
- **Snapshot replace (DR-3, R-DB-4)**: single `with conn` transaction — DELETE all, INSERT 42,
  upsert metadata; rollback on failure preserves the previous snapshot.
- **Metadata (DR-2, R-DB-5)**: separate `IngestionMetadata` table (single row id=1) holds
  `ingestedAt` (ISO 8601 +08:00) and `sourceDatasetId`; `TemperatureForecasts` DDL unchanged.
- **Fixture (DR-10, R-TC-2)**: real `F-D0047-091` response captured 2026-09-24, saved complete
  at `data/raw/F-D0047-091.json`; the test fixture `tests/fixtures/F-D0047-091_sample.json` is a
  faithful **reduced** version (only 最高溫度/最低溫度 elements per county, structure preserved) —
  it derives byte-identically to the full capture (verified). Negatives derived by test mutators.
- **Out of scope (respected)**: no shared query module, `app.py`, Flask, dashboard, CI, or
  deployment (those are later tickets). No `folium`/`streamlit-folium`.

## 4. Artifacts

- Environment: `requirements.txt` (requests==2.32.3, pytest==8.3.3), `.gitignore`, `pytest.ini`;
  local `.venv` (git-ignored).
- Code: `ingestion/{__init__,__main__,config,fetch,derive,persist,pipeline,checks}.py`.
- Data: `data/raw/F-D0047-091.json` (complete indented raw observation, no key),
  `tests/fixtures/F-D0047-091_sample.json` (reduced real fixture), `data.db` (42-row snapshot,
  regenerated offline from the saved JSON with the committed code).
- Tests: `tests/{conftest,test_derive,test_persist,test_fetch,test_pipeline,test_secrets}.py`.
- Docs: `README.md` (ingestion section, data-side labeling, poster mapping); this worklog.

## 5. Verification (self-verification per governance §3.5; not an independent audit)

- **Full suite**: `pytest -q` → **38 passed** (Python 3.12.14, offline, no network, no `.env`).
  - Derive AC-08: 42 rows, 6 regions, 7 consecutive days; 4 hand-computed Region×day values
    (南部 24/29, 中部 24/30) exercising half-up rounding; single-county region; leading partial dropped.
  - Derive AC-09: five negatives each raise a named error (missing county 苗栗縣; missing half-day
    naming 臺北市+2026-09-26; invalid `-`/empty naming county+date; only six days; non-consecutive).
  - Persist AC-05: stored DDL == teacher DDL verbatim; `PRAGMA table_info` exact; both verification
    SQLs (6 distinct regions / 7 中部地區 rows, `YYYY-MM-DD`).
  - Persist AC-06: re-ingest same fixture → 42 rows, no `(regionName,dataDate)` duplicate;
    date-shifted snapshot fully replaces (old dates gone).
  - Persist AC-24: `IngestionMetadata` single row updated in place; `TemperatureForecasts` DDL unchanged.
  - Fetch AC-11: 401/404/500/503, timeout, non-JSON, success=false, wrong resource_id all raise
    `FetchError`; error message never contains the key. Key loading: missing file / empty value.
  - Pipeline R-ING-5: offline `--from-json` rebuilds 42 rows; a validation failure returns exit 1
    and leaves the prior snapshot unchanged (AC-09 integration guarantee).
  - Secrets AC-07(d): committed fixture and raw JSON have no key pattern and no Authorization value;
    scanner positively flags a key-shaped string (guard against a no-op scanner).
- **Real fetch (AC-07a)**: on 2026-09-24 `python -m ingestion` fetched `F-D0047-091` once with the
  key from `.env` — HTTP 200, `success:"true"`, `resource_id:"F-D0047-091"`, 22 counties, 15 periods
  per temperature element; saved the raw JSON and printed the fetch summary + 42-row preview.
  The key value was never printed, logged, or written to any tracked file.
- **A-5 mechanical checks (recorded evidence; local, `.env` excluded)**:
  - #1 `git ls-files home_work_01` contains no `.env` (only `.env.example`). **CLEAN**.
  - #2/#3 Scan of every staged file's blob + the staged diff for the **literal real key**:
    **0 matches** anywhere. The two H-1 artifacts (`data/raw/F-D0047-091.json`,
    `tests/fixtures/F-D0047-091_sample.json`) are fully clean (literal / key-pattern / Authorization
    all absent). The broad `CWA-...` key-pattern / `"Authorization":"…"` heuristic matches only two
    self-referential detector files — `ingestion/checks.py` (the scanner's own regex source) and
    `tests/test_secrets.py` (the scanner's positive unit-test literals). Neither is a real secret.
    (`test_fetch.py`'s placeholder was changed to a non-key-shaped string to remove a self-inflicted match.)
  - #4 DDL comparison: `TemperatureForecasts` DDL stored in `data.db` == `config.FORECAST_TABLE_DDL`
    minus the trailing `;`. **MATCH**.
- **INV checks**: INV-3 (0 or exactly 42 rows, atomic replace) — persist design + AC-06; INV-4
  (teacher names unchanged) — AC-05 + `config`; INV-5 (key zero-leak) — A-5; INV-7 (labeling) —
  README data-side section; INV-8 (Python 3.12) — venv `3.12.14`, `requirements.txt`.

## 6. Audit status

- Formal Ticket independent audit (R1) is **required** (Bindings §5; A-1 covers H-1/H-2/H-3) and is
  **not yet performed** — dispatched separately by the Orchestrator, not by this Executor session.
  This worklog records self-verification only; it is not an audit PASS.

## 7. High-risk category checks (A-1, for the R1 audit's convenience)

- **H-1 (credential/secret)**: key read only from untracked `.env`; never printed/logged/written;
  A-5 #1–#3 recorded above; both saved artifacts scanned clean; fetch error paths key-free (tested).
- **H-2 (teacher-named interfaces)**: DDL verbatim (A-5 #4 + AC-05); table/column names, six Region
  Chinese names, `dataDate` `YYYY-MM-DD`, dataset id `F-D0047-091`, `data.db` path all in `config.py`
  and asserted by tests. Metadata stored in a separate table (DDL unchanged).
- **H-3 (derivation & labeling)**: W1 grouping, retention, county-day aggregation, project Region
  mapping, half-up mean, "all member counties present else named error / no denominator change",
  6×7 + no-partial-write — all in `derive.py`/`persist.py` and covered by AC-08/AC-09 with
  hand-computed expected values. Labeling (PROJECT-DERIVED COMPATIBILITY VALUES, project-defined
  mapping, F-A0010-001 original+delisted, F-D0047-091 compatibility replacement, W1 window) in README.

## 8. Remaining work / concerns

- None blocking for this ticket's scope. The offline observation file `data/raw/F-D0047-091.json`
  (~1.7 MB) is committed so the R1 Reviewer can verify AC-25 and rerun `--from-json` without a key.
- Downstream tickets depend on this ticket's `data.db`, the fixture, the `IngestionMetadata`
  semantics, and the `ingestion.derive.derive_snapshot` interface.
- Status: **DONE** (pending required independent audit).
