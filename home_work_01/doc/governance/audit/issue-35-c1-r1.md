# Audit record — Issue #35，cycle 1，R1（Formal Ticket independent audit）

| 欄位 | 內容 |
| --- | --- |
| Work Contract | GitHub Issue **#35**（`yotsubamomo/aiot-classwork`）「伺服器端 Latest Observation 路徑：`/api/` 觀測回應、四類失敗分類與安全邊界 re-scope」。上位：V2 Outcome Contract `home_work_01/doc/governance/outcome-contract-v2.md`（ACCEPTED 2026-09-25，normative candidate `69c5a04`；§4 A-3）；Delta Spec `home_work_01/doc/spec/SPEC-V2.md` **v2.2**（§2.2、§2.4、§2.5 R-V2-DEG-5、§2.9、§5.1、§5.3）；derivation record `derivation-SPEC-V2.md`（DV-2～DV-7、DV-15、DV-19、B-13、§6、§15）；`decision-20260923-high-risk-categories.md`（H-1／H-2／H-3、A-1、A-3）。本票分配：AC-V2-03、04、05、06（API 面）、07（觀測路徑）、16（靜態＋封網）、17(a)(b)(d)(e)、20（本票範圍）；R-V2-TC-2、TC-3；README R-V2-DOC-1 (6) 本機部分、(7)；INV-V2-1、2、4、6（伺服器面）、8；§6.3 定向 V1 重驗 AC-04、AC-07(b)(c)(d)(f)＋(e) supersede、AC-16（API 面）。 |
| 受審 subject | branch `home_work_01-v2-implementation`；BASE **`08e158e565785b56df63520a3f1307723f76b623`** .. HEAD **`c9c9ec5c66330d78231474edf2531bea11790aba`**（＝`git ls-remote origin`）；code anchor **`bbc1d56a9abaaca69733ce57805117a611b783e6`**。`git diff --stat bbc1d56..c9c9ec5` 只有 `home_work_01/doc/governance/worklog/issue-35.md`（record-only，Bindings §7）。`08e158e..bbc1d56` 的 10 檔：`observation.py`（A）、`server.py`、`api/index.py`（docstring）、`tests/test_observation.py`（A）、`tests/fixtures/O-A0001-001_sample.json`（A）、`tests/test_static_checks.py`、`tests/test_secrets.py`、`tools/credential_scan.py`、`README.md`、run record（record-only）。單元目錄外無變更。 |
| Audit 種類 | **R1**（Formal 必做的 Ticket independent audit；治理 §4.1、§4.4），**cycle 1**。不是 Spec Integration Audit。 |
| 角色 | `primary_reviewer`（definition `gov-primary-reviewer`；Bindings §3.1 mapping `claude-opus-5-5`／`xhigh`） |
| Binding 證據 | 正式核對由派工者（Orchestrator）依 Bindings §3.4 記入 run record `home_work_01/doc/governance/run/run-20260925-hw01-v2-formal.md`。Reviewer 另以 Bindings §3.4 的指令讀 harness 紀錄（session `05b8408b-260a-46d3-a4fe-ec07e3ec365a`）自行觀察到：`agent-ab39e3a58cdb76117` `gov-primary-reviewer` `[('claude-opus-5-5', 'xhigh')]`（本 Reviewer）；`agent-a1eef729c5e6bcebf` `gov-executor` `[('claude-opus-5-5', 'high')]`（#35 Executor）。兩者皆與 Bindings §3.1（b2 override）一致。此觀察只供對照，不取代派工者的核對。 |
| Independence（治理 §2.3、§4.6） | (1) **Fresh context**：未繼承 Executor 對話；worklog `issue-35.md` 與 commit message 的敘述一律當作待驗證主張，本紀錄的每項結論都來自 Reviewer 自己的讀取、測試或 probe。(2) **Binding**：見上一列。(3) **Autonomous access**：自讀 Issue #35（`gh issue view 35`）、SPEC-V2、OC-V2、derivation record、decision A-1、BRIEF-V2、V1 SPEC、git 歷史與 diff、CI run 與 log；以 `git archive` 匯出 BASE 與 code anchor 到 Reviewer scratchpad；自寫 probe（`dump_forecast.py`、`probe_failures.py`、`probe_semantics.py`、`independent_norm.py`、`run_server_main.py`＋`client.py`、`probe_default_deadline.py`，皆在 scratchpad，未提交）。(4) **Self-written record**：本紀錄由 Reviewer 以自己的 Write 工具寫入。**Model diversity：`diversity_lost`**——Executor 與 Primary Reviewer 同為 `claude-opus-5-5`（Bindings §5、b2 override；decision A-7）。這是合法狀態，不是缺陷，也不構成 independence 的減損（diversity 是偏好，不是 §2.3 的 independence）。 |
| 日期 | 2026-09-26 |

