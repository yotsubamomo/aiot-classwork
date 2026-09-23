# Audit record — Issue #22，cycle 1，R1

| 欄位 | 內容 |
| --- | --- |
| Work Contract | GitHub Issue #22（`yotsubamomo/aiot-classwork`）「自動化測試整合與 GitHub Actions CI／smoke workflow」，Scope class ENHANCED REQUIRED。所屬 Spec：`home_work_01/doc/spec/SPEC.md` v1.1（R-TC-5、R-TC-6、R-TC-7、R-ENV-3、R-SEC-1（CI 自動化）、R-DOC-1（測試與 CI 段）、§5.3；AC-20、AC-21、AC-22、AC-29、AC-07(b–d 自動化)；INV-5、INV-8；AB-16、AB-17）。Outcome Contract：`home_work_01/doc/governance/outcome-contract.md`（ACCEPTED 2026-09-23；§8.2 第 2 項為 RB-5 授權原文）。適用裁決：`decision-20260923-spec-interpretation-rulings.md` DR-12、DR-13；`decision-20260923-high-risk-categories.md` H-1、A-1、A-5；`decision-20260924-unattended-run-policy.md` N-11、N-21。分配依據：`derivation-SPEC.md` §11.1 的 #22 列（AC-22 的重跑另分配給 #25）。 |
| 受審 subject | branch `home_work_01-hw10-implementation`，HEAD **`88b871e01cd436d13710243693dcc36bc58039d2`**；程式與 workflow 的 subject 為 **`84060c9`**（`84060c9..88b871e` 只改 `home_work_01/doc/governance/worklog/issue-22.md`，屬 record-only path，Bindings §7）；BASE `a7ecdd9`。範圍 `a7ecdd9..88b871e`，7 個檔案：`.github/workflows/home_work_01-ci.yml`、`.github/workflows/home_work_01-smoke.yml`（兩者在 repo root）、`home_work_01/README.md`、`home_work_01/smoke.py`、`home_work_01/tools/__init__.py`、`home_work_01/tools/credential_scan.py`、`home_work_01/doc/governance/worklog/issue-22.md`。 |
| Audit 種類 | **R1**（對 accepted work scope 做完整的 independent audit），**cycle 1**。這是 Ticket audit，不是 Spec Integration Audit（Bindings §5 不採用單 Ticket fast path）。 |
| 角色 | `primary_reviewer`（definition `gov-primary-reviewer`；Bindings §3.1 mapping 為 `claude-opus-5-5`／`xhigh`） |
| Binding 證據 | 由派工者（Orchestrator）依 Bindings §3.4 核對，記在 run record `home_work_01/doc/governance/run/run-20260924-hw01-formal.md`。該 run record 記載的 Executor binding：agent `adebd2ac56ad6ccce` = `gov-executor`／`claude-opus-4-8`／`high`。Executor 與 Primary Reviewer 的 mapping 是不同模型，沒有 `diversity_lost`。 |
| Independence（治理 §2.3） | (1) 以 fresh context 派工，沒有繼承 Executor 的對話；worklog `worklog/issue-22.md` 與派工內容中的敘述一律當作待驗證的主張（派工內容說「兩個 workflow 都以 `paths` 過濾」，實際上 smoke workflow 沒有 `paths`，見 O-1）。(2) Binding 見上一列。(3) 自主取得：Reviewer 自己讀 Ticket 本文（`gh issue view 22`）、Spec、Outcome Contract §8.2、derivation record、DR-12／DR-13、H-1／A-5 裁決、unattended-run policy、#18／#21 audit records 中分派給 #22 的項目、git 歷史與 diff、兩個 workflow 檔、四個 CI run 的完整 log，並自己執行測試、掃描、sandbox 反例、smoke 與 GitHub API 查詢。(4) 本紀錄由 Reviewer 用自己的 Write 工具寫入。 |
| 日期 | 2026-09-24（Reviewer 的線上查詢與 smoke 時間為 2026-09-23T22:05Z–22:15Z，即 +08:00 的 2026-09-24 06:05–06:15） |

## 1. 審查方法與環境

