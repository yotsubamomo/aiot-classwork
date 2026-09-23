# Spec: HW10 Taiwan Weather Forecast（`home_work_01/`）

- **專案識別**：`home_work_01`（老師稱 HW10／Part 5）
- **Spec 版本**：**v1.1**（2026-09-23，Design Authority derive；v1.1 為同日的一致性修正，見第 10 節版本紀錄）
- **Derived 自**：Outcome Contract 草稿 [`../governance/outcome-contract.md`](../governance/outcome-contract.md)（commit `c45ec61`，`main`）；盤點 [`../brief/BRIEF.md`](../brief/BRIEF.md)（同一 commit）；詞彙 [`../../CONTEXT.md`](../../CONTEXT.md)
- **上位契約**（唯讀）：[`../requirement/REQUIREMENTS.md`](../requirement/REQUIREMENTS.md) Part A；[`../requirement/Taiwan_Weather_Forecast_course_overview.md`](../requirement/Taiwan_Weather_Forecast_course_overview.md) §1–21
- **Derivation record**：[`../governance/decisions/derivation-SPEC.md`](../governance/decisions/derivation-SPEC.md)
- **相關裁決**：[`../governance/decisions/decision-20260923-high-risk-categories.md`](../governance/decisions/decision-20260923-high-risk-categories.md)、[`../governance/decisions/decision-20260923-spec-interpretation-rulings.md`](../governance/decisions/decision-20260923-spec-interpretation-rulings.md)
- **Issue tracker**：Tickets #18–#25 已於 2026-09-24 derive（GitHub Issues，`yotsubamomo/aiot-classwork`）；索引 [`../ticket/tickets.md`](../ticket/tickets.md)；分配與 boundary determination 見 derivation record 第 11 節

## 0. 狀態與效力

| 項目 | 內容 |
| --- | --- |
| 狀態 | **EFFECTIVE（自 2026-09-23）。** Outcome Contract 第 8 節於 2026-09-23 由 acceptor 接受（normative 第 1–7 節與 `c45ec61` 相同；acceptor 原文確認本 Spec v1.1 隨接受生效，並給出限定範圍的 RB-5 GitHub Actions 授權）。本 Spec 原 derive 自 `c45ec61` 的草稿，邊界由已完成的 grill 收斂、裁決而成。**Tickets**：GitHub Issues #18–#25（2026-09-24 derive；索引 [`../ticket/tickets.md`](../ticket/tickets.md)；分配見 derivation record 第 11 節）。 |
| 生效條件 | acceptor 於 Outcome Contract 第 8 節填寫接受紀錄時，本 Spec 自動成為有效的 derived contract，不需另行核准（治理 §1.2），前提是接受時 Outcome Contract 的 **normative 內容**（第 1–7 節：intent、scope 與 scope classes、資料來源與架構條款、其他 constraints、acceptance boundary、authority／authorization、context、assurance path）與 `c45ec61` **實質相同**。填寫第 8 節接受紀錄與接受 metadata（原文、日期、commit SHA），以及隨接受一併給出、本 Spec 已列為前置條件的授權（第 9 節，例如 RB-5 workflow 授權），**本身不是內容變更，不觸發重新 derive**；不改變語義的文字校正亦同。 |
| 重新 derive 條件 | 接受前或接受時，Outcome Contract 的 normative 內容若有任何 scope、requirement、架構、acceptance boundary，或 authority／authorization 條款本身（reserved boundaries、standing authorizations、授權涵蓋範圍）的變更，本 Spec 須由 Design Authority 重新 derive（或以 derivation record 修訂確認未受影響）並更新 derivation record；在此之前不得依本 Spec 開 Ticket 或啟動 run。是否「實質相同」由 Design Authority 以 derivation record 確認（治理 §1.2 boundary determination、§5.3）。 |
| 前置（Bindings §8.2） | binding dry-run（#4）與本 Spec 附帶的高風險類別 decision record（#5）完成後，才可 Formal activation。 |
| 需要 acceptor 的動作 | 見第 9 節「前置條件（acceptor 動作）」；其中 GitHub Actions workflow 檔案位於單元目錄外，屬 RB-5，須 acceptor 明確授權。 |

**標記約定**

- 來源類型：**T** 老師要求（上位契約條款）｜**C** 專案相容性決定（acceptor 於 grill 裁決，Outcome Contract §2.3／§2.4）｜**P** 專案前提或治理約束（Outcome Contract §2.5、§4；Bindings）｜**E** ENHANCED REQUIRED（Outcome Contract §2.2）。
- Scope class：**MVM**、**ENHANCED**。OPTIONAL 與 REFERENCE 只出現在第 8 節 Out of Scope。
- MUST／SHOULD／MAY 依治理用語。SHOULD 偏離須在 worklog 記理由。
- `AB-n` 指 Outcome Contract 第 3 節 acceptance boundary；`A1-1`…`A9-5` 指 REQUIREMENTS.md Part A 編號；`§n` 單獨出現時指課程總覽章節。

## Problem Statement

老師的 HW10 要求一條完整的資料流：從 CWA Open Data 取得台灣六大區域一週預報的 JSON，提取每日 MinT／MaxT，存進 SQLite `data.db` 的 `TemperatureForecasts`，再用 Streamlit 做一個「選地區、看一週折線圖與表格」的 Web App；台灣地圖是加分。評分 20／20／20／40，全部依這些可見產物打分。

目前 `home_work_01/` 只有文件與詞彙，沒有任何實作。而且有三個事實讓「照海報做」不可能直接成立：

1. 老師指定的資料集 F-A0010-001 已於 2026-07-01 下架，帶金鑰查詢回 404。目前沒有任何仍上架的 CWA 產品直接提供六大區域的每日 MinT／MaxT。
2. acceptor 要求最終產物**必須**公開部署在 Vercel，而 Vercel 無法執行 Streamlit 伺服器。
3. 治理要求老師沒寫的功能必須明確標示 scope class，不得冒充老師要求。

Grill 已收斂出的解法（Outcome Contract）是：用縣市層級的 F-D0047-091 依專案定義的相容性規則推導六區 × 七天的 MinT／MaxT；產品維持老師的六區／七天／MinT–MaxT 語義；一個產品、兩個呈現層——本機 Streamlit 評分應用程式 `app.py` 與部署於 Vercel 的 Flask＋靜態 dashboard——共用同一份 `data.db` 與同一套查詢語義；dashboard 之上再加 ENHANCED 的 UI／UX、`Select Date` 與 Leaflet Taiwan Map；附自動化測試與 GitHub Actions CI。

本 Spec 把這個由已完成的 grill 裁決、記於 Outcome Contract 草稿（待接受）的邊界寫成可以直接開 Ticket 實作、可以逐條驗收的契約。

## Solution

**資料流（固定）**

```text
CWA F-D0047-091（縣市、12 小時期間，JSON）
  → fetch：以使用者自己的金鑰取得，保存原始 JSON 供觀察
  → derive：W1 分組成 Forecast Day → 縣市日 MinT／MaxT → 專案定義的 Region 平均 → 恰好 6 × 7
  → persist：data.db / TemperatureForecasts（老師 DDL 逐字），整份快照原子替換
  → 共用查詢／領域模組（唯一的 SQL 與預報業務邏輯）
      ├─ Grading App：home_work_01/app.py（Streamlit，本機，streamlit run app.py）
      └─ Dashboard：Flask JSON API ＋ 靜態 HTML／CSS／JS（Vercel 公開 URL）
             └─ ENHANCED：改良 UI／UX、響應式、Select Date、Leaflet Taiwan Map
```

**核心設計**

- **一個產品、兩個呈現層。** 共用模組是唯一讀 `data.db` 的地方；`app.py` 與 Flask 都只呼叫它。兩個呈現層對每一項 MVM 行為輸出相同的資料；dashboard 可以更豐富，但 MVM 不得更弱。
- **快照語義。** `TemperatureForecasts` 永遠只裝「目前這一週」的 Forecast Snapshot：恰好六個 Region × 七個完整 Forecast Day ＝ 42 列。重跑 ingestion 是整份替換，不是追加。
- **相容性推導是專案的，不是 CWA 的。** 區域值標示為 PROJECT-DERIVED COMPATIBILITY VALUES；Region 對應表標示為專案定義；F-A0010-001 記為原指定、下架記為外部限制。
- **老師指定的名字一個都不改。** `app.py`、`data.db`、`TemperatureForecasts` 與其五個欄位、六個 Region 的中文名、`streamlit run app.py`、頁面文字 `Taiwan Weather Forecast`／`Select Region`／`Select Date`／`Date`／`MinT`／`MaxT`。
- **金鑰只存在於 ingestion 的執行環境。** 兩個呈現層與共用模組沒有 HTTP client、沒有 CWA URL、沒有金鑰；部署的 dashboard 不需要任何 secret。
- **Python 3.12** 本機、CI、Vercel 一致。

**分工**

