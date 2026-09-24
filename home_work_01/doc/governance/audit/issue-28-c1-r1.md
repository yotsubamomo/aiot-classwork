# Audit record — Issue #28，cycle 1，R1（A-4 independent audit）

| 欄位 | 內容 |
| --- | --- |
| Work Contract | GitHub Issue **#28**（`yotsubamomo/aiot-classwork`）「Taiwan Map 視覺重做（post-baseline enhancement）」。本 work item 的 Outcome Contract＝acceptor 2026-09-24 直接指示（核定文逐字見 DR-20 §0；Bindings §2.3 末項、§4 第 3 列）。Governing decision：**DR-20** `doc/governance/decisions/decision-20260924-taiwan-map-rework.md`（lane＝Lightweight；boundary B-1..B-16／X-1..X-8；提案 HOW P-1..P-13 與其條件；§3.5(A) 整合重驗範圍；§3.6 驗收語義）。不變契約：Spec v1.1 R-EN-1..R-EN-7、R-SHR-4、R-SEC-1..3、INV-1/2/5/6/7/9、AC-04(b)、AC-14(6)、AC-17/18/19/20/21/27/28；DR-1、DR-4、DR-19；`decision-20260923-high-risk-categories.md` H-2、H-3、A-1、A-4。 |
| 受審 subject | branch `home_work_01-hw10-implementation`；實作 subject **`b4549e50862560eb90d3e0c370be94897c9b6ead`**；HEAD `6b906a4`（＝`git ls-remote origin`；`git diff --stat b4549e5..6b906a4` 只有 `doc/governance/worklog/20260924-taiwan-map-rework.md`，record-only，Bindings §7）。本 work item BASE `d23de58`；accepted baseline `720c0a0`。審查範圍 `git diff 720c0a0..b4549e5`（26 檔；排除 `doc/governance/**` 後為 `static/{app.js,index.html,styles.css}`（M）、`static/data/basemap.js`（A）、`tests/test_map_frontend.py`（A）、`tests/test_static_checks.py`（M）、`README.md`、`doc/acceptance/ACCEPTANCE.md`、12 張 `doc/acceptance/screenshots/issue-28-*.png`、`doc/ticket/tickets.md`）。 |
| Audit 種類 | **R1**（A-4 必做的 independent audit；DR-20.1），**cycle 1**。依 DR-20 §3.5(A) 本 R1 涵蓋 DA 指定的整合重驗範圍；本紀錄**不是** Spec Integration Audit，也不得被引用為 Spec Integration Audit（DR-20 §3.5 末段）。 |
| 角色 | `primary_reviewer`（definition `gov-primary-reviewer`；Bindings §3.1 mapping `claude-opus-5-5`／`xhigh`） |
| Binding 證據 | 由派工者（Orchestrator）依 Bindings §3.4 核對並記入 run record `home_work_01/doc/governance/run/run-20260924-hw01-formal.md`（本次 #28 A-4 dispatch；Executor `a37f68bb30f67b595` = `gov-executor`／opus-4-8／high，依派工內容）。Executor 與 Reviewer 為不同模型 mapping，沒有 `diversity_lost`。 |
| Independence（治理 §2.3） | (1) fresh context，未繼承 Executor 對話；worklog、ACCEPTANCE.md、tickets.md 與 commit message 的敘述一律當作待驗證主張（worklog 的 V-3、V-4 PASS 主張與 ACCEPTANCE §6「F-5(a) RESOLVED — all six tooltips fully visible at 375 & desktop」被本 audit 部分推翻，見 F-2、F-4）。(2) Binding 見上一列。(3) 自主取得：自讀 Issue #28（`gh issue view 28`）、DR-20、Spec、H-2／H-3／A-1／A-4、#24 R1／R2 紀錄、git 歷史與 diff、CI log、GitHub deployment API；自己以 `git archive` 匯出 subject 與 baseline、啟動本機 server、以自寫 Playwright-core（驅動本機 Chrome 153 headless）渲染、互動、量測、攔截回應並記錄 network log；自己做 mutation test。腳本與輸出在 Reviewer scratchpad 的 `pw/`（`audit.js`、`sweep.js`、`shots.js`、`behave.js`、`statemsg.js`、`v4detail.js`、`v4click.js`、`zoom.js`、`base768.js`；輸出 `pw/out/`）。(4) 本紀錄由 Reviewer 以自己的 Write 工具寫入。 |
| 日期 | 2026-09-24 |

## 1. 審查方法與環境

- **Subject 確認**：`git rev-parse HEAD` = `6b906a4…` = remote；`git status --short` 空（開始與結束相同，本紀錄檔除外）。`git diff --check 720c0a0..b4549e5`（排除 generated `basemap.js`）乾淨。commit message `[Modify] – …`＋`[Additions]/[Modification]/[Fix]`，無 Claude 標記。
- **乾淨環境**：`git archive b4549e5 home_work_01` 匯出到 scratchpad（無 `.env`、無 `.venv`）；以 repo 的 Python 3.12.14 venv 執行，`CWA_API_KEY` unset、`HTTP(S)_PROXY=http://127.0.0.1:9`（任何網路請求都會失敗）。同法匯出 baseline `720c0a0` 供對照。
- **本機 server**：subject `server.app` @ `127.0.0.1:5077`；baseline @ `127.0.0.1:5078`（只作 regression 對照）。
- **瀏覽器**：Playwright-core 1.63.0 + `C:/Program Files/Google/Chrome/Application/chrome.exe`（headless）。viewport：1920／1440／1366／1280／1180／1100／1024（desktop）、1023／960／900／880／834／820／800／768／700／641（tablet，地圖 440 高）、640／600／560／480／414／390／375／360／320（phone，地圖 360 高）；`colorScheme` light／dark。量測以 `getBoundingClientRect`、`elementFromPoint`、`getComputedStyle`、Range client rects、`page.route` 攔截（503／500／404／network abort／2xx 空值／2xx 非 JSON／延遲）。
- **Preview**：GitHub deployment API `deployments?sha=b4549e5` → `6631043843`（Preview，success）→ `https://aiot-hw01-weather-me27n9baf-nchu-aiot-class.vercel.app`。
- 結束時停止 Reviewer 自己啟動的兩個 server 與瀏覽器。

