# Audit record — Spec Integration Audit：SPEC-V2，cycle 1，R1

| 欄位 | 內容 |
| --- | --- |
| Work Contract | **SPEC-V2**（`home_work_01/doc/spec/SPEC-V2.md` **v2.2**，§5.3 儀器註記依 DV-23 更正，commit `2771a54`；以參照繼承 V1 Spec v1.1 `SPEC.md`）。上位：V2 Outcome Contract `home_work_01/doc/governance/outcome-contract-v2.md`（ACCEPTED 2026-09-25，normative candidate `69c5a04`）。Derivation record `decisions/derivation-SPEC-V2.md`（DV-1～DV-19、§4 分配、§6 高風險、§11、§14、§15）與 DV-20～DV-23 decision records；V1 `derivation-SPEC.md`；`decisions/decision-20260923-high-risk-categories.md`（A-1～A-7）。Tickets #35～#41（GitHub Issues，Reviewer 以 `gh issue view` 確認全部 CLOSED）。SPEC-V2 是 V2 Outcome Contract **唯一**的 derived Spec（derivation §4；`doc/spec/` 只有 `SPEC.md`（V1 OC）與 `SPEC-V2.md`，`SPEC.md` 不引用 OC-V2），因此本 audit 同時是「同一 Outcome Contract 最後一份未結 Spec」的全 boundary 涵蓋核對（治理 §4.7 第五項）。 |
| 受審 subject | branch `home_work_01-v2-implementation`；**最終整合 subject `9902026cc41725524f154185aeebd59057fbdadf`**（V2 code chain `08e158e`→`9902026`；README 最終版在 `49dac12`）。V2 run BASE `08e158e`（＝`main`，V1 結案 `ef15d3e` 為其祖先，Reviewer `git merge-base --is-ancestor` 確認）。審查時 HEAD `5905157`；`git diff --name-only 9902026 5905157` 只有 `doc/governance/audit/issue-41-c1-r1.md`、`run/run-20260925-hw01-v2-formal.md`、`worklog/issue-41.md`（Bindings §7 record-only）與 `doc/ticket/tickets-v2.md`（Reviewer 讀 diff：只把 #41 列的狀態由「待執行」改為「已結案…BLOCKED，不是 FAIL」並填 commit 欄＝索引 bookkeeping，不涉任何產物）——皆排除於 subject identity 之外。`git diff --name-only 08e158e 5905157` 單元目錄外 **0** 檔（RB-5），`doc/requirement/` **0** 檔。 |
| Audit 種類 | **Spec Integration Audit**（治理 §4.7；Implementation Profile §6），**cycle 1，R1**。獨立的 audit instance，subject 為整合結果；**不是**任何 Ticket audit 的 R3。 |
| 角色 | `primary_reviewer`（definition `gov-primary-reviewer`；Bindings §3.1 mapping `claude-opus-5-5`／`xhigh`） |
| Binding 證據 | 正式核對由派工者（Orchestrator）依 Bindings §3.4 記入 run record `home_work_01/doc/governance/run/run-20260925-hw01-v2-formal.md`。Reviewer 另以 Bindings §3.4 指令唯讀 harness 紀錄（session `05b8408b-260a-46d3-a4fe-ec07e3ec365a`）自行觀察：`agent-ad2f24768b95d2567` `gov-primary-reviewer` `[('claude-opus-5-5', 'xhigh')]`（本 instance；第一則訊息即本次 SIA 派工），與 #41 R1 的 `agent-a16d3b7e242f9d1aa` 為不同 instance；各票 Executor（例：`a7f0755757b237151` `gov-executor` `[('claude-opus-5-5', 'high')]`）。與 Bindings §3.1 一致。此觀察只供對照，不取代派工者核對。 |
| Independence（治理 §2.3、§4.6） | (1) **Fresh context**：未繼承任何 Executor 或任何 Ticket Reviewer 的對話；worklog、`ACCEPTANCE-V2.md`、七張票的 audit records、run record 與派工文字一律視為待驗證主張，只作入口。(2) **Binding**：見上一列。(3) **Autonomous access**：自讀 OC-V2、SPEC-V2 全文、V1 SPEC 的 INV、derivation record 全文、decision A-1、DV-20～23 分配結果、README（`9902026`，1191 行）主要章節、`CONTEXT.md`、git 歷史與 diff、CI run 與 log、GitHub Issues 與 deployments；以 `git archive` 匯出 V1 `ef15d3e` 與 `9902026` 到 Reviewer scratchpad；自寫整合情境、封網比對、金鑰格式掃描、可達性量測與多項手算；重跑全套 pytest 與全部六個瀏覽器檢查；對 final subject 的 preview 實測。(4) **Self-written record**：本紀錄由 Reviewer 以自己的 Write 工具寫入。**Model diversity：`diversity_lost`**——各票 Executor 與本 Primary Reviewer 同為 `claude-opus-5-5`（Bindings §5、b2 override；decision A-7）；合法，不減損 §2.3 independence。 |
| 日期 | 2026-09-26 |

## 1. 方法與環境

- **環境**：Windows 11；`home_work_01/.venv` Python **3.12.14**；Chrome headless（DevTools protocol）。本機 `core.autocrlf=true`，故 `git archive` 匯出樹為 CRLF；凡比對位元組者（`data.db`、preview 資產）一律改用 `git show <sha>:<path>` 的原始 blob。
- **憑證（RB-3、A-3）**：Reviewer **沒有讀取** `home_work_01/.env`、**沒有使用任何真實 CWA 金鑰**、**沒有進入 Vercel、沒有讀取或填入 Vercel 環境變數**。本機測試一律 `env -u CWA_API_KEY` 在無 `.env` 的匯出樹執行；瀏覽器情境一律用模擬上游與 Reviewer 自訂哨兵金鑰。金鑰外洩檢查只用金鑰格式（`ingestion/checks.py` `KEY_PATTERN` 與更寬的大小寫不敏感版）；命中值從不印出，只印路徑、雜湊前綴與長度。
- **對外請求**：只有 (a) `gh` 讀 Issues、CI、deployments；(b) 對 final subject **public preview** 的一般 GET 與 `smoke.py`。沒有任何 CWA 請求。
- **不寫入**：沒有 git 寫入、沒有修改追蹤中的檔案（本紀錄除外）；結束時 `git status --short` 只有審查前即存在、與本 audit 無關的 `grep.exe.stackdump`。Scratch 全在 scratchpad 內新建、事先確認不存在的 `sia/` 子目錄（未覆寫任何既有 scratch）。

## 2. 範圍一：跨 Ticket invariants（在最終 subject 上逐項核對）

### 2.1 INV-V2-1～9

