# Audit record — Issue #37，cycle 1，R1（Formal Ticket independent audit）

| 欄位 | 內容 |
| --- | --- |
| Work Contract | GitHub Issue **#37**（`yotsubamomo/aiot-classwork`）「Refresh 與狀態語義：newer／not-newer／failure、Stale／Unavailable、觀測失敗只影響 Now mode」。上位：V2 Outcome Contract `home_work_01/doc/governance/outcome-contract-v2.md`（ACCEPTED 2026-09-25，normative candidate `69c5a04`）；Delta Spec `home_work_01/doc/spec/SPEC-V2.md` **v2.2**（§2.2 R-V2-OBS-7／8／10／12（使用者可見層）／13（前端面）、§2.5 R-V2-DEG-2、R-V2-MODE-6(c)、§5.3 有界時間儀器 30 s、§4 INV-V2-6／7）；derivation record `derivation-SPEC-V2.md`（DV-4、DV-5、DV-6、DV-7、§15）；`decision-20260923-high-risk-categories.md`（A-1）。本票分配：AC-V2-06（瀏覽器 (a)～(f)）、AC-V2-08、AC-V2-04（瀏覽器 stale／unavailable 面）、AC-V2-09(b)、AC-V2-20（本票範圍：CI 全綠）；AB-V2-3、4、5（部分）；§6.3 定向 V1 重驗：無。Out of scope：#35 伺服器端、#38 縣脈絡在各狀態下的內容、#40 Radar 狀態、可選年齡提示。 |
| 受審 subject | branch `home_work_01-v2-implementation`；BASE **`d3e7f4c78fab80453236b61854691c578e39b313`** .. HEAD **`37edd5ff2bb177cebc39ff443299436f61aa1f68`**；code anchor **`7a3b4694987ebe8477e58600daafaf8359aa89f3`**。`7a3b469..37edd5f` 只有 `doc/governance/worklog/issue-37.md`；`37edd5f..c4f5475`（目前 `origin` 與本機 HEAD）只有 run record——兩者皆 record-only（Bindings §7）。`d3e7f4c..7a3b469` 的 41 檔全部在 `home_work_01/` 內（單元目錄外 0 檔、`doc/requirement/` 0 檔）。Working tree 的 code 與 `7a3b469` 相同。 |
| Audit 種類 | **R1**（Formal 必做的 Ticket independent audit；治理 §4.1、§4.4），**cycle 1**。不是 Spec Integration Audit。 |
| 角色 | `primary_reviewer`（definition `gov-primary-reviewer`；Bindings §3.1 mapping `claude-opus-5-5`／`xhigh`） |
| Binding 證據 | 正式核對由派工者（Orchestrator）依 Bindings §3.4 記入 run record `home_work_01/doc/governance/run/run-20260925-hw01-v2-formal.md`（#37 Executor 列已記 `a85fb9fb98d937131`）。Reviewer 另以 Bindings §3.4 指令讀 harness 紀錄（session `05b8408b-260a-46d3-a4fe-ec07e3ec365a`）自行觀察：`agent-a00dc725e9833283f` `gov-primary-reviewer` `[('claude-opus-5-5', 'xhigh')]`（本 Reviewer；第一則訊息即本次 #37 R1 派工）；`agent-a85fb9fb98d937131` `gov-executor` `[('claude-opus-5-5', 'high')]`（#37 Executor）。兩者皆與 Bindings §3.1（b2 override）一致。此觀察只供對照，不取代派工者的核對。 |
| Independence（治理 §2.3、§4.6） | (1) **Fresh context**：未繼承 Executor 對話；worklog `issue-37.md`、commit message、已提交的截圖與 `browser-check-results.json`／`network-log.json` 一律當作待驗證主張。(2) **Binding**：見上一列。(3) **Autonomous access**：自讀 `gh issue view 37`（及 #38、#39、#41 以判斷交接）、SPEC-V2 v2.2、derivation record（DV-4～7、§15）、decision A-1、DV-20、#35／#36 audit records、git 歷史與 diff、CI run 與 log；以 `git archive d3e7f4c` 匯出 BASE 到 Reviewer scratchpad 比對 test id；重跑 Executor 的 `check_refresh_browser.py`、`check_modes_browser.py`（輸出導向 scratchpad，不覆寫已提交證據）與 V1 `check_series_error_visible.py`；另**自寫** probe（`probe37.py` 與三個後續 `probe37b／c／d.py`，皆在 scratchpad、未提交）：自己的 CDP driver、以 `Fetch.enable {urlPattern:"*", requestStage:"Request"}` 在 request 階段攔截**全部**瀏覽器請求（非 loopback 一律 `failRequest` 並記錄）、自己的上游模擬與哨兵金鑰、自己的 oracle。(4) **Self-written record**：本紀錄由 Reviewer 以自己的 Write 工具寫入。**Model diversity：`diversity_lost`**——Executor 與 Primary Reviewer 同為 `claude-opus-5-5`（Bindings §5、b2 override；decision A-7）。這是合法狀態，不減損 §2.3 的 independence。 |
| 日期 | 2026-09-26 |

