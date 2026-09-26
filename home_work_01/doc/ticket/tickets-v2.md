# HW01 Weather Map V2 票務索引（`home_work_01/`）

票本身開在 GitHub Issues；本檔只放索引——編號、標題、scope class、high-risk、依賴、狀態與連結——不複製票內容（Bindings §7；CLAUDE.md）。V1 索引 [`tickets.md`](tickets.md)（#18–#25、#28、#29）不變。

- **Repository**：<https://github.com/yotsubamomo/aiot-classwork>
- **來源 Spec**：[`../spec/SPEC-V2.md`](../spec/SPEC-V2.md) **v2.2**（DERIVED，2026-09-25；以參照繼承 V1 Spec v1.1）
- **Outcome Contract**：[`../governance/outcome-contract-v2.md`](../governance/outcome-contract-v2.md)（ACCEPTED 2026-09-25，normative candidate `69c5a04`）
- **Derivation record**：[`../governance/decisions/derivation-SPEC-V2.md`](../governance/decisions/derivation-SPEC-V2.md) 第 15 節（Tickets 的 derivation、分配、覆蓋矩陣與 boundary determination）
- **拆票**：2026-09-25，Design Authority（`gov-design-authority`），Issues #35–#41；方法為 repo 指定的 `/to-tickets`（tracer-bullet 垂直切片、prefactoring 先行、blocking edges、固定 issue 範本），baseline `main` `b0642f8`
- **紀錄位置**（Bindings §7）：worklog `doc/governance/worklog/issue-<n>.md`；audit `doc/governance/audit/issue-<n>-c<cycle>-<r1|r2|alt>.md`；Spec Integration Audit `doc/governance/audit/spec-SPEC-V2-c<cycle>-<r1|r2|alt>.md`
- **Label**：`ready-for-agent`（`docs/agents/triage-labels.md`）
- **分類**：V2 Core／V2 Radar 是 Spec 的 scope class（皆 ENHANCED REQUIRED，只在部署的 Dashboard）；INTEGRATION／FINAL VERIFICATION 只用於 #41，表示整合驗證票、不承載新需求（V1 #25 先例）
- **Overnight run policy**：V1 的 [`../governance/decisions/decision-20260924-unattended-run-policy.md`](../governance/decisions/decision-20260924-unattended-run-policy.md) 可沿用（OC-V2 §6）
- **執行**：Bindings §6 並行度 1。技術 blocking edges 在 #36 之後分為兩條分支（#37 → #41；#38 → #39 → #40 → #41），#41 等待兩條分支皆結案；**偏好的執行順序** #35、#36、#37、#38、#39、#40、#41 是並行度 1 下的排程偏好，不是 blocked-by edge（acceptor 2026-09-25 指示：不得把並行度 1 編成假的技術依賴）

