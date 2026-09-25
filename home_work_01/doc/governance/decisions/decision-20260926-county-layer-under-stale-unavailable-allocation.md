# Decision record — 縣界互動圖層與 County 脈絡在 Stale／Unavailable 下的 Ticket 分配與內容（R-1(#37)；`home_work_01/`）

- **紀錄類型**：Design Authority decision record（治理 §3.6-A：在不改變任何 accepted 語義的前提下裁決；治理 §2.4「Contract 語義是否足夠…derived contract 的 derivation 與 boundary determination」；治理 §5.3 第 2 類「不改變 accepted 語義的 derived contract 修訂與 clarification」，須記錄對進行中工作、dependencies 與既有 evidence 的影響）。本紀錄同時是 V2 Ticket derivation 的**分配修訂**：[`derivation-SPEC-V2.md`](derivation-SPEC-V2.md) §15.2、§15.3 與 §14 以參照引用本紀錄。
- **編號**：**DV-21**（延續 `derivation-SPEC-V2.md` §3.2 的 DV-1～DV-19 與 [DV-20](decision-20260926-ac-v2-01-county-round-trip-allocation.md)）
- **日期**：2026-09-26
- **來源**：Issue #37 cycle 1 R1 audit record [`../audit/issue-37-c1-r1.md`](../audit/issue-37-c1-r1.md) §4 (c)／§7 routing signal **R-1**（治理 §4.2：契約不足是 routing signal，不是 blocking finding，不觸發 promotion）；由 Orchestrator 依治理 §2.4 派工，run record [`../run/run-20260925-hw01-v2-formal.md`](../run/run-20260925-hw01-v2-formal.md)（2026-09-26 #37 R1 checkpoint「R-1(#37) → Design Authority」）。
- **相關契約**：V2 Outcome Contract（ACCEPTED 2026-09-25，normative candidate `69c5a04`）§2.5 **S-4** 下鑽（County 脈絡＝縣名、有效／顯示測站數、最高與最低氣溫測站、測站清單）、**S-6** 失敗語義（首次載入無有效資料 → 留在 Now mode、地圖與縣界可見、明確的 unavailable 狀態；Stale＝仍顯示上一次成功資料）、**S-7** 獨立降級（觀測失敗只影響 Now mode）、§3 **AB-V2-3**「零有效測站＝失敗」、**AB-V2-4**、**AB-V2-5**、**AB-V2-6**；SPEC-V2 **v2.2** R-V2-OBS-4(c)、**R-V2-OBS-5**、**R-V2-OBS-6**、**R-V2-OBS-10(a)(b)(c)(e)**、R-V2-MODE-6(c)、R-V2-DD-2、**R-V2-DD-4**、**R-V2-DD-5**、R-V2-DD-8、R-V2-DD-9(a)、R-V2-DD-10、**R-V2-DEG-2**、INV-V2-5、INV-V2-7、**AC-V2-08**、AC-V2-10、AC-V2-12、§6.1、§6.2、§6.4；derivation record §3.2 DV-3、DV-6、§6（H-3 對 V2 的適用）、§15.2、§15.3（AC-V2-08 → #37；DEG-2 → #37）、TB-V2-2、**TB-V2-4**；`decision-20260923-high-risk-categories.md` §2.3 **H-3**、A-1；Issue **#37**（CLOSED）與 **#38**（OPEN，已含 DV-20 追加）body（DA 於 2026-09-26 以 `gh issue view` 讀取）；治理 §1.2、§3.4、§3.6、§3.8、§4.1、§4.2、§4.4、§4.7、§5.3。
- **參考 subject**：branch `home_work_01-v2-implementation` HEAD `040324b905f0b3d0897c4163cff28ea9de2abbcc`（#37 已結案，code anchor `7a3b469`）；`static/app.js:167`（`obsState`）、`:732-737`（`applyObservationFailure`：`obsState = obs ? "stale" : "unavailable"`，Unavailable 下 `obs` 維持 `null`）、`:796`（無 `obs` 時 Taiwan-wide 有效測站數顯示「—」）只作機制 grounding，不作為設計依據。
- **執行角色**：`gov-design-authority`（Bindings §3.1 `design_authority`；binding 核對由派工者依 Bindings §3.4 記入 run record）。
- **效力**：自本紀錄寫入起，Issue #38 的驗證分配與實作責任依第 4 節擴充；第 4.2 節是 R-V2-DD-5 末句與 R-V2-OBS-6／OBS-10 在 Unavailable／Stale 下的 clarification，作為 #38 Work Contract 的引用（治理 §3.6-A）；SPEC-V2 文字不變（仍 v2.2）；#37 的分配、evidence 與結案不變、不重開；Spec Integration Audit 的義務不變。本紀錄不修改任何實作或測試。

## 1. 問題

