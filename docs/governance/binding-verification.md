# Binding verification — dry-run（Project Bindings §8.2 #4）

- **日期**：2026-09-23
- **執行者**：主 session（acceptor 指示「Run the Bindings §8.2 #4 binding dry-run for all required gov-* roles and record the result in the required governance evidence file」）
- **方法**：依 Bindings §3.4，對六個 `gov-*` definition 各以 Agent tool 派一次不做事的任務（指示不讀、不寫、不執行、不裁決，只回一行 ack），再以 §3.4 的核對指令讀取 harness 紀錄 `~/.claude/projects/D--nchu-2026-AIoT-git-repository-aiot-classwork/25a2390c-ae1f-483e-8b7a-10f844793ab9/subagents/`，比對 `agent-<id>.meta.json` 的 `agentType` 與 `agent-<id>.jsonl` 各 assistant 訊息的 `message.model`／`effort`。
- **Definitions 版本**：`.claude/agents/gov-*.md` 於 `main` commit `21b25cf`（PR #17）。
- **Mapping 依據**：Bindings §3.1（Model Profile `default` v2.2，無 override）。

## 結果

| Identifier | Definition（`agentType`） | agentId | 觀測 model／effort | 預期（§3.1） | 回覆 | 工具呼叫 | 結果 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `design_authority` | `gov-design-authority` | `a0d333e6305be400d` | `claude-fable-5-1` ／ `xhigh` | `claude-fable-5-1` ／ `xhigh` | `binding dry-run ack: design_authority` | 0 | **PASS** |
| `executor` | `gov-executor` | `af2c0a9fdd4deff2a` | `claude-opus-4-8` ／ `high` | `claude-opus-4-8` ／ `high` | `binding dry-run ack: executor` | 0 | **PASS** |
| `primary_reviewer` | `gov-primary-reviewer` | `adacc75eecc548aff` | `claude-opus-5-5` ／ `xhigh` | `claude-opus-5-5` ／ `xhigh` | `binding dry-run ack: primary_reviewer` | 0 | **PASS** |
| `alternate_reviewer` | `gov-alternate-reviewer` | `a5310abf28827d8f8` | `claude-fable-5-1` ／ `xhigh` | `claude-fable-5-1` ／ `xhigh` | `binding dry-run ack: alternate_reviewer` | 0 | **PASS** |
| `final_adjudicator` | `gov-final-adjudicator` | `a7ff2fcdc96cedefd` | `claude-fable-5-1` ／ `xhigh` | `claude-fable-5-1` ／ `xhigh` | `binding dry-run ack: final_adjudicator` | 0 | **PASS** |
| `orchestrator` | `gov-orchestrator` | `af34869b0082a2554` | `claude-opus-4-8` ／ `high` | `claude-opus-4-8` ／ `high` | `binding dry-run ack: orchestrator` | 0 | **PASS**（見備註 1） |

**總判定：PASS**（6／6；無 replacement；model diversity 與 Model Profile §4 預設一致：Executor `claude-opus-4-8`、Primary Reviewer `claude-opus-5-5`）。

核對指令輸出（原樣）：

```text
agent-a0d333e6305be400d gov-design-authority [('claude-fable-5-1', 'xhigh')]
agent-a5310abf28827d8f8 gov-alternate-reviewer [('claude-fable-5-1', 'xhigh')]
agent-a7ff2fcdc96cedefd gov-final-adjudicator [('claude-fable-5-1', 'xhigh')]
agent-a80296b90d87819af gov-design-authority [('claude-fable-5-1', 'xhigh')]
agent-adacc75eecc548aff gov-primary-reviewer [('claude-opus-5-5', 'xhigh')]
agent-af2c0a9fdd4deff2a gov-executor [('claude-opus-4-8', 'high')]
agent-af34869b0082a2554 gov-orchestrator [('claude-opus-4-8', 'high')]
```

