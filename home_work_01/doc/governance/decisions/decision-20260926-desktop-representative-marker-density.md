# Decision record — 桌機全臺視野的代表標記與密度管理（R-1(#39)；`home_work_01/`）

- **紀錄類型**：Design Authority decision record（治理 §3.6-A：在不改變任何 accepted 語義的前提下裁決；治理 §2.4「Contract 語義是否足夠、material ambiguity」；治理 §5.3 第 2 類「不改變 accepted 語義的 derived contract clarification」，須記錄對進行中工作、dependencies 與既有 evidence 的影響）。本紀錄是 R-V2-DD-2／DD-3 與 R-V2-RSP-7／RSP-3 合讀的 **clarification**，作為 #39 Work Contract 的引用；不修改 Ticket 分配（#39 已是 R-V2-RSP-1～8 與 AC-V2-14 的 owner）。[`derivation-SPEC-V2.md`](derivation-SPEC-V2.md) §14 以參照引用本紀錄。
- **編號**：**DV-22**（延續 DV-1～DV-19、[DV-20](decision-20260926-ac-v2-01-county-round-trip-allocation.md)、[DV-21](decision-20260926-county-layer-under-stale-unavailable-allocation.md)）
- **日期**：2026-09-26
- **來源**：Issue #39 cycle 1 R1 audit record [`../audit/issue-39-c1-r1.md`](../audit/issue-39-c1-r1.md) §3 R-V2-RSP-7 列／§9 routing signal **R-1**（治理 §4.2：契約語義問題是 routing signal，不是 blocking finding；R1 的 VERDICT BLOCKING 來自 F-1，與本問題無關）；由 Orchestrator 依治理 §2.4 派工，run record [`../run/run-20260925-hw01-v2-formal.md`](../run/run-20260925-hw01-v2-formal.md)（2026-09-26 #39 R1 checkpoint）。
- **相關契約**：V2 Outcome Contract（ACCEPTED 2026-09-25，normative candidate `69c5a04`）§1、§2.2 V2 Core (a)、§2.5 **S-4**（「Taiwan-wide 視野每縣至多一個代表性有效測站…**中間縮放層級**的密度管理屬 HOW」）、**S-10**（「可見標記在驗證視野下可讀可選，密度管理不得使地圖不可用…**不要求 375 px** 全臺視野同時顯示 22 個代表 pill」）、S-8、§3 **AB-V2-6**、**AB-V2-8**；SPEC-V2 **v2.2** User Story 1、**R-V2-DD-2**、**R-V2-DD-3**、R-V2-DD-4、R-V2-DD-9(a)(d)(e)、R-V2-MAP-2、R-V2-MAP-4、R-V2-RSP-1、**R-V2-RSP-3**、R-V2-RSP-6、**R-V2-RSP-7**、AC-V2-10、AC-V2-11、**AC-V2-14**、§5.2（「密度管理（中間縮放層級的聚合／隱藏）」）、§5.3（44×44 儀器）、§6.2；derivation record §3.1 B-4、B-8、B-20、§3.2 DV-9、DV-11、§15.2／§15.3（RSP-1～8、AC-V2-13／14／15 → #39）、TB-V2-6；BRIEF-V2 §6「其他被接受的 outcome」、§10（「密度管理」列為 HOW）；Issue **#39** body（DA 於 2026-09-26 以 `gh issue view` 讀取）；治理 §1.2、§3.3、§3.4、§3.6、§4.2、§5.3。
- **參考 subject**：branch `home_work_01-v2-implementation` HEAD `b94d39d9c7346dfc765a09e4553b6523806e578e`（#39 code anchor `ae0b9dc`，BASE `4651d33`）。`static/app.js:217-228`（`DENSITY_PRIORITY`、`TOUCH`）、`:1146-1229`（`updateMarkerAccess`、`densityRank`、`markerBox`、`overlaps`）、`:2100`（`map--labels-hidden` 於 zoom < 8）、`static/styles.css:823`、`:1009`（`is-culled`）只作機制 grounding，不作為設計依據。
- **執行角色**：`gov-design-authority`（Bindings §3.1 `design_authority`；binding 核對由派工者依 Bindings §3.4 記入 run record）。
- **效力**：自本紀錄寫入起，第 4.2 節是 R-V2-DD-2／DD-3 與 R-V2-RSP-7／RSP-3 對「全臺視野代表標記的顯示」的 clarification，第 4.1 節是 #39 在 F-1 targeted correction 後的 subject 上 MUST 滿足並由 R2 核對的義務；SPEC-V2 文字不變（仍 v2.2）；#39 的分配不變；#36、#37、#38 的分配、evidence 與結案不變、不重開；Spec Integration Audit 的義務不變。本紀錄不修改任何實作或測試。

## 1. 問題

