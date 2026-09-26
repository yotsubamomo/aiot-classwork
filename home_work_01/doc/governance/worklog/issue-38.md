# Worklog — Issue #38 Taiwan → County → Station 下鑽：縣界互動圖層、County 脈絡、測站清單與詳情、Back to Taiwan、鍵盤路徑

- **Work item**：GitHub Issue #38（Formal lane，V2 Core；Blocked by #36——已 CLOSED）
- **Executing role**：`executor`，以 `gov-executor` definition 派工（Bindings §3.1 mapping：`claude-opus-5-5`，effort `high`）。本 session 自述的模型為 Opus 5.5；**這不是 binding 證據**。Binding verification 依 Bindings §3.4 由派工者（Orchestrator）從 harness 紀錄核對並記入 run record 或 audit record；本 worklog 不複製 harness 日誌。
- **Branch**：`home_work_01-v2-implementation`；**BASE ＝ `de004f4`**（DV-21 tracker actions 的 commit）
- **Subject**：**code anchor ＝ `2f34843`**（BASE `de004f4`..`2f34843` 為本票全部產物變更）；本 worklog 為其後的 record-only commit（`doc/governance/**`，Bindings §7 P7）
- **開始／本次更新**：2026-09-26

## Contract reference

- **Outcome Contract**：`home_work_01/doc/governance/outcome-contract-v2.md`（ACCEPTED 2026-09-25；normative candidate `69c5a04`）。A-3（金鑰）本票**未使用**；A-4 未使用。
- **Spec**：`home_work_01/doc/spec/SPEC-V2.md` **v2.2**——§1.2 Δ-11、Δ-12；§2.3 R-V2-DD-1、DD-4～DD-9、DD-11；R-V2-MODE-4、R-V2-MODE-5(a)（選縣部分）；R-V2-DEG-2（縣界互動與脈絡部分）；R-V2-OBS-6（County 脈絡欄位）、R-V2-OBS-10(a)（縣界可見，互動圖層部分）；§2.6 R-V2-RSP-6（部分）；§2.8 R-V2-DOC-1(3)；INV-V2-3、INV-V2-5、INV-V2-7（觀測失敗面：縣界互動與脈絡）。
- **Derivation record**：`home_work_01/doc/governance/decisions/derivation-SPEC-V2.md` DV-3（有效測站）、DV-9、DV-10（圍欄外測站）；V1 DR-20 P-2(c)（底圖 backdrop 不變）；§15（本票分配）。
- **Decisions（本票契約的一部分）**：
  - **DV-20** `decision-20260926-ac-v2-01-county-round-trip-allocation.md` §4.1——AC-V2-01 選縣往返（i）（ii）（iii）；R-V2-MODE-5(a) 選縣部分的實作責任。
  - **DV-21** `decision-20260926-county-layer-under-stale-unavailable-allocation.md` §4.1 (1)(2)(3) 與 §4.2——縣界互動圖層與 County 脈絡在 Stale／Unavailable 下；Unavailable 下缺值「—」、不得顯示 0。
- **High-risk decision**：`decision-20260923-high-risk-categories.md`（A-1：R1 record 須明記 H-2／H-3 核對段；下方「High-risk 核對材料」提供入口）；derivation §6（H-3 對 V2 的適用）。
- **Ticket 分配（#38）**：AC-V2-01（選縣往返部分，DV-20）、AC-V2-08(a)(b)（縣界互動與脈絡部分，DV-21）、AC-V2-10、AC-V2-12、AC-V2-23（`Back to Taiwan`）、AC-V2-16（本票範圍：縣界圖層無 CWA 字串／金鑰／絕對 URL；執行期零外部請求）、V1 AC-19 的 375 px 無不必要橫向捲動（選縣／選測站狀態）、AC-V2-20（本票範圍：CI 全綠）、README R-V2-DOC-1(3)。§6.3 定向 V1 重驗：無。
- **Out of scope（未做）**：圍欄與縮放儀器（`maxBounds`／`minZoom`／`maxZoom`，#39）；375 px 底部資訊面（#39）；R-V2-RSP-7 標記密度管理（#39）；Radar（#40）；縣市篩選與測站搜尋、URL deep-linking（Later）。
- **契約變更**：無。未修改任何 requirement、AC、invariant、gate、oracle。伺服器端（`observation.py`、`server.py`、`representative.py`、`api/**`）未修改。

