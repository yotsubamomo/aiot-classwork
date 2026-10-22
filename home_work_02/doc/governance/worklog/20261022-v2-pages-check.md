# Worklog — WI-V2-PAGES-1：HW2 V2 dashboard 在 GitHub Pages 上的檢查（Lightweight）

| 欄位 | 內容 |
| --- | --- |
| Work item | WI-V2-PAGES-1：合併後的 GitHub Pages 檢查（DA `decision-20261022-phase-acceptance-SPEC-V2.md` OI-V2-1；derivation `derivation-SPEC-V2.md` B-10、§7.5） |
| Lane | Lightweight（Bindings §4 第 4 列「已結案工作之後的單點修正」；derivation B-10 指定為合併後的 Lightweight work item）。不是 Formal run `run-20261022-hw2-v2-enhance` 的一部分，沒有 Orchestrator run |
| 日期 | 2026-10-22 |
| Branch | `home_work_02-v2-pages-check`，自 `origin/main` `062e8a45c83a4be390c79352833559b218ffbeab`（PR #79 的 merge commit）建立；只在本機 commit（SA-1），未 push |
| 狀態 | Pages 檢查完成（self-verification），結果 PASS；ACCEPTANCE V2-42、V2-18 的 Pages 部分與 G.1 第 3 列已更新；independent audit **required**，尚未派工（§9） |

## 1. Contract reference

- **Outcome Contract（Lightweight，Bindings §2.3）**：acceptor 2026-10-22 的直接指示，原文：
  > 推送 bb4362c → 合併 → 檢查 Pages
  
  本 work item 的範圍是其中的「檢查 Pages」。推送與合併已由派工者在本 work item 之前完成（PR #79 合併為 `062e8a4`）；它們不屬於本 work item。
- **檢查項目的來源**：
  - derivation `doc/governance/decisions/derivation-SPEC-V2.md` B-10（Brief V2 §8 第 3 條「於 Pages 上」、§3.2「Pages 與 ZIP 一致」、§14 P0「Pages 可正常存取」）、I-1（`http://localhost` 的結果不得記為 Pages PASS）、§7.5（audit 必要）。
  - DA `doc/governance/decisions/decision-20261022-phase-acceptance-SPEC-V2.md` OI-V2-1。
  - `doc/acceptance/ACCEPTANCE.md` V2-42（合併前寫好的檢查方式：subject 是合併 commit 觸發的 `github-pages` 部署；`index.html` 與 `assets/` 對該 commit 的 blob sha256；在 Pages 上貼老師的範例 URL，比對內建 50 Startups；請求只到該 URL 一次；King County 的 D-1～D-8 與 SR-09 (b)～(e)(g) 重做），以及 V2-18 的 Pages 部分。
  - V1 先例：`doc/governance/worklog/20261019-ad3-pages-check.md` 與 `doc/governance/audit/20261019-ad3-pages-check-c1-r1.md`。
  - 派工指示列出的檢查：下拉三項；King County 與 V1 逐字相同、切換後不變；50 Startups 五種方法完成；老師 URL 恰一個 GET、不帶憑證、不跟隨 redirect、內容相同時結果與內建相同；URL 失敗後本機檔案可用；探索時 V1 頁尾隱藏；請求只到 Pages origin 與提交的 URL；console 無錯誤。另外要求記錄該 merge commit 觸發的其他部署（Vercel Production）。
- **高風險類別**：H-2（Pages URL 是交付的一部分）、H-5（V2 的 URL 載入與請求隔離），所以需要 independent audit（derivation §7.5；OI-V2-1）。H-1 依 A-4 核對學號（§9）。
- **範圍限制（派工指示）**：只修改 `home_work_02/doc/` 下的紀錄（本 worklog、ACCEPTANCE V2-42 與 V2-18 的 Pages 部分、證據檔）。不修改程式、測試或 dashboard；發現產品缺陷時只記錄並回報。不 push、不合併。

