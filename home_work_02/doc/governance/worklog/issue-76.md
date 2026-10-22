# Worklog — #76 HW2 V2-T3（自訂資料集：URL 與本機檔案輸入、目標選擇、失敗訊息與請求隔離）

- **Work item**：GitHub issue #76（V2-T3），Formal lane，run `run-20261022-hw2-v2-enhance`（Orchestrator＝root session `37216426-f292-44f9-bad1-e2d862e7b8f1`）。
- **執行角色**：Executor（治理 §2.1；`gov-executor`，有效 mapping `claude-opus-5-5`／`high`，Bindings b5 §3.1 O-1）。
- **Subject**：branch `home_work_02-v2-enhance`（未 push）。BASE `450bcff1c8457252194d95fa1003da4edfdcf3af`（#75 結案後）；實作 commit `e405bf16a5fb008bbf8e3c4a626c9b6f650b1dfd`；之後的紀錄 commit 只改 `doc/`（本 worklog、`doc/acceptance/ACCEPTANCE.md` 的 V2-18～V2-26 與 V2-7、V2-9 的兩處指向、`doc/screenshots/v2-issue76/` 的證據），沒有程式、資料或測試的變更。**Cycle 1 targeted correction（R1-F1）**：BASE `ce97221`（含 R1 record `audit/issue-76-c1-r1.md`）；修正 commit `c4256f54a8ece52ef71aff93a719f7d8db1604b6`（只改 `assets/explore_ui.js` 與 `tests/test_explore_static.py`）；之後的紀錄 commit 只改 `doc/`（見 §10）。
- **狀態**：R1（`audit/issue-76-c1-r1.md`）BLOCKING on R1-F1；targeted correction 與其 self-verification 完成（§10），待 R2。

## 1. Contract reference

| 契約 | 位置與版本 |
| --- | --- |
| Outcome Contract | `doc/governance/outcome-contract.md` §5（V2 接受紀錄，接受基準 `d7f02d4`）、§5.2 CC-V2-1（只有那一條 `<script src>` 斷言可改；本票沒有新增腳本檔，該斷言與 `tests/test_dashboard_static.py` 未動） |
| Ticket | GitHub #76（`gh issue view 76`；body 與 DA derivation §3 記錄的 accepted 版本相同，DA R1-F3 decision §6 亦核對 sha256 `5d121dd9…b2b2`） |
| Spec | `doc/spec/SPEC-V2.md` rev 2（「載入契約」入口、「Problem 與頁面結構」切換、「離線與請求隔離」、次 seam「請求隔離（mock fetch）」、靜態 seam）；未提到的事項以 `doc/spec/SPEC.md` rev 5 為準 |
| Brief | `doc/brief/BRIEF-V2.md` rev 2＋E-1（§5.6 隔離四條）；`doc/brief/BRIEF.md` |
| DA derivation | `doc/governance/decisions/derivation-SPEC-V2.md`：§4 #76 列（在 boundary 內，附 I-1、I-2、D-1、D-2）；B-2（修改 `hw2/offline_scan.py` 在 boundary 內）；§5.2 G-5；§7.4 #76：H-1～H-5，A-1～A-5、A-7～A-9；§8 D-1（每次提交最多一個請求：單一呼叫、GET、`credentials: 'omit'`、不跟隨重新導向、無自訂標頭、不重試、逾時 abort）、D-2（輸入衍生字串只當資料）、I-1（合併前以 `http://localhost` 重現，不記為 Pages PASS）、I-2（例外只以探索載入模組路徑與 `fetch(` 為鍵；不擴充 `ALLOWED_DATA_URLS`、`DATA_FILES`；載入模組不寫死任何 URL）、I-5（既有測試不變） |
| DA decision | `decisions/decision-20261022-r1f3-v1-footer.md` R3-2、R3-5（探索模式隱藏 V1 頁尾，只在 V2 檔案實現；頁尾 DOM／文字、`style.css`、`app.js`、快照不變）。`decisions/decision-20261022-issue75-lasso-early-stop.md`：只知悉，工作屬 #77，本票未實作 |
| 追蹤 findings | #74 R1-F2（`audit/issue-74-c1-r1.md`：使用者欄名當作一般物件鍵；依 disposition 修正並加 Node 與 Python 對照案例）；#75 R1-F3（`audit/issue-75-c1-r1.md`：「每次選取都重算」用語） |
| Run invariants | run record §1 designation 第 4–7 點（經 CC-V2-1）：正式分析、`hw2/` 正式路徑、`model_data`、`results/`、Test evaluation 紀錄、V1 區塊 DOM／文字／行為（含頁尾文字）、V1 腳本與核心模組、`style.css`、既有測試不變（V2 測試可延伸）；不重跑 notebook、不做新的 Test evaluation；只有四個 seams；追蹤檔案不含學號；只改 `home_work_02/` 且不碰 `doc/requirement/` |
| 不在本票 | 運算預算、`SKIPPED_RESOURCE_LIMIT`／`FAILED`、取消、非阻塞、R4-2～R4-4（#77）；README、報告、ACCEPTANCE 彙整、ZIP、R3-6（#78） |

