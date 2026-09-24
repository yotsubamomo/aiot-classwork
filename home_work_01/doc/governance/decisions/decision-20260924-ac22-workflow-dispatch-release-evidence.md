# Decision record — AC-22 的 `workflow_dispatch` 實跑：合併前的 PASS 證據與合併後的 release evidence（`home_work_01/`）

- **紀錄類型**：Design Authority decision record（治理 §3.6-A：在不改變任何 accepted 語義的前提下裁決既有來源尚未寫明之處；治理 §5.3 第 2 類「不改變 accepted 語義的 derived contract clarification」，須記錄對進行中工作、dependencies 與既有 evidence 的影響）
- **編號**：**DR-18**（延續 [`decision-20260923-spec-interpretation-rulings.md`](decision-20260923-spec-interpretation-rulings.md) DR-1～DR-16 與 [`decision-20260924-ingestion-timestamp-semantics.md`](decision-20260924-ingestion-timestamp-semantics.md) DR-17）
- **日期**：2026-09-24
- **來源**：Issue #22 cycle 1 R1 audit record [`../audit/issue-22-c1-r1.md`](../audit/issue-22-c1-r1.md) §6、§10 routing signal **R-1**（治理 §4.2：契約不足是 routing signal，不是 blocking finding；R1 verdict 為 CLOSURE，無 blocking finding）；由 Orchestrator 依治理 §2.4 派工，run record [`../run/run-20260924-hw01-formal.md`](../run/run-20260924-hw01-formal.md)
- **相關契約**：Outcome Contract（ACCEPTED 2026-09-23）§2.5、§4、§6、AB-17、§8.2；Bindings b1 §2.5、§2.6（RB-1）、§5（release gate）；Spec v1.1 R-TC-7、R-ENV-3、AC-13、AC-15、AC-22、§5.2、§5.3、§6（Release 列）、§9（前置 #2、#4；已知風險）；DR-12、DR-13；`decision-20260924-unattended-run-policy.md` N-11、S-3；`decision-20260923-high-risk-categories.md` A-6；derivation record §11.1（AC-22 分配 #22 與 #25）、§11.5 #5；Tickets #22、#25
- **執行角色**：`gov-design-authority`（binding 核對由派工者依 Bindings §3.4 記入 run record）
- **效力**：與 Spec v1.1 同一效力層級，作為 AC-22、R-TC-7、AB-17 證據欄與 Spec §6 Release 列的解讀依據；Executor、Reviewer（含 Spec Integration Audit）、Orchestrator 以本紀錄適用該等條款，不得重開。Spec 文字不變；下次一致性修訂 MAY 在 AC-22 加註 DR-18（metadata 層級）。本紀錄不修改任何實作或測試。

## 1. 問題

AC-22（Spec v1.1；對應 OC AB-17、R-TC-7）的 PASS 條件是「以 `workflow_dispatch` 手動觸發 smoke workflow，成功完成並記錄 `GET /` 與 `/api/health` 的狀態碼；本機執行同一檢查亦成功」，證據為「workflow run URL；本機輸出」。#22 交付的 smoke workflow 定義正確、沿用同一 `smoke.py`，本機同一檢查對受審 subject 的公開部署 PASS；但 GitHub 只能 dispatch **存在於預設分支（`main`）** 的 `workflow_dispatch` workflow，而 `main` 沒有 `.github/workflows/`，workflow 只在 topic branch 上。把它放上 `main` 就是 RB-1（保留給 acceptor 的合併）。另一方面，Bindings §5 的 Formal release gate 要求在 acceptor 合併**之前**：全部 Ticket 結案、Spec Integration Audit closure（治理 §4.7：每條 Spec AC 有 evidence 與 PASS／FAIL 判定）、DA phase acceptance。兩者形成先後順序的循環。

需要裁決：(a) 為了 #22 結案、(b) 為了 Spec Integration Audit 的 AC coverage、(c) 為了 Bindings §5 release gate，AC-22 各以什麼證據為滿足；哪些是合併前依現有授權可取得的完成條件，哪些（若有）是合併後的 release evidence；Reviewer 提出的「先以非 dispatch trigger 註冊 workflow、再對 topic branch dispatch」是否為契約允許的 HOW。

