# Worklog — issue #63（HW2 T4 Ridge／Lasso 對照、p-value backward、Adjusted R² 與一次性正式 Test 評估）

- **Work item**：GitHub issue [#63](https://github.com/yotsubamomo/aiot-classwork/issues/63)，run `run-20261018-hw2-formal`（Formal，並行度 1）。
- **狀態**：進行中（2026-10-18 開始）。本檔在可接手的時點更新。
- **Subject base**：branch `home_work_02-regrill` @ `b686b3a`。

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
- **Binding 觀測**：結案前補記（Bindings §3.6）。

## 3. Work performed

（進行中）

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
