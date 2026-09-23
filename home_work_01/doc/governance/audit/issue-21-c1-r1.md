# Audit record — Issue #21，cycle 1，R1

| 欄位 | 內容 |
| --- | --- |
| Work Contract | GitHub Issue #21（`yotsubamomo/aiot-classwork`）「Dashboard 部署到 Vercel：公開 URL 與健康 endpoint smoke」，Scope class MVM。所屬 Spec：`home_work_01/doc/spec/SPEC.md` v1.1（R-DS-8 完整、R-DS-9、R-SEC-3、R-TC-7 本機部分、R-ENV-1／2、R-DOC-1 部署段；AC-15、AC-23（Vercel 部分）、AC-30、AC-07(e)；INV-5、INV-8；AB-1）。Outcome Contract：`home_work_01/doc/governance/outcome-contract.md`（ACCEPTED 2026-09-23）。適用裁決：`decision-20260923-spec-interpretation-rulings.md` DR-1、DR-7、DR-12；`decision-20260923-high-risk-categories.md` H-1、A-1。分配依據：`derivation-SPEC.md` §11.1 #21 列。 |
| 受審 subject | branch `home_work_01-hw10-implementation`，commit `d2c98fe34d2bcb07d004d15b32e65c88364c02bb`；BASE `94c03c9`；範圍 `94c03c9..d2c98fe`，4 個檔案（`.python-version`、`README.md`、`smoke.py`、`doc/governance/worklog/issue-21.md`），全部在 `home_work_01/` 內。受審部署：Vercel deployment `dpl_DqwhNe6GVFGLC98tTtzxhJyAnqG7`（見 §1）。 |
| Audit 種類 | **R1**（對 accepted work scope 做完整的 independent audit），**cycle 1** |
| 角色 | `primary_reviewer`（definition `gov-primary-reviewer`；Bindings §3.1 mapping 為 `claude-opus-5-5`／`xhigh`） |
| Binding 證據 | 由派工者（Orchestrator）依 Bindings §3.4 核對，記在 run record `home_work_01/doc/governance/run/run-20260924-hw01-formal.md`。同一份 run record 記載的 Executor binding：agent `af810237365bf75d7` = `gov-executor`／`claude-opus-4-8`／`high`。Executor 與 Primary Reviewer 的 mapping 是不同模型，沒有 `diversity_lost`。 |
| Independence（治理 §2.3） | (1) 以 fresh context 派工，沒有繼承 Executor 的對話；worklog `worklog/issue-21.md` 與派工內容中的部署敘述一律當作待驗證的主張。(2) Binding 見上一列。(3) 自主取得：自行讀取 Ticket 本文（`gh issue view 21`，另讀 #23、#25 以確認分配）、Spec、Outcome Contract、derivation record、DR-7／DR-12、H-1 裁決、#19／#20 audit records、git 歷史與 diff、全部部署相關檔案；公開部署的探測、smoke、瀏覽器渲染、GitHub deployment 紀錄查詢、測試都由 Reviewer 自己執行。(4) 本紀錄由 Reviewer 用自己的 Write 工具寫入。 |
| 日期 | 2026-09-24（Reviewer 的線上探測時間為 2026-09-23T20:53Z–21:03Z，即 +08:00 的 2026-09-24 04:53–05:03） |

## 1. 審查方法與環境