- **確認 subject**：`git rev-parse HEAD` = `git ls-remote origin home_work_01-hw10-implementation` = `88b871e01cd4…`。`git diff --quiet 84060c9 88b871e -- . ':!home_work_01/doc/governance'` 成立，所以兩者在 record-only path 以外相同。`git diff --stat 88b871e -- home_work_01 ':!home_work_01/doc' .github` 為空，工作樹的實作與 subject 相同。`git status --short` 只列出 Orchestrator 修改中的 run record（record-only）。`git diff --check a7ecdd9..88b871e` 乾淨。三個 commit message 都符合 git 規則，沒有 Claude 標記。
- **沒有改動產品、測試或資料**：`git diff --quiet a7ecdd9..88b871e -- data.db tests ingestion app.py server.py weather_query.py api static requirements.txt vercel.json`（在 `home_work_01/` 下執行）成立。本票在單元內只改了 `smoke.py`（R-TC-7 的驗證工具）、新增 `tools/`，以及 README 與 worklog。
- **CI 證據**：`gh run list`、`gh run view <id> --json …`、`gh run view <id> --log`，對象是 run `35925410250`（push，`84060c9`）、`35925413146`（pull_request，`84060c9`）、`35925865612`（push，`88b871e`）、`35925868060`（pull_request，`88b871e`），以及修正前失敗的 run `35925129537`（`d854218`）。
- **離線重現（AC-21／R-TC-5）**：以 `git archive 84060c9 home_work_01` 把 subject 樹匯出到 Reviewer 的 scratchpad。匯出的樹沒有 `.env`，環境變數也沒有 `CWA_API_KEY`（`env | grep -c` 為 0）。用單元 `.venv`（Python 3.12.14）執行 pytest，並在程序內把 `socket.connect`、`connect_ex` 與 `getaddrinfo` 對非 loopback 位址改成直接失敗（`-p no:cacheprovider`）。
- **憑證掃描**：在真實 repo 執行 `python -m tools.credential_scan`。另在 scratchpad 建立 sandbox git repo，用執行期產生、UUID 格式的**假**金鑰做反例（值沒有輸出）。真實金鑰只在程序內從被忽略的 `.env` 讀入，**只輸出布林值與次數**。
- **GitHub 查詢（全部唯讀）**：`gh workflow list --all`、`gh api …/actions/workflows`、`gh api …/actions/workflows/home_work_01-smoke.yml`、`gh repo view --json defaultBranchRef`、`gh variable list`、`gh pr list`、`git ls-remote --tags`。Reviewer **沒有**執行 `gh workflow run`：dispatch 會在 GitHub 建立 workflow run，超出 Reviewer 的唯讀範圍。
- **YAML**：用系統 Python 3.11 的 PyYAML 解析兩個 workflow 檔與修正前的 `d854218` 版本。
- **smoke**：以 subject 的 `smoke.py` 對 live preview alias 執行，並對本機一個只接受連線、永遠不回應的 socket 測 budget 上限。
- Reviewer 啟動的本機 socket server 都已關閉。`git status` 與開始時相同。

## 2. Acceptance criteria、需求與 invariants 逐條判定

