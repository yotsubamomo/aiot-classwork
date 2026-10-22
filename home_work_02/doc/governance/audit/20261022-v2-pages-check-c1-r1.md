# Audit record — R1，cycle 1：WI-V2-PAGES-1，HW2 V2 dashboard 在 GitHub Pages 上的檢查（Lightweight）

| 欄位 | 內容 |
| --- | --- |
| Work Contract | **Lightweight Outcome Contract**：acceptor 2026-10-22 的直接指示，原文「推送 bb4362c → 合併 → 檢查 Pages」。本 work item 的範圍是其中的「檢查 Pages」。我在 root session transcript（`37216426-f292-44f9-bad1-e2d862e7b8f1.jsonl`）找到這則 user 訊息：2026-10-22T06:26:16.514Z，`userType: external`，逐字相同。檢查項目的界定：derivation `decisions/derivation-SPEC-V2.md` B-10、I-1、§7.5；DA `decisions/decision-20261022-phase-acceptance-SPEC-V2.md` OI-V2-1（Brief V2 §8 第 3 條「於 Pages 上」、§3.2「Pages 與 ZIP 一致」、§14 P0「Pages 可正常存取」、ACCEPTANCE V2-42 與 V2-18 的 Pages 部分）；V1 先例 `worklog/20261019-ad3-pages-check.md` 與 `audit/20261019-ad3-pages-check-c1-r1.md`；高風險類別 H-1～H-5（derivation §7.2、§7.3） |
| 受審 subject | Branch `home_work_02-v2-pages-check`，commit **`4f5cf7bfde4bbf77a3f1880e4b215e1e1b30adae`**，parent 是 `main` **`062e8a45c83a4be390c79352833559b218ffbeab`**（PR #79 的 merge commit；`gh pr view 79`：MERGED，head `62d392a`，merged 06:27:18Z）。範圍 `062e8a4..4f5cf7b`：1 個 commit、19 個檔案，全部在 `home_work_02/doc/` 內（ACCEPTANCE 1、worklog 1、`doc/screenshots/v2-pages/` 17）。**被檢查的部署**：`062e8a4` 觸發的 `github-pages` 部署 7245410085，`https://yotsubamomo.github.io/aiot-classwork/home_work_02/`。Branch 未 push（`git ls-remote origin 'refs/heads/home_work_02-v2-pages*'` 無結果） |
| Audit 種類 | **R1，cycle 1**。Lightweight independent audit，屬 required：H-2、H-5（derivation §7.5；OI-V2-1）。Lightweight 沒有 Spec，所以本 record **不是** Spec Integration Audit（治理 §4.7 末段） |
| 角色 | `primary_reviewer`（definition `gov-primary-reviewer`） |
| 審查時間（UTC） | 2026-10-22T06:49Z～07:10Z |
| **(a) Context independence**（治理 §2.3；Bindings §3.7） | 1. **Independent context**：我是非 fork 的 subagent，從空白 context 開始。派工內容是 bounded pack（Outcome Contract 原文、範圍的紀錄路徑、subject 的 branch 與 SHA、Pages URL、worklog 與證據路徑、worklog 的 concern 編號），沒有 Executor 的結論。Worklog、ACCEPTANCE 與 `doc/screenshots/v2-pages/` 的內容，我都當作待驗證的主張。2. **Verifiable binding**：我的 transcript 是 `subagents/agent-ab740f9146544c1f3.jsonl`，`meta.json` 的 `agentType` 是 `gov-primary-reviewer`。寫入本紀錄前，以 Bindings §3.6 的掃描觀測到 `('claude-opus-5-5', 'xhigh')` 205 則，只有這一個元素，等於 R-PR 的有效 mapping。採用本紀錄前，派工者要依 §3.6 對全部 assistant 訊息做全程核對。3. **Autonomous access**：我自己讀 repo、git 歷史與 transcripts；用 `gh api` 查 Pages、deployments 與 Actions；用 curl 取得 Pages 上的檔案；在記憶體中讀繳交 ZIP；用我自己寫的 CDP 腳本（`r1pg/scripts/live.mjs`、`probe.mjs`、`probe2.mjs`，不是 Executor 的 `pages_v2.js`）在 Chrome 與 Edge 中操作線上 dashboard；在 subject 上執行 pytest。4. **Self-written record**：本紀錄由我用 Write 寫到 Bindings §7 的路徑，派工者只能原樣 commit |
| **(b) Model diversity** | Executor `a95b90b7c9ec3a748`（`gov-executor`）：我以 §3.6 掃描觀測到 `('claude-opus-5-5', 'high')` 129 則，只有一個元素，與 worklog §2 的派工者核對一致（worklog 記寫 worklog 時 108 則、commit 前 124 則）。Primary Reviewer（本 review）：`claude-opus-5-5`／`xhigh`。兩者同為 `claude-opus-5-5`，所以**無 model diversity**。Bindings §5 不宣告 diversity 關係，因此不記 `diversity_lost`；independence 依 (a) 判定 |
| Escalation | 不提出。沒有 D trigger，也沒有派工者要求 |

