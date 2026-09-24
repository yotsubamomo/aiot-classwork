# Audit record — Issue #24，cycle 1，R2

| 欄位 | 內容 |
| --- | --- |
| Work Contract | GitHub Issue #24（`yotsubamomo/aiot-classwork`）「Select Date 與 Leaflet Taiwan Map：依 Derived Map Temperature 著色」，Scope class ENHANCED REQUIRED（只在 Dashboard）。Spec `home_work_01/doc/spec/SPEC.md` v1.1：R-EN-3～R-EN-7、R-SHR-4（前端等價）、R-DOC-2、R-DS-3；AC-17、AC-18、AC-28（前端側）、AC-14 第 6 項、AC-19（重驗）、AC-27（本票範圍）；INV-2、INV-7、INV-9；AB-14、AB-15、AB-13（部分）。適用裁決：DR-1、DR-4、DR-19；H-2、H-3、A-1。與 R1 record `issue-24-c1-r1.md` 相同。 |
| 受審 subject | branch `home_work_01-hw10-implementation`，HEAD **`f9f9f15d0ec0b9c6e958c97d28257026c90192cb`**（= `git ls-remote origin home_work_01-hw10-implementation`）；修正後實作 subject **`386f30afdc884308bfd8900a3d967e817707d282`**（`git diff --name-status 386f30a..f9f9f15` 只有 `M home_work_01/doc/governance/worklog/issue-24.md`，record-only path）；R1 subject `4ec20b5`；BASE `8d46ead`。本次 targeted correction ＝ `4ec20b5..386f30a`：`static/app.js`（+30／−5）、`static/index.html`（註解 2 行）、`static/styles.css`（−32）、`tests/test_dashboard.py`（+4／−2，新增斷言）、worklog、2 張新截圖 `issue-24-f1-popup-updates-{1280,375}.png`。 |
| Audit 種類 | **R2**（scoped closure review，治理 §4.4），**cycle 1**。只核對 R1 的 blocking findings（F-1、F-2）是否解決、修正是否造成回歸、修正是否直接產生或暴露 blocking defect；另核對 Executor 併修的 F-3。不是第二次全面審查。 |
| 角色 | `primary_reviewer`（definition `gov-primary-reviewer`；Bindings §3.1 mapping `claude-opus-5-5`／`xhigh`） |
| Binding 證據 | 由派工者（Orchestrator）依 Bindings §3.4 核對，記在 run record `home_work_01/doc/governance/run/run-20260924-hw01-formal.md`。Executor binding 同 R1：agent `a0b7cb41e09a556b4` = `gov-executor`／`claude-opus-4-8`／`high`。沒有 `diversity_lost`。 |
| Independence（治理 §2.3） | (1) R2 延續 Reviewer 自己的 R1 context（治理 §2.1、Bindings §3.5 第 1 項），未繼承 Executor 的對話；已從磁碟重讀修正後的檔案與 `git diff 4ec20b5..386f30a`；worklog 的 closure 主張一律當作待驗證主張。(2) Binding 見上一列。(3) 自主取得：Reviewer 自行跑測試、查 CI log，並以自寫的 CDP client 驅動 headless Chrome 渲染、互動與量測（scratchpad `r2/`，沿用 R1 自寫的 `cdp.py` 與 band-spanning 合成 DB）。(4) 本紀錄由 Reviewer 以自己的 Write 工具寫入。 |
| 日期 | 2026-09-24 |

## 1. Subject 與環境核對

- `git rev-parse HEAD` = `f9f9f15…` = remote。`git diff 386f30a --stat -- home_work_01 ':!home_work_01/doc'` 為空：工作樹的實作等於 `386f30a`。本機 server 回傳的 `/static/app.js` md5 `7695980e…` = `git show 386f30a:home_work_01/static/app.js | md5sum`。
- `git diff --stat 4ec20b5..386f30a -- home_work_01/{app.py,server.py,weather_query.py,vercel.json,requirements.txt,data.db,api,static/vendor,tests/test_static_checks.py}` 為空：這些檔案都未被修正觸及。
- `git diff --check 4ec20b5..f9f9f15` 乾淨；兩個新 commit 的 message 是 `[Modify] – …` 格式，沒有 Claude 標記。
- 瀏覽器環境同 R1：127.0.0.1:8761 正常 `data.db`、8762 band-spanning 合成 DB（`wq.snapshot_status` = ok）、8763 不存在的 DB；Chrome 153 headless；1280×900 desktop 與 375×812 mobile＋touch。結束時已停止 server 與 Chrome。

## 2. Blocking findings 的 closure

### F-1（AC-18／R-EN-4：切換日期後開著的 popup 顯示舊值）— **已解決**

