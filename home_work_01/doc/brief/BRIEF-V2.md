# HW01 Weather Map V2 — Brief（V1 之上的 delta 盤點）

- **單元**：`home_work_01/`（HW10 Taiwan Weather Forecast；V1 已於 2026-09-24 結案並合併 `main` = `ef15d3e`）
- **性質**：V2 是 V1 之上的 **enhancement delta**。本檔只記錄 V2 的意圖、事實、grill 裁決與未定 HOW；**不重述 V1 需求**。V1 的 Outcome Contract（ACCEPTED 2026-09-23）與 Spec v1.1（EFFECTIVE）維持 normatively 不變，作為 inherited baseline。
- **依據**：2026-09-25 V2 Grill（acceptor 裁決 D-1～D-19、接受的 defaults P-1～P-36）；治理 `docs/governance/minimal-operational-governance-v2.0.md`；Project Bindings b2 `docs/governance/project-bindings.md`；V1 [`../governance/outcome-contract.md`](../governance/outcome-contract.md)、[`../spec/SPEC.md`](../spec/SPEC.md)、`../governance/decisions/`；Portable SDD Interaction Guidance（2026-09-25，非規範）。
- **狀態**：討論輸入。契約內容見 [`../governance/outcome-contract-v2.md`](../governance/outcome-contract-v2.md)（DRAFT，待 acceptor 接受）。
- **詞彙**：V1 [`../../CONTEXT.md`](../../CONTEXT.md)；V2 新詞見第 9 節（接受後併入 `CONTEXT.md`）。

## 1. 意圖與結果

把 V1 的 Taiwan Map 從六區預報視覺化升級為 **map-first 的互動天氣介面**：

```text
Taiwan Map
├── Now mode（預設）：Latest Observation ── Taiwan → County → Station 下鑽 ── Refresh ── Radar overlay
└── Forecast mode：V1 六區七日預報地圖（語義、Select Date、導出色帶不變）
下方 Forecast dashboard：Select Region、Weekly Summary、MinT／MaxT 折線圖、Daily Forecast 表格 —— 功能不變
```

頁面刻意同時包含兩種語義：**Latest Observation（CWA 測站觀測，如發布）** 與 **七日六區預報（專案推導相容性值）**。兩者不得混淆、不共用圖例或色階。

## 2. 繼承的 V1 邊界（只列 V2 觸及的部分）

| 項目 | V1 狀態 | V2 處理 |
| --- | --- | --- |
| 兩個呈現層不呼叫 CWA、Vercel 執行期不需 secret（OC AB-5、Spec R-SHR-5／R-DS-5／R-DS-8／R-SEC-3、INV-6） | accepted | **re-scope**：預報路徑、共用預報查詢模組與 Grading App 維持不呼叫 CWA；部署的 Dashboard 新增 server-side 觀測路徑（見第 5 節）。不回溯改寫 V1 文字。 |
| 金鑰唯一位置＝未追蹤 `.env`（Bindings RB-3、Spec R-SEC-1、INV-5） | accepted | **extend**：Vercel 專案環境變數成為第二個授權位置（Bindings b3；acceptor 親自填入）。 |
| Leaflet Taiwan Map：六區 pill、Select Date、導出色帶（OC AB-14、Spec R-EN-3／R-EN-4、AC-17／AC-18；DR-20 重做） | accepted、A-4 closure | **retain as Forecast mode**：語義不變；地圖預設為 Now mode。老師 Part A 的加分地圖即 Forecast mode，README 與驗收證據必須讓它容易找到。 |
| 頁面層級錯誤對應（DR-19：預報快照失敗 → 整頁 error） | DA ruling | **delta**：三條路徑（Observation／Forecast／Radar）各自降級（第 6 節）。 |
| 瀏覽器只呼叫 `/api/`、執行期零外部請求（AC-04(b)、DR-20.4、X-1） | accepted | **reaffirm**：Radar 影像也經 `/api/` 代理；不新增外部主機例外。 |
| Spec §8「Part B 的測站觀測、圖層切換」為 REFERENCE／FUTURE；「離島三縣的任何呈現」不做 | derived | **re-scope**：測站觀測與模式／Radar 切換進入 V2；Now mode 涵蓋 22 縣市（含澎湖、金門、連江）；Forecast mode 的六區地理不變。heatmap、自動更新仍為 Later。 |
| `/api/health`＝預報快照健康（DR-7／DR-9、AC-15、AC-22） | accepted | **不變**：部署健康與 smoke 永不依賴 CWA 即時可用性；觀測／雷達狀態另行揭露。 |
| Grading App 只有 MVM、無地圖（INV-9、AC-26） | accepted | **不變**。 |
| 下方 Forecast dashboard 與 `Select Region` 行為 | accepted | **不變**；觀測值不得耦合進預報控制項。 |

