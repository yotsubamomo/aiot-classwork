# Outcome Contract — HW2 Multiple Linear Regression（`home_work_02/`，re-Grill 基線）

- **狀態**：**ACCEPTED（2026-10-18）**。接受的 normative 內容是 [`../brief/BRIEF.md`](../brief/BRIEF.md)（FINAL DRAFT）於 commit **`dff7c55c70ede3dede17469a48d5a80376fda77e`**（branch `home_work_02-regrill`）的版本，連同同一 commit 的 Grill 紀錄 rev 7 與 `CONTEXT.md`。接受紀錄見第 3 節（acceptor 原文逐字）。Agent 代寫的接受紀錄不等於取得授權；效力來自第 3.1 節的 acceptor 原文（治理 §1.2、§5.3；Bindings §2.1）。
- **承載方式**：依治理 §1.2「Prompt、Task Brief … 均可承載契約」與 Bindings §2.3（Formal：`doc/governance/outcome-contract.md` 附接受紀錄），本檔**不重寫** Brief 的內容，只做兩件事：(1) 對照治理 §3.1 的七項 properties 指出 Brief 的對應位置；(2) 記錄接受。Brief 是 MATT Grill 的產物，其內部流程獨立於治理（acceptor 2026-10-18 指示）；本檔與 Brief 不一致時，以 Brief 於上列 commit 的內容為準。
- **與前一個契約的關係**：本契約取代 2026-10-14 接受的 Outcome Contract r4（branch `home_work_02-outcome-contract`，`e2153254`）作為 HW2 之後工作的 Outcome Contract。r4、其 Spec v1.1、derivation 與 decision records 保留在原 branch 作為歷史，不修改、不刪除。r4 衍生的 GitHub Issues #50–#56 的處置，由 Design Authority 在本契約下判定。
- **V2 Enhance**：**ACCEPTED（2026-10-22）**，增量 scope，不取代上列 V1 契約；接受內容是 commit **`d7f02d4179d2cb5c2ecf0c39a4643a6ef8287907`**（branch `home_work_02-v2-enhance`）的 Brief V2 rev 2（含勘誤 E-1）、Spec V2 rev 2、`tickets-v2.md` 與 issue #74–#78。接受紀錄見第 5 節。
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

## 4. 契約變更紀錄

### CC-1（2026-10-18）— F-1：Ridge／Lasso 的 Test Evaluation（APPROVED CONTRACT CHANGE）

- **性質**：治理 §5.3 第 1 類（改變 accepted 語義）。來源：Design Authority 在 [`decisions/derivation-SPEC.md`](decisions/derivation-SPEC.md) 的 boundary determination B-2／finding F-1——Spec rev 3 讓 Ridge／Lasso 在 test 上各評分一次（`metric_only`），而已接受的 Brief BR-01 第 3 點與 `CONTEXT.md` 只允許各方法 CV winner、All-in 與整體 CV winner。DA 依治理 §1.2 fail-closed 並 route 給 acceptor。
- **Acceptor 決定**：選擇 (a)，正式授權。
- **變更後的 accepted 語義**：Ridge 與 Lasso 各進行**一次**最終 Test Evaluation，只提供 USD 尺度的 MAE、MSE、RMSE、R²，作為描述性模型對照，受下列六項約束（acceptor 原文）：
  1. Ridge／Lasso 的 alpha 只能使用 Training CV 選擇。
  2. Ridge／Lasso 不參與四種特徵選擇方法及 All-in 的整體 CV winner 競爭。
  3. 每個 Ridge／Lasso 模型只允許一次最終 Test Evaluation，不得因 Dashboard 互動而重新測試。
  4. Test 結果不得回饋模型選擇、超參數調整或特徵選擇。
  5. Ridge／Lasso 仍為 metric_only，不提供 PI、Coverage 或即時預測功能。
  6. Dashboard 與報告必須清楚區分 Training CV 指標與 Test 指標，不得混用。
