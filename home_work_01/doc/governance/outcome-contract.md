# Outcome Contract — HW10 Taiwan Weather Forecast（`home_work_01/`）

- **狀態**：**ACCEPTED（2026-09-23）。** 接受紀錄見第 8 節；接受的 normative 內容為第 1–7 節於 commit `c45ec61` 的版本，未作任何內容變更。範圍、資料來源（D2）與應用架構（A1–A4）皆已於 2026-09-23 簽核，本檔無 provisional 條款。
- **依據**：Minimal Operational Governance v2.0 §3.1 七項 properties；Project Bindings b1 §2.3。
- **來源紀錄**：本檔由 2026-09-23 的 grill 收斂而成，事實與裁決細節見 [`../brief/BRIEF.md`](../brief/BRIEF.md)；詞彙見 [`../../CONTEXT.md`](../../CONTEXT.md)。
- **Acceptor**：GitHub `yotsubamomo`（Bindings §2.1）。Agent 代寫的接受紀錄不等於取得授權；第 8 節由 acceptor 親自填寫。

## 1. Intent and outcome

交付 HW10「Taiwan Weather Forecast」作業：從 CWA open data 取得資料，推導台灣六大區域一週（七個完整 Forecast Day）的每日最低溫（MinT）與最高溫（MaxT），持久化到 SQLite，並讓使用者選擇地區、查看一週 MinT／MaxT 折線圖與表格。這是**一個產品、兩個呈現層**：老師文件指定的 Streamlit 應用程式 `app.py`（本機以 `streamlit run app.py` 執行，作為評分產物）與**公開部署於 Vercel** 的 dashboard；兩者共用同一份持久化資料與同一套查詢語義。Dashboard 在 MVM 行為之上完成老師描述的 Taiwan Map 與改良的 UI／UX。附自動化測試與 CI，並以 GitHub 交付。

結果須先完整滿足上位契約的評分項目（20／20／20／40），再加上 enhanced 項目；任何 optional／reference 項目都不得成為完成條件。

## 2. Scope and boundaries

### 2.1 上位契約與延伸的邊界

- 上位契約（唯讀）：`doc/requirement/` 內老師提供的文件——Part A 海報（[`REQUIREMENTS.md`](../requirement/REQUIREMENTS.md) Part A）與課程總覽 §1–21。
- **MVM 必須完整滿足上位契約。**
- acceptor 明確授權的 ENHANCED／OPTIONAL 範圍**可以**超出老師撰寫的需求；這類延伸必須維持清楚的 scope class 標示，且不得取代、弱化或被呈現為老師要求的行為。
- 未經 acceptor 授權而新增老師沒有提出的功能，屬 scope 變更，須 acceptor 重新授權（Bindings §2.4）。

### 2.2 Scope classes

| Class | 內容 |
| --- | --- |
| **MVM REQUIRED** | CWA 資料取得（原指定 F-A0010-001；核准的相容性替代 F-D0047-091，2.3 節）；JSON 解析；六個 Region；七個完整 Forecast Day；MinT／MaxT（相容性推導值）；SQLite `data.db` 與 `TemperatureForecasts`（老師 DDL 逐字）；重複執行不重複插入；**本機 Streamlit 評分應用程式 `app.py`**（`streamlit run app.py` 可執行）；**部署於 Vercel 的 dashboard**（Flask 後端＋靜態前端）；兩個呈現層都具備：`Taiwan Weather Forecast`、`Select Region`、六個 Region、七個 Forecast Day、MinT／MaxT 折線圖、`Date`／`MinT`／`MaxT` 表格、只從 SQLite 以 SQL 查詢、不直接呼叫 API、基本錯誤狀態；共用的查詢／領域語義；GitHub 交付；**Vercel 公開 URL** |
| **ENHANCED REQUIRED**（只在部署的 dashboard） | 改良的 UI／UX（framework-agnostic 品質目標，brief §6.4）；響應式 dashboard；`Select Date`；**Leaflet** Taiwan Map，六區依 Derived Map Temperature 著色、可查看地區 Min／Max；dashboard 整合；自動化測試涵蓋兩個呈現層；GitHub Actions CI |
| **OPTIONAL** | 排程更新 CWA 資料；非必要的工程改良 |
| **REFERENCE／FUTURE（non-scope）** | React／Next.js、FastAPI、Windy；課程總覽 §22 以後；老師 repo 的 22 縣市／GIS 架構 |

