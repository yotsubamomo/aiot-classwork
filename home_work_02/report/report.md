# HW2：King County 房價多元線性回歸分析報告

> {{evidence:status}}

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

作業頁正文要求模型評估與加上區間的預測圖（見前面的標示對照表與第 6.3 節）。下面這句出自作業頁的「補充」段，是對這一階段的**建議**，不是作業頁正文的要求；本專案採用的部分是第 6.2 節的 Adjusted R² 與第 6.4 節的五大回歸假設診斷，都標〔依老師補充建議〕：

> {{quote:src2t:5. Evaluation: Compare MAE}}

### 6.1 評估協定 〔專案延伸〕

- 所有選擇（各方法的 k、整體 CV winner、Ridge／Lasso 的 alpha）只用 training set 的交叉驗證決定；選擇固定之後，保留的 Test 集**只評估一次**，Test 結果不回饋任何選擇。Test 排名與 CV 排名不同時也不換模型。
- 被授權在 Test 上評估的是各方法的 CV winner、All-in 與整體 CV winner；canonical subset 相同的 winner 是同一個模型，只評估一次。另依作者核准的對照，Ridge 與 Lasso 各評估一次，只報 MAE、MSE、RMSE、R²。實際在 Test 上評估的是 {{n_authorized_ols}} 個不同的 OLS 模型（{{authorized_keys}}）加上 {{n_metric_only}} 個 metric-only 模型，共 {{n_evaluated_models}} 個；{{n_winners}} 個 CV winner（含 All-in）共用其中的 OLS 模型。
- 唯一一次正式 Test 評估的執行識別是 {{formal_run_id}}，Test 結果的 sha256 摘要是 {{formal_result_digest}}（紀錄在 repo 的 {{formal_record}}）。之後若完整重跑 notebook，是以相同的 seed 與鎖定的套件版本**重現**同一個評估，結果必須與這個摘要完全相同；本報告建置時會核對這一點，不符就拒絕建置。

### 6.2 訓練 CV 與 Test 的比較 〔老師要求；Adjusted R² 為依老師補充建議〕

訓練 CV 欄與 Test 欄分開列出，兩者不可混用。〔依老師補充建議〕Adjusted R² 只對 OLS 子集模型、在 log 尺度以整個 training set 的擬合計算（自由度依設計矩陣的實際秩，整體 winner 為 {{overall_rank}}）；Ridge／Lasso 與 CV 平均值不適用。

{{table:comparison}}

Ridge 與 Lasso 的 Test 指標（metric-only，只出現在比較表）：

{{table:metric_only}}

- 整體 CV winner（{{overall_label}}）在 Test 上的 RMSE 是 **{{overall_test_rmse}} USD**、MAE {{overall_test_mae}} USD、R² {{overall_test_r2}}。
- Test RMSE {{overall_test_higher}}它的訓練 CV RMSE（{{overall_cv_rmse}}），相差 {{overall_test_minus_cv}} USD，約為 CV 各折 RMSE 標準差（{{overall_cv_rmse_std}}）的 {{overall_gap_in_fold_sd}} 倍。兩個原因：第一，從 {{n_methods}} 個方法、每個方法 {{k_max}} 個 k 之中挑 CV RMSE 最小者，會使 **CV winner 的 CV 分數帶有樂觀偏誤**，它不是不偏的估計；凍結選擇之後的 Test 評估才是獨立的估計。第二，USD 的 RMSE 受少數高價房屋的大誤差主導，不同切分之間本來就有相當的波動（見各折的標準差）。依協定，這個差距不會讓我們換模型。
- 〔依老師補充建議〕Adjusted R²（log 尺度）：All-in {{allin_adj_r2_log}}，整體 CV winner {{overall_adj_r2_log}}；與 log 尺度的 R²（{{overall_r2_log}}）幾乎相同，因為樣本數遠大於參數數。

### 6.3 預測區間與經驗涵蓋率 〔老師要求；涵蓋率驗證為專案延伸〕

> {{quote:src1:結果部分需包含}}