## 3. 事實（2026-09-25 查證；含來源）

### 3.1 現有實作

- 地圖：`static/app.js` 以 `center` ＋ `zoom` 初始化、對六個代表點 `fitBounds`；**沒有 minZoom、maxZoom、maxBounds**，可無限縮放、可拖入空白海域。
- 底圖 `static/data/basemap.js`：純幾何（GeometryCollection），**無縣市名稱屬性**；同源 `<script>` 載入，零外部請求。內政部縣市界線裁切框 lng 118–122.5／lat 21.5–26.5 已涵蓋 22 縣市。
- 後端 `server.py`：全部資料經 `weather_query.py` 讀 `data.db`；無 HTTP client；`api/index.py` 單一 Vercel function；`vercel.json` 全路由；執行期無環境變數。
- 靜態檢查 `tests/test_static_checks.py`：AC-04(a) Python 端無 HTTP client／CWA 字串；AC-04(b) 前端無 CWA 字串、fetch 只指向 `/api/`、不得有外部絕對 URL 請求（白名單只含非請求常數）。
- CI `home_work_01-ci.yml`：`home_work_01/**` 變動即跑全部 pytest 與 credential checks；新增測試自動納入，**V2 預期不需改 workflow**。

### 3.2 CWA 資料（官方目錄與 datasetExample，未使用金鑰；副本在 session scratchpad `cwa/`）

| 資料集 | 官方名稱 | 更新 | 樣本規模 | 要點 |
| --- | --- | --- | --- | --- |
| **O-A0001-001**（V2 採用） | 氣象觀測站-全測站逐時氣象資料 | 更新頻率：每 1 時；整點逐時觀測（採政府資料開放平臺的保守官方描述） | 876 站、845 站有有效氣溫、全部有 WGS84；JSON ≈ 1.4 MB | 欄位：StationName、StationId、ObsTime、GeoInfo（Coordinates[TWD67, WGS84]、CountyName、TownName）、WeatherElement（Weather、Now.Precipitation、WindDirection、WindSpeed、AirTemperature、RelativeHumidity、AirPressure、GustInfo、DailyExtreme）。臺北市 19 站、新竹市 6、嘉義市 5、基隆市 11。 |
| O-A0003-001（Later） | 氣象觀測站-10分鐘綜觀氣象資料 | 10 分鐘 | 363 站、348 有效氣溫；氣壓只有 28 站 | 密度低、氣壓缺；作為日後 10 分鐘升級選項。 |
| O-A0002-001（Later） | 雨量觀測站-雨量資料 | 10 分鐘 | 1343 站；JSON ≈ 1.8 MB | Now／Past10Min／Past1hr／…／Past3days。 |
| **O-A0058-003**（V2 Radar） | 雷達整合回波圖-臺灣(鄰近區域)_無地形 | 10 分鐘 | PNG 3600×3600、≈ 680 KB | 範圍 lon 118.0–124.0／lat 20.5–26.5（涵蓋 22 縣市）。JSON metadata（DateTime、ProductURL）只走 fileapi、**需金鑰**；影像檔本身為公開 S3 固定檔名、每週期覆寫。-005／-006 為透明圖層變體（未取樣）。 |

- 缺值哨兵（資料標準 V1.05）：`X` 儀器故障、`-99` 缺值／異常、`T` 雨跡、`-98` 連續無降水、`990` 風向不定。數值皆為字串、一位小數。
- Datastore 參數：Authorization、limit、offset、format、StationId[]、StationName[]、WeatherElement[]、GeoInfo[]；**沒有縣市篩選參數**。
- 額度：一般會員 20,000 次／日、2 GB／日（datastore 與 fileapi 分開計）；建議同資料集重查間隔 ≥ 10 秒。授權：政府資料開放授權條款，須標示「交通部中央氣象署 [資料名稱]」。

