# Audit record — Spec Integration Audit：SPEC rev 5（#59），cycle 1，R1

| 欄位 | 內容 |
| --- | --- |
| Work Contract | Outcome Contract `home_work_02/doc/governance/outcome-contract.md`（Brief `doc/brief/BRIEF.md` @ `dff7c55c`＋CC-1、AD-1～AD-3）；上位契約 `doc/requirement/`（SRC-1、SRC-2T）；Derived contract `doc/spec/SPEC.md` **rev 5**（＝GitHub issue #59，本文與檔案逐行相同，我以 `gh issue view 59` 比對）；DA derivation `decisions/derivation-SPEC.md`（§3 B-1～B-16、§4 acceptance boundary 分配、§9 Tickets、§9.3／§9.6 條件 1～6、§11 G-1～G-5）；DA decision records：`decision-20261018-high-risk-categories.md`（H-1～H-4、A-1～A-8）、`decision-20261018-lane.md`、`decision-20261018-issue60-a4-student-id.md`（S-1～S-6）、`decision-20261018-issue62-shared-subset-test-key.md`（D-1～D-4）、`decision-20261018-issue63-js-tolerance.md`（T-1～T-3）、`decision-20261018-issue64-notebook-rerun.md`（N-1～N-6、§9.3 條件 7、8）、`decision-20261018-issue64-standardized-reading.md`（R-1.1～R-1.5）、`decision-20261019-issue65-labels-figures.md`（L-1～L-3、F-1～F-5）、`decision-20261019-cell28-glyphs.md`（G-1～G-5）；Tickets #60～#67（全部 CLOSED，`gh issue list` 核對）；run record `run/run-20261018-hw2-formal.md`（acceptor 指示 §1、§14、§15、§17、§19） |
| 受審 subject | **最終整合 subject**：branch `home_work_02-regrill`，implementation commit **`e2780f46dbea4d0816a6dcc8bba0725bc6182797`**；整合範圍＝run activation base `60d7fa6`..`e2780f4`（`git diff 60d7fa6 e2780f4`：114 個檔案，單元外只有 root `README.md`、`CONTEXT-MAP.md` 各 +1 行，沒有 `doc/requirement/`）。審查期間 HEAD 由 `e398726` 前進到 `e383a14`；`git diff --name-only e2780f4 HEAD` 只有 `doc/governance/{audit,run,worklog}/**` 與 `doc/ticket/tickets.md`（record-only，Bindings §7）；工作樹對 `e2780f4` 的非紀錄路徑無差異（`git diff --quiet`）。**未追蹤產物（以 sha256 識別，impl-default §7）**：`dist/<學號>_hw2.zip` `c84a3c5e6d295ed383fc8c085eb68f30aaa9035208cf9ca7eeaa0d9aae763fb6`（81,432,807 bytes，56 項，由 `e2f391a` 打包；`git diff --stat e2f391a e2780f4` 只有 ACCEPTANCE.md、`tests/test_report.py` 與 root 兩列，都不在 ZIP 內）；`dist/<學號>_hw2.ipynb` `2e2f8afc1f67fd51312b894d3a3f4873049defead185b1dd4ca2ab1ace04ff64`；ZIP 內 `hw2_report.pdf` `8778b459005efda573f4028ef47417d936b24b8ba7b24edc7aaf7979556fbbfe`；acceptor 材料 `ChatGPT_logs.pdf` `0a5d29e3…a194`、NotebookLM docx `77b8f7e7…4a96`、`sources.md` `141c211b…2b`；derived `gpt_assist.md` `1a9663f7…6023`、`notebooklm_summary.md` `358c78f2…731d`、`notebooklm_trace.md` `5cae0356…b4`（全部由我自己計算） |
| Audit 種類 | **Spec Integration Audit**（治理 §4.7），獨立的 audit instance，**R1，cycle 1**。不是任何 Ticket audit 的 R3；Spec 有 8 張票，不適用單 Ticket fast path（Bindings §5）。SPEC rev 5 是同一 Outcome Contract **唯一、也是最後一份**未結 Spec，所以本 record 另核對全部 derived Specs 的分配合起來涵蓋整個 acceptance boundary（第 3.2 節） |
| 角色 | `primary_reviewer`（definition `gov-primary-reviewer`；Bindings §3.1 R-PR mapping `claude-opus-5-5`／`xhigh`） |
| Assurance (a)：context independence（治理 §2.3；Bindings §3.7） | (1) **Independent context**：Orchestrator 以 Agent tool 派工的 `gov-primary-reviewer`（非 fork），空白 context；派工內容是路徑、識別與必核項目。Worklog、run record 與各 audit record 中 Executor／Orchestrator／前一位 Reviewer 的敘述，我只當作待驗證主張；下文的事實都由我自己取得。我的 scratch 目錄與 Orchestrator session 共用同一個 scratchpad 根目錄；其中 `ex67/` 的 Executor 證據檔我只唯讀核對（第 4.1 節），我的腳本與輸出都在另建的 `sia/`。(2) **Verifiable binding**：見 (b) 欄。(3) **Autonomous access**：自行讀取 Bindings、治理 §2.3／§4.1–§4.7、impl-default §6–§7、OC、Brief、CONTEXT、上位契約轉寫、Spec、全部 DA records、全部 worklog／audit／run record、`gh issue view` #59～#67 與 #50～#56 狀態、git 歷史與 diff、程式、測試、notebook、結果檔、ZIP、未追蹤的 acceptor 材料；自行執行 pytest、Node test、離線掃描、獨立重算（不 import `hw2`）、選擇路徑的獨立重推、乾淨環境的一次完整重跑（條件 7、8）、報告 draft 建置、ZIP 解壓與逐項比對、報告 PDF 的頁面比對與文字擷取、Chrome／Edge 的離線量測、學號比對、外部連結核對。(4) **Self-written record**：本檔由我以自己的 Write 工具寫入 |
| Assurance (b)：model diversity（Bindings §5；治理 §4.6） | 我以 Bindings §3.6 的同一邏輯掃描 session `4bbff425-7ff9-4cdc-b64c-cc68e824e1b1` 的 subagent transcripts：**Executors**（`agentType`＝`gov-executor`，各自單一元素 `('claude-opus-5-5', 'high')`）：#60 `a447664b1c57e651b` 167 則、#61 `af27ea1586955f943` 285、#62 `a04e1bc646c4d6912` 257、#63 `a9f28ccd59c59b6b3` 315、#64 `a2b1c8f4cc400f3be` 220、#65 `a4779b376d79e3353` 304、#66 `ae6f6de8468402cf7` 283、#67 `ae2448c02ec3d8940` 332。**本 review**：agentId `a5b2226e12e62438f`，`agentType` `gov-primary-reviewer`，撰寫本 record 前觀測 `('claude-opus-5-5', 'xhigh')` 283 則、單一元素；全程核對由派工者依 Bindings §3.6 在採用本 record 前執行。**無 model diversity**（全部為 `claude-opus-5-5`）。Bindings §5 不宣告 diversity 關係，不記 `diversity_lost`（A-8） |
| 日期 | 2026-10-19 |

