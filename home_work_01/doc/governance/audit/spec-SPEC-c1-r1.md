# Audit record — Spec Integration Audit：SPEC v1.1（`home_work_01`），cycle 1，R1

| 項目 | 內容 |
| --- | --- |
| Outcome Contract | `home_work_01/doc/governance/outcome-contract.md`（ACCEPTED 2026-09-23；normative §1–7 ＝ `c45ec61`；acceptance boundary AB-1～AB-17） |
| Derived contract | `home_work_01/doc/spec/SPEC.md` **v1.1**（R-*、AC-01～AC-30、INV-1～INV-9、§7 AB→AC→R 矩陣）；derivation record `doc/governance/decisions/derivation-SPEC.md`（§4：**整個** AB-1～AB-17 分配給這唯一一份 Spec；§11：Tickets #18–#25） |
| 適用裁決 | `decision-20260923-high-risk-categories.md`（H-1／H-2／H-3、**A-2**、A-6）；`decision-20260923-spec-interpretation-rulings.md`（DR-1～DR-16）；DR-17（ingestion timestamp）；DR-18（AC-22）；DR-19（dashboard state mapping）；`decision-20260924-unattended-run-policy.md`。本 audit 依這些裁決判定，不重開。 |
| 受審 subject（最終整合 subject） | branch `home_work_01-hw10-implementation`，HEAD **`720c0a0e82cb51917457354ab829e1bce714a5eb`**（`origin` 相同，工作樹 clean）。派工所稱的 content subject 為 `75389e6`；本 audit 對 **HEAD `720c0a0` 的整個 `home_work_01/` 與兩個 RB-5 workflow 檔** 審查，並審查該 HEAD 產生的 Vercel preview 部署（見 §3）。`75389e6..720c0a0` 的 delta 見 F-1。 |
| Audit 種類 | **Spec Integration Audit**（治理 §4.7；impl-default §6），**cycle 1，R1**。獨立的 audit instance，不是任何 Ticket audit 的 R3；不重開已閉合的 Ticket finding。 |
| 角色 | `primary_reviewer`（`gov-primary-reviewer`） |
| Binding 證據 | 由派工者（Orchestrator）依 Bindings §3.4 從 harness 核對，記錄於 `home_work_01/doc/governance/run/run-20260924-hw01-formal.md`（本次派工：Spec Integration Audit，fresh Primary Reviewer）。Model diversity：Executor `claude-opus-4-8` 對 Reviewer `claude-opus-5-5`，存在。 |
| Independence（治理 §2.3） | Fresh context，未繼承 Executor 或任何 Ticket Reviewer 的對話；派工只給路徑與識別。所有 worklog、ACCEPTANCE.md 與 Ticket audit 的結論都當成待驗證主張，下面的判定都以 Reviewer 自己在磁碟、git、GitHub 與 live 部署上執行的檢查為依據。本 record 由 Reviewer 以 Write 寫入；未做任何 git 寫入，未改動任何追蹤檔案（審後 `git status --porcelain` 為空，`data.db` sha256 未變）。 |
| 執行時間 | 2026-09-24，約 03:00–03:25Z |

## 0. 審查方法與環境（Reviewer 自己執行）

- **乾淨匯出**：`git archive 720c0a0 home_work_01 .github` 匯出到 session scratchpad（沒有 `.git`、沒有 `.env`；已確認 `.env` 不存在）。
- **環境**：`uv venv --python 3.12` → CPython **3.12.14**；`uv pip install -r requirements.txt` → flask 3.1.2、pytest 8.3.3、streamlit 1.64.0、requests 2.32.3（pandas 3.0.6 為 streamlit 的傳遞相依）；無 folium。
- **網路隔離**：以 audit 用的 `sitecustomize.py` 攔截所有非 loopback 的 `socket.connect`／`getaddrinfo` 並記錄嘗試次數，另把 `HTTP(S)_PROXY` 指向無效位址、清除 `CWA_API_KEY`。
- **瀏覽器**：本機 Chrome headless，以 CDP（`Emulation.setDeviceMetricsOverride`、`Network`、`Runtime`）渲染與量測。注意：`--window-size=375` 在 Windows headless 下會被最小視窗寬度截成「以較寬版面排版再裁切」的假象，375 px 判定一律以 CDP 裝置模擬為準（見 §3.5）。
- **Live 部署**：公開 branch-preview alias `https://aiot-hw01-weather-git-homework01-hw10-im-8efc12-nchu-aiot-class.vercel.app`（不需登入）與 production `https://aiot-hw01-weather.vercel.app`。
- **GitHub**：`gh`（Actions runs、logs、deployments、issues、PR、variables）。

---

## 1. 範圍一：跨 Ticket invariants（INV-1～INV-9）；A-2 義務

### 1.1 A-2：老師的兩句驗證 SQL（對提交的 `data.db`）

對 `git show 720c0a0:home_work_01/data.db` 取出的 blob（sha256 `9bbf05bc6cc803444c8760432d6b484699c597f751fa16cb58bfbb5a0dbf542b`，與工作樹相同），以 `mode=ro` 唯讀開啟執行：

```
SELECT DISTINCT regionName FROM TemperatureForecasts;
  ('北部地區',) ('中部地區',) ('南部地區',) ('東北部地區',) ('東部地區',) ('東南部地區',)
  -> rows: 6

SELECT * FROM TemperatureForecasts WHERE regionName = '中部地區';
  (8,  '中部地區', '2026-09-24', 24.8, 32.8)
  (9,  '中部地區', '2026-09-25', 24.5, 32.8)
  (10, '中部地區', '2026-09-26', 24.5, 33.0)
  (11, '中部地區', '2026-09-27', 24.7, 32.8)
  (12, '中部地區', '2026-09-28', 24.8, 32.8)
  (13, '中部地區', '2026-09-29', 25.3, 32.0)
  (14, '中部地區', '2026-09-30', 24.3, 29.8)
  -> rows: 7
```

另外：`sqlite_master` 只有 `TemperatureForecasts`（`id INTEGER PRIMARY KEY, regionName TEXT, dataDate TEXT, mint REAL, maxt REAL`）與 `IngestionMetadata`；`PRAGMA index_list` 為空（沒有加索引或約束）；42 列、`(regionName, dataDate)` 重複 0、NULL 0、非 `YYYY-MM-DD` 的日期 0；`typeof` 為 integer／text／text／real／real；`IngestionMetadata` ＝ `(1, '2026-09-24T02:24:50+08:00', 'F-D0047-091')`。**結果：6 與 7，符合 R-DB-3／AB-6。** 這也是 A-6 release gate 所要求的「A-2 的 SQL 執行結果」。

