# Spec: HW2 Multiple Linear Regression — King County 房價（`home_work_02/`）

- **專案識別**：`home_work_02`（老師稱 HW2: Multiple Linear regression）
- **Spec 版本**：**v1.0**（2026-10-14，Design Authority derive）
- **Derived 自**：Outcome Contract [`../governance/outcome-contract.md`](../governance/outcome-contract.md)。Accepted normative 內容＝第 1–8 節於 commit `e2153254ccf7a97475d1c22e10d6a1e0717c5497`；接受紀錄＝第 9 節於 commit `370c0ae1bf40385baa1d954c6585d1c175b4124b`。
- **上位契約**（唯讀）：[`../requirement/HW2-requirements-Multiple Linear regression.txt`](../requirement/HW2-requirements-Multiple%20Linear%20regression.txt)（sha256 `a969e7e2…61ab`）
- **討論紀錄**（不具 authority；與 OC 不一致時以 OC 為準）：[`../brief/HW2_Grill_Brief_Draft_v0.3.md`](../brief/HW2_Grill_Brief_Draft_v0.3.md)；詞彙 [`../../CONTEXT.md`](../../CONTEXT.md)
- **Derivation record**：[`../governance/decisions/derivation-SPEC.md`](../governance/decisions/derivation-SPEC.md)
- **相關裁決**：[`../governance/decisions/decision-20261014-lane.md`](../governance/decisions/decision-20261014-lane.md)（Formal）、[`../governance/decisions/decision-20261014-high-risk-categories.md`](../governance/decisions/decision-20261014-high-risk-categories.md)（H-1～H-4）
- **Tickets**：尚未 derive（由後續 DA 派工自本 Spec derive；Ticket 本體在 GitHub Issues，索引在 `doc/ticket/`）

## 0. 狀態與效力

| 項目 | 內容 |
| --- | --- |
| 狀態 | **EFFECTIVE（自 2026-10-14）。** Outcome Contract 已於 2026-10-14 由 acceptor 接受。本 Spec 是在其 boundary 內 derive 的 derived contract，成立不需要 acceptor 逐份核准（治理 §1.2）。Boundary determination 見 derivation record 第 3 節。 |
| 重新 derive 條件 | Outcome Contract 第 1–8 節的 scope、constraints、acceptance boundary 或 authority／authorization 條款有任何變更（contract change，治理 §5.3）時，本 Spec 須由 DA 重新 derive，或以 derivation record 的修訂確認不受影響；在此之前，不得依變更後的語義實作。 |
| 變更 | 不改變 accepted 語義的修訂由 DA 以 derivation／decision record 決定（治理 §5.3 第 2 類）；Tickets 與 Executors 不得重新定義本 Spec 的 AC、invariant 或固定的設計（第 4.1 節）。 |
| Activation 前提 | Tickets derive 完成；orch-default v2.2 §3 的其他前提成立。Bindings §8.2 #3 的 Fable probe 依 OC §9 acceptor 決定不阻擋。 |

**標記約定**

- 來源類型：**T** 老師要求（上位契約）｜**G** acceptor 的 Grill 決定或釐清（G1–G8、C1–C5，經 OC 承載）｜**P** OC 的 constraint 或治理約束（OC §2.3、§2.5、§4；Bindings）｜**D** 本 Spec 的設計決定（DA，在 OC boundary 內；理由見第 4.3 節）。
- Scope class：**MVM**、**ENHANCED**（OC §2.2）。OPTIONAL 與 REFERENCE 只出現在第 8 節。
- MUST／SHOULD／MAY 依治理用語。偏離 SHOULD 須在 worklog 寫明理由。
- `OC-An` 指 OC §3.1 的 acceptance boundary；`Mn`、`En` 指 OC §2.2 的項目；`Hn` 指高風險類別。
- 詞彙依 `CONTEXT.md`：Sale、House、Source feature、Encoded column、Fit／Calibration／Test partition、Candidate procedure、Frozen predictor、Prediction interval。

## Problem Statement

老師的 HW2 要求以 Kaggle 上一個有 10–20 個特徵的公開資料集，依 CRISP-DM 六階段完成多元線性回歸分析：必須做特徵選擇與模型評估，附有區間的預測圖，並提交以學號命名的 notebook、報告 PDF（含 GPT 對話、NotebookLM 摘要、主流解法比較）與 ZIP。

Outcome Contract 把這個要求具體化為：King County 房價資料（固定 CSV sha256）；在 Fit 分區上以 group-aware nested CV 公平比較五個 candidate procedures；凍結選出的 predictor；以獨立的 Calibration 分區產生 95% split conformal 預測區間；只在 Test 分區上評估一次；並如實陳述偏誤與 conformal 保證的假設。OC 也把八項設計事項留給 Spec（OC §5）。

目前 `home_work_02/` 只有文件，沒有任何實作。本 Spec 把 OC 的語義邊界與八項設計事項寫成可以直接分解為 Tickets、可以逐條驗收的契約。

## Solution

一個 notebook（主程式）呼叫一個小型 Python 套件 `mlr/`（data、selection、modeling、evaluation、conformal 五個模組），並使用隨附且以 sha256 固定的 CSV：

1. **Data**：載入並核對 checksum；以固定 seed 依 House 隨機分為 Fit／Calibration／Test（60／20／20），再於 Fit 上產生一組 group-aware outer 5-fold，所有候選共用。
2. **Modeling**：五個 candidate procedures 共用同一套前處理與 log 目標轉換：全特徵 LR、forward LR、backward LR、Ridge、Lasso。Forward 與 backward 以 source feature 為單位選擇；特徵數與 `alpha` 由 inner CV 決定。以 outer-fold 平均 USD RMSE 排序，選出的 procedure 在整個 Fit 上重跑，存檔並記錄 hash，成為 frozen predictor。
3. **Conformal 與 Evaluation**：在 Calibration 上計算 log 尺度的 conformal quantile，之後在 Test 上一次完成評估：指標、區間、coverage、寬度、預測圖。
4. **Deployment**：保存的 frozen predictor 加上一個回傳點預測與區間的函式。
5. **交付**：notebook 把所有數值寫入結果 artifact，報告以範本取用 artifact 的值，經 HTML 轉為 PDF，並附上 acceptor 的 ChatGPT 對話頁面；打包腳本以 acceptor 提供的學號產生 ZIP。acceptor 的原始材料與建置產物預設不進 git。

## User Stories

### 評分與交付

1. 作為評分老師，我打開 `<學號>_hw2.ipynb` 就能看到 CRISP-DM 六個階段，每階段都有實際內容與輸出。
2. 作為評分老師，我在報告中能找到資料集名稱、Kaggle 連結與授權，以及特徵數量的計算方式。
3. 作為評分老師，我能看到特徵選擇的過程與結果、模型比較表、Test 評估指標，以及附預測區間的預測圖。
4. 作為評分老師，我能在報告中找到標示為「GPT 輔助內容」與「NotebookLM 摘要」的段落、主流或更優解法的比較，以及 GPT 對話過程。
5. 作為評分老師，我收到的 `<學號>_hw2.zip` 解壓後就能安裝並重跑 notebook。

### 分析的讀者

6. 作為讀者，我能分辨哪些是老師的要求、哪些是專案自行延伸的做法。
7. 作為讀者，我能理解 outer-CV 分數為何對勝出者有樂觀偏誤，以及 Test 才是獨立估計。
8. 作為讀者，我能理解 95% 是名目目標、理論保證依賴 exchangeability 假設、observed coverage 只是一次分區的實證估計。

### 維護者與 acceptor

9. 作為 acceptor，我把 ChatGPT PDF、NotebookLM 材料放進指定的資料夾、提供學號，就能得到繳交套件；這些材料在我決定之前不會被公開到 GitHub。
10. 作為維護者，我依 README 在乾淨環境重跑，得到與報告相同的數字。
11. 作為 Reviewer，我能以自動化測試確認分區隔離、凍結順序與 conformal 計算，並以獨立的方式重算。

## 1. Requirements（R）

每條需求標示 ID、來源類型、class 與對應。

### 1.1 Data — 資料

| ID | 類型 | Class | 需求 | 對應 |
| --- | --- | --- | --- | --- |
| R-DATA-1 | G／D | ENHANCED | 資料檔 MUST 位於 `home_work_02/data/kc_house_data.csv`，納入 git 追蹤，sha256 等於 `d0875baa0251b21d4bdc9d2ae940a4fe0bb6009824f23dd0e2a5b2bf04557b7e`（Kaggle `harlfoxem/housesalesprediction`，CC0-1.0）。改用不同檔案是 re-pin，MUST 先有 DA decision record，並在 README 與報告中記錄。 | E9；OC §2.5、§5；OC-A1 |
| R-DATA-2 | P | MVM | 取得資料檔是一次性的實作動作：MUST 只使用匿名公開端點（例如 Brief §10 所用的 Kaggle 公開 API），MUST NOT 使用任何憑證（Kaggle CLI 的驗證、`kaggle.json`、`KAGGLE_*` 環境變數）。匿名取得失敗時，該路徑停止，改由 acceptor 提供檔案（RB-3：第三方帳號）。取得的 URL、日期、archive sha256 與 CSV sha256 記入 worklog。 | OC §2.5；RB-3；H-1 |
| R-DATA-3 | G | ENHANCED | 載入函式 MUST 在解析前計算檔案 sha256；與固定值不同時，以指明預期值與實際值的錯誤結束，不得退而使用其他檔案。解析後 MUST 驗證：欄位依序為 `id,date,price,bedrooms,bathrooms,sqft_living,sqft_lot,floors,waterfront,view,condition,grade,sqft_above,sqft_basement,yr_built,yr_renovated,zipcode,lat,long,sqft_living15,sqft_lot15`（21 欄，取自 Brief §10 的核對證據）；21,613 列；`id` 有 21,436 個唯一值；`sqft_living = sqft_above + sqft_basement` 對每一列成立。任一不符即報錯。 | E9；OC-A1；OC §5 |
| R-DATA-4 | T | MVM | Notebook 輸出與報告 MUST 載明：資料集名稱「House Sales in King County, USA」、連結 `https://www.kaggle.com/datasets/harlfoxem/housesalesprediction`、擁有者 `harlfoxem`、授權 CC0-1.0、檔名、CSV sha256（notebook 中為實際計算值）、列數與欄數。並依 OC §2.4.1 的規則陳述 source feature：列出 19 個 source features（CSV 欄位扣除 `id` 與 `price`），說明 encode 後的欄位不計；另列出建模使用的 18 個（不含 `sqft_basement`，理由見 R-PREP-2）；兩個數量都在 10–20。 | M1；OC-A1；H-2 |

