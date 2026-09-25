# Derivation record — SPEC-V2（HW01 Weather Map V2，`home_work_01/`）

- **紀錄類型**：Design Authority derivation record（治理 §1.2、§3.4；Bindings §7「Spec 與其 Tickets 的 derivation 都記在這裡」）。本紀錄同時承載本次 derive 中依治理 §3.6-A 作出的 DA 裁決（DV-1～DV-19），效力與 decision record 相同；不另開 decision record（派工指示：只在需要新的高風險類別時才開）。
- **Derived contract**：[`../../spec/SPEC-V2.md`](../../spec/SPEC-V2.md) **v2.2**（2026-09-25；v2.0 初版、v2.1 與 v2.2 依 acceptor 指示修正，見 §14），**DERIVED — effective as derived contract of the accepted V2 Outcome Contract**。
- **Outcome Contract**：[`../outcome-contract-v2.md`](../outcome-contract-v2.md)，**ACCEPTED 2026-09-25**；normative §1–8 ＝ candidate commit `69c5a049104b2fd96289d10ff938c2c8a6d59bd4`；接受紀錄 commit `f853bcbc69ed75a27b77aeb609daabe103c96a25`；合併進 `main` 於 `8c4667d4d20fd82718d6acb4a29392cc5679b516`（PR #33）。acceptor 原文（OC §9.1）：「no additional scope beyond the candidate SHA is authorized by this acceptance」。
- **其他權威輸入**（identity）：
  - 治理 `docs/governance/minimal-operational-governance-v2.0.md`（v2.0 Adopted／Frozen）；Project Bindings **b3**（`docs/governance/project-bindings.md`，RB-3 兩個金鑰位置，PR #31 `0b42208`）；`docs/governance/binding-verification.md`（b1 6／6 PASS；b2 `executor` override dry-run 2／2 PASS，PR #32 `588ef57`）。
  - V2 Brief `home_work_01/doc/brief/BRIEF-V2.md`（同 candidate `69c5a04`；§3 事實、§9 詞彙 delta；附錄 A 為非契約 UI／UX 建議）。
  - **Inherited baseline**：V1 Outcome Contract（ACCEPTED 2026-09-23，normative `c45ec61`）；V1 Spec v1.1 EFFECTIVE；`derivation-SPEC.md`；DR-1～DR-16（`decision-20260923-spec-interpretation-rulings.md`）；H-1～H-3（`decision-20260923-high-risk-categories.md`）；DR-17（ingestion 時間戳）；DR-18（AC-22）；DR-19（dashboard 狀態對應）；DR-20（Taiwan Map 重做）；DR-21（RS-1／RS-2）；DR-22（取得時間驗證）；`phase-acceptance-SPEC.md`（`720c0a0`）與兩份增補（`5136bd2`、`ee84480`）；V1 驗收 `doc/acceptance/ACCEPTANCE.md` 與截圖。V1 結案實作 ＝ `main` `ef15d3e`（squash merge，DA 以 `git merge-base --is-ancestor` 確認為 `main` HEAD 的祖先）＝ 現行 `main` `8c4667d` 的 `home_work_01/` 內容（166 個追蹤檔）。
  - 上位契約（唯讀）：`doc/requirement/REQUIREMENTS.md` Part A、課程總覽 §1–21；Part B §B.2、§B.4、§B.16、§B.22、§B.24 只作 V2 構想來源核對。
  - 現行實作（唯讀，只為 grounding）：`server.py`、`api/index.py`、`vercel.json`、`weather_query.py`（只 grep）、`static/app.js`、`static/index.html`、`static/styles.css`（grep）、`static/data/basemap.js`（檔頭）、`tests/test_static_checks.py`、`tests/test_map_frontend.py`（測試名）、`tools/credential_scan.py`、`smoke.py`（檔頭）、`.github/workflows/home_work_01-ci.yml`、`home_work_01-smoke.yml`、README 標題與地圖／部署段、`CONTEXT.md`、`doc/ticket/tickets.md`。
  - 非規範指引：`D:/nchu/Portable SDD Interaction Guidance — 2026-09-25.md` Part B §8–§9（只用於 Spec 生成與自我審查的檢查清單）。
- **未讀取／未使用**：`home_work_01/.env`；任何 API key；未呼叫 CWA；未讀 PDF。
- **執行角色與 binding**：以 `gov-design-authority` definition 派工（Bindings §3.1：`design_authority` → `claude-fable-5-1`／`xhigh`）。實際 assignment 的核對證據依 Bindings §3.4 由派工者從 harness session 目錄取得並記錄；本紀錄不自證 binding。
- **派工指示**：acceptor 2026-09-25「Proceed with V2 DELTA SPEC DERIVATION only … Do NOT: edit the V1 Spec; rewrite V1 requirements; create Tickets yet; implement; start the Orchestrator; change the accepted V2 Outcome Contract / Brief; reopen resolved Grill decisions unless a material contradiction is found.」（全文見派工內容）。

## 1. 狀態

| 項目 | 內容 |
| --- | --- |
| 現況 | V2 Outcome Contract 已接受；OC §8 前提 #1–#3（接受紀錄、b3 生效、b2 dry-run）已滿足（OC §9 前置證據列）。本次只做 Delta Spec derivation。 |
| 效力 | SPEC-V2 v2.0 自本紀錄初版寫入起為有效 derived contract（治理 §1.2：不需 acceptor 逐份核准）；v2.1 自本紀錄 §14 的修訂列寫入起取代 v2.0（§5.3 第 2 類修訂）；v2.2 自 §14 的 v2.2 修訂列寫入起取代 v2.1（同類）。 |
| 重新 derive 條件 | V2 OC normative §1–8 的 scope、requirement、架構、acceptance boundary 或 authority／authorization 條款變更時；由 DA 重新 derive 或以本紀錄修訂確認未受影響。 |
| 未做 | 未修改 V1 Spec、V1 OC、V1 derivation record、任何 decision record、OC-V2、BRIEF-V2、`CONTEXT.md`、README、實作、測試；未建 Ticket；未啟動 run；未 commit（派工者依 SA-1 處理）。 |
| 下一步 | Ticket derivation（DA，另行派工；記入本紀錄新章節）→ Orchestrator activation（acceptor 開主 session）。 |

## 2. 依據的 Outcome Contract 條款 → Delta Spec 對應（traceability）

| OC 條款 | 用途 | 對應 SPEC-V2 |
| --- | --- | --- |
| §1 Intent and outcome | Problem Statement／Solution；map-first；兩種語義分開；ENHANCED 不冒充老師要求 | Problem Statement、Solution、INV-V2-5、INV-V2-9 |
| §2.1 Inherited V1 baseline；不得改變的 V1 產物 | 第 1 節繼承規則；INV-V2-8；第 6.3 節定向重驗 | §1.1、INV-V2-8、AC-V2-20 |
| §2.2 Scope classes（V2 Core、V2 Radar、Later） | 全部 R 的 class；第 8 節 | §2 全部、§8 |
| §2.3 Non-scope | 第 8 節；R-V2-OBS-10(d)（年齡不是 stale）；R-V2-OBS-11（伺服器不回帶資料 stale，與「不要求持久狀態」一致）；INV-V2-5（無聚合） | §8、OBS-10、OBS-11、INV-V2-5 |
| §2.4 受影響 V1 條款表（14 列） | 第 1.2 節 Δ-1～Δ-14 逐列對應，效果用語一致 | §1.2 |
| §2.5 S-1 Latest Observation 保證 | OBS-1、4、7、8、9、10；INV-V2-6 | §2.2 |
| §2.5 S-2 資料規則 | OBS-2、5、6、8 | §2.2 |
| §2.5 S-3 模式 | MODE-1～5 | §2.1 |
| §2.5 S-4 下鑽 | DD-1～3、5、6、8、10 | §2.3 |
| §2.5 S-5 測站詳情 | DD-7、OBS-3 | §2.3 |
| §2.5 S-6 失敗語義 | OBS-10～13、SEC-7 | §2.2 |
| §2.5 S-7 獨立降級 | DEG-1～5、INV-V2-7 | §2.5 |
| §2.5 S-8 圍欄 | MAP-1～4；§5.3 儀器 | §2.6 |
| §2.5 S-9 手機資訊面 | RSP-5 | §2.6 |
| §2.5 S-10 其他 outcome | RSP-1～4、6、7；DD-9；MAP-5 | §2.6、§2.3 |
| §2.5 S-11 Radar | RAD-1～6、DEG-4 | §2.7 |
| §2.6 C-1 伺服器端 CWA、瀏覽器邊界 | SEC-1～3、7；INV-V2-1～3 | §2.4 |
| §2.6 C-2 最小架構、正規化 | OBS-3、ENV-1、§5.1 技術棧 | §2.2、§2.9 |
| §2.6 C-3 金鑰位置（b3） | SEC-3；INV-V2-2 | §2.4 |
| §2.6 C-4 兩種語義；CWA 授權標示為文件 constraint | MODE-6、DOC-2、DOC-5；INV-V2-5 | §2.1、§2.8 |
| §2.6 C-5 Reserved boundaries | §8「不由 Agent 執行」；§9 前置 | §8、§9 |
| §3 AB-V2-1～13 | 每條 ≥ 1 條 AC-V2；§7 對應矩陣 | §3、§7 |
| §4 A-1～A-4 | SEC-3（A-1 b3、A-2）、SEC-6（A-3）、TC-3（A-4） | §2.4、§2.9 |
| §5 外部事實與風險 | OBS-1、RAD-1 的資料集事實；§9 已知風險；ENV-2 | §2.2、§2.7、§2.9、§9 |
| §6 Assurance path | §6 Verification Strategy；本紀錄 §6 高風險 | §6 |
| §8 Activation preconditions | §9 前置（只剩部署階段的金鑰與主 session） | §9 |

## 3. Boundary determination 與 DA 裁決（治理 §1.2、§3.6-A、§5.3 第 2 類）

**總判定：SPEC-V2 v2.2（含 v2.0 初版、v2.1 與 v2.2 修正）全部內容在 V2 Outcome Contract（candidate `69c5a04`）的 boundary 內；沒有任何 R／AC／INV 超出 §2.2 的 scope classes、§2.3 non-scope、§2.5 語義、§2.6 constraints 或 §3 acceptance boundary；沒有改變 accepted 語義；沒有重開任何 Grill 裁決（D-1～D-19、P-1～P-36）；沒有改變 V1 Spec v1.1、V1 OC 或任何 decision record 的文字；第 1.2 節 Δ 表與 OC §2.4 逐列一致，未對 §2.4 未列的 V1 條款作任何重新解讀。** 逐項依據如下（只列需要判斷者；逐字轉錄 OC 的項目不列）。

### 3.1 Boundary items（B）

