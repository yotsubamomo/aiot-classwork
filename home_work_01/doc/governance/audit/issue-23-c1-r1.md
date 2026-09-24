# Audit record — Issue #23，cycle 1，R1

| 欄位 | 內容 |
| --- | --- |
| Work Contract | GitHub Issue #23（`yotsubamomo/aiot-classwork`）「Dashboard UI／UX 品質與響應式版面」，Scope class ENHANCED REQUIRED（只在 Dashboard，Grading App 不動）。所屬 Spec：`home_work_01/doc/spec/SPEC.md` v1.1。需求：R-EN-1（六項，全部 MUST PASS）、R-EN-2、R-EN-7（版面整合部分）、R-DS-6（狀態呈現）；§1.7、§4.2。AC：AC-19；回歸 AC-02、AC-03、AC-04(b)、AC-10（Dashboard）；Ticket 本文另列 AC-26／INV-9、CI 綠、AC-27（本票範圍）。INV：INV-2、INV-6、INV-9。AB：AB-15（Outcome Contract `outcome-contract.md:83`）。適用裁決：`decision-20260923-spec-interpretation-rulings.md` DR-1（CSS／圖表函式庫屬 HOW）；`decision-20260923-high-risk-categories.md` H-2、A-1；`decision-20260924-unattended-run-policy.md` N-16、N-17、N-27。分配依據：`derivation-SPEC.md:163`（#23 列）；AC-10、AC-19 另由 #24（AC-19 重驗）與 #25（重驗 AC-02／03／04／07／10／19／24）重驗（`derivation-SPEC.md:164-165`）。 |
| 受審 subject | branch `home_work_01-hw10-implementation`，HEAD **`84722c1318662a99d2d3a52e87208ded648c0711`**（= `origin/home_work_01-hw10-implementation`）；實作 subject **`610a79771079ad626c6854b3ffabddef712bbd8c`**（`610a797..84722c1` 只改 `home_work_01/doc/governance/worklog/issue-23.md`，record-only path，Bindings §7）；BASE `39fbab7`。範圍 `39fbab7..84722c1`，10 個檔案：`home_work_01/static/{app.js,index.html,styles.css}`（+646／−176）、6 張 `doc/acceptance/screenshots/issue-23-*.png`、`doc/governance/worklog/issue-23.md`。 |
| Audit 種類 | **R1**（accepted work scope 的完整 independent audit），**cycle 1**。Ticket audit，不是 Spec Integration Audit（Bindings §5 不採用單 Ticket fast path）。 |
| 角色 | `primary_reviewer`（definition `gov-primary-reviewer`；Bindings §3.1 mapping `claude-opus-5-5`／`xhigh`） |
| Binding 證據 | 由派工者（Orchestrator）依 Bindings §3.4 核對，記在 run record `home_work_01/doc/governance/run/run-20260924-hw01-formal.md`。該 run record 記載的 Executor binding：agent `abac86af43a37ad61` = `gov-executor`／`claude-opus-4-8`／`high`。Executor 與 Primary Reviewer 的 mapping 為不同模型，沒有 `diversity_lost`。 |
| Independence（治理 §2.3） | (1) fresh context 派工，未繼承 Executor 的對話；worklog 與 run record 的敘述一律當作待驗證主張（worklog R-EN-1 第 4 列的 PASS 主張被本 audit 推翻，見 F-1）。(2) Binding 見上一列。(3) 自主取得：Reviewer 自讀 Ticket 本文（`gh issue view 23`）、Spec、Outcome Contract AB-15、derivation record、DR-1、H-2／A-1、unattended-run policy、#20 R1 audit 的 AC-10 判定、git 歷史與 diff、CI run 與 log，並自己啟動本機 server、以 headless Chrome（CDP）在多種寬度與狀態下渲染與量測，另對 live preview 渲染。Reviewer 的腳本全部自寫，放在 scratchpad 的 `pr23r1/`，未使用 scratchpad 中其他 session 的腳本。(4) 本紀錄由 Reviewer 以自己的 Write 工具寫入。 |
| 日期 | 2026-09-24（本機 +08:00 約 07:00–07:25） |

## 1. 審查方法與環境

