# Worklog — #77 HW2 V2-T4（運算預算、非阻塞、取消、進度與可重現性）

- **Work item**：GitHub issue #77（V2-T4），Formal lane，run `run-20261022-hw2-v2-enhance`（Orchestrator＝root session `37216426-f292-44f9-bad1-e2d862e7b8f1`）。
- **執行角色**：Executor（治理 §2.1；`gov-executor`，有效 mapping `claude-opus-5-5`／`high`，Bindings b5 §3.1 O-1）。
- **Subject**：branch `home_work_02-v2-enhance`（未 push）。BASE `4bd6a5983d378ce4e353ac965638d4ec87835d09`（#76 結案後）；實作 commit `99e9d42`（主要實作與測試）、`8087083`（Lasso 表的停止用語，R4-2）與 `5219f89`（大型設計矩陣上更細的讓出點），最終實作 subject＝`5219f89`；之後的紀錄 commit 只改 `doc/`（本 worklog、`doc/acceptance/ACCEPTANCE.md` 的 V2-27～V2-34 與 V2-15 的一處指向、`doc/screenshots/v2-issue77/`）。Working tree 中 Orchestrator 未 commit 的 run record 修改未動、未 stage。
- **狀態**：實作與 self-verification 完成；independent audit（R1）待 Orchestrator 派工。

## 1. Contract reference

| 契約 | 位置與版本 |
| --- | --- |
| Outcome Contract | `doc/governance/outcome-contract.md` §5（V2 接受紀錄，接受基準 `d7f02d4`）、§5.2 CC-V2-1（只有 `test_page_loads_data_as_a_js_global_and_the_bundled_chartjs` 的 `<script src>` 斷言可改；本票沒有新增腳本檔，該斷言與 `tests/test_dashboard_static.py` 未動） |
| Ticket | GitHub #77（`gh issue view 77`，2026-10-22 讀取，OPEN，`ready-for-agent`）；AC 九項與結案證據 |
| Spec | `doc/spec/SPEC-V2.md` rev 2：「候選有效性、狀態與運算預算」（SR-V2-03：預算、非阻塞、可終止、資源保護、進度）、「Exploratory run 結果契約」、「可重現性」（SR-V2-04）、主 seam「取消與失敗」「可重現性」、人工檢查表（非阻塞與取消、可重現性、效能）；未提到的事項以 `SPEC.md` rev 5 為準 |
| Brief | `doc/brief/BRIEF-V2.md` rev 2＋E-1（§5.2 運算限制、§5.4、§5.5：逐方法預算、進度、四種狀態、All-in 優先嘗試但不保證） |
| Tickets Review | `doc/ticket/tickets-v2.md` 調整 B：取消在下一個候選邊界生效、執行中 UI 可操作、取消後不呈現部分結果、重跑從頭開始；非阻塞以 UI 實際可操作為準 |
| DA derivation | `decisions/derivation-SPEC-V2.md`：§4 #77 列（在 boundary 內，附 G-3、G-4）；§5.2 G-3（Chrome 與 Edge 各一次 50 Startups 確定部分，相對 1e-9，記錄不是 gate）、G-4（最終預算常數下 50 Startups 五種方法都完成，候選狀態與 #75 fixture 相同）；§7.4 #77：H-1～H-5，A-1～A-5、A-7～A-9；D-1（新提交時每次提交至多一次讀取）；D-2；I-5 |
| DA decisions | `decision-20261022-issue75-lasso-early-stop.md`：R4-2、R4-3、R4-4 由本票實作（R4-5），R4-1 的行為保持；`decision-20261022-r1f3-v1-footer.md`：R3-2（探索模式隱藏頁尾、切回 King County 還原）在切換與取消流程下保持 |
| 追蹤項目 | #76 R1 O-1（`audit/issue-76-c1-r1.md`）：URL 與檔案讀取沒有位元組上限；資源保護屬 #77（見 §4 D-10、§8） |
| Run invariants | run record §1 designation 第 4–7 點（經 CC-V2-1）：notebook、`hw2/` 正式路徑（`hw2/selection.py`、`tests/test_explore_kc_consistency.py` 不改，R4-3 約束 5）、`model_data`、`results/`、Test evaluation 紀錄、V1 區塊 DOM／文字／行為、V1 腳本與核心模組、`style.css`、既有測試不變（V2 測試可延伸）；不重跑 notebook、不做新的 Test evaluation；只有四個 seams，沒有 E2E 框架或 CI；追蹤檔案不含學號；只改 `home_work_02/` 且不碰 `doc/requirement/` |

## 2. Binding

| 對象 | 觀測（Bindings §3.6 指令，全部 assistant 訊息） | 結果 |
| --- | --- | --- |
| 本 assignment，agentId `a7b3c024fa9b13368`（`agentType` `gov-executor`） | `('claude-opus-5-5', 'high')`：319 則（截至寫入本節；return 前由派工者依 §3.6 全程核對） | 單一元素，等於有效 mapping；無 escalation、無替代 |

