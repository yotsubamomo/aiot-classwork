# Audit record — #74 HW2 V2-T1，cycle 1，R1

- **Audit 種類**：Ticket independent audit，**R1**，cycle 1（治理 §4.4；Bindings b5 §5 Formal）。**本 record 不是 Spec Integration Audit**（Spec V2 有五張票，DA derivation §6 已判定不適用單 Ticket fast path）。
- **角色**：`primary_reviewer`（Primary Independent Reviewer；definition `gov-primary-reviewer`）。
- **Run**：`run-20261022-hw2-v2-enhance`（Orchestrator＝root session `37216426-f292-44f9-bad1-e2d862e7b8f1`）。
- **Work Contract**：GitHub issue #74（body sha256 `49e3cc50…1441`，DA derivation §3）；Outcome Contract `doc/governance/outcome-contract.md` §5（V2 接受，基準 `d7f02d4179d2cb5c2ecf0c39a4643a6ef8287907`）與 §5.2 **CC-V2-1**；Spec V2 rev 2（`doc/spec/SPEC-V2.md`；未提到者以 Spec rev 5）；Brief V2 rev 2＋E-1、Brief V1；`CONTEXT.md`；`doc/ticket/tickets-v2.md`；DA `decisions/derivation-SPEC-V2.md`（#74：H-1～H-5；A-1～A-5、A-7～A-9；G-2；I-2、I-3、I-5；D-2；F-1）與 `decision-20261018-high-risk-categories.md`；run record §1 designation 第 4 點（經 CC-V2-1 修訂）、第 5、7 點。
- **受審 subject**：branch `home_work_02-v2-enhance`，HEAD **`f4e487caa6578a187d8833a2096d550da07916bc`**；BASE `506581aea6db04422d087c4e22c5dcf211c734e9`。實作 commit `1bd1df8c72808c807d231d20400be1d1c9d415a2`；`f4e487c` 只改 `doc/governance/worklog/issue-74.md` 與 `doc/screenshots/v2-issue74/`（`git show --name-status f4e487c` 核對）。`git diff --name-only 506581a f4e487c` 的每個路徑都在 `home_work_02/` 內，沒有 `doc/requirement/`。審查時 working tree 對 subject 只差 run record（record-only path，`git diff f4e487c --stat`），程式、資料與測試與 subject 相同。

## 1. Assurance

### (a) Context independence（治理 §2.3；Bindings §3.7）

| Property | 滿足方式 |
| --- | --- |
| Independent context | Orchestrator 以 Agent tool 派工非 fork 的 `gov-primary-reviewer` subagent，從空白 context 開始，不繼承 Executor（agentId `addc2dc935a7822fe`）的對話或推理。派工內容是路徑、識別與 SHA；其中的陳述（例如「`f4e487c` 只加紀錄與證據」）我當成待驗證主張並自行核對。Worklog、ACCEPTANCE 與 evidence JSON 的內容一律當作 Executor 主張，以原始檔案、git 歷史、自己執行的測試與自己的瀏覽器檢查驗證 |
| Verifiable binding | 本 assignment：agentId `a940e0242c7bf7572`，`agentType` `gov-primary-reviewer`；以 Bindings §3.6 指令讀取自己的 transcript，寫本 record 前觀測到 `('claude-opus-5-5', 'xhigh')` 191 則，單一元素，等於有效 mapping R-PR（Opus 5.5／`xhigh`）；沒有 escalation、沒有替代。全程核對（含之後的訊息）由派工者依 §3.6 在採用 return 前執行；本 record 不自證 binding |
| Autonomous access | 自行讀取 repo、`git log／show／diff／archive`（不做 git 寫入）、GitHub API（issue、上游 repo 的授權與 blob）；自行執行 pytest、Node 測試、Python 獨立重算、mutation 檢查與 headless Chrome／Edge 檢查；scratchpad 的檔案只是我的工具，不進 repo |
| Self-written record | 本 record 由我以自己的 Write 工具寫入 Bindings §7 的位置；派工者只能原樣 commit |

### (b) Model diversity（Bindings §5；治理 §4.6 V22-17）