| 項目 | 判定 | 證據 |
| --- | --- | --- |
| **AC-20**（正向：含本單元變更的 push → CI 成功、log 顯示 3.12、各類測試收集並通過） | **PASS** | run `35925410250`（https://github.com/yotsubamomo/aiot-classwork/actions/runs/35925410250，event `push`，headSha `84060c9`，conclusion `success`，run name `home_work_01 CI`）。Log 摘錄：`Successfully set up CPython (3.12.14)`；`Show Python version` step 輸出 `Python 3.12.14`；`platform linux -- Python 3.12.14, pytest-8.3.3`；`collected 152 items`；`152 passed in 4.02s`；0 個 SKIPPED／FAILED／ERROR。各類都被收集：derive（`test_derive.py` 19）、DB／persist（`test_persist.py` 5）、共用模組（`test_weather_query.py` 29）、Streamlit `AppTest`（`test_app.py` 9）、Flask test client（`test_dashboard.py` 23）、靜態檢查（`test_static_checks.py` 22）；另有 fetch 13、pipeline 19、secrets 4、vercel path 9。`88b871e` 的 push run `35925865612` 與兩個 pull_request run 也都是 success，各自 152 passed。 |
| **AC-20**（負向：不含本單元變更的 push 不觸發） | **PASS**（以設定審查為證據；邊界情況見 F-2） | `home_work_01-ci.yml:8-17`：`push` 與 `pull_request` 都只有 `paths: ['home_work_01/**', '.github/workflows/home_work_01-ci.yml']`。依 GitHub 的 path filter 語義，一般 branch push 只有變更檔案符合其中一個 pattern 才會觸發。Reviewer 同意 literal 的 out-of-unit push 不能用來測試（RB-5）。另一種在授權內的實證做法見 O-2，本 AC 不要求。 |
| **AC-21**（涵蓋 R-TC-1／R-TC-3／R-TC-4 每一項；無網路、無 `.env` 全部通過） | **PASS** | (a) CI 如上。(b) Reviewer 的 clean-room 重現：沒有 `.env`、封鎖對外網路 → **`152 passed in 3.70s`，`BLOCKED_ATTEMPTS: 0`**，也就是沒有任何測試嘗試對外連線。(c) 對照清單依 CI log 的測試名稱，並抽查 `tests/test_app.py:78-111`（表格值等於直接讀 `data.db` 的結果、兩條線、`Date` 軸）：R-DER-1～7 正例（42 列、七個連續日、丟棄開頭不完整日、兩值齊全、四組縣市手算、單縣市 Region）與 AC-09 反例（缺縣市、缺半天、無效值／空字串／NaN／Infinity／abc、只剩六日、不連續），以及反例不寫 DB（`test_pipeline::test_ac09_negative_via_cli` ×5）；R-DB-1～4（DDL 逐字、老師 SQL、重跑無重複、日期平移後整份替換）；R-SHR-2～4（四種狀態、清單順序、序列、日值含 Derived Map Temperature、Forecast Day 清單、ingestion 時間、AC-28 的五組色帶值）；R-SHR-5 靜態 22 項；R-TC-3（標題、`Select Region` 選項與順序、中部與東南部的圖與七列表、缺失與空 DB 的訊息且無例外）；R-TC-4（`GET /` 200 含標題、health 200 與 503、regions／days／series／day values 的正常回應與 404／503）。這些測試的內容已在 #18–#21 的 audit 中 closure，本票沒有改動任何測試（§1）。 |
| **AC-22**（`workflow_dispatch` 實際執行成功並記錄兩個狀態碼；本機同一檢查也成功） | **未驗證：受 reserved boundary（RB-1）前置條件限制。不是 FAIL，也不是 implementation defect。** 詳見 §6 | 可取得的部分：workflow 定義審查 **PASS**；本機同一檢查 **PASS**（Reviewer 在 2026-09-23T22:11:09Z 執行 `python smoke.py https://aiot-hw01-weather-git-homework01-hw10-im-8efc12-nchu-aiot-class.vercel.app --timeout 90 --interval 5` → `GET / -> 200  GET /api/health -> 200`、`SMOKE PASS`（6.1s）、exit 0）。無法取得的部分：live `workflow_dispatch` run URL（smoke workflow 在 GitHub 上沒有註冊，§6）。 |
| **AC-29**（授權原文記入 worklog；只在單元與 workflow 本身變動時觸發；名稱識別本單元） | **PASS** | `diff <(sed -n '137,140p' outcome-contract.md) <(sed -n '28,31p' worklog/issue-22.md)` 無差異，worklog 逐字引用 OC §8.2 第 2 項。該授權所在的 OC 已在 `main`（`d42b1a7`）。觸發範圍見 AC-20 與 §3；名稱 `home_work_01 CI`、`home_work_01 deploy smoke`，檔名 `home_work_01-ci.yml`、`home_work_01-smoke.yml`。 |
| **AC-07(b)(c)(d) 自動化** | **PASS** | CI step `Credential mechanical checks` → `credential scan passed: 465 tracked files; no .env tracked (only .env.example); no CWA-key-format string in tracked files or committed history; no Authorization value in fixture/raw JSON.`（四個 run 相同）。Reviewer 在真實 repo 執行也得到相同結果（exit 0，465 個檔案）。sandbox 反例證明各檢查會失敗（§5）。 |
| R-TC-5（全部測試不需網路與金鑰） | **PASS** | AC-21 (b)。 |
| R-TC-6（push、Python 3.12、全部測試、path filter、名稱識別；MAY pull_request） | **PASS**（邊界情況見 F-2） | 見 CI workflow 與 AC-20。pull_request 使用相同的 filter，且在 PR #27 上實際觸發。 |
| R-TC-7（`workflow_dispatch`、repository variable、R-DS-9 兩條件、≤ 90 秒、與本機同一檢查、變數名文件化） | workflow 定義與本機部分 **PASS**；live dispatch 同 AC-22 | `home_work_01-smoke.yml:13-19` 只有 `workflow_dispatch`，input `url` 為選用。`:46-56` 以 env 傳入 `inputs.url` 與 `vars.HW01_DEPLOY_URL`，input 非空時優先。兩者都空時輸出 `error: no deployment URL: …` 並 `exit 1`（Reviewer 以相同 shell 邏輯模擬四種組合，結果符合）。之後執行同一個 `smoke.py`，檢查 `GET /` 200 且含標題、`/api/health` 200 且 `status == "ok"`；預設 budget 為 90 秒，且上限確實成立（見 §7 的 #21 N-2）。README 第 379 行記載 `HW01_DEPLOY_URL`。 |
| R-ENV-3（root workflow 只在 RB-5 授權內） | **PASS** | §3。 |
| R-SEC-1（CI 自動化部分） | **PASS** | §5。 |
| R-DOC-1（README：執行測試與 CI 段） | **PASS**（有一處措辭不正確，見 F-1） | README「Run the tests (offline)」（第 327 行起，原有）與新增的「Continuous integration (GitHub Actions)」（第 358–386 行），內容包含觸發條件、path filter、3.12、pytest 與憑證檢查、smoke、`HW01_DEPLOY_URL` 與 `url` input。 |
| Ticket：README 新增本票段落 | **PASS**（F-1） | 同上。 |
| Out of scope（不改測試以外的產品程式） | **符合** | §1。`smoke.py` 是 R-TC-7 的驗證指令，不是評分產品的 runtime。這次修改處理 #21 分派給 #22 的 N-2，也屬於 #22 的 traceability（R-TC-7「總重試時間 ≤ 90 秒」）。 |
| **INV-5** | **成立**（Reviewer 可觀察的範圍內） | §5。 |
| **INV-8**（Python 3.12 三處一致） | **CI 部分成立**；本機與 Vercel 維持先前結論 | CI 為 `3.12.14`（log）；本機 `.venv` 為 `Python 3.12.14`；Vercel 的 `.python-version=3.12` 已在 #21 驗證。 |

