# Audit record — Issue #61，cycle 1，R1

| 欄位 | 內容 |
| --- | --- |
| Work Contract | GitHub issue #61「HW2 T2 All-in baseline 端到端：fit、PI、test 守門、dashboard 垂直切片」（OPEN；含 TR-01 修訂後的 AC、「Test 時序」「Test 資料隔離」共同條款、DA TK-3 與 I-3 兩條 AC）；Parent Spec `home_work_02/doc/spec/SPEC.md` rev 5（#59）；DA derivation `doc/governance/decisions/derivation-SPEC.md` §3 B-3、B-4、B-8、B-10，§9.1、§9.3、§9.4 I-3、§9.5 TK-3、§9.6 TR-01，§11 G-3；高風險 `decisions/decision-20261018-high-risk-categories.md`（票標示 H-2、H-3；A-1～A-3，A-4 適用全部票，A-7、A-8）與 `decisions/decision-20261018-issue60-a4-student-id.md`（S-1～S-6；§2.2 H-2 標示規則）；Outcome Contract `doc/governance/outcome-contract.md`（Brief @ `dff7c55c`＋CC-1、AD-1～AD-3）；Implementation 授權：`doc/governance/run/run-20261018-hw2-formal.md` §1 designation 第 2 點 |
| 受審 subject | branch `home_work_02-regrill`，implementation commit `c9b106cbc0a8e19bc42d5d6fd4b20d0150e1a8f1`（parent／BASE `bbf0ed5`）；審查範圍 `bbf0ed5..c9b106c`（30 個檔案，全部在 `home_work_02/` 內，沒有 `doc/requirement/` 路徑）。審查時 HEAD＝`5edd092`；其後的 `ed4d32a`、`5edd092` 只改 `doc/governance/**`（record-only path，Bindings §7），已以 `git diff --stat c9b106c..HEAD` 核對（只有 worklog 與 run record 兩檔） |
| Audit 種類 | **R1**（full independent audit of accepted work scope），**cycle 1**。**本 record 不是 Spec Integration Audit**（本 Spec 有多張票，不適用單 Ticket fast path；run record §4） |
| 角色 | `primary_reviewer`（definition `gov-primary-reviewer`；Bindings §3.1 R-PR mapping `claude-opus-5-5`／`xhigh`） |
| Assurance (a)：context independence（治理 §2.3；Bindings §3.7） | (1) **Independent context**：Orchestrator 以 Agent tool 派 `gov-primary-reviewer`（非 fork），從空白 context 開始；派工內容是路徑與識別（Ticket、Spec、derivation、DA 紀錄、OC、Brief、CONTEXT、worklog、#60 R1 record、branch／SHA）。派工訊息中「後續 commit 只動 `doc/governance/**`」與 worklog、run record 的敘述，都只當作待驗證主張，並已自行核對。(2) **Verifiable binding**：見 (b) 欄。(3) **Autonomous access**：自行讀取 `gh issue view 61`、Spec、derivation、DA 紀錄、OC、Brief、git 歷史與 diff、全部實作、notebook 與測試；自行執行測試、在 `git archive` 複本上重跑 notebook、不 import `hw2` 的獨立重算、mutation probes、守門與契約的探測、以 CDP 驅動的 `file://` 瀏覽器檢查（第 1 節）。(4) **Self-written record**：本檔由 Reviewer 以自己的 Write 工具寫入。 |
| Assurance (b)：model diversity（Bindings §5） | **Executor**：agentId `af27ea1586955f943`，`agentType` `gov-executor`，觀測 `('claude-opus-5-5', 'high')` 234 則、單一元素（Reviewer 以 Bindings §3.6 的同一邏輯自行掃描 session `4bbff425-7ff9-4cdc-b64c-cc68e824e1b1` 的 subagent transcript；與 run record §10 一致）。**本 review**：agentId `a68ac8fd770753723`，`agentType` `gov-primary-reviewer`，撰寫本 record 前觀測 `('claude-opus-5-5', 'xhigh')` 162 則、單一元素；全程核對由派工者依 Bindings §3.6 在採用本 record 前執行。**無 model diversity**（兩者同為 `claude-opus-5-5`）。Bindings §5 不宣告 diversity 關係，不記 `diversity_lost`（A-8）。 |
| 日期 | 2026-10-18 |

## 1. 審查方法與環境

Reviewer 的腳本與產物都在 session scratchpad 的 `r1-61-reviewer/`（不在 repo）。工作樹沒有被修改：審查前後 `git status --short home_work_02` 都是空的。

