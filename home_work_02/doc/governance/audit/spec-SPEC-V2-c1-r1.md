# Audit record — Spec V2 rev 2（#73）的 Spec Integration Audit，cycle 1，R1

- **Work Contract**：Outcome Contract [`../outcome-contract.md`](../outcome-contract.md) §5（V2 Enhance，接受基準 `d7f02d4179d2cb5c2ecf0c39a4643a6ef8287907`）、§5.1（acceptor 原文）、§5.2 CC-V2-1；仍有效的 §1–§4（V1：Brief @ `dff7c55c`＋CC-1、AD-1～AD-3）。Derived contracts：Spec V2 rev 2（`doc/spec/SPEC-V2.md`，sha256 `695161db…`，與 `d7f02d4` 相同；GitHub #73 本文與檔案只差檔尾換行）、`doc/ticket/tickets-v2.md`（`f1e6b1a6…`）、issue #74–#78（本文 sha256 `49e3cc50…`、`834a439c…`、`5d121dd9…`、`c9b79356…`、`5e31ce34…`，2026-10-22 重算，與 `decisions/derivation-SPEC-V2.md` §3 記錄的 accepted 版本相同）；Brief V2 rev 2＋E-1（`27f08b25…`）；Spec V2 未提到者依 Spec rev 5。DA 紀錄：`derivation-SPEC-V2.md`（B-1～B-14、§5 分配、G-1～G-5、§7 H-1～H-5 與 A-1～A-9、D-1、D-2、I-1～I-5）、`decision-20261022-r1f3-v1-footer.md`（R3-1～R3-6）、`decision-20261022-issue75-lasso-early-stop.md`（R4-1～R4-6）、`decision-20261022-issue77-resource-limits.md`（C1-R1～C1-R4、C2-R1～C2-R3、§6）、`decision-20261022-issue77-cancel-final-phase.md`（CF-1、CF-2、§4）、`decision-20261018-high-risk-categories.md`（V1 的 H-1～H-4、A-1～A-8）。
- **受審 subject（整合後的最終 subject）**：branch `home_work_02-v2-enhance`，commit **`3745e9cb4b265e15538576e9b95cd64738e9de35`**（#78 的 closed subject，也是 #74–#78 整合後的狀態）。V2 範圍 `d7f02d4..3745e9c`（34 個 commit 中的實作與紀錄）；V1 狀態 `main` `392e9df`。審查時 HEAD `33107ed`；`git diff --name-only 3745e9c 33107ed` 只有 `doc/governance/audit/issue-78-c1-r1.md` 與 run record（record-only，Bindings §7）。工作樹在 `home_work_02/` 內沒有修改或未追蹤的非忽略檔案，所以主 checkout 的程式、資料與測試就是 `3745e9c` 的內容；另以 `git archive 3745e9c home_work_02` 匯出到 scratchpad 供探測與 mutation 使用。未追蹤的繳交 ZIP `dist/<學號>_hw2.zip`（由 `f56461b` 打包）一併受審（A-6）。
- **Audit 種類**：Formal 的 **Spec Integration Audit**（治理 §4.7；Bindings b5 §5），**cycle 1、R1**。它是獨立的 audit instance，subject 為整合結果，**不是**任何 Ticket audit 的 R3。Spec V2 有五張票，**不適用**單 Ticket fast path；本 record 不是任何 Ticket R1 的重新標示。
- **角色**：`primary_reviewer`（definition `gov-primary-reviewer`），Bindings b5 §3.1 有效 mapping `claude-opus-5-5`／`xhigh`（R-PR 首項），沒有 escalation、沒有替代。
- **Run**：`run-20261022-hw2-v2-enhance`（Orchestrator＝root session `37216426-f292-44f9-bad1-e2d862e7b8f1`）。
- **Binding（觀測）**：本 assignment agentId **`aa43e1e2fb1e18487`**（`agent-aa43e1e2fb1e18487.meta.json` 的 `agentType`＝`gov-primary-reviewer`，description「Spec Integration Audit Spec V2」）。寫入本 record 前以 Bindings §3.6 的方法掃描本 transcript 全部 assistant 訊息：`('claude-opus-5-5', 'xhigh')` **214 則，單一元素**，等於有效 mapping。Return 前的全程核對由派工者依 §3.6 執行。
- **Capability escalation**：不提出（Bindings §3.2 沒有 `primary_reviewer` 的 escalation；本審查的每個判斷都能以原始檔案與我自行執行的檢查作出）。

## 0. Assurance（Bindings §5 兩欄）

### (a) Context independence（治理 §2.3；Bindings §3.7）

| Property | 滿足方式 |
| --- | --- |
| 1 Independent context | 非 fork 的 `gov-primary-reviewer` subagent，從空白 context 開始，沒有繼承 Executor、Orchestrator 或任何 Ticket Reviewer 的對話與推理。派工內容是契約、紀錄與 subject 的路徑與識別、交給本 audit 的項目清單與操作規則；其中的敘述（「後續 commit 只動 `doc/governance`」「ZIP 由 `f56461b` 打包」「#74–#78 已結案」、各項的簡述）我都當作待驗證主張，本 record 的結論全部來自我自己讀取的檔案與執行的檢查（§10）。 |
| 2 Verifiable binding | 檔頭的 transcript 觀測（agentId、model、effort、則數）。 |
| 3 Autonomous access | 自行讀取 repo、git 歷史（`git show／diff／log／ls-tree／archive／grep`，不做 git 寫入）、GitHub issue #59–#67、#73–#78、未追蹤的 ZIP 與打包 manifest、作者材料的 hash、subagent transcript 的 model 欄位；自己執行 pytest、Node 測試、`offline_scan`、獨立的引擎與控制器探測、PI 獨立重算、mutation、ZIP 核對、學號比對，以及以自己啟動的 headless Chrome／Edge（全新 scratchpad profile）對 ZIP 解壓頁面與本機兩個 origin 做的整合檢查。 |
| 4 Self-written record | 本檔由我以自己的 Write 工具寫入 Bindings §7 的位置 `home_work_02/doc/governance/audit/spec-SPEC-V2-c1-r1.md`；沒有 commit，沒有修改任何追蹤中的實作、測試、契約或紀錄。 |

### (b) Model diversity（治理 §4.6 V22-17；Bindings §5）

| Assignment | 實際 model（我自行以 Bindings §3.6 的方法掃描 transcript） |
| --- | --- |
| Executor #74（`gov-executor`，agentId `addc2dc935a7822fe`） | `claude-opus-5-5`／`high`，209 則，單一元素 |
| Executor #75（`a5dedd102dd077202`） | `claude-opus-5-5`／`high`，296 則，單一元素 |
| Executor #76（`acd62ed3a70012296`） | `claude-opus-5-5`／`high`，262 則，單一元素 |
| Executor #77（`a7b3c024fa9b13368`） | `claude-opus-5-5`／`high`，434 則，單一元素 |
| Executor #78（`acc8906c845bfc14f`） | `claude-opus-5-5`／`high`，227 則，單一元素 |
| Primary Reviewer（本 Spec Integration Audit，`aa43e1e2fb1e18487`） | `claude-opus-5-5`／`xhigh`，214 則，單一元素 |
| Alternate Reviewer | 未派工 |

Executor 與本 Reviewer 是同一個 model：**無 model diversity**。Bindings §5 與 DA A-8 不宣告 diversity 關係；independence 由 (a) 判定。

## 1. 治理 §4.7 五個範圍的涵蓋（逐項聲明）

本 record 逐項涵蓋治理 §4.7 與 impl-default v2 §6 要求的五個範圍：

| # | 範圍 | 涵蓋處 | 結論 |
| --- | --- | --- | --- |
| 1 | **跨 Ticket invariants**（run designation 第 4–7 點經 CC-V2-1、正式分析不變量、請求隔離、H-1～H-5、DA 裁決在整合 subject 上同時成立） | §2 | 全部成立 |
| 2 | **Spec-level AC coverage**（每條 Spec V2 AC 有證據與 PASS／FAIL；Spec AC 整體涵蓋 derivation §5 分配的 OC boundary；本 Spec 是同一 Outcome Contract 最後一份未結 Spec，另核對全部 derived Specs 的分配合起來涵蓋整個 acceptance boundary） | §3 | 35 條全部 PASS，其中 S-19 的 Pages 部分依 B-10 為 **open item（NOT TESTED, pending merge）**，不判 FAIL；分配沒有缺口或造成歧義的重疊 |
| 3 | **整合行為**（#74–#78 的功能在整合 subject 上一起運作） | §4 | 成立 |
| 4 | **最終 subject 的 verification／audit coverage**（各票 closed subject 與其間的 delta 都有覆蓋） | §5 | 成立：每個非紀錄路徑的變更都落在某一份 closure audit 的受審範圍內 |
| 5 | **Traceability 與 boundary 符合性**（Tickets → Spec V2 → OC §5） | §6 | 成立；SIA-F1 需 Design Authority 判定（allocation／契約語義的 routing signal，不是 boundary 違反） |