---

## 1. 審查範圍與方法

R1 涵蓋 accepted work scope 的全部內容：

- 部署：`062e8a4` 的 Pages 部署與其他部署的狀態。
- 位元組：Pages 上的 dashboard 檔案、`062e8a4` 的 blob、繳交 ZIP 的 dashboard 項目三者相同（Brief V2 §3.2）；Pages URL 可開啟（§14 P0）。
- 線上行為（Brief V2 §8 第 3 條、V2-42、V2-18 的 Pages 部分，以及派工列的十項）：下拉三項；King County 與 V1 逐字相同、切換後不變；50 Startups 完成；老師 URL 恰一個 GET、不帶憑證、不跟隨 redirect、結果與內建相同；URL 失敗後本機檔案可用；探索時頁尾隱藏；只到 Pages 與提交的 URL；console。
- King County 的 D-1～D-8、SR-09 (b)～(e)(g)（V2-42 的檢查方式）。
- ACCEPTANCE 的修改是否與證據相符（H-4）。
- 高風險類別 H-1～H-5（A-1）。
- Boundary：RB-5、不修改程式與 dashboard；commit 規則。
- Worklog 的 concerns C-1～C-3。

以下每項證據都由我自己取得。Executor 留在 scratchpad `v2pages/` 的檔案，我只用來核對 worklog 的描述（腳本 hash、截圖是否存在），不把它當作結果的證據。

## 2. 獨立檢查結果

### 2.1 部署與內容的識別（06:49:34Z 起）

| 檢查 | 指令 | 結果 |
| --- | --- | --- |
| `origin/main` | `git ls-remote origin main` | `062e8a45c83a4be390c79352833559b218ffbeab` |
| Pages 設定 | `gh api repos/yotsubamomo/aiot-classwork/pages` | `status: built`，source `main` `/`，`public: true`；repo `visibility: public` |
| 最新 build | `gh api …/pages/builds/latest` | commit `062e8a4…`，`built`，06:27:19Z～06:28:21Z，`error.message: null` |
| Actions | `gh api "…/actions/runs?head_sha=062e8a4…"` | 「pages build and deployment」39734033528：`completed`／**`success`**（06:27:20Z～06:28:24Z） |
| 該 commit 的 deployments | `gh api "…/deployments?sha=062e8a4…"` 與各自的 `/statuses` | `github-pages` **7245410085**：waiting → queued → in_progress → **success**（06:28:24Z，`environment_url` 是 Pages 根網址）；它也是 `github-pages` 環境最新的部署（`?environment=github-pages`）。Vercel `Production` **7245413394**：**success**（06:28:24Z，`aiot-hw01-weather-…`，`home_work_01` 的專案）。沒有其他部署 |
| Pages 檔案與 blob | curl（`--max-redirs 0`）取得 `index.html` 與 `assets/` 下 `062e8a4` 追蹤的 16 個檔案；`git show 062e8a4:home_work_02/<path>` | 17 個都是 HTTP 200，**sha256 全部相同**。例如 `index.html` `d80f374efe9c…`（41,805 bytes）、`app.js` `c1ab3f21cd9c…`、`hw2core.js` `e75c5d48b840…`、`model_data.js` `6cf0c11eec94…`（9,787,856 bytes）、`explore_load.js` `998039a81572…`、`50_Startups.csv` `c6075ca5a755…`。`index.html` 引用的本地資源是其中 12 個（`src`／`href`），其餘引用是頁內錨點 |
| 目錄網址 | curl | `…/home_work_02` 回 301 → `…/home_work_02/`；後者 200，與 `index.html` 逐位元相同（`cmp`） |
| Pages vs ZIP（Brief V2 §3.2） | 我的腳本 `zipcmp3.py` 在記憶體中讀 `dist/` 內唯一的 ZIP，不輸出檔名或項目前綴 | ZIP sha256 **`8a51fc1ca26d176f3edb075f7f8aeda7a0dc659531484c10e695bc3800d08f8d`**，81,624,097 bytes，67 項，`testzip()` 無錯；全部項目在單一頂層資料夾下，該資料夾名稱等於 `<學號>_hw2`（只做布林比對）。Dashboard 項目 17 個，與 Pages 上取得的 17 個檔案**逐一相同**，沒有缺少，也沒有多出。`git diff 69f8e07 062e8a4 -- home_work_02/index.html home_work_02/assets` 為 0 行（ZIP 在 `69f8e07` 打包） |
| 部署內容與已 closure 的審查對象 | `git diff 17f10a7 062e8a4` | SIA R2（`audit/spec-SPEC-V2-c1-r2.md`，CLOSURE）的最終整合 subject `17f10a7` 到 `062e8a4`：dashboard 0 行，`doc/governance/` 以外沒有任何路徑改變。也就是 Pages 提供的位元組就是 SIA 審過的位元組 |
| V1 → V2 的 dashboard 變化 | `git diff --stat 5d650b1 062e8a4` | V1 的 dashboard 檔中只有 `index.html` 改變（209 行，只有新增，沒有刪除）；`app.js`、`hw2core.js`、`model_data.js`、`style.css`、`chart.umd.js` 不變 |
| README 的連結 | curl | `https://yotsubamomo.github.io/aiot-classwork/home_work_02/` 200、`https://github.com/yotsubamomo/aiot-classwork` 200 |

