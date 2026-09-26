# Worklog — Issue #39 地圖圍欄與響應式可用性：pan／zoom 圍欄、初始視野、375 px 底部資訊面、44×44、768 px 破版檢查

- **Work item**：GitHub Issue #39（Formal lane，V2 Core；Blocked by #38——已 CLOSED）
- **Executing role**：`executor`，以 `gov-executor` definition 派工（Bindings §3.1 mapping：`claude-opus-5-5`，effort `high`）。本 session 自述的模型為 Opus 5.5；**這不是 binding 證據**。Binding verification 依 Bindings §3.4 由派工者（Orchestrator）從 harness 紀錄核對並記入 run record 或 audit record；本 worklog 不複製 harness 日誌。
- **Branch**：`home_work_01-v2-implementation`；**BASE ＝ `4651d33`**（#38 結案 commit）
- **Subject**：cycle 1 初始 code anchor ＝ `ae0b9dc`（R1 受審）；**cycle 1 targeted correction（F-1、DV-22）後的 code anchor ＝ `f3bf245`**（BASE `4651d33`..`f3bf245` 為本票全部產物變更，含 evidence；`ae0b9dc`..`f3bf245` 為 correction delta，見下方「Cycle 1 targeted correction」）；其後只改 `doc/governance/**` 的 commit（本 worklog）為 record-only（Bindings §7 P7）。
- **開始／本次更新**：2026-09-26

## Contract reference

- **Outcome Contract**：`home_work_01/doc/governance/outcome-contract-v2.md`（ACCEPTED 2026-09-25；normative candidate `69c5a04`）——S-8、S-9、S-10、AB-V2-7、AB-V2-8。A-3（金鑰）本票**未使用**；A-4 未使用。
- **Spec**：`home_work_01/doc/spec/SPEC-V2.md` **v2.2**——§2.6 R-V2-MAP-1～5、R-V2-RSP-1～8；§5.3 驗證儀器；§6.2 截圖集合；§6.3 AC-19 列；R-V2-DD-9(e)；R-V2-DOC-1(8)；INV-V2-8、INV-V2-9；V1 R-EN-1、V1 INV-4、V1 DR-20 P-12。
- **Derivation record**：`derivation-SPEC-V2.md` DV-11（圍欄三項的產品語義與儀器）、B-4、B-20（附錄 A 為 advisory，未轉為需求）；§15（本票分配：AC-V2-13、14、15（完整）、20（範圍）；§6.3 AC-19；H-2）。
- **交接項（#36／#37／#38 audit records 指給 #39 者）**：#36 R1 §8 (a)(b)(c)(d)；#37 R1 (b)；#38 R1 F-2、F-3（面板版面）、County view 標記 44×24、大縣標記重疊、375 County 脈絡位置。處理方式見「Decisions」10。
- **High-risk**：`decision-20260923-high-risk-categories.md` A-1（本票觸及 **H-2**）；核對材料見下方專節。
- **契約變更**：無。未修改任何 requirement、AC、invariant、gate、oracle。§5.3 儀器值全部沿用建議值（見 Decisions 1）。伺服器端（`observation.py`、`server.py`、`representative.py`、`api/**`）未修改；`representative.MAP_RANGE` 未變。

## Decisions and assumptions（HOW；Spec §5.2 委派）