| 層 | 技術（契約固定） | 交付形態 |
| --- | --- | --- |
| Ingestion | Python 3.12、`requests`、`sqlite3` | 可從單元目錄以文件化指令執行；可離線從已保存的 JSON 重跑 derive→persist |
| 共用模組 | Python，純 `sqlite3` 讀取 | 兩個呈現層的唯一資料來源 |
| Grading App | Streamlit | `home_work_01/app.py` |
| Dashboard 後端 | Flask（單一 Python function，同時提供 API 與靜態檔） | Vercel Root Directory ＝ `home_work_01` |
| Dashboard 前端 | 靜態 HTML／CSS／JS，無 build step；Leaflet 地圖 | 由 Flask／Vercel 提供 |
| 測試與 CI | pytest、Streamlit `AppTest`、Flask test client；GitHub Actions | push 觸發測試；`workflow_dispatch` 觸發部署 smoke test |

## User Stories

### 評分與交付

1. As a 授課老師, I want 在 `home_work_01/` 執行 `streamlit run app.py` 就能打開一個 Streamlit 應用程式, so that 我能依海報的 40% 項目直接評分。
2. As a 授課老師, I want 打開 `data.db` 執行海報上的兩句驗證 SQL 就看到六個地區與中部地區的七列, so that 我能確認 20% 的 SQLite 項目。
3. As a 授課老師, I want 看到原始 JSON 的觀察輸出與提取後的資料預覽, so that 我能評「觀察 JSON」與「觀察資料」兩個細項。
4. As a 授課老師, I want 程式結構清楚、有錯誤處理、有註解、重複執行不重複插入, so that 四個「程式品質」細項有依據。
5. As a 授課老師, I want 專案在 GitHub 上、README 說明它與海報 `HW10_Weather/` 結構的對應, so that 我找得到每個評分項目對應的檔案。
6. As a 授課老師, I want README 誠實說明 F-A0010-001 已下架、專案改用 F-D0047-091 推導六區值, so that 我知道資料為何與海報範例不同，且不會誤以為那是 CWA 發布的六區預報。
7. As a 作業擁有者（acceptor）, I want 一個公開的 Vercel URL, so that 任何人不用安裝就能看到成品。
8. As a 作業擁有者, I want 我的 CWA 金鑰永遠不進 git、log、前端或文件, so that 公開 repo 與公開部署不洩漏憑證。

### 使用者（Grading App 與 Dashboard 共同）

9. As a 使用者, I want 頁面標題是 `Taiwan Weather Forecast`, so that 我一眼知道這是什麼。
10. As a 使用者, I want 用 `Select Region` 下拉選單在六個地區之間切換, so that 我看到自己關心的區域。
11. As a 使用者, I want 選了地區後看到一週七天的 MaxT 與 MinT 折線圖, so that 我掌握溫度趨勢。
12. As a 使用者, I want 折線圖下方有 `Date`／`MinT`／`MaxT` 的七列表格, so that 我能讀到精確數字。
13. As a 使用者, I want 看到這份預報是什麼時候更新的, so that 我知道資料有多新。
14. As a 使用者, I want 資料檔缺失或為空時看到明確訊息而不是錯誤堆疊或空白頁, so that 我知道是資料問題而不是我的操作問題。

### Dashboard 使用者（ENHANCED）

15. As a Dashboard 訪客, I want 頁面有清楚的視覺層級、摘要資訊與可互動的圖表, so that 不用讀說明就能操作。
16. As a Dashboard 訪客, I want 用 `Select Date` 選一個 Forecast Day, so that 地圖顯示那一天的狀況。
17. As a Dashboard 訪客, I want 在台灣地圖上看到六個地區的標記依平均溫度著色, so that 我一眼比較各區冷熱。
18. As a Dashboard 訪客, I want 點地區標記看到該區當日的 Min／Max, so that 我不必回到下拉選單查。
19. As a Dashboard 訪客, I want 地圖圖例說明四段顏色、並說明「平均溫度」是由 MinT／MaxT 導出的, so that 我不會把它當成觀測日均溫。
20. As a 手機使用者, I want 在 375 px 寬度下頁面可用且不需橫向捲動, so that 我在手機上也能看。
21. As a Dashboard 訪客, I want 載入中、無資料、錯誤三種狀態各自有明確呈現, so that 我知道現在發生什麼事。

### 維護者

22. As a 維護者, I want SQL 與預報業務邏輯只有一份, so that 改一處兩個呈現層同時正確。
23. As a 維護者, I want 推導規則有以真實 F-D0047-091 樣本為 fixture 的自動化測試（含缺縣市、缺半天、無法解析的失敗案例）, so that 重構時不會默默改變分母或日界。
24. As a 維護者, I want 不用網路、不用金鑰就能跑完整測試, so that CI 與本機測試穩定。
25. As a 維護者, I want 每次 push 都在 GitHub Actions 跑測試, so that 壞掉立刻知道。
26. As a 維護者, I want 部署後能手動觸發 smoke test 檢查公開 URL 與健康 endpoint, so that 我確認部署真的活著。
27. As a 維護者, I want 重跑 ingestion 就能得到新的一週快照, so that 資料更新不需要手動清資料庫。
28. As a 維護者, I want F-D0047-091 也下架時 ingestion 明確報錯而已部署的快照仍可服務, so that 外部變動不會讓成品變成空白。

## 1. Requirements（R）

每條需求標示 ID、來源類型、class、對應的 acceptance boundary（AB）或契約條款。

### 1.1 Ingestion — 取得資料

| ID | 類型 | Class | 需求 | 對應 |
| --- | --- | --- | --- | --- |
| R-ING-1 | T／C | MVM | Ingestion MUST 以 `requests` 對 CWA Open Data REST datastore 取得 **F-D0047-091** 的 JSON 回應（`format=JSON`），授權使用**使用者自己的** CWA 金鑰。F-A0010-001 記為原指定（見 R-DOC-2），不再嘗試取得。 | A1-1、A1-2、A1-5、A9-1；OC §2.3；AB-8 |
| R-ING-2 | P | MVM | 金鑰 MUST 只從單元目錄內**未追蹤**的 `.env` 讀取（變數 `CWA_API_KEY`，與既有 `.env.example` 一致）；缺金鑰時 MUST 以明確訊息失敗，且訊息不含金鑰值。 | OC §2.5、§4 RB-3；AB-8 |
| R-ING-3 | T | MVM | 請求 MUST 設定逾時；MUST 確認取得成功（HTTP 200 且回應 `success` 為 `"true"`、`result.resource_id` 為 `F-D0047-091`），否則以明確錯誤（含 HTTP 狀態與 CWA 訊息）結束並回傳非零結束碼。 | A1-7；AB-10 |
| R-ING-4 | T | MVM | 取得成功後 MUST 以 `json.dumps(..., indent=2, ensure_ascii=False)` 等價方式把原始 JSON **完整**寫到單元目錄內一個文件化的位置（供「觀察 JSON」評分），並在終端輸出摘要（縣市數、要素名、期間數）。 | A1-6；OC §2.1；AB-11、AB-13 |
| R-ING-5 | C | MVM | Ingestion 的 derive→persist 階段 MUST 可以不經網路、直接從一個已保存的原始 JSON 檔執行（測試、CI 與離線重建用）；機制（CLI 參數、函式介面）屬 HOW。 | AB-7、AB-9、AB-16 |
| R-ING-6 | T | MVM | Ingestion SHOULD 讓海報建議的三個階段（fetch、parse、database）在程式結構上可辨識——可用海報建議的檔名，或清楚命名的模組——並由 README 對應到海報的 `HW10_Weather/` 結構。 | A6、A7；brief §6.9 |

### 1.2 Derivation — 相容性推導