- **Subject 識別**：`git show --stat c9b106c` 30 個檔案、全部在 `home_work_02/`；`git diff --stat c9b106c..HEAD` 只有 `doc/governance/run/run-20261018-hw2-formal.md` 與 `doc/governance/worklog/issue-61.md`；工作樹的實作路徑與 `c9b106c` 相同。
- **工作樹 pytest**（單元 `.venv`，Python 3.11.2，Node v24.19.0）：`python -m pytest -q -rs -p no:cacheprovider` → **174 passed, 1 skipped**（skip：`tests/test_repo_hygiene.py:71`，`packaging.json not provided yet`）。`node --test tests/js/core.test.js`（無 fixture）→ 7 pass、2 skip（fixture 項目）。
- **Notebook 重跑**：`git archive c9b106c home_work_02` 匯出到 scratchpad，刪除 `results/model_data.json`、`assets/model_data.js`、`results/split/`，以單元 `.venv` 執行 `python -m hw2.run_notebook` → `executed hw2.ipynb in 3.4 s`。重新產生的 `model_data.json` 與 commit 中的版本逐鍵比較，只有 `meta.generated_at` 與 `meta.timing_s` 的四個時間不同；`.json` 與 `.js` 物件相同；`split_assignment.csv` 與 commit 的 blob 逐位元組相同。複本上 `pytest --ignore=tests/test_repo_hygiene.py` → 159 passed。
- **#60 區段沒有回歸**：`bbf0ed5` 與 `c9b106c` 的追蹤 `model_data` 中，`preprocess`、`inputs`、`test_inputs` 完全相同，`meta`（扣除時間與 `sections_written`）完全相同。所以 `sale_days` 與 zipcode one-hot 的向量化沒有改變任何已匯出的值。
- **Reviewer 的獨立重算：正式 All-in（只用 training 列）**。腳本不 import `hw2`。它從只含識別的 `split_assignment.csv` 取得 test 列位置，並以 `pd.read_csv(skiprows=…)` 在解析時跳過那些列，所以沒有讀到任何 test 列的特徵或 `price`。我自己寫 encoding（基準日 2014-01-01、整修旗標與有效年份、依訓練列排序的 zipcode one-hot、drop 第一類）與 OLS：
  - encoded column 名稱與順序和 `fit.coef_names` 相同；n_train 17,290、欄數 88、rank 88、df_resid 17,202；zipcode 基準 `98001`，類別清單相同。
  - 係數與 `lstsq`（欄位等化設計）的最大相對差 6.6e-10；(XᵀX)⁻¹ 最大差／最大值 1.1e-7；s² 0.033503（相對差 4e-15）；log R² 0.87908；Adjusted R² 0.87846，以 1−(1−R²)(n−1)/(n−rank) 計算（相對差 6e-16）；t(0.975, 17202) 1.9601019（完全相同）。
  - 5 個 fold 都只以該 fold 的訓練列 fit 類別與 OLS，在驗證列以 USD 計分：各折 MAE／MSE／RMSE／R² 與 `cv.folds` 的相對差 ≤ 3.2e-7；每折都是 88 欄、rank 88、未見 zipcode 0 筆；平均（RMSE 158,154、MAE 75,658、R² 0.8010）與 ddof=1 標準差（35,930、1,070、0.0862）相符。
  - 以 `inputs` 中位數（zipcode 取眾數）預測：US$503,564，PI US$351,404–US$721,610，與 dashboard 顯示及 worklog V-10 相同。
- **Reviewer 的獨立重算：synthetic fixture**。以 subject 自己的 `hw2.fixture` 程式路徑產生三組 fixture：fxA（1,500 棟＋40 筆重複，seed 20261018，n_test 310）、fxB（2,500＋120，seed 777，n_test 531）、fxU（把 7 筆 test 列的 zipcode 改成 training 沒有的類別）。獨立腳本不 import `hw2`，從 synthetic CSV **重新擬合**每個授權模型（不使用匯出的 `fit`），再對 test 列計算點預測、PI、covered 與各項指標：
  - `test_inputs` 的每一列與 CSV 在該位置的值相同（0 筆不符）；房屋數與重複交易數正確（300／10、500／31）。
  - 全部 5 個 `ols_subset` 模型 × 全部 test 列：predicted／lower／upper 的最大絕對差 ≤ 2.3e-7 USD（容差 1e-6）；`covered` 逐筆相同；n_covered、coverage、mean_width、MAE、RMSE、R²、二項近似半寬都相符。
  - fxU：有 zipcode 的模型 `n_unseen_zipcode`＝7（我自己的計數也是 7）；`lasso_path_k02` 沒有 zipcode 群組，計數 0；預測以基準類別計算，與重算相符。
  - Node：`HW2_FIXTURE_MODEL_DATA=<fxA|fxB|fxU> node --test tests/js/core.test.js` → 三組都是 9 pass、0 fail、0 skip。
