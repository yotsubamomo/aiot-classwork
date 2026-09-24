# Audit record — Issue #23，cycle 1，R2

| 欄位 | 內容 |
| --- | --- |
| Work Contract | GitHub Issue #23（`yotsubamomo/aiot-classwork`）「Dashboard UI／UX 品質與響應式版面」，Scope class ENHANCED REQUIRED（只在 Dashboard）。Spec `home_work_01/doc/spec/SPEC.md` v1.1：R-EN-1、R-EN-2、R-EN-7（版面整合部分）、R-DS-6；AC-19；回歸 AC-02、AC-03、AC-04(b)、AC-10（Dashboard）；AC-26／INV-9；INV-2、INV-6、INV-9；AB-15。適用裁決：DR-1；H-2、A-1（`decision-20260923-high-risk-categories.md`）；**DR-19**（`decision-20260924-dashboard-state-mapping.md`，Dashboard loading／empty／error 的條件對應；把 R1 F-2 定為契約回歸，併入本 cycle 修正）。 |
| 受審 subject | branch `home_work_01-hw10-implementation`，HEAD **`5312c6f6d9d72d310f7f5397a468b574f3a744f0`**（= `origin/home_work_01-hw10-implementation`）；實作 subject **`fd654f3d8f25748e821a7ae949999f241ed824e6`**（`fd654f3..5312c6f` 只改 `doc/governance/worklog/issue-23.md`，record-only path，Bindings §7）；BASE `39fbab7`；R1 subject `610a797`。本 R2 的 correction delta 為 `610a797..fd654f3`：`static/app.js`（+100／−36）、`static/index.html`（+9／−5）、`static/styles.css`（+26／−5），以及截圖與 worklog。 |
| Audit 種類 | **R2**（closure review），**cycle 1**。依治理 §4.4 只核對：(1) R1 的 blocking finding F-1 與 DR-19 判為契約回歸的 F-2 是否真正解決；(2) 修正是否造成回歸；(3) 修正是否直接產生或暴露新的 blocking defect。不是第二次 full audit；新的 non-blocking finding 不延長 cycle。 |
| 角色 | `primary_reviewer`（definition `gov-primary-reviewer`；Bindings §3.1 mapping `claude-opus-5-5`／`xhigh`） |
| Binding 證據 | 由派工者（Orchestrator）依 Bindings §3.4 核對，記在 run record `home_work_01/doc/governance/run/run-20260924-hw01-formal.md`。R1 記載的 Executor binding 為 agent `abac86af43a37ad61` = `gov-executor`／`claude-opus-4-8`／`high`。correction 的 Executor binding 以 run record 為準。Executor 與 Primary Reviewer 的 mapping 為不同模型，沒有 `diversity_lost`。 |
| Independence（治理 §2.3） | (1) 本 R2 延續 Reviewer 自己的 R1 context（治理 §2.3 第 1 項允許），未繼承 Executor 的 context。修正後的檔案與 diff 都從磁碟重讀；worklog 的 correction 段一律當作待驗證的主張。(2) Binding 見上一列。(3) 自主取得：Reviewer 自讀 DR-19、`git diff 610a797..fd654f3`、修正後的三個 static 檔、worklog、CI run 與 log，並重新啟動自寫的本機 server，以自寫的 CDP 腳本（scratchpad `pr23r1/`：`servers.py`、`cdp.py`、`r2_tooltip.py`、`r2_states.py`）渲染、量測與取證，另對 live preview 渲染。(4) 本紀錄由 Reviewer 以自己的 Write 工具寫入。 |
| 日期 | 2026-09-24 |

## 1. 方法與環境

