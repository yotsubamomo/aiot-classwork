# Audit record — Issue #62，cycle 1，R1

| 欄位 | 內容 |
| --- | --- |
| Work Contract | GitHub issue #62「HW2 T3 四種特徵選擇方法 k=1…18、canonical subsets 與 CV winners」（OPEN，`ready-for-agent`；含 TR-01 修訂後的 AC、「Test 時序」「Test 資料隔離」共同條款、DA TK-3 的 AC；高風險 H-2、H-3）；Parent Spec `home_work_02/doc/spec/SPEC.md` rev 5（#59）；DA derivation `doc/governance/decisions/derivation-SPEC.md` §3 B-1、B-3、B-4，§9.1、§9.3、§9.5 TK-3、§9.6 TR-01，§11 G-2；高風險 `decisions/decision-20261018-high-risk-categories.md`（A-1～A-8）與 `decisions/decision-20261018-issue60-a4-student-id.md`（S-1～S-6；§2.2 #62 加標 H-2）；`decisions/decision-20261018-issue62-shared-subset-test-key.md`（D-1～D-4）；Outcome Contract `doc/governance/outcome-contract.md`（Brief @ `dff7c55c`＋CC-1、AD-1～AD-3）；Implementation 授權：`doc/governance/run/run-20261018-hw2-formal.md` §1 designation 第 2 點 |
| 受審 subject | branch `home_work_02-regrill`，implementation commit `a2811e9f7191a5729d15f3a20e6eac305f85fad9`（parent／BASE `6f18d8f`）；審查範圍 `6f18d8f..a2811e9`（22 個檔案，全部在 `home_work_02/` 內，沒有 `doc/` 與 `doc/requirement/` 路徑）。審查時 HEAD＝`f66e60f`；其後的 `f6298e9`、`f66e60f` 只改 `doc/governance/**` 的三個檔案（`worklog/issue-62.md`、`run/run-20261018-hw2-formal.md`、`decisions/decision-20261018-issue62-shared-subset-test-key.md`；record-only，Bindings §7），以 `git diff --stat a2811e9 HEAD` 核對。`git status --short home_work_02` 為空，工作樹的實作路徑等於 `a2811e9`。`origin/home_work_02-regrill`＝`60d7fa67`：範圍內的 commit 都還沒 push |
| Audit 種類 | **R1**（full independent audit of accepted work scope），**cycle 1**。**本 record 不是 Spec Integration Audit**（本 Spec 有多張票，不適用單 Ticket fast path；run record §4） |
| 角色 | `primary_reviewer`（definition `gov-primary-reviewer`；Bindings §3.1 R-PR mapping `claude-opus-5-5`／`xhigh`） |
| Assurance (a)：context independence（治理 §2.3；Bindings §3.7） | (1) **Independent context**：Orchestrator 以 Agent tool 派 `gov-primary-reviewer`（非 fork），從空白 context 開始；派工內容只有路徑與識別（Ticket、Spec、DA 紀錄、OC、Brief、CONTEXT、worklog、前票 audit records、branch／SHA）。派工訊息中「之後的 commit 只動 `doc/governance/**`」，以及 worklog 與 DA 紀錄中 Executor 的敘述與結論，都只當作待驗證主張，已自行核對。(2) **Verifiable binding**：見 (b) 欄。(3) **Autonomous access**：自行讀取 `gh issue view 62`、Spec、DA 紀錄、OC、Brief、CONTEXT、前票 audit records、git 歷史與 diff、全部實作、notebook 與測試；自行執行測試、在 `git archive` 複本上重跑 notebook、不 import `hw2` 的獨立重算、契約探測、mutation probes、以 CDP 驅動的 `file://` 瀏覽器檢查（第 1 節）。(4) **Self-written record**：本檔由 Reviewer 以自己的 Write 工具寫入 |
| Assurance (b)：model diversity（Bindings §5） | **Executor**：agentId `a04e1bc646c4d6912`，`agentType` `gov-executor`，觀測 `('claude-opus-5-5', 'high')` 257 則、單一元素（Reviewer 以 Bindings §3.6 的同一邏輯自行掃描 session `4bbff425-7ff9-4cdc-b64c-cc68e824e1b1` 的 subagent transcript；與 run record §11 一致），符合 O-1。（D-1～D-4 的 DA：agentId `a915f490f10d42aad`，`gov-design-authority`，`('claude-opus-5-5', 'high')` 42 則。）**本 review**：agentId `afae922d84d46d6dc`，`agentType` `gov-primary-reviewer`，撰寫本 record 前觀測 `('claude-opus-5-5', 'xhigh')` 245 則、單一元素；全程核對由派工者依 Bindings §3.6 在採用本 record 前執行。**無 model diversity**（兩者同為 `claude-opus-5-5`）。Bindings §5 不宣告 diversity 關係，不記 `diversity_lost`（A-8） |
| 日期 | 2026-10-18 |

## 1. 審查方法與環境

Reviewer 的腳本與產物都在 session scratchpad 的 `r1-62-reviewer/`（不在 repo）。審查前後 `git status --short home_work_02` 都是空的。環境：單元 `.venv`（Python 3.11.2；numpy 2.4.6、pandas 3.0.6、scikit-learn 1.9.1）、Node v24.19.0、Chrome 155（headless）。

