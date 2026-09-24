# Worklog — Issue #25: Integration / Final Verification (`home_work_01`)

Formal lane. This ticket adds **no new MVM/ENHANCED feature**: it does the README
end-to-end run (AC-12), acceptance documentation (R-DOC-4), final verification of the
integrated subject, and prepares the Spec Integration Audit subject.

## 1. Contract reference

- **Ticket**: GitHub Issue #25 (`yotsubamomo/aiot-classwork`) — INTEGRATION / FINAL
  VERIFICATION (acceptor 2026-09-24 reclassification). Blocked by #22, #24 (both closed).
- **Spec**: `home_work_01/doc/spec/SPEC.md` v1.1 — §1.10 (R-DOC-1..5), R-ENV-1/2, R-DS-9,
  R-TC-7; §2 all AC; §3 INV-1..9; §6, §7. New ACs: AC-12, AC-13, AC-14, AC-15, AC-22,
  AC-23, AC-25, AC-27, AC-30; re-verify AC-02, AC-03, AC-04, AC-07, AC-10, AC-19, AC-24.
- **Decisions (authoritative)**: high-risk A-1/A-2/A-6; DR-6, DR-12; **DR-18** (AC-22
  (a)+(b) = verified pre-merge, (c) live `workflow_dispatch` = post-merge release
  evidence); DR-19; DR-17; unattended-run-policy.
- **Authorization**: Outcome Contract ACCEPTED 2026-09-23; SA-1 (commit+push topic
  branch), SA-2 (PR to `main`). RB-1 merge / RB-2 submit / RB-3 Vercel & repo vars /
  RB-5 out-of-unit files stay reserved.

## 2. Executing role and binding reference

- Role: `gov-executor` (Bindings §3.1: `claude-opus-4-8`, effort `high`). Binding
  verification per Bindings §3.4 is recorded by the dispatcher in the run record; this
  worklog records the work and evidence.

## 3. Subject identity

- **Branch**: `home_work_01-hw10-implementation`.
- **BASE for #25**: `2f52766c32412cc6cb7e1719a8ab0ce8a8e0c53d` (HEAD after #24 close).
- **Final subject for the Spec Integration Audit**: `__FINAL_SHA__` — **the commit that
  INCLUDES `home_work_01/doc/acceptance/ACCEPTANCE.md`** (the R-DOC-4 deliverable) and this
  worklog. **Correction of the earlier error (R1 F-3)**: per Bindings §7 **only
  `doc/governance/**` paths are record-only**, so `doc/acceptance/` is part of the subject
  and the final subject is NOT `fafcf2f` (which lacked ACCEPTANCE.md). The app / query /
  db / static / test behaviour is identical to `2f52766` — the whole #18–#25 delta over the
  #24-closure subject `386f30a` that is not `doc/governance/**` is: `README.md`,
  `requirements.txt` (comment), `.github/workflows/home_work_01-smoke.yml` (comment),
  `tests/test_fetch.py` (unused-import removal), and `doc/acceptance/ACCEPTANCE.md`; no
  `app.py`/`server.py`/`weather_query.py`/`data.db`/`static/*` behaviour change.
- **CI green** on the final subject: run `__FINAL_CI__` (152 passed, Python 3.12.14,
  credential scan passed) — see §6.
- **Correction history**: `fafcf2f` (initial #25 doc fixes) → `1396226`/`a571ccc` (initial
  ACCEPTANCE.md + worklog, R1-audited subject) → this targeted correction (R1 F-1..F-8).

## 4. Decisions and assumptions

- **R-DB-6 (do not destabilize the deployed snapshot)**: the committed
  `home_work_01/data.db` is the prepared-snapshot deliverable and is what the live
  Vercel deployment serves. For AC-12 I demonstrated ingestion **without** replacing it:
  (i) offline rebuild from the committed raw JSON reproduces the committed `data.db`
  exactly (determinism); (ii) a real online fetch runs successfully, written only to a
  scratch/observation path. No new `data.db` was committed. `sha256(data.db)` unchanged
  (`9bbf05bc6cc803444c8760432d6b484699c597f751fa16cb58bfbb5a0dbf542b`).