- **確認 subject**：`git rev-parse HEAD` = `d2c98fe34d2b…`；`git ls-remote origin home_work_01-hw10-implementation` = 同一個 SHA。`git status --short` 只列出 `doc/governance/run/run-20260924-hw01-formal.md`，這是 Orchestrator 在 record-only path 上的修改（Bindings §7），不影響 subject identity。`git diff --stat d2c98fe -- home_work_01 ':!home_work_01/doc'` 為空，工作樹的實作與 subject 相同。`git diff --name-only 94c03c9..d2c98fe` 沒有任何路徑在 `home_work_01/` 外，沒有觸及 RB-5。`git diff --check` 乾淨。commit message 符合 git 規則，沒有 Claude 標記。
- **部署與 subject 的對應（AC-15 的「部署的 commit 與受審 subject 對應」）**：Reviewer 自己查到下列證據，彼此一致：
  - `gh api repos/.../commits/d2c98fe…/status`：context `Vercel`，state `success`，target_url `https://vercel.com/nchu-aiot-class/aiot-hw01-weather/DqwhNe6GVFGLC98tTtzxhJyAnqG7`（2026-09-23T20:47:21Z）。
  - `gh api repos/.../deployments?sha=d2c98fe…`：deployment `6624091124`，creator `vercel[bot]`，environment `Preview`；其 status 的 `environment_url` 為**這個 commit 專屬、不可變**的部署 URL `https://aiot-hw01-weather-y7nw8kg1g-nchu-aiot-class.vercel.app`。
  - 對 branch-preview 別名與上述不可變 URL 取 `GET /`，Vercel 注入的 toolbar 標籤都帶 `data-deployment-id="dpl_DqwhNe6GVFGLC98tTtzxhJyAnqG7"`，與 commit status 的 deployment id 相同（2026-09-23T21:02:59Z）。所以在審查時，別名服務的就是 `d2c98fe` 的部署。worklog §5.1／§7 說公開端點沒有版本標記、無法從外部確認對應，這個說法不正確，見 F-4。
  - 內容比對：兩個 URL 服務的 `static/app.js`、`static/styles.css` 與 `git show d2c98fe:home_work_01/static/…` 的 sha256 相同。`index.html` 的前 1711 bytes 與 subject 完全相同，只多了 Vercel 在 preview 注入的 toolbar `<script>` 一行（`cmp` 驗證）。`/api/health`、`/api/regions`、`/api/days` 與七個 `/api/days/<date>` 的 JSON，都與 Reviewer 在本機以 subject 樹 `create_app()` 產生的回應相同。`data.db` 的 blob 在工作樹與 subject 都是 `687586991ce3…`。
- **離線測試**：以單元 `.venv`（Python 3.12.14）執行 `pytest -q -p no:cacheprovider`，**143 passed**。
- **線上探測**（全部是唯讀 GET，沒有改動任何 Vercel 或 GitHub 狀態）：curl、`smoke.py`、Python `urllib` 比對腳本、headless Microsoft Edge `--dump-dom`（profile 放在 Reviewer 的 scratchpad）。
- **`smoke.py` 行為測試**：在 scratchpad 寫一個本機 test double（`slow_server.py`），模擬「根路徑沒有標題」「health 503」「health 200 但 status 不是 ok」「health 非 JSON」「health 延遲回應」。另外測連線被拒、沒給 URL、production URL（404）。
- **H-1 掃描**：在程序內讀取被忽略的 `home_work_01/.env` 取得字面金鑰，**只輸出布林值與次數，不輸出任何金鑰內容**。細節見 §3。
- Reviewer 啟動的本機 server 都已終止。`git status` 與開始時相同。

## 2. Acceptance criteria、需求與 invariants 逐條判定