| INV | 結論 | Reviewer 自行取得的證據 |
| --- | --- | --- |
| **INV-V2-1** 預報路徑 CWA-free、key-free | **成立** | 自寫 `sia_fwd.py`：`ef15d3e` 與 `9902026` 各在子行程封鎖 `socket.connect`／`connect_ex`／`create_connection`／`getaddrinfo`（計數嘗試）、移除 `CWA_API_KEY`，以 Flask test client 對 **5 種 DB 狀態**（committed、missing、0-byte、有表無列、少一列）× **20 個預報路徑**（health、regions、days、六個 series、兩個未知 Region、七個 day、未列日期、`not-a-date`）比較 status＋Content-Type＋body sha256：**100 組、0 差異、兩側網路嘗試 0 次**（200×16、404×4、503×80）。`app.py`／`weather_query.py` 不含 `observation`、`radar`、`requests`、`opendata`、`CWA_API_KEY`；靜態檢查的 `_PYTHON_SIDE` 由 import closure 計算＝`{app.py, weather_query.py}`（Reviewer 執行 helper 確認）。`server.py` 的預報 handler 不呼叫觀測／雷達服務；兩服務建構時不讀金鑰（`env` 只存參照，逐請求讀）。preview（無金鑰）`/api/health` 200。 |
| **INV-V2-2** 金鑰零外洩、兩個授權位置 | **成立（repository 與本機）**；Vercel 側 **BLOCKED（RB-3）** | `git ls-files` 無 `.env`（只有 `.env.example`）；`git check-ignore -v` → `home_work_01/.gitignore:12`。自寫 `sia_keyscan.py`：`9902026`（804 檔）與 HEAD（806 檔）全部追蹤 blob、`git log -p --binary 08e158e..HEAD`（38.0 MB）——移除 `tools/credential_scan.py` 記載的唯一文件化假金鑰後，strict 命中 **0**、寬鬆 **0**（未移除前的 9 個命中檔案全部只含該假金鑰）。`python -m tools.credential_scan` → passed（806 檔）。觀測／雷達只在請求時自 `CWA_API_KEY` 讀（`observation.py:551`、`radar.py:386`），只放 `Authorization` 標頭，雷達影像請求不帶金鑰；`load_local_env` 只讀該一個變數。整合情境：Reviewer 哨兵金鑰與上游標記被注入失敗本文（例外訊息、HTTP 本文、非 JSON 本文），root logger DEBUG 擷取的 server log、每頁 `outerHTML`、`/api/` 回應皆 **0 命中**（金鑰、標記、兩個上游主機、`Authorization`）。preview 回應只含固定句 `key_not_configured`。Vercel 平台面（填入後回應與 runtime log 無金鑰）＝§8 P-2。 |
| **INV-V2-3** 瀏覽器只呼叫 `/api/`、零外部請求（含 Radar） | **成立** | 重跑六個瀏覽器檢查的 network log：modes 50＋refresh 203＋county 136＋fence 506＋radar 113 ＝ **1,008** 請求，外部 **0**（radar 20 次 `/api/radar/latest`、同源 `blob:`）；Reviewer 整合情境 5 個瀏覽器頁面（含 Radar 顯示、Forecast mode、預報 503、一次重新載入）外部 **0**。靜態：`app.js` 的請求形式只有 `fetch("/api/…")`／`fetchJson("/api/…")`、影像 `src` 只為 `URL.createObjectURL` 的同源 blob；`static/` 無 CWA 主機或 `CWA_API_KEY`；`_ALLOWED_FRONTEND_URLS` 與 V1 逐字相同（四個非請求常數）。preview 的 `index.html` 比 blob 多一行 Vercel 注入的 `vercel.live` toolbar script（平台注入、不在 subject 內，§8 注意事項）。 |
| **INV-V2-4** `/api/health`、smoke、預報 endpoint 語義不變 | **成立** | INV-V2-1 的 100 組比對；`smoke.py`、兩個 workflow blob／tree ＝ V1；final subject preview `smoke.py` PASS（0.6 s）；`/api/health` 不依賴金鑰（preview 無金鑰 200）。觀測／雷達狀態只由各自 endpoint 揭露（`server.py` health handler 未改）。 |
| **INV-V2-5** 兩種語義分開、觀測不聚合 | **成立**（H-3） | `app.js`／`index.html` 中「average／mean／平均」只出現在註解與 Forecast mode 專屬元素（`data-mode="forecast"` 的圖例註記與 DERIVED 面板「derived, not an observed daily mean」——AC-V2-10 明列之例外）；縣脈絡只有計數與單站極值（`renderCountyContext`）。Now 標記無色階；整合情境：Now mode 地圖區無 `Select Date`／`DERIVED`／導出圖例，Forecast mode 地圖區無 `Observation Time`／`Fetched Time`／`Refresh`／`Radar`／`OBSERVED`／`Latest Observation`／縣名；頁面無 `real-time`／`realtime`／`live`（`aria-live` 屬性除外）。README l. 86–103、520–530 對照表。 |
| **INV-V2-6** 新鮮度單調；Stale 只以失敗；伺服器只回成功或分類失敗 | **成立** | 伺服器：失敗本文只有 `dataset`／`reason`／`error`（／`upstreamStatus`），`_reusable` 只重用成功、只在視窗內（`observation.py:538–545`、`radar.py:374–380`）。前端：`applyObservation` 較舊 Observation Time 或同一 Fetched Time → not-newer 不改資料；失敗不動 `obs`；全檔無 `setInterval`，`setTimeout` 只有 resize 防抖與兩個 20 s 請求上限。refresh 檢查重跑 97/97（含 +2 h 時鐘仍 success）；整合情境 S1：失敗→Stale 時兩個時間與資料不變、之後成功（00:00）清除 Stale。 |
| **INV-V2-7** 三條路徑獨立降級 | **成立** | 整合情境 S1（§4）：三條同時失敗載入 → 各自顯示各自狀態；觀測單獨恢復、雷達仍 unavailable、預報仍 error；雷達單獨恢復；觀測 Stale 時同一次 Refresh 雷達成功（新 Radar Time）；雷達 Stale 時觀測成功且無觀測標記；預報區段 error 未因任一恢復被清除或遮蔽；預報恢復（reload）時觀測仍 Unavailable、Forecast mode 與 dashboard 完全正常。Now mode 不以 `/api/health` 為前提（`DOMContentLoaded` 先 `loadObservation()` 再獨立 `bootstrap()`）。 |
| **INV-V2-8** V1 不變量與產物不變 | **成立**（H-2） | `git rev-parse` blob／tree（`ef15d3e` ＝ `9902026`）：`app.py` `5693be811edc`、`weather_query.py` `4d2e92f4f385`、`data.db` `687586991ce3`、`ingestion/` `91df24e32fa7`、`data/raw/` `00cb0b88e875`、`requirements.txt`、`smoke.py`、`vercel.json`、`.python-version`、`doc/requirement/`、`.github/workflows`、`static/data/basemap.js`、`static/vendor/`、`tests/test_dashboard.py`、`test_app.py`、`test_map_frontend.py` 全部 **SAME**。V1 凍結範圍內唯一 diff：`api/index.py` docstring（行為不變）。預報 `/api/` 形狀：INV-V2-1 的 100 組。下方 dashboard：整合情境兩模式下 `#forecast-section` innerText 完全相同、表格 7 列＝`/api/` series。 |
| **INV-V2-9** Scope class 分明 | **成立** | V2 只在 Dashboard（`server.py`、`static/`、新模組）；Grading App `app.py`／`requirements.txt` blob ＝ V1（無 folium）；README「Not built」l. 1152–1157 明言 V2 為 ENHANCED、不改變 Part A 評分行為；頁面標題與概念詞未被取代。 |

### 2.2 V1 INV-1～9（V2 下的適用形式）