- Bounded assignments：**未使用**（沒有派 `gov-investigator`／`gov-bounded-worker` 或任何 subagent）。

## 3. Work performed

1. **讀取與基準**：Bindings b5、`gov-executor.md`、Implementation Profile §3–§5、§9、治理 §3.5、§3.7、§3.8；OC §5／§5.2；`gh issue view 77`；Spec V2 全文、Brief V2 §5、`tickets-v2.md`；DA derivation（§4、§5.2、§7、§8）、Lasso early-stop decision 全文、R1-F3 footer decision（R3-2、R3-5）；`audit/issue-76-c1-r1.md`（O-1）；run record §1；#74–#76 worklog；`assets/explore_*.js`、`hw2/explore_reference.py`、V2 測試。BASE `4bd6a59` 的 `python -m pytest -q -rs`：**455 passed**（54.8 s）。
2. **引擎** `assets/explore_engine.js`（`ENGINE_VERSION` → `explore-engine 3.0 (V2-T4: budgets, cancellation, unit-free paths)`）：
   - **逐方法預算**：執行前以訓練集編碼估計 `(預估 OLS 求解次數) × 訓練列數 × 編碼欄數²`；Forward／Backward／RFE 每組列 `p(p+1)/2` 次（O(p²)）、Lasso 每組列 `p` 步（O(p)），加每個 k 一次擬合，五個 fold 與整個訓練集各算一次；估計量 `>` 預算的方法整個 `SKIPPED_RESOURCE_LIMIT`（原因附 `estimate`、`budget`），完全不計算其路徑與候選；All-in 永遠最先嘗試、不被略過。`meta.budget` 記單位、常數、各方法估計量與矩陣大小（確定部分）。`options.budgets` 只供測試注入。
   - **失敗隔離**：任一方法（All-in 或路徑方法；路徑計算、候選擬合、記憶體配置失敗都算）的例外只讓該方法全部候選 `FAILED`，原因附 `error`、`message`、失敗時的 k 與環境資訊（user agent、邏輯處理器數、裝置記憶體、引擎版本；Node 為其 `navigator.userAgent`），其他方法照跑；共線診斷失敗寫入 `dependencies.error`。`FAILED`／`SKIPPED_RESOURCE_LIMIT` 沒有 CV 指標、fit、canonical 子集，不會是 winner。全部候選都非 `VALID` 時照 Spec 為 `REJECTED`／`ALL_CANDIDATES_INVALID`。
   - **分步執行與取消**：`createRun()` 回傳 stepper（`step()`／`cancel()`）；`run()` 同步跑完同一個 stepper。讓出點：每個 fold 擬合、每個路徑步、每次 LARS，以及在較大資料上每個 QR 欄步、Gram 列、LARS 迭代、診斷欄與 test 列區塊（`YIELD_CELLS = 2e5` 次乘加）。**取消只在候選邊界生效**：第一個候選之前、每個候選之後、每個略過或失敗的方法之後；讓出點不是取消點，候選中途不會被切斷。取消後 `run = { status: 'CANCELLED', methods_completed, methods_total, candidates_completed, candidates_total }`，結果只有 `meta` 與 `run`，沒有 `candidates`／`winners`／`test`，也沒有 `columns`、`groups`、`split`、`lasso_path`、`dependencies` 等部分結果。共線診斷移到最後一個候選邊界之後計算（不延遲取消）。
   - **進度**：`options.onProgress` 在開始、每個候選邊界與診斷前回報 `phase`、方法、k、已完成／總候選與方法數、比例、已耗時。
   - **確定／非確定部分**：`meta.timing_ms`（各方法耗時、`started_at_epoch_ms`）與 `FAILED` 的環境資訊是非確定部分；其餘逐值相同。
   - **R4-3／R4-4**：每組列的路徑準則都在「該組列上置中並除以其均方根」的目標上計算（尺度 0＝目標在這些列上沒有變化，此時不除）；exact LARS、RSS 與 `sd(X_g β_g)` 對縮放等變，進入順序不變，但 sklearn 的 equality tolerance 與 `TIE_RTOL` 的 `max(…, 1)` 下限都變成無單位。回報的 entry alpha＝縮放後的 alpha × 尺度；tie 叢集以縮放後的 alpha 判定。`TIE_RTOL` 值不變。
   - **R4-2**：停止原因如實回報：`active_set_degenerate`、`path_ended`（走到終點）、`alpha_increasing`、`max_iter`、`multiple_drops`、`target_constant`；R4-1 的處理（`INVALID_MODEL`／`lasso_path_degenerate`，不補齊）不變。
   - 實作細節：設計矩陣改為逐欄 `Float64Array`（配置失敗是一般例外，可被隔離）；即時預測器的數值預設（訓練 min／max／中位數）每次執行只算一次。
