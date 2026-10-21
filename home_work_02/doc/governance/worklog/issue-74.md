# Worklog — #74 HW2 V2-T1（Problem 下拉、50 Startups 內建資料與 Exploratory run 的 All-in 垂直切片）

- **Work item**：GitHub issue #74（V2-T1），Formal lane，run `run-20261022-hw2-v2-enhance`（Orchestrator＝root session `37216426-f292-44f9-bad1-e2d862e7b8f1`）。
- **執行角色**：Executor（治理 §2.1；`gov-executor`，有效 mapping `claude-opus-5-5`／`high`，Bindings b5 §3.1 O-1）。
- **Subject**：branch `home_work_02-v2-enhance`（未 push）。BASE `506581aea6db04422d087c4e22c5dcf211c734e9`；實作 commit `1bd1df8c72808c807d231d20400be1d1c9d415a2`；之後的紀錄 commit 只改 `doc/`（本 worklog、`doc/screenshots/v2-issue74/` 的證據），沒有程式、資料或測試的變更（§5）。
- **狀態**：cycle 1 R1 BLOCKING（R1-F1）→ targeted correction 完成（§9），待 R2。

## 1. Contract reference

| 契約 | 位置與版本 |
| --- | --- |
| Outcome Contract | `doc/governance/outcome-contract.md` §5（V2 接受紀錄，接受基準 `d7f02d4`）、§5.2 **CC-V2-1**（只允許修改 `tests/test_dashboard_static.py::test_page_loads_data_as_a_js_global_and_the_bundled_chartjs` 的 `<script src>` 斷言：前四項仍是 V1 四檔、順序不變，其後逐一列出 V2 腳本；其他既有測試不變） |
| Ticket | GitHub #74（body sha256 `49e3cc50…1441`，DA derivation §3） |
| Spec | `doc/spec/SPEC-V2.md` rev 2（sha256 `695161db…f9a5`）；未提到的事項以 `doc/spec/SPEC.md` rev 5 為準 |
| Brief | `doc/brief/BRIEF-V2.md` rev 2＋E-1；`doc/brief/BRIEF.md`（V1） |
| DA derivation | `doc/governance/decisions/derivation-SPEC-V2.md`：#74 類別 H-1～H-5、assurance A-1～A-5、A-7～A-9（§7.4）；G-2（§5.2）；D-2、I-2、I-3、I-5（§8）；F-5 HOW 提示（§9） |
| Run invariants | run record §1 designation 第 4–7 點（經 CC-V2-1 修訂） |

## 2. Binding

| 對象 | 觀測（Bindings §3.6 指令，全部 assistant 訊息） | 結果 |
| --- | --- | --- |
| 本 assignment，agentId `addc2dc935a7822fe`（`agentType` `gov-executor`） | `('claude-opus-5-5', 'high')`：190 則（截至寫入本節；return 前由派工者依 §3.6 全程核對） | 單一元素，等於有效 mapping；無 escalation、無替代 |

- Bounded assignments：**未使用**（沒有派 `gov-investigator`／`gov-bounded-worker` 或任何 subagent）。

## 3. Work performed

