# Worklog — Issue #24 Select Date 與 Leaflet Taiwan Map（依 Derived Map Temperature 著色）

- **Work item**：GitHub Issue #24（Formal lane，ENHANCED scope，Dashboard only；最後一張 implementation ticket）
- **Executing role**：`gov-executor`（Bindings §3.1 mapping：`claude-opus-4-8`，effort `high`）。Binding verification 依 Bindings §3.4 由派工者（Orchestrator／主 session）從 harness 紀錄核對 `agentType`／`message.model`／`effort`；本 worklog 記錄執行角色與依據，不複製 harness 日誌。
- **Branch**：`home_work_01-hw10-implementation`，BASE = HEAD `8d46ead`
- **開始**：2026-09-24

## Contract reference

- **Ticket**：Issue #24（ENHANCED REQUIRED，只在 Dashboard；Grading App 不動）。
- **Spec**：`home_work_01/doc/spec/SPEC.md` v1.1 — R-EN-3（`Select Date`：七個 Forecast Day 升序、預設第一天）、R-EN-4（Leaflet Taiwan Map：以台灣為中心、初始視野涵蓋六個標記、可縮放；六個代表點標記；顏色依所選日期的 Derived Map Temperature 色帶；點擊／hover 資訊卡 Region／`Date`／`Min`／`Max`／導出平均一位小數）、R-EN-5（四段圖例＋「導出、非觀測日均溫」註）、R-EN-6（Leaflet／底圖免金鑰／帳號／付費）、R-EN-7（整合單頁）；R-SHR-4（Derived Map Temperature 等價）；R-DOC-2（導出值標示）；R-DS-3（日值 endpoint）。§1.7、§4.2。
- **AC**：AC-17、AC-18、AC-28（前端側）、AC-14（第 6 項）、AC-19（重驗）；回歸 AC-27（本票範圍）。
- **Invariants**：INV-2、INV-7、INV-9。AB：AB-14、AB-15、AB-13（部分）。
- **裁決**：DR-4（half-up、以顯示值分帶）、DR-1（代表點座標與 CDN／vendored 屬委派 HOW）、**DR-19**（`/api/days*` 的 fetch 狀態沿用 per-Region 規則；並修 **N-1**：`fetchJson` 對 2xx 無法解析的回應目前呈現 empty，依 DR-19 §4.1 應為 error）。
- **High-risk**：H-3（Derived Map Temperature 等價性＋「導出」標示）、H-2（`Select Date`、`Min`／`Max` 文字）。本 worklog 依 A-1 記錄 H-3／H-2 核對。

## Decisions and assumptions（HOW，DR-1／DR-4 授權）