### 1.2 逐項結論

| INV | 結論 | 在整合 subject 上的證據（Reviewer 自行取得） |
| --- | --- | --- |
| **INV-1** 查詢語義只有一份 | **HOLDS** | `app.py`、`server.py`、`api/index.py` 的 import 只有 stdlib／`pandas`／`streamlit`／`flask`／`weather_query`（`api/index.py` 另有 `urllib.parse.unquote_to_bytes`，不是 HTTP client）；三者都沒有 SQL 字串（grep `SELECT/INSERT/DELETE/UPDATE/CREATE TABLE/sqlite3` 只在 `weather_query.py` 與 ingestion 出現）；兩個呈現層都 `import weather_query as wq`。瀏覽器端的全部請求（CDP `Network.requestWillBeSent`）都是 same-origin，資料請求只有 `/api/health`、`/api/regions`、`/api/regions/<r>/series`、`/api/days`、`/api/days/<d>`。Dashboard 的 weekly summary 是對 `/api/` series 的純 min／max 彙總，Taiwan Map 直接以 endpoint 的 `colourBand` 著色（`app.js:392-393`），沒有 Region／Forecast Day 推導或 Derived Map Temperature 重算。`test_static_checks.py`（22 項）通過。殘餘：`REGION_ORDER` 在 `ingestion/config.py` 與 `weather_query.py` 各有一份（#19 F-8，已閉合 Low；兩者值相同）。 |
| **INV-2** 行為對等 | **HOLDS** | (a) 本機兩層：以 Streamlit `AppTest` 跑 `app.py`，逐一選六個 Region，讀出 dataframe 的 `(Date, MinT, MaxT)`，與 Flask test client `/api/regions/<r>/series` 及 `data.db` 直接查詢比較——**六區全部相等、各 7 列、欄名 `['Date','MinT','MaxT']`**；選項順序 `AppTest` ＝ `/api/regions` ＝ `REGION_ORDER`。(b) Live 部署：六區 `/series` 與本機 test client 回應**完全相等**；七個 `/api/days/<d>` 回應與本機完全相等。(c) 兩層實際渲染（Streamlit `streamlit run app.py` 與 live dashboard）顯示相同數值（例：北部地區 2026-09-24 → 23.3／31，2026-09-28 → 24.4／32.4）。Dashboard 的 MVM 不弱於 Grading App（同樣的標題、`Select Region`、折線圖、7 列表格、ingestion 時間；DR-9 規定的 incomplete 差異是裁決內容）。 |
| **INV-3** 快照恰 6 × 7、永不部分寫入（A-2、H-3） | **HOLDS** | 提交的 `data.db` 為 42 列、6 區 × 7 個連續日期（2026-09-24～09-30），無重複、無 NULL。**獨立推導**：Reviewer 依 OC §2.3 自寫推導（W1、只採 12 小時期間、丟棄不完整開頭日、Mapping A、算術平均 half-up 一位小數），從提交的 `data/raw/F-D0047-091.json` 算出 42 格，與 `data.db` **42／42 相等、0 不符**（原始 JSON 開頭有 6 小時的 `00:00–06:00` 段，依 R-DER-2／R-DER-4 的「兩段」定義不屬任何 Forecast Day；#18 R1 已記錄，結果相同）。**原子性**：對提交 DB 的副本呼叫 `persist_snapshot`，讓第 21 列在 DELETE 之後拋出 `KeyError` → 例外傳出，快照（42 列、metadata、數值總和 2355.7）**完全不變**（`with conn` rollback 了 DELETE）。**離線重建**：`python -m ingestion --from-json data/raw/F-D0047-091.json --db <scratch>` exit 0，重建結果與提交的 `data.db` 在列、metadata、schema 上**完全相同**；沒有出處 sidecar 時 exit 1、訊息指名缺少 provenance、不寫入（DR-17 §4.3）。 |
| **INV-4** 老師指定的名字不變（H-2、A-2） | **HOLDS** | `home_work_01/app.py`、`home_work_01/data.db`、`requirements.txt`、`README.md` 都在單元根目錄；`TemperatureForecasts` DDL 五欄名稱與型別逐字（§1.1）；六個 Region 中文全名含「地區」；`dataDate` 為 `YYYY-MM-DD`；老師 SQL 6／7（§1.1）。`streamlit run app.py` 在乾淨匯出的單元目錄可啟動（§3.4）。頁面文字：Grading App `Taiwan Weather Forecast`、`Select Region`、`Temperature Forecast – <Region>`、表頭 `Date`／`MinT`／`MaxT`、線名 `MaxT`／`MinT`；Dashboard `<title>` 與 `<h1>` 為 `Taiwan Weather Forecast`，`Select Region`、`Select Date`、表頭 `Date`／`MinT`／`MaxT`、圖例 `MaxT`／`MinT`、資訊卡 `Min`／`Max`（live CDP DOM 讀取與截圖）。 |
| **INV-5** 金鑰零外洩（H-1、A-2） | **HOLDS** | `git ls-files` 只含 `home_work_01/.env.example`；`home_work_01/.env` 被 `home_work_01/.gitignore:12` 忽略；`git log --all -- home_work_01/.env` 無任何 commit。Reviewer 在程序內讀取被忽略的 `.env` 金鑰值（**從未印出**，只確認它符合 CWA 金鑰格式），以**字面值**搜尋：512 個追蹤檔案 **0**；`git log -p --all` 全歷史（13,460,037 bytes）**0**；Issues #18–#25 與 PR #27 的 body 與全部 comments **0**；`doc/acceptance/screenshots/` 43 個檔案（逐 byte）**0**；`data/raw/`、`tests/fixtures/` **0**。CWA UUID 格式字串在上述位置皆 **0**；raw JSON 與 fixture 的 `Authorization` 值 **0**。Live 部署提供的 `index.html`、`app.js`、`styles.css`、`vendor/leaflet.{js,css}` 與 `720c0a0` 的 blob byte 相同（`/` 只多出 Vercel 注入的 `data-deployment-id`），且不含金鑰、`CWA_API_KEY` 或 `opendata.cwa.gov.tw`。`server.py`／`api/index.py` 不讀 OS 環境變數。CI（HEAD）`credential scan passed: 512 tracked files`。「Vercel 專案 env 未設定 CWA 金鑰」屬 acceptor 帳號狀態（RB-3，#21 F-3），如實標為 PENDING-ACCEPTOR（§2 AC-07）。殘餘：`--env PATH` 可從授權位置外讀金鑰（#18 F-6，已閉合 Low，不外洩）。 |
| **INV-6** 呈現層不呼叫 CWA | **HOLDS** | 同 INV-1 的 import 與 grep；live 頁面零外部請求（含地圖：Leaflet 與台灣輪廓都是 vendored／same-origin，沒有 tile server）；`test_static_checks.py` 通過。 |
| **INV-7** 標示要求（H-3、A-2） | **HOLDS** | README（HEAD）逐項引用：區域值標為 `PROJECT-DERIVED COMPATIBILITY VALUES` 且「never a CWA-issued six-region forecast」（:48-53）；對應表「project-defined, not an authoritative CWA grouping」（:37-47）；Derived Map Temperature「derived value … not an observed daily mean」（:275-282）；導言「derived from CWA county-level open data (not a CWA-published six-region product)」（:3-6）；代表點「not a CWA-published location or boundary」（:270-272）。Live 地圖圖例的註記為「Average = (MinT + MaxT) / 2, a derived value — not an observed daily mean.」，資訊卡寫「Derived map temperature 27.2 °C (derived, not an observed daily mean)」（CDP 截圖，1280 與 375）。兩層的「Last updated (data fetched from CWA)」標籤符合 DR-17 §4.5。在 README、`CONTEXT.md`、`index.html`、`app.js`、`app.py`、`server.py` 中搜尋 CWA／official／publish／issued，沒有任何相反措辭。 |
| **INV-8** Python 3.12 三處一致 | **HOLDS**（Vercel build log 的確認為 acceptor 項目） | 本機：Reviewer 的乾淨 venv 為 3.12.14，Executor 的紀錄亦同。CI：`home_work_01-ci.yml` `python-version: '3.12'`；HEAD run `35949866460` 的 log 為 `Python 3.12.14`。Vercel：`home_work_01/.python-version` ＝ `3.12`（部署設定）。Vercel build log 的確認需要 acceptor 的 Vercel 帳號權限（#21 F-3，RB-3），已如實標為 PENDING-ACCEPTOR。 |
| **INV-9** Scope class 分明 | **HOLDS** | `app.py` 沒有地圖、`Select Date`、folium／pydeck／`date_input`（grep）；Grading App 渲染（CDP）只有標題、ingestion 時間、`Select Region`、圖、表；`requirements.txt` 沒有 folium。`Select Date` 與 Taiwan Map 只出現在 Dashboard；README 把它們標為「enhanced, dashboard-only」（:252-257）。OPTIONAL 的排程更新沒有實作（兩個 workflow 都沒有 `schedule`）。 |

