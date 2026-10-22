# Audit record — #75 HW2 V2-T2，cycle 1，R1

- **Audit 種類**：Ticket independent audit，**R1**，cycle 1（治理 §4.4；Bindings b5 §5 Formal）。**本 record 不是 Spec Integration Audit**（Spec V2 有五張票，DA derivation §6 判定不適用單 Ticket fast path）。
- **角色**：`primary_reviewer`（Primary Independent Reviewer；definition `gov-primary-reviewer`）。
- **Run**：`run-20261022-hw2-v2-enhance`（Orchestrator＝root session `37216426-f292-44f9-bad1-e2d862e7b8f1`）。
- **Work Contract**：GitHub issue #75（body sha256 `834a439c0408940b8116bbb3b46077694e3844a282ed97c08e78dc71823aadd5`，我以 `gh issue view 75 --json body -q .body | sha256sum` 重算，等於 DA derivation §3 的 accepted 版本；issue 從未編輯）；Outcome Contract `doc/governance/outcome-contract.md` §5（V2 接受，基準 `d7f02d4179d2cb5c2ecf0c39a4643a6ef8287907`）與 §5.2 **CC-V2-1**；Spec V2 rev 2（`doc/spec/SPEC-V2.md`，sha256 `695161db…f9a5`，與 `d7f02d4` 相同；未提到者以 Spec rev 5）；Brief V2 rev 2＋E-1（§12 A-1～A-3；sha256 `27f08b25…3b38`）、Brief V1；`CONTEXT.md`；`doc/ticket/tickets-v2.md`（sha256 `f1e6b1a6…aa4`）；DA `decisions/derivation-SPEC-V2.md`（#75：H-1～H-5；A-1～A-5、A-7～A-9；G-1、G-2；D-2；I-5）；`decision-20261022-r1f3-v1-footer.md`（分配給 #76／#78，非 #75）；run record §1 designation 第 4、5、7 點（經 CC-V2-1）。`d7f02d4..HEAD` 對 `doc/spec`、`doc/brief`、`doc/ticket`、`doc/requirement`、`CONTEXT.md` 無 diff。
- **受審 subject**：branch `home_work_02-v2-enhance`，HEAD **`ded276929d45727cbc164ec53865d6ff04cba963`**；BASE `3dfba2d9ebf2e4589845b06021693636d7156d27`。實作 commit `2069feacdd73968044a83d69dc37bc894dfd8cad`（13 個檔案，程式與測試）；`ded2769` 只改 `doc/acceptance/ACCEPTANCE.md`、`doc/governance/worklog/issue-75.md` 與 `doc/screenshots/v2-issue75/`（`git show --stat` 核對）。`git diff --name-only 3dfba2d ded2769` 每個路徑都在 `home_work_02/` 內，沒有 `doc/requirement/`。審查時 working tree 對 subject 只差 run record（record-only path，`git diff --stat ded2769`），程式、資料、測試與 subject 相同。未 push（沒有 remote branch 含 `ded2769`）。

## 1. Assurance

### (a) Context independence（治理 §2.3；Bindings §3.7）

| Property | 滿足方式 |
| --- | --- |
| Independent context | Orchestrator 以 Agent tool 派工非 fork 的 `gov-primary-reviewer` subagent，從空白 context 開始，不繼承 Executor（agentId `a5dedd102dd077202`）的對話或推理，也不延續 #74 Reviewer（`a940e0242c7bf7572`）的 context。派工內容只有路徑、識別與 SHA；其中與 worklog、ACCEPTANCE、evidence JSON 的陳述我一律當作待驗證主張，以原始檔案、git 歷史、自己執行的測試、獨立重算、mutation 與自己的瀏覽器檢查驗證 |
| Verifiable binding | 本 assignment：agentId `a9a75e1af80e98547`，`agentType` `gov-primary-reviewer`；以 Bindings §3.6 指令讀取自己的 transcript，寫本 record 前觀測到 `('claude-opus-5-5', 'xhigh')` 172 則，單一元素，等於有效 mapping R-PR（Opus 5.5／`xhigh`）；沒有 escalation、沒有替代。全程核對（含之後的訊息）由派工者依 §3.6 在採用 return 前執行；本 record 不自證 binding |
| Autonomous access | 自行讀取 repo、`git log／show／diff／archive／grep`（不做 git 寫入）、GitHub issue；自行執行 pytest、Node 測試、`offline_scan`、numpy／scipy 獨立重算、12 項 mutation（在 scratchpad 的匯出副本上）、Lasso 邊界探測，以及 headless Chrome 155／Edge 155 的 DevTools Protocol 檢查與 H-5 探測。Scratchpad 的檔案只是我的工具，不進 repo |
| Self-written record | 本 record 由我以自己的 Write 工具寫入 Bindings §7 的位置；派工者只能原樣 commit |

### (b) Model diversity（Bindings §5；治理 §4.6 V22-17）

