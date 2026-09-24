# Audit record：Issue #18，cycle 1，R2

| 欄位 | 內容 |
| --- | --- |
| Work Contract | GitHub Issue #18（`yotsubamomo/aiot-classwork`）Ingestion，MVM。所屬 Spec：`home_work_01/doc/spec/SPEC.md` v1.1。Outcome Contract：`home_work_01/doc/governance/outcome-contract.md`（ACCEPTED）。裁決依據：`decision-20260923-spec-interpretation-rulings.md`（DR-3/4/5/6/10/15/16）、`decision-20260923-high-risk-categories.md`（A-1、A-5）、**DR-17** `decision-20260924-ingestion-timestamp-semantics.md`。 |
| 受審 subject | branch `home_work_01-hw10-implementation`，commit **`7ee299c462ea778824b5360af531ac882d197983`**，為 `693c12b` 的 targeted correction。審查範圍 `693c12b..7ee299c`，共 12 個檔案，全部位於 `home_work_01/` 內。 |
| Audit 種類 | **R2**（scoped closure review，治理 §4.4），**cycle 1**；前一輪為 R1 `issue-18-c1-r1.md`，結論 BLOCKING (F-1, F-2)。 |
| 角色 | `primary_reviewer`（`gov-primary-reviewer`；mapping `claude-opus-5-5`／`xhigh`） |
| Binding 證據 | 由派工者依 Bindings §3.4 核對，記錄於 run record `home_work_01/doc/governance/run/run-20260924-hw01-formal.md`。 |
| Independence | 本輪延續 Reviewer 自己的 R1 context（治理 §2.3(1)），未繼承 Executor 的 context。依規定先從磁碟重讀修正後的檔案與 `git diff 693c12b..7ee299c`，也讀了 DR-17 紀錄全文。Executor 在 worklog §9 的敘述（含其自報的 mutation 結果）只當作待驗證的主張，全部由 Reviewer 獨立重做。本紀錄由 Reviewer 以自己的 Write 工具寫入。 |
| 範圍 | 只審以下三項：(1) R1 blocking finding 是否真正解決；(2) 修正是否引入回歸；(3) 修正直接產生或暴露的 defect，含 DR-17 合規性（依 DR-17 §9，在本 cycle 內作為審後變更驗證）。本輪不做第二次全面審查。新發現的 non-blocking finding 不延長 cycle。 |
| 日期 | 2026-09-24 |

## 1. 方法與環境

- **Subject 識別**：`git rev-parse HEAD` = `7ee299c…`；`git diff 7ee299c -- home_work_01` 為空；staged／unstaged diff 皆為空。DR-17 紀錄、R1 紀錄與 run record 目前都是未追蹤檔（record-only path，Bindings §7），不屬於受審 subject。
- **離線套件**：以 `git archive 7ee299c home_work_01` 匯出到 Reviewer scratchpad。匯出目錄沒有 `.env`，另以 `sitecustomize` 封鎖 socket 連線與 DNS，並設定無效的 proxy。使用 Python 3.12.14 執行 `pytest -v` → **60 passed**（R1 時為 38）。
- **Mutation probe**：在 scratchpad 複本上建立 9 個 mutant，逐一跑整個套件；repo 本身沒有任何改動。
- **Reviewer 自寫的 CLI harness**：以 mock HTTP 與形似金鑰的假金鑰測試 12 種 AC-11 失敗模式，並測試 offline 路徑的不良輸入。
- **資料一致性檢查**：用 R1 的獨立推導程式重算新 `data.db`，並從乾淨匯出做 offline 重建。
- **A-5 掃描**：在程序內讀取被忽略的 `.env`，只輸出命中次數，不輸出金鑰內容。

## 2. R1 blocking findings 的 closure

### F-1：「丟棄開頭不完整日」的分支現在有測試實際執行 → **RESOLVED**

- 新增 `tests/conftest.py::make_leading_incomplete`：把真實擷取中 `2026-09-24T00:00` 那一段的起始時間改標為 `2026-09-23T18:00`，使 09-23 成為只有夜間段的開頭日，也就是 brief §4.5 所記「18:00 之後擷取」的版面。
- 新增 `tests/test_derive.py:59` `test_drops_incomplete_leading_day_and_keeps_seven`，斷言：42 列、視窗為 09-24…09-30、不含 09-23、結果與未變體的輸出完全相同。
- **Mutation bar（Reviewer 獨立執行）**：M1 刪除 `derive.py:150-151`（修正後的行號，即 R1 所指的 149-150）→ **1 failed, 59 passed**，失敗的正是上述測試。
- 這個測試直接對應 AC-08 的「擷取開頭的不完整日期被丟棄」、R-TC-1（R-DER-3）與 Spec §5.1 的邊界要求。