- **守門探測**（只用 synthetic 資料；「正式資料」的行為是在探測程序內把 `data.EXPECTED_SHA256` 指向 fixture 檔來模擬，沒有開啟真實 CSV）：
  - P1 `open(winners, {})` → ALLOWED；`evaluate(ols)` → ALLOWED，對 5 個 OLS 模型評分；之後 Ridge／Lasso 在同一次執行中無法再評估。
  - P2 `open(winners, {"ridge": 1.0})` → ALLOWED；`evaluate` → ALLOWED，評分 OLS＋ridge，lasso 的 alpha 從未固定。
  - P3 同一份 fixture 資料上的第二個 `TestGate` → 可以再評估一次（只發生在非正式資料）。
  - P4 模擬正式資料且旗標為 True：第一次評估 ALLOWED，同一 process 的第二個 gate → `already loaded`。
  - P5 模擬正式資料且旗標為 False：`open` 與 `load_test_rows` 都拒絕。
  - P6 `complete` 但授權清單只有 `allin` 的 winners → 守門接受（它信任傳入的 winners）。
- **契約探測**（對 fxA `model_data` 的竄改副本執行 `contract.validate_model_data`）：C1 把一個有效的非 winner（`forward_sfs_k01`）加入授權清單並放入 `test` → ACCEPTED；C2 從授權清單與 `test` 移除方法 winner `rfe_k03` → ACCEPTED；C3 只有 `ridge` 沒有 `lasso` 的 `metric_only` → ACCEPTED；C4 `test.allin.model_key` 與它的鍵不符 → ACCEPTED。
- **其他探測**：(i) `evaluate_candidate(..., fold_groups=[…]*3)`，資料有 5 個 fold → `valid`，`cv.n_folds`＝3，`validate_entry` 接受（F-2）。(ii) 一個 `canonical_rank_deficient` 的非 winner 與有效候選並存時，winners、守門評估與匯出驗證都照常完成，invalid 項目沒有 `fit`（Spec Testing (2)）。
- **Mutation probes**（16 個，各自在 scratchpad 的複本上，以完整 suite 執行，只記錄通過或失敗）：Python PI 去掉 leverage、開區間 coverage、Adjusted R² 分母錯一、fold fit 看到全部 training 列（洩漏）、守門允許第二次評估、守門忽略不完整的 winners、JS PI 去掉 leverage、JS 未整修的有效年份錯誤、寫入端在守門關閉時接受 test、契約不檢查 ols 鍵＝授權清單、停用秩檢查、方法 winner 平手改取大 k、評估之外可以載入 test 列、USD R² 以 0 為中心、t 改成 z 1.96、JS Test 區塊改顯示整體 winner。**16／16 都被偵測**（rc=1，各有 FAILED 項目）。
- **Dashboard（`file://`，CDP）**：headless Chrome 155，`--host-resolver-rules="MAP * ~NOTFOUND"`，scratchpad 內的全新 profile，視窗 1440×1000。
  - **正式頁面**（`git archive` 複本）：沒有例外或 console error；只請求 6 個本機檔。另有一個 `data:image/svg+xml`，解碼後是 Chrome 自己的日期選擇器圖示（`fill="WindowText"`），單元檔案中沒有這個字串。KPI 四卡都標「訓練 CV（USD）」（US$158,154／US$75,658／2.605×10^10／0.8010）；fit 卡標「全訓練集擬合，R²／Adjusted R² 為 log 尺度」，數值與獨立重算相同；k 顯示「k = 18（固定）」；預測器有 18 個原始值輸入，結果 US$503,564（US$351,404–US$721,610）；Test 區塊顯示「Test 評估尚未執行」，內容區隱藏；沒有水平溢出。以 `?zipcode=99999&sqft_living=20000` 開啟時，出現兩個警告（超出 training 範圍 290–13540 仍計算；「此 zipcode 不在模型的訓練類別中，已以基準類別計算（輸入值：99999）」）。
  - **Fixture 頁面**（`python -m hw2.fixture`，n_test 4,291）：頂端顯示 fixture 警告；初始狀態為 All-in，Test 區塊標「Test 評估（USD）」與「All-in baseline · k = 18」，Test KPI 等於 `test.allin`。點選 Forward SFS 後顯示它的 winner（k = 3）且沒有提示；再點非 winner k = 1 後，KPI 與預測器換成 k = 1 的 `cv`／`fit`（只剩 1 個輸入 `sqft_living`），Test 區塊維持「Forward SFS · k = 3」，並顯示「目前選取的 Forward SFS · k = 1 不是該方法的 CV winner。Test 區塊展示的是該方法的 CV winner …切換選取不會產生新的 Test 評估。」。`window.HW2_PERF.firstDraw`＝166.8 ms（自 navigation start），`nPoints` 4,291＝n_test；方法與 k 切換的互動被記錄（6.2 ms、0.5 ms）；在 canvas 上派送的 wheel 事件被記為 `wheel-zoom`（1.3 ms，`visibility` visible）；pointermove 的 tooltip 顯示列、房屋、預測、實際、95% PI 與是否落入。CDP 原生的 `Input.dispatchMouseEvent` 滾輪在這個 headless 設定下沒有送達頁面，所以改以 DOM 事件派送；這裡只驗證量測與互動接線，不是 OV-6 的正式量測。