## 2. 範圍 1：跨 Ticket invariants

### 2.1 Run designation 第 4–7 點（經 CC-V2-1）與正式分析不變量

| 項目 | 方法 | 結果 |
| --- | --- | --- |
| V1 腳本、核心模組、`model_data`、結果檔（DA A-3 的 sha256） | `git show 3745e9c:<path> \| sha256sum`，並與 `d7f02d4` 比對 | `assets/app.js` `c1ab3f21…82ad`、`assets/hw2core.js` `e75c5d48…2c14`、`assets/model_data.js` `6cf0c11e…a7ac`、`results/model_data.json` `69dc1465…6e61`、`assets/style.css` `60a27016…5f3f`、`assets/vendor/chart.umd.js` `74401d73…d8f3`：兩個 commit 逐一相同 |
| 凍結路徑 | `git diff --stat d7f02d4 3745e9c -- results hw2.ipynb doc/spec doc/brief doc/ticket CONTEXT.md data assets/vendor design requirements.txt .gitignore` | 空 |
| `hw2/` | `git diff --name-status d7f02d4 3745e9c -- hw2` | 只有 `M offline_scan.py`（DA B-2；單檔 `fetch(` 例外，以路徑 `assets/explore_load.js` 為鍵，只豁免 `fetch\s*\(`）與 `A explore_reference.py`；`hw2/report.py`、`package.py`、`pdf_append.py`、`report/external_sources.json`、`report/chrome_capture.js` 無 diff（建置流程不變） |
| 既有測試（I-5、CC-V2-1） | 對 `d7f02d4` 的每個 `tests/` 檔逐一 `git diff --quiet` | 只有 `tests/test_dashboard_static.py` 改變，diff 只有 CC-V2-1 授權的那一條斷言：前四個 `<script src>` 仍是 V1 四檔且順序不變，其後逐一列出六個 V2 腳本 |
| `index.html` | `git diff d7f02d4 3745e9c -- index.html` | 209 行**只有新增**（4 個 hunk：`explore.css` 的 `<link>`、problem 下拉、`#explore` 子樹、六個 `<script src>`）；沒有任何刪除或修改的行，V1 的 DOM 與文字逐字保留 |
| Test evaluation 紀錄 | `hw2/report.py` 的正式紀錄（`run_id` `fe76019b…`）與 `results/` 無 diff；打包 manifest 的 `result_digest` `b53ff286…` | 不變；沒有重跑 notebook（`results/`、`hw2.ipynb` 無 diff），沒有新的 Test evaluation |
| 探索程式不讀 `model_data`（B-9） | `grep MODEL_DATA\|model_data\|test_inputs` V2 檔案 | 只在說明註解出現（`explore_engine.js` 第 104 行、`explore_reference.py` 第 8 行），沒有任何程式引用；靜態測試 `test_exploratory_files_never_read_model_data_or_test_inputs` 通過 |
| V1 紀錄 | `doc/spec/SPEC.md`、`doc/ticket/tickets.md`、`doc/brief/BRIEF.md` 無 diff；`gh issue view 59..67` | #59–#67 皆 CLOSED，`updatedAt` 都在 2026-10-19 或之前 |
| 四個 seams、不新增 E2E／CI（第 5 點） | diff 路徑清單 | 沒有 `.github/`、`package.json` 或新的依賴；新測試都屬四個 seams（`tests/test_explore_docs.py` 是 README／報告的文件測試，延伸 V1 `test_report.py` 的同類測試，不是第五個 seam） |
| 學號（第 7 點，BR-03） | §2.3 H-1 | 0 命中 |

### 2.2 請求隔離（Brief V2 §5.6；Spec「離線與請求隔離」；DA D-1、I-2）

- 靜態：V2 檔案中 `fetch(` 只有 `explore_load.js` 第 442 行 `defaultFetch` 一處，只在 `fetchCsvBytes()` 使用；沒有 `XMLHttpRequest`、`WebSocket`、`EventSource`、`sendBeacon`、`importScripts`、`import(`、`Worker`。請求 init 恰為 `{ method: 'GET', credentials: 'omit', redirect: 'error' }`（另加 abort 的 `signal`），沒有自訂 header（第 435–439 行）。V2 腳本與 `index.html` 沒有寫死任何 URL（`grep https?://`：只有錯誤訊息中的 `http://`、`https://` 字樣）。`python -m hw2.offline_scan`：repo 與 ZIP 解壓副本各 13 檔、**0 findings**。
- Node（我自己的控制器探測，注入計數 `fetchImpl`，並以 getter 陷阱攔截 `localStorage`／`sessionStorage`／`indexedDB`）：`init()`、選 King County、選 50 Startups、以本機文字載入 → **0 次**呼叫；提交 URL → **恰 1 次**，init 的鍵只有 `method`、`credentials`、`redirect`（＋`signal`）；fetch 失敗 → `URL_FETCH_FAILED`／`network`，等待後仍只有 1 次；整個探測對 storage 的存取 0 次。
- 瀏覽器（§4 的整合檢查）：ZIP 解壓頁面在 `file://`、DevTools 離線下的全部操作，非 `file:`／`data:` 請求 0；從 `http://127.0.0.1:8961` origin 提交另一個 origin（`:8962`）的 CSV URL：伺服器紀錄每次提交恰 1 個 `GET`、沒有 `OPTIONS` preflight、沒有 cookie；改選目標欄重新執行 0 個請求（Chrome、Edge 相同）。

### 2.3 高風險類別（DA derivation §7.4 Spec Integration Audit 列：H-1～H-5；A-2、A-3、A-4、A-5、A-6、A-9、A-7）

**H-1（A-4）**：比對值只在記憶體中讀自 `.local/packaging.json`，不印出。`git grep -F` 在 `3745e9c` 與 `HEAD` 的樹 0 命中；`d7f02d4..HEAD` 34 個 commit 每個的樹 0；commit message 0；issue #73–#78 的標題、本文與留言 0。ZIP 67 個項目的內容 0（檔名與頂層資料夾依老師規則含學號，屬未追蹤的繳交物）。`git ls-tree -r 3745e9c home_work_02` 中的 `.pdf` 只有 `doc/requirement/` 的老師文件；沒有 `.zip`、`.env`、`kaggle.json`、`acceptor_materials/`、`.local/`、`dist/`；`git status --porcelain home_work_02` 為空。V2 diff 新增內容中的 URL 主機只有老師公開的範例 URL（`raw.githubusercontent.com/Avik-Jain/…/50_Startups.csv`）、`localhost`／`127.0.0.1`、測試用的保留網域 `example.org` 與探測字串 `evil.example`。**PASS。**

**H-2（A-6）**：ZIP 核對見 §3 S-34；OV-1 重做見 §4（Chrome 與 Edge）；README「作業要求對應」兩列加分與「>13」見 S-31。**PASS**（SIA-F1 涉及 dashboard 的需求來源標示，見 §7）。

**H-3（A-2(V2)、A-3(V2)）**：(i) 正式分析不變見 §2.1。(ii) 我自己執行全部 pytest（含三層邊界、聚合與凍結、King County 一致性、取消／失敗／略過、可重現性、Node 對 Python 參照）與 Node 測試，全部通過；另以自己的探測驗證凍結、第二層只看訓練列、可重現性、三種入口、單位無關（§4.1），並以 numpy／scipy **獨立重算**四個探索 test 模型的逐筆 PI、covered、coverage 與指標（50 Startups 的 `allin`、`forward_sfs_k01`；我自己產生的 160 列混合資料的 `allin`、`lasso_path_k06`）：點預測、PI 上下界、指標的最大相對差 ≤ 7.3e-11，`covered` 逐筆相同，coverage 相同。(iii) README 與報告模板對 50 Startups 的 test 指標、逐筆預測、CV 平均與係數的 162 種格式字串 **0 命中**。**PASS。**

