# Decision record — Ingestion 取得時間的格式驗證（#18 R2 N-1 的後續，GitHub Issue #29）（`home_work_01/`）

- **紀錄類型**：Design Authority decision record（治理 §3.6-A：在不改變任何 accepted 語義的前提下裁決 lane、boundary determination 與驗證的接受準則；治理 §5.3 第 2 類；Bindings §4「模糊或有爭議的分類由 Design Authority 判定，並留 decision record」；治理 §5.1「DA 決定高風險分類及 assurance 要求」）
- **編號**：**DR-22**（延續 DR-21 [`decision-20260924-map-rework-rs1-rs2.md`](decision-20260924-map-rework-rs1-rs2.md)）；子裁決 DR-22.1～DR-22.6
- **日期**：2026-09-24
- **來源**：Issue #18 cycle 1 R2 audit record [`../audit/issue-18-c1-r2.md`](../audit/issue-18-c1-r2.md) §5 **N-1**（Medium，non-blocking；disposition「由 DA／Orchestrator 決定；若以單點修正處理，依 A-4 必做 independent audit」）；Orchestrator 依治理 §2.4 派工 DA；GitHub Issue **#29**（`yotsubamomo/aiot-classwork#29`，2026-09-24 建立，label `ready-for-agent`）。binding 核對由派工者依 Bindings §3.4 記入 run record。
- **本 work item 的 Outcome Contract**：acceptor 2026-09-24 的直接指示（Bindings §2.3 末項、§4 第 3 列；第 0 節逐字）。它**不取代**、也**不修改** `home_work_01` 既有的 Outcome Contract（ACCEPTED 2026-09-23）與 Spec v1.1；後兩者與 DR-17 繼續作為產品層級的 accepted 語義約束本 work item。
- **相關契約與紀錄**：Outcome Contract §2.5、AB-8、AB-10、AB-11；Spec v1.1 R-ING-3、R-ING-5、R-DB-5、R-SEC-2、R-DOC-1、R-DOC-2、R-TC-1、AC-09、AC-11、AC-12、AC-24、AC-25、INV-3、INV-5、§4.2、§5.1；**DR-17** [`decision-20260924-ingestion-timestamp-semantics.md`](decision-20260924-ingestion-timestamp-semantics.md) §4.1～§4.6、§5、§7 I-1～I-4；[`decision-20260923-high-risk-categories.md`](decision-20260923-high-risk-categories.md) H-1、H-3、A-1、A-4、A-5；DR-20 [`decision-20260924-taiwan-map-rework.md`](decision-20260924-taiwan-map-rework.md) §3.1、§3.5、§5（post-closure Lightweight work item 的先例）；[`phase-acceptance-SPEC.md`](phase-acceptance-SPEC.md) §10；[`phase-acceptance-SPEC-addendum-20260924-map-rework.md`](phase-acceptance-SPEC-addendum-20260924-map-rework.md) §6。
- **執行角色**：`gov-design-authority`（Bindings §3.1：`design_authority` → `claude-fable-5-1`／`xhigh`）。本紀錄不自證 binding。
- **效力**：Issue #29 的 Executor、Reviewer（R1／R2／Alternate）、Orchestrator 以本紀錄為 #29 的 lane、boundary、驗證接受準則、assurance 要求與 Spec Integration Audit 處置的依據，不得重開。Spec v1.1、Outcome Contract、DR-17 文字**不變**。本紀錄不修改任何實作、測試、資料、README 或 `doc/acceptance/`；DA 未 commit、未 merge。

---

## 0. Acceptor 授權文（逐字）

本 work item 的接受與授權由下列兩段 acceptor 原文共同構成；效力來自 acceptor 原文，不來自本轉錄。

**(a) 指示文件 `orchestrator-message-map-rework.md` §5「順帶（可刪）」第一點（acceptor 語氣；該文件為 acceptor 審閱並核定的指示文件，DR-20 §0 首段）：**

```text
- 我同時授權 **#18 R2 N-1**（`--acquired-at` 格式驗證）作為**另一個** Lightweight work item：獨立票、A-4 independent audit、不與地圖票混在同一 commit。
```

**(b) Acceptor 2026-09-24 對該文件的核定文（DR-20 §0 逐字，節錄相關句）：**

```text
I reviewed `orchestrator-message-map-rework.md`.
The overall direction is correct.
...
Do not modify the existing Spec or Outcome Contract.
Proceed with this as a new enhancement work item under the governance lane already described in the document.
Create/confirm the corresponding GitHub Issue and derive the work item/ticket boundary as needed.
...
Do not merge to main.
```

寫入者：Design Authority。(a) 由 DA 於 acceptor 支援 session 的 scratchpad 副本（`.../25a2390c-ae1f-483e-8b7a-10f844793ab9/scratchpad/orchestrator-message-map-rework.md` 第 107 行）逐字轉錄；該文件不在 repo 內。(b) 已由 DR-20 §0 逐字保存於 repo。既有紀錄的一致佐證：run record 終點報告第 6 項把 N-1 列為「awaiting acceptor authorization」（指示前）；DR-20 E-2／§5 與 `tickets.md`（`cc29c7f`）在指示後記為「acceptor 授權的獨立 Lightweight work item」；#28 phase 增補 §6 同。

**前置條件 C-1（Bindings §2.3 末項、治理 §3.1 第 4、7 項）**：#29 worklog 的 Contract reference MUST 逐字載入上述 (a) 與 (b)（或引用本節），並引用 Issue #29 body 作為 acceptor 授權範圍的轉錄。若 Orchestrator 無法確認 (a) 為 acceptor 審閱並核定之文件的內容，本紀錄第 3 節的裁決仍成立，但 #29 不得開始執行——授權缺口依治理 §1.2 route 至 acceptor（DA 不代行）。

---

## 1. 問題

Orchestrator 派工要求 DA 對 Issue #29 一次裁決：(1) lane（Lightweight／Formal）；(2) boundary determination——本 work item 只動 ingestion 取得時間在兩條輸入路徑（CLI `--acquired-at`、sidecar `acquiredAt`）的驗證，加上 online 值通過同一驗證、README 措辭與測試，不得動 `derive.py` 規則、DDL、`persist.py`、已提交的 `data.db`／原始 JSON／sidecar、`/api`／dashboard／地圖、DR-17 語義；(3) **驗證的精確接受準則**（依 DR-17 導出）：是否必須是含明確 UTC offset 的完整 ISO 8601 datetime；offset 是否必須恰為 `+08:00`、其他 offset（含 `Z`）拒絕還是接受並正規化；精度是否恰為秒；分隔符與大小寫；fail-closed 行為；合格與不合格例；(4) 高風險分類（H-3 → A-4）與 H-1 訊息核對；(5) 依治理 §4.7，Lightweight 是否需補 Spec Integration Audit 增補。

---

## 2. 事實（DA 自行核對；Orchestrator、Executor、Reviewer 的敘述都當作待驗證主張）

