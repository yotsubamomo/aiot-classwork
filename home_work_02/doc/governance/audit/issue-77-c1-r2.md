# Audit record — #77 HW2 V2-T4，cycle 1，R2

- **Audit 種類**：Ticket independent audit，**R2（closure review）**，cycle 1（治理 §4.4；Bindings b5 §5 Formal）。範圍只限 R1 的 blocking findings **R1-F1、R1-F2、R1-F3** 是否真正解決、修正是否引入回歸、修正是否直接產生或暴露新的 blocking defect；不是第二次全面審查。**本 record 不是 Spec Integration Audit。**
- **角色**：`primary_reviewer`（definition `gov-primary-reviewer`）。
- **Run**：`run-20261022-hw2-v2-enhance`（Orchestrator＝root session `37216426-f292-44f9-bad1-e2d862e7b8f1`）。
- **Work Contract**：與 R1 相同（`audit/issue-77-c1-r1.md` 檔頭；issue #77 body sha256 `c9b79356…90fe`；OC §5／§5.2 CC-V2-1；Spec V2 rev 2；Brief V2 rev 2＋E-1；`tickets-v2.md` 調整 B；DA derivation 與 R4、R3 decisions）。修正須符合的 DA 紀錄：**`decisions/decision-20261022-issue77-resource-limits.md`**（C1-R3、C2-R2、C2-R3、§6 (1)～(6)）與 **`decisions/decision-20261022-issue77-cancel-final-phase.md`**（CF-1、§4 (1)～(6)，對 R1-F3 的裁決；我自行讀取全文）。
- **受審 subject**：branch `home_work_02-v2-enhance`，HEAD **`31a2255fe2d1111772d46c9ea83a21c0f97d2fcb`**（紀錄與證據）；實作 commit `1514005069805b25ee9bce977d554b01ff88e8b4` 與 **`64b2dfd1f851aa4a14a3b8d1d9e6bca3aed8865a`**（實作 subject）；parent `d7147ba`（含 R1 record 與兩份 DA 紀錄）。`git diff --stat 64b2dfd 31a2255 -- assets hw2 tests index.html` 為空；`git diff --name-only d7147ba 31a2255` 的 34 個路徑全部在 `home_work_02/` 內，沒有 `doc/requirement/`；實作修改的路徑只有 `assets/explore_app.js`、`explore_engine.js`、`explore_load.js`、`explore_ui.js`、`index.html`、`tests/js/explore_run.test.js`、`tests/test_explore_static.py`。審查時 working tree 的程式、資料與測試與 `64b2dfd` 相同；唯一差異是 Orchestrator 未 commit 的 run record（record-only path）。

## 1. Assurance

### (a) Context independence（治理 §2.3；Bindings §3.7）

| Property | 滿足方式 |
| --- | --- |
| Independent context | 本 R2 依 Bindings §3.7 以 SendMessage 延續我自己的 R1 context（同一 agent），不繼承 Executor（agentId `a7b3c024fa9b13368`）的對話或推理。依治理 §2.3 第 1 項，我從磁碟重讀修正後的檔案與 `git diff d7147ba 31a2255`；worklog §10、ACCEPTANCE V2-29／V2-30／V2-32 的更正與 `c1_*` evidence 只當作待驗證主張，以我自己的測試、Node 探測、新舊載入程式的比較與我自己的瀏覽器檢查驗證；沒有執行 Executor 的腳本 |
| Verifiable binding | 本 assignment：agentId `ab93f858531ba9d08`，`agentType` `gov-primary-reviewer`；以 Bindings §3.6 指令讀取自己的 transcript（R1＋R2），寫本 record 前觀測到 `('claude-opus-5-5', 'xhigh')` 238 則，單一元素，等於有效 mapping R-PR；沒有 escalation、沒有替代。全程核對由派工者依 §3.6 在採用 return 前執行 |
| Autonomous access | 自行讀取 repo、`git show／diff／archive`（不做 git 寫入）與 transcript 的 model 欄位；自行執行 pytest、Node 測試、`offline_scan`、Node 探測、模糊比對與 headless Chrome／Edge 檢查 |
| Self-written record | 本 record 由我以自己的 Write 工具寫入 Bindings §7 的位置；派工者只能原樣 commit |