對 OLS 子集模型，在 ln(price) 尺度計算參數式 {{pi_level_pct}} 預測區間 ŷ ± t·√(s²(1 + x₀ᵀ(XᵀX)⁻¹x₀))（t 為 t 分布的臨界值，整體 winner 的 t = {{overall_t_crit}}），再以 exp 轉回 USD，所以區間不對稱。每一筆 Test 交易都有自己的區間。下圖是主程式（notebook 5.5.1）從唯一一次 Test 評估匯出的逐筆結果畫出的預測圖：x 為預測、y 為實際，log 刻度，y = x 參考線，每一筆一條垂直的預測區間線段，依實際價格是否落在區間內著色；全部 {{n_test}} 筆都畫出，沒有抽樣或聚合。畫圖只讀取匯出的結果，不是新的評估。互動版本見第九章的 dashboard。

![保留 Test 集：實際 vs 預測與每一筆的 {{pi_level_pct}} 預測區間（每個被授權評估的 OLS 模型一個面板）](fig:eval_actual_vs_predicted_pi.png)

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

作業頁正文要求的是 CRISP-DM 的 Deployment 階段。下面這句出自作業頁的「補充」段，是對這一階段的**建議**，不是作業頁正文的要求；本專案採用它，見第 7.2 節與第 7.3 節，都標〔依老師補充建議〕：

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

本章揭露 ChatGPT 與 Claude Code 在本專案中各自的用途；NotebookLM 的使用見第十一章。

### 10.1 ChatGPT

{{evidence:gpt}}

### 10.2 Claude Code

Claude Code（Anthropic 的 AI 程式開發工具）在本專案做了下列工作；過程、決定與審查紀錄都在 repo 的 `home_work_02/doc/`。

- **需求與設計文件**：以 MATT 工作流程釐清需求（Grill，由 Claude Code 提出問題與建議選項），撰寫 Brief 與 `CONTEXT.md`；以 `/to-spec` 產生 Spec 並依審查意見修正；以 `/ui-ux-pro-max` 產生 dashboard 的 wireframe；以 `/to-tickets` 拆成 GitHub Issues 上的實作票。
- **治理角色**：Design Authority、Orchestrator、Executor 與獨立 Reviewer 由不同的 Claude Code session 或 subagent 擔任，紀錄在 `doc/governance/`。
- **實作**：主程式 `hw2.ipynb`、分析套件 `hw2/`、互動 dashboard（`index.html`、`assets/`）、Python 與 JavaScript 測試、報告建置程式、單元 `README.md` 與驗收清單。
- **本報告**：除了老師原文的引用，報告的文字由 Claude Code 撰寫；本專案的數字、表與圖由建置程式從主程式的匯出結果注入。第八章的公開解法由 Claude Code 開啟原文逐一核對。第 10.1 節與第十一章的摘要，是 Claude Code 依作者提供的材料整理，不新增材料沒有的內容。
- **沒有做的事**：Claude Code 沒有產生、改寫或替代作者與 ChatGPT 的對話或 NotebookLM 的輸出；附錄 B 是作者提供的對話 PDF 原頁。

## 11. NotebookLM 摘要 〔老師要求〕

> {{quote:src1:請使用 NotebookLM}}

{{evidence:notebooklm}}

## 12. 探索模式（加分功能） 〔老師要求（新版作業頁的加分）〕

老師在更新後的作業頁（SRC-4）公告兩項加分：「有下拉視窗呈現兩種problem」與「可任意輸入 Dataset」，老師的例子是一個 CSV 的 URL（`50 Startups` 資料集）。本章說明 dashboard 為此新增的功能、分析方法、與前面各章正式分析的差異，以及限制與揭露。

本章**不含任何探索結果的數字**：探索結果每次在瀏覽器內重新計算，不保存、不進本報告的數字，也不是 Test 評估。前面各章與附錄的內容與數字只描述 King County 的正式分析，不受探索模式影響。

| 項目 | 標示 |
| --- | --- |
| Dashboard 以下拉呈現兩種 problem | 老師要求（新版作業頁的加分）；「同一頁以下拉切換兩個資料集／問題」是本專案對原文的解讀，老師原文沒有進一步定義 |
| 可任意輸入資料集（CSV 的 URL 或本機檔案） | 老師要求（新版作業頁的加分） |
| 探索模式的分析方法、評估方式、運算預算、進度與取消 | 專案延伸（本專案的決定，不是老師的要求） |
| 老師的範例資料 `50 Startups` 打包在單元內 | 專案延伸 |