### 2.3 資料來源條款（**D2 CLOSED**，acceptor 2026-09-23）

| 層次 | 內容 |
| --- | --- |
| 老師指定 | F-A0010-001，六大區域、每日 MinT／MaxT。保留為原始需求。 |
| 已驗證可用性 | 2026-07-01 下架；2026-09-23 以本專案金鑰查詢兩個 endpoint 皆 404（brief §4.2）。 |
| 核准的相容性替代 | F-D0047-091（縣市層級、12 小時期間）。專案內部決定；不因替代資料集是縣市層級而把產品改成 22 縣市。 |
| 老師確認 | 不需要（acceptor 裁定）。老師 repo 為 IMPORTANT CURRENT REFERENCE，不是契約。 |

**推導規則（固定順序，brief §4.6）**：解析 F-D0047-091 → 依 W1 把每個 12 小時期間歸入其 `StartTime` 日期（Forecast Day D ＝ D 06:00–18:00 ＋ D 18:00–D+1 06:00，是專案的相容性視窗，不是曆日）→ 丟棄不完整的起始日期、保留其後七個兩段皆在的日期 → 縣市日 MinT ＝ 期間最小值、MaxT ＝ 期間最大值 → 專案定義的 Region mapping（北部＝基隆市 臺北市 新北市 桃園市 新竹市 新竹縣 苗栗縣；中部＝臺中市 彰化縣 南投縣 雲林縣 嘉義市 嘉義縣；南部＝臺南市 高雄市 屏東縣；東北部＝宜蘭縣；東部＝花蓮縣；東南部＝臺東縣；澎湖縣 金門縣 連江縣 排除）→ Region MinT／MaxT ＝ 成員縣市的算術平均，四捨五入到小數一位 → 寫入六區 × 七天的快照。

**驗證要求**：恰好 7 個完整 Forecast Day（逐日檢查，不是取前七個標籤）；恰好 6 個 Region；每個 Region／Day 都有 MinT 與 MaxT；產生 Region 值前其全部成員縣市都存在；縣市缺漏須明確報錯，不得默默改變分母。

**標示要求**：區域值是 PROJECT-DERIVED COMPATIBILITY VALUES，不得寫成 CWA 發布的六區預報；對應表是專案相容性對應，不得寫成 CWA 權威分區。

### 2.4 應用架構（**CLOSED**，acceptor 2026-09-23，A1–A4）

- **一個產品、兩個呈現層。** 共用層：ingestion／推導 → `data.db` → 共用的查詢／領域模組；其上分別是本機 Streamlit 評分應用程式與部署的 Flask API＋靜態 HTML／JS dashboard。SQL／查詢語義與預報業務邏輯**不得**在兩個呈現層各寫一份；本機 Streamlit 應用程式必須使用與部署版相同的持久化資料與共用查詢邏輯。
- **行為對等。** 兩個呈現層都必須滿足 2.2 節列出的全部 MVM 行為；部署的 dashboard 另加 ENHANCED 項目，可以比本機評分應用程式更豐富，但 MVM 功能不得更弱。
- **Streamlit 的定位。** Streamlit 仍是必要的評分產物：`home_work_01/app.py` 是真正的 Streamlit 應用程式，老師文件的 `streamlit run app.py` 指令維持有效。Streamlit 不再是正式部署 runtime，**這是 Vercel 必要部署限制造成的相容性安排，不是「Streamlit 從未屬於作業」的主張**（Vercel 無法執行 Streamlit 伺服器，brief §5）。
- **部署。** Vercel 為必要目標；部署的 Python 應用程式使用 Flask，採與老師已驗證模式一致、且符合目前 Vercel 支援的最小結構。
- **地圖。** ENHANCED Taiwan Map 在瀏覽器以 Leaflet 繪製；本機 Streamlit MVM 不需地圖；Folium／streamlit-folium 不再是必要依賴（原 S4 因架構而被取代）。
- **Python 3.12**，本機、CI、Vercel 一致（取代原 3.11 裁決；Vercel 不提供 3.11）。
- API 路徑、JS 函式庫、路由設定、模組切分與確切檔案結構屬 Design Authority 的 Spec 決定，除非是可觀察驗收條件的一部分（老師指定的 `app.py` 與 `streamlit run app.py` 是）。