**(a) 分配缺口。** derivation record §15.2／§15.3 把 **AC-V2-08**（含 (a)「首次載入觀測失敗 → 留在 Now mode、地圖與縣界可見…」與 (b)「成功後 Refresh 失敗 → 資料…保留，Stale 標示與原因可見」）與 **R-V2-DEG-2**（「觀測失敗只影響 Now mode 的觀測層（標記、面板資料、脈絡）：地圖、**縣界互動**、模式切換、Forecast mode、下方 dashboard、Radar 全部維持可用」）**只**分配給 #37。帶縣名屬性的縣界互動圖層（R-V2-DD-4）與 County 脈絡（R-V2-DD-5）只在 **#38** 建立，而 #38 只 blocked by #36、不依賴 #37（TB-V2-2；acceptor 2026-09-25 指示移除 38←37）。因此在 #37 的 subject 上，「縣界可見」只能以 V1 底圖的靜態輪廓滿足、「縣界互動維持可用」沒有可驗證對象；#37 的 issue 把「縣脈絡在各狀態下的內容」寫為「#38 承接本票的狀態規則」，但 #38 的 body 沒有對應的 AC、Traceability 或義務。於是在 #38 之後，「互動縣界圖層與 County 脈絡在 Stale／Unavailable 下是否仍可見可用、顯示什麼」在 Ticket 層沒有 owner，只剩 Spec Integration Audit（Spec §6.4；治理 §4.7）兜底——與 #36 R1 的 R-1（→ DV-20）同型。

**(b) 附帶的語義問題。** R-V2-DD-5 末句「零有效測站的縣可選取：脈絡顯示 0 與『—』，不是錯誤」；R-V2-DEG-2／R-V2-OBS-10(a) 又把「脈絡」列為受觀測失敗影響的觀測層。Unavailable（沒有任何可顯示的 Latest Observation）下若仍可選縣而 #38 沿用 DD-5 顯示「0 個有效測站」，會把「沒有資料」呈現成「該縣零有效測站」（H-3：值是否誠實標示；no-data vs zero）。Stale 下脈絡應為上一次成功資料，Reviewer 認為無歧義。

需裁決：由哪張 Ticket 在 Ticket 層驗證 #38 的縣界互動圖層與 County 脈絡在 Stale／Unavailable 下的行為（候選 #38），或確認 Spec Integration Audit 是正確且充分的 owner；並釐清 Unavailable 下 County 脈絡不得把「0 有效測站」呈現為資料。

## 2. 事實（依原始契約與紀錄，不採用 Executor／Reviewer 的結論）

