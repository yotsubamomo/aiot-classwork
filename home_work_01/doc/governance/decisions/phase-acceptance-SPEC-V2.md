# Phase acceptance record — SPEC-V2 v2.2（HW01 Weather Map V2，`home_work_01/`）

- **紀錄類型**：Design Authority phase acceptance（治理 §3.8「Design Authority 負責 Formal 的適用 phase acceptance，包括跨 Ticket invariants、整合行為、累積 evidence 與未結 follow-up；phase acceptance MUST 引用已 closure 的第 4.7 節 Spec Integration Audit record，不得豁免或取代它」；orch-default §7 P10；Bindings §5「Design Authority phase acceptance 已完成」為 release gate 前提之一；SPEC-V2 §6.4「DA phase acceptance」列）。
- **日期**：2026-09-26。
- **執行角色**：`gov-design-authority`（Bindings §3.1：`design_authority` → `claude-fable-5-1`／`xhigh`）。實際 assignment 的核對依 Bindings §3.4 由派工者（Orchestrator）從 harness session 目錄取得並記入 run record；本紀錄不自證 binding。DA 唯讀 harness 觀察：session `05b8408b-260a-46d3-a4fe-ec07e3ec365a` 有五個 `gov-design-authority` agent，四個對應 run record 的 DV-20～DV-23（`a55412906736de2d3`、`a88338ce175849f25`、`a18427eb4267b5ab1`、`a3d6c036885e71afe`），第五個 `aaabccabe2db8806a` 應為本次 phase-acceptance 派工——皆 `claude-fable-5-1`／`xhigh`；以派工者核對為準。
- **派工**：Orchestrator run `run-20260925-hw01-v2-formal`（[`../run/run-20260925-hw01-v2-formal.md`](../run/run-20260925-hw01-v2-formal.md)），於 Spec Integration Audit closure 後自主派工（治理 §1.4、§3.8：phase adjudication 是自主派工，不是 operator checkpoint）。
- **Outcome Contract**：[`../outcome-contract-v2.md`](../outcome-contract-v2.md)，**ACCEPTED 2026-09-25**（normative §1–8 ＝ candidate `69c5a049104b2fd96289d10ff938c2c8a6d59bd4`；§9.1 acceptor 原文；acceptance boundary AB-V2-1～13；§6 assurance path；A-2「金鑰填入 Vercel 由 acceptor 於部署階段親自執行」）。V1 Outcome Contract 與 Spec v1.1 為 inherited baseline，normatively 不變。
- **Derived contract**：[`../../spec/SPEC-V2.md`](../../spec/SPEC-V2.md) **v2.2**（DV-23 註記更正，commit `2771a54`；R-V2-\*、AC-V2-01～23、INV-V2-1～9、§6.3、§6.4、§7 矩陣；以參照繼承 V1 Spec v1.1）；derivation record [`derivation-SPEC-V2.md`](derivation-SPEC-V2.md)（§4：**AB-V2-1～13 全部分配給這唯一一份 derived Spec**；§6 高風險類別；§11 #1／#4；§15 Tickets #35–#41）；DV-20～DV-23 decision records。
- **引用的 Spec Integration Audit record（治理 §4.7）**：[`../audit/spec-SPEC-V2-c1-r1.md`](../audit/spec-SPEC-V2-c1-r1.md) — **cycle 1，R1，VERDICT: CLOSURE（可完成範圍）**；受審 subject ＝ **最終整合 subject `9902026cc41725524f154185aeebd59057fbdadf`**（branch `home_work_01-v2-implementation`）；Reviewer `gov-primary-reviewer` agent `ad2f24768b95d2567`（fresh context；`claude-opus-5-5`／`xhigh`；`diversity_lost` 已記）。**本紀錄引用該 record，不豁免、不取代、不重做它。** 該 record 明記 AC-V2-17(c)、AC-V2-22 觀測部分、AC-V2-03 preview 抽樣與 decision A-6 preview 紀錄為 **BLOCKED（RB-3）、不記為 PASS**，並把「phase acceptance 是否可在其 BLOCKED 下先行」route 給 DA（其 §8、§12）——本紀錄第 3 節裁決之。
- **適用裁決**：[`decision-20260923-high-risk-categories.md`](decision-20260923-high-risk-categories.md)（H-1／H-2／H-3；A-1～A-7）與 derivation §6 對 V2 的具體化；DV-1～DV-23；V1 [`phase-acceptance-SPEC.md`](phase-acceptance-SPEC.md)（格式與「acceptor 項目不是完成條件」先例）；[`decision-20260924-unattended-run-policy.md`](decision-20260924-unattended-run-policy.md)（OC-V2 §6 沿用）。
- **Independence**：Executor worklog、`ACCEPTANCE-V2.md`、七張 Ticket 的 audit records、Spec Integration Audit record、run record 與派工文字皆當作待驗證主張。第 2 節每一列標明 DA 自行核對了什麼（第 11 節列指令與結果），其餘以已 closure 的 independent audit records 為依據。本 DA 未修改任何實作、測試、資料、`doc/acceptance/`、`doc/ticket/`、Spec 或 Bindings；未 commit；未 merge；未繳交；未讀 `home_work_01/.env`；未接觸 Vercel 專案、環境變數或 log；未使用任何 CWA 金鑰；未對 CWA 發出請求。

---

## 1. 裁決

**SPEC-V2 v2.2 的 phase：ACCEPTED（可完成範圍；2026-09-26）。**

- **受理的 subject 是 `9902026`**，即 Spec Integration Audit 的受審 subject。審查時 HEAD `bc74f9c`（`origin/main` 仍為 V2 BASE `08e158e`，未合併）；`git diff --name-only 9902026 bc74f9c` ＝ `doc/governance/audit/issue-41-c1-r1.md`、`doc/governance/audit/spec-SPEC-V2-c1-r1.md`、`doc/governance/run/run-20260925-hw01-v2-formal.md`、`doc/governance/worklog/issue-41.md`（Bindings §7 record-only）＋ `doc/ticket/tickets-v2.md`（第 2.7 節的 DA determination：#41 索引列的狀態與 commit 欄，不影響 subject identity 的驗證需求）。
- **可完成範圍**＝ SPEC-V2 全部 AC-V2-01～23、INV-V2-1～9、V1 INV-1～9、§6.3 定向重驗、AB-V2-1～13 的分配與涵蓋、整合行為、traceability 與 boundary，**扣除**下列四項在 acceptor 填入 Vercel `CWA_API_KEY`（RB-3）前無法取得證據的部分：**AC-V2-17(c)**；**AC-V2-22 觀測部分**；**AC-V2-03 preview 抽樣**；**decision A-6 preview 觀測驗證紀錄**（連帶 AB-V2-2／10／13 的部署部分與 INV-V2-2 的 Vercel 平台面）。這四項的處理是第 3 節的裁決：**phase acceptance 現在授予；四項作為本 phase 的殘餘義務 P-1～P-4 帶出，由獨立 Reviewer 在金鑰填入後重現，並以 DA addendum 結清；在結清前，本 phase acceptance 不使任何一項成為 PASS，Outcome Contract closure 與 Bindings §5／SPEC-V2 §6.4 的 release gate 也不因本紀錄而視為滿足。**

**本紀錄不是 run completion、不是 release authorization、不是 submission authorization、不是 Outcome Contract closure**（治理 §3.8 末段「MUST 分別陳述，不得互相冒充」；§5.2「work item completion 不授予 release permission」）：

