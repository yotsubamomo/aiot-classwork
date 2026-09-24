# Worklog — Issue #21 (Dashboard 部署到 Vercel：公開 URL 與健康 endpoint smoke)

- **Work item**：GitHub Issue #21（Formal lane），repo `yotsubamomo/aiot-classwork`。
- **Contract reference**：Ticket #21（accepted contract）＋ Spec `home_work_01/doc/spec/SPEC.md` v1.1
  （R-DS-8、R-DS-9、R-SEC-3、R-TC-7 本機部分、R-ENV-1/2、R-DOC-1 部署段；AC-15、AC-23（Vercel 部分）、
  AC-30、AC-07(e)；INV-5、INV-8；AB-1）。解讀依 decisions **DR-7**（`/api/health` 語義）、**DR-12**
  （AC-15 以受審 commit 的公開部署驗證；production 合併後更新為 release evidence，非完成條件）。
  High-risk **H-1**（部署產物與 Vercel 設定不得含金鑰；AC-07(e)），依 A-1 記錄核對。
- **Executing role and binding**：`gov-executor`（Model Profile `default/v2.2`：`claude-opus-4-8`、effort `high`）。
  binding 由派工者依 Bindings §3.4 從 harness 紀錄核對，記於 run record。
- **Subject / BASE**：branch `home_work_01-hw10-implementation`，BASE = `94c03c9`（#20 結案 HEAD）。
  只改 `home_work_01/` 內檔案。授權 push topic branch（SA-1）；不合併 `main`（RB-1）、不動 Vercel 專案設定、
  不設 repository variable、不付費（RB-3/RB-4，acceptor 動作）。
- **Commits**：
  - `d2c98fe`：初次交付（Python 3.12 pin、`smoke.py`、README 部署段、worklog）。R1 audit 對此 commit。
  - `e27c1dc`：**cycle-1 targeted correction**（R1 的 blocking F-1，並處理 F-2、F-4）。**目前受審 subject。**

## 1. Work performed（含 cycle-1 correction）

### 初次交付（d2c98fe）
1. **AC-23（Vercel Python 3.12）** — 部署原本沒有任何 Python 版本 pin。新增 `home_work_01/.python-version`＝`3.12`
   （Vercel 文件記載的 pin 機制；project root＝Root Directory＝`home_work_01`，符合 R-ENV-2/RB-5）。
2. **R-TC-7（本機指令）** — 新增 `home_work_01/smoke.py`（標準庫，暖機重試，時間戳/URL/狀態碼，失敗非零 exit；
   URL 由 CLI 參數或 `HW01_DEPLOY_URL` 環境變數；#22 `workflow_dispatch` 沿用同一檔）。
3. **README（#21 段）**、**AC-30 / AC-07(e) / H-1** 核對。

### Cycle-1 targeted correction（e27c1dc；治理 §4.4）
R1 audit（`doc/governance/audit/issue-21-c1-r1.md`）verdict **BLOCKING (F-1)**。針對 blocking 作 targeted correction，
並處理 non-blocking 的 F-2、F-4（F-3 為 acceptor 帳號內證據，非本 Executor 可處理，見 §7）。

1. **F-1（High, blocking）修正** — 部署上 `/api/regions/<Region>/series` 對六個 Region 全部回 404。
   **根因**：Vercel 交給 WSGI 的 `PATH_INFO` **未經 percent-decoding**（不符 PEP 3333 一般行為），中文 Region 名以
   `%E4%B8%AD...` 到達 Flask，`<region>` 對不上六區清單 → 404；本機 Werkzeug／Flask test client 會 decode，所以離線
   測試假綠。**修法（HOW）**：在 Vercel 進入點 `api/index.py` 以 thin WSGI middleware（`PercentDecodedPathInfo`）
   把仍含 `%` 的 `PATH_INFO` 還原成 PEP 3333 形式（`unquote_to_bytes(raw).decode("latin-1")`），再交給 Flask 路由；
   middleware 只在 `PATH_INFO` 含 `%` 時作用（ASCII 路徑與已解碼的 latin-1 形式都不動，idempotent）。`app` 仍是 Flask
   實例（Vercel 偵測不受影響），只包 `app.wsgi_app`。**未改任何 endpoint 形狀**，故前端、tests、README `/api/` 清單
   不需更動；INV-2 值一致性保持。`server.py` 保留標準 Flask 語義。
2. **`/api/days/<date>` 與其他 path-segment endpoint** — 日期為 ASCII，`encodeURIComponent` 不編碼，故線上本就正常
   （R1 也如此判定）；middleware 一併涵蓋，回歸測試對 encoded 日期亦驗證 200（見 §5.2）。
