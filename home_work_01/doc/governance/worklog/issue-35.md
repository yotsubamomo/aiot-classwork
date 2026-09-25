# Worklog — Issue #35 伺服器端 Latest Observation 路徑：`/api/` 觀測回應、四類失敗分類與安全邊界 re-scope

- **Work item**：GitHub Issue #35（Formal lane，V2 Core；SPEC-V2 的第一張 Ticket，Blocked by：無）
- **Executing role**：`executor`，以 `gov-executor` definition 派工（Bindings §3.1 mapping：`claude-opus-5-5`，effort `high`）。本 session 自述的模型為 Opus 5.5（`claude-opus-5-5`）；**這不是 binding 證據**。Binding verification 依 Bindings §3.4 由派工者（Orchestrator）從 harness 紀錄（`subagents/agent-<id>.meta.json` 的 `agentType`、`.jsonl` 的 `message.model`／`effort`）核對並記入 run record 或 audit record；本 worklog 不複製 harness 日誌。
- **Branch**：`home_work_01-v2-implementation`；BASE ＝ `08e158e`（branch 起點為 run record commit `305dd1c`，record-only）
- **Subject**：cycle 1 初版 code anchor ＝ `bbc1d56`（R1 受審）；**cycle 1 targeted correction（F-1）後的 code anchor ＝ `5f0dbc3`**（`observation.py`、`tests/test_observation.py`、README）。本 worklog 的更新皆為其後的 record-only commit（`doc/governance/**`，Bindings §7 P7）
- **開始／本次更新**：2026-09-26（初版）；2026-09-26（cycle 1 targeted correction F-1，見文末「Cycle 1 targeted correction」）

## Contract reference

- **Outcome Contract**：`home_work_01/doc/governance/outcome-contract-v2.md`（ACCEPTED 2026-09-25；normative candidate `69c5a04`）——特別是 §2.6 C-1／C-3、§4 **A-3**（實作期金鑰使用）、**A-4**（workflow 窄授權；本票未使用）。
- **Spec**：`home_work_01/doc/spec/SPEC-V2.md` **v2.2**（以參照繼承 V1 Spec v1.1）——§2.2 R-V2-OBS-1～6、9、11～13；§2.4 R-V2-SEC-1～7；§2.5 R-V2-DEG-5；§2.9 R-V2-TC-1～3、R-V2-ENV-2；R-V2-DOC-1(6)(7)、R-V2-DOC-6；§5.1 契約固定、§5.3 儀器（有界時間 30 秒、上游逾時建議 ≤ 10 秒、重用視窗 ≤ 10 分鐘）。
- **Derivation record**：`home_work_01/doc/governance/decisions/derivation-SPEC-V2.md` DV-2～DV-7、DV-15、DV-19、B-13、B-18、§6（H-1／H-2／H-3 的 V2 適用；A-1）、§11 #1（Vercel 時限實作期驗證）、§15（本票分配）。
- **High-risk decision**：`home_work_01/doc/governance/decisions/decision-20260923-high-risk-categories.md`（A-1：R1 record 須有明記核對段；下方「High-risk 核對材料」提供 R1 可核對的入口）。
- **Ticket 分配（#35）**：AC-V2-03（離線／API）、04（API）、05、06（API）、07（觀測路徑）、16（靜態＋封網）、17(a)(b)(d)、20（本票範圍）；R-V2-TC-2、TC-3；README R-V2-DOC-1 (6) 本機部分、(7)。INV-V2-1、2、4、6（伺服器面）、8。§6.3 定向 V1 重驗：AC-04（re-scope）、AC-07(b)(c)(d)(f) 與 (e) supersede、AC-16（API 面）。
- **契約變更**：無。未修改任何 requirement、AC、invariant、gate、oracle。

## Decisions and assumptions（HOW；Spec §5.2 委派）