1. **讀取與基準**：Bindings b5、Implementation Profile §3–§5、§9、治理 §3.5、§3.7、§3.8、Outcome Contract §5／§5.2、Spec V2 rev 2、Brief V2、`tickets-v2.md`、DA derivation、run record；既有 `index.html`、`assets/app.js`、`hw2core.js`、`style.css`、`hw2/offline_scan.py`、`ols.py`、`metrics.py`、`models.py`、相關測試。修改前跑基準測試（§6）。
2. **50 Startups 內建資料**（I-3）：以 `curl` 取得老師的 URL（HTTP 200、2,436 bytes），檔案原樣存成 `assets/data/50_Startups.csv`（CRLF、無 BOM、檔尾無換行；`.gitattributes` 加 `assets/data/** -text`）。以 `gh api` 重查：repo 授權 MIT（`LICENSE` blob `00542313…1961`）、最後修改該檔的 commit `5cd8936a…a74`、`master` @ `5d67810c…9891`；`git hash-object --no-filters` 等於 GitHub 的 blob `14ffb860…b439`。sha256 `c6075ca5a7551243b31193bad9228f0a1b9468cdde2475c6586c56dcfac5630d`。來源 URL、日期、sha256 寫在掃描範圍外的 `assets/data/50_Startups.SOURCE.md`（I-2）；MIT 聲明原文在 `50_Startups.LICENSE.md`；`assets/data/startups50.js` 以 JSON 字串內嵌同一份文字（由 scratchpad 的產生程式寫出，檔頭註明）。
3. **載入契約** `assets/explore_load.js`：純函式 CSV 文字或 bytes → `LoadResult`；八個拒絕原因、BOM、RFC 4180 引號、修剪空白、字面數字判定、缺值刪列、目標規則、sha256（自寫 SHA-256，不依賴 Web Crypto）。`LoadResult` 沒有任何欄位的保留／排除狀態（SR-V2-01）。
4. **引擎** `assets/explore_engine.js`（純函式）：mulberry32＋Fisher–Yates 的 80/20 與 5-fold；第二層只用訓練列決定 20 層級上限與常數欄；第三層每個 fold 只用該 fold 訓練列的層級、基準、one-hot 與 OLS；A-1（滿秩＋df_resid ≥ 3）；pivoted Householder QR（equilibrated，容忍度與 `hw2/ols.py` 同）；Student t 分位數；CV＝算術平均＋樣本標準差；winner 固定後才讀 test 列，只對 winner 算 test 指標、逐筆 PI、covered、coverage；結果契約 `run`（`COMPLETED`／`REJECTED`＋`ALL_CANDIDATES_INVALID`）、`meta`、`columns`、`groups`、`split`、`candidates`、`winners`、`test`；即時預測器 `inputSpec`／`predict`／`canPredict`。
5. **通用 Python 參照** `hw2/explore_reference.py`（新模組，只供測試）：同一套載入、PRNG、三層邊界與 All-in；重用 `hw2.ols.fit_ols`、`ols.log_interval`（公式在原始尺度直接使用，不取 exp）、`hw2.metrics.usd_metrics`、`coverage_stats`；不 import King County 專屬函式、不讀 `model_data`、不依賴 JS 結果。
6. **頁面**：`index.html` 加 `assets/explore.css`、`</header>` 後的 problem 下拉（`#problem-select`，三項依序，預設 King County，`autocomplete="off"`）、`<main>` 內 `#overview` 之前的 `#explore` 子樹（id 一律 `ex-`；每個區塊標題帶「探索執行，非正式評估」；KPI 標「訓練 CV」；test 區塊標「探索 test（非正式評估）」；自訂資料集是「由 V2-T3 提供」的佈局佔位，沒有輸入控制項），以及 V1 四個 `<script>` 之後的六個 V2 腳本。`assets/explore_app.js`（不碰 DOM 的 controller，依賴可注入）、`explore_ui.js`（DOM；只用 `textContent`、`createTextNode`、`<option>.text` 與非 URL 屬性，D-2）、`explore_plot.js`（V2 自己的線性刻度散佈圖，Tickets Review 調整 A；V1 腳本未修改）。
7. **測試**：Node `tests/js/explore_load.test.js`、`explore_boundary.test.js`、`explore_app.test.js`、`explore_contract.test.js`；pytest `tests/test_node_explore.py`（即時產生 Python 參照寫到暫存路徑並執行 Node）、`tests/test_explore_static.py`（V1 區塊結構快照、V1 檔案 sha256、內建資料、隔離規則）；快照 `tests/snapshots/v1_dashboard_blocks.json` 由 `git show d7f02d4:home_work_02/index.html` 產生。依 CC-V2-1 修改既有斷言（只有那一條，§4 D-8）。
8. **ACCEPTANCE**：新增 G 節 V2-1～V2-9（#74 範圍），既有 A～F 節不變。
9. **瀏覽器 self-verification**（§6.3）與 **H-5 探測**（§6.4）；證據截圖與報告在 `doc/screenshots/v2-issue74/`。

