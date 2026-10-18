# HW2：King County 房價多元線性回歸分析報告

> **報告狀態：draft。** 本報告的數字、表格與分析圖都在建置時（`python -m hw2.report`）從主程式 `hw2.ipynb` 匯出的結果（`results/model_data.json`、`results/tables/`、`results/figures/`）注入，沒有手抄數字。「GPT 輔助內容」「NotebookLM 摘要」與附錄的 ChatGPT 對話 PDF 必須由作者本人提供原始材料，目前以【待填】標示，尚未撰寫。

## 標示說明與對照表

本報告的每一章與重要段落都標示它的來源：

- 〔老師要求〕作業頁正文的書面要求。唯一的例外是互動 dashboard：它是老師的**課堂口頭要求**，作業頁與講義文字都沒有要求網站，本報告提到時一律註明「課堂口頭」。
- 〔依老師補充建議〕作業頁「補充」段的建議，本專案選擇採用；它們不是老師的必要要求。
- 〔專案延伸〕本專案自行加入的設計，不是老師的要求。

| 項目 | 標示 | 本報告的位置 |
| --- | --- | --- |
| Kaggle 公開資料集、特徵數條件、標示來源與連結 | 老師要求（特徵數另採補充段條件的交集，見第一章） | 資料來源與研究脈絡 |
| 以線性回歸預測；必做特徵選擇與模型評估 | 老師要求 | Modeling、Evaluation |
| 特徵選擇的方法清單（SFS、RFE、Lasso） | 老師要求的特徵選擇；方法取自補充段建議清單的一部分 | Modeling |
| 預測圖加上預測區間 | 老師要求 | Evaluation、Dashboard 截圖 |
| CRISP-DM 六階段 | 老師要求 | 第二章至第七章 |
| 「GPT 輔助內容」「NotebookLM 摘要」、ChatGPT 對話 PDF | 老師要求 | 對應的兩節與附錄 |
| 網路上主流或更優解法的比較與說明 | 老師要求 | 主流或更優解法比較 |
| README 整理流程與成果（有上傳 GitHub 時） | 老師要求（optional 條款；本專案使用 GitHub，所以適用） | 單元 `README.md` |
| Kaggle 名次（若有） | 老師要求（本資料集不適用，見第一章） | 資料來源與研究脈絡 |
| Adjusted R² | 依老師補充建議 | Evaluation |
| 五大回歸假設診斷 | 依老師補充建議 | Evaluation |
| Deployment 的預測新樣本與模型解釋 | 依老師補充建議 | Deployment |
| Ridge／Lasso 對照 | 依老師補充建議 | Modeling、Evaluation |
| 互動 dashboard | 老師要求（課堂口頭；作業頁正文沒有） | Deployment、Dashboard 連結與截圖 |
| 以房屋 `id` 分組的切分與交叉驗證、fold 內選擇、只評估一次的 Test 協定 | 專案延伸 | Data Preparation、Modeling、Evaluation |
| 以 ln(price) 建模、以 USD 報告 | 專案延伸 | Data Preparation |
| 預測區間的經驗涵蓋率驗證 | 專案延伸（預測區間本身是老師要求） | Evaluation |
| 講義的 p-value backward elimination 對照 | 專案延伸（講義方法，只作對照） | Modeling |
| Permutation importance | 專案延伸（只用於解釋，不用於特徵選擇） | Deployment |
| 各方法計算時間的量測 | 專案延伸 | Modeling |

## 1. 資料來源與研究脈絡 〔老師要求〕

### 1.1 資料集

