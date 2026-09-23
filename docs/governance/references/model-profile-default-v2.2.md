# Reference Model Profile — default v2.2

> **本專案快照，不是 authoritative source。**
>
> - 來源：Notion「Reference Model Profile — default v2.2」（https://app.notion.com/p/3e3463583346815b87acd94d1eb72246），屬於「Minimal Governance — Reusable Package v2.0」；頁面最後編輯 2026-09-23，擷取於 2026-09-23。
> - Authoritative source：`master_governance/references/model-profiles/default-v2.2.md`（md5 `a26ed091325a89c4c1e4173d6b858ede`），不在本 repo。Notion 版已把相對連結攤平，所以本檔不會與該 md5 byte-identical。
> - 轉換：Notion 表格、callout 與頁面連結轉成 GitHub Markdown，文字內容未改寫。
> - 與 authoritative source 不一致時，以 authoritative source 為準，並更新本快照。
> - 本專案如何採用本文件，見 [`project-bindings.md`](../project-bindings.md)。

---
> **Notion 發布版（2026-09-23 sync）。** Authoritative source 為 repo：`master_governance/references/model-profiles/default-v2.2.md`（md5 `a26ed091325a89c4c1e4173d6b858ede`）；不一致時以 repo 檔案為準。Markdown 相對連結已攤平為「repo: path」。`default-v2.1.md`（md5 `fe473990915f0e7c22b43f51cf4d5658`）與 `default-v2.md`（md5 `d97d8d1b3a2f7b011c9b52eab639054d`）保留為 repo-only frozen baseline；本頁原發布 v2.1，2026-09-23 同日更新為 v2.2。所屬 package：Minimal Governance — Reusable Package v2.0。

**Profile ID：****`default`**

**Version：****`v2.2`**

**Status：Adopted／Frozen（2026-09-23，operator 明確授權）**

**Governance：Minimal Operational Governance v2.0（Adopted／Frozen 2026-09-22）**

**Supersedes for new adoption：****`default`****／****`v2.1`**（`default-v2.1.md`（repo: `master_governance/references/model-profiles/default-v2.1.md`） 與 `default-v2.md`（repo: `master_governance/references/model-profiles/default-v2.md`） 保留為 frozen baseline；已 pin `v2.1` 或 `v2` 的專案不自動改用）

**定位：新專案的參考預設。所有可 dispatch identifier 皆有可解析的預設值與 deterministic replacement policy；binding verification 的實作證據仍由採用專案提供。**

角色定義與權限以 Minimal Operational Governance v2.0（repo: `master_governance/Minimal_Operational_Governance_v2.0_Candidate.md`） §2.1 為準。本 Profile 不改變任何 role authority、independence requirement 或 audit bounds（Minimal §2.2）。專案採用 `default`＋`v2.2`，在 Project Bindings 記錄 overrides（無則明記 `none`）；後續版本不自動影響已採用專案。模型名稱與 IDs 是設定依據，不代表已完成當前平台的可用性或 binding 驗證。

## 1. 值的四種狀態

| 標記 | 意義 | 處理方式 |
| --- | --- | --- |
| **具體值** | 本 Profile 的預設 | 直接採用；Bindings MAY override 並記錄理由 |
| **`PROJECT_BINDING`** | 依本質只能由專案提供（例如特定 harness 的 binding verification 證據位置） | 不是問題、不是缺漏。Bindings 在對應執行／activation／audit 前填入；本 Profile 對 Claude Code harness 於 §5 給出預設機制 |
| **`N/A`** | 該平台／角色不適用 | 明記不適用 |
| **`TBD`** | 沒有足以指定該值的依據 | **本版無 ****`TBD`****。** 日後出現時依 Minimal §2.2 不構成有效設定 |

v1 的 `USER_SELECTION_REQUIRED` 已移除：`primary_reviewer` 有預設值。使用者只在需要 override 時透過 Project Bindings 介入；initialization 不再詢問任何 model 選擇。

