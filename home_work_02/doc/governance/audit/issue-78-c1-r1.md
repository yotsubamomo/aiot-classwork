# Audit record — #78 HW2 V2-T5（README、報告探索模式章節、ACCEPTANCE V2 條目、OV-1／SR-09 重做與 ZIP 重打包）R1，cycle 1

- **Work Contract**：GitHub issue #78（OPEN；`gh issue view 78 --json body` 的 sha256 `5e31ce341b67409b98126b8d54e13381fa410150986186e248421090f8c233b2`，與 `derivation-SPEC-V2.md` §3 記錄的 accepted 版本相同）。契約鏈：Outcome Contract §5（V2，接受基準 `d7f02d4179d2cb5c2ecf0c39a4643a6ef8287907`）與 §5.2 CC-V2-1；Brief V2 rev 2＋E-1（§3.5、§5.6、§7、§8）；Spec V2 rev 2（「文件、README、報告與打包」、人工檢查表；未提到者依 Spec rev 5）；`decisions/derivation-SPEC-V2.md`（§4 #78 列、B-8、B-10、I-4、§7.3、§7.4 #78：H-1～H-5，A-1～A-5、A-7～A-9）；分配給 #78 的 `decision-20261022-r1f3-v1-footer.md` R3-6（含第 238 行觀察）、`decision-20261022-issue75-lasso-early-stop.md` R4-5、`decision-20261022-issue77-resource-limits.md` §6、`decision-20261022-issue77-cancel-final-phase.md` §4、`audit/issue-75-c1-r1.md` R1-F4、`audit/issue-77-c1-r2.md` O-R2-1／O-R2-2；run record §1 designation 第 4、5、7 點（經 CC-V2-1）。
- **受審 subject**：branch `home_work_02-v2-enhance`（未 push；`git branch -r --contains` 無結果），**subject identity `3745e9cb4b265e15538576e9b95cd64738e9de35`**。BASE `2b658b3cfaff37fb8ffa93087746ff0c8e3d1398`（#77 結案）。實作 commit `f56461b92c08a9ce8ac82dfcb8508be6e553b3b2`（`README.md`、`report/report.md`、新增 `tests/test_explore_docs.py`）；之後 `460d2488bf5c524d814582ccbde76044c6b8546b`、`3745e9c` 只改 `doc/`（ACCEPTANCE、worklog、`doc/screenshots/v2-issue78/`）。未追蹤的繳交 ZIP `dist/<學號>_hw2.zip`（sha256 `57e1e4a415f891e2495ce00519a0b5c638989e0067cecc47b639a033a87bcd11`，由 `f56461b` 打包；ZIP 不含 `doc/`，所以與 `3745e9c` 的對應項目內容相同，見 §3 AC-4）。
- **Audit 種類**：Formal Ticket 的 **R1**（full independent audit），cycle 1。**本 record 不是** Spec V2 的 Spec Integration Audit。
- **角色**：`primary_reviewer`（`gov-primary-reviewer`），Bindings b5 §3.1 有效 mapping `claude-opus-5-5`／`xhigh`，沒有 escalation、沒有替代。
- **Binding（觀測）**：本 assignment agentId `a1f8b04c1327ec029`（`agent-a1f8b04c1327ec029.meta.json` 的 `agentType`＝`gov-primary-reviewer`），寫入本 record 前以 Bindings §3.6 指令掃描全部 assistant 訊息：`('claude-opus-5-5', 'xhigh')` 210 則，單一元素。Return 前的全程核對由派工者執行。
- **Capability escalation**：不提出（E-AR／D 類 trigger 不屬 primary_reviewer；本審查的每個判斷都能以原始檔案與自行執行的檢查作出）。

## 0. Assurance（Bindings §5 兩欄）

### (a) Context independence（治理 §2.3、Bindings §3.7）

| Property | 滿足方式 |
| --- | --- |
| 1 Independent context | 非 fork 的 `gov-primary-reviewer` subagent，從空白 context 開始，沒有繼承 Executor 或 Orchestrator 的對話。派工內容只有契約與紀錄的路徑、subject 識別與操作規則；其中關於 Executor 的敘述（「ZIP 由 `f56461b` 打包」「records-only」「README 解讀」等）我都當作待驗證主張，本 record 的結論全部來自我自己讀取的檔案與執行的檢查。 |
| 2 Verifiable binding | 標頭的 transcript 觀測（agentId、model、effort、則數）。 |
| 3 Autonomous access | 我自行讀取 repo、git 歷史、GitHub issue、未追蹤的 ZIP、打包 manifest 與作者材料的 hash；自己執行 pytest、Node 測試、離線掃描、報告渲染比對、ZIP 核對、PI 重算、學號比對，並以自己啟動的 headless Chrome／Edge 對 ZIP 解壓的頁面做離線與 H-5 探測（§10）。 |
| 4 Self-written record | 本檔由我以自己的 Write 工具寫入 `home_work_02/doc/governance/audit/issue-78-c1-r1.md`；沒有 commit，沒有修改任何追蹤中的實作、測試、契約或紀錄。 |

### (b) Model diversity（治理 §4.6 V22-17；Bindings §5）