| 項目 | 判定 | 證據 |
| --- | --- | --- |
| AC-15 | **PASS** | 對 branch-preview 別名（`…-git-homework01-hw10-im-8efc12-nchu-aiot-class.vercel.app`）與 `d2c98fe` 專屬的不可變 URL（`…-y7nw8kg1g-…`），在沒有任何 cookie 或 token 的情況下：`GET /` → **200**，body 含 `<title>Taiwan Weather Forecast</title>` 與 `<h1 class="title">Taiwan Weather Forecast</h1>`；`GET /api/health` → **200**，`{"forecast_day_count":7,"ingestion_time":"2026-09-24T02:24:50+08:00","region_count":6,"status":"ok"}`（curl 2026-09-23T20:53:57Z）。`smoke.py` 以 CLI 參數與 `HW01_DEPLOY_URL` 兩種方式執行：`[2026-09-23T20:54:16Z] attempt 1 … GET / -> 200  GET /api/health -> 200  PASS`，`SMOKE PASS`，exit 0。對不可變 URL：`[2026-09-23T20:57:46Z] attempt 1 … PASS`，exit 0。第一次嘗試就通過，遠在 90 秒內。部署與 subject 的對應見 §1。worklog §5.1 有時間戳、URL 與狀態碼。 |
| AC-23（Vercel 部分） | **PASS（以設定為證據；build log 無法取得，判斷見 §4）** | `home_work_01/.python-version` = `3.12`（`git show d2c98fe:…`，內容就是 `3.12` 加換行）。它位於 Root Directory `home_work_01` 的根，是 Vercel Python runtime 讀取的版本設定機制。含這個 pin 的 commit 由 Vercel 建置成功（commit status success），部署正常服務。旁證：部署的 function 以 `text/javascript` 提供 `/static/app.js`；Python 3.12 的 `mimetypes` 預設表是 `text/javascript`，3.11 是 `application/javascript`（Reviewer 在本機兩個版本實測）。這只能排除 ≤ 3.11，無法區分 3.12 與更新版本，所以只當旁證。 |
| AC-23（本機部分，INV-8 一致性） | **符合** | 單元 `.venv/Scripts/python.exe --version` → `Python 3.12.14`。系統的 `python` 是 3.11.2，但 README 的流程使用 3.12 venv，`.python-version` 也讓 uv 選 3.12。CI 部分屬 #22，本票不要求。 |
| AC-30 | **PASS** | `git ls-tree -r d2c98fe`：`vercel.json`、`requirements.txt`、`.python-version`、`data.db`、`api/index.py` 都在 `home_work_01/`。repo root 沒有 `vercel.json`、`requirements.txt`、`.python-version`、`runtime.txt`、`pyproject.toml`、`Pipfile`、`.vercelignore`、`package.json`。全樹只有 `.agents/skills/ui-styling/…` 與 `.claude/skills/ui-styling/…` 內的 skill 用 `requirements.txt`，它們不是本單元的設定。Root Directory = `home_work_01`：Reviewer 無法讀 Vercel 設定，但部署行為可以證明。部署服務的 Flask function 來自 `home_work_01/vercel.json` 與 `home_work_01/api/index.py`，`static/*` 與 subject 的 `home_work_01/static/*` 位元相同。repo 裡只有這個目錄有這些檔案，Root Directory 若是其他目錄，這些內容就不可能存在。對照組：`main` 沒有這些檔案，它的 production 部署回 404，與此一致。Ticket 要求的「設定截圖」見 F-3。 |
| AC-07(e)／R-SEC-3 | **「不需環境變數」PASS；「未設定 CWA 金鑰」無法由 agent 觀察，見 F-3** | 執行期程式（`server.py`、`api/index.py`、`weather_query.py`、`static/*`、`vercel.json`）對 `environ`、`getenv`、`dotenv`、`.env`、`CWA_API_KEY` 的 `git grep`，只命中 `api/index.py:10` 與 `server.py:9` 兩行說明「不讀環境變數」的 docstring。部署回 health 200，六區七天的資料來自打包的 `data.db`，不依賴任何環境變數。Vercel 專案的環境變數設定屬於 acceptor 的帳號（RB-3），Reviewer 與 Executor 都無法讀取。 |
| R-DS-8（完整） | **FAIL，見 F-1** | 以下子項 PASS：`vercel.json:3-8` 只有一個 `@vercel/python` build（`api/index.py`）；`:10-11` 把 `/(.*)` 全部導向它，也就是單一 function 同時服務頁面與 API。`includeFiles: data.db`，部署的 health 與六個 endpoint 的內容等於 subject 的 `data.db`，證明有打包。`weather_query.py:160-161` 以 `?mode=ro` URI 唯讀開啟。執行期不需要 secret。Python 3.12 見 AC-23。**但部署的 function 沒有正確提供 API**：R-DS-3(c) 的 Region 序列 endpoint 對六個 Region 全部回 404，見 F-1。 |
| R-DS-9 | **PASS** | 見 AC-15：不需登入，`GET /` 200 且含標題，`GET /api/health` 200。 |
| R-TC-7（本機部分） | **PASS（Low 缺陷見 F-2）** | `smoke.py` 只 import `argparse`、`json`、`os`、`sys`、`time`、`urllib.error`、`urllib.request`、`datetime`，全部是標準庫。用**沒有安裝任何套件**的系統 Python 3.11.2 直接執行也 PASS，所以 CI 不需裝相依就能沿用。檢查 `GET /` 200 且含標題（`smoke.py:78`）、`GET /api/health` 200 且 `status == "ok"`（`:84`）。每次嘗試都印出 UTC 時間戳、URL 與兩個狀態碼（`:104-108`）。失敗時 exit 非零：沒給 URL → exit 2（`:151-156`）；連線被拒、`--timeout 8` → `SMOKE FAIL`、exit 1；使用預設 90 秒 budget、連線被拒 → 第 10 次嘗試後 `SMOKE FAIL (no success within 90s)`、exit 1、實際經過 86 秒；production URL（404）→ exit 1；根路徑沒有標題、health 503、health `status: "degraded"`、health 非 JSON，四種情況都 `SMOKE FAIL`、exit 1。所以內容檢查確實會判否，不是只看傳輸層。90 秒上限可能被超過，見 F-2。 |
| R-ENV-1／R-ENV-2 | **PASS** | `requirements.txt` 在單元內，四個相依都固定版本。沒有 `folium`／`streamlit-folium`。本票的全部檔案都在 `home_work_01/` 內，root 沒有本單元的檔案。 |
| R-DOC-1（部署段、公開 URL） | **PASS** | `README.md:246-293` 新增「Deploy to Vercel (public URL & smoke check)」：說明單一 function 結構與 `includeFiles`（`:248-256`）；專案建立、Root Directory 與公開存取屬 acceptor 動作（`:258-264`）；production 與 preview 的差別，以及合併後的 smoke 是 release evidence（`:266-271`，與 DR-12 一致）；公開 URL 表（`:275-276`）；smoke 指令（`:278-293`）。`:196`、`:206` 原本寫「later ticket」，已改成連到本段。「alias always serves the current branch head」的措辭不夠精確，見 F-4。 |
| INV-5 | **PASS** | 見 §3。 |
| INV-8 | **目前沒有不一致** | 本機 3.12.14；Vercel 由 `.python-version` 固定為 3.12（AC-23 的判斷見 §4）；CI 屬 #22。 |
| AB-1 | **PASS（限 AB-1 的可觀察條件）** | 公開 URL 的應用頁面與健康 endpoint 都成功回應，見 AC-15。 |
| Ticket「What to build」：任何人打開公開 URL 就看到 Dashboard | **FAIL，見 F-1** | 公開 URL 上的頁面在預設 Region 與任何 Region，都只顯示「That Region is not available in this snapshot.」，沒有折線圖，表格是空的。 |

