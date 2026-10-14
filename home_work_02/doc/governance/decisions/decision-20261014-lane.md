# Decision record — Lane 判定（`home_work_02/`，HW2 Outcome Contract 整體）

- **紀錄類型**：Design Authority decision record（治理 §2.1「lane eligibility／promotion」、§3.3、§3.6；Bindings b5 §4「模糊或有爭議的分類由 Design Authority 判定，並留 decision record」；Outcome Contract §6、§8 #5）
- **日期**：2026-10-14
- **對象**：HW2 Outcome Contract（[`../outcome-contract.md`](../outcome-contract.md)）整體預期結果。Accepted normative 內容＝第 1–8 節於 commit `e2153254ccf7a97475d1c22e10d6a1e0717c5497`；接受紀錄＝第 9 節於 commit `370c0ae1bf40385baa1d954c6585d1c175b4124b`。本 DA 以 `git show` 核對兩個 commit 的第 1–8 節內容完全相同（擷取段落的 sha256 皆為 `1cb963156f8ee8c288d79b5ee6a8735248b49efe6f8eb22a7e7a4db5ad85baa6`）。
- **適用 Bindings**：b5（`main` `5ebcc58`）
- **執行角色**：`gov-design-authority`。Binding 由派工者依 Bindings §3.6 核對並記錄；本紀錄不自證 binding。本題沒有提出 capability escalation（E-DA 的 D1、D2 都不成立，見第 5 節）。

## 1. 問題

HW2 Outcome Contract 整體應走 Lightweight 還是 Formal（Spec＋Tickets＋Orchestrator）？Outcome Contract §6 寫的「預期為 Formal」只是起草建議，由 DA 判定。Bindings b5 §4 採 Lightweight 優先，Formal 只在治理 §3.6-B 或 §3.6-C 成立時使用。

## 2. 裁決

**Formal**（Spec＋Tickets＋Orchestrator），依據是治理 §3.6-B 與 §3.6-C 各自成立；任一項單獨成立就足以排除 Lightweight。

### 2.1 §3.6-C 成立：需要多個 execution units、dependencies 與跨 session 的 run-to-completion

依「預期的整體結果」（治理 §3.3；Bindings §4）判定，完成條件 S2（OC §3.2）需要以下彼此相依的單元：

| 單元 | 依賴 |
| --- | --- |
| 資料載入與 checksum、分區、folds | — |
| 前處理與五個 candidate procedures、nested CV、選模與凍結 | 資料／分區 |
| Conformal 校準、Test 評估、預測圖、Deployment 函式 | 凍結 predictor |
| Notebook（CRISP-DM 六階段）、結果 artifact、乾淨環境重跑 | 全部模組 |
| 報告（模組結果的數值與圖） | 結果 artifact |
| acceptor 證據的整合（ChatGPT PDF、NotebookLM 摘要） | 報告；**acceptor 輸入**（OC §3.3） |
| 打包與 ZIP 核對 | 報告 PDF；**學號**（acceptor 輸入） |

- 三項 acceptor 輸入（ChatGPT PDF、NotebookLM 原始材料、學號）的到達時間不受 Agent 控制。S1 不需要它們，S2 需要。所以工作必然跨多個 session 執行，且須在等待期間只停止受影響的路徑（OC §3.2、§3.3；治理 §1.5 第 4 項）。這正是 Orchestrator 的 run-to-completion 與 routing 職責。
- Formal 下每個 Ticket 的 independent audit 與 Spec Integration Audit（治理 §4.1、§4.7）也構成跨多個 Executor／Reviewer session 的協調。

### 2.2 §3.6-B 成立：語義必須被設計

- **Parent 留給下游的必要選擇**（§3.6-B 第三項）：OC §5 明列八項「Spec 需處理的已知設計事項」，由 DA 決定：完全共線、`date`／`zipcode`、轉回 USD 的偏誤修正、tie-break、離群值、報告 PDF 的產生方式、資料取得方式、acceptor 原始材料的存放位置。若不先設計，Executor 必須自行假設 acceptance 相關語義，這違反 Lightweight eligibility（治理 §3.3：不得對 intent、scope、acceptance、authority 作任何假設）。
- **其他工作將依賴的新設計基線**（§3.6-B 第一項）：模組介面（data、selection、modeling、evaluation、conformal）、candidate procedure 的定義、fold 的共用方式、結果 artifact 與報告數值的單一來源、凍結與 Test 評估的順序證據。Notebook、報告、打包都依賴它們，OC 只給了語義邊界，沒有可錨定的設計。

### 2.3 為何不選 Lightweight

- Bindings §4 第一列（「契約清楚，且能在一個 execution unit 內完成」）的兩個條件都不成立：OC §5 刻意把設計留給 Spec，且工作無法在一個 execution unit 內完成到 S2（受 acceptor 輸入阻擋）。
- 以 §3.6-A 的 decision record 解決 §5 的設計事項，也不能讓工作留在 Lightweight，因為 §3.6-C 獨立成立。
- 不得把整體工作拆成多個 Lightweight 指示來規避 Formal 要求（治理 §3.3；Bindings §4）。

## 3. 是否改變 accepted 語義

**否。** 本裁決只決定 lane。OC §6 已把 lane 寫為「預期為 Formal，由 Design Authority 判定」。本裁決確認該預期，不改變 OC 的 intent、scope、constraints 或 acceptance semantics。

## 4. 後果與受影響工作

| 項目 | 內容 |
| --- | --- |
| Spec | 同日 derive：[`../../spec/SPEC.md`](../../spec/SPEC.md) v1.0，derivation record [`derivation-SPEC.md`](derivation-SPEC.md)。 |
| Tickets | **本次不 derive**（派工指示）；由後續 DA 派工自 Spec v1.0 derive。 |
| Audit | 每個 Ticket 做 independent audit；Spec 做 Spec Integration Audit；Spec 只有一張 Ticket 時可用 fast path（Bindings §5）。 |
| Orchestrator | Activation 前提依 orch-default v2.2 §3：OC 接受紀錄（已有）、Spec 與 Tickets 及 derivation record、Bindings 就緒（§8.2 #3 的 Fable probe 依 OC §9 acceptor 決定不阻擋 pre-Spec readiness）、高風險類別（[`decision-20261014-high-risk-categories.md`](decision-20261014-high-risk-categories.md)）。Designation 由 acceptor 作出。 |
| 進行中的 work item | 無。`home_work_02/` 目前只有文件，沒有實作。 |

## 5. Capability escalation 檢查

本題只有一個合理結論：§3.6-B 與 §3.6-C 都可從 OC 原文直接判定，不存在兩個後果實質不同、且以現有證據無法裁決的設計（E-DA/D1 不成立）；本題沒有先前的 DA 決定被推翻或爭議（E-DA/D2 不成立）。

## 6. Evidence

- OC 第 1–8 節（`e2153254`）：§3.2 S1–S4、§3.3 acceptor 輸入、§5 Spec 需處理的設計事項、§6 Assurance path、§8 #5；第 9 節（`370c0ae`）接受紀錄。
- 治理 v2.2 §1.5、§3.3、§3.4、§3.6、§4.1、§4.7；Bindings b5 §4、§5。
- `git show e2153254:…/outcome-contract.md` 與 `git show 370c0ae:…/outcome-contract.md` 第 1–8 節擷取比對（同一 sha256）。