## 2. Executing role and binding reference

- **角色**：Executor（`gov-executor` subagent，由無角色的主 session 派工；definition `.claude/agents/gov-executor.md`）。
- **Binding**（Bindings §3.6）：session `37216426-f292-44f9-bad1-e2d862e7b8f1`，agentId **`a95b90b7c9ec3a748`**，`meta.json` 的 `agentType` 為 `gov-executor`。以 §3.6 的掃描觀測到 `('claude-opus-5-5', 'high')`：寫 worklog 時 108 則、commit 前 124 則，全程只有這一個元素，等於 O-1 mapping。全程核對由派工者在採用 return 前執行。
- **Escalation／替代**：無。**Bounded assignments**：未使用。

## 3. 環境與方法

- **機器**：Windows 11 專業版 10.0.26200（acceptor 的電腦），Node v24.19.0，單元 `.venv`（Python 3.11.2）。
- **瀏覽器**：headless Google Chrome **155.0.8059.85**、Microsoft Edge **155.0.4283.62**（版本取自 CDP `Browser.getVersion`，沒有在預設 profile 上執行任何瀏覽器指令）。每個瀏覽器使用全新的暫存 profile（scratchpad `v2pages/prof-chrome-1`、`prof-edge-1`），**網路開啟**，沒有 offline 模擬、resolver 規則或 proxy。
- **腳本**（session scratchpad 的 `v2pages/scripts/`，不在 repo）：
  - `pages_v2.js`（sha256 前 16 碼 `935b6aeb1cada361`）：以 DevTools Protocol 驅動瀏覽器，改寫自 #78 的 `ov78.js`（下拉、50 Startups、自訂資料集、V1 區塊文字比對）與 V1 AD-3 R1 的 D-1～D-8 檢查。改寫的地方：URL 換成 Pages，拿掉離線設定；記錄每個請求的 phase、URL、method、type、redirect、HTTP status、request header 名稱（含 `requestWillBeSentExtraInfo`）與 associated cookies 數；記錄 console error／warning（`Runtime.consoleAPICalled` 與 `Log.entryAdded`）、例外與對話框。切換下拉、方法、k、滾輪、拖曳與縮放按鈕都送真實的鍵盤與滑鼠事件；選本機檔案用 `DOM.setFileInputFiles`。
  - `verdict.py`（`02dc2b5c2a1900cc`）：從兩份 JSON 機械判定每一項，並比對 Chrome 與 Edge。
  - `zip_cmp.py`（`795cf69d04d17165`）：在記憶體中讀繳交 ZIP，比對 dashboard 項目與 Pages 上取得的檔案，不輸出 ZIP 檔名。
- **V1 參照**：`git -c core.autocrlf=false archive 5d650b1 home_work_02/index.html home_work_02/assets` 解到 scratchpad 的 `v2pages/v1ref/`。7 個檔案的 sha256 與 `5d650b1` 的 blob 逐一相同；`5d650b1` 是 V1 AD-3 檢查過的 Pages subject。在同一個瀏覽器中以 `file://` 開啟，取得 V1 區塊的文字。（第一次解壓沒有關掉 `core.autocrlf`，換行被轉成 CRLF，hash 不同；我刪掉它，重新解壓後才使用。）
- **時間（UTC）**：部署查詢 06:28:50 起；Pages 檔案下載 06:29:18；Chrome 06:34:36～06:36:15；Edge 06:36:51～06:38:28；全部 pytest 06:41:47～06:43:59。

## 4. 部署與內容的識別

