# Decision record — SPEC-V2 §5.3 與 DV-11／DV-13 的 km↔px 換算註記數值更正（R-1(#40)；`home_work_01/`）

- **紀錄類型**：Design Authority decision record（治理 §3.6-A：在不改變任何 accepted 語義的前提下裁決；治理 §2.4「Contract 語義是否足夠、material ambiguity」；治理 §5.3 第 2 類「不改變 accepted 語義的 derived contract 修訂與 clarification」，須記錄對進行中工作、dependencies 與既有 evidence 的影響）。本紀錄是 SPEC-V2 §5.3 驗證儀器表中**非規範註記**（km↔px 換算數值）的**數值更正**，以及 derivation record DV-11、DV-13（含 v2.1 比例性補充）對應句的更正；**不是**儀器變更、oracle 變更或 AC 變更。[`derivation-SPEC-V2.md`](derivation-SPEC-V2.md) §14 以參照引用本紀錄。
- **編號**：**DV-23**（延續 DV-1～DV-19、[DV-20](decision-20260926-ac-v2-01-county-round-trip-allocation.md)、[DV-21](decision-20260926-county-layer-under-stale-unavailable-allocation.md)、[DV-22](decision-20260926-desktop-representative-marker-density.md)；寫入前 `DV-23` 於 `home_work_01/` 內 0 命中）
- **日期**：2026-09-26
- **來源**：Issue #40 cycle 1 R1 audit record [`../audit/issue-40-c1-r1.md`](../audit/issue-40-c1-r1.md) §7(a)／§9 routing signal **R-1**（治理 §4.2：契約文字問題是 routing signal，不是 blocking finding；R1 VERDICT CLOSURE，#40 已結案）；Executor worklog [`../worklog/issue-40.md`](../worklog/issue-40.md) Decisions 5 與 concerns (a)（待驗證主張；DA 自算核對，見 §2 E-5）；由 Orchestrator 依治理 §2.4 派工，run record [`../run/run-20260925-hw01-v2-formal.md`](../run/run-20260925-hw01-v2-formal.md)（2026-09-26 #40 R1 checkpoint「R-1(#40) → Design Authority (non-blocking)」）。
- **相關契約**：V2 Outcome Contract（ACCEPTED 2026-09-25，normative candidate `69c5a04`）§2.5 **S-8**（圍欄與縮放）、**S-11**（Radar「與地圖有意義的地理對齊（不預先接受實質偏移為已知限制…細微邊緣差異可記錄，明顯錯位不可）」）、§3 **AB-V2-7**、**AB-V2-9**；SPEC-V2 **v2.2** §0 標記約定（「第 5.3 節的『驗證儀器』是 DA 為客觀驗收選定的具體數值，**不是產品語義**」）、**R-V2-MAP-3**、**R-V2-RAD-5**、**AC-V2-13(d)**、**AC-V2-19**、**§5.3**（R-V2-MAP-3 列、R-V2-RAD-5 列）、§10；derivation record §3.2 **DV-11**、**DV-13**（含 v2.1 比例性補充）、§14、§15.2／§15.3（AC-V2-13 → #39；AC-V2-19 → #40）、TB-V2-7；治理 §1.2、§2.4、§3.6-A、§4.2、§5.3；Bindings §7。
- **參考 subject**：branch `home_work_01-v2-implementation` HEAD `ed5b6977ba1cc59808b2c6509f91f3c6e5e32b03`（#40 CLOSED，code anchor `fedffdd`；#39 CLOSED，code anchor `ae0b9dc`→R2 `f3bf245`）。本紀錄**未讀取任何實作或測試**；地圖 CRS 為 Leaflet 預設 EPSG:3857 這一事實取自 #40 R1 §2 AC-V2-13／15 列與 worklog §Contract reference（兩者一致，且 DA 的計算本就以 EPSG:3857 為前提——§5.3 的儀器自 v2.0 起即以 Web Mercator 為換算基礎）。
- **執行角色**：`gov-design-authority`（Bindings §3.1 `design_authority`；binding 核對由派工者依 Bindings §3.4 記入 run record）。
- **效力**：自本紀錄寫入起，SPEC-V2 §5.3 R-V2-RAD-5 列與 R-V2-MAP-3 列的 km↔px 換算註記、derivation record DV-11 與 DV-13 的對應句以 §4 的更正值為準（原文以〔DV-23 更正〕標記保留可追溯）；SPEC-V2 版本**仍為 v2.2**，§10 加「v2.2（annotation correction）」列、標頭「Spec 版本」列加註；沒有任何 R、AC、INV、oracle、儀器值或證據類別改變；#39、#40 的分配、evidence 與 CLOSURE 不變、不重開；Spec Integration Audit 與 #41 以更正後的 Spec 為準。本紀錄不修改任何實作、測試或 audit record。

