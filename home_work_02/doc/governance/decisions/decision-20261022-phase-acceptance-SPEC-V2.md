# Decision record — Phase acceptance：Spec V2 rev 2（#73）

- **紀錄類型**：Design Authority phase acceptance（治理 §3.4、§3.8、§4.7；orch-default v2.2 §6、§7；Bindings b5 §5、§7）
- **日期**：2026-10-22
- **Run**：`run-20261022-hw2-v2-enhance`（Orchestrator＝root session `37216426-f292-44f9-bad1-e2d862e7b8f1`；run record dispatch 第 26 列）。本派工是 [`decision-20261022-sia-f1-dashboard-wording.md`](decision-20261022-sia-f1-dashboard-wording.md) 第 5 節所定的重新派工：該紀錄把 phase acceptance 延後到 SIA-F1 的 rework、Executor binding 核對、Spec Integration Audit cycle 1 R2 closure 與 P7 核對都完成之後。
- **Phase**：Outcome Contract §5（V2 Enhance）唯一的一份 derived Spec：`doc/spec/SPEC-V2.md` **rev 2**（＝GitHub issue #73），Tickets #74～#78。
- **受審 subject（最終整合 subject）**：branch `home_work_02-v2-enhance`，commit **`17f10a7c1626bd334bee82c93202822d0e9f6976`**（實作 commit `69f8e0794ec0fb5b4f1fcda7a1f62bc74912a89d`；V2 範圍 `d7f02d4..17f10a7`）。撰寫時 HEAD＝`6303a06e8796b6612e8d2c99a96204cfe02fc225`；`git diff --name-only 17f10a7 HEAD` 只有 `doc/governance/audit/spec-SPEC-V2-c1-r2.md` 與 run record（record-only，Bindings §7）；工作樹在 `home_work_02/` 內沒有修改或未追蹤的非忽略檔案，對 `17f10a7` 的非紀錄路徑 `git diff --quiet` 成立。`main`＝`origin/main`＝`392e9df`；`origin` 上沒有此 branch。未追蹤的繳交物 `dist/<學號>_hw2.zip`：sha256 `8a51fc1ca26d176f3edb075f7f8aeda7a0dc659531484c10e695bc3800d08f8d`（我重新計算，等於 `dist/hw2_package_manifest.json` 的 `zip_sha256`，打包 commit `69f8e07`）。
- **Binding**：`gov-design-authority`，有效 mapping `claude-opus-5-5`／`high`（Bindings §3.1 預設；沒有 escalation、沒有替代）。撰寫前我自行掃描本 assignment 的 transcript（agentId `a7c01dd8574c584bb`，`agentType` `gov-design-authority`）：`('claude-opus-5-5', 'high')` 90 則，單一元素。全程核對由派工者依 Bindings §3.6 執行；本紀錄不自證 binding。
- **Capability escalation**：不提出。E-DA/D1 不成立：是否接受只取決於已存在的 closure records、各票結案證據、既有 DA 裁決與我自己的核對，沒有兩個後果實質不同而證據無法裁決的設計選擇。E-DA/D2 不成立：我在本單元先前的決定（derivation、R3、R4、C1／C2、CF、S1）沒有被 FA ruling 或經 route 的 Reviewer finding 推翻或實質爭議；SIA R2 以 `VERDICT: CLOSURE` 確認 S1 的 rework，並把 `#ex-lasso-card` 記為與 S1-6 一致的觀察（R2-O1）。
- **獨立性**：派工內容、run record、Executor worklog 與 Reviewer records 的敘述都只當作待驗證主張；第 3 節列出我自己取得的證據。

## 1. 問題

Spec V2 rev 2 的 phase 能否由 Design Authority 接受（治理 §3.8：跨 Ticket invariants、整合行為、累積 evidence、未結 follow-up），以及接受之後剩下哪些 open items、各由誰負責。

## 2. 裁決

**PHASE ACCEPTED — Spec V2 rev 2（#73）**，最終整合 subject `17f10a7c1626bd334bee82c93202822d0e9f6976`，附第 5 節的 open items。第 5 節的項目沒有一項記為 PASS。

依治理 §3.8，下列四種陳述分開：