| Assignment | 實際 model（證據） |
| --- | --- |
| Executor（`gov-executor`，agentId `acc8906c845bfc14f`） | `claude-opus-5-5`／`high`，227 則，單一元素——我自行以 Bindings §3.6 指令掃描 `agent-acc8906c845bfc14f.jsonl` 所得，與 run record §11 第 20→ 列的派工者核對（227 則）一致 |
| Primary Reviewer（本 R1，agentId `a1f8b04c1327ec029`） | `claude-opus-5-5`／`xhigh`，210 則，單一元素 |

Executor 與 Reviewer 是同一個 model：**無 model diversity**。Bindings §5 不宣告 diversity 關係，independence 由 (a) 判定。

## 1. Subject 與範圍

- `git diff --name-status 2b658b3 3745e9c`：`README.md`（M）、`report/report.md`（M）、`tests/test_explore_docs.py`（A）、`doc/acceptance/ACCEPTANCE.md`（M）、`doc/governance/worklog/issue-78.md`（A）、`doc/screenshots/v2-issue78/` 11 個檔（A）。全部在 `home_work_02/` 內，沒有 `doc/requirement/`（RB-5）。
- `git diff --name-status 64b2dfd 3745e9c -- assets index.html hw2 tests`：只有新增的 `tests/test_explore_docs.py`；`git diff --stat 31a2255 3745e9c -- assets index.html hw2` 為空——頁面、探索引擎、載入模組與 Python 參照都是 #77 R2 closure 時的內容。
- 工作樹：`git status --short` 只有 Orchestrator 未 commit 的 run record（record-only，非本 subject 的一部分）；`git diff --stat 3745e9c -- home_work_02` 除該檔外為空。我的測試在主 checkout 執行。

## 2. 我執行的檢查（摘要；指令見 §10）

| 檢查 | 結果 |
| --- | --- |
| `.venv/Scripts/python -m pytest -q -rs`（Python 3.11.2） | **478 passed、0 skipped**（110.7 s） |
| README 的 Node 指令：`node --test tests/js/explore_{load,boundary,app,methods,custom,run}.test.js`（Node v24.19.0） | **88 pass、0 fail、0 skipped** |
| `node --test tests/js/core.test.js` | 9 pass、3 skipped（fixture 案例需 `HW2_FIXTURE_MODEL_DATA`；由 pytest `test_node_core.py` 執行，含在 478 中；V1 既有行為） |
| `pytest tests/test_node_explore.py tests/test_node_core.py tests/test_explore_kc_consistency.py tests/test_explore_docs.py` | 38 passed |
| `python -m hw2.offline_scan`（repo）；`offline_scan.scan()` 對 ZIP 解壓的 dashboard | 13 files、0 findings；13 files、0 findings |
| 報告渲染比對：以 `d7f02d4` 與 `3745e9c` 的模板經同一個 `render_markdown()`（同一份作者材料）渲染 | 基準 15 個 `## ` 區段、現版 16 個；**去掉第 12 章後與基準逐字相同**；`dist/report/hw2_report.md` 與現版渲染逐字相同 |
| ZIP 核對（§3 AC-4） | sha256 相符、`testzip()` 無錯誤、67 項、manifest 67 項逐項 size／sha256 相同；`index.html`＋`assets/` 17 檔與 `f56461b`、`3745e9c` 的 blob 逐位元相同 |
| PI 獨立重算（A-2(V2)） | 50 Startups 的兩個 test 模型（`allin`、整體 winner `forward_sfs_k01`）：我以 numpy／scipy 依 split、canonical group 與訓練列基準層級自行擬合 OLS，逐筆點預測、PI 上下界相對誤差 ≤ 7.3e-11，`covered` 逐筆相同，coverage 1.0＝1.0，MAE／RMSE／R² 相對誤差 ≤ 3.8e-11 |
| 探索數字（I-4、H-3(iii)） | 由 Node 引擎對 50 Startups 的 test 指標、前三筆預測、17 個候選的 CV 平均產生 52 種格式字串，`README.md` 與報告模板 0 命中；渲染後第 12 章的數字只有章節號、`k_range` 的 1…18、`home_work_02`、`sha256`、`UTF-8`、`50 Startups`、`100-Days-Of-ML-Code` |
| 瀏覽器探測（§5 H-2、H-5） | Chrome 155.0.8059.85 與 Edge 155.0.4283.62，headless、全新 scratchpad profile、ZIP 解壓頁面 `file://`、DevTools offline＋`--host-resolver-rules=MAP * ~NOTFOUND`：兩個瀏覽器結果相同（§5） |

## 3. #78 Acceptance criteria 逐條

