# Decision record — Spec v1.1：pre-implementation review findings F-01～F-06 與附加問題（`home_work_02/`）

- **紀錄類型**：Design Authority decision record（治理 §1.2、§2.4、§3.6、§5.3 第 2 類；Bindings b5 §7）
- **日期**：2026-10-14
- **對象**：[`../../spec/SPEC.md`](../../spec/SPEC.md) v1.0（commit `b012e4f93defe77dab2959737f9334ce928893d8`，sha256 `7fe4163d…3153`）→ **v1.1**；Tickets #50–#56；Ticket 索引 [`../../ticket/tickets.md`](../../ticket/tickets.md)。
- **Outcome Contract**：[`../outcome-contract.md`](../outcome-contract.md) ACCEPTED。Normative 第 1–8 節於 `e2153254ccf7a97475d1c22e10d6a1e0717c5497`；接受紀錄第 9 節於 `370c0ae1`。本 DA 核對 `git diff 370c0ae HEAD` 對 OC、`doc/requirement/`、`doc/brief/`、`CONTEXT.md` 沒有任何變更（HEAD `323d3de5`）。
- **派工**：無角色主 session 作為派工介面（治理 §2.7）轉達的 DA assignment：評估 acceptor 的 pre-implementation review request 所附 findings F-01～F-06 與一個附加問題。派工者表明 findings 是待評估的主張，不是決定。
- **執行角色與 binding**：`gov-design-authority`。Binding 由派工者依 Bindings §3.6 核對並記錄；本紀錄不自證 binding。
- **相關紀錄**：[`derivation-SPEC.md`](derivation-SPEC.md)（本次新增第 14 節）；[`decision-20261014-high-risk-categories.md`](decision-20261014-high-risk-categories.md)（不修改）。

## 1. 問題（findings 原文摘要）

| ID | 嚴重度（提出者） | 主張 |
| --- | --- | --- |
| F-01 | HIGH | R-EVAL-2 規定 X＝預測、Y＝實際，卻用垂直的預測區間；要求更正圖形語義，並核對全部 Test 的圖是否可讀。 |
| F-02 | HIGH（執行風險） | Forward／backward 的 nested CV 可能需要約 10,000 次 fit；評估計算可行性，以及不弱化 CV／特徵選擇要求的允許最佳化。 |
| F-03 | MEDIUM | 釐清「Test 只評估一次」是每次獨立執行一次，可重現性測試可以重複固定的執行，但不得依 Test 重新設計。 |
| F-04 | MEDIUM | 釐清 full column rank 的檢查對象：跨 folds 與候選子集的實際訓練矩陣，含罕見或常數的 encoded 欄。 |
| F-05 | MEDIUM | 多個候選與最小 RMSE 相差 0.5 USD 以內時，outer-CV tie-break 須有決定性。 |
| F-06 | LOW | Spec 檔頭仍寫 Tickets 尚未 derive。 |
| 附加 | — | AC-23 的逐句 NotebookLM 對照，是否超出已接受的證據真實性邊界（OC §2.5.1、OC-A7）而增加不必要的複雜度？不得未經授權弱化已接受的要求。 |

## 2. 裁決總表

| ID | 分類 | 變更（Spec v1.1） | 改變 accepted 語義？ |
| --- | --- | --- | --- |
| F-01 | **REJECTED**（圖形語義）／**CONFIRMED**（可讀性） | 垂直區間的語義正確，不更正。依可讀性量測改寫 R-EVAL-2：全部 Test Sales、log-log 刻度、以帶狀區域呈現區間（等於逐筆垂直區間的聯集）、不畫逐筆線段、點的著色與 R-CONF-4 同一判定；AC-15 加入點數一致的核對。 | 否 |
| F-02 | **CONFIRMED**（規模約 1.0～1.07 萬次 fit）；HIGH 執行風險**不成立**（量測約 3～4 分鐘） | 新增 Spec §4.5：規模、量測、允許的等價最佳化、不允許的簡化；R-TEST-6 加入等價性測試；§9.2 新增風險列。 | 否 |
| F-03 | **CONFIRMED** | R-SEL-4 定義「一次執行」；新增 R-EVAL-1a（每次執行一次評估；重複執行是重現的條件；worklog 義務）；AC-09、AC-14、AC-20、INV-2 相應更新。 | 否 |
| F-04 | **CONFIRMED**（驗證範圍缺口；量測未發現秩不足） | R-PREP-2 的檢查改為 31 個實際訓練矩陣，子集由線性代數推得，失敗時報錯並 route 至 DA；R-TEST-2、AC-12 相應更新。 | 否 |
| F-05 | **CONFIRMED** | R-SEL-2 改為以最小值為錨點的平手集合 T，取 T 中偏好順序最前者；D-4、AC-12、R-TEST-6 相應更新。 | 否 |
| F-06 | **CONFIRMED** | 檔頭的 Spec 版本與 Tickets（#50–#56）；§0 activation 前提註記已完成。 | 否 |
| 附加 | **REJECTED**（逐句對照不是不必要的複雜度，維持） | 只釐清對照表「位置」的形式（R-AI-2、AC-23），使其最輕；要求本身不變。 | 否 |