| Assignment | 實際 model（transcript 觀測） |
| --- | --- |
| Executor，agentId `addc2dc935a7822fe`（`gov-executor`） | `claude-opus-5-5`／`high`（197 則，單一元素；我自己以 §3.6 指令讀取） |
| Primary Reviewer（本 R1），agentId `a940e0242c7bf7572` | `claude-opus-5-5`／`xhigh` |
| Alternate Reviewer | 尚未派工 |

**無 model diversity**（Executor 與 Primary 同為 `claude-opus-5-5`）。依 Bindings §5 與 DA A-8，不宣告 diversity 關係，不影響 independence 判定。

### Capability escalation

不提出。

## 2. CC-V2-1 的核對（H-2；Outcome Contract §5.2）

- `git diff 506581a f4e487c -- home_work_02/tests/test_dashboard_static.py`：只有 `test_page_loads_data_as_a_js_global_and_the_bundled_chartjs` 的 `assert scripts == [...]` 一條斷言改變（1 行刪除、3 行新增）。新清單前四項仍是 `assets/vendor/chart.umd.js`、`assets/model_data.js`、`assets/hw2core.js`、`assets/app.js`，順序不變，其後**逐一列出**六個 V2 腳本（`assets/data/startups50.js`、`explore_load.js`、`explore_engine.js`、`explore_plot.js`、`explore_app.js`、`explore_ui.js`），以清單等號比對，比修改前更嚴格。同一測試的其他兩條斷言（檔案存在、`lang="zh-Hant-TW"`）不變。
- 規避檢查：`index.html` 共 10 個 `<script`，全部是 `<script src="…">` 形式，沒有 inline script、沒有屬性重排或執行期注入的腳本（`grep -n "<script" index.html`）；斷言看到全部腳本。
- 其他既有測試逐位元不變：對 `git ls-tree -r d7f02d4 -- tests` 的每個檔案執行 `git diff --quiet d7f02d4 f4e487c`，唯一不同的是 `tests/test_dashboard_static.py`（就是上述那一條）。`d7f02d4..506581a` 只改 `doc/governance/`。
- **結論：符合 CC-V2-1。**

## 3. 高風險類別（DA A-1；derivation §7.4：#74 觸及 H-1～H-5）

### H-1 憑證、機密與不得公開的資料（A-4）

- 實際學號：從未追蹤的本機打包設定讀取比對值（不印出），`git grep -F` 於 `f4e487c` 與 `1bd1df8` 命中 0；`506581a..f4e487c` 的 commit message 命中 0；worklog、兩份 evidence JSON、ACCEPTANCE 命中 0。**已核對、無命中。**
- 追蹤檔案：subject 新增或修改的路徑沒有 `.pdf`、`.zip`、`.env`、`kaggle`、`acceptor_materials`、`.local`；`git ls-tree f4e487c` 中唯一的 `.pdf` 是 `doc/requirement/` 的老師文件（`b22e226` 加入，早於本票）。
- 使用者 URL 與資料：subject 新增內容中的 URL 只有老師公開的範例 URL（`50_Startups.SOURCE.md` 與 `tests/test_explore_static.py`）。Evidence JSON 不含本機路徑或使用者名稱（已去除，`<clean-clone>` 佔位）。本票沒有任何 `fetch`、沒有金鑰。
- **結果：PASS。**

### H-2 老師指定的名稱與格式（含 +1）

- +1 下拉：三項依序（`king_county`／`startups50`／`custom`），預設 King County，有 `<label for>`；我自己的 headless Chrome 155 與 Edge 155 檢查（`file://`、斷網：DevTools offline＋host resolver 全部 NOTFOUND＋無效 proxy）：Tab 第 7 下到達下拉、outline `solid 3px`、ArrowDown 切到 50 Startups（OV-4）。
- OV-1 的保持：King County 與 50 Startups 的載入與全部切換，非 `file:` 請求 0（兩個瀏覽器）。`python -m hw2.offline_scan`：13 個檔案（含全部 V2 `.js`／`.css`）PASS、0 findings；本票沒有 `offline_scan` 例外（屬 #76）。
- CC-V2-1：見第 2 節。
- **結果：PASS。**

### H-3 評估完整性（A-2、A-3）