- **靜態檢查**：在複本上 `python -m hw2.offline_scan` → `scanned 6 files: PASS (0 findings)`；`app.js`、`hw2core.js`、`style.css`、`index.html` 沒有 `http(s)://` 資源；`index.html` 唯一新增的外部引用是本機 `assets/hw2core.js`；兩個 commit 的 notebook 六章標題與順序完全相同。
- **Reviewer 自身的 test 隔離**：我沒有讀取或推導任何正式 test 列的特徵或 `price`。完整 CSV 只由 subject 自己的程式解析（結構檢查與分割，#60 AC-4 允許）。

## 2. Acceptance criteria 逐條判定

| AC（#61） | 判定 | 證據 |
| --- | --- | --- |
| AC-1 Spec rev 5「指標與推論」（含秩不足三類）、「預測區間」、`model_data` 的 `baselines.allin`／`winners`／`test[ols_subset]` 結構 | **PASS**（F-2、F-3 為 non-blocking） | `hw2/ols.py`：欄位等化後以 pivoted QR 判定 rank，秩不足時拋 `RankDeficientError`、不刪欄；df＝n−rank；Adjusted R² 用實際 rank；t(0.975, df)；PI 依 Spec 公式計算後 exp 回 USD。`hw2/metrics.py`：USD 指標、閉區間 coverage、二項近似附獨立假設說明。`hw2/models.py`：三類語義——fold 缺類別時不建欄並計數（`n_valid_unseen_zipcode`）；fold 秩不足→`fold_rank_deficient`；canonical 秩不足→`canonical_rank_deficient`、沒有 `fit`；All-in 秩不足、某方法沒有有效候選、整體 winner 無法決定→`ExperimentFailure` 列出 invalid。`tests/test_models.py` 各有案例。結構：`baselines.allin`（`cv` USD＋`fit` log）、`winners`、`test` 的 `ols_subset` 欄位齊全（`contract.OLS_TEST_KEYS`）。獨立重算見第 1 節 |
| AC-2 守門（G-3）：只在 alpha 與 winner 全部固定、本次執行尚無評估時可呼叫；第二次報錯；同樣適用於 metric_only；pytest 以 fixture 驗證 | **FAIL → F-1（blocking）** | Winner 完整性、同一 gate 的第二次呼叫、在評估之外載入、凍結授權集合、metric_only 走同一個守門且只評估一次、正式旗標都成立（`tests/test_testgate.py`；P4、P5；M5、M6、M13 被偵測）。**alpha 部分不成立**：只要沒有傳入 Ridge 或 Lasso 的 alpha，守門照樣開啟並評估（P1、P2） |
| AC-3 獨立重算（SR-02）：pytest 以 numpy 重算全部列、1e-6、不呼叫匯出的預測函式；Node 從原始值經 dashboard 自己的前處理重算 | **PASS** | `tests/test_test_section.py:84-112` 只從 `test_inputs`＋`preprocess`＋`fit` 重建設計列（`contract.model_entries` 只用來查表）；`tests/js/core.test.js:122-142` 走 `Core.predict`。Reviewer 從 synthetic CSV 重新擬合的獨立重算 ≤ 2.3e-7 USD；Node 三組 fixture 9／9；M1、M7、M8 被偵測 |
| AC-4 Dashboard：BR-01 分層與標示；預測器只對 OLS、原始值輸入、警告（SR-07）；Q43 圖 | **PASS** | 第 1 節 CDP 檢查：KPI 來自 `cv` 並標「訓練 CV（USD）」，預測器來自 `fit`，Test 區塊只讀 `test` 並標「Test 評估（USD）」與模型名稱；非 winner 時有提示；`canPredict` 排除 `metric_only` 與 invalid；下拉只列 fit 類別並標示基準類別；網址帶入未見 zipcode 時出現 Spec 指定的警告；canvas 逐筆繪製全部 4,291 列（log10、y=x、逐筆 PI 線段、依 covered 以顏色與形狀區分、滾輪／拖曳／按鈕／鍵盤縮放、游標讀取）。`app.js:339-344` 只從 `test_inputs` 讀識別與實際價格（繪圖用）；`Core.predict` 唯一的呼叫點使用使用者輸入（`test_dashboard_static.py:106-116`；B-3） |
| AC-5 OV-6 量測方式內建（SR-09 (a)(b)(f)(g)）；≥ 4,000 筆 synthetic fixture 量測並記錄 | **PASS**（只驗證方法；正式 gate 在 #67） | `window.HW2_PERF.firstDraw`（自 `performance.timeOrigin`）、`interactions[]`（事件 `timeStamp` → 重繪結束，另有 `handler_ms`、`visibility`）、`#scatter-perf`；繪圖迴圈涵蓋全部點（`app.js:498-510`）。Reviewer 在 4,291 列上重現 firstDraw 166.8 ms 與互動紀錄；worklog V-11 記錄 Chrome／Edge 量測值與環境 |
| AC-6 PI 陳述：notebook 寫明假設與「不宣稱保證 95%」；二項近似、不陳述方向（SR-12） | **PASS** | Notebook §5.2（cell 27）：公式、條件中位數、三項假設、選擇後推論與誤設、「不宣稱保證 95% 的經驗涵蓋率」、偏離時分析不判失敗、二項近似與獨立假設、「不陳述偏差的方向或幅度」、列出房屋數與重複交易數；dashboard 有相同說明（`index.html:193-194`）。報告版依 I-3 由 #65 負責 |
| AC-7 正式 test 列沒有被載入；守門保持關閉；fixture 是 synthetic；追蹤的 `model_data` 沒有 `test` 與 `test_inputs` 列；同一條程式路徑 | **PASS** | `OFFICIAL_TEST_GATE_ENABLED = False`（`testgate.py:31`）；`load_test_rows` 只在 open 狀態的 `evaluate` 內可用（`testgate.py:106-131`）；`data.read_csv` 已改為私有（`test_no_public_function_returns_the_parsed_file`）。`hw2/fixture.py` 只用 rng 產生資料，輸出受 `_outside_unit` 限制。追蹤的 `model_data`：區段＝{meta, preprocess, inputs, test_inputs, baselines, winners}，`test_inputs.written` false、0 列，`baselines` 沒有 test 欄位（Reviewer 自行核對）。notebook 與 fixture 走同一組函式（`load_and_split` → `fit_allin`／`evaluate_candidate` → `determine_winners` → `TestGate` → `build_model_data` → `write_model_data`） |
| AC-8（DA TK-3）notebook Evaluation 寫明 exp(ŷ_log) 估計條件中位數、不是條件平均 | **PASS** | Notebook cell 27「**條件中位數**……**不是條件平均**」；`test_notebook_structure.py:68-73` |
| AC-9（DA I-3）陳述先落在 notebook | **PASS** | 同上；CV winner 樂觀偏誤的陳述在 cell 25 |
| What to build：端到端鏈、匯出、dashboard 垂直切片；本票不執行正式 Test 評估 | **PASS**，但 F-1 適用 | 第 1 節 |

