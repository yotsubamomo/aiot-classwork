# docs/governance

本 repo 採用的治理規範與 Project Bindings。只有 governance flag 為 on 的範圍（目前是 `home_workNN/`）需要讀這裡；flag 的定義見 [`project-bindings.md`](project-bindings.md) 第 0 節。

| 檔案 | 內容 |
| --- | --- |
| [`project-bindings.md`](project-bindings.md) | 本 repo 的 Project Bindings：適用範圍、權限來源、角色與模型、lane、assurance、紀錄位置。**從這裡開始讀。** |
| [`minimal-operational-governance-v2.0.md`](minimal-operational-governance-v2.0.md) | 治理本文（normative authority）的快照。 |
| [`references/model-profile-default-v2.2.md`](references/model-profile-default-v2.2.md) | 角色與模型對應、replacement policies、binding verification 的預設。 |
| [`references/implementation-profile-impl-default-v2.md`](references/implementation-profile-impl-default-v2.md) | Executor 與 Reviewer 的實作 HOW。 |
| [`references/orchestrator-contract-orch-default-v2.md`](references/orchestrator-contract-orch-default-v2.md) | Formal lane 的 Orchestrator 控制面 HOW。 |

四份規範文件是 Notion「Minimal Governance — Reusable Package v2.0」的快照，不是 authoritative source；來源、md5 與轉換方式寫在各檔檔頭。六個角色的 agent definitions 在 [`.claude/agents/`](../../.claude/agents/)，檔名以 `gov-` 開頭。
