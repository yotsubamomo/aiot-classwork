# Decision record — Dashboard 三種狀態（loading／empty／error）的條件對應（`home_work_01/`）

- **紀錄類型**：Design Authority decision record（治理 §3.6-A：在不改變任何 accepted 語義的前提下裁決既有來源尚未寫明之處；治理 §5.3 第 2 類「不改變 accepted 語義的 derived contract clarification」，須記錄對進行中工作、dependencies 與既有 evidence 的影響）
- **編號**：**DR-19**（延續 [`decision-20260923-spec-interpretation-rulings.md`](decision-20260923-spec-interpretation-rulings.md) DR-1～DR-16、[`decision-20260924-ingestion-timestamp-semantics.md`](decision-20260924-ingestion-timestamp-semantics.md) DR-17、[`decision-20260924-ac22-workflow-dispatch-release-evidence.md`](decision-20260924-ac22-workflow-dispatch-release-evidence.md) DR-18）
- **日期**：2026-09-24
- **來源**：Issue #23 cycle 1 R1 audit record [`../audit/issue-23-c1-r1.md`](../audit/issue-23-c1-r1.md) §4 **F-2** ／ §6 routing signal **RS-1**（治理 §4.2：契約不足是 routing signal，不是 blocking finding；unattended-run policy N-16、N-27）；由 Orchestrator 依治理 §2.4 派工，run record [`../run/run-20260924-hw01-formal.md`](../run/run-20260924-hw01-formal.md)
- **相關契約**：Outcome Contract（ACCEPTED 2026-09-23）§2.2「基本錯誤狀態」、§2.5、AB-10、AB-15；Spec v1.1 R-SHR-2(a)(b)、R-GA-7、R-DS-2、R-DS-3、R-DS-6、R-EN-1(5)、AC-10、AC-16、AC-19、INV-2、§4.1「健康 endpoint」、§4.2；DR-1、DR-9；`CONTEXT.md`「Forecast Snapshot」「Dashboard」；brief §6.4、§6.7；[`derivation-SPEC.md`](derivation-SPEC.md) §11.1（#23、#24、#25 列）
- **執行角色**：`gov-design-authority`（binding 核對由派工者依 Bindings §3.4 記入 run record）
- **效力**：與 Spec v1.1 同一效力層級，作為 R-EN-1(5)、R-DS-6、AC-10（Dashboard 部分）、AC-19（三種狀態截圖）與 DR-9（Dashboard 部分）的解讀依據；Executor、Reviewer（含 R2、Spec Integration Audit）、Orchestrator 以本紀錄適用該等條款，不得重開。Spec 文字不變；下次一致性修訂 MAY 在 AC-10 與 R-EN-1(5) 加註 DR-19（metadata 層級）。本紀錄不修改任何實作或測試。

## 1. 問題

R-EN-1(5) 要求 Dashboard 的 loading、empty、error 三種狀態「各自有可見呈現」；AC-10 要求 `data.db` 缺失或為空時「`GET /` 頁面顯示錯誤狀態」，證據欄寫「瀏覽器截圖（error 狀態）」；DR-9 把不完整快照也定為「頁面顯示錯誤狀態」；R-DS-6 要求前端對 503／404／網路失敗顯示明確訊息。但契約沒有寫明**哪些後端條件對應 empty 呈現、哪些對應 error 呈現**。

#23 的受審 subject（`610a797`）把 `/api/health`、`/api/regions` 的**任何**非 2xx 回應（含 503 missing／empty／incomplete、500／502／504、404）都呈現為中性的 empty 狀態「No forecast data yet」，只有網路失敗才呈現 error 狀態；#23 之前（`39fbab7`）三種快照不可用條件都是紅色 error banner。需要裁決：(a) 條件 → 狀態的對應規則；(b) #23 現況是否為必須修正的契約回歸。

## 2. 事實（依原始證據，不採用 Executor／Reviewer 的結論）

