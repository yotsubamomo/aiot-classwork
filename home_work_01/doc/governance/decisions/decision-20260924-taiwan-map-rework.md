# Decision record — Taiwan Map 視覺重做（post-baseline enhancement，GitHub Issue #28）（`home_work_01/`）

- **紀錄類型**：Design Authority decision record（治理 §3.6-A：在不改變任何 accepted 語義的前提下裁決 lane、boundary determination 與提案 HOW 的採納；治理 §5.3 第 2 類；Bindings §4「模糊或有爭議的分類由 Design Authority 判定，並留 decision record」）
- **編號**：**DR-20**（延續 DR-19 [`decision-20260924-dashboard-state-mapping.md`](decision-20260924-dashboard-state-mapping.md)）；子裁決 DR-20.1～DR-20.6
- **日期**：2026-09-24
- **來源**：acceptor 2026-09-24 指示「Taiwan Map 視覺重做」（原文與核定文見第 0 節；acceptor 審閱的文件為 `orchestrator-message-map-rework.md`，其 §1–§4 由 Orchestrator 轉錄為 GitHub Issue **#28**）。由 Orchestrator 依治理 §2.4 派工 DA；binding 核對由派工者依 Bindings §3.4 記入 run record。
- **本 work item 的 Outcome Contract**：acceptor 2026-09-24 的直接指示（Bindings §2.3 末項、§4 第 3 列）。它**不取代**、也**不修改** `home_work_01` 既有的 Outcome Contract（ACCEPTED 2026-09-23）與 Spec v1.1；後兩者繼續作為產品層級的 accepted 語義（R-EN-1～R-EN-7、R-SHR-4、INV-*、AC-*）約束本 work item。
- **相關契約**：Outcome Contract §2.2（ENHANCED REQUIRED：改良 UI／UX、`Select Date`、Leaflet Taiwan Map、dashboard 整合）、§2.4（一個產品、兩個呈現層；地圖以 Leaflet）、AB-13、AB-14、AB-15；Spec v1.1 R-EN-1～R-EN-7、R-SHR-1、R-SHR-4、R-SHR-5、R-DS-4、R-DS-5、R-DS-6、R-DOC-1、R-DOC-2、R-DOC-4、R-DOC-5、R-TC-1、AC-04(b)、AC-14(6)、AC-17、AC-18、AC-19、AC-27、AC-28、INV-1、INV-2、INV-5、INV-6、INV-7、INV-9、§4.2（HOW 清單）、§8（Out of Scope）；DR-1、DR-4、DR-19；[`decision-20260923-high-risk-categories.md`](decision-20260923-high-risk-categories.md)（H-2、H-3、A-1、A-4）；[`phase-acceptance-SPEC.md`](phase-acceptance-SPEC.md) §10；#24 audit records [`../audit/issue-24-c1-r1.md`](../audit/issue-24-c1-r1.md)、[`../audit/issue-24-c1-r2.md`](../audit/issue-24-c1-r2.md)。
- **執行角色**：`gov-design-authority`（Bindings §3.1：`design_authority` → `claude-fable-5-1`／`xhigh`）。本紀錄不自證 binding。
- **效力**：Issue #28 的 Executor、Reviewer（R1／R2／Alternate）、Orchestrator 以本紀錄為 #28 的 lane、boundary、HOW 採納與 assurance 要求的依據，不得重開。Spec v1.1 與 Outcome Contract 文字**不變**。本紀錄不修改任何實作、測試、資料或 `doc/acceptance/`。
- **HOW 來源標示（依核定文）**：Issue #28 §2（＝指示文件 §2）的全部細節——數值、顏色、座標、尺寸、面板內容、底圖來源——在本指示之前**都不是 acceptor 裁決**，而是為 acceptor 準備的提案 HOW；acceptor 於本指示一次核定。本紀錄一律記為「**提案 HOW，經 acceptor 於本指示核定**（DA-proposed HOW, subsequently approved by the acceptor in this instruction）」，不寫成先前已有的 acceptor 裁決。指示文件其餘出現「acceptor 已決定」處，依此解讀。先前兩份草稿（《Dashboard 視覺方向（草稿）》、《補充段（Taiwan Map，#24）》）性質相同；與本指示衝突處以本指示為準（例如補充段 5.5-C 的 CARTO 底圖已被指示 §2.2 取代；5.5-D 的高度已被指示 §2.1 取代）。

---

## 0. Acceptor 核定文（2026-09-24，逐字）

```text
I reviewed `orchestrator-message-map-rework.md`.
The overall direction is correct.
Treat this as a NEW post-baseline Taiwan Map / Dashboard UI enhancement work item.
The previous HW01 scope, Spec, Tickets and implementation are already complete; do not reopen them.
I approve the proposed map-rework direction in this document, including:
- map-first presentation;
- full-width dark Taiwan map;
- vendored vector basemap with zero runtime external requests;
- temperature pill markers;
- floating information panel;
- Select Date integrated into the map UI;
- floating legend;
- marker interaction updating the selected-region information;
- responsive/mobile adaptation;
- preservation of the existing data/API/SQLite/Flask/Vercel architecture;
- no change to the Grading App or existing MVM behaviour.
One governance wording correction:
Some of the detailed HOW choices in this draft were produced before I explicitly ruled on them.
Record them as:
"DA-proposed HOW, subsequently approved by the acceptor in this instruction"
rather than implying that every detailed value/color/coordinate was already an earlier acceptor ruling.
This instruction now ratifies those proposed HOW choices for this enhancement.
Do not modify the existing Spec or Outcome Contract.
Proceed with this as a new enhancement work item under the governance lane already described in the document.
Create/confirm the corresponding GitHub Issue and derive the work item/ticket boundary as needed.
Do not start unrelated redesign work.
Do not merge to main.
```

寫入者：Design Authority，依派工內容與指示文件 §0.0 逐字轉錄（DA 已比對兩處原文一致）。接受與授權的效力來自 acceptor 原文，不來自本轉錄。核定文的授權範圍**只及本 work item**（Taiwan Map 卡的重做）；它沒有擴張、也沒有縮減既有 Outcome Contract 的任何條款。

---

## 1. 問題

Orchestrator 派工要求 DA 對 Issue #28 一次裁決：(1) lane（Lightweight／Formal）；(2) boundary determination（是否留在既有 Outcome Contract／Spec 邊界內、只是 R-EN-4～R-EN-7 之下的 HOW）；(3) 依 §3.6-A 逐條核對 Issue #28 §2 的提案 HOW 不牴觸 accepted 語義並採納或修改；(4) 確認預設的 vendored 向量底圖在 R-EN-6 與 AC-04(b) 之內、不需改靜態檢查白名單、不觸發指示 §3 的裁決；(5) 是否需要對已 phase-accepted 的 Spec 補做 Spec Integration Audit；(6) 逐字記錄核定文與 HOW 來源標示。

---

## 2. 事實（依原始證據；Orchestrator、Executor 與 Reviewer 的敘述都當作待驗證主張）