## 1. 審查方法與環境

- **Subject 確認**：`git status --short` 只有 run record（`doc/governance/**`，派工者的 record-only 修改）與一個無關的 `grep.exe.stackdump`；code 檔案的 working tree 與 `bbc1d56` 相同。`git diff --check 08e158e..c9c9ec5`（排除樣本 JSON）乾淨。四個 commit message 皆為 `[Modify] – …`，`grep -iE "claude|co-authored|generated with"` 0 筆。
- **環境**：`home_work_01/.venv` Python 3.12.14，requests 2.32.3；所有執行皆 `env -u CWA_API_KEY`（shell 內本來就沒有此變數）。
- **Reviewer 對憑證的處理**：Reviewer **沒有讀取** `home_work_01/.env`，沒有發出任何 CWA 請求（probe 一律以 loopback 模擬上游或封鎖非 loopback 的 DNS／socket）。金鑰外洩檢查只用金鑰格式比對與哨兵金鑰（sentinel）。需要 `.env` 的 probe 只在 scratchpad 的匯出副本內放入**哨兵** `.env`，用完即刪；Reviewer 啟動的本機 server 都已停止（`netstat` 確認 5000 埠無 listener）。沒有任何 git 寫入，也沒有修改追蹤中的檔案（本紀錄除外）。

## 2. 分配 AC 的逐條結論

