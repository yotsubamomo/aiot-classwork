# Audit record — #76 HW2 V2-T3，cycle 1，R2

- **Audit 種類**：Ticket independent audit，**R2（closure review）**，cycle 1（治理 §4.4）。範圍只限 R1 的 blocking finding **R1-F1**：是否真正解決、修正是否引入回歸、修正是否直接產生或暴露新的 blocking defect。不是第二次全面審查；R1-F2 與 O-1～O-3 依派工另行處理。本 record 不是 Spec Integration Audit。
- **角色**：`primary_reviewer`（definition `gov-primary-reviewer`）。
- **Run**：`run-20261022-hw2-v2-enhance`（Orchestrator＝root session `37216426-f292-44f9-bad1-e2d862e7b8f1`）。
- **Work Contract**：同 R1 record [`issue-76-c1-r1.md`](issue-76-c1-r1.md) 檔頭（GitHub #76 body sha256 `5d121dd9…b2b2`；Outcome Contract §5、§5.2 CC-V2-1；Spec V2 rev 2；Brief V2 rev 2＋E-1；DA `derivation-SPEC-V2.md`、`decision-20261022-r1f3-v1-footer.md`）。
- **受審 subject**：branch `home_work_02-v2-enhance`，HEAD **`9ac8499cef2af446bfb31e9b5421c7a0836cc2a2`**。修正的 BASE `ce97221ee69cde0cce538e11ed584caa46b5b907`（R1 record 的 commit；其 parent 為 R1 subject `a4b6c76`）。修正 commit `c4256f54a8ece52ef71aff93a719f7d8db1604b6`（只改 `assets/explore_ui.js`、`tests/test_explore_static.py`）；`9ac8499` 只改 `doc/acceptance/ACCEPTANCE.md`、`doc/governance/worklog/issue-76.md` 與新增 `doc/screenshots/v2-issue76/r1f1_*`（五個證據檔）。`git diff --name-status ce97221 9ac8499` 共 9 個路徑，全部在 `home_work_02/` 內，沒有 `doc/requirement/`。審查時 working tree 對 subject 只差 run record（record-only）。我的 R1 record 自 `ce97221` 起未被改動（`git diff --quiet ce97221 9ac8499 -- …/issue-76-c1-r1.md`）。

## 1. Assurance

### (a) Context independence（治理 §2.3；Bindings §3.7）

| Property | 滿足方式 |
| --- | --- |
| Independent context | Orchestrator 以 SendMessage 續派同一個 `gov-primary-reviewer` assignment（R1 的 agentId `ad730583783ecd443`），延續我自己的 R1 context（治理 §2.3 第 1 項、Bindings §3.7 第 1 項允許）；不繼承 Executor（agentId `acd62ed3a70012296`）的對話或推理。依規定**從磁碟重讀**修正後的檔案與 `git diff ce97221 9ac8499`；worklog §10、ACCEPTANCE V2-26 與 `r1f1_*.json` 的內容當作 Executor 主張，以我自己的測試、grep、瀏覽器重現與 Node 獨立計算核對 |
| Verifiable binding | 本 assignment：agentId `ad730583783ecd443`，`agentType` `gov-primary-reviewer`；以 Bindings §3.6 指令讀取自己的 transcript（R1＋R2 全部），寫本 record 前觀測到 `('claude-opus-5-5', 'xhigh')` 188 則，單一元素，等於有效 mapping R-PR；沒有 escalation、沒有替代。全程核對由派工者依 §3.6 在採用 return 前執行；本 record 不自證 binding |
| Autonomous access | 自行讀取 repo 與 git 歷史（不做 git 寫入）、執行 pytest、Node 測試、`offline_scan`，並以 headless Chrome／Edge（全新 scratchpad `--user-data-dir`）重做 R1 的頁面重現 |
| Self-written record | 本 record 由我以自己的 Write 工具寫入 Bindings §7 的位置；派工者只能原樣 commit |

### (b) Model diversity（Bindings §5；治理 §4.6）

| Assignment | 實際 model（transcript 觀測，我自己讀取） |
| --- | --- |
| Executor，agentId `acd62ed3a70012296`（`gov-executor`，含 correction） | `claude-opus-5-5`／`high`（262 則，單一元素） |
| Primary Reviewer（R1＋本 R2），agentId `ad730583783ecd443` | `claude-opus-5-5`／`xhigh`（188 則，單一元素） |
| Alternate Reviewer | 未派工 |

**無 model diversity**。不宣告 diversity 關係，不影響 independence 判定（Bindings §5、DA A-8）。

### Capability escalation

不提出。

## 2. R1-F1 是否真正解決

### 2.1 修正內容（重讀磁碟上的檔案與 diff）