**Contract change：無。Boundary 問題：無。Capability escalation：無（第 5 節）。**

## 3. 逐項評估

### 3.1 F-01 預測圖

**圖形語義（REJECTED）。** 預測區間是對**實際值 Y** 的區間：給定點預測 ŷᵢ，區間為 `[ŷᵢ·e^(−q̂), ŷᵢ·e^(q̂)]`（OC §2.4.2；R-CONF-3）。在 X＝ŷ、Y＝y 的座標中，Y 方向就是垂直方向，所以第 i 筆的區間是 x＝ŷᵢ 處、y 從 lowerᵢ 到 upperᵢ 的**垂直**範圍；點 (ŷᵢ, yᵢ) 落在自己的線段上，若且唯若 lowerᵢ ≤ yᵢ ≤ upperᵢ，也就是 R-CONF-4 的覆蓋判定。只有把軸對調（X＝實際）時區間才應該是水平的。v1.0 的「x 軸預測、y 軸實際、垂直線段」因此是一致的組合，finding 主張的矛盾不存在。v1.0 未明寫的是：區間位於 x＝ŷ、以 y＝x 為（log 尺度上的）中心，不是以觀測點為中心；v1.1 在 R-EVAL-2 與 AC-15 的 FAIL 例中寫明。

**可讀性（CONFIRMED）。** 以只用 Fit 的模擬量測（方法見 3.8 節；**沒有使用 Calibration 或 Test**，以免設計決定接觸 Test，INV-2、R-EVAL-3）：在 OC §2.4.2 的公式下，畫 5,194 筆 Sales（比 n_test ≈ 4,300 更密），比較四種畫法：

| 畫法 | 觀察 |
| --- | --- |
| 逐筆垂直線段＋線性刻度 | 價格範圍 75,000～7,700,000 USD 右偏，大多數點與線段擠在左下角約八分之一的面積內。 |
| 逐筆垂直線段＋log 刻度 | 線段合併成一條實心帶，區間內的點被遮住，只看得到區間外的點。 |
| 帶狀區域＋線性刻度 | 扇形帶，仍擠在左下角。 |
| 帶狀區域＋log 刻度 | 寬度固定（2q̂）、與 y＝x 平行的帶；區間內、外的點與參考線都清楚可見。 |

**裁決**：保留全部 Test Sales（抽樣會讓圖與圖說的 coverage 不再對應同一組 Sales，並引入另一個隨機選擇）；兩軸 log 刻度；區間以 `lower(x)=x·e^(−q̂)`、`upper(x)=x·e^(q̂)` 在 ŷ 的範圍內畫成帶狀區域。因為區間只取決於 ŷ，帶在 x＝ŷᵢ 的垂直切片恰為第 i 筆的區間，帶等於全部逐筆區間的聯集，資訊與 v1.0 相同；不另畫逐筆線段。點依 R-CONF-4 同一判定著色，標為區間內的點數 MUST 等於 coverage × n_test，使圖與數值可以互相核對。

**Boundary**：OC-A5 的 PASS 是「有預測圖（實際 vs 預測，附上下界，USD）」；上位契約是「預測圖(加上信賴區間或預測區間)」。帶狀區域就是上下界；log 刻度的刻度值仍是 USD。v1.0 已允許 log 刻度，v1.1 把它從 MAY 改為固定。屬 derived contract 的設計修訂（治理 §5.3 第 2 類）。

### 3.2 F-02 計算規模與可行性

