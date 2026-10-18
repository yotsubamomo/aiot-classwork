# Worklog — issue #60（HW2 T1 資料基線、分組切分與 model_data 契約骨架）

- **Work item**：GitHub issue [#60](https://github.com/yotsubamomo/aiot-classwork/issues/60)，run `run-20261018-hw2-formal`（Formal，並行度 1）。
- **狀態**：Executor 工作完成，待 Orchestrator 核對 binding 並派 R1 audit（本檔不代表 audit 或 closure）。
- **Subject**：branch `home_work_02-regrill`，base `e2d3e0b`；實作 commit 見第 5 節（本機 commit，未 push）。

## 1. Contract reference

| 項目 | 內容 |
| --- | --- |
| Ticket | #60（OPEN，`ready-for-agent`；含 TR-01 修訂後的 AC 與「Test 資料隔離」共同條款）；索引 `doc/ticket/tickets.md` |
| Spec | `doc/spec/SPEC.md` rev 5（#59）：「單元結構與交付物」「資料、計數與前處理」「分割與交叉驗證」「`model_data` 契約」的 `meta`／`preprocess`／`inputs`／`test_inputs`（schema）、Dashboard（骨架）、Testing Decisions 次 seam「分割」「前處理」 |
| DA derivation | `decisions/derivation-SPEC.md` §9.1（#60 的分配）、§9.3、§9.4、§9.6 TR-01（test 隔離：#60 只建 `test_inputs` schema 與 fixture，分割只對外提供 test 列識別與 n_test）；§3 B-14（極端值只用 training）、B-16（Brief 路徑）；§4 T-義務（學號設定路徑 BR-03、notebook 六章、外部 URL 靜態掃描） |
| 高風險 | `decisions/decision-20261018-high-risk-categories.md`：本票觸及 H-1、H-3（A-1、A-2、A-4） |
| Outcome Contract | `doc/governance/outcome-contract.md`：Brief @ `dff7c55c`＋CC-1、AD-1～AD-3；Brief §4（資料、sha256、commit 資料檔）、§7（離線）、§8（路徑）、§11 BR-03 |
| 授權 | `run/run-20261018-hw2-formal.md` §1 designation 第 2 點（Implementation 授權）、第 3 點（SA-1 本機 commit；不 push）、第 6 點（資料集以 acceptor 提供的 GitHub 鏡像為準並記錄來源） |
| Bindings | b5；HOW `impl-default` v2（overrides none） |

## 2. Executing role and binding

- **角色**：Executor（`gov-executor` subagent，由 Orchestrator 派工）。
- **Binding 觀測**（Bindings §3.6 指令的同一邏輯，掃描本 subagent 的 transcript）：agentId `a447664b1c57e651b`（`agent-a447664b1c57e651b.meta.json` 的 `agentType` = `gov-executor`），撰寫本節時觀測 `('claude-opus-5-5', 'high')` 140 則，單一元素，等於 O-1 mapping。全程核對（含本節之後的訊息）由 Orchestrator 在採用 return 前執行。
- **Escalation／替代**：無。
- **Bounded assignments**：未使用（沒有派 `gov-investigator` 或 `gov-bounded-worker`）。

## 3. Work performed

### 3.1 產物

| 路徑 | 內容 |
| --- | --- |
| `data/kc_house_data.csv` | 資料檔（acceptor 提供的 GitHub 鏡像；sha256 `d0875baa…57b7e`，與 Brief §4 釘住值相同，不需 re-pin）。依 Brief §4「commit 至 `home_work_02/data/`」與 Spec「資料檔 commit 在單元內」加入追蹤 |
| `hw2/paths.py` | 單元路徑、seed 42、test 比例 0.2、fold 數 5、未追蹤的本機位置（`.local/packaging.json`、`acceptor_materials/`、`dist/`） |
| `hw2/data.py` | sha256 先於解析的核對（不符時錯誤訊息含預期與實際值）；結構驗證（21 欄與順序、21,613 列、21,436 個唯一 `id`、無缺值、每列 `sqft` 恆等式）；`load_and_split()` 只回傳 training 列與 test 列識別（CSV 列序號、`id`）、n_test 與耗時，完整資料框留在函式內 |
| `hw2/split.py` | 以 `id` 分組的 80/20 切分（`default_rng([seed, 0])` 排列房屋）與分組 5-fold（`default_rng([seed, 1])`，依序發牌）；兩者只接受 id |
| `hw2/preprocess.py` | 19 個 source features、18 個 feature groups（canonical order＝CSV 欄序，排除 `sqft_basement`）；固定轉換 `sale_days`（基準日 2014-01-01）、`is_renovated`／`yr_renovated_effective`；只以給定訓練列 fit 的 `Preprocessor`（zipcode 類別取自訓練列、第一個排序類別為基準且不建欄、未見類別編為基準並回報；標準化只供 Ridge／Lasso，zipcode 欄不標準化、常數欄 scale 1）；`inputs`（training 的 min／max／median、zipcode 類別、日期範圍）；`preprocess` 規則 |
| `hw2/contract.py` | `test_inputs` schema：`fields` = `row`、`id`、`date`＋其餘 17 個建模 source features＋`actual_price`；`rows`（陣列，依 fields 順序）、`n_rows`、`n_houses`、`n_repeat_sales`、`written`；`empty_test_inputs()`（追蹤中的狀態：無列、計數為 null）、`build_test_inputs()`、`validate_test_inputs()` |
| `hw2/export.py` | `build_model_data()`（`meta`、`preprocess`＋整個 training set 的 fit、`inputs`、空的 `test_inputs`；沒有 `test`）；`write_model_data()` 同時寫 `.json` 與 `.js`（同一物件），`meta.fixture` 為 true 或未標示時拒絕寫到正式路徑；`write_split_assignment()` |
| `hw2/offline_scan.py` | Dashboard 的 html／css／js 靜態掃描（規則見模組 docstring；`python -m hw2.offline_scan`） |
| `hw2/local_config.py` | 讀取未追蹤的 `.local/packaging.json`（學號），錯誤訊息不含學號 |
| `hw2/run_notebook.py` | 以 nbclient 非互動執行 `hw2.ipynb` |
| `hw2.ipynb` | 主程式：六個 CRISP-DM 章節標題；Business Understanding（目標、研究問題、成功標準、資料來源與授權、兩條特徵數原文與 14–20 交集、19／18）、Data Understanding（全資料只做結構驗證；分布與極端值只用 training 列）、Data Preparation（固定轉換、training fit、fold、匯出）有內容；Modeling／Evaluation／Deployment 只有標題與「本章尚未完成」說明（T-義務：逐票補齊）。已執行，輸出在檔內 |
| `results/model_data.json`、`assets/model_data.js` | 正式 `model_data`：`meta`、`preprocess`、`inputs`、`test_inputs`（schema、0 列）；沒有 `test` |
| `results/split/split_assignment.csv` | 每筆交易的 `row`、`id`、`set`（train／test）、`fold`；不含特徵或價格 |
| `index.html`、`assets/app.js`、`assets/style.css` | Dashboard 骨架：概覽區（A）從 `window.MODEL_DATA.meta` 顯示資料集、授權、列數、sha256、19／18、切分與 fold、seed、版本、耗時；找不到資料或載入 fixture 時顯示警告 |
| `assets/vendor/chart.umd.js`、`chart.js.LICENSE.md` | Chart.js 4.4.1（npm registry `chart.js@4.4.1` tarball，integrity `sha512-C74QN1bx…534Dg==`；`chart.umd.js` sha256 `74401d73…fd8f3`，未修改；MIT 授權檔）。`chart.umd.js.map` 沒有打包：檔尾的 `sourceMappingURL` 是相對的本機檔名，只有開發者工具會嘗試讀取，不是對外請求 |
| `.gitattributes`（單元） | `data/kc_house_data.csv`、`assets/vendor/**` 設 `-text`：本機 `core.autocrlf=true`，沒有這條時 checkout 會把 LF 轉成 CRLF，使 sha256 釘住值失效（乾淨 clone 會在載入時停止） |
| `.gitignore`（單元） | `*.pdf`、`*.zip`（`doc/requirement/*.pdf` 除外，SRC-2 PDF 仍排除）、`/.local/`、`/acceptor_materials/`、`/dist/`、`/.venv/`、`.ipynb_checkpoints/`、`.pytest_cache/`、`__pycache__/` |
| `requirements.txt` | 鎖版本（ASCII）：numpy 2.4.6、pandas 3.0.6、scipy 1.17.1、scikit-learn 1.9.1、matplotlib 3.11.2、joblib 1.6.0、threadpoolctl 3.7.0、nbformat 5.11.1、nbclient 0.11.0、ipykernel 7.4.0、pytest 9.1.1 |
| `README.md`（單元） | 資料來源與授權、重跑步驟、未追蹤路徑表（含 `.local/packaging.json` 學號設定，BR-03 T-義務）、目前檔案配置。完整 README 屬 #65 |
| `pytest.ini`、`tests/` | 9 個測試檔（見第 4 節） |

### 3.2 重要決定與假設（HOW，Spec／Brief 留給實作者）

- **Seed 42**；切分與 fold 用同一個 seed 的兩個獨立亂數流。Test 比例以**房屋數**的 20% 抽樣，列數比例為 4,323／21,613＝0.20002。
- **`id` 保留 CSV 文字**（鏡像檔的 `id` 一律是 10 位、含前導零，2,059 列以 0 開頭）；`date`、`zipcode` 也保留文字。`price` 有 1,492 列以科學記號寫（例如 `1.225e+006`），解析為浮點數，數值不變。
- **`date` 的基準日**固定為 2014-01-01（Spec 只要求「固定基準日」）。
- **`test_inputs` 的列格式**：陣列（依 `fields` 順序）而不是物件，以縮小約 4,300 列的檔案；`date` 同時是列識別與 source feature，只出現一次。
- **`inputs`** 對 19 個 source features 都給出 training 的 min／max／median（`sqft_basement` 標 `modeled: false`）；`zipcode` 改給類別清單與眾數；`yr_renovated` 另給有整修列的範圍。
- **Fixture 防護**：`meta.fixture` 為 true 或缺少時，`write_model_data()` 拒絕寫入正式路徑。正式路徑定義在 `hw2/paths.py`（`results/model_data.json`、`assets/model_data.js`）。
- **靜態掃描的允許例外**（只有三類）：HTML `<a href>` 超連結；`assets/vendor/` 內 `/*! … */` 授權註解（Chart.js 的兩段 banner）；`assets/model_data.js` 中 Kaggle 資料集連結這一個字串（只以超連結顯示）。自有 JS 不得出現 `fetch`、`XMLHttpRequest` 等網路 API。
- 本票沒有需要 DA 裁決的語義問題。

### 3.3 Test 資料隔離（TR-01、H-3）的落實

- 只有兩個動作讀到全部列：sha256（位元組）與結構驗證（schema、列數、唯一 `id` 數、缺值、`sqft` 恆等式），都屬 AC 允許的全資料結構驗證。切分只用 `id` 欄。
- `load_and_split()` 的回傳值只含 training 列（含 `row`、`fold`）與 test 列的 `row`／`id`；pytest `test_load_and_split_returns_training_rows_and_test_identifiers_only` 斷言任何 DataFrame 屬性都不含 test 列。
- Notebook 的分布、極端值、`inputs`、zipcode 類別、fold 統計都只用 `prepared.training`。
- 被追蹤的 `model_data` 的 `test_inputs` 為 0 列、計數 null、`written: false`，沒有 `test` 區段（`test_no_test_rows_and_no_test_results_are_tracked`）。
- `test_inputs` schema 只以 synthetic fixture（`tests/conftest.py` 的亂數資料）驗證；fixture 的 `model_data` 只寫到 pytest 的 `tmp_path`，寫正式路徑會被拒絕且檔案不變（`test_fixture_model_data_is_refused_on_official_paths`）。
- `results/split/split_assignment.csv` 含 test 列的 `row`／`id`（識別），沒有特徵或價格。
- 本票沒有建立 G-3 守門（屬 #61）；也沒有任何載入 test 列特徵或 `price` 的公開函式。

## 4. Verification

環境：Windows 11、Python 3.11.2（`home_work_02/.venv`，依 `requirements.txt`）、Node v24.19.0、Microsoft Edge（headless）。

| # | 方法 | 結果 | 證據 |
| --- | --- | --- | --- |
| V-1 | `.venv/Scripts/python -m pytest -q -rs`（`home_work_02/`） | **115 passed, 1 skipped**；skip 是 `test_no_tracked_file_contains_the_student_id`：`.local/packaging.json` 尚未提供（見第 7 節） | 本機執行輸出 |
| V-2 | 次 seam「分割」：真實 `id`（只讀 `id` 欄）上 train／test 無共同 `id`、聯集為全部列、同 seed 重現且換 seed 不同、比例 0.2±0.005、fold 兩兩無共同 `id`、聯集等於 training、fold 大小差 < 1%、fold 與列順序無關；synthetic 重複交易同側同 fold；錯誤參數報錯 | 通過 | `tests/test_split.py` |
| V-3 | 次 seam「前處理」：`sale_days` 數值案例（0、1、285、365、511）與錯誤日期；整修衍生欄三個案例與負值報錯；fit 後的類別與標準化統計量只由訓練列決定（改動非訓練列後重新 fit 相等）；未見 zipcode 編為基準且計數；已知 zipcode 只設自己的欄；canonical 欄序；標準化統計量等於 training 均值／標準差；`inputs` 只由訓練列決定 | 通過 | `tests/test_preprocess.py` |
| V-4 | 資料：真實檔 sha256 與結構事實；sha256 不符時訊息含兩個值且先於解析；schema、列數、`id` 數、`sqft` 恆等式、缺值各一個失敗案例 | 通過 | `tests/test_data.py` |
| V-5 | `test_inputs` schema 以 synthetic fixture 驗證：欄位涵蓋識別、18 個 features、`actual_price`；重複交易計數；10 種竄改各被拒；列數與 n_test 不符被拒；fixture `model_data` 的 `.json`／`.js` 往返相同；fixture 寫正式路徑被拒且檔案不變 | 通過 | `tests/test_contract_fixture.py` |
| V-6 | 正式 `model_data`：`.json` 與 `.js` 相同；`meta` 的 sha256、seed、版本、n_train 17,290／n_test 4,323、fold 數 5、耗時；無 `test`、`test_inputs` 0 列；`inputs` 與 `training_fit` 等於只用 training 列重算的值；split assignment 只有識別欄 | 通過 | `tests/test_model_data_official.py` |
| V-7 | Notebook：六章標題依序；前三章有 markdown 與 code；已執行且無 error 輸出；只有 `<學號>` 佔位 | 通過 | `tests/test_notebook_structure.py` |
| V-8 | 靜態掃描 `python -m hw2.offline_scan`（index.html、app.js、style.css、model_data.js、vendor/chart.umd.js） | `scanned 5 files: PASS (0 findings)`；掃描器本身有 1 個允許案例與 11 個應報案例的測試 | `tests/test_dashboard_static.py` |
| V-9 | `node --check` app.js、model_data.js；Chart.js sha256 等於 npm 4.4.1 版本 | 通過 | 同上 |
| V-10 | `file://` 實際載入：`msedge --headless=new --dump-dom file:///…/home_work_02/index.html` | DOM 中 `meta-rows` = 21,613、`meta-sf` = 19、`meta-ntest` = 4,323、`chartjs-version` = 「Chart.js 4.4.1（本機打包）」、錯誤框 hidden：`.js` 全域變數與打包的 Chart.js 在 `file://` 下可用 | 本機執行輸出 |
| V-11 | 內建瀏覽器以本機 `http.server`（127.0.0.1）開啟 | 網路請求只有 5 個本機檔（index.html、style.css、chart.umd.js、model_data.js、app.js）；console 無訊息；474 px 與 1440 px 皆無水平溢出；資料集連結 href 為 Kaggle 頁 | 本機執行輸出 |
| V-12 | **乾淨環境重跑**（README 步驟）：把單元複製到 scratch（不含 `.venv`、`results/`、`assets/model_data.js`），`py -3.11 -m venv` → `pip install -r requirements.txt` → `python -m hw2.run_notebook` → `pytest` → `offline_scan` | 安裝成功；notebook 執行成功；113 passed、1 skipped（當時尚未加入 `.gitattributes` 的 2 個測試）；掃描 PASS；`split_assignment.csv` 與本機版**位元相同**；`model_data.json` 除 `meta.timing_s`、`meta.generated_at` 外完全相同 | 本機執行輸出 |
| V-13 | `git check-attr text` 對 `data/kc_house_data.csv`、`assets/vendor/chart.umd.js` 為 unset；staged blob 的 sha256 等於釘住值（CSV `d0875baa…57b7e`、Chart.js `74401d73…fd8f3`）。`git check-ignore`：`.local/packaging.json`、`acceptor_materials/…`、`dist/…`、`.venv/…`、`.ipynb_checkpoints/…`、任意 `*.pdf`／`*.zip`、SRC-2 PDF 都被忽略；SRC-3 老師 PDF 仍可追蹤 | 通過 | `tests/test_repo_hygiene.py` |
| V-14 | A-4（commit 後對追蹤檔案）：見第 5 節 | — | — |

**執行時間量測（Q34）**

| 項目 | 主要執行 | 乾淨環境 |
| --- | --- | --- |
| 資料載入與結構驗證（`meta.timing_s.data_load_validate`） | 0.0367 s | 0.0536 s |
| 切分與 fold（`meta.timing_s.split_and_folds`） | 0.0167 s | 0.0212 s |
| 整本 notebook 非互動執行 | 1.6 s | 5.4 s（含首次 kernel 啟動） |
| `pip install -r requirements.txt`（新虛擬環境） | — | 3 分 33 秒 |
| pytest 全部 | 1.1 s | 2.1 s |

**限制**：未在網路停用的環境測試（OV-1 正式 gate 屬 #67）；V-10 證明 `file://` 載入可用，V-8 證明沒有外部資源引用。手機實機、其他瀏覽器、無障礙與對比（OV-2～OV-5）不在本票範圍。

## 5. Commit 與 A-4 核對

（commit 後補記）

## 6. Audit status

- **Required**（Formal：每張票都要 independent audit；Bindings §5）。觸及 H-1、H-3：依 A-1 需要 R1 record 的類別核對節，依 A-2 Reviewer 自行執行分組隔離測試，依 A-4 核對追蹤檔案。
- 進度：尚未派工（由 Orchestrator 依 Bindings §3.7 派 `gov-primary-reviewer`）。本檔的 self-verification 不是 audit。

## 7. Remaining work and follow-up

- **學號的 `git grep`（A-4、AC「`git grep` 無實際學號」）**：核對程式已實作（`tests/test_repo_hygiene.py`，從 `.local/packaging.json` 讀取，不印出值），但 acceptor 尚未提供該設定，所以本票無法以實際值執行；目前只能確認本票新增的檔案沒有任何真實學號（本 Executor 沒有取得學號）。需要 acceptor 放入 `.local/packaging.json` 後由 Reviewer 或後續票執行（required authority：acceptor 提供輸入）。
- `chart.umd.js.map` 未打包（見 3.1）；若 #67 的 DevTools 離線檢查把 source map 讀取記為請求，再決定是否加入 map 檔。
- G-3 守門、Node test、其他 dashboard 區塊、notebook 第 4–6 章：依票分配屬 #61～#64。
- 未 push（designation 第 3 點：push 需 acceptor 逐次授權）。