## 2. 事實（DA 自行核對；Executor 與 Reviewer 的敘述只作為待驗證主張）

| # | 事實 | 證據 |
| --- | --- | --- |
| E-1 | 預設分支為 `main`；`origin/main`（`d42b1a7`）沒有任何 `.github/` 路徑。 | `gh repo view --json defaultBranchRef`；`git ls-tree -r --name-only origin/main`（`.github` 計數 0） |
| E-2 | GitHub 上已註冊的 workflow 只有 `.github/workflows/home_work_01-ci.yml`（id `365548428`，因 push／pull_request 觸發而註冊）與 Pages 的 dynamic workflow；REST `GET /repos/…/actions/workflows/home_work_01-smoke.yml` 回 **404**。smoke workflow 目前無法 dispatch。這與 GitHub 文件「`workflow_dispatch` 的 workflow 須位於預設分支」一致，也與 worklog 記錄的 `gh workflow run` 404 相符。 | `gh api …/actions/workflows`；`gh api …/actions/workflows/home_work_01-smoke.yml` |
| E-3 | Repository variable `HW01_DEPLOY_URL` = `https://aiot-hw01-weather.vercel.app`（2026-09-23T17:07:16Z 設定，RB-3 前置已完成），指向 **production**；目前 `GET /` 與 `/api/health` 都是 **404**（合併前 production 尚未更新，DR-12）。受審 subject 的公開 preview alias `https://aiot-hw01-weather-git-homework01-hw10-im-8efc12-nchu-aiot-class.vercel.app` 目前 `GET /` **200**、`/api/health` **200** 且 `status: "ok"`、6 區、7 日、ingestion `2026-09-24T02:24:50+08:00`。 | `gh variable list`；DA 的 curl（2026-09-24） |
| E-4 | 受審 subject `84060c9` 的兩個 workflow 檔與 `home_work_01/smoke.py` 和工作樹相同（`git diff --stat 84060c9 -- .github home_work_01/smoke.py` 為空）。smoke workflow 的 `on:` **只有** `workflow_dispatch`（選用 input `url`）；step 以 env 傳入 `inputs.url` 與 `vars.HW01_DEPLOY_URL`，`URL="${INPUT_URL:-$VAR_URL}"`，兩者皆空時明確訊息並 `exit 1`；在 `working-directory: home_work_01` 執行 `python smoke.py "$URL"`；`permissions: contents: read`；不使用任何 `secrets.*`；action 骨架（`actions/checkout@v4`、`actions/setup-python@v5` 3.12）與 CI workflow 相同。 | `.github/workflows/home_work_01-smoke.yml`、`home_work_01-ci.yml`、`home_work_01/smoke.py` @ `84060c9` |
| E-5 | CI workflow 已在 GitHub-hosted runner 對同一 subject 實跑成功：run `35925410250`（push，`84060c9`）、`35925413146`（pull_request）、`35925865612`／`35925868060`（`88b871e`，record-only delta）皆 `success`；修正前 `35925129537`（`d854218`）因 YAML 解析錯誤失敗，`84060c9` 只修了該行。R1 已用 PyYAML 解析現行兩個 workflow 檔並模擬 shell 的四種 URL 組合。 | `gh run list --workflow home_work_01-ci.yml`；R1 §1、§4、R-TC-7 列 |
| E-6 | 「本機同一檢查」對受審 subject 的公開部署 PASS 且互相獨立：Executor（1.3 s，200／200，exit 0）；Reviewer 2026-09-23T22:11:09Z（`--timeout 90 --interval 5`，6.1 s，200／200，`SMOKE PASS`，exit 0）；DA 於本紀錄日期再次確認 200／200（E-3）。 | worklog §5.6；R1 AC-22 列；E-3 |
| E-7 | 契約文字：OC AB-17「部署 smoke test **可由** `workflow_dispatch` 執行，檢查公開根路徑與健康 endpoint」，證據「workflow 執行紀錄」；OC §2.5「RB-1～RB-6 維持保留」；OC §6「Release gate：合併進 `main` 由 acceptor 執行（RB-1），前提見 Bindings §5」；Spec AC-13「合併為 acceptor 的 release 動作，不是完成條件」；Spec §6 Release 列「合併後對 production URL 重跑 smoke 記為 release evidence」；Spec §9 已知風險「合併後對 production URL 再跑一次 smoke 作為 release evidence（不是完成條件）」；DR-12「合併後對 production URL 重跑 smoke 記為 release evidence，不是 work item 或 Spec 的完成條件」；DR-13「smoke 為獨立 `workflow_dispatch` workflow」；Spec §5.3「smoke 為獨立 workflow，`workflow_dispatch`；不在 push 時打公開 URL」；R-TC-7「同一檢查 MUST 也能在本機以指令執行」。 | 各檔原文 |
| E-8 | Ticket #22 的 AC-22 條只預見 RB-3（變數缺席）的 BLOCKED；Ticket #25 要求「對最終 subject 的部署重跑 smoke（本機指令與 `workflow_dispatch`）成功」並在 Reserved 段寫「RB-1：合併後對 production URL 重跑 smoke 記為 release evidence（DR-12），不是本票完成條件」；N-11 把 AC-22 的最終驗證分配給 #25，且只寫到 RB-3 的情況；unattended-run policy S-3「run 不需要合併即可完成 #18–#25；合併是 #25 之後的 release 動作」；A-6「Release gate…另附 A-5 的最後一次 CI 結果引用，記在 `doc/acceptance/`」。 | Issues #22、#25；N-11、S-3；A-6 |
| E-9 | PR #27（`home_work_01-hw10-implementation` → `main`）已開（SA-2）。 | `gh pr list` |

