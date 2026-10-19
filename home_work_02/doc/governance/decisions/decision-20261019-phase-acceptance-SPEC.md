# Decision record — Phase acceptance：SPEC rev 5（#59）

- **紀錄類型**：Design Authority phase acceptance（治理 §3.4、§3.8；orch-default v2.2 §6、§7 P10；Bindings b5 §5、§7）
- **日期**：2026-10-19
- **Run**：`run-20261018-hw2-formal`。Orchestrator 在 Spec Integration Audit closure 之後依 orch-default §6 派工（run record §20 最後一點）。
- **Phase**：唯一的一份 derived Spec `doc/spec/SPEC.md` **rev 5**（＝GitHub issue #59），Tickets #60～#67。
- **受審 subject**：branch `home_work_02-regrill`，最終整合 implementation commit **`e2780f46dbea4d0816a6dcc8bba0725bc6182797`**（整合範圍 `60d7fa6..e2780f4`）。撰寫時 HEAD＝`bdcfd16`；`git diff --name-only e2780f4 HEAD` 只有 `doc/governance/{audit,run,worklog}/**` 與 `doc/ticket/tickets.md`（record-only，Bindings §7）；工作樹對 `e2780f4` 的非紀錄路徑無差異（`git diff --quiet`）。未追蹤產物以 sha256 識別：`dist/<學號>_hw2.zip` `c84a3c5e6d295ed383fc8c085eb68f30aaa9035208cf9ca7eeaa0d9aae763fb6`（我重新計算，相同）。
- **Binding**：`gov-design-authority`，`claude-opus-5-5`／`high`（Bindings §3.1 預設 mapping，沒有 escalation，沒有替代）。本紀錄不自證 binding，由派工者依 Bindings §3.6 核對。
- **Capability escalation**：不提出。E-DA/D1 不成立：是否接受只取決於已存在的 closure record、各票的結案證據與 acceptor 已作的決定（AD-1、AD-3），沒有兩個後果不同而證據無法裁決的設計。E-DA/D2 不成立：我先前的決定沒有被 FA ruling 或經 route 的 Reviewer finding 推翻或爭議。
- **獨立性**：Orchestrator、Executor 與 Reviewer 的敘述（含 Spec Integration Audit record）只當作待驗證主張；第 3 節列出我自己取得的證據。

## 1. 問題

SPEC rev 5 的 phase 能否由 Design Authority 接受（治理 §3.8：跨 Ticket invariants、整合行為、累積 evidence 與未結 follow-up），以及接受之後還剩哪些 open items、各由誰負責。

## 2. 裁決

**PHASE ACCEPTED — SPEC rev 5（#59）**，subject `e2780f46dbea4d0816a6dcc8bba0725bc6182797`，附第 5 節的 open items。

本裁決**只**陳述 phase acceptance。依治理 §3.8 與 orch-default §7，四種陳述分開如下：

| 陳述 | 狀態 | 決定者 |
| --- | --- | --- |
| Work item completion（#60～#67） | 已由 Orchestrator 依 orch-default §7 P1～P8 結案（run record §7、§10～§13、§15、§18、§20）；本紀錄引用，不重新宣告 | Orchestrator（依 Reviewer closure 與 DA records） |
| **Phase acceptance（SPEC rev 5）** | **ACCEPTED**（本紀錄） | Design Authority |
| Run completion | **本紀錄不陳述**。Terminus 與 completion report 屬 Orchestrator（orch-default §8） | Orchestrator |
| Release authorization | **未授予**。合併進 `main` 屬 RB-1；OC 沒有引用 SA-3（OC §2「Git」列），所以 SA-3 不適用。繳交屬 RB-2 | Acceptor |

另外，本裁決**不是** Outcome Contract 的完成：Brief §7「同一份檢查也在 GitHub Pages 的網址上做一次」與 §10「Pages URL 可開啟」依 AD-3 由合併後的 Lightweight work item 承擔，在它以 audit closure 結案前，Outcome Contract 的整個 acceptance boundary 尚未全部滿足（第 5 節 OI-1）。

