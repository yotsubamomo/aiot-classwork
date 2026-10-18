# Audit record — Issue #65，cycle 1，R2

| 欄位 | 內容 |
| --- | --- |
| Work Contract | 與 R1 相同：GitHub issue #65（高風險 H-2、H-4）；Spec rev 5（#59）；DA `derivation-SPEC.md` 與 R1 record 列出的 DA 紀錄；Outcome Contract（Brief @ `dff7c55c`＋CC-1、AD-1～AD-3）。本輪的依據是 R1 record `doc/governance/audit/issue-65-c1-r1.md`（`6025c32`）的 F-1（blocking）與其 R2 closure 條件 (a)～(d) |
| 受審 subject | branch `home_work_02-regrill`，**修正後的 implementation commit `99303c31ef5f19f9c34c562a2c2233bcfddec064`**（parent `6025c32`）。R1 subject＝`0b57c02`；`0b57c02..99303c3` 之間的 `a0a1b70`、`0c46bf3`、`6025c32` 只改 `doc/governance/**`（record-only）。之後的 `743441e` 只改 worklog。審查時 HEAD＝`743441e`；`git diff --stat 99303c3 HEAD -- . ':!home_work_02/doc/governance'` 為空；`git status --porcelain home_work_02` 審查前後皆為空。`99303c3` 沒有 push |
| Audit 種類 | **R2**（closure review），**cycle 1**。只核對 R1 blocking finding 是否解決、修正是否引入回歸、修正是否直接產生或暴露新的 blocking defect（治理 §4.4）。不是 Spec Integration Audit |
| 角色 | `primary_reviewer`（definition `gov-primary-reviewer`；`claude-opus-5-5`／`xhigh`） |
| Assurance (a)：context independence（治理 §2.3；Bindings §3.7） | (1) 本 R2 延續我自己的 R1 context（同一個 subagent 被續派；治理 §2.3 第 1 項、Bindings §3.7 第 1 項允許），不繼承 Executor 的 context；修正後的檔案與 diff 都從磁碟重新讀取，worklog §10 的敘述只當作待驗證主張。(2) Binding：見 (b) 欄。(3) Autonomous access：自行讀取 `git diff 0b57c02 99303c3`、修正後的 `report/report.md`、`README.md`、`tests/test_report.py`，自行執行完整 pytest、Node test、離線掃描、報告建置、數字交叉核對、預測圖重產、mutation probes 與 A-4 掃描。(4) Self-written record：本檔由 Reviewer 以自己的 Write 工具寫入 |
| Assurance (b)：model diversity（Bindings §5） | **Executor**：agentId `a4779b376d79e3353`，`gov-executor`，Reviewer 自行掃描 subagent transcript：`('claude-opus-5-5', 'high')` 304 則、單一元素（O-1）。**本 review**：agentId `a3ff011d2766ef922`，`gov-primary-reviewer`，撰寫本 record 前觀測 `('claude-opus-5-5', 'xhigh')` 251 則、單一元素；全程核對由派工者依 Bindings §3.6 執行。**無 model diversity**（同為 `claude-opus-5-5`）。Bindings §5 不宣告 diversity 關係（A-8） |
| 日期 | 2026-10-19 |

## 1. 修正的範圍（自行讀取 diff）

`git diff --stat 0b57c02 99303c3 -- . ':!home_work_02/doc/governance'`：只有三個檔案。

- `report/report.md`（+6／−4）：
  - 第六章（`## 6. Evaluation 〔老師要求〕`）在補充段引文之前加一句出處說明：「作業頁正文要求模型評估與加上區間的預測圖（見前面的標示對照表與第 6.3 節）。下面這句出自作業頁的「補充」段，是對這一階段的**建議**，不是作業頁正文的要求；本專案採用的部分是第 6.2 節的 Adjusted R² 與第 6.4 節的五大回歸假設診斷，都標〔依老師補充建議〕：」。
  - 第七章（`## 7. Deployment 〔老師要求〕`）同型：「作業頁正文要求的是 CRISP-DM 的 Deployment 階段。下面這句出自作業頁的「補充」段，是對這一階段的**建議**，不是作業頁正文的要求；本專案採用它，見第 7.2 節與第 7.3 節，都標〔依老師補充建議〕：」。
  - §6.2 標題改為「訓練 CV 與 Test 的比較 〔老師要求；Adjusted R² 為依老師補充建議〕」；該節兩處 Adjusted R² 的陳述（段落與條列）各加〔依老師補充建議〕。
