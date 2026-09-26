# Audit record — Issue #36，cycle 1，R1（Formal Ticket independent audit）

| 欄位 | 內容 |
| --- | --- |
| Work Contract | GitHub Issue **#36**（`yotsubamomo/aiot-classwork`）「Now mode 與 Forecast mode：預設 Now、模式切換、全臺代表測站的 Latest Observation 與 Observation Time／Fetched Time」。上位：V2 Outcome Contract `home_work_01/doc/governance/outcome-contract-v2.md`（ACCEPTED 2026-09-25，normative candidate `69c5a04`）；Delta Spec `home_work_01/doc/spec/SPEC-V2.md` **v2.2**（§1.2 Δ-5／Δ-7／Δ-14、§2.1、§2.2 OBS-4(c)／OBS-7(a)(b)(c)、§2.3 DD-2／DD-3／DD-10、§2.5 DEG-1／DEG-3／DEG-5、§2.8 DOC-1(1)(2)(3)／DOC-4／DOC-5、§5.3、§6.3）；V1 Spec v1.1（AC-02／03／10／17／18／24、INV-2／7／9）與 DR-17、DR-19、DR-20／DR-21；derivation record `derivation-SPEC-V2.md`（DV-8、DV-9、DV-14、DV-17、DV-18、§6、§15）；`decision-20260923-high-risk-categories.md`（A-1）；BRIEF-V2 §9。本票分配：AC-V2-01、02、03（瀏覽器抽樣）、04（瀏覽器 success 面）、09(a)＋API 面、11、15（模式切換路徑）、16（Now／Forecast 執行期 network log）、20（本票範圍）、21(13)、23（`Back to Taiwan` 除外）；README R-V2-DOC-1 (1)(2)(3)；§6.3 定向 V1 重驗 AC-17、AC-18、標題與 masthead、AC-02／AC-03／AC-24（Dashboard 側）、AC-10（Dashboard 側）；INV-V2-3、5、7（預報失敗面）、8、9；V1 INV-2、7、9。 |
| 受審 subject | branch `home_work_01-v2-implementation`；BASE **`42665e86581522f8b0759e08094143e390d07e1c`** .. HEAD **`dcd697c35f6f6ec3ccedbee1b51f143c52ee1f61`**；code anchor **`f63ebb145b59af1686e9ad1993876c075d8c81ae`**。`f63ebb1..dcd697c` 只有 `home_work_01/doc/governance/worklog/issue-36.md`（record-only，Bindings §7）。`git ls-remote origin` 目前指向 `55aab6e`，`dcd697c..55aab6e` 只有 run record（record-only，派工者）。`42665e8..f63ebb1` 的 29 檔全部在 `home_work_01/` 內（單元目錄外 0 檔、`doc/requirement/` 0 檔）。Working tree 的 code 與 `f63ebb1` 相同（`git diff --stat f63ebb1 HEAD` 只有兩個 `doc/governance/**` 檔）。 |
| Audit 種類 | **R1**（Formal 必做的 Ticket independent audit；治理 §4.1、§4.4），**cycle 1**。不是 Spec Integration Audit。 |
| 角色 | `primary_reviewer`（definition `gov-primary-reviewer`；Bindings §3.1 mapping `claude-opus-5-5`／`xhigh`） |
| Binding 證據 | 正式核對由派工者（Orchestrator）依 Bindings §3.4 記入 run record `home_work_01/doc/governance/run/run-20260925-hw01-v2-formal.md`（#36 Executor 一列已記 `a97513f8b8d5b2091`）。Reviewer 另以 Bindings §3.4 指令讀 harness 紀錄（session `05b8408b-260a-46d3-a4fe-ec07e3ec365a`）自行觀察：`agent-a7afb069135999b78` `gov-primary-reviewer` `[('claude-opus-5-5', 'xhigh')]`（本 Reviewer；其第一則訊息即本次 #36 R1 派工）；`agent-a97513f8b8d5b2091` `gov-executor` `[('claude-opus-5-5', 'high')]`（#36 Executor；其第一則訊息為 #36 執行派工）。兩者皆與 Bindings §3.1（b2 override）一致。此觀察只供對照，不取代派工者的核對。 |
| Independence（治理 §2.3、§4.6） | (1) **Fresh context**：未繼承 Executor 對話；worklog `issue-36.md`、commit message 與已提交的瀏覽器證據一律當作待驗證主張。(2) **Binding**：見上一列。(3) **Autonomous access**：自讀 `gh issue view 36`、SPEC-V2 v2.2、V1 SPEC、derivation record、decision A-1、BRIEF-V2、#35 audit records、git 歷史與 diff、CI run 與 log；以 `git archive 42665e8` 匯出 BASE 到 Reviewer scratchpad；重跑 Executor 的 `check_modes_browser.py`（輸出導向 scratchpad，不覆寫已提交證據）；另自寫四個 probe（`probe.py`：CDP `Fetch` domain 在 request 階段攔截**全部**請求並封鎖非 loopback；`probe2.py`／`probe3.py`：哨兵「—」、鍵盤順序、觀測失敗時的模式獨立性；`probe4.py`：遠端 Now 視野進 Forecast 再回來；`handcalc.py`：依 README 規則手算代表測站，偏好資料以文字讀取、不 import 規則模組），皆在 scratchpad、未提交。(4) **Self-written record**：本紀錄由 Reviewer 以自己的 Write 工具寫入。**Model diversity：`diversity_lost`**——Executor 與 Primary Reviewer 同為 `claude-opus-5-5`（Bindings §5、b2 override；decision A-7）。這是合法狀態，不是缺陷，也不減損 §2.3 的 independence。 |
| 日期 | 2026-09-26 |

