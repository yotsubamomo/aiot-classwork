# Audit record — Issue #20，cycle 1，R1

| 欄位 | 內容 |
| --- | --- |
| Work Contract | GitHub Issue #20（`yotsubamomo/aiot-classwork`）「Dashboard MVM：Flask /api/ 與靜態頁面在本機提供相同的 Region 查詢行為」，Scope class MVM。所屬 Spec：`home_work_01/doc/spec/SPEC.md` v1.1（EFFECTIVE）；Outcome Contract：`home_work_01/doc/governance/outcome-contract.md`（ACCEPTED 2026-09-23）。適用裁決：`decision-20260923-spec-interpretation-rulings.md` DR-1、DR-2、DR-7、DR-8、DR-9；`decision-20260924-ingestion-timestamp-semantics.md` DR-17；`decision-20260923-high-risk-categories.md` H-1、H-2、A-1。分配依據：`derivation-SPEC.md:160`。 |
| 受審 subject | branch `home_work_01-hw10-implementation`，commit `72ff874f73ac91255cc15f4064e00e333a2c683a`；BASE `592c9ed`；範圍 `592c9ed..72ff874`，15 個檔案，全部在 `home_work_01/` 內 |
| Audit 種類 | **R1**（對 accepted work scope 做完整的 independent audit），**cycle 1** |
| 角色 | `primary_reviewer`（definition `gov-primary-reviewer`；Bindings §3.1 mapping 為 `claude-opus-5-5`／`xhigh`） |
| Binding 證據 | 由派工者（Orchestrator）依 Bindings §3.4 核對，記在 run record `home_work_01/doc/governance/run/run-20260924-hw01-formal.md`。同一份 run record 記載的 Executor binding：agent `afaf4ffd7f682a155` = `gov-executor`／`claude-opus-4-8`／`high`。Executor 與 Primary Reviewer 的 mapping 是不同模型，沒有 `diversity_lost`。 |
| Independence（治理 §2.3） | (1) 以 fresh context 派工，沒有繼承 Executor 的對話；worklog `worklog/issue-20.md` 與 Executor 的敘述一律當作待驗證的主張。(2) Binding 見上一列。(3) 自主取得：自行讀取 Ticket 本文（`gh issue view 20`）、Spec、Outcome Contract 的 AB 列、derivation record、各項裁決、brief §5、#19 的 R1／R2 record、git 歷史與 diff、全部實作與測試檔；測試、探測與截圖都由 Reviewer 自己執行。(4) 本紀錄由 Reviewer 用自己的 Write 工具寫入。 |
| 日期 | 2026-09-24 |

## 1. 審查方法與環境