---

## 2. 範圍二：Spec-level AC coverage（AC-01～AC-30）與 AB-1～AB-17 的完整涵蓋

### 2.1 逐條 AC 判定

「本 audit」指 Reviewer 在最終 subject 或其 live 部署上自行取得的證據；「閉合的 Ticket audit」只作為補充引用，不取代本 audit 的判定。

| AC | 判定 | 證據 |
| --- | --- | --- |
| AC-01 | **PASS** | 本 audit：乾淨匯出的單元目錄執行 `streamlit run app.py --server.headless true` → `/_stcore/health` 200、`GET /` 200；CDP 渲染出 `Taiwan Weather Forecast`、ingestion 時間、`Select Region`、`Temperature Forecast – 北部地區`、7 列表格，沒有 exception。`test_app.py`（9 項）通過。截圖證據 `doc/acceptance/screenshots/ac01_home_default_region.png`。 |
| AC-02 | **PASS** | 兩層都有 `Taiwan Weather Forecast` 與 `Select Region`；選項恰為六區，順序 北部→中部→南部→東北部→東部→東南部（AppTest、Flask test client、live `/api/regions`、live DOM `select` 選項）。 |
| AC-03 | **PASS** | 六區（含中部、東南部）兩層都是 `MaxT`／`MinT` 兩條線、7 個日期；表格 `Date`／`MinT`／`MaxT`、7 列、升序，值 ＝ `data.db`（§1.2 INV-2 的比較）。Live 切換到東南部地區時標題與表格隨之更新（CDP）。 |
| AC-04 | **PASS** | (a)(c)(d)：§1.2 INV-1；(b)：live 的前端資料請求只有 same-origin `/api/`，靜態資源不含 CWA URL 或 `CWA_API_KEY`；`test_static_checks.py` 通過。殘餘：靜態掃描不遞迴 `static/vendor/`（#24 F-4，已閉合 Low；vendored Leaflet 已確認不含 CWA URL 或金鑰）。 |
| AC-05 | **PASS** | §1.1（提交的 `data.db`）；測試產生的 DB 由 `test_persist.py` 涵蓋（通過）。 |
| AC-06 | **PASS** | `test_persist.py`／`test_pipeline.py` 通過；提交的 DB 42 列、無重複；另見 §1.2 INV-3 的原子性與重建。 |
| AC-07 | **PASS**（(a)–(d)、(f) 已驗證；(e)「不需環境變數」已驗證；「Vercel 專案 env 未設 CWA 金鑰」＝PENDING-ACCEPTOR） | (a) 真實取得的紀錄在 `worklog/issue-18.md` 與 `worklog/issue-25.md` §5 步驟 4（不含金鑰）；(b)(c)(d)(f) 見 §1.2 INV-5（Reviewer 以字面值掃描，比 AC 要求的格式掃描更強）；(e) 依 AC 字面「Vercel 專案不需環境變數」：`server.py`／`api/index.py` 不讀環境變數，live 部署在沒有任何 secret 的情況下正常服務 → PASS。R-SEC-3 的「Vercel 專案不設定 CWA 金鑰」屬 acceptor 的帳號狀態，依 #21 F-3 的 disposition 如實記為 PENDING-ACCEPTOR（ACCEPTANCE.md:50、§5-3(c)），不是完成條件的缺口。 |
| AC-08 | **PASS** | `test_derive.py`（19 項）通過；§1.2 INV-3 以獨立推導 42／42 相符。 |
| AC-09 | **PASS** | `test_pipeline.py::test_ac09_negative_via_cli[missing_county／missing_half_day／invalid_value／only_six_days／non_consecutive]` 與 `test_derive.py` 的反例都通過（斷言不寫入、結束碼非零、訊息指名問題）。 |
| AC-10 | **PASS**（依 DR-19） | Grading App：`test_app.py` 的 missing／empty（明確訊息、無例外）與 incomplete（警告）通過。Dashboard：本 audit 以未修改的 `server.create_app(db_path=…)` 在本機服務三種 DB，CDP 渲染結果——missing：health 503，`role=alert`「Something went wrong — The forecast database is missing. Run the ingestion pipeline to create it.」；empty：503，alert「…contains no snapshot yet…」；incomplete：503，alert「…snapshot is incomplete…」；三者都沒有 JS exception、不是空白頁。對照組 ok：200，無 alert，7 列。 |
| AC-11 | **PASS** | `test_fetch.py`（13 項，mock HTTP：401／404／5xx／timeout／非 JSON）通過。 |
| AC-12 | **PASS** | Executor 在乾淨 3.12.14 venv 逐步執行的紀錄（`worklog/issue-25.md` §5，含真實取得一次）。本 audit 在另一個乾淨 venv 獨立重跑 README 的其餘步驟：建立 venv 並 `pip install -r requirements.txt`；離線重建（與提交的 DB 相同）；`streamlit run app.py`；`python server.py`（`GET /` 200、`/api/health` 200 ok、中部地區 series 200）；`pytest`（152 passed）；`python smoke.py <preview>`（SMOKE PASS）。Reviewer 沒有使用金鑰做真實取得（不必要，也不使用 acceptor 的憑證）。部署步驟：Vercel 專案設定屬 acceptor（README :296-302 如實標示），部署本身在運作（§3.3）。 |
| AC-13 | **PASS** | `git diff --stat origin/main...HEAD -- . ':!home_work_01'` 只有 `.github/workflows/home_work_01-ci.yml`、`home_work_01-smoke.yml`；PR #27 OPEN（`home_work_01-hw10-implementation` → `main`，head `720c0a0`）。合併屬 RB-1，不是完成條件。 |
| AC-14 | **PASS**（8／8） | Reviewer 依 HEAD 的 README 逐項核對：(1) :24-27；(2) :28-30；(3) :31-36；(4) :37-47；(5) :48-53；(6) :275-280；(7) :194-206（與 OC §2.4 一致，包括「compatibility accommodation … not a sign that Streamlit was outside the assignment」）；(8) 全文與 UI 文字都沒有相反措辭（§1.2 INV-7）。ACCEPTANCE.md §2 引用的行號與 HEAD 相符。 |
| AC-15 | **PASS**（受審 commit 的公開 preview）；production smoke ＝ release evidence（DR-12） | 本 audit：`python smoke.py <alias>` → `[2026-09-24T03:09:32Z] attempt 1 … GET / -> 200  GET /api/health -> 200 (1.1s elapsed) PASS`、`SMOKE PASS`、exit 0；不需登入；`<title>Taiwan Weather Forecast</title>`；`/api/health` ＝ `{"forecast_day_count":7,"ingestion_time":"2026-09-24T02:24:50+08:00","region_count":6,"status":"ok"}`。**部署與 commit 的對應**：alias 服務 `data-deployment-id="dpl_43PManN2R1XtR4cqh54XriruxZ1X"`，它就是 deployment `6629243424` 的 environment URL（`aiot-hw01-weather-4wvevgdju-…`）的 deployment id，而 `gh api …/deployments` 顯示 `6629243424` 的 sha ＝ **`720c0a0`**（Preview，status success）。所以 live 部署就是受審 HEAD 的建置。Production（`aiot-hw01-weather.vercel.app`）目前 `/` 與 `/api/health` 都是 404；`smoke.py` 對它 exit 1——這是合併前的預期狀態（DR-12），如實記為 release evidence（ACCEPTANCE.md:58、§5-2）。 |
| AC-16 | **PASS** | `test_dashboard.py`：health 200 以及 missing／empty／incomplete／mismatched-dates 的 503；live health 200 且欄位齊全（AC-15）。 |
| AC-17 | **PASS** | Live（CDP，1280）：地圖以台灣為中心，六個標記都在初始視野內，有縮放控制；六個標記的 fill 都是 `#f2b705` ＝ 圖例 yellow 色塊 `rgb(242,183,5)`，且 `/api/days/<d>` 對全部 42 格回 `colourBand: "yellow"`（本快照的 Derived Map Temperature 都在 25～<30），`derivedMapTemperature`／`colourBand` 與 `wq.derived_map_temperature`／`wq.colour_band` 逐格相等；側欄資訊卡顯示 Region、`Date`、`Min`、`Max` 與導出平均（例：北部地區 2026-09-24：23.3／31／27.2）；圖例四段並附導出說明；底圖不需金鑰（vendored，零外部請求）。四種顏色的分帶呈現另有 #24 的證據（`issue-24-map-bands-4colours.png`，閉合的 #24 audit）。 |
| AC-18 | **PASS** | `Select Date` 列出 2026-09-24～09-30 共 7 天、升序、預設第一天（live DOM）；以 CDP 切換到 2026-09-30 → 頁面顯示「Showing 2026-09-30」，並請求 `/api/days/2026-09-30`，該回應與本機 shared module 相等。打開中的 popup 在換日期時會更新（#24 F-1 已在 #24 R2 閉合）。 |
| AC-19 | **PASS** | 本 audit（live、CDP 裝置模擬）：375 px 時 `scrollWidth` 375 ＝ `innerWidth` 375，沒有任何元素超出視窗；1280 px 時 `scrollWidth` 1265 ≤ 1280；兩種寬度都能完整操作（截圖）。(1) 視覺層級、(3) 摘要（Weekly summary 兩張 stat tile）、(4) 圖表有圖例、軸標籤與 hover tooltip、(5) error 狀態由本 audit 在三種 DB 條件下驗證（AC-10），empty 與 loading 的截圖為 `issue-24-state-empty.png`（2xx 空 regions → 「No forecast data yet」，符合 DR-19）與 `issue-24-state-loading.png`；(6) 如上。R-EN-2 的概念詞都保留。 |
| AC-20 | **PASS** | HEAD `720c0a0` 的 push run `35949866460` 與 pull_request run `35949869391` 都是 success；log 顯示 `Python 3.12.14`、`152 passed in 4.11s`，每個檔案的 PASSED 行涵蓋 derive（`test_derive`）、DB（`test_persist`）、shared module（`test_weather_query`）、`AppTest`（`test_app`）、Flask test client（`test_dashboard`）；之後 `credential scan passed: 512 tracked files`。以 PyYAML 解析 `720c0a0` 的 workflow：`on.push.paths` ＝ `['home_work_01/**', '.github/workflows/home_work_01-ci.yml']`（pull_request 相同），所以不含本單元變更的 push 不會觸發。 |
| AC-21 | **PASS** | 本 audit：乾淨匯出、無 `.env`、網路攔截 → **152 passed**，**BLOCKED_ATTEMPTS=0**。每個檔案的收集數：test_app 9、test_dashboard 23、test_derive 19、test_fetch 13、test_persist 5、test_pipeline 19、test_secrets 4、test_static_checks 22、test_vercel_path_decoding 9、test_weather_query 29，涵蓋 R-TC-1／R-TC-3／R-TC-4 的項目（含 AC-09 的五個反例、AppTest 的 missing／empty／incomplete、每個 endpoint 的 404／503）。 |
| AC-22 | **PASS**（DR-18：(a)(b) 已驗證；(c) 為 release evidence，待 RB-1 後 dispatch） | (a) 本 audit 用與 workflow 相同的 `smoke.py`（`720c0a0`）對受審 subject 的公開部署執行 → 200／200、`SMOKE PASS`、exit 0（AC-15）；對 404 的 production 則 exit 1，證明失敗語義正確。(b) `home_work_01-smoke.yml` 以 PyYAML 解析：`on` 只有 `workflow_dispatch`（選用的 `url` input，預設為空字串）；step 用 env 傳入 `inputs.url` 與 `vars.HW01_DEPLOY_URL`，兩者皆空時明確失敗，在 `home_work_01` 下執行 `python smoke.py "$URL"`；`permissions: contents: read`；沒有 `secrets.*`；action 骨架與 CI 相同，而 CI 已在 HEAD 實跑成功。Repository variable `HW01_DEPLOY_URL` 已設定。(c) `gh api …/actions/workflows/home_work_01-smoke.yml` → 404；`origin/main` 的 `.github/` 路徑數為 0 → 合併前無法 dispatch。依 DR-18 如實記為 release evidence（ACCEPTANCE.md:65、§5-1）。 |
| AC-23 | **PASS**（本機、CI、Vercel 設定三處；Vercel build log 的確認為 acceptor 項目） | 見 INV-8。AC 的條件是「Vercel 部署日誌**或設定**顯示 Python 3.12」，`.python-version` ＝ `3.12` 就是部署設定；build log 的補充確認依 #21 F-3 由 acceptor 在 RB-3 範圍內提供。 |
| AC-24 | **PASS** | Grading App 的 caption 為「Last updated (data fetched from CWA): 2026-09-24T02:24:50+08:00」（AppTest 與實際渲染）；Dashboard 的 live DOM 與 `/api/health.ingestion_time` 為同一值；都等於 `IngestionMetadata.ingestedAt`，也等於提交的 sidecar `data/raw/F-D0047-091.meta.json` 的 `acquiredAt`（DR-17）。`TemperatureForecasts` DDL 未變（§1.1）。 |
| AC-25 | **PASS** | 提交的 `data/raw/F-D0047-091.json`（1,695,726 bytes）與 `json.dumps(json.loads(raw), indent=2, ensure_ascii=False)` byte 相同（完整、縮排、未加工），不含金鑰或 `Authorization`；離線 derive 印出 42 列預覽與「rows: 42 \| regions: 6 \| date range: 2026-09-24 .. 2026-09-30」（本 audit 執行）；fetch 摘要的輸出在 `worklog/issue-25.md` §5a；README 在 :149-169 說明結構與觀察產物的位置。 |
| AC-26 | **PASS** | `app.py` 及其 import（`weather_query`、pandas、streamlit）不含地圖、`Select Date`、folium；`requirements.txt` 沒有 folium；乾淨安裝後的環境也沒有 folium；Grading App 渲染不含地圖。 |
| AC-27 | **PASS**（Reviewer 的正式結論） | R-DOC-5 四項：(1) 每個 Python 模組都有說明目的的 module docstring，主要函式都有 docstring（AST 掃描只有四個小型 CLI helper 沒有：`smoke.main`、`pipeline.build_parser`、`credential_scan.tracked_files`／`run`，都是自明的入口，見 O-4）；JS／HTML／CSS 有檔頭與分段註解。(2) 錯誤處理與明確訊息：`FetchError`／`DeriveError`／`ProvenanceError` → `Ingestion failed: …`、exit 1、不寫入；`SnapshotError` 防止 SQLite 原始錯誤外洩；API 錯誤為含 `error` 的 JSON；兩層的缺失／空／不完整狀態都有明確訊息。(3) 沒有死碼與未使用的相依：`pyflakes` 對全部單元 Python（含 tests）無輸出；`vulture` 只回報 Flask route 與 `row_factory` 這類框架誤報，以及測試使用的 `scan_file`；四個 pinned 相依各有用途（requests→ingestion、pytest→tests、streamlit→`app.py`、flask→`server.py`）；pandas 為傳遞相依（#19 F-10，已閉合 Low）。(4) 結構對應資料流：`ingestion/`（fetch→derive→persist，pipeline CLI）→ `data.db` → `weather_query.py` → `app.py`／`server.py`＋`static/`，README :429-446 對應到海報的 `HW10_Weather/`。 |
| AC-28 | **PASS** | `test_weather_query.py` 的色帶／導出值案例通過；前端不重算（`app.js:392`），live 著色與 shared module 相等（AC-17）。本 audit 另以 live 值手算：北部地區 2026-09-24 為 (23.3 + 31.0)/2 ＝ 27.15 → half-up 得 27.2，與 endpoint 和畫面一致。 |
| AC-29 | **PASS** | 授權原文在 OC §8.2 第 2 點；兩個 workflow 的名稱都識別本單元（`home_work_01 CI`、`home_work_01 deploy smoke`）；CI 的 path filter 為 `home_work_01/**` 加上 CI 檔本身；smoke 只有 `workflow_dispatch`；root 沒有其他改動（AC-13）。 |
| AC-30 | **PASS**（Root Directory 的設定截圖為 acceptor 項目） | `vercel.json`、`api/index.py`、`requirements.txt`、`.python-version`、`data.db` 都在 `home_work_01/`；root 沒有 `vercel.json`／`requirements.txt`／`app.py`／`data.db`。功能上的佐證：live 部署確實由 `home_work_01/vercel.json` 的單一 `@vercel/python` function 服務（`/`、`/static/*`、`/api/*` 都回應正確），只有 Root Directory ＝ `home_work_01` 時才會如此。Vercel 後台的設定截圖屬 acceptor（RB-3，#21 F-3）。 |

