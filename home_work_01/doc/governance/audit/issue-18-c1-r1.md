# Audit record — Issue #18，cycle 1，R1

| 欄位 | 內容 |
| --- | --- |
| Work Contract | GitHub Issue #18（`yotsubamomo/aiot-classwork`）「Ingestion：從 F-D0047-091 推導六 Region × 七 Forecast Day 的 Forecast Snapshot 並持久化到 data.db」，Scope class MVM；所屬 Spec `home_work_01/doc/spec/SPEC.md` v1.1（EFFECTIVE）；Outcome Contract `home_work_01/doc/governance/outcome-contract.md`（ACCEPTED 2026-09-23）；裁決 `decision-20260923-spec-interpretation-rulings.md` DR-3/4/5/6/10/15/16、`decision-20260923-high-risk-categories.md`（H-1/H-2/H-3，A-1、A-5） |
| 受審 subject | branch `home_work_01-hw10-implementation`，commit `693c12b5e282d3c30a0c14d3c1c478c00f417c79`；BASE `d42b1a7`；審查範圍 `d42b1a7..693c12b`（22 個檔案，全部在 `home_work_01/` 內） |
| Audit 種類 | **R1**（full independent audit of accepted work scope），**cycle 1** |
| 角色 | `primary_reviewer`（definition `gov-primary-reviewer`；Bindings §3.1 mapping `claude-opus-5-5`／`xhigh`） |
| Binding 證據 | 由派工者（Orchestrator）依 Bindings §3.4 核對並記入 run record `home_work_01/doc/governance/run/run-20260924-hw01-formal.md`。Executor binding（同一 run record）：agent `af0c7aafb2f44c730` = `gov-executor`／`claude-opus-4-8`／`high`。Model diversity：Executor `claude-opus-4-8` 與 Primary Reviewer mapping `claude-opus-5-5` 不同模型，未記 `diversity_lost`。 |
| Independence（治理 §2.3） | (1) 以 fresh context 派工，未繼承 Executor 對話；worklog 與 Executor 敘述只當作待驗證主張。(2) Binding 見上列。(3) 自主取得：自行讀取 Ticket 本文（`gh issue view 18`）、Spec、裁決、上位契約、brief、CONTEXT、git 歷史與 diff、所有實作與測試檔，並自行執行測試與檢查。(4) 本紀錄由 Reviewer 以自己的 Write 工具寫入。 |
| 日期 | 2026-09-24 |

## 1. 審查方法與環境

- **Subject 識別**：`git rev-parse HEAD` = `693c12b5e282…`；`git diff 693c12b -- home_work_01` 為空（追蹤中的檔案與 commit 相同）；`git diff --cached` 為空。
- **離線執行**：以 `git archive 693c12b home_work_01` 匯出到 Reviewer scratchpad（匯出樹**沒有** `.env`），用單元 `.venv` 的 Python 3.12.14（requests 2.32.3、pytest 8.3.3、SQLite 3.53.1）執行；以 `sitecustomize` 讓 `socket.connect`／`getaddrinfo` 一律丟例外，並把 `HTTP(S)_PROXY` 指向無效位址，確保任何網路呼叫都會失敗。
- **`pytest -v -p no:cacheprovider`** → **38 passed in 0.58s**（無網路、無 `.env`）。
- **Reviewer 自寫的獨立檢查**（放在 scratchpad，不進 repo）：
  - 另寫一份獨立推導（依 R-DER-1～6，含 EndTime 長度判定段別），對 raw JSON 與 fixture 各算一次，並與提交的 `data.db` 比較。
  - 從 fixture 重新取出測試所列縣市值，逐項重算 AC-08 的手算期望值。
  - CLI 層 harness：對 AC-09 五個反例與 AC-11 各種 HTTP 失敗（mock `requests.get`，使用形狀像金鑰的假金鑰），逐一檢查結束碼、資料庫是否不變（列與中繼資料的雜湊）、輸出是否含金鑰。
  - 保留規則的邊界變體（18:00 起的擷取版面、第八日、兩個開頭不完整日、窗內缺段、「台／臺」）。
  - **Mutation probe**：在 scratchpad 的複本上做兩個 mutant，檢查測試能否偵測（見 F-1、F-2）。
  - A-5 金鑰掃描：在程序內讀取被忽略的 `home_work_01/.env` 取得字面金鑰（**只印出次數，不輸出任何金鑰內容**），並另用 CWA 金鑰格式（`CWA-` 加上 8-4-4-4-12 hex）掃描。