## 3. RB-5 範圍（OC §8.2）與 AC-29

- **Root 的改動只有兩個 workflow 檔**：`git diff a7ecdd9..88b871e --name-status` 中，`home_work_01/` 以外只有 `A .github/workflows/home_work_01-ci.yml` 與 `A .github/workflows/home_work_01-smoke.yml`。沒有動到 root `CLAUDE.md`、`docs/`、`.gitignore`、其他單元或其他 workflow。`main` 沒有 `.github/`（`git ls-tree -r --name-only main | grep ^.github` 為空）。GitHub 上另一個 workflow `pages-build-deployment` 是 Pages 的 dynamic workflow，不是檔案，也沒有被修改。
- **只服務 `home_work_01`**：兩個檔案都設 `defaults.run.working-directory: home_work_01` 與 `permissions: contents: read`。CI 只測本單元；smoke 只檢查本單元的部署。
- **path filter**：CI 的 push 與 pull_request 都限定在 `home_work_01/**` 與 CI 檔本身，符合 §8.2 的文字。
- **smoke workflow 沒有 `paths`**：見 O-1。Reviewer 判定這符合 §8.2，沒有需要交 Design Authority 的 boundary 疑義。
- **名稱識別**：見 AC-29。
- **判定**：root 變更完全在 §8.2 授權範圍內，AC-29 PASS。

## 4. CI 的建立與修正過程（AC-20 的補充）

- `d854218` 的 push run `35925129537` 失敗。Reviewer 用 PyYAML 解析 `git show d854218:.github/workflows/home_work_01-ci.yml`，得到 `ScannerError: mapping values are not allowed here`，重現了 step name 中未加引號的 `: ` 造成的解析錯誤。`84060c9` 只替該 step name 加上引號（`git diff d854218..84060c9` 只有一行），現行兩個 workflow 檔都能解析，觸發結構與 §3 相同。
- Log 中有 GitHub 平台的 Node 20 deprecation 警告，不影響結果（O-4）。

## 5. H-1 憑證與機密（decision A-1 要求的一節；本票實現 A-5）

**觸及的類別**：H-1（CI 內的金鑰掃描；workflow 不得印出 secret）。本票沒有改動產品、測試、資料、DDL 或推導，所以 **H-2、H-3 沒有被觸及**（§1 的 diff 證據）。

**核對項目與結果**：

