# Audit record — Issue #21，cycle 1，R2

| 欄位 | 內容 |
| --- | --- |
| Work Contract | GitHub Issue #21（`yotsubamomo/aiot-classwork`）「Dashboard 部署到 Vercel：公開 URL 與健康 endpoint smoke」，Scope class MVM。Spec `home_work_01/doc/spec/SPEC.md` v1.1；Outcome Contract `home_work_01/doc/governance/outcome-contract.md`（ACCEPTED 2026-09-23）；裁決 DR-1、DR-7、DR-12、H-1／A-1。與 R1 相同。 |
| 受審 subject | branch `home_work_01-hw10-implementation`，HEAD **`f02a1df20e82ee6ae145d69d5a6decf6a914d3c9`**（`git ls-remote origin` 同一個 SHA）。修正程式碼在 **`e27c1dc`**；`f02a1df` 只加了 worklog 與 `doc/acceptance/screenshots/` 兩張 PNG（`git diff --stat e27c1dc..f02a1df` 驗證）。R2 範圍 `d2c98fe..f02a1df`，7 個檔案，全部在 `home_work_01/` 內。 |
| Audit 種類 | **R2**（scoped closure review，治理 §4.4），**cycle 1**。R1 record 為 `audit/issue-21-c1-r1.md`，verdict BLOCKING (F-1)。 |
| 角色 | `primary_reviewer`（`gov-primary-reviewer`；Bindings §3.1 mapping `claude-opus-5-5`／`xhigh`）。延續本 Reviewer 的 R1 context（Bindings §3.5 第 1 點），沒有繼承 Executor context。所有證據都從磁碟、git 與線上部署重新取得，沒有沿用 R1 的輸出。 |
| Binding 證據 | 由派工者（Orchestrator）依 Bindings §3.4 核對，記在 run record `home_work_01/doc/governance/run/run-20260924-hw01-formal.md`。 |
| Independence | 同 R1：worklog 與派工訊息都當作待驗證的主張。探測、渲染、mutation、smoke 行為測試都由 Reviewer 自己執行，本紀錄由 Reviewer 用自己的 Write 工具寫入。 |
| 日期 | 2026-09-24（線上探測時間為 2026-09-23T21:29Z–21:33Z） |

## 1. 重讀的內容

- `git diff d2c98fe..f02a1df`：`api/index.py`（+53／−1）、`smoke.py`（+42）、`README.md`（+5／−1）、新增 `tests/test_vercel_path_decoding.py`（123 行）、worklog、兩張截圖。
- 以下檔案在 `d2c98fe..f02a1df` 之間 `git diff --stat` 為空，完全沒有變動：`server.py`、`static/*`、`vercel.json`、`requirements.txt`、`weather_query.py`、`app.py`、`.python-version`、`data.db`，以及除新檔以外的全部 `tests/*`。
- 其他：`git diff --check` 乾淨；沒有 `home_work_01/` 以外的路徑（RB-5）；commit message 符合 git 規則，沒有 Claude 標記。工作樹的實作與 `f02a1df` 相同（`git diff --stat f02a1df -- home_work_01 ':!home_work_01/doc'` 為空）。

## 2. F-1（High，blocking）是否真正解決：**已解決**

### 2.1 修正內容

`api/index.py:37-71` 新增 WSGI middleware `PercentDecodedPathInfo`。只有在 `PATH_INFO` 含 `%` 時（`:61`）才作用，作法是 `unquote_to_bytes(raw).decode("latin-1")`（`:62`），把路徑還原成 PEP 3333 規定的形式：已解碼的 bytes，以 latin-1 字串承載。`app` 仍是 Flask 實例（`:70`），只把 `app.wsgi_app` 換成包裝後的版本（`:71`）。修正只在部署邊界，`server.py` 維持標準 Flask 語義。

### 2.2 部署與 commit 的對應

