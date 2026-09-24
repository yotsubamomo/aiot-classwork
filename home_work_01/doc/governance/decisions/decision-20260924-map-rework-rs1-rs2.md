# Decision record — Issue #28 A-4 R1 的兩個 routing signals：V-2 對比語義（RS-1）與 masthead 導言 boundary（RS-2）（`home_work_01/`）

- **紀錄類型**：Design Authority decision record（治理 §3.6-A：不改變任何 accepted 語義的 clarification；§2.4 「契約語義是否足夠、boundary determination」；§1.2 boundary determination；治理 §5.3 第 2 類）
- **編號**：**DR-21**（延續 DR-20 [`decision-20260924-taiwan-map-rework.md`](decision-20260924-taiwan-map-rework.md)）；子裁決 **DR-21.1**（RS-1）、**DR-21.2**（RS-2）
- **日期**：2026-09-24
- **來源**：Orchestrator 依治理 §2.4 派工，處理 `gov-primary-reviewer` 在 [`../audit/issue-28-c1-r1.md`](../audit/issue-28-c1-r1.md) §4 提出的 RS-1（驗收語義）與 RS-2（boundary determination）。binding 核對由派工者依 Bindings §3.4 記入 run record。
- **本 work item 的 Outcome Contract**：與 DR-20 相同——acceptor 2026-09-24 核定文（DR-20 §0 逐字）＋其核定的指示文件 §1–§4（＝Issue #28）。本紀錄**不修改** Spec v1.1、既有 Outcome Contract、DR-20 的任何文字；不重開 #18–#25。
- **相關契約與紀錄**：DR-20 P-2（底圖 token）、P-4（藥丸與色帶 token、白 2 px 描邊、黃色帶深字）、P-5（代表點在成員縣市內）、P-13（V-1～V-5 對地圖卡的適用）、B-15、X-3、§3.5(A)、§3.6(2)；Issue #28 §2「只動 Taiwan Map 卡」、§2.9「不動 masthead …」、§4 DoD V-2；核定文「Treat this as a NEW post-baseline Taiwan Map / Dashboard UI enhancement work item」、「Do not start unrelated redesign work」；Spec v1.1 R-EN-1、R-EN-2（概念詞）、INV-7；decision A-1／H-2／H-3；#28 worklog [`../worklog/20260924-taiwan-map-rework.md`](../worklog/20260924-taiwan-map-rework.md)。
- **執行角色**：`gov-design-authority`（Bindings §3.1：`design_authority` → `claude-fable-5-1`／`xhigh`）。本紀錄不自證 binding。
- **效力**：#28 的 Executor、Reviewer（R2／Alternate）、Orchestrator 以本紀錄為 V-2 第二句的操作規則與 masthead 導言一句的 boundary 依據；**DR-21.1 與 DR-20 P-13 V-2 合併閱讀**，DR-20 本文不修改。R1 record 中 V-2 色帶部分的「UNDETERMINED」依本紀錄結案（Reviewer 在 R2 record 自行套用規則並記錄結果）。本紀錄不修改任何實作、測試、資料或 `doc/acceptance/`。

---

## 1. 問題

- **RS-1**：DR-20 P-13 採納的 V-2 第二句「四段色帶對底圖 ≥ 3:1（token 值計算）」，比較對象是 (a) **標記整體**（含白描邊）對底圖——白描邊 ≥ 3:1 即為 WCAG 1.4.11 意義下的界定，V-2 PASS、不改色；還是 (b) **色帶填色本身**對底圖（含台灣陸地 `#25324a`）——藍／綠／紅 2.37／2.83／2.35 不合格，須修正。若 (b)，修正路徑為何、是否仍在 DR-20 HOW 內、是否牴觸 acceptor 核定的 P-2／P-4 而需 acceptor。
- **RS-2**：`static/index.html:22-26` masthead 導言一句被改寫。Issue #28 §2.9 寫「不動 masthead」，DR-20 X-3 把「重做 masthead」列為 boundary 之外。此一句的改寫是否在 boundary 內（配合 map-first 的附帶文案）或在外（X-3，須在 correction 中還原）；是否改到任何 accepted 語義或概念詞。

