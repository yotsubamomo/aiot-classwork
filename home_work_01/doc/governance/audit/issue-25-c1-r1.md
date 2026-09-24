# Audit record — Issue #25 整合驗收（INTEGRATION／FINAL VERIFICATION），cycle 1，R1

| 項目 | 內容 |
| --- | --- |
| Work Contract | GitHub Issue #25（`yotsubamomo/aiot-classwork`，INTEGRATION／FINAL VERIFICATION）；Spec `home_work_01/doc/spec/SPEC.md` v1.1（§1.10、R-ENV-1/2、R-DS-9、R-TC-7、§2、§3、§6、§7）；Outcome Contract（ACCEPTED 2026-09-23）AB-1、AB-8、AB-11～AB-13、AB-17；decisions A-1／A-2／A-6、DR-6、DR-12、DR-17、DR-18、DR-19、unattended-run policy |
| 受審 subject | branch `home_work_01-hw10-implementation`，HEAD **`a571ccc78bbb13fcd982b8a5e76e27c6b544bb10`**（implementation／README／workflow 註解在 `fafcf2f`；`1396226`、`a571ccc` 新增 `doc/acceptance/ACCEPTANCE.md` 與 worklog），BASE `2f52766`。遠端 `origin/home_work_01-hw10-implementation` = `a571ccc`（`git ls-remote`）。 |
| Audit 種類 | Ticket independent audit，**R1**（full），**cycle 1**。這不是 Spec Integration Audit。 |
| 角色 | `primary_reviewer`（`gov-primary-reviewer`） |
| Binding 證據 | 由派工者依 Bindings §3.4 核對，記錄於 `home_work_01/doc/governance/run/run-20260924-hw01-formal.md`。Executor 為 `gov-executor`（agent `a0e8891359878c4f9`，opus-4-8／high，依 run record）；Reviewer mapping 為 opus-5-5／xhigh，cross-model diversity 維持。 |
| Independence（治理 §2.3） | Fresh context，未繼承 Executor 對話；Executor 的 worklog 與 ACCEPTANCE.md 只當作待驗證主張；自行讀取原始檔、`git diff 2f52766..a571ccc`、git 歷史、GitHub（Issue、PR、Actions、deployments）與公開部署，並在 scratchpad 的乾淨環境自行重跑；本 record 由 Reviewer 以自己的 Write 寫入。對 implementation、tests、contract、gates 唯讀，沒有任何 git 寫入。 |

## 1. 審查方法（Reviewer 自己執行的檢查）