| AC／項目 | 判定 | 證據（Reviewer 自行取得） |
| --- | --- | --- |
| **AC-V2-03**（離線正規化與 API 面） | **FAIL（F-1）** | Reviewer 依 SPEC-V2 R-V2-OBS-2／3／4 與 BRIEF-V2 §3.2 哨兵語義自寫獨立 oracle（`independent_norm.py`，不引用 `observation.py` 的邏輯），對樣本全部 876 筆計算期望：有效 ID 集合 849 筆與回應**完全相同**，dataset Observation Time 相同，所有欄位值與型別只有 **2 處不同**：`C0F9I0` 與 `CAF030` 的 `airPressure`（期望 `990.0`，回應 `null`）。Executor 測試的 6 個手算站（`test_observation.py:141-205`）皆正確、包含哨兵氣溫、哨兵可選欄位、離島縣；回應不含上游結構鍵（遞迴檢查 `:129-136`、`:223-227`）。但以 Reviewer 抽樣的 `C0F9I0` 手算，輸出不等於期望 → AC-V2-03 的 PASS 條件不成立。瀏覽器抽樣屬 #36、preview 屬 #41。 |
| **AC-V2-04**（API 面） | PASS | 樣本 dataset Observation Time＝`2026-09-25T23:00:00+08:00`（獨立 oracle 相同）；最大值取有效站、以時刻比較、回傳發布字串（`observation.py:355-366`）；Fetched Time＝`clock()` 的 `+08:00` 秒精度 ISO 8601（`:534-538`），可控時鐘測試 `test_observation.py:257-279` 通過。 |
| **AC-V2-05**（八個衍生反例） | PASS | `test_observation.py:285-417` 逐條對照 Spec：(1) `-99`／`X`／空字串／`abc`／`-98`／`T`／`990`／`-99.0`／`NaN`／`inf`／缺欄位 → 只排除該站、其他站逐一相等；(2) 無 WGS84、非有限、空、哨兵座標、無 `Coordinates`；(3) `台北市` 等非 22 縣；(4) 全部無效 → 502 `invalid_response`；(5) 刪一半 → 200、有效數＝剩餘有效數；(6) 樣本真實同名站 大坑 `C0T9E0`／`C0F970` 與衍生同名；(7) `ObsTime` 缺、空、`not-a-time`、只有日期、非法日期、非字串 → 排除、不計數、不參與最大值；最新站改壞 → 最大值落到其餘有效站、其他站不變；(8) 全部 `ObsTime` 壞 → 502 `invalid_response`。全部 PASS（`pytest` 385 passed）。 |
| **AC-V2-06**（API 面） | PASS | 視窗內（299 s）同 body／同 Fetched Time、上游只呼叫一次；300 s 重新取得、Fetched Time 更新；視窗 0 每次重取；> 600 s 建構子拒絕；失敗不快取；clock 倒退不延長（`test_observation.py:423-483`）。README 記載 300 s（≤ 10 分鐘）。Reviewer probe：預設參數下對停滯 loopback 上游 → 504 `upstream_unreachable`，5.03 s（read timeout 先到）；滴流由 8 s 總上限截斷（`observation.py:442-446`；測試 `:559-579`）。瀏覽器面屬 #37；平台 gateway 行為屬 #41（另見 F-2）。 |
| **AC-V2-07**（觀測路徑） | PASS | Reviewer probe（`probe_failures.py`）經**真實** Flask app＋**真實** `requests` 對 loopback 上游，root logger 為 DEBUG，並在 fd 層級擷取 stdout／stderr；上游回應本文刻意回顯 `Authorization` 標頭值與標記字串。結果：無金鑰／空白金鑰 → 503 `key_not_configured`；封網（真實 CWA URL）、拒絕連線、連上即關閉、停滯 → 504 `upstream_unreachable`；HTTP 401／403／429／500／503／404／301 → 502 `upstream_error`＋`upstreamStatus`；200 非 JSON、`success:"false"`、零有效 → 502 `invalid_response`。每例皆 JSON，含 `reason` 與非空 `error`；回應本文、標頭、log＋stdout＋stderr 中 **哨兵金鑰、上游 URL、host:port、上游路徑、`opendata.cwa.gov.tw`、上游本文標記、`Authorization` 全部 0 次**。成功路徑的 log 只有 `observation INFO latest observation fetched: 849 valid of 876 stations`。雷達路徑屬 #40。 |
| **AC-V2-16**（靜態＋封網） | PASS | (a′) `_PYTHON_SIDE` 由 import graph 計算，實際集合＝`app.py`、`weather_query.py`（Reviewer 列印確認）；closure 探針測試涵蓋直接、package、相對 import。(b) V1 前端檢查全部保留，另加 first-party 請求形式的字面目標檢查（實際目標只有 `/static/…` 與 `/api/…`）與十個外部目標探針；`_ALLOWED_FRONTEND_URLS` 未變。(c) `observation.py` 加入 no-SQL／no-`sqlite3` 集合。(d) 未變。封網無金鑰行為：見第 5 節（BASE 與 subject 的預報 endpoint byte 相同）。執行期 network log 屬 #36／#41。 |
| **AC-V2-17(a)** | PASS | `git ls-files home_work_01` 只有 `.env.example`，`.env` 被 `home_work_01/.gitignore:12` 忽略；`python -m tools.credential_scan` → `credential scan passed: 558 tracked files; no .env tracked (only .env.example); no CWA-key-format string in tracked files or committed history; no Authorization value in fixture/raw JSON.`；樣本無 `Authorization`／key／token 類鍵、無 URL、無 `CWA-` 字串、無 UUID 形字串（Reviewer 解析樣本確認）。 |
| **AC-V2-17(b)** | PASS | 程式審查：金鑰只在每次請求時由 `self._env.get("CWA_API_KEY")` 讀取（`observation.py:508`），不存於物件；`load_local_env` 只在 `server.py:223` 的 `__main__` 呼叫、路徑固定為單元目錄 `.env`，`api/index.py` 不呼叫。Reviewer 以 `python server.py`（`runpy`，只允許 loopback DNS）在 scratchpad 匯出副本實跑：單元目錄放哨兵 `.env`、cwd 在別處 → 504 `upstream_unreachable`（證明已載入）；`.env` 只在 cwd → 503 `key_not_configured`（證明不讀其他位置）；無 `.env` → 503；三例 `/api/health` 200，server 終端與回應中哨兵 0 次、CWA 主機 0 次。以真實金鑰的本機成功依 AC 的證據類別（worklog）引用 worklog V-13；Reviewer 未重做（不需使用真實金鑰即可驗證機制）。 |
| **AC-V2-17(d)** | PASS | 無金鑰 → 503 `key_not_configured`，同一 app 的預報 endpoint 與 `/api/health` 正常（`test_observation.py:753-803`；Reviewer probe case C）。 |
| **AC-V2-17(e)**（本票 evidence 無金鑰） | PASS | 追蹤檔案（含 worklog、run record）的憑證掃描 0 筆；Reviewer 對 `git diff 08e158e..c9c9ec5` 與 run record 的未提交修改以 `CWA-[0-9A-Za-z]{4,}` 及 UUID 形式搜尋：只有文件化的假金鑰 `CWA-1234-5678-90ab-cdef`（V1 既有 allowlist）與一個 session id（非 `CWA-` 前綴）。A-3 使用紀錄存在（worklog「A-3 金鑰使用紀錄」兩次 GET）。 |
| **AC-V2-20**（本票範圍） | PASS | BASE 收集 259 個 test id，subject 385 個；BASE 的 259 個 id **全部**仍存在（`comm -23` 空）；V1 測試檔的刪除行只有 `_PYTHON_SIDE`／`_NON_SHARED_PYTHON` 定義、其註解、一行區段標題與 docstring 文字（無斷言被刪）。`app.py`（`5693be8…`）、`weather_query.py`（`4d2e92f…`）、`data.db`（`6875869…`）blob 與 `ingestion/` tree（`91df24e…`）在 BASE、`bbc1d56` 與 V1 結案 `ef15d3e` 三者相同。CI：run `36161275690`（`9147997`）與 `36161386808`（HEAD `c9c9ec5`）皆 success，log 為 `385 passed` 與 credential scan passed；workflow 檔未改。 |
| **R-V2-TC-2** | PASS | 樣本為真實 O-A0001-001 回應（876 筆、22 縣、`resource_id` 正確），README 記載擷取時間 2026-09-26 00:04:56 +08:00 與「未縮減」；全部反例在測試內由樣本衍生；提交前後的自動檢查：`test_secrets.py`（樣本列入 `ARTIFACTS`）與 CI credential scan。 |
| **R-V2-TC-3** | PASS | `.github/workflows/**` 無 diff；既有 `home_work_01/**` 觸發涵蓋新測試（CI 385 passed）；A-4 未使用。 |
| **README R-V2-DOC-1 (6) 本機、(7)** | PASS | README「Latest Observation endpoint (V2 Core)」：endpoint 路徑、成功欄位表、四個 reason 與 HTTP 狀態、固定 `error`、逾時（3／5／8 s）、重用視窗 300 s、額度事實、本機 `.env` 與變數名 `CWA_API_KEY`、樣本擷取資訊。Vercel 步驟與 (11) 其餘矛盾敘述屬 #41（見 F-4）。 |
| §6.3 AC-04（re-scope） | PASS | 見第 4 節。 |
| §6.3 AC-07(b)(c)(d)(f)；(e) supersede | PASS | (b)(c)(d) 見 AC-V2-17(a)；(f) 追蹤 evidence 的掃描 0 筆、CI log 離線無金鑰；(e) 對 V2 由 AC-V2-17 取代（本票無 Vercel 動作）。 |
| §6.3 AC-16（API 面） | PASS | V1 `/api/health` 200／503 測試全數保留並通過；byte 對照見第 5 節。 |