| AC | 判定 | 證據（本 R1 自行取得） |
| --- | --- | --- |
| **AC-1 README** | **PASS**（F1、F2 為 Low） | 功能說明（第 21–24、30–36、45–75 行）；「作業要求對應」以 SRC-4 為準，特徵數「>13」（第 84 行，`HW2-req_new-20261021.txt` 二.1 原文「>13 個特徵」），兩列加分各有**操作**與**驗收**位置（第 85–86 行，所指 V2-1、V2-2、V2-10、V2-18～V2-22、V2-37、V2-42 的內容我逐條核對相符），新版沒有的條目標「新版未載明」（Brief V2 §2 Q1）；探索模式章節（第 129–181 行）含操作、方法、與正式分析的差異、限制與揭露、實作常數；50 Startups 來源、MIT、sha256（第 105 行；sha256 我從 blob 重算相同）；學號只以 `<學號>` 出現；README 的章節與數字測試（`tests/test_report.py`，未改）與新測試通過。README 的 UI 用詞（「分析問題（Problem）」「CSV 的 URL」「載入 URL」「本機 CSV 檔案」「預測目標欄」「取消執行」）與 `index.html` 一致；常數（50,000 × 60、至少 20 列、層級 20、`2e11`／`8e10`、seed 42、20%、5 fold、95%、20 秒）與 `assets/explore_load.js`／`explore_engine.js` 相同（我讀碼；`test_readme_constants_equal_the_code` 亦綁定） |
| **AC-2 報告** | **PASS**（F1、F2 為 Low） | 第 12 章「探索模式（加分功能） 〔老師要求（新版作業頁的加分）〕」在第 11 章之後、附錄 A 之前，不改動任何既有章節號；內容涵蓋加分功能、分析方法、差異（目標尺度、切分、Lasso 停止、派生規則、Test 地位）、限制與揭露、12.5 範圍說明。標示 `〔老師要求（…）〕` 符合 `hw2/report.py` `_LABEL` 的三種標示格式，與既有的 `〔老師要求（課堂口頭）〕` 同型。唯一佔位符 `{{k_range}}`（正式分析的值）；不含探索數字（§2）；渲染比對證明正式各章與前言逐字不變、無日期差異；`hw2/report.py`、`report/` 其他檔、`hw2/package.py`、`hw2/pdf_append.py` 自 `d7f02d4` 無 diff（建置流程不變）；報告建置測試在 478 中通過。章內引用的節號（4.1、4.3、4.4、6.1、7.1、第九章、10.2）我逐一核對內容相符；「訓練與 test 的比例、fold 數與正式分析相同」與 `hw2/paths.py`（0.2、5）和 `explore_engine.js`（0.2、5）相符 |
| **AC-3 ACCEPTANCE V2 條目** | **PASS** | G.1 對 Brief V2 §8 的 1～9、2a 與 acceptor 三條逐條列出條目與狀態；第 3 條拆成 localhost PASS／Pages **NOT TESTED（pending merge）**。V2-37（OV-1）、V2-38（SR-09）、V2-39（OV-2～OV-5）、V2-40（效能）、V2-41（ZIP）、V2-42（Pages）、V2-43（不變量）的陳述與 `ov78_chrome.json`、`ov78_edge.json` 的值相符（我逐項比對：首次繪製 265.1／88.4／90.0／87.2／93.9 ms 與 Edge 260.9…；SR-09 (b) 各類最大值 Chrome 12.2／4.8／9.4／1.4／1.5／1.4／1.4 ms、Edge 12.6／4.4／7.9／1.4／1.4／1.4／1.6 ms；OV-5 最低 6.49:1、6.74:1；OV-2 8 種狀態 0 px；中型資料 101 候選全部 `VALID`、各方法耗時；外部請求只有兩次提交 URL 時各一個 GET）。OV-1 我在 §5 獨立重做（Chrome、Edge）。best effort（真實觸控、Firefox、Safari、螢幕閱讀器）記 NOT TESTED，沒有記 PASS。既有條目只改 V2-11、V2-15、V2-17 三列（R1-F4 註），V1 各節未動（`git diff -U0` 只有第 159、163、165 行與第 183 行後的新增） |
| **AC-4 ZIP** | **PASS**（F3 為 Low） | 我讀取 `dist/` 的 ZIP（檔名、頂層資料夾都是 `<學號>_hw2`，與 V1 規則相同）：sha256 `57e1e4a4…bcd11`、81,620,529 bytes、`testzip()` 無錯、67 項，與 `zip_manifest.txt` 逐項 size／sha256 相同；含新增的 `assets/data/` 4 檔、`assets/explore_*.js` 5 檔、`assets/explore.css`、`hw2/explore_reference.py`；`index.html` 與 `assets/` 17 檔（＝`git ls-tree 3745e9c home_work_02/assets home_work_02/index.html` 的全部）與 `f56461b` 及 `3745e9c` 的 blob **逐位元相同**；其他追蹤檔（README、`hw2/*.py`、`results/*`、`requirements.txt`）是 CRLF 工作樹位元組，CRLF→LF 後等於 blob（與 V1 #67 相同的做法：`results/model_data.json` 的 `cac51bbe…` 也出現在 `worklog/issue-67.md`）。`dist/hw2_package_manifest.json` 記錄 commit `f56461b`、`result_digest` `b53ff286…`、notebook sha256 `2e2f8afc…`。ZIP 任何項目的內容都不含實際學號位元組。解壓後 `file://` 的下拉與 50 Startups 我自己驗證可用（§5）；打包測試在 478 中通過；`git grep` 實際學號 0 命中（§5 H-1） |
| **AC-5 Pages** | **PASS**（記錄要求） | V2-42 記 **NOT TESTED（pending merge）**，寫明合併後以合併 commit 的 `github-pages` 部署為 subject、核對 blob sha256、在 Pages 貼老師 URL 比對、重做 KC 檢查；與 DA B-10、V1 AD-3 一致 |
| **AC-6 不變量** | **PASS** | `git show 3745e9c:` 的 sha256：`app.js` `c1ab3f21…82ad`、`hw2core.js` `e75c5d48…2c14`、`model_data.js` `6cf0c11e…a7ac`、`results/model_data.json` `69dc1465…6e61`、`style.css` `60a27016…3f3f`，與 DA A-3 相同；`git diff d7f02d4 3745e9c -- results hw2.ipynb doc/requirement doc/spec doc/brief doc/ticket CONTEXT.md assets/vendor data` 為空；`hw2/` 自 `d7f02d4` 只有 `offline_scan.py` 修改（#76）與新增 `explore_reference.py`；既有測試只有 `test_dashboard_static.py` 修改（CC-V2-1）；pytest 478／0 skipped、Node 88／0 skipped；ChatGPT PDF `0a5d29e3…a194`、NotebookLM 報告 `77b8f7e7…4a96`、來源清單 `141c211b…5e2b` 與 `hw2/report.py` 的 `ACCEPTOR_MATERIALS` 相同，derived 三檔與 `DERIVED_REVIEWED` 相同；沒有重跑 notebook（`hw2/package.py` 不執行 notebook，只核對既有執行；`result_digest` 照舊）、沒有新的 Test evaluation |
| 結案證據 | 齊備 | worklog 有 Contract reference、binding、執行時間、pytest／Node 輸出（含 skipped 0）；ACCEPTANCE 條目已填且附證據位置；本 record |