1. **Subject 與 delta**：`git diff --stat 2f52766..a571ccc` 只改 4 個檔案：`.github/workflows/home_work_01-smoke.yml`（+11/−4，只改註解）、`home_work_01/README.md`（+11/−6）、`home_work_01/doc/acceptance/ACCEPTANCE.md`（+183，新增）、`home_work_01/doc/governance/worklog/issue-25.md`（+184，新增）（`git diff --numstat`）。smoke workflow 去掉註解後逐行相同，PyYAML 解析結果與 BASE 相同（`semantically identical to base: True`）。`git diff --stat 386f30a a571ccc -- home_work_01 ':!home_work_01/doc' ':!home_work_01/README.md'` 為空：自 #24 R2 closure 的 subject 之後，沒有任何 `.py`、`data.db`、`static/*`、測試或部署設定變更。所以 AC-02／03／04／10／19／24 的行為沒有被 #25 改動。
2. **乾淨的 Python 3.12 環境**：`git archive a571ccc home_work_01` 匯出到 Reviewer scratchpad（沒有 `.git`、沒有 `.env`）；用 uv 管理的 CPython 3.12.14 建立全新 `.venv`，執行 `pip install -r requirements.txt`，得到 Flask 3.1.2、pytest 8.3.3、streamlit 1.64.0、requests 2.32.3、pandas 3.0.6（間接相依），沒有 folium，也沒有 python-dotenv。
3. **測試**：`pytest -q -p no:cacheprovider` → **152 passed in 8.53s**。各檔數量與 worklog 相同（derive 19、persist 5、weather_query 29、app 9、dashboard 23、static_checks 22、fetch 13、pipeline 19、secrets 4、vercel_path_decoding 9）。
4. **Ingestion**：README 的離線指令 `python -m ingestion --from-json data/raw/F-D0047-091.json`（在匯出副本中執行）與 `--db <scratch>/rebuilt.db` 都 exit 0，印出 42 列預覽與 `rows: 42 | regions: 6 | date range: 2026-09-24 .. 2026-09-30`。重建出的 DB 與提交的 `data.db` 相比，兩張表的 DDL 與全部內容**完全相同**（位元組不同，這是 SQLite 檔案層的正常差異）。Online 路徑沒有以 acceptor 的金鑰實際呼叫 CWA（避免使用憑證）；改以 mock 的 `fetch_raw` 執行 `run_online`，看到 `Fetch summary (F-D0047-091): counties: 22 / weather elements (15) / periods per temperature element: 15`、42 列預覽，並寫出縮排的 raw JSON 與 sidecar（不含 `Authorization`）。Ingestion 程式自 #18 R2 closure（`7ee299c`）以來沒有變更。
5. **Grading App**：`streamlit run app.py --server.headless true` → `Uvicorn server started`，`GET /` 200，`/_stcore/health` 200。另以 `AppTest` 對提交的 `data.db` 執行：沒有例外；title `Taiwan Weather Forecast`；`Select Region` 選項依序為六區；中部地區與東南部地區的表格欄位為 `Date`／`MinT`／`MaxT`、七列，數值等於 `weather_query.region_series`；caption `Last updated (data fetched from CWA): 2026-09-24T02:24:50+08:00`；元素為 title、caption、selectbox、subheader、vega_lite_chart、dataframe（沒有地圖，也沒有 date input）。
6. **Flask Dashboard（本機）**：`python server.py` → `GET /` 200，`<title>Taiwan Weather Forecast</title>`；`/api/health` 200 `{"status":"ok","region_count":6,"forecast_day_count":7,"ingestion_time":"2026-09-24T02:24:50+08:00"}`；`/api/regions` 依固定順序回六區；`/api/days` 回七天。**INV-2**：六區的 `/api/regions/<r>/series` 都等於 `weather_query.region_series(r)`，各 7 列（`INV-2 API==module all six: True`）。
7. **瀏覽器（headless Chrome，最終 subject）**：`tests/check_series_error_visible.py` → `PASS`（503 與 404 都有可見訊息）。自寫的 render：資料庫缺失時 `#page-error`（`role="alert"`）可見，並顯示「database is missing」，dashboard 隱藏；正常快照下 dashboard 可見，含 `Select Region`、`Select Date`、`Last updated`、7 列表格與地圖。CDP 以 375×812 行動裝置模擬：`scrollWidth` 375 = `innerWidth` 375，6 個 marker，7 列表格，`Select Date` 7 個選項，`Select Region` 6 個選項。桌機截圖（1280 寬）上可以看到標題、控制項、摘要、圖表、表格、地圖、四段色帶圖例與「derived, not an observed daily mean」說明。
8. **公開部署**：`python smoke.py https://aiot-hw01-weather-git-homework01-hw10-im-8efc12-nchu-aiot-class.vercel.app`（2026-09-24T02:18:22Z 開始）→ `[2026-09-24T02:18:28Z] attempt 1 … GET / -> 200  GET /api/health -> 200 (6.6s elapsed) PASS`、`SMOKE PASS`、exit 0。**部署與 commit 的對應**：GitHub deployment `6628603831`（sha `a571ccc`，Preview，state success）的 environment URL 是 `aiot-hw01-weather-2hkce5qz7-…`；該 URL 與 branch alias 的 `GET /` 都帶有 Vercel 注入的 `data-deployment-id="dpl_7havCapJXgkyTYxvwYnNQGAiDLaw"`（`1396226` 的部署是 `dpl_EurBbr…`）。所以 alias 服務的正是 `a571ccc` 的部署。alias 上的 `static/app.js`、`styles.css`、`vendor/leaflet.js` 與 `git cat-file -p a571ccc:…` 的 sha256 相同；`index.html` 只多出 Vercel preview 注入的 toolbar `<script>` 一行（#21 R1 O-3 已說明）。Production `https://aiot-hw01-weather.vercel.app` 的 `/` 與 `/api/health` 都是 404，因為合併前 production 尚未更新（DR-12）。
9. **GitHub**：PR #27 `OPEN`（`isDraft: true`），head `a571ccc`，base `main`。CI `home_work_01-ci.yml` 在 `a571ccc` 的 push run `35945979604` 與 pull_request run `35945981663` 都是 success；log：`Python 3.12.14`、`152 passed in 3.90s`、`credential scan passed: 510 tracked files …`。`gh api …/actions/workflows/home_work_01-smoke.yml` → **404**（不在 `main`）。

## 2. AC 與 deliverable 判定

