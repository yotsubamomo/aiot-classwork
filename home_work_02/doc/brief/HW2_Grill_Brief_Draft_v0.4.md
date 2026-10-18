# HW2 — Re-baseline Grill Brief Draft v0.4

- **Status**：DISCUSSION DRAFT — **Grill closed 2026-10-18**。這是以老師更新後的作業頁（SRC-2）重新開始的 focused Grill。Acceptor 已對 F-1～F-7 作出最終裁決（§0，逐字），內容已帶入 Outcome Contract v2 DRAFT（[`../governance/outcome-contract-v2.md`](../governance/outcome-contract-v2.md)）。本檔仍不是 Outcome Contract，不是 Spec，不授權任何實作；裁決要等 OC v2 被 acceptor 有效接受後才生效。
- **不取代任何已接受的內容**：Brief v0.3、Outcome Contract r4（ACCEPTED @ `e2153254`，接受紀錄 @ `370c0ae`）、Spec v1.1 與其 records 保持原樣，作為歷史證據。v0.4 延續 Brief 的版本線，但 v0.3 不因此失效；兩者的關係在新的 Outcome Contract 接受時才確定。
- **來源與追溯**：[`HW2_Requirements_Rebaseline_2026-10-18.md`](HW2_Requirements_Rebaseline_2026-10-18.md)（以下稱「Delta record」）：來源登錄、逐條擷取（T-xx、S-xx）、衝突（X-x）、舊決定處理、受影響契約。
- **撰寫者**：無角色主 session（Bindings b5 §3.5）。Grill 不創造 authority（治理 §3.2）；本檔的建議在 acceptor 裁決並寫入被接受的 Outcome Contract 之前，沒有任何效力。
- **Governance**：`home_work_02/` governance on（Bindings b5）。本 Grill 收斂到新的 Outcome Contract 草稿；Spec 之後由 Design Authority derive。

**Statement classes**：
- **[T]**：老師正文（SRC-1＝SRC-2）。
- **[S]**：老師「補充」段（SRC-2 新增）。
- **[H]**：歷史決定（G1–G8、C1–C5），待重新檢視。
- **[F]**：查證過的事實。
- **[F?]**：未能完整查證的事實，選用時須再核對。
- **[R]**：起草建議，經 acceptor 裁決才有效。

## 0. Acceptor 的最終 Grill 裁決（2026-10-18，逐字）

| Frontier | 裁決 | 與起草建議 [R] 的關係 |
| --- | --- | --- |
| F-1 | **B** | 同建議 |
| F-2 | **A** | 同建議 |
| F-3 | **A** | **不同於建議（B）**：不新增 SelectKBest、RFE |
| F-4 | **B** | 同建議；五個面向由 acceptor 指定；方法交 DA |
| F-5 | **B** | 與建議不同：**不預先固定** p 為非零係數數；p 等慣例交 DA；不得改變選模準則 |
| F-6 | **B** | 同建議；另加「因果解讀的限制」 |
| F-7 | **YES** | 同建議，另有九項明確內容；SRC-2 的公開性改依 Part B 處理（見 Delta record §1.1） |

以下是 acceptor 原文（2026-10-18 對話中的「Part A — Record the acceptor's final Grill decisions」），逐字轉錄。轉錄者：無角色主 session；裁決的效力來自 acceptor 原文，並且要等 OC v2 被接受後才生效。