## 2. Binding

| 對象 | 觀測（Bindings §3.6 指令，全部 assistant 訊息） | 結果 |
| --- | --- | --- |
| 本 assignment，agentId `acd62ed3a70012296`（`agentType` `gov-executor`） | `('claude-opus-5-5', 'high')`：208 則（截至寫入本節；return 前由派工者依 §3.6 全程核對） | 單一元素，等於有效 mapping；無 escalation、無替代 |

- Bounded assignments：**未使用**（沒有派 `gov-investigator`／`gov-bounded-worker` 或任何 subagent）。

## 3. Work performed

1. **讀取與基準**：Bindings b5、`gov-executor.md`、Implementation Profile §3–§5、§9、治理 §3.5、§3.7、§3.8；OC §5／§5.2；`gh issue view 76`；Spec V2、DA derivation（#76 列、B-2、D-1、D-2、I-1、I-2、I-5、G-5、§7）、R1-F3 decision、Lasso early-stop decision（知悉）、run record；#74／#75 的 worklog 與 R1 records（R1-F2、R1-F3）；`assets/explore_*.js`、`index.html` 探索子樹、`explore.css`、`hw2/offline_scan.py`、V2 測試。BASE `450bcff` 的 `python -m pytest -q -rs`：442 passed。
2. **載入模組** `assets/explore_load.js`：`inspectCsv()`（`LoadResult`＋欄位清單，讓目標欄下拉在預設目標被拒時仍可重選；`loadCsv()` 的輸出不變）；重複欄名檢查改用 `Map`（R1-F2）；URL 入口 `checkUrl()`、`requestInit()`、`fetchCsvBytes()`——單元內唯一的 `fetch(` 在 `defaultFetch()`，`fetchImpl` 可注入。
3. **引擎** `assets/explore_engine.js`（R1-F2）：`fit.levels`、`fit.inputs`、`n_unseen_by_group` 以 `Object.defineProperty` 寫成自有屬性、以 `hasOwnProperty` 讀取（`putOwn`／`getOwn`）；`inputSpec()`、`predict()` 只讀自有屬性（或 `Map`）。物件仍是一般物件，結果契約的序列化不變。`ENGINE_VERSION` 改為 `explore-engine 2.1 (V2-T3: column names as own keys)`（只有欄名是 `Object.prototype` 成員時輸出不同）。
4. **控制器** `assets/explore_app.js`：`submitUrl()`、`submitData()`、`setTarget()`、`custom()`；離開自訂資料集或新提交時中止進行中的讀取並丟棄晚到的回應；每個拒絕原因與 URL 失敗的 zh-TW 訊息（`loadFailureText()`），URL 失敗附「下載後以本機 CSV 檔案載入」指引；`predictorView()` 以自有屬性傳值（R1-F2）。**更正（R1-F1）**：本點原本隱含 R1-F2 在頁面上已處理，並不成立——`e405bf1` 的頁面預測器在 `assets/explore_ui.js` 以一般物件指派收集輸入（`raw[x.spec.name] = …`），名為 `__proto__` 的欄的使用者輸入被靜默忽略；在 `c4256f5` 修正，見 §10。
5. **頁面**：`index.html` 的 `#ex-custom` 由佔位改為 URL 表單（「載入 URL」）、本機 CSV 檔案、預測目標欄下拉與狀態列；探索橫幅與「方法與限制」表的 Test 列改字（#75 R1-F3）。`assets/explore_ui.js`：面板呈現、`File.arrayBuffer()` 讀檔、表單 `submit` 一律 `preventDefault`、切換 problem 清空輸入。`assets/explore.css`：`body.is-exploring footer.footer { display: none !important; }`（R3-2、R3-5）與面板版面；移除不再使用的佔位樣式。
6. **靜態掃描** `hw2/offline_scan.py`：`FETCH_ALLOWED_FILE = "assets/explore_load.js"`；只有該路徑的 `fetch(` 不記 finding，其他網路 API、external-url 等規則照舊適用於該檔；`ALLOWED_DATA_URLS`、`DATA_FILES` 不變。
7. **測試**：新增 `tests/js/explore_custom.test.js`（16 項）；延伸 `tests/test_node_explore.py`（R1-F2 的兩個完整 case、兩個載入 case、Python 端斷言、登錄新 Node 檔）、`tests/test_explore_static.py`（`fetch(` 例外的掃描案例、唯一呼叫點、面板、頁尾規則、R1-F3 用語；原本「沒有 `fetch(`」的斷言改為排除載入模組，§4 D-9）。
8. **ACCEPTANCE**：新增 G 節 V2-18～V2-26；V2-7 與 V2-9 的「PENDING（#76）」改為指向新條目。其他條目不變。
9. **瀏覽器 self-verification**（§6.3）、對照與 H-5 探測（§6.4），證據在 `doc/screenshots/v2-issue76/`。