| 項目 | 判定 | 證據 |
| --- | --- | --- |
| **AC-12**（R-DOC-1） | **PASS** | README 已含 R-DOC-1 列出的每一項：3.12 與 venv（:54-77）、`pip install`（:73）、金鑰與 `.env`（:79-92）、online 與 offline ingestion（:94-127）、`streamlit run app.py`（:169-190）、本機 Flask（:206-231）、測試（:363-392）、Vercel Root Directory 與 production／preview（:282-315）、公開 URL（:312-315）、海報對應表（:427-444）。Worklog §5 逐步記錄指令、結果與日期（2026-09-24）。Reviewer 在乾淨的 3.12.14 venv 自行重跑 install、offline rebuild（重現提交的 DB 內容）、pytest 152、Streamlit headless、`server.py` 與 smoke，全部成功（§1）。Worklog 的 real-fetch 與 offline 步驟改寫到 scratch 路徑，是為了遵守 R-DB-6、不覆寫提交的快照，這是合理的偏離。Low 的文件一致性問題見 F-5。 |
| **AC-13**（R-DOC-3、R-ENV-2） | **PASS** | `git diff --name-only origin/main...HEAD` 在單元以外只有 `.github/workflows/home_work_01-{ci,smoke}.yml`（RB-5 授權）。Root 追蹤的檔案只有既有的 `.gitignore`、`AGENTS.md`、`CLAUDE.md`、`CONTEXT-MAP.md`、`README.md`，這些不是本單元的檔案。Topic branch 已 push，PR #27 為 OPEN（draft，見 O-2）。 |
| **AC-14**（R-DOC-2；Reviewer 文件審查） | **PASS**（8/8） | (1) README:23-26：F-A0010-001 為原指定，2026-07-01 下架是外部限制。(2) :27-29：F-D0047-091 是 project compatibility decision。(3) :30-35：W1 視窗，「compatibility window, not a calendar day」。(4) :36-46：「Region mapping is project-defined, not an authoritative CWA grouping」，並附成員表與「臺」的說明。(5) :47-52：`PROJECT-DERIVED COMPATIBILITY VALUES`，「never a CWA-issued six-region forecast」。(6) :273-280：Derived Map Temperature 是 derived value，not an observed daily mean。(7) :192-204：Streamlit 是 required grading artefact，不部署是 Vercel 限制造成的相容性安排。(8) 全 README 沒有反向措辭；:3-6 的導言已改為「derived from CWA county-level open data (not a CWA-published six-region product)」，#18 F-11 已修正；:268-270 說明代表點不是 CWA 發布的位置。最終 UI 的圖例與資訊卡也標示 derived（index.html:169、:185）。CONTEXT.md 的措辭見 O-1。 |
| **AC-15**（R-DS-8、R-DS-9、DR-12） | **實質 PASS；證據紀錄不符合契約 → F-1** | Reviewer 對 preview alias 的 smoke PASS（6.6 s，200／200，`status: ok`，不需登入），alias 服務的就是 `a571ccc` 的部署（§1 第 8 點）。Production smoke 依 DR-12 是 release evidence，ACCEPTANCE.md:50、:138-140 如實標為 PENDING-ACCEPTOR。但 AC-15 的證據欄、AB-1 的證據欄與 Ticket AC 都要求把 smoke **輸出**（含時間戳、URL、狀態碼）記入驗收文件；ACCEPTANCE.md 只有轉述，沒有時間戳、URL，也沒有部署與 commit 對應的證據（F-1）。 |
| **AC-22**（R-TC-7、DR-18） | **(a)(b) 實質 PASS；(a) 證據紀錄 → F-1；(c) release evidence，待 RB-1 後 dispatch** | (a) 同一支 `smoke.py` 對 `a571ccc` 的公開部署 PASS（Reviewer 重跑）。(b) Workflow 只改註解，非註解內容與 #22 審過的版本相同；`on: workflow_dispatch`（選用 `url` input），`URL="${INPUT_URL:-$VAR_URL}"`，兩者都空時明確失敗，`working-directory: home_work_01`，`python smoke.py "$URL"`，`permissions: contents: read`，不使用 secret；`checkout@v4`／`setup-python@v5` 3.12 骨架已由 `a571ccc` 的 CI 實跑成功。(c) `gh api …/home_work_01-smoke.yml` 回 404；ACCEPTANCE.md:57、:132-137 記為 PENDING-ACCEPTOR，符合 DR-18 §4.3，沒有 overclaim。DR-18 §4.1 要求 (a) 的證據包含時間戳、URL、兩個狀態碼、`SMOKE PASS` 與 exit 0，這部分見 F-1。 |
| **AC-23**（R-ENV-1、INV-8） | **PASS**（Vercel build log 待 acceptor） | 本機 3.12.14（worklog §5 與 Reviewer 的 venv）；CI `python-version: '3.12'`，log 為 `Python 3.12.14`；Vercel 的 `home_work_01/.python-version` = `3.12`。Build-log 確認依 #21 F-3 由 acceptor 提供，ACCEPTANCE.md:58、:141-143 標為 PENDING-ACCEPTOR，如實記錄。 |
| **AC-25**（R-ING-4、R-DER-8、DR-6） | **PASS**（證據形式 Low，F-7） | README:147-167 說明 raw JSON 的位置（`data/raw/F-D0047-091.json`）、產生方式（`json.dumps(..., indent=2, ensure_ascii=False)`）、擷取日期、F-D0047-091 的結構，以及預覽輸出。結構與提交的檔案相符（22 縣市、15 要素、每個溫度要素 15 個期間，`success`、`result.resource_id`）。Reviewer 看到 online（mock）與 offline 的摘要及 42 列預覽。Worklog 沒有貼出終端輸出，見 F-7。 |
| **AC-27**（R-DOC-5；Reviewer 結論） | **PASS**（Low：F-8） | (1) 說明：單元內 28 個 Python 檔都有 module docstring（AST 檢查）；126 個公開的頂層非測試定義中，113 個有 docstring。沒有的是測試 fixture，以及 `ingestion/pipeline.py:168 build_parser`、`smoke.py:180 main`、`tools/credential_scan.py:90,180`，它們的名稱與 module docstring 已說明用途。`static/app.js`、`index.html`、`styles.css` 都有檔頭與區段註解。(2) 錯誤處理：ingestion 以 fail-closed 方式處理並給出明確訊息（`pipeline.py:228-231`）；API 以 503 或 404 回傳含 `error` 的 JSON（`server.py:80-87, 122-156`）；Grading App 的 missing、empty、incomplete 都有明確訊息；前端狀態符合 DR-19（§1 第 7 點）。殘餘 #20 F-3（非 SQLite 檔、未定義的 `/api/` 路徑回 HTML）維持 Low。(3) 死碼與相依：`requirements.txt` 的四個套件都有使用；JS 沒有未使用的函式；CSS class 都有使用（部分由 JS 動態組出）；pyflakes 只找到 `tests/test_fetch.py:7` 一個未使用的 import（F-8）；pandas 未宣告的問題維持 #19 F-10。(4) 結構：`ingestion/{fetch,derive,persist,pipeline}` → `data.db` → `weather_query.py` → `app.py`／`server.py`＋`api/index.py`＋`static/`，對應資料流的各階段。 |
| **AC-30**（R-DS-8、R-ENV-2） | **PASS**（Root Directory 截圖待 acceptor） | `vercel.json`、`requirements.txt`、`.python-version`、`api/index.py` 都在 `home_work_01/`；root 沒有 `vercel.json`、`requirements.txt`、`data.db`、`app.py`。Root Directory = `home_work_01` 已由部署行為證實（#21）；dashboard 截圖依 #21 F-3 由 acceptor 提供，ACCEPTANCE.md:65、:143-144 標為 PENDING-ACCEPTOR，如實記錄。 |
| AC-02（重驗） | **PASS** | 兩層都有 `Taiwan Weather Forecast` 與 `Select Region`，選項為固定順序的六區（AppTest、`/api/regions`、headless DOM）。 |
| AC-03（重驗） | **PASS** | 中部與東南部地區的表格是七列 `Date`／`MinT`／`MaxT`，數值等於 DB（AppTest）；六區的 API 序列等於共用模組（INV-2）；圖表有 `MaxT`／`MinT` 兩條線（AppTest spec 與桌機截圖）。 |
| AC-04（重驗） | **PASS** | 22 個靜態檢查通過。Reviewer grep：呈現層沒有 SQL，SQL 只在 `weather_query.py`；沒有 HTTP client（`api/index.py` 只 import `urllib.parse`）；沒有 `opendata.cwa`／`CWA_API_KEY`；`app.js` 唯一的 `fetch(` 是 `:848` 的 `/api/` helper。 |
| AC-07（重驗 a–f） | **(a)–(d)、(f) PASS；(e) 的「Vercel 未設定金鑰」待 acceptor；紀錄 overclaim → F-2** | 見 §3 H-1。 |
| AC-10（重驗） | **PASS**（證據紀錄 Low，F-6） | Grading App 與 API：pytest 在最終 subject 通過（缺失、空表、不完整時的 AppTest 訊息，以及 health 與資料 endpoint 的 503）。頁面：Reviewer 以 headless Chrome 確認資料庫缺失時顯示 error 狀態，並有 `/series` 503／404 的可見訊息。 |
| AC-19（最終確認） | **PASS** | 最終 subject 的桌機 render 與 375 px 量測，見 §1 第 7 點。 |
| AC-24（重驗） | **PASS** | 兩層顯示的時間都是 `2026-09-24T02:24:50+08:00`，等於 `IngestionMetadata.ingestedAt`；`TemperatureForecasts` 的 DDL 沒有改變。 |
| **R-DOC-4**（驗收文件） | **存在且完整；F-1、F-2 兩處需修正** | ACCEPTANCE.md 對 AC-01～AC-30、INV-1～INV-9、AB-1～AB-17 都有一列，各列有狀態、驗證方式與證據引用。Reviewer 抽查的引用都能對應到實際產物：測試名稱（`test_ac09_negative_via_cli` 的參數化、`test_inv2_series_equals_shared_module_for_all_regions`、`test_weather_query.py:311-315` 的 AC-28 案例）、截圖（`ac02_*`、`ac03_*`、`ac10_*`、`issue-23-state-*`、`issue-24-*` 都存在）、CI run `35945880858`／`35925410250`（success），以及 audit records。 |
| Worklog subject prep（Ticket AC） | **需修正 → F-3** | §9 有列出全部 Ticket audit records 與整合證據，但最終 subject identity 寫錯，見 F-3。 |