1. **`git ls-files` 沒有 `.env`**：只追蹤 `home_work_01/.env.example`。`home_work_01/.gitignore:12` 忽略 `.env`（`git check-ignore -v`）。
2. **追蹤檔案（HEAD，465 個）**：用真實金鑰字面比對，命中 **0** 個檔案（程序內讀取，只輸出次數）。用寬鬆的 `KEY_PATTERN` 做 `git grep`，唯一的命中是 documented 假值 `CWA-1234-5678-90ab-cdef`，分布在 `tests/test_secrets.py`、`tools/credential_scan.py`、`audit/issue-18-c1-r1.md`、`audit/issue-21-c1-r1.md`、`worklog/issue-22.md`。
3. **全部 refs 的 committed 歷史**：`git log -p --all --full-history` 中，符合 `KEY_PATTERN` 的字串只有一種，就是上述假值（8 行），真實金鑰出現 **0** 次（布林值為 False）。這個範圍比掃描器本身的 HEAD 祖先範圍更大。
4. **CI log**：四個 run 的完整 log（`35925410250`、`35925413146`、`35925865612`、`35925868060`）中，`KEY_PATTERN` 命中 **0**，真實金鑰出現 **0** 次。掃描器只輸出路徑、種類與行數，不輸出比對到的字串（`tools/credential_scan.py:108,126,154-158,173,176`）。sandbox 反例的輸出也證實了這一點。
5. **Workflow 不處理任何 secret**：兩個檔案都沒有使用 `secrets.*`。`vars.HW01_DEPLOY_URL` 是公開 URL（目前值為 `https://aiot-hw01-weather.vercel.app`，由 acceptor 在 2026-09-23T17:07:16Z 設定）。`inputs.url` 與變數都透過 `env` 傳入，沒有直接插入 shell 指令，所以沒有 injection 風險。`GITHUB_TOKEN` 權限只有 `contents: read`（log 中 `GITHUB_TOKEN Permissions` 為 Contents: read、Metadata: read）。可選的 hardening 見 O-3。
6. **掃描器確實會抓（sandbox 反例；假金鑰由 `uuid4` 在執行期產生，沒有輸出）**：A 乾淨樹 → exit 0；B 追蹤檔含 UUID 格式假金鑰 → `(c) tracked file …: home_work_01/leak.txt` 與 `(c) committed history contains 1 line(s)`，exit 1；C 刪除該檔後只剩歷史 → `(c) committed history contains 2 line(s)`，exit 1；D 只新增 allowlist 假值 → 沒有新的 finding；E 追蹤 `.env` → `(b) tracked env file must not be committed: home_work_01/.env`，exit 1；F fixture 加入 `"Authorization": "x-token-value"` → `(d) non-empty Authorization value present in …F-D0047-091_sample.json`，exit 1。
7. **新增與修改的檔案**：`credential_scan.py`、`tools/__init__.py`、`smoke.py`、README、兩個 workflow、worklog 都不含金鑰；上述第 2、3 項的掃描已涵蓋。worklog §5.3 記錄了真實金鑰的長度（40），這是 UUID 格式固定的長度，不是金鑰內容，不違反 INV-5。
8. **本紀錄**不含任何金鑰內容。

**A-5 allowlist 的判斷**：`tools/credential_scan.py:60` 的 `_EXAMPLE_ALLOWLIST = ("CWA-1234-5678-90ab-cdef",)` 在比對前以 `str.replace` 移除這一個固定字串（`:63-67`），套用在追蹤檔、歷史的每一行，以及 (d) 的 artifact。Reviewer 的判斷是**可以接受，不構成 finding**，理由如下：

- **範圍很窄**：只有一個字面值，區分大小寫，而且不是 pattern。偵測器 `ingestion/checks.py:15` 沒有改動，`tests/test_secrets.py:27-31` 的自我測試仍然證明偵測器會標出這個假值。
- **不會遮蔽真實金鑰**：真實金鑰是 `CWA-` 加 8-4-4-4-12 的 hex（Reviewer 在程序內核對：`real_key_is_CWA_uuid_8-4-4-4-12: True`、`matches_KEY_PATTERN: True`、`contains_placeholder: False`、`still_matches_after_strip: True`）。假值第一段是 4 個字元，後面接 `-`，所以不可能是真實金鑰的子字串。假值與真實金鑰緊鄰時，Reviewer 實測「假值＋空白＋金鑰」「假值緊接金鑰」「金鑰緊接假值」「放在 JSON 的 Authorization 值中」四種情況，全部仍會被抓到。理論上唯一可能重疊的情況，是金鑰最後一個字元剛好是 `C`、後面緊接 `WA-1234-…`。這時移除假值後剩下 8-4-4-4-11 的字串，仍然符合寬鬆 pattern，所以還是會被抓。
- **仍然符合 AC-07(c)**：所以掃描器能偵測的集合，包含所有 CWA 金鑰格式（8-4-4-4-12）的字串。AC-07(c) 要求「以金鑰格式搜尋為 0 筆」，這在追蹤檔與全部歷史都成立（上述第 2、3 項）。
- **與先前的 disposition 一致**：#18 R1 F-7 把這件事分派給 #22，並寫明「CI 掃描應使用精確格式或明確的 allowlist」。本票採用了其中的明確 allowlist。另一種做法（把 pattern 收窄成精確格式）屬於 HOW，不是契約要求。

**結論**：H-1 在本票範圍內沒有問題，INV-5 在 Reviewer 可觀察的範圍內成立，A-5 的機械檢查已放進 CI 並實際執行通過。覆蓋範圍的邊界情況見 F-3（Low）。

## 6. AC-22 與 RB-1 的處置

**Reviewer 自己確認的事實**：