| ID | 類型 | Class | 需求 | 對應 |
| --- | --- | --- | --- | --- |
| R-DER-1 | C | MVM | 解析結構 MUST 依 brief §4.5：`records.Locations[0].Location[]`（22 個縣市，`LocationName`）→ `WeatherElement[]` 取 `ElementName` 為 `最高溫度` 與 `最低溫度` 者 → `Time[]` 的 `StartTime`／`EndTime`（ISO 8601，+08:00）與 `ElementValue[0].MaxTemperature`／`.MinTemperature`（字串）。 | OC §2.3；AB-9 |
| R-DER-2 | C | MVM | **W1 分組**：每個 12 小時期間歸入其 `StartTime` 的台灣本地日期 D。Forecast Day D ＝ D 06:00–18:00 ＋ D 18:00–D+1 06:00；兩段都存在才算**完整**。這是專案相容性視窗，不是曆日。 | OC §2.3；AB-9 |
| R-DER-3 | C | MVM | **保留規則**：依日期升序，若第一個日期不完整則丟棄它；接著取七個日期，這七個 MUST 為**連續**的曆日且每一個都完整；不足七個、不連續或其中任一不完整時 MUST 以明確錯誤結束。其後多餘的期間忽略。 | OC §2.3；AB-9 |
| R-DER-4 | C | MVM | 縣市日值：縣市日 MinT ＝ 該 Forecast Day 兩段 `MinTemperature` 的最小值；縣市日 MaxT ＝ 兩段 `MaxTemperature` 的最大值。值 MUST 能解析為數字；缺值或落在可設定的無效值集合（例如空字串、`-`、`X`、`-99`）者視為缺漏，該縣市日**不完整**，觸發 R-DER-7 的錯誤，不得跳過。 | OC §2.3；brief §6.7；AB-9 |
| R-DER-5 | C | MVM | **Region 對應（專案定義）**：北部地區＝基隆市、臺北市、新北市、桃園市、新竹市、新竹縣、苗栗縣；中部地區＝臺中市、彰化縣、南投縣、雲林縣、嘉義市、嘉義縣；南部地區＝臺南市、高雄市、屏東縣；東北部地區＝宜蘭縣；東部地區＝花蓮縣；東南部地區＝臺東縣。澎湖縣、金門縣、連江縣不屬任何 Region。縣市名以資料的 `LocationName` 逐字比對（「臺」不是「台」）。 | OC §2.3；AB-9 |
| R-DER-6 | C | MVM | Region 日值 ＝ 全部成員縣市該日值的**算術平均**，**四捨五入（half-up）到小數一位**。產生任一 Region 日值前，其全部成員縣市該日 MUST 都存在；任一缺漏 MUST 以指名縣市與日期的錯誤結束，**不得改變分母**。 | OC §2.3；AB-9 |
| R-DER-7 | C | MVM | 推導輸出 MUST 恰為 6 個 Region × 7 個 Forecast Day ＝ 42 筆，每筆有 MinT 與 MaxT；任一驗證失敗（R-DER-3、R-DER-4、R-DER-6）時 MUST 不寫入資料庫（既有快照保持不變），並回傳非零結束碼。 | OC §2.3；AB-9、AB-7 |
| R-DER-8 | T | MVM | Derive 階段 MUST 在終端輸出提取結果的預覽（至少：42 筆的 regionName／dataDate／mint／maxt 表格或其前若干列，加上 Region 數與日期範圍），供「觀察資料」評分。 | A2-1、A2-2、A2-3；§7；OC §2.1 |

### 1.3 Persistence — SQLite

| ID | 類型 | Class | 需求 | 對應 |
| --- | --- | --- | --- | --- |
| R-DB-1 | T | MVM | 資料庫檔案 MUST 是單元根目錄的 `data.db`；資料表 MUST 以老師的 DDL **逐字**建立：`CREATE TABLE TemperatureForecasts (id INTEGER PRIMARY KEY, regionName TEXT, dataDate TEXT, mint REAL, maxt REAL);` | A3-1、A3-2；§8、§9；AB-6 |
| R-DB-2 | T／C | MVM | 每列：`regionName` 為六個 Region 的中文全名之一（含「地區」）；`dataDate` 為 `YYYY-MM-DD`；`mint`／`maxt` 為 R-DER-6 的一位小數值。 | A2-3；§7；AB-6 |
| R-DB-3 | T | MVM | 老師的驗證 SQL MUST 成立：`SELECT DISTINCT regionName FROM TemperatureForecasts;` 回六列；`SELECT * FROM TemperatureForecasts WHERE regionName = '中部地區';` 回七列。 | A3-3、A3-4；§10；AB-6 |
| R-DB-4 | T／C | MVM | **重複執行不重複插入**：persist MUST 在單一交易內以「刪除全部既有列、寫入新的 42 列」整份替換快照；連續執行任意次後 `TemperatureForecasts` 恰為 42 列且 `(regionName, dataDate)` 無重複；交易失敗時既有快照不變。不新增 UNIQUE 約束或改動印出的 DDL。 | §20；OC §2.5、Q4；AB-7 |
| R-DB-5 | P | MVM | Ingestion 時間（ISO 8601，含 `+08:00`）與來源資料集 ID MUST 記錄在 `data.db` 內 `TemperatureForecasts` **以外**的地方（另一張資料表；名稱屬 HOW），供兩個呈現層顯示「最後更新時間」。`TemperatureForecasts` 的 DDL 與內容不因此改變。 | brief §6.7；decision DR-2 |
| R-DB-6 | P | MVM | MVM 交付**準備好的快照**：`data.db` 由 ingestion 在本機產生並提交到 git，部署與評分都使用它；不要求排程更新。 | OC §2.5、Q3；brief §6.1 |

### 1.4 共用查詢／領域模組

| ID | 類型 | Class | 需求 | 對應 |
| --- | --- | --- | --- | --- |
| R-SHR-1 | C | MVM | MUST 有**一個**共用 Python 模組承載全部 SQL 與預報業務邏輯；`app.py` 與 Flask 後端 MUST 只透過它取得資料。任何呈現層檔案 MUST NOT 含 SQL 字串或 Region／Forecast Day 的推導邏輯。 | OC §2.4 A1；AB-5 |
| R-SHR-2 | C | MVM | 共用模組 MUST 提供下列語義（名稱屬 HOW）：(a) 快照狀態 ∈ {ok、missing、empty、incomplete}——ok 當且僅當恰 6 Region × 7 日且每格有值；(b) Region 清單，固定順序：北部地區、中部地區、南部地區、東北部地區、東部地區、東南部地區；(c) 指定 Region 的七日序列（dataDate 升序，mint、maxt）；(d) 指定 Forecast Day 的六區值（regionName、mint、maxt、Derived Map Temperature）；(e) Forecast Day 清單（升序）；(f) 最後 ingestion 時間。 | OC §2.2、§2.4；AB-3、AB-4、AB-14 |
| R-SHR-3 | P | MVM | 共用模組 MUST 以**唯讀**方式開啟 `data.db`，路徑相對於原始碼位置解析（不依賴 process 工作目錄）；MUST 允許測試指定替代的資料庫路徑（機制屬 HOW）。 | brief §6.3；AB-10 |
| R-SHR-4 | C | ENHANCED | Derived Map Temperature ＝ (MinT ＋ MaxT) ／ 2，四捨五入（half-up）到小數一位；色帶為下界包含：`< 20` 藍、`20 – < 25` 綠、`25 – < 30` 黃、`≥ 30` 紅，以**顯示值**（一位小數）分帶。此計算與分帶 MUST 在共用模組（Python）定義；前端如需重算，MUST 與之等價且有測試對照。 | brief §6.5；R5；AB-14 |
| R-SHR-5 | T | MVM | 共用模組與兩個呈現層 MUST NOT 呼叫 CWA API。Python 端（`app.py`、Flask 後端、共用模組）不得 import 任何 HTTP client（`requests`、`httpx`、`urllib.request`、`aiohttp` 等）；瀏覽器端 JS 的資料請求只得指向本應用程式的 `/api/` 路徑；上述任何檔案不得含 `opendata.cwa.gov.tw` 字串或 `CWA_API_KEY` 引用。 | A9-2；AB-5、AB-8 |

### 1.5 Grading App — Streamlit `app.py`（MVM）

| ID | 類型 | Class | 需求 | 對應 |
| --- | --- | --- | --- | --- |
| R-GA-1 | T | MVM | `home_work_01/app.py` MUST 是真正的 Streamlit 應用程式；在單元目錄以 `streamlit run app.py` 可啟動。 | A4、A7；OC §2.4；AB-2 |
| R-GA-2 | T | MVM | 頁面 MUST 顯示標題文字 `Taiwan Weather Forecast`。 | A4 畫面範例；§16；AB-3 |
| R-GA-3 | T | MVM | MUST 有標籤為 `Select Region` 的下拉選單，選項**恰為**六個 Region 中文名、順序依 R-SHR-2(b)；SHOULD 預設選第一個。 | A4-1；§13；AB-3 |
| R-GA-4 | T | MVM | 選定 Region 後 MUST 顯示折線圖：兩條線分別標示 `MaxT` 與 `MinT`，X 軸為七個 Forecast Day（日期），Y 軸為溫度（°C）。SHOULD 有圖表標題 `Temperature Forecast – <Region>`；SHOULD MaxT 紅、MinT 藍。 | A4-3；§14；AB-4 |
| R-GA-5 | T | MVM | MUST 顯示表格，欄位名 `Date`、`MinT`、`MaxT`，恰七列，依日期升序，值與 `data.db` 該 Region 的列一致。 | A4-4；§15；AB-4 |
| R-GA-6 | T | MVM | 資料 MUST 只經共用模組以 SQL 從 `data.db` 取得（R-SHR-1、R-SHR-5）。 | A4-2、A9-2；AB-5 |
| R-GA-7 | P | MVM | `data.db` 缺失或為空時 MUST 顯示明確訊息（指出資料檔缺失／為空與如何產生），不得拋出未處理例外；快照不完整（非 6×7）時 MUST 顯示警告，MAY 仍顯示既有資料。 | OC AB-10；brief §6.7 |
| R-GA-8 | P | MVM | MUST 顯示快照的最後 ingestion 時間（R-DB-5）。 | brief §6.7；DR-2 |
| R-GA-9 | C | MVM | MUST NOT 包含 ENHANCED 項目（Taiwan Map、`Select Date`），MUST NOT 依賴 `folium`／`streamlit-folium`；它承載完整 MVM 行為且只有 MVM 行為。 | OC §2.2、§2.4 A3；CONTEXT「Grading App」 |