3. **Python 參照** `hw2/explore_reference.py`（`explore-reference 3`）：同一預算估計（與引擎相同的浮點運算順序）與略過；`canonical_paths()` 內以 `scaled_target()` 縮放；`lars_segment()` 另回報 sklearn 的數值停止（`Early stopping the lars path` 警告→`alpha_increasing`、迭代達上限→`max_iter`）；`target_constant`。`multiple_drops` 是 JS 引擎才有的停止（sklearn 無從觀察），照 DA R4-2 記錄差異，不另造 fixture。正式路徑（`hw2/selection.py` 等）未改，KC 一致性測試未改。
4. **控制器** `assets/explore_app.js`：頁面給 `schedule`（MessageChannel）時以 12 ms 時間片推進 stepper、片與片之間把控制權還給瀏覽器；沒有 `schedule`（#74–#76 的 Node 測試）時在呼叫內跑完，回傳值與行為同前。**一次只有一個執行**：新的選取、提交或改目標欄會先取消進行中的執行（在其下一個候選邊界生效），待它結束後才開始新的；等待中的多個請求只有最新的會開始；被取代的執行結果不顯示。`cancel()`：取消進行中的執行，其 `CANCELLED` 結果顯示「已取消」與已完成方法數；若有請求正在等待前一個停止，該請求不會開始，頁面立即顯示已取消。欄位清單在載入後、引擎執行前就提供給目標欄下拉（執行中可改選）。`deps.trace` 供測試觀察 start／cancel／end 事件。zh-TW 文字：進度、取消、各方法耗時、`SKIPPED_RESOURCE_LIMIT`／`FAILED` 原因與環境、六種停止原因（R4-2：只陳述已確立的事實，「走到終點」以「例如」列出可能情形，數值停止寫明是數值或上限造成）。
5. **頁面**：`index.html` 在 `#explore` 子樹新增 `#ex-run`（標「探索執行，非正式評估」的執行面板：`<progress>`、`role="status"` 的進度列、「取消執行」按鈕與說明；不是結果區塊）；`#ex-lasso-card` 的計算說明改為縮放與停止規則（R4-2）；「方法與限制」的 Lasso 退化列與新段落「運算預算、失敗與取消」。`assets/explore_ui.js`：執行中隱藏結果區塊、顯示執行面板、取消按鈕（「取消中…」）、`CANCELLED` 只顯示訊息、方法切換／k 格／比較表／原因標示 `SKIPPED_RESOURCE_LIMIT` 與 `FAILED`、完成訊息附各方法耗時。`assets/explore_plot.js`：叉號圖例改為「非 VALID 候選」。`assets/explore.css`：執行面板樣式。V1 區塊、頁尾、`style.css`、`app.js` 未動。
6. **測試**：新增 `tests/js/explore_run.test.js`（21 項）；延伸 `tests/test_node_explore.py`（新 case 與 Python 端測試，§6.1）、`tests/js/explore_contract.test.js`（注入預算、`meta.budget` 對照、略過／失敗的契約不變量）、`tests/test_explore_static.py`（4 項）。
7. **量測與瀏覽器 self-verification**（§6.2–§6.6），證據在 `doc/screenshots/v2-issue77/`。
8. **ACCEPTANCE**：新增 G 節 V2-27～V2-34；V2-15 加一處指向（#77 起的標示文字）。

## 4. Decisions and assumptions

都在 accepted contract 的 HOW 範圍內；沒有改變 requirement、AC、invariant 或 gate。