## 2. Acceptance criteria 逐條判定

| 項目 | 判定 | 證據 |
| --- | --- | --- |
| AC-05 | **PASS** | 提交的 `data.db`：`sqlite_master` 的 `TemperatureForecasts` SQL 與 `REQUIREMENTS.md` A.3 的 DDL 子字串逐字相同（去掉 `;`，比較結果 `True`）；`PRAGMA table_info` = id INTEGER pk、regionName TEXT、dataDate TEXT、mint REAL、maxt REAL；沒有索引；只有一張同名表。Reviewer 在提交的 `data.db` 上執行 `SELECT DISTINCT regionName FROM TemperatureForecasts;` 得到 6 列（北部、中部、南部、東北部、東部、東南部地區）；執行 `SELECT * FROM TemperatureForecasts WHERE regionName = '中部地區';` 得到 7 列，dataDate 為 2026-09-24…2026-09-30。測試資料庫：`test_persist.py:32`、`:52` 通過。 |
| AC-06 | **PASS**（證據精確度見 F-8） | `test_persist.py:73`（重跑兩次得到 42 列，沒有重複）。Reviewer 經 `pipeline.main --from-json` 對同一 fixture 跑兩次：42 列、0 個重複；再用**整份日期平移 +7 天的 fixture** 跑一次：42 列，日期全部是 10-01…10-07。 |
| AC-07(a) | **PASS**（證據形式見 F-9） | Worklog `issue-18.md:83-86` 記錄以 `.env` 金鑰實際取得一次，且不含金鑰值。提交的 raw JSON 結構是真實的 F-D0047-091 回應（`success:"true"`、`resource_id` F-D0047-091、22 縣市、15 個要素、每個溫度要素 15 期）。 |
| AC-07(b) | **PASS** | `git ls-files`：除了 `home_work_01/.env.example` 之外，沒有任何 `.env*`。 |
| AC-07(c) | **PASS**（附註見 F-7） | 對 `693c12b` 樹內 418 個追蹤檔案、`d42b1a7..693c12b` diff、`git log --all -p` 全部歷史、staged diff 與 unstaged diff 掃描：字面金鑰 0 筆、CWA 金鑰格式 0 筆。被忽略的 `.env` 已明確排除。 |
| AC-07(d) | **PASS** | fixture 與 `data/raw/F-D0047-091.json`：`Authorization` 子字串 0 筆，`"Authorization":"…"` 值 0 筆，字面金鑰與金鑰格式各 0 筆。`test_secrets.py:20` 通過。 |
| AC-08 | **部分 PASS／證據缺口（F-1）** | 42 筆、6 Region、7 個連續完整日（`test_derive.py:40`）。四個手算值（南部 09-24／09-29、中部 09-24／09-30）與花蓮單縣值經 Reviewer 從 fixture 重算：mins 27/27/25 → 26.3、26/26/25 → 25.7、25/25/24/25/25/25 → 24.8、25/25/24/24/24/24 → 24.3；maxs 相符，全部一致。獨立推導的 42 列與 `derive_snapshot` 的輸出、提交的 `data.db` 完全相同。**但「擷取開頭的不完整日期被丟棄」這一條沒有被任何測試實際執行**（F-1）。 |
| AC-09 | **行為 PASS／證據缺口（F-2）** | 五個反例在 derive 層都丟出指名的 `DeriveError`（`test_derive.py:106-150`）。Reviewer 的 CLI harness 逐一確認五個反例（外加 `X`、`-99`、`abc`）：結束碼 1、DB 雜湊不變、stderr 指名縣市、日期或問題。但在 pytest 中，只有「缺縣市」一例斷言了非零結束碼與不寫入（`test_pipeline.py:38-55`）。 |
| AC-11 | **行為 PASS／證據缺口（F-2）** | Reviewer 以 CLI harness 確認 401、404、500（HTML）、502、503、Timeout、ConnectTimeout、ConnectionError、200 非 JSON、`success=false`、錯誤的 `resource_id`：結束碼 1、DB 不變、stdout／stderr 不含（形狀像金鑰的）假金鑰、沒有寫出 raw JSON，錯誤訊息都含 HTTP 狀態或原因。pytest 只測到 `fetch_raw` 丟出 `FetchError`（`test_fetch.py:52-100`）。 |
| AC-24（資料面） | **PASS** | 提交的 `data.db` 有 `IngestionMetadata`：`(1, '2026-09-24T01:49:18+08:00', 'F-D0047-091')`，為 ISO 8601 且帶 +08:00；`TemperatureForecasts` 的 DDL 沒有變動（`test_persist.py:116`）。語義上的疑問見 §6 R-1。 |
| AC-25（產物） | **PASS** | raw JSON 的位元組與 `json.dumps(data, indent=2, ensure_ascii=False)` 完全相同（1,660,436 bytes，完整 15 個要素），不含金鑰。以 mock 走 online 路徑時，會印出取得摘要（22 縣市、15 個要素名、15 期）與 42 列預覽（含 Region 數與日期範圍），寫出的檔案與提交的 raw JSON 位元組相同。README 第 114–134 行說明檔案位置與 F-D0047-091 結構。 |
| R-ING-5／R-TC-5 | **PASS** | `--from-json` 可離線重建（`test_pipeline.py:29`）；在網路封鎖、沒有 `.env` 的情況下全部通過。 |
| R-ING-6（SHOULD） | **PASS** | `ingestion/fetch.py`、`derive.py`、`persist.py` 三階段清楚可辨；README 第 180–197 行有對應海報的表。 |
| R-ENV-1／R-ENV-2 | **PASS**（附註見 F-10） | `.venv` 為 3.12.14；`requirements.txt` 在單元目錄，版本固定；folium 沒有列為相依。diff 內 22 個檔案全部在 `home_work_01/`。 |
| README 本票段落 | **PASS**（附註見 F-11） | 取得金鑰、建立 `.env`、online／offline 指令、R-DOC-2 資料面標示（第 11–46 行），詳見 §3 H-3。 |
| INV-3 | **PASS** | 在單一 `with conn` 交易中 DELETE 後 INSERT 42 列並 upsert 中繼資料（`persist.py:67-81`）。Reviewer 在交易中途注入 KeyError：先前的快照雜湊不變。 |
| INV-4 | **PASS** | 見 AC-05；Region 名稱與順序（`config.py:27-37`）與 R-DER-5、R-SHR-2(b) 逐字相同；`dataDate` 為 `YYYY-MM-DD`；`data.db` 在單元根目錄。 |
| INV-5 | **PASS** | 見 §3 H-1。 |
| INV-7（資料面） | **PASS**（附註見 F-11） | 見 §3 H-3。 |
| INV-8 | **PASS（本機）** | 3.12.14；CI 與 Vercel 由後續票負責。 |
| AC-27（本票範圍） | **PASS**（Low 附註見 F-3、F-4、F-5） | (1) 每個模組都有說明目的的 docstring，主要函式也有；(2) FetchError／DeriveError 以明確訊息處理，另有少數邊緣路徑未攔截（F-3、F-4）；(3) 沒有未使用的 import 或相依，有一段自註為 unreachable 的防禦碼（F-5）；(4) 模組結構對應 fetch → derive → persist。 |

