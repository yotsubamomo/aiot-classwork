# Decision record — #77 R1-F3：最後一個候選邊界之後提出的取消（`home_work_02/`，HW2 V2 Enhance）

- **紀錄類型**：Design Authority decision record（治理 §2.4、§3.6、§5.3 第 2 類；Bindings b5 §2.4、§7）。
- **日期**：2026-10-22
- **Run**：`run-20261022-hw2-v2-enhance`（Orchestrator＝root session `37216426-f292-44f9-bad1-e2d862e7b8f1`；依治理 §2.4 直接派 DA）。
- **來源**：#77 R1 audit record [`../audit/issue-77-c1-r1.md`](../audit/issue-77-c1-r1.md)（committed `c5a04e0`，VERDICT BLOCKING）finding **R1-F3**（Medium，blocking；§7 指定修正方向的 authority＝Design Authority）與觀察 O-3。
- **Outcome Contract**：[`../outcome-contract.md`](../outcome-contract.md) §5（V2，接受基準 `d7f02d4179d2cb5c2ecf0c39a4643a6ef8287907`）與 §5.2 CC-V2-1；§1–§4（V1）仍有效。
- **相關紀錄**：[`decision-20261022-issue77-resource-limits.md`](decision-20261022-issue77-resource-limits.md)（C1-R1、C1-R3、C1-R4；本紀錄與它併用）；[`derivation-SPEC-V2.md`](derivation-SPEC-V2.md)（§0、§4 B-3、§7.2 H-3、H-4、H-5(d)）；[`decision-20261022-issue75-lasso-early-stop.md`](decision-20261022-issue75-lasso-early-stop.md)（R4-2 原因如實、R4-5 測試只擴充）；Executor worklog [`../worklog/issue-77.md`](../worklog/issue-77.md) §4 D-1。
- **Subject**：branch `home_work_02-v2-enhance`，實作 subject `5219f89`（`9d5a840` 起只有紀錄 commit；撰寫時 HEAD `c5a04e0`）。
- **Binding**：`gov-design-authority`，有效 mapping `claude-opus-5-5`／`high`（沒有 escalation、沒有替代）。撰寫前我自行讀取本 assignment 的 transcript（agentId `ac84eb317f169a98b`，與 resource-limits 紀錄同一 assignment 的續派）：觀測到 `('claude-opus-5-5', 'high')` 47 則，單一元素。全程核對由派工者依 Bindings §3.6 執行。
- **Capability escalation**：不提出。E-DA/D1 不成立：Reviewer 列出的兩個方向中，只有一個與全部 accepted 文字相容（第 3 節），可以裁決。E-DA/D2 不成立：本問題是新問題；R1 對我先前 C1-R1～C1-R4、C2-R1～C2-R3 的裁決沒有推翻或爭議（R1 §4 記為「符合」或據以判定）。
- **獨立性**：R1 的敘述與探測數字、Executor D-1 都當作待驗證主張；第 2 節的程式事實是我自己讀碼所得。本紀錄不審查實作。

## 1. 問題

`5219f89` 在最後一個候選邊界之後，依序做 A-3 共線診斷與探索 test（winner 的 test 指標、逐筆 PI）。這段「尾段」期間：控制器的 `cancel()` 仍接受取消並回傳 `true`，頁面顯示「取消中…」與「目前的候選算完後（下一個候選邊界）停止」；但尾段沒有任何取消檢查，執行照常以 `COMPLETED` 結束並顯示全部結果。R1 量得的尾段長度從 0.3 s 到 8 s，推估在載入上限的最壞情形會到分鐘級。

accepted 的「取消請求在下一個候選邊界生效」預設後面還有候選邊界；全部候選完成之後提出的取消，契約沒有直接寫出結果。要裁決的是這段期間取消的 accepted 語義，以及 #77 必須做什麼。

## 2. 依據與事實