| # | 事實 | 證據 |
| --- | --- | --- |
| E-1 | HEAD `cc29c7f`＝branch `home_work_01-hw10-implementation`；`git diff --name-only 5136bd2 cc29c7f` 只有 `doc/acceptance/ACCEPTANCE.md`、`doc/ticket/tickets.md` 與四個 `doc/governance/**` 檔；工作樹只有 `doc/ticket/tickets.md` 未提交的 #29 索引列（Orchestrator bookkeeping）。#18–#25 CLOSED；#28 audit closure（`issue-28-c1-alt.md`）、phase 增補已記；release 候選 subject 為 `5136bd2`。 | DA `git rev-parse`、`git diff`、`git status`、`git log`；phase 增補 §5 |
| E-2 | 在 `5136bd2` 與 `cc29c7f`，下列 blob 完全相同：`data.db`（`6875869…`）、`data/raw/F-D0047-091.json`（`209eb76…`）、`data/raw/F-D0047-091.meta.json`（`9edfd11…`）、`ingestion/persist.py`、`derive.py`、`config.py`、`fetch.py`。提交的 `IngestionMetadata` ＝ `(1, '2026-09-24T02:24:50+08:00', 'F-D0047-091')`；sidecar `acquiredAt` ＝ `2026-09-24T02:24:50+08:00`（同一字串）；`sqlite_master` 只有 `TemperatureForecasts`、`IngestionMetadata` 兩表。 | DA `git rev-parse <commit>:<path>`；對 `data.db` 唯讀查詢；讀 sidecar |
| E-3 | **現行程式**：`ingestion/provenance.py:63-86` `read_acquisition_time` 在 sidecar 不存在／不可讀／`acquiredAt` 為空或缺時丟 `ProvenanceError`，否則 `return str(acquired_at)`——**不驗證格式，且非字串值會被 `str()` 轉成字串**；`ingestion/pipeline.py:153-154` `run_offline` 只在 `acquired_at is None` 時讀 sidecar，CLI 傳入的 `''` 不是 `None`，會逐字傳給 `persist_snapshot`；`pipeline.py:35-41` `ingestion_timestamp()` 回 `datetime.now(TAIPEI_TZ).replace(microsecond=0).isoformat()`，即恰為 `YYYY-MM-DDTHH:MM:SS+08:00`；`pipeline.py:128-136` online 路徑在 `fetch_raw` 後取一次時間戳，先 `save_raw_json`、再 `write_provenance`、再 derive、再 persist；`main` 只攔 `FetchError`、`DeriveError`、`ProvenanceError` → `Ingestion failed: …` 到 stderr、回 1。`persist.py:22-41` 以字串參數 upsert，不驗證。 | DA 讀檔 |
| E-4 | **N-1 的五個不良輸入**（R2 實測全部 exit 0 並逐字寫入）：`--acquired-at ''`、`--acquired-at yesterday`、`--acquired-at 2026-09-24`、`--acquired-at 2026-09-24T02:24:50Z`、sidecar `acquiredAt` 為 `not-a-time`。R2 另指出兩條路徑不一致：sidecar 空值 fail-closed，CLI 空值卻寫入（shell 變數未設時 `--acquired-at "$ACQ"`）。R2 的建議 disposition：「在寫入前驗證值符合 ISO 8601、含 `+08:00`、精確到秒，不合格時與 T-3 相同方式 fail-closed」。 | `issue-18-c1-r2.md` §5 N-1 |
| E-5 | **契約文字**：R-DB-5「Ingestion 時間（ISO 8601，含 `+08:00`）…MUST 記錄在 `data.db` 內 `TemperatureForecasts` 以外的地方，供兩個呈現層顯示『最後更新時間』」。DR-17 §4.1：取得時間＝「本機時鐘時間，ISO 8601、`+08:00`、**至少到秒**」；§4.2(2)「同一個值」寫入 DB 與出處紀錄；§4.3(1) offline 值「來源只能是：該 JSON 的出處紀錄，或呼叫端明確提供的取得時間」；§4.3(2)「Offline 路徑 MUST NOT 讀取時鐘」；§4.3(3) 找不到取得時間時「MUST 在寫入前以明確訊息失敗…不得以『現在時間』或任何推測值代替」；§4.4 出處紀錄「MUST NOT 含金鑰、`Authorization` 或任何請求標頭」；§4.5 顯示值「MUST 恰等於資料庫內的 `ingestedAt`」（AC-24）；§7 I-4「提交的 `data.db` 的 `ingestedAt` MUST 等於提交的原始 JSON 的出處紀錄中的取得時間」。**DR-17 §7 I-4 的字面是字串相等的一致性要求，沒有「精確到秒」四字**；「`+08:00`、精確到秒」是 R2 對提交集合的觀察（§3.2 I-4 列）與 Issue #29 的轉述，其事實基礎是 E-2 的提交值與 E-3 的 online 產生器。 | Spec `SPEC.md:155`；DR-17 §4、§7；R2 §3.2 |
| E-6 | **Python 解析器的寬鬆度**（DA 於 Python 3.11.2 實測；3.12 同）：`datetime.fromisoformat` 接受 `2026-09-24`（回 naive 午夜）、`…50Z`、空白分隔、`.5` 小數秒、`+0800`、naive `…50`；`strptime(…, "%Y-%m-%dT%H:%M:%S%z")` 的 `%z` 亦接受 `Z` 與 `+0800`。因此「能被 Python 解析」不等於「符合 R-DB-5／DR-17 的格式」；接受準則必須以**文法比對**定義，不能只以解析成功定義。 | DA scratchpad 探測 |
| E-7 | **既有測試**（HEAD 全套 164 passed，見 phase 增補 §5；Issue #29 所寫「既有 60 測試」是 #18 結案當時的計數）：`tests/test_pipeline.py` 經 CLI 使用的取得時間字面值全部是 `YYYY-MM-DDTHH:MM:SS+08:00`（`SEED_TIME` `2026-09-24T12:00:00+08:00`、`2026-10-01T09:00:00+08:00`、`2026-09-24T08:15:30+08:00`、`2026-09-20T06:00:00+08:00`、`2026-09-22T18:30:00+08:00`、`2026-09-24T08:00:00+08:00`）；T-3 斷言 stderr 含 `provenance`；`test_persist.py`、`test_weather_query.py`、`test_app.py`、`test_dashboard.py` 的 `2026-01-02T03:04:05+08:00` 等值直接寫入 DB 或呼叫 `persist_snapshot`，不經本 work item 觸及的路徑。`test_secrets.py:16` 已把 sidecar 列為掃描對象（T-4）。 | DA grep／讀檔 |
| E-8 | **README**（`README.md:104-143`）：已說明取得時間語義、sidecar 位置與內容「`acquiredAt`（ISO 8601 `+08:00`）」、offline 讀 sidecar 或 `--acquired-at`、缺少時 fail-closed；CLI 選項列為「`--acquired-at ISO8601`」。`build_parser` 的 help 寫「(ISO 8601 +08:00)」。兩處都沒有寫出精確文法，也沒有說不合格值會被拒絕。 | DA 讀檔 |
| E-9 | **Bindings 與先例**：Bindings §4 第 3 列「已結案工作之後的單點修正：Lightweight，作為新的 work item；需要 acceptor 的直接指示作為其 Outcome Contract」；Bindings §5／decision A-4：結案後的 Lightweight 修正若觸及 H-1～H-3 的「觸及的工作」MUST 執行 independent audit；H-3 的「觸及的工作」含「驗證邏輯…或相關文件措辭」，DR-17 §5.4 明文把取得時間標示歸入 H-3；H-1 的「觸及的工作」含「任何讀取 `.env`…撰寫文件的變更」。治理 §4.7 末段：Lightweight 無 Spec、不適用 Spec Integration Audit；assurance policy MAY 要求等效的 outcome-level audit。DR-20 §3.5 已為 post-closure Lightweight work item 建立「A-4 R1 涵蓋整合重驗 ＋ Orchestrator phase 增補」的兩段式 pattern，並實際執行（phase 增補紀錄存在）。`ACCEPTANCE.md:172` §6 有 N-1 的殘餘列，owner 為「new post-#25 Lightweight follow-up」。 | Bindings §4、§5；high-risk decision §2、§3；治理 §4.7；DR-20 §3.5；phase 增補；`ACCEPTANCE.md` |
| E-10 | **Issue #29 body** 的「要做／不做／High-risk／DoD」與派工內容一致：單一驗證函式對兩條路徑強制格式、online 值通過同一驗證、精確準則由 DA 裁決、測試涵蓋五種不合格＋合格值、既有測試不弱化、提交的 `data.db`／sidecar 值與可重現性不變、錯誤訊息不含金鑰、README 補格式要求、獨立 commit、不合併不提交；不做 `derive.py`、DDL、`persist.py`、已提交資料、Dashboard／`/api/`／地圖。 | `gh issue view 29` |

