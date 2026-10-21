# Audit record — #77 HW2 V2-T4，cycle 1，R1

- **Audit 種類**：Ticket independent audit，**R1**，cycle 1（治理 §4.4；Bindings b5 §5 Formal）。**本 record 不是 Spec Integration Audit**（Spec V2 有五張票，DA derivation §6 已判定不適用單 Ticket fast path）。
- **角色**：`primary_reviewer`（Primary Independent Reviewer；definition `gov-primary-reviewer`）。
- **Run**：`run-20261022-hw2-v2-enhance`（Orchestrator＝root session `37216426-f292-44f9-bad1-e2d862e7b8f1`）。
- **Work Contract**：GitHub issue #77（我以 `gh issue view 77 --json body -q .body | sha256sum` 重算 body sha256 `c9b79356313a2ae587fe0f679c6fb680fe57abba67ec1ca7a54605d655ca90fe`，等於 DA derivation §3 記錄的 accepted 版本；OPEN、`ready-for-agent`）；Outcome Contract `doc/governance/outcome-contract.md` §5（V2 接受，基準 `d7f02d4179d2cb5c2ecf0c39a4643a6ef8287907`）與 §5.2 CC-V2-1；Spec V2 rev 2（`doc/spec/SPEC-V2.md`，特別是「候選有效性、狀態與運算預算」SR-V2-03、「Exploratory run 結果契約」、「可重現性」SR-V2-04、主 seam「取消與失敗」「可重現性」、人工檢查表；未提到者以 Spec rev 5）；Brief V2 rev 2＋E-1（§5.2、§5.5）；`CONTEXT.md`；`doc/ticket/tickets-v2.md`（Tickets Review 調整 B；非阻塞以 UI 實際可操作為準）。DA 紀錄：`decisions/derivation-SPEC-V2.md`（#77 列、§5.2 G-3、G-4、§7.4 #77：H-1～H-5，A-1～A-5、A-7～A-9、D-1、D-2、I-5）；`decision-20261022-issue75-lasso-early-stop.md` R4-2～R4-4（分配給 #77）與 R4-1（保持）；`decision-20261022-r1f3-v1-footer.md` R3-2（保持）；**`decision-20261022-issue77-resource-limits.md`**（C-1／C-2 的裁決；審查進行中由 Orchestrator 通知，commit `7fa9bef`，record-only，我自行讀取全文並作為本 audit 適用的 decision）。分配給 #77 的 tracked item：#76 R1 O-1（`audit/issue-76-c1-r1.md`）。Run invariants：run record §1 designation 第 4、5、7 點（經 CC-V2-1）。
- **受審 subject**：branch `home_work_02-v2-enhance`，subject **`9d5a840727bf64627c65fa0e81cdfced5735a091`**；BASE `4bd6a5983d378ce4e353ac965638d4ec87835d09`。實作 commit `99e9d42`、`8087083`、`5219f89`（最終實作；`git diff 5219f89 9d5a840 -- assets hw2 tests index.html` 為空）；`9d5a840` 只加 worklog、ACCEPTANCE V2-27～V2-34（與 V2-15 一處指向）與 `doc/screenshots/v2-issue77/`。`git diff --stat 4bd6a59 9d5a840`：46 個路徑，全部在 `home_work_02/` 內，沒有 `doc/requirement/`。審查期間 HEAD 先後為 `8797e2f`、`7fa9bef`，對 subject 只差 run record 與 DA decision record（record-only paths，Bindings §7）；working tree 的程式、資料與測試與 subject 相同（`git diff --name-only 9d5a840 -- home_work_02` 只有 run record）。

## 1. Assurance

### (a) Context independence（治理 §2.3；Bindings §3.7）

| Property | 滿足方式 |
| --- | --- |
| Independent context | Orchestrator 以 Agent tool 派工非 fork 的 `gov-primary-reviewer` subagent，從空白 context 開始，不繼承 Executor（agentId `a7b3c024fa9b13368`）的對話或推理。派工內容是路徑、識別與 SHA；worklog、ACCEPTANCE、evidence JSON 與派工中的陳述一律當作待驗證主張，以原始檔案、git 歷史、我自己執行的測試、獨立重算、我自己的 Node 探測與瀏覽器檢查驗證。我沒有執行 Executor 在 scratchpad 留下的腳本；我的工具全部在 scratchpad 的 `r77/` 子目錄內新寫 |
| Verifiable binding | 本 assignment：agentId `ab93f858531ba9d08`，`agentType` `gov-primary-reviewer`；以 Bindings §3.6 指令讀取自己的 transcript，寫本 record 前觀測到 `('claude-opus-5-5', 'xhigh')` 137 則，單一元素，等於有效 mapping R-PR（Opus 5.5／`xhigh`）；沒有 escalation、沒有替代。全程核對（含之後的訊息）由派工者依 §3.6 在採用 return 前執行；本 record 不自證 binding |
| Autonomous access | 自行讀取 repo、`git log／show／diff／archive／grep`（不做 git 寫入）、GitHub（issue body 與 sha256）、Executor transcript 的 model 欄位（只讀 binding，不讀內容）；自行執行 pytest、Node 測試、`offline_scan`、Python 獨立重算、Node 探測與 headless Chrome／Edge（DevTools Protocol）檢查 |
| Self-written record | 本 record 由我以自己的 Write 工具寫入 Bindings §7 的位置；派工者只能原樣 commit |