| # | 事實 | 證據 |
| --- | --- | --- |
| E-1 | AC-V2-08 的 PASS 條件：(a) 首次載入觀測失敗 → 留在 Now mode、**地圖與縣界可見**、Unavailable 狀態與類別原因可見、Refresh 可用、模式切換可見、未自動切換、無任何預報值被當成觀測；(b) 成功後 Refresh 失敗 → 資料、Observation Time、Fetched Time 保留，Stale 標示與原因可見，Refresh 可用；(c) 再次成功 → Stale 清除；(d) 年齡不觸發 Stale。證據類別「瀏覽器模擬＋截圖（stale、unavailable 各至少一張，桌機與 375）」。對應 AB-V2-4；R-V2-OBS-10。 | `SPEC-V2.md:241` |
| E-2 | R-V2-DEG-2：「觀測失敗只影響 Now mode 的觀測層（標記、面板資料、脈絡）：地圖、縣界互動、模式切換、Forecast mode、下方 dashboard、Radar 全部維持可用；狀態依 R-V2-OBS-10。」來源 S-7、AB-V2-5。 | `SPEC-V2.md:172` |
| E-3 | R-V2-OBS-10：(a) **Unavailable ＝ 沒有可顯示的有效 Latest Observation**；首次載入失敗 MUST 留在 Now mode、地圖與縣界可見、明確的 unavailable 狀態與非機密原因、Refresh 可用、不暗示預報資料是觀測；(b) **Stale ＝ 最近一次取得失敗而介面仍顯示上一次成功的資料**；失敗的 Refresh MUST 保留上一次有效資料與其兩個時間、顯示明確的 Stale 標示與原因；(c) 之後成功清除 Stale；(e) Stale／Unavailable 的呈現 MUST 與 success 在視覺與文字上可辨。這些是**狀態層級**的 MUST，沒有「只在無選取時」的限定。BRIEF-V2 §9 詞彙：Unavailable「沒有可顯示的有效 Latest Observation」。 | `SPEC-V2.md:134`；`BRIEF-V2.md:124-125` |
| E-4 | R-V2-OBS-6：「任何缺值、哨兵或無效欄位 MUST 顯示為『—』，永不顯示為數值。」R-V2-OBS-4(c)：Unavailable 狀態下兩個時間欄位仍存在、值為「—」。R-V2-DD-10：無選取時面板 MUST 顯示 dataset-level Observation Time、Fetched Time、Refresh、有效測站數。 | `SPEC-V2.md:128,130,152` |
| E-5 | R-V2-OBS-5（S-2；AB-V2-3）：一次取得成功若且唯若至少一個有效測站；**零有效測站 ＝ 失敗**（`invalid_response`）。即 OC 與 Spec 在 dataset 層已把「零有效測站」定為失敗（→ Unavailable／Stale），不是可呈現的資料值。 | `SPEC-V2.md:129`；OC-V2 §3 AB-V2-3 |
| E-6 | R-V2-DD-5：選縣後 MUST (a) 調整視野使該縣在地圖上的有效測站在視窗內；(b) 顯示 County 脈絡：縣名、有效測站數（未上圖者另顯示或標示）、最高與最低測站（名稱／值）、測站清單；(c) 不計算縣平均；(d) 全部有效測站可到達。末句：「零有效測站的縣可選取：脈絡顯示 0 與『—』，不是錯誤。」來源 S-4、D-9、P-7～P-10。R-V2-DD-4：縣界互動圖層帶縣名屬性、hover 突顯並顯示縣名、點選選取、不以資料著色、只在 Now mode 作用。R-V2-DD-2：無有效測站的縣沒有代表標記（不是失敗）。 | `SPEC-V2.md:143-147` |
| E-7 | derivation §15.3：AC-V2-08 → **#37**（唯一 owner）；DEG-2 → #37；OBS-10 → #36／#37；INV-V2-7 責任票 #36（預報失敗）、#37（觀測失敗）、#40（雷達失敗）。#38 的分配：01（選縣往返部分，DV-20）、10、12、16（縣界圖層）、20（範圍）、23（Back to Taiwan）；#38 body 的 R 列不含 OBS-10、DEG-2；AC 列不含 08；INV 列為 3、5。#37 body「Out of scope」：「縣脈絡在各狀態下的內容（#38 承接本票的狀態規則）」——但 #38 body 沒有對應義務。 | derivation §15.2、§15.3；Issue #37、#38 body |
| E-8 | #37 R1（CLOSURE）：AC-V2-08(a) 對 #37 subject PASS，「縣界可見」由 vendored 底圖的 27 條輪廓 path 滿足；R-V2-DEG-2「對本 subject 存在的元素成立（…縣界互動圖層與 Radar 尚不存在）」；Unavailable 下 Taiwan-wide 面板的有效測站數為「—」；R1 判定「不是 #37 缺陷」，以 R-1 route DA。 | `issue-37-c1-r1.md` §2 AC-V2-08(a) 列、§4 (c)、§7 R-1 |
| E-9 | H-3（`decision-20260923-high-risk-categories.md` §2.3）：風險為值算錯或不誠實標示；derivation §6 對 V2 的適用延伸至觀測值與推導值的可見分開、代表測站值不得標示為縣值、無觀測聚合、用語；#38 High-risk 段已標示 H-3。 | 該紀錄 §2.3；derivation §6；Issue #38 body |
| E-10 | 治理 §4.1：Formal 下每個 work item 的 independent audit MUST 執行；§3.8：verification 與結案版本 MUST 可對應、最終產物須受相應 coverage；§4.7：Spec Integration Audit MUST NOT 重開已閉合的 Ticket finding，除非有新的 integration-level evidence；§3.4：Tickets 不得自行重新定義 AC。TB-V2-4：每票只擁有與其切片實質相關的 AC／INV 證據。 | 治理 §3.4、§3.8、§4.1、§4.7；derivation §15.4 |
| E-11 | OC S-4、S-6、S-7 與 AB-V2-3～6 的文字在本裁決中不需改動，也沒有任何一方主張改動。 | OC-V2 §2.5、§3 |

## 3. 兩個選項與對照

- **(A) 把 AC-V2-08(a)(b) 的「縣界互動圖層與 County 脈絡」部分（連同 R-V2-DEG-2 的縣界互動／脈絡部分、R-V2-OBS-10(a)「縣界可見」的互動圖層部分、R-V2-OBS-6 對 County 脈絡欄位的適用）分配給 #38**，作為 Ticket 層 owner 與實作責任票；Spec Integration Audit 仍對整條 AC-V2-08 作 Spec 層核對。
- **(B) 只由 Spec Integration Audit 承接**：不改任何 Ticket 分配。

對照契約與治理：