| 陳述 | 狀態 | 決定者 |
| --- | --- | --- |
| Work item completion（#74～#78） | 已由 Orchestrator 依 orch-default §7 P1～P8 結案（run record #74～#78 結案核對表；#78 的 closed subject 依 SIA R2 與 P7 更新為 `17f10a7`）。本紀錄引用，不重新宣告 | Orchestrator（依 Reviewer closure 與 DA records） |
| **Phase acceptance（Spec V2 rev 2）** | **ACCEPTED**（本紀錄） | Design Authority |
| Run completion | **本紀錄不陳述**。Terminus 與 completion report 屬 Orchestrator | Orchestrator |
| Release authorization | **未授予**。OC §5 沒有引用 SA-3，合併進 `main` 屬 RB-1；push 未授權（OC §5.1；designation 第 6 點）；繳交屬 RB-2 | Acceptor |

本裁決**不是** Outcome Contract 的完成。Brief V2 §8 第 3 條「於 Pages 上」、§3.2「Pages 與 ZIP 一致」與 §14 P0「Pages 可正常存取」依 derivation B-10 由合併後的 Lightweight work item 承擔。在該 item 以 independent audit closure 結案前，V2 的 acceptance boundary 沒有全部滿足（OI-V2-1）。

## 3. 依據

### 3.1 已 closure 的 Spec Integration Audit（治理 §3.8、§4.7；orch-default §7 P10）

| 紀錄 | 內容 | 我核對的事項 |
| --- | --- | --- |
| **SIA R1**：[`../audit/spec-SPEC-V2-c1-r1.md`](../audit/spec-SPEC-V2-c1-r1.md) | cycle 1、R1，subject `3745e9c`，**`VERDICT: CLOSURE`**（檔尾），committed `3750de4` | (1) 獨立的 audit instance；檔頭寫明不是任何 Ticket audit 的 R3；有五張票，不適用單 Ticket fast path（Bindings §5）。(2) §1 逐項聲明治理 §4.7 的五個範圍：§2 跨票 invariants，§3 Spec AC S-01～S-35，§3.1／§3.2 分配與「全部 derived Specs 合起來」，§4 整合行為，§5 coverage，§6 traceability。(3) Findings SIA-F1～F5 都是 Low、non-blocking；SIA-F1 route 給 Design Authority；B-10 是 open item |
| **SIA-F1 決定**：[`decision-20261022-sia-f1-dashboard-wording.md`](decision-20261022-sia-f1-dashboard-wording.md) | S1-1～S1-7：第 12.5 節加入說明（C-1～C-4）；SIA-F2 可一併處理（S1-6）；審後驗證以同一 instance 的 R2 進行（S1-5）；phase acceptance 延後（第 5 節）；不改變 accepted 語義 | 第 5 節的四個前提都成立：rework `69f8e07`＋`17f10a7`；Executor binding（見下）；R2 CLOSURE；P7（本紀錄檔頭） |
| **SIA R2**：[`../audit/spec-SPEC-V2-c1-r2.md`](../audit/spec-SPEC-V2-c1-r2.md) | 同一 instance、cycle 1 R2，subject **`17f10a7`**，**`VERDICT: CLOSURE`**，committed `6303a06` | (1) 範圍限於治理 §4.4 的 R2（SIA-F1、SIA-F2 是否解決，以及回歸）。(2) SIA-F1 逐項符合 C-1～C-4 與形式限制，判為 resolved。SIA-F2 在 README 與報告兩處 resolved；`index.html` 依 S1-6 不在範圍（R2-O1）。(3) ZIP 中 dashboard 的 17 檔與 blob 逐位元相同；新舊 ZIP 只有 `hw2_report.pdf` 與 `README.md` 不同。(4) Reviewer 判定舊 ZIP 上的 OV-1／SR-09 頁面證據可以延用（evidence sufficiency 屬 Reviewer），並另做確認性重做。(5) R2-O1、R2-O2 是觀察 |

- **Binding 與自寫**：我掃描 SIA reviewer 的 transcript `agent-aa43e1e2fb1e18487`：`agentType`＝`gov-primary-reviewer`，`('claude-opus-5-5', 'xhigh')` 280 則（R1＋R2 及其後），單一元素，符合 R-PR。我把該 transcript 中寫入 `spec-SPEC-V2-c1-r1.md` 與 `spec-SPEC-V2-c1-r2.md` 的 Write 內容，與 HEAD 中的檔案比較（只正規化 EOL）：兩份**逐字相同**。
- **Rework 的 Executor binding**：`agent-acc8906c845bfc14f`（`gov-executor`）：`('claude-opus-5-5', 'high')` 248 則，單一元素，與 run record 第 24 列相同。
- **R2 的 subject 等於最終整合 subject**：R2 以 `17f10a7` 為新的最終整合 subject；我核對 `3745e9c..17f10a7` 中非 `doc/governance/` 的路徑，只有 `README.md`、`report/report.md`、`doc/acceptance/ACCEPTANCE.md`、`doc/screenshots/v2-issue78/zip_manifest_rework_69f8e07.txt`，正是 S1-5 第 2 點允許的集合（含採用 S1-6 時的 README）。`3750de4`、`cec4c93`、`6303a06` 只動 `doc/governance/**`。

