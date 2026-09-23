# Worklog — Issue #19（共用查詢／領域模組 ＋ Grading App `app.py`）

| 欄位 | 內容 |
| --- | --- |
| Work item | GitHub Issue #19（`yotsubamomo/aiot-classwork`）「共用查詢／領域模組與 Grading App（app.py）：Select Region、一週折線圖與表格」，Scope class **MVM**（含 R-SHR-4／AC-28 的 ENHANCED 計算，作為兩層共用邏輯在本票落地） |
| 所屬 Spec | `home_work_01/doc/spec/SPEC.md` v1.1（EFFECTIVE）——R-SHR-1…5（本票為 Python 讀取側；JS 於 #20）、R-GA-1…9、R-DB-5（讀取側）、R-TC-1（共用模組部分）、R-TC-3、R-TC-5、R-DOC-1（Grading App 段）、R-DOC-2（Streamlit 定位）、R-DOC-5；§4.1、§5 |
| Outcome Contract | `home_work_01/doc/governance/outcome-contract.md`（ACCEPTED 2026-09-23） |
| 裁決依據 | DR-1、DR-2、DR-4、DR-8、DR-9、DR-11、DR-15（`decision-20260923-spec-interpretation-rulings.md`）；DR-17（`decision-20260924-ingestion-timestamp-semantics.md`）；高風險 H-1／H-2／H-3、A-1、A-5（`decision-20260923-high-risk-categories.md`） |
| 角色 | `gov-executor`（Bindings §3.1 mapping `claude-opus-4-8`／`high`）；binding 核對由派工者依 Bindings §3.4 記入 run record |
| Lane | Formal（作業主體） |
| Subject | branch `home_work_01-hw10-implementation`；BASE = `bbc82cd`（#18 結案 commit）；本票的 head commit SHA 記於 Executor return 與 run record |
| 日期 | 2026-09-24 |
| 狀態 | **DONE**（self-verification 完成；等待 independent audit） |

## 1. 授權核對（Implementation Profile §8 / property D、E）

- Outcome Contract 已接受並授權 implementation（`outcome-contract.md` 接受紀錄，2026-09-23）。
- Ticket #19 引用其 Spec v1.1，Spec 引用 Outcome Contract；derivation record `derivation-SPEC.md` 第 11 節含 #19 的 boundary determination。引用鏈與版本對應存在。
- 本票無 reserved boundary 動作（Ticket「Reserved：無 RB 動作」）；只在 `home_work_01/` 內修改（RB-5 未觸及）。無金鑰需求（Grading App 無 secret）。

## 2. 交付內容（做了什麼）

1. **共用查詢／領域模組** `home_work_01/weather_query.py`（唯一承載讀取側 SQL 與預報業務邏輯，R-SHR-1）：
   - 以唯讀 URI（`file:<path>?mode=ro`）開啟 `data.db`；預設路徑 `DEFAULT_DB_PATH = <module dir>/data.db`，相對於原始碼位置解析、不依賴 CWD；每個入口函式接受可覆寫的 `db_path`（R-SHR-3）。
   - R-SHR-2 六項語義（名稱屬 HOW）：`snapshot_status`（ok／missing／empty／incomplete，DR-9）、`region_list`（固定順序，DR-8）、`region_series`（dataDate 升序）、`day_values`（六區值＋Derived Map Temperature＋色帶）、`forecast_days`（升序）、`last_ingestion_time`（原樣回傳 `IngestionMetadata.ingestedAt`，DR-17）。
   - R-SHR-4／DR-4：`derived_map_temperature`＝(MinT＋MaxT)/2 以 `Decimal` `ROUND_HALF_UP` 到一位小數；`colour_band` 以**顯示值**分帶（`<20` blue、`20–<25` green、`25–<30` yellow、`≥30` red）。
   - 不 import 任何 HTTP client；不含 CWA endpoint URL 或金鑰引用（R-SHR-5，H-1 靜態）。讀取側自足，不 import ingestion 套件。