## 4. Decisions and assumptions

都在 accepted contract 的 HOW 範圍內；沒有改變 requirement、AC、invariant 或 gate。

| # | 決定 | 依據 |
| --- | --- | --- |
| D-1 | 請求選項恰為 `{ method: 'GET', credentials: 'omit', redirect: 'error', signal }`，沒有 `headers`、`mode`（預設 cors）等其他成員；一次提交只呼叫一次網路函式，沒有任何重試路徑；重新導向、跨來源拒絕與網路錯誤在瀏覽器中都是同一種例外，回報為子原因 `network`（訊息寫明三種可能） | DA D-1 第 1–3 點（「重新導向的結果以既有子原因之一回報，不新增原因碼」） |
| D-2 | 逾時 20 秒（`URL_TIMEOUT_MS = 20000`），以 `AbortController` 中止，子原因 `timeout`；逾時計時涵蓋讀取回應本文 | Spec「逾時」子原因；數字是實作常數，記於 ACCEPTANCE V2-21 |
| D-3 | 子原因 `not_text`＝回應本文含 NUL 位元組（二進位資料）。是文字但不是 UTF-8 的本文（例如 Big5）交給載入契約，結果為 `ENCODING`，與同一份位元組從本機檔案載入完全相同；不依 `Content-Type` 判斷，使同一內容經 URL 或檔案得到相同結果 | Spec「回應不是文字」未定義判定方式；Spec「內建、URL、檔案三種來源只是文字的入口」 |
| D-4 | 提交前檢查輸入：只接受含 scheme 的 `http:`／`https:` 完整網址，且不含帳號密碼；其他（空白、相對路徑、`javascript:`、`data:`、`file:`、`ftp:` 等）不發任何請求，在面板顯示改正提示。這是表單輸入檢查，不是載入契約的拒絕原因，沒有新增原因碼 | D-1「每次提交最多一個請求，對象就是提交的 URL」；H-1（不帶憑證）、H-5；Out of Scope「CSV 文字貼上輸入」（`data:` URL 等同貼上文字） |
| D-5 | 目標欄下拉列出全部欄位並標示數值／類別，預設最後一欄；選到類別欄得到 `TARGET_NOT_NUMERIC` 與重選提示且不執行；改選以記憶體中同一份內容重新執行，不重新讀取 URL。目標以欄序（index）指定，避免欄名比對 | Spec「目標：預設最後一欄；可指定任一欄…UI 以此提示使用者重選」；#76 AC「目標欄」 |
| D-6 | 自訂資料集的內容只留在控制器的記憶體中，離開自訂資料集即清除（中止讀取、清空輸入欄與檔案選擇）；再選自訂資料集是空白面板，需重新提交。讀取中切換 problem 或再次提交時，舊讀取被中止、其回應被丟棄，不會覆蓋目前的畫面 | Spec「再切回探索 problem 時…要求重新提交（自訂）」「探索結果不寫入任何儲存」；DA G-5；D-1 第 3 點（新的提交是新的一次讀取） |
| D-7 | 頁尾以 `explore.css` 的 `body.is-exploring footer.footer` 規則隱藏，不改頁尾 DOM／文字，`explore_ui.js` 不碰頁尾；切回 King County 移除 class 即還原 | DA R3-2、R3-5（「或 `explore.css` 中以 `body.is-exploring` 為前提的規則，與既有的導覽處理相同」） |
| D-8 | R1-F2 的修正方式：一般物件＋`Object.defineProperty` 自有屬性＋`hasOwnProperty` 讀取（而非 `Object.create(null)`），讓結果契約仍是原型為 `Object.prototype` 的一般物件、JSON 序列化與 Node 對 Python 的比較方式不變；載入的重複欄名檢查改用 `Map`。`e405bf1` 漏了頁面預測器的輸入收集（R1-F1）；`c4256f5` 改用 `Map`，`predict()`／`predictorView()` 本來就接受 `Map` | `audit/issue-74-c1-r1.md` §7 R1-F2 disposition（「以 `Map`、`Object.create(null)` 或自有屬性檢查取代一般物件鍵」） |
| D-9 | `tests/test_explore_static.py`（#74 的 V2 測試）原有斷言「V2 腳本沒有 `fetch(`」改為「除 `assets/explore_load.js` 外沒有」，並新增「全頁恰一處 `fetch(`、在載入模組、選項為 D-1」的測試。這是 #76 AC 要求的例外，不是放寬：其他檔案的檢查照舊，且多了唯一性與選項的檢查 | #76 AC「靜態掃描」；run designation（V2 測試可延伸）；DA I-5（V1 既有測試未改） |
| D-10 | 即時預測器的 `<form>` 加上 `submit` 的 `preventDefault`：所選候選只有一個數值輸入時，按 Enter 會觸發瀏覽器的隱式送出，使網址變成 `index.html?` 並重新載入回到 King County（`450bcff` 以 Chrome 155 實測，`predictor_enter_base_vs_subject.jsonl`）。這是 V2 UI 的修正，關係到本票 AC「探索結果不寫入 URL 參數」與「切換」；V1 的表單與程式未改 | #76 AC「不儲存」「切換」；Spec「探索結果不寫入任何儲存（…URL 參數…）」 |
| D-11 | #75 R1-F3：「方法與限制」Test 列改為「探索 test：每次執行探索時只對 CV winner 計算一次（選取候選或切換方法不會重算）、不保存，永遠不是 Test evaluation」；同一用語也出現在探索橫幅（「每次選取都在瀏覽器內重新計算」），一併改為「每次執行探索（選取 50 Startups，或提交自訂資料集）都在瀏覽器內重新計算」 | `audit/issue-75-c1-r1.md` R1-F3 與 §6 disposition；Spec「UI 的任何操作都不重算 test」 |