- **A-3（正式分析不變）**：以 `git show f4e487c:<path> | sha256sum` 重算：`assets/app.js` `c1ab3f21…82ad`、`assets/hw2core.js` `e75c5d48…2c14`、`assets/model_data.js` `6cf0c11e…a7ac`、`results/model_data.json` `69dc1465…6e61`，全部等於 DA 值且等於 `d7f02d4`；`assets/style.css` 也不變。`git diff d7f02d4 f4e487c -- results hw2.ipynb assets/vendor data …` 為空。`hw2/` 只**新增** `hw2/explore_reference.py`，既有模組無修改；Test evaluation 紀錄（`fe76019b…`／`b53ff286…`）所在的 `results/` 與 notebook 無 diff。探索檔案不含 `MODEL_DATA`、`model_data`、`test_inputs`、`HW2Core`（自行讀碼，並有 `test_explore_static.py`）。
- **`hw2/explore_reference.py` 的判定**（A-3 要求 Reviewer 判定）：它是 Spec「通用 Python 參照」與 #74 授權的新模組；`hw2/__init__.py`、其他 `hw2/*.py`、`hw2.ipynb` 都不 import 它（grep），只有 `tests/test_node_explore.py` 使用；它只 import `hw2.ols`、`hw2.metrics`（group-generic 的 `fit_ols`、`design`、`log_interval` 的公式、`usd_metrics`、`coverage_stats`），不讀 `model_data`、不依賴 JS。**判定：不在正式分析路徑上，符合 designation 第 4 點。**（它會隨 `hw2/` 進入 #78 重打包的 ZIP，見觀察 O-1。）
- **A-2（自己執行測試）**：
  - 主 checkout（working tree＝subject）：`.venv/Scripts/python -m pytest -q -rs` → **433 passed，0 skipped**（Python 3.11.2，Node v24.19.0）。
  - Node 直接執行：`explore_load` 15/15、`explore_boundary` 7/7、`explore_app` 9/9，各 skipped 0；我以 `tests/test_node_explore.py::write_reference` 自行產生參照到 scratchpad 後執行 `explore_contract.test.js` → 13/13，skipped 0（PRNG、11 段載入對照、9 個 case、A-1、內嵌文字）。V1 的 `tests/test_node_core.py`（驅動 `core.test.js`）與 V2 測試模組一起執行 → 62 passed。
  - 以 `git archive` 匯出 subject 與 BASE 到 scratchpad（非 git 目錄）再跑：BASE 379 passed／16 failed／3 skipped（共 398），subject 411 passed／17 failed／5 skipped（共 433）；兩邊的 failed 全是需要 git checkout 的測試（`test_repo_hygiene`、`test_package`，subject 多一項 `git check-attr`），skipped 是需要 git 歷史或作者未追蹤材料者。結論：新增 35 項，非 git 依賴的測試在乾淨匯出上全部通過，不依賴本機未追蹤檔案。
  - **獨立重算**（不用 `hw2` 與引擎）：自寫 mulberry32＋Fisher–Yates 重現 50 Startups 的切分與 fold（與引擎相同），以 `numpy.linalg.lstsq`、`np.linalg.inv`、`scipy.stats.t` 重算五個 fold 的指標、CV 平均與樣本標準差、canonical fit、t 臨界值，以及 winner（All-in）在 10 筆 test 上的逐筆 predicted／lower／upper、covered、coverage 與 test 指標。與 JS 引擎的最大相對差：CV 3.3e-10、係數 2.1e-9、s² 3.3e-16、t 1.5e-15、逐筆 PI 7.3e-11、test 指標 7.6e-11；covered 逐筆相同；基準層級 New York（訓練列最先出現）。
  - **Verify-the-verification（mutation，在 scratchpad 的副本上，原檔未動）**：(M1) 第二層改看全部列 → boundary 5 項、contract 7 項失敗；(M2) fold 編碼看驗證列 → boundary 2 項失敗；(M3) canonical fit 含 test 列 → boundary 1、contract 7 項失敗；(M4) CV std 改 ddof 0 → contract 5 項失敗；(M6) df_resid 門檻改 2 → contract 9 項失敗；(M7) PI 去掉「1 +」→ app 1、contract 6 項失敗。(M5) covered 改為嚴格不等式加 0.1% 邊界 → 在 fixture 上與原規則等價（沒有落在該窄帶的點），由與引擎無關的 covered 不變量檢查涵蓋，不是缺口。
  - 三層邊界（SR-V2-01）、winner 固定後才讀 test、test 只對 winner、PI 公式、A-1：讀碼確認（`explore_engine.js` `run()`：`trainDecisions(load, split.train)` → `evaluateCandidate` 只用 `split.train` → winners → `evaluateTest`），並由上列測試與 mutation 佐證。
  - README 與報告：`git diff d7f02d4 f4e487c -- README.md report/` 為空，沒有探索數字進入。
