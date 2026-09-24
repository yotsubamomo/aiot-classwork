# Phase acceptance record — SPEC v1.1（HW10 Taiwan Weather Forecast，`home_work_01/`）

- **紀錄類型**：Design Authority phase acceptance（治理 §3.8「Design Authority 負責 Formal 的適用 phase acceptance，包括跨 Ticket invariants、整合行為、累積 evidence 與未結 follow-up；phase acceptance MUST 引用已 closure 的第 4.7 節 Spec Integration Audit record，不得豁免或取代它」；Bindings §5「Design Authority phase acceptance 已完成」為 release gate 前提之一；Spec v1.1 §6「DA phase acceptance」列）
- **日期**：2026-09-24
- **執行角色**：`gov-design-authority`（Bindings §3.1：`design_authority` → `claude-fable-5-1`／`xhigh`）。實際 assignment 的核對證據依 Bindings §3.4 由派工者（Orchestrator）從 harness session 目錄取得並記入 run record；本紀錄不自證 binding。
- **派工**：Orchestrator run `run-20260924-hw01-formal`（[`../run/run-20260924-hw01-formal.md`](../run/run-20260924-hw01-formal.md)「Spec-level audit & phase acceptance」段），於 Spec Integration Audit closure 後自主派工（治理 §1.4：phase adjudication 是自主派工，不是 operator checkpoint）。
- **Outcome Contract**：[`../outcome-contract.md`](../outcome-contract.md)，**ACCEPTED 2026-09-23**（§8；normative §1–7 ＝ `c45ec61`；acceptance boundary AB-1～AB-17；§8.2 acceptor 原文含 Spec v1.1 生效與有範圍的 RB-5 workflow 授權）。
- **Derived contract**：[`../../spec/SPEC.md`](../../spec/SPEC.md) **v1.1**（EFFECTIVE；R-*、AC-01～AC-30、INV-1～INV-9、§7 AB→AC→R 矩陣）；derivation record [`derivation-SPEC.md`](derivation-SPEC.md)（§4：**整個 AB-1～AB-17 分配給這唯一一份 Spec**；§11：Tickets #18–#25）。
- **引用的 Spec Integration Audit record（治理 §4.7）**：[`../audit/spec-SPEC-c1-r1.md`](../audit/spec-SPEC-c1-r1.md) — **cycle 1，R1，VERDICT: CLOSURE**；受審 subject ＝ branch `home_work_01-hw10-implementation` HEAD **`720c0a0e82cb51917457354ab829e1bce714a5eb`**；Reviewer `gov-primary-reviewer`（fresh context，agent `aedb258b6c79233ef`，`claude-opus-5-5`／`xhigh`，run record 核對）。**本紀錄引用該 record，不豁免、不取代、不重做它。**
- **適用裁決**：[`decision-20260923-high-risk-categories.md`](decision-20260923-high-risk-categories.md)（H-1／H-2／H-3；A-1、A-2、A-4、A-5、A-6）；[`decision-20260923-spec-interpretation-rulings.md`](decision-20260923-spec-interpretation-rulings.md)（DR-1～DR-16，特別是 DR-12）；[DR-17](decision-20260924-ingestion-timestamp-semantics.md)；[DR-18](decision-20260924-ac22-workflow-dispatch-release-evidence.md)；[DR-19](decision-20260924-dashboard-state-mapping.md)；[`decision-20260924-unattended-run-policy.md`](decision-20260924-unattended-run-policy.md)。
- **Independence**：Executor worklog、`ACCEPTANCE.md`、Ticket audit、Spec Integration Audit 與 run record 的敘述都當作待驗證主張；第 2 節每一列都標明本 DA 自行核對了什麼（第 11 節列出指令與結果），其餘以已 closure 的 independent audit record 為依據。本 DA 未修改任何實作、測試、資料或 `doc/acceptance/`；未 commit；未 merge；未繳交；未觸碰 Vercel 或 repository variables。

---

## 1. 裁決

**SPEC v1.1 的 phase：ACCEPTED（2026-09-24）。**

受理的 subject 是 **`720c0a0`**（＝ `origin/home_work_01-hw10-implementation`，＝ PR #27 head），即 Spec Integration Audit 的受審 subject。`720c0a0` 之後的工作樹變更只有 `doc/governance/**`（run record 更新、Spec Integration Audit record、本紀錄），依 Bindings §7 為 record-only paths，不改變 subject identity（orch-default §7 P7）。

**本紀錄不是 release authorization，也不是 submission authorization**（治理 §3.8 末段、§5.2「work item completion 不授予 release permission」）：

| 陳述（治理 §3.8 要求分別陳述） | 狀態 | Authority |
| --- | --- | --- |
| Work item completion（#18–#25） | 完成——每張票依 Orchestrator Contract §7 結案，各有 CLOSURE 的 independent audit（第 2.1 節） | Orchestrator 依 Reviewer 判定 |
| **Phase acceptance（SPEC v1.1）** | **ACCEPTED（本紀錄）** | Design Authority |
| Run completion | 由 Orchestrator 於 run record「Terminus／completion report」陳述；不由本紀錄陳述 | Orchestrator |
| Release authorization（RB-1 合併進 `main`） | **未授權；未請求 Agent 執行。** Bindings §5／A-6 release gate 的「DA phase acceptance 已完成」一項由本紀錄滿足；合併本身是 acceptor 的決定與動作 | **acceptor（RB-1）** |
| Submission（RB-2） | **未授權** | **acceptor（RB-2）** |