## 2. DR-20 §3.5(A) 必要範圍逐項結論

### 2.1 Diff-scope／boundary（§3.5(A)-1）— **HOLDS**（另有 RS-2）

- `git diff --name-only 720c0a0..b4549e5 | grep -vE "^home_work_01/(static/|tests/|README.md$|doc/acceptance/|doc/ticket/tickets.md$|doc/governance/)"` → **0 筆**。`app.py`、`server.py`、`weather_query.py`、`ingestion/`、`api/`、`data.db`、`data/`、`requirements.txt`、`vercel.json`、`.python-version`、`.github/workflows/`、`static/vendor/` 皆不在 diff（X-2、X-6 未觸及）。`tests/**` 只有新增檔與 `test_static_checks.py` 的加強（collect 由 152 → 163，`diff` 兩邊的 test id 只多 11 個、沒有刪除或改名）。
- X-1（外部請求）：network log 零外部（§2.6）；X-3：masthead／controls／Weekly summary／折線圖／表格的 CSS 與 JS 邏輯未改（`renderSummary`／`renderTable`／`showTooltip`／`loadRegion`／`formatTemp` 與 baseline 逐字相同，`renderChart`／`fetchJson` 只有註解差異），controls card 只移出 `Select Date`；**唯一例外**是 masthead 導言一句文案改寫（`index.html:22-26`），列為 RS-2 交 DA。X-4、X-5、X-7、X-8：未觸及（無新資料功能；Spec／OC／Bindings 未改；無合併、無 Vercel 設定；worklog 與 `basemap.js` 檔頭記載兩資料源取得免帳號免付費）。
- DR-20 §3.5 fail-safe：diff-scope 證明成立，本 R1 沒有提出 DA 無法關閉的 boundary finding（RS-2 屬可由 DA 直接判定的文案問題），所以目前不觸發補充 Spec Integration Audit；此判定由 Orchestrator 依 DA 對 RS-2 的回覆機械套用。

### 2.2 Invariants（§3.5(A)-2）

| INV | 判定 | 證據 |
| --- | --- | --- |
| INV-1 | **HOLDS** | 瀏覽器端資料請求只有 `/api/health`、`/api/regions`、`/api/regions/<r>/series`、`/api/days`、`/api/days/<date>`（network log）。`git grep -nE "mint\s*\+\s*maxt|[<>]=?\s*(20|25|30)\b" b4549e5 -- home_work_01/static/app.js` → 0 筆。面板兩張 tile 只對 endpoint 六筆取 max／min（`app.js:405-413`，P-9 允許）。 |
| INV-2 | **HOLDS** | `test_inv2_series_equals_shared_module_for_all_regions` PASS；折線圖／表格程式與 baseline 逐字相同（見 2.1）；全頁截圖的表格值與 `/api/regions/北部地區/series` 相同。 |
| INV-5 | **HOLDS** | `git diff 720c0a0..6b906a4` 無 CWA key 格式字串；`git ls-files home_work_01` 不含 `.env`；`static/data/basemap.js` 無 URL、無 key；CI credential scan：`credential scan passed: 530 tracked files; no .env tracked …`（run `35960925910`）。 |
| INV-6 | **HOLDS** | 每個 context 的全部 request origin 只有 `http://127.0.0.1:5077`（desktop-dark 18 筆含 7 次切日；其餘 context 各 11 筆）；外部請求 0。唯一 console error 是瀏覽器自動請求的同源 `/favicon.ico` 404。 |
| INV-7 | **HOLDS** | `DERIVED` chip、來源句 `Source: CWA F-D0047-091 (county-level) → project-derived six-region values`（`index.html:93-95`，符合 P-8 措辭條件、AC-14(8)）、所選 Region 區塊 `(derived, not an observed daily mean)`、tooltip `(derived)`、圖例 R-EN-5 原句、README:295-296。 |
| INV-9 | **HOLDS** | `app.py` 不在 diff；`test_app.py`（AppTest）與 AC-26 靜態檢查 PASS；ENHANCED 只在 Dashboard。 |
| INV-3／INV-4／INV-8 | diff 未觸及 | 沿用 `spec-SPEC-c1-r1.md` 的結論（DR-20 §3.5(A)-2）。 |

### 2.3 Spec AC 重驗（§3.5(A)-3）