**規模（CONFIRMED）。** 每個 outer fold：C2 forward 評估 18＋17＋…＋1＝171 個 group 子集；C3 backward 評估起點的全模型加 18＋17＋…＋2，同為 171 個；每個子集 5 次 inner fit，各 855 次。C4 為 25×5＝125 次，C5 為 26×5＝130 次；加上 C1 與各候選在 outer 訓練列上的最終 fit 5 次，共約 1,970 次。5 個 outer folds 約 9,850 次；frozen predictor 在整個 Fit 重跑，最多再加約 856 次（C2 或 C3）。總數約 1.0～1.07 萬次，與 finding 相符。

**可行性量測（HIGH 執行風險不成立）。** 方法見 3.8 節。

| 項目 | fit 次數 | 預設執行緒 | 單執行緒 |
| --- | --- | --- | --- |
| (A) scikit-learn `Pipeline`（`ColumnTransformer`＋`LinearRegression`）逐子集重新 fit，forward，outer fold 0 | 855 | 11.27 s（13.2 ms／次） | 11.06 s |
| (B) 每個 inner 訓練集 encode 一次、`numpy.linalg.lstsq` 解子集，forward＋backward，5 個 outer folds | 8,550 | 124.7 s | 111.8 s |
| Ridge，25 個 `alpha`，outer fold 0 | 125 | 0.66 s | 0.61 s |
| Lasso，26 個 `alpha`，cold start（`max_iter=100000`、`tol=1e-4`），outer fold 0 | 130 | 12.07 s | 11.73 s |
| Lasso，warm start 沿網格，outer fold 0 | 130 | 8.54 s | 8.31 s |

- 推估整個 nested CV（逐子集 pipeline 的直接做法）：forward＋backward 約 111 s，Ridge 約 3 s，Lasso 約 59 s，frozen predictor 重跑最多約 25 s，合計約 3～4 分鐘。即使在慢 5 倍的機器上也在 20 分鐘內。
- Lasso 在全部 26 個 `alpha` 都收斂：最大迭代 1,397 次（上限 100,000），沒有 `ConvergenceWarning`。R-CAND-5 的不收斂風險（Spec §9.2）在本資料上低。
- 在這個矩陣大小下，(B) 的 `lstsq` 沒有比 (A) 快；最佳化不是必要條件。

**裁決**：不需要任何最佳化，也不需要放寬任何要求。為了防止 Executor 以「最佳化」之名弱化 CV 或選擇，新增 Spec §4.5，明列：

- **允許的等價最佳化**（HOW，可不採用；採用時以 R-TEST-6 證明與逐子集 pipeline 的結果相同）：每個訓練集只 fit 一次前處理並重用 encoded 矩陣（one-hot 類別與標準化參數只取決於該訓練集的列、逐欄計算，取欄與重新 encode 相同）；任何得到最小平方解的 OLS 解法；Lasso 在同一訓練集內 warm start（每個 `alpha` 仍須收斂）；與順序無關、以固定順序彙整的平行計算。
- **不允許的簡化**：減少 folds、縮小網格、對列抽樣、提前停止 forward／backward 或略過 group、以 p-value、AIC／BIC、非 group-aware CV 或近似公式取代 inner-CV USD RMSE、以 outer 訓練列 fit 的前處理用於 inner folds、在驗證的執行中載入先前的選模結果。

**Boundary**：只界定 HOW 的範圍，R-PART-3、R-PART-4、R-CAND-2～R-CAND-6 的語義不變。

### 3.3 F-03「Test 只評估一次」

**評估（CONFIRMED）。** OC §2.4.1 寫「Test 在 predictor 凍結後只評估一次」；OC-A6 要求「從乾淨環境完整重跑 notebook 成功，重跑的數值與報告一致」；notebook 的 Evaluation 章節含 Test 評估（OC-A2、OC-A4）。兩條同時成立的唯一讀法是：**每次執行**在凍結後恰有一次 Test 評估，且 Test 結果不回饋任何決定（OC §3.4「以 Test 或 Calibration 選模」為 FAIL）。若讀成「整個專案只能評估一次」，OC-A6 的完整重跑就無法成立。v1.0 已採此讀法（INV-2「每次執行恰有一次」；derivation record TB-3），但 AC-09 的「可以重複評估」與 AC-14 的「有兩次 Test 評估」沒有限定在同一次執行，與 R-REPRO-2（連續兩次執行）、R-PKG-4（解壓驗證）字面上互相衝突；「一次執行」也沒有定義。

**裁決**：

