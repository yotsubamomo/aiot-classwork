# Derivation record — SPEC（HW10 Taiwan Weather Forecast，`home_work_01/`）

- **紀錄類型**：Design Authority derivation record（治理 §1.2、§3.4；Bindings §7）
- **Derived contract**：[`../../spec/SPEC.md`](../../spec/SPEC.md) **v1.1**（2026-09-23；v1.0 同日 derive，v1.1 為 acceptor 指示的一致性修正，見第 12 節）
- **Outcome Contract**：[`../outcome-contract.md`](../outcome-contract.md)，**DRAFT**，commit `c45ec61`（`main`）；第 8 節接受紀錄為空
- **其他依據**：[`../../brief/BRIEF.md`](../../brief/BRIEF.md)、[`../../../CONTEXT.md`](../../../CONTEXT.md)、上位契約 [`../../requirement/REQUIREMENTS.md`](../../requirement/REQUIREMENTS.md) Part A 與 [`../../requirement/Taiwan_Weather_Forecast_course_overview.md`](../../requirement/Taiwan_Weather_Forecast_course_overview.md) §1–21（皆 `c45ec61`）；`docs/governance/project-bindings.md` b1；治理 v2.0 §1.2、§2.1、§2.4、§3.1、§3.3–3.6、§4.7、§5.1、§5.3
- **附帶 decision records**：[`decision-20260923-high-risk-categories.md`](decision-20260923-high-risk-categories.md)（Bindings §8.2 #5）、[`decision-20260923-spec-interpretation-rulings.md`](decision-20260923-spec-interpretation-rulings.md)（治理 §3.6-A 類裁決）
- **執行角色與 binding**：以 `gov-design-authority` definition 派工（Bindings §3.1：`design_authority` → `claude-fable-5-1`／`xhigh`）。實際 assignment 的核對證據依 Bindings §3.4 由派工者從 harness session 目錄取得並記錄；本紀錄不自證 binding。
- **派工指示**：acceptor 2026-09-23「Derive the implementation-ready Spec for `home_work_01` from the completed grill records … SPEC DERIVATION ONLY」（原文見派工內容）。

## 1. 狀態：待接受

| 項目 | 內容 |
| --- | --- |
| 現況 | Outcome Contract 尚未被接受（Bindings §8.2 #4 binding dry-run、#5 高風險類別、#6 接受紀錄未完成；#5 由本次附帶的 decision record 完成）。 |
| 效力 | 本 Spec **不是**有效的 derived contract，直到 acceptor 於 Outcome Contract 第 8 節填寫接受紀錄；屆時自動生效，不需另行核准（治理 §1.2「derived contract 的成立不需 acceptor 逐份核准」），前提是接受時 Outcome Contract 第 1–7 節的 **normative 內容**與 `c45ec61` **實質相同**。填寫第 8 節接受紀錄與接受 metadata（原文、日期、commit SHA），以及隨接受一併給出、Spec 第 9 節已列為前置條件的授權（例如 B-1 的 RB-5 workflow 授權），本身不是內容變更，不觸發重新 derive；不改變語義的文字校正亦同。本紀錄的 boundary determination 對象是 `c45ec61` 的 normative 內容，不因第 8 節被填寫而失效。 |
| 需重新 derive 的情況 | 接受前或接受時，Outcome Contract 的 normative 內容若有任何 scope、requirement、架構、acceptance boundary，或 authority／authorization 條款本身（reserved boundaries、standing authorizations、授權涵蓋範圍）的變更，本 Spec 與本紀錄須由 Design Authority 重新 derive（或以本紀錄的修訂確認未受影響）；在此之前不得依本 Spec derive Tickets 或啟動 Orchestrator run（orch-default §3 activation 前提 2）。是否「實質相同」由 Design Authority 以本紀錄的修訂確認（治理 §1.2、§5.3）。 |
| 未做 | 未修改 Outcome Contract 任何部分（含第 8 節）；未實作；未建 Ticket；未建或重建 `data.db`；未呼叫 CWA API；未部署；未啟動 run；未 commit。 |

## 2. 依據的 Outcome Contract 條款