- **AC-22 (DR-18)**: (a) local `smoke.py` PASS against the audited public preview +
  (b) workflow deliverable = verified pre-merge; (c) live `workflow_dispatch` run =
  post-merge release evidence. `home_work_01-smoke.yml` is still 404 on `main` (not on
  the default branch), so (c) is impossible pre-merge and is recorded as pending-acceptor.
- **AC-15 production URL** (DR-12) and **#21 F-3 Vercel-dashboard screenshots / build-log
  / "no CWA key in Vercel env"** (RB-3): acceptor-deferred / post-merge release items.
- **Documentation-only fixes (in scope, no feature/code change)**: corrected the README
  CI paragraph and the `home_work_01-smoke.yml` header comment so neither implies the
  smoke workflow can be dispatched before the merge to `main` (DR-18 §4.6, #22 F-1); and
  the README lead sentence so it does not read as a CWA-published six-region forecast
  (#18 F-11). All other residuals are recorded as known non-blocking (see ACCEPTANCE.md).

## 5. Work performed — AC-12 README end-to-end run (clean Python 3.12 venv)

Ran every README instruction in a **fresh, clean Python 3.12.14 venv** (created from the
uv-managed CPython 3.12.14, isolated in the session scratchpad so the committed snapshot
is untouched). Date of run: **2026-09-24**.

| # | README step | Command | Result |
| --- | --- | --- | --- |
| 1 | Create venv | `python -m venv .venv` (clean 3.12.14) | OK — Python 3.12.14 (AC-23 local place 1) |
| 2 | Install deps | `pip install -r requirements.txt` | OK — Flask 3.1.2, pytest 8.3.3, streamlit 1.64.0, requests 2.32.3, pandas 3.0.6 (transitive via streamlit); no folium (AC-26) |
| 3 | Ingestion offline rebuild | `python -m ingestion --from-json data/raw/F-D0047-091.json --db <scratch>/rebuilt.db` | OK exit 0 — 42 rows; `TemperatureForecasts` **and** `IngestionMetadata` content **identical** to committed `data.db` (determinism, R-DB-6) |
| 4 | Ingestion real fetch | `python -m ingestion --raw-out <scratch>/live_raw.json --db <scratch>/live.db --env .env` | OK exit 0 — fetched F-D0047-091 (22 counties, 15 elements, 14 periods), 42-row preview printed; committed `data.db` sha256 **unchanged**; scratch raw JSON has 0 Authorization/key matches (AC-07(a)) |
| 5 | Grading App | `streamlit run app.py --server.headless true` | OK — Uvicorn started, `GET /` 200, no exception in log (AC-01) |
| 6 | Local Flask dashboard | `python server.py` | OK — `GET /` 200 contains `Taiwan Weather Forecast`; `/api/health` 200 `status:ok`, 6 regions, 7 days, ingestion `2026-09-24T02:24:50+08:00`; `/api/regions` 200 six regions in fixed order |
| 7 | Tests | `pytest` | OK — **152 passed** in the clean offline venv (7.54s) |
| 8 | Deploy / smoke | `python smoke.py <preview-alias>` | OK — `GET /` 200, `/api/health` 200, `SMOKE PASS`, exit 0, 6.5s (AC-15/AC-22(a)) |

README↔poster `HW10_Weather/` mapping table is complete (README "Correspondence to the
poster `HW10_Weather/` structure"): `fetch_weather.py`→`ingestion/fetch.py`,
`parse_weather.py`→`ingestion/derive.py`, `database.py`→`ingestion/persist.py`, runner
→`ingestion/pipeline.py`, `data.db`, `requirements.txt`, `README.md`, `app.py`,
deployed web app→`server.py`+`static/`+`api/index.py`+`vercel.json`, `weather_data.csv`
not used.

Note (local Flask + `.env`, #20 F-6): the boot log shows `Tip: There are .env files
present. Install python-dotenv to use them.` — `python-dotenv` is **not** in
`requirements.txt`, so the key is **not** loaded by the local dashboard process.
Recorded as a Low non-blocking hardening item.

### 5a. AC-25 observation terminal output (F-7; #18 F-9 owner #25) — no key

Online fetch summary (real fetch to a scratch path, 2026-09-24; key never printed):

```
Fetch summary (F-D0047-091):
  counties: 22
  weather elements (15): 平均溫度, 最高溫度, 最低溫度, 平均露點溫度, 平均相對濕度, 最高體感溫度,
    最低體感溫度, 最大舒適度指數, 最小舒適度指數, 風速, 風向, 12小時降雨機率, 天氣現象, 紫外線指數,
    天氣預報綜合描述
  periods per temperature element: 14
```

Derived 42-row snapshot preview (offline rebuild from the committed raw JSON,
`python -m ingestion --from-json data/raw/F-D0047-091.json`):

```
Derived Forecast Snapshot preview:
  regionName dataDate       mint   maxt
  北部地區       2026-09-24     23.3   31.0
  北部地區       2026-09-25     23.4   31.4
  北部地區       2026-09-26     24.1   31.4
  北部地區       2026-09-27     24.1   31.6
  北部地區       2026-09-28     24.4   32.4
  北部地區       2026-09-29     25.3   30.9
  北部地區       2026-09-30     24.6   30.3
  中部地區       2026-09-24     24.8   32.8
  中部地區       2026-09-25     24.5   32.8
  中部地區       2026-09-26     24.5   33.0
  中部地區       2026-09-27     24.7   32.8
  中部地區       2026-09-28     24.8   32.8
  中部地區       2026-09-29     25.3   32.0
  中部地區       2026-09-30     24.3   29.8
  南部地區       2026-09-24     26.3   32.0
  南部地區       2026-09-25     26.3   32.3
  南部地區       2026-09-26     26.3   32.7
  南部地區       2026-09-27     26.3   32.7
  南部地區       2026-09-28     26.3   32.7
  南部地區       2026-09-29     25.7   32.0
  南部地區       2026-09-30     25.7   29.3
  東北部地區      2026-09-24     23.0   30.0
  東北部地區      2026-09-25     23.0   32.0
  東北部地區      2026-09-26     24.0   32.0
  東北部地區      2026-09-27     24.0   31.0
  東北部地區      2026-09-28     24.0   31.0
  東北部地區      2026-09-29     24.0   29.0
  東北部地區      2026-09-30     24.0   30.0
  東部地區       2026-09-24     24.0   30.0
  東部地區       2026-09-25     24.0   31.0
  東部地區       2026-09-26     25.0   31.0
  東部地區       2026-09-27     25.0   31.0
  東部地區       2026-09-28     25.0   32.0
  東部地區       2026-09-29     25.0   30.0
  東部地區       2026-09-30     25.0   30.0
  東南部地區      2026-09-24     24.0   31.0
  東南部地區      2026-09-25     25.0   31.0
  東南部地區      2026-09-26     25.0   31.0
  東南部地區      2026-09-27     25.0   32.0
  東南部地區      2026-09-28     25.0   33.0
  東南部地區      2026-09-29     25.0   31.0
  東南部地區      2026-09-30     25.0   30.0
  rows: 42 | regions: 6 | date range: 2026-09-24 .. 2026-09-30
```

### 5b. AC-15 / AC-22(a) deployment smoke output (F-1) — recorded in ACCEPTANCE.md §8

```
$ python smoke.py https://aiot-hw01-weather-git-homework01-hw10-im-8efc12-nchu-aiot-class.vercel.app
__SMOKE_LINE_1__
__SMOKE_LINE_2__
exit: 0
```

Deployment ↔ commit: the alias served `data-deployment-id="__DPL_ID__"` = GitHub
deployment `__GH_DEPLOY_ID__` for commit `__DEPLOYED_SHA__` (Preview); the final subject
`__FINAL_SHA__` is a documentation-only delta over `__DEPLOYED_SHA__`, so the deployed
build is byte-identical. Full detail + AC-22(a) in ACCEPTANCE.md §8.

## 6. Verification — final integrated subject

**Subject**: `__FINAL_SHA__` — app / query / db / static / test behaviour identical to
`2f52766`; the whole #25 delta is documentation wording (README, requirements.txt comment,
smoke-workflow header comment), a test-only unused-import removal (`tests/test_fetch.py`),
and `doc/` records incl. `doc/acceptance/ACCEPTANCE.md`. No `app.py`/`server.py`/
`weather_query.py`/`data.db`/`static/*` behaviour change.

- **Full offline pytest**: 152 passed (clean venv, no network, no `.env`). Per-file:
  test_derive 19, test_persist 5, test_weather_query 29, test_app 9, test_dashboard 23,
  test_static_checks 22, test_fetch 13, test_pipeline 19, test_secrets 4,
  test_vercel_path_decoding 9.
- **INV-2 two-layer equivalence**: for all six Regions, Flask API `/api/regions/<r>/series`
  == `weather_query.region_series(r)` (7 rows each, identical). Grading App uses the same
  shared module. → INV-2 holds.
- **H-2 teacher SQL on committed `data.db`**: `SELECT DISTINCT regionName` → **6**
  (北部/中部/南部/東北部/東部/東南部 地區); `WHERE regionName='中部地區'` → **7**. DDL
  verbatim; 42 rows; 0 duplicate `(regionName,dataDate)`; all `dataDate` are `YYYY-MM-DD`.
- **INV-3**: `TemperatureForecasts` = 42 rows, no partial write, no duplicates.
- **INV-4 (H-2)**: six Region names carry `地區` and use `臺`; `app.py`, `data.db`,
  DDL, five column names, `streamlit run app.py`, page text unchanged.
- **AC-07 credentials**: (a) real fetch succeeded, no key in output; (b) `git ls-files`
  tracks only `home_work_01/.env.example`, no `.env`; (c) `python -m tools.credential_scan`
  = passed (508 tracked files, no CWA-key-format string in tracked files/history,
  ignored `.env` excluded); (d) fixture & saved raw JSON hold no `Authorization`;
  (e) Vercel needs no env var/secret (documented; acceptor RB-3); (f) `doc/` evidence
  scanned — 0 key-format strings.
- **AC-23 Python 3.12 three places**: local `python --version` 3.12.14; CI
  `home_work_01-ci.yml` `python-version: '3.12'`; Vercel `.python-version` = `3.12`.
- **AC-22 (DR-18)**: (a) local smoke PASS (above) + (b) workflow deliverable reviewed
  (YAML parses, `on: workflow_dispatch`, URL from `HW01_DEPLOY_URL` var / `url` input,
  reuses `smoke.py`, no secret, min permissions; action skeleton proven green by CI on
  the same subject); (c) `gh api .../actions/workflows/home_work_01-smoke.yml` = **404**
  (not on `main`) → release evidence, pending RB-1.
- **AC-19 final Dashboard (with map)**: ENHANCED manual acceptance carried by #23/#24
  audits (screenshots `issue-24-*` desktop/mobile/map/states); re-confirmed the integrated
  page boots and serves the map data endpoints.
- **AC-10 (DR-19, F-6)**: re-verified the Dashboard error state live/headless on the final
  subject — `create_app(db_path=<missing>)`, `GET /api/health` → 503 "database is missing",
  and the page rendered the red error card "Something went wrong — The forecast database is
  missing. Run the ingestion pipeline to create it." (matches the committed final-UI
  screenshot `issue-24-state-error.png`, from 386f30a; the older `ac10_dashboard_error_missing_db.png`
  is the #20-era UI). ACCEPTANCE.md AC-10 row references `issue-24-state-error.png` + DR-19.
- **AC-15 / AC-22(a) smoke** (F-1): actual output + deployment↔commit mapping recorded in
  §5b above and ACCEPTANCE.md §8.
- **AC-13/AC-30 placement**: all artifacts under `home_work_01/` except the two RB-5
  workflow files (`.github/workflows/home_work_01-{ci,smoke}.yml`); root has no unit
  config; PR #27 OPEN (`home_work_01-hw10-implementation` → `main`).

## 7. Artifacts (this ticket)

- `home_work_01/doc/acceptance/ACCEPTANCE.md` (new, R-DOC-4).
- `home_work_01/README.md` (doc-only wording fixes: lead sentence; CI dispatch paragraph).
- `.github/workflows/home_work_01-smoke.yml` (header comment doc-only fix; `on:`/steps
  unchanged — RB-5 maintenance).
- This worklog.

## 8. Audit status

- Per-ticket independent audits (Formal, MUST) — all closed:

  | Ticket | R1 subject / verdict | R2 subject / verdict | Records |
  | --- | --- | --- | --- |
  | #18 | `693c12b` BLOCKING (F-1,F-2) | `7ee299c` closure | `audit/issue-18-c1-r1.md`, `-r2.md` |
  | #19 | `353c8a7` BLOCKING (F-1,F-2,F-3) | `0672020` closure | `audit/issue-19-c1-r1.md`, `-r2.md` |
  | #20 | `72ff874` BLOCKING (F-1) | `0f5f00e` closure | `audit/issue-20-c1-r1.md`, `-r2.md` |
  | #21 | (R1) BLOCKING (F-1) | `f02a1df` closure | `audit/issue-21-c1-r1.md`, `-r2.md` |
  | #22 | `84060c9`/`88b871e` CLOSURE (no blocking; AC-22 per DR-18) | — (no R2) | `audit/issue-22-c1-r1.md` |
  | #23 | `610a797` BLOCKING (F-1,F-2) | `fd654f3` closure | `audit/issue-23-c1-r1.md`, `-r2.md` |
  | #24 | `4ec20b5` BLOCKING (F-1,F-2) | `386f30a` closure | `audit/issue-24-c1-r1.md`, `-r2.md` |

- **Issue #25 independent audit**: cycle 1 R1 = **BLOCKING (F-1, F-2, F-3)** — all
  documentation/record findings; the product passed the Reviewer's independent checks
  (`audit/issue-25-c1-r1.md`). This worklog update is the **targeted correction** (governance
  §4.4): F-1 (smoke output + deployment↔commit mapping recorded), F-2 (AC-07 (e) split;
  "no key in Vercel env" = PENDING-ACCEPTOR), F-3 (final subject = the commit incl.
  ACCEPTANCE.md), plus non-blocking F-4..F-8. R2 closure review to follow.
- **Spec Integration Audit** (Formal, MUST, governance §4.7): forthcoming on the final
  integrated subject; A-2 requires it to check INV-3/4/5/7 and run the teacher SQL on
  `data.db`. Subject-prep is §9 below.

## 9. Spec Integration Audit subject prep (impl-default §6)

- **Final subject identity**: branch `home_work_01-hw10-implementation`, commit
  `__FINAL_SHA__` — **the commit that includes `doc/acceptance/ACCEPTANCE.md`** (R-DOC-4).
  Per Bindings §7 only `doc/governance/**` is record-only, so `doc/acceptance/` is part of
  the subject. App/query/db/static/test behaviour == `2f52766` (== #24-closure `386f30a`);
  the delta is documentation + a test-only unused-import removal.
- **All Ticket audit records**: `doc/governance/audit/issue-18-c1-{r1,r2}.md`,
  `issue-19-c1-{r1,r2}.md`, `issue-20-c1-{r1,r2}.md`, `issue-21-c1-{r1,r2}.md`,
  `issue-22-c1-r1.md`, `issue-23-c1-{r1,r2}.md`, `issue-24-c1-{r1,r2}.md`,
  `issue-25-c1-r1.md` (+ the #25 R2 closure record to follow).
- **Integration evidence**: this worklog §5–§6 (incl. §5a AC-25 output, §5b smoke);
  `doc/acceptance/ACCEPTANCE.md` (AC-01..30, INV-1..9, AB-1..17 with evidence refs, §8 smoke
  evidence); CI run `__FINAL_CI__` (152 passed); screenshots under
  `doc/acceptance/screenshots/`.
- **Decisions in force**: derivation-SPEC.md; DR-1..DR-19; high-risk A-1/A-2/A-6;
  unattended-run-policy.

## 10. Remaining work / unresolved concerns

- **Acceptor-deferred (post-merge release evidence, NOT completion conditions)**:
  AC-22(c) live `workflow_dispatch` run (DR-18); AC-15 production-URL smoke (DR-12);
  #21 F-3 Vercel-dashboard items (build-log Python 3.12 confirmation, Root-Directory
  screenshot, "no CWA key set in the Vercel project env") — RB-3.
- **RB-1 merge, RB-2 submit** remain acceptor actions.
- Known non-blocking code residuals: consolidated in ACCEPTANCE.md "Known residual
  non-blocking items"; none block closure.
- No BLOCKED path. No semantic/boundary doubt encountered.
