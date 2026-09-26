# Phase acceptance addendum — SPEC-V2 v2.2，post-key 殘餘義務 P-1～P-4 結清與 F-1 裁決（HW01 Weather Map V2，`home_work_01/`）

- **紀錄類型**：Design Authority phase acceptance **addendum**（治理 §3.8；本紀錄是 [`phase-acceptance-SPEC-V2.md`](phase-acceptance-SPEC-V2.md) §3.3「結清」列與 §10 預告的 `phase-acceptance-SPEC-V2-addendum-<YYYYMMDD>-postkey.md`）。它補完先前 phase acceptance 的殘餘義務，不取代、不重寫該紀錄；兩份合起來才是 SPEC-V2 的完整 phase acceptance。
- **日期**：2026-09-26。
- **執行角色**：`gov-design-authority`（Bindings §3.1：`design_authority` → `claude-fable-5-1`／`xhigh`）。正式 binding 核對依 Bindings §3.4 由派工者（Orchestrator）記入 run record。DA 唯讀觀察：session `05b8408b-260a-46d3-a4fe-ec07e3ec365a/subagents/` 現有 6 個 `gov-design-authority` agent，皆 `claude-fable-5-1`／`xhigh`；相對先前紀錄新增的 `a118d65eae91e4721` 應為本次派工；以派工者核對為準。
- **派工**：Orchestrator run `run-20260925-hw01-v2-formal`（[`../run/run-20260925-hw01-v2-formal.md`](../run/run-20260925-hw01-v2-formal.md)「Post-key verification」段），於 post-key 驗證 record 提交後自主派工（治理 §1.4）。
- **引用的紀錄**：
  - 先前 phase acceptance：[`phase-acceptance-SPEC-V2.md`](phase-acceptance-SPEC-V2.md)（ACCEPTED，可完成範圍；§3.3 定義 P-1～P-4 的 owner、判準與紀錄位置；§2.7 定義 post-key subject 規則；§5 各 tracked item 的處置）。
  - Spec Integration Audit（治理 §4.7）：[`../audit/spec-SPEC-V2-c1-r1.md`](../audit/spec-SPEC-V2-c1-r1.md)，cycle 1 R1，**VERDICT: CLOSURE**（可完成範圍），subject `9902026`。
  - **Post-key 證據補完**：[`../audit/spec-SPEC-V2-c1-r1-postkey.md`](../audit/spec-SPEC-V2-c1-r1-postkey.md)，**VERDICT: CLOSURE（P-1..P-3 PASS，P-4 recorded）**，Reviewer `gov-primary-reviewer` agent `a55f579063a0b44bd`（fresh context；`claude-opus-5-5`／`xhigh`；`diversity_lost` 已記；與 SIA `ad2f24768b95d2567`、#41 R1 `a16d3b7e242f9d1aa` 為不同 instance）。
  - F-1 的依據：[`../audit/issue-35-c1-r1.md`](../audit/issue-35-c1-r1.md) F-2、[`../audit/issue-35-c1-r2.md`](../audit/issue-35-c1-r2.md) §4、[`../audit/issue-40-c1-r1.md`](../audit/issue-40-c1-r1.md) F-2、[`../audit/issue-37-c1-r1.md`](../audit/issue-37-c1-r1.md) AC-V2-06(e) 列與 §(d)、[`derivation-SPEC-V2.md`](derivation-SPEC-V2.md) §11 #1；SPEC-V2 v2.2 R-V2-OBS-7～13、R-V2-DEG-1～5、R-V2-RAD-4、INV-V2-6／7、§5.3 儀器、AC-V2-06／07／08；OC-V2 S-6、S-7、AB-V2-3／4／5。
- **Independence**：post-key record、run record 的 checkpoint 敘述與派工文字皆當作待驗證主張。第 10 節列出 DA 自行核對的項目與結果；未自行核對者以該 record（獨立 audit）為據。本 DA 未修改任何實作、測試、資料、`doc/acceptance/`、`doc/ticket/`、worklog、Spec 或 Bindings；未 commit；未 merge；未繳交；未讀 `home_work_01/.env`；未接觸 Vercel 專案、環境變數或 log；未要求、讀取、印出或匯出任何金鑰值；未對 CWA 或 preview 發出請求。

---

## 1. 裁決摘要

1. **P-1～P-4 結清。** P-1、P-2（回應面）、P-3 由獨立 Reviewer 在金鑰生效的 preview 上重現並判 PASS，P-4 已記錄；服務的 commit `e75303c` 符合先前 §2.7 的 subject 規則（`9902026` 的 record-only／索引後代，產品碼相同）。先前 phase acceptance 帶出的殘餘義務**全部結清**；AC-V2-17(c)、AC-V2-22 觀測部分（合併前部分）、AC-V2-03 preview 抽樣、decision A-6 preview 觀測驗證紀錄由 BLOCKED 轉為**已驗證**；AB-V2-2／10／13 的部署部分已驗證。P-2 的 Vercel runtime log 面依先前 §3.3 P-2 列為 **acceptor 於 release 時的自查項目，不阻擋本 addendum**。
2. **F-1（並行／鎖）裁決：(a)。** 在已接受的 Spec 內是可接受的 non-blocking 殘餘：降級仍有界且「分類或終態」；第 3 個以後排隊請求看到較不具體的訊息不違反任何 AC／INV；不改變 accepted 語義；不需 Executor 修正、不需 acceptor re-scope。作為 tracked follow-up，owner **acceptor**（是否指示結案後的 Lightweight work item）；第 3 節。
3. **SIA F-1（375 px 組合態）與 #38～#40 地圖可用性交接的處置不變**（non-blocking；第 4 節）。
4. **Phase 狀態：SPEC-V2 v2.2 的 phase acceptance 於本 addendum 後為「完成（全範圍）」。** DA 不再持有任何 pre-merge blocker；Bindings §5「Design Authority phase acceptance 已完成」於全範圍成立；SPEC-V2 §6.4 Release 列「acceptor 已填 Vercel 金鑰的 preview 驗證（合併前）」與 decision A-6「preview 觀測驗證紀錄」已具備。**合併（RB-1）與繳交（RB-2）仍是 acceptor 的保留動作；本紀錄不是 release authorization、不是 submission authorization、不是 Outcome Contract closure**（治理 §3.8、§5.2；第 6 節）。