Executor 的 `deployments.txt`、`pages_files_sha256.tsv`、`pages_vs_zip.txt` 的每個值都與上表相同。

### 2.2 線上 dashboard（我自己的 CDP 腳本；headless；每次全新的 scratchpad `--user-data-dir`；網路開啟）

- 瀏覽器（CDP `Browser.getVersion`）：`Chrome/155.0.8059.85`、`Edg/155.0.4283.62`。
- 執行：
  - 第一組：Chrome 06:55:45Z、Edge 06:56:50Z。
  - 第二組：06:58:21Z～06:59:08Z，加錄候選狀態，兩個瀏覽器各一次。
  - 06:54:24Z 的第一次 Chrome 執行，因我的腳本在平滑捲動完成前取座標，「比較全部」的第一次點擊與滾輪沒有落在目標上。我修正腳本後重跑（上面的第一組），這一次不作證據。
- 兩組、兩個瀏覽器的功能結果完全相同。
- 順序：King County（新載入）→ King County 互動 → 重新載入 → 50 Startups（鍵盤 ArrowDown）→ 自訂資料集（空白）→ King County（Home）→ 自訂資料集 + 老師 URL → King County → 自訂資料集 + 301 URL → 404 URL → 本機檔案 → King County → V1 參照（`file://`）。

V1 參照：`git -c core.autocrlf=false archive 5d650b1 home_work_02/index.html home_work_02/assets`，7 個檔案的 sha256 與 `5d650b1` 的 blob 逐一相同。