- **確認 subject**：`git rev-parse HEAD` = `git ls-remote origin home_work_01-hw10-implementation` = `84722c1…`。`git diff --stat 610a797..84722c1` 只有 worklog。`git diff --stat 610a797 -- home_work_01/static home_work_01/server.py home_work_01/weather_query.py home_work_01/app.py home_work_01/data.db home_work_01/api` 為空，工作樹的實作與 subject 相同。`git status --porcelain` 只列 Orchestrator 修改中的 run record（record-only）。`git diff --check 39fbab7..84722c1` 乾淨。兩個 commit message 符合 `[Modify] – …` 規則，沒有 Claude 標記。
- **產品範圍**：`git diff --name-status 39fbab7..610a797` 只有 `static/` 三檔（M）與截圖、worklog（A）；`app.py`、`server.py`、`weather_query.py`、`data.db`、`requirements.txt`、`tests/` 皆不在 diff；diff 全在 `home_work_01/` 內。
- **測試**：Reviewer 以 Python 3.12.14 venv（flask 3.1.2、streamlit 1.64.0，與 `requirements.txt` 釘選相同）在 `home_work_01/` 執行 `python -m pytest -q -p no:cacheprovider` → **152 passed**；`tests/test_app.py tests/test_dashboard.py tests/test_static_checks.py -v` → 54 passed（逐項列出見 §2）。
- **瀏覽器**：Reviewer 自寫 `servers.py` 以 `server.create_app(...)` 在 127.0.0.1 啟五個 server：5111 正常 `data.db`；5112 不存在的 DB；5113 只有表無列的 DB；5114 `data.db` 複本刪一列（41 列，incomplete）；5115 每個 `/api/` 請求延遲 8 秒（loading）。替代 DB 全在 scratchpad。自寫 CDP client（`cdp.py`，Chrome headless=new）做 `Emulation.setDeviceMetricsOverride`（1280×900、1024×768 desktop；375×812 mobile＋touch emulation）、`Network.setBlockedURLs`（error 狀態、per-Region 網路失敗）、`Fetch.fulfillRequest`（per-Region 404／503）、`Input.dispatchMouseEvent`／`dispatchTouchEvent`（hover／tap）、`Emulation.setEmulatedMedia`（dark mode）。量測以 `document.documentElement.scrollWidth`、`getBoundingClientRect` 與 `getComputedStyle` 取得。
- **Live**：`https://aiot-hw01-weather-git-homework01-hw10-im-8efc12-nchu-aiot-class.vercel.app/` `GET /` 200；其 `/static/app.js` md5 `88c89f76…` = `git show 610a797:home_work_01/static/app.js | md5sum`，即 preview 部署的是本 subject 的前端。Production alias 回 404（尚未合併進 `main`，RB-1，非本票條件）。
- **CI**：`gh run view 35930941816`（push，headSha `610a797…`，`home_work_01 CI`，conclusion success；job「offline test suite + credential checks (Python 3.12)」全部 step success）；log：`Python 3.12.14`、`152 passed in 3.89s`、`credential scan passed: 474 tracked files …`。`gh run list --commit 610a797…`：push `35930941816`、pull_request `35930943558` 皆 success；`--commit 84722c1…`：`35931051216`、`35931050377`（push）、`35931052515`（pull_request）皆 success。
- 結束時已停止 Reviewer 自己啟動的 server（PID 14696）與 Chrome；`git status` 與開始時相同（本紀錄檔除外）。

## 2. 需求、AC 與 invariants 逐條判定