### (b) Model diversity（Bindings §5；治理 §4.6 V22-17）

| Assignment | 實際 model（transcript 觀測，我自己以 §3.6 指令讀取） |
| --- | --- |
| Executor，agentId `a7b3c024fa9b13368`（`gov-executor`） | `claude-opus-5-5`／`high`（324 則，單一元素；與 run record 第 14 列相同） |
| Primary Reviewer（本 R1），agentId `ab93f858531ba9d08` | `claude-opus-5-5`／`xhigh`（137 則，單一元素） |
| Alternate Reviewer | 尚未派工 |

**無 model diversity**（Executor 與 Primary 同為 `claude-opus-5-5`）。依 Bindings §5 與 DA A-8，不宣告 diversity 關係，不影響 independence 判定。

### Capability escalation

不提出。

### 審查環境的操作

- 瀏覽器只以我啟動的程序執行：headless Chrome 155.0.8059.85（PID 10048）與 Edge 155.0.4283.62（PID 2168），各自使用 scratchpad `r77/prof_chrome`、`r77/prof_edge` 的全新 `--user-data-dir`，從未使用 acceptor 的預設 profile，也沒有執行 `chrome.exe --version` 一類會開啟預設 profile 的指令；結束時各以 `taskkill /PID <pid> /T /F` 停止，之後以 `Get-CimInstance Win32_Process` 核對沒有任何使用這兩個 profile 的殘留程序。
- 頁面是 `git archive 9d5a840 home_work_02/index.html home_work_02/assets` 的匯出（`file://`），網路以 DevTools 模擬離線。
- 沒有修改任何追蹤中的檔案；`git status --short` 只有審查前就存在的未追蹤項目。

## 2. CC-V2-1、既有測試與正式分析不變量（I-5；A-3；designation 第 4 點）

- 對 `git ls-tree -r --name-only d7f02d4 -- home_work_02/tests` 的每個檔案執行 `git diff --quiet d7f02d4 9d5a840`：唯一不同的是 `tests/test_dashboard_static.py`（#74 的 CC-V2-1 斷言，已由 #74 R1 核對）；`git diff --name-only 4bd6a59 9d5a840 -- home_work_02/tests` 只有 V2 測試（`explore_contract.test.js`、`explore_run.test.js`（新增）、`test_explore_static.py`、`test_node_explore.py`）。**本票沒有改動任何接受基準的既有測試。**
- V2 測試的兩處既有斷言修改（worklog D-11）：`test_reference_cases_meet_the_contract_invariants` 的狀態集合加入 `SKIPPED_RESOURCE_LIMIT`，並在 Lasso 被略過時改查其候選皆略過；`explore_contract.test.js` 在 `lasso_path` 為 `null` 時只允許 Lasso 沒有執行。對既有 case 的檢查不變（既有 case 以正式常數執行，G-4 測試另以 `["VALID"] * 17` 鎖定 50 Startups），沒有放寬期望值，符合 R4-5 的「只能擴充」。
- A-3：`git show 9d5a840:<path> | sha256sum`：`assets/app.js` `c1ab3f21…82ad`、`assets/hw2core.js` `e75c5d48…2c14`、`assets/model_data.js` `6cf0c11e…a7ac`、`results/model_data.json` `69dc1465…6e61`（＝Test evaluation 紀錄 `b53ff286…` 所依的檔案未變），`assets/style.css` `60a27016…5f3f`（與 `d7f02d4` 相同；R3-5）。`git diff d7f02d4 9d5a840 -- results hw2.ipynb doc/spec/SPEC.md doc/ticket/tickets.md doc/brief/BRIEF.md doc/requirement assets/vendor` 為空（只有 #74 新增的 `tests/snapshots/`）。`hw2/` 自 `d7f02d4` 只有 `explore_reference.py`、`offline_scan.py`（#76，B-2）變更；`hw2/selection.py`、`tests/test_explore_kc_consistency.py` 未變（R4-3 約束 5）。探索檔案（engine、app、ui、plot、load、css、`data/startups50.js`、`explore_reference.py`）對 `model_data`／`MODEL_DATA`／`test_inputs` 的出現只有兩處「不讀 `model_data`」的既有註解，沒有引用。
- `index.html` 的修改全部在 `#explore` 子樹內（`#ex-run` 面板、`#ex-lasso-card` 說明、「方法與限制」一列與一段）；沒有新增 `<script src>`。
- **結論：符合 CC-V2-1、I-5、A-3 與 designation 第 4 點。**

