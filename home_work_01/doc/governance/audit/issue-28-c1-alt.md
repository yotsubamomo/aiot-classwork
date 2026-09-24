# Audit record — Issue #28，cycle 1，Alternate Independent Review（A-4 independent audit，治理 §4.4 唯一一次 Alternate Review）

| 欄位 | 內容 |
| --- | --- |
| Work Contract | GitHub Issue **#28**（`yotsubamomo/aiot-classwork`）「Taiwan Map 視覺重做（post-baseline enhancement）」。本 work item 的 Outcome Contract＝acceptor 2026-09-24 直接指示（核定文逐字見 DR-20 §0；Bindings §2.3 末項、§4 第 3 列）。Governing decisions：**DR-20** `doc/governance/decisions/decision-20260924-taiwan-map-rework.md`（lane＝Lightweight；boundary B-1..B-16／X-1..X-8；§3.5(A) 整合重驗範圍；§3.6 驗收語義）；**DR-21** `decision-20260924-map-rework-rs1-rs2.md`（DR-21.1 OR-V2；DR-21.2 masthead 導言一句在 boundary 內）。不變契約：Spec v1.1 R-EN-1..R-EN-7、R-SHR-4、R-SEC-1..3、INV-1/2/5/6/7/9、AC-04(b)、AC-15、AC-17/18/19/20/21/27/28；DR-19；high-risk H-2／H-3、A-1、A-4。 |
| 受審 subject | branch `home_work_01-hw10-implementation`；**`5136bd24adffebe93769949241d0a6b08c08735f`**（cycle-1 第二次 targeted correction 後的 subject）。HEAD `5d8b169`：`git diff --name-only 5136bd2..5d8b169` 只有 `doc/governance/worklog/20260924-taiwan-map-rework.md`（record-only，Bindings §7）；工作樹 clean。前一 subject（R2 對象）`ecdc793`；R1 對象 `b4549e5`；本 work item BASE `d23de58`；accepted baseline `720c0a0`。本次 delta `git diff --name-only ecdc793..5136bd2`＝`static/app.js`、`doc/acceptance/screenshots/issue-28-state-loading.png`＋record-only（`audit/issue-28-c1-r2.md`、worklog）。 |
| Audit 種類 | **Alternate Independent Review**（治理 §4.4：R2 仍 blocking 後 exactly one Alternate Review），**cycle 1**。不重跑完整 R1、不開新 round；判斷 R2 後剩餘的每項 finding 是否有效、已解決、分類有誤或屬 design 問題，並抽驗 R2 確認過的修正與契約 invariants 是否在 `5136bd2` 上仍成立。本紀錄**不是** Spec Integration Audit（DR-20 §3.5）。 |
| 角色 | `alternate_reviewer`（definition `gov-alternate-reviewer`；Bindings §3.1 mapping `claude-fable-5-1`／`xhigh`） |
| Binding 證據 | 由派工者依 Bindings §3.4 從 harness 紀錄核對本 agent 的 `agentType`／model／effort，並記入 worklog 或 run record 的核對紀錄；本紀錄不自證 binding。Executor（`claude-opus-4-8`）與 Primary Reviewer（`claude-opus-5-5`）與本 Reviewer 為三種不同 model mapping，無 `diversity_lost`。另見 §5 follow-up FU-2（#28 各次派工的 binding 核對目前只有 Executor 與 R2 的 agentId 在已 commit 的紀錄中）。 |
| Independence（治理 §2.3） | (1) fresh context：未繼承 Executor、Primary Reviewer 或 Orchestrator 的對話；worklog「Targeted correction（cycle 2）」、R1／R2 record、ACCEPTANCE.md、tickets.md、commit message 與派工訊息的敘述一律當作待驗證主張，全部自行重測。(2) binding 見上一列。(3) 自主取得：自讀 DR-20、DR-21、R1／R2 record、worklog、ACCEPTANCE.md、tickets.md、Spec 相關條款、`static/app.js`、`static/styles.css`、`tests/test_map_frontend.py`、git 歷史與 diff、GitHub Actions log 與 deployment API；自己以 `git archive 5136bd2` 匯出乾淨 subject，自己執行 pytest 與 mutation，自己寫 Playwright-core 腳本驅動本機 Chrome headless 量測。(4) 本紀錄由 Reviewer 以自己的 Write 工具寫入。 |
| 日期 | 2026-09-24 |