---

## 2. 治理 §3.8 phase-acceptance 條件逐項核對

### 2.1 全部 Tickets 結案，且各有有效的 independent audit

| # | Issue 狀態（GitHub，DA 以 `gh` 核對） | 結案 subject | Audit records（verdict 行，DA 核對） | Binding（DA 依 Bindings §3.4 從 harness 核對） |
| --- | --- | --- | --- | --- |
| #18 | CLOSED 2026-09-23T18:39Z，結案 comment 引用 `7ee299c` | `7ee299c` | `issue-18-c1-r1.md` BLOCKING (F-1, F-2) → `issue-18-c1-r2.md` **CLOSURE** | Reviewer `a62303fcb67fae92b` ＝ `gov-primary-reviewer`／opus-5-5／xhigh；Executor `af0c7aafb2f44c730` ＝ `gov-executor`／opus-4-8／high |
| #19 | CLOSED 19:40Z，`0672020` | `0672020` | r1 BLOCKING (F-1, F-2, F-3) → r2 **CLOSURE** | `a1276a3cad339ff97`；`aa2d2cfcba2d60320` |
| #20 | CLOSED 20:32Z，`0f5f00e` | `0f5f00e` | r1 BLOCKING (F-1) → r2 **CLOSURE** | `ac58c89566afa531c`；`afaf4ffd7f682a155` |
| #21 | CLOSED 21:36Z，`f02a1df`（code `e27c1dc`） | `f02a1df` | r1 BLOCKING (F-1) → r2 **CLOSURE** | `a47fa01fa04086330`；`af810237365bf75d7` |
| #22 | CLOSED 22:31Z，`88b871e`（code `84060c9`） | `88b871e` | r1 **CLOSURE**（AC-22 依 DR-18） | `a75a924f3a0f75aa9`；`adebd2ac56ad6ccce` |
| #23 | CLOSED 2026-09-24T00:03Z，`5312c6f`（impl `fd654f3`） | `5312c6f` | r1 BLOCKING (F-1) → r2 **CLOSURE**（含 DR-19 回歸修正） | `a1bfaf2280c60aa15`；`abac86af43a37ad61` |
| #24 | CLOSED 01:46Z，`f9f9f15`（impl `386f30a`） | `f9f9f15` | r1 BLOCKING (F-1, F-2) → r2 **CLOSURE** | `a02d6ef56181e676b`；`a0b7cb41e09a556b4` |
| #25 | CLOSED 03:03Z，`75389e6`（anchor `6407d8b`） | `75389e6` | r1 BLOCKING (F-1, F-2, F-3) → r2 **CLOSURE** | `a8f6122cf722c0231`；`a0e8891359878c4f9` |

- 全部 16 份 Ticket audit records 都存在於 `doc/governance/audit/`，每份都有 Work Contract、受審 subject SHA、角色、binding 欄與 independence 說明（治理 §4.6），每份都含 decision A-1 要求的高風險類別核對段（DA 以 grep 確認 16／16 有 H-1／H-2／H-3 段）。R2 皆為同一 Reviewer 延續 R1 context 的 scoped closure review（Bindings §3.5 第 1 點允許）。沒有任何 audit 走到 Alternate Review 或 Final Adjudication；沒有 `diversity_lost`（Executor opus-4-8 對 Reviewer opus-5-5）。
- DA 自行以 Bindings §3.4 的核對指令讀取 session `e802a74c-bac7-44e4-afb3-27e58df56384` 的 `subagents/`：上表 8 個 Reviewer agent 與 8 個 Executor agent 的 `agentType`、`message.model`、`effort` 全部與 Bindings §3.1 mapping 一致；Spec Integration Audit 的 Reviewer `aedb258b6c79233ef` 亦為 `gov-primary-reviewer`／`claude-opus-5-5`／`xhigh`，且是與 8 個 Ticket-audit Reviewer 都不同的 agent identity（fresh context）。run record 的 binding 記載與 harness 一致。
- `doc/ticket/tickets.md` 索引：八張票皆「已結案」並填有結案 SHA，與 Issue 狀態及 run record 一致。

**結論：條件成立。**

### 2.2 Spec Integration Audit 已 closure（治理 §4.7）