1. **模組結構**：新增 `home_work_01/observation.py` 為部署 Dashboard 後端唯一的 CWA 存取（R-V2-SEC-2(a)）；`server.py` 只註冊 route、建立 service；`weather_query.py`、`app.py` 不 import 它（靜態 closure 檢查證明）。
2. **Endpoint 路徑與欄位名**（HOW，README 文件化）：`GET /api/observations/latest`。成功 200：`dataset`、`observationTime`、`fetchedTime`、`validStationCount`、`receivedStationCount`（診斷用總數，R-V2-OBS-2 MAY）、`stations[]`（`stationId`、`stationName`、`countyName`、`townName`、`latitude`、`longitude`、`observationTime`、`airTemperature`、可選 `relativeHumidity`、`windSpeed`、`windDirection`、`airPressure`、`precipitation`（`WeatherElement.Now.Precipitation`）、`weather`）。
3. **失敗 HTTP 狀態碼**（HOW；契約只要求非 2xx）：`key_not_configured` 503、`upstream_unreachable` 504、`upstream_error` 502（附 `upstreamStatus` 數字，DV-6 MAY）、`invalid_response` 502。`error` 為每類固定句，不插入任何上游內容。
4. **「如發布」的數值表示**：以 `Decimal` 解析發布字串；整數字串保持 int（如 `82`）、小數字串轉為同位數 float（如 `259.0`、`25.5`），不四捨五入、不換單位。`ObsTime` 字串原樣回傳；比較最大值時才解析為時刻；無時區的 `ObsTime` 只在比較時視為 `+08:00`（CWA 發布時區）。同一時刻的平手保留第一個出現者的發布字串（確定性）。
5. **有效 `ObsTime`**：須符合 `YYYY-MM-DD[T ]HH:MM` 開頭且 `datetime.fromisoformat` 可解析（R-V2-OBS-2(e)「至少含日期與時、分」）；只有日期（`2026-09-25`）視為無效。
6. **哨兵集合**：~~同一集合（`X`、`-99`、`-98`、`T`、`990`）套用於全部可選欄位與座標~~——**此決定是錯的，已於 cycle 1 依 R1 F-1 更正（`5f0dbc3`）**：改為依資料標準 V1.05（BRIEF-V2 §3.2）逐欄位套用——`X`／`-99` 適用全部欄位（含 WGS84 座標）；`T`（雨跡）／`-98`（連續無降水）只適用 `precipitation`；`990`（風向不定）只適用 `windDirection`；R-V2-OBS-2(b) 對氣溫有效性明列整個集合。文字比對＋數值比對（`-99.0` 亦為哨兵）。常數 `FIELD_SENTINELS`，建構子 `field_sentinels=` 可設定（R-V2-OBS-2(b)「可設定、有文件」），README 以表格列出每個代碼適用的欄位。
7. **結構驗證**：`success` 必須逐字為 `"true"`（布林 `true` 亦歸 `invalid_response`，依 R-V2-OBS-11 字面）；`result.resource_id` 必須為 `O-A0001-001`；`records.Station` 必須為 list。單筆測站結構不符只使該站無效，不使整體失敗。
8. **有界時間**：connect 3 秒、read 5 秒，另以 worker thread＋`join(8 s)` 給整個上游交換一個總上限 8 秒——單靠 `requests` 的 read timeout 無法限制「慢速滴流」回應的總時間。逾時的結果被丟棄、永不進入快取。8 秒低於 Vercel 最低的預設 function 時限（10 秒）；`vercel.json` 未修改（見 Remaining work 1）。
9. **重用視窗**：300 秒（≤ 600 秒契約上限；建構子拒絕 > 600）；只快取成功；視窗以同一個可注入 clock 量測，clock 倒退視為過期；記憶體內、無持久狀態。回應一律 `Cache-Control: no-store`，避免 CDN 在伺服器視窗之外再重用。
10. **Log**：只記 reason 與數字狀態碼；永不記錄例外訊息（`requests` 例外字串可能含 URL）。**`urllib3` logger 設為 ERROR**：sentinel 測試在 root logger 為 DEBUG 時抓到 urllib3 自身會記錄 `Starting new HTTPS connection (1): opendata.cwa.gov.tw:443`（成功時還會記錄請求行），違反 R-V2-SEC-7「任何路徑不記上游 URL」；此設定使任何 logging 組態下都不會出現。
11. **本機 `.env` 載入**：`observation.load_local_env()` 只在 `python server.py` 的 `__main__` 呼叫，只讀單元目錄的 `.env`、只取 `CWA_API_KEY`、不覆寫既有環境變數、不印出。部署函式（`api/index.py`）不呼叫它；金鑰於每次請求時從 `os.environ` 讀取，不存於 service 物件。
12. **22 縣集合**：在 `observation.py` 明列，並以測試核對等於 `ingestion.config.REGION_MEMBERS` 的 19 縣 ∪ 澎湖縣、金門縣、連江縣（避免部署 runtime 依賴 ingestion 套件）。
13. **靜態檢查 re-scope（R-V2-SEC-4，DV-15，只加不減）**：(a′) 集合改為 `app.py`、`weather_query.py` 與其**以 import graph 計算**的單元內 closure（目前 closure ＝ 兩檔本身）；新增 closure 解析的探針測試（直接、package、相對 import 皆被納入，`import requests` 在 helper 模組仍被抓到）。(b) 延伸：first-party 前端（`index.html`、`app.js`、`styles.css`、`data/basemap.js`）的所有請求形式字面目標只得為 `/api/` 或 `/static/`，另有十個外部目標探針；vendored Leaflet 維持既有絕對 URL 白名單檢查（其內部 `.src =` 用變數）。(c) `observation.py` 加入 no-SQL／no-`sqlite3` 集合。(d) 不變。被移除的只有集合定義行與註解（見 Verification V-7）。
14. **README 既有敘述**：本票只修正與本次變更直接矛盾、且位於本票 README 段落相鄰的句子（「backend imports no HTTP client」「no environment variable or secret is needed at runtime」、測試段的靜態檢查描述），改為限定於預報路徑。部署段（「Vercel function needs no environment variable」等）屬 R-V2-DOC-1(6) Vercel 部分與 (11)，留給 #41。
15. **樣本（A-3、R-V2-TC-2）**：一次唯讀 GET 擷取、**未縮減**（876 筆，只重新序列化為 compact JSON，879 KB）；寫入前以 `ingestion.checks.scan_text`（含金鑰字面比對）確認無金鑰、無 `Authorization`。全部衍生反例在測試內由樣本衍生。