| # | 項目 | 判定 | 依據 |
| --- | --- | --- | --- |
| B-1 | 單一 Delta Spec、V1 以參照繼承 | 在 boundary 內；OC §6「derive V2 Delta Spec（以參照繼承 V1 Spec v1.1，不重寫 V1；逐條列出 re-scope／supersede／extend 的 V1 條款）」。 | OC §6；DV-1 |
| B-2 | 觀測／雷達 `/api/` 路徑與欄位名交給實作、只凍結語義欄位與四個失敗代碼 | 在 boundary 內；OC §3 開頭「證據類別不指定框架、檔名、fixture、mock、票務或順序」；C-1「模組結構屬 HOW」；V1 DR-1 的凍結判準（可觀察驗收條件或跨 Ticket 依賴才凍結）。四個代碼字串是 AB-V2-4「四類…各自可辨」的 oracle，屬跨 Ticket 依賴（前端與 API 測試共用）。 | OC §3、C-1；DR-1；DV-6 |
| B-3 | 重用視窗上限 10 分鐘／5 分鐘、有界時間儀器 30 秒 | 在 boundary 內；OC S-1「長度屬 Spec／HOW」、S-6「界值由 DA 於 Delta Spec 決定，如客觀驗收需要」——DA 決定需要上限與儀器才能客觀驗收「bounded staleness」與「有界時間」；實際長度仍 HOW。 | S-1、S-6；DV-5、DV-7 |
| B-4 | 圍欄三項轉為產品語義＋儀器（E 與逐軸包含、本島 ≥ 25% 視窗高、1 km ≥ 20 px、375 px ≥ 5 km、minZoom 6／maxZoom 12） | 在 boundary 內；OC S-8「minZoom／maxZoom／bounds／margin／viscosity 為 HOW／驗證參數」；派工指示允許 DA 選定具體 Leaflet 數值作為驗證儀器並與產品語義區分。Spec §5.3 明確標示儀器可改、語義不可。**v2.1 修正**：v2.0 的下限條款曾要求「E 全部同時在視窗內」，acceptor 指出此強於 S-8／D-14 的接受語義（等於重新引入未被選擇的 Q14-C 行為）——DA 同意並移除；v2.0 的 pan oracle「視窗 ∩ E ≠ ∅」不足以證明「不得離開有用範圍造成空白主導」——改為中心在 E 內＋逐軸包含（DV-11）。修正後的三項語義只重述 S-8 的四個接受要點，不新增產品需求。 | S-8；DV-11 |
| B-5 | 圍欄外測站（東沙、南沙等）不上圖但列於清單 | 在 boundary 內；S-4「縣下鑽後該縣測站皆可到達」與 S-8「pan 不得離開有用的臺灣範圍」同時成立的唯一方式；不新增功能、不排除任何有效測站（仍計數、可列、可看詳情）。 | S-4、S-8、S-10；DV-10 |
| B-6 | dataset-level Observation Time ＝ 有效測站 `ObsTime` 最大值 | 在 boundary 內；S-2 的「較舊 Observation Time 不得取代較新」需要一個可比較的 dataset-level 值，OC 未定義；DA 在 §3.6-A 第二種情形（多種解讀，選擇只影響本 work item）選定最大值；測站層級 Observation Time 依 S-5 另顯示。 | S-1、S-2、S-5；DV-2 |
| B-7 | 伺服器只回成功（含重用）或分類失敗，不回「帶資料的 stale」 | 在 boundary 內；S-6 把 Stale 定義為「介面仍顯示上一次成功資料」，OC §2.3「契約不要求持久伺服器狀態」；把 stale 固定為介面狀態使四類失敗與 Stale 語義單一來源、且在 Vercel 多實例下可成立。這是設計選擇，不縮減任何 accepted outcome（使用者可見行為完全依 S-6）。 | S-6；OC §2.3、C-2；DV-5 |
| B-8 | 代表測站規則只寫性質（確定性、只依有效站、有文件、可離線驗證、不列 StationId） | 在 boundary 內；S-4 原文；驗證接縫（若在瀏覽器端實作須有等價自動化證據）是 AB-V2-6「規則的自動化驗證」的必要條件。 | S-4；AB-V2-6；DV-9 |
| B-9 | 模式切換保留脈絡的精確規則（Forecast 進入時最小調整以滿足 AC-17；返回恢復） | 在 boundary 內；S-3「切換保留使用者目前地理脈絡（除非某模式確實需要不同的有效視野）」＋ V1 AC-17 的六標記可見；DA 只把「除非」具體化為 AC-17。 | S-3；AC-17；DV-8 |
| B-10 | Radar 預設隱藏、顯示時才取得、重新取得的觸發方式為 HOW（使用者動作、不輪詢）、只在 Now mode | 在 boundary 內；S-11 未定預設；DA 依 §3.6-A 選擇對首次載入最輕的預設；Radar 歸屬 Now mode 來自 OC §1／BRIEF §1 樹狀圖與 C-4（觀測脈絡不流入 Forecast）。**v2.1 修正**：v2.0 曾規定「Refresh 在 Radar 顯示中 MUST 一併重新取得雷達」；acceptor 指出 OC 未定義此耦合——DA 同意：S-11 只要求顯示／隱藏、時間戳、對齊、`/api/` 代理、獨立狀態，重新取得的時機是 HOW；DA 不認為共用 Refresh 是實質必要的產品行為（顯示／隱藏控制本身已提供使用者觸發的重新取得路徑，獨立狀態不受影響），故不需 acceptor 決定。 | S-11；OC §1、§2.3；C-4；DV-12 |
| B-11 | Radar 對齊 oracle ≤ 1 km | 在 boundary 內；S-11「不預先接受實質偏移為已知限制…細微邊緣差異可記錄，明顯錯位不可」＋派工指示「若有意義的對齊需要具體 oracle，定義它而不預先固定重投影實作」。1 km 的選定依據見 DV-13；重投影技術與 CRS 仍 HOW。 | S-11；DV-13 |
| B-12 | 文字錨點（`Now`、`Forecast`、`Latest Observation`、`Observation Time`、`Fetched Time`、`Refresh`、`Back to Taiwan`） | 在 boundary 內；這些是 OC／BRIEF §9 的 accepted 用語與 S-4 的控制名稱；固定為逐字錨點只是讓「明顯有標籤」「永遠可見」可客觀驗收；其餘描述文字仍 HOW。不是新增老師要求（H-2 不擴張）。 | S-1、S-3、S-4；BRIEF §9；DV-14 |
| B-13 | 靜態檢查 re-scope 的檔案集合＝`app.py`、`weather_query.py` 及其單元內 import closure；預報 endpoint 以封網無金鑰行為測試 | 在 boundary 內；OC §2.4 列 2「`app.py`、共用預報查詢模組與預報讀取路徑維持無 HTTP client、無 CWA 字串…靜態檢查依此 re-scope，不弱化；不要求特定模組結構」。「預報讀取路徑」在不固定模組結構下只能以行為（封網無金鑰仍正常）驗證，故 SEC-2(c)。 | OC §2.4 列 2、D-17(6)；DV-15 |
| B-14 | CWA 授權標示：README MUST、應用內 SHOULD | 在 boundary 內；C-4「這是外部授權／法遵的文件 constraint…不是新的產品功能；標示的實際呈現位置屬 HOW」——MUST 只放文件；應用內 SHOULD 是 DA 對法遵風險的預設偏好，可偏離並記理由，不是新功能。 | C-4；DV-16 |
| B-15 | DR-19 的 delta：頁面層級 error → 預報區段層級；預報失敗時進入 Forecast mode 顯示 inline error | 在 boundary 內；OC §2.4 列 7 明列 delta 內容；DA 只把「不得停用健康的 Now mode」在既有 DR-19 條件→狀態規則上具體化（規則本身不變，只縮小遮蔽範圍）。 | OC §2.4 列 7；DR-19；DV-17 |
| B-16 | Now mode 的 `Fetched Time` 標籤須與 DR-17 的預報快照取得時間標籤可辨 | 在 boundary 內；C-4「兩種語義分開」的直接後果；**不改變 DR-17**（DR-17 的值、標籤語義、位置皆不變），只約束 V2 新增的標籤。本項是 OC §2.4 未列 V1 條款的**一致性約束**而非重新解讀，特此記錄以免被誤讀為對 DR-17 的 delta。 | C-4；DR-17（不變）；DV-18 |
| B-17 | 金鑰環境變數名 `CWA_API_KEY`、本機來源為未追蹤 `.env`、部署來源為 Vercel 環境變數 | 在 boundary 內；C-3、A-1、A-2、b3 RB-3；變數名沿用 V1 `.env.example`（既有事實），不新增憑證。載入機制 HOW。 | C-3；b3；DV-19 |
| B-18 | 有效測站定義含「`CountyName` ∈ 22 縣」與（v2.2）「有 CWA 發布且可解析的 `ObsTime`」 | 在 boundary 內；S-2 只寫氣溫與座標；縣歸屬是 S-4 下鑽與代表測站規則的必要前提（無縣就無法分組）；可解析的 `ObsTime` 是 S-1「Observation Time 永遠可見」、S-5「測站詳情含 Observation Time」與 DV-2 最大值計算的必要前提——沒有觀測時刻的紀錄不可能是 Latest Observation 的測站；BRIEF §3.2 事實：樣本全部有 CountyName 與 `ObsTime`。不排除任何可用的資料；不引入正規化（值如發布）。 | S-1、S-2、S-4、S-5；DV-3 |
| B-19 | Taiwan-wide 面板的全臺最高／最低測站為 MAY | 在 boundary 內；S-4 原文「面板**可**顯示」；AB-V2-6 的必要內容是 County 脈絡，不含全臺極值。DA 不把 MAY 升為 MUST（避免 scope leakage）。 | S-4；AB-V2-6 |
| B-20 | UI／UX 附錄 A 未轉為需求 | 在 boundary 內；OC 未接受附錄 A 為契約；Spec 只 derive 可觀察 outcome（S-9、S-10），把 segmented control、面板位置、sheet 高度、snap、顏色、動畫、透明度滑桿（MAY）、斷點實作全部列為 HOW。 | 派工指示「UI/UX advisory boundary」 |
| B-21 | OPTIONAL／Later 不 derive；速率限制列為 Later | 在 boundary 內；OC §2.2 Later 列；速率限制未被接受，ENV-2 只記述風險與契約內節制。 | OC §2.2、§5 |
| B-22 | V2 驗收文件另檔、V1 `ACCEPTANCE.md` 不改寫 | 在 boundary 內；AB-V2-12「`doc/acceptance/` 逐條對應 V2 AC」；檔名 HOW；不回溯改寫 V1 evidence（OC §2.1、AB-V2-11）。 | AB-V2-11、12 |

**未在 boundary 內而未 derive 的事項**：無。**需要 contract change 的事項**：無。**發現的 OC 內部矛盾**：無使 Spec 無法 derive 者。兩處張力已在不改變語義下解決：(i) S-4「面板可顯示」與 AB-V2-6 的必要內容（B-19，MAY 維持）；(ii) S-8「初始視野即最寬視野不是需求」與 MAP-2 下限（兩者相容：初始視野是本島＋澎湖，下限另定）。

### 3.2 DA 裁決（DV-1～DV-19；治理 §3.6-A、§5.3 第 2 類：皆不改變 accepted 語義，不需 acceptor）

每條記：問題、裁決、依據、受影響條款。