- **範圍限制**：只涵蓋 F-1；不擴大到其他模型、其他 test 結果或任意 k 的 test evaluation。
- **受影響文件**：`doc/brief/BRIEF.md` §5、§7（BR-01 第 3、4 點）、§14；`CONTEXT.md`（Test evaluation）；`doc/spec/SPEC.md`（rev 4 註記；metric_only 契約已存在，只補授權依據與約束）；`decisions/derivation-SPEC.md`（B-2／F-1 結案）。對進行中工作沒有影響（沒有 Tickets、實作或 evidence）。
- **Acceptor 原文（2026-10-18，逐字）**：

> F-1 Acceptor Decision：選擇 (a) — APPROVED CONTRACT CHANGE。
> 正式授權 Ridge 與 Lasso 各進行一次 Test Evaluation，僅提供 USD 尺度的 MAE、MSE、RMSE、R²，作為描述性模型對照。
> 約束如下：
>
> 1. Ridge／Lasso 的 alpha 只能使用 Training CV 選擇。
> 2. Ridge／Lasso 不參與四種特徵選擇方法及 All-in 的整體 CV winner 競爭。
> 3. 每個 Ridge／Lasso 模型只允許一次最終 Test Evaluation，不得因 Dashboard 互動而重新測試。
> 4. Test 結果不得回饋模型選擇、超參數調整或特徵選擇。
> 5. Ridge／Lasso 仍為 metric_only，不提供 PI、Coverage 或即時預測功能。
> 6. Dashboard 與報告必須清楚區分 Training CV 指標與 Test 指標，不得混用。
>
> 請依現行 MATT 與 Governance 流程：
>
> * 將本決策記錄為 F-1 的明確 contract change。
> * 修訂 Accepted Brief BR-01 第 3 點及必要的相關文字。
> * 同步 CONTEXT.md 的 Test Evaluation 定義。
> * 檢查 Spec rev 3 是否已有完整且一致的 metric_only 契約；只修正必要內容。
> * 更新 DA derivation／decision record 與需求追溯。
> * 執行必要的一致性檢查。
>
> 此授權只涵蓋 F-1 contract change 及其必要文件修訂。
> 不得自行擴大到其他模型、其他 Test 結果或任意 k 的 Test Evaluation。
> 完成後回報變更摘要及一致性檢查結果。
> 目前仍不授權 Implementation、Push、Merge 或 Deployment。

轉錄者：無角色主 session。變更的效力來自上述 acceptor 原文；本檔檔頭所列的接受內容（Brief @ `dff7c55c`）連同本變更，構成現行 accepted 語義。

### AD-1（2026-10-18）— F-5：Open Verification Items 的 gate 分類（acceptor 決定，不改變 scope）

- **性質**：acceptance boundary 的具體化（為 Wireframe Acceptance 留下的 OV-1～OV-6 定 PASS／FAIL 與 best-effort 的門檻），不新增 scope；依治理 §3.1 第 3 項由 acceptor 定義可觀察的 PASS／FAIL 語義。寫入 `doc/spec/SPEC.md` rev 5 的人工檢查表與 `design/WIREFRAME-ACCEPTANCE.md`。
- **Acceptor 原文（逐字）**：

> F-5：APPROVED
> OV-2 手機／觸控：
>
> * Required gate：Chrome DevTools 375 px／768 px 無水平溢出，主要功能可操作。
> * 真實觸控裝置有環境時補測；無環境則明確記錄 NOT TESTED。
>
> OV-3 跨瀏覽器：
>
> * Required gate：Chrome 或 Edge PASS。
> * Firefox／Safari 為 best effort，無環境不得標示 PASS。
>
> OV-4 Accessibility：
>
> * Required gate：鍵盤操作、focus visibility、正確 label、選單狀態及基本語意。
> * 螢幕閱讀器為 best effort，無環境記錄 NOT TESTED。
>
> OV-5 色彩對比：
>
> * Required gate：一般文字 ≥4.5:1、大字 ≥3:1。
> * 重要狀態與圖表不可只靠顏色辨識。
>
> OV-1 完全離線 file:// 與 OV-6 全部 Test PI 渲染效能，仍為原定硬性 PASS／FAIL gate，不降級。