（`a80296b90d87819af` 是同日 Spec derivation 的真實 DA 派工，非 dry-run，一併列出作為額外證據。）

## 備註

1. **Orchestrator**：Bindings §3.3 規定 Orchestrator 由 acceptor 開的主 session 擔任（模型 `claude-opus-4-8`、effort `high`），不以 subagent 派工。本 dry-run 以 subagent 派一次只為核對 definition 的 binding；正式 Formal run 前，acceptor 須另開符合該 mapping 的主 session，並以 session transcript 核對（§3.4 末段）。
2. **本 dry-run 的主 session** 模型為 `claude-fable-5-1`（harness 顯示），**不符 `executor` 也不符 `orchestrator` mapping**：本 session 只能派工與記錄，不得自任 Executor 或 Orchestrator（§3.3）。DA、Alternate Reviewer、Final Adjudicator 雖與本 session 同模型，仍一律以 subagent 派工並核對，不由主 session 冒充。
3. 六次 dry-run 的 harness 紀錄皆為 0 次工具呼叫；`git status` 於 dry-run 前後無變化。
4. Bindings §8.2 表的 #3、#4 狀態欄仍寫「待辦」；更新該表屬 Bindings 檔案變更（RB-5），待 acceptor 處理。

---

# Binding verification — b2 `executor` override（Project Bindings §3.1、§9 b2）

- **範圍**：只核對 b2 變更的兩個 definition。其他五個 `gov-*` definition 未變更，沿用上方 b1 dry-run 結果。
- **方法**：同上方 b1，依 Bindings §3.4 對 definition 各派一次不做事的任務，再以 §3.4 核對指令讀 harness 紀錄。
- **前提**：Bindings §6 規定修改 definition 後要重開 session 才會載入，所以 dry-run 必須在修改後新開的 session 執行。

## 預期與結果（dry-run 2026-09-25，session `652a0fb2-378e-42d6-9537-6c55bb12edb5`）

| Identifier | Definition（`agentType`） | agentId | 預期 model／effort | 觀測 model／effort | 回覆 | Tool uses | 結果 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `executor` | `gov-executor` | `a79fde8213e723dc9` | `claude-opus-5-5` ／ `high` | `claude-opus-5-5` ／ `high` | `binding dry-run ack: executor` | 0 | **PASS** |
| `executor`（fallback） | `gov-executor-fallback` | `adc84fb5d25b63ffc` | `claude-opus-4-8` ／ `high` | `claude-opus-4-8` ／ `high` | `binding dry-run ack: executor-fallback` | 0 | **PASS** |

**總判定：PASS**（2／2；無 replacement）。Session 於 2026-09-25 開啟（b2 合併 `0af4f2d` 之後），載入的是 b2 版本的 definitions；派工由 acceptor 於 2026-09-25 明確授權。§3.4 核對指令對該 session 的輸出如下（同一 session 內另有一個非治理角色的 `general-purpose` 研究 agent，與 binding 核對無關，只為完整列出）：

```text
agent-a569854ac76965f6a general-purpose [('claude-fable-5-1', 'xhigh')]
agent-a79fde8213e723dc9 gov-executor [('claude-opus-5-5', 'high')]
agent-adc84fb5d25b63ffc gov-executor-fallback [('claude-opus-4-8', 'high')]
```

Model diversity（Bindings §5）：b2 下 Executor `claude-opus-5-5` 與 Primary Reviewer `claude-opus-5-5` 相同，正式 audit 時依 Bindings §5 在 audit record 記 `diversity_lost`；改派 fallback `claude-opus-4-8` 時恢復。

## 修改當下 session 的觀察（2026-09-24，不計為結果）

在修改 definition 的同一 session（`58e999a6-46bd-4d53-b92e-76a61af64023`）試派，結果符合「未重開 session 不會載入新 definition」：

- `gov-executor`：agentId `aa2541de1289c9e44`，觀測 `claude-opus-4-8` ／ `high`，是 session 啟動時載入的 b1 definition。
- `gov-executor-fallback`：harness 回報 `Agent type 'gov-executor-fallback' not found`。