## 1. 審查方法與環境

- 腳本與輸出放在 session scratchpad 的 `sia/`（不在 repo）。環境：單元 `.venv`（Python 3.11.2）；另建的乾淨 venv（第 4.1 節）；全域 Python 3.11.2（pypdfium2，只讀取 PDF，`python -I`）；Node v24.19.0；Chrome 155.0.8059.80、Edge 155.0.4283.62（headless，全新暫存 profile）。
- **Test 評估**：我沒有在 repo 內執行 notebook、`hw2.run_notebook`、`hw2.package`，也沒有在 repo 內開啟守門。唯一一次執行包含評估 cell 的完整 notebook，是在 repo 外的 scratch clone，依 `decision-20261018-issue64-notebook-rerun.md` §9.3 條件 7 先做前置核對、再執行一次、依條件 2／8 比對並記錄（第 4.1 節）；它是 #63 run `fe76019b…` 的重現，不是新的評估，結果沒有寫回 repo。其他重算只用 training 列擬合，或只對已匯出的 `test`／`test_inputs` 做算術（A-2 的獨立重算）；Ridge／Lasso 我沒有在 test 列上重新預測。
- **學號、作者材料**：學號只在記憶體中讀自 `home_work_02/.local/packaging.json`（`git check-ignore` 命中 `.gitignore:13`），所有輸出只有布林值與計數，或遮罩成 `<學號>`。我讀了 NotebookLM docx 的文字與 ChatGPT PDF 的抽樣頁面（A-5），本紀錄不轉錄其內容、作者姓名或對話網址。審查結束前，我刪除了含學號路徑的 ZIP 解壓目錄、瀏覽器暫存 profile、材料文字與頁面渲染；之後以學號值對 `sia/` 的 28,124 個檔案做檔名與內容比對：**0 命中**。

## 2. 範圍一：跨 Ticket invariants

| # | Invariant（涉及的票） | 結論 | 我取得的證據 |
| --- | --- | --- | --- |
| I-1 | `model_data` 是 Python 匯出、dashboard、報告、README 的單一數字來源（#60～#67） | **成立** | `assets/model_data.js` 解析後等於 `results/model_data.json`；dashboard 的 Test 數字只讀 `test`（`app.js:537`、`:673`），`test_inputs` 只取列識別與實際價格供繪圖（`app.js:658-663`）；報告 PDF 的 72 格 k 路徑表、比較表、涵蓋率表、係數表（16 個數值欄的每 1 SD 百分比）、permutation importance、計時，與 `results/tables/*.csv`／`model_data` 逐一相符（`report_numbers.py`，缺漏 0）；README 成果段 5 個數字與 `test.forward_sfs_k17` 相符 |
| I-2 | Test 資料隔離與單次評估的時序（TR-01、§9.3 條件 1～6、CC-1 (3)(4)；#60～#63、#67） | **成立** | 被追蹤的 `model_data` 只在 `f20d70e`、`c9b106c`、`77b79f4`、`a2811e9`（`test_inputs` 0 列、無 `test`、`fixture` false）、`052984b`（#63 唯一一次評估）、`2cd2a70`（#67 重現）改變；`OFFICIAL_TEST_GATE_ENABLED` 只在 `c9b106c`（建立，關閉）與 `d413e58`（開啟）改變；notebook 中沒有設定此旗標；`tests/conftest.py:24-44` 在整個 pytest process 關閉守門 |
| I-3 | 選擇與評估路徑凍結（§9.3 條件 7(b)；#63 之後的全部票） | **成立** | `git diff 052984b e2780f4 -- hw2/{data,split,preprocess,selection,models,comparison,ols,metrics,contract,testgate,export}.py requirements.txt data/` 為空；`selection_digest`（manifest 與我依匯出 `winners`＋alphas 自行計算）＝`44f7723e…4b28`；`result_digest`（我依 `export.result_digest` 的規則自行實作）＝`b53ff286…c3cfc6` |
| I-4 | 以 `id` 分組的隔離、fit 只用訓練列、fold-internal selection（#60 分割 → #62 選擇 → #63 alpha → #64 診斷） | **成立** | 見第 7 節 A-2：分割與 fold 依文件化規則獨立重推一致；4 種方法 × (5 fold × 18＋18 canonical)＝432 個子集由我自己的實作只用訓練列重推，**0 不符**；兩個授權模型只用 training 列重擬合，係數、s²、秩與匯出一致 |
| I-5 | 「同一模型」的識別與呈現（D-1～D-4；#62～#67） | **成立** | D-4 第 1～5 點以程式核對全部成立（第 7 節）；dashboard Test 區塊對 5 個方法各以自己的身分顯示並註明共用（我的瀏覽器紀錄）；報告 §6.1「2 個不同的 OLS 模型＋2 個 metric-only，共 4 個」與比較表每列的共用註記；README 成果段同 |
| I-6 | 三種標示一致，dashboard 標為課堂口頭要求（L-1～L-3；#65、#66） | **成立** | 報告標示對照表與各章標題、README、ACCEPTANCE 開頭一致；報告第 7.1、9 章標「老師要求（課堂口頭）」；補充建議（Adjusted R²、五大假設、Deployment、Ridge／Lasso）標「依老師補充建議」 |
| I-7 | 學號與作者材料不進追蹤檔案（H-1；全部票） | **成立** | 第 7 節 S-5、第 8 節 H-1 |
| I-8 | 單一來源的主程式：追蹤的 notebook＝打包的 notebook，且來自同一次完整執行（Brief §8；N-3） | **成立** | ZIP 內 `<學號>_hw2.ipynb` 與工作樹 `hw2.ipynb`、`dist/<學號>_hw2.ipynb` 逐位元相同，與 `e2780f4` blob 只差 EOL；單次執行判準見第 7 節 N-3 |
| I-9 | 「唯一一次正式評估是 #63、之後是重現」的陳述一致（N-5） | **成立** | README「Test 評估只有一次」段與重跑步驟（「重現唯一一次的 Test 評估」）、報告 §6.1 與附錄 A（`fe76019b…`、`b53ff286…`、目前檔案 `5e74d03d…` 是重現）一致 |

## 3. 範圍二：Spec-level AC coverage

### 3.1 Spec AC 逐項判定

Spec rev 5 沒有編號的 AC；我以 Testing Decisions（主 seam、次 seam、人工檢查表、OV 分類）加上 Implementation Decisions 中可觀察的要求逐項判定。