- 預設分支是 `main`（`gh repo view --json defaultBranchRef`），`main`（`d42b1a7`，與 `origin/main` 相同）沒有 `.github/`。
- `gh workflow list --all` 與 `gh api …/actions/workflows` 只列出 `.github/workflows/home_work_01-ci.yml`（id `365548428`，因為曾由 push／PR 觸發而被註冊）與 `pages-build-deployment`。`gh api repos/yotsubamomo/aiot-classwork/actions/workflows/home_work_01-smoke.yml` 回 **HTTP 404 Not Found**。smoke workflow 在 GitHub 上沒有註冊，現在無法 dispatch。這與 GitHub 文件「To trigger the `workflow_dispatch` event, your workflow must be in the default branch」一致，也和 worklog 記錄的 `gh workflow run` 404 相符（Reviewer 沒有重跑 dispatch，§1）。
- RB-3 的前置條件（repository variable）**已經完成**：`HW01_DEPLOY_URL` 已設定。它指向 production，目前 `GET /` 與 `/api/health` 都是 **404**（Reviewer curl），符合 DR-12：production 要等合併後才會更新。
- workflow 本身是正確的（R-TC-7 一列），CI 全綠，本機同一檢查對受審 commit 的 live preview PASS（AC-22 一列）。

**判斷**：AC-22 中 live `workflow_dispatch` 執行的部分，被 reserved boundary 擋住，而不是實作缺陷。依 accepted contract，smoke workflow 的觸發方式固定為 `workflow_dispatch`（R-TC-7、Spec §5.3「smoke 為獨立 workflow，`workflow_dispatch`；不在 push 時打公開 URL」、DR-13）。在這個定義下，要讓它可以 dispatch，唯一符合契約的方式是讓 workflow 出現在預設分支，也就是 RB-1（保留給 acceptor 的合併）。Executor 無權也無法修正這一點。因此：

- AC-22 在本 R1 的狀態是 **「未驗證：受 reserved boundary（RB-1）前置條件限制」**。它**不是 PASS**，Orchestrator 與後續紀錄都**不得**把 AC-22 標為 PASS。它也**不是 FAIL**：FAIL 例「workflow 無法手動觸發」指的是 workflow 本身不能手動觸發，而這個 workflow 確實定義了 `workflow_dispatch`，受阻的原因是平台的預設分支限制加上 RB-1。
- 這個狀態沿用 DA 的 N-11 處理原則：因 acceptor 保留的前置條件而受阻時，只停止該路徑，Reviewer 判定為「未驗證（外部前置）」而不是 FAIL，AC-22 的最終驗證分配給 #25（derivation §11.1）。另外依治理 §1.5，只停止受影響的路徑。N-11 的條文只寫到變數缺席（RB-3）的情況；本案的前置條件是 RB-1，但性質相同，都是 acceptor 保留的前置條件。
- 依治理 §4.3，blocking 必須是 accepted contract 下的具體實質缺陷。本案沒有這樣的缺陷，所以**不列為 blocking finding**。本 audit 的 closure 依治理 §4.4 不豁免 §3.8 的其他完成條件，**也不代表 AC-22 已滿足**。
- **有一個需要 Design Authority 裁決的契約層級問題**（R-1，§9）：AC-22 的 PASS 需要 dispatch run URL，而這在 RB-1 之前拿不到；但 Bindings §5 的 release gate 與 Spec §6 要求 RB-1 之前 Spec Integration Audit 已 closure，並涵蓋 AC-01～AC-30（包含 AC-22）。兩者形成先後順序的循環。這是契約語義不足造成的 routing signal（治理 §4.2），不是本票的 blocking finding。
- **Reviewer 對 worklog §9「唯一解為 RB-1」的保留**：依 GitHub 社群回報的行為（Reviewer 沒有驗證，驗證需要寫入 GitHub），workflow 一旦因其他事件被註冊，就可能以 `--ref <topic branch>` dispatch。例如加一個只針對該 workflow 檔、job 以 `if: github.event_name == 'workflow_dispatch'` 略過的 push trigger，而 CI 檔正是這樣因 push 被註冊的。這種做法是否符合 R-TC-7、§5.3 與 §8.2，屬於設計判斷，不是 Executor 或 Reviewer 可以自行決定的 HOW。因此一併列入 R-1，由 DA 決定是否可行。在 DA 裁決前，Reviewer 不把「沒有採用這個做法」當作缺陷。

## 7. 先前分派給 #22 的 tracked items