#39 的 subject 在桌機驗證視野（1280；Reviewer 另量 1920）的 Now mode 初始全臺視野（R-V2-MAP-4，zoom 7）只顯示 **9／22** 個代表標記（臺北市、臺中市、嘉義縣、高雄市、花蓮縣、臺東縣、澎湖縣、金門縣、連江縣），其餘 13 縣的代表標記被密度規則隱藏（放大即出現；375 px zoom 6 為 5／22）。BASE（#38 結案）三個尺寸皆顯示 22／22，但北部代表標記互相重疊、部分文字不可讀（#36 R1 §8 交接 (b)，明列為 R-V2-RSP-7 事項交 #39）。

Spec 對「不要求同時顯示 22 個代表標記」的明文放寬只寫 375 px（R-V2-RSP-7；OC S-10）；「密度管理屬 HOW」在 OC S-4 與 Spec §5.2 都限定於「中間縮放層級」；R-V2-DD-2 寫「每縣**至多**一個代表性有效測站的標記」。R1 提出兩種讀法：**A**（Executor）——密度管理在任何縮放層級皆屬 HOW，375 一句只是舉例；**B**——只有 375 被放寬、HOW 只限中間縮放層級，桌機全臺初始視野應顯示每個有有效資料的縣之代表標記（與 User Story 1 一致）。

需裁決：桌機初始全臺視野隱藏部分代表標記是否在 accepted 契約內；R-V2-DD-2／DD-3 是否蘊含桌機必須顯示全部 22 縣的代表標記；並給出 #39 F-1 修正必須滿足的精確規則。

## 2. 事實（依原始契約與紀錄，不採用 Executor／Reviewer 的結論）