> The following decisions are explicitly confirmed.
>
> **F-1 = B — Feature count**
> Adopt the intersection of the teacher's original and supplemental feature-count conditions:
>
> * Original requirement: 10–20 features.
> * Supplemental condition: 14–39 features.
> * Adopted constraint: 14–20 source features.
> * Count before categorical encoding.
> * Exclude identifier `id` and prediction target `price`.
> * Explain the two source statements and the adopted interpretation in the report.
>
> The supplemental text remains classified according to its original wording. Do not reclassify all teacher suggestions as mandatory requirements.
>
> **F-2 = A — Dataset**
> Retain the Kaggle King County House Sales dataset.
>
> * Dataset: `harlfoxem/housesalesprediction`
> * Target: `price`
> * Source features: 19
> * Modeling feature groups: 18
> * Preserve the previously pinned CSV checksum and dataset provenance.
> * Preserve the group-aware treatment of repeated house IDs.
>
> Do not change to Predict the Flood or another recommended dataset.
> The recommended dataset list is nonexclusive and does not override the teacher's original permission to choose a topic.
>
> **F-3 = A — Feature selection and candidates**
> Retain the five accepted candidate procedures:
>
> 1. Multiple Linear Regression with all modeling feature groups.
> 2. Forward Selection Linear Regression.
> 3. Backward Selection Linear Regression.
> 4. Ridge Regression.
> 5. Lasso Regression.
>
> Preserve:
>
> * Source-feature-group-level selection.
> * Identical outer folds across candidates.
> * Nested inner-CV tuning.
> * Fit-only feature selection.
> * Outer-CV mean USD RMSE winner selection.
> * Existing tie-breaking decisions.
> * Final refit on the complete Fit partition before calibration.
>
> Do not add SelectKBest, RFE, or permutation-importance-based feature selection as new candidate procedures.
> Explain that the supplemental method list is suggested, not a requirement to implement every listed method.
>
> **F-4 = B — Five regression assumption diagnostics**
> Add an ENHANCED REQUIRED deliverable covering five diagnostic areas:
>
> 1. Linearity.
> 2. Error independence.
> 3. Homoscedasticity.
> 4. Residual normality.
> 5. Multicollinearity.
>
> Requirements:
>
> * Diagnostics use Fit-derived data only.
> * Analyze residual behavior on the log-price modeling scale.
> * Include suitable numerical or graphical evidence and interpretation for each area.
> * A detected violation is a finding to report and explain, not an automatic assignment FAIL.
> * Do not use Calibration or Test observations for diagnostics or design decisions.
> * Clearly distinguish classical regression assumptions from the assumptions supporting split conformal prediction.
>
> Leave detailed diagnostic methods and validation criteria to Design Authority during Spec derivation.
>
> **F-5 = B — Adjusted R²**
> Add Adjusted R² as an ENHANCED REQUIRED evaluation deliverable.
> Include it in the applicable outer-CV comparison and held-out Test reporting.
> Design Authority must define:
>
> * The relevant sample-size and parameter-count conventions.
> * Applicability to OLS, forward/backward subset models, Ridge, and Lasso.
> * How model complexity or effective degrees of freedom are handled.
> * Any limitations on cross-model comparability and interpretation.
>
> Do not preemptively fix the definition of p as the number of nonzero coefficients.
> Do not allow Adjusted R² to alter the already accepted model-selection criterion: outer-CV mean USD RMSE remains authoritative.
>
> **F-6 = B — Model explanation**
> Add an ENHANCED REQUIRED model-explanation deliverable in the Deployment phase.
> Include:
>
> * Interpretation of the frozen predictor.
> * Appropriate interpretation of model coefficients on the log-price scale, accounting for standardization and categorical encoding.
> * Fit-only permutation importance as an explanation tool.
> * The existing demonstration of predicting new samples.
> * Model limitations and appropriate caution about causal interpretation.
>
> Permutation importance is not a new feature-selection candidate.
> Do not access Calibration or Test for this explanation.
>
> **F-7 = YES — Governance and administrative decisions**
> Adopt the governance approach proposed in Brief v0.4, subject to the effective higher-level governance.
>
> 1. Preserve the historical Brief v0.3, accepted Outcome Contract r4, Spec v1.1, existing decision records, and their commit identifiers.
> 2. Prepare a new contract file:
> `home_work_02/doc/governance/outcome-contract-v2.md`
> 3. Explicitly state that v2 is a proposed successor to r4, becoming authoritative for future work only after valid acceptor acceptance.
> 4. Reaffirm C5, the applicable SA-1 / SA-2 permissions, SA-3 opt-in, zh-TW reporting, and authentic ChatGPT / NotebookLM evidence requirements.
> 5. Do not assume the previous one-time RB-1 merge authorization automatically covers the new baseline or its first PR.
> 6. Preserve GitHub Issues #50–#56 unchanged until the new Outcome Contract is accepted and Design Authority determines their disposition.
> 7. Continue to reserve iLearning submission, unauthorized destructive Git operations, and third-party deployment account operations to the applicable authority.
> 8. Use three report classifications:
>    * 老師要求 (mandatory teacher requirement)
>    * 依老師補充建議 (adopted supplemental suggestion)
>    * 專案延伸 (project-defined enhancement)
> 9. Do not present supplemental recommendations as mandatory teacher requirements.