| # | 事實 | 證據 |
| --- | --- | --- |
| E-1 | Subject `610a797`：`bootstrap()` 對 `/api/health` 的 `!res.ok` 一律 `showEmpty(reasonMessage(res.body))`（含註解「503 … -> empty state」），`loadRegions()` 對 `/api/regions` 的 `!res.ok` 亦 `showEmpty`；`showError` 只在 `fetch` reject（網路失敗／例外）時呼叫。empty 呈現為 `#page-empty`（`role="status"`、中性配色、標題「No forecast data yet」）；error 呈現為 `#page-error`（`role="alert"`、紅色、標題「Something went wrong」）。`regions` 為空陣列時 `showEmpty("No Regions are available…")`。 | `610a797:home_work_01/static/app.js:89-128`、`index.html:23-48`、`styles.css:151-163` |
| E-2 | 同 subject 的 per-Region 層：`/series` 非 2xx 或網路失敗時在 chart card 內以 `#chart-status`（`.state--inline`，與「Loading <Region>…」同一 info 樣式）顯示 404 訊息、伺服器 `error` 訊息或「Cannot load this Region right now…」，並隱藏 summary、清空表格；2xx 但 `series` 為空時 `renderChart`／`renderTable`／`renderSummary` 都不畫任何東西，chart card 只剩標題。 | `app.js:142-172, 177-181, 195-204, 224-226` |
| E-3 | #23 之前（`39fbab7`，#20 結案版）：`/api/health`、`/api/regions` 非 2xx → `showPageError(reasonMessage(res.body))`，呈現為 `#page-error`（`banner--error`、`role="alert"`）。#20 R1 audit 的 AC-10 列與 INV-2 列以此為 PASS 依據（「不完整的快照依 DR-9 顯示錯誤狀態」）；截圖 `doc/acceptance/screenshots/ac10_dashboard_error_missing_db.png`。 | `39fbab7:home_work_01/static/app.js:42-60, 286-295`、`index.html:13-14`；[`../audit/issue-20-c1-r1.md`](../audit/issue-20-c1-r1.md) AC-10、INV-2、F-4 列 |
| E-4 | 後端：快照狀態非 ok 時，`/api/health` 與四個資料 endpoint 都回 503 JSON `{status:"unavailable", reason:"missing"|"empty"|"incomplete", error:<人類可讀訊息>}`；三個 `error` 訊息分別指出資料庫缺失、尚無快照、快照不完整，並提示執行 ingestion。未知 Region／日期回 404 JSON 含 `error`。 | `home_work_01/server.py:44-57, 80-87, 98-160`；R-DS-2、R-DS-3 |
| E-5 | Outcome Contract：§2.2 MVM 清單把這項行為命名為「**基本錯誤狀態**」；AB-10 標題同為「基本錯誤狀態」，可觀察條件是「兩個呈現層在 `data.db` 缺失或為空時顯示明確訊息而非 crash」；AB-15 要求「loading／empty／error 狀態」（ENHANCED，UI／UX 品質清單）。 | `outcome-contract.md:27, 78, 83` |
| E-6 | Spec v1.1：AC-10 對缺失資料庫寫「`GET /` 頁面顯示錯誤狀態」、對空表寫「同上（原因 empty）」，證據欄「瀏覽器截圖（**error** 狀態）」，FAIL 例「例外堆疊；空白頁；health 仍回 200」；R-EN-1(5) 用同一組英文詞「loading、empty、error」；AC-19 要求「loading／empty／error 三種狀態各一張截圖（**可用 DevTools 模擬**）」；R-DS-6「前端 MUST 處理 API 的 503／404／網路失敗：顯示明確訊息，不得留下空白頁或未處理的 console 例外作為唯一提示」。 | `SPEC.md:191, 200, 261, 270` |
| E-7 | DR-9 對不完整快照的裁決刻意區分兩層：Grading App「顯示警告、MAY 仍顯示既有資料」；Dashboard「`/api/health` 回 503，資料 endpoint 回 503，**頁面顯示錯誤狀態**」。R-GA-7 同樣區分缺失／為空（明確訊息）與不完整（警告）。 | DR-9；`SPEC.md:178` |
| E-8 | 產品語義：Forecast Snapshot 定義為「恰 6 Region × 7 完整 Forecast Day」；MVM「用準備好的快照」交付；Region 清單固定六個；`ok` 當且僅當 6 × 7 每格有值。因此在正確部署下，任何 2xx 回應的 payload 都不會是空的；部署的 Dashboard 出現 503（missing／empty／incomplete）只會來自部署缺檔、未跑 ingestion 或人為改動——是**運作故障**，不是「資料尚未產生」的正常階段。Dashboard 的 MVM 行為不得弱於 Grading App（INV-2、OC §2.4）。 | `CONTEXT.md`「Forecast Snapshot」「Grading App」「Dashboard」；OC §2.4、§2.5；R-SHR-2(a)(b) |
| E-9 | R-EN-1(5) 的來源 brief §6.4 是 framework-agnostic 的 UI／UX 品質清單「明確的 loading／empty／error 狀態」；brief §6.7 另採 Part B 的「明確的 stale／empty／error **訊息**」。兩處都只列狀態名，沒有條件對應。 | `BRIEF.md:193, 196` |
| E-10 | 沒有任何測試釘住頁面層級的 empty／error 對應（`tests/` 內無 `page-empty`、`page-error`、`showEmpty`、`role="alert"`、「No forecast data」）。 | DA grep `home_work_01/tests/` |
| E-11 | #23 的 worklog 把「empty ＝ `/api/health` 回 503（missing／empty／incomplete）」記為實作決定（決定 4），未引用任何裁決；R1 F-2 指出此決定與 AC-10 字面不符，並將分類交 DA。 | `worklog/issue-23.md:22, 45`；R1 F-2 |

