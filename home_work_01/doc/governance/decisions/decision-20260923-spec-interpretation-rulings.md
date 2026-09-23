# Decision record — Spec derivation 的解讀裁決（`home_work_01/`）

- **紀錄類型**：Design Authority decision record（治理 §3.6-A 類：在不改變任何 accepted 語義的前提下裁決既有來源容許多種解讀之處；治理 §5.3 第 2 類）
- **日期**：2026-09-23
- **相關契約**：Outcome Contract 草稿 `c45ec61`；Spec v1.1；derivation record [`derivation-SPEC.md`](derivation-SPEC.md)
- **執行角色**：`gov-design-authority`
- **效力**：與 Spec 同時生效（生效與重新 derive 條件依 Spec §0 與 derivation record 第 1 節）；Executor 與 Reviewer 以本紀錄為 Spec 對應條款的解讀依據，不得重開。
- **用語**：各條「改變 accepted 語義」的判定對象是 Outcome Contract 草稿所載、grill 已裁決、接受後即為治理 §1.2 所稱 accepted 語義的內容；Outcome Contract 目前仍為 DRAFT。
- **修訂**：2026-09-23 續派（acceptor 一致性修正指示）修訂效力段、本用語註與總結；十六條裁決內容未變。

每條裁決記：問題、裁決、依據、是否改變 accepted 語義、受影響項目。

## DR-1 哪些 HOW 凍結在 Spec、哪些交給實作

- **問題**：OC §2.4 末項寫「API 路徑、JS 函式庫、路由設定、模組切分與確切檔案結構屬 DA 的 Spec 決定，除非是可觀察驗收條件的一部分」；acceptor 派工指示要求「leave low-level HOW decisions to implementation where they do not need to be contractually frozen」。
- **裁決**：DA 只凍結 (a) 可觀察驗收條件的一部分（`app.py`、`data.db`、DDL、`streamlit run app.py`、頁面文字、`GET /api/health`、Vercel Root Directory）、(b) 會被其他 Ticket 依賴的介面與語義（共用模組的語義、`/api/` 前綴、推導規則、資料表示、技術棧）、(c) 治理或 reserved boundary 要求的位置限制（單元目錄、workflow 範圍）。其餘（Spec §4.2）交給實作。
- **依據**：治理 §1.3「strong contract, loose execution」；§3.3「改變其他工作所依賴的設計基線」的判準；OC §2.4 本身把決定權交給 DA，DA 決定不凍結即是決定。
- **改變 accepted 語義**：否。
- **受影響**：Spec §4.1／§4.2；未來 Ticket 的 HOW 空間。

## DR-2 「最後更新時間」的儲存與顯示

- **問題**：OC §2.5 引入 brief §6.7「頁面顯示最後更新時間」；`TemperatureForecasts` 的 DDL 逐字固定、無時間欄位；S2「採與老師 DDL 一致的最簡作法」。時間存哪裡、哪一層顯示、算不算 ENHANCED？
- **裁決**：(1) ingestion 時間（ISO 8601，+08:00）與來源資料集 ID 存在 `data.db` 內另一張資料表（名稱屬 HOW）；不改 `TemperatureForecasts`；不用檔案 mtime（git checkout 與 Vercel 打包後不可靠）。(2) 兩個呈現層都顯示。(3) 這是資料出處標示，不是 ENHANCED 功能，Grading App 顯示它不違反「只有 MVM 行為」。
- **依據**：OC §2.5；brief §6.2、§6.7；CONTEXT「Grading App」；H-2 只要求 DDL 與五欄不變，另建表不觸及。
- **改變 accepted 語義**：否。
- **受影響**：R-DB-5、R-GA-8、R-DS-7、AC-24。

## DR-3 「重複執行不重複插入」的機制

- **問題**：課程總覽 §20 與 OC AB-7 要求重跑不重複；Q4 裁定資料表是「目前一週快照，不是歷史」；S2 要求 DDL 不變。可選：UNIQUE 索引＋upsert、先查後插、整份替換。
- **裁決**：整份替換——單一交易內刪除全部既有列、寫入新的 42 列；失敗則 rollback 保留舊快照。不加索引或約束、不改 DDL。
- **依據**：Forecast Snapshot 語義（CONTEXT）「A new snapshot replaces the previous one entirely」；AB-7 的觀察條件（42 列、無重複）；最簡且不改 DDL。
- **改變 accepted 語義**：否。
- **受影響**：R-DB-4、R-DER-7、AC-06、INV-3。

## DR-4 四捨五入與色帶分帶

