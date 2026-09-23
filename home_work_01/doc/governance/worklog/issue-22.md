# Worklog — Issue #22 (自動化測試整合與 GitHub Actions CI／smoke workflow)

- **Work item**：GitHub Issue #22（Formal lane，ENHANCED scope），repo `yotsubamomo/aiot-classwork`。
- **Contract reference**：Ticket #22（accepted contract）＋ Spec `home_work_01/doc/spec/SPEC.md` v1.1
  （R-TC-5、R-TC-6、R-TC-7、R-ENV-3、R-SEC-1（CI 自動化）、R-DOC-1（測試＋CI 段）；§5.3。
  AC-20、AC-21、AC-22、AC-29、AC-07(b–d 自動化)；INV-5、INV-8；AB-16、AB-17）。
  解讀依 decisions **DR-13**（workflow 範圍：path filter 至 `home_work_01/**` ＋ workflow 檔本身；smoke 為獨立
  `workflow_dispatch`；不對其他單元／root 觸發）、**DR-12**（AC-15/AC-22 的 production-vs-preview 時點：production 變數
  合併後才生效，preview 供現在示範）。High-risk **H-1**（CI 內金鑰掃描；workflow 不得印出 secret），本票實現
  **A-5**（機械檢查納入 CI），依 A-1 記錄核對。
- **Executing role and binding**：`gov-executor`（Model Profile `default/v2.2`：`claude-opus-4-8`、effort `high`）。
  binding 由派工者依 Bindings §3.4 從 harness 紀錄核對，記於 run record。
- **Subject / BASE**：branch `home_work_01-hw10-implementation`，BASE = `a7ecdd9`（#21 結案 HEAD）。
  實作與測試留在 `home_work_01/` 內；**唯一**的 root 變更是 §2 授權範圍內的兩個 `.github/workflows/` 檔（RB-5 §8.2）。
  未動 root `CLAUDE.md`、`docs/`、`.gitignore`、其他單元或其他 `.github/workflows/` 檔。授權 push topic branch（SA-1）；
  不合併 `main`（RB-1）、不設 repository variable（RB-3，acceptor 動作）、不付費（RB-4）。
- **Commits**（皆 push 到 topic branch，SA-1）：
  - `d854218`：初次交付（兩個 workflow、`tools/credential_scan.py`、smoke.py N-2 bound、README CI 段、worklog）。
  - `84060c9`：CI workflow YAML fix——一個 step name 的 unquoted colon-space 使 YAML 誤判為 nested mapping，
    workflow 在 parse 階段即失敗（0s，「workflow file issue」，未起任何 job）；加引號後修復。**目前受審 subject。**
  - `<c3>`：本 worklog 更新（run URL／證據；record-only path）。（SHA 於 push 後填入 §10。）

## 1. RB-5 §8.2 授權原文（AC-29）

本票在 repo-root `.github/workflows/` 建立檔案，依 Outcome Contract §8.2 acceptor 接受紀錄第 2 項的**逐字**授權
（`home_work_01/doc/governance/outcome-contract.md` §8.2）：

> 2. 我授權本單元所需的 RB-5 GitHub Actions 例外：
>    - 可以在 repo root `.github/workflows/` 建立與維護只服務 `home_work_01` 的 workflow；
>    - workflow 必須以 path filter 限定 `home_work_01/**` 以及該 workflow 檔案本身；
>    - 此授權不延伸到其他 root 檔案、其他單元或其他用途的 workflow。

兩個 workflow 都只服務 `home_work_01`：CI 的觸發 path filter 為 `home_work_01/**` 與 `.github/workflows/home_work_01-ci.yml`
自身；smoke 為 `workflow_dispatch`（不對任何 path 觸發），只 smoke 本單元的部署。檔名 `home_work_01-ci.yml`、
`home_work_01-smoke.yml` 識別本單元（AC-29）。未動任何其他 root 檔案或其他用途的 workflow（RB-5 邊界內）。

## 2. Work performed

1. **CI workflow** `.github/workflows/home_work_01-ci.yml`（R-TC-5/6、R-SEC-1、AC-20、AC-21、AC-07(b–d) 自動化、AC-29、
   INV-8）：
   - `on: push` ＋ `pull_request`（R-TC-6 MAY），兩者皆 `paths` 過濾至 `home_work_01/**` 與該 workflow 檔本身。
   - `defaults.run.working-directory: home_work_01`；`permissions: contents: read`。
   - Steps：checkout（`fetch-depth: 0`，供 committed-diff 金鑰掃描）→ setup-python `3.12` → `python --version`
     （log 顯示 3.12，INV-8）→ `pip install -r requirements.txt` → `python -m pytest -v`（全套離線；`-v` 使 log 顯示
     derive／DB／shared-module／AppTest／Flask-test-client／static 各類皆收集並通過）→ `python -m tools.credential_scan`
     （AC-07 b/c/d、A-5）。
