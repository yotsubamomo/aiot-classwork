# Acceptance document — HW10 Taiwan Weather Forecast (`home_work_01`)

Derived contract: `doc/spec/SPEC.md` **v1.1**. This document (Spec R-DOC-4) records,
for every acceptance criterion **AC-01…AC-30**, every invariant **INV-1…INV-9**, and
the acceptance-boundary coverage **AB-1…AB-17**, the status, verification method and
evidence reference. It is produced by Issue #25 (integration / final verification) and
is an entry point for the forthcoming **Spec Integration Audit** (governance §4.7); it is
**not** itself the independent audit.

## 0. Subject, environment, status legend

- **Final subject**: branch `home_work_01-hw10-implementation`, commit
  `6407d8b2d0f04523f5057b0880083f3bd836c6a8` — **the commit that includes this `ACCEPTANCE.md` (R-DOC-4 deliverable)**.
  Per Bindings §7 only `doc/governance/**` paths are record-only, so `doc/acceptance/`
  (this file) is part of the subject, **not** record-only. The app / query / db / static /
  test behaviour is identical to `2f52766` (the #25 delta is documentation wording +
  `doc/` records + a test-only unused-import removal; no `app.py`/`server.py`/`weather_query.py`/
  `data.db`/`static/*` behaviour change). `6407d8b` carries all the corrections + this
  deliverable and is the CI-verified (run `35948664254`) and deployment-smoked commit (§8);
  the branch HEAD is a subsequent record commit that only writes the post-build smoke/CI
  evidence values into this file and the worklog — a doc delta over `6407d8b` with no
  behaviour or verification-outcome change.
- **Environment**: clean Python **3.12.14** venv; deps from `requirements.txt`
  (Flask 3.1.2, pytest 8.3.3, streamlit 1.64.0, requests 2.32.3; pandas 3.0.6 transitive).