1. **Owner 跟著引入的元素走。** 縣界互動圖層與 County 脈絡由 #38 引入；R-V2-DEG-2 逐字要求「縣界互動」在觀測失敗下維持可用、並把「脈絡」列為觀測層；R-V2-OBS-10 的 Stale／Unavailable 是狀態層級 MUST，不因選縣而免除。治理 §4.1／§3.8 要求引入該元素的 Ticket 的 audit 能觀察到它在契約要求的狀態下是否成立。選 (B) 時，#38 可能帶著「Unavailable 下脈絡顯示 0 個有效測站」或「選縣後 Stale 標示消失」結案，要到 #39、#40、#41 全部結案後才在 Spec Integration Audit 首次被觀察到；那時是 integration-level finding、晚期 rework，可能牽動 #39 的資訊面版面（County 脈絡是資訊面的內容）與 #40——與在 #38 的瀏覽器模擬裡多跑兩個狀態相比明顯不成比例。與 DV-20 第 3 節第 1 點同理。
2. **§4.7 是 Spec 層 coverage 與整合的核對點，不是單張 Ticket 行為的首次驗證點。** 若 #38 的 audit 從未觀察縣脈絡在失敗狀態下的內容，就沒有可重開的 Ticket finding，只有一個從未被 Ticket 層驗證的 Spec 條款——這正是 §15.3 覆蓋矩陣應避免的狀態（DV-20 第 3 節第 2 點）。
3. **比例性（TB-V2-4）成立。** #38 本來就必須以瀏覽器驗收做 AC-V2-10／12（選縣、脈絡、清單、Back to Taiwan、鍵盤路徑），且 #37 已建立以攔截／替換 `/api/` 回應模擬失敗的方法；追加的只是在同一走查裡把觀測回應切到失敗（各一次 Unavailable、Stale）再做選縣。不要求 #38 重做 AC-V2-08 的其餘部分（四類可辨、Taiwan-wide 面板、(c)(d)、無標記、Forecast 可見、375 截圖集合），那些由 #37 結案 evidence 承接。
4. **(B) 會讓 derivation record 自身留下 coverage 缺口。** E-7：DEG-2 的「縣界互動」與「脈絡」部分、OBS-10 在 County 脈絡上的適用，在 §15.3 沒有實作責任票；#37 body 明寫由 #38 承接卻未寫進 #38。修正它是 Ticket derivation 的修訂（治理 §5.3 第 2 類），屬 DA 權責。
5. **附帶語義問題屬 §3.6-A，不是設計、不是 contract change。** 第 4.2 節說明既有來源（R-V2-OBS-6、OBS-5、OBS-10(a)、OBS-4(c)、DD-5 的脈絡、INV-V2-5／H-3）只有一種一致的解讀：Unavailable 下沒有有效測站集合可計數，脈絡的計數與極值是缺值 → 「—」；DD-5 的「0」只適用於存在 Latest Observation 而該縣在其中沒有有效測站。沒有任何一方主張相反解讀；就算視為兩種解讀，選擇也只影響 #38 的呈現，不改任何 OC 條款（§3.6-A 第二種情形同樣成立）。
6. **#37 沒有缺陷、不重開。** 互動圖層在 #37 subject 上不存在是垂直切片與依賴圖（#38 不依賴 #37）的必然結果；#37 R1 對可觀察部分的 PASS 與 CLOSURE 維持。

**未採用 (B) 的理由**：它只保證「最終會被看到」，不保證「在引入它的變更被審查時被看到」；治理 §4.1／§3.8 要求後者。**未採用的第三種做法**：把整條 AC-V2-08 改分配給 #38 或 #41 重做——違反 TB-V2-4，且讓 #37 已結案的 evidence 被無謂重複。**未採用的第四種做法**：修改 SPEC-V2 v2.2 的 R-V2-DD-5 文字——不必要：既有條款合起來已唯一決定行為，decision record 即為 §3.6-A 要求的持久 clarification；改 Spec 文字會觸發版本變更而無語義增益。

## 4. 裁決（DV-21）