## 1. 方法與環境

- **Subject 確認**：`git rev-parse HEAD`＝`5d8b169`；`git status --short` 空；`git diff --name-only 5136bd2 HEAD -- . ':!home_work_01/doc/governance'` 空（工作樹的非 record 檔案＝`5136bd2`）。`git diff --check b4549e5..5136bd2 -- static/app.js static/styles.css tests/test_map_frontend.py` 乾淨。commit `5136bd2` message 為 `[Modify] – …`＋`[Fix]／[Modification]／[Additions]`，無 Claude 標記。
- **乾淨環境**：`git archive 5136bd2 home_work_01` 匯出到 Reviewer scratchpad `subj/`（無 `.env`、無 `.venv`）；以 repo 的 Python 3.12.14 venv 執行，`CWA_API_KEY` unset、`HTTP(S)_PROXY=http://127.0.0.1:9`。
- **完全離線的瀏覽器量測，未啟動任何 server**：先用 Flask test client（`server.app`）把 `/`、`/api/health`、`/api/regions`、`/api/days`、七個 `/api/days/<date>`、六個 `/api/regions/<r>/series` 的回應 dump 到 `alt/api/`；Playwright-core 1.63.0 驅動 `C:/Program Files/Google/Chrome/Application/chrome.exe`（Chrome 153.0.8010.53，headless），以 `page.route('**/*')` 在假 origin `http://app.local` 下從匯出的 `static/` 與 dump 回應每個請求；**任何其他 origin 的請求一律記錄並 abort**（用來計算外部請求數）。DR-19 狀態以 route override 模擬（503 帶伺服器實際的 incomplete 訊息、2xx 空 values、8 s 延遲）。
- **量測方式**：`getBoundingClientRect`、`elementFromPoint`、`getComputedStyle`、文字節點 `Range.getClientRects()`（字元層級的裁切／遮擋面積）、真實 `mouse.click`／`mouse.move`／拖曳、`setViewportSize`。腳本在 scratchpad `alt/`（`serve.js`、`sweep.js`、`clicks.js`、`clicks2.js`、`n2.js`、`parity.js`、`dbg.js`、`probe.js`），輸出在 `alt/out/`。
- **量測校正（如實記錄）**：初版腳本有三個屬於 Reviewer 自己的 artifact，已修正後重測，本紀錄引用的都是修正後的數字：(a) Leaflet 關閉的 tooltip 會以 opacity 0 在 DOM 停留 200 ms，初版以 `querySelector` 抓到前一顆 pill 的殘留 tooltip；修正為只取「包含所指 Region 名且 opacity > 0.9」的 tooltip，並在移開後等 350 ms。(b) `initMap` 的 `fitBounds` 是 Leaflet 的 250–350 ms 動畫（`probe.js`：1024 為 zoom 動畫、1280／375 為 pan 動畫），初版在動畫中量 rect 與 hover，造成 1280 左緣點擊「失敗」與 1024 北部 tooltip 方向暫時錯誤；修正為 ready 後等 900 ms 再量，並在每次點擊前重取 rect。(c) 拖曳後 400 ms 內仍在 Leaflet 慣性動畫中，初版誤判 pan 被重設；修正為放開後等 1.5 s。真實點擊經 `probe.js` 確認**不觸發任何 map 事件、pane transform 不變**，所以 (b) 不是產品行為。
- 結束時：Reviewer 未啟動 server；各腳本自行 `browser.close()`；結束時 `tasklist` 無 node.exe、無 headless chrome.exe 殘留。