### 3.2 Work item 結案（P1～P9）

| 票 | 最後一份 audit record（Reviewer 自寫） | Routed design questions 的 DA 紀錄 |
| --- | --- | --- |
| #74 | `issue-74-c1-r1.md` BLOCKING（R1-F1）→ `issue-74-c1-r2.md` **CLOSURE** | R1-F3 → [`decision-20261022-r1f3-v1-footer.md`](decision-20261022-r1f3-v1-footer.md) |
| #75 | `issue-75-c1-r1.md` **CLOSURE** | R1-F1 → [`decision-20261022-issue75-lasso-early-stop.md`](decision-20261022-issue75-lasso-early-stop.md) |
| #76 | `issue-76-c1-r1.md` BLOCKING（R1-F1）→ `issue-76-c1-r2.md` **CLOSURE** | —（R3-5 已處理） |
| #77 | `issue-77-c1-r1.md` BLOCKING（R1-F1～F3）→ `issue-77-c1-r2.md` **CLOSURE** | C-1、C-2 → [`decision-20261022-issue77-resource-limits.md`](decision-20261022-issue77-resource-limits.md)；R1-F3 → [`decision-20261022-issue77-cancel-final-phase.md`](decision-20261022-issue77-cancel-final-phase.md) |
| #78 | `issue-78-c1-r1.md` **CLOSURE**；SIA-F1／F2 的 rework 由 SIA R2 涵蓋（S1-5） | SIA-F1 → `decision-20261022-sia-f1-dashboard-wording.md` |

- 每份 record 的最後一行都是我自己讀的。三次 BLOCKING 都以同一 worklog identity 的 targeted correction 與 R2 closure 處理，沒有 Alternate Review 或 FA。
- **自寫**：我把五個 ticket reviewer transcript 中對各自 record 的 Write 內容與 HEAD 比較。`issue-74-c1-r1/r2`、`issue-75-c1-r1`、`issue-76-c1-r2`、`issue-77-c1-r2` 逐字相同。`issue-76-c1-r1`、`issue-77-c1-r1`、`issue-78-c1-r1` 各有一到三處行號的差異，來源是同一 reviewer 在自己的 transcript 中以 Bash（`sed`／`python`）更正行號引用；仍然是 reviewer 自寫，沒有派工者的修改。
- **Executor 與 Reviewer 的 binding**（我掃描）：Executors `addc2dc935a7822fe` 209、`a5dedd102dd077202` 296、`acd62ed3a70012296` 262、`a7b3c024fa9b13368` 434、`acc8906c845bfc14f` 248，全部是 `('claude-opus-5-5','high')`。Reviewers `a940e0242c7bf7572` 219、`a9a75e1af80e98547` 181、`ad730583783ecd443` 192、`ab93f858531ba9d08` 255、`a1f8b04c1327ec029` 223，全部是 `('claude-opus-5-5','xhigh')`。DA assignments 全部是 `('claude-opus-5-5','high')`。每一個都是單一元素。
- 沒有懸而未決的 design ambiguity：每個 routed question 都有 DA 紀錄，所有 DA 紀錄都判定不改變 accepted 語義，也都沒有 acceptor 待決項。唯一的 contract change CC-V2-1 已由 acceptor 決定（OC §5.2）。
- **P9（跨 Ticket 整合驗證）**：在 phase 層由 SIA R1 §2、§4 承擔，另見 3.3、3.4 節。

### 3.3 跨 Ticket invariants（我自己的核對，subject `17f10a7`／HEAD）