| Assignment | 實際 model（transcript 觀測，Bindings §3.6 指令，我自行讀取） |
| --- | --- |
| Executor，agentId `a5dedd102dd077202`（`gov-executor`） | `claude-opus-5-5`／`high`（296 則，單一元素） |
| Primary Reviewer（本 R1），agentId `a9a75e1af80e98547` | `claude-opus-5-5`／`xhigh`（172 則，單一元素） |
| Alternate Reviewer | 尚未派工 |

**無 model diversity**（Executor 與 Primary 同為 `claude-opus-5-5`）。依 Bindings §5 與 DA A-8，不宣告 diversity 關係，不影響 independence 判定。

### Capability escalation

不提出。

## 2. 高風險類別（DA A-1；derivation §7.4：#75 觸及 H-1～H-5）

### H-1 憑證、機密與不得公開的資料（A-4）

- 實際學號：從未追蹤（`git check-ignore` 確認）的 `.local/packaging.json` 讀取比對值（不印出）：`git grep -F` 於 `ded2769` 命中 0；`3dfba2d..ded2769` 的 commit message 命中 0；該範圍的 diff 命中 0。
- `3dfba2d..ded2769` 沒有新增或修改 `.pdf`、`.zip`、`.env`、`kaggle`、`acceptor_materials`、`.local` 路徑；diff 中沒有任何 `http(s)://` URL；evidence JSON、worklog、ACCEPTANCE 的新增內容沒有本機路徑或使用者名稱。本票沒有 `fetch`、沒有金鑰。
- **結果：PASS。**

### H-2 老師指定的名稱與格式（含 +1 與 OV-1 的保持）

- 下拉、King County 區塊與 `<script src>` 清單：本票沒有改動（`index.html` 的 diff 只在 `#explore` 子樹內：`ex-data` 加共線診斷、`ex-model` 改寫、`ex-predictor` 一個 `id`、`ex-test` 一個提示段、新增 `ex-methods`；`<script src>` 仍為 CC-V2-1 的十項）。`tests/test_dashboard_static.py` 在 `3dfba2d..ded2769` 無 diff。
- OV-1 的保持：我的 headless Chrome 155／Edge 155（`file://`、斷網：DevTools offline＋host resolver 全部 NOTFOUND＋無效 proxy）載入、選 50 Startups、逐一操作五個方法與 k、比較全部、切換指標、切回 King County：非 `file:`／`data:` 請求 0。`python -m hw2.offline_scan`：`scanned 13 files: PASS (0 findings)`；`git grep "fetch"` 於 V2 腳本命中 0。
- **結果：PASS。**

### H-3 評估完整性（A-2、A-3）

**A-3（正式分析不變）**：

- `git show ded2769:<path> | sha256sum`：`assets/app.js` `c1ab3f21…82ad`、`assets/hw2core.js` `e75c5d48…2c14`、`assets/model_data.js` `6cf0c11e…a7ac`、`results/model_data.json` `69dc1465…6e61`、`assets/style.css` `60a27016…5f3f`，全部等於 DA 值且等於 `d7f02d4`。
- `git diff d7f02d4 ded2769 -- results hw2.ipynb assets/vendor data report README.md requirements.txt` 為空，所以 Test evaluation 紀錄（`results/` 內，run `fe76019b…`／digest `b53ff286…`）不變，README 與報告沒有探索數字。
- `hw2/`：`d7f02d4..ded2769` 只新增 `hw2/explore_reference.py`，既有模組（含 `selection.py`、`models.py`）無修改。
- **`hw2/explore_reference.py` 的判定**（A-3 要求 Reviewer 判定）：#75 新增它對 `hw2.selection`（`GroupGram.rss`／`importance`、`TIE_RTOL`）與 `hw2.models`（`METHOD_ORDER`、`PATH_METHODS`、`model_key`）的 import；以 `object.__new__` 建立 `GroupGram` 實例，不修改任何類別或模組狀態。`git grep explore_reference ded2769` 的程式引用只有 `tests/test_node_explore.py` 與 `tests/test_explore_kc_consistency.py`（其餘是註解與紀錄）；`hw2.ipynb` 與其他 `hw2/*.py` 不 import 它（另有 `test_the_reference_module_is_not_imported_by_any_formal_path`）。它重新表述的只有綁定 King County 的函式（`_pick` 綁 18 個 KC group、`lasso_entry` 讀 KC 列、`determine_winners` 對「方法沒有有效候選」拋例外），符合 Spec「需要 King County 專屬輸入的函式不被重用」。**判定：不在正式分析路徑上，符合 designation 第 4 點。**
- 探索檔案中 `model_data`／`MODEL_DATA`／`test_inputs`／`HW2Core`：只在兩處既有註解中出現（`explore_engine.js` 第 56 行、`explore_reference.py` 第 7 行，`3dfba2d` 已存在），沒有程式引用。

**A-2（自己執行測試與重算）**：