## 4. 分配給 #78 的項目

| 項目 | 判定 | 證據 |
| --- | --- | --- |
| R3-6（README 頁面層級陳述） | **符合** | 撰寫時第 20 行「頁面不發出任何對外請求」、第 59 行「完全離線…零對外請求」、第 21 行「Dashboard 只讀取匯出的結果」與截圖說明的「dashboard 只讀取追蹤的匯出結果」都已改寫：第 21 行列出零請求的檢視與「唯一的對外請求」（提交 URL 後一次 GET，不帶憑證、不跟隨重新導向、不重試——與 `explore_load.js` 第 436 行 `{ method: 'GET', credentials: 'omit', redirect: 'error' }` 相符）；第 15、23、36、64 行把主詞限定為 King County 檢視。`grep` README 全文，沒有其他以整頁為主詞的請求或資料來源陳述 |
| R3-6 觀察：報告第 238 行（§7.1） | **處理在 boundary 內，不需 route DA** | Executor D-1 不改 §7.1（AC 要求正式各章不變），改在新章 12.5 寫明「第 7.1 節與第九章所說的 dashboard，是頁面上的 King County（正式分析）檢視…」。這不修改任何正式章節文字，陳述依 DA R3-4 的讀法在其所屬檢視下屬實；我同意這個處理 |
| #75 R1-F4（替換資料截圖） | **符合** | V2-11、V2-15、V2-17 各加「#78 註（#75 R1-F4）」，寫明內嵌資料已替換、不得作 50 Startups 或 Pages 證據；ACCEPTANCE、README、報告的其他地方都沒有引用 `chrome_degenerate_invalid_1280_full.png`、`chrome_h5_probe_1280_full.png`（`grep`：只在這三列） |
| Lasso 提前結束（R4-5） | **符合**（F2 為 Low 的用詞精確度） | README 第 148 行、報告第 379 行：任何提前結束一律同樣處理（已求得段是實際結果、未進入只作展示、k 超過為 `INVALID_MODEL`／`lasso_path_degenerate`、不補齊）；畫面寫實際原因、「走到終點」不代表共線；停止與平手在縮放後的目標上判定、與單位無關、entry alpha 以原尺度回報。與 `explore_engine.js` 第 48–58、1048–1080 行、`explore_app.js` 第 89–94 行與 `index.html` 第 162、229 行一致 |
| resource-limits §6（揭露 (a)(b)） | **符合** | (a) README 第 166 行、報告第 386 行：取消與改選在下一個候選邊界生效；接近載入上限、類別層級多時單一候選（含 All-in）可能數分鐘；期間頁面可操作、King County 可用；README 第 165 行與報告運算預算段「不承諾任何執行時間」。(b) README 第 167 行、報告第 387 行：只以列數與欄數判定、沒有檔案大小上限、整份讀入記憶體、極大檔案可能無法讀取。報告沒有手抄實測值，常數與實測指向 README 與 ACCEPTANCE G 節（I-4 允許的「指向引用」）；README 的常數以測試綁定程式 |
| cancel-final-phase §4 | **符合** | README 第 166 行、報告第 386 行：「全部候選完成之後（計算共線診斷與探索 test 時），則在進行中的步驟完成時停止」「取消後不顯示任何結果，只顯示『已取消』與已完成的方法數；再次執行從頭開始」；切換到 King County 會取消背景執行（`explore_app.js` 第 551–563 行 `cancelActive()`），與 README「切到 King County 時正式分析立即顯示，背景中的執行同樣在下一個邊界停止」相符 |
| #77 O-R2-1、O-R2-2 | **符合** | README 第 167 行：「接近瀏覽器能處理的文字大小（約 512 MiB）時，可能耗盡分頁的記憶體使分頁當掉，而不是顯示訊息；更大的檔案改以位元組逐段檢查，需要數秒，期間頁面不回應輸入」；報告第 387 行同義、不寫數字；與 `explore_load.js` 檔頭的大型輸入說明一致 |
| B-8 | **符合** | README「>13」；報告 §1.2 未改（渲染比對）；`CONTEXT.md` 沒有「10–20」或「10 至 20」（`grep` 0） |
| B-10 | **符合** | V2-42 NOT TESTED（pending merge），G.1 第 3 條同樣標示 |
| I-4 | **符合** | 報告與 README 無探索數字（§2）；章節標題帶標示；+1、+2 標〔老師要求（新版作業頁的加分）〕；「兩種 problem＝同頁下拉切換兩個資料集」寫明是本專案的解讀、「老師原文沒有進一步定義」；探索能力集合與 50 Startups 打包標〔專案延伸〕（README 第 68–71、131 行；報告第 344–349 行標示表） |
| G-4（OV-1 重做時五種方法都有結果） | **符合** | V2-37 與我的探測：50 Startups `COMPLETED`、17 個候選全部 `VALID`、方法按鈕 5 |