- **確認 subject**：`git rev-parse HEAD` = `72ff874f…`。`git status --short` 只列出 `doc/governance/run/run-20260924-hw01-formal.md`，這是 Orchestrator 在 record-only path 上的修改（Bindings §7），不影響 subject identity。`git diff --cached` 為空。`git diff 592c9ed..72ff874 --name-only` 沒有任何路徑在 `home_work_01/` 外面，沒有觸及 RB-5。commit message 沒有 Claude 標記。
- **離線執行**：用 `git archive 72ff874 home_work_01` 匯出到 Reviewer 的 scratchpad，匯出的樹裡**沒有** `.env`。以單元 `.venv` 執行：Python 3.12.14、flask 3.1.2、werkzeug 3.1.8、streamlit 1.64.0、pytest 8.3.3。另外用 `sitecustomize` 封鎖所有非 loopback 的 `connect` 與 `getaddrinfo`，並把 `HTTP(S)_PROXY` 指向無效位址；已確認連線 `opendata.cwa.gov.tw` 會被擋下（`DNS BLOCKED by reviewer`）。
- **`pytest -q -p no:cacheprovider`**：**134 passed**。逐檔收集數：test_app 9、test_dashboard 22、test_derive 19、test_fetch 13、test_persist 5、test_pipeline 19、test_secrets 4、test_static_checks 14、test_weather_query 29。本票新增 `test_dashboard.py` 22 個；`test_static_checks.py` 由 BASE 的 9 個增為 14 個（`git show 592c9ed:…` 與 `72ff874:…` 的 `def test_` 計數）。舊的 9 個測試沒有被刪除或弱化：兩個被改名後擴大範圍（`test_no_sql_statements_outside_shared_module`、`test_python_side_does_not_touch_sqlite_directly`），其餘不變。
- **Reviewer 自己做的獨立檢查**（都在 scratchpad，不進 repo）：
  - **INV-2 三方比對**：對六個 Region，把 `/api/regions/<region>/series` 的輸出分別與兩者比對：以 `sqlite3` 直接查詢提交的 `data.db`（不經共用模組），以及 Grading App 經 `AppTest` 選定該 Region 後的表格。
  - **替代資料庫探測**，共 12 種，每種都打五個 endpoint：缺失、空表、41 列、43 列、含 null、六區日期錯位、沒有 forecast 表、沒有 metadata 列、零位元組檔、非 SQLite 檔、目錄、路徑含 `#`／空白／`%20`。
  - **404 與路徑探測**：未知 Region（含「北部」「台北」這類近似名稱）、未知日期、非日期字串、含 `%2F` 的 Region、未定義的 `/api/` 路徑、`/static/../server.py` 路徑穿越、`/data.db`、`/server.py`。
  - **真實瀏覽器**：以 Chrome 153 headless 對 Reviewer 自己啟動的 server 執行 `--dump-dom` 並截圖。情境包括：正常（預設 Region）、`?region=東南部地區`、資料庫缺失、空表、不完整、非 SQLite，以及用 scratch harness 對 `/series` 注入 503 與 404 的兩種故障。harness 只包裝受審的 `server.create_app`，沒有修改受審檔案。
  - **本機啟動**：在匯出的單元目錄實際執行 README 記載的 `python server.py` 與 `python -m flask --app server run`，兩者的 `GET /` 都回 200 並含標題，`/api/health` 回 200 `ok`。另外從**其他工作目錄**以 `importlib` 載入 Vercel entry `api/index.py`，`GET /`、`/api/health`、`/static/styles.css` 都回 200。
  - **Mutation probes**，共 25 個：13 個 AC-04 靜態檢查 probe（F-4 的六種 import 寫法；server 內的 SQL 字串、`import sqlite3`、CWA URL、讀取金鑰環境變數；前端 fetch CWA 與 fetch 非 `/api/` 路徑；以及一個 `urllib.parse` 誤報檢查）、10 個 API 行為 mutant、2 個頁面文字 mutant。另外把 F-4 的修正本身還原，檢查 regression guard 是否有效。
  - **H-1 掃描**：在程序內讀取被忽略的 `.env` 取得字面金鑰，**只輸出次數，不輸出任何金鑰內容**。另用 CWA 金鑰格式（`CWA-` 加上 8-4-4-4-12 hex）掃描。範圍：`592c9ed..72ff874` diff、commit message、`72ff874` 樹內全部 448 個追蹤檔案。
  - 完成後，Reviewer 自己啟動的 server 都已終止。`data.db` 的 blob 在 BASE、subject、工作樹與匯出樹（被 server 讀取多次之後）都是 `687586991ce3…`，也沒有產生 journal 或 WAL 檔。`git status` 與開始時相同。

## 2. Acceptance criteria、需求與 invariants 逐條判定

