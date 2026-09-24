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
- **Metadata (DR-2, R-DB-5; acquisition-time semantics per DR-17 — see §9)**: separate
  `IngestionMetadata` table (single row id=1) holds `ingestedAt` (ISO 8601 +08:00, = acquisition
  time) and `sourceDatasetId`; `TemperatureForecasts` DDL unchanged.
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
- Status after cycle 1 R1: **BLOCKING (F-1, F-2)** + DR-17 routing → targeted correction (see §9).

## 9. Cycle 1 targeted correction — R1 BLOCKING (F-1, F-2) + DR-17

- **Trigger**: R1 audit `doc/governance/audit/issue-18-c1-r1.md` returned **BLOCKING (F-1, F-2)**;
  DA record `doc/governance/decisions/decision-20260924-ingestion-timestamp-semantics.md` (DR-17)
  folded in. Same work item / worklog identity / branch; targeted correction only (governance §4.4).
- **New subject**: branch `home_work_01-hw10-implementation`; new commit reported in the return.

### 9.1 Findings addressed

- **F-1 (Medium, H-3) — drop-leading-incomplete-day now tested.** Added
  `tests/conftest.make_leading_incomplete` (relabels the real 00:00–06:00 leading partial to a
  2026-09-23 night-only day, i.e. the after-18:00 capture shape) and
  `test_derive.test_drops_incomplete_leading_day_and_keeps_seven` (asserts 2026-09-23 dropped, the
  same 42 rows / window 24..30 retained). **Regression bar met**: deleting `derive.py:149-150`
  (the drop-leading lines) now fails that test with `DeriveError: forecast day 2026-09-23 is
  missing a 12-hour period` (mutation run: 1 failed, 58 passed).
- **F-2 (Medium, H-1/H-3) — failure cases now assert through the CLI.** Added
  `test_pipeline.test_ac09_negative_via_cli` (all five AC-09 negatives) and
  `test_ac11_http_failure_via_cli` + `test_ac11_timeout_via_cli` (401/404/500/503/non-JSON/timeout),
  each asserting **exit code 1**, **snapshot signature unchanged** (all rows + metadata), and — for
  AC-11 — **key-free stdout+stderr** (sentinel key absent) and **no raw JSON written**.
  **Regression bar met**: narrowing `pipeline.py:191` so `FetchError` is not caught (fetch error →
  bare traceback) now fails all six AC-11 CLI tests (mutation run: 6 failed, 53 passed).
- **DR-17 — acquisition-time provenance implemented** (I-1..I-6):
  - `run_online` captures the timestamp **at fetch success** and writes it to a key-free provenance
    sidecar `data/raw/F-D0047-091.meta.json` (new `ingestion/provenance.py`), passing the **same
    value** to `persist_snapshot` (I-1).
  - `run_offline` reads the acquisition time from the sidecar or `--acquired-at`, **removes the
    clock read**, and **fails closed** (ProvenanceError → exit 1, no write) when absent (I-2).
  - README documents the sidecar location/content, the offline behavior, and that a rebuild does
    not update "last updated" (I-3).
  - **I-4 executed**: re-ran online ingestion **once** with the corrected pipeline (authorized N-10,
    OC AB-8/§5; CWA reachable, so the DA fallback I-5 was not needed). Committed raw JSON, provenance
    sidecar and `data.db` as a consistent set: `data.db.ingestedAt == provenance.acquiredAt ==`
    **`2026-09-24T02:24:50+08:00`** (verified). The regenerated raw JSON is byte-identical to the
    previous capture (the response carries no timestamp, DR-17 E-5), so only `data.db` and the new
    sidecar changed. Offline rebuild from the committed raw JSON + sidecar reproduces the same
    `ingestedAt` (verified). Fixture kept unchanged (AC-08 hand-computed values still valid).
  - Tests **T-1..T-4** added in `test_pipeline.py` (online records fetch-time in sidecar + db;
    offline uses sidecar not clock; explicit `--acquired-at` override; offline-without-time →
    exit 1 / no write / snapshot unchanged / message names provenance) and `test_secrets.py`
    (committed sidecar is key-free).
- **Low findings cleared (owner #18, in scope, low-risk)**:
  - **F-3**: `derive._value` now rejects `NaN`/`Infinity` (`Decimal.is_finite()`), so they surface
    as a named county-day error instead of a later crash; `test_derive.test_non_numeric_values_are_invalid`.
  - **F-4** (partial): `fetch._validate_payload` guards a non-dict JSON body; `run_offline` maps a
    missing/invalid JSON file to a clean `DeriveError` (no traceback, fail-closed).
  - **F-8**: `test_pipeline.test_shifted_fixture_reingest_replaces_via_cli` re-ingests a
    date-shifted **fixture** through the CLI and asserts full snapshot replacement.
  - **F-5**: reworded the derive post-condition comment (no longer self-labeled "unreachable"; it is
    a defensive shape guard). Not a behavior change.
- **Left to their owners (dispositioned, non-blocking)**: F-6 (`--env` flexibility — default is the
  unit `.env`; restricting it would break legitimate temp-env tests), F-7 (#22 CI regex), F-9 (#25),
  F-10 (#19), F-11 (#25).

### 9.2 Verification (self-verification; not an independent audit)

- **Full suite**: `pytest -q` → **60 passed** (was 38), offline, Python 3.12.14.
- **Mutation/regression checks** (on scratch copies, files restored):
  - Delete `derive.py:149-150` → `test_drops_incomplete_leading_day_and_keeps_seven` FAILS (1 failed / 58 passed).
  - Narrow `pipeline.py:191` catch (drop `FetchError`) → 6 AC-11 CLI tests FAIL (6 failed / 53 passed).
- **DR-17 consistency**: `data.db.ingestedAt == provenance acquiredAt ==` `2026-09-24T02:24:50+08:00`;
  offline rebuild from committed raw JSON + sidecar reproduces it.
- **A-5 refresh (staged correction set, `.env` excluded)**: literal real key **0** across all staged
  files and the staged diff; the new provenance sidecar and `data.db` are fully clean (literal /
  key-pattern / Authorization all absent); the only heuristic match is `tests/test_secrets.py`'s
  scanner unit-test literals (not a secret); `git ls-files` still has no `.env`. DDL unchanged (H-2).

### 9.3 Remaining

- Status: **DONE** (targeted correction complete; pending R2 scoped closure review).
- Not committed by this Executor (belong to their authors / the Orchestrator): the R1 audit record,
  the DR-17 decision record, and the run record — left untracked/for the dispatcher.