## 5. 高風險類別（A-1；DA derivation §7.4 #78：H-1～H-5）

### H-1 憑證、機密與不得公開的資料（A-4）

- 實際學號：從 `.local/packaging.json`（只有一個鍵 `student_id`，10 位數字；值未印出）讀取比對值，對 `origin/main..3745e9c` 的 34 個 commit 每個的樹（含大小寫變形）與 commit message、工作樹的追蹤檔、`doc/screenshots/v2-issue78/` 的 11 個證據檔、issue #78 的本文與留言比對：**全部 0 命中**。ZIP 67 項的內容 0 命中（檔名與頂層資料夾依老師的命名規則含學號，屬未追蹤的繳交物）。
- `git ls-tree -r 3745e9c` 的 `.pdf` 只有老師文件（`doc/requirement/`）；沒有 `.zip`、`acceptor_materials/`、`.local/`、`dist/`、`kaggle.json`、`.env`；#78 的 diff 沒有金鑰樣式字串。`acceptor_materials/`、`dist/` 由 `.gitignore` 排除（`git check-ignore`）。
- 紀錄中的 URL 只有老師公開的範例 URL 與 `http://localhost`、`http://127.0.0.1`；證據 JSON 只記檔名，沒有本機路徑或使用者資料；worklog 與 diff 沒有本機路徑。
- **結果：PASS。**

### H-2 老師指定的名稱與格式、課堂口頭要求的交付

- README「作業要求對應」兩列加分與 >13（§3 AC-1）；報告第 12 章的標示格式（§3 AC-2）。
- OV-1 在 King County 與 50 Startups 的保持（我的獨立探測，Chrome 與 Edge 相同）：ZIP 解壓的 `index.html`（`file://`、瀏覽器層斷網、主機名稱全部無法解析、無伺服器）：King County 五個 V1 區塊與頁尾都渲染；選 50 Startups → `COMPLETED`、17／17 `VALID`、方法按鈕 5、5 個標示區塊、V1 區塊與頁尾隱藏；頁面讀取 13 個 `file:` 資源；整個流程中非 `file:` 的請求只有 (i) 載入時一個 `data:image/svg+xml`（瀏覽器內建的日期輸入圖示，不是網路請求）與 (ii) 提交老師 URL 時恰好一個 GET；例外 0、dialog 0、console error 0；切回 King County 後五個 V1 區塊與頁尾的 `innerText` 與初始逐字相同。
- 靜態掃描在 repo 與 ZIP 解壓副本都 0 findings。ZIP 的命名、項目與 dashboard 位元組（§3 AC-4）。
- **結果：PASS**（F1 涉及「課堂口頭」標示，見 §7）。

### H-3 評估完整性（A-2(V2)、A-3(V2)）

- (i) 正式分析不變：§3 AC-6 的 sha256 與 diff；`results/`、notebook 無 diff；Test evaluation 紀錄（`b53ff286…`）由打包 manifest 與報告建置核對；探索程式（`assets/explore_*.js`、`startups50.js`、`hw2/explore_reference.py`）除 docstring 外不含 `MODEL_DATA`、`model_data`、`test_inputs`。
- (ii) 探索評估：#78 沒有修改引擎、載入模組或參照（自 `31a2255` 無 diff）。我自行執行全部 pytest（含三層邊界、聚合與凍結、King County 一致性、取消／失敗／略過、可重現性、Node 對 Python 參照）與 Node 測試，全部通過；PI 與 coverage 獨立重算（§2）。
- (iii) README 與報告不含探索結果數字（§2）。
- **結果：PASS。**

### H-4 證據真實性與如實標示（A-5(V2)）