## 4. Decisions and assumptions

都在 accepted contract 的 HOW 範圍內；沒有改變任何 requirement、AC、invariant 或 gate。

| # | 決定 | 依據 |
| --- | --- | --- |
| D-1 | PRNG＝mulberry32（32 位元整數運算）＋Fisher–Yates；切分用 `mulberry32(seed)`、fold 用 `mulberry32(seed + 1)`；seed 42；`n_test = floor(0.2n + 0.5)`（限 [1, n−1]），洗牌後前 n_test 列為 test；fold＝訓練列洗牌位置 mod 5 | Spec「切分與交叉驗證」：演算法由實作決定並記錄 |
| D-2 | 載入規則細節（HOW）：修剪 ASCII 空白；空字串＝缺值；數值欄＝至少一個非空儲存格且全部是字面十進位數字（ASCII 數字、可含正負號、小數點、指數）且有限；`NO_HEADER`＝欄名有空白或全是數字；`NOT_CSV`＝空白文字、少於兩欄、未結束的引號、閉合引號後有其他文字；`ENCODING`＝非 UTF-8 bytes 或含 U+FFFD／U+0000；檢查順序記於檔頭；未加引號欄位中的引號當字面字元；空白列略過 | Spec「載入契約」列出原因碼，判定細節屬 HOW；D-2（不求值運算式） |
| D-3 | 載入上限暫用 Spec 候選值 50,000 列 × 60 欄（`LIMITS`），最終數字的實測與記錄留給後續票 | Spec「運算預算與載入上限的數字是實作常數，由實測決定並記錄」 |
| D-4 | 層級順序＝在該次訓練列（列序遞增）中第一次出現的順序；基準＝第一個；one-hot 欄依此順序；未見層級的列編為基準並計數（每 group 與任一未見的列數） | Spec「基準＝該 fold 訓練列中最先出現的層級」 |
| D-5 | 沒有任何 feature group（全部欄位在訓練列上被排除）時，All-in 記為 `INVALID_MODEL`（`no_feature_groups`），因此 `run = REJECTED`／`ALL_CANDIDATES_INVALID`；不新增 run 層級的原因碼 | Spec「所有候選皆非 VALID 時…拒絕 ALL_CANDIDATES_INVALID」；不發明新碼 |
| D-6 | `REJECTED` 結果沒有 `candidates`／`winners`／`test`（Spec 契約不變量），無效候選的狀態與原因（規則、fold、rank、df_resid）放在 `run.invalid_candidates`，使 AC「INVALID_MODEL 附原因與 fold」可觀察 | Spec「契約不變量」與 A-1 原因必附 |
| D-7 | #74 只有 All-in：它是唯一候選，因此是整體 CV winner；`winners.method_winners` 為空；共線診斷（`dependencies`）屬 #75，本票結果不含此欄（不以空清單冒充「沒有相依」） | Ticket #74／#75 的分工 |
| D-8 | CC-V2-1 的修改只動那一條 `assert scripts == [...]`：前四項不變，其後依載入順序列出 `assets/data/startups50.js`、`explore_load.js`、`explore_engine.js`、`explore_plot.js`、`explore_app.js`、`explore_ui.js`；不加其他行 | CC-V2-1 |
| D-9 | 探索子樹放在 `#load-error` 之後、`#overview` 之前，problem 下拉放在 `</header>` 後的獨立控制列；V1 的 header、區塊與 footer 不改。探索時以 `hidden` 隱藏五個 V1 區塊與 `#load-error`（返回時還原原狀），並以 `body.is-exploring` 隱藏指向 V1 區塊的頁內導覽 | Spec「Problem 與頁面結構」；I-5（既有以區段切片的測試不需修改即成立） |
| D-10 | 樣式放在新的 `assets/explore.css`，沿用 V1 的 token 與 class；`assets/style.css` 不改 | V1 不變量 |
| D-11 | 數值欄預測器的預設值顯示為中位數取 12 位有效數字（去除浮點雜訊，例如 127188.29500000001 → 127188.295） | UI 呈現；差異遠小於任何容忍度 |
| D-12 | V1 檔案的 sha256 斷言以換行正規化為 LF 的內容計算（＝git blob；Windows checkout 會把 LF 轉為 CRLF），另以 `git diff --name-only d7f02d4` 在有 git 時補強 | A-3 的值是 blob 的 sha256 |
| D-13 | Node 對 Python 的數值比較：相對容忍度 1e-6（期望值為 0 時絕對 1e-12）；字串、布林、整數結構（切分、fold、狀態、原因、covered）逐值相同；不變量的 PI 重算以 1e-9 | Spec Testing Decisions；DA `decision-20261018-issue63-js-tolerance.md` T-1 |