| 檢查 | 結果 |
| --- | --- |
| `origin/main` | `062e8a45c83a4be390c79352833559b218ffbeab`（`git fetch` 與 `git ls-remote` 都是這個值） |
| Pages 設定（`gh api …/pages`） | `status: built`，source `main` `/`，`public: true`，`html_url` `https://yotsubamomo.github.io/aiot-classwork/` |
| Pages build（`…/pages/builds/latest`） | commit `062e8a4…`，`built`，06:27:19Z～06:28:21Z；Actions「pages build and deployment」run 39734033528：`completed`／**`success`**（06:27:20Z～06:28:24Z） |
| GitHub deployments（`deployments?sha=062e8a4…`） | `github-pages` **7245410085**：waiting → queued → in_progress → **success**（06:28:24Z，`environment_url` 是 Pages 根網址），也是 `github-pages` 環境的最新部署。Vercel `Production` **7245413394**：**success**（06:28:24Z，`aiot-hw01-weather-…vercel.app`，是 `home_work_01` 的專案，與本單元無關，只記錄）。該 commit 沒有其他部署 |
| Pages 上的檔案 vs `062e8a4` | `index.html` 與 `assets/` 下 16 個檔案，共 17 個：全部 HTTP 200，**sha256 與 `git show 062e8a4:home_work_02/<path>` 逐一相同**（`doc/screenshots/v2-pages/pages_files_sha256.tsv`）。例如 `index.html` `d80f374efe9c…`、`model_data.js` `6cf0c11eec94…`（9,787,856 bytes）、`explore_load.js` `998039a81572…`、`50_Startups.csv` `c6075ca5a755…`。`index.html` 引用的本地資源是其中的 12 個（`src`／`href`），其餘引用都是頁內錨點 |
| Pages vs ZIP（Brief V2 §3.2） | 在記憶體中讀繳交 ZIP（sha256 `8a51fc1ca26d176f3edb075f7f8aeda7a0dc659531484c10e695bc3800d08f8d`，67 項，與 V2-41 相同；檔名不輸出）：dashboard 的 17 個項目與 Pages 上取得的檔案**逐一相同**，沒有缺少（`pages_vs_zip.txt`）。另外 `git diff 69f8e07 062e8a4 -- home_work_02/index.html home_work_02/assets` 為 0 行（ZIP 是在 `69f8e07` 打包的） |
| `…/home_work_02`（無結尾斜線） | 301 → `…/home_work_02/`；後者 200，內容與 `index.html` 逐位元相同 |
| 合併 commit 的其他內容 | V1 的 7 個 dashboard 檔中，`5d650b1` → `062e8a4` 只有 `index.html` 有變（+209 行，V2 的下拉與探索區塊）；`app.js`、`hw2core.js`、`model_data.js`、`style.css`、Chart.js 沒有變 |

全部 API 輸出：`doc/screenshots/v2-pages/deployments.txt`。

## 5. King County 在 Pages 上的檢查（V2-42：D-1～D-8、SR-09 (b)～(e)(g)；與 V1 逐字相同）

Chrome 與 Edge 的功能結果完全相同（`verdict.txt`；`kc_blocks`、`d3_states`、`d4_on`、`d5_*`、`sr09_e_tooltip` 這幾段 JSON 逐字相同）。

