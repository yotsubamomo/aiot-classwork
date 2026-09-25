# Outcome Contract V2 — HW01 Weather Map V2（`home_work_01/`）

- **狀態**：**DRAFT（待 acceptor 接受）。** 接受前只是討論輸入；接受紀錄見第 9 節，由 acceptor 親自填寫。Agent 代寫的接受紀錄不等於取得授權（治理 §1.2、§5.3）。
- **性質**：V1 Outcome Contract（[`outcome-contract.md`](outcome-contract.md)，ACCEPTED 2026-09-23）之上的 **新工作、新 Outcome Contract**（治理 §5.3：「需要獨立接受的新增工作，以新的 Outcome Contract 承載」）。V1 Outcome Contract 與 Spec v1.1 **normatively 不變**，作為 inherited baseline；本檔只描述 V2 delta，並在第 2.4 節逐條列出其適用範圍被延伸、re-scope 或 supersede 的 V1 條款。
- **依據**：Minimal Operational Governance v2.0 §3.1 七項 properties；Project Bindings b2（[`../../../docs/governance/project-bindings.md`](../../../docs/governance/project-bindings.md)）§2.3、§2.4、§4、§5、§7。
- **來源紀錄**：2026-09-25 V2 Grill（acceptor 裁決 D-1～D-19、defaults P-1～P-36）；盤點見 [`../brief/BRIEF-V2.md`](../brief/BRIEF-V2.md)。
- **Acceptor**：GitHub `yotsubamomo`（Bindings §2.1）。

## 1. Intent and outcome

在已結案的 V1 產品之上，把部署於 Vercel 的 Dashboard 的 **Taiwan Map** 升級為 map-first 的互動天氣介面：預設的 **Now mode** 顯示 **Latest Observation**（CWA 測站觀測），支援 Taiwan → County → Station 下鑽、Refresh、可見的 Observation Time 與 Fetched Time、stale／unavailable 狀態，以及一個 **Radar overlay**；V1 的六區七日預報地圖保留為 **Forecast mode**，語義不變；下方 Forecast dashboard 功能不變。頁面同時承載兩種語義（CWA 發布的觀測值、專案推導的預報相容性值），兩者必須可見地分開。

V2 是 acceptor 明確授權、超出老師 Part A 需求的 ENHANCED 延伸（Bindings §2.4）；它不得取代、弱化或被呈現為老師要求的行為，Part A 的評分項目與 V1 的 MVM 行為不變。

## 2. Scope and boundaries

### 2.1 Inherited V1 baseline

- V1 Outcome Contract（ACCEPTED 2026-09-23，normative 第 1–7 節＝`c45ec61`）、Spec v1.1（EFFECTIVE）、DR-1～DR-22 與 phase acceptance 記錄，全部維持有效，除本檔第 2.4 節明列的 delta 外不變。
- 上位契約（`doc/requirement/`，唯讀）不變；V2 的觀測地圖構想來源是老師 Part B（B2-2～B2-4、B4、B16、B22、B24），依 `CONTEXT.md`「Part B 的元素只能經明確決定採用」——本檔即該決定；Part B 的架構（FastAPI、React／Next.js、Windy）仍為 REFERENCE／FUTURE。
- 下列 V1 產物 **不得改變**：Grading App `app.py`（只有 MVM、無地圖）；forecast ingestion；`data.db` 與 `TemperatureForecasts`；六區推導與 `weather_query.py` 的預報語義；預報 `/api/` endpoint 的語義；下方 Forecast dashboard 與 `Select Region` 行為（觀測值不得耦合進預報控制項）；V1 自動化測試（維持全綠，V2 只 re-scope 靜態檢查的適用範圍，不弱化）。

### 2.2 Scope classes