## 3. 高風險類別核對（decision-20260923-high-risk-categories A-1）

### H-1 憑證與機密 — 觸及（讀取 `.env`、發出 CWA 請求、保存回應、產生 fixture）

- **核對內容**：金鑰的讀取位置（`fetch.py:25-49` 只解析 `.env` 檔，不讀 process 環境變數）；傳遞方式（`fetch.py:65` 只放在 `Authorization` header，harness 斷言 URL 與 params 都不含金鑰）；所有錯誤訊息的構成（`fetch.py:70-87`、`:97-105`、`load_api_key` 的三種訊息）；有沒有 logging（沒有）；A-5 #1–#4 的機械檢查；evidence 檔（worklog、run record）、`data.db` 與 commit message 的字面金鑰與金鑰格式掃描。
- **結果**：全部 0 筆。11 種 HTTP 失敗模式與 online 成功路徑的輸出都不含假金鑰；raw JSON 由回應本體寫出，不含 header。Low 附註：F-6（`--env` 可指向其他路徑）、F-7（測試字面值符合寬鬆的金鑰 regex）。**H-1 本身沒有 blocking**；但 AC-11 的「輸出不含金鑰」目前沒有自動化證據，併入 F-2。

### H-2 老師指定的介面或資料格式 — 觸及（`data.db`、DDL、五欄、Region 名、dataDate）