## 2. R2 後剩餘 findings 的獨立判斷

### N-1（R2 Medium，blocking）— **已解決（RESOLVED）**

- **R2 主張**：`issue-28-state-loading.png` 在 `ecdc793` 與 `issue-28-desktop-dark-ac17.png` byte 相同，AC-19 的 loading 證據不成立。
- **Reviewer 自驗**：
  - `git show <sha>:…/issue-28-state-loading.png | md5sum`：`b4549e5`＝`a7544ad0ff69cadb09dad49369fea861`（原始 loading 圖）→ `ecdc793`＝`45ceda3aa14644c002027c3379d669ad`（＝`desktop-dark-ac17`，R2 指出的回歸）→ **`5136bd2`＝`c301adf87c35cd9bd6e00cca39c39fdc`**。
  - 工作樹 15 張 `issue-28-*.png` 的 md5 全部相異（`md5sum | uniq -d` 無輸出）；`desktop-dark-ac17` 仍為 `45ceda3a…`，loading 已不再與它相同。
  - Reviewer 以 Read 開啟該 PNG（2112×1276）：地圖卡標題 `Taiwan Map`、右上 `Showing 2026-09-24`；資訊面板在左上（`Six-region forecast`、`DERIVED` chip、**`Select Date` 顯示 `2026-09-24` 且為可操作的 select**、`Forecast Day: –`、來源句、兩張 tile 為 `–`、所選 Region 區塊 `北部地區` 各欄 `–`）；地圖框中央為 inline 訊息 **`Loading 2026-09-24…`**（淺藍 loading 樣式）；右下圖例四段有色；卡片不空白。這是 DR-19 的 loading 狀態（`/api/days/<date>` 在飛行中、面板保留、`Select Date` 可用，P-7(b)），不是已載入的地圖、也不是 empty／error。
  - 引用一致：`ACCEPTANCE.md` AC-19 列的 shots 清單含 `issue-28-state-loading.png`；worklog「Targeted correction（cycle 2）」記載新檔 md5 `c301adf8…`，與實檔相同。
  - 產品行為對照：Reviewer 自己在 12 個寬度模擬 loading（8 s 延遲），`#map-status` 顯示 `Loading 2026-09-24…`、`role=status`、`Select Date` 可見且可點（見 §3.1）；截圖內容與實際行為一致。
- **判定**：R2 的 closure 條件（真正的 loading 截圖、md5 唯一、引用一致、不需改實作）全部達成。**RESOLVED。**

### N-2（R2 Medium，non-blocking）— **已解決（RESOLVED），另有一項未驗證的 Low 附記**

- **R2 主張**：任何 `resize`（含只改高度）都呼叫 `fitToMarkers()`，行動瀏覽器工具列收合會重設使用者的縮放。
- **程式碼（`5136bd2` `static/app.js`）**：新增 `lastFitWidth`（`:97`）；resize handler（`:145-165`）在 150 ms debounce 後，`window.innerWidth !== lastFitWidth` 才 `fitToMarkers()`，否則只 `map.invalidateSize()`；`fitToMarkers()` 結尾 `lastFitWidth = window.innerWidth`（`:683`），init 的第一次 fit 即設定。`git diff ecdc793..5136bd2 -- static/app.js` 只有這三處，未動初始 fit、1180 breakpoint（`:674`）、`invalidateSize()`→`fitBounds()` 次序（`:673`→`:678`）、`ensureMapSized` 的 `ResizeObserver`／`visibilitychange` guard（`:532-558`）。
- **行為（`n2.js`、`dbg.js`，settled view）**：
  - 純高度變化保留縮放：375×812→375×740、375×812→375×900、1280×900→1280×820、1440×900→1440×600——zoom-in 後北部↔南部 pill 距離 489.5 px，改高度後仍 **489.5**、pane transform 不變（4／4 preserved）。
  - 純高度變化保留 pan：375 zoom-in＋拖曳（慣性結束後）pane `translate3d(-67px,-14px,0)` → 375×700 後仍 `translate3d(-67px,-14px,0)`。
  - 寬度變化重新 fit：→414×740、→360×900、→1000×820、→1280×600 距離回到 fit 值（244.4）且六 pill 全在 frame 內、與面板／圖例交集 0。
  - 1180 breakpoint：1179（stacked，fit 距離 489.5＝zoom 8）→1180（floating，重 fit 244.4，pill 與面板交集 0）→1179（stacked，重 fit）→1179×700（純高度，保留）。
  - P-12 不回歸：1280 zoom-in 後切換 `Select Date` 六次，距離與 pane transform 全程不變；`fitBounds(` 全檔仍只一處（`test_fitbounds_called_exactly_once`）。
  - Init hardening 不回歸：`#map-frame` 在 DOMContentLoaded 設 `display:none` 1.5 s 再顯示——隱藏期間 pill 數 0，顯示後六 pill 在 frame 內、marker transform 全為有限值、無 pageerror／console error。