## 3. 依據

### 3.1 P10：Spec Integration Audit closure record

- **引用**：[`../audit/spec-SPEC-c1-r1.md`](../audit/spec-SPEC-c1-r1.md) — Spec Integration Audit，SPEC rev 5，cycle 1，R1，**`VERDICT: CLOSURE`**（檔尾），commit `bdcfd16`。
- **我核對的事項**：
  1. **獨立 audit instance**：record 第 7 欄寫明不是任何 Ticket audit 的 R3；Spec 有 8 張票，不適用單 Ticket fast path（Bindings §5）。
  2. **Separately bound、自寫**：我讀取 subagent transcript `agent-a5b2226e12e62438f`：meta `agentType`＝`gov-primary-reviewer`；assistant 訊息 `('claude-opus-5-5', 'xhigh')` 340 則，單一元素，符合 R-PR mapping。該 transcript 中對 `audit/spec-SPEC-c1-r1.md` 的最後一次 Write 內容，與 `bdcfd16` 中的檔案逐字相同（只比較 EOL 正規化後的文字）。
  3. **治理 §4.7 五個範圍**：§2 跨 Ticket invariants（I-1～I-9）；§3 Spec-level AC coverage（S-1～S-20，含 §3.2 對所分配 boundary 與「全部 derived Specs」的涵蓋核對——本 Spec 是同一 Outcome Contract 唯一、也是最後一份 Spec）；§4 整合行為（乾淨環境一次重跑 bit-exact 重現 #63 的 `result_digest`；解壓 ZIP 離線、零對外請求）；§5 最終 subject 的 verification／audit coverage；§6 traceability 與 boundary 符合性。
  4. **Subject**＝最終整合 subject `e2780f4`，之後只有 record-only delta。
  5. **Findings 與 routing**：沒有 blocking finding；F-1（Low，non-blocking）；§11 沒有 route 給 DA 的設計或 boundary 事項。沒有需要 FA disposition 的未解 blocking。
  6. **DA records 的必核項目**：§7 逐項判定 A-2、A-3、A-5、A-6、S-5、cell 28／G-5、N-3、N-5、#66 F-1、R-1.5、D-4 符合；AD-3 列為 open item。§8 H-1～H-4 符合。

### 3.2 Work item 結案（P1～P9）

- `gh issue list`：#60～#67 全部 **CLOSED**；#59（Spec）OPEN——Spec 的結案以本紀錄為前提，屬 Orchestrator 的控制面動作（第 5 節 OI-9）。
- 每張票的最後一份 audit record 都是 `VERDICT: CLOSURE`：#60 R1、#61 R2（R1 BLOCKING）、#62 R1、#63 R1、#64 R1、#65 R2（R1 BLOCKING）、#66 R1、#67 R1。兩次 BLOCKING 都以同一 worklog identity 的 targeted correction 與 R2 closure 處理。
- 每個 routed design question 都有 DA record：`decision-20261018-issue60-a4-student-id.md`、`-issue62-shared-subset-test-key.md`、`-issue63-js-tolerance.md`、`-issue64-notebook-rerun.md`、`-issue64-standardized-reading.md`、`decision-20261019-issue65-labels-figures.md`、`-cell28-glyphs.md`。沒有懸而未決的 design ambiguity。
- **P9（跨 Ticket 整合驗證）**：在 phase 層由 Spec Integration Audit §2、§4 承擔，另見 3.4 節我自己的核對。

### 3.3 累積的 DA 義務與 derivation findings 的狀態