## 3. Invariants

| INV | 判定 | 證據 |
| --- | --- | --- |
| INV-V2-1 預報路徑 CWA-free、key-free | **HOLDS** | 靜態：`app.py`＋`weather_query.py` closure 無 HTTP client、無 CWA 字串；`weather_query.py`、`app.py` 不 import `observation`。行為：封網＋無金鑰下全部預報 endpoint 與 BASE byte 相同（第 5 節）；`server.py` 的預報 route 程式與 BASE 相同（diff 只加 import、參數與新 route）。 |
| INV-V2-2 金鑰零外洩、兩個授權位置 | **HOLDS** | 見第 6 節 H-1。 |
| INV-V2-4 `/api/health`、smoke、預報 endpoint 語義不變 | **HOLDS** | `smoke.py`、`vercel.json` 無 diff；`/api/health` 鍵集合不變，觀測狀態未併入；觀測上游失敗時 `/api/health` 仍 200（`test_observation.py:806-810`，Reviewer probe 亦同）。 |
| INV-V2-6（伺服器面）只回成功或分類失敗 | **HOLDS** | `latest()` 只有三條出口：重用中的成功 body、新成功 body、`ObservationFailure.response()`（`observation.py:504-549`）；視窗外的失敗回分類失敗、不帶 `stations`／`observationTime`（`test_observation.py:454-464`）；失敗不寫入快取（`:467-473`）。 |
| INV-V2-8 V1 不變量與產物不變 | **HOLDS**（本票範圍） | 見 AC-V2-20 與第 6 節 H-2；V1 全套 259 個測試保留且通過。 |