- ACCEPTANCE V2-35～V2-43、G.1、G.2 的狀態與證據逐條相符（§3 AC-3）；沒有證據者沒有記 PASS。
- 50 Startups sha256 從 `git show 3745e9c:home_work_02/assets/data/50_Startups.csv` 重算＝`c6075ca5…630d`，與 README、SOURCE、ACCEPTANCE 相同；授權陳述追溯到 `50_Startups.LICENSE.md` 與 `SOURCE.md`（repo、`LICENSE` blob、來源 commit），README／報告只陳述「取自該 repository、該 repository 以 MIT 發布」，不陳述原始出處（I-3）。
- 截圖環境：`doc/screenshots/v2-issue78/` 的 ACCEPTANCE 說明為「`f56461b` 打包、解壓的 ZIP，`file://`、斷網、headless」；我讀過 `chrome_custom_url_failure.png`、`chrome_kc_scatter_zoom.png` 與報告建置的 `dist/report/shots/overview.png`，內容與說明相符。
- 作者材料 sha256 照舊（§3 AC-6）；README、報告沒有 wireframe／mock 數值（報告渲染只來自匯出結果與作者材料）。
- Scope class 標示（I-4）符合。
- **結果：PASS**，另有 F1、F2（Low，non-blocking）。

### H-5 使用者提供的資料來源與網路請求邊界（A-9）

- 列舉：#78 沒有修改任何 V2 程式；我仍對 `assets/explore_*.js` 與 `startups50.js` 搜尋 A-9 所列 API：程式碼中唯一命中是 `explore_ui.js` 第 653 行 `channel.port2.postMessage(0)`（`MessageChannel` 排程器，傳常數 0，不是跨視窗訊息，#77 既有）；`fetch(` 只在 `explore_load.js` 第 442 行。
- Mock fetch 測試（`explore_app.test.js`、`explore_custom.test.js`）在我的 Node 執行中通過；`offline_scan` 例外以單檔為鍵，兩處掃描 0 findings。
- **瀏覽器探測**（R1 證據）：我在 scratchpad 構造的 CSV（60 列）欄名 `<img src=x onerror="document.title='pwned1'">`、`</script><b>bold</b>`、`javascript:alert(1)`（＝前兩欄之和，完全共線）、`<style>body{display:none}</style>`（類別）、`__proto__`、目標 `<script>alert(2)</script>`；類別值 `<svg onload=alert(1)>`、`"><iframe src=//evil.example>`、`a&amp;b`、`<script>alert(3)</script>`。以 `DOM.setFileInputFiles` 從 `#ex-file` 載入（ZIP 解壓頁面、`file://`、斷網）：Chrome 與 Edge 都是 `COMPLETED`；十個字串全部以字面文字出現在 `#explore` 或其下拉選項；`#explore` 內 `img／svg／iframe／script／b／style／object／embed` 元素 0；`document.title` 不變；`body` 仍為 `display: block`；`javascript:` 連結 0；檔案載入期間請求 0；預測器輸入 4 個（含 `__proto__` 欄）。
- 揭露：README 與報告的「URL 讀取」與「沒有檔案大小上限」段落（§4）。
- **結果：PASS。**

## 6. Run invariants（designation 第 4、5、7 點，經 CC-V2-1）

| 項目 | 判定 |
| --- | --- |
| 第 4 點：notebook、`hw2/` 正式路徑、`model_data`、`results/`、Test evaluation 紀錄、V1 區塊 DOM／文字／行為、V1 腳本與核心模組、既有測試不變；不重跑 notebook、無新的 Test evaluation；V1 的 SPEC／tickets／BRIEF 與 #59–#67 不修改 | 成立（§3 AC-6；V1 快照測試通過；`gh issue view 59..67` 皆 CLOSED，`updatedAt` 都在 2026-10-19 或之前） |
| 第 5 點：只有四個 seams；不新增 E2E、CI、治理規則、gate 或角色 | 成立。`tests/test_explore_docs.py` 是 README／報告文件測試，延伸 V1 `tests/test_report.py` 既有的文件測試類別，不測試探索功能的行為，不構成第五個 seam；沒有 `.github/` 變更；Node 與 headless 瀏覽器是 self-verification 手段，不是測試框架 |
| 第 7 點：50 Startups sha256 有紀錄；學號只在 `.local/packaging.json`，追蹤檔案一律 `<學號>` | 成立（§5 H-1、H-4） |
| 正式報告各章與章節號不變；建置流程不變 | 成立（渲染比對；第 12 章插在附錄之前，既有 1～11 章與附錄 A、B 的編號不變；建置程式無 diff） |
| RB-5 根目錄與單元外檔案；`doc/requirement/` | 成立（diff 全在 `home_work_02/`，沒有 `doc/requirement/`） |

## 7. Findings

### F1 — 報告前言、§7.1 與第九章仍以作業頁正文「沒有要求網站」標示 dashboard，第 12 章沒有說明 SRC-4 的主要繳交變更