## 3. 我自己執行的驗證

| 項目 | 指令／方法 | 結果 |
| --- | --- | --- |
| 全部 pytest | `.venv/Scripts/python -m pytest -q -rs -p no:cacheprovider`（Python 3.11.2，working tree＝subject） | **470 passed**、0 skipped（輸出無任何 skip 行），56.4 s |
| Node 個別檔案 | `node --test --test-reporter=tap tests/js/<f>.test.js`（Node v24.19.0） | `explore_load` 15、`explore_boundary` 7、`explore_app` 12、`explore_methods` 7、`explore_custom` 16、`explore_run` 21 pass；皆 0 fail、0 skipped、0 cancelled（`explore_contract` 由 pytest 以即時產生的 Python 參照驅動，含在 470 內） |
| 靜態掃描 | `python -m hw2.offline_scan` | `scanned 13 files: PASS (0 findings)` |
| PI 與 coverage 獨立重算（A-2(V2)） | `r77/dump_runs.js` 以 subject 引擎執行，`r77/recompute_pi.py` 以 numpy `lstsq`、`inv`、`scipy.stats.t` 從原始 CSV 列、訓練列的層級與基準重新擬合，不用引擎或參照的 fit | 50 Startups：All-in 與整體 winner `forward_sfs_k01` 的 10 筆 test 預測、上下界最大相對差 7.3e-11，`covered` 逐筆相同，coverage 1.0、RMSE 9850.21 相同；我自己的合成資料 `medium_r.csv`（20,000 列 × 26 欄，sha256 `1a04e21c…a61f`，目標單位約 0.01）：winner All-in 的 4,000 筆最大相對差 2.4e-10，`covered` 逐筆相同，coverage 0.9445 相同 |
| R4-3／R4-4 單位無關（我的資料） | `r77/probe_units.js`：`medium_r.csv` 前 3,000 列（25 個 group）與一份含精確倍數欄（`a2 = 2a`）的平手傾向資料，目標 × c（1e-12、1e-9、1e-6、1e3、1e9） | 兩份資料在每個 c 下的候選狀態與原因、各 fold 與 canonical 子集、Lasso 進入順序／已進入數／停止原因、winners 全部與 c＝1 相同；entry alpha 相對誤差 ≤ 1.4e-14 |
| G-3（記錄，不是 gate） | 頁內以 `HW2ExploreEngine.run` 跑內建 50 Startups，去掉 `meta.timing_ms` 後序列化 | Chrome 與 Edge 的確定部分 2,402 個數值全部位元相同（JSON sha256 皆 `84085e39…ad55`，結構相同）；與 Node v24 比較 2,377 個相同，最大相對差 1.7e-15。與 ACCEPTANCE V2-31 的陳述相符 |
| 取消時點與尾段（R1-F3） | `r77/probe_cancel_tail.js` | 引擎：在 `phase: 'diagnostic'` 事件時呼叫 `cancel()` → `COMPLETED`（含 `candidates`）；排程控制器：同一時點 `cancel()` 回傳 `true`，事件序列 `start → cancel → end COMPLETED`，頁面最後收到 `explore`／`COMPLETED`。尾段（最後一個候選邊界之後的 A-3 診斷與探索 test）長度：20,000 列 × 25 group 資料 279 ms；10,000 列 × 30 個 20 層級類別欄 **8.0 s**（All-in 14.1 s） |
| 大型輸入的原因（R1-F2） | `r77/probe_large.js`（記憶體內產生，不寫檔） | 536,872,488 bytes 的合法 UTF-8 CSV（`a,b,y` 後接約 8,900 萬列 `1,2,3`，列數遠超上限）→ `ENCODING`／`not_utf8`（6.4 s）；同樣內容 60,000 列 → `TOO_LARGE`／`rows_over`（對照）；`fetchCsvBytes` 的 `response.arrayBuffer()` 以 `RangeError: Array buffer allocation failed` 失敗 → `URL_FETCH_FAILED`／`network` |
| 瀏覽器檢查 | `r77/cdp77.js`（我自己的 DevTools Protocol 驅動；真實滑鼠與鍵盤事件；頁內以事件 `timeStamp` 量輸入延遲、`requestAnimationFrame` 量畫格、`PerformanceObserver('longtask')`） | 見第 4 節 AC「非阻塞與取消」與 R1-F1、R1-F3 |