- Record：`doc/governance/audit/spec-SPEC-c1-r1.md`，**VERDICT: CLOSURE**，subject **`720c0a0`**（DA 核對：`git rev-parse HEAD` ＝ `origin/home_work_01-hw10-implementation` ＝ PR #27 head ＝ `720c0a0e82cb51917457354ab829e1bce714a5eb`）。
- 五個 §4.7 範圍都有記載與判定：跨 Ticket invariants（§1）、Spec-level AC coverage 與 AB 涵蓋（§2）、整合行為（§3）、最終 subject 的 verification／audit coverage（§4）、traceability 與 boundary 符合性（§5）。
- 它是獨立的 audit instance（fresh Primary Reviewer，不是任何 Ticket audit 的 R3），且未重開已閉合的 Ticket finding（§6 明記 #18 R2 N-1 不重開的理由）。
- 兩項 findings F-1、F-2 皆 Low、non-blocking、已有 owner；本紀錄第 5 節處置。Reviewer 明記「Boundary 疑義：無。不需要 route 到 Design Authority」（§5.2、§8）——沒有治理 §1.2 所述、須 DA 先評估的 boundary 符合性 finding。
- Bindings §5「單 Ticket fast path：不採用」——本 Spec 有八張票，且另派了 Spec Integration Audit，符合。

**結論：條件成立。本紀錄引用該 record 作為 phase acceptance 的依據。**

### 2.3 跨 Ticket invariants INV-1～INV-9

| INV | Spec Integration Audit §1.2 | DA 補充核對（唯讀；第 11 節） |
| --- | --- | --- |
| INV-1 查詢語義只有一份 | HOLDS | — |
| INV-2 行為對等 | HOLDS（AppTest ＝ Flask test client ＝ 直接 SQL ＝ live，六區各 7 列） | — |
| INV-3 快照恰 6 × 7、永不部分寫入（H-3，A-2） | HOLDS（獨立推導 42／42；原子性；離線重建相同） | 提交的 `data.db`（sha256 `9bbf05bc…f542b`，與 audit 相同）：42 列、`(regionName, dataDate)` 重複 0、NULL 0、7 個不同日期 2026-09-24～09-30；`IngestionMetadata` ＝ `(1, '2026-09-24T02:24:50+08:00', 'F-D0047-091')` |
| INV-4 老師指定的名字不變（H-2，A-2） | HOLDS | `sqlite_master` 只有 `TemperatureForecasts` 與 `IngestionMetadata`；DDL 五欄逐字；老師 SQL：`SELECT DISTINCT regionName` → **6**（北部地區、中部地區、南部地區、東北部地區、東部地區、東南部地區）；`WHERE regionName = '中部地區'` → **7** |
| INV-5 金鑰零外洩（H-1，A-2） | HOLDS（金鑰字面值：追蹤檔案、全歷史、Issue／PR、截圖、live 資源皆 0） | `git ls-files` 只有 `home_work_01/.env.example`（512 個追蹤檔案）；`home_work_01/.env` 由 `home_work_01/.gitignore:12` 忽略 |
| INV-6 呈現層不呼叫 CWA | HOLDS | — |
| INV-7 標示要求（H-3，A-2） | HOLDS（README 逐行引用；live 圖例與資訊卡） | — |
| INV-8 Python 3.12 三處一致 | HOLDS（Vercel build log 為 acceptor 項目） | `720c0a0` 的 CI run `35949866460`（push）與 `35949869391`（pull_request）皆 `success` |
| INV-9 Scope class 分明 | HOLDS | — |

**結論：九條 invariant 在整合 subject 上成立；decision A-2 對 Spec Integration Audit 的義務（逐項核 INV-3／4／5／7 並對提交的 `data.db` 實際執行老師兩句 SQL）已由該 record §1.1、§7 履行，DA 另行執行得到相同結果。**

### 2.4 整合行為

Spec Integration Audit §3：ingestion → `data.db`（離線重建與提交結果完全相同、缺出處 fail-closed）→ shared module → 兩個呈現層（三方比較相等）→ live 部署（alias 的 `data-deployment-id` 對應 GitHub deployment `6629243424` ＝ commit `720c0a0`；`/`、`/api/health`、六區 `/series`、七個 `/api/days/<d>` 全部與本機相等；零外部請求；`Runtime.exceptionThrown` 0）；本機 `streamlit run app.py` 與 `python server.py` 皆可用；DR-19 的三種錯誤條件在 live 建置上呈現 error 狀態。「各部分可以一起運作；沒有發現整合層級的缺陷。」

**結論：成立。**

### 2.5 累積 evidence 充分