| Invariant | 方法 | 結果 |
| --- | --- | --- |
| 正式分析不變（A-3 V2） | `git show d7f02d4:<p>` 與 `HEAD:<p>` 的 sha256 | `assets/app.js` `c1ab3f21…`、`assets/hw2core.js` `e75c5d48…`、`assets/model_data.js` `6cf0c11e…`、`results/model_data.json` `69dc1465…`、`assets/style.css` `60a27016…`：兩者相同 |
| 凍結路徑 | `git diff --stat d7f02d4 HEAD -- results hw2.ipynb doc/spec doc/brief doc/ticket CONTEXT.md doc/requirement` | 空 |
| `hw2/` | `git diff --name-status d7f02d4 HEAD -- hw2` | 只有 `A explore_reference.py`、`M offline_scan.py`（B-2） |
| 既有測試（I-5、CC-V2-1） | `git diff --diff-filter=MD d7f02d4 HEAD -- tests` | 只有 `test_dashboard_static.py`；diff 只把 `<script src>` 清單由 V1 四檔延長為 V1 四檔（順序不變）＋六個 V2 腳本，與 CC-V2-1 的授權逐字相符 |
| V1 DOM／文字 | `git diff --numstat d7f02d4 HEAD -- index.html` | `209 0`：只新增、沒有刪除 |
| Boundary（RB-5） | `git diff --name-only d7f02d4 HEAD` | 全部在 `home_work_02/` 內；沒有 `doc/requirement/` |
| 契約版本 | 檔案 sha256；`gh issue view 74..78 --json body` 的 sha256 | `SPEC-V2.md` `695161db…`、`BRIEF-V2.md` `27f08b25…`、`tickets-v2.md` `f1e6b1a6…`；#74～#78 本文 `49e3cc50…`、`834a439c…`、`5d121dd9…`、`c9b79356…`、`5e31ce34…`：與 derivation §3 的 accepted 版本相同 |
| H-1／A-4 學號（S-5，phase acceptance 時點） | 比對值只在記憶體中讀自 `.local/packaging.json`，不印出；範圍 `392e9df..HEAD` | 40 個 commit 的樹 0；commit message 與作者／committer 欄位 0；patch（`--binary`）0；工作樹追蹤檔 0；ZIP 67 個項目的內容 0 |
| 機密 | `git ls-files` 中的 `.env` | 無；本單元沒有 API key |

### 3.4 整合行為

- **我自己執行**（工作樹＝`17f10a7` 的非紀錄路徑）：
  - `.venv/Scripts/python -m pytest -q -rs -p no:cacheprovider`：**478 passed**，沒有 skipped（113.85 s）。
  - `node --test` 六個探索測試檔（Node v24.19.0）：**88 pass、0 fail、0 skipped、0 cancelled**。
  - `python -m hw2.offline_scan`：13 files、PASS（0 findings）。
- **ZIP**（`python -I`，只讀）：
  - sha256 等於打包 manifest；`testzip()` 無錯；67 個項目。
  - ZIP 內 `index.html` 與 `assets/` 的 17 檔與 `69f8e07` 的 blob 逐位元相同（差異 0），所以 ZIP 的 dashboard 就是合併後 Pages 會發布的位元組。
- **瀏覽器層級**：我沒有自己啟動瀏覽器。整合行為依下列證據，我判定足以作 phase acceptance：
  - SIA R1 §4：Chrome 與 Edge，在 ZIP 解壓頁面的 `file://`＋離線、兩個 http origin 的 URL 入口、非阻塞／取消／重跑、H-5 構造輸入。
  - SIA R2 §6：在新 ZIP 的確認性重做。
  - ACCEPTANCE V2-37～V2-40。
  - 理由：從 `3745e9c` 到 `17f10a7`，頁面載入的位元組沒有改變，這是 R2 §5 的結論，我也以 blob 比對自行確認。
- SIA R1 §4 的結論是：#74 的下拉與 All-in 鏈、#75 的四種方法與退化、#76 的 URL／檔案入口與請求隔離、#77 的預算、非阻塞、取消（含尾段）與可重現性、#78 的文件與 ZIP，在整合 subject 上一起運作，彼此不破壞對方的不變量。
- SIA R2 確認 rework 沒有改變程式、頁面或測試。上面的自動測試結果與此一致。

### 3.5 累積的 DA 義務與 derivation findings

