# Audit record — Issue #60，cycle 1，R1

| 欄位 | 內容 |
| --- | --- |
| Work Contract | GitHub issue #60「HW2 T1 資料基線、分組切分與 model_data 契約骨架」（OPEN；含 TR-01 修訂後的 AC 與「Test 資料隔離」共同條款）；Parent Spec `home_work_02/doc/spec/SPEC.md` rev 5（#59）；DA derivation `doc/governance/decisions/derivation-SPEC.md` §3 B-14／B-16、§4 T-義務、§9.1、§9.3、§9.4、§9.6（TR-01）；高風險 `doc/governance/decisions/decision-20261018-high-risk-categories.md`（票標示 H-1、H-3；A-1、A-2、A-4）；Outcome Contract `doc/governance/outcome-contract.md`（Brief @ `dff7c55c`＋CC-1、AD-1～AD-3）；Implementation 授權：`doc/governance/run/run-20261018-hw2-formal.md` §1 designation 第 2 點 |
| 受審 subject | branch `home_work_02-regrill`，implementation commit `f20d70ebdc76ba7e1fd244769fa141fa23bf0641`（parent／BASE `e2d3e0b`）；審查範圍 `e2d3e0b..f20d70e`（35 個檔案，全部在 `home_work_02/` 內，沒有 `doc/requirement/` 路徑）。審查時 HEAD＝`7fe5ac2`；其後的 `786d46b`、`7fe5ac2` 只改 `doc/governance/**`（record-only path，Bindings §7），已以 `git diff --name-only f20d70e 7fe5ac2` 核對 |
| Audit 種類 | **R1**（full independent audit of accepted work scope），**cycle 1**。**本 record 不是 Spec Integration Audit**（run record §4：本 Spec 有多張票，不適用單 Ticket fast path） |
| 角色 | `primary_reviewer`（definition `gov-primary-reviewer`；Bindings §3.1 R-PR mapping `claude-opus-5-5`／`xhigh`） |
| Assurance (a)：context independence（治理 §2.3；Bindings §3.7） | (1) **Independent context**：Orchestrator 以 Agent tool 派 `gov-primary-reviewer`（非 fork），從空白 context 開始；派工內容只有路徑與識別（Ticket、Spec、derivation、高風險紀錄、OC、Brief、CONTEXT、worklog、branch／SHA）。Worklog 與 run record 中 Executor 的敘述只當作待驗證主張。(2) **Verifiable binding**：見 (b) 欄；本 agent 的 `agentType` 為 `gov-primary-reviewer`。(3) **Autonomous access**：自行讀取 Ticket（`gh issue view 60`）、Spec、derivation、高風險紀錄、OC、Brief、CONTEXT、上位契約轉寫、git 歷史與 diff、全部實作與測試；自行執行測試、乾淨環境重跑、獨立重算、mutation probes、`file://` 瀏覽器載入與 Chart.js 來源比對（第 1 節）。(4) **Self-written record**：本檔由 Reviewer 以自己的 Write 工具寫入。 |
| Assurance (b)：model diversity（Bindings §5） | **Executor**：agentId `a447664b1c57e651b`，`agentType` `gov-executor`，觀測 `('claude-opus-5-5', 'high')` 167 則、單一元素（Reviewer 以 Bindings §3.6 的同一邏輯自行掃描 session `4bbff425-7ff9-4cdc-b64c-cc68e824e1b1` 的 subagent transcript；與 run record §7 一致）。**本 review**：agentId `aa7add40010df5f41`，`agentType` `gov-primary-reviewer`，撰寫本 record 前觀測 `('claude-opus-5-5', 'xhigh')` 119 則、單一元素；全程核對由派工者依 Bindings §3.6 在採用本 record 前執行。**無 model diversity**（兩者同為 `claude-opus-5-5`）。Bindings §5 不宣告 diversity 關係，不記 `diversity_lost`（A-8）。 |
| 日期 | 2026-10-18 |

## 1. 審查方法與環境