## 5. Artifacts

實作 commit `e405bf16a5fb008bbf8e3c4a626c9b6f650b1dfd`（10 個檔案，+1,077／−85，`git diff --shortstat 450bcff e405bf1`；全部在 `home_work_02/` 內，不含 `doc/`）：

- 修改：`assets/explore_load.js`、`explore_engine.js`、`explore_app.js`、`explore_ui.js`、`explore.css`、`index.html`（只在 `#explore` 子樹內）、`hw2/offline_scan.py`、`tests/test_node_explore.py`、`tests/test_explore_static.py`。
- 新增：`tests/js/explore_custom.test.js`。
- 不變：`assets/app.js`、`hw2core.js`、`model_data.js`、`style.css`、`vendor/`、`data/`、`results/`、`hw2.ipynb`、其他 `hw2/*.py`（含 `explore_reference.py`）、`tests/test_dashboard_static.py` 與其他既有測試、`tests/snapshots/`、`doc/spec/`、`doc/ticket/`、`doc/brief/`、`doc/requirement/`。

紀錄 commit：本 worklog；`doc/acceptance/ACCEPTANCE.md`（V2-18～V2-26；V2-7、V2-9 各一處指向）；`doc/screenshots/v2-issue76/`：八張截圖（Chrome，256 色量化）、`chrome_check.json`、`edge_check.json`（完整紀錄）、`chrome_summary.json`、`edge_summary.json`（摘要；Chrome 的含伺服器紀錄摘要）、`contrast_custom_panel.jsonl`、`predictor_enter_base_vs_subject.jsonl`。證據檔不含本機路徑；只出現 `127.0.0.1` 的測試網址與老師公開的範例 URL（H-1）。

## 6. Verification

### 6.1 自動測試

| 時點／subject | 指令 | 結果 |
| --- | --- | --- |
| BASE `450bcff`（修改前） | `.venv/Scripts/python -m pytest -q -rs`（Python 3.11.2） | 442 passed，52.86 s |
| 工作目錄＝`e405bf1`（`git status` 對 `home_work_02/` 只有尚未 commit 的 `doc/` 紀錄） | `.venv/Scripts/python -m pytest -q -rs` | **449 passed，0 skipped**，54.34 s（新增 7：Python 端 R1-F2 斷言 1、Node 次 seam 參數化 1（`explore_custom`）、靜態 5） |
| 同上 | `node --test --test-reporter=tap tests/js/<f>.test.js`（Node v24.19.0） | `explore_load` 15、`explore_boundary` 7、`explore_app` 12、`explore_methods` 7、`explore_custom` 16 pass；皆 0 fail、0 skipped |
| 同上，參照寫到 scratchpad 後直接執行 | `HW2_EXPLORE_REFERENCE=<dir> node --test tests/js/explore_contract.test.js` | **18 pass，0 fail，0 skipped**（原 16＋`objkey_names`、`objkey_numeric_proto`；載入對照含 `proto_names`、`duplicate_proto`） |
| 同上 | `node --test tests/js/core.test.js`（未設 fixture，直接執行） | 9 pass、0 fail、3 skipped——這 3 項需要 pytest 產生的 `HW2_FIXTURE_MODEL_DATA`；由 `tests/test_node_core.py` 驅動時斷言 `# skipped 0`，包含在上列 449 passed 中 |
| 同上 | `python -m hw2.offline_scan` | `scanned 13 files: PASS (0 findings)` |