| OC 條款 | 用途 | 對應 Spec |
| --- | --- | --- |
| §1 Intent and outcome | Problem Statement／Solution；一個產品兩個呈現層；先滿足 20／20／20／40 再加 ENHANCED | Spec Problem Statement、Solution、INV-2、INV-9 |
| §2.1 上位契約與延伸的邊界 | MVM 完整滿足上位契約；ENHANCED 明確標示、不冒充老師要求 | 來源類型 T／C／P／E 標記；R-DOC-2；INV-9 |
| §2.2 Scope classes | MVM／ENHANCED／OPTIONAL／REFERENCE 的內容清單 | Spec §1 全部 R 的 class；§8 Out of Scope |
| §2.3 資料來源條款（D2 CLOSED） | 推導順序、驗證、標示 | R-ING-1、R-DER-1～R-DER-7、R-DOC-2、INV-3、INV-7 |
| §2.4 應用架構（A1–A4 CLOSED） | 共用層、行為對等、Streamlit 定位、Vercel／Flask、Leaflet、Python 3.12、「API 路徑……屬 DA 的 Spec 決定，除非是可觀察驗收條件」 | R-SHR-*、R-GA-*、R-DS-*、R-EN-4、R-ENV-1；Spec §4.1／§4.2 的固定／委派劃分（DR-1） |
| §2.5 其他 constraints → brief §6 | 快照語義、準備好的快照、路徑處理、憑證、部署設定位置、UI／UX 描述、地圖溫度、測試與 CI、採用的 Part B 做法 | R-DB-4～R-DB-6、R-SHR-3、R-SEC-*、R-EN-1、R-SHR-4、R-TC-*、R-GA-8、R-DS-7、AC-24、AC-30 |
| §3 Acceptance boundary AB-1～AB-17 | 每條 derive 為一條或多條 AC | Spec §2、§7 對應矩陣 |
| §4 Authority and authorization | RB-1～RB-6、SA-1／SA-2、本次 grill 的特定授權 | R-ENV-3、AC-13、AC-29；Spec §8「不由 Agent 執行」、§9 前置條件 |
| §5 Relevant context | 既有產物、外部事實、已知風險 | Spec §9 已知風險 |
| §6 Assurance path | Formal；每 Ticket audit＋Spec Integration Audit；H-1／H-2 待 DA | Spec §6 Verification Strategy；decision record（H） |
| §8.1 Grill 裁決紀錄 | 逐條核對 Spec 未重開任何已結案裁決（Q2–Q7、S2、S5、D0–D2-3、R2–R5、A1–A4、Python、Streamlit 定位、§2.1 邊界） | 全文 |

## 3. Boundary determination

**總判定：Spec v1.1 全部內容在 `c45ec61` Outcome Contract 草稿的 boundary 內；沒有任何 R／AC 超出 §2.2 的 scope classes、§2.3／§2.4 的 CLOSED 條款或 §3 的 acceptance boundary；沒有改變 Outcome Contract 草稿所載、grill 已裁決的語義（其接受後即為治理所稱的 accepted 語義）；沒有重開已結案的 grill 裁決。** 逐項依據如下（只列需要判斷的項目；逐字轉錄 OC 的項目不列）。

