# Worklog — Issue #41 V2 整合驗收：README 與 CONTEXT 最終審查、V2 驗收文件、定向 V1 重驗、CI 全綠與部署 preview 驗證

- **Work item**：GitHub Issue #41（Formal lane，**INTEGRATION／FINAL VERIFICATION**——非 scope class，不承載新需求；V1 #25 先例、TB-V2-11；Blocked by #37、#40——皆 CLOSED）
- **Executing role**：`executor`，以 `gov-executor` definition 派工（Bindings §3.1 mapping：`claude-opus-5-5`，effort `high`）。本 session 自述的模型為 Opus 5.5；**這不是 binding 證據**。Binding verification 依 Bindings §3.4 由派工者（Orchestrator）從 harness 紀錄核對並記入 run record 或 audit record；本 worklog 不複製 harness 日誌。
- **Branch**：`home_work_01-v2-implementation`；**BASE ＝ `df78e79`**（run 推進到 #41 的 commit）
- **Subject**：code／doc anchor ＝ **`49dac12`**（README 最終審查＋#36 瀏覽器檢查去 flake）；其後 `9902026` 只新增／修改 `doc/acceptance/`（`ACCEPTANCE-V2.md`、V1 `ACCEPTANCE.md` 一段參照、`screenshots/v2/issue-41/` 的機器證據）——`doc/acceptance/` 不是 record-only，屬 subject；**final subject ＝ `9902026`**（無任何程式、`static/`、測試、`data.db` 變更，對 `49dac12` 為文件 superset）。之後只改 `doc/governance/**` 的 commit（本 worklog）為 record-only（Bindings §7 P7）。
- **開始／本次更新**：2026-09-26

## Work performed（摘要；結果：非金鑰部分全部完成，金鑰相關的 preview 項目 BLOCKED RB-3）

- README 最終審查與更正（R-V2-DOC-1 (1)–(11)，AC-V2-21 十四項自我核對見 `ACCEPTANCE-V2.md` §2）；`CONTEXT.md` 逐字核對（未改）。
- 新增 V2 驗收文件 `doc/acceptance/ACCEPTANCE-V2.md`：AC-V2-01～23、§6.3 定向 V1 重驗（含 AC-07(e) supersede 記述）、INV-V2-1～9 與 V1 INV-1～9 最終自我核對（**Spec Integration Audit 的 subject 準備**；SIA 仍逐項獨立核對）、AB-V2 覆蓋、preview 結果與 BLOCKED 項目的驗證步驟、release-gate 材料、交接項。V1 `ACCEPTANCE.md` 只加一段參照。
- 在最終程式碼上重跑：pytest、CI、test id 保留、blob／diff、預報 `/api/` 72 組 byte 比對、老師 SQL、六個瀏覽器檢查（最終 network log）、憑證掃描、README 乾淨環境實跑、preview smoke 與 deployment ↔ commit。
- 修正交接給 #41 的 #38 R2 N-1（瀏覽器檢查 flake）、#35 R1 F-4、#37 R1 F-2／F-3。
- **Integration subject（供 SIA）**：branch `home_work_01-v2-implementation`，**final subject ＝ `9902026cc41725524f154185aeebd59057fbdadf`**（CI `36232697465` success；preview deployment `6677133574` SMOKE PASS）；#41 範圍 BASE `df78e79`..`9902026`：25 個檔案，全部在 `home_work_01/` 內（RB-5）。

## Contract reference