1. **Issue #38 是 AC-V2-08(a)(b)「縣界互動圖層與 County 脈絡在 Stale／Unavailable 下」部分的 Ticket 層 owner**，同時是 **R-V2-DEG-2（縣界互動與脈絡部分）、R-V2-OBS-10(a)「縣界可見」（互動圖層部分）與 R-V2-OBS-6（County 脈絡欄位）**的實作責任票；#38 對 **INV-V2-7** 成為觀測失敗面（縣界互動與脈絡）的責任票之一。#38 的驗證分配依第 4.1 節擴充。
2. **County 脈絡在 Unavailable／Stale 下的內容依第 4.2 節**（既有條款的 clarification；不新增 R／AC／INV／oracle）。
3. **Spec Integration Audit 仍是 AC-V2-08 整條與 INV-V2-7 的 Spec 層 owner**（Spec §6.4；治理 §4.7），對整合後的最終 subject 核對 AC-V2-08 全部（含 #39 資訊面與 #40 Radar 之後的 Stale／Unavailable 行為）。此義務不變、不被豁免；但它**單獨不足以**作為 Ticket 層 owner（第 3 節第 1、2 點）。
4. **#37 的分配、evidence 與結案不變。** #37 R1 的 R-1 由本紀錄解決；Reviewer 不需補記。#37 對 AC-V2-08／R-V2-DEG-2 的義務範圍確認為「#37 subject 上可觀察的全部部分」。
5. **#39、#40 不新增分配。** #39 的 375 px 資訊面承載 County 脈絡（AC-V2-14 已含 stale、unavailable、選縣、選測站截圖）；#40 的 Radar 狀態獨立（R-V2-DEG-4）。若兩票的變更破壞第 4.2 節的行為，屬其 Ticket audit 的 regression finding 或 Spec Integration Audit 的整合 finding，不需事先分配。
6. **#41 不新增分配。** #41 既有的 R-V2-DOC-3／AC-V2-21(14) 義務（V2 驗收文件逐條對應 AC-V2 並引用各票證據）自然涵蓋：AC-V2-08 的證據引用 #37 R1／worklog（Taiwan-wide 面）與 #38 R1／worklog（縣界互動與脈絡面）。
7. **其他一律不變**：AC-V2-08、R-V2-DD-5、R-V2-DEG-2、R-V2-OBS-6／10 的文字、PASS 條件、FAIL 例、證據類別；#38 的「What to build」（縣界互動圖層與 County 脈絡本來就是 #38 的範圍；「在觀測失敗下維持可用、缺值顯示『—』」是 Spec 對整合產品既有的 MUST）；§6.2 的必要截圖集合；沒有新增任何 R／AC／INV／oracle。

### 4.1 #38 追加的驗證分配（逐字可引用；Orchestrator 於 #38 派工與 ticket 索引引用本節）

> **AC-V2-08(a)(b)（縣界互動圖層與 County 脈絡在 Stale／Unavailable 下的部分；decision DV-21）**——在 #38 的 subject 上，以 AC-V2-08 既有的證據方式（瀏覽器模擬：攔截／替換 `/api/` 觀測回應以觸發失敗；工具 HOW）驗證下列三項：
>
> **(1) Unavailable**（首次載入觀測失敗；四類之一即可）：帶縣名屬性的縣界互動圖層（R-V2-DD-4）可見；指標 hover 仍突顯該縣並顯示縣名；分別以縣界點選與 R-V2-DD-9(a) 的不經地圖鍵盤路徑各選取一個縣 → County 脈絡（R-V2-DD-5(b)）顯示縣名（來自圖層屬性），而有效測站數、上圖數（若顯示）、最高與最低測站的名稱／值一律為「—」——**MUST NOT 顯示 `0` 或任何數值**（R-V2-OBS-6；DV-21 §4.2）；測站清單不列任何測站、不以預報或其他來源填充（R-V2-MODE-6(c)）；Unavailable 狀態、類別原因與 `Refresh`（R-V2-OBS-10(a)）在選縣後仍可見可用（位置 HOW）；`Back to Taiwan`（R-V2-DD-8）可用並清除選縣；仍在 Now mode。之後 Refresh 成功 → 若脈絡仍顯示，其內容等於新回應對該縣的有效測站（是否保留選縣屬 HOW）。無測站可納入視野時 R-V2-DD-5(a) 的視野調整行為屬 HOW，只須地圖仍可用。
>
> **(2) Stale**（成功後 Refresh 失敗；選縣發生在失敗之前與之後各驗一次）：County 脈絡的有效測站數、最高／最低測站、測站清單與失敗前完全相同，且等於保留的上一次成功回應對該縣的手算值（R-V2-OBS-10(b)「保留上一次有效資料」）；Stale 標示與原因（R-V2-OBS-10(b)(e)）在 County 脈絡顯示中仍可見（位置 HOW）；hover、選另一縣、測站清單選取、`Back to Taiwan`、`Refresh` 皆可用；之後 Refresh 成功（newer 或 not-newer）→ Stale 清除、脈絡等於目前顯示資料（R-V2-OBS-10(c)、R-V2-OBS-8）。
>
> **(3) 無資料 vs 零（H-3）**：若樣本或 #38 的衍生樣本含一個在成功回應下零有效測站的縣（AC-V2-10「若樣本有」），對照該縣在 success 下顯示 `0` 與「—」（R-V2-DD-5 末句）與 (1) 在 Unavailable 下顯示「—」，兩者在畫面上可辨（Unavailable 有狀態標示，success 無）；若沒有這樣的縣，記明並只驗 (1)。
>
> **PASS**：(1)(2)(3) 全部成立。**FAIL 例**：Unavailable 下縣脈絡顯示「0 個有效測站」或任何數值；Stale 下選縣後 Stale 標示消失；觀測失敗後縣界 hover／點選／鍵盤選縣失效；脈絡以預報值填充。**證據**（依 AC-V2-08 證據欄，不新增類別）：瀏覽器模擬走查紀錄（狀態、選縣路徑、脈絡各欄位讀數與手算對照）；截圖至少兩張（桌機 1280：Unavailable＋選縣脈絡；Stale＋選縣脈絡）；375 以走查紀錄與讀數為證（底部資訊面 outcome 由 #39；§6.2 的必要截圖集合不變）。Executor self-verification 記入 `worklog/issue-38.md`；**#38 R1 Reviewer 獨立重做**。AC-V2-08 的其餘部分（Taiwan-wide 面板、四類可辨、(c)(d)、無標記、Forecast 可見、375 stale／unavailable 截圖）已由 #37 結案 evidence 承接，#38 不重做；#38 R1 依治理 §4.4 的變更風險核對 #37 的瀏覽器檢查未被 #38 的變更破壞（重跑即可，不重做 #37 的完整 evidence）。
>
> **R-V2-DEG-2（縣界互動與 County 脈絡部分）、R-V2-OBS-10(a)「縣界可見」（互動圖層部分）、R-V2-OBS-6（County 脈絡欄位）、INV-V2-7（觀測失敗面：縣界互動與脈絡）**——#38 的實作 MUST 使縣界互動圖層與 County 脈絡在 Stale／Unavailable 下依 DV-21 §4.2 行為；機制屬 HOW。