| # | 項目 | 判定 | 依據 |
| --- | --- | --- | --- |
| B-1 | **GitHub Actions workflow 檔位於 `.github/workflows/`（單元目錄外）** | **結果在 boundary 內；動作是 reserved boundary。** AB-16／AB-17 明確要求 GitHub Actions 在 push 執行測試與 `workflow_dispatch` smoke；GitHub 只接受 repo 根的 `.github/workflows/`。這不是 contract change（OC 已要求此結果），但建立該檔案是 RB-5「修改該單元目錄以外的檔案」，OC §4 未給予此授權。DA 不得代行。 | OC AB-16、AB-17、§4；Bindings §2.6 RB-5；治理 §1.5 第 3 項 |
| | **處置** | Spec R-ENV-3 把它列為需 acceptor 有範圍授權的前置；未授權前只有 CI／smoke 部分停止，其餘照常。**Required authority：acceptor。** 建議 acceptor 在接受紀錄或對話中一併給出：「授權在 `.github/workflows/` 建立與修改本單元專用（名稱識別 `home_work_01`、路徑過濾至 `home_work_01/**`）的 workflow 檔」。 | |
| B-2 | Vercel 專案建立、Root Directory、production／preview 與 deployment protection 設定；repository variable | 結果（AB-1、AB-17）在 boundary 內；動作為第三方帳號操作（RB-3）。Spec 列為前置（§9 #3、#4）。**Required authority：acceptor 親自操作。** | OC AB-1、AB-17、§4；RB-3 |
| B-3 | 健康 endpoint 路徑固定為 `GET /api/health` 與 200／503 語義 | 在 boundary 內；OC AB-1 明文「路徑由 Spec 決定，例如 `GET /api/health`」。 | OC AB-1、AB-17 |
| B-4 | 資料 endpoint 以 `/api/` 為前綴、確切路徑委派實作；靜態前端無 build step | 在 boundary 內；OC §2.4 把「API 路徑、JS 函式庫、路由設定、模組切分與確切檔案結構」交給 DA 的 Spec 決定，DA 決定只凍結可觀察或跨 Ticket 依賴的部分（DR-1）。 | OC §2.4 末項；acceptor 派工指示「leave low-level HOW decisions to implementation where they do not need to be contractually frozen」 |
| B-5 | Ingestion 中繼資料表（ingestion 時間、來源 ID）與兩層顯示「最後更新時間」 | 在 boundary 內；OC §2.5 引入 brief §6.7「頁面顯示最後更新時間」為已裁決前提；不改 `TemperatureForecasts` DDL，故不觸及 S2「採與老師 DDL 一致的最簡作法」。不是 ENHANCED（DR-2）。 | OC §2.5；brief §6.2、§6.7 |
| B-6 | 「觀察 JSON」「觀察資料」的可觀察產物（原始 JSON 檔、終端預覽） | 在 boundary 內；OC §2.1「MVM 必須完整滿足上位契約」，A1-6、A1-7、A2-1 為有配分的上位契約條款；AB 雖未逐條列出，但 §3 說明「具體 AC 由 DA 在此邊界內 derive」且 §1 要求先滿足評分項目。 | OC §1、§2.1、§3；REQUIREMENTS A.1、A.2 |
| B-7 | 程式品質 AC-27 | 同 B-6；四個「程式品質 5%」與課程總覽 §20 是上位契約。 | OC §2.1；REQUIREMENTS A.10；§20 |
| B-8 | 整份快照原子替換作為「重複執行不重複插入」的機制 | 在 boundary 內；OC §2.5 → brief §6.2「重跑不產生重複邏輯紀錄；採與老師 DDL 一致的最簡作法」；Q4「current one-week forecast snapshot, not historical」。 | OC §2.5、§8.1 Q4 |
| B-9 | 四捨五入採 half-up；色帶以顯示值分帶 | 在 boundary 內；D2-3「rounded to one decimal」未指定 tie 規則，DA 以 decision record 選定（DR-4）；只影響實作與測試期望值。 | OC §2.3、§8.1 D2-3、R5 |
| B-10 | 保留規則的一般化（第一個日期若不完整則丟棄；七日須連續且完整） | 在 boundary 內；D2-1 原文「retain the next seven dates that each contain both expected 12-hour periods」；連續性是「一週」語義的必要條件，不新增行為（DR-5）。 | OC §2.3、§8.1 D2-1 |
| B-11 | Grading App 不含 ENHANCED 項目 | 在 boundary 內；OC §2.2 ENHANCED 列「只在部署的 dashboard」；A3「local Streamlit app … does not need the ENHANCED map」；CONTEXT「Grading App … no enhanced features」。 | OC §2.2、§2.4 |
| B-12 | Fixture 為真實 F-D0047-091 樣本，由 Executor 於實作期擷取 | 在 boundary 內；AB-8 允許 ingestion 以使用者金鑰取得資料；acceptor 派工指示「樣本不可在本次擷取」只限本輪 DA 工作。 | OC AB-8、AB-9 |
| B-13 | AB-1 的驗證時點（合併前以受審 commit 的部署驗、合併後對 production 重跑為 release evidence） | 在 boundary 內；AB-1 只要求公開 URL 成功回應；RB-1 使 production 只在合併後更新；DA 界定 evidence 時點不改變條件（DR-12）。 | OC AB-1、§4 RB-1；Bindings §5 release gate |
| B-14 | OPTIONAL 不 derive | 在 boundary 內；OC §1「任何 optional／reference 項目都不得成為完成條件」。 | OC §1、§2.2 |
| B-15 | 單一 Spec（不拆分） | 見第 4 節。 | 治理 §4.7 |
| B-16 | 新增高風險類別 H-3 | 屬 assurance 決定（治理 §5.1「DA MUST 決定專案適用的高風險分類及 assurance 要求」；Bindings §5「確認或修改」），不改變 OC 的 intent／scope／constraints／acceptance；不新增 audit round。 | decision record |

**未在 boundary 內而未 derive 的事項**：無。**需要 contract change 的事項**：無。

**OC 內部一致性核對**：未發現使 Spec 無法 derive 的矛盾。一處張力——OC §2.4 末項把 API 路徑等列為「DA 的 Spec 決定」，而 acceptor 派工指示要求低階 HOW 留給實作——由 DA 決定凍結範圍解決（DR-1），兩者不衝突。

## 4. Spec 分配到的 acceptance boundary

**只有一份 Spec（SPEC v1.1）。分配：AB-1～AB-17 全部。** 全部 derived Specs 合起來涵蓋整個 acceptance boundary的核對（治理 §4.7 第五 bullet）在本 Spec 的 Spec Integration Audit 執行，因為它同時是第一份與最後一份。

| AB | 分配 | Spec AC | 備註 |
| --- | --- | --- | --- |
| AB-1 | SPEC v1.1 | AC-15、AC-16 | 需 acceptor 的 Vercel 設定（B-2、B-13） |
| AB-2 | SPEC v1.1 | AC-01 | |
| AB-3 | SPEC v1.1 | AC-02 | 兩層 |
| AB-4 | SPEC v1.1 | AC-03 | 兩層 |
| AB-5 | SPEC v1.1 | AC-04 | INV-1、INV-6 |
| AB-6 | SPEC v1.1 | AC-05 | H-2 |
| AB-7 | SPEC v1.1 | AC-06 | INV-3 |
| AB-8 | SPEC v1.1 | AC-07 | H-1 |
| AB-9 | SPEC v1.1 | AC-08、AC-09 | H-3 |
| AB-10 | SPEC v1.1 | AC-10、AC-11、AC-16 | 兩層＋ingestion |
| AB-11 | SPEC v1.1 | AC-12、AC-25 | |
| AB-12 | SPEC v1.1 | AC-13 | 合併為 release，不是完成條件 |
| AB-13 | SPEC v1.1 | AC-14 | H-3、INV-7 |
| AB-14 | SPEC v1.1 | AC-17、AC-18、AC-28 | ENHANCED |
| AB-15 | SPEC v1.1 | AC-19 | ENHANCED |
| AB-16 | SPEC v1.1 | AC-20、AC-21 | ENHANCED；需 RB-5 授權（B-1） |
| AB-17 | SPEC v1.1 | AC-22 | ENHANCED；需 RB-5 授權（B-1）與 repository variable（B-2） |
| 非 AB 的 OC 條款 | SPEC v1.1 | AC-23、AC-24、AC-26、AC-27、AC-29、AC-30 | 來自 §2.1、§2.4、§2.5、§4 的 constraints；不擴張 boundary，只讓 constraints 可驗收 |

