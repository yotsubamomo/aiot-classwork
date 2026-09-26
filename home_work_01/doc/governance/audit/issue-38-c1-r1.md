# Audit record — Issue #38，cycle 1，R1（Formal Ticket independent audit）

| 欄位 | 內容 |
| --- | --- |
| Work Contract | GitHub Issue **#38**（`yotsubamomo/aiot-classwork`）「Taiwan → County → Station 下鑽：縣界互動圖層、County 脈絡、測站清單與詳情、Back to Taiwan、鍵盤路徑」（`gh issue view 38`：OPEN，含 DV-20／DV-21 追加）。上位：V2 Outcome Contract `home_work_01/doc/governance/outcome-contract-v2.md`（ACCEPTED 2026-09-25，normative candidate `69c5a04`）；Delta Spec `home_work_01/doc/spec/SPEC-V2.md` **v2.2**（§1.2 Δ-11／Δ-12、§2.3 R-V2-DD-1、DD-4～DD-9、DD-11、R-V2-MODE-4、R-V2-MODE-5(a)（選縣部分）、R-V2-DEG-2（縣界互動與脈絡部分）、R-V2-OBS-6（County 脈絡欄位）、R-V2-OBS-10(a)（互動圖層部分）、§2.6 R-V2-RSP-6（部分）、§2.8 R-V2-DOC-1(3)、INV-V2-3／5／7）；derivation record `derivation-SPEC-V2.md`（DV-3、DV-9、DV-10、§15）；decision **DV-20** `decisions/decision-20260926-ac-v2-01-county-round-trip-allocation.md` §4.1；decision **DV-21** `decisions/decision-20260926-county-layer-under-stale-unavailable-allocation.md` §4.1、§4.2；V1 DR-20 P-2(c)；`decisions/decision-20260923-high-risk-categories.md`（A-1）。本票分配：AC-V2-01（選縣往返部分）、AC-V2-08(a)(b)（縣界互動與脈絡部分）、AC-V2-10、AC-V2-12、AC-V2-23（`Back to Taiwan`）、AC-V2-16（縣界圖層部分）、V1 AC-19 的 375 px 無不必要橫向捲動（選縣／選測站狀態）、AC-V2-20（CI 全綠）、README R-V2-DOC-1(3)。Out of scope：#39 圍欄／縮放儀器、完整 375 px 資訊面、44×44、密度管理；#40 Radar；Later 項目。 |
| 受審 subject | branch `home_work_01-v2-implementation`；BASE **`de004f43b13ee1de1fc923b772f7bbb816b22656`** .. HEAD **`f68f7e8d824e8b0baf57452db81a8a6d84cc99c7`**；code anchor **`2f34843dbff99eb978a02d664a520f968e2778f2`**。`2f34843..f68f7e8` 只有 `doc/governance/worklog/issue-38.md`；審查時本機 HEAD `1bdcbe7`（`f68f7e8..1bdcbe7` 只有 run record）——兩者皆 record-only（Bindings §7）。`de004f4..2f34843` 的 30 檔全部在 `home_work_01/` 內（單元目錄外 0 檔）。Working tree 的 code 與 `2f34843` 相同（`git diff --stat 2f34843 HEAD -- home_work_01 ':!home_work_01/doc/governance'` 空）。 |
| Audit 種類 | **R1**（Formal 必做的 Ticket independent audit；治理 §4.1、§4.4），**cycle 1**。不是 Spec Integration Audit。 |
| 角色 | `primary_reviewer`（definition `gov-primary-reviewer`；Bindings §3.1 mapping `claude-opus-5-5`／`xhigh`） |
| Binding 證據 | 正式核對由派工者（Orchestrator）依 Bindings §3.4 記入 run record `home_work_01/doc/governance/run/run-20260925-hw01-v2-formal.md`（#38 Executor 列已記 `a85542bddce5a490b`）。Reviewer 另以 Bindings §3.4 指令讀 harness 紀錄（session `05b8408b-260a-46d3-a4fe-ec07e3ec365a`）自行觀察：`agent-aee926af828c07bf6` `gov-primary-reviewer` `[('claude-opus-5-5', 'xhigh')]`（本 Reviewer；第一則訊息即本次 #38 R1 派工）；`agent-a85542bddce5a490b` `gov-executor` `[('claude-opus-5-5', 'high')]`（#38 Executor）。兩者皆與 Bindings §3.1（b2 override）一致。此觀察只供對照，不取代派工者的核對。 |
| Independence（治理 §2.3、§4.6） | (1) **Fresh context**：未繼承 Executor 對話；worklog `issue-38.md`、commit message、已提交截圖與 `browser-check-results.json`／`network-log.json` 一律當作待驗證主張。(2) **Binding**：見上一列。(3) **Autonomous access**：自讀 `gh issue view 38`、SPEC-V2 v2.2、derivation record §15、DV-20、DV-21、decision A-1、DR-20 P-2、#36／#37 audit records、git 歷史與 diff、CI run 與 log；以 `git archive de004f4` 匯出 BASE 到 Reviewer scratchpad 比對 test id 與 BASE／subject 的瀏覽器行為；重跑 Executor 的三個瀏覽器檢查（輸出導向 scratchpad，不覆寫已提交證據）；另**自寫** probe（`join_check.py`、`rv38.py` 與 `rv38_probe／focus／focus2／under／views／tabbase／reach／m12／vis.py`，皆在 scratchpad、未提交）：只沿用單元既有的 DevTools driver 與未修改 `server.create_app` 的測試台（Rig），**oracle 全部自寫**——County 脈絡期望值由頁面實際收到的 `/api/` 本文依 SPEC-V2 §5.3 範圍 E 與 README 平手規則自行計算；縣多邊形名稱 join 以自寫 ray-casting 點在多邊形內判定；地圖視野以頁面腳本載入前安裝的 `L.Map.addInitHook` 直接讀 Leaflet 實例的 center／zoom（不經標記反算）；自己的衍生樣本（金門縣零有效、臺中站可選欄位哨兵、臺中站變無效）。(4) **Self-written record**：本紀錄由 Reviewer 以自己的 Write 工具寫入。**Model diversity：`diversity_lost`**——Executor 與 Primary Reviewer 同為 `claude-opus-5-5`（Bindings §5、b2 override；decision A-7）。這是合法狀態，不減損 §2.3 的 independence。 |
| 日期 | 2026-09-26 |