## Decisions and assumptions（HOW；Spec §5.2 委派）

1. **縣界資料來源（RB-3／RB-4 未觸發）**：互動圖層的幾何**重用** #28 已 vendored 的 `static/data/basemap.js` 的 `taiwan` 22 個縣市多邊形（內政部『直轄市、縣市界線』open data，政府資料開放授權條款；#28 取得時即為免費、免帳號、免付費）。縣名以新增的**專案自撰**資料 `static/data/counties.js`（`window.TAIWAN_COUNTY_NAMES`，22 個 CWA `CountyName` 逐字，依 basemap 多邊形順序）附加；app 在執行期把兩者 join 成帶 `countyName` 屬性的 22 個 GeoJSON Feature。沒有任何新下載、帳號或付費；零外部請求；新增檔案 1.3 KB。`basemap.js` 與其非互動 backdrop 圖層**逐位元組未變**（DR-20 P-2(c) 不變）。Join 的正確性以離線測試對消毒樣本核對（每個多邊形內有效測站的多數縣＝其名稱；98% 以上上圖測站落在自己縣的多邊形內——簡化海岸線使 8 個沿岸／小島測站落在多邊形外，例如東引）。「帶屬性縣界圖層的建置方式與資料大小預算」依 Spec §5.2 屬 HOW。
2. **縣界互動圖層（R-V2-DD-4）**：`L.geoJSON`，畫在 backdrop 之上、標記之下；平時透明（fill-opacity 0、stroke-opacity 0）；hover 為固定色外框 `#9ed0ff`＋淡填色（0.14）並以 sticky tooltip 顯示縣名；選取縣為固定色外框 `#fbbf24`；**顏色與任何資料無關**。只在 Now mode 在地圖上（`syncMap` 於 Forecast mode 移除、回 Now 再加入；`initMap` 只在 Now mode 加入）。SVG path 被滑鼠點擊時取得焦點會畫出瀏覽器外框（包住整個縣的 bounding box），以 CSS 對 `path.leaflet-interactive:focus` 取消——多邊形不是鍵盤路徑（DD-9(d)），鍵盤路徑是 County 選單。
3. **不經地圖的鍵盤選縣路徑（R-V2-DD-9(a)）**：Now 面板的原生 `<select>`「County」，第一項「All of Taiwan」（選它＝Back to Taiwan 的行為），其後 22 縣依 `representative.COUNTY_ORDER`。方向鍵每次變更即選縣。
4. **County view 的標記**：選縣後，標記改為該縣位於圍欄範圍 E 內的全部有效測站（DD-5(a)「該縣在地圖上的有效測站」）；Taiwan-wide 的代表測站標記暫時移除；Back to Taiwan 還原。County view 標記精簡（名稱標籤只在選取者顯示；hover tooltip 顯示名稱），且 `tabindex="-1"`（不是 Tab stop；鍵盤路徑是測站清單，DD-9(b)(d)）。Taiwan-wide 代表標記維持 #36 的可聚焦行為。
5. **選縣視野（R-V2-DD-5(a)）**：`fitCounty` ＝ 該縣上圖有效測站的 bounds ∪ 該縣多邊形 bounds，`maxZoom` 11，padding 沿用 `fitPadding(mode)`（≥ 1180 px 時避開浮動面板）。沒有可放入的測站（零有效或 Unavailable）時以多邊形為視野。`fitBounds` 仍只有一個呼叫點：`fitToMarkers(bounds, maxZoom)` 加一個可選參數（預設 8，原呼叫不變）。寬度改變的 resize 在選縣時改為重新套用縣視野。
6. **極值與清單順序（平手規則，README 記載）**：清單依氣溫由高到低；同溫以較小 `stationId`（字元碼順序，同代表測站規則）在前；最高／最低測站各自在同溫時取較小 `stationId`。
7. **County 脈絡內容**：縣名；`Valid stations`＝該縣有效測站數；`On the map`＝上圖數（有未上圖者顯示「57 (1 not on the map)」形式）；`Highest air temperature`／`Lowest air temperature`＝「值 °C · 測站名」；註記「Station values as published, per station; no county-level value is computed.」；清單標題 `Stations (n)`。**不計算任何聚合值**（無平均、無加總）；頁面文字不出現 average／mean／平均。
8. **Unavailable／Stale（DV-21 §4.2）**：`renderCountyContext` 在 `obs` 為 `null` 時四個值一律 `MISSING`（「—」）、不列清單、顯示「No stations to list: the Latest Observation is unavailable.」、清單標題不帶數字；縣名照常。Stale 時 `obs` 保留（#37 的 `applyObservationFailure` 不清除），脈絡即上一次成功資料。狀態在 County 脈絡內**另以一行重述**（`#county-state`：「Stale — the last successful Latest Observation (the last Refresh failed).」／「Latest Observation unavailable — no station data to show.」），由 `renderObsState` 與既有 chip、說明區塊、地圖內告示同步——選縣不會讓 Stale 標示消失。成功回應下零有效測站的縣：`0`、`0`、「—」、「—」、「No valid station in 連江縣 in this Latest Observation.」，無狀態標示（R-V2-DD-5 末句）。
9. **Refresh 與選取**：newer 回應套用時保留選縣（HOW）；若選縣，選取的測站只在新資料中仍為該縣有效測站時保留；未選縣時沿用 #36 規則（仍為代表測站才保留）。Unavailable→成功時保留選縣、不重新 fit（DV-21 §4.1(1) 允許）。
10. **選縣往返（R-V2-MODE-5(a)、DV-20）**：`selectedCounty` 為模組層級狀態，只由 `selectCounty` 與 `backToTaiwan` 寫入；`setMode`／`syncMap`／`restoreNowView` 不清除它或 `selectedStationId`。視野沿用 #36 的 `nowView`（離開 Now 時保存 center／zoom，回來 `setView`）——回來時**不**重新套用縣視野。縣界圖層回到地圖時重新套用樣式並把選取縣外框提到最上層。
11. **鍵盤焦點永不被完全遮蔽（R-V2-DD-9(e)、R-V2-RSP-6 部分）**：(a) 代表標記取得焦點時提高 z-index（北部密集處不被鄰近標記蓋住），並以 `map.panInside` 平移使其落在浮動面板與（Stale／Unavailable 時）地圖底部告示之外的淨空區；(b) 清單項目選取後其上方打開的詳情可能把焦點項目推出面板可視區，選取後以 `scrollIntoView({block: "nearest"})` 拉回；(c) 選縣時（≥ 1180 px 浮動面板）把 County 脈絡捲入面板可視區。
12. **Leaflet zoom 動畫期間的視野要求（self-verification 中發現並修正）**：Leaflet 在 zoom 動畫進行中會**靜默丟棄**新的 zoom 要求；以方向鍵快速切換縣時，最後一個縣的 fit 被丟棄，地圖停在錯誤視野（首輪截圖 `desktop-stale-county.png` 顯示花蓮縣脈絡卻是北部視野）。修正：追蹤 `zoomanim`／`zoomend`，動畫期間的 `fitToMarkers`／`restoreNowView` 要求只保留最後一個，於 `zoomend` 套用。瀏覽器檢查加入「以鍵盤選的每一縣其多邊形在地圖內且避開面板」與各鍵盤選縣後的視野核對（見 V-7 M8）。
13. **測站詳情（R-V2-DD-7）**：沿用 #36 的 `#obs-selected` 區塊並擴充：名稱＋`StationId`、`縣 · 鄉鎮`（無鄉鎮為「—」）、未上圖註記、氣溫、相對濕度、風速、風向（度）、氣壓（hPa）、雨量（`Precipitation (today)`，資料集 `Now.Precipitation`：當日累積降水 mm；README 既有說明）、天氣、該站 Observation Time；無效值「—」。區塊位置在 County 脈絡與測站清單之間。
14. **其他**：地圖 caption 在選縣時為「Latest Observation · the stations of <縣>」；標記說明文字隨 view 切換。
15. **瀏覽器檢查工具**：新增 `tests/check_county_browser.py`（`check_*` 命名不被 pytest 收集）；重用 `check_modes_browser.py` 的 DevTools driver 與 `check_refresh_browser.py` 的 `Rig`（未修改的 `create_app`、真的 `LatestObservationService`、可控時鐘、樣本衍生的模擬上游與四類失敗、哨兵金鑰），另加兩個樣本衍生變體：`c0`（臺北站 RH／氣壓／天氣設為哨兵）與 `zero`（連江縣全部測站氣溫設為 `-99`→成功回應中連江縣零有效測站）。所有期望值由頁面實際收到的 `/api/` body 以 `representative.in_map_range` 與 README 平手規則計算。無金鑰、無網路。