- **工作樹測試**：`python -m pytest -q -rs -p no:cacheprovider` → **236 passed, 1 skipped**（skip：`tests/test_repo_hygiene.py:71`，學號設定未提供），103 s。`node --test tests/js/core.test.js` → 8 pass、0 fail、3 skip（fixture 項目）；以 Reviewer 自己產生的 fixture（`HW2_FIXTURE_MODEL_DATA`）執行 → 11 pass、0 fail、0 skip。`python -m hw2.offline_scan` → `scanned 6 files: PASS (0 findings)`。
- **Notebook 重跑**：`git archive a2811e9 home_work_02` 匯出到 scratchpad，刪除 `results/model_data.json`、`assets/model_data.js`、`results/split/`，以單元 `.venv` 執行 `python -m hw2.run_notebook` → `executed hw2.ipynb in 64.8 s`。重新產生的 `model_data` 與 commit 中的版本逐鍵比較，只有 `meta.generated_at`、`meta.timing_s` 的 8 個時間值與 `meta.path_timing_s` 的時間值不同；`.js` 物件等於 `.json`；`split_assignment.csv` sha256 `901a6127…a563d` 等於 commit 的 blob。這次重跑的路徑時間（合計）：Forward 17.77 s、Backward 18.41 s、RFE 15.60 s、Lasso 7.67 s。
- **Reviewer 的獨立重算（A-2；`indep62.py`，不 import `hw2`）**：從只含識別的 `split_assignment.csv` 取得 test 列位置，以 `pd.read_csv(skiprows=…)` 在解析時跳過，只讀到 17,290 筆 training 列。依 Spec 文字自己實作：encoding（基準日 2014-01-01、整修旗標與有效年份、zipcode 類別取自給定列並以排序第一類為基準、`sqft_basement` 不進模型）；Forward／Backward SFS 以含截距的 OLS 直接 `lstsq` 的 RSS（不用 Gram）；RFE 以 sd(X_g·β_g)；Lasso 以給定列上標準化數值欄（zipcode 維持 0／1）後的 `lars_path(method="lasso")`，group 內任一欄首次非零即進入；平手依 canonical order；fold 路徑只用 `fold != f` 的列；分組 CV 以 USD 計分；canonical OLS 在整個 training set 擬合。結果：
  - 子集：4 方法 × 18 個 k ×（canonical＋5 個 fold）＝432 個子集，與 `model_data` **0 筆不符**；各步的準則值沒有任何接近平手的情形（相對差 ≤ 1e-7 的次數為 0）。
  - CV：4×18×5×4＝1,440 個逐折指標，最大相對差 **1.1e-10**。
  - Canonical fit（72 個）：rank 全部相同；係數最大相對差 4.5e-9；s² 最大相對差 1.7e-15；log 尺度 Adjusted R² 最大絕對差 3.3e-16。
  - Winners：Forward k=17（US$158,098.26）、Backward k=17（US$158,098.26）、RFE k=18（US$158,154.31）、Lasso k=17（US$157,253.88）；整體 `lasso_path_k17`；與追蹤的 `winners` 完全相同。各方法最佳與次佳的差距：56.05、56.05、511.26、900.43 USD。
  - 限制：Lasso 的 LARS 數值與 subject 使用同一個 `sklearn.linear_model.lars_path`，因此 LARS 本身不是獨立實作；標準化、group 進入規則與排序是獨立寫的。
  - 共用模型：`forward_sfs_k17`、`backward_sfs_k17`、`lasso_path_k17` 的 canonical subset 相同（18 個 group 去掉 `sqft_lot15`）；`rfe_k18` 的 canonical subset 是全部 18 個 group，等於 `allin`（D-1）。