### 2.5 其他 constraints

- 已裁決的實作前提（brief §6）：Forecast Snapshot 語義、MVM 用準備好的快照、應用檔案相對於原始碼位置解析且 `data.db` 唯讀開啟、憑證只在未追蹤的 `.env`、部署設定留在 `home_work_01/`。
- 不得把 optional／reference 項目當成必要；不得因老師 repo 而默默取代上位契約。
- Reserved boundaries RB-1～RB-6（Bindings §2.6）維持保留。

## 3. Acceptance boundary

每條為可觀察的 PASS／FAIL 與證據要求；具體 AC 由 Design Authority 在此邊界內 derive，Spec 全體合起來須涵蓋本節全部。「兩個呈現層」指本機 Streamlit 評分應用程式與部署的 dashboard。

| ID | Class | 可觀察條件 | 證據 |
| --- | --- | --- | --- |
| AB-1 | MVM | **Vercel** 公開 URL：`GET <url>` 成功回應應用頁面；Flask 健康 endpoint（路徑由 Spec 決定，例如 `GET /api/health`）成功回應；允許最多 90 秒暖機重試 | smoke test 輸出，記入 acceptance 文件 |
| AB-2 | MVM | `streamlit run app.py` 在本機依 README 步驟可啟動 `home_work_01/app.py` | worklog 紀錄＋截圖 |
| AB-3 | MVM | 兩個呈現層都可見 `Taiwan Weather Forecast` 與 `Select Region`；選項恰為六個 Region 的中文名 | Streamlit `AppTest`；Flask test client＋UI 檢查；截圖 |
| AB-4 | MVM | 兩個呈現層在選擇一個 Region 後都顯示該區七個 Forecast Day 的 MaxT／MinT 折線圖與 `Date`／`MinT`／`MaxT` 表格（7 列） | 同上 |
| AB-5 | MVM | 兩個呈現層都只從 `data.db` 以 SQL 取得資料，經同一個共用查詢模組；應用程式不呼叫 CWA API | 靜態檢查（app／server 程式無 requests／httpx／CWA URL）＋審查（查詢語義只有一份） |
| AB-6 | MVM | `data.db` 內有 `TemperatureForecasts(id INTEGER PRIMARY KEY, regionName TEXT, dataDate TEXT, mint REAL, maxt REAL)`；`SELECT DISTINCT regionName` 回六區；`WHERE regionName = '中部地區'` 回該區 7 列 | pytest |
| AB-7 | MVM | 連續執行 ingestion 兩次，`TemperatureForecasts` 恰為 42 列、無重複 (regionName, dataDate) | pytest |
| AB-8 | MVM | Ingestion 以使用者自己的 CWA 金鑰從 F-D0047-091 取得 JSON；金鑰不在 git、log、前端程式或文件 | `git ls-files` 不含 `.env`；diff 無金鑰字串；審查 |
| AB-9 | MVM | 推導驗證：7 個完整 Forecast Day、6 個 Region、每格有 MinT 與 MaxT、成員縣市齊全；缺漏時明確報錯 | pytest（含缺縣市的失敗案例） |
| AB-10 | MVM | 基本錯誤狀態：兩個呈現層在 `data.db` 缺失或為空時顯示明確訊息而非 crash；ingestion 對 API 失敗有明確錯誤 | `AppTest`＋Flask test client＋pytest |
| AB-11 | MVM | README 的安裝、資料處理、本機執行與部署步驟實際跑過並成功 | worklog 紀錄 |
| AB-12 | MVM | 專案在 GitHub `yotsubamomo/aiot-classwork` 的 `home_work_01/` 交付 | repo 狀態 |
| AB-13 | MVM | 技術文件把區域值標示為專案推導的相容性值、把對應表標示為專案定義；F-A0010-001 記為原指定、其下架記為外部限制；Streamlit 的定位依 2.4 節記述 | 文件審查 |
| AB-14 | ENHANCED | 部署的 dashboard：Leaflet Taiwan Map 有六個 Region 標記、依 Derived Map Temperature 的四段色帶著色、`Select Date` 切換 Forecast Day、可查看該區 Min／Max | 手動驗收清單＋截圖（瀏覽器測試只在此類 ENHANCED 條件需要時採用） |
| AB-15 | ENHANCED | 部署的 dashboard 的 UI／UX 品質清單全部 PASS：清楚的視覺層級、響應式、摘要資訊、可互動易讀的圖表、loading／empty／error 狀態、375 px 寬無不必要橫向捲動 | 手動驗收清單＋截圖 |
| AB-16 | ENHANCED | GitHub Actions 在 push 時執行測試並通過；涵蓋 ingestion／D2 推導／SQLite／共用查詢層（pytest）、本機評分應用程式（`AppTest`）、部署 API 行為（Flask test client） | CI 執行紀錄 |
| AB-17 | ENHANCED | 部署 smoke test 可由 `workflow_dispatch` 執行，檢查公開根路徑與健康 endpoint | workflow 執行紀錄 |