| # | 事實 | 證據 |
| --- | --- | --- |
| E-1 | OC §2.2 V2 Core (a)：「Taiwan-wide 視野每縣至多一個代表性有效測站」是 scope 項目。S-4：同句＋「選取／後備機制屬 HOW，但必須確定性、只依有效現行測站、有文件、可客觀驗證；Spec 不列舉 StationId。**中間縮放層級**的密度管理屬 HOW。」 | OC-V2 §2.2、§2.5 S-4 |
| E-2 | S-10（P-29～P-31）：「可見標記在驗證視野下可讀可選，密度管理不得使地圖不可用，縣下鑽後該縣測站皆可到達，**不要求 375 px 全臺視野同時顯示 22 個代表 pill**」。AB-V2-8 承接 S-10 與 44×44。 | OC-V2 §2.5 S-10、§3 AB-V2-8 |
| E-3 | 接受的文字中「22 個代表 pill 同時顯示」只以**非需求**的形式出現（S-10 的 375 放寬；S-8／R-V2-MAP-2 的「不要求…22 縣市同時在視窗內」，後者是視窗圍欄而非標記）；沒有任何條款以 MUST 要求某視野同時顯示 22 個代表標記。 | OC-V2 §2.5 S-8、S-10；SPEC-V2 R-V2-MAP-2、R-V2-RSP-7 |
| E-4 | R-V2-DD-2：「每縣至多一個代表性有效測站的標記，標記顯示該站氣溫；該站的測站名與縣名 MUST 可由 hover、選取或面板取得…無有效測站的縣 MUST 沒有代表標記（不是失敗）。」R-V2-DD-3：代表測站規則的性質（確定性、只依有效站、後備、README 可手算、可離線驗證、不列 StationId）。AC-V2-11：「每縣 ≤ 1 站且皆為有效站…零有效的縣無代表」。DD-2／DD-3／AC-V2-11 定義的是代表測站**集合**（成員資格），不含任何縮放層級或視窗條件。 | `SPEC-V2.md:144-145`、`:244` |
| E-5 | R-V2-RSP-7：「在驗證視野下，每個**可見**標記的文字 MUST 可讀且標記可選取；密度管理（HOW）MUST NOT 使地圖不可拖曳、不可縮放或不可選取；375 px 全臺視野不要求同時顯示 22 個代表標記，但被顯示者須滿足本條，且選縣仍有 R-V2-DD-9(a) 的路徑。」R-V2-RSP-3：測站／代表標記的可點區 MUST ≥ 44×44 CSS px。§5.2 HOW：「密度管理（中間縮放層級的聚合／隱藏）」。 | `SPEC-V2.md:188,192,297` |
| E-6 | 兩個驗證視野（RSP-1）都是 1280 與 375；RSP-7「每個可見標記」的「可見」一詞在兩個視野下同義。AC-V2-14 的 PASS 條件含「44×44 對列出的控制與標記以 DOM 量測 PASS」與「R-EN-1 六項對 V2 介面逐項 PASS」；AC-V2-10／11／14 沒有任何一條以「桌機全臺視野顯示 N 個代表標記」為 PASS 條件；AC-V2-11 只要求 Reviewer 對 ≥ 3 縣手算並與 `/api/`／畫面一致。 | `SPEC-V2.md:186,243-244,247` |
| E-7 | BASE（`4651d33`）在 1280 與 375 的全臺初始視野「北部代表標記互相重疊（截圖可見，部分文字不可讀）」，#36 R1 判為 #39 的合法分配並交接為 R-V2-RSP-7 事項；#38 R1 §7 第 1 點另量得初始視野多數縣多邊形被代表標記覆蓋（F-2，交 #39／SIA）。BASE 的 22／22 因此**不是**符合 RSP-7／RSP-3 的已接受呈現。 | `issue-36-c1-r1.md` §4 關切 3、§8 交接 #39 (b)；`issue-38-c1-r1.md` §7、F-2 |
| E-8 | 幾何事實（DA 以 Web Mercator 計算）：zoom 7 每經度 ≈ 91 CSS px，25°N 每緯度 ≈ 100 px；44 px 的最小可點區 ≈ 0.48° ≈ 48 km。北部六縣市（臺北、新北、基隆、桃園、新竹市、新竹縣）的代表測站彼此相距約 0.05–0.3°（5–30 px），西部沿海各縣代表測站相距多在 20–45 px。在 zoom 7 把 22 個代表標記放在測站位置上，**不可能**同時滿足 RSP-3 的 44×44 不重疊與 RSP-7 的可讀；R1 觀察的 9／22（1280）與 5／22（375，zoom 6）是此幾何限制下的結果。 | DA 計算；`issue-39-c1-r1.md` §9 R-1 |
| E-9 | 機制 grounding（只讀）：subject 的碰撞框 ＝ 氣溫 pill 擴大到至少 44×44（`markerBox`），名稱標籤只在有顯示時才計入；而名稱標籤在 zoom < 8 一律隱藏（`map--labels-hidden`），所以桌機初始視野（zoom 7）與 375（zoom 6）的隱藏完全由 RSP-3 的 44×44 儀器（＋2 px 間距）決定，不由任何可選裝飾決定。隱藏的標記保留 DOM 與位置、不可點、不是 Tab 停駐點，放大即出現；排名為選取站、焦點站、其後 22 縣固定順序（README 已記載）。 | `app.js:217-228,1146-1229,2100`；`styles.css:823,1009`；README「Marker density」 |
| E-10 | 契約沒有任何條款提及、要求或禁止「把標記自測站位置位移（leader line、fan-out）」；Spec §5.2 把密度管理的 HOW 描述為「聚合／隱藏」。DD-4 要求縣多邊形可 hover／點選；#38 R1 F-2 已指出代表標記覆蓋多邊形的問題（位移會擴大此問題）。 | SPEC-V2 §5.2、R-V2-DD-4；`issue-38-c1-r1.md` F-2 |
| E-11 | #39 owns R-V2-RSP-1～8、AC-V2-13／14／15；#40 的 Radar overlay 在標記之下（R-V2-RAD-6），不依賴代表標記數；#41 只彙整文件與驗收。本問題的裁決只影響 #39 的產品切片與其驗證。 | derivation §15.2、§15.3 |
| E-12 | OC S-4／S-10、AB-V2-6／AB-V2-8 的文字在本裁決中不需改動，也沒有任何一方主張改動。 | OC-V2 §2.5、§3 |

## 3. 讀法與對照

三種候選讀法：

- **A（寬）**：密度管理在任何縮放層級、任何視野皆屬 HOW；桌機全臺視野顯示多少縣由實作決定，只受 RSP-7「顯示者可讀可選、地圖可用」約束。
- **B（嚴）**：桌機全臺初始視野 MUST 顯示每個有有效資料的縣之代表標記（22／22）；密度管理只能作用於中間縮放層級與 375。
- **C（有界）**：全臺視野的標記集合就是代表測站集合（DD-2／DD-3；每個有有效測站的縣恰一個），這是契約自己為全臺視野選定的密度設計，不受 HOW 裁量；該集合在某視窗／縮放下的**呈現**受 RSP-7／RSP-3 約束——只有在兩個代表標記於當前縮放無法同時滿足 44×44 不重疊與可讀時，才可以隱藏其中一個；隱藏必須是最小的（只隱藏碰撞者）、確定性的、有文件的、放大即恢復，且被隱藏縣仍可經 DD-4 與 DD-9(a) 選取。375 的明文放寬表示在 375 顯示數不是 oracle；桌機沒有放寬，表示桌機的顯示數受此「只因碰撞」規則保護。

對照契約與治理：

