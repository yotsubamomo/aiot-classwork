# Audit record — Spec V2 rev 2（#73）的 Spec Integration Audit，cycle 1，R2

- **Work Contract**：與 R1 相同（[`spec-SPEC-V2-c1-r1.md`](spec-SPEC-V2-c1-r1.md) 檔頭：Outcome Contract §5、§5.1、§5.2 CC-V2-1 與仍有效的 §1–§4；Spec V2 rev 2；Brief V2 rev 2＋E-1；`tickets-v2.md`；#74–#78；`derivation-SPEC-V2.md` 與 V2 的 DA decisions）。本 R2 的範圍依 Design Authority 紀錄 **[`../decisions/decision-20261022-sia-f1-dashboard-wording.md`](../decisions/decision-20261022-sia-f1-dashboard-wording.md)**（committed `cec4c93`；S1-1～S1-7，特別是 S1-2 的 C-1～C-4 與形式限制、S1-3、S1-4、S1-5、S1-6）。我自行讀取該紀錄全文。
- **受審 subject**：branch `home_work_02-v2-enhance`。
  - 實作 commit **`69f8e0794ec0fb5b4f1fcda7a1f62bc74912a89d`**（只改 `README.md`、`report/report.md`）；
  - 紀錄與證據 commit **`17f10a7c1626bd334bee82c93202822d0e9f6976`**（`doc/acceptance/ACCEPTANCE.md`、`doc/screenshots/v2-issue78/zip_manifest_rework_69f8e07.txt`、`doc/governance/worklog/issue-78.md` §10）。
  - **新的最終整合 subject（供 phase acceptance 引用）：`17f10a7c1626bd334bee82c93202822d0e9f6976`**。`doc/acceptance/` 與 `doc/screenshots/` 不是 Bindings §7 的 record-only paths，所以最終 subject 取 `17f10a7`，不是 `69f8e07`；兩者之間的 diff 只有上列三個檔案，程式、頁面、測試與交付文件在兩者相同。
  - 相對 R1 subject 的 delta：`git diff 3745e9c 17f10a7`。其中 `3750de4`（R1 record 與 run record）與 `cec4c93`（DA 紀錄與 run record）只動 `doc/governance/**`。審查時 HEAD＝`17f10a7`，工作樹只有 Orchestrator 未 commit 的 run record（record-only）；`git diff --quiet 17f10a7 -- README.md report index.html assets hw2 tests` 成立，所以我在主 checkout 執行的測試就是 subject 的內容。
  - 未追蹤的繳交 ZIP `dist/<學號>_hw2.zip`（sha256 `8a51fc1c…8f8d`，打包 commit `69f8e07`）一併受審。
- **Audit 種類**：Formal 的 Spec Integration Audit，**同一 instance、cycle 1 的 R2**（治理 §4.4、§4.7；DA S1-5）。不是新的 cycle，也不是任何 Ticket audit 的 R3。依治理 §4.4，R2 只核對：R1 的待處理 finding 是否真正解決（SIA-F1；依 S1-6 一併處理的 SIA-F2）、修正有沒有引入回歸、修正有沒有直接產生或暴露 blocking defect；不是第二次全面審查。
- **角色**：`primary_reviewer`（`gov-primary-reviewer`），有效 mapping `claude-opus-5-5`／`xhigh`（R-PR），沒有 escalation、沒有替代。
- **Binding（觀測）**：agentId **`aa43e1e2fb1e18487`**（`agentType` `gov-primary-reviewer`；R1 的同一 assignment，依 Bindings §3.7 以 SendMessage 續派）。寫入本 record 前以 Bindings §3.6 的方法掃描本 transcript 全部 assistant 訊息（R1＋R2）：`('claude-opus-5-5', 'xhigh')` **270 則，單一元素**。Return 前的全程核對由派工者執行。
- **R1 record 的完整性**：`audit/spec-SPEC-V2-c1-r1.md` 在磁碟上與 `3750de4` 的 committed 版本相同（`git diff --quiet 3750de4`），最後一行 `VERDICT: CLOSURE`；本 R2 不改寫它。