| INV | 結論 | 證據 |
| --- | --- | --- |
| INV-1 單一查詢語義 | 成立 | SQL 只在 `weather_query.py`（blob ＝ V1）；`_NON_SHARED_PYTHON` 已延伸涵蓋 `server.py`、`api/index.py`、`observation.py`、`representative.py`、`radar.py`（Reviewer 執行 helper 確認），`test_no_sql_statements_outside_shared_module` 等在 614 中通過。 |
| INV-2 行為對等 | 成立 | `test_dashboard.py`（blob ＝ V1）通過；整合情境表格＝`/api/` series。 |
| **INV-3** 快照 6 × 7 | 成立（**重新推導**） | Reviewer 在匯出樹執行 `python -m ingestion --from-json data/raw/F-D0047-091.json --db <scratch>`（離線）→ 42 列；與已提交 `data.db`（blob）逐列、`IngestionMetadata`、`sqlite_master` **全部相同**；0 重複。 |
| INV-4 老師指定的名字（H-2） | 成立 | 見 §7 H-2。 |
| INV-5 金鑰零外洩（H-1；由 INV-V2-2 extend） | 成立（repo／本機）；Vercel 側 BLOCKED | 同 INV-V2-2。 |
| INV-6 呈現層不呼叫 CWA（由 INV-V2-1 re-scope） | 成立於其 V2 範圍 | 預報路徑同 INV-V2-1；伺服器端觀測／雷達路徑為 Δ-1 re-scope。 |
| INV-7 標示（H-3；extend） | 成立 | README l. 49–84（`PROJECT-DERIVED COMPATIBILITY VALUES`、對應表專案定義）、l. 867–874（Derived Map Temperature 導出）；Forecast 面板「Source: CWA F-D0047-091 (county-level) → project-derived six-region values」「(derived, not an observed daily mean)」。 |
| INV-8 Python 3.12 三處 | 成立 | `.python-version` `3.12`（blob ＝ V1）；兩個 workflow `python-version: '3.12'`；CI log `Python 3.12.14`；本機 3.12.14。Vercel build log 確認仍為 V1 acceptor 項目。 |
| INV-9 Scope class | 成立 | 同 INV-V2-9。 |

## 3. 範圍二：Spec-level AC coverage（AC-V2-01～23，含 OC boundary 分配）

判定用語：**PASS**＝本 audit 在最終 subject 上取得的證據成立；**BLOCKED（RB-3）**＝需 acceptor 填入 Vercel 金鑰，不是 FAIL，**不記為 PASS**。「重跑」＝Reviewer 在匯出的 `9902026` 樹以 `--out` 導向 scratch 執行 repo 內未修改的檢查（執行前後 `static/*`、`server.py`、`observation.py`、`radar.py`、`representative.py` sha256 相同）。