`explore_custom.test.js` 的內容：提交 URL 恰一個呼叫、URL 相同、init 的鍵恰為 `credentials`／`method`／`redirect`／`signal`（值 GET、omit、error），之後改目標、等待都不再請求、全域 `fetch` 未被使用；`requestInit()` 的值；網路錯誤、HTTP 404、NUL 本文、網路函式拋出例外各為 `URL_FETCH_FAILED` 與對應 `detail`，訊息含「下載該 CSV」與「本機 CSV 檔案」，等待後呼叫數仍為 1，之後本機檔案載入成功；逾時（40 ms 注入）中止請求、`timeout_ms` 記錄、不再請求；Big5 本文經 URL 與經檔案的 `LoadResult` 相同（`ENCODING`）；八種非 http(s) 輸入不呼叫網路函式並顯示提示；目標欄預設最後一欄、類別欄 `TARGET_NOT_NUMERIC` 不執行、改選數值欄重跑、非法 index 不動作；七種拒絕原因與 `ENCODING`、列數上限各有不同 zh-TW 訊息；內建、URL、檔案位元組、檔案文字四種入口的確定部分逐值相同；切換 King County→50 Startups→自訂→King County 時讀取中止、晚到回應丟棄、再選自訂為空白；新提交取代進行中的提交（每次提交一個呼叫）；vm 中 storage／history／cookie 為陷阱、全部路徑存取 0 次；R1-F2 欄名的載入、引擎、預測器。

**Mutation 檢查**（scratchpad 的 `mutate.js`，每項改一處、跑對應測試、以原位元組還原並逐位元比對；全部 14 項被偵測，檔案還原後 md5 與修改前相同）：加自訂標頭、`credentials: 'include'`、`redirect: 'follow'`、失敗時再呼叫一次、把 URL 寫入 `localStorage`、不丟棄晚到回應、改目標時重新讀取、`inputSpec` 改回一般物件讀取、重複欄名檢查失效、`not_text` 檢查關閉 → `explore_custom.test.js` 失敗；掃描例外改以檔名結尾為鍵、例外放寬到全部網路 API、在控制器加 `fetch(`、刪除頁尾規則 → `test_explore_static.py` 失敗。另以 BASE 的 `explore_engine.js`、`explore_load.js` 跑新的對照 case：`duplicate_proto`、`objkey_names`（`folds[0].levels.__proto__` 缺失）、`objkey_numeric_proto`（`fit.inputs.__proto__` 缺失）三項失敗，修正後 18 pass。

### 6.2 不變量核對（A-3、I-5、CC-V2-1）

- `git diff --name-status 450bcff e405bf1`：10 個路徑全部在 `home_work_02/`；不含 `doc/`。
- `git diff --name-only d7f02d4 e405bf1 -- results hw2.ipynb assets/app.js assets/hw2core.js assets/model_data.js assets/style.css assets/vendor doc/requirement doc/spec doc/brief doc/ticket`：0 行。
- `git show e405bf1:<path> | sha256sum`：`assets/app.js` `c1ab3f21…`、`hw2core.js` `e75c5d48…`、`model_data.js` `6cf0c11e…`、`results/model_data.json` `69dc1465…`、`style.css` `60a27016…`，與 A-3 值相同。
- `hw2/` 自 `d7f02d4` 只有 `explore_reference.py`（#74 新增，本票未改）與 `offline_scan.py`（B-2）變更；`tests/test_dashboard_static.py` 自 `d7f02d4` 只有 CC-V2-1 的斷言（本票未改）；`tests/snapshots/` 未改。
- `tests/test_explore_static.py` 的 V1 快照、sha256、`git diff d7f02d4` 測試照常通過；`tests/test_repo_hygiene.py` 通過（學號）。
- 沒有重跑 notebook、沒有任何 Test evaluation。

### 6.3 瀏覽器（AC「輸入面板」「目標欄」「失敗訊息」「切換」「不儲存」；Executor self-verification）

