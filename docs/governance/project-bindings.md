# Project Bindings — aiot-classwork

本檔是本 repo 依 Minimal Operational Governance v2.2 §5.1 宣告的 Project Bindings：哪些範圍採用治理，以及採用範圍內的權限來源、角色與模型、lane、assurance、工具與紀錄位置。

- **Bindings 版本**：b4（2026-10-14）
- **生效條件**：acceptor 把引入本版的 PR 合併進 `main`，即代表接受並授權本檔全部內容（含第 2.5 節的 standing authorizations）。合併前本版只是提案，b3 仍有效。
- **優先順序**（治理 §5.3；orch-default §1）：治理本文 ＞ 本檔 ＞ Accepted Work Contract ＞ Implementation Profile ＞ Orchestrator Contract ＞ Runtime 工具。Root `CLAUDE.md` 的其他規則在治理啟用的範圍內視為本檔的一部分；與治理 MUST 衝突時以治理為準。
- **整體取向：Lightweight 優先。** 本專案是個人課程作業。在治理允許的範圍內一律選最輕的做法：預設 Lightweight lane（第 4 節）、Lightweight 預設不做 independent audit（第 5 節）、bounded assignments 只採用 `investigator` 與 `bounded_worker` 兩種（第 3.4 節）、不宣告額外的 escalation trigger 或 diversity 要求。治理的 MUST 不因此放寬。

下文的 `PKG/` 指 [`Minimal_Governance_Reusable_Package_v2.2_2026-10-12b/Minimal_Governance_Reusable_Package_v2.2/`](Minimal_Governance_Reusable_Package_v2.2_2026-10-12b/Minimal_Governance_Reusable_Package_v2.2/)。

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

採用 **Minimal Governance — Reusable Package v2.2**（package 說明見 [`PKG/README.md`](Minimal_Governance_Reusable_Package_v2.2_2026-10-12b/Minimal_Governance_Reusable_Package_v2.2/README.md)）：

| Artifact | 採用版本 | Overrides | 生效檔案 |
| --- | --- | --- | --- |
| Minimal Operational Governance（normative authority） | v2.2（Adopted／Frozen 2026-10-12） | — | [`PKG/Minimal_Operational_Governance_v2.2_Candidate.md`](Minimal_Governance_Reusable_Package_v2.2_2026-10-12b/Minimal_Governance_Reusable_Package_v2.2/Minimal_Operational_Governance_v2.2_Candidate.md)（檔名沿用 Candidate 字樣，狀態以 header 為準） |
| Reference Model Profile | `default` `v2.5`（Adopted／Frozen 2026-10-11），連同其以引用方式沿用的 `default` `v2.4` 章節 | 見第 3 節（O-1、O-2、O-3） | [`PKG/references/model-profiles/default-v2.5.md`](Minimal_Governance_Reusable_Package_v2.2_2026-10-12b/Minimal_Governance_Reusable_Package_v2.2/references/model-profiles/default-v2.5.md)、[`default-v2.4.md`](Minimal_Governance_Reusable_Package_v2.2_2026-10-12b/Minimal_Governance_Reusable_Package_v2.2/references/model-profiles/default-v2.4.md) |
| Implementation Profile | `impl-default` `v2`（Adopted／Frozen 2026-09-22） | none | [`PKG/references/implementation-profiles/default-v2.md`](Minimal_Governance_Reusable_Package_v2.2_2026-10-12b/Minimal_Governance_Reusable_Package_v2.2/references/implementation-profiles/default-v2.md) |
| Reference Orchestrator Contract | `orch-default` `v2.2`（Adopted／Frozen 2026-10-12） | none | [`PKG/references/orchestrator-contracts/default-v2.2.md`](Minimal_Governance_Reusable_Package_v2.2_2026-10-12b/Minimal_Governance_Reusable_Package_v2.2/references/orchestrator-contracts/default-v2.2.md) |

- **權威位置**：package 的權威來源是 package 作者工作區的 `master_governance/`（見 `PKG/README.md`），不在本 repo。`PKG/` 是位元複本，以 `PKG/MD5SUMS`、`PKG/SHA256SUMS` 核對（2026-10-14 全部 OK）。發現與權威來源不一致時，以權威來源為準，重新放入複本並核對 hash。`PKG/` 內的檔案不在本 repo 修改。
- **只有上表的檔案是本專案生效的規範。** `PKG/` 中其他檔案——Minimal v2.1 與 orch-default v2.1 等 frozen baselines、visualization HTML、`records/` 內的採用與 review 紀錄——只供參考與追溯，不構成本專案的規則或 fallback authority。
- **版本化陳述**：impl-default v2 的 header 標 Minimal v2.0、§11 引用 Profile `default` v2；orch-default v2.2 §2 引用 Profile `default` v2.3；`default` v2.5 的 header 標 Minimal v2.1。這些是凍結當時的陳述（`PKG/README.md`「已知未處理」），本專案的實際 mapping 以第 3 節為準。
- **變更 authority**：acceptor（第 2.1 節）。Governance、本檔、profiles 與 definitions 的任何變更都依治理 §5.3 留下版本、依據與授權，記在第 9 節。

## 2. Authority sources

### 2.1 Acceptor

本 repo 擁有者（GitHub `yotsubamomo`）是唯一的人類 acceptor，沒有指定其他人類代理。Outcome Contract 的接受與授權、boundary re-authorization、第 2.6 節的 reserved boundaries，都只能由 acceptor 在對話中明確指示或在紀錄上簽署。Agent 代寫的接受紀錄不等於取得授權（治理 §5.3）。