- `README.md`（1 行）：目的段改為「依作業要求執行特徵選擇：比較四種……（方法取自作業頁「補充」段建議清單的一部分）……」（R1 F-3）。
- `tests/test_report.py`（+64）：10 個新測試（R1 F-2）——§5.2、§6.4、§7.2、§7.3 標題帶〔依老師補充建議〕且不帶〔老師要求〕；§6.2 標題與每一行 Adjusted R² 陳述帶補充建議標示；§7.1、§9 標題帶「課堂口頭」；每段 `quote:src2t` 引文在〔依老師補充建議〕標題之下或緊接在指明補充段為出處的句子之後；`quote:src1` 引文前不以「補充」為出處；README 目的段不把方法比較寫成作業要求。

新文字的事實核對：作業頁正文確實要求「模型評估」與「預測圖(加上信賴區間或預測區間)」（SRC-1 第 28–29 行）以及 CRISP-DM 的 Deployment 階段（第 36 行）；兩段引文確實在 SRC-2T 的「補充」段（第 81 行之後的第 145、146 行）；「本專案採用的部分」與報告前段對照表（Adjusted R²、五大假設、Deployment 的預測新樣本與模型解釋為〔依老師補充建議〕）一致。

## 2. F-1 的 R2 closure 條件

| 條件（R1 record F-1） | 判定 | 證據 |
| --- | --- | --- |
| (a) 渲染後的報告中，第六、七章與其他任何〔老師要求〕章節開頭沒有未註明出處的補充段引文 | **成立** | 重新建置（scratchpad `r65/build2/`）後逐一檢查渲染 Markdown 中全部 10 段引文與其前一行：補充段引文 5 段——§1.2（「作業頁的「補充」段寫：」）、§5.1（「老師的補充段建議比較下列方法：」）、§5.2（〔依老師補充建議〕標題下）、第六章（新的出處說明，渲染第 193–195 行）、第七章（新的出處說明，第 315–317 行）；正文引文 5 段（§1.2、§1.4、§6.3、§8、§10）都在〔老師要求〕或「作業頁正文寫：」之下。PDF 文字（`pdftotext`）第 268–271 行與第 581–583 行同樣是「6. Evaluation 老師要求」→ 出處說明 → 引文、「7. Deployment 老師要求」→ 出處說明 → 引文 |
| (b) §6.2 的 Adjusted R² 帶〔依老師補充建議〕 | **成立** | 渲染第 203 行「### 6.2 訓練 CV 與 Test 的比較 〔老師要求；Adjusted R² 為依老師補充建議〕」、第 205 行「〔依老師補充建議〕Adjusted R² 只對 OLS 子集模型……」、第 227 行「- 〔依老師補充建議〕Adjusted R²（log 尺度）……」。比較表的 Adjusted R² 欄在同一節（標題已標示） |
| (c) 其他標示、數字、圖與 `results/`、`assets/`、notebook 不變；delta 只有報告來源與選擇加入的測試 | **成立** | delta 只有 `report/report.md`、`tests/test_report.py`，以及 R1 record 建議併入的 F-3 README 一句；`git diff --quiet 0b57c02 99303c3 -- results assets index.html hw2.ipynb hw2 requirements.txt doc/acceptance report/external_sources.json report/chrome_capture.js` 成立。報告其他標題與標示的 diff 只有 §6.2 一處 |
| (d) 完整 pytest 通過、報告可建置 | **成立** | `.venv/Scripts/python -m pytest -q -rs -p no:cacheprovider`（工作樹＝`99303c3`）→ **348 passed、1 skipped**（skip＝學號設定未提供），48.8 s。Worklog VR-1 的全量執行在最後一次措辭修改之前，所以我以最終狀態重新執行。`python -m hw2.report --out <scratchpad>` → 成功，PDF 26 頁（多兩段文字），`external_requests: []`，建置仍先執行正式評估的 digest 核對 |

**F-1：已解決。**

## 3. 回歸核對