---

## 2. 事實（DA 自行核對；Executor、Reviewer 與 Orchestrator 的敘述都當作待驗證主張）

| # | 事實 | 證據 |
| --- | --- | --- |
| E-1 | **V-2 的三個核定來源文本**（依 DR-20 E-10／首段：兩份草稿與指示文件皆「提案 HOW，經 acceptor 於本指示核定」；衝突時指示優先）：(i) 草稿 §6 V-2：「文字對比 ≥ 4.5:1；**資料線／點／標記對底 ≥ 3:1**｜以 token 值計算（WCAG 公式），記錄於 worklog」。(ii) 補充段 5.5-E V-2：「**四段色帶對底圖的非文字對比 ≥ 3:1（黃色帶靠白描邊達成）**；藥丸內文字對藥丸底 ≥ 4.5:1（黃色帶用深色字）」；同段 5.5-A「白色 2 px 描邊＋一級陰影」；5.5-C「深色模式下藥丸的四段色帶色不變，**描邊改 `--surface`（深色）以維持 ≥ 3:1 非文字對比**」。(iii) Issue #28 §4／DR-20 P-13：「藥丸內文對底 ≥ 4.5:1、四段色帶對底圖 ≥ 3:1（token 值計算，記 worklog）」。三者沒有衝突：(iii) 是 (ii) 的濃縮，(ii) 明文以描邊作為達成 ≥ 3:1 的手段，(i) 的對象是「標記」。 | `visual-direction-draft.md:111`；`visual-direction-addendum-map.md:9, 27, 38`；`gh issue view 28` §4；DR-20 P-13 |
| E-2 | **`b4549e5` 的實作**：token `--map-sea #0f1927`、`--band-blue #2b6cb0`／`green #2f855a`／`yellow #d69e2e`／`red #c53030`（`styles.css:42, 53-56`；`app.js:77-80` 同一組）；周邊陸 fill `#1a2331`、台灣陸 fill `#25324a`／縣界 `#44577a`（`app.js:569, 575`），與 P-2 一致。藥丸 `.pill { border: 2px solid #fff; box-shadow … }`（`styles.css:567-568`）；hover／focus-within／`is-active` 時 `border-color: #9ed0ff`、寬度仍 2 px（`:589-591`）；`:focus-visible` 另有 3 px `#9ed0ff` outline（`:588`）；藍／綠／紅白字、黃 `#1a2230` 深字（`:584-587`），與 P-4 一致。圖例 swatch 16×16、`1.5px solid rgba(255,255,255,.7)` 描邊，位於面板 `--map-surface-2 #1f2a3b` 上（`:529-535`）。 | DA 讀檔（HEAD `6b906a4` 與 `b4549e5` 的 `static/` 無差異；工作樹只多本次 R1 record） |
| E-3 | **DA 以 WCAG 2.x 相對亮度公式重算（token 值）**，與 worklog `:59-61` 及 R1 §2.4 一致：填色對海 `#0f1927` 藍 3.26／綠 3.89／黃 7.39／紅 3.23；對台灣陸 `#25324a` **2.37／2.83／5.38／2.35**；對周邊陸 `#1a2331` 2.92／3.48／6.62／2.89。白描邊 `#fff` 對海 17.67、對台灣陸 **12.85**、對周邊陸 15.81。作用態描邊 `#9ed0ff` 對台灣陸 7.91、海 10.87、周邊陸 9.72。內文對填色：白／藍 5.42、白／綠 4.54、深字／黃 6.68、白／紅 5.47。 | DA 自算（scratchpad Python；公式 sRGB→線性、L=0.2126R+0.7152G+0.0722B、(L1+0.05)/(L2+0.05)） |
| E-4 | **讀法 (b) 與核定 HOW 不可能同時成立（算術）**：台灣陸 L=0.0317，填色要對它 ≥ 3:1 須 L ≥ **0.1951**；白字對填色 ≥ 4.5:1 須填色 L ≤ **0.1833**。兩個區間不相交——**任何**藍／綠／紅 hex 都無法同時滿足「填色對台灣陸 ≥ 3:1」與 P-4 的「其餘白字 ≥ 4.5:1」。反向把陸地調暗：以紅 L=0.1420 計，陸地須 L ≤ 0.014，而海 L=0.0094、目前陸／海對比只有 1.37:1——即陸地須調到與海幾乎同色，P-2 的陸／海分層消失。在藥丸外加深色 halo 不改變「填色對底圖」的數值，只是把界定改由 halo 承擔，本質仍是讀法 (a)。 | DA 自算 |
| E-5 | 六個代表點全部落在台灣縣市多邊形內（R1 §2.6 point-in-polygon；P-5 的必要條件），藥丸中心相鄰的底圖色是台灣陸 `#25324a`；藥丸邊緣、低 zoom 或拖曳時可能疊在海或周邊陸上。 | R1 §2.4、§2.6；`app.js:583-591` iconSize 104×52 |
| E-6 | **masthead 導言**：`index.html:22-26` 由「Six-region seven-day forecast — pick a region to see its temperature trend, daily table and weekly summary.」改為「Six-region seven-day forecast — read the derived map temperature for a day on the Taiwan map, then pick a region below for its temperature trend, daily table and weekly summary.」；eyebrow、`<h1>Taiwan Weather Forecast</h1>`、masthead CSS 未動。舊句由 #23（`610a797`）引入；**不出現在** Spec v1.1、Outcome Contract、`tests/**`、`doc/acceptance/ACCEPTANCE.md`、任何 audit／decision record（#23 R1 與 #24 R1 只把 masthead 當 R-EN-1(1) 的一個「區塊」核對，未引用句子內容）。R-EN-2 概念詞（`Taiwan Weather Forecast`、`Select Region`、`Select Date`、`Date`、`MinT`、`MaxT`、Region 中文名）一字未改。新句稱「derived map temperature」，與 INV-7／H-3 的導出標示一致，未把六區值寫成 CWA 發布。**#28 worklog 沒有記載這項改動。** | `git diff 720c0a0..b4549e5 -- home_work_01/static/index.html`；`git log -S`；grep `home_work_01/`（doc、tests）；worklog grep |
| E-7 | **scope 文本**：核定文「Treat this as a NEW post-baseline **Taiwan Map / Dashboard UI** enhancement work item」、「Do not start **unrelated redesign** work」；Issue #28 §2 標題「What to build（只動 Taiwan Map 卡）」、§2.9「**不動** masthead、controls、Weekly summary、折線圖、表格（核定文：Do not start unrelated redesign work）」；DR-20 X-3 的對象是「**重做** masthead、controls card（除移出 `Select Date` 之外）…」。§2.9 的「不動 controls」與 §2.5「`Select Date` 移入地圖卡（controls card 保留 …）」並存，顯示 §2.9 的「不動」已是「不重做，附帶必要改動除外」的用法。 | DR-20 §0、B-15、X-3；`gh issue view 28` |