| 項目 | 判定 | 證據 |
| --- | --- | --- |
| **R-EN-1 (1)** 視覺層級 | **PASS** | 1280／1024／375 渲染：masthead（eyebrow `Taiwan Weather Dashboard`、`<h1>`、lead）→ controls card（`Select Region`、`Select Date` 保留位、ingestion 時間）→ Weekly summary 兩張 stat tile → chart card（標題 `Temperature Forecast – <Region>`）與 table card → Taiwan Map 保留卡片。各區塊可辨、主次分明（`index.html:16-139`）。 |
| **R-EN-1 (2)** 響應式（≥1024 px 與 375 px 皆可完整操作） | **FAIL（375 px 的圖表互動，F-1）**；版面本身 PASS | 版面：≥900 px 為 chart／table 兩欄（`styles.css` `.grid` media query），1024 與 1280 皆正常；375 px 單欄堆疊、`select` 100% 寬、所有內容可達，越出視窗的元素 0 個。但 375 px 下圖表的 hover／tap tooltip 的 Date 與 MaxT 幾乎全部被裁切（42 個 Region×日期中 41 個的 Date 列被遮、29 個一半以上被遮），圖表互動在該寬度無法實際使用，見 F-1。 |
| **R-EN-1 (3)** 摘要資訊 | **PASS** | 六個 Region 逐一切換（1280 與 375），Reviewer 用共用模組 `wq.region_series` 在 Python 獨立算出最低 MinT／最高 MaxT 與日期，六區全部等於畫面上的 stat tile（例：北部地區 23.3 on 2026-09-24／32.4 on 2026-09-28；中部地區 24.3 on 2026-09-30／33 on 2026-09-26）。前端只做 min／max 聚合（`app.js:177-193`），資料只來自 `/api/regions/<r>/series`。 |
| **R-EN-1 (4)** 圖表可互動且易讀（圖例、軸標籤、hover／tooltip 顯示數值） | **FAIL（F-1）** | 圖例 `MaxT`／`MinT` 與軸標籤 `Temperature (°C)`／`Date`、刻度皆存在。Tooltip 內容正確（Date、MaxT、MinT），但被 chart 容器裁切，多數日期的 Date 與 MaxT 看不到，見 F-1。375 px 的軸標籤另有可讀性問題（F-3，non-blocking）。 |
| **R-EN-1 (5)** loading／empty／error 各自可見 | **PASS**（狀態對應的語義問題見 F-2／RS-1） | loading：5115，1280 與 375 皆見藍色 spinner 橫幅「Loading the latest forecast…」（role=status）。empty：5113 顯示「No forecast data yet」＋ reason（role=status）。error：5111 並封鎖 `*/api/*` → 紅色「Something went wrong / Cannot reach the forecast service…」（role=alert）。per-Region：封鎖 series 或回 404／503 時，chart card 內顯示 inline 訊息（「Cannot load this Region right now…」「That Region is not available in this snapshot.」「The forecast snapshot is incomplete.」），summary 隱藏、表格清空，不是空白。沒有 JS 例外（CDP `Runtime.exceptionThrown` 0 筆）。 |
| **R-EN-1 (6)** 375 px 無不必要橫向捲動 | **PASS** | 375×812 mobile：`scrollWidth` **375**、`clientWidth` 375、`innerWidth` 375。另把 `body{overflow-x:hidden}`（`styles.css:78`）以注入樣式取消後再量：`scrollWidth` 仍 375、越出視窗的元素 0 個，即沒有被 `overflow-x:hidden` 遮住的溢出。Dark mode 375：375。Live preview 375：375。1024：1024；1280：1280。例外：hover 最後一個日期時，chart 容器內部出現橫向捲動（容器 scrollWidth 359＞311），屬 F-1 的同一成因。 |
| **AC-19** | **FAIL**（R-EN-1 第 4 項，及第 2 項的 375 px 圖表互動；F-1） | AC-19 FAIL 條件「任一項 FAIL」。量測值：375 px `scrollWidth` 375 ≤ 375（與 worklog 記錄的值相同）。截圖要求：桌機、375、loading／empty／error 各一張皆已提交且為真實畫面（§5）；但 hover 截圖本身顯示了 F-1 的裁切。 |
| **R-EN-2** 概念詞 | **PASS** | 見 §3（H-2）。 |
| **R-EN-7**（版面整合部分） | **PASS** | 圖表、表格、摘要與控制項在同一頁整合。`Select Date`（`index.html:61-69`）與 Taiwan Map（`index.html:127-138`）只有標籤與「Coming soon」：保留控制項內沒有 `select`／`input`／`button`（DOM 查詢 0 個），map card 內沒有互動元素或 `.leaflet-container`（0 個）；`static/` 沒有 Leaflet 或任何外部 URL。完整整合屬 #24。 |
| **R-DS-6** | **PASS** | 503／404／網路失敗皆顯示明確訊息（R-EN-1 (5) 列）。 |
| **AC-02（Dashboard）** | **PASS** | `test_index_returns_page_with_title`、`test_index_page_has_visible_teacher_text`、`test_regions_normal` PASS。渲染 DOM：`<h1>` `Taiwan Weather Forecast`、`<label>` `Select Region`，`<option>` 依序為 北部地區、中部地區、南部地區、東北部地區、東部地區、東南部地區（R-SHR-2(b)）；1280、375、live 皆同。 |
| **AC-03（Dashboard）** | **PASS**（新版面截圖缺，F-4） | `test_region_series_normal`（六區）、`test_inv2_series_equals_shared_module_for_all_regions` PASS。渲染 DOM：六區（含中部地區、東南部地區）各 7 列、欄 `Date`／`MinT`／`MaxT`、升序，逐列等於 `/api/…/series`；`/api/` 序列等於 `wq.region_series`；兩條 polyline 各 7 點、14 個 dot。 |
| **AC-04(b)** | **PASS** | `test_frontend_has_no_cwa_url_or_key`、`test_frontend_makes_no_external_absolute_url_requests`、`test_frontend_requests_use_the_api_prefix` PASS。Reviewer grep：`static/` 內 `opendata`／`cwa.gov`／`CWA_API_KEY`／`Authorization` 0 筆；唯一絕對 URL 為 `app.js:477` 的 SVG namespace；請求只有 `fetchJson("/api/health")`、`fetchJson("/api/regions")`、`fetchJson("/api/regions/"+…+"/series")`（`app.js:91,109,151`）經 `fetch`（`app.js:422`）；沒有 XHR／WebSocket／EventSource／`url()`；HTML 只載入 `/static/styles.css` 與 `/static/app.js`。 |
| **AC-10（Dashboard）** | **API PASS；頁面：明確訊息可見 PASS；「錯誤狀態」的呈現分類有契約歧義 → F-2／RS-1** | `test_health_missing_is_503`、`…empty…`、`…incomplete…`、`…mismatched_dates…`、四個資料 endpoint 的 503 測試 PASS。渲染：missing／empty／incomplete 三種都顯示 empty 呈現「No forecast data yet」＋對應 reason 文字，不是空白頁、沒有例外、health 回 503。#23 之前這三種顯示紅色 error banner（role=alert），`ac10_dashboard_error_missing_db.png` 與 #20 R1 audit 的 AC-10 判定都以此為據。 |
| **AC-26／INV-9** | **PASS** | `app.py` 不在 diff；`tests/test_app.py` 9 項（`AppTest`）PASS；`test_app_side_imports_no_folium`、`test_app_side_uses_no_select_date_or_folium_in_code`、`test_requirements_does_not_list_folium` PASS。ENHANCED 只加在 `static/`（Dashboard 前端）。 |
| **INV-2** | **PASS** | 表格與圖表內容：見 AC-03 列（六區、兩種寬度、live 皆為 7 列且等於共用模組）。Dashboard 的 MVM 行為（標題、`Select Region`、雙線 7 點圖、7 列表、ingestion 時間、狀態訊息）都還在，沒有比 Grading App 弱。 |
| **INV-6** | **PASS** | 見 AC-04(b)。 |
| **CI 綠** | **PASS** | 見 §1 CI。 |
| **AC-27（本票範圍，R-DOC-5 四項）** | **PASS** | (1) 說明：`app.js:1-18` 檔頭說明資料來源、三種狀態與 INV-2／AC-04(b)；各段落有註解（`app.js:58,87,140,174,212,360,419`）；`styles.css:1-12` 檔頭；`index.html` 各區塊註解。(2) 錯誤處理：見 R-DS-6。(3) 死碼／未用相依：27 個函式全部被呼叫；`els` 的 19 個鍵全部被使用；沒有新增相依；只有 `chartState.H` 被存但未讀（trivial，不列 finding）；#20 的 `showPageError`／`hidePageError` 已移除且無殘留引用。(4) 結構：health → regions → series → summary／chart／table，與資料流一致。 |