- 名稱：**{{dataset_name}}**（Kaggle {{dataset_slug}}）
- 連結：<{{dataset_url}}>
- 授權：{{dataset_license}}
- 檔案：{{dataset_file}}，{{n_rows}} 列 × {{n_columns}} 欄；sha256 {{csv_sha256}}（主程式載入時先核對，不符即停止）。
- 內容：King County（美國華盛頓州，含 Seattle）的房屋成交紀錄，training set 的交易日期介於 {{date_min}} 與 {{date_max}}；每一列是一筆交易，共有 {{n_unique_ids}} 棟不同的房屋，所以有 {{n_repeat_full}} 筆是同一棟房屋的重複交易（全資料層級）。

### 1.2 特徵數與老師的兩條條件

作業頁正文寫：

> {{quote:src1:至 Kaggle 選擇一個具有}}

作業頁的「補充」段寫：

> {{quote:src2t:list kaggle multiple linear regression problems|2}}
>
> {{quote:src2t:也就是}}

本專案同時滿足兩條，採用它們的**交集**：特徵數介於 {{feature_rule_low}} 與 {{feature_rule_high}} 之間（含）。計數規則是在編碼之前計算 source features，不含識別欄 `id` 與目標 `price`：

- **Source features**：{{n_source}} 個——{{source_features}}。
- **建模用的 feature groups**：{{n_groups}} 個。{{excluded_features}} 不進模型，因為每一列都滿足 `sqft_living = sqft_above + sqft_basement`，三欄完全共線。
- zipcode 有 {{n_zip_categories}} 個類別，以 one-hot 編碼後是 {{n_zip_onehot}} 欄，但整組仍算一個 feature group；特徵選擇以 feature group 為單位，同一個 source feature 的編碼欄同進同出。

### 1.3 研究脈絡

房價是典型的連續值預測問題，King County 資料集是公開資料中常被用來練習迴歸的資料之一（第八章比較了其中幾個公開解法）。本專案的問題是：在只使用線性回歸的前提下，**哪一組特徵**能在沒見過的交易上給出最好的價格預測，以及模型給出的**預測區間**可信到什麼程度。

### 1.4 Kaggle 名次不適用

評分標準寫：

> {{quote:src1:呈現出Kaggle名次}}

這個資料集是 Kaggle 上的一般資料集（Datasets），不是有排行榜的競賽（Competitions），沒有可以提交或比較的名次，所以「Kaggle 名次」不適用。本報告依同一條標準的後半段，以**預測結果評估**取代：保留 Test 集上的 MAE、MSE、RMSE、R²，每筆 Test 交易的預測區間與經驗涵蓋率，以及預測圖（第六章、第九章）。

## 2. Business Understanding 〔老師要求〕

- **目標**：以房屋的條件（面積、房間數、建築等級、屋齡與整修、位置、交易日期等）預測成交價格，並給出每一筆預測的 {{pi_level_pct}} 預測區間。
- **使用者**：想估計房價合理範圍的買方、賣方或分析者；本作業的評分者。
- **成功的衡量**：以保留 Test 集上的 USD 誤差（MAE、RMSE）與 R² 衡量點預測；以預測區間的經驗涵蓋率衡量區間的可信度。
- **限制**：只用線性回歸（作業要求）；資料只有一年的交易；模型描述的是關聯，不是因果。

## 3. Data Understanding 〔老師要求〕

- 資料沒有缺值；載入時核對 sha256、欄位結構、列數 {{n_rows}}、唯一 `id` 數 {{n_unique_ids}}，以及 `sqft_living = sqft_above + sqft_basement` 對每一列成立（notebook 第 2 章）。
- 價格與各特徵的分布、極端值**只用 training set** 檢視（notebook 2.2、2.3），避免在選模之前看到 Test 集。價格與面積都明顯右偏，所以以 ln(price) 建模（第四章）。
- **異常值不刪除**：極端的房價與面積是真實交易，刪除它們會讓結果看起來比較好、卻不誠實。它們的影響在第六章的殘差診斷中揭露。
- 同一棟房屋的重複交易會讓誤差彼此相關：training set 有 {{train_repeat}} 筆重複交易、涉及 {{train_repeat_houses}} 棟房屋；Test 集有 {{test_n_repeat}} 筆，Test 集共有 {{test_n_houses}} 棟房屋。這是以房屋分組切分（第四章）與誤差獨立診斷（第六章）的原因。