- **問題**：D2-3「rounded to one decimal」與 R5「顯示到小數一位」未指定 tie 規則；色帶以四捨五入前或後的值分帶未定。
- **裁決**：half-up（十進位語義，例如 `Decimal` 的 `ROUND_HALF_UP`），不用二進位浮點 banker's rounding；色帶以**顯示值**（一位小數）分帶，使顏色與看到的數字一致。以整數輸入計算 Region 平均（分母 1、3、6、7）實際不會產生 tie；Derived Map Temperature 會（例如 (20.1 + 25.2) / 2 ＝ 22.65 → 22.7）。
- **依據**：「四捨五入」的通常語義；測試需要單一期望值；使用者可見一致性。
- **改變 accepted 語義**：否（只確定未寫明的 tie 規則）。
- **受影響**：R-DER-6、R-SHR-4、AC-08、AC-28。

## DR-5 保留規則的精確化

- **問題**：D2-1「discard the incomplete starting date … retain the next seven dates that each contain both expected 12-hour periods」未說明：第一個日期完整時怎麼辦、七日不連續怎麼辦、第八個以後怎麼辦。
- **裁決**：依日期升序；第一個日期不完整則丟棄，完整則保留；接著取七個日期，須為連續曆日且每一個都完整，否則 ingestion 失敗（不寫入）；其後多餘期間忽略。
- **依據**：「一週」的語義要求連續；「逐日檢查兩段都在，不是取前七個標籤」（OC §2.3 驗證要求）；brief §4.5 兩種擷取時點（06:00 起或 18:00 起）都能得到七個完整日。
- **改變 accepted 語義**：否。
- **受影響**：R-DER-3、AC-08、AC-09。

## DR-6 「觀察 JSON」「觀察資料」的可觀察產物

- **問題**：A1-6「使用 `json.dumps` 觀察回傳的 JSON」、A1-7、A2-1「分析 JSON 結構」有配分（各 5%），但 OC 的 AB 沒有逐條對應。
- **裁決**：它們是上位契約條款，MVM 必須滿足（OC §2.1）。Spec 以可觀察產物承載：fetch 階段把完整、縮排的原始 JSON 寫到單元目錄內文件化的位置並輸出摘要；derive 階段輸出 42 筆預覽；README 說明結構與位置。提交原始 JSON 檔與否屬 HOW，fixture（可縮減）必提交。
- **依據**：OC §1、§2.1、§3「具體 AC 由 DA 在此邊界內 derive」。
- **改變 accepted 語義**：否（不新增老師沒提的要求；只讓已有的配分項可驗收）。
- **受影響**：R-ING-4、R-DER-8、AC-25。

## DR-7 健康 endpoint

- **問題**：OC AB-1 把路徑交給 Spec；語義未定。
- **裁決**：`GET /api/health`；快照狀態 ok（恰 6 × 7）→ 200 與 `status: "ok"`、Region 數、Forecast Day 數、ingestion 時間；否則 503 與原因。Smoke test 以 200 為 PASS。
- **依據**：OC AB-1、AB-10、AB-17；讓健康檢查反映資料而非只反映 process 存活。
- **改變 accepted 語義**：否。
- **受影響**：R-DS-2、AC-15、AC-16、AC-22。

## DR-8 Region 選項順序

- **問題**：AB-3 只要求「恰為六個 Region 的中文名」；順序未定。
- **裁決**：依上位契約 A1-3 的順序：北部地區、中部地區、南部地區、東北部地區、東部地區、東南部地區；兩層一致；由共用模組決定，不由 SQL 排序或字母序。
- **依據**：REQUIREMENTS A1-3；INV-2 行為對等。
- **改變 accepted 語義**：否。
- **受影響**：R-SHR-2(b)、R-GA-3、R-DS-4、AC-02。

## DR-9 快照不完整時的行為

- **問題**：AB-10 只講「缺失或為空」；資料表存在但不是 6 × 7（例如手動改動或 ingestion 中斷）時未定。
- **裁決**：共用模組回報 `incomplete`；Grading App 顯示警告、MAY 仍顯示既有資料；Dashboard 的 `/api/health` 回 503，資料 endpoint 回 503，頁面顯示錯誤狀態。（DR-3 使中斷不會留下部分寫入，此情況主要來自人為改動。）
- **依據**：Forecast Snapshot 恰 6 × 7 的定義；AB-10 明確訊息不 crash 的精神。
- **改變 accepted 語義**：否。
- **受影響**：R-SHR-2(a)、R-GA-7、R-DS-2、R-DS-3、AC-10、AC-16。

## DR-10 測試 fixture 的來源

- **問題**：AB-9 的 pytest 需要 F-D0047-091 樣本；派工指示禁止本輪擷取；CI 不能用金鑰。
- **裁決**：Executor 在 ingestion Ticket 期間以 acceptor 的 `.env` 金鑰擷取一次真實回應作為 fixture；提交前以自動檢查確認不含金鑰；MAY 為完整回應或保留結構的忠實縮減版，README 記錄取樣日期與是否縮減；反例 fixture 由正例衍生。brief §4.5 已證實回應內不含金鑰。
- **依據**：OC AB-8（ingestion 使用使用者金鑰）；派工指示的限制只及本輪；R-TC-5 離線測試。
- **改變 accepted 語義**：否。
- **受影響**：R-TC-2、AC-07(d)、AC-08。

