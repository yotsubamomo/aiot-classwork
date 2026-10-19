# Worklog — issue #62（HW2 T3 四種特徵選擇方法 k=1…18、canonical subsets 與 CV winners）

- **Work item**：GitHub issue [#62](https://github.com/yotsubamomo/aiot-classwork/issues/62)，run `run-20261018-hw2-formal`（Formal，並行度 1）。
- **狀態**：實作與 self-verification 完成，待 Orchestrator 核對 binding 並派 R1（本檔不代表 audit 或 closure）。
- **Subject**：branch `home_work_02-regrill`，base `6f18d8f`；**實作 commit `a2811e9f7191a5729d15f3a20e6eac305f85fad9`**（本機，未 push）。本檔另以 record-only commit 加在其後（Bindings §7）。

## 1. Contract reference

| 項目 | 內容 |
| --- | --- |
| Ticket | #62（OPEN，`ready-for-agent`；含 TR-01 修訂後的 AC、「Test 時序」「Test 資料隔離」共同條款、DA TK-3 的 AC；高風險 H-2、H-3）；索引 `doc/ticket/tickets.md` |
| Spec | `doc/spec/SPEC.md` rev 5（#59）：「分割與交叉驗證」（選擇邊界 SR-01、canonical subset、選擇偏誤陳述）、「特徵選擇與模型」（四個路徑方法、group 單位、Lasso 平手、RFE 彙總規則、CV winner、授權集合、執行時間）、「指標與推論」秩不足三類（SR-04、SR-10）、`model_data` 的 `methods`／`winners`、Dashboard（方法與 k、指標 vs k、比較全部、來源標示、invalid 標示）、Testing Decisions 次 seam「特徵選擇」「選擇邊界」「模型與推論」「選模」與主 seam |
| DA derivation | `decisions/derivation-SPEC.md` §3 B-1、B-3、B-4；§9.1（#62 的分配）、§9.3 條件 4、5、§9.5 TK-3、§9.6 TR-01；§11 G-2 |
| 高風險 | `decisions/decision-20261018-high-risk-categories.md`（H-3；A-1～A-3）；`decisions/decision-20261018-issue60-a4-student-id.md` §2.2（#62 加標 H-2）、S-1（A-4 實際學號比對） |
| 前票的 follow-up（owner＝#62） | `audit/issue-60-c1-r1.md` F-2；`audit/issue-61-c1-r1.md` F-2、F-3（`issue-61-c1-r2.md` 維持 owner）。處理見 3.4 |
| Outcome Contract | `doc/governance/outcome-contract.md`：Brief @ `dff7c55c`＋CC-1、AD-1～AD-3 |
| 授權 | `run/run-20261018-hw2-formal.md` §1 designation 第 2 點（Implementation）、第 3 點（SA-1 本機 commit；不 push） |
| UI 參考 | `design/` Wireframe v0.2（只作版面參考；沒有沿用 `mock-data.js`／`wireframe.js` 的計算或數值）；UI 決策 1、2、4 |
| Bindings | b5；HOW `impl-default` v2（overrides none） |

## 2. Executing role and binding

- **角色**：Executor（`gov-executor` subagent，由 Orchestrator 派工）。
- **Binding 觀測**（Bindings §3.6 的同一邏輯，掃描本 subagent 的 transcript `subagents/agent-a04e1bc646c4d6912.jsonl`，`meta.json` 的 `agentType` = `gov-executor`）：實作 commit 之後觀測 `('claude-opus-5-5', 'high')` 231 則，單一元素，等於 O-1 mapping。全程核對（含之後的訊息）由 Orchestrator 在採用 return 前執行。
- **Escalation／替代**：無。
- **Bounded assignments**：未使用（沒有派 `gov-investigator` 或 `gov-bounded-worker`）。

## 3. Work performed

### 3.1 產物（commit `a2811e9`，22 個檔案，全部在 `home_work_02/` 內，不含 `doc/requirement/`）

| 路徑 | 內容 |
| --- | --- |
| `hw2/selection.py` | 新增。四個路徑方法（3.2）、`GroupGram`（給定列上置中、欄位單位化後的 Gram；最小範數解，秩不足不拋錯）、`method_paths`（每個 fold 只用該 fold 的訓練列，canonical 用整個 training set）、`evaluate_method`、`run_path_methods`（每方法計時）、`check_path`（每步恰變一個 group）、方法說明 `METHOD_NOTES` |
| `hw2/models.py` | `evaluate_candidate` 拒絕 fold 子集數≠fold 數、子集大小≠k（#61 F-2）；`determine_winners` 記錄 `test_model_key`，授權集合以 canonical subset 去重（3.3） |
| `hw2/contract.py` | `validate_methods`（只有四個路徑方法、k=1…18 依序、model_key、每步 canonical 與每個 fold 都恰加一個 group）；`validate_entry` 加 `cv.n_folds`＝`meta.cv.n_folds`、fold 記錄的 groups＝`fold_groups`、`folds_agree` 一致、子集為 canonical order；`validate_winners` 重算方法 winner（有效項目中 CV RMSE 最小、平手取小 k）與整體 winner（平手依方法順序）、`is_method_winner` 旗標一致、method winners 只限路徑方法（G-2）、授權集合＝All-in∪方法 winner∪整體 winner（共用模型一次）、每個 winner 與其 test model 的 canonical subset 相同、授權集合中沒有同一模型兩次（#61 F-3）；`validate_test` 加 `test.<key>.model_key`＝key（#61 F-3 C4） |
| `hw2/export.py` | 寫 `methods`、完整 `winners`、`meta.selection`（方法說明）、`meta.path_timing_s`；JSON 改為 compact（3.3） |
| `hw2/fixture.py` | fixture 改走真正的選擇程式；`inject_invalid_candidate` 人為使一個 RFE 候選 invalid（在 `fixture_note` 標明）；`FIXTURE_SUBSETS` 只留給守門的小測試 |
| `hw2/__init__.py` | 模組清單加 `selection` |
| `hw2.ipynb` | 4.2：方法、準則、RFE 彙總規則、Lasso、平手、秩不足、fold-internal 與 canonical 的說明；執行四個方法並列出時間、canonical 路徑、CV RMSE 表、fold 一致數、invalid 清單、CV RMSE vs k 圖。5.1：完整 winners、共用模型規則、選擇偏誤陳述（TK-3）。5.3：守門仍關閉（alpha 未固定、正式旗標關閉）。5.4：匯出 |
| `results/model_data.json`、`assets/model_data.js` | 重新產生：`meta`、`preprocess`、`inputs`、`methods`（4×18）、`baselines.allin`、完整 `winners`、`test_inputs`（schema、0 列）；沒有 `test` |
| `index.html`、`assets/app.js`、`assets/style.css` | 指標 vs k 圖（Chart.js；四條路徑、All-in 參考線、winner 圓環、invalid 叉號、選取圓圈、指標下拉 RMSE／MAE／MSE／R²、文字摘要與圖例）；「比較全部方法」切換（疊圖全部強調＋各方法 CV winner 與 All-in 比較表，標「訓練 CV（USD）」）；選取摘要加各 fold 子集與 canonical 的差異、共用模型說明；Test 區塊依 `test_model_key` 找共用模型的 test 項目並標明「與 … 為同一模型，Test 只評估一次」；沒有 test 項目時隱藏並清空 Test 數字（#61 F-3）；invalid 時預測器停用並顯示原因 |
| `assets/hw2core.js` | `testEntryKey`（只讀 `winners.*.test_model_key`，不計算任何東西） |
| `tests/` | 新增 `test_selection.py`、`test_methods_contract.py`；修改 `test_models.py`（`_cand` 每個方法不同子集；共用模型、G-2 測試）、`test_model_data_official.py`、`test_dashboard_static.py`、`test_notebook_structure.py`、`test_test_section.py`、`js/core.test.js` |
| `README.md` | 檔案配置加 `selection`；執行時間的位置（不抄數字） |

### 3.2 重要決定（HOW）

- **SFS 的步驟準則**：Forward／Backward SFS 每一步以給定列上 OLS（ln(price)）的 in-sample RSS 選 group（ISLR 的 forward／backward stepwise）；k 由外層的分組 5-fold CV RMSE（USD）決定。Spec 沒有指定 SFS 的步驟準則；我沒有選用內層 CV 準則，因為 k 已由外層 CV 選，in-sample RSS 對固定 k 的子集比較是標準做法、決定性且便宜。這是 HOW，不改變方法集合或 k 範圍；列為 concern C-2 供 Reviewer 判斷。
- **RFE 的 group 重要度**（Spec：由實作決定並寫入方法說明）：group 對擬合 ln(price) 的貢獻 X_g·β_g 在給定列上的標準差。與尺度無關；單一欄時就是標準化係數 |β|·sd(x)；zipcode 的 69 欄、整修的 2 欄各為一個整體。寫入 notebook 4.2 與 `meta.selection`。
- **Lasso 路徑排序**：在 #60 的 Ridge／Lasso 標準化（在給定列上 fit；數值欄標準化、zipcode one-hot 維持 0／1）上，以 LARS 計算精確的 Lasso 路徑；group 內任一欄首次非零即進入；沒有進入的 group 排最後。
- **平手**：準則值在相對容差 1e-12 內視為平手，依 canonical order：Forward 與 Lasso 先加入較前的 group，Backward 與 RFE 先移除較後的 group。
- **秩不足**：選擇以最小範數解計算，常數或共線的 group 只是沒有貢獻，步驟不跳過；子集能否擬合交給 `evaluate_candidate`（invalid）或 `fit_allin`（實驗層級失敗）。**觀察**：同一列上，任何子集的設計矩陣欄位都是 All-in 欄位的子集，所以 All-in 有效時，路徑候選在正式流程中不會 invalid；invalid 的呈現與「不被選為 winner」只能以人為注入驗證（fixture 的 `inject_invalid_candidate`、`test_models.py` 的單元案例）。
- **model_data 改為 compact JSON**：`methods` 讓每個 (方法, k) 都有 (XᵀX)⁻¹，含縮排的檔案為 12.2 MB，compact 為 8.7 MB（同一物件；壓縮後約 3.1 MB）。
- **Test 區塊比較表的 Test 欄位**：比較表只放訓練 CV 指標與 log 尺度 Adjusted R²；Test 指標欄（含 Ridge／Lasso 的 metric_only）屬 #63（G-4），本票沒有加入。Ridge／Lasso 參考線同屬 #63。

### 3.3 共用模型與授權集合（需要 DA 確認的解讀，concern C-1）

- 實際資料上，Forward SFS、Backward SFS、Lasso 路徑排序的 CV winner 都是 k=17，canonical subset 相同（18 個 group 去掉 `sqft_lot15`）；RFE 的 CV winner 是 k=18，也就是 All-in 的 18 個 group。整體 CV winner 是 Lasso 路徑排序 k=17（它的 fold 子集與其他方法不同，所以 CV RMSE 不同）。
- 我把「同一模型只評估一次」（Spec「特徵選擇與模型」、BR-01 第 3 點、CONTEXT「Test evaluation」）讀成：模型＝canonical subset 在整個 training set 上擬合的 OLS，canonical subset 相同即同一模型（CONTEXT「All-in baseline」也寫明它等於路徑在 k=18 的端點）。因此授權集合是 `['allin', 'forward_sfs_k17']`，各 winner 以 `test_model_key` 指向評估該模型的鍵。若改依鍵去重，會把同一個擬合模型以 5 個鍵各評估一次（數值完全相同）。
- 我認為只有前一種讀法與「同一模型只評估一次」的文字一致，所以實作它；但它決定 #63 寫出的 `test` 鍵集合與 dashboard 的呈現，屬語義解讀，請 DA 確認（required authority：Design Authority）。改為依鍵去重只需要改 `determine_winners` 與契約的對應檢查。

### 3.4 前票 follow-up 的處理

| Finding | 處理 | 證據 |
| --- | --- | --- |
| #60 R1 F-2（改動驗證列的測試應作用在同時拿到訓練列與驗證列的呼叫點） | 選擇邊界測試對 `selection.method_paths(training, method)`（拿到全部 fold 的列）改動 fold 0 的價格與特徵，斷言 fold 0 的子集序列不變（四個方法） | `tests/test_selection.py::test_changing_a_folds_validation_rows_does_not_change_that_folds_subsets`；mutant S1、S2 |
| #61 R1 F-2（`fold_groups` 被靜默截斷；契約不核對 fold 數） | `evaluate_candidate` 拒絕；契約核對 `cv.n_folds`＝`meta.cv.n_folds`、`fold_groups` 數、fold 記錄的 groups | `test_a_wrong_number_of_fold_subsets_is_refused`；tamper `meta.cv.n_folds`、`n_folds`；mutant W2、C3 |
| #61 R1 F-3（授權清單＝聯集；`model_key` 一致；dashboard 顯示舊數字） | 契約核對聯集（共用模型一次）與 `test.<key>.model_key`；`renderTest` 在沒有 test 項目時隱藏並清空 | tamper `_authorize_a_non_winner`、`model_key`；`test_test_block_never_keeps_numbers_of_another_model`；mutant C1、J1 |

### 3.5 Test 資料隔離（TR-01、H-3）

- 本票沒有載入任何正式 test 列：選擇與評估只接收 `prepared.training`；`testgate.OFFICIAL_TEST_GATE_ENABLED` 仍為 False；notebook 5.3 示範守門拒絕（winners 已完整，但正式旗標關閉、alpha 未固定）。
- 追蹤的正式 `model_data` 沒有 `test`，`test_inputs.written` false、0 列（`test_no_test_rows_and_no_test_results_are_tracked`，Node「official model_data has no test results」）。
- Test 區塊、授權集合的分層與共用模型的呈現只以 synthetic fixture 驗證；fixture 的 `model_data` 只寫到 pytest 暫存目錄與 scratchpad（`hw2.fixture` 拒絕單元目錄內的輸出）。
- 測試中讀到真實資料的只有既有的結構測試與 training 列（`prepared_real.training`）。

## 4. Verification

環境：Windows 11 專業版 10.0.26200、13th Gen Intel Core i9-13900HX（32 logical processors）、31.7 GB RAM、Python 3.11.2（`home_work_02/.venv`，依 `requirements.txt`）、Node v24.19.0、Chrome 155.0.8059.80、Edge 155.0.4283.45（皆 headless）。

| # | 方法 | 結果 | 證據 |
| --- | --- | --- | --- |
| V-1 | `.venv/Scripts/python -m pytest -q -rs -p no:cacheprovider`（`home_work_02/`，工作樹＝`a2811e9`） | **236 passed, 1 skipped**（skip＝學號設定未提供）；base 為 183 passed | 本機執行輸出 |
| V-2 | 次 seam「特徵選擇」：四個方法每步恰變一個 group、18 個巢狀子集、canonical order；`GroupGram.rss` 與直接 OLS 相同（rel 1e-8）；Forward 第 1、2 步與 Backward 第 1 步等於暴力 RSS 最小；RFE 移除的 group 等於貢獻標準差最小者，重要度等於直接計算；平手：`_pick`、Lasso 的同時進入與從未進入依 canonical order、完全相同的兩欄 Forward 取前者 Backward 先移除後者；常數 group 不停止也不跳過步驟 | 通過 | `tests/test_selection.py` |
| V-3 | 次 seam「選擇邊界」：改動 fold 0 的價格與特徵，fold 0 的子集序列不變（四個方法）；canonical 等於直接在 training set 上計算、與 fold 標籤無關；各 fold 子集等於只在該 fold 訓練列上計算；候選的 fold 記錄使用該 fold 自己的子集 | 通過 | 同上 |
| V-4 | 次 seam「選模」「無效候選」：平手取小 k、整體平手依方法順序、授權集合推導（含 k=18 與 All-in 共用、兩方法同子集共用）、invalid 不得勝出、某方法全部無效→停止、整體 winner 無法決定→停止、All-in 共線→停止、canonical 秩不足→invalid 無 fit、G-2 | 通過 | `tests/test_models.py` |
| V-5 | 主 seam（fixture，真正的選擇程式）：每方法 k=1…18、各處 k 個 group、`cv.n_folds`＝5；注入的 invalid 候選有原因、沒有 CV 平均、不是 winner、不在授權集合與 `test`，同方法其他 17 個照常；winners 可由契約重算；授權集合＝聯集（共用一次）；G-2；15 種 tamper（缺 k、`ridge` 當路徑方法、跨兩個 group 的步驟、n_folds、folds_agree、少一個 fold 子集、winner 不是最小、多一個 winner 旗標、`ridge` 當方法 winner、整體 winner 錯、winner 指向不同模型、授權集合少、非 winner 被授權並評分、winner CV 被放大、`model_key` 不符）都被拒；既有的獨立重算（全部 `ols_subset` × 全部 test 列，1e-6）照常通過 | 通過 | `tests/test_methods_contract.py`、`tests/test_test_section.py` |
| V-6 | 正式 `model_data`：區段＝{meta, preprocess, inputs, test_inputs, methods, baselines, winners}；`validate_model_data` 通過；JSON 與 JS 同一物件；四個方法 k=1…18；`meta.path_timing_s` 與 `timing_s.path_*` 一致；winners 完整且不含 Ridge／Lasso；canonical 路徑由 training 列重新計算後完全相同；整體 CV winner（Lasso k=17）的 fold 子集與 CV 指標由 training 列重算後相同（rel 1e-9） | 通過 | `tests/test_model_data_official.py` |
| V-7 | Node：`node --test tests/js/core.test.js` → 8 pass、0 fail、3 skip（fixture 項目）；pytest 以 fixture 執行同一檔（`test_node_core.py`）0 skip：官方與 fixture 各方法 k=1…18、winner＝有效項目中 CV RMSE 最小（平手小 k）、旗標唯一、invalid 不是 winner、`testEntryKey` 指向授權集合中同一 canonical subset 的鍵、不含 Ridge／Lasso；fixture 的注入 invalid 不可預測 | 通過 | `tests/js/core.test.js`、`tests/test_node_core.py` |
| V-8 | Dashboard 靜態：`python -m hw2.offline_scan` → `scanned 6 files: PASS (0 findings)`；指標 vs k 圖與比較表的程式不讀 `MD.test`／`test_inputs`、讀 `cv.mean` 與 `fit.adj_r2_log`，兩張卡標「訓練 CV（USD）」；沒有 test 項目時 Test 區塊隱藏並清空 | 通過 | `tests/test_dashboard_static.py` |
| V-9 | Notebook：六章順序；已執行無錯誤；Modeling 含 fold-internal selection、canonical subset、group 重要度彙總規則、驗證列不參與選擇、平手與 canonical order；Evaluation 含選擇偏誤、樂觀偏誤、「不是它表現的不偏估計」「Test 評估才是 CV winner 表現的獨立估計」、同一模型只評估一次 | 通過 | `tests/test_notebook_structure.py` |
| V-10 | **Dashboard（`file://`、headless Chrome、所有主機名稱無法解析，CDP）**：正式與 fixture 兩個頁面在 1440／768／375 px 都沒有例外、console error、水平溢出；只有 6 個本機檔請求、0 個非 file 請求。正式頁：方法選單五項；路徑方法 18 個 k 按鈕、winner 綠點（Forward／Backward／Lasso 17、RFE 18）；All-in 顯示「k = 18（固定）」狀態列（UI 決策 4）；圖有四條路徑＋All-in 參考線＋選取圈；指標改 R² 後 y 軸標題與摘要改變；比較全部顯示 5 列並標整體 winner 與「與 … 為同一模型」；選 k=3（非 winner）時 KPI、預測器（3 個輸入）更新；Test 區塊顯示「Test 評估尚未執行」。Fixture 頁：注入的 RFE k=7 為紅斜紋、圖上叉號、KPI 顯示「invalid 候選：fold_rank_deficient」、預測器停用並顯示原因（UI 決策 2）；選非 winner 時黃色提示說明 Test 區塊展示該方法 winner（BR-01 第 5 點、UI 決策 1）；Test KPI 屬於該 winner | 通過 | scratchpad `page_check62.js`、`pc62_official.json`、`pc62_fixture.json` |
| V-11 | 截圖目視（1440 與 375 px）：發現並修正兩個缺陷——指標下拉被 `.input` 撐滿整列（選擇器特異性）；比較表標題不換行，表格在 1440 px 需要橫向捲動。修正後表格在 1440／1024 px 不需捲動，375 px 時只在表格容器內捲動、頁面無溢出 | 修正後通過 | scratchpad `shot_fx_c.png`、`shot_off_375b.png`、`measure62.js` |
| V-12 | **OV-6 量測方式回歸檢查**（只驗證方法；正式 gate 屬 #67）：fixture dashboard（n_test 4,291，全部逐筆；`model_data.js` 11.1 MB）以 #61 的 `ov6_measure.js` 各 3 次。首次繪製 Chrome 555.0／280.7／250.0 ms、Edge 550.4／266.8／248.5 ms（#61 時約 175／41／36 ms；增加來自較大的 `model_data` 解析）；互動最大值：滾輪縮放 ≤ 39.9、方法切換 ≤ 40.6（含 k 圖重繪）、k 切換 ≤ 10.9、拖曳 ≤ 4.0、按鈕 ≤ 4.5 ms；全程 visible | 遠低於 3 s／1 s 門檻 | scratchpad `ov6_62_chrome.json`、`ov6_62_msedge.json` |
| V-13 | **Mutation probes**（scratchpad 的單元複本，完整 suite）：S1 fold 路徑看到驗證列、S2 只用驗證列、S3 Forward 平手取後者、S4 Lasso 平手不依 canonical、S5 RFE 移除最重要者、S6 Backward 反向、S7 RFE 重要度忽略尺度、W1 共用模型不去重、W2 截斷 fold 子集、C1 不核對授權聯集、C2 不重算方法 winner、C3 不核對 n_folds、J1 Test 區塊保留舊數字、J2 忽略 `test_model_key`。第一輪 11／14；W1 是等價 mutant（我的改法沒有關掉去重），C1、C2 存活是因為既有 tamper 先觸發其他檢查。補上兩個針對性的 tamper（非 winner 被授權並評分；winner 的 CV RMSE 不再最小）並把 W1 改成真正關掉去重後，三者重跑都被偵測 → **14／14 DETECTED** | 通過 | scratchpad `mutants62.py` 輸出 |
| V-14 | A-4（對 `a2811e9`）：`tests/test_repo_hygiene.py` 15 passed、1 skipped；追蹤樹沒有 `.zip`／`.env`／`kaggle`／`.local/`／`acceptor_materials/`／`dist/`，PDF 只有老師文件；新增行中 7 位以上數字只有紀錄檔名的日期 `20261018`、CV RMSE 小數部分與檔案位元組數；「學號」只出現在本 worklog 的敘述；commit message 沒有 7 位以上數字；過程中沒有印出任何疑似值 | 通過；實際學號比對 NOT VERIFIED（依 `decision-20261018-issue60-a4-student-id.md` S-1） | 本機執行輸出 |

**執行時間量測（Q34）**——四種方法各自的路徑計算時間（5 個 fold＋整個 training set 的選擇，加上 k=1…18 的 5 折 CV 與 canonical fit），單位秒。兩次完整 notebook 執行（同一機器，負載不同）：

| 方法 | 選擇：5 fold＋training set（第 1 次／第 2 次） | CV＋canonical fit（第 1 次／第 2 次） | 合計（第 1 次／第 2 次） |
| --- | --- | --- | --- |
| Forward SFS | 0.97／2.36 | 16.55／26.54 | 17.52／28.90 |
| Backward SFS | 1.31／2.34 | 15.75／25.31 | 17.06／27.65 |
| RFE | 0.76／0.96 | 16.95／20.52 | 17.72／21.48 |
| Lasso 路徑排序 | 2.19／2.70 | 7.44／9.43 | 9.63／12.13 |

- 整本 notebook 非互動執行：67.8 s／103.2 s。追蹤的 `model_data` 是第 2 次（`meta.generated_at` 2026-10-18T11:31:32Z）。兩次的 winners 與授權集合相同。
- 判斷：路徑選擇本身每方法 1–3 s，主要成本是 72 個候選 × 6 次 OLS（CV＋canonical）；整體重跑約 1–2 分鐘，可接受，沒有觸發 Q34 的停止回報。沒有縮小 k 範圍或方法集合。
- pytest 全部約 57–59 s（base 約 9 s；增加來自 fixture 改跑真正的四個方法與新的官方重算測試）。

**正式結果（只有 training CV 與擬合，沒有任何 test 數字）**：方法 CV winner——Forward SFS k=17（CV RMSE US$158,098）、Backward SFS k=17（US$158,098）、RFE k=18（US$158,154，＝All-in）、Lasso 路徑排序 k=17（US$157,254）；整體 CV winner＝Lasso 路徑排序 k=17；授權集合 `['allin', 'forward_sfs_k17']`（3.3）；沒有 invalid 候選。

**限制**：瀏覽器檢查都是 headless；OV-1～OV-6 的正式 gate 屬 #67。Node 直接執行時 fixture 項目 skip，由 pytest 以 fixture 執行涵蓋。

## 5. Commit 與 A-4 核對

- **實作 commit**：`a2811e9f7191a5729d15f3a20e6eac305f85fad9`（parent `6f18d8f`），22 個檔案，全部在 `home_work_02/` 內、不含 `doc/requirement/`。本 worklog 另以 record-only commit 加在其後。
- **未 push**（designation 第 3 點；run record §1 push 選項 (a)）。沒有 rebase、merge、force push。
- **A-4**：見 V-14。
- **Scratchpad 產物**（不在 repo）：`fx62/`（fixture dashboard）、`probe62.py`、`edit_nb62.py`、`edit_app62.py`、`edit_tests62.py`、`page_check62.js`、`shot62.js`、`measure62.js`、`mutants62.py`、量測 JSON 與截圖。
- **工作時間**：2026-10-18 19:00 至 20:30 +0800（約）。

## 6. Audit status

- **Required**（Formal：每張票都要 independent audit；Bindings §5）。觸及 H-2（dashboard 新增 Chart.js 圖、比較表與資源載入，`index.html` 路徑不變、離線掃描 PASS；notebook 六章名稱與順序不變）與 H-3（選擇邊界、fold-internal selection、CV winner、授權集合、秩不足語義、契約不變量、dashboard 分層）：依 A-1 需要 R1 record 的類別核對節，依 A-2 Reviewer 自行執行選擇邊界測試與重算，依 A-3 核對 `methods`／`baselines` 沒有 test 欄位與 UI 不以 `test_inputs` 評估。
- 進度：尚未派工（由 Orchestrator 依 Bindings §3.7 派 `gov-primary-reviewer`）。本檔的 self-verification（含 mutation probes 與瀏覽器檢查）不是 audit。

## 7. Remaining work、concerns 與 follow-up

| ID | 內容 | Required authority |
| --- | --- | --- |
| C-1 | 共用模型的解讀（3.3）：canonical subset 相同即同一模型，授權集合去重、winner 以 `test_model_key` 指向。實際資料上授權集合因此從 5 個鍵變為 2 個。請確認，或裁決改為依鍵去重 | Design Authority |
| C-2 | SFS 的步驟準則採 in-sample RSS（3.2），不是內層 CV。屬 HOW；列出供 Reviewer 判斷是否符合「Forward／Backward SFS」 | Reviewer（若有爭議 → Design Authority） |
| C-3 | 結構性觀察：All-in 有效時路徑候選不可能 invalid（3.2），所以正式資料的 invalid 呈現只以 fixture 的人為注入與單元案例驗證；Spec 的 SR-04 第 2 類在正式流程中只是防衛性路徑 | 無（告知） |
| C-4 | `model_data` 8.7 MB（compact；追蹤兩份，壓縮後各約 3 MB），之後每次重新產生都會進 git 歷史；fixture 首次繪製由約 0.2 s 增為約 0.25–0.55 s | 無（告知；OV-6 正式量測屬 #67） |

- **#63**：比較表的 Test 欄（G-4）與 Ridge／Lasso 參考線；開啟守門時以 `ols_models_for(winners, …)` 取授權鍵（共用模型一次）；#61 R1 F-4 仍屬 #63。
- **學號比對**：依 S-2～S-5，學號設定提供後執行（不是本票結案條件）。
- 未 push。