- **判定**：R2 的 disposition（只在寬度／版面模式改變時 re-fit）已落實，且未破壞初始 fit、breakpoint、次序與 F-5 guard。**RESOLVED。**
- **附記（沿用 R2 的未驗證附記，Low，non-blocking，見 §5 FU-3）**：JS 以整數 `innerWidth >= 1180`、CSS 以 `max-width:1179px`／`min-width:1180px` 判定，在瀏覽器縮放產生 1179–1180 之間小數寬度時兩者理論上可能不一致（例如 1179.4 px：CSS 走 floating 預設規則、JS 走 stacked padding）。Playwright 的 viewport 只能整數，本次未驗證；可用 `matchMedia('(min-width:1180px)')` 消除。不是契約條款違反。

### N-3（R2 Low，non-blocking）— **已解決（RESOLVED）**

- worklog「V-2（依 DR-21.1／OR-V2 重寫）」表格的兩個描邊欄現為「描邊 #fff（**預設** default）」與「描邊 #9ed0ff（**hover/focus/選取**）」，並加一句「描邊顏色依狀態（P-4）：預設＝`#fff`…，hover/focus/選取＝`#9ed0ff`…」。
- Reviewer 以 WCAG 2.x 公式自算（token 值）：填色對海／台灣陸／周邊陸＝藍 3.26／2.37／2.92、綠 3.89／2.83／3.48、黃 7.39／5.38／6.62、紅 3.23／2.35／2.89；`#fff` 描邊 17.67／12.85／15.81；`#9ed0ff` 描邊 10.87／7.91／9.72；內文對填色 5.42／4.54／6.68／5.47——與表格數值逐一相同。每一色帶對每一底圖色「填色或描邊」至少一項 ≥ 3，四種狀態皆成立；`5136bd2` 的 computed 預設描邊為 `2px solid rgb(255,255,255)`（12 個寬度相同）、hover／focus-within／`is-active` 的 `border-color: #9ed0ff`（`styles.css:600-602`）；token 未變。
- **判定**：標籤已更正、數值不變、**V-2 結論 PASS（DR-21.1）不變**；ACCEPTANCE.md AC-19 列的「V-2 = PASS per DR-21.1 / OR-V2」引用正確。**RESOLVED。**

**剩餘 finding 小結**：N-1（唯一 blocking）已解決；N-2、N-3 已解決；沒有分類有誤的 finding；沒有實質屬 design／requirement 的問題（RS-1、RS-2 已由 DR-21 關閉且本 Reviewer 無異議）。

## 3. R2 已確認之修正在 `5136bd2` 上的抽驗（不回歸）

### 3.1 F-1／F-2／F-3（面板／圖例遮擋 pill、tooltip、狀態訊息）— **HOLDS**

`sweep.js`＋`dbg.js`，dark，12 個寬度 360／375／641／768／834／1023／1024／1100／1179／1180／1280／1440（settled view）：