### 1.2 Partition — 分區與 folds

| ID | 類型 | Class | 需求 | 對應 |
| --- | --- | --- | --- | --- |
| R-PART-1 | D | ENHANCED | 全部隨機性 MUST 來自單一常數 `SEED = 2026`，定義一次，分區、outer folds、inner folds 都由它衍生；不得有未設定 seed 的隨機性。 | E2、E8；OC-A6；H-3 |
| R-PART-2 | G／D | ENHANCED | 分區以 House 為單位：把唯一的 `id` 升序排序，以 `numpy.random.default_rng(SEED)` 作 permutation；前 `round(0.6·H)` 個 House 為 Fit，接著 `round(0.2·H)` 個為 Calibration，其餘為 Test（H＝21,436 → 12,862／4,287／4,287 個 House）。同一 House 的所有 Sales 同屬一個分區。三個分區沒有共同的 `id`，合起來恰好是全部 21,613 列。 | E2、E3；C1、C2；OC §2.4.1；OC-A3 |
| R-PART-3 | G | ENHANCED | Outer folds：在 Fit 上以 House 為單位產生 5 個 group-aware folds，只產生一次，並以「每個 Fit 列的 fold 編號」保存於結果 artifact；五個候選 MUST 使用同一組 outer folds。 | E4；C3；OC-A3、OC-A4 |
| R-PART-4 | G／D | ENHANCED | Inner folds：在每個 outer 訓練集內，以 House 為單位產生 5 個 group-aware folds，由 `SEED` 與 outer fold 編號決定；同一個 outer fold 內的所有候選 MUST 使用同一組 inner folds。Frozen predictor 在整個 Fit 上重跑時，inner folds＝R-PART-3 的 outer fold 分配。 | E4；C3；OC-A3；H-3 |
| R-PART-5 | G | ENHANCED | 選模與建模的函式 MUST 只接收 Fit 的列（或其 fold 子集）；Calibration 只傳給 conformal 校準，Test 只傳給 R-EVAL-1 的單次評估。Data Understanding 的分布性 EDA（圖、統計、相關、異常值計數）MUST 只用 Fit。全資料層級的結構事實（R-DATA-3、R-DATA-4 列出的形狀、欄位、缺值、唯一 `id`、重複交易數、`sqft` 恆等式、日期範圍）可以引用全資料。 | E2；OC §2.4.1；OC-A3；H-3 |

### 1.3 Preprocessing — 前處理

| ID | 類型 | Class | 需求 | 對應 |
| --- | --- | --- | --- | --- |
| R-PREP-1 | D | ENHANCED | 固定（不 fit）的逐列轉換，對所有候選相同：(a) `date`（字串 `YYYYMMDDT000000`）→ `sale_days`＝距固定日期 2014-05-01 的天數（整數）；(b) `yr_renovated` → `is_renovated`（`yr_renovated > 0` 為 1，否則 0）與 `effective_year`（`yr_renovated > 0` 時為 `yr_renovated`，否則為 `yr_built`），兩欄都屬於 source feature `yr_renovated`；(c) `zipcode` 視為類別（nominal），不當作數值大小；(d) `sqft_basement` 不進入 design matrix（R-PREP-2）；(e) `id` 只作為 group key，`price` 只作為目標；(f) 其餘 source features（`bedrooms`、`bathrooms`、`sqft_living`、`sqft_lot`、`floors`、`waterfront`、`view`、`condition`、`grade`、`sqft_above`、`yr_built`、`lat`、`long`、`sqft_living15`、`sqft_lot15`）照原值使用。 | OC §5（`date`、`zipcode`、離群值與重新編碼）；Brief §5.1 |
| R-PREP-2 | D | MVM | 完全共線：`sqft_basement` 不進入 design matrix，因為每一列都滿足 `sqft_basement = sqft_living − sqft_above`（R-DATA-3），線性模型的欄空間不變、沒有資訊損失。在 Fit 上 encode 後的 design matrix 加上截距 MUST 為 full column rank，以自動化檢查確認並在 notebook 輸出。 | M2；OC §5（完全共線）；Brief §5.1 |
| R-PREP-3 | D | ENHANCED | 有參數的前處理放在 pipeline 內，只以該次 fit 呼叫的訓練列 fit：(a) `zipcode` one-hot，類別取自訓練列，依排序 drop 第一個類別；預測時遇到未見過的類別，編為全零（即基準類別）；(b) 其他 encoded columns 以訓練列的平均與標準差標準化；one-hot 欄不縮放。五個候選使用完全相同的前處理。 | E2、E4；OC §2.4.1；OC-A3；H-3 |
| R-PREP-4 | D | MVM | 離群值：任何分區都不刪除任何列，也不對特徵值作 clipping 或 winsorizing。Data Understanding MUST 以 Fit 的資料列出觀察到的異常（例如 `bedrooms` 的極端值與 0、`bathrooms` 為 0、`yr_renovated` 的 0 表示「未整修」），Data Preparation MUST 說明不刪除的理由（第 4.3 節 D-5）。 | OC §5（離群值）；OC-A3「合起來涵蓋全部列」 |
| R-PREP-5 | D | ENHANCED | 除了 R-PREP-1～R-PREP-3，不得加入其他特徵轉換（特徵的 log、多項式、交互作用、額外衍生欄位）。需要時 MUST 先有 DA decision record，且理由不得來自 Calibration 或 Test。 | E1；OC §2.3；H-3 |
| R-PREP-6 | G／D | ENHANCED | 目標：模型以 `ln(price)` 訓練；點預測 ŷ＝`exp(f(x))`（USD）。**不作偏誤修正**（不乘 smearing 或 `exp(σ²/2)` 等因子），對所有候選相同。報告 MUST 說明 ŷ 估計的是條件中位數（在 log 誤差對稱時），不是條件平均，並說明 USD 指標是針對這個點預測計算的。 | E5；C4；OC §5（偏誤修正）；Brief §5.3 |

### 1.4 Candidates — 五個 candidate procedures

Source-feature group：選擇的單位。建模使用的 18 個 group 依 CSV 欄位順序為 `date`、`bedrooms`、`bathrooms`、`sqft_living`、`sqft_lot`、`floors`、`waterfront`、`view`、`condition`、`grade`、`sqft_above`、`yr_built`、`yr_renovated`、`zipcode`、`lat`、`long`、`sqft_living15`、`sqft_lot15`。每個 group 包含它的全部 encoded columns（例如 `zipcode` 的全部 one-hot 欄，`yr_renovated` 的兩欄）。這個順序稱為 **canonical order**。

| ID | 類型 | Class | 需求 | 對應 |
| --- | --- | --- | --- | --- |
| R-CAND-1 | G | MVM | **C1 `lr_all`**（multiple LR baseline）：18 個 group 全部使用的 OLS（有截距），沒有選擇。 | M2；E1；G1 |
| R-CAND-2 | G／D | MVM | **C2 `lr_forward`**：從只有截距開始，每一步加入使 inner-CV 平均 USD RMSE 最小的 group，得到 k＝1…18 的巢狀路徑與每個 k 的 inner-CV RMSE；選 inner-CV RMSE 最小的 k，再以該子集在該次訓練列上重 fit OLS。 | M2；E1、E4；C3 |
| R-CAND-3 | G／D | MVM | **C3 `lr_backward`**：從 18 個 group 開始，每一步移除使 inner-CV 平均 USD RMSE 最小的 group，得到 k＝18…1 的路徑；選法同 R-CAND-2。 | M2；E1、E4；C3 |
| R-CAND-4 | G／D | ENHANCED | **C4 `ridge`**：18 個 group 全部使用；`alpha` 從固定網格 `numpy.logspace(-3, 3, 25)` 以 inner CV 選擇（scikit-learn `Ridge` 的 `alpha` 定義）。 | E1、E4；C3 |
| R-CAND-5 | G／D | ENHANCED | **C5 `lasso`**：18 個 group 全部使用；`alpha` 從固定網格 `numpy.logspace(-6, -1, 26)` 以 inner CV 選擇（scikit-learn `Lasso` 的 `alpha` 定義）。被選中的 `alpha` 擬合時 MUST 收斂（以足夠的 `max_iter`）；收斂警告記入結果 artifact。 | E1、E4；C3 |
| R-CAND-6 | D | ENHANCED | Inner-CV 準則：inner folds 的平均 RMSE，以 USD 計算（對 `exp` 轉回的預測）。Tie-break（以浮點完全相等判定）：k 取最小者；`alpha` 取最大者；同一步中多個 group 的分數相同時，取 canonical order 較前者。 | E4；OC §5（tie-break）；H-3 |
| R-CAND-7 | D | ENHANCED | 網格邊界：任一次 fit 選中的 `alpha` 等於網格最小值或最大值時，MUST 在結果 artifact 與報告中標示；這不是 FAIL。改變網格 MUST 先有 DA decision record，且理由不得來自 Calibration 或 Test。 | E4；H-3 |
| R-CAND-8 | G | MVM | 選擇與調參只依 CV 誤差；MUST NOT 使用 p-value、顯著性檢定或 Test 結果（參考實作的 p-value backward elimination 不是本作業的方法）。 | OC §2.3；OC-A4；Brief §5.3 |