- **契約探測**（subject 的 `contract.validate_model_data`；對 Reviewer 的 fixture 與追蹤的正式 `model_data` 各做竄改）：P1 某方法 winner 的模型從授權清單與 `test` 移除；P2 非 winner 被授權並評分；P3 `test.allin.model_key` 錯誤；P4 只有 ridge 的 `metric_only`；P5 整體 winner 的 `test_model_key` 指向不同模型；P6 共用模型以自己的鍵再評估一次（讀法 K）；P7 `winners.allin.test_model_key` 被改；P8 `rfe_k18` 改以自己的鍵評估；P9 整體 winner 改標為同一模型的 `backward_sfs_k17`；P10 `lasso_path_k17` 的 fold 0 子集被換；P11 清除 `lasso_path_k17` 的 `is_method_winner`；P12 `methods` 內放入 test 欄位。**12 項全部被拒**，訊息與預期相符。
- **Mutation probes**（18 個；各在 scratchpad 的複本上以完整 suite 執行（`-x`，不含需要 git 工作樹的 hygiene 測試；baseline 221 passed））：S1 fold 路徑看到全部 training 列、S2 Lasso 平手不依 canonical、S3 Forward 平手取後者、S4 RFE 移除最重要者、S5 Gram 不置中（沒有截距）、S6 canonical 路徑只用 fold 0 的訓練列、W1 共用模型不去重、W2 方法 winner 平手取大 k、W4 整體 winner 平手順序反轉、F2 重新允許截斷 fold 子集、C1 契約不核對聯集、C2 契約不重算方法 winner、C3 契約不核對 `meta.cv.n_folds`、C4 契約不核對巢狀、J1 Test 區塊保留舊數字、J2 `testEntryKey` 忽略 `test_model_key`、E1 匯出省略路徑時間：**17 個被偵測**。**C5（契約不核對「授權集合中同一模型出現兩次」）存活**，見 F-3。另以只跑合成資料單元測試的方式確認：S1、S6 由 `test_selection.py` 的選擇邊界與 canonical 測試直接偵測（不依賴正式資料的重算測試），S4、S5、F2 亦由 `test_selection.py` 偵測，W1、W2、W4 由 `test_models.py` 偵測。
- **Dashboard（`file://`，CDP）**：headless Chrome 155，`--host-resolver-rules="MAP * ~NOTFOUND"`，scratchpad 內的全新 profile。
  - **正式頁面**（`git archive` 複本，`model_data` 換回追蹤版本）：沒有例外或 console error；請求只有 6 個本機檔，外加 Chrome 自己的日期選擇器 `data:image/svg+xml`。方法選單五項；All-in 顯示「k = 18（固定）」狀態列與說明，沒有 k 按鈕（UI 決策 4）；路徑方法 18 個 k 按鈕，winner 綠點在 Forward／Backward／Lasso k=17、RFE k=18；指標 vs k 圖有四條路徑、All-in 參考線、「目前選取」；改選 R² 後摘要改為 CV R²；「比較全部方法」顯示 5 列（All-in＋四個方法 winner）、標「訓練 CV（USD）」、Lasso 列標「整體 CV winner」；選 Forward k=3 時 KPI 與預測器（3 個輸入）換成 k=3。Test 區塊顯示「Test 評估尚未執行」，`#test-body` 隱藏。Test 區塊標籤：Backward「Backward SFS · k = 17（與 Forward SFS · k = 17 為同一模型，Test 只評估一次）」＋「與整體 CV winner 為同一模型」；RFE「RFE · k = 18（與 All-in baseline · k = 18 為同一模型，Test 只評估一次）」；Lasso「Lasso 路徑排序 · k = 17（與 Forward SFS · k = 17 為同一模型，Test 只評估一次）」＋「整體 CV winner」（D-2：代表鍵 Forward 沒有被當成 Lasso 的身分）；Forward「Forward SFS · k = 17」＋「與整體 CV winner 為同一模型」；All-in「All-in baseline · k = 18」（見 F-1）。1440／768／375 px（含比較表展開）水平溢出都是 0。
  - **Fixture 頁面**（以 subject 的 `python -m hw2.fixture` 在單元以外產生；n_test 4,291；注入 `rfe_k07` invalid）：沒有例外或 console error；只請求本機檔。RFE 的 k=7 為紅斜紋、圖上叉號；選 k=7 時 KPI 區清空、`status-box` 顯示「invalid 候選：fold_rank_deficient；沒有可比較的 CV 指標。」、預測器停用並顯示「invalid 候選（fold_rank_deficient）：不提供即時預測。」（UI 決策 2）、黃色提示說明 Test 區塊展示的是 RFE · k = 9（BR-01 第 5 點）。Backward 的 Test KPI 以「Backward SFS · k = 7」標示、數值等於 `test.forward_sfs_k07`。`HW2_PERF.firstDraw` 216.4 ms（4,291 點）。**375 px 時有 44 px 水平溢出**（見 F-2）。
  - **#61 F-3 的 dashboard 部分**：把 fixture 的 `test.rfe_k09` 刪除後載入：All-in 有數字 → 切到 RFE 時 `#test-body` 隱藏、Test KPI 與涵蓋統計清空、提示「Test 評估中沒有這個方法 CV winner 的結果，因此不顯示任何 Test 數值。」→ 再切到 Lasso 時數字恢復。
  - 截圖（scratchpad `shot_fx_rfe_invalid.png`、`shot_off_compare.png`）目視：綠點、紅斜紋、圓環、叉號、選取圈、圖例與比較表標示都可辨識。
- **A-4 掃描**：見第 3 節 H-1。
- **Reviewer 自身的 test 隔離**：我沒有讀取或推導任何正式 test 列的特徵或 `price`。完整 CSV 只由 subject 自己的程式解析（結構檢查與分割，#60 AC-4 允許；以及 subject 自己的測試）。

## 2. Acceptance criteria 逐條判定