### 2.2 上位契約

`home_workNN/doc/requirement/` 內老師提供的題目、講義與規格（含其轉寫檔）是該作業的上位契約，對所有 Agent 唯讀。Outcome Contract 不得超出上位契約。

### 2.3 Outcome Contract

- **Lightweight**：acceptor 在對話中的直接指示就是 Outcome Contract（治理 §1.2、§3.5），條件是它不需要對 intent、scope、acceptance、authority 作任何假設（治理 §3.3）。Executor 在 worklog 的 Contract reference 原文引用該指示與日期。
- **Formal**，或直接指示不足以確定上述四項時：開始實作前先有一份 `home_workNN/doc/governance/outcome-contract.md`（同一作業有多份時加後綴），內容滿足治理 §3.1 七項 properties，檔尾附**接受紀錄**：acceptor 的原始指示（引用原文）、日期、所接受的檔案 commit SHA。沒有接受紀錄的 Outcome Contract 不得啟動 Formal run，也不得開始實作。

### 2.4 老師需求與契約邊界

Root `CLAUDE.md` 的「不要自行補出老師沒有提出的要求」，在治理範圍內依下列方式落實：

- 每份 Outcome Contract 的 constraints 都包含：**MVM 必須完整滿足第 2.2 節的上位契約**；acceptor 明確授權的 ENHANCED／OPTIONAL 範圍可以超出老師撰寫的需求，但必須維持明確的 scope class 標示，且不得取代、弱化或被呈現為老師要求的行為。未經 acceptor 授權而新增老師沒有提出的功能或要求，屬於超出 Outcome Contract scope，依治理 §1.2 由 acceptor 重新授權。
- 老師需求有多種解讀、且選擇會改變交付內容或評分對象時，屬於 scope 問題：在 Outcome Contract 接受前以 Grill 與 acceptor 確認，寫進 Outcome Contract。執行中才發現的，先 route 至 Design Authority 作 boundary determination；DA 無法確立在 boundary 內時 fail-closed 至 acceptor（治理 §1.2、§1.5）。
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
| RB-3 | 申請、輪替或填寫 API key 等憑證；第三方帳號操作。金鑰只能放在兩個授權位置：(a) 未追蹤的本機 `.env`；(b) 部署平台（Vercel）專案的環境變數——只由 acceptor 親自填入，Agents 不得填入、讀出、印出或匯出其值；部署的應用程式只在伺服器端執行期讀取，不得傳給前端、不得寫入 build／runtime log 或 evidence。無論位置為何，金鑰任何時候都不得進 git、log、前端程式或文件。 |
| RB-4 | 任何需要付費的動作（付費方案、付費 API 額度）。 |
| RB-5 | 修改該單元目錄以外的檔案（root、其他單元），以及修改 `doc/requirement/` 內的上位契約。 |
| RB-6 | 破壞性或不可逆的 git 操作：force push、改寫已 push 的歷史、刪除非本次 run 建立的分支。 |

**不保留**（依治理 §5.2 預設，由 Outcome Contract 的授權涵蓋）：Spec review、獨立的 implementation authorization。要改成保留，在本表加一列並記入第 9 節。

## 3. Agent definitions 與 Model Mapping Profile

### 3.1 有效 mapping

採用 `default` `v2.5`，overrides 為 O-1、O-2、O-3（O-3 見第 3.4 節）。六個治理角色與 `executor` fallback 的 definition 放在 `.claude/agents/`：

| Identifier | Definition | Model | Effort | 依據 |
| --- | --- | --- | --- | --- |
| `design_authority` | [`gov-design-authority`](../../.claude/agents/gov-design-authority.md) | `claude-opus-5-5` | `high` | Profile 預設 |
| `executor` | [`gov-executor`](../../.claude/agents/gov-executor.md) | `claude-opus-5-5` | `high` | **O-1** |
| `executor`（fallback） | [`gov-executor-fallback`](../../.claude/agents/gov-executor-fallback.md) | `claude-opus-4-8` | `high` | O-1 的 fallback（＝Profile F-EX\* 列） |
| `primary_reviewer` | [`gov-primary-reviewer`](../../.claude/agents/gov-primary-reviewer.md) | `claude-opus-5-5` | `xhigh` | Profile Claude path 首項；Codex 未宣告，屬 resolution（Profile §7＝v2.4 §6 條件 1），不記 substitution |
| `alternate_reviewer` | [`gov-alternate-reviewer`](../../.claude/agents/gov-alternate-reviewer.md) | `claude-opus-5-5` | `xhigh` | Profile 預設 |
| `final_adjudicator` | [`gov-final-adjudicator`](../../.claude/agents/gov-final-adjudicator.md) | `claude-opus-5-5` | `xhigh` | Profile 預設 |
| `orchestrator` | [`gov-orchestrator`](../../.claude/agents/gov-orchestrator.md)（root role session，不以 subagent 派工） | `claude-opus-5-5` | `medium` | Profile 預設 |

**O-1 `executor` mapping override**：Profile 預設 Sonnet 5.5／`medium` 改為 `claude-opus-5-5`／`high`。依據：沿用 b2 的 acceptor 決定（Executor 用 Opus 5.5／`high`、fallback Opus 4.8／`high`），並使 acceptor 平常的主 session（Opus 5.5／`high`）能直接擔任 Lightweight Executor（第 3.5 節），不必另派 subagent。Fallback 只有 `claude-opus-4-8`／`high`（`gov-executor-fallback`）；Profile 不允許 Executor 用 Fable，列耗盡即依治理 §1.5 recovery。Profile 的 E-EX 不適用：其 escalated mapping 等於 O-1。要改回 Profile 預設，刪除 O-1 並記入第 9 節。