| 項目 | 結果（Chrome＝Edge） |
| --- | --- |
| 載入 | 主文件 `https://yotsubamomo.github.io/aiot-classwork/home_work_02/`，`lang="zh-Hant-TW"`，標題「King County 房價多元線性回歸分析 — HW2 Dashboard」；`explore` 區塊隱藏；`load-error` 隱藏 |
| 下拉 | `#problem-select` 三項依序：`king_county`「King County 房價（正式分析）」（預設選取）、`startups50`「50 Startups 利潤（探索）」、`custom`「自訂資料集（探索）」 |
| D-1 必要區塊 | 方法 5 個（`allin`、`forward_sfs`、`backward_sfs`、`rfe`、`lasso_path`），預設 All-in，沒有 k 按鈕（`.kfixed`）；KPI 4 張；指標 vs k 圖（Chart.js 實例 1 個）；預測器 18 個欄位、19 個輸入（含日期、zipcode 下拉、未整修核取方塊）；散佈圖 `firstDraw.nPoints`＝`nTestPoints`＝4,323；Test 區塊、方法與限制、概覽都顯示 |
| D-2 zh-TW | 截圖目視（Chrome 首屏與第二屏、50 Startups 首屏、URL 失敗畫面、散佈圖縮放；Edge 老師 URL 首屏）：沒有缺字方塊；價格刻度「60 萬～200 萬」可讀 |
| D-3 方法與 k | 4 個路徑方法各試 k＝1、9、17、18：預測器欄位數等於 k；forward 的 KPI 隨 k 改變（4 個 k 得到 4 組不同數值）；All-in 時 k 固定，沒有 k 按鈕 |
| D-4 比較全部 | 開啟：`aria-pressed=true`、比較卡片顯示、表格 8 列、指標圖 8 個 dataset；關閉：`false`、卡片隱藏 |
| D-5 預測器 | 預設點預測 **US$503,564**，PI **US$351,404 – US$721,610**（與 V1 相同）。`sqft_living`＝90000 時出現外推警告「超出 training 範圍（290–13540），仍照常計算，屬於外推。」，且照常計算。切換「未整修」後整修年欄位啟用、預測改變。日期 2014-10-17 → 2015-05-01 後預測改變。zipcode 下拉 70 項。`?zipcode=00000` 時出現警告「此 zipcode 不在模型的訓練類別中，已以基準類別計算（輸入值：00000）」，仍給出預測 |
| D-6、D-7 來源標示與分欄 | KPI 的 4 個標籤都是「訓練 CV（USD）」，Test KPI 的 4 個標籤都是「Test 評估（USD）」；比較表把「訓練 CV（USD）」與「Test 評估（USD）」分欄（`chrome_kc_compare_all.png`） |
| D-8 非 winner 提示 | 非 winner 時顯示：forward、backward、lasso 的 k＝1、9、18，rfe 的 k＝1、9、17。winner 時隱藏：forward k17、backward k17、rfe k18、lasso k17、All-in（`chrome_kc_lasso_k1_notice.png`）。與 V1 的 winner（17／17／18／17）相同 |
| SR-09 (b) 互動（真實輸入） | 方法 6 次、k 4 次、滾輪 10 次、拖曳 3 次、縮放按鈕 5 次都有記錄（`HW2_PERF.interactions`）。最長：Chrome 27.7 ms（方法），Edge 22.7 ms；互動期間 long task 0；沒有例外或對話框 |
| SR-09 (c)(d)(e) | 預設視圖與滾輪縮放 4 次後的截圖（`*_kc_scatter_zoom.png`）：可分辨 y=x 虛線、藍色圓點與橙色方塊，以及個別 PI 線段。游標提示（兩個瀏覽器相同）：「第 5,148 列（房屋 7203220130）／預測 US$987,306／實際 US$994,900／95% PI US$689,162 – US$1,414,434／落入區間」 |
| SR-09 (g) | 繪製 4,323 筆＝n_test，沒有抽樣 |
| **與 V1 逐字相同** | 比較五個 V1 區塊（`overview`、`model`、`predictor`、`test`、`methods`）的 `innerText` 與頁尾文字：Pages 上的 V2（新載入）與 V1（`5d650b1` 的 blob，`file://`）**逐字相同**。唯一遮蔽的是 `#scatter-perf` 這一行（「首次繪製：N ms…」，數值隨每次載入改變）。沒有遮蔽時，只有 `test` 區塊因這一行不同（V1 346 ms、V2 61 ms） |
| SR-09 (a) 首次繪製（**只記錄**） | 新 profile 第一次載入（含 DNS／TLS 與 9.8 MB 的 `model_data.js` 下載）：Chrome 3,561 ms，Edge 1,503 ms。依 V1 DA `decision-20261019-post-merge-ad3-readme.md` 第 2 節，3 秒門檻只定義於 `file://`，在 Pages 上不是 PASS／FAIL gate；V2-42 也只要求 (b)～(e)(g) |