## 4. 靜態檢查 re-scope（R-V2-SEC-4，只加不減）

逐項比對 BASE 與 subject 的 `tests/test_static_checks.py`、`tests/test_secrets.py`、`tools/credential_scan.py`：

- **唯一縮小**：AC-04(a) 的 Python 集合由 `(app.py, weather_query.py, server.py, api/index.py)` 改為 `app.py`、`weather_query.py` 的單元內 import closure。這正是 R-V2-SEC-4(a′)／DV-15 明定的 re-scope；條件「`server.py`、`api/index.py` 與 V2 觀測模組 MUST 通過憑證掃描」由 `test_secrets.py` 的 `test_v2_code_has_no_secret`（`server.py`、`api/index.py`、`observation.py`、`test_observation.py`）與 `tools/credential_scan.py` 的全部追蹤檔掃描滿足。
- **擴大**：(b) 新增請求形式檢查與探針；(c) 加入 `observation.py`；憑證掃描 artifact 加入樣本，並有守衛測試確認 CI 清單含樣本；新增 closure 解析探針；新增封網無金鑰的預報 endpoint 行為測試（DV-15 (e)）。
- **未變**：HTTP client 偵測器與 F-4 回歸探針、前端遞迴掃描、絕對 URL 白名單、`/api/` 前綴正向檢查、SQL 擁有者檢查、AC-04(d)、AC-26 全部原樣。
- 結論：除 Spec 明定的 (a′) 集合改變外，沒有任何覆蓋被移除。

## 5. V1 回歸接縫