- 主 checkout（working tree＝subject）：`.venv/Scripts/python -m pytest -q -rs` → **442 passed，0 skipped**（52.7 s；Python 3.11.2、Node v24.19.0、sklearn 1.9.1）。`tests/test_explore_kc_consistency.py` 與 `tests/test_node_explore.py` 另行執行：16 passed、0 skipped。
- Node 直接執行：`explore_load` 15、`explore_boundary` 7、`explore_app` 12、`explore_methods` 7，皆 0 fail、0 skipped；我以 `tests/test_node_explore.py::write_reference` 自行產生參照到 scratchpad 後執行 `explore_contract.test.js` → **16/16 pass，0 skipped**；TAP diagnostic 列出 50 Startups 的 17 個候選，JS 與 Python 全部 `VALID`。
- **獨立重算**（自寫 numpy／scipy，只借用 `sklearn.linear_model.lars_path` 這個正式引擎；不用 `hw2`、不用 JS 引擎）：自寫 mulberry32＋Fisher–Yates 重現切分與 fold（與 JS 相同）；以 `lstsq` 的 RSS 做 Forward／Backward、以 `np.std(X_g b_g)` 做 RFE、以自己的標準化跑 LARS；逐 fold 擬合、驗證列計分、CV 平均與樣本標準差、A-1 有效性、方法與整體 winner；對整體 winner 的 canonical fit 以 `np.linalg.inv` 與 `scipy.stats.t` 重算 test 逐筆 PI。與 JS 引擎比較：

  | Case | 比對的 fold 子集 | 狀態、canonical 子集、winners | CV 平均／std 最大相對差 | 整體 winner 逐筆 predicted／lower／upper 最大相對差 | covered、coverage | Lasso entry alpha |
  | --- | --- | --- | --- | --- | --- | --- |
  | 50 Startups | 85，全部相同 | 全部相同（整體 `forward_sfs_k01`，四方法 winner k = 1；test 只算 `allin`、`forward_sfs_k01`） | 3.3e-10 | 2.3e-15／4.9e-15／1.3e-15 | 逐筆相同；1.0 | 順序相同，3.8e-14 |
  | synthetic_mixed | 105，全部相同 | 全部相同（整體 `allin`，與四方法 k = 5 共用模型） | 3.8e-13 | 2.8e-14／3.4e-14／2.4e-14 | 逐筆相同；0.9583 | 順序相同，2.5e-15 |
  | edge_single_categorical（G-2） | 25，全部相同 | 全部相同 | 3.6e-15 | 1.7e-15 | 逐筆相同；0.75 | 相同 |

- **Verify-the-verification（mutation，在 `git archive ded2769` 的 scratchpad 副本上；原檔未動）**：(M1) JS 方法內平手取較大 k → contract 1、methods 1 失敗；(M2) JS 方法間平手取後者 → contract 9、methods 1；(M3) JS 各 fold 的路徑改在整個訓練集上算（驗證列洩漏）→ contract 9、methods 1（layer 3 測試）；(M4) 移除 A-2、改以欄序補齊為子集 → contract 3、methods 2、app 1；(M5) 對所有 `VALID` 候選算 test → contract 9、app 1；(M6) 以 test RMSE 選 winner（破壞凍結）→ contract 9、methods 2（含 freezing）；(M7) canonical 子集改取 fold 0 的路徑 → contract 9；(M8) Lasso entry 改由小到大排序 → contract 6；(M9) RFE 改移除最重要的 group → contract 8；(M10) 相依關係的正負號規則反轉 → contract 2、app 1；(M11) Python 參照方法內平手取較大 k → contract 1、pytest 2 失敗。**(M12) 關閉 Python 參照自己的 active-set 退化判定（`_degenerate`）→ pytest 與全部 Node 測試 0 失敗**（見 R1-F2）。
- 三層邊界延伸到路徑（SR-V2-01）、winner 固定後才讀 test、test 只對 winner、PI 公式、A-1：讀碼確認（`explore_engine.js` `run()`：`trainDecisions(load, split.train)` → `dependencyGroups(…, split.train)` → 各 fold 以 `foldRows(split, f).train`、canonical 以 `split.train` 計算路徑 → `evaluateSubsets` → `determineWinners` → 之後才 `evaluateTest(…, split.test)`），並由上列測試、M3／M5／M6／M7 與獨立重算佐證。
- **結果：PASS**；另有 R1-F1（Medium，non-blocking，契約語義 routing）與 R1-F2（Low）。

### H-4 證據真實性與如實標示（A-5）