- **結果：PASS**；另有 R1-F2（Medium，non-blocking，任意欄名的健壯性，見第 6 節）。

### H-4 證據真實性與如實標示（A-5）

- 50 Startups：`git show f4e487c:home_work_02/assets/data/50_Startups.csv | sha256sum` → `c6075ca5a7551243b31193bad9228f0a1b9468cdde2475c6586c56dcfac5630d`，2,436 bytes，blob `14ffb860…6439`；內嵌於 `startups50.js` 的文字以 UTF-8 計算 sha256 相同、`bytes` 相同；`.gitattributes` 的 `assets/data/** -text`。上游以 `gh api` 重查：`repos/Avik-Jain/100-Days-Of-ML-Code/license` → `MIT`、`LICENSE` blob `00542313…1961`；`contents/datasets/50_Startups.csv` 的 blob `14ffb860…6439`、size 2436（與本地 blob 相同）；最後修改該檔的 commit `5cd8936a…a74`（2018-07-10）。`50_Startups.LICENSE.md` 的 MIT 原文與上游 `LICENSE` 去除行尾空白與 CR 後逐行相同；陳述只寫可查證的事實（I-3）。
- 截圖與 evidence JSON：環境標示（headless、`file://`、乾淨 sparse clone、斷網方式）寫在 JSON 的 `note` 與 worklog §6.3；我讀過四張截圖，與描述相符、無缺字方塊。
- ACCEPTANCE G 節 V2-1～V2-9：逐條與 committed evidence JSON 對照。V2-1、V2-2、V2-4～V2-9 的狀態與數值都有對應證據，PENDING／NOT TESTED 標示如實。**V2-3 的執行時間數值與其引用的證據不符 → R1-F1。**
- **結果：FAIL（R1-F1）。**

### H-5 使用者提供的資料來源與網路請求邊界（A-9）

- 我自己列舉六個 V2 腳本中 A-9 所列 API（`innerHTML`、`outerHTML`、`insertAdjacentHTML`、`document.write`、`DOMParser`、`createContextualFragment`、`srcdoc`、`eval`、`Function`、字串型 `setTimeout`／`setInterval`、`import(`、`Worker`、`importScripts`、`fetch`、`XMLHttpRequest`、`WebSocket`、`EventSource`、`sendBeacon`、`.src`／`.href`／`location`、`window.open`、storage、cookie、`postMessage`）：程式碼中**零**出現（唯一命中是 `explore_app.js:13` 的註解文字）。
- DOM 寫入點：`explore_ui.js` 只用 `textContent`、`createTextNode`、`<option>.value`／`.text`、`className`，以及 `el()` 的 `setAttribute`（呼叫者只傳固定鍵 `scope`、`for`、`id`、`type`、`step`、`inputmode`，值不來自資料）；`explore_plot.js` 用 canvas `fillText` 與 tooltip 的 `textContent`，`style` 只寫數值座標。符合 D-2。
- `fetch`：本票沒有任何網路路徑；`offline_scan` 例外屬 #76，本票未新增例外。
- Mock fetch：`explore_app.test.js` 的請求隔離前四條與 vm 載入測試，我自己執行通過（見 H-3）。
- **瀏覽器探測**（R1 證據）：把 subject 的 `index.html` 與 `assets/` 複製到 scratchpad，將內嵌資料換成刻意構造的 CSV（欄名 `<img src=x onerror="document.title='pwned'">`、`</script><b>bold</b>`、`javascript:alert(1)`、`<script>alert(2)</script>`（目標欄）；類別值 `<svg onload=alert(1)>`、`"><iframe src=//evil.example>`、`a&amp;b`、`<style>body{display:none}</style>`），headless Chrome 155、`file://`、斷網、選 50 Startups：`run = COMPLETED`；欄位表、預測器 label 與下拉選項全部以字面文字顯示；`#explore` 內 `img／svg／iframe／script／b／style` 元素 0；`document.title` 不變；`body` 仍顯示；dialog 0、例外 0、console error 0、非 `file:` 請求 0；切回 King County 後五個 V1 區塊的 `innerText` 與切換前逐字相同。
- **結果：PASS**（R1-F2 的健壯性問題不涉及 markup 或請求，只會讓特定欄名的探索結果出錯或預測器失效，見第 6 節）。