## 6. 下拉、50 Startups 與自訂資料集在 Pages 上的檢查（V2-42、V2-18 的 Pages 部分）

順序是 King County（新載入，作為參照）→ 50 Startups → 自訂資料集（空白）→ King County → 自訂資料集 + 老師的 URL → King County → 自訂資料集 + 301 URL → 404 URL → 本機檔案 → King County。最後在同一個瀏覽器中以 `file://` 開 V1，作為參照。切換下拉都用鍵盤（ArrowDown／Home／End）。

| 項目 | 結果（Chrome＝Edge） |
| --- | --- |
| **50 Startups** | 選取後完成（從按鍵到結果 Chrome 687 ms、Edge 703 ms；long task 84／67 ms）。`COMPLETED`，`source: builtin`，target Profit，內容 sha256 `c6075ca5…630d`，17 個候選全部 `VALID`。方法按鈕 5 個（All-in baseline、Forward SFS、Backward SFS、RFE、Lasso 路徑排序），比較表 5 列，指標 vs k 圖與 PI 圖已繪製，預測器有值（112,274；PI 93,156 ～ 131,391）。探索 test KPI「Test RMSE 9,850／MAE 8,351／MSE 97,026,682／R² 0.9399／PI 涵蓋率 100.0%」，與 V2-18、V2-37 記錄的數值相同。五個探索區塊都顯示，也都有「探索執行，非正式評估」標示。這一段的網路請求 0 |
| **探索時 V1 頁尾隱藏** | 50 Startups、自訂資料集（空白）、老師 URL 的結果、本機檔案的結果：五個 V1 區塊都隱藏，`footer` 不顯示 |
| 自訂資料集（空白） | 面板顯示，狀態「尚未載入資料：請以 URL 或本機 CSV 檔案提交。」；沒有結果區塊；請求 0 |
| **切回 King County** | 三次切回（三向切換之後、老師 URL 成功之後、URL 失敗與本機檔案之後）：五個 V1 區塊與頁尾的文字和新載入時逐字相同；頁尾重新顯示，`explore` 隱藏；請求 0 |
| **老師的範例 URL** `https://raw.githubusercontent.com/Avik-Jain/100-Days-Of-ML-Code/master/datasets/50_Startups.csv` | 在 `#ex-url` 以 `insertText` 輸入，按「載入 URL」。對該 URL **恰好一個請求**：`GET`、type `Fetch`、HTTP 200、沒有 redirect。`request.headers` 與 `requestWillBeSentExtraInfo` 的標頭中都沒有 `cookie` 或 `authorization`（有 `origin`，是 CORS 請求），associated cookies 0，對應程式的 `credentials: 'omit'`、`redirect: 'error'`（`assets/explore_load.js:436`）。結果：`COMPLETED`，`source: url`，內容 sha256 `c6075ca5…630d`（與內建相同；以 curl 取得同一 URL，sha256 也相同），17 個候選全部 `VALID`。訓練 CV KPI、探索 test KPI、預測值與 PI 的文字和內建 50 Startups **逐字相同**。狀態列「目前的資料：URL https://raw.githubusercontent.com/…/50_Startups.csv」 |
| **不跟隨 redirect**（301 URL） | 提交 `https://yotsubamomo.github.io/aiot-classwork/home_work_02/assets/data`（curl：301 → `…/assets/data/`）：該 URL 只有一個請求，`net::ERR_FAILED`；**沒有對 `…/assets/data/` 發出請求**，CDP 沒有任何帶 `redirectResponse` 的請求。頁面顯示「無法載入資料：URL 讀取失敗（URL_FETCH_FAILED，network）……或該網址會重新導向（本頁不跟隨重新導向）。請用瀏覽器下載該 CSV，再以下方的「本機 CSV 檔案」載入……」，沒有結果區塊（`*_custom_url_redirect_failure.png`） |
| 404 URL | 提交 `…/assets/data/no-such-file.csv`：一個請求，HTTP 404；頁面顯示「URL_FETCH_FAILED，http_status：…HTTP 404。…」，沒有結果區塊 |
| **URL 失敗後改用本機檔案** | 404 失敗之後，以 `#ex-file` 選擇本機的 `50_Startups.csv`（從 Pages 下載的檔案，與 blob 相同）：`COMPLETED`，`source: file`，sha256 相同，訓練 CV 與探索 test 的顯示和內建 50 Startups 逐字相同，新增的網路請求 0 |
| **請求（整段，不含最後的 `file://` V1 參照）** | 兩個瀏覽器各 69 個網路請求。host 只有 `yotsubamomo.github.io` 與 `raw.githubusercontent.com`；後者只有上面那一個 GET。其他 host 0。Pages origin 上非 200 的只有三個：瀏覽器自動請求的 `/favicon.ico` 404，以及我刻意提交的 301 與 404 URL |
| **Console、例外、對話框** | 頁面程式（`console.error`／`warn`／`assert`）0、例外 0、對話框 0。network 層的 `Log.entryAdded` error 有 3 則：(1) `https://yotsubamomo.github.io/favicon.ico` 404，瀏覽器自動請求，頁面沒有引用，與 V1 D-12 的觀察 O-1 相同；(2) 301 URL 失敗時的 `net::ERR_FAILED`，Chrome 把它記在 redirect 目標 `…/assets/data/` 上，但沒有發出該請求；(3) 404 URL 的 404。(2)(3) 是本檢查刻意製造的失敗 |