## 0. Assurance（Bindings §5 兩欄）

### (a) Context independence（治理 §2.3；Bindings §3.7）

| Property | 滿足方式 |
| --- | --- |
| 1 Independent context | R2 依治理 §2.3 第 1 項與 Bindings §3.7 延續我自己的 R1 context，不繼承 Executor（agentId `acc8906c845bfc14f`）、Orchestrator 或 Design Authority 的對話。我從磁碟與 git 重讀修正後的檔案與 diff（`git diff 3745e9c 17f10a7`）、DA 紀錄、ACCEPTANCE 的變更與 worklog §10；其中的敘述（「12.5 採 DA 參考文字」「只有 PDF 與 README 不同」「17 檔不需改寫」「學號 0 命中」等）都當作待驗證主張，以我自己的檢查驗證（§2–§6）。 |
| 2 Verifiable binding | 檔頭的 transcript 觀測。 |
| 3 Autonomous access | 自行讀取 repo 與 git（不做 git 寫入）、未追蹤的 ZIP、`dist/` 的打包 manifest 與建置後的報告、作業頁原文 SRC-4；自己執行 pytest、Node、`offline_scan`、報告渲染、PDF 文字抽取、ZIP 核對、學號比對，並以自己啟動的 headless Chrome（全新 scratchpad profile）對新 ZIP 的 dashboard 做離線檢查。 |
| 4 Self-written record | 本檔由我以自己的 Write 工具寫入 `home_work_02/doc/governance/audit/spec-SPEC-V2-c1-r2.md`；沒有 commit，沒有修改任何追蹤中的檔案。 |

### (b) Model diversity（治理 §4.6；Bindings §5）

| Assignment | 實際 model（我自行掃描 transcript） |
| --- | --- |
| Executor #78（含本次 rework），agentId `acc8906c845bfc14f`（`gov-executor`） | `claude-opus-5-5`／`high`，248 則，單一元素 |
| Design Authority（SIA-F1 紀錄），agentId `a67436700d54c6ca4` | `claude-opus-5-5`／`high`，61 則，單一元素 |
| Primary Reviewer（本 SIA R1＋R2），agentId `aa43e1e2fb1e18487` | `claude-opus-5-5`／`xhigh`，270 則，單一元素 |

**無 model diversity**。Bindings §5 不宣告 diversity 關係；independence 由 (a) 判定。

## 1. 修正的範圍（重讀 diff）

- `git diff --name-only 3745e9c 17f10a7` 中非 `doc/governance/` 的路徑只有 `README.md`、`report/report.md`、`doc/acceptance/ACCEPTANCE.md`、`doc/screenshots/v2-issue78/zip_manifest_rework_69f8e07.txt`——正是 DA S1-5 第 2 點允許的集合（S1-6 採用時含 `README.md`）。沒有 `home_work_02/` 以外的路徑，沒有 `doc/requirement/`（RB-5）。
- `report/report.md`：+2／−1 行，都在第 12 章內：12.3「Lasso 路徑的停止」段落改寫一行（SIA-F2）；12.5 在既有兩條之前新增一條（SIA-F1）。
- `README.md`：+1／−1 行，只有「探索模式（加分功能）」的「Lasso 路徑的停止」條目（SIA-F2）。
- `index.html`、`assets/`、`hw2/`、`tests/`、`results/`、`hw2.ipynb`、`data/`、建置與打包程式（`hw2/report.py`、`package.py`、`pdf_append.py`、`report/` 其他檔）、`doc/spec`、`doc/brief`、`doc/ticket`、`CONTEXT.md`、`.gitignore`、`.gitattributes`、`requirements.txt`：`git diff --stat 3745e9c 17f10a7` 為空。