## Artifacts（code anchor `2f34843`；BASE `de004f4`）

| 檔案 | 動作 |
| --- | --- |
| `home_work_01/static/data/counties.js` | 新增：22 縣名（basemap 多邊形順序），同源 script global |
| `home_work_01/static/app.js` | 修改：縣界互動圖層（`buildCountyLayer`、`countyStyle`、`styleCounties`、`raiseSelectedCounty`）、`selectCounty`、`backToTaiwan`、`fitCounty`、`renderCountySelection`、`renderCountyContext`、`renderCountyList`、`markListSelection`、`countyStations`、`onMap`、極值與排序、`selectStation`、`keepInClearArea`、County view 標記、擴充的 `renderSelectedStation`、`applyObservation` 的選取保留、`renderObsState` 的 County 狀態行、`fitToMarkers(bounds, maxZoom)`、zoom 動畫期間的視野要求延後套用、caption；檔頭說明 |
| `home_work_01/static/index.html` | 修改：`counties.js` script、County 選單、County 脈絡（含 `Back to Taiwan`）、測站清單區塊、擴充的測站詳情 |
| `home_work_01/static/styles.css` | 修改：County 選單、County 脈絡、狀態行、清單、未上圖標示、county tooltip、County view 標記、SVG path 焦點外框 |
| `home_work_01/tests/test_county_frontend.py` | 新增：15 個靜態守衛 |
| `home_work_01/tests/check_county_browser.py` | 新增：可重現的瀏覽器檢查（58 項） |
| `home_work_01/tests/test_static_checks.py` | 修改：`_FIRST_PARTY_FRONTEND` 加入 `data/counties.js`（只加） |
| `home_work_01/tests/test_secrets.py` | 修改：三個新檔加入憑證掃描清單（只加） |
| `home_work_01/README.md` | 修改：模式表兩列；「Switching keeps your place」含選縣；新增「Now mode — Taiwan → County → Station」（選縣、County view、County 脈絡與平手規則、清單與詳情欄位、`Back to Taiwan`、Stale／Unavailable、**圍欄外測站規則**（R-V2-DOC-1(3)）、縣界圖層來源）；測試段 |
| `home_work_01/doc/acceptance/screenshots/v2/issue-38/*` | 新增：16 張截圖、`browser-check-results.json`、`network-log.json`、#36／#37 回歸檢查結果與 network log |