| # | Spec 要求（rev 5 章節） | 判定 | 證據（我自己取得） |
| --- | --- | --- | --- |
| S-1 | 主 seam pytest：區段與必要欄位；`methods` k＝1…18、canonical 與各 fold 的 group 數＝k；`invalid` 附原因且不是 winner；`methods`／`baselines` 無 test 欄位；`winners` 與旗標一致；`ols_subset` 鍵＝授權清單、`metric_only` 只有 Ridge／Lasso、PI 欄位有無與 kind 一致；covered／coverage／平均寬度一致；獨立重算（容差依 T-1 為相對 1e-6）；`meta` 的 sha256、seed、版本、時間；`test_inputs` 房屋數與重複交易數 | **PASS** | repo（工作樹＝`e2780f4`）`python -m pytest -q`：**395 passed**；乾淨 clone：392 passed、3 skipped（3 個只在本機有學號設定或材料時才執行的測試）；我自己的 `indep_check.py`（不 import `hw2`）全部項目成立，逐筆重算的相對差為 0（兩個模型 × 4,323 列） |
| S-2 | 主 seam Node：每個 `ols_subset` × 每列 test 以 dashboard 自己的前處理與預測重算 prediction／lower／upper／covered；`metric_only` 不提供預測；前處理單元案例；All-in k 固定；winner 與契約一致；`invalid` 不為 winner | **PASS** | `node --test tests/js/core.test.js`：9 pass、0 fail、3 skipped（fixture 版需環境變數；fixture 版由 `tests/test_node_core.py` 執行，含在 395 之內）；官方逐筆重算 pass |
| S-3 | 次 seam 分割：無共同 `id`、聯集為全部、同 seed 重現、約 80／20；fold 兩兩無共同 `id` | **PASS** | `test_split.py` 11 項；我依 `meta.split`／`meta.cv` 文件化的規則（`default_rng([seed,0])`、`[seed,1]`）獨立重推 test 房屋集合與 fold 分配，與 `split_assignment.csv` 相同；train／test 共同 `id` 0、fold 兩兩共同 `id` 0、test 房屋比例 0.19999 |
| S-4 | 前處理：fit 只看訓練列、未見類別編為基準、日期與整修的數值案例 | **PASS** | `test_preprocess.py` 16 項；我只用 training 列擬合的兩個授權模型，one-hot 類別、係數（最大絕對差 5.5e-9）、s²（相對差 4.1e-16）、秩與 df 都等於匯出 `fit` |
| S-5 | 特徵選擇：每步變動恰一個 group；Lasso 平手依 canonical order；p-value backward 只移除 p＞門檻；選擇邊界（改動驗證列不改變子集；canonical 只由整個 training set 決定） | **PASS** | `test_selection.py` 16 項、`test_comparison.py::test_pvalue_selection_boundary_is_fold_internal`；我以自己的 Forward／Backward（in-sample RSS）、RFE（`sd(X_g β_g)`）、Lasso 路徑（LARS、group 首次非零）實作，只用各 fold 的訓練列與整個 training set 重推：432 個子集 0 不符，`folds_agree` 一致 |
| S-6 | 模型與推論：秩不足三類語義；Adjusted R² 用實際秩；PI 公式；coverage 閉區間 | **PASS** | `test_models.py` 16 項、`test_ols.py` 7 項；正式資料 0 個 invalid 候選；我以實際秩重算兩個授權模型的 log 尺度 R² 與 Adjusted R²，與 `fit` 相符（差 < 1e-9）；t 臨界值＝`t.ppf(0.975, df_resid)` |
| S-7 | 選模：winner 平手規則；授權集合推導；同一執行內第二次呼叫評估函式報錯 | **PASS** | 我依 Spec 規則（CV RMSE 最小、平手取小 k；整體依固定方法順序）重推 4 個方法 winner 與整體 winner（`lasso_path_k17`），與 `winners` 相同；notebook cell 42 輸出「second evaluation refused」；manifest `evaluations_in_this_run` 1；`test_testgate.py` 21 項 |
| S-8 | 資料：sha256 先於解析、schema、列數、唯一 `id`、`sqft` 恆等式 | **PASS** | 我計算的 CSV sha256＝Brief 釘值；21,613 × 21、唯一 `id` 21,436、恆等式每列成立；`test_data.py` 8 項 |
| S-9 | Ridge／Lasso 對照（CC-1 六項約束；G-1～G-4） | **PASS** | alpha 等於 `cv_by_alpha` 的訓練 CV 最小者（Ridge 1e-4、Lasso 1e-8，皆位於網格下緣，報告 §5.2 如實說明）；`winners` 不含 Ridge／Lasso；`test` 的 `metric_only` 只有 USD 的 MAE／MSE／RMSE／R²，無 PI、coverage、逐筆欄位；`baselines.ridge`／`lasso` 無 `fit`；dashboard 的預測只對有 `fit` 的 OLS（`hw2core.js` `canPredict`）；報告 §6.2 比較表訓練 CV 欄與 Test 欄分開；`test_comparison.py::test_changing_the_test_rows_changes_no_alpha_cv_metric_or_selection`（G-1） |
| S-10 | `model_data` 契約不變量（含 B-3：UI 不以 `test_inputs` 評估） | **PASS** | 第 7 節 A-3 |
| S-11 | Dashboard 人工檢查：必要區塊、zh-TW 無缺字、方法與 k 切換、比較全部、預測器與警告、來源標示、Test 區塊標示與不同模型提示、`invalid` 標示、可讀性與反應性 (a)～(e)、離線 | **PASS**（`invalid` 標示只能以 fixture 驗證，正式資料無 invalid） | 我在解壓的 ZIP 上以 Chrome、Edge 量測（第 4.2 節）：全部必要區塊渲染、5 個方法、KPI 4、預測器 19 個輸入、方法與 k 切換同步、非 winner 時 Test 提示出現（k＝1、9、18）、winner 時不出現（k＝17）、比較全部、預測器輸入後更新；畫面文字 U+FFFD／U+25A1 為 0，截圖目視無缺字；`app.js`／`index.html` 含「訓練 CV（USD）」「Test 評估（USD）」「全訓練集擬合，R²／Adjusted R² 為 log 尺度」與未見 zipcode 警告原文；`invalid` 由 `tests/js/core.test.js` fixture 與 `test_models.py::test_invalid_candidates_never_win_even_with_the_lowest_rmse` |
| S-12 | Pages URL 上重做同一份檢查 | **NOT TESTED（pending merge）** | AD-3：合併後的 Lightweight work item（觸及 H-2，需 audit）；ACCEPTANCE D-12 如實記錄；我 2026-10-19 以 `curl -L` 確認目前 404（`origin/main` 沒有 `home_work_02/`）。依 AD-3 列為 open item，不阻擋本 audit |
| S-13 | OV-1～OV-6（AD-1） | **PASS**（best-effort：真實觸控、Safari、螢幕閱讀器 NOT TESTED；Firefox best effort） | OV-1、OV-3（Chrome 與 Edge）、OV-6 (a)(b)(g) 與 OV-2（375／768 px）由我自行量測（第 4.2 節）；OV-6 (c)(d) 我看了自己的縮放截圖：y＝x、區間內外以顏色與形狀可分辨，放大後可分辨個別 PI 線段；OV-4、OV-5、OV-6 (e)(f) 依 `worklog/issue-67.md` §8.4、§8.5、§8.6 與 ACCEPTANCE E 節的紀錄，已由 #67 R1 獨立重核（OV-5 重算最低對比 6.49:1），我沒有重做鍵盤巡覽與對比量測 |
| S-14 | 報告人工檢查：章節完整、三種標示、數字與匯出一致、附錄 ChatGPT PDF、NotebookLM 字數與可追溯性、主流解法連結可開啟 | **PASS** | ZIP 內報告 PDF 149 頁＝28＋121；附錄 121 頁與 `ChatGPT_logs.pdf` 逐頁渲染相同（121／121）；本文含標示對照表、第 1 章（含 §1.4 Kaggle 名次不適用）、第 2～7 章六個 CRISP-DM 階段、第 8 章 4 個公開解法（附連結、自報指標與不可比之處）、第 9 章 dashboard 連結與截圖、第 10 章「GPT 輔助內容」、第 11 章「NotebookLM 摘要」、附錄 A、B；數字見 I-1；摘要本文漢字 523（我以 `unicodedata` 自行計數，B-15）；外部連結 `curl -L`：6 個 200，SciTePress DOI 302 至 SciTePress 網域（#67 已以瀏覽器確認可開啟） |
| S-15 | Repo：`git grep` 無實際學號；追蹤檔案不含 acceptor 材料、PDF（老師文件除外）、ZIP、`.env` | **PASS** | 第 7 節 S-5；`git ls-files` 的 PDF 只有 `doc/requirement/` 的老師文件，無 `.zip`、`.env`、`kaggle.json`、`.local/`、`dist/`、`acceptor_materials/`；整合 diff 中沒有金鑰型字串 |
| S-16 | 乾淨環境重跑：新建 venv、安裝、非互動執行、重跑測試、建置報告、打包；數字與追蹤檔一致 | **PASS** | 我自己的重跑（第 4.1 節）：新 venv、鎖定版本安裝、條件 7、一次完整執行、測試、報告 draft 建置；`result_digest` bit-exact；結果檔 18／18 逐位元相同。打包步驟由 #67 Executor 在乾淨 clone 執行（`worklog/issue-67.md` §7），我以 ZIP 與 manifest 逐項核對其產物（第 7 節 A-6） |
| S-17 | 打包：由同一份 notebook 產生學號檔名、ZIP 內容、記錄 sha256 與檔案清單、解壓驗證離線 | **PASS** | 第 7 節 A-6 |
| S-18 | 執行時間量測並記錄（Brief Q34；Spec「特徵選擇與模型」） | **PASS** | `meta.timing_s`、`meta.path_timing_s` 每方法有值；notebook 4.2、報告 §5.4 列出；README 指出記錄位置（數字每次執行不同，依 Q26 不手抄）；`test_selection.py::test_run_path_methods_times_every_method` |
| S-19 | 單元 `.gitignore`、`requirements.txt` 鎖版本、Out of Scope | **PASS** | `.gitignore` 排除 SRC-2 PDF、`acceptor_materials/`、`.local/`、`dist/`、`.venv/`、`.ipynb_checkpoints/`；`requirements.txt` 11 個套件 `==` 鎖定；沒有後端、API、資料庫；沒有 SelectKBest／permutation importance 作為選擇方法；異常值未刪除；沒有 Ridge／Lasso 的 PI 或即時預測；沒有對全部 (方法, k) 的 test 評估；沒有修改其他單元 |
| S-20 | Root README 與 CONTEXT-MAP 各一列（RB-5） | **PASS** | 第 6 節 |

