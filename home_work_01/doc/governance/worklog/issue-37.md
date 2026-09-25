# Worklog — Issue #37 Refresh 與狀態語義：newer／not-newer／failure、Stale／Unavailable、觀測失敗只影響 Now mode

- **Work item**：GitHub Issue #37（Formal lane，V2 Core；Blocked by #36——已 CLOSED）
- **Executing role**：`executor`，以 `gov-executor` definition 派工（Bindings §3.1 mapping：`claude-opus-5-5`，effort `high`）。本 session 自述的模型為 Opus 5.5；**這不是 binding 證據**。Binding verification 依 Bindings §3.4 由派工者（Orchestrator）從 harness 紀錄核對並記入 run record 或 audit record；本 worklog 不複製 harness 日誌。
- **Branch**：`home_work_01-v2-implementation`；**BASE ＝ `d3e7f4c`**（DV-20 tracker actions 的 run-record commit）
- **Subject**：**code anchor ＝ `7a3b469`**（BASE `d3e7f4c`..`7a3b469` 為本票全部產物變更）；本 worklog 為其後的 record-only commit（`doc/governance/**`，Bindings §7 P7）
- **開始／本次更新**：2026-09-26

## Contract reference

- **Outcome Contract**：`home_work_01/doc/governance/outcome-contract-v2.md`（ACCEPTED 2026-09-25；normative candidate `69c5a04`）。A-3（金鑰）本票**未使用**；A-4 未使用。
- **Spec**：`home_work_01/doc/spec/SPEC-V2.md` **v2.2**——§2.2 R-V2-OBS-7、OBS-8、OBS-10、OBS-12（使用者可見層）、OBS-13（前端面）；§2.5 R-V2-DEG-2；R-V2-MODE-6(c)（Unavailable 不暗示預報為觀測）；§5.3 有界時間儀器（30 秒）；INV-V2-6、INV-V2-7（觀測失敗面）。
- **Derivation record**：`home_work_01/doc/governance/decisions/derivation-SPEC-V2.md` DV-4（取代規則；相等亦套用；not-newer 不是 Stale）、DV-5（伺服器只回成功或分類失敗；Stale 為介面狀態）、DV-6（四個失敗代碼）、DV-7（有界時間：前端對非 JSON／平台層錯誤仍依 failure 處理；儀器 30 秒）；§15（本票分配）。
- **High-risk decision**：`home_work_01/doc/governance/decisions/decision-20260923-high-risk-categories.md`（A-1：R1 record 須明記核對段；下方「High-risk 核對材料」提供入口）。
- **Ticket 分配（#37）**：AC-V2-06（瀏覽器面 (a)～(f)；API 面已由 #35）、AC-V2-08、AC-V2-04（瀏覽器 stale／unavailable 面）、AC-V2-09(b)、AC-V2-20（本票範圍：CI 全綠）。AB-V2-3、AB-V2-4、AB-V2-5（部分）。§6.3 定向 V1 重驗：無。
- **Out of scope（未做）**：伺服器端分類與重用（#35；`observation.py`、`server.py` 未修改）、Radar 狀態（#40）、縣脈絡在各狀態下的內容（#38）、可選年齡提示（未實作）。
- **契約變更**：無。未修改任何 requirement、AC、invariant、gate、oracle。

## Decisions and assumptions（HOW；Spec §5.2 委派）

