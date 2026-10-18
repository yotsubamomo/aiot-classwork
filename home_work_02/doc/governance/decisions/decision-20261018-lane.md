# Decision record — HW2 的 lane（`home_work_02/`，現行 Outcome Contract）

- **紀錄類型**：Design Authority decision record（治理 §3.3、§3.6；Bindings b5 §4）
- **日期**：2026-10-18
- **對象**：由已接受的 Brief（`dff7c55c`；[`../outcome-contract.md`](../outcome-contract.md)）與 [`../../spec/SPEC.md`](../../spec/SPEC.md) rev 3（#59；[`derivation-SPEC.md`](derivation-SPEC.md)）界定的 HW2 整體工作
- **取代**：r4 下的 `decision-20261014-lane.md` 不沿用（處置紀錄 N-3）
- **Binding**：`gov-design-authority`，`claude-opus-5-5`／`high`（Bindings §3.1 預設 mapping，沒有 escalation，沒有替代）。由派工者依 Bindings §3.6 核對。

## 1. 問題

HW2 的整體工作應走 Lightweight 還是 Formal？OC §2 預期是 Formal，由 DA 判定。

## 2. 裁決：**Formal**（Spec＋Tickets＋Orchestrator）

理由（lane 依預期的**整體**結果判定，治理 §3.3）：

1. **治理 §3.6-C 成立**：整體工作要分成多個彼此相依的 execution units，大致是：資料與分割 → 特徵選擇路徑與 CV → OLS fit、PI 與授權模型的 test 評估 → `model_data` 匯出 → dashboard 與 Node 測試 → 報告 → 打包與整合驗收。後段依賴前段的產物與介面；部分路徑要等 acceptor 的輸入（ChatGPT PDF、NotebookLM 材料、學號設定、RB-5 的 root 兩列）；Backward SFS 與 RFE 在 fold-internal 下約要計算 6 倍，很可能跨越多個 Executor／Reviewer session。
2. **治理 §3.6-B 也成立**：`model_data` 契約是 Python 與 dashboard 兩側共同依賴的新介面，invariant 與 gate（BR-01 的 test 暴露規則、逐筆重算）沒有更早的 accepted baseline。Spec rev 3 就是它的設計基線。
3. **Lightweight 不適用**：工作無法在一個 execution unit 內完成；把它拆成多個 Lightweight 指示來規避 Formal 要求是禁止的（治理 §3.3；Bindings §4）。

## 3. 執行配置

| 項目 | 內容 |
| --- | --- |
| Spec | 一份：Spec rev 3，derivation 見 `derivation-SPEC.md` |
| Tickets | 由 DA 在 `derivation-SPEC.md` §9 derive。MATT `/to-tickets` 只產出 ticket 草稿；票的 authority 來自 DA 的 derivation，不來自 skill（治理 §3.4）。DA 要逐張核對草稿：AC 只能引用 Spec，不得重新定義；要帶入 T-義務、OV 項目、高風險類別與 F-1 的處理，之後才算 derive 完成 |
| Orchestrator | 由 acceptor 在主 session 指定的 root role session（Bindings §3.5），`claude-opus-5-5`／`medium`；E-OR 的 (M1)／(D1) 成立時為 `high`（Bindings §3.1、§3.2）。開始前先讀 `.claude/agents/gov-orchestrator.md`，以 run record `doc/governance/run/run-<YYYYMMDD>-<slug>.md` 作為 work identity；依 orch-default v2.2，並行度 1（Bindings §6）。不以 subagent 派工 |
| Executor | `gov-executor`（Opus 5.5／`high`，O-1），fallback 為 `gov-executor-fallback` |
| Audit | 每張 Ticket 做 independent audit（R1／R2／Alternate／FA）；另做 Spec Integration Audit（治理 §4.7）。有多張票時不適用單 Ticket fast path（Bindings §5） |
| Phase acceptance | 由 DA 執行，必須引用已 closure 的 Spec Integration Audit record |
| 合併與發布 | 現行 OC 沒有 SA-3 opt-in，合併進 `main` 屬 RB-1，由 acceptor 決定。依 N-10，PR checks 不是 Ticket 的條件 |
| 高風險與 assurance | [`decision-20261018-high-risk-categories.md`](decision-20261018-high-risk-categories.md) |
| 結案後的單點修正 | Lightweight，作為新的 work item，以 acceptor 的直接指示作為其 Outcome Contract（Bindings §4 第 4 列）；audit 是否觸發依高風險紀錄第 4 節 |

## 4. Orchestrator activation 的前置條件

| # | 條件 | 狀態（2026-10-18） | Authority |
| --- | --- | --- | --- |
| 1 | acceptor 授權 `/to-tickets` 與實作（OC §2 目前只授權到接受紀錄與 `/to-spec`） | 未授權 | acceptor |
| 2 | Spec rev 3 的 derivation record | 完成（`derivation-SPEC.md`） | DA |
| 3 | 現行契約下的 lane 與高風險紀錄 | 完成（本紀錄與高風險紀錄） | DA |
| 4 | Tickets derive 完成，並填寫 `derivation-SPEC.md` §9 | 未開始 | DA（`/to-tickets` 為 HOW） |
| 5 | F-1（Ridge／Lasso 的 test 評分）：acceptor 已決定，或 Tickets 明確排除該路徑 | 待 acceptor | acceptor |
| 6 | Bindings §8.2 #3：`model: fable` 的 binding 實測仍未完成（2026-10-14 遇到 HTTP 429）。r4 時 acceptor「不阻擋」的決定沒有沿用（處置紀錄 N-2）。Bindings 要求 activation 前完成 | 未完成 | 先重跑 probe（不需要 acceptor）；Fable 仍不可用時，是否視為阻擋由 acceptor 決定 |
| 7 | Push 的授權狀態：acceptor 2026-10-18 明示不授權 push；SA-1 涵蓋 push，但被這次的指示排除 | 待 acceptor 釐清 | acceptor（不阻擋本機工作，只影響 push 與 PR） |
| 8 | Disposition 中的 GitHub 操作（#50–#56 關閉） | 完成（派工者以 `gh` 核對） | — |

## 5. 是否改變 accepted 語義

否。Lane 是 DA 的判定（治理 §3.6；Bindings §4），沒有新增 scope、audit round 或 acceptor gate；第 4 節的 acceptor 項目都來自既有的 OC §2 與 Bindings。

## 6. 受影響的 work items

#59（Spec）；即將 derive 的 Tickets；之後的 Orchestrator run。