## 3. 兩種解讀

- **(A) live dispatch run 是合併前的完成條件。** 依 AC-22 字面，PASS 需要 workflow run URL。但在 accepted OC 的其他條款下（RB-1 保留、AB-17 把觸發方式固定為 `workflow_dispatch`）加上 GitHub 的預設分支規則（E-1、E-2），這個 run 在 acceptor 執行 release 動作之前，任何 Agent 依現有授權都拿不到；release gate 反過來又要求它先存在。這個讀法使 accepted contract 的條款彼此不可同時滿足，也與 Spec §6／§9、DR-12 已經寫下的「合併後 smoke 是 release evidence」不一致；而且 workflow 的**預設** URL 來源就是 production 變數，其預設執行在合併前依設計必然 404（E-3）——它本來就是合併後的檢查。
- **(B) 依驗證對象拆分 AC-22 的證據與時點。** AC-22 的實質是：同一個檢查對受審 subject 的公開部署真的執行且成功，並且交付了一個以 `workflow_dispatch` 執行同一檢查的 workflow。前者與 workflow 交付物的正確性在合併前可完整驗證；「GitHub-hosted 的 live dispatch run」在 RB-1 之後才可取得，其地位與 DR-12 對 AC-15 的 production smoke 相同：release evidence。

## 4. 裁決（DR-18）：採 (B)

### 4.1 AC-22 的三個組成與各自的證據

| 組成 | 內容 | PASS 證據 |
| --- | --- | --- |
| **AC-22(a) 檢查實質** | 與 workflow 使用的**同一** `smoke.py`（同一 subject SHA）對受審 subject 的公開部署（不需登入）執行：`GET /` 200 且含 `Taiwan Weather Forecast`；`GET /api/health` 200 且 `status == "ok"`；在 90 秒重試內達成。 | 本機指令輸出：時間戳、URL、兩個狀態碼、`SMOKE PASS`、exit 0；Reviewer 獨立重跑。 |
| **AC-22(b) workflow 交付物** | 受審 SHA 的 smoke workflow：YAML 可解析；`on:` 為 `workflow_dispatch`（選用 `url` input）；URL 來自 repository variable（變數名在 README 文件化），input 非空時覆寫，兩者皆空時明確失敗；在 `home_work_01` 下執行同一 `smoke.py`；不使用 secret、最小 permissions；與 CI workflow 共用的 action 骨架已在 GitHub-hosted runner 對同一 subject 實跑成功。 | workflow 檔審查（解析、觸發、URL 解析邏輯模擬）；CI run URL（骨架實跑）；README 變數名。 |
| **AC-22(c) GitHub-hosted live `workflow_dispatch` run** | 該 workflow 在 GitHub 上以 `workflow_dispatch` 實際執行成功，log 記錄兩個狀態碼。 | workflow run URL＋log 摘錄（兩個狀態碼、`SMOKE PASS`）。 |