## 7. Decisions and assumptions

- 檢查方法沿用 V1 AD-3（Pages 檔案 sha256、CDP 驅動的瀏覽器檢查）與 #78 的 `ov78.js`（下拉、探索、V1 文字比對）。這是 HOW，沒有新增或刪減 V2-42 的驗收項目。
- **「與 V1 逐字相同」的比較對象**：V1 已不在 Pages 上，所以我用 `5d650b1` 的 blob（V1 AD-3 驗過的 Pages subject）以 `file://` 開啟，作為 V1。只遮蔽 `#scatter-perf` 的計時行，因為它的數值每次載入都不同，不是內容；原文差異也一併記錄（§5）。
- **URL 失敗用 Pages origin 上的網址**（301 與 404）：這樣不會對 Pages 與老師 URL 以外的 host 發出請求。301 的網址同時直接驗證了「不跟隨 redirect」。派工指示只要求「URL 失敗後」，我選了這兩種失敗原因；離線的 `network` 失敗已由 V2-37 在 `file://` 驗證過。
- **Console 判定**：頁面程式沒有 console error。network 層的 favicon 404 是瀏覽器對網站根目錄的自動請求，V1 D-12 與 V1 R1（O-a）已把它歸為觀察，不是頁面缺陷。另外兩則是我刻意製造的 URL 失敗，瀏覽器一定會記錄。我把派工的「no console errors」判為符合（頁面程式 0），並把這個判讀列為 concern C-1，讓 audit 核對。
- **ACCEPTANCE 的修改範圍**：V2-42 的證據欄、執行欄、狀態欄；V2-18 狀態欄最後的 Pages 句；以及 G.1 第 3 列的狀態（原為「Pages NOT TESTED（pending merge）」，是 V2-42 的鏡像；不改會和 V2-42 矛盾）。G.1 第 3 列不在派工指示列舉的範圍內，我判斷它屬於「V2-42／V2-18 的 Pages 部分」，記為 concern C-2。AD-1 的 best-effort 項目沒有改動。D-12（V1）與 F 節沒有改動。
- OV-2、OV-4、OV-5 沒有在 Pages 上重做：V2-42 沒有列出這三項；Pages 上的位元組與 ZIP 相同（§4），V2-37～V2-39 已在 ZIP 的同一份位元組上驗證過。D-9（invalid 候選）只能以 fixture 驗證；D-11／OV-1 是離線檢查，不適用於 Pages。
- 沒有修改程式、測試、dashboard、報告、notebook 或結果。

