# Project Bindings — aiot-classwork

本檔是本 repo 依 Minimal Operational Governance v2.0 §5.1 宣告的 Project Bindings：哪些範圍採用治理，以及採用範圍內的權限來源、角色與模型、lane、assurance、工具與紀錄位置。

- **Bindings 版本**：b2（2026-09-24）
- **生效條件**：acceptor 把引入本檔的 PR 合併進 `main`，即代表接受並授權本檔全部內容（含第 2.5 節的 standing authorizations）。合併前本檔只是提案。
- **優先順序**（治理 §5.3）：治理本文 ＞ 本檔 ＞ Accepted Work Contract ＞ Implementation Profile ＞ Orchestrator Contract ＞ Runtime 工具。Root `CLAUDE.md` 的其他規則在治理啟用的範圍內視為本檔的一部分；與治理 MUST 衝突時以治理為準。

## 0. 適用範圍（governance flag）

| 範圍 | governance |
| --- | --- |
| `weekNN/`（DIC，課堂實作） | off |
| `home_workNN/`（作業） | on |
| Root 與跨單元檔案（`CLAUDE.md`、`AGENTS.md`、`docs/`、`.claude/`、`.agents/` 等） | off |

- **off**：不採用治理，只適用 root `CLAUDE.md`（Codex 為 `AGENTS.md`）的規則，不需讀本目錄。
- **on**：該範圍內的每個 work item 都適用治理本文全部的 MUST／SHOULD／MAY 與本檔。
- flag 沒有中間狀態，不能只關掉部分規則；lane（Lightweight／Formal）由治理 §3.3、§3.6 與第 4 節判定，不由 flag 決定。
- 一個工作同時動到 on 與 off 範圍時，on 範圍內的部分依治理處理；改到單元目錄外的檔案另受第 2.6 節 RB-5 約束。
- 變更 flag 是 Bindings 變更：只在 work item 之間切換，並在第 9 節留下版本、依據與授權；新設定不自動適用進行中的工作（治理 §5.3）。

## 1. Governance adoption

採用 **Minimal Governance — Reusable Package v2.0**：

| Artifact | 採用版本 | Overrides | 本 repo 快照 |
| --- | --- | --- | --- |
| Minimal Operational Governance | v2.0（Adopted／Frozen 2026-09-22） | — | [`minimal-operational-governance-v2.0.md`](minimal-operational-governance-v2.0.md) |
| Reference Model Profile | `default` `v2.2`（Adopted／Frozen 2026-09-23） | 見第 3 節（`executor` mapping override） | [`references/model-profile-default-v2.2.md`](references/model-profile-default-v2.2.md) |
| Implementation Profile | `impl-default` `v2`（Adopted／Frozen 2026-09-22） | none | [`references/implementation-profile-impl-default-v2.md`](references/implementation-profile-impl-default-v2.md) |
| Reference Orchestrator Contract | `orch-default` `v2`（Adopted／Frozen 2026-09-22） | none | [`references/orchestrator-contract-orch-default-v2.md`](references/orchestrator-contract-orch-default-v2.md) |

- **權威位置**：四份文件的 authoritative source 是 package 作者 repo 內的 Markdown（各快照檔頭列出路徑與 md5），不在本 repo。本 repo 的快照取自 Notion 發布版，作為日常工作用的副本；發現與 authoritative source 不一致時，以 authoritative source 為準並更新快照。
- Implementation Profile 與 Orchestrator Contract 內文引用的是凍結當時的 Model Profile `default／v2`；本專案 pin 的是 `default／v2.2`，實際 mapping 以第 3 節為準。
- **變更 authority**：acceptor（第 2.1 節）。Governance、本檔、profiles 的任何變更都依治理 §5.3 留下版本、依據與授權，記在第 9 節。

## 2. Authority sources

### 2.1 Acceptor

本 repo 擁有者（GitHub `yotsubamomo`）是唯一的人類 acceptor，沒有指定其他人類代理。Outcome Contract 的接受與授權、boundary re-authorization、第 2.6 節的 reserved boundaries，都只能由 acceptor 在對話中明確指示或在紀錄上簽署。Agent 代寫的接受紀錄不等於取得授權（治理 §5.3）。

### 2.2 上位契約