## 3. High-risk H-1（A-1 要求的一節）

- **觸及的類別**：H-1（憑證與機密）。本票觸及其中的「撰寫部署設定」「撰寫文件」，以及部署產物與 Vercel 環境變數這兩個涵蓋位置。
- **核對了什麼，結果如何**：
  1. **追蹤檔案（subject 樹，455 個檔案）**：用字面金鑰比對（從被忽略的 `.env` 讀入，不輸出）命中 **0** 個檔案。用 `ingestion.checks` 的 `KEY_PATTERN`／`AUTH_VALUE_PATTERN` 掃描，命中的只有既有文件與測試裡的佔位字串：`CWA-1234-5678-90ab-cdef`（`tests/test_secrets.py:29-30` 刻意放的合成樣本、`audit/issue-18-c1-r1.md:150` 引用同一樣本）、`"Authorization": "YOUR_API_KEY"`（`doc/requirement/REQUIREMENTS.md:55`）、`"Authorization": "..."`（課程總覽 `:43`）、`"Authorization":"…"`（`worklog/issue-18.md:93`）、`checks.py` 的 regex 本身。這些都不是本票的變更，也都不是真實的值。`git ls-tree` 裡沒有 `.env`。
  2. **Subject diff（`94c03c9..d2c98fe`）**：pattern 命中 0 次，字面金鑰不存在，沒有出現 `CWA_API_KEY`。
  3. **部署產物與設定**：`vercel.json`、`requirements.txt`、`.python-version`、`api/index.py`、`server.py`、`weather_query.py`、`static/*` 都沒有金鑰，也沒有讀取環境變數（見 §2 AC-07(e) 列）。`smoke.py` 只讀 `HW01_DEPLOY_URL`，那是公開 URL 而不是 secret；它不讀 `.env`，也不會被部署的 function import。
  4. **線上回應**：不可變部署 URL 的 `/`、`/static/app.js`、`/static/styles.css`、`/static/index.html`、`/api/health`、`/api/regions`、`/api/days`，都沒有金鑰格式、字面金鑰、`CWA_API_KEY` 或 `opendata.cwa`。
  5. **部署來源**：`d2c98fe` 的部署由 Vercel Git 整合（`vercel[bot]`，GitHub deployment `6624091124`）從已 push 的 commit 建置。未追蹤的 `.env` 不在 git 裡，所以不可能進入部署來源。依 GitHub deployment 紀錄與 worklog，本票沒有從本機目錄以 CLI 上傳部署；而且 Executor 的 Vercel token 對該 team 回 403，這條路也走不通。
  6. **Vercel 環境變數**：執行期不需要，已證明。專案是否**設定了**金鑰，只有 acceptor 能看（RB-3），見 F-3。即使設定了，程式也不讀取，第 4 點已證明它不會出現在任何回應中。