- `assets/explore_ui.js` 第 382–385 行（`renderPredictor` 的 `update()`）：`var raw = new Map(); inputs.forEach(function (x) { raw.set(x.spec.name, x.input.value); }); var v = App.predictorView(Engine, candidate, raw);`。`predictorView`（`explore_app.js` 第 276 行）本來就以 `raw instanceof Map ? raw.get(s.name) : …` 讀取，再以 `putOwn` 傳給引擎，所以任何欄名（含 `__proto__`）的輸入值都到達 `predict()`。修正只在 V2 檔案，符合 R1 要求的第 1 點。
- 我 grep 全部 V2 頁面腳本（`assets/explore_*.js`、`assets/data/startups50.js`）的方括號寫入：以使用者欄名為鍵的一般物件寫入已為 0；其餘都是陣列索引、指標名（`cv.mean[m]`）、方法名（`methodWinners[m]`、`meta.timing_ms[method]`）或候選鍵（`testKeyOf[key]`、`test[key]`），不是資料衍生的鍵。符合 R2 核對 (b)。

### 2.2 真實頁面路徑的重現（R1 的同一套檢查）

- **方法**：`git archive 9ac8499 home_work_02/index.html home_work_02/assets` 匯出到 scratchpad，由我的 `servers.py` 在 `http://127.0.0.1:8871` 提供（第二個 origin `8872` 同 R1）；我的 `cdp76.js` 以 DevTools Protocol 驅動 headless Google Chrome 155.0.8059.85 與 Microsoft Edge 155.0.4283.62，各用全新的 scratchpad `--user-data-dir`（`prof_chrome_r2`、`prof_edge_r2`）。資料與 R1 相同：我自己的 `proto_numeric.csv`（數值 `__proto__`、`constructor`，目標 `y`）與 `proto_categorical.csv`（數值 `x`、類別 `__proto__` = base／high／low），以檔案選擇（`DOM.setFileInputFiles`）載入；在預測器**自己的** `<input>`／`<select>` 改值並觸發 `input`／`change` 事件，讀頁面顯示的點預測與 PI。
- **對照值**：Node 以同一份 CSV 位元組執行載入＋引擎，依同樣的改值順序以 `Map` 呼叫 `predictorView`，並用與頁面相同的數字格式化。
- **結果**（Chrome 與 Edge 完全相同；每一步頁面顯示＝對照值）：

| 資料 | 改值（依序） | 頁面點預測 | 頁面 PI | R1（`a4b6c76`）時頁面顯示 |
| --- | --- | --- | --- | --- |
| 數值 `__proto__` | `__proto__` = 9 | **41.18** | 40.21 ～ 42.16 | 2.24 |
| | `__proto__` = −9 | **−30.76** | −31.73 ～ −29.79 | 2.24 |
| | `constructor` = 0.9 | −26.91 | −27.9 ～ −25.93 | 6.08 |
| | `constructor` = 0.1 | −34.96 | −35.96 ～ −33.96 | −1.97 |
| 類別 `__proto__` | `__proto__` = high | **60.88** | 59.96 ～ 61.81 | 10.92 |
| | `__proto__` = low | **−39.13** | −40.05 ～ −38.21 | 10.92 |
| | `x` = 9 | −32.03 | −32.97 ～ −31.09 | 18.01 |
| | `x` = 1 | −47.88 | −48.83 ～ −46.93 | 2.16 |

  `__proto__` 每次改值，顯示都跟著改變，且等於 R1 record 第 6 節以自有屬性／`Map` 計算的正確值（41.1840、−30.7577、60.8811、−39.1290）。R1 時 `constructor`、`x` 那幾列的不同，是因為當時 `__proto__` 停在預設值。
- **Executor 的證據**：`r1f1_chrome_fixed.json`、`r1f1_edge_fixed.json`、`r1f1_chrome_before.json` 與 worklog §10 用的是 Executor 自己的資料，數值與我的不同；我只把它們當作主張，結論以上表我自己的重現為準，兩者方向一致（修正前顯示不變，修正後隨輸入改變且等於參照值）。
- **紀錄的更正**（R1 要求第 3 點）：ACCEPTANCE V2-26 改以 `c4256f5` 為核對 subject，寫明 `e405bf1` 的 R1-F2 陳述只在 Node 路徑成立、頁面路徑在修正後才成立，並引用頁面路徑證據；worklog 檔頭、§3 第 4 點、§4 D-8、§8 加上更正，§10 記錄修正。陳述與我的重現一致。
- **結論：R1-F1 已解決。**

## 3. 回歸核對