## 5. Artifacts

實作 commit `1bd1df8c72808c807d231d20400be1d1c9d415a2`（26 個檔案，+7,799／−1；全部在 `home_work_02/` 內，不含 `doc/requirement/`）：

- 新增：`assets/data/50_Startups.csv`、`50_Startups.SOURCE.md`、`50_Startups.LICENSE.md`、`startups50.js`；`assets/explore_load.js`、`explore_engine.js`、`explore_plot.js`、`explore_app.js`、`explore_ui.js`、`explore.css`；`hw2/explore_reference.py`；`tests/js/explore_load.test.js`、`explore_boundary.test.js`、`explore_app.test.js`、`explore_contract.test.js`；`tests/test_node_explore.py`、`tests/test_explore_static.py`、`tests/snapshots/v1_dashboard_blocks.json`；`doc/screenshots/v2-issue74/*.png`。
- 修改：`index.html`（只新增）、`.gitattributes`（只新增）、`tests/test_dashboard_static.py`（只有 CC-V2-1 那一條斷言，`git diff` 3 行新增、1 行刪除）、`doc/acceptance/ACCEPTANCE.md`（只新增 G 節）。
- 不變（核對見 §6.2）：`assets/app.js`、`hw2core.js`、`model_data.js`、`style.css`、`vendor/`、`results/`、`hw2.ipynb`、其他既有 `hw2/*.py` 與既有測試、`doc/spec/`、`doc/ticket/`、`doc/brief/`、`doc/requirement/`。

紀錄 commit（本 worklog 所在）：本 worklog；`doc/screenshots/v2-issue74/` 的截圖換成在 `1bd1df8` 乾淨 clone 上擷取的版本，並加入 `browser_check_chrome.json`、`browser_check_edge.json`（已去除本機路徑）。

## 6. Verification

### 6.1 自動測試

| 時點／subject | 指令 | 結果 |
| --- | --- | --- |
| 基準（BASE `506581a`，修改前） | `.venv/Scripts/python -m pytest -q`（Python 3.11.2） | **398 passed，0 skipped**，54.23 s |
| 基準 | `node --test tests/js/core.test.js`（Node v24.19.0，未設 fixture） | 9 pass、3 skipped（fixture 項目；經 pytest 執行時 skipped 0） |
| 工作目錄（＝`1bd1df8` 的內容），主要 checkout | `python -m pytest -q -rs` | **433 passed，0 skipped**，52.35 s（新增 35 項） |
| 同上 | `node --test` 個別檔案 | `explore_load` 15/15、`explore_boundary` 7/7、`explore_app` 9/9（各 skipped 0）；`explore_contract` 與 `core` 單獨執行時因未設參照而 skip（設計如此），經 pytest 執行時 skipped 0 |
| 同上，參照寫到 scratchpad 後直接執行 | `HW2_EXPLORE_REFERENCE=<dir> node --test tests/js/explore_contract.test.js` | **13 pass，0 fail，0 skipped**（PRNG、載入對照 11 段文字、9 個 case、A-1、內嵌文字） |
| `1bd1df8` 的乾淨 sparse clone（無 `.local/`、無 acceptor 材料） | `python -m pytest -q -rs` | **430 passed，3 skipped**，54.69 s；skip 只有 `test_repo_hygiene.py:72`（`.local/packaging.json` 不在 clone）、`test_report.py:547`、`:584`（作者的未追蹤材料），與本票無關；主要 checkout 上這三項通過 |
| 主要 checkout，`git add` 之後 | `pytest tests/test_repo_hygiene.py` | 17 passed，0 skipped（學號 `git grep -F` 0 命中，值不印出；新增檔案已在 index 中） |
| — | `python -m hw2.offline_scan` | `scanned 13 files: PASS (0 findings)`（V2 檔案沒有任何 `fetch(`） |

