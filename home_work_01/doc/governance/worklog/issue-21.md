# Worklog — Issue #21 (Dashboard 部署到 Vercel：公開 URL 與健康 endpoint smoke)

- **Work item**：GitHub Issue #21（Formal lane），repo `yotsubamomo/aiot-classwork`。
- **Contract reference**：Ticket #21（accepted contract）＋ Spec `home_work_01/doc/spec/SPEC.md` v1.1
  （R-DS-8、R-DS-9、R-SEC-3、R-TC-7 本機部分、R-ENV-1/2、R-DOC-1 部署段；AC-15、AC-23（Vercel 部分）、
  AC-30、AC-07(e)；INV-5、INV-8；AB-1）。解讀依 decisions **DR-7**（`/api/health` 語義）、**DR-12**
  （AC-15 以受審 commit 的公開部署驗證；production 合併後更新為 release evidence，非完成條件）。
  High-risk **H-1**（部署產物與 Vercel 設定不得含金鑰；AC-07(e)），依 A-1 記錄核對。
- **Executing role and binding**：`gov-executor`（Model Profile `default/v2.2`：`claude-opus-4-8`、effort `high`）。
  binding 由派工的 Orchestrator/主 session 依 Bindings §3.4 從 harness 紀錄核對。
- **Subject / BASE**：branch `home_work_01-hw10-implementation`，BASE = `94c03c9`（#20 結案 HEAD）。
  只改 `home_work_01/` 內檔案。授權 push topic branch（SA-1）以觸發 Vercel rebuild；不合併 `main`（RB-1）、
  不動 Vercel 專案設定、不設 repository variable、不付費（RB-3/RB-4，acceptor 動作）。

## 1. Work performed

1. **AC-15 smoke（公開 preview URL，不需登入）** — 對 acceptor 已連結、Root Directory ＝ `home_work_01`
   的 Vercel 專案（team `nchu-aiot-class`）branch-preview 公開別名做 smoke。
2. **AC-23（Vercel Python 3.12）** — 部署原本沒有任何 Python 版本 pin（無 `.python-version`、無 `runtime.txt`、
   `vercel.json` 無 `functions.runtime`），即 Vercel runtime 版本不被確定性固定，INV-8「三處一致」無保證。
   新增 `home_work_01/.python-version` ＝ `3.12`（Vercel 文件記載的 pin 機制；「project root」＝ Root Directory
   ＝ `home_work_01`，檔案落在單元目錄內，符合 R-ENV-2/RB-5）。
3. **R-TC-7（本機指令）** — 新增 `home_work_01/smoke.py`：標準庫（`urllib`）實作，檢查
   `GET /` 200 含 `Taiwan Weather Forecast`、`GET /api/health` 200 且 `status == "ok"`，暖機重試總預算
   預設 90 s，輸出含 UTC 時間戳、URL、兩個狀態碼，失敗 exit 非零。URL 由 CLI 參數或 `HW01_DEPLOY_URL`
   環境變數（＝ #22 smoke workflow 注入的 repository variable）提供；#22 的 `workflow_dispatch` 直接沿用同一檔。
4. **README（#21 段）** — 新增「Deploy to Vercel (public URL & smoke check)」：單一 function 結構、
   Python 3.12 pin、acceptor-only 專案/Root Directory 設定、production vs preview（DR-12）、公開 URL、smoke 指令；
   並把既有兩處「later ticket」措辭改為指向本段。
5. **AC-30 / AC-07(e) / H-1** — 核對部署設定位置、無環境變數需求、無金鑰。

## 2. Decisions and assumptions

- **AC-23 Vercel 3.12 的 evidence 取徑**：Ticket 明示 evidence 可為「build-log 摘錄 **and/or** 部署設定中的
  明確 runtime pin」。本 session 的 Vercel MCP token **無 `nchu-aiot-class` team scope**
  （`get_deployment` / `get_project` / `list_deployments` 皆回 403；`list_teams` 回空），因此無法讀取該專案的
  build log 或設定。依 Ticket 允許的替代，AC-23 的 evidence 以 **`.python-version` ＝ `3.12` 明確 pin**（committed
  在部署設定內）＋ push 後 rebuild 仍通過 smoke 為準。pin 機制與 3.12 為 Vercel 官方文件記載且支援
  （見 §5 Verification）。**限制**：無法以 build log 獨立確認 rebuild 實際跑在 3.12 且成功；見 §7 Remaining。
- **`.python-version` 而非 `pyproject.toml`/`runtime.txt`**：專案用 `requirements.txt`（非 pyproject），
  `.python-version` 是最小、對現有 `builds`＋`@vercel/python` 設定影響最小的 pin；不引入 pyproject 以免改變安裝方式。
- **不加執行期版本標記**：不在 `/api/health` 或頁面加 Python 版本欄位——那會改動 H-2/AC-16 定義的 health JSON
  契約與頁面契約，屬語義變更，超出本票；故不做（DR-7/AC-16 契約維持）。