| 項目 | 結果（Chrome＝Edge） |
| --- | --- |
| 載入 | `location` 是 Pages URL，`lang="zh-Hant-TW"`，標題「King County 房價多元線性回歸分析 — HW2 Dashboard」；`#explore` 隱藏，`#load-error` 隱藏，五個 V1 區塊與頁尾顯示 |
| **下拉三項** | `#problem-select` 依序：`king_county`「King County 房價（正式分析）」（預設選取）、`startups50`「50 Startups 利潤（探索）」、`custom`「自訂資料集（探索）」。以鍵盤切換三項都生效 |
| D-1 | 方法按鈕 5 個（`allin`、`forward_sfs`、`backward_sfs`、`rfe`、`lasso_path`），預設 All-in、沒有 k 按鈕；KPI 4 張；預測器 19 個輸入；`HW2_PERF.firstDraw.nPoints`＝4,323 |
| D-3、D-4 | 切到路徑方法後 k 按鈕 18 個；k＝1 時預測器 1 個欄位。「比較全部方法」開啟：`aria-pressed=true`、卡片顯示、表格 10 列（含表頭）；關閉：`false` |
| D-5（`probe.mjs`，07:04:25Z） | 預設點預測 **US$503,564**、PI **US$351,404 – US$721,610**。`sqft_living`＝90000（真實鍵盤輸入）時出現「超出 training 範圍（290–13540），仍照常計算，屬於外推。」，且照常給出預測。點「未整修」後整修年欄位由停用變為啟用，預測改變。日期改為 2015-05-01 後預測改變。zipcode 下拉 70 項。`?zipcode=00000` 時出現「此 zipcode 不在模型的訓練類別中，已以基準類別計算（輸入值：00000）」，仍給出預測 |
| D-8 | 非 winner 時提示顯示：forward／backward／lasso 的 k＝1、9、18，rfe 的 k＝1、9、17。winner 時隱藏：forward k17、backward k17、rfe k18、lasso k17。與 worklog 及 V1 相同 |
| SR-09 (b) | 方法 5 次、k 1 次、比較全部 2 次、滾輪 4 次（真實滑鼠事件），都記錄在 `HW2_PERF.interactions`。最長：第一組 Chrome 34.2 ms、Edge 30.2 ms，第二組都是 24.2 ms。沒有例外或對話框 |
| SR-09 (c)(d)(e)(g) | 我看了 Executor 提交的 `edge_kc_scatter_zoom.png`：y＝x 虛線、藍色圓點與橙色方塊、逐筆 PI 線段可分辨，刻度「60 萬～200 萬」可讀。(g)：繪製 4,323 筆＝n_test |
| **King County 與 V1 逐字相同** | 五個 V1 區塊（`overview`、`model`、`predictor`、`test`、`methods`）的 `innerText` 與頁尾文字，只遮蔽 `#scatter-perf` 那一行：Pages 上新載入、重新載入、三次切回之後，以及 V1（`5d650b1` 的 blob，`file://`），**全部逐字相同**。沒有遮蔽時，只有 `test` 區塊因該行的毫秒數不同（例如 Pages 2,779 ms、V1 328 ms） |
| **50 Startups** | 選取後 `COMPLETED`，`source: builtin`，內容 sha256 `c6075ca5…630d`，候選 **`VALID` 17 個**（第二組）。方法按鈕 5 個（All-in baseline「k = 4 固定」、Forward SFS、Backward SFS、RFE、Lasso 路徑排序），比較表 5 列。五個探索區塊（`ex-data`、`ex-model`、`ex-predictor`、`ex-test`、`ex-methods`）都顯示，標題都含「探索執行，非正式評估」。探索 test KPI「Test RMSE 9,850／MAE 8,351／MSE 97,026,682／R² 0.9399／PI 涵蓋率 100.0%（10 / 10）」，預測器 112,274（93,156 ～ 131,391）。這一段沒有任何網路請求 |
| **探索時頁尾隱藏** | 50 Startups、自訂資料集（空白）、老師 URL 結果、301 失敗、404 失敗、本機檔案結果：五個 V1 區塊與 `footer` 都不顯示。切回 King County 後都重新顯示，`#explore` 隱藏 |
| 自訂資料集（空白） | 面板顯示「尚未載入資料：請以 URL 或本機 CSV 檔案提交。」，沒有結果區塊，請求 0 |
| **老師的範例 URL** | 以 `Input.insertText` 輸入 `https://raw.githubusercontent.com/Avik-Jain/100-Days-Of-ML-Code/master/datasets/50_Startups.csv`，以滑鼠點「載入 URL」。對該 host **恰好一個請求**：`GET`、type `Fetch`、HTTP 200。沒有 `OPTIONS` preflight，沒有帶 `redirectResponse` 的 `requestWillBeSent`。`request.headers` 與 `requestWillBeSentExtraInfo` 的標頭都沒有 `cookie` 或 `authorization`（有 `origin`，是 CORS 請求），associated cookies 0。結果：`COMPLETED`，`source: url`，內容 sha256 `c6075ca5…630d`（我另以 curl 取得同一 URL：200、0 次 redirect、2,436 bytes，sha256 相同），候選 `VALID` 17 個。訓練 CV KPI、探索 test KPI、預測值與 PI、方法按鈕、比較表、winner 摘要的文字，與內建 50 Startups **逐字相同**。狀態列「目前的資料：URL https://raw.githubusercontent.com/…/50_Startups.csv」 |
| **不跟隨 redirect** | 提交 `https://yotsubamomo.github.io/aiot-classwork/home_work_02/assets/data`（Pages 回 301）：該 URL 只有一個請求，`net::ERR_FAILED`；沒有對 `…/assets/data/` 發出請求。頁面顯示「無法載入資料：URL 讀取失敗（URL_FETCH_FAILED，network）……或該網址會重新導向（本頁不跟隨重新導向）。請用瀏覽器下載該 CSV，再以下方的「本機 CSV 檔案」載入……」，沒有結果區塊 |
| 404 URL | 提交 `…/assets/data/r1-no-such-file.csv`：一個請求，HTTP 404；「URL_FETCH_FAILED，http_status：伺服器回應錯誤的 HTTP 狀態：HTTP 404。……」，沒有結果區塊 |
| **URL 失敗後改用本機檔案** | 404 之後以 `DOM.setFileInputFiles` 選擇 `50_Startups.csv`（`062e8a4` blob 的位元組）：`COMPLETED`，`source: file`，sha256 相同，候選 `VALID` 17 個，顯示與內建 50 Startups 逐字相同。新增請求 0 |
| **請求** | Pages 階段（不含最後的 `file://` V1 參照）：host 只有 `yotsubamomo.github.io` 與 `raw.githubusercontent.com`。後者只有上面那一個 GET，其他 host 0。`data:` URI 3 個，是瀏覽器為日期欄位的日曆圖示產生的，不是網路請求。50 Startups、自訂資料集（空白）、三次切回 King County、本機檔案這幾段的請求都是 0。`kc_interact` 段的一個 Document 請求是我的腳本執行 `Page.reload` 造成的 |
| **Console** | `Runtime.consoleAPICalled` 0 則，例外 0，對話框 0。`Log.entryAdded`（source `network`，level `error`）3 則：(1) `https://yotsubamomo.github.io/favicon.ico` 404，瀏覽器對網站根目錄的自動請求，頁面沒有任何 icon 引用（`index.html` 的 `href` 只有兩個 CSS 與頁內錨點）；(2) 301 URL 失敗時的 `net::ERR_FAILED`，記在 redirect 目標 `…/assets/data/` 上，但沒有對它發出請求；(3) 404 URL。(2)(3) 是我刻意製造的失敗 |
| 首次繪製（只記錄） | Pages、新 profile：Chrome 2,779 ms 與 1,171 ms，Edge 1,169 ms 與 1,410 ms。依 V1 DA `decision-20261019-post-merge-ad3-readme.md` 第 2 節，3 秒門檻只定義於 `file://`，Pages 上不是 gate；V2-42 也只要求 (b)～(e)(g) |