| AC | 判定 | 證據 |
| --- | --- | --- |
| AC-04(b) | **PASS** | `_static_files()` 改為 `rglob`（`test_static_checks.py:206-214`），三個前端檢查的斷言語義不變；`_ALLOWED_FRONTEND_URLS` 新增的三個字串皆為非請求常數：`https://leafletjs.com`（`leaflet.js` 檔頭註解與 attribution prefix 的 href，且 `app.js:560` 已 `setPrefix(false)`）、兩個 bug-tracker URL（`leaflet.css:64`、`:102` 的 CSS 註解）；沒有任何請求目標被放行（DR-20 P-3、§3.4）。`test_frontend_requests_use_the_api_prefix` PASS。 |
| AC-14(6) | **PASS** | README:295-296 導出說明維持；README:259-293 新增底圖來源、授權、免金鑰、代表點（含微調座標）與 `Select Date` 位置。 |
| AC-17 | **desktop PASS；tablet 寬度下六標記可見性 FAIL（F-1）** | 1280／1024（light、dark）：六個 pill 全在容器內、無互相重疊、未被面板／圖例遮；zoom 控制可用（zoom-in 後 map pane 位移、`map--labels-hidden` 依 zoom 切換）；每個 pill 的 class／底色＝endpoint `colourBand`（見 2.5 H-3）；hover tooltip 與點擊後面板皆有 Region／`Date`／`Min`／`Max`／導出值；圖例四段＋「derived」註記；底圖 vendored 免金鑰。**641–880 px**：浮動面板蓋住 1–5 個 pill 且 pointer 無法觸及（F-1）。 |
| AC-18 | **PASS** | `Select Date` 7 個 option `2026-09-24…2026-09-30` 升序、預設第一天（每個 viewport 相同）。七天逐一切換（1280 dark、375 light）：六 pill 文字／class／aria-label、tile、所選 Region 區塊與 endpoint 0 筆不符；map pane transform 七次切換都不變（不重設視野）。 |
| AC-19 | **PASS（R-EN-1 六項於 1280 與 375 成立；另見 F-2、F-3、F-4 的 V 判準／可讀性問題）** | 375：`scrollWidth == innerWidth == 375`（320–640 全部無橫向捲動）；地圖可縮放、可點選（除 F-4 的局部誤觸）；DR-19 三狀態皆有可見呈現、地圖卡不空白、`Select Date` 可見可操作（見 2.7）。 |
| AC-20／AC-21 | **PASS** | 見 2.8。 |
| AC-27 | **PASS** | 舊地圖卡的 `.map-layout`／`.map-side`／`.infocard*`／`.legend-bands*`／inline outline／circleMarker／popup 全部移除（grep 0 筆）；`app.js` 取用的每個 id 都存在於 `index.html`；各函式有說明註解；Leaflet 不存在時有 inline error 路徑（`app.js:391-393`）。 |
| AC-28（前端側） | **PASS** | 注入合成 `/api/days/<date>`（藍 19.9、綠 20.0、黃 25.0、紅 30.0、綠 22.7，外加刻意不一致的「31.0＋blue」）：六個 pill 的 class 與計算後底色完全依 endpoint band（31.0 仍顯示藍），證明前端不重算、不重分帶；圖例 swatch 計算色 `rgb(43,108,176)`／`rgb(47,133,90)`／`rgb(214,158,46)`／`rgb(197,48,48)` 等於 pill 色。五個邊界案例的 pytest（共用模組）在 163 passed 內。 |
| AC-15（DR-20 §3.5(A)-3） | **preview PASS（對 `b4549e5`）** | deployment `6631043843`（sha `b4549e5`，success）；`GET /` 200、`/api/health` 200 `{"forecast_day_count":7,…,"region_count":6,"status":"ok"}`；`/static/data/basemap.js` 200 **196,260 bytes** ＝ `git cat-file -s b4549e5:home_work_01/static/data/basemap.js`；served `app.js` 含 `ensureMapSized`；subject 的 `smoke.py` → `[2026-09-24T06:01:55Z] SMOKE PASS … (1.1s)`，exit 0。targeted correction 之後的 subject 需重做。 |
| AC-02／AC-03（回歸抽查） | **PASS** | `Select Region` 與六區選項、ingestion 時間、Weekly summary、折線圖、表格在 1280 全頁截圖與 test suite 中不變。 |

### 2.4 V-1～V-5（DR-20 P-13；DR-20.6(2)：V 的 FAIL 是本 work item 的 DoD FAIL）

| V | 判定 | 證據 |
| --- | --- | --- |
| V-1 字級 ≥ 12 px 固定 px（地圖卡） | **PASS** | 每個 viewport 對地圖卡內所有可見、含文字節點的元素取 computed `font-size`：最小值 12 px，< 12 px 的元素 0 個（7 個 context）。地圖卡內不適用「內文 ≥ 16 px」（P-13）。 |
| V-2 對比 | **藥丸內文 PASS；色帶對底圖＝UNDETERMINED，交 DA（RS-1）** | 見下方裁量段落。 |
| V-3 六個 tooltip 完整可見（375 與桌機） | **375 PASS；桌機 1024–~1150 FAIL（F-2）** | 375：六個 tooltip 的 rect 都在 `#map-frame` 內；東部 tooltip 右上角的空白 padding 與 zoom 控制重疊 193 px²，文字不受影響。1280：南部 tooltip 左上角 padding 被面板蓋 2.5%（文字完整）。**1024：南部 tooltip 15.6% 在資訊面板下，Region 名「南部地」被遮；1100：5.2%，「南」字被遮**。 |
| V-4 可點區 ≥ 44×44 | **desktop PASS；375 FAIL（F-4）** | 1280：每個 pill 中心 44×44 內 225／225 取樣點都命中自己。375：北部 213／225、南部 182／225、東南部 195／225；南部可見 pill 內有 22 個取樣點命中其他元素，實點 x=139、146（pill 範圍 93–151）選到 **東南部地區**。 |
| V-5 截圖 | **PASS（附 F-9 Low）** | 12 張截圖與 Reviewer 自己的渲染一致（版面、值、狀態訊息相同）；light／dark × desktop／375 皆有；hover 只有 dark（F-9）。Executor 自己的 `issue-28-state-error.png` 可見 F-3 與 F-6 的現象。 |

