# Audit record — Issue #29，cycle 1，R1（A-4 independent audit）

| 欄位 | 內容 |
| --- | --- |
| Work Contract | GitHub Issue **#29**（`yotsubamomo/aiot-classwork`）「Ingestion 取得時間格式驗證（#18 R2 N-1）」。本 work item 的 Outcome Contract＝acceptor 2026-09-24 直接指示（逐字見 DR-22 §0；Bindings §2.3 末項、§4 第 3 列）。Governing decision：**DR-22** `doc/governance/decisions/decision-20260924-acquired-at-validation.md`（DR-22.1 lane＝Lightweight、A-4 必做；DR-22.2 boundary B-1..B-8／X-1..X-10；DR-22.3 接受準則 AT-1..AT-12、OK-1..OK-6、NG-1..NG-14、V-1..V-8；DR-22.4 H-3／H-1／H-2；DR-22.5(A) 整合重驗；DR-22.6 文字義務）。不變契約：DR-17 §4.1–§4.6、§7；R-DB-5；INV-3、INV-5；`decision-20260923-high-risk-categories.md` H-1、H-3、A-1、A-4、A-5。來源 finding：`issue-18-c1-r2.md` §5 N-1。 |
| 受審 subject | branch `home_work_01-hw10-implementation`；實作 subject **`bd52ede140233a9c4c5b568ffaf9ead1620a6ce0`**；parent `cc29c7fed7dabc826b7d01f0d4d0b8104c235c59`。HEAD `b4b121f`：`git diff --name-only bd52ede..b4b121f` 只有 `doc/governance/worklog/20260924-acquired-at-validation.md`（record-only，Bindings §7）。審查範圍 `git diff cc29c7f..bd52ede`（9 檔；排除 `doc/governance/**` 後 7 檔，見 §5.1）。 |
| Audit 種類 | **R1**（A-4 必做 independent audit；DR-22.1），**cycle 1**。依 DR-22.5(A) 本 R1 涵蓋 DA 指定的整合重驗（§5）。本紀錄**不是** Spec Integration Audit，也不得被引用為 Spec Integration Audit（DR-22.5 首段）。 |
| 角色 | `primary_reviewer`（definition `gov-primary-reviewer`；Bindings §3.1 mapping `claude-opus-5-5`／`xhigh`） |
| Binding 證據 | 由派工者依 Bindings §3.4 核對並記入 worklog 或 run record。**本 audit 時點（HEAD `b4b121f`）worklog 與 `run/run-20260924-hw01-formal.md` 都還沒有 #29 的 binding 核對紀錄**（grep `#29`／`DR-22` 於 `doc/governance/run/` 0 筆；worklog 無 agentId／observed model 欄位），見 F-5。本紀錄不自證 binding。 |
| Independence（治理 §2.3） | (1) fresh context，未繼承 Executor 對話；worklog、commit message、`ACCEPTANCE.md`、`tickets.md` 的敘述全部當作待驗證主張（worklog「`re.fullmatch` 等效」與 README「Anything else is rejected」被本 audit 推翻，見 F-1、F-3）。(2) Binding 見上一列。(3) 自主取得：自己讀 DR-22、DR-17、N-1、high-risk decision、Bindings、治理本文；自己用 `git archive` 匯出 subject 與 parent；以專案 pin 的 Python 3.12.14（`home_work_01/.venv`）跑全套測試、真實 `python -m ingestion` CLI、自寫的 validator 探測、mutation run、A-5 掃描與 `gh run` 查 CI。(4) 本紀錄由 Reviewer 以自己的 Write 工具寫入。 |
| 日期 | 2026-09-24 |

## 1. 審查方法與環境

- **Subject 確認**：`git rev-parse bd52ede cc29c7f` 與派工一致；`git status --porcelain` 開始與結束都只有 repo 根目錄的未追蹤 `grep.exe.stackdump`（不是本 audit 產生）。本 audit 未改任何追蹤檔案，也沒有做任何 git 寫入。
- **乾淨匯出**（Reviewer scratchpad，每個目錄都是新建的）：`pr29r1_subj`、`pr29r1_parent`（全套測試、mutation 來源）；`pr29r1_h1`、`pr29r1_parent_h1`（CLI harness，放入哨兵 `.env`，跑完即刪除）；`pr29r1_ac12`（AC-12 重建）。匯出內容 161 檔，等於 `git ls-tree -r bd52ede home_work_01` 的 161 檔，沒有 `.env`。
- **Python**：`home_work_01/.venv/Scripts/python.exe` → `Python 3.12.14`（`.python-version` = `3.12`）。
- **網路封鎖**：CLI／AC-12 執行時以 `PYTHONPATH` 載入 Reviewer 的 `sitecustomize.py`，讓 `socket.connect`、`create_connection`、`getaddrinfo` 丟 `OSError`；已確認 `getaddrinfo('opendata.cwa.gov.tw', 443)` → `OSError: network blocked by reviewer harness`。
- **腳本**（scratchpad）：`pr29r1_probe_validator.py`（validator 探測）、`pr29r1_cli_harness.py`＋`pr29r1_online_wrapper.py`（真實 CLI subprocess）、`pr29r1_mutants.py`（mutation）、`pr29r1_a5_scan.py`（A-5）。
- 所有 subprocess 都已正常結束；沒有啟動任何 server 或背景程序。

