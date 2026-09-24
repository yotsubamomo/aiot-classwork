# Worklog — Issue #23 Dashboard UI／UX 品質與響應式版面

- **Work item**：GitHub Issue #23（Formal lane，ENHANCED scope，Dashboard only）
- **Executing role**：`gov-executor`（Bindings §3.1 mapping：`claude-opus-4-8`，effort `high`）。Binding verification 依 Bindings §3.4 由派工者（Orchestrator／主 session）從 harness 紀錄核對 `agentType`／`message.model`／`effort`；本 worklog 記錄執行角色與依據，不複製 harness 日誌。
- **Branch**：`home_work_01-hw10-implementation`，BASE = HEAD `39fbab7`
- **開始**：2026-09-24

## Contract reference

- **Ticket**：Issue #23（ENHANCED REQUIRED，只在 Dashboard；Grading App 不動）。
- **Spec**：`home_work_01/doc/spec/SPEC.md` v1.1 — R-EN-1（六項 UI／UX 品質清單，全部 MUST PASS）、R-EN-2（保留概念詞）、R-EN-7（版面整合、預留 Select Date／Map 位置）、R-DS-6（狀態呈現）；§1.7、§4.2。
- **AC**：AC-19；回歸 AC-02、AC-03、AC-04(b)、AC-10（Dashboard）。
- **Invariants**：INV-2、INV-6、INV-9。AB：AB-15。
- **裁決**：DR-1（CSS 與圖表函式庫是委派的 HOW）。
- **High-risk**：H-2（保留老師可見概念詞：`Taiwan Weather Forecast`、`Select Region`、`Date`、`MinT`、`MaxT`、六個中文 Region 名）。本 worklog 記錄 H-2 核對（A-1）。

## Decisions and assumptions（HOW，DR-1 授權）

1. **無外部資源。** `tests/test_static_checks.py::test_frontend_makes_no_external_absolute_url_requests` 禁止 static/ 內任何 absolute URL（僅允許 `http://www.w3.org/2000/svg`）。因此不引入任何 CDN、web font、圖表函式庫或 Leaflet；圖表維持手繪 inline SVG，字型用 system stack。此限制與 R-EN-6 免金鑰／免付費一致，也讓 #24 的 Leaflet 決定留在 #24。
2. **概念詞保留（H-2 / R-EN-2）。** `<h1>` 內容維持 `Taiwan Weather Forecast`；`Select Region` 維持 `<label>`；表頭維持 `Date`／`MinT`／`MaxT` 的 `<th>`。整合版面主題「Taiwan Weather Dashboard」以 subtitle 呈現，不取代 H1 概念詞。
3. **摘要資訊（R-EN-1(3)）。** 取所選 Region 的七日序列（既有 `/api/regions/<r>/series`），前端只做 Math.min(mint)／Math.max(maxt) 聚合顯示「本週最低／最高」與其日期，無新業務邏輯（資料仍只來自 `/api/`，INV-2／AC-04(b) 不受影響）。
4. **三種狀態（R-EN-1(5)／R-DS-6）。** ~~loading＝請求進行中；empty＝`/api/health` 回 503（missing／empty／incomplete）；error＝網路失敗~~ **【由 DR-19 取代，見下方 targeted correction（cycle 1）】**。DR-19 的分類：loading＝請求進行中；**error＝任何失敗請求（網路失敗、無法解析、或任何非 2xx——含 503 missing／empty／incomplete、5xx、404）**，並顯示伺服器 `error` 訊息；**empty＝請求成功（2xx）但無內容**（`/api/regions` 空清單＝頁面 empty；`/series` 空序列＝inline empty）。快照不可用（503）永遠是 error。
5. **圖表互動（R-EN-1(4)）。** 保留圖例、軸標籤與每點 `<title>`；另加自訂 hover：垂直導引線＋highlight＋HTML tooltip 顯示 Date／MaxT／MinT，無函式庫。
6. **預留位置（R-EN-7）。** 以標示清楚的 disabled placeholder 區塊預留 `Select Date` 控制項與 Taiwan Map（#24），只放標籤與說明，不實作行為。