- **核對內容**：`sqlite_master` 儲存的 DDL 與上位契約 `REQUIREMENTS.md` A.3 **逐字**比對；`PRAGMA table_info`；有無索引或同名表；在提交的 `data.db` 執行老師的兩句 SQL；六個 Region 的中文全名與順序；`dataDate` 格式；各欄 `typeof`（integer／text／text／real／real）；`data.db` 位於單元根目錄；中繼資料放在另一張表，沒有改動 `TemperatureForecasts`。
- **結果**：全部符合，見 AC-05、AC-24。**沒有 H-2 finding。**

### H-3 資料語義與標示 — 觸及（推導、驗證、fixture 期望值、標示）

- **核對內容**：
  - W1 分組（`derive.py:126-139`）：只用 06:00 與 18:00 起始的兩段。
  - 保留規則（`derive.py:142-171`），對照 DR-5 的六個變體：開頭只有夜間段 → 丟棄並得到相同的 42 列；第八個完整日 → 忽略；兩個開頭不完整日 → 失敗；窗內有一天缺段 → 失敗並指名日期；只剩六天 → 失敗；不連續 → 失敗。
  - 縣市日值取 min／max，兩段缺一即失敗且指名縣市與日期，不改變分母（DR-16）；「台」取代「臺」時失敗並指名縣市。
  - Region 對應表逐字對照 R-DER-5。
  - half-up：以 `Decimal` 做 `ROUND_HALF_UP`（`derive.py:226-231`），(20.1+25.2)/2 → 22.7、0.25 → 0.3、−0.25 → −0.3。
  - 以獨立推導重算全部 42 列，與提交的 `data.db` 完全相同。
  - 手算期望值由 Reviewer 重算，全部一致。
  - README 標示，逐項核對：F-A0010-001 為原指定且 2026-07-01 下架（第 17–20 行）；F-D0047-091 為相容性替代（第 21–23 行）；W1 視窗（第 24–29 行）；對應表為專案定義、非 CWA 權威分區（第 30–40、46 行）；`PROJECT-DERIVED COMPATIBILITY VALUES`、「never a CWA-issued six-region forecast」（第 41–46 行）。終端預覽標為「Derived Forecast Snapshot」。
- **結果**：推導與標示的**實作**符合 R-DER-1～8、DR-4、DR-5、DR-16。**Blocking：F-1**（保留規則的「丟棄開頭不完整日」分支沒有被測試執行，刪掉它 38 個測試仍全數通過）與 **F-2**（反例沒有逐一斷言不寫入與非零結束碼）。Low：F-3（`NaN`／`Infinity`）、F-11（README 第 3 行措辭）。

## 4. A-5 機械檢查（Reviewer 在本機獨立執行）

| # | 檢查 | 結果 |
| --- | --- | --- |
| 1 | `git ls-files` 不含 `.env` | 除 `home_work_01/.env.example` 外 0 筆 |
| 2 | 追蹤檔案（`693c12b` 樹，418 個）以字面金鑰與 CWA 金鑰格式搜尋；排除被忽略的 `home_work_01/.env` | 字面 0、格式 0（寬鬆 regex 只命中 `tests/test_secrets.py` 的測試字面值，見 F-7） |
| 3 | staged／committed diff：`git diff --cached`（空）、`git diff`（空）、`d42b1a7..693c12b`、`git log --all -p` | 字面 0、格式 0 |
| 4 | fixture 與保存的 raw JSON 不含 `Authorization` 值 | 兩個檔案都是 0 |
| 5 | `data.db` 的 DDL 與老師 DDL 比對 | 與 `REQUIREMENTS.md` A.3 逐字相同 |