- **結論**：H-1 在 agent 可觀察的範圍內**沒有發現洩漏**，INV-5 成立。唯一的殘餘是「Vercel 專案沒有設定 CWA 金鑰」需要 acceptor 確認（F-3，non-blocking）。

## 4. AC-23 build log 的權限限制與 Reviewer 的充分性判斷

- **限制**：Vercel team `nchu-aiot-class` 的 build log 與專案設定，都在 acceptor 的帳號範圍內。依 worklog §2 與 run record，Executor 的 Vercel token 與 Orchestrator 的 Vercel MCP 都回 403。Reviewer 沒有這個 scope，也不會使用他人的憑證（RB-3 保留第三方帳號操作）。在現有 authority 下，build log 摘錄**無法取得**。公開端點不會暴露 Python 版本；worklog §2 也說明，為此在 health 或頁面加版本欄位會改變 AC-16／H-2 的契約，所以不加是對的。
- **判斷**：AC-23 的 PASS 條件是「Vercel 部署日誌**或設定**顯示 Python 3.12」。`home_work_01/.python-version` = `3.12` 是提交在部署 Root Directory 內、由 Vercel Python runtime 讀取的版本設定，它明確寫出 3.12。它也可以在 git 中逐位元驗證，來源比截圖更可靠。含這個 pin 的 commit 建置成功，部署正常服務。`.js` 的 MIME 旁證與 ≥ 3.12 一致。Reviewer 判定：**這份設定證據滿足 AC-23（Vercel 部分）的字面條件；build log 摘錄不是不可或缺。**
- **殘餘不確定**：設定證明的是「要求的版本」，不是「實際執行的版本」。如果 Vercel 忽略這個 pin，改用別的預設版本，FAIL 條件「三者任一不同」就無法從外部排除。這是證據強度的殘餘，不是實作缺陷；Executor 也無法再做什麼補強。建議 acceptor 在 release 或 #25 的驗收文件附一段 build log 或 Vercel 設定截圖，見 F-3。
- **語義路由（non-blocking）**：Spec AC-23 的證據欄寫「Vercel 設定截圖」，Ticket 寫「截圖或日誌摘錄」。如果 Design Authority 把「設定」解讀為只能是 Vercel dashboard 的設定畫面，那麼 AC-23 與 AC-30 的截圖就是 acceptor 必須提供的證據項（RB-3），不是 Executor 的 rework。本 verdict 不依賴這項解讀，因為 blocking 只有 F-1。

## 5. Findings

### F-1：部署上的 Region 序列 API 對六個 Region 全部回 404，公開 Dashboard 永遠顯示不出折線圖與表格

