# Audit record — Issue #29，cycle 1，R2（A-4 independent audit，closure review）

| 欄位 | 內容 |
| --- | --- |
| Work Contract | GitHub Issue **#29**「Ingestion 取得時間格式驗證（#18 R2 N-1）」。Outcome Contract＝acceptor 2026-09-24 直接指示（DR-22 §0）。Governing decision：**DR-22** `doc/governance/decisions/decision-20260924-acquired-at-validation.md`（接受準則 DR-22.3 AT-1..AT-12；boundary DR-22.2；assurance DR-22.4／DR-22.5(A)）。不變契約：DR-17、R-DB-5、INV-3、INV-5、H-1、H-3、A-1、A-4、A-5。 |
| 前一輪 | R1 `doc/governance/audit/issue-29-c1-r1.md`，subject `bd52ede`，**VERDICT: BLOCKING (F-1)**；non-blocking F-2、F-3、F-4、F-5。 |
| 受審 subject | branch `home_work_01-hw10-implementation`；correction subject **`ee8448060be4204d87d938718d0b8b9719b69e2d`**。派工內容寫成 `ee84480060be…`（41 字元，多一個 `0`）；本 audit 以唯一可解析的 `ee84480` → `ee8448060be4204d87d938718d0b8b9719b69e2d` 為準，這也與 worklog 記載一致。git parent＝`b4b121f`；R1 subject `bd52ede`；工作 base `cc29c7f`。HEAD `def4597`：`git diff --name-only ee84480..def4597` 只有 worklog（record-only）。 |
| Audit 種類 | **R2**（治理 §4.4 closure review），**cycle 1**。範圍限於：(1) R1 blocking 是否真正解決；(2) 修正是否引入回歸；(3) 修正直接產生或暴露的 blocking defect。不做第二次全面審查。 |
| 角色 | `primary_reviewer`（definition `gov-primary-reviewer`；Bindings §3.1 `claude-opus-5-5`／`xhigh`）。R2 依 Bindings §3.5(1) 延續本 Reviewer 的 R1 context，但以下證據全部從磁碟與新的匯出重新取得。 |
| Binding 證據 | 派工者已記入 worklog「A-4 R1 findings — disposition」段（F-5）。本 Reviewer 另依 Bindings §3.4 的方法，唯讀核對 harness 紀錄 `~/.claude/projects/D--nchu-2026-AIoT-git-repository-aiot-classwork/e802a74c-…/subagents/`：`a50b4ef41f367d729` = `gov-design-authority`／`claude-fable-5-1`／`xhigh`；`a068f9df30c34349e` = `gov-executor`／`claude-opus-4-8`／`high`（這也是做 correction 的 Executor，是唯一提到 `ee84480`／`re.ASCII` 的 `gov-executor` transcript）；`afd86af32279b362c` = `gov-primary-reviewer`／`claude-opus-5-5`／`xhigh`。三者都符合 Bindings §3.1，沒有 `diversity_lost`。 |
| Independence | (1) 未繼承 Executor 的 context；worklog 的「259 passed」「mutant FAILED」「Diff-scope」「IDENTICAL」等主張都自行重驗。(2) Binding 見上一列。(3) 自己用 `git archive ee84480` 做新的乾淨匯出（`pr29r2_subj`、`pr29r2_h1`、`pr29r2_ac12`，各 161 檔，沒有 `.env`），用 Python 3.12.14 跑測試、真實 CLI、探測、mutation、A-5、`gh run`。(4) 本紀錄由 Reviewer 以自己的 Write 工具寫入。 |
| 日期 | 2026-09-24 |

## 1. 修正內容（自讀 `git diff bd52ede..ee84480`）

- 變更檔：`ingestion/acquisition_time.py`、`tests/test_acquisition_time.py`、`README.md`，加上 worklog（record-only）。`ingestion/pipeline.py`、`ingestion/provenance.py`、`doc/acceptance/ACCEPTANCE.md`、`doc/ticket/tickets.md` 的 blob 與 `bd52ede` 相同，所以三個套用點的呼叫方式、訊息 hint 與 `main` 的攔截都沒有改變。
- `acquisition_time.py`：`_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+08:00", re.ASCII)`（`:40`），套用點由 `_PATTERN.match(value)` 改為 `_PATTERN.fullmatch(value)`（`:93`）；module docstring（`:3-7`）與註解（`:34-39`）同步更正。`validate_acquisition_time` 的訊息組成程式碼（`:117-128`）未改。
- 測試：只在檔尾新增（`git diff bd52ede..ee84480 -- home_work_01/tests` 刪除行數＝0）。新增 20 個：`test_non_ascii_digits_rejected_by_validator`、`_fail_closed_via_cli`、`_fail_closed_via_sidecar` 各 ×6（全形年／月／日／秒、阿拉伯-印度年、天城體年），`test_pattern_rejects_trailing_newline`，`test_cli_validation_precedes_raw_json_read`。
- README `:126-139`：補「The digits must be ASCII `0`-`9` (a full-width or other Unicode digit is rejected)」，拒絕清單也加上「non-ASCII digits, and any surrounding whitespace (including a trailing newline)」。