- **Outcome Contract**：`home_work_01/doc/governance/outcome-contract-v2.md`（ACCEPTED 2026-09-25；normative candidate `69c5a04`）；A-3（本票用於一次 README 實跑的定向即時驗證，見 A-3 紀錄）；A-4 未使用（workflow 未改）。
- **Spec**：`home_work_01/doc/spec/SPEC-V2.md` **v2.2（DV-23 更正，commit `2771a54`）**——§2.8 R-V2-DOC-1～6；§2.9 R-V2-TC-3、TC-4、ENV-1、ENV-2；§3 AC-V2-03（preview）、16、17、20、21、22；§4 INV-V2-1～9；§6.3；§9 前置條件。
- **Derivation record**：`derivation-SPEC-V2.md` §6（A-1、A-5、A-6）、§11（未決 #1 Vercel 時限、#4 acceptor 填金鑰）、DV-16（授權標示：README MUST／應用內 SHOULD）、§15（本票分配）；DV-20～DV-23 已套用。
- **High-risk**：`decision-20260923-high-risk-categories.md` A-1——本票觸及 **H-1、H-2、H-3**；核對材料見下方專節。
- **契約變更**：無。未修改任何 requirement、AC、invariant、gate、oracle；未改任何產品程式或頁面。

## Decisions and assumptions（HOW）

1. **不新增行為**：本票只改 README、V2 驗收文件、V1 驗收文件一段參照，以及一個瀏覽器檢查工具的 harness 時鐘（見 4）。`static/**`、伺服器模組、`app.py`、`weather_query.py`、`ingestion/`、`data.db`、workflows 全未改。
2. **README（R-V2-DOC-1、AC-V2-21）**：新增 Contents（Forecast mode 以粗體獨立項直達其專屬標題）；「Data source and labeling」加觀測（如發布）vs 專案推導的對照表；新增「Data licence and attribution (CWA open data)」（O-A0001-001、O-A0058-006 全名授權標示，另列 F-D0047-091）；部署段改為 V2 事實（只有觀測與雷達 endpoint 讀 `CWA_API_KEY`；預報路徑與 `/api/health` 仍不需 secret——V1 敘述保留）並新增「Vercel key setup (acceptor only, V2)」（變數名、Production＋Preview、acceptor 親自填、redeploy、不讀值的檢查、不用 `vercel env pull`；不含值）；`.env` 段更正（原「read solely by the ingestion fetch stage」）；V1 分支 alias preview URL 改為「每個 commit 的 GitHub Preview deployment URL」；新增「Not built: the accepted Later list (V2)」（Spec §8 全部項目）；修 #37 R1 F-3（首次載入措辭）；CI 段的憑證掃描 artifact 清單加 V2 樣本；poster 對照表加 V2 模組。錨點以 scratchpad `anchors41.py`（GitHub slug 規則）核對：52 個連結全部可解析。
3. **Preview URL**：Vercel 分支 alias 名稱因長度被截斷加 hash，無法由 agent 推得（Vercel API 對 `nchu-aiot-class` scope 回 403，未嘗試其他帳號操作——RB-3）；改用 GitHub deployment 記錄的**每 commit deployment URL**，其與 commit 的對應直接由 GitHub deployment（sha、environment、state）證明，比 alias 更強。
4. **#38 R2 N-1 去 flake（owner：#41）**：`tests/check_modes_browser.py` 的伺服器以 `SecondApartClock` 取代真實時鐘（真實 Taipei 時間，但每次讀數至少比上一次晚 1 s），使首次載入與 Refresh 不會共用同一秒的 Fetched Time（R-V2-OBS-8 會正確判為 not-newer）。斷言與其餘 36 項不變；未弱化——前提變成確定的「新取得」，正是該檢查要驗的。
5. **應用內授權標示（DV-16 SHOULD）**：頁面 Now notes 已有「CWA station observations (O-A0001-001, hourly)」與雷達完整標示；觀測一行未含「交通部中央氣象署 氣象觀測站-全測站逐時氣象資料」全名。本票「不做任何行為或 UI 變更」，未改 `index.html`；README（MUST）兩個資料集全名皆具。列為 concern（見 Remaining work）。
6. **CONTEXT.md**：只核對（#36 已逐字併入；`test_context_glossary_delta_is_verbatim` 通過）。「Web App」詞條「never call CWA」描述的是讀取預報快照的產品行為，與 V2 伺服器端觀測路徑（Δ-1 re-scope）不矛盾；R-V2-DOC-4 只要求 delta 逐字，未改其他詞條。
7. **V2 驗收文件檔名**：`doc/acceptance/ACCEPTANCE-V2.md`（Spec 建議名，HOW）。證據以引用彙整；#41 只在最終 subject 重跑 §0.3 所列檢查。
8. **Commit 指令**：第一個 commit 使用了 `git -c core.hooksPath= commit`；事後確認本 repo 沒有設定 `core.hooksPath`，`.git/hooks/` 只有 `*.sample`——沒有任何 hook 被略過。之後的 commit 未再使用該參數。