**AC 判定彙總**：30／30 PASS；FAIL 0。其中四條附有依既有裁決、如實記錄的 acceptor／release 項目：AC-15（production smoke，DR-12）、AC-22(c)（live `workflow_dispatch`，DR-18）、AC-07 的 Vercel env 確認、AC-23 的 build log 確認與 AC-30 的後台截圖（#21 F-3，RB-3）。這些都不是 coverage failure；現有授權下能取得的部分，本 audit 都已實際驗證（公開 preview 的 smoke 與部署↔commit 對應、workflow 交付物、`.python-version` 設定、root 無設定檔、runtime 不讀 env）。Reviewer 不爭議這些 disposition。

### 2.2 AB-1～AB-17 的涵蓋（治理 §4.7 最後一份 Spec 的核對）

- 只有一份 derived Spec：`home_work_01/doc/spec/` 只有 `SPEC.md`；derivation record §4 把 **AB-1～AB-17 全部**分配給它。所以「全部 derived Specs 的分配合起來涵蓋整個 acceptance boundary」這項核對，就是核對這一份 Spec 的 AC 是否涵蓋全部 17 條 AB。
- Spec §7 矩陣、derivation §4 表、ACCEPTANCE.md §4 三者的 AB→AC 對應一致：AB-1→AC-15、AC-16；AB-2→AC-01；AB-3→AC-02；AB-4→AC-03；AB-5→AC-04；AB-6→AC-05；AB-7→AC-06；AB-8→AC-07；AB-9→AC-08、AC-09；AB-10→AC-10、AC-11、AC-16；AB-11→AC-12、AC-25；AB-12→AC-13；AB-13→AC-14；AB-14→AC-17、AC-18、AC-28；AB-15→AC-19；AB-16→AC-20、AC-21；AB-17→AC-22。**17／17 都有至少一條 AC，而且這些 AC 在 §2.1 都判定為 PASS。** 其餘 AC-23／24／26／27／29／30 對應 OC §2.1／§2.4／§2.5／§4 的 constraints，沒有擴張 boundary。
- 實質涵蓋：各 AC 的 PASS 條件逐一承接 AB 的可觀察條件與證據類別（例：AB-1 的「允許最多 90 秒暖機」→ AC-15 與 `smoke.py --timeout 90`；AB-5 的「靜態檢查＋查詢語義只有一份」→ AC-04 (a)–(d)；AB-10 的「兩層＋ingestion」→ AC-10＋AC-11＋AC-16；AB-17 的「workflow 執行紀錄」→ AC-22(c)，依 DR-18 在 release 時交付）。
- **分配缺口：無。造成歧義的重疊：無**（AB-10 由三條 AC 分別承接 Grading App、Dashboard 與 ingestion；AB-1 由 AC-15（公開 URL）與 AC-16（health 語義）承接，兩者不衝突）。