```text
agent-aa2541de1289c9e44 gov-executor [('claude-opus-4-8', 'high')]
```

這不是 binding FAIL，只證明 b2 的 dry-run 須在新 session 執行。新 session 完成 dry-run 後，把 agentId、觀測值與核對指令輸出填入上表（已於 2026-09-25 完成，見上表）。

---

# Binding verification — b4（Package v2.2 re-pin，Project Bindings §3.1、§8.2 #3）

- **日期**：2026-10-14（b4 經 PR #47 合併進 `main` `6a75345` 之後）
- **執行者**：以 `claude -p --session-id 71b409f6-4592-4887-bcab-0f16b0f08a64 --model claude-opus-5-5 --effort high --allowedTools Agent` 啟動的全新 CLI session（無角色，只派工），依 acceptor 2026-10-14 指示「在新 session 跑 b4 binding dry-run」。核對與紀錄由另一個無角色 session（`8943ecf6-f2b0-4c4d-8e41-c796a644c4b4`）以 Bindings §3.6 指令讀 harness 紀錄完成。
- **方法**：在同一則訊息平行派出 12 個不做事的任務（只回一行 ack，不呼叫工具）：九個 definition 各一次，另加三個 per-dispatch 參數組合。除表列參數外不指定 model 或 effort。
- **Definitions 版本**：`main` `6a75345` 的 `.claude/agents/gov-*.md`（新 process 載入，Bindings §6）。
- **全程核對**：每個 agent 的 (model, effort) 集合都只有一個元素。

## 結果

| # | Identifier | Definition（`agentType`） | 派工參數 | 預期 model／effort | agentId | 觀測（則數） | Tool uses | 結果 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `design_authority` | `gov-design-authority` | — | `claude-opus-5-5` ／ `high` | `afba561c5711ffb35` | `claude-opus-5-5` ／ `high`（2） | 0 | **PASS** |
| 2 | `executor` | `gov-executor` | — | `claude-opus-5-5` ／ `high` | `aa9dc75658ef8ffd7` | `claude-opus-5-5` ／ `high`（2） | 0 | **PASS** |
| 3 | `executor`（fallback） | `gov-executor-fallback` | — | `claude-opus-4-8` ／ `high` | `a8a6e63cec562396a` | `claude-opus-4-8` ／ `high`（1） | 0 | **PASS** |
| 4 | `primary_reviewer` | `gov-primary-reviewer` | — | `claude-opus-5-5` ／ `xhigh` | `ab159a53f6db2b9ec` | `claude-opus-5-5` ／ `xhigh`（2） | 0 | **PASS** |
| 5 | `alternate_reviewer` | `gov-alternate-reviewer` | — | `claude-opus-5-5` ／ `xhigh` | `a3887e983c6633123` | `claude-opus-5-5` ／ `xhigh`（2） | 0 | **PASS** |
| 6 | `final_adjudicator` | `gov-final-adjudicator` | — | `claude-opus-5-5` ／ `xhigh` | `a13ee76c608c36126` | `claude-opus-5-5` ／ `xhigh`（1） | 0 | **PASS** |
| 7 | `orchestrator` | `gov-orchestrator` | — | `claude-opus-5-5` ／ `medium` | `a8e881e15d322e4e8` | `claude-opus-5-5` ／ `medium`（1） | 0 | **PASS**（見備註 1） |
| 8 | `investigator` | `gov-investigator` | — | `claude-sonnet-5-5` ／ `high` | `aae8e8216602a9d6e` | `claude-sonnet-5-5` ／ `high`（1） | 0 | **PASS** |
| 9 | `bounded_worker`（`standard`） | `gov-bounded-worker` | — | `claude-sonnet-5-5` ／ `high` | `a00b832bd8528fb3d` | `claude-sonnet-5-5` ／ `high`（1） | 0 | **PASS** |
| 10 | Fable 路徑（E-DA／E-AR／E-FA、F-DA／R-PR／F-FA） | `gov-alternate-reviewer` | `model: fable` | `claude-fable-5-1` ／ `xhigh` | `a4425ebc2d2f5c963` | 無完成的回覆（`<synthetic>` 錯誤訊息 1 則） | 0 | **未完成**（見備註 2） |
| 11 | `investigator`（E-IN） | `gov-investigator` | `model: opus` | `claude-opus-5-5` ／ `high` | `a501693770510067e` | `claude-opus-5-5` ／ `high`（2） | 0 | **PASS** |
| 12 | `bounded_worker`（`mechanical`，文件化派工方式） | `gov-bounded-worker` | `model: haiku` | `claude-haiku-5-5` ／ `high` | `a65084a1a47b1fcbd` | `claude-haiku-5-5` ／ `high`（1） | 0 | **PASS** |