**F-7(a)／(d) 的落實**：
- SRC-2 的追蹤依 acceptor 的 Part B 指示處理，不採本檔原先的建議「追蹤 PDF」。Part B 的指示是：先檢查個人資料、受限內容與公開揭露的風險，適合時才納入，否則改以忠實轉寫加上 sha256。檢查結果是不追蹤原始 PDF，改追蹤轉寫檔 SRC-2T（Delta record §1.1）。
- Topic branch 依 acceptor 的 Part E 授權建立。

## 1. 為什麼要重新基準化

- 老師的正文與評分標準**沒有變**（Delta record §2）。
- 新增的「補充」段是老師貼上的一段 LLM 回答，提問句是老師自己寫的「choose features > 13, < 40」（Delta record §2.1）。
- 這段帶來四類新內容：
  - 特徵數 14–39；
  - Adjusted R²；
  - 五大回歸假設；
  - 推薦的資料集與特徵選擇方法。
- 其中只有特徵數一項可能是新的硬性限制，其餘都是建議語氣。

## 2. Frontiers（依重要性排序；每輪裁決一項）

每個 frontier 都列出證據類別、選項、評分風險與建議 [R]，最後是要 acceptor 回答的問題。

---

### F-1　「補充」段的規範力與特徵數規則

**證據**：
- [T] T-02「10 至 20 個特徵」。
- [S] S-01 提問句「features > 13, < 40」（老師寫的）。
- S-02「14–39 個輸入特徵，不包含 Target」（LLM 轉述）。
- S-04 一方面說「原始特徵數限制」，一方面又說可透過特徵選擇建立「練習版本」。
- S-06「類別編碼後可能增加」支持以編碼前計數。
- [F] King County：19 個 source features（建模用 18 個）。

| 選項 | 內容 | 評分風險 |
| --- | --- | --- |
| A | 補充段整段視為建議；特徵數只依正文 10–20 | 老師若改以 14–39 評分：19 仍符合，風險低；但契約沒有處理新條件，報告也無法說明 |
| **B** [R] | **兩種讀法同時滿足**：source features（編碼前，不含 `id` 與 target）落在 10–20 與 14–39 的交集 14–20。報告逐字引用兩條原文，並說明計數方式與結果。補充段其餘內容依原文措辭視為建議（S），採用與否逐項由 F-2～F-6 決定 | 最低：不論老師依哪一條評分都符合。限制是日後若換資料集，選擇範圍只剩 14–20 |
| C | 以 14–39 取代 10–20 | 正文仍寫 10–20，報告與正文不一致 |
| D | 採用 S-04 的「選擇後」計數（原始特徵可超過範圍，選擇後符合） | 和正文與 S-06 都不一致；不建議 |

**問題**：F-1 採用哪個選項？若選 B，計數規則沿用 OC r4 的 source feature 定義（不含 `id`、不含 target、編碼前）是否確認？

---

