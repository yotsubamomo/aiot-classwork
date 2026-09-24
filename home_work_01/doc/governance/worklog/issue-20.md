# Worklog — Issue #20（Dashboard MVM：Flask `/api/` 與靜態頁面）

| 欄位 | 內容 |
| --- | --- |
| Work item | GitHub Issue #20（`yotsubamomo/aiot-classwork`），Formal lane，Scope class MVM |
| 所屬 Spec | `home_work_01/doc/spec/SPEC.md` v1.1（EFFECTIVE）：R-DS-1…R-DS-8（結構部分）、R-SHR-5（JS 側）、R-SEC-3、R-TC-4、R-TC-5、R-DOC-1、R-DOC-5；§4.1、§4.2、§5 |
| Outcome Contract | `home_work_01/doc/governance/outcome-contract.md`（ACCEPTED 2026-09-23） |
| 依據裁決 | DR-1、DR-2、DR-7、DR-8、DR-9、DR-17；高風險 H-1、H-2、A-1 |
| Prior-ticket follow-up | issue-19 R1 finding **F-4**（owner #20）：強化 AC-04(a) 靜態 HTTP-client 檢查 |
| Branch | `home_work_01-hw10-implementation`，BASE `592c9ed` |
| Executor | `gov-executor`（Bindings §3.1：`claude-opus-4-8`／`high`） |
| 狀態 | DONE（cycle 1 R1 blocking F-1 已 targeted correction；待 R2 closure review） |

## 1. Contract 摘要與 HOW 選擇

在 accepted contract 內自主選擇的 HOW（DR-1 未凍結者，Spec §4.2）：

- **後端**：單一 Flask 應用 `home_work_01/server.py`，`create_app(db_path=None)` factory，模組層 `app = create_app()` 供 Vercel。`GET /` 回 dashboard 頁面，`/api/` 前綴的 JSON endpoints，靜態資源由同一應用經 `/static/` 提供（R-DS-1）。資料只經 `weather_query.py`（R-DS-5、INV-1），不 import HTTP client，無 CWA URL／`CWA_API_KEY`（R-SHR-5、H-1）。
- **Vercel 結構**（brief §5.2 teacher-verified pattern；只建結構、本機驗證，不部署——#21）：`api/index.py` 把上層加入 `sys.path` 後 `from server import app`；`vercel.json` builds/routes 單一 function 接全部路由；`requirements.txt` 加 `flask`（pinned）；`data.db` 隨程式打包（`weather_query` 以原始碼位置解析路徑，已由 #19 實作）；執行期不需環境變數（R-DS-8 結構、R-SEC-3）。
- **API endpoints**（HOW，`/api/` 前綴，README 文件化）：
  - `GET /api/health`（DR-7／R-DS-2）
  - `GET /api/regions`（R-SHR-2(b) Region 清單）
  - `GET /api/regions/<region>/series`（R-SHR-2(c) 指定 Region 七日序列）
  - `GET /api/days`（R-SHR-2(e) Forecast Day 清單）
  - `GET /api/days/<date>`（R-SHR-2(d) 指定 Forecast Day 六區值，含 Derived Map Temperature）
  - 未知 Region／date → 404 JSON `error`；快照非 ok（missing／empty／incomplete）→ 503 JSON `error`（DR-9）
- **前端**：靜態 HTML／CSS／JS，無 build step；MaxT／MinT 折線圖以 vanilla-JS inline SVG 繪製（無外部相依、免金鑰、離線可用，符合 R-EN-6 精神且避免 CDN／CSP 風險）。資料只從本應用 `/api/`（R-SHR-5、AC-04(b)）。503／404／網路失敗顯示明確訊息（R-DS-6）。ingestion 時間依 DR-17 §4.5 標籤。
- **F-4**：強化 `tests/test_static_checks.py` 的 ImportFrom 偵測（`from urllib import request`、`from urllib.request import ...`、`from http import client`），並把 Flask 後端納入 Python-side 靜態檢查範圍。

## 2. 進度（完成）

新增／修改（全部在 `home_work_01/` 內）：

| 檔案 | 內容 |
| --- | --- |
| `server.py`（新增） | Flask 後端，`create_app(db_path=None)` factory＋模組層 `app`。`GET /`→頁面；`/api/health`、`/api/regions`、`/api/regions/<region>/series`、`/api/days`、`/api/days/<date>`；503／404 JSON `error`。只經 `weather_query` 讀資料。 |
| `api/index.py`（新增） | Vercel serverless 入口：`sys.path` 加單元目錄後 `from server import app`（brief §5.2）。 |
| `vercel.json`（新增） | 單一 function 接全部路由（builds/routes）；`includeFiles: data.db`。 |
| `static/index.html`、`static/styles.css`、`static/app.js`（新增） | 靜態前端，無 build step；標題、`Select Region`、inline-SVG MaxT／MinT 折線圖、`Date`／`MinT`／`MaxT` 表格、ingestion 時間；503／404／網路失敗顯示明確訊息；`?region=` deep link。`[hidden]{display:none!important}` 確保錯誤狀態不殘留空控制項。 |
| `requirements.txt`（修改） | 新增 `flask==3.1.2`。 |
| `tests/test_dashboard.py`（新增） | Flask test client 覆蓋（見 §3）。 |
| `tests/test_static_checks.py`（修改） | **F-4**：ImportFrom 偵測 `from urllib import request`／`from urllib.request import ...`／`from http import client`；把 Flask 後端納入 AC-04(a)(c)(d)；新增前端 AC-04(b) 檢查。 |
| `README.md`（修改） | 新增「Run the dashboard (Flask) locally」段與 `/api/` endpoint 清單；更新 scope 註與海報對應表。 |
| `doc/acceptance/screenshots/ac02_dashboard_default.png`、`ac03_dashboard_central.png`、`ac03_dashboard_southeast.png`、`ac10_dashboard_error_missing_db.png`（新增） | AC-02／AC-03／AC-10 截圖。 |