## 3. 高風險類別核對（A-1）

| 類別 | 核對內容 | 結果 |
| --- | --- | --- |
| **H-3**（票已標示） | A-2：Reviewer 自己執行全部 pytest（含分組隔離 `test_split.py`、fit 只用訓練列、M4 洩漏 mutant 被偵測）、Node test，以及兩種獨立重算（正式 All-in 從 training 列；fixture 從 synthetic CSV 重新擬合）。選擇邊界測試屬 #62（本票沒有選擇方法）。README 沒有引用匯出的數字；worklog 的數字（RMSE 158,154 ± 35,930 等）與匯出及 Reviewer 的重算相同。A-3：追蹤的 `model_data` 中 `baselines` 沒有 test 欄位，也沒有 `methods`；fixture 的 `test` 鍵集合等於授權清單（`test_test_section.py:73-81`；Reviewer 的 fxA／fxB）；dashboard UI 不以 `test_inputs` 評估任何模型（第 2 節 AC-4）。TR-01：守門關閉、正式 test 列未載入（AC-7）。G-3：見 F-1。另見 F-2（fold 子集長度）、F-3（授權清單完整性）、F-4（正式資料的守門加固） | AC 層級除 G-3（F-1）外 PASS |
| **H-2**（票已標示） | 依 `decision-20261018-issue60-a4-student-id.md` §2.2 的清單：notebook 六章的名稱與順序未改（`bbf0ed5` 與 `c9b106c` 相同）；`offline_scan` PASS，唯一新增的引用是本機 `assets/hw2core.js`；`file://` 在所有主機名稱都無法解析時正常載入，只請求本機檔；`home_work_02/index.html` 路徑不變；預測圖（Q43）的必要元素如 AC-4；README 的重跑步驟（`node --test`、`python -m hw2.fixture`）Reviewer 實際執行過；zh-TW 標示與 `lang="zh-Hant-TW"` | PASS |
| **H-1**（A-4，適用全部票） | `git ls-tree -r c9b106c -- home_work_02` 唯一的 PDF 是老師文件 SRC-3；沒有 `.zip`、`.env`、`kaggle.json`，也沒有 `.local/`、`acceptor_materials/`、`dist/` 下的檔案；範圍內新增的行沒有 `KAGGLE_KEY`／`api key`／`secret`／`password`／`token`。**學號**：`.local/packaging.json` 不存在，A-4 的實際值比對無法執行。依 S-1 記為 **NOT VERIFIED**，不是 PASS。S-1 替代證據（Reviewer 以腳本取得；所有數字在輸出前都先遮罩，沒有印出任何疑似值），範圍 `bbf0ed5..HEAD`（3 個 commit、21,983 行新增）：7 位以上的數字串都已歸類——15,735 個是含小數點或指數的資料值（`model_data` 的浮點數）、3 個是 hex hash、10 個是 YYYYMMDD 日期（紀錄檔名中的日期與 fixture seed），另外 2 個是一日的毫秒數常數（`hw2core.js` 的 `DAY_MS` 與 worklog 對它的說明）；「學號」出現在 5 行新增內容中，全部是 run record 與 worklog 的敘述用詞，實作 commit 中沒有出現；3 個 commit message 中只有 1 個 8 位數字串，是日期形態。S-4 尚未觸發（學號設定不存在） | 憑證與材料 PASS；學號 NOT VERIFIED（S-1） |
| H-4 | 未觸及：沒有報告或 acceptor 材料。Wireframe 的 mock 沒有被使用（`hw2core.js`、`app.js` 沒有引用 `design/`）；fixture 數值只出現在單元以外，頁面會顯示 fixture 警告（DA §9.3 條件 4） | 不適用 |