- **修正內容**：`applyDay` 第一次綁定 tooltip／popup，之後以 `setTooltipContent`／`setPopupContent` 就地更新（`app.js:395-411`）。Leaflet 1.9.4 的 `setPopupContent` 會重繪已開著的 popup。
- **Reviewer 驗證（自己的 render）**：對六個 marker 各做一次：在 2026-09-24 點開 popup，popup 保持開著，依序把 `Select Date` 切到 09-25 → 09-28 → 09-30 → 09-24。每次切換後比對 popup 全文與該日 `/api/days/<date>` 的 Region／`Date`／`Min`／`Max`／導出值（一位小數），同時比對六個 marker 的 `fill`、側欄 info card 的日期與值、caption 與 `date-select.value`。四種組合 × 30 次檢查（6 次開 popup＋24 次切換）**全部相符**：
  - 合成 DB 1280：例如 北部地區 popup 由「Date: 2026-09-24 Min: 15°C · Max: 24.8°C … 19.9°C」變為「Date: 2026-09-25 Min: 31°C · Max: 35°C … 33.0°C」，marker `#e03131`（red），側欄 `北部地區／2026-09-25／31／35／33.0`。南部地區 popup → 2026-09-25、22／26、24.0，marker `#2f9e44`（green）。
  - 合成 DB 375、真實資料 1280、真實資料 375：同樣全部相符（例：真實資料南部地區 popup 由 2026-09-24／29.2 變為 2026-09-28／26.3／32.7／29.5）。
  - hover 中的 tooltip 在切換日期時也就地更新：東北部地區 tooltip 由「2026-09-24 … 30.0」變為「2026-09-25 Min: 26°C · Max: 28°C … 27.0」（合成 DB，1280 與 375）。
  - 切換後再逐一 hover 六個 marker，tooltip 全部是新日期的值。
  - popup 開著時切到回 503 的日期 → 地圖區塊隱藏、顯示 inline error；再切到正常日期 → 地圖恢復，同一個 popup 顯示新日期的值（中部地區 → 2026-09-25／10／12／11.0）。
  - `Runtime.exceptionThrown` 0 筆，console 錯誤 0 筆，non-same-origin 請求 0 筆。
- popup、它所屬的 marker 與側欄都顯示所選日期的值。側欄在切換後重設為北部地區（R1 F-5(b)），所以 popup 開在其他 Region 時，兩者顯示不同 Region，但都是同一天的正確值，不構成不一致。
- **判定**：AC-18 的「切換日期後…資訊卡值隨之更新，與該日 endpoint 值一致」現在 PASS。

### F-2（AC-27：死 CSS 與過時註解）— **已解決**

- `styles.css` 的 `.control--reserved` 與整段 `.placeholder*` 已刪除；`index.html:62-63` 的註解改為「Controls: Select Region (chart/table) and Select Date (Taiwan Map), integrated on one page (R-EN-7).」；`app.js` 檔頭的 DR-19 說明補上地圖卡片的 inline 狀態（R1 列為次要項）。
- `grep -n -i "placeholder\|reserved\|coming soon\|NOT implemented" static/{styles.css,index.html,app.js}` → 0 筆。Reviewer 把 `styles.css` 的每個 class selector 與 `index.html`／`app.js` 比對，沒有找到的只有 `chart__dot--maxt／mint`、`chart__line--maxt／mint`、`state--inline-{loading,error,empty}`（皆由 JS 字串組合產生）與 `leaflet-container`（由 Leaflet 加上），沒有死規則。
- **沒有版面回歸**：地圖容器、台灣輪廓與六個 marker 的 bounding box 在 1280（map `[124,988,792,1368]`）與 375（map `[32,1652,343,1972]`）都與 R1 的量測逐像素相同；375 `scrollWidth` 375 = `innerWidth`，1280 為 1265（垂直捲軸）。
- **判定**：AC-27（本票範圍）R-DOC-5 (1)、(3) 現在 PASS；(2)、(4) 維持 R1 的 PASS。

## 3. 併修的 F-3（non-blocking，亂序回應）— **已解決**

