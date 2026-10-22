# Audit record — #76 HW2 V2-T3，cycle 1，R1

- **Audit 種類**：Ticket independent audit，**R1**，cycle 1（治理 §4.4；Bindings b5 §5 Formal）。**本 record 不是 Spec Integration Audit**（Spec V2 有五張票，DA derivation §6 已判定不適用單 Ticket fast path）。
- **角色**：`primary_reviewer`（Primary Independent Reviewer；definition `gov-primary-reviewer`）。
- **Run**：`run-20261022-hw2-v2-enhance`（Orchestrator＝root session `37216426-f292-44f9-bad1-e2d862e7b8f1`）。
- **Work Contract**：GitHub issue #76（我以 `gh issue view 76 --json body -q .body | sha256sum` 重算 body sha256 `5d121dd9c08ea8fd05155c45aa4670a8d20bfc28cb954814f502be79e74cb2b2`，等於 DA derivation §3 記錄的 accepted 版本；OPEN、`ready-for-agent`、updatedAt 2026-10-21T16:27:24Z）；Outcome Contract `doc/governance/outcome-contract.md` §5（V2 接受，基準 `d7f02d4179d2cb5c2ecf0c39a4643a6ef8287907`）與 §5.2 CC-V2-1；Spec V2 rev 2（`doc/spec/SPEC-V2.md`；未提到者以 Spec rev 5）；Brief V2 rev 2＋E-1（含 §5.6 隔離）、Brief V1；`CONTEXT.md`；`doc/ticket/tickets-v2.md`；DA `decisions/derivation-SPEC-V2.md`（#76 列、B-2、B-11、B-12、B-14、D-1、D-2、I-1、I-2、I-5、G-5、§7.4 #76：H-1～H-5，A-1～A-5、A-7～A-9）；`decision-20261022-r1f3-v1-footer.md` R3-2、R3-5（分配給 #76）；`decision-20261022-issue75-lasso-early-stop.md`（分配給 #77，本票範圍外）；`decision-20261018-high-risk-categories.md`；run record §1 designation 第 4、5、7 點（經 CC-V2-1）。分配給 #76 核對的 findings：#74 R1-F2（`audit/issue-74-c1-r1.md`）、#75 R1-F3（`audit/issue-75-c1-r1.md`）。
- **受審 subject**：branch `home_work_02-v2-enhance`，HEAD **`a4b6c76d147e80011e848d23bc8424c3085fe9b3`**；BASE `450bcff1c8457252194d95fa1003da4edfdcf3af`。實作 commit `e405bf16a5fb008bbf8e3c4a626c9b6f650b1dfd`（10 個路徑：五個 `assets/explore*`、`index.html`、`hw2/offline_scan.py`、三個測試檔）；`a4b6c76` 只改 `doc/acceptance/ACCEPTANCE.md`、`doc/governance/worklog/issue-76.md` 與 `doc/screenshots/v2-issue76/`（`git show --stat` 核對）。`git diff --name-status 450bcff a4b6c76` 的 26 個路徑全部在 `home_work_02/` 內，沒有 `doc/requirement/`。審查時 working tree 對 subject 只差 run record（record-only path；`git diff a4b6c76 --stat`）；程式、資料與測試與 subject 相同。Commit 未 push（`git branch -r --contains a4b6c76` 為空）。

## 1. Assurance

### (a) Context independence（治理 §2.3；Bindings §3.7）

| Property | 滿足方式 |
| --- | --- |
| Independent context | Orchestrator 以 Agent tool 派工非 fork 的 `gov-primary-reviewer` subagent，從空白 context 開始，不繼承 Executor（agentId `acd62ed3a70012296`）的對話或推理。派工內容是路徑、識別與 SHA；其中的陳述（例如「`a4b6c76` 只加紀錄與證據」）與 worklog、ACCEPTANCE、evidence JSON 的內容一律當作 Executor 主張，以原始檔案、git 歷史、我自己執行的測試、獨立重算、mutation 與我自己的瀏覽器檢查驗證 |
| Verifiable binding | 本 assignment：agentId `ad730583783ecd443`，`agentType` `gov-primary-reviewer`；以 Bindings §3.6 指令讀取自己的 transcript，寫本 record 前觀測到 `('claude-opus-5-5', 'xhigh')` 155 則，單一元素，等於有效 mapping R-PR（Opus 5.5／`xhigh`）；沒有 escalation、沒有替代。全程核對（含之後的訊息）由派工者依 §3.6 在採用 return 前執行；本 record 不自證 binding |
| Autonomous access | 自行讀取 repo、`git log／show／diff／archive／grep`（不做 git 寫入）、GitHub API（issue body 與 sha256）；自行執行 pytest、Node 測試、`offline_scan`、Python 獨立重算、mutation 檢查與 headless Chrome／Edge（DevTools Protocol）檢查；scratchpad 的檔案只是我的工具，不進 repo |
| Self-written record | 本 record 由我以自己的 Write 工具寫入 Bindings §7 的位置；派工者只能原樣 commit |

### (b) Model diversity（Bindings §5；治理 §4.6 V22-17）