| Commit | Vercel commit status | GitHub deployment | 不可變 URL |
| --- | --- | --- | --- |
| `e27c1dc` | success，`…/2zcQ1r3NSXBYNhP5fwvFSuw81jB8`（21:20:01Z） | `6624687732`（`vercel[bot]`，Preview） | `aiot-hw01-weather-2bmr74dya-nchu-aiot-class.vercel.app` |
| `f02a1df` | success，`…/C1xiNY5UkRYKkS9dqG6MnTzuBX2J`（21:26:15Z） | `6624792619`（`vercel[bot]`，Preview） | `aiot-hw01-weather-5tc51a137-nchu-aiot-class.vercel.app` |

2026-09-23T21:29:38Z 對 branch-preview 別名取 `GET /`，得到 `data-deployment-id="dpl_C1xiNY5UkRYKkS9dqG6MnTzuBX2J"`，所以別名服務的是 `f02a1df` 的部署。

### 2.3 線上驗證

Reviewer 自己執行，對上表兩個不可變 URL 與別名三者都做：

- **16 個 API endpoint 比對**：以 `urllib.parse.quote` 編碼，與瀏覽器的 `encodeURIComponent` 相同。每個 URL 都是 `16 endpoints compared, 0 mismatches`，與本機 subject 的 `create_app()` 一致。包含六個 `/api/regions/<Region>/series`，R1 時這六個全部是 404，現在全部是 **200**。
- **與 `data.db` 直接比對**：對別名取六區序列，與直接以 `sqlite3`（`mode=ro`）執行 `SELECT dataDate, mint, maxt FROM TemperatureForecasts WHERE regionName = ? ORDER BY dataDate` 的結果比較，不經共用模組。六區都是 7 列，`equals_direct_SQL=True`，**6/6**。
- **真實瀏覽器**（headless Edge `--dump-dom`，別名，2026-09-23T21:30:52Z）：

  | 頁面 | heading | `#chart-status` | chart polyline | 表格 |
  | --- | --- | --- | --- | --- |
  | 預設 | `Temperature Forecast – 北部地區` | `hidden`，沒有文字 | `chart__line--maxt`、`chart__line--mint` | 7 列，`2026-09-24 / 23.3 / 31` … `2026-09-30 / 24.6 / 30.3` |
  | `?region=中部地區` | 同上格式 | `hidden` | 兩條 | 7 列，`24.8 / 32.8` … `24.3 / 29.8` |
  | `?region=東南部地區` | 同上格式 | `hidden` | 兩條 | 7 列，`24 / 31` … `25 / 30` |

  三個頁面都沒有出現「not available」訊息。數值與 `data.db` 相同。
- **截圖真實性**：Reviewer 以 1280×1200 對別名的 `?region=中部地區` 截圖，得到的 PNG 與 committed 的 `doc/acceptance/screenshots/issue-21-dashboard-central.png` **位元相同**（`cmp`，51245 bytes）。`issue-21-dashboard-default.png` 的內容與上表預設頁面的 DOM 相符。

### 2.4 離線回歸守衛

`tests/test_vercel_path_decoding.py` 以 `importlib` 載入 `api/index.py` 的 `app`，也就是 Vercel 實際呼叫的 WSGI callable（`:33-39`）。測試自己組 WSGI environ，把未解碼的 `PATH_INFO` 直接傳入（`:42-71`），刻意繞過會自動解碼的 Flask test client。它**確實重現了缺陷**：`test_plain_app_404s_without_fix`（`:99-106`）證明沒有 middleware 的 app 回 404，而且 body 含 `%E4%B8%AD`。

Reviewer 用 `git archive f02a1df` 把樹匯出到 scratchpad，對匯出樹做 mutation，repo 本身沒有被修改：

| Mutant | 結果 |
| --- | --- |
| A：刪除 `app.wsgi_app = PercentDecodedPathInfo(...)` | **6 failed, 3 passed** |
| B：middleware 主體改成 no-op | **6 failed, 3 passed** |
| C：錯誤的承載方式 `.decode("utf-8")` | **6 failed, 3 passed** |
| 還原 | 9 passed |