1. **§5.3 儀器值（全部沿用建議值，未替換）**：圍欄範圍 **E ＝ lon 117.6–122.9、lat 21.2–26.7**（＝既有 `representative.MAP_RANGE`／`app.js MAP_RANGE`，故 #38 的上圖／未上圖計數與代表測站皆不變）；Leaflet **`maxBounds` ＝ E、`maxBoundsViscosity` ＝ 1.0**（硬邊界）；**`minZoom` 6、`maxZoom` 12**；初始 `fitBounds` ＝ **lon 119.25–122.05、lat 21.85–25.35**（本島＋澎湖，#36 既有常數）加 24 px padding（手機資訊面開啟時另加其覆蓋高度）；中等縮放儀器 **zoom 8**；資訊面 peek **≥ 50 % 地圖高度未遮蔽**（實作：peek `max-height` 172 px／地圖 360 px、212 px／440 px）；**44×44 CSS px**。實測讀數見 Verification V-5（`instruments`）。圍欄與縮放範圍作用於單一地圖實例，因此 Forecast mode 同樣受限（V1 未定任何縮放／邊界值，六標記與 AC-17 的初始視野仍在 E 內；#36 回歸見 V-6）。
2. **桌機（≥ 1024 px）Now 面板改為地圖旁的欄位，不再浮在地圖上**。理由（計算於實作前、瀏覽器驗證後確認）：原浮動面板覆蓋地圖左側約 330 px；加上 `maxBounds` ＝ E 後，z8 時視窗左緣最遠只能到 117.6E，金門（118.3E）落在 x ≈ 127 px、完全在面板下（z9 同樣），且鍵盤焦點落到被面板覆蓋、又因圍欄無法平移出來的標記——會違反 R-V2-MAP-1（金門須可到達並可選取測站）與 R-V2-DD-9(e)／RSP-6。改為 CSS grid 兩欄（面板 312 px＋地圖）後，地圖視窗整個可用，金門／連江在任何縮放都可到達（V-5 實測 z8 與 z12 皆 PASS）。Forecast mode 的版面維持 V1（≥ 1180 px 浮動、以下堆疊），模式切換時地圖尺寸改變由既有的模式切換路徑（`invalidateSize()` 先於任何視野變更）處理。面板高度上限＝地圖高度，面板內捲動；選取測站時面板捲到詳情。
3. **< 1024 px：地圖上方精簡狀態列＋地圖底部資訊面（R-V2-RSP-5）**。狀態列：標題與 chip、Stale／Unavailable 區塊、Observation Time／Fetched Time／Valid stations（標籤與值同列）、`Refresh`、`County` 選單、`Back to Taiwan`、`Details`。來源說明與標記說明兩句移到地圖下方（`.now-notes`，文字不變）使 375 px 地圖上移（map top 由 782 px 降到約 554 px）。資訊面（`#info-sheet`：County 脈絡、測站詳情、測站清單）在 < 1024 px 以 `position:absolute` 疊在地圖下緣：**peek**（≤ 地圖高度一半）、**expanded**（顯示測站清單，上緣停在縮放鈕之下 104 px）、**closed**。`Close` 為有可見文字的按鈕，Esc 亦可關閉；未實作滑動（MAY）。關閉**保留選取**，焦點移到 `Details`，`Details` 重開並把焦點放到 `Close`。開啟中選另一站／縣即更新內容。`Back to Taiwan` 從 County 脈絡移到 `County` 選單下方（兩種版面皆同），使資訊面關閉時仍可用（R-V2-DD-8、RSP-5(g)）。版面判斷由 JS 讀資訊面的 computed `position`，不另寫一份斷點。資訊面是 now-panel 的子元素；now-panel 在 flex 版面下 `z-index:auto`，避免其形成低於 Leaflet 標記層的 stacking context（實作中以截圖發現並修正）。
4. **資訊面開啟時的選取可見（R-V2-RSP-6）**：新 `reveal(latlng)`：若標記不在「地圖減去 padding、資訊面覆蓋、地圖告示」的淨空區內，先在目前縮放平移；若圍欄擋住（例如屏東縣最南測站在 peek 下），逐級放大直到可見；每個候選視野先以 Leaflet `_limitCenter` 限制在 E 內，所以不會再被圍欄彈回。用於選站、資訊面開合、resize 後，以及**鍵盤**焦點進入標記時（取代 #38 的 `panInside`）。
5. **標記密度與鍵盤可達（R-V2-RSP-3、RSP-7、DD-9(e)）**：`updateMarkerAccess()` 依排名逐一放置標記，觸控區（pill 擴大到至少 44×44，顯示名稱時含名稱）與已放置者相距不足 2 px 即隱藏（`is-culled`：`visibility:hidden`，不可點、不是 Tab 停駐點，DOM 與位置保留，放大即出現）。排名：選取的測站、焦點所在的測站，其後 Taiwan-wide 依 `DENSITY_PRIORITY`（22 縣的固定順序，先分散全島：臺北市、高雄市、臺中市、花蓮縣、臺東縣、澎湖縣、金門縣、連江縣……，README 列出），County view 依該縣最高、最低、代表測站、其餘（StationId）。另外，被資訊面或地圖告示覆蓋的 Taiwan-wide 標記暫時 `tabindex=-1`，因此鍵盤焦點永遠不會落在被覆蓋的標記上。每個縣仍在 `County` 選單、每個測站仍在測站清單（DD-5(d)、DD-9(a)(b)）。
6. **程式化 fit 不再動畫並立即落在圍欄內**：`fitToMarkers` 的 `fitBounds` 加 `animate:false`，其後 `panInsideBounds(maxBounds, {animate:false})`。否則 Leaflet 會在 `moveend` 以動畫把視野彈回圍欄，使之後的 reveal／密度計算量到舊視野。`fitBounds(` 仍只有一個呼叫點、`invalidateSize()` 仍在其前（V1 守衛未動）。#38 的「zoom 動畫期間延後套用」機制保留（使用者觸發的縮放動畫仍可能進行中）。
7. **滑鼠點擊標記不移動地圖**（self-verification 中發現並修正）：pill 被滑鼠按下時也會取得焦點；原本 focus handler 會平移地圖，使 mouseup 落在別處而遺失 click（臺北市上限檢查中 5–18 次點擊選錯站）。改為只有 `:focus-visible`（鍵盤）焦點才 reveal。
8. **Tooltip 不被裁切**：安裝一次性包裝 `L.Tooltip.prototype._setPosition`（vendored、pinned Leaflet 1.9.4 的內部方法），在 Leaflet 定位後把 tooltip 夾進地圖容器（4 px 邊距）；V1 的 top／bottom 方向規則不變，只修正會溢出者。
9. **County 脈絡狀態行加上原因**（#38 R1 F-3 建議「原因與 County 狀態行同處可見」）：`Stale — … Reason: <類別文字> — <代碼>.`；**不含 HTTP 狀態碼數字**，以維持 DV-21 §4.2「Unavailable 時 County 脈絡無任何數字」（`failureText(failure, true)`）。
10. **交接項處理**：#36 (a) 375 首屏地圖只露 92 px → 版面 3（地圖上移，且資訊面不再把脈絡推到地圖上方）；(b) 北部標記重疊 → 5；(c) 寬度改變時重設 Now 視野 → **保留** #28 F-1 的規則（寬度改變可能切換版面，須重新 fit），resize 改經尺寸守衛，選取測站於 fit 後以 reveal 保持可見；(d) E 未改，`MAP_RANGE` 不需同步。#37 (b) 面板捲動 → 2、9。#38 F-2（初始縮放多數縣多邊形被標記蓋住）→ 5 使初始視野的標記數大幅減少（1280：9 個、375：5 個），多邊形可點面積增加；SIA 以 #38 的量測方法重核 DD-4（未由本票宣稱結論）。County view 標記 44×24 → pill 可見高度仍 24 px，但觸控區為 44×44（`::before`），V-5 以 `elementFromPoint` 網格實測每個顯示中標記的 44×44 全部命中該標記。大縣標記重疊 → 5。375 County 脈絡位置 → 3。
11. **瀏覽器檢查工具**：新增 `tests/check_fence_browser.py`（`check_*`，pytest 不收集），重用 #37 `Rig` 與 #38 `S`／`add_variants`。地圖視野由 Leaflet 的 `.leaflet-proxy` 元素讀取（`translate3d`＝中心的世界像素、`scale`＝2^(zoom−1)），以 Web Mercator 公式換算中心與四邊——不讀 app 內部狀態。拖曳以 DevTools 滑鼠事件模擬；上限的四向拖曳到底：先在 z8 拖到該邊、以滾輪在該邊附近放大到 z12、再拖到底。
12. **修改了 #38 的瀏覽器檢查 `tests/check_county_browser.py`（4 處，未弱化）**：(a) 「浮動面板下的標記取得焦點後被帶出」→ 本票移除了浮動 Now 面板，改為「面板與地圖不重疊，且放大後在畫面外的標記取得焦點時被完整帶入視野」（仍驗 DD-9(e)）；(b) Tab walk 的「22 個標記停駐點」→「停駐點數＝頁面提供為停駐點的標記數（顯示中且未被覆蓋，至少 1）；隱藏的標記不可見」——22 的前提因密度規則（RSP-7 明文允許）不再成立；(c)(d) 375 從 `Back to Taiwan` Tab 進清單：先經過資訊面自己的 `Expand`、`Close`（只允許這兩個、且焦點皆可見），再到第一個清單項——比原檢查多驗中間停駐點。
13. **其他**：`.leaflet-control-zoom a` 改為 44×44；Stale 時 on-map 告示位置不再為浮動面板預留 344 px。