### 2.3 H-5 探測（`probe2.mjs`，07:09:16Z，Chrome 與 Edge）

- 方法：在 Pages 上選自訂資料集，以本機檔案載入一份 synthetic CSV（80 列，不進 git，不是使用者資料）：
  - 欄名含 `<img src=x onerror=alert(1)>`、`</script><script>alert(2)</script>`、`javascript:alert(3)`、`<svg onload=alert(4)>`。
  - 類別值含 `<iframe src=//example.invalid>`、`<b>bold</b>`、`javascript:alert(5)`。
  - 之後依序點五個方法與「比較全部方法」。
- 結果（兩個瀏覽器相同）：
  - `COMPLETED`。
  - 這些字串全部以字面文字出現在 `#explore` 的 `innerText`。
  - `#explore` 內 `img`、`svg`、`iframe`、`script`、`b` 元素 0（載入前也是 0）。
  - 帶 `on*` 屬性的元素 0，`javascript:` 連結 0。
  - 對話框 0，例外 0，載入後的網路請求 0。
  - 切回 King County 後，區塊與頁尾文字和載入時相同。
- 這只是在公開 origin 上的行為確認。程式的 A-9 審查（DOM 寫入點列舉）屬於已 closure 的 Spec Integration Audit；Pages 提供的位元組與其 subject 相同（§2.1）。

### 2.4 ACCEPTANCE 的修改與證據（`git diff 062e8a4 4f5cf7b -- home_work_02/doc/acceptance/ACCEPTANCE.md`）

修改只有三列：V2-18 的狀態欄、V2-42 的證據、執行與狀態欄、G.1 第 3 列的狀態欄。

| 陳述 | 核對 |
| --- | --- |
| V2-42 subject：`main` @ `062e8a45…` 觸發的 `github-pages` 部署 7245410085，06:28:24Z success | 符合（§2.1） |
| 17 個檔案 200，sha256 與 blob 相同，也與 ZIP `8a51fc1c…8f8d` 的 17 項相同 | 符合（§2.1） |
| Chrome 155.0.8059.85、Edge 155.0.4283.62，新 profile、網路開啟，兩者結果相同 | 符合（我量到的版本相同） |
| 下拉三項的順序 | 符合 |
| King County：方法 5、KPI 4、預測器 19 個輸入、點預測與 PI、4,323 點；V1 區塊與頁尾逐字相同，只遮蔽 `#scatter-perf`；切換後仍相同 | 符合（§2.2）。互動最長 27.7／22.7 ms 是 Executor 的量測，與我的 24～34 ms 同一數量級 |
| 50 Startups：`COMPLETED`、17 個 `VALID`、五種方法、比較表 5 列、五個區塊有探索標示 | 符合 |
| 老師 URL：恰一個 GET（Fetch、200、無 redirect、無 Cookie／Authorization、associated cookies 0）；sha256 相同；訓練 CV、探索 test、預測器逐字相同 | 符合 |
| 301 只一個請求、未跟隨（network）；404 為 `http_status`；之後本機 CSV `COMPLETED`、結果相同、新增請求 0 | 符合 |
| 探索時 V1 區塊與頁尾隱藏，切回後顯示 | 符合 |
| 請求只到 `yotsubamomo.github.io` 與提交的 URL | 符合 |
| Console：頁面程式 0、例外 0、對話框 0；network 層 3 則（favicon 404 與兩次刻意的失敗） | 符合 |
| 首次繪製只記錄 | 符合（DA `decision-20261019-post-merge-ad3-readme.md` 第 2 節） |
| 證據位置可開啟（狀態規則） | 符合。V2-42 證據欄列出的 worklog §4～§6 與 `doc/screenshots/v2-pages/` 的 6 個檔案與截圖都在 `4f5cf7b` 中（11 張 PNG） |
| V2-18：「GitHub Pages 上：**PASS**，見 V2-42……」 | 符合；localhost 的原文保留 |
| G.1 第 3 列：「localhost PASS；Pages **PASS**（V2-42）」 | 符合，見 §3 C-2 |
| V2 區段沒有殘留的「pending merge」 | 符合。`grep` 只命中狀態規則表第 14 行的說明文字 |
| 沒有 audit PASS 的陳述 | 符合。V2-42 證據欄的「需 audit」是原有的要求敘述；worklog §9 記 audit status＝required、尚未派工 |