## 4. #60 R1 follow-up（owner＝#61）

- **#60 F-1**（守門測試以追蹤的正式路徑為目標）：**已處理**。`tests/test_contract_fixture.py` 的 `stand_in_official` 以 monkeypatch 把 `export.OFFICIAL_PATHS` 指向暫存檔，teardown 時核對追蹤的兩個 `model_data` 檔 sha256 沒有改變。測試中沒有其他呼叫以預設的正式路徑寫入；notebook 是唯一的正式寫入點。
- **#60 F-3**（`hw2.data.read_csv` 是公開、沒有守門的全資料讀取）：**已處理**。改為私有 `_read_csv`；新增只回傳結構事實的 `structural_facts`；test 列唯一的讀取路徑是 `TestGate.load_test_rows`。`test_no_public_function_returns_the_parsed_file` 斷言這一點。

## 5. Findings

### F-1 — G-3 守門沒有要求 CC-1 的 metric-only alpha 全部固定

- **Severity**：Medium。**Blocking**：**是**。觸及 H-3，所以 A-7 適用：若要 defer，必須有 DA 確認。
- **證據**：
  - `hw2/testgate.py:93-99`：`open()` 只檢查**有傳入**的 alpha（只允許 ridge／lasso，值必須有限且大於 0），沒有要求 `set(alphas) == {"ridge", "lasso"}`。
  - `evaluate()`（`testgate.py:151-153`）要求 metric-only 模型集合等於**凍結的** alpha 集合，所以集合是空的或只有其中一個時也會通過。
  - 探測結果：P1 `open(winners, {})` ALLOWED → 評估 5 個 OLS 模型 → 同一次執行中再也無法評估 Ridge／Lasso；P2 `open(winners, {"ridge": 1.0})` ALLOWED → 評估 OLS 與 ridge，lasso 的 alpha 從未固定。
  - `hw2/fixture.py:132`（`gate.open(winners, alphas or {})`）與 `tests/test_testgate.py:85`、`:97`、`:102`、`:117`、`:132`、`:169` 都以 `{}` 開啟守門並評估。現行測試只驗證「傳入的 alpha 未固定」（`:75`，`{"ridge": None}`），沒有驗證「省略 alpha」會被拒絕。
  - 交付物的陳述與程式不符：notebook §5.3（`hw2.ipynb:1740`）寫「守門只有在 `winners` 完整……且全部 metric-only 模型（Ridge、Lasso）的 alpha 都已以 training CV 固定之後才能開啟」；commit message「opens only with complete winners and fixed metric-only alphas」；worklog §3.3 也這樣寫。
  - 另外，`contract.validate_test` 接受只有 `ridge` 沒有 `lasso` 的 `metric_only`（C3，`contract.py:311`）。