## 4. AC 與分配義務逐項核對

| 項目 | 核對內容 | 結論 |
| --- | --- | --- |
| AC 預算與略過（主 seam） | 讀碼：`resourceEstimates`／`estimateSolves`（`explore_engine.js` 第 658–670 行）＝（Forward／Backward／RFE 每組列 p(p+1)/2、Lasso p，加每個 k 一次擬合）×（五個 fold＋訓練集）× 訓練列數 × 編碼欄數²，`q` 取訓練集編碼；判定在方法執行前、只依 `meta.budget.estimates`（第 1342 行，`>` 才略過）；All-in 在迴圈外、永遠先執行（第 1326–1336 行）。我重算 V2-32 的估計量：40,000 × 1,121² × 10,974＝5.52e14（Forward）、× 708＝3.56e13（Lasso），與紀錄相同。測試：`explore_run.test.js` 以 hooks 計數證明被略過的方法 0 個路徑、候選與擬合，其餘候選與未注入時 `deepEqual`，winner 只來自執行過的 `VALID`；時鐘無關、等於預算時執行；`budget_skip` Node 對 Python 含 `meta.budget` 比對 | 符合 |
| AC 失敗隔離（主 seam） | 讀碼：All-in 與每個路徑方法各自 `try`（第 1327–1331、1356–1364 行），例外只讓該方法 k = 1…p 全部 `FAILED`（`methodCandidate`，`cv`／`fit`／`canonical_groups` 為 `null`、`folds` 為空），原因附 `error`、`message`、`k`、環境；其他方法照跑；全部失敗時 `REJECTED`／`ALL_CANDIDATES_INVALID`。測試涵蓋候選中、路徑計算中、All-in 中與全部失敗 | 符合 |
| AC 取消語義（主 seam） | 讀碼：取消只在 `runSteps` 的候選邊界檢查（第 1323、1336、1350、1369、1382 行），讓出點（`yield null`）不是取消點；`CANCELLED` 結果只有 `meta` 與 `run`（第 1302–1307 行）。測試以計數證明 n＝0、1、2、5、9、16 時不多算、候選中途提出的取消讓該候選算完；重跑從 All-in 開始且確定部分與未取消相同。**例外**：最後一個候選邊界之後提出的取消不生效（R1-F3） | 候選期間符合；尾段見 R1-F3 |
| AC 不並行 | 讀碼：控制器 `active`／`waiting` 兩個位置，`request()` 先 `cancelActive()`，等前一次結束才 `next.start()`（`explore_app.js` 第 452–477 行）；測試以 `deps.trace` 斷言 `start 1 → cancel 1 → end 1 CANCELLED → start 2 → end 2 COMPLETED`、任何時刻至多一個；每次 URL 提交一次讀取（D-1） | 符合 |
| AC 可重現性（主 seam） | 測試以 `deepStrictEqual` 比較兩次執行的確定部分；三種入口確定部分相同；我自己的 G-3 比較（第 3 節） | 符合 |
| AC 非阻塞與取消（人工檢查表；UI 實際可操作） | 我自己的瀏覽器檢查，`medium_r.csv`（20,000 列 × 26 欄；訓練 16,000 列、25 group、101 個候選）。Chrome／Edge：選檔後 196／177 ms 出現執行面板；執行中點開問題下拉再按 Esc（值仍為「自訂資料集」）、點開目標欄下拉再按 Esc（可用、26 項）、在 URL 欄打 40 個字元（值正確）；進度在 1.7→5.5 s（Chrome）由 18% 前進到 48%、已耗時 1.5→5.0 s；輸入事件 89 個，最大延遲 13.4／14.8 ms；畫格中位數 12.5 ms、p95 16.7 ms；long task 各 1 個（175／168 ms，提交時的 CSV 結構檢查）；按取消 13／14 ms 後顯示「取消中…」，403／265 ms 後結束為 `CANCELLED`（Chrome 50／101 個候選、2／5 個方法；Edge 51／101、3／5），訊息「已取消：…停止時已完成 2／5 個方法（50／101 個候選）…」，五個結果區塊全部隱藏、執行面板隱藏；以同一檔案重跑，進度自「準備資料與切分」開始，11.7／11.6 s 完成，101 個候選，結果區塊顯示，完成訊息列出各方法耗時。對外請求 0、dialog 0、例外 0；切回 King County 時五個 V1 區塊與頁尾顯示。headless 不會出現「網頁沒有回應」對話框，以 long task 與畫格間隔替代（觀察 O-2）。**但**長候選期間進度不更新（R1-F1），尾段的取消不生效（R1-F3） | 中型資料上的可操作性符合；R1-F1、R1-F3 |
| AC 預算常數的紀錄 | ACCEPTANCE V2-27 記錄量度、常數（Forward／Backward／RFE `2e11`、Lasso `8e10`）與實測依據；V2-32 記錄載入上限 50,000 × 60。數字與 `BUDGETS`、`LIMITS` 相同（`test_budget_constants_are_the_same_in_the_engine_and_the_reference` 通過）；DA C1-R2 判定維持 50,000 × 60 在 boundary 內。V2-32 等紀錄須依 DA decision §6 (4) 更正（併入 R1-F1、R1-F2 的修正） | 符合（紀錄更正隨 R1-F1、R1-F2） |
| AC 可重現性（人工檢查表） | Executor 的 `*_startups.json`；我的 G-3 頁內比較（同一瀏覽器兩次的確定部分由 Node 測試與頁內比較涵蓋） | 符合 |
| AC 不變量 | 第 2 節；V1 快照測試與 sha256 測試通過；SR-09 量測記錄（V2-34；正式 gate 在 #78），我沒有另做 SR-09 量測 | 符合 |
| R4-2 | `CAUSE_TEXT`（`explore_app.js` 第 88–95 行）：`path_ended` 只陳述「其餘 group 與殘差的相關在數值上為零」，可能情形以「例如」列出（含完全擬合）；三種數值停止寫明是數值或上限造成；`target_constant` 如實。Lasso 表「未進入（路徑停止後，只作展示）」、摘要寫實際停止原因。Python 參照能偵測的 `alpha_increasing`、`max_iter` 與引擎一致，`multiple_drops` 的差異記於 worklog | 符合 |
| R4-3／R4-4 | 讀碼：`rowSetup`（第 1084–1098 行）以同一批列的置中目標均方根縮放，尺度 0 不除；Forward／Backward／RFE 的 Gram 與 Lasso 都用縮放後目標；回報 alpha＝縮放 alpha × 尺度；tie 叢集用縮放 alpha；`TIE_RTOL` 值不變；參照 `scaled_target`／`canonical_paths` 相同。KC 一致性測試未改且通過；50 Startups（c＝1）17 個候選全部 `VALID`。我自己的資料探測（第 3 節）通過 | 符合 |
| R3-2 | 探索模式頁尾隱藏（`body.is-exploring footer.footer`），我的檢查在 Chrome／Edge 切回 King County 時 `footer` 顯示；取消畫面沒有結果區塊 | 符合 |
| G-3 | 第 3 節 | 符合（記錄） |
| G-4 | `test_g4_startups50_under_the_final_budgets_runs_every_method`、`explore_run.test.js`「G-4」：最終常數下估計量 Forward 8.4e4、Lasso 4.8e4，17 個候選全部 `VALID` | 符合 |
| D-1（新提交時每次提交至多一次讀取） | `explore_run.test.js` scheduled 兩項（URL 提交在執行中仍一次讀取、改目標欄不重新讀取） | 符合 |
| #76 R1 O-1 ／ DA C2-R1～C2-R3 | 沒有位元組上限（C2-R2：正確，不得實作）；C2-R3 (a)(b) 不符合 | 見 R1-F2 |
| DA C1-R1、C1-R2 | 候選中的長等待與 50,000 × 60 上限依 DA 在 accepted 語義內；不是 finding | 符合 |
| DA C1-R3 | 執行中、取消中、等待中的進度不即時 | 見 R1-F1 |