### 3.3 9/30 疑問（已查證，非缺陷）

原始檔 `data/raw/F-D0047-091.json` 於 2026-09-24 02:24:50+08:00 取得；22 縣市皆為 15 個期間、自 09-24 00:00 至 09-30 18:00（末期間止於 10-01 06:00）。開頭 00:00–06:00 期間不在 06／18 節奏內，`derive.py` 的 `_period_key` 忽略之；視窗＝09-24～09-30，七日皆完整。9/30 六區同步偏低，與縣市原始值一致（臺北市 9/30 MaxT＝max(30, 27)＝30、MinT＝25）。**合法的第七個 Forecast Day，無需修正**。快照首日已成過去是 V1「準備好的快照」設計（Q3 A），與 V2 無關。

## 4. V2 範圍

| Class | 內容 |
| --- | --- |
| **V2 Core（ENHANCED REQUIRED）** | Now mode（預設）：Latest Observation 測站氣溫、Taiwan → County → Station 下鑽與 Back to Taiwan、測站詳情、Refresh、Observation Time／Fetched Time、stale／unavailable 狀態；Forecast mode（V1 地圖語義不變）與明顯的模式切換；地圖 pan／zoom 圍欄；桌機與 375 px 的可用性（含手機底部資訊面）。 |
| **V2 Radar（ENHANCED REQUIRED）** | 最新雷達回波 overlay：顯示／隱藏、時間戳、與底圖有意義的地理對齊、經 `/api/` 代理；狀態與觀測獨立。透明度調整只在實作代價微小時提供。 |
| **OPTIONAL／Later（不在 V2 接受範圍）** | 獨立雨量圖層；雷達動畫／歷史；heatmap；自動更新；縣市篩選與測站搜尋；URL deep-linking；10 分鐘資料集升級；Windy；22 縣市預報；歷史觀測儲存。 |

「MVM」在本專案保留給 Part A 評分基線；V2 不使用「V2 MVM」。V2 全部項目位於部署的 Dashboard（INV-9 不變）。

## 5. Latest Observation 的語義與架構（D-1、D-2、D-3、D-5）

- **保證**：latest published, bounded staleness。載入與 Refresh 顯示伺服器最近一次上游取得的最新觀測；短暫的共用重用視窗可接受；Observation Time（CWA 觀測時刻）與 Fetched Time（伺服器取得時刻）永遠可見。逐時節奏可接受，因為兩個時間都顯示。產品用語為「Latest Observation」，不用「realtime」。
- **路徑**：browser → 本應用 `/api/` → Flask／Vercel 伺服器端向 CWA 取得 → 正規化／裁剪後的回應。金鑰只在伺服器端（本機未追蹤 `.env`；部署為 acceptor 填入的 Vercel 環境變數），瀏覽器永不取得。契約不要求持久伺服器狀態；快取機制屬 HOW。
- **不回溯改寫 V1**：V1 的 CWA-free／SQLite-only 條款對預報路徑、Grading App、共用預報查詢語義與既有驗證邊界繼續有效；V2 觀測路徑是對部署 Dashboard 的明確例外／superseding delta。模組結構屬 HOW（不要求「唯一呼叫者模組」）。
- **資料規則**：無有效氣溫或無 WGS84 座標的測站不進氣溫圖層；詳情欄位缺值／哨兵顯示「—」，永不顯示為數值；成功＝回應可解析且至少一個有效測站，零有效測站＝失敗；成功的 Refresh 不得以較舊的 Observation Time 取代已顯示資料；測站數少於平常仍是成功，顯示有效測站數、不設契約門檻；StationId 為穩定識別。

## 6. 模式、下鑽、狀態、圍欄（D-6～D-15）