## 2. R1 blocking finding

### F-1（非 ASCII 數字被接受，違反 AT-2）— **已解決**

逐一對照 R1 定下的 closure 條件：

1. **三處都 fail-closed**
   - **Pattern 層**（`pr29r2_probe_pattern.py`；把 module 內的 `datetime` 換成 spy 來記錄 `strptime` 呼叫）：12 種非 ASCII 數字變體全部 `fullmatch=None`、`is_valid=False`、`validate` 丟錯，**`strptime` 一次都沒有被呼叫**。這 12 種是全形年／月／日／秒／時、阿拉伯-印度年／分／秒、天城體年、孟加拉日、泰文年、數學粗體數字 `U+1D7CE`。所以 `int()`／`strptime` 已經不會看到非 ASCII 數字。
   - **真實 `python -m ingestion`**（`pr29r2_cli_nonascii.py`）：派工列出的 6 種，加上 R1 重現值 `2026-09-24T02:24:5٠+08:00`，共 7 種，每種都走 CLI、sidecar、CLI（DB 不存在）、sidecar（DB 不存在）四條路徑，**28/28 都通過**。每個案例都確認：exit 1；stderr 以 `Ingestion failed: invalid acquisition time` 開頭；沒有 traceback；stdout 為空；訊息有來源標籤（`from --acquired-at`，或 `resp.meta.json` 的 `'acquiredAt' field`）、`repr(值)` 與格式；seeded DB 的 sha256、mtime 與內容都不變；DB 不存在時沒有被建立；沒有哨兵金鑰。
   - 範例 stderr：`Ingestion failed: invalid acquisition time '２０２６-09-24T02:24:50+08:00' from --acquired-at: expected exactly YYYY-MM-DDTHH:MM:SS+08:00 (e.g. 2026-09-24T02:24:50+08:00); omit --acquired-at to read the provenance sidecar instead`。
   - R1 harness 的 F-1 重現段在 `ee84480` 上：CLI 與 sidecar 的 `２０２６…`、`…5٠…` 全部 exit 1，沒有寫入任何值（R1 時是 exit 0 並寫入）。
2. **測試涵蓋**：validator、CLI、sidecar 三層各有 6 個變體，至少涵蓋全形與另外兩種 Unicode `Nd`，符合 R1 的 closure 條件。
   - Mutation R2-M1（拿掉 `re.ASCII`）→ **9 failed**，三個新測試函式各有 3 個失敗。
   - 只有 9 個是因為 Python `strptime` 的 `%m`／`%d`／`%S` 要求第一個字元是 ASCII，所以月、日、秒變體即使沒有 `re.ASCII` 也會被拒；真正依賴 `re.ASCII` 的是「年」的三種變體。守護強度仍足夠。
3. **沒有回歸**：R1 的 validator 探測矩陣在 `ee84480` 上是 **65/65 OK、0 BAD**。這 65 個是 8 個合格值、46 個不合格字串（含 R1 的 6 個非 ASCII）與 11 個非字串。8 個合格值（OK-1..OK-6、`2000-02-29…`、提交的 sidecar 值）仍被接受，且 `validate_acquisition_time` 回傳同一個物件（`r is v`）。AT-3 的曆法檢查仍會被執行：`02-30`、`T24`、`13-01` 會到達 `strptime` 並被拒絕。
4. **README 一致**：`README.md:126-139` 現在的敘述與實際行為一致。

## 3. R1 non-blocking findings 的修正核對

### F-3（`re.match`＋`$` 讓尾隨 `\n` 通過 pattern）— **已解決**

- `:93` 改為 `fullmatch`；pattern 裡沒有 `^`、`$`；`_PATTERN.flags & re.ASCII` 成立。
- Spy 探測：`…+08:00\n`、`\r\n`、尾隨空白、前導空白都在 pattern 階段被拒，**不會到達 `strptime`**。
- 註解 `acquisition_time.py:34-39`、docstring `:3-7`，以及 worklog 的實作段（「`re.compile(r"…", re.ASCII).fullmatch(value)`：`re.ASCII` 使 `\d` 只限 ASCII `[0-9]`、`fullmatch` 比對整串」）現在都與程式一致。
- **觀察 R2-O1（Low，non-blocking，不延長 cycle）**：`test_pattern_rejects_trailing_newline` 直接對 `_PATTERN.fullmatch` 做斷言，沒有鎖住套用點。Mutation R2-M2 把 `:93` 改回 `_PATTERN.match(value)` 後仍然 **259 passed**。這時 pattern 變成前綴比對，尾綴改由 `strptime` 拒絕，所以對外行為仍然正確，這只是測試鑑別力的問題。**Disposition**：可選的測試強化，例如用 spy 斷言 `strptime` 沒有被呼叫，或對 `is_valid_acquisition_time("…+08:00XYZ")` 以外的套用方式做斷言。Owner：Orchestrator 追蹤。F-3 本身已解決。