- **Subject 識別**：`git rev-parse HEAD`＝`7fe5ac28…`；`git diff --stat f20d70e -- home_work_02 ':(exclude)home_work_02/doc/governance'` 為空，`git diff HEAD` 為空，所以工作樹的實作路徑與 `f20d70e` 相同。`git show --stat f20d70e`：35 個檔案、全部在 `home_work_02/`。
- **工作樹 pytest**（單元 `.venv`，Python 3.11.2）：`python -m pytest -q -rs -p no:cacheprovider` → **115 passed, 1 skipped**；skip 是 `tests/test_repo_hygiene.py:71`（`packaging.json not provided yet`）。執行後 `git status` 不變。
- **乾淨環境重跑**（README 的重跑步驟）：`git archive f20d70e home_work_02` 匯出到 Reviewer scratchpad，刪除 `results/` 與 `assets/model_data.js`；`py -3.11 -m venv` 建立新環境，`pip install -r requirements.txt` rc 0（建立加安裝約 3 分 42 秒）；`python -m hw2.run_notebook` → `executed hw2.ipynb in 7.4 s`；`pytest -q --ignore=tests/test_repo_hygiene.py`（該檔需要 git 工作樹）→ **100 passed**；`python -m hw2.offline_scan` → `scanned 5 files: PASS (0 findings)`。新環境的 `pip freeze`（55 個套件）與單元 `.venv` 完全相同。重新產生的 `results/split/split_assignment.csv` sha256 `901a6127…a563d`，等於 commit 中的 blob（`git cat-file -p f20d70e:… | sha256sum`）；重新產生的 `results/model_data.json` 與 commit 版本逐鍵比較，只有 `meta.timing_s.data_load_validate`、`meta.timing_s.split_and_folds`、`meta.generated_at` 不同；重新產生的 `.js` 物件等於 `.json`。
- **Reviewer 的獨立重算**（scratchpad 腳本，不 import `hw2`；只讀 CSV 的 `id` 欄，以及依 assignment 檔挑出的 training 列）：
  - CSV sha256＝釘住值 `d0875baa…57b7e`；assignment 21,613 列，`row`＝0…21612，`id` 欄與 CSV 順序相同。
  - train 17,290／test 4,323（比例 0.20002）；沒有房屋同時在兩側；聯集為全部列；每棟 training 房屋只在一個 fold；fold 兩兩無共同 `id`、聯集等於 training 房屋；test 列沒有 fold。各 fold 列數 3,454／3,462／3,461／3,456／3,457，房屋數 3,430×4／3,429。
  - 依 `meta.split.method`、`meta.cv.method` 文字自行重寫演算法，重現的 test 集合與 fold 編號與 commit 完全相同；seed 43 得到不同的 test 集合。
  - `model_data.inputs`：每個數值 source feature 的 min／max／median 與我只用 training 列算的值相同（0 筆不符）；zipcode 類別（70 個）與眾數 98103、日期範圍 2014-05-02～2015-05-27 與中位數 2014-10-17、整修年範圍 1940–2015 都相同；`preprocess.training_fit` 的 zipcode 類別等於 training 類別，基準 `98001`，87 個 encoded columns；`inputs.n_rows`＝17,290。
  - 頂層區段＝{`meta`, `preprocess`, `inputs`, `test_inputs`}，沒有 `test`；`test_inputs`：`schema_version` 1、21 個 fields（`row`、`id`、`date`＋17 個建模 source features＋`actual_price`）、`written` false、`rows` 空、`n_rows` 0、`n_houses`／`n_repeat_sales` 為 null。