| # | 決定 | 依據 |
| --- | --- | --- |
| D-1 | **候選邊界**＝第一個候選之前、每個候選完成之後、每個被略過或失敗的方法之後。路徑方法的路徑計算（六組列）屬於該方法的第一個候選（k = 1）的工作，所以取消不會停在路徑計算與第一個候選之間。讓出控制權的點比候選邊界細得多，但只有候選邊界檢查取消。共線診斷與 test 在最後一個邊界之後計算；在那之後才提出的取消不再有邊界，執行照常完成 | Spec「取消請求在下一個候選邊界生效」；Tickets Review 調整 B；「不在候選中途中斷」 |
| D-2 | **預算量度與常數**：量度照 Spec 字面（預估 OLS 求解次數 × 訓練列數 × 編碼欄數²；Forward／Backward／RFE 以 O(p²)、Lasso 以 O(p)），求解次數含五個 fold 與整個訓練集的路徑和每個 k 的擬合；編碼欄數取整個訓練集的編碼（fold 的編碼欄不會更多）。判定為估計量 `>` 預算（等於時執行）。常數：Forward／Backward／RFE `2e11`、Lasso `8e10`，依 §6.5 的實測：參考機（i9-13900HX）上接近預算的資料各方法約 15～20 s 完成，超過的方法略過；50 Startups 的估計量（Forward 8.4e4、Lasso 4.8e4）遠低於常數（G-4）。常數是確定部分的一部分（`meta.budget`），與引擎版本一同決定可重現性 | Spec「運算預算」「數字由實作在參考環境實測後定，記錄於 ACCEPTANCE」；Brief §5.5 |
| D-3 | **FAILED 是整個方法**：例外發生在第 k 個候選或其路徑時，該方法 k = 1…p 全部 `FAILED`（已算出的候選捨棄），同一個原因。原因欄位：`rule: 'unexpected_error'`、`scope: 'method'`、`k`、`error`（例外名稱）、`message`、`environment`。All-in 失敗同樣只影響 All-in | Spec「任何方法的非預期例外（含記憶體不足）只讓該方法為 FAILED」；DA decision R4-1「FAILED 在 Spec 與 #77 是非預期例外、整個方法的狀態」 |
| D-4 | **CANCELLED 結果**只有 `meta`（確定的識別資訊與非確定的計時）與 `run`（狀態與完成數），其他鍵都不存在，所以任何部分結果都無從被呈現 | Spec「已算出的部分結果不呈現為結果…只顯示已取消與已完成的方法數」；契約不變量 |
| D-5 | **不並行的做法**：控制器保留「進行中」與「等待中（最新的一個）」兩個位置；新請求先取消進行中的執行，等它在候選邊界結束（`CANCELLED`）才開始，因此任何時刻最多一個執行在跑。被取代的執行的結果與進度都不顯示；它的 Promise 解析為 `null`。等待中按「取消執行」時，等待的請求不會開始，頁面立即顯示已取消 | Spec「引擎對同一輸入不並行啟動第二次執行（新的提交會先取消進行中的執行）」；#77 AC「不並行」 |
| D-6 | **非阻塞的技術**：主執行緒時間片（MessageChannel，12 ms）＋引擎讓出點；不使用 Worker（`Worker(` 在 V2 檔案的禁用清單中，Spec 不指定 Worker）。CSV 結構檢查與 sha256 在提交時於一個工作中完成（載入契約本身未改），列為量測項目（§6.3） | Spec SR-V2-03「具體技術由實作決定」；DA A-9 禁用清單 |
| D-7 | **R4-3／R4-4 的做法**：DA 舉例的「以同一批列計算的正值尺度除目標」——尺度＝置中目標在同一批列上的均方根，只取自該路徑的列（第三層：該 fold 的訓練列；canonical：整個訓練集），確定性；尺度為 0 時不除、Lasso 沒有 group 進入、原因 `target_constant`。Forward／Backward／RFE 的準則也在縮放後的目標上計算（R4-4 的「在 R4-3 縮放後的目標上計算全部準則」）。winner 比較不受影響 | DA decision R4-3 約束 1–6、R4-4 |
| D-8 | **R4-2 的用語**：`path_ended`：「路徑已走到終點：其餘 feature group 與殘差的相關在數值上為零，exact LARS 不會讓它們進入（可能的情形例如：…）」；數值停止三種各自寫明是數值計算或上限造成；Lasso 表的未進入標示由「未進入（退化後，只作展示）」改為「未進入（路徑停止後，只作展示）」，摘要的「另有 n 個 fold 的路徑退化」改為「…也在全部 group 進入前停止」（`8087083`），使「走到終點」不被說成退化 | DA decision R4-2（「走到終點」不得斷言共線或無變化；H-4） |
| D-9 | **載入上限的最終數字＝50,000 列 × 60 欄**（與候選值相同），依 §6.5 的實測：上限內的較大資料（50,000 列 × 35 個 group）All-in 1.5 s，路徑方法由預算決定是否執行；最壞情形（59 個各 20 層級的類別欄，編碼 1,121 欄）All-in 一律嘗試（Spec 不允許略過 All-in），參考機上單一 All-in 候選約 4.5 分鐘（Chrome），期間頁面仍可操作、King County 可用，但取消要等這個候選算完。是否以更低的上限換取較短的取消等待屬 Spec 與 acceptor 的取捨，我保留候選值並列為 concern（§8） | Spec「載入上限（候選值 50,000 列 × 60 欄；最終數字由實測後寫入實作常數）」「All-in 永遠優先嘗試執行」；Brief §5.5「不保證任何資料都能成功」 |
| D-10 | **#76 R1 O-1（讀取沒有位元組上限）不加位元組上限**：已接受的載入上限只有列數與欄數（`TOO_LARGE` 的定義），以位元組數拒絕一份列數與欄數都在上限內的檔案是新的拒絕條件，會改變載入契約，不在我的 HOW 範圍內。我量測現況（§6.5）並把是否增設位元組上限列為需 Design Authority 判定的 concern（§8） | Spec「載入契約」大小一條；DA derivation B-9（不得自行新增拒絕條件）；治理 §1.2 |
| D-11 | **V2 測試的修改都是延伸**：`tests/js/explore_contract.test.js` 只增加注入預算的參數、`meta.budget` 的比對，以及略過／失敗候選與「Lasso 被略過時沒有 `lasso_path`」的不變量；`tests/test_node_explore.py::test_reference_cases_meet_the_contract_invariants` 的狀態集合加入 `SKIPPED_RESOURCE_LIMIT` 並在 Lasso 被略過時改為檢查其候選皆為略過——兩者對既有 case 的檢查不變，沒有放寬任何期望值。接受基準的既有測試（I-5）與 #74–#76 的其他 V2 測試未改 | DA decision R4-5（V2 測試只能擴充，期望值修改須說明且不得削弱）；I-5 |
| D-12 | `exact_fit`（y＝2·x1＋3）的 test 區間寬度為 0，`covered` 在兩種語言間不是穩定的 oracle，所以不放進 Node 對 Python 的 case，而是兩側各自測試其停止原因與狀態 | 主 seam 的比對只對可比對的量；R4-2 的驗證 |