- **DV-1 Delta-Spec 模型與優先順序**。問題：如何在不改寫 V1 的前提下讓兩份 Spec 共同構成契約。裁決：SPEC-V2 §1.1 六條繼承規則；只有 §1.2 Δ 表明列的範圍以 V2 為準；未列的 V1 條款不得被 V2 隱性重新解讀；Spec Integration Audit 同時核 V1 INV 與 INV-V2。依據：OC §6、§2.4 末段。影響：全檔。
- **DV-2 dataset-level Observation Time**。裁決：＝全部有效測站 `ObsTime` 最大值；測站層級另顯示於詳情；取代規則（DV-4）與 INV-V2-6 以 dataset-level 值比較。依據：B-6。影響：OBS-4、OBS-8、AC-V2-04。v2.2 補充：因 DV-3(e) 只有具可解析 `ObsTime` 的紀錄才是有效測站，缺少或無法解析 `ObsTime` 的紀錄不參與最大值；成功回應（≥ 1 有效測站）下最大值恆有定義，DD-7 的測站 Observation Time 對每個可列的測站恆存在。
- **DV-3 有效測站**（v2.2 修訂）。裁決：非空 StationId ＋ 氣溫可解析為有限數且不在哨兵集合（至少 `X`、`-99`、`-98`、`T`、`990`；可設定、有文件）＋ WGS84 有限座標 ＋ `CountyName` 逐字屬 22 縣 ＋（v2.2 新增 (e)）CWA 發布的 `ObsTime` 存在且可解析為明確觀測時刻（至少日期與時、分；如發布、不正規化；解析方式 HOW；新舊不影響有效性）。名稱不作識別。無效紀錄不進氣溫圖層、代表測站選取、縣統計與 dataset-level Observation Time。依據：S-1、S-2、S-5、P-1、P-15～P-19、BRIEF §3.2（哨兵與欄位事實）；B-18。影響：OBS-2、OBS-4(a)、AC-V2-05(7)(8)、TC-1。v2.2 動機：acceptor 指出 v2.1 的 OBS-2 未要求 `ObsTime`，使 OBS-4 的最大值與 DD-7 的必要欄位可能對某站無定義；本補正是 derived-contract 一致性修正（治理 §5.3 第 2 類），不改變 S-2 的接受語義（S-2 列的是最小規則，S-1 與 S-5 的可見義務已蘊含此條件；實際資料每站皆有 `ObsTime`，不縮減任何可用資料）。
- **DV-4 取代規則**。裁決：回應 dataset-level Observation Time ≥ 顯示者 → 套用（相等亦套用，Fetched Time 更新）；< 顯示者 → 保留並告知已是最新；Fetched Time 相同（重用）→ 同告知；not-newer 不是 Stale（沒有失敗）。依據：S-2「較舊不得取代較新」只禁止較舊；相等時資料可能含遲報測站，套用不違反任何條款；S-6「視窗內 Refresh 可回同一 Fetched Time 並告知已是最新」。影響：OBS-7、OBS-8、AC-V2-06、INV-V2-6。
- **DV-5 重用視窗上限與伺服器回應形態**。裁決：觀測 ≤ 10 分鐘、雷達 ≤ 5 分鐘（契約上限；長度 HOW，MAY 0）；伺服器只重用成功；伺服器不回「帶資料的 stale」，Stale 為介面狀態。依據：S-1「短暫」＋逐時節奏（10 分鐘 ≤ 節奏的 1/6，且 CWA 建議同資料集重查間隔 ≥ 10 秒、額度 20,000／日皆遠寬鬆）；雷達節奏 10 分鐘故上限取其一半；B-3、B-7。影響：OBS-9、OBS-11、RAD-2、AC-V2-06、AC-V2-18。
- **DV-6 四個失敗代碼**。裁決：`key_not_configured`、`upstream_unreachable`、`upstream_error`、`invalid_response`；非 2xx JSON 含 `reason` 與 `error`；零有效測站歸 `invalid_response`；`upstream_error` MAY 附上游 HTTP 狀態碼數字（非機密）。依據：S-6 四類；B-2。影響：OBS-11、RAD-2、AC-V2-07。
- **DV-7 有界時間**。裁決：產品語義＝每次 Refresh 到達終態、上游逾時存在且小於平台 function 上限、平台層錯誤仍依 failure 處理；驗證儀器＝30 秒（V1 smoke 的 90 秒是暖機預算，不適用單次互動；30 秒足以涵蓋冷啟動＋一次 ~1.4 MB 上游取得＋逾時）。依據：S-6、P-25；B-3。影響：OBS-13、AC-V2-06(e)(f)。
- **DV-8 模式切換保留脈絡**。裁決：Now 狀態往返恢復；進入 Forecast 時已顯示六標記則保留視野，否則最小調整（AC-17 是「模式確實需要不同視野」的唯一情形）；返回 Now 恢復離開時視野。依據：B-9。影響：MODE-5、AC-V2-01。
- **DV-9 代表測站規則**。裁決：只寫性質（確定性、只依有效站與有文件靜態偏好、後備、README 可手算、可離線驗證、不列 StationId 為契約）；若在瀏覽器端實作，須有等價自動化證據（瀏覽器自動化或靜態守衛；工具 HOW）。依據：B-8。影響：DD-3、AC-V2-11、TC-1。
- **DV-10 圍欄外測站**。裁決：不上圖、仍計數、列於清單並標示、可看詳情；README 記述。依據：B-5；DA 核對 CWA 測站事實（高雄市所轄東沙、南沙測站位於 lat 20.7N／10.4N，遠在任何「有用的臺灣範圍」之外）。影響：DD-5、DD-6、DD-11、AC-V2-12。
- **DV-11 圍欄三項的產品語義與儀器**（v2.1 修訂；v2.0 版本見下方「未採用的解讀」）。裁決：(pan) 任何可到達的視野，視窗中心在 E 內，且每一軸上視窗 ⊆ E 或（視窗大於 E 的軸）E ⊆ 視窗；金門、連江可藉拖曳／縮放到達並選取測站；(zoom-out) 下限存在；下限時本島南北 ≥ 25% 視窗高、圍欄判準仍成立；**不要求** E 或 22 縣市同時在視窗內；(zoom-in) 上限存在、1 km ≥ 20 CSS px、375 px 視窗 ≥ 5 km、臺北市測站可個別選取；儀器：E ＝ lon 117.6–122.9／lat 21.2–26.7，`maxBounds` ＝ E，minZoom 6，maxZoom 12（12–13 可接受），初始 fitBounds 本島＋澎湖。依據：B-4；S-8 的四個接受要點（zoom-out 在臺灣小到無用或空白主導前停止；金門連江可達；初始視野本島＋澎湖；初始視野不必是最寬）逐一對應，沒有第五項；pan oracle 選「中心＋逐軸包含」是因為它排除了「視窗 ∩ E ≠ ∅」仍允許的空白主導視野（例如視窗只在角落碰到 E），且 vendored Leaflet 1.9.4 的 `maxBounds` 逐軸行為（`_getBoundsOffset`／`_rebound`：視窗小於界 → 限制在界內；視窗大於界 → 界置中）恰好同時滿足 (i)(ii)，使儀器與語義可直接對照；DA 以 Web Mercator 公式計算（scratchpad）：z6 時本島南北 174 px（1280×560 視窗 31%、375×360 視窗 48%；z5 為 15% FAIL；z7 亦 PASS）；z12 時 1 km ≈ 24 px、375 px ≈ 16 km（z11 12 px FAIL；z14 4 km FAIL）；z10 時桌機視窗寬 ≈ 1.76°、375 px ≈ 0.52°，均小於 E 寬 5.3°，故可在圍欄內平移到金門（118.24–118.5E）與連江（119.9–120.5E、25.9–26.4N）。影響：MAP-1～4、§5.3、AC-V2-13。
- **DV-12 Radar 預設與觸發**（v2.1 修訂）。裁決：預設隱藏；顯示時取得；顯示中重新取得最新影像的觸發方式屬 HOW（例如再次切換顯示或由 Refresh 一併觸發），限使用者動作、不自動更新或輪詢（OC §2.3）、維持 RAD-4 的獨立狀態與時間戳語義、README 記載；只在 Now mode。v2.0 的「Refresh MUST 一併重新取得雷達」已移除（OC 未定義此耦合；不是 S-11 的接受語義）。依據：B-10。影響：RAD-3、MODE-4、DOC-1(9)、AC-V2-18、AC-V2-21(10)。
- **DV-13 Radar 對齊 oracle**。裁決：每個影像像素與地圖對其經緯度的投影相距 ≤ 1 km；參考點＝產品範圍四角、四邊中點、中心＋本島內 ≥ 3 點；zoom 7 與 10；自動化可重現。依據：產品像素 ≈ 185 m（6°／3600 px），縣層級使用；DA 計算把等經緯度影像線性貼在 Mercator lat 20.5–26.5 的最大誤差 ≈ 3.8 km（lat 23.55 附近；lat 22.0 為 2.8 km、25.0 為 2.9 km），即預設 `L.imageOverlay` 作法 FAIL——這正是 S-11 所稱「實質偏移／重投影問題」，故 oracle 必須排除它；1 km 是 5 個原生像素、在 zoom 10 約 2.8 CSS px，可量測且對縣層級脈絡無明顯錯位。重投影技術或地圖 CRS 仍 HOW。影響：RAD-5、AC-V2-19。
  **DV-13 補充（v2.1，acceptor 要求的比例性複核；oracle 保留為 ≤ 1 km）**。問題：1 km 是否對「有意義的地理對齊」過嚴，因為它迫使實作做重投影／CRS 工作（線性貼圖已知偏差約 3.8 km）。DA 複核：(1) **工作量由接受語義決定，不由數字決定**——S-11 明文「不預先接受實質偏移為已知限制…明顯錯位不可」並把系統性偏移／重投影問題列為 route DA 的事項，所以「不能用線性貼圖」是 acceptor 已接受的結果；任何 < 3.8 km 的容差都同樣迫使處理緯度非線性，任何 ≥ 3.8 km 的容差都等於預先接受實質偏移（在 zoom 10 為 ≈ 10.6 CSS px、zoom 12 為 ≈ 43 px 的可見錯位），違反 S-11。(2) **1 km 對正確處理不構成額外負擔**——逐列重採樣或改用等經緯度 CRS 的殘差在一個原生像素（≈ 185 m）量級；分段線性近似的殘差（DA 重算）：兩段 ≈ 1.02 km（略超出）、三段 ≈ 0.46 km、四段 ≈ 0.26 km，所以 1 km 允許三段以上的簡單近似解法，不強迫逐像素精確方案。(3) **可量測性**——1 km 在 zoom 10 約 2.8 CSS px，瀏覽器量測可分辨；更寬的容差（例如 2 km）不減少任何工作，只會放寬對粗糙近似的把關；更嚴的容差（例如 200 m）在 zoom 10 不足 1 px、無法可靠量測。(4) 與縣層級使用一致：雷達產品像素 185 m，縣內站距通常 1–10 km，1 km 的錯位不會把回波錯置到相鄰縣或相鄰測站。**裁決：保留 ≤ 1 km；不需 acceptor**——改變容差只有兩種方向：放寬到 ≥ 3.8 km 會改變 accepted 產品品質（須 acceptor），放寬到 1–3.8 km 之間不改變工作量也不改變品質保證的性質，故無理由變動。影響：無條款變更；本補充作為 AC-V2-19 的比例性依據。