## Artifacts（初版 code anchor `bbc1d56`；F-1 更正見文末；BASE `08e158e`）

| 檔案 | 動作 |
| --- | --- |
| `home_work_01/observation.py` | 新增：Latest Observation service、正規化、四類失敗、有界 fetch、重用視窗、本機 `.env` 載入 |
| `home_work_01/server.py` | 修改：`create_app(..., observation_service=None)`；`GET /api/observations/latest`；`__main__` 載入 `.env`；docstring 更正 |
| `home_work_01/api/index.py` | 修改：只改 docstring（不再宣稱後端不讀環境變數） |
| `home_work_01/tests/test_observation.py` | 新增：41 個測試函式，參數化展開後 106 項 |
| `home_work_01/tests/fixtures/O-A0001-001_sample.json` | 新增：消毒真實樣本（擷取 2026-09-26 00:04:56 +08:00；`ObsTime` 2026-09-25T23:00:00+08:00；876 筆；849 筆有效） |
| `home_work_01/tests/test_static_checks.py` | 修改：R-V2-SEC-4 re-scope（見決定 13） |
| `home_work_01/tests/test_secrets.py` | 修改：樣本加入 artifact 掃描；V2 後端程式憑證掃描；CI 掃描清單含樣本的守衛 |
| `home_work_01/tools/credential_scan.py` | 修改：`_AUTH_ARTIFACTS` 加入樣本 |
| `home_work_01/README.md` | 修改：新增「Latest Observation endpoint (V2 Core)」段落；測試段與 endpoint 段的矛盾句更正 |

未修改：`app.py`、`weather_query.py`、`ingestion/**`、`data.db`、`static/**`、`smoke.py`、`vercel.json`、`requirements.txt`、`.github/workflows/**`、`CONTEXT.md`、`doc/requirement/**`；單元目錄外無變更（RB-5）。

## Verification

環境：Windows 11，`home_work_01/.venv` Python 3.12.14（與 CI 3.12 一致），requests 2.32.3／urllib3 2.8.0。以下「subject」皆指 working tree ＝ `bbc1d56`。