1. **A 使兩個限定語失效。** OC S-4 與 Spec §5.2 都把密度管理的 HOW 限定在「中間縮放層級」；S-10／RSP-7 把「不要求 22 個同時顯示」限定在 375。若任何視野的密度都屬 HOW，這兩個限定語都成為贅文，且 S-4「Taiwan-wide 視野每縣至多一個代表性有效測站」作為 V2 Core 的 scope 項目可被實作掏空（原則上可只顯示一縣）。解讀 accepted 文字時應使每一句都有效，A 不符。
2. **B 只能靠契約未載的設計成立，否則與明文 MUST 衝突。** E-8：zoom 7 下 22 個代表標記放在測站位置上不可能同時滿足 RSP-3（44×44）與 RSP-7（可讀）——BASE 的 22／22 正是以違反 RSP-7 為代價（E-7），而 RSP-3／RSP-7 都是 acceptor 接受的 MUST（S-10、AB-V2-8）。B 要成立只有兩條路：(i) 讓標記位移離開測站位置（leader line 等）——契約沒有這種設計（E-10），DA 把它寫成 MUST 即是新增 requirement（治理 §5.3 第 1 類）；(ii) 犧牲 44×44 或可讀——弱化 accepted AC。兩者 DA 都不得為之。此外 B 所依據的「22」在 accepted 文字裡只以非需求形式出現（E-3），沒有一條 AC 以它為 PASS 條件（E-6）；把它升為桌機 oracle 是新增 AC。
3. **C 讓每一句都有效，且不新增、不弱化。** 代表集合由 DD-2／DD-3 決定（成員資格），呈現由 RSP-7／RSP-3 決定（可讀、44×44、可用），375 放寬使 375 的顯示數不是 oracle，桌機的顯示數則以「只因碰撞才隱藏」受保護；「中間縮放層級」的 HOW 自由（聚合、隱藏、切換到全部測站）保留給全臺與縣視野之間的層級。acceptor 在 375 已接受「可讀優先於同時顯示 22」；C 只是把同一優先順序用於桌機上同型的幾何衝突，並要求隱藏最小化。
4. **DD-2／DD-3 是否蘊含桌機必須顯示全部縣的標記。** 不蘊含同時可見；蘊含集合完整。DD-2 的「至多一個」是每縣上限，其唯一內建例外是「無有效測站的縣沒有代表標記」；DD-3／AC-V2-11 對每個有有效站的縣恰選出一個。所以全臺視野的**圖層成員**必須是全部有有效站的縣各一個代表（實作不得以偏好省略某些縣），但 DD-2 沒有任何縮放或視窗條件，RSP-7 對 375 的放寬也證明契約把「圖層成員」與「某視窗下同時可見」分開處理。同時可見與否歸 RSP-7／RSP-3。
5. **BASE 不是基線。** E-7：BASE 的 22／22 在北部重疊、部分文字不可讀，是 #36 R1 交接給 #39 依 RSP-7 解決的事項，不是已接受的呈現；「回到 BASE」等於要求 #39 違反 RSP-7。
6. **User Story 1 的分量。** 「打開頁面就看到全臺各縣的最新測站氣溫」是 Spec 的 context，不是 R／AC；C 之下它仍實質成立：每縣的代表標記都在圖層中、有數縣因幾何衝突須放大一級才見，且各縣皆可 hover／點選／自選單選取。它不足以把「22 同時可見」升為 MUST。
7. **選擇的影響範圍。** E-11：只影響 #39 的產品切片與其驗證（F-1 修正、R2、SIA 對 RSP-7 的核對）；不建立 #40／#41 依賴的新設計基線；不涉及 scope、constraints 或 acceptance boundary 的變更。即使把 A／B／C 視為 §3.6-A 第二種情形（多種解讀），選擇也只影響本 work item，DA 有權裁決；不需 acceptor。

**未採用的做法**：修改 SPEC-V2 v2.2 的 R-V2-RSP-7 文字——不必要：既有條款合讀已唯一決定行為，decision record 即為 §3.6-A 要求的持久 clarification；改 Spec 文字會觸發版本變更而無語義增益。**未採用的做法**：fail-closed 至 acceptor——治理 §1.2 的 fail-closed 條件是「無法確立在 boundary 內」；A、B、C 都在 V2 OC boundary 內，本問題是語義釐清而非 boundary 或授權缺口；DA 依 §2.4 與 §3.6-A 自行裁決並記錄。

## 4. 裁決（DV-22）