以下**不算** (c)：CI workflow 的 run；本機或模擬器執行 workflow；job 被略過的 run；只對 404 的 production 跑到 FAIL 的 run。

### 4.2 時點：什麼是完成條件、什麼是 release evidence

1. **(a)＋(b) 是合併前的完成條件**：#22 結案以其 subject 的 (a)＋(b) 為準；#25 對最終 subject 重新建立 (a)，並重新確認 (b)（workflow 檔未變或已重審、最近一次 CI run）；Spec Integration Audit 對 AC-22 以 (a)＋(b) 給 PASS／FAIL。
2. **(c) 是 release evidence（RB-1 之後）**，與 DR-12 對 AC-15 的 production smoke 同一地位：workflow 抵達 `main` 後的第一次 dispatch——以預設來源（`HW01_DEPLOY_URL`＝production）執行——就是 Spec §6 Release 列「合併後對 production URL 重跑 smoke」的機械化版本。它**不是** #22、#25、Spec Integration Audit、DA phase acceptance 或 run completion 的完成條件。
3. **(c) 仍然是必要的**：OC AB-17 的證據欄「workflow 執行紀錄」在 release 時交付；release gate 的材料（A-6，`doc/acceptance/`）與 Orchestrator 完成報告 MUST 把它列為 acceptor 在 RB-1 之後要產生的 release 項目，不得省略或寫成已完成。
4. **例外——提前取得**：若在合併前依現有授權取得真正的 (c)（第 4.5 節），MUST 立即記入 #22 或 #25 的 worklog 與 `doc/acceptance/`，此時合併後以 production 預設來源的 run 就只是 DR-12 的 production release evidence。

### 4.3 紀錄規則（Orchestrator、Executor、Reviewer 共同適用）

- 任何紀錄對 AC-22 的狀態一律寫成：「**AC-22 PASS（DR-18：(a)(b) 已驗證；(c) release evidence，待 RB-1 後 dispatch）**」。不得寫成無保留的 PASS，也不得隱藏 (c) 的狀態。
- R1 record `issue-22-c1-r1.md` 不改寫；其 AC-22 列的「未驗證：受 RB-1 前置條件限制」加上本紀錄，就是 AC-22 在 #22 的 disposition。Orchestrator 對 #22 的結案判定，AC-22 部分依：R1 AC-22 與 R-TC-7 列已核對的 (a)(b) 證據＋本紀錄（orch-default §7 P3：gate 適用範圍由 DA §3.6-A clarification 確立；P6：已 route 的 design question 有 decision record）。本紀錄**不要求** #22 做任何 correction。
- **#25**：對最終 subject 重做 (a)（本機指令對最終 subject 的公開部署）；重新確認 (b)；記錄 (c) 當時的狀態與證據（`gh api …/actions/workflows/home_work_01-smoke.yml` 的 404，或已取得的 run URL）。`doc/acceptance/` 的 AC-22 條目列出 (a)(b) 的證據引用，並把 (c) 標為「release evidence，待 RB-1 後 dispatch」；A-6 的 release gate 材料含此項。Ticket #25「AC-15、AC-22：…（本機指令與 `workflow_dispatch`）成功」依本紀錄解讀：`workflow_dispatch` 部分即 (c)，除非提前取得，否則為 release evidence，不是 #25 的完成條件。
- **Spec Integration Audit**：對最終 subject 核 AC-22 的 (a)(b)，給 PASS／FAIL；(c) 依本紀錄記為 release evidence。Reviewer 若對本 determination 提出 boundary 符合性 finding 且在 DA 評估後仍有爭議，依治理 §1.2／§4.7 視為 DA 無法確立，該路徑 fail-closed 至 acceptor。
- **DA phase acceptance 與 Orchestrator 完成報告**：依治理 §3.8「run completion、work item completion、phase acceptance 與 release authorization 分別陳述」，明列「AC-22(c)＝release evidence，由 acceptor 於 RB-1 後產生」。
- **合併後**：dispatch 可由 acceptor 在 Actions 頁「Run workflow」執行，或由 Agent 依 acceptor 的直接指示執行（建立 workflow run 不在 RB-1～RB-6 之列；但此時 Formal run 已結束，屬 Bindings §4「已結案工作之後的單點修正」的 Lightweight work item）。run URL 與兩個狀態碼記入 `doc/acceptance/` 的 AC-22 條目。若 dispatch 失敗，那是對 release evidence 的缺陷：依 acceptor 指示以新的 Lightweight work item 修正，不重開 Formal run；release 本身仍是 acceptor 的決定。

