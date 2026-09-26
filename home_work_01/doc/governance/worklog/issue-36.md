# Worklog — Issue #36 Now mode 與 Forecast mode：預設 Now、模式切換、全臺代表測站的 Latest Observation 與 Observation Time／Fetched Time

- **Work item**：GitHub Issue #36（Formal lane，V2 Core；Blocked by #35——已 CLOSED）
- **Executing role**：`executor`，以 `gov-executor` definition 派工（Bindings §3.1 mapping：`claude-opus-5-5`，effort `high`）。本 session 自述的模型為 Opus 5.5；**這不是 binding 證據**。Binding verification 依 Bindings §3.4 由派工者（Orchestrator）從 harness 紀錄（`subagents/agent-<id>.meta.json` 的 `agentType`、`.jsonl` 的 `message.model`／`effort`）核對並記入 run record 或 audit record；本 worklog 不複製 harness 日誌。
- **Branch**：`home_work_01-v2-implementation`；**BASE ＝ `42665e8`**（#35 CLOSE 的 run-record commit）
- **Subject**：**code anchor ＝ `f63ebb1`**（BASE..`f63ebb1` 為本票全部產物變更）；本 worklog 為其後的 record-only commit（`doc/governance/**`，Bindings §7 P7）
- **開始／本次更新**：2026-09-26

## Contract reference

- **Outcome Contract**：`home_work_01/doc/governance/outcome-contract-v2.md`（ACCEPTED 2026-09-25；normative candidate `69c5a04`）——§4 **A-3**（實作期金鑰使用，本票用於一次定向即時驗證，見 V-13）；A-4 未使用。
- **Spec**：`home_work_01/doc/spec/SPEC-V2.md` **v2.2**（以參照繼承 V1 Spec v1.1）——§1.2 Δ-5／Δ-7／Δ-14；§2.1 R-V2-MODE-1～6；§2.2 R-V2-OBS-4(c)、OBS-7(a)(b)(c)；§2.3 R-V2-DD-2、DD-3、DD-10；§2.5 R-V2-DEG-1、DEG-3、DEG-5（前端面）；R-V2-MAP-5（模式切換路徑）；R-V2-RSP-4；§2.8 R-V2-DOC-1(1)(2)(3)、DOC-4、DOC-5；R-V2-TC-4；§5.3 儀器（初始視野 `fitBounds` 範圍、圍欄範圍 E）；§6.3。V1：AC-17、AC-18、AC-02、AC-03、AC-10、AC-24；DR-17（不變）、DR-19（條件→狀態規則不變，範圍收斂）、DR-20／DR-21。
- **Derivation record**：`home_work_01/doc/governance/decisions/derivation-SPEC-V2.md` DV-8、DV-9、DV-14、DV-17、DV-18；§6（H-2／H-3 的 V2 適用；A-1）；§15（本票分配）。
- **High-risk decision**：`home_work_01/doc/governance/decisions/decision-20260923-high-risk-categories.md`（A-1：R1 record 須明記核對段；下方「High-risk 核對材料」提供入口）。
- **Brief**：`home_work_01/doc/brief/BRIEF-V2.md` §9（詞彙 delta，逐字併入 `CONTEXT.md`）；附錄 A 為非契約建議，未作為需求。
- **Ticket 分配（#36）**：AC-V2-01、02、03（瀏覽器抽樣＋哨兵「—」）、04（瀏覽器 success 面）、09(a)＋API 面、11、15（本票範圍）、16（本票範圍：執行期 network log）、20（本票範圍）、21(13)、23（`Back to Taiwan` 除外）；README R-V2-DOC-1 (1)(2)(3)；§6.3 定向 V1 重驗 AC-17、AC-18、標題與 masthead、AC-02／AC-03／AC-24（Dashboard 側）、AC-10（Dashboard 側）。INV-V2-3、5、7（預報失敗面）、8、9；V1 INV-2、7、9。
- **契約變更**：無。未修改任何 requirement、AC、invariant、gate、oracle。

## Decisions and assumptions（HOW；Spec §5.2 委派）