三種 mutant 下，六個 Region 的測試全部失敗，所以守衛有效。

### 2.5 Endpoint 形狀與 INV-2

`server.py`、`static/app.js`、既有 tests 都沒有變動，README 的 `/api/` 清單也沒有變動，所以 endpoint 形狀沒有改變。線上六區的值等於 `data.db`，INV-2 維持。`app.py` 沒有變動。`/api/days/<date>` 在三個 URL 上都是 200，而且等於本機。

**結論：F-1 已解決。** R1 列出的 closure 證據都已具備：部署上六區 200 且等於 `data.db`；真實瀏覽器在三個 Region 都顯示圖與 7 列表格；AC-15 smoke 與 deployment id 已對新 subject 重做（見 §3）；有離線回歸證據，且經 mutation 證明有效。

## 3. 回歸，以及修正直接引入或暴露的缺陷：**沒有 blocking**

- **離線全套**：以單元 `.venv`（Python 3.12.14）執行 `pytest -q -p no:cacheprovider`，**152 passed**。在 `git archive` 匯出的乾淨樹（沒有 `.env`）執行，同樣 152 passed。
- **AC-15／R-DS-9 重做**：`smoke.py <別名>` 得到 `attempt 1 … GET / -> 200  GET /api/health -> 200  (0.6s elapsed)  PASS`、`SMOKE PASS`、exit 0（21:32:41Z）。以 `HW01_DEPLOY_URL` 指向 `f02a1df` 的不可變 URL，用**系統 Python 3.11.2**（沒有安裝任何套件）執行，同樣 PASS、exit 0，所以 stdlib-only 仍然成立。
- **解碼的安全面**：修正後 `%2F`、`%2E` 會被解碼，Reviewer 對別名做了下列探測：
  - 以下路徑都回 **404**，檔案沒有外洩：`/static/..%2Fserver.py`、`/static/%2E%2E/server.py`、`/static/%2e%2e%2fdata.db`、`/api/..%2Fserver.py`、`/static/%2E%2Eserver.py`、`/data.db`、`/server.py`、`/api/index.py`、`/.env`。原因是 Flask 的 `send_from_directory` 用 `safe_join` 擋掉 `..`。
  - `/static/..%2F..%2Fhome_work_01%2Fdata.db`、`/%2E%2E/%2E%2E/etc/passwd`、`/api/health%00` 由 Vercel edge 回 400 `BAD_REQUEST`。`/api/regions/%ZZ/series` 由 edge 拒絕，HTTP/2 是 PROTOCOL_ERROR，HTTP/1.1 是 400。修正前的 `d2c98fe` 部署（`…-y7nw8kg1g-…`）對這些路徑有相同的回應，所以不是修正造成的。
  - 雙重編碼的 `%25E4…` 只被解碼一次，得到 `Unknown Region: '%E4%B8%AD…'`、404，沒有發生二次解碼。
  - 無效的 UTF-8（`%FF%FE`）回 404，錯誤訊息是 `'��'`，沒有 500。
  - `%41BC` 解碼成 `ABC`，回 404。
  - `/static/app%2Ejs` 回 200，修正前是 404，這才是符合 PEP 3333 的行為。
  - 區段內的 `%2F`（`…%E5%8D%80%2Fseries`）解碼後會路由到 series，回 200。這與本機 PEP 3333 server 會解碼 `%2F` 的行為相同，不是新的暴露面。
- **本機執行路徑不受影響**：`python server.py` 與 `flask --app server run` 使用 `server.app`，不經 `api/index.py`。middleware 只在 `PATH_INFO` 含 `%` 時作用，所以 test client 或本機 server 送入的已解碼 latin-1 路徑不會被處理，是 idempotent 的。
- **R1 已 PASS 的項目不受影響**：AC-23（`.python-version` 沒有變動，含 pin 的兩個 commit 都建置成功）、AC-30（部署設定位置沒有變動，root 仍沒有本單元設定檔）、R-TC-7（見 §4）、INV-8，都維持 R1 的判定。