| Assignment | 實際 model（transcript 觀測，我自己以 §3.6 指令讀取） |
| --- | --- |
| Executor，agentId `acd62ed3a70012296`（`gov-executor`） | `claude-opus-5-5`／`high`（220 則，單一元素） |
| Primary Reviewer（本 R1），agentId `ad730583783ecd443` | `claude-opus-5-5`／`xhigh`（155 則，單一元素） |
| Alternate Reviewer | 尚未派工 |

**無 model diversity**（Executor 與 Primary 同為 `claude-opus-5-5`）。依 Bindings §5 與 DA A-8，不宣告 diversity 關係，不影響 independence 判定。

### Capability escalation

不提出。

## 2. CC-V2-1 與既有測試（I-5；designation 第 4 點）

- 對 `git ls-tree -r --name-only d7f02d4 -- home_work_02/tests` 的每個檔案執行 `git diff --quiet d7f02d4 a4b6c76`：唯一不同的是 `tests/test_dashboard_static.py`，其 diff 只有 CC-V2-1 那一條 `assert scripts == [...]`（前四項仍為 V1 四檔、順序不變，其後逐一列出六個 V2 腳本）；`git diff 450bcff a4b6c76 -- tests/test_dashboard_static.py` 為空——**本票沒有改動任何既有測試**。
- 本票修改的 `tests/test_explore_static.py`、`tests/test_node_explore.py` 是 #74（`1bd1df8`）新增的 V2 測試（`git log --diff-filter=A`）。`test_explore_static.py` 原有「V2 腳本沒有 `fetch(`」改為排除 `assets/explore_load.js`，是 #76 AC「靜態掃描」本身要求的例外；同時新增唯一呼叫點與選項的斷言（worklog D-9）。不是放寬既有不變量。
- **結論：符合 CC-V2-1 與 I-5。**

## 3. 高風險類別（DA A-1；derivation §7.4：#76 觸及 H-1～H-5）

### H-1 憑證、機密與不得公開的資料（A-4）

- 實際學號：從未追蹤的 `.local/packaging.json`（`home_work_02/.gitignore:13` 忽略）讀取比對值，不印出；`git grep -F` 於 `a4b6c76` 與 `e405bf1` 命中 0；`450bcff..a4b6c76` 的 commit message 命中 0。**已核對、無命中。**
- 新增或修改的追蹤路徑沒有 `.pdf`、`.zip`、`.env`、`kaggle`、`acceptor_materials`、`.local`。Evidence JSON／JSONL 沒有本機路徑或使用者名稱（`grep` `C:\Users`、`/Users/`、使用者名稱命中 0）。
- 新增內容中的 URL（`git diff 450bcff a4b6c76`，排除 PNG）：老師公開的範例 URL；`http://127.0.0.1:8761/8762`、`http://localhost`（Executor 的測試 origin）；測試中的合成值 `https://example.org/data.csv`、`https://user:secret@example.org/x.csv`、`https://other.example.org`；既有的 Kaggle URL（測試斷言 `ALLOWED_DATA_URLS` 未擴充）。沒有其他使用者 URL 或資料內容。
- URL 讀取不帶憑證：`requestInit()` 恰為 `{ method: 'GET', credentials: 'omit', redirect: 'error' }`（＋signal）；含帳密的 URL 在請求前被拒（`checkUrl` `has_credentials`）。我的瀏覽器檢查（第 3 節 H-5）：同 host 已持有 cookie 時，頁面發出的每個讀取都沒有 Cookie 標頭。沒有任何金鑰（RB-3）。
- **結果：PASS。**

### H-2 老師指定的名稱與格式（含 +2）

- +2「可任意輸入 Dataset」：URL 表單、本機 CSV 檔案、目標欄下拉齊備（`index.html` `#ex-custom`；`test_custom_dataset_panel_has_the_three_inputs_and_sends_no_form`）。老師範例 URL 在 `http://127.0.0.1` 頁面 origin 上載入成功（I-1 的 localhost 重現，見第 4 節）；**GitHub Pages 本身不在本票**（B-10、I-1），ACCEPTANCE V2-18 如實記 NOT TESTED（pending merge），沒有把 localhost 記為 Pages PASS。
- `offline_scan`：`python -m hw2.offline_scan` → `scanned 13 files: PASS (0 findings)`。例外以 `rel == FETCH_ALLOWED_FILE`（`assets/explore_load.js`，精確路徑）且 match 是 `fetch(` 為條件（`hw2/offline_scan.py` 第 29、41、124–127 行），其他規則對該檔照舊；`ALLOWED_DATA_URLS`、`DATA_FILES` 未改。我在 subject 匯出的副本上另做四項注入：`explore_app.js` 加 `fetch('x.csv')` → `network-api`；`explore_load.js` 加 `new XMLHttpRequest()` → `network-api`；`explore_load.js` 加外部 URL 字串 → `external-url`；`explore_ui.js` 加 `window.fetch ('a')` → `network-api`。乾淨匯出 0 findings。
- King County 與 50 Startups 零對外請求（請求隔離第 1 條）：我的 Chrome／Edge 在 `startups50`、`custom` 選取、檔案載入、目標改選與全部切換階段，DevTools 記錄的請求 0（第 3 節 H-5）。`file://` 斷網的 OV-1 重做屬 #78／Spec Integration Audit（A-6）。
- **結果：PASS。**

### H-3 評估完整性（A-2、A-3）