## 3. H-2 核對（decision A-1）

- **觸及的類別**：H-2（老師指定的介面或資料格式；本票觸及頁面文字）。
- **核對了什麼**：
  1. 頁面概念詞：在 1280、1024、375（light 與 dark）與 live preview 的渲染 DOM 讀取 `document.title` = `Taiwan Weather Forecast`；`<h1>` = `Taiwan Weather Forecast`（`index.html:17`）；`label[for=region-select]` = `Select Region`（`index.html:57`）；表頭 `<th>` = `Date`、`MinT`、`MaxT`（`index.html:119`）；圖例 = `MaxT`、`MinT`；X 軸標題 = `Date`；dot `<title>` 與 tooltip 使用 `MaxT`／`MinT`。`Select Date` 以保留位標籤出現（R-EN-2、Spec §4.1「文字」）。整合名稱 `Taiwan Weather Dashboard` 只作 eyebrow，未取代 `<h1>`。`test_index_page_has_visible_teacher_text` 對靜態 HTML 守住 `<h1>`、label 與三個表頭。
  2. 中文 Region 名：選項由 `/api/regions` 資料驅動，逐字為六個含「地區」的全名，順序符合 R-SHR-2(b)；圖表標題與 summary 亦用同一字串。
  3. 其他 H-2 項目：`git diff --name-status 39fbab7..84722c1` 不含 `app.py`、`data.db`、`requirements.txt`、`README.md`、`weather_query.py`，故 `streamlit run app.py`、`TemperatureForecasts` DDL 與五欄、`dataDate` 格式與老師驗證 SQL 的結果都未被觸及。
