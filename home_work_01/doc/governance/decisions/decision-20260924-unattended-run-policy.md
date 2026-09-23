# Decision record — Unattended overnight Formal run：停止條件、非停止條件與 stop report（`home_work_01/`）

- **紀錄類型**：Design Authority decision record（治理 §3.6-A：在不改變任何 accepted 語義的前提下裁決解讀；§5.3 第 2 類）
- **日期**：2026-09-24
- **適用範圍**：`home_work_01/` 依 Spec v1.1 與 Tickets #18–#25 進行的 Formal run（Orchestrator run-to-completion），含其中每個 Ticket 的 Executor、Reviewer、Alternate Reviewer、Final Adjudicator、Design Authority 派工
- **Authority 來源**：治理 v2.0 §1.4、§1.5、§2.4、§3.8、§4.1–4.5；Bindings b1 §2.5、§2.6、§3.3、§4、§5、§6；Outcome Contract（ACCEPTED 2026-09-23）§4、§8.2；Spec v1.1；acceptor 2026-09-24 execution policy（第 1 節逐字）
- **執行角色**：`gov-design-authority`（binding 核對由派工者依 Bindings §3.4 記錄）
- **性質**：本紀錄不創造 authority、不擴張任何角色權限、不豁免任何 audit；它把既有治理與 acceptor 的 standing instruction 對到本專案的具體條款，並裁決 Spec／Tickets 中可能被誤讀為「需要 acceptor」的解讀。

## 1. Acceptor 的 execution policy（2026-09-24，逐字引用）

> The intended execution policy for the later Orchestrator is: once the Formal run starts, continue autonomously from the first ready Ticket through #25; do not pause between Tickets merely to ask for confirmation; do not pause for routine self-verification; do not pause for normal implementation choices already inside the accepted Spec / Ticket boundary; do not pause merely because an independent audit returns FAIL; when a Ticket or audit fails for an implementation-correctable reason, autonomously route it back for repair, re-run required verification, and re-audit according to governance; after Ticket closure, automatically continue to the next ready Ticket; use the effective Outcome Contract, Spec, Ticket graph, and governance as standing authorization for work already within scope; do not reinterpret ordinary implementation details as acceptor decisions; do not ask the acceptor to approve every Ticket transition, repair, verification pass, or reviewer finding.
>
> The later Formal run may stop only when continuation genuinely requires new authority or a reserved action, including: a new product / scope / architecture decision outside the accepted Outcome Contract / Spec; a normative Spec or Outcome Contract change; RB-1 merge to `main`; RB-2 submission; RB-3 account / project / repository-variable / third-party-account action; RB-4 payment; RB-5 outside the explicitly authorized `home_work_01` GitHub Actions workflow scope; RB-6; missing credentials or authentication that the Agent is not authorized to resolve; an external service failure that remains unrecoverable after reasonable retries.
>
> Do NOT treat the following as acceptor blockers: ordinary implementation defects; compilation / runtime errors; test failures; failed self-verification; reviewer findings; audit FAIL that can be repaired inside the Spec; code-quality fixes; dependency-install issues that can be resolved without changing the accepted contract; implementation HOW choices delegated by the Spec.

## 2. Design Authority 的判定：與治理一致