- **結果與評估完整性（H-3）**：`results/model_data.json`、`assets/model_data.js`、`results/` 全部、notebook、`hw2/` 與 `0b57c02` 相同（第 2 節 (c)）；`export.result_digest`＝`b53ff286ae0734add8b272089aba904a1cb7f5aca444a62d356420b25dc3cfc6`；預測圖由追蹤的 `model_data` 在獨立 process 重產，sha256 仍為 `8afdb90b…a4bc4a39`（與追蹤檔相同）。沒有執行 notebook、沒有開啟守門、沒有評估任何 test 列。
- **數字單一來源**：以 R1 的獨立交叉核對腳本（`xcheck.py`、`xcheck_comp.py`）核對新建置的報告與修正後的 README：**350 項，0 項不符**。模板「沒有手抄數字」的測試通過；新文字只含章節編號（第 6.2、6.3、6.4、7.2、7.3 節），屬測試允許的結構性引用。
- **其他測試與檢查**：`node --test tests/js/core.test.js` → 9 pass、0 fail、3 skip（正式逐筆重算通過）；`python -m hw2.offline_scan` → PASS（0 findings）。
- **Mutation probes（R2 自行重做；`git -c core.autocrlf=false archive 99303c3` 的 scratchpad 複本；`tests/test_report.py` 基準 26 passed，跑完後仍 26 passed）**：R1 存活的 L1～L6（§6.4、§7.3、§5.2 的標示改成〔老師要求〕，§9、§7.1 刪除「課堂口頭」，§1.2 的補充段出處改成正文）現在**全部 DETECTED**；另外針對本次修正的 7 個 mutant 也全部 DETECTED：刪除第六章出處說明、刪除第七章出處說明、把第六章出處改寫成「出自作業頁正文」、刪除 §6.2 標題標示、刪除 §6.2 條列標示、刪除 §6.2 段落標示、README 目的段還原。**13／13 DETECTED。** 新測試的強度足以守住 F-1 的修正。
- **標示的一致性**：新的出處說明本身沒有把任何補充建議寫成老師要求（明寫「不是作業頁正文的要求」）；§6.2 標題的複合標示與既有的 §6.3「〔老師要求；涵蓋率驗證為專案延伸〕」同型，由 `hw2/report.py` 的標示 regex 渲染為〔老師要求〕標籤加說明文字。L-1～L-3（dashboard 的「課堂口頭」）不受影響，並由新測試守住。
- **H-1（A-4，S-1 替代證據；重述）**：`0b57c02..HEAD` 新增的 337 行中「學號」16 次：1 次 `<學號>`、15 次敘述用詞，沒有一次後面接 7 位以上數字；7 位以上數字串只有日期、sha／digest 片段與 ASSET 頁碼（R1 record 中的引用），沒有未分類者；5 個 commit message 只有紀錄檔名中的日期。delta 沒有新增 PDF、ZIP、`.env`、`kaggle`、`acceptor_materials/`、`.local/`、`dist/`。實際學號比對 **NOT VERIFIED**（依 S-1）。
- **Git**：`99303c3` 的訊息依 `docs/conventions/git-commit-rules.md`（`[Modify] –` 開頭，`[Fix]`／`[Additions]` 分類），沒有 Claude 標記；未 push。

**沒有發現修正引入的回歸，也沒有修正直接產生或暴露的 blocking defect。**

## 4. 高風險類別（A-1；重述修正結果）

| 類別 | R2 結果 |
| --- | --- |
| H-1 | 第 3 節：PASS（實際學號比對 NOT VERIFIED，S-1） |
| H-2 | 報告章節名稱與順序不變；「GPT 輔助內容」「NotebookLM 摘要」標題不變；預測圖、dashboard、notebook 不變；README 只改目的段一句。PASS |
| H-3 | 正式產物、digest、預測圖不變；數字交叉核對 0 不符。PASS |
| H-4 | 三種標示：F-1 已解決（第 2 節），章節層級標示與補充段出處由新測試守住（F-2 的處理，13／13 mutant 被偵測）；README 措辭已修正（F-3）。外部來源、mock／wireframe、待填位置、ACCEPTANCE 狀態都不在 delta 中，維持 R1 的結果。PASS |

## 5. R1 findings 的狀態

| Finding | R1 判定 | R2 狀態 |
| --- | --- | --- |
| F-1 | Medium，blocking | **已解決**（第 2 節） |
| F-2 | Low，non-blocking，owner #65（未完成則 #66） | 已在本次修正處理（10 個新測試；L1～L6 被偵測）。不是 R2 closure 條件，記錄於此 |
| F-3 | Low，non-blocking，可併入 F-1 修正，否則 #67 | 已在本次修正處理（`README.md:8`；有測試）。不是 R2 closure 條件，記錄於此 |
| F-4 | Low，non-blocking，owner #67；修正前須 route Design Authority | 未處理（依 R1 disposition 與派工指示，正確）；仍 open，owner **#67**，required authority＝**Design Authority**（動到凍結的 cell 0–45 之前） |

## 6. 新的 findings

無。

## 7. 結論

- F-1 的四項 R2 closure 條件全部成立；修正沒有引入回歸，也沒有產生或暴露新的 blocking defect。
- F-2、F-3 已一併處理；F-4 維持 open（owner #67，修正前須 route Design Authority）。
- 正式 Test 評估沒有被再執行；`model_data` 與 `result_digest` `b53ff286…` 不變。
- A-4 學號：NOT VERIFIED（S-1），不是本票結案的條件；S-2～S-5 仍 open。

VERDICT: CLOSURE
