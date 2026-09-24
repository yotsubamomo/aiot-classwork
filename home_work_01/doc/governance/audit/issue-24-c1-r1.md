# Audit record — Issue #24，cycle 1，R1

| 欄位 | 內容 |
| --- | --- |
| Work Contract | GitHub Issue #24（`yotsubamomo/aiot-classwork`）「Select Date 與 Leaflet Taiwan Map：依 Derived Map Temperature 著色」，Scope class ENHANCED REQUIRED（只在 Dashboard）。所屬 Spec：`home_work_01/doc/spec/SPEC.md` v1.1。需求：R-EN-3、R-EN-4、R-EN-5、R-EN-6、R-EN-7；R-SHR-4（前端等價）；R-DOC-2（導出值標示）；R-DS-3（日值 endpoint 的使用）。AC：AC-17、AC-18、AC-28（前端側）、AC-14 第 6 項、AC-19（重驗）；Ticket 本文另列 R-EN-6 記 worklog、INV-2／INV-9／CI 綠、README 本票段落、AC-27（本票範圍）。INV：INV-2、INV-7、INV-9。AB：AB-14、AB-15、AB-13（部分）。適用裁決：`decision-20260923-spec-interpretation-rulings.md` DR-1（代表點座標、CDN／vendored 屬 HOW）、DR-4（half-up、以顯示值分帶）；`decision-20260924-dashboard-state-mapping.md` DR-19（`/api/days*` 適用 per-Region 規則；無法解析的 2xx 是 error）；`decision-20260923-high-risk-categories.md` H-2、H-3、A-1。 |
| 受審 subject | branch `home_work_01-hw10-implementation`，HEAD **`87acc97e20b82f1f62f05687a4d20e4135e26da3`**（= `git ls-remote origin home_work_01-hw10-implementation`）；實作 subject **`4ec20b5e6bcca98361bf03f7a1d380e81561f87e`**（`git diff --name-status 4ec20b5..87acc97` 只有 `M home_work_01/doc/governance/worklog/issue-24.md`，record-only path，Bindings §7）；BASE `8d46ead`。範圍 `8d46ead..87acc97`，19 個檔案：`home_work_01/static/{app.js,index.html,styles.css}`（M）、`home_work_01/static/vendor/{leaflet.js,leaflet.css}`（A）、`README.md`（M）、12 張 `doc/acceptance/screenshots/issue-24-*.png`（A）、`doc/governance/worklog/issue-24.md`（A）。 |
| Audit 種類 | **R1**（accepted work scope 的完整 independent audit），**cycle 1**。Ticket audit，不是 Spec Integration Audit（Bindings §5 不採用單 Ticket fast path）。 |
| 角色 | `primary_reviewer`（definition `gov-primary-reviewer`；Bindings §3.1 mapping `claude-opus-5-5`／`xhigh`） |
| Binding 證據 | 由派工者（Orchestrator）依 Bindings §3.4 核對，記在 run record `home_work_01/doc/governance/run/run-20260924-hw01-formal.md`。該 run record 記載的 Executor binding：agent `a0b7cb41e09a556b4` = `gov-executor`／`claude-opus-4-8`／`high`（run record 第 63 行）。Executor 與 Primary Reviewer 的 mapping 為不同模型，沒有 `diversity_lost`。 |
| Independence（治理 §2.3） | (1) fresh context 派工，未繼承 Executor 的對話；worklog 與 run record 的敘述一律當作待驗證主張（worklog AC-18「切換後資訊卡值與該日 endpoint 一致」的 PASS 主張被本 audit 部分推翻，見 F-1）。(2) Binding 見上一列。(3) 自主取得：Reviewer 自讀 Ticket 本文（`gh issue view 24`）、Spec、DR-1／DR-4／DR-9／DR-19、H-2／H-3／A-1、#20 R2 與 #23 R2 的 tracked items、git 歷史與 diff、CI run 與 log；自己啟動本機 server、以自寫的 CDP client 驅動 headless Chrome 渲染、互動與量測，並以 CDP `Fetch` 攔截模擬各種回應。腳本全部自寫，放在 scratchpad 的 `r1/`。(4) 本紀錄由 Reviewer 以自己的 Write 工具寫入。 |
| 日期 | 2026-09-24 |

## 1. 審查方法與環境