1. **Vendored Leaflet，無外部請求（R-EN-6；避免 AC-04(b) 外部 URL 陷阱）。** 將 Leaflet 1.9.4（`leaflet.js`、`leaflet.css`）vendored 於 `home_work_01/static/vendor/`（釘住版本、免金鑰）。`tests/test_static_checks.py::test_frontend_makes_no_external_absolute_url_requests` 只掃 `static/` 頂層檔案（`_STATIC_DIR.iterdir()` 非遞迴），不掃子目錄，故 Leaflet 自帶的 attribution 連結（`https://leafletjs.com`，一個超連結、非資料請求）不觸發檢查；我沒有修改或弱化該檢查。底圖用 **vendored 簡化台灣輪廓 GeoJSON**（inline 於 `app.js`，非第三方，完全在 URL／key 檢查涵蓋內），以 `L.geoJSON` 繪製向量層，**不使用任何 tile server**，執行期零外部請求。標記用 `L.circleMarker`（SVG，不需圖示 PNG），故 `leaflet.css` 的 `url(images/*.png)` 規則不套用到任何元素、不產生請求。未引入需要金鑰／帳號／付費的地圖服務（RB-3、RB-4）。
2. **直接以 endpoint 回傳值著色（R-SHR-4、H-3 單一來源）。** 前端**不重算** Derived Map Temperature 或色帶；直接用 `/api/days/<date>` 回傳的 `colourBand` 對應到顏色、`derivedMapTemperature` 顯示（一位小數）。因此 AC-28 前端側走「以 endpoint 值直接著色，記錄之」路徑，不需 JS 對照測試（H-3 的推導與分帶只在共用模組定義）。
3. **代表點座標（DR-1，HOW；README 標示專案定義）。** 六區代表點 [lat, lng]：北部 [25.03,121.50]、中部 [24.15,120.68]、南部 [22.85,120.35]、東北部 [24.72,121.74]、東部 [23.98,121.55]、東南部 [22.80,121.10]。地圖 `fitBounds` 至六標記，確保以台灣為中心且六標記皆可見（R-EN-4）。
4. **`Select Date`（R-EN-3）** 取 `/api/days`（升序七天），預設第一天；切換觸發 `/api/days/<date>` 重著色與更新資訊卡（AC-18）。
5. **DR-19 狀態對應 + N-1 修正。** `fetchJson` 改為讀取回應文字後 `JSON.parse`，區分「解析成功」與「無法解析」；2xx 但無法解析（或空 body）→ `parseError`，呼叫端一律視為 **error**（DR-19 §4.1，修 N-1；原本 `.json().catch(()=>({}))` 會把 2xx 無法解析當成空內容 → empty）。`/api/days`、`/api/days/<date>` 沿用 per-Region（inline，於 map card 內）規則：非 2xx／網路失敗／無法解析 → inline error；2xx 空資料 → inline empty；in-flight → inline loading。
6. **概念詞保留（H-2 / R-EN-2）。** 新增 `Select Date` `<label>`；資訊卡用 `Min`／`Max`／`Date`。既有 `Taiwan Weather Forecast`／`Select Region`／表頭 `Date`/`MinT`/`MaxT` 未改。AC-26 只約束 Grading App 側（`app.py`＋共用模組），前端 dashboard 加 `Select Date`／地圖不觸發 AC-26。

## Artifacts

- `home_work_01/static/vendor/leaflet.js`、`static/vendor/leaflet.css`（vendored Leaflet 1.9.4，未改）
- `home_work_01/static/index.html`、`static/styles.css`、`static/app.js`（改版：Select Date、Taiwan Map、legend、infocard、N-1 fetchJson 修正）
- README 新增 #24 段落（Taiwan Map、`Select Date`、代表點為專案定義、Derived Map Temperature 為導出值）
- 截圖：`home_work_01/doc/acceptance/screenshots/`（#24 名稱）

## Verification（結果）

**環境**：本機 Python 3.12.14（uv-managed，`home_work_01/.venv`；CI 亦 3.12，AC-23 由 #22 CI 涵蓋）。本機預設 `python` 為 3.11.2，故以 3.12 venv 跑全套（與 CI 對齊）。截圖以 headless Chrome + CDP（`Emulation.setDeviceMetricsOverride`）擷取，量測值以 CDP `document.documentElement.scrollWidth`／DOM 幾何確認，並以 desktop-app 內建瀏覽器複核。網路以 CDP／內建瀏覽器 network log 檢視。截圖工具與同步憑證檢查用的 `websocket-client` 只安裝在被 ignore 的 `.venv`，未列入 `requirements.txt` 或 CI。

**Subject**：branch `home_work_01-hw10-implementation`；改動只在 `home_work_01/static/{index.html,styles.css,app.js}`（`git diff --stat`：3 檔，+551/−32）與新增 vendored `static/vendor/{leaflet.js,leaflet.css}`（Leaflet 1.9.4，未改；sha256 leaflet.js `db49d009…5641a`、leaflet.css `a7837102…d04c6`）。`app.py` 自 BASE `8d46ead` 起未被觸及（`git diff --name-only | grep -c app.py` = 0）。`server.py`、`weather_query.py`、`vercel.json` 未改（`/api/days`、`/api/days/<date>` 已於 #21 存在）。

### AC-17（Taiwan Map；PASS）