上段只引用 SPEC-V2 v2.2 既有條款並限定 #38 承接的部分（TB-V2-1 的「範圍說明」形式）；(1) 的「MUST NOT 顯示 `0` 或任何數值」是 R-V2-OBS-6 既有 oracle（「永不顯示為數值」）對 County 脈絡欄位的直接適用，不是新的 oracle；(2) 的「Stale 標示仍可見」是 R-V2-OBS-10(b)(e) 狀態層級義務的直接適用。

### 4.2 County 脈絡在 Unavailable／Stale 下的內容（既有來源的唯一合理解讀；治理 §3.6-A 第一種情形）

1. **R-V2-DD-5 末句的適用範圍。** 「零有效測站的縣可選取：脈絡顯示 0 與『—』，不是錯誤」適用於**存在可顯示的 Latest Observation（success 或 stale）而該縣在其中沒有有效測站**的情形。它來自 D-9／P-7～P-10：某些縣（例如離島）在某一小時可能沒有有效站，這不是錯誤。「0」是對一個實際存在的有效測站集合（R-V2-OBS-2、OBS-5 定義於「一次上游取得」）計數的結果。
2. **Unavailable 下沒有集合可計數。** Unavailable ＝「沒有可顯示的有效 Latest Observation」（R-V2-OBS-10(a)；BRIEF §9）。此時 County 脈絡的有效測站數、上圖數、最高／最低測站與清單都是**缺值**，依 R-V2-OBS-6「任何缺值…MUST 顯示為『—』，永不顯示為數值」顯示為「—」。這與 R-V2-OBS-4(c)（Unavailable 下兩個時間欄位存在、值「—」）及 R-V2-DD-10 的 Taiwan-wide 有效測站數同一處理方式。
3. **為何不是「0」。** 把「沒有資料」呈現為「該縣 0 個有效測站」會把資料缺席冒充為觀測結果：違反 R-V2-OBS-10(a)「明確的 Latest Observation unavailable 狀態」、H-3「值是否誠實標示」與 INV-V2-5。OC 自身在 dataset 層已把「零有效測站」定為失敗而非資料（AB-V2-3；R-V2-OBS-5 → `invalid_response` → Unavailable／Stale）；county 層在沒有 dataset 時更不可能以 0 為資料。
4. **縣名照常顯示。** 縣名來自 R-V2-DD-4 的圖層屬性，不是觀測資料；hover 突顯、縣名、選取、`Back to Taiwan`、R-V2-DD-9(a) 鍵盤路徑在 Unavailable／Stale 下皆維持可用（R-V2-DEG-2「縣界互動…維持可用」）。
5. **Stale。** County 脈絡 ＝ 保留的上一次成功資料對該縣的內容（R-V2-OBS-10(b)「保留上一次有效資料」；脈絡是「資料」的一種呈現）；Stale 標示與原因是狀態層級義務（10(b)(e)），與選取狀態無關——選縣不得使 Stale 標示消失，否則使用者會把舊的縣資料當成新的（使用者故事 4）。之後成功的 Refresh 清除 Stale 並依 R-V2-OBS-8 更新脈絡。
6. **HOW 保留給 #38。** 脈絡欄位在 Unavailable 下的版面（是否收合、是否合併顯示 Unavailable 告示）、Stale 標示在脈絡中的位置、無測站時的視野調整、Refresh 成功後是否保留選縣，皆為 HOW；只須滿足上述 1–5 與 R-V2-RSP-6（選取項與關鍵控制可見可達）。