## 1. 審查方法與環境

- **環境**：Windows 11；`home_work_01/.venv` Python 3.12；Chrome headless（DevTools protocol，`websocket-client`）；Node（只用來以唯讀方式載入 `basemap.js`／`counties.js` 兩個 global 供 Python 幾何計算）。
- **憑證**：Reviewer **沒有讀取** `home_work_01/.env`，沒有發出任何 CWA 請求。瀏覽器檢查全部對 loopback 上未修改的 `server.create_app`（觀測服務為真的 `observation.LatestObservationService`，上游為由已提交消毒樣本衍生的模擬，金鑰為哨兵字串）。
- **不寫入**：沒有 git 寫入、沒有修改追蹤中的檔案（本紀錄除外）；結束時 `git status --porcelain` 只有與本票無關、既存的 `grep.exe.stackdump`。
- **Commit 衛生**：`2f34843`、`f68f7e8` 兩個 message 皆為 `[Modify] – …` 格式，分類行 `[Additions]`／`[Modification]`／`[Fix]`；`grep -icE "claude|co-authored|generated with"` → 0。`git diff --check de004f4 2f34843`（排除 PNG）乾淨。

## 2. 分配 AC 的逐條結論

| AC／項目 | 判定 | 證據（Reviewer 自行取得） |
| --- | --- | --- |
| **AC-V2-10** hover → 突顯＋縣名 | **PASS** | 1280：以自寫幾何找出臺中市多邊形內、最上層為縣路徑的像素，CDP 合成滑鼠移入 → 該 path `stroke-opacity 1`、`fill-opacity 0.14`，county tooltip 文字「臺中市」。Unavailable 下同樣成立（見 DV-21 (1)）。 |
| **AC-V2-10** 點選 → 視野與 County 脈絡＝`/api/` 手算 | **PASS** | 臺中市（地圖點選）：縣名、`Valid stations 60`、`On the map 60`、`28.8 °C · 潭子`、`4.3 °C · 雪山圈谷`、清單 60 項且順序（氣溫降冪、同溫較小 `stationId`）與每項氣溫皆＝自算；標記 60 個全為 county-view 標記、全部上圖測站座標落在 `map.getBounds()` 內、無一在浮動面板下；恰一個多邊形為選取樣式。**臺北市**（最密）：鍵盤選單 → 19／19、極值＝自算；另以使用者路徑「先點新北市 → 在其縣視野點臺北市」選取 → 同值。**澎湖縣／金門縣**（離島）：選單選取＝自算（金門縣在初始視野外，選取後其上圖測站全在視野內）；兩縣在 z9／z10 以滑鼠 hover 顯示縣名、點選選取（probe）。**連江縣**（樣本中最少測站）：4／4、極值＝自算。**零有效**：見 DV-21 (3)。**全部 22 縣**：以不經地圖的鍵盤選單逐一選取 → 每縣脈絡＝自算、上圖測站全在視野內、恰一個選取多邊形（金門縣另以選取 path 的 bounding box＝自算投影的金門縣 bbox (551,412)-(1034,749) 確認為本縣）。無選取時面板：Observation Time、Fetched Time、`Valid stations 849`、`Refresh`（截圖目視）。**DOM 文字**：Now mode 可見文字無 average／mean／平均、無 real-time／live；`document.body.textContent` 全文命中只有 Forecast mode 的導出註記三處（「derived, not an observed daily mean」「Average = (MinT + MaxT) / 2, a derived value — not an observed daily mean.」×2），屬 AC 明列的例外。 |
| **AC-V2-12** 清單鍵盤、詳情、`Back to Taiwan`、非地圖路徑、圍欄外測站 | **PASS**（另見 F-1） | 1280：自 `Back to Taiwan` 按 Tab → 焦點在清單第 1 項（中心可被命中）；Enter → 詳情＝`/api/`（名稱＋` station`、`StationId`、`縣 · 鄉鎮`、該站 Observation Time 至分、氣溫；RH／風速／風向／氣壓／雨量／天氣＝`/api/` 值或「—」）；Tab 到第 2 項、Space → 詳情更新、清單 `aria-pressed` 與標記 `is-active` 各恰一個、焦點可見。375：自 `Back to Taiwan` Tab 到清單、Enter → 詳情＝`/api/`；焦點可見；`scrollWidth 375 ≤ 375`。哨兵：自製衍生樣本把臺中站 467490 的 RH／氣壓／風向／雨量設 `-99`、天氣 `X` → `/api/` 對應 `null`，詳情全為「—」。**`Back to Taiwan`**（鍵盤 Enter，1280 與 375）：選縣與選測站清除、選單回「All of Taiwan」、脈絡與詳情隱藏、標記回 22 個代表標記；1280 回來的視野 center／zoom 與頁面初始載入**完全相同**（Leaflet 實例讀數），且含本島四極點與澎湖（R-V2-MAP-4）。**非地圖路徑**：原生 `<select>`，方向鍵逐一選 22 縣皆成立（上列）。**圍欄外測站**：高雄市 `On the map` 顯示「57 (1 not on the map)」、`Valid stations 58`；東沙島 `468100`（116.73E）在清單中標示「not on the map」、無其標記（57 個標記）；鍵盤 Enter（1280）與 Space（375）開其詳情＝`/api/` 並顯示「Not on the map — outside the map range」。 |
| **AC-V2-01（選縣往返部分；DV-20 §4.1）** | **PASS** | 見 §3。 |
| **AC-V2-08(a)(b)（縣界互動與脈絡部分；DV-21 §4.1、§4.2）** | **PASS**（另見 F-3） | 見 §4。 |
| **AC-V2-23**（`Back to Taiwan` 錨點） | **PASS** | 選縣後 `#back-to-taiwan` textContent 逐字 `Back to Taiwan`、可見；未選縣時隱藏（在 `#county-context` 內）。 |
| **AC-V2-16**（縣界圖層部分）／INV-V2-3 | **PASS** | 靜態：`static/data/counties.js` 無絕對 URL、無 `opendata.cwa.gov.tw`、無 `CWA_API_KEY`、無請求形式（唯一「CWA」字樣是註解「the CWA `CountyName`」——既有靜態檢查與 V1 以來的解讀皆以 CWA 主機 URL／金鑰名為「CWA 字串」，`app.js`／`index.html` 自 #36 起即含可見文字「CWA」）；`test_static_checks.py` 的 `_FIRST_PARTY_FRONTEND` 只擴充加入 `data/counties.js`（Reviewer diff 核對）。**執行期**：Reviewer 自己的 10 段情境（1280／375；success、Unavailable 兩類、Stale 三類、往返、零有效、競態）全部瀏覽器請求皆為 `http://127.0.0.1:<port>/…`，**外部 0**；不同路徑只有 `/`、`/static/{app.js,styles.css,vendor/leaflet.{js,css},data/basemap.js,data/counties.js}`、`/api/{observations/latest,health,regions,regions/…/series,days,days/…}`、`/favicon.ico`。已提交 `network-log.json` 108 個 URL 亦全為 loopback。 |
| **V1 AC-19（375 px 無不必要橫向捲動；選縣／選測站狀態）** | **PASS** | 375×812（mobile emulation）：選縣、選測站、往返回來（選縣＋選測站）、Unavailable＋選縣、Stale＋選縣、選高雄市＋圍欄外詳情——`document.documentElement.scrollWidth` 皆 ≤ `innerWidth`（375）。完整 375 資訊面屬 #39。 |
| **AC-V2-20**（本票範圍：CI 全綠） | **PASS** | Subject `pytest -q` → **493 passed**（Reviewer 本機）；BASE（`git archive de004f4`）收集 **475** 個 test id，**全部**仍在 subject（`comm -23` 空），新增 18 個（`test_county_frontend.py` 15、`test_secrets.py` 參數化 3）。既有測試檔的變更只有 `_FIRST_PARTY_FRONTEND` tuple 加一項與 `V2_CODE` 清單加三項（只加不減、無斷言移除）。CI `36207033490`（headSha `2f34843`）success：log `493 passed`、`credential scan passed: 644 tracked files…`；`36207254045`（`f68f7e8`）success。 |
| **README R-V2-DOC-1(3)**（圍欄外測站規則） | **PASS** | README 新增「Now mode — Taiwan → County → Station」段的「Stations outside the map range」：範圍 lat 21.2–26.7、lon 117.6–122.9（＝SPEC-V2 §5.3 E＝`app.js:205` `MAP_RANGE`＝`representative.MAP_RANGE`，靜態守衛核等值）、東沙島例、計入、清單標示、可開詳情；另含平手規則、零有效縣、Stale／Unavailable 行為、縣界圖層來源。 |
| 不變產物（INV-V2-8 面） | **確認** | `git diff --stat de004f4 2f34843` 對 `app.py`、`weather_query.py`、`ingestion/`、`data.db`、`smoke.py`、`vercel.json`、`requirements.txt`、`server.py`、`api/`、`observation.py`、`representative.py`、`static/data/basemap.js`、`static/vendor/`、`.github/`、`doc/requirement/` → 空。本票為純前端＋文件＋測試。 |