- **地圖以台灣為中心、六個標記可見、可縮放**：vendored Leaflet；`ensureMap` 以 `L.geoJSON`（vendored 簡化台灣輪廓向量層，無 tile server）＋六個 `L.circleMarker`，`fitBounds` 至六標記 → 以台灣為中心、六標記皆可見；zoom control（+／−）在，可縮放。截圖 `issue-24-map-desktop-ac17.png`（桌機 1280）、`issue-24-mobile-375-ac19.png`（手機 375）。
- **每個標記顏色 == 共用模組色帶（以 endpoint 值對照）**：前端直接以 `/api/days/<date>` 回傳的 `colourBand` → `BAND_COLOURS` 著色，不重算。所選日 2026-09-24 六區 endpoint band 與標記 fill 對照（marker fill 讀自 `path.leaflet-interactive@fill`）：

  | Region | endpoint derivedMapTemperature | endpoint colourBand | marker fill | BAND_COLOURS[band] | 一致 |
  | --- | --- | --- | --- | --- | --- |
  | 北部地區 | 27.2 | yellow | #f2b705 | #f2b705 | ✓ |
  | 中部地區 | 28.8 | yellow | #f2b705 | #f2b705 | ✓ |
  | 南部地區 | 29.2 | yellow | #f2b705 | #f2b705 | ✓ |
  | 東北部地區 | 26.5 | yellow | #f2b705 | #f2b705 | ✓ |
  | 東部地區 | 27.0 | yellow | #f2b705 | #f2b705 | ✓ |
  | 東南部地區 | 27.5 | yellow | #f2b705 | #f2b705 | ✓ |

  （提交的快照九月下旬六區導出溫度皆落在 25–<30，故實資料六標記皆黃，與 endpoint band 全部一致。四段著色映射另以 band-spanning 合成快照示證，見 AC-28。）
- **資訊卡（Region／Date／Min／Max／導出平均一位小數）**：每個 marker 綁 Leaflet tooltip（hover）與 popup（click，`autoPan:false`），內容含 Region、`Date`、`Min`、`Max`、導出平均（`toFixed(1)`）；另有側欄 info card 同步 hover／click 更新。截圖 `issue-24-map-infocard-ac17.png`：click 南部地區 popup 顯示「南部地區／Date: 2026-09-24／Min: 26.3°C · Max: 32°C／Derived map temperature: 29.2°C (derived)」，與 endpoint（mint 26.3、maxt 32.0、derived 29.2）一致。
- **圖例四段＋「導出」說明**：`.legend-bands` 四段（`<20` 藍／`20–<25` 綠／`25–<30` 黃／`≥30` 紅，swatch 由 JS `BAND_COLOURS` 上色，與標記同源）＋註記「Average = (MinT + MaxT) / 2, a derived value — not an observed daily mean.」（R-EN-5）。
- **底圖不需金鑰**：見 R-EN-6。

### AC-18（Select Date 兩個日期；PASS）

- `Select Date` 選項＝ `/api/days` 七天升序 `2026-09-24 … 2026-09-30`，預設第一天（R-EN-3）。
- 切換後標記顏色與資訊卡值與該日 endpoint 一致：
  - date1 `2026-09-24`（截圖 `issue-24-map-date1-ac18.png`）：info card 北部地區 Min 23.3／Max 31／導出 27.2。
  - date2 `2026-09-28`（截圖 `issue-24-map-date2-ac18.png`）：caption「Showing 2026-09-28」，info card 北部地區 Min 24.4／Max 32.4／導出 28.4。
  - 值隨日期更新（23.3/31/27.2 → 24.4/32.4/28.4），與各日 endpoint 相符；顏色兩日皆黃（與各日 endpoint band 一致）。

### AC-28（前端側；PASS — 以 endpoint 值直接著色，記錄之）