## Artifacts（進行中）

- `home_work_01/static/index.html`、`static/styles.css`、`static/app.js`（改版；Dashboard 前端）
- 截圖：`home_work_01/doc/acceptance/screenshots/`（#23 名稱）

## Verification（結果）

**環境**：本機 Python 3.12.14（uv-managed，scratchpad venv；CI 亦 3.12，AC-23 由 #22 CI 涵蓋）。本機預設 `python` 為 3.11.2，故以 3.12 venv 跑全套（與 CI 對齊）。截圖以 headless Chrome + CDP（`Emulation.setDeviceMetricsOverride`，DSF=1）擷取，量測值以 CDP 與 mcp 瀏覽器 `document.documentElement.scrollWidth` 雙重確認。

**Subject**：branch `home_work_01-hw10-implementation`；改動只在 `home_work_01/static/{index.html,styles.css,app.js}`（`git diff --stat`：3 檔，+646/−176）。`app.py` 不在 diff（`git diff --name-only | grep -c app.py` = 0）。

### R-EN-1 六項（全部 PASS）

| # | 項目 | 結果 | 證據 |
| --- | --- | --- | --- |
| 1 | 視覺層級：標題／控制項／圖表／表格／摘要各自可辨、主次分明 | PASS | masthead（eyebrow＋H1＋lead）、controls card、Weekly summary stat tiles、chart card、table card、reserved map card 各自成區。`issue-23-desktop-ok.png` |
| 2 | 響應式：桌機（≥1024px）與 375px 皆可完整操作 | PASS | `issue-23-desktop-ok.png`（1280，scrollWidth=1280）、`issue-23-mobile-375-ok.png`（375，單欄堆疊，控制項／摘要／圖表／表格全可讀） |
| 3 | 至少一項摘要資訊 | PASS | 「Weekly summary」兩張 stat tile：所選 Region 本週 Lowest MinT（23.3°C on 2026-09-24）／Highest MaxT（32.4°C on 2026-09-28），前端由 `/api/regions/<r>/series` 做 Math.min／Math.max 聚合，無新業務邏輯 |
| 4 | 圖表可互動且易讀：圖例、軸標籤、hover/tooltip 顯示數值 | PASS | 圖例（MaxT／MinT）、X 軸標籤（日期＋「Date」）、Y 軸標籤（Temperature (°C)）＋刻度；自訂 hover tooltip＋垂直導引線＋dot highlight，另保留每點原生 `<title>`。`issue-23-desktop-chart-hover.png`（09-28：MaxT 32.4°C／MinT 24.4°C） |
| 5 | loading／empty／error 三種狀態各有可見呈現 | PASS | loading（藍色 info 橫幅＋spinner「Loading the latest forecast…」，5003 節流）`issue-23-loading.png`；empty（中性橫幅「No forecast data yet」，5001 空表 DB→/api/health 503）`issue-23-empty.png`；error（紅色 alert「Something went wrong / Cannot reach the forecast service…」，5002 阻斷 /api 連線→fetch reject）`issue-23-error.png` |
| 6 | 375px 無不必要橫向捲動 | PASS | 375px 下 `document.documentElement.scrollWidth`＝**375**、`clientWidth`＝375、`window.innerWidth`＝375；掃描所有元素超出視窗右緣者＝**0**。CDP 與 mcp 瀏覽器兩處量測一致 |

**量測值（AC-19）**：375px 視窗，`document.documentElement.scrollWidth = 375 ≤ 視窗寬度 375`（不大於）。桌機 1280px：scrollWidth = 1280。

### R-EN-2 / H-2 概念詞（PASS）