**Spec 條款對照（本票 Traceability）**：R-V2-DD-1（22 縣逐字、離島三縣可選）——**成立**。R-V2-DD-4——hover／點選／不以資料著色（靜止時 22 條 path 樣式完全相同且全透明；選取／hover 顏色固定、與資料無關）／同源零外部請求／只在 Now mode（Forecast mode 下 overlay pane 內 `path.leaflet-interactive` 為 0、County 選單與脈絡隱藏）——**成立**（初始全臺縮放層級的指標可達性見 F-2）。R-V2-DD-5 (a)(b)(c)(d) 與末句——**成立**。R-V2-DD-6、DD-7、DD-8、DD-11——**成立**。R-V2-DD-9 (a)(b)(c)(d)——**成立**；**(e)——不成立**（F-1）。R-V2-MODE-4（縣互動只在 Now mode）、R-V2-MODE-5(a)（選縣部分）——**成立**。R-V2-DEG-2（縣界互動與脈絡部分）、R-V2-OBS-10(a)（互動圖層部分）、R-V2-OBS-6（脈絡欄位）——**成立**。R-V2-RSP-6（部分）——選取項與關鍵控制可見可達**成立**；「鍵盤焦點永不被完全遮蔽」**不成立**（F-1）。INV-V2-3、INV-V2-5——**成立**；INV-V2-7（觀測失敗面：縣界互動與脈絡）——**成立**。