- **V-1 V1 基準（BASE 狀態）**：`305dd1c`（＝BASE＋record-only）`python -m pytest -q` → **259 passed**。
- **V-2 全套（subject）**：`python -m pytest -q` → **385 passed**（259 V1 ＋ 126 新增：`test_observation.py` 106 項、`test_static_checks.py` 23 → 37（＋14）、`test_secrets.py` 4 → 10（＋6））。全離線：唯一的 socket 為 loopback（127.0.0.1）停滯／滴流／成功模擬伺服器；不讀 `.env`、不需金鑰。
- **V-3 CI 憑證掃描**：`python -m tools.credential_scan`（staged 後）→ `credential scan passed: 557 tracked files; no .env tracked (only .env.example); no CWA-key-format string in tracked files or committed history; no Authorization value in fixture/raw JSON.` exit 0。
- **V-4 金鑰字面比對**：以腳本讀 `.env`（不印出）比對 `git diff --cached` 全文（955,958 bytes）→ literal key present: **False**；`git ls-files` 無 `.env`（只有 `.env.example`）。
- **V-5 AC-V2-03（離線／API）**：`test_sample_normalises_to_hand_computed_stations` 對樣本手算六站（C0TB40 崇德 一般站；C0TC30 虎頭山 風速／風向 `-99` → `null`；C2I260 北坑 氣壓 `-99` → `null`；C0W240 九宮 金門縣；467990 馬祖 連江縣；C0AH70 松山 臺北市）全欄位相等；哨兵氣溫站 C0TC00、A0W080（澎湖）不在回應中；有效 849／收到 876；22 縣全部出現；回應無 `records`／`Station`／`WeatherElement`／`GeoInfo`／`ObsTime`／`Coordinates`／`success`／`result` 等鍵（遞迴檢查）。瀏覽器抽樣屬 #36，preview 抽樣屬 #41。
- **V-6 AC-V2-04（API）**：樣本 dataset-level Observation Time ＝ `2026-09-25T23:00:00+08:00`；衍生最大值測試；Fetched Time 以可控 clock 驗證值與格式（UTC clock 轉為 `+08:00`、秒精度）；預設 clock 格式檢查。
- **V-7 AC-V2-05 八個反例**（全部由樣本衍生）：(1) 氣溫 `-99`／`X`／空字串／`abc`／`-98`／`T`／`990`／`-99.0`／`NaN`／`inf`／缺欄位 → 只排除該站、其他站逐一相等；(2) 無 WGS84、`NaN`、`inf`、空字串、哨兵座標、無 `Coordinates` → 排除；(3) `台北市`、`東京都`、空、`None`、`臺北` → 排除；(4) 全部無效 → 502 `invalid_response`；(5) 刪一半 → 200，有效數等於獨立計算值；(6) 樣本真實同名站（大坑 C0T9E0／C0F970）與衍生同名 → 各自獨立；(7) `ObsTime` 缺、空、`not-a-time`、只有日期、非法日期、數字、`-99` → 排除且不計數；最新站改壞 → 最大值落回其餘有效站、其他站不變；無效站的 `ObsTime` 不影響最大值；(8) 全部 `ObsTime` 壞 → 502 `invalid_response`。
- **V-8 AC-V2-06（API）**：可控 clock：視窗內（299 s）同 body、同 Fetched Time、上游只呼叫 1 次；300 s 重新取得、Fetched Time 更新；視窗 0 每次重取；> 600 拒絕；視窗外失敗回分類失敗、不帶舊資料（INV-V2-6）；失敗不被快取；clock 倒退不延長重用。停滯與滴流 loopback 伺服器（read timeout 5 s、deadline 0.6 s）→ 504 `upstream_unreachable`，耗時 < 3 s；預設 deadline 8 s < 10 s、connect／read ≤ deadline。
- **V-9 AC-V2-07（觀測路徑）**：經 Flask test client，18 個案例（無金鑰、空白金鑰、ConnectionError 其訊息刻意含 URL 與哨兵金鑰、ConnectTimeout、ReadTimeout、非預期例外、401／403／429／500、非 JSON、非 UTF-8、`success:"false"`、`success:true`（布林）、錯誤 dataset id、缺 `records`、JSON 陣列、零有效）：狀態非 2xx、JSON 含 `reason`／`error`、`upstreamStatus` 只在 `upstream_error`、`Cache-Control: no-store`；回應本文、caplog（DEBUG）、stdout／stderr（capfd）皆**不含哨兵金鑰、`opendata.cwa.gov.tw`、上游本文標記、`Authorization`**。另：真實 `requests` 路徑在封網時（socket 被阻擋）→ 504 且同樣無洩漏；loopback 成功路徑在 DEBUG logging 下無 urllib3 紀錄、無主機位址。金鑰只以 `Authorization` 標頭送出、不在 URL／params。雷達路徑屬 #40。
- **V-10 AC-V2-16**：(a′)(b)(c)(d) 見決定 13，`tests/test_static_checks.py` 37 passed；封網（`socket.connect`／`connect_ex`／`create_connection`／`getaddrinfo` 皆拋錯）且無 `CWA_API_KEY`：`/api/health`、`/api/regions`、全部 `/api/regions/<r>/series`、`/api/days`、全部 `/api/days/<d>` 皆 200 且等於共用模組直接計算值（`test_forecast_endpoints_unchanged_air_gapped_and_keyless`），`/api/health` 鍵集合未變。**Byte-level 對照（scratchpad 腳本 `forecast_equivalence.py`，未提交）**：以 `git show 08e158e:home_work_01/server.py` 載入 V1 server，與 subject server 在封網、無金鑰下對 4 種 DB（正常、missing、empty、incomplete）× 19 個預報路徑（含未知 Region／日期的 404 與 `/`）比較 status＋body bytes＋Content-Type：**76 組，0 差異**。執行期 network log 屬 #36／#41。
- **V-11 AC-V2-17**：(a) V-3、V-4、樣本 `test_artifact_has_no_secret`；(b) 程式審查：`LatestObservationService.latest()` 每次請求讀 `env.get("CWA_API_KEY")`；`load_local_env` 只讀單元 `.env`；本機以 `.env` 執行（V-13）成功且終端無金鑰；(d) `test_no_key_in_process_env_is_key_not_configured`（503 `key_not_configured`）＋ V-10（預報路徑正常）。(c) preview 屬 #41。
- **V-12 AC-V2-20（本票範圍）／H-2**：`git diff --stat 08e158e -- app.py weather_query.py ingestion/ data.db static/ smoke.py vercel.json requirements.txt ../.github/workflows/` → 空；`data.db` blob `687586991ce3654e8b336b5b0a1616e98aa83a66` ＝ BASE blob。老師驗證 SQL（唯讀開啟）：SQL1 → 6 列（北部地區、中部地區、南部地區、東北部地區、東部地區、東南部地區）；SQL2（中部地區）→ 7 列（2026-09-24…2026-09-30）。V1 測試保留：以腳本比對 BASE 全部 V1 測試檔的 144 個 `test_*` 函式在 subject 皆存在（missing: []）；`git diff 08e158e -- tests/ tools/` 的刪除行只有 `_PYTHON_SIDE`／`_NON_SHARED_PYTHON` 定義、其註解、一行區段標題與兩處 docstring 文字，無斷言被刪除。
- **V-13 A-3 定向即時驗證（本機，README 步驟實跑）**：scratchpad 腳本 `live_local_check.py` 以 `python server.py` 啟動（子行程環境先移除 `CWA_API_KEY`，金鑰只能來自單元 `.env`），請求 `/api/observations/latest` 兩次與 `/api/health` 一次後終止：第一次 200（0.17 s；`observationTime` 2026-09-26T00:00:00+08:00、`fetchedTime` 2026-09-26T00:27:19+08:00、有效 848／876、`Cache-Control: no-store`），第二次重用（body 相同、同 Fetched Time），health 200；無上游結構鍵。終端 log 10 行（Flask 啟動訊息與 werkzeug 請求行，只含路徑）；終端輸出與回應中金鑰字面 **False**、金鑰格式 **False**、`opendata.cwa.gov.tw` **False**。
- **V-14 自我驗證：mutation checks**（暫時修改 `observation.py`、跑 `test_observation.py`、還原並以 `cmp` 確認；非正式 audit）：移除數值哨兵比對 → 4 失敗；`ObsTime` 不必要 → 8；不檢查縣 → 5；永遠重用 → 4；失敗時回舊資料 → 1；log 例外內容 → 4；恢復 urllib3 logging → 2；最大值改最小值 → 2；忽略上游狀態碼 → 5；deadline ×20 → 2（停滯測試逾時）；完全移除 deadline → 滴流測試卡住（以此確認 deadline 是唯一界限）。移除「文字哨兵」分支時全數通過——該分支與 `Decimal`／數值比對重複，非測試缺口。
- **V-15 CI（R-V2-TC-3）**：push `9147997`（＝code anchor `bbc1d56`＋本 worklog）後，既有 workflow「home_work_01 CI」run `36161275690`（ubuntu，Python 3.12）**success**：`385 passed in 10.73s`；`credential scan passed: 558 tracked files …`。Workflow 檔未修改（A-4 未使用）。
- **未執行／限制**：瀏覽器、preview 部署、Vercel 時限實測皆不在本票（#36／#41）。