`static/index.html` 靜態檢查：`Taiwan Weather Forecast`（`<title>` 與 `<h1>`）、`Select Region`（`<label>`＋aria-label）、表頭 `Date`／`MinT`／`MaxT`、圖例 `MaxT`／`MinT` 皆存在且逐字未改；中文 Region 名（北部地區…）為資料驅動、來自未改動的 `/api/regions`，截圖顯示 `北部地區`。`tests/test_dashboard.py::test_index_page_has_visible_teacher_text` PASS（守 `<h1>`、Select Region label、Date/MinT/MaxT 表頭）。**A-1 H-2 核對**：本票只改前端呈現，未觸及 `app.py`、`data.db`、`TemperatureForecasts` DDL、五欄名、`streamlit run app.py`、Region 名或既有頁面概念詞；概念詞逐字保留，未新增取代或弱化老師要求的行為。

### R-EN-7 整合與預留（PASS）

單頁整合版面（eyebrow「Taiwan Weather Dashboard」＋H1 概念詞＋controls／summary／chart／table 一體）。預留兩個標示清楚的 disabled placeholder：`Select Date`（controls 內，「COMING SOON」）與 `Taiwan Map`（頁尾卡片，「COMING SOON」＋說明），皆只放標籤／說明，未實作行為（#24）。

### INV-2 / AC-26 / INV-9（PASS）

- INV-2：`tests/test_dashboard.py::test_inv2_series_equals_shared_module_for_all_regions` PASS——六區的 `(Date, MinT, MaxT)` 與共用模組（＝Grading App）序列逐筆相同；資料仍只來自 `/api/`，表格與圖表內容未變（只改呈現）。
- AC-26／INV-9：`app.py` 不在 diff；`tests/test_app.py`（Streamlit `AppTest`）全數 PASS；`tests/test_static_checks.py` 的 AC-26 檢查 PASS（Grading App 無 map／Select Date／folium）。ENHANCED 只加在 Dashboard 前端。

### AC-04(b)（PASS）

`tests/test_static_checks.py::{test_frontend_has_no_cwa_url_or_key, test_frontend_makes_no_external_absolute_url_requests, test_frontend_requests_use_the_api_prefix}` PASS；靜態 grep：`opendata.cwa.gov.tw`／`CWA_API_KEY` 在 static/ 為 0；前端唯一 absolute URL 為 SVG namespace（allowlist）；所有 `fetch/fetchJson` 字面目標以 `/api/` 開頭。

### 全套離線測試（PASS）

`python -m pytest`（3.12，無網路、無 `.env`）：**152 passed**。含 Flask test client（AC-02/03/10 Dashboard 回歸、AC-16 health）、AC-04 靜態檢查、Streamlit `AppTest`、derive/DB/共用模組各類。

### CI（PASS）