## Artifacts（code anchor `ae0b9dc`；BASE `4651d33`）

| 檔案 | 動作 |
| --- | --- |
| `home_work_01/static/app.js` | 修改：圍欄與縮放範圍（`MIN_ZOOM`、`MAX_ZOOM`、`maxBounds`）、`DENSITY_PRIORITY`／`TOUCH`、`updateMarkerAccess`／`densityRank`／`markerBox`／`overlaps`／`coveringRects`、`reveal`／`clearBox`／`revealSelection`、資訊面（`sheetLayout`、`sheetShown`、`sheetCover`、`renderSheet`、`closeSheet`、`reopenSheet`、`toggleSheetExpanded`、`afterSheetChange`）、`resizeMap`（經 `ensureMapSized`）、`fitToMarkers`（不動畫＋`panInsideBounds`）、`fitPadding`（Now 不再預留浮動面板）、`keepTooltipsInsideMap`、`selectStation`／`selectCounty`／`backToTaiwan`／`renderCountySelection`／`renderObsState`／`failureText`、鍵盤焦點才移動地圖 |
| `home_work_01/static/index.html` | 修改：`map-shell` id／class、Now 面板結構（`county-actions`：`Back to Taiwan`、`Details`；`#info-sheet` 含標頭 `Expand`／`Close` 與原 County 脈絡、詳情、清單）、`.now-notes` 移到地圖下方 |
| `home_work_01/static/styles.css` | 修改：≥ 1024 px Now 面板在地圖旁、< 1024 px 狀態列與資訊面、44×44 縮放鈕、`is-culled`、`county-actions`、`.now-notes`；移除 Now 面板浮動時的捲動與告示位移規則 |
| `home_work_01/tests/test_fence_frontend.py` | 新增：16 個靜態守衛 |
| `home_work_01/tests/check_fence_browser.py` | 新增：可重現的瀏覽器檢查 |
| `home_work_01/tests/check_county_browser.py` | 修改：Decisions 12 的 4 處 |
| `home_work_01/tests/test_secrets.py` | 修改：3 個檔案加入憑證掃描清單（只加） |
| `home_work_01/README.md` | 修改：新增「Now mode — map range, zoom range and layout」（R-V2-DOC-1(8)）；`Back to Taiwan` 位置；測試段 |
| `home_work_01/doc/acceptance/screenshots/v2/issue-39/*` | 新增：60 張截圖（1280／375／768）、`browser-check-results.json`（每項觀察值＋`instruments`＋`fenceSweeps`）、`network-log.json`、`regression-check-issue-{36,37,38}-results.json`／`…-network-log.json` |