## 5. Artifacts

- 實作 commit `99e9d42`（11 個檔案）、`8087083`（`assets/explore_app.js`，2 行）與 `5219f89`（`assets/explore_engine.js`）：修改 `assets/explore_engine.js`、`explore_app.js`、`explore_ui.js`、`explore_plot.js`、`explore.css`、`index.html`（只在 `#explore` 子樹內）、`hw2/explore_reference.py`、`tests/js/explore_contract.test.js`、`tests/test_node_explore.py`、`tests/test_explore_static.py`；新增 `tests/js/explore_run.test.js`。`git diff --shortstat 4bd6a59 5219f89`：11 個檔案，+1,614／−224。
- 不變：`assets/app.js`、`hw2core.js`、`model_data.js`、`style.css`、`vendor/`、`data/`、`explore_load.js`、`results/`、`hw2.ipynb`、`hw2/` 其他模組（含 `selection.py`、`offline_scan.py`）、`tests/test_explore_kc_consistency.py`、`tests/test_dashboard_static.py` 與其他既有測試、`tests/snapshots/`、`doc/spec/`、`doc/ticket/`、`doc/brief/`、`doc/requirement/`。
- 紀錄 commit：本 worklog；`doc/acceptance/ACCEPTANCE.md`；`doc/screenshots/v2-issue77/`（§6 列出的 JSON、截圖與 TAP 輸出；不含本機路徑，只有 `file://` 匯出頁面的相對檔名與合成資料的檔名）。

## 6. Verification

### 6.1 自動測試

| 時點／subject | 指令 | 結果 |
| --- | --- | --- |
| BASE `4bd6a59`（修改前） | `.venv/Scripts/python -m pytest -q -rs`（Python 3.11.2） | 455 passed，54.8 s |
| 工作目錄＝`5219f89`（`git diff --quiet 5219f89 -- assets hw2 tests index.html`；只有本票未 commit 的 `doc/` 紀錄與 Orchestrator 的 run record） | `.venv/Scripts/python -m pytest -q -rs` | **470 passed，0 skipped**，55.7 s（新增 15：Node 次 seam 參數化 1（`explore_run`）、R4-3 單位 5、exact fit、`max_iter`、`target_constant`、budget skip、G-4 各 1、靜態 4） |
| 同上 | `node --test --test-reporter=tap tests/js/<f>.test.js`（Node v24.19.0） | `explore_load` 15、`explore_boundary` 7、`explore_app` 12、`explore_methods` 7、`explore_custom` 16、`explore_run` **21** pass；皆 0 fail、0 skipped。`explore_run` 的 TAP 輸出存於 `doc/screenshots/v2-issue77/explore_run_tap.txt` |
| 同上 | `explore_contract.test.js`（由 pytest 以即時產生的 Python 參照驅動） | 包含在 470 中；新增 case `startups50_x1e-12`、`startups50_x1e-10`、`startups50_x1e6`、`budget_skip`，`meta.budget` 逐值比對 |
| 同上 | `python -m hw2.offline_scan` | `scanned 13 files: PASS (0 findings)` |