1. **前端有界時間**：`requestObservation()` 以 `setTimeout(OBS_TIMEOUT_MS = 20000)`＋`AbortController` 包住 `fetch("/api/observations/latest")`，並以 `settled` 旗標保證只 settle 一次——回應、網路失敗／abort、逾時三條路徑皆 settle；逾時後即使晚到的回應也不會被套用。20 秒的理由：大於伺服器上游界限 8 s（`observation.UPSTREAM_DEADLINE_SECONDS`，#35），使分類過的 JSON 通常先到；小於 §5.3 的 30 秒儀器。README 記載。
2. **回應分類（前端）**：2xx 只有在 body 可用（`stations` 陣列、`observationTime` 與 `fetchedTime` 可解析為時刻）時才是成功；非 2xx 只有在 JSON 的 `reason` 恰為四個伺服器代碼之一時才歸該類；其他一切（平台 HTML 502、空 body、不可解析、未知 reason、2xx 但 body 不可用）歸前端類別 `unexpected_response`；逾時／網路失敗歸 `no_response`。這兩個是**前端呈現類別**，不是新的伺服器 reason 代碼（伺服器 DV-6 四代碼不變）；它們承接 R-V2-OBS-13「平台層錯誤仍依 failure 處理」。
3. **三種結果（R-V2-OBS-7(d)、OBS-8、DV-4）**：先判 `body.fetchedTime === obs.fetchedTime`（重用視窗內的同一份回應）→ not-newer；再判回應的 dataset Observation Time **<** 顯示者 → not-newer（資料與兩個時間都不動）；否則（≥）→ newer，資料、Observation Time、Fetched Time 一併替換。Observation Time 相等但為新的取得 → 依 DV-4 套用，告知文字為「Updated: fetched again; the Observation Time is unchanged.」（結果仍屬 newer／applied）。not-newer 的告知為「Already the latest: no newer Latest Observation than the one shown.」，樣式為成功色（非 Stale）。首次載入成功不顯示告知（資料本身即結果）；Unavailable 後成功顯示「Loaded the Latest Observation.」。
4. **狀態機（R-V2-OBS-10）**：`obsState` ∈ `loading`／`success`／`stale`／`unavailable`，只有三處賦值：初值 `loading`、`applyObservation` 設 `success`（newer 與 not-newer 皆清除 Stale／Unavailable，OBS-10(c)）、`applyObservationFailure` 設 `obs ? "stale" : "unavailable"`。失敗路徑不清除 `obs`（保留上一次有效資料與兩個時間）。狀態碼無任何時鐘／年齡判斷、無計時器（INV-V2-6、OBS-10(d)）；可選年齡提示未實作。
5. **一次只一個 Refresh（OBS-7(e)）**：沿用 #36 的 `obsInFlight` 忽略；另加 `obsSeq`，只有目前的 Refresh 可套用結果（防禦性；與 abort＋settle 一起保證晚到的回應不會被套用）。套用過程若拋錯，`.then(null, …)` 轉為 failure 終態，之後才清除 busy。
6. **Stale／Unavailable 呈現（OBS-10(e)）**：面板標題的狀態 chip（`STALE` 琥珀色／`UNAVAILABLE` 紅色）；面板內說明區塊（標題「Stale」或「Latest Observation unavailable」、一句說明、`Reason: <類別文字>[ (HTTP n)] — <reason 代碼>.`）；地圖左下（≥ 1180 px 時位於浮動面板右側）不攔截指標的地圖內告示；Stale 時標記改為虛線框、灰階底（`--obs-stale-bg`／`--obs-stale-border`，與四段導出色帶互斥）。`#now-panel` 帶 `data-obs-state` 與 `data-refresh-result` 供驗證。Refresh 旁的 live region 簡述結果（「Refresh failed: data is Stale.」／「Latest Observation unavailable.」）。
7. **H-1（非機密原因）**：頁面顯示的原因一律是前端固定文字（`OBS_FAILURE_TEXT`）＋ reason 代碼＋（若有）數字 HTTP 狀態；**不再顯示伺服器 `error` 文字**（#36 的暫時呈現會顯示它），任何回應本文都不進 DOM。`upstreamStatus` 只在為 100–599 的整數時才顯示。
8. **H-3**：Unavailable 時 Now 面板不顯示任何溫度值；不自動切換到 Forecast mode；說明文字不提預報、不暗示預報可替代觀測；用語為 Latest Observation／Stale／Unavailable，無 real-time／live。
9. **版面**：Now 面板標題列允許 chip 換行（避免 `UNAVAILABLE` chip 溢出）；≥ 1180 px 浮動時 Now 面板 `max-height: calc(100% - 28px); overflow-y: auto`，不再超出地圖框（加入 Stale 說明後，選取測站時面板高度可能超過 560 px 地圖）。
10. **既有 #36 測試／檢查的最小調整**：(a) `test_modes_frontend.py::test_observation_load_is_not_gated_on_health` 的端點字面斷言原本在 `loadObservation` 內，請求移入 `requestObservation()` 後改為斷言 `loadObservation` 呼叫 `requestObservation()` 且後者含 `fetch("/api/observations/latest"`——斷言強度不變（仍要求字面端點，且現在綁在 `fetch(` 上）。(b) `check_modes_browser.py` 一項斷言由「Refresh 成功後狀態文字為空」改為「狀態文字為 `Updated to a newer Latest Observation.`」（#37 新增的 newer 告知），其餘 36 項未改。
11. **瀏覽器檢查工具**：新增 `tests/check_refresh_browser.py`（`check_*` 命名不被 pytest 收集；重用 `check_modes_browser.py` 的 DevTools driver）。伺服器為未修改的 `create_app`，以 threaded WSGI server 於 loopback 執行、Flask `debug=True`、root logger `DEBUG`、`CWA_API_KEY` 為哨兵字串；觀測服務為真的 `LatestObservationService`（可控時鐘、重用視窗 600 s），上游為樣本衍生的模擬（各變體把擷取小時的 `ObsTime` 平移 −1～+4 小時），外加一層只攔 `/api/observations/latest` 的「平台」WSGI（HTML 502 或保留請求 25 s 後才放行）。無金鑰、無網路。