未修改：`app.py`、`weather_query.py`、`ingestion/**`、`data.db`、`smoke.py`、`vercel.json`、`requirements.txt`、`server.py`、`api/**`、`observation.py`、`representative.py`、`CONTEXT.md`、`static/data/**`、`static/vendor/**`、`.github/workflows/**`、`doc/requirement/**`；單元目錄外無變更（RB-5）。

## Verification

環境：Windows 11，`home_work_01/.venv` Python 3.12；Chrome headless（DevTools protocol，`websocket-client`）；`node --check static/app.js`。以下皆指 subject `ae0b9dc` 的工作樹（瀏覽器檢查執行前後以 sha256 確認 `app.js`／`styles.css`／`index.html` 與 commit 內容相同）。

- **V-1 全套**：`python -m pytest -q` → **513 passed**（BASE 494 ＋ `test_fence_frontend.py` 16 ＋ `test_secrets.py` 參數化 3）。全離線、無金鑰。
- **V-2 quality floor**：以 `git archive 4651d33` 匯出 BASE 收集 test id：BASE 的 494 個 id 在 subject **全部存在**（差集為空）。`test_secrets.py` 無刪除行；V1 `test_map_frontend.py` 初始化守衛未修改且通過（`fitBounds(` 全檔仍 1 處、`invalidateSize()` 在前）。`check_county_browser.py` 的修改見 Decisions 12（未弱化）。無 skip、無門檻降低。
- **V-3 CI**：push `ae0b9dc` 後 workflow「home_work_01 CI」run **`36216924939`** **success**：`513 passed`；`credential scan passed: 719 tracked files …`。Workflow 未修改（A-4 未使用）。
- **V-4 憑證**：`python -m tools.credential_scan` passed；以腳本讀 `.env`（不印出）比對 `git diff --cached` 全文（380,019 bytes）→ 真金鑰字面 **False**；evidence 目錄 grep 哨兵金鑰、上游標記、`opendata.cwa.gov.tw`、`Authorization` → 無命中；`git ls-files` 無 `.env`。
- **V-5 瀏覽器檢查 `python tests/check_fence_browser.py` → 74/74 PASS**（約 12 分鐘），evidence `home_work_01/doc/acceptance/screenshots/v2/issue-39/`：
  - **AC-V2-13(a)／MAP-4**：初始視野（1280：z7、375：z6）含本島（120.03–122.01E、21.90–25.30N）與澎湖本島（119.52–119.70E、23.52–23.66N）；`Back to Taiwan` 後同樣成立（兩視野）。
  - **AC-V2-13(b)／MAP-1**：z8 與 z12 各向 W／E／N／S 拖曳到底（z12：先在 z8 拖到該邊、滾輪在該邊放大到 z12、再拖到底；到邊距離 ≤ 0.00023°），另 z6 四向與鍵盤方向鍵平移——每個讀到的視野：中心在 E 內，每一軸「地圖 ⊆ E」或「E ⊆ 地圖」（逐次讀數在 `fenceSweeps`）。**金門、連江**：z8 以拖曳到達（陸地框在視窗內）、點擊其代表標記選取測站（`467110`／`467990`），並在 z12 再到達、點擊選取（兩視野；截圖 `*-reach-kinmen-*`、`*-reach-lienchiang-*`）。
  - **AC-V2-13(c)／MAP-2**：下限 z6——本島南北 168.9 px：1280 地圖 560 px 高 **30.2 %**、375 地圖 360 px 高 **46.9 %**；`−` 停用，`-` 鍵與滾輪不再縮小；下限時四向拖曳圍欄仍成立。PASS 條件**不**含「E 全部在視窗內」。
  - **AC-V2-13(d)／MAP-3**：上限 z12——1280：**28.95 px/km**、375 px ≈ **12.96 km**；375：29.06 px/km、12.9 km；`+` 停用，`=` 鍵不再放大。**臺北市（19 個上圖測站）在 z12**：1280 有 16 站以點擊其標記選取、其餘在清單選取後於地圖上顯示並標示；375 為 11／10（部分站兩者皆驗）；零問題。
  - **AC-V2-14 375 資訊面**：選縣 → peek，地圖**未遮蔽 52.5 %**（188/360 px）；`Close` 可見且未被覆蓋；縮放鈕、模式切換、`Refresh`、`Back to Taiwan` 以 `elementFromPoint` 命中；`Expand`（Enter）→ 清單在面板內可見、縮放鈕仍未被覆蓋；開啟中選清單另一站、選另一縣、點地圖上另一標記 → 面板標題與詳情皆更新（＝`/api/`）；peek 時選取的標記在面板上方可見；**屏東縣最南測站（墾雷，21.90N）**自清單選取 → 仍在面板上方可見（圍欄擋住平移時放大）且圍欄成立；`Close`（Enter）→ 關閉、焦點到 `Details`、選取保留；`Details`（Enter）→ 重開、焦點到 `Close`；Esc 關閉；`Back to Taiwan` → 清除並關閉。
  - **RSP-3 44×44**：兩視野與 County＋測站狀態下，模式切換、Refresh、County、Back to Taiwan、Expand、Close、Details（可見時）、縮放鈕、清單項目 `getBoundingClientRect` 全部 ≥ 44×44。**標記**：Taiwan-wide 初始、放大兩級、臺中市 County view——每個顯示中且完整在地圖內的標記，其 44×44 方格 25 點 `elementFromPoint` 全部命中該標記；顯示中的標記觸控區兩兩不重疊；隱藏標記皆不可見；放大後顯示數增加。
  - **RSP-6 桌機**：Now 面板與地圖不重疊；選取測站標記與縮放鈕命中；面板把詳情捲入可視區。距地圖西／北／東／南緣約 36 px 的標記 hover → tooltip 完全在地圖內。
  - **RSP-1 768 px**：Now 預設、選縣 peek、expanded、Forecast mode——控制兩兩無重疊、`scrollWidth` ＝ 768；地圖可縮放、可拖曳；peek 未遮蔽 ≥ 50 %；關鍵控制未被覆蓋。
  - **R-V2-RSP-2／§6.3 AC-19**：375 的 11 個狀態（預設、county peek、expanded、station、closed、loading、Stale、Stale＋縣、Unavailable、Unavailable＋縣、Forecast）`scrollWidth` ≤ 375。
  - **AC-V2-15／MAP-5**：375 起：選縣（peek）、expand、選站、close、reopen、→Forecast、→Now，再 resize 768×1024、1280×900、1024×768、375×812、375×640（只改高），以及**地圖容器隱藏時 resize＋開合資訊面後再顯示**、回 375——每步無 NaN／0×0 標記、有標記、視野在圍欄內（15 步）。
  - **R-EN-1 六項（V2 介面）**：(1) 標題逐字、Taiwan Map 卡在預報區之上、Now 面板有標題、模式切換在首屏；(2) 由上述兩視野全部操作證明；(3) Valid stations 數與 Weekly summary 顯示；(4) 圖表 legend、軸標籤、hover tooltip（V1 圖表不變）；(5) loading、Stale、Unavailable 各一張（1280：`desktop-states-state-*.png`；375：`375-state-*.png`）；(6) 見上。
  - **AC-V2-16／INV-V2-3**：224 個瀏覽器請求，**外部 0**；請求 URL 無金鑰或上游標記；console 無 JS 例外、無 NaN／Invalid LatLng。