| 陳述（治理 §3.8） | 狀態 | Authority |
| --- | --- | --- |
| Work item completion（#35–#41） | 完成——七張票依 Orchestrator Contract §7 結案，各有 CLOSURE 的 independent audit（第 2.1 節）；#41 為「可完成範圍」結案，P-1～P-4 記 BLOCKED（不是 FAIL） | Orchestrator 依 Reviewer 判定 |
| **Phase acceptance（SPEC-V2 v2.2）** | **ACCEPTED（可完成範圍；本紀錄）**；殘餘義務 P-1～P-4 見第 3 節；結清以 addendum 記錄（第 10 節） | Design Authority |
| Run completion | 由 Orchestrator 於 run record「Terminus／completion report」陳述；治理 §3.8 允許在「剩餘工作皆受第 1.5 節真正 boundary 阻擋且已記錄」時結束 run——P-1～P-4 受 RB-3 阻擋即屬此情形 | Orchestrator |
| Outcome Contract closure（OC-V2 全 acceptance boundary） | **未完成**：AB-V2-2／10／13 的部署部分待 P-1～P-3 的 Reviewer 重現 | acceptor（closure 判斷）；DA addendum 提供 phase 面的確認 |
| Release authorization（RB-1 合併進 `main`） | **未授權；未請求 Agent 執行。** Bindings §5 gate 的「DA phase acceptance 已完成」由本紀錄滿足**可完成範圍**；SPEC-V2 §6.4 Release 列的「acceptor 已填 Vercel 金鑰的 preview 驗證」與 decision A-6 的「preview 觀測驗證紀錄」**尚未具備**（第 6 節） | **acceptor（RB-1）** |
| Submission（RB-2） | **未授權** | **acceptor（RB-2）** |

---

## 2. 治理 §3.8 phase-acceptance 條件逐項核對

### 2.1 全部 Tickets 結案，且各有有效的 independent audit

| # | Issue 狀態（GitHub，DA 以 `gh issue list` 核對） | 結案 code anchor（索引 `tickets-v2.md`） | Audit records（verdict 行，DA 以 grep 核對） | Binding（DA 依 Bindings §3.4 從 harness 核對） |
| --- | --- | --- | --- | --- |
| #35 | CLOSED 2026-09-25T17:08:32Z | `5f0dbc3` | `issue-35-c1-r1.md` BLOCKING (F-1) → `issue-35-c1-r2.md` **CLOSURE** | Reviewer `ab39e3a58cdb76117`；Executor `a1eef729c5e6bcebf` |
| #36 | CLOSED 18:09:25Z | `f63ebb1` | `issue-36-c1-r1.md` **CLOSURE** | `a7afb069135999b78`；`a97513f8b8d5b2091` |
| #37 | CLOSED 19:21:32Z | `7a3b469` | `issue-37-c1-r1.md` **CLOSURE** | `a00dc725e9833283f`；`a85fb9fb98d937131` |
| #38 | CLOSED 2026-09-26T02:35:12Z | `286ee9d` | r1 BLOCKING (F-1) → `issue-38-c1-r2.md` **CLOSURE** | `aee926af828c07bf6`；`a85542bddce5a490b` |
| #39 | CLOSED 06:45:17Z | `f3bf245` | r1 BLOCKING (F-1) → `issue-39-c1-r2.md` **CLOSURE**（含 DV-22 §4.1 逐項核對） | `a2832f7b12b48dec1`；`af8f083fccf7b5395` |
| #40 | CLOSED 08:40:15Z | `fedffdd` | `issue-40-c1-r1.md` **CLOSURE** | `a0ea5bfb8f8f1ce75`；`aadf0a28e2b419e94` |
| #41 | CLOSED 09:54:13Z | `9902026`（final subject） | `issue-41-c1-r1.md` **CLOSURE**（可完成範圍；P-1～P-4 BLOCKED，未記 PASS） | `a16d3b7e242f9d1aa`；`a7f0755757b237151` |

- 十份 Ticket audit records 都在 `doc/governance/audit/`，每份有 Work Contract、受審 subject SHA、角色、binding 欄與 independence 說明（治理 §4.6）；A-1 要求的高風險核對段：九份以「高風險類別核對／High-risk／decision A-1」為題，`issue-35-c1-r2.md` 以表列方式重述 H-1（四類失敗零洩漏、git／evidence 掃描）與 H-3（「如發布」）的修正結果——A-1「R2 對該節的修正結果重述」在實質上成立。三個 R2 皆為同一 Reviewer 延續 R1 context 的 scoped closure review（Bindings §3.5 第 1 點允許）。沒有任何 audit 走到 Alternate Review 或 Final Adjudication。每份 record 依 Bindings §5 記 `diversity_lost`（Executor 與 Primary Reviewer 同為 `claude-opus-5-5`，b2 override；合法）。
- DA 自行以 Bindings §3.4 指令讀取 session `05b8408b-260a-46d3-a4fe-ec07e3ec365a/subagents/`（20 個 agent）：上表 7 個 Reviewer 皆 `gov-primary-reviewer`／`claude-opus-5-5`／`xhigh`；7 個 Executor 皆 `gov-executor`／`claude-opus-5-5`／`high`；與 Bindings §3.1（b2 override）及 run record 逐一相符。
- `doc/ticket/tickets-v2.md`：七張票皆「已結案」並填結案 SHA，與 Issue 狀態及 run record 一致。

**結論：條件成立。**

### 2.2 Spec Integration Audit 已 closure（治理 §4.7）

- Record：`doc/governance/audit/spec-SPEC-V2-c1-r1.md`，**VERDICT: CLOSURE**，subject **`9902026`**（DA 核對 `git log 9902026..HEAD` 只有四個 record-only commit 與索引列；第 2.7 節）。
- 五個 §4.7 範圍都有記載與判定：跨 Ticket invariants（§2：INV-V2-1～9、V1 INV-1～9，含 INV-3 重新推導與老師 SQL）、Spec-level AC coverage 與 AB 涵蓋（§3、§3.2：AB-V2-1～13 全部分配、S-1～S-11／C-1～C-5 可到達，且因 SPEC-V2 為 OC-V2 唯一 derived Spec，同時完成「最後一份未結 Spec」的全 boundary 核對）、整合行為（§4：六個既有檢查重跑＋Reviewer 自寫跨票情境 71/71）、最終 subject 的 verification／audit coverage（§5：各票 closing anchor 皆在 `9902026` 祖先鏈；票後整合變更由 #41 R1 審查並在最終 subject 重驗）、traceability 與 boundary 符合性（§6：無超出 boundary、無需 DA 裁決的語義不足或 boundary 疑義）。
- 它是獨立的 audit instance：Reviewer `ad2f24768b95d2567` 與七個 Ticket-audit Reviewer 皆為不同 agent identity（DA 自 harness 核對），fresh context；不是任何 Ticket audit 的 R3；未重開已閉合的 Ticket finding（其 §11 O-2 明記不重開 #41 R1 F-1）。
- 唯一 finding **F-1 為 Low、non-blocking、已有 owner**（第 5 節處置）；Reviewer 明記無 boundary 符合性 finding、無需 route DA 的契約語義不足——沒有治理 §1.2 所述須 DA 先評估的 boundary finding。
- Bindings §5「單 Ticket fast path：不採用」——本 Spec 有七張票，且另派了 Spec Integration Audit，符合。
- **RB-3 閘門項目在該 record 中一律記為 BLOCKED，未有任何一項被記為 PASS**（其 §3 判定用語、§3.2 末段、§8、§14）；「CLOSURE」的範圍限於可完成範圍——DA 核對其 §14 的結論句與此一致。