## 4. Authority and authorization

- **接受與授權**：acceptor `yotsubamomo`。接受本契約即授權具相應 authority 的 Agents 在本邊界內規劃、分解（Spec／Tickets）、實作、審查、修正至完成。
- **Reserved**（Bindings §2.6）：RB-1 合併進 `main`；RB-2 繳交；RB-3 憑證申請／填寫；RB-4 付費；RB-5 修改單元目錄外的檔案；RB-6 破壞性 git 操作。
- **Standing**（Bindings §2.5）：SA-1 topic branch commit 與 push；SA-2 開 PR。
- **本次 grill 中 acceptor 已給的特定授權**：root `CONTEXT-MAP.md` 指向 `home_work_01/CONTEXT.md` 的一列（已 ratify）；以本專案金鑰對 `opendata.cwa.gov.tw` 做唯讀驗證 GET（已執行三次，用途結束）。原 R1 對 root `.streamlit/config.toml` 的授權隨 R1 撤回而失效。
- **不需外部確認**：資料來源替代為專案內部決定。

## 5. Relevant context

- **既有產物**：`CONTEXT.md`、`doc/requirement/`（上位契約與轉寫）、`doc/brief/BRIEF.md`、`.env`（未追蹤，acceptor 的 CWA 金鑰）、`.env.example`、`doc/governance/worklog/`。
- **外部事實**：F-A0010-001 下架（brief §4.2）；老師 repo `huanchen1107/AIoT_L3_CWA_HW1`——2026-09-23 發現、與海報實質不同、屬 IMPORTANT CURRENT REFERENCE（老師的建議／參考實作），不取代也不修改上位契約，此分類沒有待老師確認的事項；其 Flask＋靜態＋Vercel 模式已直接讀取（brief §4.4、§5.2）；F-D0047-091 實際結構（brief §4.5）與樣本驗算（§4.6）；Vercel 平台事實（brief §5.3，提交前再驗證）。
- **已知風險**：替代資料集也可能再下架；Vercel Hobby 是否需信用卡未驗證；SQLite 唯讀讀取在 Vercel 未見官方文件、以老師 repo 的成功部署為證據；40% 項目的部署形態與海報不同（由 2.4 節的相容性安排承擔）；兩個呈現層的行為對等須靠共用模組與測試維持。

## 6. Assurance path