1. **單一 Leaflet 地圖、兩個 layer group**：Forecast mode 的六個 Region pill 放在 `forecastLayer`、Now mode 的代表測站標記放在 `nowLayer`；任一時刻只有目前模式的 group 在地圖上（Forecast 的 pill 在 Now mode 不存在於 DOM）。底圖兩模式共用。V1 的 pill 行為、`REGION_POINTS`、`BAND_COLOURS`、`paintPill`／tooltip、Select Date 流程原樣保留；pill 的 `add` handler 在每次 layer 被加回時對新元素重新綁定，進入 Forecast mode 後以 `latestDay` 重新上色。
2. **模式歸屬**：模式專屬元素帶 `data-mode="now"`／`"forecast"`，`renderModeChrome()` 只顯示目前模式者；Forecast 的 inline status（DR-19）以狀態保存、只在 Forecast mode 顯示，Now mode 的地圖永不被預報狀態覆蓋。
3. **模式切換控制**：兩個 `<button type="button">`（`aria-pressed`、`role="group"`），可見文字「Now · Latest Observation」「Forecast · 7-day」；≤ 560 px 時後綴以 visually-hidden 保留於 accessible name，可見文字仍含 `Now`／`Forecast`。放在地圖卡片標題列（兩個驗證視野不捲動即可見）。原生 button：Tab 可達（頁面第一個 Tab 停點）、Enter／Space 啟動。
4. **往返保留（DV-8）**：離開 Now mode 時存 `nowView`（center＋zoom）；回 Now 時 `setView` 恢復；Now 的選取（選中的代表測站）保存在 `selectedStationId`，標記重建時重新套用。進入 Forecast mode：若六個 Region 點都落在「地圖容器扣除 Forecast 面板 padding」的清空區，保留視野；否則 `fitToMarkers(六點 bounds ∪ 目前清空區)`——只擴大到包含六點（「最小調整」），不重設為任意預設視野。
5. **`fitBounds` 單一呼叫點維持**：V1 靜態守衛要求 `fitBounds(` 全檔只出現一次且在 `fitToMarkers` 內、`invalidateSize()` 在其前。`fitToMarkers(bounds)` 泛化為「目前模式的初始視野或給定 bounds」；`initMap` 仍呼叫 `fitToMarkers()`。Forecast mode 的 padding 值與 V1 相同；Now mode 初始視野用 §5.3 儀器 `fitBounds` 範圍（lon 119.25–122.05、lat 21.85–25.35）。
6. **初始化守衛（R-V2-MAP-5）**：頁面載入、資料到達、模式切換都經同一個 `bringUpMap()` → `ensureMapSized(function …)`；`ensureMapSized` 的守衛原樣，只在觸發時重設 `mapInitScheduled`（使之後再次 0×0 時仍可排程）。延後的步驟讀取「目前狀態」（`syncMap()`），所以排程期間被丟棄的呼叫不會遺失狀態。模式切換分支先 `map.invalidateSize()` 再做任何 `removeLayer`／`setView`／fit。
7. **代表測站規則（DV-9；伺服器端實作）**：新增純函式模組 `representative.py`：候選＝該縣的有效測站且座標在地圖範圍（§5.3 E：lat 21.2–26.7、lon 117.6–122.9，含邊界）；偏好站為候選則選之；否則取 `stationId` 字元碼最小者；無候選則無標記。偏好資料 `PREFERRED_STATION`（22 筆，HOW data、非契約）：縣治所在或以縣／縣治命名的平地測站，有 CWA 有人站則用之，否則用縣治鄉鎮的自動站。選擇伺服器端的理由：規則可在 CI 以 pytest 離線對樣本與衍生樣本驗證（AC-V2-11），`/api/` 回應直接帶結果（`representativeStationIds`）供讀者依 README 手算核對。範圍外測站（例如高雄市東沙島 lon 116.73）永不為代表——它不會被放上臺灣地圖（與 DD-11 一致；DD-11 的清單／詳情行為屬 #38）。
8. **API 附加欄位**：成功回應新增頂層 `representativeStationIds`（依固定縣序排列的 list）。#35 的 `test_response_carries_no_upstream_structure` 以**精確鍵集合**斷言成功回應，已把此鍵加入該集合（仍為精確比對，未放寬）；測站物件本身未改（#35 的手算全欄位相等測試不受影響）。`server.py` 未修改。
9. **Now mode 資料流**：`loadObservation()` 在 `DOMContentLoaded` 直接呼叫，與預報 `bootstrap()` 平行、互不等待（R-V2-DEG-1）。`Refresh` 為 `<button>`，文字逐字 `Refresh`；進行中以 `aria-disabled`（不用 `disabled`，避免鍵盤焦點遺失）＋ `aria-busy`＋spinner＋「Refreshing the Latest Observation…」表示，進行中再按被忽略。成功時若回應的 dataset Observation Time 較目前顯示者舊則不套用（INV-V2-6；「已是最新」告知屬 #37）。
10. **失敗的暫時呈現（#37 之前）**：觀測失敗時保留已顯示資料、在 Refresh 旁顯示伺服器的非機密 `error` 文字；尚無資料時兩個時間維持「—」。Stale／Unavailable 的標示、三種 Refresh 結果、前端有界時間屬 #37，本票未實作其語義。
11. **時間顯示**：Observation Time 顯示到分、Fetched Time 顯示到秒，皆附發布字串中的 UTC offset（例如 `2026-09-25 23:00 +08:00`）；只重新排版字串，不經瀏覽器時鐘或時區轉換。
12. **標記呈現（H-3）**：代表測站標記為中性淺色圓角矩形（`--obs-pill-*`，與四段導出色帶的顏色互斥，靜態守衛與瀏覽器檢查皆核對），文字為該站氣溫（`/api/` 值，至少一位小數、不四捨五入）；標記下方顯示測站名（zoom ≥ 8）；hover／focus 的 tooltip 與 aria-label 為「<站名> station, <縣>…station value」，永不寫成縣的氣溫。Now mode 無色階、無圖例（觀測圖例「若有」條款不觸發）。
13. **選取的測站區塊**：顯示站名、縣・鄉鎮、氣溫、相對濕度、風速、天氣現象、該站 Observation Time；缺值／哨兵顯示「—」。未顯示 StationId（測站詳情契約 R-V2-DD-7 屬 #38）。
14. **DR-19 範圍收斂（DV-17）**：`#page-error`／`#page-loading`／`#page-empty`／`#dashboard` 移入 `#forecast-section`（地圖卡片之下），條件→狀態規則與 V1 文字不變；bootstrap 失敗時另在 Forecast mode 地圖顯示同一伺服器訊息（`role="alert"`）並停用 Select Date；regions 為空時同理顯示 empty。
15. **DR-17 標籤不變（DV-18）**：下方 `Last updated (data fetched from CWA): …` 原樣；Now mode 的 `Fetched Time` 在地圖的 Now 面板內，文字與位置皆不同。
16. **Masthead**：`<h1>`／`<title>` 逐字 `Taiwan Weather Forecast` 不變；lead 改寫為描述兩種模式（DR-21.2 先例，R-V2-RSP-4 MAY）。
17. **CONTEXT.md**：BRIEF-V2 §9 十個詞條逐字併入（定義與「避免」原文）；原「Refresh」詞條改名「Re-ingestion」並改為 BRIEF 原文；「Taiwan Map」改為 BRIEF 原文，新增 Now mode、Forecast mode；新增「Latest Observation (V2)」區段放其餘六詞。以測試逐字比對（`test_context_glossary_delta_is_verbatim`）。其他詞條未改（#41 做最終文件審查）。
18. **README**：新增「Taiwan Map modes: Now mode and Forecast mode (V2 Core)」（含兩模式對照表、語義分開、Fetched Time 與 Last updated 的差異、往返保留、獨立降級、零外部請求）、「Now mode — Latest Observation」（來源 O-A0001-001 與保守的逐時描述、面板、Refresh、標記）、「Representative station rule」（四步手算規則、偏好資料的原則與位置、四個工作範例；不列舉 22 個 StationId——測試限制 README 中偏好 ID ≤ 4、Spec 中 0）；原「Taiwan Map and `Select Date`」段改為專屬標題「Forecast mode — the Part A bonus map: six-region Taiwan Map and `Select Date`」並自頂端 scope 註記直接連結；API 表加 `representativeStationIds`；測試段加新測試。其餘 R-V2-DOC-1 項目（(4)～(11)）不在本票。
19. **瀏覽器驗證工具**：`tests/check_modes_browser.py` 以 DevTools protocol（`websocket-client`）驅動本機 headless Chrome；伺服器為未修改的 `create_app`，觀測上游以樣本衍生的模擬回應提供（無金鑰、無網路）。oracle 一律取頁面實際收到的 `/api/` 回應本文。命名為 `check_*`，不被 pytest 收集（沿用 `check_series_error_visible.py` 慣例）。`websocket-client` 不在 `requirements.txt`（本機 venv 另裝；CI 不跑此檢查），未為此修改 `requirements.txt`。