---

## 3. 範圍三：整合行為

### 3.1 Ingestion → `data.db`

提交的 raw JSON 加上 provenance sidecar，經離線重建，得到與提交的 `data.db` 完全相同的列、metadata 與 schema；獨立推導 42／42 相符；缺少 provenance 時 fail-closed；寫入中途失敗時快照不變（§1.2 INV-3）。Ingestion 時間從 sidecar 一路傳到 `IngestionMetadata`，再由 shared module 傳到兩層與 `/api/health`，值完全相同（AC-24）。

### 3.2 `data.db` → shared module → 兩個呈現層（INV-2 比較）

以 `AppTest`（Grading App）、Flask test client（Dashboard API）與直接 SQL 做三方比較：六區各 7 列，全部相等；Region 順序三方相同（§1.2 INV-2）。兩層實際渲染的數值相同（Streamlit 的 CDP 截圖與 live dashboard 的截圖）。

### 3.3 部署的 dashboard（live，審查 HEAD 的建置）

- Alias → `dpl_43PManN2R1XtR4cqh54XriruxZ1X` → GitHub deployment `6629243424` → commit **`720c0a0`**。
- `GET /` 200、`text/html`，`<title>` 與 `<h1>` 都是 `Taiwan Weather Forecast`；`/api/health` 200 `status: ok`、6、7、`2026-09-24T02:24:50+08:00`；`/api/regions` 200，六區依固定順序；`/api/days` 200，7 天。
- 六個 Region 的 percent-encoded `/series`（#21 F-1 的修正路徑）都是 200，與本機 shared module 相等；七個 `/api/days/<d>` 都是 200 且相等；未知 Region（`台北地區`）與未知日期都回 404 JSON，含 `error`。未定義的 `/api/nope` 回 HTML 404（#20 F-3，已閉合 Low；R-DS-3 只要求未知 Region／日期回 JSON）。
- Live 靜態資源與 `720c0a0` 的 blob byte 相同（§1.2 INV-5）。
- CDP 渲染（1280 與 375 裝置模擬）：圖表、表格、摘要、`Select Date`、六個地圖標記、圖例與導出說明都正常；`Runtime.exceptionThrown` 0 筆、console error 0 筆；全部網路請求都是 same-origin（`/`、`/static/*`、`/static/vendor/*`、`/api/*`、`/favicon.ico`）。