2. **憑證機械檢查** `home_work_01/tools/credential_scan.py`（新增；A-5、AC-07 b/c/d、H-1）：
   - (b) `git ls-files` 無 `.env`（只允許 `.env.example`）；
   - (c) 追蹤檔案與 committed 歷史（`git log -p`）無 CWA 金鑰格式字串，明確排除被忽略的 `home_work_01/.env`；
   - (d) fixture 與保存的原始 JSON 無 `Authorization` 值、無金鑰格式字串。
   - 只印出「發現的路徑＋種類」，**不印任何 secret 值**（H-1）。金鑰／Authorization pattern 重用 `ingestion.checks`
     （與離線 `tests/test_secrets.py` 同一偵測器；後者未改動，其偵測器自我測試仍證明會 flag 金鑰）。
   - 以 `-m tools.credential_scan` 從 `home_work_01/` 執行，`ingestion.checks` import 可解析；git 以 `--show-toplevel`
     解析 repo root，掃描全 repo 追蹤檔（cwd 無關）。新增 `tools/__init__.py`。
3. **Smoke workflow** `.github/workflows/home_work_01-smoke.yml`（R-TC-7、AC-22、AB-17）：
   - `on: workflow_dispatch`，input `url`（選用，預設空）。
   - 步驟以 env 傳入 `INPUT_URL=${{ inputs.url }}`、`VAR_URL=${{ vars.HW01_DEPLOY_URL }}`，`URL="${INPUT_URL:-$VAR_URL}"`
     （input 非空則覆寫變數，否則用變數）；兩者皆空時以明確訊息 `exit 1`。**沿用 `smoke.py` 原檔**（R-TC-7 同一檢查）。
     smoke.py 只用標準庫，無需安裝相依。
4. **smoke.py N-2 bound**（#21 N-2，optional／non-blocking）：`_check_once` 改為接受 `deadline`，兩個 GET 各自以
   「剩餘 budget（≤15s，≥0.1s）」為 timeout，使**單次 attempt 的兩個請求合計不超出 budget**（先前慢的 root GET 之後
   health GET 仍以整個 budget 為上限，可能溢出）。行為與介面對外不變（CLI／env、輸出、exit code）。
5. **README**：新增「Continuous integration (GitHub Actions)」段（R-DOC-1）：本機執行測試（既有段）、CI（觸發／path
   filter／Python 3.12／pytest＋憑證檢查）、smoke（`workflow_dispatch`、`HW01_DEPLOY_URL` 變數名與選用 `url` input）、
   production-vs-preview 說明。

## 3. Decisions and assumptions

- **AC-07(c)／A-5 的「金鑰格式字串」掃描——documented example allowlist（HOW；本票唯一實質解讀，交 Reviewer 檢視）。**
  追蹤樹內唯一符合 KEY_PATTERN 的字串是 `CWA-1234-5678-90ab-cdef`——`tests/test_secrets.py` 用來證明偵測器會 flag 金鑰的
  **刻意假造**佔位值（另被兩份 audit record 引用）。真實 CWA 金鑰是 `CWA-` 前綴的 UUID（8-4-4-4-12）；此 4-4-4-4 佔位值
  不可能是註冊金鑰。掃描器在比對前移除此一 documented 例（`_EXAMPLE_ALLOWLIST`），使檢查保持有意義——**真實金鑰在
  任何檔案仍會被抓**——同時不因專案自己的 documented 例而誤報。**不弱化驗證**（impl-default §5）：見 §5.3 的
  literal-real-key self-verification（追蹤檔 0、歷史 0，且真實金鑰確實 match 廣義 pattern，故會被抓）。`ingestion.checks`
  未改，其偵測器仍會 flag 金鑰。此解讀記入本 worklog；若 Reviewer／DA 認為應改為別的機制，屬 targeted correction。
- **committed-diff 掃描以全歷史 `git log -p`**：checkout 用 `fetch-depth: 0` 供其掃描；binary blob 由 git 顯示為
  「Binary files differ」不含內容，故大二進位（`data.db`、原始 JSON）不被逐位元掃描（其內容另由追蹤檔掃描與 (d) 涵蓋）。
- **AC-20 negative（不含本單元變更不觸發）以 path filter config 為證據**：literal negative test 需 out-of-unit push
  （RB-5，禁止），不執行；改以 workflow 的 `paths` 設定與「本 run 每個 commit 都動到 `home_work_01/**` 故 CI 有觸發」佐證。