### 3.2 Spec AC 對分配的 acceptance boundary 的涵蓋，以及全部 derived Specs 的涵蓋

- **分配**：`derivation-SPEC.md` §4 把 Outcome Contract 的**全部** acceptance boundary（Brief §3、§4～§11 的驗收意圖，含 CC-1）分配給唯一的 SPEC。只有一份 derived Spec，所以「全部 derived Specs 合起來涵蓋整個 boundary」等同於這份 Spec 的涵蓋。
- **逐項對照**：我逐條讀 Brief §3.1（T-資料、T-模型、T-預測圖、T-CRISP-DM、T-AI、T-繳交、T-GitHub、T-評分）、§3.2（dashboard、補充建議與標示）、§3.4（不做）、§4（資料、前處理、log 目標、異常值、分割）、§5（方法、All-in、group、k、公平性、winner、test 範圍、最終模型、指標、推論）、§6（PI、限制陳述、涵蓋率驗證、五大假設）、§7（技術、離線驗收、必要區塊、操作、BR-01 五點與 UI 驗收、預測器、Q43）、§8（交付物）、§9（acceptor 輸入）、§10（驗證）、§11（BR-03），每一項都在 S-1～S-20 或第 7、8 節有對應證據與判定。derivation §4 標為 T-義務的項目（notebook 六章、README 內容、Q38、學號設定路徑、外部 URL 靜態掃描）都由票帶入並在最終 subject 上成立（`test_notebook_structure.py`；README；報告 §1.4；`.local/packaging.json`；`hw2/offline_scan.py`）；TK-2（結果 CSV／PNG）與 DA F-1（預測圖 PNG）在 ZIP 與報告中成立；TK-3、TK-4 成立（報告 §4.3、§6.2；S-1）。
- **唯一不在本 run 完成的部分**：Brief §7「同一份檢查也在 GitHub Pages 的網址上做一次」與 §10「Pages URL 可開啟」。依 acceptor 的 AD-3，它被分配到合併進 `main` 之後的 Lightweight work item，不是缺口，也不是重疊；本 audit 與 phase acceptance 把它列為 open item（S-12）。
- **結論**：Spec AC 整體涵蓋其分配的 acceptance boundary；扣除 AD-3 明確移出的 Pages 項目，全部 derived Specs（只有這一份）的分配合起來涵蓋整個 acceptance boundary。沒有分配缺口或造成歧義的重疊。

## 4. 範圍三：整合行為

### 4.1 乾淨環境的一次完整重跑（我自己執行；§9.3 條件 7、8）