- **Committed `data.db`** sha256 `9bbf05bc6cc803444c8760432d6b484699c597f751fa16cb58bfbb5a0dbf542b`
  (the prepared-snapshot deliverable, R-DB-6; unchanged by #25).
- **PR**: #27 (`home_work_01-hw10-implementation` → `main`), OPEN.
- **Status legend**: **PASS** = verified on the final subject; **PASS (pre-merge; (c)
  post-merge)** = AC-22 per DR-18; **PENDING-ACCEPTOR** = post-merge release evidence /
  reserved-boundary item, not a completion condition and not a failure.

Evidence shorthand: *tests* = offline `pytest` (152 passed); *cred-scan* =
`python -m tools.credential_scan`; *shots* = `doc/acceptance/screenshots/`; *wl25* =
`doc/governance/worklog/issue-25.md`; *audit N* = `doc/governance/audit/issue-N-c1-*.md`;
*CI* = GitHub Actions `home_work_01-ci.yml` — latest green push run on the final subject
is `35948664254` (`6407d8b2d0f04523f5057b0880083f3bd836c6a8`), 152 passed, Python 3.12.14, credential scan passed.

## 1. Acceptance Criteria (AC-01 … AC-30)

| AC | Class | Status | Verification method & evidence |
| --- | --- | --- | --- |
| AC-01 | MVM | PASS | `streamlit run app.py` in clean 3.12 venv: Uvicorn started, `GET /` 200, no exception (wl25 §5 step 5). `test_app.py` (title/options/table). audit 19 R2. |
| AC-02 | MVM | PASS | Both layers show `Taiwan Weather Forecast` + `Select Region`; six Regions in R-SHR-2(b) order. `AppTest` (`test_app.py`), Flask client (`test_dashboard.py`), `/api/regions` order verified live (wl25 §5 step 6). shots `ac02_*`. audit 19/20/23. |
| AC-03 | MVM | PASS | Selected Region → MaxT/MinT line + `Date`/`MinT`/`MaxT` 7-row table; values == `data.db`; central & southeast checked. INV-2 comparison all six Regions identical, 7 rows (wl25 §6). `test_app.py`, `test_dashboard.py`. shots `ac03_*`. |
| AC-04 | MVM | PASS | Static checks pass (22 in `test_static_checks.py`): Python layers import no HTTP client (dotted forms incl.), no `opendata.cwa.gov.tw`/`CWA_API_KEY`; SQL only in `weather_query.py`; frontend requests target only `/api/`; both layers import the one shared module. audit 19 F-4→#20 resolved, 20 F-2. Residual: static scan does not recurse `static/vendor/` (#24 F-4, non-blocking — vendored Leaflet, no CWA URL/key). |
| AC-05 | MVM | PASS | `TemperatureForecasts` DDL verbatim (`id INTEGER PRIMARY KEY, regionName TEXT, dataDate TEXT, mint REAL, maxt REAL`); teacher SQL on committed `data.db`: DISTINCT regionName → 6, 中部地區 → 7; all dataDate `YYYY-MM-DD` (wl25 §6). `test_persist.py`. |
| AC-06 | MVM | PASS | Two consecutive ingests → 42 rows, no `(regionName,dataDate)` dup; date-shifted fixture → 42 all-new rows. `test_persist.py`, `test_pipeline.py`. Committed db verified 42 rows / 0 dup (wl25 §6). |
| AC-07 | MVM | PASS (a–d,f); (e) split — see note | (a) real fetch succeeded, no key in output (wl25 §5 step 4); (b) `git ls-files` tracks only `.env.example`; (c) cred-scan: 510 tracked files, no key-format string in tracked files/history, ignored `.env` excluded; (d) fixture/raw JSON no `Authorization`; (e) **the deployed dashboard needs no env var/secret = PASS** (server reads no OS env; documented), but **"no CWA key is set in the Vercel project env" = PENDING-ACCEPTOR** (R-SEC-3, H-1, RB-3, #21 F-3 — a Vercel-account setting only the acceptor can confirm; consistent with §5-3(c)); (f) `doc/` evidence scanned, 0 key-format. audit 18/19/20/21/22. |
| AC-08 | MVM | PASS | Derive on real fixture → 7 consecutive complete Forecast Days, 6 Regions, 42 rows; ≥2 Region×date hand-computed (half-up); leading incomplete day dropped. `test_derive.py` (19). audit 18 R2 (mutation-tested). |
| AC-09 | MVM | PASS | Five negative cases each fail, no DB write, non-zero exit, named problem; prior snapshot preserved. `test_derive.py`, `test_pipeline.py::test_ac09_negative_via_cli` ×5. audit 18 R1/R2. |
| AC-10 | MVM | PASS | Missing/empty/incomplete db: Grading App clear message no exception; `/api/health` 503, data endpoints 503, Dashboard page error state (DR-19). `AppTest`, `test_dashboard.py`, `check_series_error_visible.py` (browser). Final-UI Dashboard error-state screenshot: `issue-24-state-error.png` (missing-db "Something went wrong — The forecast database is missing", final subject); re-verified live headless on the final subject in #25 (wl25 §6). Note: `ac10_dashboard_error_missing_db.png` is the **#20-era** UI (superseded). audit 20/23/24; DR-19. |
| AC-11 | MVM | PASS | Ingestion on HTTP 401/404/5xx/timeout/non-JSON: clear error, non-zero exit, no DB write, no key. `test_fetch.py` (mock HTTP). audit 18. |
| **AC-12** | MVM | PASS | Every README step run in a clean 3.12.14 venv (create venv, `pip install`, ingestion real-fetch + offline rebuild reproducing committed `data.db`, `streamlit run app.py`, local Flask, `pytest` 152 passed, `smoke.py`). Full log wl25 §5. |
| **AC-13** | MVM | PASS | All artifacts under `home_work_01/` except the two RB-5 workflow files; PR #27 OPEN (SA-2). `git diff --name-only origin/main...HEAD` out-of-unit = only `.github/workflows/home_work_01-{ci,smoke}.yml`. Merge = acceptor RB-1 (not a completion condition). |
| **AC-14** | MVM | PASS | Documentation labeling — 8/8 PASS with README line citations; see §2 below. audit-level conclusion by Reviewer; this is the #25 self-check. |
| **AC-15** | MVM | PASS (audited preview); production PENDING-ACCEPTOR | `smoke.py` vs public **preview** alias (no login) — actual output in §8 (timestamp, URL, both status codes, `SMOKE PASS`, exit 0) with the served `data-deployment-id` matched to the final-subject commit's Vercel build. **Production-URL smoke after merge = release evidence (DR-12), pending-acceptor.** |
| AC-16 | MVM | PASS | `/api/health` 200 ok w/ 6/7/ingestion-time for a good snapshot; 503 w/ reason for missing/empty/incomplete. `test_dashboard.py` (health 200 + three 503). |
| AC-17 | ENHANCED | PASS | Map centered on Taiwan, six markers visible & zoomable; marker colours == shared-module band per selected day; click info card Region/Date/Min/Max/derived; 4-band legend w/ "derived" caveat; keyless basemap. Manual acceptance + shots `issue-24-map-*`, `issue-24-map-infocard-ac17.png`. audit 24. |
| AC-18 | ENHANCED | PASS | `Select Date` lists seven days ascending; switching recolours markers + updates info cards to that day's endpoint values (open popups refresh too — #24 F-1 fixed R2). shots `issue-24-map-date1/2-ac18.png`, `issue-24-f1-popup-updates-*`. audit 24 R2. |
| AC-19 | ENHANCED | PASS | R-EN-1 six items each PASS; desktop (≥1024) & 375px screenshots; 375px `scrollWidth == innerWidth` (375); loading/empty/error states each shot. shots `issue-24-desktop-ok-ac19.png`, `issue-24-mobile-375-ac19.png`, `issue-24-state-*`. audit 23/24. |
| AC-20 | ENHANCED | PASS | CI push run success, log shows Python 3.12.14 + pytest collecting derive/DB/shared/AppTest/Flask categories, 152 passed; path filter → out-of-unit push does not trigger. CI; audit 22 (run `35925410250`). |
| AC-21 | ENHANCED | PASS | Suite covers R-TC-1/3/4 items; passes with no network / no `.env` (clean-room 152 passed, BLOCKED_ATTEMPTS 0). tests; audit 22. |
| **AC-22** | ENHANCED | PASS ((a)+(b) pre-merge; (c) PENDING-ACCEPTOR) | Per **DR-18**: (a) local `smoke.py` PASS vs audited preview — actual output (timestamp, URL, two status codes, `SMOKE PASS`, exit 0) in §8; (b) smoke workflow deliverable reviewed — `on: workflow_dispatch`, URL from `HW01_DEPLOY_URL` var / `url` input, reuses `smoke.py`, no secret, min permissions, action skeleton green in CI; (c) live `workflow_dispatch` run = **release evidence, pending RB-1** (`gh api .../home_work_01-smoke.yml` = 404, not on `main`). audit 22; DR-18 §4. |
| **AC-23** | MVM | PASS | Local `python --version` 3.12.14 (wl25 §5); CI `home_work_01-ci.yml` `python-version: '3.12'`; Vercel `.python-version` = `3.12`. Vercel **build-log** confirmation = acceptor Vercel-dashboard item (RB-3, PENDING-ACCEPTOR). |
| AC-24 | MVM | PASS | Both layers show last ingestion time == db value (`2026-09-24T02:24:50+08:00`); `TemperatureForecasts` DDL unchanged. `AppTest`, `test_dashboard.py`, `/api/health` live (wl25 §6). DR-17. |
| **AC-25** | MVM | PASS | After ingestion, complete indented raw JSON in unit dir (no key); terminal prints fetch summary + 42-row preview; README documents F-D0047-091 structure + artifact locations. README "Observation artifacts" (lines 147–166) + "Response structure" block (line 152); wl25 §5. |
| AC-26 | MVM | PASS | `app.py` + imports carry no map/`Select Date`/folium; `requirements.txt` no folium (clean install had no folium). `test_static_checks.py`, `test_app.py`. Residual: INV-9 final self-check — see §3. |
| **AC-27** | MVM | PASS (self-check; Reviewer to conclude) | R-DOC-5 four items self-checked: modules/functions carry docstrings; errors handled w/ clear messages & JSON `error`; no dead code (placeholder CSS removed #24 R2); structure = shared module → API → frontend. audit 20/24 R2 gave (1)(3)(4) + (2). Reviewer gives the formal AC-27 conclusion. |
| AC-28 | ENHANCED | PASS | Derived Map Temperature + band cases: (20.1,25.2)→22.7; (19.9,20.0)→20.0 green; (24.9,25.0)→25.0 yellow; (29.9,30.0)→30.0 red; (15,24.8)→19.9 blue. `test_weather_query.py`. |
| AC-29 | ENHANCED | PASS | Workflow creation authorized (Outcome Contract §8.2 scoped RB-5, recorded audit 22 §1); workflows trigger only on `home_work_01/**` + self; names identify the unit. audit 22; DR-13. |
| **AC-30** | MVM | PASS | Deploy config + `requirements.txt` in `home_work_01/`; Vercel Root Directory = `home_work_01`; root has no unit config file. `git ls-files` (no root `vercel.json`/`requirements.txt`/`data.db`/`app.py`). **Root-Directory Vercel-dashboard screenshot = acceptor item (RB-3, PENDING-ACCEPTOR).** |

## 2. AC-14 documentation labeling — 8/8 PASS (README line citations)

Citations are line numbers in the final `home_work_01/README.md`.

| # | Item | Status | README citation |
| --- | --- | --- | --- |
| 1 | F-A0010-001 originally assigned + delisted (external constraint) | PASS | lines 23–26 ("Originally assigned dataset: CWA `F-A0010-001` … **CWA delisted it on 2026-07-01** … external constraint, not a project choice"). |
| 2 | F-D0047-091 is a compatibility replacement | PASS | lines 27–29 ("Compatibility replacement: CWA `F-D0047-091` … a **project compatibility decision**, not a teacher instruction"). |
| 3 | W1 window definition | PASS | lines 30–35 ("Forecast Day (W1 window) … **compatibility window, not a calendar day** … complete only when both periods are present"). |
| 4 | Mapping labeled project-defined (not CWA) | PASS | lines 36–46 ("Region mapping is **project-defined**, not an authoritative CWA grouping" + member-county table + verbatim `臺` note). |
| 5 | Region values labeled PROJECT-DERIVED COMPATIBILITY VALUES | PASS | lines 47–52 ("Region MinT / MaxT are `PROJECT-DERIVED COMPATIBILITY VALUES` … **never** a CWA-issued six-region forecast"). |
| 6 | Derived Map Temperature labeled derived | PASS | lines 273–278 ("**Derived Map Temperature** is a **derived value**: `(MinT + MaxT) / 2` … **not** an observed daily mean … legend states the 'derived, not observed' caveat"). |
| 7 | Streamlit positioning consistent with OC §2.4 | PASS | lines 192–203 ("required grading artefact … **not** the deployed runtime: the public deployment target (Vercel) cannot run a Streamlit server … a compatibility accommodation forced by that hosting constraint, **not** a sign that Streamlit was outside the assignment"). |
| 8 | Nowhere states region values are CWA-published / mapping is a CWA division | PASS | Reviewed entire README: lead sentence lines 3–6 ("**derived from CWA county-level open data** (not a CWA-published six-region product)"); lines 19–21, 51–52; map representative points lines 268–270 ("**not** a CWA-published location or boundary"). No reverse wording found. |

## 3. Invariants (INV-1 … INV-9) — final self-check

| INV | Status | Evidence |
| --- | --- | --- |
| INV-1 (single query semantics) | PASS | SQL only in `weather_query.py`; `app.py` + `server.py` call it; frontend calls only `/api/`. `test_static_checks.py`. Residual: `REGION_ORDER` duplicated in `ingestion/config.py` and `weather_query.py` with no cross-check test (#19 F-8, non-blocking; values currently agree). |
| INV-2 (behavioural equivalence) | PASS | All six Regions: Flask API series == shared module == 7 rows (wl25 §6, explicit comparison); Streamlit uses the same module; Dashboard MVM ≥ Grading App. `test_dashboard.py` INV-2 test. |
| INV-3 (snapshot exactly 6×7) | PASS | Committed `data.db`: 42 rows, 0 duplicate `(regionName,dataDate)`, never partial (single-transaction replace). `test_persist.py`; wl25 §6. |
| INV-4 (teacher names unchanged, H-2) | PASS | `app.py`, `data.db`, DDL verbatim, five columns, six Region names (`地區`, `臺`), `streamlit run app.py`, page text. Teacher SQL 6 & 7 on committed db. `test_persist.py`, `test_app.py`, `test_dashboard.py`. |
| INV-5 (zero key leak, H-1) | PASS | cred-scan (508 tracked files, no key, ignored `.env` excluded); `git ls-files` no `.env`; fixture/raw JSON/`doc/` evidence clean. Residual: `--env PATH` can read a key from outside the authorized location (#18 F-6, non-blocking, does not leak). |
| INV-6 (presentation layers never call CWA) | PASS | `test_static_checks.py` (no HTTP client, no CWA URL/key in Python; frontend only `/api/`). |
| INV-7 (labeling, H-3) | PASS | See §2 items 1–8; region values = project-derived, mapping = project-defined, Derived Map Temperature = derived. |
| INV-8 (Python 3.12 three places) | PASS | AC-23: local 3.12.14, CI `3.12`, Vercel `.python-version` `3.12`. |
| INV-9 (scope classes distinct) | PASS | ENHANCED (map, `Select Date`) only in Dashboard; Grading App MVM-only. `test_static_checks.py`, `test_app.py`. Residual: automated no-map check covers folium + literal `Select Date` (#19 F-5, non-blocking); manual + AppTest confirm no map elements. |

## 4. Acceptance-boundary coverage (AB-1 … AB-17)

| AB | AC(s) | Status | Note |
| --- | --- | --- | --- |
| AB-1 (public deployment + health) | AC-15, AC-16 | PASS (preview); production smoke PENDING-ACCEPTOR | Preview smoke green; production = release evidence (DR-12). |
| AB-2 (`streamlit run app.py`) | AC-01 | PASS | Headless boot + AppTest. |
| AB-3 (title + Select Region six) | AC-02 | PASS | Both layers. |
| AB-4 (chart + 7-row table) | AC-03 | PASS | Both layers, values == db. |
| AB-5 (single shared module, no CWA) | AC-04 | PASS | Static checks. |
| AB-6 (DDL + verification SQL) | AC-05 | PASS | Teacher SQL 6 & 7 on committed db. |
| AB-7 (idempotent 6×7 replace) | AC-06 | PASS | `test_persist.py`/`test_pipeline.py`. |
| AB-8 (credentials) | AC-07 | PASS | cred-scan + real fetch. |
| AB-9 (derivation positive + negative) | AC-08, AC-09 | PASS | `test_derive.py` incl. 5 negatives. |
| AB-10 (error states) | AC-10, AC-11, AC-16 | PASS | AppTest + Flask client + browser guard. |
| AB-11 (README run + observation) | AC-12, AC-25 | PASS | Clean-venv end-to-end run (wl25 §5). |
| AB-12 (all artifacts in unit) | AC-13 | PASS | Out-of-unit = workflow files only. |
| AB-13 (labeling) | AC-14 | PASS | §2, 8/8. |
| AB-14 (map / Select Date / Derived Map Temp) | AC-17, AC-18, AC-28 | PASS | audit 24; `test_weather_query.py`. |
| AB-15 (UI/UX quality) | AC-19 | PASS | audit 23/24 + screenshots. |
| AB-16 (tests + CI) | AC-20, AC-21 | PASS | CI 152 passed, offline. |
| AB-17 (deploy smoke) | AC-22 | PASS ((a)+(b)); (c) PENDING-ACCEPTOR | DR-18. |
| (OC §2.4 A2) | AC-23 | PASS | Python 3.12 three places. |
| (OC §2.5 brief §6.7) | AC-24 | PASS | Ingestion time both layers. |
| (OC §2.2/§2.4 A3) | AC-26 | PASS | Grading App MVM-only. |
| (OC §2.1 code quality) | AC-27 | PASS (self-check) | Reviewer concludes. |
| (OC §4 RB-5) | AC-29 | PASS | Scoped workflow authorization. |
| (OC §2.5 brief §6.3) | AC-30 | PASS | Deploy config in unit; Vercel Root-Directory shot = acceptor item. |

All seventeen AB items are covered by at least one PASS criterion (the two AC-22(c) /
AC-15-production items are post-merge release evidence, per DR-12/DR-18, not gaps).

## 5. Acceptor-deferred / post-merge items (NOT failures, NOT completion conditions)

Per governance §3.8 (run completion, work-item completion, phase acceptance and release
authorization are stated separately) and DR-12/DR-18:

1. **AC-22(c)** — live `workflow_dispatch` smoke run URL + two status codes. The smoke
   workflow is not on the default branch (`main`) before the reserved merge (RB-1), so
   GitHub cannot dispatch it pre-merge (`gh api …/home_work_01-smoke.yml` = 404). After
   merge, the default dispatch uses `HW01_DEPLOY_URL` (production) and is **release
   evidence** (DR-18 (c)). Owner: acceptor (RB-1), or an agent under direct acceptor
   instruction as a post-run Lightweight item.
2. **AC-15 production URL smoke** — `GET /` + `/api/health` against
   `https://aiot-hw01-weather.vercel.app` after merge (production updates only on merge).
   Release evidence (DR-12). Owner: acceptor.
3. **#21 F-3 Vercel-dashboard items** (RB-3, acceptor-only): (a) build-log confirmation
   that Vercel used Python 3.12 (completes AC-23's third place beyond the committed
   `.python-version`); (b) Root-Directory = `home_work_01` dashboard screenshot (AC-30);
   (c) confirmation that no CWA key is set in the Vercel project env (AC-07(e)). These are
   settings/logs in the acceptor's Vercel account, outside agent authority.

The A-6 release gate material (`doc/acceptance/`) comprises: this document; the teacher
SQL result on `data.db` (6 & 7, wl25 §6); the latest green CI run (152 passed, Python
3.12.14). The three items above are listed for the acceptor to produce at release.

## 6. Known residual non-blocking items (tracked, none block closure)

Consolidated from the closed per-ticket audits **and the #25 R1 audit**
(`issue-25-c1-r1.md`). All are non-blocking; owners/dispositions as recorded. Only trivial
documentation/record items were fixed in #25; code/UI residuals are recorded here as known
non-blocking (feature/UI/behaviour code change is out of #25 scope).

| ID | Item | Severity | Disposition |
| --- | --- | --- | --- |
| #22 F-1 | README + smoke-workflow comment implied pre-merge dispatch | Low (doc) | **FIXED in #25** — README CI paragraph + `home_work_01-smoke.yml` header comment corrected per DR-18 §4.6. |
| #18 F-11 | README lead sentence could read as CWA-published six-region forecast | Low (doc) | **FIXED in #25** — lead sentence now "derived from CWA county-level open data (not a CWA-published six-region product)". |
| #25 F-8 | unused `import json` in `tests/test_fetch.py` | Low | **FIXED in #25** — import removed; `test_fetch.py` 13 passed. |
| #20 F-7 / #25 F-5 | stale README scope note + "later ENHANCED dashboard work" wording (ENHANCED is done; Leaflet is vendored JS, not a Python dep) | Low (doc) | **FIXED in #25** — README "Scope" note updated to say CI + deployment are documented here; the map-library exclusion note reworded to "the map dashboard's vendored JS libraries are not Python dependencies". |
| **#18 R2 N-1** | **offline ingestion (`--acquired-at` / sidecar path) does not validate the acquisition-time format — a malformed value (e.g. `--acquired-at yesterday`) is accepted and written to `IngestionMetadata.ingestedAt`** (R-DB-5, DR-17) | **Medium** | **NOT fixed here (touches the high-risk H-3/DR-17 ingestion path — out of #25's doc-only scope).** Owner = **new post-#25 Lightweight follow-up work item**; because it touches a high-risk area it **requires an independent audit under decision A-4**. Orchestrator to assign the owner (the item had no owner after #25 closes). Fail-closed today: the value is written verbatim, no crash. |
| #18 R2 N-2 | test-only constant clock (T-1) cannot detect an online "re-read clock" regression | Low | Test-double improvement only; behaviour is correct by design (DR-17). No change. |
| #18 R2 N-3 | AC-06 date-transform test rotates rather than week-shifts; a helper docstring mismatches its implementation | Low | Semantics verified by Reviewer; optional test/docstring cleanup. |
| #18 R2 N-4 | when raw JSON and sidecar are both absent, the error message mentions only the missing provenance | Low | Fail-closed (exit 1, no DB write); optional message wording. |
| #18 R2 N-5 | an online run that fails in derive leaves a freshly fetched raw JSON + sidecar in the tree while `data.db` keeps the old snapshot (README lacks a "do not commit `data/raw/` after a failed online run" caution) | Low | Optional README caution; tracked, no code change in #25. |
| #18 R1 F-9 / #25 F-7 | worklog did not paste the AC-25 terminal output | Low (record) | **FIXED in #25** — the ingestion fetch summary + 42-row derived preview pasted into worklog §5a. |
| #19 R1 F-6 | AC-03 test does not directly assert the chart carries seven dates | Low | Chart x-axis is the seven Forecast Days (AppTest spec + desktop screenshot); optional explicit assertion. |
| #19 R1 F-10 | `pandas` used by `app.py` but not declared in `requirements.txt` (transitive via streamlit) | Low | Present transitively (streamlit → pandas 3.0.6, confirmed in the clean install); optional explicit pin. |
| #20 R1 F-4 | data-endpoint 503 test not parametrized across empty/incomplete | Low | health 503 covered for missing/empty/incomplete; data-endpoint 503 covered for missing. Optional parametrization. |
| #21 R2 N-1 | (tracked in `issue-21-c1-r2.md`) | Low | Recorded in the #21 audit; no #25 action. |
| #22 F-2 | CI push `paths` filter — platform edge case may trigger without unit change | Low | Config review; GitHub path-filter semantics accepted. Owner tracked; no code change. |
| #22 F-3 | credential scanner coverage edge cases | Low | Does not affect current result (cred-scan clean). Owner #22; no change needed now. |
| #24 F-4 | static CWA-URL/key scan does not recurse `static/vendor/` | Low | Vendored Leaflet has no CWA URL/key; recursion + attribution-URL allowlist is optional hardening. |
| #24 F-5 | 375px east-marker popup clipping / sidebar reset / south outline | Low | Map UX detail; no contract clause violated. |
| #24 F-6 | `Select Date` label has no automated regression test | Low | Optional one-line assertion. |
| #24 F-3 | `/api/days/<date>` out-of-order responses could apply a stale day | Medium | **Addressed R2** (stale-day responses dropped, #24 commit 386f30a); low-probability, deploy-only. |
| #19 F-8 | `REGION_ORDER` duplicated (`ingestion/config.py` vs `weather_query.py`), no cross-check test | Low | Values currently agree; optional equality test. |
| #19 F-9 | chart Y-axis has no title/unit | Low | Cosmetic; SHOULD (DR-15) not violated. |
| #19 F-5 | no-map automation covers folium + literal `Select Date` only | Low | Manual + AppTest confirm no map in Grading App (INV-9). |
| #20 F-3 | non-SQLite `data.db` / undefined `/api/` path returns HTML 500/404 (not JSON) | Low | Prepared snapshot is valid SQLite; JSON error handler for `/api/` is optional hardening. |
| #20 F-5 | weak automated regression for visible page text | Low | `<title>` tested; #23/#24 preserve R-EN-2 strings. |
| #20 F-6 | local Flask loads `home_work_01/.env` if `python-dotenv` is installed | Low | `python-dotenv` not in `requirements.txt`, so not loaded in the documented setup (boot log confirms the Tip). Optional `load_dotenv=False` hardening. |
| #18 F-3/F-4/F-5/F-6 | `NaN`/`Infinity` decimal edge, some traceback error paths, defensive unreachable code, `--env PATH` scope | Low | All fail-closed (no DB write, non-zero exit); outside CWA numeric space / not in AC-11 enumerated modes. |

## 8. AC-15 / AC-22(a) deployment smoke evidence (OC AB-1, DR-18 §4.1)

`smoke.py` run against the public branch **preview** alias (no login), with the served
`data-deployment-id` matched to the final-subject commit's Vercel build:

```
$ python smoke.py https://aiot-hw01-weather-git-homework01-hw10-im-8efc12-nchu-aiot-class.vercel.app
[2026-09-24T02:47:42Z] attempt 1  url=https://aiot-hw01-weather-git-homework01-hw10-im-8efc12-nchu-aiot-class.vercel.app  GET / -> 200  GET /api/health -> 200  (0.9s elapsed)  PASS
[2026-09-24T02:47:42Z] SMOKE PASS  url=https://aiot-hw01-weather-git-homework01-hw10-im-8efc12-nchu-aiot-class.vercel.app  (0.9s)
exit: 0
```

- **URL**: `https://aiot-hw01-weather-git-homework01-hw10-im-8efc12-nchu-aiot-class.vercel.app`
- **GET /** → **200** (body contains `Taiwan Weather Forecast`); **GET /api/health** → **200** (`status: "ok"`, 6 regions, 7 days).
- **Deployment ↔ commit**: the alias served `data-deployment-id="dpl_5geV9Trc3cX1WGZiRKg1oNEHSqqZ"`, which is
  GitHub deployment `6629046658` for commit **`6407d8b`** (Preview) —
  confirmed via `curl <alias>/` and `gh api repos/…/deployments`. The final subject
  `6407d8b2d0f04523f5057b0880083f3bd836c6a8` is a documentation-only delta over `6407d8b` (no
  `app.py`/`server.py`/`weather_query.py`/`data.db`/`static/*` change), so the deployed
  dashboard build is byte-identical.
- **AC-22(a)** uses this same output (DR-18 §4.1). **AC-22(c)** live `workflow_dispatch`
  run and the **production**-URL smoke (AC-15) remain post-merge release evidence
  (DR-18 (c), DR-12) — see §5.
- Reviewer independently reproduced the preview smoke in the #25 R1 audit
  (`issue-25-c1-r1.md` §1.8), matching the alias deployment to the audited commit.

## 7. Cross-reference

- Worklog: `doc/governance/worklog/issue-25.md`.
- Per-ticket audit records: `doc/governance/audit/issue-{18,19,20,21,23,24}-c1-{r1,r2}.md`,
  `issue-22-c1-r1.md`; #25's forthcoming record.
- Decisions: `doc/governance/decisions/` (derivation-SPEC.md; DR-1..DR-19; high-risk
  A-1/A-2/A-6; ingestion-timestamp DR-17; dashboard-state DR-19; unattended-run-policy).
- Screenshots: `doc/acceptance/screenshots/`.