**結論：條件成立。本紀錄引用該 record 作為 phase acceptance 的依據。**

### 2.3 跨 Ticket invariants

| INV | Spec Integration Audit §2 | DA 補充核對（唯讀；第 11 節） |
| --- | --- | --- |
| INV-V2-1 預報路徑 CWA-free、key-free | 成立（封網無金鑰 100 組 0 差異、0 網路嘗試） | — |
| INV-V2-2 金鑰零外洩、兩個授權位置（H-1） | 成立（repository 與本機）；**Vercel 平台面 BLOCKED（RB-3）** | `git ls-files` 807 檔只有 `home_work_01/.env.example`；`git check-ignore -v home_work_01/.env` → `home_work_01/.gitignore:12`；CI `36232697465`（`9902026`）與 `36236093336`（HEAD `bc74f9c`）皆 success（含 credential scan） |
| INV-V2-3 瀏覽器只呼叫 `/api/`、零外部請求 | 成立（1,008 ＋ 整合情境，外部 0） | — |
| INV-V2-4 health／smoke／預報 endpoint 不變 | 成立 | preview deployment `6677133574` ↔ `9902026`（DA 以 `gh api deployments?sha=` 核對） |
| INV-V2-5 兩種語義分開、觀測不聚合（H-3） | 成立 | — |
| INV-V2-6 新鮮度單調；Stale 只以失敗 | 成立 | — |
| INV-V2-7 三條路徑獨立降級 | 成立（S1 情境） | — |
| INV-V2-8 V1 不變量與產物不變（H-2） | 成立（blob／tree 全部 SAME；唯一 diff 為 `api/index.py` docstring） | 老師兩句 SQL 對 `git show 9902026:home_work_01/data.db`（sha256 `9bbf05bc…f542b`，＝工作樹）：`SELECT DISTINCT regionName` → **6**（北部地區、中部地區、南部地區、東北部地區、東部地區、東南部地區）；`WHERE regionName = '中部地區'` → **7**（id 8–14，2026-09-24～09-30）；42 列、(regionName, dataDate) 重複 0、7 個日期；DDL 逐字五欄；表只有 `IngestionMetadata`、`TemperatureForecasts`；`IngestionMetadata` ＝ `(1, '2026-09-24T02:24:50+08:00', 'F-D0047-091')` |
| INV-V2-9 Scope class 分明 | 成立 | — |
| V1 INV-1～9（V2 下的適用形式） | 成立（含 INV-3 離線重新推導 42 列相同、INV-6 依 Δ-1 re-scope） | 同上 |

**結論：跨 Ticket invariants 在整合 subject 上成立；decision A-2 對 Spec Integration Audit 的義務（逐項核 INV-V2-2／5／8 與 V1 INV-4，並對提交的 `data.db` 重跑老師兩句 SQL）已由該 record §2、§7 履行，DA 另行執行得到相同結果。INV-V2-2 的 Vercel 平台面是唯一未驗證處，由第 3 節的 P-2 承接。**

### 2.4 整合行為

Spec Integration Audit §4：三條路徑同時失敗後各自恢復（S1）、下鑽＋雷達＋模式往返＋Stale＋Back to Taiwan（S2，1280 與 375）、組合態版面（S3）、縣多邊形指標可達性量測——Reviewer 自寫情境 **71/71**，六個既有瀏覽器檢查在最終 subject 重跑 37/37、97/97、72/72、113/113、47/47、V1 series PASS；未發現整合層級缺陷。

**結論：成立。**

### 2.5 累積 evidence 充分（可完成範圍）

- **自動化**：Reviewer 在 `9902026` 匯出樹、無網路、無 `.env` 下 **614 passed**；CI `36232697465`（headSha `9902026`，Python 3.12.14，614 passed，credential scan passed）——DA 以 `gh run list --commit` 核對 conclusion success；V1 259 個 test id 全部在 614 中。
- **部署（非金鑰部分）**：`smoke.py` 對受審 subject 的公開 preview PASS（#41 R1 與 SIA 各自獨立執行）；deployment ↔ commit 已證明；服務的靜態資產與 `9902026` blob 位元組相同；缺金鑰時觀測／雷達 503 `key_not_configured`、health 200——**這同時證實 Vercel 金鑰尚未填入**。
- **手動／瀏覽器 ENHANCED 項目**：AC-V2-01／02／08／10／12／13／14／15／18／19 由 Reviewer 以自己的情境與重跑在最終 subject 驗證，不只依賴 Executor 截圖。
- **文件**：AC-V2-21 十四項由 #41 R1 與 SIA 各自逐項閱讀 README `9902026` 判定；R-V2-DOC-3 的 `ACCEPTANCE-V2.md` 在 subject 內且如實標示 BLOCKED（未 overclaim，#41 R1 §3 核對）。
- **README 實跑（Bindings §5 gate 項）**：wl41 V-9 於乾淨 3.12.14 venv 逐步實跑（install、離線 rebuild ＝ committed `data.db`、614 tests、Streamlit 200、`python server.py` 觀測／雷達 200 於 A-3 一次性定向驗證、終端無金鑰）；#41 R1 與 SIA 各自重跑離線 rebuild 得到相同結果。
- **Spec-level AC coverage**：AC-V2-01～23 在可完成範圍 **全部 PASS**；AC-V2-03 preview 抽樣、AC-V2-17(c)、AC-V2-22 觀測部分 **BLOCKED（RB-3）**——這些不是 coverage failure，也不是 FAIL；其證據類別（Spec §3：「preview 驗證紀錄（Reviewer 重現）」）在金鑰填入前無法由任何 Agent 合法產生（治理 §1.5 第 3、4 項）。
- **AB 涵蓋**：只有一份 derived Spec；derivation §4、Spec §7 矩陣、SIA §3.2、`ACCEPTANCE-V2.md` §5 四者一致；13／13 各有至少一條 PASS 的 AC；無分配缺口、無歧義重疊。AB-V2-2／10／13 的部署部分待 P-1～P-3。

**結論：evidence 對最終 subject 直接成立（不需經 anchor 推論），在可完成範圍內充分；不足處只有 RB-3 閘門的四項，且其缺口是證據無法取得而非證據失敗。**

### 2.6 無未解且未經合法處置的 blocking finding；無影響完成的未決 design ambiguity

- 十份 Ticket audit 的全部 blocking findings（#35 F-1、#38 F-1、#39 F-1）都在同一 cycle 的 R2 判定為已解決；Spec Integration Audit 無 blocking finding。
- Run 中 route 到 DA 的四個 routing signals（#36 R-1 → DV-20；#37 R-1 → DV-21；#39 R-1 → DV-22；#40 R-1 → DV-23）都已以 decision record 裁決，均為治理 §5.3 第 2 類（不改變 accepted 語義）；後續 R2 與 SIA 都依其判定；沒有 Reviewer 對這些 determination 提出爭議。
- 沒有需要 Final Adjudicator 的 routing／review 爭議；沒有 fail-closed 至 acceptor 的路徑；沒有 stop report。
- DA 另檢視 SIA F-1 與 §9 交接項是否隱含未決 design ambiguity（第 5 節）：否。

**結論：成立。**

### 2.7 Review、verification 與結案版本可對應；審後變更已受相應驗證