**V-2 裁量（依派工要求明確裁定）。** Reviewer 以 WCAG 2.x 相對亮度公式自行計算（token 值），結果與 worklog 一致：藥丸內文對藥丸底 blue 5.42、green 4.54、yellow（`#1a2230` 字）6.68、red 5.47，**全部 ≥ 4.5，PASS**。色帶對海 `#0f1927`：3.26／3.89／7.39／3.23（全 ≥ 3）；對台灣陸地 `#25324a`：**2.37／2.83／5.38／2.35**（藍、綠、紅 < 3）；對周邊陸地 `#1a2331`：2.92／3.48／6.62／2.89；白色 2 px 描邊對海 17.67、對台灣陸地 12.85。六個代表點經 point-in-polygon 核對**全部落在台灣縣市多邊形內**，所以 pill 實際相鄰的底圖顏色是台灣陸地 `#25324a`，不是海。**裁定**：(a) Reviewer **不接受**以「對海 ≥ 3:1」證明 V-2——那不是 pill 所在位置的相鄰底色，對 V-2 要測的東西沒有證明力。(b) 白描邊理由在 WCAG 1.4.11 的意義下成立：以 ≥ 3:1 的邊界界定元件時，填色本身不必與外部背景達 3:1，而白描邊對所有底圖色都遠超 3:1；另外色帶資訊不只靠顏色傳達（pill 上有數值，另有圖例）。但 V-2 經 acceptor 核定的文字是「**四段色帶**對底圖 ≥ 3:1（token 值計算）」（Issue #28 DoD；DR-20 P-13），對比的對象是色帶 token，不是整個標記；指示來源草稿寫的是「標記對底 ≥ 3:1」（DR-20 E-10）。白描邊能否滿足 V-2，取決於 V-2 對比的是「色帶顏色」還是「標記」，契約沒有說清楚。而且兩組都經 acceptor 核定的 HOW token（P-2 陸地 `#25324a`、P-4 色帶）在字面讀法下，藍、綠、紅三色必然不合格，Executor 除非改動核定 token，否則無法修正。**因此 border 理由是否滿足 V-2，屬於驗收語義的問題，由 Design Authority 裁決（RS-1）**；在 DA 裁決前，V-2 的色帶部分記為 **UNDETERMINED**：不是 PASS，也不是本 R1 的 blocking FAIL（治理 §4.2：契約語義不足是 routing signal）。worklog 的「PASS with border rationale」在 DA 裁決前，不得以 PASS 帶進 ACCEPTANCE.md 或 phase-acceptance 增補。Reviewer 不要求改 token。

### 2.5 High-risk 核對（A-1；A-4 觸發）

- **觸及的類別**：H-2（頁面標籤移位：`Select Date` 移入地圖面板；地圖卡新增 `Date`／`Min`／`Max` 與六個 Region 名）、H-3（Derived Map Temperature 的顯示與「導出／相容性」標示；README 措辭）、H-1（README 與截圖屬「撰寫文件」）。
- **H-2 核對與結果：HOLDS。** 渲染 DOM 與原始檔逐字：`<h1>Taiwan Weather Forecast</h1>`（`index.html:21`）；`<label … for="region-select">Select Region</label>`（`:150`）；`<label … for="date-select">Select Date</label>`（`:89`）；表頭 `Date`／`MinT`／`MaxT`（`:201`）、圖表圖例 `MaxT`／`MinT`；地圖面板 `Date`／`Min`／`Max`（`:110-112`）、tooltip `Date …`、`Min … · Max …`；六個 Region 中文全名逐字出現在 pill 標籤、tooltip、`aria-label`、面板（全部取自 `REGION_ORDER`，`app.js:51-53`，與 `/api/regions` 相同）。`test_dashboard.py::test_index_page_has_visible_teacher_text` 與 `test_map_frontend.py::test_index_has_map_panel_select_date_and_legend` PASS。`data.db`／DDL／`app.py` 未觸及。
- **H-3 核對與結果：HOLDS。** (1) 七個 Forecast Day 各取 `/api/days/<date>`，與 DOM 逐一比對六個 pill：文字＝`derivedMapTemperature.toFixed(1)+"°"`、class＝`pill pill--<colourBand>`、`aria-label` 的 Min／Max／derived、tooltip、tile max／min、所選 Region 區塊——兩個 context 共 84 個 pill 比對，**0 筆不符**（本快照 42 格皆 yellow，例：9/24 北部 27.2、中部 28.8、南部 29.2、東北部 26.5、東部 27.0、東南部 27.5）。(2) 以合成 endpoint 覆蓋四個色帶與 AC-28 邊界值，外加「31.0＋blue」不一致對，前端照 endpoint band 著色（見 AC-28），證明沒有前端重算或重分帶。(3) `toFixed(1)` 只作用在 endpoint 已是一位小數的值（`app.js:688-691`），不是捨入邏輯。(4) 標示：見 INV-7；來源句沒有把六區值寫成 CWA 發布（AC-14(8)）；README 沒有把 vendored 縣市多邊形描述成資料圖層（「backdrop only, not a data layer」，README:274-276；P-2(c)）。
- **H-1 核對與結果：HOLDS。** 見 INV-5；新增的 12 張 PNG 與 README 沒有金鑰；CI credential scan 綠。

### 2.6 R-EN-6／零外部請求