- **V1 全套離線**：subject 上 `pytest` → **385 passed**（含 BASE 的全部 259 個 id）。
- **預報 endpoint byte 對照（封網、無金鑰）**：Reviewer 自寫 `dump_forecast.py`，在兩個獨立 process 分別載入 BASE（`git archive 08e158e`）與 subject（`git archive bbc1d56`）的 `server.py`，封鎖 `socket.connect`／`connect_ex`／`create_connection`／`getaddrinfo`，對 `/api/health`、`/api/regions`、`/api/days`、6 個 `/api/regions/<r>/series`、7 個 `/api/days/<d>`、未知 Region／日期、`/api/nope`、`/`，以及 missing DB 下的 4 個路徑，記錄 status、body sha256、標頭（排除 Date 類）與 `Cache-Control`：兩份輸出檔 **`cmp` 相同**（26 組）。
- **老師的兩句 SQL**（唯讀開啟 `data.db`）：`SELECT DISTINCT regionName …` → 6 列（北部地區、中部地區、南部地區、東北部地區、東部地區、東南部地區）；`SELECT * … WHERE regionName = '中部地區'` → 7 列（2026-09-24～2026-09-30）；`TemperatureForecasts` DDL 五欄不變。

## 6. High-risk 核對段（decision A-1；derivation record §6）

本票觸及 **H-1、H-2、H-3**（Issue #35 High-risk 段）。

### H-1 憑證與機密 — 核對結果：**HOLDS**

- **兩個授權位置（b3）**：程式只從 process 環境變數 `CWA_API_KEY` 讀金鑰，每次請求時讀、不保存（`observation.py:483`、`:508`）；本機來源只有單元目錄的 `.env`（`load_local_env`，只在 `python server.py` 的 `__main__`），Reviewer 以哨兵 `.env` 證明不讀 cwd 的 `.env`；部署來源為 Vercel 專案環境變數（本票未觸及，RB-3 未觸發）。
- **傳輸**：金鑰只作 `Authorization` 標頭，不在 URL 或 params（`observation.py:386-391`；`test_observation.py:690-697`）。
- **回應與 log**：四類失敗的 `error` 為常數（`observation.py:122-141`）；例外以 `from None` 斷開，例外文字永不記錄或回傳；log 格式只有 reason 與數字狀態；`urllib3` logger 設為 ERROR（`:69`），Reviewer 在 root DEBUG 下確認 urllib3 的 `Starting new HTTPS connection …` 等主機紀錄不出現。第 2 節 AC-V2-07 的 probe（含上游回顯金鑰的最壞情況）零洩漏。
- **git／樣本／evidence**：`.env` 未追蹤；credential scan 0 筆（含歷史）；diff 與 run record 無金鑰格式字串；樣本無 `Authorization`。
- **A-3**：worklog 記錄兩次唯讀 GET（樣本擷取、定向驗證）與不印出／不匯出；Reviewer 未使用金鑰。

### H-2 老師指定的介面或資料格式 — 核對結果：**HOLDS**

`app.py`、`weather_query.py`、`data.db`、`ingestion/`、`static/**`、`requirements.txt`、`smoke.py`、`vercel.json` 與 BASE 無差異（blob／tree 相同，亦等於 V1 結案 `ef15d3e`）；兩句 SQL 結果如第 5 節；預報 `/api/` 與 `/api/health` 在封網無金鑰下與 BASE byte 相同；頁面標題與 V1 概念詞所在的前端檔案未改。

### H-3 資料語義與標示 — 核對結果：**DOES NOT HOLD（F-1）**

- **ObsTime 不正規化**：HOLDS——站層級 `observationTime` 回傳發布字串原文（未 strip、未轉換），dataset 值為最大時刻站的發布字串（`test_values_are_as_published_not_rounded` 以 `"2026-09-25 23:00"` 驗證）。
- **哨兵永不成為數值**：HOLDS——氣溫、可選欄位、座標的哨兵皆為 `null` 或使該站無效；Reviewer 獨立 oracle 未發現任何哨兵變成數值。
- **觀測值「如發布」**：**不成立**——有效的發布值 `AirPressure "990.0"` 被當成哨兵改為 `null`（F-1）。
- **語義分開、無聚合**：HOLDS（本票範圍）——回應只有逐站值，無縣平均或其他聚合；README 標示觀測值為 CWA 測站觀測（如發布）、不是預報或專案推導值，並說明 Fetched Time 不是預報快照取得時間；新增文字無 `real-time`／`live`／`average`。代表測站標示、UI 標示與 CWA 授權標示屬 #36～#41。