- **修正內容**：`loadDay` 以 `mapReqSeq` 標記請求（`app.js:103, 337`），`.then` 與 `.catch` 開頭都檢查 `seq !== mapReqSeq` 就丟棄（`app.js:342, 365`）。只改同一組函式，沒有擴大範圍（`loadRegion` 未動，與 R1 的說明一致）。
- **Reviewer 驗證**（合成 DB，CDP `Fetch` 暫停第一個 `/api/days/2026-09-24` 請求，之後才放行）：
  - A：選 09-25 → 09-24（暫停）→ 09-25，放行成功的 09-24 回應：畫面維持 09-25（`fill` `#e03131,#2b6cb0,#2f9e44,#f2b705,#2b6cb0,#e03131`、側欄 2026-09-25／33.0、沒有狀態訊息）。R1 在同一操作下得到的是 09-24 的顏色。
  - A375：375 px、popup 開著，同上操作：維持 09-25，popup 也維持 09-25。
  - B、C：被取代的請求在放行時回 503 或網路失敗：畫面維持最後選的 09-26，沒有出現 inline error。
  - D：09-24（暫停）→ 09-25 → 09-24（新請求）→ 09-25 → 09-24，之後放行被暫停的請求，並把它的內容改成 band 全為 red：畫面採用新請求的正確 09-24 值，改過的舊回應被丟棄。
  - E（沒有被取代，控制組）：選 09-25 → 09-24（暫停）；放行前是 inline loading，放行後套用 09-24，popup 也更新為 09-24。
  - 以上 `Runtime.exceptionThrown` 皆 0 筆。
- R1 為 F-3 記的 disposition（追蹤到 #25）不再需要。

## 4. 回歸核對

| 項目 | 結果 | 證據 |
| --- | --- | --- |
| 測試 | **PASS** | 本機 Python 3.12.14：`pytest -q -p no:cacheprovider` → **152 passed in 3.19s**；`tests/test_app.py tests/test_static_checks.py tests/test_dashboard.py tests/test_weather_query.py` → 83 passed。 |
| CI | **PASS** | `gh run view 35943197399`：push，headSha `386f30af…`，全部 step success；log：`Python 3.12.14`、`collected 152 items`、`152 passed in 3.79s`、`credential scan passed: 506 tracked files; …`。pull_request `35943204314`（`386f30a`）與 `f9f9f15` 的 push `35943302812`、pull_request `35943305007` 也都 success。 |
| 新增的測試斷言 | **PASS**（強化，沒有弱化） | `tests/test_dashboard.py:67` `assert ">Select Date</label>" in html`；它在本 subject 成立，把標籤改成其他字時會失敗（Reviewer 以字串 mutant 確認）。原有斷言全部保留。這也處理了 R1 的 F-6（Low）。 |
| AC-17（42 個 marker＝endpoint、置中、六個 marker、縮放、圖例、導出註記） | **PASS** | 重跑 R1 的 map 檢查：真實資料 7 天 × 6 區與合成 DB 7 天 × 6 區，marker `fill`、tooltip、側欄全部等於 endpoint；六個 marker 都在容器內，形心偏移 1280 (+9.8, −0.5) px、375 (+10.3, −0.5) px；zoom-in 間距 ×2.00（1280）、×1.19（375），zoom-out 恢復；圖例 swatch 顏色＝`BAND_COLOURS`。 |
| R-EN-3／AC-18 清單 | **PASS** | 7 個 option，等於 `/api/days`、升序、預設第一天（1280、375）。 |
| R-EN-6 | **PASS** | 全部渲染的請求都是同源（`/`、`/static/*`、`/static/vendor/*`、`/api/*`），non-same-origin 0 筆，`.leaflet-tile` 0 個。`static/vendor/` 不在修正 diff 內。 |
| AC-19 重驗（375 無橫向捲動、地圖在手機可用） | **PASS** | 375×812 mobile：`scrollWidth` 375；tap 開 popup、切換日期、tap 縮放都正常；1280 版面與 R1 相同。 |
| DR-19／N-1 | **PASS** | 重跑 R1 的 18 個攔截情境，結果與 R1 相同：`/api/regions` 或 `/api/health` 回 200 非 JSON、200 空 body、500，以及缺 DB 的真實 503 → 頁面 error；`{"regions": []}` → 頁面 empty；`/api/days`、`/api/days/<d>` 回非 2xx、200 非 JSON 或網路失敗 → inline error（`role="alert"`）；`{"days": []}`、`{"values": []}` → inline empty；暫停請求時顯示 loading。例外 0 筆。 |
| INV-2 | **PASS** | `test_inv2_series_equals_shared_module_for_all_regions` PASS；瀏覽器中六個 Region 的表格等於 `wq.region_series`（合成 DB）。修正沒有改到圖表與表格的渲染程式。 |
| INV-9／AC-26 | **PASS** | `app.py`、`weather_query.py`、`requirements.txt` 不在修正 diff；`tests/test_app.py`（`AppTest`）與 AC-26 靜態檢查 PASS。 |
| AC-04(b) | **PASS** | `tests/test_static_checks.py` 與 `static/vendor/` 都未改；三個前端檢查 PASS。新增程式碼沒有新的 URL，也沒有新的請求目標。 |
| AC-28（前端側） | **PASS** | 修正沒有加入任何推導或門檻；著色仍是 `BAND_COLOURS[v.colourBand]`。 |

## 5. 高風險類別核對重述（A-1）