---

## 3. 裁決

### 3.1 DR-21.1 — RS-1：V-2 第二句採讀法 (a)；操作規則如下；不需改色；DR-20 不修改；不需 acceptor

**裁決**：V-2「四段色帶對底圖 ≥ 3:1」的比較對象是**以該色帶著色的標記整體**對其所在底圖，達成方式包含填色本身或標記的界定描邊——這正是核定來源 5.5-E 自己寫明的「（黃色帶靠白描邊達成）」與草稿 §6 的「標記對底」；Issue §4／P-13 的措辭是濃縮，不是改變。讀法 (b) 不採。

**操作規則 OR-V2**（Reviewer／Executor 依此判定；token 值計算，WCAG 2.x 公式；結果記 worklog）：

1. **文字句（不變）**：每一色帶的藥丸內文對該藥丸填色 ≥ 4.5:1（黃色帶以深字計）。
2. **標記句**：對每一色帶 b 與標記可能疊上的每一個底圖色 c——**MUST 含台灣陸 `#25324a`**（E-5），並同時列出海 `#0f1927` 與周邊陸 `#1a2331`——下列至少一項成立：CR(填色_b, c) ≥ 3，**或** CR(界定描邊, c) ≥ 3。「界定描邊」指 P-4 核定的藥丸實線、連續、寬 2 CSS px 的描邊；規則適用於標記的**每一狀態**（預設、hover、focus、選取；描邊顏色依 P-4 可變，寬度與連續性不得低於 2 px 實線）。
3. **證據要求**：只列「對海」的數字**沒有證明力**（採納 R1 §2.4(a)）；worklog MUST 同時列出填色與描邊對三個底圖色的數值，並註明依 DR-21.1 判定。
4. **範圍界定**：「底圖」只指 Leaflet 底圖幾何的填色（海、周邊陸、台灣陸）。圖例 swatch、tooltip、面板不是「底圖」，不在 V-2 第二句之內；本紀錄**不**為它們新增任何對比判準（R1 未對其提 finding，DA 不預判）。