- **契約條款**：#61 AC-2「test 評估函式只在 alpha 與 winner **全部**固定……時可呼叫；……守門同樣適用於日後的 `metric_only` 模型」；derivation §11 G-3「pytest 驗證 test 評估在 alpha 與 winner 固定之後才發生」；§9.3 條件 1「每次完整執行仍然只評估一次，且只評估授權集合（**含 CC-1 的 metric_only**）」；CC-1 (3)(4)；H-3「用 test 選模」。
- **風險**：第一次開啟正式守門是不可逆的事件。依現在的程式，#63 只要在 Ridge／Lasso 的 alpha 固定之前呼叫 `open`，就能在本次執行中評估 OLS 的 test 結果，而守門與契約驗證都不會阻止。之後在另一次執行中選 alpha 時，test 結果已經被看過，違反 CC-1 (4) 與 G-3。這個守門正是為了在機械層面防止這件事。本票中正式守門是硬性關閉的，所以現在沒有實際暴露；因此判為 Medium 而不是 High。
- **R2 的 closure 條件**：
  - (a) 只要 Ridge 或 Lasso 任一個的 alpha 沒有固定——包含兩個都沒傳與只傳一個——守門就拒絕開啟；
  - (b) `evaluate` 只在兩個 metric-only 模型都提供時才執行（凍結集合完整後，現有的等式檢查就涵蓋這一點）；
  - (c) pytest 以 fixture 驗證兩種省略情況都會被拒絕；
  - (d) notebook §5.3 的文字與程式的實際行為一致；
  - (e) 沒有回歸：全部 pytest 與 Node 測試通過；正式守門仍然關閉；追蹤的 `model_data` 仍然沒有 `test`。

  Fixture 怎麼提供替身的 metric-only 模型屬於 HOW（例如沿用 `tests/test_testgate.py` 的 `StubMetricOnly` 模式），條件是輸出仍然只在單元以外並標示為 fixture。C3（契約要求兩個 metric_only 同時存在）可以在這次修正中一併處理，或交給 #63；它不是本 finding 的 closure 條件。
- **如果有爭議**：若 Executor 或 Orchestrator 認為 derivation §11「負責 test 評估的票要把 Ridge／Lasso 的一次性評估納入同一個守門條件」是把 alpha 完整性分配給 #63 而不是 #61，這是 blocking status 的爭議，而且涉及設計語義的分配，依治理 §4.3 先交 Design Authority。即使採這種讀法，notebook §5.3 與 commit 中的陳述仍然與程式不符，需要更正。

### F-2 — `evaluate_candidate` 會靜默截斷長度不符的 `fold_groups`；契約不核對 fold 數

- **Severity**：Medium。**Blocking**：否（latent：本票所有呼叫都使用預設的 `fold_groups=None`，追蹤的 All-in 有 5 個 fold，已核對）。
- **證據**：`hw2/models.py:188`：`for fold, groups in zip(fold_ids, fold_groups)`。探測：資料有 5 個 fold，傳入 3 個子集 → 得到 `status valid`、`cv.n_folds` 3。`contract.validate_entry` 只核對 `len(cv.folds) == cv.n_folds`（`contract.py:228-229`），所以 3 折的項目會被接受；`meta.cv.n_folds`（5）沒有被拿來比對。
- **契約條款**：Spec rev 5「分割與交叉驗證」（所有方法、所有 k 都用同一組 fold）；`model_data`「契約記錄各 fold 的子集與一致的 fold 數」；H-3（公平性、選擇完整性）。
- **Disposition**：Owner＝**#62**（第一個傳入 fold-internal 子集的票；Executor 與其 R1）。`evaluate_candidate` 應在 `len(fold_groups)` 不等於 fold 數時拒絕，契約應核對每個項目的 `cv.n_folds` 等於 `meta.cv.n_folds`。本票不需修改。

### F-3 — 契約不核對授權清單＝{All-in} ∪ 各方法 winner ∪ {整體 winner}；dashboard 在這種狀態下會顯示前一個模型的 Test 數字

- **Severity**：Low。**Blocking**：否。
- **證據**：`contract.validate_winners`（`contract.py:274-295`）只檢查授權清單含 `allin`、沒有重複、沒有 metric-only、每個鍵都是有效項目、方法 winner 與它的項目一致、complete 時整體 winner 在清單中。它不檢查授權清單是否**等於**上述聯集。探測 C1（非 winner 被授權並評分）與 C2（方法 winner 不在授權清單與 `test` 中）都被接受；C4（`test.<key>.model_key` 與鍵不符）也被接受。在 C2 的狀態下，`app.js:368-372` 會在 `!tEntry` 時提前 return：Test 區塊的標題換成新模型，但 Test KPI、涵蓋統計與散佈圖仍然是前一個模型的數字。實際的匯出路徑由 `determine_winners` 產生授權清單，而且有測試（`test_models.py:166-172`），所以目前不會發生。
- **契約條款**：Spec「特徵選擇與模型」中授權集合的定義與契約不變量；Brief §10「Test 暴露檢查」；BR-01 UI 驗收（來源標示不得混淆）。
- **Disposition**：Owner＝**#62**（winners 在這張票變為完整；方法與 k 的 dashboard 也屬它）。建議在 `validate_winners` 加上聯集相等與 `model_key` 一致的檢查，並讓 `renderTest` 在 `!tEntry` 時清空或隱藏 Test 內容。#63 的 R1 在第一次寫出正式 `test` 時再核對。本票不需修改。