**PASS。** Network log 見 INV-6（含 7 次切日與 zoom 操作，外部 0）。`static/data/basemap.js`：無 `https?://`、無 `fetch(`、無 `opendata.cwa.gov.tw`／`CWA_API_KEY`；大小 196,260 bytes ≤ 300 KB；`window.TAIWAN_BASEMAP = Object.freeze({context, taiwan})`，22 個台灣幾何、座標皆為有限數。README 記載來源（Natural Earth `ne_50m_admin_0_countries` public domain；內政部「直轄市、縣市界線(TWD97經緯度)」v1140318，政府資料開放授權條款）、attribution（地圖 attribution control 的文字，`app.js:561-563`）、免金鑰／帳號／付費、代表點為專案定義並列出微調座標、`Select Date` 位置（README:259-293）。P-5：六個代表點全部落在台灣縣市多邊形內（point-in-polygon，各落在不同多邊形），北部 `[25.12,121.38]`、東北部 `[24.66,121.80]` 在地理上分別位於新北、宜蘭。

### 2.7 已閉合 #24 findings 的不回歸（§3.5(A)-5）與 DR-19

- **#24 F-1（切換日期後開著的資訊卡須更新）— 未回歸。** 點中部 pill（tooltip 開著）後把 `Select Date` 改為 2026-09-29：tooltip 由 `24.8／32.8／28.8` 更新為 `Date 2026-09-29 / Min 25.3°C · Max 32.0°C / Derived 28.7°C`，所選 Region 區塊同步更新，皆等於 endpoint。
- **#24 F-3（亂序回應）— 未回歸。** 將 2026-09-25 的回應延遲 2.5 s，150 ms 後改選 2026-09-28；等延遲回應落地後，畫面仍是 2026-09-28（北部 28.4°＝endpoint）。`mapReqSeq` 守衛保留（`app.js:343, 348, 371`）。
- **#24 F-4（靜態掃描遞迴）— 已修且有守衛測試**（見 AC-04(b)）。
- **#24 R2 N-1（地圖邊緣裁切）— 375 與 1280 的容器邊緣裁切已解決**（`tipDir()`，`app.js:455-459`）；但新版面引入的是**被浮動面板遮住**（1024–~1150 的南部 tooltip，F-2），不是容器裁切。320／360 px 仍有邊緣裁切（F-11，V-3 判準外）。
- **DR-19（P-7(b)）— PASS。** 對 `/api/days/2026-09-26` 模擬 503、500、404、network abort、2xx 空值、2xx 非 JSON、4 s 延遲：分別顯示 inline error（`role="alert"`，伺服器訊息或 404 專用文案）、empty（`role="status"`）、loading；`Select Date` 可見、未停用、7 個 option；地圖卡高度不變（非空白）；改選可用日期後狀態清除、值更新。`/api/days` 本身 503 或空清單（375）：inline error／empty，`Select Date` 可見但停用（無日期可列，P-7(b) 允許）；不是整頁 error。可讀性問題見 F-3（desktop）、F-1（tablet）、F-6、F-7。
- **Init hazard（P-12）— 行為 PASS，但回歸測試不足（F-5）。** 在 DOMContentLoaded 後把 `#map-frame` 設為 `display:none` 2 s，以及把 `.map` 高度設為 0 1.5 s：兩種情況下地圖都等到容器有尺寸才初始化（期間 pill 數 0），顯示後六個 marker 座標有限、全在 frame 內，transform 與正常載入相同，沒有 console error 或 pageerror。

### 2.8 測試與 CI（§3.5(A)-3 AC-20／AC-21）

- 乾淨匯出的 subject、無 `.env`、無網路：`python -m pytest -q -p no:cacheprovider` → **163 passed in 7.53s**（Python 3.12.14）。baseline `720c0a0` 收集到 152；subject 163；多出的 11 個＝`test_map_frontend.py` 10＋`test_static_checks.py::test_static_scan_is_recursive_over_subdirectories` 1。
- CI：`b4549e5` push `35960925910`、pull_request `35960928988` 皆 success；log 顯示 checkout `b4549e50…`、`163 passed in 3.88s`、`credential scan passed: 530 tracked files; …`。`6b906a4` 的兩個 run 亦 success。
- `test_map_frontend.py` 是否真的鎖住行為：H-3（`test_frontend_does_not_re_derive_or_re_band`）、pill 與圖例 token 相等、basemap 完整性／大小、面板 wiring 都有實質檢查力。**init hazard 的兩個測試沒有檢查力**，見 F-5（mutation 證據）。

### 2.9 Work item DoD 紀錄

README（見 2.6）與 tickets.md 的 #28 列（Lightweight、H-2／H-3、Blocked by #24／#25）存在；ACCEPTANCE.md 的 AC-04／17／18／19 列與 §6 已更新，但 §6「F-5(a) … all six tooltips fully visible at 375 & desktop (V-3 measured)」與 worklog 的 V-3／V-4 敘述都與本 audit 的量測不符（F-2、F-4），修正時須一併更正。worklog 的 Audit status 正確寫「required（A-4）」。

## 3. Findings

### F-1 — High — **blocking**：tablet 寬度（641–~880 px）浮動資訊面板／圖例遮住 pill，使其不可見、無法點選或 hover