### 12.1 加分功能 〔老師要求（新版作業頁的加分）〕

- **下拉呈現兩種 problem**：dashboard 頂端的「分析問題（Problem）」下拉有三項：King County 房價（正式分析，就是第九章的 dashboard）、`50 Startups` 利潤（探索）與自訂資料集（探索）。`50 Startups` 是老師給的範例資料，逐位元打包在單元的 `assets/data/`（取自 GitHub repository `Avik-Jain/100-Days-Of-ML-Code`，該 repository 以 MIT License 發布；來源、sha256 與授權聲明都在同一目錄），所以在繳交 ZIP 內以 `file://` 開啟、沒有網路也能選取執行。它只是示範 problem，不宣稱符合作業的特徵數條件。
- **任意輸入資料集**：選「自訂資料集」後，可貼 CSV 的 URL（由瀏覽器直接讀取）或選本機 CSV 檔案；預測目標欄預設最後一欄，可以改選。URL 讀取失敗（網路或跨來源限制、HTTP 狀態、逾時、回應不是文字）時，畫面寫出原因，並提示下載後改以本機檔案載入。
- **網路請求**：頁面載入、King County 與 `50 Startups` 的所有操作、以本機檔案載入，都不發出任何對外請求。唯一的對外請求是使用者在自訂資料集提交 URL 之後，對該 URL 的一次 GET：不帶 cookie 等憑證、不跟隨重新導向、不重試。
- 每個探索區塊都標示「探索執行，非正式評估」；King County 的區塊沒有這個標示。

### 12.2 分析方法 〔專案延伸〕

探索模式在瀏覽器內執行一次 Exploratory run。它沿用正式分析的選模語義，但沒有任何 King County 專屬的規則：

- **載入**：UTF-8、逗號分隔、第一列為欄名的 CSV。每個非空儲存格都能解析為有限數字的欄是數值欄，其他是類別欄；含缺值的列整列刪除並顯示筆數；目標必須是數值欄。載入只檢查 CSV 的結構，不計算任何欄位的分布。
- **切分與前處理**：固定 seed 的逐列隨機切分；訓練與 test 的比例、訓練列的 fold 數與正式分析相同，但不分組（正式分析的切分見第 4.4 節）。類別欄的層級數上限與常數欄的排除只用訓練列判定；每個 fold 的類別層級、基準與 Lasso 的標準化只從該 fold 的訓練列學；canonical 路徑與最終擬合只用整個訓練列；test 列在全部選擇固定之後才讀取。
- **特徵選擇**：一個來源欄＝一個 feature group，整組進出。Forward／Backward SFS 以 RSS、RFE 以 group 對擬合值貢獻的標準差 sd(X_g β_g)、Lasso 路徑以 exact LARS 的進入順序，平手依 CSV 欄序；另有 All-in baseline。每個方法在每個 fold 的訓練列上重新選擇（fold 內選擇），候選的 CV 指標是各 fold 指標的平均。
- **候選狀態與 winner**：每個 (方法, k) 候選只有一個狀態——有效（`VALID`）；無效（`INVALID_MODEL`：任一 fold 或整個訓練集上設計矩陣秩不足或殘差自由度不足，或 Lasso 路徑停止之後的 k）；超出運算限制而未執行（`SKIPPED_RESOURCE_LIMIT`）；非預期的計算失敗（`FAILED`，只影響該方法）。各方法與整體 CV winner 只從有效候選中以 CV RMSE 選出，平手規則與正式分析相同。全部候選都無效時整個執行拒絕，並顯示共線診斷：哪些編碼欄線性相依、對應哪些 feature group，不指認單一的問題欄。
- **評估**：指標 vs k 圖與 KPI 只用訓練 CV。探索 test 只對各方法與整體 CV winner 計算一次：MAE、MSE、RMSE、R²，以及以與正式分析相同的 OLS 參數式公式、在目標原始尺度計算的逐筆預測區間與涵蓋率；它不回饋任何選擇。即時預測器只對目前選取的有效候選提供預測。
- **數值驗證**：單元的測試以一份通用的 Python 參照即時產生參照結果，與瀏覽器端的引擎逐值比對；同一份參照套在 King County 的正式訓練表上，重現正式分析的四條 canonical 路徑與 All-in，所以兩個 problem 用的是同一套選模準則。

