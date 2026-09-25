# Worklog — 2026-09-25 V2 Ticket derivation（Design Authority 派工）

依 Minimal Operational Governance v2.0 §3.7。

## Work performed

1. 主 session 核對前置：`main` 為 `b0642f8fec359090c772f26d37cade1438628881`（PR #34 合併，SPEC-V2 **v2.2** 為有效 derived contract）；V2 Outcome Contract ACCEPTED（candidate `69c5a04`、接受紀錄 `f853bcb`）；Bindings b3 生效；b2 executor dry-run PASS。從 `main` 建立 topic branch `home_work_01-v2-tickets`。
2. 以 SendMessage 續派同一個 Design Authority assignment（`agent-a813b9bb4bfbfd4cc`），原文轉交 acceptor 的 `/to-tickets` 指示（含十項專案限制與八項 derivation-quality check），並轉錄 `/to-tickets` 方法（垂直切片、blocking edges、issue template、`ready-for-agent`、依依賴順序發布、GitHub 原生 blocked-by）、tracker 慣例（`docs/agents/issue-tracker.md`、`triage-labels.md`）與 V1 前例（`tickets.md`、`derivation-SPEC.md` §11、Issue #24 的票體結構）。要求先重讀磁碟上的 Spec v2.2、derivation record、OC-V2、Bindings；產出 GitHub Issues、`doc/ticket/tickets-v2.md`、derivation record §15；不寫 worklog、不 commit。追加指示：只允許改 SPEC-V2 的兩處 metadata（標頭 Issue tracker 列、§10 metadata 列，版本不變），比照 V1 前例。
3. Design Authority 建立 Issues **#35–#41**（7 張，label `ready-for-agent`，GitHub 原生 blocked-by 6 條邊，單鏈 #35 → #36 → #37 → #38 → #39 → #40 → #41），寫 `doc/ticket/tickets-v2.md`，在 `derivation-SPEC-V2.md` 新增 §15（依據、分配表、覆蓋矩陣、boundary determination TB-V2-n、八項 derivation-quality check 全 PASS、evidence）與 §14 修訂列，把 SPEC-V2 標頭「Issue tracker」列改為指向 #35–#41 與索引、§10 加一列 metadata（版本仍 v2.2）。回報：無 Spec 矛盾、無 blocker；`/to-tickets` skill 檔在此環境未安裝，方法依 repo 文件與派工內容轉錄套用（與 V1 `/to-spec` 情況相同，記於 §15.1／TB-V2-12）。
4. 主 session 核對：binding；`gh issue list` 七張票皆 open、label `ready-for-agent`；API `dependencies/blocked_by` 與 DA 回報的圖一致；每張票體含 `## Blocked by` 段、金鑰格式掃描 0、模型名稱（Opus／Fable／Codex／claude-）0 命中（model-agnostic）；`git status` 只有三個允許路徑的變更；SPEC-V2 diff 只有標頭一列與 §10 一列；新檔與修改檔金鑰格式掃描 0。寫本 worklog；commit、push、開 PR（SA-1、SA-2）。未 merge（無 RB-1 授權）。

5. **依賴圖修正輪（同日，acceptor 指示；PR #42 合併前）**：acceptor 指出 #37 → #38 不是 Spec 要求的技術依賴（#38 只需要 #36 的 Now mode 基礎，不需要 #37 的 Refresh／Stale／Unavailable 語義完成），並指定新圖：#35 → #36；#36 → #37、#36 → #38；#38 → #39 → #40；#37 → #41、#40 → #41（#41 等兩個分支）。Bindings §6 並行度 1 維持，但偏好的執行順序 #35, #36, #37, #38, #39, #40, #41 只是排程偏好，不得表示為 blocked-by 邊。以 SendMessage 續派同一個 Design Authority assignment：DA 以 `gh api` 修改原生 blocked-by（刪 #37 阻擋 #38；加 #36 阻擋 #38；加 #37 阻擋 #41）、只改 #38 與 #41 票體的 `## Blocked by` 段（其餘逐字不變，DA 自行比對並修正一次 CRLF 漂移）、更新 `tickets-v2.md`（表格、執行順序圖、「7 條邊＋排程偏好」說明）與 derivation record §15（§15.1、§15.2、TB-V2-2、§15.5 第 5 項、§15.6、§14 一列）；`/to-tickets` skill 不可用的 provenance 原樣保留；重跑八項 derivation-quality check 全 PASS；票務範圍、AC／INV／high-risk 分配與 SPEC-V2 內容不變（治理 §5.3 第 2 類）。主 session 再次核對 binding、API 邊、票體 Blocked by 段、label、變更範圍、金鑰掃描，修正本檔第 3、4 項與 Decisions／Verification 的單鏈敘述（見下），commit、push，並依 acceptor 對 PR #42 的 item-specific RB-1 授權以 merge commit 合併、驗證 `main`。

## Contract reference

V2 Outcome Contract（ACCEPTED 2026-09-25，`outcome-contract-v2.md` §9）→ SPEC-V2 v2.2（EFFECTIVE，`main` `b0642f8`）→ 本次 Tickets #35–#41（derived contracts，治理 §1.2；不需 acceptor 逐張核准）。Acceptor 2026-09-25 的 `/to-tickets` 指示：「Proceed with V2 Ticket derivation using Matt's `to_tickets` skill … Do NOT start the Orchestrator. Do NOT implement. … Do NOT merge.」