**H-4（A-5(V2)）**：50 Startups sha256 從 blob 重算 `c6075ca5…630d`，等於 README、`50_Startups.SOURCE.md`、`startups50.js`、ACCEPTANCE V2-4 的紀錄值；blob id `14ffb860…` 等於 SOURCE 的紀錄；授權陳述追溯到 `50_Startups.LICENSE.md` 與 SOURCE 記錄的 `LICENSE` blob 與來源 commit（I-3）。作者材料 sha256：ChatGPT PDF `0a5d29e3…`、NotebookLM 報告 `77b8f7e7…`、來源清單 `141c211b…`，與 `hw2/report.py` `ACCEPTOR_MATERIALS` 相同。ACCEPTANCE G 節：V2-1～V2-43 與 G.1 對照表的狀態，我以 §3、§4 的獨立檢查抽核（V2-1、2、3、6、7、18、19、21～25、29～31、33、37、40、41、42、43），沒有發現證據不符；Pages 記 NOT TESTED（pending merge），best effort 項目記 NOT TESTED，沒有無證據的 PASS。替換資料截圖的註記（#75 R1-F4）已在 V2-11、V2-15、V2-17。Scope class 標示（I-4）：+1、+2 標〔老師要求（新版作業頁的加分）〕，「兩種 problem＝同頁下拉」寫明是本專案解讀，探索能力集合標〔專案延伸〕。**PASS**，另有 SIA-F1、SIA-F2（Low）。

**H-5（A-9）**：列舉 V2 檔案（`assets/explore_*.js`、`assets/data/startups50.js`、`index.html` 的 V2 部分）中 A-9 所列 API：`innerHTML`、`outerHTML`、`insertAdjacentHTML`、`document.write`、`DOMParser`、`createContextualFragment`、`srcdoc`、`eval`、`new Function`、字串型計時器、對 `src`／`href`／`location` 的指派、web storage、`document.cookie`、`history.*State` **0 命中**；唯一的 `postMessage` 是 `explore_ui.js` 第 653 行 `MessageChannel` 排程器傳常數 0。`index.html` 沒有 inline script 與 inline 事件屬性。`explore_ui.js` 的 `el()` 只以 `textContent`、`createTextNode` 與非 URL 屬性寫入；所有呼叫的屬性鍵只有 `class`、`text`、`scope`、`colspan`、`rowspan`、`type`、`id`、`for`、`step`、`inputmode`、`aria-pressed`、`data-method` 與兩處 `style`（值是程式內的方法顏色常數，不是資料）；`<option>` 以 `.text`／`.value` 寫入（D-2）。瀏覽器探測（ZIP 頁面、`file://`、離線、Chrome）：本機檔案載入我構造的 70 列 CSV，欄名 `<img src=x onerror="document.title='pwn'">`、`</script><b>b</b>`、`<style>body{display:none}</style>`、`__proto__`、`constructor`，目標欄 `<script>alert(1)</script>`，類別值 `<svg onload=alert(2)>`、`"><iframe src=//evil.example>`、`javascript:alert(3)`、`a&amp;b`；點遍五個方法與全部 k：`COMPLETED`（21 個候選）、九個字串全部以字面文字出現、`#explore` 內 `img／svg／iframe／script／style／b／object／embed／javascript: 連結` 0 個、`document.title` 不變、`body` 仍顯示、預測器輸入 5 個（含 `__proto__`、`constructor`）、非 `file:` 請求 0、dialog 0、例外 0，切回 King County 後 V1 區塊文字不變。**PASS。**

**A-7**：本 record 沒有 blocking finding，沒有 deferral。

### 2.4 DA 裁決在整合 subject 上同時成立

| 裁決 | 核對 | 結果 |
| --- | --- | --- |
| D-1（一次讀取的嚴格讀法） | §2.2：init、無自訂 header、無 preflight、不重試；重新導向以 `redirect: 'error'` 落到 `URL_FETCH_FAILED`／`network` 並給出檔案指引（頁面訊息原文含「該網址會重新導向（本頁不跟隨重新導向）…以下方的「本機 CSV 檔案」載入」） | 成立 |
| D-2、B-14（輸入字串只當資料） | §2.3 H-5 | 成立 |
| I-2（單檔例外、不寫死 URL） | §2.2；`offline_scan.py` diff | 成立 |
| I-3（50 Startups 的授權與來源） | §2.3 H-4；`.gitattributes` 以 `assets/data/** -text` 固定位元組 | 成立 |
| I-4（報告與 README 無探索數字、標示） | §2.3 H-3 (iii)、H-4 | 成立 |
| I-5（既有測試不變） | §2.1 | 成立 |
| G-1～G-5 | §3 S-13、S-01、S-29、S-06／S-17、S-26 | 成立 |
| R3-1～R3-3（V1 頁尾是 V1 區塊、探索時隱藏、文字不變） | 瀏覽器：50 Startups 與自訂資料集時 `footer.footer` 的 computed `display` 為 `none`，King County 為 `block`；切回後頁尾 `textContent` 與初始逐字相同（Chrome、Edge）；`explore_ui.js` 不含 `footer`（靜態測試） | 成立 |
| R3-6（README 頁面層級陳述） | README 第 21–24 行：零請求的檢視與「唯一的對外請求」分列；King County 檢視才是「只讀取匯出的結果」 | 成立 |
| R4-1（任何提前結束都套 A-2） | 引擎與參照的 `lasso_path_degenerate` 附 `cause`；Node `R4-2` 測試；我的 twin 欄探測：六個 row set 都是 `active_set_degenerate`、All-in `INVALID_MODEL`、相依診斷列出 `a`、`a_twin`，頁面原因文字為「要加入的欄與路徑中已有的欄線性相依（active set 退化）」 | 成立 |
| R4-2（原因如實） | `explore_app.js` `causeText` 對 `path_ended` 以「例如」列可能情形；數值停止寫「數值／上限」；`target_constant` 有自己的原因（Node 測試） | 成立（README／報告的列舉不完整見 SIA-F2） |
| R4-3、R4-4（與目標單位無關；tie 同） | 測試以 c＝1e-12、1e-10、1e-9、1e-6、1e6 驗證；我另以測試沒有用過的 c＝1e-14、2.5e-8、1e3、1e9，對 50 Startups 與我自己的 7 個 group、含缺值列的混合資料執行：候選狀態、canonical 與各 fold 子集、原因、Lasso 已進入數／停止原因／進入順序、winners、groups **全部相同**；entry alpha 與 c 倍原值的最大相對差 7.1e-14；twin 資料乘 1e-11 亦相同。`tests/test_explore_kc_consistency.py` 未改且通過；`hw2/selection.py` 無 diff | 成立 |
| C1-R1、C1-R2（取消等待與載入上限 50,000 × 60） | `LIMITS = { maxRows: 50000, maxColumns: 60, minRows: 20 }`；All-in 沒有預算（`BUDGETS` 只有四個路徑方法） | 成立 |
| C1-R3（執行中、取消中、等待中進度即時） | 瀏覽器（中型資料，15,000 列 × 22 欄、100 個編碼欄、89 個候選）：同一個長候選期間「已耗時」0.7→1.5 秒持續前進（候選數未變）；按取消後「取消中：目前的候選算完後（下一個候選邊界）停止…已耗時 4.4→4.6 秒」；Node 探測 heartbeat 的 `elapsed_ms` 單調、取消後 `cancelling: true` | 成立 |
| C2-R1～C2-R3（無位元組上限；超限一律 `TOO_LARGE`；大小造成的環境失敗如實說明、不新增原因碼） | 程式中沒有位元組上限；`REASONS` 與 `URL_CAUSES` 與 Spec 的枚舉逐一相同。Node 探測以 `options.decode` 強迫走位元組路徑：50,001 列 → `TOO_LARGE`（`rows_over: 50000`）、61 欄（解碼器回傳空字串）→ `TOO_LARGE`（`columns: 61`）、上限內但解碼器拋一般 `Error` → `reason: null` 加 `environment_error`（`stage: 'decode'`）、`TypeError` → `ENCODING` | 成立 |
| CF-1（尾段取消） | Node：在 `diagnostic` 事件與第一個 winner 的 test 步驟注入取消 → `CANCELLED`、結果只有 `meta` 與 `run`；之後重跑的確定部分與未取消的完整執行相同。排程控制器（8,000 列資料，phase 進入 `diagnostic` 時按取消）：`cancel()` 回傳 `true`，即時文字「取消中：全部候選已完成，正在進行的共線診斷或探索 test 步驟完成後停止，不顯示任何結果。已耗時 5.1 秒」，結果 `CANCELLED`、沒有 `candidates`／`winners`／`test`／`dependencies`，trace `start → cancel → end:CANCELLED`。`index.html` 第 95 行與「方法與限制」涵蓋尾段 | 成立 |

## 3. 範圍 2：Spec-level AC coverage