## 1. 審查方法與環境

- **環境**：Windows 11；`home_work_01/.venv` Python 3.12.14；Chrome 153 headless（DevTools protocol，`websocket-client` 1.9.2，venv 內既有）。
- **Reviewer 對憑證的處理**：Reviewer **沒有讀取** `home_work_01/.env`，沒有發出任何 CWA 請求。所有 probe 以 `create_app(observation_service=…)` 注入由已提交樣本 `tests/fixtures/O-A0001-001_sample.json` 產生的模擬上游與佔位金鑰（`x-not-a-key`）；預報 503 情境以不存在的 DB 路徑觸發（事後 `git status` 確認未產生檔案）。沒有 git 寫入、沒有修改追蹤中的檔案（本紀錄除外）；工作結束時 `git status --short` 只有與本票無關、既存的 `grep.exe.stackdump`。
- **Commit 衛生**：`42665e8..dcd697c` 兩個 commit message 皆為 `[Modify] – …` 格式；`grep -icE "claude|co-authored|generated with"` → 0。`git diff --check 42665e8 f63ebb1`（排除 PNG）乾淨。

## 2. 分配 AC 的逐條結論

| AC／項目 | 判定 | 證據（Reviewer 自行取得） |
| --- | --- | --- |
| **AC-V2-01** | **PASS**（本 subject 可觀察的全部部分）；「選一縣」往返見 §4 關切 1 與 R-1 | 載入即 Now：`app.js:81` `var mode = MODE_NOW`、`index.html:51,54` 初始 `aria-pressed`；Reviewer probe 在任何動作前取樣，`/api/health` 200 與 503 兩情境、1280 與 375 皆為 `now:"true"`。Now 載入不經 `/api/health`：`app.js:257-260` 在 `DOMContentLoaded` 直接呼叫 `loadObservation()`，與 `bootstrap()` 並列。切換控制：兩個原生 `<button>`（`index.html:50-57`），可見文字含 `Now`／`Forecast`，`aria-pressed`＋填色指示目前模式；probe 量測 toggle rect 1280＝y 236–288（視窗 900）、375＝y 253–305（視窗 812），`scrollY` 0。鍵盤：新載入後 Tab 順序 `mode-now → mode-forecast → refresh-button → map`（`probe3.py`）；Executor 檢查以 Enter 切 Forecast、Space 切回，Reviewer 重跑通過。往返：`setMode`（`app.js:265-277`）離開 Now 時存 `nowView`，`restoreNowView`（`:346-352`）以 `setView` 恢復，選取存於 `selectedStationId`；Reviewer probe 在放大／縮小／Refresh／選站後往返（中間在 Forecast 改日期並點 pill），兩個視野 22 個標記的畫面座標完全相同、選取仍為「臺北 station」；`probe4.py` 以 zoom 10 拖曳到西側遠端視野（1280 只剩澎湖標記、375 無標記）後進 Forecast → 6/6 pill 在地圖內、回 Now → 視野逐點相同。進入 Forecast 時六標記可見：`showSixRegions`（`:357-362`）六點皆在清空區則保留，否則 `fitToMarkers(六點 ∪ 清空區)`（DV-8 的最小調整）。Forecast mode 內 AC-17／AC-18 見 §6.3 列。截圖：Executor 提交的 1280／375 Now 預設與 Forecast mode 截圖存在；Reviewer 另產生同組截圖於 scratchpad。 |
| **AC-V2-02** | PASS | Now mode：`Select Date`、`forecast-panel`、`forecast-legend` 帶 `data-mode="forecast"`，`renderModeChrome`（`app.js:281-300`）以 `hidden` 隱藏，CSS `[hidden]{display:none !important}`（`styles.css:101`）確保不被覆寫；probe 的 `.map-shell` `innerText` 無 `Select Date`／`Derived map temperature`／`DERIVED`，Forecast pill 不在 DOM（`forecastLayer` 已移除）。Forecast mode：`now-panel` 隱藏、`nowLayer` 移除，`innerText` 無 `Refresh`／`Observation Time`／`Fetched Time`／`Latest Observation`，station 標記 0。觀測無圖例、無色階；標記底色 `--obs-pill-bg #f2f5fa` 與四個 `--band-*` 互斥（靜態 `test_observation_markers_share_no_colour_with_the_derived_bands` 與瀏覽器計算色皆核對）。全頁 `innerText`、`index.html`、`app.js` 無 `real-time`／`realtime`／`live`（`aria-live` 屬性除外）。`Fetched Time` 在 Now 面板（`index.html:81-82`），預報快照時間 `Last updated (data fetched from CWA): …`（`app.js:1563-1566`，DR-17 原樣）在 `#forecast-section` 的控制卡，垂直距離 > 100 px、文字不同。下方 `#dashboard` 的 `innerText` 在兩模式完全相同。 |
| **AC-V2-03**（瀏覽器抽樣） | PASS | Reviewer probe 以頁面實際取得的 `/api/observations/latest` 本文為 oracle：臺北 `466920` 27.1、澎湖 `467350` 26.3、馬祖 `467990` 24.6 的標記文字分別為 `27.1°`／`26.3°`／`24.6°`，`aria-label` 為「<站名> station, <縣>: air temperature … (Latest Observation, station value)」；在 1280／375、預報 OK／503 四組皆同。哨兵：`probe2.py` 把澎湖的 `Weather`＝`X`、`WindSpeed`＝`-99`、`RelativeHumidity`＝`-99.0` → `/api/` 三欄 `null`，選取後畫面三欄皆「—」、氣溫 `26.3 °C`。preview 抽樣屬 #41。 |
| **AC-V2-04**（瀏覽器 success 面） | PASS | `<dt>` 逐字 `Observation Time`、`Fetched Time`（`index.html:77,81`）；值以 `formatObsTime` 只重排發布字串（`app.js:747-752`，不經瀏覽器時鐘；靜態守衛 `test_observation_times_are_shown_as_published`），Observation Time 到分、Fetched Time 到秒；Executor 檢查（Reviewer 重跑 37/37）核對面板值等於回應 `observationTime`／`fetchedTime`／`validStationCount`，Refresh 後兩個時間更新為新回應。Stale／Unavailable 面屬 #37。 |
| **AC-V2-09(a)＋API 面** | PASS | 預報 503（DB 缺失）＋觀測正常：Reviewer probe 1280／375 皆為 Now 預設、22 個標記、toggle 可見可用；Executor 檢查（重跑）另核對 `#page-error` 可見、`role="alert"`、文字＝伺服器 `error`、位於 `#forecast-section`、`#dashboard` 隱藏、地圖卡可見（非整頁遮蔽）、預報 503 時 Refresh 仍成功；切 Forecast → 地圖 inline error `role="alert"`、同一伺服器訊息、`Select Date` 停用（`app.js:385-395`、`:1204-1218` 只在 Forecast mode 渲染）；切回 Now 不覆蓋地圖。API 面：`server.py`、`smoke.py`、`vercel.json`、`weather_query.py` 在 `42665e8..f63ebb1` 無 diff；V1 `/api/health` 200／503 測試與 #35 的「觀測無金鑰時 `/api/health` 仍 200」測試保留並通過。 |
| **AC-V2-11** | PASS | 離線：`tests/test_representative.py` 11 項通過——每縣 ≤ 1、皆有效、22 縣全涵蓋；重複與輸入重排結果相同；四縣偏好站設 `-99` → 後備、其他 18 縣不變；範圍外東沙島 `468100` 永不被選；連江縣全無效 → 無代表；`/api/` 回應的 `representativeStationIds` 等於規則重算。**Reviewer 手算**（`handcalc.py`，依 README「Representative station rule」四步，偏好資料以文字自 `representative.py` 讀出）：臺北市 19 候選 → 偏好 `466920` 臺北；澎湖縣 8 候選 → `467350` 澎湖；金門縣 6 候選 → `467110` 金門；連江縣 4 候選 → `467990` 馬祖；新竹市 6 候選 → `C0D660`；衍生樣本（臺北、高雄、澎湖偏好站設 `X`）→ 臺北 `466910` 鞍部、高雄 `72V140`（`468100` 經度 116.73 在範圍外被排除）、澎湖 `467300` 東吉島，其餘 19 縣不變；**全部 22 縣手算＝`/api/`**；畫面標記與 `/api/` 一致（AC-V2-03 列）。README 與 Spec 不列舉 22 個 StationId（測試限制 README ≤ 4、實為 1；Spec 0）。 |
| **AC-V2-15**（模式切換路徑） | PASS | V1 `test_map_frontend.py` 四個初始化守衛未修改且通過（`fitBounds(` 全檔 1 處、在 `fitToMarkers` 內、`invalidateSize()` 在前，`app.js:1156-1167`）。模式切換經 `bringUpMap → ensureMapSized`（`:313-322`、`:984-1011`），`syncMap` 的切換分支先 `invalidateSize()` 再 `removeLayer`／fit／`setView`（`:324-343`；靜態守衛 `test_mode_switch_recomputes_size_before_any_view_change`）。Reviewer probe 各情境往返後 `.leaflet-marker-icon` 的 transform 無 `NaN`、無 0×0（全部 0 件），`Runtime.exceptionThrown` 0 件。資訊面開合與 resize 屬 #39。 |
| **AC-V2-16**（執行期 network log） | PASS | **Reviewer 重新擷取**（不採信已提交的 `network-log.json`）：`probe.py` 以 CDP `Fetch.enable {urlPattern:"*", requestStage:"Request"}` 攔截所有資源類型，非 loopback 一律 `failRequest` 並記錄；另比對 `Network.requestWillBeSent` 與 `performance.getEntriesByType('resource')`。操作涵蓋：載入、放大 4 級、縮小 6 級、Refresh、選站、切 Forecast、改 Select Date、點 pill、切回 Now；1280 與 375；預報 OK 與 503。結果：預報 OK 攔截 31 筆、503 攔截 21 筆，唯一 URL 只有 `/`、`/favicon.ico`、`/static/{app.js,styles.css,vendor/leaflet.css,vendor/leaflet.js,data/basemap.js}` 與 `/api/{health,regions,regions/<r>/series,days,days/<d>,observations/latest}`；**外部請求 0**（三個來源皆 0）。靜態：`styles.css` 無 `url(`／`@import`／`@font-face`；`index.html`／`app.js` 的絕對 URL 只有 SVG namespace 常數；`test_static_checks.py` 的前端檢查與白名單未變。Radar 顯示中的 log 屬 #40。 |
| **AC-V2-20**（本票範圍） | PASS | Subject `pytest` → **459 passed**；BASE（`git archive 42665e8`）收集 424 個 test id，**全部**仍在 subject（`comm -23` 空），新增 35 個。既有測試檔只有兩處修改：`test_observation.py:238-242` 精確鍵集合加入 `representativeStationIds`（仍為 `==` 精確比對）、`test_static_checks.py:77-79` 把 `representative.py` 加入 no-SQL 集合（只加）；`test_secrets.py` 只加掃描對象。`test_map_frontend.py`、`test_dashboard.py`、`test_app.py` 未修改。`app.py`、`weather_query.py`、`ingestion/`、`data.db`（blob `687586991ce3…` 兩端相同）、`smoke.py`、`requirements.txt`、`server.py`、`api/`、`.github/` 在 `42665e8..f63ebb1` 無 diff；對 `main`（V1 結案內容）`app.py`／`weather_query.py`／`ingestion`／`data.db`／`smoke.py`／`requirements.txt` 亦無 diff。CI：`36168995238`（`f63ebb1`）、`36169390402`（`dcd697c`）、`36169636649`（`55aab6e`）皆 success，log 為 `459 passed` 與 `credential scan passed`。 |
| **AC-V2-21(13)** | PASS | `CONTEXT.md` diff：BRIEF-V2 §9 十列的定義與「避免」逐字併入（Taiwan Map、Now mode、Forecast mode、Latest Observation、Observation Time、Fetched Time、Refresh、Re-ingestion、Stale、Unavailable）；原「Refresh」詞條改名 Re-ingestion，舊的「Running Ingestion again」定義已不存在；Reviewer 逐列目視比對 diff 與 BRIEF-V2 第 116–125 行一致，另有 `test_context_glossary_delta_is_verbatim` 守衛。其他詞條未改。最終文件審查屬 #41。 |
| **AC-V2-23**（`Back to Taiwan` 除外） | PASS | `index.html`：`<title>`／`<h1>` 逐字 `Taiwan Weather Forecast`（`:6`、`:22`）；`Now`、`Forecast`（`:52`、`:55`）；`Latest Observation`（`:70`）；`Observation Time`、`Fetched Time`（`:77`、`:81`）；`Refresh`（`:90`）；V1 概念詞 `Select Region`、`Select Date`、`Date`／`MinT`／`MaxT`、六 Region 中文名（`REGION_ORDER` 未改）不變；無 `real-time`／`realtime`／`live`。 |
| **README R-V2-DOC-1 (1)(2)(3)** | PASS | (1) `README.md:375-412`「Taiwan Map modes: Now mode and Forecast mode (V2 Core)」含對照表；Forecast mode 有專屬標題 `:479`「Forecast mode — the Part A bonus map: …」，並自頂端 scope 註記 `:12-16` 直接連結。(2) `:414-421` O-A0001-001 與保守描述（「CWA describes it as hourly data」）。(3) `:441-477` 四步規則、偏好資料原則與所在位置、四個工作範例（Reviewer 手算與之一致）。API 表 `:298` 文件化 `representativeStationIds`。其餘 DOC-1 項目屬 #41 等。 |
| §6.3 **AC-17、AC-18**（Forecast mode 內） | PASS | Executor 檢查（Reviewer 重跑）：六 pill 文字＝`/api/days/<d0>` 的 `derivedMapTemperature` 一位小數、背景色＝該 band；圖例四色＝四 token 並有 derived 說明；以鍵盤選中部地區 pill → 面板 Region／Date／Min／Max／derived＝endpoint；Select Date 七日升序、預設第一天，改第三天 → pill 與面板＝該日 endpoint、pill 畫面位置不變。Reviewer probe 另改到最後一日並點 pill。截圖 `desktop-forecast-ac17.png`（Reviewer 目視：DERIVED 面板、Select Date、六 pill、四段圖例與「not an observed daily mean」）。V1 `REGION_POINTS`、`BAND_COLOURS`、`paintPill`、`tooltipHtml`、Select Date 流程在 diff 中未被改寫。 |
| §6.3 **標題與 masthead** | PASS | 標題逐字不變；lead 改寫為兩種模式描述（R-V2-RSP-4 的 MAY，DR-21.2 先例），概念詞不變。 |
| §6.3 **AC-02／AC-03／AC-24**（Dashboard 側） | PASS | 自動化：`test_dashboard.py`、`test_app.py` 未修改且通過；瀏覽器：`Select Region` 選項＝`/api/regions` 六名稱與順序、表頭 `Date`／`MinT`／`MaxT`、七列＝`/api/regions/北部地區/series`、`Last updated …`＝`/api/health.ingestion_time`；全頁截圖 `desktop-full-page-now.png`、Reviewer 375 全頁截圖同。 |
| §6.3 **AC-10**（Dashboard 側） | PASS | 見 AC-V2-09(a)：預報 503 → 預報區段顯示 V1 error（`role="alert"`＋伺服器訊息），不遮蔽整頁（DV-17）。 |