3. **回歸守衛** — 新增 `tests/test_vercel_path_decoding.py`：直接以 encoded `PATH_INFO`（如 Vercel 所送）呼叫**部署用的
   WSGI callable**（`api/index.py` 的 `app`），六區皆需 200 且值等於 `data.db`；另證明「拿掉 middleware 的 plain app 對
   encoded 路徑仍 404」。Flask test client 會 decode，無法重現，故測試繞過它、直接建 WSGI environ。
4. **F-2（Low）修正** — `smoke.py` 的 90 秒 budget 原本只在兩次嘗試之間檢查，可能在 budget 用完後才回報 PASS。
   改為：每次請求 timeout 受剩餘 budget 上限限制；且若成功發生在 deadline 之後判為 FAIL。
5. **F-4（Low）更正 worklog／README** — (a) 依原文引用 AC-23；(b) 移除「無法從外部辨識受審 commit」的錯誤敘述，改記
   以 `data-deployment-id` 對應（見 §5.1）；(c) README「always serves the current branch head」改為「serves the
   branch's most recent successful build … confirm the deployment id」。

## 2. Decisions and assumptions

- **F-1 修法選擇**：於 `api/index.py`（部署邊界）decode，而非 `server.py`。理由：缺陷是 Vercel 特有（平台不 decode），
  在邊界修正可保 `server.py` 標準語義；且本機 `PATH_INFO` 已是解碼後的 latin-1 形式，若在共用層無條件 decode 會把已解碼
  路徑二次編碼而破壞本機行為——middleware 的「只在含 `%` 時作用」正是避免此問題（本機路徑無 `%` → 不動）。
- **AC-23 evidence（依原文引用，F-4a）**：Ticket AC-23 原文為「Vercel 部署日誌**或設定**顯示 Python 3.12（**截圖或
  日誌摘錄**）」。本 session 的 Vercel token 無 `nchu-aiot-class` team scope（`get_deployment`/`list_teams` 皆 403/空），
  無法取 build log 或 dashboard 設定截圖。依原文「或設定」，以提交在部署 Root Directory 內、由 Vercel Python runtime 讀取
  的 `.python-version`＝`3.12`（可於 git 逐位元驗證）作為「設定」evidence。含此 pin 的 `e27c1dc` 由 Vercel **建置成功**
  （commit status `success`，deployment `dpl_2zcQ1r3NSXBYNhP5fwvFSuw81jB8`），部署正常服務——證明 3.12 pin 未使建置失敗。
  **限制**：build log 摘錄／dashboard 截圖屬 acceptor 帳號證據（F-3，非本 Executor 可補）。
- **不加執行期版本標記**：不在 `/api/health` 或頁面加 Python 版本或 commit 欄位——會改動 AC-16／H-2 契約，超出本票。
- **DR-12**：AC-15 以受審 commit 的公開（不需登入）部署為 PASS；production URL 合併後才更新，屬 release evidence。

## 3. Artifacts

| 類型 | 路徑 | 說明 |
| --- | --- | --- |
| 新增 | `home_work_01/.python-version` | `3.12`；本機/CI/Vercel runtime pin（R-DS-8、R-ENV-1、AC-23、INV-8）。 |
| 新增 | `home_work_01/smoke.py` | stdlib deploy smoke（R-TC-7、AC-15）；F-2 修正後強制 budget；#22 沿用。 |
| **修改（e27c1dc）** | `home_work_01/api/index.py` | **F-1 修正**：PATH_INFO decode middleware；`app` 仍為 Flask 實例。 |
| **新增（e27c1dc）** | `home_work_01/tests/test_vercel_path_decoding.py` | **F-1 回歸守衛**：encoded PATH_INFO → 六區 200＋值一致；plain app 仍 404。 |
| 修改 | `home_work_01/README.md` | Vercel 部署段；F-4c 措辭更正。 |
| 新增 | `home_work_01/doc/acceptance/screenshots/issue-21-dashboard-default.png`、`…-central.png` | 線上渲染截圖（F-1 closure）。 |
| 記錄 | 本檔 | worklog（record-only path）。 |

`vercel.json`、`server.py`、`weather_query.py`、`static/*`、`data.db` 未變。修正只在 Vercel 進入點與離線測試；deployed
runtime 行為對 encoded 路徑修正、其餘不變。

## 4. AC / requirement 對照（受審 subject e27c1dc）