| 步驟 | 內容與結果 |
| --- | --- |
| 環境 | `git clone -c core.longpaths=true --no-checkout` 本機 repo 到 scratch，`checkout --detach e2780f46…`（clone 工作樹乾淨）；`py -3.11 -m venv`（Python 3.11.2）；`pip install -r requirements.txt` 09:29:57Z～09:32:40Z，exit 0；`pip freeze` 中 11 個鎖定版本全部相符 |
| 條件 7(a)（重跑前、守門不開） | 我自己寫的 `sia_cond7a.py`：kernel 內先把 `hw2.testgate.OFFICIAL_TEST_GATE_ENABLED` 設為 False，只執行開啟守門那一格（cell 41）之前的 24 個 code cell，notebook 檔案不寫回；09:33:04Z～09:33:54Z。`selection_digest`（模組函式與我自己的 sha256 實作）＝`44f7723e4023afc3e8e997f42bf4eb59db392af81cced11743757a9857cb4b28`；授權 `allin`、`forward_sfs_k17`；整體 winner `lasso_path_k17`；alphas ridge 1e-4、lasso 1e-8；正式 test 列未載入；資料 sha256＝釘值；notebook 未變 |
| 條件 7(b) | 凍結模組與 `requirements.txt` 對 `052984b` 的 diff 為空；notebook cell 0–27、29–45 的 source、id、型態與 `052984b` 相同；cell 28 恰為 G-3 的一行、0 行註解（G-5 修正版）；metadata 相同；資料 sha256＝釘值 |
| 完整執行（只一次） | `.venv/Scripts/python -m hw2.run_notebook`，09:34:08Z～09:34:49Z，`executed hw2.ipynb in 40.4 s`，exit 0 |
| 條件 8：本次 manifest | `run_id` `922a7e60c8de45249786e97c4da51a28`；`selection_digest` `44f7723e…4b28`；`code_revision` `{commit: e2780f46dbea4d0816a6dcc8bba0725bc6182797, package_modified: false}`；`official_data` true；`evaluations_in_this_run` 1；`scored` ols_subset `allin`、`forward_sfs_k17`，metric_only `lasso`、`ridge`；`test_rows_digest` `e9ef12b5…c3d1`。**本次是 #63 run `fe76019b9af84b1e8ff46095d5ac0fb2` 的重現**；唯一一次正式評估的權威紀錄仍是 `worklog/issue-63.md` §5 |
| 條件 2：比對 | `result_digest`＝`b53ff286ae0734add8b272089aba904a1cb7f5aca444a62d356420b25dc3cfc6`（bit-exact）；對追蹤的 `e2780f4` `model_data` 深度比對 69 個不同葉節點，**全部**在 N-3 允許的欄位內（`meta.generated_at`、`meta.timing_s`、`meta.path_timing_s`、`meta.comparison_timing_s`、`baselines.pvalue_backward.timing_s`、`meta.test_evaluation` 的時刻／耗時／`code_revision`、manifest 的 `run_id`／時刻），不允許的差異 0；`meta.versions` 相同；`.js`＝`.json` |
| 結果檔 | `results/` 下 18 個檔（PNG 8、CSV 9、pickle 1；`model_data.json` 另比）與 `e2780f4` blob **逐位元相同** |
| notebook | source 全部相同；40 個 code cell 執行序號 1…40；錯誤輸出 0；「Glyph」／「missing from font」0；評估 cell 印出的 `run_id`＝本次 manifest。輸出不同的只有 cell 5、21、25、30、33（耗時）、41（`run_id`、時刻、與耗時欄位文字長度相關的檔案大小）；cell 49 的 stream 被 kernel 切成不同段數，串接後文字相同。所有內嵌 PNG（含 cell 28）與追蹤版相同 |
| 測試 | 乾淨 clone：pytest 392 passed、3 skipped（只在本機有學號設定或材料時執行的 3 項）；Node 9 pass、0 fail；`hw2.offline_scan` PASS |
| 報告建置 | `python -m hw2.report --out <scratch>`（draft；材料不在 clone 中）：成功，27 頁，`external_requests: []`，`first_draw_ms` 244 |
| 寫入範圍 | 重跑的產物只在 scratch clone；repo 的追蹤檔案沒有改動（`git status` 前後皆無追蹤檔變更） |

這次重跑與 #67 Executor 在 `1f3a8b6` 的重跑（`worklog/issue-67.md` §4–§5，我唯讀核對其 `ex67/cond7a.json` 寫於 08:11:12Z、`full_run.log` 08:11:26Z～08:12:07Z，條件 7(a) 先於完整執行）互相獨立，兩者都 bit-exact 重現 #63 的 `result_digest`。

### 4.2 解壓後 ZIP 的 dashboard（離線、`file://`）

我以 Python `zipfile` 把 `dist/<學號>_hw2.zip` 解壓到新的空目錄（路徑先檢查無 `..`），以自己寫的 CDP 腳本 `ov_sia.mjs` 啟動 headless 瀏覽器（全新 profile；`Network.emulateNetworkConditions(offline)`、`--host-resolver-rules=MAP * ~NOTFOUND`、`--proxy-server=http://127.0.0.1:9`；沒有任何本機伺服器），以 `file://` 開啟 `index.html`，記錄 `Network.requestWillBeSent` 的**每一個**請求。

| 項目 | Chrome 155.0.8059.80 | Edge 155.0.4283.62 |
| --- | --- | --- |
| 請求（含互動全程） | 7：`file` 6（`index.html`、`style.css`、`chart.umd.js`、`model_data.js`、`hw2core.js`、`app.js`）、`data` 1；**非 file／data：0**；`loadingFailed` 0 | 同左 |
| 例外／console error／log error | 0／0／0 | 0／0／0 |
| 必要區塊 (1)(2)(3)(5)(6)(9)、Test 區塊 | 全部可見；load-error 區塊隱藏；`lang="zh-Hant-TW"` | 同左 |
| 首次繪製（SR-09 (a)） | 225、228、234 ms（三次載入）；`nPoints`＝4,323＝n_test（(g)） | 228 ms；4,323 |
| 互動（(b)） | 方法 5 次、k 4 次、比較全部、預測器輸入、滾輪縮放 4 次：最大 12–13 ms | 最大約 13 ms |
| OV-2（375／768 px，mobile、DPR 2） | 8 種狀態（初始、5 個方法、k＝5、比較全部），Test 區塊有正式資料：水平溢出最大 **0 px** | — |
| 靜態掃描 | 解壓副本 `hw2.offline_scan.scan`：0 findings；我自己的 grep：`index.html`、`style.css`、`app.js`、`hw2core.js` 沒有任何 URL；`model_data.js` 只有資料集頁的超連結資料；`chart.umd.js` 只有授權註解中的 2 個網址；沒有 `fetch`、`XMLHttpRequest`、`WebSocket`、`@import` | — |

- headless 下以 `Input.dispatchMouseEvent` 送出的滾輪沒有觸發 canvas 的 `wheel` 處理器；改以 DOM `WheelEvent` 送出後記錄到 4 次 `wheel-zoom`。這是 headless 的事件派送差異；Executor 與 #67 R1 已在可見視窗以真實事件驗證滾輪、拖曳與按鈕縮放。
- **斷網方式的充分性**（Executor C-1；#67 R1 已判定足夠）：我同意。頁面在整個 session 中發出的每一個請求都被記錄，全部是 `file:` 或 `data:`；也就是說，即使網路可用，頁面也不會嘗試任何對外請求，網卡層級是否停用不改變 Brief §7 BR-04 的可觀察結果。

### 4.3 端到端資料流

資料 CSV（釘值）→ 分組切分與 fold（我獨立重推）→ fold-internal 選擇（我獨立重推）→ CV 與 winner（我獨立重算）→ alpha（training CV argmin）→ 守門開啟與單次評估（manifest；我的重現 bit-exact）→ `model_data`（`.js`＝`.json`）→ dashboard（逐筆 PI 由 Node 重算一致；離線可用）→ 報告（數字逐一相符；附錄原頁）→ ZIP（內容＝最終 subject）。整合後沒有觀察到票與票之間的介面不一致。

