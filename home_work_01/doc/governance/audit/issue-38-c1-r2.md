# Audit record — Issue #38，cycle 1，R2（scoped closure review）

| 欄位 | 內容 |
| --- | --- |
| Work Contract | GitHub Issue **#38**（`yotsubamomo/aiot-classwork`）；契約與分配同 R1 record `home_work_01/doc/governance/audit/issue-38-c1-r1.md` 表頭（V2 Outcome Contract `69c5a04`；SPEC-V2 **v2.2**；DV-20 §4.1；DV-21 §4.1、§4.2；decision A-1）。本 R2 只核對 R1 的 blocking finding **F-1**（R-V2-DD-9(e)、R-V2-RSP-6）是否解決、修正是否引入回歸、是否直接產生或暴露新的 blocking defect（治理 §4.4 R2 三項）。 |
| 受審 subject | branch `home_work_01-v2-implementation`；BASE **`de004f43b13ee1de1fc923b772f7bbb816b22656`** .. HEAD **`2239ac353a4697515b24f256d9755cf4f0721124`**；修正後 code anchor **`286ee9dde6f519aa15303e42c8bb0f319eb6ed90`**。Correction delta ＝ **`2f34843..286ee9d`**：非紀錄檔只有 `286ee9d` 一個 commit（`README.md`、`static/app.js`、`static/data/counties.js`、`static/styles.css`、`tests/test_county_frontend.py`、`tests/check_county_browser.py`、`doc/acceptance/screenshots/v2/issue-38/*`）；其間的 `1bdcbe7`、`6656fd2`（run record）、`94835ed`（R1 record）與其後的 `2239ac3`（worklog）、`7d984db`（run record，審查時本機 HEAD）皆 record-only（Bindings §7）。單元目錄外 0 檔。Working tree 的 code 與 `286ee9d` 相同。 |
| Audit 種類 | **R2**（scoped closure review；治理 §4.4），**cycle 1**。不是第二次全面審查。 |
| 角色 | `primary_reviewer`（definition `gov-primary-reviewer`；Bindings §3.1 mapping `claude-opus-5-5`／`xhigh`） |
| Binding 證據 | 正式核對由派工者依 Bindings §3.4 記入 run record `home_work_01/doc/governance/run/run-20260925-hw01-v2-formal.md`（R1 列記 `aee926af828c07bf6`；correction 列記 Executor `a85542bddce5a490b`）。Reviewer 以 Bindings §3.4 指令再次讀 harness 紀錄（session `05b8408b-260a-46d3-a4fe-ec07e3ec365a`）：`agent-aee926af828c07bf6` `gov-primary-reviewer` `[('claude-opus-5-5', 'xhigh')]`（本 Reviewer；R1 與本 R2 同一 agent，225 則 assistant 訊息皆此 binding）。此觀察只供對照，不取代派工者的核對。 |
| Independence（治理 §2.3、§4.6） | (1) **Context**：依治理 §2.1／§2.3 與 Bindings §3.5，R2 延續 Reviewer 自己的 R1 context（同一 agent 續派），未繼承 Executor 的對話；**已從磁碟重讀**修正後的 `git diff 2f34843 286ee9d`（程式、README、測試、evidence）與 worklog 更新 `git diff f68f7e8 2239ac3`，Executor 的「已修正」與 worklog C-1～C-6 一律當作待驗證主張。(2) **Binding**：見上一列。(3) **Autonomous access**：自行重跑全套測試、BASE／R1 subject test id 比對、CI log、憑證掃描；**自寫** R2 焦點走查 `rv38_r2.py`（與 Executor 新增的 Tab-walk 情境無共用程式，只沿用單元既有 DevTools driver 與未修改 `create_app` 的 Rig）；原封重跑 R1 的自寫檢查 `rv38.py`；重跑 Executor 的 #36／#37／#38 檢查（輸出導向 scratchpad）；對 #36 檢查的間歇失敗自寫診斷 `diag36.py`，並以 `git archive` 匯出 BASE `de004f4` 與 R1 subject `2f34843` 兩棵樹對照。全部在 Reviewer scratchpad、未提交。(4) **Self-written record**：本紀錄由 Reviewer 以自己的 Write 工具寫入。**Model diversity：`diversity_lost`**——Executor 與 Primary Reviewer 同為 `claude-opus-5-5`（Bindings §5、b2 override；decision A-7）。這是合法狀態，不減損 §2.3 的 independence。 |
| 日期 | 2026-09-26 |

## 1. 修正內容（Reviewer 自讀 diff）