### 1.6 Dashboard — Flask API ＋ 靜態前端（MVM 部分）

| ID | 類型 | Class | 需求 | 對應 |
| --- | --- | --- | --- | --- |
| R-DS-1 | C | MVM | Dashboard 後端 MUST 是 Flask 應用程式：`GET /` 回 dashboard 頁面（HTML），靜態資源由同一應用程式或 Vercel 提供；JSON API 一律以 `/api/` 為路徑前綴。 | OC §2.4 A4；brief §5.2；AB-1 |
| R-DS-2 | C | MVM | **健康 endpoint** MUST 為 `GET /api/health`：快照狀態 ok 時回 HTTP 200 與 JSON（至少 `status: "ok"`、Region 數、Forecast Day 數、ingestion 時間）；狀態非 ok 時回 HTTP 503 與 JSON（`status: "unavailable"`、原因、訊息）。 | OC AB-1、AB-17（路徑由 Spec 決定）；AB-10 |
| R-DS-3 | C | MVM | MUST 提供 JSON 資料 endpoint（路徑屬 HOW，`/api/` 前綴，README 文件化），涵蓋 R-SHR-2 的 (b) Region 清單、(c) 指定 Region 七日序列、(d) 指定 Forecast Day 六區值（含 Derived Map Temperature）、(e) Forecast Day 清單；未知 Region／日期回 404 與 JSON 錯誤；快照不可用回 503 與 JSON 錯誤。錯誤 JSON MUST 含人類可讀的 `error` 訊息。 | OC §2.2；AB-4、AB-10、AB-14 |
| R-DS-4 | T | MVM | Dashboard 頁面 MUST 顯示 `Taiwan Weather Forecast`、`Select Region`（六個 Region、固定順序）；選定 Region 後顯示 `MaxT`／`MinT` 七日折線圖與 `Date`／`MinT`／`MaxT` 七列表格；值與 `data.db` 一致。 | A4-1、A4-3、A4-4；AB-3、AB-4 |
| R-DS-5 | T | MVM | 後端 MUST 只經共用模組讀 `data.db`（R-SHR-1、R-SHR-5）；前端 MUST 只呼叫本應用程式的 `/api/` endpoint，不得呼叫 CWA。 | A9-2；AB-5 |
| R-DS-6 | P | MVM | 前端 MUST 處理 API 的 503／404／網路失敗：顯示明確訊息，不得留下空白頁或未處理的 console 例外作為唯一提示。 | AB-10；brief §6.7 |
| R-DS-7 | P | MVM | Dashboard MUST 顯示快照的最後 ingestion 時間。 | brief §6.7；DR-2 |
| R-DS-8 | C | MVM | Vercel 部署 MUST：Python 3.12；單一 Python serverless function 同時提供 API 與頁面（與老師 repo 已驗證模式一致）；Vercel 專案 Root Directory ＝ `home_work_01`；部署設定與 `requirements.txt` 都在單元目錄內；`data.db` 隨程式打包並唯讀讀取；執行期不需要任何環境變數或 secret。 | OC §2.4；brief §5.1–5.3、§6.3；AB-1 |
| R-DS-9 | P | MVM | 公開 URL MUST 不需登入即可存取；`GET /` 回 200 且內容含 `Taiwan Weather Forecast`；`GET /api/health` 回 200。Smoke test 允許最多 90 秒的暖機重試。 | OC AB-1、Q5 |

### 1.7 Dashboard — ENHANCED

| ID | 類型 | Class | 需求 | 對應 |
| --- | --- | --- | --- | --- |
| R-EN-1 | E | ENHANCED | **UI／UX 品質清單**（全部 MUST PASS）：(1) 清楚的視覺層級——標題、控制項、圖表、表格、地圖各自可辨、主次分明；(2) 響應式——桌機（≥ 1024 px）與 375 px 寬皆可完整操作；(3) 至少一項摘要資訊（例如所選 Region 本週最低／最高，或所選日期六區概況）；(4) 圖表可互動且易讀——有圖例、軸標籤、hover／tooltip 顯示數值；(5) loading、empty、error 三種狀態各自有可見呈現；(6) 375 px 寬無不必要的橫向捲動。 | OC AB-15；brief §6.4；Q6 |
| R-EN-2 | E | ENHANCED | 保留老師可見的概念詞：`Taiwan Weather Forecast`、`Select Region`、`Select Date`、`Date`、`MinT`、`MaxT` 與中文 Region 名；視覺框架不限。 | brief §6.4 |
| R-EN-3 | E | ENHANCED | **`Select Date`** 控制項 MUST 列出快照的七個 Forecast Day（升序），選擇後 Taiwan Map 切換到該日；SHOULD 預設第一天。 | A5、§18；AB-14 |
| R-EN-4 | E | ENHANCED | **Taiwan Map** MUST 以 Leaflet 在瀏覽器繪製：以台灣為中心、初始視野涵蓋六個標記、可縮放；六個 Region 各一個標記，位置為專案定義的代表點（座標屬 HOW，README 標示為專案定義）；標記顏色依所選日期該 Region 的 Derived Map Temperature 色帶（R-SHR-4）；點擊或 hover 顯示資訊卡：Region 名、`Date`、`Min`、`Max` 與 Derived Map Temperature（一位小數）。 | A5-1～A5-4、§17–19；OC AB-14；A3 |
| R-EN-5 | E | ENHANCED | 地圖 MUST 有四段色帶圖例，並在圖例或旁註明「平均溫度為 (MinT + MaxT) / 2 導出，非觀測日均溫」。 | brief §6.5；R5；AB-13、AB-14 |
| R-EN-6 | E | ENHANCED | 地圖底圖與 Leaflet 的取得方式（CDN 或 vendored）屬 HOW，但 MUST NOT 需要金鑰、帳號或付費。 | OC §4 RB-3、RB-4 |
| R-EN-7 | E | ENHANCED | **Dashboard 整合**：Region 折線圖／表格、`Select Date`、Taiwan Map 與摘要在同一頁面上整合（「Taiwan Weather Dashboard」）。 | §19；OC §2.2 |

### 1.8 測試與 CI（ENHANCED）

| ID | 類型 | Class | 需求 | 對應 |
| --- | --- | --- | --- | --- |
| R-TC-1 | E | ENHANCED | **pytest** MUST 涵蓋：R-DER-1～R-DER-7（正例與 AC-09 的反例）、R-DB-1～R-DB-4（DDL、驗證 SQL、重複執行）、R-SHR-2～R-SHR-4（狀態、清單、序列、日值、Derived Map Temperature 與色帶）、R-SHR-5 的靜態檢查。 | OC AB-16；Q7 |
| R-TC-2 | E | ENHANCED | **Fixture** MUST 是一份真實的 F-D0047-091 回應（由 Executor 在實作期間以 acceptor 的金鑰擷取一次），提交前 MUST 以自動檢查確認不含金鑰；MAY 為完整回應或保留結構的忠實縮減版（README 記錄取樣日期與是否縮減）。反例 fixture 由正例衍生（刪縣市、刪半天、改無效值）。 | AB-9、AB-8 |
| R-TC-3 | E | ENHANCED | **Streamlit `AppTest`** MUST 涵蓋：標題、`Select Region` 選項、選定 Region 後折線圖與七列表格存在且值正確、`data.db` 缺失與為空時的訊息（無例外）。 | OC AB-3、AB-4、AB-10、AB-16 |
| R-TC-4 | E | ENHANCED | **Flask test client** MUST 涵蓋：`GET /` 200 含標題、`/api/health` 的 200 與 503 兩種、R-DS-3 每個資料 endpoint 的正常回應與 404／503 錯誤。 | OC AB-1、AB-10、AB-16 |
| R-TC-5 | E | ENHANCED | 全部自動化測試 MUST 不需網路與金鑰即可執行。 | AB-16 |
| R-TC-6 | E | ENHANCED | **CI**：GitHub Actions workflow MUST 在 push 時執行全部測試（Python 3.12）；MUST 以路徑過濾只在 `home_work_01/**` 與該 workflow 本身變動時觸發，且 workflow 名稱識別本單元；MAY 另在 pull_request 觸發。 | OC AB-16；RB-5（見 R-ENV-3） |
| R-TC-7 | E | ENHANCED | **部署 smoke test**：另一個以 `workflow_dispatch` 觸發的 workflow，從 repository variable 讀取公開 URL（變數名屬 HOW，README 文件化），檢查 R-DS-9 的兩個條件，總重試時間 ≤ 90 秒；同一檢查 MUST 也能在本機以指令執行。 | OC AB-17；brief §6.6 |