- **確認 subject**：`git rev-parse HEAD` = `87acc97…` = remote。`git diff 4ec20b5 --stat -- home_work_01 ':!home_work_01/doc'` 為空，工作樹的實作與 subject 相同。`git status --short` 只列 Orchestrator 修改中的 run record（record-only）。`git diff --check 8d46ead..87acc97`（排除 vendored 檔）乾淨。兩個 commit message 為 `[Modify] – …` 格式，沒有 Claude 標記。
- **產品範圍**：`app.py`、`server.py`、`weather_query.py`、`data.db`、`requirements.txt`、`vercel.json`、`api/`、`tests/` 皆不在 diff；diff 全在 `home_work_01/` 內。`/api/days`、`/api/days/<date>` 由既有 `server.py:135-168` 提供（#21），本票只在前端使用。
- **Vendored Leaflet 身分**：`git show 4ec20b5:home_work_01/static/vendor/leaflet.js | openssl dgst -sha256 -binary | base64` = `20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=`，等於 Leaflet 1.9.4 官方發布的 SRI 值；檔頭 `Leaflet 1.9.4`。`leaflet.css` 工作樹檔案的 sha256 = `p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=`，等於官方 1.9.4 SRI 值；committed blob 因 `core.autocrlf=true` 以 LF 儲存（hash 不同），把 blob 的行尾還原為 CRLF 後 hash 同為 `p4Nx…`，即內容未改、只有行尾正規化。兩檔皆未經修改。
- **測試**：Reviewer 以 Python 3.12.14 venv 在 `home_work_01/` 執行 `python -m pytest -q -p no:cacheprovider` → **152 passed in 3.26s**；`tests/test_weather_query.py tests/test_static_checks.py tests/test_app.py tests/test_dashboard.py` → 83 passed。
- **瀏覽器**：自寫 `serve.py` 以 `server.create_app(...)` 在 127.0.0.1 啟三個 server：8761 正常 `data.db`；8762 `data.db` 在 scratchpad 的複本，只改 2026-09-24、2026-09-25 兩天共 12 格，使 endpoint 跨四個色帶並含 AC-28 邊界值（`wq.snapshot_status` = ok）；8763 不存在的 DB。自寫 CDP client（Chrome 153 headless=new）做 `Emulation.setDeviceMetricsOverride`（1280×900 desktop；375×812 mobile＋touch emulation）、`Input.dispatchMouseEvent`／`dispatchTouchEvent`（hover、click、tap）、`Fetch.fulfillRequest`／`failRequest`／暫停請求（狀態與順序模擬），並全程記錄 `Network.requestWillBeSent`、`Runtime.exceptionThrown`、console／Log 錯誤。量測以 `getBoundingClientRect`、`getComputedStyle`、SVG `fill` 屬性與 `document.documentElement.scrollWidth` 取得。
- **CI**：`gh run list --branch home_work_01-hw10-implementation`：`4ec20b5…` push `35940942570`、pull_request `35940944706` 皆 success；`87acc97…` push `35941045550`、pull_request `35941047498` 皆 success。`gh run view 35940942570`：headSha `4ec20b5e…`，job「offline test suite + credential checks (Python 3.12)」全部 step success；log：`Python 3.12.14`、`collected 152 items`、`152 passed in 4.05s`、`credential scan passed: 504 tracked files; no .env tracked …`。
- 結束時已停止 Reviewer 自己啟動的 server 與 Chrome；`git status` 與開始時相同（本紀錄檔除外）。

## 2. 需求、AC 與 invariants 逐條判定