## 3. Invariants

| INV | 判定 | 證據 |
| --- | --- | --- |
| INV-V2-3 瀏覽器只呼叫 `/api/`、零外部請求 | **HOLDS** | AC-V2-16 列（Reviewer 自行以 request 階段攔截重新擷取，兩模式、兩視野、兩情境皆 0）。 |
| INV-V2-5 兩種語義分開、觀測不聚合 | **HOLDS** | Now 面板標題 `Latest Observation`＋`OBSERVED`、來源句「CWA station observations …, shown as published」；Forecast 面板 `DERIVED`＋「project-derived」；兩者不共用面板、圖例、色階（Now 無色階）。代表標記的 `title`、`aria-label`、tooltip 皆以站名與「station value」「Station value, not a county value」標示（`app.js:627-631`、`:707-723`），面板註記「a station value, not a county temperature」（`index.html:93-96`）；前端不計算任何觀測統計（有效站數取自 API）；無 realtime／live。`representativeStationIds` 是站識別的選取，不是數值、不是聚合（見 §4 關切 2）。 |
| INV-V2-7 三條路徑獨立降級（預報失敗面） | **HOLDS** | AC-V2-09(a) 列；另 `probe2.py` 反向 sanity（#37 範圍，不作判定依據）：觀測 `key_not_configured` 時仍在 Now mode、兩個時間「—」、下方 dashboard 正常、Forecast mode 六 pill 與日期正常。 |
| INV-V2-8 V1 不變量與產物不變 | **HOLDS**（本票範圍） | AC-V2-20 列；H-2 核對段。下方 dashboard 的程式（`loadRegion`／`renderChart`／`renderTable`／`renderSummary`／`?region=`）在 diff 中只有註解或位置變動；`#dashboard` 移入 `#forecast-section` 是 DV-17 明定的 DR-19 範圍收斂。 |
| INV-V2-9 Scope class 分明 | **HOLDS** | 變更只在部署 Dashboard（`static/**`、`observation.py`、新 `representative.py`）；Grading App（`app.py`）與 MVM 產物無 diff；README 標 V2 Core／ENHANCED、dashboard-only。 |
| V1 INV-2 行為對等 | **HOLDS** | `weather_query.py`、`server.py` 無 diff；`test_dashboard.py`／`test_app.py` 的對等測試通過；瀏覽器表格七列＝series endpoint。 |
| V1 INV-7 標示要求 | **HOLDS** | Forecast mode 的 `DERIVED`、「project-derived six-region values」、「(derived, not an observed daily mean)」、圖例「Average = (MinT + MaxT) / 2, a derived value — not an observed daily mean」原樣；README「Data source and labeling」未改。 |
| V1 INV-9 | **HOLDS** | 同 INV-V2-9。 |