- **證據**：`sweep.js`（dark，捲動到地圖，`elementFromPoint` 測 pill 中心，rect 相交面積；pill 約 58×30＝1,749 px²）：
  - 641：中部、南部 pill 的中心落在面板內容上（`map-tile__value`、`map-sel__row`）；東部的中心落在圖例上；東南部被面板遮 1,595 px²；北部被遮 988 px²；hover 無法觸及 4 個 pill。
  - 700：中部、南部整個被蓋（1,749 px²），中心落在面板上；東南部 785、東部 414（圖例）、北部 113 px²。
  - **768**：中部被遮 965 px²，中心落在 `map-panel--info`；**南部整個在面板下（1,749 px²）**；兩者 hover 都無法觸及。
  - 800／820／834：南部的中心仍落在面板（被遮 1,445／1,145／935 px²）；中部被部分遮。880：南部被遮 245 px²。≥ 900：pill 不再被遮，但 tooltip 仍被遮（900：中部 13.7%、南部 31.6%；960：南部 13.7%）。
  - 同一問題也使 DR-19 狀態訊息在 768 被面板蓋住（error 44.6%、empty 37.9%、loading 28.4% 的文字面積，`statemsg.js`）。
  - 截圖 `pw/out/ev-768-initial.png`、`ev-820-initial.png`：768 只看得到中部的「8°」，南部 pill 完全不見。
  - **回歸**：baseline `720c0a0` 在 768（`base-768.png`）六個 marker 全部可見（側欄版面）。
- **原因**：`.map-panel--info` 在 ≥ 641 px 為 `position:absolute`、寬 288 px、高約 413 px、`z-index:600`（`styles.css:447-454`），疊在 `z-index:400` 的 Leaflet map pane 上；tablet 的地圖寬約 580–950 px、高 440 px（`styles.css:402`），但 `fitBounds` 只用固定 padding `[26,52]`／`[26,44]`（`app.js:640-644`），沒有把浮動面板佔的區域留出來。
- **契約**：DR-20 **P-7(c)**「面板不得遮住任何藥丸的初始位置（R-EN-4『初始視野涵蓋六個標記』以可見為準）」——此條件沒有限定 viewport，而 P-1 本身就定義了平板版面（440 px）；Spec **R-EN-4**「初始視野涵蓋六個標記」與「點擊或 hover 顯示資訊卡」；AC-17「六個標記皆可見」。
- **Closure 條件（R2 核對）**：641–1023 每個寬度（至少 641／700／768／800／820／834／880／900／960／1023）的初始視野下，沒有 pill 與面板或圖例相交，且每個 pill 中心的 `elementFromPoint` 都是該 pill；tablet 下的 DR-19 狀態訊息沒有被面板遮住；worklog／ACCEPTANCE 補 tablet 寬度的證據。修正方式屬 HOW（例如 tablet 不浮動、依面板實寬設定 `fitBounds` padding 等）。

### F-2 — Medium — **blocking**：V-3 在桌機 1024–~1150 px 不成立——南部 tooltip 被資訊面板遮住 Region 名

- **證據**：`sweep.js`／`shots.js`：1024 hover 南部，tooltip 面積 15.6% 在面板下，截圖 `pw/out/ev-1024-hover-south.png` 只看得到「區」與「26-09-24」，Region 名與 Date 前段被遮；1100 為 5.2%，「南」字被遮（`ev-1100-hover-south.png`）；≥ 1180 為 2.5%，只有 padding 角落（`ev-1280-hover-south.png`，文字完整）。Executor 的 V-3 量測只在 1280、只和 `.leaflet-container` 的邊界比（worklog Verification V-3），沒有把浮動面板算進去。
- **原因**：與 F-1 相同（map pane 的 tooltip 在 `z-index:600` 的面板下面；`fitBounds` 沒有替面板留空間；南部 tooltip 向上、向左延伸到面板區）。
- **契約**：DR-20 **P-13 V-3**「六個標記的 tooltip 在 375 與桌機皆完整可見」；桌機依 Spec R-EN-1(2)／AC-19 為 ≥ 1024 px；DR-20.6(2)：V FAIL 是本 work item 的 DoD FAIL。也使 ACCEPTANCE.md §6 對 #24 F-5(a) 的「RESOLVED」與 worklog V-3 PASS 的敘述不成立。
- **Closure 條件**：1024、1100、1280（及 ≥ 1024 的其他抽樣寬度）下，六個 tooltip 的文字都沒有被面板、圖例或 zoom 控制遮住，也沒有被容器裁切；更正 worklog 與 ACCEPTANCE §6 的敘述。

### F-3 — Medium — non-blocking：桌機的 DR-19 error 訊息開頭被浮動面板遮住

- **證據**：`statemsg.js` 以伺服器實際的 incomplete 訊息（`server.py:54`「The forecast snapshot is incomplete — it is not the full six Regions × seven Forecast Days.」）模擬第一天 503：文字面積 1280 有 15.5%、1024 有 23.5% 在面板下；`pw/out/statemsg-error-1024.png` 只看得到「…t is incomplete — …」。Executor 自己提交的 `issue-28-state-error.png` 也看得到「napshot is incomplete…」，開頭「The forecast s」被遮。短訊息（empty、loading）在桌機沒有被遮。
- **契約影響**：R-EN-1(5)／AC-19 的「三種狀態各自有可見呈現」與 DR-20.6(4)「地圖卡不得空白」仍成立，原因（incomplete）仍可辨識，所以 non-blocking；但伺服器訊息被截斷，不符合 DR-19「顯示伺服器訊息以區分原因」的用意。
- **Disposition**：owner＝Executor；根因與 F-1／F-2 相同，預期在同一 targeted correction 中一併處理（例如讓狀態訊息避開面板區）；不延長 cycle。

### F-4 — Medium — **blocking**：V-4 在 375 px 不成立——相鄰 marker 透明 icon box 攔截點擊，點南部 pill 右側會選到東南部