---

## 2. P-1～P-4 結清

### 2.1 Subject 規則（先前 §2.7）的核對

| 項目 | DA 自行核對結果 |
| --- | --- |
| Preview ↔ commit | GitHub deployment **`6678056047`**：sha `e75303c16da66c199e88fb558cb1e45e0434c322`、environment Preview、creator `vercel[bot]`、created 2026-09-26T11:07:14Z、status success、`environment_url` ＝ `https://aiot-hw01-weather-8qeq3ey4t-nchu-aiot-class.vercel.app`（`gh api …/deployments/6678056047` 與 `…/statuses`）。 |
| `e75303c` 是 `9902026` 的後代 | `git merge-base --is-ancestor 9902026 e75303c` 成立。 |
| 差異只在允許的路徑 | `git diff --name-only 9902026 e75303c` ＝ `doc/governance/audit/issue-41-c1-r1.md`、`audit/spec-SPEC-V2-c1-r1.md`、`decisions/phase-acceptance-SPEC-V2.md`、`run/run-20260925-hw01-v2-formal.md`、`worklog/issue-41.md`（Bindings §7 record-only）＋ `doc/ticket/tickets-v2.md`（先前 §2.7 已判定的 #41 狀態列）。`git diff --stat 9902026 e75303c -- home_work_01 ':!home_work_01/doc'` **為空**。 |
| 產品碼相同 | `home_work_01/static` tree `a27d174e…`、`server.py` blob `0692caee…`、`observation.py` blob `6f19255c…`、`radar.py` blob `a10b83ca…` 在 `9902026` 與 `e75303c` 兩側相同。 |
| CI | `e75303c`：run `36237807133`、`36237805654` 皆 success。 |
| 之後的 delta | `git diff --name-only 9902026 HEAD`（HEAD `ee0b75b`）只多 `audit/spec-SPEC-V2-c1-r1-postkey.md` 與 run record 更新（record-only）；`doc/acceptance/` 在 `9902026..HEAD` **零變更**；單元目錄外自 BASE `08e158e` 零變更；`origin/main` 仍為 `08e158e`（未合併）。 |

**結論：Reviewer 驗證的就是 phase acceptance subject `9902026` 的產品碼；subject identity 不變。**

### 2.2 Post-key 驗證的合法性（治理 §2.3、§4.7；先前 §3.3 步驟 1）

- Reviewer 為 `gov-primary-reviewer` fresh instance（DA 以 Bindings §3.4 指令核對 `agent-a55f579063a0b44bd` ＝ `gov-primary-reviewer`、`[('claude-opus-5-5','xhigh')]`），不是 Executor，不是 acceptor 敘述；record 由 Reviewer 自寫（Bindings §3.5 第 4 點），由派工者原樣 commit（`ee0b75b`）。
- 證據類別符合 Spec §3 原文「preview 驗證紀錄（Reviewer 重現）」與先前 §3.3 步驟 1 的要求（bounded pack 附 #41 R1 F-2 兩項註記：`vercel.live` 屬平台注入；P-2 只以金鑰格式掃描）。record 檔頭列明其只做 P-1～P-4 的證據補完，不重做 SIA、不重開已閉合 finding——與先前 §3.3「紀錄位置」列一致（cycle 1 SIA instance 的補完，不是 R2、不是新 cycle）。
- 憑證（RB-3 b3、H-1）：record §1 明記未讀 `.env`、未讀取／列出／匯出任何環境變數、未進入 Vercel 後台、未對 CWA 發出請求；所有記錄的回應本文與標頭、evidence 與 record 本身的金鑰格式掃描 0 命中（唯一命中為 Reviewer 自造的掃描器自測字串，已說明）。DA 未在 record 中發現任何金鑰值、上游 URL 或 `Authorization` 值。

### 2.3 逐項結清