- `static/app.js` `buildCountyLayer`（`:1309-1322`）：每個縣多邊形在每次 `add` 事件時對其 path 元素設 `tabindex="-1"`（Leaflet 每次把圖層加回地圖都重建 path，故綁在 `add`）；註解說明原因（tooltip 使 Leaflet 綁 focus 監聽 → Chromium 放進循序焦點）與 DD-9(a)(d)。沒有其他邏輯變更。
- `static/styles.css`：只改 `path.leaflet-interactive:focus { outline: none; }` 上方註解（規則保留，只針對滑鼠點擊的焦點）；`.station-icon--county .spill { height: 24px }` 等其他規則未動。
- `static/data/counties.js`：只改檔頭註解（F-4）。`README.md`：縣界段改為「只從本應用同源載入、無外部請求」並註明縣形狀不是 Tab 停駐點、County 選單是鍵盤路徑（F-4）。
- 測試：`test_county_frontend.py` 新增 `test_county_polygons_are_never_keyboard_tab_stops`（只加）；`check_county_browser.py` 新增 Tab-walk 情境並把它加入兩個情境清單（`git diff 2f34843 286ee9d -- tests` 的刪除行只有這兩個清單行，皆被擴充後的同一行取代，無斷言移除）。
- Worklog（`2239ac3`）：記 correction、F-3 的 DOM／可視措辭更正、F-4、R1 處置後狀態。
- 範圍：只限 F-1 與兩個 R1 non-blocking 的文件／措辭（F-3 措辭、F-4），沒有夾帶無關變更或重新設計（治理 §4.4 targeted correction）。F-2、County view 標記 44×24、375 版面未動。

## 2. F-1 是否解決——**已解決**

Reviewer 自寫 `rv38_r2.py`：對每個焦點停駐點自行分類——是否為縣 path、焦點指示是否可見（聚焦時 computed `outline-style`／`outline-width` 或 `box-shadow`）、是否完全被遮蔽（元素矩形中心與四角共 5 點以 `elementFromPoint` 命中本元素或其子孫的點數）、是否為可操作種類（原生控制、`role="button"` 標記、地圖容器、縮放按鈕；其他一律列為 unknown）；並實際啟動停駐點（地圖容器按 → 應平移、第一與最後一個標記停駐點按 Enter 應選取該站並開詳情、縮放按鈕按 Enter 應改變 zoom）。每個情境做兩種走查：自 `#map` 起到焦點離開地圖；自 `Now` 模式按鈕起經整個 Now 卡片到下方 `Select Region`。

| 視野 | 情境 | 22 條縣 path `tabindex` | 自 `#map` 走查 | 整張 Now 卡片走查 | 停駐點實際作用 |
| --- | --- | --- | --- | --- | --- |
| 1280×900 | 全臺視野 | 全為 `-1` | 22 個代表標記＋2 縮放按鈕；0 path；全部可見、無完全遮蔽 | 模式／Refresh 按鈕、County 選單、地圖、22 標記、縮放、`Select Region`；0 path；0 unknown | 地圖 → 平移；標記 Enter → 選站＋詳情（首、末）；縮放 Enter → zoom 變 |
| 1280 | 臺中市縣視野＋選一站 | 全為 `-1` | 只有 2 縮放按鈕（County view 標記依設計 `tabindex=-1`，清單為其鍵盤路徑）；0 path | 含 `Back to Taiwan` 與 60 個清單按鈕；0 path；全部可見 | 同上（無標記停駐點） |
| 1280 | 花蓮縣，**Now→Forecast→Now 往返後**（path 被重建） | 全為 `-1`；Forecast mode 時 overlay pane 互動 path 為 0 | 同上；0 path | 含 61 清單按鈕；0 path | 同上 |
| 1280 | **Unavailable**（`upstream_error` 500）＋臺中市 | 全為 `-1` | 同上；0 path | 0 path；全部可見 | 同上 |
| 1280 | **Stale**（`upstream_error` 429）＋花蓮縣 | 全為 `-1` | 同上；0 path | 0 path；全部可見 | 同上 |
| 375×812 | 上列五個情境各一次 | 全為 `-1` | 同 1280 的分類結果；0 path | 同上；0 path；全部可見、無完全遮蔽 | 同上 |

- 結果：**45 項檢查 45 PASS**（`rv38_r2.py`）。所有情境、兩個視野：**沒有任何縣 path 是 Tab 停駐點**；**沒有不可見或無作用的停駐點**；每一停駐點都有可見焦點指示且未被完全遮蔽——**R-V2-DD-9(e)、R-V2-RSP-6 成立**；DD-9(d)（多邊形不必可聚焦）與實作一致。
- 指標路徑未回歸：hover 花蓮縣 → path `stroke-opacity 1`＋tooltip「花蓮縣」、path 帶 `tabindex="-1"`；點選 → County 脈絡＝`/api/` 自算。點選後 `document.activeElement` 為 `BODY`（未留下隱形焦點），再按 Tab 進入 `Back to Taiwan`（`outline: solid 3px`、可命中）。
- 新靜態守衛有鑑別力（Reviewer 於記憶體中對 `app.js` 的 scratch 複本做兩個變異，未寫入 repo）：移除 `setAttribute("tabindex", "-1")` → 守衛 `AssertionError`；把 `add` 監聽改成 `remove` → 守衛失敗（`ValueError`）；原檔 → PASS。
- R1 當時用來證明 F-1 的探測（BASE→subject 自 `#map` Tab 的序列）在修正後：自 `#map` 第一個 Tab 即到代表標記，與 BASE 相同。