| 來源 | 狀態 |
| --- | --- |
| derivation B-1～B-9、B-11、B-12、B-14 | 成立（SIA R1 §2、§6） |
| derivation B-10（Pages） | **Open**：OI-V2-1 |
| derivation B-13／F-1 | RESOLVED：CC-V2-1（OC §5.2）；修改只限授權的斷言（3.3 節） |
| derivation F-2（G-1～G-5） | 成立（SIA R1 §2.4、S-01、S-06、S-13、S-17、S-26、S-29） |
| derivation F-3（接受基準中過時的狀態文字） | 未修改，依 derivation 的建議不改接受基準。只是資訊；現行授權以 OC §5.1 為準（OI-V2-14） |
| derivation F-4（`CONTEXT.md` 未逐名列入 OC §5） | B-6 已判定在 boundary 內；不需決定 |
| derivation F-5 | 已由實作處理（報告無手打數字，`test_report.py` 通過） |
| D-1、D-2、I-1～I-5 | 成立（SIA R1 §2.2、§2.3 H-5、§2.4） |
| H-1～H-5、A-1～A-9（derivation §7） | 各票 R1／R2 與 SIA R1 §2.3 逐類核對，PASS；沒有 deferral（A-7 未觸發） |
| R3-1～R3-3、R3-5（V1 頁尾） | 成立（SIA R1 §2.4：Chrome／Edge 的 computed `display` 與 `textContent` 核對；`explore_ui.js` 不含 `footer`） |
| R3-4 | 說明性裁決，不需證據 |
| R3-6（README 頁面層級陳述） | 成立（SIA R1 §2.4）；報告第 7.1 節與第九章的範圍由 12.5 既有條目限定 |
| R4-1、R4-3、R4-4 | 成立（SIA R1 §2.4：twin 探測，以及測試以外的 c 值下的單位無關性） |
| R4-2 | 頁面上的原因文字（`explore_app.js` `CAUSE_TEXT`）完整屬實。`#ex-lasso-card` 列舉的殘餘問題見 3.7 節與 **OI-V2-5** |
| R4-5、R4-6 | #77 已承接；#78 的 README 與報告由 SIA R2 確認（SIA-F2 resolved） |
| C1-R1～C1-R3、C2-R1～C2-R3、resource-limits §6 的 #78 揭露 | 成立（SIA R1 §2.4 與「交給本 audit 的其他項目」） |
| CF-1、cancel-final-phase §4 的 #78 揭露 | 成立（SIA R1 §2.4） |
| S1-1～S1-6（SIA-F1 決定） | 成立（SIA R2 §2、§3、§5）。S1-7 未採用，沒有 contract change |
| 各票的 non-blocking findings | #74 R1-F2／#76 R1-F1 已解決；#75 R1-F3、R1-F4 已處理；#75 R1-F2 → SIA-F4；#76 R1-F2 → SIA-F5；#77 O-R2-1、O-R2-2 已揭露，O-R2-3 屬 best effort；#78 R1 F1→SIA-F1、F2→SIA-F2、F3→SIA-F3（SIA R1 §7、§8） |
| ACCEPTANCE V2 條目 | V2-1～V2-43 與 G.1／G.2 經 SIA R1 抽核；R2 確認 V2-35、V2-36、V2-37、V2-41 的 rework 註記。下列記 NOT TESTED，沒有 PASS：V2-42（Pages，pending merge）、V2-18 的 Pages 部分，以及 V2-1、V2-8、V2-17、V2-26、V2-39 的 AD-1 best-effort 項目（真實觸控裝置、Firefox、Safari、螢幕閱讀器）（我以 grep 確認） |
| Bindings §5 release gate：README 的執行步驟有變動 | `重跑步驟` 新增探索模式的 `node --test` 指令，pytest 註解也有修改。`worklog/issue-78.md` §6.1 記錄實際執行（88 pass），§10 在 rework 後重跑；我也重跑一次（3.4 節） |

### 3.6 Acceptance boundary 的分配與合起來的覆蓋

- derivation §5.1 把 V2 的整個 acceptance boundary 分配給 Spec V2 rev 2。SIA R1 §3 對 Spec AC S-01～S-35 逐條判定，§3.1 確認涵蓋該分配，沒有缺口或造成歧義的重疊。我同意：G-1～G-5 都有承接（3.5 節），§5.3 列出的項目是 acceptor 的保留動作，以及有明確安排的 Pages item，不是缺口。
- Spec V2 是同一 Outcome Contract 最後一份未結的 Spec。SIA R1 §3.2 核對了全部 derived Specs 合起來的覆蓋：
  - V1 boundary 由 Spec rev 5 承擔：phase accepted，見 [`decision-20261019-phase-acceptance-SPEC.md`](decision-20261019-phase-acceptance-SPEC.md)；V1 AD-3 的 Pages item 由 `audit/20261019-ad3-pages-check-c1-r1.md` closure。
  - V2 boundary 由 Spec V2 承擔。
  - V1 保持要求在整合 subject 上成立（3.3 節）。
  - 唯一未執行的部分是 B-10，與 V1 AD-3 同型；它是 open item，不是分配缺口。