## 5. 是否改變 accepted 語義：**否**

- **Outcome Contract**：S-4（County 脈絡內容）、S-6（Unavailable／Stale 定義；「地圖與縣界可見」）、S-7（觀測失敗只影響 Now mode）、AB-V2-3「零有效測站＝失敗」、AB-V2-4、AB-V2-5、AB-V2-6 的文字與語義不變；縣界互動與脈絡在失敗狀態下的行為是 S-4 與 S-6／S-7 三個已接受 outcome 的交集，早已在 acceptance boundary 內（AB-V2-4、5、6 皆分配給 SPEC-V2，derivation §4）。
- **Derived contract**：SPEC-V2 v2.2 文字不變；沒有新增、刪除或弱化任何 R／AC／INV／oracle／證據類別；AC-V2-08 的 PASS 條件與 FAIL 例逐字維持；R-V2-DD-5 末句不改、只釐清其適用範圍（第 4.2 節第 1 點）。
- **變更性質**：只修正 Ticket 的驗證分配與實作責任分配（治理 §5.3 第 2 類；與 DV-20 與 §14「Tickets（V2）依賴圖修正」同類），加一份 §3.6-A clarification。不改 #38 的「What to build」。
- **Boundary determination**：本裁決所涉的 derived-contract 修訂與 clarification 在 V2 Outcome Contract boundary 內；**不需 acceptor**；沒有 fail-closed 路徑。

## 6. 受影響 work items 與 evidence

| 對象 | 影響 |
| --- | --- |
| **#37**（已結案） | 無。分配、evidence、CLOSURE 不變；R1 的 R-1 由本紀錄解決。 |
| **#38**（待執行；READY） | 驗證分配擴充（第 4.1 節）；實作責任加 R-V2-DEG-2（縣界互動與脈絡部分）、R-V2-OBS-10(a) 互動圖層部分、R-V2-OBS-6（脈絡欄位）、INV-V2-7（觀測失敗面）；Work Contract 引用第 4.2 節。Ticket body 的修改與派工由 Orchestrator 執行（第 7 節）。#38 的 R1 audit record 須對第 4.1 節 (1)(2)(3) 逐項 PASS／FAIL，並依 decision A-1 在 H-3 核對段記「無資料 vs 零」的核對。#38 若修改 #37 結案的前端狀態程式（`applyObservationFailure`／`renderObsState` 等），屬 #38 契約內的變更，由 #38 R1 依 §4.4 核對未破壞 #37 的 audited guarantees。 |
| **#39、#40**（待執行） | 不新增分配（第 4 節第 5 點）。 |
| **#41**（待執行） | 不新增分配；既有 R-V2-DOC-3／AC-V2-21(14) 的對照把 AC-V2-08 引用到 #37 與 #38 兩處 evidence（第 4 節第 6 點）。 |
| **Spec Integration Audit** | 義務不變（Spec §6.4；治理 §4.7；derivation §6 A-2 的 INV-V2-5／H-3 逐項核對含本紀錄第 4.2 節）；核對 AC-V2-08 與 INV-V2-7 時預期在 #37 R1 與 #38 R1 兩份 record 找到 Ticket 層 evidence。 |
| **derivation-SPEC-V2.md** | §15.2 #38 列、§15.3 AC 表 08 列、§15.3 INV 表 7 列、§15.3「R-V2 群組覆蓋」OBS／DEG 列、§15.3「缺口」段 AB-4／AB-5 與 §14 修訂紀錄依本紀錄同步（DA 於本次一併以最小修改更新；只加不減）。 |
| **`doc/ticket/tickets-v2.md`** | 「實作過程中的調整」段由 Orchestrator 補一列引用本紀錄（索引由派工者維護）。 |
| **既有 evidence** | #35、#36、#37 的 audit records、worklogs、截圖、network log 全部沿用；沒有任何既有 evidence 因本裁決失效。 |
| **Dependencies** | 依賴圖 7 條邊不變；#38 仍只 blocked by #36。#38 的 Executor 以 #37 已結案的 subject（`7a3b469` 之後的 branch HEAD）為 BASE 是排程事實（並行度 1、偏好順序），不是新 edge。 |

## 7. Orchestrator／tracker 動作（本紀錄指定；DA 不執行）