| Class | 內容 |
| --- | --- |
| **V2 Core（ENHANCED REQUIRED）** | (a) **Now mode**（頁面載入預設）：Latest Observation 測站氣溫標記；Taiwan-wide 視野每縣至多一個代表性有效測站；County 選取／下鑽與 County 脈絡；測站選取與測站詳情；Back to Taiwan；Refresh；Observation Time 與 Fetched Time；stale／unavailable 狀態。(b) **Forecast mode**：V1 六區地圖（Select Date、導出色帶、資訊）語義不變；明顯、有標籤的模式切換。(c) **地圖圍欄**：pan／zoom-out／zoom-in 三項 outcome。(d) **響應式可用性**：桌機與 375 px；手機底部資訊面。(e) 三條資料路徑（Observation／Forecast／Radar）獨立降級。(f) 文件與驗收證據更新（README、`doc/acceptance/`、`CONTEXT.md` 詞彙）。 |
| **V2 Radar（ENHANCED REQUIRED）** | 最新雷達回波 overlay（CWA O-A0058 系列，臺灣鄰近範圍）：顯示／隱藏、時間戳、與地圖有意義的地理對齊、經本應用 `/api/` 代理、狀態與時間戳獨立於觀測。透明度調整只在實作代價微小時提供。 |
| **OPTIONAL／Later（不在接受範圍，不得成為完成條件）** | 獨立雨量圖層（O-A0002-001）；雷達動畫／歷史回放；heatmap；自動更新；縣市篩選與測站搜尋；URL deep-linking；10 分鐘資料集（O-A0003-001）升級；歷史觀測儲存；Windy；22 縣市預報；Grading App 的任何 V2 行為。 |

「MVM」在本專案專指 Part A 評分基線；本檔不使用「V2 MVM」。V2 全部項目只在部署的 Dashboard（V1 INV-9 不變）。

### 2.3 Non-scope（明確排除）

- 任何持久化伺服器狀態、Redis／Postgres、queue、背景 worker、新雲端基礎設施；契約不要求持久伺服器狀態。
- 瀏覽器直接呼叫 CWA 或任何外部主機；前端外部主機例外（含 Radar）。
- 專案推導的縣平均氣溫或任何觀測值的聚合推導值。
- 以年齡為契約的 stale 條件；自動 Refresh；輪詢。
- 修改 V1 Outcome Contract、Spec v1.1、derivation record 的 normative 文字（第 2.4 節的 delta 由本檔與 V2 Delta Spec 承載）。
- 上述 OPTIONAL／Later 列。

### 2.4 受 V2 delta 影響的 V1 條款（逐條；不回溯改寫 V1 文字）