- R-SEL-4 定義「一次執行」：從 `partitioned` 開始、建立一份新 manifest 的完整流程；每次執行建立新 manifest，不得附加到舊的。
- 新增 R-EVAL-1a：重複執行同一套固定設計是重現，不是新的評估，條件是 (a) 第 4.1 節的固定參數與 H-3 範圍程式沒有因 Calibration 或 Test 結果改變；(b) 報告與 README 的 Test 數值只來自最終驗證執行，不得從多次執行中挑選；(c) 自任何一次執行第一次到達 `test_evaluated` 起，H-3 範圍程式的每次修改，所屬 Ticket 的 worklog 寫明理由與依據（依據不得是 Calibration 或 Test 的結果）。
- AC-09、AC-14 的 FAIL 例限定為「同一次執行」，並加入「新的執行附加到舊 manifest」「從多次執行中挑選」；AC-20、INV-2 加註。

(c) 是 R-EVAL-3「Test 結果不得成為任何決定的輸入」的可觀察證據；沒有它，Reviewer 無法核對開發期間在看過 Test 結果之後的修改。它只要求 worklog 的一行說明，不新增 gate 或 audit round（治理 §3.7 的 worklog 本來就是 MUST）。

**Boundary**：釐清 OC 已接受語義的唯一合理讀法，並補上證據形式；不改變 accepted 語義。

### 3.4 F-04 Full column rank 的檢查範圍

**評估（CONFIRMED）。** v1.0 R-PREP-2 只要求「在 Fit 上 encode 後的 design matrix」為 full rank，但 OLS 實際在每個 outer 與 inner 訓練集上 fit，前處理參數也各自由該訓練集 fit（R-PREP-3）；fold 層級的秩不足不會被 v1.0 的檢查發現。

**量測**（方法見 3.8 節，只用 Fit）：31 個訓練矩陣（整個 Fit 12,974 列；5 個 outer 訓練集；25 個 inner 訓練集）以各自的前處理 encode 後加截距，都是 88 欄（截距 1＋非 one-hot 18＋`zipcode` one-hot 69），秩全部為 88；最大條件數約 365；任一訓練集中最少的 `zipcode` 類別有 11 筆；`waterfront`＝1 最少 60 筆；沒有常數欄。實際的 fold 分配由實作產生（HOW），所以結果可能與本量測的分配不同，但邊際很大。

**裁決**：檢查對象改為這 31 個矩陣（frozen predictor 重跑的 inner 訓練集就是 outer 訓練集，不另計）。Candidate 子集不另外檢查：full column rank 矩陣的任何欄子集（含截距欄）仍是 full column rank。罕見類別：one-hot 類別取自訓練列，每個 one-hot 欄在訓練列中至少有一個 1；常數欄：非 one-hot 欄若在某訓練集為常數，標準化後是零向量，被同一檢查偵測。失敗時報錯並停止，route 至 DA，不得臨時刪欄、合併類別或改 encoding。結果記入 artifact，notebook 輸出摘要。R-TEST-2 加入對合成秩不足矩陣會報錯的測試。

**Boundary**：D-1（OC §5「完全共線的處理方式」）既有設計的驗證範圍，不改變 accepted 語義。

### 3.5 F-05 Outer-CV tie-break

**評估（CONFIRMED）。** v1.0 R-SEL-2 寫「兩者差的絕對值 < 0.5 USD 視為平手，依偏好順序取較前者」，是成對關係，不具遞移性。例：平均 RMSE 為 100.0（C4）、100.4（C2）、100.8（C1）時，C4～C2、C2～C1，但 C4 與 C1 不平手；依比較順序不同，結果可以是 C1 或 C2。

**裁決**：以最小值為錨點。m＝最小平均 RMSE；平手集合 T＝{ 平均 RMSE − m < 0.5 USD }（未四捨五入的浮點值）；選 T 中偏好順序 C1、C2、C3、C4、C5 最前者。上例 T＝{C4, C2}，選 C2。兩個候選時與 v1.0 相同。Artifact 記錄 m、T 與選出者；R-TEST-6 涵蓋鏈狀接近、只有最小者、多個在範圍內三種情況。

**Boundary**：OC §5 明列 tie-break 為 DA 的設計事項；OC-A4 只要求「選擇規則與 tie-break 有文件」。不改變 accepted 語義。

### 3.6 F-06 檔頭

**CONFIRMED**：v1.0 檔頭「Tickets：尚未 derive」在 commit `323d3de5`（Tickets #50–#56）之後已不正確。v1.1 改寫檔頭的版本與 Tickets 欄，§0 的 activation 前提註記 Tickets 已完成。

### 3.7 附加問題：AC-23 的逐句對照