| 項目 | 先前 §3.3 判準 | Post-key record 的判定與關鍵證據 | DA 結清 |
| --- | --- | --- | --- |
| **P-1** AC-V2-17(c) 觀測、AC-V2-22 觀測部分 | `/api/observations/latest` 200、`dataset` O-A0001-001、`validStationCount` ≥ 1、`stations[]`、兩個時間；瀏覽器 Now mode 顯示 Latest Observation 與兩個時間；`smoke.py` PASS；deployment ↔ commit | **PASS**（§3）：200、`O-A0001-001`、840 有效／876 收到、`observationTime` `2026-09-26T19:00:00+08:00`、`fetchedTime` ＝ 請求當下；本文 0 上游結構鍵、0 上游主機、0 `Authorization`、金鑰格式 0；1280 與 375 Now mode `success`（1.69 s／1.30 s），頁面兩個時間與有效站數 ＝ 頁面自己收到的本文（DevTools 讀回）；22 個代表標記；外部請求 0；`smoke.py` PASS 0.6 s；deployment ↔ commit 如 2.1 | **結清（PASS）** |
| **P-2** AC-V2-17(c) 雷達、INV-V2-2 平台面（H-1，必要） | `/api/radar/latest` 200 `image/png`＋`X-Radar-Time`＋`X-Radar-Dataset: O-A0058-006`；所有記錄的回應金鑰格式 0、無上游 URL、無 `Authorization`；runtime log 只在 acceptor 提供時掃描 | **PASS（回應面）**（§4）：200 `image/png` 72,393 B、3600×3600、三個 `X-Radar-*` 標頭、`no-store`；瀏覽器 Radar On → `success` 2.73 s、`Radar Time` ＝ `X-Radar-Time`、24 條同源 `blob:` strip、圖層順序 basemap 300 ＜ radar 350 ＜ overlay 400 ＜ marker 600（像素證據：標記在雷達之上）；全部 30 餘個回應本文與標頭金鑰格式 strict 0／broad 0、`Authorization` 0、上游主機 0。**Runtime log 面：acceptor 未提供**，Reviewer 依先前 §3.3 P-2 記「未提供；以本機 DEBUG-log 零洩漏證據（SIA §2 INV-V2-2）為據」，並確認程式面 log 只記 reason／狀態碼／站數／雷達時間／位元組數 | **結清（PASS，回應面）**。Runtime log 面依先前 §3.3 的既定規則成為 **acceptor 於 release 時的自查項目**（V1 #21 F-3 先例）；只以金鑰格式規則自查、不匯出；**不阻擋本 addendum** |
| **P-3** AC-V2-03 preview 抽樣 | ≥ 3 站頁面值 ＝ 同頁 `/api/` 本文；哨兵顯示「—」 | **PASS**（§5）：22／22 代表標記 pill ＝ 同站 `airTemperature`；8 站詳情全部欄位逐字相等（涵蓋 RH、氣壓、風速／風向、雨量各為 `null` 的站、天氣有值、連江、金門、臺北市）；抽樣中 10 個 `null` 全顯示「—」；本文 0 個欄位等於哨兵碼。上游哨兵→`null` 的對應以 AC-V2-03 離線證據為據（preview 上依 RB-3 不能讀上游原文）——這是 AC 原文的證據分層，不是缺口 | **結清（PASS）** |
| **P-4** decision A-6 preview 觀測驗證紀錄＋Vercel 時序／並行 | 記錄 P-1～P-3 的時間、URL、deployment id 與結果；冷啟動；可行時並行請求；終態在頁面 20 s 內；平台時限 ≤ 8 s 上限 → route DA | **已記錄**（§6）：A-6 紀錄表（URL、GitHub `6678056047`、Vercel `dpl_du45X9VRwcPgRxfZJTnXRrSt7cFr`、sha、逐時段結果）；冷啟動 6.41 s（health）／7.69 s（觀測，含新取得）；新取得約 2–2.7 s；重用 0.3–0.7 s；頁面終態 ≤ 2.73 s；並行 23 個回應全部 200；公開文件 Fluid 預設時限 300 s，`X-Vercel-Id` region 與文件一致；**「平台時限 ≤ 8 s」的 DA flag 條件未成立**；新證據：部署有 in-function concurrency（→ F-1，第 3 節） | **結清（已記錄）**。derivation §11 #1 的「函式執行上限是否容納一次取得＋逾時」以此證據**解決**：8 s ＜ 300 s，§5.3 儀器與裁剪策略**不需調整**，derivation record 不需修訂。殘餘不確定（後台層級的 Max Duration 覆寫）無任何跡象，acceptor 可於 release 時順便確認（**非必要**） |

### 2.4 結清的效果

- **AC-V2-17(c)**、**AC-V2-22 觀測部分（合併前 preview 部分）**、**AC-V2-03 preview 抽樣**：由 BLOCKED（RB-3）轉為 **PASS**——證據為 post-key record §3～§5，不是本紀錄。AC-V2-22 的「production 於合併後重跑」依 AC 原文仍是 **release evidence，不是完成條件**。
- **decision A-6「preview 觀測驗證紀錄」**：已具備（post-key record §6.1）。
- **AB-V2-2／10／13 的部署部分**：已驗證。AB-V2-13「Now mode 於部署上回傳 Latest Observation（acceptor 填入金鑰後）」與「部署 commit 與受審 subject 對應」成立。
- **INV-V2-2 的 Vercel 平台面**：回應面成立（H-1）；runtime log 面 → acceptor release 自查（2.3 P-2 列）。
- 先前 phase acceptance §1 表格中標「未完成／未具備」的各列，依第 5 節更新。

---

## 3. F-1 裁決：並行請求在上游停滯時被鎖序列化——(a) 可接受的 non-blocking 殘餘

### 3.1 事實（DA 自行核對者標明）