### 1.9 憑證與安全

| ID | 類型 | Class | 需求 | 對應 |
| --- | --- | --- | --- | --- |
| R-SEC-1 | T／P | MVM | 金鑰 MUST 只存在於被 `.gitignore` 忽略、未追蹤的 `home_work_01/.env`（唯一授權位置）；`.env.example` 只含變數名；`git ls-files` MUST 不含任何 `.env`；下列位置 MUST 不含金鑰字串：追蹤檔案（`git ls-files` 所列）、staged／committed diff、終端與 CI log、fixture、保存的原始 JSON、README 與文件、前端／靜態資源、產生的 evidence（worklog、audit、acceptance 紀錄、截圖）。金鑰掃描 MUST 明確排除該被忽略的 `.env`，不得以「整個工作樹零金鑰」為條件。 | A9-1；OC §4 RB-3；AB-8 |
| R-SEC-2 | P | MVM | Ingestion 的任何輸出（終端、錯誤訊息、保存的 JSON）MUST 不含金鑰；請求標頭不得被記錄。 | AB-8 |
| R-SEC-3 | P | MVM | 部署的 Dashboard MUST 不需要任何 secret；Vercel 專案不設定 CWA 金鑰。 | R-DS-8 |

### 1.10 文件與交付

| ID | 類型 | Class | 需求 | 對應 |
| --- | --- | --- | --- | --- |
| R-DOC-1 | T | MVM | 單元 README MUST 含：Python 3.12 與虛擬環境、`pip install -r requirements.txt`、取得金鑰與建立 `.env`、執行 ingestion 的指令（含離線重跑）、`streamlit run app.py`、本機執行 Flask dashboard、執行測試、Vercel 部署步驟（Root Directory、production／preview）、公開 URL、與海報 `HW10_Weather/` 結構的對應表。 | A6、A7、§21；OC AB-11、AB-12；brief §6.9 |
| R-DOC-2 | C | MVM | 技術文件（README 或其連結的文件）MUST 明確記述：F-A0010-001 為老師原指定、2026-07-01 下架為外部限制；F-D0047-091 為專案相容性替代；Forecast Day 的 W1 視窗定義；Region 對應表為**專案定義**、非 CWA 權威分區；區域 MinT／MaxT 為 **PROJECT-DERIVED COMPATIBILITY VALUES**、非 CWA 發布的六區預報；Derived Map Temperature 為導出值；Streamlit 的定位依 OC §2.4（仍是必要評分產物；不作為部署 runtime 是 Vercel 限制造成的相容性安排）。 | OC §2.3、§2.4；AB-13 |
| R-DOC-3 | T | MVM | 專案 MUST 在 GitHub `yotsubamomo/aiot-classwork` 的 `home_work_01/` 交付；原始 JSON 觀察檔、`data.db`、fixture、測試、部署設定都在單元目錄內。 | §21；OC AB-12 |
| R-DOC-4 | P | MVM | 單元 `doc/acceptance/` MUST 有驗收文件，逐條對應本 Spec 第 2 節的 AC，記錄狀態、驗證方式與證據引用（截圖、測試、CI／smoke 執行紀錄、worklog）。 | OC AB-1 證據欄；CLAUDE.md doc 慣例 |
| R-DOC-5 | T | MVM | **程式品質**（海報四個 5%、§20）：模組與主要函式有說明其目的的註解或 docstring；錯誤有處理與明確訊息；沒有死碼與未使用的相依；結構對應資料流的階段。 | A1／A2／A3／A4 程式品質；§20 |

### 1.11 環境與邊界

| ID | 類型 | Class | 需求 | 對應 |
| --- | --- | --- | --- | --- |
| R-ENV-1 | P | MVM | Python **3.12** 本機、CI、Vercel 一致；`requirements.txt` 在單元目錄；相依 SHOULD 固定版本。`folium`／`streamlit-folium` 不列入。 | OC §2.4 A2；A3 |
| R-ENV-2 | P | MVM | 所有實作、資料、測試、部署設定 MUST 留在 `home_work_01/` 內；root 不放本單元檔案。 | OC §2.5；brief §6.3；RB-5 |
| R-ENV-3 | P | ENHANCED | 唯一的例外是 GitHub 強制置於 repo 根 `.github/workflows/` 的 workflow 檔（R-TC-6、R-TC-7）：其建立與修改屬 **RB-5**，MUST 先有 acceptor 的明確、有範圍的授權（見第 9 節與 derivation record）；未授權前該部分工作停止，其餘工作不受影響。 | OC §4；Bindings §2.6 RB-5 |

## 2. Acceptance Criteria（AC）

每條給出可觀察的 PASS 條件、FAIL 例、證據與驗證方式，並對應 Outcome Contract 的 AB 或條款。「兩層」指 Grading App 與 Dashboard。

