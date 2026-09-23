# Decision record — 高風險類別與 assurance 要求（`home_work_01/`）

- **紀錄類型**：Design Authority decision record（治理 §5.1「Design Authority MUST 決定專案適用的高風險分類及 assurance 要求」；Bindings §5、§8.2 #5）
- **日期**：2026-09-23
- **適用範圍**：`home_work_01/` 全部 work items（Formal 主體與其後的 Lightweight 單點修正）
- **相關契約**：Outcome Contract 草稿 `c45ec61` §6；Spec v1.1 §6
- **用語**：本紀錄所稱「accepted 語義」指 Outcome Contract 草稿所載、grill 已裁決、接受後即為治理 §1.2 所稱 accepted 語義的內容；Outcome Contract 目前仍為 DRAFT。
- **修訂**：2026-09-23 續派（acceptor 一致性修正指示）修訂 H-1 表的授權位置、A-5 的掃描範圍與第 4 節用語；未改變分類或 assurance 要求的實質。
- **執行角色**：`gov-design-authority`（binding 核對由派工者依 Bindings §3.4 記錄）

## 1. 問題

Bindings §5 列出兩個初始候選高風險類別（H-1 憑證與機密、H-2 老師指定的介面或資料格式），要求第一次 Formal activation 前由 Design Authority 以 decision record 確認或修改；Outcome Contract §6 亦列為待 DA 確認。需決定：類別內容、是否增減、各類別的 assurance 要求。

## 2. 裁決

### 2.1 H-1 憑證與機密 — **確認**，內容具體化

| 項目 | 內容 |
| --- | --- |
| 風險 | acceptor 的 CWA 金鑰進入任何可公開的位置。 |
| 唯一授權位置 | 被 `.gitignore` 忽略、未追蹤的 `home_work_01/.env`。金鑰掃描明確排除它；「整個工作樹零金鑰」不是要求。 |
| 涵蓋位置 | git 追蹤的任何檔案（含 `data.db`、fixture、保存的原始 JSON、README、截圖）；staged／committed diff；終端與 CI log；前端程式與部署產物；Vercel 環境變數；worklog、audit、acceptance 紀錄；PR 描述與 Issue。 |
| 觸及的工作 | 任何讀取 `.env`、發出 CWA 請求、保存回應、產生 fixture、撰寫部署設定、撰寫文件的變更。 |
| 對應 Spec | R-ING-2、R-SEC-1～R-SEC-3、AC-07、INV-5 |

### 2.2 H-2 老師指定的介面或資料格式 — **確認**，內容列舉

| 項目 | 內容 |
| --- | --- |
| 風險 | 評分直接依賴的名稱或格式被改動，導致老師的指令或 SQL 失效、或評分項目找不到對應產物。 |
| 涵蓋項目 | `home_work_01/app.py` 與 `streamlit run app.py`；`data.db`；`TemperatureForecasts` 的 CREATE TABLE DDL 與五個欄位名／型別；六個 Region 中文全名；`dataDate` 的 `YYYY-MM-DD`；老師的兩句驗證 SQL 的結果；頁面文字 `Taiwan Weather Forecast`、`Select Region`、`Select Date`、`Date`、`MinT`、`MaxT`；`requirements.txt` 與 README 的存在。 |
| 觸及的工作 | 任何改動上述名稱、DDL、資料表內容形狀、頁面標籤的變更；任何在 `data.db` 內新增物件的變更（須證明 DDL 未變）。 |
| 對應 Spec | R-DB-1～R-DB-3、R-GA-1～R-GA-5、R-DS-4、AC-01～AC-03、AC-05、AC-26、INV-4 |

### 2.3 H-3 資料語義與標示 — **新增**

| 項目 | 內容 |
| --- | --- |
| 風險 | 六區 × 七天的相容性推導被默默改變（分母、日界、對應、四捨五入），使「提取正確 10%」與 AB-9 失效而測試仍綠；或文件把專案推導值寫成 CWA 發布值，違反 AB-13 與 Bindings §2.4「不得冒充老師要求的行為」。 |
| 涵蓋項目 | W1 分組與完整性判定；保留規則（七個連續完整日）；縣市日 MinT／MaxT 聚合；Region 對應表；算術平均與 half-up 一位小數；「成員縣市齊全否則報錯」；6 × 7 驗證與不部分寫入；Derived Map Temperature 與色帶；PROJECT-DERIVED COMPATIBILITY VALUES、專案定義對應表、導出值三項標示。 |
| 觸及的工作 | 任何改動推導函式、驗證邏輯、對應表、fixture 期望值、Derived Map Temperature、或相關文件措辭的變更。 |
| 對應 Spec | R-DER-1～R-DER-7、R-SHR-4、R-DOC-2、R-EN-5、AC-08、AC-09、AC-14、AC-28、INV-3、INV-7 |