1. **程式**（DA 讀 `e75303c` ＝ `9902026` 的 blob）：`observation.py:549` `with self._lock:` 涵蓋金鑰讀取、重用檢查與 `fetch_upstream`（上限 8 s）；`radar.py:384` 同構，涵蓋 `fetch_product`；兩個鎖是**各自服務的物件**，互不相關；失敗不寫入快取（`observation.py:591`、`radar.py:420` 只在成功後寫）。
2. **前端**（DA 讀 `static/app.js`）：`OBS_TIMEOUT_MS`／`RADAR_TIMEOUT_MS` ＝ 20,000（l. 263、297）；`requestObservation()` 在上限到時 abort 並 settle `no_response`（l. 809–812、830）；非 2xx 且 JSON `reason` 為四個代碼之一 → 以該代碼為類別，否則 `unexpected_response`（l. 840–860）；`failureText()` 對四個伺服器代碼附上代碼本身，對 `no_response`／`unexpected_response` 用固定非機密句（l. 277–278、948–957）；Stale／Unavailable 各有 chip 與說明（l. 963–969）。同一頁面進行中不重複觸發（l. 776–779，R-V2-OBS-7(e)）。
3. **平台**（post-key record §6.3、§6.4，DA 未重跑）：stagger 三個請求共用同一次取得（同一 Fetched Time；雷達三者在 21 ms 內結束）→ 同一 instance 同時處理多個 invocation（Fluid compute optimized concurrency）；公開文件時限預設 300 s；本部署 30 餘個回應無平台逾時，最長 7.69 s。
4. **停滯＋並行的行為**（post-key record §6.5 的本機重現，用 subject 自己的程式與 threaded WSGI；DA 未重跑；與 #35 R1 F-2、#40 R1 F-2、#37 R1 的 probe 一致）：單一 8.03 s → 504 `upstream_unreachable`；4 個並行觀測 8.01／16.02／24.04／32.05 s，皆 504 `upstream_unreachable`；3 個並行雷達 8.02／16.03／24.03 s；每個排隊請求各自再試一次上游（失敗不快取）。
5. **對使用者的效果**：同一 instance 上，CWA 停滯期間第 k 個並行請求約在 8k s 得到分類 JSON；頁面對每個請求的 20 s 上限先到時（k ≥ 3），該頁面顯示 `no_response` 的固定句（「this site's server did not answer in time or could not be reached」）並進入 Stale（有資料）或 Unavailable（無資料）；頁面放棄的請求仍在伺服器端排隊直到輪到它並各自嘗試一次上游。k ≥ 38 才會超過 300 s 變成平台錯誤，此時頁面早已以 `no_response` 到達終態，遲來的平台錯誤被忽略（`settle()` 只生效一次）。
6. **#37 已涵蓋的部分**（DA 讀 `issue-37-c1-r1.md`）：AC-V2-06(e) PASS 時已包含「兩個請求排在伺服器鎖前」16.0 s 情境與 Reviewer 扣住請求 20.4 s 情境，皆在 30 s 儀器內到達終態；#37 R1 §(d) 明記部署上的多實例與平台時序交 #41。

### 3.2 逐條對照契約（不弱化任何 oracle）

| 條款 | 要求 | F-1 情境下 | 判定 |
| --- | --- | --- | --- |
| **R-V2-OBS-13** 有界時間 | 每次 Refresh 在有界時間內到達 newer／not-newer／Stale／Unavailable 之一；伺服器對上游請求設逾時、README 文件化，且**小於平台 function 執行上限**，使上游停滯以 `upstream_unreachable` 分類回應而非平台 gateway 錯誤；前端對任何非 JSON 或平台層錯誤回應仍依 failure 處理 | 每個請求 ≤ 20 s 到達終態（頁面上限）；上游逾時 8 s 已文件化（README l. 407–410）；8 s ＜ 300 s；排隊請求（k ≤ 37）仍得到分類 JSON；k ≥ 38 的平台錯誤與 20 s 內無回應皆由前端依 failure 處理 | **成立**。本條約束的是「上游請求的逾時」相對平台上限，以及前端對非分類回應的處理；它沒有承諾在任意並行度下每個 client 都能在頁面上限內拿到伺服器的分類，且它自己要求前端不得為了等分類而停在進行中。這是唯一合理的讀法（見 3.4） |
| **R-V2-OBS-12** 非機密錯誤；四類失敗在使用者可見層各自可辨 | 訊息不含金鑰／上游 URL／上游本文；四類伺服器分類到達 UI 時可辨 | 收到分類 JSON 者顯示該代碼（可辨）；20 s 內未收到任何回應者顯示固定非機密句 `no_response` | **成立**。「四類各自可辨」的前提是 UI 收到其中一類；沒有任何回應時無類可辨，UI 以非機密的類別描述呈現，符合 R-V2-OBS-10(a)(b)「非機密原因」 |
| **R-V2-OBS-10** Success／Stale／Unavailable | 失敗 → 保留資料與兩個時間（Stale）或 Unavailable；Refresh 仍可用；之後成功清除；Stale 只以失敗為基準 | `no_response` 走與四類相同的 `applyObservationFailure` 路徑：資料與兩時間保留（Stale）／Unavailable；Refresh 可用；成功清除 | **成立** |
| **R-V2-OBS-7(e)**、**R-V2-OBS-8**、**INV-V2-6** | 進行中不重複觸發；亂序不以舊蓋新；伺服器只回成功或分類失敗；Stale 只以失敗為基準 | 單一頁面單飛（`obsInFlight`、`obsSeq`）；遲來回應被忽略；伺服器排隊回應仍是分類失敗（不是帶資料的 stale）；平台錯誤不是「伺服器回應」 | **成立** |
| **R-V2-OBS-9** 重用視窗 | 只重用成功；≤ 10 分鐘 | 失敗不快取（每個排隊請求各自嘗試上游） | **成立**（其代價是 3.5 的 tracked item，不是違反） |
| **R-V2-DEG-1～5、INV-V2-7、R-V2-RAD-4** | 三條路徑各自載入、失敗、恢復；觀測失敗只影響觀測層；`/api/health` 不依賴 CWA | 觀測鎖與雷達鎖是不同物件；預報路徑與 `/api/health` 不取鎖；上游等待為 I/O（釋放 GIL），同一 instance 的其他路徑不被阻擋（post-key record §6.3 的並行處理即證明 instance 同時處理多個請求） | **成立** |
| **AC-V2-06(e)／(f)、AC-V2-07、AC-V2-08** | 停滯模擬 30 s 內 Stale／Unavailable 且回應為分類 JSON；平台非 JSON 5xx 仍到達終態；四類各自觸發、可辨 | 已在 #35／#37／SIA 於其定義的情境（單一停滯、2 個排隊、扣住請求、平台頁）PASS；F-1 是這些 AC **未定義**的情境（≥ 3 個並行停滯落在同一 instance），AC 的 oracle 本身不受影響 | **維持 PASS**；DA 不擴張 AC 的情境（擴張即新增 OC 未涵蓋的 requirement，屬 §5.3 第 1 類，非本紀錄可為） |
| **§5.3 儀器** | 終態 ≤ 30 s；上游逾時建議 ≤ 10 s 且 ＜ Vercel `maxDuration` | 20 s ≤ 30 s；8 s ≤ 10 s ＜ 300 s | **成立，不需調整**（derivation §11 #1 解決；2.3 P-4 列） |
| **OC-V2 S-6、AB-V2-3／4／5** | 每次 Refresh 在有界時間內到達 success／stale／unavailable；伺服器端失敗分類「（驗證用）」；使用者可見錯誤非機密；三路徑獨立 | 全部如上 | **成立**。OC 把伺服器分類明標為驗證用途；使用者面的 accepted 語義是有界終態＋非機密原因＋Stale 保留資料，皆成立 |