- **#18 R1 F-7**（測試字面值符合寬鬆的金鑰 regex，Owner #22）：**已解決**。採用明確 allowlist，判斷見 §5。
- **#21 R1 F-2／R2 N-2**（`smoke.py` FAIL 時實際經過時間可能超過 budget，Owner #22，可選）：**已解決**。`smoke.py:71-99` 讓每個請求的 timeout 以 `deadline` 的剩餘時間為上限（最多 15 秒，最少 0.1 秒）。Reviewer 對一個只接受連線、永遠不回應的本機 socket 測試：`--timeout 6` → exit 1，wall **6.3s**；`--timeout 20` → exit 1，wall **20.2s**（修正前第二個請求會再用滿 timeout）。超過 budget 才成功的情況仍判為 FAIL（`:130-139`），對外的 CLI、env、輸出與 exit code 沒有改變。對 live preview 的正常路徑也 PASS（AC-22 一列）。
- #18 R1 F-6（`--env PATH`）的 owner 是 #18／#25，不是 #22，本票不處理。

## 8. Findings

### F-1 — README 與 smoke workflow 的註解說合併前就可以 dispatch smoke workflow

- **Severity**：Low　**Blocking**：否
- **契約依據**：R-DOC-1（README 的 CI 段）；AC-12 要求 README 的每一步都實際執行成功，由 #25 做最終核對。
- **證據**：`home_work_01/README.md:383-386` 寫「Because `HW01_DEPLOY_URL` points at the production URL, which is live only after the reserved merge to `main`, demonstrate the workflow now by dispatching it with the `url` input set to the public preview alias」；`.github/workflows/home_work_01-smoke.yml:7-9` 也寫「so the workflow can be demonstrated against a live preview before the reserved merge (RB-1)」。但 §6 已確認，合併前 smoke workflow 沒有註冊（REST 404），所以「now」這一步現在無法執行。合併後帶 `url` input dispatch 是可行的，所以問題只在「合併前」的時點描述。
- **Disposition**：改正措辭，例如「workflow 位於 `main` 後才能 dispatch；在那之前以本機 `python smoke.py <preview>` 執行同一檢查」。Owner：#22 Executor（可選，不延長本 cycle）；否則由 #25 在 AC-12 README 核對時處理。如果 R-1 的 DA 裁決改變了 AC-22 的做法，依裁決同步修改。

### F-2 — CI 的 push trigger 只有 `paths`，平台層級的邊界情況可能在沒有本單元變更時觸發

- **Severity**：Low　**Blocking**：否
- **契約依據**：R-TC-6、AC-20 負向、DR-13「只在 `home_work_01/**` 與其自身變動時觸發」。
- **證據**：`.github/workflows/home_work_01-ci.yml:9-12` 在 `push` 下只有 `paths`，沒有 `branches` 或 `tags`。依 GitHub 文件的語義：(a) push tag 時不評估 path filter；只要沒有定義 `branches`／`tags`，任何 tag push 都會觸發。(b) 一次 push 超過 1,000 個 commit，或 GitHub 因逾時無法產生 diff 時，workflow 一律執行。Reviewer **沒有實測**：實測需要 push tag，屬於寫入動作。
- **風險**：repo 目前沒有 tag（本機 0 個、`git ls-remote --tags` 0 個），範圍內也沒有使用 tag 的流程。即使誤觸發，也只是多跑一次免費、唯讀、沒有 secret 的本單元測試，不影響其他單元或 root。因此在宣告的 operating scope 內沒有實質風險。
- **Disposition**：可選的 hardening 是在 `push` 下加 `branches: ['**']`，這樣 tag push 就不會觸發。Owner：#22 Executor（可選）或 #25。

### F-3 — 憑證掃描器覆蓋範圍的邊界情況（不影響目前的結果）

- **Severity**：Low　**Blocking**：否
- **契約依據**：AC-07(c)(d)；A-5（機械檢查納入 CI，其中也列了「DDL 比對」）。
- **證據**：
  1. (d) 的 Authorization 檢查只看寫死的三個路徑（`tools/credential_scan.py:53-57`）。這三個目前正好是全部追蹤中的 fixture 與原始 JSON（`git ls-files` 中 `home_work_01` 的 `.json` 只有這三個加上 `vercel.json`）。之後若新增 fixture，不會自動納入 Authorization 值的檢查；不過 (c) 的金鑰格式掃描涵蓋所有追蹤檔，而外洩的 Authorization 值就是金鑰本身，所以仍會被 (c) 抓到。
  2. 歷史掃描使用 `git log -p`（`:137-159`），不會輸出 merge commit 的 patch（沒有 `-m`／`--cc`），也不會輸出 binary blob 的內容；範圍是 HEAD 的祖先；而且不偵測 shallow clone。目前的 binary 內容由 (c) 的追蹤檔掃描涵蓋（以 bytes 讀取，含 `data.db`），CI 也使用 `fetch-depth: 0`。
  3. A-5 在 CI 中的「DDL 比對」是對 persist 產生的資料庫（`tests/test_persist.py:32-49`），不是對提交的 `data.db`。Reviewer 另外直接查了提交的 `data.db`：DDL 與老師的 DDL 相同，老師的兩句 SQL 回 6／7。依 A-2，Spec Integration Audit 會再對提交的 `data.db` 執行。