### 1.5 Selection — 比較、選模與凍結

| ID | 類型 | Class | 需求 | 對應 |
| --- | --- | --- | --- | --- |
| R-SEL-1 | G | ENHANCED | 對每個 outer fold j 與每個候選：在 outer 訓練列上執行整個 procedure（含 inner CV），預測 outer 驗證列，計算 USD 的 RMSE、MAE、MSE、R²。結果 artifact 記錄每個 fold 的四個指標，以及 C2、C3 選中的 k 與 groups、C4、C5 選中的 `alpha`、C5 的非零係數數。 | E4；C3、C4；OC-A4 |
| R-SEL-2 | G／D | ENHANCED | 排序依 5 個 outer folds 的 RMSE 平均值；選最小者。兩者差的絕對值 < 0.5 USD（即在報告的整數 USD 精度下無法區分）視為平手，依偏好順序 C1、C2、C3、C4、C5 取較前者。比較表 MUST 列出每個候選四個指標的平均與標準差。 | E4；G2；OC §5（tie-break）；OC-A4 |
| R-SEL-3 | G | ENHANCED | 凍結：選出的 procedure 在整個 Fit 上重跑（inner folds 依 R-PART-4），存成 `results/` 下的單一檔案，計算其 sha256，並在 run manifest 記錄「frozen」事件（procedure、檔案、sha256），之後才可進行任何 Calibration 或 Test 的預測。記錄 frozen predictor 選中的 groups 或 `alpha`。 | E2；OC §2.4.1；OC-A3、OC-A4；H-3 |
| R-SEL-4 | G | ENHANCED | Run manifest：同一次執行依序附加的事件紀錄，至少有 `partitioned`、`outer_cv_done`、`selected`、`frozen`、`calibrated`、`test_evaluated`，每個事件有序號與必要的識別值（例如 frozen 的 sha256、calibrated 的 n_cal 與 q̂）。 | OC-A3 證據「識別與 Test 評估的順序」 |

### 1.6 Conformal — 預測區間

| ID | 類型 | Class | 需求 | 對應 |
| --- | --- | --- | --- | --- |
| R-CONF-1 | G | ENHANCED | 以 frozen predictor（載入 R-SEL-3 的檔案並核對 sha256）預測 Calibration；每一筆 Sale 的分數 `s = abs(ln y − ln ŷ)`（自然對數，與訓練相同）。n_cal 為 Calibration 的 Sale 數。 | E6；G3、C4；OC §2.4.2 |
| R-CONF-2 | G | ENHANCED | `α = 0.05`；`k = ⌈(n_cal + 1)(1 − α)⌉`；q̂＝分數由小到大的第 k 個（從 1 起算）。k > n_cal 時 q̂＝+∞，並在報告中說明（以本資料的 n_cal 不會發生）。記錄 n_cal、k、q̂、`exp(q̂)`。 | E6；OC §2.4.2 |
| R-CONF-3 | G | ENHANCED | 區間（USD）＝`[ŷ·exp(−q̂), ŷ·exp(q̂)]`。 | E6；OC §2.4.2 |
| R-CONF-4 | G | ENHANCED | Observed coverage＝Test Sales 中 `lower ≤ y ≤ upper` 的比例（閉區間）；平均寬度＝`mean(upper − lower)`（USD）；同時記錄 n_test，以及描述性的抽樣誤差幅度 `1.96·sqrt(0.95·0.05/n_test)`。 | E6；OC §2.4.2；OC-A5 |
| R-CONF-5 | P | ENHANCED | Calibration 只用於 R-CONF-1～R-CONF-2，不用於任何 fit 或選擇。不實作 OC §2.4.2 以外的 conformal 方法（含以 House 為單位的 conformal）。 | OC §2.3、§2.4.2；H-3 |

### 1.7 Evaluation — Test 評估與預測圖

| ID | 類型 | Class | 需求 | 對應 |
| --- | --- | --- | --- | --- |
| R-EVAL-1 | G | MVM | Test 評估是單一函式呼叫，只在 manifest 已有 `frozen` 與 `calibrated` 事件、frozen 檔案的 sha256 與紀錄相同、且本次執行尚無 `test_evaluated` 事件時才執行，否則報錯。一次呼叫內完成：點預測、USD 的 R²、MAE、MSE、RMSE、區間、coverage、平均寬度。 | M2；E2、E6；OC-A3、OC-A4、OC-A5；H-3 |
| R-EVAL-2 | T／G | MVM | 預測圖（USD）：Test Sales；x 軸為預測價格、y 軸為實際價格；每筆 Sale 以垂直線段標出 `[lower, upper]`；畫 y＝x 參考線；落在區間外的點以不同顏色標示；可以使用 log 刻度（須在圖說註明）；標題、軸標籤與圖說為 zh-TW，軸標籤含「USD」；圖說寫明名目 95%、observed coverage 與 n_test。存為 `results/` 下的 PNG，notebook 與報告都顯示。zh-TW 字元不得出現缺字方塊。 | M3；E6；OC-A5；H-2 |
| R-EVAL-3 | G | ENHANCED | Test 的任何結果 MUST NOT 成為任何設計或實作決定的輸入（procedure、特徵、轉換、網格、seed、前處理、tie-break）。 | OC §2.4.1；OC §3.4；H-3 |
| R-EVAL-4 | D | ENHANCED | Notebook MAY 加入只使用 Fit outer-fold 預測的診斷圖（例如殘差圖）；不得使用 Calibration 或 Test。這些圖沒有對應的 AC。 | OC §2.2 OPTIONAL（只限 Fit） |

### 1.8 Deployment — CRISP-DM 的部署階段

| ID | 類型 | Class | 需求 | 對應 |
| --- | --- | --- | --- | --- |
| R-DEP-1 | D | MVM | `mlr` MUST 提供一個預測函式：輸入為原始 schema 的列（source feature 欄位），載入 frozen predictor 檔案並核對 sha256，使用結果 artifact 記錄的 q̂，回傳每列的點預測與區間下界、上界（USD）。 | M4（Deployment）；Brief §6 |
| R-DEP-2 | D | MVM | Notebook 的 Deployment 章節以人工建構的範例，或 Fit 的列，示範 R-DEP-1（不得使用 Calibration 或 Test 的列），並寫明使用限制：King County、2014-05～2015-05 的交易；coverage 是 marginal 的；依賴 exchangeability 假設；超出資料範圍屬外推。 | M4；OC §2.4.2 |
| R-DEP-3 | P | — | 不建立 Web App、API、資料庫或 MLOps。 | OC §2.3 |

### 1.9 Notebook — 主程式

| ID | 類型 | Class | 需求 | 對應 |
| --- | --- | --- | --- | --- |
| R-NB-1 | T | MVM | `home_work_02/hw2.ipynb` MUST 有六個依序的頂層章節，標題含階段英文名稱（Business Understanding、Data Understanding、Data Preparation、Modeling、Evaluation、Deployment），可另附 zh-TW 名稱；每章節的內容至少包含第 4.4 節的清單項目。 | M4；OC-A2；H-2 |
| R-NB-2 | G | ENHANCED | Notebook 是主程式：負責呼叫 `mlr` 的函式、顯示輸出與說明；資料、選擇、建模、評估、conformal 的邏輯 MUST 在 `mlr` 模組內。 | E7；G5 |
| R-NB-3 | D | ENHANCED | Notebook 執行時把全部報告用的數值寫入 `results/` 的結果 artifact（JSON），連同 run manifest、圖檔、frozen predictor 檔案。 | OC-A6；H-3 |
| R-NB-4 | G | ENHANCED | Notebook MUST 能以非互動方式（例如 `jupyter nbconvert --to notebook --execute`）從頭執行到尾，不需要網路。Git 追蹤的 `hw2.ipynb` 與 `results/` MUST 是最終程式碼在乾淨環境重跑（AC-20）的輸出。 | E8；OC-A6 |
| R-NB-5 | P | MVM | Notebook 的 Markdown 說明為 zh-TW；程式識別字與技術名詞可保留英文。 | OC §2.5；OC §9 |

### 1.10 Report — 報告