### INV-1～INV-9（Ticket 層級最終自檢的核對；Spec 層級的結論由 Spec Integration Audit 另行給出）

| INV | 判定 | Reviewer 證據 |
| --- | --- | --- |
| INV-1 | PASS | SQL 只在 `weather_query.py`；`app.py:27`、`server.py:36` 都 import 同一個模組；前端只呼叫 `/api/`。殘餘 #19 F-8 為 Low。 |
| INV-2 | PASS | 六區 API == 共用模組，各 7 列（§1 第 6 點）；AppTest 的兩區表格也相同。 |
| INV-3 | PASS | 提交的 DB 為 42 列，`(regionName,dataDate)` 沒有重複，沒有 NULL；日期為連續七天。 |
| INV-4（H-2） | PASS | 見 §3 H-2。 |
| INV-5（H-1） | PASS（Vercel env 的確認待 acceptor） | 見 §3 H-1。 |
| INV-6 | PASS | 同 AC-04；即時部署的 `/` 與 `app.js` 都沒有 `opendata.cwa`。 |
| INV-7（H-3） | PASS | 見 §3 H-3。 |
| INV-8 | PASS | 同 AC-23。 |
| INV-9 | PASS | Grading App 的元素清單沒有地圖與 date input；地圖與 `Select Date` 只出現在 Dashboard。 |