### F-2　資料集：保留 King County，或改用推薦清單

**證據**：
- [T] T-03「類型不限」，正文沒有變。
- [S] S-05、S-07、S-10 推薦清單，S-10「My first choice is Predict the Flood」。
- [H] G1 選 King County，並已依此 derive Spec v1.1（尚未實作）。

| 資料集 | 事實 |
| --- | --- |
| **King County**（`harlfoxem/housesalesprediction`） | [F] CC0-1.0；21,613 列；19 source features；0 缺值；CSV 已以 sha256 固定（Brief v0.3 §10）。不在推薦清單內。沒有競賽排行榜 |
| Predict the Flood（SRC-2 連結：`kaggle.com/competitions/predictheflood`） | [F?] Kaggle 競賽頁；內容未查證（competitions API 需要登入）。**rev 2 更正**：rev 1 把它寫成 Playground S4E5，但依 PDF 的 link annotation，S4E5 是第 2 列「Flood Prediction Dataset」的連結 |
| Flood Prediction Dataset（SRC-2 連結：`kaggle.com/competitions/playground-series-s4e5`） | [F?] Playground S4E5 競賽，target `FloodProbability`；旁證只有第三方彙整頁面的 R² 分數（clist.by）。名次要提交才有，提交需要 Kaggle 帳號（RB-3）。**rev 2 更正**：rev 1 查到的 `naiyakhalid/flood-prediction-dataset`（CC0；50,000 列 × 21 欄）不是 SRC-2 連結的資料集，只是同名的另一個 dataset |
| Istanbul Apartment Prices 2026（`brahimenesulusoy/istanbul-apartment-prices-2026`） | [F] CC BY-SA 4.0；「25K+ apartments」；最後更新 2026-03-19。精確特徵數要檢查 CSV（S-06 也這樣說） |
| Human–AI Interaction、Swiss Housing | [F?] 未能確認是哪個資料集；Swiss 註明 restricted access |

| 選項 | 內容 | 影響 |
| --- | --- | --- |
| **A** [R] | **保留 King County**。在報告中說明它不在推薦清單，但符合 T-02、S-01／S-02、S-03 的條件（連續目標、可用 `LinearRegression`、適合特徵選擇與假設檢驗） | Spec v1.1 的資料、分區、conformal 部分大致可沿用；工作量最小。Kaggle 名次仍不適用 |
| B | 改用 Predict the Flood | 幾乎全部重新 derive：group-aware 分區（沒有 `id` 重複）、log 目標（target 有界於 0～1）、conformal 設計都要重新檢視。若要名次，須由 acceptor 自行提交。合成資料使「研究脈絡」較弱 |
| C | 改用推薦清單中的其他資料集 | 同 B，另需查證特徵數與授權 |

**問題**：資料集保留 King County 嗎？

---

### F-3　特徵選擇的方法範圍與 k

**證據**：
- [T] T-07 只要求「必須執行特徵選擇」，沒有指定方法。
- [S] S-09 建議比較 SelectKBest、RFE、SFS、Lasso、permutation importance，k ∈ {14, 20, 25, 30}，只用訓練資料。
- [H] G1、C3：forward／backward（SFS）與 Lasso，k 由 inner CV 選。
- [F] King County 只有 18 個建模 group，所以 k = 20、25、30 在 group 層級不存在。

