# Worklog — WI-DOC-README-1：HW01 README 重整（文件）

- **Work item**：`WI-DOC-README-1`（**Lightweight**，documentation-only；Bindings §4「單元 `README.md`、`CONTEXT.md`、文件與不改變交付行為的修正」）。無 Grill、無新 Spec、無 Ticket。
- **範圍**：`home_work_01/`（governance on）＋ root `README.md`（governance off；單元目錄外的修改屬 RB-5，本指示明確要求更新 root README 的 `home_work_01` 條目，即為授權）。
- **Branch**：`home_work_01-readme-restructure`（SA-1），parent `main` `a50331d`。PR 依 SA-2；**不合併**（RB-1）、**不提交**（RB-2）。
- **Binding（Bindings §3.3／§3.4）**：Executor = 主 session `de316248-08b6-4df2-b78b-d273bf392565`，`claude-opus-5-5`／`high`，符合 `executor` mapping；未派 subagent。
- **Audit**：Lightweight，**完成且依 policy 未要求 independent audit**（未觸及 H-1：文件只說明金鑰的位置與流程、不含值；未觸及 H-2：老師指定的介面、檔名、資料表與輸出格式都未改，`README.md` 檔名保留）。本紀錄不是 audit PASS。

## Contract reference（Lightweight Outcome Contract，Bindings §2.3）

acceptor 2026-09-26 於本 session 的直接指示（逐字）：

> Update the repository documentation for the completed HW01 Weather Map project.
>
> This is a documentation-only Lightweight change.
> No Grill and no new Spec are required.
>
> Re-ground from the repository first.
>
> Read:
> - root `README.md`
> - `week02/README.md`
> - `home_work_01/README.md`
> - current `home_work_01` implementation / production state
> - relevant tests and docs that reference `home_work_01/README.md`
>
> Use `week02/README.md` as the presentation / information-architecture reference,
> not as content to copy blindly.
>
> ## Objective
>
> Make the repository documentation consistent and submission-friendly now that
> HW01 V2 + UI polish are released.
>
> Production:
> https://aiot-hw01-weather.vercel.app
>
> ## Work
>
> ### 1. Root README
>
> Update the `home_work_01` entry so it accurately represents the completed
> weather project.
>
> Keep the root README concise.
> Include the live demo link and a short current feature summary.
> Follow the style used by the other coursework entries.
>
> Do not duplicate the full homework documentation into the root README.
>
> ### 2. Preserve the existing HW01 README as technical reference
>
> The current `home_work_01/README.md` contains substantial implementation,
> architecture, deployment and verification material.
>
> Preserve it rather than deleting it.
>
> Move / rename it to:
>
> `home_work_01/README.technical-reference.md`
>
> Before doing so, search the repository for:
> - tests that inspect README content;
> - links / anchors that point to the existing README;
> - acceptance / governance references that depend on it.
>
> Update references only where necessary.
> Do not silently discard required documentation claims.
>
> ### 3. Create a new `home_work_01/README.md`
>
> Use `week02/README.md` as the structural and visual documentation reference.
>
> The new README should be concise, polished and oriented toward someone viewing
> the homework repository.
>
> Suggested content:
>
> - project title / short description
> - Live Demo
> - screenshot / preview where appropriate
> - implemented features
> - assignment requirement / grading coverage
> - current weather vs 7-day forecast distinction
> - technology stack
> - data sources
> - local run instructions
> - project structure
> - deployment note
> - important security note (`CWA_API_KEY` is server-side and not committed)
> - links to detailed technical/reference documentation
>
> Accurately describe the released implementation.
>
> Do not resurrect obsolete design proposals from earlier requirements.
> Use the actual repository as the source of truth.
>
> ## Boundaries
>
> Documentation only.
>
> Do not change:
> - application code;
> - tests except where a README-path assertion genuinely requires an update;
> - API behavior;
> - data;
> - deployment configuration;
> - governance contracts.
>
> If moving the old README would break a substantive contract or required test,
> report that before widening scope.
>
> ## Verification
>
> Check:
> - all Markdown links you change;
> - root README references;
> - README anchors / referenced paths;
> - relevant README/static documentation tests;
> - `git diff` contains documentation-only changes unless a narrowly necessary
>   path-reference test update is required.
>
> Use a topic branch, commit, push and open a PR.
> Do not merge.
>
> Report:
> - files changed;
> - old README reference path;
> - root README change summary;
> - new HW01 README structure;
> - verification result;
> - PR URL.