| 項目 | 判定 | 證據 |
| --- | --- | --- |
| AC-02（Dashboard） | **PASS** | `test_dashboard.py:52-55` 驗證 `GET /` 回 200 且 HTML 含標題；`:112-115` 驗證 `/api/regions` 等於共用模組的固定清單，這份清單另由 `test_weather_query.py` 的 `test_region_list_fixed_order` 逐字釘住。Reviewer 自己打 `/api/regions`，得到北部地區、中部地區、南部地區、東北部地區、東部地區、東南部地區（DR-8）。真實瀏覽器 DOM 的 `<option>` 順序相同，`<label>` 為 `Select Region`。截圖 `ac02_dashboard_default.png` 含 `Select Region`，也是真實畫面（見 AC-10 列）。可見文字的回歸保護較弱，見 F-5。 |
| AC-03（Dashboard） | **PASS** | `test_dashboard.py:145-154` 對六個 Region 驗證 7 列且升序；`:203-212` 對六個 Region 驗證與共用模組完全相同，而共用模組的輸出另由 `test_weather_query.py:198` 與直接 SQL 比對，因此是傳遞性的等於 `data.db`。Reviewer 另做**直接**比對：六個 Region 的 API 輸出都等於不經共用模組的 `sqlite3` 查詢結果。中部地區為 `(2026-09-24, 24.8, 32.8) … (2026-09-30, 24.3, 29.8)`，東南部地區為 `(2026-09-24, 24.0, 31.0) … (2026-09-30, 25.0, 30.0)`，都是 7 列且升序。瀏覽器 DOM 有兩條 polyline（`chart__line--maxt`、`chart__line--mint`），x 軸 7 個日期，表頭 `Date`／`MinT`／`MaxT`，表格 7 列，數值與 `data.db` 相同。整數值顯示為 `31` 而不是 `31.0`，與 Grading App 的預設格式相同（#19 O-2）。截圖 `ac03_dashboard_central.png`、`ac03_dashboard_southeast.png` 的內容與上述 DOM 相符。 |
| AC-04（完整 a／b／c／d） | **PASS** | (a) 以 AST 與 grep 檢查：`server.py` 的 import 只有 `pathlib`、`flask`、`weather_query`；`api/index.py` 只有 `os`、`sys`、`server`；`app.py` 與 `weather_query.py` 在本範圍沒有變動。沒有 HTTP client。backend 與 frontend 對 `opendata`、`CWA_API_KEY`、`environ`、`getenv`、`dotenv`、`.env`、`Authorization` 的 grep，只命中兩行說明「不讀環境變數」的 docstring。F-4 的六種 import 寫法 mutant 全部被抓到：`from urllib import request`、`from urllib.request import urlopen`、`import urllib.request`、`from http import client`、`api/index.py` 內的 `from urllib import request`、`import requests as r`。加入 `from urllib.parse import quote` 與 `from urllib import parse` 時，36 個測試全部通過，確認沒有誤報。回歸保護的強度問題見 F-2。(b) `static/` 內沒有 CWA URL 或金鑰。唯一的絕對 URL 是 SVG namespace。唯一的 `fetch` 在 `app.js:261` 的 `fetchJson(url)` 內，呼叫端只有 `/api/health`（`:40`）、`/api/regions`（`:58`）與 `"/api/regions/" + encodeURIComponent(region) + "/series"`（`:90`）。`index.html` 只載入同源的 `/static/styles.css` 與 `/static/app.js`，沒有外部字型或 CDN。mutant「fetch CWA」與「fetch 非 `/api/` 路徑」都被抓到。(c) `git grep` 找不到任何在 `weather_query.py` 以外、非 ingestion、非 tests 的 SQL 或 `sqlite3`。mutant「server 內放 SQL 字串」「server import sqlite3」都被抓到。(d) `server.py:36` 有 `import weather_query as wq`。每個 endpoint 都只呼叫 `wq.snapshot_status`、`wq.region_list`、`wq.region_series`、`wq.forecast_days`、`wq.day_values`、`wq.last_ingestion_time`，Derived Map Temperature 與色帶也直接取自 `DayValue`，沒有自己寫查詢或推導。前端 JS 只負責顯示，沒有重算任何業務值。 |
| AC-10（Dashboard） | **API PASS；頁面 PASS（列舉的三種狀態）；R-DS-6 另有 blocking 見 F-1** | 測試：`test_dashboard.py:74-106` 驗證 health 在缺失、空表、41 列與日期錯位時都回 503，`reason` 分別對應；`:118-197` 驗證四個資料 endpoint 在資料庫缺失時回 503 且含 `error`。Reviewer 的 12 種資料庫探測中，缺失、空表、41 列、43 列、含 null、日期錯位、沒有 forecast 表、零位元組檔、目錄這九種，五個 endpoint **全部**回 503 JSON，`reason` 正確且有 `error`。路徑含特殊字元的正常資料庫回 200。真實瀏覽器在缺失、空表、不完整三種狀態下，都顯示紅色錯誤 banner，訊息分別是「The forecast database is missing…」「…contains no snapshot yet…」「…is incomplete…」，控制項與面板都隱藏，不是空白頁。截圖 `ac10_dashboard_error_missing_db.png` 是真實畫面：它的檔案大小（15053 bytes）與 Reviewer 獨立重現的畫面完全相同。自動化證據只涵蓋部分情境，見 F-4。非 SQLite 檔的情況見 F-3。 |
| AC-16 | **PASS** | `test_dashboard.py:61-68`：200、`status == "ok"`、`region_count == 6`、`forecast_day_count == 7`、`ingestion_time` 等於直接查詢 `IngestionMetadata` 的值。Reviewer 實際取得的回應是 `{'forecast_day_count': 7, 'ingestion_time': '2026-09-24T02:24:50+08:00', 'region_count': 6, 'status': 'ok'}`。缺失、空表、不完整時回 503，內容為 `status: "unavailable"`、`reason`、`error`（`server.py:80-87`），符合 R-DS-2 的「原因、訊息」。mutant「不 ok 時仍回 200」（4 個測試失敗）與「時間改成常數」都被抓到。 |
| AC-24（Dashboard） | **PASS** | 頁面顯示 `Last updated (data fetched from CWA): 2026-09-24T02:24:50+08:00`（瀏覽器 DOM 與全部截圖），與 `IngestionMetadata` 的 `(1, '2026-09-24T02:24:50+08:00', 'F-D0047-091')` 逐字相同，而且來自 `/api/health` 的 `ingestion_time`，不是檔案 mtime。標籤寫的是「資料從 CWA 取得」，沒有寫成發布時間、頁面載入時間或部署時間，符合 DR-17 §4.5。`TemperatureForecasts` 的 DDL 沒有變動：`sqlite_master` 內仍是老師的五欄 DDL，`data.db` 的 blob 維持 `687586991ce3…`，不在 diff 之內。 |
| AC-27（本票範圍，R-DOC-5） | **(1)(3)(4) PASS；(2) 待 F-1** | (1) `server.py:1-28`、`api/index.py:1-11`、`app.js:1-13`、`styles.css:1-4` 都有說明目的的模組註解，`server.py` 的每個 endpoint 函式也都有 docstring。(2) 503 與 404 都回 JSON，並附人類可讀的 `error`；頁面對 health 與 regions 的錯誤、網路失敗都有明確訊息。但 series 在首次載入時失敗，訊息會被隱藏（F-1，blocking）。非 SQLite 檔會得到 HTML 500（F-3，Low）。(3) 沒有未使用的相依（`flask` 有用到）。測試檔內有一個未使用的常數（F-8，Low）。(4) 結構為共用模組 → Flask API → 靜態前端，與資料流一致。 |
| R-DS-1 | **PASS** | `GET /` 回 `static/index.html`（`server.py:91-94`）；靜態資源由同一個應用程式經 `/static/` 提供；JSON API 一律使用 `/api/` 前綴。路徑穿越探測（`/static/../server.py`、`..%2F`）與 `/data.db`、`/server.py` 都回 404。 |
| R-DS-2 | **PASS** | 見 AC-16。 |
| R-DS-3 | **PASS**（Low：F-3、F-4） | 四個資料 endpoint（`/api/regions`、`/api/regions/<region>/series`、`/api/days`、`/api/days/<date>`）的正常、503 都有測試；需要參數的兩個 endpoint 另有 404 測試（`test_dashboard.py:157-197`）。錯誤 JSON 都有 `error`。`/api/days/<date>` 的每一筆都含 `derivedMapTemperature` 與 `colourBand`，值等於共用模組的計算結果。README `:228-237` 列出全部 endpoint、回應格式與錯誤行為。10 個 API 行為 mutant 全部被抓到。 |
| R-DS-4 | **PASS** | 見 AC-02、AC-03。SHOULD 項目也都有達成：小標題 `Temperature Forecast – <Region>`（en dash），MaxT 紅 `#d62728`、MinT 藍 `#1f77b4`，Y 軸標題 `Temperature (°C)`，預設選第一個 Region。 |
| R-DS-5 | **PASS** | 見 AC-04。 |
| R-DS-6 | **FAIL（F-1，blocking）** | health 與 regions 失敗、網路失敗時，都會顯示明確訊息（見 AC-10）。但**首次載入**時，series 若回 503 或 404，訊息會寫進仍被隱藏的面板，畫面上看不到，見 F-1。 |
| R-DS-7 | **PASS** | 見 AC-24。 |
| R-DS-8（結構部分） | **PASS（本機驗證）** | 由單一 Flask app 同時提供頁面與 API（`server.py:60-175`）；`api/index.py` 把單元目錄加入 `sys.path` 後 `from server import app`；`vercel.json` 以 `builds` 指定 `@vercel/python` 為 `api/index.py`，`routes` 把 `/(.*)` 全部導向它，並以 `includeFiles: data.db` 打包資料庫。這與 brief §5.2 記載的老師已驗證模式一致。`requirements.txt` 與 `vercel.json` 都在 `home_work_01/`，root 沒有本單元的設定檔。`data.db` 以 `?mode=ro` 唯讀開啟（blob 不變、沒有 journal）。從其他工作目錄載入 entry 時可以正常服務。backend 與共用模組都沒有讀取環境變數或 secret。實際部署屬於 #21，本 audit 不要求公開 URL。Vercel function 體積的前瞻風險（#19 O-3）仍由 #21 處理。 |
| R-SHR-5（JS 側） | **PASS** | 見 AC-04(b)。 |
| R-SEC-3 | **PASS**（Low：F-6） | 執行期不需要任何 secret 或環境變數。Flask 在安裝 `python-dotenv` 時會自動載入 `.env`，這個條件性行為見 F-6。 |
| R-TC-4 | **PASS** | `GET /` 200 且含標題；health 的 200 與 503；每個資料 endpoint 的正常與 404／503 回應，都有 test client 測試（見上）。 |
| R-TC-5 | **PASS** | 在網路封鎖、沒有 `.env` 的匯出樹中，134 個測試全部通過。 |
| R-DOC-1（Dashboard 本機段、endpoint 清單） | **PASS**（Low：F-7） | README `:201-243`：本機啟動指令（`python server.py`、`flask --app server run`，Reviewer 都實跑成功）、網址、`/api/` endpoint 表、Vercel 結構說明。其他段落有幾處過時的文字，見 F-7。 |
| R-DOC-5 | 見 AC-27。 | |
| INV-1（完整） | **PASS** | 讀取端的 SQL 只在 `weather_query.py`；`app.py` 與 `server.py` 都只呼叫它；瀏覽器端 JS 只呼叫 `/api/`（見 AC-04）。Flask 與前端都沒有重新實作 Region 順序、日期清單、Derived Map Temperature 或色帶。寫入端的 SQL 在 `ingestion/`，已由 #19 R1 的 O-1 判定符合 OC §2.4 的分層。 |
| INV-2 | **PASS** | 自動化測試：`test_dashboard.py:203-212` 對六個 Region 斷言 API 的 `(Date, MinT, MaxT)` 等於共用模組。Reviewer 的三方比對：六個 Region 的 API 輸出都等於直接 SQL 查詢，也等於 Grading App 在 `AppTest` 中實際顯示的表格（`GA==API … True` 六次，欄位 `['Date', 'MinT', 'MaxT']`）。Dashboard 的 MVM 行為沒有比 Grading App 弱：不完整的快照依 DR-9 顯示錯誤狀態。 |
| INV-4（頁面文字） | **PASS**（Low：F-5） | 頁面文字 `Taiwan Weather Forecast`（`<title>` 與 `<h1>`）、`Select Region`、`Date`、`MinT`、`MaxT`、圖例 `MaxT`／`MinT`、六個 Region 名，在 DOM 與截圖中都逐字相同。Region 名來自共用模組的常數。`data.db` 與 DDL 沒有變動。 |
| INV-6 | **PASS** | 見 AC-04(a)(b)。 |
| AB-1（本機）、AB-3、AB-4、AB-5、AB-10 | **AB-1（本機）、AB-3、AB-4、AB-5 PASS；AB-10 的列舉狀態 PASS** | 對應以上各列。AB-10 要求的「缺失或為空時顯示明確訊息而非 crash」，在 test client 與瀏覽器中都成立。 |
| #19 F-4（owner #20） | **已解決**（Low：F-2） | 見 AC-04(a)。所有 F-4 寫法現在都會被抓到，也沒有誤報。但名為 F-4 regression guard 的那個測試，其實沒有保護到這次修正的機制，見 F-2。 |