## 4. Executor 三項關切的獨立判斷

**關切 1 — AC-V2-01 的「選一縣並縮放後往返」。** 縣選取（R-V2-DD-5／AC-V2-10／12）屬 #38，#38 依賴 #36；因此在 #36 的 subject 上 AC-V2-01 的「選一縣」字面 oracle **無法執行**。本 subject 已存在的 Now 選取狀態（選測站）與視野的往返恢復，Reviewer 以兩種獨立操作驗證 PASS（§2），機制（`nowView`＋模組層級的選取狀態）是通用的。判斷：這不是 #36 的實作缺陷；#36 的 AC-V2-01 義務在本 subject 可觀察的範圍內已滿足。但 derivation record §15 把 AC-V2-01 只分配給 #36，#38 的分配（AC-V2-10、12、16、20、23）不含 AC-V2-01，#41 亦不含；「選縣」往返因此在 Ticket 層沒有一個能觀察到它的 owner，只剩 Spec Integration Audit 兜底。這是 Ticket 分配（contract sufficiency）問題，依治理 §4.2 為 routing signal、不是 blocking finding——見 **R-1**，required authority ＝ **Design Authority**。

**關切 2 — `representativeStationIds` 進入 #35 已結案的觀測回應。**
- (a) **在 #36 的 accepted contract 內**：R-V2-DD-3 只規定 WHAT、機制屬 HOW；Spec §5.2 把「觀測／雷達 `/api/` 的確切路徑、回應欄位名」與「代表測站的具體機制」列為 HOW；R-V2-OBS-3 的成功回應是「至少承載」清單，並要求欄位名在 README 文件化（`README.md:298` 已做）；DV-9 只對「瀏覽器端實作」要求等價自動化證據，隱含伺服器端為預設；AC-V2-11 的 oracle 本身寫「手算並與 `/api/`／畫面一致」，預設選取結果可在 `/api/` 或畫面觀察。
- (b) **未破壞 #35 已稽核的保證**：INV-V2-6——新欄位只在成功路徑、由同一份 `dataset.stations` 純函式計算，與成功 body 一起放入快取（`observation.py:577-591`），重用回傳同一物件，失敗路徑（`ObservationFailure.response()`）不含它，伺服器仍只有「成功（含重用）」與「分類失敗」兩種回應。H-3 在 API 層——欄位內容只是站識別字串的清單，不含任何數值，不改變 `stations[]` 的任何欄位（#35 的全欄位手算測試未改且通過），不是縣值、平均或任何觀測聚合（INV-V2-5）；它也不是預報推導值，沒有預報語義流入觀測回應。精確鍵集合——`test_observation.py:238-242` 仍以 `set(body) == {…}` 精確比對，只新增一個有文件的鍵，沒有放寬為子集或存在性檢查；`assert_no_upstream_structure` 仍通過。規則模組 `representative.py` 無 I/O、無 SQL、無 HTTP client、無金鑰，已加入 no-SQL 集合與憑證掃描清單，不在 `app.py`／`weather_query.py` 的 import closure 內（INV-V2-1 不受影響）。唯一的旁支觀察是呼叫點位於 `latest()` 的例外守衛之外，見 **F-1**（Low）。
- (c) **不是需要 Design Authority 的 boundary／semantic 問題**：理由同 (a)(b)——契約已把欄位與機制交給 HOW，AC-V2-11 預期 `/api/` 可觀察選取，欄位不承載觀測值或推導值。Reviewer 不建議為此 route DA。