`home_workNN/doc/requirement/` 內老師提供的題目、講義與規格（含其轉寫檔）是該作業的上位契約，對所有 Agent 唯讀。Outcome Contract 不得超出上位契約。

### 2.3 Outcome Contract

- 每份作業在開始實作前，先有一份 Outcome Contract：`home_workNN/doc/governance/outcome-contract.md`。
- 內容須滿足治理 §3.1 七項 properties：intent／outcome、scope 與 non-scope、acceptance boundary（可觀察的 PASS／FAIL 與證據要求）、authority／authorization、relevant context、assurance path（lane 與 audit）、stable reference（檔案 commit）。
- 檔尾附 **接受紀錄**：acceptor 的原始指示（引用原文）、日期、所接受的檔案 commit SHA。沒有接受紀錄的 Outcome Contract 不得啟動 Formal run，也不得開始實作。
- Lightweight 工作的 Outcome Contract 可以就是 acceptor 在對話中的直接指示（治理 §1.2、§3.5），由 Executor 原文記入 worklog 的 Contract reference。

### 2.4 老師需求與契約邊界

Root `CLAUDE.md` 的「不要自行補出老師沒有提出的要求」，在治理範圍內依下列方式落實：

- 每份 Outcome Contract 的 constraints 都包含：**MVM 必須完整滿足第 2.2 節的上位契約**；acceptor 明確授權的 ENHANCED／OPTIONAL 範圍可以超出老師撰寫的需求，但必須維持明確的 scope class 標示，且不得取代、弱化或被呈現為老師要求的行為。未經 acceptor 授權而新增老師沒有提出的功能或要求，屬於超出 Outcome Contract scope，依治理 §1.2 由 acceptor 重新授權。
- 老師需求有多種解讀、且選擇會改變交付內容或評分對象（例如 `home_work_01` 的 Part A 與 Part B 要做哪一份）時，屬於 scope 問題：在 Outcome Contract 接受前以 Grill 與 acceptor 確認，寫進 Outcome Contract。執行中才發現的，先 route 至 Design Authority 作 boundary determination；DA 無法確立在 boundary 內時 fail-closed 至 acceptor（治理 §1.2、§1.5）。
- 已接受範圍內、只影響實作的語義問題，由 Design Authority 以 decision record 裁決（治理 §3.6-A），不回問 acceptor。

### 2.5 Standing authorizations

以下由 acceptor 宣告，隨本檔生效；撤銷方式是修改本節並記入第 9 節。範圍只限 governance on 的單元，且只在有已接受的 Outcome Contract 時適用。

| ID | 涵蓋 | 排除 |
| --- | --- | --- |
| SA-1 | 依 `docs/conventions/git-commit-rules.md` 建立 topic branch、在 topic branch 上 commit，並 push topic branch 到 `origin`。 | 在 `main` 上 commit；force push；刪除或改寫既有歷史。 |
| SA-2 | 從 topic branch 對 `main` 開 Pull Request，PR 描述依 git 規則撰寫。 | 合併 PR（見 RB-1）。 |

### 2.6 Reserved boundaries

治理 §5.2 採 opt-in；本專案保留下列決定與動作給 acceptor，Agent 遇到時只停止受影響路徑並依治理 §1.5 寫 stop report：

| ID | 保留的決定／動作 |
| --- | --- |
| RB-1 | 合併任何分支進 `main`（`main` 同時是 GitHub Pages 的發布來源）。 |
| RB-2 | 繳交作業或任何對外提交。 |
| RB-3 | 申請、輪替或填寫 API key 等憑證；第三方帳號操作。金鑰只能放在未追蹤的本機 `.env`，任何時候都不得進 git、log、前端程式或文件。 |
| RB-4 | 任何需要付費的動作（付費方案、付費 API 額度）。 |
| RB-5 | 修改該單元目錄以外的檔案（root、其他單元），以及修改 `doc/requirement/` 內的上位契約。 |
| RB-6 | 破壞性或不可逆的 git 操作：force push、改寫已 push 的歷史、刪除非本次 run 建立的分支。 |

**不保留**（依治理 §5.2 預設，由 Outcome Contract 的授權涵蓋）：Spec review、獨立的 implementation authorization。要改成保留，在本表加一列並記入第 9 節。

## 3. Agent definitions 與 Model Mapping Profile

### 3.1 有效 mapping