## 2. 範圍 1：SIA-F1 是否依 DA 紀錄解決

新條目（`report/report.md` 第 393 行，12.5 的第一條）與 DA S1-2 的參考文字逐字相同。逐項核對：

| 要求 | 核對 | 結果 |
| --- | --- | --- |
| **C-1** 範圍 | 「前面各章（標示說明與對照表、第一章到第十一章與附錄）引用或描述的作業頁內容，依的是撰寫正式分析時的舊版作業頁；為了讓正式分析的內容不變，這些引用與標示保留原文。」 | 符合 |
| **C-2 (a)** | 「標示說明與對照表、第 7.1 節與第九章的「課堂口頭」標示與「作業頁正文沒有要求網站」只描述舊版作業頁」 | 符合 |
| **C-2 (b)** | 引用「跟 DIC2 一樣github and web」——與 SRC-4 第 37、44 行「主要繳交:   跟 DIC2 一樣github and web」的字串相同，也與 README 第 24 行相同 | 符合 |
| **C-2 (c)** | 「本專案的 web 交付就是 GitHub Pages 上的這個 dashboard，所以 GitHub repository 與這個 dashboard 現在是作業頁正文列出的主要繳交」——web＝Pages 上的 dashboard 以「本專案」為主詞，寫成本專案的對應，不是老師原文 | 符合 |
| **C-2 (d)** | 「dashboard 的標示類別仍是老師要求，改變的只是來源」 | 符合 |
| **C-3** | 「特徵數條件改為 `>13` 個特徵；第 1.2 節的交集條件依舊版作業頁，King County 的 source feature 數也符合新條件」——不寫特徵數；與 SRC-4 第 16 行「>13 個特徵」相符；King County 19 個 source features 確實符合 | 符合 |
| **C-4** | 「舊版的「補充」段在更新後的作業頁沒有載明，本報告不推定老師已刪除它」；沒有提評分標準（DA 允許不提） | 符合 |
| 形式：無手打數字 | 日期未以數字出現（用「更新後的作業頁（SRC-4）」）；`>13` 在 code span；「第一章到第十一章」「一是」「二是」用中文數字；只有 `SRC-4`、`DIC2`、`第 7.1 節`、`第 1.2 節` 這類不命中的形式。`tests/test_report.py` 的手打數字檢查在全部 pytest 中通過 | 符合 |
| 形式：無新 placeholder | 我以 regex 抽取第 12 章的 placeholder：只有 `{{k_range}}` | 符合 |
| 形式：12.5 既有兩條保留、「第 7.1 節與第九章」仍在 | 第 394、395 行與 R1 subject 相同 | 符合 |
| 形式：不提「講義」 | 新條目不含「講義」 | 符合 |
| 形式：不超出 SRC-4 原文 | 沒有「新版作業頁要求了 dashboard 的某項功能」這類說法；對 SRC-4 只陳述主要繳交字串與「>13」 | 符合 |
| S1-3 必須不變 | 我的比對：`69f8e07` 的模板去掉第 12 章後與 `d7f02d4` 的模板**逐字相同**；第 12 章相對 R1 subject 只有上列兩行改變（12.3 一行、12.5 新增一行），標題、標示、開頭兩段、標示表與 12.1～12.4 其餘不變；`tests/test_report.py`、`tests/test_explore_docs.py` 與其他測試自 `3745e9c` 無 diff | 符合 |
| H-4、A-5(V2)：陳述與 SRC-4、Brief V2 §2／§3.5 相符 | 依 Brief V2 §2（SRC-4 為正式需求、SRC-1／SRC-2T 為歷史來源、未載明不得推定刪除）與 §3.5 覆寫 1、4，陳述屬實；與 README 第 24、84 行一致 | 符合 |
| 交付形式（S1-4） | 新 ZIP 的 `hw2_report.pdf`（sha256 `ba56dc5b…f9fe`，152 頁）以 `pypdf` 抽取文字並以 NFKC 正規化（PDF 字型把部分漢字對到康熙部首碼位）：12.5 新條目全文都在（「撰寫正式分析時的舊版作業頁」「跟 DIC2 一樣github and web」「本專案的 web 交付就是 GitHub Pages 上的這個 dashboard」「dashboard 的標示類別仍是老師要求」「第 1.2 節的交集條件依舊版作業頁」「不推定老師已刪除它」各 1 次）；ZIP 內的 PDF 與 `dist/report/hw2_report.pdf` 逐位元相同；`dist/report/hw2_report.md` 與我以 `hw2.report.render_markdown()` 渲染 `69f8e07` 模板的結果**逐字相同**，pending placeholder 0；以同一函式渲染 `d7f02d4` 模板，兩者在第 12 章以外逐字相同 | 符合 |

