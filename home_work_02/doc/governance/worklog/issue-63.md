# Worklog — issue #63（HW2 T4 Ridge／Lasso 對照、p-value backward、Adjusted R² 與一次性正式 Test 評估）

- **Work item**：GitHub issue [#63](https://github.com/yotsubamomo/aiot-classwork/issues/63)，run `run-20261018-hw2-formal`（Formal，並行度 1）。
- **狀態**：實作、self-verification 與唯一一次正式 Test 評估完成；**一項 AC 部分 BLOCKED**（Node 逐筆重算在 2 個數值上超出絕對容差 1e-6 USD，需 Design Authority 裁決容差語義，見 §7 C-1）。本檔不代表 audit 或 closure。
- **Subject base**：branch `home_work_02-regrill` @ `b686b3a`。
- **Commits**（本機，未 push）：`69eb814`（pre-gate 實作）→ `1aefe05`（pre-gate 紀錄，record-only）→ `d413e58`（開啟守門）→ `052984b`（正式評估的產物）→ 本檔的 record-only commit。最終 implementation commit＝`052984ba21568499aad4b02e6ba8c564901e8c76`。

## 1. Contract reference

| 項目 | 內容 |
| --- | --- |
| Ticket | #63（OPEN，`ready-for-agent`；含 TR-01 的「開啟守門」AC、DA TK-2、TK-4 的 AC；高風險 H-2、H-3）；索引 `doc/ticket/tickets.md` |
| Spec | `doc/spec/SPEC.md` rev 5（#59）：「特徵選擇與模型」（對照模型、CC-1 六項約束、講義 p-value 對照、授權集合）、「指標與推論」（Adjusted R²）、「預測區間」、`model_data` 的 `baselines`／`winners`／`test_inputs`／`test`（`ols_subset`、`metric_only`）與不變量、Dashboard（參考線、比較表、分層規則、來源標示）、Testing Decisions 主 seam 與次 seam |
| DA derivation | `decisions/derivation-SPEC.md` §3 B-2、B-3、B-10；§9.1（#63 的分配）、§9.3（Test 時序，條件 1–6）、§9.5 TK-2、TK-4；§9.6 TR-01（#63 的開啟守門 AC）；§11 G-1～G-4、CC-1 |
| 其他 DA 紀錄 | `decisions/decision-20261018-high-risk-categories.md`（H-2、H-3；A-1～A-3、A-7、A-8）；`decisions/decision-20261018-issue60-a4-student-id.md`（S-1；§2.2 #63 加標 H-2）；`decisions/decision-20261018-issue62-shared-subset-test-key.md`（D-1～D-4；§7 對 #63 的要求） |
| 前票 follow-up（owner＝#63） | `audit/issue-61-c1-r1.md` F-4（`issue-61-c1-r2.md` 維持 owner）；`audit/issue-62-c1-r1.md` F-1、F-2、F-3 |
| Outcome Contract | `doc/governance/outcome-contract.md`：Brief @ `dff7c55c`＋CC-1（六項約束）、AD-1～AD-3 |
| 授權 | `run/run-20261018-hw2-formal.md` §1 designation 第 2 點（Implementation）、第 3 點（SA-1 本機 commit；不 push、不 rebase、不 merge） |
| UI 參考 | `design/` Wireframe v0.2（只作版面參考，不沿用 mock 計算或數值） |
| Bindings | b5；HOW `impl-default` v2（overrides none） |

## 2. Executing role and binding

- **角色**：Executor（`gov-executor` subagent，由 Orchestrator 派工）。
- **Binding 觀測**（Bindings §3.6 的同一邏輯，掃描本 subagent transcript `subagents/agent-a9f28ccd59c59b6b3.jsonl`，`meta.json` 的 `agentType`＝`gov-executor`）：正式評估的產物 commit 之後觀測 `('claude-opus-5-5', 'high')` 284 則，單一元素，等於 O-1 mapping。全程核對由 Orchestrator 在採用 return 前執行。
- **Escalation／替代**：無。**Bounded assignments**：未使用。

## 3. Work performed

### 3.1 產物

| 路徑 | 內容 |
| --- | --- |
| `hw2/comparison.py`（新增） | Ridge／Lasso：全部 18 group、在每次擬合的列上標準化（數值欄標準化、zipcode one-hot 0／1），alpha 以共用的分組 5-fold training CV（USD）RMSE 最小者選（平手取較大 alpha），網格與 CV 曲線都記錄；整個 training set 上重新擬合成 metric-only 模型（只提供點預測給一次性評估；係數不匯出）。p-value backward：group partial F 檢定、門檻 0.05、每步移除 p 最大者；fold-internal＋canonical；只作對照列 |
| `hw2/contract.py` | `baselines.ridge`／`lasso`（只有 `cv`＋alpha；禁止 `fit`、係數、PI 欄位；alpha 可由 CV 曲線重算；Adjusted R² 為 null）與 `baselines.pvalue_backward` 的檢查；`test` 的 metric-only alpha＝training-CV alpha、p-value 不得出現在 `test`；`test_inputs.n_unseen_zipcode` 與各 `ols_subset` 的 `n_unseen_zipcode`（SR-07） |
| `hw2/testgate.py` | `is_official` 不只看 sha256（官方路徑或官方結構也算，#61 R1 F-4）；開啟時計算凍結選擇的 sha256 digest；評估回傳 manifest（run id、時間戳、digest、授權鍵、資料 sha256、test 列 digest、評估次數 1）；`OFFICIAL_TEST_GATE_ENABLED = True`（`d413e58`） |
| `hw2/export.py` | 寫出 `baselines.ridge／lasso／pvalue_backward`、`meta.comparison`、`meta.comparison_timing_s`、`meta.test_evaluation.manifest`／`code_revision`；`write_result_tables`（TK-2：`cv_by_method_k.csv`、`comparison.csv`（`cv_*` 與 `test_*` 分欄）、`alpha_cv.csv`，都由 `model_data` 產生）；`result_digest` |
| `hw2/fixture.py` | fixture 改跑真正的 Ridge／Lasso CV 與 p-value（取代 stand-in） |
| `hw2.ipynb` | 4.3 Ridge／Lasso、4.4 p-value、5.2 Adjusted R²（只對 OLS 子集；其他標「不適用」）、5.3 PI（原 5.2）、5.4 凍結選擇＋唯一一次評估＋同一 cell 匯出、第二次呼叫被拒、5.5 結果（訓練 CV 與 Test 分欄、共用模型標示、D-3 的評估數量由程式計算、涵蓋率偏離的描述） |
| `results/model_data.json`、`assets/model_data.js`、`results/tables/*.csv` | 正式評估的產物（`052984b`） |
| `index.html`、`assets/app.js`、`assets/style.css` | 指標 vs k 圖加 Ridge／Lasso 參考線與圖例；比較表改為「訓練 CV（USD）」「Test 評估（USD）」兩組欄，含 Ridge／Lasso（Adjusted R² 與涵蓋率「不適用」）與 p-value 列（「不在 Test 上評估」）；共用模型標示列出全部共用的 winner（#62 R1 F-1）；Test 區塊 grid 欄寬修正（#62 R1 F-2）；KPI 區註明 Adjusted R² 對 CV 聚合值不適用 |
| `tests/` | 新增 `test_comparison.py`；更新 `conftest.py`（autouse：測試中正式守門一律關閉）、`test_testgate.py`、`test_test_section.py`、`test_methods_contract.py`、`test_contract_fixture.py`、`test_dashboard_static.py`、`test_model_data_official.py`、`test_notebook_structure.py`、`js/core.test.js` |
| `README.md`、`hw2/__init__.py` | 檔案配置、Test 評估只執行一次與重跑一致性的說明、時間欄位位置（不抄數字） |

全部改動在 `home_work_02/` 內，沒有 `doc/requirement/`（`git diff --name-only b686b3a 052984b`）。

### 3.2 重要決定（HOW）

- **Alpha 網格與規則**：Ridge `logspace(-4, 5, 37)`、Lasso `logspace(-8, -1, 29)`，準則是 USD 尺度 CV RMSE（與路徑方法一致）。網格是在正式 training CV 上看曲線後決定的（training-only，不涉及 test）。兩者在正式資料上都選到網格**下緣**：CV RMSE 隨懲罰減弱單調下降，趨近 All-in OLS（Ridge 158,154.48、Lasso 158,154.87 vs All-in 158,154.31）。這是誠實的結果，不再擴大網格（再小只會更接近 OLS）；`alpha_at_grid_edge` 記錄在契約中，notebook 印出說明。列為 concern C-2。
- **Lasso 演算法**：`lasso_path`（中心化資料＋Gram 矩陣，沿網格 warm start，tol 1e-10），比逐 alpha 的座標下降快約兩個數量級且無收斂警告；與 scikit-learn `Lasso` 直接擬合核對（rtol 1e-6）。
- **p-value 的 F 檢定**：以 `selection.GroupGram`（中心化、欄單位化的 Gram）算 RSS 與秩，df＝n − 1 − rank；與兩次直接 OLS 擬合的 F、df、p 核對。
- **正式資料識別（#61 R1 F-4 的判斷）**：sha256 之外，再以官方路徑或官方結構（21,613 列、21,436 唯一 id）判定為正式（fail-closed）。
- **正式評估的執行方式**：開啟守門（旗標）是單獨的 commit；notebook 以乾淨的 `hw2/` 執行一次，`meta.test_evaluation.code_revision` 記錄 `d413e58`、`package_modified: false`。
- **比較表版面**：備註放在模型名稱下方，數值欄不換行；1440 px 時表格在自己的容器內有約 11 px 的橫向捲動，頁面不溢出。
- **報告草稿**：報告檔由 #65 建立（DA I-3、§11 G-4「報告的結果表也照同樣方式分開」由 #65 負責）；本票提供的是 notebook 與 CSV 的分欄表格。

### 3.3 前票 follow-up

| Finding | 處理 | 證據 |
| --- | --- | --- |
| #61 R1 F-4（正式資料「每個 process 只載入一次」沒有測試；只以 sha256 識別） | 以 synthetic 資料＋monkeypatch 的 `EXPECTED_SHA256` 測旗標關閉時拒絕、旗標開啟時第一個 gate 評估、第二個 gate 被「already loaded」拒絕；識別加上路徑與結構 | `test_testgate.py::test_official_data_cannot_be_opened_while_the_flag_is_off`、`…_load_at_most_once_per_process`、`…_identity_does_not_rest_on_the_sha256_alone`；mutant M5 |
| #62 R1 F-1（代表鍵所屬 winner 的共用說明不完整） | `sharedWinners` 對每個 winner 列出全部共用者，用於選取摘要、比較表、Test 區塊；CSV 的 notes 同樣列出 | 正式頁 CDP：All-in「與 RFE · k = 18 為同一模型…Test 只評估一次」、Forward「與 Backward SFS · k = 17、Lasso 路徑排序 · k = 17 為同一模型…」 |
| #62 R1 F-2（Test 區塊 375 px 溢出 44 px） | `.testzone`、`#test-body` 加 `grid-template-columns: minmax(0, 1fr)` | 正式頁與 fixture 頁（Test 區塊有資料）在 375／768／1440 px、各 8 種狀態溢出 0 px（Chrome、Edge） |
| #62 R1 F-3（D-4 第 3 點沒有測試） | tamper：共用模型的 winner 以自己的鍵授權並評分 → 被拒 | `test_methods_contract.py`（`_score_a_shared_model_twice`）；mutant M10 |

## 4. 守門開啟前的狀態（pre-gate record，在開啟守門之前寫入並 commit）

- **Pre-gate implementation commit**：`69eb814ecdf54ac8c8c3b6c7260fde893da01d01`（parent `b686b3a`）。`hw2/testgate.py` 的 `OFFICIAL_TEST_GATE_ENABLED = False`；正式 test 列至此沒有被載入，也沒有任何評估使用過它們。
- **選擇結果**（只用正式 training 列，2026-10-18 以 `pregate.py` 在 scratchpad 計算；gate 狀態 `{'state': 'closed', 'official_data': True, 'official_gate_enabled': False}`，計算 110.8 s）：

| 項目 | 值 |
| --- | --- |
| 各方法 CV winner（CV RMSE USD → test_model_key） | Forward SFS k=17（158,098.26 → `forward_sfs_k17`）；Backward SFS k=17（158,098.26 → `forward_sfs_k17`）；RFE k=18（158,154.31 → `allin`）；Lasso 路徑排序 k=17（157,253.88 → `forward_sfs_k17`） |
| All-in CV RMSE | 158,154.31 |
| 整體 CV winner | `lasso_path_k17`（test_model_key `forward_sfs_k17`） |
| **授權集合**（D-1） | `['allin', 'forward_sfs_k17']`＋metric-only `ridge`、`lasso` |
| Ridge alpha（training CV） | 0.0001（網格 1e-4…1e5，37 點；在網格下緣），CV RMSE 158,154.48 |
| Lasso alpha（training CV） | 1e-08（網格 1e-8…1e-1，29 點；在網格下緣），CV RMSE 158,154.87 |
| p-value backward（講義對照） | canonical k=16（移除 `sqft_lot15`、`bedrooms`）；fold 子集大小 17/17/16/16/16；CV RMSE 158,584.85；不評估 Test |
| **Selection digest**（`testgate.selection_digest(winners, alphas)`） | `44f7723e4023afc3e8e997f42bf4eb59db392af81cced11743757a9857cb4b28` |

- 正式執行時，notebook 重算同樣的選擇並在開啟守門時凍結；正式結果的 `meta.test_evaluation.manifest.selection_digest` 必須等於上表的值（事後核對）。
- **開啟前的 self-verification**（全部只用 synthetic 資料或 training 列）：
  - pytest（`69eb814` 工作樹）：270 passed、1 skipped（學號設定未提供）、10 failed——10 個都是需要「已執行的正式 notebook／正式 `test`」的測試（`test_model_data_official.py` 7 個、`test_notebook_structure.py` 2 個、`test_node_core.py` 1 個），在正式評估前必然失敗，正式執行後重跑。
  - Node `core.test.js`：正式 test 的兩項同理待正式執行；以 rehearsal 的 `model_data` 當 fixture 執行時，全部 test 列 × 授權 OLS 模型的 JS 逐筆重算通過（容差 1e-6）。
  - **Notebook 全程演練**（scratchpad `ex63/rehearse_nb.py`）：在 notebook 的複本前插入一個 cell，把 `data.load_and_split` 換成 synthetic CSV（21,430 列，非正式資料），所有寫出改到 scratchpad；其餘每個 cell 原樣執行（路徑方法、Ridge／Lasso CV、p-value、winners、守門開啟、唯一一次評估、匯出、結果表、第二次呼叫被拒）。3,040 列與 21,430 列兩次演練都無錯誤（55.0 s）。演練輸出再以 `reh_plugin.py` 指向 `test_model_data_official.py`：14 passed，3 個失敗都是預期的 synthetic 差異（sha256、列數、`official_data` False）；manifest 的 digest、授權集合、alphas、test-row digest 另以腳本核對全部相符。`test_notebook_structure.py` 對演練 notebook 7 passed。
  - Dashboard（`file://`、headless Chrome 155.0.8059.80、主機名稱全部無法解析，CDP，scratchpad `ex63/page_check63.js`）：fixture dashboard（n_test 4,291）在 1440／768／375 px、8 種狀態都沒有例外、console error、非 file 請求，水平溢出 0 px（#62 R1 F-2 修正後 Test 區塊有資料時也是 0）；Ridge／Lasso 參考線在圖上；比較表分「訓練 CV（USD）」「Test 評估（USD）」兩組欄、含 Ridge／Lasso（Adjusted R² 與涵蓋率「不適用」）與 p-value 列（「不在 Test 上評估」）；Test 區塊在所有狀態都只顯示 `ols_subset`，不含 Ridge／Lasso；共用模型的每一方都列出其他 winner（#62 R1 F-1）。
  - **Mutation probes**（scratchpad `ex63/mutants63.py`，單元複本，相關測試檔）：15 個中 14 個被偵測；M12（比較表列先讀自己的鍵再退回 test_model_key）是等價 mutant（授權集合去重後，共用者自己的鍵不在 `test`），改成非等價的 M12b（只讀自己的鍵）後被偵測。
- 下一步：把 `OFFICIAL_TEST_GATE_ENABLED` 改為 `True` 並單獨 commit（開啟守門），然後以 `python -m hw2.run_notebook` 執行唯一一次正式評估。

## 5. 正式 Test 評估的執行紀錄（唯一一次）

| 項目 | 值 |
| --- | --- |
| 守門開啟 | commit `d413e5862486af812b6eec29f813689b17b0c15e`（`OFFICIAL_TEST_GATE_ENABLED = True`）；開啟前狀態見 §4（`69eb814`、紀錄 `1aefe05`） |
| 執行指令 | `.venv/Scripts/python -m hw2.run_notebook`（`home_work_02/`），**只執行這一次**；執行紀錄 scratchpad `ex63/formal_run.log` |
| 執行時間 | 開始 2026-10-18T13:36:56Z，結束 13:37:33Z；`executed hw2.ipynb in 36.8 s`；exit 0 |
| 守門開啟時間戳 | `opened_at` 2026-10-18T13:37:32+00:00；`evaluated_at` 2026-10-18T13:37:32+00:00 |
| 執行識別 | `run_id` `fe76019b9af84b1e8ff46095d5ac0fb2`；`code_revision` `d413e58`、`package_modified: false`；資料 sha256 `d0875baa…57b7e`（`official_data: true`） |
| 凍結選擇 | `selection_digest` `44f7723e4023afc3e8e997f42bf4eb59db392af81cced11743757a9857cb4b28`＝§4 預先記錄的值（相符）；授權 `['allin', 'forward_sfs_k17']`；alphas ridge 0.0001、lasso 1e-08 |
| 評估範圍 | `ols_subset`：`allin`、`forward_sfs_k17`；`metric_only`：`ridge`、`lasso`；`evaluations_in_this_run: 1`；notebook 的第二次呼叫被拒（「the test evaluation already ran in this run; it runs once」） |
| Test 列 | n_test 4,323；房屋 4,287；重複交易 36；未見 zipcode（編為基準）0；`test_rows_digest` `e9ef12b50dce6d7249fb524b05c697baffe5eb75c2fee1b92aa531a45aa7c3d1` |
| 結果 digest（比對基準，bit-exact） | `export.result_digest`（`test_inputs`＋`test`）＝`b53ff286ae0734add8b272089aba904a1cb7f5aca444a62d356420b25dc3cfc6` |
| 產物 commit | `052984ba21568499aad4b02e6ba8c564901e8c76`（`results/model_data.json`、`assets/model_data.js`、`results/tables/*.csv`、已執行的 `hw2.ipynb`） |

**`test` 摘要**（之後重跑的比對基準，DA §9.3 條件 2；USD）：

| 鍵（kind） | RMSE | MAE | MSE | R² | PI 涵蓋率（涵蓋／n） | 平均寬度 | 二項近似 ± |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `allin`（ols_subset；All-in、RFE k=18） | 183,596.7048 | 78,114.2594 | 3.3707750015e10 | 0.782848199 | 0.944252（4,082／4,323） | 401,086.73 | 0.006839 |
| `forward_sfs_k17`（ols_subset；Forward k=17、Backward k=17、Lasso 路徑排序 k=17＝整體 CV winner） | 183,369.7846 | 78,100.1503 | 3.3624477904e10 | 0.783384654 | 0.944483（4,083／4,323） | 401,052.38 | 0.006826 |
| `ridge`（metric_only，alpha 1e-4） | 183,596.5037 | 78,114.2656 | 3.3707676181e10 | 0.782848674 | — | — | — |
| `lasso`（metric_only，alpha 1e-8） | 183,596.7424 | 78,114.2996 | 3.3707763802e10 | 0.782848110 | — | — | — |

- Test 結果沒有回饋任何選擇：正式執行之後沒有修改任何選擇、alpha、前處理或模型集合的程式；之後的 commit 只有本 worklog。
- 時間（`meta.timing_s`，秒）：路徑方法 forward 8.37、backward 8.53、rfe 7.30、lasso_path 4.03；All-in CV 0.47；Ridge 1.86、Lasso 0.88、p-value 1.09；Test 載入 0.034、評分 0.146；notebook 全程 36.8 s。演練（synthetic 21,430 列）55.0 s；開啟前的 training-only 計算 110.8 s（機器負載不同）。沒有觸發 Q34 的停止回報。

## 6. Verification（正式評估之後）

環境：Windows 11 專業版 10.0.26200、13th Gen Intel Core i9-13900HX、31.7 GB RAM、Python 3.11.2（`.venv`，`requirements.txt`）、Node v24.19.0、Chrome 155.0.8059.80、Edge 155.0.4283.45（headless）。

| # | 方法 | 結果 | 證據 |
| --- | --- | --- | --- |
| V-1 | `.venv/Scripts/python -m pytest -q -rs -p no:cacheprovider`（工作樹＝`052984b`） | **280 passed、1 skipped、1 failed**。skip＝學號設定未提供；failed＝`test_node_core.py`（它執行 `core.test.js`，失敗原因見 V-3） | 本機輸出 |
| V-2 | 主 seam pytest（numpy 獨立重算）：`test_model_data_official.py` 17 項全過——區段與 TK-4（`methods`、`baselines` 無 test 欄位）；`ols_subset` 鍵＝授權清單、`metric_only` 只有 Ridge／Lasso、PI 欄位與 kind 一致；`test_inputs` 列識別＝分割的 test 列、房屋數／重複交易數／未見 zipcode 數；**兩個 `ols_subset` 模型的 4,323 筆逐筆點預測與 PI（絕對容差 1e-6 USD）、covered、coverage、平均寬度、二項近似、MAE／MSE／RMSE／R² 全部相符**；manifest（digest 由匯出的 winners 與 alphas 重算相符、test-row digest、code revision）；Ridge／Lasso alpha、CV 曲線與 p-value 由 training 列重新計算相符（G-1）；CSV 與 `model_data` 一致（TK-2）且 `cv_*`／`test_*` 分欄 | 通過 | 同上 |
| V-3 | Node `node --test tests/js/core.test.js` | 8 pass、**1 fail**、3 skip（fixture 項目；由 pytest 以 fixture 執行）。失敗的是「official: JS prediction, PI and covered reproduce the contract on every test row」：25,938 個數值中有 **2 個**超出絕對 1e-6 USD——`forward_sfs_k17` 第 1878 列 lower（9,370,545.03，差 1.33e-6）與 upper（19,433,214.09，差 2.90e-6）；最大相對差 2.6e-13；covered 4,323×2 筆全部一致。以分數／Decimal 精確計算該列：**匯出值本身與精確值相差 2.26e-6（upper）、9.4e-7（lower）**，所以任何 float64 實作在這幾個千萬美元級的值上都不能保證絕對 1e-6；numpy 的 pytest 重算能過是因為它和匯出用同一個運算式。見 §7 C-1 | 部分 BLOCKED（Design Authority） | scratchpad `ex63/jscovered.json`、`jsdiff.js` 輸出、精確計算的輸出（本節數字） |
| V-4 | `python -m hw2.offline_scan` | `scanned 6 files: PASS (0 findings)` | 本機輸出 |
| V-5 | 正式 dashboard（`file://`、主機名稱全部無法解析，CDP，`ex63/page_check63.js`），Chrome 與 Edge 各一次 | 1440／768／375 px 都沒有例外、console error、非 file 請求（6 個本機檔），各 8 種狀態水平溢出 0 px；指標 vs k 圖有四條路徑＋All-in＋Ridge＋Lasso 參考線；比較表 8 列（5 個 winner 各自身分＋Ridge＋Lasso＋p-value），分欄「訓練 CV（USD）」「Test 評估（USD）」，Ridge／Lasso 的 Adjusted R² 與涵蓋率「不適用」、p-value「不在 Test 上評估」；Test 區塊在全部選取下只顯示 `ols_subset`、不含 Ridge／Lasso，標示所展示的方法與 k 及共用說明；非 winner（Lasso 路徑排序 k=3）時出現提示；散佈圖 4,323 筆；firstDraw Chrome 220 ms、Edge 192 ms（只驗證方法，OV-6 正式 gate 屬 #67） | 通過 | `ex63/pc63_off_chrome.json`、`pc63_off_msedge.json`、截圖 `shot_off_*` |
| V-6 | Notebook：六章順序；已執行無錯誤；Modeling／Evaluation 的 #63 陳述；只有一個 `gate.open`、一次評估、一次被拒的第二次呼叫 | 通過 | `test_notebook_structure.py` |
| V-7 | 開啟前的 self-verification（演練、fixture、mutation probes） | 見 §4 | §4 |

- **A-4（S-1）**：追蹤樹沒有 `.zip`／`.env`／`kaggle`／`.local/`／`acceptor_materials/`／`dist/`（`test_repo_hygiene.py` 15 passed、1 skipped）；本票新增行中「學號」0 次；7 位以上數字串只有日期 `20261018`、浮點數值的數字段、檔案位元組數、hash 片段與資料中的房屋 `id`（`model_data`）；commit messages 中的長英數字只有 run id／digest 前綴；過程中沒有印出任何疑似值。**實際學號比對 NOT VERIFIED**（學號設定尚未提供；依 `decision-20261018-issue60-a4-student-id.md` S-1）。
- **Git**：commit message 依 git 規則，無 Claude 標記；未 push、rebase、merge、force push。

## 7. Concerns 與所需 authority

| ID | 內容 | Required authority |
| --- | --- | --- |
| C-1 | **Node 逐筆重算的容差語義**（AC「SR-02 獨立重算…pytest（numpy）與 Node…逐筆相符（容差 1e-6）」；Spec「主 seam」）。現行測試把 1e-6 解讀為絕對 USD；正式資料有千萬美元級的 PI 端點，float64 的捨入（相對約 1e-13）在這裡就超過 1e-6 USD——匯出值本身與精確值差 2.26e-6。正式評估的數值不能重算（不得再次評估），重新評估也會得到同樣的值，所以這不是需要重新評估的缺陷。兩種合理讀法：(a) 絕對 1e-6 USD（目前 2 個值不符）；(b) 相對 1e-6（或「絕對 1e-6 或相對 1e-12」之類的組合；全部相符，最大相對差 2.6e-13）。這是 accepted verification 門檻的語義，我不自行放寬測試：`core.test.js` 維持絕對 1e-6 並如實失敗 | **Design Authority**（BLOCKED，只限這一項；其他工作已完成） |
| C-2 | Ridge 與 Lasso 的 alpha 都落在網格下緣（CV RMSE 隨懲罰減弱單調下降、趨近 All-in OLS）。符合 CC-1「alpha 只以 training CV 選」；契約記錄 `alpha_at_grid_edge: "lower"`，notebook 印出說明；報告（#65）需要如實說明「正則化在此資料上沒有改善 CV」 | Reviewer（若有爭議 → Design Authority） |
| C-3 | Test RMSE（約 183,400–183,600）明顯高於 CV RMSE（約 157,300–158,200），是描述性事實；依協定不換模型。報告（#65）需說明（CV winner 的樂觀偏誤、test 的獨立估計） | 無（告知 #65） |
| C-4 | `test_node_core.py`（pytest 經由它執行整個 `core.test.js`）因 C-1 失敗；C-1 裁決後依裁決調整 | 隨 C-1 |
| C-5 | 比較表在 1440 px 有約 11 px 的表格內橫向捲動（頁面不溢出）；更窄時表格在容器內捲動 | 無（OV-2 的正式量測屬 #67） |

## 8. Audit status 與 remaining work

- **Audit**：Required（Formal；觸及 H-2：dashboard 參考線、比較表、Test 區塊改讀正式結果、notebook 章節內容；H-3：唯一一次正式評估、CC-1 約束、契約不變量）。依 A-1 需要 R1 record 的類別核對節；依 A-2 Reviewer 自行執行 pytest／Node 與重算；依 A-3 核對 `methods`／`baselines` 無 test 欄位、`test` 鍵集合、UI 不以 `test_inputs` 評估。尚未派工（由 Orchestrator 依 Bindings §3.7）。本檔的 self-verification 不是 audit。
- **之後的票**（DA §9.3）：#64～#67 完整重跑 notebook 時會以同一 seed 與鎖版本重做這次評估；結果必須與 §5 的摘要與 `result_digest` 一致（digest 是 bit-exact；若只在最後幾位不同，依 §5 的數值摘要判斷並 route 給 DA）。任何會改變選擇、alpha、前處理或模型集合的修改都不得以 test 結果為理由。
- **Remaining**：C-1 的 DA 裁決與其後 `core.test.js` 的對應調整；學號比對（S-2～S-5）；push 依 run record 選項 (a)。
- **Scratchpad 產物**（不在 repo）：`ex63/`——`probe_alpha.py`、`probe_cmp.py`、`pregate.py`／`pregate.json`、`rehearse_nb.py`、`reh_small/`、`reh_full/`、`reh_plugin.py`、`nb_plugin.py`、`page_check63.js`、`tw.js`、`pc63_*.json`、截圖、`mutants63.py`／`mutants63.out`、`formal_run.log`、`jsdiff.js`、`jscovered.js`／`jscovered.json`、`edit_*.py`。
- **工作時間**：2026-10-18 約 20:40 至 21:55 +0800。