- **自動化**：Reviewer 在 `720c0a0` 乾淨匯出、無網路、無 `.env` 下 **152 passed**（BLOCKED_ATTEMPTS ＝ 0）；CI 對 `720c0a0` 的 push 與 pull_request run 皆 success（Python 3.12.14、152 passed、credential scan passed: 512 tracked files）——DA 以 `gh run list --commit 720c0a0` 核對兩個 run 的結論。
- **部署**：`smoke.py` 對受審 subject 的公開 preview alias PASS（Reviewer 於 2026-09-24T03:09:32Z 獨立執行）；部署 ↔ commit 對應已證明。
- **手動 ENHANCED 項目**：AC-17／18／19 由 Reviewer 以 CDP 在 live 建置上重驗（1280 與 375 裝置模擬），不只依賴 Executor 截圖。
- **文件**：AC-14 8／8 逐行引用；AC-27 由 Reviewer 給出正式結論。
- **R-DOC-4 驗收文件**：`doc/acceptance/ACCEPTANCE.md` 在 subject 內，逐條對應 AC／INV／AB 並如實標示 PENDING-ACCEPTOR 項目（#25 R2 已核對無 overclaim）。
- **Spec-level AC coverage**：AC-01～AC-30 **30／30 PASS**，其中 AC-07(e) 部分、AC-15 production、AC-22(c)、AC-23 build log、AC-30 後台截圖依既有裁決（DR-12、DR-18、#21 F-3）如實記為 acceptor／release 項目——這些不是 coverage failure（第 4 節）。
- **AB 涵蓋**：只有一份 derived Spec，derivation §4 把 AB-1～AB-17 全部分配給它；Spec §7 矩陣、derivation §4 表、`ACCEPTANCE.md` §4 三者一致；17／17 各有至少一條 PASS 的 AC；無分配缺口、無歧義重疊。治理 §4.7「最後一份未結 Spec」的全體涵蓋核對已在該 record §2.2 完成。

**結論：evidence 對最終 subject 直接成立，不需經 anchor 推論；充分。**

### 2.6 無未解且未經合法處置的 blocking finding；無影響完成的未決 design ambiguity

- 16 份 Ticket audit 的全部 blocking findings 都在同一 cycle 的 R2 判定為已解決；Spec Integration Audit 無 blocking finding。
- Run 中 route 到 DA 的三個 contract-sufficiency 問題（#18 R-1 → DR-17；#22 R-1 → DR-18；#23 RS-1／F-2 → DR-19）都已以 decision record 裁決，均為治理 §5.3 第 2 類（不改變 accepted 語義），後續 R2 或 Spec Integration Audit 都依其判定；沒有任何 Reviewer 對這些 determination 提出爭議。
- 沒有需要 Final Adjudicator 的 routing／review 爭議。
- 沒有 fail-closed 至 acceptor 的路徑；沒有 stop report。

**結論：成立。**

### 2.7 Review、verification 與結案版本可對應；審後變更已受相應驗證

- 各 Ticket 的結案 SHA、audit 的受審 SHA 與 Issue 結案 comment 一致（第 2.1 節）。
- `75389e6`（#25 結案）→ `720c0a0` 的 delta 為 `doc/governance/audit/issue-25-c1-r1.md`、`issue-25-c1-r2.md`、`run/run-20260924-hw01-formal.md` 與 **`doc/ticket/tickets.md`**（DA 以 `git diff --name-only 75389e6 720c0a0` 核對）。Spec Integration Audit 直接以 `720c0a0` 為 subject，所以這段 delta 在其 coverage 內（見第 5 節 F-1）。
- `720c0a0` → 目前工作樹：只有 `doc/governance/**`（record-only）；`git diff --name-only 720c0a0 HEAD` 為空。

**結論：成立。**

### 2.8 Traceability 與 boundary

- OC → Spec → Tickets → evidence 的鏈完整（Spec Integration Audit §5.1；derivation §11.7 五方一致性核對）。
- **單元外的改動只有 OC §8.2 授權的兩個 workflow 檔**：DA 核對 `git diff --name-only origin/main...HEAD -- . ':!home_work_01'` ＝ `.github/workflows/home_work_01-ci.yml`、`home_work_01-smoke.yml`；`origin/main`（`d42b1a7`）沒有任何 `.github/` 路徑。
- 沒有超出 accepted boundary 的功能（OPTIONAL 未做；REFERENCE 未出現；ENHANCED 標示為 dashboard-only）。
- 沒有 reserved action 被 Agent 執行：未合併（PR #27 OPEN）、未繳交、未動 Vercel／變數、未付費、無破壞性 git 操作。

**結論：成立。不需要 boundary determination；不需要 contract change。**

### 2.9 Worklog 已反映實際結果與 follow-up

run record 的 frontier 表與 checkpoint 逐票記載 subject、audit verdict、binding、routing 與 tracked items；`worklog/issue-25.md` 與 `ACCEPTANCE.md` §5／§6 列出 acceptor-deferred 項目與殘餘非阻擋項目。第 4 節把未結項目與其 owner／authority 正式列出，供 Orchestrator 完成報告引用。

---

## 3. 高風險類別（decision A-1／A-2）

| 類別 | Ticket audits（A-1） | Spec Integration Audit（A-2） | DA |
| --- | --- | --- | --- |
| H-1 憑證與機密 | #18、#19（靜態）、#20、#21、#22、#25 各有核對段，全 PASS | INV-5 HOLDS；金鑰字面值多處掃描 0 | `git ls-files` 無 `.env`；`.env` 被忽略 |
| H-2 老師指定介面 | #18、#19、#20、#23、#24、#25 各有核對段，全 PASS | INV-4 HOLDS；老師 SQL 6／7 | 老師 SQL 6／7；DDL 逐字；兩張表 |
| H-3 資料語義與標示 | #18、#19、#24、#25 各有核對段，全 PASS | INV-3、INV-7 HOLDS；獨立推導 42／42 | 42 列／0 重複／0 NULL／7 日 |