### A-3 金鑰使用紀錄

| # | 時間（+08:00） | 目的 | 動作 | 上游 GET 次數 | 輸出 |
| --- | --- | --- | --- | --- | --- |
| 1 | 2026-09-26 00:04:56 | (i) 擷取樣本 | scratchpad `capture_o_a0001.py`：讀 `.env`、一次唯讀 GET、`scan_text(key=...)` 確認乾淨後寫入 fixture | 1 | 只印 status 200、bytes 880,378、findings []、resource_id |
| 2 | 2026-09-26 00:27:19 | (ii) 本機定向驗證 | V-13 | 1（第二次請求為重用，未呼叫上游） | 只印布林檢查與非機密摘要 |

無輪詢、無壓測、未印出或匯出金鑰；未觸及 Vercel（RB-3）；CI 與自動化測試不依賴金鑰或網路。scratchpad 腳本與 log 不在 repo。

## High-risk 核對材料（供 R1 依 decision A-1 明記核對段）

- **H-1 憑證**：金鑰位置——程式只讀 process env `CWA_API_KEY`（`observation.py` `LatestObservationService.latest`）；本機來源只有單元 `.env`（`load_local_env`，只在 `server.py` `__main__`）；部署來源為 Vercel 專案環境變數（本票未觸及）。零外洩證據：V-3、V-4、V-9（回應／log／stdout／stderr，含哨兵金鑰與刻意含金鑰的例外訊息）、V-11、V-13；樣本與 V2 程式在 `test_secrets.py` 與 `tools/credential_scan.py` 範圍內。可核對點：`_FAILURES` 為固定文字；`except requests.RequestException: raise ... from None`；log 格式只含 reason／status；`urllib3` logger 為 ERROR。
- **H-2 老師指定介面**：V-12（`app.py`、`weather_query.py`、`ingestion/**`、`data.db` 與 BASE 無差異、blob 相同、兩句 SQL 6／7 列）；V-10（預報 endpoint 與 `/api/health` byte 相同、封網無金鑰）。頁面與前端未動。
- **H-3 語義與標示**：觀測值「如發布」（決定 4；`test_values_are_as_published_not_rounded`；**F-1 更正後**：只對欄位適用的代碼視為哨兵，真實 `990.0` 氣壓／雨量原樣回傳——`test_real_990_air_pressure_is_kept_as_published`、`test_sentinel_applies_only_to_its_fields`、手算站 `C0F9I0`；V-17 全樣本獨立 oracle 0 差異）；`ObsTime` 不正規化；哨兵永不成為數值（`test_every_station_has_the_contract_fields`、`test_per_field_sentinel_sets`、`test_parse_published_number_generic_codes`、反例 (1)）；伺服器回應無任何聚合值（無縣平均；`stations` 只有逐站值）。README 段落標示觀測值為 CWA 測站觀測（如發布）、Fetched Time 不是預報快照取得時間。UI 標示屬 #36～#38。