## 5. 範圍四：最終 subject 的 verification／audit coverage

- **實作 commit 都在受審範圍內**：`60d7fa6..e2780f4` 中每一個改動非紀錄路徑的 commit（21 個），都落在某張票 closure audit 的受審範圍內（#60 `e2d3e0b..f20d70e`；#61 `bbf0ed5..77b79f4`（R2）；#62 `6f18d8f..a2811e9`；#63 `b686b3a..1f8e7c4`；#64 `b34cc50..003b825`；#65 `bc56c06..99303c3`（R2）；#66 `752791b..d379732`；#67 `ace3958..e2780f4`），沒有未受審的實作 delta。全部票的最後一份 audit record 都是 `VERDICT: CLOSURE`。
- **audit 之後的 delta**：`e2780f4..HEAD`（含審查期間新增的 `e383a14`）只改 `doc/governance/**` 與 `doc/ticket/**`。
- **未追蹤產物與最終 subject 的對應**：ZIP 的 54 個非 PDF 項目與 `e2780f4` 的 blob 相同（12 個逐位元、42 個只差 EOL，差異 0）；兩個 PDF 以 sha256 識別（ChatGPT PDF＝收件值；報告 PDF＝`dist/report/` 的建置）。
- **最終 subject 上的 verification**：第 4 節的測試、重跑、建置與離線檢查都在 `e2780f4`（或內容相同的 ZIP）上執行。
- **Open items**：S-12 Pages 檢查（AD-3）；前票 non-blocking findings 的處置見第 9 節。

## 6. 範圍五：Spec／Tickets 對 Outcome Contract 的 traceability 與 boundary 符合性

- **Traceability**：OC（Brief @ `dff7c55c`＋CC-1、AD-1～AD-3，接受紀錄附 acceptor 原文）→ SPEC rev 5（issue #59 本文＝檔案）→ `derivation-SPEC.md` §2（OC 條款 → Spec 章節）、§4（boundary 分配）、§9.1（Spec → 票）、§9.5（覆蓋與 TK-1～TK-5）→ 票 #60～#67（本文都引用 Parent #59、Spec rev 5，並含 TR-01「Test 資料隔離」共同條款）→ 每張票的 worklog 與 audit record → `doc/ticket/tickets.md` 的狀態（全部「已結案」，引用 audit record）。DA 在 Ticket derivation 之後的補充（D-1～D-4、T-1、N-1～N-6、R-1.1～R-1.5、L／F、G-1～G-5）都以 decision record 承載並在最終 subject 上成立（第 7 節）。r4 的 #50～#56 都是 CLOSED（not planned），沒有殘留的舊 derived contract。
- **Boundary**：整合 diff 中單元外只有 root `README.md`、`CONTEXT-MAP.md` 各 +1 行（`611ad07`），與 run record §19 的擬稿逐字相同（程式比對），授權紀錄 `cbb895d`（15:50）早於修改（16:32），範圍與 acceptor 的 RB-5 原文一致；`doc/requirement/` 沒有變更；沒有 push、merge、deployment（`origin/home_work_02-regrill` 仍是 `60d7fa6`）。Brief §3.4／Spec Out of Scope 的排除項目都沒有出現（S-19）。CC-1 只擴大到 Ridge／Lasso 的一次性 metric-only 評估，實作沒有超出（p-value 對照不在 test 上評估；`test` 只有 4 個鍵）。我沒有發現需要 Design Authority 判定的 boundary 疑義或契約語義不足。

## 7. DA 高風險紀錄與派工指定的必核項目