| 來源 | 內容 |
| --- | --- |
| Spec V2 SR-V2-03 非阻塞 | 「**探索執行期間**，頁面的輸入、下拉、**取消按鈕**與進度顯示必須保持可操作」 |
| Spec V2 SR-V2-03 可終止 | 「UI 有『取消』；取消請求在下一個候選邊界生效；取消後執行狀態為 `CANCELLED`，已算出的部分結果不呈現為結果（不顯示 winner、test、預測器），只顯示『已取消』與已完成的方法數；再次執行從頭開始」 |
| Spec V2 結果契約 | `run` 為 `COMPLETED`／`CANCELLED`／`REJECTED`；`CANCELLED` 與 `REJECTED` 沒有 `candidates`、`winners`、`test`；`CANCELLED` 由使用者動作決定，不是可重現性的對象 |
| `tickets-v2.md` 調整 B；#77 AC | 取消「下一個候選邊界生效，不寫成瞬間終止」；執行期間 UI 可操作、取消後不呈現部分結果、重跑從頭開始；AC「不在候選中途中斷」、「按取消後在下一個候選邊界停止並顯示『已取消』與已完成方法數、沒有任何結果區塊」；What to build「在任意大小的合法資料集上都…可取消」 |
| derivation H-4、R4-2 | 畫面陳述必須屬實，不得宣稱未確立的事 |
| `decision-20261022-issue77-resource-limits` C1-R1、C1-R3 | 長的計算步驟本身可接受；執行進行中（含取消中）的進度要即時 |

我讀碼（`5219f89`）確認：`explore_engine.js` 的取消只在候選邊界檢查；最後一個邊界之後（約第 1385–1414 行）依序 `emit('diagnostic')`、`dependencySteps()`、判定 `REJECTED`／winners、`testSteps()`，之後直接回傳 `COMPLETED`，期間沒有檢查 `control.cancel`；`explore_app.js` `cancel()` 只要有進行中的執行就呼叫 `cancelActive()` 並回傳 `true`；`index.html` 第 95 行與「方法與限制」段落寫「取消在下一個候選邊界生效」。

## 3. 裁決

### CF-1 尾段仍是執行期間；取消可用，並以 `CANCELLED` 結束、不呈現任何結果

一次執行從開始到它的結果確定為止（`COMPLETED`、`REJECTED` 或 `CANCELLED`）都是「探索執行期間」，包括最後一個候選之後的共線診斷與探索 test。在這段期間收到的取消請求：

1. **必須生效**：執行以 `run = CANCELLED` 結束，結果只有 `meta` 與 `run`（沒有 `candidates`、`winners`、`test`、`dependencies` 等任何部分結果），頁面只顯示「已取消」與已完成的方法數（此時通常是全部方法與全部候選，照實顯示），沒有任何結果區塊；再次執行從頭開始。取消請求在執行結果確定前到達時，即使原本會是 `REJECTED`（`ALL_CANDIDATES_INVALID`），也以 `CANCELLED` 結束。
2. **生效時點**：尾段沒有候選邊界；accepted 的「下一個候選邊界」在這段期間的對應是**下一個步驟邊界**——進行中的共線診斷或探索 test 步驟完成時，至遲在結果交付之前。與候選相同，進行中的步驟**不要求**在中途中斷（調整 B「不寫成瞬間終止」）；在步驟內部更細的點生效也不違反契約，但不是要求。具體在哪些步驟邊界檢查是 HOW。
3. **顯示必須屬實**：取消中的說明不得在尾段寫「目前的候選算完後」；應如實說明正在進行的步驟完成後停止（或等效文字）。進度在取消中仍依 C1-R3 保持即時。`index.html` 的取消說明與「方法與限制」段落要涵蓋尾段的情形。
4. 結果已確定並交付之後，已經沒有進行中的執行，取消不適用（不是本裁決的對象）。

**理由**：

- Reviewer 的方向 (ii)「這段期間不可取消，頁面如實說明」與 Spec SR-V2-03 非阻塞的明文衝突：取消按鈕在**探索執行期間**必須保持可操作，而尾段仍在執行中；它也與 #77 What to build「在任意大小的合法資料集上都…可取消」衝突——尾段的長度隨設計矩陣變大，在大型資料上可長到與一個長候選相當，使用者在這段期間會無法終止執行。所以 (ii) 是 accepted 文字之外的例外，不是讀法；採用它屬 contract change。
- 方向 (i)（本裁決）滿足全部 accepted 文字：取消按鈕在整個執行期間可操作；取消生效後狀態為 `CANCELLED`、不呈現部分結果、只顯示已取消與完成數、重跑從頭開始（可終止條款與 AC）；不在候選中途中斷（尾段不是候選，且步驟也不要求中途中斷）；`CANCELLED` 的結果結構與契約不變量相同；`CANCELLED` 不是可重現性的對象，確定部分不受影響。「下一個候選邊界」是 accepted 文字為「何時生效」定的時點，它的作用是不切斷正在算的單位；在沒有下一個候選的尾段，把同一原則套在尾段的步驟上，是唯一同時保住「可取消」與「不瞬間終止」的讀法。
- 現行行為（接受取消、宣稱會停止、卻以 `COMPLETED` 顯示全部結果）在任何讀法下都不成立：它違反可終止條款與 AC「沒有任何結果區塊」，也違反 H-4／R4-2 的陳述屬實。
- R1 提到的「把共線診斷移到第一個候選之前」不是本問題的解：test 必須在 winner 凍結之後（Spec「凍結與 test」），所以尾段永遠存在。診斷的位置是 HOW，可以調整，但不能取代 CF-1。