### 4.4 不接受的做法

- 把 smoke workflow 的觸發方式改成 push／pull_request 而在 push 時打公開 URL：違反 AB-17（觸發方式為 `workflow_dispatch`）、Spec §5.3、DR-13。
- 以 CI workflow 的 run、`smoke.py` 的本機輸出，或 job 被略過的 run 冒充 (c)。
- 以 (c) 未取得為由，把 AC-22 記為 FAIL 或把 #22／#25 記為 BLOCKED 停止整個 run；也不得為此新增「保險起見問 acceptor」的 gate（治理 §5.2）。

### 4.5 可選路徑（advisory；DA 不要求；不採用不構成 finding）

- **(i) Reviewer 的 R-1(b)：先註冊、再對 topic branch dispatch。** 在 smoke workflow 加一個只針對其自身檔案的 `push` trigger（`paths: ['.github/workflows/home_work_01-smoke.yml']`），job 以 `if: github.event_name == 'workflow_dispatch'` 讓 push 時整個 job 略過，push 一次使 GitHub 註冊該 workflow，再 `gh workflow run home_work_01-smoke.yml --ref home_work_01-hw10-implementation -f url=<公開 preview alias>`。**Boundary 判定**：在 OC §8.2 內（path filter 恰為該 workflow 檔本身）；符合 R-TC-7、Spec §5.3 與 DR-13 的目的（push 時不打公開 URL；不對其他單元或 root 檔案觸發；AC-29 仍成立），屬契約允許的 HOW。**效力未經驗證**（依社群回報的 GitHub 行為；R1 與 DA 都沒有執行，驗證需要對 GitHub 寫入）。若嘗試且產生對受審 subject 公開 preview 的真正 `workflow_dispatch` run，該 run 即為合併前的 (c)；若不成功，回復為純 `workflow_dispatch` 檔即可，AC-22 仍依本紀錄處置。這是受審 subject 的變更：在 #22 屬審後 delta（治理 §3.8、orch-default §7 P7，需相應驗證），在 #25 屬「已授權 workflow 的維護」；是否投入由 Orchestrator 依成本判斷，不是必要工作。
- **(ii) Acceptor 的選項。** RB-1 屬 acceptor；acceptor 可以在任何時點自行決定先把兩個 workflow 檔（或整個分支）合併進 `main`，使 (c) 在最終合併前可取得。這不是請求，也不是停止條件；本紀錄只說明其存在。

### 4.6 R1 F-1 的措辭方向

README「Continuous integration」段與 smoke workflow 檔頭註解目前寫成合併前就可以帶 `url` input dispatch（R1 F-1，Low，非 blocking，owner 依 R1：#22 Executor 可選，否則 #25 於 AC-12 處理）。修正時依本紀錄：workflow 位於 `main` 之前無法 dispatch，合併前以 `python smoke.py <preview>` 執行同一檢查；合併後 dispatch 預設用 production 變數（release evidence），`url` input 供對其他 URL 檢查。Owner 與 severity 依 R1，不由本紀錄改動。