## Artifacts（code anchor `f63ebb1`；BASE `42665e8`）

| 檔案 | 動作 |
| --- | --- |
| `home_work_01/representative.py` | 新增：代表測站規則（`COUNTY_ORDER`、`MAP_RANGE`、`PREFERRED_STATION`、`select_representatives`） |
| `home_work_01/observation.py` | 修改：成功回應加 `representativeStationIds`；docstring |
| `home_work_01/static/index.html` | 修改：模式切換、Now 面板、Forecast 面板／圖例標 `data-mode`、預報區段 `#forecast-section`、masthead lead |
| `home_work_01/static/app.js` | 修改：模式狀態與切換、`bringUpMap`／`syncMap`、Now mode 觀測載入／Refresh／標記／選取、預報區段層級狀態、Forecast inline status 依模式顯示；圖表／表格／摘要程式未變 |
| `home_work_01/static/styles.css` | 修改：模式切換、Now 面板、測站標記、`--toggle-*`／`--obs-pill-*` token、地圖卡標題列對齊 |
| `home_work_01/tests/test_representative.py` | 新增：11 個測試 |
| `home_work_01/tests/test_modes_frontend.py` | 新增：18 個靜態守衛（含 CONTEXT 詞彙逐字） |
| `home_work_01/tests/check_modes_browser.py` | 新增：可重現的瀏覽器檢查（37 項） |
| `home_work_01/tests/test_observation.py` | 修改：成功回應精確鍵集合加入 `representativeStationIds`（一行＋註解） |
| `home_work_01/tests/test_static_checks.py` | 修改：`representative.py` 加入 no-SQL／no-`sqlite3` 集合（只加） |
| `home_work_01/tests/test_secrets.py` | 修改：新程式檔加入憑證掃描清單（只加） |
| `home_work_01/CONTEXT.md` | 修改：BRIEF-V2 §9 詞彙 delta 逐字併入 |
| `home_work_01/README.md` | 修改：見決定 18 |
| `home_work_01/doc/acceptance/screenshots/v2/issue-36/*` | 新增：15 張截圖、`browser-check-results.json`、`network-log.json`（由 `check_modes_browser.py` 產生） |