## 2. 獨立測試矩陣

### 2.1 Validator（DR-22.3 AT-1..AT-7；`ingestion/acquisition_time.py`）

獨立 oracle 直接依 AT-1～AT-3 撰寫：`isinstance(v, str)`，`[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\+08:00` 的 `fullmatch`（ASCII 數字，依 AT-2 括號文字），以及 `strptime` 成功。

| 類別 | 值 | 結果 |
| --- | --- | --- |
| VALID（8） | `2026-09-24T02:24:50+08:00`（OK-1）、`2026-09-24T01:39:31+08:00`（OK-2）、`2026-09-24T12:00:00+08:00`（OK-3）、`2026-01-01T00:00:00+08:00`（OK-4）、`2026-12-31T23:59:59+08:00`（OK-5）、`2028-02-29T12:00:00+08:00`（OK-6）、`2000-02-29T00:00:00+08:00`、提交的 sidecar 值（讀檔） | 全部接受；`validate_acquisition_time` 回傳原字串（AT-12） |
| INVALID，ASCII 字串（40） | `''`、`yesterday`、`2026-09-24`、`…50Z`、`not-a-time`、naive `…50`、`+0800`、`+08`、`+09:00`、`+00:00`、`-08:00`、小寫 `z`、`.5`、`.000`、`.123456`、空白分隔、小寫 `t`、前導空白、尾隨空白、尾隨 `\n`、前導 `\t`、尾隨 `\r\n`、`'   '`、`2026-02-29`、`2026-02-30`、`2026-13-01`、`2026-00-10`、`2026-09-00`、`2026-09-31`、`T24:00:00`、`:60:00`、`:24:60`、`:24:61`、`1900-02-29`、`20260924T022450+08:00`、`2026-9-24…`、`+2026-…`、`+08:00:00`、`+08:00Z`、`…02:24+08:00` | 全部拒絕（`AcquisitionTimeError`）；訊息含 `repr(值)` 與 `YYYY-MM-DDTHH:MM:SS+08:00`。小數秒被拒絕，**沒有被截斷**；前後空白被拒絕，**沒有被 trim** |
| INVALID，非 ASCII 數字（6） | `２０２６-09-24T02:24:50+08:00`（全形）、`٢٠٢٦-09-24T02:24:50+08:00`（阿拉伯-印度數字）、`2026-09-24T02:24:5٠+08:00`、`2026-09-24T0２:24:50+08:00`、`2026-09-24T02:2٤:50+08:00`、`2026-09-2４T02:24:50+08:00` | **6 個全部被接受**（oracle＝不合格）→ **F-1** |
| 非字串（11） | `1758651890`、`1.5`、`nan`、`True`、`False`、`None`、`{}`、`[]`、`['…+08:00']`、`{'v': '…+08:00'}`、`b'…+08:00'` | 全部拒絕；訊息附 JSON 型別（`JSON number／boolean／null／object／array`；bytes → `bytes`） |

原因（F-1）：`_PATTERN = re.compile(r"^\d{4}-…$")`（`acquisition_time.py:35`）在 Python 的 str pattern 中，`\d` 會匹配所有 Unicode 十進位數字；`strptime` 的 `%Y`／`%d`／`%H`／`%M`／`%S` 也接受它們（`int()` 會把全形與阿拉伯-印度數字轉成整數），所以兩道檢查都通過。

### 2.2 三個套用點，經真實 `python -m ingestion`（subprocess，`cwd`＝匯出目錄）

每個失敗案例都檢查：exit＝1；stderr 以 `Ingestion failed: ` 開頭；沒有 `Traceback`；**stdout 為空**（沒有印出 derive preview，表示驗證在讀 raw JSON／derive 之前）；seeded DB 的 sha256、`st_mtime_ns`、`TemperatureForecasts` 全部列與 `IngestionMetadata` 都不變（INV-3）；stdout＋stderr 不含哨兵金鑰、`CWA_API_KEY`、`Authorization` 或哨兵片段。

