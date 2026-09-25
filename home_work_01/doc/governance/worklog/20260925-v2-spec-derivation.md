# Worklog — 2026-09-25 V2 Delta Spec derivation（Design Authority 派工）

依 Minimal Operational Governance v2.0 §3.7 的八項 properties。Lightweight work item（Bindings §4：文件；acceptor 直接指示為其 Outcome Contract），產出是 V2 Formal 工作的 derived contract。

## Work performed

1. 主 session 核對狀態：`main` 為 `8c4667d4d20fd82718d6acb4a29392cc5679b516`；V2 Outcome Contract 已接受（normative candidate `69c5a049104b2fd96289d10ff938c2c8a6d59bd4`、接受紀錄 `f853bcbc69ed75a27b77aeb609daabe103c96a25`）；Bindings b3 已生效（PR #31，`0b42208`）；b2 `executor` binding dry-run PASS 已記入 `docs/governance/binding-verification.md`（PR #32，`588ef57`）；`doc/spec/SPEC-V2.md` 與 `doc/governance/decisions/derivation-SPEC-V2.md` 尚不存在。
2. 從 `main` 建立 topic branch `home_work_01-v2-delta-spec`。
3. 以 Agent tool 派工 `gov-design-authority`（fresh context，非 fork）。Bounded pack 只含：acceptor 的 derivation 指示原文、權威輸入的路徑與識別（治理、Bindings b3、V2 Outcome Contract、V2 Brief、V1 Spec v1.1、V1 derivation record、DR-1～DR-22、phase acceptance、V1 acceptance evidence、`CONTEXT.md`、上位契約、現行實作檔、非規範的 Portable SDD Interaction Guidance）、產出位置與邊界（只寫 `doc/spec/`、`doc/governance/decisions/`；不改任何既有檔、不建 Ticket、不 commit、不讀 `.env`）。未放入本 session 的結論或草案。
4. Design Authority 自行讀取後寫出 Delta Spec v2.0 與 derivation record（見 Artifacts），並回報無需 STOP 的事項。
5. 主 session 依 Bindings §3.4 核對 binding（見下）、確認變更路徑只有兩個新檔、掃描金鑰格式字串、抽查文件結構（第 1.2 節 delta 表、第 3 節 AC 表、第 5.3 節驗證儀器、derivation record 的裁決、高風險判定、self-review、未決事項）；寫本 worklog；commit、push、開 PR（SA-1、SA-2）。未 merge（無 RB-1 授權）。

6. **DA 修正輪（同日，acceptor 指示；PR #34 未合併）**：以 SendMessage 續派同一個 Design Authority assignment（`agent-a813b9bb4bfbfd4cc`），原文轉交 acceptor 的五項指示（移除下限「E 全部／22 縣市同時在視窗內」的 PASS 條件、以中心與逐軸規則取代「視窗 ∩ E ≠ ∅」的 pan 儀器、移除 Refresh→Radar 的 MUST 耦合、驗證方法用語去框架化、雷達 1 km oracle 比例性複核），並要求先重讀磁碟上的檔案再修改、只改兩份 DA 文件、不 commit。Design Authority 修訂 Spec 為 **v2.1**（R-V2-MAP-1、R-V2-MAP-2、AC-V2-13、R-V2-RAD-3、AC-V2-18、R-V2-DOC-1(9)、AC-V2-21(10)、R-V2-TC-1、§5.3、§6.1 與八個 AC 證據欄）與 derivation record（§14 修訂列、DV-11／DV-12 重寫、DV-13 補充、B-4／B-10、§9 self-review、§10 evidence），回報：無任何 accepted 語義改變；第 3、5 項不需 acceptor 決定；1 km oracle 保留並記錄理由。主 session 再次核對 binding（同一 agentId，observed `('claude-fable-5-1', 'xhigh')`）、變更範圍（只有兩檔，48＋／44－）、金鑰掃描 0 命中、版本列與修訂列存在，並確認框架名稱只剩 §5.2 HOW 清單與 V1 既有事實的引用。

7. **DA 最終一致性修正輪（同日，acceptor 指示）**：再次以 SendMessage 續派同一個 Design Authority assignment，原文轉交 acceptor 的第 1 項（有效測站定義未要求可解析的 `ObsTime`，與 R-V2-OBS-4 的 dataset-level 最大值及 R-V2-DD-7 的必要欄位不一致）並要求先重讀檔案、只改兩份 DA 文件、升版 v2.2。Design Authority 修訂 Spec 為 **v2.2**：R-V2-OBS-2 新增 (e)「有 CWA 發布且可解析的 `ObsTime`，值如發布、不正規化、解析屬 HOW」並把排除範圍擴及 dataset-level Observation Time 的計算；R-V2-OBS-4(a) 註明只取有效測站、成功回應下恆有定義；AC-V2-05 新增 (7)(8) 反例（壞 `ObsTime` 的站不進圖層、不被選為代表、不計入縣有效數、不決定 dataset-level 最大值；全部壞 → 零有效 → `invalid_response`）；R-V2-TC-1 涵蓋；derivation record DV-3 修訂、DV-2 補充、B-18、§9、§10、§14。回報：治理 §5.3 第 2 類，無任何 accepted 語義改變；六項聚焦檢查 PASS。主 session 依第 2 項把本檔 Artifacts 表的 Spec 版本改為目前 v2.2（保留 v2.0 為初版的敘述），再次核對 binding、變更範圍、版本列、金鑰掃描，commit、push、更新 PR #34，並依 acceptor 對 PR #34 的 item-specific RB-1 授權以 merge commit 合併、驗證 `main`。