Spec V2 rev 2 的 AC 是它的 Testing Decisions（四個 seams）、人工檢查表與「文件、README、報告與打包」的交付要求；下表逐條列出（S-xx 是本 record 的編號），附我取得的證據與判定。「pytest」指我在主 checkout 執行的 `.venv/Scripts/python -m pytest -q -rs -p no:cacheprovider`：**478 passed、0 skipped**（188 s）；「Node」指 `node --test` 六個探索測試檔：**88 pass、0 fail、0 skipped**（Node v24.19.0）；`core.test.js` 9 pass、3 skipped（fixture 案例由 pytest `test_node_core.py` 執行，V1 既有行為）。

| ID | Spec V2 AC | 證據 | 判定 |
| --- | --- | --- | --- |
| S-01 | 主 seam 資料 (a) 50 Startups、(b) synthetic 非退化、(c) synthetic 退化（完全共線、和欄、相等 entry）、(d) 恰 20 列／單一類別欄／全部數值 | `tests/test_node_explore.py` `CASES`：`startups50`、`synthetic_mixed`、`degenerate_mixed`、`a1_collinear`、`edge_twenty_rows`、`edge_single_categorical`、`edge_all_numeric`（G-2） | PASS |
| S-02 | 主 seam 驗證內容（欄位型態與訓練列狀態、切分與 fold、候選狀態與原因、VALID 的各 fold 子集與指標、CV 平均與 std、canonical 子集、係數、s²、df_resid、winners 含平手、test 只對 winner、相依欄位組、Lasso entry alpha 與順序或退化步） | pytest `test_node_explore_contract_matches_the_python_reference`（驅動 `explore_contract.test.js`）、`test_winner_rules_on_injected_candidates`、`test_degenerate_fixture_semantics`；我的 PI 獨立重算（§2.3 H-3） | PASS（參照的 active-set 退化分支未被測試，SIA-F4） |
| S-03 | 聚合與凍結（CV＝fold 算術平均；改 test 列目標只改 test） | pytest `test_cv_metrics_are_the_arithmetic_mean_of_the_fold_metrics`、`test_changing_test_targets_moves_only_the_test_numbers`；我的探測：50 Startups 與混合資料把 test 列目標改為 3y+1000 → 候選（狀態、原因、CV、canonical、fold、係數）、winners、Lasso 路徑、groups、相依診斷全部相同，test 改變 | PASS |
| S-04 | 可重現性（兩次逐值相同；三種入口相同） | Node `explore_run.test.js`；我的探測：兩次執行的確定部分 JSON 逐字相同；位元組（檔案／URL）、文字、內建全域三種入口的確定部分相同 | PASS |
| S-05 | 取消與失敗（第 n 個候選後取消 → `CANCELLED`；注入例外 → `FAILED`；預算超出 → `SKIPPED_RESOURCE_LIMIT` 且以計數證明未執行） | Node `explore_run.test.js`（31 項）；pytest `test_reference_budget_skips_whole_methods_and_keeps_all_in`；我的 CF-1 與控制器探測（§2.4） | PASS |
| S-06 | 50 Startups 全部 k 有效由 fixture 證明 | pytest `test_startups50_every_candidate_is_valid_and_the_split_is_80_20`、`test_g4_startups50_under_the_final_budgets_runs_every_method`；我的探測：最終預算常數（Forward／Backward／RFE `2e11`、Lasso `8e10`）下 `COMPLETED`、17／17 `VALID`、五種方法（G-4） | PASS |
| S-07 | King County 一致性（通用參照重現四條 canonical 路徑與 All-in；不取代 (a)～(d)） | pytest `tests/test_explore_kc_consistency.py` 2 項；`test_the_reference_module_is_not_imported_by_any_formal_path` | PASS |
| S-08 | 契約不變量以通用檢查函式驗證每份結果 | pytest `test_reference_cases_meet_the_contract_invariants`；JS 端同類檢查在 `explore_contract.test.js` | PASS |
| S-09 | 載入契約（每個拒絕原因、BOM／引號／空白／科學記號／負數／空儲存格、缺值刪列與不足 20 列、目標預設與指定、重複欄名；`LoadResult` 不含保留／排除狀態） | Node `explore_load.test.js` 15 項；`REASONS` 與 Spec 枚舉相同 | PASS |
| S-10 | 三層邊界（第二層只看訓練列、第三層只看該 fold 訓練列、canonical 只看整個訓練集） | Node `explore_boundary.test.js` 7 項；我的探測：只在 test 列變化的欄 `tconst` → `EXCLUDED_CONSTANT`（`n_distinct_train: 1`），只在 test 列出現的層級 `ZZ_test_only` 不影響 groups 與任何選擇（test 中計為未見層級 1 筆） | PASS |
| S-11 | 請求隔離（mock fetch 前四條與第五條） | Node `explore_app.test.js`、`explore_custom.test.js`；我的控制器探測（§2.2） | PASS（晚到回應的世代檢查未被測試，SIA-F5） |
| S-12 | 離線靜態掃描照跑；只有探索載入模組允許 `fetch(` | pytest `test_offline_scan_exception_is_one_path_and_fetch_only`、`test_fetch_appears_once_and_only_in_the_load_module`；`offline_scan` repo 與 ZIP 副本各 0 findings | PASS |
| S-13 | King County 不變（`model_data` 測試照跑；V1 區塊 DOM／靜態文字結構快照） | pytest `test_v1_blocks_match_the_pre_ticket_snapshot`、`test_the_snapshot_is_the_accepted_baseline_page`、`test_v1_files_have_no_diff_from_the_accepted_baseline`、`test_model_data_official.py`；§2.1 sha256 | PASS |
| S-14 | 內建資料一致（內嵌文字＝`.csv`＝紀錄 sha256） | pytest `test_embedded_50_startups_text_equals_the_csv_and_the_recorded_sha256`、`test_bundled_data_is_byte_pinned`；§2.3 H-4 的 blob 重算 | PASS |
| S-15 | 既有 dashboard 靜態測試照跑（分層、test 數字只讀 `model_data`、核心模組不含選擇程式碼） | `tests/test_dashboard_static.py` 除 CC-V2-1 斷言外未改，全部通過 | PASS |
| S-16 | 人工 §8-1：下拉三項；King County 逐字相同 | ACCEPTANCE V2-1、V2-2、V2-24、V2-37；我的瀏覽器：選項依序「King County 房價（正式分析）／50 Startups 利潤（探索）／自訂資料集（探索）」、label「分析問題（Problem）」；探索與載入失敗後切回，五個 V1 區塊與頁尾的 `innerText` 與初始逐字相同（Chrome、Edge） | PASS |
| S-17 | 人工 §8-2：50 Startups `file://` 斷網選取即完成，五種方法、winner、test、PI 圖、預測器；時間只記錄 | V2-3、V2-10、V2-14、V2-37、V2-40；我的瀏覽器（ZIP 頁面、離線）：Chrome 57 ms、Edge 56 ms 完成，方法按鈕 5，結果區塊（資料、模型、預測器、test、方法與限制）都顯示，非 `file:` 請求 0 | PASS |
| S-18 | 人工 §8-2a：預測器只在 `VALID` 可用，否則停用並顯示狀態與原因 | V2-5、V2-11；`explore_ui.js` 第 398–407 行（`view.enabled` 為假時不建立輸入、顯示狀態與原因）；Node `explore_app.test.js` 的 `predictorView` 案例 | PASS |
| S-19 | 人工 §8-3：老師 URL「於 Pages 上」載入，內容 sha256 相同時與內建一致 | V2-18（`http://localhost` 重現，含老師 URL）；我以另一個本機 origin 提供同一份位元組（sha256 相同）重現 URL 入口：結果與內建逐字相同、恰 1 個 GET（Chrome、Edge）。**Pages 部分**：V2-42 NOT TESTED（pending merge），依 DA B-10／I-1 屬合併後的 Lightweight work item | PASS（localhost）；Pages＝**open item（B-10）**，不判 FAIL |
| S-20 | 人工 §8-4：同一份 CSV 以檔案載入，數字一致 | V2-19；我的瀏覽器：檔案入口的 test KPI、選取候選與預測值與內建逐字相同（Chrome、Edge） | PASS |
| S-21 | 人工 §8-5：各失敗訊息；超出預算標 `SKIPPED_RESOURCE_LIMIT` | V2-21、V2-27、V2-28、V2-32；Node 失敗案例；我的瀏覽器：沒有 CORS 的 URL →「URL 讀取失敗（URL_FETCH_FAILED，network）：網路或跨來源限制…請用瀏覽器下載該 CSV，再以下方的「本機 CSV 檔案」載入」；C2-R3 探測 | PASS |
| S-22 | 人工 §8-6：每個探索區塊有標示，King County 沒有 | V2-6；我的瀏覽器：顯示中的每個 `.ex-block` 標題都含「探索執行，非正式評估」，五個 V1 區塊都不含；靜態測試 `test_every_exploratory_block_is_labelled`、`test_v1_blocks_carry_no_exploratory_label…` | PASS |
| S-23 | 人工 §8-7：頁面載入與 King County／50 Startups 零請求；自訂 URL 一次讀取 | V2-7、V2-22、V2-23、V2-37；§2.2 | PASS |
| S-24 | 人工 §8-8：Node 對 Python／sklearn 參照 | V2-14、V2-16、V2-33、V2-43；pytest 與 Node 全部通過 | PASS |
| S-25 | 人工 §8-9：OV-1、SR-09 因 UI 變動重做 | V2-37、V2-38；我在 ZIP 解壓頁面獨立重做 OV-1（§4）；SR-09 (b)～(g) 的互動量測我沒有重做，依 `doc/screenshots/v2-issue78/ov78_*.json` 與 #78 R1 的逐值核對；我觀察到的 King County 首次繪製 191～274 ms（門檻 3,000 ms） | PASS |
| S-26 | acceptor 追加三條：三向切換；URL 失敗後改以本機 CSV 成功；探索執行或失敗後 King County 不變 | V2-24、V2-21、V2-37；我的瀏覽器：King County → 50 Startups → 自訂（檔案）→ King County → 自訂（面板清空、目標欄停用、URL 欄空白，G-5）→ 50 Startups（重新執行，結果相同）→ King County；URL 失敗後檔案載入成功且與內建相同；King County 文字逐字不變 | PASS |
| S-27 | 效能：50 Startups 與中型資料集的實測時間、瀏覽器、硬體；不設門檻 | V2-40；我的量測：50 Startups 執行 21～22 ms（頁面訊息）；中型資料 89 個候選 Chrome 46.6 s、Edge 47.1 s | PASS（只記錄） |
| S-28 | 非阻塞與取消（中型資料：下拉、輸入、取消可操作；進度持續更新；無「沒有回應」；取消 → 已取消、無結果區塊；重跑從頭） | V2-30；我的瀏覽器（Chrome、Edge）：執行中每 0.7 s 在 URL 欄寫入文字（各次 3～28 ms 完成、值正確），取消按鈕可用，進度與已耗時持續更新；取消後「已取消：取消在下一個候選邊界生效，停止時已完成 1／5 個方法（17／89 個候選）…」（Edge 16／89），五個結果區塊都隱藏；重跑完成並顯示全部結果；dialog 0、例外 0 | PASS |
| S-29 | 可重現性（人工）：同一份資料連續兩次，顯示的確定部分相同 | V2-31；我的瀏覽器：50 Startups 重跑的 test KPI 逐字相同；Chrome 與 Edge 對 50 Startups 與中型資料顯示的 test KPI、選取候選、預測值逐字相同（G-3） | PASS |
| S-30 | OV-2～OV-5 對新增控制項與區塊（AD-1 的 gate 分類） | V2-8、V2-17、V2-26、V2-39；我的 OV-2 抽查：375／768 px 下 King County、50 Startups、自訂資料集三個檢視 `scrollWidth`＝`clientWidth`（375＝375、753＝753），無水平溢出；OV-4 下拉的 label、`aria-describedby`、`aria-controls` 存在（靜態測試）；OV-5 對比我沒有重測，依 V2-39 證據與 #78 R1 核對；best effort 記 NOT TESTED | PASS |
| S-31 | README：功能說明、「作業要求對應」兩列（+1、+2 → 操作與驗收位置）、限制與揭露、50 Startups 來源與授權、「>13」 | V2-35；README 第 21–24、84–86、129–181 行；pytest `tests/test_explore_docs.py` 8 項 | PASS（SIA-F2 為 Low） |
| S-32 | 報告新增「探索模式」一章；正式分析各章數字不變；建置流程不變 | V2-36；`report/report.md` 第 12 章；pytest `test_every_other_part_of_the_report_is_the_accepted_baseline`；建置程式無 diff；探索數字 0 命中 | PASS（SIA-F1、SIA-F2 為 Low） |
| S-33 | ACCEPTANCE：既有條目保留；新增 V2 條目（§8 的 1～9、2a 與 acceptor 三條） | G 節 V2-1～V2-43、G.1 對照、G.2 量測；A～F 節除 #75 R1-F4 的註記外不變 | PASS |
| S-34 | 打包：新增資源進 ZIP；ZIP 與 Pages 的 dashboard 相同；記錄 sha256 與清單 | 我自己的 ZIP 核對（`python -I`）：sha256 `57e1e4a4…bcd11`（81,620,529 bytes）等於 `dist/hw2_package_manifest.json` 與 V2-41；`testzip()` 無錯；67 項與 `doc/screenshots/v2-issue78/zip_manifest.txt` 逐項 size／sha256 相同（notebook 項目在 manifest 以 `<學號>` 記名，sha256 `2e2f8afc…` 相同）；`index.html` 與 `assets/` 17 檔與 `3745e9c` 的 blob **逐位元相同**（Pages 發布的就是這些 blob）；其他追蹤檔 47 個中 11 個相同、36 個 CRLF→LF 後相同、0 個不同；3 個產生物（notebook、報告 PDF、ChatGPT PDF） | PASS（SIA-F3 為 Low） |
| S-35 | 單元 `.gitignore` 不改；學號規則（BR-03）不變 | `.gitignore` 無 diff；§2.3 H-1 | PASS |