| # | 套用點 | 案例 | 結果 |
| --- | --- | --- | --- |
| P1-a | CLI `--acquired-at`（DB 先 seed） | 21 個不良值：NG-1..NG-4、`not-a-time`、NG-6、NG-7、NG-8(+09/+00)、NG-9(`.5`、`.000`)、NG-10、NG-11、NG-12（前導空白、尾隨空白、前導 tab、`'   '`）、NG-13（`02-29`、`13-01`、`T24`、`:60`） | 21/21 fail-closed；訊息含 `repr(值)`、`from --acquired-at`、格式、「omit --acquired-at to read the provenance sidecar instead」 |
| P1-b | CLI，DB 路徑不存在 | `''`、`yesterday`、`…Z`、`….5+08:00` | 4/4 exit 1，**DB 檔沒有被建立**（證明沒有開啟 DB） |
| P1-c | CLI 不合格＋**合格** sidecar（AT-9） | `''`、`yesterday`、`…Z` | 3/3 exit 1，快照不變，**沒有退回 sidecar** |
| P1-d | CLI 合格＋不合格 sidecar | `2026-09-22T18:30:00+08:00`＋sidecar `not-a-time` | exit 0，存入 CLI 值（sidecar 沒有被讀） |
| P2-a | sidecar `acquiredAt`（不給 `--acquired-at`，DB 先 seed） | 16 個：`not-a-time`（NG-5）、`''`、`yesterday`、`2026-09-24`、`…Z`、naive、`.5`、前導空白、尾隨 `\n`、`02-30`；NG-14：`1758651890`、`1.5`、`true`、`null`、`{}`、`[]` | 16/16 fail-closed；訊息含 `resp.meta.json`、`'acquiredAt' field`、格式，以及 `repr(值)` 或 `(JSON <型別>)` |
| P2-b | sidecar，DB 路徑不存在 | `not-a-time`、`null`、`''` | 3/3 exit 1，DB 檔沒有被建立 |
| P2-c | sidecar 缺鍵／非 dict／損壞／不存在 | — | 皆 exit 1、快照不變。缺鍵與非 dict 的訊息為 `provenance record resp.meta.json has no 'acquiredAt' value`，**與 parent `cc29c7f` 逐字相同**（Reviewer 對 parent 匯出跑同一案例）；損壞與不存在的訊息沿用既有 `ProvenanceError` |
| P3-a | online `ingestion_timestamp()` mutation（mock `fetch_raw`，真實 `load_api_key` 讀哨兵 `.env`，DB 先 seed） | 8 個：`…Z`、`….123456+08:00`、`+00:00`、naive、`''`、尾隨空白、`None`、`1758651890` | 8/8 exit 1，**raw JSON 沒有寫出、sidecar 沒有寫出、raw 目錄沒有建立**、DB 不變；訊息含 `from ingestion_timestamp()` 與格式；沒有哨兵 |
| P3-b | online，DB 路徑不存在 | `…Z` | exit 1，DB 沒有建立，raw 沒有寫出 |
| P3-c | online 正向對照 | patch 合格值 `2026-09-24T09:00:00+08:00`；不 patch（真實時鐘） | 兩者 exit 0；raw、sidecar、DB 都有寫入，`DB.ingestedAt == sidecar.acquiredAt`（真實時鐘：`2026-09-24T17:14:20+08:00`）。證明 P3-a 的拒絕確實發生在寫入之前，而不是 harness 本來就到不了寫入階段 |
| V-3 | 合格值經 CLI 與經 sidecar | OK-1、OK-2、OK-4、OK-5、OK-6 | 10/10 exit 0，`ingestedAt == 輸入` |
| F-1 重現 | 非 ASCII 數字 | CLI 與 sidecar：`２０２６-09-24T02:24:50+08:00`、`2026-09-24T02:24:5٠+08:00` | **4/4 exit 0，DB 存入原字串**（`isascii() == False`） |

Harness 總計：0 個非預期結果（F-1 重現段是刻意的探測）。Harness 對匯出目錄內提交的 `data.db` 前後 sha256 相同。

**Parent 對照（`cc29c7f`）**：N-1 的五個輸入在 parent 全部 exit 0 並原樣寫入（`''`、`'yesterday'`、`'2026-09-24'`、`'2026-09-24T02:24:50Z'`、sidecar `'not-a-time'`）。這表示 N-1 在 parent 確實可重現，而 subject 對這五個輸入全部 fail-closed。

## 3. H-3（資料語義與標示）— A-1 核對段

觸及類別：H-3。本 work item 改的是取得時間的驗證邏輯與 README 相關措辭（DR-22.4）。