## Re-ground 發現（實作前）

| # | 發現 | 處理 |
| --- | --- | --- |
| F-1 | `tests/test_representative.py` 以 `UNIT_DIR / "README.md"` 守 AC-V2-11（README 不得列舉 22 個偏好 StationId，至多 4 個作為範例）。搬移後若不更新，檢查仍會通過，但**會默默失去**對原詳細內容的覆蓋。 | 必要的路徑更新：同一個測試改為同時檢查 `README.md` 與 `README.technical-reference.md`（各 ≤ 4），`SPEC-V2.md` 維持 0；判準未放寬。其他測試與 workflow 都不讀 README。 |
| F-2 | `doc/acceptance/ACCEPTANCE.md` §2（AC-14，8 項）與 `ACCEPTANCE-V2.md` §2（AC-V2-21，14 項）以**行號**引用「final `home_work_01/README.md`」；R-V2-DOC-3 規定 V1 `ACCEPTANCE.md` 既有條目不改寫、只加參照。 | 舊 README 以 `git mv` **逐位元不變**改名（blob `40c2240b…` 前後相同），行號引用在新檔名下仍有效；兩份驗收文件只加指向說明（V2 那一行的連結改指新檔名，並註明 WI-UI-THEME-1 在 l. 845 後加了兩行），所有證據列未改。 |
| F-3 | **契約條款**：SPEC R-DOC-1 與 SPEC-V2 R-V2-DOC-1 規定「單元 README MUST 含／增補」一系列內容（執行與部署步驟、海報結構對照、兩種模式、代表測站與圖外測站規則、觀測／預報標示差異、CWA 授權、Vercel 金鑰步驟、endpoint 欄位／失敗代碼／時限／重用視窗、圍欄與縮放、Radar、Later 清單）；R-V2-DOC-2 要求 README 有 CWA 授權標示；R-V2-DOC-5／V1 AC-14 規範標示用語。若新 README 只是精簡概覽，會違反這些 MUST。 | **不縮減契約內容、不擴大範圍**：新 `README.md` 仍逐項涵蓋上述 MUST（下表），以精簡措辭呈現，詳細技術項目放在 `<details>` 摺疊區，完整原文保留在技術參考檔。沒有需要 Delta Spec 或 DA 裁決的衝突。 |
| F-4 | Governance 紀錄（decisions、audit、run、worklog）引用 README 的內容與行號。 | 歷史紀錄，描述當時的檔案；不改。 |

### 新 README 對契約條款的涵蓋

| 條款 | 新 `README.md` 位置 |
| --- | --- |
| R-DOC-1：Python 3.12 與 venv、`pip install`、金鑰與 `.env`、ingestion（含離線重跑）、`streamlit run app.py`、本機 Flask、測試 | 「本機執行」1–6 |
| R-DOC-1：Vercel 部署（Root Directory、production／preview）、公開 URL | 「部署（Vercel）」、「專案資料」 |
| R-DOC-1：與海報 `HW10_Weather/` 結構的對應表 | 「專案結構」對應表 |
| R-DOC-2／AC-14 八項：F-A0010-001 下架、F-D0047-091 相容替代、W1 視窗、六區對照為專案定義、`PROJECT-DERIVED COMPATIBILITY VALUES`、Derived Map Temperature 為導出值、Streamlit 定位、不宣稱為 CWA 發布 | 「資料來源與標示」 |
| R-V2-DOC-1 (1) 兩種模式，Forecast mode 有自己的標題且容易找到 | 「Taiwan Map 的兩種模式」＋ `### Forecast mode — 老師 Part A 的加分地圖`（功能清單有連結） |
| (2) O-A0001-001 與逐時節奏（保守描述） | Now mode 小節 |
| (3) 代表測站規則、圖外測站規則 | 技術參考摘要「代表測站規則與地圖範圍外的測站」 |
| (4) 觀測（依發布原樣）與推導值的標示差異 | 「資料來源與標示」對照表 |
| (5)／R-V2-DOC-2 CWA 授權標示（O-A0001-001、O-A0058-006，另 F-D0047-091） | 「CWA 資料授權標示」 |
| (6) Vercel 金鑰步驟（變數名、環境、由 owner 填入、不含值）與本機 `.env` | 「安全性：`CWA_API_KEY`」 |
| (7) 觀測／雷達 endpoint、回應欄位、失敗代碼、時限、重用視窗 | 技術參考摘要第一節 |
| (8) 地圖圍欄與縮放範圍 | 技術參考摘要「地圖圍欄與縮放範圍」 |
| (9) Radar 來源、對齊、重新取得的觸發、metadata／影像、已知限制 | 技術參考摘要「Radar overlay」 |
| (10) 接受的 Later 清單 | 技術參考摘要最後一節 |
| (11) 與 V2 矛盾的舊敘述 | 新文件只描述現況：只有觀測與雷達需要金鑰，預報路徑不需要 |
| R-V2-DOC-5：不把觀測寫成預報、不把代表測站值寫成縣市氣溫、不以 real-time／live 稱呼最新觀測、`Fetched Time` 與預報取得時間分開 | 全文（「Live Demo」只指展示網站） |