未修改：`app.py`、`weather_query.py`、`ingestion/**`、`data.db`、`smoke.py`、`vercel.json`、`requirements.txt`、`server.py`、`api/**`、`observation.py`、`representative.py`、`static/data/basemap.js`、`static/vendor/**`、`.github/workflows/**`、`doc/requirement/**`；單元目錄外無變更（RB-5）。

## Verification

環境：Windows 11，`home_work_01/.venv` Python 3.12；Chrome headless（DevTools protocol，`websocket-client`）；`node --check static/app.js`。以下 subject 皆指 `2f34843` 的工作樹。

- **V-1 全套**：`python -m pytest -q` → **493 passed**（BASE 475 ＋ 18：`test_county_frontend.py` 15、`test_secrets.py` 參數化 ＋3）。全離線。
- **V-2 V1／既有測試保留（quality floor）**：BASE `tests/` 的 240 個 `test_*` 函式在 subject 全部存在（missing: []），新增 15。`git diff --cached -- home_work_01/tests/` 對既有檔案的刪除行只有一行：`_FIRST_PARTY_FRONTEND` tuple 被**擴充**為含 `data/counties.js` 的 tuple。無 skip、無門檻降低、無斷言移除。#36／#37 的測試與檢查工具未修改。
- **V-3 CI**：push `2f34843` 後 workflow「home_work_01 CI」run **`36207033490`** **success**：`493 passed in 10.96s`；`credential scan passed: 644 tracked files …`。Workflow 未修改（A-4 未使用）。
- **V-4 憑證**：`python -m tools.credential_scan`（staged 後）passed；以腳本讀 `.env`（不印出）比對 `git diff --cached` 全文（233,966 bytes）→ 真金鑰字面 **False**；evidence 目錄全文 grep 哨兵金鑰、上游／平台標記、`opendata.cwa.gov.tw`、`Authorization` → 無命中。
- **V-5 瀏覽器檢查 `python tests/check_county_browser.py` → 58/58 PASS**（約 2 分鐘），證據 `home_work_01/doc/acceptance/screenshots/v2/issue-38/`（`browser-check-results.json` 記每項觀察值與期望值）。桌機 1280×900 與 375×812（mobile emulation）：
  - **DD-4／DD-1**：Now mode 有 22 個互動縣路徑；平時全部同一透明樣式（非資料著色）；以 County 選單依序選 22 縣，每次恰一個多邊形為選取樣式、hover 該多邊形顯示的縣名＝所選縣（22 個不同名稱→22 個不同多邊形），且每一縣的多邊形都在地圖內、避開浮動面板。
  - **AC-V2-10 hover**：hover 臺中市 → 外框 opacity 1、fill-opacity 0.14、tooltip「臺中市」（`desktop-county-hover.png`）。
  - **AC-V2-10 點選**（期望值由 `/api/` 手算）：臺中市（地圖點選）60／60、最高 28.8 °C · 潭子、最低 4.3 °C · 雪山圈谷；**臺北市**（先點新北市，再在其視野中點臺北市）19／19、28.4 °C · 石牌、19.4 °C · 鞍部（`desktop-county-taipei.png`）；**金門縣**（鍵盤選單）6／6、26.0 °C · 金寧、23.3 °C · 金門(東)（`desktop-county-kinmen.png`）；**連江縣**（最少測站）4／4、25.3 °C · 東引、23.3 °C · 東莒。每次標記數＝該縣上圖測站數、全部在地圖內且避開面板，縣多邊形亦在視野內。清單完整、依氣溫由高到低、每項氣溫＝`/api/`。Now mode 頁面全文無 average／mean／平均、無 real-time／live。
  - **AC-V2-12 清單鍵盤**：自 `Back to Taiwan` 按 Tab 依序到清單第 1、2 項（焦點在其中心可被命中、未被遮蔽）；Enter 選臺北站 → 詳情＝`/api/`（名稱、`466920`、`臺北市 · 中正區`、Observation Time、氣溫；哨兵的 RH／氣壓／天氣為「—」），標記與清單項標示選取，焦點留在該項且可見；Space 選另一項 → 詳情＝`/api/`；County view 標記點擊亦選取（`desktop-station-detail.png`）。
  - **AC-V2-12／DD-11 圍欄外測站**：高雄市 58 個有效測站、`On the map` 顯示「57 (1 not on the map)」；清單中東沙島 `468100` 標示「not on the map」；無其標記（57 個標記）；Enter 開啟其詳情，含「Not on the map — outside the map range」（`desktop-county-kaohsiung-offmap.png`）。
  - **DD-5 零有效測站的縣（衍生樣本 `zero`）**：成功回應（845 有效站、21 個代表標記）下選連江縣 → `0`、`0`、「—」、「—」、「No valid station in 連江縣 …」，狀態仍 success、無 Stale／Unavailable 標示（`desktop-county-zero-valid.png`）。
  - **AC-V2-12／DD-8／AC-V2-23 `Back to Taiwan`**：逐字可見，Enter 啟動 → 選縣與選測站清除、22 個代表標記、選單回「All of Taiwan」、每個標記在地圖中的位置與頁面初始載入時相同（初始視野 R-V2-MAP-4），焦點移到 County 選單。375 同。
  - **DD-9(e)**：以鍵盤平移使「基隆」代表標記落在浮動面板下，再使其取得焦點 → 被提到最上層並平移出面板，焦點中心可被命中。
  - **DV-20 AC-V2-01 選縣往返（§4.1）**：桌機：地圖點選臺中市（縣視野 zoom 9.003、中心 24.21964, 120.5346）→ 清單選一站 → 放大一級（zoom 9.999、中心 24.21966, 120.53335）→ 鍵盤切 Forecast（六個 Region 標記、無縣界圖層、無 County 脈絡）→ 鍵盤切回 Now：(i) 臺中市仍選取（選單值、選取樣式多邊形、County 脈絡＝`/api/`）；(ii) 視野讀數 zoom 9.999、中心 24.21966, 120.53335——**等於離開時**，不等於縣視野（每個標記位置差 ≤ 0.5 px）；(iii) 選取的測站、詳情、清單項與標記選取恢復（`desktop-roundtrip-returned.png`）。375：花蓮縣（縣視野 zoom 8.001 → 放大後 9.0）同樣 (i)(ii)(iii) PASS，無橫向捲動（`375-roundtrip-returned.png`）。視野讀數由兩個已知經緯度標記的畫面位置以 Web Mercator 反算（工具 HOW）。
  - **DV-21 (1) Unavailable**（首次載入 `upstream_error` HTTP 500）：22 個縣路徑存在；hover 臺中市仍突顯並顯示縣名；地圖點選臺中市 → 縣名「臺中市」，`Valid stations`／`On the map`／最高／最低皆「—」，County 脈絡文字**無任何數字**，不列測站、顯示「No stations to list …」，County 狀態行「Latest Observation unavailable — no station data to show.」，`UNAVAILABLE` chip、類別原因「… (HTTP 500) — upstream_error.」、`Refresh` 可用、仍在 Now mode（`desktop-unavailable-county.png`）；無測站可 fit 時地圖仍可鍵盤平移；鍵盤選單選花蓮縣 → 同樣「—」且視野為其多邊形；`Back to Taiwan` 可用；之後 Refresh 成功 → 保留的縣脈絡＝新回應手算值。375（`key_not_configured`）：鍵盤選臺中市 → 只有「—」、狀態與 Refresh 可見、無橫向捲動（`375-unavailable-county.png`）。
  - **DV-21 (2) Stale**：成功後鍵盤選花蓮縣（61／61、27.0 °C · 和仁、8.7 °C · 合歡山；視野含其測站與多邊形）→ Refresh 失敗（`upstream_error` 429）→ Stale：脈絡與失敗前完全相同且＝保留的成功回應手算值；`STALE` chip、County 狀態行、原因（含 `upstream_error`）、地圖內告示皆可見（`desktop-stale-county.png`）。失敗**之後** hover＋地圖點選臺東縣 → 脈絡＝保留回應手算值、Stale 仍顯示；清單選取（詳情＝保留資料）、`Back to Taiwan` 可用；not-newer Refresh（較舊 Observation Time）→ 清除 Stale、脈絡不變；再失敗（`upstream_unreachable`）→ Stale；newer Refresh → 清除、脈絡＝新回應。375（`invalid_response`）：臺中市脈絡保留、Stale 顯示、無橫向捲動（`375-stale-county.png`）。
  - **DV-21 (3) 無資料 vs 零**：成功下零有效測站的連江縣文字含 `0` 且無狀態標示；Unavailable 下臺中市文字無任何數字且含狀態標示——兩者畫面可辨（兩段文字記於 `browser-check-results.json` 的 `evidence`）。
  - **R-V2-RSP-2（V1 AC-19 375 px 部分）**：375 選縣、選測站、往返、Stale、Unavailable 各狀態 `scrollWidth` ≤ `innerWidth`；桌機選縣＋選測站亦無橫向捲動。
  - **AC-V2-16／INV-V2-3**：7 段情境共 107 個瀏覽器請求全為 `http://127.0.0.1:<port>/…`，含 `/static/data/counties.js`；**外部請求 0**（`network-log.json`）。請求 URL 無哨兵金鑰或上游標記；console 無 JavaScript 例外、無 NaN／Invalid LatLng。