前端**不重算** Derived Map Temperature 或色帶，直接用 `/api/days/<date>` 回傳的 `derivedMapTemperature`（顯示，一位小數）與 `colourBand`（著色）。共用模組的推導與分帶（含五組邊界案例）由 `tests/test_weather_query.py`／`test_dashboard.py::test_day_values_normal`（斷言 `derivedMapTemperature == wq.derived_map_temperature` 且 `colourBand ∈ {blue,green,yellow,red}`）涵蓋（AC-28 pytest 側綠）。因此前端側無 JS 對照測試，改以「直接用 endpoint 值著色」記錄（Ticket 允許）。band→colour 映射另以合成 band-spanning 快照示證（截圖 `issue-24-map-bands-4colours.png`）：北部 blue(19.0)#2b6cb0、中部 green(22.0)#2f9e44、南部 red(32.0)#e03131、東北部 yellow(27.0)#f2b705、東部 green(20.0)#2f9e44、東南部 red(31.0)#e03131——四段顏色皆正確，含邊界 20.0→green（`≥20` 綠）、`≥30`→red，marker fill 與 endpoint band 全部一致。

### AC-19 重驗（六項 R-EN-1 + 375px + 手機地圖；PASS）

地圖加入後全頁重驗（截圖 `issue-24-desktop-ok-ac19.png` 桌機、`issue-24-mobile-375-ac19.png` 手機 375）：

| # | R-EN-1 項目 | 結果 | 證據 |
| --- | --- | --- | --- |
| 1 | 視覺層級 | PASS | masthead／controls（Select Region＋Select Date）／summary／chart／table／Taiwan Map 各自成區、主次分明 |
| 2 | 響應式（≥1024 與 375） | PASS | 桌機雙欄、手機單欄堆疊；地圖與側欄（info card＋legend）在 760px 以下改為單欄 |
| 3 | 摘要資訊 | PASS | Weekly summary（本週 Lowest MinT／Highest MaxT），另地圖側欄 info card 為所選日六區概況入口 |
| 4 | 圖表互動 | PASS | 折線圖圖例／軸標籤／hover tooltip（#23 既有，未回歸） |
| 5 | loading／empty／error | PASS | 頁面層級三態：`issue-24-state-loading.png`、`issue-24-state-empty.png`（regions 2xx `[]`）、`issue-24-state-error.png`（missing DB，role="alert"）；地圖層級三態：inline loading／`issue-24-map-inline-empty.png`（days 2xx `[]`）／`issue-24-map-inline-error.png`（days 500，`state--inline-error`、role="alert"、map 隱藏不留白） |
| 6 | 375px 無不必要橫向捲動 | PASS | 375px 下 `document.documentElement.scrollWidth = 375 = innerWidth`（不大於）；desktop 1280 下 scrollWidth = 1280 |

- **地圖在手機可用**：375px 下地圖 markers = 6、`map-layout` 可見、六標記＋輪廓＋info card＋四段圖例可讀（`issue-24-mobile-375-ac19.png`）。CDP 於 375 全頁量測另見一個 Leaflet 內部絕對定位 pane 右緣超出 innerWidth，但其位於 `.map`（`overflow:hidden`）內、不造成頁面捲動（`scrollWidth=375`）；desktop-app 瀏覽器於可見狀態下量測超出元素為 0。

### R-EN-6（免金鑰／帳號／付費；PASS）

- Leaflet 1.9.4 **vendored** 於 `static/vendor/`（釘住版本，無金鑰）；底圖為 vendored 台灣輪廓向量層，**無 tile server**；標記為 `L.circleMarker`（SVG，不需 marker PNG）。
- 執行期 network log（內建瀏覽器）：全部請求皆同源 `127.0.0.1`——`/`、`/static/{vendor/leaflet.js,vendor/leaflet.css,styles.css,app.js}`、`/api/*`；**零外部請求**（無 tile／CDN／字型／`leaflet.js.map`）。不需任何金鑰、帳號或付費（RB-3、RB-4 未觸及）。

### N-1 修正（fetchJson 2xx 無法解析 → error；PASS）

