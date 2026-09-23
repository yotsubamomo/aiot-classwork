# Worklog — 2026-09-23 grill → Outcome Contract draft（Lightweight，採用前）

依 Minimal Operational Governance v2.0 §3.7 的八項 properties。本 work item 發生在 Project Bindings b1 生效（PR 合併）之前；acceptor 於對話中裁定「Treat governance as the target operating model for home_work_01」，故以治理格式記錄，供重開 session 後接手。

## Work performed

1. 讀取上位契約（PDF、`REQUIREMENTS.md`、課程總覽），對 Streamlit／SQLite／Pandas／Folium 做五類證據分析，提出架構選項；acceptor 裁決 S1–S5。
2. 以 acceptor 授權、用本專案的 CWA 金鑰對 `opendata.cwa.gov.tw` 做唯讀 GET：F-A0010-001 兩個 endpoint 皆 404（金鑰有效）；F-D0047-091 回 200，結構記入 brief §4.5。金鑰未出現在任何輸出、檔案或紀錄。
3. 背景研究（三個 general-purpose 子代理）：Streamlit 部署平台事實、F-A0010-001 現況、替代資料集；結果經本 session 逐項複核後才寫入 brief（未複核者標「二手／未驗證」）。
4. 發現老師 repo `huanchen1107/AIoT_L3_CWA_HW1`（2026-09-23 完成，F-D0047-091、22 縣市、Leaflet、Vercel）；acceptor 裁定為 IMPORTANT CURRENT REFERENCE，非上位契約。
5. 檔案操作（acceptor 逐項指示）：`backend/.env` 移至 `home_work_01/.env`（先確認 `.gitignore:11` 忽略）；刪除 `frontend/.env`、`backend/`、`frontend/`；新增 `home_work_01/.env.example`（只有變數名）。
6. 新增 `home_work_01/CONTEXT.md`（詞彙）；root `CONTEXT-MAP.md` 加一列（acceptor 已 ratify，RB-5）。
7. 產出 `doc/brief/BRIEF.md`、`doc/governance/outcome-contract.md`（DRAFT）與本 worklog。

8. **後續（同日）**：acceptor 撤回「需老師確認」，裁定 D2 為專案內部決定並結案（W1 視窗、Mapping A、算術平均一位小數、驗證與標示要求）；宣告 Vercel 為必要部署目標、撤回 R1；S1／S3 只在 Vercel 相容性範圍內重開。以實際 F-D0047-091 樣本驗算 D2 方案（W1／W2、Mapping A／B、mean／envelope）。背景研究 Vercel Python runtime、stlite、Next.js＋sql.js；直接讀取老師 repo 的 `vercel.json`、`api/index.py`、`server.py`。更新 `CONTEXT.md`（Forecast Day、Region mapping、Compatibility value、Assigned dataset、Replacement source、County）、brief §4.6–4.7、§5、§6、§7，重寫 outcome-contract（D2 CLOSED、Vercel 必要、§2.1 邊界措辭、架構相關條款標 provisional）。

9. **架構簽核（同日）**：以 Vercel、stlite、Next.js 研究與老師 repo 模式提出 V1–V5；acceptor 裁決 A1 V3（一個產品、兩個呈現層、共用查詢語義、行為對等）、A2 Python 3.12、A3 部署地圖 Leaflet／本機 Streamlit 不需地圖／Folium 不再必要、A4 Flask；撤回 `/_stcore/health` 檢查。依此重寫 outcome-contract（移除全部 provisional 標示、§2.4 架構 CLOSED、AB 重編為 17 條涵蓋兩個呈現層）、更新 brief §1–3、§5、§6.6、§7 與 `CONTEXT.md`（Web App／Grading App／Dashboard）。

## Contract reference

Acceptor 在對話中的直接指示（`/grill-with-docs` 的 brief 與各回合裁決；原文摘錄見 outcome-contract §8.1）。無已接受的 Outcome Contract；本 item 是收斂 Outcome Contract 的 grill 與行政作業，不是作業主體的實作。

## Executing role and binding reference

主 session，model `claude-fable-5-1`（harness 顯示）。此 binding 符合 Bindings §3.1 的 `design_authority`／`alternate_reviewer`／`final_adjudicator` 而非 `executor`；因治理尚未生效且本 item 不含實作，記錄為事實，不主張任何治理角色。子代理三個皆為 `general-purpose`（研究用，非 `gov-*`）。

## Decisions and assumptions

- 全部 scope／技術／部署決定由 acceptor 裁決，見 outcome-contract §8.1；本 session 只提出選項與建議。
- 未決：H-1／H-2 高風險類別（待 DA）；Outcome Contract 的接受（待 acceptor）。D2 與架構皆已結案。
- 假設：acceptor 的 CWA 金鑰是其本人的（acceptor 於授權時聲明）。

## Artifacts

| 動作 | 路徑 |
| --- | --- |
| 新增 | `home_work_01/CONTEXT.md`、`home_work_01/.env.example`、`home_work_01/doc/brief/BRIEF.md`、`home_work_01/doc/governance/outcome-contract.md`、本檔 |
| 修改 | root `CONTEXT-MAP.md`（+1 列） |
| 移動 | `home_work_01/backend/.env` → `home_work_01/.env`（未追蹤） |
| 刪除 | `home_work_01/frontend/.env`、`home_work_01/backend/`、`home_work_01/frontend/` |
| 既有（本次之前） | `home_work_01/doc/requirement/REQUIREMENTS.md`（本 session 稍早轉寫）、`Taiwan_Weather_Forecast_course_overview.md`（acceptor 提供） |

尚未 commit；版本以 acceptor commit 時的 SHA 為準。

## Verification

- `git check-ignore -v home_work_01/.env` → `.gitignore:11`；`.env.example` 由 `.gitignore:13` 解除忽略。
- `grep -c "CWA-"` 於 F-D0047-091 回應：0；`REQUIREMENTS.md` 不含 PDF 內的金鑰字串（grep 0）。
- CWA endpoint 狀態碼與 data.gov.tw 頁面由本 session 直接取得；老師 repo 內容由本 session 直接讀取；CWA 下架公告全文未能直接讀取（JS 應用）。
- 未執行任何程式碼測試（無實作）。

## Audit status

Not required：採用前的 Lightweight 行政與文件工作，Bindings §5 未要求 independent audit；如實標示「完成且依 policy 未要求 independent audit」，非 audit PASS。

## Remaining work

| 事項 | 阻擋原因 | 負責 |
| --- | --- | --- |
| acceptor 審閱 outcome-contract／brief 的最終 delta | 待 acceptor | acceptor |
| Bindings PR 合併、重開 session、binding dry-run | RB-1、session | acceptor |
| 接受 Outcome Contract（§8） | 待上兩項 | acceptor |
| DA derive Spec／Tickets；Formal run | 待接受 | `gov-design-authority`、Orchestrator |
| Commit 本次產物到 topic branch | 未要求 commit | acceptor 指示後依 SA-1 |