- **V-6 回歸**：`check_modes_browser.py`（#36）**37/37**；`check_refresh_browser.py`（#37）**97/97**；`check_county_browser.py`（#38）**72/72**；V1 `check_series_error_visible.py` PASS。結果複製為 `regression-check-issue-{36,37,38}-*.json`。（開發中途一次 #36 為 36/37，失敗項為 #38 R2 記錄的已知 N-1 flake，最終執行通過。）
- **V-7 自我驗證：mutation checks**（scratchpad `mut39.py`：暫時修改後跑靜態守衛與相關瀏覽器情境，sha256 確認還原；**非正式 audit**）：M1 移除 `maxBoundsViscosity` → 靜態 1＋瀏覽器 2；M1b 移除 `maxBounds` → 靜態 1＋頁面錯誤（檢查中斷）；M2 `minZoom` 5 → 靜態 1＋瀏覽器 2；M3 `maxZoom` 14 → 靜態 1＋瀏覽器中斷；**M4 resize 不經守衛 → 靜態 1，瀏覽器 0**（見限制 (a)）；M5 取消隱藏 → 瀏覽器 6；M6 peek 240 px → 靜態 1＋瀏覽器 3；M7 移除 tooltip 夾限 → 靜態 1＋瀏覽器 1；M8 選站不 reveal → 瀏覽器 1；M9 被覆蓋標記仍為 Tab 停駐點 → 靜態 1；M10 資訊面路徑移除尺寸守衛 → 靜態 1。每個 mutation 至少被一層抓到。
- **V-8 H-2／不變產物**：`git diff --stat 4651d33` 對 `app.py`、`weather_query.py`、`ingestion/`、`data.db`、`smoke.py`、`vercel.json`、`requirements.txt`、`server.py`、`api/`、`observation.py`、`representative.py`、`.github/`、`doc/requirement/`、`static/data/`、`static/vendor/`、`CONTEXT.md` → 空。
- **未執行／限制**：(a) resize 路徑的尺寸守衛只有**靜態**守衛能區分（M4）：在 vendored Leaflet 1.9.4 上，對隱藏容器直接 fit 未在瀏覽器中產生 NaN，所以瀏覽器情境證明「守衛存在時沒有 NaN」，不證明「沒有守衛就會有 NaN」；AC-V2-15 允許靜態守衛。(b) 拖曳、滾輪、點擊為 DevTools 合成的滑鼠事件；無實體觸控、無 pinch 測試；滑動關閉未實作（MAY）。(c) 只測 Chromium headless；未做螢幕閱讀器測試。(d) preview／Vercel 部署上的行為屬 #41。(e) 瀏覽器檢查不在 CI（需 Chrome），由 Reviewer 本機重現。