`fetchJson` 改為 `response.text()` 後 `JSON.parse`，加 `parseError` 旗標；呼叫端以 `failed(res)=!res.ok||res.parseError` 判定。行為驗證（headless，注入 2xx 非 JSON body）：
- `/api/regions` 回 200 非 JSON → 頁面 **error**（`page-error` 顯示、`page-empty` 未顯示；訊息「The forecast data is currently unavailable.」）。修正前會顯示 empty。
- `/api/days` 回 200 非 JSON → 地圖 inline **error**（`state--inline-error`）。
符合 DR-19 §4.1「無法解析的回應是 error」。既有非 2xx（404／503／5xx）與網路失敗行為不變（error）。

### DR-19 地圖狀態（PASS）

`/api/days`、`/api/days/<date>` 沿用 per-Region（inline）規則：非 2xx／網路失敗／無法解析 → inline error（`issue-24-map-inline-error.png`）；2xx 空資料 → inline empty（`issue-24-map-inline-empty.png`）；in-flight → inline loading；狀態顯示時隱藏 `map-layout`，不留白。

### H-3／H-2 核對（A-1）

- **H-3（Derived Map Temperature 等價 + 導出標示）**：前端未重算導出值或色帶，直接用共用模組經 endpoint 回傳的 `derivedMapTemperature`／`colourBand`（單一來源，`server.py`／`weather_query.py` 未改）；資訊卡導出平均以 `(derived)` 標示、圖例註「導出、非觀測日均溫」；README 段落標示 Derived Map Temperature 為導出值（AC-14 第 6 項）。未改動推導函式、對應表、fixture 期望值或分帶。
- **H-2（Select Date、Min／Max 文字）**：新增 `Select Date` `<label>`；資訊卡用 `Min`／`Max`、`Date`；既有 `Taiwan Weather Forecast`／`Select Region`／表頭 `Date`/`MinT`/`MaxT` 逐字未改。`tests/test_dashboard.py::test_index_page_has_visible_teacher_text` PASS。未觸及 `app.py`、DDL、五欄名、Region 名、`streamlit run app.py`。

### INV-2／INV-9／AC-26／AC-04(b)（PASS）

- INV-2：`test_inv2_series_equals_shared_module_for_all_regions` PASS；資料仍只來自 `/api/`。
- INV-9／AC-26：`app.py` 不在 diff；`tests/test_app.py`（`AppTest`）全 PASS；`test_static_checks.py` AC-26（Grading App 無 map／Select Date／folium）PASS。ENHANCED 只加在 Dashboard 前端。
- AC-04(b)：`test_static_checks.py::{test_frontend_has_no_cwa_url_or_key, test_frontend_makes_no_external_absolute_url_requests, test_frontend_requests_use_the_api_prefix}` PASS。vendored Leaflet 置於 `static/vendor/`（子目錄）；`_static_files()` 以 `iterdir()` 非遞迴只掃頂層檔，不掃子目錄，故 Leaflet 內含的 attribution 連結（`https://leafletjs.com`，超連結、非資料請求）不觸發檢查；**未修改或弱化該檢查**。我方 authored 前端（app.js／index.html／styles.css）完全在 URL／key 檢查涵蓋內，唯一 absolute URL 仍為 SVG namespace，所有 `fetch/fetchJson` 字面目標以 `/api/` 開頭（新增 `/api/days`、`/api/days/<date>`）。

### 全套離線測試（PASS）

`./.venv/Scripts/python -m pytest`（3.12，無網路、無 `.env`）：**152 passed**（BASE 亦 152；本票未新增／刪除 pytest 測試——前端為 JS，band→colour 與導出等價由既有共用模組測試涵蓋，AC-28 前端側走 endpoint-值著色記錄路徑）。

### Subject 與 CI（PASS）