| 來源 | 狀態 |
| --- | --- |
| derivation §7 F-1（Ridge／Lasso test） | RESOLVED：CC-1；SIA S-9 核對六項約束成立 |
| derivation §7 F-2（CONTEXT 修訂表與 CV winner 措辭） | RESOLVED：Brief §14 補記；措辭依 AD-2 修正 |
| derivation §7 F-3（CI 敘述） | RESOLVED：AD-2、N-10（Spec rev 5） |
| derivation §7 F-4（T-義務） | 由票帶入；SIA §3.2 確認在最終 subject 上成立 |
| derivation §7 F-5（OV-2～OV-5 門檻，原定 phase acceptance 前決定） | RESOLVED：AD-1；ACCEPTANCE E 節 required gates PASS，best-effort 無環境者記 NOT TESTED |
| derivation §9.5 TK-1（Pages） | AD-3：合併後的 Lightweight work item → **OI-1** |
| derivation §9.5 TK-2～TK-5 | 成立（SIA §3.2） |
| derivation §9.3 條件 1～6、§9.6 TR-01、TR-02 | 成立（SIA I-2、I-3） |
| derivation §11 G-1～G-4 | 成立（SIA S-9） |
| derivation §11 G-5（CONTEXT 重複的 `_Avoid_`） | RESOLVED：`CONTEXT.md` 的 Metric-only model 詞條現在只有一行 `_Avoid_`（我讀檔核對） |
| high-risk A-1～A-8、H-1～H-4 | 符合（SIA §7、§8；各票 R1／R2） |
| student-id S-1～S-6 | S-2 完成（run record §19）；S-4 由 #67 R1 與 SIA 重做；**S-5 在 phase acceptance 時點**由我重做（3.4 節），0 命中；S-3／S-5 對之後的 push 與合併仍有效（OI-6、OI-7） |
| notebook-rerun N-1～N-6、條件 7、8；acceptor 回覆 run record §14 第 1～3 點 | 成立（SIA §4.1、§7 N-3、N-5） |
| standardized-reading R-1.1～R-1.5、labels-figures L-1～L-3／F-1～F-5、cell28 G-1～G-5、js-tolerance T-1～T-3、shared-subset D-1～D-4 | 成立（SIA §7、I-5、I-6、S-2） |

### 3.4 我自己取得的證據

| 項目 | 結果 |
| --- | --- |
| `python -m pytest -q`（單元 `.venv`，工作樹＝`e2780f4` 的非紀錄路徑） | **395 passed**（49.4 s） |
| `node --test tests/js/core.test.js` | 12 項：9 pass、0 fail、3 skipped（fixture 版需環境變數；含官方逐筆 PI 重算 pass） |
| `results/model_data.json` 的不變量 | `test` 鍵＝{`allin`, `forward_sfs_k17`（`ols_subset`），`ridge`, `lasso`（`metric_only`）}；`winners.authorized_test_models`＝{`allin`, `forward_sfs_k17`}；`metric_only` 只有 alpha、kind、mae、mse、rmse、r2、n_test、scale、model_key（無 PI、coverage、逐筆欄位）；`methods`／`baselines` 中名稱含 `test` 的鍵 0 個；manifest `selection_digest`＝`44f7723e…4b28`、`evaluations_in_this_run`＝1、`official_data`＝true |
| ZIP | sha256＝`c84a3c5e…3fb6`，與 run record §20、SIA 表頭相同 |
| Boundary | `git diff --name-only 60d7fa6 e2780f4`：114 個檔；單元外只有 root `README.md`、`CONTEXT-MAP.md` 各 +1 行（RB-5，acceptor 授權見 run record §19）；`doc/requirement/` 0 個；`origin/home_work_02-regrill` 仍是 `60d7fa6`（沒有 push、merge、deployment） |
| S-5 學號比對（phase acceptance 時點） | 比對值只在記憶體中讀自 `.local/packaging.json`。範圍 `origin/main`（`5be4d39`）..`HEAD`（`bdcfd16`），**91 個 commit**：每個 commit 的樹（`git grep -F -q`）0；commit message 與作者／committer 欄位 0；同一 range 的 patch（`--binary`）0；工作樹追蹤檔案 0。本紀錄寫入後另以同一方法核對本檔：0 |

### 3.5 Acceptance boundary 與 boundary 符合性