## 5. 高風險類別（DA A-1；derivation §7.4：#77 觸及 H-1～H-5）

### H-1 憑證、機密與不得公開的資料（A-4）

- 讀取 `.local/packaging.json` 的學號（不印出），`git grep -c -F <學號> 9d5a840 -- home_work_02` 沒有任何命中。
- `git diff --name-only 4bd6a59 9d5a840` 的 46 個檔案中，URL 只有老師的範例 URL（`raw.githubusercontent.com/Avik-Jain/…/50_Startups.csv`）、`example.org`、`http://localhost`／`127.0.0.1`、既有的 Kaggle 來源；沒有本機路徑（`C:\Users`、`AppData`）或使用者提供的 URL；新增的資料檔 `s50_x1e-10.csv`（sha256 `d60fda8e…ee83`）、`exact_fit.csv`（`1a1fcd02…aedd`）是公開資料的縮放與合成資料，與 worklog 記錄的雜湊相同。
- 新增 UI 文字中的環境資訊（user agent、處理器數、裝置記憶體）只在 `FAILED` 原因顯示，不儲存。沒有 API key。
- **結論：符合。**

### H-2 老師指定的名稱與格式（OV-1 保持、請求隔離、`offline_scan`）

- 沒有新增 `<script src>`；`fetch(` 只在 `assets/explore_load.js`（`offline_scan` PASS、靜態測試通過）；我的兩個瀏覽器檢查（`file://`、離線）非 `file:` 請求 0；King County 區塊切回後顯示。
- **結論：符合。**