### F-2：AC-09 與 AC-11 的失敗案例改由 CLI 入口斷言 → **RESOLVED**

- **AC-09**：`test_pipeline.py:105` `test_ac09_negative_via_cli` 以參數化涵蓋五個反例（缺縣市、缺半天、無效值、只剩六天、不連續）。每個反例都先寫入一份快照，再經 `pipeline.main --from-json` 執行，斷言 `exit == 1`，且 `snapshot_signature`（全部資料列加上中繼資料）不變。
  - 指名縣市與日期的斷言仍在 derive 層的測試（`test_derive.py:121-168`）。
  - offline 路徑不會讀取金鑰，因此這裡沒有「輸出不含金鑰」的議題。
- **AC-11**：`test_pipeline.py:143` 涵蓋 401、404、500、503 與非 JSON 回應；`:159` 涵蓋逾時。每一項經 online CLI 路徑，使用寫在暫存 `.env` 的哨兵金鑰，斷言 `exit == 1`、快照不變、stdout 與 stderr 都不含哨兵金鑰。除逾時外，也斷言沒有寫出 raw JSON。
- **Mutation bar（Reviewer 獨立執行）**：

| Mutant | 內容 | 結果 |
| --- | --- | --- |
| M2 | 讓 `pipeline.py:228` 不再攔截 `FetchError` | **6 failed**（全部 AC-11 CLI 測試） |
| M7 | 已攔截的失敗改回傳 0 | **12 failed**（5 個 AC-09 與 6 個 AC-11 CLI 測試，外加 T-3） |
| M8 | 把金鑰串進 HTTP 錯誤訊息 | **5 failed**（4 個 AC-11 CLI 測試與原本的 `test_error_message_never_leaks_key`） |
| M9 | offline 路徑在 derive 之前先寫入 DB | **5 failed**（全部 AC-09 CLI 測試） |

- Reviewer harness 另外確認：401、404、500（HTML）、502、503、Timeout、ConnectTimeout、ConnectionError、200 非 JSON、`success=false`、錯誤 `resource_id`、JSON 陣列本體，共 12 種，全部 exit 1、DB 不變、輸出不含金鑰、沒有寫出 raw JSON。

## 3. 回歸與修正引入的變更（含 DR-17）

### 3.1 回歸檢查

- 60 個測試全數通過。R1 原有的 38 個測試仍在，其斷言沒有被弱化。`test_offline_rerun_from_saved_json` 只多傳一個 `--acquired-at` 參數，這是 DR-17 的要求。
- `persist.py`、`config.py`、DDL、fixture 與 R-DER 規則都沒有改動。`derive.py` 只有兩處變更：`_value` 新增 `is_finite` 判斷，以及一段註解。
- 修正後的 `data.db` 資料列與 `693c12b` 的 `data.db` **逐列相同**，只有 `IngestionMetadata.ingestedAt` 由 `01:49:18` 改為 `02:24:50`。

### 3.2 DR-17 合規核對