## 1. 問題

SPEC-V2 v2.2 §5.3 的兩列儀器註記、以及 derivation record 的對應句，把「1 km 地面距離換算成該 zoom 的 CSS px」算錯：

- §5.3 R-V2-RAD-5 列：「每點誤差 ≤ 1 km（換算 px：z7 ≈ 0.35 px、z10 ≈ 2.8 px；…）」；DV-13：「1 km 是 5 個原生像素、在 zoom 10 約 2.8 CSS px」；DV-13 v2.1 補充 (1)「≥ 3.8 km…在 zoom 10 為 ≈ 10.6 CSS px、zoom 12 為 ≈ 43 px 的可見錯位」與 (3)「1 km 在 zoom 10 約 2.8 CSS px…更嚴的容差（例如 200 m）在 zoom 10 不足 1 px、無法可靠量測」。
- §5.3 R-V2-MAP-3 列：「z12 時 1 km ≈ 24 px、375 px 視窗 ≈ 16 km；z11 時 1 km ≈ 12 px FAIL；z14 時 375 px ≈ 4 km FAIL」；DV-11 同句。

#40 的 Executor（worklog Decisions 5）與 Primary Reviewer（R1 §7(a)、§9 R-1）各自以 Web Mercator 公式重算，得 z7 ≈ 0.87–0.91 px/km、z10 ≈ 6.98–7.31 px/km、z12 ≈ 27.9–29.2 px/km（#39 頁面實測 z12 28.95 px/km 同尺度）。R1 指出的 ambiguity：讀者若把 §5.3 的 px 註記當作 AC-V2-19 的換算門檻，會套用約 0.39 km 而非 1 km。

需裁決：(a) 這些數值是否確實錯誤；(b) 是否有任何 AC 以這些 px 數值為 PASS／FAIL 判準（若有，更正即語義變更，須 route acceptor）；(c) 若沒有，以何種形式更正並記錄版本。

## 2. 事實（依原始契約與紀錄；Executor／Reviewer 的計算只作對照，DA 自算）