## 3. 兩種解讀

- **(A) 依請求結果分類**（UI 慣用定義）：loading ＝ 請求進行中；**error ＝ 請求失敗**（非 2xx——含 503、404、500／502／504——或網路失敗、回應無法解析）；**empty ＝ 請求成功（2xx）但沒有可呈現的內容**。在此讀法下 AC-10 的三種條件（missing／empty／incomplete → 503）都是 error。
- **(B) 依資料有無分類**（#23 實作的讀法）：empty ＝ 快照不可用（503，不論原因）；error ＝ 只限網路失敗或非預期例外。在此讀法下 AC-10 的「頁面顯示錯誤狀態」被讀成「任何有明確訊息、不 crash 的狀態」。

對照契約：

1. **Spec 內部用語一致性。** AC-10 證據欄的「error 狀態」與 R-EN-1(5) 的「error」是同一份文件、同一個英文詞；同一詞在同一 Spec 內指同一狀態。(B) 必須把 AC-10 的 error 讀成 R-EN-1(5) 的 empty，與 Spec 自己的用語矛盾。
2. **DR-9 的刻意區分。** DR-9 把 Grading App 定為「警告」、Dashboard 定為「錯誤狀態」，兩者不同強度；若「錯誤狀態」只是「有訊息的任何狀態」，這個區分就沒有意義（E-7）。
3. **Outcome Contract 的命名。** acceptor 接受的契約把這項行為命名為「基本錯誤狀態」（E-5）。(A) 與此一致；(B) 讓契約命名為 error 的條件在頁面上呈現為 empty。
4. **訊息的準確性（AB-10、R-DS-6「明確訊息」）。** 「No forecast data yet」對 incomplete（資料存在但不合格）與 500／502／504（服務故障）都不是事實；對部署缺檔也把故障描述成正常的「尚未有資料」（E-8）。不準確的訊息不是「明確訊息」。
5. **R-EN-1(5) 在兩種讀法下都成立**（三種呈現都存在、各自可見），所以 R-EN-1(5) 本身不決定對應；決定對應的是 AC-10 與 DR-9。(B) 只讓 error 狀態在網路失敗時可達，並未因此違反 R-EN-1(5)，但違反 AC-10。
6. **(A) 的 empty 在正確部署下只能靠模擬到達**（E-8）。這不構成問題：AC-19 明文允許「可用 DevTools 模擬」取得三種狀態截圖，empty 狀態在本產品的角色是防禦性的——保證 payload 意外為空時頁面不留白（R-DS-6 精神），不是描述某個正常的營運階段。

## 4. 裁決（DR-19）：採 (A)

### 4.1 條件 → 狀態的規則（Dashboard；Executor 實作、Reviewer 核對的唯一依據）

**頁面層級**（bootstrap：`/api/health` → `/api/regions`）：

| 條件 | 狀態 |
| --- | --- |
| 請求進行中 | **loading** |
| `fetch` reject（網路失敗）或回應無法解析 | **error** |
| `/api/health` 或 `/api/regions` 回任何非 2xx——包括 503（`reason` 為 missing／empty／incomplete 任一）、500／502／504、404 | **error** |
| `/api/regions` 回 2xx 但 `regions` 缺席或為空陣列 | **empty** |
| `/api/regions` 回 2xx 且至少一個 Region | 顯示 dashboard，接著載入第一個（或深連結指定的）Region |

**Per-Region 層級**（`/api/regions/<r>/series`，以及 #24 之後新增的任何 `/api/` 資料請求）：呈現在對應的 card 內、不取代整頁：