**O-2 fallback 列的 runtime override**（Profile §4.2 末句：runtime 無法派工某 model 時由 Bindings override）：Agent tool 只能以 definition frontmatter 或 `model` alias（`opus`、`sonnet`、`haiku`、`fable`）指定 model，沒有對應 Opus 4.8 的 alias。因此被派工角色的 fallback 列略過 Opus 4.8（`executor` 除外，它有 `gov-executor-fallback`）。有效 fallback 列：

| Policy | 有效 mapping | Fallback（依序） | 派工方式 |
| --- | --- | --- | --- |
| F-DA | Opus 5.5／`high` | Fable 5.1／`high` | `gov-design-authority`＋`model: fable`、`effort: high` |
| F-DA\* | Fable 5.1／`xhigh`（E-DA） | Opus 5.5／`xhigh` | `gov-design-authority`＋`effort: xhigh` |
| F-EX\*（O-1） | Opus 5.5／`high` | Opus 4.8／`high` | `gov-executor-fallback` |
| R-PR | Opus 5.5／`xhigh` | Fable 5.1／`xhigh` | `gov-primary-reviewer`＋`model: fable` |
| F-AR | Opus 5.5／`xhigh` | 無（列耗盡 → 治理 §1.5 recovery） | — |
| F-AR\* | Fable 5.1／`xhigh`（E-AR） | Opus 5.5／`xhigh` | `gov-alternate-reviewer`（frontmatter 即此 mapping） |
| F-FA | Opus 5.5／`xhigh` | Fable 5.1／`xhigh` | `gov-final-adjudicator`＋`model: fable` |
| F-FA\* | Fable 5.1／`xhigh`（E-FA） | Opus 5.5／`xhigh` | `gov-final-adjudicator`（frontmatter 即此 mapping） |
| F-OR／F-OR\* | Opus 5.5／`medium`（`high`） | 依 Profile 列：Opus 4.8 → Sonnet 5.5／`high` | Root session 以完整 model id 啟動（`claude --model claude-opus-4-8 --effort <effort>` 或 `/model`、`/effort`），不受 alias 限制 |
| F-BW（`standard`，O-3） | Sonnet 5.5／`high` | Opus 5.5／`high` | `gov-bounded-worker`＋`model: opus` |
| F-BW（`mechanical`，O-3） | Haiku 5.5／`high`（qualification 通過後；之前依 `standard` 派工） | Sonnet 5.5／`high` → Opus 5.5／`high` | `gov-bounded-worker`（Sonnet）；`gov-bounded-worker`＋`model: opus` |
| F-IN（O-3） | Sonnet 5.5／`high` | Opus 5.5／`high` | `gov-investigator`＋`model: opus`、`effort: high` |
| F-IN\* | Opus 5.5／`high`（E-IN，O-3） | Sonnet 5.5／`high` | `gov-investigator`（frontmatter 即此 mapping） |

替代規則見 Profile §4.1（＝v2.4 §3 共同規則 1–5 加規則 6–7）：只能依當次錯誤或當下可用性證據替代，不得憑記憶或前次 session 跳過；每次替代記錄原 mapping、替代 mapping、證據引用（Profile §8）。Overload／rate-limit 不另宣告 bounded retry：harness 自身重試後仍回傳的 429／529 即構成當次可用性證據。Mapping 變更 authority 為 acceptor。

### 3.2 Capability escalation

採用 Profile §3，限於下列 identifier；trigger、範圍與規則依 Profile §3.1 E-1～E-10 與治理 §2.5。Orchestrator 或派工的 session 只機械套用 trigger，不判斷能力是否足夠。

| ID | Identifier | Escalated mapping | 本專案採用的 trigger | 派工方式 |
| --- | --- | --- | --- | --- |
| E-DA | `design_authority` | Fable 5.1／`xhigh` | (D1)、(D2)。(M1) 不採用：本檔不宣告任何類別的 DA 決定使用 Fable | `gov-design-authority`＋`model: fable`、`effort: xhigh` |
| E-AR | `alternate_reviewer` | Fable 5.1／`xhigh` | (D1)，含 Profile 所列三項條件 | `gov-alternate-reviewer`＋`model: fable`（fresh context） |
| E-FA | `final_adjudicator` | Fable 5.1／`xhigh` | (M2)、(D1)。(M1) 不採用：本檔不宣告以高風險類別觸發 Fable | `gov-final-adjudicator`＋`model: fable`（fresh context） |
| E-OR | `orchestrator` | Opus 5.5／`high` | (M1)、(D1)；於 activation 或 successor session 生效，記入 run record | Root session 以 `--effort high`（或 `/effort high`）啟動 |
| E-BW | `bounded_worker` | `mechanical` → `standard`（Sonnet 5.5／`high`，O-3） | (D1)：呼叫者核對後記錄 `mechanical` 輸出不足或錯誤；`standard` 不再升級 | `gov-bounded-worker`（frontmatter 即 `standard`） |
| E-IN | `investigator` | Opus 5.5／`high`（O-3） | (D1) 呼叫者記錄調查跨多個子系統且原因交互作用；(D2) investigator 回報 inconclusive 並附理由 | `gov-investigator`＋`model: opus` |