**為何不拆分為多份 Spec**：AB-3、AB-4、AB-5、AB-10 各自橫跨兩個呈現層，AB-16 橫跨三個測試接縫，INV-1／INV-2 是兩層共同的 invariant；拆成「資料層 Spec」與「呈現層 Spec」會讓行為對等變成跨 Spec invariant，而治理 §4.7 的 Spec Integration Audit 以單一 Spec 為 subject 才能一次核對它。工作量由 Tickets 分解承擔，不由 Spec 數量承擔。

## 5. Implementation-readiness 核對（治理 §3.4）

| 條件 | 狀態 |
| --- | --- |
| 沒有把必要設計留待下游決定 | 全部會被其他工作依賴的介面與語義已凍結（Spec §4.1）：資料流、推導規則、DDL 與資料表示、共用模組語義、健康 endpoint、頁面文字、技術棧、憑證模型、測試接縫。委派項目（Spec §4.2）都是單一 Ticket 內可自行決定、不被其他 Ticket 依賴的 HOW。 |
| 每條 AC 有可觀察 PASS／FAIL 與證據要求 | Spec §2 三十條各有 PASS 條件、FAIL 例、證據與方法。 |
| Invariants 明確 | Spec §3 INV-1～INV-9。 |
| Dependencies 可辨識 | 第 7 節的預期分解已列依賴；正式 dependencies 在 Ticket derivation 時定。 |
| Verification contract 不由下游重新定義 | Spec §6 規定各階段誰看什麼；Tickets 只能引用。 |

## 6. 高風險類別與 assurance

依 Bindings §5、§8.2 #5，見 [`decision-20260923-high-risk-categories.md`](decision-20260923-high-risk-categories.md)：確認 H-1、H-2，新增 H-3，並規定 Ticket audit record 對觸及類別的核對義務。Spec §6 的 Verification Strategy 引用之。

## 7. 受影響工作

| 工作 | 影響 |
| --- | --- |
| 進行中的 work item | 無。`home_work_01/` 目前只有文件，沒有實作與 Ticket。 |
| Tickets | **已於 2026-09-24 derive 為 Issues #18–#25，見第 11 節**（本列其餘為 2026-09-23 的規劃紀錄，保留供追溯）。原預期分解（非約束）：T-A ingestion＋推導＋持久化＋fixture＋pytest（AB-6～AB-9、AB-11 部分）→ T-B 共用模組＋Grading App＋`AppTest`（AB-2～AB-5、AB-10）→ T-C Flask API＋靜態 dashboard MVM＋test client（AB-1 本機部分、AB-3～AB-5、AB-10）→ T-D dashboard ENHANCED：UI／UX、`Select Date`、Leaflet 地圖（AB-14、AB-15）→ T-E CI 與 smoke workflow（AB-16、AB-17；RB-5 gated）→ T-F Vercel 部署、README、驗收文件（AB-1、AB-11～AB-13）。依賴：B←A；C←B；D←C；E←A、B、C；F←C、D、E。並行度 1（Bindings §6）。 |
| 既有紀錄 | grill worklog `worklog/20260923-grill-outcome-contract.md` 的「Remaining work」第 4 列（DA derive Spec）在 OC 接受後可標為 Spec 已 derive、Tickets 待 derive；本紀錄不修改它。 |
| Outcome Contract | 不修改。建議 acceptor 接受時附上 B-1 的 RB-5 授權原文（不需改 OC 內容；記在第 8 節即可）。 |
| `CONTEXT.md` | 不需修改；Spec 用語與其一致。若實作期需要新詞（例如中繼資料表的概念名），由 Executor 依 `docs/agents/domain.md` 提出。 |
| Bindings | 不需修改。H-3 是 DA 依 §5.1 的決定，Bindings §5 已預留「由 DA 確認或修改」。 |

## 8. 需要其他 authority 的事項