## 3. 回歸核對（不重開已 PASS 項目，只確認未回歸）

| 項目 | 結果 | 證據 |
| --- | --- | --- |
| **DV-20 §4.1** (i)(ii)(iii) | **仍 PASS** | 原封重跑 R1 的 `rv38.py`：1280（地圖點選臺中市）與 375（選單花蓮縣）往返，回來的 Leaflet center／zoom 與離開時完全相等、選縣與 County 脈絡＝`/api/`、選測站與詳情恢復。 |
| **DV-21 §4.1 (1)(2)(3)＋§4.2** | **仍 PASS** | 同上：Unavailable（1280 地圖＋鍵盤、375 鍵盤）四值「—」且脈絡無任何數字、無清單、狀態行、Refresh 可用、Back to Taiwan、Refresh 成功後＝新 `/api/`；Stale（失敗前／後選縣、not-newer 與 newer 清除、375 `invalid_response`）；零有效金門縣（自製樣本）`0`／「—」且無狀態標示。 |
| AC-V2-10、AC-V2-12、AC-V2-23 | **仍 PASS** | `rv38.py` 對應各行 PASS（22 縣脈絡＝自算、清單 Tab／Enter／Space、詳情＝`/api/`、圍欄外東沙島、`Back to Taiwan` 回初始視野）。`rv38.py` 本輪 68 PASS／2 FAIL——兩個 FAIL 與 R1 §8 已說明的檢查假陽性完全相同（澎湖縣 5 px 格點、金門縣縣視野多邊形被標記覆蓋）；R1 時失敗的 F-1 對應行（全臺 Tab 走查）本輪 PASS。 |
| AC-V2-16／INV-V2-3 | **仍 PASS** | `rv38.py` 與 `rv38_r2.py` 全部情境的瀏覽器請求皆為 loopback，外部 0；已提交 `issue-38/network-log.json` 的 URL 亦 0 個非 loopback。 |
| V1 AC-19（375 無橫向捲動） | **仍 PASS** | `rv38.py` 375 各狀態 `scrollWidth ≤ innerWidth`。 |
| Executor 檢查重跑 | #38 **72/72**；#37 **97/97**；V1 `check_series_error_visible.py` PASS；#36 見下 | 輸出在 scratchpad `r2rerun36／37／38`。 |
| #36 `check_modes_browser.py` | **無回歸**（見 §4 N-1） | 本輪 6 次執行：3 次 37/37、3 次 36/37，失敗項一律為「B-desktop／B-375 AC-V2-09(a) Refresh works while the forecast snapshot is unavailable」。§4 證明這是 R1 之前即存在的檢查工具時序偽陽性，與本次修正及 #38 無關。 |
| 全套測試、test id、CI | **PASS** | `pytest -q` → **494 passed**；BASE `de004f4` 的 475 個 test id 與 R1 subject 的 493 個 test id **全部**仍在（`comm -23` 皆空），新增 1 個（`test_county_polygons_are_never_keyboard_tab_stops`）。CI `36210392148`（`286ee9d`）、`36210510564`（`2239ac3`）、`36210583457`（`7d984db`）皆 success，log 皆 `494 passed`、`credential scan passed: 648 tracked files`。 |
| 不變產物、H-1 | **確認** | `git diff --stat de004f4 286ee9d` 對 `app.py`、`weather_query.py`、`ingestion/`、`data.db`、`smoke.py`、`vercel.json`、`requirements.txt`、`server.py`、`api/`、`observation.py`、`representative.py`、`static/data/basemap.js`、`static/vendor/`、`.github/`、`doc/requirement/` → 空；`index.html` 自 `2f34843` 起未變。`python -m tools.credential_scan` passed（不讀 `.env`）。 |

**High-risk（decision A-1）重述**：修正只觸及 path 的 `tabindex`、註解、README 一段與測試，不觸及 County 脈絡計算、標示文字、資料著色或老師概念詞。R1 §5 的 **H-3**（無聚合、代表測站值不當縣值、**無資料 vs 零**）與 **H-2** 核對結論不變，並由上表 DV-21 (3) 與 #36 檢查中下方 dashboard／`Select Region` 項目（6 次皆 PASS）確認未回歸；H-1 未觸及。

