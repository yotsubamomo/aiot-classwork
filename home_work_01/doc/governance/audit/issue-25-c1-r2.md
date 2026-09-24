# Audit record — Issue #25 整合驗收（INTEGRATION／FINAL VERIFICATION），cycle 1，R2

| 項目 | 內容 |
| --- | --- |
| Work Contract | GitHub Issue #25（`yotsubamomo/aiot-classwork`，INTEGRATION／FINAL VERIFICATION）；Spec `home_work_01/doc/spec/SPEC.md` v1.1；Outcome Contract（ACCEPTED 2026-09-23）AB-1、AB-8、AB-11～AB-13、AB-17；decisions A-1／A-2／A-6、DR-12、DR-17、DR-18、DR-19；R1 record [`issue-25-c1-r1.md`](issue-25-c1-r1.md) |
| 受審 subject | branch `home_work_01-hw10-implementation`，HEAD **`75389e6796b081033a8783a66f3ac66b0b63c35e`**（`git ls-remote` 相同）；Executor 指定的 verification anchor 為 **`6407d8b2d0f04523f5057b0880083f3bd836c6a8`**。R1 subject 為 `a571ccc`；修正 delta 為 `a571ccc..75389e6`（`6407d8b` → `10ca4f8` → `0e093f2` → `75389e6`）。 |
| Audit 種類 | Ticket audit **R2**（scoped closure review），**cycle 1**。依治理 §4.4，只核對 R1 blocking 是否解決、有無回歸，以及修正是否直接產生新的 blocking defect；不是第二次全面審查。 |
| 角色 | `primary_reviewer`（`gov-primary-reviewer`） |
| Binding 證據 | 由派工者依 Bindings §3.4 核對，記錄於 `home_work_01/doc/governance/run/run-20260924-hw01-formal.md`。 |
| Independence | 延續 Reviewer 自己的 R1 context（治理 §2.3 第 1 項允許）；不繼承 Executor context。本輪從磁碟與 git 重讀修正後的檔案與 diff，自行重跑檢查；本 record 由 Reviewer 以 Write 寫入；沒有任何 git 寫入。 |

## 1. 修正 delta 的範圍（回歸核對的基礎）

- `git diff --numstat a571ccc..75389e6`：`README.md`（+13/−11）、`doc/acceptance/ACCEPTANCE.md`（+69/−23）、`doc/governance/worklog/issue-25.md`（+127/−23）、`requirements.txt`（+3/−2）、`tests/test_fetch.py`（−2）。
- 排除 `home_work_01/doc` 之後，只剩 `README.md`、`requirements.txt` 與 `tests/test_fetch.py`。`requirements.txt` 只改註解，四行固定版本（`requests==2.32.3`、`pytest==8.3.3`、`streamlit==1.64.0`、`flask==3.1.2`）不變，也沒有 folium。`test_fetch.py` 只刪除未使用的 `import json`。
- 沒有改動 `app.py`、`server.py`、`weather_query.py`、`api/`、`static/`、`data.db`、`ingestion/`、`vercel.json`、`.python-version` 或 `.github/workflows/`。
- `6407d8b..75389e6` 只改 `ACCEPTANCE.md` 與 worklog（`git diff --stat`）：填入 smoke 與 CI 證據值、更新 AC-14 行號、調整措辭。

## 2. R1 blocking findings 的 closure 核對

### F-1（smoke 輸出與部署 ↔ commit 對應）— **已解決**

