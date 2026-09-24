# HW10 票務索引（`home_work_01/`）

票本身開在 GitHub Issues；本檔只放索引——編號、標題、scope class、high-risk、依賴、狀態與連結——不複製票內容（Bindings §7；CLAUDE.md）。

- **Repository**：<https://github.com/yotsubamomo/aiot-classwork>
- **來源 Spec**：[`../spec/SPEC.md`](../spec/SPEC.md) v1.1（EFFECTIVE，2026-09-23）
- **Outcome Contract**：[`../governance/outcome-contract.md`](../governance/outcome-contract.md)（ACCEPTED 2026-09-23，normative 內容 `c45ec61`）
- **Derivation record**：[`../governance/decisions/derivation-SPEC.md`](../governance/decisions/derivation-SPEC.md) 第 11 節（Tickets 的 derivation、分配與 boundary determination）
- **拆票**：2026-09-24，Design Authority（`gov-design-authority`），Issues #18–#25
- **紀錄位置**（Bindings §7）：worklog `doc/governance/worklog/issue-<n>.md`；audit `doc/governance/audit/issue-<n>-c<cycle>-<r1|r2|alt>.md`；Spec Integration Audit `doc/governance/audit/spec-SPEC-c<cycle>-<r1|r2|alt>.md`
- **Label**：`ready-for-agent`（`docs/agents/triage-labels.md`）
- **分類**：MVM／ENHANCED 是 Spec 的 scope class；INTEGRATION／FINAL VERIFICATION 只用於 #25，表示整合驗證票，不承載新需求
- **Overnight run policy**：[`../governance/decisions/decision-20260924-unattended-run-policy.md`](../governance/decisions/decision-20260924-unattended-run-policy.md)（合法停止條件、非停止條件、stop report 內容、run 前檢查表）
- **執行**：Bindings §6 並行度 1；blocking edges 給出唯一順序＝編號順序 #18 → #25