## 4. AC 逐條核對（#74）

| AC | 結果 | 證據（本 R1 自行取得） |
| --- | --- | --- |
| 下拉與 King County 不變（靜態 seam）：三項依序、鍵盤可操作；V1 區塊結構快照；`model_data`、V1 腳本與核心模組 sha256 不變；既有全部 pytest 與 Node 測試通過 | PASS | 第 2、3 節；`test_the_snapshot_is_the_accepted_baseline_page` 以 `git show d7f02d4:home_work_02/index.html` 重導快照並通過；433 passed（既有 398 項全在內，`core.test.js` 經 pytest skipped 0） |
| 內建資料（靜態 seam）：內嵌文字＝`.csv`、sha256＝記錄值；沒有任何 `fetch(` | PASS | H-4 節的 sha256 重算；A-9 列舉 |
| 載入契約（次 seam）：八個拒絕原因各有案例；BOM、引號、空白、科學記號、負數、空儲存格；`LoadResult` 不含保留／排除狀態 | PASS（另見 R1-F2 的 `__proto__` 重複欄名） | `explore_load.test.js` 15/15（逐一讀過案例）；Python／JS 的 11 段載入對照 |
| 三層邊界（次 seam）：20／21 層級以訓練列計；只在 test 列變化／常數的欄；改 test 列不改 group、canonical、fit、預測器層級；fold 驗證列與訓練列 | PASS | `explore_boundary.test.js` 7/7；mutation M1–M3 |
| All-in 結果契約（主 seam，Node 對 Python 參照，1e-6）與契約不變量 | PASS | contract 13/13；我獨立重算的 50 Startups（第 3 節 H-3） |
| A-1 有效性：某 fold 秩不足 → `INVALID_MODEL` 附原因與 fold；全部無效 → `REJECTED`／`ALL_CANDIDATES_INVALID`；df_resid < 3 | PASS | `a1_fold_rank_deficient`（fold 2、`rank_deficient`）、`a1_small_df`、`a1_collinear`、`a1_no_groups` |
| 即時預測器：只對 `VALID`；中位數預設；超範圍警告仍計算；類別只列訓練層級加基準、未見層級以基準計算並警告；非 `VALID` 停用並顯示狀態與原因 | PASS（50 Startups；另見 R1-F2） | `explore_app.test.js`；我的瀏覽器檢查：4 個輸入、State 下拉「New York（基準）、California、Florida」、R&D Spend＝9,999,999 仍給出點預測並顯示一則超範圍警告 |
| 請求隔離前四條（mock fetch） | PASS | `explore_app.test.js` 的前三項測試；瀏覽器非 `file:` 請求 0 |
| 人工檢查表（ACCEPTANCE V2） | **FAIL（R1-F1）**：V2-3 的時間數值與證據不符；其餘條目與證據相符 | 第 3 節 H-4 |
| UI 一致性：zh-TW 無缺字；OV-2 375／768 px 無水平溢出；OV-5 對比 | PASS | 我的 Chrome／Edge：三種狀態 × 375／768 px 溢出皆 0；我的對比計算（50 Startups 狀態，下拉列＋`#explore` 可見文字 172 處）最低 6.74:1、0 處低於門檻；涵蓋以圓點／方塊區分；截圖目視無缺字。真實觸控、螢幕閱讀器 NOT TESTED（AD-1） |

其他行為（Spec「Problem 與頁面結構」）：選 50 Startups 每次重跑、切回 King County 結果留在記憶體不顯示（`explore_app.test.js`）；自訂資料集只顯示佔位區塊、輸入控制項 0（瀏覽器）；探索時頁內導覽隱藏、切回後恢復；V1 散佈圖切回後重新繪製（非白像素 > 0）；`getElementById` 是 V1 唯一的取元素方式，V2 id 一律 `ex-`，全頁沒有重複 id。

## 5. DA 對 #74 的票義務與 run invariants