| 核對項 | 結果 |
| --- | --- |
| DR-17 語義：取得時間＝「最後更新時間」 | **維持**。`ingestion_timestamp()`（`pipeline.py:36-42`）與「fetch 後取一次」的位置不變（`pipeline.py:128-129`）；驗證不會再讀時鐘，也不改值（`validate_acquisition_time` 回傳同一物件）。offline 路徑沒有任何時鐘呼叫；M3（offline 讀時鐘）→ 7 failed，M5（缺 sidecar 時退回時鐘）→ 2 failed |
| AT-1 型別 | 符合。`str()` 轉型已移除（`provenance.py:92-95`）；非字串一律拒絕並標出 JSON 型別（§2.1、P2-a） |
| AT-2 文法 | **不符合**：非 ASCII 十進位數字會被接受 → **F-1**。其餘文法邊界（offset、精度、分隔符、大小寫、空白、長度）都符合 |
| AT-3 曆法有效 | 符合（閏年、月／日／時／分／秒範圍；`:60`／`:61`／`T24`／`02-29`（非閏年）都被拒絕） |
| AT-4／AT-5／AT-6（不正規化、不截斷、不 trim） | 符合；mutant M-F（先 strip 再檢查）→ 2 failed，M-I（截掉小數秒）→ 3 failed |
| AT-7 不做合理性檢查 | 符合（validator 只用 `strptime`，不讀時鐘；`9999`／`2000` 年不受限制） |
| AT-8 三個套用點 | 符合（§2.2 P1、P2、P3） |
| AT-9 優先順序 | 符合（P1-c、P1-d；缺鍵時的訊息與 parent 相同） |
| AT-10 fail-closed | 符合（exit 1、`Ingestion failed:`、無 traceback、DB 沒有開啟也沒有寫入、offline 在 derive 前、online 在 `save_raw_json`／`write_provenance` 前）。測試對 offline 順序的鑑別力不足 → F-2（實作本身正確） |
| AT-11 訊息 | 符合：值（`repr`，超過 80 字元截斷並加 `...`）、來源標籤、格式與範例、CLI 的 hint |
| AT-12 原樣寫入 | 符合（V-3 10/10；online 的 sidecar 與 DB 是同一字串） |
| V-6 乾淨匯出重建（AC-12） | 符合（§5.3）：exit 0，`ingestedAt = 2026-09-24T02:24:50+08:00`，重建出的 `data.db` blob 與提交的 blob 相同 |
| README 措辭（DR-17 §4.5、DR-22.6） | 符合：`README.md:104-110, 118-124, 154-155` 仍說明這是「從 CWA 取得的時間」、offline 重建不會讓它看起來更新，沒有把它寫成 CWA 發布時間或頁面時間。新段落 `README.md:126-137` 列出了精確格式與範例、拒絕的類型（空值、只有日期、無 offset、`Z` 或其他 offset、小數秒、空白分隔）、fail-closed、不退回 sidecar、不做合理性檢查。**例外**：`README.md:130`「Anything else is **rejected**」在 F-1 存在時不成立 |
| 顯示面 | 兩個呈現層都原樣顯示 `ingestedAt`（`static/app.js:1067-1069`、`app.py:53-63`，本 diff 未改）。因此 F-1 情境下，非 ISO 字串會以「Last updated (data fetched from CWA)」出現在兩層 |

**H-3 結果**：F-1（AT-2 被違反，Medium，blocking）。其他規則與 DR-17 語義都成立。

## 4. H-1（憑證與機密）— A-1 核對段

觸及類別：H-1。本 diff 改動了 online 路徑所在的模組（`pipeline.py`，它呼叫讀取 `.env` 的 `load_api_key`），新增了錯誤訊息，也改了 README（DR-22.4）。

| 核對項 | 結果 |
| --- | --- |
| 訊息組成（AT-11） | `validate_acquisition_time` 的訊息只由 `_render(value)`、`source`、`REQUIRED_FORMAT`、`EXAMPLE`、可選的 `hint` 組成（`acquisition_time.py:114-123`）；三個呼叫點的 `source`／`hint` 都是字面字串或 sidecar 檔名（`pipeline.py:133-135, 167-171`；`provenance.py:92-95`）。沒有路徑會把 env、標頭或 raw JSON 帶進訊息 |
| **哨兵金鑰測試**（Reviewer 自跑） | 哨兵 `〔哨兵金鑰值已遮蔽 — R-SEC/H-1〕` 放在三處：(a) process 環境變數 `CWA_API_KEY`；(b) 匯出目錄的預設 `.env`；(c) online 案例的 `--env` 檔。online 案例由真實 `load_api_key` 讀入，mock 的 `fetch_raw` 會確認拿到的就是哨兵（不是的話 exit 97），所以產生失敗訊息時，金鑰確實在 process 記憶體裡。掃描全部失敗執行（P1 28 次、P2 23 次、P3 9 次）的 stdout＋stderr，檢查哨兵全文、片段 `5E171E1A`、`CWA_API_KEY`、`Authorization`：**0 筆**。online 正向對照也是 0 筆 |
| A-5：`git ls-files` | 沒有追蹤 `.env`（只有 `.env.example`） |
| A-5：追蹤檔案（`bd52ede`，542 檔） | 本機真實金鑰的字面值（在記憶體內比對，沒有印出）：**0 筆**。金鑰格式 pattern 只命中 6 個本 diff 未改動的檔案，而且命中的都是文件化的佔位字串 `CWA-1234-5678-90ab-cdef`（4-4-4-4 形，不可能是真金鑰；見 `tools/credential_scan.py` 的 allowlist 說明） |
| A-5：diff | `cc29c7f..bd52ede` 與 `bd52ede..b4b121f` 的新增行：沒有金鑰格式字串，沒有字面金鑰；`Authorization` 在新增行出現 3 次，都只是文字描述（DR-22 E-5、worklog）或測試斷言 `assert "Authorization" not in message` |
| A-5：專案 gate | `python -m tools.credential_scan` → exit 0（「542 tracked files; no .env tracked…; no CWA-key-format string in tracked files or committed history; no Authorization value in fixture/raw JSON」）；`tests/test_secrets.py` 4 passed（sidecar 仍在掃描對象內，`test_secrets.py:16`，未改）；CI run `35979067273` 的 credential step 同樣通過 |
| 紀錄 | worklog、DR-22 與本紀錄都不含金鑰；本紀錄只寫哨兵，沒有寫真實金鑰 |
| 設計上的回顯（不是 finding） | AT-11(a) 要求訊息原樣回顯不合格值。操作者如果誤把金鑰貼進 `--acquired-at`，stderr 會回顯（最多 80 字元）。這是 DA 裁決的行為，而且回顯的是操作者自己的輸入，不是從 env 或檔案洩漏。這裡只記錄，不列 finding |