## Cycle 1 targeted correction（R1 F-1 ＋ decision DV-22；2026-09-26）

- **依據**：R1 audit record `home_work_01/doc/governance/audit/issue-39-c1-r1.md`（VERDICT: BLOCKING (F-1)；其餘分配項 PASS）；DA decision **DV-22** `home_work_01/doc/governance/decisions/decision-20260926-desktop-representative-marker-density.md` §4.1／§4.2（解決 R1 routing signal R-1，即本 worklog 原 concern 的 9／22）；Orchestrator 的 targeted correction 派工（同 branch、同 worklog identity、不結案、之後 R2）。另依派工允許順修 F-2；F-3、O-2 未處理（見下）。
- **F-1 修正（HOW）**：原因是 ≥ 1024 px Now 面板整體 `overflow-y:auto`，選縣／選站時程式 `scrollIntoView` 把面板捲動，使狀態區離開可視區。修正：(1) ≥ 1024 px Now 面板改為**不捲動**（`overflow:hidden`、`height:562px`），以明確列的 CSS grid 排列——第 1 列標題、第 2 列 Stale／Unavailable 區塊、第 3 列三個時間、第 4 列 `Refresh`、第 5 列 `County` 選單與 `Back to Taiwan` 並排、第 6 列（`minmax(0,1fr)`）資訊部分；只有資訊部分 `#sheet-body`（County 脈絡、詳情、清單）捲動；欄寬 312 → **360 px**，使 Stale 狀態下狀態區仍精簡（1024 px 實測：狀態區約 330 px，資訊部分 ≥ 178 px）。(2) 選取程式不再呼叫任何 `scrollIntoView`，改為 `scrollInPanel(el, toTop)`：只調整 `#sheet-body.scrollTop`，並以該捲動區在視窗內的部分為準（短視窗時不讓項目落在視窗外）。選站時先把詳情捲到資訊部分頂端；清單項目若有**鍵盤**焦點（`:focus-visible`）再保持其可見（R-V2-DD-9(e)）。(3) County 狀態行已含原因（Decisions 9），狀態區又固定可見，Stale chip 與原因在所有選取狀態下都在畫面上。
- **DV-22 §4.1（HOW）**：`markerBox` 改為只算**必要可點區**（氣溫 pill 擴大到 ≥ 44×44），不再含名稱標籤；碰撞仍為「相距不足 2 px」。名稱標籤（zoom ≥ 8 才顯示）改為讓位：與任何顯示中標記的必要可點區或較早顯示的標籤重疊時，標籤以 `label-off`（`visibility:hidden`）隱藏，標記不隱藏。圖層成員仍只來自 `/api/` 的 `representativeStationIds`。另把 Leaflet 縮放鈕列為「覆蓋物」：被縮放鈕蓋住的顯示中標記**不隱藏**，但暫時不是 Tab 停駐點（R1 O-4；DD-9(e)）。README「Marker density」段改寫為此規則（2 px、必要可點區、標籤讓位、排名、1280 顯示 9／22 與 375 顯示 5／22 為樣本資料下的結果）。
- **F-2（順修）**：`ensureMapSized` 在等待尺寸時改為把每個延後步驟排入 `pendingSized`，尺寸到位後依序全部執行，不再丟棄（模式切換、resize、資訊面開合的延後步驟不會互相覆蓋）。
- **未處理（non-blocking，依派工 MAY）**：F-3（< 1024 px expanded 狀態自清單選站後標記在資訊面下）——未改；R1 判定不是契約違反，交 SIA 觀察。O-2（下限時拖曳中暫態）——Leaflet 行為，R1 判定在 HOW 內，不處置。
- **Artifacts（correction delta `ae0b9dc`..`f3bf245`）**：`static/app.js`（`updateMarkerAccess`、`markerBox`、`coveringRects`、`scrollInPanel`、`selectStation`、`selectCounty`、`toggleSheetExpanded`、`ensureMapSized`）、`static/styles.css`（≥ 1024 px 面板 grid、`label-off`）、`README.md`（Marker density、Layout）、`tests/test_fence_frontend.py`（＋3 守衛、2 處字串更新：欄寬 360 px、`it.hidden`）、`tests/check_fence_browser.py`（F-1 與 DV-22 情境；density 檢查只在資訊面真的疊在地圖上時才排除其下方的標記——原檢查在桌機誤把地圖下半排除，改正後量測範圍變大、未弱化）、`doc/acceptance/screenshots/v2/issue-39/*`（全部重產）。`index.html` 未改。`check_county_browser.py` 本次未改。
- **Correction verification**（subject `f3bf245`；瀏覽器執行前後以 sha256 確認三個前端檔與 commit 相同）：
  - **C-1 F-1 守衛（新瀏覽器情境，1024×768、1100×900、1280×900）**：success、Stale、Unavailable 各自：全臺、全臺＋點地圖代表標記選站、選縣、選縣＋**清單點選**選站、選縣＋**點地圖標記**選站——`#obs-time`、`#obs-fetched`、`#refresh-button`、`#mode-now`、`#mode-forecast`、`#county-select`、`#back-to-taiwan`（選縣時）、`#obs-state-chip`（Stale／Unavailable 時）的可見比例（計入所有 overflow 祖先與視窗）**全部 1.0** 且中心 `elementFromPoint` 命中；面板 `scrollTop` 恆為 0；選站後 `#obs-sel-name` 可見比例 1.0。鍵盤路徑（清單第 21 項 Enter）：焦點可見、面板未捲動、狀態元素未被面板裁切；1100／1280 視窗容得下地圖卡時狀態元素亦全部在視窗內；1024×768 視窗容不下地圖卡，瀏覽器自身的焦點捲動會把**頁面**捲下（不是面板遮蔽），此時只要求前兩項。9 個情境截圖 `f1-{1024,1100,1280}-*.png`。
  - **C-2 DV-22 §4.1（新瀏覽器情境，1280 與 375；初始、重新載入、zoom 8、`Back to Taiwan` 後）**：(1) 全臺圖層＝`/api/` 代表集合 22／22，隱藏者 `visibility:hidden`、`tabindex=-1`、中心不可點；(2) 每個被隱藏者的必要可點區與至少一個**顯示中**代表的必要可點區相距 < 2 px（每一對的 `getBoundingClientRect` 讀數在 `browser-check-results.json` 的 `dv22`）；zoom 8 名稱標籤顯示時同樣成立、且至少一個標籤顯示；(3) 顯示者兩兩不重疊、≥ 44×44、地圖內者中心命中（375 zoom 8 有一個標記在縮放鈕下：保留顯示、非 Tab 停駐點，記於 `shownUnderZoomButtons`）；(4) 重新載入顯示集合相同；(5) 被隱藏縣抽驗 4 縣（基隆市、新北市、桃園市、新竹縣——含北部）：hover 顯示縣名並點選選縣（375 的基隆市、新北市在 zoom 10 才可指到多邊形，DD-4 不限縮放）、`County` 選單可選、滾輪放大到其代表標記出現並點選選取該站。顯示數：1280 初始 **9／22**（zoom 8：14）、375 初始 **5／22**。
  - **C-3 全部 #39 瀏覽器檢查 `python tests/check_fence_browser.py` → 113/113 PASS**（原 74 項＋F-1 9 項＋DV-22 30 項；AC-V2-13／14／15、§6.3 AC-19、圍欄、44×44、768 全部仍 PASS）；**505** 個瀏覽器請求，外部 **0**。
  - **C-4 回歸**：#36 `check_modes_browser.py` **37/37**；#37 `check_refresh_browser.py` **97/97**；#38 `check_county_browser.py` **72/72**；V1 `check_series_error_visible.py` PASS。結果複製為 `regression-check-issue-{36,37,38}-*.json`。
  - **C-5 全套與 CI**：`pytest` **516 passed**（＋3 守衛）；BASE 494 id 仍全在；CI run **`36223369715`**（head `f3bf245`）**success**：`516 passed`、`credential scan passed: 733 tracked files`。
  - **C-6 mutation（self-verification）**：M11「面板恢復整體捲動」→ 靜態 1＋瀏覽器 F-1 情境 2 項 FAIL；M12「必要可點區含名稱標籤」→ 靜態 1＋瀏覽器 DV-22 zoom 8 情境 4 項 FAIL；檔案以 sha256 確認還原。
  - **C-7 憑證／不變產物**：`tools.credential_scan` passed；staged diff 450,872 bytes 以 `.env` 比對真金鑰字面 False；evidence 無哨兵金鑰／上游標記／`opendata.cwa.gov.tw`／`Authorization`；`git diff --stat 4651d33 f3bf245` 對 V-8 清單（含 `app.py`、`data.db`、`weather_query.py`、伺服器檔、`static/data`、`static/vendor`、workflows、`test_map_frontend.py`）為空。
  - **限制**：同 V 節（合成滑鼠事件、只測 Chromium headless、無螢幕閱讀器）；1920 px 未另測（DV-22 為參考值）。