| AC | 判定 | 證據（Reviewer 自行取得） |
| --- | --- | --- |
| AC-V2-01 | **PASS** | `check_modes_browser.py` 重跑 **37/37**（health 200／503 皆開在 Now、切換在 1280／375 首屏可見且文字含 `Now`／`Forecast`、鍵盤、Forecast mode 內 AC-17／AC-18 逐字、往返）；`check_county_browser.py` 重跑 **72/72**（DV-20 選縣往返）。整合 S2（1280、375）：選縣 臺北市＋選站 `C0AI40`＋開雷達＋放大一級 → Forecast（6 標記全在地圖內）→ Now：縣、站、中心與 zoom（差 < 1e-6°）、雷達 overlay 與 Radar Time 完全恢復。S1：預報 503 載入仍為 Now。 |
| AC-V2-02 | **PASS** | modes 37/37；整合 S2 兩視野：Now 地圖區無 `Select Date`／`DERIVED`／導出圖例，Forecast 地圖區無觀測／Refresh／Radar／縣文字，dashboard 文字兩模式相同，無 real-time／live；README l. 526–530 與頁面「Last updated (data fetched from CWA)」位置不同。 |
| AC-V2-03 | **PASS**（離線、API、瀏覽器）；**preview 抽樣 BLOCKED（RB-3）** | 614 含 `test_sample_normalises_to_hand_computed_stations` 等。Reviewer 自寫 oracle：真實 `create_app` ＋樣本上游 → `/api/observations/latest` 200，鍵集合只有 7 個正規化鍵、無 `records`／`WeatherElement`／`GeoInfo`／`ObsTime`／`Coordinates`；自原始紀錄手算 臺北 `466920`、金門縣 `C0W240`、連江縣 `C0W220`、澎湖縣 `C0W180` 全部必要與可選欄位 → **0 差異**；哨兵氣溫 `-99` 的 `C0TC00`、`C0V930` 不在回應；可選欄位哨兵（`C0TC30` 風向／風速 `-99`、`C0SE00` 降水 `-99`、`C2I260` 氣壓 `-99`）→ `null`。瀏覽器：modes 重跑（22 標記＝`/api/`、哨兵「—」）。preview：§8 P-3。 |
| AC-V2-04 | **PASS** | API：dataset Observation Time ＝ 有效站最大 `ObsTime`（`test_dataset_observation_time_is_the_max_valid_obstime`；Reviewer API 實得 `2026-09-25T23:00:00+08:00`＝樣本全部 849 有效站之值），Fetched Time `+08:00` 到秒（實得 `2026-09-26T18:24:37+08:00`）。UI：整合 S1 Unavailable 兩欄「—」、Stale 兩時間保留原值、success 更新；refresh 重跑 97/97。 |
| AC-V2-05 | **PASS** | 614 中 `test_ce1`～`test_ce8`（含 (7) 最新 `ObsTime` 改壞 → 最大值落到其餘有效站、(8) 全壞 → `invalid_response`）通過；Reviewer 讀 `normalize_station`／`normalize` 確認排除順序與零有效 → `INVALID_RESPONSE`。 |
| AC-V2-06 | **PASS** | API：reuse 300 s ≤ 600、失敗不重用、時鐘倒退不延長（614）；README l. 407–419 記載值。瀏覽器 (a)～(f)：refresh 重跑 **97/97**。 |
| AC-V2-07 | **PASS** | 614 中 `test_failure_class_through_the_api[no-key／blank-key／http-401／403／429／500／success-false／success-boolean／zero-valid]` 與雷達同構測試通過；整合情境以哨兵金鑰觸發 unreachable／HTTP 500／403／429／非 JSON：頁面與 DEBUG log 0 洩漏，UI 各類別文字可辨。 |
| AC-V2-08 | **PASS** | refresh 97/97；county 72/72（DV-21）；整合 S1：首載失敗 → Now、Unavailable＋類別原因、縣界 22 路徑、Refresh 可用、未自動切模式；選 臺東縣 → 脈絡全「—」（非 0）＋狀態列；成功 → 清除；之後失敗 → Stale 保留資料與兩時間、縣脈絡保留值＋Stale 列。 |
| AC-V2-09 | **PASS**（(a)(b)(c)、API）；smoke 對 preview PASS | 整合 S1：(a) 預報 missing（503）時 Now 完整可用——下鑽、Refresh、雷達皆實際操作成功；預報區段 `role="alert"` 顯示伺服器訊息「The forecast database is missing…」；Forecast mode 地圖 inline 同訊息、`Select Date` 停用；無整頁遮蔽。(b) 觀測斷線＋預報正常（reload）→ dashboard 6 Region、7 列＝`/api/`，Forecast mode 6 標記、圖例、7 日、無 inline error。(c) 雷達 403／非 JSON 只改雷達狀態。API：§2 INV-V2-1 100 組；`test_dashboard.py` 不變通過。 |
| AC-V2-10 | **PASS** | county 72/72 重跑；Reviewer 手算 臺東縣（61 站）最高 27.5 臺東／最低 12.9 向陽，與整合頁面「27.5 °C · 臺東」一致；臺北市 19 站 28.4 石牌／19.4 鞍部、金門縣 6 站 26.0 金寧／23.3 金門(東)（供對照）。無觀測平均字樣（§2 INV-V2-5）。 |
| AC-V2-11 | **PASS** | 614 中 `test_representative.py`；Reviewer **只依 README l. 784–820 的文字規則**對 API 回應手算 22 縣 → **22／22 ＝ `representativeStationIds`**；後備（移除偏好站）臺北市→`466910`、高雄市→`72V140`（東沙島排除）、嘉義縣→`467530`，與模組一致。README 未列舉 22 個 StationId。 |
| AC-V2-12 | **PASS** | county 72/72 重跑（清單 Tab＋Enter、詳情欄位含 StationId、`Back to Taiwan`、鍵盤選縣、東沙島「not on the map」可開詳情）；整合 S2：`Back to Taiwan` 清除選取、視野含本島＋澎湖（1280 z7、375 z6）。 |
| AC-V2-13 | **PASS** | `check_fence_browser.py` 重跑 **113/113**（初始視野、z8／上限拖曳到底逐軸判準、金門／連江可達可選、下限 30.2 %／46.9 %、上限儀器、臺北市可選）。DV-23 更正後數值 Reviewer 以 Web Mercator 自算一致（z12：156543.03·cos23.5°/4096 ≈ 35.05 m/px → 28.5 px/km、375 px ≈ 13.1 km）。地圖 CRS 未被 #40 改變（`L.map` 預設 EPSG:3857）。 |
| AC-V2-14 | **PASS**（另見 F-1） | fence 113/113 重跑；整合 S3：375 在「觀測 Stale＋雷達 Stale＋選縣」組合態 peek 資訊面遮 171／360 px（**52.5 %** 未遮）、Close 可見 ≥ 44×44、`scrollWidth` ＝ 375；S2-375 全序列 `scrollWidth` ≤ 375。 |
| AC-V2-15 | **PASS** | V1 `test_map_frontend.py` blob ＝ V1 且通過；fence 重跑含模式切換／資訊面開合／resize 無 NaN；整合 S2 全序列後 `noNaN` 空、console 無例外；`ensureMapSized` 已改為排隊（#39 R1 F-2 已修，Reviewer 讀 `app.js:2329–2361`）。 |
| AC-V2-16 | **PASS** | (a′)(b)(c)(d)：`test_static_checks.py` 通過、closure 集合與白名單如 §2；封網無金鑰 100 組；network log §2 INV-V2-3。V1 靜態斷言未弱化（刪除行只有 `_PYTHON_SIDE`／`_NON_SHARED_PYTHON` 兩個定義行被延伸版取代與 docstring）。 |
| AC-V2-17 | **PASS (a)(b)(d)(e)**；**(c) BLOCKED（RB-3）** | (a)(e) §2 INV-V2-2 掃描；(b) 程式審查（請求時自 `CWA_API_KEY` 讀、本機只由 `load_local_env` 讀該變數）＋worklog 實跑紀錄（wl35 V-13、wl41 V-9；Reviewer 依 RB-3 未以真金鑰重跑）；(d) 本機 `test_no_key_in_process_env_is_key_not_configured` ＋ **preview（無金鑰）觀測與雷達皆 503 `key_not_configured`、`no-store`**、health 200；(c) §8 P-1、P-2。 |
| AC-V2-18 | **PASS** | `check_radar_browser.py` 重跑 **47/47**；整合 S1／S2：顯示時取得、再次開啟與「顯示中 Refresh」各取得新影像（Radar Time 14:40 → 14:50）、無輪詢、Radar Time 獨立一列、unavailable（無 overlay）／stale（保留 overlay＋時間）、Forecast mode 無雷達、回 Now 恢復。 |
| AC-V2-19 | **PASS** | 重跑 alignment：DOM 幾何 z10 最大 **0.0048 km**、z7 0.0118 km、375 z6 0.0188 km；rendered 像素判定通過；未經重投影的單一 image overlay 3.83 km（儀器具鑑別力）。Reviewer 自 Mercator 公式獨立重算：24 條帶理論最大殘差 **0.0075 km**、單一條帶 **3.808 km**。 |
| AC-V2-20 | **PASS** | 本機匯出樹 614 passed；CI run **`36232697465`**（headSha `9902026`，Python 3.12.14，`614 passed in 9.63s`，credential scan passed）；HEAD `5905157` 之 CI `36234167698` success。Test id：V1 259 個全部在 final 614 中（缺 **0**）。blob／tree 與 §6.3 見 §2、§3.1。 |
| AC-V2-21 | **PASS** | Reviewer 閱讀 README `9902026`：(1) 目錄 l. 39 粗體獨立項 → l. 822 Forecast mode 專屬標題；(2) l. 342–344、546–551；(3) l. 784–820（手算見 AC-V2-11）；(4) l. 646–652；(5) l. 86–103、520–530、601–607、620–630，全文無 DOC-5 (a)–(d) 反例（`live` 只作動詞 l. 1120）；(6) l. 876–891 兩個 V2 資料集全名＋F-D0047-091；(7) l. 903–933（變數名、Production＋Preview、acceptor 親填、不含值、禁 `vercel env pull`）、`.env` l. 130–151、294–298、421–430；(8) l. 340–437、439–502，逾時／重用值與程式常數一致（觀測 3／5／8 s、300 s；雷達 3／5／8 s、120 s）；(9) l. 663–683；(10) l. 720–782；(11) l. 1152–1172 Spec §8 全部項目；(12) l. 141–151、903–911 為 V2 事實且保留預報路徑無 secret；(13) `test_context_glossary_delta_is_verbatim` 自 BRIEF-V2 原檔解析 10 列比對（Reviewer 讀測試本體），BRIEF-V2 在 run 中未改；(14) `ACCEPTANCE-V2.md` 23 列＋§6.3，V1 `ACCEPTANCE.md` 只加 6 行參照（Reviewer diff）。 |
| AC-V2-22 | **PASS**（`GET /` V2、health、smoke、免登入、deployment ↔ commit）；**觀測部分 BLOCKED（RB-3）**；production 為合併後 release evidence | `gh api …/deployments?sha=9902026…` → **`6677133574`**（Preview、sha／ref `9902026…`、`vercel[bot]`）→ status success、`https://aiot-hw01-weather-cckt159kq-nchu-aiot-class.vercel.app`；無 cookie：`python smoke.py <url>` → `SMOKE PASS`（0.6 s）、exit 0；`GET /` 200、`<title>Taiwan Weather Forecast</title>`、`id="mode-now"`、`id="radar-toggle"`、`data-deployment-id="dpl_HVDtY3JaXwXWGCzBwjepGURRJntw"`；服務的 `app.js`、`styles.css`、`data/counties.js` 與 `9902026` blob **位元組相同**，`index.html` 只多一行 Vercel preview toolbar script。 |
| AC-V2-23 | **PASS** | `test_verbatim_labels`、`test_mode_switch_is_two_labelled_buttons`、`test_no_real_time_or_live_wording` 與 county 的 `Back to Taiwan` 測試通過；`index.html` 讀得 `Taiwan Weather Forecast`、`Now`、`Forecast`、`Latest Observation`、`Observation Time`、`Fetched Time`、`Refresh`、`Back to Taiwan`、`Select Region`、`Select Date`、`Date`、`MinT`、`MaxT`。 |