### 3.1 Spec AC 對 derivation §5 分配的涵蓋

- derivation §5.1 把 V2 的整個 acceptance boundary 分配給 Spec V2 rev 2：Brief V2 §8 第 1～9、2a 條與數值驗證定義（S-01～S-08、S-16～S-25）、§5.6 隔離（S-11、S-12、S-23；§2.2）、§7 交付物（S-31～S-34）、§3.5 四項覆寫（覆寫 1：README 第 24 行與 S-31；覆寫 2：§2.2；覆寫 3：Submission package 由 README 記述、繳交本身屬 RB-2；覆寫 4：「>13」S-31）、Spec V2 的 Testing Decisions 與人工檢查表（S-01～S-30）、四個 seams、依賴（§5）、V1 保持要求（§2.1）。
- derivation §5.2 的 G-1～G-5 都有承接與證據（§2.4 表）。
- derivation §5.3 不由 run 承擔的項目（Pages 檢查、合併、push、繳交、向老師確認）不是分配缺口：Pages 是 B-10 的 open item，其餘是 acceptor 的保留動作。
- **沒有分配缺口，也沒有造成歧義的重疊**（SIA-F1 是兩項 accepted 要求之間的張力，屬 Design Authority 的 allocation 判定，不是分配缺口）。

### 3.2 本 Spec 是同一 Outcome Contract 最後一份未結 Spec：全部 derived Specs 的分配合起來

- V1 boundary（OC §1–§4）全部分配給 Spec rev 5（`derivation-SPEC.md` §4）：其 Spec Integration Audit `audit/spec-SPEC-c1-r1.md` 為 `VERDICT: CLOSURE`；DA phase acceptance `decision-20261019-phase-acceptance-SPEC.md`「PHASE ACCEPTED — SPEC rev 5（#59）」；AD-3 移出的 Pages 項目由合併後的 Lightweight item 承擔，`audit/20261019-ad3-pages-check-c1-r1.md` 為 `VERDICT: CLOSURE`。
- V2 boundary（OC §5）全部分配給 Spec V2（上一節），V2 對 V1 條款的覆寫由 Spec V2 承擔新版本的驗收。
- V1 保持要求在整合 subject 上成立（§2.1）。
- **合起來涵蓋整個 Outcome Contract 的 acceptance boundary**；唯一未執行的部分是 V2 的 Pages 檢查（B-10，pending merge），與 V1 AD-3 同型，依 derivation B-10 與 §5.3 是 open item，不是缺口。

## 4. 範圍 3：整合行為（#74–#78 在整合 subject 上一起運作）

### 4.1 引擎與控制器（Node，我自己的探測；`git archive 3745e9c` 的匯出）

見 §2.2、§2.4 與 §3 S-03～S-06、S-10。另：我自己的 160 列混合資料（5 個數值欄、2 個類別欄、3 列缺值）`COMPLETED`、刪除 3 列、29 個候選全部 `VALID`；不並行：執行中再次選 50 Startups → 第一次 `null`、trace `CANCELLED, COMPLETED`；三向切換在控制器層面 0 次 fetch。