| # | 事實 | 證據 |
| --- | --- | --- |
| E-1 | SPEC-V2 §0 標記約定：「第 5.3 節的『驗證儀器（verification instrument）』是 DA 為客觀驗收選定的具體數值，**不是產品語義**：Executor 可以選不同數值，只要第 5.3 節列出的產品語義判準仍成立並記錄。」§5.3 標題：「驗證儀器（DA 為客觀驗收選定；不是產品語義）」。 | `SPEC-V2.md:29,304` |
| E-2 | **R-V2-RAD-5**（規範條款）：「overlay 的每個影像像素 MUST 落在地圖對該像素經緯度…投影位置的 **1 km** 地面距離內（DV-13 的驗證 oracle）」。**AC-V2-19** PASS 條件：「…在 zoom 7 與 zoom 10（儀器）下，overlay 中該經緯度對應像素的畫面位置與地圖 `latLng → containerPoint` 的投影位置相距 **≤ 1 km 地面距離（換算為該 zoom 的 px）**」。兩處都不含任何 px 數值；px 只是「讀數的尺度」，門檻是 km。 | `SPEC-V2.md:203,252` |
| E-3 | **R-V2-MAP-3**（規範條款）：「上限 MUST 足以…個別選取測站（第 5.3 節儀器：1 km 地面距離 ≥ 20 CSS px）；MUST NOT 允許無意義的過度放大（第 5.3 節儀器：375 px 寬的視窗在上限仍跨 ≥ 5 km）」。**AC-V2-13(d)**：「放到上限：儀器檢查（1 km ≥ 20 CSS px；375 px 視窗跨 ≥ 5 km）成立、再放不動」。這兩個門檻（≥ 20 px、≥ 5 km）是儀器本身；§5.3 列內的「z12 時 1 km ≈ 24 px、375 px ≈ 16 km」等是 DA 對「`maxZoom` 12 滿足門檻、11 與 14 不滿足」的**推算註記**，不是門檻。 | `SPEC-V2.md:183,246,310` |
| E-4 | §5.3 R-V2-RAD-5 列的 px 數字出現在 PASS 檢查欄的括號內，前綴「換算 px」；同欄主句是「每點誤差 ≤ 1 km」。DV-13 的對應句是裁決的「依據」段（可量測性），不是裁決本身；裁決本身是「≤ 1 km；參考點…；zoom 7 與 10；自動化可重現」。 | `SPEC-V2.md:314`；`derivation-SPEC-V2.md:107-108` |
| E-5 | **DA 自算**（Web Mercator ＝ Leaflet `L.CRS.EPSG3857`，R ＝ 6378137 m，256 px tile；地面解析度 ＝ 2πR·cos φ／(256·2^z)；腳本見 §8）：1 km 換算 CSS px，lat 20.5–26.5（雷達產品範圍）→ **z7 0.873–0.914**（23.5°N 0.892）、**z10 6.984–7.309**（23.5°N 7.133）、**z11 13.97–14.62**（23.5°N 14.27）、**z12 27.93–29.24**（23.5°N 28.53）、**z13 55.9–58.5**（23.5°N 57.06）、**z14 111.7–116.9**（23.5°N 114.1）。375 px 視窗跨距（23.5°N）：z11 26.3 km、**z12 13.1 km**、z13 6.6 km、**z14 3.3 km**。3.8 km 於 z10 ≈ 27.1 px、z12 ≈ 108 px；200 m 於 z10 ≈ 1.43 px、z12 ≈ 5.7 px；z7 時 1 CSS px ≈ 1.12 km。與 Executor（0.89／7.1）、Reviewer（0.873–0.914／6.98–7.31／27.9–29.2）及 #39 實測（z12 28.95）一致。 | DA scratchpad `da23/mercator.py`（§8） |
| E-6 | 原文數值的錯誤型態：z7 0.35 與 z10 2.8 對正確值的比例同為 ≈ 1／2.55（同一個換算錯誤傳遞到 v2.0 的 DV-13 與 v2.1 補充的 10.6／43 px、「200 m 不足 1 px」）；z12 24 px 對正確值的比例 ≈ 1／1.19，且 16 km／12 px／4 km 與之一致——是 v2.0 DV-11 中另一個獨立的換算誤差。兩者都是 DA 在 v2.0 derive 時的計算錯誤；DV-11 同句中以**度**為單位的計算（z6 本島南北 174 px、z10 視窗 1.76°／0.52°）DA 重算後正確，不在更正範圍。 | 比例由 E-5 計算；`derivation-SPEC-V2.md:105,107,108` |
| E-7 | **#39**（AC-V2-13 owner）的判定：上限 z12 實測 1 km ≈ 28.95 px ≥ 20、375 px 視窗 ≥ 5 km → PASS；#39 R1／R2 CLOSURE。以正確值重推：z12 28.5 px ≥ 20 ✓、13.1 km ≥ 5 ✓；z13 57 px ✓、6.6 km ✓（「可接受 12–13」仍成立）；z11 14.3 px < 20 ✗；z14 3.3 km < 5 ✗——每個 zoom 的 PASS／FAIL 與原註記**完全相同**。 | `issue-40-c1-r1.md` §9 R-1（#39 實測值）；E-5 |
| E-8 | **#40**（AC-V2-19 owner）的判定一律以 km 作成：Executor「本票的量測一律以該點緯度的 km/px 換算為 km 判定，不使用上述 px 數字」；Reviewer 自算逐列誤差 ≤ 0.0075 km、參考點 DOM 幾何 z7 ≤ 0.0118 km／z10 ≤ 0.0048 km、渲染像素 z10 ≤ 0.064 km（0.45 px）／z7 ≤ 0.713 km（−0.65 px）、線性貼圖對照 3.879 km；R1 §7(a) 另核對：即使有人把錯誤 px 註記字面當門檻（≈ 0.39 km），主要判定（DOM 幾何、z10）仍通過。#40 R1 CLOSURE。 | `worklog/issue-40.md` Decisions 5；`issue-40-c1-r1.md` §2 AC-V2-19 列、§7(a) |
| E-9 | Issue #40 body（`gh issue view 40`）與 `doc/ticket/tickets-v2.md` 都**不含**任何 px 換算數值（只寫「1 km」與「約 3.8 km」）；README 的雷達段以 km 描述對齊（R1 §2 README 列），無 px 換算數值；V2 驗收文件尚未存在（#41）。錯誤數值只存在於 SPEC-V2 §5.3、derivation DV-11／DV-13，以及引用它們作為觀察的 #40 worklog 與 R1 record。 | `gh issue view 40`；grep `0.35|2.8 px|24 px|16 km|12 px FAIL|4 km FAIL` 於 `home_work_01/`（排除 `.venv`） |
| E-10 | SPEC-V2 §10 既有先例：「v2.2（metadata）」列——不動語義、R、AC、INV 或儀器的文字變更**不改版本號**、只加一列版本紀錄。v2.1 改版是因為儀器與 oracle 本身改變（pan oracle、下限 PASS 條件、Refresh 耦合）。 | `SPEC-V2.md:424-426` |
| E-11 | OC-V2 S-8、S-11、AB-V2-7、AB-V2-9 不含任何 px 數值；本裁決不需、也沒有任何一方主張改動它們。 | OC-V2 §2.5、§3 |