## 4. 修正直接產生或暴露的缺陷——**無 blocking**

### N-1 — #36 瀏覽器檢查 `check_modes_browser.py` 情境 B 的間歇失敗是既有的時序偽陽性（Low，non-blocking；不是本次修正或 #38 造成）

- **現象**：`B-{desktop,375} AC-V2-09(a) Refresh works while the forecast snapshot is unavailable` 間歇失敗（本輪 6 次中 3 次），詳情為 Observation Time 仍是 `2026-09-25 23:00 +08:00`。
- **診斷**（Reviewer 自寫 `diag36.py`，重現該步驟並擷取頁面實際收到的兩個 `/api/observations/latest` 本文）：失敗時 Refresh 確實觸發（上游被呼叫 1 次、HTTP 200、本文為較新的 `2026-09-26T00:00` 觀測），頁面結果為 `data-refresh-result="not-newer"`、「Already the latest …」；**每一次失敗的兩個本文 Fetched Time 字串完全相同**（例：`2026-09-26T10:27:23+08:00` 與 `…10:27:23+08:00`），每一次成功則相差 ≥ 1 s。原因：該檢查的 Rig 以 `reuse_window_seconds=0` 與真實時鐘執行，Fetched Time 解析度為秒；首次載入與 Refresh 落在同一秒時，頁面依 **R-V2-OBS-8**「回應的 Fetched Time 與目前顯示者相同 → 同 (b) 的告知、無變更」正確判為 not-newer。
- **不是回歸**：同一診斷在三棵樹各跑 16 次——BASE `de004f4`（#38 之前）**3／16** 失敗、R1 subject `2f34843` **6／16**、修正後 `286ee9d` **2／16**，每次失敗都是同秒 Fetched Time。本次修正與 #38 皆未改動 Fetched Time 比較（該規則屬 #37 已稽核的 `applyObservation`）。產品行為符合 R-V2-OBS-8 原文，不是產品缺陷，不需 Design Authority。
- **Disposition**：檢查工具的可靠性問題。Owner：**Orchestrator 追蹤**，於下一個修改 `check_modes_browser.py` 的票或 **#41**（最終 V2 evidence）處理（例如像 `check_refresh_browser.py` 那樣注入可控時鐘，或確保兩次取得的 Fetched Time 不同）。Spec Integration Audit 重跑此檢查時，單次 36/37 應先核對兩個本文的 Fetched Time 再判定。另記：Executor worklog C-3 與 R1 時的「37/37」皆為單次執行結果，未反映此間歇性。不延長本 cycle。

## 5. R1 non-blocking findings 與交接的狀態

| R1 項目 | 狀態 |
| --- | --- |
| **F-2**（初始全臺視野多數縣多邊形無法以指標命中） | 未動（本次修正與它無關；`tabindex` 不影響指標命中）。仍交接 **#39**（R-V2-RSP-7）與 Spec Integration Audit。 |
| **F-3**（選縣後面板自動捲動使 chip／原因離開可視區；worklog 可見性措辭） | worklog V-5 DV-21 (1)(2) 兩段已改為「chip 與原因存在於 DOM、選縣後在面板可視區外、捲動即見；可見的是 County 狀態行與地圖內告示」，與 R1 量測一致。面板版面未動，仍交 **#39**。 |
| **F-4**（同源請求敘述） | `counties.js` 檔頭改為「瀏覽器只從本應用同源取得、無外部請求」；README 同步——與 Reviewer network log（`/static/data/counties.js` 為同源請求）一致。已更正。 |
| County view 標記 44×24、大縣標記重疊、375 County 脈絡位置 | 未動（`styles.css` 的 `height: 24px` 仍在）；仍交接 **#39**。 |

## 6. Routing

- **Design Authority**：無。**Acceptor（reserved）**：無。

## 7. Evidence 索引（Reviewer 自產，皆在 Reviewer scratchpad，未提交）

- `rv38_r2.py`、`rv38_out/r2_results.json`（F-1 closure，45/45）；`rv38.py` 重跑紀錄 `rv38_r2regr.log`（68 PASS／2 已知假陽性）；`diag36.py` 與三棵樹的診斷輸出（N-1）；Executor 檢查重跑輸出 `r2rerun36`、`r2rerun36_1…4`、`r2rerun37`、`r2rerun38`；BASE 與 R1 subject 匯出樹 `base/`、`r1tree/`。
- `pytest -q` 494 passed；test id 比對（BASE 475、R1 493 全在）；CI `36210392148`、`36210510564`、`36210583457` success；`tools.credential_scan` passed。

VERDICT: CLOSURE