| 選項 | 內容 | 評分與成本 |
| --- | --- | --- |
| A | 維持 OC r4 的五個候選（LR、forward、backward、Ridge、Lasso） | 已涵蓋 S-09 的 SFS 與 Lasso；S-09 的另外三種方法沒有回應 |
| **B** [R] | 維持五個候選，**另加 SelectKBest 與 RFE 兩個 group 層級的選擇候選**（同一組 outer／inner folds、同樣的 nested CV 與指標）。**Permutation importance 作為模型解釋工具**（F-6），不作為選擇器。k 由 inner CV 在 1…18 中選；報告說明 S-09 的 14 包含在範圍內，20、25、30 超過本資料的 18 個 group 而不適用 | 回應 S-09 的全部五種方法，S-09 本身沒有要求它們都要是選擇器。SelectKBest 成本低；RFE 中等（Spec v1.1 §4.5 的計算預算要由 DA 重新估計） |
| C | 五種方法全部作為選擇器，含 permutation importance | 以 permutation importance 在 nested CV 內選特徵，計算量大，結果也不穩定 |
| D | 在 encoded column 層級選擇（約 87 欄），使 k = 14、20、25、30 都可行 | 會拆開 `zipcode` 的 one-hot group，與 OC r4 的計數規則和 Spec v1.1 的 group 單位衝突；不建議 |

SelectKBest 與 RFE 在 group 層級的實作方式（例如 group 的分數如何彙總）屬於 Spec 設計，由 DA 決定。

**問題**：F-3 採用 B 嗎？若是，新增的兩個候選是否仍適用 OC r4 的選模規則（同一組 outer folds、USD 平均 RMSE 排序、偏誤陳述）？

---

### F-4　五大回歸假設的檢驗

**證據**：
- [S] S-03、S-08f「check the five regression assumptions」，沒有列出是哪五項。
- [H] OC r4 只把額外的診斷圖列為 OPTIONAL；Spec v1.1 R-EVAL-4 允許只用 Fit、沒有 AC。
- [T] T-17「結果合理、美觀且具有說服力」與「CRISP-DM 流程完整」可能受益。

| 選項 | 內容 |
| --- | --- |
| A | 不採用，維持 OPTIONAL |
| **B** [R] | **ENHANCED REQUIRED**，在 Evaluation 階段檢驗五項：(1) 線性、(2) 誤差獨立、(3) 同質變異、(4) 殘差常態、(5) 無多重共線性。條件如下：<br>• **資料只用 Fit**，例如選出 procedure 的 outer-fold out-of-fold 殘差，維持 OC r4 的隔離；<br>• 在 **log 尺度**上做（模型的訓練尺度）；<br>• 每項有圖或統計量，並寫出解讀；<br>• **檢驗顯示違反不是 FAIL**；<br>• 報告須說明兩件事：conformal 預測區間不依賴常態或同質變異；誤差獨立受 177 筆重複交易與地理鄰近影響 |
| C | 同 B，但用 Test 的殘差 | 會讓 Test 用於凍結後評估以外的用途；不建議 |

具體的檢定方法（例如 Breusch–Pagan、Q-Q 圖、VIF）屬於 Spec，由 DA 決定。

**問題**：F-4 採用 B 嗎？五項的清單是否確認為上述五項？

---

### F-5　Adjusted R²

**證據**：
- [S] S-08e 建議比較 MAE、MSE、RMSE、R² 與 Adjusted R²。
- [H] OC r4 OC-A4 只有前四項。
- [F] 若以全部 encoded columns 計，p 約 87；Test n 約 4,300。

| 選項 | 內容 |
| --- | --- |
| A | 不採用 |
| **B** [R] | **ENHANCED REQUIRED**：在 outer-CV 比較表與 Test 指標表都加入 Adjusted R²，以 USD 計算（與 R² 相同的預測與尺度）。p 的定義由 DA 在 Spec 中固定，條件是：(1) 寫在 notebook 與報告；(2) 對所有候選用同一規則。起草建議是「fitted model 中係數不為 0 的 encoded columns 數」，所以 Lasso 依非零係數計，Ridge 依全部欄計。報告說明它對懲罰模型只是近似 |

**問題**：F-5 採用 B 嗎？

---

### F-6　Deployment 的「explain the model」

**證據**：
- [S] S-08g「Predict new samples and explain the model」。
- [H] OC r4 的 Deployment＝凍結 predictor＋預測函式＋使用限制。