- **V-6 回歸**：`python tests/check_modes_browser.py`（#36）→ **37/37 PASS**；`python tests/check_refresh_browser.py`（#37）→ **97/97 PASS**（結果複製為 `regression-check-*-results.json`／`…-network-log.json`；#36、#37 自己的 evidence 目錄未重產）；V1 `python tests/check_series_error_visible.py` → PASS。
- **V-7 自我驗證：mutation checks**（scratchpad `mutations38.py`：暫時修改 `app.js`，跑 `test_county_frontend.py`＋`test_modes_frontend.py`＋`test_map_frontend.py`＋`test_refresh_frontend.py`＋`test_static_checks.py`，部分再跑瀏覽器檢查，最後以 sha256 確認還原；**非正式 audit**）：M1 Unavailable 縣計數顯示 `0` → 靜態 1＋瀏覽器 4；M2 縣界依資料著色 → 靜態 1；M3 切換模式清除選縣 → 靜態 1＋瀏覽器 ≥ 5（DV-20 (i)(ii)(iii) 桌機與 375）；M4 Forecast mode 仍留縣界圖層 → 靜態 1；M5 Back to Taiwan 不清選測站 → 靜態 1；M6 圍欄範圍放寬（東沙上圖）→ 靜態 1；M7 計算縣平均 → 靜態 1；M8 移除 zoom 動畫期間的延後套用 → 瀏覽器 3（靜態 0：時序行為）；M9 County 脈絡不顯示 Stale 狀態 → 靜態 1；M10 清單焦點不拉回 → 瀏覽器 1（靜態 0）。每個 mutation 至少被一層抓到。
- **V-8 H-2／不變產物**：`git diff --stat de004f4 2f34843 -- app.py weather_query.py ingestion/ data.db smoke.py vercel.json requirements.txt server.py api/ observation.py representative.py ../.github/ doc/requirement/ static/data/basemap.js static/vendor/` → 空。
- **未執行／限制**：preview／Vercel 部署上的行為屬 #41；A-3 金鑰未使用；瀏覽器檢查不在 CI（需 Chrome 與 `websocket-client`），由 Reviewer 本機重現（約 2 分鐘）；hover／點擊以 DevTools 合成的滑鼠事件驗證（無實體觸控裝置測試）；未做螢幕閱讀器測試；375 px 的完整資訊面、44×44 全面量測、768 px 破版檢查屬 #39（本票清單項目與按鈕已為 ≥ 44 px 高，未做全面量測）。