- **影響**：目前的結果都成立。Reviewer 對全部 refs 的歷史，以及包含 binary 的追蹤檔內容做了獨立掃描，真實金鑰 0 次，符合 pattern 的只有 allowlist 假值（§5）。
- **Disposition**：記錄即可。可選的 hardening：(d) 改用 glob、歷史掃描加 `-m` 並偵測 shallow clone、在 CI 對提交的 `data.db` 比對 DDL。Owner：#25（A-2／INV-4／INV-5 的最終核對）或 #22 Executor（可選）。

## 9. Observations（不是 finding）

- **O-1 smoke workflow 沒有 `paths` filter，但符合 §8.2**：GitHub 的 `paths` 只能用在 `push`、`pull_request`、`pull_request_target`，不能用在 `workflow_dispatch`。smoke workflow 沒有任何自動觸發，所以「限定觸發範圍」的目的已經完全達成。R-TC-7 與 Spec §5.3 規定 smoke 以 `workflow_dispatch` 觸發、不在 push 時執行；Spec §9 #2 請求的授權明列「CI 與 smoke」兩個 workflow；而 acceptor 在同一段接受原文（§8.2 第 1 項）中也接受了 Spec v1.1。所以把 §8.2 的 path filter 條文解讀成禁止只有 `workflow_dispatch` 的 workflow，會與同時接受的 Spec 矛盾。派工內容說「兩者都有 `paths`」，這與事實不符，在此更正。
- **O-2 AC-20 負向還有一種授權內的實證做法**：一個只改 `.github/workflows/home_work_01-smoke.yml` 的 commit，在 §8.2 授權內（維護本單元的 workflow），而且不在 CI 的 filter 內，理論上不會觸發 CI。所以 worklog 說 literal 負向測試「需 out-of-unit push」略有誇大。AC-20 沒有要求這種實證，設定審查已經足夠，不需要為此做沒有必要的 commit。之後如果因為 F-1 修改 smoke 檔，可以順便觀察一次。
- **O-3 可選的 hardening**：CI checkout 可以設 `persist-credentials: false`，因為掃描只需要本機 git，不需要驗證。現在的 token 已經只有 `contents: read`，這一點不影響任何契約條款。
- **O-4** CI log 中有 GitHub 的 Node 20 deprecation 警告（`actions/checkout@v4`、`actions/setup-python@v5` 被強制以 Node 24 執行），不影響結果，是日後的維護事項。
- **O-5** 目前沒有 cross-ticket 回歸：`88b871e` 的 push 與 PR run 都是 152 passed、掃描通過。從本票起，CI 是後續票的回歸證據來源（Ticket 的 cross-ticket 段）。

## 10. Routing 與所需 authority

- **R-1 → Design Authority**（契約語義不足造成的 routing signal，治理 §4.2；不是 blocking finding）。具體的歧義是：AC-22 的 PASS 要求「以 `workflow_dispatch` 手動觸發……workflow run URL」。在 smoke 定義為只有 `workflow_dispatch` 的前提下（R-TC-7、§5.3、DR-13），這在 RB-1 之前拿不到。但 Bindings §5 的 release gate 與 Spec §6 要求 RB-1 之前，Spec Integration Audit 已 closure 並涵蓋 AC-22。N-11 只處理 RB-3（變數缺席），DR-12 只處理 AC-15。需要 DA 裁決：(a) AC-22 的 live dispatch 是否比照 DR-12 作為 RB-1 之後的 release evidence，以及 RB-1 之前的 PASS 證據要是什麼（例如 workflow 審查、CI 全綠，加上對受審部署執行本機同一檢查），或者這樣做是否已經構成 acceptance semantics 的變更（治理 §5.3 第 1 類，需要 acceptor）；(b) 以 path filter 限定、job 會略過的非 dispatch trigger 先註冊 workflow，再以 `--ref` 在 topic branch dispatch，是否算 R-TC-7、§5.3、§8.2 允許的 HOW（依據是社群回報的 GitHub 行為，Reviewer 沒有驗證）；(c) 若 DA 無法確立兩者都在 boundary 內，依治理 §1.2 fail-closed 到 acceptor。
- **Acceptor**：RB-1 是 acceptor 的保留動作；只要 R-1 的結果需要把 workflow 放上 `main`，就需要 acceptor 執行。RB-3 的 repository variable 已經設定，不需要其他 acceptor 動作。
- **Orchestrator**：依 §6，AC-22 記為「未驗證：受 RB-1 前置條件限制」，不得標為 PASS；F-1～F-3 依各自的 owner 追蹤。

VERDICT: CLOSURE