2. **Grading App** `home_work_01/app.py`（Streamlit，`streamlit run app.py`，R-GA-1）：
   - 標題 `Taiwan Weather Forecast`（R-GA-2）；`Select Region` 下拉，選項恰六個 Region、固定順序、預設第一個（R-GA-3、DR-8／DR-15）。
   - 選定 Region → `MaxT`／`MinT` 七日折線圖（MaxT 紅 `#d62728`、MinT 藍 `#1f77b4`，圖表標題 `Temperature Forecast – <Region>`，DR-15 SHOULD）＋ `Date`／`MinT`／`MaxT` 七列升序表格，值等於 `data.db`（R-GA-4／5）。
   - 資料只經共用模組（無 SQL、無 HTTP client、無 CWA URL／金鑰；R-GA-6、R-SHR-5）。
   - 顯示快照最後 ingestion（取得）時間，標籤「Last updated (data fetched from CWA)」（R-GA-8、DR-17）。
   - 錯誤狀態（R-GA-7、DR-9）：missing／empty → `st.error` 明確訊息且無未處理例外；incomplete → `st.warning`（仍嘗試顯示既有資料）。
   - 不含 Taiwan Map、`Select Date`，不依賴 folium／streamlit-folium（R-GA-9、DR-11）。
   - `main()` 以 `if __name__ == "__main__"` 觸發：`streamlit run` 與 `AppTest.from_file` 會執行，`import app` 不會，供替代路徑測試。
3. **測試**（`home_work_01/tests/`，pytest ＋ Streamlit `AppTest`，全離線）：
   - `test_weather_query.py`（27 例）：R-SHR-2(a–f) 六語義、R-SHR-3（唯讀、source-relative、覆寫）、AC-28 五組色帶邊界。
   - `test_app.py`（8 例）：AC-02（標題、六選項、順序、預設）、AC-03（中部地區與東南部地區：圖表 spec 含 MaxT/MinT 兩線＋紅藍色＋Date 軸；表格七列升序、值等於 `data.db`）、AC-10（missing／empty／incomplete → 訊息／警告、無例外）、AC-24（顯示的 ingestion 時間 == 中繼資料值）。
   - `test_static_checks.py`（9 例）：AC-04(a)(c)(d) Python 側（無 HTTP client、無 CWA URL／金鑰於程式碼、SQL 只在共用模組、`app.py` import 共用模組且不直接用 sqlite3）、AC-26（無 map/`Select Date`/folium；`requirements.txt` 不列 folium）。靜態檢查以 AST 排除 docstring／comment，SQL 以「語句結構」比對，避免把 `Select Region` 標籤或說明文字誤判。
4. **`requirements.txt`**：新增 `streamlit==1.64.0`（固定版本）；重寫註解移除 `folium` 字樣（見 §5 F-10 closure）。
5. **README**：更新 scope 註、相依清單、新增「Run the Grading App」段（含 R-DOC-2 的 Streamlit 定位敘述，依 OC §2.4：必要評分產物、非部署 runtime 的 Vercel 相容性安排）、更新測試段與海報對應表 `app.py` 列。
6. **Docstring／錯誤處理／無死碼**（AC-27、R-DOC-5）：模組與主要函式皆有說明目的的 docstring；missing/empty 以 `SnapshotError` 與 UI 訊息處理；無未使用相依。

## 3. Self-verification（方法、結果、證據；治理 §3.5）

驗證環境：`home_work_01/.venv`（uv，Python **3.12.14**）；`streamlit 1.64.0`、`pandas 3.0.6`、`pytest 8.3.3`、`requests 2.32.3`。

| # | 驗證 | 方法 | 結果 |
| --- | --- | --- | --- |
| V-1 | 全套件 | `.venv/Scripts/python.exe -m pytest -q`（單元目錄） | **104 passed in ~2.7s**（#18 的 66 例 ＋ 本票新增 44 例：test_weather_query 27、test_app 8、test_static_checks 9）。無回歸。 |
| V-2 | 離線（R-TC-5） | 以 `sitecustomize` 攔截非 loopback `connect`／`getaddrinfo`（保留 asyncio self-pipe），無 `.env` 依賴，重跑全套件 | **104 passed**。外部網路封鎖下通過；測試不讀 `.env`。 |
| V-3 | AC-01 boot | `streamlit run app.py --server.headless true --server.port 8765`（單元目錄） | 伺服器啟動；`GET /` → **200**；`GET /_stcore/health` → **200 "ok"**；boot log 無 traceback／exception。 |
| V-4 | AC-01 render | `AppTest.from_file("app.py").run()`（V-1 內 test_app） | 首頁渲染標題、`Select Region`、選 Region 後圖表＋表格、caption 皆存在，`at.exception` 為空——「首頁渲染無例外」成立。 |
| V-5 | AC-03 值對照 | test_app 直接查 `data.db` 建立期望，比對 `AppTest` 表格 | 中部地區、東南部地區各七列升序、`MinT`/`MaxT` 值與 `data.db` 相同。 |
| V-6 | AC-28 邊界 | test_weather_query 參數化五組 | (20.1,25.2)→22.7/green、(19.9,20.0)→20.0/green、(24.9,25.0)→25.0/yellow、(29.9,30.0)→30.0/red、(15,24.8)→19.9/blue，全通過（half-up、以顯示值分帶）。 |
| V-7 | R-SHR-3 唯讀 | test_weather_query 以 `_read_only_connection` 試寫 | `DELETE` 觸發 `sqlite3.OperationalError`（唯讀）；`DEFAULT_DB_PATH == <module>/data.db`；chdir 後預設路徑仍解析到提交的 `data.db`。 |