| ID | 類型 | Class | 需求 | 對應 |
| --- | --- | --- | --- | --- |
| R-RPT-1 | T | MVM | 報告（PDF，zh-TW）MUST 包含：CRISP-DM 六個依序章節（標題規則與內容清單同 R-NB-1、第 4.4 節）；資料集來源與研究脈絡；「GPT 輔助內容」節（R-AI-1）；「NotebookLM 摘要」節（R-AI-2）；主流或更優解法比較節（R-AI-3）；scope class 標示（R-RPT-5）；參考資料；附錄 GPT 對話過程（R-AI-4）。 | M4–M8；OC-A2、OC-A7；H-2 |
| R-RPT-2 | G | ENHANCED | 偏誤陳述（OC §2.4.1）：每個候選的 outer-CV 分數估計的是該 procedure 的表現；從多個候選中取最小者，使勝出者的 outer-CV 分數有樂觀偏誤；凍結 predictor 表現的獨立估計是 Test 評估；frozen predictor 是在整個 Fit 上重訓的，不是產生 outer-CV 分數的那些模型。不得把勝出者的 outer-CV 分數寫成不偏估計。 | E4；OC §2.4.1；OC-A4；H-3 |
| R-RPT-3 | G | ENHANCED | Conformal 陳述分三層，措辭不超過 OC §2.4.2：(1) nominal target 1 − α＝95% 是設計參數，不是結果；(2) 理論保證：在 Fit 訓練的 predictor 固定、Calibration 的分數與一筆新的 Test 交易的分數 exchangeable 的**假設**下，P(Y ∈ C(X)) ≥ 95%；保證是 marginal 的，不是對特徵值、價格區間或地區的條件保證；沒有 ties 時上界為 95% + 1/(n_cal+1)；group-aware 分區與整棟房屋的隨機分派都**不能單獨證明** exchangeability（同一房屋的 177 筆重複交易彼此相依、各房屋交易筆數不同、系統性差異可能破壞假設）；保證只適用於本資料集 2014-05～2015-05 中被保留的交易；(3) observed coverage 是單次分區的實證估計，列出 n_test、平均寬度與抽樣誤差幅度，本身不證明也不否定保證。另說明 `exp` 單調，coverage 在 log 與 USD 尺度相等。Observed coverage 超出抽樣誤差幅度時，MUST 說明可能原因，包括 exchangeability 假設可能不成立。 | E6；OC §2.4.2、§3.4；OC-A5；H-3 |
| R-RPT-4 | D | MVM | 產生方式：報告原稿為 `report/report.md`（zh-TW Markdown 範本）；所有計算出的數值與圖都以範本欄位從結果 artifact 與 `results/` 取得。`tools/build_report.py` 把範本轉成 HTML，再以 headless Chromium 系瀏覽器（Edge 或 Chrome）列印為 PDF，最後把 ChatGPT 對話 PDF 的頁面原樣附在報告最後作為附錄。輸出在 `dist/`。有兩種模式：draft（acceptor 證據的位置可以是標示清楚的待填文字）與 final（任一範本欄位未解析、任一 acceptor 材料缺少、或仍有待填文字時，MUST 失敗）。PDF 中的 zh-TW 文字 MUST 正確顯示（字型嵌入、無缺字）。指令寫在 README。 | M4、M9；OC §5（報告 PDF 的產生方式）；H-2 |
| R-RPT-5 | P | MVM | Scope class 標示：報告 MUST 有一節或一張表，區分老師的要求（MVM）與專案延伸（ENHANCED E1–E9，標示「專案延伸（非老師要求）」）；正文提到 ENHANCED 的做法時，不得寫成老師要求。參考實作（week05）的行為不得寫成老師要求。 | OC §2.2、§2.5、§3.4；Bindings §2.4；H-4 |
| R-RPT-6 | G | ENHANCED | 報告與 README 中，任何由執行結果得出的數值 MUST 來自結果 artifact，不得手寫。呈現精度：USD 金額（RMSE、MAE、寬度）取整數；MSE 以科學記號 4 位有效數字；R² 取 4 位小數；coverage 以百分比取 2 位小數；q̂ 取 4 位小數。 | OC-A6；H-3 |

### 1.11 AI 協助與研究證據

| ID | 類型 | Class | 需求 | 對應 |
| --- | --- | --- | --- | --- |
| R-AI-1 | T／G | MVM | 「GPT 輔助內容」節：標題含字串「GPT 輔助內容」；以一張表如實揭露 AI 工具的使用：ChatGPT 的用途（只依 acceptor 的 ChatGPT PDF 忠實描述），以及 Claude Code 的用途（程式、測試、報告草稿等實際範圍）。不得把 Claude 的產出寫成 ChatGPT 的產出；揭露說明不替代 ChatGPT PDF。指向附錄與 ZIP 中 ChatGPT PDF 的檔名。 | M7；OC §2.5.1；OC-A7；H-2、H-4 |
| R-AI-2 | T／G | MVM | 「NotebookLM 摘要」節：標題含字串「NotebookLM 摘要」；正文（不含標題與註記）的**漢字數 ≥ 100**；內容只來自 acceptor 提供的 NotebookLM 原始材料，允許忠實編輯（排版、修正錯字、摘錄、翻譯、縮寫），經整理處註明「依 NotebookLM 研究整理」；列出材料中的來源連結。每一句摘要都 MUST 能以對照表（`acceptor_materials/notebooklm/traceability.md`）對回材料中的位置。材料未提供前，只能放標示清楚的待填文字，不得放範例內容。 | M6；OC §2.5.1；OC-A7；H-2、H-4 |
| R-AI-3 | T／G | MVM | 主流或更優解法比較節：比較本資料集或同類房價問題的主流或更優做法（例如樹模型、梯度提升、空間特徵等），每一項都有可查證的公開來源連結；引用的效能數字只照來源原文，並標示為來源的數字，說明與本作業的評估協定是否可比；說明與本作業做法的差異與取捨。若引用 NotebookLM 材料，依 R-AI-2 的規則。不得有無來源的主張。 | M8；OC §2.5.1；OC-A7；H-4 |
| R-AI-4 | T／G | MVM | ChatGPT 對話 PDF：由 acceptor 提供；Executor 收到時在 worklog 記錄日期、原檔名、sha256 與 acceptor 的提供訊息引用；原檔不修改。報告附錄是它的頁面原樣附加；ZIP 內另有一份位元相同的副本（R-PKG-1）。遮蔽個資只由 acceptor 進行；有遮蔽時在報告中註明。Agent 不得產生、改寫或補造對話，不得以 Claude 或無關對話替代。 | M5；G6；OC §2.5.1；OC-A7；H-1、H-4 |
| R-AI-5 | D | MVM | acceptor 原始材料的存放位置：`home_work_02/acceptor_materials/chatgpt/`（ChatGPT PDF）與 `home_work_02/acceptor_materials/notebooklm/`（NotebookLM 輸出、來源清單、R-AI-2 的對照表）。此目錄被單元 `.gitignore` 忽略（R-REPO-2）；acceptor 決定公開前，不得 commit 或 push（R-REPO-3）。 | OC §2.5.1；OC §5（存放位置）；H-1 |

### 1.12 Packaging — 繳交套件

| ID | 類型 | Class | 需求 | 對應 |
| --- | --- | --- | --- | --- |
| R-PKG-1 | T | MVM | `tools/package_submission.py` 以學號為參數產生 `dist/<學號>_hw2.zip`。ZIP 根目錄 MUST 含：`<學號>_hw2.ipynb`（已驗證的 `hw2.ipynb` 位元副本）、`<學號>_hw2_report.pdf`（final 模式的報告）、`<學號>_hw2_chatgpt.pdf`（acceptor 原檔的位元副本）、`mlr/`、`data/kc_house_data.csv`、`requirements.txt`、`README.md`。MAY 含：`tests/`、`results/`、`tools/`、`report/`。MUST NOT 含：`acceptor_materials/` 的其他內容、`dist/`、`doc/`、`.git`、快取目錄、虛擬環境、`.env`。 | M5、M9；OC-A8；H-2 |
| R-PKG-2 | T | MVM | 學號只由 acceptor 提供。打包腳本 MUST 拒絕空值、含老師範例的佔位 `XXX`（不分大小寫）、含 `<`、`>` 或「學號」字樣、或含檔名不允許字元的值。ZIP 內任何檔名都不得含佔位。 | M9；OC-A8；OC §3.4；H-2 |
| R-PKG-3 | D | MVM | ZIP 留在 `dist/`（不追蹤）。ZIP 的 sha256、檔案清單與每個檔案的 sha256 記入 worklog；S4 時用來核對所繳交的檔案。 | OC-A8；OC §3.2；H-1 |
| R-PKG-4 | D | MVM | 解壓驗證：把 ZIP 解壓到新的空目錄，以其中的 `requirements.txt` 建立新的 Python 3.11 虛擬環境，非互動執行 `<學號>_hw2.ipynb`，MUST 成功，且數值與報告一致（R-RPT-6 的精度）。 | M9；老師評分「模型正確可執行」；OC-A8 |

### 1.13 Repository — 檔案配置與追蹤

| ID | 類型 | Class | 需求 | 對應 |
| --- | --- | --- | --- | --- |
| R-REPO-1 | D | ENHANCED | 單元根目錄配置：`hw2.ipynb`、`mlr/`（`data.py`、`selection.py`、`modeling.py`、`evaluation.py`、`conformal.py`）、`tests/`、`data/`、`results/`、`report/`、`tools/`、`requirements.txt`、`README.md`、`.gitignore`；不追蹤的 `acceptor_materials/`、`dist/`。追蹤的 notebook 名稱不含學號（學號在實作開始時尚未提供）。 | E7；G5、G7；CLAUDE.md 單元結構 |
| R-REPO-2 | D | MVM | 單元 `.gitignore`（`home_work_02/.gitignore`）MUST 忽略 `acceptor_materials/`、`dist/`、虛擬環境目錄、`.ipynb_checkpoints/`。 | OC §2.5.1；H-1 |
| R-REPO-3 | P | MVM | Git 追蹤的檔案、push 的 branch 與 PR MUST NOT 含 acceptor 原始材料、PDF 或 ZIP，除非 acceptor 明確決定公開某一項；該決定的原文記入 worklog，A-4 檢查依該決定調整。這不是 S2 的條件，沒有決定時就維持不追蹤。 | OC §2.5.1；H-1 |
| R-REPO-4 | T／G | MVM | `home_work_02/README.md` MUST 有：目的；scope class 摘要；資料來源、授權與 sha256；流程（CRISP-DM 摘要）；成果（選出的 procedure、Test 指標、coverage、平均寬度，數值依 R-RPT-6）；重跑步驟（Python 3.11、建立虛擬環境、安裝、執行 notebook、執行測試、建置報告、打包；報告建置需要 Edge 或 Chrome）；GitHub 連結 `https://github.com/yotsubamomo/aiot-classwork/tree/main/home_work_02`；檔案配置。 | M10；OC-A6、OC-A8；H-2 |
| R-REPO-5 | D | MVM | `home_work_02/doc/acceptance/ACCEPTANCE.md`：AC-01～AC-31 逐條的驗證方式、證據位置與狀態。 | CLAUDE.md 單元結構；治理 §4.7（AC coverage） |