**結論：SIA-F1 已依 DA 紀錄解決（resolved）。**

## 3. 範圍 2：SIA-F2 是否依 S1-6 解決（`index.html` 不在範圍）

| 要求（S1-6） | 核對 | 結果 |
| --- | --- | --- |
| README 與報告 12.3 一致地修改，兩處都只改兩點 | 兩處的 diff 各只有兩個片段改變：停止原因的列舉加入「同一步有多個 group 同時離開路徑」「預測目標在這些列上沒有變化」；尺度由「目標除以它在同一批列上的均方根」改為「目標在同一批列上置中後除以其均方根」。其餘文字逐字不變；兩處用詞一致 | 符合 |
| 與實作一致 | `assets/explore_engine.js` 檔頭：`multiple_drops`、`target_constant` 是停止原因，尺度是「target … centred and divided by its root mean square on the same rows」；`explore_app.js` 的原因文字「同一步有多個欄同時離開路徑」「預測目標在這些列上沒有變化」；`index.html` `#ex-lasso-card`「目標在同一批列上置中並除以其均方根」。我在 R1 對引擎驗證過這些原因與單位無關性（R1 §2.4） | 符合 |
| 不改 `index.html` 與 `assets/` | `git diff --stat 3745e9c 17f10a7 -- index.html assets` 為空 | 符合 |
| `test_exploratory_limits_are_disclosed` 要求的字樣保留 | 「均方根」「不改變進入順序、停止點與候選狀態」「實際的停止原因」都還在；該測試在全部 pytest 中通過 | 符合 |
| PDF | NFKC 正規化後，新的兩個原因與「目標在同一批列上置中後除以其均方根」在 PDF 各出現 1 次；舊字串「目標除以它在同一批列上的均方根」0 次 | 符合 |

**結論：SIA-F2（README 與報告的部分）已解決（resolved）。** `index.html` `#ex-lasso-card` 的列舉仍不完整（「active set 退化、路徑走到終點，或數值停止（alpha 回升、迭代達上限）」），DA S1-6 明定不在本次範圍（改它會動到 dashboard 位元組與 OV-1 證據）；頁面上方摘要與候選原因寫出實際的停止原因（`explore_app.js` 的原因文字完整）。這是既有的狀態，不是修正造成的，記為 §7 的觀察 R2-O1。

## 4. 範圍 3：回歸