| 項目 | 判定 | 證據 |
| --- | --- | --- |
| **R-EN-3** `Select Date` | **PASS** | 渲染 DOM：`<label for="date-select">` textContent `Select Date`（`index.html:74-75`）；7 個 option `2026-09-24 … 2026-09-30`，等於 `GET /api/days`，升序；預設選取 `2026-09-24`（第一天，`app.js:306-307`）。1280 與 375 相同。 |
| **R-EN-4／AC-17** Taiwan Map | **PASS**（資訊卡在切換日期後的問題歸 AC-18，見 F-1） | **以台灣為中心、涵蓋六標記**：1280 下 map 容器 668×380，六個 marker 全在容器內；marker 形心距容器中心 (+9.8, −0.5) px；台灣輪廓形心距中心 (−3, +30) px。375 下容器 311×320，六個 marker 全在容器內，形心偏移 (+10.3, −0.5) px。恰好 6 個 `path.leaflet-interactive`，沒有離島或第七個標記。**可縮放**：zoom 控制存在（`app.js:417-421` 另開 `scrollWheelZoom`）；1280 點 zoom-in 後 marker 最大間距 240.6 → 481.7 px（×2.00），zoom-out 回 240.6；375 以 tap 操作 zoom-in 視野改變。**顏色＝共用模組色帶**：真實資料 7 天 × 6 區 = 42 個 marker，每個 SVG `fill` 等於 `BAND_COLOURS[endpoint colourBand]`，全部相符（本快照 42 格皆 `yellow`，`#f2b705`）；band-spanning 合成 DB 2 天 × 6 區 = 12 個 marker 亦全部相符，涵蓋四個色帶（見 §3 H-3 的列表）。**資訊卡**：hover 出現 Leaflet tooltip，click 出現 popup，側欄 info card 同步更新；三者都含 Region、`Date`、`Min`、`Max` 與 Derived map temperature（一位小數，例 `27.0`、`20.0`），值與 endpoint 相同（42＋12 個 marker 逐一比對）。**圖例**：四段 `< 20 °C`／`20 – < 25 °C`／`25 – < 30 °C`／`≥ 30 °C`，swatch 計算後顏色 `rgb(43,108,176)`／`rgb(47,158,68)`／`rgb(242,183,5)`／`rgb(224,49,49)` = marker 用的 `BAND_COLOURS`；註記「Average = (MinT + MaxT) / 2, a derived value — not an observed daily mean.」（`index.html:176-187`）。**不需金鑰**：見 R-EN-6。代表點座標在 `app.js:52-59`，README:266-268 標示為專案定義。 |
| **AC-18** 切換日期 | **FAIL（F-1）**；清單與 marker 顏色 PASS | 七天逐一切換（1280、375、真實資料與合成 DB）：marker 顏色、hover tooltip、側欄 info card 的值每次都等於該日 endpoint；caption 顯示 `Showing <date>`。但切換時若有 marker 的 popup（click 資訊卡）開著，popup 仍顯示前一天的 `Date`／`Min`／`Max`／導出值，與已重新著色的 marker 矛盾，見 F-1。另在回應亂序時可能套用舊日期的值，見 F-3（non-blocking）。 |
| **R-EN-5** 圖例與導出說明 | **PASS** | 見 AC-17 列。 |
| **R-EN-6** 免金鑰／帳號／付費 | **PASS** | 1280 與 375 全程 network log 的請求只有 `http://127.0.0.1:8761/`、`/static/{styles.css,app.js,vendor/leaflet.css,vendor/leaflet.js}`、`/api/health`、`/api/regions`、`/api/regions/<r>/series`、`/api/days`、`/api/days/<date>`（另有一次 `/favicon.ico` 同源 404，#24 之前即存在）；**non-same-origin 請求 0 筆**，`.leaflet-tile` 0 個，無 tile／CDN／字型／source map 請求；`leaflet.css` 的 `url(images/*.png)` 在執行期沒有被請求。Leaflet 以檔案 vendored，底圖是 `app.js:78-95` 的專案輪廓 GeoJSON。沒有任何金鑰、帳號或付費服務。worklog 有記錄（`worklog/issue-24.md:85-88`）。 |
| **R-EN-7** 單頁整合 | **PASS** | 同一頁含 `Select Region`、`Select Date`、Weekly summary、折線圖、表格、Taiwan Map（`index.html:60-190`）。地圖與日期獨立於 Region：六個 Region 逐一切換後 caption 仍 `Showing 2026-09-24`、marker 仍 6 個。 |
| **AC-28（前端側）／R-SHR-4** | **PASS** | 前端不重算：`app.js` 內與溫度有關的運算只有 `BAND_COLOURS[v.colourBand]`（`app.js:382`）與顯示用 `oneDp(v.derivedMapTemperature)`（`app.js:487,498`，對已是一位小數的值做 `toFixed(1)`）；grep 沒有 `(mint+maxt)/2` 或 20／25／30 門檻。共用模組推導與分帶未改（不在 diff），`tests/test_weather_query.py:308-322` 的五組邊界案例 PASS。worklog 記錄採「以 endpoint 值直接著色」路徑（`worklog/issue-24.md:66-68`），符合 AC-28 與 Ticket 的允許選項。 |
| **AC-14 第 6 項／R-DOC-2（導出值）** | **PASS** | README:271-278「Derived Map Temperature is a derived value: (MinT + MaxT) / 2, rounded half-up … It is not an observed daily mean.」；README:274-275 說明圖例的 derived 註記。 |
| **README 本票段落** | **PASS** | README:248-278：`Select Date`、Taiwan Map、vendored Leaflet 1.9.4、代表點為專案定義、Derived Map Temperature 為導出值。README:255-258 宣稱切換後「updates the info cards」，F-1 修正後才成立。 |
| **AC-19 重驗（R-EN-1 六項）** | **PASS** | (1) 視覺層級：masthead → controls（兩個 select）→ summary → chart／table → Taiwan Map（地圖＋側欄 info card＋圖例），各自成區。(2) 響應式：1280 下地圖 2fr／側欄 1fr；375 下單欄，地圖 311×320，六個 marker 在容器內、可 tap 開 popup、可縮放。(3) 摘要：Weekly summary 仍在。(4) 圖表：375 hover 第 4 個日期，tooltip「2026-09-27 MaxT 31.6°C MinT 24.1°C」，軸標籤與圖例存在（#23 行為未回歸）。(5) 三種狀態：見 DR-19 列。(6) 375×812 mobile：`scrollWidth` **375** = `innerWidth` 375；六個 marker 的 popup 逐一開著時各量一次仍為 375。1280：`scrollWidth` 1265（垂直捲軸 15 px）。375 下東側 marker 的 popup 右緣被地圖容器裁切，見 F-5（Low）。 |
| **DR-19／N-1** 狀態對應 | **PASS** | Reviewer 以 CDP `Fetch` 攔截逐項驗證（1280，`Runtime.exceptionThrown` 全部 0 筆）：`/api/regions` 回 200 非 JSON 或 200 空 body → 頁面 error（`#page-error` 顯示、`#page-empty` 隱藏，「The forecast data is currently unavailable.」），**N-1 已修**；`/api/health` 回 200 非 JSON → 頁面 error；`/api/regions` 回 500 → 頁面 error 並顯示伺服器訊息；`/api/regions` 回 `{"regions": []}` → 頁面 empty；missing DB（8763，真實 503）→ 頁面 error「The forecast database is missing. …」，且不請求 `/api/days`。地圖 inline：`/api/days` 回 200 非 JSON／500／503／網路失敗 → `state--inline-error`、`role="alert"`、地圖區塊隱藏（顯示伺服器訊息或「Cannot load the map right now…」）；`/api/days` 回 `{"days": []}` → `state--inline-empty`、`role="status"`；`/api/days/<d>` 回 404／503／200 非 JSON／網路失敗 → inline error（404 為「That date is not available in this snapshot.」）；`/api/days/<d>` 回 `{"values": []}` → inline empty；暫停 `/api/health` → 頁面 loading；暫停 `/api/days` → `state--inline-loading`「Loading the map…」。成功載入後切到一個回 503 的日期 → inline error、地圖隱藏；再切回正常日期 → 地圖恢復、值正確。三種 inline 樣式在 `styles.css:172-193` 各自定義。 |
| **R-DS-3（使用）** | **PASS** | 前端只以 `fetchJson("/api/days")`、`fetchJson("/api/days/" + encodeURIComponent(date))` 取日值（`app.js:294,331`）。 |
| **INV-2** | **PASS** | `test_inv2_series_equals_shared_module_for_all_regions` PASS。瀏覽器：六個 Region 逐一切換，表格 7 列 `(Date, MinT, MaxT)` 全部等於 `wq.region_series`。diff 未改圖表與表格的渲染函式；`fetchJson` 的改動只影響無法解析的回應（見 DR-19 列）。 |
| **INV-9／AC-26** | **PASS** | `app.py`、`weather_query.py`、`requirements.txt` 不在 diff；`tests/test_app.py`（`AppTest`）與 AC-26 靜態檢查 PASS。`Select Date` 與地圖只在 `static/`（Dashboard）。 |
| **INV-7** | **PASS** | 導出標示存在於圖例註記、側欄 info card「(derived, not an observed daily mean)」（`index.html:168-169`）、tooltip／popup「(derived)」（`app.js:486-488`）與 README:271-278。 |
| **AC-04(b)** | **PASS**（自動化涵蓋缺口見 F-4） | 三個前端靜態檢查 PASS。Reviewer grep：`app.js`／`index.html`／`styles.css` 無 `opendata.cwa.gov.tw`／`CWA_API_KEY`；`fetchJson` 字面目標全以 `/api/` 開頭。`static/vendor/` 兩檔：`opendata.cwa.gov.tw` 0 筆、`CWA_API_KEY` 0 筆（不分大小寫的 `cwa` 只命中 base64 資料 `ACwAAAAA`）；絕對 URL 只有 `https://leafletjs.com`（attribution 超連結）、`http://www.w3.org/2000/svg` 與 CSS 註解內兩個 bug tracker 網址，都不是請求。執行期 network log 證實沒有外部請求（R-EN-6 列）。 |
| **AC-27（本票範圍，R-DOC-5 四項）** | **FAIL（F-2）** | (1) 註解說明目的：新函式皆有註解；但 `index.html:62-63` 仍寫 Select Date「NOT implemented here」，`styles.css:239` 仍寫 reserved placeholders — 與程式不符。(2) 錯誤處理與明確訊息：PASS（DR-19 列）。(3) 沒有死碼：`styles.css:229, 239-268` 的 `.control--reserved`、`.placeholder*` 規則已無任何元素使用 — FAIL。(4) 結構對應資料流：PASS（`loadDays` → `loadDay` → `applyDay`／`ensureMap`，狀態集中在 `setMapStatus`）。 |
| **CI** | **PASS** | 見 §1。 |