未修改：`app.py`、`weather_query.py`、`ingestion/**`、`data.db`、`server.py`、`api/**`、`smoke.py`、`vercel.json`、`requirements.txt`、`.github/workflows/**`、`doc/requirement/**`；單元目錄外無變更（RB-5）。

## Verification

環境：Windows 11，`home_work_01/.venv` Python 3.12.14；Chrome 153（headless，DevTools protocol）；Node 只用於 `node --check static/app.js` 語法檢查。以下「subject」皆指 working tree ＝ `f63ebb1`。

- **V-1 全套（subject）**：`python -m pytest -q` → **459 passed**（BASE 424 ＋ 35：`test_representative.py` 11、`test_modes_frontend.py` 18、`test_secrets.py` 參數化 ＋6）。全離線。
- **V-2 V1／既有測試保留（quality floor）**：以腳本比對 BASE `tests/` 全部 197 個 `test_*` 函式在 subject 皆存在（missing: []）；`git diff 42665e8 -- tests/` 對既有測試檔的刪除行只有兩行：`_NON_SHARED_PYTHON` 定義行（改為加入 `_REPRESENTATIVE`）與 #35 精確鍵集合的最後一行（加入 `representativeStationIds`，仍為精確比對）；無斷言刪除、無 skip、無門檻降低。V1 `test_map_frontend.py` 的四個初始化／單一 fit 守衛與 `test_dashboard.py` 未修改且通過。
- **V-3 CI**：push `f63ebb1` 後既有 workflow「home_work_01 CI」run **`36168995238`**（ubuntu，Python 3.12）**success**：`459 passed in 10.74s`；`credential scan passed: 580 tracked files …`。Workflow 檔未修改（A-4 未使用）。
- **V-4 憑證**：`python -m tools.credential_scan`（staged 後）→ passed（580 tracked files，無 `.env`）；以腳本讀 `.env`（不印出）比對 `git diff --cached` 全文（199,937 bytes）→ 金鑰字面 **False**。
- **V-5 瀏覽器檢查（`python tests/check_modes_browser.py`）→ 37/37 PASS**，證據 `home_work_01/doc/acceptance/screenshots/v2/issue-36/`（`browser-check-results.json` 記每項觀察值）。情境 A（預報正常）與 B（`db_path` 指向不存在的檔，`/api/health` 503），各在 1280×900 與 375×812（mobile emulation）：
  - AC-V2-01：載入即 Now（`aria-pressed`、面板，任何動作之前取樣；B 情境同樣）；切換控制兩視野皆在初始視窗內（`scrollY` 0、rect 在 `innerHeight` 內）、文字含 `Now`／`Forecast`；頁面第一個 Tab 停點為 `mode-now`；以鍵盤 Enter 切 Forecast、Space 切回；Forecast 六個 pill 皆在地圖容器內；Now 選 臺北 站＋放大一級＋鍵盤平移後往返，所有 22 個 Now 標記的畫面座標完全相同、選取恢復（`is-active` 1 個、面板仍為 臺北 station）。
  - AC-17 重驗（Forecast mode 內）：六 pill 文字＝`/api/days/<d0>` 的 `derivedMapTemperature` 一位小數、背景色＝該 band 色；圖例四色＝四 token、含「derived value」說明；以鍵盤選 中部地區 pill → 面板 Region／Date／Min／Max／derived 等於 endpoint。AC-18：Select Date 七日升序、預設第一天；改為第三天 → pill 文字／顏色與面板等於該日 endpoint，六 pill 畫面位置不變（視野未重設）。
  - AC-V2-02：Now mode 的地圖區無 `Select Date`／`Derived map temperature`／`DERIVED`、無 Forecast pill；Forecast mode 的地圖區無 `Refresh`／`Observation Time`／`Fetched Time`／`Latest Observation`、無測站標記；觀測標記的計算背景色與四個 band 色無交集；全頁 `innerText` 無 `real-time`／`realtime`／`live`；`#ingestion-time` 為 `Last updated (data fetched from CWA): <health.ingestion_time>`、在 `#forecast-section` 內，`#obs-fetched` 在 Now 面板內，兩者垂直距離 > 100 px；下方 `#dashboard` 的 `innerText` 在兩模式完全相同。
  - AC-V2-03（瀏覽器）：22 個標記的文字全部等於頁面收到的回應中該代表站 `airTemperature`、標記名＝`stationName`、每縣一個；選取 臺北（模擬回應中其相對濕度 `-99`、天氣 `X`）→ 回應為 `null`，畫面顯示「—」，氣溫 `27.1 °C`、測站 Observation Time 等於回應。
  - AC-V2-04（瀏覽器 success 面）：`<dt>` 逐字 `Observation Time`、`Fetched Time`；值等於回應 `observationTime`（到分）與 `fetchedTime`（到秒）；有效測站數等於 `validStationCount`；Refresh 後（上游改為下一小時）兩個時間與 臺北 氣溫更新為新回應的值。
  - OBS-7(a)(c)(e)：Refresh 進行中（上游延遲 1.5 s）`aria-disabled="true"`、`aria-busy="true"`、spinner＋「Refreshing…」可見（截圖 `desktop-now-refresh-in-progress.png`）；進行中再按 Enter → 只有 1 次 `/api/observations/latest` 請求。
  - AC-V2-09(a)：B 情境兩視野——Now mode 22 標記、兩個時間、切換皆可用；`#page-error` 可見、`role="alert"`、文字＝伺服器 `error`（`The forecast database is missing. Run the ingestion pipeline to create it.`）、位於 `#forecast-section`、`#dashboard` 隱藏；地圖卡片可見（非整頁遮蔽）；Refresh 在預報 503 下仍成功；切到 Forecast mode → 地圖 inline error 可見、`role="alert"`、文字＝同一伺服器訊息、Select Date 停用、Forecast 面板可見；切回 Now → inline error 不覆蓋地圖。
  - AC-V2-15（本票範圍）：模式切換後（兩視野）所有 `.leaflet-marker-icon` 的 transform 無 `NaN`、box 非 0×0；console 無例外、無 `NaN`／`Invalid LatLng` 訊息。
  - AC-V2-16（執行期 network log）：兩情境共 46 個瀏覽器請求全部為 `http://127.0.0.1:<port>/…`（頁面、`/static/`、`/api/`、`favicon.ico`）；**外部請求 0**（`network-log.json`）。Radar 顯示中的 log 屬 #40。
  - §6.3 AC-02／AC-03／AC-24（Dashboard 側）：標題、`Select Region` 標籤、選項＝`/api/regions` 六名稱與順序、表頭 `Date`／`MinT`／`MaxT`、七列等於 `/api/regions/北部地區/series`；全頁截圖 `desktop-full-page-now.png`。自動化面：`test_dashboard.py`、`test_app.py` 未修改且通過。