ACCEPTANCE 的 PASS 陳述都有證據，數值與識別都與我的獨立證據相符。Worklog 的一處敘述與證據不符，見 F-1。

### 2.5 測試（07:00:21Z～07:02:15Z）

- 在主 checkout（HEAD＝`4f5cf7b`，追蹤檔案無修改）以單元 `.venv` 執行 `python -B -m pytest -q -rs -p no:cacheprovider`：**478 passed，0 skipped**，與 worklog 相同。
- 執行前後 `git status --porcelain --ignored -- home_work_02` 相同。
- `tests/test_report.py` 的 ACCEPTANCE 斷言只取 A～E 與 OV 列（第 305–310 行的 regex），V2 列不受斷言約束。所以 V2-42 的內容由 §2.4 逐項核對。

### 2.6 Boundary 與其他義務

- 19 個路徑全部在 `home_work_02/doc/`；`doc/requirement/` 0 行（RB-5）。沒有修改程式、測試、dashboard、報告或結果，符合 Outcome Contract 的範圍。
- Commit message 第一行是 `[Modify] – …`（en-dash）。Claude 標記（`claude|co-authored|generated with`）0 處。Author 與 committer 是 `momo.dai`。
- `git ls-files` 中沒有 `.env`；`home_work_02/` 沒有追蹤 `.zip`、`dist/`、`.local/`。
- 合併本身不屬於本 work item。PR #79 是 acceptor 依 RB-1 逐次授權的合併（run record §14），不是 SA-3，因為 OC 沒有 opt-in。`bb4362c..62d392a` 只改 run record（record-only），`392e9df..062e8a4` 的 diff 全部在 `home_work_02/` 內。
- 程序（Executor）：
  - `v2pages/scripts/` 的三個腳本的 sha256 前 16 碼與 worklog §3 相同（`935b6aeb1cada361`、`02dc2b5c2a1900cc`、`795cf69d04d17165`）。
  - `pages_v2.js` 以 `--user-data-dir` 啟動瀏覽器。
  - 我掃描 Executor transcript 的 Bash 指令：沒有不帶 `--user-data-dir` 的瀏覽器啟動，也沒有瀏覽器的 `--version`。唯一含 `--version` 的指令是 `node --version`。
- 程序（我）：
  - 我的每次瀏覽器執行都以 CDP `Browser.close` 結束。
  - 每次之後以 `Win32_Process` 命令列（含 `r1pg`，限 `chrome.exe`、`msedge.exe`、`node.exe`）核對，結果都是 0，所以沒有需要以 PID 停止的程序。
  - 我沒有停止任何不是我啟動的程序，也沒有使用 acceptor 的預設 profile。

## 3. Worklog 的 concerns

- **C-1（favicon 404 與刻意的 URL 失敗 vs「no console errors」）**：**我同意 Executor 的判讀，不構成 finding**。
  - 頁面程式的 console error、例外、對話框都是 0（§2.2）。
  - favicon 404 是瀏覽器對網站根目錄 `/favicon.ico` 的自動請求。它在 `home_work_02/` 之外，頁面沒有引用，也不是對外 host。V1 R1 的 O-a 已這樣歸類。
  - 另外兩則是瀏覽器對刻意失敗的 fetch 記下的 network log。頁面以 zh-TW 訊息正確處理了這兩次失敗，這正是被檢查的行為。
  - Brief V2 §8、§14 與 V2-42 都沒有要求 network log 為零。V2-42 如實記載了這 3 則。
  - 要消除 favicon 404，必須修改 `index.html`（H-2，需 audit），屬於新的 work item，由 acceptor 決定。這不是本 work item 的缺陷。