- **AC-22 現在以 preview 示範**：`vars.HW01_DEPLOY_URL` 指向 production（合併前 404，DR-12），故以 `url` input 帶入 live
  preview alias 示範；production 變數的 live run 為 release／#25 確認。
- **不新增產品功能、不改測試以外的產品程式**（Out of scope）：唯一的產品側改動是 smoke.py 的 N-2 bound（#21 遺留、
  optional 授權，且 smoke workflow 沿用此檔），介面不變；`tools/` 為 CI 專用工具，非 graded 應用碼。

## 4. Artifacts

| 類型 | 路徑 | 說明 |
| --- | --- | --- |
| 新增（root，RB-5 §8.2） | `.github/workflows/home_work_01-ci.yml` | push/PR 觸發、path 過濾至本單元、Python 3.12、pytest＋憑證檢查。 |
| 新增（root，RB-5 §8.2） | `.github/workflows/home_work_01-smoke.yml` | `workflow_dispatch`、`HW01_DEPLOY_URL` 變數＋選用 `url` input、沿用 smoke.py。 |
| 新增 | `home_work_01/tools/credential_scan.py` | AC-07 b/c/d 機械檢查（A-5、H-1）；重用 `ingestion.checks`。 |
| 新增 | `home_work_01/tools/__init__.py` | `tools` 套件（CI 工具，非產品 runtime）。 |
| 修改 | `home_work_01/smoke.py` | N-2 bound：兩 GET 合計不超出 budget；對外行為不變。 |
| 修改 | `home_work_01/README.md` | 新增 CI/CD 段（R-DOC-1）。 |
| 記錄 | 本檔 | worklog（record-only path）。 |

## 5. Verification（self-verification；治理 §3.5，非 audit）

### 5.1 全套離線測試（本機 `.venv`，Python 3.12.14）
- `python -m pytest -q` → **152 passed**（無網路、無 `.env`；R-TC-5）。收集涵蓋 derive（`test_derive`）、
  DB/persist（`test_persist`）、shared module（`test_weather_query`）、Streamlit AppTest（`test_app`）、
  Flask test client（`test_dashboard`）、static（`test_static_checks`）等類。CI 以 `-v` 重跑（§6 填入 run URL）。

### 5.2 憑證機械檢查（`tools/credential_scan.py`）
- `python -m tools.credential_scan` → exit 0：`460 tracked files; no .env tracked (only .env.example);
  no CWA-key-format string in tracked files or committed history; no Authorization value in fixture/raw JSON.`
- Pattern 自我測試：`tests/test_secrets.py::test_scanner_flags_a_key_and_auth_value` 仍 PASS（偵測器未被削弱）。

### 5.3 H-1 / INV-5 金鑰零外洩（A-1 一節）
- **觸及類別**：H-1（CI 內金鑰掃描；本票實現 A-5）。
- **核對**：
  - `git ls-files` **無** `.env`（只 `home_work_01/.env.example`）。
  - 追蹤樹符合 KEY_PATTERN 的唯一字串為 documented 假例 `CWA-1234-5678-90ab-cdef`（見 §3 allowlist）。
  - **literal-real-key self-verification**（金鑰從本機 `.env` 讀入、**全程未印出**）：真實金鑰長度 40、**match** 廣義
    KEY_PATTERN（故會被掃描器抓）、**不等於**假例；掃描全部 460 追蹤檔與全歷史 `git log -p` → **追蹤檔 0 筆、歷史 0 筆**
    含真實金鑰。⇒ allowlist 不遮蔽任何真實外洩。
  - 新增/修改檔（兩 workflow、`tools/*`、smoke.py、README、worklog）不含金鑰、不含 `CWA_API_KEY`、不含 `opendata.cwa`；
    workflow 不 echo secret（credential_scan 只印路徑與種類）。smoke workflow 只讀公開 URL 變數／input。
- **結論**：agent 可觀察範圍內 INV-5 成立。

### 5.4 smoke.py N-2 bound
- 失敗案例（黑洞 IP `http://10.255.255.1`、`--timeout 6 --interval 2`）：attempt 1 root GET 用滿 6s → health GET budget
  ≈0.1s 立即失敗 → `SMOKE FAIL (no success within 6s)`、exit 1、**實測 wall 6s**（修正前 root 6s＋health 6s≈12s 會溢出）。
- 缺 URL → exit 2（訊息不含金鑰）。正常路徑（CLI／`HW01_DEPLOY_URL`）行為不變（見 #21 §5.6）。