| # | 事實 | 證據 |
| --- | --- | --- |
| E-1 | 目前 HEAD `d23de58`＝`origin/home_work_01-hw10-implementation`；`git diff --name-only 720c0a0 HEAD` 只有 `doc/governance/audit/spec-SPEC-c1-r1.md`、`doc/governance/decisions/phase-acceptance-SPEC.md`、`doc/governance/run/run-20260924-hw01-formal.md`（record-only，Bindings §7）；工作樹 clean。**受 phase acceptance 的 subject 仍是 `720c0a0`**；#18–#25 全部 CLOSED；PR #27 OPEN；`origin/main` 未變。 | DA `git rev-parse HEAD`、`git diff`、`git status`；phase-acceptance-SPEC.md §1、§10 |
| E-2 | Issue #28 body 與指示文件 `orchestrator-message-map-rework.md` §1（不變邊界）、§2（2.1～2.9）、§3（OSM 替代）、§4（DoD）逐項一致；指示 §5 的「#18 R2 N-1 另開 Lightweight work item」不在 #28 內（獨立 work item，本紀錄不涵蓋）。Issue 標示 `ready-for-agent`，Blocked by #24、#25。 | `gh issue view 28`；指示文件全文 |
| E-3 | 核定文（本紀錄第 0 節）與指示文件 §0.0 逐字相同。核定文列舉的十一項方向與指示 §2 的內容對應；核定文另明示：不改 Spec／OC、不重開 #18–#25、不做無關重設計、不合併。 | 派工內容；指示文件 §0.0 |
| E-4 | 目前地圖實作（`720c0a0`）：專案自繪台灣輪廓 GeoJSON 向量層（`static/app.js:82-99`）＋六個 `L.circleMarker`（`:461-467`）＋側欄資訊卡；代表點 `REGION_POINTS`（`:56-63`：北部 `[25.03, 121.50]`、東北部 `[24.72, 121.74]`）；`BAND_COLOURS`（`:70-75`：`#2b6cb0`／`#2f9e44`／`#f2b705`／`#e03131`）；著色直接用 endpoint 的 `colourBand`（`:392-393`），數值以 `oneDp`（`toFixed(1)`）顯示（`:560-563`）——前端不重算；tooltip／popup 就地更新（`:401-410`，#24 F-1 修正）；`mapReqSeq` 丟棄亂序回應（`:103, 337, 342, 365`，#24 F-3 修正）。`Select Date` 目前在 controls card（`static/index.html:70-76`），地圖卡在 `:139-190`，圖例與導出註記在 `:176-187`。深色 scheme 變數在 `styles.css:41-64`（含 `--map-sea`）。 | DA 讀檔 |
| E-5 | 靜態檢查（`tests/test_static_checks.py`）：`_ALLOWED_FRONTEND_URLS = {"http://www.w3.org/2000/svg"}`（`:78`，只允許「已知的非請求常數」）；`_static_files()` 只列 `static/` 頂層檔（`:194-195`，即 #24 F-4 指出的不遞迴）；`test_frontend_has_no_cwa_url_or_key`（`:198-202`）；`test_frontend_makes_no_external_absolute_url_requests`（`:205-211`）；`test_frontend_requests_use_the_api_prefix` 要求 `app.js` 內 `fetch`／`fetchJson` 的字面目標都以 `/api/` 開頭（`:214-221`）。`tests/test_dashboard.py:67` 斷言頁面含 `>Select Date</label>`（#24 R2 新增）。 | DA 讀檔；#24 R1 F-4、R2 §4 |
| E-6 | 參考樣稿 `map-mock/index.html`：藥丸 `L.marker`＋`L.divIcon`（`:197-206`）；藥丸內文與 class 直接取 `v.derivedMapTemperature`、`v.colourBand`（`:224-225`），`fmt` 只是 `Number(x).toFixed(1)` 顯示格式（`:210`）；面板含 `<label for="date">Select Date</label>`（`:117`）、`Forecast Day:`、來源句 `Source: CWA F-D0047-091 → project six-region derivation`（`:121`）、兩張 tile 對六筆取 max／min（`:216-219`）、所選 Region 區塊含 `(derived, not an observed daily mean)`（`:126-133`）；圖例四段＋ R-EN-5 原句（`:138-145`）；色帶 token `#2b6cb0`／`#2f855a`／`#d69e2e`／`#c53030`（`:19`，與目前 `BAND_COLOURS` 不同）；代表點北部 `[25.12, 121.38]`、東北部 `[24.66, 121.80]`（`:155-160`）。**樣稿有三處不得原樣帶進 repo**：預設向量底圖以 `fetch("context.geojson")`／`fetch("counties.geojson")` 載入（`:183-190`），且保留 `?base=osm`／`?base=carto` 的外部 tile URL 程式路徑（`:174-177`）；示範用 `counties.geojson` 9.3 MB、`ne50.geojson` 3.0 MB 未簡化。`days.js` 的資料形狀＝`/api/days/<date>` 回應形狀。 | DA 讀檔；`ls -la map-mock/` |
| E-7 | Spec v1.1 把下列項目明列為 HOW：`Select Date` 與地圖的 CSS 作法、Leaflet 與底圖 CDN 或 vendored、六個 Region 代表點座標（§4.2；DR-1）；R-EN-2「視覺框架不限」；R-EN-6「底圖與 Leaflet 的取得方式屬 HOW，但 MUST NOT 需要金鑰、帳號或付費」；R-EN-1(3) 的摘要資訊例示含「所選日期六區概況」；Spec §8 Out of Scope 列出 Part B 的測站觀測、heatmap、圖層切換、離島呈現等。DR-19 §6 已規定 `/api/days*` 適用 per-Region（inline）狀態規則。 | Spec §1.7、§4.2、§8；DR-1、DR-19 |
| E-8 | Bindings §4：第 2 列「文件與不改變交付行為的修正」、第 3 列「已結案工作之後的單點修正：Lightweight，作為新的 work item；需要 acceptor 的直接指示作為其 Outcome Contract」；「模糊或有爭議的分類由 DA 判定」。Bindings §5／decision A-4：結案後的 Lightweight 修正若觸及 H-1～H-3 的「觸及的工作」MUST 執行 independent audit。phase-acceptance-SPEC.md §10：`720c0a0` 之後對 `home_work_01/` 的任何變更都不在該 phase acceptance 的 coverage 內，依 Bindings §4 以 acceptor 直接指示開新的 Lightweight work item。治理 §4.7 末段：Lightweight 無 Spec、不適用 Spec Integration Audit；assurance policy MAY 要求等效的 outcome-level audit。治理 §3.8：審後變更需要相應驗證，可能影響原 review 結論者由 Reviewer／DA 判定必要後續。 | Bindings §4、§5；decision A-4；phase-acceptance §10；治理 §3.8、§4.7 |
| E-9 | 已閉合但與本 work item 直接相關的 #24 findings：F-1（切換日期後開著的資訊卡須更新，已修）、F-3（亂序回應守衛，已修）、F-4（靜態檢查不遞迴 `static/vendor/`，Low，disposition 為遞迴＋對 vendored Leaflet attribution URL 加明確 allowlist）、F-5(a)／R2 N-1（地圖邊緣 tooltip／popup 被容器裁切，Low，未修）。 | #24 R1 §4、R2 §2–§3、§6 |
| E-10 | 視覺判準 V-1～V-5 的定義在《視覺方向（草稿）》§6（V-1 可讀文字 ≥ 12 px、內文 ≥ 16 px；V-2 文字對比 ≥ 4.5:1、標記對底 ≥ 3:1；V-3 tooltip 不裁切；V-4 可點區 ≥ 44×44；V-5 淺深色各一組截圖），補充段 5.5-E 給出地圖卡的對應（藥丸數值 14 px、Region 標籤 12 px、圖例 12 px，皆固定 px；黃色帶用深字；六個標記 375 px 下 tooltip 不裁切）。草稿 §6 自述 V-1～V-5「是 R-EN-1 既有條款的量化」。 | 兩份草稿（acceptor 核定為「提案 HOW，經本指示核定」） |
| E-11 | README `:252-282` 目前的 Taiwan Map 段落記載：vendored Leaflet 1.9.4、專案自繪簡化輪廓、無外部 tile server、代表點為 project-defined、Derived Map Temperature 為導出值且在共用模組算一次。 | DA 讀檔 |