E-EX 不適用（O-1）；E-AD 不適用（`advisor` 未採用，第 3.4 節）。Escalation record 依 Profile §8 寫在派工者的 worklog 或 run record；review／adjudication 角色提出 D trigger 時寫在自己的 record，並且不作 verdict 或 ruling（治理 §2.5 規則 3）。

### 3.3 Codex

Codex **未宣告**：不作任何角色的 mapping 或 override，也不在任何 fallback 列。`primary_reviewer` 因此解析為 Opus 5.5／`xhigh`（resolution）。要讓 Codex 擔任 `primary_reviewer`，先在本節完成 Profile v2.4 §5 的四項宣告與 qualification，並記入第 9 節。

### 3.4 Bounded assignments 與其他 subagents

採用 Profile §2.2 的兩個 bounded assignments（治理 §2.6）。它們**不是治理角色，沒有任何 authority**；輸出是呼叫者待核對的輸入，不構成 finding、verdict、ruling、decision、derivation、接受、授權或 audit record。`advisor` 不採用。

| Identifier | Definition | Model | Effort | 用途 | 允許的呼叫者 |
| --- | --- | --- | --- | --- | --- |
| `investigator` | [`gov-investigator`](../../.claude/agents/gov-investigator.md) | `claude-sonnet-5-5` | `high`（O-3） | 唯讀調查：跨檔案追查、root-cause 假設、證據蒐集 | Executor；Orchestrator（只限控制面，例如狀態擷取） |
| `bounded_worker`（`standard`） | [`gov-bounded-worker`](../../.claude/agents/gov-bounded-worker.md) | `claude-sonnet-5-5` | `high`（O-3） | 有界、呼叫者可核對的工作：搜尋、擷取、格式轉換、依明確樣式的機械修改、log／diff 摘要 | Executor；Orchestrator（只限控制面，例如紀錄整理） |
| `bounded_worker`（`mechanical`） | `gov-bounded-worker`＋`model: haiku` | `claude-haiku-5-5`（O-3；qualification-gated，見下） | `high`（O-3） | 同上，可由呼叫者機械核對者 | 同上 |

- **Task class**：呼叫者派工時指定 `standard` 或 `mechanical` 並記錄；無法明確歸為 `mechanical` 者一律 `standard`。
- **Haiku 是 qualification-gated**（Profile §2.2）：第 8.2 節的 qualification probe 觀測到實際 model 為 `claude-haiku-5-5`、effort 為 `high`，並記入 `binding-verification.md` 之後，`mechanical` 才以 Haiku 派工；在那之前 `mechanical` 依 `standard` 派工（Sonnet 5.5／`high`，resolution，不記 substitution）。
- **O-3 effort／model override**（acceptor 2026-10-14 決議）：`investigator` 與 `bounded_worker`（`standard`）由 Profile 的 Sonnet 5.5／`medium` 改為 Sonnet 5.5／`high`；`bounded_worker`（`mechanical`）由 Haiku 5.5／`low` 改為 Haiku 5.5／`high`。Fallback 依同一 effort（第 3.1 節 F-BW、F-IN）。E-IN 的 escalated mapping 由 Profile 的 Opus 5.5／`medium` 改為 Opus 5.5／`high`。
- **呼叫者限制**：Design Authority、Reviewers 與 Final Adjudicator 的 definition 沒有 Agent tool，不呼叫 bounded assignments，審查與裁決的證據一律自己取得。Orchestrator 不得藉 bounded assignment 取得治理 §2.4 禁止它作的判斷（治理 §2.6 第 6 項）。
- **呼叫者的責任**（治理 §2.6）：自行核對輸出後才使用；需要 authority 的決定由呼叫者以自己的角色作出並寫入自己的紀錄。Executor 使用 bounded assignment 屬 self-verification，不算 independent audit。呼叫者在 worklog 或 run record 記下所用的 bounded assignment、task class、binding 證據（第 3.6 節）與輸出的採用方式；它的動作不另成 work item。
- **範圍**：bounded assignment 不得擴大委派範圍、派工任何 subagent，或以任何角色的名義作成紀錄；`investigator` 唯讀，不修改任何檔案。
- 在 governance on 的 work item 中，治理角色只派工第 3.1 節與本節的 `gov-*` definitions；不派 `Explore`、`Plan`、`general-purpose`、fork 型或其他未在本檔宣告的 subagent。

### 3.5 Session 的角色（治理 §2.2、§2.7）

- **無角色 session**：主 session 預設不擔任任何治理角色。它可以與 acceptor 對話、Grill、查詢、說明，也可以作為派工介面派 `gov-*`（派工仍須符合第 3.6、3.7 節），但不取得任何 authority，派工也不構成任何角色的 activation basis。它寫的內容不是治理紀錄；依 acceptor 明確指示轉錄決定時，紀錄標明決定者。
- **Lightweight direct-execution Executor**：主 session 明確進入 Executor 角色前，須同時具備：(1) activation basis——acceptor 已接受的 Outcome Contract（第 2.3 節）且 lane 為 Lightweight；(2) 該 session transcript 的 model／effort 為 `claude-opus-5-5`／`high`（第 3.6 節）；(3) 讀過 `.claude/agents/gov-executor.md`；(4) 該 work item 的 worklog。進入點記入 worklog。Model／effort 不符時，主 session 不得擔任 Executor，改派 `gov-executor` subagent，自己只負責派工與 routing。
- **Orchestrator**：acceptor 在主 session 指定（designation），session 以 `claude-opus-5-5`、effort `medium`（E-OR 成立時 `high`）執行，先讀 `.claude/agents/gov-orchestrator.md`，以 run record 為 work identity。`gov-orchestrator` 不以 subagent 派工。
- 一次只擔任一個角色；work item 或 run 結束時角色隨之結束（治理 §2.7 第 6、7 項）。同一執行 context 不得轉名成 Reviewer。