主 seam 的 case：(a) 50 Startups；(b) synthetic 非退化（120 列，3 數值＋2 類別欄，numpy seed 74）；(d) 恰好 20 列、單一類別欄、全部數值（G-2）；A-1：只在某 fold 訓練列秩不足（`spike` 只在 fold 2 驗證列非零）→ `INVALID_MODEL`／`rank_deficient`／fold 2，`run = REJECTED`；20 列 × 11 特徵 → 五個 fold 都 `df_resid_lt_3`；`x3 = x1 + x2` → 五個 fold 與整個訓練集都秩不足；沒有 feature group → `no_feature_groups`。每個 case 比對 LoadResult、切分與 fold、欄位狀態、候選狀態與原因、各 fold 子集／層級／指標／係數、CV 平均與標準差、canonical 係數、(XᵀX)⁻¹、s²、df_resid、t、Adjusted R²、winners、test 指標、逐筆 predicted／lower／upper（1e-6）與 covered（逐值）、coverage；並以測試內自寫的程式檢查契約不變量與逐筆 PI 重算。

**Mutation 檢查**（確認測試有鑑別力，事後已還原並 `cmp` 確認）：t 臨界值乘 (1＋2e-6) → contract 6 項失敗；fold 指派位移 → 10 項失敗；V1 `#methods` 文字加一個句號、或 `#k-grid` 加一個屬性 → 快照測試失敗。

50 Startups（All-in，參照與 JS 一致）：切分 test 列 [2, 10, 15, 24, 33, 35, 38, 39, 43, 47]（40／10），全部欄位保留，All-in `VALID`（k = 4，State 基準 New York），df_resid 34。數字只記在這裡作為 self-verification 證據，不進 README 或報告（I-4）。

### 6.2 不變量核對（A-3、I-5、CC-V2-1）

- `git diff --cached --name-only`（commit 前）：26 個路徑全部在 `home_work_02/`；對 `doc/requirement`、`results`、`hw2.ipynb`、`assets/app.js`、`hw2core.js`、`model_data.js`、`style.css`、`doc/spec`、`doc/ticket`、`doc/brief` 為空；既有檔案中被修改的測試只有 `tests/test_dashboard_static.py`，既有 `hw2/*.py` 沒有修改。
- V1 檔案 sha256（LF 正規化）等於 A-3 值：`app.js` `c1ab3f21…82ad`、`hw2core.js` `e75c5d48…2c14`、`model_data.js` `6cf0c11e…a7ac`、`results/model_data.json` `69dc1465…6e61`；`style.css` `60a27016…5f3f`（`tests/test_explore_static.py`）。
- 既有 `tests/test_dashboard_static.py` 其他斷言（區段切片、`#methods` 到 `</main>` 恰四個 `<article>`、沒有 `http`）不需修改即通過。
- 探索檔案不含 `MODEL_DATA`、`model_data`、`test_inputs`、`HW2Core`；也不含 `innerHTML` 等寫入 markup 或執行字串的 API、網路 API、storage（`test_explore_static.py`）。

### 6.3 瀏覽器（AC「人工檢查表」與 UI 一致性；Executor self-verification）