---

## 3. 裁決

### 3.1 DR-22.1 — Lane：**Lightweight**（新的 work item；A-4 independent audit 必做）

**裁決**：Issue #29 是 Bindings §4 第 3 列的 post-closure 單點修正，lane 為 **Lightweight**，以第 0 節的 acceptor 直接指示（其範圍由 Issue #29 body 轉錄）作為本 work item 的 Outcome Contract。依 decision A-4，因觸及 H-3 與 H-1 的「觸及的工作」（3.4 節），**independent audit 必做**：fresh `gov-primary-reviewer` R1，其後依治理 §4.4 同一套 R2／一次 Alternate／Final Adjudication；R1 record 依 A-1 明記 H-3／H-1 核對段。worklog 的 Audit status MUST 寫「required（A-4）」，不得寫「依 policy 未要求」。

**依據（治理 §3.3、§3.6）**：

1. **§3.3 eligibility 成立。** intent 與 scope 由第 0 節與 Issue #29「要做／不做」給定；authority 由第 0 節給定；acceptance 的唯一語義缺口——「什麼值合格」——正是 §3.3 所說必須 route DA 的語義缺口，由本紀錄 3.3 節裁決，不留給 Executor 假設。裁決後 Executor 不需對 intent、scope、acceptance、authority 作任何假設。
2. **不是 §3.6-B。** 被驗證的行為（`ingestedAt` 的格式與 fail-closed 姿態）有 accepted baseline 可錨定（R-DB-5、DR-17 §4.1、§4.3(3)）；沒有其他工作依賴新的驗證器（#18–#25、#28 全部結案，無進行中的工作）；所需裁決不改變 accepted 語義（第 4 節）；沒有 parent 把必要設計留待下游——驗證機制是 Spec §4.2「Ingestion 的…CLI 介面」之下的 HOW。
3. **不是 §3.6-C。** 一張票、一個 Executor、一個 Reviewer 流程、同一 branch、一個 commit 集合；沒有多 execution units 或 dependency 管理需求。
4. **§3.3 末段的排除不適用。** 結果不改變 accepted 語義；不改變其他工作所依賴的設計基線——`persist_snapshot` 介面、`IngestionMetadata` 欄位、DDL、sidecar schema、`/api/` 形狀、兩個呈現層的顯示義務全部不動。CLI／sidecar 對**合格**值的行為不變；改變的只是對**不合格**值的行為（從逐字寫入改為拒絕），而逐字寫入本來就違反 R-DB-5。
5. **不得拆成多個 Lightweight 以規避 Formal（§3.3）**：本 work item 的整體結果就是一個驗證器與其測試、文件；N-2～N-5 等其他 tracked items 不在其內（3.2 節 X-9），不存在被切碎的更大整體。

**若下列任一情況出現，本裁決失效、路徑停止並 route DA 重判**：需要改動 `persist.py`、`derive.py`、`config.py`（DDL）、`fetch.py`、已提交的 `data.db`／原始 JSON／sidecar、`/api/`、`app.py`、`weather_query.py`；需要改變 DR-17 §4 的任何語義（例如 offline 讀時鐘、正規化、推測值）；需要新增 AC／INV 或改變既有 AC 的 PASS／FAIL 語義；需要第二個 execution unit。

**紀錄命名（Bindings §7；DA 具體化）**：worklog `doc/governance/worklog/20260924-acquired-at-validation.md`（Lightweight 命名；`tickets.md` 已引用）；audit `doc/governance/audit/issue-29-c<cycle>-<r1|r2|alt>.md`（本 work item 有 GitHub Issue，沿用 Ticket 命名以維持可追溯，同 #28 先例）；`doc/ticket/tickets.md` 的 #29 列已存在（scope class「POST-BASELINE ENHANCEMENT（Lightweight work item）」；High-risk H-3、H-1；Blocked by #18）。派工機制依 Bindings §3.3／§3.5：Executor 為 `gov-executor` subagent（或主 session 在 binding 符合 `executor` mapping 時直接執行——擇一並記錄 binding）；Reviewer 一律以 Agent tool 派 fresh `gov-primary-reviewer`，bounded pack 只放路徑與識別（本紀錄、Issue #29、DR-17、`issue-18-c1-r2.md`、worklog、subject SHA、parent SHA），不放 Executor 結論。

### 3.2 DR-22.2 — Boundary determination（治理 §1.2、§3.6-A）

**總判定：Issue #29 的全部工作項目都在既有 Outcome Contract（AB-8 ingestion、AB-10「ingestion 對失敗有明確錯誤」、AB-11 README、§2.5 constraints）、Spec v1.1（R-DB-5、R-ING-5、R-SEC-2、R-DOC-1、AC-09／AC-11 的 fail-closed 姿態、INV-3、INV-5）與 DR-17 的 boundary 內，並在第 0 節 acceptor 指示的範圍內；它是 R-DB-5 既有格式要求與 DR-17 §4.3(3) 既有 fail-closed 要求在兩條輸入路徑上的執行，屬 Spec §4.2「Ingestion 的 CLI 介面」之下的 HOW。不新增 requirement、AC、invariant 或 gate；不改變任何 accepted 語義；不改 Spec、不改 Outcome Contract、不改 DR-17。**

**在 boundary 內（允許觸及的路徑；R1 diff-scope 證明的 allowlist）**：