## DR-11 Grading App 只有 MVM 行為

- **問題**：A3 說本機 Streamlit「does not need the ENHANCED map」；CONTEXT 說「no enhanced features」；是否禁止？
- **裁決**：Grading App MUST NOT 包含 Taiwan Map 與 `Select Date`，MUST NOT 依賴 folium／streamlit-folium。理由：OC §2.2 把 ENHANCED 限定「只在部署的 dashboard」；讓 Grading App 保持海報可逐字對應的評分產物，避免 scope class 混淆。
- **依據**：OC §2.2、§2.4 A3；Bindings §2.4「維持明確的 scope class 標示」。
- **改變 accepted 語義**：否。
- **受影響**：R-GA-9、AC-26、INV-9。

## DR-12 AB-1 的驗證時點與 Vercel 設定

- **問題**：AB-1 要求公開 URL；RB-1 使 production 只在 acceptor 合併後更新；Vercel preview 部署可能受 deployment protection 保護（需登入）。
- **裁決**：AC-15 以「受審 commit 的 Vercel 部署、不需登入可存取」為 PASS；用 preview 或 production 由 acceptor 的 Vercel 設定決定（前置條件）。合併後對 production URL 重跑 smoke 記為 release evidence，不是 work item 或 Spec 的完成條件。
- **依據**：OC AB-1；Bindings §5 release gate；治理 §3.8「run completion、work item completion、phase acceptance 與 release authorization 分別陳述」。
- **改變 accepted 語義**：否。
- **受影響**：R-DS-9、AC-15、Spec §6、§9 前置 #3。

## DR-13 Workflow 的範圍限制

- **問題**：CI workflow 必須放在 repo 根 `.github/workflows/`（RB-5，見 derivation record B-1）；一旦 acceptor 授權，workflow 對其他單元的影響應多小？
- **裁決**：workflow MUST 以路徑過濾只在 `home_work_01/**` 與其自身變動時觸發，名稱識別本單元；smoke 為獨立 `workflow_dispatch` workflow；兩者都不對其他單元或 root 檔案觸發。
- **依據**：RB-5 的精神（不影響單元外）；CLAUDE.md「處理某週任務時只修改該週目錄」。
- **改變 accepted 語義**：否（授權本身仍待 acceptor）。
- **受影響**：R-TC-6、R-TC-7、R-ENV-3、AC-20、AC-29。

## DR-14 OPTIONAL 不 derive

- **問題**：OC §2.2 的 OPTIONAL（排程更新、非必要工程改良）要不要進 Spec？
- **裁決**：不 derive；列於 Spec §8。日後要做由 DA 另行 derive（仍在 OC 內，不需 acceptor），且不得成為本 Spec 的完成條件。
- **依據**：OC §1「任何 optional／reference 項目都不得成為完成條件」；Q3。
- **改變 accepted 語義**：否。
- **受影響**：Spec §8。

## DR-15 海報建議結構與範例畫面的強度

- **問題**：A.6 的 `fetch_weather.py`／`parse_weather.py`／`database.py` 是「專案結構建議」；A.4 畫面範例的圖表標題、線條顏色、預設選「中部地區」是「範例」。
- **裁決**：三個階段可辨識為 SHOULD（可用建議檔名或清楚命名的模組，README 對應）；圖表標題 `Temperature Forecast – <Region>` 與 MaxT 紅／MinT 藍為 SHOULD；預設選項為第一個 Region（SHOULD）。MUST 的只有老師以「需求」列出的項目與明確點名的檔名（`app.py`、`data.db`、`requirements.txt`、`README.md`）。
- **依據**：REQUIREMENTS.md 轉寫原則「需求強度沿用原文用語」；OC §2.1。
- **改變 accepted 語義**：否。
- **受影響**：R-ING-6、R-GA-3、R-GA-4、Spec §9。

## DR-16 無效值的處理

- **問題**：brief §6.7 採用 Part B 的「可設定的無效值解析」；F-D0047-091 樣本未出現缺值；缺值時怎麼辦？
- **裁決**：無法解析或屬可設定無效值集合的值視為缺漏 → 該縣市日不完整 → ingestion 失敗並指名縣市與日期；不得以其他期間或其他縣市補值，不得改變分母。
- **依據**：OC §2.3 驗證要求「縣市缺漏須明確報錯，不得默默改變分母」。
- **改變 accepted 語義**：否。
- **受影響**：R-DER-4、R-DER-6、AC-09(3)。

## 總結

十六條裁決皆為治理 §5.3 第 2 類（不改變 Outcome Contract 草稿所載語義的 derived contract 設計與 clarification），不觸發 acceptor 核准。與 Spec 一起生效；Spec 條文與本紀錄不一致時以 Spec 為準並回報 DA 修正。