### 3.6 Binding verification

- 每個 definition 的 frontmatter 綁定完整 model id 與 effort，不使用 `inherit`。不設定會覆寫角色綁定的全域 subagent model（例如 `CLAUDE_CODE_SUBAGENT_MODEL`）。
- Escalated 或 fallback mapping 以同一 definition 加 Agent tool 的 per-dispatch `model`／`effort` 參數派工（Profile §6 (b)），`gov-executor-fallback` 除外。`model` 參數是 alias，每次都以 transcript 核對實際 model。
- **證據來源**（orch-default v2.2 §11；可逐筆觀察）：
  - 被派工的 assignment：`~/.claude/projects/<專案 slug>/<session-id>/subagents/` 內，`agent-<agentId>.meta.json` 的 `agentType` 是 definition 名稱，`agent-<agentId>.jsonl` 每一則 assistant 訊息的 `message.model` 與 `effort` 是實際 model 與 effort。
  - Root role session（Orchestrator、direct-execution Executor）：`~/.claude/projects/<專案 slug>/<session-id>.jsonl` 每一則 assistant 訊息的 `message.model` 與 `effort`。
- **全程核對**（治理 §2.2 V22-10；orch-default v2.2 §3）：核對對象是 assignment 的全部 assistant 訊息，不只第一則。觀測到的 (model, effort) 集合必須只有一個元素，且等於該次派工的有效 mapping（含已記錄的 escalation 或替代）。出現第二個元素即是改變點；自改變點起的工作不是合格產出，依治理 §2.2 修復或替代。時點：
  - 採用被派工 assignment 的 return 之前。
  - Root role session 的工作被用作 commit、gate、routing、rollover 交接或 completion 的依據之前，核對自上次核對以來的該段 transcript；direct-execution Executor 至少在結案前核對一次。
  - 無法取得涵蓋該段工作的證據時 fail closed：該段工作不作上述依據。
- 核對結果以「agentId（或 session-id）＋觀測到的 (model, effort) 與則數」寫進 worklog、audit record 或 run record 的 binding 欄位。

核對指令（`<session-dir>` 換成 `~/.claude/projects/<專案 slug>/<session-id>`）：

```bash
python - "<session-dir>" <<'EOF'
import json, pathlib, sys
from collections import Counter
root = pathlib.Path(sys.argv[1])
def scan(path):
    seen = Counter()
    for line in path.open(encoding="utf-8"):
        d = json.loads(line)
        m = d.get("message")
        if d.get("type") == "assistant" and isinstance(m, dict) and m.get("model"):
            seen[(m["model"], d.get("effort"))] += 1
    return dict(seen)
session = root.with_suffix(".jsonl")
if session.exists():
    print("root-session", root.name, scan(session))
for meta in sorted(root.joinpath("subagents").glob("agent-*.meta.json")):
    agent_type = json.loads(meta.read_text(encoding="utf-8")).get("agentType")
    print(meta.name.replace(".meta.json", ""), agent_type,
          scan(meta.with_name(meta.name.replace(".meta.json", ".jsonl"))))
EOF
```

### 3.7 Independent dispatch 機制（治理 §2.3）

正式 audit 與裁決由 Orchestrator 或主 session 透過 Claude Code 的 Agent tool 派工，`subagent_type` 指定 `gov-primary-reviewer`、`gov-alternate-reviewer` 或 `gov-final-adjudicator`。四項 properties 的滿足方式：

1. **Independent context**：非 fork 的 subagent 從空白 context 開始，不繼承派工者的對話。派工內容只放 bounded pack：Outcome Contract、Spec／Ticket、worklog、受審 subject（branch 與 commit SHA）的**路徑與識別**，不放 Executor 的結論或摘要。審查與裁決一律不得使用 fork 型 subagent。R2 可延續同一 reviewer 的 R1 context（以 SendMessage 續派同一個 agent），但 MUST 重讀修正後的檔案與 diff；以 escalated mapping 重派的 review 或 adjudication 一律是新的 fresh 派工。
2. **Verifiable binding**：依第 3.6 節核對。
3. **Autonomous access**：reviewer 與 adjudicator 有 Read、Grep、Glob、Bash，可自行讀取整個 repo、git 歷史並執行測試；bounded pack 只是入口。
4. **Self-written record**：reviewer／adjudicator 以自己的 Write 工具把 record 寫到第 7 節的位置；派工者只能原樣 commit，不得改寫、刪減或決定是否記錄。Subagent transcript 內的 Write 呼叫即為作者證據。

Claude Code 的自動記憶（memory）不是權威紀錄：不得以它代替 re-ground，也不把 review、裁決或 Executor 的結論寫進自動記憶，以免被之後的 context 繼承。

以下一律只算 self-verification，不得記為正式 audit：Executor session 內的 fork 型 subagent 或 code-review 類 skill、未綁定 `gov-*` definition 的一般 agent、由 Executor 轉述的 review 結論。

## 4. Lane policy