### 3.4 本機兩個執行形態

- `streamlit run app.py`：啟動並渲染（AC-01）。
- `python server.py`（README 的指令）：`GET /` 200、health 200、中部地區 series 200。
- 錯誤狀態的整合（DR-19）：缺失／空／不完整的 DB → health 503 → 頁面顯示紅色 `role=alert` error 並帶出伺服器訊息（AC-10）。

### 3.5 關於 375 px 的量測方法

`chrome --headless=new --window-size=375,…` 截圖看起來右側被裁切，但原因是 Windows headless 的最小視窗寬度：版面以較寬的 viewport 排版，再裁成 375。改用 CDP `Emulation.setDeviceMetricsOverride(width=375, mobile=true)` 後，`innerWidth` ＝ `scrollWidth` ＝ 375，沒有元素超出視窗，版面為單欄（截圖）。這不是缺陷，AC-19 的判定以裝置模擬的量測為準。

**整合行為的結論：各部分可以一起運作；沒有發現整合層級的缺陷。**

---

## 4. 範圍四：最終 subject 的 verification／audit coverage（治理 §3.8；impl-default §7）

- **Verification**：(1) 本 audit 在 `720c0a0` 的乾淨匯出上跑完整離線 pytest，152 passed，無網路、無 `.env`；(2) CI 對 `720c0a0` 的 push 與 pull_request 都成功（`35949866460`、`35949869391`：Python 3.12.14、152 passed、credential scan passed）；(3) Live 部署就是 `720c0a0` 的建置，smoke PASS。三者都直接對應最終 subject，不需要透過 anchor 推論。
- **Audit coverage**：#18–#25 每張 Ticket 都有閉合的 independent audit record。最後一行的 verdict：#18、#19、#20、#21、#23、#24、#25 的 R1 為 BLOCKING、R2 為 **CLOSURE**；#22 的 R1 為 **CLOSURE**（AC-22 另依 DR-18）。GitHub Issues #18–#25 都是 CLOSED，每張票各有一則結案 comment。本 record 就是 Spec 層級的 audit。
- **Post-review deltas**：`#25` R2 審查的是 `75389e6`；`75389e6..720c0a0` 改了 `doc/governance/**`（audit／run record）與 `doc/ticket/tickets.md`（#25 狀態列）。本 audit 直接以 `720c0a0` 為 subject，所以這段 delta 已在本 audit 的 coverage 內（識別方式的說明見 F-1）。
- **Gates**：Bindings §5 的「無追蹤中的機密」已獨立驗證（§1.2 INV-5）；「README 的步驟實際跑過」已有 worklog 紀錄，並由本 audit 部分重跑（AC-12）。
- **結論：最終 subject 具有有效的 verification 與 audit coverage。**