### 3.1 §6.3 定向 V1 重驗

| V1 項目 | 判定 | 證據 |
| --- | --- | --- |
| AC-17、AC-18 | PASS | modes 重跑 37/37（Forecast mode 內逐字）；整合 S1／S2 Forecast mode 6 標記全在地圖內、圖例、7 日。 |
| AC-19 | PASS | fence 113/113 重跑（R-EN-1 六項、375 無橫捲、三態截圖）；整合 S2-375、S3 `scrollWidth` ＝ 375。 |
| AC-02、AC-03、AC-24（Dashboard 側） | PASS | `test_dashboard.py`、`test_app.py` blob ＝ V1 且通過；整合 S1 表格 7 列＝`/api/` series、`Select Region` 6 項順序不變。 |
| AC-04 | PASS | §3 AC-V2-16。 |
| AC-07(b)(c)(d)(f) | PASS | credential scan 通過（`_AUTH_ARTIFACTS` 延伸含兩個 V2 樣本）；金鑰格式掃描 0。 |
| AC-07(e) | **SUPERSEDED for V2**（Δ-3）——一致 | `ACCEPTANCE-V2.md` §3 與 V1 `ACCEPTANCE.md` 新增參照段記述 supersede、不回溯改寫 V1 evidence；存續部分（預報路徑與 health 不需 secret）由 preview 無金鑰 health 200 證明。 |
| AC-10（Dashboard 側） | PASS | 整合 S1（區段層級 error）；`check_series_error_visible.py` 重跑 PASS（503、404 皆可見）。 |
| AC-14 | PASS | 八項不變（README l. 55–58、59–61、62–67、68–77、79–84、867–874 及其餘 Reviewer 抽讀）＋ AC-V2-21 新項。 |
| AC-15、AC-16、AC-22(a) | PASS（preview）；production 合併後 | §3 AC-V2-22、AC-V2-09；`smoke.py`／smoke workflow blob ＝ V1。 |
| AC-26、INV-9 | PASS | `app.py`、`requirements.txt` blob ＝ V1；no-map 靜態檢查通過。 |
| 標題與 masthead | PASS | `<title>`／`<h1>` 逐字；masthead 導言描述兩模式（DR-21.2 先例、RSP-4 MAY）。 |
| 其餘 V1 AC | PASS（CI 全綠＋blob／diff） | V1 259 個 test id 全在且通過；所依產物位元組相同；V2 變更全在單元內（RB-5）。 |

### 3.2 Outcome Contract acceptance boundary 的分配與涵蓋

- **分配完整**（derivation §4：AB-V2-1～13、C-1～C-5、§5 風險全部分配給 SPEC-V2）：Reviewer 以 SPEC-V2 §3 各 AC 的「對應」欄與 §7 矩陣逐條核對——AB-V2-1（01、02、23）、2（03、04、05、23）、3（05、06）、4（07、08）、5（09）、6（10、11、12、23）、7（13）、8（12、14、15）、9（18、19）、10（16、17）、11（20＋§6.3）、12（21）、13（22、17(c)）；每條 AC-V2 都至少對應一條 AB；無缺口、無造成歧義的重疊。S-1～S-11、C-1～C-5 經 derivation §2 對應到 R 再到 AC（S-3→MODE→01；S-4／S-5→DD→10～12；S-6→OBS-10～13→06～08；S-7→DEG→09；S-8→MAP→13；S-9→RSP-5→14；S-10→RSP／DD-9／MAP-5→12、14、15、23；S-11→RAD→18、19；C-1～C-4→02、16、17、21；C-5→reserved）——皆可到達。
- **全 derived Specs 合起來涵蓋整個 boundary**：OC-V2 只有 SPEC-V2 一份 derived Spec，上述即為全 boundary 核對——**成立**。
- **Boundary 的驗證狀態**：AB-V2-2 的「preview 部署驗證」、AB-V2-10 的「部署的 Now mode 在 acceptor 設定金鑰後可運作」、AB-V2-13 的「Now mode 於部署上回傳 Latest Observation」三部分 **BLOCKED（RB-3）**；其餘全部 PASS。分配（coverage）完整不等於這三部分已驗證（§8）。

## 4. 範圍三：整合行為（同一部署頁面上）

除重跑六個既有檢查（modes 37/37、county 72/72、radar 47/47、refresh 97/97、fence 113/113、V1 series PASS——各票各自的整合面）外，Reviewer 自寫跨票情境 `sia_integration.py`：未修改的 `server.create_app`＋真實 `LatestObservationService`／`RadarService`＋模擬上游＋Reviewer 哨兵金鑰，預報快照以 `app.config["DB_PATH"]` 在執行期切換；重用 repo 的 DevTools driver 與雷達測試圖樣，未修改之。**71／71 PASS**。

| 情境 | 驗證的跨票互動 | 結果 |
| --- | --- | --- |
| **S1**（1280×800）三條路徑同時失敗載入後各自恢復 | 預報 missing＋觀測 unreachable＋雷達 403 → Now、Unavailable（原因 `upstream_unreachable`）、預報區段 `role="alert"`、縣界 22 路徑；選縣（Unavailable 下「—」）；開雷達 → radar unavailable（HTTP 403）不改觀測；切 Forecast → inline error、`Select Date` 停用、無標記／縣界／雷達；回 Now 縣與雷達狀態保留。觀測恢復 → success 849 站、縣脈絡 61 站有值、該縣 61 個上圖站全在視野內、雷達仍 unavailable、預報仍 error。雷達恢復 → overlay＋Radar Time 14:40。觀測 500 → Stale（資料、兩時間保留）而同一次 Refresh 雷達成功（14:50）。雷達非 JSON 而觀測成功（00:00）→ 觀測清除 Stale、雷達 Stale 保留 overlay 與 14:50、觀測無標記。預報恢復（reload）而觀測斷線 → dashboard 6 Region／7 列＝`/api/`、Forecast mode 正常、觀測 Unavailable。 | 全部成立 |
| **S2**（1280×800、375×812）下鑽＋雷達＋模式往返＋Stale＋Back to Taiwan | 見 AC-V2-01／02／12；Stale 時縣、站、詳情保留而雷達同次成功；`Back to Taiwan` 後 Stale 與雷達仍在、視野含本島＋澎湖；全序列無 NaN、無 console 錯誤、0 外部請求、0 洩漏。 | 全部成立 |
| **S3**（375×667、375×812）組合態版面 | 觀測 Stale＋雷達 Stale＋選縣（花蓮縣）：兩狀態獨立並存、`scrollWidth` 375、peek 52.5 % 地圖未遮、Close ≥ 44×44；首屏量測見 F-1。 | 契約判準成立；F-1（Low） |
| 縣多邊形指標可達性（`sia_reach.py`，#38 F-2 交接） | 初始視野 3 px 格點 `elementFromPoint`：1280 z7 為 0 的縣＝嘉義市、臺北市（開雷達結果相同——雷達 pane 不攔截指標）；375 z6＝新北市、臺北市、金門縣；1280 放大一級（z8）後臺北市、嘉義市可命中；County 選單 22 縣。 | 契約成立（O-1） |