未結的高風險相關項目只有 #18 R2 N-1（第 4 節第 4 項），它是 non-blocking、已閉合 Ticket 內的 tracked item，並非 blocking finding 的 deferral（A-3 不適用）。

---

## 4. 未結項目：不是 phase-completion blocker，屬 acceptor 的 release 時／合併後動作或待授權的 follow-up

以下每一項都有既有的 accepted decision 作為「不是完成條件」的依據；本紀錄不新增、不刪除、不改變其地位，只正式列出（治理 §3.8「未結 follow-up」；DR-18 §4.3「DA phase acceptance 與 Orchestrator 完成報告 MUST 分別列出」）。

| # | 項目 | 依據 | 現況（DA 2026-09-24 核對） | Owner／authority | 完成時記到哪 |
| --- | --- | --- | --- | --- | --- |
| 1 | **AC-22(c)**：GitHub-hosted 的 live `workflow_dispatch` smoke run（run URL ＋ `GET /`、`/api/health` 兩個狀態碼＋`SMOKE PASS`） | **DR-18** §4.2：(c) 是 RB-1 之後的 release evidence，不是 #22、#25、Spec Integration Audit、phase acceptance 或 run completion 的完成條件；但 OC AB-17 的證據欄「workflow 執行紀錄」在 release 時**仍然必要**，不得省略或寫成已完成 | `gh api …/actions/workflows/home_work_01-smoke.yml` → **404**（workflow 未在預設分支 `main`，合併前無法 dispatch）；(a)(b) 已驗證 | **acceptor**：RB-1 合併後於 Actions 頁「Run workflow」（預設 `HW01_DEPLOY_URL` ＝ production），或依 acceptor 直接指示由 Agent 以 post-run Lightweight work item 執行（建立 workflow run 不在 RB-1～RB-6 之列） | `doc/acceptance/` AC-22 條目（DR-18 §4.3 末段）；dispatch 失敗時以新的 Lightweight work item 修正，不重開 Formal run |
| 2 | **AC-15 production URL smoke**：`https://aiot-hw01-weather.vercel.app` 的 `GET /` 與 `/api/health` | **DR-12**：合併後對 production URL 重跑 smoke 記為 release evidence，不是完成條件；Spec §6 Release 列、§9 已知風險 | production 目前 404（合併前的預期狀態；production 只在 RB-1 後更新）；受審 subject 的 preview alias smoke PASS 已作為 AC-15 PASS 證據 | **acceptor**（RB-1 之後）；第 1 項的預設 dispatch 就是這次 smoke 的機械化版本（DR-18 §4.2 第 2 點） | `doc/acceptance/` AC-15 條目 |
| 3 | **#21 F-3 Vercel 後台項目**（三項）：(a) Vercel build log 顯示 Python 3.12（AC-23／INV-8 的第三處補充確認）；(b) Root Directory ＝ `home_work_01` 的後台截圖（AC-30）；(c) **確認 Vercel 專案 env 未設定 CWA 金鑰**（AC-07(e) 後半、R-SEC-3、H-1） | #21 R1 F-3（Medium，acceptor-owned）與 R2 disposition；`ACCEPTANCE.md` §5-3；Spec Integration Audit AC-07／AC-23／AC-30 列與 §8。這些是 acceptor 帳號內的設定與日誌，任何 Agent 都無法取得（治理 §1.5 第 4 項、RB-3） | 依現有授權可取得的部分都已驗證：`.python-version` ＝ `3.12`（部署設定）、runtime 不讀 env、live 部署在沒有任何 secret 下正常服務、root 無設定檔、live 由 `home_work_01/vercel.json` 的單一 function 服務 | **acceptor**（RB-3） | `doc/acceptance/` 對應條目（(c) 完成後 AC-07(e) 由 PENDING-ACCEPTOR 改為 PASS） |
| 4 | **#18 R2 N-1 結案後 follow-up**（Medium，non-blocking）：offline ingestion 路徑（`--from-json` 搭配 sidecar 或 `--acquired-at`）**不驗證取得時間的格式**，格式不良的值會被原樣寫入 `IngestionMetadata.ingestedAt`（R-DB-5「ISO 8601 含 `+08:00`」；DR-17 §4.1、§4.3(3)）。提交的 `data.db` 與 sidecar 都是合法值（`2026-09-24T02:24:50+08:00`），online 路徑正確；風險只在日後有人手動以不良參數執行離線重建。Spec Integration Audit F-2 指出它在交付文件中沒有具名 owner；本節即為具名 | 治理 §1.2：follow-up 在 acceptor 接受並授權前只是 **tracked item**，不得作為新工作執行；Bindings §4 第 3 列：已結案工作之後的單點修正 ＝ Lightweight、新的 work item、需要 acceptor 的直接指示作為其 Outcome Contract；**decision A-4**：修正觸及 H-3「觸及的工作」（DR-17 ingestion 時間戳路徑；驗證邏輯），**MUST 執行 independent audit**，worklog 不得標「依 policy 未要求」。可與 #18 R2 N-2（Low，T-1 常數時鐘）一併處理 | 未修正；不影響提交的任何產物；不是 Spec 完成條件 | **Orchestrator** 在完成報告中具名列出並向 acceptor 提出；**acceptor** 決定是否授權（直接指示即為該 Lightweight work item 的 Outcome Contract）；授權後的 Executor 與 Reviewer 依 A-4 派工。DA 對是否、何時執行不作要求：它不是 release 或 submission 的前提；acceptor 可以在 RB-1 前後任一時點處理，或決定不處理並留為已知限制 | 新的 Lightweight worklog `doc/governance/worklog/<YYYYMMDD>-<slug>.md` 與其 audit record |
| 5 | **`ACCEPTANCE.md` 的紀錄措辭小問題**（#25 R2 N-2、Spec Integration Audit O-5）：§0 把 `6407d8b` 標為「Final subject」（verification anchor 的寫法）；tracked-file 數 508／510 對 HEAD CI 的 512；§6→§8→§7 章節順序；N-1 列的「Fail-closed today」實為 fail-open 的描述 | 皆 Low、non-blocking、已閉合；不影響任何判定 | 存在於 subject 內（`doc/acceptance/` 不是 record-only） | 可選。若要修正，屬結案後的 Lightweight 文件修正（Bindings §4 第 2／3 列），且會改變 subject identity，需相應的（有限度的）審後驗證；**不修正亦可**。所有下游紀錄一律以 **`720c0a0`** 為 Spec Integration Audit 與本 phase acceptance 的 subject，以 `6407d8b` 為行為驗證 anchor | — |
| 6 | **快照時效**（Spec Integration Audit O-2）：提交的快照涵蓋 2026-09-24～09-30 | OC Q3 A：MVM 使用準備好的快照，refresh 屬 OPTIONAL——已接受的語義，不是缺陷；程式與測試不依賴當日日期 | — | 若 acceptor 想在繳交（RB-2）前 Refresh：那是改動 `data.db` 的結案後 Lightweight work item，觸及 H-2／H-3，依 A-4 需要 independent audit。DA 不建議也不反對；只說明其治理路徑 | — |