### 1.14 Reproducibility — 可重現

| ID | 類型 | Class | 需求 | 對應 |
| --- | --- | --- | --- | --- |
| R-REPRO-1 | G／D | ENHANCED | Python 3.11；`requirements.txt` 以 `==` 固定所有直接相依（分析、notebook 執行、測試、報告建置所需的套件）。 | E8、E9；OC-A6 |
| R-REPRO-2 | G | ENHANCED | 決定性：同一環境連續執行兩次 notebook，結果 artifact 的數值在 R-RPT-6 的精度下相同。 | OC-A6；H-3 |
| R-REPRO-3 | P | ENHANCED | Notebook 與測試執行時不使用網路，不讀取任何憑證。 | OC §2.5；H-1 |

### 1.15 Tests — 自動化測試

| ID | 類型 | Class | 需求 | 對應 |
| --- | --- | --- | --- | --- |
| R-TEST-1 | G | ENHANCED | pytest，位於 `tests/`，從單元根目錄執行，離線。 | E8；G8 |
| R-TEST-2 | G | ENHANCED | 資料測試：checksum 不符時報錯（以竄改的副本測試）；schema 與列數驗證；`sqft` 恆等式；R-PREP-1 的轉換（`sale_days` 的起始日、`is_renovated`／`effective_year` 的兩種情況）；R-PREP-2 的 full column rank。 | OC-A1；G8 |
| R-TEST-3 | G | ENHANCED | Leakage 測試：AC-06～AC-09。 | OC-A3；G8；H-3 |
| R-TEST-4 | G | ENHANCED | Conformal 測試：(a) 已知答案的合成資料（含 k 的邊界與 k > n_cal 的情況）；(b) 以**不 import `mlr.conformal`** 的獨立程式碼，從保存的 Calibration 分數與 Test 預測重算 q̂、coverage、平均寬度，與結果 artifact 比對；(c) 區間下界 > 0。 | OC-A5；G8；H-3 |
| R-TEST-5 | D | MVM | 追蹤檔案檢查（高風險裁決 A-4）：在 git work tree 中時，`git ls-files` 的單元檔案不含 `acceptor_materials/`、`dist/`、`.pdf`、`.zip`、`kaggle.json`，且不含 Kaggle token 格式；不在 git work tree 中（例如 ZIP 解壓後）時 skip。 | OC §2.5.1；H-1 |
| R-TEST-6 | D | ENHANCED | 選模測試：候選恰為五個；R-CAND-6、R-SEL-2 的 tie-break；同一 outer fold 內各候選的 inner folds 相同；forward 與 backward 的路徑長度與 group 單位。 | OC-A4；H-3 |
| R-TEST-7 | D | MVM | 打包與報告建置測試：R-PKG-2 的拒絕條件；ZIP 必要內容；final 模式在缺材料或有未解析欄位時失敗；R-AI-2 的漢字計數函式。 | OC-A7、OC-A8 |

## 2. Acceptance Criteria（AC）

每條給出可觀察的 PASS 條件、FAIL 例、證據與方法。「兩處」指 notebook 與報告。