## 1. 審查方法與環境

- **環境**：Windows 11；`home_work_01/.venv` Python 3.12.14；Chrome headless（DevTools protocol，`websocket-client` 1.9.2，venv 內既有）。
- **Reviewer 對憑證的處理**：Reviewer **沒有讀取** `home_work_01/.env`，沒有發出任何 CWA 請求。Probe 以未修改的 `server.create_app(db_path=None, observation_service=…)` 在 loopback 以 threaded WSGI server 執行，觀測服務為真的 `observation.LatestObservationService`（可控時鐘、重用視窗 600 s、`env={"CWA_API_KEY": "RVW-SENTINEL-KEY-7f3a9c-r1"}`），上游為 Reviewer 自寫的模擬（由已提交樣本 `tests/fixtures/O-A0001-001_sample.json` 把全部 876 站的 `ObsTime` 平移 −2～+5 小時；失敗模式把哨兵金鑰、上游主機與本文標記塞進例外訊息與回應本文）。Flask `app.debug = True`、root logger `DEBUG`、WSGI 存取紀錄另行收集。沒有 git 寫入、沒有修改追蹤中的檔案（本紀錄除外）；工作結束時 `git status --short` 只有與本票無關、既存的 `grep.exe.stackdump`。
- **Commit 衛生**：`d3e7f4c..37edd5f` 兩個 commit message 皆為 `[Modify] – …` 格式、分類行 `[Additions]`／`[Modification]`；`grep -icE "claude|co-authored|generated with"` → 0。`git diff --check d3e7f4c 7a3b469`（排除 PNG）乾淨。

## 2. 分配 AC 的逐條結論