1. **桌機初始全臺視野隱藏部分代表標記，在 accepted 契約內**——但只在第 4.2 節的界限內：隱藏只能是 R-V2-RSP-3（44×44）與 R-V2-RSP-7（可讀）於當前縮放下無法同時滿足時的碰撞處理，且必須最小、確定、有文件、放大即恢復、被隱藏縣仍可選取。**不採**讀法 A（任何視野任意隱藏）與讀法 B（桌機 MUST 22／22）。
2. **桌機初始視野 MUST NOT 被要求顯示全部 22 縣的代表標記**（as at BASE）：BASE 的 22／22 違反 RSP-7，不是基線；契約沒有以 MUST 要求任何視野同時顯示 22 個代表標記。
3. **R-V2-DD-2／DD-3 蘊含的是集合完整**（每個有有效測站的縣恰一個代表標記在全臺圖層中，實作不得以偏好省略某些縣），**不蘊含在每個視窗下同時可見**。同時可見歸 RSP-7／RSP-3，依第 4.2 節。
4. **#39 在 F-1 targeted correction 後的 subject 上 MUST 滿足第 4.1 節**；#39 R2 MUST 逐項核對第 4.1 節（依 AC-V2-14 既有證據類別）。#39 R1 對 R-V2-RSP-7「成立（依字面）」與 AC-V2-14 其餘各列的結論在本裁決下**維持**，不需重做；R2 只補第 4.1 節的核對。
5. **#39 的分配不變**（R-V2-RSP-1～8、AC-V2-13／14／15）；#36、#37、#38 的分配、evidence 與結案不變；#36 R1 交接 (b) 由 #39 依本紀錄處理。**#40、#41 不新增分配。**
6. **Spec Integration Audit 仍是 R-V2-RSP-7／AC-V2-14 的 Spec 層 owner**（Spec §6.4；治理 §4.7），對整合後的最終 subject（含 #40 之後）核對第 4.2 節仍成立；此義務不變、不被豁免。
7. **其他一律不變**：R-V2-DD-2／DD-3、R-V2-RSP-3／RSP-7、AC-V2-10／11／14 的文字、PASS 條件、FAIL 例、證據類別；§5.3 儀器；§6.2 截圖集合；沒有新增任何 R／AC／INV／oracle。

### 4.1 #39 F-1 修正後 MUST 滿足、R2 MUST 核對的義務（逐字可引用；Orchestrator 於 F-1 correction 派工、R2 派工與 ticket 索引引用本節）

> **R-V2-DD-2／DD-3 與 R-V2-RSP-7／RSP-3（全臺視野代表標記的顯示；decision DV-22）**——在 #39 F-1 修正後的 subject 上，於桌機 1280 的 Now mode 初始全臺視野（R-V2-MAP-4）與 `Back to Taiwan` 後，以 AC-V2-14 既有的證據方式（瀏覽器驗收清單＋DOM 量測；工具 HOW）驗證下列各項；375 同樣執行 (1)(2)(4)(5)，但依 R-V2-RSP-7 其顯示數不是 oracle：
>
> **(1) 集合完整**：全臺圖層的代表標記集合等於 `/api/` 回應的代表測站集合（AC-V2-11 的規則；每個有有效測站的縣恰一個，零有效的縣無），不因視窗或縮放而少任何縣；被隱藏者是否保留於 DOM 屬 HOW，但 MUST 不可點、不是 Tab 停駐點（R-V2-DD-9(e)）。
>
> **(2) 隱藏只因碰撞**：每一個在該視野被隱藏的代表標記，其**必要可點區**——氣溫 pill 的矩形擴大到至少 44×44 CSS px（R-V2-RSP-3；§5.3 儀器）——MUST 與至少一個**顯示中**代表標記的必要可點區重疊（實作若採用微小最小間距，例如 2 px，MUST 在 README 或 worklog 記載並一律適用）。沒有任何代表標記因為可選的名稱標籤、面板、版面偏好或其他非必要元素而被隱藏：可選元素與必要可點區碰撞時，由可選元素讓位，不隱藏標記。
>
> **(3) 顯示者合規**：顯示中的代表標記兩兩不重疊、文字可讀、可選取，可點區 ≥ 44×44（R-V2-RSP-7、RSP-3 既有檢查）。
>
> **(4) 確定性與文件**：同一觀測資料與同一視窗尺寸重複載入得到同一顯示集合；隱藏的優先順序在 README 記載（R-V2-DOC-1(8)；既有「Marker density」段即可，內容須與實作一致）。
>
> **(5) 被隱藏縣的可達性**：對每個代表標記被隱藏的縣，該縣多邊形 hover 突顯並顯示縣名、點選可選取（R-V2-DD-4）；`County` 選單可選取（R-V2-DD-9(a)）；以縮放放大到不再碰撞的層級時其代表標記出現並可選取（S-10「密度管理不得使地圖不可用」）。以 ≥ 3 個被隱藏縣抽驗（含北部至少一縣）。
>
> **PASS**：(1)～(5) 全部成立。**FAIL 例**：某縣有有效測站卻不在全臺圖層；某代表標記被隱藏而其必要可點區與任何顯示中代表標記都不重疊；顯示中兩個代表標記重疊或文字不可讀；被隱藏縣無法經 hover／點選／選單選取或放大後仍不出現；重複載入顯示集合不同。**證據**（依 AC-V2-14 證據欄，不新增類別）：瀏覽器驗收紀錄——1280 與 375 各一份：顯示中與被隱藏的代表標記清單、每個被隱藏者與其碰撞的顯示中標記的矩形讀數（DOM `getBoundingClientRect`）、抽驗縣的可達性走查；截圖沿用 §6.2 既有的桌機「Now mode 預設」一張（不新增集合）。1920 MAY 記錄為參考，不是 oracle（R-V2-RSP-1 的桌機驗收視野是 1280）。Executor self-verification 記入 `worklog/issue-39.md`；**#39 R2 Reviewer 獨立重做**（延續 R1 context，重讀修正後的檔案與 diff）。