## 3. 對照

1. **數值確實錯誤（問題 (a)）。** E-5 的 DA 自算與 Executor、Reviewer 兩個獨立計算及 #39 的頁面實測四方一致；原文數值無法由任何合理的 Web Mercator 參數（R、tile 尺寸、緯度）得出（E-6）。這是 DA 自己在 v2.0 derive 時的算術錯誤，不是解讀差異。
2. **沒有任何 AC 以 px 註記為 PASS／FAIL 判準（問題 (b)）。** AC-V2-19 與 R-V2-RAD-5 的門檻是 **1 km 地面距離**，px 只是「換算為該 zoom 的 px」的讀數尺度（E-2）；AC-V2-13(d) 與 R-V2-MAP-3 的門檻是儀器 **≥ 20 CSS px、≥ 5 km**，§5.3 列內的 24 px／16 km 等只是 DA 推算 `maxZoom` 12 滿足門檻的註記（E-3）。§0 明文儀器不是產品語義，而這裡連儀器值（1 km、≥ 20 px、≥ 5 km、`minZoom` 6、`maxZoom` 12、E、參考點、zoom 7／10）都不動，只動註記。因此更正不改任何 AC 的文字、PASS 條件、FAIL 例或證據類別，也不改任何 R、INV、oracle。**不觸發 fail-closed。**
3. **更正不改變任何已作出的判定。** #39：每個 zoom 的 PASS／FAIL 在正確值下與原註記相同（E-7）。#40：全部以 km 判定，且在任何讀法下皆通過（E-8）。兩票的 evidence、audit record 與 CLOSURE 不受影響、不重開。
4. **DV-13 比例性補充的結論不變，但其第 (1)(3) 點的數值前提須更正。** (1) 的「≥ 3.8 km 容差 ＝ 預先接受可見錯位」在正確值下更強（z10 ≈ 27 px、z12 ≈ 108 px，而非 10.6／43 px）。(3) 的「200 m 在 zoom 10 不足 1 px、無法可靠量測」前提錯誤：正確為 ≈ 1.4 px。更正後 (3) 的論證是：1 km 在 z10 ≈ 7.1 px，瀏覽器量測可清楚分辨；200 m ≈ 1.4 px 落在渲染像素量測 1–2 px 的量化極限（#40 R1 的渲染量測本身在 z10 讀到 0.45 px 的殘差、z7 讀到 −0.65 px，正是此量級），且與正確作法本身約一個原生像素（≈ 185 m，(2) 點）的殘差同量級，無法可靠地與實作殘差區分。保留 ≤ 1 km 的裁決由 (1)（S-11 的接受語義決定工作量）、(2)（1 km 不構成額外負擔）、(4)（縣層級使用）獨立支撐，(3) 只是可量測性的佐證；R1 亦判「保留 1 km 的結論不受影響」。DA 確認：**DV-13 的裁決與比例性結論維持，不重開**；更正只及數值前提。
5. **版本與形式（問題 (c)）。** 依 E-10 先例，本次不改版本號（仍 v2.2），§10 加「v2.2（annotation correction）」列並在標頭加註；Spec 與 derivation 內以〔DV-23 更正；原文 …〕標記就地更正，使引用原文數值的 #40 worklog／R1 record 仍可對照。
6. **未採用的做法。** (i) *不更正、只靠 §0 的「儀器不是產品語義」聲明*——不採：R1 已指出一條具體的誤讀路徑（把 px 註記當門檻 → 0.39 km），而 Spec Integration Audit 與 #41 的驗收文件都會再讀 §5.3；一份數值錯誤的 derived contract 是持續的誤導。(ii) *改版為 v2.3*——不採：沒有任何規範內容改變，與「v2.2（metadata）」先例不一致，改版會讓 #35–#40 的 record 引用的「v2.2」看似被取代。(iii) *route acceptor*——不需：治理 §1.2 的 re-authorization 條件（超出 scope／constraints、改變 accepted 語義、reserved boundary）無一成立；治理 §5.3 第 2 類由 DA 以 decision record 決定。(iv) *順帶改動 z7 的「粗檢」定位或 zoom 選擇*——不採：正確值（z7 時 1 px ≈ 1.1 km，容差小於 1 px）恰好證明 zoom 7 只能作粗檢、zoom 10 為主要判定的原設計是對的，儀器不需調整。