| 條件 | 狀態 |
| --- | --- |
| 請求進行中 | **loading**（inline） |
| 網路失敗，或任何非 2xx（404、503、5xx） | **error**（inline）：訊息指明是失敗（沿用伺服器 `error` 訊息或「無法載入」類文字）；summary 隱藏、表格清空；card 不得留白 |
| 2xx 但 `series`（或對應資料陣列）為空 | **empty**（inline）：訊息指明該 Region 沒有可呈現的資料；summary 隱藏；card 不得留白 |
| 2xx 且有資料 | 正常渲染 |

分類原則一句話：**empty 只用於「請求成功但沒有東西可呈現」；任何請求失敗（非 2xx 或網路失敗）都是 error；快照不可用（503）永遠是 error，不是 empty。**

### 4.2 呈現要求

1. 頁面層級三種狀態 MUST 各自可見且彼此可辨（R-EN-1(5)）：error 呈現 MUST 與 empty、loading 在視覺上不同（`610a797` 既有的紅色、`role="alert"` 的 `#page-error` 已符合，維持即可）。
2. error 呈現 MUST 在伺服器回應帶有 `error` 訊息時把該訊息顯示出來（E-4 的三個訊息），使 missing／empty／incomplete 對使用者仍可區分；沒有訊息時用一般性的失敗文字。這是 AC-10「（原因 empty）」在頁面上可觀察的方式。
3. 文字措辭屬 HOW（DR-1），但受兩條限制：失敗條件 MUST NOT 被描述成正常的「尚未有資料」；empty 條件 MUST NOT 被描述成故障。
4. Per-Region inline 狀態：R-EN-1(5) 的「三種狀態各自可見」在頁面層級判定（R1 的讀法維持）；inline error MUST 以文字可辨識為失敗（`610a797` 的三種 inline 訊息已符合），inline error 與 inline loading 採不同視覺樣式為 SHOULD（R1 F-5(b) 維持 Low、Executor 自行決定）。
5. 頁面層級 error／empty 出現時是否隱藏整個 dashboard、有無重試按鈕，屬 HOW。

### 4.3 對 #23 現況的判定

- Subject `610a797` 把 `/api/health`、`/api/regions` 的 503／5xx／404 呈現為 empty（E-1），在 AC-10 的兩種條件（缺失、空表）與 DR-9 的第三種（不完整）下頁面**沒有**顯示錯誤狀態。AC-10（Dashboard）是 #23 被分配的回歸 AC（derivation record §11.1 #23 列「回歸 AC-02／03／04(b)／10（DS）」），而 `39fbab7` 的行為符合 AC-10（E-3）。**這是契約回歸，#23 的修正 MUST 包含它。**
- 依 R1 F-2 的 disposition（「DA 若判定 AC-10 要求 error 呈現，本項即成為契約回歸，須由 Executor 修正，可在 F-1 的 targeted correction 中一併處理，由 DA 決定」）：**併入 cycle 1 對 F-1 的 targeted correction**，同一 Executor identity、同一 cycle，R2 一併核對。修正屬契約內 rework（治理 §1.2、§3.8），不是新工作。
- 本紀錄確立的是語義：F-2 所描述的行為違反 AC-10／DR-9。Finding 的 severity 與 blocking 標示仍由 Reviewer 在 R2 record 依 §4.3 記錄；但既然它主張契約違反，依 §4.5 disposition 邊界第 1 項不得 deferred，#23 依 §3.8 不得在此未修正的情況下結案。
- 頁面層級的 `regions` 為空 → empty（E-1 末句）已符合 4.1；per-Region 2xx 空序列目前留白（E-2），依 4.1 須改為 inline empty；其餘 per-Region 行為已符合 4.1，不需改動。

### 4.4 R2 對 F-2 的 closure 證據要求

以 Reviewer 自己的環境（R1 §1 的替代 DB 與 CDP 工具或等效方法）核對 subject 修正後的版本：