| DR-17 條款 | 判定 | 證據 |
| --- | --- | --- |
| §4.1／§4.2 online：在 fetch 驗證通過時讀一次時鐘，同一個值寫入 sidecar 與 DB | **符合**（測試證據的缺口見 N-2） | `pipeline.py:127-137`：`fetch_raw` 回傳後立即取 `acquired_at`，同一個變數傳給 `write_provenance` 與 `persist_snapshot`，persist 時不再讀時鐘。T-1 在 `test_pipeline.py:208`。 |
| §4.3(1)(2) offline：值來自 sidecar 或明確參數，不讀時鐘 | **符合** | `pipeline.py:153-154`，offline 函式內沒有任何時鐘呼叫。T-2、T-2b 位於 `test_pipeline.py:231`、`:250`。Mutant M3（offline 改讀時鐘）→ T-2 與 T-2b 失敗。 |
| §4.3(3) 缺少取得時間時，寫入前即 fail-closed | **符合**（不良值的情況見 N-1） | `provenance.read_acquisition_time` 在 sidecar 不存在、無法解析、或 `acquiredAt` 為空時丟出 `ProvenanceError`，由 `main` 轉成 exit 1。T-3 在 `test_pipeline.py:265`。Mutant M5（缺 sidecar 時退回讀時鐘）→ T-3 失敗。Reviewer 另以損壞的 sidecar 測試：exit 1，訊息指名該檔。 |
| §4.4 不改動 raw JSON；sidecar 位於單元目錄、不含金鑰、與 raw JSON 一起提交 | **符合** | raw JSON 在 `693c12b` 與 `7ee299c` 之間 blob 相同，也等於 `json.dumps(indent=2, ensure_ascii=False)` 的輸出（1,695,726 bytes，22 個縣市，15 個要素）。sidecar `data/raw/F-D0047-091.meta.json` 已提交，欄位為 `sourceDatasetId`、`acquiredAt`、`rawJson`、`note`，不含金鑰（A-5 #4）。T-4 在 `test_pipeline.py:280`；`test_secrets.py` 的掃描對象已納入 sidecar。 |
| §4.4 從乾淨 checkout 可重現提交的 `data.db` | **符合** | 從乾淨匯出（無 `.env`、網路封鎖）執行 `python -m ingestion --from-json data/raw/F-D0047-091.json`：exit 0，資料列、`IngestionMetadata` 與 `sqlite_master` 三者都與提交的 `data.db` 相同，`ingestedAt` 為 `2026-09-24T02:24:50+08:00`。 |
| §7 I-4：以一次 online 重跑產生一致的提交集合 | **符合** | `data.db.ingestedAt` 與 sidecar `acquiredAt` 都是 `2026-09-24T02:24:50+08:00`，`sourceDatasetId` 一致，格式為 ISO 8601 含 `+08:00`、精確到秒。工作樹中 raw JSON、sidecar、`data.db` 三者的 mtime 同為 `02:24:50`，commit 時間為 `02:28:13`，佐證同一次 online run 寫出三個檔案。raw JSON 與 01:39 的擷取逐位元組相同，這與 E-5（回應本體不含時間）一致。worklog §9.1 記有此次 online 取得，且不含金鑰。 |
| §7 I-3：README | **符合** | README 的 ingestion 段新增：取得時間、sidecar 的位置與內容、offline 重建不會更新「last updated」、缺少時間時 fail-closed、`--acquired-at` 選項。 |

### 3.3 以新資料集合重新建立 R1 的資料證據（DR-17 §9）

| 項目 | 判定 | 證據 |
| --- | --- | --- |
| AC-05 | **PASS** | 新 `data.db` 中 `sqlite_master` 的 DDL 與 `REQUIREMENTS.md` A.3 逐字相同；PRAGMA 為五欄且型別正確；只有 `TemperatureForecasts` 與 `IngestionMetadata` 兩張表，沒有索引。老師的兩句 SQL：`SELECT DISTINCT regionName` 回 6 列；`WHERE regionName = '中部地區'` 回 7 列，日期為 2026-09-24…30，格式皆為 `YYYY-MM-DD`。 |
| AC-08 | **PASS** | 對提交的 raw JSON 做獨立推導，結果與新 `data.db` 相同，共 42 列。fixture 沒有改動，四組手算期望值仍然有效，60 個測試中含這些斷言且全部通過。 |
| AC-25（產物） | **PASS** | raw JSON 完整且為縮排格式，不含金鑰（同 §3.2）。online 摘要與預覽的程式碼除新增一行 provenance 輸出外沒有改動。 |
| AC-07(c) | **PASS** | 字面金鑰與 CWA 格式（8-4-4-4-12）的命中數：`7ee299c` 樹內 420 個追蹤檔案為 0；diff `693c12b..7ee299c` 為 0；diff `d42b1a7..7ee299c` 為 0；`git log --all -p` 為 0；staged／unstaged 為 0。寬鬆 regex 仍只命中 `tests/test_secrets.py` 的測試字面值（R1 F-7，已分派給 #22）。 |
| AC-07(d) | **PASS** | fixture、raw JSON、sidecar、`data.db` 四個檔案中：`Authorization` 為 0、`Authorization` 值為 0、字面金鑰為 0、金鑰格式為 0。 |
| A-5 #1 | **PASS** | `git ls-files` 中除 `home_work_01/.env.example` 外沒有 `.env`。 |
| Evidence 檔 | **PASS** | worklog、DR-17、run record、R1 紀錄與 commit message 的字面金鑰與金鑰格式命中數都是 0。 |

## 4. 受修正影響的高風險類別核對（A-1）