## High-risk 核對材料（decision A-1；供 R1 明記 H-2 核對段）

- **H-2（老師概念詞、下方 dashboard、Grading App、標題）**：V-8 空 diff（`app.py`、`data.db`、`weather_query.py` 等）；`Taiwan Weather Forecast`、`Select Region`、`Select Date`、`Date`、`MinT`、`MaxT` 未改（`test_verbatim_labels` 等 #36 守衛通過；R-EN-1(1) 瀏覽器檢查讀 h1 逐字）；Forecast section 的 HTML 未動（`index.html` diff 只在 Taiwan Map 卡內）；#36 回歸 37/37（含下方 dashboard 兩模式相同、`Select Region` 六名與七列表、預報 503 時 section 層級 error）；768／375 Forecast mode 截圖。masthead 導言文字未改（只在 ≤ 640 px 縮小字級）。
- **H-3（附帶）**：密度規則只隱藏／顯示標記，不計算任何值；County 脈絡計算未改（`test_county_context_computes_no_aggregate` 通過）；狀態行加的原因是固定類別文字、無數字（DV-21 §4.2；Unavailable＋縣無數字由 V-5 驗證）。
- **H-1（附帶）**：伺服器與金鑰路徑未改；V-4。
- **Diversity**：Executor 與 Primary Reviewer 同為 `claude-opus-5-5` 時，audit record 記 `diversity_lost`（Bindings §5）。
- **Cycle 1 correction 對 H-2 的影響**：`ae0b9dc`..`f3bf245` 只改 `static/app.js`（Now 面板捲動與標記密度）、`static/styles.css`（≥ 1024 px Now 面板版面、`label-off`）、README、測試與 evidence；`index.html`、masthead、Forecast section、`app.py`、`data.db`、`weather_query.py` 皆未改（C-7 空 diff）；#36 回歸 37/37（下方 dashboard、`Select Region`、概念詞）；R-EN-1(1) 標題逐字檢查仍 PASS（C-3）。