- **Mutation probes**（在 scratchpad 的複本上，用乾淨環境執行；只觀察通過與失敗的數目）：M1 分割改為逐列而非逐房屋 → 5 failed；M2 fold 改為逐列 → 5 failed；M3 training 含 test 列 → 9 failed、5 errors；M4 基準改為最後一個類別 → 3 failed；M5 移除 fixture 守門 → 6 failed（另見 F-1）；M6 未見 zipcode 不編為基準 → 1 failed。六個 mutant 都被偵測。
- **`file://` 載入**：對 `git archive` 的 subject 複本，以 headless Chrome（`--headless=new --host-resolver-rules="MAP * ~NOTFOUND" --dump-dom`，scratchpad 內的全新 profile，所有主機名稱都無法解析）開啟 `index.html`。DOM 顯示 21,613 筆、21,436 棟、177 筆重複交易、sha256、19／18、17,290／4,323、5 個 fold（3,454／3,462／3,461／3,456／3,457）、seed 42、套件版本、`Chart.js 4.4.1（本機打包）`；`#load-error` 為 hidden。Chrome net log 只有瀏覽器自身的服務請求（Google 帳號、更新、時間、gstatic），全部無法解析；沒有任何指向頁面所引用主機的請求。
- **Chart.js 來源**：在 scratchpad 以 `npm pack chart.js@4.4.1` 取得 tarball，`package/dist/chart.umd.js` 與 `assets/vendor/chart.umd.js` 逐位元組相同（`cmp`），sha256 `74401d73…fd8f3`；`package/LICENSE.md` 與 `assets/vendor/chart.js.LICENSE.md` 相同（MIT）；`npm view chart.js@4.4.1 dist.integrity`＝`sha512-C74QN1bx…534Dg==`，與 worklog 相符。Vendor 檔中的 URL 只出現在 `/*! … */` banner（chartjs.org、kurkle color readme），沒有 `fetch(`、`XMLHttpRequest` 等網路 API。
- **自行 grep 外部資源**：`index.html`、`assets/app.js`、`assets/style.css`、`assets/model_data.js` 中唯一的 `//host.tld` 是 `model_data.js` 的 `https://www.kaggle.com/datasets/harlfoxem/housesalesprediction`，由 `assets/app.js:24` 設為 `<a href>`；`style.css` 沒有 `url(`、`@import` 或 `@font-face`。
- **A-4 掃描**：見第 2 節 AC-8 與第 3 節 H-1。
- **Reviewer 自身的 test 隔離**：Reviewer 的腳本沒有讀取或推導任何 test 列的特徵或 `price`。完整檔案的解析只發生在 subject 自己的結構測試（AC-4 允許）與 mutation probes（只看通過與失敗的數目）。

## 2. Acceptance criteria 逐條判定