採用 `default` `v2.2`，唯一的 mapping override 是 `executor`（見表後說明）。六個治理角色的 definition 與 `executor` fallback 的 definition 放在 `.claude/agents/`：

| Identifier | Definition | Model | Effort | Replacement |
| --- | --- | --- | --- | --- |
| `design_authority` | [`gov-design-authority`](../../.claude/agents/gov-design-authority.md) | `claude-fable-5-1` | `xhigh` | R-DA |
| `executor` | [`gov-executor`](../../.claude/agents/gov-executor.md) | `claude-opus-5-5`（override） | `high` | override fallback，再 R-EX（不含 Codex，見 3.2） |
| `executor`（fallback） | [`gov-executor-fallback`](../../.claude/agents/gov-executor-fallback.md) | `claude-opus-4-8` | `high` | 只在替代 `gov-executor` 時派工 |
| `primary_reviewer` | [`gov-primary-reviewer`](../../.claude/agents/gov-primary-reviewer.md) | `claude-opus-5-5` | `xhigh` | R-PR（不含 Codex） |
| `alternate_reviewer` | [`gov-alternate-reviewer`](../../.claude/agents/gov-alternate-reviewer.md) | `claude-fable-5-1` | `xhigh` | R-AR（不含 Codex） |
| `final_adjudicator` | [`gov-final-adjudicator`](../../.claude/agents/gov-final-adjudicator.md) | `claude-fable-5-1` | `xhigh` | R-FA |
| `orchestrator` | [`gov-orchestrator`](../../.claude/agents/gov-orchestrator.md) | `claude-opus-4-8` | `high` | R-OR |

**`executor` override（b2）**：model 由 Profile 預設 `claude-opus-4-8` 改為 `claude-opus-5-5`，effort 維持 `high`。Override fallback 列只有 `claude-opus-4-8`／`high`，以 `gov-executor-fallback` 派工。依 Model Profile §3 共同規則 2，實際替代順序是 `claude-opus-4-8`／`high`，再接 Profile R-EX 列；R-EX 列中的 Opus 5.5 就是 primary 本身、Codex 未宣告（3.2），兩者略過，剩下 `claude-fable-5-1`／`high`。

Replacement 順序與規則見 Model Profile §3：只能依當次錯誤或當下可用性證據替代，不得憑記憶或前次 session 的狀態跳過；每次替代記錄原 mapping、替代 mapping、證據與 model diversity 是否改變。沒有 reusable subagent 被宣告（Model Profile §7）。Mapping 變更 authority 為 acceptor。

### 3.2 Codex

Codex **未宣告可用**：不作任何角色的 override，也不列入 fallback；Model Profile §3 fallback 列中的 Codex 一律略過。要讓 Codex 參與，先在本節宣告其 model／version、effort 對應與 binding 驗證方式，並記入第 9 節（Model Profile §6）。

### 3.3 主 session 的角色

- **Orchestrator** 由 acceptor 開一個主 session 擔任：啟動前把 session 模型設為 `claude-opus-4-8`、effort `high`，然後以 Orchestrator Contract §3 的啟用句指定，並讓它先讀 `.claude/agents/gov-orchestrator.md`。`gov-orchestrator` 不以 subagent 派工。
- **Lightweight direct execution**：主 session 的模型與 effort 符合 `executor` mapping 時，可以自己擔任 Executor；不符合時，主 session 只負責派工與 routing，實作交給 `gov-executor` subagent。主 session 不得以不符 mapping 的 binding 冒充 Executor（治理 §2.2）。

### 3.4 Binding verification（Model Profile §5 的 Claude Code 機制）

- 每個 definition 檔的 frontmatter 綁定完整 model id 與 effort，不使用 `inherit`。
- 不設定會覆寫角色綁定的全域 subagent model（例如 `CLAUDE_CODE_SUBAGENT_MODEL` 環境變數）。
- 每次派工後，從 harness 紀錄核對實際 assignment：`~/.claude/projects/<專案 slug>/<session-id>/subagents/` 內，`agent-<agentId>.meta.json` 的 `agentType` 是 definition 名稱，`agent-<agentId>.jsonl` 各 assistant 訊息的 `message.model` 與 `effort` 是實際 model 與 effort。三者都要與第 3.1 節一致。
- 主 session（Orchestrator 或 direct execution 的 Executor）以同一 session 目錄上層的 session transcript 核對 `message.model` 與 `effort`。
- 核對結果以「agentId＋observed model／effort」寫進 worklog 或 audit record 的 binding 欄位。不符合的 assignment 依治理 §2.2 修復或依 replacement 替代，不得記為合格的 execution、review 或 adjudication。