### AD-2（2026-10-18）— F-3、push、`/to-tickets`（acceptor 決定）

- **F-3**：「依現行 MATT 與治理流程，對已被 N-10 取代的『本單元另設 CI』敘述，以及 CONTEXT.md 的 CV winner 詞條，進行最小編輯性修正。不得新增 CI Workflow、改變統計流程或擴大需求。」→ Spec rev 5、CONTEXT.md 已修。
- **Push**：「完成上述修訂、必要審查與本機 commit 後，授權將目前 `home_work_02-regrill` 分支以一般 fast-forward push 推送至 origin。禁止 force push、merge、deployment。Push 後確認 HEAD 一致，並同步 GitHub Issue #59。」
- **`/to-tickets`**：「完成決策同步後，正式執行 MATT `/to-tickets`。以 Accepted Brief（含 CC-1）、最新 Spec、CONTEXT、DA derivation、已接受的 Wireframe v0.2 為輸入。Tickets 必須涵蓋：Spec 全部功能與正式交付物。DA G-1～G-4。H-1～H-4 對應的 assurance requirements。OV-1～OV-6 的 gate／best-effort 分類。明確依賴、驗收標準、驗證證據與需求追溯。遵守 MATT 原生 to-tickets 流程及現行治理要求，不重新開啟已接受的設計決策。」
- **Fable probe**：「請在現行 Bindings 所要求的 Orchestrator 啟動點前完成。若失敗，保留證據並依現行規則回報，不自行豁免。」
- **未授權**：「本次不授權 Implementation 或啟動 Orchestrator。」
- 本節的授權範圍到此為止；OC §2「本次實際授權的範圍」依本節擴充為：接受紀錄、`/to-spec`、CC-1 文件修訂、F-3／F-5 修訂、fast-forward push、`/to-tickets`。

### AD-3（2026-10-18）— TK-1：GitHub Pages URL 檢查的安排（acceptor 決定）

- **背景**：DA derivation §9 finding TK-1：Brief §7／§10 要求在 GitHub Pages 網址上重做 dashboard 檢查，但 Pages 只發布 `main`，合併屬 RB-1，#67 無法執行。
- **Acceptor 原文（逐字）**：「TK-1 採 (a)：GitHub Pages URL 的檢查作為合併進 main 之後的 Lightweight work item（觸及 H-2，需 audit）；#67 與 ACCEPTANCE.md 先記 NOT TESTED（pending merge）。」
- **效果**：Pages 檢查從 #67 的完成條件移出，成為合併後的獨立 Lightweight work item（依 Bindings §4、§5：以 acceptor 的直接指示為其 Outcome Contract；觸及 H-2 → 需 independent audit）。#67 與 ACCEPTANCE.md 對該項記 NOT TESTED（pending merge）；Spec Integration Audit 與 phase acceptance 把它列為 open item，不阻擋 S2。

## 5. V2 Enhance 接受紀錄（2026-10-22）

