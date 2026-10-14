# docs/governance

本 repo 採用的治理規範與 Project Bindings。只有 governance flag 為 on 的範圍（目前是 `home_workNN/`）需要讀這裡；flag 的定義見 [`project-bindings.md`](project-bindings.md) 第 0 節。

| 檔案 | 內容 |
| --- | --- |
| [`project-bindings.md`](project-bindings.md) | 本 repo 的 Project Bindings：適用範圍、權限來源、角色與模型、lane、assurance、紀錄位置。**從這裡開始讀。** 第 1 節列出哪些 package 檔案是生效的規範。 |
| [`Minimal_Governance_Reusable_Package_v2.2_2026-10-12b/`](Minimal_Governance_Reusable_Package_v2.2_2026-10-12b/Minimal_Governance_Reusable_Package_v2.2/README.md) | Minimal Governance — Reusable Package v2.2 的位元複本（以 package 內的 `MD5SUMS`、`SHA256SUMS` 核對），不在本 repo 修改。只有 Bindings 第 1 節列出的四份是生效規範：Minimal Operational Governance v2.2、Model Profile `default` v2.5（連同其引用的 v2.4 章節）、`impl-default` v2、`orch-default` v2.2；其他檔案只供參考。 |
| [`binding-verification.md`](binding-verification.md) | `gov-*` definitions 的 binding dry-run 紀錄。 |

六個角色、`executor` fallback 與兩個 bounded assignments（`gov-investigator`、`gov-bounded-worker`）的 agent definitions 在 [`.claude/agents/`](../../.claude/agents/)，檔名以 `gov-` 開頭。

## 舊版快照

Bindings b1–b3 採用的 Package v2.0 快照（`minimal-operational-governance-v2.0.md`、`references/model-profile-default-v2.2.md`、`references/implementation-profile-impl-default-v2.md`、`references/orchestrator-contract-orch-default-v2.md`）已在 b4 移除，不再是生效規範。`home_work_01/` 在 b1–b3 下留下的紀錄仍引用這些路徑；需要時從 git 歷史讀取，例如：

```bash
git show b265766:docs/governance/minimal-operational-governance-v2.0.md
```