## Audit status

- **Required**：Formal mandatory independent audit（治理 §4.1；Bindings §5）。本 worklog 的瀏覽器檢查與 mutation checks 皆為 Executor self-verification，**不是**正式 audit。
- **Records**：cycle 1 R1 `home_work_01/doc/governance/audit/issue-39-c1-r1.md`——**VERDICT: BLOCKING (F-1)**（Medium）；F-2（Low，本次順修）、F-3（Low，未改）；routing signal R-1 由 DA decision DV-22 解決（§4.1 由 R2 核對）；O-1～O-4 為 observations。F-1 與 DV-22 §4.1 的 targeted correction 已完成（subject `f3bf245`），**待 R2 scoped closure review**（Orchestrator 派工）。Executor 的「已修正」不是 closure。

## Remaining work

1. **正式 audit**：R2 closure review of F-1 ＋ DV-22 §4.1 (1)～(5)（含修正造成的回歸），Orchestrator 派工。結案條件依治理 §3.8。
2. **Concerns（交有權角色判斷；Executor 未自行裁決）**——R1 已處置：(a) → O-1；(b) → R1 判定不衝突、不需 DA；(c) → 位置屬 HOW，捲動缺陷即 F-1（已修）；(d) → R1 §6 判定未弱化；(e) → SIA；(f) → R1 判定不是缺陷。本次 correction 新增的待 R2 核對點：
   - (g) **1024×768 的鍵盤路徑**：視窗容不下地圖卡時，鍵盤焦點移到清單下方項目會由瀏覽器捲動**頁面**（不是面板），模式切換可能暫時在視窗上方之外；面板本身不捲動、狀態元素未被裁切或遮蔽。若 R2 認為此情形仍屬 F-1 範圍，authority：Primary Reviewer（依 §4.3 爭議流程）。
   - (h) **縮放鈕下的標記**（R1 O-4）：保留顯示（DV-22 不允許因非碰撞理由隱藏）、被蓋住時非 Tab 停駐點；指標需平移後才能點選。
   - (i) 桌機 Now 欄寬 312 → 360 px（地圖在 1280 由 692 → 約 644 px 寬）；AC-V2-13 全部重跑 PASS。
   原 concerns 全文：
   - (a) **使用 vendored Leaflet 1.9.4 的內部 API**：`map._limitCenter`（reveal 的圍欄限制）與包裝 `L.Tooltip.prototype._setPosition`（tooltip 夾限）。版本已 pin，有靜態與瀏覽器檢查；更換 Leaflet 版本時須重驗。屬 HOW，提請 R1 判斷。
   - (b) **圍欄與縮放範圍同樣作用於 Forecast mode**（單一地圖）。V1 未規定任何縮放／邊界值；六標記與 AC-17／AC-18 在 #36 回歸中 PASS。若 Reviewer 認為與 R-V2-MODE-3「Forecast mode ＝ V1 地圖、語義不變」有張力，authority：Design Authority。
   - (c) **桌機 Now 面板改為地圖旁欄位**（Decisions 2）：Forecast mode 仍為 V1 浮動版面，兩模式在 ≥ 1180 px 的地圖寬度不同（模式切換路徑已處理尺寸）。附錄 A 的「沿用 V1 左上浮動面板」是 advisory（B-20）；提請 R1 核對。
   - (d) **修改了 #38 已稽核的檢查與程式**：`check_county_browser.py` 4 處（Decisions 12）；`keepInClearArea` 改走 `reveal`（只在鍵盤焦點時）；`Back to Taiwan` 移出 County 脈絡；County 狀態行加原因。#38 回歸 72/72。提請 R1 依治理 §4.4 核對未弱化。
   - (e) **#38 F-2（DD-4 指標可達）**：密度規則使初始視野的多邊形可點面積增加，但本票未以 #38 的格點量測重做；#38 R1 F-2 disposition 指定 SIA 重核。
   - (f) **375 County view 在 peek 下縮放較低**：縣被 fit 進 peek 上方的淨空區，大縣（例如臺中市 60 站）在該縮放只顯示少數標記（其餘隱藏、放大即現、清單可達）。符合 RSP-7；提請 R1 判斷可用性。
3. **後續票**：#40（Radar；只在改變 CRS 時重驗 AC-V2-13／15）、#41（preview 驗證、README 其餘項目、V2 驗收文件；AC-V2-13／14／15 的證據引用本票）。