- 我沒有發現需要新的 boundary determination 的疑義：整合 diff 全在單元內；沒有 Spec V2「Out of Scope」的項目（SIA R1 §6）；CC-V2-1 沒有被超出。

### 3.7 `#ex-lasso-card` 的停止原因列舉（R4-2 的殘餘問題）

- **事實**：`index.html` 第 162 行寫「路徑結束時若仍有 group 未進入——active set 退化、路徑走到終點，或數值停止（alpha 回升、迭代達上限）——就停在那裡，上方摘要寫出實際的停止原因」。引擎另有 `multiple_drops`（數值停止）與 `target_constant`（目標在這些列上沒有變化）兩種原因（`assets/explore_engine.js` 第 46–49、1025、1080 行）。後者在引擎中是獨立的原因，不屬「路徑走到終點」。
- **判定**：卡片的操作性陳述屬實，有三點依據：
  - 任何提前結束都套 A-2 的處理；
  - 上方摘要寫出實際原因，而 `CAUSE_TEXT` 對六種原因的文字完整、如實（R4-2 第 1、2 點；SIA R1 §2.4 已在瀏覽器確認）；
  - 讀者不會因此得到錯誤的處理結論。
- **殘餘**：列舉沒有標明「例如」，可能被讀成完整清單，而它缺了兩種原因。所以就 R4-2 第 4 點「`#ex-lasso-card` 的說明必須仍然屬實」而言，這是精確度上的缺口：不記為 PASS，也不作為 phase acceptance 的阻擋。
- **不在本 phase 修正的理由**（沿用 S1-6）：修改會改變 dashboard 位元組，必須重做 OV-1，並依 SIA-F3 重新核對 ZIP。它屬 V2 探索子樹的文字，修改可在 boundary 內進行，但要以一個新的 bounded work item 承擔，依治理 §1.2 須 acceptor 接受（OI-V2-5）。
- 這不是對 S1-6 的改判：S1-6 已明定它不在 rework 範圍，SIA R2 以 R2-O1 記錄同一事實，沒有爭議。

## 4. 是否改變 accepted 語義

**否。** 本紀錄只作 phase acceptance：

- 不修改 Outcome Contract（§1–§5、CC-V2-1）、Brief V2、Spec V2、`tickets-v2.md`、GitHub issues、derivation 或任何 DA 紀錄；
- 不新增或移除 acceptance 條件；
- 不豁免 Spec Integration Audit（它已 closure，本紀錄引用它）；
- B-10 的安排沿用 derivation B-10，以及 acceptor 已接受的 `tickets-v2.md`（與 V1 AD-3 同型），不是 DA 的豁免或 scope 縮減。

不需 acceptor 對本裁決核准。

## 5. Phase acceptance 之後的 open items（都不是 PASS）

依治理 §1.2，下列 follow-up 在 acceptor 接受並授權前只是 tracked items，不得作為新工作執行。