`explore_run.test.js` 的內容：注入小預算使 Forward 與 Lasso 略過——以 hooks 計數，兩者路徑、候選、擬合 0 次，其餘候選與未注入時逐值相同、winner 只來自執行過的 `VALID`；同一輸入在競速時鐘與停止時鐘下確定部分相同、估計量＝預算時執行、減 1 時略過；G-4；RFE 在 k = 2 拋出 `RangeError` → RFE 全部 `FAILED`，其他與未注入相同；路徑計算中、All-in fold 3 中、全部方法失敗（→ `REJECTED`）；在第 0、1、2、5、9、16 個候選後取消 → `CANCELLED` 且開始的候選數恰為 n、沒有任何部分結果鍵；在 Backward k = 2 的 fold 1 中途取消 → 該候選的五個 fold 與訓練集擬合全部完成後停止（1＋4＋2 個候選）；取消後重跑從 All-in 開始、17 個候選、確定部分與未取消相同；進度事件單調、`skipped` 一次、最後是 `diagnostic` 且比例 1；50 Startups 與混合資料兩次執行 `deepStrictEqual`；R4-3／R4-4：50 Startups 與混合資料目標 × 1e-12、1e-10、1e-9、1e-6、1e6 的狀態、子集、fold 子集、原因、停止、winner 相同、alpha 相對誤差 ≤ 1e-9；完全擬合 `path_ended` 與頁面文字；`target_constant`；排程控制器：時間片多於候選數、結果與立即模式相同；新提交取代進行中的執行（事件 `start 1 → cancel 1 → end 1 CANCELLED → start 2 → end 2 COMPLETED`、任何時刻至多一個）；連續兩個請求只有最新的開始、URL 一次讀取；「取消執行」→ `CANCELLED` 只有完成數、之後重跑完整；等待中取消 → 等待的請求不開始；切到 King County → 取消且不再顯示探索內容；執行中改目標欄 → 前一次 `CANCELLED`、新目標完成、不重新讀取 URL；三種入口確定部分相同。

**#74–#76 V2 測試的修改**（全部是延伸，§4 D-11）：`explore_contract.test.js` 新增 `budgets` 參數、`meta.budget` 比對與略過／失敗的不變量；`test_node_explore.py::test_reference_cases_meet_the_contract_invariants` 的狀態集合加入 `SKIPPED_RESOURCE_LIMIT`、Lasso 被略過時改查其候選皆略過。其他 V2 測試與接受基準的既有測試未改。

### 6.2 不變量核對（A-3、I-5、CC-V2-1、R4-3 約束 5）

- `git diff --name-status 4bd6a59 5219f89`：11 個路徑，全部在 `home_work_02/`，不含 `doc/`；`git diff --name-only 4bd6a59 5219f89 -- tests/test_explore_kc_consistency.py tests/test_dashboard_static.py hw2/selection.py doc`：0 行。
- `git diff --name-only d7f02d4 5219f89 -- results hw2.ipynb assets/app.js assets/hw2core.js assets/model_data.js assets/style.css assets/vendor doc/requirement doc/spec doc/brief doc/ticket hw2/selection.py`：0 行（另列出的 `tests/snapshots/`、`test_dashboard_static.py`、`test_explore_kc_consistency.py` 是 #74、#75 已審的變更，本票未動）。`hw2/` 自 `d7f02d4` 只有 `explore_reference.py` 與 `offline_scan.py`（#76）變更。
- `git show 5219f89:<path> | sha256sum`：`app.js` `c1ab3f21…`、`hw2core.js` `e75c5d48…`、`model_data.js` `6cf0c11e…`、`results/model_data.json` `69dc1465…`、`style.css` `60a27016…`，與 A-3 相同。
- 沒有新增腳本檔（`<script src>` 斷言未動）；沒有重跑 notebook、沒有 Test evaluation；`tests/test_repo_hygiene.py` 通過（學號）。

### 6.3 瀏覽器：非阻塞與取消（AC「非阻塞與取消」；ACCEPTANCE V2-30）