- **測試**（主 checkout，working tree＝subject）：`.venv/Scripts/python -m pytest -q -rs` → **455 passed**，0 skipped（R1 時 449；多出的 6 個是新靜態測試對 6 個 V2 腳本的參數化）。Node 直接執行：`explore_load` 15、`explore_boundary` 7、`explore_app` 12、`explore_methods` 7、`explore_custom` 16，皆 0 fail、0 skipped；`explore_contract.test.js` 對 Python 參照 18 pass（`explore_reference.py` 與 `test_node_explore.py` 自 R1 起未改，我沿用 R1 產生的參照目錄）。`python -m hw2.offline_scan` → 13 files PASS（0 findings）。
- **新增的靜態測試** `test_exploratory_files_never_assign_a_computed_key_on_a_plain_object`：只新增，不修改任何既有斷言。我以同一個 regex 對 `ce97221` 的 `explore_ui.js` 執行 → 命中 `raw[x.spec.name] =`；對 `9ac8499` → 0，所以它確實能抓到 R1-F1 這一類寫法。它是 V2 測試的延伸（designation 第 5 點允許），不是新 AC 或新 seam。
- **既有測試與不變量**：對 `d7f02d4` 的每個測試檔執行 `git diff --quiet d7f02d4 9ac8499`，唯一不同的仍只有 CC-V2-1 的 `test_dashboard_static.py`；`git diff --stat d7f02d4 9ac8499 -- assets/app.js assets/hw2core.js assets/model_data.js assets/style.css assets/vendor results hw2.ipynb` 為空（A-3 不變）；修正 diff 沒有碰到 `index.html`、引擎、載入、控制器、CSS 或 `offline_scan.py`。
- **頁面行為**（同一次 Chrome／Edge 執行的其餘步驟，結果與 R1 相同）：50 Startups、自訂資料集選取、目標改選、檔案載入、H-5 探測與全部切換階段請求 0；每次 URL 提交恰一個 GET，伺服器紀錄每個讀取都帶 `Origin`、沒有 Cookie，OPTIONS 0，302 的目標沒有被請求；CORS URL、老師範例 URL（真實網路）與檔案載入的探索 test KPI 與內建 50 Startups 相同；302／無 CORS → `network`、404 → `http_status`、PNG → `not_text`、單欄 → `NOT_CSV`、`javascript:` 拒絕且請求 0、State 目標 → `TARGET_NOT_NUMERIC`；H-5 探測檔的 markup 全部以字面文字顯示（`#explore` 內 img／svg／iframe／script／b／style 0、標題不變、`body` 顯示）；KC→50→自訂→KC 時頁尾 `block`／`none`／`none`／`block`，兩次切回 KC 的 V1 區塊與頁尾和初次載入逐字相同；localStorage／sessionStorage 0、網址不變；dialog 0、例外 0、console error 0。
- **結論：沒有回歸。**

## 4. 修正是否直接產生或暴露 blocking defect

- `Map` 只在 `update()` 內建立並傳給 `predictorView`，不寫入 DOM、不儲存、不進入結果契約；D-2（輸入只以文字寫入頁面）與請求隔離不受影響（第 3 節）。
- 新的靜態測試是以鍵運算式名稱判斷的啟發式檢查，可能在未來對正當寫法誤報，但目前全部通過、不影響任何行為；這不是 defect。
- **結論：沒有。**

## 5. Findings

R2 沒有新的 finding。R1-F1：**已解決**。R1-F2（Low，non-blocking）與 O-1～O-3 依 R1 record 第 7 節的 disposition 處理，不在本 R2 範圍。

## 6. 程序

- 兩個本機伺服器（PID 26408 與其子程序 10464）與兩個瀏覽器（Chrome PID 36904、Edge PID 25660）都是我啟動的，只以這些 PID 結束（`taskkill /T /PID`）；瀏覽器一律使用 scratchpad 的全新 `--user-data-dir`，沒有在 acceptor 的預設 profile 上啟動任何瀏覽器。結束後核對：上列 PID 都不存在，使用我的 scratchpad profile 的程序 0，埠 8871／8872 的監聽 0。
- 本 R2 只寫入本 record；沒有修改實作、測試、契約、gates 或其他紀錄，沒有 git 寫入操作。

## 7. Evidence（本 R2 執行的主要指令）

- `git log`、`git show --stat c4256f5`、`git diff --name-status／--stat ce97221 9ac8499`、`git diff ce97221 9ac8499 -- assets tests doc/acceptance doc/governance/worklog`；`git diff --quiet d7f02d4 9ac8499 -- <每個既有測試檔>`；`git diff --stat d7f02d4 9ac8499 -- <A-3 路徑>`；`git archive 9ac8499 …`（scratchpad）。
- `.venv/Scripts/python -m pytest -q -rs`（455 passed）；`node --test --test-reporter=tap tests/js/explore_{load,boundary,app,methods,custom}.test.js`；`HW2_EXPLORE_REFERENCE=<scratchpad> node --test tests/js/explore_contract.test.js`（18 pass）；`python -m hw2.offline_scan`。
- 自寫工具（scratchpad，不進 repo）：`servers.py`、`cdp76.js`（Chrome／Edge 全流程，結果 `chrome_r2.json`、`edge_r2.json`）、Node 對照計算、對 `ce97221`／`9ac8499` 的 regex 檢查。
- Binding：Bindings §3.6 指令，讀取 `agent-ad730583783ecd443`（本 assignment）與 `agent-acd62ed3a70012296`（Executor）。

VERDICT: CLOSURE