## 3. 高風險類別核對（decision-20260923-high-risk-categories A-1）

### H-1 憑證與機密：觸及

- **核對內容**：以 AST 與 grep 檢查 `server.py`、`api/index.py` 與 `static/*` 的 import 與字面內容：沒有 HTTP client，沒有 CWA URL，沒有 `CWA_API_KEY`，沒有 `environ`、`getenv`、`dotenv`、`Authorization`。`vercel.json` 沒有 env 設定。以字面金鑰（從被忽略的 `.env` 在程序內取得，長度 40，只輸出次數）與 CWA 金鑰格式，掃描 `592c9ed..72ff874` diff、commit message 與 `72ff874` 樹內 448 個追蹤檔案。`git ls-tree` 是否含 `.env`。檢視四張新截圖。在沒有 `.env` 的匯出樹中啟動 server，確認執行期不需要任何環境變數。檢查 Flask 3.1.2 的 `cli.load_dotenv` 原始碼：只有在安裝 `python-dotenv` 時才會載入 `.env`；單元 `.venv`（依 `requirements.txt` 安裝）沒有這個套件。
- **結果**：字面金鑰 0 筆，金鑰格式 0 筆，沒有追蹤任何 `.env`；截圖只有公開的預報資料與取得時間；API 回應與頁面都不含任何秘密。**H-1 沒有 blocking。** Flask 在安裝 `python-dotenv` 的環境中會自動載入 `.env`，這個加固建議見 F-6（Low）。