- **A-3（正式分析不變）**：以 `git show a4b6c76:<path> | sha256sum` 重算：`assets/app.js` `c1ab3f21…82ad`、`assets/hw2core.js` `e75c5d48…2c14`、`assets/model_data.js` `6cf0c11e…a7ac`、`results/model_data.json` `69dc1465…6e61`，全部等於 DA 值且等於 `d7f02d4`；`assets/style.css` `60a27016…` 也不變。`git diff --stat d7f02d4 a4b6c76 -- results hw2.ipynb assets/vendor data doc/requirement doc/spec doc/brief doc/ticket README.md report CONTEXT.md` 為空。`hw2/` 自 `d7f02d4` 只有 `explore_reference.py`（#74 新增，本票未改）與 `offline_scan.py`（B-2，在 boundary 內，不屬正式分析路徑）。Test evaluation 紀錄所在的 `results/` 與 notebook 無 diff。探索檔案不含 `MODEL_DATA`、`model_data`、`test_inputs`、`HW2Core` 的程式引用（唯一 grep 命中是 `explore_engine.js:56` 的註解「Nothing here reads model_data」，#74 起就有）。
- `index.html` 的 V1 部分：`d7f02d4` 版本的每一行都仍存在於 subject（逐行比對，缺 0 行）；頁尾 `<footer>` 元素逐字相同；diff 只在探索子樹內（橫幅、`#ex-custom`、`ex-semantics` 表的 Test 列）。
- **A-2（自己執行測試）**：
  - 主 checkout（working tree＝subject）：`.venv/Scripts/python -m pytest -q -rs` → **449 passed，0 skipped**（60.6 s；Python 3.11.2、Node v24.19.0）。
  - Node 直接執行：`explore_load` 15、`explore_boundary` 7、`explore_app` 12、`explore_methods` 7、`explore_custom` 16，皆 pass、0 fail、0 skipped。以 `tests/test_node_explore.py::write_reference` 自行產生參照到 scratchpad 後執行 `explore_contract.test.js` → **18 pass**、0 fail、0 skipped（含新的 `objkey_names`、`objkey_numeric_proto` 對 Python 參照，`closeTo` 以 `hasOwnProperty` 檢查 `fit.levels`／`fit.inputs` 的每個鍵）。
  - **獨立重算**（numpy／scipy，不用 `hw2` 與引擎）：以控制器 `submitData()` 載入我構造的自訂資料（`x` 數值、類別欄名為 `__proto__`、層級 base／high／low，60 列），取 JS 結果的切分；整體 winner＝All-in（`x`、`__proto__`）；自行以訓練列最先出現的層級為基準做 one-hot、`lstsq`、`inv(XᵀX)`、`t(0.975, 44)`，重算 12 筆 test 的 predicted／lower／upper、covered、coverage 與 RMSE／MAE／R²。與 JS 的最大相對差：predicted 2.0e-15、lower 2.1e-15、upper 1.9e-15、指標 5.2e-14；covered 逐筆相同；coverage 11/12 相同；`result.test` 的鍵只有 `allin`。
  - 引擎的變更只有 `putOwn`／`getOwn` 與 `ENGINE_VERSION`（`git diff 450bcff e405bf1 -- assets/explore_engine.js`）；50 Startups 的探索 test KPI 在內建、URL、檔案三種入口與我的瀏覽器中都是「9,850／8,351／97,026,682／0.9399／100.0%」。Lasso 停止條件未改（R4 屬 #77）。
  - README 與報告：`git diff d7f02d4 a4b6c76 -- README.md report/` 為空，沒有探索數字進入。
- **結果：FAIL（R1-F1）**：即時預測器在頁面上對名為 `__proto__` 的欄忽略使用者輸入，靜默給出錯誤的點預測與 PI（第 6 節）。其餘 H-3 核對 PASS。

### H-4 證據真實性與如實標示（A-5）

- ACCEPTANCE G 節 V2-18～V2-26 與 V2-7、V2-9 的兩處指向（`a4b6c76`）：逐條對照 committed evidence。`chrome_summary.json`／`edge_summary.json`：`teacher_url_localhost`（一個 GET、`type` Fetch、sha256 與 KPI 相等）、`url_cors_localhost`（`cookie:none`）、`target_requests_added` 0、`failures` 13 項（四種 URL 失敗與逾時的 `guide` true；其餘載入拒絕各有訊息）、`timeout_seconds` 20.041／20.028、`file_after_url_failure`（請求 0、sha256 與 KPI 相等）、`back_to_kc_identical`、`back_to_kc_2_identical`、`pending_then_kc`、`custom_again`、`end`（storage 0、網址與 cookie 不變）、`overflow` 0／0、`h5_probe`；`predictor_enter_base_vs_subject.jsonl`（BASE 變成 `index.html?`、subject 不變）；Chrome 的 `server_log`（OPTIONS 0、帶 Cookie／Authorization 0）。數值與 ACCEPTANCE、worklog §6 一致。我讀過 `chrome_custom_teacher_url_localhost_1280.png`：畫面為老師 URL 載入後的結果，檔名標示 localhost，底部沒有頁尾。
- 環境標示：V2-18 與 worklog §6.3 明寫「`http://localhost`，不是 Pages」；Pages 記 NOT TESTED（pending merge）（I-1、B-10）。
- **例外**：V2-26 把「#74 R1-F2 欄名（`__proto__`、`constructor`、`toString`）」列入 PASS 的範圍，worklog §3 第 4 點與 §8 也寫 R1-F2 已處理；證據只涵蓋載入、引擎與 `predictorView()` 的 Node 路徑，頁面上的預測器輸入路徑沒有被驗證，而且它實際上仍有缺陷（R1-F1）。這一處陳述需隨 R1-F1 的修正更正，歸入 R1-F1，不另立 finding。
- **結果：PASS，例外歸入 R1-F1。**