| 選項 | 內容 |
| --- | --- |
| A | 不採用 |
| **B** [R] | **ENHANCED REQUIRED**：Deployment 章節加入凍結 predictor 的解釋。內容包括：<br>• 係數在 log 尺度上換算為百分比效果，並說明標準化與 one-hot 的讀法；<br>• permutation importance，只用 Fit 計算，同時回應 F-3 的 S-09；<br>• 「預測新樣本」沿用 R-DEP-2，以人工建構的範例示範，不使用 Calibration 或 Test |

**問題**：F-6 採用 B 嗎？

---

### F-7　治理與行政事項（不影響分析內容）

| 項目 | 選項與建議 |
| --- | --- |
| **(a) SRC-2 是否納入 git 追蹤** | SRC-1（`.txt`）有追蹤；HW01 的老師 PDF 被 `.gitignore` 排除。[R] 追蹤 SRC-2（1 MB）。原因：它是新的上位契約，需要以 git 固定內容，sha256 也記在新契約中。若 acceptor 不願公開老師頁面的列印檔，改為 gitignore，並追蹤一份 acceptor 認可的轉寫檔。兩者都屬 RB-5（修改 `doc/requirement/`），由 acceptor 決定 |
| **(b) 新契約的形式** | [R] 新檔 `doc/governance/outcome-contract-v2.md`，明確寫出取代 r4 作為之後工作的 Outcome Contract；r4 原樣保留 |
| **(c) 沿用的授權** | C5（Git 授權）、SA-3 opt-in、語言 zh-TW、§2.5.1 證據規則：[R] 在新契約中逐項重新陳述，由 acceptor 重新接受。r4 的 **RB-1 一次性授權**（第一個 HW2 PR）不能由 Agent 推定沿用；新契約的第一個 PR 仍會含 `doc/requirement/`，須由 acceptor 重新授權或改由 acceptor 合併 |
| **(d) 本次文件的 commit** | Delta record 與本 Brief 目前只在工作目錄。[R] 在新的 topic branch `home_work_02-rebaseline` 上 commit 並 push，由 acceptor 逐次授權：重新基準化是 r4 範圍外的新 work item，SA-1 不涵蓋。分支以 `home_work_02-outcome-contract` 為基礎，保留舊歷史，不 rebase |
| **(e) 標示規則（X-7）** | [R] 報告的 scope 標示分三種：「老師要求」（T）、「依老師補充建議」（採用的 S 項目）、「專案延伸」（其餘 ENHANCED）。不得把 S 寫成「老師要求」 |
| **(f) 既有 Issues #50–#56** | [R] 保持 OPEN、不修改，直到新契約接受後由 DA 在新的 derivation 中決定處置。在此之前不啟動任何 Formal run |

**問題**：(a)～(f) 是否依建議？特別是 (a) 與 (d) 需要 acceptor 的明確授權。

## 3. 建議的新 Outcome Contract 邊界（rev 1，假設 F-1～F-7 都依 [R]）

> **rev 2 註記**：本節是裁決前的建議，保留作為紀錄。Acceptor 的裁決與建議有兩處不同：F-3＝A，所以 E1 不擴充、沒有 SelectKBest／RFE；F-5 不固定 p。依裁決後的實際邊界見 OC v2 DRAFT 第 10 節。

### 3.1 必須改變的邊界