| AC（#60） | 判定 | 證據 |
| --- | --- | --- |
| AC-1 Spec rev 5「資料、計數與前處理」「分割與交叉驗證」條款；`meta` 含 sha256、seed、版本、n_train／n_test、fold 數 | **PASS** | `hw2/data.py:125-153`：`verify_sha256` 在 `read_csv` 之前，不符時訊息含預期值、實際值與 re-pin 提示（`test_data.py` 的 mismatch 與「先於解析」兩案例）；`validate_structure`（`data.py:71-100`）：21 欄與順序、21,613 列、21,436 個 `id`、`sqft` 恆等式（另含缺值檢查，見 AC-4）。`hw2/preprocess.py`：19 個 source features、18 個 feature groups（CSV 欄序，排除 `sqft_basement`）；`sale_days`（基準日 2014-01-01）、`is_renovated`／`yr_renovated_effective`（未整修為 `yr_built`，兩欄同屬 `yr_renovated` group）、`zipcode` nominal；需要 fit 的 one-hot（類別取自傳入的訓練列，排序第一類為基準不建欄，未見類別編為基準）與只供 Ridge／Lasso 的標準化。目標 ln(price) 與 exp 回轉寫在 `preprocess.target`；本票沒有模型，點預測由 #61 實作。極端值只以 training 列列出（notebook §2.3），不刪除。分割：以 `id` 分組、seed 42 的 80/20，三個不變量成立（第 1 節）；5 個分組 fold 只產生一次，逐列保存在 `results/split/split_assignment.csv` 與 `PreparedData.training["fold"]`。fold-internal selection、canonical subset 與選擇偏誤陳述依 DA §9.5 屬 #62。`meta`：`csv_sha256`、`seed` 42、`versions`、`split.n_train` 17,290／`split.n_test` 4,323、`cv.n_folds` 5 |
| AC-2 pytest 次 seam「分割」「前處理」 | **PASS**（測試強度見 F-2） | `tests/test_split.py`：無共同 `id`、聯集為全部列、同 seed 重現且換 seed 不同、約 80/20、fold 兩兩無共同 `id` 且聯集等於 training、synthetic 重複交易同側同 fold、fold 與列順序無關。`tests/test_preprocess.py`：fit 的類別與統計量只來自訓練列（`test_fit_uses_only_the_training_rows`、`test_categories_come_from_training_rows_only`、`test_standardization_statistics_are_training_statistics`、`test_input_ranges_come_from_training_rows_only`）；`sale_days` 0／1／285／365／511 與格式錯誤；整修三案例與負值。兩次執行都通過；Reviewer 的獨立重算與 M1、M2、M4、M6 偵測結果一致 |
| AC-3 `test_inputs` schema 以 synthetic fixture 通過 pytest；追蹤的正式 `model_data` 中 `test_inputs` 無列、無 `test`（TR-01） | **PASS** | `hw2/contract.py`：`TEST_INPUT_FIELDS`（21 個）、`empty_test_inputs`、`build_test_inputs`、`validate_test_inputs`（房屋數、`n_repeat_sales = n_rows − n_houses`、與 n_test 一致）。`tests/test_contract_fixture.py`（全部 synthetic）：fields 涵蓋識別、18 個 features 與 `actual_price`；fixture 列通過 schema；60 棟／8 筆重複交易的計數；10 種竄改被拒；n_test 不符被拒；未寫入卻有列被拒；`.json`／`.js` 往返相同；fixture 寫入正式路徑被拒。追蹤檔：Reviewer 自行核對沒有 `test`、`test_inputs.rows` 為空、`written` false（亦見 `test_model_data_official.py`） |
| AC-4 全資料層級只做結構驗證；分布與極端值只用 training 列（B-14）；分割只對外提供 test 列識別與 n_test | **PASS** | 讀到全部列的只有：sha256（位元組）、解析加 `validate_structure`、以 `id` 分割。`load_and_split`（`data.py:125-153`）只回傳 training 列、test 列的列序號與 `id`、n_test，並在函式內 `del full`；`test_load_and_split_returns_training_rows_and_test_identifiers_only`；M3 被偵測。Notebook 的分布、極端值、fold 統計都來自 `prepared.training`（cells 7–11、17）。`split_assignment.csv` 只有 `row`、`id`、`set`、`fold`。附註：結構檢查另含「無缺值」（`data.py:85-87`，列於 `meta.structural_checks`），不在 AC 括號所列五項之中；它是完整性檢查，不產生任何分布數值，本審查讀為「結構驗證」的一部分，不列 finding |
| AC-5 Notebook 六個 CRISP-DM 章節標題；前三章有內容 | **PASS** | `## 1. Business Understanding` 至 `## 6. Deployment` 依序出現；BU（目標、研究問題、成功標準、來源與授權、兩條老師原文與 14–20 交集、19／18）、DU（結構驗證、training 分布、極端值）、DP（固定轉換、training fit、fold、匯出）都有 markdown 與 code；第 4–6 章只有標題與「本章尚未完成」（T-義務：逐票補齊）。兩條老師原文與 `doc/requirement/` SRC-1 第 22 行、SRC-2T 第 36 行與第 82–83 行逐字相符。已執行且沒有 error 輸出（`test_notebook_structure.py`；乾淨環境重新執行成功） |
| AC-6 Dashboard 骨架：`.js` 全域變數、Chart.js 打包、靜態掃描無外部資源（BR-04；OV-1 前置） | **PASS** | `index.html` 只載入 `assets/vendor/chart.umd.js`、`assets/model_data.js`、`assets/app.js`；資料為 `window.MODEL_DATA`；Chart.js 4.4.1 與 npm 版本逐位元組相同。`offline_scan` 在工作樹與乾淨環境都 PASS，Reviewer 的 grep 結果相同。Kaggle URL 是以 `<a href>` 顯示的資料，依 Brief §7 BR-04「文件內的超連結不算資源」；掃描器的例外只限 `assets/model_data.js` 中這一個字串。`file://` 在所有主機名稱都無法解析的情況下正常渲染概覽區（A） |
| AC-7 單元 `.gitignore` 涵蓋 acceptor 材料、打包設定與輸出、虛擬環境、checkpoints；固定學號設定路徑並寫入 README（BR-03） | **PASS** | `.gitignore`：`*.pdf`、`*.zip`（`!/doc/requirement/*.pdf`）、SRC-2 PDF、`/.local/`、`/acceptor_materials/`、`/dist/`、`/.venv/`、`.ipynb_checkpoints/`、`.pytest_cache/`、`__pycache__/`。Reviewer 以 `git check-ignore -v --no-index` 探測 15 個應被忽略的路徑（含 `.local/packaging.json`、`acceptor_materials/` 下的 PDF 與筆記、`dist/` 下的 `*_hw2.zip`／`*_hw2.ipynb`／報告 PDF、`.venv/`、根目錄與子目錄的 `.ipynb_checkpoints/`、單元內任意 `*.pdf`／`*.zip`、SRC-2 PDF、`.env`），全部被忽略。`doc/requirement/` 下的 PDF（含 SRC-3 老師 PDF）依 `!/doc/requirement/*.pdf` 仍可追蹤；該目錄是上位契約，修改屬 RB-5。README「本機、不進 git 的設定與材料」列出 `.local/packaging.json`（`{"student_id": "<學號>"}`），緊接在「重跑步驟」之後；`paths.PACKAGING_CONFIG`、`local_config.read_student_id`（錯誤訊息不含值，有測試） |
| AC-8 `git grep` 無實際學號；追蹤檔案無 PDF（老師文件除外）、ZIP、金鑰（A-4） | **部分**：PDF／ZIP／金鑰 **PASS**；實際學號 **NOT VERIFIED**（R-1） | `git ls-tree -r f20d70e -- home_work_02` 中唯一的 PDF 是老師文件 SRC-3；整棵樹沒有 `.zip`、`kaggle.json`，單元內沒有 `.env`；單元內 `KAGGLE_KEY`／`KAGGLE_USERNAME`／`kaggle.json`／`api key`／`secret`／`token`／`password` 只命中 hygiene 測試的比對字串、wireframe 的 CSS 註解「token」與治理文字。**學號**：`.local/packaging.json` 不存在，`test_no_tracked_file_contains_the_student_id` skip（`tests/test_repo_hygiene.py:67-74`），A-4 指定的比對無法執行。替代證據（不等同 A-4）：35 個變更檔案中，「學號」每次出現都是 `<學號>` 佔位或敘述用詞（README 1 處、worklog 8 處，以遮罩後的上下文檢查）；每一段 7–12 位數字都歸類為 sha256 hex、CSV 房屋 `id`、8 位日期、資料數值、notebook cell id 或測試字面值 `A1234567`（以腳本分類，未印出數值）；`f20d70e`、`786d46b`、`7fe5ac2` 的 commit message 除了一個日期之外沒有 7–12 位數字。處理見第 5 節 R-1 |
| AC-9 資料與分割的耗時記入 `meta` 與 worklog | **PASS** | `meta.timing_s`：`data_load_validate` 0.0367、`split_and_folds` 0.0167（與 notebook cell 5、19 的輸出一致）；worklog §4 的量測表。Reviewer 乾淨環境：0.1347／0.049 |
| What to build：從乾淨環境執行資料階段 | **PASS** | 第 1 節乾淨環境重跑 |