---

## 3. 裁決

### 3.1 DR-20.1 — Lane：**Lightweight**（新的 work item；必做 independent audit）

**裁決**：Issue #28 是 Bindings §4 第 3 列的 post-closure work item，lane 為 **Lightweight**，以 acceptor 2026-09-24 的直接指示（第 0 節核定文＋其核定的指示文件 §1–§4，即 Issue #28）作為本 work item 的 Outcome Contract。依 decision A-4，因觸及 H-2（頁面文字 `Select Date`、`Date`／`Min`／`Max`、六個 Region 中文名）與 H-3（Derived Map Temperature 的顯示與導出標示）的「觸及的工作」，**independent audit 必做**：fresh `gov-primary-reviewer` R1，其後依治理 §4.4 同一套 R2／一次 Alternate／Final Adjudication 流程；R1 record 依 A-1 明記 H-2／H-3 核對段。worklog 的 Audit status MUST 寫「required（A-4）」，不得寫「依 policy 未要求」。

**依據（治理 §3.3、§3.6）**：

1. **§3.3 eligibility 成立。** Executor 不需對 intent、scope、acceptance、authority 作任何假設：intent 與 scope 由核定文與 Issue #28 §2／§2.9 給定；acceptance 由 Issue #28 §4（AC-17／18／19 重驗、V-1～V-5、H-3 逐日對照、零外部請求、測試與 CI、README、ACCEPTANCE.md）給定；authority 由核定文給定。剩餘的語義缺口（例如「資訊卡」在無 popup 設計下的滿足方式、`Select Date` 在 inline 狀態下的可用性、來源句措辭、V-1 對地圖卡的適用）由本紀錄 3.3／3.6 節裁決，不留給 Executor 假設。
2. **不是 §3.6-B。** 本工作引入的行為都有 accepted baseline 可錨定（R-EN-1～R-EN-7、AB-14、AB-15），且沒有其他工作將依賴它（#18–#25 已結案，沒有進行中的工作）；所需裁決不改變 accepted 語義（第 4 節）；Spec 沒有把必要設計留待下游——地圖的視覺與座標是 Spec §4.2 **刻意**交給實作的 HOW（DR-1），不是未完成的設計。
3. **不是 §3.6-C。** 一張票、一個 Executor、一個 Reviewer 流程、同一 branch；沒有多 execution units 或 dependency 管理需求。工作篇幅（新增底圖資料檔、改寫地圖卡）不是需要 Spec 的判準（§3.6-B 末句）。
4. **§3.3 末段的排除不適用。** 結果不改變 accepted 語義；不改變其他工作所依賴的設計基線——`/api/` 形狀、共用模組、Grading App、`data.db`、INV-1～INV-9、gates 全部不動；`Select Date` 的 `<label>` 與七日語義不變（`tests/test_dashboard.py:67` 仍成立）。
5. **不得拆成多個 Lightweight 以規避 Formal**（§3.3）：本 work item 的整體結果就是一張地圖卡的呈現；核定文明禁無關重設計（masthead、controls、Weekly summary、折線圖、表格不動），所以不存在「更大的整體工作被切碎」的情況。若日後 acceptor 要求重做其餘區塊，那是另一個 work item，屆時由 DA 依預期整體結果重新判定 lane。

**若下列任一情況出現，本裁決失效、路徑停止並 route DA 重判（可能 promote 至 Formal 或 fail-closed 至 acceptor）**：需要改動 `/api/` 回應形狀、`weather_query.py`、`app.py`、`data.db`、ingestion、`requirements.txt`、`vercel.json`、`.python-version` 或 `.github/workflows/`；需要新增 AC／INV 或改變既有 AC 的 PASS／FAIL 語義；需要外部請求（tile／CDN／字型）；需要第二個 execution unit。

**紀錄命名（Bindings §7；DA 對本 work item 的具體化）**：worklog `doc/governance/worklog/20260924-taiwan-map-rework.md`（Lightweight 命名）；audit `doc/governance/audit/issue-28-c<cycle>-<r1|r2|alt>.md`（本 work item 有 GitHub Issue，沿用 Ticket 命名以維持可追溯）；`doc/ticket/tickets.md` 加一列 #28（scope class 標「POST-BASELINE ENHANCEMENT（Lightweight work item）」；High-risk H-2、H-3；Blocked by #24、#25）。派工機制依 Bindings §3.3／§3.5：Executor 為 `gov-executor` subagent（或主 session 在 binding 符合 `executor` mapping 時直接執行——擇一並記錄 binding）；Reviewer 一律以 Agent tool 派 fresh `gov-primary-reviewer`，bounded pack 只放路徑與識別（本紀錄、Issue #28、Spec、worklog、subject SHA），不放 Executor 結論。

### 3.2 DR-20.2 — Boundary determination（治理 §1.2、§3.6-A）

**總判定：Issue #28 的全部工作項目都在既有 Outcome Contract（§2.2 ENHANCED REQUIRED、§2.4、AB-13～AB-15）與 Spec v1.1 的 boundary 內，是 R-EN-1～R-EN-7、R-SHR-4、INV-2／INV-7／INV-9、AC-04(b) 之下的 HOW；不新增 requirement、AC、invariant 或 gate；不改變任何 accepted 語義；不改 Spec、不改 Outcome Contract；不動 `/api/`、MVM 行為與 Grading App。** 逐項如下（只列需要判斷者）。