| # | 票 | Scope class | High-risk | Blocked by | 狀態 | Commit |
| --- | --- | --- | --- | --- | --- | --- |
| [#35](https://github.com/yotsubamomo/aiot-classwork/issues/35) | 伺服器端 Latest Observation 路徑：`/api/` 觀測回應、四類失敗分類與安全邊界 re-scope | V2 Core | H-1、H-2、H-3 | — | 已結案（audit `issue-35-c1-r1`/`r2`；R1 BLOCKING F-1 → R2 CLOSURE） | `5f0dbc3` |
| [#36](https://github.com/yotsubamomo/aiot-classwork/issues/36) | Now mode 與 Forecast mode：預設 Now、模式切換、全臺代表測站的 Latest Observation 與 Observation Time／Fetched Time | V2 Core | H-2、H-3 | #35 | 已結案（audit `issue-36-c1-r1`；R1 CLOSURE；F-1 Low、R-1→DA 追蹤） | `f63ebb1` |
| [#37](https://github.com/yotsubamomo/aiot-classwork/issues/37) | Refresh 與狀態語義：newer／not-newer／failure、Stale／Unavailable、觀測失敗只影響 Now mode | V2 Core | H-1、H-3 | #36 | 已結案（audit `issue-37-c1-r1`；R1 CLOSURE；F-1/F-2/F-3 Low、R-1→DA） | `7a3b469` |
| [#38](https://github.com/yotsubamomo/aiot-classwork/issues/38) | Taiwan → County → Station 下鑽：縣界互動圖層、County 脈絡、測站清單與詳情、Back to Taiwan、鍵盤路徑 | V2 Core | H-3、H-2 | #36 | 已結案（audit `issue-38-c1-r1`/`r2`；R1 BLOCKING F-1 → R2 CLOSURE；DV-20/DV-21 獨立重驗 PASS） | `286ee9d` |
| [#39](https://github.com/yotsubamomo/aiot-classwork/issues/39) | 地圖圍欄與響應式可用性：pan／zoom 圍欄、初始視野、375 px 底部資訊面、44×44、768 px 破版檢查 | V2 Core | H-2 | #38 | 待執行 | |
| [#40](https://github.com/yotsubamomo/aiot-classwork/issues/40) | Radar overlay：`/api/` 代理、顯示／隱藏、雷達時間戳、獨立狀態與 1 km 地理對齊 oracle | V2 Radar | H-1、H-3 | #39 | 待執行 | |
| [#41](https://github.com/yotsubamomo/aiot-classwork/issues/41) | V2 整合驗收：README 與 CONTEXT 最終審查、V2 驗收文件、定向 V1 重驗、CI 全綠與部署 preview 驗證 | INTEGRATION／FINAL VERIFICATION（非 scope class） | H-1、H-2、H-3 | #37、#40 | 待執行（AC-V2-17(c)、AC-V2-22 觀測部分在 acceptor 填入 Vercel 金鑰前為 BLOCKED，不是 FAIL） | |

狀態值：待執行／執行中／audit 中／已結案（引用 audit record）／BLOCKED（引用 stop report）。Commit 欄填結案時的 subject SHA。

## 執行順序與依賴

技術依賴（blocked-by edges；只反映 Spec 要求的前置）：

```text
#35 伺服器端 Latest Observation 路徑（V2 Core；tracer bullet 的資料面）
 └─ #36 Now mode 與 Forecast mode（V2 Core；使用者可見的 tracer bullet：預設 Now、代表測站、兩個時間、模式切換、Forecast 保留）
     ├─ #37 Refresh 與狀態語義（V2 Core；失敗路徑：Stale／Unavailable、獨立降級）
     │    └─────────────────────────────────────┐
     └─ #38 Taiwan → County → Station 下鑽（V2 Core）  │
         └─ #39 地圖圍欄與響應式可用性（V2 Core）        │
             └─ #40 Radar overlay（V2 Radar；含 1 km 對齊 oracle）
                 └─ #41 V2 整合驗收（INTEGRATION／FINAL VERIFICATION）← 同時等待 #37 與 #40
```

偏好的執行順序（Bindings §6 並行度 1 下的排程偏好，**不是** edge）：#35 → #36 → #37 → #38 → #39 → #40 → #41。Orchestrator 在 #36 結案後 MAY 依既定條件先派 #38 分支再派 #37，兩者對 Spec 而言互不依賴。

- 共 7 條 blocking edges，以 GitHub 原生 issue dependencies（blocked by）建立：35→36、36→37、36→38、38→39、39→40、37→41、40→41；每條邊的 blocker 編號都小於被阻擋票、無環；票內 `Blocked by` 段為權威。#38 不依賴 #37（下鑽只需 #36 的 Now mode 基礎，不需 Refresh／Stale／Unavailable 語義完成；acceptor 2026-09-25 指示修正）。
- #40 排在 #39 之後：若對齊所採的重投影或 CRS 改變地圖投影，#40 須重驗 AC-V2-13 與 AC-V2-15（票內已列），避免 #39 的圍欄儀器在 #40 之後失效。

## 拆票原則

- **垂直切片、tracer bullet 先行**：#35 是資料面的最薄路徑（觀測 `/api/` 可用 API 驗證與離線樣本獨立驗收，如同 V1 #18 的 ingestion）；#36 是使用者可見的 tracer bullet（載入即見全臺 Latest Observation、兩個時間、可切到 Forecast mode）；之後每張票各加寬一個面向：失敗語義（#37）、下鑽（#38）、圍欄與手機（#39）、Radar（#40），最後整合（#41）。
- **沒有獨立的 prefactoring 票**：V2 需要的 prefactoring（靜態檢查 re-scope、憑證掃描延伸、樣本）本身就是 #35 的可驗收內容。
- **每張票只擁有與其切片實質相關的 AC／INV 證據**（Spec §6 的比例性）；AC-V2-20（CI 全綠、V1 產物不變）每票只在自己的範圍內維持，最終由 #41 彙整；不要求每票重跑 AC-V2-01～23。
- **憑證依賴放到最後**：#35～#40 以本機未追蹤 `.env`（A-3）與離線樣本完成實作與驗證；需要 Vercel 金鑰的 preview 證據（AC-V2-17(c)、AC-V2-22 觀測部分）只在 #41，且在 acceptor 執行 RB-3 前記 BLOCKED。
- **Radar 對齊由 #40 明確擁有**（R-V2-RAD-5、AC-V2-19、1 km oracle）；**Forecast 保留由 #36 明確擁有**（AC-17／AC-18 重驗、Forecast mode 原樣、預報區段層級降級），V1 產物不變的證明由 #35（後端）與 #41（最終 blob／diff）承接。
- README 由每張票各自增補該票對應的 R-V2-DOC-1 項目，#41 做最終文件審查（AC-V2-21）與實跑。
- Ticket 不指定 Executor 模型；模型與 binding 是 Orchestrator／Bindings 的事（§3.1、§3.4）。附錄 A 的 UI／UX 建議只是 advisory，不在任何票的 AC 內。

## Acceptor 前置動作（到達該票前完成，否則該路徑 BLOCKED；其餘先做）

| 動作 | 需要的票 | 依據 |
| --- | --- | --- |
| 在 Vercel 專案填入 `CWA_API_KEY`（preview 與 production 環境；不印出、不匯出） | #41（只影響 AC-V2-17(c) 與 AC-V2-22 的觀測部分；其餘 #41 項目與 #35～#40 不需要） | OC-V2 A-2；RB-3（Bindings b3）；Spec §9 #1 |
| 受審 commit 的部署不需登入可存取（V1 既有設定沿用） | #41 | RB-3；Spec §9 #2 |
| 開符合 `orchestrator` mapping 的主 session 並依 Bindings §3.4 核對 | 全部 | Bindings §3.3；Spec §9 #3 |

既有 CI／smoke workflow 預期不需修改；若某票確有必要，只在 OC-V2 A-4 的窄授權內修改並記錄。

## 實作過程中的調整

- 2026-09-26 — **DV-20**（[`../governance/decisions/decision-20260926-ac-v2-01-county-round-trip-allocation.md`](../governance/decisions/decision-20260926-ac-v2-01-county-round-trip-allocation.md)；來源 #36 R1 的 routing signal R-1）：**#38** 追加 AC-V2-01「選縣往返部分」與 R-V2-MODE-5(a) 選縣部分的驗證與實作分配（逐字見 DV-20 §4.1）；Spec Integration Audit 仍為 AC-V2-01 的 Spec 層 owner；#36 分配與結案不變。#38 issue body 已更新（Acceptance criteria／Traceability／Decisions）。不改 accepted 語義（治理 §5.3 第 2 類）。
- 2026-09-26 — **DV-21**（[`../governance/decisions/decision-20260926-county-layer-under-stale-unavailable-allocation.md`](../governance/decisions/decision-20260926-county-layer-under-stale-unavailable-allocation.md)；來源 #37 R1 的 routing signal R-1）：**#38** 追加 AC-V2-08(a)(b)「縣界互動圖層與 County 脈絡在 Stale／Unavailable 下」的驗證與實作分配（逐字見 DV-21 §4.1），含 §4.2 §3.6-A 釐清（Unavailable 縣脈絡缺值顯示「—」、不得為 0 或數值）；Spec Integration Audit 仍為 AC-V2-08／INV-V2-7 的 Spec 層 owner；#37 不變。#38 issue body 已更新。不改 accepted 語義（§5.3 第 2 類）。

## Post-baseline 追加 work item（合併前）

（無。）