## Artifacts（code anchor `7a3b469`；BASE `d3e7f4c`）

| 檔案 | 動作 |
| --- | --- |
| `home_work_01/static/app.js` | 修改：`requestObservation`（有界時間、abort、單次 settle）、`classifyObservationResponse`、`usableObservation`、三種結果的 `applyObservation`、Stale／Unavailable 的 `applyObservationFailure`、`renderObsState`、`failureText`、`OBS_FAILURE_TEXT`、`obsState`／`obsSeq`；檔頭說明 |
| `home_work_01/static/index.html` | 修改：Now 面板狀態 chip、`#obs-state` 說明區塊、`data-obs-state="loading"`、地圖內告示 `#obs-map-state` |
| `home_work_01/static/styles.css` | 修改：狀態 chip、說明區塊、地圖內告示、Stale 標記樣式與 token、成功告知色、Now 面板標題換行與浮動時捲動 |
| `home_work_01/tests/test_refresh_frontend.py` | 新增：14 個靜態守衛 |
| `home_work_01/tests/check_refresh_browser.py` | 新增：可重現的瀏覽器檢查 |
| `home_work_01/tests/test_modes_frontend.py` | 修改：決定 10(a) |
| `home_work_01/tests/check_modes_browser.py` | 修改：決定 10(b) |
| `home_work_01/tests/test_secrets.py` | 修改：兩個新測試檔加入憑證掃描清單（只加） |
| `home_work_01/README.md` | 修改：Now mode 的 Refresh 三結果、Time bound、Stale and Unavailable、Failure reasons；endpoint 段加前端 20 s；測試段 |
| `home_work_01/doc/acceptance/screenshots/v2/issue-37/*` | 新增：截圖、`browser-check-results.json`、`network-log.json`、`regression-check-modes-browser-results.json` |

未修改：`observation.py`、`server.py`、`representative.py`、`app.py`、`weather_query.py`、`ingestion/**`、`data.db`、`api/**`、`smoke.py`、`vercel.json`、`requirements.txt`、`.github/workflows/**`、`doc/requirement/**`；單元目錄外無變更（RB-5）。

## Verification

環境：Windows 11，`home_work_01/.venv` Python 3.12；Chrome（headless，DevTools protocol，`websocket-client`）；`node --check static/app.js` 語法檢查。以下 subject 皆指 `7a3b469` 的工作樹。

