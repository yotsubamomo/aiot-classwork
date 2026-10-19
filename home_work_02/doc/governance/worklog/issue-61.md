# Worklog — issue #61（HW2 T2 All-in baseline 端到端：fit、PI、test 守門、dashboard 垂直切片）

- **Work item**：GitHub issue [#61](https://github.com/yotsubamomo/aiot-classwork/issues/61)，run `run-20261018-hw2-formal`（Formal，並行度 1）。
- **狀態**：cycle 1 的 targeted correction（R1 F-1）完成，待 Orchestrator 核對 binding 並派 R2（本檔不代表 audit 或 closure）。修正紀錄見第 8 節。
- **Subject**：branch `home_work_02-regrill`，base `bbf0ed5`；R1 受審的實作 commit `c9b106cbc0a8e19bc42d5d6fd4b20d0150e1a8f1`；**修正後的實作 commit `77b79f4e2b775d331bc7f4be3da42354033b1c0c`**（parent `9b47896`；本機，未 push）。本檔另以 record-only commit 加在其後（Bindings §7）。

## 1. Contract reference

| 項目 | 內容 |
| --- | --- |
| Ticket | #61（OPEN，`ready-for-agent`；含 TR-01 修訂後的 AC、「Test 時序」與「Test 資料隔離」共同條款、DA TK-3、I-3 兩條 AC）；索引 `doc/ticket/tickets.md` |
| Spec | `doc/spec/SPEC.md` rev 5（#59）：「指標與推論」（秩不足三類）、「預測區間」、「`model_data` 契約」的 `baselines.allin`／`winners`／`test[kind=ols_subset]`、Dashboard（KPI、即時預測器、test 區塊、實際 vs 預測圖、SR-07、SR-09）、Testing Decisions 主 seam 與次 seam「模型與推論」「選模」 |
| DA derivation | `decisions/derivation-SPEC.md` §3 B-3（UI 不以 `test_inputs` 評估）、B-4、B-8、B-10；§9.1（#61 的分配）、§9.3 條件 4、5、§9.4 I-3、§9.5 TK-3、§9.6 TR-01；§11 G-3 |
| 高風險 | `decisions/decision-20261018-high-risk-categories.md`：#61 觸及 H-2、H-3（A-1～A-3）；A-4 的實際學號部分依 `decision-20261018-issue60-a4-student-id.md` S-1 |
| #60 R1 的 follow-up | `audit/issue-60-c1-r1.md` F-1、F-3（owner＝#61），處理見 3.3 |
| Outcome Contract | `doc/governance/outcome-contract.md`：Brief @ `dff7c55c`＋CC-1、AD-1～AD-3 |
| 授權 | `run/run-20261018-hw2-formal.md` §1 designation 第 2 點（Implementation）、第 3 點（SA-1 本機 commit；不 push） |
| UI 參考 | `design/` Wireframe v0.2（只作版面參考；沒有沿用 `mock-data.js`／`wireframe.js` 的任何計算或數值） |
| Bindings | b5；HOW `impl-default` v2（overrides none） |

## 2. Executing role and binding

- **角色**：Executor（`gov-executor` subagent，由 Orchestrator 派工）。
- **Binding 觀測**（Bindings §3.6 的同一邏輯，掃描本 subagent 的 transcript）：agentId `af27ea1586955f943`（`agent-af27ea1586955f943.meta.json` 的 `agentType` = `gov-executor`），實作 commit 之後觀測 `('claude-opus-5-5', 'high')` 227 則，單一元素，等於 O-1 mapping。全程核對（含之後的訊息）由 Orchestrator 在採用 return 前執行。
- **Escalation／替代**：無。
- **Bounded assignments**：未使用（沒有派 `gov-investigator` 或 `gov-bounded-worker`）。

## 3. Work performed

### 3.1 產物（commit `c9b106c`，30 個檔案，全部在 `home_work_02/` 內，不含 `doc/requirement/`）

| 路徑 | 內容 |
| --- | --- |
| `hw2/ols.py` | 新增。OLS（log(price)、原始尺度的設計矩陣含截距）；rank 由欄位等化後的 column-pivoted QR 判定（容差同 numpy `matrix_rank`）；秩不足時拋 `RankDeficientError`，不刪欄；係數、(XᵀX)⁻¹、df_resid＝n−rank、s²、log 尺度 R² 與 Adjusted R²＝1−(1−R²)(n−1)/(n−rank)、t(0.975, df)；PI 以匯出的 (XᵀX)⁻¹ 依 Spec 公式計算後 exp 回 USD |
| `hw2/metrics.py` | 新增。USD 的 MAE／MSE／RMSE／R²；閉區間 coverage、涵蓋筆數、平均寬度、二項近似 1.96·√(p(1−p)/n)，附獨立性假設的說明文字 |
| `hw2/models.py` | 新增。候選 (方法, k)：每個 fold 只以該 fold 訓練列 fit 前處理與 OLS、在驗證列算 USD 指標（各折值、平均、ddof=1 標準差），另在整個 training set 做 canonical fit；秩不足三類語義（3.2）；`fit_allin`；`determine_winners`（平手規則、授權集合、`complete`）；契約項目 `to_entry()` |
| `hw2/testgate.py` | 新增。G-3 守門（3.3） |
| `hw2/fixture.py` | 新增。synthetic 資料產生器與走同一條程式路徑的 fixture run；fixture `model_data` 只寫到單元目錄以外；`python -m hw2.fixture <dir>` 產生 fixture 版 dashboard 複本（OV-6 量測用） |
| `hw2/contract.py` | 擴充 `validate_model_data`：`methods`／`baselines` 沒有 test 欄位；`baselines.allin` 是 18 group 的單一 OLS；有效項目必有 USD `cv` 與 log `fit`（滿秩、尺寸一致）；`winners` 只指向有效項目、不含 metric-only；`test` 的 `ols_subset` 鍵集合＝授權清單、`metric_only` 只限 Ridge／Lasso 且沒有 PI 欄位；逐筆 covered、n_covered、coverage、平均寬度與 `test_inputs` 一致；`test_inputs` 列與 `test` 必須同時存在 |
| `hw2/export.py` | `build_model_data` 加入 `baselines.allin`、`winners`、`methods`、`test`（只來自守門的評估結果）；`write_model_data` 每次寫入都跑 `validate_model_data`，並在守門關閉時拒絕把 test 結果或 `test_inputs` 列寫到正式路徑 |
| `hw2/data.py` | 全資料讀取改為私有 `_read_csv`；新增 `structural_facts()`（只回傳結構事實）；`PreparedData.source_path` |
| `hw2/preprocess.py` | `sale_days` 與 zipcode one-hot 向量化（結果相同；錯誤行為不變，既有測試全過） |
| `hw2/__init__.py` | 模組清單 |
| `assets/hw2core.js` | 新增。dashboard 自己的前處理（日期天數、整修旗標與有效年份、依模型 fit 類別的 one-hot、未見 zipcode→基準並回報）與點預測＋PI；瀏覽器與 Node 共用；不含任何指標、coverage 或選模計算 |
| `index.html`、`assets/app.js`、`assets/style.css` | B/C：方法選單（列出 `model_data` 中存在的方法；正式資料只有 All-in，k＝18 固定）、選取摘要、KPI（`cv`，標「訓練 CV（USD）」）、全訓練集擬合卡（標「全訓練集擬合，R²／Adjusted R² 為 log 尺度」）；D：即時預測器（只列 `fit.uses_source_features`、原始值、training 中位數預設、zipcode 下拉只列 fit 類別並標基準、未整修勾選、超出範圍警告仍計算、網址參數帶入未見 zipcode 時以基準計算並警告）；E：Test 區塊（標「Test 評估（USD）」與展示模型；選取模型與 Test 模型不同時的提示；Test KPI；canvas 實際 vs 預測圖：全部列、log 刻度、y=x、逐筆 PI 線段、落入／未落入以顏色與形狀區分、滾輪縮放、拖曳平移、按鈕、鍵盤、游標讀取單筆；涵蓋統計六卡與二項近似、PI 假設的說明）；沒有 `test` 時顯示「Test 評估尚未執行」；手機選單 |
| `hw2.ipynb` | 第 4 章 4.1 All-in（CV 表、平均／標準差、fit 統計）；第 5 章 5.1 winners（未完成）與 CV winner 樂觀偏誤、5.2 PI 定義與假設、條件中位數、不宣稱保證 95%、二項近似與不陳述方向、5.3 守門關閉的示範、5.4 匯出 `model_data`；3.4 改為只寫切分紀錄 |
| `results/model_data.json`、`assets/model_data.js` | 重新產生：`meta`、`preprocess`、`inputs`、`baselines.allin`、`winners`（`complete: false`、授權清單只有 `allin`）、`test_inputs`（schema、0 列）；沒有 `test` |
| `tests/` | 新增 `test_ols.py`、`test_models.py`、`test_testgate.py`、`test_test_section.py`、`test_node_core.py`、`js/core.test.js`；修改 `conftest.py`（session fixture run）、`test_contract_fixture.py`、`test_dashboard_static.py`、`test_data.py`、`test_model_data_official.py`、`test_notebook_structure.py` |
| `README.md` | 重跑步驟加 Node 測試與 fixture dashboard 指令；檔案配置 |

### 3.2 重要決定與假設（HOW）

- **秩不足三類**（Spec「指標與推論」SR-04、SR-10）：(1) fold 訓練列缺少某 zipcode→該 fold 沒有那一欄、fit 成功，驗證列的該 zipcode 編為基準並計數（`n_valid_unseen_zipcode`），每個 fit 記錄類別清單與基準；(2) fold 設計矩陣秩不足→該 fold `valid: false` 附原因，整個 (方法, k) `invalid`（`fold_rank_deficient`），CV 平均為 null；canonical fit 秩不足→`canonical_rank_deficient`、沒有 `fit`；invalid 不會成為 winner，dashboard 不提供預測；(3) All-in 在任一 fold 或整個 training set 秩不足、某方法沒有有效候選、整體 winner 無法決定→`ExperimentFailure`，列出全部 invalid 候選與原因。
- **Winners 的部分狀態**：路徑方法屬 #62，所以正式 `winners` 為 `complete: false`、`overall: null`、`pending_methods` 列出四個方法、`authorized_test_models: ["allin"]`。守門拒絕不完整的 winners。方法識別碼 `forward_sfs`、`backward_sfs`、`rfe`、`lasso_path`，模型鍵 `allin`／`<method>_k<NN>`；整體 winner 平手依 Brief §5 的 A→E 順序（`allin` 最先）。這些是 #62 可沿用的 HOW，不是語義決定。
- **CV 標準差**用 ddof=1，記在 `cv.std_ddof`。
- **方法選單**：dashboard 依 `model_data` 實際存在的方法產生選單與 k 按鈕（fixture 有 stand-in 候選，所以方法／k 切換可量測）；完整的 k＝1…18 格子、比較全部、指標 vs k 圖仍屬 #62。
- **Fixture 的路徑方法**：#62 之前沒有選擇方法，fixture 以固定的 stand-in 子集（`fixture.FIXTURE_SUBSETS`，非選擇結果）讓 winners 完整、守門可以開啟；只出現在 fixture `model_data`（`meta.fixture: true`、`fixture_note`），不在追蹤檔中。
- **容差 1e-6** 以 USD 絕對值檢查（最嚴格的讀法）；Python 與 numpy 重算、Node 重算都通過。
- **OV-6 量測方式**：`window.HW2_PERF.firstDraw`＝navigation start（`performance.timeOrigin`）到散佈圖第一次完整繪製結束的 `performance.now()`；`interactions[]` 每筆有 `ms`（input event 的 `timeStamp` 到受影響區塊重繪完成）、`handler_ms`（只算處理函式內部，用來區分排隊時間）與 `visibility`；頁面上 `#scatter-perf` 也顯示首次繪製與最近一次互動。
- 本票沒有需要 DA 裁決的語義問題。

### 3.3 Test 資料隔離（TR-01、H-3）、G-3 與 #60 R1 follow-up

- **守門（`hw2/testgate.py`）**：每次執行一個 `TestGate`，初始 `closed`。`open(winners, alphas)` 只接受完整的 winners（四個方法的 CV winner 與整體 winner 都已決定）與全部 metric-only 模型（只允許 `ridge`、`lasso`）已固定的 alpha，並凍結一份副本〔更正（第 8 節）：`c9b106c` 實際只檢查**有傳入**的 alpha，省略 Ridge 或 Lasso 仍可開啟——R1 F-1；這句陳述在 `77b79f4` 才成立〕；`evaluate()` 只對凍結的授權清單（`ols_subset`）與凍結 alpha 的 metric-only 模型各評估一次，回傳同一次執行的 `test_inputs` 與 `test`；第二次呼叫報錯，評估中途出錯也結束本次執行；`load_test_rows()` 只在 `evaluate()` 內部可用，其他任何時候拋 `TestGateClosed`。正式資料（以 sha256 識別）在 `OFFICIAL_TEST_GATE_ENABLED = False` 時連 `open()` 都拒絕；另外正式 test 列在同一個 Python process 中最多載入一次。旗標只在 #63 開啟。
- **F-3**：`hw2.data.read_csv` 改為私有 `_read_csv`，模組內沒有任何公開函式回傳完整資料框；正式 test 列的特徵與 `price` 唯一的程式路徑是守門（`test_no_public_function_returns_the_parsed_file`）。
- **F-1**：寫入守門的測試改以 monkeypatch `export.OFFICIAL_PATHS` 指向暫存檔，並在 fixture 結束時核對追蹤的 `model_data` 兩檔 sha256 不變；守門退化也碰不到追蹤檔。
- **本票沒有載入任何正式 test 列**：正式資料只做到守門關閉的斷言（`load_test_rows`、`open`、`evaluate` 都拒絕）；notebook 5.3 示範兩個拒絕；pytest、Node test 與 OV-6 量測只用 synthetic fixture。測試中唯一讀到全部列的是既有的結構測試（#60 AC-4 允許）。`test_official_winners_are_not_complete...` 與 `test_allin_baseline_is_reproduced...` 只用 training 列。
- **追蹤的正式 `model_data`** 沒有 `test`、`test_inputs` 為 0 列（`test_no_test_rows_and_no_test_results_are_tracked`）；寫入端另在守門關閉時拒絕把 test 結果寫到正式路徑（`test_official_paths_refuse_test_results_while_the_gate_is_closed`）。
- **同一條程式路徑**：正式資料（notebook）與 fixture 都經過 `data.load_and_split` → `models.fit_allin`／`evaluate_candidate` → `models.determine_winners` → `testgate.TestGate` → `export.build_model_data` → `export.write_model_data`（含 `validate_model_data`）；差別只有資料檔與正式資料的守門旗標。Fixture 的 `model_data` 只寫到 pytest 暫存目錄與本 session 的 scratchpad（`hw2.fixture` 拒絕單元目錄內的輸出）。
- **B-3**：`assets/app.js` 對 `test_inputs` 只讀列識別與 `actual_price`（繪圖用）以及房屋數／重複交易筆數；唯一的 `Core.predict` 呼叫的輸入是使用者輸入；`hw2core.js` 沒有指標、coverage 或選模程式（靜態測試）。

## 4. Verification

環境：Windows 11 專業版 10.0.26200、13th Gen Intel Core i9-13900HX（32 logical processors）、31.7 GB RAM、Python 3.11.2（`home_work_02/.venv`，依 `requirements.txt`）、Node v24.19.0、Chrome 155.0.8059.80、Edge 155.0.4283.45（皆 headless）。

| # | 方法 | 結果 | 證據 |
| --- | --- | --- | --- |
| V-1 | `.venv/Scripts/python -m pytest -q -rs -p no:cacheprovider`（`home_work_02/`，commit 前的工作樹＝`c9b106c`） | **174 passed, 1 skipped**；skip 是 `test_no_tracked_file_contains_the_student_id`（`.local/packaging.json` 尚未提供） | 本機執行輸出 |
| V-2 | 次 seam「模型與推論」：手算例子（n=5）核對係數、s²、R²、Adjusted R²、(XᵀX)⁻¹、t；PI 與教科書公式 se_pred＝√(s²(1+1/n+(x₀−x̄)²/Sxx)) 一致且在 USD 不對稱；Adjusted R² 用實際 rank；四種秩不足設計（常數欄、重複欄、線性組合、全零欄，尺度差 1e5）都拋錯；大尺度差的滿秩設計 (XᵀX)⁻¹ 與 `inv` 相符；USD 指標與已知上下界的閉區間 coverage | 通過 | `tests/test_ols.py` |
| V-3 | 秩不足三類與選模：合法 encoding（fold 0 獨有的 zipcode：該 fold 少一欄、fit 成功、驗證列以基準計數）；fold 秩不足→invalid、被排除於 winner；canonical 秩不足的非 winner→invalid、沒有 fit、其他候選照常；All-in 共線→`ExperimentFailure` 列出 `allin`；某方法沒有有效候選→停止；winner 平手取小 k、整體平手依方法順序、授權集合去重、invalid 不得勝出、不完整時整體 winner 未定、NaN 時停止；fold 0 的模型不受 fold 0 價格影響 | 通過 | `tests/test_models.py` |
| V-4 | G-3：正式資料下 `load_test_rows`／`open`／`evaluate` 全部拒絕且旗標為 False；正式 winners 不完整；fixture 上：不完整 winners、未固定 alpha、未知 metric-only 被拒；開啟前評估、開啟後在評估外載入被拒；評估一次後第二次報錯、之後載入與再開啟被拒；授權集合多一個或少一個被拒（且不消耗本次執行）；開啟後修改原 winners 不影響凍結副本；metric-only 只經同一守門各評估一次、alpha 不符被拒、只有指標欄位；資料檔在切分後被改動→sha256 錯誤且本次執行結束；守門載入的列＝切分的 test 列 | 通過 | `tests/test_testgate.py` |
| V-5 | 主 seam（SR-02）：fixture `model_data` 寫檔後讀回，以 numpy 只從 `test_inputs` 原始值、`preprocess` 規則與各模型 `fit` 重建設計列（不 import hw2 的預測或前處理），重算全部 5 個 `ols_subset` 模型 × 全部 test 列的點預測、lower、upper（**USD 絕對容差 1e-6**）、covered、n_covered、coverage、平均寬度、MAE／MSE／RMSE／R²、二項近似；`test_inputs` 房屋數與重複交易數；10 種契約違反（covered 竄改、coverage 竄改、未授權鍵、缺少 allin、metric_only 帶 PI 欄位、`baselines` 夾帶 test 欄位兩種、lower 大於 predicted、winners 夾帶 ridge、只有 `test_inputs` 列沒有 `test`）都被拒 | 通過 | `tests/test_test_section.py` |
| V-6 | JS（Node）：`node --test tests/js/core.test.js`（無 fixture：前處理案例 7 項通過、fixture 2 項 skip）；pytest 以 `HW2_FIXTURE_MODEL_DATA` 執行同一檔：9 項全過、0 skip——全部 `ols_subset` 模型 × 全部 test 列的 prediction／lower／upper（1e-6）與 covered 一致；日期天數（基準日、ISO 與 CSV 格式、非法日期）、整修三案例、已知／基準／未見 zipcode、預測＝截距＋Σ貢獻、All-in k＝18、各方法 Test 模型＝winner、invalid 不為 winner、metric-only 不可預測 | 通過 | `tests/test_node_core.py`、`tests/js/core.test.js` |
| V-7 | Dashboard 靜態：script 順序、`node --check`、`python -m hw2.offline_scan` → `scanned 6 files: PASS (0 findings)`；`app.js` 只以使用者輸入呼叫 `Core.predict`、`test_inputs` 只讀識別／實際價格／計數；`hw2core.js` 沒有指標或選模字詞 | 通過 | `tests/test_dashboard_static.py` |
| V-8 | 正式 `model_data`：區段＝{meta, preprocess, inputs, test_inputs, baselines, winners}；`validate_model_data` 通過；`baselines` 沒有 test 欄位；All-in 以 training 列重新擬合後 CV 平均、rank、欄位、類別、係數相同；winners 部分狀態 | 通過 | `tests/test_model_data_official.py` |
| V-9 | Notebook：六章順序；前五章有內容與程式；已執行無錯誤；Evaluation 含「不宣稱保證 95% 的經驗涵蓋率」「條件中位數」「不是條件平均」「二項近似」「不陳述偏差的方向或幅度」、假設三項與 CV winner 樂觀偏誤；`python -m hw2.run_notebook` 執行成功（20.6 s，含 kernel 啟動） | 通過 | `tests/test_notebook_structure.py`；notebook 輸出 |
| V-10 | 正式 dashboard 以 `file://` 在 headless Chrome（所有主機名稱無法解析）於 1440／768／375 px 載入（CDP）：沒有例外與 console error；沒有水平溢出（scrollWidth ≤ innerWidth）；KPI 四卡均標「訓練 CV（USD）」，CV RMSE US$158,154；fit 卡標示正確；預測器 18 個輸入、以中位數預設得點預測 US$503,564、PI US$351,404–US$721,610；Test 區塊顯示「Test 評估尚未執行」、圖不顯示；k 顯示「k = 18（固定）」；請求只有 6 個本機檔（另有一筆瀏覽器內部的 `data:image/svg+xml`，不是頁面檔案引用，`grep svg+xml` 在單元檔案中 0 筆）。網址參數 `?zipcode=99999&sqft_living=20000` → 兩個警告（超出 training 範圍 290–13540 仍計算；「此 zipcode 不在模型的訓練類別中，已以基準類別計算（輸入值：99999）」） | 通過 | scratchpad `page_check.js` 輸出 |
| V-11 | **OV-6 量測方式**（SR-09 (a)(b)(f)(g)；只驗證量測方法，正式 gate 屬 #67）：synthetic fixture dashboard（`python -m hw2.fixture`，n_test **4,291**，全部列逐筆繪製，不抽樣不聚合），以 `file://` 在 headless Chrome 與 Edge 1440×1000 載入，CDP 送真實的滾輪、拖曳、按鈕、方法與 k 點擊，讀 `window.HW2_PERF`。每個瀏覽器 3 次（第 1 次冷啟動）：首次繪製 Chrome 174.3／41.1／36.3 ms、Edge 175.7／46.0／42.0 ms；另以 `--dump-dom` 冷啟動 6 次 178–224 ms。互動最大值（ms，event timeStamp 到重繪完成）：滾輪縮放 Chrome 33.6／27.6／29.9、Edge 25.6／28.8／31.8；拖曳平移 ≤ 1.6；縮放與重設按鈕 ≤ 2.1；方法切換 ≤ 7.0；k 切換 ≤ 1.0。全程 `visibilityState` = visible | 量測方式可用、時間戳可讀取 | scratchpad `ov6_measure.js`、`ov6_chrome.json`、`ov6_edge.json` |
| V-12 | 內建瀏覽器（Chromium 152，pane 474 px）以本機 `http.server`（127.0.0.1）開啟 fixture dashboard：散佈圖、游標讀取單筆（列、房屋、預測、實際、PI、是否落入）、縮放、平移正常；發現兩個缺陷並修正（log 刻度標籤把 200 萬顯示為「2 萬」；放大後刻度標籤重疊；tooltip 超出右緣）。當時 pane 被隱藏，兩次滾輪事件測得 1,054／1,742 ms（頁面在背景被節流，事件排隊），因此加入 `handler_ms` 與 `visibility` 欄位，並改以 V-11 的 headless CDP 量測 | 修正後重測通過 | 本 session 的瀏覽器操作 |
| V-13 | **Mutation probes**（在 scratchpad 的單元複本上；11 個 mutant 全部被測試抓到）：守門允許第二次評估、PI 去掉 leverage、開區間 coverage、JS PI 去掉 leverage、正式守門旗標改為 True、fold fit 看到驗證列、Adjusted R² 分母錯一、忽略秩不足、JS 不回報未見 zipcode、在評估外允許載入、平手取大 k | 11／11 DETECTED | scratchpad `mutants.py` 輸出 |
| V-14 | `tests/test_repo_hygiene.py`（commit 後）：15 passed、1 skipped（學號設定未提供）；新增檔案中 7 位以上數字只有日期樣式（`20261018` fixture seed、日期字串）與 `86400000`（一日毫秒） | 通過；實際學號比對 NOT VERIFIED（依 `decision-20261018-issue60-a4-student-id.md` S-1） | 本機執行輸出 |

**執行時間量測（Q34）**

| 項目 | 時間 |
| --- | --- |
| 資料載入與結構驗證（`meta.timing_s.data_load_validate`） | 0.097 s |
| 切分與 fold（`split_and_folds`） | 0.045 s |
| All-in 5 折 CV（`allin_cv`） | 1.80 s |
| All-in 全訓練集擬合（`allin_canonical_fit`） | 0.33 s |
| 整本 notebook 非互動執行 | 20.6 s（含 kernel 啟動） |
| pytest 全部 | 6–42 s（同一機器不同負載下兩次） |
| fixture dashboard 產生（21,430 列 synthetic） | 4.4 s |

向量化前的 All-in 為 3.2 s（`sale_days` 逐列解析與 zipcode 逐類別比較），向量化後 1.2 s（單獨量測）；這對 #62 的路徑計算成本有幫助，數值結果相同（既有前處理測試與 All-in 重現測試）。

**正式 All-in（training 列）**：CV（USD，5 折平均 ± 標準差）RMSE 158,154 ± 35,930、MAE 75,658 ± 1,070、R² 0.8010 ± 0.0862；fit：n_train 17,290、88 欄、rank 88、df_resid 17,202、R²（log）0.8791、Adjusted R²（log）0.8785、s² 0.03350、t 1.9601。這些只是 training CV 與擬合數字，沒有任何 test 數字。

**限制**：OV-6 只以 headless Chrome／Edge 與 synthetic fixture 驗證量測方法，不是參考環境（acceptor 的電腦、有畫面的 Chrome／Edge）下的正式量測，也沒有記錄「網頁沒有回應」提示的觀察；這些屬 #67。OV-2～OV-5 只做了 375／768 px 無水平溢出的檢查，正式 gate 屬 #67。

## 5. Commit 與 A-4 核對

- **實作 commit**：`c9b106cbc0a8e19bc42d5d6fd4b20d0150e1a8f1`（parent `bbf0ed5`），30 個檔案，全部在 `home_work_02/` 內、不含 `doc/requirement/`。本 worklog 另以 record-only commit 加在其後。
- **未 push**。
- **A-4（對 `c9b106c`）**：新增與修改的檔案沒有 PDF、ZIP、`.env`、`kaggle.json`、`.local/`、`acceptor_materials/`、`dist/`；hygiene 測試 15 passed、1 skipped。實際學號比對 NOT VERIFIED（學號設定尚未提供；依 S-1）；替代證據：本 commit 新增內容中「學號」只出現在既有檔案的 `<學號>` 佔位，新增檔案沒有出現；新增檔案的 7 位以上數字都已分類（見 V-14）；commit message 沒有 7 位以上數字。過程中沒有印出任何疑似值。
- **Scratchpad 產物**（不在 repo）：fixture dashboard `ov6_dashboard/`、其工作目錄、量測與檢查腳本、量測 JSON；本機 `http.server` 已停止。
- **工作時間**：2026-10-18 17:35 至 18:12 +0800。

## 6. Audit status

- **R1（cycle 1）**：`audit/issue-61-c1-r1.md`，VERDICT: BLOCKING (F-1)。Blocking：F-1（Medium，H-3）；non-blocking：F-2、F-3（owner #62）、F-4（owner #63），本票不處理。F-1 以第 8 節的 targeted correction 處理，待 R2。
- **Required**（Formal：每張票都要 independent audit；Bindings §5）。觸及 H-2（dashboard 的資源載入、Test 區塊與預測圖、notebook 的 Modeling／Evaluation 章節）與 H-3（PI、守門、隔離、重算、Python／JS 一致性）：依 A-1 需要 R1 record 的類別核對節，依 A-2 Reviewer 自行執行重算與測試，依 A-3 核對 `methods`／`baselines` 沒有 test 欄位、`test` 鍵集合與 UI 不以 `test_inputs` 評估。
- 進度：尚未派工（由 Orchestrator 依 Bindings §3.7 派 `gov-primary-reviewer`）。本檔的 self-verification（含 mutation probes）不是 audit。

## 7. Remaining work and follow-up

- **#62**：四個路徑方法填入 `methods` 與完整的 winners；dashboard 的 k＝1…18 格子、比較全部、指標 vs k 圖、invalid 標示的完整呈現沿用本票的 `Candidate`、`determine_winners` 與方法選單。Fixture 的 stand-in 子集在 #62 之後可改由實際方法產生。
- **#63**：把 `testgate.OFFICIAL_TEST_GATE_ENABLED` 改為 True 並在 alpha 與 winners 固定後以守門執行唯一一次正式評估（Ridge／Lasso 以 `metric_only` 經同一守門）；`write_model_data` 屆時才接受正式路徑上的 `test`。
- **#67**：OV-6 正式量測（參考環境、有畫面的瀏覽器、無回應提示的觀察、ACCEPTANCE.md 記錄）；可直接使用 `window.HW2_PERF` 與 `#scatter-perf`。
- **學號比對**：依 S-2～S-5，學號設定提供後執行（required authority：acceptor 提供輸入；不是本票結案條件）。
- 未 push（designation 第 3 點）。

## 8. Targeted correction — cycle 1（R1 F-1）

- **依據**：`audit/issue-61-c1-r1.md` §5 F-1 與其 R2 closure 條件 (a)～(e)（以 record 為準）；Orchestrator 2026-10-18 的修正派工（同一 worklog identity、同樣的約束）。F-2、F-3（#62）、F-4（#63）依 record 的 disposition 不在本次修正範圍，沒有修改。
- **是否有爭議**：沒有。F-1 屬本票 AC-2（「alpha 與 winner **全部**固定」「守門同樣適用於 metric_only」），也是 notebook §5.3、commit message 與本 worklog §3.3 已陳述的行為；我接受它是 #61 的 implementation 缺陷，不需要 Design Authority。
- **Binding**：同一個 `gov-executor` subagent（agentId `af27ea1586955f943`）以 SendMessage 續派；修正 commit 之後觀測 `('claude-opus-5-5', 'high')` 275 則，單一元素。沒有 escalation、替代或 bounded assignment。
- **修正 commit**：`77b79f4e2b775d331bc7f4be3da42354033b1c0c`（parent `9b47896`），8 個檔案，全部在 `home_work_02/` 內：

| 檔案 | 修改 |
| --- | --- |
| `hw2/testgate.py` | `open()` 對 `ridge` 與 `lasso` **兩者**都要求有限且大於 0 的 alpha；省略任一個或兩個都拋 `TestGateError`（「alpha of … is not fixed」），守門維持 `closed`；凍結的 alpha 集合因此必為 {ridge, lasso}，`evaluate()` 既有的「metric-only 模型集合＝凍結 alpha 集合」檢查就要求兩個模型都提供（閉合條件 (b)）。模組說明同步 |
| `hw2/contract.py` | `validate_test`：`metric_only` 項目必須恰好是 ridge 與 lasso（R1 探測 C3；record 說可在此一併處理） |
| `hw2/fixture.py` | 新增 `StandInMetricOnly`（固定 alpha、以 training 列 mean ln(price) 的 exp 為常數預測；明確標為 stand-in，不是 Ridge／Lasso 擬合）與 `FIXTURE_ALPHAS`；`run_fixture` 預設以兩個 stand-in 開啟守門並評估；`fixture_note` 註明 stand-in。輸出仍只在單元以外 |
| `tests/test_testgate.py` | 既有測試改以兩個 alpha 與兩個 stub 開啟與評估；新增 `test_gate_refuses_to_open_unless_both_metric_only_alphas_are_fixed`（6 種：兩個都省略、只給 ridge、只給 lasso、lasso 為 None、ridge 為 NaN、ridge 為 0；每種都拒絕、狀態仍為 closed、`evaluate` 仍被拒、拒絕不消耗本次執行）；metric-only 測試加「兩個都沒提供」的評估拒絕；`test_fixture_run_scores_both_metric_only_stand_ins_once` |
| `tests/test_test_section.py` | fixture 的 `test` 現在含兩個 `metric_only`：斷言恰好 ridge 與 lasso、欄位只有指標；獨立重算只走 `ols_subset`；新增兩種竄改（少 lasso、兩個都移除）被拒 |
| `hw2.ipynb` | §5.3 改為「兩個 metric-only 模型（Ridge 與 Lasso）的 alpha 都已以 training CV 固定之後才能開啟（省略其中任何一個，或兩個都省略，守門都拒絕開啟）」與「只評估授權清單中的 OLS 子集模型與這兩個 metric-only 模型（各一次）」；重新執行（2.8 s） |
| `results/model_data.json`、`assets/model_data.js` | notebook 重跑的結果：與 `c9b106c` 逐鍵比較，只有 `meta.timing_s` 四個值與 `meta.generated_at` 不同；仍沒有 `test`，`test_inputs` 0 列 |

- **閉合條件的對應與證據**：

| R2 條件 | 證據 |
| --- | --- |
| (a) Ridge 或 Lasso 任一個 alpha 未固定（含兩個都沒傳與只傳一個）就拒絕開啟 | `hw2/testgate.py` `open()`；`test_gate_refuses_to_open_unless_both_metric_only_alphas_are_fixed`（6 個參數化案例）全過 |
| (b) `evaluate` 只在兩個 metric-only 模型都提供時執行 | 凍結集合恆為 {ridge, lasso}＋既有等式檢查；`test_metric_only_models_go_through_the_same_gate_once` 斷言只給 ridge、兩個都不給時都拒絕 |
| (c) pytest 以 fixture 驗證兩種省略都被拒絕 | 同 (a)；fixture 為 `tests/test_testgate.py::small_run`（synthetic） |
| (d) notebook §5.3 與程式一致 | §5.3 文字見上；cell 輸出：正式資料 `open refused: the official test gate stays closed …`（旗標先擋）、`load_test_rows refused` |
| (e) 沒有回歸 | 見下方回歸證據 |

- **回歸證據**（修正後的工作樹＝`77b79f4`）：
  - `.venv/Scripts/python -m pytest -q -rs -p no:cacheprovider` → **183 passed, 1 skipped**（skip 仍是學號設定未提供）；修正前 174 passed（新增 9 項）。
  - `node --test tests/js/core.test.js` → 7 pass、0 fail、2 skip（fixture 項目）；pytest 內以 fixture 執行同一檔（`test_node_core.py`）→ 9／9、0 skip（含兩個 `metric_only` 項目被略過的 fixture）。
  - `python -m hw2.offline_scan` → `scanned 6 files: PASS (0 findings)`。
  - `testgate.OFFICIAL_TEST_GATE_ENABLED` 仍為 False；追蹤的 `model_data` 區段＝{baselines, inputs, meta, preprocess, test_inputs, winners}，沒有 `test`，`test_inputs.written` false、0 列；本次修正沒有載入任何正式 test 列（守門測試的正式資料部分只斷言拒絕）。
  - fixture dashboard（`python -m hw2.fixture`，n_test 4,291，test 鍵含 ridge／lasso stand-in）以 `file://` 在 headless Chrome 155 於 1440／375 px 載入：沒有例外、沒有 console error、Test 區塊顯示「All-in baseline · k = 18」、沒有水平溢出（`page_check.js`，scratchpad）。Dashboard 不顯示 metric_only（依 BR-01 第 4 點，比較表屬 #63）。
  - **F-1 回歸 mutants**（scratchpad `mutants_f1.py`，單元複本，完整 suite）：恢復原本「只檢查有傳入的 alpha」→ DETECTED（3 failed）；只不要求 lasso → DETECTED（1 failed）；契約接受 metric_only 子集 → DETECTED（2 failed）。
  - `tests/test_repo_hygiene.py`（commit 後）：15 passed、1 skipped。新增內容沒有 7 位以上數字串；「學號」沒有出現；實際學號比對仍 NOT VERIFIED（S-1）。
- **時間**：2026-10-18 18:25 至 18:45 +0800。
- **Remaining**：R2（Orchestrator 派工）。#63 開啟正式守門時須提供真正的 Ridge／Lasso 模型與 training CV 選出的 alpha，守門會要求兩者都在；F-4 仍屬 #63。