| # | 項目（Issue #28 §2） | 判定 | 依據 |
| --- | --- | --- | --- |
| B-1 | 2.1 map-first、整寬、兩種 color scheme 下地圖區皆深色、高度 560／440／360 px | 在 boundary 內：視覺框架與 CSS 屬 HOW。 | R-EN-1(1)(2)；R-EN-2「視覺框架不限」；Spec §4.2「CSS 作法」；DR-1 |
| B-2 | 2.2 vendored 向量底圖：Natural Earth `ne_50m_admin_0_countries`（public domain）周邊海岸線＋內政部「直轄市、縣市界線」開放資料（政府資料開放授權條款）縣市多邊形，簡化 ≤ 300 KB | 在 boundary 內：底圖取得方式屬 HOW；兩個來源皆不需金鑰、帳號或付費；授權條款的**標示義務**（attribution）不是金鑰、帳號或付費，寫入 README 即可。縣市多邊形只是底圖線條（`interactive: false`），不是圖層切換、不是縣市層級的資料呈現，不觸及 OC §2.2 REFERENCE「老師 repo 的 22 縣市／GIS 架構」與 Spec §8。**條件**：見 3.3 P-2。 | R-EN-6；Spec §4.2「Leaflet ... CDN 或 vendored」；OC §4 RB-3／RB-4 未觸及；Spec §8 |
| B-3 | 2.2 資料以 `static/data/*.js` 全域變數（或 inline）載入、不用 `fetch` | 在 boundary 內：同源 `<script>` 載入不是資料請求；瀏覽器端資料請求仍只指向 `/api/`；執行期零外部請求。 | R-SHR-5；R-DS-5；AC-04(b)；INV-1；INV-6 |
| B-4 | 2.2 新增靜態子目錄納入 CWA URL／金鑰掃描（順修 #24 F-4） | 在 boundary 內：屬 R-TC-1 靜態檢查的 HOW，且只**加強**不弱化；#24 F-4 的 disposition 已把它交給 Executor／後續票。 | R-TC-1；AC-04(b)；#24 R1 F-4 |
| B-5 | 2.3 藥丸標記：內文＝endpoint `derivedMapTemperature`、底色＝endpoint `colourBand`、白描邊、a11y、可點區 ≥ 44×44、Region 全名標籤（zoom < 8 隱藏） | 在 boundary 內：R-EN-4 只要求「六個 Region 各一個標記，顏色依色帶」；標記形式（circle 或 divIcon）屬 HOW；在標記上顯示導出值是對 endpoint 值的顯示，不是重算；Region 名逐字。 | R-EN-4；R-SHR-4／H-3（不重算）；R-EN-2／H-2；DR-1 |
| B-6 | 2.3 代表點微調：北部 `[25.12, 121.38]`、東北部 `[24.66, 121.80]`，其餘不變；375 px 初始視野六顆不得重疊 | 在 boundary 內：R-EN-4「位置為專案定義的代表點（座標屬 HOW，README 標示為專案定義）」。記為**專案定義 HOW**（3.3 P-5）。 | R-EN-4；Spec §4.2；DR-1；README 標示義務 |
| B-7 | 2.4 hover tooltip：Region、Date、Min、Max、Derived（一位小數）＋「(derived)」；不被裁切 | 在 boundary 內：R-EN-4「點擊或 hover 顯示資訊卡」的 hover 路徑；不裁切是 R-EN-1(2)(4) 的量化（V-3），並解決 #24 R2 N-1。 | R-EN-4；AC-17；INV-7；#24 R2 N-1 |
| B-8 | 2.5 `Select Date` 移入地圖卡的浮動面板（controls card 保留 `Select Region` 與 ingestion 時間） | 在 boundary 內：R-EN-3 只規定控制項的內容（七日升序、預設第一天、切換地圖）與標籤文字，不規定位置；R-EN-7 要求同一頁面整合，仍成立；H-2 的 `Select Date` 標籤逐字保留；R-DS-4／R-DS-7 的 `Select Region` 與 ingestion 時間不動。**條件**：見 3.3 P-7。 | R-EN-3；R-EN-7；H-2／INV-4；R-DS-4；R-DS-7 |
| B-9 | 2.5 當日兩張摘要 tile（Highest MaxT／Lowest MinT＋Region 名）：對六筆 endpoint 值取 max／min | 在 boundary 內：R-EN-1(3) 明文例示「所選日期六區概況」；對已回傳的六個數值取極值不是 Region／Forecast Day 推導邏輯（R-SHR-1），與 #23 Weekly summary 同一性質（Spec Integration Audit INV-1 列已認定）。 | R-EN-1(3)；R-SHR-1；INV-1；#23 先例 |
| B-10 | 2.5 所選 Region 區塊（Region、Date、Min、Max、Derived map temperature、「(derived, not an observed daily mean)」；點藥丸更新；預設北部地區） | 在 boundary 內：這就是 R-EN-4「點擊…顯示資訊卡」與 AC-17「點擊標記顯示 Region、Date、Min、Max 與導出平均」的實現；預設 Region 屬 HOW。 | R-EN-4；AC-17；INV-7 |
| B-11 | 2.5 標題＋`DERIVED` chip、`Forecast Day: <date>`、來源句 | 在 boundary 內：屬 UI 文案 HOW；來源句與 chip 有助於 INV-7／AB-13 的標示要求。**條件**：見 3.3 P-8。 | R-EN-1(1)；INV-7；AB-13；R-DOC-2 |
| B-12 | 2.6 右下浮動圖例：四段色帶＋ R-EN-5 原句；不用連續漸層 | 在 boundary 內：R-EN-5 逐字滿足；位置屬 HOW。 | R-EN-5；AC-17 |
| B-13 | 2.7 切換 `Select Date` 只更新藥丸／tooltip／面板，不重設視野 | 在 boundary 內：AC-18 的 HOW；「不重設視野」不與任何條款衝突。 | AC-18；R-EN-4「可縮放」 |
| B-14 | 2.8 初始化強化（容器尺寸非 0 才初始化；`invalidateSize()` 後 `fitBounds`）＋已知 hazard 的回歸測試 | 在 boundary 內：程式品質與測試方法屬 HOW；回歸測試的形式（jsdom／headless／pytest 驅動）屬 HOW，但證據必須可由 Reviewer 重現。 | R-DOC-5；R-TC-1；impl-default |
| B-15 | 2.9 不做清單；masthead／controls／Weekly summary／折線圖／表格不動；不動 Grading App、MVM、`/api/` | 與 Spec §8、OC §2.2 REFERENCE／OPTIONAL、核定文「Do not start unrelated redesign work」一致。 | Spec §8；OC §2.2；核定文 |
| B-16 | §4 DoD：AC-17／18／19 重驗、V-1～V-5、H-3 逐日對照、零外部請求、測試＋CI、README、ACCEPTANCE.md、tickets.md、worklog、R1 audit | 在 boundary 內：AC-17／18／19 依 Spec 原文重驗（不重定義）；V-1～V-5 是**本 work item 的驗收判準**（acceptor 核定），對 Spec AC 是**附加**、不是替代（3.6 節）；README／ACCEPTANCE.md 更新是 R-DOC-1／R-DOC-2／R-DOC-4 的既有義務。 | Spec §2；R-DOC-1／2／4；治理 §3.1(3) |

**明確在 boundary 之外、本 work item 不得執行的事項**（出現時 Executor 停止該路徑並 route DA；DA 無法確立在 boundary 內時 fail-closed 至 acceptor）：

| # | 事項 | 為何在外 | 所需 authority |
| --- | --- | --- | --- |
| X-1 | OSM／CARTO／Esri 或任何外部 tile、CDN、字型、source map 等**執行期外部請求** | 核定文核定的是「vendored vector basemap with zero runtime external requests」；改用外部請求就改變了本 work item 的 accepted constraint；同時牽動 AC-04(b) 靜態檢查的解讀（指示 §3）。 | 先 DA（獨立 decision record，見 3.4）；DA 會把「與核定文相反」的部分 route 至 acceptor 重新指示 |
| X-2 | 改動 `/api/` 回應形狀、`server.py`／`api/index.py` 的路由語義、`weather_query.py`、`app.py`、`data.db`、`ingestion/`、`data/`、`requirements.txt`、`vercel.json`、`.python-version` | INV-1／INV-2／INV-9、H-2／H-3；核定文「preservation of the existing data/API/SQLite/Flask/Vercel architecture; no change to the Grading App or existing MVM behaviour」。 | DA（重判 lane／boundary；很可能 promote 或 route acceptor） |
| X-3 | 重做 masthead、controls card（除移出 `Select Date` 之外）、Weekly summary、折線圖、表格 | 核定文「Do not start unrelated redesign work」；指示 §2 末項。 | acceptor（新 work item） |
| X-4 | 新增資料功能（多測站／觀測、雨量／雷達／颱風／濕度、特報、圖層切換、定位、重新整理鈕、連續漸層、手動深淺切換、離島呈現） | Spec §8；OC §2.2 REFERENCE／OPTIONAL；指示 §2.9。 | acceptor（新 Outcome Contract） |
| X-5 | 修改 Spec v1.1、Outcome Contract、derivation record、Bindings | 核定文明禁；治理 §5.3。 | acceptor |
| X-6 | 修改 `.github/workflows/` | 指示「RB-5：只動單元內檔案（`.github/workflows/` 不動）」。 | acceptor（OC §8.2 的有範圍授權只涵蓋維護本單元 workflow；本票不需要） |
| X-7 | 合併進 `main`、繳交、建立／修改 Vercel 設定或 repository variable | RB-1、RB-2、RB-3。 | acceptor |
| X-8 | 取得底圖資料若需要**註冊帳號**或**付費** | R-EN-6；RB-3「第三方帳號操作」、RB-4。 | acceptor（停止該路徑並 stop report；改用不需帳號的來源或由 acceptor 指示） |