| Policy 句 | 對應治理／Bindings | 判定 |
| --- | --- | --- |
| 「continue autonomously … do not pause between Tickets … after Ticket closure, automatically continue」 | 治理 §1.4：work item 完成、phase boundary、findings、rework、DA decision、Final Adjudication、rollover 都 MUST NOT 成為等待 operator 的理由；orch-default §4 步驟 10「完成一個 work item 不需 operator 確認」 | 一致；是治理本文的重述 |
| 「do not pause merely because an independent audit returns FAIL … route it back for repair, re-run required verification, and re-audit according to governance」 | 治理 §4.4：R1 blocking → targeted correction → R2 → exactly one Alternate → Final Adjudication；§4.5 disposition 邊界與新 cycle 的兩個合法起點 | 一致。「re-audit」依 §4.4 的 R2 scoped closure review，不是無限制的第二次 R1；新 cycle 只由 FA 授權的 material rework 或 DA 的 contract change 開始 |
| 「use the effective Outcome Contract, Spec, Ticket graph, and governance as standing authorization」 | 治理 §1.2：Outcome Contract 一次接受＋授權規劃、分解、實作、審查、修正至完成；Spec／Tickets 為 derived contracts；Bindings §2.5 SA-1、SA-2；§5.2「Spec review 與獨立 implementation authorization 不保留」 | 一致；沒有新增授權 |
| 「do not reinterpret ordinary implementation details as acceptor decisions」 | 治理 §2.4：契約內 HOW 屬 Executor；語義屬 DA；只有接受／授權缺口屬 acceptor；§3.3 routing condition 的三分法 | 一致 |
| 停止條件清單 | 治理 §1.5 四項（唯一權威清單）＋Bindings §2.6 RB-1～RB-6＋Outcome Contract §8.2 的 RB-5 例外 | 一致；第 3 節逐項對應 |
| 「Do NOT treat the following as acceptor blockers」 | 治理 §1.5「工具失敗、context 問題或 Agent 不可用 MUST 先走已授權的 recovery／replacement 路徑」；§4.2「契約不足是 routing signal」；§2.4 DA-first | 一致；第 4 節擴充本專案的具體情況 |

**結論**：policy 未擴張任何 authority，也未弱化任何 gate；它是治理 §1.4／§1.5 在本 run 的 standing instruction。Orchestrator 依本紀錄與治理執行，不需在每個 Ticket 邊界回問 acceptor。

## 3. 合法的停止條件（只停止受影響路徑；治理 §1.5、orch-default §9）

| # | 條件 | 治理／Bindings 依據 | 本專案的具體情況 |
| --- | --- | --- | --- |
| S-1 | Outcome Contract 的接受與授權本身 | §1.5 第 1 項 | 已完成（2026-09-23）；run 中不會再出現，除非 S-2 |
| S-2 | 需要 re-authorization 的 boundary 變更：預期結果超出 Outcome Contract scope／constraints、改變 accepted 語義、normative Spec 變更；或 DA 無法確立在 boundary 內而 fail-closed；或 Reviewer 的 boundary finding 在 DA determination 後仍有爭議 | §1.2、§1.5 第 2 項、§5.3 第 1 類、§4.7 | 例如：需要第二個替代資料集、放棄 Vercel、改 22 縣市、改 DDL、改六區語義。**先派 DA**；DA 確立在 boundary 內則繼續，只有 DA 無法確立時才停 |
| S-3 | RB-1 合併進 `main` | Bindings §2.6 | run 不需要合併即可完成 #18–#25；合併是 #25 之後的 release 動作 |
| S-4 | RB-2 繳交 | 同上 | run 外 |
| S-5 | RB-3：申請、輪替或填寫憑證；第三方帳號操作——Vercel 專案建立、Root Directory、production branch、deployment protection；GitHub repository variable；任何需要登入 acceptor 帳號後台的設定 | 同上；Spec §9 #3、#4 | #21 的 Vercel 前置與 #22 AC-22 的 variable 前置；未完成時依第 4 節 N-9、N-10 處理 |
| S-6 | RB-4 付費：Vercel 要求信用卡、付費方案、付費 API | 同上 | 若 Hobby 註冊要求信用卡，屬 acceptor 決定 |
| S-7 | RB-5 超出 §8.2 授權範圍：任何 root 檔案或其他單元的修改，除了「只服務 `home_work_01`、path filter 限定 `home_work_01/**` 與 workflow 檔本身」的 `.github/workflows/` workflow | Outcome Contract §8.2 第 2 點 | 例如修改 root `CLAUDE.md`、`docs/`、`.gitignore`、Bindings 檔、其他單元；`.github/workflows/` 內非本單元的 workflow |
| S-8 | RB-6 破壞性 git：force push、改寫已 push 歷史、刪除非本 run 建立的分支 | Bindings §2.6 | 不需要這些動作即可完成 run |
| S-9 | 缺少 Agent 無權取得的憑證或驗證：`home_work_01/.env` 不存在或金鑰無效（CWA 回 401）、`gh` 未登入或 token 失效、Vercel 部署需登入才可存取 | §1.5 第 4 項；RB-3 | 依 §1.5 先 re-ground（確認 `.env` 存在、`gh auth status`）；仍缺則停止該路徑 |
| S-10 | 外部服務在合理重試後仍無法恢復：CWA API 持續 5xx／404（F-D0047-091 也下架）、Vercel 平台故障、GitHub Actions／API 故障 | §1.5 第 4 項 | 「合理重試」依第 5 節 |
| S-11 | Recovery 三步（re-ground、replacement／repair、routing）完成後繼續執行仍 unsafe 或 indeterminate；進行中 assignment 結果無法確認且可能已產生不可逆副作用 | §1.5 recovery 段 | 例如：無法確認某次 push 是否成功且可能重複 |
| S-12 | Model／Agent 替代的 fallback 列耗盡 | Model Profile §3 規則 4 | 先依 R-EX／R-PR／R-AR／R-FA／R-DA 替代；耗盡才進 §1.5 |