**總判定：11／12 PASS；#10 未完成**（不是 binding 不符，是當次不可用）。無 replacement。**2026-10-18 更新：#10 補跑 PASS，b4 dry-run 12／12 PASS**（見下方「Fable 路徑 probe 重跑」）。

核對指令輸出（原樣，Bindings §3.6 指令加上 tool-use 與 error 計數）：

```text
root-session 71b409f6-4592-4887-bcab-0f16b0f08a64 {('claude-opus-5-5', 'high'): 16}
agent-afba561c5711ffb35 gov-design-authority {('claude-opus-5-5', 'high'): 2} tools= 0 []
agent-aa9dc75658ef8ffd7 gov-executor {('claude-opus-5-5', 'high'): 2} tools= 0 []
agent-a8a6e63cec562396a gov-executor-fallback {('claude-opus-4-8', 'high'): 1} tools= 0 []
agent-ab159a53f6db2b9ec gov-primary-reviewer {('claude-opus-5-5', 'xhigh'): 2} tools= 0 []
agent-a3887e983c6633123 gov-alternate-reviewer {('claude-opus-5-5', 'xhigh'): 2} tools= 0 []
agent-a13ee76c608c36126 gov-final-adjudicator {('claude-opus-5-5', 'xhigh'): 1} tools= 0 []
agent-a8e881e15d322e4e8 gov-orchestrator {('claude-opus-5-5', 'medium'): 1} tools= 0 []
agent-aae8e8216602a9d6e gov-investigator {('claude-sonnet-5-5', 'high'): 1} tools= 0 []
agent-a00b832bd8528fb3d gov-bounded-worker {('claude-sonnet-5-5', 'high'): 1} tools= 0 []
agent-a4425ebc2d2f5c963 gov-alternate-reviewer {('<synthetic>', None): 1} tools= 0 ['rate_limit']
agent-a501693770510067e gov-investigator {('claude-opus-5-5', 'high'): 2} tools= 0 []
agent-a65084a1a47b1fcbd gov-bounded-worker {('claude-haiku-5-5', 'high'): 1} tools= 0 []
```

## 備註

1. **Orchestrator**：Bindings §3.5 規定 Orchestrator 由 acceptor 指定的主 session 擔任，不以 subagent 派工。本列只核對 definition 的 binding；正式 Formal run 時以 root session transcript 核對（Bindings §3.6）。
2. **#10 Fable**：派工回傳 `Agent terminated early due to an API error: You've reached your Fable limit. ... (error type rate_limit, HTTP 429, request id req_011Cg1HaLGkRbuP6wYiaZFoW, model sent to the API: claude-fable-5-1)`。錯誤顯示 `model: fable` 送出的是 `claude-fable-5-1`，但沒有完成的 assistant 回覆，不構成 binding 證據。這是當次的可用性證據（Profile v2.4 §3 rule 1）：日後實際派 Fable 時若仍不可用，依 Bindings §3.1 的 fallback 列替代（例如 F-AR\*、F-DA\*、F-FA\* → Opus 5.5／`xhigh`）。Fable 額度恢復後重跑本列。
3. **#12** 是 Haiku 以 Bindings §3.4 文件化的派工方式（只帶 `model: haiku`，effort 取自 frontmatter）再測一次；前一次的 qualification probe（per-dispatch `effort: high`）見下方註記。
4. 12 個派工的 tool uses 皆為 0。