## 3. DV-20 §4.1 — AC-V2-01 選縣往返（Reviewer 獨立重做）

視野讀數直接取自 Leaflet 實例（`getCenter()`／`getZoom()`，未經標記位置反算）。

| 視野 | 路徑 | 步驟與讀數 | (i) 選縣 | (ii) 視野 | (iii) 選測站 |
| --- | --- | --- | --- | --- | --- |
| **桌機 1280×900** | 地圖點選臺中市 | 縣視野讀數 → 清單以鍵盤 Enter 選第 3 站 → 以滑鼠點 `+` 縮放控制＋地圖聚焦後按 → 平移，離開視野與縣視野不同（zoom 與 center 皆變）→ 鍵盤 Enter `Forecast`（6 個 Region pill、overlay pane 無縣路徑、County 脈絡隱藏、`aria-pressed` 正確）→ 鍵盤 Enter `Now` | **PASS**：選單值、County 脈絡＝同縣且＝`/api/` 自算、恰一個選取多邊形 | **PASS**：回來的 center lat／lng 與 zoom 與離開時**完全相等**（差 < 1e-9；非縣視野、非初始視野） | **PASS**：詳情物件與離開前完全相同（同 `StationId`）、清單 `aria-pressed` 恰該站、標記 `is-active` 恰一個 |
| **375×812** | 鍵盤選單選花蓮縣 | 同上（縮放控制點擊、平移） | **PASS** | **PASS**（完全相等） | **PASS**；另 `scrollWidth ≤ innerWidth` |

截圖：Reviewer scratchpad `rv38_out/d-rt-roundtrip-returned.png`（桌機，回到 Now 後含 County 脈絡）、`m-rt-roundtrip-returned.png`。R-V2-MODE-5(a) 選縣部分的機制：`selectedCounty` 為模組狀態，只由 `selectCounty`（`app.js:1131`）與 `backToTaiwan`（`:1153`）寫入；`setMode`（`:394-409`）只存 `nowView` 並清 `hoveredCounty`；`syncMap`（`:458-481`）回 Now 時重新加入縣圖層並套樣式——與 #36 的視野／選測站保存同一機制。AC-V2-01 其餘部分（#36 結案 evidence）順帶抽驗未被破壞：#36 檢查重跑 37/37（見 §6）。

## 4. DV-21 §4.1 (1)(2)(3) 與 §4.2 — 縣界互動圖層與 County 脈絡在 Stale／Unavailable 下（Reviewer 獨立重做）

