# Worklog — Ingestion 取得時間格式驗證（#29，#18 R2 N-1）

- **Work item**：[Issue #29](https://github.com/yotsubamomo/aiot-classwork/issues/29)（Lightweight，POST-BASELINE ENHANCEMENT）
- **Lane／boundary／驗證接受準則／H-3**：`doc/governance/decisions/decision-20260924-acquired-at-validation.md`（**DR-22**）
- **來源 finding**：`doc/governance/audit/issue-18-c1-r2.md` §5 N-1（Medium，non-blocking）
- **不變契約**：DR-17（取得時間＝「最後更新時間」語義）；R-DB-5（`+08:00`）；INV-2/3/5；不改 Spec／Outcome Contract／已提交 `data.db`／sidecar／DDL。

## Outcome Contract（acceptor 授權，DR-22 §0 C-1）

本 work item 的 Outcome Contract 為 acceptor 2026-09-24「Taiwan Map 視覺重做」指示中一併給出的授權（acceptor 於本 session 的 genuine chat 指示，非僅 scratchpad 抄本）：**授權 #18 R2 N-1（`--acquired-at` 格式驗證）作為「另一個」獨立的 Lightweight work item——獨立票、A-4 independent audit、不與地圖票混在同一 commit。** 不合併（RB-1）、不提交（RB-2）保留給 acceptor。C-1 由 Orchestrator 依 acceptor 的 genuine 指示確認為已授權，無 authorization gap。

## DR-22 驗證接受準則（Executor 依此實作）

合格 iff 字串 **完全符合** `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+08:00$` **且**為真實曆法瞬間（月/日/時/分/秒範圍、閏年）。offset 必為 `+08:00`（`Z` 與其他 offset 一律拒絕，不正規化）；精確到秒（小數秒拒絕，不截斷）；大寫 `T`、無空白分隔、不 trim；不做未來/範圍檢查（會讀時鐘，DR-17 §4.3(2)）。

- 三個套用點：CLI `--acquired-at`（只要有給，含 `''`；失敗**不** fallback sidecar）、sidecar `acquiredAt`（被讀時）、online `ingestion_timestamp()` 輸出（於 `save_raw_json`／`write_provenance` 前驗證）。
- fail-closed：exit 1（`Ingestion failed:`），不開/寫 DB，訊息含引號包住的不合格值＋來源（`--acquired-at`／`<raw>.meta.json` 的 `acquiredAt`／`ingestion_timestamp()`）＋要求格式；不含金鑰/env/header（H-1）。合格值逐字存。
- 合格例：`2026-09-24T02:24:50+08:00`、`2026-09-24T01:39:31+08:00`、`2026-01-01T00:00:00+08:00`、`2026-12-31T23:59:59+08:00`、`2028-02-29T12:00:00+08:00`。
- 不合格例（finding 五種 + NG-6..NG-14）：`''`、`yesterday`、`2026-09-24`、`2026-09-24T02:24:50Z`、sidecar `not-a-time`；naive、`+0800`、其他 offset、小數秒、空白/小寫、前後空白、不存在日期、非字串 JSON。

## Allowlist（DR-22.2）

`ingestion/pipeline.py`、`ingestion/provenance.py`、至多一個新 validator 模組、`tests/**`（只強化）、README ingestion 段、`ACCEPTANCE.md` §6 N-1 列、`tickets.md`、`doc/governance/**`。**Out**：`derive.py`／`config.py`／`persist.py`／`fetch.py`、已提交 `data.db`／raw JSON／sidecar（blob 須與 parent 逐位元組相同）、sidecar schema、任何正規化、任何合理性/時鐘檢查、`/api`／dashboard／`static`、Spec/OC/DR-17、workflows、N-2..N-5、合併/提交。

## 執行紀錄

**環境**：branch `home_work_01-hw10-implementation`，parent `cc29c7f`（tree clean）。測試用專案 pin 的 `.venv` Python 3.12.14（`home_work_01/.venv/Scripts/python.exe`），`pytest` 由 `pytest.ini`（`pythonpath=.`, `testpaths=tests`）驅動。全程離線、未讀 `.env`。

### 實作（DR-22.2 allowlist 內）

- **Validator（新模組，B-3）**：`ingestion/acquisition_time.py`
  - `is_valid_acquisition_time(value)`：AT-1 型別（`isinstance str`）→ AT-2 文法（`re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+08:00", re.ASCII).fullmatch(value)`：`re.ASCII` 使 `\d` 只限 ASCII `[0-9]`、`fullmatch` 比對整串，非 ASCII 數字與尾隨換行都在 pattern 階段被拒）→ AT-3 曆法有效（`datetime.strptime(value, "%Y-%m-%dT%H:%M:%S%z")`，pattern 已固定 offset 與精度）。三者皆成立才 True。不讀時鐘、不正規化。（初版誤用 Unicode `\d`＋`re.match`＋`$`，於 A-4 R1 修正，見「Targeted correction（R1）」。）
  - `validate_acquisition_time(value, *, source, hint=None)`：合格回傳**原字串**（AT-12）；不合格丟 `AcquisitionTimeError`，訊息＝值（`repr`，>80 截斷，AT-11(a)）＋來源（AT-11(b)，非字串另附 `_json_type`）＋要求格式與例（AT-11(c)），選擇性 `hint`。訊息只由值/來源/格式組成，無金鑰/env/header（H-1）。
- **三個套用點（AT-8）**：
  1. **CLI `--acquired-at`**：`ingestion/pipeline.py` `run_offline`，`acquired_at is not None`（含 `''`）時 `validate_acquisition_time(..., source="--acquired-at", hint="omit --acquired-at to read the provenance sidecar instead")`，**在讀 raw JSON／derive 之前**；失敗**不** fallback sidecar（AT-9）。
  2. **sidecar `acquiredAt`**：`ingestion/provenance.py` `read_acquisition_time`，改為「缺鍵 → 既有 `ProvenanceError`（訊息不變，AT-9）」＋「有鍵 → `validate_acquisition_time(record["acquiredAt"], source="the <raw>.meta.json 'acquiredAt' field")`」；移除舊 `str(acquired_at)` 轉型（AT-1）。
  3. **online `ingestion_timestamp()`**：`pipeline.py` `run_online`，取值後 `validate_acquisition_time(..., source="ingestion_timestamp()")`，**在 `save_raw_json`／`write_provenance` 之前**（AT-10）。
- **Fail-closed 連線**：`main` 的 except tuple 加入 `AcquisitionTimeError` → 既有 `Ingestion failed:` 前綴、stderr、exit 1、不開/寫 DB（無 traceback）。
- **argparse**：`--acquired-at` metavar 改 `YYYY-MM-DDTHH:MM:SS+08:00`、help 寫出精確文法與「不 fallback sidecar」（DR-22.6.4）。
- **文件**：README ingestion 段補「Acquisition-time format」段（精確格式、拒絕類型、fail-closed、不 fallback；保留 DR-17 §4.5「取得時間＝last updated、offline 重建不更新」語義）；`ACCEPTANCE.md` §6 N-1 列改 FIXED in #29；`tickets.md` #29 列狀態與 DR-22 引用。

### Self-verification（實測，全部離線）

- **Validator 單元（V-8）＋三套用點（V-1..V-6）**：新增 `tests/test_acquisition_time.py`，**75 passed**。涵蓋：OK-1..OK-6 接受且原字串回傳；INVALID_STRINGS 20 種（NG-1..NG-13＋非閏年 2/29、13 月）拒絕，訊息含值＋`--acquired-at`＋格式；NG-14 非字串 6 種（number/float/bool/null/object/array）拒絕且訊息含 JSON 型別；CLI 11 種不良值經 `pipeline.main` → exit 1、`snapshot_signature` 不變、stderr 含值與來源、無 raw body；sidecar 不良字串 6 種＋非字串 6 種 → exit 1、快照不變、訊息含 `resp.meta.json`＋`acquiredAt`／JSON 型別；缺鍵 sidecar 保留舊 `has no 'acquiredAt' value` 訊息（AT-9）；OK 值經 CLI 與 sidecar 各 6 種 → exit 0、`ingestedAt == 輸入`；優先順序（不良 CLI＋合格 sidecar → exit 1 不 fallback；合格 CLI＋不良 sidecar → exit 0 寫 CLI 值）；online `ingestion_timestamp()` 真值合格、patch 微秒/日界仍為秒精度合格、patch 成 NG-4 → exit 1 且 raw/sidecar/DB 皆未寫、無哨兵金鑰；提交 sidecar 值合格。
- **INV-3**：每個 fail 情境 `snapshot_signature` 逐位不變（測試斷言）。**INV-5／H-1**：新訊息與 README 無金鑰；online fail-closed 哨兵掃描（見下）零外洩。
- **DR-17 T-1..T-4**：`pytest -k "t1 or t2 or t3 or t4"` → **5 passed**（t1/t2/t2b/t3/t4），未改動、未弱化。
- **全套離線基線**：parent `cc29c7f` **164 passed**；本 work item 後 **239 passed**（164＋75），既有 164 全數保留、斷言未弱化（僅新增檔案，未改既有測試）。
- **H-1 哨兵掃描**：對 CLI／sidecar／online 三路的失敗訊息掃描 → 無 `CWA-xxxx…` 金鑰格式、無 `Authorization`、無 `CWA_API_KEY` token；online 帶哨兵 `.env` 的 bad-timestamp run 輸出**不含**哨兵（唯一命中出現在我把哨兵字串「當成 `--acquired-at` 輸入」時的回顯，屬操作者自帶輸入，非 env 外洩）。
- **AC-12 clean-export 重建**：從乾淨副本（無 `.env`、`sitecustomize` 封鎖 `connect`/`getaddrinfo`/`create_connection`）跑 `python -m ingestion --from-json data/raw/F-D0047-091.json` → exit 0、42 列、兩表、`IngestionMetadata.ingestedAt = 2026-09-24T02:24:50+08:00`；重建 `data.db` blob `687586991ce3654e8b336b5b0a1616e98aa83a66` 與**提交值逐位元相同**。提交 sidecar 值在新規則下合格。
- **Diff-scope／blob 不變**：working-tree tracked diff 僅 `README.md`、`doc/acceptance/ACCEPTANCE.md`、`doc/ticket/tickets.md`、`ingestion/pipeline.py`、`ingestion/provenance.py`；新增 untracked `ingestion/acquisition_time.py`、`tests/test_acquisition_time.py`、本 worklog、DR-22 decision（record-only）。全部落在 DR-22.2 B-1..B-8 allowlist；X-1/X-2/X-6/X-8 未觸及。`data.db`（`687586991…`）、raw JSON（`209eb76…`）、sidecar（`9edfd11…`）三個 blob 與 parent `cc29c7f` 相同（`git hash-object` 核對）。

### Subject 與 CI

- **Subject SHA**：`bd52ede140233a9c4c5b568ffaf9ead1620a6ce0`（branch `home_work_01-hw10-implementation`，parent `cc29c7f`）。
- **Diff-scope（`git diff --name-only cc29c7f..bd52ede`，排除 `doc/governance/**`）**：`README.md`、`doc/acceptance/ACCEPTANCE.md`、`doc/ticket/tickets.md`、`ingestion/acquisition_time.py`、`ingestion/pipeline.py`、`ingestion/provenance.py`、`tests/test_acquisition_time.py` — 全數落在 DR-22.2 B-1..B-7 allowlist。record-only（B-8）：DR-22 decision、本 worklog。`data.db`/raw JSON/sidecar 三個 blob 在 `cc29c7f` 與 `bd52ede` 之間相同（`687586991…`／`209eb76…`／`9edfd11…`）。
- **CI**：push run `35979067273` 與 PR run `35979071769` 皆 **success**（headSha `bd52ede`，offline test suite + credential checks / Python 3.12）。
- **狀態**：Executor 完成，DONE。未合併（RB-1）、未提交（RB-2）。closure 由 A-4 independent audit（fresh `gov-primary-reviewer` R1，涵蓋 DR-22.5(A) 整合重驗）判定；本紀錄不自證 closure。

## A-4 R1 findings — disposition (Orchestrator)

- **R1 verdict**：`audit/issue-29-c1-r1.md` = **BLOCKING (F-1)**（reviewer `afd86af32279b362c`，binding `gov-primary-reviewer`／`claude-opus-5-5`／`xhigh`，§3.4 通過）。F-1 = validator 的 `\d` 收 Unicode 數字（全形 `２０２６` 被接受），違反 DR-22 AT-2「ASCII digits only」。
- **F-1（blocking）＋ F-2／F-3（Low，同 footprint）**：交 Executor targeted correction（`re.ASCII`／`re.fullmatch`、offline-order 測試、comment/README 更正）。
- **F-4（Low，process）**：commits `cc29c7f`、`bd52ede`、`b4b121f` 帶 `Co-Authored-By: Claude` trailer，違反 CLAUDE.md:98（該規則優先於工具 attribution 提示）。成因：Orchestrator 誤依 session attribution reminder。**Disposition（acceptor 2026-09-24 裁定）：leave for squash-merge** — 不改已 push 歷史（RB-6 destructive git 保留），後續所有 commit 一律不加任何 Claude 標記；合併 PR #27 時由 acceptor squash-merge，trailer 不進 `main`。已修正 Orchestrator 與 Executor 後續行為。
- **F-5（Low，record）**：#29 binding 核對（§3.4，全部對照 model-profile-default-v2.2 通過）：
  - Design Authority `a50b4ef41f367d729` = `gov-design-authority`／`claude-fable-5-1`／`xhigh`（DR-22 作者）
  - Executor `a068f9df30c34349e` = `gov-executor`／`claude-opus-4-8`／`high`
  - Primary Reviewer（R1，R2 續派）`afd86af32279b362c` = `gov-primary-reviewer`／`claude-opus-5-5`／`xhigh`

## Targeted correction（R1）

A-4 R1 audit（`doc/governance/audit/issue-29-c1-r1.md`，VERDICT: BLOCKING F-1）後的 targeted correction。只動 DR-22.2 allowlist（`ingestion/acquisition_time.py`、`tests/**`、README、註解）；驗證契約、三個套用點、`data.db`/raw/sidecar blob 皆不變。

- **F-1（BLOCKING）— ASCII 數字**：`ingestion/acquisition_time.py` 的 pattern 從 `re.compile(r"^\d{4}-...$")`（Unicode `\d`）改為 `re.compile(r"\d{4}-...\+08:00", re.ASCII)`。原因：Python `\d` 匹配任意 Unicode 十進位數字，且 `int()`/`strptime %Y` 接受全形/阿拉伯-印度數字，故 `--acquired-at "２０２６-09-24T02:24:50+08:00"` 原本被接受並寫入，違反 AT-2「ASCII 數字」。修正後 6 種非 ASCII 數字變體（全形年/月/日/秒、阿拉伯-印度年、天城體年）在 pattern 階段即被拒。
  - 證據：`test_non_ascii_digits_rejected_by_validator`（validator 層 6×）、`test_non_ascii_digits_fail_closed_via_cli`（CLI 6×：exit 1、快照不變、訊息含 `--acquired-at`）、`test_non_ascii_digits_fail_closed_via_sidecar`（sidecar 6×：exit 1、快照不變、訊息含 `resp.meta.json`）。
- **F-3（Low）— 尾隨換行**：`_PATTERN.match(value)`＋`$` 會讓 `"...+08:00\n"` 溜過 regex（僅 strptime 抓到）。改用 `fullmatch`（無 `^`/`$`，整串比對），使 regex 本身即拒尾隨換行與任何尾綴；~L32 註解「ASCII digits only」與本 worklog「`re.fullmatch`」措辭於修正後為真。
  - 證據：`test_pattern_rejects_trailing_newline`（`_PATTERN.fullmatch("...\n") is None`）；既有 `trailing_nl` 反例仍拒。
- **F-2（Low，新增測試）— offline 驗證先於讀 raw JSON**：新增 `test_cli_validation_precedes_raw_json_read`：不良 `--acquired-at "yesterday"` ＋不存在的 raw JSON 路徑 → 必須以 acquisition-time 錯誤（來源 `--acquired-at`）失敗，而非「raw JSON not found」。**Mutant 驗證**：把 `validate_acquisition_time` 移到 `json.loads` 之後，該測試 **FAILED**（訊息變 `raw JSON not found`）；還原後 PASSED。既有斷言全部保留、未弱化。
- **README**：ingestion 段「rejected」清單補「ASCII `0`-`9`（拒全形/其他 Unicode 數字）」與「尾隨空白/換行」。

### 驗證（R1 correction，全部離線）

- 全套離線：**259 passed**（前一 subject 239＋新增 20：非 ASCII 3×6＝18、pattern 換行 1、ordering 1）；既有 239 全保留、未弱化。DR-17 T-1..T-4 仍綠。
- Blob 不變：`data.db`（`687586991…`）、raw JSON（`209eb76…`）、sidecar（`9edfd11…`）與 parent `cc29c7f` 逐位相同。
- Diff-scope：僅 `ingestion/acquisition_time.py`、`tests/test_acquisition_time.py`、`README.md`（＋本 worklog record-only）；落在 B-1..B-8 allowlist，`home_work_01/` 外零變更。

- **Correction subject SHA**：`ee8448060be4204d87d938718d0b8b9719b69e2d`（parent `cc29c7f`；前一 subject `bd52ede`）。commit message 無任何 Claude attribution（CLAUDE.md:98 / git-commit-rules）。
- **Diff-scope（`git diff --name-only cc29c7f..ee84480`，排除 `doc/governance/**`）**：`README.md`、`doc/acceptance/ACCEPTANCE.md`、`doc/ticket/tickets.md`、`ingestion/acquisition_time.py`、`ingestion/pipeline.py`、`ingestion/provenance.py`、`tests/test_acquisition_time.py` — 全數 B-1..B-7 allowlist；R1 correction 實際只動 `acquisition_time.py`、`tests/test_acquisition_time.py`、`README.md`（＋本 worklog record-only）。`data.db`/raw JSON/sidecar 三 blob 與 `cc29c7f` 逐位相同（IDENTICAL）。
- **CI**：push run `35982002167` 與 PR run `35982005624` 皆 **success**（headSha `ee84480`）。
- **狀態**：R1 targeted correction 完成，DONE。未合併（RB-1）、未提交（RB-2）。closure 由 R2 判定；本紀錄不自證 closure。`doc/governance/audit/issue-29-c1-r1.md`（Primary Reviewer 自寫，record-only）保留原樣由派工者提交，Executor 未改寫。

## Closure

A-4 ladder：R1 = BLOCKING(F-1 non-ASCII 數字) → R1 targeted correction（`ee84480`：`re.ASCII`+`fullmatch`、offline-order 測試、comment/README）→ **R2 = AUDIT CLOSURE**（`audit/issue-29-c1-r2.md`）。final subject `ee84480`；259 pytest 綠、CI 綠、data.db/raw/sidecar blobs 不變、clean-export AC-12 重現、H-3/H-1 維持。R2 獨立複核三個 binding 皆符。phase 增補：`decisions/phase-acceptance-SPEC-addendum-20260924-acquired-at-validation.md`（DR-22 §5(B)）。STOP：不合併（RB-1）、不提交（RB-2）。