## 3. 高風險類別核對（decision A-1）

本票觸及 **H-1、H-2、H-3**。

### H-1 憑證與機密

- **核對內容**：`python -m tools.credential_scan` → `credential scan passed: 510 tracked files; no .env tracked (only .env.example); no CWA-key-format string in tracked files or committed history; no Authorization value in fixture/raw JSON.`（exit 0）。`git ls-files | grep .env` 只有 `home_work_01/.env.example`，內容只有變數名。`home_work_01/.env` 被單元的 `.gitignore:12` 忽略，root `.gitignore` 也忽略它。
- **以真實金鑰值做的獨立比對**（從被忽略的 `.env` 讀進 shell 變數，長度 40，**從未印出**，只輸出筆數）：`git grep -F` 在 HEAD 追蹤檔案中 **0** 筆；`git log --all -p` 全歷史 **0** 筆；追蹤檔案中 CWA-UUID 格式字串 **0** 筆；PR #27 與 Issues #18–#25 的 body 與 comments **0** 筆；即時 preview 的 `/`、`/static/app.js`、`/static/index.html`、`/api/*` 回應 **0** 筆。CI log（`a571ccc`）顯示 scan 通過。部署端：`server.py` 與 `api/index.py` 不讀任何 OS 環境變數（`environ` 只指 WSGI environ）。
- **結果**：AC-07 (a) 由 #18 的證據沿用，ingestion 自 `7ee299c` 以來沒有變更；(b)(c)(d)(f) PASS；(e) 的「不需環境變數」PASS。「Vercel 專案沒有設定 CWA 金鑰」（R-SEC-3，#21 F-3）仍待 acceptor 提供，這一項如實標為 pending 就不是 finding。但 ACCEPTANCE.md 的 AC-07 列沒有這樣標示，見 **F-2**。H-1 沒有發現洩漏。

### H-2 老師指定的介面與資料格式

- **Reviewer 親自對提交的 `home_work_01/data.db` 執行老師的兩句 SQL**（檔案取自 `git show a571ccc:home_work_01/data.db`，sha256 `9bbf05bc…f542b`，與工作樹及 `2f52766` 相同；`data.db` 最後一次變更在 `7ee299c`，#25 沒有更換它，符合 R-DB-6）：
  - `SELECT DISTINCT regionName FROM TemperatureForecasts;` → **6 列**：北部地區、中部地區、南部地區、東北部地區、東部地區、東南部地區。
  - `SELECT * FROM TemperatureForecasts WHERE regionName = '中部地區';` → **7 列**，id 8–14，`dataDate` 為 2026-09-24…2026-09-30，格式都是 `YYYY-MM-DD`。
  - `sqlite_master` 中的 `TemperatureForecasts` 依序為 `id INTEGER PRIMARY KEY, regionName TEXT, dataDate TEXT, mint REAL, maxt REAL`（`PRAGMA table_info` 相符；token 與老師 DDL 相同，只有換行排版不同）。另一張表是 `IngestionMetadata`（DR-17），`TemperatureForecasts` 的形狀沒有改變。全表 42 列，沒有重複，沒有 NULL。
- **名稱**：`app.py`、`data.db`、`streamlit run app.py`（實際啟動成功）、`requirements.txt`、`README.md` 都存在；頁面文字 `Taiwan Weather Forecast`、`Select Region`、`Select Date`（只在 Dashboard）、`Date`／`MinT`／`MaxT` 在兩層都存在；六個 Region 名稱都帶「地區」。
- **結果**：PASS。

### H-3 資料語義與標示

- **推導**：`2f52766..a571ccc` 沒有改動推導、驗證、對應表或 fixture。Reviewer 從提交的 raw JSON 手算（W1 視窗、縣市日 min/max、成員平均、half-up）：中部地區 09-24 (24.8, 32.8)、09-30 (24.3, 29.8)；北部地區 09-24 (23.3, 31.0)、09-30 (24.6, 30.3)；東北部地區 09-24 (23.0, 30.0)、09-30 (24.0, 30.0)。全部等於提交的 `data.db`。Offline rebuild 也重現了完全相同的內容。
- **標示**：AC-14 八項 PASS（§2）；README 導言的修正準確；最終 UI 的圖例與資訊卡標示「derived, not an observed daily mean」。
- **結果**：PASS。CONTEXT.md 的措辭見 O-1。

## 4. 驗收文件的 overclaim 核對（派工指定項目）

| 項目 | 驗收文件的寫法 | 判定 |
| --- | --- | --- |
| AC-22(c) live `workflow_dispatch` | `PASS ((a)+(b) pre-merge; (c) PENDING-ACCEPTOR)`；§5-1 | 如實記錄（DR-18 §4.3） |
| AC-15 production smoke | `PASS (audited preview); production PENDING-ACCEPTOR`；§5-2 | 如實記錄（DR-12） |
| #21 F-3：AC-23 build log | AC-23 列與 §5-3(a) 標為 PENDING-ACCEPTOR | 如實記錄 |
| #21 F-3：AC-30 Root Directory 截圖 | AC-30 列與 §5-3(b) 標為 PENDING-ACCEPTOR | 如實記錄 |
| #21 F-3：Vercel env 沒有 CWA 金鑰 | §5-3(c) 標為 pending；但 **AC-07 列**的狀態是 `PASS ((e)/(f) note)`，並寫「acceptor-verified in Vercel dashboard, RB-3」 | **Overclaim，文件前後不一致 → F-2** |