## 3. 高風險類別核對（A-1）

### H-3 Derived Map Temperature 的等價性與「導出」標示

- **核對內容**：(a) 前端是否重算導出值或色帶；(b) 共用模組的推導與分帶是否被改動；(c) 端到端：畫面上每個 marker 的顏色與值是否等於共用模組經 endpoint 回傳的值，且涵蓋四個色帶與 AC-28 邊界；(d) 導出標示。
- **結果**：
  - (a) 未重算。唯一的溫度相關前端邏輯是 band 名稱對應顏色（`app.js:66-71, 382`）與一位小數顯示（`app.js:537-540` `oneDp`）。
  - (b) `weather_query.py`、`server.py` 不在 diff；AC-28 五組 pytest PASS（`tests/test_weather_query.py:308-322`）；Reviewer 另以 `wq.derived_map_temperature`／`wq.colour_band` 直接算出 (20.1,25.2)→22.7 green、(19.9,20.0)→20.0 green、(24.9,25.0)→25.0 yellow、(29.9,30.0)→30.0 red、(15,24.8)→19.9 blue。
  - (c) 真實資料 42 個 marker 全部相符。合成 DB（endpoint 由共用模組計算）：

    | 日期 | Region | MinT／MaxT | endpoint 導出值／band | marker fill | 資訊卡導出值 |
    | --- | --- | --- | --- | --- | --- |
    | 2026-09-24 | 北部地區 | 15／24.8 | 19.9／blue | `#2b6cb0` | 19.9 |
    | 2026-09-24 | 中部地區 | 19.9／20 | 20.0／green | `#2f9e44` | 20.0 |
    | 2026-09-24 | 南部地區 | 24.9／25 | 25.0／yellow | `#f2b705` | 25.0 |
    | 2026-09-24 | 東北部地區 | 29.9／30 | 30.0／red | `#e03131` | 30.0 |
    | 2026-09-24 | 東部地區 | 20.1／25.2 | 22.7／green | `#2f9e44` | 22.7 |
    | 2026-09-24 | 東南部地區 | 29.8／30 | 29.9／yellow | `#f2b705` | 29.9 |
    | 2026-09-25 | 北部地區 | 31／35 | 33.0／red | `#e03131` | 33.0 |
    | 2026-09-25 | 中部地區 | 10／12 | 11.0／blue | `#2b6cb0` | 11.0 |
    | 2026-09-25 | 南部地區 | 22／26 | 24.0／green | `#2f9e44` | 24.0 |
    | 2026-09-25 | 東北部地區 | 26／28 | 27.0／yellow | `#f2b705` | 27.0 |
    | 2026-09-25 | 東部地區 | 19.8／20 | 19.9／blue | `#2b6cb0` | 19.9 |
    | 2026-09-25 | 東南部地區 | 30／30 | 30.0／red | `#e03131` | 30.0 |

  - (d) 導出標示齊全（INV-7 列）。
  - **例外**：F-1 使 popup 在切換日期後顯示前一天的導出值（例：marker 已是 red／33.0，popup 仍寫 19.9）。這不是推導等價性的問題，而是畫面上出現與所選日期不一致的導出值，列為 blocking 並在 R2 重述。
