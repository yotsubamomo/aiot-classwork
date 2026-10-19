# Worklog — issue #67（HW2 T8 打包、離線驗收（OV-1～OV-6）、乾淨環境重跑與整合）

- **Work item**：GitHub issue [#67](https://github.com/yotsubamomo/aiot-classwork/issues/67)，run `run-20261018-hw2-formal`（Formal，並行度 1）。最後一張票。
- **狀態**：實作與 self-verification 完成，待 Orchestrator 核對 binding 並派 R1。本檔不代表 audit、closure 或 phase acceptance。
- **Subject**：branch `home_work_02-regrill`，base `ace3958c66072fb8b70b56adbf473919d4ec325d`；**最後的實作 commit `e2780f46dbea4d0816a6dcc8bba0725bc6182797`**（本機，未 push）。單元的最後一個打包內容 commit 是 `e2f391a`（ZIP 由它打包；之後只改 `doc/acceptance/ACCEPTANCE.md`、`tests/test_report.py` 與 root 兩列，都不在 ZIP 內）。本檔以其後的 record-only commit 加入（Bindings §7）。

## 1. Contract reference

| 項目 | 內容 |
| --- | --- |
| Ticket | #67（OPEN；高風險 H-1～H-4，A-4、A-6）；索引 `doc/ticket/tickets.md` |
| Spec | `doc/spec/SPEC.md` rev 5：「報告與打包」的打包條款、Dashboard（SR-09 (a)～(g)）、人工檢查表、OV-1～OV-6 的 gate 分類、「乾淨環境重跑」 |
| Brief／OC | `doc/brief/BRIEF.md` @ `dff7c55c` §7（BR-04 離線驗收）、§8（ZIP 內容）、§10；`doc/governance/outcome-contract.md`（CC-1、AD-1 OV 分類、AD-3 Pages 檢查記 NOT TESTED pending merge） |
| Wireframe acceptance | `design/WIREFRAME-ACCEPTANCE.md`（OV-1～OV-6） |
| DA records | `decision-20261019-cell28-glyphs.md`（G-1～G-5）；`decision-20261018-issue64-notebook-rerun.md`（N-1～N-6、§9.3 條件 7、8）；`decision-20261018-issue60-a4-student-id.md`（S-4／S-5 由 R1 重做）；`derivation-SPEC.md`（§9.3 條件 1～6、§9.6 TR-01）；`decision-20261018-high-risk-categories.md`（A-4、A-6）；`decision-20261018-issue63-js-tolerance.md`（T-1）；`decision-20261018-issue62-shared-subset-test-key.md`（D-2～D-4）；`decision-20261019-issue65-labels-figures.md`（F-4、O-2）；`decision-20261018-issue64-standardized-reading.md` |
| Acceptor 指示 | Run record §14 第 1～3 點（重跑＝reproducibility verification；每次執行只對授權集合評估一次；digest／manifest 比對，不一致時停止並回報 DA，非決定性 metadata 另行記錄）；§15（shell 寫入交付物的 workaround）；§19（RB-5：root 兩列逐字套用擬稿；學號設定已建立） |
| 前票 findings（owner #67） | #64 R1 F-1（三項測試缺口）；#66 R1 F-1（final 建置前比對 derived sha256）；#65 R1 F-4（cell 28，已由 DA G-1～G-5 處置）；#65 worklog C-4（k 刻度）與 R1 §8 第 4 點（價格刻度「1.00e+3 萬」）；#66 worklog C-3（SciTePress DOI 瀏覽器確認）；#62 R1 F-2（OV-2 須在 Test 區塊有資料時量測）；#60 R1 F-4（版本漂移記錄） |
| 派工約束 | 單元外只改 root 兩列；不改 `doc/requirement/`；SA-1 本機 commit、不 push／rebase／merge／deploy；學號、作者姓名、對話網址、acceptor 材料、PDF、ZIP 不進追蹤檔案或 commit message；完整重跑只在條件 7 成立後執行一次 |
| Bindings／HOW | b5；`impl-default` v2（overrides none） |

## 2. G-3：cell 28 的獨立 commit

- Commit `e0be302`（parent `ace3958`）：只改 `hw2.ipynb` cell 28（id `2fc16ee1`）source 的一行：`label=models.METHOD_LABELS[m])` → `label="Lasso path ranking" if m == "lasso_path" else models.METHOD_LABELS[m])`。沒有加註解行，沒有改輸出（舊輸出由完整重跑重新產生）。以位元組層級替換 notebook JSON 中唯一的一處（scratchpad `ex67/edit_cell28.py`），diff 只有 1 行。
- 與 `052984b` 的 unified diff（cell 28 source）：

```diff
-            label=models.METHOD_LABELS[m])
+            label="Lasso path ranking" if m == "lasso_path" else models.METHOD_LABELS[m])
```

- 事前確認（G-4 第 3 點，MAY）：`ex67/legend_probe.py`，Agg backend、`-W error::UserWarning`，只畫 5 個圖例標籤的空圖：exit 0，沒有缺字警告。

## 3. 實作的變更（commits）

| Commit | 內容 | 依據 |
| --- | --- | --- |
| `e0be302` | cell 28 一行（§2） | DA G-3 |
| `1f3a8b6` | 新增 `hw2/package.py`（打包：先核對已 commit、單一次完整執行、正式評估、final 報告建置，再寫 `dist/<學號>_hw2.ipynb` 與固定排序／時間戳的 `dist/<學號>_hw2.zip`，讀回逐項比對 sha256，manifest 只用 `<學號>`）與 `tests/test_package.py`；`hw2/report.py` 新增 `DERIVED_REVIEWED` 與 `check_derived_reviewed()`，`--final` 且讀本機材料時，derived 三檔不是 #66 R1 審查版本就拒絕建置（#66 R1 F-1，選擇以追蹤的釘值實作，會留下 git delta）；#64 R1 F-1 的三項測試（低於 training 下界的外推標示、整體 winner 與 All-in 為同一模型時 `shared_with` 含 All-in、group 內各欄以同一列排列打亂）；README 的打包步驟；`hw2/__init__.py` 說明 | Spec「報告與打包」（打包模組）；#66 R1 F-1；#64 R1 F-1 |
| `99a3ed4` | `hw2/package.py` 以「開啟守門的那一格」（`gate.open(`）辨認評估 cell：notebook 有兩格呼叫 `gate.evaluate(`（評估與被拒絕的第二次呼叫），原本的判斷在打包時會誤報；測試同步 | 自我驗證時發現（§5 比對時看到 cell 41、42 都含 `gate.evaluate(`），在打包之前修正 |
| `2cd2a70` | 單一次完整執行的產物：`hw2.ipynb`、`results/model_data.json`、`assets/model_data.js`（CSV、PNG、pickle 內容與追蹤檔相同，git 無 delta） | N-3 |
| `e2f391a` | `assets/app.js`：(1) 「指標 vs k」圖 x 軸 0.5～18.5，Chart.js 產生的刻度落在 k 之間，k 數字完全沒有顯示 → 以 `afterBuildTicks` 在 k = 1…18 各放一個刻度；(2) 散佈圖價格刻度 ≥ 1,000 萬時顯示「1.00e+3 萬」→ 改為「1,000 萬」 | #65 C-4／DA O-2（交 #67 的 D-1、D-4 檢查）；#65 R1 §8 第 4 點（D-2、OV-6 (c)）。不在凍結範圍、不影響 `model_data` 或任何評估；修正後重新打包並重做 OV 全部檢查 |
| `611ad07` | Root `README.md` 作業表、`CONTEXT-MAP.md` 各一列，**逐字**取自 run record §19 的擬稿（以程式從 run record 擷取，不手抄）；獨立 commit，diff 各 1 行 | RB-5 授權（run record §19） |
| `8a902c2` | `doc/acceptance/ACCEPTANCE.md` 全部填寫 | Ticket AC |
| `e2780f4` | `tests/test_report.py`：#65 的「驗收前不得有 PASS」測試改為驗收後的規則（每列有 PASS／FAIL／NOT TESTED 且 PASS 有證據位置、沒有 PENDING、D-12 為 NOT TESTED（pending merge）、無環境的 best-effort 為 NOT TESTED、subject 與 OV-6 紀錄已填）。舊測試的語義就是「#67 之前」，新規則更嚴格，不是放寬 | Ticket AC「ACCEPTANCE.md 每一項有狀態與證據位置」 |

- `8a902c2` 單獨時 `tests/test_report.py` 有 1 個失敗（舊規則）；`e2780f4` 修正後全部通過（§6）。
- 寫檔：worklog、ACCEPTANCE、程式與測試以 Write／Edit 工具寫入，沒有遇到 #65 的誤判；notebook 與 root 兩列以腳本精確替換（理由是逐字與位元組層級，不是 workaround）。

## 4. §9.3 條件 7 的前置核對與 G-5（完整重跑之前，subject `1f3a8b6`）

| 核對 | 方法 | 結果 |
| --- | --- | --- |
| 7(a) selection digest | 乾淨環境（§5）的 kernel 中，任何 cell 之前先把 `hw2.testgate.OFFICIAL_TEST_GATE_ENABLED` 設為 False，執行 cell 41（開啟守門）之前的全部 24 個 code cell（notebook 副本，不寫回檔案），在 kernel 中重算 `testgate.selection_digest(winners, alphas)`（`ex67/cond7a.py`，2026-10-19T08:10:24Z～08:11:12Z，47.3 s） | `44f7723e4023afc3e8e997f42bf4eb59db392af81cced11743757a9857cb4b28`＝#63 值；授權 `['allin', 'forward_sfs_k17']`；整體 winner `lasso_path_k17`；alphas ridge 1e-4、lasso 1e-8；`_official_test_rows_loaded` False；資料 sha256＝釘值；notebook 檔案未變 |
| 7(b) 凍結模組 | `git diff --stat 052984b 1f3a8b6 -- hw2/{data,split,preprocess,selection,models,comparison,ols,metrics,contract,testgate,export}.py requirements.txt`（`ex67/cond7b.py`） | 空 |
| 7(b) notebook（G-5 修正版） | 逐格比對 `052984b` 與 `1f3a8b6` 的 cell 0–45 | cell 0–27、29–45 的 source 相同（45 格）；cell 28 差異恰為 G-3 的一行、0 行新增註解，把新行換回原文後與 `052984b` 完全相同；cell 0–45 的 id 與型態不變；notebook metadata 相同 |
| 7(b) 資料 | commit blob 的 sha256 | `d0875baa…57b7e`＝Brief 釘值 |

條件 7 成立 → 執行完整重跑（只一次）。

## 5. 乾淨環境的單一次完整執行（reproduction of #63 run `fe76019b…`）

- **環境**：scratchpad `ex67/clean/`＝`git clone -c core.longpaths=true --branch home_work_02-regrill`（本機 repo，HEAD `1f3a8b6`；`core.longpaths` 只設在這個 clone，因為 `docs/governance/` 的 package 路徑超過 Windows 預設長度）；`py -3.11 -m venv .venv`（Python 3.11.2）；`pip install -r requirements.txt`（08:06:58Z～08:09:59Z，exit 0；鎖定版本全部相符：numpy 2.4.6、pandas 3.0.6、scipy 1.17.1、scikit-learn 1.9.1、matplotlib 3.11.2、joblib 1.6.0、threadpoolctl 3.7.0、nbformat 5.11.1、nbclient 0.11.0、ipykernel 7.4.0、pytest 9.1.1；`ex67/pip_freeze.txt` 共 57 個套件）。#60 R1 F-4：沒有觀察到版本漂移（`meta.versions` 與追蹤檔相同）。
- **執行**：`.venv/Scripts/python -m hw2.run_notebook`，2026-10-19T08:11:26Z 開始，`executed hw2.ipynb in 41.3 s`，exit 0，08:12:07Z 結束（`ex67/full_run.log`）。**只執行這一次**。本次是 #63 run `fe76019b9af84b1e8ff46095d5ac0fb2` 的重現；唯一一次正式評估的權威紀錄仍是 `worklog/issue-63.md` §5。
- **本次 manifest（條件 8）**：`run_id` `5e74d03d6c81499f913532a551af3e6d`；`selection_digest` `44f7723e…4b28`；`code_revision` `{commit: 1f3a8b6fde6526746505dcecb12e375213964d05, package_modified: false}`；`official_data` true；`evaluations_in_this_run` 1；`test_rows_digest` `e9ef12b5…c3d1`（＝#63）；opened／evaluated 2026-10-19T08:12:01+00:00。
- **比對（條件 2；acceptor §14 第 3 點；`ex67/compare_run.py` → `compare_run.json`）**：

| 項目 | 結果 |
| --- | --- |
| 資料 | sha256＝釘值；`test_rows_digest`＝#63 |
| split／fold | `results/split/split_assignment.csv` 內容與追蹤檔相同 |
| winner、授權模型集合 | `winners` 整段相同；授權 `allin`、`forward_sfs_k17` |
| alpha | ridge 1e-4、lasso 1e-8，相同 |
| Test 預測與指標 | `result_digest`＝`b53ff286ae0734add8b272089aba904a1cb7f5aca444a62d356420b25dc3cfc6`（bit-exact）；`test`、`test_inputs` 整段相同 |
| `model_data` 其他內容 | 深度比對 70 個不同路徑，全部在 N-3 允許的欄位內（`meta.generated_at`、`meta.timing_s`、`meta.path_timing_s`、`meta.comparison_timing_s`、`baselines.pvalue_backward.timing_s`、`meta.test_evaluation` 的時刻／耗時／`code_revision`／manifest 的 `run_id`、`opened_at`、`evaluated_at`）；不允許的差異 0；`.js` 與 `.json` 是同一物件 |
| CSV、PNG、pickle | 18 個追蹤檔：PNG 與 pickle 逐位元相同，CSV 內容相同（只差 EOL） |
| Notebook（N-3） | 40 個 code cell，執行序號 1…40 連續、無重複；錯誤輸出 0；cell 41 印出的 `run_id`＝`model_data` manifest；source 與 commit 相同；metadata 相同 |
| G-5 (i) | 整份 notebook 的輸出中「Glyph」0 次、「missing from font」0 次 |
| G-5 (ii) | cell 28 只有 1 個輸出（stderr 消失），`display_data` 有 `image/png`，`text/plain`＝`<Figure size 900x450 with 1 Axes>`；圖例 5 個標籤 `Forward SFS`、`Backward SFS`、`RFE`、`Lasso path ranking`、`All-in baseline` 都可讀（人工目視 PNG，ACCEPTANCE A-4） |
| 輸出不同的 cell | 5、21、25、30、33（耗時）、28（G-5 允許）、41（manifest 的 `run_id`／時刻；以及見下） ；PNG 不同的只有 cell 28 |

- **非決定性 metadata（另行記錄，acceptor §14 第 3 點）**：cell 41 印出的 `model_data.json`／`.js` 檔案大小由 9,787,774／9,787,860 變為 9,787,770／9,787,856 bytes。驗證它完全來自 N-3 欄位：把重跑物件的 N-3 欄位換回追蹤值後，以 `export.to_json` 序列化的位元組與追蹤的 `model_data.json`（EOL 正規化）完全相同（`ex67/size_explain.py`）。所以這是耗時與時刻欄位的文字長度造成的印出差異，不是內容差異。其餘耗時：路徑 forward 8.16、backward 8.18、rfe 7.06、lasso_path 4.02 s（#63：8.37、8.53、7.30、4.03）。
- **追蹤**：把 clone 的 `hw2.ipynb`、`results/**`、`assets/model_data.js` 原樣複製回 repo（先另存 `ex67/run_outputs/`，21 個檔的 sha256 在 `run_outputs.sha256`），`git diff` 只有 3 個檔（notebook、兩個 `model_data`），commit `2cd2a70`。之後 clone fast-forward 到 `2cd2a70`，追蹤版與另存的執行產物逐檔相同（21／21）。打包用的 `<學號>_hw2.ipynb` 與追蹤的 `hw2.ipynb`、執行產物三者 sha256 相同（`2e2f8afc…ff64`）。

## 6. 測試（乾淨環境，subject `e2f391a`；另在 repo 對最後 subject `e2780f4`）

| 位置 | 指令 | 結果 |
| --- | --- | --- |
| clean clone @ `2cd2a70` | `python -m pytest -q -rs` | 395 passed、0 skipped（50.5 s）；Node `tests/js/core.test.js` 9 pass、0 fail、3 skipped（fixture 版，需環境變數；由 `tests/test_node_core.py` 以 fixture 執行，skip 0）；`hw2.offline_scan` PASS（6 檔，0 findings） |
| clean clone @ `e2f391a` | 同上 | 395 passed（48.7 s）；Node 9 pass；offline_scan PASS |
| repo @ `e2780f4` | 同上 | 395 passed（48.6 s）；Node 9 pass |

- 新增測試的 verify-the-verification（`ex67/mutants67.py`，scratch 複本，每次只改一處）：D2（只檢查上界）、D4（All-in 共用分支 `if False`）、E1（group 內各欄獨立打亂）、R1（final 建置跳過 derived 核對）、R2（derived 釘值不比較）、P1（不檢查執行序號）、P2（不檢查 run id）、P3（不比對 ZIP 項目）：**8／8 DETECTED**；未突變基準 82 passed、2 skipped（無材料與學號設定的複本）。
- 執行中「不重新評估」：pytest 與 Node 只讀匯出的 `test`／`test_inputs`；`tests/` 沒有在正式資料上開啟守門的 fixture（#63 R1 F-2 的 guard 未被觸及）。

## 7. 打包與 ZIP

- 指令：clean clone @ `e2f391a`，`python -m hw2.package`（內含 `report.build(final=True)`），08:26:44Z～08:26:59Z，exit 0。學號設定與 acceptor 材料以複本放入 clone 的 ignored 位置（`notebooklm_v1_superseded/` 不複製、不使用）；用畢已從 scratchpad 刪除。
- 建置前核對（#66 R1 F-1）：`acceptor_materials/derived/` 三檔 sha256 與 `audit/issue-66-c1-r1.md` 表頭相同（`gpt_assist.md` `1a9663f7…6023`、`notebooklm_summary.md` `358c78f2…731d`、`notebooklm_trace.md` `5cae0356…b4`）；同值已釘在 `hw2/report.py` 的 `DERIVED_REVIEWED`，final 建置自動核對。材料三檔 sha256 與收件值相同（ChatGPT PDF `0a5d29e3…a194`、docx `77b8f7e7…4a96`、`sources.md` `141c211b…2b`）。
- **ZIP**：`<學號>_hw2.zip`，**sha256 `c84a3c5e6d295ed383fc8c085eb68f30aaa9035208cf9ca7eeaa0d9aae763fb6`**，81,432,807 bytes，56 個項目，單一頂層資料夾 `<學號>_hw2/`；位置：`home_work_02/dist/`（未追蹤，`.gitignore:19`），另有 `dist/<學號>_hw2.ipynb`（sha256 `2e2f8afc1f67fd51312b894d3a3f4873049defead185b1dd4ca2ab1ace04ff64`）、`dist/hw2_package_manifest.json`、`dist/report/`。
- 獨立核對（`ex67/zip_inspect.py`，不使用 `hw2.package`）：檔名＝學號＋`_hw2.zip`；`testzip` 無錯；每個項目與 commit `e2f391a` 的 blob 相同（文字檔 EOL 正規化，PNG／pickle／資料 CSV／vendor 逐位元）；ChatGPT PDF＝收件值；`hw2_report.pdf`＝建置輸出，149 頁（報告 28 頁＋附錄 121 頁）；沒有 `__pycache__`、`.local`、`acceptor_materials`、`tests/`、`doc/`、derived 或 NotebookLM 材料。Brief §8 的九類內容都在（主程式、報告 PDF、ChatGPT PDF、`hw2/`、`requirements.txt`、資料 CSV、README、`results/`、dashboard）。TK-2：報告引用的 8 張 `results/figures/*.png` 與 8 個 `results/tables/*.csv` 都在 ZIP 內，且與追蹤檔相同。
- 第一次打包（@ `2cd2a70`，ZIP sha256 `e771b96f…61bd`）在 `e2f391a` 的 dashboard 修正後作廢，被上面的 ZIP 取代；OV 檢查全部在新 ZIP 上重做（§8）。

ZIP 項目（sha256 由 `ex67/zip_inspect.py` 自 ZIP 讀出）：

| # | ZIP 內路徑（`<學號>_hw2/` 之下） | bytes | sha256 |
| --- | --- | --- | --- |
| 1 | `<學號>_hw2.ipynb` | 1,363,461 | `2e2f8afc1f67fd51312b894d3a3f4873049defead185b1dd4ca2ab1ace04ff64` |
| 2 | `hw2_report.pdf` | 44,572,021 | `8778b459005efda573f4028ef47417d936b24b8ba7b24edc7aaf7979556fbbfe` |
| 3 | `ChatGPT_logs.pdf` | 41,784,474 | `0a5d29e30802270af6a7ff02b692e2bf26e808a5102c6b787adf1ee36a3ca194` |
| 4 | `README.md` | 11,854 | `749dd696f48d92421131274d3fbba0bc1b9c653b93884350942935038d8abad4` |
| 5 | `assets/app.js` | 58,993 | `940a27ab0f763e5ec131606abb7fd4b93ebc0304dc7368c54475a33b9fe503e4` |
| 6 | `assets/hw2core.js` | 8,012 | `7acf6e96403d42e99dada91fb26a29554f750e4d89e2f2c26bfc11a3f992cdc0` |
| 7 | `assets/model_data.js` | 9,787,858 | `570891bfc415eee8d1d91272629c09178da78b6482cf49d0c05916d3feaa1dda` |
| 8 | `assets/style.css` | 19,749 | `1244951237718bd13bd8d8355ea84ac08037797e16584dc415cd79e95c768e32` |
| 9 | `assets/vendor/chart.js.LICENSE.md` | 1,093 | `5a0877ad6d818529be4f33009d0942cdf7e2ed7656156f4aba7308459a546030` |
| 10 | `assets/vendor/chart.umd.js` | 205,125 | `74401d738dd3e03ee5dfb3b6841210fe2c4ead8a960c4011ca4ba0b78a9fd8f3` |
| 11 | `data/kc_house_data.csv` | 2,515,206 | `d0875baa0251b21d4bdc9d2ae940a4fe0bb6009824f23dd0e2a5b2bf04557b7e` |
| 12 | `hw2/__init__.py` | 2,520 | `ea15796d75731aba26ad358cb6d6e9db28e47f44463c26ffb05da7ed421b7602` |
| 13 | `hw2/comparison.py` | 18,146 | `6c38978c68e06c72b693715dff8aded92e04b50c06fc74f313b5a1cfad3b1733` |
| 14 | `hw2/contract.py` | 35,527 | `45152c2ea8713a0d14d376f0401cab7e7292841a06e27e1e2a278ae1304a4082` |
| 15 | `hw2/data.py` | 7,649 | `9e9e7a6a17f2ce5754389cdc5b2fa34871bcdcae2eb6d7d2a411a6b178cf571c` |
| 16 | `hw2/deployment.py` | 12,517 | `12ee24b9126aed3eecbc670d79422c9794a21b632aba27e3593d8ff46c1275f9` |
| 17 | `hw2/diagnostics.py` | 30,072 | `eb0eb59c20ccb3a4dd7eeab14b898ab01d65d7a82514813f599fec5310a50176` |
| 18 | `hw2/explain.py` | 10,284 | `bd1eaff3d289eea61f5e94e57d9d0261860d3c824db062e683697a227659d2de` |
| 19 | `hw2/export.py` | 22,041 | `d250f24f34a1e855ed0473bbd5c6e8dbc8e5a15fc683ab04d7a5916da95cfac8` |
| 20 | `hw2/fixture.py` | 12,777 | `40d193ab225ead1386755e0da491f264b90b3c76c581116bd8bfa07392fbc269` |
| 21 | `hw2/local_config.py` | 1,677 | `c6ad7440d0b0244d4db984719b6d7abb358fe1853520e76db76f11b277cd5e57` |
| 22 | `hw2/metrics.py` | 2,544 | `e242a3eeddf8ae1d551c40a4822ed29e5af29a51999eced76d704eb7b358757f` |
| 23 | `hw2/models.py` | 16,991 | `1c73bb9c258026662c3e99a4381f69b854826f10da06d7dc4a5e877554e83d15` |
| 24 | `hw2/offline_scan.py` | 6,992 | `998064017561d2aa121630fe38f381f92d5a2cacede000f4732edccbd8e6acb6` |
| 25 | `hw2/ols.py` | 6,490 | `197eb646ece6ccc8db9002ec61ab5a4bc65bd409a1998617d79bae515b112d28` |
| 26 | `hw2/package.py` | 10,917 | `885633b4a79c521824e7f7be87e68e75c7b19b67e3f9591a89270ed9e4e8e287` |
| 27 | `hw2/paths.py` | 1,926 | `4a46b3ad9094efc079ece12547a726f59e5fa4f86e6c566ebc21605f870543d7` |
| 28 | `hw2/pdf_append.py` | 20,350 | `8453497d14f538131229374bea8d8f8653cc8ac79552ddbbe4affff773f87517` |
| 29 | `hw2/prediction_plot.py` | 8,624 | `0816e12f95a0e0ca5a0cf290b84c4a8d7e809a17fdd1475be3c615c2d2ef7677` |
| 30 | `hw2/preprocess.py` | 14,004 | `93997ca91908f3420f618bf1022213a5a550c8b5181f20f7848208e5633988d5` |
| 31 | `hw2/report.py` | 66,887 | `3b7ed0aaa02f9c99e13d347400e21a82ecd750873b765679f49e572193b1268e` |
| 32 | `hw2/run_notebook.py` | 677 | `7b8bfc8562fa1161c807b09ca117eca404d70d096b5254b68ff3c3e387b3be24` |
| 33 | `hw2/selection.py` | 16,453 | `75caaaf68daebe1fbf7901f7301605c88d8dbb1e2f5c2230ceaf4e1d79fd9354` |
| 34 | `hw2/split.py` | 2,406 | `3a4783f5a33276c490ea582714a7f30fdac747a91940406426c3b8b9c43f94a1` |
| 35 | `hw2/testgate.py` | 14,053 | `972508bb9d62082cb99a0968de3442729ab70b6dffdbf118a7a4f92e3d5b9e58` |
| 36 | `index.html` | 21,514 | `dc80764bde8041f9f8dc47dc38e3afec41e05b5ef4f0c9e62a2b679b4e72aa45` |
| 37 | `requirements.txt` | 513 | `fb8571a80582a45a13889a5fb1a7235b079fbeb3bc48bcb10e8dca8185c56c9b` |
| 38 | `results/deployment/final_model.pkl` | 65,470 | `6358185ab742b5c3fa05577e2604d611f1da7722f789a5fff4135d5365cc93cd` |
| 39 | `results/figures/diag_homoscedasticity_scale_location.png` | 163,500 | `52d924e34d20170280fed7f3a51d431138d2624ec97e20aa686ff12ca0564d92` |
| 40 | `results/figures/diag_independence_residuals_by_date_and_repeat_sales.png` | 172,503 | `526ce3e34e4d4ff971edcefca5291a011454e88b93aa24b78f55a160f9ca6c6d` |
| 41 | `results/figures/diag_linearity_residuals_vs_fitted.png` | 109,637 | `029db97b33f2882badde16f300e2f7b17e98fd01d656a4d392a4fe6caa5ece54` |
| 42 | `results/figures/diag_multicollinearity_gvif.png` | 43,838 | `06bcdbd3f6fd9f4b3109d3f865b136e09f019368e3bc2dabda37d848d5240d03` |
| 43 | `results/figures/diag_normality_qq.png` | 64,242 | `c567351d06528a3d184b204f463200ab44b0242bed3a8a5d82cb8618a34defbc` |
| 44 | `results/figures/eval_actual_vs_predicted_pi.png` | 158,031 | `8afdb90b6aa9f1fce55fc7cf565db6a8ecefa71c136541f49b55dc1a54bc4a39` |
| 45 | `results/figures/explain_coefficients_percent_effects.png` | 60,659 | `331ba220642d53cf50c6bcf94de2342f9ae99679af368d2e6cab126db4441bbf` |
| 46 | `results/figures/explain_permutation_importance.png` | 44,070 | `fdcee9eb7743ee0054590d013ddca75b4ea600c720d5ca76c783b1e2b1bea15f` |
| 47 | `results/model_data.json` | 9,787,771 | `cac51bbe8338fe8ceb0c1e409f1ab69bc2126538478fad69f86d705dc2274b65` |
| 48 | `results/split/split_assignment.csv` | 542,199 | `44cb3d8a0655f91a701b001e814e5a26cd872010dc344e02e5d02c4a2db6bd33` |
| 49 | `results/tables/alpha_cv.csv` | 6,912 | `09b98bc9db8ac3a3c255e1b9bae9a4a1004fb7df27227e647f9d31f5c839ff9e` |
| 50 | `results/tables/comparison.csv` | 5,008 | `39549010d10318cd90b6c7b06d532fb34eca738f639b1885d05d300b14cb27e1` |
| 51 | `results/tables/cv_by_method_k.csv` | 18,956 | `d21a64f8a24301b4ec3a3dfcda4aab1088144b6fc449a55e4990c090aa7b2f3c` |
| 52 | `results/tables/diagnostics_summary.csv` | 1,739 | `61579ae575bbe8d4c2380cb3cfda02b105108071f90365b34af0a9f93cc494f5` |
| 53 | `results/tables/diagnostics_vif_by_column.csv` | 3,521 | `60285ada364a253bf09f600200cc0740eab0fe74810cea82dfeaba96f612d430` |
| 54 | `results/tables/diagnostics_vif_by_group.csv` | 1,281 | `f89af16fe5dbfb2074c159f9dabe49310d53b4f8f00eb07e1fe0d44d6eb21eec` |
| 55 | `results/tables/final_model_coefficients.csv` | 17,154 | `4fa02fb54a690401b9caa2db89f349ac0c906211f7b3f55630b439e345d814b9` |
| 56 | `results/tables/permutation_importance_training.csv` | 2,155 | `8495cd1ef0e735e993a87690b80922e38f4342a547d789d5cf7c2d69202c5482` |

## 8. Open Verification Items（ZIP 解壓後的 dashboard）

**共同條件**：以 Python `zipfile` 把 `dist/<學號>_hw2.zip` 解壓到新的空目錄 `ex67/ov2/unz/`（路徑先檢查無 `..`），以 `file://` 開啟 `<學號>_hw2/index.html`，沒有任何本機伺服器。瀏覽器以獨立的暫存 profile、**可見視窗**（非 headless）在 acceptor 的電腦上啟動，經 CDP 送出真實的滑鼠、滾輪、鍵盤事件（`ex67/ov67.js`）。**斷網的方式**：DevTools `Network.emulateNetworkConditions(offline)`、`--host-resolver-rules=MAP * ~NOTFOUND`（所有主機名稱無法解析）、`--proxy-server=http://127.0.0.1:9`（無效 proxy）。作業系統層級的網路介面沒有停用（變更系統網路設定不在 Agent 的權限內），見 §11 C-1。結果檔 `ex67/ov2/{chrome,edge}/*_result.json`、`summary.txt` 與截圖（路徑中的解壓資料夾名以 `<top>` 遮罩）。Chrome 2026-10-19T08:27:23Z～08:28:04Z，Edge 08:28:04Z～08:28:45Z。

### 8.1 OV-1（硬性 gate）— PASS

| 檢查 | Chrome 155.0.8059.80 | Edge 155.0.4283.62 |
| --- | --- | --- |
| 必要區塊 (1) 方法 5 個、k 18 個（路徑方法；All-in 時 k 固定、沒有 k 按鈕）、(2) KPI 4 張、(3) 指標 vs k 圖（Chart.js 實例，7～8 個 dataset）、(5) 預測器 18 個輸入、點預測 US$503,564 與 PI US$351,404–US$721,610、(6) 散佈圖 4,323 點與 Test 區塊、(9) 方法與限制 | 全部渲染 | 全部渲染 |
| 方法切換（forward、backward、rfe、lasso、allin）、k 切換（1、9、17、18）、「比較全部」開關（比較表 8 列） | KPI、圖、預測器、Test 區塊同步；非 winner 時出現提示 | 同左 |
| 預測器輸入 | sqft_living 3500 → US$611,588（PI US$426,669–US$876,651）；90000 → 外推警告「超出 training 範圍（290–13540）…」且照常計算 | 同左 |
| 散佈圖縮放 | 滾輪 10 次、拖曳 3 次、按鈕 5 次全部生效 | 同左 |
| zh-TW 無缺字 | 各區塊與 canvas 截圖目視無缺字方塊 | 同左 |
| 對外請求（DevTools Network，整段 session） | 63 個請求：file 54、data 9；**非 file／data：0**；載入失敗 0；檔案只有 `index.html`、`style.css`、`chart.umd.js`、`model_data.js`、`hw2core.js`、`app.js` | 同左（63：54／9／0） |
| 例外、console error、對話框 | 0、0、0 | 0、0、0 |
| 靜態掃描 | 解壓副本 `offline_scan.scan(<解壓目錄>)`：6 檔，PASS，0 findings | — |

### 8.2 OV-2（required）— PASS；真實觸控 NOT TESTED

- DevTools 裝置模擬：375×812（mobile、DPR 2、觸控模擬）與 768×1024；兩個寬度各 8 種狀態（初始、forward、rfe、lasso、lasso k=5、比較全部、All-in、預測器輸入後），**Test 區塊有正式資料**（#62 R1 F-2）：頁面水平溢出 **0 px**（Chrome 與 Edge 皆同），沒有超出視窗的元素（`.tablewrap` 內的捲動除外）。
- 主要功能：方法／k 切換、比較全部、縮放按鈕、預測器輸入（2500 → US$541,221）都可操作；導覽選單按鈕 `aria-expanded` false →（點擊）true →（Escape）false。
- 真實觸控裝置：沒有環境 → **NOT TESTED**。

### 8.3 OV-3（required）— PASS；Firefox best effort；Safari NOT TESTED

- Required：Chrome 155.0.8059.80 與 Edge 155.0.4283.62 都通過 §8.1、§8.2、§8.4～§8.6 的全部檢查。
- Firefox 123.0.1（best effort；WebDriver BiDi，`ex67/ff67.js`，暫存 profile 設無效 proxy）：解壓副本 `file://` 渲染（首次繪製 212 ms、4,323 點）；方法切換（forward、lasso）、k 切換（k=5，出現非 winner 提示）、預測器輸入（2500 → US$449,395）、滾輪縮放都生效；水平溢出 0；Test 區塊截圖無缺字。限制：BiDi 的請求事件只記到 Firefox 自己的歡迎頁對 `accounts.firefox.com` 的 1 個請求（被無效 proxy 擋下，不是 dashboard 發出），`file://` 載入不產生 BiDi 請求事件，所以 Firefox 的零對外請求以 Chrome／Edge 與靜態掃描為準；縮放按鈕的自動點擊沒有記錄到互動；log 有 1 則 Firefox 內部的 `InternalError: Promise rejection value is a non-unwrappable cross-compartment wrapper`（來源未確定）。記為 best effort PASS（核心項目）並列出限制。
- Safari：沒有環境 → **NOT TESTED**。

### 8.4 OV-4（required）— PASS；螢幕閱讀器 NOT TESTED

- 鍵盤：從頁首按 Tab 70 次，依序到達跳到主要內容、5 個頁內導覽、資料集連結、5 個方法按鈕、比較全部、指標選單、係數表 summary、18 個預測器輸入（日期、數值、「未整修」核取方塊、zipcode 下拉）、縮放 3 個按鈕、散佈圖 canvas。操作：在 RFE 按 Enter → 方法切到 rfe；在 k=7 按 Space → k=7；canvas 上 `+`、`←`、`0` → 3 次 `key` 互動；比較全部按 Space → `aria-pressed` true。
- Focus visibility：每個停留點都 `:focus-visible`，按鈕／連結／summary／canvas 為 3 px 實線外框，輸入與下拉為瀏覽器預設 focus ring；日期輸入內部的月、日兩段以反白顯示目前段落（computed outline 為 none，截圖 `ov2/chrome/date_focus_seg2.png` 目視可見）。
- Label 與語意：8 個表單控制項全部有 label；28 個按鈕全部有名稱；24 個按鈕有 `aria-pressed`；導覽按鈕 `aria-expanded` 正確切換（§8.2）；`lang="zh-Hant-TW"`；landmarks header／nav／main／footer 各 1；h1 1 個，h2／h3 層級；兩個 canvas 都是 `role="img"` 並有說明；live region `status`／`alert`。
- 螢幕閱讀器：沒有環境 → **NOT TESTED**。

### 8.5 OV-5（required）— PASS

- 方法：瀏覽器內以 WCAG 2.x 相對亮度公式，對 792 個可見的 DOM 文字元素計算前景色與實際背景（逐層合成半透明背景）的對比；大字＝≥ 24 px 或粗體 ≥ 18.66 px。
- 結果（Chrome 與 Edge 相同）：一般文字最低 **6.49:1**（綠色 winner 標籤 `rgb(22,101,52)` on `rgb(220,252,231)`）；大字最低 16.78:1；不合格 0。Canvas 文字以程式中的顏色計算：散佈圖刻度 `#475569`／軸標題 `#334155` on 白 7.58／10.35:1；Chart.js 刻度預設 `#666` on 白 5.74:1。
- 不只靠顏色：散佈圖落入 PI 為圓點、未落入為方塊，圖例與游標提示另有文字；指標 vs k 圖的 CV winner（圓環）、invalid（叉號）、目前選取（大圓圈）以形狀標示並有 DOM 圖例；Test 區塊的非 winner 提示是文字；k 按鈕的 winner／invalid 寫在 `aria-label`。

### 8.6 OV-6（硬性 gate）— PASS

| SR-09 | 結果 |
| --- | --- |
| (a) 首次繪製 ≤ 3 s | Chrome：254（冷啟動，新 profile）、78.1、81.2、79.7、80.1 ms；Edge：251.6（冷啟動）、90.3、88.5、88.4、85.3 ms（`HW2_PERF.firstDraw`，navigation start → 散佈圖第一次完整繪製）。長任務只有冷啟動載入時 1 個（Chrome 172 ms、Edge 144 ms） |
| (b) 互動 ≤ 1 s、無「沒有回應」 | Chrome：方法 6 次（最大 14.3 ms）、k 3 次（7.5）、滾輪縮放 10 次（34.2）、拖曳平移 3 次（4.4）、縮放按鈕 5 次（4.0）。Edge：16.5、3.7、30.2、3.9、3.6 ms。互動期間長任務 0 個、頁面 `visible`、有焦點、沒有任何對話框 |
| (c) 預設視圖 | 截圖 `ov2/chrome/chrome_scatter_default.png`：y=x 虛線、區間內藍色圓點與區間外橙色方塊可分辨；圖例與軸標籤可讀；刻度「10 萬／100 萬／1,000 萬」（修正後） |
| (d) 個別線段 | 滾輪 4 次後 x 約 30 萬～400 萬（約十倍區間，`chrome_scatter_zoom4.png`），再 4 次後約 55 萬～230 萬（`chrome_scatter_zoom8.png`）：個別 PI 線段與端點可分辨；最密集區仍有重疊（SR-09 (d) 不要求） |
| (e) 游標 | 游標停在一點時提示「第 15,120 列（房屋 …）預測 US$967,938、實際 US$1,225,000、95% PI US$675,209 – US$1,387,576、落入區間」 |
| (f) 紀錄 | ACCEPTANCE.md E 節量測紀錄表（瀏覽器與版本、Windows 11 專業版 10.0.26200、i9-13900HX 24 核／32 執行緒、31.7 GB、n_test 4,323、量測方式、各次數值） |
| (g) 不抽樣 | `firstDraw.nPoints`＝`nTestPoints`＝4,323＝n_test；繪圖迴圈畫全部列 |

### 8.7 Pages

GitHub Pages URL 的檢查：**NOT TESTED（pending merge）**（AD-3；合併後的 Lightweight work item）。

## 9. 其他核對

- **學號（A-4；只輸出計數）**：`git grep -c -F` 全 repo 追蹤檔案 0 個檔案命中；`ace3958..HEAD` 8 個 commit 的 patch 0、commit message 0；`origin/main..HEAD` patch 0；本 worklog 0。ZIP 與 `dist/` 以外沒有寫出含學號的檔案；scratchpad 中含學號或材料的複本（clone 的 `.local/`、`acceptor_materials/`、`dist/`，解壓目錄）用畢已刪除。打包程式與本紀錄只用 `<學號>`。S-4／S-5 的比對由 R1、Spec Integration Audit、合併前各自重做。
- **追蹤檔案的禁止項目（D-21）**：`tests/test_repo_hygiene.py` 通過（含學號測試，skip 0）。
- **主流解法連結（A-10、D-18、#66 C-3）**：`curl -L`：`doi.org/10.26877/asset.v6i3.602` → 200（journal2.upgris.ac.id）；GitHub notebook → 200；Atlantis Press PDF → 200；Kaggle 資料集頁 → 200；`doi.org/10.5220/0013055900004601` 在 curl 下停在 302，**以瀏覽器開啟**解析到 SciTePress 的「The Study on the Influencing Factors of Housing Price」頁面（IAMPA 2024）→ 可開啟。
- **Mock 數值（C-14、A-5）**：`design/wireframe/mock-data.js` 的 98 個有辨識度的數字中，報告出現的 5 個都是巧合的真實值（98001 基準 zipcode、21613／21436 資料列數與唯一 id 數、0.0001 Ridge alpha、1.012 `date` 的 GVIF），README、`index.html` 0 個，`app.js` 1 個（色碼 `334155`）；報告提到 wireframe 的 2 處是 AI 揭露文字。
- **報告（D-13、B-6）**：final 建置的 Markdown 有標示對照表、第 1～11 章與附錄 A、B，`【待填` 0 處，狀態行為 final；附錄 A 寫明唯一一次正式評估是 `fe76019b…`，目前檔案的 `5e74d03d…` 是重現（N-5）。
- **Root 兩列（RB-5）**：`611ad07` 的 diff 各 1 行，與 run record §19 擬稿逐字相同（程式擷取後插入，`git diff` 核對）。

## 10. Executing role and binding

- **角色**：Executor（`gov-executor` subagent，Orchestrator 派工）。
- **Binding 觀測**（Bindings §3.6 同一邏輯，`subagents/agent-ae2448c02ec3d8940.jsonl`，`meta.json` 的 `agentType`＝`gov-executor`）：撰寫本節時 `('claude-opus-5-5', 'high')` 318 則，單一元素，等於 O-1 mapping。全程核對由 Orchestrator 在採用 return 前執行。
- **Escalation／替代**：無。**Bounded assignments**：未使用。

## 11. Audit status、concerns 與 remaining work

- **Audit**：required（Formal；高風險 H-1～H-4）。R1 尚未派工；之後 Spec Integration Audit（A-6 親自核對 ZIP 檔名、內容、sha256 與離線檢查）與 DA phase acceptance。
- **Concerns**：
  - **C-1（OV-1 的斷網方式）**：斷網以瀏覽器層級達成（DevTools offline、主機名稱無法解析、無效 proxy），沒有停用作業系統的網路介面（屬系統設定，Agent 不得變更）。零對外請求另有靜態掃描與 DevTools 紀錄。是否足以滿足 Brief §7「網路已停用的機器」屬 evidence sufficiency → R1 判斷；若要求實體斷網，需 acceptor 親自拔網後開啟解壓的 `index.html` 補一次觀察。
  - **C-2（審查後的 dashboard 修正）**：`e2f391a` 修改了已在 #61～#65 審查過的 `assets/app.js`（k 軸刻度、價格刻度）。不在凍結範圍、不影響 `model_data` 與評估；我判斷屬 #67 被指派的 D-1／D-4／OV-6 (c) 檢查範圍內的 HOW。R1 請核對這兩處 diff。
  - **C-3（測試規則的替換）**：`e2780f4` 把 #65 的「驗收前不得 PASS」測試換成驗收後的規則（§3）。R1 請確認這是契約狀態的轉換而非放寬。
  - **C-4（打包時機）**：完整重跑在 `1f3a8b6` 執行；之後 `99a3ed4`（打包程式）、`e2f391a`（dashboard）改了 `hw2/package.py`、測試與 `assets/app.js`，所以 `meta.test_evaluation.code_revision` 是 `1f3a8b6`，而 ZIP 由 `e2f391a` 打包。兩個 commit 之間，除了 `2cd2a70` 寫入的這次執行產物（`hw2.ipynb` 的輸出、兩個 `model_data`）之外，沒有改動 notebook source 或任何選擇與評估模組（`git diff --stat 1f3a8b6 e2f391a` 只有 `hw2/package.py`、`tests/test_package.py`、`assets/app.js` 與上述執行產物）。
  - **C-5（Firefox 的限制）**：見 §8.3；best effort，不影響 required gate。
- **Remaining work**：R1（含 S-4 學號比對自行重做）；Spec Integration Audit；DA phase acceptance；push 授權（run record §9，S-3 每次 push 前重跑比對）；合併（RB-1）後的 Pages Lightweight work item（AD-3）；iLearning 繳交（RB-2，acceptor）。繳交檔案：`home_work_02/dist/<學號>_hw2.zip`（sha256 `c84a3c5e…3fb6`）。
- **執行時間（Q34）**：venv＋安裝 3 min 1 s；條件 7(a) 47.3 s；完整執行 41.3 s；pytest 約 50 s；打包（含報告建置）15 s；OV 檢查每個瀏覽器約 41 s。