| ID | 項目 | 狀態 | Owner／所需 authority |
| --- | --- | --- | --- |
| **OI-V2-1** | **B-10：GitHub Pages URL 上的檢查**（Brief V2 §8 第 3 條「於 Pages 上」、§3.2、§14 P0；ACCEPTANCE V2-42 與 V2-18 的 Pages 部分記 NOT TESTED（pending merge）；SIA R1 S-19） | Open。合併後的 Lightweight work item（Bindings §4 第 4 列），以 acceptor 的直接指示作為其 Outcome Contract；觸及 H-2、H-5，**須 independent audit**（derivation §7.5）。該 item 結案前，V2 的 acceptance boundary 沒有全部滿足 | **Acceptor**：在 RB-1 合併後下指示；執行者是該 item 的 direct-execution Executor |
| **OI-V2-2** | **SIA-F3**：ZIP 內 dashboard 與 blob 逐位元相同，依賴一個手動換行步驟（`hw2/package.py` 讀工作樹；`.gitattributes` 對 `index.html`、`assets/*.js|css` 沒有 `-text`） | Tracked。目前的 ZIP（`8a51fc1c…8f8d`）符合條件（我核對 17 檔，差異 0）。之後任何重新打包（含合併後、繳交前），都須核對 ZIP 內 `index.html` 與 `assets/` 的 sha256 等於該 commit 的 blob；不符時重做換行步驟 | Orchestrator（寫入 completion report）；重新打包的執行者 |
| **OI-V2-3** | **SIA-F4**：Python 參照的 active-set 退化分支沒有測試覆蓋 | Tracked（測試覆蓋的技術債；不是契約違反） | Orchestrator；新的工作須 acceptor 接受 |
| **OI-V2-4** | **SIA-F5**：控制器丟棄晚到 URL 回應的世代檢查沒有測試偵測；`explore_ui.js` 只有靜態測試 | Tracked（同上） | Orchestrator；新的工作須 acceptor 接受 |
| **OI-V2-5** | **`index.html` `#ex-lasso-card` 的停止原因列舉不完整**（缺 `multiple_drops`、`target_constant`；SIA R2 R2-O1；3.7 節） | Tracked。依 S1-6 不在本 phase 範圍。修改可在 boundary 內進行，但會改變 dashboard 位元組，須重做 OV-1、依 OI-V2-2 核對 ZIP，並需 H-2／H-4／H-5 的 independent audit | Orchestrator（tracked）；新的工作須 acceptor 接受 |
| **OI-V2-6** | **SIA R2 R2-O2**：ACCEPTANCE V2-38、V2-39、V2-40 與 G.2 寫「`f56461b` 打包的 ZIP」，沒有像 V2-37 那樣加新舊 ZIP 的對應註記 | 可選。R2 §6 已判定這些證據對最終 ZIP 成立，該 record 即為對應的紀錄 | Orchestrator（可選，之後整理 ACCEPTANCE 時） |
| **OI-V2-7** | **AD-1 best-effort 項目**：真實觸控裝置、Firefox、Safari、螢幕閱讀器（V2-1、V2-8、V2-17、V2-26、V2-39） | NOT TESTED（無環境），依 AD-1 不是 gate、不得記 PASS。不需 owner 動作，除非取得環境 | — |
| **OI-V2-8** | **Push**：`392e9df..HEAD` 共 40 個 commit 都在本機，`origin` 沒有此 branch | 未執行、未授權（OC §5.1「No push」；designation 第 6 點選項 (a)）。每次 push 前須以 3.3 節的方法對到該次 push 的 tip 重做 S-3／S-5 學號核對 | **Acceptor** |
| **OI-V2-9** | **合併進 `main`（RB-1）** | 未授權：OC §5 沒有 SA-3 opt-in。Bindings §5 的 Formal gates 在本紀錄後成立：全部票結案、SIA closure、DA phase acceptance、README 步驟已實際跑過、沒有追蹤中的機密。這些是合併的**前提，不是授權**。合併前須對合併時的 subject 重做 S-5；若合併後有新的非紀錄 commit，依 orch-default §7 P7 重新核對 | **Acceptor** |
| **OI-V2-10** | **iLearning 繳交（RB-2）**：Submission package（repository URL＋Pages URL＋ZIP） | 未執行。目前 `dist/<學號>_hw2.zip`（sha256 `8a51fc1c…8f8d`，打包 `69f8e07`）是本 phase 的繳交物；它覆寫了先前 V1 的 ZIP（同一路徑）。要繳哪一份由 acceptor 決定。Pages URL 在合併前沒有 V2 內容，所以建議 RB-1 與 OI-V2-1 先於繳交（先後順序是 acceptor 的決定）。任何重新打包適用 OI-V2-2 | **Acceptor** |
| **OI-V2-11** | **GitHub issues #73～#78** 仍是 OPEN（我以 `gh issue list` 確認） | commits 未 push；本 run 的權威結案紀錄是 run record、audit records 與本紀錄。#73 的結案以本紀錄為前提 | **Orchestrator**（控制面），在 acceptor 的 push／merge 決定時同步；`doc/ticket/tickets-v2.md` 的狀態欄同時更新（record-only） |
| **OI-V2-12** | Run terminus 與 completion report | 本紀錄不陳述 | **Orchestrator**：引用本紀錄；四種陳述分列（第 2 節）；列出 OI-V2-1～OI-V2-14 |
| **OI-V2-13** | 向老師確認「兩種 problem」的解讀（Brief V2 §9） | 可選，不是完成條件 | **Acceptor** |
| **OI-V2-14** | derivation F-3：接受基準中 Spec V2 檔頭與 `tickets-v2.md` 的過時狀態文字 | 依 derivation 建議不改接受基準。只是資訊 | **Acceptor**（若要更新，屬 accepted 內容的編輯） |

**已處理、不列為 open**：