- **V-1 全套**：`python -m pytest -q` → **475 passed**（BASE 459 ＋ 16：`test_refresh_frontend.py` 14、`test_secrets.py` 參數化 ＋2）。全離線。
- **V-2 V1／既有測試保留（quality floor）**：BASE `tests/` 全部 226 個 `test_*` 在 subject 皆存在（missing: []）；`git diff d3e7f4c -- tests/` 對既有檔案的刪除行只有兩行——決定 10(a)(b) 的兩個斷言（皆以同等或更強的斷言取代）；無 skip、無門檻降低、無斷言移除。
- **V-3 CI**：push `7a3b469` 後 workflow「home_work_01 CI」run **`36176654923`** **success**：`475 passed in 11.72s`；`credential scan passed: 617 tracked files …`。Workflow 未修改（A-4 未使用）。
- **V-4 憑證**：`python -m tools.credential_scan`（staged 後）passed；以腳本讀 `.env`（不印出）比對 `git diff --cached` 全文（166,820 bytes）→ 真金鑰字面 **False**；`static/**` 無哨兵字串；evidence JSON 無哨兵金鑰、上游標記、平台標記、`opendata.cwa.gov.tw`、`Authorization`。
- **V-5 瀏覽器檢查 `python tests/check_refresh_browser.py` → 97/97 PASS**，證據 `home_work_01/doc/acceptance/screenshots/v2/issue-37/`（`browser-check-results.json` 記每項觀察值）。桌機 1280×900 與 375×812（mobile emulation）各跑「成功後」與「首次載入失敗」兩個情境，另有 1280 的年齡情境：
  - **AC-V2-06(a)** 回應 Observation Time 較新 → 資料、兩個時間、臺北氣溫一併更新，告知「Updated to a newer Latest Observation.」（`desktop-newer.png`、`375-newer.png`）。
  - **AC-V2-06(b)** 回應 Observation Time 較舊（上游平移 −1 小時；回應 `observationTime` 2026-09-25T22:00、Fetched Time 為新）→ 顯示的 Observation Time、Fetched Time、標記、選取皆不變，「Already the latest…」，狀態仍 success（`desktop-not-newer-older-observation-time.png`）。
  - **AC-V2-06(c)** 伺服器重用視窗回同一 Fetched Time → not-newer，同上（`*-not-newer-same-fetched-time.png`）。DV-4：相等 Observation Time＋新 Fetched Time → 套用。
  - **AC-V2-06(d)** 上游延遲 1.5 s 時一次連點 5 下 → 只 1 個 `/api/observations/latest` 請求、一個結果套用；平台保留請求 25 s（超過頁面 20 s）且保留中的答案是**更新的**一小時 → 頁面 20.4 s（375：20.3 s）進入 Stale「did not answer in time」，伺服器之後答完，顯示仍為原資料（晚到答案未套用）。
  - **AC-V2-06(e)** 上游停滯 40 s → 伺服器 8.4 s 回 504 JSON `upstream_unreachable`（非平台 gateway 頁），頁面 Stale（`desktop-stale-upstream-stall.png`）；首次載入停滯 → 8.4 s 內 Unavailable（`desktop-unavailable-stall.png`）。另：停滯時已有兩個其他請求排在伺服器鎖前（#35 R1 F-2 的排隊情境）→ 本頁 Refresh 16.0 s 到達 Stale（< 30 s）。
  - **AC-V2-06(f)** 平台層 HTML 502 → 0.4 s 內 Stale，原因「this site's server gave an unexpected answer (HTTP 502)」，平台頁內容未進 DOM（`desktop-stale-platform-502.png`）；首次載入 → Unavailable（`desktop-unavailable-unexpected_response.png`）。
  - **AC-V2-08(a)** 首次載入四類失敗各一次（`key_not_configured` 503、`upstream_unreachable` 504、`upstream_error` 403→502、`invalid_response` 502）＋停滯＋平台 502：皆 Unavailable——留在 Now mode（再等 1.5 s 仍未切換）、兩個時間與有效測站數為「—」、無標記、`UNAVAILABLE` chip、「Latest Observation unavailable」說明與類別原因、地圖內告示、Refresh 可用（`aria-disabled="false"`）、模式切換可見；地圖框與縣界（底圖 27 條多邊形路徑）可見、Now 面板無任何溫度值、無 pill、無 `DERIVED`／`Select Date`、Forecast inline status 不顯示（`desktop-unavailable-*.png`、`375-unavailable-key_not_configured.png`）。之後 Refresh 成功 → 清除 Unavailable、22 個標記、「Loaded the Latest Observation.」。
  - **AC-V2-08(b)／AC-V2-04（stale 面）** 成功後四類失敗各一次（`upstream_error` 429、`upstream_unreachable`、`invalid_response`、`key_not_configured`）：資料、`Observation Time`、`Fetched Time`、有效測站數、22 個標記文字、選取的臺北測站皆與失敗前相同；`STALE` chip、「Stale」說明＋類別原因、地圖內「Stale · last successful Latest Observation」、標記虛線框、Refresh 可用（`desktop-stale-*.png`、`375-stale-upstream_error.png`）。兩個標籤逐字存在；unavailable 時值為「—」。
  - **R-V2-OBS-12 四類可辨**：四個原因行文字互不相同且各含其 reason 代碼；`upstream_error` 另含「(HTTP 429)」／「(HTTP 403)」。
  - **AC-V2-08(c)** Stale 後 newer 成功 → 清除；Stale 後 not-newer 成功（較舊 Observation Time）→ 也清除、顯示不變。
  - **AC-V2-08(d)** 以 DevTools `Emulation.setVirtualTimePolicy` 讓頁面時鐘前進 7,500,000 ms（> 2 小時，`virtualTimeBudgetExpired` 已觸發）→ 仍 success、無 Stale；之後一次 not-newer Refresh 仍 success。
  - **INV-V2-6** 頁面載入前注入的 MutationObserver 記錄整個生命週期內 `#obs-time` 的每個值：`— → 23:00 → 00:00 → 01:00 → 02:00`（兩個視野皆同），期間經過較舊回應、各類失敗、晚到答案，從未遞減。
  - **AC-V2-09(b)／R-V2-DEG-2／INV-V2-7** 在 Stale 與 Unavailable 兩種觀測失敗下：地圖可鍵盤平移、可縮放；切到 Forecast mode（鍵盤）→ 六個 pill 文字＝`/api/days/<d0>` 導出值、band 色、Select Date 七日可用、圖例與面板可見、無 Now 狀態文字；下方 dashboard 以 Select Region 選南部地區 → 七列＝`/api/` series、圖表兩條線；切回 Now → 原狀態仍在（`*-obs-stale-forecast-mode.png`、`*-obs-unavailable-forecast-mode.png`、`desktop-obs-*-full-page.png`）。Radar 尚不存在（#40）。
  - **R-V2-OBS-7(c)／RSP-8** 首次載入（上游延遲 2 s）時 loading 狀態：spinner、「Loading the Latest Observation…」、`aria-disabled="true"`（`*-now-loading.png`）。
  - **R-V2-RSP-2** 375 各情境結束時 `scrollWidth` ≤ `innerWidth`。
  - **H-1** 伺服器以哨兵 `CWA_API_KEY`、Flask `debug=True`、root logger `DEBUG` 執行；模擬上游把金鑰、上游主機與上游本文標記放進例外訊息與回應本文。全部觀測回應本文、各狀態 DOM 快照、console 事件皆無哨兵金鑰、上游本文標記、`opendata.cwa.gov.tw`、`Authorization`；DOM 無平台頁標記；伺服器 log（38 行，含 `latest observation failed: reason=…`）同樣無。
  - **H-3** 各狀態 DOM 文字無 `real-time`／`realtime`／`live`；console 無 JavaScript 例外。
  - **AC-V2-16／INV-V2-3** 五段情境共 192 個瀏覽器請求全部為 `http://127.0.0.1:<port>/…`；**外部請求 0**（`network-log.json`）。