- **結果**：**PASS**。沒有概念詞被改名、刪除或被 ENHANCED 文字取代。

## 4. Findings

### F-1：圖表 tooltip 被 chart 容器裁切，Date 與 MaxT 在多數日期看不到（R-EN-1 第 4 項、第 2 項的 375 px 圖表互動；AC-19）

- **Severity**：High　**Blocking**：是
- **契約依據**：Spec R-EN-1「UI／UX 品質清單（全部 MUST PASS）… (2) 響應式——桌機（≥ 1024 px）與 375 px 寬皆可完整操作；… (4) 圖表可互動且易讀——有圖例、軸標籤、hover／tooltip 顯示數值」（`SPEC.md:200`）；AC-19 PASS「R-EN-1 六項各自 PASS」、FAIL「任一項 FAIL」（`SPEC.md:270`）；Outcome Contract AB-15「可互動易讀的圖表」（`outcome-contract.md:83`）。
- **證據**：
  - 成因：`styles.css:296` `.chart__canvas { position: relative; width: 100%; overflow-x: auto; }`。依 CSS 規則，overflow-x 不是 visible 時 overflow-y 也計算為 auto；Reviewer 以 `getComputedStyle` 量得 `auto/auto`。Tooltip 是該容器內的絕對定位元素，`app.js:387-391` 把它放在 `top = yAt(maxt)·scale`，再以 `styles.css:313` `transform: translate(-50%, -110%)` 往上移動自身高度的 110%。Y 軸上限為 `ceil(max + 15% 範圍)`（`app.js:230-234`），所以 MaxT 點永遠靠近容器上緣，tooltip 超出上緣的部分被裁掉。第一個日期向左、最後一個日期向右超出，也被裁切或造成容器內的橫向捲動。
  - 量測（tooltip 高 71.2 px，三列依序為 Date、MaxT、MinT；hover 在各日期的 dot 所在 x）：
    - **375 px**（六區 × 七日 = 42）：42 個全部上緣被裁，裁掉 14.5–55.8 px；Date 列被遮（裁 ≥ 18 px）41 個；一半以上被遮 29 個。首日左側另裁 30.8–36.1 px，末日右側另裁 42.8–48.1 px。
    - **1280 px**：上緣被裁 28／42，Date 列被遮 19／42（每一區的週最高點都在其中，例：北部地區 09-28 裁 36.1 px、南部地區 09-26～09-28 各裁 34.6 px）；有任一方向裁切 37／42；首日左側裁 13.3–18.6 px；末日右側裁 36.4–42.8 px，且 chart 容器 scrollWidth 625＞584（出現容器內橫向捲動）。1024 px 的情況相同（北部地區 09-28 裁 40.3 px）。
  - **Touch**：375 px mobile emulation 下實際 tap 09-27（`Input.dispatchTouchEvent`）→ tooltip 出現，但只看得到「MinT 24.1°C」，Date 與 MaxT 被裁（裁 48.5／71.2 px；Reviewer 截圖 `pr23r1/out/m375-tap-3.png`）。
  - **Live preview** 重現：北部地區 09-28 hover，1280 px 裁 36.1／71.2 px，375 px 裁 55.8／71.2 px。
  - 沒有替代的數值顯示：dot 上原生 `<title>` 的 fallback（`app.js:303`）被後加的全高透明 `rect.chart__hit`（`app.js:315-328`）蓋住；`document.elementFromPoint` 在 dot 中心回傳 `rect.chart__hit`，只有剛好落在右邊界的末日 dot 例外。
  - **提交的證據與主張不符**：`doc/acceptance/screenshots/issue-23-desktop-chart-hover.png` 的 tooltip 看不到 Date 列，「MaxT 32.4°C」也被切掉上半，只有「MinT 24.4°C」完整。但 worklog R-EN-1 第 4 列以這張圖為據，記為 PASS（「09-28：MaxT 32.4°C／MinT 24.4°C」）。