**套用於 `b4549e5`**（E-3）：文字句 5.42／4.54／6.68／5.47 PASS；標記句——黃：填色對三底圖 5.38／7.39／6.62 已 ≥ 3；藍／綠／紅：填色對台灣陸 < 3，但白描邊對台灣陸 12.85、海 17.67、周邊陸 15.81 ≥ 3；作用態描邊 `#9ed0ff` 對三底圖 7.91／10.87／9.72 ≥ 3。**V-2 於 `b4549e5` 為 PASS（依 DR-21.1）**；由 Reviewer 在 R2 record 自行核算後記錄，本紀錄不代 Reviewer 作 audit 結論。

**依據**：

1. **核定文本本身**（E-1）：定義 V-2 的 5.5-E 明文「黃色帶靠白描邊達成」，5.5-C 又以「描邊改深色以維持 ≥ 3:1 非文字對比」為手段；criterion 的作者與 acceptor 核定的就是「描邊可以達成」的規則。當時弱的是黃色帶（淺底圖），現在弱的是藍／綠／紅（深底圖），機制相同。
2. **3:1 的出處**：3:1 是 WCAG 2.x 1.4.11 非文字對比的門檻，其判定規則即「元件邊界或填色任一對相鄰色 ≥ 3:1」；criterion 引用該門檻，就承接其判定規則。
3. **一致性**（E-4）：讀法 (b) 使 acceptor 在同一指示中核定的 V-2、P-2 陸地色、P-4 白字三者**必然**互斥——沒有任何藍／綠／紅 hex 能同時通過。當同一批核定材料存在一種讓它們彼此一致的讀法（且該讀法就寫在核定來源裡），把它們讀成自相矛盾不是 accepted 意圖。
4. **選擇只影響本 work item**（§3.6-A 第二種情形）：V-2 是 #28 的附加 DoD（DR-20.6(2)），不是 Spec AC；沒有其他工作依賴它。

**對 correction 的要求**：

- **不需**、也**不得**為 V-2 修改 P-2／P-4 token 或藥丸文字色（那是無必要地改動核定 HOW）；不需加 halo、不需調陸地色。
- worklog 的 V-2 段 MUST 改寫：依 OR-V2 列出填色與描邊（含作用態）對海／台灣陸／周邊陸的數值，判定寫「PASS（DR-21.1）」，不再寫「PASS with border rationale」這種以 Executor 自己解讀為依據的措辭。ACCEPTANCE.md 的 V-2 列同樣引用 DR-21.1。
- R2 核對：描邊在四種狀態下仍為 2 px 實線連續；token 未變（若因其他 finding 變動，依 OR-V2 重算）。

**DR-20 是否改變**：**否**。DR-20 P-13 的 V-2 文字不動；DR-21.1 是其操作規則，二者合併閱讀。R1 record 的「UNDETERMINED」依此結案。

**是否需要 acceptor**：**否**（§3.6-A、§5.3 第 2 類）。附記：若 acceptor 另行要求「填色本身對台灣陸 ≥ 3:1」，依 E-4 那必然連帶改變已核定的 P-4 白字或 P-2 陸／海分層，屬 acceptor 對本 work item HOW 的**新指示**；本紀錄不請求、不建議。