第 1～3 項合起來就是 **A-6 release gate 的 acceptor 項目**（DR-18 §4.2 第 3 點、`ACCEPTANCE.md` §5）。第 4～6 項不是 release gate 項目。

---

## 5. 對 Spec Integration Audit findings 的處置與觀察

### F-1（Low）— 「content subject `75389e6`」的說法不精確；`doc/ticket/tickets.md` 不是 record-only path

- **DA 確認**：Bindings §7 明定 record-only paths **只有** `doc/governance/**`。`75389e6..720c0a0` 除了三個 `doc/governance/**` 檔案外還改了 `doc/ticket/tickets.md`（#25 那一列的狀態與 SHA）。因此 run record 第 96 行「`doc/governance/**` audit-record commits on top are record-only … excluded from subject identity」對 `tickets.md` 那一項不成立。
- **對 coverage 的影響：無。** Spec Integration Audit 明確以 `720c0a0` 為 subject 並直接驗證了 `720c0a0` 的 CI 與部署；`tickets.md` 是索引檔，不影響任何產品行為。
- **處置**：(1) 本紀錄與 Orchestrator 完成報告一律寫「**Spec Integration Audit subject ＝ `720c0a0`；phase acceptance subject ＝ `720c0a0`**」，不寫「content subject `75389e6`（delta 為 record-only）」；(2) 自 `720c0a0` 起，若之後只 commit `doc/governance/**`，subject 仍是 `720c0a0`；若再改 `doc/ticket/` 或 `doc/acceptance/`，那是 subject 變更，須依治理 §3.8 識別並由 Reviewer／DA 判定必要的後續驗證；(3) DA **不**提議把 `doc/ticket/` 改列為 record-only——那是 Bindings 變更（acceptor），且不是必要動作。
- Owner：Orchestrator（記入 run record 與完成報告）。

### F-2（Low）— #18 R2 N-1 沒有具名 owner

- 已於第 4 節第 4 項具名：Orchestrator 於完成報告提出 → acceptor 授權與否 → 授權後為 Lightweight work item，A-4 independent audit 必要。`ACCEPTANCE.md:172` 的措辭（「Fail-closed today」）可一併更正但不是必要條件（第 4 節第 5 項）。

### 觀察（不需處理）

- O-1（375 px headless 截圖假象，量測以 CDP 裝置模擬為準）、O-3（Dashboard 頁面本身未標示區域值為推導值——契約不要求，AB-13／R-DOC-2 要求的是技術文件，且頁面無相反措辭）、O-4（四個小型 CLI helper 無 docstring，不影響 AC-27）：DA 同意 Reviewer 的判定，均不是 finding。

---

## 6. Bindings §5／decision A-6 release gate 材料的狀態（供 acceptor 參考；不是本紀錄的授權）