- **Subject**：`git rev-parse HEAD` = `origin/home_work_01-hw10-implementation` = `5312c6f…`。`git diff --stat fd654f3 -- static server.py weather_query.py app.py data.db api tests`（`home_work_01/` 下）為空，工作樹與實作 subject 相同。`git diff --name-only 39fbab7..5312c6f` 不含 `app.py`、`server.py`、`weather_query.py`、`data.db`、`requirements.txt`、`tests/`。`git diff --check 610a797..5312c6f` 乾淨。兩個新 commit 的 message 符合 git 規則，沒有 Claude 標記。`git status` 除了 Orchestrator 的 run record、R1 record 與 DR-19（皆為 record-only、未追蹤或修改中）以外乾淨。
- **本機 server**：沿用 R1 的 `servers.py`：5111 正常 `data.db`、5112 不存在的 DB、5113 只有表無列的 DB、5114 刪一列的 DB（41 列）、5115 每個 `/api/` 延遲 8 秒。
- **CDP**：Chrome headless=new，`Emulation.setDeviceMetricsOverride`（1280×950、1024×768、1280×820；375×812 mobile＋touch），`Input.dispatchMouseEvent`／`dispatchTouchEvent`，`Fetch.fulfillRequest`（模擬 500／502／504／404、2xx 空陣列、2xx 非 JSON），`Network.setBlockedURLs`（網路失敗）。每個情境都收集 `Runtime.exceptionThrown`。
- **測試**：Python 3.12.14 venv，在 `home_work_01/` 執行 `python -m pytest -q -p no:cacheprovider` → **152 passed**。
- **CI**：run `35934994213`（push，headSha `fd654f3…`，`home_work_01 CI`，success；log：`Python 3.12.14`、`152 passed in 3.91s`、`credential scan passed: 486 tracked files …`）；`35934995758`（pull_request，`fd654f3`）success；`5312c6f` 的 `35935080227`（push）與 `35935082960`（pull_request）success。
- **Live**：preview `https://aiot-hw01-weather-git-homework01-hw10-im-8efc12-nchu-aiot-class.vercel.app/` 的 `/static/app.js` md5 `af810bfb4b1b…` = `git show fd654f3:home_work_01/static/app.js | md5sum`。
- 結束時已停止 Reviewer 自己的 server（PID 18812）與 Chrome。

## 2. F-1（High，blocking）— 圖表 tooltip 被裁切：**已解決**

- **修正內容**（`610a797..fd654f3`）：`styles.css` 的 `.chart__canvas` 改為 `overflow: visible`，移除 tooltip 的 `transform: translate(-50%,-110%)`。`app.js` `renderChart` 改以容器實際像素寬繪製 SVG（`els.chart.clientWidth`），並在 resize 時重繪。`showTooltip` 改由 JS 計算位置：水平置中並 clamp 在 canvas 內；放在 MaxT 點上方會超出上緣時，翻到 MinT 點下方，再 clamp（`app.js` `showTooltip`、`clamp`）。每個 hit rect 加上 `<title>`。
- **Reviewer 的量測**（六區 × 七日 = 42 個 Region-日期；hover 在各日期 MaxT dot 的 x；檢查 tooltip 與每一個 `overflow` 非 visible 的祖先元素、canvas 及 viewport 的相對位置）：

| 寬度 | 結果 |
| --- | --- |
| 375（mobile＋touch） | 42／42：tooltip 可見，三列文字（Date、MaxT、MinT）逐字等於該日 `/api/` 值；完全在 canvas 內與 viewport 內；祖先裁切量 **0**；`.chart__canvas` 為 `visible/visible`，容器 `scrollWidth` = `clientWidth`（311）；`document.documentElement.scrollWidth` **375** ≤ 375。 |
| 1024 | 42／42 同上；`scrollWidth` 1009（含垂直捲軸）≤ 1024。 |
| 1280 | 42／42：可見、文字正確、在 viewport 內、祖先裁切量 0、無容器內捲動。東北部、東部、東南部地區的末日 tooltip 右緣超出 canvas 矩形 **≤ 0.6 px**：`offsetWidth` 取整數（101），canvas 寬為小數（583.6）。仍在 chart card 的 18 px padding 內，沒有任何祖先裁切，屬次像素誤差，不是缺陷。 |

- **最壞情況**（北部地區；週高點 09-28、首日 09-24、末日 09-30）：1280 與 375 下都顯示完整三列。375 的週高點翻到點下方（`out-r2/tap-clean-375-4.png`）；1280 的首日與末日分別貼齊 canvas 左、右緣（`out-r2/hover-1280-0.png`、`hover-1280-6.png`）。
- **Touch**：375 mobile emulation 下，在全新載入的頁面 tap 北部、南部、東北部地區的首日、週高點、末日（9 次），tooltip 皆可見、三列完整、在 canvas 內、裁切 0、`scrollWidth` 375。另外觀察到：同一頁先以 CDP 送滑鼠事件再 tap，模擬的滑鼠指標會在 tap 後觸發 `mouseout`／`mouseleave` 而把 tooltip 關掉。這是混用滑鼠與觸控模擬造成的 harness 現象，真機沒有另一個滑鼠指標，不列 finding。
- **數值 fallback**：42／42 的 `rect.chart__hit` 都有 `<title>`（例：`2026-09-28 — MaxT 32.4°C, MinT 24.4°C`）。`elementFromPoint` 在每個 dot 中心都回到帶 `<title>` 的 hit rect。
- **Live preview** 重現結果：北部地區首日、週高點、末日在 1280 與 375 下都完整、裁切 0、在 viewport 內；375 `scrollWidth` 375。
- **提交截圖**：`issue-23-desktop-chart-hover.png`、`issue-23-chart-hover-1280-{first,last}.png`、`issue-23-chart-hover-375-{peak,first,last}.png` 都完整顯示三列，位置與翻轉行為和 Reviewer 的渲染一致；因捲動位置不同，未做逐位元組比對。與 R1 不同，這組截圖支持 worklog 的主張。
- **判定**：R-EN-1 (4) PASS；R-EN-1 (2) 的 375 px 圖表互動 PASS。**F-1 closure。**

