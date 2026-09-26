# Acceptance document V2 — HW01 Weather Map V2 (`home_work_01`)

Derived contract: [`doc/spec/SPEC-V2.md`](../spec/SPEC-V2.md) **v2.2** (Delta Spec, inherits V1 Spec
v1.1 by reference; §5.3 annotation figures as corrected by DV-23, commit `2771a54`). This document is
the V2 acceptance document required by **R-V2-DOC-3**: for every acceptance criterion **AC-V2-01 …
AC-V2-23** and every row of the Spec **§6.3 targeted V1 revalidation** it records the status, the
verification method and the evidence reference. The evidence was produced by the closed Tickets
**#35–#40** and is **aggregated here by reference, not redone**; Issue **#41** (integration / final
verification) added only the final-subject checks named in §0.3. It is an entry point for the
forthcoming **Spec Integration Audit** (governance §4.7) and is **not** itself an independent audit.
The V1 acceptance document [`ACCEPTANCE.md`](ACCEPTANCE.md) stays as it was (it gains only a pointer
to this file).

## 0. Subject, environment, status legend, evidence shorthand

### 0.1 Subject

- **Branch** `home_work_01-v2-implementation`; V2 run BASE `08e158e` (= `main` with V1 merged; the V1
  closed implementation is the squash merge `ef15d3e`, an ancestor of every V2 commit).
- **#41 BASE** `df78e79` (the commit that advanced the run to #41). **#41 code/doc anchor**
  `49dac12` (README final review + the browser-check de-flake, §0.3); the commit that adds this file
  and the #41 final-subject evidence (`doc/acceptance/`) is a documentation-only superset of `49dac12`
  (no `app.py`, `server.py`, `observation.py`, `representative.py`, `radar.py`, `weather_query.py`,
  `data.db`, `static/`, `api/` or test change). Per Bindings §7 only `doc/governance/**` is
  record-only, so `doc/acceptance/` (this file) is part of the subject. The **final subject** named for
  the Spec Integration Audit is the branch commit that contains this file; the worklog
  ([`issue-41.md`](../governance/worklog/issue-41.md)) records its SHA, its CI run and its preview smoke.
- **Per-ticket closed code anchors** (all audited, run record
  [`run-20260925-hw01-v2-formal.md`](../governance/run/run-20260925-hw01-v2-formal.md)): #35 `5f0dbc3`,
  #36 `f63ebb1`, #37 `7a3b469`, #38 `286ee9d`, #39 `f3bf245`, #40 `fedffdd`.

### 0.2 Environment

Windows 11; `home_work_01/.venv` Python **3.12.14**; Chrome headless over the DevTools protocol
(`websocket-client`) for the browser checks; CI = GitHub Actions `home_work_01-ci.yml` (ubuntu,
Python 3.12). Committed `data.db` sha256
`9bbf05bc6cc803444c8760432d6b484699c597f751fa16cb58bfbb5a0dbf542b` (= V1, git blob `6875869`).

### 0.3 What #41 ran on the final subject (the rest is by reference)

| Check | Result | Evidence |
| --- | --- | --- |
| Offline suite `python -m pytest -q` | **614 passed** (local, `49dac12`) | wl41 V-1 |
| CI on `49dac12` | run **`36231516727`** success | wl41 V-2 |
| Test ids: V1 closed `ef15d3e` 259, BASE `08e158e` 259, #40 `fedffdd` 614 → all present at HEAD (614) | 0 missing | wl41 V-3 |
| Blob / diff vs V1 closed `ef15d3e`: `app.py`, `weather_query.py`, `ingestion/`, `data.db`, `data/raw/`, `requirements.txt`, `smoke.py`, `vercel.json`, workflows | identical blobs / trees | wl41 V-4 |
| Forecast `/api/` responses, V1 `ef15d3e` server vs final server, network blocked, no key, 4 DB states × 18 forecast paths | **72 pairs, 0 byte differences** | wl41 V-5 |
| Teacher SQL on committed `data.db` | SQL 1 → 6 rows; SQL 2 → 7 rows; 42 rows, 0 duplicates; DDL verbatim | wl41 V-6 |
| All six browser checks on the final code | see §0.4 | ev41 |
| Credential scan, `git ls-files` no `.env`, key literal absent from diff | passed | wl41 V-8 |
| README install and run steps, clean venv | recorded | wl41 V-9 |
| Vercel preview of `49dac12` (no login), smoke, deployment ↔ commit | **SMOKE PASS**; `dpl_GBZ1di8wdyraABA3n8VqU5R7d2o7` ↔ GitHub deployment `6676924592` (sha `49dac12`) | §6 |

### 0.4 Final-subject browser checks (#41 re-run, code = `49dac12`)

All six browser checks, unmodified except the #36 check's clock (§8, a38-r2 N-1), were re-run
against the final code (`static/`, `server.py`, `observation.py`, `radar.py` sha256-identical before
and after the runs), writing to a scratch directory; the results and network logs are copied to ev41
(the ticket evidence directories were **not** regenerated).