- BASE = `8d46ead`；commit（受審 subject）＝ **`4ec20b5`**，已 push `origin/home_work_01-hw10-implementation`（SA-1）。改動：`static/{index.html,styles.css,app.js}` 修改、`static/vendor/{leaflet.js,leaflet.css}` 新增、`README.md`、`doc/acceptance/screenshots/issue-24-*.png`、`doc/governance/worklog/issue-24.md`。
- 本機憑證機械檢查（`tools/credential_scan.py`）：passed（504 tracked files；無 `.env`；追蹤檔與歷史 diff 無 CWA 金鑰格式；fixture／raw JSON 無 Authorization 值）——含新 vendored Leaflet。
- CI（`.github/workflows/home_work_01-ci.yml`，Python 3.12，offline pytest 全套＋憑證機械檢查）於 `4ec20b5`：
  - push run `35940942570` → completed/**success**
  - pull_request run `35940944706` → completed/**success**
  - 全步驟綠（Show Python version 3.12；full offline pytest 152 passed；credential checks）。註記僅為 GitHub 對 Node20／ubuntu label 的 deprecation 提醒，非失敗。

## Targeted correction — cycle 1（R1 BLOCKING F-1、F-2；併修 F-3）

**輸入**：R1 audit `doc/governance/audit/issue-24-c1-r1.md`（VERDICT: BLOCKING (F-1, F-2)）。同一 work item、同一 worklog、同一 branch。治理 §4.4 targeted correction：只修 findings，不弱化測試、不擴大 scope（`app.py` 未動、資料只來自 `/api/`、DR-19／N-1 維持、AC-04(b) 靜態檢查與 vendored Leaflet 未動）。

**新 subject**：`home_work_01-hw10-implementation`，correction commit（見 §CI-2）；改動只在 `static/{app.js,index.html,styles.css}` 與 `tests/test_dashboard.py`（新增 Select Date 斷言，加強覆蓋、未弱化）。

### F-1（Medium, blocking；AC-18／R-EN-4）— 切換日期後開著的 popup 顯示舊值 → 已修

- **成因**：`applyDay` 每次切換都 `marker.bindPopup(html)` 綁新 popup，但不更新目前開著的 popup。
- **修法（HOW）**：`applyDay` 改為 `getPopup()`／`getTooltip()` 判斷——首次 `bindTooltip`／`bindPopup`（`autoPan:false`），其後 `setTooltipContent`／`setPopupContent` **就地更新**；`setPopupContent` 會即時刷新已開著的 popup，故切換日期時開著的 click 資訊卡改顯示新日期的 `Date`／`Min`／`Max`／導出值（不再殘留前一天）。
- **closure 證據（headless CDP，真實資料）**：點北部地區 marker 開 popup，再把 `Select Date` 由 2026-09-24 切到 2026-09-28：
  - 1280：popup `before`＝「北部地區 Date: 2026-09-24 Min: 23.3°C · Max: 31°C Derived map temperature: 27.2°C (derived)」→ `after`＝「…Date: 2026-09-28 Min: 24.4°C · Max: 32.4°C … 28.4°C (derived)」，popup 仍開著、值＝該日 endpoint。
  - 375：同上（before 27.2 → after 28.4）。
  - marker 顏色、側欄 info card、popup 三者一致。截圖 `issue-24-f1-popup-updates-1280.png`、`issue-24-f1-popup-updates-375.png`。七天切換既有行為無回歸（全套 152 passed）。

### F-2（Medium, blocking；AC-27）— placeholder 死 CSS 與過時註解 → 已修

- 移除 `styles.css` 的 `.control--reserved` 與整段 `.placeholder`／`.placeholder--inline`／`.placeholder--map`／`.placeholder__tag`／`.placeholder__note`（本票移除 placeholder 標記後已無元素使用）。
- 更正 `index.html` controls 區塊註解（原「Select Date … NOT implemented here」→ 改為描述已整合的 Select Region／Select Date）。
- 併修次要項：`app.js` 檔頭 DR-19 狀態說明補上地圖 inline 狀態（`/api/days[/<date>]` 的 loading／error／empty 在 map card 內）。
- **closure 證據**：`grep -rn "placeholder\|control--reserved" static/`（排除 vendor）**0 筆**；`grep "NOT implemented|reserved|Coming soon"` static 前端 **0 筆**。只移除未使用規則，版面與 `scrollWidth`（375）不變（無渲染回歸）。

### F-3（Medium, non-blocking；AC-18）— `/api/days/<date>` 回應亂序 → 已於同組函式併修

- **修法（HOW）**：`loadDay` 以 `mapReqSeq` 序號標記每次請求（`var seq = ++mapReqSeq;`），回應（`.then`／`.catch`）先檢查 `seq === mapReqSeq`，否則丟棄——較舊／較晚到達的回應不會覆寫目前選取的日期。不擴大 scope（同組函式、同一 AC-18 性質；`loadRegion` 的相同模式屬 #20／#23 已結案程式，未觸及）。
- **closure 證據（headless CDP，伺服器端延遲 `/api/days/2026-09-25` 2.5s）**：載入（24）→ 選 2026-09-25（慢）→ 立即選 2026-09-26（快，先完成、套用 26）→ 等延遲的 25 回應到達：最終 `caption="Showing 2026-09-26"`、`infocard-date=2026-09-26`、`date-select=2026-09-26`、`map-status` 隱藏——延遲的 25 回應被丟棄，未覆寫當前選取。

### 併修的 optional（F-6，Low）

`tests/test_dashboard.py::test_index_page_has_visible_teacher_text` 新增 `>Select Date</label>` 斷言（H-2 評分頁面文字的自動化回歸保護；加強覆蓋，未弱化任何測試）。F-4（AC-04(b) 不掃 vendor）依派工指示不動靜態檢查與 vendored Leaflet；F-5（375 popup 裁切等 UX 細節）不違反契約條款，未改。

### 回歸與陳舊證據

- 全套離線測試（3.12，無網路／無 `.env`）：**152 passed**（含新增的 Select Date 斷言）。
- F-1／F-3 為行為修正、F-2 移除未使用 CSS 與更正註解——UI 靜態外觀不變，故既有 12 張 AC 截圖（AC-17／18/19、狀態、band）維持有效；另新增兩張 F-1 closure 截圖。
- AC-17／R-EN-3/5/6/7、AC-28 前端側、AC-14 第 6 項、DR-19／N-1、INV-2／INV-7／INV-9、AC-04(b)、H-2／H-3 維持 PASS（本次未觸及其判定依據；`app.py`／`server.py`／`weather_query.py`／`vercel.json`／vendored Leaflet 仍不在 diff）。

## Audit status

Formal Ticket → independent audit required（Bindings §5；治理 §4.1）。cycle 1 R1 = BLOCKING (F-1, F-2)；本次 targeted correction 已附 F-1、F-2 的 closure 證據與 F-3（non-blocking）的併修證據，交 **R2**（Primary Reviewer 延續其 R1 context、重讀修正後檔案與 diff）核對，範圍依 R1 §4 F-1／F-2 的 closure 條件；R2 須依 A-1 重述 H-3 的核對。R2 由 Orchestrator／主 session 依 Bindings §3.5 派工，不由 Executor 自派。本 Ticket 觸及 H-2／H-3，audit record 依 A-1 明記核對。原始 R1（含 self-verification 主張）記於本 worklog 上方各節。

## Remaining work

無 blocking 剩餘工作。實作與 self-verification 完成；待 commit／push 與 CI 綠（見下）。
- 待 Primary Reviewer R1（Formal，由 Orchestrator／主 session 依 Bindings §3.5 派工，不由 Executor 自派）。本票觸及 H-3／H-2，audit record 依 A-1 明記核對。
- README 新增 #24 段落（Taiwan Map、`Select Date`、代表點為專案定義、Derived Map Temperature 為導出值，AC-14 第 6 項）——見本次 commit 對 `README.md` 的變更。
- AC-17／AC-18 手動驗收清單與 `doc/acceptance/` 收錄、AC-10（Dashboard）最終重驗由 #25 依 derivation record §11.1 進行；本票已提供對應證據截圖。
- 合併進 `main` 為 acceptor 的 release 動作（RB-1），非本票完成條件。