---

## 5. 範圍五：Spec／Tickets → Outcome Contract 的 traceability 與 boundary 符合性

### 5.1 Traceability 鏈

- **OC → Spec**：Spec 標頭記載 derive 自 OC `c45ec61`；OC §8 的接受紀錄把 Spec v1.1 列為隨接受生效的 derived contract；derivation §2 逐條對應 OC 條款，§3 為 boundary determination，§4 為 AB 分配。
- **Spec → Tickets**：derivation §11.1／§11.2 的分配表；本 audit 抓取 Issue #18–#25 的 body，每張都引用 `SPEC.md` 與自己的 `worklog/issue-<n>.md`。各 Issue body 所列 AC 的聯集為 AC-01～AC-30，**30 條全部涵蓋**（例：AC-05／06／08／09／11 在 #18；AC-12／13 在 #25；AC-16 在 #20；AC-17／18 在 #24；AC-20／21／29 在 #22；AC-26 在 #19、#23）。`doc/ticket/tickets.md` 的索引與 Issue 狀態一致（全部已結案，並填有結案 SHA）。
- **Tickets → evidence**：每張票都有 worklog 與 audit record；ACCEPTANCE.md（R-DOC-4）逐條對應 AC、INV 與 AB，並引用 evidence。
- 結論：traceability 鏈完整且一致。紀錄層面有兩個小問題，見 F-1 與 F-2。

### 5.2 Boundary 符合性

- **單元外的改動**：只有 OC §8.2 授權的兩個 workflow 檔，兩者都以 path filter 限定本單元，或只能 `workflow_dispatch`（AC-13、AC-29）。沒有其他 root 或其他單元的檔案被改動（RB-5）。
- **沒有超出 accepted boundary 的內容**：實作出的功能都對應 OC §2.2 的 MVM 或 ENHANCED REQUIRED，或 Spec／DR 的決定——provenance sidecar 來自 DR-17；`smoke.py` 來自 R-TC-7；credential scan 來自 A-5；weekly summary 來自 R-EN-1(3)；`?region=` 深連結是 ENHANCED UI 內的 HOW。OPTIONAL 的排程更新沒有做；REFERENCE 項目（React、FastAPI、Windy、folium、Streamlit 部署）都沒有出現。ENHANCED 項目在 README 都標為 dashboard-only 的 enhanced 功能，沒有被寫成老師的要求。
- **沒有 reserved action 被 Agent 執行**：沒有合併到 `main`（`origin/main` 仍為 `d42b1a7`，沒有 `.github/`）；沒有繳交；Vercel 與 repository variable 由 acceptor 設定；沒有付費；沒有破壞性 git 操作。
- **Boundary 疑義：無。不需要 route 到 Design Authority。**

---

## 6. Findings

### F-1 — 「content subject `75389e6`」的說法不完全精確：`75389e6..720c0a0` 也改了不屬於 record-only 路徑的 `doc/ticket/tickets.md`

- **Severity**：Low　**Blocking**：否
- **證據**：`git diff --name-only 75389e6 720c0a0` → `home_work_01/doc/governance/audit/issue-25-c1-r1.md`、`…/issue-25-c1-r2.md`、`…/run/run-20260924-hw01-formal.md`，**以及 `home_work_01/doc/ticket/tickets.md`**（#25 那一列從「待執行」改為「已結案」並填入 `75389e6`）。Bindings §7 明定 record-only paths **只有** `doc/governance/**`。派工內容與 run record :96 都把這段 delta 描述為 record-only。
- **契約依據**：Bindings §7；impl-default §7（每個 verification／audit 結果都 MUST 識別它涵蓋的 subject 版本）；orch-default §7 P7。
- **影響**：對 coverage 沒有影響——本 audit 以 `720c0a0` 為 subject，也直接驗證了 `720c0a0` 的 CI 與部署。這個改動只是索引的狀態欄，不影響任何產品行為。
- **Disposition**：Owner 為 Orchestrator。DA phase acceptance 與 Orchestrator 的完成報告應寫明「Spec Integration Audit subject ＝ `720c0a0`」，不要寫成「content subject `75389e6`（delta 為 record-only）」。之後若只有 `doc/governance/**` 的 commit，subject 仍是 `720c0a0`；如果還會再改 `doc/ticket/`，也應同樣識別。若希望索引檔被視為 record-only，那是 Bindings 的變更（acceptor），不是必要動作。