| 項目 | 方法 | 結果 |
| --- | --- | --- |
| 全部 pytest | `.venv/Scripts/python -m pytest -q -rs -p no:cacheprovider`（工作樹＝`17f10a7` 的程式、文件與測試） | **478 passed、0 skipped**（110 s） |
| Node | `node --test tests/js/explore_{load,boundary,app,methods,custom,run}.test.js`（v24.19.0） | **88 pass、0 fail、0 skipped、0 cancelled** |
| 靜態掃描 | `python -m hw2.offline_scan`；新 ZIP 的 dashboard 副本 `offline_scan.scan()` | 13 files、0 findings；0 findings |
| 正式章節凍結（#78 AC、I-5） | 模板與渲染兩層的比對（§2）；`tests/test_explore_docs.py::test_every_other_part_of_the_report_is_the_accepted_baseline` 通過 | 第 12 章以外逐字等於接受基準 |
| 測試未改 | `git diff --stat 3745e9c 17f10a7 -- tests` | 空 |
| 正式分析與 V1 不變量（DA A-3） | `git show 69f8e07:<path> \| sha256sum` | `app.js` `c1ab3f21…`、`hw2core.js` `e75c5d48…`、`model_data.js` `6cf0c11e…`、`results/model_data.json` `69dc1465…`、`style.css` `60a27016…` 與 R1 相同；`results/`、`hw2.ipynb`、`hw2/` 無 diff；打包 manifest 的 `result_digest` 仍是 `b53ff286…`（沒有重跑 notebook、沒有新的 Test evaluation） |
| A-4 學號 | 比對值只在記憶體中讀自 `.local/packaging.json`，不印出 | `git grep -F`：`17f10a7` 的樹 0、`HEAD` 的樹 0、工作樹追蹤檔 0；`d7f02d4..HEAD` 38 個 commit 每個的樹 0；commit message 0；`3745e9c..HEAD` 的 patch 0；新清單 `zip_manifest_rework_69f8e07.txt` 以 `<學號>` 記名；新 ZIP 67 個項目的內容 0（檔名與頂層資料夾依老師規則含學號，屬未追蹤的繳交物）；`home_work_02/` 沒有未追蹤的非忽略檔案 |
| 作者材料 | 新 ZIP 的 `ChatGPT_logs.pdf` 與 notebook 項目與舊清單相同（`0a5d29e3…`、`2e2f8afc…`） | 不變 |

## 5. 範圍 4：ZIP（SIA-F3、A-6、H-1）

我自己的核對（`python -I`，只讀 repo 與 `dist/`）：

- `dist/<學號>_hw2.zip`：檔名規則與頂層資料夾 `<學號>_hw2` 與 V1 相同；sha256 **`8a51fc1ca26d176f3edb075f7f8aeda7a0dc659531484c10e695bc3800d08f8d`**，81,624,097 bytes，等於 `dist/hw2_package_manifest.json`（`commit` `69f8e07`、`result_digest` `b53ff286…`）與 ACCEPTANCE V2-41；`testzip()` 無錯；67 個項目，與 `zip_manifest_rework_69f8e07.txt` 逐項 size／sha256 相同，沒有缺漏。
- **SIA-F3**：ZIP 內 `index.html` 與 `assets/` 共 17 個檔，與 `69f8e07` 的 blob **逐位元相同**（也就是合併後 Pages 會提供的位元組）。工作樹中這些檔目前是 `i/lf w/lf`。
- **與已驗證的舊 ZIP 逐項比對**：舊 ZIP（sha256 `57e1e4a4…bcd11`）已被覆寫；我在 R1 已核對它與 `doc/screenshots/v2-issue78/zip_manifest.txt` 逐項 size／sha256 相同，所以以該清單代表舊 ZIP。新舊項目名稱與順序完全相同，沒有新增或刪除；**sha256 不同的只有 `hw2_report.pdf` 與 `README.md`**。
- ZIP 內 `README.md` 等於 `69f8e07` 的 blob 經 CRLF→LF 後的位元組（與 V1 起其他追蹤文字檔的打包方式相同）。
- **README 在 ZIP 內改變是否要緊（Executor 提出）**：不要緊。DA S1-4 第 3 點「預期只有 PDF 改變」是在 S1-3「`README.md`（S1-6 例外）不改」的前提下寫的；Orchestrator 採用了 S1-6，README 的修改經既有打包流程（以 `git ls-files` 決定項目）進入 ZIP 是必然結果，S1-3 本身也把 README 列為 S1-6 的例外。ZIP 的 README 正是 subject 的 README（CRLF→LF 等同 blob），內容只有 SIA-F2 的那一處；它不是 dashboard 頁面載入的資源，不影響 dashboard 位元組或 OV-1／SR-09 證據。這個差異已如實記在 ACCEPTANCE V2-41 與 worklog §10。