- **C-2（G.1 第 3 列超出派工列舉的列）**：**在範圍內，不需還原，不構成 finding**。
  - 派工文字只列了 V2-42 與 V2-18 的 Pages 部分。但 Outcome Contract 的範圍（OI-V2-1）包含 Brief V2 §8 第 3 條「於 Pages 上」，G.1 第 3 列正是該條的對照列，原值「Pages NOT TESTED（pending merge）」是 V2-42 的鏡像。
  - 不更新，ACCEPTANCE 會自相矛盾（H-4）。
  - 修改是 record-only、在單元內，並已在 worklog §7、§9 揭露。
  - 派工指示本身不是 authority 來源；它沒有擴大或縮小 Outcome Contract。
- **C-3（沒有執行 `home_work_01` 的 smoke）**：**同意，不構成 finding**。
  - Bindings §5 的「SA-3 合併後驗證」只適用於依 SA-3 的合併。PR #79 是 RB-1 的逐次授權合併（run record §14；OC 沒有 opt-in SA-3）。
  - 本 work item 的 Outcome Contract 是「檢查 Pages」（`home_work_02`）。
  - 我確認 `062e8a4` 觸發的 Vercel `Production` 7245413394 為 success，而且 PR #79 的 diff 沒有任何 `home_work_02/` 以外的路徑，所以 `home_work_01` 的部署輸入沒有改變。
  - 若 acceptor 仍要對 `home_work_01` production 跑 smoke，是 acceptor 的選擇，不屬本 work item。

## 4. 高風險類別（A-1）

| 類別 | 觸及方式 | 核對與結果 |
| --- | --- | --- |
| **H-2** Pages URL（SRC-4「github and web」）、加分 +1／+2、Pages 與 ZIP 一致 | 本 work item 的檢查對象 | 部署 success；Pages URL 與 README 兩個連結 200；Pages、blob、ZIP 三者 17 檔逐位元相同；下拉三項；老師 URL 在 Pages 上載入，結果與內建相同；King County 與 V1 逐字相同（§2.1、§2.2）。**符合** |
| **H-5** 使用者提供的資料來源與請求邊界 | 線上請求邊界與不受信任內容 | 只在提交後對該 URL 一次 GET：沒有 preflight、沒有重試、不帶 cookie／authorization、不跟隨 301。頁面載入、King County、50 Startups、本機檔案這幾段都沒有任何對外請求。其他 host 0。Synthetic 惡意字串在公開 origin 上只以文字呈現，沒有注入元素，也沒有請求（§2.2、§2.3）。程式位元組與 SIA 已 closure 的 subject 相同。**符合** |
| **H-4** 證據真實性 | ACCEPTANCE V2-42、V2-18、G.1 由 NOT TESTED 改為 PASS | 每個數值與識別都與我的獨立證據相符（§2.4）。截圖放在 `v2-pages/`，環境是 Pages。Worklog 的一處檔名敘述不符，見 F-1。**符合，附 F-1** |
| **H-1** 學號、憑證、使用者資料（A-4） | 本 commit；證據檔；ZIP 的讀取 | 比對值只在記憶體中讀自 `.local/packaging.json`，不輸出：<br>（1）`git log -p --binary --format=fuller 062e8a4..4f5cf7b`（3,842,758 bytes）：完全相同 0、允許分隔字元的變形 0、前 8 碼 0、後 8 碼 0。<br>（2）作者、committer 與 message 0。<br>（3）`4f5cf7b` 上變更路徑的 19 個 blob 0。<br>（4）`git grep -F` 對 `4f5cf7b` 整棵樹命中檔案 0；正對照「WI-V2-PAGES-1」命中 2 個檔案。<br>（5）我的 scratchpad 80 個檔案（不含瀏覽器 profile）0。<br>（6）Executor transcript 0、我的 transcript 0。<br>ZIP 檔名與項目前綴都沒有輸出。追蹤檔案的 diff 中，URL 只有老師的範例 URL、本 repo 的 Pages origin、`home_work_01` 部署網址（`gh api` 輸出）與原有的 localhost 文字。沒有使用者提供的 URL 或資料。`credentials: 'omit'`（`assets/explore_load.js:436`）在線上請求中成立。**符合** |
| H-3 評估完整性 | 未觸及：沒有修改程式或結果 | Pages 上 `app.js`、`hw2core.js`、`model_data.js` 的 sha256 等於 DA A-3 的值（`c1ab3f21…`、`e75c5d48…`、`6cf0c11e…`）。只作記錄 |

## 5. Findings

### F-1 — Low，non-blocking：worklog §6 寫的本機檔名與提交的證據不符