### (b) Model diversity（Bindings §5；治理 §4.6）

| Assignment | 實際 model（transcript 觀測，我自己以 §3.6 指令讀取） |
| --- | --- |
| Executor，agentId `a7b3c024fa9b13368`（`gov-executor`；含 targeted correction） | `claude-opus-5-5`／`high`（434 則，單一元素） |
| Primary Reviewer（R1＋本 R2），agentId `ab93f858531ba9d08` | `claude-opus-5-5`／`xhigh`（238 則，單一元素） |

**無 model diversity**。依 Bindings §5 與 DA A-8，不宣告 diversity 關係，不影響 independence 判定。

### 審查環境的操作

- 瀏覽器只以我啟動的程序執行：headless Chrome 155.0.8059.85（PID 30764、38100、3052）與 Edge 155.0.4283.62（PID 26080），各自使用 scratchpad `r77/prof_r2_*` 的全新 `--user-data-dir`，從未使用 acceptor 的預設 profile；每次結束以 `taskkill /PID <pid> /T /F` 停止，之後以 `Get-CimInstance Win32_Process` 核對沒有使用這些 profile 的殘留程序（0），profile 目錄已刪除。頁面是 `git archive 64b2dfd home_work_02/index.html home_work_02/assets` 的匯出（`file://`），網路以 DevTools 模擬離線。
- 我建立的兩個大型測試檔（`big_over.csv` 541,064,706 bytes、`big_within.csv` 539,964,981 bytes）只在 scratchpad，檢查後已刪除。其他探測在記憶體內產生輸入，不寫檔。
- 沒有修改任何追蹤中的檔案。

## 2. Blocking findings 的核對

### R1-F1（High）執行中的進度不即時 — **已解決**

- **修正**（讀碼）：排程控制器在每個時間片之後、至少每 200 ms 送出 `mode: 'heartbeat'` 的 view（`explore_app.js` `beat()`，`pump()` 每次未完成時呼叫；`cancel()` 時 `beat(true)`），內含即時的已耗時、最後一個進度事件、是否取消中；等待前一次停止的請求以 `live.kind = 'waiting'` 計時。`explore_ui.js` `showHeartbeat()` 以 `App.liveText()` 寫入進度列（`textContent`）。完成數與方法數仍在候選邊界更新；取消時點、不並行與結果契約沒有改變（引擎的候選邊界檢查未動）。按取消後的固定文字已移除，改為即時文字。`explore_ui.js` 檔頭註解已改寫。
- **頁面路徑**（我的檢查，`cat_heavy.csv`：10,000 列 × 30 個 20 層級類別欄，訓練編碼 570 欄、121 個候選、All-in 約 14 s）：
  - 執行中（All-in 這一個長候選期間每秒取樣）：Chrome「…已完成 0／121 個候選、0／5 個方法（0%），已耗時 0.9／1.9／3.0／4.0／5.0 秒」；Edge 0.9／1.9／3.0／4.0／5.0 秒。（R1 時 `9d5a840` 同一資料一直是「已耗時 0.0 秒」。）
  - 取消中（在 All-in 內按取消，每秒取樣）：「取消中：目前的候選算完後（下一個候選邊界）停止，不顯示任何結果。已耗時 6.0／7.0／8.1／9.1／10.1 秒」（Edge 6.0→10.2），之後結束為 `CANCELLED`（1／121 個候選、1／5 個方法），沒有結果區塊、執行面板隱藏。
  - 等待中（長執行中再次選同一檔案）：「等待前一次執行停止（…），之後從頭開始新的執行…已等待 0.9／1.9／2.9／4.0 秒」（Chrome 與 Edge 相同）；此時按「取消執行」→ `cancelled` 畫面，沒有結果區塊。
  - 執行中輸入延遲最大 12.0／12.2 ms，畫格 p95 12.6／12.7 ms，long task 0（Chrome／Edge）。
- Node：`explore_run.test.js` 的 heartbeat 測試（執行中、取消中、等待中嚴格前進；結果交付後不再送出）通過。
- **結論**：DA C1-R3 與 §6 (1) 的要求在頁面上成立；R1-F1 resolved。

### R1-F2（Medium）大型輸入的拒絕原因不屬實 — **已解決**