| # | 事項 | Authority | 理由 |
| --- | --- | --- | --- |
| 1 | 接受 Outcome Contract（第 8 節）；第 1–7 節 normative 內容與 `c45ec61` 實質相同時 Spec 自動生效（Spec §0、本紀錄第 1 節） | acceptor | 治理 §1.2；本 Spec 的生效條件 |
| 2 | 對 `.github/workflows/` 內本單元 workflow 檔的有範圍 RB-5 授權 | acceptor | B-1；未授權則 AB-16／AB-17 路徑 fail-closed |
| 3 | Vercel 專案建立、Root Directory、production／preview 或 deployment protection 設定；repository variable | acceptor | B-2；RB-3 |
| 4 | 本機安裝 Python 3.12 | acceptor | brief §7 #4 |
| 5 | Bindings §8.2 #4 binding dry-run | acceptor／主 session | Formal activation 前提 |

以上皆非 contract change；Outcome Contract 草稿所載的語義不變。

## 9. Evidence

- 讀取：`docs/governance/project-bindings.md`、`minimal-operational-governance-v2.0.md`（全文）、三份 references；`home_work_01/doc/governance/outcome-contract.md`、`doc/brief/BRIEF.md`、`CONTEXT.md`、`doc/requirement/REQUIREMENTS.md`（全文）、`Taiwan_Weather_Forecast_course_overview.md`、`doc/governance/worklog/20260923-grill-outcome-contract.md`、`.env.example`（只有變數名）、root `.gitignore`、`CLAUDE.md`、`docs/agents/*.md`、`docs/conventions/git-commit-rules.md`、`week02/doc/spec/SPEC.md`、`week02/doc/ticket/tickets.md`、`week02/doc/acceptance/ACCEPTANCE.md`。
- `git log`：`c45ec61` 為 `main` HEAD，含 OC、brief、CONTEXT、REQUIREMENTS 等 8 個檔案；工作樹 clean。
- `home_work_01/` 檔案清單：只有文件、`.env`（未追蹤、未讀取）、`.env.example`、receipts；**沒有任何實作**。
- `/to-spec` skill 未安裝於本環境（搜尋 `.claude/`、user skills、plugins 皆無）；Spec 結構沿用 `week02/doc/spec/SPEC.md` 前例，加上 acceptor 要求的 R／AC／對應矩陣／verification strategy。
- 未讀取 `home_work_01/.env`；未讀取 PDF；產出不含任何金鑰字串。

## 10. 寫入的檔案

| 檔案 | 動作 |
| --- | --- |
| `home_work_01/doc/spec/SPEC.md` | 新增（v1.0）；同日續派修訂為 v1.1（第 12 節） |
| `home_work_01/doc/governance/decisions/derivation-SPEC.md` | 新增（本檔）；同日續派修訂第 1、3、4、8、10、12 節 |
| `home_work_01/doc/governance/decisions/decision-20260923-high-risk-categories.md` | 新增；同日續派修訂 H-1 表、A-5、第 4 節與修訂註 |
| `home_work_01/doc/governance/decisions/decision-20260923-spec-interpretation-rulings.md` | 新增；同日續派修訂效力段、用語註與總結 |

未 commit；依 SA-1 由派工者於 OC 接受流程中處理。

## 11. Tickets（2026-09-24 derive）

- **依據**：Outcome Contract **ACCEPTED**（2026-09-23，§8；normative 第 1–7 節與 `c45ec61` 相同；acceptor 原文確認 Spec v1.1 隨接受生效並給出限定範圍的 RB-5 GitHub Actions 授權）；Spec v1.1 **EFFECTIVE**；Bindings §8.2 #4 binding dry-run PASS（`docs/governance/binding-verification.md`）。
- **派工指示**：acceptor 2026-09-23「Derive the implementation-ready Ticket set for `home_work_01` from the effective `SPEC.md` v1.1 … TICKET DERIVATION ONLY」。
- **索引**：[`../../ticket/tickets.md`](../../ticket/tickets.md)。Tickets 本體在 GitHub Issues #18–#25，label `ready-for-agent`。
- **Spec 對應版本**：v1.1（本次只更新 Spec §0 狀態列與 §10 版本紀錄的 metadata，語義與版本不變）。

### 11.1 Ticket 清單與分配