## 4. 裁決（DV-23）

1. **SPEC-V2 §5.3 與 derivation record 的 km↔px 換算註記數值有誤，予以更正**；更正值見第 4.1 節。更正是治理 §5.3 第 2 類的非規範註記修訂（§3.6-A clarification 形式），**不是**儀器變更、oracle 變更或 AC 變更。
2. **沒有任何 AC 以 px 註記為判準**（第 3 節第 2 點）；AC-V2-13、AC-V2-19、R-V2-MAP-3、R-V2-RAD-5、DV-13 裁決（≤ 1 km）的文字、PASS 條件、FAIL 例、證據類別**逐字不變**；儀器值（1 km、≥ 20 CSS px、≥ 5 km、`minZoom` 6、`maxZoom` 12（12–13 可接受）、E、參考點集合、zoom 7 與 10、zoom 10 為主要判定／zoom 7 為粗檢）**全部不變**。
3. **SPEC-V2 的更正**（DA 本次以最小修改執行）：(a) §5.3 R-V2-RAD-5 列 PASS 檢查欄的括號內數值改為第 4.1 節的值，並明示「oracle 是地面距離；px 只是該 zoom 的讀數尺度」與 z7 作粗檢的理由（1 px ≈ 1.1 km）；(b) §5.3 R-V2-MAP-3 列儀器欄的推算註記改為第 4.1 節的值（含 z13 仍 PASS，支撐「可接受 12–13」）；(c) 標頭「Spec 版本」列加註「2026-09-26 §5.3 儀器註記的 px 換算數值依 DV-23 更正，版本不變」；(d) §10 加「v2.2（annotation correction）」列。**版本仍 v2.2**。
4. **derivation record 的更正**（DA 本次以最小修改執行）：DV-11 的「z12 時 1 km ≈ 24 px、375 px ≈ 16 km（z11 12 px FAIL；z14 4 km FAIL）」、DV-13 的「在 zoom 10 約 2.8 CSS px」、DV-13 補充 (1) 的「≈ 10.6 CSS px／≈ 43 px」與 (3) 全句，依第 4.1 節就地更正並以〔DV-23 更正〕標記保留原文；§14 加一列引用本紀錄。DV-11、DV-13 的裁決內容與「不需 acceptor」結論不變。
5. **#39、#40 的分配、evidence、audit record 與 CLOSURE 不變、不重開**；#40 R1 §7(a) 與 §9 R-1、worklog Decisions 5／concerns (a) 由本紀錄解決，Reviewer 與 Executor 不需補記。**#41 不新增分配**；其 V2 驗收文件（R-V2-DOC-3／AC-V2-21(14)）對 AC-V2-13、AC-V2-19 的引用以 km 與更正後的 §5.3 為準。
6. **Spec Integration Audit 以更正後的 Spec 為契約**（SPEC-V2 v2.2 含 DV-23 更正；識別以派工者 commit 的 SHA 為準，第 7 節）。SIA 核對 AC-V2-13／AC-V2-19 時，#39／#40 record 內引用的原文 px 數值以本紀錄第 4.1 節對照即可，不構成 finding；SIA 的義務不變、不被豁免。
7. **其他一律不變**：OC-V2 全文；SPEC-V2 §0–§4、§5.1–§5.2、§6–§9 全文；§5.3 其餘各列；DV-1～DV-22；Ticket 分配與依賴圖。