## 3. F-2 ／ DR-19（契約回歸，AC-10 Dashboard）：**已解決**

依 DR-19 §4.1 規則與 §4.4 的 closure 證據要求，以 Reviewer 自己的 server 與 CDP 模擬核對（1280×820；另在 375 抽驗 missing DB 與 `regions []`）：

| DR-19 §4.4 | 情境 | 結果 |
| --- | --- | --- |
| (1) | missing DB（5112）；empty DB（5113）；incomplete DB（5114） | 三者皆為 **error**：`#page-error` 可見、`role="alert"`、紅底（`rgb(253,236,236)`），內文為伺服器的 `error` 訊息：「The forecast database is missing. Run the ingestion pipeline to create it.」「…contains no snapshot yet…」「…is incomplete — it is not the full six Regions × seven Forecast Days.」`#page-empty` 未顯示；不是空白頁；`Runtime.exceptionThrown` **0**。`/api/health` 回 503 由 `test_health_{missing,empty,incomplete}_is_503` 驗證（PASS）。375 的 missing DB 同樣是 error。 |
| (2) | `/api/health` 500（HTML 與 JSON body）、502、504（空 body）、404（JSON）；`/api/regions` 500、404（JSON）；封鎖 `*/api/*` | 全部為 **error**。有 JSON `error` 時顯示該訊息（例：「Internal Server Error (simulated 500)」「Not found」），沒有時顯示「The forecast data is currently unavailable.」；網路失敗顯示「Cannot reach the forecast service…」。exceptions 0。 |
| (3) | `/api/regions` 回 2xx `{"regions":[]}` | **empty**：`#page-empty`（`role="status"`、中性底 `rgb(244,246,250)`）「No forecast data yet／No Regions are available in this snapshot.」。與 error（紅）、loading（`rgb(238,244,251)`）可辨。375 同樣是 empty。 |
| (4) | `/series` 回 2xx `{"series":[]}`（首次載入與切換 Region 各一次） | chart card 內顯示 inline **empty**「No forecast data for this Region yet.」（`state--inline-empty`、`role="status"`），summary 隱藏；card 不留白。 |
| 4.1 per-Region | `/series` 404、503、500（HTML）、網路失敗（R1 已測，路徑未變） | inline **error**（`state--inline-error`、`role="alert"`、紅底），文字分別為「That Region is not available in this snapshot.」、伺服器訊息、「The forecast data is currently unavailable.」；summary 隱藏、表格清空。 |
| (5) | loading：5115 在 1.2 秒時；以 `Fetch` 暫停 `/series` | 頁面層級 loading 可見（藍色 spinner）；等所有請求完成後正常顯示 dashboard。inline loading 為「Loading 南部地區…」（`state--inline-loading`，藍），與 inline error／empty 可辨。 |
| (6) | 截圖 | Reviewer 的渲染與提交截圖**逐位元組相同**：`issue-23-error-missing-db.png`（`982e9b7fd516`）、`issue-23-state-empty-db-error.png`（`f99de4cd0f2c`）、`issue-23-state-incomplete-db-error.png`（`bf5e656f83cf`）、`issue-23-state-network-error.png`（`adbc1a5c57a0`）、`issue-23-state-500-error.png`（`be77284121f6`，以 JSON body `{"error":"Internal Server Error (simulated 500)"}` 重現）、`issue-23-state-empty-regions.png`（`9d1aebd171a0`）、`issue-23-state-empty-series.png`（`f6db302e8cb8`）。`issue-23-loading.png` 畫面相同，差別只在 spinner 的動畫格。R1 時的舊截圖 `issue-23-empty.png`（舊的「503 → empty」）已刪除；`issue-23-error.png` 改名為 `issue-23-state-network-error.png`。 |
| (7) | 註解一致性 | `app.js` 檔頭（DR-19 對應與一句話原則）、`bootstrap`／`loadRegions`／`loadRegion` 的行內註解、`index.html` 的 ERROR／EMPTY 區塊註解，都已改為 DR-19 的對應，不再有「empty ＝ 503」。 |