以上之外，**沒有其他停止條件**。Bindings §2.6 明文禁止 Agent 臨時增加「保險起見問 operator」的 gate（治理 §5.2）。

## 4. 明確不是停止條件的事項

### 4.1 Acceptor 清單（逐字對應第 1 節第三段）

N-1 ordinary implementation defects；N-2 compilation／runtime errors；N-3 test failures；N-4 failed self-verification；N-5 reviewer findings；N-6 audit FAIL that can be repaired inside the Spec；N-7 code-quality fixes；N-8 dependency-install issues resolvable without changing the accepted contract；N-9 implementation HOW choices delegated by the Spec（Spec §4.2 的全部委派項目）。

### 4.2 本專案 Spec／Tickets 中可能被誤判為需要 acceptor 的點（DA 裁決其解讀）

| # | 情況 | 裁決 | 依據 |
| --- | --- | --- | --- |
| N-10 | **#18 fixture 擷取與 ingestion 真跑需要 `.env` 內 acceptor 的 CWA 金鑰** | 已授權，不是停止條件。Outcome Contract AB-8「Ingestion 以使用者自己的 CWA 金鑰從 F-D0047-091 取得 JSON」與 §5「既有產物：`.env`（未追蹤，acceptor 的 CWA 金鑰）」即為讀取與使用該金鑰的授權；RB-3 只保留申請、輪替、填寫。Executor 讀取既有 `.env` 執行 ingestion 一次（AC-07(a)）、擷取 fixture（DR-10）皆在授權內。只有 `.env` 缺失或金鑰無效時才是 S-9。 | OC AB-8、§5；Bindings §2.6 RB-3；DR-10 |
| N-11 | **#22 AC-22 在 repository variable 缺席時** | 不是整張票的停止條件。#22 的其餘 AC（AC-20、AC-21、AC-29、AC-07 自動化）照常完成；AC-22 的 `workflow_dispatch` 實跑路徑寫一份 stop report（S-5，RB-3）後，**#22 可以在 audit 中以「AC-22 實跑待 acceptor 變數」的狀態進入 R1**；Reviewer 對 AC-22 只能判定「未驗證（外部前置）」而非 FAIL。AC-22 的最終驗證本來就分配給 #25（derivation record §11.1）。Orchestrator 記錄該路徑 BLOCKED，繼續 #23、#24；到 #25 時若變數仍缺席，才是最終的 S-5 停止。 | 治理 §1.5「只停止該路徑」、§3.8；derivation record §11.1 |
| N-12 | **#21 Vercel 專案不存在或部署需登入** | 這是真正的 S-5（RB-3）前置：#21 及其後全部 Ticket 都依賴它，run 會在 #21 停止。**因此列入第 6 節 run 前檢查表**；acceptor 在啟動 run 前完成即可避免。若 run 中才發現，Orchestrator 寫 stop report 並停止；不得自行建立 Vercel 專案或改帳號設定。 | Spec §9 #3；RB-3 |
| N-13 | **Vercel 部署失敗（build 失敗、function 例外、SQLite 唯讀讀取失敗、runtime 版本不符）** | 屬 N-1／N-2：Executor 在單元目錄內修正部署設定或程式（HOW），以 push 觸發重新部署（SA-1），重跑 smoke。不是停止條件。只有失敗原因是**只有 acceptor 能改的帳號／專案設定**（S-5）、要求付費（S-6）、或平台故障經第 5 節重試仍無法恢復（S-10）時才停止。SQLite 唯讀在 Vercel 若確實不可行，屬設計問題 → 派 DA（不是 acceptor）；DA 在 Outcome Contract 內裁決（例如以唯讀複本到 `/tmp` 開啟仍是 HOW）。 | §1.5、§2.4；Spec §9 已知風險 |
| N-14 | **Python 3.12 未安裝或套件安裝失敗** | 套件問題屬 N-8：Executor 調整版本 pin、改用等價套件（在 Spec 技術棧內）。Python 3.12 缺席：Executor MAY 以使用者層級、不需管理員權限、不付費的方式安裝（例如 `uv python install`、`py` launcher 的使用者安裝），這是環境 HOW，不是 RB；需要管理員權限或帳號密碼才是 S-9。列入第 6 節檢查表。 | §1.5 第 4 項；Spec R-ENV-1 |
| N-15 | **Audit 回 FAIL** | §4.4 路徑：targeted correction → R2 → 一次 Alternate → FA。FA 的 deferred disposition 若涉及 H-1／H-2／H-3，須派 DA 確認（decision record A-3），仍是自主派工。同一 root cause 在新 cycle R2 後仍未解 → FA 交 DA，不是 acceptor。 | §4.4、§4.5 |
| N-16 | **Executor／Reviewer 提出 material ambiguity、兩種解讀、需猜語義、修 finding 要改 invariant** | 派 DA（`gov-design-authority` subagent）；DA 以 decision record 裁決或以 derivation record 作 boundary determination；只有 DA 判定為 contract change 或無法確立 boundary 時才成為 S-2。 | §2.4、§3.6 |
| N-17 | **Spec 寫「手動驗收清單＋截圖」（AC-17、AC-18、AC-19）** | 「手動」指非自動化測試的驗證，由 **Executor** 以瀏覽器（含 headless 瀏覽器工具）操作與截圖，Reviewer 核對；不是 acceptor 的動作，不是停止條件。 | Spec §5.2「手動驗收清單＋截圖」 |
| N-18 | **AC-12 README 端到端實跑、AC-01 `streamlit run app.py`** | Executor 在本機執行；不是 acceptor 動作。 | Spec AC-01、AC-12 |
| N-19 | **AC-13「PR 已開」、topic branch push、commit `data.db` 與 fixture、建立 `doc/acceptance/`** | SA-1、SA-2 standing authorization；不是停止條件。合併（RB-1）不是完成條件。 | Bindings §2.5；DR-12 |
| N-20 | **GitHub Actions 因 push 自動執行、Vercel 因 push 自動建置** | 公開 repo 的 Actions 與 Vercel Hobby 皆免費；不是 RB-4。若平台要求付費才是 S-6。 | Bindings §2.6 RB-4 |
| N-21 | **`.github/workflows/` 內建立本單元 workflow** | 已由 Outcome Contract §8.2 授權（範圍：只服務 `home_work_01`；path filter `home_work_01/**` 與 workflow 檔本身）；不是停止條件。超出範圍才是 S-7。 | OC §8.2 |
| N-22 | **GitHub Issue 的狀態操作（加註解、關閉、改 label）與 `doc/ticket/tickets.md` 狀態欄更新** | Orchestrator 的控制面 bookkeeping；依 `docs/agents/issue-tracker.md` 慣例；不是 RB。Issue 關閉以 audit closure record 為依據，不以 Executor 敘述。 | orch-default §2「控制面操作不在此限」 |
| N-23 | **Model 不可用或 binding 不符** | 依 Model Profile §3 deterministic replacement（引用當次錯誤證據）；記錄 `diversity_lost`；不是停止條件，fallback 耗盡才是 S-12。 | Bindings §3.1；Model Profile §3 |
| N-24 | **Context rollover、需要新的 Executor／Reviewer session** | §1.4 明列；接手 session 沿同一 worklog identity。 | §1.4、§3.7 |
| N-25 | **Spec Integration Audit 與 DA phase acceptance** | 自主派工（`gov-primary-reviewer`、`gov-design-authority`）；「phase adjudication 是自主派工，不是 operator checkpoint」。 | §3.8、§4.7；impl-default §6 |
| N-26 | **Bindings §8.2 表的 #3、#4 狀態欄仍寫「待辦」** | 實質前提已滿足（`docs/governance/binding-verification.md` PASS 6／6；definitions 已載入並實際派工）。該表格文字是 Bindings 檔案的 metadata，更新屬 RB-5（root 檔），由 acceptor 方便時處理；**不阻擋 activation**。orch-default §3 核對的是 bindings 就緒且可驗證，不是表格文字。 | Bindings §8.2；orch-default §3 前提 3 |
| N-27 | **Reviewer 認為「缺少 Spec 條款」或契約不足** | routing signal → DA；不是 blocking finding，也不觸發 promotion 或停止。 | §4.2 |
| N-28 | **OPTIONAL 項目（排程更新）被提出** | 不做；不是停止條件（Spec §8：本 Spec 不 derive）。 | Spec §8 |