### 4.1 更正值（Web Mercator ＝ Leaflet `L.CRS.EPSG3857`；R ＝ 6378137 m；256 px tile；地面解析度 ＝ 2πR·cos φ／(256·2^z)）

| 項目 | 原文（有誤） | 更正值（lat 20.5–26.5；括號為 23.5°N） | 用途與判定 |
| --- | --- | --- | --- |
| 1 km @ z7 | ≈ 0.35 px | **≈ 0.87–0.91 px**（0.89） | §5.3 RAD-5 列讀數尺度；1 CSS px ≈ 1.1 km → zoom 7 只作粗檢（不變） |
| 1 km @ z10 | ≈ 2.8 px | **≈ 6.98–7.31 px**（7.13） | §5.3 RAD-5 列、DV-13、DV-13 補充 (3)；zoom 10 為主要判定（不變） |
| 1 km @ z11 | ≈ 12 px FAIL | **≈ 14.0–14.6 px**（14.3）< 20 → **FAIL（不變）** | §5.3 MAP-3 列、DV-11 |
| 1 km @ z12 | ≈ 24 px | **≈ 27.9–29.2 px**（28.5）≥ 20 → **PASS（不變）**；#39 實測 28.95 | §5.3 MAP-3 列、DV-11 |
| 375 px 視窗 @ z12 | ≈ 16 km | **≈ 13.1 km** ≥ 5 → **PASS（不變）** | §5.3 MAP-3 列、DV-11 |
| z13（可接受上限） | （未列） | 1 km ≈ 57 px、375 px ≈ 6.6 km → **PASS**（「可接受 12–13」不變） | §5.3 MAP-3 列、DV-11（補列，只作推算） |
| 375 px 視窗 @ z14 | ≈ 4 km FAIL | **≈ 3.3 km** < 5 → **FAIL（不變）** | §5.3 MAP-3 列、DV-11 |
| 3.8 km 線性貼圖偏移 | z10 ≈ 10.6 px、z12 ≈ 43 px | **z10 ≈ 27 px、z12 ≈ 108 px** | DV-13 補充 (1)：可見錯位的論證更強 |
| 200 m @ z10 | 不足 1 px、無法可靠量測 | **≈ 1.4 px**（z12 ≈ 5.7 px）——在 1–2 px 渲染量化極限、與 ≈ 185 m 原生像素殘差同量級 | DV-13 補充 (3)：前提更正、結論（保留 ≤ 1 km）不變 |

未更正（DA 重算後正確）：DV-11／§5.3 MAP-2 列以度計算的 z6 本島南北 174 px（fitBounds lat 21.85–25.35 ＝ 3.5° × ≈ 49.7 px/°）與 z10 視窗寬 1.76°／0.52°；DV-13 的線性貼圖最大誤差 ≈ 3.8 km（#40 R1 自算 3.8079 km 一致）、分段殘差 1.02／0.46／0.26 km、原生像素 ≈ 185 m。

## 5. 是否改變 accepted 語義：**否**