## Artifacts

| 檔案 | 動作 | Commit |
| --- | --- | --- |
| `home_work_01/README.md` | 修改：見決定 2 | `49dac12` |
| `home_work_01/tests/check_modes_browser.py` | 修改：`SecondApartClock`（決定 4） | `49dac12` |
| `home_work_01/doc/acceptance/ACCEPTANCE-V2.md` | 新增：V2 驗收文件 | `9902026` |
| `home_work_01/doc/acceptance/ACCEPTANCE.md` | 修改：只在開頭加一段 V2 參照（既有條目未改寫） | `9902026` |
| `home_work_01/doc/acceptance/screenshots/v2/issue-41/*` | 新增：最終 subject 的六個瀏覽器檢查結果與 network log | `9902026` |
| `home_work_01/doc/governance/worklog/issue-41.md` | 新增：本 worklog（record-only） | 其後 |

## Verification

環境：Windows 11，`home_work_01/.venv` Python 3.12.14；Chrome headless（DevTools protocol，`websocket-client`）；clean venv 以 `uv` 建立（見 V-9）。

- **V-1 全套**：`python -m pytest -q` → **614 passed**（`49dac12`，repo venv；clean venv 同為 614，V-9）。全離線、無金鑰。
- **V-2 CI**：`49dac12` run **`36231516727`** success（`614 passed`；`credential scan passed: 782 tracked files …`）；final subject `9902026` run **`36232697465`** success（Python 3.12.14，`614 passed in 9.63s`；`credential scan passed: 804 tracked files; no .env tracked (only .env.example); no CWA-key-format string in tracked files or committed history; no Authorization value in fixture/raw JSON.`）。Workflow 未修改（A-4 未使用）。
- **V-3 V1 測試保留、未弱化（AC-V2-20）**：以 `git archive` 匯出並 `pytest --collect-only` 收集 test id：V1 結案 `ef15d3e` 259、run BASE `08e158e` 259、#40 `fedffdd` 614、HEAD 614；三者對 HEAD 的差集皆 **0**。`git diff ef15d3e HEAD` 對 V1 的 test／tool 檔：只有 `test_secrets.py`、`test_static_checks.py`、`tools/credential_scan.py` 有變更（+256／−9），刪除行只有 `_PYTHON_SIDE`／`_NON_SHARED_PYTHON` 兩個 re-scope 定義行與 docstring 文字（DV-15 add-only），無斷言刪除。本票對測試只改 `check_modes_browser.py` 的時鐘（決定 4；不被 pytest 收集）。
- **V-4 blob／diff vs V1 結案版 `ef15d3e`**：`git rev-parse` blob／tree 相同——`app.py` `5693be8…`、`weather_query.py` `4d2e92f…`、`data.db` `6875869…`、`requirements.txt` `f5199f4…`、`smoke.py` `5f09950…`、`vercel.json` `83dc6a1…`、`ingestion/` tree `91df24e…`、`data/raw/` tree `00cb0b8…`；`git diff --stat ef15d3e HEAD` 對上列＋`.python-version`＋`.github/workflows` → 只有 `api/index.py` 的 docstring（#35，3+/1−，不影響行為）；對 run BASE `08e158e` 同一清單（含 `doc/requirement/`）→ 空。`ef15d3e` 是 HEAD 的祖先。
- **V-5 預報 `/api/` 回應形狀（INV-V2-4、INV-V2-8）**：scratchpad `fwd41.py`——以 `git archive` 分別匯出 `ef15d3e` 與 HEAD 的單元，各自在子行程中封鎖 socket（`connect`／`connect_ex`／`create_connection`／`getaddrinfo`）且無 `CWA_API_KEY`，以 Flask test client 對 4 種 DB（committed、missing、empty、incomplete——少一列）× 18 個預報路徑（`/api/health`、`/api/regions`、`/api/days`、六個 series、未知 Region、七個 day、未知日期）比較 status＋Content-Type＋body sha256：**72 組，0 差異**（V1 status：200×16、404×2、503×54）。`GET /` 不在比較內（V2 頁面本來就不同）。
- **V-6 老師 SQL（A-2／A-6，唯讀開啟 committed `data.db`）**：SQL 1 → 6 列（北部地區、中部地區、南部地區、東北部地區、東部地區、東南部地區）；SQL 2（中部地區）→ 7 列 2026-09-24…09-30；共 42 列、0 重複；DDL 逐字（`id INTEGER PRIMARY KEY, regionName TEXT, dataDate TEXT, mint REAL, maxt REAL`）；`IngestionMetadata` `2026-09-24T02:24:50+08:00`／`F-D0047-091`；sha256 `9BBF05BC…0DBF542B`（＝ V1 `ACCEPTANCE.md` 記錄值）。
- **V-7 瀏覽器檢查（最終程式碼；`--out` 指向 scratchpad，未重產各票 evidence 目錄）**：執行前後 `static/app.js`、`index.html`、`styles.css`、`server.py`、`observation.py`、`radar.py` 的 sha256 相同。#36 `check_modes_browser.py` **37/37**，另連跑 5 次皆 **37/37**（6/6；#38 R2 N-1 記 6 次中 3 次失敗）；#37 `check_refresh_browser.py` **97/97**（199 s）；#38 `check_county_browser.py` **72/72**；#39 `check_fence_browser.py` **113/113**（608 s；第一次在印出 `−` 時因 Windows console `cp950` 編碼錯誤中止於第 1 項之後——與檢查邏輯無關——以 `PYTHONIOENCODING=utf-8` 重跑）；#40 `check_radar_browser.py` **47/47**（未帶 `--real-image`／`--coastline`，那兩個情境需另下載的公開 CWA 影像，#40 曾跑 52/52）；V1 `check_series_error_visible.py` PASS（503 與 404 皆有可見訊息）。結果與 network log 複製到 `doc/acceptance/screenshots/v2/issue-41/`（`final-check-*`），另五張最終截圖。
- **V-7a AC-V2-16 最終 network log**：六個 log 共 50＋203＋136＋506＋113 ＝ **1,008** 個瀏覽器請求，全部為 `http://127.0.0.1:<port>/…` 或同源 `blob:`，**外部 0**。Now mode 含 Radar 顯示＋Forecast mode：`final-check-radar-network-log.json` 的 `1280-main`（23 個請求，含 4 次 `/api/radar/latest`、2 次 `/api/observations/latest`、Forecast mode 的 `/api/days/<d>`、4 個同源 `blob:`；外部 0）；Forecast mode 另見 `final-check-modes-network-log.json`（A、B 兩情境）。
- **V-8 憑證（AC-V2-17(a)(e)、H-1、Bindings §5）**：`python -m tools.credential_scan` passed；`git ls-files` 只有 `.env.example`；scratchpad `keyscan41.py`（讀 `.env`，只輸出布林與計數）：`git diff 08e158e..HEAD`＋staged＋unstaged（23,408,146 chars）真金鑰字面 **False**、金鑰格式 **False**；追蹤中的 `home_work_01` 檔案 400 個（含全部 worklog、audit、acceptance、截圖、樣本）0 命中；`issue-41/` 21 檔、新文件 3 檔、scratchpad 瀏覽器輸出 254 檔、README 實跑 log 6 檔皆 0 命中。
- **V-9 README 安裝與執行步驟實跑（Bindings §5 release gate；AC-V2-21 相關；V1 AC-12 的新步驟）**：以 `git archive 49dac12` 匯出到 scratchpad（乾淨樹，無 `.env`）：
  - `uv venv --python 3.12 .venv` → CPython **3.12.14**；`uv pip install -r requirements.txt` → exit 0（flask 3.1.2、requests 2.32.3、streamlit 1.64.0、pytest 8.3.3；`import folium` → ModuleNotFoundError）。（README 的 `python -m venv` 需本機 3.12；本機 PATH 上是 3.11，因此用 README 同段的 `uv` 替代寫法。）
  - `python -m ingestion --from-json data/raw/F-D0047-091.json --db ../rebuild.db`（離線；`--db` 指向 scratch，未動 committed `data.db`）→ 印出 42 列預覽、`Persisted 42 rows … (ingested at 2026-09-24T02:24:50+08:00)`、exit 0；重建結果與 committed `data.db` 的全部列、`IngestionMetadata` 與 DDL **相同**。線上 `python -m ingestion`（F-D0047-091）**未執行**：不屬 A-3 授權的 V2 資料路徑，且 `ingestion/` 與 V1 byte 相同（V-4），V1 的實跑證據（wl25 §5）沿用。
  - `pytest -q` → **614 passed**。
  - `streamlit run app.py --server.headless true --server.port 8599` → Uvicorn 啟動、`GET /` 200、`/_stcore/health` 200，log 無 traceback；之後停止。
  - `python server.py`（repo 單元目錄，子行程環境先移除 `CWA_API_KEY`，金鑰只能來自 `.env`；scratchpad `live41.py`）→ `GET /` 200（標題、`mode-now`）；`/api/health` 200；`/api/observations/latest` **200**（0.22 s；`observationTime` 2026-09-26T17:00:00+08:00、`fetchedTime` 2026-09-26T17:23:59+08:00、有效 841／876、代表 22、`no-store`）；`/api/radar/latest` **200** `image/png` 65,853 bytes、PNG、`X-Radar-Time` 2026-09-26T17:10:00+08:00、`X-Radar-Dataset` O-A0058-006；server log 11 行；回應、標頭與 log 中真金鑰字面 **False**、金鑰格式 **False**、`opendata.cwa.gov.tw`／`amazonaws`／`Authorization` **False**（AC-V2-17(b)）。
  - `python smoke.py <preview>`：V-11。