## 5. Findings

### F-1 — 驗收文件沒有記錄 AC-15／AC-22(a) 的 smoke 輸出，也沒有提出部署與 commit 對應的證據

- **Severity**：Medium　**Blocking**：**是**
- **契約依據**：Outcome Contract AB-1 的證據欄「smoke test 輸出，記入 acceptance 文件」；Spec AC-15 的證據欄「smoke 指令輸出（含時間戳、URL、狀態碼）記入 `doc/acceptance/`」，PASS 條件含「部署的 commit 與受審 subject 對應」；DR-18 §4.1 規定 AC-22(a) 的證據為「本機指令輸出：時間戳、URL、兩個狀態碼、`SMOKE PASS`、exit 0」，§4.3 規定 `doc/acceptance/` 的 AC-22 條目要列出 (a) 的證據；Ticket #25 AC「AC-15、AC-22：對最終 subject 的部署重跑 smoke … 成功，**輸出記入驗收文件**」；A-6（release gate 的材料放在 `doc/acceptance/`）。
- **證據**：ACCEPTANCE.md:50 只寫「`smoke.py` vs public **preview** alias (no login): `GET /` 200 …, `/api/health` 200 `ok`, in 6.5s (wl25 §5 step 8 …). Preview serves the audited commit.」:57 只寫「(a) local `smoke.py` PASS vs audited preview (wl25 §5/§6)」。兩列都沒有時間戳，沒有 URL，也沒有 smoke 的原始輸出。Worklog `issue-25.md:78` 的指令寫成 `python smoke.py <preview-alias>`，結果只有「OK — `GET /` 200, `/api/health` 200, `SMOKE PASS`, exit 0, 6.5s」，同樣沒有 URL 與時間戳。「Preview serves the audited commit」沒有任何 deployment id 或 commit 對應的依據；README:304-307 自己也要求「confirm the served deployment id matches the commit rather than assuming it」，#21 R1 F-4 也曾因同類敘述提出 finding。實質內容本身成立：Reviewer 在 2026-09-24T02:18:28Z 取得 PASS，alias 的 `dpl_7havCapJXgkyTYxvwYnNQGAiDLaw` 就是 `a571ccc` 的 GitHub deployment `6628603831`（§1 第 8 點）。缺的是契約要求的紀錄。
- **為何 blocking**：這是本票主要交付物（R-DOC-4 驗收文件）對 AB-1 的明文證據要求，而且 Ticket AC 逐字要求把輸出記入。Spec Integration Audit 與 acceptor 的 release gate（A-6）都以這份文件作為證據入口。這不是設計疑義，也不需要其他 authority。
- **修正方向（HOW 由 Executor 決定）**：對最終 subject 的部署重跑 `smoke.py`，把逐行輸出（時間戳、URL、兩個狀態碼、`SMOKE PASS`、exit 0）記入 ACCEPTANCE.md 的 AC-15／AC-22(a)／AB-1，並寫入 worklog；同時記錄 alias 服務的 deployment id 與受審 commit 的對應，例如 GitHub deployment 的 sha 與 environment URL，對照頁面注入的 `data-deployment-id`。

### F-2 — AC-07 列把待 acceptor 確認的「Vercel 未設定 CWA 金鑰」寫成已驗證（H-1）

- **Severity**：Medium　**Blocking**：**是**
- **契約依據**：R-SEC-3「Vercel 專案不設定 CWA 金鑰」；AC-07 對應 R-SEC-1～R-SEC-3；H-1 的涵蓋位置包含「Vercel 環境變數」（`decision-20260923-high-risk-categories.md` §2.1）；#21 R1 F-3 的 disposition：AC-07(e) 要拆成「不需環境變數 PASS」與「未設定金鑰，待 acceptor」，並由 #25 最終記錄；治理 §1.5（不得捏造 evidence）、§4.5（不得虛報 verification）。ACCEPTANCE.md 自己在 §0 定義了 PENDING-ACCEPTOR 狀態，也用在 AC-15、AC-22、AC-23、AC-30。
- **證據**：ACCEPTANCE.md:42 的狀態欄是 `PASS ((e)/(f) note)`，(e) 寫「Vercel needs no env var/secret — **documented; acceptor-verified in Vercel dashboard, RB-3**」。同一份文件的 :141-145（§5-3(c)）卻把「confirmation that no CWA key is set in the Vercel project env (AC-07(e))」列為 acceptor 尚未產生的項目。AC-07 列沒有 PENDING-ACCEPTOR 標記，「acceptor-verified」讀起來就是已經完成的驗證。Reviewer 查不到任何 acceptor 提供該確認的紀錄；Vercel 帳號屬 RB-3，Reviewer 也無法自行查證。
- **為何 blocking**：這正是派工要求核對、不得寫成已完成的 acceptor-deferred 項目，而且屬於 H-1 高風險類別。Acceptor 在 release 時可能依這一列認為這項核對已經做過。依 A-3，高風險的 blocking finding 不得由 Final Adjudicator 單獨 defer。
- **修正方向**：AC-07 列改為「(a)(b)(c)(d)(f) PASS；(e) 不需環境變數 PASS；Vercel 未設定 CWA 金鑰 = PENDING-ACCEPTOR（RB-3，#21 F-3）」，並與 §5-3(c) 一致。