- **AC-10（Dashboard）判定**：**PASS（已恢復）**。缺失、空表、不完整三種條件下，`GET /` 頁面顯示 error 狀態並帶出原因；health 與資料 endpoint 回 503 JSON（`tests/test_dashboard.py` 的 503 測試皆 PASS）；沒有例外、沒有空白頁。這是 #23 被分配的回歸 AC，沒有被 defer。`ac10_dashboard_error_missing_db.png` 的最終重拍仍依 DR-19 §4.4(6) 由 #25 進行，不影響本判定。
- **R-EN-1 (5)**：三種頁面層級狀態各自可見且可辨（PASS，維持）。**R-DS-6**：PASS（維持）。
- **F-2 closure。** 殘留的邊緣情況見 N-1（非本次修正造成，non-blocking）。

## 4. F-3、F-4、F-5（R1 的 non-blocking findings）

- **F-3（375 px 軸標籤）— 已解決。** SVG viewBox 寬等於容器寬（375：311 = 311；1024：517 = 517；1280：584 對 583.6），縮放 ≈ 1。刻度字實際 **11 px**（R1 為 4.75 px），軸標題 **12 px**（R1 為 5.2 px），刻度文字方框高 14 px（worklog 的「14px」指的是方框高度）。從 1280 動態縮到 375 不重新載入：重繪為 viewBox 311、縮放 1、刻度 11 px、`scrollWidth` 375。
- **F-4（新版面 AC-02／AC-03 截圖）— 已補。** `issue-23-dashboard-central.png`（`6874809e12cd`）、`issue-23-dashboard-southeast.png`（`7d25596d2217`）與 Reviewer 在 1280×1260 選中部地區、東南部地區的渲染逐位元組相同；`issue-23-desktop-ok.png`（`f35327dd660e`）與 `issue-23-mobile-375-ok.png`（`3be63aae0ae3`，375×1760 mobile）也逐位元組相同。
- **F-5 — 已解決。** (a) `index.html` 外層還原為 `<main class="page">`（DOM 確認 `main.page` 存在）。(b) inline 三態改為 `state--inline-{loading,error,empty}`，底色依序為藍、紅、中性，error 另設 `role="alert"`。

## 5. 回歸核對

| 項目 | 判定 | 證據 |
| --- | --- | --- |
| AC-26／INV-9 | **PASS** | `app.py` 不在 `39fbab7..5312c6f`；`tests/test_app.py`（`AppTest`）全數 PASS；AC-26 靜態檢查 PASS；ENHANCED 只在 `static/`。 |
| INV-2（AC-02／AC-03 Dashboard） | **PASS** | 1280 與 375：六區逐一切換，表格 7 列逐列等於 `wq.region_series`（共用模組，即 Grading App 的資料），兩條 polyline 各 7 點、14 個 dot，標題 `Temperature Forecast – <Region>`，summary 等於獨立計算的 min／max；`test_inv2_series_equals_shared_module_for_all_regions` PASS；`<option>` 六個、順序符合 R-SHR-2(b)。 |
| AC-04(b)／INV-6 | **PASS** | `static/` 內 `opendata`／`cwa.gov`／`CWA_API_KEY`／`Authorization` 0 筆；唯一絕對 URL 為 `app.js:541` 的 SVG namespace；請求只有 `fetchJson("/api/health")`（`:105`）、`fetchJson("/api/regions")`（`:124`）、`fetchJson("/api/regions/"+…+"/series")`（`:166`），經 `fetch`（`:477`）。三個前端靜態測試 PASS。 |
| R-EN-1 (1)(3)(6)、R-EN-7 | **PASS** | 版面與 R1 相同；375 `scrollWidth` 375，取消 `body{overflow-x:hidden}` 後仍為 375、越出視窗的元素 0 個，沒有內部捲動容器在捲動；`Select Date` 與 Map 仍為無互動元素的 placeholder。 |
| 全套測試／CI | **PASS** | 本機 152 passed；CI 見 §1。 |
| JS 例外 | **PASS** | tooltip、狀態、live 各輪 `Runtime.exceptionThrown` 皆 0。 |
| 修正本身造成的缺陷 | **無 blocking** | resize 重繪只在 `currentSeries` 存在時進行；`setChartStatus` 會清除 `currentSeries`，所以失敗、empty 或 loading 狀態下 resize 不會畫出舊圖。`mouseleave` 監聽重複加入時由 DOM 自動去重。翻到下方的 tooltip 會蓋住部分 x 軸刻度，桌機上 hover 久一點會同時出現原生 `<title>` 與自訂 tooltip；兩者都是外觀問題，tooltip 本身完整可見，不列 finding。 |