| AC（#62） | 判定 | 證據 |
| --- | --- | --- |
| AC-1 Spec rev 5「分割與交叉驗證」的選擇邊界、「特徵選擇與模型」、三類秩不足語義（SR-04／SR-10）；每個 (方法, k) 的 canonical groups 數與各 fold groups 數都等於 k | **PASS** | `hw2/selection.py:293-312`（`method_paths`）：fold f 的路徑只用 `training[training["fold"] != f]`，canonical 用整個 training set；`check_path` 要求 k 個 group、每步恰變一個。`GroupGram`／`lasso_entry` 的前處理只在給定列上 fit。`models.evaluate_candidate`（`models.py:172-231`）以各 fold 自己的子集在 fold 訓練列擬合、驗證列計分，`len(fold_groups)` 不等於 fold 數或子集大小不等於 k 時拒絕（`:187-192`）。秩不足：選擇以最小範數解計算，不停止也不跳過步驟；fold／canonical 秩不足走 #61 的 invalid 語義；All-in 秩不足、方法沒有有效候選、整體 winner 無法決定為 `ExperimentFailure`。Reviewer 的獨立重算 432 個子集 0 不符、1,440 個 CV 值 ≤ 1.1e-10；契約 `validate_entry`／`validate_methods` 核對 k、canonical order、巢狀與 `n_folds` |
| AC-2 pytest 次 seam「特徵選擇」「選擇邊界」「無效候選」「選模」 | **PASS**（F-3 為 non-blocking） | `tests/test_selection.py`：每步恰變一個 group；RSS 準則對直接 OLS；RFE 重要度；`_pick` 與 Lasso 平手依 canonical order；從未進入的 group 排最後；重複欄的平手；常數 group 不停止也不跳過；**改動 fold 0 驗證列的價格與特徵，fold 0 的子集序列不變**（四個方法；呼叫點同時拿到訓練列與驗證列）；canonical 只由整個 training set 決定；候選使用各 fold 自己的子集；fold 子集數錯誤被拒。`tests/test_models.py`：fold 秩不足→invalid 不勝出；canonical 秩不足→invalid、沒有 `fit`、流程繼續；方法全部無效→停止；All-in 共線→停止；整體 winner 無法決定→停止；方法 winner 平手取小 k；整體平手依方法順序；授權集合推導（含 k=18 與 All-in 共用、兩方法同子集共用）。Mutants S1–S6、W1、W2、W4、F2 都被偵測 |
| AC-3 `winners` 的各方法 winner 與整體 winner 不含 Ridge／Lasso（G-2，以測試斷言） | **PASS** | `test_model_data_official.py::test_winners_are_complete_and_never_metric_only`、`test_models.py::test_winners_never_include_ridge_or_lasso`（另斷言 `ridge` 當路徑方法被拒）、`test_methods_contract.py` 的 G-2 斷言與 tamper、Node `checkPaths`。契約 `validate_winners` 拒絕非路徑方法的 method winner（`contract.py` 「G-2」訊息） |
| AC-4 執行時間：四種方法各自的路徑計算時間（5 fold＋整個 training set）記入 `meta` 與 worklog；不可接受時依 Q34 停止回報 | **PASS** | `meta.path_timing_s`（每方法 `selection_folds`×5、`selection_training`、`selection`、`evaluation`、`total`）與 `meta.timing_s.path_<方法>`；worklog §4 的兩次量測表與判斷；notebook 4.2 的時間表與追蹤的 `meta` 一致。Reviewer 重跑：整本 notebook 64.8 s，四方法合計 7.7–18.4 s。沒有縮小 k 範圍或方法集合 |
| AC-5 Dashboard：UI 決策 4、winner／invalid 標示、指標下拉、比較全部疊圖＋各方法 winner 比較表、BR-01 第 5 點提示；`invalid` 時預測器停用（UI 決策 2） | **PASS**（F-1、F-2 為 non-blocking） | 第 1 節 CDP 檢查與截圖。指標 vs k 圖與比較表只讀 `cv`（以及 log 尺度 Adjusted R² 的 `fit`），不讀 `MD.test` 或 `test_inputs`（`test_dashboard_static.py::test_k_chart_and_comparison_table_read_cv_only`；Reviewer 讀 `app.js` 確認），兩張卡都標「訓練 CV（USD）」。Ridge／Lasso 參考線與比較表的 Test 欄屬 #63（derivation §9.1、§11 G-4），不是本票 AC |
| AC-6 Node test：每個方法 k=1…18、winner 與契約一致、`invalid` 不會被選為 winner | **PASS** | `tests/js/core.test.js` `checkPaths`（正式與 fixture）、fixture 的 `testEntryKey` 指向授權集合中同一 canonical subset、注入的 invalid 不勝出且 `canPredict` 為 false；Reviewer 執行 8／8（無 fixture）、11／11（Reviewer 的 fixture）；J2 被偵測 |
| AC-7 正式 test 列仍未載入、G-3 守門保持關閉；Test 區塊與授權集合的分層只以 fixture 驗證；追蹤的正式 `model_data` 不含 `test` 與 `test_inputs` 列（worklog 記錄） | **PASS** | 追蹤的 `model_data` 區段＝{meta, preprocess, inputs, test_inputs, methods, baselines, winners}，沒有 `test`，`test_inputs.written` false、0 列（Reviewer 自行核對）；notebook 5.3 輸出 `gate: {'state': 'closed', 'official_data': True, 'official_gate_enabled': False}` 與兩次拒絕；`a2811e9` 的 diff 中沒有任何新增的 `_read_csv`、`load_test_rows` 呼叫或對 `OFFICIAL_TEST_GATE_ENABLED` 的修改；選擇與評估只接收 `prepared.training`；fixture 的 `model_data` 只寫到單元以外。Worklog §3.5 有記錄 |
| AC-8（DA TK-3）notebook 寫明 CV winner 的 CV 分數帶有選擇偏誤、test 才是獨立估計 | **PASS** | Notebook §5.1（cell 29）：「選擇偏誤……樂觀偏誤，不是它表現的不偏估計；全部選擇凍結之後的 Test 評估才是 CV winner 表現的獨立估計」，並說明 CV 估計的是「方法在 k 下的程序」；`test_notebook_structure.py::test_modeling_and_evaluation_state_the_selection_protocol_and_its_bias`。報告版屬 #65 |
| What to build：四方法 fold-internal＋canonical、三類秩不足、winners、時間、`methods`／`winners` 匯出、dashboard 路徑檢視；本票不執行正式 Test 評估 | **PASS** | 第 1 節；`methods` 每個項目的鍵恰為 `ENTRY_KEYS`（`model_key`、`method`、`k`、`canonical_groups`、`fold_groups`、`folds_agree`、`status`、`cv`、`fit`、`is_method_winner`） |