| V1 條款 | 效果 | V2 delta（依據） |
| --- | --- | --- |
| OC AB-5「兩個呈現層都只從 `data.db` 以 SQL 取得資料…應用程式不呼叫 CWA API」；Spec INV-6「呈現層不呼叫 CWA」 | **re-scope** | 對預報路徑（Grading App、共用預報查詢模組、預報 `/api/`、Forecast mode、下方 dashboard）繼續完整有效。部署的 Dashboard 新增 **server-side** 觀測／雷達路徑：瀏覽器 → 本應用 `/api/` → 伺服器端向 CWA 取得 → 正規化／裁剪回應。（D-2） |
| Spec R-SHR-5、R-DS-5「Python 端不得 import HTTP client…不得含 `opendata.cwa.gov.tw` 字串」；AC-04(a)；R-TC-1 靜態檢查 | **re-scope** | `app.py`、共用預報查詢模組與預報讀取路徑維持無 HTTP client、無 CWA 字串；部署 Dashboard 後端得含 V2 伺服器端 CWA 存取。靜態檢查依此 re-scope，不弱化；不要求特定模組結構。瀏覽器端 JS 資料請求仍只指向 `/api/`。（D-2、D-17(6)） |
| Spec R-DS-8「執行期不需要任何環境變數或 secret」；R-SEC-3「部署的 Dashboard MUST 不需要任何 secret；Vercel 專案不設定 CWA 金鑰」；AC-07(e)「Vercel 專案不需環境變數」；Spec §4.1「憑證…Dashboard 不需 secret」 | **supersede（V2 起）** | 部署的 function 為觀測／雷達路徑自 Vercel 專案環境變數讀取 CWA 金鑰；預報路徑仍不需 secret。金鑰由 acceptor 親自填入，不印出、不匯出、不提交、不進前端、不進 log／evidence。（D-3） |
| Bindings RB-3「金鑰只能放在未追蹤的本機 `.env`」；Spec R-SEC-1「唯一授權位置」；INV-5；OC §2.5、AB-8 | **extend** | Vercel 專案環境變數成為第二個授權位置（Bindings **b3**，須先生效，第 8 節）。AB-8 其餘條件（不進 git、log、前端、文件、evidence）不變並適用於 V2。（D-3） |
| OC §2.2 ENHANCED「Leaflet Taiwan Map，六區依 Derived Map Temperature 著色、可查看地區 Min／Max」；AB-14；Spec R-EN-3、R-EN-4、AC-17、AC-18；DR-20 全部 | **extend（retain as Forecast mode）** | 這些條款在 **Forecast mode** 內原樣成立；Taiwan Map 預設為 Now mode；模式切換必須明顯有標籤；README 與驗收證據必須讓 Forecast mode（老師 Part A 加分地圖）容易找到。不搬移、不移除。（D-6） |
| Spec R-EN-1、AC-19（UI 品質清單、三種狀態截圖）；R-EN-7（整合） | **extend** | 清單同樣適用於 V2 的新介面（模式、面板、底部資訊面、Now mode 狀態）；三種狀態涵蓋 V2 的 stale／unavailable。（D-11、D-15） |
| Spec R-DS-6、DR-19（預報快照失敗 → 頁面層級 error 遮蔽整個 dashboard） | **delta** | 觀測、預報、雷達三條路徑獨立降級：預報快照失敗依 V1 語義影響 Forecast mode 與下方 dashboard，不得停用健康的 Now mode；觀測失敗只影響 Now mode；雷達獨立。AC-10「頁面顯示錯誤狀態」對受影響部分仍成立。（D-13） |
| Spec R-DS-2、DR-7、DR-9、AC-15、AC-16、AC-22（`/api/health`、smoke） | **不變（重申）** | `/api/health` 保持 V1 部署健康語義，永不依賴 CWA 即時可用性；觀測／雷達狀態另行揭露。（P-24） |
| Spec AC-04(b)、DR-20.4、DR-20 X-1（前端資料請求只指向 `/api/`、零外部請求） | **不變（重申）** | Radar 影像與觀測資料皆經 `/api/`；不新增前端外部主機例外。（D-7） |
| Spec §8「REFERENCE／FUTURE：Part B 的測站觀測、heatmap、自動更新、圖層切換」；DR-20 X-4（新增資料功能在 #28 之外） | **re-scope** | 測站觀測 → V2 Core；模式／Radar 切換 → V2；heatmap、自動更新仍為 Later。X-4 所指的新資料功能由本檔承載。（D-4） |
| Spec §8「不做：離島三縣的任何呈現」 | **re-scope（只限 Now mode）** | Now mode 涵蓋 22 縣市中有有效觀測資料者（含澎湖、金門、連江）；Forecast mode 六區語義與地理不變。（P-7） |
| DR-20 P-2c（vendored 底圖只是 backdrop，不承載縣市層級資料語義） | **extend** | #28 底圖仍為 backdrop；V2 另加帶名稱屬性的縣界互動圖層，只作互動幾何，不以資料著色。（D-8、P-30） |
| Spec INV-7、R-DOC-2、AC-14（標示要求） | **extend** | 觀測值標示為 CWA 測站觀測（如發布），與專案推導的六區預報值可見地分開、不共用圖例或色階；CWA 資料授權標示（政府資料開放授權條款）納入文件要求。（P-2） |
| `CONTEXT.md`「Refresh」「Taiwan Map」詞條 | **glossary delta** | 「Refresh」改為 Now mode 使用者動作，原意改名「Re-ingestion」；「Taiwan Map」增加 Now mode／Forecast mode；新增 Latest Observation、Observation Time、Fetched Time、Stale、Unavailable。（D-19） |