核對指令（`<session-dir>` 換成實際 session 目錄）：

```bash
python - "<session-dir>" <<'EOF'
import json, pathlib, sys
for meta in sorted(pathlib.Path(sys.argv[1], "subagents").glob("agent-*.meta.json")):
    agent_type = json.loads(meta.read_text(encoding="utf-8")).get("agentType")
    seen = set()
    for line in meta.with_name(meta.name.replace(".meta.json", ".jsonl")).open(encoding="utf-8"):
        d = json.loads(line)
        m = d.get("message")
        if isinstance(m, dict) and m.get("model"):
            seen.add((m["model"], d.get("effort")))
    print(meta.name.replace(".meta.json", ""), agent_type, sorted(seen))
EOF
```

### 3.5 Independent dispatch 機制（治理 §2.3）

正式 audit 與裁決由 Orchestrator 或 direct execution 的主 session 透過 Claude Code 的 Agent tool 派工，`subagent_type` 指定 `gov-primary-reviewer`、`gov-alternate-reviewer` 或 `gov-final-adjudicator`。四項 properties 的滿足方式：

1. **Independent context**：非 fork 的 subagent 從空白 context 開始，不繼承派工者的對話。派工內容只放 bounded pack：Outcome Contract、Spec／Ticket、worklog、受審 subject（branch 與 commit SHA）的**路徑與識別**，不放 Executor 的結論或摘要。審查與裁決一律不得使用 fork 型 subagent。R2 可延續同一 reviewer 的 R1 context（以 SendMessage 續派同一個 agent），但 MUST 重讀修正後的檔案與 diff。
2. **Verifiable binding**：依第 3.4 節核對。
3. **Autonomous access**：reviewer 與 adjudicator 有 Read、Grep、Glob、Bash，可自行讀取整個 repo、git 歷史並執行測試；bounded pack 只是入口。
4. **Self-written record**：reviewer／adjudicator 以自己的 Write 工具把 record 寫到第 7 節的位置；派工者只能原樣 commit，不得改寫、刪減或決定是否記錄。Subagent transcript 內的 Write 呼叫即為作者證據。

以下一律只算 self-verification，不得記為正式 audit：Executor session 內的 fork 型 subagent 或 code-review 類 skill、未綁定 `gov-*` definition 的一般 agent、由 Executor 轉述的 review 結論。

### 3.6 目前狀態

機制已宣告，**尚未在本 repo 實測**。第一次正式 audit 或 Orchestrator activation 前，須完成第 8.2 節的 dry-run；結果不符時先修正本節或依 replacement 處理，再開始正式工作。治理 §5.4 禁止以文字宣稱尚未具備的 binding 能力。

## 4. Lane policy

| 工作 | 預設 lane |
| --- | --- |
| 作業主體：依上位契約交付的實作 | **Formal**（Spec＋Tickets＋Orchestrator）。作業主體通常需要多個 execution units 與 dependencies（治理 §3.6-C）。 |
| 單元 `README.md`、`CONTEXT.md`、文件與不改變交付行為的修正 | Lightweight |
| 已結案工作之後的單點修正 | Lightweight，作為新的 work item；需要 acceptor 的直接指示作為其 Outcome Contract |
| 通知、進度同步、文件維護等行政作業慣例 | Lightweight（治理 §3.6-B 的六項條件） |

- 模糊或有爭議的分類由 Design Authority 判定，並留 decision record。
- 預設分類不取代治理 §3.3 的 eligibility：Lightweight 工作中第一個需要對 intent、scope、acceptance、authority 作假設之處，就是 routing condition。
- 不得把需要 Formal 管理的作業主體拆成多個 Lightweight 指示來執行（治理 §3.3）。

## 5. Assurance policy