- **方法**：scratchpad 的 `browser_check.js`，以 DevTools Protocol 驅動 headless Google Chrome 155.0.8059.85 與 Microsoft Edge 155.0.4283.62；開啟 `file://` 的 `index.html`；網路以三種方式封鎖（`Network.emulateNetworkConditions` offline、`--host-resolver-rules=MAP * ~NOTFOUND`、無效 proxy），記錄每個 `Network.requestWillBeSent`、例外與 console 錯誤。Windows 11 Pro 10.0.26200，Intel Core i9-13900HX。最後一次在 `1bd1df8` 的乾淨 sparse clone 上執行；報告 `doc/screenshots/v2-issue74/browser_check_chrome.json`、`browser_check_edge.json`。
- **結果（Chrome 與 Edge 相同）**：
  - 下拉三項依序、預設 King County、探索子樹隱藏；Tab 第 7 下到達下拉，focus 外框 3px solid；ArrowDown 切到 50 Startups（鍵盤可操作，OV-4）。
  - 選 50 Startups 即完成：All-in `VALID`，四個訓練 CV KPI、fold 表、全訓練集擬合、五個探索 test KPI（含 PI 涵蓋率）、散佈圖已繪製（非白像素 7,979）、預測器四個輸入（三個數值、State 下拉：New York（基準）、California、Florida）並給出點預測與 PI；四個探索區塊標題都有「探索執行，非正式評估」。**執行時間**（頁內量測，5 次）：change handler（載入＋執行＋繪製）Chrome 2.0～4.0 ms、Edge 2.1～6.8 ms；controller（載入＋引擎）Chrome 0.4～1.7 ms、Edge 0.4～3.7 ms（不設門檻）。
  - 預測器輸入 R&D Spend＝9,999,999（超出訓練範圍）仍計算，顯示一則超出範圍警告。
  - 自訂資料集：只顯示佔位區塊，其中輸入控制項 0 個。
  - 切回 King County：五個 V1 區塊的 `innerText` 與切換前逐字相同；V1 區塊沒有「探索」字樣；V1 散佈圖首次繪製 248 ms（Chrome）／245 ms（Edge）。
  - **零對外請求**：三次載入與全部切換，非 `file:`／`data:` 請求 0 個（`data:` 只有 V1 既有的 CSS 內嵌圖），console 錯誤與例外 0。
  - **OV-2**：375 px 與 768 px 下 King County、50 Startups、自訂資料集三種狀態的水平溢出都是 0 px。真實觸控裝置 NOT TESTED（無環境）。
  - **OV-5**：下拉列與探索區塊的可見文字共 173 處（375 px：172 處），最低對比 6.74:1（`.muted` 說明文字），需求 4.5:1；涵蓋狀態以圓點／方塊區分，不只靠顏色。
  - **zh-TW 無缺字**：目視 `chrome_startups50_1280_full.png`、`chrome_startups50_375_full.png`、`chrome_custom_1280.png`、`chrome_kc_1280.png`，沒有缺字方塊。
- 限制：headless 瀏覽器由 Executor 驅動，不是 acceptor 的人工操作；螢幕閱讀器、真實觸控、Firefox／Safari 未測（AD-1 的 best-effort 項目）。

### 6.4 H-5 探測（A-9 的同一風險；self-verification，不是 R1 證據）

把 `index.html` 與 `assets/` 複製到 scratchpad，將內嵌資料換成刻意構造的 CSV（欄名 `<img src=x onerror="document.title=1">`、`</script><b>bold</b>`、`javascript:alert(1)`；類別值 `<svg onload=alert(1)>`、`a&amp;b`、`"><iframe src=//evil.example>`），在 headless Chrome、斷網下選 50 Startups：`run = COMPLETED`；`#explore` 內 `img`／`svg`／`iframe`／`b`／`script` 元素 0 個；欄位表、預測器 label 與下拉選項全部以字面文字顯示；`document.title` 未變；dialog 0、例外 0、對外請求 0；切回 King County 內容逐字不變。另有靜態測試禁止 V2 檔案使用 `innerHTML` 等 API（§6.2）。

## 7. Audit status

- Formal：本票 independent audit **required**（Bindings §5；治理 §4.1；DA derivation §7.4：H-1～H-5，A-1～A-5、A-7～A-9）。由 Orchestrator 依 Bindings §3.7 派工；本 worklog 不記錄 audit 結果。
- R1 須以 H-2 核對 CC-V2-1 的那一條斷言（outcome-contract §5.2）。
- 以上 §6 全部是 Executor self-verification，不是 audit。