- **Outcome Contract**：S-8、S-11、AB-V2-7、AB-V2-9 的文字與語義不變；OC 從未含 px 數值（E-11）。「有意義的地理對齊、不預先接受實質偏移」的接受語義由 1 km oracle 承載，oracle 不變。
- **Derived contract**：R-V2-MAP-3、R-V2-RAD-5、AC-V2-13、AC-V2-19 逐字不變；§5.3 的儀器值不變；只有儀器表內「DA 推算／換算」的註記數值更正。沒有新增、刪除或弱化任何 R／AC／INV／oracle／證據類別；沒有任何已作出的 PASS／FAIL 改變（E-7、E-8）。
- **變更性質**：治理 §5.3 第 2 類（不改變 accepted 語義的 derived contract 修訂；§3.6-A 第一種情形——既有來源只有一種正確讀法：門檻是 km，px 是尺度——的 clarification 加數值更正）。不建立任何其他工作將依賴的新設計基線（正確的 px/km 是幾何事實，#39／#40 已各自以此事實工作）。
- **Boundary determination**：更正在 V2 Outcome Contract boundary 內；不涉及 scope、constraints、acceptance boundary 或授權；**不需 acceptor**；沒有 fail-closed 路徑。若更正會改變任何 AC 的 PASS／FAIL（第 3 節第 2、3 點證明不會），才會是第 1 類 contract change——本紀錄明確確認此情形不成立。

## 6. 受影響 work items 與 evidence

| 對象 | 影響 |
| --- | --- |
| **#40**（已結案） | 無。分配、evidence、R1 CLOSURE 不變；R1 §7(a)／§9 R-1 與 worklog Decisions 5／concerns (a) 由本紀錄解決。worklog 與 R1 record 內引用的原文 px 數值是對當時 Spec 的正確觀察，不需改寫（audit record 與 worklog 不由 DA 修改）。 |
| **#39**（已結案） | 無。AC-V2-13(d) 的 PASS（z12 實測 28.95 px/km ≥ 20；375 px ≥ 5 km）在更正後的註記下同樣成立；R1／R2 CLOSURE 不變。 |
| **#35～#38**（已結案） | 無。 |
| **#41**（READY，最後一票） | 不新增分配。V2 驗收文件對 AC-V2-13／AC-V2-19 的對照以更正後的 §5.3 與 km 為準；README 雷達段已以 km 描述（E-9），不需因本紀錄修改；#41 若引用 §5.3 數值，用更正值。 |
| **Spec Integration Audit**（#41 之後） | 以更正後的 SPEC-V2 v2.2（含 DV-23，commit SHA 由派工者記入 run record）為契約；義務不變、不豁免。#39／#40 record 內的原文 px 數值以第 4.1 節對照，不是 finding。 |
| **SPEC-V2.md** | §5.3 兩列、標頭第 4 行、§10 一列（DA 本次以最小修改更新；版本仍 v2.2）。 |
| **derivation-SPEC-V2.md** | §3.2 DV-11、DV-13、DV-13 補充 (1)(3)（就地更正＋〔DV-23 更正〕標記）；§14 加一列（DA 本次以最小修改更新）。§15.2／§15.3 不變。 |
| **`doc/ticket/tickets-v2.md`** | 「實作過程中的調整」段由 Orchestrator 補一列引用本紀錄。 |
| **既有 evidence** | #35～#40 的 audit records、worklogs、截圖、`alignment.json`、network log 全部沿用；沒有任何既有 evidence 因本裁決失效。 |
| **Dependencies** | 依賴圖 7 條邊不變。 |

## 7. Orchestrator／tracker 動作（本紀錄指定；DA 不執行）