## 4. #21 自己負責的 Low findings

- **F-2（`smoke.py` budget）：已修正。** 修正後每次嘗試前先檢查剩餘時間，用完就結束（`smoke.py:106-107`）。每個請求的 timeout 取 `min(15, 剩餘時間)`（`:112`）。成功若發生在 deadline 之後，判為 FAIL（`:121-127`）。Reviewer 用 R1 的 test double 重測：

  | 情境 | 修正前（R1） | 修正後 |
  | --- | --- | --- |
  | R1 的情境（health 延遲 6 秒、10 秒後 ready，`--timeout 10`） | PASS，13.2 秒 | `SMOKE FAIL (no success within 10s)`，exit 1，wall 10.2 秒 |
  | 專測「超時才成功」分支（root 與 health 各延遲 4 秒、12 秒後 ready，`--timeout 15`） | — | `attempt 2 … PASS` 之後判 `SMOKE FAIL … passed after the 15s budget (17.1s elapsed)`，exit 1 |
  | 在 budget 內暖機成功（`late 1 3`，`--timeout 10`） | — | `SMOKE PASS (3.1s)`，exit 0 |
  | 內容檢查（沒有標題、health status 錯誤） | FAIL | 仍然 FAIL，exit 1 |
  | 沒給 URL | exit 2 | exit 2（`:177`） |

  結論是 **PASS 不可能在 budget 之後被回報**。殘餘見 N-2。
- **F-4（worklog／README）：已修正。**
  - (a) worklog `:55-56` 引用 AC-23 原文「Vercel 部署日誌或設定顯示 Python 3.12（截圖或日誌摘錄）」，與 Ticket 一致。
  - (b)「無法從外部辨識受審 commit」的說法已刪除，改用 deployment id 證明對應（`:99-103`）。
  - (c) `README.md:268-271` 改成別名服務的是分支「most recent successful build」，並提醒用 deployment id 確認，與 Reviewer 觀察到的行為一致。
  - (d) worklog 的 AC 對照表新增 R-DS-8 列（`:89`）。AC-07(e) 拆成「不需環境變數 PASS」與「未設定金鑰，待 acceptor」兩列（`:87-88`），這與 R1 F-3 的 disposition 一致。
- **F-3**：依派工，這項仍由 acceptor 負責（Orchestrator 取得證據，最晚 #25 記錄），不屬於本 cycle。Executor 沒有嘗試取得，這是正確的。

## 5. High-risk H-1：修正是否影響先前的核對（A-1，R2 重述）

- **這次修正觸及的 H-1 範圍**：部署產物（`api/index.py`）、測試、`smoke.py`、README、worklog、兩張截圖。
- **核對與結果**：
  - `f02a1df` 樹內 458 個追蹤檔案：以字面金鑰比對（從被忽略的 `.env` 在程序內讀入，**不輸出**），命中 **0**。以 pattern 掃描，命中的只有 R1 已列出的既有佔位字串，沒有新增。沒有追蹤 `.env`。
  - `d2c98fe..f02a1df` diff：pattern 命中 0 次，字面金鑰不存在。唯一出現的 `CWA_API_KEY` 在 worklog `:138`，是描述「線上無 `CWA_API_KEY`」的變數名稱，不是值。
  - `api/index.py` 與新測試裡的 `environ` 都是 **WSGI environ**，不是 `os.environ`。middleware 只 import `urllib.parse.unquote_to_bytes`，不讀任何環境變數或 secret，也沒有引入 HTTP client。
  - 兩張截圖的畫面內容只有 dashboard（Reviewer 已檢視），沒有金鑰。
  - `f02a1df` 的線上 `/`、`/static/*`、`/api/health`、`/api/regions`、`/api/days`，都沒有金鑰格式、字面金鑰、`CWA_API_KEY` 或 `opendata.cwa`。