- **模式**：Now 預設；切換明顯且有標籤；Forecast mode 保留六區／Select Date／導出色帶語義；切換保留使用者目前的地理脈絡（除非某模式確實需要不同的有效視野）。
- **下鑽**：Taiwan → 選縣 → 縣內測站 → 測站詳情；縣脈絡＝縣名、有效／顯示測站數、最高與最低氣溫測站（名稱／值）、含氣溫的測站清單；**不計算縣平均**。Back to Taiwan 清除選縣並回到全臺視野。Taiwan-wide 視野每縣至多一個代表性有效測站（機制屬 HOW，但須確定性、只用有效現行測站、有文件、可客觀驗證；Spec 不列 22 個 StationId）。
- **測站詳情**：契約必要＝測站名稱／識別、縣、鄉鎮、Observation Time、氣溫；有效時顯示＝相對濕度、風速、風向、氣壓、今日雨量、天氣現象。單一欄位（如氣壓）不獨立成為契約關鍵。
- **狀態**：首次載入無有效資料 → 留在 Now mode、地圖與縣界可見、明確 unavailable 狀態與非機密原因、Refresh 可用、Forecast mode 可見、不自動切換、不暗示預報是觀測。Stale＝最近一次 Refresh／上游取得失敗而仍顯示上一次成功資料（純失敗基準；年齡不是契約 stale 條件）。每次 Refresh 在有界時間內到達 success／stale／unavailable（界值不在 grill 決定）。重用視窗內的 Refresh 可回同一 Fetched Time 並告知已是最新。只有手動 Refresh。
- **獨立降級**：觀測失敗只影響 Now mode；預報快照失敗依 V1 語義影響 Forecast mode 與下方 dashboard，不得停用健康的 Now mode；Radar 狀態獨立。伺服器端失敗分類（驗證用）：金鑰未設定；上游不可達／逾時；上游錯誤狀態（含 auth／quota）；無效或空的回應。使用者可見錯誤不得含金鑰、原始上游 URL、原始上游回應。
- **圍欄（outcome triad）**：pan 不得離開有用的臺灣範圍造成大片無意義空白，金門、連江仍可到達；zoom-out 不得讓臺灣小到無用或空白主導；zoom-in 支援縣／局部層級個別測站選取，不允許無意義的過度放大。minZoom／maxZoom／bounds／margin／viscosity 為 HOW／驗證參數。
- **手機（375 px）資訊面**：可關閉的底部資訊面；normal／peek 狀態下地圖可見；需要時可展開（測站清單）；一個清楚可見的關閉控制；滑動可有但不得是唯一關閉方式；面開啟時選另一測站即更新；關鍵地圖控制不被完全遮蔽。
- **其他被接受的 outcome**：可見標記在驗證視野下可讀、可選，密度管理不得讓地圖不可用，縣下鑽後該縣測站皆可到達，不要求 375 px 全臺視野同時顯示 22 個代表 pill；初始視野提供本島＋澎湖脈絡；地圖為主要內容區、模式切換不捲動即可見、頁面標題仍為 `Taiwan Weather Forecast`；overlay 不得讓地圖不可用、目前選取項與關鍵控制可見可達、鍵盤焦點永不被完全遮蔽；縣選取有非地圖的鍵盤路徑、測站詳情有測站清單的鍵盤路徑，多邊形與標記不必各自可聚焦；繼承 44×44 CSS px 目標、375 px 無不必要橫向捲動、桌機 ≥ 1024 與 375 px 為驗證案例、768 px 檢查明顯破版、tooltip／詳情不裁切、非零尺寸初始化回歸保護。瀏覽器歷史與 `prefers-reduced-motion` 屬 HOW／Later。Radar 對齊不預先接受為「已知限制」：須對齊到能提供有意義天氣脈絡，實作發現系統性偏移即 route DA。

## 7. 驗證意圖（要證明什麼；不定框架、檔名、fixture、mock、票務、順序）