- 各 Ticket 的結案 code anchor（`5f0dbc3`、`f63ebb1`、`7a3b469`、`286ee9d`、`f3bf245`、`fedffdd`、`49dac12`／`9902026`）都在 `9902026` 的祖先鏈上（SIA §5）；票後的整合變更（`df78e79..9902026`）由 #41 R1 審查，SIA 在最終 subject 重驗其產品面。
- **`9902026` → HEAD `bc74f9c` 的 delta 與 DA determination**：四個 `doc/governance/**` 檔（record-only，Bindings §7）＋ **`doc/ticket/tickets-v2.md`**。DA 讀 diff：只有 #41 那一列由「待執行（…BLOCKED…）」改為「已結案（audit `issue-41-c1-r1`；R1 CLOSURE 可完成範圍；P-1..P-4 … BLOCKED，不是 FAIL）」並填 commit 欄 `9902026`——票務索引的 bookkeeping，鏡射 GitHub Issue 與 audit record 的狀態，不含任何產品、測試、驗收或文件語義。依 V1 phase acceptance §5 F-1 的既定處置：`doc/ticket/` **不是** record-only path，此類變更須「由 Reviewer／DA 判定必要的後續驗證」——**DA 判定：不需任何後續驗證；phase acceptance subject 維持 `9902026`**。SIA 已在其檔頭作同樣讀取與排除。
- **對第 3 節 post-key 驗證的 subject 規則**：redeploy 的 preview 所對應的 commit 必須是 `9902026` 本身，或其後代且 `git diff --name-only 9902026 <commit>` 只含 `doc/governance/**` 與 `doc/ticket/tickets-v2.md` 的狀態列；任何其他路徑的變更即為 subject 變更，須先依治理 §3.8 由 Reviewer／DA 判定必要驗證，不得逕以本 phase acceptance 涵蓋。

**結論：成立。**

### 2.8 Traceability 與 boundary

- OC-V2 → SPEC-V2 → Tickets → evidence 的鏈完整（SIA §6；derivation §15.3）。#35～#41 issue body 皆引用 OC-V2 `69c5a04`、SPEC-V2 v2.2 與 derivation §15；DV-20～23 已反映在 issue body、索引與 derivation §14。
- **單元目錄外零變更**：DA 核對 `git diff --name-only 08e158e HEAD -- . ':!home_work_01'` ＝ 空（RB-5 未觸及；A-4 窄授權未使用，workflow blob ＝ V1）；`doc/requirement/` 零變更。
- 沒有超出 accepted boundary 的功能（SIA §6：無 O-A0002／O-A0003、history、`localStorage`、heatmap、`setInterval`、持久寫入、速率限制；OPTIONAL／Later 未做）；ENHANCED 標示明確、只在部署的 Dashboard（INV-V2-9）。
- 沒有 reserved action 被 Agent 執行：未合併（`origin/main` ＝ `08e158e`）、未繳交、未動 Vercel／環境變數、未付費、無破壞性 git；branch 目前**沒有** PR（SA-2 允許開 PR，屬 Orchestrator／acceptor 於 terminus 的動作，不是 gate）。

**結論：成立。不需要 boundary determination；不需要 contract change。**

### 2.9 Worklog 已反映實際結果與 follow-up

七份 worklog（`issue-35.md`～`issue-41.md`）與 run record 的 frontier 表逐票記載 subject、audit verdict、binding、routing 與 tracked items；`worklog/issue-41.md` Remaining work 1 與 `ACCEPTANCE-V2.md` §6.2、§7、§8 列出 RB-3 閘門項目、release-gate 材料狀態與交接項，且未把 BLOCKED 寫成完成。第 3、5 節把殘餘義務與未結項目及其 owner 正式列出，供 Orchestrator 完成報告引用。

---

## 3. RB-3 閘門項目的裁決：phase acceptance 現在授予（可完成範圍），P-1～P-4 為本 phase 的殘餘義務

### 3.1 裁決

**(a)：phase acceptance 現在授予可完成範圍；AC-V2-17(c)、AC-V2-22 觀測部分、AC-V2-03 preview 抽樣與 decision A-6 preview 紀錄（P-1～P-4）作為本 phase 明確定義的 post-key 驗證義務帶出，由獨立 Reviewer 在 acceptor 填入金鑰後重現，並以 DA addendum 結清；結清前，Outcome Contract closure 與 release gate 的對應項目維持未滿足。** 不採 (b)（等待金鑰填入與 P-1～P-3 重現後才作 phase acceptance）。

### 3.2 理由

1. **阻擋的性質是治理 §1.5 的真正 boundary，不是 evidence 失敗或 design 缺口。** 填入 Vercel 環境變數是 Bindings §2.6 RB-3 明列的 reserved action（§1.5 第 3 項），且其證據（部署平台在有金鑰時的行為）無法由任何 Agent 在現有授權內合法取得（§1.5 第 4 項）。SIA 與 #41 R1 皆以 preview 503 `key_not_configured` 證實金鑰尚未填入、缺金鑰時平台行為正確（AC-V2-17(d)、INV-V2-4）。四項的 PASS 條件、驗證方法與證據類別在 Spec、`ACCEPTANCE-V2.md` §6.2 與 SIA §8 已完整定義；所缺的只是 acceptor 的一個動作。
2. **治理 §3.8 與 §1.4 要求 phase acceptance 是自主派工而非 operator checkpoint，並允許 run 在剩餘工作皆受真正 boundary 阻擋且已記錄時結束。** 若採 (b)，phase acceptance 會變成等待 acceptor 動作的 checkpoint，且會把所有已在最終 subject 上獨立驗證成立的 invariants、整合行為與 evidence（第 2 節）都懸置在一個與其無關的平台設定之後——這與 §1.5「只停止受影響路徑」「無關且不會預判或影響該決定的工作 SHOULD 繼續」相違。
3. **授予可完成範圍不弱化任何 gate、不捏造 evidence、不隱性縮減 scope（§1.5 末段）**，因為本紀錄：(i) 不把任何 BLOCKED 項記為 PASS；(ii) 把四項逐字保留為 Spec 的 AC 義務與 AB-V2-2／10／13 的未驗證部分；(iii) 明示 Outcome Contract closure 與 Bindings §5／SPEC-V2 §6.4／A-6 的 release gate 在 P-1～P-4 結清前不滿足（第 6 節）；(iv) 要求證據類別依 Spec 原文「Reviewer 重現」，不接受 Executor 或 acceptor 自述結案。
4. **§5.1 assurance（H-1 高風險）**：INV-V2-2 的 Vercel 平台面是唯一未驗證處。程式路徑（請求時讀取、只放 `Authorization` 標頭、影像請求不帶金鑰、失敗文字為常數、DEBUG log 零洩漏）已在本機以哨兵金鑰與整合情境獨立驗證，部署的是同一份程式（服務資產與 blob 位元組相同）。殘餘風險是平台層（例如平台 log 的請求記錄），其驗證只能在金鑰填入後進行——因此 **DA 依 §5.1 決定：P-2 為 release 前的必要 assurance，不是可選項**；其執行方式限定為金鑰格式掃描、永不讀出 Vercel 值（第 3.3 節）。這與 A-3（高風險 blocking finding 不得由 FA 單獨 deferred）無涉：這裡沒有 blocking finding，也沒有 deferral——是尚未取得的證據被明確帶出。
5. **先例一致但有一處刻意差異**：V1 phase acceptance 以 DR-12／DR-18 把 production smoke、workflow dispatch 與 Vercel 後台項目列為「合併後的 release evidence，不是完成條件」。V2 的四項**不同**：Spec §6.4 Release 列明文把「acceptor 已填 Vercel 金鑰的 preview 驗證」放在**合併前**，A-6 把 preview 觀測驗證紀錄列為 release-gate 材料，AC-V2-22 更把 production 重跑（合併後）與 preview 觀測驗證（合併前）分開。因此本紀錄不把 P-1～P-4 降為 post-merge release evidence，而是作為合併前的 phase 殘餘義務（第 6 節）。