- **R2 的 closure 證據要求**：六區七日在 1280（或 ≥1024）與 375 px 下，tooltip 的 Date、MaxT、MinT 三列都完整可見，並附量測（tooltip 的矩形落在可見的裁切範圍內，首末日也要）；375 px 的 `document.documentElement.scrollWidth` 仍 ≤ 375；兩種寬度各重拍 hover 截圖，並附 375 px 的 tap 截圖。修法屬 Executor 的 HOW（DR-1），本紀錄不指定。

### F-2：AC-10 的不可用快照改用 empty 呈現；「錯誤狀態」如何對應 R-EN-1 的 empty／error 有契約歧義

- **Severity**：Medium　**Blocking**：否（契約語義不足；routing signal RS-1 → Design Authority，治理 §4.2、unattended-run policy N-16／N-27）
- **契約依據**：AC-10「指向不存在的資料庫路徑：… `GET /` 頁面顯示錯誤狀態。指向只有表無列的資料庫：同上（原因 empty）」，證據「瀏覽器截圖（error 狀態）」（`SPEC.md:261`）；DR-9（incomplete →「頁面顯示錯誤狀態」）；R-EN-1 (5)「loading、empty、error 三種狀態各自有可見呈現」（`SPEC.md:200`），但沒有定義哪些條件屬 empty、哪些屬 error。
- **證據**：`app.js:93-96` 與 `:110-112` 對**任何**非 2xx 的 `/api/health`、`/api/regions` 都呼叫 `showEmpty(...)`，呈現為「No forecast data yet」、中性配色、`role="status"`（`index.html:42`）；error 呈現（紅色、`role="alert"`，`index.html:25`）只用於網路失敗或例外（`app.js:101-105`）。`app.js:94` 的註解寫「503: … -> empty state」，但程式對 500／502／504（例如 Vercel function 錯誤或逾時）也走 empty。Reviewer 渲染 missing、empty、incomplete 三種 DB，都顯示「No forecast data yet」加對應 reason。#23 之前三者都是紅色 error banner（`39fbab7` 的 `showPageError`）；`ac10_dashboard_error_missing_db.png` 與 `issue-20-c1-r1.md` 的 AC-10 列都以 error banner 為 PASS 依據，這張證據截圖現在已與實際行為不符。
- **影響**：訊息仍然明確，AC-10 列出的 FAIL 例（例外堆疊、空白頁、health 回 200）都沒有發生，R-DS-6 也成立。但若依 AC-10 字面，頁面在 AC-10 的三種條件下已不再顯示「錯誤狀態」；「No forecast data yet」對 incomplete 快照（其實有資料）與 5xx 伺服器錯誤也不準確。
- **Disposition**：交 Design Authority 判定（RS-1）。DA 若判定 AC-10 要求 error 呈現，本項即成為契約回歸，須由 Executor 修正（可在 F-1 的 targeted correction 中一併處理，由 DA 決定）。DA 若判定 empty 呈現加 reason 即符合，則不需修改；AC-10 的截圖證據改由 #25 在重驗 AC-10 時重拍（`derivation-SPEC.md:165`）。Owner：Orchestrator 派 DA。

### F-3：375 px 下圖表文字隨 viewBox 縮小，約 4.8 px，難以閱讀

- **Severity**：Medium　**Blocking**：否
- **契約依據**：R-EN-1 (4)「易讀」、(2)「375 px 寬皆可完整操作」。R-EN-1 (4) 列舉的元件（圖例、軸標籤、tooltip 數值）都存在，本項是可讀性品質的風險，不是元件缺漏，故不列 blocking。
- **證據**：SVG viewBox 寬 720（`app.js:215`），375 px 下實際寬 311 px，縮放 0.43。刻度字 `font-size: 11px`（`styles.css:306`）實際約 **4.75 px**，軸標題 12 px（`:307`）約 **5.2 px**，dot 半徑約 1.5 px；1024 px 時刻度約 7.9 px，1280 px 時約 8.9 px。提交的 `issue-23-mobile-375-ok.png` 可以看到刻度幾乎無法閱讀。這在 #20 已存在（相同字級、相同 viewBox），但 #23 是負責 R-EN-1 在 375 px 成立的票。
- **Disposition**：與 F-1 是同一個圖表元件、同一項需求，Executor 可以在 F-1 的 targeted correction 中一併處理。若未處理，由 Orchestrator 帶到 #24 的 AC-19 重驗（Ticket #23「Cross-ticket invariants」段、`derivation-SPEC.md:164`）。