1. **Issue #38 body（`gh issue edit 38`）**，只改下列三處、其餘逐字不變（以 diff 證明）：
   - 「Acceptance criteria」清單加一行：`- [ ] AC-V2-08(a)(b)（縣界互動圖層與 County 脈絡在 Stale／Unavailable 下的部分——依 decision DV-21 \`home_work_01/doc/governance/decisions/decision-20260926-county-layer-under-stale-unavailable-allocation.md\` §4.1；County 脈絡在 Unavailable 下缺值顯示「—」、不得顯示 0 或任何數值，依 DV-21 §4.2；其餘部分已由 #37）`。
   - 「Traceability」的 **R** 列加 `R-V2-DEG-2（縣界互動與脈絡部分）；R-V2-OBS-10(a)（縣界可見，互動圖層部分）；R-V2-OBS-6（County 脈絡欄位）`；**AC** 列加 `08(a)(b)（縣界互動與脈絡部分）`；**INV** 列加 `INV-V2-7（觀測失敗面：縣界互動與脈絡）`；**AB** 列加 `AB-V2-4（部分）、AB-V2-5（部分）`。
   - 「Spec／worklog」的 Decisions 列加本紀錄路徑（DV-21）。
2. **`doc/ticket/tickets-v2.md`**：「實作過程中的調整」段加一列：2026-09-26，DV-21（本紀錄路徑；來源 #37 R1 的 routing signal R-1），#38 追加 AC-V2-08(a)(b) 縣界互動圖層與 County 脈絡在 Stale／Unavailable 下的部分、R-V2-DEG-2／OBS-10(a)／OBS-6 對應部分與 INV-V2-7 觀測失敗面；County 脈絡在 Unavailable 下缺值為「—」、不得顯示 0（DV-21 §4.2）；Spec Integration Audit 仍為 AC-V2-08 的 Spec 層 owner；#37 分配與結案不變；不改 accepted 語義（治理 §5.3 第 2 類）。
3. **#38 派工**：Executor 與 R1 的 bounded pack 皆列入本紀錄路徑，並引用第 4.1 節與第 4.2 節；不改派工的其他內容。#38 High-risk 段既有的 H-3 標示已涵蓋，不需改動；R1 record 的 A-1 H-3 核對段須含「無資料 vs 零」。
4. **Run record**：在 checkpoints／routing 記本次 DA 派工結果（R-1(#37) resolved by DV-21）與 DA binding 核對（Bindings §3.4）。
5. **Commit**：本紀錄與 `derivation-SPEC-V2.md` 的最小修改依 SA-1 由派工者原樣 commit（`doc/governance/**` record-only）。

## 8. Evidence（DA 自行執行，全部唯讀；未讀取 `.env`、未使用任何金鑰、未呼叫 CWA）

- 讀取：Bindings b3 全文；治理 §1.2、§1.5、§2.1、§2.3、§2.4、§3.1、§3.3–§3.8、§4.1–§4.7、§5.1–§5.4；`SPEC-V2.md` 全文（§0–§10，含 §2.1 MODE、§2.2 OBS-2／4／5／6／10、§2.3 DD-1～11、§2.5 DEG-1～5、§3 AC-V2-01～23、§4 INV-V2、§5.3、§6.1–§6.4、§7）；`derivation-SPEC-V2.md` 全文（§1–§15）；`issue-37-c1-r1.md` 全文；DV-20 全文；`decision-20260923-high-risk-categories.md` §2.3 H-3 與 §3 A-1～A-5；OC-V2 §2.4 列 7、§2.5 S-4／S-6／S-7、§3 AB-V2-3～6（grep）；BRIEF-V2 §9 Stale／Unavailable 詞條（grep）；`tickets-v2.md` 全文；run record「Work item status」與 2026-09-26 各 checkpoint（含 #37 R1 checkpoint 的 R-1(#37) 派工敘述）；`gh issue view 37`（CLOSED）與 `gh issue view 38`（OPEN，label `ready-for-agent`，已含 DV-20 追加）。
- 實作 grounding（只讀）：`static/app.js:167`（`obsState` 初值）、`:595-600`、`:687-688`、`:723-737`（`applyObservation` 設 `success`；`applyObservationFailure` 設 `obs ? "stale" : "unavailable"`，不動 `obs`）、`:763-778`（`renderObsState`）、`:796`（無 `obs` 時有效測站數 `MISSING`）。
- Git（read-only）：HEAD `040324b905f0b3d0897c4163cff28ea9de2abbcc`（`home_work_01-v2-implementation`）；`git status --porcelain` 只有既存的工具殘留 `grep.exe.stackdump`；`grep -r "DV-21" home_work_01/` 於寫入前為 0 命中（編號未被占用）。
- 寫入：本紀錄（新增）；`derivation-SPEC-V2.md` §15.2 #38 列、§15.3 AC 表 08 列、§15.3 INV 表 7 列、§15.3「R-V2 群組覆蓋」OBS／DEG 列、§15.3「缺口」段、§14 新增一列（Edit 局部修改）。未修改 SPEC-V2、OC-V2、任何 audit record、worklog、實作或測試；未 commit（派工者依 SA-1 處理）；未動 GitHub Issue。
- 產出不含任何金鑰格式字串。