### H-5 使用者提供的資料來源與網路請求邊界（A-9）

- **API 列舉**（我自行 grep 全部 V2 腳本：`innerHTML`、`outerHTML`、`insertAdjacentHTML`、`document.write`、`DOMParser`、`createContextualFragment`、`srcdoc`、`eval`、`Function`、字串型 `setTimeout`／`setInterval`、`import(`、`Worker`、`importScripts`、`fetch`、`XMLHttpRequest`、`WebSocket`、`EventSource`、`sendBeacon`、`.src=`、`.href=`、`location`、`window.open`、storage、`indexedDB`、`document.cookie`、`postMessage`、`history.`、以 `on*`／`style`／`href`／`src` 為鍵的 `setAttribute`）：程式碼中唯一命中是 `explore_load.js:322` 的 `function defaultFetch(url, init) { return fetch(url, init); }`；另一處是 `explore_app.js:19` 的註解文字。
- **`fetch` 的呼叫路徑**：`defaultFetch` 只在 `fetchCsvBytes()` 未注入 `fetchImpl` 時使用；`fetchCsvBytes` 只由控制器 `submitUrl()` 呼叫；`submitUrl` 只由 `#ex-url-form` 的 `submit` 處理程序呼叫（`explore_ui.js:543–547`，`preventDefault`，按鈕停用時不動作）。選項符合 D-1：單一呼叫、GET、`credentials: 'omit'`、`redirect: 'error'`、沒有 `headers`／`mode`；失敗不重試；逾時以 `AbortController` 中止（20 s）；新提交或離開自訂資料集先中止前一個讀取並丟棄晚到的回應。
- **DOM 寫入**：新程式只用 `textContent`、`<option>.text`／`.value`、`disabled`；`el()` 的 `setAttribute` 鍵是固定字串。URL、檔名、HTTP 狀態文字、欄名與層級都經由文字型 API（D-2）。
- **Mock fetch**：`explore_custom.test.js` 16 項我自己執行通過；`explore_app.test.js` 的前四條仍通過。
- **我的 mutation**（scratchpad 的 subject 副本，每項改一處後還原）：`redirect: 'follow'`、`credentials: 'include'`、失敗後再呼叫一次網路函式、`leaveCustom` 不中止讀取 → `explore_custom.test.js` 各 2 項失敗；`predictorView` 改回一般鍵讀取 → 1 項失敗。控制器的 `generation` 檢查拿掉（晚到回應不以世代判斷丟棄）→ 0 項失敗（見 R1-F2）。
- **瀏覽器探測（R1 證據）**：我以 `git archive a4b6c76` 匯出 `index.html` 與 `assets/`，由 scratchpad 的 Python 伺服器在 `http://127.0.0.1:8871` 提供；第二個 origin `http://127.0.0.1:8872` 提供有／無 CORS 的 50 Startups、302、404、PNG 位元組、單欄文字，並記錄每個請求（方法、路徑、Cookie、Origin、`Access-Control-Request-Method`）。先造訪第二個 origin 的 `/setcookie` 讓瀏覽器持有 `127.0.0.1` 的 cookie，再開頁面。Headless Google Chrome 155.0.8059.85 與 Microsoft Edge 155.0.4283.62，全新 profile，DevTools Protocol 驅動。兩個瀏覽器結果相同：
  - 以檔案選擇（`DOM.setFileInputFiles`）載入刻意構造的 CSV：欄名 `<img src=x onerror="document.title='pwned'">`、`</script><b>bold</b>`、`javascript:alert(1)`（類別）、`<iframe src="//evil.example/x"></iframe>`（類別）、`<style>body{display:none}</style>`（目標），類別值 `<svg onload=alert(1)>`、`"><iframe src=//evil.example>`、`a&amp;b`、`<script>alert(3)</script>`、`javascript:void(0)`、`http://evil.example/z`。`run = COMPLETED`；欄位表、目標欄下拉、預測器 label 與下拉選項全部以字面文字顯示；`#explore` 內 img／svg／iframe／script／b／style 元素 0；`document.title` 不變；`body` 仍為 `display: block`；dialog 0、例外 0、console error 0；該階段請求 0。
  - URL 提交：每次提交恰一個 `GET`（`type` Fetch）；伺服器紀錄每個頁面讀取都帶 `Origin: http://127.0.0.1:8871`、沒有 Cookie（同 host 的 `/favicon.ico` 導覽請求帶有 cookie，證明 cookie 存在）、OPTIONS 0；`/redirect.csv` 之後沒有對其目標的請求（不跟隨重新導向）；`javascript:alert(1)` 請求 0。
  - 切回 King County：五個 V1 區塊與頁尾的 `innerText` 與初次載入逐字相同。