## 3. 高風險類別核對（A-1）

| 類別 | 核對內容 | 結果 |
| --- | --- | --- |
| **H-3**（票已標示） | A-2：Reviewer 自己執行全部 pytest（含 `test_split.py` 分組隔離、`test_selection.py` 選擇邊界）與 Node test；不 import `hw2` 的獨立重算從 training 列重現全部 432 個子集、1,440 個逐折 CV 值、72 個 canonical fit 與 winners（第 1 節）。PI／coverage 的逐筆重算由既有的 `test_test_section.py`（fixture，全部 `ols_subset` × 全部 test 列）與 Node 的 fixture 項目在 Reviewer 的執行中通過；本票沒有改動 PI 或 test 評估的程式。README 沒有引用匯出數字；worklog 的正式結果數字（四個 winner 的 CV RMSE、授權集合 `['allin', 'forward_sfs_k17']`）與匯出及 Reviewer 的重算相同。A-3：追蹤的 `methods`、`baselines` 沒有 test 欄位（`test_field_paths` 與 P12）；`test` 尚不存在；fixture 的 `test` 中 `ols_subset` 鍵＝授權集合；dashboard UI 不以 `test_inputs` 評估任何模型（`Core.predict` 唯一呼叫點使用使用者輸入，`app.js:498`；`test_inputs` 只供繪圖與計數）。選擇只在 training 內（TR-01；AC-7）。D-4 不變量見第 5 節 | PASS；F-1、F-3 non-blocking |
| **H-2**（票已標示；DA S 紀錄 §2.2） | notebook 六章的名稱與順序在 `6f18d8f` 與 `a2811e9` 完全相同（`## 1. Business Understanding` … `## 6. Deployment`）；`python -m hw2.offline_scan` PASS；`index.html` 的 `<script>`／`<link>` 仍只有本機的 `assets/style.css`、`assets/vendor/chart.umd.js`、`assets/model_data.js`、`assets/hw2core.js`、`assets/app.js`，`assets/vendor/` 沒有變更，沒有新增任何對外資源；`file://` 在所有主機名稱都無法解析時正常載入，只請求本機檔；`home_work_02/index.html` 路徑不變；zh-TW 標示。375 px 的版面見 F-2（Test 區塊，自 #61 起；不是本票引入） | PASS；F-2 non-blocking |
| **H-1**（A-4，適用全部票） | `git ls-tree -r a2811e9 -- home_work_02` 與 HEAD：唯一的 PDF 是老師文件 SRC-3（`doc/requirement/`），沒有 `.zip`、`.env`、`kaggle.json`、`.local/`、`acceptor_materials/`、`dist/`；範圍內新增的行（不含匯出資料檔與 notebook）沒有 `KAGGLE_KEY`／`KAGGLE_USERNAME`／`api key`／`secret`／`password`／`token`；沒有單元以外或 `doc/requirement/` 的變更。**學號**：`.local/packaging.json` 不存在，A-4 的實際值比對無法執行，依 S-1 記為 **NOT VERIFIED**，不是 PASS。S-1 替代證據（Reviewer 以腳本取得；所有數字在輸出前都先遮罩，沒有印出任何疑似值），範圍 `6f18d8f..HEAD`（3 個 commit）：新增行中 7 位以上的數字串都已歸類——758,317 個是含小數點或指數的資料值（`model_data` 與 notebook 輸出的浮點數）、2 個是 hex hash、8 個是 YYYYMMDD 日期（紀錄檔名中的日期），其餘 4 個是 `model_data.inputs` 中一個數值特徵的 training 最大值（`.json` 與 `.js` 各一次）與 notebook 輸出的兩個檔案位元組數；「學號」在新增行出現 6 次，全部在 worklog 的敘述用詞中（S-1、A-4、skip 原因），實作 commit 中沒有出現；3 個 commit message 中只有 1 個 8 位數字串，為日期形態，沒有「學號」。S-4 尚未觸發（學號設定不存在） | 憑證與材料 PASS；學號 NOT VERIFIED（S-1） |
| H-4 | 未觸及：沒有報告或 acceptor 材料；`app.js`、`hw2core.js`、`index.html`、`hw2/*.py` 沒有引用 `design/`、wireframe 或 mock；fixture 數值只在單元以外，頁面顯示 fixture 警告（DA §9.3 條件 4） | 不適用 |