| AC／項目 | 判定 | 證據（Reviewer 自行取得） |
| --- | --- | --- |
| **AC-V2-06(a)** 較新 → 資料與兩個時間更新 | **PASS** | `applyObservation`（`static/app.js:687-727`）的 else 分支一次替換 `obs`（`:703`）並重建 `obsById`、標記與面板。Reviewer probe（1280）：上游 +1 h → 面板 Observation Time／Fetched Time＝伺服器實際回應（WSGI 端擷取的本文）、`data-refresh-result="newer"`、「Updated to a newer Latest Observation.」。Executor 檢查重跑亦 PASS（1280／375，臺北氣溫一併更新）。 |
| **AC-V2-06(b)** 較舊 → 不變、「已是最新」、無 Stale | **PASS** | `:694` `instant(body.observationTime) < instant(obs.observationTime)` 在 `obs = body`（`:703`）之前判斷；靜態守衛 `test_not_newer_never_replaces_the_shown_data`。Probe：上游 −1 h、新的 Fetched Time → 兩個時間、標記文字全部不變，`not-newer`，「Already the latest: …」，`data-obs-state="success"`、無 chip。另一次 Stale 之後以較舊回應 Refresh（`probe37b`）→ not-newer 且清除 Stale、顯示不變。 |
| **AC-V2-06(c)** 同一 Fetched Time → 同 (b) | **PASS** | `:690` 先判 `body.fetchedTime === obs.fetchedTime`。Probe：時鐘不前進（重用視窗內）且上游已改為 +3 h → 伺服器回同一 Fetched Time 的快取本文，頁面 not-newer、無變更、非 Stale。**DV-4**：相等 Observation Time＋新 Fetched Time → 套用（Fetched Time 更新、Observation Time 不變，「Updated: fetched again; …」），與 R-V2-OBS-8(a)「相等時亦套用」一致。 |
| **AC-V2-06(d)** 連按 → 只一個結果、無亂序 | **PASS** | `:585` `if (obsInFlight) return;`，`:591` 只有目前序號可套用，`requestObservation` 的 `settle` 只生效一次（`:612-640`）。Probe：上游延遲 2 s 時同一 tick 連 `click()` 6 次 → `/api/observations/latest` 請求**只 1 筆**，進行中 `aria-disabled="true"`、「Refreshing…」＋spinner，結束後一個 newer 結果。**亂序嘗試**：以 Fetch domain 扣住請求 A 超過頁面界限（→ Stale）、再發請求 B 得 +4 h 並套用，之後才放行 A（上游已改 +5 h）→ 顯示仍為 B；另一次把被扣住的請求在逾時後以一個更新的 2xx 本文 `fulfill` → 未被套用。 |
| **AC-V2-06(e)** 上游停滯 → 30 s 內 Stale／Unavailable、分類 JSON | **PASS** | Probe：已有資料時上游停滯 40 s → **8.4 s** Stale，伺服器回應為 `{"reason":"upstream_unreachable",…}` JSON（非平台頁）；首次載入停滯 → 8.4 s Unavailable（1280）。Executor 檢查重跑另含「兩個請求排在伺服器鎖前」的排隊情境 16.0 s（< 30 s）。 |
| **AC-V2-06(f)** 平台層非 JSON 5xx → 仍到終態 | **PASS** | `classifyObservationResponse`（`:647-671`）：非 2xx 只在 JSON `reason` 屬四代碼之一時歸該類，否則 `unexpected_response`；2xx 只在 `usableObservation`（`:674-678`）成立時為成功。Probe 以 Fetch domain 直接替換回應：HTML 502、HTML 200、JSON 500 未知 `reason`、JSON 200 缺 `fetchedTime`、空本文 504 → 皆 **0.4 s** Stale、原因「this site's server gave an unexpected answer (HTTP n)」；首次載入 HTML 502 → Unavailable（1280 與 375）。**扣住請求不回應** → **20.4 s** Stale（首次載入 20.4 s Unavailable），原因「did not answer in time」——頁面界限 `OBS_TIMEOUT_MS = 20000`（`:176`）介於伺服器 8 s（`observation.UPSTREAM_DEADLINE_SECONDS`）與 30 s 儀器之間（靜態守衛 `test_client_bound_between_server_bound_and_instrument`）。 |
| **AC-V2-08(a)** 首次載入失敗 → Unavailable | **PASS** | Probe 對 7 種首次載入失敗（`key_not_configured`、`upstream_unreachable`、`upstream_error` 429、`invalid_response`、平台 HTML 502、上游停滯、請求被扣住）於 1280，及 `key_not_configured`／HTML 502 於 375 各開新頁（`probe37d` 33/33）：`data-obs-state="unavailable"`、Now 仍 `aria-pressed="true"`（終態後再等 2 s 仍未切換）、Observation Time／Fetched Time／有效測站數皆「—」、無站標記、`UNAVAILABLE` chip、「Latest Observation unavailable」說明＋類別原因、地圖內告示、Refresh 可見且 `aria-disabled="false"`、模式切換與 Forecast 按鈕可見、地圖容器 1016×560 可見且底圖 27 條 path（縣界輪廓）、Now mode 內無可見 pill、無 Forecast inline status、無 `Select Date`、Now 面板無任何「數字＋°」。地圖可縮放。之後 Refresh 成功 → 清除、22 標記。截圖目視（已提交 `desktop-unavailable-key_not_configured.png`、`375-unavailable-key_not_configured.png` 與 Reviewer 自產）：縣界輪廓可見、狀態明顯。縣界「互動」圖層屬 #38，見 §4 (c) 與 R-1。 |
| **AC-V2-08(b)** 成功後失敗 → Stale | **PASS** | `applyObservationFailure`（`:732-740`）只設 `obsState = obs ? "stale" : "unavailable"`，不動 `obs`（靜態守衛：全檔 `obs = ` 只有宣告與 `:703` 兩處）。Probe 成功後依序 7 種伺服器失敗（無金鑰、連線例外、403、非 JSON、`success:"false"`、`http_get` 拋出非 requests 例外、429）＋6 種平台／未分類回應＋扣住請求：每次 Observation Time、Fetched Time、有效測站數、22 個標記文字與失敗前完全相同，`STALE` chip、「Stale」說明、原因、地圖內「Stale · last successful Latest Observation」、標記虛線框（`map--obs-stale`）、Refresh 可用、仍在 Now mode。 |
| **AC-V2-08(c)** 之後成功清除 Stale | **PASS** | Probe：Stale → newer 成功 → 清除；Stale → not-newer 成功（較舊 Observation Time）→ 清除且顯示不變（`probe37b`）。`applyObservation` 兩類成功皆設 `obsState="success"`、`obsFailure=null`（`:722-723`）。 |
| **AC-V2-08(d)** 年齡不觸發 Stale | **PASS** | 狀態碼無時鐘／計時器：靜態守衛 `test_no_clock_or_age_in_the_observation_state_code`、全檔無 `setInterval`，`obsState` 只有三個賦值點（`test_stale_and_unavailable_are_set_only_by_a_failure`）；Reviewer 讀 `:163-176`、`:583-785` 確認唯一 `setTimeout` 在 `requestObservation` 的單次請求界限內。Probe 以 `Emulation.setVirtualTimePolicy` 推進 7,500,000 ms 後仍 success、無 chip；Executor 年齡情境重跑 PASS（`virtualTimeBudgetExpired` 已觸發，之後 not-newer 仍 success）。 |
| **AC-V2-08** 四類各至少一次且可辨 | **PASS** | 四類在 (a) 與 (b) 皆出現；原因行四種文字互不相同並附各自 reason 代碼，`upstream_error` 另附「(HTTP 403／429)」；`OBS_FAILURE_TEXT`（`:185-192`）六個文字互異（靜態守衛）。截圖集合：stale／unavailable 桌機與 375 皆有（已提交）。 |
| **AC-V2-04**（瀏覽器 stale／unavailable 面） | **PASS** | `<dt>` 逐字 `Observation Time`、`Fetched Time` 在所有狀態存在（`index.html` 未改動該段）；Stale 時值＝上一次成功回應（見 (b)），Unavailable 時值「—」（見 (a)）。 |
| **AC-V2-09(b)** 觀測失敗＋預報正常 | **PASS** | Probe（Unavailable：`key_not_configured`、扣住請求；1280 與 375）：以鍵盤切到 Forecast mode → 可見 pill 集合＝`/api/days/<d0>` 的 `derivedMapTemperature` 一位小數、`Select Date` 可見、`#dashboard` 可見、無 `#page-error`、無 Now 狀態告示或 chip；表格 7 列；切回 Now → Unavailable 原樣保留；地圖可縮放。Executor 檢查重跑另涵蓋 Stale 情境、pill 顏色＝band、Select Date 七日、以 Select Region 選南部地區 → 七列＝`/api/` series、圖表兩條線。Radar 尚不存在（#40）。 |
| **AC-V2-20**（本票範圍：CI 全綠） | **PASS** | Subject `pytest` → **475 passed**（Reviewer 本機）；BASE（`git archive d3e7f4c`）收集 459 個 test id，**全部**仍在 subject（`comm -23` 空），新增 16 個（`test_refresh_frontend.py` 14、`test_secrets.py` 參數化 2）。CI `36176654923`（headSha `7a3b469`）success：log `475 passed in 11.72s`、`credential scan passed`；`36177105877`（`c4f5475`）success。 |
| 伺服器與 V1 產物不變 | **確認** | `git diff --stat f63ebb1 7a3b469`（#36 code anchor 起）與 `d3e7f4c 7a3b469` 對 `observation.py`、`server.py`、`representative.py`、`app.py`、`weather_query.py`、`ingestion/`、`data.db`、`api/`、`smoke.py`、`vercel.json`、`requirements.txt`、`.github/` → 皆空；對 `main`（V1 結案內容）`app.py`／`weather_query.py`／`ingestion`／`data.db`／`smoke.py`／`doc/requirement` 亦空。本票為純前端。 |
| #35／#36 回歸 | **無回歸** | 全套 475 通過（含 #35 的 `test_observation.py` 與 #36 的 `test_modes_frontend.py` 全部）；`check_modes_browser.py` 重跑 **37/37**；V1 `check_series_error_visible.py` PASS（503 與 404 皆有可見訊息）。 |