### F-2（沒有測試鑑別 offline 驗證在讀 raw JSON 之前）— **已解決**

- 新測試 `test_cli_validation_precedes_raw_json_read`：不良的 `--acquired-at yesterday` 加上不存在的 raw JSON，斷言 exit 1、快照不變、訊息含 `--acquired-at` 與 `'yesterday'`，且**不含** `not found` 與 `raw JSON`。
- Shipped 順序：這個測試 PASSED。直接跑 CLI 得到 `Ingestion failed: invalid acquisition time 'yesterday' from --acquired-at: …`，DB 沒有被建立。
- Mutation：R2-M4（CLI 驗證移到 `json.loads` 的 try/except 之後）→ 全套 **1 failed**，就是這個測試，直接跑 CLI 得到 `Ingestion failed: raw JSON not found: …`。R2-M5（R1 存活的 M-J：移到 derive 之後、persist 之前）→ 同樣 **1 failed**。R1 找到的測試缺口已經補上。

### F-4（三個已 push 的 commit 帶 `Co-Authored-By: Claude`）— **disposition 充分**

- worklog 記載 acceptor 2026-09-24 的裁定：「leave for squash-merge」，不改寫已 push 的歷史（RB-6），後續 commit 都不加標記。
- 本 audit 核對：`ee84480`、`def4597` 的 commit message 中 `Co-Authored-By: Claude`／`Generated with` 為 **0 筆**。
- 已 push 歷史的處置權屬 acceptor（RB-6／RB-1）；本 finding 是 Low，本 audit 不要求改寫。
- **提醒 acceptor（不是 finding）**：GitHub squash merge 的預設 commit message 會帶入被 squash 的 commit 訊息，也會保留 co-author trailer。要讓「trailer 不進 `main`」成立，acceptor 合併時需要手動編輯 squash message。

### F-5（#29 binding 核對未記錄）— **disposition 充分**

- worklog「A-4 R1 findings — disposition」段已記錄 DA、Executor、Primary Reviewer 三個 agentId 與 observed model／effort。本 Reviewer 已依 Bindings §3.4 從 harness 紀錄獨立核對，結果一致（見表頭 Binding 證據）。

## 4. 回歸與契約完整性（治理 §4.4 第 2 項）

| 項目 | 結果 |
| --- | --- |
| 全套離線測試（`ee84480` 乾淨匯出） | **259 passed**（5.10s）。collect 出的 259 個 test id 包含 parent 的 164 個與 `bd52ede` 的 239 個，一個都沒少；新增 20 個全部在 `test_acquisition_time.py`。239＋20＝259，與 worklog 相符 |
| DR-17 T-1..T-4 | 5/5 PASSED（t1、t2、t2b、t3、t4）；`tests/test_pipeline.py` 的 blob `75b91ef…` 未變 |
| 三個套用點（R1 harness 在 `ee84480` 重跑） | **68/68 OK、0 BAD**：CLI 21 個不良值、DB 不存在 ×4、不退回 sidecar ×3、CLI 合格＋sidecar 不合格 ×1、sidecar 16 個不良值、DB 不存在 ×3、缺鍵／非 dict／損壞／不存在 ×4（訊息與 parent 相同）、V-3 合格值 ×5（CLI＋sidecar）、online mutation ×8、DB 不存在 ×1、online 正向對照 ×2。與 R1 結果完全相同 |
| Diff-scope（`cc29c7f..ee84480`，排除 `doc/governance/**`） | `README.md`、`doc/acceptance/ACCEPTANCE.md`、`doc/ticket/tickets.md`、`ingestion/acquisition_time.py`、`ingestion/pipeline.py`、`ingestion/provenance.py`、`tests/test_acquisition_time.py`，7 檔都在 B-1..B-7；`home_work_01/` 以外 0 檔 |
| Blob 相同（`cc29c7f` 對 `ee84480`） | `data.db` `687586991ce3…`、raw JSON `209eb767367d…`、sidecar `9edfd1182fa5…`；另以 `git hash-object` 核對匯出檔，三者相同。`derive.py`、`config.py`、`persist.py`、`fetch.py`、`checks.py`、`__main__.py`、`__init__.py`、`server.py`、`app.py`、`weather_query.py`、`vercel.json`、`requirements.txt`、`.python-version`、`api/index.py`、`tests/fixtures/*`、`test_secrets.py` 的 blob 相同；tree `static`、`api`、`tests/fixtures`、`.github` 相同 |
| AC-12（新匯出、沒有 `.env`、`CWA_API_KEY` unset、網路封鎖、先刪除 `data.db`） | exit 0，stderr 0 bytes；`IngestionMetadata = [(1, '2026-09-24T02:24:50+08:00', 'F-D0047-091')]`，42 列；重建出的 `data.db` 的 `git hash-object` ＝ `687586991ce3654e8b336b5b0a1616e98aa83a66`，**與提交的 blob 相同** |
| CI | `gh run list --commit ee8448060be4…`：push `35982002167` 與 PR `35982005624` 都是 `completed/success`。push log：「259 passed in 3.82s」，credential scan 通過 |