## 5. Findings

### F-1 — AC-08「擷取開頭的不完整日期被丟棄」與 DR-5 丟棄分支沒有測試證據

- **Severity**：Medium　**Blocking**：**是**
- **契約依據**：AC-08 的 PASS 條件列有「擷取開頭的不完整日期被丟棄」，證據方式為 pytest；R-TC-1（derive 部分已分配給 #18）要求「pytest MUST 涵蓋 R-DER-1～R-DER-7」，其中 R-DER-3 包含丟棄規則；Spec §5.1 的「邊界優先：擷取開頭只有夜間段的日期」；H-3 風險描述為「保留規則被默默改變而測試仍綠」。
- **證據**：
  - 提交的 fixture 是 2026-09-24 凌晨的擷取，第一期是 `2026-09-24T00:00→06:00`，長 6 小時，接著才是 09-24 06:00…09-30 18:00。`_period_key`（`derive.py:126-139`）在推導視窗之前就濾掉這一段，所以 `global_segments` 裡第一天（09-24）已經完整。結果是 `derive.py:149-150` 的丟棄分支在整個測試套件中從未執行。
  - `test_derive.py:49-55`（`test_retains_seven_consecutive_days_dropping_leading_partial`）的斷言與 `:40-46` 相同，沒有構造「開頭只有夜間段」的日期。
  - **Mutation probe**：在 scratchpad 複本中刪除 `derive.py:149-150` 後執行 `pytest -q`，得到 **38 passed**。同一個 mutant 處理 brief §4.5 記錄的 18:00 起算版面時（第一天只有夜間段），會以 `forecast day 2026-09-23 is missing a 12-hour period` 失敗。也就是說，這條規則若退化，所有在 18:00–24:00 擷取的 ingestion 都會失敗，測試卻不會發現。
  - 現行實作是正確的：Reviewer 把開頭那段改標為 `2026-09-23T18:00` 後，得到的 42 列與原始結果相同。
- **需要的修正（不指定做法）**：補上實際執行丟棄分支的自動化證據，例如由真實 fixture 衍生「開頭只有夜間段」的版面，斷言該日被丟棄且結果為指定的七日。

### F-2 — AC-09 與 AC-11 的反例沒有逐一斷言「不寫入、非零結束碼」；AC-11 沒有斷言「輸出不含金鑰」

- **Severity**：Medium　**Blocking**：**是**
- **契約依據**：
  - AC-09：五個反例「各自失敗且**不寫入**資料庫、結束碼非零、訊息指名問題…既有快照在失敗後保持原狀」，證據為 pytest。
  - AC-11：HTTP 401／404／5xx／逾時／非 JSON 時要有「明確錯誤訊息、**非零結束碼、不寫資料庫、輸出不含金鑰**」，證據為 pytest（mock HTTP）；FAIL 例為「例外堆疊為唯一訊息」。
  - Spec §5.1：「反例必須斷言『沒有寫入資料庫』而不只是『拋出錯誤』」。
  - 涉及 H-1（輸出不含金鑰）與 H-3。
- **證據**：
  - AC-09：五個反例中只有「缺縣市」經 CLI 斷言 `exit == 1` 且快照不變（`test_pipeline.py:38-55`）；其餘四個只斷言 `DeriveError`（`test_derive.py:113-150`）。
  - AC-11：`test_fetch.py:52-100` 只斷言 `fetch_raw` 丟出 `FetchError` 與訊息內容。沒有任何測試經過 `pipeline.main` 或 `run_online` 驗證 FetchError 會轉成非零結束碼、不寫 DB、輸出不含金鑰。金鑰不外洩只在 401 一例、對例外字串斷言（`:96-100`）。
  - **Mutation probe**：在 scratchpad 複本中把 `pipeline.py:191` 改成只攔截 `DeriveError`（AC-11 的失敗因而變成 traceback，正是 FAIL 例）後執行 `pytest -q`，得到 **38 passed**。
  - 現行行為是正確的：Reviewer 的 CLI harness 對五個 AC-09 反例與 11 種 AC-11 失敗逐一確認結束碼 1、DB 雜湊不變、輸出不含假金鑰（見 §2）。