- **DR-12**：AC-15 以受審 commit 的公開（不需登入）部署為 PASS；production URL（`aiot-hw01-weather.vercel.app`，
  ＝ repo variable `HW01_DEPLOY_URL`）目前 404、合併後才更新，屬 release evidence，非本票完成條件。

## 3. Artifacts

| 類型 | 路徑 | 說明 |
| --- | --- | --- |
| 新增 | `home_work_01/.python-version` | `3.12`；本機/CI/Vercel runtime pin（R-DS-8、R-ENV-1、AC-23、INV-8）。 |
| 新增 | `home_work_01/smoke.py` | stdlib deploy smoke（R-TC-7、AC-15）；#22 沿用。 |
| 修改 | `home_work_01/README.md` | 新增 Vercel 部署段（R-DOC-1 部署段、公開 URL、smoke 指令）；更新兩處 later-ticket 連結。 |
| 記錄 | 本檔 | 本 work item 的 worklog（record-only path）。 |

未改動任何應用程式碼（`server.py`、`weather_query.py`、`api/index.py`、`static/`、`vercel.json` 皆未變），
故受審部署的執行期行為與 BASE `94c03c9` 位元相同；本票只加入 build-time 版本 pin、非路由的本機 helper 與文件。

## 4. AC / requirement 對照

| 項目 | 結果 | Evidence（§5） |
| --- | --- | --- |
| AC-15（公開 URL、不需登入、90s 內、對應受審 commit） | PASS | §5.1 smoke 輸出（curl ＋ `smoke.py`），含時間戳/URL/狀態碼 |
| AC-23（Vercel Python 3.12） | 以明確 pin 為 evidence（Ticket 允許）；build-log 未能獨立確認（token scope，§7） | §5.2 `.python-version`；本機 3.12.14 |
| AC-23（本機 3.12） | PASS | §5.2 `.venv` `python --version` ＝ 3.12.14 |
| AC-30（部署設定＋requirements 在單元；Root Directory；root 無單元設定檔） | PASS | §5.3 |
| AC-07(e)（Vercel 不需環境變數；未設 CWA 金鑰） | PASS（部署以無 secret 服務，`/api/health` 200） | §5.4 |
| R-DS-9（公開不需登入；GET / 200 含標題；health 200） | PASS | §5.1 |
| R-TC-7（本機指令） | PASS（正常＋失敗路徑自驗） | §5.5 |
| INV-5（金鑰零外洩） | PASS | §5.4 H-1 掃描 |
| INV-8（Python 3.12 三處一致） | 本機 3.12 ＋ pin 使 Vercel/CI 固定 3.12；#22 CI 另設 3.12 | §5.2 |

## 5. Verification（方法、結果、限制、evidence）

### 5.1 AC-15 / R-DS-9 smoke（公開 preview，不需登入）

- **URL**：`https://aiot-hw01-weather-git-homework01-hw10-im-8efc12-nchu-aiot-class.vercel.app`
- **curl（2026-09-23T20:37:37Z / 本地 2026-09-24T04:37:37+0800）**：
  - `GET /` → **HTTP 200**；body 含 `Taiwan Weather Forecast`；`<title>Taiwan Weather Forecast</title>`。
  - `GET /api/health` → **HTTP 200**；`{"forecast_day_count":7,"ingestion_time":"2026-09-24T02:24:50+08:00","region_count":6,"status":"ok"}`。
  - `GET /api/regions` → **HTTP 200**；六個 Region 中文名，固定順序（北部/中部/南部/東北部/東部/東南部）。
  - response header `server: Vercel`、`x-vercel-id: ...iad1...`（Vercel Python function 執行），無登入導向（curl 直接 200）。
- **`smoke.py`（2026-09-23T20:40:33Z）**：CLI 參數與 `HW01_DEPLOY_URL` 兩路徑皆 `SMOKE PASS`、exit 0。
- **對應受審 commit**：branch-preview 別名依 Vercel git 整合追蹤 branch head；push 本票 commit 為 head 後
  rebuild 即服務該 commit。**限制**：公開端點無版本標記、Vercel API 無 team scope，無法從外部讀出「別名正服務的
  commit SHA」；對應性依 Vercel「branch-preview 別名 ＝ branch head」契約 ＋ push HEAD 成立。因本票未改執行期
  程式，別名服務 BASE 或本票 commit 的 smoke 結果相同。

### 5.2 AC-23 / INV-8 Python 3.12

- **本機**：`home_work_01/.venv/Scripts/python.exe --version` → **Python 3.12.14**（uv `--python 3.12` 建立）。
- **Vercel**：新增 `home_work_01/.python-version` ＝ `3.12`（deploy config 內的明確 runtime pin）。Vercel 文件
  `functions/runtimes/python/python-version`：於 project root（＝ Root Directory ＝ `home_work_01`）放
  `.python-version` 檔即固定 Python 版本；3.12 為支援版本（後端/Flask 文件 `requires-python = ">=3.12"`）。