### H-3 評估完整性（A-2(V2)、A-3）

- 我自己執行 pytest（470 passed、0 skipped）與 Node 測試（含三層邊界、聚合與凍結、KC 一致性、取消／失敗／略過、可重現性）；自行重算兩份資料的 winner 逐筆 PI 與 coverage（第 3 節）；`SKIPPED_RESOURCE_LIMIT`／`FAILED`／`CANCELLED` 沒有 winner、test 或預測（讀碼與測試；`canPredict` 只對 `VALID`）；README 與報告未被本票修改，也沒有 50 Startups 的探索數字（以 KPI 數字 grep `README.md`、`report/*.md` 為 0）。正式分析不變（第 2 節）。
- **結論：符合。**

### H-4 證據真實性與如實標示（A-5）

- 50 Startups：`git show 9d5a840:home_work_02/assets/data/50_Startups.csv | sha256sum`＝`c6075ca5…630d`，與內嵌資料的 `sha256` 欄與 ACCEPTANCE 相同。
- ACCEPTANCE V2-30 的數字逐項對照 `chrome_subject_medium.json`、`edge_subject_medium.json`（取消 102／103 ms、232／291 ms、26／101 個候選、2／5 個方法、最大輸入延遲 13.7／13.6 ms、long task 130 ms、dialog 0）相同；V2-32 與 `chrome_subject_heavy.json`（268,792 ms、1／237）相同；V2-31 的 G-3 陳述與我自己的比較相同。截圖與 JSON 標明 `file://`、headless 環境。
- **但**頁面在兩處顯示不屬實的陳述：長候選期間「已耗時 0.0 秒、0%」（R1-F1）；尾段按取消後「取消中：目前的候選算完後（下一個候選邊界）停止」而執行照常完成（R1-F3）；大型輸入被標為「不是 UTF-8」或網路／跨來源（R1-F2）。ACCEPTANCE V2-30／V2-32 與 worklog D-9、D-10、§8 須依 DA decision §6 (4) 更正。
- **結論：不符合（R1-F1、R1-F2、R1-F3）。**

### H-5 使用者提供的資料來源與網路請求邊界（A-9）

- 我列舉 V2 五個 JS 檔中 A-9 的全部 API（`grep` `innerHTML|outerHTML|insertAdjacentHTML|document.write|DOMParser|createContextualFragment|srcdoc|eval(|new Function|字串型 setTimeout|setInterval|import(|Worker(|importScripts|fetch(|XMLHttpRequest|WebSocket|EventSource|sendBeacon|.src=|.href=|location|localStorage|sessionStorage|cookie|postMessage`）：只有 `explore_load.js` 第 322 行的 `fetch(url, init)`（#76 已審）與本票新增的 `MessageChannel`（`explore_ui.js` 第 632–633 行：`port1.onmessage` 只執行佇列中的函式、`port2.postMessage(0)` 只送數字 0 給自己的 port，不是跨 origin 訊息、不執行字串），以及以函式為參數的 `setTimeout(fn, 0)`。本票新增的 DOM 寫入（進度列、取消按鈕、取消與完成訊息、`SKIPPED`／`FAILED` 原因、診斷錯誤）全部經 `textContent` 或 `el(..., {text})`；`test_exploratory_files_write_no_markup_and_run_no_strings` 通過。
- 不並行與每次提交一次讀取（D-1）符合（第 4 節）；mock fetch 測試通過；不儲存（#76 的測試照常通過）。
- H-5(d) 資源：候選期間的可操作性符合；長候選的進度（R1-F1）與大型輸入的原因（R1-F2）、尾段的取消（R1-F3）不符合。
- 探測：本票沒有改動載入與欄名呈現的路徑（`explore_load.js` 未變）；Executor 已以 `probe76.csv` 在 subject 上探測。我沒有重做 A-9 的刻意構造 CSV 探測，理由是本票新增的寫入點不含任何輸入衍生字串（只有方法名稱、數字與引擎訊息），上列 grep 與靜態測試已涵蓋；Spec Integration Audit 會在整合 subject 上再做。
- **結論：DOM 與請求邊界符合；資源保護見 R1-F1～F3。**