1. **Latest Observation**：顯示值 → 本應用 `/api/` → 對應的上游測站紀錄可追溯；兩個時間可見；四類失敗各自產生要求的 stale／unavailable；失敗的 Refresh 保留有效資料；零有效測站＝失敗；較舊觀測時間永不取代較新。
2. **下鑽**：Taiwan → county → station → back；縣脈絡符合第 6 節；代表測站選取確定且有文件；縣下鑽可到達其有效測站。
3. **模式**：Now 預設；切換明顯；繼承的 Forecast 地圖語義仍成立；觀測與預報失敗獨立降級。
4. **圍欄／響應式**：第 6 節的圍欄與手機資訊面 outcome；桌機與 375 px 驗收；768 px 破版檢查。
5. **Radar**：顯示／隱藏、時間戳、有意義的地理對齊、瀏覽器只經本應用 API 取得。
6. **安全邊界**：V2 即時天氣的 CWA 存取只在伺服器端；瀏覽器永不取得或直接使用憑證；前端天氣資料請求留在 `/api/`；預報讀取路徑與 Grading App 不直接存取 CWA；金鑰不出現在 Git、前端資產、log 或 evidence。
7. **回歸**：V1 自動化套件維持全綠；下方 Forecast dashboard 與 Grading App 保持繼承行為；只在 V2 delta 可能實質影響處重驗繼承的手動驗收，**不重做整套 V1 evidence**。

證據類別：以消毒後的真實上游樣本與衍生反例做離線自動化驗證；後端／API 正常與失敗行為；適當 re-scope 的靜態／安全檢查；新地圖行為與重要失敗狀態的瀏覽器驗收與截圖；CI 回歸；憑證掃描；acceptor 設定 Vercel 金鑰後的 preview 部署驗證。

## 8. 相依、前置與風險

- **Bindings b3**（RB-3 金鑰位置新增 Vercel 環境變數）須在 V2 implementation activation 前生效（acceptor 合併；Bindings §0／§9）。
- **b2 executor binding dry-run** 在 `docs/governance/binding-verification.md` 仍記為「待辦」；首次以 b2 mapping 派 Executor 前須完成。
- **RB-5 workflows**：V1 OC §8.2 的 workflow 授權是 V1 契約內的特定授權，不是 Bindings §2.5 的 standing authorization（acceptor 2026-09-25 確認）。acceptor 已於 2026-09-25 另給 V2 的窄授權：只在為本 V2 工作保留或延伸驗證所必要時修改**既有的** HW01 CI／smoke workflow 檔，變更限於 home_work_01 行為；不含無關的 root 檔案、無關 workflow 或整體 CI 重設計；不需要就不改（OC §4 A-4）。V2 預期不需改 workflow（3.1 節）。
- **實作期金鑰使用**（acceptor 已授權，D-17）：只為擷取上游樣本與對已接受 V2 資料路徑做定向即時驗證；用本機未追蹤 `.env`；唯讀 GET；不輪詢、不壓測；不印出、不匯出；樣本／log／evidence 不含憑證；CI 不依賴即時憑證。不含建立、更換憑證或填入 Vercel。
- **Vercel 金鑰填入**由 acceptor 在部署階段執行；部署驗證 AC 以此為前提。
- 風險：O-A0001-001 也可能下架（明確失敗、不寫入）；Vercel function 時限／回應大小於實作期再驗證；雷達影像固定檔名每週期覆寫，metadata 時間與影像可能短暫不一致（實作註記）；雷達為等經緯度柵格、Leaflet 為 Mercator，須檢查對齊（實質偏移 route DA）；V2 合併 `main` 會更新 production URL，與 V1 繳交（RB-2）的先後由 acceptor 於合併時決定。

## 9. 詞彙 delta（接受後併入 `CONTEXT.md`）

| 詞 | 定義 | 避免 |
| --- | --- | --- |
| **Taiwan Map** | Dashboard 的地圖（沿用），現有兩個模式：Now mode、Forecast mode。 | weather map（泛稱）、station map |
| **Now mode** | Taiwan Map 的預設模式：顯示 Latest Observation、縣／測站下鑽、Refresh、Radar。 | live mode、realtime |
| **Forecast mode** | Taiwan Map 的 V1 六區七日預報模式：語義、Select Date、導出色帶不變。 | old map |
| **Latest Observation** | 伺服器最近一次成功自 CWA O-A0001-001 取得的測站觀測集合（CWA 發布值，非專案推導）。 | realtime data、live data、current forecast |
| **Observation Time** | 所顯示觀測資料的 CWA 觀測時刻（ObsTime）。 | updated at、data time |
| **Fetched Time** | 伺服器取得該資料的時刻。 | last updated（單獨使用） |
| **Refresh** | Now mode 的使用者動作：要求顯示最新的 Latest Observation（bounded staleness）。 | reload、sync |
| **Re-ingestion** | （原「Refresh」詞條改名）重跑 Ingestion 使持久化的 Forecast Snapshot 更新；OPTIONAL。 | refresh（V2 起） |
| **Stale** | 最近一次 Refresh／上游取得失敗，介面仍顯示上一次成功的觀測資料；純失敗基準。 | outdated（年齡意義） |
| **Unavailable** | 沒有可顯示的有效 Latest Observation。 | error（泛稱） |