- **方法**：scratchpad 的 `servers.py` 起兩個 `http://127.0.0.1` origin——頁面 origin（埠 8761）提供 `e405bf1` 的 `git archive` 匯出（`index.html`＋`assets/`）；第二個 origin（埠 8762）提供有／無 CORS 標頭的 50 Startups、302 重新導向、404、PNG 位元組、25 秒才回應、Big5 文字與各種被拒的 CSV，並記錄收到的每個請求（方法、路徑、Cookie、Authorization、Origin）。`check76.js` 以 DevTools Protocol 驅動 headless Google Chrome 155.0.8059.85 與 Microsoft Edge 155.0.4283.62（全新 profile），先造訪第二個 origin 的 `/setcookie` 讓瀏覽器持有 `127.0.0.1` 的 cookie，再開頁面。老師的範例 URL 使用真實網路。Windows 11 Pro 10.0.26200。這是 DA I-1 的 `http://localhost` 重現，**不是 GitHub Pages**；Pages 上的檢查屬合併後的 item（B-10）。伺服器與瀏覽器只以本 session 啟動的 PID 結束。
- **結果**（`chrome_summary.json`、`edge_summary.json`；兩個瀏覽器除計時外相同）：
  - 初次載入 King County：五個 V1 區塊與頁尾顯示。50 Startups 與自訂資料集：頁尾不顯示（R3-2）；切回 King County 後五個 V1 區塊與頁尾的 innerText 與初次載入逐字相同（每次切回皆是，共四次）。
  - 第二個 origin 的 CORS 50 Startups：一個 GET、無 Cookie 標頭；sha256 與內建相同、探索 test KPI「9,850／8,351／97,026,682／0.9399／100.0%」與內建逐字相同；目標欄預設 `Profit`。
  - 老師的範例 URL（`raw.githubusercontent.com`）：一個 GET（`type` Fetch），sha256 `c6075ca5…630d`、KPI 與內建逐字相同。
  - 目標欄：選 State →「預測目標欄「State」不是數值欄（TARGET_NOT_NUMERIC），沒有執行分析。…」，只顯示面板與資料區塊；選 Administration → 完成（KPI 改變）；三次改選新增請求 0。
  - URL 失敗：無 CORS、302 → `URL_FETCH_FAILED，network`；404 → `http_status`「HTTP 404 Not Found」；PNG → `not_text`；`/slow.csv` → `timeout`（Chrome 20.04 s、Edge 20.03 s 中止）；皆附下載後以本機 CSV 檔案載入的指引；Big5、NOT_CSV、NO_HEADER、RAGGED_ROWS、TOO_FEW_ROWS、TARGET_NOT_NUMERIC、DUPLICATE_COLUMN、TOO_LARGE 各為其 zh-TW 訊息；每次提交恰一個請求。`javascript:alert(1)`：提示「只接受 http:// 或 https:// 開頭的網址。」、請求 0。
  - URL 失敗後以檔案選擇 `50_Startups.csv`（`DOM.setFileInputFiles`）：完成，請求 0，sha256 與 KPI 與內建相同，來源列「本機 CSV 檔案：50_Startups.csv」。
  - 讀取中（`/slow.csv`）切到 King County：King County 逐字相同、探索區塊 0；再選自訂資料集：空白面板、目標欄停用。
  - 伺服器紀錄（兩個瀏覽器共 38 筆）：OPTIONS（preflight）0；頁面發出的讀取帶 Cookie 0、帶 Authorization 0（同一 host 的 `/favicon.ico` 導覽請求帶有該 cookie，證明 cookie 存在）；`/redirect.csv` 2 次（每個瀏覽器一次），其目標 `/cors/50_Startups.csv` 4 次＝明確提交的次數（每個瀏覽器以按鈕與 Enter 各一次），重新導向沒有被跟隨。
  - 不儲存：全部流程後 `localStorage`／`sessionStorage` 長度 0、網址與 `document.cookie` 不變；URL 欄按 Enter 只經頁面程式讀取一次、網址不變；即時預測器（k = 1，一個輸入）按 Enter 不再送出表單（D-10；BASE `450bcff` 會變成 `index.html?` 並回到 King County）。
  - OV-2：完成狀態下 375／768 px 水平溢出 0。OV-5（`contrast76.js`）：自訂資料集空白、URL 失敗、完成三種狀態，`#problembar`＋`#explore` 可見文字 17／18／358 處，低於門檻 0 處，最低 6.74:1（完成後 6.49:1），Chrome 與 Edge 相同。
  - 例外 0、console error 0、dialog 0；瀏覽器自身的錯誤 log 8 則都是失敗案例預期的訊息（CORS 封鎖、404、`net::ERR_FAILED`）。
- 截圖：`chrome_custom_teacher_url_localhost_1280.png`、`chrome_custom_url_localhost_1280.png`、`chrome_custom_target_not_numeric_1280.png`、`chrome_custom_url_fail_cors_1280.png`、`chrome_custom_file_1280.png`、`chrome_custom_h5_probe_file_1280.png`、`chrome_custom_url_375.png`、`chrome_kc_after_switching_1280.png`。目視沒有缺字方塊；探索模式的截圖底部沒有頁尾。
- 限制：headless 瀏覽器由 Executor 驅動，不是 acceptor 的人工操作；不是 GitHub Pages；真實觸控、螢幕閱讀器、Firefox／Safari 未測（AD-1 best-effort）。

### 6.4 H-5 探測（A-9 的同一風險；self-verification，不是 R1 證據）

以檔案選擇載入 scratchpad 的 `probe76.csv`：欄名 `<img src=x onerror="document.title=1">`、`</script><b>bold</b>`、`javascript:alert(1)`（類別）、`<style>body{display:none}</style>`（目標），類別值 `<svg onload=alert(1)>`、`"><iframe src=//evil.example>`、`a&amp;b`、`<script>alert(3)</script>`（RFC 4180 引號）。Chrome 與 Edge：`run = COMPLETED`；欄位表、目標欄下拉、預測器 label 與下拉、來源列（檔名）全部以字面文字顯示；`#explore` 內 img／svg／iframe／script／b／style 元素 0；`document.title` 不變；`body` 仍為 `display: block`；任何請求（含頁面 origin）0；切回 King County 逐字相同。新程式寫入 DOM 只用 `textContent`、`<option>.text`／`.value`、`disabled`；URL、檔名、HTTP 狀態文字都經 `textContent`；`tests/test_explore_static.py` 的 API 禁用清單照常通過。