- 版面：≤1179 資訊面板 `position:static`（stacked）、≥1180 浮動；地圖高 360（≤640）／440（641–1023）／560（≥1024）；每個寬度 `scrollWidth == innerWidth`。
- **Pill**：六個 pill 全在 `#map-frame` 內、與 `.map-panel--info`／`.map-panel--legend`／zoom 控制／attribution 的交集面積 **0**、中心 `elementFromPoint` 命中自己——12／12 寬度。
- **Tooltip**（逐一 hover，每次恰好一個可見 tooltip、內含該 Region 名）：文字 client rects 落在 frame 外的面積 **0**、被任一 overlay 遮的面積 **0**——12 寬度 × 6 pill 全部成立。方向：≤1179 北部向下開、其餘向上；≥1180 全部向上。唯二的非文字重疊：360／375 東部 tooltip 的右上 **padding** 與 zoom 控制重疊 284／193 px²（文字不受影響；與 R2 的觀察相同）；360 南部／東北部 tooltip 的 box 有 195／180 px² 在 frame 外（文字在內；360 在 V-3 的 375 判準之外，R1 F-11）。
- **DR-19 狀態**（error＝伺服器 incomplete 長訊息 503、empty＝2xx 空 values、loading＝8 s 延遲）：12 寬度 × 3 狀態的狀態文字 rects 在 frame 外 **0**、被面板／圖例遮 **0**；`role` 為 alert／status／status；`Select Date` 可見、未停用、7 個 option、捲入視窗後中心 `elementFromPoint` 命中 select（375／768／1024／1179 實測）；四個圖例 swatch 在三種狀態下都是四種不同顏色（F-6 不回歸）；error／empty 下改選 2026-09-26 後六 pill 正常渲染（P-7(b) 復原）。

### 3.2 F-4（375 相鄰透明 icon box 攔截點擊）— **HOLDS**

- computed `pointer-events`：`.pill-icon`＝`none`、`.pill`＝`auto`（12 個寬度相同）；`.rlabel`＝`none`；tooltip＝`none`。
- **真實點擊**（`clicks2.js`，每次點擊前重取該 pill 的 rect，點擊間隔 550 ms；360／375／414／1280 × 6 pill × 8 個位置＝左緣 +3%／中心／88%／右緣 −3%／右上／右下／左上／左下）：**48／48 全部選到自己的 Region**，錯選 0，`dblclick` 0，點擊前後 pane transform 不變。
- **44×44 取樣**（15×15，pill 中心）：每個 pill 210–225／225 命中自己，**命中其他 Region 0、命中 attribution 0**；其餘取樣點落在地圖底圖（非互動）。attribution 為右下角單行 `Natural Earth · 內政部 open data`。
- 說明：Reviewer 初版 `clicks.js` 在 1280 出現 5 次左緣點擊「失敗」，經 `probe.js` 證實是 Reviewer 在初始 fit 動畫中取到過期 rect 的 artifact（見 §1 校正 (b)），不是產品缺陷。

### 3.3 F-5（init hazard 回歸測試的偵測力）— **HOLDS**

Reviewer 在 `5136bd2` 匯出副本上自行做 mutation（`tests/test_map_frontend.py` 11 個測試）：

| 副本 | 結果 |
| --- | --- |
| 未突變 | **11 passed** |
| (a) `fitToMarkers` 內把 `map.invalidateSize()` 移到 `fitBounds()` 之後 | **1 failed**：`test_fittomarkers_invalidatesize_precedes_fitbounds` |
| (b) `if (sized()) { cb(); return; }` 改為 `cb(); return;` | **1 failed**：`test_ensuremapsized_guards_on_nonzero_container_size` |
| (a)+(b) | **2 failed**（上述兩個） |

行為面另見 §2 N-2 的 init hardening 測試（隱藏 1.5 s 後顯示，pill 數 0→6，無 NaN）。