- **V-10 AC-V2-21(14)**：`git diff 49dac12 9902026 -- doc/acceptance/ACCEPTANCE.md` 只有開頭新增一段引用（6 行），既有條目未改寫。README 52 個錨點連結全部可解析（`anchors41.py`）。R-V2-DOC-5：README 全文無 `real-time`／`realtime`／`live`（grep；`lives` 除外）。`CONTEXT.md` 逐字由 `test_context_glossary_delta_is_verbatim` 在最終 subject 通過。
- **V-11 部署 preview（AC-V2-22 非金鑰部分、AC-V2-17(d) 平台面）**：
  - `49dac12`：GitHub deployment `6676924592`（Preview、sha `49dac12…`、success）→ `https://aiot-hw01-weather-extcrypm1-nchu-aiot-class.vercel.app`，`data-deployment-id` `dpl_GBZ1di8wdyraABA3n8VqU5R7d2o7`；`smoke.py` SMOKE PASS（2026-09-26T09:03:54Z，1.6 s）。
  - **final subject `9902026`**：GitHub deployment **`6677133574`**（Preview、sha `9902026cc41725524f154185aeebd59057fbdadf`、created 2026-09-26T09:25:30Z、success）→ `https://aiot-hw01-weather-cckt159kq-nchu-aiot-class.vercel.app`，頁面 `data-deployment-id="dpl_HVDtY3JaXwXWGCzBwjepGURRJntw"`；未帶 cookie、無登入：
    ```
    $ python smoke.py https://aiot-hw01-weather-cckt159kq-nchu-aiot-class.vercel.app
    [2026-09-26T09:25:52Z] attempt 1  url=https://aiot-hw01-weather-cckt159kq-nchu-aiot-class.vercel.app  GET / -> 200  GET /api/health -> 200  (1.3s elapsed)  PASS
    [2026-09-26T09:25:52Z] SMOKE PASS  url=https://aiot-hw01-weather-cckt159kq-nchu-aiot-class.vercel.app  (1.3s)
    exit: 0
    ```
    `GET /` 含 `<title>Taiwan Weather Forecast</title>`、`id="mode-now"`、`id="radar-toggle"`（V2 頁面）；`/api/health` 200 `{"forecast_day_count":7,"ingestion_time":"2026-09-24T02:24:50+08:00","region_count":6,"status":"ok"}`；`/api/observations/latest` **503** `reason: key_not_configured`（`cache-control: no-store`）；`/api/radar/latest` **503** `key_not_configured`——部署上尚未填入金鑰，且缺金鑰時觀測／雷達以分類失敗回應、預報與 health 不受影響（INV-V2-4、AC-V2-17(d)）。
  - Vercel 分支 alias 無法取得（決定 3）；以每 commit deployment URL ＋ GitHub deployment 記錄作為 deployment ↔ commit 證據。