**H-1 結果**：成立，沒有 finding。

## 5. DR-22.5(A) 整合重驗

### 5.1 Diff-scope／boundary — **成立**

- `git diff --name-only cc29c7f..bd52ede -- . ':(exclude)home_work_01/doc/governance/**'` → `README.md`、`doc/acceptance/ACCEPTANCE.md`、`doc/ticket/tickets.md`、`ingestion/acquisition_time.py`、`ingestion/pipeline.py`、`ingestion/provenance.py`、`tests/test_acquisition_time.py`，分別對應 B-5、B-6、B-7、B-3、B-1、B-2、B-4。`home_work_01/` 以外 0 檔（X-8）。record-only（B-8）：DR-22、worklog。
- **Blob 相同**（`git rev-parse cc29c7f:<p>` 與 `bd52ede:<p>` 比對，另以 `git hash-object` 核對兩個匯出與工作樹）：`data.db` `687586991ce3654e8b336b5b0a1616e98aa83a66`、`data/raw/F-D0047-091.json` `209eb767367de882030bbf54854696d47bd38086`、`data/raw/F-D0047-091.meta.json` `9edfd1182fa58082549510ade49958df36ae46e0`（X-2）；`derive.py`、`config.py`、`persist.py`、`fetch.py`、`checks.py`、`__main__.py`、`__init__.py`（X-1）；`server.py`、`app.py`、`weather_query.py`、`vercel.json`、`requirements.txt`、`.python-version`、`api/index.py`、`static/{app.js,index.html,styles.css}`（X-6）；tree `static`、`api`、`tests/fixtures`、`.github` 皆相同。
- `write_provenance` 在 diff 中未改（X-3）；online 正向對照寫出的 sidecar 仍是 `sourceDatasetId`、`acquiredAt`、`rawJson`、`note` 四欄，`note` 文字相同。
- 既有測試：`git diff --name-status cc29c7f..bd52ede -- home_work_01/tests` 只有 `A tests/test_acquisition_time.py`；collect 出的 test id，parent 164 個全部存在於 subject，新增的 75 個全部在新檔。
- DR-22.5 fail-safe：diff-scope 證明成立，本 R1 沒有 boundary finding，所以不觸發補充的 Spec Integration Audit instance（由 Orchestrator 機械判定）。

### 5.2 Invariants

- **INV-3**：每個不合格情境（P1-a..c、P2-a..c、P3-a..b）DB 的位元組、mtime 與內容都不變；DB 路徑不存在時也沒有被建立；online 失敗時 raw JSON 與 sidecar 都沒有寫出。成立。
- **INV-5**：§4。成立。
- **INV-4／H-2**：diff 未觸及，blob 相同（§6）。

### 5.3 Spec AC

- **AC-09、AC-11**：`test_ac09_negative_via_cli[5]`、`test_ac11_http_failure_via_cli[5]`、`test_ac11_timeout_via_cli` 在 subject 全部 PASSED，測試檔 blob 未變（`test_pipeline.py` `75b91ef…`）。
- **AC-12**（Reviewer 在乾淨匯出實跑）：新的 `git archive bd52ede` 匯出（沒有 `.env`），先**刪除** `data.db`，`CWA_API_KEY` unset，網路封鎖，執行 README 指令 `python -m ingestion --from-json data/raw/F-D0047-091.json` → exit 0，stderr 0 bytes，`Persisted 42 rows … (ingested at 2026-09-24T02:24:50+08:00)`。唯讀查詢：`IngestionMetadata = [(1, '2026-09-24T02:24:50+08:00', 'F-D0047-091')]`，兩張表，42 列。重建出的 `data.db` 的 `git hash-object` ＝ `687586991ce3654e8b336b5b0a1616e98aa83a66`，**與提交的 blob 相同**。
- **AC-24**：`data.db` blob 未變，沿用 `spec-SPEC-c1-r1.md` 的結論。**AC-25**：raw JSON blob 未變。
- **R-DOC-1／R-DOC-2**：§3 README 列（`README.md:130` 的例外歸入 F-1）。
- **AC-20／AC-21**：`gh run list --commit bd52ede…` → push run `35979067273` 與 PR run `35979071769` 都是 `completed/success`，headSha `bd52ede…`。push run 的 log：「239 passed in 4.68s」且 credential scan 通過。