### 3.3 殘餘義務的精確內容（P-1～P-4）

以下逐項是 `ACCEPTANCE-V2.md` §6.2 與 SIA §8 已定義的計畫，DA 在此固定其 owner、順序、紀錄位置與判準；**不新增任何 AC 或 oracle**。

| 步驟 | 內容 | Owner／authority | 依據 |
| --- | --- | --- | --- |
| **0（前提，只有 acceptor 能做）** | 依 README「Vercel key setup (acceptor only, V2)」步驟 1–3：在 Vercel 專案填入 `CWA_API_KEY`（**Production 與 Preview 兩個環境**），不印出、不匯出、不提交；redeploy 本 branch 的最新 preview；向 Orchestrator（run record）告知已完成及 redeploy 後的 preview URL 或 GitHub deployment id。**Agents 不得填入、讀出、印出、匯出或以 `vercel env pull` 取得該值。** | **acceptor**（RB-3；OC-V2 A-2；Spec §9 前置 1；derivation §11 #4） | Bindings §2.6 b3 |
| **1（派工）** | 派一位獨立 Reviewer（`gov-primary-reviewer`，Bindings §3.5 機制：fresh context，或 SIA Reviewer `ad2f24768b95d2567` 以 R2 方式延續自己的 context 並重讀）重現 P-1～P-3、記錄 P-4；bounded pack 附 #41 R1 F-2 的兩項程序註記（preview 頁面的 `vercel.live` 注入屬平台注入、不得記為 AC-V2-16／INV-V2-3 違規；P-2 只以 `KEY_PATTERN`／`tools.credential_scan` 同一規則的金鑰格式掃描，永不讀出 Vercel 值）。**不得由 Executor 重現，也不得以 acceptor 的口頭或截圖敘述代替 Reviewer 紀錄。** 這是契約內的 re-verification（治理 §1.2：「契約內必要的 rework／re-verification 不是新工作接受 gate」），**不需新的 Outcome Contract、不需新 Ticket、不是新的 audit round 或 cycle**——它完成 cycle 1 SIA 在 RB-3 下未能取得的證據。 | **Orchestrator**（派工；同一 run identity 的 post-key checkpoint）；判定由 Reviewer | 治理 §1.4、§2.3、§4.7；Bindings §3.5 |
| **P-1** | AC-V2-17(c) 觀測、AC-V2-22 觀測部分：對 redeploy 的 preview（不需登入）`GET /api/observations/latest` → 200，`dataset` `O-A0001-001`、`validStationCount` ≥ 1、`stations[]`、`observationTime`、`fetchedTime`；瀏覽器開 `<preview>/` → Now mode 顯示 Latest Observation（標記、`Observation Time`、`Fetched Time`）；`smoke.py` 仍 PASS；deployment id ↔ commit 依第 2.7 節的 subject 規則證明。 | Reviewer | Spec AC-V2-17(c)、AC-V2-22；`ACCEPTANCE-V2.md` §6.2 P-1 |
| **P-2** | AC-V2-17(c) 雷達、INV-V2-2 平台面（H-1，必要）：`GET /api/radar/latest` → 200 `image/png`＋`X-Radar-Time`＋`X-Radar-Dataset: O-A0058-006`（只記標頭與位元組數）；所有記錄的回應本文與標頭以金鑰格式掃描 **0 命中**、無上游 URL、無 `Authorization`。Vercel runtime log 畫面：**只在 acceptor 主動提供時**由 Reviewer 以同一金鑰格式規則掃描並記錄；acceptor 未提供時，Reviewer 記「未提供；本機 DEBUG-log 零洩漏證據（SIA §2 INV-V2-2）為據」，該 log 面即成為 acceptor 於 release 時自行確認的項目（V1 #21 F-3 先例），**不阻擋 addendum**。Reviewer 不得進入 Vercel 後台（RB-3「第三方帳號操作」）。 | Reviewer（回應面）；acceptor（log 面，選擇性提供） | Spec AC-V2-17(c)；INV-V2-2；derivation §6 H-1；決定 A-6 |
| **P-3** | AC-V2-03 preview 抽樣：≥ 3 站，頁面顯示值（標記／詳情）＝ 同一頁 `/api/observations/latest` 本文中的同站值；任何哨兵顯示為「—」。 | Reviewer | Spec AC-V2-03 |
| **P-4** | 決定 A-6 preview 觀測驗證紀錄＋Vercel 時序（#35 R1 F-2、#40 R1 F-2、wl35 Remaining 1）：記錄 P-1～P-3 的時間、URL、deployment id 與結果；量首次（cold）請求時間；可行時兩個並行請求；終態須在頁面 20 s 內；**若平台時限低於 8 s 上游上限的假設（Vercel 預設 10 s）→ route Design Authority**（derivation §11 #1），由 DA 於 addendum 或另開 decision record 處理（可能調整 §5.3 儀器或裁剪策略而不改語義；若需改語義則 fail-closed 至 acceptor）。 | Reviewer（紀錄）；DA（平台時限議題） | 決定 A-6；derivation §11 #1 |
| **紀錄位置** | Reviewer 自寫 record：**`doc/governance/audit/spec-SPEC-V2-c1-r1-postkey.md`**（Bindings §7 audit 命名加 `-postkey` 後綴，DA 指定；它是 cycle 1 SIA instance 的證據補完，不是 R2、不是新 cycle）；必要欄位同治理 §4.6（Work Contract、受審 subject 與 deployment、角色與 binding、independence、逐項 PASS／FAIL、evidence）。Orchestrator 於 run record 記 binding 核對與 checkpoint。`worklog/issue-41.md` 由接手角色補一列指向該 record。**結果主要記在 record-only 路徑；`ACCEPTANCE-V2.md` §1／§5／§6.2／§7 的字面更新（BLOCKED → PASS 與 #41 R1 F-1 的數字更正）MAY 一併做，但那是 `doc/acceptance/` 的 subject 變更（文件性），須在同一 post-key record 內由 Reviewer 確認 delta 只含該文件的狀態與引用文字；不做亦可，留待 acceptor 指示的結案後 Lightweight 文件修正。** | Reviewer；Orchestrator | Bindings §3.5 第 4 點、§7；治理 §4.6；V1 phase acceptance §6 的 A-6 位置說明 |
| **結清** | DA 讀該 record，寫 **`doc/governance/decisions/phase-acceptance-SPEC-V2-addendum-<YYYYMMDD>-postkey.md`**：確認 P-1～P-3 PASS 與 P-4 紀錄後，宣告本 phase 的殘餘義務結清、AB-V2-2／10／13 部署部分已驗證、Bindings §5「DA phase acceptance 已完成」在**全範圍**成立；或處理 P-4 的平台時限議題；或在任一項 FAIL 時依下段處理。自主派工（治理 §1.4）。 | **Design Authority**（Orchestrator 派工） | 治理 §3.8 |

**若 P-1、P-2 或 P-3 任一 FAIL**：那是對整合 subject的新 integration-level finding（治理 §4.7「此時它是對整合 subject 的新 finding」），由 Reviewer 在 post-key record 內以 severity／blocking 記錄；本 phase acceptance 對受影響 AC 的效力即告懸置；修正屬契約內 targeted correction（不需新授權），修正若改變 subject（任何非 record-only 路徑），依治理 §3.8 需相應驗證，後續 round／cycle 的機制依 §4.4–§4.5 由 Orchestrator（必要時 Final Adjudicator）決定；DA 於 addendum 重述受影響範圍。**若失敗原因涉及設計語義（例如平台限制迫使改變 8 s／20 s 界值或裁剪策略）**，route DA；若須改變 accepted 語義，contract change → acceptor（§5.3）。