### 5.5 CI run（AC-20、AC-21、AC-07 自動化、INV-8）
- **Run**：push run `35925410250`（commit `84060c9`），conclusion **success**，
  `https://github.com/yotsubamomo/aiot-classwork/actions/runs/35925410250`。同一 push 另觸發 pull_request run
  `35925413146`（branch 已開 PR），亦執行（R-TC-6 MAY）。
- **log 摘錄**：
  - `Show Python version` step → `Python 3.12.14`；pytest 平台行 → `platform linux -- Python 3.12.14, pytest-8.3.3`（INV-8）。
  - pytest 各類皆收集且通過：`test_derive` 19、`test_persist` 5、`test_weather_query`（shared module）29、`test_app`
    （Streamlit AppTest）9、`test_dashboard`（Flask test client）23、`test_static_checks` 22 → `152 passed in 4.02s`（AC-20、AC-21）。
  - 憑證檢查 step → `credential scan passed: 465 tracked files; no .env tracked (only .env.example); no CWA-key-format
    string in tracked files or committed history; no Authorization value in fixture/raw JSON.`（AC-07 b/c/d、A-5）。
- **AC-20 negative（不含本單元變更不觸發）**：以 path filter config 為證據（§3；literal negative test 需 out-of-unit
  push＝RB-5，禁止）。本 run 的兩個 commit（`d854218` 動 `home_work_01/**` 與 workflow 檔；`84060c9` 動 workflow 檔本身）
  都落在 `paths` filter 內，故 CI 有觸發——與「僅 filter 內變更才觸發」一致。
- 註記（non-blocking）：run 有 GitHub 平台 deprecation 警告（Node 20 → 24、ubuntu-latest 未來遷移），不影響結果。

### 5.6 Smoke workflow（AC-22、AB-17）
- **本機同一檢查（AC-22「本機執行同一檢查亦成功」）**：`python smoke.py <preview> --timeout 90 --interval 5` →
  `GET / -> 200  GET /api/health -> 200`、`SMOKE PASS`、exit 0（1.3s；preview alias
  `aiot-hw01-weather-git-homework01-hw10-im-8efc12-nchu-aiot-class.vercel.app`，公開不需登入）。
- **`workflow_dispatch` 實際執行——BLOCKED（見 §9）**：GitHub 規定 `workflow_dispatch` 的 workflow **必須存在於預設分支**
  才可 dispatch。`home_work_01-smoke.yml` 目前只在 topic branch，`main`（預設分支）無 `.github/workflows/`，故
  `gh workflow run home_work_01-smoke.yml --ref home_work_01-hw10-implementation -f url=<preview>` 回
  `HTTP 404: workflow home_work_01-smoke.yml not found on the default branch`；`gh workflow list` 也未列出它
  （相對地 `home_work_01-ci.yml` 因 push/PR 觸發已註冊）。把它放上 `main` 需合併＝**RB-1（acceptor）**。
  URL 可用（本機 smoke 已 PASS），blocker 純為「dispatch 需預設分支」的平台限制，其唯一解為 RB-1，非 Executor 可控。

## 6. CI / smoke workflow 執行證據

| 項目 | 結果 | Evidence |
| --- | --- | --- |
| CI push run（AC-20：3.12、各類測試收集且通過、憑證檢查通過） | **success** | run `35925410250`（`84060c9`）：Python 3.12.14、152 passed（六類齊全）、credential scan passed；§5.5 |
| CI pull_request run（R-TC-6 MAY） | 觸發並執行 | run `35925413146`（同 push） |
| Smoke `workflow_dispatch`（AC-22：兩狀態碼） | **BLOCKED**（workflow 需在預設分支；RB-1） | 本機同一檢查 PASS（`GET /`＝200、`/api/health`＝200，exit 0）；§5.6、§9 |

## 7. AC / requirement 對照