- **H-1 憑證與機密**：修正涉及新的 sidecar 檔、新的 CLI 選項 `--acquired-at`、新的 `ProvenanceError` 訊息（只含路徑）、JSON 本體非物件時的錯誤訊息，以及 AC-11 的 CLI 測試。核對方式：A-5 全套重跑、12 種 HTTP 失敗的輸出掃描、mutant M8。結果：零外洩；「輸出不含金鑰」現在有測試證據，且 mutant M8 證明這項測試能抓到外洩。**無 H-1 finding。**
- **H-2 老師指定介面**：`data.db` 已重新產生。核對 DDL 逐字、老師的兩句 SQL、五欄的型別、表的數量，並比對資料列與 `693c12b` 相同。結果：全部符合，`TemperatureForecasts` 沒有改動。**無 H-2 finding。**
- **H-3 資料語義與標示**：
  - 推導規則：保留規則現在有測試證據（M1）；NaN、Infinity、-Infinity 會以指名縣市與日期的錯誤失敗（M6 → 3 failed）；資料值未改變。
  - 「最後更新時間」的語義依 DR-17 核對，online 與 offline 都符合（M3、M5 能被測試抓到）；README 的 sidecar 說明誠實描述了此值是取得時間。
  - 結果：沒有 blocking。新發現的 **N-1**（Medium，non-blocking）與 **N-2**（Low）見第 5 節。

## 5. 新 findings（修正直接產生或暴露；皆 non-blocking，不延長 cycle）

### N-1：offline 路徑不檢查取得時間的格式，空字串也照寫

- **Severity**：Medium　**Blocking**：否
- **契約依據**：R-DB-5 規定 ingestion 時間為 ISO 8601 並含 `+08:00`。DR-17 §4.1 規定此值為 ISO 8601、`+08:00`、至少精確到秒。DR-17 §4.3(3) 規定缺少取得時間時必須 fail-closed，且不得以推測值代替。
- **證據**：Reviewer 以 CLI 實測，下列輸入全部 exit 0，並把原字串寫進 `IngestionMetadata.ingestedAt`：

| 輸入 | 寫入的值 |
| --- | --- |
| `--acquired-at ''` | `''` |
| `--acquired-at yesterday` | `'yesterday'` |
| `--acquired-at 2026-09-24` | 只有日期，沒有時間與時區 |
| `--acquired-at 2026-09-24T02:24:50Z` | UTC 時間，不是 `+08:00` |
| sidecar 內 `acquiredAt` 為 `not-a-time` | `'not-a-time'` |

  - 原因：`pipeline.py:153` 只判斷 `acquired_at is None`；`provenance.py:82` 只判斷值是否為空。
  - 兩條路徑的行為不一致：sidecar 的空值會 fail-closed，CLI 明確傳入的空值卻會被寫入。例如 shell 變數未設定時執行 `--acquired-at "$ACQ"`，就會寫進空的「最後更新時間」。
- **為何不列為 blocking**：
  - 只有在維護者對 override 介面傳入錯誤值、或手動改壞 sidecar 時才會發生。
  - 主要路徑都產生合格的值：online 路徑、以及由程式寫出的 sidecar。
  - 提交的交付物已驗證合格：`data.db` 與 sidecar 的值都是 `2026-09-24T02:24:50+08:00`，而且可以從乾淨 checkout 重現。
  - 因此殘餘風險是日後維護操作可能寫入格式不合的標示值，不影響已接受的交付物。
- **Disposition**：
  - 建議：在寫入前驗證值符合 ISO 8601、含 `+08:00`、精確到秒，不合格時與 T-3 相同方式 fail-closed。
  - Owner：Orchestrator，依治理 §4.3 追蹤。是否歸入 #25，或在 #18 結案後以單點修正處理，由 DA／Orchestrator 決定；若採後者，依 high-risk decision A-4 必須做 independent audit。

### N-2：T-1 的時鐘是常數，無法偵測 online 路徑「重讀時鐘」的退化

- **Severity**：Low　**Blocking**：否
- **契約依據**：DR-17 §4.2(1) 規定只取一次時間；§4.6 T-1。
- **證據**：mutant M4 讓 online 路徑在 persist 時再呼叫一次 `ingestion_timestamp()`，結果 **60 passed**。原因是 `test_pipeline.py:218` 把時鐘 patch 成常數，每次呼叫都得到同一個值。
- 實作目前正確：只取一次時間，並以同一個變數傳遞（`pipeline.py:128`、`:130`、`:136`）。
- **Disposition**：可改用每次呼叫都遞增的假時鐘。Owner：Orchestrator 追蹤，與 N-1 一併處理即可。

### N-3：F-8 測試的日期變換實際上是輪轉，不是平移一週；另有一段 helper docstring 與實作不符