| 項目 | 結果 | Evidence（§5） |
| --- | --- | --- |
| AC-15（公開 URL、不需登入、90s 內、對應受審 commit） | PASS | §5.1（AC-15 re-smoke；deployment-id 對應） |
| AC-23（Vercel Python 3.12） | PASS（以「設定」pin 為證據，依原文；build 成功）；build-log/截圖為 acceptor 證據（F-3） | §5.3 |
| AC-23（本機 3.12） | PASS（`.venv` 3.12.14） | §5.3 |
| AC-30（部署設定＋requirements 在單元；Root Directory；root 無單元設定檔） | PASS（Root Directory 由部署行為確證；dashboard 截圖為 acceptor 證據 F-3） | §5.4 |
| AC-07(e)：Vercel 不需環境變數 | PASS（部署以無 secret 服務） | §5.5 |
| AC-07(e)：Vercel 未**設定** CWA 金鑰 | **未由 agent 驗證**——需 acceptor 讀取專案設定（F-3，acceptor-owned，本票未做） | §5.5、§7 |
| R-DS-8 完整（含「單一 function 同時提供 API 與頁面」） | PASS（F-1 修正後六區 series 線上 200） | §5.1、§5.2 |
| R-DS-9（公開不需登入；GET / 200 含標題；health 200） | PASS | §5.1 |
| R-TC-7（本機指令；budget 強制） | PASS | §5.6 |
| INV-2（Dashboard series ＝ 共用模組） | PASS（線上六區值＝data.db；離線 INV-2 測試） | §5.1、§5.2 |
| INV-5（金鑰零外洩） | PASS | §5.5 |
| INV-8（Python 3.12 三處一致） | 本機 3.12；Vercel 由 pin 固定；CI 屬 #22 | §5.3 |

## 5. Verification（受審 subject e27c1dc）

### 5.1 F-1 closure — 線上六區 encoded series ＋ 渲染 ＋ AC-15 re-smoke ＋ commit 對應
- **受審部署與 commit 對應（更正 F-4b）**：`e27c1dc` 的 Vercel build `success`，deployment
  `dpl_2zcQ1r3NSXBYNhP5fwvFSuw81jB8`（commit status target `.../aiot-hw01-weather/2zcQ1r3NSXBYNhP5fwvFSuw81jB8`）。
  GitHub deployment `6624687732` 的 immutable URL＝`https://aiot-hw01-weather-2bmr74dya-nchu-aiot-class.vercel.app`。
  branch-preview 別名與該 immutable URL 的 `GET /` 都注入 `data-deployment-id="dpl_2zcQ1r3NSXBYNhP5fwvFSuw81jB8"`
  ——三者一致，證明別名服務的就是 `e27c1dc`（2026-09-23T21:19–21:22Z）。
- **六區 encoded `/api/regions/<encodeURIComponent(Region)>/series`（別名，2026-09-23T21:21Z）**：六個全部 **HTTP 200**、
  每區 7 列、值等於本機 `weather_query.region_series(region, data.db)`（`values==data.db: True` × 6）。encoded 路徑例：
  `/api/regions/%E5%8C%97%E9%83%A8%E5%9C%B0%E5%8D%80/series`、`…%E4%B8%AD%E9%83%A8…`、`…%E5%8D%97%E9%83%A8…`、
  `…%E6%9D%B1%E5%8C%97%E9%83%A8…`、`…%E6%9D%B1%E9%83%A8…`、`…%E6%9D%B1%E5%8D%97%E9%83%A8…`。
- **AC-15 re-smoke（別名，2026-09-23T21:21:08Z）**：`GET /`→200 含標題、`GET /api/health`→200 `status:"ok"`；
  `smoke.py` `SMOKE PASS`、exit 0、第一次嘗試 0.6s（遠在 90s 內）。
- **真實瀏覽器渲染（headless Chrome，`--virtual-time-budget`）**：
  - 別名 `/`（預設 Region 北部地區）：DOM 有 2 條 chart polyline（MaxT/MinT）、表格 7 列、heading
    `Temperature Forecast – 北部地區`、**0** 個「not available in this snapshot」訊息。截圖
    `doc/acceptance/screenshots/issue-21-dashboard-default.png`（可見折線圖與 7 列 `Date/MinT/MaxT`，值 23.3/31…24.6/30.3）。
  - 別名 `/?region=中部地區`：截圖 `…issue-21-dashboard-central.png`（另一個 Region 亦正常渲染；線上該區 series 200＝data.db）。

### 5.2 F-1 離線回歸守衛
- `tests/test_vercel_path_decoding.py`：以 encoded `PATH_INFO` 呼叫 `api/index.py` 的 `app`，六區皆 200＋值＝data.db；
  `/api/days/<date>` ASCII 與 encoded 皆 200；`/api/health`（ASCII）不受影響；`test_plain_app_404s_without_fix` 證明
  plain app 對 encoded 路徑仍 404。
- **Regression bar（revert-fails-check）**：暫時註銷 `api/index.py` 的 `app.wsgi_app = PercentDecodedPathInfo(...)` 一行，
  `pytest tests/test_vercel_path_decoding.py` → **6 failed（六區 404≠200）, 3 passed**；還原後全數通過。確認移除修正即失敗。
- **全套離線測試**（單元 `.venv`，Python 3.12.14）：`pytest -q` → **152 passed**（原 143 ＋ 新 9）。