- `derivation-SPEC.md` §4 把 Outcome Contract 的**全部** acceptance boundary 分配給這份唯一的 Spec。SIA §3.2 逐條對照 Brief §3～§11 的驗收意圖，結論是除 AD-3 明確移出的 Pages 項目以外全部涵蓋，沒有分配缺口或造成歧義的重疊。我同意：Pages 項目不是 Spec 分配的缺口，而是 acceptor 以 AD-3 把它的執行安排到合併之後；AD-3 原文明定 Spec Integration Audit 與 phase acceptance 把它列為 open item、不阻擋。
- 我沒有發現需要 boundary determination 的疑義：整合 diff 的單元外變更在 RB-5 授權範圍內；CC-1 的範圍沒有被超出（`test` 只有 4 個鍵）；Out of Scope 的項目沒有出現（SIA S-19）。

### 3.6 觀察（不影響裁決）

- ACCEPTANCE.md 記錄的「核對的 subject」是 `e2f391a`（ZIP 的打包 commit）。之後到 `e2780f4` 的 delta 只有 root 兩列、ACCEPTANCE 本身與 `tests/test_report.py`，都不在 ZIP 內（SIA O-2、§5）。不需處理。
- Executor 在 #65 以 shell 寫入交付物的作法經 acceptor 同意（run record §15）；內容已由 #65 R1／R2 與 SIA 依 A-5 審查。不需處理。

## 4. 是否改變 accepted 語義

**否。** 本紀錄只作 phase acceptance，不修改 Brief、CC-1、AD-1～AD-3、Spec、Tickets 或任何 derived contract，不新增或移除 acceptance 條件。Pages 項目的處理沿用 acceptor 的 AD-3，不是 DA 的豁免或 scope 縮減。不需要 acceptor 對本裁決核准。

## 5. Phase acceptance 之後的 open items

依治理 §1.2，下列 follow-up 在 acceptor 接受並授權前只是 tracked items，不得作為新工作執行（OI-1 的安排已由 AD-3 接受，但執行仍以合併後 acceptor 的直接指示為其 Outcome Contract）。

| ID | 項目 | Owner／所需 authority | 說明 |
| --- | --- | --- | --- |
| **OI-1** | **AD-3：GitHub Pages URL 檢查**（Brief §7、§10；Spec 人工檢查表 Pages 項；ACCEPTANCE D-12 NOT TESTED（pending merge）；SIA S-12） | **Acceptor** 在 RB-1 合併後以直接指示啟動；執行者為該 Lightweight work item 的 direct-execution Executor | 觸及 H-2：依 `decision-20261018-high-risk-categories.md` §4 **必須 independent audit**。依 SIA F-1，同一 work item 一併開啟報告第九章的原始碼連結。結案後才可陳述 Outcome Contract 的 acceptance boundary 全部滿足 |
| **OI-2** | **SIA F-1**（Low）：報告第九章的 Pages 與原始碼連結在合併前都是 404，報告沒有標明合併後才可開啟 | **Acceptor**（安排 RB-1 先於 RB-2，或接受合併前繳交時連結暫時無效）；**OI-1 的 work item**（核對兩個連結） | 若 acceptor 要在報告加註，那是報告文字修改加重新打包（H-2），以新的 work item 處理，並觸及 OI-3 |
| **OI-3** | **#67 R1 F-1**（Low）：`package.check_committed()` 缺測試 | **之後任何修改 `hw2/package.py` 或重新打包的 work item** | 目前不需行動 |
| **OI-4** | **#67 R1 F-3**（Low）：ZIP 內 README 的重跑步驟以 repo 為前提 | **Acceptor**（是否在繳交前加註，RB-2 範圍） | 若要修改：新的 work item（README＋重新打包，H-2 → audit），並觸及 OI-3 |
| **OI-5** | **#66 R1 F-2**（Low）：`hw2/pdf_append.py` 對支援範圍外的兩類輸入沒有拒絕 | **Acceptor 重新提供 ChatGPT PDF 時，更新釘值的 work item** | 目前不需行動 |
| OI-6 | Push 授權：`60d7fa6..HEAD` 全部未 push（push 選項 (a)，run record §1、§9） | **Acceptor**（逐次授權）；Orchestrator 在每次 push 前機械執行 S-3（涵蓋到該次 push 的 tip，含本紀錄的 commit） | — |
| OI-7 | 合併進 `main`（RB-1） | **Acceptor** | Bindings §5 的 Formal gate（全部票結案、SIA closure、DA phase acceptance）在本紀錄後成立；README 的重跑步驟已實際跑過（SIA §4.1、O-3；`worklog/issue-67.md` §7）；追蹤檔案無機密（SIA S-15、H-1）。合併前 S-5 必須涵蓋到合併時的 subject。這些是合併的前提，不是授權 |
| OI-8 | 繳交（RB-2） | **Acceptor** | 繳交物 `dist/<學號>_hw2.zip`，sha256 `c84a3c5e…3fb6`；先後順序見 OI-2 |
| OI-9 | Spec #59 結案、`doc/ticket/tickets.md` 與 run record 的 phase acceptance 狀態、run record §8 S-3～S-5 的狀態更新、terminus 與 completion report | **Orchestrator**（控制面） | 引用本紀錄；四種陳述分列（第 2 節） |