- **V-6 AC-V2-11**：`tests/test_representative.py`——樣本：22 縣各恰一站、皆為有效站、依固定縣序；手算期望（臺北市 `466920`、新竹市 `C0D660`、嘉義縣 `C0M680`、高雄市 `467441`、連江縣 `467990`）且全部 22 縣取得偏好站；重複執行與輸入順序改變（反序、依名稱排序）結果相同；衍生樣本把臺北市、南投縣、嘉義縣、高雄市的偏好站氣溫設為 `-99` → 各自後備到手算的 `466910`、`42HA10`、`467530`、`72V140`（東沙島 `468100` 有效但在範圍外，不被選），其餘 18 縣不變；連江縣全部無效 → 無代表、其餘 21 縣不變；偏好資料恰涵蓋 22 縣且在樣本中皆為有效、在範圍內、屬該縣；README 中偏好 ID ≤ 4（實為 1）、Spec 中 0；`/api/` 回應的 `representativeStationIds` 等於規則重算。
- **V-7 AC-V2-21(13)**：`test_context_glossary_delta_is_verbatim` 自 BRIEF-V2 §9 解析 10 列，逐一比對 `CONTEXT.md` 的「**詞**:\n定義\n_Avoid_: …」完全相等；舊「Running Ingestion again」定義已不存在。
- **V-8 AC-V2-23（本票範圍）**：`test_verbatim_labels`（`Observation Time`、`Fetched Time`、`Refresh`、`Latest Observation`、`Taiwan Weather Forecast`、`Select Region`、`Select Date`、`Date`／`MinT`／`MaxT`、六 Region 中文名）、`test_mode_switch_is_two_labelled_buttons`（`Now`／`Forecast`）、`test_no_real_time_or_live_wording`。`Back to Taiwan` 屬 #38。
- **V-9 AC-V2-16 靜態**：既有 `test_static_checks.py` 全部通過（前端請求形式字面目標只為 `/api/`、`/static/`；絕對 URL 白名單未變；`representative.py` 納入 no-SQL 集合）。
- **V-10 AC-V2-20（本票範圍）／H-2**：`git diff --stat 42665e8 -- app.py weather_query.py ingestion/ data.db smoke.py vercel.json requirements.txt server.py api/ ../.github/workflows/` → 空；`data.db` blob `687586991ce3654e8b336b5b0a1616e98aa83a66` ＝ BASE blob。預報 `/api/` 程式（`server.py`）未變。
- **V-11 自我驗證：mutation checks**（scratchpad `mutations.py`：暫時修改、跑 `test_modes_frontend.py`＋`test_map_frontend.py` 與瀏覽器檢查、以 sha256 確認還原；非正式 audit）：M1 回 Now 不恢復視野 → 靜態 1 失敗＋瀏覽器 1；M2 Now mode 不在載入時自行取觀測 → 靜態 1（守衛修正後）＋瀏覽器 3；M3 導出圖例在 Now mode 可見 → 靜態 2＋瀏覽器 2；M4 模式切換路徑移除 `invalidateSize()` → 靜態 1（瀏覽器同尺寸下無可觀察差異，由靜態守衛承擔）；M5 回 Now 清除選取 → 瀏覽器 1；M6 預報失敗隱藏整個地圖卡 → 瀏覽器 6；M7 測站標記改用 band 色 → 靜態 1＋瀏覽器 1（瀏覽器色彩檢查為此新增）；M8 進行中不忽略 Refresh → 靜態 1＋瀏覽器 1。每個 mutation 至少被一層抓到。首輪發現 M2 的靜態守衛被 Refresh listener 內的呼叫滿足、M7 瀏覽器無色彩斷言，兩者已補強並重跑確認。
- **V-12 README 實跑（本票段落）**：`python server.py` 本機啟動、頁面預設 Now mode（V-13）；瀏覽器檢查以同一 `create_app` 驅動 README 描述的兩模式行為。
- **V-13 A-3 定向即時驗證（本機）**：scratchpad `live_rep_check.py` 以 `python server.py` 啟動（子行程環境先移除 `CWA_API_KEY`，金鑰只能來自單元 `.env`），請求 `/api/observations/latest` **一次**後終止：200（0.44 s；`observationTime` 2026-09-26T01:00:00+08:00、`fetchedTime` 2026-09-26T01:43:36+08:00、有效 840／876）；`representativeStationIds` 22 筆、22 個不同縣、等於規則重算、**22 縣皆為偏好站（無後備）**；回應與伺服器 log（8 行）中金鑰字面 **False**、金鑰格式 **False**、`opendata.cwa.gov.tw` **False**。
- **未執行／限制**：preview 部署驗證屬 #41；Stale／Unavailable／not-newer 與前端有界時間屬 #37；縣下鑽、`Back to Taiwan`、County 選取的往返屬 #38；圍欄、底部資訊面、44×44、768 px、resize 路徑屬 #39；Radar 屬 #40。瀏覽器檢查不在 CI（需 Chrome 與 `websocket-client`），由 Reviewer 於本機重現。