- **結果：PASS**（R1-F1 是資料處理的正確性問題，不涉及 markup 或請求）。

## 4. AC 逐條核對（#76）

| AC | 結果 | 證據（本 R1 自行取得） |
| --- | --- | --- |
| 輸入面板：老師範例 URL 在 Pages 環境載入並顯示結果；同一份 CSV 以檔案載入 → 相同數字；sha256 相同時 URL／檔案／內建三種入口確定部分一致（Node） | PASS（依 I-1：localhost 重現；Pages 屬 B-10） | 我的 Chrome／Edge：老師 URL（真實網路）一個 GET，sha256 `c6075ca5…630d`，探索 test KPI 與內建逐字相同；URL 失敗後以檔案載入 `50_Startups.csv`：KPI 與 sha256 相同、請求 0；`explore_custom.test.js`「the URL, file and built-in entrances…」：去掉計時與入口標籤後逐值相同 |
| 目標欄：預設最後一欄；可改；非數值 → `TARGET_NOT_NUMERIC` 提示重選、不執行 | PASS | 瀏覽器：預設 `Profit`（index 4）；改選 State →「預測目標欄「State」不是數值欄（TARGET_NOT_NUMERIC），沒有執行分析。請在「預測目標欄」下拉改選數值欄…」，模型與 test 區塊不顯示；改選 Administration → 完成（KPI 改變）；改選期間請求 0；Node「target column」 |
| 失敗訊息：非 CSV、無欄名、目標非數值、列數不足、超過載入上限、重複欄名、URL 失敗（含跨來源）各有 zh-TW 訊息；URL 失敗含「下載後以檔案載入」；之後改以本機 CSV 成功 | PASS | 瀏覽器：無 CORS 與 302 → `URL_FETCH_FAILED，network`（訊息寫明跨來源與重新導向）；404 →「HTTP 404 Not Found」；PNG → `not_text`；單欄文字 → `NOT_CSV`「只有 1 欄」；四種 URL 失敗皆附「請用瀏覽器下載該 CSV，再以下方的「本機 CSV 檔案」載入」；之後檔案載入成功。Node：七種拒絕＋`ENCODING`＋列數上限各有不同訊息；我另以 Node 核對 `TOO_LARGE`（列、欄）、`TOO_FEW_ROWS`、`NO_HEADER`、`RAGGED_ROWS` 的訊息內容與 detail 相符。逾時（20 s）我沒有在瀏覽器重現：由 mock 測試（40 ms 注入、abort、呼叫數 1）與讀碼確認，並與 Executor 的 committed evidence（20.04／20.03 s）一致 |
| 請求隔離第五條（mock fetch）：只有提交自訂 URL 時恰一次 GET、不重試、不帶憑證；失敗回報 `URL_FETCH_FAILED` 與子原因且不再發請求；V2-T1 前四條仍通過 | PASS | `explore_custom.test.js`（init 的鍵恰為 `credentials`／`method`／`redirect`／`signal`）；`explore_app.test.js` 12 pass；我的 mutation M1–M3；瀏覽器伺服器紀錄 |
| 靜態掃描：只有探索載入模組允許 `fetch(`；其他任何檔案出現網路 API 即 finding；既有掃描測試通過 | PASS | 第 3 節 H-2 的四項注入；`test_offline_scan_exception_is_one_path_and_fetch_only`、`test_fetch_appears_once_and_only_in_the_load_module`；`test_dashboard_static.py` 既有掃描測試未改且通過 |
| 切換：KC→50→自訂→KC，V1 區塊不變；自訂失敗或成功後切回 KC 亦不變；重新選自訂時要求重新提交 | PASS | 瀏覽器：在多次 URL 成功／失敗與檔案載入之後，KC→50 Startups→自訂→KC：兩次 KC 的 V1 區塊與頁尾 `innerText` 與初次載入逐字相同；再選自訂時面板狀態「尚未載入資料」、URL 欄空白、目標欄停用。Node「switching…」（讀取中切換：中止、晚到回應丟棄） |
| 不儲存：不寫入 localStorage、URL 參數或檔案 | PASS | 瀏覽器：全部流程後 localStorage／sessionStorage 長度 0、`location.href` 不變、`document.cookie` 只有我設的測試 cookie；Node vm 陷阱 0 次 |
| 不變量：V1 區塊 DOM／文字／`model_data`／腳本 sha256 不變；既有測試與 V2-T1 測試全部通過 | PASS | 第 2 節、第 3 節 H-3；449 passed、0 skipped |
| 結案證據：Node 與 pytest 輸出、ACCEPTANCE 條目附證據位置、mock fetch 輸出、localhost 截圖 | PASS，例外歸入 R1-F1 | 第 3 節 H-4 |

## 5. DA 對 #76 的票義務、分配的 findings 與 run invariants