| ID | Class | 對應 | PASS 條件 | FAIL 例 | 證據／方法 |
| --- | --- | --- | --- | --- | --- |
| AC-01 | MVM | OC-A1；R-DATA-4 | 兩處都載明資料集名稱、Kaggle 連結、擁有者、授權 CC0-1.0、檔名、列數與欄數。 | 缺連結或授權；只在 notebook 有。 | notebook 輸出；報告資料說明節。 |
| AC-02 | ENHANCED | OC-A1；R-DATA-1、R-DATA-3 | Notebook 輸出實際計算的 CSV sha256，等於固定值；竄改副本使載入報錯並指明兩個值；schema、列數、唯一 `id` 數、`sqft` 恆等式驗證通過。 | 只印出常數而不是計算值；不符時仍繼續；改用其他檔案而無 re-pin 紀錄。 | notebook 輸出；pytest（R-TEST-2）。 |
| AC-03 | MVM | OC-A1；R-DATA-4、R-PREP-2 | 兩處都依 OC §2.4.1 規則陳述 source feature：列出 19 個、說明 encode 後的欄位不計、列出建模使用的 18 個與 `sqft_basement` 不使用的理由；數量都在 10–20。 | 以 encode 後的欄位數計數；只寫數字不寫規則。 | notebook 輸出的欄位清單；報告資料說明節。 |
| AC-04 | MVM | OC-A2；R-NB-1、R-NB-5 | Notebook 有六個依序的頂層章節，標題含階段名稱；每章節包含第 4.4 節清單的全部項目，且有對應的程式輸出或說明。 | 缺一個階段；只有標題；階段順序錯。 | 章節清單比對（可自動擷取標題）；Reviewer 逐項核對第 4.4 節。 |
| AC-05 | MVM | OC-A2；R-RPT-1 | 報告有六個依序章節，規則同 AC-04。 | 同 AC-04。 | 報告 PDF 的目錄與章節；Reviewer 逐項核對。 |
| AC-06 | ENHANCED | OC-A3；R-PART-1、R-PART-2 | 自動化測試證明：三個分區沒有共同的 `id`；聯集恰為全部 21,613 列；House 數為 12,862／4,287／4,287；以同一 SEED 重跑得到相同分區。 | 有 `id` 跨分區；列數不合；未設 seed。 | pytest 輸出。 |
| AC-07 | ENHANCED | OC-A3、OC-A4；R-PART-3、R-PART-4 | 自動化測試證明：每個 outer fold 與每個 inner fold 的訓練列與驗證列沒有共同的 `id`；outer folds 只產生一次，五個候選使用同一組；同一 outer fold 內各候選的 inner folds 相同；outer folds 只含 Fit 的列。 | 以列為單位分 fold；不同候選的 folds 不同。 | pytest 輸出；結果 artifact 的 fold 編號。 |
| AC-08 | ENHANCED | OC-A3；R-PART-5、R-PREP-3、R-CAND-\* | 自動化測試證明：(a) 一次 fit 之後，標準化參數與 one-hot 類別等於只由該次訓練列計算的值；(b) 只改動驗證列、Calibration 或 Test 的特徵與目標，不會改變對同一組訓練列執行 procedure 的結果（選中的 groups、`alpha`、係數）；(c) 選模函式的輸入只含 Fit 的 `id`。 | 前處理在切 fold 前以全部資料 fit；選擇看到驗證列。 | pytest 輸出。 |
| AC-09 | ENHANCED | OC-A3；R-SEL-3、R-SEL-4、R-EVAL-1 | Run manifest 的事件依序為 partitioned → outer_cv_done → selected → frozen（含 sha256）→ calibrated → test_evaluated；測試證明 Test 評估函式在缺少 frozen 或 calibrated、sha256 不符、或已評估過時都會報錯。 | Test 評估早於 frozen；沒有 hash 紀錄；可以重複評估。 | 結果 artifact 中的 manifest；pytest 輸出。 |
| AC-10 | MVM＋ENHANCED | OC-A4；R-CAND-1～R-CAND-5、R-SEL-1、R-SEL-2 | 比較表列出 C1～C5，五者都有 5 個 outer folds 的 USD RMSE、R²、MAE、MSE，以及平均與標準差；五者使用的 outer fold 編號相同；兩處都有此表。 | 缺任一候選；某候選用了不同 folds；只有平均沒有逐 fold 紀錄。 | 結果 artifact；notebook 表格；報告表格。 |
| AC-11 | MVM＋ENHANCED | OC-A4；R-CAND-2～R-CAND-8 | 結果 artifact 與 notebook 記錄每個 outer fold 中 C2、C3 選中的 k 與 groups 及 inner-CV 路徑、C4、C5 選中的 `alpha`（含網格邊界標示）、C5 的非零係數數；選擇只依 inner-CV USD RMSE；程式中沒有 p-value 或顯著性檢定用於選擇。 | 以 p-value 選特徵；`alpha` 固定而未調；k 以 Test 決定。 | 結果 artifact；notebook 輸出；Reviewer 檢查 `mlr/selection.py`、`mlr/modeling.py`。 |
| AC-12 | ENHANCED | OC-A4；R-SEL-2、R-SEL-3、R-PREP-2 | 選擇規則與 tie-break 寫在 notebook 與報告；結果 artifact 記錄選出的候選與比較依據；frozen predictor 是選出的 procedure 在整個 Fit 上重跑的結果，記錄選中的 groups 或 `alpha`；Fit 的 design matrix full rank 檢查通過並輸出。 | 選擇與排序不符；frozen predictor 以 outer fold 的模型代替；rank 不足。 | 結果 artifact；notebook 輸出；pytest（R-TEST-2、R-TEST-6）。 |
| AC-13 | ENHANCED | OC-A4；R-RPT-2、R-PREP-6 | 報告含 R-RPT-2 的四項陳述，以及 R-PREP-6 的「ŷ 是條件中位數的估計、未作偏誤修正」說明。 | 寫「勝出者的 CV 分數是其真實表現的估計」而未說明偏誤；未說明重訓。 | 報告的 Modeling／Evaluation 節。 |
| AC-14 | MVM | OC-A4；R-EVAL-1 | 兩處都有 frozen predictor 在 Test 上的 R²、MAE、MSE、RMSE（USD），來自 manifest 中唯一的 `test_evaluated` 事件。 | 指標用 log 尺度；有兩次 Test 評估；Test 指標出現在選模前。 | 結果 artifact；notebook；報告。 |
| AC-15 | MVM＋ENHANCED | OC-A5；R-EVAL-2 | 預測圖符合 R-EVAL-2 的全部項目，兩處都顯示；zh-TW 無缺字。 | 沒有區間；軸不是 USD；畫的是 Calibration 或 Fit；缺字方塊。 | 圖檔；notebook；報告。 |
| AC-16 | ENHANCED | OC-A5；R-CONF-1～R-CONF-5 | 結果 artifact 的 n_cal、k、q̂、coverage、平均寬度、n_test，與 R-TEST-4(b) 的獨立重算一致（q̂ 完全相等；coverage 與寬度在浮點誤差內）；合成資料測試通過；所有區間下界 > 0。 | 分位數以內插計算；以 n_cal 而非 n_cal+1 計算 k；分數用了 Test。 | pytest 輸出；結果 artifact。 |
| AC-17 | ENHANCED | OC-A5；R-RPT-3 | 報告分開陳述三層，逐項含 R-RPT-3 列出的內容；措辭不超過 OC §2.4.2；observed coverage 超出抽樣誤差幅度時附原因說明。 | 漏寫 exchangeability 假設；把 group-aware 分區或隨機分派寫成已證明 exchangeability；把 observed coverage 寫成保證的證明；寫成條件保證。 | 報告的區間說明節；Reviewer 逐句對照 OC §2.4.2。 |
| AC-18 | MVM | OC-A2（Deployment）、OC-A5；R-DEP-1～R-DEP-2 | 預測函式對給定的列回傳點預測與上下界，等於以 frozen predictor 與記錄的 q̂ 直接計算的值；sha256 不符時報錯；notebook 的 Deployment 章節以非 Calibration、非 Test 的輸入示範，並寫明使用限制。 | 示範使用 Test 列；區間與 R-CONF-3 不一致；沒有使用限制。 | pytest；notebook。 |
| AC-19 | ENHANCED | OC-A6；R-PART-1、R-REPRO-1、R-REPO-4 | `SEED = 2026` 定義一次；`requirements.txt` 全部 `==` 固定且含 Python 版本說明；README 有完整的重跑步驟。 | 依賴未固定；README 缺步驟。 | 檔案檢查。 |
| AC-20 | ENHANCED | OC-A6；R-NB-3、R-NB-4、R-REPRO-2、R-REPRO-3、R-RPT-6 | 在新建的 Python 3.11 虛擬環境中，依 README 安裝並非互動執行 notebook，成功；重跑的結果 artifact 與報告、README 中的每一個數值在 R-RPT-6 精度下相同；連續兩次執行的數值相同；執行期間不需網路。 | 重跑失敗；任一數值不同；報告數值手寫。 | worklog 的重跑紀錄（指令、環境、輸出、比對結果）；Reviewer 自行比對（高風險裁決 A-2）。 |
| AC-21 | ENHANCED | OC-A6；R-TEST-1～R-TEST-7 | 在 AC-20 的乾淨環境中，全部 pytest 通過，沒有被 skip 的必要測試（R-TEST-5 在 git work tree 外的 skip 除外）。 | 任一測試失敗；以弱化或刪除測試取得通過。 | pytest 輸出。 |
| AC-22 | MVM | OC-A7；R-AI-1 | 報告有「GPT 輔助內容」節，揭露 ChatGPT 與 Claude Code 的實際用途；ChatGPT 的描述可對回 ChatGPT PDF。 | 缺標示；沒有揭露 Claude Code；把 Claude 的產出寫成 ChatGPT 的。 | 報告；ChatGPT PDF 對照。 |
| AC-23 | MVM | OC-A7；R-AI-2 | 報告有「NotebookLM 摘要」節，正文漢字數 ≥ 100（以 R-TEST-7 的計數函式與人工核對）；整理處有「依 NotebookLM 研究整理」；對照表把每一句對回 acceptor 的原始材料；沒有材料以外的論點或來源。 | 少於 100 字；摘要含材料沒有的內容；沒有原始材料卻有摘要。 | 報告；`acceptor_materials/notebooklm/` 的材料與對照表；Reviewer 直接比對（高風險裁決 A-3）。 |
| AC-24 | MVM | OC-A7；R-AI-3 | 報告有主流或更優解法比較節；每一項都有可開啟的來源連結；引用的數字與來源原文一致並標明出處與可比性。 | 無來源的主張；數字與來源不符。 | 報告；Reviewer 抽查來源。 |
| AC-25 | MVM | OC-A7；R-AI-4、R-AI-5 | 報告附錄含 ChatGPT PDF 的全部頁面（原樣）；ZIP 中的 `<學號>_hw2_chatgpt.pdf` 與 worklog 記錄的 acceptor 原檔 sha256 相同；worklog 有收到的紀錄。 | Agent 產生的對話；以 Claude 紀錄替代；頁面被修改；sha256 不符。 | worklog；sha256 比對；報告 PDF 頁數比對。 |
| AC-26 | MVM | OC-A8；R-PKG-1～R-PKG-4 | ZIP 名稱為 `<學號>_hw2.zip`（實際學號）；根目錄含 R-PKG-1 的全部必要項目、沒有排除項目；檔名沒有佔位；ZIP 的 sha256 與檔案清單已記錄；解壓驗證成功。 | 學號為佔位；缺報告或 ChatGPT PDF；含 `acceptor_materials/` 其他內容；解壓後無法執行。 | ZIP 檔案清單與 sha256（worklog）；解壓驗證紀錄；pytest（R-TEST-7）。 |
| AC-27 | MVM | OC-A8；R-REPO-4 | README 有 R-REPO-4 的全部項目；GitHub 連結指向 `yotsubamomo/aiot-classwork` 的 `home_work_02/`。連結在合併前可能無法開啟，「可開啟」屬 S3，不是本 AC。 | 缺流程、成果或連結；成果數字與 artifact 不符。 | README。 |
| AC-28 | MVM | OC-A8；R-REPO-2、R-REPO-3、R-TEST-5 | 在受審 subject 上：`git ls-files` 不含 `.env`、`acceptor_materials/`、`dist/`、PDF、ZIP（acceptor 已記錄的公開決定除外）；追蹤檔案與 diff 不含憑證；R-TEST-5 通過。 | ChatGPT PDF 或 ZIP 被 commit；`kaggle.json` 被 commit。 | `git ls-files` 輸出；R-TEST-5 輸出；Reviewer 檢查 diff。 |
| AC-29 | MVM | OC §2.2、§2.5、§3.4；R-RPT-5 | 報告有 scope class 標示（老師要求 vs. 專案延伸）；正文沒有把任何 ENHANCED 做法或參考實作的行為寫成老師要求。 | 寫「老師要求以 nested CV 比較」；寫「老師要求 conformal」。 | 報告；Reviewer 逐節檢查。 |
| AC-30 | MVM | OC §2.5；R-NB-5、R-RPT-1 | Notebook 的說明與報告的內文為 zh-TW（程式識別字與技術名詞可為英文）。 | 報告主體為英文。 | notebook；報告。 |
| AC-31 | MVM | OC §2.5；R-DATA-2、R-REPRO-3 | Worklog 記錄資料取得的方式（匿名端點或 acceptor 提供）、URL、日期與 sha256；程式與 worklog 中沒有使用憑證的痕跡；notebook 與測試在無網路下執行成功。 | 以 Kaggle CLI 驗證下載；notebook 執行時連網下載。 | worklog；程式檢查；AC-20 的重跑紀錄。 |

## 3. Invariants（跨 Ticket，Spec Integration Audit 必核）

| ID | Invariant | 依據 |
| --- | --- | --- |
| INV-1 | **隔離**：三個分區依 House 互斥且涵蓋全部列；每次 fit 的有參數步驟只看到該次的訓練列；Calibration 只用於 q̂；Test 只用於 R-EVAL-1。 | OC §2.4.1；OC-A3；H-3 |
| INV-2 | **Test 單次使用且不影響決定**：每次執行恰有一次 Test 評估，在 frozen 與 calibrated 之後；Test 的結果不是任何設計或實作決定的輸入。第 4.1 節固定的參數（seed、網格、groups、轉換、準則、tie-break）只能經 DA decision record 改變，理由不得來自 Calibration 或 Test。 | OC §2.4.1、§3.4；H-3 |
| INV-3 | **公平比較**：五個候選共用同一組 outer folds、同一個 outer fold 內共用 inner folds、相同的前處理與 log 目標轉換、相同的點預測定義（無偏誤修正）、相同的指標定義。 | OC §2.4.1；E4、E5；H-3 |
| INV-4 | **數值單一來源**：報告與 README 的每個計算數值，都來自 notebook 最終執行寫出的結果 artifact；追蹤的 notebook、`results/`、報告、ZIP 都對應同一次執行。 | OC-A6；H-3 |
| INV-5 | **Conformal 語義固定**：分數、k、q̂、區間、coverage 的定義依 R-CONF-1～R-CONF-4；報告陳述不超過 OC §2.4.2。 | OC §2.4.2；H-3 |
| INV-6 | **老師指定的名稱不變**：`<學號>_hw2.ipynb`、`<學號>_hw2.zip`、「GPT 輔助內容」、「NotebookLM 摘要」、六個 CRISP-DM 階段名稱與順序、報告為 PDF、預測圖附區間。 | M4–M9；H-2 |
| INV-7 | **證據真實與標示誠實**：沒有任何 Agent 產生或替代的對話或研究內容；摘要可追溯；工具使用如實揭露；ENHANCED 不被寫成老師要求。 | OC §2.5.1、§3.4；H-4 |
| INV-8 | **不使用憑證；acceptor 材料不公開**：沒有憑證被使用或追蹤；acceptor 原始材料、PDF、ZIP 不進入追蹤檔案、push 的 branch 或 PR，除非 acceptor 有記錄的公開決定。 | OC §2.5、§2.5.1；H-1 |
| INV-9 | **可重現**：CSV 以 sha256 固定；`SEED = 2026`；Python 3.11 與固定的相依版本；執行不需網路。 | E8、E9；OC-A6 |