## 4. Data Preparation 〔老師要求〕

### 4.1 固定的逐列轉換

這些轉換不需要從資料學習，對所有模型都一樣：

- `date` → 距基準日 {{base_date}} 的天數 `sale_days`。
- `yr_renovated` → 兩欄：是否整修過 `is_renovated`，以及有效年份 `yr_renovated_effective`（沒整修過時等於建造年 `yr_built`）；兩欄同屬 `yr_renovated` group。
- `zipcode` → 類別（nominal），不是數值。
- 其他欄照原值使用；{{excluded_features}} 不進模型（第一章）。

### 4.2 需要從資料學習的前處理

- `zipcode` 的 one-hot 類別只取自**當次擬合的訓練列**（以排序後的第一類為基準）；預測時遇到訓練列沒有的 zipcode，編為基準類別並提示。正式 Test 集中這樣的筆數是 {{test_n_unseen_zip}}。
- 數值欄的標準化只用於 Ridge／Lasso，而且同樣只用當次的訓練列；OLS 以原始尺度擬合，係數可以直接以原始單位解讀。

### 4.3 目標尺度 〔專案延伸〕

以 {{model_scale}} 建模，所有預測、區間與指標都轉回 {{report_scale}} 報告。點預測 exp(ŷ_log) 沒有做偏誤修正，所以它估計的是**條件中位數**，不是條件平均；在右偏的房價上，條件平均會比條件中位數高。

### 4.4 切分與交叉驗證 〔專案延伸〕

- **以房屋 `id` 分組**的隨機切分：training {{train_pct}}%、Test {{test_pct}}%（seed {{seed}}），training {{n_train}} 筆（{{n_train_houses}} 棟房屋）、Test {{n_test}} 筆。同一棟房屋的所有交易都在同一邊，避免同一棟房屋同時出現在訓練與評估中。
- Training set 內再以 `id` 分組成 {{n_folds}} 個 fold（每折 {{fold_rows}} 筆），所有方法、所有 k、Ridge／Lasso 都用同一組 fold，比較才公平。
- 每一筆交易屬於哪一邊與哪一折，記錄在 `results/split/split_assignment.csv`（只有識別，沒有特徵或價格）。

## 5. Modeling 〔老師要求〕

### 5.1 特徵選擇：四種方法 × k = {{k_range}} 〔老師要求〕

作業要求必做特徵選擇。老師的補充段建議比較下列方法：

> {{quote:src2t:For Feature Selection, compare SelectKBest}}

本專案比較其中四種**能對每個 k 給出一組特徵**的方法（以 feature group 為單位）：Forward SFS、Backward SFS、RFE、Lasso 路徑排序（依 group 進入 Lasso 路徑的先後取前 k 個）；另以單一的 **All-in baseline**（全部 {{n_groups}} 個 group 的 OLS，等於路徑在 k = {{k_max}} 的端點）作為基準。SelectKBest（單變量篩選）與 permutation importance 不作為特徵選擇方法：前者不考慮特徵之間的關係，後者在本專案只用於模型解釋（第七章）。

**選擇與評估的邊界** 〔專案延伸〕：每個方法在每個 fold 的**訓練列上重新**計算 k = {{k_range}} 的子集，再以該子集在同一折的訓練列擬合 OLS、在驗證列算 USD 指標；驗證列不參與任何選擇。CV 指標因此估計的是「這個方法在 k 下的整個程序」。另在整個 training set 上以同一方法計算一次 **canonical subset**，它是 dashboard 顯示、即時預測與 Test 評估所用的模型。

每個方法每個 k 的訓練 CV RMSE（USD，{{n_folds}} 折平均；★ 為該方法的 CV winner）：