1. 缺失 DB、只有表無列的 DB、不完整 DB 三種條件：頁面顯示 **error** 狀態（`role="alert"`、error 樣式），內容含伺服器的 `error` 訊息；不是 empty 狀態；無空白頁；`Runtime.exceptionThrown` 0 筆；`/api/health` 回 503。
2. 非 503 的失敗（例如以 `Fetch.fulfillRequest` 回 500 或 502）與封鎖 `/api/*` 的網路失敗：error 狀態。
3. 以 `Fetch.fulfillRequest` 模擬 `/api/regions` 回 2xx `{"regions": []}`：**empty** 狀態出現且與 error、loading 可辨——證明 R-EN-1(5) 的 empty 呈現仍存在；AC-19 的 empty 截圖 MAY 以此方式產生。
4. 以模擬 `/api/regions/<r>/series` 回 2xx `{"series": []}`：chart card 內顯示 inline empty 訊息，不留白。
5. loading 狀態不變（R1 已 PASS）。
6. 截圖：AC-19 的 error 截圖 SHOULD 以缺失或空表 DB 產生，使其同時作為 #23 AC-10（Dashboard）回歸核對的證據；`ac10_dashboard_error_missing_db.png` 的最終重拍仍由 #25 在重驗 AC-10 時進行（derivation record §11.1 #25 列，不變）。
7. `app.js` 檔頭與 `index.html` 的狀態註解（「empty ＝ 503」）須與新對應一致（AC-27 (1) 說明正確性）；作法屬 HOW。

## 5. 是否改變 accepted 語義

**否。** Outcome Contract AB-10 的可觀察條件（明確訊息、不 crash）、其「基本錯誤狀態」命名、AB-15 的三種狀態，全部不變；本紀錄只確定它們合起來已經蘊含的對應。Spec AC-10、R-EN-1(5)、R-DS-6、AC-19 與 DR-9 文字不變、強度不變：三種狀態仍各自存在，error 狀態沒有被刪除或弱化，AC-10 的「錯誤狀態」維持字面意義。屬治理 §5.3 第 2 類，不需 acceptor。

不採 (B) 的理由：它要求把 Spec 同一詞「error」在 AC-10 與 R-EN-1(5) 讀成兩個不同狀態，與 DR-9 的兩層區分和 OC 的命名衝突，並讓故障條件顯示為不準確的「尚未有資料」（§3 第 1–4 點）。

## 6. 受影響的工作、dependencies 與既有 evidence

| 項目 | 影響 |
| --- | --- |
| **#23**（進行中，cycle 1） | Targeted correction 範圍 ＝ F-1 ＋ 本紀錄 §4.3；R2 範圍依 R1 §6 加上 §4.4。worklog `issue-23.md` 決定 4「empty ＝ 503」由本紀錄取代（Executor 更新 worklog 的 Decisions 欄引用 DR-19）。 |
| **#24**（未開始） | `Select Date`／Taiwan Map 新增的 `/api/days`、`/api/days/<date>` 請求適用 §4.1 的 per-Region 層級規則：404（未知日期）、503、5xx、網路失敗 → inline error；2xx 空資料 → inline empty。AC-19 重驗依本紀錄。 |
| **#25**（未開始） | AC-10（Dashboard）重驗與截圖重拍依 §4.1；AC-19 重驗依本紀錄；R-DOC-4 驗收文件引用 DR-19。 |
| **Spec Integration Audit** | AC-10、AC-19、R-DS-6、R-EN-1(5) 的 Spec-level coverage 依本紀錄判定。 |
| **既有 evidence** | #20 的 AC-10 PASS（`issue-20-c1-r1.md`、`ac10_dashboard_error_missing_db.png`）是對 subject `0f5f00e` 的證據，與本紀錄一致，維持有效；它不證明 #23 subject 的行為，#23 subject 由 R2 依 §4.4 另行取證。#23 R1 的 R-EN-1(5) PASS、R-DS-6 PASS 判定所依據的「三種呈現都存在、訊息明確」事實不變，但 AC-10 列的判定依本紀錄改為需修正。 |
| **Grading App** | 不受影響：R-GA-7 與 DR-9 的 Grading App 部分（缺失／為空 → 明確訊息；不完整 → 警告、MAY 仍顯示）不變。 |
| **後端** | 不受影響：R-DS-2、R-DS-3 的 503／404 語義不變（E-4）。 |
| **測試** | 沒有既有測試需要修改（E-10）。Executor MAY 加靜態或 headless 檢查釘住 §4.1，屬 HOW。 |
| **Spec 文字** | 不變。下次一致性修訂 MAY 在 AC-10 證據欄與 R-EN-1(5) 加註「DR-19」。 |

## 7. Authority

- 本裁決在 Design Authority 的 contract-sufficiency／設計語義權限內（治理 §2.1、§2.4、§3.6-A）。不需要 acceptor。
- Reviewer 保有 findings、severity、blocking 與 closure 的判定（§2.1、§4.3）；本紀錄不代 Reviewer 關閉 F-2，也不代 Executor 決定修法。
- Orchestrator 依 §2.4 記錄派工與 binding，並把本紀錄納入 #23 correction 與 R2 的 bounded pack。