- **證據**：`v4detail.js`（375、414）：北部 pill 中心 44×44 取樣 213／225 命中自己（12 點落在東北部的 icon box）；南部 182／225（28 點落在東南部的透明 icon box、15 點落在 attribution control；**其中 22 點位於南部可見的 pill 內**）；東南部 195／225（30 點落在 attribution control）。`v4click.js` 以真實滑鼠點擊南部 pill（範圍 x 93–151，y 中心 531）：x=99、122 → 南部地區／29.2；**x=139、146 → 東南部地區／27.5**。hover 同一位置顯示東南部的 tooltip（`pw/out/v4-375-frame.png`）。1280 下六個 pill 皆 225／225。
- **原因**：`styles.css:544-552` 以 `.pill-icon { pointer-events:none }` 讓透明的 104×52 icon box 不攔截事件，但 Leaflet 的 `.leaflet-marker-icon.leaflet-interactive { pointer-events:auto }`（`vendor/leaflet.css:250-255`，specificity 較高）把它蓋掉——computed `pointer-events` 為 `auto`（`behave.js` 六個 icon 皆是）；`app.js:597-598` 又把 click listener 掛在整個 icon 元素上。因此較晚繪製的鄰近 marker 的透明 box 會蓋在前一個 pill 上。worklog V-4「`.pill-icon`/`.rlabel` pointer-events:none，相鄰標記不互擋」的敘述與實際不符。
- **契約**：DR-20 **P-4／P-13 V-4**「可點區 ≥ 44×44」；R-EN-4（點擊標記顯示**該** Region 的資訊卡）；R-EN-1(2)「375 px 寬可完整操作」；DR-20.6(2)。
- **Closure 條件**：375（及 360–640 抽樣寬度）下，每個 pill 中心 44×44 區域內的取樣點都只命中該 pill（不被鄰近 icon box 或 attribution control 攔截）；點擊任一可見 pill 的任一點都選到該 Region；更正 worklog 的 V-4 敘述。

### F-5 — Medium — **blocking**：「NaN／0×0 init hazard」的回歸測試無法偵測回歸

- **證據**（mutation，Reviewer 在 scratchpad 的 subject 副本上做）：同時做兩個突變——(a) `initMap` 內把 `map.invalidateSize()` 移到 `fitBounds(...)` 之後；(b) 把 `ensureMapSized` 的 `if (sized()) { cb(); return; }` 改成 `cb(); return;`（不論容器尺寸都立即初始化）——`pytest tests/test_map_frontend.py` → **10 passed**。原因：`test_map_invalidates_size_before_fitbounds`（`test_map_frontend.py:54-62`）用 `src.find("invalidateSize()")` 抓到的是 resize handler 的 `map.invalidateSize()`（`app.js:149`），不是 `initMap` 內那一次；`test_map_init_defers_until_container_has_nonzero_size`（`:43-51`）只檢查 `ResizeObserver`、`visibilitychange`、`clientWidth > 0` 等字串是否存在（這些字串也出現在註解中）。（`test_pill_uses_endpoint_value_and_band` 同樣只是字串存在檢查，但 H-3 另有 `test_frontend_does_not_re_derive_or_re_band` 有實質檢查力，此處不列為 blocking。）
- **契約**：Issue #28 §2.8「已知 hazard『`Invalid LatLng (NaN,NaN)`／0×0 標記』**須加回歸測試**」；DR-20 **P-12**（回歸測試形式屬 HOW，但須可由 Reviewer 重現，且不得只靠截圖）。在 hazard 被重新引入時仍然通過的測試，不構成該 hazard 的回歸測試。實際行為本身正確（見 2.7）。
- **Closure 條件**：新的或修改後的測試在上述 (a)、(b) 任一突變下都 FAIL（R2 會重做這兩個 mutation）；形式屬 HOW（pytest 讀原始碼並限定在 `initMap`／`ensureMapSized` 的函式本體，或 headless 驅動皆可），但要能在無網路環境重現。

### F-6 — Low — non-blocking：第一個日期載入成功前，圖例 swatch 沒有顏色

- **證據**：`colourLegend()` 只在 `initMap()` 內呼叫（`app.js:646`），而 `initMap` 要等第一個成功的 `/api/days/<date>` 才執行。第一天 error／empty／loading 時，四個 swatch 的計算色都是 `rgb(31,42,59)`（`statemsg.js`）；Executor 的 `issue-28-state-error.png` 可見空白的 swatch。這些狀態下沒有 marker，所以 R-EN-5 的實質影響小。**Disposition**：owner＝Executor（可在 DOMContentLoaded 時就上色）；可選。

### F-7 — Low — non-blocking：切換日期後若該日請求失敗、無值或仍在載入，面板繼續顯示前一天的值

- **證據**：`behave.js` 各狀態下，`Select Date`＝2026-09-26、caption「Showing 2026-09-26」，但面板仍是 `Forecast Day: 2026-09-24`、tile 與所選 Region 區塊是 9/24 的值（`app.js:339-377` 只在成功時才呼叫 `renderDay`）。這些值都標著它們自己的日期，沒有把值標錯日期，所以不違反 P-10(a)；但同一個面板裡出現兩個日期容易誤讀。**Disposition**：owner＝Executor；建議在 inline 狀態時把面板的值清空或變暗；可選。

### F-8 — Low — non-blocking：每個 marker 有兩個 tab stop，外層 stop 按 Enter 沒有作用

- **證據**：`L.marker(..., { keyboard: true })`（`app.js:592`）讓外層 icon 成為 `tabindex=0`、`role="button"`，內層 `.pill` 也是 `tabindex="0"`、`role="button"`，所以 6 個 marker 共 12 個 tab stop，且形成巢狀 button。焦點在外層 icon 時按 Enter，所選 Region 不變（`zoom.js`：仍為北部地區）；焦點在 pill 時按 Enter 可正常選取。核定的 a11y 項目（可 Tab、`aria-label`）仍成立。**Disposition**：owner＝Executor；可選（例如 `keyboard:false`）。