### A-3 金鑰使用紀錄

| # | 時間（+08:00） | 目的 | 動作 | 上游 GET 次數 | 輸出 |
| --- | --- | --- | --- | --- | --- |
| 1 | 2026-09-26 01:43:36 | (ii) 對已接受的 V2 資料路徑做定向即時驗證（代表測站規則對當期真實資料） | V-13 | 1 | 只印非機密摘要與布林檢查 |

無輪詢、無壓測、未印出或匯出金鑰；未觸及 Vercel（RB-3）；CI 與自動化測試不依賴金鑰或網路。瀏覽器檢查與全部自動化測試使用樣本衍生的模擬上游。scratchpad 腳本不在 repo。

## High-risk 核對材料（decision A-1；供 R1 明記核對段）

- **H-2（老師指定的介面）**：`<title>`／`<h1>` 逐字 `Taiwan Weather Forecast`；`Select Region`、`Select Date` label、`Date`／`MinT`／`MaxT` 表頭、六 Region 中文名（`REGION_ORDER`、`/api/regions`）不變——`test_dashboard.py::test_index_page_has_visible_teacher_text`、`test_modes_frontend.py::test_verbatim_labels`、瀏覽器 AC-02／03／24 項。`app.py`、`weather_query.py`、`data.db`（blob 相同）、`requirements.txt`、預報 `/api/` 未變（V-10）。
- **H-3（資料語義與標示）**：觀測值只在 Now mode、標為 Latest Observation／CWA station observations as published／`OBSERVED`；預報值只在 Forecast mode 與下方 dashboard、維持 `DERIVED` 與導出說明；兩者不共用面板、圖例或色階（Now 無色階；顏色互斥由靜態與瀏覽器檢查核對）；代表測站標記以站名標示、tooltip／aria-label 寫「station value, not a county value」，無縣平均或任何觀測聚合（前端不計算任何觀測統計；有效測站數為 API 值）；無 `real-time`／`realtime`／`live`；`Fetched Time` 與 DR-17 `Last updated (data fetched from CWA)` 文字與位置皆不同。README 對應段落見決定 18。V1 推導語義（`weather_query.py`、pill 值與色帶單一來源）未變——`test_map_frontend.py::test_frontend_does_not_re_derive_or_re_band`、`test_pill_uses_endpoint_value_and_band` 仍通過。
- **H-1（附帶觸及：`observation.py` 與 A-3）**：新欄位由純函式計算、不含上游內容；`representative.py` 無 I/O、無 HTTP client、無金鑰；新程式檔納入憑證掃描（`test_secrets.py`）；V-3、V-4、V-13。
- **Diversity**：Executor 與 Primary Reviewer 同為 `claude-opus-5-5` 時，audit record 記 `diversity_lost`（Bindings §5）。