| 工作 | 預設 lane |
| --- | --- |
| 作業的實作、修正或文件，契約清楚，且能在一個 execution unit 內完成 | **Lightweight** |
| 作業需要分解成多個 execution units、管理其 dependencies，或需要跨多個 Executor／Reviewer session 協調完成（治理 §3.6-C） | **Formal**（Spec＋Tickets＋Orchestrator） |
| 需要為產品行為、介面、invariant 或 gate 建立其他工作將依賴的新設計基線（治理 §3.6-B） | **Formal** |
| 已結案工作之後的單點修正 | Lightweight，作為新的 work item；以 acceptor 的直接指示作為其 Outcome Contract |
| 通知、進度同步、文件維護等行政作業慣例 | Lightweight（治理 §3.6-B 的條件） |

- Lane 依預期的**整體**結果判定，不依本次增量；不得把需要 Formal 的作業拆成多個 Lightweight 指示來執行（治理 §3.3）。
- 模糊或有爭議的分類由 Design Authority 判定，並留 decision record。
- 預設分類不取代治理 §3.3 的 eligibility：Lightweight 工作中第一個需要對 intent、scope、acceptance、authority 作假設之處，就是 routing condition。
- Lightweight 不產生 Spec／Tickets，也不啟動 Orchestrator run（治理 §3.5；orch-default §1）；需要其他 authority 時，由 direct-execution session 依第 3.7 節派工。

## 5. Assurance policy

- **Formal**：每個 Ticket 的 independent audit 與每份 Spec 的 Spec Integration Audit 都必須執行（治理 §4.1、§4.7）。
- **單 Ticket fast path**（治理 §4.7）：**採用**。Spec 只有一張 Ticket 時，該 Ticket 的 R1 可同時滿足 Spec Integration Audit，條件是派工時就指定該 R1 兼作 Spec Integration Audit，且 record 逐項記載治理 §4.7 的五個範圍並明寫「本 record 同時是 Spec Integration Audit」。核對方式：Orchestrator 依 orch-default §6 逐項核對 record 是否載明五個範圍、subject 是否為最終整合 subject，缺任一項即另派。不得事後重新標示既有 R1 record。
- **Lightweight audit 預設**：不要求 independent audit。worklog 如實標示「完成且依 policy 未要求 independent audit」，不得寫成 audit PASS。
- **Lightweight audit 觸發條件**：acceptor 要求；變更涉及該單元 Design Authority 確認的高風險類別；Design Authority 裁決要求。
- **高風險類別**：治理 §5.1 規定由 Design Authority 決定，以單元的 decision record 承載。初始候選為 H-1 憑證與機密（API key 是否可能進入瀏覽器端程式、git、log 或文件）與 H-2 老師指定的介面或資料格式（評分直接依賴的檔名、資料表結構、API endpoint、輸出格式）；每份作業第一次正式 audit 或 Formal activation 前，由 Design Authority 確認或修改。`home_work_01/` 已確認並新增 H-3（`home_work_01/doc/governance/decisions/decision-20260923-high-risk-categories.md`）。本檔不以任何高風險類別作為 capability escalation trigger。
- **Integration／release gates**：release 指合併進 `main`（RB-1，保留給 acceptor）。請 acceptor 合併前須具備：
  - Formal：全部 Ticket 依 orch-default §7 結案、每份 Spec 的 Spec Integration Audit 已 closure、Design Authority phase acceptance 已完成。
  - 單元 `README.md` 的安裝與執行步驟有變動時，已實際跑過，結果與證據記在 worklog。
  - 沒有追蹤中的機密：`git ls-files` 不含 `.env`，diff 內沒有金鑰字串。
- **Model diversity**（治理 §2.2 V22-11；Profile §5）：因 O-1，Executor、Primary Reviewer、Alternate Reviewer 預設同為 `claude-opus-5-5`，Profile §5 的 D1、D3 在本專案的拓樸下不成立；本檔不宣告任何 diversity 關係（D1–D4 皆記「未宣告」），所以不記 `diversity_lost`。Audit record 分兩欄記載：(a) context independence 四項 properties 的滿足方式；(b) Executor、Primary、Alternate 的實際 model（引用第 3.6 節證據），相同時記「無 model diversity」，不得主張 diversity。Diversity 不影響 independence 的判定；本專案沒有要求恢復 diversity 才能 audit 的類別。

## 6. Skills and runtime