- **Severity**：Low。**Blocking**：否。
- **證據**：`report/report.md` 第 9 行「唯一的例外是互動 dashboard：它是老師的**課堂口頭要求**，作業頁與講義文字都沒有要求網站」、第 28 行標示表「互動 dashboard｜老師要求（課堂口頭；作業頁正文沒有）」、第 236 行與第 294 行的標題〔老師要求（課堂口頭）〕。SRC-4（`doc/requirement/HW2-req_new-20261021.txt` 二.5 與三）寫「主要繳交: 跟 DIC2 一樣github and web」，Brief V2 §3.5 覆寫 1 把 dashboard 與 repository 改為主要交付。README 已依此改寫（第 24、42、91、97 行，Executor D-5），報告第 12 章只說明兩項加分（第 340 行），12.5 只限定 §7.1／第九章的資料來源與請求陳述，沒有說明這些「課堂口頭」標示是依舊版作業頁。同類的凍結文字還有 King County 概覽區塊的「作業正文 10–20 與補充 14–39 的交集」（V1 區塊，DA B-8 未分配修改）。
- **依據**：DA H-4（V2）「scope class 標示」、Bindings §2.4 的標示規則；#78 AC「正式分析各章內容與數字不變」與 I-5（`tests/test_report.py` 第 140 行、第 369–371 行鎖定「老師要求（課堂口頭」與 §7.1、第九章標題）。
- **Non-blocking 的理由**：這些段落是 AC 與 I-5 凍結的 V1 文字，Executor 不改它們是正確的；陳述對它引用的舊版作業頁（SRC-1／SRC-2T）屬實，且只低估、沒有把專案延伸冒充成老師要求；報告在 SRC-4 下是 optional，主要交付的 README 已正確說明。沒有 accepted 條款或 DA 分配要求第 12 章處理這一點。
- **Disposition**：見 §8。

### F2 — README 與報告對 Lasso 停止的描述有兩處不精確

- **Severity**：Low。**Blocking**：否。
- **證據**：README 第 148 行與報告第 379 行列舉停止原因為「active set 退化、走到終點…，或數值停止（alpha 回升、迭代達上限）」，沒有列出實作中的 `multiple_drops`（`explore_app.js` 第 93 行「同一步有多個欄同時離開路徑」）與 `target_constant`（第 94 行「預測目標在這些列上沒有變化」）；兩處都寫判定在「目標除以它在同一批列上的均方根」的尺度上，實作是目標**先置中**再除以其均方根（`explore_engine.js` 第 50–52 行；頁面 `index.html` 第 162 行寫「置中並除以其均方根」）。
- **依據**：R4-5（說明須與 R4-1～R4-4 實作後的行為一致）、H-4。
- **Non-blocking 的理由**：兩段的核心陳述——任何提前結束一律同樣處理、畫面寫出實際原因、判定與目標單位無關、entry alpha 以原尺度回報——都正確；列舉以「不論原因是」引出，讀者不會因此得到錯誤的處理結論；頁面本身的原因說明完整。
- **Disposition**：見 §8。

### F3 — ZIP 中 dashboard 與 git blob 逐位元相同，靠的是一個沒有寫進打包程式或測試的手動 EOL 步驟

- **Severity**：Low。**Blocking**：否。
- **證據**：`hw2/package.py` 以 `git ls-files` 決定項目、讀**工作樹**位元組；`.gitattributes` 對 `index.html`、`assets/*.js`、`assets/*.css` 沒有 `-text`，在 `core.autocrlf=true` 的 checkout 下會是 CRLF（`git ls-files --eol` 顯示同目錄的 `hw2/*.py`、README 現在就是 `w/crlf`）。Executor 在打包前把 5 個 V1 dashboard 檔以 `git show HEAD:<path>` 寫回 blob 位元組（worklog §3 第 5 點、D-6、§8 觀察 1），這次的 ZIP 因此與 blob 逐位元相同（我在 §3 AC-4 驗證）。`tests/test_package.py` 不檢查 ZIP 內 dashboard 與 blob 的位元組相等。
- **依據**：#78 AC「ZIP 內 dashboard 檔案與 repo 內逐位元相同」、Spec V2「ZIP 與 Pages 的 dashboard 內容相同」。
- **Non-blocking 的理由**：本 subject 的 ZIP 滿足 AC；git 內容沒有被改動（`git status` 乾淨、blob 不變）；風險只在之後有人重新打包而沒有重做這個步驟，屆時位元組不同但內容與功能相同；改打包程式或 `.gitattributes` 不在 #78 的範圍。
- **Disposition**：見 §8。

### 觀察（不是 finding）

- **O-1**：派工把 `460d248` 稱為 records-only。依 Bindings §7，record-only paths 只有 `doc/governance/**`；`460d248` 另改了 `doc/acceptance/ACCEPTANCE.md` 與 `doc/screenshots/v2-issue78/`。本 R1 的 subject 是包含它們的 `3745e9c`，所以沒有影響；之後若在 `3745e9c` 後再有 `doc/acceptance/` 或 `doc/screenshots/` 的修改，不能以 P7 的 record-only 規則略過核對。
- **O-2**：README 第 7 行「完成日期：2026-10-19（合併進 `main`，PR #68）」描述 V1，現在仍屬實；V2 合併後是否更新屬合併後的事項，不是 #78 的 AC。
- **O-3**：Executor 的 Edge 程序樹問題我自己也遇到：以 `taskkill /PID <launcher> /T` 停止後，父程序已結束的 `msedge.exe`（PID 38952，命令列為我的 scratchpad profile）仍在；我以命令列確認是自己的程序後以 PID 停止，之後以 `Win32_Process` 命令列核對，含本 R1 profile 路徑的瀏覽器程序 0 個。沒有以映像名稱停止任何程序，沒有在預設 profile 上啟動瀏覽器（Chrome 版本取自安裝目錄名稱，沒有執行 `chrome.exe --version`）。