**Spec 條款對照（本票 Traceability）**：R-V2-OBS-7 (a) 逐字 `Refresh`、可鍵盤；(b) 無輪詢（`loadObservation()` 全檔只有定義、頁面載入、按鈕 listener 三處）；(c) 進行中指示；(d) 三結果以 `data-refresh-result` 與文字可觀察；(e) 見 AC-V2-06(d)——**成立**。R-V2-OBS-8——**成立**（含 DV-4 相等套用）。R-V2-OBS-10 (a)～(e)——**成立**。R-V2-OBS-12（使用者可見層）——**成立**（見 H-1 段）。R-V2-OBS-13（前端面）——**成立**。R-V2-DEG-2——對本 subject 存在的元素**成立**（地圖、底圖縣界、模式切換、Forecast mode、下方 dashboard；縣界互動圖層與 Radar 尚不存在，見 R-1）。R-V2-MODE-6(c)——**成立**（見 H-3 段）。

## 3. Invariants

| INV | 判定 | 證據 |
| --- | --- | --- |
| INV-V2-6 新鮮度單調；Stale 只以失敗為基準 | **HOLDS** | 結構：`obs` 只在 `:703` 被賦值，且只在「非同一 Fetched Time 且 Observation Time 不小於顯示者」的分支；`usableObservation` 要求兩個時間可解析，比較不會遇到 NaN。行為：Reviewer 在頁面載入前注入 MutationObserver 記錄 `#obs-time` 全生命週期的值，經過較舊回應、同 Fetched Time、13 種失敗、扣住請求、晚到回應、連點與虛擬時間推進後，序列單調不減（1280）；Executor 檢查重跑兩個視野同樣成立。Stale 只由 `applyObservationFailure` 設定（見 AC-V2-08(d)）。 |
| INV-V2-7 三條路徑獨立降級（觀測失敗面） | **HOLDS** | AC-V2-09(b) 列；`applyObservationFailure`／`renderObsState` 只碰 Now 面板、`#obs-map-state` 與 `#map` 的 `map--obs-stale` class（只作用於 `.spill` 觀測標記），不觸及 `forecastMapStatus`、`#page-error`、`#dashboard`。Radar 面屬 #40。 |
| INV-V2-3 瀏覽器只呼叫 `/api/`、零外部請求 | **HOLDS** | **Reviewer 重新擷取**（不採信已提交的 `network-log.json`）：10 次頁面載入（1280 與 375；成功、Stale、Unavailable、Forecast mode、dashboard）全部請求經 Fetch domain 攔截，唯一 URL 集合只有 `/`、`/favicon.ico`、`/static/{app.js,styles.css,vendor/leaflet.css,vendor/leaflet.js,data/basemap.js}`、`/api/{health,regions,regions/<r>/series,days,days/<d>,observations/latest}`；**外部請求 0**。本票 diff 不含任何絕對 URL；`fetch("/api/observations/latest", …)` 為同源相對路徑。 |
| INV-V2-5 兩種語義分開 | **HOLDS**（本票面） | Stale／Unavailable 的標示只在 Now mode（`#obs-state`、chip、`.obs-map-state-wrap` 皆在 `data-mode="now"` 範圍內，靜態守衛 `test_state_presentation_belongs_to_the_now_mode`；probe 在 Forecast mode 下兩者皆不可見）；Stale 標記色 `--obs-stale-bg #cfd6e1`／`--obs-stale-border #9aa4b6` 與四個 `--band-*` 互斥。 |
| INV-V2-8 V1 不變量與產物不變 | **HOLDS**（本票範圍） | AC-V2-20 列與「伺服器與 V1 產物不變」列。 |

