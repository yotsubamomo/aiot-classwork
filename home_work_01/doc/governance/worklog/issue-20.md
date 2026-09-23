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
| 狀態 | DONE（self-verification 完成；待 independent audit） |

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

- **全套離線 pytest**：`python -m pytest -q -p no:cacheprovider` → **134 passed**（#19 為 104；本票 `test_dashboard.py` 22、`test_static_checks.py` 由 12 增至 14）。逐檔：test_dashboard 22、test_static_checks 14、其餘不變。測試不需網路與 `.env`（R-TC-4、R-TC-5）。
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