## 3. 高風險類別核對（A-1）

| 類別 | 核對內容 | 結果 |
| --- | --- | --- |
| **H-1**（票已標示） | (a) 憑證：沒有使用 Kaggle CLI／API（資料是 acceptor 提供的鏡像，designation 第 6 點，來源記在 `meta.dataset.acquired_from`）；憑證字串掃描如 AC-8。(b) acceptor 材料、PDF、ZIP：如 AC-7、AC-8。(c) 學號：只有替代證據，A-4 比對未執行（R-1）。另以 grep 確認 subject 的輸出與 notebook 不含本機絕對路徑或本機使用者名稱（只有 docs 中公開的 GitHub 帳號）。Commit message 沒有學號形態的數字 | (a)(b) PASS；(c) NOT VERIFIED → R-1 |
| **H-3**（票已標示） | A-2：Reviewer 自行執行分組隔離測試（工作樹與乾淨環境各一次）並獨立重算（第 1 節）；不變量全部成立，M1–M3 被偵測。Fit 只用訓練列：前處理 API 只接收傳入的列，呼叫點 `export.build_model_data`（`prepared.training`）與 notebook cell 15（`train`）；追蹤的 `training_fit` 與 `inputs` 等於 Reviewer 只用 training 列的重算。TR-01：`load_and_split` 之外沒有 test 列的特徵或 `price`；追蹤的 `model_data` 沒有 `test`，`test_inputs` 沒有列；fixture 的 `model_data` 只寫到 `tmp_path`，寫正式路徑被守門拒絕（測試與 M5）。A-3：`methods`／`baselines`／`test` 尚不存在；`app.js` 只讀 `meta` 與 `preprocess.excluded_source_features`，沒有使用 `test_inputs`。選擇邊界、PI／coverage 與 Python／JS 一致性不在本票範圍（沒有選擇、模型、PI 或 JS 計算），自 #61～#63 起適用 | PASS；F-1、F-2、F-3 為 non-blocking |
| **H-2**（票未標示，見 F-5） | Notebook 六章的名稱與順序；`home_work_02/index.html` 路徑；`file://` 載入與零對外資源；README；資料集名稱與 Kaggle 連結；兩條老師原文逐字正確 | PASS |
| H-4 | 未觸及：沒有報告、acceptor 材料或 ACCEPTANCE.md；dashboard 只顯示匯出的 `meta`，沒有 wireframe 的 mock 數值或截圖（`grep mock` 只命中 `style.css` 對設計筆記的註解） | 不適用 |