### F-3 — Worklog 的「最終 subject identity」寫錯：把 R-DOC-4 交付物當成 record-only，排除在 subject 之外

- **Severity**：Medium　**Blocking**：**是**
- **契約依據**：Ticket #25 AC「worklog 記錄最終 subject identity（branch 與 commit SHA）」與 What to build 第 5 項（Spec Integration Audit subject 準備）；Bindings §7 規定 record-only paths **只有** `doc/governance/**`；impl-default §7「Every verification／audit result MUST identify the subject version」；Spec R-DOC-4（`doc/acceptance/` 的驗收文件是 MVM 交付物）；治理 §4.7 第四項（最終 subject 的 coverage）。
- **證據**：`issue-25.md:31-33` 寫「`fafcf2f..1396226` touches only `doc/` record-only paths, Bindings §7」；:37-40 與 §9（:163-164）把最終 subject 定為 `fafcf2f`。ACCEPTANCE.md:12-13 也寫「Final subject … `fafcf2f`」。然而 `1396226` 新增的 `home_work_01/doc/acceptance/ACCEPTANCE.md` 不在 `doc/governance/**` 之下，而是 R-DOC-4 要求的交付物，在 `fafcf2f` 並不存在。依目前寫法，Spec Integration Audit 若以 `fafcf2f` 為 subject，就會漏掉 R-DOC-4 的交付物與其內容。
- **為何 blocking**：Spec Integration Audit 的 subject identity 是本票明文要求的交付內容，錯誤的 identity 會直接影響後續 audit 的 coverage。F-1 與 F-2 的修正會再改動 ACCEPTANCE.md，所以最終 subject 一定會是一個新的 commit。
- **修正方向**：Worklog §3、§9 與 ACCEPTANCE.md §0 改寫：最終 subject 是包含最終 ACCEPTANCE.md 的 commit（修正後的 HEAD）；說明 `doc/acceptance/` 不是 record-only path，只有 `doc/governance/**` 的後續 delta 才是 record-only。

### F-4 — 殘餘項目的彙整不完整：多個指定給 #25 的 tracked findings 沒有 disposition

- **Severity**：Medium　**Blocking**：否
- **契約依據**：治理 §4.3「Non-blocking findings MUST 記錄 disposition；需後續處理者須有 owner」；run record :89（#18 R2 **N-1（Medium）**、N-2 → #25）；各 audit record 的 disposition。
- **證據**：ACCEPTANCE.md §6（:151-174）自稱「Consolidated from the closed per-ticket audits」，worklog :61 與 :182-183 也說其餘 residuals 都已記錄。但下列 owner 為 #25 的項目既沒有修正，也沒有出現在 §6：#18 R2 **N-1**（Medium，offline 路徑不驗證取得時間格式；Reviewer 在最終 subject 重現：`--acquired-at yesterday` → exit 0，`ingestedAt = 'yesterday'`）；#18 R2 N-2（T-1 常數時鐘）、N-3、N-4、N-5（README 沒有加註「online 失敗後不要提交 `data/raw/`」）；#18 R1 F-9（見 F-7）；#19 R1 F-6（AC-03 沒有直接斷言圖表有七個日期）；#19 R1 F-10（pandas 未宣告）；#20 R1 F-4（資料 endpoint 的 503 測試未參數化到 empty 與 incomplete）；#21 R2 N-1。
- **為何不列為 blocking**：這些項目本身都是 non-blocking，沒有違反 AC；它們仍然記錄在原 audit record 與 run record 中，沒有消失，只是「已完整彙整」的說法不正確。
- **Disposition**：Owner 為 Orchestrator，#25 Executor 在處理 F-1～F-3 的 targeted correction 時**可以**一併把上述項目補進 §6，並寫明 disposition（修正，或繼續追蹤及其 owner）。N-1 屬 Medium，且 #25 結案後就沒有 owner，建議 Orchestrator 明確重新指派，例如作為結案後的 Lightweight 單點修正；它觸及 R-DB-5／DR-17，依 A-4 需要 independent audit。本項不延長 cycle，R2 也不以此為 closure 條件。

### F-5 — README 仍有過時的範圍說明；ACCEPTANCE.md 把 #20 F-7 記為已解決，並不正確