| # | 路徑 | 允許的變更 |
| --- | --- | --- |
| B-1 | `home_work_01/ingestion/pipeline.py` | `run_offline` 對 CLI 值的驗證與精確的來源判定（3.3 AT-8、AT-9）；`run_online` 對 `ingestion_timestamp()` 值的驗證（AT-8、AT-10）；`--acquired-at` 的 help／metavar 寫出精確文法；`main` 的例外攔截維持「無 traceback、`Ingestion failed:` 前綴、exit 1」。 |
| B-2 | `home_work_01/ingestion/provenance.py` | sidecar `acquiredAt` 的型別與格式驗證（AT-1～AT-7）；驗證函式 MAY 放在此檔。`write_provenance` 的輸出 schema（四個欄位、`note` 文字）**不變**；它 MAY 在寫出前對值呼叫同一驗證。 |
| B-3 | `home_work_01/ingestion/<新模組>.py`（至多一個，例如 `acquisition_time.py`）與 `ingestion/__init__.py`（只限 export） | 驗證函式若獨立成模組。屬 HOW。 |
| B-4 | `home_work_01/tests/**`（不含 `tests/fixtures/**`） | 新增測試；既有測試只能加強，不得弱化或刪除斷言；fixture 不動。 |
| B-5 | `home_work_01/README.md` | ingestion 段：`--acquired-at` 與 sidecar `acquiredAt` 的精確格式、拒絕的類型、fail-closed 訊息（3.6 節）。其他段落不動。 |
| B-6 | `home_work_01/doc/acceptance/ACCEPTANCE.md` | 只更新 §6「#18 R2 N-1」列的狀態與證據引用；AC 列的判定文字不動（`data.db` 未變，AC-24／AC-05 證據仍是原紀錄）。 |
| B-7 | `home_work_01/doc/ticket/tickets.md` | #29 索引列的狀態與 commit。 |
| B-8 | `home_work_01/doc/governance/**` | record-only（Bindings §7）。 |

**明確在 boundary 之外、本 work item 不得執行的事項**（出現時 Executor 停止該路徑並 route DA；DA 無法確立在 boundary 內時 fail-closed 至 acceptor）：

| # | 事項 | 為何在外 | 所需 authority |
| --- | --- | --- | --- |
| X-1 | 改動 `ingestion/derive.py`（R-DER 規則）、`config.py`（DDL、常數）、`persist.py`、`fetch.py`、`checks.py`、`__main__.py` | Issue #29「不做」；H-2／H-3／H-1 的核心面；DR-17 §7「不變的部分」。 | DA（重判 lane／boundary） |
| X-2 | 改動已提交的 `data.db`、`data/raw/F-D0047-091.json`、`data/raw/F-D0047-091.meta.json`（含重新產生） | DR-17 §7 I-4 的提交集合已驗證一致（E-2）；本 work item 不需要任何資料變更；重新產生會使 R2／SIA 對資料的證據失效。**三個 blob 在 #29 subject 與 parent 之間 MUST 相同。** | acceptor（新指示） |
| X-3 | 改動 sidecar schema（新增／改名欄位）或 `write_provenance` 的輸出形狀 | 不在指示內；會使日後 online run 產生的 sidecar 與提交的形狀不同。DR-17 §4.4「MAY 另記其他資訊」是 DR-17 允許的空間，但不是本 work item 的授權。 | DA（另一 decision record） |
| X-4 | 對不合格值做**正規化／轉換**（例如把 `Z` 換算成 `+08:00`、截掉小數秒、trim 空白）後接受 | 3.3 節裁決為拒絕；轉換是對出處值的計算，沒有 accepted 來源（DR-17 §4.2(2)、§4.3(1)「同一個值」）。 | DA（會 route acceptor，因為它改變本 work item 的 accepted 行為） |
| X-5 | 合理性／範圍／「不得在未來」檢查 | 需要讀時鐘（DR-17 §4.3(2) 禁止 offline 讀時鐘）或任意界限（無 accepted 來源，屬新 requirement）。 | acceptor（新 requirement） |
| X-6 | 改動 `/api/`、`server.py`、`api/`、`app.py`、`weather_query.py`、`static/**`、`vercel.json`、`requirements.txt`、`.python-version` | Issue #29「不做」；INV-1／INV-2／INV-9；與 #28 的 subject 分離。 | DA（重判） |
| X-7 | 修改 Spec v1.1、Outcome Contract、derivation record、DR-17、Bindings | 核定文「Do not modify the existing Spec or Outcome Contract」；治理 §5.3。 | acceptor |
| X-8 | 修改 `.github/workflows/**` 或 `home_work_01/` 以外的檔案 | RB-5；OC §8.2 的 workflow 授權只涵蓋維護本單元 workflow，本票不需要。 | acceptor |
| X-9 | 順帶處理 #18 R2 **N-2**（T-1 遞增時鐘）、**N-3**（測試註解／docstring）、**N-4**（raw JSON 與 sidecar 皆缺時的訊息）、**N-5**（README「online 失敗後不要提交 `data/raw/`」）或 `ACCEPTANCE.md` §6 的其他 tracked items | 治理 §1.2：non-blocking finding 的後續事項在 acceptor 接受並授權前只是 tracked items；第 0 節只授權 N-1。worklog 不得把它們記為已處理。Executor 為 3.3 節 V-4 所寫的 online 測試若在技術上也能偵測 N-2，屬 HOW，但 N-2 的 disposition 仍由 Orchestrator 追蹤、不在 #29 結案。 | acceptor（新指示） |
| X-10 | 合併進 `main`、繳交、任何 Vercel／repo variable 操作 | RB-1、RB-2、RB-3。 | acceptor |

**Boundary 疑義的處理**：Reviewer 若對上述任一項提出 boundary 符合性 finding，依治理 §1.2 先由 DA 評估；DA determination 後仍有爭議者視為 DA 無法確立，受影響路徑 fail-closed 至 acceptor。

### 3.3 DR-22.3 — 驗證的接受準則（核心語義裁決，依 DR-17 導出）

#### 3.3.1 規則（Executor 實作、Reviewer 核對的唯一準則）

一個取得時間值 **合格**，若且唯若 AT-1～AT-7 全部成立；AT-8～AT-12 規定適用範圍、優先順序、失敗行為與訊息。