### 3.4 F-6／F-8／F-9 與 R1 保留項

- F-6（狀態下圖例上色）：見 §3.1。F-8：`keyboard:false`（`app.js:613`）；地圖內 tab stop 只有六個 `.pill`。F-9：`issue-28-desktop-light-hover-tooltip.png` 存在且 md5 唯一。
- F-7／F-10／F-11：依 R1 disposition 保留，本次未要求處理；F-11 於 360 寬度可觀察（§3.1）。

## 4. 契約 invariants 與 high-risk 核對（A-1；H-2／H-3 明記）

### 4.1 Diff-scope 與 boundary（DR-20 §3.5(A)-1、DR-20.2、DR-21.2）— **HOLDS**

- `git diff --name-only b4549e5..5136bd2` 排除 `doc/**` 後只有 **`static/app.js`、`static/styles.css`、`tests/test_map_frontend.py`**；`doc/` 內為 `doc/acceptance/ACCEPTANCE.md`、14 張 `doc/acceptance/screenshots/issue-28-*.png`、`doc/ticket/tickets.md` 與 record-only 檔。`git diff --name-only b4549e5..5136bd2 -- static/index.html app.py server.py weather_query.py api vercel.json static/data README.md tests/test_static_checks.py tests/test_dashboard.py data.db requirements.txt .github` → **0 檔**。
- `styles.css` 的 delta 只在地圖區塊（`:433-445` `.map-status` 的 ≥1180 padding；`:547-562` `.pill-icon` 註解與 `!important`；`:639-668` 堆疊 breakpoint 由 640 提高到 1179、手機 `.map` 高度分離）；`app.js` 的 delta 只在地圖相關（resize handler 的 map 分支、`colourLegend()` 提前、attribution 文字、`keyboard:false`、click listener 掛 `.pill`、`refreshMapChrome`／`fitToMarkers`、`lastFitWidth`）；`renderSummary`／`renderTable`／`renderChart`／`showTooltip`／`loadRegion` 不在任何 hunk 內。masthead／controls／Weekly summary／折線圖／表格的 CSS 與 JS 未被本 correction 觸及。
- `index.html` 自 `b4549e5` 起未變；`720c0a0..5136bd2` 對 `index.html` 在地圖卡以外的唯一改動仍是 DR-21.2 已判定在 boundary 內的 masthead 導言一句（`git diff` hunk `@@ -20,8 +20,9 @@`），worklog 已補記並引用 DR-21.2。Reviewer 對此 boundary 無異議，不觸發 DR-20 §3.5 fail-safe。
- Grading App／MVM／`/api/`：`app.py`、`server.py`、`weather_query.py`、`api/` 未觸及；`test_app.py`（AppTest）與 INV-2 測試在 164 個通過測試內。

### 4.2 H-2（頁面概念詞逐字）— **HOLDS**

- `index.html` 未變（§4.1），R1 §2.5 對 `index.html` 的逐字核對結果延續。渲染 DOM（1280 dark、375 light、768 dark 三個 context 相同）：`<h1>`＝`Taiwan Weather Forecast`；`<label>Select Region</label>`、`<label>Select Date</label>` 存在；表頭 `["Date","MinT","MaxT"]`；面板 `Date`／`Min`／`Max`；六個 Region 中文名逐字出現在每個 pill 的 `aria-label` 開頭與 `.rlabel`（`北部地區`、`中部地區`、`南部地區`、`東北部地區`、`東部地區`、`東南部地區`，皆取自 `REGION_ORDER`）；`DERIVED` chip、來源句 `project-derived six-region values`、`not an observed daily mean`、`Last updated (data fetched from CWA)` 皆在。
- `test_dashboard.py::test_index_page_has_visible_teacher_text` 與 `test_map_frontend.py::test_index_has_map_panel_select_date_and_legend` 在 164 passed 內。

### 4.3 H-3（藥丸值／色直接取 endpoint；前端不重算、不重分帶）— **HOLDS**