| 項目 | 結果 | Evidence |
| --- | --- | --- |
| AC-20（含本單元變更 push → CI 成功；3.12；各類測試；不含變更不觸發＝path filter config） | **PASS**（run `35925410250` success）；negative 以 config（§3） | §5.5、§6 |
| AC-21（R-TC-1/3/4 每項；無網路無 `.env` 通過） | **PASS**（CI 152 passed，六類齊全） | §5.1、§5.5 |
| AC-22（`workflow_dispatch` smoke 成功、記兩狀態碼；本機同檢查） | 本機同檢查 **PASS**（200/200）；`workflow_dispatch` 執行 **BLOCKED**（RB-1，acceptor，§9） | §5.6、§9 |
| AC-29（RB-5 §8.2 授權原文入 worklog；只在單元＋自身觸發；名稱識別單元） | PASS | §1、workflow `paths`／檔名 |
| AC-07(b) `git ls-files` 無 `.env` | PASS | §5.2、§5.3 |
| AC-07(c) 追蹤檔＋committed diff 無金鑰格式（排除 `.env`） | PASS（§3 allowlist；literal-real-key 0） | §5.2、§5.3 |
| AC-07(d) fixture＋原始 JSON 無 Authorization | PASS | §5.2；`tests/test_secrets.py` |
| R-TC-6（push 觸發、path 過濾、3.12；MAY pull_request） | PASS | CI workflow |
| R-TC-7（smoke `workflow_dispatch`、同一檢查、變數名文件化） | PASS | smoke workflow、README |
| R-TC-5（測試無網路無金鑰） | PASS | §5.1 |
| R-DOC-1（README 測試＋CI 段） | PASS | README CI 段 |
| INV-5（金鑰零外洩） | PASS | §5.3 |
| INV-8（Python 3.12 三處一致） | 本機 3.12.14；CI `3.12`；Vercel pin（#21） | §5.1、§6、CI workflow |

## 8. Audit status

Formal Ticket → independent audit **required**。本 worklog 的 verification 為 self-verification，**不**記為 audit PASS。
交派工者依 Bindings §3.5 派 Primary Reviewer（fresh context）作 R1；本票觸及 H-1，audit record 依 A-1 記錄金鑰核對。
受審 subject：branch `home_work_01-hw10-implementation`，commit **`84060c9`**（程式與 workflow）。本 worklog 之後的 `<c3>`
只更新 record-only path，不改受審 subject identity（Bindings §7、Orchestrator Contract §7 P7）。

## 9. Remaining work / concerns / required authority

- **AC-22 的 `workflow_dispatch` 實際執行 — BLOCKED，required authority = acceptor（RB-1）。** GitHub 規定
  `workflow_dispatch` 的 workflow 必須存在於**預設分支**才能 dispatch；`home_work_01-smoke.yml` 目前只在 topic branch，
  `main` 無 `.github/workflows/`，故 dispatch 回 `HTTP 404 ... not found on the default branch`（§5.6）。唯一解為把
  smoke workflow 放上 `main`＝**RB-1 合併**（acceptor 保留動作，且本就是 release gate）；**非 Executor 可控**，也不是
  N-13（不在控制範圍內）。已提供的最強證據：(a) 本機以 `smoke.py` 對 live preview 執行同一檢查 **PASS**（`GET /`＝200、
  `/api/health`＝200，exit 0）；(b) smoke workflow 的 URL 解析與檔案正確（沿用 smoke.py 原檔）。合併後在 `main` 上
  dispatch（可帶 `url` input，或用 production 變數）即完成 AC-22 的 live 執行——與 DR-12「production 變數的 live 確認屬
  release／#25」同一 disposition。**其餘 AC（AC-20、AC-21、AC-29、AC-07 自動化）已在 CI 完成，不受此 block 影響。**
- **AC-07(c)／A-5 example allowlist（§3）**：本票唯一實質解讀，已附 literal-real-key self-verification 佐證不弱化。
  提請 Reviewer／DA 檢視是否認可此機制；若要求改為別種實作，屬契約內 targeted correction。
- **reserved boundary**：只在 §2 授權範圍內動 root（兩 workflow 檔，RB-5 §8.2）；未合併（RB-1）、未設 repository variable
  （RB-3，acceptor）、未付費（RB-4）、未動其他單元或其他 root 檔案。
- **狀態**：**DONE_WITH_CONCERNS** — 契約內可做的部分完成並經 CI 驗證；唯 AC-22 的 live `workflow_dispatch` 執行待 RB-1
  （acceptor）。

## 10. Change log（本 worklog）

| 時間 | 事件 |
| --- | --- |
| 2026-09-24 | `d854218`：CI＋smoke workflow、`tools/credential_scan.py`、smoke.py N-2 bound、README CI 段、worklog；本機 152 passed、scanner exit 0、literal-real-key 掃描 clean、smoke budget 實測。 |
| 2026-09-24 | `84060c9`：CI workflow YAML fix（step name colon-space 加引號）。push run `35925410250` **success**：Python 3.12.14、152 passed（六類齊全）、credential scan passed（465 tracked）；pull_request run `35925413146` 亦觸發。 |
| 2026-09-24 | 本機 smoke 對 live preview PASS（200/200）；`workflow_dispatch` dispatch 回 404「not found on the default branch」→ AC-22 live 執行 BLOCKED（RB-1，acceptor，§9）。`<c3>`：本 worklog 更新（record-only）。 |