| 項目 | 結果 |
| --- | --- |
| F-1 → CC-V2-1 | 符合（第 2 節） |
| G-2 主 seam (d)：恰好 20 列、單一類別欄、全部數值 | 有：`edge_twenty_rows`、`edge_single_categorical`、`edge_all_numeric`，Node 對 Python 通過 |
| I-2 單檔例外與來源 URL 位置 | 本票沒有任何例外；V2 頁面檔案沒有寫死 URL；來源 URL 只在掃描範圍外的 `50_Startups.SOURCE.md` |
| I-3 授權與換行 | 符合（H-4 節） |
| I-5 既有測試不變、區段切片測試不修改即成立 | 符合（第 2 節；`test_dashboard_static.py` 其他測試未改且通過） |
| D-2 | 符合（H-5 節） |
| designation 第 4 點（經 CC-V2-1） | 符合：notebook、`results/`、`model_data`、V1 腳本與核心模組、`style.css` 無 diff；既有 `hw2/` 模組無修改；V1 Spec／tickets／Brief 無 diff；沒有重跑 notebook 或新的 Test evaluation |
| designation 第 5 點 | 符合：沒有新增 CI、E2E 框架、`package.json` 或依賴（`requirements.txt` 無 diff）；Node 測試只用 `node:test`／`node:vm` |
| designation 第 7 點 | 符合：50 Startups 已取得並記錄 sha256；學號見 H-1 |
| Git 規則 | `506581a..f4e487c` 兩個 commit 的 message 依 `[Modify] –` 格式，沒有 Claude 標記；未 push |

## 6. Findings

### R1-F1 — ACCEPTANCE V2-3 的執行時間數值沒有證據支持

- **Severity**：Medium。**Blocking**：**是**。
- **證據**：
  - `doc/acceptance/ACCEPTANCE.md` 第 151 行（V2-3，`1bd1df8` 加入、`f4e487c` 未改）：狀態欄寫「頁內量測 change handler 2.1～5.2 ms、引擎 0.4～2.5 ms，`doc/governance/worklog/issue-74.md` §6」。
  - 它引用的 worklog §6.3 第 102 行寫「change handler … Chrome 2.0～4.0 ms、Edge 2.1～6.8 ms；controller（載入＋引擎）Chrome 0.4～1.7 ms、Edge 0.4～3.7 ms」。
  - committed evidence `doc/screenshots/v2-issue74/browser_check_chrome.json` 的 `checks.timing_in_page`：`handler_ms` 4、2.8、2.1、2.2、2；`controller_ms` 1.7、0.7、0.4、0.5、0.4。`browser_check_edge.json`：`handler_ms` 6.8、2.9、2.1、2.1、2.2；`controller_ms` 3.7、0.9、0.4、0.4、0.5。兩份 JSON 支持 worklog 的數值，不支持 ACCEPTANCE 的「2.1～5.2」「0.4～2.5」（Edge 的 6.8 ms 與 3.7 ms 都超出 ACCEPTANCE 所寫的範圍，Chrome 的 2.0 ms 低於下限）。這些值看來來自 `f4e487c` 換掉的較早一次執行，該次執行的證據已不在 subject 中。
  - 其他 V2 條目（V2-1 的 Tab 第 7 下與 3px outline、V2-2 的逐字相同、V2-8 的溢出 0 與 6.74:1、V2-9 的輸入 0 等）與 JSON 相符。
- **依據的契約條款**：#74 AC「人工檢查表（ACCEPTANCE V2）：… 記錄執行時間，不設門檻」與結案證據「本票 AC 對應的 ACCEPTANCE.md 條目…已填且附證據位置」；DA derivation §7.2 H-4（涵蓋「執行時間…的實測紀錄」）與 §7.3 **A-5（V2）**「ACCEPTANCE 狀態與證據逐條相符」；`decision-20261018-high-risk-categories.md` H-4（沒有證據的量測值）。
- **Blocking 的理由**：PASS 狀態本身成立（時間不設門檻），但同一格記錄的實測值與它引用的證據矛盾，而且它屬於 DA 宣告的高風險類別 H-4，並違反該類別的具體 assurance 要求 A-5。ACCEPTANCE 是 #78 彙整、Spec Integration Audit 核對的驗收帳本，數值錯誤會往下傳。修正範圍很小、可驗證。
- **要求的 targeted correction**：只修改 V2-3 的時間數值，使它與 subject 中的 committed evidence 一致（或改引用確實支持其數值、且已 commit 的證據）。不需重跑瀏覽器，也不得改動其他條目、程式或測試。R2 核對：V2-3 的數值逐一對應 evidence JSON，且 diff 只限該格。