未列於上表的 V1 條款一律不變（含 INV-1、INV-2、INV-3、INV-4、INV-8、INV-9、R-TC-5「測試不需網路與金鑰」、AC-26、R-DS-4、R-DS-7、R-GA-*、R-ING-*、R-DER-*、R-DB-*）。

### 2.5 語義（accepted 語義，Delta Spec 在此邊界內 derive AC）

- **S-1 Latest Observation 保證**（D-1、D-5）：latest published, bounded staleness。載入與 Refresh 顯示伺服器最近一次上游取得的最新觀測；短暫的共用重用視窗可接受（長度屬 Spec／HOW）；Observation Time 與 Fetched Time 永遠可見；Refresh 不得清空有效資料；上游失敗保留上一次有效資料並清楚標示 stale／unavailable。資料來源 CWA **O-A0001-001**（逐時），用語「Latest Observation」，不用「realtime」。
- **S-2 資料規則**（P-1、P-16～P-19、P-15）：無有效氣溫或無 WGS84 座標的測站不進氣溫圖層；缺值／哨兵欄位顯示「—」、永不顯示為數值；成功＝回應可解析且至少一個有效測站，零有效測站＝失敗；成功的 Refresh 不得以較舊的 Observation Time 取代已顯示資料；測站數少於平常仍是成功、顯示有效測站數、不設契約最小數量；StationId 為穩定識別、名稱可重複。
- **S-3 模式**（D-6、P-28）：Now 預設；切換明顯有標籤；Forecast mode 保留六區／Select Date／導出色帶語義；切換保留使用者目前地理脈絡（除非某模式確實需要不同的有效視野）；「單一地圖實例」屬 HOW。
- **S-4 下鑽**（D-8、D-9、P-7～P-14）：Taiwan → County → County 內測站 → 測站詳情。County 脈絡＝縣名、有效／顯示測站數、最高與最低氣溫測站（名稱／值）、含氣溫的測站清單；**不計算、不顯示縣平均**。Back to Taiwan 清除選縣並回到全臺視野。Taiwan-wide 視野每縣至多一個代表性有效測站；選取／後備機制屬 HOW，但必須確定性、只依有效現行測站、有文件、可客觀驗證；Spec 不列舉 StationId。中間縮放層級的密度管理屬 HOW。無選取時面板可顯示 Observation Time、Fetched Time、Refresh、有效測站數、最高與最低測站，無平均。
- **S-5 測站詳情**（D-10）：契約必要＝測站名稱／識別、縣、鄉鎮、Observation Time、氣溫。有效時顯示、否則「—」＝相對濕度、風速、風向、氣壓、今日雨量（取自觀測資料集）、天氣現象。單一欄位不獨立成為契約關鍵。
- **S-6 失敗語義**（D-11、D-12、P-20～P-27）：首次載入無有效資料 → 留在 Now mode、地圖與縣界可見、明確的 Latest Observation unavailable 狀態、非機密原因、Refresh 可用、Forecast mode 可見、不自動切換、不暗示預報資料是觀測。**Stale**＝最近一次 Refresh／上游取得失敗而介面仍顯示上一次成功資料（純失敗基準；年齡不是契約條件；年齡警示屬 HOW 且不得重定義 stale）。伺服器端失敗分類（驗證用）：金鑰未設定；上游不可達／逾時；上游錯誤狀態（含 auth／quota）；無效或空回應。使用者可見錯誤不得含金鑰、原始上游 URL、原始上游回應／錯誤內容。每次 Refresh 在有界時間內到達 success／stale／unavailable（界值由 DA 於 Delta Spec 決定，如客觀驗收需要）。重用視窗內的 Refresh 可回同一 Fetched Time 並告知已是最新。只有手動 Refresh。
- **S-7 獨立降級**（D-13）：觀測失敗只影響 Now mode；Forecast mode 與下方 dashboard 在其快照有效時維持可用；預報快照失敗依 V1 錯誤語義影響 Forecast mode 與下方 dashboard，不得自動停用健康的 Now mode；Radar 狀態與時間戳獨立於觀測。`/api/health` 語義不變。
- **S-8 圍欄**（D-14）：pan——使用者不得離開有用的臺灣範圍而造成大片無意義空白，金門、連江仍可到達；zoom-out——不得縮到臺灣小到無用或空白主導；zoom-in——支援縣／局部層級的個別測站選取，不允許無意義的過度放大。minZoom／maxZoom／bounds／margin／viscosity 為 HOW／驗證參數；「初始視野即最寬視野」不是產品需求。初始視野提供本島＋澎湖的有用脈絡。
- **S-9 手機資訊面**（D-15）：375 px 的縣／測站詳情用可關閉的底部資訊面：normal／peek 狀態下地圖可見；需要時可展開（測站清單）；一個清楚可見的關閉控制；滑動可有但不得是唯一關閉方式；開啟中選另一測站即更新；關鍵地圖控制可用、不被完全遮蔽。函式庫、高度、動畫、snap 點、CSS 屬 HOW。
- **S-10 其他 outcome**（P-29～P-36）：可見標記在驗證視野下可讀可選，密度管理不得使地圖不可用，縣下鑽後該縣測站皆可到達，不要求 375 px 全臺視野同時顯示 22 個代表 pill；地圖為主要內容區、模式切換不捲動即可見、頁面標題逐字 `Taiwan Weather Forecast`；overlay 不得使地圖不可用、目前選取項與關鍵控制可見可達、鍵盤焦點永不被完全遮蔽；縣選取有非地圖的鍵盤路徑、測站詳情有測站清單的鍵盤路徑，多邊形與標記不必各自可聚焦；瀏覽器歷史、`prefers-reduced-motion` 屬 HOW／Later。
- **S-11 Radar**（D-4、D-7、P-36）：顯示／隱藏、時間戳、與地圖有意義的地理對齊（不預先接受實質偏移為已知限制；實作發現系統性偏移／重投影問題即 route DA；細微邊緣差異可記錄，明顯錯位不可）、只經本應用 `/api/`、狀態獨立。