**Boundary 疑義的處理**：Reviewer 若對上述任一項提出 boundary 符合性 finding，依治理 §1.2 先由 DA 評估；DA determination 後仍有爭議者視為 DA 無法確立，受影響路徑 fail-closed 至 acceptor。

### 3.3 DR-20.3 — §3.6-A 對提案 HOW 的逐條採納

每條標示：來源＝「提案 HOW，經 acceptor 於本指示核定」；DA 核對其不牴觸 accepted 語義後**採納**，必要處附 DA 條件（條件只是把既有 accepted 條款在該 HOW 上的具體含義寫明，不新增需求）。沒有任何一條需要以契約推翻；有兩處**樣稿與核定判準衝突**（P-1 的高度、P-12 的 V-1 字級）依「指示文件優先於草稿、判準優先於樣稿」取捨並註明。

| # | 提案 HOW | 核對的 accepted 條款 | 裁決 |
| --- | --- | --- | --- |
| P-1 | 版面：整寬、地圖區固定深色（頁面其餘照系統深淺色）、高度桌機 560／平板 440／375 px 360 px；卡標題 `Taiwan Map`＋當前 Forecast Day | R-EN-1(1)(2)(6)、R-EN-2 | **採納。** 補充段 5.5-D 的 480／420／320 被指示 §2.1 取代（指示優先）。深色地圖區在淺色頁面上仍須符合 R-EN-1(1) 各區可辨（V-5 兩組截圖驗證）。 |
| P-2 | 底圖：Natural Earth `ne_50m_admin_0_countries`（保留 CHN／TWN／PHL／JPN／VNM／HKG／MAC 並依 bbox 裁切）＋內政部「直轄市、縣市界線」；簡化 ≤ 300 KB；海 `#0f1927`、周邊陸 `#1a2331`／邊 `#2b3648`、台灣陸 `#25324a`／縣界 `#44577a` 0.9 px | R-EN-6、R-SEC-1、AC-04(b)、INV-5、INV-7、Spec §8 | **採納，附條件**：(a) README 記載兩個資料集的名稱、來源、授權（Natural Earth public domain；內政部資料依政府資料開放授權條款附 attribution）、取得日期與簡化方式；worklog 記載取得過程**不需帳號、不付費**（X-8）。(b) 交付的 `static/data/*` **不得含任何絕對 URL、金鑰或 `opendata.cwa.gov.tw` 字串**（attribution 的**文字**可以放在地圖 attribution control 或資料檔；超連結只放 README）——如此 B-4 的遞迴掃描對新目錄直接成立，且不需動白名單。(c) 樣稿的 9.3 MB／3.0 MB 示範檔**不得直接 vendored**；簡化後的幾何只作 backdrop（`interactive: false`），不承載任何縣市層級的資料語義，README 不得把它描述成資料圖層。(d) 樣稿的 `?base=osm`／`?base=carto` 程式路徑與其 tile URL **不得帶進 repo**（會使 `test_frontend_makes_no_external_absolute_url_requests` 失敗，且與核定文相反）。 |
| P-3 | 載入：`static/data/*.js` 全域變數（或 inline），不用 `fetch`；新增靜態子目錄納入 CWA URL／金鑰掃描（遞迴，順修 #24 F-4） | R-SHR-5、AC-04(b)、R-TC-1 | **採納。** 靜態檢查的改法屬 HOW，但：只能加強、不能弱化既有三個前端檢查；`test_frontend_requests_use_the_api_prefix` 與 `test_frontend_has_no_cwa_url_or_key` 的斷言語義不變。若把絕對 URL 檢查也改為遞迴而掃到 `static/vendor/leaflet.*` 內既有的非請求常數（`https://leafletjs.com` 等，#24 R1 已核對不是請求），MAY 依 #24 F-4 的 disposition 把該**精確字串**加入 `_ALLOWED_FRONTEND_URLS`——這與既有 `http://www.w3.org/2000/svg` 同類（已知非請求常數），不是請求目標，不改變 AC-04(b) 語義（見 3.4）。**任何請求目標（tile／CDN）都不得加入白名單。** |
| P-4 | 藥丸標記：`L.marker`＋`L.divIcon`；內文 `27.2°`（一位小數＝endpoint `derivedMapTemperature`，不另捨入）；14 px／600／`tabular-nums`；底色＝該日色帶 token（藍 `#2b6cb0`／綠 `#2f855a`／黃 `#d69e2e`／紅 `#c53030`，圖例同一組）；白 2 px 描邊＋陰影；黃色帶深字 `#1a2230`、其餘白字；hover／focus／選取放大 1.08、描邊改 accent；`tabindex="0"`、`role="button"`、`aria-label` 含 Region、Date、Min、Max、derived；可點區 ≥ 44×44；下方 Region **全名**標籤 12 px，zoom < 8 隱藏 | R-EN-4、R-EN-5、R-SHR-4／H-3、DR-4、R-EN-2／H-2、AC-28（前端側） | **採納，附條件**：(a) 內文與底色 MUST 直接取自 `/api/days/<date>` 的 `derivedMapTemperature` 與 `colourBand`；前端不得出現 `(mint + maxt) / 2`、20／25／30 門檻或任何分帶邏輯；`toFixed(1)` 只是對已為一位小數的值做顯示格式（與 #24 `oneDp` 同性質），不是捨入邏輯。(b) 色帶 token 的 hex 屬 HOW，可與目前 `BAND_COLOURS` 不同，但四個 token MUST 仍可辨識為 R-SHR-4 命名的藍／綠／黃／紅四色家族（README 與圖例文字沿用這四個名字），且藥丸、圖例 swatch、README 描述使用**同一組**值（R-EN-5、AC-17「標記顏色等於色帶」以 swatch 對照）。(c) Region 標籤與 `aria-label` 的 Region 名逐字（H-2）。(d) 標籤在 zoom < 8 隱藏時，Region 名仍可由 tooltip、面板與 `aria-label` 取得，R-EN-4 不受影響。 |
| P-5 | 代表點：以 #24 座標為基礎，北部改 `[25.12, 121.38]`、東北部改 `[24.66, 121.80]`（其餘不變），使 375 px zoom 7 六顆不重疊；採用或另選皆可 | R-EN-4、DR-1、README 標示義務 | **採納為專案定義 HOW。** DA 澄清「代表點」的含義：每個點 MUST 落在該 Region 成員縣市的地理範圍內（否則不是該 Region 的「代表」點，且與 README「a single point standing in for each Region」矛盾）；在此前提下為避免重疊而微調屬 HOW。README MUST 維持「project-defined representative points … not a CWA-published location or boundary」的標示，並記下本次微調的座標。 |
| P-6 | tooltip（hover）：Region 全名、Date、Min、Max、Derived（一位小數）＋「(derived)」；深色 surface；`direction: "top"`；375 px 與桌機六個標記皆不得被卡片裁切 | R-EN-4、AC-17、INV-7、R-EN-1(2)(4) | **採納。** 不裁切是 V-3 的地圖對應（5.5-E），同時關閉 #24 R2 N-1。`direction` 的具體值屬 HOW（5.5-E 允許 `auto`）；判準是結果不裁切。 |
| P-7 | 左上浮動資訊面板（375 px 改為地圖上方一列、不浮動）：標題＋`DERIVED` chip；`Select Date` 移入；`Forecast Day: <date>` | R-EN-3、R-EN-7、H-2／INV-4、DR-19、AC-18、AC-19 | **採納，附條件**：(a) `Select Date` MUST 仍是可見的 `<label>` 文字 `Select Date` 加對應的 `<select>`（`tests/test_dashboard.py:67` 的斷言維持），七個 Forecast Day 升序、預設第一天（R-EN-3）。(b) **DR-19 inline 狀態下的可用性**：目前 `setMapStatus` 會隱藏整個 `#map-layout`；`Select Date` 移入地圖卡後，MUST 保證在 `/api/days` 成功、但 `/api/days/<date>` 回 404／503／5xx／網路失敗或 2xx 空值（inline error／empty）時，`Select Date` **仍可見且可操作**，使用者可以切到另一天恢復（#24 R1 驗證過的「切到 503 日期 → inline error → 切回正常日期 → 恢復」行為 MUST 保留）；`/api/days` 本身失敗或為空時，卡片顯示 inline error／empty、控制項可隱藏或停用（沒有可列的日期）。(c) 面板不得遮住任何藥丸的初始位置（R-EN-4「初始視野涵蓋六個標記」以可見為準）。 |
| P-8 | 面板來源句 `Source: CWA F-D0047-091 → project six-region derivation`；`DERIVED` chip | INV-7、AB-13、R-DOC-2、AC-14(8) | **採納，附措辭條件**：句子 MUST 讓讀者知道六區值是**專案推導**的相容性值，MUST NOT 讀成 CWA 發布六區預報。樣稿句可用；SHOULD 更明確，例如 `Source: CWA F-D0047-091 (county-level) → project-derived six-region values`。措辭細節屬 HOW，Reviewer 依 AC-14(8)「沒有任何地方把區域值寫成 CWA 發布」核對頁面文字。 |
| P-9 | 當日兩張摘要 tile：`Highest MaxT (this day)`／`Lowest MinT (this day)`＋該 Region 名；前端對六筆 endpoint 取 max／min | R-EN-1(3)、R-SHR-1、INV-1 | **採納。** 只允許對 `/api/days/<date>` 回傳的六筆值取極值與對應 Region 名；不得引入任何其他計算。 |
| P-10 | 所選 Region 區塊：Region、Date、Min、Max、`Derived map temperature`、`(derived, not an observed daily mean)`；點藥丸更新；預設北部地區 | R-EN-4、AC-17、AC-18、INV-7、H-2 | **採納，附條件**：(a) 切換 `Select Date` 時，此區塊、所有藥丸與任何開著的 tooltip MUST 同步更新為新日期的值（#24 F-1 確立的「資訊卡不得留舊值」原則，AC-18）；所選 Region 在切換日期後 MAY 保留（改善 #24 F-5(b)）或重設，屬 HOW。(b) `Min`／`Max` 的顯示格式（`31` 或 `31.0`）屬 HOW，但值 MUST 等於 endpoint 值；SHOULD 與頁面表格的格式一致以免同頁兩種寫法。(c) 文字 `Date`、`Min`、`Max` 逐字（Spec §4.1「資訊卡 `Min`／`Max`」）。 |
| P-11 | 右下浮動圖例：四段色帶＋ R-EN-5 原句「Average = (MinT + MaxT) / 2, a derived value — not an observed daily mean.」；不用連續漸層；右上只有 Leaflet 縮放控制 | R-EN-5、AC-17 | **採納。** 圖例 swatch 與藥丸用同一組 token（P-4(b)）。 |
| P-12 | 切換 `Select Date` 不重設視野；初始化強化（`ResizeObserver`／`visibilitychange`；`invalidateSize()` 後 `fitBounds`）；hazard「`Invalid LatLng (NaN, NaN)`／0×0 標記」加回歸測試 | AC-18、R-DOC-5、R-TC-1 | **採納。** #24 F-3 的亂序守衛（`mapReqSeq` 或等效）MUST 保留（否則重開已閉合的 AC-18 缺陷）。回歸測試的形式屬 HOW，但 MUST 可由 Reviewer 在自己的環境重現（例如 headless 腳本或 pytest 驅動的檢查），且不得只靠截圖。 |
| P-13 | V-1～V-5 作為本 work item 的驗收判準 | R-EN-1(1)(2)(4)(6)、AC-19 | **採納，並澄清 V-1 對地圖卡的適用**（草稿 §6 的「內文 ≥ 16 px」與樣稿 12–14 px 的面板／藥丸字級有張力）：依 acceptor 核定的補充段 5.5-E，地圖卡內的判準為——所有可讀文字 ≥ 12 px 固定 px（藥丸數值 14 px、Region 標籤 12 px、圖例 12 px、面板 meta ≥ 12 px、tooltip ≥ 12 px）；「內文 ≥ 16 px」適用於頁面其餘區塊的段落文字（本 work item 不動，#23／#25 已驗），**不**適用於地圖卡內的任何元素。V-2：藥丸內文對藥丸底 ≥ 4.5:1（黃色帶靠深字）、四段色帶對底圖 ≥ 3:1，以 token 值計算記 worklog。V-3：六個標記的 tooltip 在 375 與桌機皆完整可見。V-4：可點區 ≥ 44×44。V-5：淺色與深色各一組截圖（桌機、375，含 hover 一個標記）。 |