HOW 說明：MVM 折線圖以 vanilla-JS inline SVG 繪製（無外部相依、免金鑰、離線可用），符合 R-EN-6「免金鑰免付費」精神並避開 CDN／CSP 風險；Leaflet Taiwan Map 與 `Select Date` 為 ENHANCED，不在本票。

## 3. 驗證（實際方法、結果、證據）

環境：`home_work_01/.venv`（Python 3.12.14），`flask==3.1.2`（werkzeug 3.1.8）。

- **全套離線 pytest**：初次 subject `72ff874` → **134 passed**（BASE `592c9ed` 為 107；本票新增 `test_dashboard.py` 22、`test_static_checks.py` 由 9 增至 14；107 + 22 + 5 = 134）。cycle 1 correction 後 → **143 passed**（見第 5 節）。測試不需網路與 `.env`（R-TC-4、R-TC-5）。〔F-9 更正：原記「#19 為 104」「由 12 增至 14」有誤，正確為 BASE 107、9→14。〕
- **Flask test client（R-TC-4）**：`GET /` 200 含標題；`/api/health` 200（ok：status ok、region_count 6、forecast_day_count 7、ingestion_time＝DB 值）與 503（missing／empty／incomplete／錯位快照，reason 對應）；四個資料 endpoint 各有正常、404（未知 Region／date）、503（快照不可用）。
- **INV-2 自動化比對**：`test_inv2_series_equals_shared_module_for_all_regions` 對六個 Region 斷言 series endpoint 的七筆 `(Date, MinT, MaxT)` 與 `weather_query.region_series`（即 Grading App 所用）完全相同。PASS。
- **AC-04 靜態檢查（完整＋F-4 強化）**：(a) app.py／shared／server.py／api/index.py 不 import HTTP client；F-4 的四種 import 形式以 helper 直接驗證全部被抓、benign `urllib.parse` 不誤報（獨立腳本＋`test_import_check_catches_from_urllib_import_request`）；無 CWA URL／key。(b) 前端無 CWA URL／key，唯一絕對 URL 為 SVG namespace（allowlist），fetch/fetchJson 目標字面全部 `/api/` 前綴。(c) SQL 只在 shared module。(d) server.py import weather_query、不 import sqlite3。全 PASS。
- **H-1／H-2 核對（A-1）**：新檔 grep 無 `opendata.cwa.gov.tw`／`CWA_API_KEY`／`os.environ`／`getenv`／`.env`／`load_dotenv`／`Authorization`；後端無 HTTP client import；`ingestion.checks.scan_file` 對七個新／改追蹤檔 0 命中；`git ls-files` 無 `.env`（僅 `.env.example`）。`python server.py` 啟動時 Flask 提示「.env files present. Install python-dotenv」但未安裝亦未 import，確認執行期不讀 `.env`（R-SEC-3）。H-2：頁面文字與六個 Region 名源自 shared module 常數（截圖逐字相符）；`data.db`／DDL 未改動。
- **截圖擷取（headless Chrome）**：以 `create_app` 啟本機 server（ok：port 5050；missing DB：port 5051），Chrome `--headless=new --virtual-time-budget=9000 --window-size=1280,1000 --screenshot=<abs path> <url>` 擷取。指令與 URL 記於本節；證據於 `doc/acceptance/screenshots/`。四張皆經目視確認：AC-02 標題＋`Select Region`（北部地區）；AC-03 中部地區／東南部地區各七列表格與雙線圖；AC-10 missing DB 顯示紅色錯誤 banner、無殘留控制項、無空白頁。
- **本機 `python server.py`**：`GET /` 200 含標題、`/api/health` 200 ok（documented run 指令實跑）。

## 4. 未解 concerns 與剩餘工作

- **Out of scope（本票不做）**：實際 Vercel 部署（#21；不建立專案、不設 repository variable — Reserved／RB-3 已遵守）、`Select Date`、Taiwan Map、UI/UX 品質清單（ENHANCED）、CI。
- **前瞻（#19 O-3，非本票 blocking）**：`requirements.txt` 含 streamlit＋flask，Vercel function 體積由 #21 部署時確認；若需拆分相依而牽動 R-DS-8「requirements.txt 在單元目錄」，應 route Design Authority。本票只建結構、本機驗證，未觸及。
- **DR-1 凍結項全部遵守**：頁面文字、`GET /api/health` 語義、`/api/` 前綴、共用模組唯一資料來源、Region 順序（DR-8）、ingestion 時間標籤（DR-17 §4.5）。
- 無 BLOCKED 事項；無需其他 authority。