### 5.3 AC-23 / INV-8 Python 3.12
- 本機：`.venv/Scripts/python.exe --version` → **Python 3.12.14**。
- Vercel：`.python-version`＝`3.12`（部署設定內的明確 runtime pin，git 可逐位元驗證）。含此 pin 的 `e27c1dc` build `success`。
- 限制：無 team scope，無法取 build log 佐證實際執行版本（F-3，acceptor）。

### 5.4 AC-30 部署設定位置與 Root Directory
- `home_work_01/` 內：`vercel.json`、`requirements.txt`、`.python-version`、`data.db`、`api/index.py`。
- repo root 無本單元設定檔（`git ls-files` 的 `vercel.json`/`requirements.txt`/`.python-version` 僅在 `home_work_01/`；
  其餘 `requirements.txt` 在 `.agents`/`.claude` skills 目錄，非本單元）。
- Root Directory＝`home_work_01`：dashboard 截圖屬 acceptor 證據（F-3）；行為證據見 R1 §2（別名服務單元內容、`main` production 404）。

### 5.5 AC-07(e) / INV-5 / H-1 無 secret（A-1 一節）
- **觸及類別**：H-1（撰寫部署設定、撰寫文件；涵蓋位置含部署產物與 Vercel 環境變數）。
- **核對**：`git ls-files` **無** `.env`；新增/修改檔（`.python-version`、`smoke.py`、`api/index.py`、
  `test_vercel_path_decoding.py`、`README.md`）以金鑰格式搜尋 **0 筆**；部署產物與線上回應無金鑰、無 `CWA_API_KEY`、
  無 `opendata.cwa`；`smoke.py` 只讀公開 URL 變數、不讀 `.env`、不被部署 import；middleware 不引入任何 HTTP client
  或 secret（`from urllib.parse import unquote_to_bytes`，非 HTTP client，不觸發 R-SHR-5 靜態檢查）。
- **結論**：agent 可觀察範圍內無洩漏，INV-5 成立。**「Vercel 專案未設定 CWA 金鑰」需 acceptor 確認**（F-3）；即使設定，
  程式不讀取、線上回應無金鑰。

### 5.6 R-TC-7 `smoke.py`（budget 強制，F-2）
- 正常：別名 CLI 參數與 `HW01_DEPLOY_URL` 皆 `SMOKE PASS`、exit 0，輸出含 `(Xs elapsed)`。
- Budget：不可解析主機、`--timeout 6 --interval 2` → 第 3 次嘗試（~4.1s）後 `SMOKE FAIL (no success within 6s)`、
  exit 1、實測 wall 4s；不再於 budget 用完後才判 PASS。未給 URL → exit 2。

## 6. Audit status

Formal Ticket → independent audit **required**。**R1**（`audit/issue-21-c1-r1.md`）verdict **BLOCKING (F-1)**。
本 worklog 記錄 cycle-1 targeted correction（`e27c1dc`）與 closure evidence，交 **R2**（Primary Reviewer 續派，非本 Executor
context）核對 F-1 closure、回歸與修正引入之風險。本 worklog 的 verification 為 self-verification，不記為 audit PASS。

## 7. Remaining work / concerns / required authority

- **F-3（Medium，non-blocking，acceptor-owned；本票未做）**：AC-23 build-log／設定截圖、AC-30 Root Directory 截圖、
  AC-07(e)「Vercel 未設定 CWA 金鑰」——皆需 acceptor 讀取其 Vercel 專案（RB-3），Executor／Orchestrator 均 403。
  由 Orchestrator 向 acceptor 取得，記入 `doc/acceptance/`，最晚於 #25 最終核對。worklog 的 AC-07(e) 已拆為「不需環境
  變數 PASS」與「未設定金鑰 待 acceptor」（§4）。
- **AC-23 殘餘不確定**：pin 證明「要求版本」，非「實際執行版本」；build log 可補強（F-3）。`.python-version` 為官方支援標準
  pin，build 成功，風險低。
- 無 reserved boundary 命中：公開 URL 不需登入；未動 Vercel 設定、未付費、未合併 `main`。本票無 BLOCKED。
- **Out of scope（本票）**：CI/smoke workflow（#22）、README 端到端實跑（整合驗收票）、ENHANCED、F-3 的 acceptor 證據。

## 8. Change log（本 worklog）

| 時間 | 事件 |
| --- | --- |
| 2026-09-23T20:xxZ | d2c98fe：初次交付（Python 3.12 pin、smoke.py、README、worklog）。 |
| 2026-09-23T21:2xZ | e27c1dc：cycle-1 correction（F-1 修正＋回歸守衛、F-2、F-4）；線上六區 200、AC-15 re-smoke、渲染截圖、152 passed、revert-fails-check。 |
