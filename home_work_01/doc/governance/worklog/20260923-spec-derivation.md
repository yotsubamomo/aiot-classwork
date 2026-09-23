# Worklog — 2026-09-23 Spec derivation（Design Authority 派工）

依 Minimal Operational Governance v2.0 §3.7 的八項 properties。

## Work performed

1. 主 session 核對狀態：`main` 為 `c45ec61`；Outcome Contract 第 8 節仍為「尚未接受」；Bindings §8.2 #1–#3 已完成（PR #17 合併、`gov-*` definitions 已載入），#4 binding dry-run 與 #5 高風險類別未完成；`doc/spec/`、`doc/governance/decisions/` 尚不存在。
2. 以 Agent tool 派工 `gov-design-authority`（fresh context，非 fork），bounded pack 只含檔案路徑、acceptor 指示原文、狀態事實、產出位置與邊界；未放入本 session 的結論。
3. Design Authority 自行讀取 Outcome Contract、brief、CONTEXT、上位契約、bindings、治理本文與 `week02` Spec 前例後，寫出 Spec v1.0、derivation record 與兩份 decision record（見 Artifacts）。
4. 主 session 依 Bindings §3.4 核對 binding（見下），確認 `git status` 只有四個新檔，掃描無金鑰格式字串。

5. **一致性修正（同日，acceptor 指示）**：以 SendMessage 續派同一個 Design Authority assignment（`agent-a80296b90d87819af`），要求先重讀檔案再修正四項：接受用語、生效／重新 derive 條件、金鑰掃描範圍（排除被忽略的 `home_work_01/.env`）、AC-04 共用模組措辭（瀏覽器 JS 只打 `/api/`）。Design Authority 修訂 Spec 為 **v1.1**（連帶修正 R-SHR-5、INV-1、INV-5、AC-07、R-SEC-1；新增 §10 版本紀錄），並更新三份 record；回報未改任何 normative 決定、AB 分配不變。主 session 再次核對 binding、變更路徑、金鑰掃描，並抽查修正條款（§0、R-SEC-1、AC-04、AC-07、R-SHR-5、§9 #1、§10）與 Spec 內殘留的「已接受／accepted」用語（僅剩正確用法）。

## Contract reference

Acceptor 2026-09-23 於對話中的直接指示（`/to-spec` 派工文：「Derive the implementation-ready Spec for `home_work_01` … SPEC DERIVATION ONLY … Do NOT implement. Do NOT create Tickets yet …」）。Outcome Contract（`c45ec61`）尚未接受，故本次產出的 Spec 尚非有效 derived contract；效力條件記於 Spec §0 與 derivation record。

## Executing role and binding reference

- 派工者：主 session（model `claude-fable-5-1`，harness 顯示）；只做派工、核對與紀錄，未做設計裁決。
- Design Authority：`agent-a80296b90d87819af`，`agentType = gov-design-authority`，observed `('claude-fable-5-1', 'xhigh')`（Bindings §3.4 指令輸出）。與 Bindings §3.1 的 `design_authority` mapping（`claude-fable-5-1`、`xhigh`）一致。無 replacement。
- 注意：Bindings §8.2 #4 的正式 binding dry-run 尚未執行；本筆核對是本次實際派工的證據，不取代 dry-run。

## Decisions and assumptions

- 全部設計裁決由 Design Authority 作出並自寫紀錄（derivation record 的 B-1～B-16、decision record 的 H-1～H-3 與 DR-1～DR-16）；主 session 未改寫、未篩選。
- Design Authority 回報：無使 Spec 無法 derive 的矛盾；未重開已結案裁決。
- 未依 `/to-spec` skill 把 Spec 發布到 issue tracker：Bindings §7 規定 Spec 放 `doc/spec/`、Tickets 才開 GitHub Issues；acceptor 指示本輪不建 Ticket。

## Artifacts

| 動作 | 路徑 | 作者 |
| --- | --- | --- |
| 新增 | `home_work_01/doc/spec/SPEC.md`（v1.1，DERIVED，待 Outcome Contract 接受後生效；v1.0 → v1.1 為同日一致性修正） | Design Authority |
| 新增 | `home_work_01/doc/governance/decisions/derivation-SPEC.md` | Design Authority |
| 新增 | `home_work_01/doc/governance/decisions/decision-20260923-high-risk-categories.md` | Design Authority |
| 新增 | `home_work_01/doc/governance/decisions/decision-20260923-spec-interpretation-rulings.md` | Design Authority |
| 新增 | 本檔 | 主 session |

未 commit；未修改 Outcome Contract、brief、CONTEXT.md、上位契約或任何實作檔案。

## Verification

- Binding：Bindings §3.4 指令輸出 `agent-a80296b90d87819af gov-design-authority [('claude-fable-5-1', 'xhigh')]`。
- 變更範圍：`git status --short` 只列 `home_work_01/doc/governance/decisions/` 與 `home_work_01/doc/spec/`。
- 機密：四個新檔 grep `CWA-[0-9A-F]{8}-` 命中 0；Design Authority 回報未讀取 `.env` 與 PDF。
- 未執行任何程式碼測試（無實作）。

## Audit status

Not required：Spec derivation 是 Design Authority 的設計行為；其正式審查是 Formal run 中每張 Ticket 的 audit 與 Spec Integration Audit（治理 §4.7），於實作後執行。如實標示「完成且依 policy 未要求 independent audit」。

## Remaining work

| 事項 | 阻擋原因 | 負責 |
| --- | --- | --- |
| RB-5 授權：GitHub Actions workflow 須放在 repo 根 `.github/workflows/`（單元目錄外）；Design Authority 建議在接受紀錄中給出有範圍的授權（本單元專用、路徑過濾 `home_work_01/**`） | 保留動作 | acceptor |
| Vercel 專案建立、Root Directory＝`home_work_01`、部署不需登入可存取；smoke test 的 repository variable | RB-3／第三方帳號 | acceptor |
| ~~Outcome Contract 接受~~ | 已完成 2026-09-23（見 outcome-contract §8；SPEC v1.1 隨之生效） | — |
| ~~Bindings §8.2 #4 binding dry-run~~ | 已完成 2026-09-23，PASS 6／6（`docs/governance/binding-verification.md`） | — |
| 本機安裝 Python 3.12 | — | acceptor |
| Ticket derivation（下一輪 DA 工作） | 待上述接受 | `gov-design-authority` |
| Commit 本次產物到 topic branch | 未要求 | acceptor 指示後依 SA-1 |