## 5. Cycle 1 targeted correction（R1 audit `issue-20-c1-r1.md`）

R1 verdict：BLOCKING (F-1)。依治理 §4.4 做 targeted correction，不弱化測試、不擴張 scope。同一 work item／worklog identity／branch。

### F-1（Medium，blocking，R-DS-6）— 已修正

- **root cause**：`static/app.js` 的 `loadRegion` 在 series 非 2xx 分支呼叫 `showChartStatus` 後直接 return，未 un-hide `#region-panel`；而 `#chart-status` 位於該（初始 `hidden`）面板內，故首次載入時 series 回 503／404，訊息寫進隱藏面板、畫面看不到（且 Region 切換失敗時小標題殘留前一區）。
- **修正**：把「un-hide 面板＋設定小標題」移到 `fetchJson` 之前，使成功、404、503、網路失敗四種結果都在可見面板內呈現；小標題永遠是當前 Region。`showChartStatus` 仍清空圖與表並顯示訊息。
- **可重現驗證**（HOW；不進 offline pytest，需真實 Chrome）：新增 `tests/check_series_error_visible.py`——包裝未改動的 `server.create_app`，以 `before_request` 對 `/series` 注入 503／404（`/api/health`、`/api/regions` 仍正常，故頁面照常 bootstrap 後才撞上失敗），以 headless Chrome `--dump-dom`＋`--screenshot` 斷言 `#region-panel` 未 hidden 且 `#chart-status` 有可見文字。
  - 指令：`CHROME=<chrome> python tests/check_series_error_visible.py --shot <png>`。
  - 結果：503 → 顯示注入訊息；404 → 顯示「That Region is not available in this snapshot.」；**PASS，exit 0**。
  - **guard 有效性**：把修正還原（移除 fetch 前的 un-hide）後同一檢查 **exit 1（FAIL）**，證明它確實抓得到 F-1 回歸。
  - 證據截圖：`doc/acceptance/screenshots/ac10_dashboard_error_series_503.png`（面板可見、小標題 `Temperature Forecast – 北部地區`、info banner 顯示訊息）。

### SHOULD 清掉的 #20-owned Low findings（不擴張 scope）

- **F-2**：`tests/test_static_checks.py` 的 F-4 regression guard 改為經**真正的** `_import_targets` 解析原始碼（`test_import_check_catches_http_client_from_source` 參數化六種 import 寫法＋`test_import_check_allows_benign_imports_from_source` 三種 benign）。驗證：把 `_import_targets` 的 `ImportFrom` `module.name` 記錄還原後，該 guard 對 `from urllib import request`／`... as _r`／`from http import client` **FAIL（3 failed）**；修正版 22 passed。
- **F-5**：`tests/test_dashboard.py` 新增 `test_index_page_has_visible_teacher_text`，斷言 `GET /` HTML 含可見 `<h1>Taiwan Weather Forecast</h1>`、`Select Region` label、表頭 `Date`／`MinT`／`MaxT`（不只 `<title>`）。
- **F-7**：`README.md` 更新過時文字——Requirements 加列 `flask`、Dashboard「in a later ticket」改為「其公開 Vercel 部署為後續票」、測試段補述 Flask test client／INV-2／強化靜態檢查與瀏覽器層檢查。
- **F-8**：移除 `tests/test_static_checks.py` 未使用的 `_BACKEND` 常數。
- **F-9**：更正本 worklog §3 的測試數（BASE 107、`test_static_checks.py` 9→14）。

### 追蹤給 owner（不在本次修正）

- **F-3**（Low，owner #25）：`data.db` 為非 SQLite 檔時 `/api/` 回 HTML 500；與 #19 F-7 同 root cause（共用模組），本票不重開。
- **F-6**（Low，owner #21／#25 選項）：Flask 僅在安裝 `python-dotenv` 時才自動載入 `.env`，pinned `.venv` 未含此套件，執行期不讀 `.env`（R-SEC-3 仍成立）。
- **O-1**（`?region=` deep link）：observation，無 action（Reviewer 視為 R-DS-4 的 HOW）。

### correction 後全套驗證

- **全套離線 pytest**：**143 passed**（新增 test_dashboard 22→23、test_static_checks 14→22）。逐檔：test_app 9、test_dashboard 23、test_derive 19、test_fetch 13、test_persist 5、test_pipeline 19、test_secrets 4、test_static_checks 22、test_weather_query 29。無網路、無 `.env`。
- **F-1 瀏覽器檢查**：503／404 皆 PASS（見上）。
- **H-1 複核**：新增／修改檔（`static/app.js`、`tests/check_series_error_visible.py`、測試、README、worklog）無 CWA URL／key／`Authorization`；`check_series_error_visible.py` 只包裝 `create_app`、不含 secret；`git ls-files` 仍無 `.env`。
- 無 BLOCKED；無需其他 authority。