## 2. Default mapping（operator S-1 決定，2026-09-22）

| identifier | role / subagent | model | model id／resolution policy | effort／mode | replacement policy | binding verification |
| --- | --- | --- | --- | --- | --- | --- |
| `design_authority` | Design Authority | Fable 5.1 | `claude-fable-5-1`；當次解析結果須驗證 | `xhigh`；design decision／clarification／derivation／phase acceptance | R-DA（§3） | §5 |
| `executor` | Executor | Opus 4.8 | `claude-opus-4-8`；不依 parent model 隱性解析 | `high`；implementation＋self-verification | R-EX（§3） | §5 |
| `primary_reviewer` | Primary Independent Reviewer | Opus 5.5 | `claude-opus-5-5`；不依 parent model 隱性解析 | `xhigh`；independent review-only：R1／R2、Spec Integration Audit（Minimal §4.7） | R-PR（§3） | §5 |
| `alternate_reviewer` | Alternate Independent Reviewer | Fable 5.1 | `claude-fable-5-1` | `xhigh`；fresh independent review-only；exactly one Alternate | R-AR（§3） | §5 |
| `final_adjudicator` | Final Adjudicator | Fable 5.1 | `claude-fable-5-1` | `xhigh`；independent adjudication | R-FA（§3） | §5 |
| `orchestrator` | Orchestrator | Opus 4.8 | `claude-opus-4-8` | `high`；control plane／routing／run-to-completion | R-OR（§3） | §5 |

Design Authority、Alternate Independent Reviewer 與 Final Adjudicator 使用同一 model；所行使的 authority MUST 可區別（Minimal §2.1），且各自使用獨立 context（Minimal §2.3）。Effort 值是預設，Bindings MAY 以 explicit override 調整並記錄理由。Orchestrator 自身 effort 依 orch-default §11 於 activation 設定並記錄。

## 3. Deterministic replacement policies

共同規則（Minimal §2.2、§2.3）：

1. **觸發依據**：當次 dispatch 的錯誤，或當下的可用性檢查證據；不得憑記憶或先前 session／run 的不可用狀態跳過指定 model。
2. **順序**：先依 Project Bindings override 的 fallback 列，再依本節 fallback 列，逐項嘗試第一個可用者；不跳序、不猜。
3. **每次替代 MUST**：維持 Minimal §2.3 四項 properties（review／adjudication 角色的 fresh context 不因替代而繼承任何既有對話）；不新增 audit round；不改變 authority；在 worklog／run record 記錄 substitution（原 mapping、替代 mapping、證據引用、model diversity 是否改變）。
4. **Fallback 列耗盡**：該路徑進入 Minimal §1.5 recovery；三步完成後仍 unsafe／indeterminate 才停止該路徑。
5. **替代不重新觸發任何初始化詢問**（Minimal §2.2；v1 的 Primary Reviewer initialization 節已不存在）。