## 6. 範圍 5：舊 ZIP 上的 OV-1／SR-09 瀏覽器證據能否延用（由我判定）

**判定：可以延用。** 理由與證據：

1. OV-1（V2-37）與 SR-09（V2-38）以及 OV-2～OV-5（V2-39）、效能（V2-40）、G.2 的量測，檢查的都是解壓後以 `file://` 開啟的 dashboard。頁面只讀取 `index.html` 與本機的 `assets/` 資源（R1 時我觀察到非 `file:`／`data:` 請求 0、只讀本機資源；V2-37 記錄 `index.html` 與 12 個本機資源）。
2. 這些檔案在新舊 ZIP 之間逐位元相同（§5），也等於 `69f8e07` 的 blob。改變的兩個項目（報告 PDF 與 README）不是頁面載入的資源，也不在 `offline_scan` 的掃描範圍（`.html`、`.css`、`.js`）。
3. 所以舊 ZIP 上的頁面證據就是在最終 subject 的同一份 dashboard 位元組上取得的。另外，與 dashboard 無關的硬體、瀏覽器版本與量測方法沒有改變。
4. 確認性重做（不是必要條件）：我把新 ZIP 的 `index.html` 與 `assets/` 解到 scratchpad，以 headless Chrome 155.0.8059.85（全新 profile、DevTools 離線、`file://`）執行：本機檔案載入構造的 CSV → `COMPLETED`（21 個候選）、字串全部以字面文字顯示、注入元素 0、非 `file:` 請求 0、dialog 0、例外 0、切回 King County 後 V1 區塊文字不變；375／768 px 下 King County、50 Startups、自訂資料集三個檢視 `scrollWidth`＝`clientWidth`（無水平溢出）。

V2-37 已加註新舊 ZIP 的對應並寫明「是否延用由 Spec Integration Audit R2 判定」；本節是該判定。V2-38、V2-39、V2-40 與 G.2 的證據標示寫「`f56461b` 打包的 ZIP」，標示如實，依上述理由對最終 ZIP 同樣成立（觀察 R2-O2）。

## 7. 範圍 6：修正是否直接產生或暴露 blocking defect

沒有。修正只改了兩份文件的三行；正式章節、測試、程式、頁面與正式分析都不變；新 ZIP 的差異只在預期的兩個項目；報告的建置結果與模板渲染一致。以下是觀察，不延長 cycle（治理 §4.4）：

| ID | 內容 | Disposition | Owner |
| --- | --- | --- | --- |
| R2-O1 | `index.html` `#ex-lasso-card` 的停止原因列舉仍沒有「同一步有多個 group 同時離開路徑」與「預測目標在這些列上沒有變化」。既有狀態，不是本修正造成；DA S1-6 明定不在本次範圍；頁面摘要與候選原因寫出實際原因 | 不需本 cycle 處理；之後若有在 boundary 內修改 dashboard 的工作，可一併補上（屆時須重做 OV-1 並依 SIA-F3 核對位元組） | Orchestrator（tracked） |
| R2-O2 | V2-38、V2-39、V2-40、G.2 引用「`f56461b` 打包的 ZIP」，沒有像 V2-37 那樣加新舊 ZIP 的對應註記；DA S1-4 第 2 點只要求對引用舊 ZIP sha256 的條目加註（這幾條沒有引用 sha256），所以不違反該點 | 依 §6，這些證據對最終 ZIP 成立；本 record 即為該對應的紀錄。若之後整理 ACCEPTANCE，可在這幾條補一句指向本 record | Orchestrator（可選） |