## 8. Artifacts

| 檔案 | 變更 |
| --- | --- |
| `home_work_02/doc/governance/worklog/20261022-v2-pages-check.md` | 新增（本檔） |
| `home_work_02/doc/acceptance/ACCEPTANCE.md` | V2-42（證據、執行、狀態 → **PASS**）；V2-18 狀態欄的 Pages 句（→ PASS，見 V2-42）；G.1 第 3 列（Pages → PASS（V2-42）） |
| `home_work_02/doc/screenshots/v2-pages/` | 新增證據：`deployments.txt`（gh API 輸出）、`pages_files_sha256.tsv`（17 個檔案的 Pages／blob sha256）、`pages_vs_zip.txt`（ZIP 比對，檔名以 `<學號>` 表示）、`pages_chrome.json`、`pages_edge.json`（每項檢查的原始結果與每個請求）、`verdict.txt`（機械判定與兩個瀏覽器的對照）、截圖 11 張。`*_top.png` 是全頁截圖的上半部裁切（Chrome 的 King County 首屏、50 Startups、老師 URL、URL 失敗後的本機檔案），完整的全頁截圖留在 scratchpad |

腳本、瀏覽器輸出原檔、全頁截圖、V1 參照與 Pages 下載的檔案都在 session scratchpad 的 `v2pages/`，不進 git。

## 9. Verification、audit status、concerns 與 remaining work

- **Verification**：
  - 部署與位元組：§4。瀏覽器：§5、§6；兩個瀏覽器各跑一次，都沒有重跑，也沒有不作證據的執行。
  - 每項判定由 `verdict.py` 從 JSON 機械產生：`dropdown_3_options`、`D1_blocks`、`D3_switch`、`D4_compare`、`D5_pred`、`D6D7_labels`、`SR09_e_tooltip`、`SR09_g`、`S50_complete`、`footer_hidden_exploring`、`KC_unchanged_after_switch`（3 次）、`KC_vs_V1_masked_identical`、`URL_one_GET`、`URL_no_credentials`、`URL_same_as_builtin`、`redirect_not_followed`、`url_404_failure`、`file_after_url_failure`，Chrome 與 Edge 全部 True；`other_hosts` 都是空的。
  - `python -m pytest -q -rs -p no:cacheprovider`（單元 `.venv`，ACCEPTANCE 修改後、commit 前）：**478 passed**，0 skipped（與 #78 的 478 相同；`tests/test_report.py` 的 ACCEPTANCE 斷言只涵蓋 A～E 與 OV 列，V2 列不受影響）。
  - **程序清理**：Chrome（PID 2292）在腳本的 `taskkill /PID … /T /F` 之後已不存在。Edge 的啟動程序（PID 21456）結束後，留下父程序已不存在的 `msedge.exe` PID 39808 與 8 個子程序；它們的命令列都是本 work item 的 scratchpad profile `v2pages/prof-edge-1`（#78 也記錄過同樣情況）。我以 `taskkill /PID 39808 /T /F` 停止。之後以 `Win32_Process` 的命令列核對，含本 session `v2pages` 路徑的 chrome、msedge、node 程序為 0。沒有以映像名稱停止任何程序，也沒有使用 acceptor 的預設 profile。