### 2.6 架構與安全 constraints

- **C-1** V2 即時天氣的 CWA 存取只在伺服器端；瀏覽器永不取得或直接使用憑證；前端天氣資料請求留在本應用 `/api/`；預報讀取路徑與 Grading App 不直接存取 CWA；金鑰不出現在 Git、前端資產、log、evidence。模組結構屬 HOW。
- **C-2** 最小架構：Flask、Vercel 單一 function、Leaflet、SQLite 預報快照、Streamlit Grading App、既有 CI 全部保留；契約不要求持久伺服器狀態；快取機制屬 HOW；上游 payload 於前端使用前正規化／裁剪。
- **C-3** 金鑰位置：本機未追蹤 `.env`；部署為 acceptor 填入的 Vercel 專案環境變數（b3 條件：acceptor 填入、不印出／匯出、不提交、不進前端、不進 log／evidence）。
- **C-4** 兩種語義分開：觀測值標示為 CWA 測站觀測（如發布），不與專案推導的預報值共用圖例或色階；Forecast mode 與下方 dashboard 維持 V1 的推導值標示。CWA 資料授權標示依政府資料開放授權條款（「交通部中央氣象署 [資料名稱]」）：這是外部授權／法遵的**文件 constraint**（acceptor 2026-09-25 確認），不是新的產品功能；標示的實際呈現位置屬 HOW。
- **C-5** Reserved boundaries RB-1～RB-6（Bindings §2.6）維持保留；不因本檔擴張。

## 3. Acceptance boundary

每條為可觀察的 PASS／FAIL 與證據類別；具體 AC 由 Design Authority 於 V2 Delta Spec 在此邊界內 derive，Delta Spec 全體合起來須涵蓋本節全部。證據類別不指定框架、檔名、fixture、mock、票務或順序。