## 8. R1 findings 的狀態

| Finding | R2 結論 |
| --- | --- |
| SIA-F1 | **Resolved**（§2） |
| SIA-F2 | **Resolved**，README 與報告兩處（§3）；`index.html` 的對應文字依 DA S1-6 不在範圍（R2-O1） |
| SIA-F3 | 本次重新打包符合條件（§5）；作為之後任何重新打包（含繳交前）的條件，維持 tracked item（R1 §8；DA 第 5 節） |
| SIA-F4、SIA-F5 | 不在本 R2 範圍；維持 R1 §8 的 disposition（tracked） |
| B-10 | 仍是 open item（ACCEPTANCE V2-42 NOT TESTED，pending merge），不判 FAIL |

## 9. Routing

- 沒有 blocking finding，不需要 Alternate Review 或 Final Adjudicator；沒有需要 Design Authority 或 acceptor 裁決的新問題。
- Spec Integration Audit（cycle 1）在本 R2 closure；最終整合 subject 為 **`17f10a7c1626bd334bee82c93202822d0e9f6976`**（實作 `69f8e07`）。依 DA 紀錄第 5 節，Orchestrator 核對本 subject 與 phase acceptance 時的 HEAD 之間只有 record-only delta 後，可重新派工 Design Authority 作 phase acceptance；open items 照 DA 紀錄第 5 節的表。

## 10. Evidence（本 R2 執行的主要指令）

- 讀取：`decision-20261022-sia-f1-dashboard-wording.md` 全文；`git diff 3745e9c 69f8e07 -- report/report.md README.md`；`git diff 69f8e07 17f10a7`（ACCEPTANCE 的逐字差異、worklog §10、新清單）；`doc/requirement/HW2-req_new-20261021.txt`（第 16、37、44 行）；`index.html` 第 162 行；`assets/explore_engine.js` 檔頭。
- Git（只讀）：`git log --oneline 3745e9c..HEAD`、`git diff --name-only／--name-status／--stat／--quiet`（`3745e9c`、`3750de4`、`cec4c93`、`69f8e07`、`17f10a7`）、`git show <rev>:<path> | sha256sum`、`git grep -F -c`／`-q`（學號，不印值）、`git log -p`、`git rev-list`、`git status --porcelain`。
- 測試：全部 pytest（478 passed、0 skipped）；Node 六個探索測試檔（88 pass）；`python -m hw2.offline_scan`。
- Scratchpad 腳本（`python -I`；只讀 repo 與 `dist/`）：`zipcheck_r2.py`（ZIP sha256、新清單、舊清單、blob 比對、學號位元組、PDF 取出）、`pdfcheck_r2.py` 與 NFKC 文字比對（`pypdf`）、`hw2.report.render_markdown()` 對 `d7f02d4` 與 `69f8e07` 模板的渲染比對、第 12 章 placeholder 抽取；`cdp_h5.js`、`cdp_ov2.js`（新 ZIP dashboard 副本，headless Chrome，profile `prof_r2a`、`prof_r2b`）。
- 程序：只停止我啟動的程序——Chrome PID 27336、19080 以 `taskkill /PID … /T /F` 停止；pytest 的 python 程序（PID 42124、25808）自行結束。之後以 `Win32_Process` 命令列核對：含 scratchpad 路徑的 `chrome.exe`、`msedge.exe`、`node.exe` 0 個。沒有使用 acceptor 的預設 profile，沒有以映像名稱停止任何程序。解出的 PDF、dashboard 副本與 profile 目錄在寫完本 record 後刪除。
- Binding：Bindings §3.6 的方法掃描 `aa43e1e2fb1e18487`（本 R1＋R2）、`acc8906c845bfc14f`（Executor）、`a67436700d54c6ca4`（DA）。
- 寫入的追蹤檔案只有本 record；沒有 commit，沒有 git 寫入操作。

VERDICT: CLOSURE