## 4. Implementation Decisions

### 4.1 契約固定（Executor 不得自行改變）

- **檔案配置**：R-REPO-1；資料檔 R-DATA-1；材料目錄 R-AI-5；`dist/` 與 `.gitignore` R-REPO-2；報告原稿 `report/report.md`；腳本 `tools/build_report.py`、`tools/package_submission.py`；acceptance 文件 R-REPO-5。
- **隨機性與分區**：`SEED = 2026`；R-PART-2 的演算法與 House 數；outer folds 共用與保存（R-PART-3）；inner folds 規則（R-PART-4）。
- **特徵**：18 個 groups 與 canonical order（第 1.4 節）；R-PREP-1 的轉換（起始日 2014-05-01、`is_renovated`、`effective_year`）；`sqft_basement` 不使用；`zipcode` one-hot（drop first、未知類別為基準）；非 one-hot 欄標準化；不加其他轉換。
- **目標與點預測**：`ln(price)` 訓練；ŷ＝`exp(f)`；不作偏誤修正。
- **候選**：C1～C5 的定義；Ridge 網格 `logspace(-3, 3, 25)`；Lasso 網格 `logspace(-6, -1, 26)`；inner 準則為 USD RMSE；R-CAND-6 與 R-SEL-2 的 tie-break。
- **凍結與順序**：R-SEL-3、R-SEL-4 的 manifest 事件；R-EVAL-1 的守門條件。
- **Conformal**：R-CONF-1～R-CONF-4 的公式。
- **報告**：Markdown 範本 → HTML → headless Chromium 系瀏覽器 → PDF → 附加 ChatGPT 頁面；draft／final 模式；數值只來自 artifact；R-RPT-6 精度。
- **打包**：R-PKG-1 的檔名與內容；學號檢查；ZIP 不追蹤。
- **環境**：Python 3.11；`==` 固定相依；執行期不連網。

### 4.2 交給實作（HOW）

- `mlr` 各模組內的函式名稱與簽名（R-DEP-1 的語義除外）；fold 產生的具體寫法（例如 `GroupKFold(shuffle=True)` 或以 permutation 分配），只要符合 R-PART-3、R-PART-4 且具決定性。
- scikit-learn 的組裝方式（`Pipeline`、`ColumnTransformer`、`TransformedTargetRegressor`、自訂 selector 等）；Lasso 的 `max_iter` 與 `tol`。
- 結果 artifact 與 manifest 的 JSON 結構與鍵名；frozen predictor 的序列化格式（例如 `joblib`）。
- 圖的樣式、配色、log 刻度與否、matplotlib 的 CJK 字型設定；報告的 CSS 與版面。
- 報告範本欄位的語法與替換方式；使用 Edge 或 Chrome；PDF 合併使用的套件。
- 測試檔案的組織與 fixtures（合成資料、竄改的 CSV 副本）。
- 具體的相依版本（在 Python 3.11 上可安裝並固定即可）。
- Notebook 內的輔助輸出、說明文字的措辭（須符合 AC）。

### 4.3 OC §5 設計事項的裁決與理由

| # | OC §5 事項 | 裁決 | 理由 |
| --- | --- | --- | --- |
| D-1 | 完全共線 | `sqft_basement` 不進入 design matrix；加 full-rank 檢查（R-PREP-2）。 | 每一列都滿足 `sqft_basement = sqft_living − sqft_above`（Brief §10），刪去其中一欄不改變線性模型的欄空間，沒有資訊損失；無懲罰的 OLS 需要 full rank 才能識別係數。刪去哪一欄對預測等價，固定為 `sqft_basement` 只是為了決定性。Dataset 層級的 source feature 數仍為 19，建模使用 18，兩者都在 10–20。 |
| D-2 | `date` 與 `zipcode` | `date` → 以固定起始日 2014-05-01 計算的 `sale_days`；`zipcode` → pipeline 內的 one-hot，在 forward／backward 中作為一個 group（R-PREP-1、R-PREP-3、第 1.4 節）。 | `sale_days` 以常數起始日計算，不從資料 fit，所以沒有洩漏；它捕捉 13 個月內的市場趨勢。13 個月的資料無法把季節性與趨勢分開，所以不加月份。`zipcode` 是名目變數（OC 要求不得當數值大小）；以 group 為選擇單位，使 forward／backward 一次加入或移除整個地區效果，「特徵選擇」的單位與 source feature 計數的單位一致。Drop first 讓 OLS 可識別。 |
| D-3 | 轉回 USD 的偏誤修正 | 不修正；ŷ＝`exp(f)`，報告說明它是條件中位數的估計（R-PREP-6）。 | (a) OC §2.4.2 的 conformal 公式以 `ln ŷ` 為中心的對稱分數定義；加上偏誤修正因子會使區間中心偏離 log 誤差的中位數，對稱分數因而變大，區間變寬。(b) 對所有候選相同，比較仍然公平（INV-3）。(c) 修正的大小約為 `exp(σ²/2)`（σ 為 log 殘差的標準差），影響小，而且不改變任何 OC 驗收條件。報告須如實說明 USD 指標是對中位數預測計算的。 |
| D-4 | 選模的 tie-break | Outer：平均 RMSE 差 < 0.5 USD 視為平手，偏好 C1 > C2 > C3 > C4 > C5。Inner：k 取最小、`alpha` 取最大、同分的 group 取 canonical order 較前者（R-CAND-6、R-SEL-2）。 | 偏好較簡單、調參步驟較少的 procedure；0.5 USD 對應報告的整數精度。Inner 的規則偏好較簡單或正則化較強的模型，並使結果具決定性。 |
| D-5 | 離群值 | 任何分區都不刪列、不 clip；在 Data Understanding 以 Fit 的資料列出異常，在 Data Preparation 說明理由（R-PREP-4）。 | (a) OC-A3 要求三個分區合起來涵蓋全部列；(b) 從 Calibration 或 Test 刪列會改變 coverage 與 Test 指標所指的母體；(c) log 目標降低極端價格的影響，Ridge 與 Lasso 候選提供收縮；(d) 固定規則不需要以資料決定，因此也沒有洩漏的可能。`yr_renovated = 0` 的意義以 R-PREP-1(b) 重新編碼處理。 |
| D-6 | 報告 PDF 的產生方式 | Markdown 範本 → HTML → headless Edge／Chrome → PDF，附加 ChatGPT 頁面；draft／final 模式（R-RPT-4）。 | acceptor 的機器上沒有 pandoc 與 LaTeX，但有 Edge 與 Chrome（2026-10-14 DA 核對），瀏覽器能正確排版並嵌入 zh-TW 字型；範本使數值只有一個來源（INV-4）；附加 ChatGPT 頁面滿足老師「報告需包含 GPT 對話過程」，ZIP 中另有獨立的 PDF 滿足 G6；final 模式防止待填文字進入繳交套件。 |
| D-7 | 資料取得方式 | CSV 隨 repo 與 ZIP 附上，載入時核對 sha256；只由 Executor 匿名取得一次（R-DATA-1～R-DATA-3）。 | CC0-1.0 允許散布（E9）；2.5 MB 適合 git；執行期不連網、不需憑證（OC §2.5），重跑與 ZIP 解壓驗證都可離線完成。 |
| D-8 | acceptor 原始材料的存放位置 | `acceptor_materials/chatgpt/` 與 `acceptor_materials/notebooklm/`，由單元 `.gitignore` 忽略；ZIP 只含 ChatGPT PDF 的副本（R-AI-5、R-REPO-3、R-PKG-1）。 | OC §2.5.1 規定是否放進公開 repository 由 acceptor 決定，所以在決定之前維持不追蹤；ZIP 依 M5、M9 必須含 ChatGPT PDF。放在單元目錄內，Reviewer 可以直接讀取原始材料（高風險裁決 A-3）。 |

**沒有留給 Tickets 的設計事項。** 第 4.2 節的項目是單一 Ticket 內的 HOW，不被其他 Ticket 依賴，也不改變任何 AC。

### 4.4 CRISP-DM 各階段的內容清單（AC-04、AC-05）

| 階段 | 至少包含 |
| --- | --- |
| Business Understanding | 目標（預測 King County 房屋成交價）；使用情境；成功的衡量方式（USD 指標、區間 coverage；本作業沒有效能門檻）；老師要求與專案延伸的區分。 |
| Data Understanding | AC-01～AC-03 的資料說明；結構事實（R-PART-5 允許的全資料事實）；只用 Fit 的分布探索（價格分布、主要特徵與價格的關係）；異常值清單；`sqft` 恆等式；重複交易。 |
| Data Preparation | 分區（group-aware、60／20／20、seed、各分區的 House 數與列數）；R-PREP-1 的轉換；共線處理；encoding 與標準化；不刪列的理由；log 目標與點預測的定義。 |
| Modeling | 五個 candidate procedures；nested CV 的設計（outer 與 inner、group-aware、共用 folds）；每個 fold 的選擇結果；比較表；選擇規則與結果；在 Fit 上重跑與凍結（含 sha256）。 |
| Evaluation | Test 指標；conformal 校準（n_cal、k、q̂）；coverage、平均寬度、n_test；預測圖；偏誤陳述（R-RPT-2）；三層 conformal 陳述（R-RPT-3，報告中完整，notebook 中至少摘要並指向報告）。 |
| Deployment | Frozen predictor 檔案與預測函式；示範（R-DEP-2）；使用限制；如何重跑。 |

## 5. Testing Decisions

### 5.1 什麼是好的測試