{{table:kpath}}

- 各方法的 CV winner：{{winner_forward_sfs}}（{{winner_forward_sfs_cv_rmse}} USD）、{{winner_backward_sfs}}（{{winner_backward_sfs_cv_rmse}}）、{{winner_rfe}}（{{winner_rfe_cv_rmse}}）、{{winner_lasso_path}}（{{winner_lasso_path_cv_rmse}}）；All-in 是 {{allin_cv_rmse}}。
- **整體 CV winner** 是 CV RMSE 最小者：**{{overall_label}}**（{{overall_cv_rmse}} USD）。它的 canonical subset 只少了 {{overall_groups_dropped}}，與 {{shared_with_overall}} 是同一個擬合模型（同一組 groups 在整個 training set 上的 OLS）。這幾個 CV winner 的 CV RMSE 可能不同，因為 CV 評估的是各方法在 fold 內的選擇程序，不是同一個模型有兩個分數。
- 所有候選都是有效的（設計矩陣沒有秩不足）。

### 5.2 對照模型：Ridge 與 Lasso 〔依老師補充建議〕

> {{quote:src2t:4. Modeling: Train LinearRegression}}

Ridge 與 Lasso 使用全部 {{n_groups}} 個 group、標準化後擬合，alpha 只以同一組 fold 的訓練 CV（USD RMSE）選擇。它們是 **metric-only 對照**：不參與 CV winner 競爭，不提供預測區間或即時預測，係數也不匯出。

{{table:alpha}}

兩者都選到 alpha 網格的**下緣**：CV RMSE 隨懲罰減弱而單調下降，最佳值趨近沒有懲罰的 All-in OLS（Ridge {{ridge_cv_rmse}}、Lasso {{lasso_cv_rmse}}、All-in {{allin_cv_rmse}} USD）。也就是說，**正則化在這份資料上沒有改善 CV**：training 的列數（{{n_train}}）遠多於欄數，OLS 的估計變異本來就不大。把網格再往下延伸只會更接近 OLS，所以不再擴大。

### 5.3 講義方法對照：p-value backward elimination 〔專案延伸〕

課堂講義的做法是從全部特徵開始，逐步移除 p-value 最大且大於門檻的特徵。本專案在 group 層級以 partial F 檢定執行（門檻 {{pvalue_threshold}}），與正式方法一樣在每個 fold 的訓練列上做、在驗證列上評估，另在整個 training set 上做一次得到單一子集。它沒有 k 路徑，**只列為對照**，不參與 CV winner，也不在 Test 上評估。

{{table:pvalue}}

結果保留 {{pvalue_k}} 個 group（移除 {{pvalue_removed}}），訓練 CV RMSE 是 {{pvalue_cv_rmse}} USD，比 CV 選出的整體 winner（{{overall_cv_rmse}}）大；{{n_folds}} 個 fold 中有 {{pvalue_folds_agree}} 個得到與整個 training set 相同的子集。p-value 衡量的是「係數是否顯著不為零」，不是「拿掉它預測會不會變差」，這是兩者結果不同的原因。

### 5.4 計算時間 〔專案延伸〕

每個路徑方法要做 {{n_folds}} 個 fold 加上整個 training set 的選擇，以及每個 k 的 CV 與擬合；各方法的時間（秒）每次執行都會量測並匯出：

{{table:timing}}

## 6. Evaluation 〔老師要求〕

> {{quote:src2t:5. Evaluation: Compare MAE}}

### 6.1 評估協定 〔專案延伸〕