### F-9 — Low — non-blocking：V-5 的 hover 截圖只有深色系

- **證據**：`issue-28-desktop-hover-tooltip.png` 與 `issue-28-375-hover-tooltip.png` 的頁面背景都是深色（像素取樣 `(15,19,26)`）；P-13 寫的是「淺色與深色各一組截圖（桌機、375，含 hover 一個標記）」。地圖卡在兩種色系下都是深色，所以影響小。**Disposition**：owner＝Executor；在修正後重拍截圖時補淺色 hover。

### F-10 — Low — non-blocking：同一頁有兩種溫度寫法（P-10(b) SHOULD）

- **證據**：地圖面板、tooltip、tile 用 `oneDp` 顯示 `31.0 °C`，表格用 `formatTemp` 顯示 `31`（1280 全頁截圖）。值都等於 endpoint；P-10(b) 是 SHOULD。**Disposition**：記錄；可選。

### F-11 — Low（資訊）— non-blocking：320／360 px 下 tooltip 被容器邊緣裁切

- **證據**：`sweep.js`：320、360 下南部與東北部的 tooltip 超出 `#map-frame`；375 以上都沒有。V-3 的判準是 375，所以不構成 FAIL。**Disposition**：記錄；無需處理。

## 4. Routing signals（不是 blocking finding）

- **RS-1 → Design Authority（驗收語義）**：V-2「四段色帶對底圖 ≥ 3:1」的比較對象與範圍。請 DA 裁定：(i) 比較對象是色帶 token 本身（字面讀法；pill 位於台灣陸地 `#25324a` 上時，藍 2.37、綠 2.83、紅 2.35 不合格），還是整個標記（草稿「標記對底」；白色 2 px 描邊對陸地 12.85、對海 17.67，依 WCAG 1.4.11 界定元件）；(ii) 若採字面讀法，P-2 的陸地色與 P-4 的色帶 token 都是 acceptor 核定的 HOW，兩者無法同時成立，須由 DA 決定修改路徑（以及是否需要 acceptor）。在裁定前，V-2 的色帶部分為 UNDETERMINED（見 2.4）。
- **RS-2 → Design Authority（boundary determination，低風險）**：`index.html:22-26` 的 masthead 導言由「pick a region to see its temperature trend, daily table and weekly summary」改寫為「read the derived map temperature for a day on the Taiwan map, then pick a region below …」。Issue #28 §2.9 寫「**不動** masthead」；X-3 的禁止對象是「重做 masthead」。Reviewer 的看法：這是配合 map-first 版面、描述頁面順序的一句文案，概念詞 `Taiwan Weather Forecast` 未動，看起來不是 X-3 所指的重設計；但依規則，boundary 疑義先交 DA 判定。DA 若判定在 boundary 內，本項即關閉；若判定在外，Executor 在 targeted correction 中還原該句。

## 5. 給 targeted correction 與 R2 的範圍

- **Blocking**：F-1（tablet 遮擋 pill／狀態訊息）、F-2（V-3 桌機 1024–~1150 南部 tooltip 被遮）、F-4（V-4 375 相鄰 icon box 攔截）、F-5（init hazard 回歸測試無偵測力）。F-1 與 F-2 根因相同；F-3 預期隨之解決。
- **修正後須重做的證據**：受影響的截圖（含 tablet 寬度、淺色 hover）、worklog 的 V-3／V-4 量測敘述、ACCEPTANCE.md §6 的 F-5(a) 敘述、對新 subject 的 CI 與 preview smoke（AC-15）。
- **R2 會核對**：各 blocking finding 的 closure 條件；不回歸——H-3 七日 parity、network 零外部、DR-19 七種模擬與 P-7(b) 復原、#24 F-1／F-3、`fitBounds` 只呼叫一次（不重設視野）、375 無橫向捲動、V-1、163＋新增測試與 CI。
- **RS-1、RS-2** 的 DA 裁定不阻擋 targeted correction 開始；但 V-2 在 DA 裁定前不得記為 PASS。

## 6. 證據索引（Reviewer 自行產生，scratchpad `pw/`）

| 腳本 | 內容 | 主要輸出 |
| --- | --- | --- |
| `audit.js` | 7 個 context 的版面、network、V-1、tooltip、七日 parity | `out/report1.json`、`desktop-*.png`、`m375-*.png`、`tablet-*.png` |
| `sweep.js` | 26 個寬度：pill 被遮／可點、tooltip 裁切／被遮 | `out/sweep-320-1920.json` |
| `shots.js`、`base768.js` | F-1／F-2 的截圖；baseline 768／820 對照 | `out/ev-*.png`、`out/base-768.png`、`base-820.png` |
| `behave.js` | DR-19 七種模擬＋復原、`/api/days` 失敗、#24 F-3／F-1、init hazard、鍵盤、44×44、色帶注入 | `out/behave.json`、`state-*.png`、`init-*.png`、`bands-injected.png` |
| `statemsg.js` | 狀態訊息被面板遮住的比例（F-3、F-1）、swatch 顏色（F-6） | `out/statemsg-error-{1024,768}.png` |
| `v4detail.js`、`v4click.js` | F-4 的取樣與實點擊 | `out/v4-375-frame.png` |
| `zoom.js` | zoom 與標籤切換、外層 icon 的 Enter（F-8）、favicon | console 輸出 |
| mutation（`mut/home_work_01`） | F-5 | `10 passed` |

VERDICT: BLOCKING (F-1, F-2, F-4, F-5)