## 6. Findings

| ID | Severity | Blocking | 內容與證據 | 依據的契約條款 |
| --- | --- | --- | --- | --- |
| **R1-F1** | **High** | **是** | **執行進行中的進度顯示不即時**（DA C1-R3 的最終判定）。讀碼：引擎只在開始、候選邊界、略過、失敗與診斷前 `emit` 進度（`explore_engine.js` 第 1322、1335、1349、1368、1381、1387 行）；控制器只在收到事件時 `render({mode:'progress'})`（`explore_app.js` 第 434 行）；`explore_ui.js` 沒有其他更新進度的計時器，按取消後進度列寫入固定文字「取消中：目前的候選算完後（下一個候選邊界）停止。」（第 617 行），之後 `showProgress` 因按鈕停用不再寫入（第 114 行）；等待中的請求顯示固定文字（第 108 行）；檔頭註解宣稱「the progress line keeps updating」（第 32 行）。我的瀏覽器檢查（`cat_heavy.csv`：10,000 列 × 30 個 20 層級類別欄、1,130,350 bytes，訓練編碼 570 欄、121 個候選；All-in 約 13.6 s）：Chrome 在 1.1、2.1、3.1、4.1、5.1、6.1 s 的進度列都是「執行中（準備完成，開始計算候選）：已完成 0／121 個候選、0／5 個方法（0%），已耗時 0.0 秒」，Edge 相同；按取消後 7.9 s（Chrome）／7.7 s（Edge）內進度列一直是同一句固定文字，之後才 `CANCELLED`（1／121）。Executor 的 `chrome_subject_heavy.json` 在 50,000 × 60 的資料上第 8 秒同樣是「已耗時 0.2 秒、0%」，取消後等了 268.8 s。輸入延遲（≤ 11.8 ms）與畫格（p95 12.6 ms）正常——頁面可操作，但顯示的已耗時不是事實，使用者無法分辨頁面是否卡住 | #77 AC「進度持續更新」、What to build「任意大小的合法資料集上都不卡死」；Spec SR-V2-03 進度（含「已耗時」、UI 顯示）；Brief V2 §5.5「執行中有可觀察的進度」；US-27；DA `decision-20261022-issue77-resource-limits` C1-R3 與 §6 (1)；H-4、H-5(d) |
| **R1-F2** | **Medium** | **是** | **大型輸入的拒絕原因不屬實**（DA C2-R3 (a)(b) 的最終判定）。讀碼：`inspectCsv()` 把 `decodeUtf8Strict()` 的任何例外回報為 `ENCODING`／`not_utf8`（`explore_load.js` 第 226–227 行）；`fetchCsvBytes()` 把本文讀取的任何失敗回報為 `URL_FETCH_FAILED`／`network`（第 372–377 行）。我的探測：536,872,488 bytes、列數遠超 50,000 的**合法** UTF-8 CSV → `ENCODING`／`not_utf8`，而不是 `TOO_LARGE`；同一內容 60,000 列 → `TOO_LARGE`（對照）；`response.arrayBuffer()` 以 `RangeError: Array buffer allocation failed` 失敗 → `URL_FETCH_FAILED`／`network`（頁面說成網路或跨來源限制，但本文其實已收到）。`explore_load.js` 自 #76 未變；這不是 #76 已驗證範圍內的缺陷（DA C2-R3 末段），是 O-1 分配給 #77 的資源保護範圍。不得以位元組上限修正（C2-R2） | Spec V2「載入契約」（超過拒絕 `TOO_LARGE`；原因與子原因枚舉）；Brief V2 §8 第 5 條；DA `decision-20261022-issue75-lasso-early-stop` R4-2（畫面不得宣稱未確立的原因）；DA `decision-20261022-issue77-resource-limits` C2-R3、§6 (2)(3)；H-4、H-5(d) |
| **R1-F3** | **Medium** | **是**（修正方向需 Design Authority，見第 7 節） | **最後一個候選邊界之後的取消被接受、宣稱會停止，但不生效**。讀碼：A-3 診斷與探索 test 在最後一個候選邊界之後執行，之後沒有任何取消檢查（`explore_engine.js` 第 1385–1414 行）；控制器 `cancel()` 在這段期間仍回傳 `true`（`explore_app.js` 第 576–578 行），頁面把按鈕改為「取消中…」並寫「取消中：目前的候選算完後（下一個候選邊界）停止。」（`explore_ui.js` 第 612–618 行）；`index.html` 第 95 行的說明與「方法與限制」段落（第 236 行）都說取消在下一個候選邊界生效、只顯示「已取消」。Executor 在 worklog D-1 揭露了「在那之後才提出的取消不再有邊界，執行照常完成」，但頁面沒有。我的驗證：Node 探測——引擎在 `diagnostic` 事件時取消 → `COMPLETED`；控制器 `cancel()` 回傳 `true`、事件序列 `start → cancel → end COMPLETED`。瀏覽器（`cat_heavy.csv`）：13.7 s（Chrome）／14.3 s（Edge）進入尾段，進度列「執行中（全部候選已完成，正在計算共線診斷與探索 test）：已完成 121／121 個候選…（100%）」；此時按取消，頁面顯示「取消中…」與上述停止文字，9.3 s／8.4 s 後顯示「執行完成：五種方法共 121 個候選…」與全部五個結果區塊。尾段長度隨設計矩陣變大：20,000 列 × 25 group 約 0.3 s、10,000 列 × 570 編碼欄約 8 s；以 O(n·p²) 外推，50,000 × 60 的最壞情形為分鐘級（未量測，推估）。不論契約要求的是「尾段的取消也要結束為 `CANCELLED`」或「尾段不可取消」，現行行為都不成立：前者下 run 狀態錯誤，後者下頁面接受取消並宣稱會停止是不屬實的陳述 | Spec SR-V2-03「可終止：取消請求在下一個候選邊界生效；取消後執行狀態為 `CANCELLED`」；#77 What to build「任意大小的合法資料集上都…可取消」、AC「按取消後在下一個候選邊界停止並顯示『已取消』…沒有任何結果區塊」；H-4 |