- **判定**：推導單一來源、等價性與標示 **PASS**；導出值的顯示一致性待 F-1 修正。

### H-2 老師指定的頁面文字

- **核對內容**：`Select Date` 標籤、資訊卡的 `Date`／`Min`／`Max`；既有 `Taiwan Weather Forecast`、`Select Region`、表頭 `Date`／`MinT`／`MaxT` 是否被改；Grading App 側的 H-2 項目是否被觸及。
- **結果**：`Select Date` 逐字（渲染 textContent `'Select Date'`）；tooltip／popup／側欄都用 `Date`、`Min`、`Max`；`index.html` 的 diff 只動 `<head>` 的 CSS link、controls 區塊（placeholder 換成 `Select Date`）、map section 與 script，`<h1>`、`Select Region` label、表頭未改；`test_index_page_has_visible_teacher_text` PASS；六個 Region 中文名與順序不變；`app.py`、DDL、`data.db`、`requirements.txt` 不在 diff。
- **判定**：**PASS**。`Select Date` 目前沒有自動化測試保護，見 F-6（Low）。

## 4. Findings

### F-1 — 切換日期後，開著的 click 資訊卡（popup）仍顯示前一天的值

- **Severity**：Medium　**Blocking**：**是**
- **依據**：AC-18「切換日期後標記顏色與資訊卡值隨之更新，與該日 endpoint 值一致」；R-EN-4「點擊或 hover 顯示資訊卡」；Ticket #24 What to build「切換日期後標記顏色與資訊卡隨之更新」；README:255-258 的同一宣稱。H-3 相關（畫面上的導出值與所選日期不一致）。
- **證據**：
  - 程式：`applyDay`（`app.js:365-397`）每次切換都以 `marker.bindPopup(html, { autoPan: false })`（`app.js:387`）綁一個新的 popup，但沒有關閉或更新目前開著的 popup；`app.js` 內沒有 `closePopup` 或 `setPopupContent`。側欄 info card 被重設為北部地區的新值（`app.js:393-394`），hover tooltip 會被 Leaflet 重新綁定，但已開的 popup 不受影響。
  - 重現（合成 DB，1280）：點北部地區 marker（2026-09-24，blue）→ popup「北部地區 Date: 2026-09-24 Min: 15°C · Max: 24.8°C Derived map temperature: 19.9°C (derived)」→ `Select Date` 改為 2026-09-25 → `date-select.value` = `2026-09-25`、caption `Showing 2026-09-25`、該 marker `fill` = `#e03131`（red）、側欄 `北部地區／2026-09-25／33.0`，**popup 仍是 2026-09-24／15／24.8／19.9**。截圖 scratchpad `r1/stale-popup-synth.png`：紅色 marker 上方的 popup 寫 19.9°C。
  - 真實資料在 1280 與 375 都重現：點南部地區（2026-09-24，29.2）後切到 2026-09-28，popup 仍是「Date: 2026-09-24 … 29.2°C」，側欄為 `北部地區／2026-09-28／28.4`。
  - 附帶效果：留下的舊 popup 擋住其下方的 marker，hover 該 marker 時不會出現 tooltip（1280 真實資料下東部地區 marker 被擋）。