## Audit status

- **Required**（Formal；Bindings §5）：Ticket independent audit。
- **Cycle 1 R1**：`home_work_01/doc/governance/audit/issue-35-c1-r1.md`（Reviewer 自寫；本 Executor 未修改）——**BLOCKING**：F-1（Medium，H-3，blocking）；non-blocking：F-2（Medium，owner #37／#41）、F-3（Low，不需處理）、F-4（Low，owner #41）。
- **F-1 targeted correction**：已完成於 `5f0dbc3`（見文末）；Executor 的「已修正」不是 closure，待 **R2 scoped closure review**。
- 本 worklog 中的 mutation checks、獨立 oracle 與測試皆為 Executor self-verification，不是 audit。
- Model diversity：Executor 與 Primary Reviewer 預設同為 `claude-opus-5-5` → audit record 應記 `diversity_lost`（Bindings §5；derivation record §6 A-7）。

## Remaining work

0. **R2**（Orchestrator 派 `gov-primary-reviewer`）：核對 F-1 closure 與回歸，subject `5f0dbc3`。

1. **Vercel function 時限實測**（derivation record §11 #1；DA 為 authority）：本票以 8 秒總上限假設平台最低預設時限 10 秒，`vercel.json`（legacy `builds`）未設 `maxDuration`。部署上的實際時限與「上游停滯 → 分類 JSON 而非平台 gateway 頁」需在 preview 驗證（#41，acceptor 填入 Vercel 金鑰後）；若平台時限低於假設，route DA（§5.3 儀器調整，不改語義）。
2. **README 部署段**（R-V2-DOC-1(6) Vercel 步驟、(11) 其餘矛盾敘述，例如「function needs no environment variable and no secret」）：#41。
3. **瀏覽器面**（AC-V2-03 抽樣、04 UI、06 UI、network log）：#36、#37；preview（AC-V2-03、17(c)、22）：#41。
4. 本票不需 workflow 變更（R-V2-TC-3；A-4 未使用）；新測試由既有 `home_work_01/**` 觸發的 CI 涵蓋。
5. Ticket 結案條件（治理 §3.8）：待 R1（與必要時 R2）audit closure；不由 Executor 關閉 Issue。