- **V-6 #36 回歸**：`python tests/check_modes_browser.py` → **37/37 PASS**（結果複製為 `regression-check-modes-browser-results.json`／`…-network-log.json`；#36 自己的 evidence 目錄未重產）。V1 `python tests/check_series_error_visible.py` → PASS（503 與 404 皆有可見訊息）。
- **V-7 自我驗證：mutation checks**（scratchpad `mutations37.py`：暫時修改 `app.js`，跑 `test_refresh_frontend.py`＋`test_modes_frontend.py`，部分再跑瀏覽器檢查，最後以 sha256 確認還原；非正式 audit）：M1 同一 Fetched Time 不當 not-newer → 靜態 1＋瀏覽器 3；M2 較舊 Observation Time 被套用 → 靜態 2；M3 以 1 小時計時器設 Stale → 靜態 2＋瀏覽器（年齡情境）1；M4 前端界限改 90 s → 靜態 1＋瀏覽器 ≥ 6（頁面等到保留的答案並套用了它）；M5 顯示伺服器 `error` 文字 → 靜態 1；M6 失敗時清掉資料 → 靜態 1（首輪靜態未抓到，已補守衛）＋瀏覽器 ≥ 6；M7 進行中不忽略 Refresh → 靜態 2。每個 mutation 至少被一層抓到。（排隊情境檢查是 mutation 之後才加入，其餘檢查不變。）
- **V-8 H-2／不變產物**：`git diff --stat d3e7f4c -- app.py weather_query.py ingestion/ data.db smoke.py vercel.json requirements.txt server.py api/ observation.py representative.py ../.github/` → 空。
- **未執行／限制**：preview／Vercel 部署上的行為（真實平台逾時頁與 cold start）屬 #41；A-3 金鑰未使用；瀏覽器檢查不在 CI（需 Chrome 與 `websocket-client`），由 Reviewer 本機重現（約 5 分鐘，含 20–25 s 的保留情境）；縣界**互動**圖層與各狀態下的縣脈絡屬 #38（本票的「縣界可見」由 vendored 底圖的縣多邊形呈現）；Radar 屬 #40；底部資訊面、44×44、768 px 屬 #39。