- **Severity**：High　**Blocking**：**是**
- **契約依據**：
  - Ticket #21 Traceability 的 **R-DS-8 完整**：「單一 Python serverless function **同時提供 API 與頁面**」。部署的 function 沒有提供 R-DS-3(c)「指定 Region 七日序列」：每個有效 Region 都被當成未知 Region。
  - Ticket #21「What to build」：「任何人打開 Vercel 公開 URL（不需登入）就看到 Dashboard」，以及「Executor 的工作是讓受審 commit 的部署成功……必要時作 targeted 修正部署設定」。Ticket 的 Cross-ticket invariants 也寫「本票證明 Vercel 路徑可行」。
  - Outcome Contract §2.2 MVM REQUIRED：「部署於 Vercel 的 dashboard」必須具備 MinT／MaxT 折線圖與 `Date`／`MinT`／`MaxT` 表格。AB-4：「兩個呈現層在選擇一個 Region 後都顯示……折線圖與……表格（7 列）」。§2.4 行為對等與 INV-2：「Dashboard 的 MVM 行為不弱於 Grading App」。
- **證據**：
  - 前端取得序列的方式是 `fetchJson("/api/regions/" + encodeURIComponent(region) + "/series")`（`static/app.js:99`），也就是中文 Region 名一定以 percent-encoding 送出。後端路由是 `@app.get("/api/regions/<region>/series")`（`server.py:121`）。
  - 對不可變部署 URL 與別名都執行：`curl "$D/api/regions/%E5%8C%97%E9%83%A8%E5%9C%B0%E5%8D%80/series"` → **HTTP 404** `{"error":"Unknown Region: '%E5%8C%97%E9%83%A8%E5%9C%B0%E5%8D%80' is not one of the six Regions."}`。
  - Reviewer 的比對腳本（`urllib.parse.quote` 編碼，與瀏覽器相同）把 16 個 endpoint 的線上回應與本機 subject `create_app()` 比較：health、regions、days 與七個 `/api/days/<date>` 都相同；**六個 `/api/regions/<Region>/series` 全部是線上 404、本機 200**（兩個 URL 結果相同）。
  - 機制：在 Vercel 上，path segment 到達 Flask 時**沒有經過 percent-decoding**。`/api/regions/%41BC/series` 回 `Unknown Region: '%41BC'`，沒有被解碼成 `ABC`；`/api/days/2026%2D09%2D24` 回 `Unknown Forecast Day: '2026%2D09%2D24'`；`/static/app%2Ejs` 回 404。本機的 Werkzeug 與 Flask test client 會解碼，所以 #20 的 22 個 Flask 測試無法重現這個問題。
  - 真實瀏覽器：用 headless Edge 對 `https://aiot-hw01-weather-y7nw8kg1g-nchu-aiot-class.vercel.app/` 執行 `--dump-dom`，六個 `<option>` 都在，heading 是 `Temperature Forecast – 北部地區`，但 `#chart-status` 顯示「That Region is not available in this snapshot.」，`<tbody id="table-body"></tbody>` 是空的。同一個頁面用 Reviewer 在本機啟動的 subject server（`127.0.0.1:18800`）渲染，`#chart-status` 為 `hidden`，表格從 `2026-09-24 / 23.3 / 31` 開始列出七列。
  - 這個缺陷在 BASE 就已存在：`94c03c9` 的部署（`…-exijd3s7g-…`）對 `中部地區` 同樣回 404。它來自 #20 加入的 `vercel.json`／`api/index.py`（`72ff874`），只在 Vercel 上發生。#20 的 audit 明確把實際部署劃給 #21（`issue-20-c1-r1.md:46`）。#21 負責部署與「必要時修正部署設定」，所以這是 #21 在契約內應處理的缺陷，不需要設計決定。R-DS-3 的 API 路徑形式依 DR-1 屬 HOW。
  - AC-15 本身仍 PASS，因為它只檢查 `/` 與 `/api/health`，所以 Executor 的 smoke 沒有發現這個問題。worklog §5.1 只探測到 `/api/regions`。