## Audit status

- **Required**：Formal mandatory independent audit（治理 §4.1；Bindings §5）。R1 待 Orchestrator 以 fresh `gov-primary-reviewer` 派工（Bindings §3.5）。本 worklog 的 mutation checks 與瀏覽器檢查皆為 Executor self-verification，**不是**正式 audit。
- **Records**：尚無。

## Remaining work

1. **正式 audit**：R1（Orchestrator 派工）。
2. **Concerns（交有權角色判斷；Executor 未自行裁決）**：
   - (a) **AC-V2-01 的「選一縣並縮放後往返」**：縣選取由 #38 建立。本票以通用機制（`nowView`＋Now 選取狀態）實作往返保留，並以「選代表測站＋放大＋平移」驗證；縣選取的往返在 #38 加入縣選取後才可觀察。是否由 #38 重驗此項，屬 Ticket 分配判斷——**authority：Design Authority**（若 Reviewer 認為需裁決）。
   - (b) **跨票修改 #35 已稽核的產物**：`observation.py` 成功回應新增一個衍生欄位，並把 #35 的精確鍵集合測試加上該鍵（決定 7、8）。未改變 #35 的任何既有欄位或行為；提請 Reviewer 在 R1 一併核對。
   - (c) **375 px 版面**：Now 面板沿用 V1 在 < 1180 px 堆疊於地圖上方的做法，375 px 首屏只見地圖頂端；模式切換不捲動可見（PASS）。地圖為主要內容區（R-V2-RSP-4 的完整意義）、底部資訊面屬 #39。
   - (d) **全臺視野的標記密度**：初始 zoom 下北部代表標記互相重疊；密度管理（R-V2-RSP-7）屬 #39。
   - (e) **視窗寬度改變時的 re-fit**：沿用 V1 規則（寬度改變 → 重新 fit 目前模式的初始視野），Now mode 的使用者視野會被重設；resize 路徑屬 #39（R-V2-MAP-5 resize）。
   - (f) **代表測站範圍 E**：`representative.MAP_RANGE` 使用 §5.3 儀器值；#39 若改變圍欄範圍 E，應同步此常數（README 規則第 1 步的數字亦同）。
3. **後續票**：#37（Refresh 三結果、Stale／Unavailable、前端有界時間、觀測失敗面）、#38（縣下鑽、測站詳情含 StationId、`Back to Taiwan`、DD-11 清單）、#39、#40、#41（README 其餘 DOC-1 項目、V2 驗收文件、preview）。