### 4.2 瀏覽器（整合 subject 的 ZIP 頁面；Chrome 155.0.8059.85 與 Edge 155.0.4283.62，headless、全新 scratchpad profile）

- **階段 1（OV-1 重做，A-6）**：ZIP 解壓的 `index.html`，`file://`，DevTools 離線、沒有伺服器。King County 五個 V1 區塊與頁尾顯示 → 50 Startups 完成（五種方法、標示、頁尾隱藏、V1 區塊隱藏）→ 自訂（只有輸入面板）→ 本機檔案（與內建相同）→ King County（V1 文字與初始逐字相同、頁尾顯示）→ 自訂（清空）→ 50 Startups（重跑相同）→ King County（仍相同）。非 `file:`／`data:` 請求 0；`localStorage`、`sessionStorage` 長度 0，`location.search`、`location.hash` 為空。兩個瀏覽器結果相同。
- **階段 2（URL 入口，DA I-1 的 http origin）**：頁面在 `http://127.0.0.1:8961`，CSV 在 `http://127.0.0.1:8962`：允許 CORS 的 URL → 一個 GET、結果與內建相同；改選目標欄 → 0 個請求；不允許 CORS 的 URL → 一個 GET、`URL_FETCH_FAILED`／`network` 與檔案指引；之後本機檔案成功。
- **階段 3（非阻塞、即時進度、取消、重跑）**：見 S-28、§2.4 C1-R3。
- **King County 在探索後不變**：另一個檢查在 http 頁面上比較探索前與探索後（50 Startups、檔案、中型資料執行中取消）的 King County 文字：**0 差異**。跨 origin（`file://` 與 http）的唯一差異是 V1 測試區塊的「首次繪製：… ms」量測值（V1 既有、每次載入不同的量測顯示），不是探索造成。
- **H-5 探測**：§2.3。
- **OV-2 抽查**：S-30。

結論：#74 的下拉、內建資料與 All-in 鏈，#75 的四種方法、winners、退化與診斷，#76 的 URL／檔案入口與請求隔離，#77 的預算、非阻塞、取消（含尾段）、進度與可重現性，以及 #78 的 README、報告與 ZIP，在整合 subject 上一起運作，彼此沒有破壞對方的不變量。

## 5. 範圍 4：最終 subject 的 verification／audit coverage

| 票 | Closure audit 的受審範圍（BASE..subject） | 最後 verdict |
| --- | --- | --- |
| #74 | R1 `506581a..f4e487c`；R2 `f4e487c..9e99a10` | `issue-74-c1-r2.md` CLOSURE |
| #75 | R1 `3dfba2d..ded2769` | `issue-75-c1-r1.md` CLOSURE |
| #76 | R1 `450bcff..a4b6c76`；R2 `a4b6c76..9ac8499` | `issue-76-c1-r2.md` CLOSURE |
| #77 | R1 `4bd6a59..9d5a840`；R2 `d7147ba..31a2255` | `issue-77-c1-r2.md` CLOSURE |
| #78 | R1 `2b658b3..3745e9c` | `issue-78-c1-r1.md` CLOSURE |

- 各範圍之間的 delta（`d7f02d4..506581a`、`9e99a10..3dfba2d`、`ded2769..450bcff`、`9ac8499..4bd6a59`、`9d5a840..d7147ba`、`31a2255..2b658b3`）以及 `3745e9c..33107ed`：`git diff --name-only` 只有 `home_work_02/doc/governance/**`（record-only）。
- 聯集核對：`d7f02d4..3745e9c` 中每一個非 `doc/governance/` 的路徑都出現在上表某個受審範圍的 diff 中，**沒有未受審的實作或證據 delta**（`460d248` 對 `doc/acceptance`、`doc/screenshots` 的修改在 #78 R1 的範圍內）。
- 整合 subject 的驗證由本 audit 執行（§2–§4）：pytest 478／0 skipped、Node 88／0 skipped、`offline_scan` 0 findings、獨立探測、兩個瀏覽器的整合檢查、ZIP 核對。未追蹤的 ZIP 由 `f56461b` 打包；`git diff --name-only f56461b 3745e9c` 只有 `doc/`，ZIP 不含 `doc/`，所以 ZIP 的每個項目與 `3745e9c` 的對應內容相同（S-34）。
- GitHub 上 #74–#78 仍是 OPEN（未 push，run record §9 說明由 acceptor 的 push／merge 決定時處理）；本 run 的權威結案紀錄是 run record 與上列 audit records。

## 6. 範圍 5：Traceability 與 boundary 符合性（Tickets → Spec V2 → OC §5）

- **引用鏈**：#74–#78 的本文都以「Parent #73」與共同條款引用 Spec V2 rev 2 與 Brief V2 rev 2＋E-1；#73 是 Spec V2；OC §5 接受 `d7f02d4` 的 Brief V2、Spec V2、`tickets-v2.md` 與 #74–#78；`derivation-SPEC-V2.md` 記錄版本識別、boundary determination（B-1～B-14）與分配（§5）。本文 hash 與 accepted 版本相同（檔頭），`d7f02d4..3745e9c` 沒有修改 Spec V2、Brief V2、`tickets-v2.md`、`CONTEXT.md`。
- **Boundary**：`git diff --name-only d7f02d4 3745e9c` 的每個路徑都在 `home_work_02/` 內，沒有 `doc/requirement/`（RB-5）；沒有 root 檔案；沒有新增 OC 以外的功能（Spec V2「Out of Scope」逐項核對：沒有後端、貼上輸入、分組欄、log 開關、Exhaustive／SelectKBest／permutation importance、資料清理、儲存或匯出、探索數字進報告）。B-13（F-1）由 CC-V2-1 解決，修改只限授權的那一條斷言（§2.1）。D-1、D-2、I-1～I-5、R3、R4、C1、C2、CF-1 都是 DA 在 accepted 語義內的裁決，其實作沒有新增原因碼、狀態、seam 或 gate（§2.4）。
- **Push／merge**：沒有 push（`origin` 沒有此 branch，run record 記錄），沒有合併；合併屬 RB-1（OC §5 沒有 SA-3 opt-in）。
- **Boundary 疑義**：沒有需要 fail-closed 的 boundary 問題。SIA-F1 是 accepted 要求之間的張力（H-4 的如實標示 vs 凍結的正式章節文字），依治理 §4.2 是 routing signal，required authority＝Design Authority（§8）。

## 7. Findings

### SIA-F1 — 報告前言、標示對照表、§7.1 與第九章仍以「作業頁正文沒有要求網站」標示 dashboard，與目前的需求來源 SRC-4 不一致；第 12 章沒有說明（#78 R1 F1，交本 audit 判斷是否 material）

- **Severity**：Low。**Blocking**：否。**判定為 material，需 Design Authority 判定**（routing signal，治理 §4.2）。
- **證據**：`report/report.md` 第 9 行「唯一的例外是互動 dashboard：它是老師的**課堂口頭要求**，作業頁與講義文字都沒有要求網站」；第 28 行對照表「互動 dashboard｜老師要求（課堂口頭；作業頁正文沒有）」；第 236 行 §7.1 與第 294 行第九章標題〔老師要求（課堂口頭）〕。`doc/requirement/HW2-req_new-20261021.txt`（SRC-4）寫「主要繳交: 跟 DIC2 一樣github and web」，Brief V2 §3.5 覆寫 1 把 dashboard 與 repository 改為主要交付。README 第 24 行已正確說明（「Dashboard 原是老師的課堂口頭要求（舊版作業頁正文沒有要求網站）；2026-10-21 更新的作業頁把主要繳交改為…」），但報告第 12 章（第 338–390 行）只說明兩項加分，12.5 只限定 §7.1／第九章的資料來源與請求陳述。這份報告隨 ZIP 交付（`hw2_report.pdf`），讀者會看到一句與現行作業頁相反的事實陳述。同類而已有裁決的凍結文字：King County 概覽區塊「作業正文 10–20 與補充 14–39 的交集」（`index.html` 第 264 行；V1 區塊依 Brief V2 §4 逐字保留，「>13」的處理已由 DA B-8 決定只改 README）。
- **依據**：DA derivation §7.2 H-4（V2）「scope class 標示（I-4）」與 Bindings §2.4 的標示規則（宣告的高風險類別）；Brief V2 §3.5 覆寫 1；對立的 accepted 要求：#78 AC「正式分析各章內容與數字不變（與上一版報告逐章比對，只有新章節與日期不同）」、I-5（`tests/test_report.py` 鎖定「老師要求（課堂口頭」與 §7.1、第九章標題）。
- **為何 material**：(1) 陳述的對象是「老師要求了什麼」，屬 DA 宣告的高風險類別 H-4；(2) 它出現在交付的報告中，且與現行上位契約 SRC-4 相反；(3) 在不改凍結文字的前提下，唯一的修正位置是第 12 章（例如 12.5 加一句），但沒有任何 AC 或 DA 分配要求這句——要不要加是 allocation 的判定，我不得自行補寫需求。
- **為何不 blocking**：標示的類別「老師要求」仍然正確，只有來源限定詞過時，方向是低估而不是把專案延伸冒充成老師要求；主要交付的 README 已正確；報告在 SRC-4 下是 optional；凍結文字由 accepted AC 與 I-5 保護，Executor 不改它們是正確的；沒有任何 accepted 條款被違反。
- **具體 ambiguity（交 Design Authority）**：Spec V2「報告：新增『探索模式』一章（…限制與洩漏揭露）」與 H-4 的如實標示，是否要求第 12 章（新章節，不受凍結）加入一句說明：前面各章的「課堂口頭」標示依舊版作業頁（SRC-1／SRC-2T），新版作業頁（SRC-4）把 GitHub 與 web 列為主要繳交。若 DA 判定需要，屬契約內的分配（不改正式章節、不改既有測試）；若任何處理需要修改凍結的正式文字或 `tests/test_report.py`，屬 acceptor 的 contract change（治理 §5.3 第 1 類）。
- **Disposition**：見 §8。