### 3.3 裁決

**採 (a)：F-1 是已接受的 Spec 內可接受的 non-blocking 殘餘。** 沒有任何 AC、invariant 或 gate 被違反；不需 Executor 的 corrective work；不需 acceptor re-scope；不延長 cycle 1；不影響 P-1～P-4 的結清與本 phase acceptance。

**不採 (b) 的理由**：(b) 需要指出一條被違反的 AC／INV。3.2 逐條檢視後沒有；把「第 3 個以後的排隊請求必須看到 `upstream_unreachable`」或「伺服器端不得在停滯期間累積佇列」讀進契約，會新增 OC 未涵蓋的 requirement（治理 §5.3 第 1 類），DA 不得以 decision／addendum 隱性擴張 baseline（§3.6-A 末段）。

**先前處置的前提更新（不改結論）**：#35 R1 F-2 的 non-blocking 理由依賴「每個 instance 一次只處理一個請求」與「10 s 平台時限」兩個假設。P-4 證明前者**不成立**（instance 會同時處理多個請求）、後者**過於保守**（文件時限 300 s，8 s 上限遠在其內）。兩者相抵後，可達的殘餘比原先擔心的更小：原先擔心的「第 2 個請求 16 s 超過平台時限變成平台錯誤」不會發生；實際殘餘只是 k ≥ 3 時的訊息具體度與伺服器端佇列。先前 phase acceptance §5.3「#35 R1 F-2／#40 R1 F-2：修正屬 HOW，只能在後續合法授權的變更中處理，non-blocking」的處置**維持**，事實基礎以本節取代。

### 3.4 記錄的契約解讀（供後續引用；不改變 accepted 語義）

R-V2-OBS-13 的「伺服器對上游請求 MUST 設定逾時，且 MUST 小於部署平台的 function 執行上限，使上游停滯以 `upstream_unreachable` 分類回應、而非平台層 gateway 錯誤」，其約束對象是**單次上游請求的逾時值**相對平台上限，目的是讓「一次上游停滯」得到分類回應；它與同條「前端對任何非 JSON 或平台層錯誤回應仍 MUST 依 failure 處理（不得停在進行中）」和「每次 Refresh MUST 在有界時間內到達終態」構成兩層：伺服器層盡力分類、前端層保證終態。契約沒有、也不應被讀成「在任意並行度下每個 client 都必定在其自身上限內收到伺服器分類」。這是既有條文唯一合理的讀法（治理 §3.6-A 第一種情形：只有一種合理解讀而尚未寫下），故以本 addendum 記錄即可，不另開 decision record；它不改變 R-V2-OBS-13 的任何字句、不改變任何 AC 的 PASS 條件。

### 3.5 Disposition、owner 與 routing

| 項目 | 內容 |
| --- | --- |
| Severity／blocking | Low、non-blocking（維持 Reviewer 判定；DA 同意其理由） |
| 對本 phase 的效果 | 無。不 gate phase acceptance、不 gate release gate 的任何 DA 項目 |
| Tracked item | **T-F1**：「觀測／雷達服務在上游取得期間持鎖，CWA 停滯＋同一 instance ≥ 3 個並行請求時，第 3 個以後的使用者看到頁面的 `no_response` 而非伺服器的 `upstream_unreachable`；停滯期間伺服器端佇列與各請求的上游重試會累積（頁面放棄的請求仍佔位並各嘗試一次上游）。」 |
| **Owner** | **acceptor**——決定是否指示後續 work item。依 Bindings §4 第 3 列，這是「已結案工作之後的單點修正」，需要 acceptor 的直接指示作為其 Outcome Contract；在此之前只是 tracked item，不得作為新工作執行（治理 §1.2）。DA 不建議也不反對，只說明路徑與邊界 |
| 若 acceptor 指示修正 | 修正屬 **HOW**（例如：不跨上游呼叫持鎖、single-flight 讓等待者共用同一次取得結果或同一次失敗、或對停滯中的請求快速回分類失敗），MUST 保持：只重用成功（R-V2-OBS-9）、伺服器只回成功或分類失敗（INV-V2-6）、逐請求讀金鑰且零外洩（R-V2-SEC-3／7、INV-V2-2）、8 s 上游上限與 README 文件化（R-V2-OBS-13）、觀測與雷達路徑獨立（R-V2-DEG-4）。變更會觸及 `observation.py`／`radar.py`（金鑰讀取所在的模組）→ 屬 H-1「觸及的工作」，依 decision A-4 該 Lightweight work item **需 independent audit**；並在 #35／#37 既有的並行 probe 上重驗（≥ 3 個並行停滯請求皆在 20 s 內得到分類 JSON 為其自然 oracle——那是該 work item 的驗證設計，不是本 Spec 的新 AC） |
| 若 acceptor 要求「任何並行度下都必須收到伺服器分類」或「停滯期間伺服器不得排隊」作為**保證** | 那是新的 requirement——contract change（治理 §5.3 第 1 類），須由 acceptor 明示接受，不是本 Spec 的缺陷 |
| 額度面 | 停滯期間每個排隊請求各嘗試一次上游，是對 CWA 額度的放大；OC-V2 §5 風險與 derivation §11 #3（速率限制為 Later、acceptor 日後可另指示）已涵蓋，不另開項目 |
| 需要 Final Adjudicator | 否——沒有 review 爭議或 routing 爭議 |