### CF-2 是否改變 accepted 語義

**否**。CF-1 是 accepted 的非阻塞、可終止條款與 #77 AC 在尾段的唯一一致讀法；它不新增狀態、原因碼、AC、seam 或 gate，也不改變候選期間的取消語義、不並行規則或結果契約。屬治理 §5.3 第 2 類，不需 acceptor 核准；沒有 fail-closed 的項目。若 Executor 或 Reviewer 發現 CF-1 唯一可行的做法需要改變結果契約、狀態枚舉或候選期間的取消語義，該路徑超出本紀錄，須 route 回 Design Authority（可能需 acceptor）。

## 4. 受影響的工作與義務

| 對象 | 義務 |
| --- | --- |
| **#77**（結案前；與 R1-F1、R1-F2 的修正同一次進行） | (1) 引擎：最後一個候選之後提出的取消，在下一個步驟邊界（共線診斷或探索 test 完成時，至遲在結果交付前）生效，結果為 `CANCELLED`，結構與候選期間取消的 `CANCELLED` 相同，沒有任何部分結果；取消優先於尾段原本的 `COMPLETED` 或 `REJECTED`。(2) 控制器與頁面：尾段的取消照常可用；取消中的文字屬實（不寫「目前的候選算完後」）；`CANCELLED` 畫面沒有任何結果區塊；新提交、改目標欄或切換 problem 在尾段同樣先取消、等它停止，再開始新的執行（不並行）。(3) `index.html` 第 95 行的取消說明與「方法與限制」段落涵蓋尾段；worklog D-1 依本紀錄更正。(4) 證據（Executor self-verification；做法由 Executor 決定）：Node 以 `diagnostic` 事件時與探索 test 期間注入取消 → `CANCELLED`、沒有 `candidates`／`winners`／`test`／`dependencies`，之後重跑從頭開始且確定部分與未取消相同；全部候選無效的資料在尾段取消 → `CANCELLED`；候選期間的既有取消測試結果不變（R1 O-3；V2 測試只擴充，R4-5）；瀏覽器在尾段按取消 → 「已取消」、沒有結果區塊。全部 pytest 與 Node 測試通過、0 skipped；A-3 sha256 與 V1 區塊不變。(5) ACCEPTANCE V2-29、V2-30 的陳述與修正後的證據一致。(6) 修正由 #77 的 R2 依本紀錄核對（Bindings §5；治理 §3.8） |
| **#78** | README 與報告的探索模式限制說明（#78 既有 AC）中，取消的描述與 CF-1 一致：取消在下一個候選邊界生效，全部候選完成後則在進行中的步驟完成時生效，取消後不顯示任何結果 |
| **Spec Integration Audit（Spec V2）** | 在整合 subject 上核對尾段取消（H-3、H-4、H-5(d)） |
| **Run record** | Orchestrator 記錄本紀錄路徑，並把它與 `decision-20261022-issue77-resource-limits.md` 一起放入 #77 targeted correction 與 R2 的 pack |
| **Outcome Contract、Brief、Spec、tickets、GitHub issues** | 不修改 |

## 5. Evidence

- 讀取：`audit/issue-77-c1-r1.md`（第 3、4、5 節相關列，第 6 節 R1-F1～R1-F3 與觀察，第 7 節 routing）；`d7f02d4` 的 Spec V2 SR-V2-03、結果契約、可重現性、「凍結與 test」；`tickets-v2.md` 調整 B；`gh issue view 77`（body sha256 `c9b79356…90fe`，先前已核對）；worklog D-1；本 assignment 先前讀取的治理與 Bindings 條文。
- 讀碼：`assets/explore_engine.js` 第 1295–1312、1378–1416 行；`assets/explore_app.js` 第 570–580 行；`index.html` 第 93–96、234–236 行。
- 寫入的檔案只有本紀錄；沒有修改契約、Spec、票、實作或測試；沒有 commit。