- **Formal**：每個 Ticket 的 independent audit 與每份 Spec 的 Spec Integration Audit 都必須執行（治理 §4.1、§4.7）。
- **Lightweight audit 預設**：不要求 independent audit。worklog 如實標示「完成且依 policy 未要求 independent audit」，不得寫成 audit PASS。
- **Lightweight audit 觸發條件**：acceptor 要求；變更涉及下列高風險類別；Design Authority 裁決要求。
- **高風險類別（初始候選）**：治理 §5.1 規定由 Design Authority 決定。下列為初始候選，第一次 Formal activation 前須由 Design Authority 以 decision record 確認或修改：
  - H-1 憑證與機密：API key 是否可能進入瀏覽器端程式、git、log 或文件。
  - H-2 老師指定的介面或資料格式：指定的檔名、資料表結構、API endpoint、輸出格式。評分直接依賴這些項目。
- **Integration／release gates**：release 指合併進 `main`（RB-1，保留給 acceptor）。請 acceptor 合併前須具備：
  - Formal：全部 Ticket 依 Orchestrator Contract §7 結案、每份 Spec 的 Spec Integration Audit 已 closure、Design Authority phase acceptance 已完成。
  - 單元 `README.md` 的安裝與執行步驟已實際跑過，結果與證據記在 worklog。
  - 沒有追蹤中的機密：`git ls-files` 不含 `.env`，diff 內沒有金鑰字串。
- **單 Ticket fast path**（治理 §4.7）：不採用；每份 Spec 都另派 Spec Integration Audit。
- **Model diversity**：因第 3.1 節的 `executor` override，Executor 與 Primary Reviewer 預設同為 `claude-opus-5-5`，Model Profile §4 的 cross-model 預設在本專案不成立。依 Profile §4 這仍合法：diversity 是偏好，不是治理 §2.3 的 independence。Diversity 依該次實際的 Executor 與 Primary Reviewer model 判定，兩者相同時，須在 audit record 的 independence 說明（治理 §4.6）記錄 `diversity_lost`；Executor 改用 fallback `claude-opus-4-8` 時 diversity 恢復。本專案沒有要求恢復 diversity 才能 audit 的類別。

## 6. Skills and runtime

- **Implementation HOW**：`impl-default` `v2`，overrides none。
- **Control-plane HOW**（只在 Formal）：`orch-default` `v2`，overrides none。並行度 1（逐張 Ticket 執行）。
- **Harness**：Claude Code（desktop app 或 CLI），Windows。派工用 Agent tool，角色 definition 在 `.claude/agents/gov-*.md`。新增或修改 definition 後要重開 session 才會載入，並依 Orchestrator Contract §11 checkpoint。
- **工作 skills**：`/to-spec`、`/to-tickets`、`gh` CLI（見 `docs/agents/issue-tracker.md`）與其他已安裝的 skills 只提供 HOW，不因被呼叫而取得設計、接受或核准權（治理 §3.4）。
- **Git**：依 `docs/conventions/git-commit-rules.md`；commit message 與 PR 描述不加 Claude 標記。
- **Recovery**：依 Orchestrator Contract §8 與治理 §1.5，從第 7 節的紀錄 re-ground；對話 context 只是 cache。

## 7. Work records

每個 governance on 的單元：

```text
home_workNN/doc/
├── requirement/            # 上位契約（老師原文與轉寫），唯讀
├── spec/                   # Spec（derived contract）
├── ticket/                 # Ticket 索引；Ticket 本體在 GitHub Issues
├── acceptance/             # 驗收對照
└── governance/
    ├── outcome-contract.md # Outcome Contract 與 acceptor 接受紀錄
    ├── decisions/          # DA 的 derivation／decision records、FA 的 rulings
    ├── worklog/            # 每個 work item 一份
    ├── audit/              # Reviewer 自寫的 audit records
    └── run/                # Orchestrator run records
```

| 紀錄 | 位置與命名 |
| --- | --- |
| Outcome Contract | `doc/governance/outcome-contract.md`；同一作業有多份時加後綴 |
| Spec | `doc/spec/`（沿用既有慣例） |
| Ticket | GitHub Issues；Issue 內引用所屬 Spec 與 worklog 路徑。`doc/ticket/` 只放索引 |
| Derivation record | `doc/governance/decisions/derivation-<spec>.md`（Spec 與其 Tickets 的 derivation 都記在這裡） |
| Decision record | `doc/governance/decisions/decision-<YYYYMMDD>-<slug>.md` |
| FA ruling | `doc/governance/decisions/ruling-<YYYYMMDD>-<slug>.md` |
| Worklog | Formal：`doc/governance/worklog/issue-<n>.md`；Lightweight：`doc/governance/worklog/<YYYYMMDD>-<slug>.md`。續接 session 更新同一份 |
| Audit record | Ticket：`doc/governance/audit/issue-<n>-c<cycle>-<r1\|r2\|alt>.md`；Spec Integration Audit：`doc/governance/audit/spec-<spec>-c<cycle>-<r1\|r2\|alt>.md` |
| Run record | `doc/governance/run/run-<YYYYMMDD>-<slug>.md` |