| ID | Class | 對應 | PASS 條件 | FAIL 例 | 證據／驗證方式 |
| --- | --- | --- | --- | --- | --- |
| AC-01 | MVM | AB-2；R-GA-1 | 在 Python 3.12 虛擬環境、單元目錄執行 `streamlit run app.py`，伺服器啟動且首頁渲染無例外。 | 需要額外參數或從其他目錄才可啟動；啟動即例外。 | worklog 記錄指令與輸出；截圖。 |
| AC-02 | MVM | AB-3；R-GA-2、R-GA-3、R-DS-4 | 兩層皆顯示 `Taiwan Weather Forecast` 與 `Select Region`；選項恰為六個 Region 中文名且順序為 R-SHR-2(b)。 | 少一區、多一區、順序或名稱不同（例如少「地區」二字）。 | `AppTest` 斷言選項；Flask test client 斷言 Region endpoint 與頁面 HTML；瀏覽器截圖。 |
| AC-03 | MVM | AB-4；R-GA-4、R-GA-5、R-DS-4 | 兩層選定任一 Region 後：折線圖有 `MaxT`、`MinT` 兩條線、七個日期；表格欄位 `Date`／`MinT`／`MaxT`、七列、升序；數值等於 `data.db` 該 Region 的列。以中部地區與東南部地區各驗一次。 | 六列或八列；欄名不同；值與資料庫不符；圖與表不一致。 | `AppTest` 斷言 dataframe 內容與 chart 元素；Flask test client 斷言序列 endpoint 七筆與值；截圖。 |
| AC-04 | MVM | AB-5；R-SHR-1、R-SHR-5、R-GA-6、R-DS-5 | 自動化靜態檢查通過：(a) `app.py`、Flask 後端與共用模組（Python）不 import 任何 HTTP client、不含 `opendata.cwa.gov.tw` 或 `CWA_API_KEY`；(b) 前端 JS／靜態資源不含 `opendata.cwa.gov.tw` 或 `CWA_API_KEY`，其資料請求只指向本應用程式的 `/api/` 路徑；(c) SQL 字串只存在於共用模組；(d) `app.py` 與 Flask 後端都 import 同一個共用 Python 模組，且不各自實作查詢或推導邏輯。 | 呈現層自帶 SQL；前端直接 fetch CWA；Flask 另寫一份查詢。 | pytest 靜態檢查；Reviewer 審查 Python import 圖與前端請求目標。 |
| AC-05 | MVM | AB-6；R-DB-1～R-DB-3 | `sqlite_master` 中 `TemperatureForecasts` 的欄位為 `id INTEGER PRIMARY KEY, regionName TEXT, dataDate TEXT, mint REAL, maxt REAL`；`SELECT DISTINCT regionName` 回六列；`WHERE regionName = '中部地區'` 回七列且 dataDate 為 `YYYY-MM-DD`。對提交的 `data.db` 與測試產生的資料庫都成立。 | 欄名大小寫或型別不同；多一張同名表；日期格式不同。 | pytest；Reviewer 對提交的 `data.db` 執行兩句 SQL。 |
| AC-06 | MVM | AB-7；R-DB-4 | 以同一 fixture 連續 ingest 兩次 → 42 列、`(regionName, dataDate)` 無重複；以日期平移後的第二份 fixture ingest → 42 列且全部為新日期（舊快照完全被替換）。 | 84 列；混合新舊日期。 | pytest。 |
| AC-07 | MVM | AB-8；R-ING-1、R-ING-2、R-SEC-1～R-SEC-3 | (a) worklog 記錄以 `.env` 金鑰實際成功取得 F-D0047-091 一次（不含金鑰值）；(b) `git ls-files` 不含 `.env`；(c) 對追蹤檔案（`git ls-files` 所列）與 staged／committed diff 以金鑰格式搜尋為 0 筆，掃描明確排除被忽略的 `home_work_01/.env`；(d) fixture 與保存的原始 JSON 無 `Authorization` 值；(e) Vercel 專案不需環境變數；(f) 產生的 evidence（worklog、audit、acceptance 紀錄、截圖）與終端／CI log 不含金鑰。 | fixture 內含金鑰；README 貼出金鑰；Flask 讀 `.env`；evidence 貼出含金鑰的指令列。 | worklog；CI 內的自動檢查（b、c、d）；Reviewer 審查（f）。 |
| AC-08 | MVM | AB-9；R-DER-1～R-DER-7 | 對真實 fixture 執行 derive：得到七個**連續**且完整的 Forecast Day、六個 Region、42 筆皆有 MinT／MaxT；至少兩個 Region × 兩個日期的值等於測試內以縣市值手算的期望（含 half-up 一位小數）；擷取開頭的不完整日期被丟棄。 | 取前七個標籤而未逐日檢查；分母錯；四捨五入錯。 | pytest，期望值寫在測試內並註明來源縣市值。 |
| AC-09 | MVM | AB-9；R-DER-3、R-DER-4、R-DER-6、R-DER-7 | 反例各自失敗且**不寫入**資料庫、結束碼非零、訊息指名問題：(1) 刪除一個成員縣市（例如苗栗縣）→ 錯誤指名縣市；(2) 刪除某日一段 → 錯誤指名日期；(3) 某值改為 `-`／空字串 → 錯誤指名縣市與日期；(4) 只剩六個完整日 → 錯誤；(5) 七日不連續 → 錯誤。既有快照在失敗後保持原狀。 | 缺縣市時以其餘縣市平均；缺半天時以單段當整日。 | pytest。 |
| AC-10 | MVM | AB-10；R-GA-7、R-DS-2、R-DS-3、R-DS-6、R-SHR-3 | 指向不存在的資料庫路徑：Grading App 顯示明確訊息且無例外；`/api/health` 回 503 JSON、資料 endpoint 回 503 JSON、`GET /` 頁面顯示錯誤狀態。指向只有表無列的資料庫：同上（原因 empty）。不完整快照：Grading App 顯示警告；`/api/health` 回 503。 | 例外堆疊；空白頁；health 仍回 200。 | `AppTest`（替代路徑）；Flask test client；瀏覽器截圖（error 狀態）。 |
| AC-11 | MVM | AB-10；R-ING-3 | Ingestion 面對 HTTP 401、404、5xx、逾時與非 JSON 回應時：明確錯誤訊息、非零結束碼、不寫資料庫、輸出不含金鑰。 | 靜默結束；例外堆疊為唯一訊息。 | pytest（mock HTTP）。 |
| AC-12 | MVM | AB-11；R-DOC-1 | README 的每一步驟在乾淨的 Python 3.12 虛擬環境實際執行成功：安裝、ingestion（真實一次＋離線重跑）、`streamlit run app.py`、本機 Flask、測試；部署步驟依 README 完成。 | 步驟缺漏或與實際指令不符。 | worklog 逐步記錄指令、結果與日期。 |
| AC-13 | MVM | AB-12；R-DOC-3、R-ENV-2 | 全部產物在 `home_work_01/` 內（workflow 檔除外，R-ENV-3）；topic branch 已 push、PR 已開（SA-1、SA-2）。合併為 acceptor 的 release 動作（RB-1），不是完成條件。 | 單元檔案散落 root。 | repo 狀態；PR 連結。 |
| AC-14 | MVM | AB-13；R-DOC-2 | 文件審查清單全部 PASS：(1) F-A0010-001 原指定與下架；(2) F-D0047-091 為相容性替代；(3) W1 視窗定義；(4) 對應表標示專案定義；(5) 區域值標示 PROJECT-DERIVED COMPATIBILITY VALUES；(6) Derived Map Temperature 標示導出；(7) Streamlit 定位敘述與 OC §2.4 一致；(8) 沒有任何地方把區域值寫成 CWA 發布或把對應表寫成 CWA 分區。 | 任一項缺失或措辭相反。 | Reviewer 文件審查，逐項引用行號。 |
| AC-15 | MVM | AB-1；R-DS-8、R-DS-9 | 對 Vercel 公開 URL（不需登入）：`GET /` 200 且 body 含 `Taiwan Weather Forecast`；`GET /api/health` 200 且 `status` 為 `ok`；在 90 秒重試內達成。部署的 commit 與受審 subject 對應。 | 需登入（deployment protection）；health 503；超過 90 秒。 | smoke 指令輸出（含時間戳、URL、狀態碼）記入 `doc/acceptance/`。 |
| AC-16 | MVM | AB-1、AB-10；R-DS-2 | `/api/health` 對正常快照回 200 JSON 含 `status: "ok"`、六、七與 ingestion 時間；對缺失／空／不完整回 503 JSON 含原因。 | 缺欄位；不完整仍回 ok。 | Flask test client。 |
| AC-17 | ENHANCED | AB-14；R-EN-4、R-EN-5、R-EN-6 | 瀏覽器手動驗收：地圖以台灣為中心、六個標記皆可見、可縮放；對所選日期每個標記顏色等於共用模組算出的色帶（以 endpoint 回傳值對照）；點擊標記顯示 Region、Date、Min、Max 與導出平均；圖例四段且有「導出」說明；底圖不需金鑰。 | 標記顏色與值不符；缺圖例；離島或第七個標記。 | 手動驗收清單＋桌機截圖；色帶對照以 endpoint 值列表附證。 |
| AC-18 | ENHANCED | AB-14；R-EN-3 | `Select Date` 列出七個 Forecast Day（升序）；切換日期後標記顏色與資訊卡值隨之更新，與該日 endpoint 值一致。 | 少於七個；切換無效。 | 手動驗收＋兩個日期的截圖。 |
| AC-19 | ENHANCED | AB-15；R-EN-1、R-EN-2、R-EN-7 | R-EN-1 六項各自 PASS，並在桌機（≥ 1024 px）與 375 px 各截圖；375 px 下 `document.documentElement.scrollWidth` 不大於視窗寬度；loading／empty／error 三種狀態各一張截圖（可用 DevTools 模擬）。 | 任一項 FAIL；375 px 出現橫向捲軸。 | 手動驗收清單＋截圖。 |
| AC-20 | ENHANCED | AB-16；R-TC-6 | 對含本單元變更的 push，GitHub Actions 執行成功；job log 顯示 Python 3.12 與 pytest 收集到 derive、DB、共用模組、`AppTest`、Flask test client 各類測試且全數通過；對不含本單元變更的 push 不觸發。 | 任一類測試缺席；用 3.11 執行。 | CI run URL＋log 摘錄。 |
| AC-21 | ENHANCED | AB-16；R-TC-1～R-TC-5 | 測試套件存在且涵蓋 R-TC-1、R-TC-3、R-TC-4 列出的每一項；在無網路、無 `.env` 的環境全部通過。 | 測試依賴網路或金鑰；反例缺席。 | pytest 輸出；Reviewer 對照清單。 |
| AC-22 | ENHANCED | AB-17；R-TC-7 | 以 `workflow_dispatch` 手動觸發 smoke workflow，成功完成並記錄 `GET /` 與 `/api/health` 的狀態碼；本機執行同一檢查亦成功。 | workflow 無法手動觸發；未檢查 health。 | workflow run URL；本機輸出。 |
| AC-23 | MVM | OC §2.4 A2；R-ENV-1 | 本機 `python --version` 為 3.12.x（worklog）；CI 指定 3.12；Vercel 部署日誌或設定顯示 Python 3.12。 | 三者任一不同。 | worklog；CI log；Vercel 設定截圖。 |
| AC-24 | MVM | OC §2.5→brief §6.7；R-DB-5、R-GA-8、R-DS-7 | 兩層皆顯示最後 ingestion 時間，且等於資料庫內記錄值；`TemperatureForecasts` 的 DDL 未改。 | 只有一層顯示；時間取自檔案 mtime。 | `AppTest`；Flask test client；AC-05。 |
| AC-25 | MVM | OC §2.1→A1-6、A1-7、A2-1；R-ING-4、R-DER-8 | 執行 ingestion 後，單元目錄內存在完整、縮排的原始 JSON 檔（不含金鑰）；終端輸出含取得成功摘要與 42 筆預覽；README 說明 F-D0047-091 的結構（可引用 brief §4.5）與這些觀察產物的位置。 | 只印 `resp.status_code`；沒有預覽。 | worklog 貼終端輸出；檔案存在；Reviewer 審查。 |
| AC-26 | MVM | OC §2.2、§2.4 A3；R-GA-9 | `app.py` 及其 import 不含地圖、`Select Date`、`folium`／`streamlit-folium`；`requirements.txt` 不含 folium。 | Grading App 出現地圖。 | 靜態檢查；`AppTest`。 |
| AC-27 | MVM | OC §2.1→程式品質、§20；R-DOC-5 | Reviewer 依 R-DOC-5 四項逐一給出 PASS 並引用位置。 | 無錯誤處理；模組無說明；死碼。 | Reviewer 審查。 |
| AC-28 | ENHANCED | AB-14；R-SHR-4 | pytest 驗證 Derived Map Temperature 與色帶：(20.1, 25.2) → 22.7；(19.9, 20.0) → 20.0 → 綠；(24.9, 25.0) → 25.0 → 黃；(29.9, 30.0) → 30.0 → 紅；(15, 24.8) → 19.9 → 藍。前端若重算，相同案例有 JS 對照測試或以 endpoint 值直接著色。 | 邊界值分帶錯；banker's rounding 造成 22.6。 | pytest（＋前端對照）。 |
| AC-29 | ENHANCED | OC §4 RB-5；R-ENV-3、R-TC-6 | workflow 檔的建立有 acceptor 授權紀錄（接受紀錄或對話原文記入 worklog）；workflow 只在 `home_work_01/**` 與自身變動時觸發；名稱識別本單元。 | 無授權即建立；觸發全 repo。 | worklog 引用授權原文；workflow 內容審查。 |
| AC-30 | MVM | OC §2.5→brief §6.3；R-DS-8、R-ENV-2 | 部署設定與 `requirements.txt` 在 `home_work_01/`；Vercel Root Directory ＝ `home_work_01`；root 沒有本單元的設定檔。 | root 出現 `vercel.json` 或 `requirements.txt`。 | repo 狀態；Vercel 設定截圖。 |