## 5. 範圍四：最終 subject 的 verification／audit coverage

- **Subject identity**：本 audit 的全部證據取自 `9902026`（匯出樹、`git show` blob、`9902026` 的 CI run、`9902026` 的 GitHub deployment 與其服務資產位元組比對）；不以各票 SHA 代替。`9902026` 之後的 delta 只有 record-only 與索引 bookkeeping（見檔頭），不影響本 coverage（Implementation Profile §7）。
- **Verification**：全套 614（本機匯出樹＋CI）、六個瀏覽器檢查重跑、Reviewer 自寫整合情境 71/71、封網比對、INV-3 重新推導、金鑰掃描、preview smoke。
- **Audit coverage**：七張票的 closing audit 最後一行（Reviewer `grep`）——#35 r2、#36 r1、#37 r1、#38 r2、#39 r2、#40 r1、#41 r1 皆 `VERDICT: CLOSURE`；各票 closing code anchor（`5f0dbc3`、`f63ebb1`、`7a3b469`、`286ee9d`、`f3bf245`、`fedffdd`、`49dac12`／`9902026`）都在 `9902026` 的祖先鏈上；票後的整合變更（`df78e79..9902026`：README、`check_modes_browser.py` 時鐘、`doc/acceptance/`）已由 #41 R1 審查，且本 audit 在最終 subject 上重驗其產品面。未發現 audit 後才出現、未受覆蓋的產品變更。
- **未涵蓋**：§8 的 RB-3 閘門項目（BLOCKED）。

## 6. 範圍五：traceability 與 boundary 符合性

- **Ticket → SPEC-V2 → OC-V2**：#35～#41 issue body 的 Parent 段皆引用 OC-V2（`69c5a04`）、SPEC-V2 v2.2 與 derivation §15；AC 段只引用 SPEC-V2 ID；`Blocked by` 與 derivation §15.1 的 7 條邊一致。
- **DV-20～23 分配已反映**：DV-20（AC-V2-01 選縣往返）與 DV-21（AC-V2-08 縣層於 Stale／Unavailable）寫入 #38 issue body AC 段與 Decisions；DV-22 寫入 #39 AC 段；DV-23 為 SPEC-V2 §5.3 註記更正（`2771a54`：`git diff` 只改標頭加註、§5.3 兩列註記與 §10 一列，無 R／AC／INV 變更；Reviewer 自算數值正確）；`tickets-v2.md`「實作過程中的調整」有四列。derivation §14 各有修訂列。
- **Δ-1～Δ-14 與實作一致**：Δ-1 re-scope（預報路徑 CWA-free，伺服器端觀測／雷達路徑存在）✓；Δ-2（靜態集合＝`app.py`＋`weather_query.py` closure，前端仍只 `/api/`）✓；Δ-3 supersede（部署 function 只為觀測／雷達讀 `CWA_API_KEY`，預報不需；AC-07(e) supersede 記述）✓；Δ-4（掃描延伸到 V2 樣本／程式／evidence）✓；Δ-5（Forecast mode ＝ V1 地圖、AC-17／18、README 可找）✓；Δ-6（R-EN-1 於 V2 介面、Now 三態）✓；Δ-7（DR-19 收斂為預報區段層級，§4 S1）✓；Δ-8（health／smoke 不變）✓；Δ-9（無前端外部主機例外）✓；Δ-10（heatmap／自動更新仍 Later：無輪詢碼）✓；Δ-11（離島只在 Now：代表站含 澎湖縣 `467350`、金門縣 `467110`、連江縣 `467990`；Forecast 六區不變）✓；Δ-12（`basemap.js` blob ＝ V1、縣互動圖層固定樣式不以資料著色、只在 Now）✓；Δ-13（標示與授權，README）✓；Δ-14（CONTEXT 詞彙 delta 逐字）✓。§1.2 末段「明確不變」各項皆由 §2 blob／行為證據支持。
- **沒有超出 boundary**：程式中無 O-A0002／O-A0003、`pushState`／history、`localStorage`、heatmap、`setInterval`、持久寫入、速率限制；`?region=` 深連結為 V1 既有（V1 `app.js` 同樣存在）；53 個 V2 commit 全在單元內、無 `doc/requirement/` 變更、無 workflow 變更（A-4 未使用）、訊息格式合規且無 Claude 標記。
- **契約語義不足**：未發現需要 Design Authority 裁決的 ambiguity 或 boundary 疑義。

## 7. 高風險類別核對段（decision A-1、A-2；derivation §6 A-2）

- **H-1 憑證與機密（INV-V2-2／V1 INV-5）——核對了什麼**：(a) `git ls-files`／`check-ignore`；(b) `9902026` 與 HEAD 全部追蹤 blob、V2 全 patch 的金鑰格式掃描（假金鑰外 0）；(c) repo 掃描工具通過；(d) 程式審查：請求時讀、只作 `Authorization` 標頭、影像主機不帶金鑰、log 只記 reason／狀態碼、失敗文字為常數；(e) 整合情境以哨兵金鑰與上游標記觸發五類失敗，頁面／回應／DEBUG log 0 洩漏；(f) README 金鑰步驟無值；(g) b3 兩位置：本機 `.env` 未追蹤；Vercel 尚未填入（preview 503 `key_not_configured` 證實）；(h) Reviewer 本身未讀 `.env`、未接觸 Vercel。**結果：成立（Vercel 平台面 BLOCKED，§8 P-2）。**
- **H-2 老師指定的介面或資料格式（INV-V2-8／V1 INV-4）——核對了什麼**：(a) §2 blob／tree 全部 SAME；(b) Reviewer 以唯讀 URI 開啟 `git show 9902026:home_work_01/data.db`（sha256 `9bbf05bc6cc803444c8760432d6b484699c597f751fa16cb58bfbb5a0dbf542b`，與工作樹相同）執行老師兩句 SQL：`SELECT DISTINCT regionName FROM TemperatureForecasts;` → **6 列**（北部地區、中部地區、南部地區、東北部地區、東部地區、東南部地區）；`SELECT * FROM TemperatureForecasts WHERE regionName = '中部地區';` → **7 列**（id 8–14，2026-09-24…2026-09-30）；共 42 列、重複 0；DDL 逐字 `id INTEGER PRIMARY KEY, regionName TEXT, dataDate TEXT, mint REAL, maxt REAL`；(c) INV-3 重新推導相同；(d) 預報 `/api/` 100 組相同；(e) 頁面標題與概念詞逐字、preview `<title>`。**結果：成立。**
- **H-3 資料語義與標示（INV-V2-5／V1 INV-3、INV-7）——核對了什麼**：觀測（如發布，`OBSERVED`）與推導（`DERIVED`）分開、不共用圖例或色階；代表站值不當縣值（頁面註記、README）；無觀測聚合（§2）；Latest Observation 用語、無 real-time／live；`Fetched Time` 與預報快照取得時間分開；CWA 授權標示 README 兩個 V2 資料集全名（應用內見 O-3）；V1 推導值標示與 INV-3 推導不變。**結果：成立。**
- A-3（高風險 blocking finding 不得由 FA 單獨 defer）：本 audit 無 blocking finding，不適用。