- **H-1／A-4 學號核對**：比對值只在記憶體中讀自 `.local/packaging.json`，不輸出。commit 前的核對（完全相同、允許空白／`_`／`.`／`,`／`/`／`-` 分隔的變形、前 8 碼、後 8 碼）：staged diff（`--binary`，含 ACCEPTANCE、本 worklog 與 17 個證據檔）0、commit message 0、`doc/screenshots/v2-pages/` 17 個檔案 0、scratchpad `v2pages/` 63 個檔案（不含瀏覽器 profile）0、`git grep --cached -F` 命中檔案 0、本 Executor 的 transcript 0。ZIP 只在記憶體中讀取，檔名沒有出現在任何輸出、證據檔或紀錄中。
- **Audit status**：**required**（H-2、H-5；derivation §7.5；OI-V2-1）。依 Bindings §3.7，由主 session 派 `gov-primary-reviewer`；Executor 不自行派工。受審 subject：branch `home_work_02-v2-pages-check` 的最終 commit（見 return），加上 `062e8a4` 觸發的 `github-pages` 部署 7245410085（`https://yotsubamomo.github.io/aiot-classwork/home_work_02/`）。Audit record 位置：`doc/governance/audit/20261022-v2-pages-check-c1-r1.md`。尚未派工。OI-V2-1 要在這次 audit closure 之後才能結案。
- **Concerns**：
  - **C-1**（給 audit 核對；如要消除 favicon 404，由 acceptor 決定）：派工指示要求 console 無錯誤。頁面程式的 console error 是 0；network 層的 favicon 404 是瀏覽器的自動請求（V1 O-1），另外兩則是刻意製造的 URL 失敗。我判為符合。若 acceptor 要消除 favicon 404，需要在 `index.html` 加 `<link rel="icon">` 或 favicon，屬於修改 dashboard 的新 work item（H-2，需 audit）。
  - **C-2**（給 audit 核對）：G.1 第 3 列的狀態是 V2-42 的鏡像，所以一併更新（§7）。若 reviewer 認為它超出派工範圍，還原這一列是 record-only 的修改。
  - **C-3**（只記錄）：Vercel `Production` 7245413394 為 success。Bindings §5 的 SA-3 合併後驗證（對 `home_work_01` production 跑 smoke）只適用於依 SA-3 的合併；這次是 acceptor 依 RB-1 指示的合併，所以本 work item 沒有執行 smoke。
- **Remaining work**：independent audit（R1）的派工與 closure（主 session）；之後 OI-V2-1 才能結案。本 branch 未 push（SA-1 的 push 由派工者決定），合併屬 RB-1，繳交屬 RB-2（OI-V2-10）。

## Audit status（派工的無角色主 session 轉錄，2026-10-22）

- Independent audit：**required → closed**。`../audit/20261022-v2-pages-check-c1-r1.md`：`VERDICT: CLOSURE`（Primary Reviewer agentId `ab740f9146544c1f3`，`gov-primary-reviewer`，主 session 核對 `('claude-opus-5-5','xhigh')` 210 則，單一元素）。C-1～C-3 經 Reviewer 判定無須處理；F-1（Low，§6 的檔名描述）non-blocking，未修改，留作紀錄。
- Executor binding（主 session 核對）：agentId `a95b90b7c9ec3a748`，`('claude-opus-5-5','high')` 129 則，單一元素。
- 結果：WI-V2-PAGES-1 完成；OI-V2-1（derivation B-10）結案。

## Push 與 PR（acceptor 授權，2026-10-22）

- Acceptor 原文逐字：「授權推送 home_work_02-v2-pages-check（推送前重跑學號檢查）並開 PR 到 main；不合併。」
- 依 SA-1、SA-2 執行；合併屬 RB-1，未授權。學號檢查與 PR 連結由派工的主 session 於推送後回報（PR 描述與對話）。
- Acceptor 追加原文逐字（同日，推送進行中送達）：「做完後merge」——取代上一則的「不合併」：推送與開 PR 完成後，以 merge commit 合併該 PR 進 `main`（RB-1 的逐次明確授權；不 squash、不 rebase、不刪 branch）。