| 項目 | 判定 | 證據 |
| --- | --- | --- |
| **(1) Unavailable**——1280（首次載入 `upstream_error` HTTP 500） | **PASS** | `data-obs-state="unavailable"`、Now `aria-pressed="true"`；22 條縣互動 path 存在；hover 臺中市 → 突顯＋「臺中市」；**地圖點選**臺中市與**鍵盤選單**選花蓮縣：縣名正確，`Valid stations`／`On the map`／最高／最低四值皆「—」，`#county-context` innerText **無任何數字**（`/\d/` 不命中），清單 0 項、顯示「No stations to list: the Latest Observation is unavailable.」，County 狀態行「Latest Observation unavailable — no station data to show.」可見；`UNAVAILABLE` chip 與「Reason: … (HTTP 500) — upstream_error.」存在（面板可視區的細節見 F-3）；`Refresh` 可見且 `aria-disabled="false"`；仍在 Now mode。`Back to Taiwan`（鍵盤）清除選縣。再選臺中市後 Refresh 成功 → 保留的脈絡＝新 `/api/` 自算。無測站可 fit 時視野為多邊形、地圖可用。 |
| **(1) Unavailable**——375（`key_not_configured`） | **PASS** | 鍵盤選單選臺中市 → 同上全為「—」、無數字、無清單、狀態行；chip、原因、Refresh；`scrollWidth ≤ innerWidth`；Back to Taiwan；Refresh 成功後脈絡＝新 `/api/`。 |
| **(2) Stale**——選縣在失敗**之前** | **PASS** | 成功（樣本 h0）後鍵盤選花蓮縣（61／61、`27.0 °C · 和仁`、`8.7 °C · 合歡山`＝自算）→ Refresh 失敗（`upstream_error` 429）→ `stale`；脈絡名稱、四值、清單（id、氣溫、off-map 旗標、順序）與失敗前**完全相同**且＝保留回應自算；County 狀態行以「Stale — …」開頭、`STALE` chip 存在。 |
| **(2) Stale**——選縣在失敗**之後** | **PASS** | 仍為 Stale 時 hover 臺東縣（tooltip「臺東縣」）＋地圖點選 → 脈絡＝保留回應自算、Stale 狀態行與 chip 仍在；清單 Enter → 詳情＝保留資料；`Back to Taiwan` 可用（仍 stale）。not-newer Refresh（較舊 Observation Time）→ `success`／`not-newer`、Stale 清除、脈絡不變；再失敗（`upstream_unreachable`）→ Stale；newer Refresh → `success`／`newer`、Stale 清除、脈絡＝新 `/api/` 自算。375（上游非 JSON → `invalid_response`）：臺中市脈絡保留＝自算、Stale 狀態行、無橫向捲動。 |
| **(3) 無資料 vs 零（H-3）** | **PASS** | Reviewer **自製**衍生樣本（金門縣全部氣溫 `X`；+1 h）：成功回應下選金門縣 → `0`、`0`、「—」、「—」、清單 0 項、「No valid station in 金門縣 …」、**無** County 狀態行、`success`、無 chip。對照 (1)：Unavailable 下脈絡無任何數字、有狀態行與 chip。兩者在畫面文字與狀態標示上可辨。 |
| **§4.2** | **成立** | 1：`0` 只在存在 Latest Observation 而該縣零有效時出現（`renderCountyContext`，`app.js:1202-1235`：`!obs` 分支四值 `MISSING`、`renderCountyList` 不列項目）。2／3：Unavailable 全「—」、不顯示 0。4：縣名來自圖層屬性／選單，hover、選取、`Back to Taiwan`、鍵盤路徑可用。5：Stale 脈絡＝保留資料；Stale 標示在選縣時不消失（`renderObsState` 同步 County 狀態行，`:882-886`）。6：HOW。 |

## 5. High-risk 核對段（decision A-1）

**觸及類別：H-3、H-2**（H-1 未觸及——伺服器與金鑰路徑未改；仍核對如下）。

- **H-3（資料語義與標示；V2 延伸：觀測不聚合、代表測站值不當縣值、無資料 vs 零）**——**PASS**。
  - 程式：`renderCountyContext`／`highestStation`／`lowestStation`／`byTemperatureDesc`（`app.js:1106-1235`）只有計數（`list.length`、上圖數）與「選出一個測站」；新增程式無 `reduce`、加總、除以長度（Reviewer grep 新增行）。靜態守衛 `test_county_context_computes_no_aggregate` 通過。
  - 畫面：County 脈絡的極值以「值 °C · 測站名」呈現，並註記「Station values as published, per station; no county-level value is computed.」；county-view 標記 aria-label「… station, <縣>: air temperature … °C (Latest Observation, station value)」、tooltip「Station value, not a county value」；代表標記說明「a station value, not a county temperature」不變。Now mode 可見文字與全文無觀測用的 average／mean／平均（§2 AC-V2-10 列）。
  - 縣界圖層不以資料著色：靜止時 22 條 path 的 stroke／fill／opacity 完全相同且透明；以兩個不同資料變體載入時樣式相同（固定色 `#9ed0ff`／`#fbbf24`）。
  - **無資料 vs 零**：見 §4 (3)——Unavailable 全「—」且無任何數字；成功回應下零有效縣為 `0`／「—」且無狀態標示；兩者可辨。**PASS**。