- **為何 blocking**：這是驗收操作中的一般流程（點 marker 看值，再換日期），每次都會發生，不需要特殊網路條件；手機上 `Select Date` 在地圖上方約 1600 px，使用者點過 marker 後捲回上方換日期、再捲回地圖，就會看到舊日期的值掛在新顏色的 marker 上。它直接違反 AC-18 的可觀察條件；依治理 §4.5 disposition 邊界第 1 項，主張契約違反的 finding 不能 defer。
- **Closure 證據（R2）**：在修正後的 subject 上，以 popup 開著（以及 tooltip 開著）的狀態切換日期，popup 須關閉或更新為新日期的 `Date`／`Min`／`Max`／導出值；以合成的跨色帶資料（或等效方法）在 1280 與 375 各示範一次；marker 顏色、側欄與 popup 三者一致；七天切換的既有行為無回歸。作法屬 HOW。
- 若 Executor 主張 popup 不屬於 AC-18 所稱的「資訊卡」，那是 blocking 判定的爭議，依治理 §4.3 交 Final Adjudicator；Reviewer 的判斷是：popup 是 click 出現的資訊卡，Ticket 與 README 也把它當作資訊卡。

### F-2 — AC-27（本票範圍）：placeholder 移除後留下死 CSS 與過時註解