### H-2 老師指定的介面或資料格式：觸及

- **核對內容**：頁面文字 `Taiwan Weather Forecast`、`Select Region`、`Date`、`MinT`、`MaxT`，圖例與線名 `MaxT`／`MinT`，六個 Region 中文全名與 DR-8 順序（瀏覽器 DOM、截圖、`/api/regions`）。`dataDate` 維持 `YYYY-MM-DD`。`data.db` 在 BASE、subject 與讀取之後都是同一個 blob（`687586991ce3…`）。`sqlite_master` 只有 `TemperatureForecasts`（老師的 DDL 逐字）與 `IngestionMetadata`。對提交的 `data.db` 執行老師的兩句驗證 SQL，得到 6 個 distinct regionName，`中部地區` 有 7 列。`app.py`、`requirements.txt`、`README.md` 仍在單元根目錄，`app.py` 在本範圍內沒有變動。
- **結果**：名稱、文字、格式與 DDL 全部符合，**H-2 沒有 blocking**。可見文字的自動化回歸保護較弱（只有 `<title>` 被測試到），見 F-5（Low）。

## 4. Findings

### F-1：首次載入時，series endpoint 的 503／404（或任何非 2xx）回應訊息會寫進被隱藏的面板，畫面上看不到

- **Severity**：Medium　**Blocking**：**是**
- **契約依據**：
  - Spec R-DS-6（`SPEC.md:191`）：「前端 **MUST** 處理 API 的 503／404／網路失敗：顯示明確訊息，不得留下空白頁或未處理的 console 例外作為唯一提示。」
  - Ticket #20「What to build」：「前端對 503／404／網路失敗顯示明確訊息，不留空白頁。」Traceability 列出 R-DS-1～R-DS-7。
  - Spec AC-10 的 FAIL 例包含「空白頁」。Spec §6：Ticket audit 依 Ticket 引用的需求逐條判定。