## 4. 前票 follow-up（owner＝#62）

- **#60 R1 F-2**（「改動驗證列」的測試應作用在同時拿到訓練列與驗證列的呼叫點）：**已處理**。`test_selection.py::test_changing_a_folds_validation_rows_does_not_change_that_folds_subsets` 呼叫 `selection.method_paths(training, method)`（拿到全部 fold 的列），改動 fold 0 的價格與四個特徵，斷言 fold 0 的子集序列不變，並以 sanity 斷言確認改動確實影響其他 fold 或 canonical。Mutant S1 只跑 `test_selection.py` 時 8 個測試失敗。
- **#61 R1 F-2**（`fold_groups` 被靜默截斷；契約不核對 fold 數）：**已處理**。`models.py:187-192` 拒絕；`validate_entry` 核對 `cv.n_folds`＝`meta.cv.n_folds`、`fold_groups` 數與 fold 記錄的 groups（`contract.py:230-240`）。Mutants F2、C3 被偵測。
- **#61 R1 F-3**（授權清單＝聯集；`test.<key>.model_key`；dashboard 顯示舊數字）：**已處理**。`validate_winners` 核對聯集（共用模型一次，`contract.py:385`）與每個 winner 和它的 test 模型是同一個 canonical subset；`validate_test` 核對 `model_key`（`:415-417`）；`renderTest` 在沒有 test 項目時隱藏並清空（Reviewer 以刪除 `test.rfe_k09` 的 fixture 實測，第 1 節）。Mutants C1、J1 被偵測；契約探測 P1、P2、P3 被拒。
- #61 R1 F-4（正式資料的單次載入守門；owner #63）不在本票範圍；本票沒有改動 `testgate.py`。

## 5. DA decision D-1～D-4 與 Executor 的 concerns

- **D-4**（DA 要求 R1 核對）：(1) 每個 winner 的 `canonical_groups` 等於其 `test_model_key` 項目的 `canonical_groups`——正式資料成立（`backward_sfs_k17`、`lasso_path_k17`→`forward_sfs_k17`；`rfe_k18`→`allin`），契約檢查（`contract.py:383-384`；P5、P8 被拒）。(2) 授權集合＝全部 `test_model_key` 的集合——成立（`['allin', 'forward_sfs_k17']`），契約檢查（`:385`；P1、P2、P7 被拒；C1 被偵測）。(3) 授權集合內沒有兩個鍵的 canonical subset 相同——成立，契約檢查（`:388-390`；P6 被拒），但沒有測試守住這項檢查（C5 存活，F-3）。(4) `test` 的 `ols_subset` 鍵＝授權集合——`validate_test` 檢查，fixture 成立。(5) 「每個模型只評估一次」以 D-1 的模型為單位——`testgate.ols_models_for`（`testgate.py:213-222`）只依去重後的授權清單建立評估對象。
- **D-2 的標示**：每個 winner 保留自己的方法、k、`model_key`、CV 指標與 winner 標記（`winners.method_winners`、各項目的 `is_method_winner`）；dashboard Test 區塊以選取方法的 winner 身分標示，數值經 `test_model_key` 取得；整體 winner 以「Lasso 路徑排序 · k = 17」與「整體 CV winner」呈現，沒有被呈現為 Forward SFS（第 1 節）。不足之處：代表鍵本身所屬的 winner（Forward SFS k=17、All-in）沒有寫出與哪些 winner 共用模型，見 F-1。共用模型的不同 CV RMSE：指標 vs k 圖的說明寫明「CV 指標估計的是『方法在 k 下的程序』，不是 canonical subset 本身」，沒有寫成同一個擬合模型有兩個 CV 分數。
- **C-1**（共用模型的解讀）：已由 DA D-1～D-4 結案；實作與 D-1 一致（第 1 節、本節）。
- **C-2**（SFS 的步驟準則採 in-sample RSS）：Spec 與 Brief 沒有規定 SFS 的步驟準則（Brief §12 把彙總規則等列為 HOW；Spec 只規定 group 單位、每步恰變一個 group、平手依 canonical order，以及 k 由 CV 決定），所以這是 Executor 的 HOW，不是契約缺口，也不構成 finding。準則已寫入 notebook 4.2 與 `meta.selection`。附帶的觀察：以 RSS 比較不同欄數的 group 時，多欄的 group（zipcode 69 欄）較容易先被加入；這是準則本身的性質，k 依契約計算 group 數，不影響正確性。報告（#65）描述方法時應如實寫出準則。
- **C-3**（All-in 有效時路徑候選不可能 invalid）：成立。同一批列上，任何子集的設計矩陣欄位都是 All-in 設計矩陣欄位的子集（zipcode 類別取自同一批列），All-in 滿秩則任何欄位子集也滿秩。正式資料沒有 invalid 候選（notebook 4.2 輸出 `invalid candidates: none`）；invalid 的呈現與勝出規則以 fixture 注入與單元測試驗證，Reviewer 已實測。
- **C-4**（`model_data` 8.7 MB）：已知；fixture 首次繪製 216 ms（Reviewer），遠低於 3 s。OV-6 正式量測屬 #67。