- ACCEPTANCE.md §8（:196-220）、AC-15 列（:58）、AC-22 列（:65）與 worklog §5b 都貼出實際輸出：`[2026-09-24T02:47:42Z] attempt 1 url=https://aiot-hw01-weather-git-homework01-hw10-im-8efc12-nchu-aiot-class.vercel.app GET / -> 200 GET /api/health -> 200 (0.9s elapsed) PASS`、`SMOKE PASS`、`exit: 0`，並記錄 URL、兩個狀態碼，以及 `data-deployment-id="dpl_5geV9Trc3cX1WGZiRKg1oNEHSqqZ"` = GitHub deployment `6629046658` = commit `6407d8b`。符合 AB-1、AC-15、DR-18 §4.1 與 Ticket AC 的證據要求。
- **證據的真實性（Reviewer 自行核對）**：
  - `gh api …/deployments`：`6629046658` 的 sha 是 `6407d8b`，Preview，建立於 02:47:03Z，status success。Environment URL `aiot-hw01-weather-pgk50bikt-…` 的 `GET /` 帶有 `data-deployment-id="dpl_5geV9Trc3cX1WGZiRKg1oNEHSqqZ"`，與記錄相符。下一個部署（`10ca4f8`）建立於 02:50:41Z，所以 02:47:42Z 時 alias 指向 `6407d8b` 的部署，與時間線一致。
  - Reviewer 在 2026-09-24T02:58:59Z 對 alias 重跑 `smoke.py` → `GET / -> 200 GET /api/health -> 200 (0.8s) PASS`、`SMOKE PASS`、exit 0。`<title>Taiwan Weather Forecast</title>`；`/api/health` 回 `{"status":"ok","region_count":6,"forecast_day_count":7,"ingestion_time":"2026-09-24T02:24:50+08:00"}`。
  - 目前 alias 服務的是 `dpl_EfrSYrivRkvRrz7BPTPcBQiDrNR4`，即 deployment `6629144717`，也就是 **HEAD `75389e6`** 的部署。
  - 對 `6407d8b` 的 immutable deployment URL 重跑 smoke → `SMOKE PASS`（0.8s）。
  - alias 上的 `static/app.js`、`styles.css`、`vendor/leaflet.js` 與 `75389e6`、`6407d8b` 的 blob 的 sha256 都相同。
- 「部署的 commit 與受審 subject 對應」對 anchor 與 HEAD 都成立。

### F-2（AC-07(e) overclaim，H-1）— **已解決**