- 測外部行為：給定分區，斷言 `id` 互斥；給定訓練列，斷言前處理參數；給定分數，斷言 q̂。不測函式內部如何分組。
- 全部離線，不讀憑證。
- Leakage 測試以「改動不該被看到的列，結果不變」的方式證明，不只檢查呼叫參數。
- Conformal 的獨立重算不得 import 被測模組的計算函式；期望值寫在測試內並註明來源。
- 不得為了通過而弱化或刪除測試；期望值的改變屬 H-3，須在 worklog 寫明理由。

### 5.2 範圍與方法

| 範圍 | 方法 | 對應 |
| --- | --- | --- |
| 資料 | pytest：checksum、schema、恆等式、轉換、rank | R-TEST-2；AC-02、AC-03、AC-12 |
| 隔離 | pytest：分區、folds、fit 範圍、manifest 守門 | R-TEST-3；AC-06～AC-09 |
| 選模 | pytest：候選數、tie-break、folds 共用 | R-TEST-6；AC-07、AC-11、AC-12 |
| Conformal | pytest：合成資料、獨立重算、下界 > 0 | R-TEST-4；AC-16 |
| Deployment | pytest：預測函式與直接計算一致、sha256 守門 | AC-18 |
| 追蹤檔案 | pytest：`git ls-files` 檢查 | R-TEST-5；AC-28 |
| 打包與報告建置 | pytest：學號檢查、ZIP 內容、final 模式、漢字計數 | R-TEST-7；AC-23、AC-26 |
| 整體 | 乾淨環境重跑 notebook；數值比對；ZIP 解壓驗證 | AC-20、AC-26 |
| 文件 | Reviewer 逐項核對章節、陳述、標示、來源 | AC-04、AC-05、AC-13、AC-17、AC-22～AC-24、AC-29、AC-30 |

### 5.3 開發順序的建議（SHOULD）

在 notebook 第一次完整執行之前，Executor SHOULD 以 Fit 的資料完成並測試資料、選模、建模模組；因為第 4.1 節已固定全部的選擇參數，第一次接觸 Test 的結果時，就不再有可以依 Test 調整的參數（INV-2）。

## 6. Verification Strategy（誰在什麼時候看什麼）

| 階段 | 動作 | 依據 |
| --- | --- | --- |
| Executor self-verification（每個 Ticket） | 執行 Ticket 引用的 AC 對應的測試與檢查；worklog 引用結果；不得以弱化測試取得通過。 | 治理 §3.5；impl-default §5 |
| Ticket independent audit（R1／R2） | Reviewer 依 Ticket 引用的 AC 逐條判定 PASS／FAIL；觸及 H-1～H-4 時，依高風險裁決 A-1～A-4 記錄與核對。 | 治理 §4；Bindings §5 |
| Spec Integration Audit（全部 Ticket 結案後） | 對整合 subject 核對 INV-1～INV-9、AC-01～AC-31、OC-A1～OC-A8 的涵蓋（本 Spec 是唯一的 Spec，同時核對全部 derived Specs 的分配合起來涵蓋整個 acceptance boundary）、traceability，以及高風險裁決 A-5。 | 治理 §4.7；derivation record 第 4 節 |
| DA phase acceptance | 引用已 closure 的 Spec Integration Audit record。 | 治理 §3.8 |
| Release（合併進 `main`） | Bindings §5 的 gates；HW2 的第一個 PR 依 OC §9 的一次性 RB-1 授權，其後依 OC §4.2 的 SA-3；另附高風險裁決 A-8 的證據。合併（S3）與 iLearning 繳交（S4）都不是 S2 的條件。 | Bindings §2.5、§5；OC §3.2、§4.2、§9 |

## 7. 對應矩陣（OC-A → AC → R）

| OC-A | AC | 主要 R |
| --- | --- | --- |
| OC-A1 資料集 | AC-01、AC-02、AC-03 | R-DATA-1～R-DATA-4、R-PREP-2 |
| OC-A2 CRISP-DM | AC-04、AC-05、AC-18（Deployment 內容） | R-NB-1、R-RPT-1、R-DEP-1、R-DEP-2；第 4.4 節 |
| OC-A3 隔離 | AC-06、AC-07、AC-08、AC-09 | R-PART-\*、R-PREP-3、R-SEL-3、R-SEL-4、R-EVAL-1 |
| OC-A4 比較與選模 | AC-07、AC-10、AC-11、AC-12、AC-13、AC-14 | R-CAND-\*、R-SEL-\*、R-PREP-6、R-RPT-2、R-EVAL-1 |
| OC-A5 預測區間 | AC-15、AC-16、AC-17、AC-18 | R-CONF-\*、R-EVAL-2、R-RPT-3、R-DEP-1 |
| OC-A6 可重現 | AC-19、AC-20、AC-21 | R-REPRO-\*、R-NB-3、R-NB-4、R-RPT-6、R-TEST-\* |
| OC-A7 AI 協助與研究 | AC-22、AC-23、AC-24、AC-25 | R-AI-\* |
| OC-A8 繳交套件 | AC-26、AC-27、AC-28 | R-PKG-\*、R-REPO-\*、R-TEST-5 |
| OC 的 constraints（不擴張 boundary，只讓它們可驗收） | AC-29（§2.2、§2.5、§3.4 scope class 標示）、AC-30（§2.5 語言）、AC-31（§2.5 不使用憑證） | R-RPT-5、R-NB-5、R-DATA-2、R-REPRO-3 |

## 8. Out of Scope

- **Non-scope（OC §2.3）**：Web App、FastAPI、資料庫、完整 MLOps、強制比較非線性或深度學習模型（M8 的比較只是文獻說明，不實作）；Kaggle 名次；Auto Regression；任何捏造的研究或對話；以 Claude 或無關對話替代 ChatGPT PDF；OC §2.4.2 以外的 conformal 方法；修改 `week05/`、其他單元或 root 檔案（含 root `CONTEXT-MAP.md`）；把參考實作的行為當成老師要求。
- **OPTIONAL（OC §2.2）**：其他候選的區間、額外的診斷圖。本 Spec 不 derive 為 requirement；只允許 R-EVAL-4 的 Fit 診斷圖。其他候選的 Test 區間會增加 Test 的使用，不做。
- **REFERENCE**：`week05/multiple_linear_regression_crisp_dm.ipynb` 與 `week05/docs/`；NotebookLM 或網路研究找到的他人解法。可讀，不是要求。
- **不由 Agent 執行**：iLearning 繳交（RB-2）；acceptor 材料的產生（ChatGPT 對話、NotebookLM 研究）；任何第三方帳號操作（RB-3）；在 acceptor 決定前公開 acceptor 材料（R-REPO-3）。

## 9. Further Notes

### 9.1 acceptor 輸入（缺少時只停止受影響的 AC；治理 §1.5 第 4 項）

| # | 輸入 | 影響的 AC | 交付方式 |
| --- | --- | --- | --- |
| 1 | ChatGPT 對話 PDF | AC-22、AC-25、AC-26 | 放入 `acceptor_materials/chatgpt/`，並在對話中告知；Executor 記錄 sha256。 |
| 2 | NotebookLM 原始材料（輸出與來源清單） | AC-23（及 AC-24，若引用） | 放入 `acceptor_materials/notebooklm/`。 |
| 3 | 學號 | AC-26 | 在對話中提供。 |
| 4 | （可選）是否公開 acceptor 材料或 PDF | AC-28 的檢查範圍 | 在對話中明確指示；沒有指示就不公開。不是 S2 的條件。 |
| 5 | （條件性）資料檔 | AC-02、AC-31 | 只有匿名取得失敗時，由 acceptor 下載並放入 `data/`（RB-3）。 |

S1（OC-A1～OC-A6 PASS）不需要以上任何輸入；報告以 draft 模式建置，acceptor 證據的位置以標示清楚的待填文字保留。

### 9.2 已知風險與處理

| 風險 | 處理 |
| --- | --- |
| 匿名下載端點在實作時失效 | R-DATA-2：改由 acceptor 提供；sha256 必須相同，否則需要 re-pin 的 DA decision record。 |
| Lasso 在小 `alpha` 不收斂 | R-CAND-5：增加 `max_iter`；記錄警告；網格是固定的，不得因此改用 Test 決定網格。 |
| Edge／Chrome 的 headless 參數因版本而異 | R-RPT-4 只固定「Chromium 系瀏覽器列印」；具體指令屬 HOW，寫入 README。 |
| 報告建置需要非 pip 的瀏覽器 | README 寫明需求；notebook 重跑（OC-A6）不依賴瀏覽器。 |
| Observed coverage 明顯偏離 95% | 不是 FAIL（OC §3.4）；依 R-RPT-3 說明原因。 |
| 開發期間多次執行 notebook，使 Executor 多次看到 Test 結果 | 第 4.1 節已固定全部選擇參數；INV-2 禁止 Test 結果影響任何決定；變更須經 DA decision record（第 5.3 節的建議順序降低風險）。 |
| 學號出現在 worklog 的 ZIP 檔案清單 | OC-A8 要求記錄檔案清單；OC 沒有把學號列為機密（高風險裁決 2.1 節「不涵蓋」）。 |

### 9.3 詞彙

本 Spec 使用 `CONTEXT.md` 的詞彙。新增的設計名詞（source-feature group、canonical order、run manifest、結果 artifact）只在本 Spec 內使用；若實作期需要把它們加入 `CONTEXT.md`，由 Executor 依 `docs/agents/domain.md` 提出（`CONTEXT.md` 在單元內，可在 Ticket 中修改）。

## 10. 版本紀錄

| 版本 | 日期 | 依據 | 變更 |
| --- | --- | --- | --- |
| v1.0 | 2026-10-14 | DA 派工（lane、高風險類別、Spec derivation）；Outcome Contract 第 1–8 節 `e2153254`、接受紀錄 `370c0ae` | 初版 derive。 |