| ID | Class | 可觀察條件 | 證據類別 |
| --- | --- | --- | --- |
| AB-V2-1 | Core | 頁面載入為 Now mode；明顯有標籤的切換可到 Forecast mode；Forecast mode 下 V1 AC-17／AC-18 原樣成立；切換保留地理脈絡（S-3） | 瀏覽器驗收與截圖（桌機、375）；V1 回歸 |
| AB-V2-2 | Core | Now mode 顯示 Latest Observation 測站氣溫；Observation Time 與 Fetched Time 可見；抽樣顯示值等於本應用 `/api/` 回應、`/api/` 正規化值可追溯至對應上游測站紀錄；哨兵永不顯示為數值（S-1、S-2、S-5） | 以消毒真實樣本的離線自動化驗證；API 驗證；瀏覽器抽樣；preview 部署驗證 |
| AB-V2-3 | Core | Refresh 在有界時間內到達 success／stale／unavailable；成功不清空資料；視窗內 Refresh 回同一 Fetched Time 並告知最新；較舊 Observation Time 永不取代較新；零有效測站＝失敗（S-1、S-2、S-6） | API 驗證（含反例）；瀏覽器模擬 |
| AB-V2-4 | Core | 四類伺服器端失敗各自可辨、訊息不含金鑰／上游 URL／上游內容；首次載入失敗 → S-6 的 unavailable 狀態；Refresh 失敗 → stale 且保留資料（S-6） | API 驗證；瀏覽器截圖（stale、unavailable） |
| AB-V2-5 | Core | 預報快照不可用時 Forecast mode 與下方 dashboard 依 V1 錯誤語義、Now mode 正常；觀測失敗只影響 Now mode；Radar 狀態獨立；`/api/health` 語義不變（S-7） | API 驗證；瀏覽器模擬狀態；既有 smoke |
| AB-V2-6 | Core | County hover／選取／視野調整、County 脈絡內容、測站清單、測站詳情、Back to Taiwan 皆如 S-4／S-5；Taiwan-wide 代表測站規則確定性且有文件；縣下鑽後其有效測站皆可到達 | 瀏覽器驗收；規則的自動化驗證；README 文件審查 |
| AB-V2-7 | Core | S-8 圍欄三項以拖曳／縮放可觀察；金門、連江可到達；初始視野含本島＋澎湖 | 瀏覽器驗收（桌機、375） |
| AB-V2-8 | Core | S-9 手機資訊面 outcome；S-10 可用性 outcome；44×44 CSS px 目標；375 px 無不必要橫向捲動；桌機 ≥ 1024 與 375 px 驗收、768 px 破版檢查；鍵盤路徑存在 | 瀏覽器驗收與截圖；DOM 檢查（如 V1 的 scrollWidth） |
| AB-V2-9 | Radar | Radar 顯示／隱藏、時間戳、與海岸線有意義的對齊、狀態獨立；瀏覽器只經 `/api/` 取得（S-11） | 瀏覽器截圖（開／關）；API 驗證；靜態檢查 |
| AB-V2-10 | Core | 安全邊界 C-1／C-3：靜態檢查 re-scope 後通過；憑證掃描（含新路徑）零命中；前端請求只指向 `/api/`；部署的 Now mode 在 acceptor 設定金鑰後可運作而 repo／log／evidence 無金鑰 | 靜態檢查；憑證掃描；preview 部署驗證；Reviewer 審查 |
| AB-V2-11 | Core | V1 自動化套件全綠；Grading App 與下方 dashboard 繼承行為不變；只在 V2 delta 可能實質影響處重驗繼承的手動驗收（Forecast mode 的 AC-17／18／19、標題與 masthead）；不重做整套 V1 evidence | CI；選定截圖 |
| AB-V2-12 | Core | 文件：README 記述 Now／Forecast mode（Forecast mode 容易找到）、Latest Observation 來源與逐時節奏、代表測站規則、觀測／推導值標示、CWA 授權標示、Vercel 金鑰設定步驟（不含值）、Later 項目；`doc/acceptance/` 逐條對應 V2 AC；`CONTEXT.md` 詞彙 delta 併入 | 文件審查 |
| AB-V2-13 | Core | Vercel preview／production 提供 V2 dashboard；`/api/health` 既有 smoke 通過；Now mode 於部署上回傳 Latest Observation（acceptor 填入金鑰後）；部署 commit 與受審 subject 對應 | smoke 輸出；preview 驗證紀錄 |