| # | 規則 | 依據 |
| --- | --- | --- |
| **AT-1 型別** | 值 MUST 是字串。CLI 值恆為字串；sidecar `acquiredAt` MUST 是 JSON string——number、boolean、null、object、array 一律不合格（現行 `str(acquired_at)` 的轉型 MUST 移除）。 | DR-17 §4.1（值是 ISO 8601 字串）；E-3 |
| **AT-2 文法** | 整個字串 MUST 恰為 `YYYY-MM-DDTHH:MM:SS+08:00`：正規表示式 `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+08:00$`（ASCII 數字；大寫 `T`；字面 `+08:00`；長度恰 25；無小數秒；字串內任何位置無空白）。 | R-DB-5「ISO 8601，含 `+08:00`」；DR-17 §4.1；online 產生器的輸出形（E-3）；E-6（解析成功不等於合格） |
| **AT-3 曆法有效** | 日期時間部分 MUST 是真實存在的時刻：月 01–12、日在該年該月的範圍內（含閏年）、時 00–23、分 00–59、秒 00–59。等價檢查：`datetime.strptime(value, "%Y-%m-%dT%H:%M:%S%z")` 成功——**但 strptime 單獨不足**（E-6），MUST 與 AT-2 同時成立。 | R-DB-5（有效的 ISO 8601 時刻） |
| **AT-4 Offset** | offset MUST 恰為 `+08:00`。`Z`、`+00:00`、`+0800`、`+08`、`+09:00`、`-08:00` 等一律**不合格**；**不正規化、不換算**成 `+08:00`；合格值以**原字串**寫入（AT-12）。 | 理由見 3.3.2 |
| **AT-5 精度** | 恰為秒。含小數秒（`.0`、`.123456`）**不合格**；不截斷。 | 理由見 3.3.2 |
| **AT-6 分隔符、大小寫、空白** | 日期與時間之間只接受大寫 `T`；空白分隔、小寫 `t`、小寫 `z` 不合格。不 trim：前後或中間的空白、tab、換行使值不合格。 | 單一正規形；理由見 3.3.2 |
| **AT-7 不做合理性檢查** | 不檢查是否在未來、是否早於某日期、是否與 raw JSON 的 StartTime 相關；offline 路徑 MUST NOT 讀時鐘。 | DR-17 §4.3(2)；X-5 |
| **AT-8 適用範圍** | 同一驗證 MUST 套用於三個來源：(a) CLI `--acquired-at`——只要選項出現（含 `''`）即以 CLI 為來源驗證；(b) sidecar `acquiredAt`——在 sidecar 被讀取時；(c) online `ingestion_timestamp()` 的回傳值——每次 online run 於產生後立即驗證。 | Issue #29；DR-17 §4.2、§4.3 |
| **AT-9 優先順序** | CLI 值存在 → 只驗證 CLI 值；**不合格時不退回 sidecar**（fail-closed，訊息告知「省略 `--acquired-at` 可改用 sidecar」）。CLI 值不存在 → 讀 sidecar 並驗證。CLI 值存在且合格 → sidecar 不被讀取，其內容無關。sidecar 不存在、不可讀、缺 `acquiredAt` 鍵的現行行為與訊息不變（N-4 不在本票）。 | DR-17 §4.3(1)(3)；README「overriding the sidecar」；E-4 的不一致 |
| **AT-10 Fail-closed 行為** | 不合格時：結束碼 **1**（經既有 `main` 的攔截，`Ingestion failed: …` 前綴，stderr，無 traceback）；**不開啟、不寫入資料庫**（既有快照與 `IngestionMetadata` 逐位元不變，`snapshot_signature` 相同；INV-3 不受影響）。offline：驗證 MUST 在讀取 raw JSON 與 derive **之前**完成。online：驗證 MUST 在 `ingestion_timestamp()` 回傳後、`save_raw_json` 與 `write_provenance` **之前**完成——不合格時 raw JSON、sidecar、DB 三者都不寫。 | DR-17 §4.3(3)；AC-09／AC-11 姿態；Spec §5.1 |
| **AT-11 訊息內容** | 訊息 MUST 含：(a) 不合格的值本身，以引號或 `repr` 界定，使空字串與空白可見（值超過 80 字元 MAY 截斷並加省略標記——HOW）；(b) 來源：CLI 寫 `--acquired-at`；sidecar 寫 sidecar 檔名或路徑（`<raw>.meta.json`）與鍵名 `acquiredAt`，非字串時另寫 JSON 型別；online 寫 `ingestion_timestamp()`（內部錯誤）；(c) 要求的格式 `YYYY-MM-DDTHH:MM:SS+08:00` 與一個例子。訊息 MUST NOT 含金鑰、`.env` 內容、任何請求標頭、環境變數、raw JSON 內容（H-1、R-SEC-2、DR-17 §4.4）。 | Issue #29；H-1；R-SEC-2 |
| **AT-12 原樣寫入** | 合格值 MUST 原字串寫入 `IngestionMetadata.ingestedAt`（`stored == input`）；online 路徑寫入 sidecar 與 DB 的仍是同一字串（DR-17 §4.2(2)）。 | DR-17 §4.2(2)、§4.3(1)、§7 I-4 |

argparse 對 `--acquired-at` 缺參數的 usage error（exit 2）不在本裁決內，維持現狀。

#### 3.3.2 理由（依 DR-17、R-DB-5；不採用 Executor／Reviewer 的結論）

1. **完整 datetime＋明確 offset 是既有要求，不是新要求。** R-DB-5 要求「ISO 8601，含 `+08:00`」；DR-17 §4.1 把值定義為「本機時鐘時間，ISO 8601、`+08:00`、至少到秒」。空字串、`yesterday`、只有日期、naive 時間都不是這個值——它們不含 `+08:00`、或根本不是時刻。拒絕它們只是執行 R-DB-5。
2. **Offset 恰為 `+08:00`、不正規化——四個理由。** (i) R-DB-5 的字面要求是**儲存的字串**含 `+08:00`；AC-24 要求兩層顯示的值恰等於 DB 值，所以 DB 內的字串就是使用者看到的字串——存 `Z` 直接違反 R-DB-5。(ii) DR-17 把這個值定義為**本機（Taipei）時鐘的表示**，並在 §4.2(2)、§4.3(1) 反覆要求 pipeline 傳遞「同一個值」：pipeline 是出處紀錄的**載體**，不是計算者。把 `…50Z` 換算成 `…10:24:50+08:00` 是對出處值的一次計算，沒有任何 accepted 來源要求或允許它，且會引入自己的正確性面（其他 offset 的換算、`Z` 在不同 Python 版本的解析）。(iii) §7 I-4 與 R2 的驗證都是**字串相等**（`data.db.ingestedAt == sidecar.acquiredAt`）；正規化會讓「操作者提供的值 ≠ 寫入的值」，破壞這條可用字串比對核驗的一致性鏈，而這正是 N-1 指出的模糊。(iv) H-3 誠實標示：維護者傳入 `Z` 時，pipeline 無法知道那是「真的 UTC」還是「把本機時間誤標成 `Z`」；拒絕是唯一**永遠不會記錄錯誤時刻**的選擇，代價只是操作者以正確字串重跑一次，而訊息（AT-11）已告訴他正確形式。DR-17 §4.3(3) 的姿態——「不得以推測值代替」——延伸到這裡就是：不確定的輸入不猜。
3. **精度恰為秒。** DR-17 §4.1「至少到秒」是下限，秒滿足它；把接受文法固定在恰為秒，是因為 (a) online 產生器就是這個形（`replace(microsecond=0)`），(b) 提交集合（E-2）是這個形，(c) AC-24 把字串原樣顯示在兩層，小數秒會讓兩條路徑對同一資料顯示不同形（違反 DR-17 §5.5「兩條路徑對同一資料應得到同一標示」），(d) 截斷與正規化同罪（第 2 點 (ii)）。這是 §3.6-A「既有來源容許多種解讀但選擇僅影響本 work item」的選擇：DR-17 允許 ≥ 秒，本紀錄為本 work item 選定恰為秒的**單一正規形**；沒有其他工作依賴更細精度。
4. **分隔符、大小寫、空白。** 單一正規形（＝online 產生器的 `isoformat()` 輸出）讓接受準則可以用一條正規表示式完整測試；任何寬鬆都會重新製造「同一時刻多種寫法」，而 R2 的驗證與 I-4 的一致性都建立在字串相等上。不 trim 的理由同第 2 點 (ii)：pipeline 不修改出處值。
5. **不做合理性檢查（AT-7）。** 「不得在未來」需要讀時鐘，DR-17 §4.3(2) 明文禁止 offline 讀時鐘；任何固定界限都沒有 accepted 來源，會是新 requirement（治理 §5.3 第 1 類）。N-1 也沒有要求它。
6. **CLI 不合格時不退回 sidecar（AT-9）。** 明確傳入的錯誤值是操作者錯誤，靜默改用 sidecar 會掩蓋它（R2 的 `--acquired-at "$ACQ"` 情境正是變數未設而不自知）；DR-17 §4.3(3) 與 AC-09／AC-11 的一貫姿態是「明確訊息、非零、不寫入」。訊息告知可省略選項改用 sidecar，操作者一次即可修正。
7. **Online 值也過同一驗證（AT-8(c)）。** 這是對 DR-17 §4.2 的自我一致性斷言：若日後有人改動 `ingestion_timestamp()`（例如拿掉 `replace(microsecond=0)` 或換時區），run 會在寫任何檔案前失敗，而不是把不合格的形寫進 sidecar 與 DB。