- **未執行／限制**：(a) 任何需要 Vercel 金鑰的 preview 驗證（見 Remaining work 1，BLOCKED RB-3）；(b) 線上 F-D0047-091 ingestion（V-9）；(c) 瀏覽器檢查只在 Chromium headless、合成滑鼠事件；(d) Streamlit 只驗啟動與 HTTP 200（畫面內容由 `AppTest` 覆蓋）；(e) Streamlit 啟動時自身的 usage-statistics／外部 IP 偵測屬 V1 既有行為，未改。

### A-3 金鑰使用紀錄

| # | 時間（+08:00） | 目的 | 動作 | 帶金鑰的上游 GET | 輸出 |
| --- | --- | --- | --- | --- | --- |
| 1 | 2026-09-26 17:23:58–17:24:00 | (ii) 對已接受的 V2 資料路徑做定向即時驗證（README「Run the dashboard locally」實跑） | V-9 `live41.py`：`python server.py`（金鑰只能來自 `.env`），觀測一次、雷達一次、health 一次 | 2（觀測 1；雷達 metadata 1＋公開影像 1 不帶金鑰） | 只印非機密摘要與布林檢查 |

無輪詢、無壓測、未印出或匯出金鑰；未進入 Vercel、未讀取 Vercel 環境變數（RB-3）；對 preview 的請求為公開 endpoint 的一般 GET，preview 上無金鑰（回 `key_not_configured`）。CI 與自動化測試不依賴金鑰或網路。

