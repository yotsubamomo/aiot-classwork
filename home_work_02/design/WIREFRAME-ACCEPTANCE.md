# HW2 Dashboard Wireframe — Final Acceptance Record

- **Verdict**：**UI DESIGN ACCEPTED**（acceptor，2026-10-18）。
- **接受的設計基準**：Wireframe **v0.2**，commit **`0eb862594c8e38616534e9dd1be388e18ad01aa8`**（branch `home_work_02-regrill`）。檔案 blob：
  - `wireframe/index.html` `54fedde191567500836450bc0b49aa4cd3a0b1b0`
  - `wireframe/wireframe.css` `ad4b5dc4c7ce8d693d528600bed0c2b1c78fa491`
  - `wireframe/wireframe.js` `4da1681022f2bd607b4ed66bb0e84edeb90140aa`
  - `wireframe/mock-data.js` `e011ff24bff0c50fb138880a9c6477ec4aa8b511`
  - 設計說明 `UI-DESIGN-NOTES.md`、檢查表 `WIREFRAME-REVIEW-CHECKLIST.md`、設計系統 `design-system/hw2-king-county-dashboard/MASTER.md`（同一 commit）。
- **地位**：後續 Dashboard 實作的 **UI Design Reference**。功能與統計的權威仍是已接受的 Brief（`doc/brief/BRIEF.md` @ `dff7c55c`）與 Spec rev 3（`doc/spec/SPEC.md`，issue #59）；wireframe 與它們不一致時以 Brief／Spec 為準。
- **Mock data**：只供展示；不是正式模型數據，不是統計驗證證據。Executor 不須、也不應直接複製 `mock-data.js`／`wireframe.js` 的模擬預測計算。
- **驗收方式**：acceptor 親自開啟 wireframe 目視檢查（整體視覺、頁面配置、資訊層級、主要操作流程），非自動化驗證。
- **記錄者**：無角色主 session，依 acceptor 指示逐字轉錄；效力來自 acceptor 原文。

## Acceptor 原文（2026-10-18，逐字）

> HW02 Wireframe v0.2 — Final Acceptance
> Verdict：UI DESIGN ACCEPTED
> 我已親自開啟並目視檢查 Wireframe v0.2，確認整體視覺設計、頁面配置、資訊層級及主要操作流程符合預期。
> 正式接受目前的 Wireframe v0.2，作為後續 Dashboard Implementation 的 UI Design Reference。
> 確認以下事項：
>
> 1. 七項 UI 決策全部接受，維持目前 v0.2 設計。
> 2. Training CV／Test Evaluation 的分層方式符合需求。
> 3. Mock Data 僅供展示，不能作為正式模型數據或統計驗證證據。
> 4. 後續實作以 Accepted Brief、Spec rev 3 為功能與統計權威，以 Wireframe v0.2 為 UI 設計參考。
> 5. 不要求 Executor 直接複製 Mock JavaScript 的預測計算邏輯。
>
> 尚未完成的驗證
> 以下仍屬 Open Verification Items，不得標示為 PASS：
>
> * 真正斷網環境下的 `file://` 操作
> * 真實手機及觸控操作
> * Safari／Firefox 相容性
> * 螢幕閱讀器與完整 Accessibility
> * 色彩對比量測
> * 正式 Dashboard 的逐筆 PI 渲染效能（SR-09）
>
> 請將這些項目保留至後續 Tickets 與 Acceptance Criteria。

## Open Verification Items（帶入 `/to-tickets` 與 ACCEPTANCE.md 的規劃輸入）

| # | 項目 | 狀態 | 對應 Spec | 預期落點 |
| --- | --- | --- | --- | --- |
| OV-1 | 真正斷網環境下以 `file://` 開啟 ZIP 解壓後的 dashboard，必要區塊與互動正常、零對外請求 | OPEN | Dashboard 離線驗收（BR-04）、人工檢查表 | 正式 dashboard 的票與打包／驗收票；ACCEPTANCE.md 離線一節 |
| OV-2 | 真實手機與觸控操作（選單、k 切換、預測器輸入、散佈圖拖曳與雙指縮放） | OPEN | 版面、SR-09 | 正式 dashboard 的票；人工檢查表 H |
| OV-3 | Safari／Firefox 相容性 | OPEN | 參考環境為 Chrome／Edge；其他瀏覽器屬延伸檢查 | 正式 dashboard 的票（非阻擋，記錄結果） |
| OV-4 | 螢幕閱讀器與完整 accessibility（朗讀順序、`aria-expanded` 播報、`aria-live` 預測結果、表單錯誤關聯） | OPEN | 無障礙規則；人工檢查表 H | 正式 dashboard 的票；ACCEPTANCE.md |
| OV-5 | 色彩對比量測（文字 ≥ 4.5:1、非文字 ≥ 3:1） | OPEN | 設計系統 token；人工檢查表 H | 正式 dashboard 的票 |
| OV-6 | 正式 dashboard 的逐筆 PI 渲染效能：首次繪製 ≤ 3 秒、互動 ≤ 1 秒、不抽樣、量測紀錄 | OPEN | SR-09 (a)(b)(f)(g) | 正式 dashboard 的票；ACCEPTANCE.md 效能一節 |

**Gate 分類（acceptor 2026-10-18 F-5；原文見 `doc/governance/outcome-contract.md` §4 AD-1）**：OV-1、OV-6 為硬性 PASS／FAIL gate；OV-2 的 required gate 是 DevTools 375／768 px 無水平溢出且主要功能可操作（真實觸控 best effort）；OV-3 的 required gate 是 Chrome 或 Edge PASS（Firefox／Safari best effort）；OV-4 的 required gate 是鍵盤、focus、label、選單狀態與基本語意（螢幕閱讀器 best effort）；OV-5 的 required gate 是文字 ≥ 4.5:1、大字 ≥ 3:1 且不只靠顏色。Best-effort 項目無環境時記 NOT TESTED。

這些項目在 wireframe 階段**不得標示為 PASS**；wireframe 的自動／半自動檢查結果（檢查表 §L）只證明原型在本機 Chromium 以本機伺服器開啟時的行為。

## 本紀錄之後

- 下一步依已確認的流程是 MATT `/to-tickets`；本紀錄寫入時**尚未授權**。
- Push、merge、deployment、實作都未授權。