- **Closure 需要的證據（R2 會核對）**：修正後 subject 的**部署**上，六個 `/api/regions/<encodeURIComponent(Region)>/series` 都回 200，且等於 `data.db`／本機 subject 的輸出；公開 URL 的真實瀏覽器渲染在預設 Region 與至少另一個 Region，都顯示折線圖與 7 列表格；AC-15 smoke 與部署對應（deployment id）要對新的 subject 重做；另外依治理 §4.4 提供回歸證據，形式屬 HOW。注意 Flask test client 無法重現這個缺陷，證據必須包含部署本身。

### F-2：`smoke.py` 的 90 秒 budget 只在兩次嘗試之間檢查，所以可能在 budget 用完後才回報 PASS

- **Severity**：Low　**Blocking**：否
- **契約依據**：R-TC-7「總重試時間 ≤ 90 秒」；AC-15 的 FAIL 條件「超過 90 秒」；R-DS-9「最多 90 秒的暖機重試」。
- **證據**：`smoke.py:98` 設定 deadline；`:103` 每次嘗試執行兩個請求，各有 15 秒 timeout；`:112` 只在一次嘗試結束後才比較 deadline。所以最後一次嘗試可以在接近 90 秒時開始，再花最多約 30 秒（`urlopen` 的 timeout 是每次 socket 操作的上限，遇到慢速回應還可能更久）。成功時仍印 `SMOKE PASS`、exit 0。Reviewer 用 test double 實測：health 每次延遲 6 秒、10 秒後才 ready，搭配 `--timeout 10 --interval 1`，得到 `attempt 2 … PASS`、`SMOKE PASS`、exit 0，**實際經過 13.2 秒**，超過 budget。這次 AC-15 的實際證據是第一次嘗試就在 1 秒內通過，所以本票的判定不受影響。
- **附帶觀察**：嘗試失敗時，輸出只寫 `not-ready`，沒有說明是「缺標題」還是「health 的 status 不是 ok」。遇到「200／200 但失敗」時（Reviewer 的 nomark 與 hbad 測試），需要自己再查。這不是契約要求。
- **Disposition**：記錄即可，不延長本 cycle。可選的修正方式：讓每個請求的 timeout 受剩餘 budget 限制，或在 deadline 之後把結果判為失敗。Owner：#21 Executor 處理 F-1 時可以一併修正（可選）；否則交 #22，因為它的 `workflow_dispatch` 會原樣沿用這個檔案，同樣受 R-TC-7 約束。

### F-3：AC-23／AC-30 的「設定截圖／日誌摘錄」與 AC-07(e) 的「Vercel 未設定 CWA 金鑰」，都只能由 acceptor 提供證據

- **Severity**：Medium　**Blocking**：否
- **契約依據**：Ticket AC-23「Vercel 部署日誌或設定顯示 Python 3.12（截圖或日誌摘錄）」；AC-30「Root Directory ＝ `home_work_01`（設定截圖）」；AC-07(e)／R-SEC-3「Vercel 專案不需環境變數；未設定 CWA 金鑰」；H-1 的涵蓋位置包含「Vercel 環境變數」。
- **證據**：worklog §4 把 AC-07(e) 整項記為 PASS，但它的依據（§5.4）只證明「不需要」環境變數，沒有證明「沒有設定」。AC-23 與 AC-30 的截圖或日誌都不存在。這三項都需要讀取 acceptor 帳號內的 Vercel 專案，Executor 與 Orchestrator 都得到 403，而第三方帳號操作屬 RB-3。
- **為何不列為 blocking**：(1) AC-30 的實質（Root Directory = `home_work_01`）已由部署行為確定性證明（§2）。(2) AC-23 的設定證據已足以滿足字面條件，判斷見 §4。(3) 就「未設定金鑰」而言，執行期不讀任何環境變數，線上回應也沒有金鑰（§3 第 4 點），殘餘風險只是一個不會被使用、存放在 acceptor 自己帳號內的值，不構成公開外洩。(4) 這些證據只能由 acceptor 補，Executor 的 targeted correction 無法處理，列為 blocking 只會讓 cycle 卡住。
- **Disposition**：Owner：Orchestrator 向 acceptor 取得三項確認（build log 的 Python 版本行或設定截圖、Root Directory 截圖、Environment Variables 沒有 CWA 金鑰），記入 `doc/acceptance/`。最晚在 #25 的最終核對（AC-07 全項、AC-23 三處證據、AC-30）完成。worklog 的 AC-07(e) 列應改寫為只有「不需環境變數」PASS。如果 Design Authority 裁定截圖是必要證據，這仍然是 acceptor 的證據動作，見 §4 的語義路由。