## High-risk 核對材料（decision A-1；供 R1 明記核對段）

- **H-3（無縣平均、無觀測聚合；代表測站值與縣值的標示；無資料 vs 零）**：County 脈絡只有測站數（計數，不是觀測值推導）與個別測站的發布值（最高／最低測站以「值 · 測站名」呈現），註記「per station; no county-level value is computed」；`renderCountyContext` 等函式無 `reduce`、加總、除以長度（`test_county_context_computes_no_aggregate`；M7）；頁面全文無 average／mean／平均（瀏覽器檢查；`test_no_average_wording_in_the_now_mode_texts`）。縣界圖層不以資料著色（`test_county_layer_is_interaction_geometry_never_coloured_by_data`；M2；瀏覽器樣式一致性）。代表標記與 County view 標記的 aria-label／tooltip 仍為「station value」「Station value, not a county value」。**無資料 vs 零**：Unavailable 下縣脈絡一律「—」、不顯示 0 或任何數字（`test_unavailable_county_context_is_dashes_never_zero`；M1；DV-21 (1)(3)）；成功回應下零有效測站的縣顯示 `0`、「—」且無狀態標示；Stale 下脈絡為保留資料且帶 Stale 標示（M9）。用語 Latest Observation，無 real-time／live。
- **H-2（不動下方 dashboard、`Select Region`、老師概念詞、`app.py`）**：V-8 空 diff；`test_verbatim_labels` 等 #36 守衛仍通過；#36 回歸 37/37（含下方 dashboard 兩模式相同、`Select Region` 六名與七列表）。頁面標題與 V1 概念詞未改。
- **H-1**：本票未觸及金鑰路徑（伺服器未改）；新檔無金鑰、無 URL（`test_county_names_are_a_same_origin_global_with_no_url_or_key`、憑證掃描清單延伸）；V-4。
- **Diversity**：Executor 與 Primary Reviewer 同為 `claude-opus-5-5` 時，audit record 記 `diversity_lost`（Bindings §5）。