**其他 HOW 觀察（不設條件，供 Executor 參考）**：樣稿把 `#map` 標為 `role="img"`；`role="img"` 會讓子元素對輔助科技呈現為 presentational，與「藥丸可 Tab、有 `aria-label`」的核定意圖相反——SHOULD 改用能容納互動子元素的 ARIA 作法（例如 `role="region"`＋`aria-label`）。屬 HOW，由 Executor 決定，Reviewer 只核對核定的 a11y 項目（可 Tab、`aria-label`）是否實際可達。

### 3.4 DR-20.4 — AC-04(b) 與底圖：預設方案不需白名單變更、不觸發指示 §3 的裁決

**裁決**：Issue #28 §2.2 的 vendored 向量底圖（`static/data/*.js` 同源 `<script>` 載入、執行期零外部請求）**完全在 R-EN-6 與 AC-04(b) 之內**：

1. AC-04(b) 的兩個可觀察條件——「前端 JS／靜態資源不含 `opendata.cwa.gov.tw` 或 `CWA_API_KEY`」與「其資料請求只指向本應用程式的 `/api/` 路徑」——在此方案下都直接成立；R-SHR-5「瀏覽器端 JS 的資料請求只得指向 `/api/`」亦成立；INV-6 不變。
2. `_ALLOWED_FRONTEND_URLS` **不需要**因底圖而變更：本方案沒有任何請求目標需要放行。白名單的性質維持「已知的**非請求**常數」；P-3 允許的唯一變動（若 Executor 把絕對 URL 檢查改為遞迴）是為 vendored Leaflet 內既有的非請求 attribution 常數加精確字串，那是測試 HOW，不是 AC-04(b) 語義的改變，也不是本節所稱的白名單變更。
3. 指示 §3 的裁決（AC-04(b) 是否只針對天氣資料請求而不含底圖圖磚）**本次不作出、也不需要**。acceptor 在指示 §3 對其原意的說明**已記錄在案**，但依 §3 自己的措辭「是否在 accepted 語義內仍由 DA 判定」，那是留待觸發時才作的 determination。
4. **OSM 圖磚替代方案不在本 work item 範圍內。** 若 Executor 或 Reviewer 日後主張需要它（例如認為向量底圖不足），那是**另一次獨立的 DA 裁決**（獨立 decision record），不得在 #28 內自行採用。DA 預先說明其路徑：因核定文核定的是「zero runtime external requests」，改用外部圖磚會改變本 work item 的 accepted constraint（X-1），DA 在該次裁決中會把此部分 route 至 acceptor 重新指示（治理 §1.2），並同時判定 AC-04(b) 的解讀與 `_ALLOWED_FRONTEND_URLS` 的允許範圍；在 acceptor 指示與 DA 裁決都成立前，任何外部請求都是 AC-04(b) 的 FAIL。