## 5. 「合理重試」與外部服務失敗的邊界（S-10 的操作定義）

治理 §1.5 規定恢復義務「不以次數或門檻計算」，只有三步完成後仍 unsafe／indeterminate 才停。因此本節不設數字上限，而是定義三步在本專案的具體內容；三步完成仍失敗即為 S-10：

1. **Re-ground**：確認失敗屬外部服務而非本專案程式（例如以 CWA 的其他公開 endpoint、Vercel 狀態頁、GitHub 狀態頁或另一次獨立請求佐證）；記錄 HTTP 狀態、時間、回應摘要（不含金鑰）。
2. **Repair／replacement**：對可修的部分修正（設定、重試邏輯、部署重推）；對暫時性失敗以指數退避重試，至少涵蓋 Spec 的 90 秒暖機視窗與一次完整的重新部署；CWA 取得失敗時，若已提交的 `data.db` 快照仍有效，**MVM 不因此受阻**（Spec §9：已部署快照仍可服務），只有需要新快照或 fixture 的 #18 路徑受影響。
3. **Routing**：若失敗揭露設計問題（例如替代資料集也下架），派 DA；DA 若判定需要 Outcome Contract 外的決定 → S-2。

三步後仍無法繼續 → 寫 stop report（第 7 節）並停止該路徑；其他不依賴該服務的 Ticket 工作繼續。