| Gate 項目 | 狀態 | 依據 |
| --- | --- | --- |
| Formal：全部 Ticket 依 Orchestrator Contract §7 結案 | 完成 | 第 2.1 節 |
| Formal：每份 Spec 的 Spec Integration Audit 已 closure | 完成 | `spec-SPEC-c1-r1.md` |
| Formal：Design Authority phase acceptance 已完成 | **完成（本紀錄）** | 第 1 節 |
| README 的安裝與執行步驟已實際跑過，結果與證據記在 worklog | 完成 | `worklog/issue-25.md` §5（Executor 乾淨 3.12.14 venv 逐步實跑）；Spec Integration Audit AC-12 列（Reviewer 另一乾淨 venv 部分重跑） |
| 沒有追蹤中的機密：`git ls-files` 不含 `.env`，diff 內沒有金鑰字串 | 完成 | Spec Integration Audit INV-5（金鑰字面值全歷史 0）；CI credential scan passed（512 tracked files）；DA `git ls-files` 核對 |
| A-6 另附：A-2 的 SQL 執行結果 | 完成 | **`spec-SPEC-c1-r1.md` §1.1**（對 `720c0a0` 的 `data.db` 執行：6 與 7）；DA 本紀錄第 2.3 節重跑結果相同；`ACCEPTANCE.md` §5 引用 Executor 的 wl25 §6 結果 |
| A-6 另附：A-5 的最後一次 CI 結果引用 | 完成 | HEAD `720c0a0` 的 run **`35949866460`**（push）與 `35949869391`（pull_request），皆 success、152 passed、Python 3.12.14、credential scan passed；`ACCEPTANCE.md` §0／§5 引用的 `35948664254` 是 anchor `6407d8b` 的 run，對 anchor 有效 |

**A-6 位置條款的說明（DA 依治理 §5.1 對自己 assurance 決定的 clarification；不改變 gate 的實質，也不改變任何 accepted 語義）**：A-6 寫「記在 `doc/acceptance/`」。`ACCEPTANCE.md` 是 subject 的一部分，而 A-2 的 SQL 執行結果由定義上在它之後才產生（Spec Integration Audit 的義務），對 HEAD 的最後一次 CI run 也一樣；若為了把這兩個引用寫回 `ACCEPTANCE.md` 而再 commit，就會改變受審 subject 並需要再一輪驗證。因此 A-6 的「另附」義務以下列方式視為已滿足：`ACCEPTANCE.md` §5（A-6 材料清單）＋ `spec-SPEC-c1-r1.md` §1.1（A-2 結果）＋ 本紀錄第 6 節（HEAD CI run 引用）。Acceptor 若仍希望 `doc/acceptance/` 內有字面引用，可指示為結案後的 Lightweight 文件修正（第 4 節第 5 項的路徑）；這是 acceptor 的選擇，不是 DA 的要求。

上述清單只說明 gate 材料是否備齊；**是否合併（RB-1）由 acceptor 決定**。

---

## 7. 是否改變 accepted 語義；boundary determination

**否。** 本紀錄不 derive 新的 contract、不修改 Spec、不新增或移除任何 AC／INV／gate；第 4 節的每一項都只是引用既有 accepted decisions（DR-12、DR-18、#21 F-3 disposition、A-4、Bindings §4）所已經確立的地位。Phase acceptance 是治理 §3.8 授予 DA 的判定，不是接受或授權行為（治理 §1.2、§5.2）。

**Boundary determination（治理 §1.2）**：不需要——沒有任何 Reviewer 提出 boundary 符合性 finding，Spec Integration Audit §5.2 明記無 boundary 疑義；沒有 fail-closed 的路徑。

---

## 8. 受影響 work items

| 對象 | 影響 |
| --- | --- |
| #18–#25 | 無重開；結案狀態不變。 |
| Orchestrator（run record、完成報告） | 記錄本 phase acceptance；完成報告 MUST：(1) 以 `720c0a0` 為 subject（第 5 節 F-1）；(2) 分別陳述 work item completion、phase acceptance、run completion、release authorization（治理 §3.8）；(3) 逐項列出第 4 節第 1～3 項為 acceptor 的 release 項目、第 4 項為待 acceptor 授權的 tracked follow-up（含 A-4 audit 要求）；(4) 不得把任何 PENDING-ACCEPTOR 項目寫成已完成。 |
| acceptor | 第 4 節第 1～3 項（RB-1、RB-3）、第 4 項（是否授權 Lightweight follow-up）、RB-1 合併、RB-2 繳交。 |
| Spec v1.1、derivation record、Bindings | 不需修改。 |

---

## 9. 需要其他 authority 的事項

| 事項 | Authority | 理由 | 是否阻擋 phase acceptance |
| --- | --- | --- | --- |
| 合併 PR #27 進 `main`（release） | acceptor | RB-1；Bindings §5／A-6 gate 材料見第 6 節 | 否 |
| 合併後產生 AC-22(c) run 與 AC-15 production smoke | acceptor（或依其直接指示的 Agent） | DR-18、DR-12；OC AB-17 證據欄 | 否 |
| #21 F-3 三項 Vercel 後台確認 | acceptor | RB-3；治理 §1.5 第 4 項 | 否 |
| 授權 #18 R2 N-1（＋N-2）的 Lightweight follow-up | acceptor | 治理 §1.2 tracked item；Bindings §4 第 3 列；A-4 | 否 |
| 繳交作業 | acceptor | RB-2 | 否 |
| Final Adjudicator | — | 沒有 routing 或 review 爭議 | — |