### 5.4 DR-17 合規不回歸

- T-1..T-4：`test_t1_online_records_fetch_time_in_both_places`、`test_t2_offline_uses_provenance_not_clock`、`test_t2b_offline_explicit_acquired_at_overrides`、`test_t3_offline_without_acquisition_time_fails_closed`、`test_t4_provenance_record_is_key_free` 全部 PASSED，檔案未改。
- offline 不讀時鐘：M3 → 7 failed，M5 → 2 failed（兩個 mutant 都被抓到）。
- sidecar schema 與 `write_provenance` 的輸出不變（§5.1）。

### 5.5 全套離線測試

- Subject 乾淨匯出：`python -m pytest -q -p no:cacheprovider` → **239 passed**（4.54s）。
- Parent 乾淨匯出：**164 passed**（4.05s）。
- 239 ＝ 164 ＋ 75。既有 164 個測試全部保留，檔案逐位元未變，斷言沒有被弱化。

### 5.6 Work item DoD（Issue #29；DR-22.5(A)-5）

DR-22.3 規則與例值：除 AT-2（F-1）外都成立。README（DR-22.6.1）：成立，但有 F-1 例外。`ACCEPTANCE.md` §6 N-1 列（DR-22.6.2）：已改為「FIXED in #29」，並引用 DR-22、worklog、audit；AC 列未改。`tickets.md` #29 列：成立。worklog：成立。`--acquired-at` 的 metavar／help（DR-22.6.4）：成立。獨立 commit、不含 `static/**`：成立。commit 標記見 F-4。

## 6. H-2（老師指定介面）— 未觸及

diff 未觸及。`data.db`（`6875869…`）、`ingestion/config.py`（DDL，`7697f93…`）、`ingestion/persist.py`（`7872a6f…`）、`app.py`、`requirements.txt` 的 blob 在 parent 與 subject 之間相同。這裡只記為「diff 未觸及、blob 相同」，**不是**新的 PASS 主張。

## 7. 測試強度（verify-the-verification：mutation，每個 mutant 都是 subject 匯出的新副本）

| Mutant | 結果 |
| --- | --- |
| M-A 移除 CLI 驗證 | 12 failed |
| M-B CLI 不合格時退回 sidecar | 12 failed |
| M-C sidecar 恢復 `str()` 轉型、不驗證 | 12 failed |
| M-D 移除 online 驗證 | 1 failed |
| M-E online 驗證移到 `save_raw_json` 之後 | 1 failed |
| M-F 先 strip 再檢查（正規化） | 2 failed |
| M-G 移除 `strptime` 曆法檢查 | 7 failed |
| M-H `main` 不攔 `AcquisitionTimeError` | 25 failed |
| M-I 截掉小數秒 | 3 failed |
| **M-J CLI 驗證移到 derive 之後、persist 之前** | **239 passed（存活）** → F-2 |
| M3 offline 讀時鐘（DR-17） | 7 failed |
| M5 缺 sidecar 時退回時鐘（DR-17） | 2 failed |
| 修正探測：`_PATTERN` 加上 `re.ASCII` | 239 passed。F-1 的修正是有界的，現有測試不會因此失敗，但現有測試也完全沒有涵蓋 F-1 |

## 8. Findings

### F-1：Validator 接受非 ASCII 的 Unicode 十進位數字，違反 AT-2

- **Severity**：Medium　**Blocking**：**是**
- **契約依據**：DR-22 §3.3.1 規定「一個取得時間值合格，**若且唯若** AT-1～AT-7 全部成立」，並稱之為「Executor 實作、Reviewer 核對的唯一準則」。AT-2：「整個字串 MUST 恰為 `YYYY-MM-DDTHH:MM:SS+08:00`…（**ASCII 數字**；大寫 `T`；字面 `+08:00`；長度恰 25…）」。AT-10：不合格值 MUST fail-closed、不寫入。R-DB-5 要求 ISO 8601。DR-22.6.1 要求 README 誠實描述拒絕行為。
- **證據**：
  - `ingestion/acquisition_time.py:35`：`_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+08:00$")`，沒有 `re.ASCII`，也沒有用 `[0-9]`。Python 的 str pattern 中，`\d` 匹配全部 Unicode `Nd`。`acquisition_time.py:94` 的 `datetime.strptime(value, "%Y-%m-%dT%H:%M:%S%z")` 同樣接受這些數字（`int('２０２６') == 2026`）。`acquisition_time.py:32` 的註解寫「ASCII digits only」，但程式沒有做到。
  - Validator 探測（§2.1）：6 個含全形或阿拉伯-印度數字的值，`is_valid_acquisition_time` 全部回 `True`。
  - 真實 CLI（§2.2 F-1 重現）：`python -m ingestion --from-json <fixture> --db <tmp>/data.db --acquired-at "２０２６-09-24T02:24:50+08:00"` → **exit 0**，`IngestionMetadata.ingestedAt = '２０２６-09-24T02:24:50+08:00'`（`isascii() == False`）。sidecar `"acquiredAt": "２０２６-09-24T02:24:50+08:00"`（或 JSON 跳脫 `"２０２６-…"`）同樣 exit 0 並寫入。`2026-09-24T02:24:5٠+08:00` 也一樣。
  - 兩個呈現層原樣顯示該值（`static/app.js:1067-1069`、`app.py:53-63`），成為「Last updated (data fetched from CWA): ２０２６-09-24T02:24:50+08:00」。`README.md:130` 聲稱「Anything else is **rejected**」，與實際行為不符。