## 3. Invariants（跨 Ticket，Spec Integration Audit 必核）

| ID | Invariant | 依據 |
| --- | --- | --- |
| INV-1 | 查詢語義只有一份：全部 SQL 與預報業務邏輯在共用 Python 模組；`app.py` 與 Flask 後端只呼叫它；瀏覽器端 JS 只呼叫 Flask 的 `/api/`。 | OC §2.4 A1；AB-5 |
| INV-2 | 行為對等：對同一 Region，兩層顯示相同的七筆 `(Date, MinT, MaxT)`；Dashboard 的 MVM 行為不弱於 Grading App。 | OC §2.4 |
| INV-3 | 快照恰 6 × 7：`TemperatureForecasts` 任何時刻為 0 列（未 ingest）或 42 列；永不部分寫入。 | OC §2.3；AB-7、AB-9 |
| INV-4 | 老師指定的名字不變：`app.py`、`data.db`、`TemperatureForecasts` DDL、五個欄位名、六個 Region 名、`streamlit run app.py`、頁面文字。 | AB-2、AB-3、AB-6；H-2 |
| INV-5 | 金鑰零外洩：只在被忽略、未追蹤的 `home_work_01/.env`；不進 git（追蹤檔案與 diff）、log、前端、文件、fixture、產生的 evidence。 | AB-8；H-1 |
| INV-6 | 呈現層不呼叫 CWA。 | A9-2；AB-5 |
| INV-7 | 標示要求：區域值＝專案推導相容性值；對應表＝專案定義；Derived Map Temperature＝導出。 | AB-13；H-3 |
| INV-8 | Python 3.12 三處一致。 | OC §2.4 A2 |
| INV-9 | Scope class 分明：ENHANCED 只在 Dashboard；Grading App 只有 MVM。 | OC §2.1、§2.2 |

## 4. Implementation Decisions

### 4.1 契約固定（Executor 不得自行改變）

- **單元錨點。** `app.py` 與 `data.db` 在 `home_work_01/` 根；`requirements.txt` 與 Vercel 設定在同一目錄；Vercel Root Directory ＝ `home_work_01`。共用模組、ingestion、Flask 後端與靜態前端都在單元目錄內，位置與名稱屬 HOW。
- **Region 與日期表示。** Region 名稱與順序依 R-SHR-2(b)；`dataDate` 為 `YYYY-MM-DD`（台灣本地日期）；共用模組回傳的序列一律日期升序。
- **快照替換。** R-DB-4：單一交易、刪全部再寫 42 列；不改 DDL、不加索引或約束。`id` 由 SQLite 指派。
- **推導。** R-DER-1～R-DER-7 逐字；四捨五入採 half-up（以十進位語義，例如 `Decimal` 的 `ROUND_HALF_UP`），不用二進位浮點的 banker's rounding。以整數輸入計算 Region 平均時實際不會出現 tie；Derived Map Temperature 會。
- **Ingestion 中繼資料。** R-DB-5：另一張表記錄 ingestion 時間與來源資料集 ID；不改 `TemperatureForecasts`。
- **健康 endpoint。** `GET /api/health`，語義依 R-DS-2；其他 JSON endpoint 以 `/api/` 為前綴。錯誤回應為 JSON 含 `error`。
- **文字。** `Taiwan Weather Forecast`、`Select Region`、`Select Date`、`Date`、`MinT`、`MaxT`、`MaxT`／`MinT` 線名；資訊卡 `Min`／`Max`。
- **技術。** Python 3.12；`requests`；`sqlite3`；Streamlit；Flask；靜態 HTML／CSS／JS 無 build step；Leaflet；底圖免金鑰免付費。不用 Folium、streamlit-folium、React／Next.js、FastAPI、Windy。
- **憑證。** `CWA_API_KEY` 於未追蹤 `.env`，只有 ingestion 讀；Dashboard 不需 secret。
- **測試接縫。** 共用模組（兩層共同依賴）、ingestion 的 derive 函式（純函式，輸入為解析後的 JSON 物件）、`AppTest`、Flask test client、smoke 指令；fixture 為真實樣本。

### 4.2 交給實作（HOW）

- Ingestion 的檔案切分與 CLI 介面（SHOULD 讓 fetch／parse／database 三階段可辨識，R-ING-6）；原始 JSON 的保存檔名；可設定無效值集合的形式。
- 共用模組與中繼資料表的名稱；資料庫路徑覆寫機制（環境變數或參數）。
- `/api/` 之下資料 endpoint 的確切路徑與查詢參數形式。
- Streamlit 的圖表 API；Dashboard 的圖表函式庫（免費、免金鑰）；CSS 作法；Leaflet 與圖表函式庫用 CDN 或 vendored；六個 Region 代表點座標。
- Flask 的靜態檔提供方式與 Vercel 設定內容（依老師 repo 已驗證模式：單一 function 接全部路由）。
- 測試檔案配置、fixture 是否縮減、反例 fixture 的產生方式。
- Workflow 檔名（須識別本單元）、repository variable 名稱、smoke 指令的語言（Python 或 shell）。
- Logging 與終端輸出格式。

## 5. Testing Decisions

### 5.1 什麼是好的測試

- 測外部行為：給定 fixture 得到什麼 42 筆、什麼錯誤；不測內部函式怎麼分組。
- 全部離線：不呼叫 CWA、不讀 `.env`；HTTP 失敗以 mock 產生。
- 一個測試一個行為；反例必須斷言「沒有寫入資料庫」而不只是「拋出錯誤」。
- 邊界優先：擷取開頭只有夜間段的日期、第八個日期只有白天段、`臺` 與 `台`、half-up 的 `.x5`、色帶四個下界。

### 5.2 範圍與方法（對應 R-TC）

| 層 | 方法 | 必測 |
| --- | --- | --- |
| Derive | pytest，真實 fixture＋衍生反例 | AC-08、AC-09、AC-28 |
| Persist | pytest，暫存資料庫 | AC-05、AC-06、AC-24 |
| 共用模組 | pytest，暫存與缺失資料庫 | 狀態四種、清單、序列、日值、時間 |
| Grading App | Streamlit `AppTest` | AC-02、AC-03、AC-10、AC-24、AC-26 |
| Dashboard API | Flask test client | AC-02、AC-03、AC-10、AC-16、AC-24 |
| 靜態檢查 | pytest 讀原始碼 | AC-04、AC-07(d)、AC-26 |
| 部署 | smoke 指令（本機＋`workflow_dispatch`） | AC-15、AC-22 |
| ENHANCED UI | 手動驗收清單＋截圖；瀏覽器自動化只在需要時採用 | AC-17、AC-18、AC-19 |

### 5.3 CI

- push 觸發、路徑過濾至本單元、Python 3.12、執行整個 pytest（含 `AppTest` 與 Flask test client 測試）、再執行 AC-07(b)(c)(d) 的憑證檢查。
- smoke 為獨立 workflow，`workflow_dispatch`；不在 push 時打公開 URL。

### 5.4 既有做法

`week02/` 用 Node 內建測試器測純邏輯、副作用留給手動驗收；本單元沿用「純邏輯集中在可匯入模組、副作用以最薄的接縫測」的原則，工具改為 Python 生態（pytest、`AppTest`、Flask test client）。

## 6. Verification Strategy（誰在什麼時候看什麼）