| 項目 | 結果 |
| --- | --- |
| D-1 嚴格讀法 | 符合（第 3 節 H-5；mock 以 init 參數驗證；瀏覽器 OPTIONS 0、不跟隨 302、無 Cookie） |
| D-2 | 符合（H-5 探測） |
| I-1 | 符合：localhost 重現並標明；Pages 記 NOT TESTED（pending merge） |
| I-2 | 符合：例外以精確路徑與 `fetch(` 為鍵；`ALLOWED_DATA_URLS`、`DATA_FILES` 不變；載入模組沒有寫死任何 URL（`test_fetch_appears_once…` 的 `https?://` 斷言與我的 grep） |
| I-5 | 符合（第 2 節） |
| G-5 | 符合：切回 50 Startups 時 `selectProblem('startups50')` 每次重跑（讀碼；Node `views.at(-1).run.result.run.status`）；切回自訂要求重新提交（瀏覽器與 Node） |
| R3-2、R3-5（V1 頁尾） | 符合：`explore.css` 的 `body.is-exploring footer.footer { display: none !important; }`，`explore_ui.js` 不碰頁尾；我的瀏覽器：初次 KC `display: block`，50 Startups 與自訂（空白、成功、失敗後）`none`，切回 KC `block` 且 `innerText` 與 `outerHTML` 長度與初次相同；頁尾 DOM／文字與 `d7f02d4` 逐字相同；`style.css`、`app.js` sha256 不變；快照與 `V1_SELECTORS` 測試通過 |
| #75 R1-F3（「每次選取都重算」） | **已解決**：`ex-semantics` Test 列改為「探索 test：每次執行探索時只對 CV winner 計算一次（選取候選或切換方法不會重算）、不保存，永遠不是 Test evaluation」；探索橫幅同類用語一併改為「每次執行探索（選取 50 Startups，或提交自訂資料集）都在瀏覽器內重新計算」；兩處都在探索子樹內；`test_methods_table_no_longer_says_recomputed_on_every_selection` 通過 |
| #74 R1-F2（使用者欄名作一般物件鍵） | **部分解決**：載入的重複欄名檢查（`Map`）、引擎的 `fit.levels`、`fit.inputs`、`n_unseen_by_group`、`inputSpec()`、`predict()`、`predictorView()` 已改為自有屬性；Node 與 Python 對照案例 `objkey_names`、`objkey_numeric_proto`、`proto_names`、`duplicate_proto` 通過，`__proto__,__proto__,y` 為 `DUPLICATE_COLUMN`。**頁面預測器的輸入收集仍以一般物件指派**，名為 `__proto__` 的欄仍出錯 → **R1-F1** |
| `decision-20261022-issue75-lasso-early-stop.md` | 本票範圍外（#77）；本票沒有修改 Lasso 停止條件或 `path_ended` 說明 |
| designation 第 4 點（經 CC-V2-1） | 符合（第 2 節、第 3 節 H-3） |
| designation 第 5 點 | 符合：沒有新增 CI、E2E 框架、`package.json` 或依賴；新測試只用 `node:test`／`node:vm` |
| designation 第 7 點 | 符合（H-1） |
| Git 規則 | `e405bf1`、`a4b6c76` 的 message 依 `[Modify] –` 格式，沒有 Claude 標記（grep 0）；未 push |

### Executor 提給 Reviewer 的 concerns（worklog §8）

- **#1 讀取沒有位元組上限**：同意這屬 #77 的「資源保護」（Spec V2「候選有效性、狀態與運算預算」）；本票的 AC 沒有大小拒絕以外的要求，`TOO_LARGE` 照契約在讀完後判定。不是本票 finding；列為觀察 O-1。
- **#2 D-3 與 D-4**：D-4（只接受含 scheme 的 `http:`／`https:` 完整網址、拒絕帳密，請求前在面板提示，不新增原因碼）與 D-1「每次提交最多一個請求、對象就是提交的 URL」、H-1「不帶憑證」、Out of Scope「CSV 文字貼上輸入」（`data:` URL 等同貼上）一致，屬 HOW。D-3（回應本文含 NUL 位元組＝`not_text`）是 Spec「回應不是文字」子原因的合理判定；同一份含 NUL 的位元組經檔案會是 `ENCODING`（`nul_character`），經 URL 是 `URL_FETCH_FAILED`／`not_text`——兩者都是拒絕且都有指引，差異來自 Spec 只為 URL 入口列出的子原因，不影響「內容相同即確定部分相同」（那是對可執行內容的契約）。不需 Design Authority。
- **#3 D-10**（預測器表單按 Enter 會送出）：我核對 `predictor_enter_base_vs_subject.jsonl` 與 `explore_ui.js:552`；修正只在 V2 檔案，與本票 AC「不儲存（URL 參數）」「切換」相關，V1 表單未動。符合。
- **#4 引擎在主執行緒同步執行**：屬 #77。

## 6. Findings

### R1-F1 — 頁面的即時預測器以一般物件收集輸入：名為 `__proto__` 的欄，使用者輸入被靜默忽略，顯示錯誤的點預測與 PI（#74 R1-F2 未完全解決）