- **修正**（讀碼）：`inspectCsv()` 只把 `TypeError`（無效 UTF-8）回報為 `ENCODING`；其他解碼例外，以及解碼器靜默回傳過短字串（`text.length * 3 < bytes.length - 3`；合法 UTF-8 每 3 個位元組至少 1 個 UTF-16 單位，不會誤判完整解碼）改走 `inspectBytes()`：分段嚴格 UTF-8、U+FFFD／NUL、與 `readRecords` 相同規則與順序的位元組記錄計數、單獨解碼的欄名列、記錄長度；超過列數或欄數上限者為 `TOO_LARGE`，全部通過時回傳 `{ ok: false, reason: null, environment_error }`（沒有新原因碼或子原因）。URL 本文 `arrayBuffer()` 的 `RangeError` 回傳 `environment_error`（`stage: 'read_body'`），其他失敗仍是 `URL_FETCH_FAILED`／`network`。本機檔案讀取的 `RangeError` 有自己的訊息。沒有位元組上限（C2-R2）。
- **我的 Node 探測**（真實的 V8 解碼器，輸入在記憶體內產生）：
  - 536,872,488 bytes 的合法 UTF-8、列數遠超上限 → `TOO_LARGE`／`rows_over: 50000`（8.3 s）；R1 時同一輸入是 `ENCODING`／`not_utf8`。
  - 537,126,861 bytes、5,371 列 × 3 欄（在上限內，超過 V8 字串上限）→ `{ ok: false, reason: null, environment_error: { stage: 'decode', error: 'Error', message: 'Cannot create a string longer than 0x1fffffe8 characters', … } }`；頁面文字「瀏覽器無法處理這份輸入…這不是 CSV 格式或編碼的問題；沒有執行分析。」
  - URL 本文 `RangeError: Array buffer allocation failed` → `environment_error`（`read_body`，HTTP 200），頁面文字明寫「這不是網路或跨來源限制」；R1 時是 `URL_FETCH_FAILED`／`network`。
- **頁面路徑**（Chrome，檔案選擇）：`big_over.csv`（541 MB，9,000 萬列）→「無法載入資料：超過載入上限（TOO_LARGE）：資料列超過 50,000 列的上限；不會截斷。」（7.3 s）；`big_within.csv`（540 MB，19,995 列 × 3 欄）→「無法載入資料：瀏覽器無法處理這份輸入（約 515 MB）：它是有效的 UTF-8，列數與欄數都在載入上限內，但超過這個瀏覽器分頁能以文字處理的大小或記憶體（Error：the decoder returned 0 characters for 539964981 bytes …）。這不是 CSV 格式或編碼的問題；沒有執行分析。」（8.8 s）。這也確認了 Chrome 155 的解碼器對 540 MB 輸入靜默回傳空字串（`64b2dfd` 處理的情形）。兩次都沒有分頁崩潰、例外 0、請求 0。
- **位元組路徑與文字路徑一致**（`r77/r2_bytepath.js`，我自己的模糊比對）：約 60,000 份隨機的 CSV 類輸入（引號、CRLF、空白列、BOM、多位元組字元、U+FFFD、NUL、無效位元組、不等長記錄、小的列數／欄數上限），以拋出 `RangeError` 與回傳空字串兩種解碼器強制走位元組路徑，共 118,899 次比較：文字路徑在 `ENCODING`／`NOT_CSV`／`TOO_LARGE`／`NO_HEADER`／`DUPLICATE_COLUMN`／`RAGGED_ROWS` 拒絕者，位元組路徑的 `LoadResult` 逐欄相同（107,893 次）；文字路徑接受或在之後的階段拒絕者（`TOO_FEW_ROWS` 等），位元組路徑為 `environment_error` 且 sha256 相同（11,006 次）；**0 個不一致**。新的逐區塊 SHA-256 對 307 種長度（0～300 與到 1 MiB）與 `node:crypto` 全部相同。
- **結論**：DA C2-R3 (a)(b) 與 §6 (2)(3) 成立，沒有位元組上限；R1-F2 resolved。

### R1-F3（Medium）最後一個候選邊界之後的取消不生效 — **已解決**（依 DA CF-1）