| Check | Owner | Result on the final code | ev41 file |
| --- | --- | --- | --- |
| `check_modes_browser.py` | #36 | **37/37**, then **5 further runs 37/37** (6/6 — the a38-r2 N-1 flake no longer occurs) | `final-check-modes-results.json`, `…-repeat{1..5}-results.json`, `final-check-modes-network-log.json` |
| `check_refresh_browser.py` | #37 | **97/97** | `final-check-refresh-results.json`, `…-network-log.json` |
| `check_county_browser.py` | #38 | **72/72** | `final-check-county-results.json`, `…-network-log.json` |
| `check_fence_browser.py` | #39 | **113/113** | `final-check-fence-results.json`, `…-network-log.json` |
| `check_radar_browser.py` | #40 | **47/47** (without the optional `--real-image` / `--coastline` screenshot scenarios, which need a separately downloaded public CWA image; #40 ran them: 52/52) | `final-check-radar-results.json`, `…-alignment.json`, `…-network-log.json` |
| `check_series_error_visible.py` | V1 | **PASS** (visible message for 503 and 404) | wl41 V-7 |

Final-subject screenshots (synthetic, sample-derived data): `final-desktop-now-default.png`,
`final-375-now-default.png`, `final-desktop-forecast-mode.png`, `final-1280-radar-on.png`,
`final-1280-forecast-mode-no-radar.png`.

(The first attempt of the fence check stopped after one step on a Windows console-encoding error when
printing a `−` character — `cp950`; it was re-run with `PYTHONIOENCODING=utf-8` and passed; no check
logic involved.)

### 0.5 Status legend and shorthand

- **PASS** — verified; the evidence is the closed ticket's record (and its independent audit), plus the
  #41 final-subject re-run where named.