- **方法**：scratchpad 的 `check77.js` 以 DevTools Protocol 驅動 headless Google Chrome 155.0.8059.85 與 Microsoft Edge 155.0.4283.62（每次全新的 scratchpad `--user-data-dir`；`file://`、網路模擬離線、所有 host 無法解析），頁面為 `git archive 5219f89` 的匯出（`index.html`＋`assets/`）。以 `Input.dispatchMouseEvent`／`dispatchKeyEvent` 送真實輸入事件；頁內以事件 `timeStamp` 量輸入延遲、`requestAnimationFrame` 量畫格間隔、`PerformanceObserver('longtask')` 量長任務；以 `DOM.setFileInputFiles` 選檔。參考機：13th Gen Intel Core i9-13900HX（24 核／32 執行緒）、31.7 GB、Windows 11 專業版 10.0.26200。每個瀏覽器只以本 session 啟動的 PID（`taskkill /PID <pid> /T /F`）結束，沒有在 acceptor 的預設 profile 上啟動任何瀏覽器。
- **資料**：合成 `medium.csv`，20,000 列 × 26 欄（`x0`～`x19` 數值、`c0`～`c4` 各 10 層級、目標 `y`），2,725,065 bytes，sha256 `0f4ef1d3882582dc63cb85b651ac2440581e3b036d10b4ca64a449fecd6e4a64`；以 mulberry32(7) 產生（數值＝12 個均勻數和減 6 乘 10、四捨五入到 0.01；y＝50＋係數×數值＋層級效果＋雜訊×5）。只存配方與雜湊，不存檔。
- **結果**：見 ACCEPTANCE V2-30（`chrome_subject_medium.json`、`edge_subject_medium.json`）。重點：執行中輸入延遲最大 13.7／13.6 ms，畫格 p95 16.7 ms，long task 只有提交時的一個（130 ms，CSV 結構檢查與 sha256）；取消 102／103 ms 內回應、232／291 ms 內停在第 26 個候選之後；`CANCELLED` 畫面只有訊息與輸入面板；重跑自 0 開始，19.8／19.9 s 完成，101 個候選 `VALID`。
- **改進的經過**（同一 session 的 working tree 預檢，未當作證據）：第一版只在每個 fold 擬合後讓出，Chrome 量得畫格 p50 58 ms、long task 113 個（最大 212 ms）、輸入延遲最大 194 ms；把讓出點細化到 QR 欄步、Gram 列、LARS 迭代並快取預測器預設值後，降為 p50 12.5 ms、long task 1 個。這是我自己的 HOW 調整，結果契約不變（確定部分與先前相同）。
- **限制**：headless 瀏覽器由 Executor 驅動，不是 acceptor 的人工操作；headless 不會出現「網頁沒有回應」對話框，以長任務與畫格間隔作為替代證據（dialog 事件 0）；原生下拉的彈出視窗在 headless 中以點擊後焦點與 Esc 關閉、值不變驗證。

### 6.4 瀏覽器：其他檢查（ACCEPTANCE V2-31～V2-34）

- **50 Startups 兩次**（`*_startups.json`）：Chrome／Edge 兩次的顯示 KPI 與確定部分相同；17 個候選 `VALID`；請求 0。
- **G-3**（`g3_*.json`）：Chrome 與 Edge 的 50 Startups 確定部分 2,402 個數值、中型資料 281,417 個數值全部位元相同；Chrome 對 Node 24：50 Startups 2,377／2,402 位元相同、最大相對差 1.7e-15（Math 函式的實作差異），中型資料全部相同。記錄，不是 gate。
- **R4-2／R4-3 頁面路徑**（`*_units.json`；資料 `s50_x1e-10.csv` sha256 `d60fda8e…ee83`、`exact_fit.csv` `1a1fcd02…aedd` 已存於證據目錄）：見 ACCEPTANCE V2-33。BASE `4bd6a59` 的同一檢查（`chrome_base_units.json`）重現 R1-F1 的問題，subject 修正。
- **H-5 探測**（`*_probe.json`；#76 的 `probe76.csv`）：Chrome／Edge `COMPLETED`，`#explore` 內 img／svg／iframe／script／b／style 0、標題不變、請求 0。本票新增的文字（進度、取消、原因、耗時）只含方法名稱、數字與引擎訊息，全部經 `textContent` 寫入；`test_exploratory_files_write_no_markup_and_run_no_strings` 照常通過。
- **SR-09 量測**（`*_kc.json`，BASE 與 subject 同一 session）：見 ACCEPTANCE V2-34；沒有退步。量測限制：腳本送出的滾輪與拖曳在兩個版本都沒有被頁面的 `HW2_PERF` 記錄到，正式 gate 在 #78。
- **執行面板 OV-2／OV-4／OV-5**（`*_ov.json`、`chrome_subject_run_panel_375.png`）：見 ACCEPTANCE V2-34。
- **極大資料**（`chrome_subject_heavy.json`）：見 ACCEPTANCE V2-32 與 §6.5。
- 全部檢查：dialog 0、例外 0、非 `file:` 請求 0。

### 6.5 量測：預算常數、載入上限與讀取大小