- **限制**：token 無 `nchu-aiot-class` scope，無法讀 build log 以獨立確認 rebuild 的 Python 版本與成功。
  Ticket 允許以「部署設定中的明確 runtime pin」作 evidence，本項即以該 pin 為 AC-23 Vercel 部分之 evidence。

### 5.3 AC-30 部署設定位置與 Root Directory

- `home_work_01/vercel.json`、`home_work_01/requirements.txt`、`home_work_01/.python-version`、
  `home_work_01/data.db` 皆在單元目錄內。
- Root Directory ＝ `home_work_01`（acceptor 已設定；Orchestrator 偵察值，本票沿用，公開別名服務單元內容佐證）。
- **repo root 無本單元設定檔**：`git ls-files` 追蹤的 `vercel.json`/`requirements.txt`/`.python-version` 僅位於
  `home_work_01/`，root 無同名檔（見 §5 指令輸出）。

### 5.4 AC-07(e) / INV-5 / H-1 無 secret

- 部署以**無環境變數**服務：`/api/health` 200 且 `status:"ok"`，執行期未讀任何 secret（`server.py`、
  `api/index.py` 皆不讀 env/secret；程式碼註解與 #19/#20 靜態檢查已涵蓋）。
- H-1 掃描：`git ls-files` **無** `.env`；新增/修改檔（`.python-version`、`smoke.py`、`README.md`）以 CWA 金鑰格式
  搜尋 **0 筆**；`smoke.py` 不含任何金鑰、不讀 `.env`。部署產物（`vercel.json`、`requirements.txt`、
  `.python-version`、`api/index.py`、`server.py`）無金鑰字串。（A-1：本票觸及 H-1，已核對「部署產物與 Vercel
  設定不含金鑰、Vercel 不需環境變數」，結果為零金鑰。）

### 5.5 R-TC-7 `smoke.py` 自驗（正常＋失敗）

- 正常：對公開別名 CLI 參數與 `HW01_DEPLOY_URL` 皆 PASS、exit 0。
- 失敗：未給 URL → `error: no URL ...`、**exit 2**；`https://example.com`（200 但無標題、health 404）→
  `SMOKE FAIL`、**exit 1**（確認標題與 health-status 內容檢查會判否，非僅測傳輸）；不可解析主機（傳輸錯誤）→
  `SMOKE FAIL`、**exit 1**。
- offline 測試套件（`pytest`，Python 3.12.14）：**143 passed**；`smoke.py` 不在靜態檢查
  `_PYTHON_SIDE` 範圍（它是部署 client，非 presentation side），其 `urllib.request` import 不觸發 R-SHR-5 檢查。

（§5.3 的指令輸出、§5.4 的掃描指令輸出留在 Executor 執行紀錄；本檔以引用方式記錄，避免複製全文。）

## 6. Audit status

Formal Ticket → independent audit **required**（Bindings §5；A-1：本票觸及 H-1，R1 record 須明記 H-1 核對）。
本票為 self-verification 完成；independent audit 由 Orchestrator/主 session 依 Bindings §3.5 另派 `gov-primary-reviewer`
（非本 Executor context）。本 worklog 的 verification 為 self-verification，不記為 audit PASS。

## 7. Remaining work / concerns

- **AC-23 build-log 確認（未解，非 blocker）**：本 session 的 Vercel token 無 `nchu-aiot-class` team scope，
  無法讀 build log 獨立確認 rebuild 跑在 Python 3.12 且成功。Ticket 允許以明確 pin 作 evidence，故本項達 Ticket 的
  evidence 門檻；但無 build-log 佐證。建議由 acceptor（或有該 Vercel scope 的 Reviewer）在 Vercel 儀表板確認
  build log 顯示 Python 3.12；或於合併後 production build 一併surface 任何 pin 問題。`.python-version` ＝ `3.12`
  為官方支援的標準 pin，破壞 build 的風險低。
- **受審 commit 對應（未解，非 blocker）**：公開端點無版本標記，無法從外部讀出別名正服務的 commit SHA
  （見 §5.1）。對應性依 Vercel branch-preview 契約成立。
- **非 reserved boundary 命中**：公開 URL 不需登入（curl 直接 200），未遇 deployment protection；未動 Vercel 設定、
  未付費、未合併 `main`——皆為 acceptor 動作且已就緒。故本票無 BLOCKED。
- **Out of scope（本票）**：GitHub Actions CI/smoke workflow（#22）、README 端到端實跑（整合驗收票）、ENHANCED。

## 8. Change log（本 worklog）

| 時間 | 事件 |
| --- | --- |
| 2026-09-23T20:xxZ | 建立 worklog；記錄 AC-15 smoke、Python 3.12 pin、AC-30/AC-07(e)、`smoke.py` 自驗、README。commit＋push 見 Executor return。 |