## 4. Executor 關切的獨立判斷

**(a) 兩個前端呈現類別（`no_response`「did not answer in time」、`unexpected_response`「unexpected answer」）是否牴觸 DV-6。** 不牴觸，在 #37 契約內，不需 Design Authority。理由：DV-6／R-V2-OBS-11 規定的是**伺服器** `/api/` 失敗回應的 `reason` 必須恰為四代碼之一——本票未改伺服器，四代碼集合、`OBS_SERVER_REASONS`（`:193-195`）與 `observation.FAILURE_REASONS` 一致（靜態守衛比對兩者）。兩個前端類別只描述「伺服器的分類答案根本沒到達頁面」的情形（逾時／網路失敗、平台頁或未知格式），它們不被當成伺服器代碼顯示（`failureText` 只對四個伺服器類別附代碼，`:748-757`），也不會把平台層錯誤誤標為某個伺服器類別。R-V2-OBS-13／DV-7 明文要求「前端對任何非 JSON 或平台層錯誤回應仍 MUST 依 failure 處理」，R-V2-OBS-10(a)(b) 要求 Stale／Unavailable 帶非機密原因；為此類失敗提供獨立、非機密的類別文字是 HOW 的合理實現。R-V2-OBS-12 要求四類「各自可辨」，增加前端類別不降低四類的可辨性（六個文字互異）。

**(b) ≥ 1180 px 時 Now 面板改為面板內捲動。** 合法交接 #39，不是 #37 缺陷。R-V2-RSP-6／AC-V2-14（桌機面板不遮蔽選取項與關鍵控制、詳情不被裁切到不可讀）分配給 #39（derivation §15；#39 issue 列 AC-V2-14）。在本 subject 上，AC-V2-08(b) 要求可見的項目——Stale 標示與原因、兩個時間、Refresh——在 1280×900 選取測站＋Stale 時無需捲動即可見（已提交 `desktop-stale-upstream_error.png` 與 Reviewer 截圖目視）；選取測站詳情在面板內捲動可達，選中的標記仍在地圖上突顯。捲動取代溢出地圖框是正向改善。