**關切 3 — 375 px Now 面板在地圖上方、北部標記重疊。** Reviewer 量測：375×812 首屏地圖只露出約 92 px（地圖 top y≈720），Now 面板在 y 366–709；1280 與 375 的全臺初始視野北部代表標記互相重疊（截圖可見，部分文字不可讀）。判斷：這是 **#39 的合法分配，不是 #36 的缺陷**。依據：地圖為主要內容區的可驗收判準、標記可讀與密度（R-V2-RSP-7）、375 px 底部資訊面（R-V2-RSP-5）都在 AC-V2-14，derivation §15 分配給 #39；#36 對 R-V2-RSP-4 的可驗收部分是標題逐字（AC-V2-23）與模式切換不捲動可見（AC-V2-01），兩者 PASS；375 px 面板堆疊在地圖上方沿用 V1 已接受的版面（V1 Forecast 面板在 < 1180 px 同樣堆疊）。交接事項見第 8 節。

## 5. 測試保留與靜態檢查（只加不減）

- BASE 424 個 test id 全部仍存在；V1 與 #35 既有測試檔沒有斷言被刪除、沒有 skip、沒有門檻降低（逐檔 diff：只有 `test_observation.py` 精確鍵集合加一鍵、`test_static_checks.py` no-SQL 集合加一檔、`test_secrets.py` 掃描清單加六檔）。
- 新增守衛有牙齒：`test_modes_frontend.py` 以函式本體（去註解）斷言載入不經 `/api/health`、模式專屬元素、色彩互斥、切換路徑先 `invalidateSize()`、CONTEXT 逐字；Executor 的 mutation 自驗（worklog V-11）是 self-verification，Reviewer 未採為證據，但 Reviewer 讀過的守衛內容與其描述一致。
- `_ALLOWED_FRONTEND_URLS`、HTTP client 偵測、前端請求形式檢查、SQL owner 檢查皆未變。