- **Implementation HOW**：`impl-default` `v2`，overrides none。
- **Control-plane HOW**（只在 Formal）：`orch-default` `v2.2`，overrides none。並行度 1（逐張 Ticket 執行）。
- **Harness**：Claude Code（desktop app 或 CLI），Windows。派工用 Agent tool，角色 definition 在 `.claude/agents/gov-*.md`。新增或修改 definition 後要重開 session 才會載入，binding 驗證也必須在新 session 進行（Profile §6）。
- **工作 skills**：`/to-spec`、`/to-tickets`、`gh` CLI（見 `docs/agents/issue-tracker.md`）與其他已安裝的 skills 只提供 HOW，不因被呼叫而取得設計、接受或核准權（治理 §3.4）。
- **Git**：依 `docs/conventions/git-commit-rules.md`；commit message 與 PR 描述不加 Claude 標記。
- **Recovery**：依 orch-default §8 與治理 §1.5，從第 7 節的紀錄 re-ground；對話 context 與自動記憶只是 cache。

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
| Outcome Contract | `doc/governance/outcome-contract.md`；同一作業有多份時加後綴。Lightweight 的直接指示原文記在 worklog |
| Spec | `doc/spec/`（沿用既有慣例） |
| Ticket | GitHub Issues；Issue 內引用所屬 Spec 與 worklog 路徑。`doc/ticket/` 只放索引 |
| Derivation record | `doc/governance/decisions/derivation-<spec>.md`（Spec 與其 Tickets 的 derivation 都記在這裡） |
| Decision record | `doc/governance/decisions/decision-<YYYYMMDD>-<slug>.md` |
| FA ruling | `doc/governance/decisions/ruling-<YYYYMMDD>-<slug>.md` |
| Worklog | Formal：`doc/governance/worklog/issue-<n>.md`；Lightweight：`doc/governance/worklog/<YYYYMMDD>-<slug>.md`。續接 session 更新同一份 |
| Audit record | Ticket：`doc/governance/audit/issue-<n>-c<cycle>-<r1\|r2\|alt>.md`；Spec Integration Audit：`doc/governance/audit/spec-<spec>-c<cycle>-<r1\|r2\|alt>.md` |
| Run record | `doc/governance/run/run-<YYYYMMDD>-<slug>.md` |
| Escalation／substitution record | 派工者的 worklog（Lightweight）或 run record（Formal）；review／adjudication 角色提出的 escalation 記在自己的 audit record 或 ruling（Profile §8） |

- 資料夾在真的產出該類紀錄時才建立。
- `doc/governance/**` 是 **record-only paths**：只改這些路徑的 delta 不影響受審 subject 的 identity（orch-default §7 P7）。
- 紀錄只放文件；實作、資料與測試留在單元根目錄或既有位置。

## 8. 採用時的處理

### 8.1 進行中的工作（治理 §5.3）

- b4 起草時（2026-10-14）沒有 open 的 issue 或 PR，沒有在治理下進行中的 work item。
- `home_work_01/` 在 b1–b3（Minimal v2.0）下完成的 work items、audit 與 decision records 保持原樣，不重新審查、不改寫；其中引用的 v2.0 快照已自本目錄移除，需要時以 git 歷史讀取（見 [`README.md`](README.md)）。b4 生效後開始的 work item 一律適用 Minimal v2.2 與本檔。
- `weekNN/`：governance off，不受影響。

### 8.2 第一次正式 audit 或 Orchestrator activation 前（b4）

治理 §5.1：bindings 與 definitions 須在 Orchestrator activation 前、以及 Lightweight work item 第一次正式 audit 前就緒且可驗證。Lightweight direct execution 本身不需等待以下 dry-run（root session 依第 3.6 節自行核對）。

| # | 項目 | 狀態 |
| --- | --- | --- |
| 1 | b4（本檔、`PKG/`、更新後的 `gov-*` definitions）合併進 `main` | 待 acceptor（RB-1） |
| 2 | 重開 Claude Code session，確認更新後的 `gov-*` definitions 已載入 | 待辦 |
| 3 | Binding dry-run：對九個 `gov-*` definition 各派一次不做事的任務；另以 per-dispatch 參數各派一次，核對 alias 的實際 model：`model: fable`（escalation／fallback 路徑）、`gov-investigator`＋`model: opus`（E-IN）、`gov-bounded-worker`＋`model: haiku`（Haiku qualification probe，預期 `claude-haiku-5-5`／`high`，第 3.4 節）。以第 3.6 節指令核對，結果記在 [`binding-verification.md`](binding-verification.md) b4 節 | 待辦 |
| 4 | 每份作業的高風險類別由 Design Authority 確認（第 5 節） | 每份作業各自處理（`home_work_01/` 已完成） |
| 5 | 該作業的 Outcome Contract 有 acceptor 接受紀錄（第 2.3 節） | 每份作業各自處理 |

## 9. 變更紀錄