上段只引用 SPEC-V2 v2.2 既有條款（DD-2／DD-3／DD-4／DD-9、RSP-3／RSP-7、AC-V2-11／14、§5.3、§6.2）並限定 #39 承接的部分（TB-V2-1 的「範圍說明」形式）；(2) 的「必要可點區 ≥ 44×44」是 R-V2-RSP-3 既有 oracle 的直接引用，「隱藏只因碰撞」是第 4.2 節 clarification 的可觀察形式，不是新的產品需求。

### 4.2 全臺視野代表標記的顯示規則（既有來源合讀的唯一一致解讀；治理 §3.6-A）

1. **圖層成員由 DD-2／DD-3 決定，不受 HOW 裁量。** 全臺視野的標記圖層 ＝ 代表測站集合：每個有 ≥ 1 有效測站的縣恰一個代表（DD-3 確定性規則；AC-V2-11），零有效的縣無（DD-2 末句）。這是契約自己為全臺視野選定的密度設計（相對於縣視野的「該縣全部上圖測站」）。實作不得以版面偏好、排名偏好或任何非碰撞理由把某縣排除在圖層之外。
2. **同時可見由 RSP-7／RSP-3 決定。** 在某視窗／縮放下，若兩個代表標記無法同時滿足「可點區 ≥ 44×44 且不重疊」與「文字可讀」，實作 MAY 以密度管理處理碰撞（聚合／隱藏屬 §5.2 的 HOW；位移不是契約要求也不被禁止，但採用時仍受 DD-4 與本節約束）。隱藏 MUST 是最小的：只隱藏與顯示中標記的必要可點區碰撞者；碰撞判定只以必要元素（氣溫 pill＋44×44 可點區）為準，可選元素（名稱標籤等）不得成為隱藏標記的理由。
3. **375 的放寬與桌機的差別。** S-10／RSP-7 的「不要求 375 px 全臺視野同時顯示 22 個代表 pill」表示在 375 顯示數不是 oracle（第 2 點的機制仍適用，但 Reviewer 不以顯示數判 FAIL）。桌機沒有此放寬：桌機的顯示數受第 2 點「只因碰撞」保護——每一個被隱藏的代表標記都必須能指出它碰撞的顯示中標記，否則 FAIL。
4. **中間縮放層級。** S-4／§5.2 的「中間縮放層級的密度管理屬 HOW」指全臺視野與縣視野之間的層級：實作可自由聚合、隱藏或改顯示全部測站，只受 RSP-7 的可讀、可選、地圖可用約束；本節第 1～3 點不限制中間層級的設計，但被隱藏的代表標記 MUST 在某個可到達的縮放層級出現（S-10「不得使地圖不可用」；DD-9(a) 路徑恆在）。
5. **可達性恆成立。** 不論是否隱藏，每個有有效測站的縣 MUST 可經 DD-4（hover／點選）與 DD-9(a)（不經地圖的選單）選取，其代表測站的名稱與縣名 MUST 可由 hover、選取或面板取得（DD-2）。
6. **確定性與文件。** 隱藏的排名與規則 MUST 確定（同輸入同結果）並在 README 記載（R-V2-DOC-1(8)），與 DD-3(a)(d) 對代表規則的要求同型；排名內容屬 HOW。
7. **BASE 不是基線。** BASE 的 22／22（北部重疊、部分不可讀）違反 RSP-7，不作為本節的比較對象；#39 對北部重疊的處理屬其分配範圍。

## 5. 是否改變 accepted 語義：**否**