- ACCEPTANCE.md:50 的狀態欄改為 `PASS (a–d,f); (e) split — see note`，(e) 拆成「the deployed dashboard needs no env var/secret = PASS」與「"no CWA key is set in the Vercel project env" = **PENDING-ACCEPTOR** (R-SEC-3, H-1, RB-3, #21 F-3 …; consistent with §5-3(c))」，與 §5-3(c)（:149-153）一致。
- `git grep -i "acceptor-verified"` 在 `75389e6` 的 `doc/acceptance` 與 worklog 中沒有結果。
- 「不需環境變數」的 PASS 有依據：`server.py` 與 `api/index.py` 不讀 OS 環境變數（R1 已核對，本輪兩個檔案都沒有變更）。

### F-3（最終 subject identity）— **已解決**（殘餘的措辭不一致列為 non-blocking N-1）

- R1 指出的錯誤已更正：worklog §3（:31-49）、§9 與 ACCEPTANCE.md §0（:12-24）都明寫「per Bindings §7 only `doc/governance/**` paths are record-only, so `doc/acceptance/` … is part of the subject」，不再稱 `fafcf2f` 為最終 subject，也不再把 `1396226` 稱為 record-only。
- Subject 的識別方式：以 `6407d8b` 作為 verification anchor（CI run `35948664254` success，152 passed，credential scan passed；部署 smoke PASS），並明寫「The Spec Integration Audit reviews the branch HEAD, which is behaviourally identical to and a doc-superset of the anchor」（ACCEPTANCE.md:23-24、worklog :46-47）。Reviewer 核對 `6407d8b..75389e6` 確實只改 `ACCEPTANCE.md` 與 worklog，沒有任何行為變更，所以這個 anchor 加上文件 delta 的描述是可靠的 identity 識別（impl-default §7：識別 delta 並核對 coverage）。Spec Integration Audit 被導向 HEAD，而 HEAD 包含最終版的 R-DOC-4 交付物。R1 F-3 的實質風險，也就是 SIA 審查的 subject 缺少驗收文件，已經消除。
- 殘餘問題見 N-1：「Final subject = `6407d8b`」這個標籤與「SIA reviews the branch HEAD」並存，而且 `6407d8b` 內的 ACCEPTANCE.md 是含 placeholder 的草稿。

## 3. Non-blocking F-4～F-8 的處理（不作 closure 條件，只記錄結果）

| R1 finding | 結果 |
| --- | --- |
| F-4（彙整不完整） | **已處理**。ACCEPTANCE.md §6 新增 #18 R2 N-1～N-5、#18 R1 F-9、#19 R1 F-6、#19 R1 F-10、#20 R1 F-4、#21 R2 N-1。**#18 R2 N-1** 標為 Medium，未在 #25 修正，owner 為 post-#25 的 Lightweight follow-up，依 A-4 需要 independent audit，由 Orchestrator 指派（:172）。措辭問題見 N-2。 |
| F-5（README 過時措辭） | **已修正**。README:8-16 的 Scope 說明改為涵蓋 CI 與 Vercel 部署，anchor `#continuous-integration-github-actions`、`#deploy-to-vercel-public-url--smoke-check` 對應實際標題。:59-63 與 `requirements.txt` 註解改為說明 Leaflet 是 vendored JS，不是 Python 相依。 |
| F-6（AC-10 證據引用） | **已處理**。AC-10 列（:53）引用 DR-19 與最終 UI 的 `issue-24-state-error.png`，並註明 `ac10_dashboard_error_missing_db.png` 是 #20 時期的 UI；worklog §6 記錄了在最終 subject 上的 headless 重驗。 |
| F-7（AC-25 終端輸出） | **已處理**。Worklog §5a 貼出 fetch 摘要（real fetch 到 scratch 路徑，`periods per temperature element: 14`，這是較晚一次擷取的即時資料，已標明）與 offline rebuild 的 42 列預覽（與 Reviewer 在 R1 看到的輸出逐列相同），沒有金鑰。 |
| F-8（未使用的 import） | **已修正**。`pyflakes tests/test_fetch.py` 沒有輸出；`test_fetch.py` 仍收集到 13 個測試並通過。 |

AC-14 的 README 行號引用已隨 README 變更更新，Reviewer 逐項對照 `75389e6:home_work_01/README.md` 的 :3-6、:20-21、:24-27、:28-30、:31-36、:37-47、:48-53、:194-204、:270-272、:275-280，以及 AC-25 的 :149-167、:154，內容都正確。AC-14 仍是 8/8 PASS。

## 4. 回歸核對

- **測試**：`git archive 75389e6 home_work_01` 匯出到 scratchpad（沒有 `.env`，沒有 `.git`），以乾淨的 Python 3.12.14 venv 執行 → **152 passed in 4.10s**。CI：`6407d8b` 的 push run `35948664254` 與 `75389e6` 的 push run `35949279269` 都是 success；log 為 `Python 3.12.14`、`152 passed`、`credential scan passed: 510 tracked files`。`10ca4f8`、`0e093f2` 的 push 與 pull_request run 也都是 success。
- **資料與行為**：`75389e6` 的 `data.db` sha256 仍是 `9bbf05bc…f542b`。INV-2：Flask test client 對六區的 series 都等於 `weather_query.region_series`（True）；`/api/health` 為 ok 6/7。App、static 與部署 build 沒有改變，所以 R1 對 AC-02／03／04／10／19／24／27 的判定維持有效。
- **Acceptor-deferred 項目仍如實標為 pending**：
  - AC-22(c)：ACCEPTANCE.md:65、§5-1；`gh api …/home_work_01-smoke.yml` 仍為 404。
  - AC-15 production：:58、§5-2；production `/api/health` 仍為 404，這是合併前的預期狀態。
  - #21 F-3 的三項：AC-23 build log（:66、§5-3(a)）、AC-30 Root Directory 截圖（:73、§5-3(b)）、Vercel env 沒有金鑰（:50、§5-3(c)）。
  - 沒有任何一項被寫成已完成。PR #27 仍為 OPEN（draft），head `75389e6`。
- 修正沒有造成回歸，也沒有直接產生或暴露新的 blocking defect。

## 5. 高風險類別核對（decision A-1，重述）

- **H-1**：在 `75389e6` 的工作樹執行 `python -m tools.credential_scan` → passed（510 個追蹤檔案，只有 `.env.example`，追蹤檔案與歷史中沒有金鑰格式字串，fixture 與 raw JSON 沒有 `Authorization`）。以被忽略的 `.env` 中的真實金鑰值比對（值從未印出）：`75389e6` 的追蹤檔案 **0** 筆，`git log --all -p` 全歷史 **0** 筆；`a571ccc..75389e6` 的 diff 中 CWA-UUID 格式字串 **0** 筆。Worklog §5a 貼出的輸出不含金鑰。AC-07 的 Vercel env 項目已正確標為 PENDING-ACCEPTOR（F-2）。**PASS**。
- **H-2**：Reviewer 對 `75389e6` 提交的 `data.db` 親自執行老師的兩句 SQL：`SELECT DISTINCT regionName FROM TemperatureForecasts;` → **6**；`SELECT * FROM TemperatureForecasts WHERE regionName = '中部地區';` → **7**。`PRAGMA table_info` 為 `id INTEGER PK, regionName TEXT, dataDate TEXT, mint REAL, maxt REAL`。`app.py`、`data.db`、`streamlit run app.py`、頁面文字與六個 Region 名稱都沒有變更；修正沒有觸及這些項目。**PASS**。
- **H-3**：沒有改動推導、驗證、對應表、fixture 或 Derived Map Temperature 的程式。README 修改的是 Scope 說明與相依說明，R-DOC-2 的標示段落內容不變，只有行號位移；AC-14 8/8 依新行號逐項確認。**PASS**。

## 6. 新的 non-blocking 項目（不延長 cycle）

### N-1 — 「Final subject」標籤指向 `6407d8b`，但該 commit 內的 ACCEPTANCE.md 是含 placeholder 的草稿

- **Severity**：Low　**Blocking**：否
- **證據**：`git show 6407d8b:home_work_01/doc/acceptance/ACCEPTANCE.md` 的 §0 為 `` `__FINAL_SHA__` ``，§8 為 `__SMOKE_LINE_1__`、`__SMOKE_LINE_2__`、`__DPL_ID__`、`__GH_DEPLOY_ID__`、`__DEPLOYED_SHA__`；這些值在 `10ca4f8` 才填入。ACCEPTANCE.md:12-13 與 worklog §9（「Final subject identity … `6407d8b` — the commit that includes `doc/acceptance/ACCEPTANCE.md`」）把 `6407d8b` 稱為 final subject，同時又寫 SIA 審查 branch HEAD。ACCEPTANCE.md 不能寫出包含它自己的 commit SHA，所以用 anchor 的寫法可以理解；但 worklog 屬 record-only path，可以寫出確切的 HEAD SHA。
- **為何不列為 blocking**：兩份文件都明寫 SIA 審查 branch HEAD，也明寫 anchor 到 HEAD 的 delta 只有文件；Reviewer 已核對這個 delta。R1 F-3 的實質風險已經消除。
- **Disposition**：Owner 為 Orchestrator。派 Spec Integration Audit 時，dispatch pack 應以**確切的 HEAD SHA**（目前是 `75389e6`，之後只有 `doc/governance/**` 的 commit 時不變）作為受審 subject，`6407d8b` 只作為行為驗證的 anchor。Worklog §9 可以選擇同步更新；它是 record-only，更新不影響 subject identity。

### N-2 — 小的紀錄措辭與一致性問題

- **Severity**：Low　**Blocking**：否
- **證據**：
  - (a) ACCEPTANCE.md:172 對 #18 R2 N-1 寫「Fail-closed today: the value is written verbatim, no crash」。把不合格的值原樣寫入是 fail-open，不是 fail-closed。
  - (b) INV-5 列（:98）仍寫「508 tracked files」，AC-07 列（:50）與 CI 為 510。
  - (c) 章節順序是 §6 → §8 → §7；§7（:226）仍寫「#25's forthcoming record」。
- **Disposition**：可選的文字修正，owner 為 Orchestrator。都不影響任何判定。

## 7. 其他 authority

- 不需要 Design Authority 或 Final Adjudicator：沒有契約語義疑義或爭議。
- 維持 R1 的建議：#18 R2 N-1（Medium）由 Orchestrator 指派 post-#25 的 Lightweight owner，依 A-4 需要 independent audit。
- Acceptor 在 release 時（RB-1、RB-3）處理的項目不變：AC-22(c)、AC-15 production smoke、#21 F-3 的三項確認。

## 8. 結論

R1 的 blocking findings F-1、F-2、F-3 都已解決。修正沒有造成回歸（152 passed、CI 綠燈、app／static／DB 沒有變更、H-1／H-2／H-3 PASS），也沒有直接產生或暴露新的 blocking defect。新的 N-1、N-2 都是 non-blocking，已記錄 owner。

VERDICT: CLOSURE