## 8. RB-3 金鑰閘門（BLOCKED，不是 FAIL）

- **現況**：final subject preview（`6677133574`）`/api/observations/latest` 與 `/api/radar/latest` 皆 **503 `key_not_configured`**、`/api/health` 200——證實金鑰尚未填入，且缺金鑰時平台行為正確。這是 Bindings §2.6 RB-3 的真正保留 boundary（Spec §9 前置 1、derivation §11 #4）。
- **BLOCKED 項目（本紀錄不將任何一項記為 PASS）**：**AC-V2-17(c)**；**AC-V2-22 觀測部分**；**AC-V2-03 preview 抽樣**；**decision A-6 preview 觀測驗證紀錄**；連帶 AB-V2-2／10／13 的部署部分、INV-V2-2 的 Vercel 平台面。
- **Post-key 驗證計畫**（`ACCEPTANCE-V2.md` §6.2 P-1～P-4，Reviewer 核對其可執行性並補充）：前提＝acceptor 依 README l. 913–933 在 Vercel 專案填入 `CWA_API_KEY`（Production＋Preview）並 redeploy；之後在該 redeploy 的 preview（以 GitHub deployment 證明 deployment ↔ commit，且該 commit 與本 subject 的差異只能是 record-only）：
  - **P-1**（AC-V2-17(c)、AC-V2-22 觀測）：`GET /api/observations/latest` → 200、`dataset` O-A0001-001、`validStationCount` ≥ 1、`stations[]`、`observationTime`、`fetchedTime`；瀏覽器 Now mode 顯示 Latest Observation 與兩個時間；`smoke.py` 仍 PASS。
  - **P-2**（AC-V2-17(c) 雷達、INV-V2-2 平台面）：`GET /api/radar/latest` → 200 `image/png`＋`X-Radar-Time`＋`X-Radar-Dataset: O-A0058-006`；所有記錄的回應本文與標頭、以及 acceptor 提供的 Vercel runtime log 畫面，**只以金鑰格式（`KEY_PATTERN`／`tools.credential_scan` 同一規則）掃描**，驗證者永不讀出 Vercel 值；無上游 URL、無 `Authorization`。
  - **P-3**（AC-V2-03 preview）：≥ 3 站頁面值＝同頁 `/api/observations/latest` 本文、哨兵「—」。
  - **P-4**（A-6 紀錄＋Vercel 時序；#35 F-2／#40 F-2）：記錄 P-1～P-3 的時間、URL、deployment id；量冷啟動；可行時兩個並行請求；終態在頁面 20 s 內；若平台時限低於 8 s 上游上限的假設 → route **Design Authority**（derivation §11 #1）。
  - 注意：preview 頁面會載入 Vercel 注入的 `https://vercel.live/_next-live/feedback/feedback.js`——屬平台注入、不在 subject 內、production 不注入，不得記為 AC-V2-16／INV-V2-3 違規（AC-V2-16 的證據本就是 loopback log）。
  - **證據類別要求「Reviewer 重現」**：P-1～P-3 的結果須由獨立 Reviewer 重現（本 SIA 的後續派工、或 Orchestrator 另派同角色的 post-key 驗證），不得只以 Executor 紀錄結案。
- **對後續階段的意義**：本 SIA 的 CLOSURE 只涵蓋可完成範圍；DA phase acceptance 與 Outcome Contract closure 不得把上列項目視為已驗證。phase acceptance 是否可在其 BLOCKED 下先行（或須待 post-key 驗證），由 Design Authority 依治理 §3.8 判斷；填入金鑰本身屬 acceptor（RB-3）。

## 9. #38～#40 地圖可用性交接（`ACCEPTANCE-V2.md` §8）——整合層判定

| 交接項 | 整合層判定 |
| --- | --- |
| a38-r1 F-2／a39 hand-off：初始縮放的縣多邊形指標可達性 | Reviewer 重量（§4）：1280 z7 嘉義市、臺北市，375 z6 新北市、臺北市、金門縣無可命中像素（被代表標記覆蓋）；放大一級即可命中、County 選單 22 縣、代表標記本身可選。R-V2-DD-4 未綁定縮放層級、DD-9(a) 路徑存在、DV-22 §4.2(5) 只要求可經 hover／點選到達——**不違反任何 Spec AC**。記 O-1，non-blocking。 |
| a39-r1 F-3：< 1024 px expanded 資訊面中選站後標記在面板下 | RSP-5(b) 只約束 normal／peek；Collapse 後 `reveal` 把標記帶到 peek 上方；整合情境 peek 態 52.5 % 未遮。**不違反 AC**；non-blocking，維持 #39 disposition。 |
| a39-r1 O-2：下限 zoom 6、寬 ≥ 768 px 時拖曳中暫態中心離開 E | AC-V2-13 以「拖曳到底後」讀取，fence 重跑 113/113 靜止視野全部 PASS；R-V2-MAP-1 明列彈性回彈屬 HOW。**不違反 AC**。 |
| a39-r2 O-5／O-6／O-7 | O-5（1024×768 頁面捲動）、O-6（清單下方項目焦點優先）、O-7（縮放鈕下標記保留顯示）皆為一般版面性質、無 AC 受影響；整合情境未見惡化。non-blocking。 |
| a40-r1 F-1：375 px 雷達控制使首屏地圖減少 | Reviewer 在整合組合態重量——**累積效應比單票所見更明顯**，記為 **F-1**（Low，non-blocking）。 |
| a39-r1 F-2（延後步驟被丟棄） | 已於 #39 修正（`app.js:2335–2338` 排隊），整合情境無回歸。 |

## 10. Findings

### F-1（Low，non-blocking）——375 px 失敗組合態下，地圖上方的狀態區累積到 606 px，首屏看不到地圖

- **證據**：`sia_integration.py` S3（`layout.json`；截圖 `S3-375x812-combined-first-screen.png`、`…-combined-map-in-view.png`）。地圖頂端 y／首屏可見地圖高（地圖高 360 px）：

  | 狀態 | 375×812 | 375×667 |
  | --- | --- | --- |
  | success、雷達關 | 610／**202** px | 610／**57** px |
  | success、雷達開 | 642／**170** px | 642／**25** px |
  | 觀測 Stale＋雷達 Stale＋選縣 | 948／**0** px（Now 面板高 606 px） | 948／**0** px |

  組合態把地圖捲入視野（下緣對齊）時：375×812 仍同時看得到兩個時間、`Refresh`、`Back to Taiwan` 與 peek 面板（模式切換在畫面外 −257 px）；375×667 則 `Refresh` 頂端 −4 px、時間與模式切換皆在畫面外。成因是 #36～#40 各自加入、在 < 1024 px 全堆在地圖上方的內容：Stale 說明區塊（標題＋說明＋原因）、雷達按鈕使 County 換列、Radar Time 列與 3～4 行 radar stale 原因。