**爭議處理**：Reviewer 依 OR-V2 內的事實（描邊寬度、連續性、狀態）提出的問題是一般 finding；對 OR-V2 規則本身的不同意不是對實作的 finding，屬 review dispute，由 Orchestrator 依 §2.4 交 Final Adjudicator 釐清 routing，FA 不因此取得語義決定權。

### 3.2 DR-21.2 — RS-2：masthead 導言一句在 boundary 內（附帶、與核定方向一致）；不還原；不是 X-3；不需 acceptor

**裁決**：`index.html:22-26` 導言一句的改寫**在本 work item 的 Outcome Contract boundary 內**，是 map-first 呈現的附帶文案調整，不是 X-3 所指的「重做 masthead」；correction **不須還原**。本 determination 只及於 `b4549e5` 該一句（E-6 原文與新文），不及於 masthead 的任何其他部分。

**依據**（治理 §1.2 的三個判準）：

1. **未超出 scope**：acceptor 自己的核定文把 work item 界定為「Taiwan Map / **Dashboard UI** enhancement」，其限制是「Do not start **unrelated** redesign work」（E-7）。導言是頁面對自身閱讀順序的描述；map-first 是核定的十一項方向之一；核定後的頁面若導言仍寫「pick a region to see …」而不提地圖，就是對核定版面的錯誤描述。該改動因此是核定項目的**直接後果**，「related」而非「unrelated」，且不是 redesign（結構、樣式、eyebrow、`<h1>` 全未動）。Issue §2.9 的「不動 masthead」與同段「不動 controls」一樣，是「不重做、附帶必要改動除外」的用法（E-7）；controls card 的附帶改動有被明列，masthead 的沒有，這是提案文本的列舉疏漏，不是 scope 的差異。X-3 的字面對象是「重做」。
2. **未違反 constraints**：不涉 X-1／X-2／X-4～X-8；不動 `/api/`、MVM、Grading App。
3. **未改變 accepted 語義**（E-6）：R-EN-2／H-2 概念詞一字未改；舊句不在 Spec、OC、測試、ACCEPTANCE、任何 audit 證據之中，沒有任何既有結論依賴它；新句的「derived map temperature」與 INV-7／H-3 一致，未作 CWA 歸屬。

**條件**：

- (a) #28 內**不得**再動 masthead 的任何其他部分（eyebrow、`<h1>`、版面、CSS）；那些是 X-3，需 acceptor 的新 work item。
- (b) 本項改動目前**未記於 worklog**（E-6）；correction 的 worklog MUST 補記為「附帶改動（地圖卡以外）」並引用 DR-21.2（治理 §3.7 worklog 完整性）。Executor 日後在地圖卡以外的任何附帶改動，MUST 先記 worklog 並由 Reviewer 核對，不得默默帶入。
- (c) Reviewer 在 R2 record 關閉 RS-2。若 Reviewer 在本 determination 後**仍**對此 boundary 有異議，依治理 §1.2 該 boundary 對 closure 視為未確立，此一句的路徑 fail-closed 至 acceptor（屆時安全路徑是還原該句；由 Orchestrator 機械套用，不需再問 DA）。

**是否需要 acceptor**：**否**——DA 已依 §1.2 確立在 boundary 內。

---

## 4. 是否改變 accepted 語義

**否。** 兩項裁決都是治理 §5.3 第 2 類／§3.6-A：DR-21.1 在核定來源已寫明的讀法中選定操作規則，未改變 V-2 的門檻、對象或 PASS／FAIL 語義，未改任何 Spec R／AC／INV／gate；DR-21.2 是 §1.2 的 boundary determination，確立既有改動在已接受的 boundary 內，未擴張 scope。Spec v1.1、既有 Outcome Contract、#28 的 Outcome Contract（核定文＋Issue #28）與 DR-20 文字全部不變。DA 未代行任何接受或授權。

---

## 5. 受影響的工作、dependencies 與既有 evidence