- **Severity**：Low　**Blocking**：否
- **契約依據**：R-DOC-1；AC-12 的文件一致性；#20 R1 F-7（owner #25）。
- **證據**：README:8-15 的「Scope of this README section」寫「Automated CI and the actual Vercel deployment are covered by their own tickets」，但同一份 README 已在 :282-332、:394-425 說明部署與 CI。README:58-61 與 `requirements.txt` 的註解都寫「The map libraries used by the later ENHANCED dashboard work are intentionally excluded」，但 ENHANCED 已完成，而且它用的是 vendored 的 Leaflet JS，不是 Python 相依。ACCEPTANCE.md:161 卻說 #20 F-7「Already resolved … no 'later ticket' phrasing remains」。
- **Disposition**：可選的文字修正，owner 為 #25 Executor（可併入 targeted correction）或 Orchestrator 追蹤。

### F-6 — AC-10 的證據引用：DR-19 指定 #25 重拍的截圖沒有重拍，AC-10 列也沒有引用 DR-19 與最終 UI 的截圖

- **Severity**：Low　**Blocking**：否
- **契約依據**：DR-19 §4.4(6) 與 §6（「#25：AC-10（Dashboard）重驗與截圖重拍依 §4.1；R-DOC-4 驗收文件引用 DR-19」）；Ticket AC「AC-10 對最終 subject 兩層重驗」。
- **證據**：`ac10_dashboard_error_missing_db.png` 最後一次變更在 `72ff874`（#20 的舊 UI），#25 沒有重拍；ACCEPTANCE.md:45 引用 `ac10_*`（舊 UI）與 `issue-23-state-*`（`fd654f3`，還沒有地圖），沒有引用 DR-19，也沒有引用最終 UI 的 `issue-24-state-error.png`（資料庫缺失，error 狀態）。Worklog §6 也沒有記錄 Dashboard 頁面層級的 AC-10 重驗。實質內容成立：自 `386f30a` 以來程式沒有變更，Reviewer 在最終 subject 以 headless Chrome 確認了 error 狀態（§1 第 7 點）。
- **Disposition**：可選。在 AC-10 列補上 DR-19 與 `issue-24-state-error.png`，並重拍 `ac10_dashboard_error_missing_db.png` 或註明它是 #20 時期的 UI。Owner 為 #25 Executor 或 Orchestrator。

### F-7 — AC-25 要求「worklog 貼終端輸出」，仍然沒有貼（#18 R1 F-9 的 owner 是 #25）

- **Severity**：Low　**Blocking**：否
- **契約依據**：Spec AC-25 的證據欄「worklog 貼終端輸出」；#18 R1 F-9 的 disposition（Owner：#25）。
- **證據**：`issue-25.md:74` 只用敘述說明「fetched … 42-row preview printed」，沒有貼出摘要與預覽的實際輸出。Reviewer 已看到兩段輸出（§1 第 4 點），所以 AC-25 的判定不受影響。
- **Disposition**：可選。把一次 ingestion 的終端輸出（摘要與 42 列預覽，不含金鑰）貼進 worklog。

### F-8 — `tests/test_fetch.py:7` 有未使用的 `import json`

- **Severity**：Low　**Blocking**：否
- **契約依據**：R-DOC-5「沒有死碼」（AC-27）。
- **證據**：pyflakes 輸出 `tests/test_fetch.py:7:1: 'json' imported but unused`（:29 的 `def json(self)` 是 `FakeResponse` 的方法）。這是整個單元唯一被找到的項目。
- **Disposition**：可選，owner 為 Orchestrator。不影響 AC-27 PASS。

## 6. 觀察（不是 finding）

- **O-1**：`CONTEXT.md:3-4` 寫「a one-week temperature forecast for six Taiwan regions, taken from CWA open data」，與 #18 F-11 修正前的 README 導言相同。它是詞彙表，:46、:63-64、:81-82 都明確寫出「Never a CWA-issued six-region forecast」與「_Avoid_: CWA regions」，所以沒有構成 AC-14(8) 的反向措辭。Executor 可以選擇順手統一措辭。
- **O-2**：PR #27 目前是 draft。AC-13「PR 已開」已經成立；合併前是否改為 ready 由 acceptor 在 RB-1 時決定。
- **O-3**：Vercel 會在 preview 的 HTML 注入 `https://vercel.live/_next-live/feedback/feedback.js`，這是平台注入（#21 R1 O-3），不是 subject 的前端請求，不影響 AC-04(b)／INV-6。
- **O-4**：ACCEPTANCE.md §0 與「Evidence shorthand」引用的 CI run 是 `1396226` 的 `35945880858`。`a571ccc` 已有更新的綠色 run（`35945979604`／`35945981663`）。依 A-6，release 時應引用「最後一次」CI 結果；修正 F-1～F-3 之後，會再有新的 run。

## 7. 其他 authority

- 不需要 Design Authority：沒有契約語義不足或 boundary 疑義。DR-12、DR-18、DR-19、#21 F-3 已足以判定各項。
- 不需要 Final Adjudicator：目前沒有爭議。
- Acceptor 項目維持 release 時處理，不是本票的完成條件：AC-22(c)、AC-15 production smoke，以及 #21 F-3 的三項 Vercel 確認（RB-1、RB-3）。
- Blocking 的 F-1、F-3 為文件修正，F-2 為 H-1 相關的紀錄修正；三項都在 #25 範圍內，屬 targeted correction，由 R2 核對。F-4 的 #18 R2 N-1 建議由 Orchestrator 重新指派 owner（見 F-4）。

VERDICT: BLOCKING (F-1, F-2, F-3)