## Cycle 1 targeted correction — F-1（2026-09-26）

- **Finding**：R1 F-1（Medium，blocking，H-3）：`990` 被當成通用哨兵套用到全部可選數值欄位，使真實的 `AirPressure "990.0"`（樣本 `C0F9I0` 神岡、`CAF030` 國一S169K，皆臺中市約 195 m 海拔）回傳 `null`；測試 `test_observation.py:217-219`、`:844` 把錯誤行為固定。
- **契約依據（重讀）**：R-V2-OBS-2(b)（氣溫有效性：整個集合）、R-V2-OBS-3（可選欄位「有效為數值／文字，無效為 `null`」）、R-V2-OBS-6（缺值、哨兵或無效欄位 → 「—」）、R-V2-DD-7；BRIEF-V2 §3.2（DV-3 引用的哨兵事實）：`X` 儀器故障、`-99` 缺值／異常、`T` 雨跡、`-98` 連續無降水、`990` 風向不定。
- **歧義評估**：逐欄位對照後**沒有需要猜測的語義**，未 route DA：`X`／`-99` 的定義不限欄位 → 全部欄位；`T`、`-98` 的定義是降水語義 → 只 `precipitation`；`990` 是風向代碼 → 只 `windDirection`；氣溫有效性由 R-V2-OBS-2(b) 字面指定整個集合（`990`／`-98`／`T` 不是可能的氣溫值，不影響任何可用資料）；`weather` 文字與 WGS84 座標只適用通用代碼。`T`／`-98` 在 `precipitation` 仍回 `null`（顯示「—」）而不是換算為數值，依 R-V2-OBS-6「哨兵永不顯示為數值」。
- **改動（`5f0dbc3`）**：`observation.py`——`MISSING_CODES`、`PRECIPITATION_CODES`、`WIND_DIRECTION_CODES`、`SENTINELS`（氣溫用全集合）、`FIELD_SENTINELS`（逐欄位對應）；`normalize_station`／`normalize`／`LatestObservationService` 改用 `field_sentinels`（鍵不完整即 `ValueError`）；`parse_published_number`／`parse_published_text` 預設只用通用代碼。`tests/test_observation.py`——手算站加入 `C0F9I0`（`airPressure` 990.0）；`test_every_station_has_the_contract_fields` 改為逐欄位斷言；`test_parse_published_number` 改為 `test_parse_published_number_generic_codes`（`"990.0"` → 990.0、`"-98"` → -98）；新增 `test_per_field_sentinel_sets`、`test_field_sentinel_sets_match_the_data_standard`、`test_real_990_air_pressure_is_kept_as_published`、`test_sentinel_applies_only_to_its_fields`（13 個由樣本衍生的例子：`AirPressure`／`Precipitation` 的 `990`／`990.0` 保留，`WindDirection "990"`／`"990.0"`、`Precipitation "T"`／`"-98"`／`"-98.0"`、各欄位 `-99`／`X` → `null`，該站仍有效）、`test_field_sentinels_are_configurable`。README——「Sentinel codes, per field」表。未修改：`server.py`、`api/index.py`、樣本、`test_static_checks.py`、`test_secrets.py`、`tools/credential_scan.py`、任何 V1 產物。
- **F-2／F-3／F-4**：依派工指示不處理。F-2 與本 worklog Remaining work 1（Vercel 時限）相互影響：鎖在上游停滯期間序列化同一 instance 的並行請求，第 k 個請求約 8k 秒，故 #41 的 preview 驗證應同時量測並行停滯；本票未改鎖設計。