### 3.4 本裁決對各 gate 的效果（明示，避免冒充）

| Gate／狀態 | 本紀錄之後 | P-1～P-4 結清（addendum）之後 |
| --- | --- | --- |
| Bindings §5「Formal：全部 Ticket 結案、SIA closure、DA phase acceptance 已完成」 | 前兩項完成；第三項**完成於可完成範圍** | 第三項全範圍完成 |
| Bindings §5「README 實跑」「無追蹤中的機密」 | 完成（第 6 節） | 不變 |
| SPEC-V2 §6.4 Release 列「acceptor 已填 Vercel 金鑰的 preview 驗證」 | **未具備** | 具備 |
| 決定 A-6「preview 觀測驗證紀錄」 | **未具備** | 具備 |
| Outcome Contract AB-V2-2／10／13 的部署部分 | **未驗證**（BLOCKED，不是 FAIL） | 已驗證（或依 FAIL 處理） |
| 合併（RB-1）、繳交（RB-2） | acceptor 的決定；DA 不建議在 addendum 前合併（宣告的 gate 尚未齊備）。若 acceptor 仍決定先合併（RB-1 為其保留決定），P-1～P-4 改對合併後的 production／preview 執行，義務不消失，addendum 記錄順序差異 | acceptor 的決定 |

---

## 4. 高風險類別（decision A-1／A-2；derivation §6）

| 類別 | Ticket audits（A-1） | Spec Integration Audit（A-2） | DA |
| --- | --- | --- | --- |
| H-1 憑證與機密 | #35、#37、#40、#41 各有核對段（#35 R2 重述），全 PASS；#36、#38、#39 亦以掃描／靜態面核對 | INV-V2-2／V1 INV-5：全部追蹤 blob 與 V2 全 patch 金鑰格式掃描 0；哨兵金鑰整合情境 0 洩漏；preview 只回固定句 | `git ls-files` 無 `.env`；`.env` 被忽略；CI 掃描通過。**Vercel 平台面 → P-2（必要）** |
| H-2 老師指定介面 | #35、#36、#38、#39、#41 各有核對段，全 PASS | INV-V2-8／V1 INV-4：blob／tree SAME；老師 SQL 6／7；預報 `/api/` 100 組相同；標題與概念詞逐字 | 老師 SQL 6／7；DDL 逐字；兩張表；42 列 0 重複（第 2.3 節） |
| H-3 資料語義與標示 | #35、#36、#37、#38、#40、#41 各有核對段，全 PASS | INV-V2-5、V1 INV-3／INV-7：語義分開、無聚合、代表站不當縣值、授權標示、INV-3 重新推導相同 | — |

未結的高風險相關項目只有 P-2（H-1 平台面，第 3 節）與 O-3（應用內觀測授權全名，SHOULD，第 5 節）。沒有任何 blocking finding 的 deferral（A-3 不適用）。

---

## 5. 對 Spec Integration Audit F-1、#38～#40 地圖可用性交接與其他 tracked items 的處置

### 5.1 SIA F-1（Low，non-blocking）——375 px 雙失敗組合態（觀測 Stale＋雷達 Stale＋選縣，雷達由使用者開啟）下地圖上方狀態區累積到 606 px，首屏看不到地圖

- **DA 確認 Reviewer 的契約判定**：R-V2-RSP-4／OC S-10 對地圖只給「主要內容區」與「模式切換不捲動即可見」兩個判準——後者有客觀 oracle（載入時成立）；前者在結構上成立（地圖是頁面最大的內容元素；非失敗態與單一失敗態在 375×812 首屏仍有地圖；V1 在 375×667 本就只部分顯示地圖）。RSP-5(b)(g)／RSP-6 約束的是資訊面與 overlay 的遮蔽（組合態 52.5 % 未遮、控制可達）。OC S-1／OBS-4(c)「兩個時間永遠可見」：兩時間始終顯示於 Now 面板、未被應用程式隱藏或遮蔽——與 #39 R1 F-1（面板自身捲動把時間移出視野，已修正）性質不同。**無 AC 或 invariant 違反；不是 design ambiguity，不需 §3.6-A decision record。**
- **是否由 DA 提出修正**：否。壓縮狀態區（例如 < 1024 px 時把 Stale／radar stale 說明收成一行、雷達按鈕與 County 同列）屬 HOW，且 SPEC-V2 已結案於本 subject；任何 UI 變更都是 Bindings §4 第 3 列的「已結案工作之後的單點修正」——需要 acceptor 的直接指示作為其 Outcome Contract，並依 A-4 判斷是否觸及 H-1／H-2／H-3「觸及的工作」（純版面變更通常不觸及，仍由該 work item 依 policy 判定）。若 acceptor 想要「375 px 首屏必有地圖」的**保證**，那是新的 requirement——contract change（§5.3 第 1 類）——不是本 Spec 的缺陷。
- **Disposition**：non-blocking；不阻擋 phase acceptance；owner **acceptor**（是否指示後續 work item）；DA 不建議也不反對，只說明治理路徑。

### 5.2 #38～#40 地圖可用性交接（`ACCEPTANCE-V2.md` §8；SIA §9 整合層判定）

| 交接項 | DA 處置 |
| --- | --- |
| O-1：初始縮放層級部分縣多邊形無可命中像素（1280 z7 嘉義市、臺北市；375 z6 新北市、臺北市、金門縣；被代表標記覆蓋） | 同意 SIA：R-V2-DD-4 未綁定縮放層級；DD-9(a) 的非地圖鍵盤路徑存在；DV-22 §4.2(5) 只要求可經 hover／點選到達（放大一級即可）；代表標記本身可選；County 選單 22 縣。**契約成立，non-blocking。** 若要改善（例如多邊形提升到標記之上的命中層），屬 HOW，路徑同 5.1（acceptor 指示的新 work item）。 |
| #39 R1 F-3（< 1024 px expanded 資訊面中選站後標記在面板下） | RSP-5(b) 只約束 normal／peek；Collapse 後 `reveal` 把標記帶到 peek 上方。**契約成立，non-blocking；維持 #39 disposition。** |
| #39 R1 O-2（下限 zoom 6 拖曳中暫態中心離開 E，放手回彈） | AC-V2-13 以「拖曳到底後」讀取；R-V2-MAP-1 明列彈性回彈屬 HOW。**契約成立。** |
| #39 R2 O-5／O-6／O-7 | 一般版面性質、無 AC 受影響、整合情境未見惡化。**non-blocking，無動作。** |
| #40 R1 F-1（375 px 雷達控制使首屏地圖減少） | 已由 SIA 在組合態重量並併入 F-1（5.1）。 |
| #39 R1 F-2（延後步驟被丟棄） | 已於 #39 修正，SIA 整合情境無回歸。**已閉合。** |

### 5.3 其他 tracked items