- 資料夾在真的產出該類紀錄時才建立。
- `doc/governance/**` 是 **record-only paths**：只改這些路徑的 delta 不影響受審 subject 的 identity（Orchestrator Contract §7 P7）。
- 紀錄只放文件；實作、資料與測試留在單元根目錄或既有位置。

## 8. 採用時的處理

### 8.1 進行中的工作（治理 §5.3）

- `week02/`：governance off，不受影響。
- `home_work_01/`：本檔生效時，沒有任何在治理下進行中的 work item。已存在的老師文件、`doc/requirement/REQUIREMENTS.md` 轉寫與本機 `.env` 都是採用前的輸入。治理從本檔生效後第一個 work item 開始適用：先與 acceptor Grill 出 Outcome Contract 並取得接受紀錄，再依第 4 節進入 lane。採用前已產生的 spec 草稿可作為 Design Authority 的輸入，但須重新 derive 並附 derivation record 才成為有效 Spec。

### 8.2 第一次正式 audit 或 Orchestrator activation 前

| # | 項目 | 狀態 |
| --- | --- | --- |
| 1 | 治理快照與本檔合併進 `main` | 本 PR |
| 2 | 六個角色 definition 存在於 `.claude/agents/` | 本 PR |
| 3 | 重開 Claude Code session，確認 `gov-*` definitions 已載入 | 待辦 |
| 4 | Binding dry-run：對六個 `gov-*` 各派一次不做事的任務，用第 3.4 節指令核對 `agentType`、model、effort，結果記在 `docs/governance/binding-verification.md` | 待辦 |
| 5 | Design Authority 以 decision record 確認第 5 節的高風險類別 | 待辦（第一次 Formal activation 前） |
| 6 | 該作業的 Outcome Contract 有 acceptor 接受紀錄 | 每份作業各自處理 |

## 9. 變更紀錄

| 版本 | 日期 | 變更 | 依據 | 授權 |
| --- | --- | --- | --- | --- |
| b1 | 2026-09-23 | 初版：`home_workNN/` 採用 Minimal Governance — Reusable Package v2.0，`weekNN/` 與 root 不採用；宣告第 1–8 節全部 bindings。 | acceptor 2026-09-23 指示：導入治理原則並以 flag 控制啟用，DIC 不使用，採用 Notion 的 Minimal Governance — Reusable Package v2.0。 | 待 acceptor 合併引入本檔的 PR 後生效 |
| b1（合併前修訂） | 2026-09-23 | 第 2.4 節 scope 規則改為：MVM 必須完整滿足上位契約；acceptor 授權的 ENHANCED／OPTIONAL 可超出老師撰寫的需求，須明確標示且不得取代、弱化或冒充老師要求的行為。 | acceptor 2026-09-23 於 `home_work_01` grill 中裁決，並依 RB-5 授權此最小修改。 | 隨 b1 一同待合併 |
| b2 | 2026-09-24 | 第 3.1 節 `executor` mapping override：model 由 `claude-opus-4-8` 改為 `claude-opus-5-5`（effort `high` 不變）；新增 override fallback `claude-opus-4-8`／`high` 與其 definition `gov-executor-fallback`；第 1 節 override 標示與第 5 節 model diversity 相應更新。其他角色 mapping、replacement policy、lane、assurance、audit flow 與 implementation method 不變。 | acceptor 2026-09-24 指示：「Primary Executor：Opus 4.8 → Opus 5.5」「Executor fallback：Opus 4.8」，其餘全部維持現狀；本輪只是 project configuration／model-mapping 調整，不觸發 implementation audit。 | 待 acceptor 合併引入本變更的 PR 後生效；不適用生效前已開始的 work item（治理 §5.3），變更時沒有 open 的 issue 或 PR。第一次以 b2 mapping 派 Executor 前，須完成 `binding-verification.md` b2 節的 dry-run |