- **契約**：R-V2-RSP-4／OC S-10「地圖 MUST 是頁面的主要內容區；模式切換不捲動即可見」——只對模式切換給出「不捲動」判準（載入時成立：底緣 291 px），對地圖沒有首屏量化判準；V1 在 375×667 本就只有部分地圖在首屏。R-V2-RSP-5(b)(g)、RSP-6 約束的是資訊面／overlay 遮蔽（組合態仍 52.5 % 未遮、控制未被遮蔽、捲動可達）。OC S-1／R-V2-OBS-4(c)「兩個時間永遠／同時可見」：兩時間始終顯示於 Now 面板、未被應用程式隱藏；這裡是使用者在短視窗捲動頁面所致，與 #39 R1 F-1（應用程式自身的面板捲動在核心下鑽態把時間移出視野）性質不同。**無 AC 或 invariant 違反**。
- **為何 non-blocking**：可用性退化而非契約違反；只在兩條路徑同時失敗（且雷達由使用者開啟）時出現；非失敗態與單一失敗態仍有地圖在首屏（375×812）。
- **Disposition**：不延長本 cycle。Owner：**acceptor**——若要壓縮（例如 < 1024 px 時把 Stale／radar stale 說明收成一行、雷達按鈕與 County 同列），屬 HOW，須以新的 work item（Bindings §4 第 3 列，已結案工作之後的單點修正）經 acceptor 指示授權；若 acceptor 要求 375 px 首屏必有地圖的保證，那是新的 requirement（contract change），不是本 Spec 的缺陷。不需 Design Authority。

（無 Critical／High／Medium finding。）

## 11. 觀察（非 finding）

- **O-1**：縣多邊形指標可達性量測（§4、§9）——契約成立，記錄供後續可用性工作參考。
- **O-2**：`ACCEPTANCE-V2.md` 的最終 network log 數字（136／506／1,008，「six logs」）與已提交 ev41 五個 log 的內容（135／505）不一致——即 #41 R1 F-1，已有 owner，本 audit 不重開；Reviewer 重跑得到 136／506／合計 1,008，顯示差異為執行間的正常浮動，零外部的結論不受影響。
- **O-3**：應用內觀測授權標示（R-V2-DOC-2 SHOULD）：`index.html` l. 283 只寫「CWA station observations (O-A0001-001, hourly)」，未含「交通部中央氣象署 氣象觀測站-全測站逐時氣象資料」全名（雷達列 l. 291 有全名）；README（MUST）兩者齊全，偏離理由記於 wl41 決定 5。整合層判定同 #41 R1：SHOULD 部分滿足、有記錄理由，non-blocking；若 acceptor 要補齊，是一行 UI 文字的後續 work item。
- **O-4**：`CONTEXT.md`「Web App」詞條「never call CWA」描述的是 MVM 的預報讀取行為，依 Δ-1／INV-V2-1 與 V2 伺服器端觀測路徑不矛盾（#41 R1 O-1 同判）；R-V2-DOC-4 只要求 BRIEF-V2 §9 的 delta。
- **O-5**：伺服器觀測／雷達服務在上游取得期間持鎖（#35 F-2、#40 F-2）——同 instance 的並行停滯請求會排隊；前端 20 s 上限保證終態。平台行為屬 §8 P-4（BLOCKED）。
- **O-6**：`requests` 對雷達影像會跟隨重新導向（#40 O-3）；金鑰只在 metadata 請求、跨主機重新導向時 `requests` 會移除 `Authorization`。不在契約範圍。
- **O-7**：375 z6 的雷達開／關命中計數有差異（金門縣 0 → 有），Reviewer 推測是雷達資訊列使版面下移後 3 px 格點的取樣相位不同（未另行證實）；1280 下開／關完全相同，且雷達 pane `pointer-events: none` 已由程式（`app.js:2406–2408`）確認，雷達不攔截指標。

## 12. Routing

| 事項 | Authority | 理由 |
| --- | --- | --- |
| 在 Vercel 填入 `CWA_API_KEY`（Production＋Preview）並 redeploy，解除 §8 的 BLOCKED | **acceptor**（RB-3，Bindings §2.6） | 保留 boundary；Agents 不得填入／讀出。 |
| 金鑰填入後由獨立 Reviewer 重現 P-1～P-3、記錄 P-4 | **Orchestrator**（派工）；判定由 Reviewer | AC-V2-17(c)、AC-V2-22 的證據類別要求 Reviewer 重現。 |
| P-4 若平台時限低於 8 s 上游上限的假設 | **Design Authority** | derivation §11 #1。 |
| DA phase acceptance 如何處理 §8 的 BLOCKED 項（先行或等待 post-key 驗證） | **Design Authority**（治理 §3.8） | 本 CLOSURE 不把任何 RB-3 項目記為 PASS。 |
| F-1、O-3 的任何 UI 調整 | **acceptor**（新 work item 的指示） | 已結案範圍之後的單點修正；非契約缺陷。 |
| 合併（RB-1）、繳交（RB-2）；production smoke 與觀測抽樣為合併後 release evidence | **acceptor** | 保留 boundary。 |

未發現需要 Design Authority 裁決的契約語義不足或 boundary 疑義。

## 13. Evidence（Reviewer scratchpad `…/scratchpad/sia/`，未提交）

- `fin/`、`v1/`（`git archive` 匯出）；`data_sia.db`、`dbs/`、`rebuild.db`；`ids_fin.txt`、`ids_v1.txt`。
- `sia_fwd.py`＋`fwd_v1.json`／`fwd_fin.json`（封網無金鑰 100 組）；`sia_keyscan.py`（金鑰格式掃描）；`sia_integration.py`＋`int1/`（`results.json` 71/71、`layout.json`、`network.json`、`server.log`、截圖）；`sia_reach.py`（指標可達性）。
- `bc/`：六個既有瀏覽器檢查重跑的結果、network log 與截圖；`sha_before.txt`／`sha_after.txt`（執行前後 subject 檔案不變）。
- `pv/`：final subject preview 的回應本文、標頭與 blob 比對。

## 14. 結論

五個範圍在最終整合 subject `9902026` 上逐項核對：跨 Ticket invariants（INV-V2-1～9、V1 INV-1～9，含 INV-3 重新推導與老師 SQL 6／7）成立；AC-V2-01～23 與 §6.3 定向 V1 重驗在可完成範圍內全部 PASS，OC-V2 的 AB-V2-1～13、S-1～S-11、C-1～C-5 經 SPEC-V2 完整分配且 SPEC-V2 為唯一 derived Spec；整合行為（三路徑獨立降級、模式／下鑽／Refresh／Stale／雷達／圍欄在同一頁面的互動）以 Reviewer 自寫情境 71/71 與六個檢查重跑證實；最終 subject 的 verification／audit coverage 完整；traceability、DV-20～23 分配與 boundary 符合。H-1／H-2／H-3 成立。唯一 finding F-1 為 Low、non-blocking。**AC-V2-17(c)、AC-V2-22 觀測部分、AC-V2-03 preview 抽樣與 decision A-6 preview 紀錄維持 BLOCKED（RB-3），本紀錄不將其記為 PASS**；解除後依 §8 由獨立 Reviewer 重現。

VERDICT: CLOSURE