## High-risk 核對材料（decision A-1；供 R1 明記 H-1／H-2／H-3 核對段）

- **H-1**：README 金鑰步驟只有變數名 `CWA_API_KEY`、環境、步驟與不讀值的檢查，**無值**；preview 紀錄只含 `key_not_configured` 回應本文；`ACCEPTANCE-V2.md`、本 worklog、`issue-41/` 證據無金鑰（V-8 掃描：金鑰字面與金鑰格式 0 命中）；`git ls-files` 無 `.env`；未進入 Vercel、未讀出／印出／匯出任何金鑰（RB-3）。
- **H-2**：`app.py`、`weather_query.py`、`ingestion/`、`data.db`（sha256 `9bbf05bc…542b`）、`requirements.txt`、`smoke.py`、`vercel.json`、`data/raw/` 與 V1 結案版 `ef15d3e` blob／tree 相同（V-4）；老師 SQL 6／7（V-6）；DDL 逐字；預報 `/api/` 72 組與 V1 byte 相同（V-5）；頁面標題與概念詞由 #36 靜態守衛與 preview `<title>` 確認。
- **H-3**：README 對照表與「Two meanings kept apart」段；授權標示兩資料集（README）；代表測站值不當縣值、無觀測聚合（README l. 86–103、603–607、623–625）；全文無 `real-time`／`realtime`／`live`；`Fetched Time` 與 `Last updated (data fetched from CWA)` 分開說明。應用內觀測授權標示為 SHOULD 的部分滿足（決定 5）。
- **Diversity**：Executor 與 Primary Reviewer 同為 `claude-opus-5-5` 時，audit record 記 `diversity_lost`（Bindings §5）。