### 3.6 相關觀察的處置

- **Post-key record O-1（README 平台時限用語）**：README l. 409–410「below Vercel's smallest default function duration (10 s)」是保守的舊值，結論（8 s ＜ 時限）仍正確；l. 573–574「The server itself answers within about 8 s even when CWA stalls」對單一請求成立、對排隊請求不成立，但同段已寫明頁面 20 s 上限與「the platform holds the request」的處理。AC-V2-21(8) 的 oracle（記載 endpoint、失敗代碼、逾時、重用視窗）成立；(12)「與 V2 矛盾的舊敘述」不適用（這不是與 V2 行為矛盾的敘述，是平台事實的保守版本）。**non-blocking**；若 acceptor 想更新措辭（例如改為「below the platform's function duration limit」並補一句排隊情形），是結案後的 Lightweight 文件修正（不觸及 H 類別；README 已是 MUST 文件但此句非老師指定介面）。
- **Post-key record O-2（`vercel.live` 注入）**：維持 #41 R1 F-2(a) 的既定判定——平台注入、不在 subject 內、不是 AC-V2-16／INV-V2-3 違規；且兩個 headless session 實際上外部請求 0。

---

## 4. SIA F-1、#38～#40 地圖可用性交接與其他 tracked items——處置不變

- **SIA F-1**（375 px「觀測 Stale＋雷達 Stale＋選縣」組合態下狀態區累積至 606 px，首屏無地圖）：post-key 驗證在 1280 與 375 的 success 態進行，未觸及此組合態，也沒有新證據改變其契約判定。**維持先前 §5.1 的處置**：無 AC／INV 違反；non-blocking；owner acceptor（是否指示結案後 UI work item）；若要求「375 px 首屏必有地圖」的保證，是 contract change。
- **#38～#40 交接（O-1 指標可達性、#39 R1 F-3、#39 R1 O-2、#39 R2 O-5／O-6／O-7、#40 R1 F-1、#39 R1 F-2）**：post-key record 在 preview 上的行為觀察（22 個代表標記、雷達 pane `pointer-events: none`、圖層順序）與 SIA 判定一致，無新證據。**維持先前 §5.2 的處置**（全部 non-blocking；#39 R1 F-2 已閉合）。
- **先前 §5.3 其他項目**：SIA O-3（應用內觀測授權全名，SHOULD）、#41 R1 F-1（network-log 數字，editorial）、#41 R1 O-1／SIA O-4（`CONTEXT.md` 詞條）、#35 R1 F-3／#36 R1 F-1／#37 R1 F-1（Low）、#41 R1 O-3（A-6 CI 引用位置）——**全部維持**。#41 R1 F-2 的兩項程序註記已由 post-key 派工落實（record §1、O-2）——**已閉合**。#35 R1 F-2／#40 R1 F-2／#40 R1 O-3 一列由第 3 節取代其事實基礎，處置不變。
- **`ACCEPTANCE-V2.md` 的字面狀態**：post-key 後 `doc/acceptance/` 零變更，其 §1／§5／§6.2／§7 仍寫 BLOCKED 與 #41 R1 F-1 的舊數字。依先前 §3.3「紀錄位置」列，這個更新是 MAY、「不做亦可」；**本 addendum 與 post-key record 是 P-1～P-4 結果的權威紀錄**，`ACCEPTANCE-V2.md` 的字面不構成 gate 缺口。若 acceptor 想讓該檔自洽，是結案後的 Lightweight 文件修正（只改狀態與引用文字；不觸及 H 類別）。

---

## 5. Gate 材料的狀態（本 addendum 之後；供 acceptor 參考，不是授權）

| Gate 項目 | 先前紀錄 | 本 addendum 之後 | 依據 |
| --- | --- | --- | --- |
| Bindings §5 Formal：全部 Ticket 依 Orchestrator Contract §7 結案 | 完成 | 完成 | 先前 §2.1 |
| Bindings §5 Formal：每份 Spec 的 Spec Integration Audit 已 closure | 完成（可完成範圍） | **完成（全範圍）**——cycle 1 SIA instance 的 RB-3 缺口由其 post-key 證據補完 record 填補 | `spec-SPEC-V2-c1-r1.md`＋`spec-SPEC-V2-c1-r1-postkey.md` |
| Bindings §5 Formal：Design Authority phase acceptance 已完成 | 完成於可完成範圍 | **完成（全範圍）** | 先前紀錄＋本 addendum |
| Bindings §5：README 實跑 | 完成 | 不變 | wl41 V-9；#41 R1；SIA |
| Bindings §5：無追蹤中的機密 | 完成 | 不變；post-key 另證實金鑰生效的 preview 回應面零外洩 | SIA INV-V2-2；post-key §4、§7 |
| A-6 另附：A-2 SQL、A-5 CI 引用 | 完成 | 不變（`e75303c` CI `36237807133`、`36237805654` 另可引用） | 先前 §6 |
| A-6 另附：preview 觀測驗證紀錄（AC-V2-17(c)、22） | 未具備 | **具備** | post-key §6.1 |
| SPEC-V2 §6.4 Release 列：acceptor 已填 Vercel 金鑰的 preview 驗證（合併前） | 未具備 | **具備** | post-key record 全文 |
| OC-V2 AB-V2-2／10／13 部署部分 | 未驗證（BLOCKED） | **已驗證** | 2.4 |
| P-2 Vercel runtime log 金鑰格式自查 | — | **acceptor release 自查**（不阻擋） | 先前 §3.3 P-2；2.3 |
| SPEC-V2 §6.4：合併後對 production 重跑 smoke 與觀測抽樣 | 合併後 release evidence | 不變（合併後） | AC-V2-22；DR-12 先例 |