#### 3.3.3 合格例（全部 MUST 被接受並原字串寫入）

| # | 值 | 備註 |
| --- | --- | --- |
| OK-1 | `2026-09-24T02:24:50+08:00` | 提交的 `data.db`／sidecar 值（E-2） |
| OK-2 | `2026-09-24T01:39:31+08:00` | DR-17 E-4 的原始取得時間 |
| OK-3 | `2026-09-24T12:00:00+08:00` | 既有測試 `SEED_TIME`（E-7） |
| OK-4 | `2026-01-01T00:00:00+08:00` | 日界下限 |
| OK-5 | `2026-12-31T23:59:59+08:00` | 日界上限 |
| OK-6 | `2028-02-29T12:00:00+08:00` | 閏日 |

#### 3.3.4 不合格例（全部 MUST 依 AT-10／AT-11 fail-closed）

N-1 列出的五個（原字串）：

| # | 來源 | 值 | 違反 |
| --- | --- | --- | --- |
| NG-1 | CLI | `''`（空字串） | AT-2；AT-9（CLI 出現即為 CLI 來源，不退回 sidecar） |
| NG-2 | CLI | `yesterday` | AT-2 |
| NG-3 | CLI | `2026-09-24` | AT-2（只有日期；`fromisoformat` 會接受，故必須文法比對，E-6） |
| NG-4 | CLI | `2026-09-24T02:24:50Z` | AT-4（UTC 標記，不是 `+08:00`；不換算） |
| NG-5 | sidecar | `not-a-time` | AT-2（訊息指名 sidecar 檔與 `acquiredAt`） |

邊界補充（Reviewer 核對文法邊緣，Executor 測試 SHOULD 涵蓋）：

| # | 值 | 違反 |
| --- | --- | --- |
| NG-6 | `2026-09-24T02:24:50`（naive） | AT-2／AT-4 |
| NG-7 | `2026-09-24T02:24:50+0800` | AT-2／AT-4 |
| NG-8 | `2026-09-24T02:24:50+09:00`、`2026-09-24T02:24:50+00:00` | AT-4 |
| NG-9 | `2026-09-24T02:24:50.000+08:00` | AT-5 |
| NG-10 | `2026-09-24 02:24:50+08:00`（空白分隔） | AT-6 |
| NG-11 | `2026-09-24t02:24:50+08:00` | AT-6 |
| NG-12 | ` 2026-09-24T02:24:50+08:00`、`2026-09-24T02:24:50+08:00\n`、`   `（純空白） | AT-6／AT-2 |
| NG-13 | `2026-02-30T02:24:50+08:00`、`2026-09-24T24:00:00+08:00`、`2026-09-24T02:24:60+08:00` | AT-3 |
| NG-14 | sidecar `"acquiredAt": 1758651890`、`null`、`true`、`{}` | AT-1（訊息指名 JSON 型別） |

#### 3.3.5 必要的自動化證據（形式屬 HOW；Reviewer 於 R1 核對存在與強度）

| # | 證據 | 斷言 |
| --- | --- | --- |
| V-1 | CLI 路徑對 NG-1～NG-4（＋SHOULD NG-6～NG-13）逐一經 `pipeline.main --from-json … --acquired-at <值>`，DB 先 seed | exit 1；`snapshot_signature` 不變；stderr 含該值（以可見形式）與 `--acquired-at`；stdout＋stderr 不含 raw JSON 內容 |
| V-2 | sidecar 路徑對 NG-5、NG-14（＋SHOULD NG-6～NG-13 寫入 sidecar）經 `pipeline.main --from-json …`（無 `--acquired-at`） | exit 1；快照不變；stderr 含 sidecar 檔名與該值（或 JSON 型別） |
| V-3 | OK-1～OK-6 分別經 CLI 與 sidecar | exit 0；`IngestionMetadata.ingestedAt` 與輸入字串相等 |
| V-4 | online：(a) `ingestion_timestamp()` 的實際輸出（真實時鐘一次、patch 的時鐘含微秒與日界一次）通過驗證函式；(b) 把 `ingestion_timestamp` patch 成不合格值（例如 NG-4）跑 `run_online`／`main`（mock `fetch_raw`，`.env` 放哨兵金鑰） | (a) 合格；(b) exit 1、raw JSON 與 sidecar 都**不存在**、DB 不變、stdout＋stderr 不含哨兵金鑰（H-1） |
| V-5 | 優先順序：不合格 CLI ＋ 合格 sidecar；合格 CLI ＋ 不合格 sidecar | 前者 exit 1、快照不變；後者 exit 0、寫入 CLI 值 |
| V-6 | 提交集合：讀取 repo 內 `data/raw/F-D0047-091.meta.json` 的 `acquiredAt` 通過驗證；乾淨匯出下 `python -m ingestion --from-json data/raw/F-D0047-091.json` | 通過；exit 0 且 `ingestedAt == 2026-09-24T02:24:50+08:00`（AC-12、DR-17 §4.4；Reviewer 於乾淨匯出重跑） |
| V-7 | 既有 164 測試（parent commit）全部保留、斷言未弱化；T-1～T-4 仍綠 | Reviewer 以 parent 與 subject 的測試名與斷言 diff 核對 |
| V-8 | 驗證函式的單元測試：對 3.3.3、3.3.4 全部值逐一斷言 | 表格與程式一致 |

### 3.4 DR-22.4 — 高風險分類與 assurance 要求

- **H-3（資料語義與標示）— 觸及。** 取得時間＝「最後更新時間」的語義（DR-17 §4.1、§5.4 明文歸入 H-3）；本 work item 改動的是該值的**驗證邏輯**（H-3「觸及的工作」）與 README 的相關措辭。**→ A-4：independent audit 必做**（fresh `gov-primary-reviewer` R1）。R1 record 依 A-1 MUST 有一節明記 H-3 的核對：3.3.1 規則逐條、3.3.3／3.3.4 全部例值的實測（Reviewer 自跑 CLI，不只看測試）、V-6 乾淨匯出重現、README 措辭未把值寫成 CWA 發布時間或頁面時間（DR-17 §4.5）。
- **H-1（憑證與機密）— 觸及。** 改動 `pipeline.py`（online 路徑所在模組，讀 `.env` 的呼叫端）、新增錯誤訊息、修改 README（H-1「觸及的工作」含「撰寫文件的變更」）。A-1 段 MUST 核對：AT-11 的訊息只由值、來源、格式組成；V-4(b) 的哨兵金鑰不出現在輸出；A-5 全套（`git ls-files` 無 `.env`；tracked 與 diff 無金鑰格式字串；sidecar 仍被 `test_secrets.py` 掃描）對 #29 subject 重跑；worklog、本紀錄、audit record 不含金鑰。
- **H-2（老師指定介面）— 不觸及，但 MUST 留證據。** R1 以 blob id 證明 `data.db`、`ingestion/config.py`（DDL）、`ingestion/persist.py` 在 parent 與 subject 之間相同（E-2 的方法），並記為「diff 未觸及」；不得記為新的 PASS 主張。
- **A-3**：若 R1／R2 對 H-3 產生 blocking finding 而 Final Adjudicator 考慮 deferral，MUST 另有 DA 確認（治理 §4.5）。
- **A-7／Model diversity**：Executor `claude-opus-4-8`、Primary Reviewer `claude-opus-5-5` 為預設；替代造成 diversity 消失時照記 `diversity_lost`。