- **七日 parity**（`parity.js`；1280 dark、375 light、768 dark）：對七個 Forecast Day 各以 `Select Date` 切換並等 `aria-label` 帶到該日期後，逐一比對六個 pill 的文字＝`derivedMapTemperature.toFixed(1)+"°"`、class＝`pill pill--<colourBand>`、computed background＝該 band token（`rgb(43,108,176)`／`rgb(47,133,90)`／`rgb(214,158,46)`／`rgb(197,48,48)`）；另比對 `Forecast Day`、兩張 tile 的 max／min 與 Region 名、所選 Region 區塊的 Date／Min／Max／Derived、四個圖例 swatch 顏色——**3 個 context × 7 日 × 6 pill＝126 筆 pill 比對，0 筆不符**；tile／所選區塊／圖例 0 筆不符。
- **AC-28 前端側**：以合成 `/api/days/2026-09-25`（19.9 blue、20.0 green、25.0 yellow、30.0 red、22.7 green，外加刻意不一致的 **31.0＋blue**）注入：六個 pill 的文字、class、底色**完全依 endpoint 的 band**（31.0 顯示 `31.0°`、底色 `rgb(43,108,176)` 藍）——證明前端不重算、不重分帶。
- `test_frontend_does_not_re_derive_or_re_band`（`mint + maxt`、20／25／30 門檻皆不得出現在 `app.js`／`basemap.js`）PASS。標示文字（chip、來源句、圖例註記、`(derived, not an observed daily mean)`）未變。

### 4.4 R-SEC-1／INV-6（零外部請求）與 H-1 — **HOLDS**

- 離線 harness 記錄每個 context 的全部請求：parity 三個 context 各 17 筆（載入＋7 次切日）、sweep 12 個 context 各 11 筆、clicks／n2 各 context——**全部 origin 只有 `http://app.local`（假的同源），外部請求 0**（任何其他 origin 會被記錄並 abort，記錄為 0）。
- CI credential scan（run `35968255009` log）：`credential scan passed: 536 tracked files; no .env tracked (only .env.example); no CWA-key-format string in tracked files or committed history; no Authorization value in fixture/raw JSON.`；`git ls-files home_work_01` 不含 `.env`。

### 4.5 INV-2／INV-9、AC-15、AC-17／18／19、AC-20／21 — **HOLDS**

- INV-2／INV-9：見 §4.1（相關檔案未觸及；`/api/` 形狀由 dump 的回應確認未變：`/api/days/<date>` 仍為 `{date, values[{regionName,mint,maxt,derivedMapTemperature,colourBand}]}`）。
- **AC-15（preview smoke，DR-20 §3.5(A)-3；R1 要求 correction 後的 subject 重做）**：GitHub deployments API `?sha=5136bd2…` → deployment **`6632269623`**（Preview，`success`，2026-09-24T07:11:35Z）→ `https://aiot-hw01-weather-eczp4gyzc-nchu-aiot-class.vercel.app`。subject 的 `smoke.py` 對該 URL：`[2026-09-24T08:10:55Z] SMOKE PASS … GET / -> 200 GET /api/health -> 200`，exit 0；served `/static/app.js` 含 `lastFitWidth`（3 處）＝部署的是 `5136bd2` 的程式。
- AC-17／AC-18／AC-19 的 #28 證據：ACCEPTANCE.md 三列的截圖檔全部存在且 md5 互異；AC-19 的 loading／empty／error 三張各自對應真實狀態（N-1 已解）；R-EN-1 各項在 375 與 ≥1024 的量測見 §3.1（無橫向捲動、可縮放可點選、三狀態可見、卡片不空白、`Select Date` 可操作）。
- AC-20／AC-21：乾淨匯出、無網路、無 `.env`：**`164 passed in 3.77s`**（Python 3.12.14）。CI：`5136bd2` push run `35968255009` 與 pull_request run `35968259191` 皆 **success**；log `164 passed in 4.24s`＋credential scan（見 §4.4）；`5d8b169`（record-only）的兩個 run 亦 success。