- **證據**：
  - `static/index.html:22`：`<section id="region-panel" class="panel" hidden>`。`:26`：`#chart-status` 位在這個 section **裡面**。
  - `static/app.js:89-99`：`loadRegion` 在 `!res.ok` 時呼叫 `showChartStatus(...)` 後直接 `return`，**沒有**設定 `els.panel.hidden = false`。`:291-296` 的 `showChartStatus` 本身也不會解除面板的隱藏。對照 `:107-110` 的 `.catch`（網路失敗）有先執行 `els.panel.hidden = false`。
  - 重現：Reviewer 用只包裝受審 `create_app` 的 harness，對 `/series` 注入 503 與 404，再以 headless Chrome 渲染。DOM 顯示 `<section id="region-panel" class="panel" hidden="">`，其中 `<div id="chart-status" …>injected 503</div>` 有文字卻看不到。截圖只有標題、`Select Region`（北部地區）與取得時間，**沒有圖、沒有表，也沒有任何訊息**。404 的結果相同。
  - 在宣告的 operating scope 內是可以發生的：部署到 Vercel 後，series 是一次獨立的 serverless 呼叫，平台的 5xx（例如逾時）或 `SnapshotError` 競態造成的 500 都會走進 `!res.ok` 這個分支（HTML 錯誤頁會被 `fetchJson` 轉為 `{}`，但一樣是 non-ok）。本機則會發生在 health 與 regions 成功之後、`data.db` 被替換或刪除的時候。
  - 次要（同一段程式）：已經有 Region 成功顯示之後，若切換 Region 時 series 失敗，面板雖然可見，小標題仍是前一個 Region 的名稱。
- **需要的修正（不指定做法）**：series 的非 2xx 回應，無論是不是首次載入，都要讓使用者看到明確訊息，而且不能留下看起來正常、實際上缺少圖表與表格的畫面。修正要附上可重現的驗證證據（例如以故障注入渲染，或等效方法），做法屬於 HOW。

### F-2：F-4 的 regression guard 測試沒有保護到這次修正的機制

- **Severity**：Low　**Blocking**：否
- **契約依據**：AC-04(a)；#19 R1 F-4（owner #20）的目的是強化回歸保護。
- **證據**：`test_static_checks.py:150-157` 只把手寫的 target 集合（例如 `{"urllib", "urllib.request"}`）交給 `_imports_http_client`，沒有經過真正修正的 `_import_targets`（`:103-106`，對 `ImportFrom` 記錄 `module.name`）。Reviewer 在 scratch 副本中把 `:104-106` 還原為修正前的寫法，14 個靜態測試**全部通過**；再加上 `from urllib import request as _r` 到 `server.py`，14 個測試**仍然全部通過**。目前 subject 的檢查本身是正確的（見 AC-04(a) 的 mutant 結果）。
- **Disposition**：Owner **#20**（可以併入 F-1 的 targeted correction，例如讓 guard 從原始碼字串經 `_import_targets` 驗證），否則由 **#25** 在 AC-04 最終核對時處理。

### F-3：`data.db` 為非 SQLite 檔時，全部 `/api/` endpoint 回 HTML 500；未定義的 `/api/` 路徑回 HTML 404