| # | 票 | Class | 分配的 AC | 分配的 AB | INV | High-risk | Blocked by |
| --- | --- | --- | --- | --- | --- | --- | --- |
| #18 | Ingestion：F-D0047-091 → Forecast Snapshot → `data.db` | MVM | AC-05、AC-06、AC-07(a–d)、AC-08、AC-09、AC-11、AC-24（資料面）、AC-25（產物）、AC-27（部分） | AB-6、AB-7、AB-8、AB-9、AB-10（ingestion）、AB-11／AB-13（部分） | INV-3、INV-4、INV-5、INV-7（資料面）、INV-8 | H-1、H-2、H-3 | — |
| #19 | 共用模組＋Grading App | MVM | AC-01、AC-02（GA）、AC-03（GA）、AC-04（Python 側）、AC-10（GA）、AC-24（GA）、AC-26、AC-28（Python 側）、AC-27（部分） | AB-2、AB-3、AB-4、AB-5、AB-10、AB-14（支撐） | INV-1、INV-2（基準）、INV-4、INV-6、INV-9 | H-2、H-3（H-1 靜態檢查） | #18 |
| #20 | Dashboard MVM 本機 | MVM | AC-02（DS）、AC-03（DS）、AC-04（完整）、AC-10（DS）、AC-16、AC-24（DS）、AC-27（部分） | AB-1（本機）、AB-3、AB-4、AB-5、AB-10 | INV-1、INV-2、INV-4、INV-6 | H-1、H-2 | #19 |
| #21 | Vercel 部署 | MVM | AC-15、AC-23（Vercel）、AC-30、AC-07(e) | AB-1 | INV-5、INV-8 | H-1 | #20 |
| #22 | CI／smoke workflow | ENHANCED | AC-20、AC-21、AC-22、AC-29、AC-07(b–d 自動化) | AB-16、AB-17 | INV-5、INV-8 | H-1 | #20、#21 |
| #23 | UI／UX | ENHANCED | AC-19；回歸 AC-02／03／04(b)／10（DS） | AB-15 | INV-2、INV-6、INV-9 | H-2 | #21、#22 |
| #24 | Select Date＋Taiwan Map | ENHANCED | AC-17、AC-18、AC-28（前端側）、AC-14（第 6 項）、AC-19（重驗） | AB-14、AB-15、AB-13（部分） | INV-2、INV-7、INV-9 | H-2、H-3 | #23 |
| #25 | 整合驗收 | INTEGRATION／FINAL VERIFICATION（非 scope class；2026-09-24 重新分類，原 MVM） | AC-12、AC-13、AC-14、AC-15（重跑）、AC-22（重跑）、AC-23、AC-25、AC-27、AC-30；重驗 AC-02／03／04／07／10／19／24 | AB-1、AB-11、AB-12、AB-13；全部 AB 的最終對照 | INV-1～INV-9 最終核對 | H-1、H-2、H-3 | #22、#24 |

### 11.2 覆蓋矩陣（自我核對）

| Spec 項目 | 涵蓋票 |
| --- | --- |
| R-ING-1～6、R-DER-1～8、R-DB-1～6 | #18（R-DB-5 讀取側 #19） |
| R-SHR-1～5 | #19（R-SHR-5 JS 側 #20；R-SHR-4 前端等價 #24） |
| R-GA-1～9 | #19 |
| R-DS-1～R-DS-7 | #20 |
| R-DS-8、R-DS-9 | #20（結構）、#21 |
| R-EN-1、R-EN-2、R-EN-7 | #23（#24 完成整合） |
| R-EN-3～R-EN-6 | #24 |
| R-TC-1 | #18、#19 |
| R-TC-2 | #18 |
| R-TC-3 | #19 |
| R-TC-4 | #20 |
| R-TC-5 | #18、#22 |
| R-TC-6 | #22 |
| R-TC-7 | #21（本機指令）、#22（workflow） |
| R-SEC-1、R-SEC-2 | #18（CI 自動化 #22） |
| R-SEC-3 | #20、#21 |
| R-DOC-1 | 每票增補該票段落；#25 完整 |
| R-DOC-2 | #18、#19、#24、#25 |
| R-DOC-3、R-DOC-4 | #25 |
| R-DOC-5 | 每票；#25 |
| R-ENV-1、R-ENV-2 | #18、#21、#25 |
| R-ENV-3 | #22 |
| AC-01～AC-30 | 每條至少一張票（見 11.1；AC-01 #19；AC-05／06／08／09／11 #18；AC-12／13／14 #25；AC-15 #21、#25；AC-16 #20；AC-17／18 #24；AC-19 #23、#24、#25；AC-20／21／22／29 #22；AC-23 #21、#25；AC-25 #18、#25；AC-26 #19；AC-28 #19、#24；AC-30 #21、#25） |
| INV-1～INV-9 | 每條至少兩張票；#25 最終核對全部 |
| AB-1～AB-17 | 全部涵蓋（AB-1 #20／#21／#25；AB-2 #19；AB-3～AB-5 #19、#20；AB-6～AB-9 #18；AB-10 #18–#20；AB-11 #18、#25；AB-12 #25；AB-13 #18、#24、#25；AB-14 #19、#24；AB-15 #23、#24；AB-16、AB-17 #22） |

**缺口：無。** MVM 票（#18–#21）的 blocked-by 只含 MVM 票；#25 分類為 INTEGRATION／FINAL VERIFICATION（非 MVM／ENHANCED），為 Spec §6 要求的整合驗證工作，合法地依賴全部 MVM 與 ENHANCED 票。

### 11.3 Boundary determination