- 所有選擇（各方法的 k、整體 CV winner、Ridge／Lasso 的 alpha）只用 training set 的交叉驗證決定；選擇固定之後，保留的 Test 集**只評估一次**，Test 結果不回饋任何選擇。Test 排名與 CV 排名不同時也不換模型。
- 被授權在 Test 上評估的是各方法的 CV winner、All-in 與整體 CV winner；canonical subset 相同的 winner 是同一個模型，只評估一次。另依作者核准的對照，Ridge 與 Lasso 各評估一次，只報 MAE、MSE、RMSE、R²。實際在 Test 上評估的是 {{n_authorized_ols}} 個不同的 OLS 模型（{{authorized_keys}}）加上 {{n_metric_only}} 個 metric-only 模型，共 {{n_evaluated_models}} 個；{{n_winners}} 個 CV winner（含 All-in）共用其中的 OLS 模型。
- 唯一一次正式 Test 評估的執行識別是 {{formal_run_id}}，Test 結果的 sha256 摘要是 {{formal_result_digest}}（紀錄在 repo 的 {{formal_record}}）。之後若完整重跑 notebook，是以相同的 seed 與鎖定的套件版本**重現**同一個評估，結果必須與這個摘要完全相同；本報告建置時會核對這一點，不符就拒絕建置。

### 6.2 訓練 CV 與 Test 的比較

訓練 CV 欄與 Test 欄分開列出，兩者不可混用。Adjusted R² 只對 OLS 子集模型、在 log 尺度以整個 training set 的擬合計算（自由度依設計矩陣的實際秩，整體 winner 為 {{overall_rank}}）；Ridge／Lasso 與 CV 平均值不適用。

{{table:comparison}}

Ridge 與 Lasso 的 Test 指標（metric-only，只出現在比較表）：

{{table:metric_only}}

- 整體 CV winner（{{overall_label}}）在 Test 上的 RMSE 是 **{{overall_test_rmse}} USD**、MAE {{overall_test_mae}} USD、R² {{overall_test_r2}}。
- Test RMSE {{overall_test_higher}}它的訓練 CV RMSE（{{overall_cv_rmse}}），相差 {{overall_test_minus_cv}} USD，約為 CV 各折 RMSE 標準差（{{overall_cv_rmse_std}}）的 {{overall_gap_in_fold_sd}} 倍。兩個原因：第一，從 {{n_methods}} 個方法、每個方法 {{k_max}} 個 k 之中挑 CV RMSE 最小者，會使 **CV winner 的 CV 分數帶有樂觀偏誤**，它不是不偏的估計；凍結選擇之後的 Test 評估才是獨立的估計。第二，USD 的 RMSE 受少數高價房屋的大誤差主導，不同切分之間本來就有相當的波動（見各折的標準差）。依協定，這個差距不會讓我們換模型。
- Adjusted R²（log 尺度）：All-in {{allin_adj_r2_log}}，整體 CV winner {{overall_adj_r2_log}}；與 log 尺度的 R²（{{overall_r2_log}}）幾乎相同，因為樣本數遠大於參數數。

### 6.3 預測區間與經驗涵蓋率 〔老師要求；涵蓋率驗證為專案延伸〕

> {{quote:src1:結果部分需包含}}

對 OLS 子集模型，在 ln(price) 尺度計算參數式 {{pi_level_pct}} 預測區間 ŷ ± t·√(s²(1 + x₀ᵀ(XᵀX)⁻¹x₀))（t 為 t 分布的臨界值，整體 winner 的 t = {{overall_t_crit}}），再以 exp 轉回 USD，所以區間不對稱。每一筆 Test 交易都有自己的區間；預測圖見第九章的 dashboard 截圖（實際 vs 預測，log 刻度，每一筆的垂直區間線段，依是否落在區間內著色，全部 {{n_test}} 筆，沒有抽樣）。

{{table:interval}}