- **Severity**：Low　**Blocking**：否
- **契約依據**：R-DS-3「錯誤 JSON MUST 含人類可讀的 `error`」；R-DOC-5「錯誤有處理與明確訊息」。這些情境不在 AC-10／AC-16 列舉的三種狀態之內。
- **證據**：在非 SQLite 的情境下，五個 endpoint 都回 `500(non-JSON)`，traceback 出現在 `weather_query.py:167` 的 `sqlite3.DatabaseError: file is not a database`。這與 #19 R1 **F-7** 是同一個 root cause（共用模組），本紀錄不重開該 finding，只記錄它在 API 層的表現。此外，`/api/regions/a%2Fb/series`、`/api/nope`、`/api/days/` 都回 Flask 預設的 HTML 404。頁面仍然會顯示「The forecast data is currently unavailable.」，不是空白頁（瀏覽器已驗證）。
- **Disposition**：Owner **#25**（AC-27 最終核對，與 #19 F-7 一併處理），例如為 `/api/` 加上 JSON 格式的錯誤處理。

### F-4：AC-10 的自動化證據只涵蓋部分情境

- **Severity**：Low　**Blocking**：否
- **契約依據**：Spec AC-10（`SPEC.md:261`）：資料庫缺失，以及「只有表無列…同上」，都要求資料 endpoint 回 503、頁面顯示錯誤狀態；DR-9 對不完整的快照也要求相同處理。
- **證據**：資料 endpoint 的 503 測試（`test_dashboard.py:118-197`）只用**缺失**的資料庫；空表與不完整只測了 health。頁面錯誤狀態的截圖也只有缺失這一張。Reviewer 已獨立驗證行為成立：空表與不完整時五個 endpoint 都回 503，瀏覽器也顯示錯誤 banner（見 §2 AC-10）。所有 endpoint 共用同一個 `snapshot_status` 檢查，行為分歧的風險很低。
- **Disposition**：Owner **#25**（依 derivation record，AC-10 由 #25 重驗），可以把測試參數化到三種狀態。

### F-5：頁面可見文字的自動化回歸保護較弱

- **Severity**：Low　**Blocking**：否
- **契約依據**：INV-4、H-2（頁面文字）；AC-02（Dashboard）的證據要求是「根路徑 HTML 含標題」加上「截圖含 `Select Region`」，這兩項都已滿足。
- **證據**：`test_dashboard.py:52-55` 只斷言 HTML 某處含有標題，由 `<title>` 滿足。mutant「只改 `<h1>`」與「把 `Select Region` 標籤改成 `Region`」都沒有被抓到（36 passed）。表頭 `Date`／`MinT`／`MaxT` 也沒有自動化斷言。
- **Disposition**：Owner **#25**（AC-02／INV-4 最終核對）；#23／#24 改動 UI 時必須維持 R-EN-2 的這些字樣，可以一併補上斷言。

### F-6：在安裝 `python-dotenv` 的環境中，README 記載的兩種本機啟動方式都會把 `home_work_01/.env` 載入 Dashboard 的 process 環境

- **Severity**：Low　**Blocking**：否
- **契約依據**：Ticket #20 High-risk：「Dashboard 不得含任何 secret；**不讀 `.env`**」；AC-07 的 FAIL 例「Flask 讀 `.env`」；R-SEC-3。
- **證據**：`server.py:181` 呼叫 `app.run(...)`，而 Flask 3.1.2 的 `load_dotenv` 參數預設為 True（`flask/app.py:551`、`:623-624`），`flask run` 也會呼叫 `cli.load_dotenv()`。後者在安裝 `python-dotenv` 時，會以 `find_dotenv(".env", usecwd=True)` 載入 `.env`（`flask/cli.py:706-770`）。依 `requirements.txt` 建立的 `.venv` **沒有**這個套件（`find_spec('dotenv')` 為 False），所以在宣告的環境中不會載入，Executor 在 worklog 看到的「Install python-dotenv」提示也與此一致。即使被載入，程式也不會使用或輸出金鑰。Vercel 部署沒有 `.env`。
- **Disposition**：加固建議，例如 `app.run(..., load_dotenv=False)`，並在 README 對 `flask run` 註明 `FLASK_SKIP_DOTENV=1`。Owner：**#20**（可選）、**#21**（AC-07(e)），或 **#25**（AC-07 最終核對）。

### F-7：README 有幾處在本票之後過時的文字