- **Outcome Contract**：S-4（Taiwan-wide 視野每縣至多一個代表性有效測站；中間縮放層級的密度管理屬 HOW）、S-10（可見標記可讀可選、密度管理不得使地圖不可用、不要求 375 同時顯示 22 個）、AB-V2-6、AB-V2-8 的文字與語義不變。第 4.2 節只是把這幾句合讀：圖層成員（S-4）、呈現約束（S-10、44×44）、375 放寬（S-10）各自有效；沒有把 375 放寬延伸到桌機（桌機仍以「只因碰撞」受保護），也沒有把「22 同時可見」升為 MUST（accepted 文字中它只以非需求形式出現，E-3）。
- **Derived contract**：SPEC-V2 v2.2 文字不變；沒有新增、刪除或弱化任何 R／AC／INV／oracle／證據類別；R-V2-DD-2「至多一個」、R-V2-RSP-7 全文、AC-V2-14 的 PASS 條件與 FAIL 例逐字維持；第 4.1 節的可觀察檢查只組合既有 oracle（RSP-3 的 44×44、AC-V2-11 的代表集合、DD-4／DD-9(a) 的可達性）。
- **變更性質**：治理 §5.3 第 2 類的 clarification（§3.6-A：既有來源合讀只有一種使每句皆有效的解讀；即便視為多種解讀，選擇只影響 #39 的產品切片）。不改 #39 的「What to build」（可見標記可讀可選、密度管理不使地圖不可用、44×44 本來就是 #39 的範圍）。
- **Boundary determination**：讀法 A、B、C 皆在 V2 Outcome Contract boundary 內；本裁決不涉及 scope、constraints、acceptance boundary 或授權；**不需 acceptor**；沒有 fail-closed 路徑。讀法 B 若被採為 MUST 才會構成 §5.3 第 1 類（新增位移設計或弱化 RSP-3／RSP-7），DA 不採。

## 6. 受影響 work items 與 evidence

| 對象 | 影響 |
| --- | --- |
| **#39**（audit 中；R1 BLOCKING F-1，F-1 修正待派） | 第 4.1 節加入 F-1 targeted correction 的義務與 R2 的核對項；F-1 本身（面板捲動使兩個時間與 `Refresh` 離開可視區）不受本紀錄影響，仍依 R1 的修正與驗證要求。R1 對 R-V2-RSP-7 與 AC-V2-14 其餘各列的結論維持；R1 的 R-1 由本紀錄解決。Executor 目前的密度機制在種類上符合第 4.2 節（E-9：桌機初始視野的碰撞框正是 44×44 必要可點區、名稱標籤在 zoom < 8 不顯示），修正時 MUST 保持此性質並提供第 4.1 節的證據。 |
| **#36、#37、#38**（已結案） | 無。分配、evidence、CLOSURE 不變；#36 R1 交接 (b) 由 #39 依本紀錄處理；#38 R1 F-2（初始視野多邊形指標可達性）仍依其 disposition 交 SIA，本紀錄第 4.2 節第 5 點不改變其處理。 |
| **#40**（待執行） | 不新增分配。Radar overlay 在標記之下（R-V2-RAD-6）；若 #40 改變 CRS 或縮放行為而使碰撞集合改變，屬其既有的 AC-V2-13／15 重驗與 SIA 的整合核對，不需事先分配。 |
| **#41**（待執行） | 不新增分配；既有 R-V2-DOC-3／AC-V2-21(9)(14) 的對照把 R-V2-RSP-7 的證據引用到 #39 R1／R2；README「Marker density」段已存在，#41 只核對與實作一致。 |
| **Spec Integration Audit** | 義務不變（Spec §6.4；治理 §4.7）；核對 R-V2-RSP-7／AC-V2-14 時依第 4.2 節，預期在 #39 R2 record 找到第 4.1 節的 Ticket 層 evidence。 |
| **derivation-SPEC-V2.md** | §14 修訂紀錄加一列引用本紀錄（DA 於本次一併以最小修改更新）；§15.2／§15.3 不變（#39 已是 owner）。 |
| **`doc/ticket/tickets-v2.md`** | 「實作過程中的調整」段由 Orchestrator 補一列引用本紀錄。 |
| **既有 evidence** | #35～#38 的 audit records、worklogs、截圖、network log，以及 #39 R1 record 與已提交截圖全部沿用；沒有任何既有 evidence 因本裁決失效。 |
| **Dependencies** | 依賴圖 7 條邊不變。 |

## 7. Orchestrator／tracker 動作（本紀錄指定；DA 不執行）

1. **Issue #39 body（`gh issue edit 39`）**，只改下列三處、其餘逐字不變（以 diff 證明）：
   - 「Acceptance criteria」清單加一行：`- [ ] R-V2-RSP-7／R-V2-DD-2（全臺視野代表標記的顯示：集合完整、隱藏只因 44×44 碰撞、被隱藏縣可達——依 decision DV-22 \`home_work_01/doc/governance/decisions/decision-20260926-desktop-representative-marker-density.md\` §4.1；AC-V2-14 的證據類別）`。
   - 「Traceability」的 **R** 列加 `R-V2-DD-2、DD-3（全臺圖層集合完整部分）、R-V2-DD-4／DD-9(a)（被隱藏縣的可達性部分）`；**AC** 列加 `11（代表集合＝圖層集合的對照部分）`。
   - 「Spec／worklog」的 Decisions 列加本紀錄路徑（DV-22）。