**已處理、不列為 open**：#67 R1 F-2（Orchestrator 已刪除含學號的瀏覽器暫存 profile 並重掃為 0，run record §20、`e383a14`）；#60～#66 的其他 non-blocking findings（SIA §9 確認已由後續票解決）。AD-1 的 best-effort 項目（真實觸控裝置、Safari、螢幕閱讀器）如實記為 NOT TESTED，是 acceptor 決定的非 gate 項目，不需 owner 動作。

## 6. 受影響的 work items

| 對象 | 影響 |
| --- | --- |
| #59（SPEC rev 5） | Phase accepted；可由 Orchestrator 結案（OI-9） |
| #60～#67 | 無變更；已結案 |
| Run `run-20261018-hw2-formal` | Phase acceptance 已完成；terminus 由 Orchestrator 判定 |
| Pages Lightweight work item（AD-3） | 尚未建立；OI-1 |
| Spec、Brief、Outcome Contract、Tickets、程式、測試、notebook、ACCEPTANCE.md | 本紀錄不修改 |

## 7. Evidence

- 讀取：Bindings b5（§2、§3.2、§4、§5、§7）；治理 v2.2 §1.2、§1.4、§1.5、§2.1、§2.4、§2.5、§3.4～§3.8、§4.6、§4.7、§5.1～§5.3；orch-default v2.2 §6、§7（P9、P10）、§8；`outcome-contract.md`（CC-1、AD-1～AD-3）；`derivation-SPEC.md`（全文）；本目錄全部 decision records；`audit/spec-SPEC-c1-r1.md`（全文）；`audit/issue-66-c1-r1.md`、`audit/issue-67-c1-r1.md` 的 findings；全部 audit records 的 verdict；`run/run-20261018-hw2-formal.md`（全文）；`worklog/issue-67.md` 的 remaining work；`doc/acceptance/ACCEPTANCE.md` 的 NOT TESTED 項目；`CONTEXT.md` 的 `_Avoid_` 行。
- 執行：`gh issue list`（#59～#67 狀態）；`git rev-parse`、`git diff --name-only`／`--numstat`／`--quiet`；單元 `.venv` 的 pytest；Node test；以 Python 讀取 `results/model_data.json` 的鍵與 manifest；`sha256sum` ZIP；SIA reviewer transcript 的 binding 與 Write 內容比對；只輸出計數的學號比對（腳本在 session scratchpad 的 `da-pa/`，不在 repo）。
- 沒有執行 notebook、`hw2.run_notebook`、`hw2.package` 或任何會開啟 test 守門的程式。寫入的檔案只有本紀錄；沒有修改 Spec、Outcome Contract、Tickets、程式或其他紀錄；沒有 commit 或 push。

## 8. Required authority

本裁決不需要其他 authority，也不需要 escalation。第 5 節中由 acceptor 負責的項目（OI-1 的啟動、OI-2、OI-4、OI-6～OI-8）都是既有的 reserved boundaries 或 acceptor 自己的決定，不是本紀錄新增的 gate。