- **Severity**：Medium　**Blocking**：**是**
- **依據**：AC-27／R-DOC-5 第 (1) 項（註解說明目的，須與程式一致）與第 (3) 項（沒有死碼）；AC-27 FAIL 欄明列「死碼」；Ticket #24 AC 清單「AC-27（本票範圍）」。先例：DR-19 §4.4 第 7 項把過時的狀態註解列為 AC-27 (1) 的修正要求。
- **證據**：
  - `styles.css:229` `.control--reserved { opacity: .7; }` 與 `styles.css:239-268` 整段「reserved placeholders (Select Date, Taiwan Map — Issue #24)」的 `.placeholder`、`.placeholder--inline`、`.placeholder--map`、`.placeholder__tag`、`.placeholder__note`：`grep -n "placeholder\|control--reserved" static/index.html static/app.js` 0 筆。這些規則原本服務於本票移除的 placeholder 標記（diff 移除了 `index.html` 的兩個 placeholder 與 media query 內的 `.placeholder--inline`，但保留了主規則），是本票造成的死碼。
  - `index.html:62-63` 註解「Controls: primary (Select Region) plus a reserved, disabled slot for the next ticket's Select Date (#24 — NOT implemented here, R-EN-7).」緊鄰已實作的 `Select Date`（`index.html:70-76`），內容相反。
  - 次要（併入同一修正即可，不單獨阻擋）：`app.js:20-31` 檔頭的 DR-19 狀態說明只列 chart card 與 `/series`，沒有提到地圖的 inline 狀態。
- **Closure 證據（R2）**：死規則移除（或重新被使用）、兩處過時註解更正；grep 證明 `static/` 沒有未使用的 placeholder selector；渲染無回歸（1280／375 版面、`scrollWidth` 375）。

### F-3 — `/api/days/<date>` 回應亂序時會套用已被取代的日期

- **Severity**：Medium　**Blocking**：否
- **依據**：AC-18（marker 與資訊卡須與所選日期一致）。
- **證據**：`loadDay`（`app.js:328-363`）在回應到達時沒有確認它仍是目前選取的日期。Reviewer 以 `Fetch` 暫停 `/api/days/2026-09-24`，依序選 2026-09-25 → 2026-09-24 → 2026-09-25，再放行暫停的請求：`date-select.value` = `2026-09-25`、caption `Showing 2026-09-25`，但 marker fill 變成 2026-09-24 的 `#2b6cb0,#2f9e44,#f2b705,#e03131,#2f9e44,#f2b705`，側欄日期變成 `2026-09-24`，直到再次切換才恢復。
- **為何 non-blocking**：需要較早的請求比較晚的請求更晚完成（例如以鍵盤方向鍵快速切換，加上 Vercel cold start 等延遲差異）；本機直連無法自然重現，也不在 AC-18 的手動驗收流程內。風險在宣告的 operating scope（部署後的 Dashboard）內但機率低。`loadRegion` 有同樣的模式，屬 #20／#23 已結案的程式，本 audit 不重開。
- **Disposition**：owner Orchestrator。它和 F-1 在同一組函式、同一個 AC-18 性質，Executor MAY 在 F-1 的 targeted correction 中一併處理（例如回應到達時與 `dateSelect.value` 比對、不符就丟棄），這不算無關的 scope 擴張；R2 不以此為 closure 條件。未處理時追蹤到 #25。

### F-4 — AC-04(b) 的自動化靜態檢查不掃 `static/vendor/`

- **Severity**：Low　**Blocking**：否
- **依據**：AC-04(b)（前端 JS／靜態資源不含 CWA URL／金鑰；證據欄「pytest 靜態檢查；Reviewer 審查前端請求目標」）。
- **證據**：`tests/test_static_checks.py:194-195` `_static_files()` 以 `_STATIC_DIR.iterdir()` 只列頂層檔案，因此三個前端檢查不涵蓋 `static/vendor/leaflet.{js,css}`。這個測試檔自 `0f5f00e` 起未改，本票沒有弱化檢查；worklog 也如實揭露（`worklog/issue-24.md:19, 110`）。
- **判斷**：對本 subject，排除 `static/vendor/` **可接受**：兩檔是未修改的上游 Leaflet 1.9.4（SRI hash 相符，§1）；Reviewer grep 無 `opendata.cwa.gov.tw`／`CWA_API_KEY`，其絕對 URL 都不是請求（§2 AC-04(b) 列）；執行期零外部請求；app 自己的 `app.js`／`index.html`／`styles.css` 仍在掃描範圍；CI 的 `tools/credential_scan.py` 對全部追蹤檔（含 vendor）做金鑰格式掃描。殘餘風險：之後若有人改動或新增 vendor 檔，AC-04(b) 的自動檢查看不到。
- **Disposition**：owner #25（最終驗證）或 Executor 自行決定：把 CWA URL／金鑰檢查改為遞迴（vendor 檔目前會通過），絕對 URL 檢查則對 vendored Leaflet 的 attribution URL 加上明確 allowlist。

### F-5 — 地圖 UX 細節（375 px popup 裁切、側欄重設、南端輪廓）

- **Severity**：Low　**Blocking**：否
- **證據**：(a) `autoPan: false`（`app.js:387`）使 375 px 下東側 marker 的 popup 右緣與關閉鈕被地圖容器裁切，內容仍可讀（scratchpad `r1/mob-popup-375.png`）；不造成頁面橫向捲動（六個 popup 各量 `scrollWidth` 375）。(b) 每次切換日期，側欄 info card 都重設為北部地區（`app.js:393-394`），不保留使用者剛看的 Region；值正確。(c) `fitBounds` 以 marker 為範圍（`app.js:461`），初始視野把台灣輪廓南端裁掉約 9 px；契約只要求涵蓋六個 marker，已符合。
- **Disposition**：不違反契約條款；Executor 自行決定，不需 owner。

### F-6 — `Select Date` 標籤沒有自動化回歸保護

- **Severity**：Low　**Blocking**：否
- **證據**：`tests/test_dashboard.py:58-67` 保護 `<h1>`、`Select Region` 與三個表頭，但沒有保護 `Select Date`；H-2 把 `Select Date` 列為評分依賴的頁面文字。
- **Disposition**：optional，owner #25 或 Executor 自行決定（在同一測試加一行 `>Select Date</label>`）。

## 5. Executor 證據的核對

- 12 張截圖存在且與 Reviewer 的渲染一致（`issue-24-map-date2-ac18.png`：2026-09-28、北部地區 24.4／32.4／28.4；`issue-24-map-bands-4colours.png`：四色著色；`issue-24-mobile-375-ac19.png`：375 全頁）。`issue-24-map-desktop-ac17.png` 與 `issue-24-map-date1-ac18.png` 為同一檔（sha256 `a9b7a410…`），作為 AC-18 的第一個日期可以接受。
- worklog 的 AC-17、R-EN-6、N-1、DR-19、INV-2、INV-9、CI、測試數與 vendored hash 等主張，經 Reviewer 獨立驗證相符。worklog AC-18「切換後資訊卡值與該日 endpoint 一致」在 popup 開著的情況下不成立（F-1）。worklog 列出的 leaflet.css sha256（`a7837102…`）是 CRLF 工作樹檔案的值，committed blob 為 LF（§1），不影響結論。

## 6. Routing signals

無。F-1～F-6 都能依 accepted contract 判定，沒有需要 Design Authority 裁決的語義不足或 boundary 疑義。

## 7. 結論

- Blocking：**F-1**（AC-18：popup 在切換日期後顯示舊值）、**F-2**（AC-27：死 CSS 與過時註解）。
- Non-blocking：F-3（Medium，owner Orchestrator，MAY 併入 F-1 的修正，否則追蹤到 #25）、F-4（Low，owner #25／Executor）、F-5（Low，Executor 自行決定）、F-6（Low，optional，#25／Executor）。
- 其餘 accepted scope（AC-17、R-EN-3／5／6／7、AC-28 前端側、AC-14 第 6 項、AC-19 重驗、DR-19／N-1、INV-2、INV-7、INV-9／AC-26、AC-04(b)、H-2、H-3 的推導等價與標示、CI）PASS。
- 下一步依治理 §4.4：Executor 對 F-1、F-2 做 targeted correction，再由 R2 依 §4 F-1、F-2 的 closure 證據核對；R2 須依 A-1 重述 H-3 的核對結果。

VERDICT: BLOCKING (F-1, F-2)