## 5. H-3（資料語義與標示）— A-1 重述

- AT-2 現在成立：只接受 ASCII 數字，並比對整個字串。AT-1、AT-3..AT-12 未變且仍成立（§2、§4）。
- DR-17 語義（取得時間＝「最後更新時間」、online 只取一次、offline 不讀時鐘、不正規化、原樣寫入）未變：`pipeline.py`、`provenance.py` 的 blob 與 `bd52ede` 相同，T-1..T-4 為綠。
- README 措辭：新增的敘述準確；DR-17 §4.5 的語義段落（`README.md:104-124, 156-157`）未改。
- AC-12 byte-identical 重建。
- **結果**：H-3 成立，沒有 blocking。

## 6. H-1（憑證與機密）— A-1 重述

- 訊息組成程式碼（`acquisition_time.py:117-128`）未改，只由值、來源、格式與 hint 組成。
- 哨兵 `〔哨兵金鑰值已遮蔽 — R-SEC/H-1〕` 放在 process env、匯出目錄的預設 `.env` 與 online 的 `--env` 檔。online 路徑確實由真實 `load_api_key` 讀入它。R1 harness 的 68 項檢查與非 ASCII 的 28 次執行，stdout＋stderr 都**不含**哨兵全文、片段、`CWA_API_KEY` 或 `Authorization`。
- A-5（`ee84480`，542 個追蹤檔）：沒有追蹤 `.env`；本機真實金鑰的字面值 0 筆；金鑰格式 pattern 只命中文件化的佔位字串（6 個未改動的檔案）。`cc29c7f..ee84480`、`bd52ede..ee84480`、`ee84480..def4597` 的新增行都沒有金鑰格式字串，也沒有字面金鑰。`python -m tools.credential_scan` exit 0；CI 的 credential step 通過。
- worklog 與本紀錄都不含金鑰。
- **結果**：H-1 成立。

H-2：diff 未觸及。`data.db`、`config.py`、`persist.py` 的 blob 相同；只記錄為未觸及，不是新的 PASS 主張。

## 7. 修正直接產生或暴露的新問題（治理 §4.4 第 3 項）

- 沒有新的 blocking defect。
- R2-O1（Low，non-blocking；§3 F-3 段）：依治理 §4.4，新的 non-blocking finding 不延長 cycle。

## 8. 紀錄與 routing 備註

- R1 紀錄 `doc/governance/audit/issue-29-c1-r1.md` 在 HEAD `def4597` 的工作樹中仍是**未追蹤**檔案。內容就是本 Reviewer 寫入的最終版本（檔尾 `VERDICT: BLOCKING (F-1)`）。依 Bindings §3.5(4)，派工者須原樣 commit R1 與本 R2 紀錄，才能做 closure bookkeeping。
- 不需要 DA、Final Adjudicator 或 Alternate Review。F-4 對已 push 歷史的任何處置仍屬 acceptor（RB-6／RB-1）。
- Audit closure 不豁免治理 §3.8 的其他完成條件，也不涵蓋 DR-22.5(B) phase-acceptance 增補；後者由 Orchestrator 產出。

## 9. 結論

- F-1 已真正解決：非 ASCII 數字在 pattern 階段就被拒絕，validator、CLI、sidecar 三處都 fail-closed，而且有測試守護。
- F-2、F-3 在程式與測試上都已解決；R2-O1 只是可選的測試強化。
- F-4、F-5 的 disposition 充分。
- 沒有回歸：259 passed、blob 相同、boundary 成立、AC-12 byte-identical、CI 綠、H-1 與 H-3 成立。

VERDICT: AUDIT CLOSURE


> [Orchestrator R-SEC 遮蔽 2026-09-24] 上文原本寫出 A-4 H-1 測試用的哨兵金鑰字面值（CWA 格式，非真實金鑰）。為避免 tracked 內容含 CWA-金鑰格式字串觸發機械式 credential scan（`tools.credential_scan`；H-1／R-SEC-1），已將該字面值改為遮蔽佔位符。Reviewer 的 finding 與 verdict 不變。