- 整體 CV winner 的經驗涵蓋率是 {{overall_test_coverage}}（{{overall_test_n_covered}}／{{n_test}}），平均區間寬度 {{overall_test_mean_width}} USD。名目的 {{pi_level_pct}} {{overall_nominal_in_band}}二項近似的範圍內。
- 二項近似假設各筆的涵蓋事件彼此獨立。Test 集含 {{test_n_houses}} 棟房屋、{{test_n_repeat}} 筆同一房屋的重複交易，涵蓋事件不保證獨立，所以這個近似的準確度沒有經過估計。
- 區間的假設是殘差常態、同質變異、彼此獨立；它也沒有把特徵選擇的不確定性與可能的模型誤設算進去。第 6.4 節的診斷顯示這些假設在 training 殘差上都有偏離，所以我們**不宣稱保證 {{pi_level_pct}} 的經驗涵蓋率**。總涵蓋率接近名目值，不代表每一類房屋都如此：異質變異與厚尾會讓不同房屋的區間準確度不同，總數中可能互相抵銷。經驗涵蓋率是對區間的檢驗，不是區間正確的證明。

### 6.4 五大回歸假設診斷 〔依老師補充建議〕

診斷用最終模型（整體 CV winner 在整個 training set 上的擬合）在 **training set** 的 log 尺度殘差，不使用 Test 集。違反假設只揭露與分析，不判定失敗；{{n_assumptions}} 項中有 {{n_violations}} 項偵測到偏離。

{{table:diagnostics}}

**線性。** 殘差對擬合值的分箱平均大致在零附近，但 RESET 檢定（加入擬合值的平方與立方）F = {{reset_f}}、p = {{reset_p}}，表示還有線性模型沒有捕捉到的曲率；第八章的公開解法以多項式項或樹模型得到更好的指標，與這一點一致。

![殘差 vs 擬合值（training set，log 尺度）](fig:diag_linearity_residuals_vs_fitted.png)

**誤差獨立。** 依交易日期排序的 Durbin–Watson 是 {{dw}}，接近沒有序列相關的值；但同一棟房屋相鄰兩次交易的殘差相關係數是 {{repeat_corr}}（{{repeat_pairs}} 對，p = {{repeat_corr_p}}）：同一棟房屋的誤差正相關。這是以房屋分組切分的原因，也表示這些交易的誤差獨立假設不成立。

![依日期的殘差與同一房屋重複交易的殘差](fig:diag_independence_residuals_by_date_and_repeat_sales.png)

**同質變異。** Breusch–Pagan（Koenker）檢定 LM = {{bp_lm}}、p = {{bp_p}}：殘差的變異隨欄位而不同，常數 s² 的區間對不同房屋的準確度不一。

![尺度—位置圖](fig:diag_homoscedasticity_scale_location.png)

**殘差常態。** Jarque–Bera = {{jb}}、p = {{jb_p}}；偏態 {{skewness}}、超額峰態 {{kurtosis}}，studentized 殘差絕對值超過常態 {{pi_level_pct}} 臨界值的比例是 {{tail_share}}。殘差分布的尾部比常態厚。

![Studentized 殘差的 Q–Q 圖](fig:diag_normality_qq.png)

**多重共線性。** 每欄 VIF 最大的是 {{max_vif_column}}（{{max_vif}}），相關矩陣的條件數是 {{cond_corr}}；以 GVIF^(1/(2·df)) 衡量 group 層級的共線性時，超過 √10 的是 {{gvif_high_groups}}。這些參考門檻是慣例，只用於閱讀。共線性不影響預測，但使個別係數的解讀與標準誤不穩定。

{{table:gvif}}

![Feature group 的 GVIF](fig:diag_multicollinearity_gvif.png)

**結論。** 五項假設在 training 殘差上都有偏離。點預測與 CV／Test 指標不依賴這些假設；受影響的是係數的標準誤、p-value 與預測區間。經驗涵蓋率接近名目值（第 6.3 節）是對區間的實際檢驗，但不能據此宣稱假設成立。

## 7. Deployment 〔老師要求〕

> {{quote:src2t:6. Deployment: Predict new samples}}

### 7.1 互動 dashboard 〔老師要求（課堂口頭）〕