| 項目 | 內容 |
| --- | --- |
| 狀態 | **已接受**（2026-10-22） |
| Acceptor | GitHub `yotsubamomo`，於 Claude Code 對話中以第 5.1 節原文接受 |
| 接受的內容 | commit `d7f02d4179d2cb5c2ecf0c39a4643a6ef8287907`（原文 `d7f02d4`；branch `home_work_02-v2-enhance`）的 `doc/brief/BRIEF-V2.md` rev 2（含勘誤 E-1）、`doc/spec/SPEC-V2.md` rev 2、`doc/ticket/tickets-v2.md` 與 GitHub issue #74–#78；V2 的驗收條件、四個測試 seams、依賴與 V1 保持要求。接受基準只限該 commit，不以 working tree、issue label 或之後的實作 commit 代替（原文） |
| 與 V1 的關係 | 不取代第 1–4 節的 V1 契約；V1 契約對 V1 正式分析仍有效且具權威。V2 是增量 Enhance scope，只受明確接受的 V2 覆寫約束（原文） |
| 授權 | Design Authority 派工以產生 `decisions/derivation-SPEC-V2.md`（含 lane 與高風險類別判定，涵蓋使用者提供 URL 的 fetch 能力）；兩項前提完成並驗證後，Orchestrator 續行既有 run `run-20261022-hw2-v2-enhance` 並派 #74，執行限 #74–#78 與其依賴；SA-1 下的本機 commit |
| 未授權 | push、merge、修改凍結的 V1 產物 |
| SA-3 | 原文標題為「SA-3 DECISION」，內容授權在本檔登錄 V2 接受，**沒有明確引用 SA-3 作為合併授權**，且原文明示「No push, merge … is authorized」。依 Bindings §2.5 SA-3 條件 (1)（未引用者仍屬 RB-1），V2 的合併屬 **RB-1，保留給 acceptor** |

### 5.1 Acceptor 原文（2026-10-22，逐字）

> HW2 V2 — Outcome Contract Acceptance & SA-3 Decision
> Acceptance date: 2026-10-22
> Accepted baseline commit: d7f02d4
> Accepted branch: home_work_02-v2-enhance
> ACCEPTOR DECISION: ACCEPTED
> I formally accept the HW2 V2 Enhance contract at baseline commit d7f02d4, including:
>
> 1. BRIEF-V2.md rev 2, including erratum E-1.
> 2. SPEC-V2.md rev 2.
> 3. tickets-v2.md and GitHub issues #74–#78.
> 4. The V2 acceptance criteria, four approved test seams, dependencies, and V1 preservation requirements.
> 5. The previously accepted V1 contract remains unchanged and authoritative for V1 formal analysis.
>
> SA-3 DECISION:
> Authorize registration of this V2 acceptance in the existing outcome-contract.md under the current governance rules.
> The accepted baseline is d7f02d4. Do not substitute the working-tree state, an issue label, or a later implementation commit as the acceptance basis.
> This acceptance does not supersede the V1 contract. V2 is an additive Enhance scope, subject to the explicitly accepted V2 overrides.
> DESIGN AUTHORITY AUTHORIZATION:
> Authorize dispatch of gov-design-authority to produce derivation-SPEC-V2.md against the accepted V2 Outcome Contract.
> The Design Authority must determine the applicable lane and high-risk categories using existing governance rules, including the user-supplied URL fetching capability.
> Do not presume a low-risk classification or bypass any required review.
> No separate approval is required merely to dispatch the Design Authority.
> EXECUTION AUTHORIZATION:
> After the Outcome Contract registration and Design Authority derivation are completed and validated, the Orchestrator may continue the existing run and dispatch #74, provided all other existing preconditions pass.
> Execution remains limited to accepted V2 tickets #74–#78 and their dependencies.
> Follow existing Bindings, Orchestrator Contract, independent review requirements, and evidence rules. Do not add governance rules or new approval gates.
> GIT AUTHORIZATION:
> Local changes and commits required for the accepted governance records and authorized V2 ticket execution may follow existing SA-1 rules.
> No push, merge, or modification of frozen V1 artifacts is authorized.
> If a mandatory governance precondition fails, stop and report the specific failure rather than modifying governance rules or inventing an exception.
> Please record this acceptor decision verbatim, complete the two missing preconditions, and report their validation results before dispatching #74.

轉錄者：Orchestrator session `37216426-f292-44f9-bad1-e2d862e7b8f1`，依上述原文「Authorize registration of this V2 acceptance in the existing outcome-contract.md」轉錄；接受與授權的效力來自原文，不來自本轉錄。本節不改變第 1–4 節的任何內容。