**評估（REJECTED：不是不必要的複雜度）。**

- OC-A7 的證據要求明寫「摘要與原始材料的對照」；OC §3.5 的驗證也列出「摘要與原始材料的對照」；OC §2.5.1 規定「摘要必須可追溯到原始材料與來源連結」，FAIL 條件是「摘要含原始材料沒有的內容」。
- 這個 FAIL 條件是逐個論點的性質；要讓它可觀察，對照的單位必須細到能看出每個論點的出處。句子是摘要中最小的自然單位。「NotebookLM 摘要」約 100～300 字，對照表約 4～10 列，成本低。
- 改成段落層級或取消對照表，會降低 OC-A7 證據的可觀察性，屬弱化已接受的證據要求；本裁決不做。
- 對照表也不取代 Reviewer 的直接比對（高風險裁決 A-3）：它是 Executor 的 self-verification 證據，Reviewer 仍自行讀原始材料。

**裁決**：要求不變。為了不讓「材料中的位置」被理解成需要複雜的格式，v1.1 在 R-AI-2 釐清：每一列是「摘要的一句 → 支撐它的材料位置」；位置是材料檔名加上可定位的頁碼、段落或標題，或支撐該句的原文摘錄（翻譯的句子對回原文）；格式不限，不需要其他欄位。AC-23 引用之。

### 3.8 量測方法（一次性，不在 repository 內）

- **環境**：scratchpad（session `8943ecf6`）內新建的一次性虛擬環境：Python 3.11.2、numpy 2.4.6、pandas 3.0.6、scikit-learn 1.9.1、matplotlib 3.11.2；Windows 11，32 個邏輯 CPU。腳本 `scratchpad/da_f02/measure.py` 與 `plot_probe.py`，以 `python -I` 執行，資料路徑以參數傳入；沒有在 repository 內新增或修改任何檔案。單執行緒的數值以 `OMP_NUM_THREADS`、`OPENBLAS_NUM_THREADS`、`MKL_NUM_THREADS`＝1 量測。
- **資料**：`scratchpad/kc_probe/dl.bin`（Brief §10 的 archive），在記憶體中讀取 `kc_house_data.csv`，核對 CSV sha256＝`d0875baa…7b7e`（Spec R-DATA-1 的固定值）。
- **分區**：依 Spec R-PART-2 的演算法（唯一 `id` 升序、`default_rng(2026)` permutation、前 `round(0.6·H)` 個 House 為 Fit），得到 12,862 個 House、12,974 列。**Calibration 與 Test 的列在分區後立即丟棄，其目標值沒有被讀取或建模。**
- **Folds**：以 permutation 指派的 group-aware 5-fold（`default_rng([2026, 0])` 為 outer；`default_rng([2026, 1, j])` 為 outer fold j 內的 inner）。這是 Spec §4.2 允許的 HOW 之一，不是對實作的指定。
- **前處理**：R-PREP-1、R-PREP-3（`sqft_basement` 不用；非 one-hot 欄以訓練列標準化；`zipcode` one-hot、drop first）；目標 `ln(price)`；inner 準則為 USD RMSE。
- **可讀性模擬**：在 outer folds 3、4 上 fit 全部 18 個 group 的 OLS，以 fold 2 依 R-CONF-2 的公式算 q̂，畫 folds 0、1 的 5,194 筆 Sales，四種畫法見 3.1 節。模擬中的選擇結果、q̂ 與 coverage 都只是 Fit 內部的量測，不構成任何結果，也不記入 Spec 或報告。

## 4. 是否改變 accepted 語義；boundary determination

**否。** 每一項都屬治理 §5.3 第 2 類（derived contract 的設計、修訂與 clarification）：

| 變更 | 依據的 OC 條款 | 判定 |
| --- | --- | --- |
| R-EVAL-2、AC-15（F-01） | OC-A5「預測圖（實際 vs 預測，附上下界，USD）」；M3 | 在 boundary 內：上下界與 USD 都保留；呈現方式是 DA 的設計。 |
| Spec §4.5、R-TEST-6（F-02） | OC E4、§2.4.1 | 在 boundary 內：只界定 HOW，CV 與選擇的語義不變。 |
| R-SEL-4、R-EVAL-1a、AC-09、AC-14、AC-20、INV-2（F-03） | OC §2.4.1、§3.4、OC-A6 | 在 boundary 內：OC 條文唯一一致的讀法；v1.0 已採用。 |
| R-PREP-2、R-TEST-2、AC-12（F-04） | OC §5（完全共線） | 在 boundary 內：既有設計的驗證範圍。 |
| R-SEL-2、D-4、AC-12、R-TEST-6（F-05） | OC §5（tie-break）、OC-A4 | 在 boundary 內：OC 明文交由 DA 設計。 |
| 檔頭、§0（F-06） | — | 編輯性。 |
| R-AI-2、AC-23（附加） | OC §2.5.1、OC-A7、§3.5 | 在 boundary 內：要求不變，只釐清形式。 |