理由：H-1、H-2 涵蓋「洩漏」與「名字」，但不涵蓋「值是否算對、是否誠實標示」；後者是本作業最大的內容風險（資料來源已替換，值是專案推導的），且測試期望值本身也可能被改。列為高風險使 §4.5 的 deferral 限制與 Lightweight audit 觸發條件適用於它。

### 2.4 不新增的候選

- 部署可用性（AB-1）：失敗可觀察且可重試，不是隱性風險，不列。
- UI／UX（AB-15）：ENHANCED、手動驗收，不列。

## 3. Assurance 要求

| # | 要求 | 適用 | 依據 |
| --- | --- | --- | --- |
| A-1 | **Formal Ticket audit**：Ticket 觸及 H-1／H-2／H-3 任一類別時，其 R1 audit record MUST 有一節明記「觸及的類別、核對了什麼、結果」；R2 對該節的修正結果重述。不新增 audit round。 | 全部 Formal Tickets | 治理 §4.6；orch-default §7「不新增 round」 |
| A-2 | **Spec Integration Audit** MUST 逐項核 INV-4（H-2）、INV-5（H-1）、INV-3 與 INV-7（H-3），並對提交的 `data.db` 實際執行老師的兩句驗證 SQL。 | Spec v1.1 | 治理 §4.7 |
| A-3 | **Deferral**：高風險類別的 blocking finding，Final Adjudicator 不得單獨 deferred，須另有 DA 確認並記入 disposition。 | 全部 | 治理 §4.5（重申，非新增） |
| A-4 | **Lightweight audit 觸發**：結案後的 Lightweight 單點修正（Bindings §4 第 3 列）若觸及 2.1～2.3 列出的「觸及的工作」，MUST 執行 independent audit；worklog 不得標「依 policy 未要求」。 | 結案後 | Bindings §5 觸發條件 |
| A-5 | **機械檢查納入 CI**（Spec R-TC-6、AC-07）：`git ls-files` 無 `.env`；追蹤檔案與 staged／committed diff 無金鑰格式字串（掃描明確排除被忽略的 `home_work_01/.env`）；fixture 與保存的 JSON 無 `Authorization` 值；DDL 比對。CI 檢查是 evidence，不取代 Reviewer 判斷。 | Formal | 治理 §5.4「已可由既有 tooling 檢查者 SHOULD 使用」 |
| A-6 | **Release gate**（合併前，acceptor 執行 RB-1）：維持 Bindings §5 三項；另附 A-2 的 SQL 執行結果與 A-5 的最後一次 CI 結果引用，記在 `doc/acceptance/`。 | Release | Bindings §5 |
| A-7 | **Model diversity**：維持 Bindings §5——沒有類別要求恢復 diversity 才能 audit；`diversity_lost` 照記。 | 全部 | Model Profile §4 |

## 4. 是否改變 accepted 語義

**否。** 本裁決只決定 assurance 分類與核對義務，不改變 Outcome Contract 草稿所載（接受後即為 accepted）的 intent、scope、constraints 或 acceptance semantics，不新增 requirement／AC／gate 的內容，不新增 audit round。H-3 的新增是治理 §5.1 授予 DA 的決定，Bindings §5 明文「確認或修改」。

## 5. 受影響 work items

- Tickets #18–#25（2026-09-24 derive）：每張票的 High-risk 段已標示觸及的類別（H-1：#18、#20、#21、#22、#25；H-2：#18、#19、#20、#23、#24、#25；H-3：#18、#19、#24、#25；#19 對 H-1 以靜態檢查涵蓋）。
- Reviewer 的 audit record：依 A-1 增加一節。
- Orchestrator run record：依 A-3 在 disposition 時核對 DA 確認存在（只核對存在）。
- Bindings：不需修改；§5 的候選列表由本紀錄取代為有效分類。

## 6. Evidence

- Bindings §5、§8.2 #5；治理 §4.5、§5.1、§5.4。
- Outcome Contract `c45ec61` §6、AB-6、AB-8、AB-9、AB-13。
- REQUIREMENTS.md A.3（DDL、驗證 SQL）、A.9 第 1、2 條；brief §4.6 驗證與標示要求。