| # | 票 | Scope class | High-risk | Blocked by | 狀態 | Commit |
| --- | --- | --- | --- | --- | --- | --- |
| [#18](https://github.com/yotsubamomo/aiot-classwork/issues/18) | Ingestion：從 F-D0047-091 推導六 Region × 七 Forecast Day 的 Forecast Snapshot 並持久化到 `data.db` | MVM | H-1、H-2、H-3 | — | 已結案 | `7ee299c` |
| [#19](https://github.com/yotsubamomo/aiot-classwork/issues/19) | 共用查詢／領域模組與 Grading App（`app.py`）：Select Region、一週折線圖與表格 | MVM | H-2、H-3（H-1 靜態檢查） | #18 | 已結案 | `0672020` |
| [#20](https://github.com/yotsubamomo/aiot-classwork/issues/20) | Dashboard MVM：Flask `/api/` 與靜態頁面在本機提供相同的 Region 查詢行為 | MVM | H-1、H-2 | #19 | 已結案 | `0f5f00e` |
| [#21](https://github.com/yotsubamomo/aiot-classwork/issues/21) | Dashboard 部署到 Vercel：公開 URL 與健康 endpoint smoke | MVM | H-1 | #20 | 已結案 | `f02a1df` |
| [#22](https://github.com/yotsubamomo/aiot-classwork/issues/22) | 自動化測試整合與 GitHub Actions CI／smoke workflow | ENHANCED | H-1 | #20、#21 | 已結案（AC-22 (c) 待 RB-1 後 release evidence，DR-18） | `88b871e` |
| [#23](https://github.com/yotsubamomo/aiot-classwork/issues/23) | Dashboard UI／UX 品質與響應式版面 | ENHANCED | H-2 | #21、#22 | 已結案 | `5312c6f` |
| [#24](https://github.com/yotsubamomo/aiot-classwork/issues/24) | Select Date 與 Leaflet Taiwan Map：依 Derived Map Temperature 著色 | ENHANCED | H-2、H-3 | #23 | 已結案 | `f9f9f15` |
| [#25](https://github.com/yotsubamomo/aiot-classwork/issues/25) | 整合驗收：README 實跑、驗收文件、最終 smoke 與 Spec Integration Audit subject 準備 | INTEGRATION／FINAL VERIFICATION（非 scope class；含 ENHANCED 最終核對） | H-1、H-2、H-3 | #22、#24 | 已結案 | `75389e6` |

狀態值：待執行／執行中／audit 中／已結案（引用 audit record）／BLOCKED（引用 stop report）。Commit 欄填結案時的 subject SHA。

## 執行順序與依賴

```text
#18 Ingestion（MVM）
 └─ #19 共用模組＋Grading App（MVM）
     └─ #20 Dashboard MVM 本機（MVM）
         ├─ #21 Vercel 部署（MVM）
         │    ├─ #22 CI／smoke workflow（ENHANCED）   ← 也被 #20 阻擋
         │    └─ #23 UI／UX（ENHANCED）              ← 也被 #22 阻擋
         │         └─ #24 Select Date＋Taiwan Map（ENHANCED）
         └─────────── #25 整合驗收 ← 被 #22、#24 阻擋
```

- MVM 票（#18–#21）只依賴 MVM 票；ENHANCED 票（#22–#24）在 MVM 之上；#25 分類為 **INTEGRATION／FINAL VERIFICATION**（不是 MVM 也不是 ENHANCED；acceptor 2026-09-24 指示重新分類，原標 MVM），是 Spec 要求的整合／驗證工作，合法地依賴全部 MVM 與 ENHANCED 票。重新分類未改變 #25 的需求、DoD、依賴、驗證責任或覆蓋。
- 依賴同時以 GitHub 原生 issue dependencies（blocked by）建立，共 10 條邊；票內 `Blocked by` 段為權威。

## 拆票原則

- 每張票是穿過所有層的垂直切片，可獨立驗證：#18 跑完就有可用 SQL 驗證的 `data.db`；#19 跑完老師就能 `streamlit run app.py`；#20 跑完本機就有對等的 Dashboard；#21 跑完就有公開 URL。
- 沒有獨立的 prefactor 票：單元從零開始，環境骨架與測試佈局併入 #18；共用模組（兩層的測試接縫）併入 #19，因為它與 Grading App 一起才有使用者可見的結果。
- 部署（#21）刻意排在 ENHANCED 之前：先證明 Vercel 路徑（SQLite 唯讀、Python 3.12）可行，再迭代 UI。
- CI（#22）緊接部署之後，讓 #23、#24 有回歸證據。
- README 由每張票各自增補該票的段落，#25 做端到端實跑與最終核對。

## Acceptor 前置動作（到達該票前完成，否則該路徑 BLOCKED）

| 動作 | 需要的票 | 依據 |
| --- | --- | --- |
| 建立 Vercel 專案、連結 repo、Root Directory ＝ `home_work_01`、受審 commit 的部署不需登入可存取 | #21 | RB-3；Spec §9 #3 |
| 設定 smoke 用的 repository variable（公開 URL；變數名由 #22 在 README 文件化） | #22（AC-22） | RB-3；Spec §9 #4 |
| 本機 Python 3.12 | #18 | Spec §9 #5 |
| 開 Orchestrator 主 session（`claude-opus-4-8`／`high`）並依 Bindings §3.4 核對 | 全部 | Bindings §3.3 |

RB-5 GitHub Actions 例外已於 Outcome Contract §8.2 授權（只服務 `home_work_01`、path filter `home_work_01/**` 與 workflow 檔本身）；#22 只能在此範圍內動 root。

## 實作過程中的調整

（執行後由 Orchestrator／Executor 依 worklog 補記。）

## Post-baseline 追加 work item（合併前）

| # | 票 | 類型 | High-risk | Blocked by | 狀態 | Commit |
| --- | --- | --- | --- | --- | --- | --- |
| [#28](https://github.com/yotsubamomo/aiot-classwork/issues/28) | Taiwan Map 視覺重做（map-first、vendored 向量深色底圖、溫度藥丸、浮動面板/圖例、Select Date 併入地圖） | POST-BASELINE ENHANCEMENT（**Lightweight**，DR-20） | H-2、H-3 | #24、#25 | 實作完成＋self-verified（163 pytest 綠、零外部請求、V-1..V-5、七日 parity）；待 A-4 independent audit | 見 worklog／PR |

- Outcome Contract：acceptor 2026-09-24 指示（Bindings §4 第 3 列）。lane／boundary／HOW 採納：`doc/governance/decisions/decision-20260924-taiwan-map-rework.md`（DR-20）。
- 不重開 #18–#25；不改 Spec／Outcome Contract。A-4 必做 independent audit（fresh Primary Reviewer）；audit `doc/governance/audit/issue-28-c<cycle>-<r1|r2|alt>.md`；worklog `doc/governance/worklog/20260924-taiwan-map-rework.md`。
- 另一 acceptor 授權的獨立 Lightweight work item：#18 R2 N-1（`--acquired-at` 格式驗證），獨立票、A-4 audit、不與地圖票混同一 commit（待建立）。