## 4. Authority and authorization

- **Acceptor**：`yotsubamomo`。接受本契約即授權具相應 authority 的 Agents 在此邊界內規劃、derive Spec／Tickets、實作、審查、修正至完成（治理 §1.2）。
- **Standing**（Bindings §2.5）：SA-1 topic branch commit 與 push；SA-2 開 PR。
- **Reserved**（Bindings §2.6，不擴張）：RB-1 合併 `main`；RB-2 繳交；RB-3 憑證管理；RB-4 付費；RB-5 單元目錄外的檔案；RB-6 破壞性 git。
- **本契約的特定授權**（acceptor 於 2026-09-25 grill 中給出，D-3、D-17）：
  - **A-1 Bindings b3**：Vercel 專案環境變數為 CWA 金鑰的授權位置（條件見 C-3）。Bindings 變更依治理 §5.3 與 Bindings §9 留紀錄，由 acceptor 合併生效；**須在 V2 implementation activation 前生效**。
  - **A-2 金鑰填入 Vercel**：acceptor 於部署階段親自執行（RB-3）。
  - **A-3 實作期金鑰使用**：授權有界、唯讀地使用既有本機專案憑證，只為 (i) 擷取必要的上游樣本；(ii) 對已接受的 V2 資料路徑做定向即時驗證。條件：用未追蹤本機 `.env`；只有唯讀 GET；不輪詢、不壓測；不印出、不匯出；已提交樣本、log、evidence 不含憑證；CI 不依賴即時憑證。不含建立、更換憑證或填入 Vercel。
  - **A-4 RB-5 workflows**：V1 OC §8.2 的 workflow 授權是 V1 契約內的特定授權，**不是** Bindings §2.5 的 standing authorization，不自動適用於 V2（acceptor 2026-09-25 確認）。acceptor 另於 2026-09-25 依 RB-5 給予 V2 的**窄授權**（原文逐字）：「modification of the EXISTING HW01 CI / smoke workflow files only when necessary to preserve or extend verification for this accepted V2 work; changes must remain scoped to HW01 / home_work_01 behavior. This does NOT authorize: unrelated root-file changes; unrelated workflows; broad repository CI redesign. If no workflow change is needed, do not modify them.」V2 預期不需修改 `.github/workflows/`（既有 CI 以 `home_work_01/**` 觸發並執行全部測試）；本授權於第 9 節接受紀錄再次引用。
- **不需外部確認**：V2 為專案內部的 ENHANCED 延伸；不需老師確認。

## 5. Relevant context

- **既有產物**：V1 Outcome Contract、Spec v1.1、DR-1～DR-22、`doc/acceptance/ACCEPTANCE.md`、`README.md`、`CONTEXT.md`、`.env`（未追蹤）、production `https://aiot-hw01-weather.vercel.app`。
- **外部事實**（2026-09-25 自官方目錄查證，實作時再驗證即時結構；brief §3.2）：O-A0001-001 逐時、樣本 876 站（845 有效氣溫）；O-A0058-003 每 10 分鐘、PNG 3600×3600 ≈ 680 KB、範圍 lon 118–124／lat 20.5–26.5、metadata 需金鑰（fileapi）；一般會員額度 20,000 次／日、2 GB／日；授權標示要求。
- **已知風險**：O-A0001-001 可能下架（明確失敗、保留資料）；Vercel function 時限與回應大小限制實作時再驗證；雷達影像固定檔名每週期覆寫，metadata 時間與影像可能短暫不一致；雷達等經緯度柵格與 Mercator 的對齊（S-11）；V2 合併 `main` 會更新 production URL，與 V1 繳交（RB-2）先後由 acceptor 於合併時決定，不在本契約內。