| 項目 | 結論 | 證據 |
| --- | --- | --- |
| **A-2**（自行執行隔離測試與重算；自行比對匯出與報告、README） | **符合** | 我執行完整 pytest（含 `test_split.py`、`test_models.py::test_cv_fold_uses_only_its_training_rows`、`test_selection.py::test_changing_a_folds_validation_rows_does_not_change_that_folds_subsets`、`test_model_data_official.py::test_independent_recomputation_of_every_official_test_row`）與 Node；另以不 import `hw2` 的腳本：分割與 fold 規則重推、432 個選擇子集重推、兩個授權模型只用 training 列重擬合、5 個 CV 候選（`allin`、`forward_sfs_k17`、`backward_sfs_k17`、`lasso_path_k17`、`rfe_k18`）以各 fold 自己的子集重算 USD 指標（最大相對差 7.7e-11）、全部 4,323 列的點預測與 PI 重算（相對差 0）、`covered` 完全相等、coverage、涵蓋筆數、平均寬度、二項近似、USD 指標；報告與 README 的數字比對見 I-1 |
| **A-3**（`methods`／`baselines`／`test` 鍵的不變量；UI 不以 `test_inputs` 評估） | **符合** | 遞迴掃描 `methods`、`baselines`：名稱含 `test` 的鍵 0 個；`test` 的 `ols_subset` 鍵＝`winners.authorized_test_models`＝{`allin`, `forward_sfs_k17`}，`metric_only`＝{`ridge`, `lasso`}；`ols_subset` 都有 predicted／lower／upper／covered／coverage 等欄，`metric_only` 都沒有。UI：`Core.predict` 只在 `predictNow` 以 `readInputs` 讀自表單的原始值呼叫（`app.js:603-647`）；`test_inputs` 只在 `testRows()` 取 `row`、`id`、`actual_price` 供散佈圖繪製（`app.js:658-663`），點預測與 PI 直接取自 `MD.test[tKey]`（`app.js:673`、`:739-742`）；`hw2core.js` 的 `rowObject` 只被 `tests/js/core.test.js` 使用 |
| **A-5**（自行比對 acceptor 原始材料；sha256；沒有 mock 數值或 wireframe 截圖） | **符合** | 材料與 derived 的 sha256 與收件／#66 R1 紀錄相同；`notebooklm_v1_superseded/` 的檔名不出現在追蹤檔案、derived 檔或報告中，報告的 7 個來源與 v2 的 `sources.md` 一致。**NotebookLM**：我自己抽出 v2 docx 的文字，逐句對照報告第十一章摘要的 5 段：每個論點、數字與歸屬都在 docx 對應章節中找得到，沒有 docx 以外的論點、數字或來源；漢字 523（≥100）。**ChatGPT PDF**：我渲染並閱讀第 1、3、6、71、86、90、113、121 頁，與報告 10.1 各列所述的動作與頁碼相符（確認交付範圍、給 Claude Code 的 Grill／`/ui-ux-pro-max`／`/to-tickets` 指令、F-1 決定的起草回覆、以 GitHub 連接器讀 Issue 本文的 Tickets Review、對實作進度的起草回覆）；#66 R1 已讀完全部 121 頁。**Mock／wireframe**：`design/wireframe/mock-data.js` 的 140 個有辨識度的數字中，報告出現的 12 個全部是真實值或常數（例如 21,613、21,436、177、98001、4,287、1.96、1e-4、±0.68%、1.012、+0.33%），README 2 個（100、21613）、`index.html` 2 個（1.96、100）、`app.js` 5 個（樣式常數與色碼），`hw2core.js` 0；報告的 dashboard 截圖是建置時擷取的真實資料畫面（我看了第 9、22、24 頁：US$183,370、4,083／4,323、k 軸 1～18），沒有 wireframe 截圖 |
| **A-6**（ZIP 檔名、內容、sha256；斷網 `file://` 與零對外請求） | **符合** | ZIP 檔名＝學號＋`_hw2.zip`、唯一頂層資料夾＝學號＋`_hw2`（記憶體中比對）；sha256＝run record §20 的值；`testzip` 無錯；56 項含 Brief §8 的九類內容（主程式、報告 PDF、ChatGPT PDF、`hw2/` 24 個模組、`requirements.txt`、資料 CSV、README、`results/`、dashboard）；沒有 `tests/`、`doc/`、`.local`、`acceptor_materials`、`derived`、`__pycache__`、`.venv`、`dist`；非 PDF 項目中學號 0 次；`dist/hw2_package_manifest.json` 的 56 個 sha256 與 ZIP 項目全部相符，manifest 中沒有學號；報告 PDF 149 頁、附錄 121／121 頁渲染相同；離線與零對外請求見第 4.2 節 |
| **S-5**（學號比對，`decision-20261018-issue60-a4-student-id.md` S-2 的範圍） | **已核對、無命中** | 比對值只在記憶體中讀自 `.local/packaging.json`（10 位數字）。範圍 `origin/main`（`5be4d39`）..`HEAD`（`e383a14`），共 **90 個 commit**：每個 commit 的樹以 `git grep -F` 比對完全相同、以 `git grep -P` 比對字元之間允許空白、`_`、`.`、`,`、`/`、`-` 的變形、以 `-F` 比對全形數字：**0**（grep 錯誤 0）；同一 range 的 patch（`--binary`，含作者與 committer 欄位與訊息，約 103 MB）：完全相同 0、變形 0、前 8 碼與後 8 碼的部分比對 0；commit 物件全文 0；工作樹 1,459 個追蹤檔案：0（部分比對 0）；ref 名稱 0；GitHub issues #59～#67 的標題、本文與留言：0；本 branch 的 PR：0 個。正向對照：同一組偵測器對含該值與分隔變形的合成資料全部命中。本 record 寫入後我另以同一方法核對本檔：0 |
| **cell 28／G-5**（`decision-20261019-cell28-glyphs.md`） | **符合** | `e0be302` 是只改 cell 28（id `2fc16ee1`）一行的獨立 commit，早於重跑；條件 7(b) 的 G-5 修正版成立（第 4.1 節）；最終 notebook：全部輸出「Glyph」0、「missing from font」0、stderr 0、本機絕對路徑 0；cell 28 只有 1 個 `display_data`（`image/png`＋`text/plain`＝`<Figure size 900x450 with 1 Axes>`）；我解出 PNG 目視：圖例 5 個 ASCII 標籤可讀；我的重跑產生的 cell 28 PNG 與追蹤版相同 |
| **N-3**（單一次完整執行是追蹤版與打包版的唯一來源） | **符合** | 執行序號 1…40 連續無重複；評估 cell（41，唯一含 `gate.open(` 的格）印出的 `run_id`＝追蹤 `model_data` 的 manifest `5e74d03d6c81499f913532a551af3e6d`；追蹤 `model_data` 對 `052984b` 的差異全部在 N-3 允許欄位內（我的深度比對）；PNG、CSV、pickle 在 `ace3958..e2780f4` 沒有 git delta；ZIP notebook＝追蹤 notebook（I-8） |
| **N-5**（README 與報告的措辭） | **符合** | README 寫明唯一一次正式評估是 `fe76019b…`／`b53ff286…`、權威紀錄 `worklog/issue-63.md` §5、`meta.test_evaluation` 只記錄產生目前檔案的那次執行、重跑是 bit-exact 的重現；重跑步驟寫「重現唯一一次的 Test 評估」；報告 §6.1、附錄 A 同義 |
| **#66 F-1**（derived 文字的釘值） | **符合** | `hw2/report.py:127-134` 的 `DERIVED_REVIEWED` 三個值＝`audit/issue-66-c1-r1.md` 表頭的值＝本機三個 derived 檔的 sha256；final 建置強制核對（`check_derived_reviewed()`）；ZIP 內報告 PDF 的文字中，`notebooklm_summary.md` 5／5 段、`gpt_assist.md` 的表格儲存格 17／18 與敘述 3／3 逐字出現（唯一未比對到的一格是 PDF 文字層把「SR-12」的連字號擷取成 U+FFFE，屬擷取瑕疵） |
| **R-1.5**（`decision-20261018-issue64-standardized-reading.md`） | **符合** | 報告 §7.3 寫明 OLS 以原始尺度擬合、Ridge／Lasso 的標準化只用於其自身擬合；16 個數值欄的「每增加 1 個 training 標準差」百分比與 sd 都等於 `results/tables/final_model_coefficients.csv` 的 `pct_per_train_sd`、`train_sd`；報告、notebook（只有 3 處方法敘述）與 dashboard（`baselines.ridge`／`lasso` 無 `coef`；`app.js` 無相關參照）都沒有 Ridge／Lasso 的係數或係數讀法 |
| **D-4**（`decision-20261018-issue62-shared-subset-test-key.md`） | **符合** | (1) 6 個 winner（All-in、4 個方法、整體）的 `canonical_groups` 都等於其 `test_model_key` 項目；(2) 授權集合＝全部 `test_model_key` 的集合；(3) 授權集合內兩個鍵的子集互不相同；(4) `test` 的 `ols_subset` 鍵＝授權集合；(5) manifest `scored.ols_subset` 每個模型一次。dashboard 與報告的共用標示見 I-5 |
| **AD-3**（Pages） | **open item，NOT TESTED（pending merge），不阻擋** | S-12 |

## 8. 高風險類別