### 3.5 DR-22.5 — Spec Integration Audit：不適用；改採 DR-20 §3.5 的兩段式 outcome-level assurance

**裁決**：**不另開 Spec Integration Audit instance**。治理 §4.7 末段明文「Lightweight 無 Spec，不適用本節」；DA 不得把 #29 的 audit record 事後標為 Spec Integration Audit。依 §4.7「assurance policy MAY 對特定類別要求等效的 outcome-level audit」、§4.1「有權裁決決定」與 §5.1「DA 決定 assurance 要求」，本 work item 採與 DR-20 §3.5 相同的兩段式，兩段都必要：

**(A) #29 的 A-4 R1 MUST 涵蓋下列整合重驗，並以獨立一節記載**（這是 §4.4「R1 完整審查 accepted work scope、適用 invariants、變更風險與 acceptance evidence」在本 work item 的具體化，不是新增 audit instance、round 或角色）：

1. **Diff-scope 證明**：`git diff --name-only <parent>..<subject>`（parent ＝ #29 subject 所基於的 commit，≥ `cc29c7f`；排除 `doc/governance/**`）MUST 只落在 3.2 節 B-1～B-7 的 allowlist；X-1、X-2、X-3、X-6、X-8 所列路徑任一出現即為 boundary finding → route DA。另以 blob id 證明 X-2 的三個資料檔相同。
2. **Invariants**：INV-3（每一個不合格情境都不部分寫入——V-1、V-2、V-4(b)、V-5）、INV-5（A-5 重跑；新訊息與 README 無金鑰）；INV-4／H-2 記為「diff 未觸及、blob 相同」（3.4 節）。
3. **Spec AC**：AC-09、AC-11 的 CLI 反例仍綠（既有測試未弱化）；AC-12 的離線重跑由 Reviewer 在乾淨匯出實跑（V-6）；AC-24 記為「`data.db` blob 未變，`spec-SPEC-c1-r1.md` 的結論沿用」；AC-25 記為「raw JSON blob 未變」；R-DOC-1／R-DOC-2 對 README ingestion 段的措辭核對（3.6 節）；AC-20／AC-21 對 subject 的 CI 綠。
4. **DR-17 合規不回歸**：T-1～T-4 仍綠；offline 無時鐘讀取（Reviewer MAY 重跑 R2 的 M3／M5 mutant 手法）；sidecar schema 與 `write_provenance` 輸出不變。
5. **Work item DoD**（Issue #29 §Acceptance）：3.3 節全部規則與例值；README；`ACCEPTANCE.md` §6 N-1 列；`tickets.md`；worklog；獨立 commit（不含 `static/**`）。

**(B) #29 audit closure 後，Orchestrator 自主派工產出 phase-acceptance 增補紀錄** `doc/governance/decisions/phase-acceptance-SPEC-addendum-20260924-acquired-at-validation.md`：引用 `phase-acceptance-SPEC.md`（`720c0a0`）、`phase-acceptance-SPEC-addendum-20260924-map-rework.md`（`5136bd2`）、已 closure 的 `spec-SPEC-c1-r1.md`（對未受 diff 觸及的部分仍有效）與已 closure 的 #29 audit record（對受觸及部分），以 (A)-1 的 diff-scope 證明把它們接起來，宣告新的 release 候選 subject 的 phase 狀態。它不是新的 phase acceptance、不是 release authorization；性質與 DR-20 §3.5(B) 相同，是治理 §3.8「審後變更…由 DA 判定必要後續」的 DA 判定，由 Orchestrator 依規則產出、不需再問 DA。Bindings §5／A-6 release gate 的「DA phase acceptance 已完成」一項，對 #29 之後的 subject 以 `phase-acceptance-SPEC.md` ＋ 兩份增補共同滿足。

**Fail-safe（何時仍需補充的 Spec Integration Audit instance）**：若 (A)-1 的 diff-scope 證明不成立、且該變更經 DA 判定仍在 boundary 內而被接受，或 #29 的 R1／R2／Alternate 流程產生 DA 無法關閉的 boundary finding，則 (A)(B) 不足：MUST 對新 HEAD 另派一次獨立的 Spec Integration Audit instance（Bindings §7 命名 `doc/governance/audit/spec-SPEC-c<n>-r1.md`，取下一個未用的 cycle 號，record 內註明「supplementary instance over changed subject，依 §3.8，不是 FA 授權的 rework cycle」），closure 後才可產出 (B)。此條由 Orchestrator 依規則機械判定。

### 3.6 DR-22.6 — README、ACCEPTANCE.md 與 Issue 的文字義務

1. **README ingestion 段（R-DOC-1、R-DOC-2）** MUST 補：`--acquired-at` 與 sidecar `acquiredAt` 的精確格式 `YYYY-MM-DDTHH:MM:SS+08:00`（一個例子）；明列拒絕的類型（空值、只有日期、無 offset、`Z` 或其他 offset、小數秒、空白分隔）；不合格時 fail-closed（訊息指名值與來源、exit 1、不寫入）；「`--acquired-at` 存在時不會退回 sidecar」。**MUST 維持** DR-17 §4.5 的語義措辭（取得自 CWA 的時間，不是發布時間、不是頁面時間；offline 重建不更新「last updated」）。措辭細節屬 HOW。
2. **`ACCEPTANCE.md` §6「#18 R2 N-1」列**：改為已修正並引用 #29 commit 與 audit record；AC 列不動。
3. **Issue #29**：Orchestrator 以 comment 引用本紀錄（控制面 bookkeeping）；Issue 的 DoD 第一項「DA decision record」以本紀錄滿足；不改 Issue 的其他 AC。
4. **`build_parser` 的 help**：SHOULD 顯示精確文法（例如 metavar `YYYY-MM-DDTHH:MM:SS+08:00`）。

---

## 4. 是否改變 accepted 語義

**否。** 既有 Outcome Contract 的 intent、scope、constraints 與 acceptance boundary（AB-8、AB-10、AB-11）不變；Spec v1.1 的每一條 R／AC／INV 文字與強度不變；DR-17 §4 的語義（取得時間、online 取一次、offline 不讀時鐘、缺少時 fail-closed、兩層顯示同一值）不變；沒有新增 requirement、AC、invariant 或 gate；#18–#25、#28 不重開。本紀錄所有裁決都是治理 §5.3 第 2 類：把 R-DB-5 已要求的格式與 DR-17 §4.3(3) 已要求的 fail-closed 姿態，具體化為兩條輸入路徑上可測試的接受準則（3.3 節），並具體化 assurance 要求（3.4、3.5 節）。3.3 節在 DR-17 容許的空間內所作的選擇（恰為秒、單一正規形、不正規化）只影響本 work item：合格值的既有行為不變，改變的只是對本來就違反 R-DB-5 的值的處置。本 work item 自身的 Outcome Contract（第 0 節）由 acceptor 接受並授權，DA 未代行任何接受或授權。