## 6. Assurance path

- **Lane**：**Formal（lean）**（Bindings §4；治理 §3.6-B／C：新的產品行為與 invariant baseline、多 execution units）。Design Authority derive **V2 Delta Spec**（以參照繼承 V1 Spec v1.1，不重寫 V1；逐條列出 re-scope／supersede／extend 的 V1 條款）與一組小而連貫的垂直切片 Tickets（**粒度與數量屬 DA derivation，本檔不設數量要求**），附 derivation record。
- **Audit**：每張 Ticket 的 independent audit；Delta Spec 的 Spec Integration Audit；Design Authority phase acceptance；Orchestrator run-to-completion（可沿用 V1 的 unattended-run policy）。
- **高風險類別**：H-1（憑證）、H-2（老師指定介面）、H-3（標示）繼續適用；V2 新增的伺服器端 CWA 路徑是否需要新增類別由 DA 以 decision record 確認（Bindings §5）。
- **Release gate**：合併進 `main` 由 acceptor 執行（RB-1），前提依 Bindings §5（全部 Ticket 結案、Spec Integration Audit closure、phase acceptance、README 實跑、無追蹤中的機密）。

## 7. Stable reference

- 本檔：`home_work_01/doc/governance/outcome-contract-v2.md`；接受時的 commit SHA 記於第 9 節。
- 盤點：`home_work_01/doc/brief/BRIEF-V2.md`（同一 commit）。
- Inherited baseline：V1 Outcome Contract（`c45ec61` normative；接受紀錄 `d42b1a7`）、Spec v1.1、`main` = `ef15d3e`（V1 結案）＋ `0af4f2d`（Bindings b2）。

## 8. Activation preconditions（缺任一項時只停止受影響路徑）

| # | 項目 | 狀態（2026-09-25） | 依據 |
| --- | --- | --- | --- |
| 1 | acceptor 接受本契約並填寫第 9 節接受紀錄 | 待辦 | 治理 §1.2；Bindings §2.3 |
| 2 | Bindings **b3**（RB-3 金鑰位置新增 Vercel 環境變數）由 acceptor 合併生效 | **待辦（blocker）** | Bindings §0「新設定不自動適用進行中的工作」、§9；D-3 |
| 3 | b2 `executor` binding dry-run 完成並記入 `docs/governance/binding-verification.md` | **待辦（blocker；檔案記為「待辦」）** | Bindings §9 b2 列、§8.2 #4 |
| 4 | DA derive V2 Delta Spec 與 Tickets，附 derivation record；DA 確認高風險類別 | 接受後 | 治理 §3.4；Bindings §5 |
| 5 | RB-5 workflows：acceptor 已於 2026-09-25 給予窄授權（A-4）；接受紀錄再次引用 | 已授權（A-4） | A-4；RB-5 |
| 6 | acceptor 於部署階段填入 Vercel 金鑰（AB-V2-10、AB-V2-13 的前提，不是 activation 前提） | 部署時 | A-2；RB-3 |

## 9. 接受紀錄

| 欄位 | 內容 |
| --- | --- |
| 狀態 | **DRAFT — 未接受** |
| Acceptor | GitHub `yotsubamomo`（Bindings §2.1） |
| Acceptor 原始指示（引用原文） | （待 acceptor 於對話中給出接受原文後逐字轉錄） |
| 日期 | — |
| 接受的檔案 commit SHA | — |
| RB-5 workflows 准駁 | — |
| 前置證據 | Bindings b3 生效的 commit；b2 dry-run 紀錄 |

寫入者：待接受時由主 session 依 acceptor 的明確指示逐字轉錄；接受與授權的效力來自 acceptor 原文，不來自轉錄。