## 6. Run 前檢查表（acceptor 於啟動前完成；缺項會在對應 Ticket 成為合法停止）

| # | 項目 | 影響 | 依據 |
| --- | --- | --- | --- |
| P-1 | **Orchestrator 主 session** 模型 `claude-opus-4-8`、effort `high`，以 Orchestrator Contract §3 啟用句指定並先讀 `gov-orchestrator` definition；不設定會覆寫角色綁定的全域 subagent model；以 session transcript 核對 binding 記入 run record | 全部（activation 前提） | Bindings §3.3、§3.4；binding-verification 備註 1、2 |
| P-2 | `home_work_01/.env` 存在且金鑰有效（2026-09-23 曾成功） | #18 | N-10、S-9 |
| P-3 | `gh auth status` 有效（issue 操作、PR、Actions 查詢） | 全部 | S-9 |
| P-4 | 本機 Python 3.12 可用 | #18 起 | N-14 |
| P-5 | Vercel 專案已建立並連結本 repo、Root Directory ＝ `home_work_01`、受審 commit（topic branch）的部署**不需登入**可存取 | #21 起 | N-12、S-5 |
| P-6 | 若 Vercel 註冊要求信用卡：acceptor 已決定 | #21 | S-6 |
| P-7 | Smoke 用的 repository variable 已設定（變數名由 #22 在 README 文件化；acceptor 可先與 Orchestrator 約定名稱，或在 #22 開始後設定） | #22 AC-22、#25 | N-11 |
| P-8 | 工作樹乾淨或已知；`main` 的 HEAD 已記錄為 BASE | 全部 | impl-default §7 |