- **H-2（老師指定介面／概念詞）**——**PASS**。`index.html` 的 diff 只在 Now 面板與一個 `<script>`；`Taiwan Weather Forecast`、`Select Region`、`Select Date`、`>Date<`、`MinT`、`MaxT` 的出現次數 BASE＝subject；`app.py`、`weather_query.py`、`ingestion/`、`data.db` 無 diff；#36 檢查重跑 37/37（含下方 dashboard 兩模式相同、`Select Region` 六名與七列表）。
- **H-1**——未觸及。`python -m tools.credential_scan` → passed（645 tracked files；不讀 `.env`）；`git ls-files` 無 `.env`；已提交 `issue-38/` evidence 無 `SENTINEL`／`Authorization=`／`opendata.cwa` 命中；新檔無 URL、無金鑰。

## 6. 變更風險（治理 §4.4）——對已稽核 #36／#37 程式的修改（Executor concern (4)）

| 被修改處 | 核對 | 結論 |
| --- | --- | --- |
| `fitToMarkers(bounds, maxZoom)`：加可選 `maxZoom`（預設仍 8）與 zoom 動畫期間延後套用（`app.js:1815-1833`、`:1752-1760`） | **BASE 與 subject 行為對照**（同一 Rig、同一瀏覽器、Leaflet 實例讀數）：1280、375、1024 三個寬度的「初始 Now 視野」「進入 Forecast 視野」「回 Now 視野」「放大後往返的 Forecast 與回 Now 視野」「寬度 resize 後的 re-fit」**逐一完全相同**。競態探測：選縣（動畫 fit）後 60 ms 內切 Forecast（臺中市、花蓮縣、屏東縣）→ 1.5 s 後 zoom 7、6 個 Region pill 全在地圖內（未把縣視野套進 Forecast mode）。 | 無回歸 |
| `restoreNowView` 延後（`:484-491`） | DV-20 往返在 1280／375 視野完全相等（§3）；BASE／subject 往返讀數相同。 | 無回歸 |
| `applyObservation` 的選取保留規則（`:796-803`） | 未選縣分支與 BASE 逐字相同（`else if`）；Reviewer 探測：全臺選一個代表站 → newer Refresh → 仍選取、視野不變、無 County 脈絡。選縣分支：該站在新資料仍為本縣有效站 → 保留；自製樣本讓臺中站變無效 → 選縣保留、選測站清除、脈絡＝新 `/api/`。 | 成立 |
| `renderObsState` 加 County 狀態行（`:879-886`）；`wireStationMarker` 加焦點提升／`keepInClearArea` 平移；`renderStations` 依選縣重建 | #37 檢查重跑 **97/97**；#36 檢查重跑 **37/37**；V1 `check_series_error_visible.py` PASS；#38 檢查重跑 **58/58**（全部輸出導向 scratchpad）。 | 無回歸 |

## 7. Executor concerns 的獨立判斷

1. **臺北市在全臺縮放層級無法以指標點選**——事實成立且範圍更大：Reviewer 以 3 px 格點＋自寫幾何量測初始全臺視野中「多邊形內且最上層為縣路徑」的像素：1280（z7）有 5 縣為 0（基隆市、臺北市、新竹市、嘉義市、金門縣）；375（z6）有 **19／22** 縣為 0（多數被代表標記覆蓋）。放大後皆可 hover＋點選（z9／z10 實測澎湖縣、金門縣、臺北市、連江縣），且 R-V2-DD-9(a) 選單對 22 縣皆可用。判斷：R-V2-DD-4 未綁定縮放層級；R-V2-RSP-7（owner #39）明定密度管理不得使地圖不可選、375 全臺視野不要求顯示 22 個代表標記且選縣仍有 DD-9(a) 路徑——契約充分，**不需 Design Authority**。記為 F-2（Low，交接 #39 與 Spec Integration Audit）。
2. **大縣 County view 標記重疊**（花蓮縣 61 站 ≈ z8）——R-V2-DD-5(d)「全部有效測站可到達（地圖上或清單）」由清單滿足；密度屬 R-V2-RSP-7（#39）。交接，非本票缺陷。
3. **縣界互動圖層與 backdrop 共用幾何（以位置 join 名稱）**——Reviewer 以自寫點在多邊形內判定：22 個多邊形各自內含的有效測站多數縣＝`counties.js` 對該索引的名稱（**22／22 一致**；849 有效站中 5 站落在鄰縣簡化多邊形內、4 站不在任何多邊形內——湖西、東沙島、西濱N000K、東引——皆為簡化海岸線／圍欄外，不影響 join）。`basemap.js` 逐位元組未變；backdrop 的 `L.geoJSON(basemap.taiwan, {interactive:false, …})` 兩段程式未變（diff 核對）且在 overlay pane 仍為非互動 path；互動圖層是**另一個** `L.geoJSON`，帶縣名屬性、只作互動幾何、不以資料著色、只在 Now mode。判斷：DR-20 P-2(c) 約束的是 backdrop 圖層（`interactive: false`、不承載縣市層級資料語義、README 不得稱其為資料圖層）——皆仍成立；Δ-12／R-V2-DD-4「另加帶名稱屬性的縣界互動圖層」已由獨立圖層滿足；SPEC-V2 §5.2 明列「帶屬性縣界圖層的建置方式與資料大小預算（SHOULD 保持精簡）」為 HOW，重用幾何正符合精簡。沒有第二種合理解讀需要裁決——**不是 Design Authority 事項**。join 對底圖重產的脆弱性由 `test_each_polygon_is_the_county_it_is_named` 守住。
4. **修改已稽核的 #36 程式**——見 §6，無回歸。
5. **375 px 選縣後 County 脈絡在地圖上方**——R-V2-RSP-5（375 資訊面，#39）。Reviewer 另觀察：375 以地圖點選縣後脈絡在頁面上方、需捲動才見。交接 #39，非本票缺陷。