### SIA-F2 — README 與報告對 Lasso 停止原因的列舉不完整，並省略「置中」（#78 R1 F2，整合 subject 上仍在）

- **Severity**：Low。**Blocking**：否。
- **證據**：README 第 148 行與報告第 379 行列舉「active set 退化、走到終點…，或數值停止（alpha 回升、迭代達上限）」，沒有實作中的 `multiple_drops`（`explore_app.js` 「同一步有多個欄同時離開路徑」）與 `target_constant`（「預測目標在這些列上沒有變化」）；尺度寫「目標除以它在同一批列上的均方根」，實作是先置中再除（`explore_engine.js` 檔頭第 50–52 行；頁面 `#ex-lasso-card` 寫「置中並除以其均方根」）。
- **依據**：DA R4-5（README 與報告須與 R4-1～R4-4 實作後的行為一致）、H-4。
- **Non-blocking 的理由**：核心陳述（任何提前結束一律以 A-2 處理、畫面寫實際原因、判定與目標單位無關、entry alpha 以原尺度回報）正確，我在整合 subject 上驗證過行為（§2.4）；頁面本身的原因說明完整；列舉以「不論原因是」引出，讀者不會因此得到錯誤的處理結論。
- **Disposition**：見 §8。

### SIA-F3 — ZIP 中 dashboard 與 blob 逐位元相同，依賴一個沒有寫進打包程式或測試的手動換行步驟（#78 R1 F3，A-6 核對）

- **Severity**：Low。**Blocking**：否。
- **證據**：本 subject 的 ZIP 我已核對逐位元相同（S-34）。`hw2/package.py` 讀工作樹位元組；`core.autocrlf=true`；`.gitattributes` 對 `index.html`、`assets/*.js`、`assets/*.css` 沒有 `-text`（只有 `assets/data/**`、`assets/vendor/**`）；目前 `git ls-files --eol` 顯示這些檔 `i/lf w/lf`，之後的 checkout 可能轉成 CRLF。`tests/test_package.py` 不檢查 ZIP 內 dashboard 與 blob 的位元組相等。
- **依據**：Spec V2「ZIP 與 Pages 的 dashboard 內容相同」；#78 AC「ZIP 內 dashboard 檔案與 repo 內逐位元相同」。
- **Non-blocking 的理由**：目前的 ZIP 滿足 AC；Pages 發布 blob（LF），所以目前 ZIP 與合併後的 Pages 一致；風險只在之後重新打包而沒有重做該步驟。
- **Disposition**：見 §8。

### SIA-F4 — Python 參照的 active-set 退化分支在整合 subject 上仍沒有測試覆蓋（#75 R1-F2，交本 audit 知悉；不重開）

- **Severity**：Low。**Blocking**：否。
- **證據**：在 `git archive 3745e9c` 的副本中把 `hw2/explore_reference.py` 第 667 行改為 `if False and _degenerate(G, active, j):`，`tests/test_node_explore.py` 與 `tests/test_explore_kc_consistency.py` 仍 **29 passed**（我確認被 import 的是副本中的模組）。#77 新增的 R4 測試沒有涵蓋這個分支。JS 的對應分支有 `explore_methods.test.js` 的 twin 測試，我的 twin 探測也確認 JS 正確停止並如實標示（§2.4 R4-1）。
- **依據**：Spec V2 Testing Decisions「失敗語義逐條有案例：…退化與相依情境各至少一個案例」；#75 AC「退化與相依」；Brief V2 §8「不假設 sklearn 保證…唯一進入順序」。
- **Non-blocking 的理由**：與 #75 R1 的判斷相同，沒有新的 integration-level evidence 改變它：AC 的文字已滿足（退化 fixture 的狀態與原因、退化前 entry alpha 經 Node 對 Python 比對）；精確的 active-set 退化只來自平手，跨實作沒有確定的順序，Brief 明文不要求一致；受影響的只有測試用參照的一段程式，頁面行為已驗證。
- **Disposition**：見 §8。

### SIA-F5 — 控制器丟棄晚到 URL 回應的世代檢查在整合 subject 上仍沒有測試偵測；`explore_ui.js` 只有靜態測試（#76 R1-F2，交本 audit 知悉；不重開）

- **Severity**：Low。**Blocking**：否。
- **證據**：在副本中把 `explore_app.js` 第 672 行改為 `if (!custom) return null;`（M-a1，等同 #76 R1 的 M6）或只拿掉 `gen !== generation ||`（M-a2），`explore_custom.test.js`、`explore_run.test.js`、`explore_app.test.js` 都是 **59 pass、0 fail**。沒有任何 Node 測試載入 `explore_ui.js`；`tests/test_explore_static.py` 對它只做字串層面的檢查（不含 `footer`、使用 `MessageChannel` 排程）。
- **依據**：Spec V2 Testing Decisions；#76 AC「切換」「新提交取代進行中的提交」。
- **Non-blocking 的理由**：行為正確——abort 路徑保證晚到的回應以 `cancelled` 結束、不被顯示，且第 672 行另有 `custom !== c` 的檢查；我的控制器探測與兩個瀏覽器的整合檢查都沒有看到錯置的結果或提前恢復的按鈕。`explore_ui.js` 沒有行為測試是已接受的 seam 設計的結果（UI 以 ACCEPTANCE 人工檢查表驗證，不引入瀏覽器 E2E 框架），不是契約違反。
- **Disposition**：見 §8。

### 交給本 audit 的其他項目（不構成 finding）

| 項目 | 整合 subject 上的核對 | 結果 |
| --- | --- | --- |
| R4-1～R4-4 | §2.4 | 成立 |
| resource-limits（C1-R1～C1-R3、C2-R1～C2-R3）與 §6 的 #78 揭露 | §2.4；README 第 165–167 行、報告 12.4（取消與改選的生效時點、單一候選可能數分鐘、頁面仍可操作、不承諾時間；沒有檔案大小上限、整份讀入記憶體、極大檔案可能無法讀取） | 成立 |
| cancel-final-phase（CF-1）與 §4 的 #78 揭露 | §2.4；README 第 166 行、報告 12.4 第 4 點、`index.html` 第 95 行 | 成立 |
| #77 O-R2-1（接近 512 MiB、在上限內、可解碼的輸入可能使分頁記憶體耗盡而不是顯示訊息） | DA resource-limits §6 把它的處理定為 #78 的揭露；README 第 167 行與報告 12.4「可能耗盡分頁的記憶體使分頁當掉，而不是顯示訊息」 | 已揭露；沒有新的 integration-level evidence；不是 finding |
| #77 O-R2-2（大於約 512 MiB 的位元組路徑在一個同步工作中完成，數秒內頁面不回應） | DA C2-R3 明定串流或分段不是要求；它發生在載入階段（不是 Spec SR-V2-03 所說的探索執行期間）；README 與報告「更大的檔案改以位元組逐段檢查，需要數秒，期間頁面不回應輸入」 | 已揭露；不是 finding |
| #77 O-R2-3（`aria-live` 進度列頻繁更新） | 螢幕閱讀器是 AD-1 的 best effort（NOT TESTED） | 不是 finding |
| #75 R1-F3（「每次選取都重算」） | `index.html` 第 231 行已改為「每次執行探索時只對 CV winner 計算一次（選取候選或切換方法不會重算）」；靜態測試 `test_methods_table_no_longer_says_recomputed_on_every_selection` | 已解決 |
| #75 R1-F4（替換資料的截圖） | V2-11、V2-15、V2-17 的註記；ACCEPTANCE、README、報告沒有把它們當作 50 Startups 或 Pages 的證據 | 已處理 |
| #74 R1-F2／#76 R1-F1（以欄名作一般物件鍵） | `explore_ui.js` 第 436 行以 `Map` 收集預測器輸入；靜態測試 `test_exploratory_files_never_assign_a_computed_key_on_a_plain_object`；我的 H-5 探測中 `__proto__`、`constructor` 欄的輸入都存在 | 已解決 |
| B-10（Pages 檢查） | V2-42、G.1 第 3 條記 NOT TESTED（pending merge） | **Open item**：合併後由 acceptor 直接指示的 Lightweight work item 執行，需 independent audit（derivation B-10、§7.5）；不判 FAIL，不阻擋本 audit |