- **Severity**：Low　**Blocking**：否
- **契約依據**：R-DOC-1；AC-12／AC-14 的文件一致性。
- **證據**：`README.md:54-57` 的 Requirements 只列 `requests`、`pytest`、`streamlit`，沒有 `flask`，還寫「the later dashboard ticket」。`:195` 寫「served publicly by a Flask + static dashboard in a later ticket」，但 Dashboard 本票已經完成，之後的票只負責部署。`:280-294` 的測試說明沒有提到 Flask test client 與前端靜態檢查。安裝指令 `pip install -r requirements.txt` 本身仍然正確。
- **Disposition**：Owner **#25**（README 實跑與文件審查），#20 也可以選擇順手修正。

### F-8：測試檔內有一個未使用的常數

- **Severity**：Low　**Blocking**：否
- **契約依據**：R-DOC-5「沒有死碼」。
- **證據**：`tests/test_static_checks.py:47` 定義了 `_BACKEND = (_SERVER, _API_ENTRY)`，全檔沒有任何地方使用它（grep 只命中定義那一行）。
- **Disposition**：Owner **#20**（可選）。

### F-9：worklog 的測試數量有誤

- **Severity**：Low　**Blocking**：否
- **契約依據**：治理 §3.7（worklog 必須如實）。
- **證據**：`worklog/issue-20.md:52` 寫「#19 為 104；… `test_static_checks.py` 由 12 增至 14」。實際上 BASE 共有 107 個測試（#19 R2 也記錄 107），`test_static_checks.py` 由 **9** 個增為 14 個。依 worklog 的數字，104 + 22 + 2 = 128，與它自己寫的總數 134 不一致；實際為 107 + 22 + 5 = 134。
- **Disposition**：Owner **#20**，在處理 F-1 更新 worklog 時一併更正。

## 5. 觀察（不是 finding）

- **O-1（`?region=` deep link）**：`app.js:67-70` 在 `?region=` 是六個 Region 之一時預選該 Region，README `:221` 有說明。這沒有被寫成老師的要求，沒有改變或弱化任何 MVM 行為，也沒有新增驗收宣稱。Reviewer 視它為 R-DS-4「選定 Region」互動的 HOW，因此沒有 route。如果 Design Authority 認為它應該標示為 ENHANCED UI（#24），那是 scope class 標示的問題，與本票的 closure 無關。
- **O-2**：快照是 6 × 7 但沒有 `IngestionMetadata` 列時，`/api/health` 回 200，`ingestion_time` 為 `null`，頁面顯示「unknown」。正常的 ingestion 會一起寫入 metadata，所以這只會出現在人為修改的資料庫。
- **O-3**：#19 O-3（`requirements.txt` 含 streamlit，Vercel function 的體積）仍由 #21 處理。worklog §4 也有記錄。
- **O-4**：README 的 `flask --app server run`，Reviewer 以 `python -m flask --app server run` 驗證，兩者是同一個 CLI。

## 6. 需要其他 authority 的事項

無。F-1 是已接受契約（R-DS-6）內的實作缺陷，用 targeted correction 處理即可，不需要改變設計或契約。F-2～F-9 都是 non-blocking，owner 與 disposition 已記錄在各項下。O-1 只有在 Design Authority 主動認為需要時，才會成為 scope class 標示的事項，本 audit 沒有 route。

## 7. 結論

實作主體符合已接受的契約，而且都經過 Reviewer 獨立驗證：
- Flask 單一 app 同時提供頁面與 `/api/`，只經共用模組讀取資料，沒有 SQL、沒有 HTTP client、沒有 CWA 引用（INV-1、INV-6、AC-04 a／b／c／d，F-4 的各種 import 寫法都會被抓到）。
- 六個 Region 的序列同時等於直接 SQL 查詢與 Grading App 實際顯示的表格（INV-2）。
- health 的 200／503 語義與 DR-7、DR-9 一致，12 種資料庫探測中，列舉的狀態全部回 503 JSON。
- 頁面文字、Region 順序與取得時間在真實瀏覽器中逐字相符（AC-02、AC-03、AC-24、INV-4），截圖是真實畫面。
- Vercel 結構可以在本機從其他工作目錄載入，執行期不需要任何環境變數。
- 在網路封鎖、沒有 `.env` 的環境下，134 個離線測試全部通過。25 個 probe 中，24 個是應該被抓到的 mutant，其中 22 個被抓到；沒被抓到的兩個只涉及可見文字的回歸保護（F-5）。另一個是 `urllib.parse` 的誤報檢查，正確地沒有觸發。
- H-1 掃描零命中。

有一項 blocking：

- **F-1**：R-DS-6 要求前端對 503／404 顯示明確訊息，但首次載入時 series 失敗，訊息會被寫進隱藏的面板，使用者看不到，已用故障注入在真實瀏覽器中重現。這可以用有界的 targeted correction 解決。

VERDICT: BLOCKING (F-1)