最終的結果以離線可用的靜態 dashboard 呈現：選擇方法與 k 查看訓練 CV 指標、各方法的 k 路徑比較、即時房價預測與 {{pi_level_pct}} 預測區間、保留 Test 集的實際 vs 預測圖。連結與截圖見第九章。Dashboard 的任何操作都只讀取匯出的結果，不會觸發新的 Test 評估。

### 7.2 預測新樣本 〔依老師補充建議〕

`hw2.deployment.predict_price()` 接受與原始 CSV 相同格式的房屋資料（日期、房間數、面積、建造與整修年、zipcode、經緯度…），回傳點預測（USD）與 {{pi_level_pct}} 預測區間，並標示超出 training 範圍的輸入與未見過的 zipcode。notebook 6.3 以幾筆人工構造的房屋示範，並以匯出的係數直接計算核對；notebook 6.4 示範以 pickle 保存與載入整個模型（dashboard 不讀取 pickle）。

### 7.3 模型解釋 〔依老師補充建議〕

最終模型是 **{{overall_label}}**（與 {{shared_with_overall}} 為同一模型），以 ln(price) 為目標、原始尺度的欄位擬合。

- **每單位的讀法**：係數 b 的意思是「其他欄位固定時，該欄增加 1 單位，預測價格（條件中位數）約變化 (exp(b) − 1)」，以百分比表示。
- **標準化的讀法**：最終模型以原始尺度擬合，係數直接以原始單位解讀，沒有需要還原的標準化；Ridge／Lasso 的標準化只用於它們自己的擬合，不用於這裡的解讀。為了比較單位不同的欄位，下表另列「每增加 1 個 training 標準差」的百分比（標準差只來自 training set）。
- **one-hot 的讀法**：zipcode 的每一欄是相對於基準 zipcode {{zip_baseline}} 的價格差異；`is_renovated` 與 `yr_renovated_effective` 兩欄要一起解讀。

最終模型的係數（不含 zipcode 的 one-hot 欄；百分比與信賴區間依古典 OLS 標準誤）：

{{table:coefficients}}

例如，其他條件相同時，居住面積每增加 1 個 training 標準差（{{coef_sqft_living_sd}} 平方英尺），預測價格約變化 {{coef_sqft_living_pct_sd}}；建築等級高一級約 {{coef_grade_pct}}；臨水約 {{coef_waterfront_pct}}。zipcode 的效果相對於基準類別：

{{table:zipcode}}

![最終模型係數的百分比效果（含信賴區間）](fig:explain_coefficients_percent_effects.png)

**Permutation importance** 〔專案延伸〕：只用 training set，把一個 feature group 的值隨機打亂（{{perm_n_repeats}} 次）後看 ln(price) 的 RMSE 增加多少。它只用於解釋，不用於特徵選擇。最重要的是 {{perm_first}}（RMSE 增加為 baseline 的 {{perm_first_pct}}），其次是 {{perm_second}} 與 {{perm_third}}。排序依 ln(price) 尺度；USD 欄只作參考，它可能是負的，因為 OLS 在 ln(price) 上擬合，並不最小化 USD 誤差。

{{table:permutation}}

![Permutation importance（training set）](fig:explain_permutation_importance.png)

**非因果提醒**：係數與重要性描述的是這份觀察資料中、其他欄位固定時的**關聯**，不是因果效果；不能用來推論「把房子改建成更高的等級，價格就會增加多少」。

### 7.4 使用限制

- 只適用於 King County、與 training 資料相同期間（{{date_min}} 至 {{date_max}}）的房屋交易；超出 training 範圍的輸入仍會計算，但屬於外推。
- 未見過的 zipcode 以基準類別計算，誤差會比較大。
- 預測區間的假設在第 6.4 節都有偏離，區間是近似，不保證 {{pi_level_pct}} 涵蓋。
- 點預測是條件中位數的估計；需要平均價格（例如估計總額）時會系統性偏低。