- **DV-14 文字錨點**。裁決：`Now`、`Forecast`（切換）、`Latest Observation`、`Observation Time`、`Fetched Time`、`Refresh`、`Back to Taiwan` 逐字為驗證錨點；禁止以 `real-time`／`realtime`／`live` 指稱觀測；標題與 V1 概念詞不變。依據：B-12。影響：MODE-2、OBS-4、OBS-7、DD-8、DOC-5、AC-V2-23。
- **DV-15 靜態檢查 re-scope 與預報路徑行為接縫**。裁決：(a′) 集合＝`app.py`、`weather_query.py` 及其單元內 import closure；`server.py`、`api/index.py`、V2 觀測／雷達模組退出但受憑證掃描；(b) 前端檢查延伸至所有請求形式；(c)(d) 不變；新增 (e) 預報 endpoint 封網無金鑰行為不變。依據：B-13；現行 `tests/test_static_checks.py` 的 `_PYTHON_SIDE` 含 `server.py`／`api/index.py`（必須 re-scope 才能容納 V2）。影響：SEC-2、SEC-4、AC-V2-16。
- **DV-16 CWA 授權標示**。裁決：README MUST（兩個資料集）；應用內 SHOULD。依據：B-14。影響：DOC-2、AC-V2-21(6)。
- **DV-17 DR-19 delta 的範圍**。裁決：DR-19 的條件→狀態規則不變；「頁面層級」在 V2 收斂為「預報區段層級」（Forecast mode 內容＋下方 dashboard）；預報失敗時 Now mode 與模式切換維持可用；進入 Forecast mode 時地圖區 inline error（DR-19 per-Region 規則）、`Select Date` 可隱藏或停用；AC-10 對受影響部分仍成立。依據：B-15。影響：DEG-3、AC-V2-09；Δ-7。
- **DV-18 `Fetched Time` 與 DR-17 標籤可辨**。裁決：V2 標籤須與下方 dashboard 的預報快照取得時間在文字與位置上可辨；DR-17 不變。依據：B-16。影響：MODE-6(d)、DOC-5(d)、AC-V2-02。
- **DV-19 金鑰來源**。裁決：只從 `CWA_API_KEY` 環境變數讀；本機來源未追蹤 `.env`（載入 HOW）；部署來源 Vercel 環境變數；缺則 `key_not_configured`。依據：B-17。影響：SEC-3、AC-V2-17。

**未採用的解讀（供追溯）**：伺服器端 stale-with-data（B-7，會使 Stale 有兩個來源）；dataset-level Observation Time 取眾數（不如最大值簡單且同樣確定）；以固定 minZoom 為產品語義（改為儀器）；把 Taiwan-wide 極值升為 MUST（B-19）；把附錄 A 的 segmented control、sheet 高度等寫入需求（B-20）。**v2.0 曾採、v2.1 依 acceptor 指示撤回**：(a) 下限 PASS 條件「E 全部／22 縣市同時在視窗內」（超出 S-8／D-14；等於重新引入未被選擇的 Q14-C 行為）；(b) pan oracle「視窗 ∩ E ≠ ∅」（允許空白主導的視野，證明力不足）；(c) 「Refresh MUST 一併重新取得雷達」（OC 未定義的耦合）；(d) 對新 V2 驗證直接點名 pytest／mock／Flask test client／headless（框架屬 HOW；V1 既有工具只作既有回歸事實命名）。

## 4. Spec 分配到的 acceptance boundary

**V2 Outcome Contract 只有一份 derived Spec（SPEC-V2 v2.2）。分配：AB-V2-1～AB-V2-13 全部，加 §2.6 C-1～C-5 constraints 與 §5 風險的可驗收化。** 全部 derived Specs 合起來涵蓋整個 acceptance boundary 的核對（治理 §4.7 第五 bullet）在本 Spec 的 Spec Integration Audit 執行（它同時是第一份與最後一份）。V1 Spec v1.1 是 V1 Outcome Contract 的 derived Spec，不屬 V2 OC 的 boundary 分配；V2 對 V1 的 delta 由本 Spec §1.2 承載並由同一次 Spec Integration Audit 核對一致性。

| AB-V2 | 分配 | AC-V2 | 備註 |
| --- | --- | --- | --- |
| AB-V2-1 | SPEC-V2 | AC-V2-01、02、23 | 含 V1 AC-17／18 在 Forecast mode 的重驗 |
| AB-V2-2 | SPEC-V2 | AC-V2-03、04、05、23 | 消毒樣本；preview 抽樣需 acceptor 金鑰 |
| AB-V2-3 | SPEC-V2 | AC-V2-05、06 | 含反例與 30 秒儀器 |
| AB-V2-4 | SPEC-V2 | AC-V2-07、08 | H-1（訊息與 log） |
| AB-V2-5 | SPEC-V2 | AC-V2-09 | DR-19 delta |
| AB-V2-6 | SPEC-V2 | AC-V2-10、11、12、23 | H-3（無縣平均、代表站標示） |
| AB-V2-7 | SPEC-V2 | AC-V2-13 | 儀器見 Spec §5.3 |
| AB-V2-8 | SPEC-V2 | AC-V2-12、14、15 | |
| AB-V2-9 | SPEC-V2 | AC-V2-18、19 | 對齊 oracle |
| AB-V2-10 | SPEC-V2 | AC-V2-16、17 | H-1；靜態 re-scope |
| AB-V2-11 | SPEC-V2 | AC-V2-20 | 第 6.3 節定向重驗清單 |
| AB-V2-12 | SPEC-V2 | AC-V2-21 | H-3（標示） |
| AB-V2-13 | SPEC-V2 | AC-V2-22、17(c) | 需 acceptor 填金鑰（A-2） |
| C-1～C-5、§5 風險 | SPEC-V2 | AC-V2-02、06(e)(f)、07、16、17 | 讓 constraints 可驗收，不擴張 boundary |

**為何不拆分**：AB-V2-1／5／8／10／11 橫跨伺服器、前端與文件；INV-V2-1／5／7 是跨層 invariant；拆分會讓它們變成跨 Spec invariant而失去單一 Spec Integration Audit 的核對點。工作量由 Tickets 承擔。

## 5. Implementation-readiness 核對（治理 §3.4）

| 條件 | 狀態 |
| --- | --- |
| 沒有把必要設計留待下游決定 | 會被其他 Ticket 依賴的語義已凍結（Spec §5.1）：模式與預設、資料集、時間表示、文字錨點、有效測站與成功定義、取代規則、四個失敗代碼與回應形態、重用上限、有界時間、22 縣、代表規則性質、詳情欄位、圍欄語義、金鑰模型、靜態檢查集合、health 不變、對齊 oracle、技術棧、文件義務。委派項目（§5.2）都是單一 Ticket 內可自行決定、不被其他 Ticket 依賴的 HOW，或以儀器（§5.3）給出可替換的具體值。 |
| 每條 AC 有可觀察 PASS／FAIL 與證據類別 | AC-V2-01～23 各有 PASS 條件、FAIL 例、證據類別與方法；需要儀器者引用 §5.3。 |
| Invariants 明確 | INV-V2-1～9；V1 INV-1～9 依 Δ 表繼續適用。 |
| Dependencies 可辨識 | 第 13 節的預期分解（非約束）；正式 dependencies 在 Ticket derivation 時定。 |
| Verification contract 不由下游重新定義 | Spec §6 規定各階段誰看什麼；Tickets 只能引用（治理 §3.4）。 |
| Negative／failure behaviour | 每條 A～G 都有反例：無效測站六種、四類失敗、亂序 Refresh、平台層錯誤、預報失敗與 Now 健康、雷達失敗、圍欄外測站、零有效縣、缺金鑰。 |

## 6. 高風險類別判定（治理 §5.1；Bindings §5；OC §6）

**判定：V2 不需要新增高風險類別。H-1、H-2、H-3 繼續適用；其「涵蓋位置／項目」與「觸及的工作」在 V2 的具體含義如下（這是既有類別對 V2 的適用說明，不是類別的新增或修改；`decision-20260923-high-risk-categories.md` 文字不變）。**

| 類別 | V2 的具體適用 | Spec 對應 |
| --- | --- | --- |
| **H-1 憑證與機密** | 授權位置依 Bindings **b3** 為兩個：未追蹤 `home_work_01/.env`、acceptor 填入的 Vercel 專案環境變數（H-1 表「唯一授權位置」一句以 b3 為準；H-1 的「涵蓋位置」原本已含「Vercel 環境變數」作為不得洩漏之處，b3 只授權它作為**存放**位置，不改變「值不得出現在任何可公開位置」的要求）。V2 新增的「觸及的工作」：任何伺服器端 CWA 存取程式、錯誤訊息與 log、`/api/` 回應、消毒樣本、preview 驗證紀錄、README 的金鑰步驟。 | INV-V2-2、SEC-3、5、7、OBS-12、AC-V2-07、17 |
| **H-2 老師指定的介面或資料格式** | V2 不新增老師指定項目；風險是 V2 改動**破壞**既有項目（標題、`Select Region`／`Select Date`、Region 名、`app.py`、`data.db`、DDL）。V2 文字錨點（DV-14）不是老師指定，不納入 H-2。 | INV-V2-8、INV-V2-9、MODE-4、RSP-4、AC-V2-20、23 |
| **H-3 資料語義與標示** | 延伸涵蓋：觀測值與專案推導值的可見分開（C-4）；代表測站值不得標示為縣值；無觀測聚合；Latest Observation 用語；`Fetched Time` 與預報快照取得時間可辨；CWA 授權標示。V1 的推導語義項目不變。 | INV-V2-5、MODE-6、DD-2、DD-5、DOC-2、DOC-5、AC-V2-02、10、21 |

**不新增的候選與理由**：
- *伺服器端 CWA 路徑*：其風險面是憑證（H-1）與標示（H-3），已涵蓋；可用性失敗可觀察、有四類分類與 Stale／Unavailable 語義，不是隱性風險。
- *上游額度／公開 endpoint 濫用*：無付費（CWA 免費，RB-4 不觸發）；耗盡結果可觀察（`upstream_error` → Stale）；契約內節制為重用視窗與逾時；速率限制為 Later。列為 Spec §9 已知風險，不列高風險類別。
- *雷達對齊*：正確性風險以客觀 oracle（AC-V2-19）承接；不是需要 deferral 限制的類別。
- *UI／UX、圍欄*：ENHANCED、手動驗收，與 V1 決定一致不列。

**Assurance 要求（沿用 decision A-1～A-7，對 V2 的具體化）**：
- A-1：觸及 H-1／H-3 的 V2 Ticket，R1 record MUST 有明記核對段（H-1：兩個位置、log、回應、樣本、evidence；H-3：語義分開、代表站標示、無聚合、授權標示）。
- A-2：Spec Integration Audit MUST 逐項核 INV-V2-2（H-1）、INV-V2-5（H-3）、INV-V2-8／V1 INV-4（H-2），並對提交的 `data.db` 重跑 V1 兩句驗證 SQL（證明 V1 產物未變）。
- A-3：高風險類別的 blocking finding，Final Adjudicator 不得單獨 deferred。
- A-5：CI 機械檢查延伸至新程式與樣本路徑（R-V2-SEC-5）。
- A-6：release gate 材料加 preview 觀測驗證紀錄（AC-V2-17(c)、22）。
- A-7／diversity：b2 下 Executor `claude-opus-5-5` 與 Primary Reviewer `claude-opus-5-5` 相同，audit record 記 `diversity_lost`（Bindings §5）。

## 7. 受影響工作