## 5. Non-blocking follow-ups（治理 §4.3：記錄 disposition 與 owner，不延長 cycle）

| ID | 內容 | Severity | Owner／disposition |
| --- | --- | --- | --- |
| FU-1 | 紀錄過期措辭：`ACCEPTANCE.md` §6「#28 A-4 R1」列仍寫「Awaiting R2」；`tickets.md` #28 列仍寫「待 R2」；worklog「Audit status」仍寫「等待 R2」，且「Targeted correction（cycle 2）」把 `5136bd2` 稱為「R3/closure 對象」並自稱「cycle 2」——依治理 §4.4／§4.5 沒有 R3，本次是 cycle 1 內 R2 後的第二次 targeted correction＋唯一一次 Alternate Review，audit record 命名亦為 `c1`。不影響任何驗證結論。 | Low | Executor：audit closure 後更新三份文件的狀態措辭（「cycle 2」改為「cycle 1 第二次 targeted correction」、「R3」改為「Alternate Review」）。 |
| FU-2 | Binding 可追溯性：已 commit 的紀錄只含 Executor（`a37f68bb30f67b595`，R1 record）與 R2 reviewer（`abca3f739e1523101`，worklog routing note）的 agentId；R1 record 與 worklog都寫「記入 run record」，但 `run-20260924-hw01-formal.md` 沒有任何 #28 條目。R1 reviewer 與本次 Alternate 的 binding 核對應由派工者依 Bindings §3.4 補記到 worklog 或 run record。屬 record 完整性，不影響 subject。 | Low | Orchestrator／派工者：補記 #28 各次派工的 agentId＋observed model／effort。 |
| FU-3 | N-2 附記：1179–1180 之間的小數 viewport 寬度下 JS（整數 `innerWidth`）與 CSS media query 可能不一致；未驗證。可改用 `matchMedia('(min-width:1180px)')`。 | Low | Executor：可選；不是契約條款。 |
| FU-4 | 觀察（非 finding，無需處理）：`initMap` 的 `fitBounds` 以 Leaflet 動畫（約 250–350 ms）完成，tooltip 方向在 `moveend` 後才由 `refreshMapChrome` 重算；在該視窗內 hover 可能短暫看到方向錯誤的 tooltip。使用者實務上不會在載入 300 ms 內 hover；settled 後全部正確（§3.1）。 | — | 記錄。 |
| — | R1 的 F-7／F-10／F-11 依 R1 disposition 維持。 | Low | 見 R1。 |

## 6. 結論

- R2 後剩餘的唯一 blocking finding **N-1 已解決**（真正的 loading 截圖、md5 唯一、引用一致、不需改實作）；**N-2、N-3 已解決**；沒有分類有誤的 finding；沒有需要 Design Authority 的 design／requirement 問題。
- R1 的 F-1／F-2／F-3／F-4／F-5 修正在 `5136bd2` 上經 Reviewer 獨立重測仍成立；F-6／F-8／F-9 亦成立。
- 契約 invariants 成立：H-2、H-3（126 筆七日 parity 0 不符；合成 band 注入證明不重算不重分帶）、R-SEC-1／INV-6（外部請求 0；credential scan 綠）、INV-2／INV-9（相關檔案未觸及）、DR-20 boundary（diff-scope 只在地圖卡；masthead 一句依 DR-21.2）、AC-15（`5136bd2` preview smoke PASS）、AC-20／AC-21（離線 164 passed；CI 綠）。
- 依治理 §4.4，Alternate Review 無未解 blocking → **audit closure**。Audit closure 不豁免治理 §3.8 的其他完成條件；合併仍是 acceptor 的 RB-1，繳交為 RB-2。DR-20 §3.5(B) 的 phase-acceptance 增補由 Orchestrator 依規則派 DA。

VERDICT: AUDIT CLOSURE
