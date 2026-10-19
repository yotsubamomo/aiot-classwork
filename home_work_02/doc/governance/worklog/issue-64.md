# Worklog — issue #64（HW2 T5 五大假設診斷、模型解釋與 Deployment）

- **Work item**：GitHub issue [#64](https://github.com/yotsubamomo/aiot-classwork/issues/64)，run `run-20261018-hw2-formal`（Formal，並行度 1）。
- **狀態**：實作與 self-verification 完成，待 Orchestrator 核對 binding 並派 R1。本檔不代表 audit 或 closure。
- **Subject**：branch `home_work_02-regrill`，base `b34cc50`；**implementation commit `003b825426a500fa2d11ebea584d48c93cd4635d`**（本機，未 push）。本檔以其後的 record-only commit 加入（Bindings §7）。

## 1. Contract reference

| 項目 | 內容 |
| --- | --- |
| Ticket | #64（OPEN，`ready-for-agent`；含 TR-02 修訂後的重複交易文字、DA TK-2（診斷與解釋圖 PNG）、I-1／TK-5（「Fit」＝training set）的 AC；高風險 H-2、H-3、H-4）；索引 `doc/ticket/tickets.md` |
| Spec | `doc/spec/SPEC.md` rev 5（#59）：「診斷與解釋」、「特徵選擇與模型」的最終模型、「預測區間」（PI 假設、SR-08／SR-12 措辭）、Dashboard（區塊 (9) 方法與限制；選配係數表與其來源標示）、「報告與打包」的三種標示 |
| DA derivation | `decisions/derivation-SPEC.md` §9.1（#64：B-6、B-7；H-3、H-4）、§9.2（#64 只依賴 #62）、§9.3（Test 時序，條件 1–6）、§9.4 I-1、I-2、I-3、§9.5 TK-2、TK-5、§9.6 TR-01、TR-02 |
| 其他 DA 紀錄 | `decisions/decision-20261018-high-risk-categories.md`（H-2、H-3、H-4；A-1、A-2、A-5、A-7、A-8）；`decisions/decision-20261018-issue60-a4-student-id.md`（S-1；§2.2 #64 加標 H-2）；`decisions/decision-20261018-issue62-shared-subset-test-key.md`（D-2：最終模型以整體 CV winner 的身分呈現）；`decisions/decision-20261018-issue63-js-tolerance.md`（T-1） |
| 前票 follow-up（owner＝#64） | `audit/issue-63-c1-r1.md` F-1、F-2 |
| Outcome Contract | `doc/governance/outcome-contract.md`：Brief @ `dff7c55c`＋CC-1（第 3 點：每個模型只一次 Test 評估）、AD-1～AD-3 |
| 授權與派工約束 | `run/run-20261018-hw2-formal.md` §1 designation 第 2 點（Implementation）、第 3 點（SA-1 本機 commit；不 push、rebase、merge、force push）；Orchestrator 2026-10-18 的派工約束：正式 Test 評估已在 #63 執行一次，本票不得再執行、不得重新開啟守門、不得重新評估或重寫 `test`／`test_inputs`；只修改 `home_work_02/`（不含 `doc/requirement/`）；不寫入實際學號、acceptor 材料、金鑰；不建立 `.local/packaging.json` |
| UI 參考 | `design/` Wireframe v0.2（UI 決策 5：係數表預設收合；方法與限制四段的版面只作參考，沒有沿用 mock 數值或計算） |
| Bindings | b5；HOW `impl-default` v2（overrides none） |

## 2. Executing role and binding

- **角色**：Executor（`gov-executor` subagent，由 Orchestrator 派工）。
- **Binding 觀測**（Bindings §3.6 的同一邏輯，掃描本 subagent 的 transcript `subagents/agent-a2b1c8f4cc400f3be.jsonl`，`meta.json` 的 `agentType`＝`gov-executor`）：implementation commit 之後觀測 `('claude-opus-5-5', 'high')` 217 則，單一元素，等於 O-1 mapping。全程核對（含之後的訊息）由 Orchestrator 在採用 return 前執行。
- **Escalation／替代**：無。**Bounded assignments**：未使用。

## 3. Work performed

### 3.1 產物（commit `003b825`，31 個檔案，全部在 `home_work_02/` 內，沒有 `doc/requirement/`）

| 路徑 | 內容 |
| --- | --- |
| `hw2/deployment.py`（新增） | `final_model()`：整體 CV winner 的 canonical subset 在整個 training set 上重新擬合，並逐位元核對等於該候選的 canonical fit；以整體 winner 自己的方法與 k 呈現，`shared_with` 列出共用同一擬合模型的其他 winner（D-2）。`predict_price()`：原始 CSV schema 的列（DataFrame／dict／list；`date` 接受 CSV 或 ISO）→ 點預測、95% PI、未見 zipcode 與超出 training 範圍的標示。`save_pipeline()`／`load_pipeline()`（pickle；非正式資料不得寫入單元）。`training_rows()`：只接受資料階段的 training 列，含 test 列位置即拒絕 |
| `hw2/diagnostics.py`（新增） | 五大假設（第 3.2 節）；`summary_table`（違反一律標「揭露，不判失敗」）；圖（matplotlib `Figure`，不經 pyplot）與 CSV；非正式資料不得寫入單元 |
| `hw2/explain.py`（新增） | 係數表（log 尺度係數、古典 SE、每單位與每 1 個 training 標準差的百分比、zipcode 相對基準）；group permutation importance（training 列、10 次、固定串流 `[SEED, 2]`） |
| `hw2.ipynb` | 5.6（最終模型與五大假設，含 5.6.1–5.6.5）；第 6 章 6.1 dashboard、6.2 模型解釋（標示「依老師補充建議」；permutation importance 標「專案延伸」）、6.3 `predict_price()`（含與 `fit` 直接計算的核對）、6.4 pickle 示範（不屬於 dashboard）、6.5 使用限制。執行方式見第 4 節 |
| `results/figures/*.png`（7 張）、`results/tables/` 5 個 CSV、`results/deployment/final_model.pkl` | TK-2：診斷圖、解釋圖與其數字表；pickle 示範檔 |
| `index.html`、`assets/app.js`、`assets/style.css` | F「方法與限制」四段（特徵選擇方法〔老師要求〕、訓練 CV／Test 協定〔專案延伸〕、預測區間的統計假設〔老師要求〕、限制與非因果解讀〔依老師補充建議〕）、三種標示的圖例、導覽連結；適用期間由 `MD.inputs.date_range`（training）填入。選配係數表在「全訓練集擬合」卡內，`<details>` 預設收合，摘要標「全訓練集擬合，R²／Adjusted R² 為 log 尺度」，只讀所選模型的 `fit` |
| `tests/` | 新增 `test_deployment.py`、`test_diagnostics.py`；`test_notebook_structure.py`（六章都有內容；5.6 與第 6 章的必要陳述；這些 cell 不引用任何 test 端名稱；已執行）、`test_dashboard_static.py`（四段三標示、係數表收合與來源）；F-1、F-2（第 3.4 節） |
| `README.md`、`hw2/__init__.py`、`hw2/paths.py`、`.gitattributes` | 檔案配置與模組清單（不抄數字）；新結果路徑；PNG／pkl 標為 binary。README 的安裝與執行步驟沒有改變 |

`results/model_data.json`、`assets/model_data.js`、`results/split/`、#63 的三個結果表都沒有改變（第 5 節 V-6）。

### 3.2 重要決定（HOW）

- **診斷統計量**（Spec「統計量由實作選」）：線性＝殘差 vs 擬合值（20 個等量分箱平均）＋Ramsey RESET（標準化擬合值的平方、立方）；獨立＝依交易日期的 Durbin–Watson＋training 的重複交易（列數 − 唯一 `id`，程式計算）與同一房屋相鄰兩次交易殘差的 Pearson 相關；全資料 177 只作背景、標「全資料層級」（TR-02）；同質變異＝尺度—位置圖＋Koenker Breusch–Pagan（全部欄位，另附只對擬合值）；常態＝studentized 殘差 Q–Q＋Jarque–Bera、偏態、超額峰態、尾部比例；多重共線性＝group 內（多欄 group 只在自己的欄之間的最大 VIF）、group 間（GVIF、GVIF^(1/(2·df))）、每欄 VIF、相關矩陣與含截距設計矩陣的條件數。參考值（VIF 10、√10、30）是慣例，只用於閱讀。
- **古典假設與 PI 假設分開陳述**（SR-08／SR-12）：notebook 5.6、6.5 與 dashboard 都寫明診斷不能證明或否定 PI 的 95% 涵蓋，並重述「不宣稱保證 95% 的經驗涵蓋率」。
- **Permutation importance 的指標**：先以 USD RMSE 試算，數個 group 出現穩定的負值（OLS 不最小化 USD 誤差），不適合解讀；改以 ln(price) 尺度的 in-sample RMSE 增加排序，USD 只作參考欄，並在 notebook 說明。這只用於解釋（B-6），不影響任何選擇。
- **最終模型的取得**：refit 而不是直接沿用候選物件，並以位元相等核對；pytest 另以真實 training 列 refit，與 `model_data` 匯出的 `fit` 比對（rtol 1e-12）。
- **Dashboard 係數表不提供「每 1 個標準差」欄**：training 標準差不在 `model_data` 中，加入需要重寫 `model_data`（違反派工約束），所以 dashboard 只列係數、SE 與每單位百分比，標準化的讀法放在 notebook 6.2 與 CSV。
- **標示的分配**：依 Brief §3 的來源標記——特徵選擇與預測區間是 [T]（老師要求）；五大假設與模型解釋是 [S]（依老師補充建議）；分組 CV／一次性 Test 的協定與 permutation importance 是本專案的設計（專案延伸）。協定一段同時寫明「模型評估本身是老師的要求」。見第 7 節 C-2。

### 3.3 實際結果摘要（training set；全部由 notebook 輸出與 `results/tables/` 引用）

最終模型＝Lasso 路徑排序 k=17（`lasso_path_k17`；與 Forward SFS k=17、Backward SFS k=17 為同一擬合模型，Test 在 #63 以 `forward_sfs_k17` 評估一次）。五項診斷在 training 殘差上都偵測到偏離，全部依規則揭露：RESET 顯著；同一房屋相鄰交易殘差 r＝0.335（141 對；training 重複交易 141 筆、140 棟），Durbin–Watson 1.966；Breusch–Pagan 顯著；Jarque–Bera 顯著、超額峰態約 3；`lat`、`yr_built`、`long` 的 GVIF^(1/(2·df)) 超過 √10，相關矩陣條件數 47.1。Permutation importance 第一名是 `zipcode`。這些數字只是本檔的索引，報告應引用匯出的 CSV。

### 3.4 前票 follow-up（`audit/issue-63-c1-r1.md`，owner＝#64）

| Finding | 處理 | 證據 |
| --- | --- | --- |
| F-1 (1) 平手測試沒有呼叫被測程式 | `test_select_alpha_breaks_a_real_tie_toward_the_larger_alpha`：monkeypatch `_fit_coefs` 讓每個 alpha 得到相同擬合，斷言曲線真的平手，再由 `select_alpha` 選出最大 alpha（Ridge、Lasso 各一次）；原測試中自行計算平手的部分移除 | mutant M15（平手改取較小 alpha）DETECTED |
| F-1 (2) 沒有只違反 argmin 的竄改 | `test_an_alpha_that_is_not_the_cv_argmin_is_rejected`：以 `dataclasses.replace(sel, alpha=內部非最佳點).to_entry()` 產生 `cv`、邊界旗標都一致、只有 argmin 不成立的 entry，斷言錯誤訊息是 argmin 那一條 | mutant M14（argmin 檢查停用）DETECTED |
| F-2 conftest 不涵蓋 session／module fixture | `tests/conftest.py` 加 `pytest_configure`：整個測試 process 在任何 fixture 之前關閉正式守門；function 範圍的還原保留；docstring 改為實際保證；`test_testgate.py` 新增以 session 與 module fixture 讀取旗標的測試 | mutant M16（移除 `pytest_configure` 的關閉）DETECTED |

## 4. Notebook 的執行方式（不觸發第二次 Test 評估）

- 守門自 #63 起是開啟的（`OFFICIAL_TEST_GATE_ENABLED = True`），完整執行 notebook 會在 cell 41 再做一次評估，違反派工約束，所以**沒有執行 `hw2.run_notebook`**。
- 改以 scratchpad `ex64/run_partial.py` 在**單一 kernel**（cwd `home_work_02/`）中：(0) 以 `store_history=False` 先把該 kernel 的 `hw2.testgate.OFFICIAL_TEST_GATE_ENABLED` 設為 `False`（任何開啟守門的嘗試都會失敗）；(1) 依序執行 5.6 之前的全部 code cell，**排除** 4 個 test 端 cell（index 41、42、44、45，即 #63 的執行序號 25–28：`gate.open`／`gate.evaluate`／讀匯出的 `model_data`），這些 setup cell 在副本上執行，notebook 中保留 #63 的原始輸出；(2) 執行 #64 的 11 個 code cell，只把它們的輸出寫回；(3) 檢查。
- 執行紀錄（`ex64/run_partial.log`，2026-10-18T14:57:10Z–14:58:29Z，setup 70.5 s、#64 cell 7.9 s）：kernel 內 `_official_test_rows_loaded` 為 False、旗標為 False；kernel 中沒有 `gate`、`evaluation`、`model_data` 名稱；由 kernel 狀態重算的 selection digest＝`44f7723e4023afc3e8e997f42bf4eb59db392af81cced11743757a9857cb4b28`（＝#63 pre-gate 值），所以新 cell 使用的 training 端狀態就是正式執行的狀態。
- 結果：cell 0–45 與 `b34cc50` 的 JSON 完全相同（含輸出與 notebook metadata）；新 cell 的執行序號是該 kernel 的實際序號 25–35（setup 的 24 個 cell 佔 1–24，與 #63 相同），所以與 #63 的 25–28 重疊。Notebook 因此**不是單一次完整執行的輸出**（見第 7 節 C-1）。

## 5. Self-verification

環境：Windows 11、i9-13900HX、Python 3.11.2（單元 `.venv`）、Node v24.19.0、Chrome 155.0.8059.80、Edge 155.0.4283.62（headless）。腳本與輸出都在 session scratchpad 的 `ex64/`。

| # | 方法 | 結果 |
| --- | --- | --- |
| V-1 | 完整 pytest（工作樹＝`003b825`）`.venv/Scripts/python -m pytest -q -rs -p no:cacheprovider` | **314 passed、1 skipped**（skip＝學號設定未提供），89.6 s（baseline `b34cc50`：281 passed） |
| V-2 | Node `node --test tests/js/core.test.js` | 9 pass、0 fail、3 skip（fixture 項目由 pytest 執行） |
| V-3 | `python -m hw2.offline_scan` | `scanned 6 files: PASS (0 findings)` |
| V-4 | AC：`predict_price()` 等於以 `fit` 直接計算 | 測試自寫 encoding（不呼叫 hw2 前處理或預測），人工構造的列（ISO／CSV 日期、整修與未整修、已見與未見 zipcode、超出範圍）與 training 列：點預測與上下界 rtol 1e-12 相等；notebook 6.3 也以 `fit` 直接計算核對 4 列。示範與測試都沒有使用 test 列 |
| V-5 | AC：診斷與 permutation importance 只用 training 列 | `test_changing_the_test_rows_changes_no_diagnostic_or_explanation`：synthetic 資料把全部 test 列的價格與 7 個特徵改掉（含未見 zipcode、日期），全部診斷數字、殘差、VIF、係數表、permutation 表都不變；`training_rows` 拒絕含 test 列位置的輸入；notebook 靜態測試：5.6 與第 6 章的 code 不含 `model_data`、`evaluation`、`gate`、`test_inputs`、`test_rows` 等名稱 |
| V-6 | #63 產物不變 | `results/model_data.json` sha256 `fa86d76c…b891e3`、`assets/model_data.js` `37626bf9…5b29a72`、`split_assignment.csv`、`alpha_cv.csv`、`comparison.csv`、`cv_by_method_k.csv` 的 sha256 與執行前相同；`export.result_digest`＝`b53ff286ae0734add8b272089aba904a1cb7f5aca444a62d356420b25dc3cfc6`（＝#63 §5） |
| V-7 | 正式最終模型 | pytest：真實 training 列 refit 等於匯出的 `fit`（coef、(XᵀX)⁻¹、s²，rtol 1e-12）；追蹤的 pickle 的 model key、test key、資料 sha256、groups、coef、(XᵀX)⁻¹ 等於 `model_data`，`shared_with` 等於 winners 推得的共用者 |
| V-8 | 統計量正確性 | 殘差／槓桿／studentized 殘差對直接 hat matrix；RESET 對直接巢狀 lstsq；BP＝n·R²；JB、偏態、峰態對 scipy；欄位 VIF 對直接回歸、單欄 GVIF＝VIF、group 內 VIF＝1/(1−ρ²)；DW 與重複交易配對的手算案例 |
| V-9 | 產物可重現 | `ex64/determinism.py` 以獨立 process（快取的 training 端狀態、不碰守門）重新產生 7 張 PNG、5 個 CSV 與 pickle，13 個檔案與單元內的檔案位元相同（最後一次在最終程式碼上執行） |
| V-10 | Mutation probes（`ex64/mutants64.py`，單元的 scratch 複本） | 20 個 mutant **全部 DETECTED**（M1–M13 新模組與測試；M14–M16 F-1、F-2；M17–M19 dashboard 收合、標示、係數表讀 Test；M20 RESET df）；未變異複本 91 passed |
| V-11 | Dashboard（`file://`、主機名稱全部無法解析，CDP，`ex64/page_check64.js`；Chrome 與 Edge） | 1440／768／375 px：沒有例外、console error、非 file 請求（6 個本機檔）；7 種狀態（初始收合、鍵盤 Enter 展開、Lasso winner、Lasso k=3、比較全部、Forward、鍵盤 Space 收合）頁面水平溢出都是 0。方法與限制：4 段、標示各一（老師要求×2、專案延伸、依老師補充建議）、圖例、期間 2014-05-02 至 2015-05-27 由 `inputs` 填入；1440 兩欄、≤1024 一欄。係數表：初始收合；列數隨選取模型（All-in 88、k=17 87、k=3 4）；375 px 時表格在自己的容器內捲動。截圖 `shot_chrome_*_methods.png`、`*_fitcard.png` |
| V-12 | Notebook | 新 cell 都有輸出、沒有錯誤；7 張圖以 `display` 呈現；pickle 重新載入後同一筆預測相同 |

- **A-4（S-1）**：`git ls-files` 的 PDF 只有老師文件；沒有 `.zip`、`.env`、`kaggle`、`.local/`、`acceptor_materials/`、`dist/`；沒有建立 `.local/packaging.json`。本票新增行中「學號」只出現在本 worklog 的敘述（2 次），後面沒有數字；7 位以上數字串只有日期（`20140615`、`20140720`、`20141013`、`20141209`、`20150101`、`20150210`、`20261018`）；PNG base64 與浮點小數位除外。Commit message 沒有長數字。過程中沒有印出任何疑似值。**實際學號比對 NOT VERIFIED**（學號設定尚未提供；依 S-1）。
- **H-2**：notebook 六章名稱與順序不變（`test_six_crisp_dm_chapters_in_order`）；`index.html` 路徑不變；新增的頁面內容沒有任何外部資源（掃描 PASS、CDP 只請求本機檔）。
- **Git**：commit message 依規則、沒有 Claude 標記；未 push、rebase、merge、force push。

## 6. Audit status

Required（Formal；H-2：notebook Evaluation／Deployment 章節、README、dashboard 新區塊；H-3：最終模型、診斷與解釋只用 training、test 未被再評估；H-4：三種標示與非因果、不宣稱 95%）。依 A-1 需要 R1 record 的類別核對節；依 A-2 Reviewer 自行執行 pytest／Node 與重算；依 A-5 核對沒有 mock 數值或 wireframe 截圖。尚未派工（由 Orchestrator 依 Bindings §3.7）。本檔的 self-verification 不是 audit。

## 7. Concerns 與所需 authority

| ID | 內容 | Required authority |
| --- | --- | --- |
| C-1 | **Notebook 的輸出來自兩次執行**：cell 0–45 是 #63 正式執行（run `fe76019b…`）的輸出，5.6 與第 6 章是 #64 的部分執行（第 4 節）。Spec 要求數字可追溯到「一次可重現的執行」；新 cell 的數字可由 #67 的乾淨環境完整重跑重現（DA §9.3 視為重現，不是新評估），屆時 notebook 才回到單一執行。若 Orchestrator／DA 認為 #64 結案前就必須是單一執行，那需要先決定完整重跑與 CC-1 第 3 點、派工約束的關係 | Design Authority（是否需要在 #67 之前處理） |
| C-2 | 「方法與限制」四段的標示分配（特徵選擇〔老師要求〕、評估協定〔專案延伸〕、PI〔老師要求〕、限制與非因果〔依老師補充建議〕）依 Brief §3 的來源標記；評估協定一段是設計選擇，與 wireframe 的參考標示不同（wireframe 把特徵選擇標為補充建議）。若 Reviewer 認為應不同 | Reviewer（爭議時 Design Authority） |
| C-3 | 票 AC「報告草稿的解釋段落標『依老師補充建議』與『專案延伸』」：報告檔由 #65 建立（derivation §9.1；與 §9.4 I-3、#63 R1 AC-8 同型），本票把這兩個標示放在 notebook 6.2（報告的來源）。報告版由 #65 負責 | 無（若有不同解讀 → Design Authority） |
| C-4 | 診斷結果五項都偵測到偏離（第 3.3 節），依規則揭露、不判失敗；#65 的報告需要連到 5.5 的涵蓋率說明（Brief §6），不得以此修正區間 | 無（告知 #65） |

## 8. Remaining work

- #64 R1（Orchestrator 派工）。學號比對 S-2～S-5；push 依 run record 選項 (a)。
- #65：報告引用 `results/figures/`、`results/tables/` 的診斷與解釋（TK-2 的報告核對）；C-3、C-4。#67：乾淨環境完整重跑（C-1）。
- **Scratchpad 產物**（不在 repo）：`ex64/`——`state.py`／`state.pkl`、`smoke.py`、`edit_nb64.py`、`edit_tests64.py`、`run_partial.py`／`run_partial.log`、`determinism.py`、`mutants64.py`／`mutants64.out`、`page_check64.js`、`pc64_chrome.json`、`pc64_edge.json`、截圖、`hw2.head.ipynb`。

## 9. 執行時間量測

- 工作時間：2026-10-18 約 14:20Z 至 15:10Z（22:20–23:10 +0800）。
- Baseline pytest（`b34cc50`）281 passed、1 skipped，48.2 s；最終 pytest 314 passed、1 skipped，89.6 s。
- Training 端狀態（資料、四個路徑方法、Ridge／Lasso CV，沒有守門）94.0 s；部分執行：setup 70.5 s、#64 cell 7.9 s（診斷約 0.9 s、解釋約 2.9 s）。Mutation probes 20 個約 1.5 分鐘。