- **BLOCKED (RB-3)** — needs the acceptor to enter `CWA_API_KEY` in the Vercel project (reserved
  boundary RB-3; Spec §9 precondition 1; derivation record §11 #4). **Not a FAIL.** §6.2 lists exactly
  what verifies each item once the key is in.
- **Post-merge** — release evidence after the reserved merge (RB-1), not a completion condition.

Shorthand: *wlNN* = [`doc/governance/worklog/issue-NN.md`](../governance/worklog/); *aNN-r1/r2* =
`doc/governance/audit/issue-NN-c1-r1.md` / `-r2.md` (Reviewer-written); *shotsNN* =
`doc/acceptance/screenshots/v2/issue-NN/`; *ev41* = `doc/acceptance/screenshots/v2/issue-41/`
(final-subject browser results and network logs); *run* = the V2 run record; *DV-n* =
`doc/governance/decisions/` (derivation record `derivation-SPEC-V2.md` and the `decision-20260926-*`
records DV-20…DV-23).

## 1. Acceptance criteria AC-V2-01 … AC-V2-23

| AC | Class | Status | Owner | Verification method & evidence |
| --- | --- | --- | --- | --- |
| AC-V2-01 | V2 Core | PASS | #36; #38 (county round trip, DV-20) | Browser: opens in Now mode with `/api/health` 200 and 503; mode switch visible without scrolling at 1280 and 375, text `Now` / `Forecast`, Enter/Space; AC-17 / AC-18 re-verified verbatim inside Forecast mode; round trip keeps selection and view (wl36 V-5; shots36 `desktop-now-default.png`, `375-now-default.png`, `desktop-forecast-ac17.png`, `desktop-forecast-ac18-date3.png`; a36-r1 CLOSURE). County round trip (i)(ii)(iii) at 1280 and 375 (wl38 V-5 DV-20; shots38 `desktop-roundtrip-returned.png`, `375-roundtrip-returned.png`; a38-r1 re-did DV-20 → PASS, a38-r2 CLOSURE). #41 re-run: ev41 modes, county. |
| AC-V2-02 | V2 Core | PASS | #36 | Now mode has no `Select Date` / derived legend / forecast value; Forecast mode has no Refresh / Radar / county context / observation; marker colours disjoint from the four bands; no `real-time` / `realtime` / `live`; `Fetched Time` (Now panel) vs `Last updated (data fetched from CWA)` (forecast section) > 100 px apart; forecast dashboard text identical in both modes (wl36 V-5; `test_modes_frontend.py`; a36-r1). Radar absent in Forecast mode (wl40 V-9; a40-r1). |
| AC-V2-03 | V2 Core | PASS (offline, API, browser); **preview sample BLOCKED (RB-3)** | #35; #36; #41 (preview) | Offline: hand-computed stations incl. sentinel temperature, sentinel optional fields, 金門縣 / 連江縣, no upstream keys (`test_sample_normalises_to_hand_computed_stations`; wl35 V-5, V-17 independent oracle 0 diffs over 876 records; a35-r2 re-derived 0 diffs). Browser: all 22 markers = `/api/` `airTemperature`, sentinel → "—" (wl36 V-5; a36-r1). Preview: §6.2 item P-3. |
| AC-V2-04 | V2 Core | PASS | #35 (API); #36 (success); #37 (stale / unavailable) | API: dataset Observation Time = max valid `ObsTime`; Fetched Time `+08:00` to the second from the controllable clock (wl35 V-6). Browser labels verbatim and values = response in success (wl36 V-5), stale and unavailable ("—") (wl37 V-5; shots37 `desktop-stale-*.png`, `desktop-unavailable-*.png`; a37-r1). Note (a37-r1 F-2): the #37 check uses a **synthetic server clock** starting 2026-09-26 00:04:56 and simulated `ObsTime` shifts, so some #37 screenshots show a Fetched Time earlier than the Observation Time; this is the test rig, not product behaviour (every oracle is the response the page actually received). |
| AC-V2-05 | V2 Core | PASS | #35 | All eight derived counter-examples incl. (7) broken newest `ObsTime` → maximum falls to the remaining valid stations and (8) all `ObsTime` broken → `invalid_response` (wl35 V-7, V-22; a35-r1, a35-r2). |
| AC-V2-06 | V2 Core | PASS | #35 (API); #37 (UI) | API: reuse window 300 s (≤ 600 s), outside window re-fetch, 0 = always fetch, failures not cached (wl35 V-8). Browser (a)–(f): newer, not-newer (older Observation Time; same Fetched Time), five rapid presses → one request, upstream stall → `upstream_unreachable` JSON in 8.4 s, platform HTML 502 → Stale, held request → Stale at 20.4 s (< 30 s) (wl37 V-5; a37-r1). |
| AC-V2-07 | V2 Core | PASS | #35 (observation); #40 (radar) | Four reasons with a sentinel key; body, root-DEBUG log, stdout/stderr free of key, upstream host, upstream body, `Authorization` — 18 observation cases (wl35 V-9; a35-r1) and 18 radar cases (wl40 V-5; a40-r1 ran 15 more incl. an upstream echoing the key). |
| AC-V2-08 | V2 Core | PASS | #37; #38 (county part, DV-21) | (a) first-load failure for each reason → Unavailable in Now mode, both times "—", Refresh usable, no auto-switch; (b) Stale keeps data and both times; (c) next success clears; (d) page clock +2 h → still success (wl37 V-5; shots37; a37-r1). County layer and County context under Stale / Unavailable, "—" never 0 (wl38 V-5 DV-21; shots38 `desktop-unavailable-county.png`, `desktop-stale-county.png`; a38-r1 re-did DV-21 → PASS). |
| AC-V2-09 | V2 Core / V2 Radar | PASS | #36 (a); #37 (b); #40 (c); #41 (smoke) | (a) forecast 503 + observation OK → Now mode fully usable, section-level V1 error with `role="alert"`, Forecast mode inline error (wl36 V-5; shots36 `desktop-forecast503-*.png`); (b) observation failure → Forecast mode and dashboard normal (wl37 V-5); (c) radar failure changes only the radar, both directions (wl40 V-6, V-9; a40-r1). API: `/api/health` V1 tests unchanged (`test_dashboard.py`), 200 air-gapped and keyless (wl35 V-10). `smoke.py` vs preview: §6.1. |
| AC-V2-10 | V2 Core | PASS | #38 | Hover highlight + name; 臺中市, 臺北市, 金門縣, 連江縣 contexts = hand-computed from `/api/`; no average wording (wl38 V-5; shots38 `desktop-county-taipei.png`, `desktop-county-kinmen.png`; a38-r1 hand-computed all 22 counties). |
| AC-V2-11 | V2 Core | PASS | #36 | `tests/test_representative.py` (sample, three derived fallbacks, no-candidate county, determinism); README rule hand-computable (README l. 784–818); a36-r1 hand-computed the rule for all 22 counties = `/api/`. |
| AC-V2-12 | V2 Core | PASS | #38 | Station list Tab + Enter/Space, detail fields incl. `StationId`, `Back to Taiwan`, keyboard county path, off-map 東沙島 listed and openable (wl38 V-5, C-1; shots38 `desktop-station-detail.png`, `desktop-county-kaohsiung-offmap.png`, `desktop-back-to-taiwan.png`; a38-r2). |
| AC-V2-13 | V2 Core | PASS | #39 (#40: CRS unchanged) | Opening view holds main island + 澎湖; drags to every edge at z6/z8/z12 keep the centre in E and each axis ⊆ / ⊇; 金門, 連江 reached and selectable; floor z6 = 30.2 % (1280) / 46.9 % (375); ceiling z12 = 28.95 px/km, 375 px ≈ 12.96 km; 臺北市 stations selectable (wl39 V-5, C-3; shots39 `*-reach-*`, `*-zoom-*`; a39-r1, a39-r2). Map CRS unchanged by #40 (a40-r1). |
| AC-V2-14 | V2 Core | PASS | #39 | 1280 and 375 sets, 375 info panel 52.5 % map visible, Close button + Esc, 44×44, 768 no breakage, `scrollWidth` ≤ 375 in 11 states, desktop panel state rows 100 % visible (F-1 fixed) (wl39 V-5, C-1–C-3; shots39; a39-r2 36 desktop states). |
| AC-V2-15 | V2 Core | PASS | #36 (mode switch); #39 (complete) | V1 `test_map_frontend.py` guards unchanged and passing; no NaN / 0×0 markers after mode switch, info panel open/close, resizes (wl36 V-5; wl39 V-5 15 steps; a39-r1). |
| AC-V2-16 | V2 Core | PASS | #35; #36; #38; #40; #41 (final log) | Static re-scope add-only (`test_static_checks.py`; wl35 V-10; a35-r1). Forecast endpoints unchanged air-gapped and keyless (wl35 V-10; #41 72-pair comparison, §0.3). Final network log Now mode **with the radar shown** and Forecast mode (ev41 `final-check-radar-network-log.json`, scenario `1280-main`: 23 requests incl. 4 `/api/radar/latest`, 2 `/api/observations/latest`, `/api/days/<d>` for Forecast mode, 4 same-origin `blob:`; **0 external**); all six final logs together: 50 + 203 + 136 + 506 + 113 requests, **0 external** (every request `http://127.0.0.1:<port>/…` or a same-origin `blob:`). |
| AC-V2-17 | V2 Core | PASS (a)(b)(d)(e); **(c) BLOCKED (RB-3)** | #35; #40; #41 | (a) `git ls-files` no `.env`; credential scan passed; samples carry no `Authorization` value (wl41 V-8). (b) key read only from process env `CWA_API_KEY` at request time (`observation.py`, `radar.py`; a35-r1, a40-r1); local run with `.env` succeeded with no key in the terminal (wl35 V-13, wl36 V-13, wl40 V-7, wl41 V-9). (d) no key → `key_not_configured`, forecast normal — locally (`test_no_key_in_process_env_is_key_not_configured`) **and on the preview deployment** (§6.1). (e) all worklogs, audits, acceptance files and screenshots scanned (wl41 V-8). (c): §6.2 P-1, P-2. |
| AC-V2-18 | V2 Radar | PASS | #40 | Labelled control, off by default, keyboard; overlay + `Radar Time` separate from the observation times; re-fetch = switching on, or Refresh while shown (README l. 739); unavailable / stale; layer order; Forecast mode has no radar; API image + `X-Radar-Time`, four reasons, reuse 120 s ≤ 300 s (wl40 V-5, V-9; shots40; a40-r1). |
| AC-V2-19 | V2 Radar | PASS | #40 | 24-strip placement, computed max 0.0075 km at z6–12; rendered ≤ 0.067 km at z10, 0.72 km at z7 (coarse); naive overlay 3.83 km (check discriminates) (wl40 V-8; `shots40/alignment.json`; a40-r1 independently recomputed ≤ 0.0075 km and measured ≤ 0.064 km at z10). |
| AC-V2-20 | V2 Core | PASS | every ticket; #41 complete | CI green on the final subject; V1 tests kept and not weakened; blob / diff and forecast `/api/` comparison; §6.3 below (§0.3; wl41 V-1–V-6). |
| AC-V2-21 | V2 Core | PASS (self-check; Reviewer concludes) | #36 (13); #41 (all) | Fourteen items with README line citations: §2. |
| AC-V2-22 | V2 Core | PASS (`GET /`, `/api/health` smoke, no login, deployment ↔ commit); **observation part BLOCKED (RB-3)**; production post-merge | #41 | §6.1 (smoke output, deployment id). Observation part: §6.2 P-1, P-4. |
| AC-V2-23 | V2 Core | PASS | #36; #38 (`Back to Taiwan`) | `test_verbatim_labels`, `test_mode_switch_is_two_labelled_buttons`, `test_no_real_time_or_live_wording` (wl36 V-8); `Back to Taiwan` verbatim (wl38 V-5; `test_county_frontend.py`). |

## 2. AC-V2-21 documentation review — fourteen items (self-check)

Line numbers refer to the final `home_work_01/README.md` (1191 lines), now kept unchanged as
[`home_work_01/README.technical-reference.md`](../../README.technical-reference.md) (renamed 2026-09-26;
`README.md` is now a concise overview). WI-UI-THEME-1 later added two lines after l. 845, so
citations past l. 845 are two lower than the current file's line numbers.

| # | Item | Status | Citation |
| --- | --- | --- | --- |
| 1 | Now / Forecast mode explained; Forecast mode has its own heading, reachable from the contents | PASS | Contents l. 21–47, direct bold entry l. 39 → heading l. 822 "Forecast mode — the Part A bonus map: six-region Taiwan Map and `Select Date`"; modes table l. 504–520; scope note l. 8–19 also links it. |
| 2 | O-A0001-001 source and hourly cadence, conservative wording | PASS | l. 546–551 ("which CWA describes as hourly data … When CWA publishes a new hour is up to CWA"); l. 340–345. |
| 3 | Representative station rule, hand-computable | PASS | l. 784–818 (four steps, worked examples); `representativeStationIds` l. 360. |
| 4 | Off-map station rule | PASS | l. 646–652 (range, 東沙島 example, counted / listed / detail). |
| 5 | Observation (as published) vs derived kept apart; none of R-V2-DOC-5 (a)–(d) | PASS | l. 86–103 (comparison table), l. 520–530 ("Two meanings kept apart"; "`Fetched Time` is not the forecast's 'Last updated'"), l. 603–607 and 623–625 (no county average). Search of the whole README: no `real-time` / `realtime` / `live`; observation values never called forecasts or derived; no representative value called a county value. |
| 6 | CWA attribution for both V2 datasets | PASS | l. 876–891 table: 交通部中央氣象署 氣象觀測站-全測站逐時氣象資料 (O-A0001-001); 交通部中央氣象署 雷達整合回波圖-臺灣(鄰近地區)_透明底圖 (O-A0058-006); Open Government Data License; also l. 780–782. |
| 7 | Vercel key steps: variable name, environments, entered by the acceptor, no value; local `.env` | PASS | l. 913–932 (`CWA_API_KEY`, Production + Preview, acceptor only, RB-3, redeploy, key-free check, no `vercel env pull`); l. 903–911 (what needs a key); `.env` l. 130–152, l. 294–298, l. 421–430. No key value anywhere. |
| 8 | Observation / radar endpoints, failure codes, timeout, reuse window | PASS | l. 340–432 (observation: fields, four reasons l. 393–404, 8 s bound + 20 s page bound + 300 s reuse l. 407–419); l. 439–500 (radar: headers, four reasons l. 471–483, 8 s + 120 s l. 485–494). |
| 9 | Fence and zoom range | PASS | l. 665–683 (range 21.2–26.7 / 117.6–122.9, zoom 6–12, opening view). |
| 10 | Radar source, alignment method, re-fetch trigger, known limits | PASS | l. 439–446, l. 725–782 (source, drawing order, re-fetch trigger l. 739–745, alignment l. 756–770, known limits l. 771–779). |
| 11 | Accepted Later list | PASS | l. 1152–1172 (Spec §8 OPTIONAL / Later, all items). |
| 12 | V2-contradicting old statements corrected; V1 "forecast path needs no secret" kept | PASS | Corrected in #41: `.env` usage (l. 141–152, was "read solely by the ingestion fetch stage"), deployment (l. 903–911, was "The running function needs no environment variable and no secret — the CWA key is never part of the deployment"), V1 branch-alias preview URL replaced (l. 945–959), Refresh first-load wording (l. 559–562, a37-r1 F-3), credential-scan artifact list (l. 1130–1135). Kept: l. 905 "needs **no environment variable and no secret**, exactly as in V1" for the forecast part; l. 336–338. |
| 13 | `CONTEXT.md` vocabulary delta verbatim | PASS | [`CONTEXT.md`](../../CONTEXT.md) l. 97–99, 122–132, 146–170 — ten BRIEF-V2 §9 entries verbatim; machine-checked by `test_modes_frontend.py::test_context_glossary_delta_is_verbatim` (passes on the final subject). |
| 14 | V2 acceptance document maps every AC-V2 and §6.3 row; V1 `ACCEPTANCE.md` not rewritten | PASS | This file §1 (23 / 23) and §3 (all §6.3 rows); `ACCEPTANCE.md` diff = one added pointer paragraph only (wl41 V-10). |

## 3. §6.3 targeted V1 revalidation

| V1 item | Via | Status | Evidence |
| --- | --- | --- | --- |
| AC-17, AC-18 | AC-V2-01 | PASS | Re-verified verbatim inside Forecast mode (wl36 V-5; shots36 `desktop-forecast-ac17.png`, `desktop-forecast-ac18-date3.png`; a36-r1); #41 re-run ev41 modes. |
| AC-19 (R-EN-1 six items, 375 no horizontal scroll, three states) | AC-V2-14 | PASS | wl39 V-5 (R-EN-1 six items on the V2 page; 375 `scrollWidth` ≤ 375 in 11 states; loading / Stale / Unavailable shots `desktop-states-state-*.png`, `375-state-*.png`); a39-r1/r2. |
| AC-02, AC-03, AC-24 (dashboard side) | automated + screenshot | PASS | V1 `test_dashboard.py`, `test_app.py` unchanged, all ids present, passing (§0.3); browser: title, `Select Region` options and order, seven-row table = `/api/`, `Last updated (data fetched from CWA)` (wl36 V-5; shots36 `desktop-full-page-now.png`). |
| AC-04 | AC-V2-16 | PASS | Static re-scope add-only; `app.py` / `weather_query.py` import closure has no HTTP client, no CWA string (wl35 V-10; a35-r1; V1 test lines removed only the `_PYTHON_SIDE` / `_NON_SHARED_PYTHON` definitions and docstrings, wl41 V-3). |
| AC-07 (b)(c)(d)(f) | AC-V2-17 | PASS | Credential scan extended to the V2 samples and code (wl35, wl40; final run wl41 V-8). |
| AC-07 (e) — supersede note | AC-V2-17 | SUPERSEDED for V2 (Spec §1.2 Δ-3) | V1 AC-07(e) "the deployed dashboard needs no env var / no CWA key is set in the Vercel project env" was the V1 closed subject's criterion (its "no key in Vercel env" confirmation was listed PENDING-ACCEPTOR in `ACCEPTANCE.md` §5-3(c)). From V2 on it no longer applies to the deployed dashboard: the acceptor enters `CWA_API_KEY` in the Vercel project (Bindings b3 RB-3, second authorised location) and AC-V2-17 replaces it. The V1 evidence is not re-interpreted retroactively. The part that survives — the forecast path and `/api/health` need no secret — holds (INV-V2-1; preview `/api/health` 200 while observation / radar answer `key_not_configured`, §6.1). |
| AC-10 (dashboard side) | AC-V2-09 | PASS | Page-level error narrowed to the forecast section (DV-17): wl36 V-5 (`role="alert"`, server message, Now mode still usable); V1 `check_series_error_visible.py` PASS on the final subject (ev41). |
| AC-14 | AC-V2-21 | PASS | Eight V1 items unchanged, new citations: (1) F-A0010-001 delisted l. 55–58; (2) F-D0047-091 compatibility replacement l. 59–61; (3) W1 window l. 62–67; (4) mapping project-defined l. 68–77; (5) `PROJECT-DERIVED COMPATIBILITY VALUES` l. 79–84; (6) Derived Map Temperature derived l. 867–874; (7) Streamlit positioning l. 266–278; (8) no reverse wording — lead l. 3–6, representative points l. 857–860, whole-file review. New V2 items: §2 rows 2–7. |
| AC-15, AC-16, AC-22(a) | AC-V2-22, AC-V2-09 | PASS (preview); production post-merge | AC-15 / AC-22(a): `smoke.py` vs the no-login preview of `49dac12` → `SMOKE PASS`, exit 0 (§6.1). AC-16: `test_dashboard.py` health 200 + three 503 cases unchanged and passing; 72-pair forecast comparison (§0.3). AC-22(b): smoke workflow file unchanged (blob = V1). AC-22(c) and the production smoke: post-merge release evidence (DR-12, DR-18). |
| AC-26, INV-9 | AC-V2-20 | PASS | `app.py` blob identical to V1 (`5693be8`); `requirements.txt` identical (no folium); `test_static_checks.py` / `test_app.py` no-map checks pass (§0.3). |
| Title and masthead | AC-V2-23 | PASS | `<title>` / `<h1>` `Taiwan Weather Forecast` verbatim (wl36 V-8; preview page `<title>Taiwan Weather Forecast</title>`, §6.1); masthead lead describes the two modes (DR-21.2 precedent, R-V2-RSP-4 MAY). |
| All other V1 ACs (AC-01, 05, 06, 08, 09, 11, 12 except new README steps, 13, 20, 21, 23, 25, 27 except new code, 28, 29, 30) | CI green + blob / diff | PASS | V1 evidence stands (`ACCEPTANCE.md`); the V1 artefacts they rest on are byte-identical (§0.3); all 259 V1 test ids pass. AC-12's new README steps: wl41 V-9. AC-13: every V2 change is inside `home_work_01/` (the two workflow files are unchanged). |

## 4. Invariants — final self-check (Spec Integration Audit preparation; the SIA re-does each independently)

### 4.1 INV-V2-1 … INV-V2-9

| INV | Status | Evidence |
| --- | --- | --- |
| INV-V2-1 forecast path CWA-free and key-free | PASS | Static closure of `app.py` / `weather_query.py` (a35-r1); forecast endpoints byte-identical to V1 air-gapped and keyless (72 pairs, §0.3); preview `/api/health` 200 with no key in Vercel (§6.1). |
| INV-V2-2 zero key leak, two locations | PASS (repository, local); deployment part pending RB-3 | Credential scan, `git ls-files`, key literal absent from every committed diff (wl35…wl41); key read at request time from `CWA_API_KEY` only; sentinel-key tests on responses and logs (#35, #37, #40); preview responses carry only `key_not_configured`. The Vercel-side check (no key in responses / logs once entered) is §6.2 P-2. |
| INV-V2-3 browser calls only `/api/`, zero external requests (incl. radar) | PASS | Network logs #36 (46), #37 (192), #38 (135), #39 (505), #40 (all loopback / same-origin `blob:`), final #41 re-run 1,008 requests across the six logs, 0 external (ev41); `_ALLOWED_FRONTEND_URLS` unchanged. |
| INV-V2-4 `/api/health`, smoke, forecast endpoints unchanged | PASS | `smoke.py` blob = V1; §0.3 comparison; health 200 on preview without key. |
| INV-V2-5 two meanings apart, no observation aggregate | PASS | a36-r1 / a37-r1 / a38-r1 / a40-r1 H-3 sections; `test_county_context_computes_no_aggregate`; README §2 row 5. |
| INV-V2-6 freshness monotone; Stale failure-only; server success-or-classified-failure | PASS | wl35 V-8; wl37 V-5 (MutationObserver record never decreases; +2 h clock stays success); a37-r1. |
| INV-V2-7 three paths degrade independently | PASS | wl36 (forecast), wl37 (observation), wl38 (county layer, DV-21), wl40 (radar, both directions). |
| INV-V2-8 V1 invariants and artefacts unchanged | PASS | §0.3 blobs, test ids, 72 pairs; §4.2. |
| INV-V2-9 scope classes distinct | PASS | V2 only in the deployed dashboard; Grading App unchanged (`app.py` blob = V1); README "Not built" l. 1152–1157 states V2 is ENHANCED and does not change graded Part A behaviour. |

### 4.2 V1 INV-1 … INV-9

| INV | Status | Evidence |
| --- | --- | --- |
| INV-1 single query semantics | PASS | SQL only in `weather_query.py` (blob = V1); V2 modules in the no-SQL set (`test_static_checks.py`). |
| INV-2 behavioural equivalence | PASS | `test_dashboard.py` INV-2 test unchanged; forecast responses byte-identical. |
| INV-3 snapshot 6 × 7 | PASS | 42 rows, 0 duplicates (§0.3). |
| INV-4 teacher names (H-2) | PASS | DDL verbatim, SQL 6 / 7, `app.py`, `data.db`, title and concept words unchanged. |
| INV-5 zero key leak (H-1; extended by INV-V2-2) | PASS | As INV-V2-2. |
| INV-6 presentation layers never call CWA (re-scoped by INV-V2-1) | PASS for its V2 scope | Forecast path as INV-V2-1; the server-side observation / radar path is the Δ-1 re-scope. |
| INV-7 labeling (H-3; extended) | PASS | §2 and §3 AC-14 row. |
| INV-8 Python 3.12 three places | PASS | `.python-version` 3.12 (unchanged), CI `3.12`, local 3.12.14; Vercel build-log confirmation remains the V1 acceptor item. |
| INV-9 scope classes | PASS | As INV-V2-9. |

## 5. Acceptance-boundary coverage AB-V2-1 … AB-V2-13

| AB-V2 | AC-V2 | Status |
| --- | --- | --- |
| AB-V2-1 modes | 01, 02, 23 | PASS |
| AB-V2-2 Latest Observation | 03, 04, 05, 23 | PASS (preview sample BLOCKED RB-3) |
| AB-V2-3 Refresh / freshness | 05, 06 | PASS |
| AB-V2-4 failure classes / Stale / Unavailable | 07, 08 | PASS |
| AB-V2-5 independent degradation | 09 | PASS |
| AB-V2-6 Taiwan → County → Station | 10, 11, 12, 23 | PASS |
| AB-V2-7 fence / zoom | 13 | PASS |
| AB-V2-8 responsive usability | 12, 14, 15 | PASS |
| AB-V2-9 radar | 18, 19 | PASS |
| AB-V2-10 security boundary | 16, 17 | PASS except 17(c) BLOCKED RB-3 |
| AB-V2-11 tests / CI / V1 regression | 20 (+ §3) | PASS |
| AB-V2-12 documentation | 21 | PASS (self-check) |
| AB-V2-13 deployment | 22, 17(c) | PASS for the key-free part; observation part BLOCKED RB-3 |

Every AB-V2 item is covered by at least one criterion; the only open items are the three RB-3
preview checks of §6.2, which wait on an acceptor action and are not failures.

## 6. Deployment preview

### 6.1 Key-free part (done)

`smoke.py` against the public preview deployment of `49dac12` (no login, no cookie):

```
$ python smoke.py https://aiot-hw01-weather-extcrypm1-nchu-aiot-class.vercel.app
[2026-09-26T09:03:54Z] attempt 1  url=https://aiot-hw01-weather-extcrypm1-nchu-aiot-class.vercel.app  GET / -> 200  GET /api/health -> 200  (1.6s elapsed)  PASS
[2026-09-26T09:03:54Z] SMOKE PASS  url=https://aiot-hw01-weather-extcrypm1-nchu-aiot-class.vercel.app  (1.6s)
exit: 0
```

- `GET /` → 200, `<title>Taiwan Weather Forecast</title>`, the V2 page (`id="mode-now"`,
  `id="radar-toggle"` present), `data-deployment-id="dpl_GBZ1di8wdyraABA3n8VqU5R7d2o7"`.
- **Deployment ↔ commit**: that URL is the environment URL of GitHub deployment `6676924592`
  (environment *Preview*, sha `49dac12f6451a0462cb0f6c92256417b080cac1c`, state success)
  (`gh api repos/…/deployments?sha=49dac12…` and `…/deployments/6676924592/statuses`).
- `GET /api/health` → 200 `{"forecast_day_count":7,"ingestion_time":"2026-09-24T02:24:50+08:00","region_count":6,"status":"ok"}`.
- `GET /api/observations/latest` → **503** `{"dataset":"O-A0001-001","error":"Latest Observation is unavailable: the server has no CWA API key configured.","reason":"key_not_configured"}`, `cache-control: no-store`;
  `GET /api/radar/latest` → **503** `reason: key_not_configured`. This is the correct V2 behaviour for a
  deployment without the key (AC-V2-17(d) on the platform) and confirms the key has **not** been
  entered yet. `/api/health` does not depend on it (INV-V2-4).
- The same check on the deployment of the final subject is recorded in wl41 (Preview section).

### 6.2 BLOCKED until the acceptor enters `CWA_API_KEY` in Vercel (RB-3) — not failures

Precondition (acceptor only): README "Vercel key setup (acceptor only, V2)" steps 1–3 — variable
`CWA_API_KEY`, environments Production and Preview, then a redeploy of the branch's latest preview.
Then, on that redeployed preview, a Reviewer or agent verifies **without ever reading the key**:

| # | Item | Verification once the key is in | PASS condition |
| --- | --- | --- | --- |
| P-1 | AC-V2-17(c), AC-V2-22 (observation part) | `GET <preview>/api/observations/latest`; open `<preview>/` in a browser | 200 JSON with `dataset` `O-A0001-001`, `validStationCount` ≥ 1, `stations[]`, `observationTime`, `fetchedTime`; the Now mode shows the Latest Observation (markers, `Observation Time`, `Fetched Time`); `smoke.py` still PASS; deployment id ↔ commit as §6.1 |
| P-2 | AC-V2-17(c) radar, INV-V2-2 on the platform | `GET <preview>/api/radar/latest` (headers + byte count only); scan every recorded response body and header and the Vercel runtime log view the acceptor exposes for the key | 200 `image/png` with `X-Radar-Time`, `X-Radar-Dataset: O-A0058-006`; no key, no upstream URL, no `Authorization` in any response, record or log |
| P-3 | AC-V2-03 preview sample | Sample ≥ 3 stations: the value shown in the page (marker / detail) vs the same station in that page's `/api/observations/latest` body | Equal; any sentinel shown as "—" |
| P-4 | Decision A-6 preview observation-verification record; #35 R1 F-2 / #40 R1 F-2 and wl35 remaining-work 1 (Vercel timing) | Record P-1–P-3 with time, URL, deployment id and results in the #41 worklog / this section; time the first (cold) request; if practical, two concurrent requests | Terminal answers within the page's 20 s bound; a stalled CWA would answer `upstream_unreachable` (8 s cap < Vercel's 10 s default) rather than a platform page — if the platform limit proves lower, route to Design Authority (derivation §11 #1) |

Production smoke and production observation sampling after the merge are **release evidence**
(Spec §6.4, AC-V2-22), not completion conditions of #41.

## 7. Release-gate material (Bindings §5; decision A-6)

| Item | Status | Where |
| --- | --- | --- |
| README install and run steps actually run | Done (final subject) | wl41 V-9 |
| `git ls-files` has no `.env` (only `.env.example`) | Done | wl41 V-8 |
| No key in tracked files or history (credential scan) | Done — passed | wl41 V-8; CI run in wl41 |
| Teacher SQL on the committed `data.db` (A-2 / A-6) | Done — 6 and 7 rows | §0.3; wl41 V-6 |
| Latest green CI on the final subject | Done | wl41 V-2 |
| Preview observation verification (A-6, AC-V2-17(c), AC-V2-22) | **BLOCKED (RB-3)** | §6.2 |
| All Tickets closed, Spec Integration Audit closure, DA phase acceptance | Pending — SIA and phase acceptance come after #41 | run record |

## 8. Tracked non-blocking items and hand-offs

| Source | Item | Disposition |
| --- | --- | --- |
| a35-r1 F-2, a40-r1 F-2 | Service lock held during the upstream fetch: concurrent stalled requests queue on one instance | Browser side bounded by the 20 s page limit (a37-r1 (d)); deployment timing = §6.2 P-4 (BLOCKED RB-3). |
| a35-r1 F-3 | A non-string `CountyName` fails the whole response | Low; CWA always sends a string; no change. |
| a35-r1 F-4 | README "deployed function needs no secret" | **Fixed in #41** (§2 row 12). |
| a36-r1 F-1 | Representative selection outside `latest()`'s classification guard | Low; unreachable; note for the next editor of `representative.py`. |
| a37-r1 F-1 | A malformed 2xx body that passes the shallow check could replace `obs` before failing | Low; unreachable with this server. |
| a37-r1 F-2 | #37 screenshots show a synthetic clock | **Annotated in #41** (AC-V2-04 row). |
| a37-r1 F-3 | README first-load wording | **Fixed in #41** (§2 row 12). |
| a38-r2 N-1 | `check_modes_browser.py` "Refresh works while the forecast snapshot is unavailable" flaked when two fetches shared a second | **Fixed in #41** (`49dac12`): the check's server clock keeps fetches at least one second apart; assertion unchanged; 6 runs on the final code all 37/37 (a38-r2 had 3/6 failing) (wl41 V-7). |
| a38-r1 F-2, a39 SIA hand-offs (F-3, O-2, O-6, opening-zoom county reachability), a39-r2 O-5 / O-7 | Map usability observations | Handed to the Spec Integration Audit by the closing audits; not re-judged here. |
| a40-r1 F-1 | 375 px: the radar button pushes the map down (258 → 202 px visible at first screen) | Handed to the SIA (combined #36–#40 usability view). |
| In-app attribution (R-V2-DOC-2 SHOULD) | The Now-mode notes name "CWA station observations (O-A0001-001, hourly)" and the radar dataset with its full 交通部中央氣象署 attribution; the observation line does not repeat the full dataset title | README (MUST) carries both full attributions (§2 row 6). #41 makes no UI change; recorded as a concern for the SIA / acceptor (wl41). |

## 9. Cross-reference

- Worklogs: `doc/governance/worklog/issue-{35,36,37,38,39,40,41}.md`.
- Audit records: `doc/governance/audit/issue-35-c1-{r1,r2}.md`, `issue-36-c1-r1.md`, `issue-37-c1-r1.md`,
  `issue-38-c1-{r1,r2}.md`, `issue-39-c1-{r1,r2}.md`, `issue-40-c1-r1.md`.
- Decisions: `derivation-SPEC-V2.md` (DV-1…DV-19, §6 A-1…A-7, §11, §15), DV-20, DV-21, DV-22, DV-23;
  `decision-20260923-high-risk-categories.md`.
- Screenshots and machine evidence: `doc/acceptance/screenshots/v2/issue-{36,37,38,39,40,41}/`.
- V1 acceptance: [`ACCEPTANCE.md`](ACCEPTANCE.md).