- **需要的修正（不指定做法）**：讓 AC-09 每個反例與 AC-11 每種失敗模式都有斷言「非零結束碼、既有快照不變」的自動化證據，AC-11 另須斷言輸出（stdout／stderr）不含金鑰。

### F-3 — `NaN`／`Infinity` 值觸發未攔截的 `decimal.InvalidOperation`，沒有產生指名縣市與日期的錯誤

- **Severity**：Low　**Blocking**：否
- **契約依據**：R-DER-4、DR-16 規定「無法解析」的值視為缺漏，須以指名縣市與日期的錯誤結束。
- **證據**：`Decimal("NaN")`、`Decimal("Infinity")` 可以解析（`derive.py:220-221`）。之後在 `min()`（NaN）或 `quantize`（Infinity）時丟出 `InvalidOperation`，`pipeline.main` 沒有攔截，結果是 traceback。harness 顯示結束碼非零，DB 不變。
- **Disposition**：仍然 fail-closed（不寫入、非零結束碼），而且這兩個值不在 CWA 已知的數值空間內。Owner：#18 Executor，可在本 cycle 的 targeted correction 順手處理；不處理也不影響 closure。

### F-4 — 少數錯誤路徑以 traceback 結束

- **Severity**：Low　**Blocking**：否
- **契約依據**：R-DOC-5「錯誤有處理與明確訊息」。
- **證據**：
  - `--from-json` 指向不存在或非 JSON 的檔案：`pipeline.py:135` 丟出 `FileNotFoundError` 或 `JSONDecodeError`，process 結束碼 1 並印出 traceback。
  - 200 回應但本體是 JSON 陣列：`fetch.py:95` 的 `data.get` 丟出 `AttributeError`。
  - 以上都不寫 DB，也不含金鑰。
- **Disposition**：不屬於 AC-11 列舉的失敗模式。Owner：#18 Executor（可選）；#25 做 AC-27 最終核對時再看。

### F-5 — 自註為 unreachable 的防禦碼

- **Severity**：Low　**Blocking**：否
- **契約依據**：R-DOC-5「無死碼」。
- **證據**：`derive.py:86-90`，註解寫明「the loops above make this unreachable」。
- **Disposition**：屬於防禦性斷言，無害。Owner：#18 Executor（可選）。

### F-6 — `--env PATH` 允許從唯一授權位置以外的路徑讀取金鑰

- **Severity**：Low　**Blocking**：否
- **契約依據**：R-ING-2「金鑰 MUST 只從單元目錄內未追蹤的 `.env` 讀取」；R-SEC-1「唯一授權位置」。
- **證據**：`pipeline.py:165-171` 與 README 第 105–107 行。預設值是 `home_work_01/.env`，所以不會造成外洩。
- **Disposition**：Owner：#18 Executor（可選，例如移除這個選項或限制在單元目錄內）；#25 做 INV-5 最終核對時再看。

### F-7 — 測試字面值符合 repo 自己的寬鬆金鑰 regex

- **Severity**：Low　**Blocking**：否
- **契約依據**：AC-07(c) 的 CI 自動化由 #22 負責。
- **證據**：`tests/test_secrets.py:28-29` 的 `CWA-1234-5678-90ab-cdef` 符合 `checks.py:15` 的 `KEY_PATTERN`，但不符合 CWA 的 8-4-4-4-12 格式（格式掃描 0 筆）。
- **Disposition**：Owner：#22。CI 掃描應使用精確格式或明確的 allowlist，否則可能誤報。

### F-8 — AC-06 的日期平移測試是平移已推導的列，不是平移 fixture 後重新 ingest