## 6. High-risk 核對段（decision A-1；derivation record §6）

本票觸及 **H-2、H-3**（Issue #36 High-risk 段）；另附帶觸及 H-1（`observation.py` 修改、A-3 使用紀錄）。

### H-2 老師指定的介面或資料格式 — 核對結果：**HOLDS**

- **核對了什麼**：頁面文字 `Taiwan Weather Forecast`（`<title>`、`<h1>`）、`Select Region`、`Select Date`、`Date`／`MinT`／`MaxT` 表頭、六 Region 中文名；`app.py`、`streamlit run app.py`、`data.db`、`TemperatureForecasts` DDL、老師兩句 SQL、`requirements.txt`、README 存在；預報 `/api/`。
- **結果**：上列文字在 `index.html` 逐字存在、`REGION_ORDER` 未改（AC-V2-23 列）；瀏覽器取得 `Select Region` 六選項＝`/api/regions` 順序。`app.py`、`weather_query.py`、`ingestion/`、`data.db`、`requirements.txt`、`server.py`、`api/` 在 subject 無 diff（`data.db` blob 相同）。Reviewer 以唯讀連線對 `data.db` 執行 `SELECT DISTINCT regionName FROM TemperatureForecasts;` → **6 列**（北部地區、中部地區、南部地區、東北部地區、東部地區、東南部地區）；`SELECT * FROM TemperatureForecasts WHERE regionName = '中部地區';` → **7 列**（2026-09-24～2026-09-30）；DDL 五欄 `id INTEGER PRIMARY KEY, regionName TEXT, dataDate TEXT, mint REAL, maxt REAL` 不變。預報 `/api/` 由未改動的 `server.py`＋`weather_query.py`＋`data.db` 提供，形狀不變。