| 工作 | 影響 |
| --- | --- |
| 進行中的 work item | 無（V1 全部結案並合併；#28、#29 結案）。 |
| Tickets | 尚未 derive；預期分解見第 13 節（非約束）。 |
| V1 Spec、V1 OC、V1 derivation record、DR-1～DR-22、phase acceptance | 不修改；依 SPEC-V2 §1.2 以參照適用。 |
| V1 evidence | 沿用；只在 SPEC-V2 §6.3 列出的項目定向重驗。 |
| `CONTEXT.md`、README、`doc/acceptance/` | 由 V2 Tickets 依 R-V2-DOC-1～5 更新（本紀錄不改）。 |
| Bindings | 不需修改；b3 已生效。 |
| 既有測試 | `tests/test_static_checks.py` 的 `_PYTHON_SIDE`／`_import_targets` 檢查須依 DV-15 re-scope（只加不減）；其餘 V1 測試預期不變。 |
| Workflows | 預期不需修改；A-4 窄授權存在備用。 |

## 8. 需要其他 authority 的事項

| # | 事項 | Authority | 理由 |
| --- | --- | --- | --- |
| 1 | 部署階段在 Vercel 專案填入 `CWA_API_KEY`（preview 與 production 環境） | acceptor | A-2；RB-3（b3）；AC-V2-17(c)、22 的前提，不是 activation 前提 |
| 2 | 開符合 `orchestrator` mapping 的主 session 啟動 Formal run（Ticket derivation 之後） | acceptor | Bindings §3.3 |
| 3 | 合併（RB-1）、繳交（RB-2） | acceptor | release |

以上皆非 contract change；V2 Outcome Contract 的 accepted 語義不變。**本次 derivation 沒有需要 STOP 並回報的未決事項**（見第 11 節）。

## 9. Self-review（DA consistency pass；派工指示的十一項）

| # | 檢查 | 結果 | 說明 |
| --- | --- | --- | --- |
| 1 | Outcome Contract coverage | PASS | AB-V2-1～13 每條 ≥ 1 AC（§4 表）；S-1～S-11、C-1～C-5 每條 ≥ 1 R（§2 表）；OC §2.4 十四列 ↔ Δ-1～Δ-14 逐列；A-1～A-4 ↔ SEC-3、SEC-6、TC-3。 |
| 2 | Missing negative／failure behaviour | PASS | 無效測站八種（AC-V2-05；v2.2 加入缺少／無法解析 `ObsTime` 及其對 dataset-level Observation Time 的影響）、四類失敗（07）、首次載入 vs 失敗 Refresh（08）、亂序／連按（06(d)）、上游停滯與平台層錯誤（06(e)(f)）、預報失敗與 Now 健康（09）、雷達失敗（18）、零有效縣（DD-5）、圍欄外測站（DD-11）、缺金鑰（17(d)）、年齡不觸發 stale（08(d)）。 |
| 3 | Unverifiable AC | PASS | 「有意義」「有用」「明顯」皆轉為儀器或錨點（§5.3、DV-11、13、14）；「不得使地圖不可用」以可拖曳／縮放／選取的具體檢查表達。v2.1：pan 圍欄的 oracle 由「視窗 ∩ E ≠ ∅」（證明力不足）改為「中心在 E 內＋逐軸包含」，可由視窗 bounds 讀數客觀判定。殘留主觀項只剩 SHOULD（視覺抽驗、應用內標示）。 |
| 4 | Verification mismatch | PASS | 客戶端規則（取代規則、代表選取若在前端）要求瀏覽器自動化或靜態守衛的等價證據，不以 API 測試冒充；對齊以量測不以截圖；預報路徑 CWA-free 以封網行為測試而非只看 import；preview 驗證由 Reviewer 重現。v2.1：AC 證據欄與 §6.1 對新 V2 驗證只寫證據類別（離線自動化、API 驗證、靜態檢查、瀏覽器驗收／自動化、量測），V1 既有 pytest／Flask test client／靜態守衛只以既有回歸事實命名；每條 AC 的 PASS／FAIL oracle 文字未變（AC-V2-13 除外，其 oracle 依項目 1、2 修正）。 |
| 5 | Scope leakage | PASS | 速率限制、Taiwan-wide 極值（MAY）、透明度滑桿（MAY）、應用內授權標示（SHOULD）、年齡提示（MAY）、自動更新皆未升為 MUST；無新增 CWA 資料集；縣互動圖層與圍欄外規則皆為既有 outcome 的必要條件。v2.1 複核：移除了兩處 v2.0 的 leakage——下限「E 全部同時在視窗內」（超出 S-8）與「Refresh MUST 重取雷達」（超出 S-11）；修正後 MAP-1～4 只承載 S-8 的四個接受要點，RAD-3 只承載 S-11 的五個接受要點；未新增任何 MUST。 |
| 6 | Hidden HOW | PASS | 端點路徑／欄位名、模組結構、快取、逾時值、Leaflet 常數、資訊面實作、Radar 變體與重投影、測試框架皆列 §5.2；凍結者（§5.1）各有跨 Ticket 依賴或可觀察驗收理由（DR-1 判準）。四個失敗代碼字串與文字錨點是刻意凍結（B-2、B-12）。v2.1 複核：雷達重新取得時機回歸 HOW；`minZoom` 6／`maxBounds` ＝ E 明確標示為儀器且 §5.3 說明儀器不創造需求；pytest／mock／headless 不再出現在新 V2 驗證的規範句中。 |
| 7 | Contradiction with V1 | PASS | 每條與 V1 不同的規定都在 Δ 表且與 OC §2.4 一致；DR-17、DR-19 的處理方式（DV-17、DV-18）明確標示不變／delta 範圍；AC-17「初始視野」在 Forecast mode 進入時解讀（Δ-5）；V1 INV-1～9 與 INV-V2 無互斥（INV-6 以 re-scope 形式由 INV-V2-1 承接）。 |
| 8 | Missing traceability | PASS | 每條 R 有「對應」欄（OC／AB／V1／DV）；每條 AC 有 AB 與 R；每條 DV 有 B-item 依據；Δ 表引 OC §2.4 列號與 Grill D／P。 |
| 9 | Disproportionate evidence burden | PASS | §6.2 截圖集合限於新行為與關鍵失敗態；V1 evidence 沿用、只定向重驗 §6.3；Radar 影像不要求真實 fixture；瀏覽器自動化只在需要時；不重做整套 V1。 |
| 10 | UI advisory → contract | PASS | 附錄 A 的 segmented control、面板位置、sheet 高度／snap、顏色、動畫、透明度、斷點實作皆為 HOW；只保留 OC 已接受的 outcome（S-9、S-10）。「用 button 不用 div」轉為「可鍵盤操作」outcome。 |
| 11 | Accidental reopening of V1 | PASS | 未改 V1 任何文字；未重開 D2、A1–A4、DR-20 核定 HOW、#28／#29 結論；Forecast mode 原樣；`data.db`、Grading App、預報 `/api/` 不變（INV-V2-8 以 blob／diff 證明）。 |

補充檢查（DA 以腳本核對）：兩檔未把 V2 稱為 MVM（「MVM」只用於 Part A 評分基線，SPEC-V2 §0 只重申 OC 的禁用句）；兩檔不含任何金鑰格式字串；AC-V2-01～23 與 73 條 R-V2 的定義與引用雙向一致；DV 編號與 SPEC-V2 引用一致（DV-2～DV-13 於 Spec 條款內引用；DV-1、DV-14～DV-19 由本紀錄承載並各自對應到 Spec 條款）；兩檔全部表格列的欄數與表頭一致。

**v2.2 聚焦複核（acceptor 指示的六項）**：(1) 有效測站定義 vs Observation Time——PASS：OBS-2(e) 使每個有效測站具可解析 `ObsTime`，OBS-4(a) 的最大值與 DD-7 的必要欄位對有效測站恆有定義，三者不再可能互相矛盾；(2) 缺少／無法解析 `ObsTime` 的負向行為——PASS：AC-V2-05(7)(8) 以衍生樣本客觀驗證排除範圍（圖層、代表選取、縣統計、最大值）與最大值落到其餘有效站；TC-1 涵蓋；(3) scope leakage——PASS：未新增產品功能或正規化方案，只把 S-1／S-5 已蘊含的前提寫成一致的定義；(4) hidden HOW——PASS：解析方式明示為 HOW，值「如發布」，未指定格式或函式庫；(5) traceability——PASS：OBS-2 的對應欄加 S-1、S-5，DV-3／B-18 記載依據與動機，§10／§14 記錄版本；(6) verification mismatch——PASS：反例以離線自動化對衍生樣本判定，與需求的可觀察結果一一對應，未以存在性檢查冒充正確性。

## 10. Evidence（DA 自行執行，全部唯讀；未印出任何金鑰）

- 讀取：Bindings b3 全文；治理 v2.0 全文（§1–§5 與附錄）；`binding-verification.md`（grep）；OC-V2 全文；BRIEF-V2 全文；V1 OC 全文；V1 Spec v1.1 全文；`derivation-SPEC.md` 全文；DR-1～DR-16、H-1～H-3、DR-17、DR-19、DR-20、DR-21、DR-22 全文；兩份 phase 增補全文；`phase-acceptance-SPEC.md` 標題與 §10；`ACCEPTANCE.md` 全文；`CONTEXT.md` 全文；`tickets.md` 全文；`REQUIREMENTS.md` Part B §B.1–B.5、§B.16、§B.22、§B.24；SDD 指引 §8–§9；實作檔（第 0 節清單）。
- Git（read-only）：`main` HEAD ＝ `8c4667d4d20fd82718d6acb4a29392cc5679b516`；`git log --oneline -5 main` 含 PR #33／#32／#31 merges 與 `f853bcb`；`git merge-base --is-ancestor ef15d3e main` → true；`ef15d3e` ＝「HW10 Taiwan Weather Forecast (home_work_01): ingestion, Grading App, Dashboard/Vercel, map rework and acquisition-time validation」；`git status --porcelain` 只有未追蹤 `grep.exe.stackdump`（工具殘留，非本紀錄產物）；`main` 追蹤 `home_work_01/` 166 檔，含 `data/raw/F-D0047-091.json`、`.meta.json`、`tests/fixtures/F-D0047-091_sample.json`。
- 實作事實：`server.py` 無 HTTP client、無環境變數；`api/index.py` 單一 function；`vercel.json` 全路由；`tests/test_static_checks.py` 的 `_PYTHON_SIDE` ＝ `app.py`、`weather_query.py`、`server.py`、`api/index.py`（須 re-scope）；`_ALLOWED_FRONTEND_URLS` 四個非請求常數；`app.js` 以 `center [23.75,121.0]`／`zoom 7` 初始化、`fitToMarkers` 為唯一 `fitBounds`（`maxZoom: 8`）、無 `minZoom`／`maxZoom`／`maxBounds`；`styles.css` 地圖高度 560／440（≤ 1023）；`basemap.js` 檔頭聲明純幾何無屬性；`smoke.py` 只檢 `GET /` 與 `/api/health`；兩個 workflow 以 `home_work_01/**` 觸發。
- 計算（scratchpad `geo.py`，Web Mercator 公式）：等經緯度影像線性貼圖於 lat 20.5–26.5 的最大緯度誤差 3.80 km（lat 23.55）；lat 22.0／23.5／24.5／25.0 分別 2.80／3.80／3.42／2.90 km；產品像素 0.0017° ≈ 185 m。z5／6／7／8 時 E（117.6–122.9／21.2–26.7）為 121×137／241×274／482×548／965×1096 px（v2.1 起只作圍欄儀器的參考，不再是下限 PASS 條件）；本島（120.03–122.05／21.85–25.35）南北 87／174／348／695 px；本島＋澎湖（119.25 起）寬 64／127／255／510 px。z11／12／13 時 1 km ≈ 12／24／47 px。
- v2.1 複核（read-only）：vendored `static/vendor/leaflet.js`（Leaflet 1.9.4）的 `_getBoundsOffset`／`_rebound`：`0<t+e ? Math.round(t-e)/2 : Math.max(0,Math.ceil(t))-Math.max(0,Math.floor(e))`——視窗在某軸大於 `maxBounds` 時把界置中，否則把視窗限制在界內；`_panInsideMaxBounds` 於移動時強制。此為 §5.3 MAP-1 儀器說明的依據。分段線性近似殘差由同一 Mercator 公式對等分區間重算（scratchpad）：一段 3.803 km、兩段 1.019 km、三段 0.463 km、四段 0.263 km、八段 0.067 km。`git diff --stat HEAD` 於修正前為空（工作樹與 `dae3ab0` 一致）。
- v2.2 複核（read-only）：`git rev-parse HEAD` ＝ `4efe77739e100da1f6242846a4b5bd38b808a276`；`git status --porcelain` 只有派工者維護的 worklog 修改與 `grep.exe.stackdump`（DA 未觸及）；BRIEF-V2 §3.2 記載 O-A0001-001 每筆紀錄欄位含 `ObsTime`（與 `StationName`、`StationId`、`GeoInfo`、`WeatherElement` 並列），為 OBS-2(e) 的資料事實依據。
- 未讀取 `home_work_01/.env`；未使用 API key；未呼叫 CWA；產出不含任何金鑰字串。