## 7. Audit status

- Formal：本票 independent audit **required**（Bindings §5；治理 §4.1；DA derivation §7.4：H-1～H-5，A-1～A-5、A-7～A-9）。由 Orchestrator 依 Bindings §3.7 派工；本 worklog 不記錄 audit 結果。
- 以上 §6 全部是 Executor self-verification，不是 audit。

## 8. Remaining work and concerns

- **本票範圍內**：無未完成項目。GitHub Pages 上貼 URL 的檢查依 DA I-1／B-10 屬合併後的 item，ACCEPTANCE V2-18 記 NOT TESTED（pending merge）。
- **R3-5、#75 R1-F3**：已在本票處理（§4 D-7、D-11）。**#74 R1-F2**：原寫「已在本票處理」，在 `e405bf1` 並不完整（頁面預測器的輸入收集仍用一般物件鍵，#76 R1-F1）；R1-F1 的修正在 `c4256f5` 完成，證據見 §10，待 R2 核對。
- **觀察（給 Orchestrator／Reviewer／後續票，不需決定）**：
  1. 讀取的大小沒有位元組上限：載入上限（列、欄）在讀完之後才檢查；極大的 URL 回應或本機檔案會先整份讀入記憶體（URL 有 20 秒逾時）。資源保護屬 #77（Spec「資源保護」），本票未加新的拒絕條件。
  2. D-4 的輸入檢查（非 http(s) 完整網址不發請求）與 D-3 的 `not_text` 判定（NUL 位元組）是 Spec 未明定處的實作選擇，列出以便 R1 核對其與 D-1、H-5 的一致性。
  3. D-10 修正的是 #74 起就存在的 V2 預測器表單行為；V1 的表單未動。
  4. 引擎目前仍在瀏覽器主執行緒同步執行（非阻塞、取消屬 #77）；URL 讀取本身是非同步的。
- **Push**：未 push（OC §5.1 未授權）。

## 9. 執行時間

- 開始：2026-10-22 03:58（+08:00）；實作 commit `e405bf1`：約 04:14；最終瀏覽器檢查、ACCEPTANCE 與本 worklog：至約 04:30。
- 主要耗時：測試 `pytest` 每次約 54 s；瀏覽器檢查每個瀏覽器約 60 s（含 20 秒逾時案例）；mutation 檢查 14 項約 2 分鐘。

## 10. Cycle 1 targeted correction — R1-F1（2026-10-22）

- **來源**：`audit/issue-76-c1-r1.md` §6 R1-F1（Medium，blocking）與其要求的 targeted correction 1–4；Orchestrator 派工（同一 worklog identity、同一 Executor agentId `acd62ed3a70012296`），BASE `ce97221`。R1-F2 與 O-1～O-3 依派工不處理。
- **問題（我自己重現）**：`e405bf1` 的 `assets/explore_ui.js` `renderPredictor` → `update()` 以 `var raw = {}; raw[x.spec.name] = x.input.value;` 收集輸入；欄名為 `__proto__` 時呼叫的是 `Object.prototype.__proto__` 的 setter，字串值被丟棄，`predictorView()` 以 `getOwn` 讀到 `undefined` 而改用預設值（訓練中位數／基準層級），沒有任何警告。我的 Node 測試只以 `putOwn`／`Map` 建 `raw`，沒有走頁面的收集方式；我的瀏覽器探測沒有使用 `__proto__` 欄名。所以原本 V2-26 與 §3 第 4 點、§8 的 R1-F2 陳述超出了證據。
- **修正**（`c4256f54a8ece52ef71aff93a719f7d8db1604b6`，2 個檔案 +14／−2，`git diff --stat ce97221 c4256f5`）：
  - `assets/explore_ui.js`：`var raw = new Map(); inputs.forEach(function (x) { raw.set(x.spec.name, x.input.value); });`（`predictorView()` 與 `predict()` 已接受 `Map`）。我 grep 全部 V2 頁面腳本的 `obj[…] =` 寫入：這是唯一以使用者欄名作鍵的一般物件寫入；其餘的鍵都是陣列索引、候選鍵（如 `allin`、`forward_sfs_k01`）或方法名。
  - `tests/test_explore_static.py::test_exploratory_files_never_assign_a_computed_key_on_a_plain_object`（6 個 V2 腳本參數化）：鍵的運算式提到 name／group／level／header／column／target 的方括號寫入即失敗。對 `ce97221` 的 `explore_ui.js` 執行 → 1 failed（`raw[x.spec.name] =`）；`c4256f5` → 6 passed。這是靜態的防回歸，不是新 AC、不是新 seam。
  - 沒有其他修改：引擎、載入、控制器、`index.html`、CSS、`offline_scan.py`、其他測試未動。
