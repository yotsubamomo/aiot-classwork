# Outcome Contract — HW2 Multiple Linear Regression（`home_work_02/`，re-Grill 基線）

- **狀態**：**ACCEPTED（2026-10-18）**。接受的 normative 內容是 [`../brief/BRIEF.md`](../brief/BRIEF.md)（FINAL DRAFT）於 commit **`dff7c55c70ede3dede17469a48d5a80376fda77e`**（branch `home_work_02-regrill`）的版本，連同同一 commit 的 Grill 紀錄 rev 7 與 `CONTEXT.md`。接受紀錄見第 3 節（acceptor 原文逐字）。Agent 代寫的接受紀錄不等於取得授權；效力來自第 3.1 節的 acceptor 原文（治理 §1.2、§5.3；Bindings §2.1）。
- **承載方式**：依治理 §1.2「Prompt、Task Brief … 均可承載契約」與 Bindings §2.3（Formal：`doc/governance/outcome-contract.md` 附接受紀錄），本檔**不重寫** Brief 的內容，只做兩件事：(1) 對照治理 §3.1 的七項 properties 指出 Brief 的對應位置；(2) 記錄接受。Brief 是 MATT Grill 的產物，其內部流程獨立於治理（acceptor 2026-10-18 指示）；本檔與 Brief 不一致時，以 Brief 於上列 commit 的內容為準。
- **與前一個契約的關係**：本契約取代 2026-10-14 接受的 Outcome Contract r4（branch `home_work_02-outcome-contract`，`e2153254`）作為 HW2 之後工作的 Outcome Contract。r4、其 Spec v1.1、derivation 與 decision records 保留在原 branch 作為歷史，不修改、不刪除。r4 衍生的 GitHub Issues #50–#56 的處置，由 Design Authority 在本契約下判定。
- **Bindings**：b5（`main` merge commit `5ebcc58eba1d776cc7380d391ced1dc503a3ee31`）。
- **Acceptor**：GitHub `yotsubamomo`（Bindings §2.1）。
- **撰寫者**：無角色主 session，依 acceptor 2026-10-18 指示「完成必要的 Brief／Outcome Contract acceptance 記錄」轉錄。

## 1. 治理 §3.1 七項 properties 在 Brief 中的位置

| Property | Brief 位置 |
| --- | --- |
| 1 Intent and outcome | §1 目標 |
| 2 Scope and boundaries | §3 範圍（必要／選配／不做）、§4–§7 的限制、§11 風險 |
| 3 Acceptance and verification | §7 的驗收條件（離線、BR-01 UI 驗收、Q43 圖）、§10 驗證與驗收、§13 Brief Review；Spec 的具體 AC 在這些邊界內 derive |
| 4 Authority and authorization | 第 2 節（本檔）；§9 acceptor 專屬輸入 |
| 5 Relevant context | §2 來源與地位、§4 資料事實、§12 HOW 清單 |
| 6 Assurance path | 第 2 節（本檔）；lane 由 Design Authority 判定 |
| 7 Stable reference | commit `dff7c55c`（本檔檔頭） |

## 2. Authority and authorization