P-5、P-7 缺席不會讓 run 立即失敗：run 會完成 #18–#20，在 #21 停止（P-5）或在 #22 只停 AC-22 路徑（P-7）。

## 7. Stop report 內容（治理 §1.5；orch-default §9）

每個停止點 Orchestrator MUST 在 run record 與受影響 Ticket 的 worklog 寫入：

1. **Run identity 與受影響路徑**：run id、Ticket 編號、停止時間、受影響的 AC／路徑；**不受影響、仍在繼續的路徑**。
2. **現況**：subject identity（branch、commit SHA）、已完成與未完成的 AC、最後一次 verification／audit 狀態與 record 引用。
3. **缺少事項**：具體缺什麼（例如「Vercel 專案未連結」「repository variable X 未設定」「`.env` 缺失」），對應第 3 節的 S-n 與 RB-n。
4. **已嘗試的 re-ground／replacement／routing 及其結果**：三步各做了什麼、證據引用（HTTP 狀態、時間戳、record 路徑）。
5. **所需 authority 與理由**：acceptor（並指明是 RB-n 或 §1.5 第幾項）；若是 DA fail-closed，附 DA 的 derivation／decision record 引用。
6. **下一步**：acceptor 完成該動作後，Orchestrator 從哪個 checkpoint、以什麼指令恢復；恢復時依 §3.8 從權威紀錄 re-ground。
7. **不含金鑰**；不含 Executor 結論的轉述作為 evidence。

## 8. 是否改變 accepted 語義

**否。** 本紀錄只把治理與 acceptor 的 standing instruction 對應到本 run 的具體條款，並裁決既有 Spec／Ticket 文字的解讀（N-10～N-28）。沒有新增或移除任何 requirement、AC、invariant、gate 或 reserved boundary；沒有改變依賴圖；沒有豁免任何 audit（含 Spec Integration Audit）。若 run 中出現本紀錄未涵蓋的情況，依治理 §2.4 route：語義 → DA；接受／授權 → acceptor；routing 爭議 → FA。

## 9. 受影響 work items 與 evidence

- Tickets #18–#25 全部；Orchestrator run record；各 Ticket worklog 的 stop report 格式。
- Evidence：治理 §1.4、§1.5、§2.4、§3.8、§4.1–4.5；Bindings §2.5、§2.6、§3.3、§3.4、§4、§5、§6；orch-default §3、§4、§5、§9；Model Profile §3；Outcome Contract §4、§5、§8.2；Spec v1.1 §4.2、§5.2、§8、§9；`docs/governance/binding-verification.md`；Issues #18–#25 的 Reserved 段。