- **修正**（讀碼）：`explore_engine.js` 在共線診斷完成後、以及每個 winner 的探索 test 完成後檢查取消（`if (control.cancel) return cancelled();`），取消優先於 `REJECTED` 與 `COMPLETED`，結果只有 `meta` 與 `run`；進行中的步驟不在中途中斷；新增進度 phase `test`；引擎版本 3.1。頁面：尾段的取消中文字為「取消中：全部候選已完成，正在進行的共線診斷或探索 test 步驟完成後停止，不顯示任何結果」，已取消訊息寫「取消在全部候選完成後、進行中的步驟完成時生效」；`index.html` 第 95 行的說明與「方法與限制」段落涵蓋尾段。
- **我的 Node 探測**：R1 的 `probe_cancel_tail.js` 情境（`diagnostic` 事件時取消）在 `64b2dfd` 結果為 `CANCELLED`、沒有 `candidates`（R1 時為 `COMPLETED`）；新增的 Node 測試涵蓋探索 test 期間、全部候選無效（原本 `REJECTED`）與排程控制器的尾段取消與新提交。
- **頁面路徑**（`cat_heavy.csv`）：
  - 尾段的共線診斷期間（Chrome 15.1 s 時進度列「執行中（全部候選已完成，正在計算共線診斷）：已完成 121／121 個候選…（100%）」）按取消 → 取消中文字如上、已耗時 15.6→16.4 秒持續前進 → 6.6 s 後（診斷步驟完成時）結束為 `CANCELLED`（121／121、5／5），訊息「已取消：取消在全部候選完成後、進行中的步驟完成時生效…」，**沒有任何結果區塊**、執行面板隱藏。Edge：7.4 s 後同樣結果。
  - 探索 test 期間（Chrome 21.9 s 時「…正在計算探索 test」）按取消 → 1.9 s 後 `CANCELLED`，沒有結果區塊；Edge 1.7 s，相同。
  - R1 時同一操作在 `9d5a840` 以 `COMPLETED` 顯示全部五個結果區塊。
- **結論**：DA CF-1 與 §4 (1)～(5) 成立；R1-F3 resolved。

## 3. 回歸

| 項目 | 方法 | 結果 |
| --- | --- | --- |
| 全部 pytest | `.venv/Scripts/python -m pytest -q -rs -p no:cacheprovider`（working tree＝`64b2dfd`） | **470 passed**、0 skipped（60.5 s） |
| Node 個別檔案 | `node --test --test-reporter=tap`（Node v24.19.0） | `explore_load` 15、`explore_boundary` 7、`explore_app` 12、`explore_methods` 7、`explore_custom` 16、`explore_run` 31 pass；皆 0 fail、0 skipped、0 cancelled |
| 靜態掃描 | `python -m hw2.offline_scan` | `scanned 13 files: PASS (0 findings)` |
| 測試的修改 | `git diff d7147ba 64b2dfd -- tests` | 只擴充：`explore_run.test.js` 新增 10 項；唯一改動的既有期望是 `progress` 測試的最後 phase 由 `diagnostic` 改為 `['diagnostic', 'test']`（新增 phase 的必然結果，其餘斷言不變）；`test_explore_static.py` 只增加說明文字的片語。候選期間的取消測試（R1 O-3 所指）未改且通過。接受基準的既有測試只有 CC-V2-1 的 `test_dashboard_static.py`（#74，未再動） |
| A-3 與 V1 | `git show 64b2dfd:<path> \| sha256sum` | `app.js` `c1ab3f21…82ad`、`hw2core.js` `e75c5d48…2c14`、`model_data.js` `6cf0c11e…a7ac`、`results/model_data.json` `69dc1465…6e61`、`style.css` `60a27016…5f3f` 不變；`hw2/`、`tests/test_explore_kc_consistency.py`、`assets/data/` 自 `9d5a840` 無 diff；沒有新增 `<script src>`；V1 快照測試通過；兩個瀏覽器切回 King County 時五個 V1 區塊與頁尾顯示 |
| 引擎結果 | 以 `64b2dfd` 與 `9d5a840` 的引擎跑 50 Startups 與我的 `medium_r.csv`，比較確定部分（去掉 `meta.engine_version`） | 逐值相同；`medium_r` 的 winner 逐筆 PI 我再以 numpy／scipy 獨立重算，最大相對差 2.4e-10、`covered` 逐筆相同。頁內 50 Startups 的確定部分 Chrome 與 Edge 相同，且與 R1 時的 Chrome 結果相同（只差引擎版本字串） |
| 載入結果不變（DA C2-R3 限制） | `r2_oldnew*.js`：`64b2dfd` 與 `9d5a840` 的 `explore_load.js` 對同一輸入的 `inspectCsv()` | 80,000 份隨機輸入（含各種拒絕原因與指定目標欄）與 3,012 份可解碼輸入（2,708 份被接受，含 50 Startups、`medium_r`、`cat_heavy` 與目標欄 0～2）：`LoadResult` 與欄位描述 **0 個差異** |
| 非阻塞與取消（中型資料） | 我的瀏覽器檢查，`medium_r.csv` | 執行中點開問題下拉再按 Esc、在 URL 欄打字（值正確）；進度前進（23%→43%）；輸入延遲最大 15.0／15.5 ms、畫格 p95 16.7 ms、long task 2（提交時的載入，最大 150／140 ms）；取消後 `CANCELLED`（Chrome 44／101、Edge 47／101），沒有結果區塊；重跑 12.1／11.6 s 完成並顯示五個結果區塊 |
| H-5 | `grep` V2 檔案的 A-9 API | 修正沒有新增任何 DOM 解析、字串執行或網路 API；`fetch(` 仍只在 `explore_load.js` 原有的一處；新的寫入（heartbeat、取消中、環境失敗訊息）都經 `textContent`；環境失敗訊息中的 `message` 來自 JS 引擎的例外文字或本程式自己的字串 |
| 請求與錯誤 | 兩個瀏覽器的全部檢查 | 非 `file:` 請求 0、dialog 0、例外 0、分頁崩潰 0 |
| 紀錄 | 讀 worklog §10、D-1、D-9、D-10、§8 與 ACCEPTANCE V2-29／V2-30／V2-32 的更正 | 已依兩份 DA 紀錄更正；我抽查的數字（heartbeat 的取樣、尾段取消、540 MB 檔案的結果）與我自己的重現一致 |