## 8. Remaining work and concerns

- **本票範圍內**：無未完成項目。
- **留給後續票（依 tickets-v2 分工，不是本票缺口）**：四種方法、winner 規則、Lasso 退化、共線診斷 `dependencies`、G-1 的切分限制揭露（#75）；URL／檔案輸入、目標選擇、`offline_scan` 單檔 `fetch` 例外、mock fetch 第五條、三向切換（#76）；運算預算、`SKIPPED_RESOURCE_LIMIT`／`FAILED`、取消、非阻塞、進度、可重現性、載入上限與預算的最終數字（#77）；README、報告探索章節、ACCEPTANCE 彙整、OV-1／SR-09 重做、ZIP（#78）。
- **觀察（給 Orchestrator／Reviewer，不需決定）**：
  1. 自訂資料集的佔位文字依票面寫「由 V2-T3 提供」，屬開發中的暫時用語，#76 會替換。
  2. 證據截圖與瀏覽器報告追蹤在 `doc/screenshots/v2-issue74/`（`doc/` 不進 ZIP，`package.tracked_files()` 排除）。
  3. 新模組 `hw2/explore_reference.py` 會隨 `hw2/` 進入 ZIP（#78 重打包時會看到）；它只被測試 import。
- **Push**：未 push（OC §5.1 未授權）。

## 9. Targeted correction — cycle 1，R1-F1（2026-10-22）

- **來源**：R1 audit record `doc/governance/audit/issue-74-c1-r1.md`（commit `0631bc1`）的 R1-F1（Medium，blocking；H-4／A-5）：`doc/acceptance/ACCEPTANCE.md` V2-3 的執行時間「change handler 2.1～5.2 ms、引擎 0.4～2.5 ms」與它引用的 committed evidence 不符。這些數值來自較早一次執行，`f4e487c` 換掉證據時沒有同步改這一格（我的疏失）。Orchestrator 派工的範圍：只修正這一格的時間數值，不重跑量測，不處理 R1-F2、R1-F3。
- **修正**：V2-3「狀態」欄改為 committed evidence 的數值並直接引用證據檔：頁內量測 5 次，change handler Chrome 2.0～4.0 ms、Edge 2.1～6.8 ms；controller（載入＋引擎）Chrome 0.4～1.7 ms、Edge 0.4～3.7 ms；來源為 `doc/screenshots/v2-issue74/browser_check_chrome.json`、`browser_check_edge.json` 的 `checks.timing_in_page`。PASS 狀態與其他文字不變。
- **Closure 證據**：
  - 以 `git show HEAD:home_work_02/doc/screenshots/v2-issue74/browser_check_<b>.json` 讀出 `checks.timing_in_page`：Chrome 155.0.8059.85 `handler_ms` [4, 2.8, 2.1, 2.2, 2]（2.0～4.0）、`controller_ms` [1.7, 0.7, 0.4, 0.5, 0.4]（0.4～1.7）；Edge 155.0.4283.62 `handler_ms` [6.8, 2.9, 2.1, 2.1, 2.2]（2.1～6.8）、`controller_ms` [3.7, 0.9, 0.4, 0.4, 0.5]（0.4～3.7）。新數值逐一等於這些最小值與最大值，也與 §6.3 一致。
  - Diff 範圍：`git diff` 只有 `doc/acceptance/ACCEPTANCE.md` 1 行（第 151 行，V2-3），逐格比較 5 格中只有第 5 格（狀態）不同；其他條目、程式、測試、證據都沒有修改。
- **Regression**：`python -m pytest -q -rs`（主 checkout）**433 passed，0 skipped**，53.04 s（與修正前相同）。本修正只改文件，沒有重跑瀏覽器量測（依派工）。
- **Binding**：同一 assignment，agentId `addc2dc935a7822fe`；修正前核對 `('claude-opus-5-5', 'high')` 單一元素，return 前由派工者依 Bindings §3.6 全程核對。
- **未處理（依派工）**：R1-F2（排入 #76）、R1-F3（DA）。