## 4. Findings

### F-1 — 守門測試直接以追蹤中的正式 `model_data` 路徑為目標

- **Severity**：Low。**Blocking**：否。
- **證據**：`tests/test_contract_fixture.py:111-120` 把 `json_path=MODEL_DATA_JSON` 或 `js_path=MODEL_DATA_JS` 傳給 `export.write_model_data`；`:123-128` 以預設的正式路徑呼叫 `export.write_model_data(md)`，且已刪除 `meta.fixture`。守門在 `hw2/export.py:133`。Mutation M5（停用守門）在 scratchpad 複本跑 pytest 後，該複本的 `results/model_data.json` 與 `assets/model_data.js` 變成 68 列的 synthetic `model_data`，而且沒有 `meta.fixture`（dashboard 以 `meta.fixture` 顯示的警告也不會出現）。在目前的 subject 中守門正常，追蹤檔完整（`meta.fixture` false、`n_rows` 21,613、工作樹 diff 為空）。
- **契約條款**：共同條款「Test 資料隔離」（DA TR-01）：「Fixture 產生的 `model_data` 不得寫到被追蹤的正式 `model_data` 路徑」。
- **風險判斷**：只有在守門日後退化時才會發生（#61～#63 擴充 `hw2/export.py` 時可能改到它）；偵測有多層（守門測試失敗、`test_model_data_official.py:29` 失敗、git diff），所以判為 Low。
- **Disposition**：本票不需修改。建議由下一個修改 `hw2/export.py` 的票（預期 #61）的 Executor 把這些測試改成以登記為正式路徑的暫存路徑驗證守門（例如 monkeypatch `export.OFFICIAL_PATHS`），使守門退化也不會碰到追蹤檔。