## 6. H-2 核對（decision A-1，R2 重述）

- **觸及的類別**：H-2（頁面文字）。
- **核對了什麼**：修正後在 1280 與 375 的渲染 DOM 讀取 `document.title` = `Taiwan Weather Forecast`；`<h1>` = `Taiwan Weather Forecast`；`label[for=region-select]` = `Select Region`；表頭 `Date`、`MinT`、`MaxT`；圖例 `MaxT`、`MinT`；軸標題 `Temperature (°C)`、`Date`；`Select Date` 保留位標籤仍在；Region 選項為六個含「地區」的中文全名，順序依 R-SHR-2(b)。`test_index_page_has_visible_teacher_text` PASS。`index.html` 在本次修正只改外層標籤（`div` → `main`）與註解，沒有動任何概念詞。`app.py`、`data.db`、DDL、`requirements.txt`、`README.md` 都不在 diff。
- **結果**：**PASS**，與 R1 相同，修正沒有影響 H-2。

## 7. 新 findings（non-blocking，不延長 cycle）

### N-1：2xx 但 body 無法解析時，頁面層級沒有依 DR-19 呈現為 error

- **Severity**：Low　**Blocking**：否
- **契約依據**：DR-19 §4.1 頁面層級第 2 列「`fetch` reject（網路失敗）或回應無法解析 → error」；§4.2(3)「失敗條件 MUST NOT 被描述成正常的『尚未有資料』」。
- **證據**：`app.js:476-487` 的 `fetchJson` 在 `:481` 以 `.catch(function () { return {}; })` 吞掉 JSON 解析錯誤，並回傳 `ok: response.ok`。以 `Fetch.fulfillRequest` 讓 `/api/regions` 回 200 `text/html`：頁面顯示 **empty**「No forecast data yet／No Regions are available in this snapshot.」，不是 error。讓 `/api/health` 回 200 非 JSON：頁面照常進入 dashboard，ingestion 時間顯示為 `unknown`。這段程式自 #20 以來沒有改過（`39fbab7:home_work_01/static/app.js:271`），不是本次修正造成的，也不在 DR-19 §4.4 列出的 closure 證據裡；AC-10 的三種條件（皆為 503）不受影響。
- **風險**：只有在 2xx 回應卻不是 JSON 時才會發生，例如使用者網路上的 captive portal 或設定錯誤的 proxy；Vercel 上的 Flask function 回應都是 JSON，錯誤頁都是非 2xx。畫面仍有可見訊息、不是空白頁，只是把失敗說成「沒有資料」。
- **Disposition**：Owner **Orchestrator**，交 #24 的 Executor。DR-19 §6 已要求 #24 新增的 `/api/days` 等請求適用 §4.1，而修正點就在同一個共用的 `fetchJson`，可在那時一併處理。#24 的 AC-19 重驗或 #25 的 AC-10／AC-19 重驗依 DR-19 §4.1 核對此列。契約語義清楚，不需要 DA routing。

### N-2：`styles.css` 檔頭註解已過時

- **Severity**：Low　**Blocking**：否
- **證據**：`styles.css:11-12`「only the chart and table have their own overflow containers」。修正後 `.chart__canvas` 已是 `overflow: visible`，只剩 `.table-scroll` 有自己的 overflow 容器。
- **Disposition**：只是註解文字，Executor 自行決定是否修正，不需追蹤。

## 8. 結論

- **F-1**：closure（§2）。**F-2／DR-19**：closure，**AC-10（Dashboard）已恢復**（§3）。**AC-19**：R-EN-1 六項在 1280、1024、375 全部 PASS，375 `scrollWidth` 375 ≤ 375，桌機、375、loading、empty、error 截圖齊全且為真實畫面。
- F-3、F-4、F-5 都已解決（§4）。修正沒有造成回歸，也沒有直接產生 blocking defect（§5）。H-2 PASS（§6）。
- 新的 non-blocking findings：N-1（Low，owner Orchestrator → #24）、N-2（Low，Executor 自行決定）。
- 不需要其他 authority。

VERDICT: CLOSURE