### R1-F2 — 以使用者欄名當作一般物件的鍵：特定欄名讓預測器失效、契約輸出遺失，`__proto__` 重複欄名繞過 `DUPLICATE_COLUMN`

- **Severity**：Medium。**Blocking**：**否**。
- **證據**（我在 Node 以 subject 的檔案重現；腳本在 scratchpad，未進 repo）：
  - `assets/explore_engine.js` 第 525 行 `var lv = fit.levels[name]`：`fit.levels` 是一般物件（第 350 行 `levelsOf`），數值欄名若是 `Object.prototype` 的成員（`constructor`、`toString`、`valueOf`、`hasOwnProperty`…），會讀到繼承來的函式而被當成類別欄，`lv.levels.slice()` 拋出 `TypeError`。實測：數值欄 `constructor` 或 `toString` 的資料 `run = COMPLETED`，但 `inputSpec` 與 `predictorView` 都拋出 `Cannot read properties of undefined (reading 'slice')`。在頁面上，`render()` 會在 `renderPredictor` 中斷，預測器沒有輸入，探索 test 區塊沒有繪製。
  - 類別欄名 `__proto__`：`levelsOf` 的 `out['__proto__'] = …` 改的是原型而不是自有屬性，結果契約的 `fit.levels` 序列化為 `{}`，Python 參照有該鍵，兩者分歧。第 152 行的 `unseenByGroup[g.name]`、第 361 行的 `inputsOf` 也有同類問題。
  - `assets/explore_load.js` 第 221–227 行：`seen` 是一般物件，`seen['__proto__'] = c` 不會成為自有屬性，因此表頭 `__proto__,__proto__,y` 被 JS 接受（`ok: true`），而 `hw2/explore_reference.py` 回傳 `DUPLICATE_COLUMN`。這違反 Spec「載入契約」的「重複的欄名：拒絕 `DUPLICATE_COLUMN`」，也是 Node／Python 的分歧。
  - 不會造成全域原型污染或任何 markup／請求（只改區域物件的原型，或賦值被忽略）；H-5 探測與 A-9 列舉不受影響。
- **依據**：Spec V2「載入契約」（重複欄名拒絕）、「通用 Python 參照」（同一規則）、「即時預測器」；Brief V2 §3.1「可任意輸入 Dataset」；DA D-2 的理由（不變量必須對任意輸入成立）；H-3(ii)。
- **Non-blocking 的理由**：在 #74 的 operating scope 內，頁面只能載入內建的 50 Startups（欄名不觸發），自訂資料集只有佔位、不接受輸入，所以本票的使用者路徑上沒有實現條件。#76 開放 URL／檔案輸入後，這些欄名就能由使用者送入。
- **Disposition**：見第 7 節。

### R1-F3 — 探索模式下仍顯示 V1 頁尾；其文字與 V2 的隔離覆寫之間有契約語義的空白（routing signal）

- **Severity**：Low。**Blocking**：否（契約語義不足，依治理 §4.2 是 routing signal，不是對實作的 blocking finding）。
- **證據**：`index.html` 第 375 行的 V1 頁尾「本頁讀取主程式 `hw2.ipynb` 匯出的 `model_data`；所有資料與程式庫都在本機，不發出任何對外請求。…」。`explore_ui.js` 第 17 行只隱藏五個 V1 section，探索時頁尾仍顯示（截圖 `chrome_startups50_1280_full.png`、`chrome_custom_1280.png` 底部）。`tests/test_explore_static.py` 第 110 行把頁尾列為 V1 區塊並以快照鎖定文字。
- **具體的 ambiguity**：Spec V2「選 50 Startups 或自訂資料集：隱藏 V1 區塊」（SPEC-V2.md 第 95 行）沒有說頁尾是否屬於要隱藏的「V1 區塊」，也沒有說它可否改字。在 #74 它仍然屬實（沒有任何請求）。#76 加入使用者提交的一次 GET 後，「不發出任何對外請求」在自訂 URL 模式下就不成立；而 V1 文字不變的不變量（快照與 designation 第 4 點）使它不能改字。是否在探索模式隱藏頁尾、或依 Brief V2 §3.5 覆寫 2 處理其文字，需要 Design Authority 裁決，最好在 #76 實作前。
- **Required authority**：Design Authority（本 R1 不裁決）。