## Executing role and binding reference

- 派工者：主 session（harness 紀錄 `claude-fable-5-1`／`xhigh`）；只派工、核對與紀錄，未作分解或分配裁決。
- Design Authority：`agent-a813b9bb4bfbfd4cc`，`agentType = gov-design-authority`，observed `('claude-fable-5-1', 'xhigh')`（Bindings §3.4 指令輸出；同一 assignment 自 Delta Spec derivation 起延續）。與 Bindings §3.1 的 `design_authority` mapping 一致。無 replacement。

## Decisions and assumptions

- 全部分解、分配與 boundary determination 由 Design Authority 作出並自寫於 `derivation-SPEC-V2.md` §15；主 session 未改寫、未篩選。
- Design Authority 回報：七張票皆在 Spec v2.2 boundary 內；沒有 Ticket 新增語義、AC、invariant、架構或 oracle；每條 AC-V2-01～23 有 owner；INV-V2-1～9 各有負責票且全部保留在 Spec Integration Audit；§6.3 定向 V1 重驗全部有 owner；H-1／H-2／H-3 在票體「High-risk」段可辨；未引入額外人工 gate；憑證 gate 只在 #41 的 AC-V2-17(c) 與 AC-V2-22 觀測部分（acceptor 填入 Vercel 金鑰前記 BLOCKED，不是 FAIL）；#35–#40 以本機未追蹤 `.env`（A-3）與離線樣本進行。
- 依賴圖（第 5 項修正後）為兩個分支：#35 → #36；#36 → #37 與 #36 → #38；#38 → #39 → #40；#41 被 #37 與 #40 阻擋。#40 Radar 排在 #39 圍欄之後，使對齊所需的 CRS／重投影變更能在 #40 內重驗 AC-V2-13／15。初版（第 3 項）的單鏈 #35 → … → #41 把並行度 1 的排程偏好誤寫成 #37 → #38 的技術邊，已依 acceptor 指示修正；並行度 1 下偏好的執行順序仍可為 #35, #36, #37, #38, #39, #40, #41，但那是排程偏好，不是 blocked-by 邊。

## Artifacts

| 動作 | 路徑／識別 | 作者 |
| --- | --- | --- |
| 新增 | GitHub Issues #35–#41（`yotsubamomo/aiot-classwork`，label `ready-for-agent`，原生 blocked-by 7 條邊——初版 6 條單鏈，第 5 項修正後為兩分支） | Design Authority |
| 新增 | `home_work_01/doc/ticket/tickets-v2.md` | Design Authority |
| 修改 | `home_work_01/doc/governance/decisions/derivation-SPEC-V2.md`（§15、§14 一列） | Design Authority |
| 修改 | `home_work_01/doc/spec/SPEC-V2.md`（標頭 Issue tracker 列、§10 metadata 列；版本 v2.2 不變） | Design Authority |
| 新增 | 本檔 | 主 session |

未實作、未呼叫 CWA API、未部署、未啟動 run、未動 Vercel 或 repository variables。V1 `tickets.md`、V1 Spec、兩份 Outcome Contract、Brief、`CONTEXT.md`、上位契約、程式、測試、root 檔案未變。

## Verification

- Binding：`agent-a813b9bb4bfbfd4cc gov-design-authority [('claude-fable-5-1', 'xhigh')]`。
- Issues：`gh issue list` 顯示 #35–#41 皆 open、label `ready-for-agent`；API `dependencies/blocked_by`（第 5 項修正後，主 session 逐票重查）：#36←#35；#37←#36；#38←#36；#39←#38；#40←#39；#41←#37、#40（#35 無）；與票體 `Blocked by` 段、`tickets-v2.md`、derivation record §15.2 四方一致。初版（修正前）為 #38←#37、#41←#40 的單鏈。
- 票體：七張皆有 `## Blocked by` 段；金鑰格式 0 命中；模型名稱 0 命中。
- 變更範圍：`git status --short` 只列 `doc/ticket/tickets-v2.md`（新）、`doc/governance/decisions/derivation-SPEC-V2.md`、`doc/spec/SPEC-V2.md`（3＋／1－，只有兩處 metadata）。
- 機密：新檔與修改檔金鑰格式掃描 0。
- 未執行任何程式碼測試（無實作）。

## Audit status

Not required：Ticket derivation 是 Design Authority 的設計行為；正式審查於 Formal run 中逐張 Ticket 的 audit 與 Spec Integration Audit 執行。如實標示「完成且依 policy 未要求 independent audit」。

## Remaining work

| 事項 | 阻擋原因 | 負責 |
| --- | --- | --- |
| 合併本 PR（Tickets 索引、derivation record §15、Spec metadata） | RB-1，本輪無授權 | acceptor |
| 開符合 `orchestrator` mapping 的主 session（`claude-opus-4-8`／`high`）啟動 Formal run | Bindings §3.3；session 模型 | acceptor |
| Vercel 專案環境變數填入 `CWA_API_KEY`（preview 與 production） | RB-3；只影響 #41 的 AC-V2-17(c)、AC-V2-22 觀測部分 | acceptor |
| 本機 Python 3.12、未追蹤 `.env`（#35 起，A-3） | — | acceptor（已具備） |