| Policy | Fallback 列（依序） | 附加規則 |
| --- | --- | --- |
| **R-DA** `design_authority` | Opus 5.5／`xhigh` | 合格替代者以 Design Authority 身分派工即行使 Design Authority 權限；其有效 decision 即為 DA decision（authority 屬角色，不屬 model；Minimal §1.3、§2.2），不需 preferred／default DA model 事後確認；preferred model 恢復可用本身不重開、不使先前 decision 失效。日後任何變更依 Minimal §5.3 一般規則，以角色權限與新證據為依據、依變更實際性質適用第 1 或第 2 類，不以 model 身分為依據。替代 DA 不得修改 norm，不擴張為 Final Adjudication 權限 |
| **R-EX** `executor` | Opus 5.5／`high` → Codex（Bindings 宣告可用時）→ Fable 5.1／`high` | 接手 Executor 沿同一 worklog identity（impl-default §10）。替代使 Executor 與 `primary_reviewer` 同 model 時，記錄 `diversity_lost`（§4） |
| **R-PR** `primary_reviewer` | Codex（Bindings 宣告可用時；fresh context）→ Fable 5.1／`xhigh` → Opus 4.8／`xhigh` | 替代為 Fable 5.1 時，該 cycle 的 `alternate_reviewer` 改用 Opus 5.5／`xhigh`，使 Alternate 仍為 Primary 以外的 fresh context（同 model 亦合法，但記錄）。替代為 Opus 4.8 時記錄 `diversity_lost`。R2 由同一替代 reviewer 延續其 R1 context（Minimal §2.3） |
| **R-AR** `alternate_reviewer` | Opus 5.5／`xhigh` → Codex（Bindings 宣告可用時） | 仍 exactly one Alternate；不因替代重跑 R1／R2 |
| **R-FA** `final_adjudicator` | Opus 5.5／`xhigh` | 替代 FA 的 ruling 即為有效 ruling（authority 屬角色，不屬 model；Minimal §2.2）；不採 provisional。 |
| **R-OR** `orchestrator` | Opus 5.5／`high` → Fable 5.1／`high` | Successor 以同一 run identity 從權威紀錄 bootstrap（orch-default §8）；替代於 run record 記錄 |

## 4. Assurance defaults

- **Cross-model review 是預設 assurance policy**：Executor model ≠ Primary Reviewer model（預設 Opus 4.8 vs Opus 5.5）。這是 diversity 偏好，不是 Minimal §2.3 的 independence 定義；四項 properties 才是。
- 替代導致 diversity 消失時，替代仍合法；MUST 記錄 `diversity_lost`，並在該 audit record 的 independence 說明（Minimal §4.6）中註明。Project Bindings MAY 宣告特定高風險類別要求恢復 diversity 後再 audit；此為 assurance policy 宣告，不是新 audit round。
- Reviewer-tier diversity（Primary vs Alternate）不是要求（Final Architecture Review G-1 ruling：NON-MATERIAL）；本 Profile 預設給不同 model 只是偏好。

## 5. Binding verification

規範依據：Minimal §2.2、§2.3、§5.1。

**Claude Code harness 預設機制（SHOULD）**：角色 definition 檔綁定完整 model id 與 effort；每次 dispatch 以 harness 記錄的 `message.model` 與 `effort` 對照 definition；結果引用於 worklog／audit record。不設會覆寫角色綁定的全域 subagent model override。此為 10-ASPICE_auto 已驗證的做法（dry-run 4／4、run 20／20、21／21 MATCH），在此作為預設參考；不代表新專案已完成綁定，採用專案仍須提供自己的執行證據。

**其他 harness**：`PROJECT_BINDING`。

Prompt 自稱、設定存在、model 名稱相同，皆不構成 binding 證據。不同 model 不自動構成 independent review。

## 6. Codex as project override／replacement

Codex（OpenAI）為合格的 project override／replacement：Project Bindings 宣告其可用性、model／version、effort／mode 對應與 binding verification 方式後，可作 `primary_reviewer` 或 `executor` 的 override，或依 §3 列入 fallback。不可用時依 Minimal §2.2 引用當次證據跳過，不得憑先前不可用狀態預先排除。Codex 不因是不同 provider 而自動構成 independence；仍須滿足 Minimal §2.3。

## 7. Reusable subagents

同 v1：`master_governance` 中無已採用且有明確獨立 definition 的 reusable subagents，本版不新增推測性 rows。日後採用時依 Minimal §2.1–§2.2 在 Profile 或 Project overrides 中列明 identifier 與 mapping。

## 8. Change record