沒有任何事項需要 acceptor 才能完成本 phase acceptance；本紀錄不向 acceptor 請求任何動作，只列出 OC 原本就分配給 acceptor 的 release 與 reserved 動作。

---

## 10. Phase acceptance 的效力與後續

- 本 phase 的 accepted subject 為 `720c0a0`。之後任何對 `home_work_01/`（含 `doc/acceptance/`、`doc/ticket/`）或兩個 workflow 檔的變更，都不在本 phase acceptance 的 coverage 內：依 Bindings §4 屬「已結案工作之後的單點修正」，以 acceptor 的直接指示為 Outcome Contract 開新的 Lightweight work item；觸及 H-1／H-2／H-3「觸及的工作」者依 A-4 需 independent audit。
- 只 commit `doc/governance/**`（本紀錄、run record 更新、audit record）不改變 subject identity。

---

## 11. Evidence（DA 自行執行，全部唯讀；未印出任何金鑰）

- 讀取：Bindings b1 §0–§9；治理 v2.0 §1.2、§1.4、§1.5、§3.8、§4.6、§4.7、§5.1–§5.4；Outcome Contract 全文；Spec v1.1 全文；derivation record 全文；decision A-1～A-7；DR-12（spec-interpretation-rulings）；DR-17、DR-18、DR-19 全文；`spec-SPEC-c1-r1.md` 全文；`issue-25-c1-r2.md` 全文；`issue-18-c1-r2.md` §4–§5（N-1）；`issue-21-c1-r2.md` F-3 段；16 份 Ticket audit 的標頭欄與 verdict 行；`ACCEPTANCE.md` 全文；`tickets.md` 全文；run record 全文。
- `git rev-parse HEAD` ＝ `720c0a0e82cb51917457354ab829e1bce714a5eb` ＝ `origin/home_work_01-hw10-implementation`；`origin/main` ＝ `d42b1a7`；`git status --porcelain` 只有 `M doc/governance/run/run-20260924-hw01-formal.md` 與 `?? doc/governance/audit/spec-SPEC-c1-r1.md`；`git diff --name-only 720c0a0 HEAD` 為空。
- `git diff --name-only 75389e6 720c0a0` ＝ `issue-25-c1-r1.md`、`issue-25-c1-r2.md`、`run-20260924-hw01-formal.md`、**`doc/ticket/tickets.md`**。
- `git diff --name-only origin/main...HEAD -- . ':!home_work_01'` ＝ 兩個 `home_work_01-*.yml`；`git ls-tree -r origin/main .github` 計數 0。
- `git ls-files | grep -i '\.env'` ＝ `home_work_01/.env.example`；追蹤檔案 512；`git check-ignore -v home_work_01/.env` → `home_work_01/.gitignore:12:.env`。
- `data.db` 唯讀（`mode=ro`）：sha256 `9bbf05bc6cc803444c8760432d6b484699c597f751fa16cb58bfbb5a0dbf542b`；表 `IngestionMetadata`、`TemperatureForecasts`；DDL 五欄逐字；`SELECT DISTINCT regionName` → 6（北部地區、中部地區、南部地區、東北部地區、東部地區、東南部地區）；`WHERE regionName = '中部地區'` → 7（id 8–14，2026-09-24～09-30）；42 列；重複 0；NULL 0；7 個不同日期；`IngestionMetadata` ＝ `(1, '2026-09-24T02:24:50+08:00', 'F-D0047-091')`。
- `gh issue list`：#18–#25 全部 CLOSED（2026-09-23T18:39Z … 2026-09-24T03:03Z）；每張最後一則 comment 為「Closed by Formal-run audit closure. Subject `<sha>`」，SHA 與 `tickets.md`、run record 一致。`gh pr list`：#27 OPEN，head `720c0a0` → `main`。
- `gh run list --commit 720c0a0`：`35949866460`（push）與 `35949869391`（pull_request）皆 `completed`／`success`。
- `gh api …/actions/workflows/home_work_01-smoke.yml` → 404（合併前無法 dispatch，與 DR-18 E-2 一致）。
- Bindings §3.4 核對指令對 session `e802a74c-bac7-44e4-afb3-27e58df56384/subagents/`：8 個 `gov-primary-reviewer`（Ticket audits）＋ 1 個 `gov-primary-reviewer`（`aedb258b6c79233ef`，Spec Integration Audit）皆 `claude-opus-5-5`／`xhigh`；8 個 `gov-executor` 皆 `claude-opus-4-8`／`high`；4 個 `gov-design-authority` 皆 `claude-fable-5-1`／`xhigh`。agent id 與 run record 逐一相符。
- Grep：16 份 Ticket audit 與 Spec Integration Audit 皆含 `高風險`／`High-risk`／`A-1` 段。