Push `610a797` 觸發 `.github/workflows/home_work_01-ci.yml`（Python 3.12，offline pytest 全套＋憑證機械檢查 A-5）：
- push run `35930941816` → completed/**success**（sha 610a797）
- pull_request run `35930943558` → completed/**success**（sha 610a797）

job「offline test suite + credential checks (Python 3.12)」全步驟綠（Show Python version 確認 3.12；full offline pytest；credential checks AC-07 b/c/d）。註記僅為 GitHub 對 Node20／ubuntu label 的 deprecation 提醒，非失敗。

## Targeted correction — cycle 1（R1 BLOCKING F-1；DR-19 契約回歸 F-2）

**輸入**：R1 audit `doc/governance/audit/issue-23-c1-r1.md`（VERDICT: BLOCKING (F-1)）；DA 裁決 `doc/governance/decisions/decision-20260924-dashboard-state-mapping.md`（**DR-19**，把 F-2 定為必修的契約回歸，併入本 cycle）。同一 work item、同一 worklog、同一 branch。治理 §4.4 targeted correction：只修 findings，不弱化測試、不擴大 scope。

**新 subject**：`home_work_01-hw10-implementation`，correction commit（見 §CI-2）；改動只在 `static/{app.js,index.html,styles.css}`（`git diff 84722c1 -- static`：3 檔）。`app.py` 自 BASE `39fbab7` 起未被觸及（`git diff --name-only 39fbab7 -- app.py` 空）。

### F-1（High, blocking）— 圖表 tooltip 被容器裁切 → 已修

- **成因**：`.chart__canvas { overflow-x: auto }` 使 overflow-y 計為 auto 而裁切；tooltip 以固定 `translate(-50%,-110%)` 放在近上緣的 MaxT 點上方。
- **修法（HOW，DR-1）**：(a) `.chart__canvas { overflow: visible }`（移除裁切與 hover 時的內部捲軸）；(b) SVG 改以**容器實際像素寬**繪製（`renderChart` 量 `clientWidth`，scale≈1），並在 resize 重繪；(c) tooltip 位置改由 JS 計算——水平置中並 clamp 於 canvas 內、垂直優先放點上方，會裁到上緣時**翻轉到點下方**，再 clamp；(d) hit-rect 各加 `<title>`，補回被覆蓋的數值 fallback。
- **closure 證據**（CDP，`Emulation.setDeviceMetricsOverride`，DSF 1；量 tooltip 與 canvas 的 `getBoundingClientRect`）：北部地區七日在 **1280 與 375** 下對三種最壞情況——**top-edge 週高點（idx 4）、第一天（idx 0）、最後一天（idx 6）**——tooltip 皆 `full_visible=True`、三列（Date＋MaxT＋MinT）完整、`within_canvas=True`、`in_viewport=True`、`overflow=visible/visible`、`canvasNoInnerScroll=True`、`document.documentElement.scrollWidth ≤ innerWidth`（1280≤1280、375≤375）。截圖：`issue-23-desktop-chart-hover.png`（1280 峰值）、`issue-23-chart-hover-1280-{first,last}.png`、`issue-23-chart-hover-375-{peak,first,last}.png`（375 峰值示範翻轉到點下方）。

### F-2 / DR-19（契約回歸，必修）— 狀態對應 → 已依 DR-19 §4.1 實作

- **實作**：頁面層級（`bootstrap`：`/api/health`→`/api/regions`）任何非 2xx → `showError`（紅色 `role="alert"` `#page-error`，內文為伺服器 `error` 訊息）；`/api/regions` 2xx 空清單 → `showEmpty`（頁面 empty）。Per-Region（`/series`）非 2xx／網路失敗 → inline **error**（`state--inline-error`，紅）；2xx 空序列 → inline **empty**（`state--inline-empty`，中性，「No forecast data for this Region yet.」，不留白）；in-flight → inline **loading**（`state--inline-loading`，藍）。`app.js` 檔頭與 `index.html` 的「empty＝503」註解已改為 DR-19。
- **closure 證據（DR-19 §4.4）**（CDP；page-level state 探測 `#page-error`／`#page-empty`／`#chart-status` 的可見性、文字、role、`Runtime.exceptionThrown` 計數）：
  - §4.4(1) missing DB（5006）、empty DB（5001）、incomplete DB（5007）：三者皆 **error**（`role="alert"`），內文為伺服器訊息（「database is missing」／「contains no snapshot yet」／「snapshot is incomplete」），`empty=false`，exceptions=**0**。截圖 `issue-23-error-missing-db.png`（＝AC-19 error 截圖，兼 AC-10 回歸證據）、`issue-23-state-empty-db-error.png`、`issue-23-state-incomplete-db-error.png`。
  - §4.4(2) 非 503 失敗：`Fetch.fulfillRequest` 回 500（`issue-23-state-500-error.png`）與封鎖 `/api/*` 的網路失敗（`issue-23-state-network-error.png`）皆 **error**。
  - §4.4(3) `Fetch.fulfillRequest` 回 2xx `{"regions":[]}` → **empty**（「No Regions are available in this snapshot.」）：`issue-23-state-empty-regions.png`。
  - §4.4(4) `Fetch.fulfillRequest` 回 2xx `{"series":[]}` → chart card 內 inline **empty**、不留白：`issue-23-state-empty-series.png`。
  - §4.4(5) loading 不變：`issue-23-loading.png`（5003 節流）。
  - 全部 12 個情境 `Runtime.exceptionThrown` = 0。
- worklog 的「決定 4」已標示由 DR-19 取代（見上方 Decisions）。

### F-3（Medium）— 375px 軸標籤約 4.8px → 已修

SVG 改以容器寬繪製後 scale≈1，字級以真實 px 呈現。量測（`.chart__tick-label` 的 `getBoundingClientRect().height`）：375 與 1280 皆 **14px**（原 375 約 4.8px）。截圖 `issue-23-mobile-375-ok.png`、`issue-23-chart-hover-375-*.png` 可見刻度與軸標題清楚。

### F-4（Low）— 新版面 AC-02／AC-03 截圖 → 已補

`issue-23-dashboard-central.png`（中部地區）、`issue-23-dashboard-southeast.png`（東南部地區），新版面、7 列、`Date`／`MinT`／`MaxT`、值與 `data.db` 一致。

### F-5（Low）— 無障礙與狀態辨識 → 已修

(a) 外層 `<div class="page">` 還原為 `<main class="page">`（`main` landmark 回復）。(b) inline per-Region 三態改用不同視覺（loading 藍／error 紅／empty 中性；`state--inline-{loading,error,empty}`），error 另設 `role="alert"`。

### 回歸與陳舊證據

- 全套離線測試（3.12，無網路／無 `.env`）：**152 passed**（含 AC-02/03/10 Dashboard、AC-04 靜態、`AppTest`）。
- 概念詞（H-2／R-EN-2）、AC-04(b)（static/ 無 CWA/key、僅 SVG namespace、fetch 皆 `/api/`）、INV-2、AC-26/INV-9（`app.py` 未在 diff）維持 PASS。
- 移除兩張陳舊截圖（舊 mapping）：`issue-23-empty.png`（舊「503→empty」）、`issue-23-error.png`（由 `issue-23-state-network-error.png` 取代）。

## Audit status

Formal Ticket → independent audit required（Bindings §5；治理 §4.1）。cycle 1 R1 = BLOCKING (F-1)；本次 targeted correction 已附 F-1 的 closure／回歸證據與 DR-19（F-2）的 §4.4 證據，交 **R2**（Primary Reviewer 延續其 R1 context、重讀修正後檔案與 diff）核對，範圍依 R1 §6＋DR-19 §4.4。R2 由 Orchestrator／主 session 依 Bindings §3.5 派工，不由 Executor 自派。本 Ticket 觸及 H-2，audit record 依 A-1 明記核對。

## Remaining work

無 blocking 剩餘工作。targeted correction 與 self-verification 完成；committed 並 pushed；CI 綠。

**§CI-2（correction commit `fd654f3`）**：push run `35934994213`、pull_request run `35934995758` 皆 completed/**success**（sha fd654f3）。job「offline test suite + credential checks (Python 3.12)」全綠（152 passed）。BASE `39fbab7`；cycle-1 commit 序列：`610a797`（原實作）→ `84722c1`（CI 紀錄）→ `fd654f3`（targeted correction，受審 subject）。
- 待 R2 closure review（Primary Reviewer）。
- `Select Date` 控制項與 Taiwan Map 為 #24 範圍：本票只留標示清楚的 disabled placeholder，未實作；#24 在本版面加入地圖後須依 Cross-ticket invariants 重驗 AC-19。#24 之後新增的 `/api/days`、`/api/days/<date>` 請求適用 DR-19 §4.1 的 per-Region 規則。
- AC-10（Dashboard）最終截圖重拍與 AC-02/03 `doc/acceptance/` 收錄由 #25 依 derivation record §11.1 進行；本票已提供對應證據截圖。
- 合併進 `main` 為 acceptor 的 release 動作（RB-1），非本票完成條件。