## 6. Findings

### F-1 — D-2 的共用模型說明對「代表鍵」本身的 winner 不完整

- **Severity**：Low。**Blocking**：否。觸及 H-3（BR-01 標示），A-7 適用。
- **證據**：`assets/app.js:526-527`：Test 區塊只有在 `tKey !== key`（winner 的 test 項目不是自己的鍵）時才附「（與 … 為同一模型，Test 只評估一次）」；`:532-533` 的標籤只區分「整體 CV winner」與「與整體 CV winner 為同一模型」。`sharedWith`（`:201`）同樣只從共用者一方回報。CDP 實測（正式資料）：選 Forward SFS 時，Test 區塊為「Forward SFS · k = 17」＋「與整體 CV winner 為同一模型」，沒有寫出 Backward SFS k=17 也是同一模型，也沒有「Test 只評估一次」；選 All-in 時為「All-in baseline · k = 18」＋「All-in baseline」，沒有寫出 RFE k=18 是同一模型。比較表（`app.js:377`）的「備註」欄對 Forward SFS 與 All-in 兩列也沒有共用說明。Fixture 頁面相同（Forward SFS k=7 是整體 winner，與 Backward k=7 共用，Test 區塊未提及）。
- **契約條款**：DA `decision-20261018-issue62-shared-subset-test-key.md` D-2 第 2 點：「任何呈現 winner 的 test 結果時（dashboard 的 Test 區塊與比較表、……），都以該 winner 自己的身分標示，……並明確寫出它與哪些 winner 是同一模型、Test 只評估一次」。
- **風險判斷**：共用者一方的標示正確，沒有任何身分被錯標，也沒有誤導；整體關係可以從比較表各列拼出。本票的正式 Test 區塊沒有任何 test 數值（「Test 評估尚未執行」），所以目前沒有呈現任何正式的 winner test 結果；這項要求在 #63 寫出正式 `test` 並加上比較表 Test 欄時才實際生效。因此判為 Low。DA §6 對 `a2811e9` 的標示作過「符合 D-1、D-2」的設計層級判斷；本 finding 只針對 D-2 第 2 點的字面完整性。
- **Disposition**：本票不需修改。Owner＝**#63**（第一次呈現正式 winner test 結果；DA §7 已要求 #63 的比較表 Test 欄「標明共用（D-2）」）：Test 區塊與比較表對代表鍵所屬的 winner 也列出共用的 winner（例如「與 Backward SFS · k = 17、Lasso 路徑排序 · k = 17 為同一模型，Test 只評估一次」）。若 Executor 或 Orchestrator 認為 DA §6 的判斷已涵蓋這種呈現，屬 D-2 的解讀，交 **Design Authority**。

### F-2 — Test 區塊在 375 px 有 44 px 水平溢出（自 #61 起；worklog V-10 的 375 px 主張未能重現）

- **Severity**：Medium。**Blocking**：否（不是本票引入，也不在本票 AC 內；理由見下）。觸及 H-2，A-7 適用。
- **證據**：
  - Reviewer 的 fixture 頁面（`a2811e9` 的 `python -m hw2.fixture`）以 CDP `Emulation.setDeviceMetricsOverride` 375 px：`scrollWidth − clientWidth`＝**44 px**，在 All-in、四個方法、invalid 候選、非 winner 等 8 種狀態都一樣；不開 mobile 模擬時（視窗 360 CSS px）為 59 px。超出視窗的元素都在 Test 區塊內：`.testzone__head`、`#test-source`、`#test-body`、`#kpi-test`、各 `.kpi--test`、`.scatter-wrap`、`#covstats`、`#coverage-note`（寬 381 px，右緣 419 px）。`.testzone`（`assets/style.css:208`）與 `#test-body` 是 `display: grid`，沒有指定 `grid-template-columns`，隱含的 `auto` 欄依子項目的 min-content 撐到 380.656 px，大於 `.testzone` 的內容寬度。#62 對 `.stack` 加了 `minmax(0, 1fr)`，但 Test 區塊的這兩個 grid 沒有。
  - 正式頁面目前是 0：Test 區塊沒有資料、`#test-body` 隱藏。
  - **不是本票引入**：以 base `6f18d8f`（#61 結案狀態）的 `hw2.fixture` 產生頁面，同樣在 375 px 溢出 44 px；`a2811e9` 沒有修改這部分的 CSS。
  - Worklog §4 V-10 寫「正式與 fixture 兩個頁面在 1440／768／375 px 都沒有……水平溢出」，fixture 頁面 375 px 的部分 Reviewer 無法重現（不同狀態、mobile 與非 mobile 模擬都溢出）。Self-verification 的這項主張不能作為 OV-2 的證據。