- 50 Startups：`git show ded2769:home_work_02/assets/data/50_Startups.csv | sha256sum` → `c6075ca5a7551243b31193bad9228f0a1b9468cdde2475c6586c56dcfac5630d`，與 ACCEPTANCE V2-4 記錄值相同；`3dfba2d..ded2769` 對 `assets/data/` 與 `.gitattributes` 無 diff（#74 R1 已核對來源與授權，本票未改）。
- ACCEPTANCE G 節新增的 V2-10～V2-17 與 V2-3 的指向修改，逐條對照 committed evidence：V2-10 的 change handler Chrome 10.3～42.6 ms（JSON `[42.6, 14.4, 10.3, 12.5, 12.3]`）、Edge 13.5～44.4 ms（`[44.4, 15.7, 13.5, 17.4, 17.7]`）、最後一次 controller Chrome 4.4 ms、Edge 6.7 ms（`engine_ms`）、圖的非白像素 16,157／16,040（`kchartPixels`）、比較全部 0／3、R² 摘要；V2-11 的無效 k（Forward／Backward／Lasso 6、7，RFE 5、6、7，`by_method[].kgrid`）與 Lasso k = 6 的 6 條原因、預測器 `aria-disabled=true`（`invalid_selected`）；V2-12 的四個 k = 2 提示與 All-in 無有效候選提示（`by_method[].nonWinner`）、`non_winner_with_test: []`；V2-15 的 Lasso 表與兩組相依關係（`initial.lassoRows`、`initial.deps`）；V2-17 的對比 6.49:1（341 處）／6.47:1（380 處）、溢出 0、markup 0、請求 0。全部相符；V2-13 的「比較表 5 列」指 `ex-semantics` 的五列，與 `index.html` 相符。V2-16 的測試數字與我自己的執行相同。
- 截圖：我讀過 `chrome_startups50_1280_full.png`、`chrome_degenerate_invalid_1280_full.png`，與描述相符、無缺字方塊；頁尾仍顯示（R3-5 屬 #76）。兩張修改內嵌資料後拍的截圖在畫面上仍顯示「50 Startups」標題與內建來源列，見 R1-F4。
- 「50 Startups 全部 k 有效」：Python 參照與 JS 都列出 17 個候選的狀態（我自己的 TAP 輸出與獨立重算），全部 `VALID`，Lasso 在訓練集與五個 fold 都沒有退化，共線診斷 0 組。
- **結果：PASS**；另有 R1-F3、R1-F4（Low，non-blocking）。

### H-5 使用者提供的資料來源與網路請求邊界（A-9）

- 我自己列舉五個 V2 腳本與 `startups50.js` 中 A-9 所列 API（`innerHTML`、`outerHTML`、`insertAdjacent*`、`document.write`、`DOMParser`、`createContextualFragment`、`srcdoc`、`eval`、`Function`、`setTimeout`／`setInterval`、`import(`、`Worker`、`importScripts`、`fetch`、`XMLHttpRequest`、`WebSocket`、`EventSource`、`sendBeacon`、`.src`／`.href`／`location`、`window.open`、storage、cookie、`postMessage`、`cssText`）：程式碼中**零**出現（唯一命中是 `explore_app.js` 第 13 行註解的 `localStorage` 字樣）。
- DOM 寫入點（#75 新增）：`explore_ui.js` 只用 `textContent`、`createTextNode`、`<option>.value`／`.text`、`className`，以及 `el()` 的 `setAttribute`——呼叫者傳入的鍵只有 `scope`、`rowspan`、`colspan`、`type`、`aria-pressed`、`aria-label`、`title`、`data-method`、`style`、`id`、`for`、`step`、`inputmode`，值都是常數、數字或 `'color:' + 常數色碼`，不來自資料；`explore_plot.js` 的 `KChart` 以 Chart.js 的文字選項（canvas）繪製，只有方法標籤與數字，`style` 只寫數值座標（既有 Scatter）。#75 沒有新增以使用者欄名為一般物件鍵的程式（diff grep）。符合 D-2。
- **瀏覽器探測**（R1 證據）：把 subject 匯出的 `index.html` 與 `assets/` 複製到 scratchpad，將內嵌資料換成我構造的 CSV（RFC 4180 引號）：欄名 `<img src=x onerror="document.title='pwned1'">`、`</script><b>bold</b>`、`javascript:alert(1)`（＝前兩欄之和，產生共線診斷與未進入 Lasso 的 group）、`<style>body{display:none}</style>`（類別）、`<script>alert(2)</script>`（目標）；類別值 `<svg onload=alert(1)>`、`"><iframe src=//evil.example>`、`a&amp;b`、`<script>alert(3)</script>`。headless Chrome 155、`file://`、斷網、選 50 Startups：`run = COMPLETED`；這些字串在共線診斷（feature group、編碼欄、關係式）、Lasso 表（含「未進入（退化後，只作展示）」列）、比較表、選取摘要、各 fold 子集、預測器 label 與下拉選項中全部以字面文字顯示；`#explore` 內 `img／svg／iframe／script／b／style` 元素 0；`document.title` 不變；`body` 仍為 `display: block`；選取無效的 Lasso k = 4、非 winner、All-in、比較全部、R² 指標都正常；dialog 0、例外 0、console error 0、非 `file:` 請求 0；切回 King County 後五個 V1 區塊與頁尾的 `innerText` 與切換前逐字相同。
- Mock fetch 測試（`explore_app.test.js`）我自己執行通過；`offline_scan` 例外屬 #76，本票沒有新增例外。
- **結果：PASS。**