### F-4：worklog 的部分敘述與證據不符

- **Severity**：Low　**Blocking**：否
- **契約依據**：治理 §3.7（worklog 必須如實）；Implementation Profile §7（Executor 報告是待驗證的主張）。
- **證據**：
  - (a) `worklog/issue-21.md:34` 說 Ticket 明示 evidence 可以是「build-log 摘錄 **and/or** 部署設定中的明確 runtime pin」。Ticket 原文是「Vercel 部署日誌或設定顯示 Python 3.12（截圖或日誌摘錄）」。worklog 把原文改寫成對自己有利的版本，應照原文引用。
  - (b) `:84-87`、`:139-140` 說公開端點沒有版本標記，無法從外部讀出別名正在服務的 commit。實際上可以：commit status 的 deployment id、GitHub deployment 紀錄（sha → 不可變 URL）、頁面注入的 `data-deployment-id` 三者可以互相印證（§1）。
  - (c) `README.md:267-268` 與 worklog `:84` 說 branch-preview 別名「always serves the current branch head」。更精確地說，別名指向該分支**最近一次建置成功**的部署；如果某次建置失敗，別名會繼續服務舊的 commit。所以應該用 deployment id 證明對應，不應假設。
  - (d) worklog §4 沒有列出 R-DS-8（Ticket 要求「R-DS-8 完整」），部署 API 的探測也只做了 `/api/regions`，所以沒有發現 F-1。
- **Disposition**：由 #21 Executor 在處理 F-1 更新 worklog 時一併更正。README 的 (c) 可選擇修正。

## 6. 觀察（不是 finding）

- **O-1（#19 O-3／#20 O-3：function 體積）**：`requirements.txt` 含 `streamlit`（連帶 pandas、pyarrow 等），但 `d2c98fe` 仍然建置成功並正常服務，所以在這個 subject 上，體積風險沒有發生。之後的票新增相依時才需要再看。
- **O-2（#20 F-6：dotenv 自動載入）**：這項只影響本機的 `python server.py`／`flask run`。Git 建置的 Vercel 部署沒有 `.env`，所以與本票的部署無關，仍依既有 disposition 由 #25 追蹤。
- **O-3（Vercel preview toolbar）**：Vercel 會在 preview 的 HTML 注入 `https://vercel.live/_next-live/feedback/feedback.js`（`data-explicit-opt-in="true"`）。這不是 subject 的程式，production 部署也不會注入。之後的票（#23／#24／#25）如果在 preview URL 做瀏覽器網路稽核（R-DS-5「前端只呼叫本應用程式的 `/api/`」），會看到這個外部請求，應該把它歸為平台注入，不要算成前端違規。
- **O-4**：production URL `https://aiot-hw01-weather.vercel.app` 目前 `GET /` 與 `/api/health` 都是 404（Reviewer 的 smoke 對它 exit 1），與 DR-12 一致：合併前 production 不是完成條件。

## 7. 需要其他 authority 的事項

- **Acceptor（經 Orchestrator，RB-3）**：F-3 的三項 Vercel 帳號內證據。不影響本 cycle 的 verdict。
- **Design Authority（可選）**：只有在 Orchestrator 或 acceptor 對「AC-23／AC-30 的『設定』是否包括提交在 repo 內、由 Vercel 讀取的設定檔」有疑義時才需要，見 §4。本 verdict 不依賴它。
- F-1 屬於契約內的實作與部署缺陷，走 Executor targeted correction，然後 R2；不需要設計決定。

VERDICT: BLOCKING (F-1)