- AC 的編號與數量（AC-01～AC-31）不變；OC-A1～OC-A8 的分配不變（derivation record 第 4 節）；沒有新增 scope、acceptor gate 或 audit round。
- **Contract change**：無。**Fail-closed 至 acceptor 的 boundary 問題**：無。

## 5. Capability escalation 檢查（Bindings b5 §3.2 E-DA）

- **(D1)**：沒有「兩個以上合理設計的後果實質不同、且以現有證據無法裁決」的問題。F-01 的帶狀區域與逐筆線段在數學上等價，差別只在可讀性，已以量測裁決；F-02 的可行性已量測；F-03 只有一種與 OC 一致的讀法；F-04 的子集推論是線性代數事實；F-05 以最小值為錨點是唯一保留 v1.0「0.5 USD＝整數精度無法區分」且具決定性、兩個候選時與 v1.0 相同的規則。
- **(D2)**：不成立。這些 findings 來自 acceptor 要求的 pre-implementation review，不是 FA ruling，也不是經 route 的治理 Reviewer finding（本單元尚無任何 audit record）；且只有 F-01 主張先前的 DA 決定有誤，該主張已以 3.1 節的推導反駁。若之後有經 route 的治理 Reviewer 以證據再次爭議 R-EVAL-2 的圖形語義，該問題即符合 (D2)，應以 E-DA 重派，而不是由本 DA 再裁決。

## 6. 對進行中工作、dependencies 與 evidence 的影響

| 項目 | 影響 |
| --- | --- |
| 進行中的工作 | **無。** 2026-10-14 核對：`home_work_02/` 沒有實作檔案、沒有 `doc/governance/worklog/`、`audit/`、`run/`；Issues #50–#56 皆 OPEN、沒有 comment；Orchestrator 尚未啟動。沒有既有 evidence 或 audit 結論需要重做。 |
| Tickets | 七張票的 Spec 引用改為 v1.1（v1.0 已不是有效版本）。內容變更：#51（F-02、F-04、F-05）、#52（F-01、F-03）、#53（F-03、F-04 的 notebook 輸出）；#50、#54、#55、#56 只改版本引用並加註。AC 的分配與「Blocked by」不變。 |
| Dependencies | 不變：#50 → #51 → #52 → #53 → #54 → #55 → #56；acceptor 輸入不變（Spec §9.1）。 |
| AC → Ticket 覆蓋 | 不變（derivation record §13.2）。新增的 R-EVAL-1a 由 #52（第一次執行）、#53（重現與 notebook）、#56（最終重跑）承接，與 AC-09、AC-14、AC-20 的既有分配相同。 |
| 高風險裁決 | 不修改。R-EVAL-1a、R-EVAL-2 已在 H-3 的「R-EVAL-\*」與 H-2 的範圍內；A-2 的 Reviewer 獨立重算不變。 |
| Ticket 索引 | 來源 Spec 改為 v1.1，加註本紀錄。 |
| Outcome Contract、Brief、`CONTEXT.md`、上位契約、Bindings | 不修改。 |

## 7. 寫入的檔案與外部動作

| 對象 | 動作 |
| --- | --- |
| `home_work_02/doc/spec/SPEC.md` | v1.0 → v1.1（修訂處標示「（v1.1）」；第 10 節版本紀錄） |
| `home_work_02/doc/governance/decisions/decision-20261014-spec-v1-1-review-findings.md` | 新增（本檔） |
| `home_work_02/doc/governance/decisions/derivation-SPEC.md` | 只新增：第 12 節一列、第 14 節 |
| `home_work_02/doc/ticket/tickets.md` | 來源 Spec 改為 v1.1，加註修訂 |
| GitHub Issues #50–#56 | 以 `gh issue edit --body-file` 修改 body：Spec 版本引用、各票受影響的條文、文末「修訂紀錄」一節 |

未實作；未 commit；未執行 git 寫入操作；量測腳本與圖只在 scratchpad。