| 類別 | 核對內容 | 結果 |
| --- | --- | --- |
| **H-1** 憑證、機密與不得公開的資料 | S-5（第 7 節）；追蹤檔案與整合 diff 沒有 `.env`、`kaggle.json`、金鑰型字串；作者材料、打包設定與輸出只在 ignored 路徑（`.gitignore:13`、`:16`、`:19`）；ZIP 的非 PDF 項目沒有學號；報告 PDF 本文（第 1–28 頁）學號 0、ChatGPT 對話網址 0；作者姓名、對話網址只存在於作者的 ChatGPT PDF 與含它的報告附錄（老師要求報告含 GPT 對話，Brief §9），不在任何追蹤檔案；我的 scratch 已清理並重掃為 0 | 符合 |
| **H-2** 老師指定的名稱與格式、dashboard | `<學號>_hw2.ipynb`、`<學號>_hw2.zip`、單一頂層資料夾；notebook 六章名稱與順序（`## 1.`～`## 6.`）；報告第 2～7 章六個階段；「GPT 輔助內容」「NotebookLM 摘要」是第 10、11 章標題（逐字）；摘要 523 漢字；資料集名稱與 Kaggle 連結；附 PI 的預測圖在 notebook 5.5.1、`results/figures/eval_actual_vs_predicted_pi.png`、報告 §6.3；README 的流程與成果；dashboard 路徑 `home_work_02/index.html`、`file://` 離線、ZIP 內可用；報告與 README 沒有把 dashboard 寫成書面要求 | 符合（Pages 見 S-12；連結的時序見 F-1） |
| **H-3** 評估完整性 | 第 2 節 I-2～I-5、第 4.1 節、第 7 節 A-2、A-3、N-3、D-4 | 符合 |
| **H-4** 證據真實性與如實標示 | 第 7 節 A-5、#66 F-1、R-1.5；ACCEPTANCE 的 PASS 都有證據位置，best-effort 無環境者記 NOT TESTED，OV-1 如實寫出瀏覽器層斷網，Firefox 如實列出限制；量測值與我的量測同一量級，沒有 fixture 或 wireframe 數字 | 符合 |

## 9. 前票 non-blocking findings 的狀態（不重開；治理 §4.7）

我核對了 run record 與各 audit record 的處置。#60 F-1～F-4、#61 F-2～F-4、#62 F-1～F-3、#63 F-1～F-2、#64 F-1、#65 F-2～F-4、#66 F-1 都已由後續票解決並由後續 R1 確認（其中 #62 F-2 的 375 px 溢出，我在最終 ZIP 上重測為 0 px；#65 F-4 見 G-5；#66 F-1 見上）。仍開放、各有 owner 的是：#66 F-2（`pdf_append.py` 的輸入範圍；只在 acceptor 重新提供 ChatGPT PDF 時處理）、#67 F-1（`package.check_committed()` 缺測試；owner 之後修改打包程式的 work item）、#67 F-3（ZIP 內 README 的重跑步驟以 repo 為前提；acceptor 決定，RB-2）。#67 F-2 已由 Orchestrator 處理（`e383a14`）。我沒有新的 integration-level 證據推翻其中任何一項的 disposition。

## 10. Findings

### F-1 — Low，non-blocking：報告第九章的 GitHub Pages 與原始碼連結在合併前都是 404；報告 PDF 沒有標明「合併後才可開啟」，原始碼連結也不在 AD-3 的檢查範圍內

- **證據**：`report/report.md:296` 與 `:298` 在建置時注入 `https://yotsubamomo.github.io/aiot-classwork/home_work_02/` 與 `https://github.com/yotsubamomo/aiot-classwork/tree/main/home_work_02`（ZIP 內報告 PDF 第 20 頁）。2026-10-19 我以 `curl -L` 開啟兩者都是 **404**；`git ls-tree origin/main` 沒有 `home_work_02`。README 的 Pages 一行有「合併進 `main` 後才會更新」的註記（`README.md:40`），報告沒有；AD-3 與 ACCEPTANCE D-12 只涵蓋 Pages 網址的檢查，原始碼連結沒有被任何一項檢查涵蓋。
- **契約條款**：Brief §3.1 T-GitHub（「有 GitHub 時提供連結」；老師正文 optional 條款「需提供連結」）、§3.2（Pages 網址）、§8（報告含 dashboard 連結與截圖）；OC AD-3。
- **風險判斷**：只要合併（RB-1）先於繳交（RB-2），兩個連結都會成立，最終 subject 沒有違反任何 accepted 條款；但若 acceptor 在合併前繳交 ZIP，評分者在報告中看到的兩個連結都打不開。風險在宣告的 operating scope 之內、由 acceptor 自己保留的動作順序決定，所以判為 Low。
- **Disposition**：不延長 cycle，不需修改受審 subject。Owner：**acceptor**（安排 RB-1 合併先於 RB-2 繳交；或決定接受合併前繳交時連結暫時無效）；以及 **AD-3 的合併後 Lightweight work item**（在 Pages 檢查中一併開啟報告的原始碼連結）。若 acceptor 想在報告中加註「合併後可開啟」，那是報告文字與重新打包的修改（觸及 H-2），應作為新的 work item 處理。不需要 Design Authority：這不是契約語義不足，也不是 boundary 疑義。

### 未列為 finding 的觀察

- **O-1**：notebook 5.4 的標題與說明寫「唯一一次的 Test 評估」，沒有提到目前輸出是 #63 run 的重現。依 N-1，「每次執行只評估一次」是每次執行的不變量，這句話在每一次執行中都成立；N-5 的措辭義務只針對 README 與報告，而兩者都已寫明。不構成不實陳述，不需處理。
- **O-2**：ACCEPTANCE 的「核對的 subject」寫 `e2f391a`（ZIP 的打包 commit），之後的 `611ad07`、`8a902c2`、`e2780f4` 只改 root 兩列、ACCEPTANCE 本身與 `tests/test_report.py`，不影響任何核對結果；我在 `e2780f4` 上重做的檢查結果與該清單一致。
- **O-3**：Bindings §5 的 integration／release gate「README 的安裝與執行步驟有變動時已實際跑過」：README 的重跑步驟（venv、安裝、`run_notebook`、`pytest`、`offline_scan`、Node、報告建置）我在乾淨環境逐一執行成功；`hw2.package` 需要學號設定與材料，由 #67 Executor 在乾淨 clone 執行（我核對了其產物）。合併屬 RB-1，本 audit 不判定 release gate。

## 11. Routing

沒有需要其他 authority 的事項：沒有 blocking finding；沒有契約語義不足或 boundary 疑義需要 Design Authority；F-1 的處理屬 acceptor 自己保留的 RB-1／RB-2 動作順序，不是授權缺口。

## 12. Closure evidence

- 五個範圍：跨 Ticket invariants I-1～I-9 成立（第 2 節）；Spec AC S-1～S-20 除 S-12（Pages，AD-3 open item，NOT TESTED pending merge）外全部 PASS，Spec AC 涵蓋所分配的整個 acceptance boundary，唯一一份 derived Spec 的分配涵蓋整個 boundary（第 3 節）；整合行為：乾淨環境一次重跑 bit-exact 重現、ZIP 離線零對外請求（第 4 節）；最終 subject 的 audit 與 verification 涵蓋完整（第 5 節）；traceability 完整、boundary 符合（第 6 節）。
- 必核項目 A-2、A-3、A-5、A-6、S-5、G-5、N-3、N-5、#66 F-1、R-1.5、D-4 全部符合；AD-3 為 open item（第 7 節）。
- Blocking findings：無。Non-blocking：F-1（Low；owner acceptor 與 AD-3 的合併後 work item）。
- 受審 subject：`e2780f46dbea4d0816a6dcc8bba0725bc6182797`（整合範圍 `60d7fa6..e2780f4`），加上表頭以 sha256 識別的 ZIP、打包 notebook、報告 PDF 與 acceptor 材料／derived 檔。

VERDICT: CLOSURE