| 版本 | 日期 | 變更 | 依據 | 授權 |
| --- | --- | --- | --- | --- |
| b1 | 2026-09-23 | 初版：`home_workNN/` 採用 Minimal Governance — Reusable Package v2.0，`weekNN/` 與 root 不採用；宣告第 1–8 節全部 bindings。 | acceptor 2026-09-23 指示：導入治理原則並以 flag 控制啟用，DIC 不使用，採用 Notion 的 Minimal Governance — Reusable Package v2.0。 | 待 acceptor 合併引入本檔的 PR 後生效 |
| b1（合併前修訂） | 2026-09-23 | 第 2.4 節 scope 規則改為：MVM 必須完整滿足上位契約；acceptor 授權的 ENHANCED／OPTIONAL 可超出老師撰寫的需求，須明確標示且不得取代、弱化或冒充老師要求的行為。 | acceptor 2026-09-23 於 `home_work_01` grill 中裁決，並依 RB-5 授權此最小修改。 | 隨 b1 一同待合併 |
| b2 | 2026-09-24 | 第 3.1 節 `executor` mapping override：model 由 `claude-opus-4-8` 改為 `claude-opus-5-5`（effort `high` 不變）；新增 override fallback `claude-opus-4-8`／`high` 與其 definition `gov-executor-fallback`；第 1 節 override 標示與第 5 節 model diversity 相應更新。其他角色 mapping、replacement policy、lane、assurance、audit flow 與 implementation method 不變。 | acceptor 2026-09-24 指示：「Primary Executor：Opus 4.8 → Opus 5.5」「Executor fallback：Opus 4.8」，其餘全部維持現狀；本輪只是 project configuration／model-mapping 調整，不觸發 implementation audit。 | 待 acceptor 合併引入本變更的 PR 後生效；不適用生效前已開始的 work item（治理 §5.3），變更時沒有 open 的 issue 或 PR。第一次以 b2 mapping 派 Executor 前，須完成 `binding-verification.md` b2 節的 dry-run |
| b3 | 2026-09-25 | 第 2.6 節 RB-3：金鑰授權位置由「只能放在未追蹤的本機 `.env`」改為兩個位置——未追蹤的本機 `.env`，以及部署平台（Vercel）專案的環境變數（只由 acceptor 親自填入；Agents 不得填入、讀出、印出或匯出；只在伺服器端執行期讀取；不傳給前端、不進 log／evidence）。其他憑證限制、角色 mapping、lane、assurance、audit flow 與 implementation method 全部不變。 | acceptor 2026-09-25 於 HW01 Weather Map V2 grill 裁決（D-3）：授權 Vercel 專案環境變數為 CWA 金鑰的第二個位置（條件：acceptor 填入、不印出／匯出、不提交、不暴露前端、不進 log／evidence），並依 RB-5 授權起草只含此變更的最小 b3 修正。 | 待 acceptor 合併引入本變更的 PR 後生效（RB-1）；不適用生效前已開始的 work item（治理 §5.3）；`home_work_01` V2 work item 的 activation 以本變更生效為前置（`home_work_01/doc/governance/outcome-contract-v2.md` §8）。 |
| b4 | 2026-10-14 | **Re-pin 至 Reusable Package v2.2**（治理 §5.3）：Minimal v2.0 → v2.2、Model Profile `default` v2.2 → v2.5、orch-default v2 → v2.2、impl-default v2 不變；生效檔案改為 `PKG/` 內的位元複本，移除舊的 v2.0 快照。第 3 節依 v2.5 改寫：DA、Alternate、FA、Orchestrator 的 mapping 改為 Profile 預設（Opus 5.5），保留 b2 的 `executor` override 為 O-1，新增 O-2（Agent tool 無 Opus 4.8 alias 的 fallback override）、capability escalation（E-DA、E-AR、E-FA、E-OR）、不採用 bounded assignments、session 角色（無角色 session、direct-execution Executor 的進入條件）與全程 binding 核對。第 4 節 lane policy 改為 Lightweight 優先，Formal 只在治理 §3.6-B／C 成立時使用。第 5 節採用單 Ticket fast path，model diversity 改為不宣告關係、分兩欄記載。第 2.3 節區分 Lightweight 與 Formal 的 Outcome Contract 形式。Authority sources、standing authorizations、reserved boundaries、work records 位置不變。 | acceptor 2026-10-14 指示：「請將新版 Minimal Governance v2.2 套用至目前的 `aiot-classwork` 專案」，以 Package 為權威來源，採用 Lightweight Governance（保留核心原則與角色分工；簡單任務輕量、複雜任務才啟用完整流程；不引入不必要的文件、審核關卡或流程），不需逐步詢問批准。 | 待 acceptor 合併引入本變更的 PR 後生效（RB-1）；不適用生效前已開始的 work item（治理 §5.3），變更時沒有 open 的 issue 或 PR。第一次正式 audit 或 Orchestrator activation 前須完成第 8.2 節 #2、#3 |
| b4（合併前修訂） | 2026-10-14 | 第 3.4 節改為採用 Profile §2.2 的 `investigator`（Sonnet 5.5／`medium`）與 `bounded_worker`（`standard` Sonnet 5.5／`medium`；`mechanical` 在 Haiku qualification 通過前解析為 Sonnet 5.5／`low`），新增 definitions `gov-investigator`、`gov-bounded-worker`；呼叫者限 Executor 與 Orchestrator（只限控制面）；`advisor` 不採用。第 3.1 節 O-2 加 F-BW、F-IN、F-IN\*；第 3.2 節加 E-BW、E-IN；第 8.2 節 #3 加對應的 dry-run 與 Haiku qualification probe。其他內容不變。 | acceptor 2026-10-14 回覆「採用 bounded assignments，這個可以接受」（針對 `investigator` 與 `bounded_worker` 的提議）。 | 隨 b4 一同待合併 |
| b4（合併前修訂 2） | 2026-10-14 | 第 3.4 節新增 O-3：`investigator` 與 `bounded_worker`（`standard`）改為 Sonnet 5.5／`high`；`bounded_worker`（`mechanical`）改為 Haiku 5.5／`high`（仍須通過 qualification probe，之前依 `standard` 派工）。第 3.1 節 F-BW、F-IN 依新 effort 改寫，第 3.2 節 E-BW 目標相應更新，E-IN 維持 Profile 原值；definitions `gov-investigator`、`gov-bounded-worker` 的 effort 改為 `high`；第 8.2 節 #3 的 probe 相應更新。 | acceptor 2026-10-14 決議：「mechanical 可以改為 haiku 5.5 high，沒問題，sonnet 5.5 的 2 個也拉高到 high，這是我現在的決議。」 | 隨 b4 一同待合併 |
| b4（合併前修訂 3） | 2026-10-14 | 第 3.2 節 E-IN 的 escalated mapping 由 Opus 5.5／`medium` 改為 Opus 5.5／`high`（併入 O-3）；第 3.1 節 F-IN\* 與第 8.2 節 #3 的 probe 相應更新。 | acceptor 2026-10-14 對「E-IN 是否也改成 Opus 5.5／high」回覆「改成 high」。 | 隨 b4 一同待合併 |