1. **`doc/ticket/tickets-v2.md`**：「實作過程中的調整」段加一列：2026-09-26，DV-23（本紀錄路徑；來源 #40 R1 的 routing signal R-1，non-blocking），SPEC-V2 §5.3 R-V2-RAD-5／R-V2-MAP-3 列與 derivation DV-11／DV-13 的 km↔px 換算註記數值更正為 Web Mercator 正確值（1 km：z7 ≈ 0.89、z10 ≈ 7.13、z12 ≈ 28.5 px）；不改任何 AC／oracle／儀器值、不改 #39／#40 任何判定；SPEC-V2 版本仍 v2.2；不改 accepted 語義（治理 §5.3 第 2 類）。
2. **Issue #40、#39**：不需修改（body 不含 px 數值，且已 CLOSED）。**Issue #41**：不需修改 body；派工 #41 與 Spec Integration Audit 時，bounded pack 列入本紀錄路徑並註明「SPEC-V2 v2.2（DV-23 更正後，commit `<SHA>`）」。
3. **Run record**：在 checkpoints／routing 記本次 DA 派工結果（R-1(#40) resolved by DV-23）、DA binding 核對（Bindings §3.4），以及承載本更正的 commit SHA。
4. **Commit**：本紀錄、`derivation-SPEC-V2.md` 與 `SPEC-V2.md` 的最小修改依 SA-1 由派工者原樣 commit。注意：`doc/spec/SPEC-V2.md` 在 `doc/spec/`，**不在** Bindings §7 的 record-only paths（`doc/governance/**`）；本次 delta 只含契約註記文字、無實作或測試變更，不改變任何已結案 Ticket 的 code subject（code anchor `ae0b9dc`／`f3bf245`、`fedffdd` 等不變）。派工者依 Orchestrator Contract §7 判定並記錄此 delta 對 subject identity 的處理方式（建議：Spec＋records 單獨一個 commit，run record 註明「contract-text only」）。

## 8. Evidence（DA 自行執行，全部唯讀；未讀取 `.env`、未使用任何金鑰、未呼叫 CWA、未讀任何實作或測試檔）

- 讀取：Bindings b3 全文；治理 §1.2、§2.1、§2.4、§3.3–§3.6、§5.3；`SPEC-V2.md` 標頭與 §0、§2.6（MAP-1～4、RSP-1～8）、§2.7（RAD-1～6）、§3（AC-V2-01～23 全表）、§5（§5.1–§5.3 全部）、§10；`derivation-SPEC-V2.md` 標頭、§1、§3.2 DV-11～DV-19 與「未採用的解讀」、§14 全部列、§15 章節標題；`issue-40-c1-r1.md` 全文；`worklog/issue-40.md` 的 px 相關段（Contract reference、Decisions 5、渲染像素量測、concerns (a)）；`outcome-contract-v2.md` S-11、AB-V2-9、已知風險列（grep）；run record「Work item status」#40 列與 2026-09-26 #37／#40 R1 checkpoint；DV-20、DV-21、DV-22 全文（格式先例）；`gh issue view 40`（title、state、labels、body 的 px／km／DV 相關行）；`doc/acceptance/` 目錄（只有 V1 `ACCEPTANCE.md`）。
- 計算：scratchpad `da23/mercator.py`（Web Mercator：R ＝ 6378137、256 px tile、cos φ；輸出 z7／10／11／12／13／14 於 lat 20.5、22.0、23.5、23.55、25.0、25.3、26.5 的 px/km，375 px 視窗跨距，3.8 km 與 200 m 的 px 換算，z7 的 1 px 公里數，原生像素尺寸）。輸出值全部列於 §2 E-5 與 §4.1。
- Grep：`0\.35|2\.8 (CSS )?px|≈ 24 px|24 px|≈ 16 km|10\.6 CSS|43 px|不足 1 px|12 px FAIL|4 km FAIL` 於 `home_work_01/`（排除 `.venv`）——錯誤數值只在 `SPEC-V2.md:310,314`、`derivation-SPEC-V2.md:105,107,108`，以及引用它們的 `worklog/issue-40.md:23,109` 與 `issue-40-c1-r1.md:78,104-105`；`DV-23` 於 `home_work_01/` 0 命中。
- Git（read-only）：branch `home_work_01-v2-implementation` HEAD `ed5b6977ba1cc59808b2c6509f91f3c6e5e32b03`；`git status --porcelain` 只有既存的工具殘留 `grep.exe.stackdump`。
- 寫入：本紀錄（新增）；`SPEC-V2.md` 標頭第 4 行、§5.3 R-V2-MAP-3 列、§5.3 R-V2-RAD-5 列、§10 新增一列（Edit 局部修改）；`derivation-SPEC-V2.md` DV-11 一句、DV-13 一句、DV-13 補充兩處、§14 新增一列（Edit 局部修改）。未修改 OC-V2、任何 audit record、worklog、Issue、實作或測試；未 commit（派工者依 SA-1 處理）。
- 產出不含任何金鑰格式字串。