**結論：DA 認定 pre-merge gate 已清——宣告的 release-gate 材料中屬於 Formal 流程、Spec §6.4 合併前列與 A-6 的項目全部具備；剩下的只有 acceptor 自己的 release 動作與自查。是否合併（RB-1）仍由 acceptor 決定。**

---

## 6. Phase 狀態（治理 §3.8：分別陳述，不互相冒充）

| 陳述 | 狀態 | Authority |
| --- | --- | --- |
| Work item completion（#35–#41） | 完成（不變） | Orchestrator 依 Reviewer 判定 |
| **Phase acceptance（SPEC-V2 v2.2）** | **完成（全範圍）**：先前 ACCEPTED（可完成範圍）＋本 addendum 結清 P-1～P-4。Accepted subject 仍為 **`9902026`**（產品碼）。**沒有剩餘的 pre-merge blocker 由 DA 持有** | Design Authority |
| Run completion | Orchestrator 於 run record 陳述；post-key follow-on 為同一 run identity 的契約內 re-verification（先前 §3.3 步驟 1） | Orchestrator |
| Outcome Contract closure（OC-V2 全 acceptance boundary） | **phase 面的前提已齊備**：AB-V2-1～13 經 SPEC-V2 全部分配且在 `9902026` 的產品碼上有 PASS 證據（AB-V2-13 的 production 部分依 AC-V2-22 為合併後 release evidence）。closure 判斷仍是 acceptor 的 | acceptor |
| Release authorization（RB-1 合併進 `main`） | **未授權；未請求 Agent 執行；本紀錄不是授權。** DA 先前「不建議在 addendum 前合併」的保留**解除**：DA 現在不持有反對合併的 gate 理由。PR **#43**（`home_work_01-v2-implementation` → `main`）已依 SA-2 開啟、未合併；`origin/main` ＝ `08e158e` | **acceptor（RB-1）** |
| Submission（RB-2） | **未授權** | **acceptor（RB-2）** |

**合併時的 subject 規則（先前 §10 的延伸）**：合併的產品碼必須仍是 `9902026`（即分支 HEAD 相對 `9902026` 只多 `doc/governance/**` 與 `tickets-v2.md` 狀態列）。合併前若對 `home_work_01/` 任何其他路徑作變更（含 `doc/acceptance/`、README 措辭、F-1 的修正），該變更不在本 phase acceptance 的 coverage 內：依 Bindings §4 第 3 列以 acceptor 直接指示開新的 Lightweight work item，並依 A-4 判斷是否需 independent audit。

---

## 7. 是否改變 accepted 語義；boundary determination

**否。** 本 addendum 不 derive 新契約、不修改 Spec、不新增或移除任何 AC／INV／gate、不調整 §5.3 儀器；P-1～P-4 的結清是先前紀錄既定計畫的執行結果；F-1 的裁決只確認既有條文（R-V2-OBS-10／12／13、R-V2-DEG、INV-V2-6／7、S-6、AB-V2-3／4／5）在新事實下仍成立，並記錄其唯一合理的讀法（3.4），不建立其他工作將依賴的新設計基線；T-F1 只是 tracked item。屬治理 §5.3 第 2 類（不改變 accepted 語義）／§3.6-A。

**Boundary determination（治理 §1.2）**：不需要——post-key record §8 明記無 boundary 符合性 finding、無需 route DA 的契約語義不足；F-1 不是 boundary finding。沒有 fail-closed 至 acceptor 的路徑。

---

## 8. 受影響 work items 與 bookkeeping

| 對象 | 影響 |
| --- | --- |
| #35–#41 | 無重開；結案狀態不變。#41 Remaining work 1（P-1～P-4）**結清**。 |
| Orchestrator | (1) 記錄本 addendum 於 run record「Post-key verification」段，並陳述 run 的最終狀態；(2) 完成報告 MUST 分別陳述第 6 節五項；(3) 依先前 §3.3「紀錄位置」列，`worklog/issue-41.md` 補一列指向 `audit/spec-SPEC-V2-c1-r1-postkey.md` 與本 addendum（DA 核對時該 worklog 尚無此列；record-only、不影響 subject；非 gate）；(4) 原樣 commit 本 addendum（Bindings §3.5 第 4 點）；(5) 向 acceptor 回報第 9 節的 release 動作與自查項目；不合併（RB-1）。 |
| acceptor | 第 9 節。 |
| SPEC-V2 v2.2、derivation record、DV-20～23、Bindings | 不需修改。derivation §11 #1 以本紀錄 2.3 P-4 列解決，不需修訂 derivation record。 |
| `ACCEPTANCE-V2.md`、`tickets-v2.md`、README | 本紀錄不改；4 節與 3.6 的可選 Lightweight 文件修正只在 acceptor 指示時進行。 |

---

## 9. 需要其他 authority 的事項

