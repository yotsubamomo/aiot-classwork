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