- **H-3（Derived Map Temperature 的等價性與「導出」標示）**：修正後，前端仍然不重算導出值或色帶；`weather_query.py`、`server.py` 不在修正 diff 內；AC-28 的五組 pytest PASS。R1 列為 H-3 例外的情況（popup 在切換日期後顯示與所選日期不一致的導出值）已經消除：在 1280 與 375、真實資料與跨四個色帶的合成 DB 上，popup、tooltip、側欄的導出值都等於所選日期的 endpoint 值（§2 F-1）。亂序回應也不會再讓舊日期的導出值與顏色蓋過目前的選擇（§3）。導出標示（圖例註記、側欄「(derived, not an observed daily mean)」、tooltip／popup「(derived)」、README:271-278）都未改動。**判定：PASS。**
- **H-2（`Select Date`、`Min`／`Max` 文字）**：`index.html` 的修正只改了一段註解，`<label for="date-select">Select Date</label>`、`<h1>`、`Select Region`、表頭都沒動；tooltip／popup 仍使用 `Date`／`Min`／`Max`；新增的 `>Select Date</label>` 斷言把這個評分用詞納入自動化保護。`app.py`、DDL、`data.db` 不在 diff。**判定：PASS。**

## 6. 新的 non-blocking 觀察

### N-1 — 靠近地圖邊緣的 marker，其 tooltip／popup 會被地圖容器裁切（修正 R1 F-5(a) 所描述的範圍）

- **Severity**：Low　**Blocking**：否
- **證據**：Reviewer 量測每個 marker 的 tooltip 與 popup 超出 `#map` 容器的像素數（正數表示被裁切）。1280：北部地區 tooltip 上緣 36 px、popup 上緣 49 px；東北部地區 tooltip 5 px、popup 18 px。375：北部地區 popup 上緣 78 px、右緣 47 px；東北部地區 popup 上 47／右 69 px；中部地區 popup 左 39 px；南部地區 popup 左 69 px；東部地區 popup 右 52 px；東南部地區 popup 右 11 px（tooltip 的數值較小，但分布相同）。北側 marker 被裁掉的部分包含 Region 名與 `Date` 列；Executor 的 `issue-24-f1-popup-updates-375.png` 也看得到這一點。
- **來源**：不是這次修正造成的。tooltip／popup 的選項（`direction: "top"`、`offset`、`autoPan: false`）在修正前後相同，R1 的 subject 也有同樣情況（R1 自己的 `stale-popup-synth.png` 就看得到上緣被裁）。R1 的 F-5(a) 只描述了 375 px 東側 marker 的右緣，範圍寫得不夠完整，這裡補正。
- **為何 non-blocking**：R-EN-4／AC-17 要求「點擊或 hover 顯示資訊卡：Region、Date、Min、Max 與導出平均」。側欄 info card（`#map-infocard`）在 hover 與 click 時都會更新，並完整顯示這五項，不會被裁切（1280 在地圖旁邊，375 在地圖正下方）；所以契約條款已經滿足，被裁切的只是地圖上重複顯示的 overlay。這不違反任何 accepted 條款，也不是這次修正直接產生的 blocking defect。
- **Disposition**：owner Orchestrator，追蹤到 #25（最終驗證），或由 acceptor 之後以 Lightweight 單點修正處理。可行的修法例如 `autoPan: true`（或 `keepInView`）、tooltip `direction: "auto"`；屬 HOW。依治理 §4.4，這項不延長本 cycle。

### 其他

- R1 的 F-4（AC-04(b) 自動檢查不掃 `static/vendor/`，Low，owner #25／Executor）維持原 disposition：修正依派工指示沒有動 vendor 與靜態檢查。F-5(b)(c) 維持 R1 的 disposition（Executor 自行決定）。
- worklog 把 `doc/acceptance/screenshots/` 稱為 record-only；依 Bindings §7，record-only 只有 `doc/governance/**`。這兩張截圖已在 `386f30a` 內，是受審 subject 的一部分，不影響本結論。

## 7. 結論

- F-1：已解決。F-2：已解決。F-3（non-blocking）：已解決。F-6（Low）：已由新增的測試斷言處理。
- 修正沒有造成回歸：測試 152 passed、CI 綠、AC-17／AC-18／AC-19／R-EN-6／DR-19／N-1／INV-2／INV-9／AC-26／AC-04(b)／AC-28 前端側都維持 PASS；H-2、H-3 PASS。
- 修正沒有直接產生或暴露新的 blocking defect。新的 non-blocking N-1 已記錄 owner（Orchestrator → #25），不延長 cycle。
- 沒有需要 Design Authority 裁決的 routing signal。#24 cycle 1 audit closure。

VERDICT: CLOSURE