- SIA-F1、SIA-F2（README 與報告）：SIA R2 resolved。
- 各票已解決的 non-blocking findings（3.5 節）。
- #77 O-R2-1、O-R2-2：已在 README 與報告揭露。
- #75、#76、#78 回報的程序副作用（以映像名稱停止 Chrome、以預設 profile 開啟 Chrome、殘留 Edge 程序）：已由 Orchestrator 告知 acceptor，之後的派工 pack 已加入操作規則（run record 第 7、11、20 列），對 repo 沒有影響。

## 6. 受影響的 work items

| 對象 | 影響 |
| --- | --- |
| #73（Spec V2 rev 2） | Phase accepted；可由 Orchestrator 結案（OI-V2-11） |
| #74～#78 | 無變更；已結案（run record） |
| Run `run-20261022-hw2-v2-enhance` | Phase acceptance 完成；terminus 由 Orchestrator 判定（OI-V2-12） |
| 合併後的 Pages Lightweight item（B-10） | 尚未建立；OI-V2-1 |
| Outcome Contract、Brief、Spec、Tickets、GitHub issues、程式、測試、ACCEPTANCE、報告、README、V1 產物 | 本紀錄不修改 |

## 7. Evidence

- **讀取**：
  - Bindings b5 全文；治理 v2.2 §1.1–§1.5、§2.1、§2.4、§2.5、§3.1、§3.3–§3.8、§4.1–§4.7、§5.1–§5.4；
  - `outcome-contract.md` 全文（§5、§5.1、§5.2）；
  - `derivation-SPEC-V2.md` 全文；`decision-20261022-r1f3-v1-footer.md` §3–§5；`decision-20261022-issue75-lasso-early-stop.md` §4–§6；`decision-20261022-issue77-resource-limits.md` §6–§7；`decision-20261022-issue77-cancel-final-phase.md` §4；`decision-20261022-sia-f1-dashboard-wording.md` 全文；`decision-20261019-phase-acceptance-SPEC.md` 全文（V1 先例）；
  - `audit/spec-SPEC-V2-c1-r1.md` 全文、`audit/spec-SPEC-V2-c1-r2.md` 全文；`audit/issue-74..78-*` 的 verdict 行；
  - `worklog/issue-74..78.md` 的 §8，`worklog/issue-78.md` §10；
  - run record 全文；
  - ACCEPTANCE G 節的 NOT TESTED 條目；`index.html` 第 158–162 行；`assets/explore_engine.js` 第 38–62 行；`assets/explore_app.js` 第 89–94 行；README 的章節與 `d7f02d4..HEAD` diff。
- **Git（只讀）**：`git rev-parse HEAD main origin/main`；`git ls-remote --heads origin home_work_02-v2-enhance`；`git diff --name-only／--name-status／--stat／--numstat／--quiet`（`d7f02d4`、`3745e9c`、`69f8e07`、`17f10a7`、HEAD）；`git log --oneline --name-only 3745e9c..HEAD`；`git show <rev>:<path> | sha256sum`；`git status --porcelain`；`git rev-list --count`。
- **GitHub**：`gh issue view 74..78 --json body`（sha256）；`gh issue list`（#73～#78 狀態）。
- **測試**：pytest 478 passed；Node 六檔 88 pass；`hw2.offline_scan` PASS。
- **Scratchpad 外的只讀 Python**（`python -I`，不印出學號）：ZIP sha256、manifest、`testzip()`、dashboard 17 檔與 `69f8e07` blob 的比對、ZIP 內容與 `392e9df..HEAD` 每個 commit 的樹、訊息與 patch 的學號比對。
- **Transcript**：以 Bindings §3.6 的方法掃描本 session 全部 subagent 與 root session（root `('claude-opus-5-5','medium')` 273 則）；SIA 與 ticket reviewer 的 Write 內容與 committed record 的比對。
- 沒有啟動瀏覽器；沒有執行 notebook、`hw2.package` 或任何會開啟 test 守門或改寫 `dist/` 的程式。寫入的檔案只有本紀錄；沒有 commit、push 或任何 git 寫入。

## 8. Required authority

- 本裁決不需要其他 authority，也不需要 capability escalation。
- 第 5 節由 acceptor 負責的項目都是既有的 reserved boundaries 或 acceptor 自己的決定，不是本紀錄新增的 gate：
  - OI-V2-1 的啟動；
  - OI-V2-8 push；
  - OI-V2-9 RB-1；
  - OI-V2-10 RB-2；
  - OI-V2-13、OI-V2-14；
  - OI-V2-3～OI-V2-5 成為新工作時的接受。