### F-4：沒有以新版面重拍 AC-02／AC-03（Dashboard）截圖

- **Severity**：Low　**Blocking**：否
- **契約依據**：Ticket #23 AC 清單「INV-2：AC-02、AC-03（Dashboard）的 Flask test client 與截圖驗證在改版後仍 PASS」；AC-03「以中部地區與東南部地區各驗一次」（`SPEC.md:254`）。
- **證據**：worklog 的 INV-2 段只引用 pytest。`issue-23-*` 截圖只有北部地區。既有的 `ac02_dashboard_default.png`、`ac03_dashboard_central.png`、`ac03_dashboard_southeast.png` 都是 #23 之前的版面。Reviewer 已在新版面的渲染 DOM 獨立驗證六區內容（§2 AC-03 列），所以行為是 PASS，缺的只是證據紀錄。
- **Disposition**：Executor 在 F-1 修正後重拍截圖時，一併補拍中部地區與東南部地區；若未補，由 #25 在 `doc/acceptance/` 重驗 AC-02／03 時補（R-DOC-4）。

### F-5：無障礙與狀態辨識的小退步

- **Severity**：Low　**Blocking**：否
- **證據**：(a) `index.html:10` 把 `39fbab7` 的 `<main class="page">` 改成 `<div class="page">`，頁面失去 `main` landmark。(b) per-Region 的錯誤訊息（404／503／網路失敗）與「Loading <Region>…」共用 `.state--inline` 的藍色 info 樣式（`index.html:100`、`styles.css:170`），畫面上錯誤與載入中不易區分。頁面層級的三種狀態仍然彼此不同，所以不影響 R-EN-1 (5)。
- **Disposition**：契約沒有要求；是否順手修正由 Executor 決定，不需要追蹤。

## 5. 提交截圖的真實性

- `issue-23-desktop-ok.png`（1280×1226）：與 Reviewer 在 5111、1280 px 獨立渲染的 full-page 截圖**逐位元組相同**（md5 `4af72a6d2e688d5aa2a67de73f55b203`）。
- `issue-23-empty.png`、`issue-23-error.png`（1280×760）：與 Reviewer 以空表 DB、封鎖 `/api/` 渲染的截圖逐位元組相同（md5 `e1bd11f9…`、`fa1234ae…`）。
- `issue-23-loading.png`：md5 與 Reviewer 的不同，但畫面相同，差別只在 spinner 的動畫格。
- `issue-23-mobile-375-ok.png`（375×1734，DSF 1）：與 Reviewer 的 375 px 渲染（DSF 2）版面、文字與數值一致。
- `issue-23-desktop-chart-hover.png`：是真實畫面，但它記錄的正是 F-1 的裁切，不支持 worklog 的 PASS 主張。

## 6. 結論

- 通過：R-EN-1 第 1、3、5、6 項；R-EN-2／H-2；R-EN-7（本票部分）；R-DS-6；AC-02、AC-03、AC-04(b)（Dashboard）；AC-26／INV-9；INV-2；INV-6；CI；AC-27（本票範圍）。
- 未通過：R-EN-1 第 4 項，以及第 2 項在 375 px 的圖表互動，因此 **AC-19 FAIL**（F-1，blocking）。
- Routing：RS-1（F-2）交 **Design Authority**，由其判定 AC-10「頁面顯示錯誤狀態」與 R-EN-1 (5) empty／error 呈現的對應。這是契約語義問題，不是本 audit 的 blocking 依據。
- Non-blocking 的 disposition：F-3（隨 F-1 修正或帶到 #24）、F-4（隨 F-1 重拍或由 #25 補）、F-5（Executor 自行決定）。
- R2 的範圍：只核對 F-1 是否解決（§4 F-1 的 closure 證據要求），以及修正有沒有造成回歸（R-EN-1 其他各項、375 px `scrollWidth`、H-2 概念詞、INV-2 內容、AC-04(b)、全套 pytest 與 CI）。若 DA 就 RS-1 判定需要修正，該修正的核對依 DA 的裁決納入。

VERDICT: BLOCKING (F-1)