- **Severity**：Low　**Blocking**：否
- **契約依據**：AC-06「以日期平移後的第二份 fixture ingest」。
- **證據**：`test_persist.py:86-110` 在 persist 層直接替換。Reviewer 以平移 +7 天的 fixture 經 CLI 完整執行一次，確認整份被替換。
- **Disposition**：語義已由 Reviewer 驗證。Owner：#18 Executor（可選，可與 F-2 的補強一併處理）。

### F-9 — Worklog 沒有貼出終端輸出

- **Severity**：Low　**Blocking**：否
- **契約依據**：AC-25 的證據欄「worklog 貼終端輸出」。
- **證據**：`issue-18.md:83-86` 只用敘述說明取得摘要與 42 列預覽。Reviewer 已以 mock 的 online 路徑與 offline 路徑實際看到這兩段輸出。
- **Disposition**：Owner：#25（AC-25 其餘部分與 AC-12 實跑時貼上）。

### F-10 — `requirements.txt` 的註解含有字串「folium」

- **Severity**：Low　**Blocking**：否
- **契約依據**：R-ENV-1 已滿足（沒有列為相依）；AC-26（#19）要求「`requirements.txt` 不含 folium」。
- **證據**：`requirements.txt:4` 是註解。若 #19 的靜態檢查以子字串判斷，會誤判為 FAIL。
- **Disposition**：Owner：#19。檢查應判斷「是否列為相依」，或把該註解改寫。

### F-11 — README 第 3 行措辭可能讓人以為六區預報直接取自 CWA

- **Severity**：Low　**Blocking**：否
- **契約依據**：AC-14(8)、INV-7。
- **證據**：README 第 3 行「A one-week temperature forecast for six Taiwan Regions, taken from CWA open data」，緊接的第 11–46 行標示段已明確說明值由專案推導，所以不構成冒充。
- **Disposition**：Owner：#25（AC-14 文件審查時一併調整，例如改為「derived from CWA county-level open data」）。

## 6. Routing signals（非 blocking，不影響本 audit verdict）

- **R-1 → Design Authority**：offline `--from-json` 重建時，`IngestionMetadata.ingestedAt` 應該記哪個時間？
  - R-DB-5／DR-2 只說「ingestion 時間」，而 R-GA-8／R-DS-7 把它顯示為「最後更新時間」（user story 13：資料有多新）。
  - 實作記的是 derive→persist 的執行時間（`pipeline.py:138`）。提交的 `data.db` 是 offline 重建的，`ingestedAt` = `2026-09-24T01:49:18+08:00`，不是 raw JSON 的擷取時間。
  - online 路徑下兩者相同；若日後以舊 JSON 離線重建，顯示的時間會比資料實際擷取的時間新。
  - 契約沒有規定這一點，屬於語義不足，請 DA 決定。本票現有快照的時間差只有數分鐘，不影響本票判定。
- **觀察（不需 routing）**：真實擷取出現了 6 小時的 `00:00–06:00` 開頭期間，與 brief §4.5「期間只有兩種」的描述不同。依 Spec R-DER-2／R-DER-4 的「兩段」定義，這段不屬於任何 Forecast Day，結果可以確定；Reviewer 驗算過，即使把它併入 09-24，42 個值也不會改變。

## 7. 結論

實作行為符合 accepted contract：推導、持久化、DDL、老師 SQL、快照替換、中繼資料、金鑰零外洩與資料面標示都已由 Reviewer 獨立驗證。提交的 `data.db` 恰為 42 列、6 個 Region、7 天，並與獨立推導完全一致。

有兩項 blocking：F-1 與 F-2 都屬於 acceptance evidence 的缺口，而且都落在高風險類別（H-3，F-2 另涉及 H-1）。兩者都已用 mutation probe 證實：對應的退化發生時，現有 38 個測試仍全數通過。Targeted correction 只需補上對應的自動化證據，不需要改動設計。

Non-blocking findings F-3～F-11 的 owner 與 disposition 已分別記在各項之下。R-1 交 Design Authority。

VERDICT: BLOCKING (F-1, F-2)