## Contract reference

Acceptor 2026-09-25 於對話中的直接指示：「Proceed with V2 DELTA SPEC DERIVATION only … Do NOT: edit the V1 Spec; rewrite V1 requirements; create Tickets yet; implement; start the Orchestrator … Work on a topic branch. SA-1 / SA-2 remain available for: commit; push; PR. Do NOT merge.」上位的 accepted contract：V2 Outcome Contract（`outcome-contract-v2.md`，ACCEPTED 2026-09-25）。

## Executing role and binding reference

- 派工者：主 session（harness 紀錄 `claude-fable-5-1`／`xhigh`）；只做派工、核對與紀錄，未作任何設計裁決。
- Design Authority：`agent-a813b9bb4bfbfd4cc`，`agentType = gov-design-authority`，observed `('claude-fable-5-1', 'xhigh')`（Bindings §3.4 指令輸出）。與 Bindings §3.1 的 `design_authority` mapping（`claude-fable-5-1`、`xhigh`）一致。無 replacement。

## Decisions and assumptions

- 全部設計裁決由 Design Authority 作出並自寫紀錄（derivation record §3.1 boundary items、§3.2 DV-1～DV-19、§6 高風險判定）；主 session 未改寫、未篩選。
- Design Authority 回報：Delta Spec 全部在已接受的 V2 Outcome Contract boundary 內；沒有 contract change；未重開任何 Grill 裁決；未動 V1 normative 文字；不需新增高風險類別；沒有需要 STOP 的事項。
- 主 session 注意到並如實轉達（不裁決）：Design Authority 在 Spec §5.3 選定了客觀驗收用的驗證儀器（與產品語義分開標示），其中雷達對齊 oracle 使單純的 Web Mercator `imageOverlay` 依設計會不通過（DA 估算約 3.8 km 偏移），重投影／CRS 選擇屬 HOW；既有 `tests/test_static_checks.py` 把 `server.py`／`api/index.py` 納入無 HTTP client 集合，須依 DV-15 re-scope。

## Artifacts

| 動作 | 路徑 | 作者 |
| --- | --- | --- |
| 新增 | `home_work_01/doc/spec/SPEC-V2.md`（目前 **v2.2**，DERIVED；v2.0 為 2026-09-25 的初版 derive，v2.1 與 v2.2 為同日依 acceptor 指示的 DA 修正，見 Spec §10；自 2026-09-25 起為 V2 Outcome Contract 的有效 derived contract，以參照繼承 V1 Spec v1.1） | Design Authority |
| 新增 | `home_work_01/doc/governance/decisions/derivation-SPEC-V2.md` | Design Authority |
| 新增 | 本檔 | 主 session |

未修改 V1 Spec、V1／V2 Outcome Contract、Brief、`CONTEXT.md`、上位契約、任何實作、測試、資料或 root 檔案。未建 Ticket。

## Verification

- Binding：Bindings §3.4 指令輸出 `agent-a813b9bb4bfbfd4cc gov-design-authority [('claude-fable-5-1', 'xhigh')]`。
- 變更範圍：派工後 `git status --short` 只列 `home_work_01/doc/spec/SPEC-V2.md` 與 `home_work_01/doc/governance/decisions/derivation-SPEC-V2.md`（另有本 session 前既存、未追蹤的 `grep.exe.stackdump`，不屬本工作）。
- 機密：兩個新檔以 CWA 金鑰格式 regex 掃描命中 0；Design Authority 回報未讀取 `.env`、未使用任何金鑰、未呼叫 CWA。
- 用語：兩檔只在「本專案不使用『V2 MVM』」的說明句出現該詞；Spec 檔頭明示以參照繼承 v1.1，第 1.1 節規定 V2 只在第 1.2 節明列範圍內優先於 V1。
- 未執行任何程式碼測試（無實作）。

## Audit status

Not required：Spec derivation 是 Design Authority 的設計行為；其正式審查是 Formal run 中每張 Ticket 的 audit 與 Delta Spec 的 Spec Integration Audit（治理 §4.7），於實作後執行。如實標示「完成且依 policy 未要求 independent audit」。

## Remaining work

| 事項 | 阻擋原因 | 負責 |
| --- | --- | --- |
| Ticket derivation（Design Authority；derivation record §13 為非約束的分解草案） | 等 acceptor 指示 | acceptor → DA |
| Orchestrator 主 session（`claude-opus-4-8`／`high`）啟動 | Ticket derivation 之後；acceptor 開 session | acceptor |
| Vercel 專案環境變數填入 CWA 金鑰（preview 與 production） | 部署階段；RB-3；AC-V2 的部署驗證項在此之前為 BLOCKED，不是 FAIL | acceptor |
| 本 PR 合併 | RB-1，本輪無授權 | acceptor |