| OC r4 位置 | 新邊界 |
| --- | --- |
| §2.1 上位契約 | SRC-2（sha256 `1b3a5aad1c261425eb34f2eb46aebe6a62c73aba4fbf2d67a166fe9df28639d7`）為現行上位契約；SRC-1 為歷史，正文兩者相同 |
| §2.2 M1 | Kaggle 公開資料集；source features（編碼前，不含 `id` 與 target）同時落在 10–20 與 14–39；標明名稱與連結 |
| §2.2 E1 | 比較範圍：LR baseline、forward、backward、SelectKBest、RFE（皆 group 層級、k 由 inner CV 在 1…18 選）、Ridge、Lasso |
| §2.2 新增 E 項 | Adjusted R²（F-5）；五大假設檢驗（F-4）；模型解釋與 permutation importance（F-6）；「依老師補充建議」的標示規則（F-7(e)） |
| §2.3 Non-scope | 加入：不採用「選擇後」的特徵數讀法；不在 encoded column 層級選擇；不以 Test 或 Calibration 做假設檢驗或解釋；permutation importance 不作為選擇器 |
| §3.1 | OC-A1：兩個範圍。OC-A4：七個候選與 Adjusted R²。新增 OC-A9：假設檢驗。新增 OC-A10：模型解釋。OC-A2：Deployment 內容 |
| §3.4 | 不是 FAIL：假設檢驗顯示違反；選出 SelectKBest 或 RFE 以外的候選。是 FAIL：以 Test 或 Calibration 做檢驗或解釋；把 S 項目寫成老師要求 |
| §5 | DA 需處理的新設計事項：Adjusted R² 的 p；group 層級 SelectKBest 與 RFE 的評分方式；五項檢驗的方法與資料來源；計算預算 |
| §7、§9 | 新的 stable reference 與接受紀錄；RB-1 是否授權（F-7(c)） |

### 3.2 可以不變的邊界（新契約重新陳述，語義不變）

- **資料**：King County、CSV sha256 `d0875baa…7b7e`、CC0。
- **分區與 CV**：60／20／20 group-aware 分區；同一組 outer 5-fold；inner CV；USD 平均 RMSE 排序；偏誤陳述（G2、G4、C1–C3）。
- **目標與指標**：`log(price)` 訓練，USD 指標（C4）。
- **Conformal**：OC r4 §2.4.2 全部內容（G3），含三層陳述與 exchangeability 假設。
- **證據與標示**：§2.5.1 AI 研究與對話證據規則；「GPT 輔助內容」與「NotebookLM 摘要」。
- **完成狀態與輸入**：§3.2 S1～S4 完成狀態；§3.3 acceptor 輸入（ChatGPT PDF、NotebookLM 材料、學號）。
- **授權**：§4 authority；C5 Git 授權；SA-3 opt-in（Bindings b5）。
- **語言**：zh-TW。
- **Non-scope**：Web App、API、資料庫、MLOps、Auto Regression；Kaggle 名次不適用。

### 3.3 Lane（由 DA 判定）

預期仍為 **Formal**：多個相依的 execution units，加上 acceptor 輸入。新契約接受後，DA 重新判定 lane 與高風險類別，並決定 Spec v1.1 是修訂為 v2.0 還是重新 derive。

## 4. 下一步

1. ~~逐項裁決 F-1～F-7~~：完成（§0）。
2. ~~授權 Git 動作~~：完成（acceptor 2026-10-18 Part E；SRC-2 依 Part B 處理）。
3. OC v2 DRAFT r1 已起草（[`../governance/outcome-contract-v2.md`](../governance/outcome-contract-v2.md)），交 acceptor 審閱與接受。**本 session 不會自行接受新的 Outcome Contract。**

## 5. Revision history

| Version | Date | Change |
| --- | --- | --- |
| v0.4（rev 1） | 2026-10-18 | 以 SRC-2 重新基準化：補充段的證據性質、F-1～F-7 frontiers、建議的新 Outcome Contract 邊界。v0.1～v0.3 不變 |
| v0.4（rev 2） | 2026-10-18 | Grill closed：§0 逐字記錄 acceptor 的 F-1～F-7 裁決；F-2 事實表依 PDF link annotation 更正 Predict the Flood 與 Flood Prediction Dataset 的連結對應；§3 標註為裁決前的建議；§4 更新。rev 1 未曾 commit，rev 2 是第一個 commit 的版本 |