### F-2 — `test_fit_uses_only_the_training_rows` 有一部分是恆真的

- **Severity**：Low。**Blocking**：否。
- **證據**：`tests/test_preprocess.py:68-74`：`_mutate_other_rows(frame, mask)[mask]` 選出的 training 列與 `frame[mask]` 完全相同，所以 `before == after` 必然成立，沒有真正改動到 fit 的輸入。這個性質目前主要由 API 的形式（只接收傳入的列）保證；其他證據足以支持 AC-2：同一測試對類別的斷言、`test_categories_come_from_training_rows_only`、`test_standardization_statistics_are_training_statistics`、`test_inputs_and_fit_come_from_the_training_rows`（追蹤的 fit 等於只用 training 列的 fit）、Reviewer 的重算，以及 M4 被偵測。
- **契約條款**：Spec rev 5 次 seam「前處理」：「fit 後的類別與統計量只由訓練列決定（改動驗證列不改變它們）」；#60 AC-2。
- **Disposition**：不需修改。供 #62 參考：fold-internal pipeline 出現後，「改動驗證列」的測試應作用在同時拿到訓練列與驗證列的呼叫點，因為洩漏真正可能發生在那裡。

### F-3 — `hw2.data.read_csv` 是公開且沒有守門的全資料讀取函式

- **Severity**：Low。**Blocking**：否。
- **證據**：`hw2/data.py:66-68` 回傳全部列（含 test 列的特徵與 `price`）。目前只在 `load_and_split` 內部與 `tests/test_data.py` 的結構測試中使用；Reviewer 檢查全部模組與 notebook，沒有任何程式以它推導 test 列的數值。
- **契約條款**：TR-01「正式 test 列的特徵與 `price` 只能經由 test 評估守門（G-3）載入」；G-3 守門屬 #61 的交付（#61 AC）。#60 的分割介面符合 AC-4。
- **Disposition**：本票不需修改。Owner：#61（Executor 與其 R1）；G-3 的設計需要涵蓋或限制這條讀取路徑。

### F-4 — `requirements.txt` 只鎖定直接與指定的套件

- **Severity**：Low。**Blocking**：否。
- **證據**：`requirements.txt:4-17` 鎖定 11 個套件；其餘遞移相依（例如 `pyzmq`、`tornado`、`pillow`、`fonttools`、`python-dateutil`、`tzdata`）在安裝時才解析。今天的乾淨安裝得到 55 個套件，與 Executor 的環境完全相同（`pip freeze` 無差異），所以目前沒有影響；數值結果取決於已鎖定的 numpy、pandas、scipy、scikit-learn、joblib、threadpoolctl。
- **契約條款**：Brief §10「鎖版本的 `requirements.txt`、乾淨環境完整重跑後數字一致」：目前成立。
- **Disposition**：不需處理。供 #67 的乾淨環境重跑參考：若觀察到版本漂移，記錄實際解析出的版本集合。

### F-5 — #60 觸及 H-2 的工作，但票只標示 H-1、H-3

- **Severity**：Low。**Blocking**：否。**Required authority**：Design Authority（標示的確認或修正）。
- **證據**：`decision-20261018-high-risk-categories.md` H-2 的「觸及的工作」包括「notebook 或報告的章節與標示 … README、dashboard 的路徑、資源載入方式與離線行為」。#60 建立了 notebook 六章、README、`home_work_02/index.html` 與它的 `file://` 載入方式；issue #60 與 derivation §9.1 都只標示 H-1、H-3。
- **影響**：A-1 的覆蓋：本 record 已在第 3 節核對 H-2，全部 PASS。A-7（H-2 的 blocking finding 若要 defer，需要 DA 確認）若沒有標示，就不會明顯連結到 #60。
- **Disposition**：route 給 DA 確認或修正標示；不需要修改實作。

## 5. Routing（需要其他 authority）

### R-1 — AC-8／A-4 的實際學號 `git grep`：required authority＝**Design Authority**