## Audit status

- **Required**：Formal mandatory independent audit（治理 §4.1；Bindings §5）。本 worklog 的所有檢查皆為 Executor self-verification，**不是**正式 audit。之後另有 Spec Integration Audit（§4.7）與 DA phase acceptance。
- **Records**：尚無。待 Orchestrator 派 R1。

## Remaining work

1. **BLOCKED（RB-3，acceptor 動作；不是 FAIL）**——前提：acceptor 依 README「Vercel key setup (acceptor only, V2)」步驟 1–3 在 Vercel 專案填入 `CWA_API_KEY`（Production＋Preview）並 redeploy 分支最新 preview。之後由 Reviewer 或 agent（**不讀取金鑰**）在該 redeploy 的 preview 上驗證，並記入本 worklog 與 `ACCEPTANCE-V2.md` §6：
   - **P-1 AC-V2-17(c)、AC-V2-22 觀測部分**：`GET <preview>/api/observations/latest` → 200，`dataset` O-A0001-001、`validStationCount` ≥ 1、`stations[]`、`observationTime`、`fetchedTime`；瀏覽器開 `<preview>/` → Now mode 顯示 Latest Observation（標記、兩個時間）；`smoke.py` 仍 PASS；deployment id ↔ commit（GitHub deployment）。
   - **P-2 AC-V2-17(c) 雷達、INV-V2-2 平台面**：`GET <preview>/api/radar/latest` → 200 `image/png`、`X-Radar-Time`、`X-Radar-Dataset: O-A0058-006`；所有記錄的回應本文與標頭（以及 acceptor 提供的 Vercel runtime log 畫面）無金鑰、無上游 URL、無 `Authorization`。
   - **P-3 AC-V2-03 preview 抽樣**：≥ 3 站，頁面顯示值 ＝ 同頁 `/api/observations/latest` 本文；哨兵顯示「—」。
   - **P-4 decision A-6 preview 觀測驗證紀錄＋Vercel 時序**（#35 R1 F-2、#40 R1 F-2、wl35 Remaining 1）：記錄 P-1～P-3 的時間、URL、deployment id 與結果；量首次（cold）請求時間；可行時兩個並行請求；終態須在頁面 20 s 內；若平台時限低於 8 s 上限的假設（Vercel 預設 10 s），route **Design Authority**（derivation §11 #1）。
2. **正式 audit**：R1（Orchestrator 派 `gov-primary-reviewer`）；結案依治理 §3.8。之後 Spec Integration Audit（subject ＝ `9902026` 或其後只改 `doc/governance/**` 的 HEAD）與 DA phase acceptance；合併（RB-1）、繳交（RB-2）屬 acceptor。production smoke 與觀測抽樣是合併後的 release evidence。
3. **Concerns（交有權角色判斷；Executor 未自行裁決）**：
   - (a) **應用內觀測授權標示（DV-16 SHOULD）**：頁面只寫「CWA station observations (O-A0001-001, hourly)」，未含「交通部中央氣象署 氣象觀測站-全測站逐時氣象資料」全名（雷達已有全名）；本票不改 UI（決定 5）。若需補，屬 `index.html` 一行文字；authority：Reviewer／SIA 判斷是否需要，或 acceptor 指示。
   - (b) **Preview 分支 alias** 不可得（決定 3）；README 改為每 commit 的 GitHub Preview deployment URL。
   - (c) **SIA 交接項**（各結案 audit 指定，非本票裁決）：#38 F-2 與 #39 F-3、O-2、O-5、O-6、O-7（地圖可用性觀察）、#40 F-1（375 px Radar 按鈕使地圖下移）——列於 `ACCEPTANCE-V2.md` §8。
4. **已在本票處理的交接項**：#35 R1 F-4（README 部署段）、#37 R1 F-2（截圖合成時鐘註記）、#37 R1 F-3（首次載入措辭）、#38 R2 N-1（#36 檢查去 flake）。