| # | 判定 | 依據 |
| --- | --- | --- |
| TB-1 | 八張票的 What to build 與 AC 全部引用 Spec v1.1 既有的 R／AC／INV，沒有新增 requirement、AC 或 scope；票內只引用不重定義 PASS／FAIL 語義（治理 §3.4）。 | Spec §1–§3 |
| TB-2 | 部署（#21）排在 ENHANCED 之前、CI（#22）為 ENHANCED 但排在 UI 票之前：這是執行順序的設計，不改變 scope class；MVM 完成不依賴 ENHANCED。 | OC §1、§2.2；Spec INV-9 |
| TB-3 | #22 的 root 變更限於 Outcome Contract §8.2 授權範圍（只服務 `home_work_01`、path filter）；票內逐字引用該範圍。其他 root 變更仍為 RB-5 保留。 | OC §8.2；Bindings §2.6 |
| TB-4 | #21 的 Vercel 專案建立與 #22 的 repository variable 為 acceptor 動作（RB-3），票內列為前置；未完成時 Orchestrator 只停止該路徑（治理 §1.5、orch-default §5）。 | Spec §9 #3、#4 |
| TB-5 | #25 不引入新的 AC；它是 Spec §6 Verification Strategy 的整合驗證與 R-DOC-4 驗收文件，並準備 Spec Integration Audit 的 subject（impl-default §6）。合併與繳交仍為 RB-1、RB-2。 | 治理 §3.8、§4.7；Bindings §5 |
| TB-6 | 票標題與內文使用 `CONTEXT.md` 詞彙；不含檔案路徑與程式碼（老師指定的 `app.py`、`data.db`、`TemperatureForecasts`、`streamlit run app.py`、`requirements.txt`、README 與 Bindings §7 要求的 Spec／worklog／decision 路徑除外）。 | CLAUDE.md；Bindings §7 |
| TB-7 | 沒有發現使分解不可能的 Spec 矛盾；未重開任何架構或產品決定。 | — |
| TB-8 | **#25 重新分類**（acceptor 2026-09-24 指示）：由「MVM（整合）」改為 INTEGRATION／FINAL VERIFICATION。它不是第三種 scope class、不新增需求；只解決「MVM 票不依賴 ENHANCED 票」與 #25 依賴 #24 的表述衝突。#25 的需求、DoD、依賴（#22、#24）、驗證責任與覆蓋不變；依賴圖與執行順序不變。 | 治理 §5.3 第 2 類；acceptor 指示原文 |
| TB-9 | **Overnight run readiness**：acceptor 2026-09-24 的 execution policy 與治理 §1.4／§1.5／§2.4／§3.8／§4.4–4.5 一致，且 Spec／Tickets 沒有條款迫使不必要的停止；AC-22 在 repository variable 缺席時的處理、Vercel 失敗的重試邊界、fixture 擷取的授權來源、手動驗收由 Executor 執行等解讀，見 `decision-20260924-unattended-run-policy.md`。 | 治理 §3.6-A |

### 11.4 既有 evidence 的可用範圍

目前沒有任何實作或既有測試 evidence；`c45ec61` 之後的工作樹只有文件與 record。brief §4.5 的 F-D0047-091 結構與 §4.6 的樣本驗算可作 #18 的設計輸入，但不是 verification evidence；#18 須自行擷取 fixture 並產生測試證據。

### 11.5 需要 acceptor 的事項（Ticket 層）

| # | 事項 | 影響的票 | Authority |
| --- | --- | --- | --- |
| 1 | 建立 Vercel 專案、Root Directory ＝ `home_work_01`、受審 commit 的部署不需登入可存取 | #21（及其後） | acceptor（RB-3） |
| 2 | 設定 smoke 用的 repository variable | #22 AC-22（否則該 AC 路徑 BLOCKED，其餘先完成） | acceptor（RB-3） |
| 3 | 本機 Python 3.12 | #18 | acceptor |
| 4 | 開符合 `orchestrator` mapping 的主 session 啟動 Formal run | 全部 | acceptor（Bindings §3.3） |
| 5 | 合併（RB-1）、繳交（RB-2） | #25 之後 | acceptor |

### 11.6 Evidence

- Issues：<https://github.com/yotsubamomo/aiot-classwork/issues/18> … `/issues/25`（2026-09-24 建立；label `ready-for-agent` 既存於 repo，未新建 label）。
- 建立後核對：八張票 body 無殘留 placeholder、無金鑰格式字串、各自引用 `doc/governance/worklog/issue-<n>.md`、`Blocked by` 為真實編號；GitHub 原生 issue dependencies 建立結果見 `tickets.md`。
- 本輪未實作、未建 `data.db`、未呼叫 CWA API、未部署、未啟動 run、未 commit、未動 repository variables 或 Vercel。

### 11.7 五方一致性核對（2026-09-24，#25 重新分類後）

方法：以程式讀取 (a) GitHub Issue #18–#25 的 body（Scope class、Blocked by、Traceability、High-risk 段）、(b) GitHub 原生 issue dependencies（REST `dependencies/blocked_by`）、(c) `tickets.md` 表格、(d) 本紀錄 §11.1 表格、(e) Spec v1.1 §1／§2／§3 的 R／AC／INV 條目與 §7 對應矩陣，逐項比對。