- **Severity**：Medium。**Blocking**：**是**。
- **證據**：
  - `assets/explore_ui.js` 第 382–385 行（`renderPredictor` 的 `update()`）：`var raw = {}; inputs.forEach(function (x) { raw[x.spec.name] = x.input.value; }); var v = App.predictorView(Engine, candidate, raw);`。欄名為 `__proto__` 時，`raw['__proto__'] = '<字串>'` 呼叫的是 `Object.prototype.__proto__` 的 setter，值不是物件而被忽略，不會成為自有屬性。`explore_app.js` 第 276 行的 `predictorView` 以 `engine.getOwn(raw, s.name)` 讀取，得到 `undefined`，於是改用 `s.default`（數值欄＝訓練中位數；類別欄＝基準層級），**不產生任何警告**。
  - 我的 headless Chrome 155 與 Edge 155（subject 的 `git archive` 匯出、`http://127.0.0.1` origin、以檔案選擇載入）結果相同：
    - 數值欄 `__proto__`、`constructor`，目標 `y`（y ≈ 4·`__proto__` + 10·`constructor`），整體 winner All-in：把 `__proto__` 輸入改為 `9` 與 `-9`，頁面都顯示點預測 **2.24**、PI 1.29～3.19；改 `constructor` 為 0.9／0.1 則顯示 6.08／−1.97（正常）。
    - 類別欄 `__proto__`（base／high／low，效果 0／+50／−50）與數值欄 `x`，winner All-in：選 `high` 與 `low`，頁面都顯示 **10.92**、PI 9.99～11.84；改 `x` 則正常變化。
  - 同一份資料在 Node 以頁面的建法（一般物件指派）與以自有屬性／`Map` 呼叫 `predictorView` 對照：`__proto__ = 9` → 頁面路徑 2.2376、正確值 41.1840；`-9` → 2.2376 對 −30.7577；`high` → 10.9156 對 60.8811；`low` → 10.9156 對 −39.1290；頁面路徑的 warnings 皆 0。
  - 載入契約接受 `__proto__` 作為欄名（`LOAD_CASES["proto_names"]` 斷言 `ok`；只有重複欄名被拒），所以這是 #76 開放的 URL／檔案入口上合法、可達的輸入。
  - 測試沒有涵蓋這條路徑：`explore_custom.test.js` 第 381–389 行以 `E.putOwn` 或 `Map` 建 `raw` 後呼叫 `predictorView`；沒有任何 Node 測試載入 `explore_ui.js`；Executor 的瀏覽器探測沒有使用 `__proto__` 欄名。ACCEPTANCE V2-26 與 worklog §3 第 4 點、§8 把 R1-F2 記為已處理（第 3 節 H-4）。
  - V2 頁面檔案中，以使用者欄名作一般物件鍵的寫入，我 grep 後只剩這一處（`[x.spec.name] =`）；引擎、載入與 `predictorView` 已改。
- **依據的契約條款**：
  - Spec V2「即時預測器」（輸入依該候選的 group 動態產生；輸出點預測與 PI），以及「載入契約」（欄名除重複外不受限）；Brief V2 §3.1 +2「可任意輸入 Dataset」與 §5.4 即時預測器；DA D-2 的理由（accepted 不變量必須對任意輸入成立）。
  - #74 R1-F2 的 disposition（`audit/issue-74-c1-r1.md` §7）：以 `Map`、`Object.create(null)` 或自有屬性檢查取代一般物件鍵，修正須在 #76 結案前完成，由 #76 R1（H-3、H-5）核對。
  - DA derivation §7.2 H-3(ii)：錯誤不會讓程式失敗，只會讓結果看起來正確；H-4：ACCEPTANCE 狀態與證據逐條相符（A-5）。
- **Blocking 的理由**：#74 R1 把 R1-F2 判為 non-blocking，唯一理由是在 #74 的 operating scope 內使用者無法送入任意欄名；#76 開放了這兩個入口，實現條件因此成立。這個缺陷讓頁面對一個 accepted 契約接受的輸入靜默顯示錯誤的數值（不是錯誤訊息），屬 DA 宣告的高風險類別 H-3 所描述的機制；它也是分配給本票、明訂在本票結案前完成的修正的一部分。發生需要特定欄名，機率低，所以是 Medium 而不是 High；修正範圍很小，可驗證。
- **要求的 targeted correction**：
  1. 頁面預測器的輸入收集改用與 D-8 相同的方式（`Engine.putOwn`、`Map` 或等效作法），使任何欄名（含 `__proto__`）的輸入值都送到 `predictorView`。做法由 Executor 決定，限 V2 檔案。
  2. 提供 closure 與回歸證據（治理 §4.4）：頁面路徑上 `__proto__` 數值欄與類別欄的輸入改變時，點預測與 PI 隨之改變並等於以自有屬性／`Map` 計算的值；全部 pytest 與 Node 測試通過；A-3 sha256 不變。是否新增自動化測試由 Executor 決定（不是新 AC、不是新 seam）。
  3. 更正 ACCEPTANCE V2-26 與 worklog 中 R1-F2 的陳述，使其與修正後的證據一致（record-only）。
  4. 不夾帶其他修改。
- **R2 核對**：(a) 在瀏覽器以數值與類別 `__proto__` 欄重做上列探測，預測隨輸入改變且數值正確；(b) V2 頁面檔案中沒有其他以使用者欄名作一般物件鍵的寫入；(c) 修正的 diff 只限上述範圍；(d) 測試全部通過、A-3 與 V1 區塊不變；(e) V2-26 與 worklog 的陳述與證據一致。

### R1-F2 — 控制器以世代丟棄晚到回應的檢查沒有被任何測試偵測；頁面接線（`explore_ui.js`）沒有自動化覆蓋