### 12.3 與正式分析的差異 〔專案延伸〕

| 項目 | King County（正式分析） | 探索模式（`50 Startups`、自訂資料集） |
| --- | --- | --- |
| 目標尺度 | 以 ln(price) 建模，預測與區間以 exp 轉回 USD（第 4.3 節） | 原始尺度建模與報告，不取 log；目標可以是負值或零 |
| 切分 | 以房屋 `id` 分組的切分與分組 fold（第 4.4 節） | 逐列隨機切分與逐列 fold，沒有分組欄 |
| Lasso 路徑沒有讓全部 group 進入時 | 未進入的 group 依欄序補成 k = {{k_range}} 的子集，這是 King County 的選模語義 | 停在已進入的 group（見下段）；之後的 group 只作展示，k 超過的候選無效 |
| 派生規則 | 交易日期轉天數、整修年拆成旗標與有效年份、zipcode 為類別（第 4.1 節） | 沒有；一個來源欄就是一個 feature group |
| Test 的地位 | 唯一一次的正式 Test 評估，記錄在案（第 6.1 節） | 探索 test：每次執行探索都重新計算、不保存，永遠不是 Test 評估 |

**Lasso 路徑的停止。** 在某一批列（某個 fold 的訓練列，或整個訓練集）上，LARS 路徑結束時若仍有 group 未進入——不論原因是 active set 退化、路徑走到終點時其餘 group 與殘差的相關在數值上為零、同一步有多個 group 同時離開路徑、預測目標在這些列上沒有變化，或數值上的停止（alpha 回升、迭代達上限）——一律同樣處理：已求得的路徑段（entry alpha 與順序）是實際結果；未進入的 group 只依 CSV 欄序列出作展示，不是實際路徑，也不構成選模依據；k 超過已進入 group 數的 Lasso 候選為無效（`lasso_path_degenerate`），不以欄序補齊。畫面寫出實際的停止原因，只陳述已確立的事實，例如「走到終點」不代表那些 group 一定與已進入的欄共線。停止與平手的數值判定在「目標在同一批列上置中後除以其均方根」的尺度上計算，所以把目標換單位（乘上任何正常數）不改變進入順序、停止點與候選狀態；entry alpha 仍以目標的原始尺度回報。

### 12.4 限制與揭露 〔專案延伸〕