| 核對項 | 結果 |
| --- | --- |
| 依賴圖：body、原生 dependencies、`tickets.md`、§11.1 四方對每張票的 Blocked by 相同；共 10 條邊：19←18；20←19；21←20；22←20、21；23←21、22；24←23；25←22、24 | PASS，與重新分類前相同 |
| 執行順序：每條邊的 blocker 編號都小於被阻擋票 → #18→#25 的編號順序即唯一序列順序 | PASS，未改變 |
| 分類：body 與 `tickets.md`、§11.1 一致；#18–#21 MVM、#22–#24 ENHANCED、#25 INTEGRATION／FINAL VERIFICATION；MVM 票的 blocker 只有 MVM 票 | PASS |
| High-risk：body、`tickets.md`、§11.1 三方相同（#19 三方皆記 H-1 為靜態檢查涵蓋）。H-1 → #18、#19、#20、#21、#22、#25；H-2 → #18、#19、#20、#23、#24、#25；H-3 → #18、#19、#24、#25 | PASS |
| R 群組覆蓋：Spec 的 ING、DER、DB、SHR、GA、DS、EN、TC、SEC、DOC、ENV 十一組都出現在至少一張票的 Traceability | PASS |
| AC-01～AC-30：每條至少一張票 | PASS，缺口 0 |
| INV-1～INV-9：每條至少一張票 | PASS，缺口 0 |
| AB-1～AB-17：每條至少一張票 | PASS，缺口 0 |
| §11.1 對每張票分配的 AC／AB 都是該票 body Traceability 的子集 | PASS |
| 每張票：label `ready-for-agent`；引用自己的 `doc/governance/worklog/issue-<n>.md`；body 無金鑰格式字串 | PASS |

Spec traceability：Spec §7 對應矩陣（AB→AC→R）未改動；Tickets 只引用其 ID。本次未改任何 Issue 的依賴或原生 dependency 記錄；只更新 Issue #25 的 Scope class 段與其 Decisions 引用列。

## 12. 修訂紀錄

| 版本 | 日期 | 依據 | 變更 | 性質 |
| --- | --- | --- | --- | --- |
| Spec v1.0／本紀錄初版 | 2026-09-23 | acceptor 派工「SPEC DERIVATION ONLY」 | 初版 derive。 | — |
| Tickets 修訂／本紀錄修訂 | 2026-09-24 | acceptor 續派「Ticket #25 classification … SPEC.md stale Ticket metadata … Verify the derived Ticket graph … Unattended overnight Formal-run readiness」 | (1) #25 重新分類為 INTEGRATION／FINAL VERIFICATION（Issue #25 Scope class 段、`tickets.md`、本紀錄 §11.1／§11.2／TB-8）；需求、DoD、依賴、驗證責任、覆蓋不變。(2) Spec 標頭「Issue tracker」列改為 Tickets #18–#25 已 derive 與索引路徑；§10 的 2026-09-24 metadata 列同步修正。(3) 五方一致性核對（Issue bodies、GitHub 原生 dependencies、`tickets.md`、本紀錄、Spec traceability）結果記於 §11.7。(4) 新增 `decision-20260924-unattended-run-policy.md`（TB-9）。 | 治理 §5.3 第 2 類。依賴圖、執行順序、Spec normative 內容、AB 分配皆不變。 |
| Spec v1.1／本紀錄修訂 | 2026-09-23 | acceptor 續派「perform one Spec consistency correction pass only」（原文四項） | (1) Spec §0 與 Problem Statement：把「已接受的邊界」改為「由已完成的 grill 裁決、記於 Outcome Contract 草稿（待接受）的邊界」；生效條件改為「第 8 節填寫接受紀錄即生效，前提是第 1–7 節 normative 內容與 `c45ec61` 實質相同；接受紀錄、接受 metadata 與隨接受給出的前置授權不是內容變更」；「失效條件」改為「重新 derive 條件」，限於 scope、requirement、架構、acceptance boundary、authority／authorization 條款本身的變更。(2) R-SEC-1、AC-07、INV-5：金鑰零外洩的掃描範圍改為追蹤檔案、staged／committed diff、log、fixture、保存的 JSON、文件、前端／靜態資源、產生的 evidence，明確排除被忽略的 `home_work_01/.env`（唯一授權位置）；不再以「整個工作樹零金鑰」為條件。(3) AC-04、R-SHR-5、INV-1：明確為「`app.py` 與 Flask 後端 import 同一個共用 Python 模組；瀏覽器端 JS 只呼叫 Flask 的 `/api/`」，不再可被讀成瀏覽器 JS 需 import Python 模組。(4) Spec §8 OPTIONAL 與 §9 前置 #1、本紀錄第 1、3、8 節、兩份 decision record：把「授權／accepted 語義」的用語對齊為「Outcome Contract 草稿所載、grill 已裁決的語義」。 | 治理 §5.3 第 2 類（不改變 accepted 語義的 derived contract 修訂）。**未改變任何 normative 產品決定**：架構、scope classes、D2 推導語義、requirement intent、AB 分配（第 4 節）全部不變。受影響工作：無進行中 work item；Tickets 尚未 derive。 |