- **證據**：
  - Worklog §6「URL 失敗後改用本機檔案」列寫「以 `#ex-file` 選擇本機的 `50_Startups.csv`（從 Pages 下載的檔案，與 blob 相同）」。
  - 提交的 `doc/screenshots/v2-pages/chrome_custom_file_after_url_failure_top.png` 的狀態列與「來源」欄都顯示「本機 CSV 檔案：assets_data_50_Startups.csv」。
  - 同一截圖的內容 sha256 是 `c6075ca5…630d`，與 blob 相同。
- **依據**：H-4「證據真實性與如實標示」（derivation §7.2）。
- **Severity 與 blocking**：Low，non-blocking。
  - 只有檔名敘述不同；內容與 sha256 的陳述成立。
  - ACCEPTANCE V2-42 沒有寫檔名（「以本機 CSV 載入」），所以驗收狀態不受影響。
  - 我在 Pages 上以 `50_Startups.csv` 重做這一步，結果相同（§2.2）。
- **Disposition**：
  - 不需要修改受審 subject 即可 closure。
  - 派工者在 worklog 記錄 audit 狀態時（record-only），可以順帶把檔名改成實際的 `assets_data_50_Startups.csv`。
  - **Owner**：派工者（主 session）。這是選擇性的紀錄修正，不延長本 cycle。

### Observations（不構成 finding）

- **O-a**：Worklog §5 D-2 引用的「Edge 老師 URL 首屏」與 Chrome「第二屏」截圖只在 Executor 的 scratchpad（`v2pages/shots/edge_custom_teacher_url_1280.png`、`tiles/chrome_kc_default_1.png`）。Worklog §8 已揭露全頁截圖留在 scratchpad。提交的截圖已涵蓋兩個瀏覽器的 zh-TW 顯示（我看了 Chrome 首屏、Chrome 本機檔案頁、Chrome 301 失敗頁、Edge 散佈圖縮放），所以 D-2 有證據。
- **O-b**：DA OI-V2-1 寫「執行者是該 item 的 direct-execution Executor」。Root session transcript 觀測為 `('claude-opus-5-5', 'medium')` 329 則；依 Bindings §3.5 不能擔任 Executor。所以改派 `gov-executor` subagent 是 Bindings 規定的路徑，沒有 authority 缺口（與 V1 R1 的 O-c 相同）。
- **O-c**：`verdict.txt` 的 `identical_functional_sections.custom_teacher_url: False`，我比對兩份 JSON：差異只有完成訊息中的毫秒數與 CDP `requestId`。Worklog「Chrome＝Edge」的陳述對功能結果成立。
- **O-d**：G.1 的檔頭寫「核對的 subject：`f56461b`」，但第 3 列的 Pages 狀態的 subject 是 `062e8a4` 的部署。檔頭同時寫明各條目核對各自的 subject（見各列），V2-42 列有完整識別，所以不構成矛盾。

## 6. 需要其他 authority

- F-1 不需要其他 authority，也沒有契約語義不足或 boundary 疑義需要交 Design Authority。
- 既有的 acceptor 保留事項維持原狀，不是本紀錄新增的 gate：
  - 推送本 branch 由派工者依 SA-1 決定。
  - 合併本 branch 屬 RB-1。
  - iLearning 繳交屬 RB-2（OI-V2-10）。
  - 是否消除 favicon 404（C-1）與是否對 `home_work_01` 跑 smoke（C-3），都是 acceptor 的選擇。
- 依 DA phase acceptance OI-V2-1，本 audit closure 之後，OI-V2-1 可以結案。

## 7. 證據位置（本機 scratchpad，不進 git）

`…/scratchpad/r1pg/`（session `37216426-f292-44f9-bad1-e2d862e7b8f1`）：

- 腳本 `scripts/`：
  - `live.mjs`、`probe.mjs`、`probe2.mjs`（CDP）。
  - `judge.py`。
  - `zipcmp3.py`（不輸出檔名）。
  - `a4.py`（只輸出計數）。
  - `binding.py`。
- 結果：
  - `out/`、`out2/`：主檢查兩組，`chrome.json`、`edge.json` 與截圖。
  - `out3/`：D-5、D-8。
  - `out4/`：H-5 探測。
- 輸入與參照：
  - `fetch/`：Pages 上取得的 17 個檔案。
  - `blob/`：`062e8a4` 的 blob。
  - `v1ref/`：`5d650b1` 的 V1 參照。
  - `teacher/`：curl 取得的老師 CSV。
  - `probe_in/h5_probe.csv`：synthetic。
- 寫入的追蹤檔案只有本 record；沒有 commit，沒有 git 寫入操作。

VERDICT: CLOSURE