- **Lane**：**Formal**（Bindings §4：作業主體）。Spec＋Tickets 由 Design Authority derive 並附 derivation record；Orchestrator run-to-completion。
- **Audit**：每張 Ticket 的 independent audit、每份 Spec 的 Spec Integration Audit（不採單 Ticket fast path）；Design Authority phase acceptance。
- **高風險類別**（待 DA 以 decision record 確認）：H-1 憑證與機密；H-2 老師指定的檔名、資料表結構與輸出格式（含 `app.py`、`data.db`、`TemperatureForecasts`）。
- **Release gate**：合併進 `main` 由 acceptor 執行（RB-1），前提見 Bindings §5。
- **前置**（Bindings §8.2）：bindings PR 合併、載入 `gov-*` definitions 的 session、binding dry-run、DA 確認高風險類別。

## 7. Stable reference

- 本檔：`home_work_01/doc/governance/outcome-contract.md`，接受時的 commit SHA 記於第 8 節。
- 上位契約：`home_work_01/doc/requirement/`（同一 commit）。
- 盤點：`home_work_01/doc/brief/BRIEF.md`（同一 commit）。

## 8. 接受紀錄

| 欄位 | 內容 |
| --- | --- |
| 狀態 | **已接受**（2026-09-23） |
| Acceptor | GitHub `yotsubamomo`（Bindings §2.1），於 Claude Code 對話中以下列原文接受 |
| Acceptor 原始指示（引用原文） | 見第 8.2 節（逐字） |
| 日期 | 2026-09-23 |
| 接受的檔案 commit SHA | normative 內容（第 1–7 節）：`c45ec61`（`main`，2026-09-23 合併 PR #16）。本接受紀錄寫入後的 commit：待 commit 時填入 |
| 隨接受生效的 derived contract | `home_work_01/doc/spec/SPEC.md` v1.1（derivation record：`doc/governance/decisions/derivation-SPEC.md`） |
| 前置證據 | Bindings §8.2 #4 binding dry-run PASS：`docs/governance/binding-verification.md`（2026-09-23） |

### 8.2 Acceptor 接受原文（2026-09-23，逐字）

> 我接受 `home_work_01` 的 Outcome Contract。
>
> 接受範圍為目前 `c45ec61` 中第 1–7 節的 normative content，不做任何內容變更。
>
> 同時確認：
>
> 1. `home_work_01/doc/spec/SPEC.md` v1.1 為此 Outcome Contract 的有效 derived contract，隨本次接受生效；本次 acceptance record / metadata 的寫入不構成 normative content change，不需要重新 derive。
>
> 2. 我授權本單元所需的 RB-5 GitHub Actions 例外：
>    - 可以在 repo root `.github/workflows/` 建立與維護只服務 `home_work_01` 的 workflow；
>    - workflow 必須以 path filter 限定 `home_work_01/**` 以及該 workflow 檔案本身；
>    - 此授權不延伸到其他 root 檔案、其他單元或其他用途的 workflow。
>
> 3. 其餘 reserved actions 維持原 governance 規則，不因本次接受而擴張。
>
> 請將以上原文寫入 Outcome Contract §8 acceptance record。

寫入者：主 session（agent），依 acceptor 的明確指示逐字轉錄；接受與授權的效力來自上述 acceptor 原文，不來自本轉錄。

### 8.1 Grill 裁決紀錄（2026-09-23，acceptor 於對話中的原文摘錄，供接受時引用）