### F-2 — 待處理的追蹤項目 #18 R2 N-1（Medium）在交付文件中沒有具名 owner

- **Severity**：Low　**Blocking**：否
- **證據**：`doc/acceptance/ACCEPTANCE.md:172` 寫「Orchestrator to assign the owner (the item had no owner after #25 closes)」，同一列還把「value is written verbatim」稱為「Fail-closed today」（實際上是 fail-open，#25 R2 N-2(a) 已指出）。Run record :99 寫「new post-#25 owner (acceptor to authorize a Lightweight follow-up)」。這個項目原本在 run record :91 被分派給 #25，但 #25 以「超出 doc-only 範圍」為由沒有處理。
- **契約依據**：治理 §4.3「Non-blocking findings MUST 記錄 disposition；需後續處理者須有 owner」；decision A-4（觸及 H-3／DR-17 的結案後修正需要 independent audit）；Bindings §4 第 3 列（結案後的單點修正屬 Lightweight，需要 acceptor 的直接指示）。
- **本 audit 不重開 N-1 本身**，因為沒有新的整合層級證據：提交的 `data.db` 與 sidecar 都是合法的 ISO 8601 `+08:00` 值（`2026-09-24T02:24:50+08:00`），離線重建可以重現它，兩層顯示也正確（§1.2 INV-3、AC-24）。風險只存在於操作者日後手動傳入格式錯誤的 `--acquired-at` 或 sidecar 時，這正是 #18 R2 已記錄的內容。
- **Disposition**：Owner 為 Orchestrator。在完成報告中具名列出此追蹤項目與其 owner（例如：「Orchestrator 向 acceptor 提出；acceptor 授權後成為結案後的 Lightweight work item；依 A-4 需要 independent audit」）；DA phase acceptance 把它列為未結的 follow-up。ACCEPTANCE.md 的措辭可以一併更正，但不是必要條件。

### 觀察（不是 finding，不需要處理）

- **O-1**：375 px 的 headless 截圖假象，見 §3.5。
- **O-2**：準備好的快照涵蓋 2026-09-24～09-30，之後就會過期。這是 OC 已接受的語義（Q3 A：MVM 使用準備好的快照，refresh 屬 OPTIONAL），不是缺陷；程式與測試都沒有依賴「今天」的日期（grep 只有 `pipeline.ingestion_timestamp` 與 `smoke.py` 的 log 時間戳），所以測試不會因時間經過而失敗。若 acceptor 在繳交（RB-2）前想更新資料，那次 Refresh 會改動 `data.db`，屬 Bindings §4 第 3 列的結案後修正，而且觸及 H-2／H-3，依 A-4 需要 independent audit。
- **O-3**：Dashboard 頁面本身沒有把區域值標為「推導值」。契約不要求：AB-13／R-DOC-2 要求的是技術文件，R-EN-5 只要求地圖溫度的導出標示；而頁面上也沒有任何相反措辭，AC-14(8) 成立。
- **O-4**：四個小型 CLI helper 沒有 docstring（見 AC-27），不影響 R-DOC-5 的 PASS。
- **O-5**：ACCEPTANCE.md 中已知的紀錄小問題（#25 R2 N-1／N-2，已閉合）仍然存在：§0 把 `6407d8b` 稱為「Final subject」；tracked-file 數寫成 508／510，而 HEAD 的 CI 現在是 512（因為之後加入了 record 檔）；章節順序為 §6→§8→§7。本 audit 不重開；DA phase acceptance 引用時應以本 record 的 subject（`720c0a0`）為準。

---

## 7. 高風險類別（decision A-1／A-2）

- **H-1**：INV-5 HOLDS（§1.2），並以金鑰字面值掃描追蹤檔案、全歷史、Issue／PR 文字、截圖與 live 資源。**PASS**。
- **H-2**：INV-4 HOLDS；老師 SQL 6／7（§1.1）。**PASS**。
- **H-3**：INV-3 與 INV-7 HOLDS；以獨立推導 42／42 相符；Derived Map Temperature 與色帶都只在 shared module 算一次，live 值與 shared module 相等；標示逐項核對。**PASS**。

## 8. 需要其他 authority 的事項

- **Design Authority**：不需要 routing——沒有契約語義不足，也沒有 boundary 疑義。DA phase acceptance（治理 §3.8）可以引用本 record；請同時留意 F-1（subject 應寫 `720c0a0`）與 F-2（未結的 follow-up）。
- **Final Adjudicator**：不需要。
- **Acceptor**（已在既有裁決中記錄的 release／RB 項目，本 audit 不爭議，也不視為缺口）：RB-1 合併之後的 AC-22(c) live `workflow_dispatch` run（DR-18）與 production URL smoke（AC-15，DR-12）；#21 F-3 的 Vercel 後台項目——Python 3.12 的 build log、Root Directory 截圖、「Vercel 專案 env 未設定 CWA 金鑰」的確認（RB-3）；是否授權 #18 R2 N-1 的結案後 Lightweight 修正（F-2）；RB-2 繳交。

## 9. 結論

五個範圍都成立：跨 Ticket invariants INV-1～INV-9 在整合 subject 上都成立（A-2 的 INV-3／4／5／7 已逐項核對，老師 SQL 對提交的 `data.db` 得到 6 與 7）；AC-01～AC-30 全部 PASS，acceptor／release 項目都依 DR-12／DR-18／#21 F-3 如實記錄；AC 合起來涵蓋整個 AB-1～AB-17，沒有缺口或歧義重疊；ingestion → `data.db` → shared module → 兩個呈現層 → live 部署的整合行為正確，兩層對等；最終 subject `720c0a0` 有有效的 verification 與 audit coverage；Ticket → Spec → OC 的 traceability 完整，也沒有超出 accepted boundary 的內容。兩項 findings（F-1、F-2）都是 Low，屬 non-blocking，已記錄 owner。

VERDICT: CLOSURE