## 7. Findings

### F-1 — 有效的氣壓值 `990.0` 被當成哨兵隱藏（Medium，**blocking**）

- **證據**：
  - 樣本中 `C0F9I0` 神岡（臺中市，海拔 194 m）與 `CAF030` 國一S169K（臺中市，海拔 195 m）發布 `WeatherElement.AirPressure = "990.0"`；經 `/api/observations/latest` 回應為 `"airPressure": null`（`probe_semantics.py`）。
  - 這是真實量測：同海拔鄰近站同時段為 潭子 175 m 990.8、中寮 192 m 990.9、茶改場 195 m 989.2、富貴角 196 m 990.2 hPa（測站氣壓隨海拔遞減，990 hPa 落在 ~190 m 站的正常範圍）。
  - Reviewer 的獨立 oracle 對 876 筆全部比對，只有這 2 個欄位不同（其餘 849 站所有欄位相同）。
  - 原因：`SENTINELS` 含 `"990"`（`observation.py:94`），`parse_published_number` 對每個數值哨兵做數值相等比對（`:202-207`），並被套用到所有可選數值欄位（`:325-329`，`airPressure` 在 `:328`、`precipitation` 在 `:329`）。同理，發布的當日累積雨量 `Now.Precipitation = "990.0"`（颱風時罕見但可能）也會變成 `null`（probe 確認）。
  - 測試把這個行為固定下來：`test_observation.py:217-219` 斷言任何可選欄位都不得等於 `990`，`:844` 斷言 `"990.0"` → `None`；worklog 決定 6 把同一集合套用到全部可選欄位。
- **契約依據**：R-V2-OBS-3（可選欄位「有效為數值／文字，無效為 `null`」）；R-V2-DD-7（可選欄位「有效時顯示」）；Issue #35 High-risk 段 H-3「觀測值『如發布』」；AC-V2-03（輸出須等於依樣本手算的期望）。R-V2-OBS-2(b) 的哨兵集合引用「資料標準 V1.05」，其語義依 BRIEF-V2 §3.2（DV-3 引用的「哨兵與欄位事實」）為 `990`＝**風向不定**，是風向代碼，不是氣壓或雨量的缺值代碼；R-V2-OBS-6 的「哨兵→「—」」適用於哨兵，而 990.0 hPa 的測站氣壓不是哨兵、也不是缺值或無效值。
- **影響**：每當有測站的測站氣壓剛好是 990.0 hPa（約 190–200 m 海拔的測站，本樣本 849 站中有 2 站），有效觀測值會以「—」呈現，等同宣稱缺值。方向是隱藏而非捏造，但違反 H-3「如發布」；且錯誤行為已寫進測試，後續票不會發現。
- **Blocking 理由**：這是對 accepted contract（R-V2-OBS-3、R-V2-DD-7、AC-V2-03）的偏離，屬宣告的高風險類別 H-3，並在真實樣本上重現。依 decision A-3，高風險類別的 blocking finding 不得由 Final Adjudicator 單獨 defer。
- **Closure 條件（WHAT；HOW 由 Executor 決定）**：對某欄位而言不是哨兵的發布數值（至少：`AirPressure`、`Now.Precipitation` 的 `990`／`990.0`）必須原樣以數值回傳；各欄位適用的哨兵集合仍須可設定並在 README 文件化（寫明哪些代碼適用哪些欄位）；`WindDirection` 的 `990`（風向不定）仍為 `null`；以樣本衍生反例證明（例如 `C0F9I0`、`CAF030` 的 `airPressure` 為 `990.0`、`WindDirection "990"` → `null`），並修正把 990 固定為「任何可選欄位皆不得出現」的測試斷言。R2 以 Reviewer 的獨立 oracle 重跑全樣本比對。
- **Routing**：若 Executor 或 Orchestrator 主張 Spec 有意把完整集合套用到每個可選欄位，這是設計語義爭議，依治理 §4.3 先交 **Design Authority** 判斷，不得由 Executor 自行關閉本 finding。