## 8. Findings

### F-1 — 22 個縣多邊形成為看不見、也不能操作的鍵盤焦點停駐點；選縣後多數停駐點的焦點完全不可見（Medium，**blocking**）

- **證據**：
  - BASE 與 subject 對照（1280，同一 Rig）：焦點在 `#map` 後按 Tab——BASE 依序到代表標記 `SPAN.spill`；subject 依序到 `path.leaflet-interactive` **22 次**，之後才到標記（BASE overlay pane 互動 path 0 條，subject 22 條）。
  - 被聚焦的 path：computed `outline-style: none`（`static/styles.css:929` `.leaflet-overlay-pane path.leaflet-interactive:focus { outline: none; }`，#38 新增）、`stroke-opacity 0`、`fill-opacity 0`；唯一的指示是 Leaflet 在焦點時打開、定位於多邊形中心的縣名 tooltip。對聚焦的 path 按 Enter、Space → County 選單值不變（不選取）。
  - 焦點**完全不可見**的停駐點數（1280×900，樣本 h0；判準：該停駐點唯一的指示 tooltip 整個落在地圖容器裁切區外，或整個落在浮動 Now 面板內）：全臺視野 0／22；**選縣後**：臺中市視野 12／22、臺南市 17／22、嘉義縣 18／22、雲林縣 18／22、花蓮縣 15／22（其中**雲林縣、嘉義縣兩個停駐點的指示整個位在浮動 Now 面板之下**）、澎湖縣 21／22。375 選臺中市後，金門縣、澎湖縣兩個停駐點的指示在視窗外。
  - 機制（觀察所得，非設計依據）：`buildCountyLayer` 對每個多邊形 `layer.bindTooltip(...)`（`app.js:1303`），vendored Leaflet 1.9.4 的 `_addFocusListenersOnLayer` 因此在每條 path 綁定 focus／blur；Chromium 讓帶焦點監聽的 SVG 元素進入循序焦點（path 無 `tabindex` 屬性仍可被 Tab 到）。Worklog 決定 2 只把它視為「滑鼠點擊取得焦點的外框」而以 CSS 取消外框；Executor 的焦點走查（`Back to Taiwan` → 清單、代表標記）未經過這 22 個停駐點。
- **契約依據**：R-V2-DD-9(e)「鍵盤焦點 MUST NOT 被任何面板或 overlay 完全遮蔽」與 R-V2-RSP-6「鍵盤焦點永不被完全遮蔽」（本票分配：DD-4～DD-9、RSP-6 部分）；OC S-10「鍵盤焦點永不被完全遮蔽」；AC-V2-12 的鍵盤走查。R-V2-DD-9(d)「縣多邊形不必各自可聚焦」允許多邊形不進焦點序，不豁免 (e)。此缺陷由本 subject 引入（BASE 不存在）。
- **為何 blocking**：違反本票分配範圍內明文的 MUST，可重現、可觀察；鍵盤使用者在 Now mode 每次經過地圖都會遇到 22 個無作用的停駐點，選縣後其中多數焦點完全消失（含被面板完全遮蔽的情形）。這是契約違反主張，依治理 §4.5 不能以 deferral 處置；#39 的 AC-V2-14 焦點走查亦會在此失敗，屬本票應在引入時修正的缺陷。
- **Closure 要求（R2 將核對）**：在 Now mode（全臺視野與至少兩個縣視野；1280 與 375）從地圖起 Tab 走查，沒有任何焦點停駐點完全不可見、且沒有看起來可操作卻無作用的停駐點；hover 突顯＋縣名、點選選取、DD-9(a) 選單、代表標記與清單的鍵盤路徑、DV-20／DV-21 行為不回歸；附自動化或可重現的瀏覽器證據。修法屬 HOW（例如讓多邊形退出循序焦點，或給予可見焦點並提供一致的鍵盤行為）——Reviewer 不指定。

### F-2 — 初始全臺視野下多數縣多邊形無法以指標命中（Low，non-blocking；交接）