| 項目 | 處置 |
| --- | --- |
| SIA O-3／#41 R1 §4(a)：應用內觀測授權標示只寫「CWA station observations (O-A0001-001, hourly)」，未含資料集全名（雷達列有全名） | DV-16 的 SHOULD 維持，不升為 MUST（B-14：C-4 是文件 constraint，應用內為 DA 的法遵預設偏好）；偏離理由已記於 wl41 決定 5 與 `ACCEPTANCE-V2.md` §8；README（MUST）兩個資料集全名齊全。**non-blocking。** 若 acceptor 要補齊，是一行 `index.html` 文字的結案後 Lightweight work item（觸及 H-3「相關文件措辭」→ 依 A-4 需 independent audit）。 |
| #41 R1 F-1：`ACCEPTANCE-V2.md`／wl41 的 network-log 數字（136／506／1,008、「six logs」）與已提交五個 log 的 135／505／1,006 不符；SIA 重跑得 136／506／1,008（執行間正常浮動） | Editorial；零外部的結論不受影響。Owner：記錄 P-1～P-4 結果時若更新 `ACCEPTANCE-V2.md` 順修（第 3.3 節「紀錄位置」的 subject 變更規則適用）；不更新亦可。 |
| #41 R1 F-2：post-key 計畫的兩項程序註記 | 已納入第 3.3 節步驟 1 的派工內容要求。Owner：Orchestrator。 |
| #41 R1 O-1／SIA O-4：`CONTEXT.md`「Web App … never call CWA」詞條 | 描述的是 MVM 預報讀取行為，與 Δ-1／INV-V2-1 一致；R-V2-DOC-4 只要求 BRIEF-V2 §9 delta 逐字併入。**不是缺陷。** 若 acceptor 想加註「V2 伺服器端觀測／雷達路徑除外」，屬結案後 Lightweight 文件修正（不觸及 H 類別）。 |
| #35 R1 F-2／#40 R1 F-2（上游取得期間持鎖，並行停滯請求排隊；前端 20 s 上限保證終態）；#40 R1 O-3（影像請求跟隨重新導向） | 平台行為由 P-4 記錄；修正方式屬 HOW，只能在後續合法授權的變更中處理；重新導向不在契約範圍。**non-blocking。** |
| #35 R1 F-3、#36 R1 F-1、#37 R1 F-1（Low；不可達或 CWA 不會觸發） | 維持各票 disposition；不需動作。 |
| #41 R1 O-3：A-6「最後一次 CI 結果引用記在 `doc/acceptance/`」 | 套用 V1 phase acceptance §6 的 A-6 位置說明：final subject 的 CI run id 必然在該 commit 之後產生；A-6 的「另附」義務以 `ACCEPTANCE-V2.md` §7（材料清單與指向）＋ wl41 V-2 ＋ SIA AC-V2-20 列 ＋ 本紀錄第 6 節（HEAD CI run 引用）視為已滿足。不改變 gate 實質。 |

---

## 6. Bindings §5／decision A-6／SPEC-V2 §6.4 release gate 材料的狀態（供 acceptor 參考；不是本紀錄的授權）

| Gate 項目 | 狀態 | 依據 |
| --- | --- | --- |
| Formal：全部 Ticket 依 Orchestrator Contract §7 結案 | 完成 | 第 2.1 節 |
| Formal：每份 Spec 的 Spec Integration Audit 已 closure | 完成（可完成範圍） | `spec-SPEC-V2-c1-r1.md` |
| Formal：Design Authority phase acceptance 已完成 | **完成於可完成範圍（本紀錄）；全範圍待 addendum** | 第 1、3 節 |
| README 的安裝與執行步驟已實際跑過，結果與證據記在 worklog | 完成 | `worklog/issue-41.md` V-9（乾淨 3.12.14 venv 逐步實跑）；#41 R1 與 SIA 各自重跑離線 rebuild 相同 |
| 沒有追蹤中的機密：`git ls-files` 不含 `.env`，diff 內沒有金鑰字串 | 完成 | SIA INV-V2-2（全 blob 與 V2 全 patch 0 命中）；CI credential scan passed；DA `git ls-files`／`check-ignore` 核對 |
| A-6 另附：A-2 的 SQL 執行結果 | 完成 | SIA §7 H-2（6 與 7）；#41 R1 §5；DA 本紀錄第 2.3 節重跑相同 |
| A-6 另附：A-5 的最後一次 CI 結果引用 | 完成 | `9902026` run **`36232697465`** success；HEAD `bc74f9c` run **`36236093336`** success（DA `gh run list --commit` 核對） |
| A-6 另附：preview 觀測驗證紀錄（AC-V2-17(c)、22） | **未具備——BLOCKED（RB-3）** | 第 3 節 P-1～P-4 |
| SPEC-V2 §6.4 Release 列：acceptor 已填 Vercel 金鑰的 preview 驗證（合併前） | **未具備——BLOCKED（RB-3）** | 第 3 節 |
| SPEC-V2 §6.4 Release 列：合併後對 production 重跑 smoke 與觀測抽樣 | 合併後的 release evidence（不是完成條件） | AC-V2-22；DR-12 先例 |

**結論：宣告的 release gate 材料尚未齊備——差 acceptor 的 RB-3 動作與其後的 Reviewer 重現。是否合併（RB-1）由 acceptor 決定。**

---

## 7. 是否改變 accepted 語義；boundary determination

**否。** 本紀錄不 derive 新的 contract、不修改 Spec、不新增或移除任何 AC／INV／gate；第 3 節只固定既有計畫（Spec §3 證據類別、`ACCEPTANCE-V2.md` §6.2、SIA §8、決定 A-6、derivation §11 #1／#4）的 owner、順序與紀錄位置；第 5 節的每一項都只引用既有 accepted decisions（DV-16、DV-22、A-4、Bindings §4）已確立的地位。P-2 的「必要」是 DA 依治理 §5.1 對高風險 assurance 的決定，不新增產品需求。Phase acceptance 是治理 §3.8 授予 DA 的判定，不是接受或授權行為（§1.2、§5.2）。

**Boundary determination（治理 §1.2）**：不需要——沒有任何 Reviewer 提出 boundary 符合性 finding，SIA §6 明記無 boundary 疑義；沒有 fail-closed 的路徑。第 2.7 節對 `tickets-v2.md` 的判定是 subject-identity 的驗證需求判斷，不是 boundary 問題。

---

## 8. 受影響 work items

| 對象 | 影響 |
| --- | --- |
| #35–#41 | 無重開；結案狀態不變。#41 的 Remaining work 1（P-1～P-4）由第 3 節承接為 phase 殘餘義務。 |
| Orchestrator（run record、完成報告、post-key checkpoint） | 記錄本 phase acceptance 於「Spec-level audit & phase acceptance」段；完成報告 MUST：(1) 以 `9902026` 為 SIA 與 phase acceptance 的 subject；(2) 分別陳述 work item completion、phase acceptance（可完成範圍）、run completion、Outcome Contract closure（未完成）、release authorization（未授權）；(3) 逐項列出第 3.3 節步驟 0 為 acceptor 的唯一解除動作、P-1～P-4 為 Reviewer 重現義務、addendum 為 DA 結清；(4) 不得把任何 BLOCKED 項寫成已完成；(5) acceptor 告知金鑰已填入後，以同一 run identity 派工步驟 1（bounded pack 附 #41 R1 F-2 兩項註記），核對 binding，原樣 commit Reviewer record，再派 DA 寫 addendum。 |
| acceptor | 第 3.3 節步驟 0（RB-3）；第 6 節 gate 的合併決定（RB-1）；繳交（RB-2）；第 5 節各選擇性 follow-up 的授權與否。 |
| SPEC-V2 v2.2、derivation record、DV-20～23、Bindings | 不需修改。 |
| `ACCEPTANCE-V2.md`、`tickets-v2.md` | 本紀錄不改；第 3.3 節「紀錄位置」定義 post-key 更新的規則。 |