| 項目 | 內容 |
| --- | --- |
| 接受後的授權 | 在 Brief 的邊界內，授權具相應 authority 的 Agents 規劃、分解、實作、審查、修正至 Brief §8 的交付物完成，範圍限 `home_work_02/`；root `README.md` 與 `CONTEXT-MAP.md` 的一列（Brief §8，Q39）屬 RB-5，動手前先說明並取得 acceptor 逐次授權 |
| **本次（2026-10-18）實際授權的範圍** | 只涵蓋：本接受紀錄，以及 MATT `/to-spec`。**不含** `/ui-ux-pro-max`、`/to-tickets`、實作、push、merge、deployment（acceptor 原文第 3.1 節「執行邊界」） |
| 已確認的後續工作流程（尚未授權執行） | Brief Acceptance → MATT `/to-spec` → `/ui-ux-pro-max` 產生獨立的靜態 HTML Wireframe → Wireframe Review → MATT `/to-tickets` → Implementation。Wireframe 依 Spec 設計，作為 UI 實作的參考，不得修改已接受的功能或統計要求 |
| Git | SA-1（topic branch 的 commit 與 push）、SA-2（開 PR）依 Bindings §2.5 在接受後適用；**但 acceptor 本次明示不授權 push**，所以在下一次指示前只做本機 commit。合併進 `main`：SA-3 需契約明確 opt-in——Brief 沒有 opt-in，所以合併屬 **RB-1，保留給 acceptor**，由 acceptor 逐次決定 |
| 保留給 acceptor | RB-1 合併；RB-2 iLearning 繳交；RB-3 憑證與第三方帳號；RB-4 付費；RB-5 單元外檔案與 `doc/requirement/`；RB-6 破壞性 git |
| Acceptor 輸入 | Brief §9：ChatGPT 對話 PDF、NotebookLM 原始材料、學號（已提供，追蹤檔案一律 `<學號>`）、繳交 |
| MATT skills 與治理 | `/to-spec`、`/to-tickets`、grilling 依其自身流程進行，不以治理規則重新定義其內部流程（acceptor 2026-10-18）；它們的產物進入治理後，Design Authority、Review 與授權邊界照常適用 |
| Lane 與 audit | 由 Design Authority 判定並留 decision record；高風險類別同。預期 Formal（多個相依的 execution units＋acceptor 輸入） |

## 3. 接受紀錄

| 項目 | 內容 |
| --- | --- |
| 狀態 | **已接受**（2026-10-18） |
| Acceptor | GitHub `yotsubamomo`，於 Claude Code 對話中以第 3.1 節原文接受 |
| 接受的內容 | `home_work_02/doc/brief/BRIEF.md`（FINAL DRAFT）、`home_work_02/doc/brief/HW2_Regrill_Brief_Draft_v0.1.md`（rev 7）、`home_work_02/CONTEXT.md`，於 commit `dff7c55c70ede3dede17469a48d5a80376fda77e` |
| 接受時的修訂 | 無 |
| 本次授權 | 接受紀錄＋MATT `/to-spec`（第 2 節） |

### 3.1 Acceptor 原文（2026-10-18，逐字）

> Homework02 Final Brief Draft：確認通過（ACCEPTED）。
> 接受目前 BRIEF.md FINAL DRAFT 所定義的需求、範圍、限制、交付項目與驗收意圖，包括 BR-01～BR-04 的最終處理結果。
> 請依現行 Minimal Governance 與 Project Bindings，完成必要的 Brief／Outcome Contract acceptance 記錄。
> 下一階段授權使用 MATT `/to-spec`，根據已接受的 Brief 產生 Spec。
> 補充已確認的 UI 工作流程：
> Brief Acceptance
> → MATT /to-spec
> → /ui-ux-pro-max 產生獨立的靜態 HTML Wireframe
> → Wireframe Review
> → MATT /to-tickets
> → Implementation
> Wireframe 應依 Spec 設計，作為後續 UI Implementation 的參考，不得自行修改已接受的功能或統計要求。
> 執行邊界：
>
> 1. 本次授權僅涵蓋完成必要的 Acceptance 記錄及 `/to-spec`。
> 2. `/to-spec` 與專案治理維持獨立，不以治理規則重新定義 MATT Skill 的內部流程。
> 3. 遵守既有 Design Authority、Review 與授權邊界。
> 4. 不提前執行 `/ui-ux-pro-max`、`/to-tickets` 或 Implementation。
> 5. 不授權 Push、Merge 或 Deployment。
> 6. 若 Acceptance 記錄需要 Commit，先依現行治理確認權限，不得自行擴大授權。
>
> 完成 Spec 後，先回報產物、未解決問題及審查狀態，等待下一步指示。

轉錄者：無角色主 session。接受與授權的效力來自上述原文，不來自本轉錄。

### 3.2 本檔 commit 的權限依據

- 接受成立後，Bindings §2.5 **SA-1** 涵蓋「在 topic branch 上 commit」；本檔是 `home_work_02/doc/governance/` 內的紀錄檔，屬單元內、record-only path（Bindings §7）。
- acceptor 原文第 5 點排除 push，所以本檔只做**本機 commit，不 push**，等待下一次指示。
- 這不是對授權的擴大：SA-1 是既有的常設授權；push 與合併都未執行。