### H-3 資料語義與標示 — 核對結果：**HOLDS**

- **核對了什麼**：觀測與推導可見地分開；代表測站標記不被呈現為縣值；Latest Observation 用語；`Fetched Time` 與預報快照取得時間可辨；V1 推導值的單一來源與標示；觀測值「如發布」。
- **結果**：(1) 分開——觀測只在 Now mode（`OBSERVED`、「as published」），推導只在 Forecast mode 與下方 dashboard（`DERIVED`、導出說明），面板／圖例／色階不共用，Forecast mode 無觀測、Now mode 無預報（AC-V2-02 列，瀏覽器 `innerText` 核對）。(2) 代表標記——tooltip、`aria-label`、`title`、面板註記都寫站名與「station value / not a county value」；無縣平均或任何前端觀測聚合；README `:433-439` 同樣聲明。(3) 用語——`Latest Observation`；頁面、`app.js`、README 新增段落無 realtime／live（README 兩處「average」皆為否定句）。(4) `Fetched Time`（Now 面板）與 `Last updated (data fetched from CWA)`（預報控制卡，DR-17 原樣）文字不同、位置相距 > 100 px，README `:397-401` 明文區分。(5) V1 推導單一來源——`test_frontend_does_not_re_derive_or_re_band`、`test_pill_uses_endpoint_value_and_band`、`test_band_colours_match_between_pills_and_legend_tokens` 未改且通過；瀏覽器 pill 值與色＝endpoint。(6) 如發布——標記溫度與面板值以 `/api/` 數值顯示（不四捨五入，只補到一位小數），哨兵欄位為「—」（`probe2.py`）；`representativeStationIds` 不改變任何觀測值（§4 關切 2）。

### H-1（附帶）— 核對結果：**HOLDS**

- `representative.py` 無 I/O／HTTP client／金鑰；`observation.py` 的修改不新增 log 內容、不觸及金鑰讀取；新程式檔已列入 `test_secrets.py`。`python -m tools.credential_scan` → `credential scan passed: 581 tracked files; no .env tracked (only .env.example); no CWA-key-format string in tracked files or committed history; no Authorization value in fixture/raw JSON.`；`git diff 42665e8 dcd697c` 以 `CWA-[0-9A-Za-z]{4,}` 搜尋只命中英文詞 `CWA-free`；已提交的 `browser-check-results.json`／`network-log.json` 無 `Authorization`／`opendata`／`CWA_API_KEY`。Worklog 的 A-3 使用紀錄存在（一次 GET，只印非機密摘要）；Reviewer 未重做即時驗證。