- **證據**：§7 第 1 點的量測（1280 z7：5 縣為 0 可命中像素；375 z6：19／22 縣為 0）。放大後可 hover／點選；DD-9(a) 選單對 22 縣可用。
- **判定**：不違反 R-V2-DD-4（未綁定縮放層級）；屬 R-V2-RSP-7 密度管理（owner #39）。
- **Disposition**：交接 **#39**（R-V2-RSP-7；特別是 375 全臺視野），並請 Spec Integration Audit 在 #39 之後以同一量測重核 R-V2-DD-4 的指標可達性。不延長本 cycle。

### F-3 — 選縣後浮動面板自動捲動，使 Stale／Unavailable 的 chip 與類別原因離開可視區；worklog 對此的「可見」主張過度（Low，non-blocking）

- **證據**：`selectCounty` 於 ≥ 1180 px 執行 `els.county.scrollIntoView({block:"nearest"})`（`app.js:1144-1145`）。Reviewer 量測（考慮祖先 overflow 裁切的可視比例）：1280×900 與 1280×800，Unavailable＋選縣後 `#obs-state-chip`、`#obs-state`、`#obs-state-reason` 可視 **0%**（面板 `scrollTop` 347），Stale＋選縣後同為 0%（`scrollTop` 305）；同時 County 狀態行、`Refresh`、地圖內告示可視 100%。已提交的 `desktop-unavailable-county.png`、`desktop-stale-county.png` 也顯示 chip 與原因不在面板可視區內；worklog V-5 對兩張截圖寫「`STALE` chip、County 狀態行、原因…皆可見」「`UNAVAILABLE` chip、類別原因…」——實為 DOM 存在，不是可視。
- **判定**：DV-21 §4.1 (1)(2) 與 §4.2(5) 的核心——選縣不得使 Stale／Unavailable **標示**消失——由 County 狀態行、地圖內告示與狀態訊息滿足；類別原因仍在同一面板、捲動即見，位置屬 HOW（§4.2(6)；R-V2-RSP-6「可見可達」）。判 PASS。
- **Disposition**：記錄證據措辭的落差；**#39**（資訊面／面板版面與 AC-V2-14 的 Stale／Unavailable 截圖）宜考慮讓原因與 County 狀態行同處可見。不延長本 cycle。

### F-4 — 「瀏覽器不為它發出請求」的敘述不精確（Low，non-blocking）

- **證據**：`static/data/counties.js` 檔頭「the browser makes NO request for it」、README「load no data from anywhere」；實際上瀏覽器以同源請求載入 `/static/data/counties.js`（Reviewer network log）。意圖是「無外部請求、不另取資料」。
- **依據**：R-V2-DOC-6（程式說明正確）。**Disposition**：下一次編輯該檔或 #41 的 README 彙整時改為「只有同源請求、無外部請求」。不延長本 cycle。

### 其他交接（非 finding）

- County view 標記的 pill 為 44×**24** px（`styles.css` `.station-icon--county .spill { height: 24px }`）——R-V2-RSP-3 的 44×44 量測屬 **#39**（AC-V2-14），請 #39 納入。
- 大縣 County view 標記重疊（§7 第 2 點）、375 County 脈絡位置（§7 第 5 點）→ **#39**。
- Reviewer 自寫檢查 `rv38.py` 首輪的三個 FAIL 中，兩個是檢查本身的假陽性並已另行排除：「澎湖縣在初始視野以地圖點選」（5 px 格點未命中；3 px 格點可命中、z9 實測可選——併入 F-2）與「金門縣選取多邊形身分」（縣視野中多邊形幾乎被標記覆蓋；改以選取 path 的 bbox 對照自算投影確認為金門縣）。第三個即 F-1。

## 9. Routing

- **Design Authority**：無。Executor concerns (1)(3) 經判斷契約充分、無需裁決（§7）。
- **Acceptor（reserved）**：無。縣界資料未涉及帳號或付費（重用 #28 已 vendored 的內政部開放資料），RB-3／RB-4 未觸發；無單元目錄外變更（RB-5）。

## 10. Evidence 索引（Reviewer 自產，皆在 Reviewer scratchpad，未提交）

- `join_check.py`（縣名 join 的點在多邊形內判定）；`rv38.py`（主檢查：67 PASS／3 FAIL（見 §8 說明）／9 NOTE）、`rv38_out/results.json`、`rv38_out/network.json` 與截圖；`rv38_probe.py`、`rv38_focus.py`、`rv38_focus2.py`、`rv38_under.py`、`rv38_tabbase.py`（F-1）；`rv38_reach.py`（F-2）；`rv38_vis.py`（F-3）；`rv38_views.py`（BASE／subject 視野對照）；`rv38_m12.py`（375 清單／詳情／圍欄外）。
- 重跑 Executor 檢查：`check_modes_browser.py` 37/37、`check_refresh_browser.py` 97/97、`check_county_browser.py` 58/58、`check_series_error_visible.py` PASS（輸出在 scratchpad `rerun36／37／38`）。
- `pytest -q` 493 passed；BASE 475 個 test id 全在；CI `36207033490`、`36207254045` success；`tools.credential_scan` passed。

VERDICT: BLOCKING (F-1)