## 5. 依據

1. **accepted contract 必須讀成條款可同時滿足。** OC 同時接受了 AB-17（觸發方式 `workflow_dispatch`、證據為 workflow 執行紀錄）、§2.5／§4（RB-1 保留）與 §6（release gate＝acceptor 合併，前提依 Bindings §5）。在 GitHub 的預設分支規則下，解讀 (A) 讓 AB-17 的證據只能由 release 動作本身產生，卻又要在 release 之前存在——沒有任何 Agent 在現有授權內能滿足。解讀 (B) 是唯一與全部條款相容的讀法（治理 §3.6-A「既有來源只有一種合理解讀而尚未寫下」）。
2. **完成與 release 已被分開陳述，且 acceptor 已接受這個框架。** OC §6 把 release gate 交給 Bindings §5；acceptor 接受時同時使 Spec v1.1 生效，其 AC-13、§6 Release 列、§9 已知風險與 DR-12 都寫明「合併後對 production URL 重跑 smoke 是 release evidence，不是完成條件」。smoke workflow 的預設來源就是 production 變數（E-3、E-4）：它以預設方式執行的那次 run，**就是**這句話所指的 smoke。DR-18 只是把 DR-12 已裁決的地位套用到承載它的 workflow run。
3. **治理 §3.8、§5.2。** 「Run completion、work item completion、phase acceptance 與 release authorization MUST 分別陳述」；「work item completion 不授予 release permission」——反之，release evidence 也不是 work item 的完成 gate。本紀錄沒有取消或弱化任何 gate（Bindings §5 三項、A-6、§4.7 的 AC coverage 全部維持），只把 AC-22 的證據對到各自可取得的階段。
4. **實質沒有被弱化。** workflow 執行的檢查與本機檢查是同一個檔案（R-TC-7 的 MUST，E-4）；這個檢查已對受審 subject 的公開部署真正執行且成功，Executor 與 Reviewer 各自獨立（E-6）；GitHub-hosted 的 action 骨架已由 CI 對同一 subject 實跑證明（E-5）。合併前無法排除的殘餘風險只剩「smoke YAML 在 GitHub 上執行時本身出錯」，已由 YAML 解析、shell 邏輯模擬與相同 action 版本收窄，並會在 release 時的 dispatch 立刻暴露，有 Lightweight 修正路徑；這與 DR-12 已接受的「production 在合併後才更新」是同一類 release 時點風險。
5. **與 N-11 一致，且必須延伸。** N-11 已裁決：因 acceptor 保留的前置條件而受阻時，Reviewer 判「未驗證（外部前置）」而非 FAIL，最終驗證交 #25。RB-3 的變數已設定（E-3），剩下的前置是 RB-1；與 RB-3 不同，RB-1 依 S-3「合併是 #25 之後的 release 動作」在定義上就在 run 之後，所以把 (c) 留給 #25 只會在 #25 產生一個必然、且無路可走的停止。治理 §1.5 只允許在缺少的授權**真的**是繼續執行所必需時停止；(c) 不是完成所必需，因此不得作為 #25 的完成條件。
6. **不得自創 gate、也不得為進度捏造證據。** 本紀錄同時禁止把 (c) 寫成已完成（第 4.3 節）與把它當作停止整個 run 的理由（第 4.4 節），符合治理 §1.5「Run-to-completion 不授權弱化 gate、捏造 evidence、隱性縮減 scope，或跨越保留權限」。

## 6. 是否改變 accepted 語義；boundary determination

**否。** AB-17 的可觀察條件（smoke test 可由 `workflow_dispatch` 執行、檢查公開根路徑與健康 endpoint）與證據類別（workflow 執行紀錄）都不變，本紀錄只確定該證據在哪個階段產生，而這個階段（release）正是 OC §6 自己指向的階段。沒有新增 requirement、AC、scope 或 invariant；沒有取消任何 gate；Spec 文字不變。不建立其他工作依賴的新設計基線：唯一受影響的下游是 #25 與 Spec Integration Audit 對既有 AC-22 的驗證路徑。屬治理 §5.3 第 2 類，不觸發 acceptor 核准。