## 11. 未決事項（不阻擋 derivation；皆為實作期或部署期事項）

| # | 事項 | 處理 | Authority |
| --- | --- | --- | --- |
| 1 | Vercel function 執行上限與回應大小是否容納一次 O-A0001-001 取得＋逾時（OC §5 風險） | 實作期驗證；若 §5.3 的 30 秒儀器或裁剪策略需調整而語義不變 → DA 修訂本紀錄；若需改變語義 → route acceptor | DA（實作期） |
| 2 | Radar 透明變體（-005／-006）是否可用；若不可用，去背處理屬 HOW | Executor 決定；無法使非回波區透明時 route DA（RAD-6） | Executor／DA |
| 3 | 公開 endpoint 的額度暴露（速率限制為 Later） | Spec §9 記錄；不在本次範圍；acceptor 日後可另指示 | acceptor（若要） |
| 4 | acceptor 於部署階段填入 Vercel 金鑰（preview 與 production 環境） | 前置 #1；AC-V2-17(c)、22 在此之前記 BLOCKED（不是 FAIL） | acceptor |

沒有需要 STOP 並回報的未決事項：沒有任何未解問題會實質改變產品行為、acceptance、安全或 authority。

## 12. 寫入的檔案

| 檔案 | 動作 |
| --- | --- |
| `home_work_01/doc/spec/SPEC-V2.md` | 新增（v2.0，commit `dae3ab0`）；v2.1 修正（`4efe777`）；v2.2 修正（本次，Edit 局部修改） |
| `home_work_01/doc/governance/decisions/derivation-SPEC-V2.md` | 新增（本檔，`dae3ab0`）；v2.1 修訂（`4efe777`）；v2.2 修訂（本次） |

未 commit；依 SA-1 由派工者處理。未建立 decision record（無新高風險類別，第 6 節）。v2.1、v2.2 未觸及任何其他檔案。

## 13. 預期的 Ticket 分解（非約束；供 Ticket derivation 參考）

| 切片 | 內容 | 主要 AC-V2 | 依賴 |
| --- | --- | --- | --- |
| T-A 伺服器端 Latest Observation 路徑 | 觀測 `/api/`、正規化、有效測站、四類失敗、重用、逾時、log、金鑰讀取、靜態檢查 re-scope、消毒樣本與 API 測試、預報路徑封網測試 | 03、04、05、06（API）、07、16、17(a)(b)(d) | — |
| T-B Now mode 前端基礎 | 兩模式與切換、Latest Observation 顯示、Observation／Fetched Time、Refresh 三種結果、Stale／Unavailable、獨立降級（DR-19 delta）、文字錨點 | 01、02、06（UI）、08、09、23 | T-A |
| T-C 下鑽與代表測站 | 縣互動圖層、代表規則、County 脈絡、測站清單與詳情、Back to Taiwan、鍵盤路徑、圍欄外測站 | 10、11、12 | T-B |
| T-D 圍欄與響應式 | pan／zoom 圍欄、初始視野、底部資訊面、44×44、768 破版、初始化守衛 | 13、14、15 | T-C |
| T-E Radar | 雷達 `/api/`、overlay、顯示／隱藏、時間戳、對齊 oracle、獨立狀態 | 18、19 | T-A、T-B |
| T-F 文件、驗收與部署驗證 | README、`CONTEXT.md`、V2 驗收文件、定向 V1 重驗、preview 驗證（金鑰後）、整合 | 20、21、22、17(c)(e) | 全部 |

## 14. 修訂紀錄

| 版本 | 日期 | 依據 | 變更 | 性質 |
| --- | --- | --- | --- | --- |
| SPEC-V2 v2.0／本紀錄初版 | 2026-09-25 | acceptor 派工「Proceed with V2 DELTA SPEC DERIVATION only」 | 初版 derive。 | 治理 §1.2 derived contract；§5.3 第 2 類 |
| SPEC-V2 v2.1／本紀錄修訂 | 2026-09-25 | acceptor 指示「Perform a focused DA correction pass on SPEC-V2 v2.0 and its derivation record. The accepted V2 Outcome Contract is NOT being changed.」（三項實質修正＋一項 HOW 清理＋一項比例性複核；PR #34 不合併、不 derive Tickets） | (1) R-V2-MAP-2、AC-V2-13(c)、§5.3：移除「E 全部／22 縣市同時在視窗內」的下限 PASS 條件；下限只以本島 ≥ 25% 視窗高＋圍欄判準驗證；`minZoom` 6 保留為儀器。(2) R-V2-MAP-1、AC-V2-13(b)、§5.3：pan oracle 改為「中心在 E 內＋逐軸視窗 ⊆ E 或 E ⊆ 視窗」，金門／連江以截圖證明可達；儀器對照 vendored Leaflet `maxBounds` 行為。(3) R-V2-RAD-3、AC-V2-18、R-V2-DOC-1(9)、AC-V2-21(10)：移除「Refresh MUST 一併重取雷達」；觸發方式為 HOW（使用者動作、不輪詢、狀態獨立、README 記載）。(4) R-V2-TC-1、§6.1、AC-V2-02／06／07／09／15／16／19／23 證據欄：框架中立的證據類別用語；V1 既有工具只作既有事實命名；oracle 未弱化。(5) DV-13 補充：1 km 對齊 oracle 比例性複核，保留。本紀錄同步更新：header、§1 效力、§3 總判定、B-4、B-10、DV-9（用語）、DV-11、DV-12、DV-13 補充、未採用的解讀、§4、§9 第 3／4／5／6 列、§10 evidence、§12。 | 治理 §5.3 第 2 類：不改變 V2 OC 的 intent、scope、constraints 或 acceptance semantics；不改變 V1 任何文字；無進行中 work item、無 Ticket、無既有 V2 evidence 受影響；B-4／B-10 的 boundary determination 維持「在 boundary 內」且修正後更貼近 accepted 語義。項目 3 與 5 經 DA 判定不需 acceptor 決定（B-10、DV-13 補充）。 |
| SPEC-V2 v2.2／本紀錄修訂 | 2026-09-25 | acceptor 指示「Valid-station Observation Time consistency … correct this without changing accepted product semantics」（v2.1 committed at `4efe777`；OC-V2 不重開） | R-V2-OBS-2 新增 (e)：有效測站 MUST 有 CWA 發布且可解析為明確觀測時刻的 `ObsTime`（如發布、不正規化；解析 HOW；新舊不影響有效性），缺少或無法解析者不進氣溫圖層、代表測站選取、縣統計與 dataset-level Observation Time；R-V2-OBS-4(a) 明示最大值只取有效測站、成功回應下恆有定義；AC-V2-05 新增反例 (7)（含最新 `ObsTime` 的站改壞 → 最大值落到其餘有效站）與 (8)（全部壞 → `invalid_response`），對應欄加 OBS-4，FAIL 例補充；R-V2-TC-1 涵蓋範圍同步；§10 加 v2.2 列。本紀錄同步更新：header、§1 效力、§3 總判定、B-18、DV-2 補充、DV-3 修訂、§4、§9 第 2 列與 v2.2 聚焦複核段、§10 evidence、§12。 | 治理 §5.3 第 2 類：derived-contract 一致性修正；不改變 V2 OC 的 intent、scope、constraints、acceptance semantics（S-1、S-2、S-5 不變）；不改變 V1 任何文字；無進行中 work item、無 Ticket、無既有 V2 evidence 受影響；不需 acceptor 決定。 |
| Tickets（V2）／本紀錄 §15 | 2026-09-25 | acceptor 指示「Proceed with V2 Ticket derivation using Matt's `to_tickets` skill … Do not create new: product semantics; acceptance criteria; invariants; architecture; verification oracles」（baseline `main` `b0642f8`；SPEC-V2 v2.2） | 新增 §15：Issues #35–#41（七張垂直切片，一條 blocking 鏈）、分配、覆蓋矩陣（AC-V2-01～23、INV-V2-1～9、§6.3 全部列、A-1～A-7）、boundary determination TB-V2-1～TB-V2-12、derivation-quality check（八項）、evidence。索引 `doc/ticket/tickets-v2.md`；SPEC-V2 只改標頭「Issue tracker」列與 §10 metadata 列（版本仍 v2.2）。 | 治理 §1.2、§3.4：Tickets 為 derived contracts，不需 acceptor 逐張核准；未新增任何 requirement、AC、invariant、架構或 oracle。 |
| Tickets（V2）依賴圖修正／本紀錄 §15 | 2026-09-25 | acceptor 指示「do not encode Bindings parallelism=1 as a false technical dependency … The current edge: #37 -> #38 is not required by the authoritative Spec」（PR #42 合併前；Ticket set、scope、AC／INV／high-risk ownership、SPEC-V2 不變） | 移除 blocked-by edge 38←37、新增 41←37（GitHub 原生 dependencies、#38 與 #41 的 `Blocked by` 段、索引 `tickets-v2.md`、本紀錄 §15.1／15.2／TB-V2-2／15.5 第 5 項／15.6 四方同步）；偏好執行順序改記為並行度 1 的排程偏好而非 edge；provenance（`/to-tickets` skill 未安裝）維持原文；八項 derivation-quality check 重跑皆 PASS。 | 治理 §5.3 第 2 類：只修正 Ticket 之間的依賴表示，不改任何 Ticket 的 What to build、AC、INV、High-risk 或 Spec 內容；不需 acceptor 逐張核准。 |
| Tickets（V2）分配修訂／本紀錄 §15 | 2026-09-26 | Issue #36 c1 R1 audit routing signal **R-1**（治理 §4.2）；Orchestrator 依治理 §2.4 派工 DA | decision record [`decision-20260926-ac-v2-01-county-round-trip-allocation.md`](decision-20260926-ac-v2-01-county-round-trip-allocation.md)（**DV-20**）：AC-V2-01 的「選縣往返」部分與 R-V2-MODE-5(a) 的選縣部分分配給 **#38**（Ticket 層 owner；追加的驗證分配逐字見該紀錄 §4.1）；Spec Integration Audit 對整條 AC-V2-01 的 Spec 層核對不變、不豁免。§15.2 #38 列、§15.3 AC 表 01 列與「R-V2 群組覆蓋」MODE 列同步。#36 分配、evidence 與結案不變；#39／#40／#41 不新增分配；SPEC-V2 文字不變（仍 v2.2）。 | 治理 §5.3 第 2 類：只修正 Ticket 的驗證與實作責任分配，不新增 AC／INV／R／oracle，不改 #38 的 What to build，不改 accepted 語義（OC S-3／AB-V2-1 不變）；不需 acceptor。 |