### F-4 — 正式資料「每個 process 只載入一次」的守門沒有測試；正式資料只以 sha256 識別

- **Severity**：Low。**Blocking**：否。
- **證據**：`testgate.py:35`、`:111-120` 的 `_official_test_rows_loaded` 沒有任何測試引用（`grep` 只在 `hw2/testgate.py` 命中）。Reviewer 的 P4 以模擬的正式資料確認它可以運作。P3：非正式資料上同一份 `PreparedData` 的第二個 `TestGate` 可以再評估一次——對 synthetic 資料可以接受。`is_official` 只比對 sha256（`testgate.py:46-47`），所以位元組被改動過的正式資料複本會被視為非正式。目前的緩解：唯一的非正式流程 `hw2.fixture` 只產生 synthetic 資料，不接受外部 CSV。
- **契約條款**：#61 AC-2「本次執行尚無 test 評估時可呼叫」；derivation §9.3 條件 1；TR-01。
- **Disposition**：Owner＝**#63**（開啟正式守門的票）。開啟旗標時，以 synthetic 資料加上 monkeypatch 的 `EXPECTED_SHA256` 為這個守門加測試（Reviewer 的 P4 做法），並判斷正式資料的識別是否需要 sha256 以外的依據。本票不需修改。

## 6. Routing（需要其他 authority）

- 目前沒有。F-1 是 implementation 層級的 blocking finding，以 Executor 的 targeted correction 處理，再進 R2。若 F-1 的 blocking status 或它在 #61／#63 之間的分配有爭議，依治理 §4.3 先交 **Design Authority**（見 F-1「如果有爭議」）。
- 學號（A-4）：依 S-1 記 NOT VERIFIED，不是本票結案的條件。S-2～S-5 仍是 run record §8 的 open 項目。

## 7. 其他核對與備註（不是 finding）

- **Run record §10 的 Orchestrator concerns**：
  - (1) A-4 學號：見第 3 節 H-1。
  - (2) dashboard 的方法選單與 k 按鈕先於 #62 建置：這些是依 `model_data` 實際存在的方法產生的通用元件。#61 AC-5 要求以 SR-09 (b) 量測「方法／k 切換」，所以本票需要它們；它們沒有超出 Spec 或 Outcome Contract。完整的 k = 1…18 格子、「比較全部」、指標 vs k 圖與 invalid 標示仍由 #62 及其 R1 核對。
  - (3) OV-6 只在 headless 量測：#61 AC-5 只要求驗證量測方法；正式 gate 在 #67。
- **B-3 的字面**：derivation B-3 寫「test 區塊只讀 `test`」，但 Spec 的契約把實際價格與房屋數／重複交易數放在 `test_inputs`，而 Q43 圖需要實際價格作為 y 軸。`app.js` 只從 `test_inputs` 讀識別、實際價格與這兩個計數，沒有評估任何模型，符合 B-3 的目的（「不得用 `test_inputs` 評估任何模型」）。
- **Spec Testing (2)**：「其他有效候選的 CV 與 test 評估照常完成」沒有專門的 pytest，但 Reviewer 的探測（第 1 節 (ii)）確認整條流程可以完成。
- **Worklog 的主張**：V-1～V-11、V-13、V-14、時間量測與 binding 則數都已由 Reviewer 重現或核對。V-12（內建瀏覽器）沒有重做，已由 CDP 檢查取代。
- **範圍與 git**：沒有單元目錄以外的變更，沒有修改 `doc/requirement/`（RB-5）。Commit message 符合 git 規則，沒有 Claude 標記。沒有 push（designation 第 3 點；run record §1 push 選項 (a)）。

## 8. 結論

- Blocking findings：**F-1**（Medium，H-3）。
- Non-blocking findings：F-2（Medium，owner #62）、F-3（Low，owner #62）、F-4（Low，owner #63）。
- Routing：無（F-1 若有爭議，交 Design Authority）。
- A-4 學號：NOT VERIFIED（S-1）。

VERDICT: BLOCKING (F-1)