### Re-verification（subject ＝ `5f0dbc3`）

- **V-16 修正前後對照**：把 `observation.py` 暫時換回 `bbc1d56` 版本執行新測試（`-k "real_990 or hand_computed or only_to_its_fields"`）→ **5 failed**（手算站 C0F9I0、樣本 990.0 氣壓、`AirPressure 990`／`990.0`、`Precipitation 990.0`）；換回修正版 → 全數通過（`cmp` 確認還原）。
- **V-17 全樣本獨立 oracle**：另寫一個不引用 `observation.py` 正規化邏輯的逐欄位計算（只引用 `COUNTIES` 常數），對樣本 876 筆計算期望：有效 849 筆、ID 集合相同、**所有欄位值與型別 0 差異**（含 `C0F9I0`／`CAF030` 的 `airPressure` 990.0）。
- **V-18 全套**：`python -m pytest -q` → **424 passed**（385 ＋ 39：`test_observation.py` 106 → 145）。
- **V-19 H-1 回歸**：四類失敗、封網真實 client、loopback 成功路徑的 leak 測試（哨兵金鑰、root DEBUG logging、capfd 擷取 stdout／stderr；斷言回應、log、輸出無金鑰、`opendata.cwa.gov.tw`、上游本文標記、`Authorization`）→ 相關子集 30 passed（含於 V-18）；`tools.credential_scan` → `credential scan passed: 558 tracked files …`；staged diff 的金鑰字面比對 **False**。本次未使用真實金鑰、未呼叫 CWA（A-3 使用紀錄仍為兩次）。
- **V-20 H-2／INV-V2-1／4／8 回歸**：`git diff --stat 08e158e -- app.py weather_query.py ingestion/ data.db static/ smoke.py vercel.json requirements.txt ../.github/workflows/` → 空；`data.db` blob `687586991ce3654e8b336b5b0a1616e98aa83a66`；老師 SQL 6／7 列；BASE `server.py` 對 subject 在封網無金鑰下 4 DB × 19 路徑 **76 組 byte 相同、0 差異**；無金鑰觀測路徑 503 `key_not_configured`。
- **V-21 INV-V2-6**：重用／失敗不快取／視窗外失敗不帶舊資料的測試未變且通過（含於 V-18）。
- **V-22 AC-V2-05**：八個反例測試未變且通過，仍全部由提交的樣本衍生（`tests/fixtures/O-A0001-001_sample.json` 未改）。
- **V-23 靜態檢查 re-scope 仍只加不減**：`git diff c9c9ec5 -- tests/test_static_checks.py tests/test_secrets.py tools/credential_scan.py` → 0 行（與 R1 受審版本相同）；BASE 的 144 個 V1 測試函式全部存在；`test_static_checks.py`＋`test_secrets.py` 47 passed。
- **V-24 CI**：push 後的 workflow 結果記於下一次 worklog 更新（本段 commit 前尚未產生）。
- **過程紀錄（可驗證事實）**：re-verification 時一個指令誤執行 `git stash -u`，暫時收起了未提交的修正與 Reviewer 未追蹤的 audit record；立即以 `git stash pop` 完整還原（stash 內容 4 檔：README、`observation.py`、`test_observation.py`、`issue-35-c1-r1.md`；還原後 audit record 仍為未追蹤、內容未被 Executor 修改），並在還原後的樹上重跑 V-18、V-20、V-23（上列結果皆為還原後的數據）。