## Audit status

- **Required**：Formal mandatory independent audit（治理 §4.1；Bindings §5）。R1 待 Orchestrator 以 fresh `gov-primary-reviewer` 派工（Bindings §3.5），並依 DV-20 §4.1、DV-21 §4.1 由 R1 Reviewer 獨立重做。本 worklog 的 mutation checks 與瀏覽器檢查皆為 Executor self-verification，**不是**正式 audit。
- **Records**：尚無。

## Remaining work

1. **正式 audit**：R1（Orchestrator 派工）。
2. **Concerns（交有權角色判斷；Executor 未自行裁決）**：
   - (a) **臺北市在 Taiwan-wide 縮放層級不可直接點選**：臺北市多邊形在初始視野很小，完全被北部密集的代表標記（臺北、新北、基隆）覆蓋，因此在該縮放層級無法以滑鼠點到；可經放大、先點新北市再點臺北市、或 County 選單到達（瀏覽器檢查以後兩者驗證）。縮放上限與標記密度管理屬 #39（R-V2-MAP-3、R-V2-RSP-7）。提請 R1 判斷是否符合 R-V2-DD-4「點選／點擊 MUST 選取該縣」；若認為需要設計決定，authority：Design Authority。
   - (b) **大縣的 County view 標記重疊**：例如花蓮縣 61 站在 zoom ≈ 8 時標記大量重疊（清單與放大仍可選取每一站）。密度管理屬 #39（R-V2-RSP-7）。
   - (c) **縣界互動圖層重用 basemap 幾何＋獨立名稱表（決定 1）**：`basemap.js` 與其 backdrop 未變，但互動圖層與 backdrop 共用同一份幾何並以索引 join。若 Reviewer 認為與 DR-20 P-2(c)／Δ-12 的「另加帶名稱屬性的縣界互動圖層」有張力，authority：Design Authority。
   - (d) **修改了 #36 已稽核的視野程式**：`fitToMarkers` 加入可選 `maxZoom` 參數與 zoom 動畫期間的延後套用，`restoreNowView` 同樣延後（決定 5、12）；`applyObservation` 的選取保留規則擴充（決定 9）。#36／#37 回歸 37/37、97/97 通過；提請 R1 依治理 §4.4 一併核對。
   - (e) **375 px**：選縣後 County 脈絡在地圖上方的堆疊面板中（沿用 #36／#37 的 < 1180 px 版面）；以地圖點選縣時需往上捲動才見脈絡。375 px 資訊面 outcome 屬 #39。
3. **後續票**：#39（圍欄與縮放儀器、375 px 底部資訊面、標記密度）、#40（Radar）、#41（preview 驗證、README 其餘項目、V2 驗收文件；AC-V2-01／AC-V2-08 的證據引用 #36／#37 與本票）。