### F-2 — 並行請求在上游停滯時被序列化，延遲倍增（Medium，non-blocking）

- **證據**：`LatestObservationService.latest()` 在整個上游取得期間持有 `self._lock`（`observation.py:506`，涵蓋 `:514-522` 的 `fetch_upstream`，上限 8 s），而失敗不快取。Reviewer probe：3 個同時請求、停滯的 loopback 上游、deadline 1.0 s → 分別 1.00 s、2.00 s、3.02 s 完成。以預設 8 s 推算，同一 process 第 k 個並行請求約需 8k s：第 2 個（16 s）超過 worklog 假設的 10 s 平台時限，第 4 個（32 s）超過 §5.3 的 30 s 儀器。本機 `python server.py`（Flask threaded dev server）會發生；部署上只在同一 function instance 同時處理多個請求時發生。
- **契約**：R-V2-OBS-13。對上游請求的逾時 MUST 在字面上成立；端到端的有界時間取決於平台的並行模型與前端的失敗處理（R-V2-OBS-13 同時要求前端把非 JSON／平台層錯誤視為 failure）。
- **為何 non-blocking**：在 worklog 假設的部署模型（每個 instance 一次只處理一個請求）下不會有請求等鎖；前端依契約本來就須把平台錯誤當 failure，UI 仍會到達終態；平台時限與並行模型已是 derivation record §11 #1 的待驗項目。
- **Disposition／owner**：Orchestrator 把本項帶到 **#37**（AC-V2-06(e) 瀏覽器面：前端的 30 秒終態不得只依賴伺服器回應時間）與 **#41**（preview 驗證 Vercel 時限與並行行為）。平台證據若顯示並行停滯會超過界限，依 derivation §11 #1 route **Design Authority**。修正方式屬 HOW（例如不要跨上游呼叫持鎖、或 single-flight），只能在後續合法授權的變更中處理，不併入 F-1 的 targeted correction。

### F-3 — 單筆 `CountyName` 為不可雜湊型別時整體失敗（Low，non-blocking）

- **證據**：某一筆紀錄的 `GeoInfo.CountyName` 為 list 時，`county not in COUNTIES`（`observation.py:305`）拋 `TypeError`，被 `:530-532` 的 catch-all 轉為整體 502 `invalid_response`（probe 確認），而不是只排除該站。與 worklog 決定 7「單筆測站結構不符只使該站無效」不一致。
- **契約**：R-V2-OBS-11 允許「結構不符」回 `invalid_response`，不構成契約違反；CWA 實際發布的 `CountyName` 為字串，實務上碰不到。
- **Disposition**：記錄即可，不需後續處理；日後若修改 `normalize_station`，owner 為該次變更的 Executor。

### F-4 — README 部署段仍寫「function 不需要環境變數與 secret」（Low，non-blocking）

- **證據**：`home_work_01/README.md:411-412`「The running function needs **no environment variable and no secret** — the CWA key is never part of the deployment.」在 #35 加入讀取 `CWA_API_KEY` 的觀測路徑後已不正確。
- **契約**：R-V2-DOC-1(11) 與 (6) 的 Vercel 部分依 derivation record §15.3 分配給 **#41**；#35 只負責 (6) 本機部分與 (7)。worklog Remaining work 2 已列出。
- **Disposition／owner**：**#41**（AC-V2-21(12) 文件審查時修正）。

## 8. Routing 與 reserved boundaries

- **Design Authority**：目前不需要。只有在 F-1 的語義被爭議時才 route（見 F-1）；F-2 在平台證據顯示會超出界限時依 derivation §11 #1 route。
- **Acceptor（reserved boundaries）**：本票沒有觸發任何 RB。沒有合併、沒有 Vercel 操作、單元目錄外沒有變更、workflow 沒有修改。
- **Blocking 與後續流程**：F-1 需要 targeted correction，之後進 R2（治理 §4.4）。F-2、F-3、F-4 不延長本 cycle。

VERDICT: BLOCKING (F-1)