## 8. 主流或更優解法比較 〔老師要求〕

> {{quote:src1:網路上主流或更優解法}}

以下是四個使用同一份 King County 資料的公開解法。表中的數字都是**來源自己回報的值**（附在來源中的位置），不是本專案重算的結果；各來源的設定與本專案不同，數字不能直接比大小，不可比之處列在表後。

{{table:sources}}

{{table:source_notes}}

**與本專案的比較。**

- **尺度與指標**：本專案的 Test 指標在 USD 尺度（整體 CV winner 的 Test R² {{overall_test_r2}}、RMSE {{overall_test_rmse}} USD）；log 尺度的 R² 只對整個 training set 的擬合計算（{{overall_r2_log}}）。來源 [2] 的 R² 在 log 尺度；來源 [1]、[3] 的 R² 不是在保留的 Test 集上計算；只有來源 [4] 回報 USD 尺度的 Test 指標。
- **切分**：本專案以房屋 `id` 分組切分，同一棟房屋的重複交易不會同時出現在訓練與評估中；四個來源都是隨機切分或沒有切分。重複交易同時出現在兩邊時，評估會偏樂觀。
- **一致的發現**：把 zipcode 當作類別是線性模型的重要改善（來源 [2]；本專案的 permutation importance 也以 {{perm_first}} 排第一）；Ridge／Lasso 對 OLS 沒有改善（來源 [1]；本專案第 5.2 節）。
- **更優的方向**：線性模型的 RESET 檢定顯示還有曲率（第 6.4 節）。來源 [1] 的二次項、來源 [2] 依地區分開的係數、來源 [4] 的梯度提升都在處理這一點，並回報更好的指標。本專案依作業要求只使用線性回歸，著重在可解釋的係數、參數式預測區間與只評估一次的 Test 協定；這些方向是可能的延伸，不在本作業範圍內。

## 9. Dashboard 連結與截圖 〔老師要求（課堂口頭）〕

- GitHub Pages：<{{dashboard_url}}>（發布自 repo 的 `main` 分支）
- 繳交 ZIP 內：解壓後直接以瀏覽器開啟 `index.html`（`file://`），不需要網路或伺服器。
- 原始碼：<{{repo_url}}>

以下截圖在報告建置時以 headless 瀏覽器開啟 `index.html` 擷取（它讀取同一份匯出結果；擷取時封鎖所有網路請求）。

![資料集、特徵數與切分](shot:overview)

![模型選擇：整體 CV winner 的方法，訓練 CV 指標與指標 vs k 圖](shot:model)

![比較全部：四種方法的 k 路徑（All-in、Ridge、Lasso 為參考線）](shot:compare)

![保留 Test 集：實際 vs 預測（log 刻度，每筆的預測區間，依是否落在區間內著色）](shot:test)

![方法與限制](shot:methods)

## 10. GPT 輔助內容 〔老師要求〕

> {{quote:src1:請在報告中明確標示}}

{{pending:gpt}}

## 11. NotebookLM 摘要 〔老師要求〕

{{pending:notebooklm}}

## 附錄 A：ChatGPT 對話 PDF 〔老師要求〕

{{pending:chatgpt_pdf}}

## 附錄 B：重現資訊

- 主程式：`hw2.ipynb`（CRISP-DM 六章）；分析套件 `hw2/`；鎖定版本的 `requirements.txt`；重跑步驟見單元 `README.md`。
- seed {{seed}}；資料 sha256 {{csv_sha256}}。
- 唯一一次正式 Test 評估：執行識別 {{formal_run_id}}，選擇摘要 {{formal_selection_digest}}，Test 結果摘要 {{formal_result_digest}}（{{formal_record}}）。目前匯出檔案記錄的執行識別是 {{file_run_id}}；它是否就是那一次評估：{{file_run_is_formal}}。
- 套件版本：

{{table:versions}}