## 10. 未定的實作 HOW／Later

**HOW（DA／Executor）**：重用視窗長度；Refresh 時限值；快取機制；Leaflet 常數、範圍 margin、snap-back；代表測站機制；密度管理；帶屬性縣界圖層的建置；底部資訊面實作；觀測氣溫色階；雷達變體選擇與重投影；endpoint 形狀與 payload 裁剪；測試框架、fixture 處理；Spec／檔案命名；票務粒度；瀏覽器歷史；reduced-motion；可選年齡警示；CWA 授權標示的呈現位置。

**Later**：第 4 節 OPTIONAL／Later 列。

---

## 附錄 A — 非契約的 UI／UX 設計建議（advisory only）

以 `ui-ux-pro-max` 作為設計鏡頭產出；**不是需求、不是 AC、不改變語義／架構／安全邊界、不重開 V1**。與已接受決定衝突時以決定為準。

- **Map-first 層級**：masthead 壓縮為一列（保留逐字標題），地圖卡直接在其下全寬；桌機以相對視窗的高度讓地圖明顯為主；下方區塊明確標題為「七日六區預報」，讓兩種語義一眼可分。
- **模式切換**：兩選項 segmented control，用真正的 button 與 pressed 狀態，標籤如「Now · Latest Observation」／「Forecast · 7-day」；桌機放面板頂端、手機放地圖上方第一列；切換時同步換圖例、面板標題與狀態列，只顯示現行模式的圖例。
- **桌機面板**：沿用 V1 左上浮動面板作為唯一脈絡面，三種脈絡（全臺總覽／縣／測站）；一行麵包屑「Taiwan › 縣 › 測站」兼作返回路徑；測站清單右對齊等寬數字；選取項會被面板遮住時平移地圖而非隱藏。
- **手機資訊面**：底部 sheet，peek 標頭含麵包屑、選取值與關閉鈕，展開把手供測站清單；捲動限制在 sheet 內；縮放、模式切換、Refresh 留在 sheet 之上。
- **縣／測站 affordance**：縣 hover 用描邊＋淡填色與名稱提示，觸控以點選為主；選縣後在面板／sheet 與地圖角落各有「Back to Taiwan」chip；測站 pill 印出氣溫，選取以外框與提升層級表示，按下回饋約 100 ms 內。
- **Refresh 與時間**：帶圖示與文字的 Refresh 鈕放在面板標頭、旁列「Observed HH:MM · Fetched HH:MM」；進行中停用並顯示 spinner；結果以 polite live region 宣告；Stale 為狀態列上的持續徽章，Unavailable 為面板內狀態，含原因、Retry 與前往 Forecast mode 的連結。
- **Radar 控制**：帶標籤的開關與自己的時間戳放在圖層列；overlay 畫在底圖之上、標記之下；透明度滑桿只在代價微小時提供；一句簡短說明產品名稱；沿用深色 vendored 底圖使回波色可讀。
- **響應式**：沿用 V1 斷點（寬螢幕浮動面板、其下堆疊、768、375）；pill 依內容決定寬度並設最小寬，文字放大不裁切；手機橫向時 peek 保持小。
- **無障礙／可用性**：用 button 不用 div；模式與 Radar 控制有 pressed 狀態；深色地圖上的可見焦點環；pill 文字對比 4.5:1；氣溫一律印出，顏色不是唯一訊號；面板內縣選單作鍵盤路徑；reduced-motion 下略過飛行動畫。
- **與下方 dashboard 的整合**：共用 V1 的卡片節奏與單一強調色；`Select Region` 維持既有行為（不與 Now mode 觀測值耦合）；觀測值永不交叉連結進預報卡片，讓推導值與觀測值分開。