- **Closure 與回歸證據（真實頁面路徑）**：scratchpad 的 `r1f1_page.js` 以 DevTools Protocol 驅動 headless Chrome 155.0.8059.85 與 Edge 155.0.4283.62（全新 scratchpad `--user-data-dir`），頁面由 `http://127.0.0.1:8761` 提供 `git archive c4256f5`（修正後）與 `git archive a4b6c76`（修正前）的匯出。流程：選自訂資料集 → 以檔案選擇（`DOM.setFileInputFiles`）載入 CSV → 按頁面的 All-in 方法按鈕 → 在預測器**自己的** `<input>`／`<select>` 改值並觸發 `input`／`change` 事件 → 讀頁面顯示的點預測與 PI。對照兩個參考值：(a) 同一頁的引擎以 `Map` 呼叫 `predictorView`，以頁面相同的數字格式化；(b) Node 以同一 CSV 位元組獨立執行載入＋引擎，以 `Map` 計算（相對 1e-9）。
  - 資料：`r1f1_numeric.csv`（數值 `__proto__`、`constructor`，y ≈ 4·`__proto__` + 10·`constructor`）、`r1f1_categorical.csv`（類別 `__proto__` = base／high／low，效果 0／+50／−50，與數值 `x`）；兩份都是合成資料，已放入證據目錄。
  - **修正後（`c4256f5`）**，Chrome 與 Edge 相同（`r1f1_chrome_fixed.json`、`r1f1_edge_fixed.json`）：數值 `__proto__` = 9 → 40.27（PI 39.7～40.83），= −9 → −31.31（−31.87～−30.74），之後 `constructor` = 0.9 → −26.9，`__proto__` = 2.5 → 18.83；9 與 −9 超出訓練範圍時顯示「__proto__ 的輸入超出訓練範圍…」警告（自有鍵被讀到的另一個跡象）。類別 `__proto__` = high → 59.72（58.52～60.91），low → −40.69，base → 9.48；`x` = 3 → 6.07。每一步頁面顯示＝(a)＝(b)；`__proto__` 每次改值，顯示都跟著改變。請求 0、例外 0。
  - **修正前（`a4b6c76`）**，Chrome（`r1f1_chrome_before.json`）：數值 `__proto__` = 9 與 −9 都顯示 3.47（2.96～3.98），參考值是 40.27 與 −31.31；類別 high／low 都顯示 9.48（基準層級的值），參考值是 59.72 與 −40.69；沒有警告。R1-F1 在頁面上重現，同一檢查在修正後通過。
- **測試與不變量**（工作目錄＝`c4256f5`）：`.venv/Scripts/python -m pytest -q -rs` **455 passed，0 skipped**（449＋新靜態測試 6 個參數）；Node 直接執行：`explore_load` 15、`explore_boundary` 7、`explore_app` 12、`explore_methods` 7、`explore_custom` 16 pass，皆 0 fail、0 skipped（`explore_contract` 與 `core` 由 pytest 驅動，包含在 455 中）；`python -m hw2.offline_scan`：13 files PASS（0 findings）。`git show c4256f5:<path> | sha256sum`：`app.js` `c1ab3f21…`、`hw2core.js` `e75c5d48…`、`model_data.js` `6cf0c11e…`、`results/model_data.json` `69dc1465…`、`style.css` `60a27016…`，與 A-3 相同；`git diff --stat ce97221 c4256f5` 只有上列兩個檔案，都在 `home_work_02/` 內。
- **紀錄的更正**（record-only，本次紀錄 commit）：ACCEPTANCE V2-26 的狀態改為以 `c4256f5` 為核對 subject，寫明 `e405bf1` 的 R1-F2 陳述只在 Node 路徑成立、頁面路徑在 R1-F1 修正後才成立，並加上頁面路徑證據；本 worklog 的檔頭、§3 第 4 點、§4 D-8、§8 加上更正。證據檔：`doc/screenshots/v2-issue76/r1f1_chrome_fixed.json`、`r1f1_edge_fixed.json`、`r1f1_chrome_before.json`、`r1f1_numeric.csv`、`r1f1_categorical.csv`（不含本機路徑；只有 `127.0.0.1` 網址）。
- **程序**：本機伺服器（PID 20112）與每個瀏覽器都只以我啟動的 PID 結束；瀏覽器一律使用 scratchpad 的全新 profile，沒有在 acceptor 的預設 profile 上啟動任何瀏覽器；結束後核對沒有殘留的監聽埠或我的 profile 的瀏覽器程序。
- **Binding**：agentId `acd62ed3a70012296`，`('claude-opus-5-5', 'high')`：256 則（截至寫入本節；單一元素；return 前由派工者全程核對）。
- **Audit status**：R1 BLOCKING（R1-F1）→ 本 correction → 待 R2（同一 Reviewer）。本節是 Executor self-verification，不是 closure。
- **時間**：約 04:35～04:55（+08:00）。