- **契約條款**：OC §4 AD-1（acceptor 原文）OV-2「Required gate：Chrome DevTools 375 px／768 px 無水平溢出」；Spec rev 5 人工檢查表 OV-2。
- **為何不是 blocking**：#62 的 AC 不含 OV-2；OV-2 是 #67 的 gate（derivation §9.1）；這個缺陷在 #61 已存在、本票沒有擴大；正式頁面要到 #63 寫出正式 `test` 後才會出現。判為 Medium 是因為它會讓一個 Required gate 失敗，且 worklog 的錯誤主張可能讓後續誤以為已驗證。
- **Disposition**：Owner＝**#63**（第一次讓正式 Test 區塊有內容，且會修改 Test 區塊與比較表）：修正 Test 區塊在窄螢幕的 grid 欄寬，並以「Test 區塊有資料」的狀態在 375／768 px 量測。**#67** 的 OV-2 量測必須在 Test 區塊有資料的狀態下進行。

### F-3 — 契約檢查「授權集合中同一模型不得出現兩次」（D-4 第 3 點）沒有測試守住

- **Severity**：Low。**Blocking**：否。觸及 H-3，A-7 適用。
- **證據**：`hw2/contract.py:388-390` 的檢查存在且有效（Reviewer 探測 P6：讓 `backward_sfs_k07` 以自己的鍵再評估一次（讀法 K），被以「the authorized set scores one model (canonical subset) twice」拒絕）。但 mutant C5（把這項檢查改成 `if False:`）在完整 suite 下**存活**（221 passed）：`test_methods_contract.py` 的 15 種 tamper 都會先被聯集或其他檢查攔下，沒有一種只違反這一條。`determine_winners` 的去重本身有測試（W1 被 `test_models.py` 偵測），所以目前實際匯出的授權集合是正確的。
- **契約條款**：DA D-4 第 3 點；D-1「每個模型只在一個代表鍵下評估一次」；G-3（以 D-1 的模型為單位）。
- **Disposition**：本票不需修改。Owner＝**#63**（第一次寫出正式 `test`，也是 D-4 第 4、5 點的負責票）：在 `test_methods_contract.py` 加一個 tamper——某個共用模型的 winner 改以自己的鍵授權並評分（如 P6）——斷言被拒。

## 7. Routing（需要其他 authority）

- 目前沒有必要的 routing。F-1 若對 D-2 的解讀有爭議，交 **Design Authority**（見 F-1）。
- 學號（A-4）：依 S-1 記 NOT VERIFIED，不是本票結案的條件。S-2～S-5 仍是 run record §8 的 open 項目；範圍內的 commit 都還沒 push（S-3 適用）。

## 8. 其他核對與備註（不是 finding）

- **Worklog 的主張**：V-1（236／1）、V-2～V-9、V-13（Reviewer 另做 18 個 mutants）、V-14、時間量測表、正式結果、Executor binding 則數都已由 Reviewer 重現或核對。V-10 的 375 px 部分見 F-2；其餘 V-10 項目（無例外、只請求本機檔、k 格子、winner 綠點、All-in 狀態列、比較全部、非 winner 提示、invalid 呈現）已重現。V-11 的截圖檢查以 Reviewer 自己的截圖取代；正式頁面在 375 px 時比較表只在表格容器內捲動（頁面溢出 0），與 V-11 一致。V-12 的 OV-6 方法驗證只重現了 firstDraw（216 ms）。
- **Invalid 候選的「全訓練集擬合」卡**：fixture 中注入的 `rfe_k07` 是 fold 層級 invalid、canonical fit 有效，dashboard 仍顯示它的 log 尺度 R² 等擬合統計，預測器停用。Spec 允許 fold 層級 invalid 的項目保有 `fit`（只有 `canonical_rank_deficient` 沒有 `fit`），UI 決策 2 只要求顯示原因並停用預測，所以不構成 finding；正式資料依 C-3 不會出現這種情形。
- **README**：Spec「特徵選擇與模型」要求路徑時間寫入匯出中繼資料「與 README」；本票的 README 寫明時間的位置並說明不抄寫數字（與 Brief US-37「README 的數字都引自匯出結果」一致）；本票 AC 只要求 `meta` 與 worklog。README 的最終內容屬 #65。
- **Ridge／Lasso**：比較全部的 Ridge／Lasso 參考線、比較表的 Test 欄與 Ridge／Lasso test 指標都屬 #63（derivation §9.1、§11 G-4），本票沒有實作，符合分配。
- **範圍與 git**：沒有單元目錄以外的變更，沒有修改 `doc/requirement/`（RB-5）。`requirements.txt`、`.gitignore`、`assets/vendor/` 沒有變更。Commit message 符合 git 規則（`[Modify] –` 加上 `[Additions]`／`[Modification]`／`[Fix]`），沒有 Claude 標記；未 push。

## 9. 結論

- Blocking findings：無。
- Non-blocking findings：F-1（Low，owner #63）、F-2（Medium，owner #63；#67 OV-2 量測須含 Test 區塊有資料的狀態）、F-3（Low，owner #63）。
- 前票 follow-up：#60 R1 F-2、#61 R1 F-2、#61 R1 F-3 已處理。
- DA D-4：(1)(2)(4)(5) 成立並有測試；(3) 成立，測試缺口見 F-3。
- Routing：無（F-1 若有解讀爭議，交 Design Authority）。
- A-4 學號：NOT VERIFIED（S-1），不是本票結案的條件。

VERDICT: CLOSURE