## 8. Dispositions 與 owner

| Finding | Disposition | Owner |
| --- | --- | --- |
| F1 | 不需本票修改；不阻擋 #78 結案。列入 Spec V2 Spec Integration Audit 的 pack 供知悉。若之後要處理，在 boundary 內的作法是在第 12 章（例如 12.5）加一句說明前面各章的「課堂口頭」標示依舊版作業頁、新版把 GitHub 與 web 列為主要繳交——不改正式章節、不改測試；是否需要這句屬 allocation 問題，由 Design Authority 判定，Reviewer 不預判。修改凍結的正式文字或 `tests/test_report.py` 會改變 accepted invariant（I-5），屬 acceptor 的 contract change，不建議 | Orchestrator（列入 Spec Integration Audit pack；如要處理，route Design Authority） |
| F2 | 不需本票修改；之後若有在 boundary 內修改 README 或第 12 章的工作，順帶補上 `multiple_drops`、`target_constant` 與「置中」 | Orchestrator（tracked；Spec Integration Audit 知悉） |
| F3 | 不需本票修改。任何重新打包（含合併後的更新）須在打包後再核對 ZIP 內 `index.html` 與 `assets/` 的 sha256 等於該 commit 的 blob（V2-41 的做法），不符時重做 EOL 步驟；Spec Integration Audit 依 A-6 核對 ZIP 時一併確認 | Orchestrator（run record 記錄；Spec Integration Audit pack） |
| O-1～O-3 | 僅供知悉 | — |

## 9. Routing

- 沒有 blocking finding：不需要 targeted correction、R2、Alternate Review 或 Final Adjudicator。
- 沒有需要 Design Authority 現在裁決的契約語義問題；F1 只有在 Orchestrator 或 Spec Integration Audit 決定處理時才 route 至 Design Authority（allocation）。
- 不需要 acceptor 的決定；push、merge（RB-1）、繳交（RB-2）仍保留給 acceptor，本 R1 不涉及。

## 10. Evidence（本 R1 執行的主要指令）

- 讀取：Bindings b5 全文；治理 v2.2 §2.3、§4.1–§4.7；impl-default v2 §6、§7；`outcome-contract.md`（§1–§5.2）；`gh issue view 78`（body sha256）；`SPEC-V2.md`、`BRIEF-V2.md` 全文；`derivation-SPEC-V2.md` 全文；`decision-20261018-high-risk-categories.md`、`decision-20261018-issue60-a4-student-id.md` §1–§2；四份分配的 DA decision 全文；`audit/issue-75-c1-r1.md` R1-F4、§6；`audit/issue-77-c1-r2.md` O-R2-1～3；run record（committed 與工作樹）；worklog `issue-78.md`；`git show 3745e9c:` 的 README、報告模板、ACCEPTANCE G 節、`50_Startups.SOURCE.md`／`LICENSE.md`、`tests/test_explore_docs.py`、`tests/test_report.py` 相關段落；`assets/explore_load.js`、`explore_engine.js`、`explore_app.js`、`explore_ui.js`、`index.html` 相關段落；`hw2/report.py`、`hw2/package.py`、`hw2/paths.py` 相關段落；`doc/requirement/HW2-req_new-20261021.txt`。
- Git：`git rev-parse`、`git log`、`git show --stat`、`git diff --name-status／--stat／-U0`（`d7f02d4`、`2b658b3`、`31a2255`、`64b2dfd`、`f56461b`、`3745e9c`）、`git ls-files --eol`、`git ls-tree`、`git show <rev>:<path> | sha256sum`、`git grep -F -q`（學號，不印值）、`git rev-list origin/main..3745e9c`、`git check-ignore`、`git branch -r --contains`。
- `gh issue view 59..67、78 --json number,state,updatedAt`；`gh issue view 78 --json body,comments`。
- 測試：`.venv/Scripts/python -m pytest -q -rs -p no:cacheprovider`；`node --test`（六個探索測試檔、`core.test.js`）；四個 pytest 檔的單獨執行；`python -m hw2.offline_scan`；`offline_scan.scan()` 對 ZIP 解壓副本。
- Scratchpad 腳本（`python -I`，只讀 repo 與 `dist/`）：`zipcheck.py`（ZIP sha256、manifest、blob 比對、學號位元組）、`rendercmp.py`（基準與現版模板的渲染比對）、`run50.js`＋`pi_recompute.py`（引擎結果與 PI 獨立重算）、探索數字字串搜尋、`probe.js`（Chrome／Edge 的 CDP 探測；結果 `probe_chrome.json`、`probe_edge.json` 留在 scratchpad）。ZIP 解壓副本與兩個瀏覽器 profile 已刪除。
- 作者材料與 derived 三檔：`sha256sum`（只比對 hash，沒有讀取或轉錄內容）。
- Binding：Bindings §3.6 指令對 `agent-a1f8b04c1327ec029.jsonl`（本 R1）與 `agent-acc8906c845bfc14f.jsonl`（Executor）。
- 寫入的檔案只有本 record；沒有 commit，沒有修改任何追蹤中的檔案。

VERDICT: CLOSURE