| 事項 | Authority | 理由 | 是否阻擋 phase acceptance |
| --- | --- | --- | --- |
| 合併 PR #43（`home_work_01-v2-implementation` → `main`） | **acceptor（RB-1）** | Bindings §2.6；gate 材料見第 5 節（DA 側已齊備） | 否（phase acceptance 已完成） |
| Release 時自查 Vercel runtime log 無金鑰格式字串（P-2 log 面；只掃描、不匯出） | acceptor | 先前 §3.3 P-2；RB-3 禁止 Agent 進入後台 | 否 |
| （選擇性）在 Vercel 後台確認 Fluid compute 與 Default Max Duration 未被設為 ≤ 8 s | acceptor | post-key §6.4 的殘餘不確定；無任何跡象 | 否 |
| 合併後 production `smoke.py` 與觀測抽樣（AC-V2-22 release evidence） | acceptor（或依其直接指示的 Agent） | SPEC-V2 §6.4；DR-12 先例 | 否 |
| 繳交作業 | **acceptor（RB-2）** | Bindings §2.6 | 否 |
| 是否指示 T-F1（3.5）、SIA F-1／#38～#40（4）、O-1 README 措辭、`ACCEPTANCE-V2.md` 字面更新、O-3 應用內授權全名等結案後 Lightweight work items | acceptor | 治理 §1.2 tracked items；Bindings §4 第 3 列；A-4 | 否 |
| Final Adjudicator | — | 沒有 review 或 routing 爭議 | — |

本紀錄不向 acceptor 請求任何動作；只列出 OC-V2 與 Bindings 原本就保留給 acceptor 的 release 與 reserved 動作。

---

## 10. Evidence（DA 自行執行，全部唯讀；未印出任何金鑰）

- **讀取**：Bindings b3；治理 v2.0 §1.2、§1.4、§1.5、§2.1–§2.4、§3.3–§3.8、§4.6–§4.7、§5.1–§5.3；`phase-acceptance-SPEC-V2.md` 全文；`spec-SPEC-V2-c1-r1.md` 全文；`spec-SPEC-V2-c1-r1-postkey.md` 全文；`issue-35-c1-r1.md` 全文、`issue-35-c1-r2.md` 全文、`issue-40-c1-r1.md` §7–§8、`issue-37-c1-r1.md` AC-V2-06(e) 列與 §(d)；`derivation-SPEC-V2.md` §11；SPEC-V2 v2.2 R-V2-OBS-6～13、R-V2-DEG-1～5、R-V2-RAD-3／4、AC-V2-03～09、17、22、INV-V2-6、§5.3；OC-V2 S-6、AB-V2-3／4／5／13、§8 前置 6；run record l. 96–137（post-key 段全文）；README l. 400–420、568–579；`worklog/issue-41.md` 的 P-1～P-4 與 BLOCKED 段；`observation.py:530–598`；`radar.py:370–423`；`static/app.js:263、277–278、297、313–314、760–860、940–969`。
- **Git**：HEAD `ee0b75b0442d8a6f3044674abb5227c747529a13`（branch `home_work_01-v2-implementation`）；`origin/main` `08e158e565785b56df63520a3f1307723f76b623`；`git merge-base --is-ancestor 9902026 e75303c` 成立；`git diff --name-only 9902026 e75303c` ＝ 5 個 `doc/governance/**` ＋ `doc/ticket/tickets-v2.md`；`git diff --stat 9902026 e75303c -- home_work_01 ':!home_work_01/doc'` 空；`git rev-parse` `home_work_01/static`＝`a27d174e1c368c2d5aaeb1fab386742bfc15e6bb`、`server.py`＝`0692caee99557fc457dc2189830216800ff32fea`、`observation.py`＝`6f19255ce487531c049a2999f2b8a83a4cece018`、`radar.py`＝`a10b83cab602ebdd87a55cd8514a8cd0a2256fe2` 於 `9902026` 與 `e75303c` 相同；`git log --oneline 9902026..HEAD` ＝ 9 個 record-only／索引 commit；`git diff --name-only 9902026 HEAD -- home_work_01/doc/acceptance` 空；`git diff --name-only 08e158e HEAD -- . ':!home_work_01'` 空；`git status --porcelain` 只有審查前即存在、無關的 `grep.exe.stackdump`。
- **GitHub**：`gh api repos/yotsubamomo/aiot-classwork/deployments/6678056047` → sha `e75303c…`、Preview、`vercel[bot]`、2026-09-26T11:07:14Z；`…/statuses` → success、`https://aiot-hw01-weather-8qeq3ey4t-nchu-aiot-class.vercel.app`；`gh run list --commit e75303c…` → `36237807133`、`36237805654` 皆 completed success；`gh pr list --head home_work_01-v2-implementation --state all` → **#43 OPEN**。
- **Bindings §3.4 核對指令**對 session `05b8408b-260a-46d3-a4fe-ec07e3ec365a/subagents/`（22 個 agent）：`agent-a55f579063a0b44bd` ＝ `gov-primary-reviewer` `[('claude-opus-5-5','xhigh')]`；9 個 `gov-primary-reviewer` 皆 `claude-opus-5-5`／`xhigh`；7 個 `gov-executor` 皆 `claude-opus-5-5`／`high`；6 個 `gov-design-authority` 皆 `claude-fable-5-1`／`xhigh`。與 Bindings §3.1 及 run record 一致。
- **未執行**：未對 preview 或 CWA 發出任何請求；未重跑 pytest、瀏覽器檢查或停滯重現（以 post-key record 與各 audit record 為據，治理 §3.8）；未讀 `home_work_01/.env`；未接觸 Vercel；未使用任何金鑰。