- **Severity**：Low。**Blocking**：否。
- **證據**：我的 mutation M6 把 `explore_app.js` `submitUrl()` 中的 `if (gen !== generation || state.problem !== 'custom' || !custom) return null;` 改為 `if (!custom) return null;`，`explore_custom.test.js` 0 項失敗。原因是被取代的讀取同時被 abort，`fetchCsvBytes` 回傳 `cancelled`，所以測試看不出世代檢查是否存在；若拿掉它，前一次提交的 `cancelled` 回應會把下一次仍在進行中的提交標為非 busy（按鈕提前恢復）。另外沒有任何 Node 測試載入 `explore_ui.js`，R1-F1 就在這一層。
- **依據**：Spec V2 Testing Decisions（只測外部可觀察的行為與契約）；#76 AC「切換」「新提交取代進行中的提交」由現有測試在行為層面涵蓋。
- **Non-blocking 的理由**：行為正確（abort 路徑已保證晚到回應不顯示，我的瀏覽器與 Node 都核對過）；缺的是防禦層的測試覆蓋，不是契約違反。
- **Disposition**：見第 7 節。

### 觀察（不是 finding）

- **O-1**：讀取沒有位元組上限（Executor concern #1）。資源保護屬 #77（Spec「資源保護」）；供 #77 與 Spec Integration Audit 知悉。
- **O-2**：載入失敗但內容已讀到時（例如 `NOT_CSV`），面板狀態寫「目前的資料：URL …」，同時訊息區明確寫出拒絕原因；可理解，不影響 AC。
- **O-3（審查環境的副作用，不在 subject 內）**：我在確認瀏覽器是否存在時，執行了 `chrome.exe --version`；在 Windows 上這會啟動 Chrome（使用者預設 profile），而不是只印出版本。我以 PowerShell 確認該程序（PID 9848，父程序是我的 bash）與其子程序都是我啟動的，以 `taskkill /PID 9848 /T`（之後 `/F`）只結束這棵程序樹；當時沒有其他 Chrome 程序。之後的瀏覽器檢查一律使用 scratchpad 的全新 profile，並以各自的 PID（9128、14640）結束；兩個本機伺服器以 PID 38048（及其子程序 36772）結束；結束後以命令列核對沒有殘留。這次啟動可能在 acceptor 的 Chrome 預設 profile 留下一次開啟紀錄；告知 Orchestrator 以便需要時轉告 acceptor。

## 7. Non-blocking findings 的 disposition

| Finding | Disposition | Owner |
| --- | --- | --- |
| R1-F2 | 本票不要求額外工作；不延長本 cycle。R1-F1 的修正若新增頁面層的測試，可順帶涵蓋，但不是條件。列入 Spec Integration Audit 的 pack 供知悉 | Orchestrator（列入 Spec Integration Audit pack） |
| O-1 | 供 #77 派工 pack 與 Spec Integration Audit 知悉 | Orchestrator |
| O-2 | 無需處理 | — |
| O-3 | 告知 acceptor（是否需要轉告由 Orchestrator 依其規則決定） | Orchestrator |

## 8. Routing

- **Executor（targeted correction）**：R1-F1，經 Orchestrator 派工（同一 worklog identity）；之後由 R2 核對。
- 沒有需要 Design Authority、Final Adjudicator 或 acceptor 裁決的契約語義或 boundary 問題（Executor concern #2 的 D-3／D-4 我判定在 HOW 範圍內，見第 5 節）。

## 9. Evidence（本 R1 執行的主要指令）

- `git log`、`git show --stat`、`git diff --stat／--name-status／--name-only`（`d7f02d4`、`450bcff`、`e405bf1`、`a4b6c76`）；`git ls-tree -r`；`git diff --quiet`（既有測試逐檔）；`git show <rev>:<path> | sha256sum`；`git grep`（學號比對，值不印出）；`git branch -r --contains a4b6c76`；`git archive a4b6c76 home_work_02/index.html home_work_02/assets`（scratchpad；不寫 git）。
- `gh issue view 76`（body、sha256、狀態、label、時間）。
- `.venv/Scripts/python -m pytest -q -rs`（主 checkout：449 passed）；`node --test --test-reporter=tap tests/js/explore_{load,boundary,app,methods,custom}.test.js`；`HW2_EXPLORE_REFERENCE=<scratchpad> node --test tests/js/explore_contract.test.js`（18 pass）；`python -m hw2.offline_scan`。
- 自寫工具（scratchpad，不進 repo）：`servers.py`（兩個 `127.0.0.1` origin 與請求紀錄）、`cdp76.js`（Chrome／Edge DevTools Protocol：初次載入、50 Startups、自訂空白、CORS URL、目標改選、302、無 CORS、404、PNG、單欄文字、`javascript:`、老師 URL、URL 失敗後檔案、H-5 探測、`__proto__` 預測器探測、切換、storage）、構造的 CSV（`probe76.csv`、`proto_numeric.csv`、`proto_categorical.csv`）、numpy／scipy 獨立重算、mutation 副本（M1–M6）、`offline_scan` 注入副本。
- Binding：Bindings §3.6 指令，對 session `37216426-…` 的 `subagents/` 讀取 `agent-ad730583783ecd443`（本 assignment）與 `agent-acd62ed3a70012296`（Executor）。
- 本 R1 只寫入本 record；沒有修改實作、測試、契約、gates 或其他紀錄，沒有 git 寫入操作。

VERDICT: BLOCKING (R1-F1)