## 變更

- `home_work_01/README.md` → `home_work_01/README.technical-reference.md`（`git mv`，內容逐位元不變）。
- 新 `home_work_01/README.md`（繁體中文，資訊架構參考 `week02/README.md`）：專案資料、Live Demo（兩張已提交的截圖）、專案摘要、已實作功能、作業要求對應（Part A 配分表＋Part B 處理）、資料來源與標示（含 CWA 授權）、Taiwan Map 的兩種模式（Now mode／Forecast mode 專節）、技術棧、專案結構（含海報對照）、本機執行、部署、安全性、技術參考摘要（五個 `<details>`）、驗證紀錄、詳細文件。
- root `README.md`：作業表改為與課堂實作一致的「目錄／作業／內容／Live Demo」四欄，`home_work_01` 條目寫實際完成的內容與 Live Demo；GitHub Pages 段補一句 `home_work_01` 部署在 Vercel 的原因與網址。其餘不變。
- `home_work_01/tests/test_representative.py`：AC-V2-11 檢查涵蓋兩份 README（F-1）。
- `home_work_01/doc/acceptance/ACCEPTANCE.md`、`ACCEPTANCE-V2.md`：只加指向說明（F-2）。

未改：任何應用程式碼、其他測試、API、資料、部署設定、governance 契約。

## Verification

| 檢查 | 結果 |
| --- | --- |
| 舊 README 保留 | `git hash-object`：改名前 `home_work_01/README.md` 與改名後 `README.technical-reference.md` 同為 `40c2240b71837f8f9f0d9260f97d669975f258bb`（逐位元相同）。git 的 diff 因同路徑有新 `README.md` 而顯示為「README.md 修改＋技術參考新增」。 |
| pytest（`home_work_01/`） | **625 passed**（含更新後的 `test_readme_and_spec_do_not_enumerate_the_preference_ids`，同時檢查兩份 README）。 |
| 連結與 anchor | 改動的四份文件（root `README.md`、新 `home_work_01/README.md`、`ACCEPTANCE.md`、`ACCEPTANCE-V2.md`）共 **61** 個相對連結、技術參考檔 **100** 個相對連結：目標檔案都存在，`#anchor` 都對應到目標檔的標題（GitHub slug 規則；含中文標題 `#forecast-mode--老師-part-a-的加分地圖`）；0 個問題。外部連結：Live Demo `https://aiot-hw01-weather.vercel.app`（production，已於 WI-UI-THEME-1 smoke PASS）。 |
| 標示用語 | 新 README 無 `real-time`、無「即時」；「Live」只出現在「Live Demo」（展示網站）。README 未列舉任何偏好 StationId。 |
| diff 範圍 | 只有 `.md` 文件，加上 `tests/test_representative.py` 一個必要的路徑更新（F-1）。應用程式碼、API、資料、部署設定、governance 契約都未改。 |