## 7. Findings

### F-1 — 代表測站選取的呼叫點位於 `latest()` 的分類守衛之外

- **Severity**：Low。**Blocking**：否。
- **證據**：`observation.py:549-575` 的 `try … except ObservationFailure … except Exception` 是 #35 為「never let an unclassified error escape」而設的守衛；#36 新增的 `representative.select_representatives(dataset.stations)`（`:587-589`）位於守衛之後。若它拋出例外，`server.py:204` 不會攔截，回應會是 Flask 預設的非 JSON 500，而不是 R-V2-OBS-11 要求的「非 2xx JSON＋`reason`」。
- **為何不是 blocking**：目前不可達。`normalize()` 保證每站 `stationId` 為非空字串、`countyName ∈ COUNTIES`、座標為有限 float；`COUNTY_ORDER` 與 `COUNTIES` 集合相等（`test_preference_data_covers_exactly_the_22_counties`）；規則只做 dict 查找、list append、對非空字串 list 取 `min`。Reviewer 找不到能觸發例外的輸入，契約行為在任何可達輸入下都成立。
- **契約依據**：R-V2-OBS-11（失敗回應形態）；#35 audit 的 INV-V2-6 伺服器面結論所依賴的「三條出口」結構。
- **Disposition**：#36 不需修改。之後若有 Ticket 修改 `representative.py` 或 `observation.py` 的成功 body（例如 #39 同步 `MAP_RANGE`），建議把呼叫移入守衛或保持輸入型別保證。Owner：無需指定（非待辦；屬可選的強化）。

（無其他 finding。）

## 8. Routing signals 與交接事項（不是 finding，不延長本 cycle）

- **R-1 → Design Authority（Ticket 分配／contract sufficiency）**：AC-V2-01 的「在 Now mode 選一縣並縮放後往返 Forecast，回到 Now 時選縣與視野恢復」在 #36 無法執行（縣選取屬 #38）；derivation §15 只把 AC-V2-01 分配給 #36，#38／#41 的分配都不含它。請 DA 決定由哪一張票（例如 #38）在縣選取存在後重驗「選縣往返」，或確認由 Spec Integration Audit 承接。此項不影響 #36 的 closure。
- **交接給 #38**：(a) 往返保留目前保存 `nowView` 與 `selectedStationId`；#38 加入縣選取時須把選縣狀態納入同一往返保存（R-V2-MODE-5(a)）。(b) 目前 Now 面板的「選取測站」區塊是 DD-2 的「可由選取取得站名與縣名」，**未顯示 StationId**；R-V2-DD-7 的測站詳情（含 StationId、氣壓、雨量、風向）由 #38 完成。派工文字中的「no StationId shown」應理解為 R-V2-DD-3(f)「Spec 與 README 不列舉 22 個 StationId」，不是介面禁止顯示 StationId。
- **交接給 #39**：(a) 375×812 首屏地圖只露出約 92 px（Now 面板堆疊在地圖上方），R-V2-RSP-4「地圖為主要內容區」與 R-V2-RSP-5 底部資訊面須在 AC-V2-14 驗收；(b) 1280 與 375 的全臺初始視野北部代表標記重疊、部分文字不可讀（R-V2-RSP-7）；(c) 視窗寬度改變時 `fitToMarkers()` 會把 Now 視野重設為初始視野（worklog 關切 (e)；R-V2-MAP-5 resize 路徑）；(d) 若 #39 改變圍欄範圍 E，`representative.MAP_RANGE` 與 README 規則第 1 步的數字須同步（worklog 關切 (f)），並重驗 AC-V2-11。
- **交接給 #37**：觀測失敗目前只在 Refresh 旁顯示伺服器 `error` 文字、兩個時間維持「—」；Stale／Unavailable、not-newer 告知、前端有界時間屬 #37。

## 9. 結論

#36 分配的 AC（AC-V2-01 可觀察部分、02、03、04、09(a)＋API、11、15、16、20、21(13)、23）、README (1)(2)(3)、§6.3 定向 V1 重驗全部 PASS；INV-V2-3、5、7、8、9 與 V1 INV-2、7、9 成立；H-2、H-3（及附帶 H-1）核對成立。Executor 關切 2 在契約內且未破壞 #35 的保證，不需 DA；關切 3 為 #39 的合法分配；關切 1 以 R-1 交 Design Authority 作 Ticket 分配裁決，不阻擋本票。唯一 finding F-1 為 Low、non-blocking。

VERDICT: CLOSURE