證據路徑：本 worklog §2–§5；`home_work_01/tests/`；scratchpad 的 boot log（`.../scratchpad/st_boot.log`，非 repo 追蹤）。截圖：本環境無法擷取瀏覽器畫面；依 Ticket AC-01 註記，以 `AppTest`（渲染無例外）＋ headless boot（200／health ok、log 無例外）作為 AC-01 證據，實機截圖留待後續人工驗證補充。

## 4. 高風險核對（A-1；治理 §4.6）

- **H-2 老師指定介面／文字**：頁面文字 `Taiwan Weather Forecast`、`Select Region`、`Date`、`MinT`、`MaxT` 與六個 Region 名逐字（test_app 斷言）；`streamlit run app.py` 於單元目錄可啟動（V-3）；未新增或改動 `TemperatureForecasts` DDL／五欄／`data.db`（本票只讀）。**無 finding。**
- **H-3 資料語義與標示**：Derived Map Temperature 與色帶定義在共用模組（唯一處），half-up、以顯示值分帶（AC-28 五例）；`region_list` 固定順序來自共用模組常數（非 SQL／字母序，DR-8）；README 的 Streamlit 定位與 DR-17 取得時間標籤未把專案值寫成 CWA 發布值。**無 finding。**
- **H-1 憑證與機密（本票以靜態檢查涵蓋）**：`app.py`、`weather_query.py` 不 import HTTP client、程式碼無 CWA endpoint URL 或金鑰引用（test_static_checks，AST 排除 docstring）；另人工 grep 確認新檔無金鑰字面或 `CWA-<hex>` 格式；`git ls-files` 僅 `.env.example`，無 `.env`。**無 finding。**

## 5. 前票 follow-up：F-10 closure（owner #19）

- `issue-18-c1-r1.md` F-10：`requirements.txt` 的註解含字串「folium」，若 #19 靜態檢查以子字串判斷會誤判。
- 處置：(1) 重寫 `requirements.txt` 註解，移除 `folium` 字樣（整檔不再含該子字串）；(2) `test_requirements_does_not_list_folium` 同時做「非註解行不列 folium」與「整檔無 folium 子字串」兩層斷言，即使他人以子字串檢查亦通過。**F-10 已 closed。**

## 6. 契約固定的沿用

- 老師名字不變（app.py、data.db、DDL、五欄、Region 名、頁面文字，H-2／INV-4）。
- 共用模組是讀取側唯一 SQL／業務邏輯處（INV-1）；`app.py` 只呼叫它。
- ENHANCED 只在 Dashboard；Grading App 只有 MVM（INV-9、DR-11）——本模組另含 R-SHR-4 的 Derived Map Temperature 計算，因 Spec 將其歸屬共用模組供 #20/#24 使用，Grading App 本身未呈現地圖或色帶。

## 7. Unresolved concerns 與剩餘工作

- **無 blocking concern。**
- 本票範圍外（後續票）：Flask JSON API 與靜態前端（#20）、Taiwan Map／Select Date／ENHANCED UI（#24）、CI／smoke（#22／#23）、Vercel 部署（#21）、`doc/acceptance/` 逐條對照與 README 全流程實跑（#25）。
- AC-01 實機截圖為後續人工補充項（本環境不可擷取），不影響本票 self-verification 結論。
- INV-2（兩層行為對等）之「對照」在 #20 完成後由 Spec Integration Audit 核；本票輸出即該對照基準。

## 8. Binding

- 依 Bindings §3.4，本 Executor assignment 的 `agentType`／model／effort 由派工者從 harness 紀錄核對並記入 run record；本 worklog 的 subject（branch＋commit SHA）與該核對併同構成 binding 證據。