**Boundary determination（治理 §1.2）**：在已接受的 Outcome Contract boundary 內。本裁決本身不需要任何 reserved action；它所依賴的 reserved action（RB-1）是 OC 原本就分配給 acceptor 的 release 動作，時點與內容都未改變。第 4.5 節 (i) 亦在 OC §8.2 的 RB-5 授權範圍內（path filter 為該 workflow 檔本身）。

## 7. 對 work items 的影響

- **#22**：可依 R1 CLOSURE＋本紀錄進入結案判定；AC-22 依第 4.3 節記錄。F-1～F-3 的 owner 與 severity 依 R1 不變；本紀錄不要求 correction，也不要求嘗試第 4.5 節 (i)。
- **#23、#24**：不受影響。
- **#25**：第 4.3 節；Ticket 內「`workflow_dispatch`」部分依本紀錄解讀為 (c)。
- **Spec Integration Audit**：AC-22 以 (a)(b) 判 PASS／FAIL，(c) 記為 release evidence；不新增 audit instance 或 round。
- **DA phase acceptance、Orchestrator 完成報告、Bindings §5 release gate**：可在 (c) 未取得的狀態下完成與陳述，但 MUST 分別列出 (c) 為 acceptor 的 release 項目；A-6 材料含此項。
- **控制面**：Orchestrator 於 run record 與 Issue #22、#25 以 comment 引用 DR-18（N-22）。

## 8. 對既有 evidence 與 audit coverage 的影響（治理 §5.3 第 2 類、§3.8）

- R1 `issue-22-c1-r1.md` AC-22 列與 R-TC-7 列的證據（本機同一檢查 PASS、workflow 定義審查、shell 模擬、CI run）即 #22 subject 的 (a)(b) 證據，不需重做；其「未驗證」判定與本紀錄並存、不衝突。
- 不重開任何已閉合的 finding；不新增 audit round。若採用第 4.5 節 (i) 而改動 subject，依 §3.8／P7 由 Reviewer 判定必要的審後驗證。
- worklog `issue-22.md` §9「唯一解為 RB-1」的敘述依本紀錄修正為「(c) 為 release evidence；可選路徑見 DR-18 §4.5」（record-only）。

## 9. 需要其他 authority 的事項

無需即時的其他 authority。不需 acceptor（不改變 accepted 語義、不新增 reserved action）；不需 Final Adjudicator（沒有 routing 或 review 爭議）。Acceptor 在 release 時執行 RB-1 並（自行或指示 Agent）dispatch 一次以產生 (c)，這是 OC 已分配的 release 動作；第 4.5 節 (ii) 為 acceptor 可自行選擇的提前選項，不是請求。

## 10. Evidence

- 治理 v2.0 §1.2、§1.5、§2.4、§3.6-A、§3.8、§4.2、§4.3、§4.7、§5.2、§5.3；Bindings b1 §2.4、§2.5、§2.6、§4、§5、§7；orch-default §7 P3、P6、P7。
- Outcome Contract §2.5、§4、§6、AB-1、AB-17、§8.2；Spec v1.1 R-TC-7、R-ENV-3、AC-13、AC-15、AC-22、AC-29、§5.2、§5.3、§6、§9、§10。
- DR-12、DR-13；N-11、S-3、N-22；A-5、A-6；derivation record §11.1、§11.5、TB-4、TB-5。
- `issue-22-c1-r1.md` §1、§2（AC-22、R-TC-7 列）、§6、§8 F-1、§10 R-1；`worklog/issue-22.md` §5.6、§9；Issues #22、#25。
- Subject `84060c9`：`.github/workflows/home_work_01-smoke.yml`、`home_work_01-ci.yml`、`home_work_01/smoke.py`；DA 於 2026-09-24 的唯讀核對：`gh repo view`、`git ls-tree origin/main`、`gh api …/actions/workflows`（含 smoke 404）、`gh variable list`、`gh run list`、`gh pr list`、production 與 preview URL 的 curl、`git diff --stat 84060c9`。