**(c) Unavailable 的「縣界可見」由 vendored 底圖呈現。** 對本 subject **PASS**：R-V2-DD-4 的帶屬性互動圖層尚不存在，底圖的縣界輪廓（27 條 path）在 Unavailable 下可見。但此項揭露一個 Ticket 分配缺口，見 **R-1**（routing signal，非 blocking）。

**(d) #35 R1 F-2（伺服器鎖使同時停滯排隊）。** 瀏覽器面由本票承接且成立：頁面界限 20 s 使任何排隊中的 Refresh 最遲約 20.4 s 到達 Stale／Unavailable（< 30 s 儀器）；Executor 的排隊情境 16.0 s，Reviewer 的扣住請求情境 20.4 s。部署上的多實例與平台時序屬 #41——合法交接。

**(e) 兩個 #36 斷言被修改。** 皆**未弱化**，與 #36 CLOSED 行為（`f63ebb1` 的 R1 CLOSURE）一致：
- `tests/test_modes_frontend.py:142-145`：原斷言 `'"/api/observations/latest"' in _body("loadObservation")` 改為 `"requestObservation()" in _body("loadObservation")` 且 `'fetch("/api/observations/latest"' in _body("requestObservation")`。該測試保護的是「Now mode 不以 `/api/health` 為前提」——頁面載入時直接呼叫 `loadObservation()`、`bootstrap`／`loadRegions`／`showDashboard` 不呼叫它——這些斷言原封未動；端點字面仍被釘住，且新斷言綁在 `fetch(` 上，較原本更精確。
- `tests/check_modes_browser.py:580-582`：Refresh 成功後 `after["status"] == ""` 改為 `== "Updated to a newer Latest Observation."`。原斷言的作用是「成功時沒有錯誤文字」；新斷言是精確字串比對，同樣排除任何錯誤文字，並納入 #37 新增、R-V2-OBS-7(d) 要求可觀察的 newer 結果告知。同一檢查的其餘條件（一次請求、兩個時間＝回應、氣溫 26.4）未變。Reviewer 重跑 37/37。
- #36 的暫時呈現「失敗時在 Refresh 旁顯示伺服器 `error` 文字」被本票取代，這正是 #36 R1 記錄的交接（`issue-36-c1-r1.md` 第 105 行）；取代後只顯示固定文字，更嚴格。

## 5. High-risk 核對段（decision A-1）

**觸及類別：H-1、H-3。H-2 未觸及。**

- **H-1（憑證與機密；R-V2-OBS-12、R-V2-SEC-7 的使用者可見面）**
  - *核對了什麼*：(i) 原始碼——頁面顯示的原因只來自 `OBS_FAILURE_TEXT` 固定文字＋伺服器 reason 代碼（已驗證屬四代碼之一）＋數字 HTTP 狀態；`classifyObservationResponse` 只從本文取 `reason` 與 `upstreamStatus`（後者須為 100–599 整數，`isHttpStatus` `:680-682`），`applyObservationFailure`／`failureText`／`renderObsState` 不讀 `.error`、不用 `innerHTML`，只用 `textContent`；`app.js` 無 `console.*`、無 `localStorage`／`sessionStorage`。(ii) 行為——Reviewer 以哨兵金鑰 `RVW-SENTINEL-KEY-7f3a9c-r1`、Flask `debug=True`、root logger `DEBUG` 執行，上游模擬把哨兵金鑰、`opendata.cwa.gov.tw` 與本文標記放進例外訊息（`requests.ConnectionError`、`RuntimeError`）與 403／429／非 JSON／`success:"false"` 本文；平台層以 Fetch domain 注入含標記**與哨兵金鑰**的 HTML 502、`error` 欄含哨兵金鑰的 JSON 500，以及 `reason` 合法但 `error` 含金鑰、`upstreamStatus` 為 `"<b>x</b>"` 的 JSON 502。掃描：伺服器端擷取的全部 `/api/observations/latest` 回應本文、每個終態的 `document.documentElement.outerHTML`、全部 console／`Log.entryAdded`／例外事件、伺服器 log（177 行，含 `latest observation failed: reason=…` 與存取紀錄）——哨兵金鑰、上游本文標記、上游主機、`Authorization`、平台頁標記 **0 命中**；`upstreamStatus` 非數字時不顯示。(iii) 機械檢查——`python -m tools.credential_scan` passed（618 tracked files）；`git ls-files` 無 `.env`；本票 diff 對 `static/**` 無 `opendata`／`CWA_API_KEY`／`Authorization`；兩個新測試檔已加入憑證掃描清單。b3 兩個授權位置：本票未觸及金鑰讀取路徑（伺服器檔案無 diff）。
  - *結果*：**成立**。