## 15. Tickets（V2，2026-09-25 derive）

### 15.1 依據、識別與方法

- **依據**：V2 Outcome Contract ACCEPTED（candidate `69c5a04`；§4 授權「derive Spec／Tickets」）；SPEC-V2 **v2.2**（DERIVED；`main` `b0642f8fec359090c772f26d37cade1438628881` 已合併 PR #34）；本紀錄 §1–§14；Bindings b3（§4 Formal、§5 assurance、§6 並行度 1、§7 紀錄）；`docs/agents/issue-tracker.md`、`docs/agents/triage-labels.md`；V1 先例 `tickets.md`、`derivation-SPEC.md` §11、Issue #24 的 issue 形狀。
- **派工指示**：acceptor 2026-09-25「Proceed with V2 Ticket derivation using Matt's `to_tickets` skill … Keep the Ticket set lean and coherent … There is NO required Ticket count … Do not create new: product semantics; acceptance criteria; invariants; architecture; verification oracles … Tickets must remain model-agnostic … Keep the Vercel credential dependency late … Radar alignment ownership must be explicit … Forecast preservation must be explicit」（全文見派工內容）。
- **方法**：repo 指定的 `/to-tickets`（Bindings §6；`docs/agents/issue-tracker.md`）。DA 核對本環境：`.claude/skills/` 只有設計類 skills、使用者層只安裝 `ui-ux-pro-max` plugin，**`/to-tickets` 的 skill 檔案未安裝**（與 V1 derivation record §9 對 `/to-spec` 的情形相同）；因此依 repo 文件與派工內容轉錄的同一方法執行——tracer-bullet 垂直切片（每張票是穿過所有層、可獨立驗證的窄路徑，大小以一個 fresh context window 為度）、prefactoring 先行、每票宣告 blocking edges、固定 issue 範本（Parent／What to build／Acceptance criteria 引用 Spec ID／Blocked by）、label `ready-for-agent`——不是另行發明的流程。
- **索引**：[`../../ticket/tickets-v2.md`](../../ticket/tickets-v2.md)。Tickets 本體在 GitHub Issues **#35–#41**（`yotsubamomo/aiot-classwork`），依依賴順序建立，GitHub 原生 issue dependencies **7 條邊**（36←35、37←36、38←36、39←38、40←39、41←37、41←40；2026-09-25 依 acceptor 指示修正：移除 38←37、新增 41←37），票內 `Blocked by` 段為權威。
- **Spec 對應版本**：v2.2（本次只改 SPEC-V2 標頭「Issue tracker」列與 §10 一列 metadata；語義、R、AC、INV、儀器不變）。

### 15.2 Ticket 清單與分配

| # | 票 | Class | 分配的 AC-V2 | 分配的 AB-V2 | INV-V2 | High-risk | Blocked by |
| --- | --- | --- | --- | --- | --- | --- | --- |
| #35 | 伺服器端 Latest Observation 路徑：`/api/` 觀測回應、四類失敗分類與安全邊界 re-scope | V2 Core | 03（離線／API）、04（API）、05、06（API）、07（觀測）、16（靜態＋封網）、17(a)(b)(d)、20（範圍） | 2、3、4、5（API）、10、11（部分） | 1、2、4、6（伺服器）、8 | H-1、H-2、H-3 | — |
| #36 | Now mode 與 Forecast mode：預設 Now、模式切換、全臺代表測站的 Latest Observation 與 Observation Time／Fetched Time | V2 Core | 01、02、03（瀏覽器抽樣）、04（UI success）、09(a)＋API 面、11、15（模式切換）、16（network log）、20（範圍）、21(13)、23（除 Back to Taiwan） | 1、2、5（部分）、6（代表規則）、11、12（部分） | 3、5、7（預報失敗）、8、9 | H-2、H-3 | #35 |
| #37 | Refresh 與狀態語義：newer／not-newer／failure、Stale／Unavailable、觀測失敗只影響 Now mode | V2 Core | 04（UI stale／unavailable）、06（UI）、08、09(b)、20（範圍） | 3、4、5（部分） | 6、7（觀測失敗） | H-1、H-3 | #36 |
| #38 | Taiwan → County → Station 下鑽：縣界互動圖層、County 脈絡、測站清單與詳情、Back to Taiwan、鍵盤路徑 | V2 Core | 01（選縣往返部分；DV-20）、10、12、16（縣界圖層）、20（範圍）、23（Back to Taiwan） | 1（選縣往返部分）、6、8（鍵盤路徑）、10（部分） | 3、5 | H-3、H-2 | #36 |
| #39 | 地圖圍欄與響應式可用性：pan／zoom 圍欄、初始視野、375 px 底部資訊面、44×44、768 px 破版檢查 | V2 Core | 13、14、15（完整）、20（範圍） | 7、8 | 8、9 | H-2 | #38 |
| #40 | Radar overlay：`/api/` 代理、顯示／隱藏、雷達時間戳、獨立狀態與 1 km 地理對齊 oracle | V2 Radar | 07（雷達）、09(c)、16（雷達 URL／log）、17(a)(e)（雷達）、18、19、20（範圍）；13、15 只在改變 CRS 時重驗 | 9、5（雷達）、10（部分） | 2、3、7（雷達） | H-1、H-3 | #39 |
| #41 | V2 整合驗收：README 與 CONTEXT 最終審查、V2 驗收文件、定向 V1 重驗、CI 全綠與部署 preview 驗證 | INTEGRATION／FINAL VERIFICATION（非 scope class；V1 #25 先例） | 03（preview）、16（最終 log）、17(c)(e)、20（完整）、21（全部）、22 | 10、11、12、13；全部 AB-V2 最終對照 | 1～9 最終自我核對 | H-1、H-2、H-3 | #37、#40 |

### 15.3 覆蓋矩陣（自我核對）

**AC-V2 → owner**（每條至少一張票；「部分」以票內範圍說明為準）：

| AC-V2 | Owner |
| --- | --- |
| 01 | #36（#36 subject 可觀察的全部部分）、#38（選縣往返部分；DV-20 [`decision-20260926-ac-v2-01-county-round-trip-allocation.md`](decision-20260926-ac-v2-01-county-round-trip-allocation.md) §4.1） |
| 02 | #36 |
| 03 | #35（離線／API）、#36（瀏覽器抽樣）、#41（preview） |
| 04 | #35（API）、#36（UI success）、#37（UI stale／unavailable） |
| 05 | #35 |
| 06 | #35（API）、#37（UI） |
| 07 | #35（觀測路徑）、#40（雷達路徑） |
| 08 | #37 |
| 09 | #36（(a)＋`/api/health` 回歸與 smoke 不變）、#37（(b)）、#40（(c)） |
| 10 | #38 |
| 11 | #36 |
| 12 | #38 |
| 13 | #39（#40 只在改變 CRS 時重驗） |
| 14 | #39 |
| 15 | #36（模式切換路徑）、#39（完整；#40 只在改變 CRS 時重驗） |
| 16 | #35（靜態檢查 re-scope＋封網）、#36（Now／Forecast network log）、#38（縣界圖層）、#40（雷達 URL 與 log）、#41（最終 log） |
| 17 | #35（(a)(b)(d)）、#40（(a)(e) 雷達）、#41（(c)、(e) 全部 evidence） |
| 18 | #40 |
| 19 | #40 |
| 20 | 每票在自己範圍維持（CI 全綠、V1 產物不變）；#41 完整（blob／diff、§6.3 彙整） |
| 21 | #36（第 13 項 `CONTEXT.md`）、#41（十四項全部） |
| 22 | #41（觀測部分 BLOCKED until RB-3） |
| 23 | #36（全部錨點，除 Back to Taiwan）、#38（Back to Taiwan） |

**INV-V2 → accountable coverage**（全部仍由 Spec Integration Audit 逐項核對，本表只是實作期的責任票）：

| INV-V2 | 責任票 |
| --- | --- |
| 1 預報路徑 CWA-free、key-free | #35（靜態＋封網）；#41 最終 |
| 2 金鑰零外洩、兩個位置 | #35、#40、#41 |
| 3 瀏覽器只呼叫 `/api/`、零外部請求 | #36、#38、#40、#41 |
| 4 `/api/health`、smoke、預報 endpoint 不變 | #35、#36、#41 |
| 5 兩種語義分開、觀測不聚合 | #36、#38（#37 的 Stale／Unavailable 標示） |
| 6 新鮮度單調 | #35（伺服器回應形態）、#37（UI 取代規則、Stale 只以失敗為基準） |
| 7 三條路徑獨立降級 | #36（預報失敗）、#37（觀測失敗）、#40（雷達失敗） |
| 8 V1 不變量與產物不變 | #35、#36、#39、#41（blob／diff） |
| 9 Scope class 分明 | #36、#39、#41 |

**§6.3 定向 V1 重驗 → owner**：AC-17、AC-18 → #36；AC-19 → #39；AC-02／AC-03／AC-24（Dashboard 側）→ #36；AC-04 → #35；AC-07(b)(c)(d)(f) 與 (e) supersede → #35（記述 #41）；AC-10（Dashboard 側）→ #36；AC-14 → #41；AC-15、AC-16、AC-22(a) → #41（AC-16 API 回歸亦於 #35、#36）；AC-26／INV-9 → #41（每票維持）；標題與 masthead → #36。其餘 V1 AC 依 Spec §6.3 末段以 CI 全綠與 blob／diff 證明（每票維持、#41 彙整）。

**A-1～A-7 → 承接**：A-1（觸及 H-1／H-2／H-3 的票，R1 record 明記核對段）→ #35～#41 全部（每票的 High-risk 段已標示類別）；A-2（Spec Integration Audit 逐項核 INV-V2-2／5／8 與 V1 兩句 SQL）→ Spec Integration Audit instance，不是票；A-3（高風險 blocking finding 不得由 FA 單獨 deferred）→ 全部票的 adjudication；A-4 → 不適用（Formal）；A-5（CI 機械檢查延伸）→ #35（延伸）、#41（最終執行）；A-6（release gate 材料）→ #41；A-7（diversity 記錄）→ Orchestrator 於各 audit record。