## 3. AC 逐條核對（#75）

| AC | 結果 | 證據（本 R1 自行取得） |
| --- | --- | --- |
| 四種方法與 winner（主 seam，Node 對 Python 參照）：50 Startups 與 synthetic 非退化 fixture 的各 fold 子集、canonical 子集、狀態、各 fold 指標、CV 平均與 std、fit；方法 winner 與整體 winner（含平手）；test 只對 winner 且相對 1e-6；Lasso entry alpha 1e-6 與順序 | PASS | contract 16/16（`closeTo` 對 `folds`、`cv`、`fit`、`lasso_path`（訓練集與五個 fold）、`test`，`strictEqual` 對狀態、原因、子集、winners）；平手：`winner_cases.json` 三組注入案例 Node 對 Python，以及 50 Startups 的天然平手（四方法 k = 1 同 RMSE → 整體依方法順序取 Forward）；第 2 節 H-3 的獨立重算；M1、M2、M8、M9、M11 |
| 聚合與凍結（主 seam）：手算小案例 CV＝fold 算術平均；改 test 目標值只改 test 數字 | PASS | `explore_methods.test.js` 的閉式簡單回歸手算；JS 與 Python 各一個凍結測試；M6 使兩者失敗 |
| 退化與相依（主 seam）：退化 fixture 的 Lasso 退化步與其後 `INVALID_MODEL`／`lasso_path_degenerate`、退化前 entry alpha 相符、展示順序不標為實際路徑；共線候選 `INVALID_MODEL`；相依組與 group 映射與參照相同；winner 只從 `VALID`；All-in 無效時仍完成；不比退化情境的數值假設 | PASS（另見 R1-F1、R1-F2） | `degenerate_mixed`、`a1_collinear` Node 對 Python（只放寬完全相同兩欄的名稱）；`test_degenerate_fixture_semantics`；A-2 twin 測試（JS）；M4、M10；瀏覽器中 Lasso 表與共線診斷的呈現（探測頁與 Executor 的退化頁 evidence） |
| 50 Startups 全部 k 有效（主 seam） | PASS | Python 與 JS 都列出 17 個候選，全部 `VALID`（TAP diagnostic；`test_startups50_every_candidate_is_valid_and_the_split_is_80_20`；獨立重算） |
| King County 一致性（pytest）：通用參照重現正式分析的四條 canonical 路徑與 All-in；正式路徑不 import 參照 | PASS | `tests/test_explore_kc_consistency.py` 2 passed、0 skipped（與 `results/tables/cv_by_method_k.csv` 的 4×18 個 canonical 子集比對；All-in 係數 rtol 1e-12、R²／Adjusted R² 1e-12；只讀正式切分的訓練列）；import 判定見 H-3 |
| UI（人工檢查表）：五種方法的指標 vs k、比較全部、各方法 winner 與整體 winner、`INVALID_MODEL` 標示、非 winner 提示、兩個 problem 的語義差異；KPI 與圖只用訓練 CV 並標示；test 數字只出現在 winner | PASS（另見 R1-F3） | 我的 Chrome 155／Edge 155：五個方法按鈕；預設整體 winner Forward SFS k = 1；圖已繪製（非白像素 15,593／15,482）、標題「指標 vs k 訓練 CV」；KPI 子標「訓練 CV」；比較表 5 列、表頭分「訓練 CV」與「探索 test（非正式評估）」兩組；四個路徑方法選 k = 2 時 test 區塊展示該方法 k = 1 winner 並提示，選 winner 時無提示；All-in 選取時展示自身；比較全部 `aria-pressed` 切換；R² 摘要改變；比較表按鈕選取該 winner；`result.test` 只有 `allin`、`forward_sfs_k01`；`ex-methods` 區塊含四項差異、Test 的地位與逐列切分限制；375／768 px 溢出 0；無效候選的標示在探測頁（Lasso k = 4：KPI「無訓練 CV 指標」與原因、預測器停用）與 Executor 的退化頁 evidence |
| 不變量：V1 區塊 DOM／文字／`model_data`／腳本 sha256 不變；既有測試與 V2-T1 的測試全部通過；仍零 `fetch(` | PASS | H-3 A-3；442 passed（V1 既有測試與 `test_dashboard_static.py` 未改；`snapshots/v1_dashboard_blocks.json` 未改）；瀏覽器切回 King County 逐字相同；`fetch` 命中 0 |

**結案證據**：Node 與 pytest 輸出（skipped 0）——worklog §6.1 與我的執行相同；King County 一致性與 50 Startups 候選狀態表——worklog §6.1；ACCEPTANCE V2-10～V2-17 已填且附證據位置（H-4）；`model_data` sha256 不變（H-3）。