Issue #29 body「DR-17 §7 I-4 已將提交格式固定為…精確到秒」是對提交集合的正確描述，但不是 I-4 的字面（E-5）；Reviewer 引用時請引 DR-17 §4.1 與本紀錄 3.3 節，不要把「精確到秒」歸給 I-4。

---

## 5. 受影響的工作、dependencies 與既有 evidence

| 項目 | 影響 |
| --- | --- |
| **#29**（新，Lightweight） | 依本紀錄執行；Executor 以第 0 節＋Issue #29＋本紀錄為契約，維護 `worklog/20260924-acquired-at-validation.md`（Contract reference 依 C-1）；A-4 audit 必做（`audit/issue-29-c1-r1.md` 起），R1 範圍含 3.5(A)。完成後 STOP 回報票號與 subject SHA；不合併、不繳交。 |
| **#18–#25、#28** | 不重開；結案狀態與 audit records 不變。#18 R2 N-1 由 #29 關閉；N-2～N-5 維持 tracked（X-9）。 |
| **Spec v1.1、Outcome Contract、DR-17、derivation record、Bindings** | 不修改。 |
| **`phase-acceptance-SPEC.md`、map-rework 增補** | accepted subject `720c0a0` 與 #28 subject `5136bd2` 的判定不變；#29 之後依 3.5(B) 產出第二份增補，不改寫原紀錄。 |
| **`spec-SPEC-c1-r1.md`、`issue-18-c1-r2.md`** | 對 `data.db`、raw JSON、sidecar 的資料證據因 X-2（blob 不變）而**沿用有效**；對 offline 路徑行為的證據由 #29 audit 對受觸及部分重新取證。 |
| **`ACCEPTANCE.md`、`tickets.md`、README** | 都是 subject 的一部分（不是 record-only）；#29 的 subject SHA 以含這些檔案的 commit 為準（#25 F-3、#28 先例）。 |
| **Release gate（Bindings §5／A-6）** | 合併前材料 ＝ 既有清單 ＋ #28 材料 ＋ #29 audit closure ＋ 3.5(B) 第二份增補 ＋ 對 #29 subject 的 CI 綠。RB-1 仍由 acceptor。 |
| **Orchestrator run record** | 記錄本派工與 binding；#29 以新的 Lightweight work item 記錄（同 #28 的處理方式，MAY 在同一 run record 的「post-run Lightweight work items」段）；C-1 的確認寫入 run record 或 worklog。 |

---

## 6. Authority

- 本裁決在 Design Authority 的 lane eligibility、boundary determination、contract-sufficiency 與 assurance 權限內（治理 §2.1、§2.4、§3.3、§3.6-A、§4.1、§5.1）。
- **不需要 acceptor 的任何新動作即可開始 #29**：接受與授權已由第 0 節給出；Spec review 與 implementation authorization 未被 Bindings 保留（§2.6）。唯一的前置是 C-1（把 acceptor 原文載入 worklog）；若 (a) 無法被 Orchestrator 確認為 acceptor 核定文件的內容，那是授權缺口，route acceptor。
- **仍屬 acceptor 的事項**（本紀錄不請求，只列出）：RB-1 合併、RB-2 繳交、X-2（重新產生提交資料）、X-4／X-5（正規化或合理性檢查——會是 accepted 行為的改變或新 requirement）、X-9（N-2～N-5 的新指示）。
- Reviewer 保有 findings、severity、blocking 與 closure 的判定（§2.1、§4.3）；本紀錄不預判任何 finding；3.3.5 的 V-1～V-8 是 DA 對「充分證據」的要求，Reviewer 仍自行判定其是否被滿足。
- Final Adjudicator：目前沒有 routing 或 review 爭議，不需要。
- DA 未修改任何實作、測試、資料、README、Spec、OC 或 `doc/acceptance/`；未 commit；未 merge。

---

## 7. Evidence（DA 自行執行，全部唯讀；未印出任何金鑰）

- 讀取：Bindings b1 §0–§9；治理 v2.0 §1.2、§1.3、§1.4、§1.5、§2.1–§2.4、§3.1–§3.8、§4.1–§4.7、§5.1–§5.4；Outcome Contract 全文（含 §8 接受原文）；Spec v1.1 R-ING-3、R-ING-5、R-DB-5、R-GA-8、R-TC-1、R-SEC-2、R-DOC-1、AC-09、AC-11、AC-12、AC-24、INV-3、§4.1（grep 行 129–305）；DR-17 全文；`issue-18-c1-r2.md` 全文；`decision-20260923-high-risk-categories.md` 全文；DR-20 全文；DR-21 §0–§2；`phase-acceptance-SPEC-addendum-20260924-map-rework.md` 全文；`ACCEPTANCE.md:60-63, 168-189`；`README.md:101-143, 182-188, 223-229, 378-384`；`ingestion/pipeline.py`、`provenance.py`、`persist.py` 全文；`tests/test_pipeline.py` 全文；`tests/test_persist.py:14-18, 123-128`；`tests/test_weather_query.py:36-44`；`tests/test_app.py:224-230`；`tests/test_dashboard.py:274-280`；`tests/test_secrets.py`（grep）；`weather_query.py`、`app.py`（grep `ingestedAt`）；`data/raw/F-D0047-091.meta.json`；run record `run-20260924-hw01-formal.md`（grep N-1：第 61–62、90、99、122、130–140 行）；`worklog/20260924-taiwan-map-rework.md`（grep）；`tickets.md`（HEAD 與工作樹 diff）。
- 外部輸入：`gh issue view 29`（body、label `ready-for-agent`、OPEN、2026-09-24T08:30:29Z）；acceptor 支援 session scratchpad 的 `orchestrator-message-map-rework.md` 第 52–55、99–109 行（第 0 節 (a) 的來源）。
- Git：`git rev-parse HEAD` ＝ `cc29c7fed7dabc826b7d01f0d4d0b8104c235c59`；`git status --porcelain` ＝ ` M home_work_01/doc/ticket/tickets.md`、`?? grep.exe.stackdump`；`git log --oneline 5136bd2..cc29c7f` ＝ `cc29c7f`、`5d8b169`；`git diff --name-only 5136bd2 cc29c7f`（六個 doc 檔）；blob ids 見 E-2。
- SQLite（唯讀 URI）：`SELECT * FROM IngestionMetadata` ＝ `(1, '2026-09-24T02:24:50+08:00', 'F-D0047-091')`；`sqlite_master` 兩表。
- Python 探測（3.11.2；語義與專案 pin 的 3.12 相同）：`fromisoformat` 與 `strptime %z` 對 NG-3、NG-4、NG-6、NG-7、NG-9、NG-10 的接受情況（E-6）。
- Grep：`home_work_01/doc/governance/` 內 DR 編號最高為 DR-21（本紀錄取 DR-22）；`tests/**` 內所有 `YYYY-MM-DDTHH:MM` 字面值（E-7）。