- **具體失敗情境**：維護者在中文輸入法的全形模式下輸入 `--acquired-at`，或從中文文件複製一個含全形數字的時間戳，接著重建 `data.db`。這個非 ISO 8601、不合 AT-2 的「最後更新時間」會被寫入並公開顯示。這正是 N-1 所描述的缺陷類別（「不合格值被接受並原樣寫入」），而本 work item 的整個 scope 就是關閉這類缺陷。
- **為何 blocking**：F-1 違反本 work item 核心接受準則的明文條款（AT-2「ASCII 數字」與「若且唯若」），落在高風險類別 H-3 的驗證邏輯上。若在此結案，等於把 AT-2 記為滿足，但實際並未滿足。F-1 不是契約不足：AT-2 的括號文字已經明確寫出 ASCII，實作自己的註解（`acquisition_time.py:32`）也宣稱只接受 ASCII，所以不需要 route DA。若修正方對這個解讀有異議，屬設計語義爭議，依治理 §4.3 先交 DA。
- **R2 的 closure 條件**（只描述要達成的結果，HOW 由 Executor 決定）：(1) 日期時間任何位置出現非 ASCII 數字，都會在 validator、CLI、sidecar 三處 fail-closed（exit 1、不寫入）；online 產生器天生只輸出 ASCII，不需另外處理。(2) 自動化測試至少涵蓋全形數字與另一種 Unicode `Nd`（例如阿拉伯-印度數字），分別在 validator 層與至少一條 CLI／sidecar 路徑上驗證。(3) 不回歸：全套測試、blob 相同、diff 仍在 allowlist 內。(4) `README.md:130` 的敘述與實際行為一致。修正探測顯示加上 `re.ASCII` 後全套仍是 239 passed。
- **A-3**：F-1 屬高風險類別 H-3。若之後有人考慮 deferral，MUST 另有 DA 確認（治理 §4.5）。

### F-2：測試沒有鑑別 offline 驗證「在讀 raw JSON／derive 之前」的順序（AT-10）

- **Severity**：Low　**Blocking**：否
- **契約依據**：DR-22 AT-10「offline：驗證 MUST 在讀取 raw JSON 與 derive **之前**完成」；V-1 的斷言。
- **證據**：mutant M-J 把 CLI 驗證移到 `derive_snapshot` 之後、`persist_snapshot` 之前，結果 **239 passed**。`tests/test_acquisition_time.py:206` 斷言 `"WeatherElement" not in (captured.out + captured.err)`，但 preview 本來就不會印出 `WeatherElement`，所以這個斷言無法鑑別順序；它的註解（`:205`）宣稱它能證明順序。
- **實作本身正確**：`pipeline.py:164-171` 的驗證在 `:172-178` 讀 JSON 與 derive 之前。Reviewer 的真實 CLI 對全部失敗案例都觀察到 stdout 為空，沒有 preview。INV-3 也仍然受保護，因為 M-J 下 DB 同樣不會被寫入。
- **Disposition**：可選的測試強化，例如在 V-1／V-2 斷言 `captured.out == ""`。這在 #29 自己的 B-4 範圍內，MAY 併入 F-1 的 targeted correction，但不是 R2 closure 的條件。Owner：Orchestrator 追蹤。

### F-3：文法檢查用 `re.match`＋`$`，本身不會拒絕尾隨 `\n`，要靠 `strptime` 補上；註解與 worklog 的描述不準確

- **Severity**：Low　**Blocking**：否
- **證據**：`acquisition_time.py:88` 用 `_PATTERN.match(value)`，而 `$` 可以匹配在尾隨 `\n` 之前，所以 `"2026-09-24T02:24:50+08:00\n"` 能通過正規表示式。這個值實際上仍被拒絕，是因為 `strptime` 會丟「unconverted data remains」（§2.1、P2-a 已確認拒絕）。註解 `acquisition_time.py:32-34`（「anchored, so any … trailing whitespace … fails」）與 worklog 第 32 行（「`re.fullmatch` 等效」）的描述都不準確。
- **影響**：目前行為正確。風險只在日後有人移除 `strptime`、只留文法檢查時才出現（M-G 會有 7 個測試失敗，其中包含 `trailing_nl`，所以測試仍會抓到）。
- **Disposition**：不需要行動。如果 F-1 的修正本來就要改 `acquisition_time.py:35` 這一行，Executor MAY 一併改用 `fullmatch`／`\Z`，並修正註解。Owner：Orchestrator 追蹤。