**#74 的 V2 測試被 #75 修改**（worklog D-10、D-11）：我讀過 `3dfba2d..ded2769` 對 `test_node_explore.py`、`explore_contract.test.js`、`explore_app.test.js`、`test_explore_static.py` 的刪除行。被改的是 #74 All-in 切片專屬的期望（三個 A-1 fixture 由 `REJECTED` 改為 `COMPLETED`，因為 Spec 只在全部候選無效時拒絕）與區塊清單（加 `ex-methods`）；A-1 的規則與 fold 改在 All-in 候選上照舊斷言，`a1_no_groups` 仍斷言 `REJECTED`／`ALL_CANDIDATES_INVALID`，沒有削弱任何檢查。DA I-5 與 designation 第 4 點的「既有測試不變」指接受基準時的測試，這些 V1 測試在本票無 diff。

## 4. DA 對 #75 的票義務與 run invariants

| 項目 | 結果 |
| --- | --- |
| G-1 UI 揭露逐列切分的限制（位於探索區塊） | 符合：`#explore` 子樹內的 `ex-methods`「逐列切分的限制」列出重複的列、同一實體多筆、時間相依、「不代表正式研究結論」；區塊標「探索執行，非正式評估」（`test_methods_block_states_the_two_problems_and_the_row_split_limits`；我的瀏覽器 `methodsText`） |
| G-2 主 seam (d) 的四種方法 | 符合：`edge_twenty_rows`、`edge_single_categorical`、`edge_all_numeric` 跑全部五種方法，Node 對 Python 通過；`edge_single_categorical` 另經獨立重算 |
| D-2 | 符合（H-5 節） |
| I-5 | 符合（第 3 節末段；`test_dashboard_static.py` 與快照未改且通過） |
| `ex-methods` 中關於 King County 的陳述 | 我對照 `hw2/preprocess.py`（`date`→`sale_days`、`yr_renovated`→旗標與有效年份、`zipcode` 類別、`sqft_basement` 不建模）、`hw2/split.py`（以房屋 `id` 分組的 80/20 與分組 5-fold）、`hw2/selection.py`（未進入的 group 依欄序排後）：屬實 |
| designation 第 4 點（經 CC-V2-1） | 符合（H-3 A-3） |
| designation 第 5 點 | 符合：沒有新增 CI、E2E 框架、`package.json` 或依賴（`requirements.txt` 無 diff）；新測試只用 `node:test` 與 pytest |
| designation 第 7 點 | 符合：學號見 H-1；50 Startups 未改 |
| Git 規則 | `2069fea`、`ded2769` 的 message 依 `[Modify] –` 格式，沒有 Claude 標記；未 push |
| 不在本票 | #74 R1-F2（一般物件鍵）與 R3-5（頁尾隱藏）屬 #76；預算、`SKIPPED_RESOURCE_LIMIT`／`FAILED`、取消、可重現性屬 #77；README／報告／ZIP 屬 #78。本票未處理它們，符合分配 |

## 5. Findings

### R1-F1 — 不是 active-set 退化的 Lasso 提前結束也被當成 A-2 退化；結果隨目標單位改變，頁面給出不屬實的原因（契約語義 routing）

- **Severity**：Medium。**Blocking**：**否**。其中的語義問題是 routing signal（治理 §4.2），required authority＝**Design Authority**。
- **證據**：
  - `assets/explore_engine.js` 第 777 行 `if (alpha <= EQ_TOL) break;`：LARS 在 `alpha = C / n` 不大於 float32 eps（1.19e-7，sklearn 的 `equality_tolerance`）時結束；目標只置中、不縮放，所以這個門檻是目標單位的絕對值。第 901 行把「路徑結束時仍有 group 未進入」一律標為 `cause = 'path_ended'`（`alpha_increasing`、`max_iter`、`multiple_drops` 也落在這裡），第 903 行使 k 超過已進入數的 Lasso 候選沒有子集 → `INVALID_MODEL`／`lasso_path_degenerate`。`hw2/explore_reference.py` 第 682–684 行同樣處理（worklog D-3）。
  - `assets/explore_app.js` 第 65 行把 `path_ended` 對使用者解釋為「路徑結束時仍有 feature group 沒有進入（它們與已進入的欄線性相依，或在這些列上沒有變化）」。
  - 我的探測（scratchpad `edge.js`，以 subject 的引擎）：50 Startups 只把 Profit 乘上常數，其他不變。×1、×1e-6：17 個候選全部 `VALID`；×1e-9：Lasso k = 4 `INVALID_MODEL`（fold 0、3 的路徑在 Administration 進入前結束）；×1e-10：k = 3、4 無效（Administration、State 未進入，訓練集與五個 fold）；×1e-12：Lasso k = 1～4 全部無效。Python 參照在 ×1e-10 得到相同結果。這些欄沒有共線、也有變化，所以頁面顯示的原因不屬實。