### 3.5 DR-20.5 — 是否補做 Spec Integration Audit；Orchestrator 遵循的規則

**裁決**：**不另開 Spec Integration Audit instance**（不以 #28 觸發治理 §4.7）；改以下列**兩段式** assurance 取代，兩段都必要：

**(A) #28 的 A-4 independent audit（fresh Primary Reviewer R1）MUST 涵蓋 DA 指定的整合重驗範圍**，並在 record 中以獨立一節明記；這是 §4.4「R1 完整審查 accepted work scope、適用 invariants、變更風險與 acceptance evidence」在本 work item 的具體化，不是新增 audit instance、round 或角色：

1. **Diff-scope 證明**：`git diff --name-only 720c0a0..<subject>`（排除 `doc/governance/**`）MUST 只落在 `home_work_01/static/**`（含新增的 `static/data/`）、`home_work_01/tests/**`（只允許加強或新增）、`home_work_01/README.md`、`home_work_01/doc/acceptance/**`、`home_work_01/doc/ticket/tickets.md`。任何其他路徑（特別是 X-2、X-6 所列）出現即為 boundary finding → route DA。
2. **Invariants**：INV-1（瀏覽器端只呼叫 `/api/`；`static/` 內無推導與分帶邏輯）、INV-2（折線圖／表格程式未動；六區表格值仍等於共用模組——以 diff 與抽查證明）、INV-5（新增靜態資產與截圖不含金鑰；CI credential scan）、INV-6（執行期 network log 零外部請求）、INV-7（圖例註記、面板導出註記、來源句、README 標示）、INV-9（`app.py` 未動；Grading App 不受影響）。INV-3／INV-4／INV-8 記為「diff 未觸及，沿用 `spec-SPEC-c1-r1.md` 的結論」。
3. **Spec AC**：AC-04(b)（含新目錄的靜態掃描）、AC-14(6)（README 導出說明）、AC-17、AC-18、AC-19（DR-19 三種狀態；P-7(b) 的 inline 狀態可用性）、AC-20／AC-21（既有 152 測試＋新增測試、CI 綠）、AC-27（新程式碼；舊地圖卡的死 CSS／過時註解不得殘留——#24 F-2 先例）、AC-28 前端側（不重算）、AC-15（對新 subject 的 preview 部署 smoke，並證明部署 ↔ commit 對應）；AC-02／AC-03 作回歸抽查（controls card 改動後 `Select Region` 與表格不變）。
4. **Work item DoD**：V-1～V-5（依 P-13 的地圖卡適用）、H-2／H-3 核對段（A-1）、七日藥丸值／色與 endpoint 逐一對照、README 段落、ACCEPTANCE.md 的 AC-04／17／18／19 列與 §6、tickets.md 索引列、worklog。
5. **已閉合 #24 findings 的不回歸**：F-1 原則（P-10(a)）、F-3 守衛（P-12）、N-1 裁切（P-6）、F-4 遞迴（P-3）。

**(B) #28 audit closure 後，Orchestrator 自主派工 DA 產出 phase-acceptance 增補紀錄** `doc/governance/decisions/phase-acceptance-SPEC-addendum-20260924-map-rework.md`：引用已 closure 的 `spec-SPEC-c1-r1.md`（對 `720c0a0` 未受 diff 觸及的部分仍有效）與已 closure 的 #28 audit record（對受觸及部分），並以 (A)-1 的 diff-scope 證明把兩者接起來，宣告 release 候選 subject 的 phase 狀態。它**不是**新的 phase acceptance、**不是** release authorization；只是治理 §3.8「審後變更…由 Reviewer／DA 判定必要後續」的 DA 判定。Bindings §5／A-6 release gate 的「DA phase acceptance 已完成」一項，對 #28 之後的 subject 以 `phase-acceptance-SPEC.md` ＋ 本增補共同滿足。

**規則的依據與界限**：治理 §4.7 明文 Lightweight 不適用 Spec Integration Audit，且 DA 不得把既有 Ticket audit record 事後重標為 Spec Integration Audit——所以 #28 的 audit record **MUST NOT** 自稱或被引用為 Spec Integration Audit。DA 依 §4.1「有權裁決決定」與 §5.1「DA 決定 assurance 要求」，把等效的 outcome-level 整合重驗納入 A-4 必做的 audit 範圍（§4.7 末段允許），並以 (B) 維持 release gate 的可追溯。

**Fail-safe（何時仍需完整的補充 Spec Integration Audit）**：若 (A)-1 的 diff-scope 證明不成立（改到 X-2 所列檔案或其他路徑）且該變更經 DA 判定仍在 boundary 內而被接受，或 #28 的 R1／R2／Alternate 流程產生 DA 無法關閉的 boundary finding，則 (A)(B) 不足：MUST 對新 HEAD 另派一次獨立的 Spec Integration Audit instance（`doc/governance/audit/spec-SPEC-c2-r1.md`，record 內註明「supplementary instance over changed subject，依 §3.8，不是 FA 授權的 rework cycle」），closure 後才可產出 (B) 的增補。這條由 Orchestrator 依規則機械判定，不需再問 DA。

### 3.6 DR-20.6 — 本 work item 的驗收語義與既有 Spec AC 的關係

1. **AC-17／AC-18／AC-19 依 Spec v1.1 原文重驗**，PASS／FAIL 語義不變；本紀錄不重定義它們（治理 §3.1(3)、§3.4）。
2. **V-1～V-5 是本 work item 的附加驗收判準**（acceptor 核定的 Outcome Contract 內容），依 P-13 的地圖卡適用；V 的 FAIL 是本 work item 的 DoD FAIL，與 AC-19 的判定各自獨立、互不冒充。Reviewer 的 finding 引用時寫明是 Spec AC 還是 V 判準。
3. **H-3 的核對方式**：對七個 Forecast Day 各取 `/api/days/<date>`，逐一比對六個藥丸的內文與 class／底色、tooltip、面板值；並以 grep 證明 `static/**` 內沒有推導或分帶邏輯（AC-28 前端側）。
4. **DR-19 適用不變**：`/api/days` 與 `/api/days/<date>` 仍依 per-Region（inline）規則；地圖卡在三種狀態下都不得空白；P-7(b) 是 DR-19 在新版面下的可用性條件，不是新狀態規則。
5. **README（R-DOC-1／R-DOC-2）MUST 更新**：底圖來源與授權（P-2(a)）、免金鑰／帳號／付費、代表點為專案定義（含微調座標）、`Select Date` 的新位置、Derived Map Temperature 導出說明維持。README 現有 `:263-269` 對「project-authored simplified outline」的描述由新底圖的描述取代。