- **H-3（資料語義與標示；Stale／Unavailable 不把預報當觀測、用語）**
  - *核對了什麼*：Unavailable 時 Now mode 無任何觀測或預報數值（面板只有「—」；無站標記、無 pill、無 `DERIVED`、無 `Select Date`、無 Forecast inline status）、不自動切換模式、說明文字「No Latest Observation to show. Use Refresh to try again.」不提預報、不暗示預報可替代觀測（R-V2-MODE-6(c)）；Stale 保留的是上一次成功的**觀測**，標為 Stale 並附「Shown: the last successful Latest Observation and its own times」，標記樣式不使用四段導出色；觀測失敗時 Forecast mode 的 `DERIVED` 標示、band 色 pill 與面板不變且不出現 Now 狀態；代表標記的「station value, not a county value」標示未被改動；所有終態 DOM（Reviewer 與 Executor 兩套）無 `real-time`／`realtime`／`live`（`aria-live` 屬性除外）。
  - *結果*：**成立**。另見 F-1：在宣告的運作範圍之外（伺服器不可能產生的 2xx 本文），Stale 的「last successful」敘述可能不實——Low、non-blocking。
- **H-2**：未觸及。頁面標籤與 V1 概念詞未改（`test_verbatim_labels` 等守衛通過），`app.py`、`weather_query.py`、`data.db` 無 diff。

## 6. Findings

### F-1 — 通過淺層檢查但在套用中拋錯的 2xx 本文，會在 `obs` 已被替換後才轉為失敗

- **Severity**：Low｜**Blocking**：否
- **證據**：`usableObservation`（`app.js:674-678`）只檢查 `stations` 是陣列與兩個時間可解析；`applyObservation` 在 `:703` 先 `obs = body`，`:705` 的 `body.stations.forEach(function (s) { obsById[s.stationId] = s; })` 遇到 `null` 元素即拋錯；`loadObservation` 的 `.then(null, …)`（`:598-601`）隨後以 `unexpected_response` 呼叫 `applyObservationFailure`，此時 `obs` 已是未成功套用的本文。Reviewer `probe37c` 以 Fetch domain 回 `{"stations":[null],"observationTime":"2026-09-26T09:00:00+08:00","fetchedTime":"2026-09-26T09:05:00+08:00",…}`：首次載入 → `stale`（而非 `unavailable`），面板顯示 09:00／09:05／有效測站 1；成功之後 → `stale`，面板時間換成該本文的時間，地圖仍是前一份的 22 個標記，且標示為「last successful Latest Observation and its own times」。
- **契約關聯與風險**：R-V2-OBS-10(a)(b) 的 Stale 定義是「仍顯示上一次成功的資料」。但觸發條件只能是本應用自己的 `/api/` 回了一個不符 R-V2-OBS-3 的成功本文——#35 的正規化器只輸出物件、伺服器只回成功或分類失敗（#35 已結案稽核），平台層也不會產生帶 `stations` 陣列的 2xx JSON；因此在宣告的運作範圍內不可到達。INV-V2-6 不受影響（只有 ≥ 分支會替換）。每次 Refresh 仍到達終態（R-V2-OBS-13 成立）。
- **Disposition**：non-blocking；本票不需後續處理。可選的加固（在任何狀態變更前完成驗證，或例外時還原 `obs`／`obsById`）留給下一位修改此套用路徑的 Executor 在其自身契約內考慮；無須另開工作項。

### F-2 — 已提交的證據中 Fetched Time 早於 Observation Time

- **Severity**：Low｜**Blocking**：否
- **證據**：`check_refresh_browser.py` 的 `Clock` 從 2026-09-26 00:04:56 起、每次新取得前進 601 s，而上游變體把 `ObsTime` 平移到 −1～+4 h，兩者互不相依。結果如 `desktop-stale-upstream_error.png` 顯示 Observation Time `2026-09-26 01:00`、Fetched Time `00:55:01`；`browser-check-results.json` 的「late answer」一項記 time 02:00、fetched 01:45:06——伺服器在觀測時刻之前就取得資料，現實中不可能。
- **契約關聯與風險**：不影響任何檢查的判定（oracle 取自頁面實際收到的回應），產品行為正確。但這些截圖是 AC-V2-08 的必要截圖集合，將被 V2 驗收文件引用；讀者（acceptor、授課老師）可能因此質疑時間語義。
- **Disposition**：non-blocking；owner **#41**（彙整 `ACCEPTANCE-V2.md` 時為引用的 #37 截圖註明「合成時鐘」，或以時間一致的設定重產）。