- **依據的契約條款**：Spec V2「LARS 退化（A-2）」與 Brief V2 §12 A-2 只把「active set 退化（新增欄使 active set 秩不足）」定義為 `lasso_path_degenerate` 的條件；Spec「Feature group 與特徵選擇」要求 Lasso 以 exact LARS 的 entry 排序、與正式分析相同；正式分析的欄序補齊規則明確不作探索模式的選模語義。契約沒有說「路徑因其他原因結束、仍有 group 未進入」時探索模式怎麼處理。DA H-3(ii)（A-1～A-3 語義）與 H-4（如實標示）。
- **具體 ambiguity（交 Design Authority）**：(a) 非 active-set 退化的提前結束（sklearn 的 equality tolerance、`alpha_increasing`、`max_iter`、同步多個 drop）是否屬於 A-2 的 `lasso_path_degenerate`／`INVALID_MODEL`，若是，原因應如何如實標示；(b) 探索模式的 Lasso 路徑可否用與目標單位無關的方式判定結束（例如對置中後的目標縮放再跑 LARS、entry alpha 以原尺度回報），並仍算「與正式分析相同」的 exact LARS。不論 (a)(b) 如何裁決，`path_ended` 的說明文字不得在原因不是共線或無變化時這樣宣稱（H-4），這是契約內的實作修正。
- **Non-blocking 的理由**：在 #75 的 operating scope 內，頁面只能載入原單位的 50 Startups（全部 `VALID`，已重現），沒有實現條件；這個行為只會移除 Lasso 候選，不會產生錯誤的數字、winner 或 test（winner 仍只從 `VALID` 選，test 仍只對 winner），不涉及洩漏。任意目標要到 #76 開放 URL／檔案輸入後才能送入；Brief V2 §10 已把「LARS 在使用者資料上退化」列為以 A-2 狀態處理的已知風險。
- **Disposition**：見第 6 節。

### R1-F2 — 主 seam 的退化 fixture 沒有觸發 active-set 退化；Python 參照的 A-2 判定沒有任何測試覆蓋

- **Severity**：Low。**Blocking**：否。
- **證據**：`degenerate_mixed` 與 `a1_collinear` 在訓練集與每個 fold 的停止原因都是 `path_ended`（Executor 的退化頁 evidence 與我的重跑），所以 A-2 的「加入的欄使 active set 秩不足」分支只由 `explore_methods.test.js` 的 JS-only twin 測試驗證。Mutation M12（把 `hw2/explore_reference.py` 第 646 行改為 `if False and _degenerate(G, active, j):`）後，pytest（`test_node_explore.py`、`test_explore_kc_consistency.py`）與全部 Node 測試仍 0 失敗。`tests/test_node_explore.py` 第 128–129 行 docstring 說「the Lasso path meets them last」，實際上路徑在嘗試 `dup_b` 之前就結束。我另以 twin 資料（`x1, twin=x1, x2, x3`）核對：JS 在 k = 2 以 `active_set_degenerate` 停止，參照得到 `path_ended`、三個 group 進入——與 worklog 的觀察一致，Brief V2 §8 允許退化情境下兩邊順序不同。
- **依據**：#75 AC「退化與相依（主 seam）」；Brief V2 §8「不假設 sklearn 保證…唯一進入順序」。
- **Non-blocking 的理由**：AC 的文字已滿足（退化 fixture 含共線欄、和欄、相等 entry，退化步、其後的 `INVALID_MODEL`、退化前 entry alpha 都經 Node 對 Python 比對）；精確的 active-set 退化在精確算術下只來自平手，跨實作沒有確定的順序，Brief 明文不要求一致；JS 的分支有 twin 測試與 M4 的失敗佐證。風險只在測試用參照的一段程式未被驗證。
- **Disposition**：見第 6 節。

### R1-F3 — 「方法與限制」表的「Test 的地位」寫「每次選取都重算」，容易被讀成選取候選會重算 test

- **Severity**：Low。**Blocking**：否。
- **證據**：`index.html` `ex-semantics` 的「Test 的地位」列：「探索 test：每次選取都重算、不保存，永遠不是 Test evaluation」。頁面其他地方的「選取」都指選取候選（「目前選取」「選取非 winner 時」），同一區塊下一段又說 test「只對 winner 計算一次」。實際行為：選取候選不重算 test（`testView` 只讀 `result.test`）；只有重新選取 problem 時整個 Exploratory run 重跑。
- **依據**：Spec V2「切分與交叉驗證」第 7 點「UI 的任何操作都不重算 test」；Brief V2 §5.6 第 4 條「探索結果每次重算」；DA H-4。
- **Disposition**：見第 6 節。

### R1-F4 — 兩張以修改後內嵌資料拍攝的截圖，畫面仍顯示 50 Startups 標題與內建來源