- **逐列切分可能洩漏**：資料中若有重複的列、同一個實體的多筆紀錄（例如同一家公司或同一個人的多次觀測），或時間相依的資料，同一來源的資訊可能同時出現在訓練與 test（或同一 fold 的訓練與驗證）列，使 CV 與 test 指標過度樂觀。探索結果只供操作與比較，**不代表正式研究結論**。
- **不是正式評估**：探索結果不保存（不寫入瀏覽器儲存、cookie、URL 參數或檔案）、不進本報告的數字，也不是 Test 評估；探索程式不讀取匯出的 `model_data`。CV winner 的 CV 分數帶有樂觀的選擇偏誤。預測區間假設殘差常態、同質變異、彼此獨立，不保證名目的經驗涵蓋率。
- **運算預算**：Forward SFS、Backward SFS、RFE 與 Lasso 路徑在執行前依資料大小（訓練列數與編碼欄數）估計運算量，只依估計、不依耗時；超過預算的方法整個標為超出運算限制、不執行，其他方法照跑。All-in baseline 一律最先嘗試、不會被略過，但不保證任何資料都能在特定時間內完成。本報告不承諾任何執行時間。
- **取消與改選的生效時點**：執行中按「取消執行」，或改選資料、目標欄或 problem 時，進行中的執行在目前的候選算完後（下一個候選邊界）才停止；全部候選完成之後（計算共線診斷與探索 test 時），則在進行中的步驟完成時停止。新的執行要等前一次停止後才開始。取消後不顯示任何結果，只顯示「已取消」與已完成的方法數；再次執行從頭開始。在接近載入上限、類別層級多的資料上，單一候選（包括一律嘗試的 All-in）可能需要數分鐘；這段期間頁面仍可操作、進度與已耗時持續更新、King County 可用，但取消或新的執行要等這個候選算完。
- **沒有檔案大小上限**：載入上限只以列數與欄數判定。URL 的回應與本機檔案都整份讀入瀏覽器的記憶體；超過列數或欄數上限的輸入以超過載入上限（`TOO_LARGE`）拒絕、不截斷。極大的檔案可能無法讀取：接近瀏覽器能以文字處理的大小時，可能耗盡分頁的記憶體使分頁當掉，而不是顯示訊息；更大的檔案改以位元組逐段檢查，需要數秒，期間頁面不回應輸入。頁面偵測到瀏覽器無法處理這份輸入（例如解碼或配置記憶體失敗）時，畫面如實說明是大小或記憶體的限制，不會說成格式或編碼錯誤。
- **URL 讀取**：對方伺服器必須允許跨來源讀取（CORS），例如 GitHub 上的檔案要用 Raw 連結；需要登入、會重新導向或不允許跨來源的網址會失敗，此時請下載後以本機檔案載入。
- **實作常數與實測**：載入上限、類別欄的層級數上限、各方法的運算預算與 URL 讀取逾時的數值，以及決定它們的實測，記在單元 `README.md` 的「探索模式（加分功能）」與驗收清單 `doc/acceptance/ACCEPTANCE.md` 的 G 節；本報告不重抄這些數值，也不陳述任何執行時間。

### 12.5 前面各章的範圍

- 前面各章（標示說明與對照表、第一章到第十一章與附錄）引用或描述的作業頁內容，依的是撰寫正式分析時的舊版作業頁；為了讓正式分析的內容不變，這些引用與標示保留原文。更新後的作業頁（SRC-4）有兩處與此不同。一是主要繳交改為「跟 DIC2 一樣github and web」：本專案的 web 交付就是 GitHub Pages 上的這個 dashboard，所以 GitHub repository 與這個 dashboard 現在是作業頁正文列出的主要繳交；標示說明與對照表、第 7.1 節與第九章的「課堂口頭」標示與「作業頁正文沒有要求網站」只描述舊版作業頁，dashboard 的標示類別仍是老師要求，改變的只是來源。二是特徵數條件改為 `>13` 個特徵；第 1.2 節的交集條件依舊版作業頁，King County 的 source feature 數也符合新條件。舊版的「補充」段在更新後的作業頁沒有載明，本報告不推定老師已刪除它。
- 第 7.1 節與第九章所說的 dashboard，是頁面上的 King County（正式分析）檢視：它只讀取匯出的結果，任何操作都不會觸發新的 Test 評估，也不發出任何對外請求。探索模式是同一個頁面上另外的檢視，在瀏覽器內計算，不讀取也不改寫匯出的結果。
- 探索模式的實作、測試與文件同樣由 Claude Code 完成，紀錄在 repo 的 `home_work_02/doc/`（見第 10.2 節）。

## 附錄 A：重現資訊

- 主程式：`hw2.ipynb`（CRISP-DM 六章）；分析套件 `hw2/`；鎖定版本的 `requirements.txt`；重跑步驟見單元 `README.md`。
- seed {{seed}}；資料 sha256 {{csv_sha256}}。
- 唯一一次正式 Test 評估：執行識別 {{formal_run_id}}，選擇摘要 {{formal_selection_digest}}，Test 結果摘要 {{formal_result_digest}}（{{formal_record}}）。目前匯出檔案記錄的執行識別是 {{file_run_id}}；它是否就是那一次評估：{{file_run_is_formal}}。
- 套件版本：

{{table:versions}}

## 附錄 B：ChatGPT 對話 PDF 〔老師要求〕

> {{quote:src1:所有與 ChatGPT 的對話}}

{{evidence:chatgpt_pdf}}