---

## 9. 需要其他 authority 的事項

| 事項 | Authority | 理由 | 是否阻擋 phase acceptance |
| --- | --- | --- | --- |
| 在 Vercel 專案填入 `CWA_API_KEY`（Production＋Preview）並 redeploy；告知 Orchestrator | acceptor | RB-3（Bindings §2.6 b3）；OC-V2 A-2；Spec §9 前置 1 | 否（阻擋的是 P-1～P-4 與 OC closure） |
| 派獨立 Reviewer 重現 P-1～P-3、記錄 P-4；之後派 DA 寫 addendum | Orchestrator | 治理 §1.4、§2.3；Bindings §3.5 | 否 |
| P-4 若平台時限低於 8 s 假設 | Design Authority | derivation §11 #1 | 否 |
| 合併 branch 進 `main`（release） | acceptor | RB-1；gate 材料見第 6 節（尚未齊備） | 否 |
| 合併後 production smoke 與觀測抽樣 | acceptor（或依其直接指示的 Agent） | AC-V2-22；SPEC-V2 §6.4 | 否 |
| 授權 5.1／5.2／5.3 列的任何選擇性 UI／文件 follow-up | acceptor | 治理 §1.2 tracked item；Bindings §4 第 3 列；A-4 | 否 |
| 繳交作業 | acceptor | RB-2 | 否 |
| Final Adjudicator | — | 沒有 routing 或 review 爭議 | — |

沒有任何事項需要 acceptor 才能完成本 phase acceptance（可完成範圍）；本紀錄不向 acceptor 請求任何動作，只列出 OC-V2 原本就分配給 acceptor 的 RB-3 前提、release 與 reserved 動作。

---

## 10. Phase acceptance 的效力與後續

- 本 phase 的 accepted subject 為 `9902026`。之後任何對 `home_work_01/`（含 `doc/acceptance/`、`doc/ticket/`）的變更，都不在本 phase acceptance 的 coverage 內：依 Bindings §4 屬「已結案工作之後的單點修正」，以 acceptor 的直接指示為 Outcome Contract 開新的 Lightweight work item；觸及 H-1／H-2／H-3「觸及的工作」者依 A-4 需 independent audit。**例外**：第 3.3 節允許的 `ACCEPTANCE-V2.md` 狀態／引用更新與 `tickets-v2.md` 狀態列，依該節規則處理。
- 只 commit `doc/governance/**`（本紀錄、run record 更新、post-key audit record、addendum）不改變 subject identity。
- **殘餘義務的結清**以 `phase-acceptance-SPEC-V2-addendum-<YYYYMMDD>-postkey.md` 記錄；在其寫入前，本紀錄第 1 節表格中標「未完成／未具備」的各列維持原狀。
- 若 acceptor 決定不填入金鑰（例如放棄部署 Now mode 的即時觀測），那是改變 OC-V2 AB-V2-13 與 §1 intent 的 contract change（§5.3 第 1 類），須由 acceptor 明示；本紀錄不預設此路徑。

---

## 11. Evidence（DA 自行執行，全部唯讀；未印出任何金鑰）

- **讀取**：Bindings b3 全文；治理 v2.0 §1.2、§1.4、§1.5、§2.1–§2.4、§3.3–§3.8、§4.1–§4.7、§5.1–§5.4；OC-V2 全文；SPEC-V2 §0、§3（AC-V2-03／17／22 列）、§6、§7、§8、§9、§10；derivation-SPEC-V2 全文（§1–§15）；decision A-1～A-7；DV-20～DV-23 的引用段；V1 `phase-acceptance-SPEC.md` 全文；`spec-SPEC-V2-c1-r1.md` 全文；`issue-41-c1-r1.md` 全文；十份 Ticket audit records 的標頭欄與 verdict 行、#38～#40 的 findings 標題與 disposition 行、`issue-35-c1-r2.md` 的 H-1／H-3 列；`ACCEPTANCE-V2.md` 全文；`tickets-v2.md` 全文；run record 全文；`worklog/issue-41.md` §Verification、A-3 紀錄、High-risk 材料、Audit status、Remaining work。
- **Git**：`git rev-parse HEAD` ＝ `bc74f9c00a4da3dd55ca12b54d6594ab5094a60e`（branch `home_work_01-v2-implementation`）；`origin/main` ＝ `08e158e565785b56df63520a3f1307723f76b623` ＝ V2 BASE；`git log --oneline 9902026..HEAD` ＝ `7588583`、`38e20fa`、`5905157`、`bc74f9c`；`git diff --name-only 9902026 HEAD` ＝ 4 個 `doc/governance/**` ＋ `doc/ticket/tickets-v2.md`（diff 內容：只有 #41 索引列）；`git diff --name-only 08e158e HEAD -- . ':!home_work_01'` ＝ 空；`git diff --name-only 08e158e HEAD -- home_work_01/doc/requirement` ＝ 空；`git status --porcelain` 只有審查前即存在、與本紀錄無關的 `grep.exe.stackdump`；`git ls-files` 807 檔，`.env` 相關只有 `home_work_01/.env.example`；`git check-ignore -v home_work_01/.env` → `home_work_01/.gitignore:12:.env`。
- **GitHub**：`gh issue list`：#35～#41 全部 CLOSED（時間見第 2.1 節）；`gh pr list --head home_work_01-v2-implementation` → 無 PR；`gh run list --commit 9902026…` → `36232697465` push completed success；`--commit bc74f9c…` → `36236093336` push completed success；`gh api repos/…/deployments?sha=9902026…` → `6677133574` Preview、sha `9902026`、`vercel[bot]`。
- **Bindings §3.4 核對指令**對 session `05b8408b-260a-46d3-a4fe-ec07e3ec365a/subagents/`（20 個 agent）：8 個 `gov-primary-reviewer`（7 個 Ticket audits ＋ `ad2f24768b95d2567` SIA）皆 `claude-opus-5-5`／`xhigh`；7 個 `gov-executor` 皆 `claude-opus-5-5`／`high`；5 個 `gov-design-authority` 皆 `claude-fable-5-1`／`xhigh`。agent id 與 run record 及各 audit record 的自述逐一相符；SIA Reviewer 與七個 Ticket Reviewer 皆不同 identity。
- **`data.db`**（`git show 9902026:home_work_01/data.db` 寫入暫存檔後以 `mode=ro` 開啟；與工作樹 sha256 相同 `9bbf05bc6cc803444c8760432d6b484699c597f751fa16cb58bfbb5a0dbf542b`）：表 `IngestionMetadata`、`TemperatureForecasts`；DDL `id INTEGER PRIMARY KEY, regionName TEXT, dataDate TEXT, mint REAL, maxt REAL`；SQL 1 → 6（北部地區、中部地區、南部地區、東北部地區、東部地區、東南部地區）；SQL 2 → 7（id 8–14，2026-09-24～09-30）；42 列；重複 0；7 個日期；`IngestionMetadata` ＝ `(1, '2026-09-24T02:24:50+08:00', 'F-D0047-091')`。
- **Grep**：十份 Ticket audit 的 verdict 行（第 2.1 節）；九份含「高風險類別核對／High-risk／decision A-1」段，`issue-35-c1-r2.md` 以表列重述 H-1／H-3。
- **未執行**：未重跑 pytest 或瀏覽器檢查（以 SIA closure record 為據，治理 §3.8）；未讀 `home_work_01/.env`；未使用 API key；未呼叫 CWA；未對 preview 發出請求；未接觸 Vercel。