- **Severity**：Low。**Blocking**：否。
- **證據**：`doc/screenshots/v2-issue75/chrome_degenerate_invalid_1280_full.png` 的資料區顯示「50 Startups 利潤（探索）」與「來源：內建資料（assets/data/50_Startups.csv，取自 Avik-Jain/100-Days-Of-ML-Code，MIT 授權）」，資料卻是合成的退化資料（x1、x2、x_sum、dup_a…）；`chrome_h5_probe_1280_full.png` 同樣是替換內嵌資料的頁面。影像本身沒有標示；說明只在檔名、ACCEPTANCE V2-11／V2-15／V2-17（「合成退化資料頁」「探測頁」）與 worklog §6.3（「只替換內嵌資料的兩份頁面」）。
- **依據**：DA A-5「截圖的環境標示正確」、H-4。
- **Non-blocking 的理由**：引用它們的紀錄都如實說明了頁面經過修改，A-5 的環境標示由紀錄承擔；風險只在之後有人單獨引用影像。
- **Disposition**：見第 6 節。

### 觀察（不是 finding）

- **O-1**：Executor worklog §8 第 4 點的 `taskkill /F /IM chrome.exe` 是執行環境的副作用，不在 subject 內；Orchestrator 已處理（run record 第 162 列）。我只以自己啟動的程序 handle 結束 headless 瀏覽器，結束後以命令列核對沒有殘留。
- **O-2**：探索模式下頁尾仍顯示（我的截圖），依 DA R3-5 屬 #76。

## 6. Non-blocking findings 的 disposition

| Finding | Disposition | Owner |
| --- | --- | --- |
| R1-F1 | Route 至 Design Authority 裁決第 5 節的 (a)(b)，最好在 #76 的 R1 之前（#76 讓任意目標可以送入）。裁決之後的修正（含 `path_ended` 說明文字的如實化）屬契約內 rework，由 DA 指定承接的票（例如 #76 或 #77），並由該票的 R1 與 Spec Integration Audit 核對；不延長本 cycle | Orchestrator（派工 DA、排入後續票並追蹤）；裁決 authority＝Design Authority |
| R1-F2 | 本票不需修正。列入 Spec Integration Audit 的 pack 供知悉：參照的 active-set 退化分支未經測試、JS 分支只有 JS-only 測試。後續票若修改 Lasso 退化邏輯（例如依 R1-F1 的裁決），可同時補一個能讓參照的 `_degenerate` 生效的案例；不是新 AC | Orchestrator |
| R1-F3 | 文字修正（例如「每次執行探索都重算」），屬契約內的小修正；併入下一張修改 `index.html` 探索區塊的票（#76 或 #78），由該票的 R1 核對 | Orchestrator |
| R1-F4 | 不需修改影像。#78 彙整 ACCEPTANCE、README、報告與 ZIP 時，以及 Spec Integration Audit，不得把這兩張影像當作 50 Startups 或 Pages 的證據引用；若 #78 重整證據說明，可在 ACCEPTANCE 的證據欄補一句「內嵌資料已替換」 | Orchestrator（列入 #78 的派工 pack） |
| O-1、O-2 | 僅供知悉 | — |

## 7. Routing

- **Design Authority**：R1-F1（契約語義：非 active-set 退化的 Lasso 提前結束如何分類與標示；能否以與目標單位無關的方式判定結束）。
- 沒有 blocking finding，不需要 targeted correction、Final Adjudicator 或 acceptor。

## 8. Evidence（本 R1 執行的主要指令）

- `git rev-parse`、`git log`、`git show --stat`、`git diff --stat／--name-only／--name-status`（`d7f02d4`、`3dfba2d`、`2069fea`、`ded2769`）、`git show <rev>:<path> | sha256sum`、`git grep`（`explore_reference`、`model_data`、學號、URL、本機路徑）、`git archive ded2769 home_work_02 | tar -x`（scratchpad；不寫 git）、`git branch -r --contains ded2769`、`git check-ignore`。
- `gh issue view 75 --json body,…`（body sha256、建立與更新時間）。
- `.venv/Scripts/python -m pytest -q -rs`（主 checkout）；`tests/test_explore_kc_consistency.py`、`tests/test_node_explore.py` 單獨執行；`node --test --test-reporter=tap tests/js/explore_{load,boundary,app,methods}.test.js`；`HW2_EXPLORE_REFERENCE=<scratchpad> node --test tests/js/explore_contract.test.js`；`python -m hw2.offline_scan`。
- sklearn 1.9.1 `_least_angle.py` 第 625–910 行（LARS 主迴圈、退化警告、drop 與 verbose 輸出），用來核對 JS port 與參照的 verbose 解析。
- 自寫工具（scratchpad，不進 repo）：`dump_js.js`（JS 結果）、`indep.py`（numpy／scipy 獨立重算）、`mutate.py`（12 項 mutation）、`edge.js`（目標縮放與 twin 探測）、`make_pages.py`＋`cdp_check.js`（Chrome／Edge DevTools Protocol 檢查與 H-5 構造 CSV 探測）。
- Binding：Bindings §3.6 指令，對 session `37216426-…` 的 `subagents/` 讀取 `agent-a9a75e1af80e98547`（本 assignment）與 `agent-a5dedd102dd077202`（Executor）。
- 本 R1 只寫入本 record；沒有修改實作、測試、契約、gates 或其他紀錄，沒有 git 寫入操作。

VERDICT: CLOSURE