| 項目 | 影響 |
| --- | --- |
| **#28 targeted correction**（F-1、F-2、F-4、F-5 之外） | 不新增實作修正。**記錄修正**：worklog V-2 段依 OR-V2 重寫（含台灣陸／海／周邊陸、填色與描邊、作用態）、判定引用 DR-21.1；worklog 補記 masthead 導言一句為附帶改動並引用 DR-21.2；ACCEPTANCE.md 的 V-2 列引用 DR-21.1。 |
| **#28 R2**（同一 Reviewer 續派） | 依 OR-V2 自行核算並記錄 V-2 結果，關閉 RS-1、RS-2；核對 3.1 與 3.2 的條件。R1 的 blocking findings 與 closure 條件不受本紀錄影響。 |
| **DR-20** | 文字不變；P-13 V-2 與 DR-21.1 合併閱讀；X-3 的解讀以 DR-21.2 為準（對象是「重做」）。 |
| **DR-20 §3.5 fail-safe** | RS-2 由 DA 直接確立在 boundary 內且未被爭議 → 不觸發補充 Spec Integration Audit（維持 R1 §2.1 的判定）；若 3.2(c) 的異議情形出現，依 §3.5 fail-safe 由 Orchestrator 機械判定。 |
| **phase-acceptance 增補**（DR-20 §3.5(B)） | 對 V-2 的引用以 DR-21.1 為依據。 |
| **Spec v1.1、Outcome Contract、Bindings、#18–#25** | 不變、不重開。 |

---

## 6. Authority

- 兩項裁決在 Design Authority 的 contract-sufficiency、驗收語義與 boundary determination 權限內（治理 §1.2、§2.1、§2.4、§3.6-A、§5.1）。
- **不需要 acceptor 的任何動作。** 仍屬 acceptor 的事項（本紀錄不請求，只列出）：若 acceptor 想改採「填色本身對陸地 ≥ 3:1」，那是對核定 HOW 的新指示（3.1 附記）；masthead 其他部分的重做（X-3）是新 work item。
- Final Adjudicator：目前沒有 routing 或 review 爭議；只在 3.1「爭議處理」或 3.2(c) 的情形出現時依 §2.4 介入 routing。
- Reviewer 保有 findings、severity、blocking 與 closure 的判定（§2.1、§4.3）；本紀錄不代 Reviewer 作 V-2 的 audit 結論，只給規則與 DA 自算的參考數字。
- DA 未修改任何實作、測試、資料、Spec、OC、DR-20 或 `doc/acceptance/`；未 commit；未 merge。

---

## 7. Evidence（DA 自行執行，全部唯讀；未印出任何金鑰）

- 讀取：Bindings b1 全文；治理 v2.0 §1.2、§2.4、§3.6、§4.2、§5.3；DR-20 全文；`issue-28-c1-r1.md` 全文；Issue #28（`gh issue view 28`，OPEN，`ready-for-agent`）；`static/styles.css:42-56, 524-537, 538-602`；`static/app.js:556-611`；`static/index.html` diff `720c0a0..b4549e5`；#28 worklog `:59-61, 84` 與 masthead grep（0 筆）；`visual-direction-draft.md:109-113`、`visual-direction-addendum-map.md:7-12, 25-27, 35-40`（acceptor 支援 session scratchpad，DR-20 E-10 所引；唯讀）。
- Git：HEAD `6b906a4`；`git status --porcelain` 只有未追蹤的 `doc/governance/audit/issue-28-c1-r1.md`；`git diff --stat b4549e5..HEAD -- home_work_01/static` 為空（受審 subject 的 `static/` 與 HEAD 相同）；`git log -S "pick a region to see its temperature trend"` → `b4549e5`（移除）、`610a797`（#23 引入）。
- Grep：`home_work_01/doc/governance/**`、`doc/acceptance/ACCEPTANCE.md`、`tests/**` 內無舊導言句；`DR-21` 在本紀錄之前只出現於 DR-20 E 段的「無 DR-21」自述。
- 計算：WCAG 2.x 相對亮度與對比（scratchpad Python），數值見 E-3、E-4；與 worklog 及 R1 的數字一致。