### F-3 — README 對首次載入結果的敘述與實作略有出入

- **Severity**：Low｜**Blocking**：否
- **證據**：`README.md`（Now mode 段）「Every Refresh — and the page's first load — ends in exactly one of three results, shown next to the button」；實作在首次載入成功時刻意不顯示告知（`app.js:711-712` `message = ""`，worklog 決定 3 亦如此記載）。
- **Disposition**：non-blocking；owner **#41**（R-V2-DOC-1／AC-V2-21 最終文件審查時調整措辭）。

## 7. Routing signals（不是 blocking finding）

### R-1 — 觀測失敗下「縣界互動圖層」與「縣脈絡」的 Ticket 層驗證沒有 owner → **Design Authority**

- **具體缺口**：derivation record §15 把 AC-V2-08（含 (a)「地圖與縣界可見」）與 R-V2-DEG-2（「觀測失敗只影響 Now mode 的觀測層（標記、面板資料、脈絡）：地圖、**縣界互動**…全部維持可用」）只分配給 #37。帶屬性的縣界互動圖層（R-V2-DD-4）與 County 脈絡（R-V2-DD-5）由 #38 建立，而 #38 **不**被 #37 阻擋（tickets-v2 與 TB-V2-2 明定），其 issue 本文的 AC 與 Traceability 不含 AC-V2-08、AC-V2-09(b)、R-V2-OBS-10、R-V2-DEG-2 或 INV-V2-7；#37 的 issue 寫「縣脈絡在各狀態下的內容（#38 承接本票的狀態規則）」，但 #38 的本文沒有對應的義務。因此在 #37 的 subject 上「縣界可見」只能以 V1 底圖輪廓滿足（本票 PASS）、「縣界互動維持可用」無可驗證對象；在 #38 之後，觀測 Stale／Unavailable 時互動圖層是否仍可見可用、County 脈絡顯示什麼，在 Ticket 層沒有能觀察它的 owner，只剩 Spec Integration Audit 兜底——與 #36 R1 的 R-1（→ DV-20）同型。
- **附帶的語義問題（供 DA 一併判斷是否需要釐清）**：Unavailable（沒有任何可顯示的觀測）時若仍可選縣，County 脈絡應呈現什麼？R-V2-DD-5 規定「零有效測站的縣…脈絡顯示 0 與『—』，不是錯誤」，而 R-V2-DEG-2／R-V2-OBS-10(a) 把脈絡列為受觀測失敗影響的觀測層；若 #38 在 Unavailable 下沿用 DD-5 顯示「0 個有效測站」，會把「沒有資料」呈現成「該縣零有效測站」。Stale 時脈絡應為上一次成功資料（R-V2-OBS-10(b)）似無歧義。
- **Required authority**：Design Authority（Ticket 分配／契約充分性，治理 §4.2、§2.4）。不阻擋 #37。

## 8. 結論

#37 分配的 AC-V2-06（瀏覽器 (a)～(f)）、AC-V2-08（(a)～(d) 與四類可辨）、AC-V2-04（瀏覽器 stale／unavailable 面）、AC-V2-09(b)、AC-V2-20（本票範圍）全部 **PASS**；R-V2-OBS-7／8／10／12（使用者可見層）／13（前端面）、R-V2-DEG-2（本 subject 既有元素）、R-V2-MODE-6(c) 成立；INV-V2-6、INV-V2-7（觀測失敗面）、INV-V2-3、INV-V2-5、INV-V2-8 成立。H-1、H-3 核對成立，H-2 未觸及。伺服器檔案自 #36 起無 diff，#35／#36 無回歸（475 tests、BASE 459 id 全在、CI 綠、#36 瀏覽器檢查 37/37）；Reviewer 自行重新擷取的 network log 外部請求 0。Executor 關切 (a)(e) 在契約內且未弱化 #36 保證，不需 DA；(b)(d) 為 #39／#41 的合法交接；(c) 對本 subject 成立，其揭露的分配缺口以 R-1 route Design Authority。Findings F-1、F-2、F-3 皆 Low、non-blocking，disposition 如上。

VERDICT: CLOSURE