| Version | Date | Status | Basis | Change |
| --- | --- | --- | --- | --- |
| `v1` | 2026-09-16／17 | Adopted | Final Architecture Review：ADOPT | 初版；`primary_reviewer` = `USER_SELECTION_REQUIRED`；`orchestrator` 與三項 replacement policy = `TBD` |
| `v2` | 2026-09-22 | **Candidate** | vNext Architecture Analysis（repo: `Governance vNext Architecture Analysis(Fable-5.1).md`） §B.1、條件 C-5；operator S-1 決定 3（2026-09-22） | 全部 identifier 有預設值；deterministic replacement policies R-DA～R-OR；assurance defaults（cross-model 為預設、非 independence）；Codex override／replacement；`PROJECT_BINDING` 取代 `USER_SELECTION_REQUIRED`；無 `TBD`。S-4（M-4，2026-09-22）：R-DA 移除 provisional decision 與 primary-model 追認；替代 DA 的有效 decision 即為 DA decision，與 R-FA 同理由 |
| `v2` adoption／freeze | 2026-09-22 | **Adopted／Frozen** | S-3 Opus 5 acceptance review（repo: `Governance v2.0 Candidate Independent Acceptance Review(Opus-5).md`）：ADOPT WITH REQUIRED CHANGES；S-4 M-4 correction；Opus 5 closure（repo: `Governance v2.0 Candidate S-4 Closure Review(Opus-5).md`）：M-4 CLOSED；pruning P-13；Astra final regression（repo: `Governance v2.0 Final Pruning Regression Check(Astra).md`）：PASS；operator S-5 明確授權（Adoption and Freeze Record（repo: `Governance v2.0 Adoption and Freeze Record.md`）） | **`default / v2`**** formally Adopted／Frozen**；僅更新 header 與本列 metadata；mapping、replacement policies、assurance defaults、binding verification 不變 |
| `v2.1` | 2026-09-23 | **Candidate** | Operator 指示（2026-09-23）：官方新 model Opus 5.5（`claude-opus-5-5`）發布，預設 Opus 5 改為 Opus 5.5 | **Model-id revision only**：§2 `primary_reviewer` 由 Opus 5／`claude-opus-5` 改為 Opus 5.5／`claude-opus-5-5`；§3 R-DA、R-EX、R-PR、R-AR、R-FA、R-OR fallback 列中的 Opus 5 改為 Opus 5.5；§4 cross-model 預設說明相應更新。Opus 4.8、Fable 5.1 mapping、effort、replacement 順序、assurance policy、binding verification 不變。採用專案須以自身 §5 證據驗證 `claude-opus-5-5` binding |
| `v2.1` adoption／freeze | 2026-09-23 | **Adopted／Frozen** | Operator 於 2026-09-23 對「直接以 model-id 小改採用」回覆「可以」並指示更新 HTML 與 sync Notion；變更僅為 model id，不觸及 role authority、independence、audit bounds，未另行 independent review | **`default / v2.1`**** formally Adopted／Frozen**；僅更新 header 與本列 metadata；mapping、replacement policies、assurance defaults、binding verification 與 Candidate 內容相同；同一採用動作中修正 Candidate 漏改的自我版本引用（本檔導言「專案採用 `default`＋`v2`」→「`v2.1`」） |
| `v2.2` | 2026-09-23 | **Adopted／Frozen** | Operator 指示（2026-09-23）：review 時 effort 升一級；operator 選定「新 Model Profile 版本」方案（Option A）並明確授權；effort-only revision，不觸及 role authority、independence、audit bounds，未另行 independent review | **Effort-only revision**：§2 `primary_reviewer` effort 由 `high` 改為 `xhigh`；§3 R-PR 最後一個 fallback Opus 4.8 由 `high` 改為 `xhigh`，使替代 Primary Reviewer 不低於預設 effort。Model mapping、其他角色 effort、replacement 順序、assurance policy、binding verification 不變。預期成本：Primary Reviewer 承擔 R1／R2 與每份 Spec 的 Spec Integration Audit，token 與時間成本相應增加 |

本 Profile 之後的變更依 Minimal §5.3 留下版本、依據與授權；新版本不自動適用既有專案。