2. **`doc/ticket/tickets-v2.md`**：「實作過程中的調整」段加一列：2026-09-26，DV-22（本紀錄路徑；來源 #39 R1 的 routing signal R-1），桌機初始全臺視野隱藏部分代表標記在契約內但只限「44×44 碰撞」的最小隱藏（DV-22 §4.2）；#39 F-1 修正後須滿足 DV-22 §4.1 並由 R2 核對；不改 #39 分配；不改 accepted 語義（治理 §5.3 第 2 類）。
3. **#39 F-1 targeted correction 派工**：Executor 的 bounded pack 列入本紀錄路徑並引用第 4.1 節與第 4.2 節；不改派工的其他內容（F-1 的修正與驗證要求依 R1 record）。**#39 R2 派工**：bounded pack 同樣列入本紀錄，R2 MUST 對第 4.1 節 (1)～(5) 逐項 PASS／FAIL。
4. **Run record**：在 checkpoints／routing 記本次 DA 派工結果（R-1(#39) resolved by DV-22）與 DA binding 核對（Bindings §3.4）。
5. **Commit**：本紀錄與 `derivation-SPEC-V2.md` 的最小修改依 SA-1 由派工者原樣 commit（`doc/governance/**` record-only）。

## 8. Evidence（DA 自行執行，全部唯讀；未讀取 `.env`、未使用任何金鑰、未呼叫 CWA）

- 讀取：Bindings b3 全文；治理 §1.2、§1.5、§2.1、§2.3、§2.4、§3.3–§3.6、§5.3、§5.4；`SPEC-V2.md` 全文（§0–§10，含 User Stories、§1.2、§2.3 DD-1～11、§2.6 MAP／RSP 全部、§3 AC-V2-10／11／13／14、§5.1–§5.3、§6.1–§6.4、§7、§10）；`derivation-SPEC-V2.md` 全文（§1–§15，含 B-4、B-8、B-20、DV-9、DV-11、§14、§15.2／15.3、TB-V2-1／4／6）；`outcome-contract-v2.md` 全文（§1、§2.2、§2.5 S-4／S-8／S-10、§3 AB-V2-6／8、§9.1）；`BRIEF-V2.md` 全文（§6、§10、附錄 A）；`issue-39-c1-r1.md` 全文（含 §3 RSP-7 列、§6、§7-6、§9 R-1）；`worklog/issue-39.md` §Contract reference、§Decisions 1–13、§Artifacts；`issue-36-c1-r1.md` §4 關切 3、§8 交接 #39；`issue-38-c1-r1.md` §7、F-2；`issue-38-c1-r2.md` 交接列；DV-20、DV-21 全文（格式與精度先例）；V1 `SPEC.md` R-EN-1、AC-19；README「Now mode — map range, zoom range and layout」段（`README.md:540-579`）；`tickets-v2.md` 全文；run record「Work item status」與 2026-09-26 各 checkpoint（含 #39 Executor return）；`gh issue view 39`（OPEN，label `ready-for-agent`，body 全文）。
- 實作 grounding（只讀）：`static/app.js:210-228`（`MIN_ZOOM`／`MAX_ZOOM`、`DENSITY_PRIORITY`、`TOUCH`）、`:1146-1247`（`updateMarkerAccess`、`densityRank`、`markerBox`、`overlaps` 的 2 px 間距、`coveringRects`）、`:937-939`（`representativeIds` 取自 `/api/` 的 `representativeStationIds`）、`:1026`（`.slabel`）、`:2100`（`map--labels-hidden` 於 zoom < 8）；`static/styles.css:812-823`、`:938-939`、`:1009`。
- 計算（Web Mercator）：zoom 7 每經度 256·2⁷／360 ≈ 91.0 CSS px；25°N 每緯度 ≈ 100 px；44 px ≈ 0.48° ≈ 48 km（1° 經度於 25°N ≈ 100.6 km）。
- Git（read-only）：HEAD `b94d39d9c7346dfc765a09e4553b6523806e578e`（`home_work_01-v2-implementation`）；`git status --porcelain` 只有既存的工具殘留 `grep.exe.stackdump`；`DV-22` 於寫入前在 `home_work_01/` 內 0 命中（編號未被占用）。
- 寫入：本紀錄（新增）；`derivation-SPEC-V2.md` §14 新增一列（Edit 局部修改）。未修改 SPEC-V2、OC-V2、任何 audit record、worklog、實作或測試；未 commit（派工者依 SA-1 處理）；未動 GitHub Issue。
- 產出不含任何金鑰格式字串。