### 觀察（不是 finding）

| ID | 內容 | Disposition | Owner |
| --- | --- | --- | --- |
| O-1 | 提交時的 CSV 結構檢查與 sha256 是同步的一個工作：我的 3.8 MB 資料 175／168 ms、Executor 的 10.7 MB 資料 434 ms；只有欄寬極大的檔案（worklog §6.5：95 MB）才會到數秒。載入契約未改；DA 已在 C2 裁決讀取階段的要求（C2-R3 只要求原因如實，串流與分段不是要求） | 供 Spec Integration Audit 知悉；不需處理 | Orchestrator（列入 Spec Integration Audit pack） |
| O-2 | Executor 與我的「非阻塞」證據都是 headless 瀏覽器以 DevTools 送出的真實輸入事件，不是 acceptor 的人工操作；headless 不會出現「網頁沒有回應」對話框，以 long task 與畫格間隔替代。我認為這足以作為 AC「UI 實際可操作」的證據，ACCEPTANCE V2-30 也如實標示 | 無需處理 | — |
| O-3 | `explore_run.test.js`「cancel after the n-th candidate」刻意排除 `diagnostic` 事件（與 D-1 一致），所以尾段的取消沒有任何測試覆蓋 | 隨 R1-F3 的修正處理（測試方式是 HOW，由 Executor 決定） | Executor（R1-F3 修正時） |

## 7. Routing

- **R1-F1、R1-F2** → Executor targeted correction（DA `decision-20261022-issue77-resource-limits` §6 (1)～(6) 已定義義務與證據，含 worklog D-9、D-10、§8、ACCEPTANCE V2-30／V2-32 與 `explore_ui.js` 檔頭註解的更正）→ R2。
- **R1-F3** → **required authority：Design Authority**（契約語義不足的部分）。具體 ambiguity：Spec 的「取消請求在下一個候選邊界生效」預設還有下一個候選邊界；最後一個候選邊界之後（A-3 診斷與探索 test 執行期間）提出的取消，契約沒有說是 (i) 應在執行結束時以 `CANCELLED` 結束、不呈現結果，或 (ii) 這段期間不可取消、頁面須如實表示（例如停用或改寫取消控制項與說明），或其他處理；也沒有說診斷可否移回第一個候選邊界之前。不論 DA 選哪一種，現行行為都需要修正（第 6 節），所以這是 blocking finding，不是單純的 routing signal；修正方向等 DA 裁決後由 Executor 實作，R2 依該裁決核對。建議 Orchestrator 在派 R1-F1、R1-F2 的 targeted correction 前取得 DA 對 R1-F3 的裁決，使同一次修正涵蓋三項。
- 沒有需要 acceptor 的事項；沒有 boundary 疑義。

## 8. Non-blocking findings 的 disposition

本 R1 沒有 non-blocking finding；觀察 O-1～O-3 的 disposition 與 owner 見第 6 節。

VERDICT: BLOCKING (R1-F1, R1-F2, R1-F3)