## High-risk 核對材料（decision A-1；供 R1 明記核對段）

- **H-1（使用者可見錯誤與前端不含金鑰、上游 URL、上游本文）**：前端原因只來自 `OBS_FAILURE_TEXT` 固定文字＋reason 代碼＋數字 HTTP 狀態（`failureText`）；`classifyObservationResponse` 只讀 body 的 `reason` 與 `upstreamStatus`，任何回應文字不進 DOM（`test_no_response_text_is_ever_displayed`）。#36 的暫時呈現「顯示伺服器 `error`」已移除。見 V-5 H-1 段（哨兵金鑰、DEBUG、四類＋停滯＋平台 502＋保留）、V-4。`observation.py`／`server.py` 未修改（伺服器端 H-1 屬已結案的 #35）。
- **H-3（Stale／Unavailable 不把預報當觀測；用語）**：Unavailable 時 Now 面板與地圖無任何溫度值、無 pill、不切換模式、說明文字不提預報；Stale 保留的是上一次成功的**觀測**並標 Stale；Stale 標記樣式不用四段導出色（`test_stale_markers_share_no_colour_with_the_derived_bands`）；觀測失敗時 Forecast mode 的 DERIVED 標示與 pill 不變；用語 Latest Observation／Stale／Unavailable，無 real-time／live（靜態與各狀態 DOM）。
- **H-2**：未觸及（V-8；#36 的 `test_verbatim_labels` 等守衛仍通過）。
- **Diversity**：Executor 與 Primary Reviewer 同為 `claude-opus-5-5` 時，audit record 記 `diversity_lost`（Bindings §5）。

## Audit status

- **Required**：Formal mandatory independent audit（治理 §4.1；Bindings §5）。R1 待 Orchestrator 以 fresh `gov-primary-reviewer` 派工（Bindings §3.5）。本 worklog 的 mutation checks 與瀏覽器檢查皆為 Executor self-verification，**不是**正式 audit。
- **Records**：尚無。

## Remaining work

1. **正式 audit**：R1（Orchestrator 派工）。
2. **Concerns（交有權角色判斷；Executor 未自行裁決）**：
   - (a) **前端兩個非伺服器類別**（`no_response`、`unexpected_response`）：為承接 R-V2-OBS-13「平台層／非 JSON 錯誤依 failure 處理」而設的**呈現類別**，不是新的 `/api/` reason 代碼；四個伺服器類別仍各自可辨。若 Reviewer 認為需確認此呈現不牴觸 DV-6，authority：Design Authority。
   - (b) **Now 面板浮動時可捲動**（決定 9）：≥ 1180 px 且選取測站並處於 Stale 時，面板內容超過 560 px 地圖，改為面板內捲動（選取測站區塊末列需捲動才見）。面板版面與 R-V2-RSP-6 的完整驗收屬 #39。
   - (c) **「縣界可見」**：Unavailable 狀態下由 vendored 底圖的縣多邊形呈現；帶名稱屬性的互動縣界圖層（R-V2-DD-4）屬 #38，#38 須在各狀態下維持它可見（#38 承接本票狀態規則）。
   - (d) **#35 R1 F-2（伺服器鎖使同時的上游停滯排隊）**：前端 20 s 界限使排隊中的 Refresh 仍在 30 s 內到達 Stale（V-5 (e) 排隊情境 16.0 s）；部署上的多實例與平台時序屬 #41。
   - (e) **跨票修改 #36 已稽核的產物**：`test_modes_frontend.py` 一個斷言與 `check_modes_browser.py` 一個斷言（決定 10），以及 #36「失敗時顯示伺服器 `error`」的暫時呈現被本票取代；提請 Reviewer 一併核對。
3. **後續票**：#38（縣下鑽與各狀態下的縣脈絡）、#39、#40（Radar 獨立狀態）、#41（preview 驗證、README 其餘項目、V2 驗收文件）。
