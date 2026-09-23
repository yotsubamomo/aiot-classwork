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
4. **三種狀態（R-EN-1(5)／R-DS-6）。** loading＝請求進行中的可見指示；empty＝`/api/health` 回 503（missing／empty／incomplete）時的「目前無可用預報」空狀態；error＝網路失敗或非預期錯誤的錯誤橫幅（role=alert）。三者互斥且各自可截圖。
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

### CI

見下方「CI」段（push 後補）。

## Audit status

Formal Ticket → independent audit required（Bindings §5；治理 §4.1）。本 Ticket 觸及 H-2，R1 audit record 依 A-1 須明記核對。audit 由 Orchestrator／主 session 依 Bindings §3.5 派工，不由 Executor 自派。

## Remaining work

實作 static 三檔 → self-verification（pytest 全套、瀏覽器截圖五張、375px scrollWidth 量測、概念詞靜態檢查、app.py 未動確認）→ commit＋push → 確認 CI 綠。