### 觀察（不是 finding）

- **O-1**：我的排程控制器尾段取消探測，在小資料上看不到 `diagnostic` phase（尾段在一個步驟內完成），改用 8,000 列資料後成立；這是探測設計，不是缺陷（尾段的讓出點依 `YIELD_CELLS`）。
- **O-2**：審查環境：瀏覽器只以我啟動的程序執行（Chrome PID 43456、40456、27880、36384；Edge PID 41124），各自使用 scratchpad 的全新 `--user-data-dir`，沒有使用 acceptor 的預設 profile，也沒有執行 `chrome.exe --version`（版本取自安裝目錄名稱）。Edge 的啟動程序結束後，命令列含我的 profile 路徑的子樹（PID 23624）仍在，我以命令列確認後以 PID 停止；每次結束後以 `Win32_Process` 命令列核對，含 scratchpad profile 的 `chrome.exe`／`msedge.exe` 為 0。兩個本機伺服器（PID 32964 與其子程序）以 PID 停止並確認 0 殘留。沒有以映像名稱停止任何程序。一次失誤在系統暫存目錄建立了一個空檔，已立即刪除。

## 8. Non-blocking findings 的 disposition 與 owner

| Finding | Disposition | Owner |
| --- | --- | --- |
| SIA-F1 | Route **Design Authority**：判定 §7 所列的 ambiguity（第 12 章是否須加入一句說明舊版／新版作業頁對 dashboard 的差異）。若 DA 判定需要，屬契約內 rework（新章節，不改正式章節與既有測試），依治理 §3.8 作審後驗證；若任何處理需要修改凍結文字，屬 acceptor 的 contract change。DA 的判定應在 DA phase acceptance 之前或之中作出；不延長本 cycle | Orchestrator（派工 DA、追蹤）；判定 authority＝Design Authority |
| SIA-F2 | 不需本 cycle 修正。若 SIA-F1 的處理或其他在 boundary 內的工作修改 README／第 12 章，順帶補上 `multiple_drops`、`target_constant` 與「置中」 | Orchestrator（tracked） |
| SIA-F3 | 不需本 cycle 修正。任何重新打包（含合併後、繳交前）都須在打包後核對 ZIP 內 `index.html` 與 `assets/` 的 sha256 等於該 commit 的 blob（V2-41 的方法），不符時重做換行步驟；把這個條件寫進 completion report 給 acceptor（繳交屬 RB-2） | Orchestrator（run record／completion report） |
| SIA-F4 | 不需本 cycle 修正；測試覆蓋的技術債。之後若有修改 Lasso 退化邏輯的工作，可補一個讓參照的 `_degenerate` 生效的案例（不是新 AC；新的工作須依治理 §1.2 取得接受） | Orchestrator（tracked） |
| SIA-F5 | 不需本 cycle 修正；之後若有修改控制器的工作，可補晚到回應的測試（例如讓被取代的讀取不被 abort 而晚到成功） | Orchestrator（tracked） |
| B-10 | Open item（不是 finding）：合併後的 Lightweight Pages 檢查 | acceptor 指示後執行 |

## 9. Routing

- **Design Authority**：SIA-F1（契約語義／allocation：H-4 的如實標示與凍結的正式章節之間，第 12 章是否須加說明）。Phase acceptance 時一併處理。
- 沒有 blocking finding：不需要 targeted correction、R2、Alternate Review 或 Final Adjudicator。
- 不需要 acceptor 的決定（除非 DA 判定 SIA-F1 需要修改凍結文字）。Push、merge（RB-1）、繳交（RB-2）、合併後的 Pages 檢查仍保留給 acceptor。

## 10. Evidence（本 audit 執行的主要指令）

- 讀取：Bindings b5 全文；治理 v2.2 §2.3、§4.1–§4.7；impl-default v2 §6、§7；`outcome-contract.md` 全文；`SPEC-V2.md`、`BRIEF-V2.md`、`tickets-v2.md` 全文；`gh issue view 74..78`（本文）；`derivation-SPEC-V2.md` 全文；四份 V2 DA decision 與 `decision-20261018-high-risk-categories.md` 全文；`audit/issue-75-c1-r1.md` §5–§8、`audit/issue-76-c1-r1.md` §6–§9、`audit/issue-77-c1-r2.md` 全文、`audit/issue-78-c1-r1.md` 全文、各 V2 audit 的標題與 verdict；`audit/spec-SPEC-c1-r1.md`、`audit/20261019-ad3-pages-check-c1-r1.md` 的 verdict 與 `decision-20261019-phase-acceptance-SPEC.md` 的裁決段；run record 全文；ACCEPTANCE G 節與 G.1、G.2；README 與 `report/report.md` 的相關段落；`assets/explore_load.js`、`explore_app.js`、`explore_ui.js`、`explore_engine.js`（檔頭與相關段落）、`index.html` 的 V2 部分、`hw2/offline_scan.py` diff、`tests/test_explore_static.py`、`tests/js/explore_run.test.js` 的相關段落。
- Git（只讀）：`git rev-parse`、`git log --oneline d7f02d4..3745e9c`、`git diff --name-only／--name-status／--stat／-U0`（`d7f02d4`、`506581a`、`f4e487c`、`9e99a10`、`3dfba2d`、`ded2769`、`450bcff`、`a4b6c76`、`9ac8499`、`4bd6a59`、`9d5a840`、`d7147ba`、`31a2255`、`2b658b3`、`f56461b`、`3745e9c`、`33107ed`）、`git show <rev>:<path> | sha256sum`、`git ls-tree`、`git ls-files --eol`、`git grep -F -c`（學號，不印值）、`git status --porcelain／--ignored`、`git archive 3745e9c home_work_02`（匯出到 scratchpad）。
- GitHub：`gh issue view 73..78 --json body`（sha256）、`gh issue view 59..67 --json number,state,updatedAt`、#73–#78 的標題、本文與留言的學號比對。
- 測試：`.venv/Scripts/python -m pytest -q -rs -p no:cacheprovider`（478 passed）；`node --test tests/js/explore_{load,boundary,app,methods,custom,run}.test.js`（88 pass）；`node --test tests/js/core.test.js`；`python -m hw2.offline_scan`；`offline_scan.scan()` 對 ZIP 解壓副本。
- Scratchpad 腳本（`python -I`、Node；只讀 repo 與 `dist/`）：`zipcheck.py`（ZIP sha256、manifest、blob 比對、學號位元組）、`probe_engine.js`（凍結、第二層、可重現性、三種入口、單位無關、twin、匯出）、`pi_recompute.py`（numpy／scipy 獨立重算）、`probe_ctrl.js`、`probe_cf1.js`（請求隔離、CF-1、heartbeat、不並行、切換、C2-R3）、mutation 副本 M-a1、M-a2、M-b、`servers.py`（兩個本機 origin 與請求紀錄）、`cdp_sia.js`、`cdp_kcdiff.js`、`cdp_h5.js`、`cdp_ov2.js`（Chrome／Edge DevTools Protocol）、`make_crafted.js`、中型資料產生器。
- Binding：Bindings §3.6 的方法掃描本 assignment（`aa43e1e2fb1e18487`）與五個 Executor assignments 的 transcript。
- 寫入的追蹤檔案只有本 record；沒有 commit，沒有 git 寫入操作，沒有修改任何追蹤中的實作、測試、契約或紀錄。

VERDICT: CLOSURE