- **Severity**：Low　**Blocking**：否
- **證據**：
  - `test_pipeline.py:182-188` 依序套用 `shift_day`，最後一步把 `10-01` 改為 `10-08`，而這些 10-01 的時段本來就是由 09-24 平移而來。因此結果的視窗是 10-02…10-08，且 09-24 的值被移到 10-08（Reviewer 驗證：北部 10-08 等於原本的 09-24）。註解卻寫「Shift the whole fixture forward one week」。
  - 這個測試仍能證明整份替換（42 列、日期全部為新），所以 F-8 的 closure 不受影響。R1 時 Reviewer 已另外以真正平移 +7 天的 fixture 驗證過。
  - `test_pipeline.py:122-124` 的 docstring 宣稱回傳 5-tuple，實際只回傳 3 個值。
- **Disposition**：屬於測試可讀性問題。Owner：Orchestrator 追蹤，可選處理。

### N-4：raw JSON 不存在且也沒有 sidecar 時，錯誤訊息只提到缺少 provenance

- **Severity**：Low　**Blocking**：否
- **證據**：`pipeline.py:153-154` 先讀 provenance，所以檔案不存在時回報的是「no acquisition-time provenance found」，沒有指出 raw JSON 本身不存在。
  - 仍是 fail-closed：exit 1，不寫入。
  - 有提供 `--acquired-at` 時，則正確回報「raw JSON not found」。
- **Disposition**：Owner：Orchestrator 追蹤，可選處理。

### N-5：online run 若在 derive 階段失敗，工作樹中的 raw JSON 與 sidecar 已換成新擷取，但 `data.db` 仍是舊快照

- **Severity**：Low　**Blocking**：否
- **證據**：寫檔順序為 `pipeline.py:129-130`（raw JSON 與 sidecar）先於 `:134` 的 derive。
  - 先存 raw JSON 的順序在 R1 就已存在並被接受。
  - DR-17 §4.4 要求提交的 raw JSON 與 sidecar 必須能重現提交的 `data.db`。在上述情況下，只要維護者不提交失敗後的工作樹，這項要求就仍然成立。
- **Disposition**：可在 README 註明「online 失敗後不要提交 `data/raw/`」，或改用先寫暫存檔、成功後再替換的做法。Owner：#25（README 實跑與 AC-12）。

## 6. R1 中由 #18 負責的 Low findings

| R1 finding | 狀態 | 證據 |
| --- | --- | --- |
| F-3（NaN／Infinity） | **已處理** | `derive.py:227` 以 `is_finite` 排除；`test_derive.py:169` 以參數化測試 NaN、Infinity、-Infinity、abc，斷言錯誤指名縣市與日期；mutant M6 → 3 failed。 |
| F-4（traceback 路徑） | **已處理** | `fetch.py:95` 擋下非物件的 JSON 本體（harness：exit 1，訊息為「not a JSON object (got list)」）；offline 路徑檔案不存在或非 JSON 時回報明確錯誤，exit 1、DB 不變。訊息措辭的殘餘問題見 N-4。 |
| F-5（unreachable 註解） | **已處理** | `derive.py:86-88` 改寫為說明理由的防禦性 post-condition。保留這段防禦碼的處置可以接受。 |
| F-8（AC-06 fixture 層級） | **已處理** | `test_pipeline.py:177` 經 CLI 以改動日期的 fixture 驗證整份替換。測試的註解與實際變換不符，見 N-3。 |
| F-6、F-7、F-9、F-10、F-11 | 不屬於本 cycle | 依派工說明與 R1 的 disposition，繼續由各自 owner（#19、#22、#25）追蹤。 |

## 7. 流程備註（不是 finding）

- DR-17 紀錄 `decisions/decision-20260924-ingestion-timestamp-semantics.md`、R1 紀錄與 run record 目前在工作樹中都是未追蹤檔。它們屬於 record-only path，不影響受審 subject 的識別（Bindings §7）。依 Bindings §3.5(4)，由派工者原樣提交。

## 8. 結論

- F-1、F-2 都已真正解決，兩者的 mutation bar 經 Reviewer 獨立重跑確認：刪除 `derive.py:150-151` 會使測試失敗；不再攔截 `FetchError` 會使 6 個 AC-11 CLI 測試失敗。
- 沒有發現回歸。
- DR-17 的 online、offline、fail-closed、sidecar 與可重現性要求都符合。R1 中綁定在舊資料上的證據（AC-05、AC-08、AC-25、AC-07(c)(d)、A-5）已對新的提交集合重新建立，結果都成立；`data.db.ingestedAt` 等於 sidecar 的 `acquiredAt`（`2026-09-24T02:24:50+08:00`），且 sidecar 不含金鑰。
- 修正產生或暴露的新問題 N-1～N-5 都判定為 non-blocking，owner 與 disposition 已列在第 5 節。

VERDICT: CLOSURE