- **具體的 ambiguity**：A-4（`decision-20261018-high-risk-categories.md` §3）要求每張票結案前以 `git grep` 比對實際學號，比對值從本機未追蹤的學號設定讀取；#60 AC-8 重述這項要求。同一條契約鏈卻把學號設定排為 #67 的 acceptor 輸入（derivation §9.2「#67 另需學號設定」；`doc/ticket/tickets.md` #67；run record §1 designation 第 5 點「我會在 #66／#67 之前提供」）；Spec「Acceptor 輸入與等待」寫缺少 acceptor 輸入時「只停止對應章節與打包，其餘工作照常」。契約沒有說明在學號設定出現之前結案的票，要怎樣才算滿足 A-4／AC-8。可能的讀法：(i) #60 結案前必須執行 → 這是 acceptor 輸入的 boundary（治理 §1.5），由 Orchestrator 現在向 acceptor 取得 `.local/packaging.json`；(ii) #60～#66 以替代證據暫代，學號設定出現後再執行一次權威比對（須涵蓋當時全部追蹤檔，以及自 `e2d3e0b` 起曾變更但之後被移除的檔案的歷史）；(iii) 其他安排。
- **現況**：AC-8 的實際學號部分為 **NOT VERIFIED**。本 audit 的 closure 不證明這一項（治理 §4.4：audit closure 不豁免第 3.8 節的其他完成條件）。替代證據見第 2 節 AC-8。
- **H-1 備註**：這項風險在 push 後才變成不可逆（RB-6）。`f20d70e` 尚未 push；建議 DA 在任何涵蓋這個 subject 的 push 請求之前作出判定。
- **為何不是 blocking finding**：這是契約的不足（治理 §4.2：routing signal，不是對 implementation 的 blocking finding），而且 Executor 的 targeted correction 無法解決它。

F-5 也需要 DA（標示確認），見第 4 節。

## 6. 其他核對與備註（不是 finding）

- **EOL**：在 `core.autocrlf=true` 下，`git archive` 與 checkout 會把文字檔轉成 CRLF（例如 `results/split/split_assignment.csv`）；只有 `data/kc_house_data.csv` 與 `assets/vendor/**` 設為 `-text`。Subject 的讀取都用文字模式（`read_text`、pandas），所以 CRLF 的複本也通過（乾淨環境重跑就是從 CRLF 的 archive 複本執行，100 passed）。之後若要比對匯出檔的位元組（例如 #67 的「數字與追蹤的結果檔一致」或 ZIP checksum），應比對 git blob 或先統一 EOL。
- **Worklog 的主張**：V-1～V-9、V-12、V-13、Chart.js 的 integrity 與 binding 則數都已由 Reviewer 獨立重現或核對；V-10 以 Chrome 加上 DNS 封鎖重現；V-11（本機 `http.server`）沒有重做，已由 `file://` 加 net log 的檢查取代。
- **範圍**：沒有超出 #60 的實作。標準化 helper 屬 Spec「資料、計數與前處理」，該節分配給 #60；`local_config.read_student_id` 支援本票固定的 BR-03 路徑與 A-4 測試。沒有單元目錄以外的變更，也沒有修改 `doc/requirement/`（RB-5）。Commit message 符合 git 規則，沒有 Claude 標記。
- **Test 資料隔離的範圍說明**：`tests/test_data.py::test_real_csv_structure` 與 `test_split.py` 讀取全部列，但只用於結構事實（列數、唯一 `id` 數、`sqft` 恆等式）與 `id`；這在 AC-4 明文允許的「全資料層級結構驗證」之內，不是 TR-01 所禁止的使用。

## 7. 結論

- Blocking findings：無。
- Non-blocking findings：F-1、F-2、F-3、F-4、F-5（Low；disposition 見各項）。
- Routing：R-1（Design Authority；AC-8 的實際學號部分為 NOT VERIFIED，#60 是否完成依 DA 的判定），F-5（Design Authority）。

VERDICT: CLOSURE