## 4. 修正直接產生或暴露的問題

沒有 blocking defect。以下是觀察，不延長 cycle（治理 §4.4）：

| ID | 內容 | Disposition | Owner |
| --- | --- | --- | --- |
| O-R2-1 | 一份**可以**解碼、略小於 V8 字串上限、且在列數與欄數上限內的輸入（我的探測：536,541,011 bytes、1,001 列、每列一格 536 KB），在既有的文字路徑解析時耗盡 Node 的預設 heap（`FATAL ERROR … heap out of memory`）；瀏覽器中可能是分頁崩潰而不是訊息。這是**既有**行為：文字路徑在本修正中沒有改變（新舊載入程式比較 0 差異），也不是不屬實的原因，所以不屬 R1-F2 的範圍，也不是修正造成的。DA `decision-20261022-issue77-resource-limits` §6 已要求 #78 揭露「超過瀏覽器能力的極大檔案可能無法讀取」 | 供 #78 的揭露與 Spec Integration Audit 知悉；不需本票處理 | Orchestrator（列入 #78 與 Spec Integration Audit pack） |
| O-R2-2 | 新的位元組路徑與 SHA-256 在一個同步工作中完成：Chrome 上 540 MB 檔案約 7.3～8.8 s，期間頁面不回應輸入（Executor 在 worklog §10 也記錄）。只發生在大於約 512 MiB 的輸入；DA C2-R3 不要求串流或分段（與 R1 O-1 同性質） | 供 Spec Integration Audit 知悉 | Orchestrator |
| O-R2-3 | 進度列 `#ex-progress-text` 帶 `aria-live="polite"`，heartbeat 約每 200 ms 改寫一次文字；螢幕閱讀器可能頻繁朗讀。螢幕閱讀器在 AD-1 是 best effort（NOT TESTED），不是 gate，也不違反契約 | 無需本票處理；Spec Integration Audit 的 OV-4 核對時可參考 | — |

## 5. Verdict

R1-F1、R1-F2、R1-F3 都已解決並在頁面路徑上驗證；修正沒有引入回歸，也沒有直接產生或暴露 blocking defect。觀察 O-R2-1～O-R2-3 不延長 cycle。

VERDICT: CLOSURE