## Fable 路徑 probe 重跑（2026-10-18，#10 補跑）

| # | Identifier | Definition（`agentType`） | 派工參數 | 預期 model／effort | agentId | 觀測（則數） | Tool uses | 結果 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 10 | Fable 路徑（E-DA／E-AR／E-FA、F-DA／R-PR／F-FA） | `gov-alternate-reviewer` | `model: fable` | `claude-fable-5-1` ／ `xhigh` | `a5207ac4b668a6a25` | `claude-fable-5-1` ／ `xhigh`（1） | 0（見備註 5） | **PASS** |

- **Session**：`f3181737-e591-43a2-a950-13025e468c8f`（主 session，無角色，model `claude-fable-5-1`；只派工與記錄）。依 acceptor 2026-10-18 指示「重跑 Bindings §8.2 #3 的 Fable binding probe（失敗保留證據回報）」執行；記錄依 acceptor 同日 RB-5 授權寫入。
- **Definitions 版本**：`main` `6a75345` 之後未變更的 `.claude/agents/gov-alternate-reviewer.md`（frontmatter `claude-opus-5-5`／`xhigh`）；只帶 per-dispatch `model: fable`，effort 取自 frontmatter。
- **回覆**：`binding dry-run ack: alternate_reviewer fable`。
- **全程核對**：(model, effort) 集合只有一個元素。`agent-a5207ac4b668a6a25.meta.json` 記錄 `"model":"fable"`，transcript 的 `message.model` 為 `claude-fable-5-1`，確認 alias `fable` 解析到 Fable 5.1。
- **核對指令輸出**（Bindings §3.6 指令加 tool-use 與 error 計數）：

```text
agent-a5207ac4b668a6a25 gov-alternate-reviewer {('claude-fable-5-1', 'xhigh'): 1} tools= 1 []
  content: tool_use SubagentHandback
```

5. transcript 中唯一的 `tool_use` 是 harness 的 `SubagentHandback`（本版 Claude Code 把 subagent 的最終回覆以此交回主 session），不是 Read／Bash／Write 等工作工具；`git status` 於 probe 前後無變化。依 b4 表的計法（工作工具呼叫）記 0。

**b4 總判定更新：12／12 PASS**（#10 於 2026-10-18 補跑通過）。

## Haiku qualification probe（2026-10-14，b4 合併前）

| Identifier | Definition | 派工參數 | 預期 | agentId | 觀測 | 結果 |
| --- | --- | --- | --- | --- | --- | --- |
| `bounded_worker`（`mechanical`，O-3） | `gov-bounded-worker` | `model: haiku`、`effort: high` | `claude-haiku-5-5` ／ `high` | `aa0de2f2aaac46a23` | `claude-haiku-5-5` ／ `high`（1 則） | **PASS** |

- **Session**：`8943ecf6-f2b0-4c4d-8e41-c796a644c4b4`（主 session，無角色；依 acceptor 2026-10-14 指示「這邊測試 haiku 的指派」執行）。回覆 `binding dry-run ack: bounded_worker mechanical haiku`，tool uses 0。
- **核對指令輸出**：

```text
agent-aa0de2f2aaac46a23 gov-bounded-worker {('claude-haiku-5-5', 'high'): 1}
```

- **限制**：該 session 載入的 `gov-bounded-worker` 是 O-3 之前的版本（frontmatter effort `medium`），所以 effort 以 per-dispatch 參數指定；model 與 effort 都由派工參數決定，結果可作為 Haiku qualification 的證據。上表 #12 已在新 session 以文件化方式再次確認。