- **預算常數**：Node（`measure.js`，預算設為無限大以量測每個方法）9 種規模見 `node_budget_table.jsonl`；Chrome（`chrome_subject_time.json`）：10,000 列（編碼 43 欄、19 group；Forward 估計 1.85e10）各方法約 1.0 s；中型（1.42e11）約 4.6～5.1 s；50,000 列 × 7 個 20 層級類別（Forward 1.49e11、Lasso 5.94e10）Forward 16.3 s、Lasso 19.9 s；50,000 列 × 10 數值＋4 類別（Forward 2.11e11）Forward／Backward／RFE 略過、Lasso 13.2 s。量度對 group 數多的資料偏保守（例如 5,000 列 × 59 group 估計 1.95e12、實際約 24 s），對 group 數少、編碼欄多的類別資料每單位最慢（約 0.11 ns），常數依後者定：在參考機上，不被略過的方法約 20 s 內完成。
- **載入上限**：最壞情形（50,000 列 × 59 個 20 層級類別）All-in 單一候選在 Chrome 約 4.5 分鐘（Node 只跑 All-in 與診斷 395 s，單一步驟最長 361 ms），頁面仍可操作（V2-32）；較大的一般資料（50,000 列 × 35 group、編碼 75 欄）All-in 1.5 s；不設預算時全部方法約 90 s，在最終預算下四個路徑方法的估計量（8.98e11、9.45e10）都超過預算而略過，只有 All-in 有結果——這是「不承諾所有方法都能在載入上限的規模完成」（Brief §5.2）的實例。最終數字維持 50,000 × 60（D-9）。
- **#76 R1 O-1（讀取大小）**：Node 以同一載入程式量測（`bigread.js`）：114 MB、400,000 列 × 30 欄 → 讀完後在解析中以 `TOO_LARGE`（列數）拒絕，1.7 s（一個工作）；95 MB、40,000 列 × 60 欄（每格 40 字元，在上限內）→ 載入成功，4.3 s，heap 約 2.4 GB。瀏覽器中這段時間是提交時的一個長任務，極大的檔案可能耗盡分頁記憶體。我沒有加位元組上限（D-10），列為 concern。

### 6.6 Self-review

- 對照 #77 AC 九項逐條（ACCEPTANCE V2-27～V2-34）；DA G-3、G-4、D-1、R4-2～R4-4、R3-2 各有證據位置。
- 以 diff 逐檔重看：引擎的讓出點只是 `yield null`，不改計算順序；取消只在 `runSteps` 的四個邊界檢查；`FAILED`／`SKIPPED` 的候選結構與契約不變量一致；控制器的立即模式與 #74–#76 相同（舊測試未改且通過）；V2 檔案沒有 `innerHTML` 等禁用 API、沒有以欄名作一般物件鍵的寫入（靜態測試通過）。
- 品質下限：沒有刪除或跳過任何測試、沒有降低容忍度；兩處 V2 測試的修改見 D-11。

## 7. Audit status

- Formal：本票 independent audit **required**（Bindings §5；治理 §4.1；DA derivation §7.4：H-1～H-5，A-1～A-5、A-7～A-9）。由 Orchestrator 依 Bindings §3.7 派工；本 worklog 不記錄 audit 結果。
- §6 全部是 Executor self-verification，不是 audit。

## 8. Remaining work and concerns

- **本票範圍內**：沒有未完成的實作或驗證。Pages 上的檢查不屬本票（B-10）。
- **Concern C-1（需要 Design Authority；可能需 acceptor）— 最壞情形的取消等待**：All-in 依已接受語義一律嘗試、不可略過，取消只在候選邊界生效；載入上限 50,000 × 60 下，全部欄都是 20 層級類別欄時 All-in 單一候選在參考機約 4.5 分鐘（V2-32），這段期間頁面可操作、King County 可用，但按取消或改選資料都要等它算完（新的執行在它停止後才開始）。可選的處置（例如較低的載入上限、或把 All-in 的設計矩陣大小納入執行前的拒絕）都會改變 accepted 的上限數字的取捨或新增拒絕條件，不在我的 HOW 範圍內；我照 Spec 以實測定下的候選值，並如實記錄。
- **Concern C-2（需要 Design Authority）— #76 R1 O-1 讀取大小**：URL 與本機檔案仍是整份讀入後才檢查列數與欄數；95 MB 但在上限內的檔案在 Node 用到約 2.4 GB heap、4.3 s（§6.5）。增設位元組上限是新的 `TOO_LARGE` 條件（D-10），請 DA 判定是否在 boundary 內、或維持現狀並記為已知限制。
- **觀察（不需決定）**：(1) 提交時的 CSV 結構檢查與 sha256 在一個工作中完成（中型資料約 130 ms）；載入契約未改。(2) 預算量度照 Spec 字面，對 group 多的資料偏保守（V2-27），50,000 列 × 35 group 的資料四個路徑方法都會略過。(3) `multiple_drops` 只在 JS 引擎可能出現（D-8／§3 第 3 點）。(4) #78 的 README／報告須說明 R4-1～R4-4 的實作行為（DA R4-5）並帶入預算常數與載入上限（I-4）；SR-09 的滾輪與拖曳量測留給 #78 的正式 gate。
- **Push**：未 push（OC §5.1 未授權）。

## 9. 執行時間

- 開始：2026-10-22 05:04（+08:00，BASE pytest）；實作 commit `99e9d42` 約 05:35、`8087083` 約 05:40、`5219f89` 約 06:35；最終瀏覽器檢查、ACCEPTANCE 與本 worklog：至約 07:00。
- 主要耗時：pytest 每次約 56 s；中型資料每個瀏覽器約 1.5 分鐘；極大資料（Chrome）約 11 分鐘；Node 的預算量測表約 6 分鐘、只跑 All-in 的極大資料約 7 分鐘。