| 階段 | 動作 | 依據 |
| --- | --- | --- |
| Executor self-verification（每 Ticket） | 跑 Ticket 引用的 AC 對應測試；worklog 引用結果；不得以弱化測試取得通過。 | 治理 §3.5；impl-default §5 |
| Ticket independent audit（R1／R2） | Reviewer 依 Ticket 引用的 AC 逐條 PASS／FAIL；觸及 H-1／H-2／H-3 的 Ticket，audit record MUST 明記對該類別的核對（見 decision record）。 | 治理 §4；Bindings §5 |
| Spec Integration Audit（全部 Ticket 結案後） | 對整合 subject 核 INV-1～INV-9、AC-01～AC-30 全部（含 ENHANCED 手動項）、AB-1～AB-17 的涵蓋、traceability。 | 治理 §4.7；derivation record |
| DA phase acceptance | 引用已 closure 的 Spec Integration Audit record。 | 治理 §3.8 |
| Release（acceptor） | 合併前：Bindings §5 gate（全部 Ticket 結案、Spec Integration Audit closure、phase acceptance、README 實跑、無追蹤中的機密）；合併後對 production URL 重跑 smoke 記為 release evidence。 | Bindings §5；RB-1 |

## 7. 對應矩陣（AB → AC → R）

| AB | AC | 主要 R |
| --- | --- | --- |
| AB-1 | AC-15、AC-16 | R-DS-2、R-DS-8、R-DS-9 |
| AB-2 | AC-01 | R-GA-1 |
| AB-3 | AC-02 | R-GA-2、R-GA-3、R-DS-4、R-SHR-2 |
| AB-4 | AC-03 | R-GA-4、R-GA-5、R-DS-3、R-DS-4 |
| AB-5 | AC-04 | R-SHR-1、R-SHR-5、R-GA-6、R-DS-5 |
| AB-6 | AC-05 | R-DB-1～R-DB-3 |
| AB-7 | AC-06 | R-DB-4、R-DER-7 |
| AB-8 | AC-07 | R-ING-1、R-ING-2、R-SEC-1～R-SEC-3 |
| AB-9 | AC-08、AC-09 | R-DER-1～R-DER-7、R-TC-2 |
| AB-10 | AC-10、AC-11、AC-16 | R-GA-7、R-DS-2、R-DS-3、R-DS-6、R-ING-3 |
| AB-11 | AC-12、AC-25 | R-DOC-1、R-ING-4、R-DER-8 |
| AB-12 | AC-13 | R-DOC-3、R-ENV-2 |
| AB-13 | AC-14 | R-DOC-2、R-EN-5 |
| AB-14 | AC-17、AC-18、AC-28 | R-EN-3～R-EN-6、R-SHR-4 |
| AB-15 | AC-19 | R-EN-1、R-EN-2、R-EN-7 |
| AB-16 | AC-20、AC-21 | R-TC-1～R-TC-6 |
| AB-17 | AC-22 | R-TC-7 |
| OC §2.4 A2 | AC-23 | R-ENV-1 |
| OC §2.5（brief §6.7） | AC-24 | R-DB-5、R-GA-8、R-DS-7 |
| OC §2.2／§2.4 A3 | AC-26 | R-GA-9 |
| OC §2.1（程式品質） | AC-27 | R-DOC-5 |
| OC §4 RB-5 | AC-29 | R-ENV-3 |
| OC §2.5（brief §6.3） | AC-30 | R-DS-8、R-ENV-2 |

## 8. Out of Scope

- **OPTIONAL（Outcome Contract 草稿列為可做、本 Spec 不 derive）**：排程更新 CWA 資料（GitHub Actions 定時、伺服器排程、自動重建 `data.db`）；非必要的工程改良。日後要做時由 Design Authority 在 Outcome Contract 邊界內另行 derive（接受後不需 acceptor 重新授權），但不得成為本 Spec 的完成條件。
- **REFERENCE／FUTURE（non-scope）**：React／Next.js、FastAPI、Windy；老師 repo 的 22 縣市／GIS 架構；課程總覽 §22 以後；Part B 的測站觀測、heatmap、自動更新、圖層切換。
- **不做**：把 Streamlit 部署到任何平台（Streamlit Community Cloud、Render、stlite）；歷史預報儲存；離島三縣的任何呈現；多語言 UI；使用者帳號；Folium。
- **不由 Agent 執行（reserved）**：建立 Vercel 專案與設定 Root Directory／production branch／deployment protection（RB-3）；設定 GitHub repository variable（RB-3）；合併進 `main`（RB-1）；繳交作業（RB-2）；任何付費（RB-4）；建立 `.github/workflows/` 檔案除非 RB-5 授權（R-ENV-3）。

## 9. Further Notes

### 前置條件（acceptor 動作；缺任一項時只停止受影響路徑）

| # | 動作 | 影響的 AC | 保留依據 |
| --- | --- | --- | --- |
| 1 | 接受 Outcome Contract（第 8 節）；其第 1–7 節 normative 內容與 `c45ec61` 實質相同時本 Spec 自動生效（第 0 節）。 | 全部 | 治理 §1.2 |
| 2 | 對 `.github/workflows/` 內本單元 workflow 檔（建議兩個：CI 與 smoke）給予**有範圍**的 RB-5 授權；建議在接受紀錄中一併寫明。 | AC-20、AC-22、AC-29 | RB-5 |
| 3 | 在 Vercel 建立專案、連結本 repo、Root Directory ＝ `home_work_01`，並使受審 commit 的部署可**不需登入**存取（production branch 指向 topic branch，或關閉 preview 的 deployment protection）。 | AC-15、AC-17～AC-19、AC-23 | RB-3 |
| 4 | 設定 smoke 用的 repository variable（公開 URL）。 | AC-22 | RB-3 |
| 5 | 本機安裝 Python 3.12（brief §7 #4）。 | AC-01、AC-12、AC-23 | — |
| 6 | 完成 Bindings §8.2 #4 binding dry-run。 | Formal activation | Bindings §3.6 |

### 已知風險與處理

- **F-D0047-091 也可能下架。** Ingestion 依 R-ING-3 明確報錯；已提交的 `data.db` 仍可服務兩層。不在本 Spec 內預備第二替代來源。
- **Vercel deployment protection。** 新專案的 preview 部署預設可能要求登入；AC-15 要求「不需登入」，由 acceptor 的 Vercel 設定決定用 preview 或 production 驗證。合併後對 production URL 再跑一次 smoke 作為 release evidence（不是完成條件）。
- **Vercel Hobby 是否需信用卡未驗證**；若需要，屬 RB-4，由 acceptor 決定。
- **`data.db` 是提交到 git 的二進位檔**（約數十 KB）；每次 ingestion 會產生新的 diff。這是 MVM「準備好的快照」的直接後果。
- **原始 JSON 觀察檔約 686 KB**；MAY 只提交 fixture（可縮減）而把完整觀察檔列入 `.gitignore` 例外之外——但 AC-25 要求 README 說明其位置與產生方式；提交與否屬 HOW。
- **SQLite 唯讀讀取在 Vercel** 只以老師 repo 的成功部署為證據；若失敗，屬實作期發現，route Design Authority。
- **W1 之外的方案已被拒**（EndTime 歸屬、苗栗→中部、極值 envelope）；對 2026-09-23 樣本影響 ≤ 0.6 °C。不得在實作中重開。

### 與海報的對應說明（給 README）

海報 `HW10_Weather/` 的 `fetch_weather.py`／`parse_weather.py`／`database.py`／`app.py`／`data.db`／`requirements.txt`／`README.md` 是建議結構；本專案保留 `app.py`、`data.db`、`requirements.txt`、`README.md` 四個名字，其餘以 README 的對應表說明（R-ING-6、R-DOC-1）。海報的 `weather_data.csv` 為可選中間產物，本 Spec 不要求。

### 詞彙

以 [`../../CONTEXT.md`](../../CONTEXT.md) 為準：Region、County、Forecast Day、MinT／MaxT、Compatibility value、Forecast Snapshot、Ingestion、Refresh、Web App、Grading App、Dashboard、Taiwan Map、Derived Map Temperature、Select Region／Select Date、MVM、Scope class。

## 10. 版本紀錄

| 版本 | 日期 | 變更 | 性質 |
| --- | --- | --- | --- |
| v1.0 | 2026-09-23 | 初版 derive（Outcome Contract 草稿 `c45ec61`）。 | — |
| v1.1 | 2026-09-23 | 一致性修正（acceptor 指示）：第 0 節的接受用語與生效／重新 derive 條件；Problem Statement 的「已接受」用語；R-SHR-5、AC-04、INV-1 的共用模組與瀏覽器端措辭；R-SEC-1、AC-07、INV-5 的金鑰掃描範圍（排除被忽略的 `.env`）；第 8 節 OPTIONAL 與第 9 節前置 #1 的用語。 | 治理 §5.3 第 2 類：不改變任何 normative 產品決定、scope、D2 語義、架構或 acceptance boundary。詳見 derivation record 第 12 節。 |
| v1.1（metadata） | 2026-09-24 | 第 0 節狀態列改為 EFFECTIVE（Outcome Contract 第 8 節於 2026-09-23 接受）；記錄 Ticket derivation（Issues #18–#25，索引 `doc/ticket/tickets.md`）；同日第二次編修（acceptor 指示）把標頭「Issue tracker」列由「尚未 derive」改為已 derive 與索引路徑。 | Metadata，不動語義，版本不變。 |