| 項目 | 裁決（原文摘錄） |
| --- | --- |
| Q2 地圖 | 「Q2 B」；「Classify the Taiwan map as ENHANCED REQUIRED, not MVM REQUIRED.」 |
| Q3 資料新鮮度 | 「Q3 A for MVM. Scheduled refresh remains OPTIONAL for now, not ENHANCED REQUIRED.」 |
| Q4 表語義 | 「Q4 A」；「Treat TemperatureForecasts as the current one-week forecast snapshot, not historical forecast storage.」 |
| Q5 主機 | 「Prefer free-tier hosting without requiring a credit card. Cold start is acceptable; deployment smoke tests may retry for up to 90 seconds.」 |
| Q6 UI | 「Improved UI/UX is ENHANCED REQUIRED.」 |
| Q7 測試 | 「Q7 A. Automated tests are ENHANCED REQUIRED and should run in GitHub Actions on every push.」 |
| S1／S3 架構（原） | 「S1: Option 1」「Streamlit is the graded application architecture.」— 後依 Vercel 必要而重開，結果見 A1 |
| S2 SQLite | 「S2: Confirm」；「SQLite remains mandatory as specified.」 |
| S4 地圖技術（被取代） | 「S4: A … Folium」→「deployed Taiwan Map → Leaflet; local Streamlit MVM → no map required; Folium / streamlit-folium → no longer required dependencies」 |
| S5 Part B | 「S5: Adopt as listed」；「React / FastAPI / Windy remain REFERENCE / FUTURE and must not expand the current implementation scope.」 |
| D1 驗證 | 「D1: A」；「Treat F-A0010-001 as unavailable based on the completed verification.」 |
| R1 主機（撤回） | 「R1: A — Streamlit Community Cloud…」→「Vercel is REQUIRED for the final public deployment. Therefore withdraw the previous R1 ruling」 |
| R2 repo | 「R2: Monorepo.」 |
| R3 smoke | 「R3: A.」→「Withdraw any Streamlit-Community-Cloud-specific acceptance check such as /_stcore/health」 |
| R4 清理 | 「R4: Delete and move as proposed.」 |
| R5 地圖溫度 | 「R5: Adopt … derived_map_temperature = (MinT + MaxT) / 2 … must explicitly state that this value is DERIVED」 |
| Python | 「Python 3.11…」→「Replace the earlier Python 3.11 ruling with: Python 3.12 consistently across local development, CI, and Vercel.」 |
| D0 上位契約 | 「D0 … CLOSED = A.」「The teacher repository remains IMPORTANT CURRENT REFERENCE only.」 |
| D2 資料來源 | 「We do NOT need teacher confirmation for D2. The compatibility decision is ours to make for this project.」 |
| D2-1 視窗 | 「W1 — assign each 12-hour period to its StartTime date.」「a Forecast Day labelled D is not a strict calendar-day 00:00–24:00 meteorological interval.」「retain the next seven dates that each contain both expected 12-hour periods.」 |
| D2-2 對應 | 「Mapping A.」「Treat this mapping as a PROJECT-DEFINED compatibility mapping.」 |
| D2-3 聚合 | 「arithmetic mean, rounded to one decimal.」「These regional values are PROJECT-DERIVED COMPATIBILITY VALUES.」 |
| Vercel | 「Vercel is now a MUST deployment target」 |
| A1 架構 | 「A1: V3.」「Treat V3 as ONE product with two presentation adapters, not two independently designed applications.」「Do not duplicate SQL/query semantics or forecast business logic between Streamlit and Flask.」 |
| A2 Python | 「A2: (a) Python 3.12 everywhere.」 |
| A3 地圖 | 「A3: Leaflet for the deployed Taiwan Map; the local Streamlit app contains the complete MVM chart/table workflow but does not need the ENHANCED map.」 |
| A4 框架 | 「A4: Flask.」 |
| Streamlit 定位 | 「Streamlit remains a required grading artefact. Keep home_work_01/app.py … Record this as a compatibility accommodation caused by the mandatory Vercel deployment constraint, not as a claim that Streamlit was never part of the assignment.」 |
| G1 治理 | 「G1: A. Treat governance as the target operating model for home_work_01.」「Do not write the final spec in this session.」 |
| RB-5 | 「RB-5: Ratify. Keep the root CONTEXT-MAP.md row pointing to home_work_01/CONTEXT.md.」 |
| §2.1 邊界 | 「MVM must fully satisfy the upper contract. Enhanced/Optional scope explicitly authorized by the acceptor may extend beyond the teacher-authored requirements.」 |