---

## 4. 是否改變 accepted 語義

**否。** 既有 Outcome Contract 的 intent、scope（ENHANCED REQUIRED：Leaflet Taiwan Map 六區依色帶著色、`Select Date`、改良 UI／UX、dashboard 整合）、constraints（一個產品兩個呈現層、免金鑰、reserved boundaries）與 acceptance boundary（AB-13～AB-15）全部不變；Spec v1.1 的每一條 R／AC／INV 文字與強度不變；沒有新增 requirement、AC、invariant 或 gate；#18–#25 不重開。本紀錄所有裁決都是治理 §5.3 第 2 類（不改變 accepted 語義的 clarification 與 assurance 具體化）。本 work item 自身的 Outcome Contract（核定文）由 acceptor 接受並授權，DA 未代行任何接受或授權。

指示 §3 所述 acceptor 對 AC-04(b) 原意的說明，本紀錄只記錄、不裁決（3.4 第 3 點）；因此本紀錄沒有對 AC-04(b) 作任何解讀變更。

---

## 5. 受影響的工作、dependencies 與既有 evidence

| 項目 | 影響 |
| --- | --- |
| **#28**（新，Lightweight） | 依本紀錄執行；Executor 以 Issue #28＋本紀錄為契約，維護 `worklog/20260924-taiwan-map-rework.md`；A-4 audit 必做（`audit/issue-28-c1-r1.md` 起），R1 範圍含 3.5(A)。完成後 STOP 回報 preview URL 與票號；不合併、不繳交。 |
| **#18–#25** | 不重開；結案狀態與 audit records 不變。#24 的閉合 findings F-1／F-3／F-4／N-1 以 3.3 P-3／P-6／P-10／P-12 的方式在 #28 內延續（不是重開，是不回歸與順修）。 |
| **Spec v1.1、Outcome Contract、derivation record、Bindings** | 不修改。 |
| **phase-acceptance-SPEC.md** | 其 accepted subject 仍是 `720c0a0`；#28 之後依 3.5(B) 產出增補紀錄，不改寫原紀錄。 |
| **`spec-SPEC-c1-r1.md`** | 對 `720c0a0` 的結論維持有效；對 #28 觸及的部分（地圖卡、靜態檢查、README、ACCEPTANCE.md）由 #28 audit 重新取證；增補紀錄以 diff-scope 證明銜接。 |
| **`doc/acceptance/ACCEPTANCE.md`、`doc/ticket/tickets.md`、README** | 都是 subject 的一部分（不是 record-only）；#28 的 subject SHA 以含這些檔案的 commit 為準（#25 F-3 先例）。 |
| **Release gate（Bindings §5／A-6）** | 合併前材料 ＝ 既有清單 ＋ #28 audit closure ＋ 3.5(B) 增補 ＋ 對 #28 subject 的 CI 綠與 preview smoke。RB-1 仍由 acceptor。 |
| **Orchestrator run record** | 記錄本派工與 binding；#28 以新的 Lightweight work item 記錄（不併入已 terminus 的 `run-20260924-hw01-formal` 的 Formal frontier，MAY 在同一 run record 加「post-run Lightweight work items」段或另開 `run-20260924-hw01-map-rework.md`，屬 control-plane HOW）。 |
| **#18 R2 N-1 的 Lightweight work item**（指示 §5） | 獨立 work item，不在本紀錄內；acceptor 直接指示即其 Outcome Contract，A-4 audit 必做；與 #28 不混在同一 commit。若執行中遇到語義問題再 route DA。 |
| **Executor 環境** | 樣稿 `map-mock/` 只是視覺目標與資料示範；交付物 MUST 依 P-2 自行取得並簡化底圖資料，MUST NOT 複製樣稿的 `fetch`／tile 程式路徑（P-2(d)、P-3）。 |

---

## 6. Authority

- 本裁決在 Design Authority 的 lane eligibility、boundary determination、contract-sufficiency 與 assurance 權限內（治理 §2.1、§2.4、§3.3、§3.6-A、§4.1、§5.1）。
- **不需要 acceptor 的任何動作即可開始 #28**：接受與授權已由核定文給出；Spec review 與 implementation authorization 未被 Bindings 保留（§2.6）。
- **仍屬 acceptor 的事項**（本紀錄不請求，只列出）：RB-1 合併、RB-2 繳交、X-1（OSM 替代——需重新指示）、X-3／X-4（其他區塊重設計或新功能——新 work item）、X-8（底圖資料若需帳號或付費）。
- Reviewer 保有 findings、severity、blocking 與 closure 的判定（§2.1、§4.3）；本紀錄不預判任何 finding。
- Final Adjudicator：目前沒有 routing 或 review 爭議，不需要。
- DA 未修改任何實作、測試、資料、Spec、OC 或 `doc/acceptance/`；未 commit；未 merge。

---

## 7. Evidence（DA 自行執行，全部唯讀；未印出任何金鑰）

- 讀取：Bindings b1 §0–§9；治理 v2.0 §1.2、§1.4、§1.5、§2.1–§2.4、§3.1–§3.8、§4.1–§4.7、§5.1–§5.4；Outcome Contract 全文；Spec v1.1 全文（§0–§10）；derivation-SPEC.md §3、§4、§11.1、§11.3；decision-20260923-spec-interpretation-rulings.md（DR-1～DR-16）；DR-19 全文；decision-20260923-high-risk-categories.md 全文；phase-acceptance-SPEC.md 全文；spec-SPEC-c1-r1.md 全文；issue-24-c1-r1.md、issue-24-c1-r2.md 全文；run-20260924-hw01-formal.md 全文；tickets.md 全文；README `:252-282` 與 grep；`static/app.js`、`static/index.html` 全文；`static/styles.css` 的 map／dark 相關行；`tests/test_static_checks.py:40-229`；`tests/test_dashboard.py:67`（經 #24 R2 記載與 grep）。
- 外部輸入：`gh issue view 28`（body、label `ready-for-agent`、OPEN）；指示文件 `orchestrator-message-map-rework.md` 全文與 `orchestrator-message-map-addendum.md`；補充段 `visual-direction-addendum-map.md` 全文；草稿 `visual-direction-draft.md` §6；樣稿 `map-mock/index.html` 全文、`days.js` 前 40 行、`map-mock/` 與 `map-mock/vendor/` 目錄列表（`counties.geojson` 9,325,913 bytes、`ne50.geojson` 3,083,490 bytes、`context.geojson` 169,604 bytes、vendored Leaflet 與 repo 內同大小）。
- Git：`git rev-parse HEAD` ＝ `d23de58d7ef152a0368e1f8ee1d14cc94eefc138`；`git log --oneline -3` ＝ `d23de58`、`720c0a0`、`75389e6`；`git status --porcelain` 為空；`git diff --name-only 720c0a0 HEAD` ＝ 三個 `doc/governance/**` 檔案。
- Grep：`home_work_01/doc/governance/` 內無 `DR-20`／`DR-21`（本紀錄取 DR-20）；repo 內無 `orchestrator-message-map-rework.md`（該文件只在 acceptor 支援 session 的 scratchpad，內容已依核定文逐字轉錄於第 0 節）。