### F-4：受審 commit 帶有 Claude attribution 行，違反專案 git 規則

- **Severity**：Low　**Blocking**：否
- **契約依據**：root `CLAUDE.md:98`（「Commit message 與 PR description 都不加任何 Claude 標記：不寫 `Co-Authored-By: Claude`…此規則優先於工具預設的 attribution 提示」）；`docs/conventions/git-commit-rules.md:22`；Bindings §6「commit message 與 PR 描述不加 Claude 標記」。
- **證據**：`git log -1 --format=%B bd52ede` 的最後一行是 `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`。`b4b121f` 與 `cc29c7f` 也有；更早的 `5d8b169`、`5136bd2`…`6407d8b` 都沒有。這三個 commit 已經 push 到 `origin/home_work_01-hw10-implementation`。
- **為何 non-blocking**：這不影響 DR-22 的接受準則，也不影響程式行為或 invariants。
- **Disposition**：Orchestrator 在之後的 commit 停止加這一行。已 push 的歷史要不要改寫是 RB-6，保留給 acceptor；本 audit 不要求改寫。合併時如何處理 commit message 也由 acceptor 決定（RB-1）。

### F-5：#29 的 binding 核對尚未寫入 worklog 或 run record

- **Severity**：Low　**Blocking**：否（紀錄完整性，record-only 路徑）
- **契約依據**：Bindings §3.4（核對結果以「agentId＋observed model／effort」寫進 worklog 或 audit record 的 binding 欄位）；DR-22 §3.1 末段（Executor 是 `gov-executor` subagent 還是主 session direct execution，擇一並記錄 binding）；DR-22 §5「Orchestrator run record：記錄本派工與 binding」；治理 §4.6。
- **證據**：在 HEAD `b4b121f`，`home_work_01/doc/governance/run/` grep `#29|acquired-at-validation|DR-22` 為 0 筆；worklog `20260924-acquired-at-validation.md` 沒有 Executor 的 agentId 與 observed model／effort，也沒有寫 Executor 是 subagent 還是 direct execution。
- **Disposition**：Owner：Orchestrator。在 #29 結案 bookkeeping 前，補記 Executor 與本 Reviewer 派工的 binding 核對。這些都是 `doc/governance/**` record-only 路徑，不影響 subject identity。

### 觀察（不是 finding）

- O-1：`ingestion_timestamp()` 如果被改壞、回傳非字串，訊息會標成「(JSON null)」等 JSON 型別（`acquisition_time.py:47-61`），但 online 來源不是 JSON。這只是措辭，只有產生器被改壞時才會出現，而且仍然 fail-closed。
- O-2：worklog 的 C-1 以「DR-22 §0 C-1」與 Issue #29 連結引用 acceptor 授權。DR-22 §0 已逐字保存授權原文，符合 C-1「或引用本節」。authorization 的確認由 Orchestrator 負責，本 audit 不代為確認。

## 9. Routing／authority

- F-1：Executor targeted correction 後進 R2（治理 §4.4）。F-1 不是契約不足，不需要 DA；若修正方對 AT-2 的解讀有異議，交 DA。
- F-4：已 push 歷史的任何處置屬 acceptor（RB-6／RB-1）。
- F-5：Orchestrator（record-only）。
- 沒有 boundary finding；不需要 Final Adjudicator。

## 10. 結論

- 三個套用點的 fail-closed 行為、INV-3、INV-5、H-1、DR-17 不回歸、diff-scope／blob 相同、AC-12 byte-identical 重建、CI 綠、164 → 239 且未弱化：全部成立。
- DR-22.3 AT-2 的「ASCII 數字」條款不成立：非 ASCII 的 Unicode 十進位數字能通過 validator，並經 CLI 與 sidecar 寫入 `IngestionMetadata.ingestedAt`（F-1，Medium，blocking）。
- Non-blocking：F-2、F-3、F-4、F-5 已列出 disposition 與 owner，不延長本 cycle。

VERDICT: BLOCKING (F-1)


> [Orchestrator R-SEC 遮蔽 2026-09-24] 上文原本寫出 A-4 H-1 測試用的哨兵金鑰字面值（CWA 格式，非真實金鑰）。為避免 tracked 內容含 CWA-金鑰格式字串觸發機械式 credential scan（`tools.credential_scan`；H-1／R-SEC-1），已將該字面值改為遮蔽佔位符。Reviewer 的 finding 與 verdict 不變。