### 觀察（不是 finding）

- **O-1**：`hw2/explore_reference.py` 與 `assets/data/50_Startups.SOURCE.md`／`LICENSE.md` 會經 `hw2/package.py` 的 `git ls-files … hw2 … assets` 進入 #78 重打包的 ZIP。前者只供測試，後者使 ZIP 內的副本保有 MIT 聲明（I-3）。供 #78 與 Spec Integration Audit 知悉。
- **O-2**：自訂資料集佔位文字「由 V2-T3 提供」是開發中的暫時用語，#76 會替換（Executor 已記）。

## 7. Non-blocking findings 的 disposition

| Finding | Disposition | Owner |
| --- | --- | --- |
| R1-F2 | 需要修正，屬已接受契約內的 rework（Spec 載入契約與任意輸入），不需新授權；不延長本 cycle，也不併入 R1-F1 的 targeted correction（治理 §4.4）。建議在 #76（自訂資料集讓任意欄名可由使用者送入的那張票）由 Executor 修正：以 `Map`、`Object.create(null)` 或自有屬性檢查取代一般物件鍵，並新增 Node 與 Python 的對照案例（數值欄 `constructor`、類別欄 `__proto__`、重複 `__proto__` 表頭）；修正須在 #76 結案前完成，由 #76 R1（H-3、H-5）與 Spec Integration Audit 核對 | Orchestrator（排入 #76 的派工並追蹤） |
| R1-F3 | Route 至 Design Authority，取得頁尾在探索模式的處理與其文字是否可改的裁決（應在 #76 實作前）；本 R1 不作設計決定 | Orchestrator（派工 DA）；裁決 authority＝Design Authority |
| O-1、O-2 | 僅供後續票與 Spec Integration Audit 知悉，無需處理 | — |

## 8. Routing

- **Design Authority**：R1-F3（契約語義：V1 頁尾在探索模式是否隱藏、文字可否依 Brief V2 §3.5 覆寫 2 調整）。
- **Executor（targeted correction）**：R1-F1，經 Orchestrator 派工；之後由 R2 核對。
- 沒有需要 acceptor 或 Final Adjudicator 的事項。

## 9. Evidence（本 R1 執行的主要指令）

- `git log`／`show --stat`／`show --name-status`／`diff --name-status`／`diff --stat`（`d7f02d4`、`506581a`、`1bd1df8`、`f4e487c`）；`git ls-tree -r`；`git show <rev>:<path> | sha256sum`；`git rev-parse f4e487c:home_work_02/assets/data/50_Startups.csv`；`git archive f4e487c|506581a home_work_02 | tar -x`（scratchpad；不寫 git）。
- `gh issue view 74`；`gh api repos/Avik-Jain/100-Days-Of-ML-Code/license`、`…/contents/datasets/50_Startups.csv`、`…/commits?path=datasets/50_Startups.csv`。
- `.venv/Scripts/python -m pytest -q -rs`（主 checkout 與兩份匯出）；`node --test --test-reporter=tap tests/js/explore_{load,boundary,app}.test.js`；`HW2_EXPLORE_REFERENCE=<scratchpad> node --test tests/js/explore_contract.test.js`；`python -m hw2.offline_scan` 與 `dashboard_files()` 清單。
- 自寫工具（scratchpad，不進 repo）：獨立重算（numpy／scipy）、mutation 副本、`__proto__`／`constructor` 探測、Chrome／Edge DevTools Protocol 檢查（下拉、鍵盤、50 Startups 內容、預測器超範圍、自訂佔位、切回 King County 逐字比較、375／768 px 溢出、請求、例外、dialog）、H-5 構造 CSV 探測、OV-5 對比計算。
- Binding：Bindings §3.6 指令，對 session `37216426-…` 的 `subagents/` 讀取 `agent-a940e0242c7bf7572`（本 assignment）與 `agent-addc2dc935a7822fe`（Executor）。
- 本 R1 只寫入本 record；沒有修改實作、測試、契約、gates 或其他紀錄，沒有 git 寫入操作。

VERDICT: BLOCKING (R1-F1)