- **結論**：修正沒有改變 R1 的 H-1 結論，INV-5 仍然成立。「Vercel 專案沒有設定 CWA 金鑰」仍待 acceptor 確認（R1 F-3），不在本 cycle。

## 6. 新的 non-blocking findings（不延長 cycle）

### N-1：`test_ascii_and_encoded_day_paths_both_resolve` 裡的「encoded」日期其實沒有編碼

- **Severity**：Low　**Blocking**：否
- **證據**：`tests/test_vercel_path_decoding.py:114` 用 `quote(date, safe="")` 產生「encoded」日期，但 `-` 是 unreserved 字元，`quote('2026-09-24', safe='')` 的結果仍是 `'2026-09-24'`（Reviewer 實測）。所以這個測試的後半段與 ASCII 案例完全相同，沒有測到解碼：在 mutant A、B、C 下它都照樣通過。worklog `:40` 與 `:118` 說「對 encoded 日期亦驗證 200」，說法過頭。實際行為是正確的：Reviewer 在線上對 `/api/days/2026%2D09%2D24` 取得 200（修正前是 404）。
- **Disposition**：可選的改進是改用真正的 percent-escape，例如把 `-` 寫成 `%2D`，並修正 worklog 的說法。Owner：#21 Executor（可選）或 #25。

### N-2：`smoke.py` 判定 FAIL 時，實際經過時間可能略超過 budget

- **Severity**：Low　**Blocking**：否
- **證據**：同一次嘗試有兩個依序的請求，各自的 timeout 都是嘗試開始時的剩餘時間，所以最後一次嘗試可能延伸到 deadline 之後。例如：`--timeout 8` 對連線被拒的 port，第 2 次嘗試在 9.9 秒結束，wall 10 秒；「超時才成功」的情境 wall 17.3 秒，budget 是 15 秒。Windows 的連線被拒重試本身也不受 timeout 控制。
- **影響**：PASS／FAIL 的**判定**是正確的，超過 budget 一定判 FAIL，所以不會接受 R-TC-7／AC-15 所禁止的「超過 90 秒才通過」。殘餘只是 FAIL 的回報時間稍晚，不違反契約。
- **Disposition**：記錄即可。如果 #22 的 workflow 需要嚴格的 wall-clock 上限，可以在那張票以 job `timeout-minutes` 或類似機制處理。Owner：#22（可選）。

### 觀察（不是 finding）

- **O-1（subject identity）**：`f02a1df` 新增的 `doc/acceptance/screenshots/*.png` 不在 Bindings §7 的 record-only path（`doc/governance/**`）內，所以嚴格來說 `f02a1df` 是一個新的 subject。Reviewer 因此直接審查 `f02a1df` 的部署：16 個 endpoint 0 mismatch、三個 Region 的渲染、smoke，都是對它做的，另外也審查了 `e27c1dc` 的部署。兩者行為相同，這兩張 PNG 也不會被 function 服務，所以本 R2 的 coverage 同時涵蓋 `e27c1dc` 與 `f02a1df`。worklog `:16`、`:79` 仍寫「受審 subject e27c1dc」，建議 Orchestrator 在 run record 記載 closure subject 為 `f02a1df`，程式碼 `e27c1dc`。
- **O-2**：R1 record `audit/issue-21-c1-r1.md` 在本 R2 開始時仍是 untracked（`git status` 顯示 `??`）。依 Bindings §3.5 第 4 點，應由派工者原樣 commit；本 R2 record 也一樣。

## 7. 需要其他 authority 的事項

- 本 cycle 沒有需要其他 authority 的事項。
- R1 F-3 仍依原 disposition，由 acceptor 透過 Orchestrator 提供證據（RB-3），最晚在 #25 記錄。這不是本 cycle 的 closure 條件。

VERDICT: CLOSURE