**R-V2 群組覆蓋**：MODE → #36（MODE-6(c) 另 #37；MODE-5(a) 選縣部分另 #38，DV-20）；OBS-1～6、9、11～13 → #35，OBS-4(c)、7、8、10、12（UI）、13（UI）→ #36／#37；DD-2、3、10 → #36，DD-1、4～9、11 → #38；SEC-1～7 → #35（雷達面 #40；SEC-3(c)(d)、SEC-5 最終 #41）；DEG-1、3、5 → #36（DEG-5 API 面 #35），DEG-2 → #37，DEG-4 → #40；MAP-1～4 → #39，MAP-5 → #36／#39；RSP-1～8 → #39（RSP-4 #36、RSP-6 部分 #38）；RAD-1～6 → #40；DOC-1 → #35 (6)(7)、#36 (1)(2)(3)、#38 (3)、#39 (8)、#40 (5)(9)、#41 全部；DOC-2 → #40、#41；DOC-3 → #41；DOC-4 → #36；DOC-5 → #36、#41；DOC-6 → 全部；TC-1 → #35（各票對自己的自動化）；TC-2 → #35（雷達樣本 #40）；TC-3 → #35、#41；TC-4 → #36～#40；ENV-1 → #41；ENV-2 → #35（文件）、#41。全部 73 條 R-V2 至少出現在一張票的 Traceability。

**缺口：無。** AB-V2-1～13 每條至少一張票（AB-1 #36；AB-2 #35／#36／#41；AB-3 #35／#37；AB-4 #35／#37；AB-5 #35／#36／#37／#40；AB-6 #36／#38；AB-7 #39；AB-8 #38／#39；AB-9 #40；AB-10 #35／#38／#40／#41；AB-11 #35／#36／#41；AB-12 #36／#41；AB-13 #41）。

### 15.4 Boundary determination（TB-V2）

| # | 判定 | 依據 |
| --- | --- | --- |
| TB-V2-1 | 七張票的 What to build 與 Acceptance criteria 全部引用 SPEC-V2 v2.2 既有的 R／AC／INV／§6.3 項目；票內只以「範圍說明」限定該票承接的部分，不重述、不改寫任何 PASS／FAIL oracle；沒有新增 requirement、AC、invariant、架構決定或 oracle（治理 §3.4）。 | Spec §2–§6 |
| TB-V2-2 | 技術 blocking edges 共 7 條（35→36、36→37、36→38、38→39、39→40、37→41、40→41），在 #36 之後分為兩條分支、#41 等待兩者；每條邊反映 Spec 要求的真實前置（#36 需觀測 `/api/`；#37 需 Now mode 骨架；#38 需 Now mode 基礎與代表測站，**不需** #37 的 Refresh／Stale／Unavailable 語義完成；#39 需縣／測站面板為資訊面內容；#40 排在圍欄儀器之後並在改變 CRS 時重驗 AC-V2-13／15；#41 需兩條分支全部結案）。Bindings §6 的並行度 1 只決定排程：偏好順序 #35、#36、#37、#38、#39、#40、#41 是排程偏好，**不**編成 blocked-by edge（初版曾以 38←37 表示此偏好，2026-09-25 依 acceptor 指示移除）。 | Bindings §6；Spec §2.3、§2.5、§5.3 |
| TB-V2-3 | Ticket 不指定 Executor 模型，不含 Opus／Fable／Codex 等字樣；模型與 binding 依 Bindings §3.1／§3.4 由 Orchestrator 處理。 | 派工指示 5；Bindings §3 |
| TB-V2-4 | 驗證比例性：每票只擁有與其切片實質相關的 AC／INV 證據；AC-V2-20 每票只在自身範圍維持、#41 彙整；沒有票重跑全部 AC-V2-01～23；#41 對 §6.3 以引用各票證據為主，不重做。 | 派工指示 6；Spec §6 |
| TB-V2-5 | 憑證依賴最後：#35～#40 以 A-3 的本機 `.env` 與離線樣本完成；需要 Vercel 金鑰的 preview 證據只在 #41 的 AC-V2-17(c)／AC-V2-22 觀測部分，且 RB-3 前記 BLOCKED（不是 FAIL）。沒有票要求 Agent 填入金鑰。 | 派工指示 7；OC-V2 A-2、A-3；Spec §9 |
| TB-V2-6 | UI／UX 附錄 A 未成為任何票的需求；#36／#39 明列其為 advisory。 | 派工指示 8；B-20 |
| TB-V2-7 | Radar 對齊由 #40 明確擁有（R-V2-RAD-5、AC-V2-19、1 km oracle、DV-13）；改變 CRS 時的 AC-V2-13／15 重驗亦在 #40。 | 派工指示 9 |
| TB-V2-8 | Forecast 保留由 #36 明確擁有（AC-17／AC-18 重驗、Forecast mode 原樣、預報區段層級降級、下方 dashboard 不變）；V1 產物不變的證明由 #35（後端 blob／diff）與 #41（最終）承接。 | 派工指示 10；Δ-5、Δ-7 |
| TB-V2-9 | 沒有新增人為 gate：唯一的 acceptor 動作是 Spec §9 已列的 RB-3 金鑰填入（只擋 #41 的兩個子項）與既有的部署可匿名存取、Orchestrator 主 session；RB-1／RB-2 維持 release 動作。 | 治理 §1.5；Bindings §2.6 |
| TB-V2-10 | 票標題與內文使用 `CONTEXT.md`／BRIEF-V2 §9 詞彙；不含程式碼；檔案路徑只限老師指定的名稱（`app.py`、`weather_query.py`、`data.db`、README、`CONTEXT.md`）與 Bindings §7 要求的 Spec／worklog／decision／索引路徑（V1 TB-6 同一規則）；內文無金鑰格式字串、無 `.env` 內容。 | CLAUDE.md；Bindings §7；H-1 |
| TB-V2-11 | #41 分類為 INTEGRATION／FINAL VERIFICATION（非 scope class），沿用 V1 #25 的 TB-8 先例：不新增需求，只做整合驗證、文件與部署證據；合法地依賴全部實作票。 | derivation-SPEC.md TB-8 |
| TB-V2-12 | `/to-tickets` skill 檔案未安裝於本環境（15.1）；依 repo 文件與派工內容轉錄的同一方法執行，未發明替代流程；此為方法（HOW）事實，不影響 Tickets 作為 derived contracts 的效力（治理 §3.4：Skills 屬 HOW，不取得設計權）。 | Bindings §6；V1 derivation record §9 先例 |

沒有發現 Spec 矛盾；未重開任何 Spec、OC 或 Grill 決定。

### 15.5 Derivation-quality check（acceptor 指示的八項）

| # | 檢查 | 結果 | 說明 |
| --- | --- | --- | --- |
| 1 | 每條 AC-V2-01～23 有 owner | PASS | 15.3 AC 表；23／23。 |
| 2 | 每條 INV-V2-1～9 有責任票且仍在 Spec Integration Audit | PASS | 15.3 INV 表；Spec §6.4 與本紀錄 §6 A-2 維持 SIA 逐項核對。 |
| 3 | 定向 V1 重驗有 owner | PASS | 15.3 §6.3 段；十列全部分配。 |
| 4 | H-1／H-2／H-3 覆蓋可發現 | PASS | 每票 High-risk 段標示類別並引用 A-1；15.2 表彙整（H-1：#35、#37、#40、#41；H-2：#35、#36、#38、#39、#41；H-3：#35、#36、#37、#38、#40、#41）。 |
| 5 | 依賴圖一致 | PASS | 7 條邊（35→36、36→37、36→38、38→39、39→40、37→41、40→41）、無環、blocker 編號皆小於被阻擋票、無把排程偏好編成的假依賴；票內 `Blocked by`、GitHub 原生 dependencies、索引、15.2 表四方一致（修正後 DA 以 `gh api` 逐票重新核對：#35 []、#36 [35]、#37 [36]、#38 [36]、#39 [38]、#40 [39]、#41 [37, 40]）。 |
| 6 | 未引入不必要的人為 gate | PASS | TB-V2-9。 |
| 7 | 無 Ticket 創造的語義 | PASS | TB-V2-1；AC 清單只引用 Spec ID 與範圍說明。 |
| 8 | 無票數膨脹或重複證據負擔 | PASS | 七張（V1 為八張）；TB-V2-4；每張為可獨立驗證的垂直切片；未依 R／AC 編號機械拆分。 |

### 15.6 Evidence（DA 自行執行；未印出任何金鑰）

- `git rev-parse HEAD` ＝ `b0642f8fec359090c772f26d37cade1438628881`（branch `home_work_01-v2-tickets`；`git status --porcelain` 只有工具殘留 `grep.exe.stackdump`）。
- 讀取：SPEC-V2 v2.2 全文（§1.2、§2、§3、§4、§5.3、§6、§7、§9）；本紀錄 §6、§11、§13、§14；OC-V2 §3、§4、§8；Bindings b3 §4–§7；`docs/agents/issue-tracker.md`、`triage-labels.md`；V1 `tickets.md`、`derivation-SPEC.md` §11.1、`worklog/20260924-ticket-derivation.md`；`gh issue view 24`（body、label、`dependencies/blocked_by` ＝ [23]）。
- Skill 核對：`.claude/skills/` ＝ banner-design、brand、design、design-system、slides、ui-styling、ui-ux-pro-max；`~/.claude/skills`、`~/.claude/commands` 不存在；`installed_plugins.json` 只有 `ui-ux-pro-max`；repo 內無 `to-tickets` 檔案。
- `gh issue create` ×7 → #35～#41（label `ready-for-agent`，body 以完整內容取代，0 個殘留 placeholder）；`gh api -X POST …/issues/<n>/dependencies/blocked_by` ×6；`GET …/dependencies/blocked_by`：#35 []、#36 [35]、#37 [36]、#38 [37]、#39 [38]、#40 [39]、#41 [40]。
- 依賴圖修正（2026-09-25，acceptor 指示；branch 於 `ba973686f4544cd565b0c45ce010c4b99495add0`）：`gh api -X DELETE …/issues/38/dependencies/blocked_by/<#37 的 issue id>`、`gh api -X POST …/issues/41/dependencies/blocked_by`（#37）；#38 與 #41 的 body 只改 `## Blocked by` 段（DA 以 diff 證明段落外零變更）；修正後 `GET …/dependencies/blocked_by`：#35 []、#36 [35]、#37 [36]、#38 [36]、#39 [38]、#40 [39]、#41 [37, 40]。Ticket scope、AC／INV／high-risk 分配與 SPEC-V2 未變。
- 七份 issue body 的金鑰格式掃描 0 命中；本節、索引與 SPEC-V2 的 metadata 修改亦不含金鑰。
- 本次未實作、未呼叫 CWA、未部署、未啟動 run、未 commit、未動 Vercel 或 repository variables。

### 15.7 需要 acceptor 的事項（Ticket 層）

| # | 事項 | 影響的票 | Authority |
| --- | --- | --- | --- |
| 1 | 在 Vercel 專案填入 `CWA_API_KEY`（preview 與 production 環境） | #41 的 AC-V2-17(c)、AC-V2-22 觀測部分（其餘先完成；BLOCKED 不是 FAIL） | acceptor（RB-3，b3） |
| 2 | 受審 commit 的部署不需登入可存取 | #41 | acceptor（RB-3） |
| 3 | 開符合 `orchestrator` mapping 的主 session 啟動 Formal run | 全部 | acceptor（Bindings §3.3） |
| 4 | 合併（RB-1）、繳交（RB-2） | #41 之後 | acceptor |
