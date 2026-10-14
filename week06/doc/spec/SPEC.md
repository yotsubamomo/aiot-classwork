# Spec: 50 Startups Multiple Linear Regression & Feature Selection Explorer（DIC-2）

- **專案識別**：`AIoT2026-DIC2-MultipleLR`
- **依據**：老師的 DIC-2 成果網站 <https://huanchen1107.github.io/AIoT-DIC2-MultipleLR/> 與其原始碼 `huanchen1107/AIoT-DIC2-MultipleLR`，固定在 commit `8b65e3bd9745e650ae7bea28f9562c059d5029ed`（2026-10-14）。這是**參考成果**，不是題目原文：repo 中沒有老師 DIC-2 的需求文字，若之後取得，放進 [`../requirement/`](../requirement/)，並以它為準重新核對本 spec。
- **狀態**：定案，待實作（2026-10-14）。第 9 節 D-1～D-6 依建議定案。**優先順序：先完成當週課堂練習，本 spec 保留到之後再實作**
- **Issue tracker**：未開票，本 spec 暫存為檔案
- **單元與治理**：`week06/`（DIC），governance off，只適用 root `CLAUDE.md`

## 1. Problem Statement

老師在 DIC-2 示範了一個網站：以 Kaggle 的 50 Startups 資料集做多元線性回歸，用 5 種特徵選擇演算法，比較選 1～5 個特徵時的模型表現，並以互動頁面呈現 KPI、圖表、回歸方程式、係數統計、即時預測器與殘差診斷。

我們要做出自己的版本並上傳。目前 `week06/` 是空的，對使用者來說的問題是：

- 沒有自己的 DIC-2 成果可以展示或繳交。
- 老師的成果無法從 repo 完整重現：網站讀取的 `model_data.json` 含係數的 SE、t、p、CI、VIF 與殘差表，但 repo 裡**沒有任何腳本會產生它**（`feature_progression_analysis.py` 只輸出 RMSE／R² 的 CSV 與圖，`main.py` 是另一套 CLI 分析）。
- 參考成果有幾個方法上的問題（第 8 節），照抄會把問題一起帶進來。

## 2. Solution

在 `week06/` 做一個**可從原始碼完整重現**的版本，維持 week02 的做法：零建構、可直接部署到 GitHub Pages。

- **分析管線（Python）**：一支腳本從資料下載、切分、5 種特徵選擇、k=1～5 的評估，一路到係數統計與殘差，產生網站用的資料檔。每一個數字都能由這支腳本重跑得到。
- **網站（Vanilla HTML／CSS／JS＋Chart.js）**：功能對齊參考網站，包括演算法切換、k 切換、KPI、兩張折線圖、回歸方程式、係數統計表、即時預測器與殘差表。網站讀取預先算好的資料檔，不需要後端。
- **發布**：GitHub Pages 的 `https://yotsubamomo.github.io/aiot-classwork/week06/`，與 week02 相同的方式。

## 3. 範圍分類

| Class | 內容 |
| --- | --- |
| **PARITY**（對齊參考） | 第 4 節的 user stories：參考網站已有的全部可見功能 |
| **REPRO**（我們補的必要項） | 產生網站資料的完整腳本、固定的相依版本、README 的重跑步驟；參考成果缺少這些 |
| **DECIDED**（已定案的偏離） | 第 9 節 D-1～D-6：方法修正與參考網站沒有的功能，已依建議定案 |
| **REFERENCE** | 老師 repo 的程式與 README、`week05/` 的 50 Startups notebook。只作參考，不構成要求 |

## 4. User Stories

### 資料與分析

1. 身為學習者，我想用與參考相同的 50 Startups 資料（50 筆、`R&D Spend`、`Administration`、`Marketing Spend`、`State`、目標 `Profit`），讓結果可以與老師的成果對照。
2. 身為學習者，我想看到 `State` 經 one-hot 編碼成 `State_Florida`、`State_New York`，以 California 為基準，讓候選特徵正好是 5 個。
3. 身為學習者，我想對 5 種演算法（Lasso L1 Ranking、Forward SFS、RFE、ElasticNet Ranking、Exhaustive Best Subset）各得到 k=1～5 的特徵子集，以比較它們挑特徵的順序。
4. 身為學習者，我想對每個（演算法, k）組合看到 RMSE、MAE、R²、Adjusted R²、F 統計量與其 p-value。
5. 身為維護者，我想只執行一支腳本就重新產生網站用的全部數字，讓成果可以重現與檢查。

### 演算法與特徵數切換

6. 身為使用者，我想用下拉選單切換 5 種演算法，整頁的 KPI、圖表、方程式、係數表、預測器與殘差表都跟著更新。
7. 身為使用者，我想有「Compare All 5 Methods」按鈕，在同一張圖上比較 5 種演算法的曲線。
8. 身為使用者，我想切換 k = 1～5，即時看到該子集的結果。

### 指標與圖表

9. 身為使用者，我想看到 KPI 卡片：Test RMSE、R²、Adjusted R²、MAE、F 統計量（含 p-value）與目前使用的特徵。
10. 身為使用者，我想看到「RMSE by Number of Features」與「R-squared by Number of Features」兩張折線圖，並標出目前的 k 與最佳點。
11. 身為使用者，我想把滑鼠移到圖上的點時，看到該點的 k、特徵與數值。

### 方程式與係數

12. 身為使用者，我想看到目前模型的回歸方程式，例如 `Profit = β₀ + β₁ × (R&D Spend) + …`，隨 k 與演算法即時更新。
13. 身為使用者，我想看到係數表：Predictor、Estimate（β）、Std. Error、t-Stat、p-Value、95% CI（係數）、VIF。

### 預測與診斷

14. 身為使用者，我想輸入 R&D、Marketing、Administration 與 State，立即看到預測利潤，並看到每個特徵對預測值的貢獻。
15. 身為使用者，我想看到 Test set 的殘差表：排名、樣本編號、實際值、預測值、殘差、絕對誤差、百分比誤差與診斷狀態，依絕對殘差排序。

### 說明與部署

16. 身為老師或訪客，我想看到依 CRISP-DM 六階段整理的專案說明、資料來源與參考資料。
17. 身為擁有者，我想從 repo 根目錄的 README 與 `week06/README.md` 開啟 Live Demo。

## 5. Implementation Decisions

### 5.1 資料與切分（對齊參考）

- **資料來源**：`https://raw.githubusercontent.com/Avik-Jain/100-Days-Of-ML-Code/master/datasets/50_Startups.csv`（與參考相同）。下載後計算 sha256 並寫入資料檔的 metadata；同時在 `week06/` 保留一份本機副本作為離線備援。
- **編碼**：`pd.get_dummies(State)`，候選特徵固定為 `["R&D Spend", "Administration", "Marketing Spend", "State_Florida", "State_New York"]`。
- **切分**：`train_test_split(test_size=0.20, random_state=0)`，得到 40 筆 train、10 筆 test，與參考相同。
- **標準化**：`StandardScaler` 只在 train 上 fit，供 Lasso、ElasticNet、RFE 使用。

### 5.2 五種特徵選擇（對齊參考的 `feature_progression_analysis.py`）

| 演算法 | 子集產生方式 |
| --- | --- |
| Lasso (L1 Ranking) | 在標準化的 train 上跑 `LassoCV(cv=5, random_state=0)`，依 \|coef\| 由大到小排序，取前 k 個 |
| Forward SFS | `SequentialFeatureSelector(LinearRegression(), n_features_to_select=k, direction="forward")`，fit 在 train |
| RFE | `RFE(LinearRegression(), n_features_to_select=k)`，fit 在標準化的 train |
| ElasticNet Ranking | 在標準化的 train 上跑 `ElasticNetCV(cv=5, random_state=0)`，依 \|coef\| 排序取前 k 個 |
| Exhaustive Best Subset | 對每個 k 列舉所有組合，依 D-1 以 train 上的 5-fold CV RMSE 選子集（老師的版本用 test RMSE） |

每個子集都以 `LinearRegression` 在 train 上 fit，並在 test 上計算 RMSE、MAE、R²。

### 5.3 統計量（參考成果沒有產生腳本；定義已由其資料檔反推驗證）

- 係數統計用 `statsmodels` 的 OLS，**在 train 上 fit**（含常數項），取得 β、SE、t、p、95% CI。
- VIF 用 `variance_inflation_factor`，對該子集的 train 設計矩陣（含常數項）計算。
- Adjusted R² 依 test 的 n 與 k 計算；F 統計量與其 p-value 取自 train 的 OLS。實作時要在 README 寫清楚每個指標是用哪一份資料算的。
- **驗證**（2026-10-14，以參考的 `model_data.json`、Lasso k=2 子集 `[R&D Spend, Marketing Spend]` 重算）：
  - train OLS 的 β(R&D) = 0.7886、β₀ = 46,346.34，與參考的 coef 0.788618 相符；
  - train F = 349.0，與參考的 `f_stat` 349.04 相符；
  - 以 test n=10 計算的 Adjusted R² = 0.9324，與參考的 0.932421 相符。
  - 所以上面的定義與參考一致。
- 殘差表使用 test 的全部 10 筆，依 |residual| 排序。

### 5.4 資料檔（data contract）

沿用參考的結構，只多加一個 `meta` 區塊，讓前端可以直接沿用參考的資料存取方式：

```text
{
  "meta": { "source_url", "csv_sha256", "random_state", "test_size", "generated_at", "versions" },
  "<Algorithm>": [            // Lasso, Forward SFS, RFE, ElasticNet, Exhaustive，各 5 筆（k = 1..5）
    { "k", "features": [...], "rmse", "mae", "r2", "adj_r2", "f_stat", "f_pvalue",
      "coefficients": [ { "feature", "coef", "stderr", "tstat", "pvalue", "ci_lower", "ci_upper", "vif" } ],
      "outliers":     [ { "rank", "index", "actual", "predicted", "residual", "abs_error", "pct_error" } ] }
  ]
}
```

同一份內容輸出成 `model_data.json`（給腳本與測試用）與 `model_data.js`（`window.MODEL_DATA = …`，讓頁面不經 fetch 也能以 `file://` 開啟）。

### 5.5 前端

- **技術**：Vanilla HTML／CSS／JS；Chart.js 以 CDN 固定版本 `chart.js@4.4.1` 載入（與參考相同）；不使用 build 工具。
- **模組切分**（比照 week02 的 `core.js`／`app.js`）：
  - `core.js`：純函式，例如由係數與輸入計算預測值與各特徵貢獻、找出最佳 k、格式化數字。可以在 Node 中測試。
  - `app.js`：DOM、事件與 Chart.js。
- **介面語言**：英文，與參考及 week02 一致。README 用 zh-TW。
- **「最佳 k」標示**：由資料計算，不寫死在 HTML（參考把 k=2 的 ★ 寫死）。計算規則依 D-1。
- **Compare All**：見 D-6。

### 5.6 檔案配置

```text
week06/
├── doc/spec/SPEC.md       # 本檔
├── README.md              # 專案資料、Live Demo、重跑步驟、CRISP-DM 摘要
├── analysis.py            # 5.1–5.4 的完整管線，產生 model_data.json / model_data.js
├── requirements.txt       # 固定版本：numpy、pandas、scikit-learn、statsmodels（matplotlib 只在需要輸出圖時）
├── 50_Startups.csv        # 資料的本機副本（sha256 記在 metadata）
├── model_data.json
├── model_data.js
├── index.html
├── style.css
├── core.js
├── app.js
└── tests/                 # Python 與 JS 測試
```

## 6. Testing Decisions

### 什麼是好的測試

- 只測外部可觀察的行為：腳本輸出的數字與資料檔結構、`core.js` 的計算結果。
- 不測 Chart.js 或 DOM 的內部細節。

### 測試範圍與項目

- **重現性**：連續執行 `analysis.py` 兩次，產生的 `model_data.json`（不含 `generated_at`）逐位元相同。
- **對齊參考**：對 Lasso、Forward SFS、RFE、ElasticNet，k=1～5 的特徵子集與 test RMSE，與參考 README 的比較表一致（容許 ±0.01 USD 的浮點誤差）。Exhaustive 依 D-1 的決定另訂期望值。
- **統計量**：β、SE、t、p、CI 與 `statsmodels` 直接計算的結果一致；VIF ≥ 1。
- **資料檔結構**：5 種演算法 × 5 個 k 都存在，欄位齊全，數值型別正確。
- **前端計算**：`core.js` 的預測值等於 β₀ + Σβᵢxᵢ；State 為 California 時不加任何 dummy；最佳 k 依 D-1 的規則算出。
- **部署 smoke**：`index.html` 以 `file://` 與 GitHub Pages 開啟都能載入資料，主控台沒有錯誤。

### 既有做法

比照 `week02/tests/core.test.js`（JS 純函式測試）；Python 端用 pytest。

## 7. Out of Scope

- Flask 後端與 REST API（`/api/models`、`/api/predict`、`/api/summary`）、Vercel 部署：GitHub Pages 無法執行，見 D-3。
- 換資料集或加入參考沒有的模型（例如非線性模型）。
- 使用者上傳資料、帳號、資料庫。
- `week05/` 的任何修改。

## 8. 參考成果的已知問題（證據來自 commit `8b65e3bd`）

| # | 問題 | 證據 | 本 spec 的處理 |
| --- | --- | --- | --- |
| R-1 | Exhaustive Search 依 **test RMSE** 挑子集，「k=2 最佳」也是依 test RMSE 判定，等於用 test set 選模型 | `feature_progression_analysis.py` 第 89–94 行 | D-1 |
| R-2 | test set 只有 10 筆，k 之間的 RMSE 差距（例如 $8,198 vs $8,171）在雜訊範圍內，「k=5 overfitting cliff」證據薄弱；殘差表的「前 10 名」就是全部 test 資料 | `test_size=0.20`，50 筆資料 | 頁面加一句說明，不修改資料；見 D-1 |
| R-3 | 網站結論（k=2）與 repo 內 `main.py` 的結論（5-fold CV，`random_state=42`，五種方法都選 3 個特徵）互相矛盾 | `feature_selection_comparison.csv` | D-1 |
| R-4 | 網站沒有**預測值**的區間；95% CI 只針對係數，Live Predictor 只給點估計 | 頁面與 `index.html` 第 1330 行起的 `calculateLivePrediction` | D-2 |
| R-5 | `model_data.json` 無法由 repo 內的腳本產生 | repo 中沒有寫出該檔的程式 | 5.3、5.4：由 `analysis.py` 產生 |
| R-6 | 「Compare All」時 KPI 卡片固定顯示 Lasso 的數據；F 統計量缺值時顯示寫死的 `347.8`；k=2 的 ★ 寫死在 HTML。HTML 的預設文字與資料檔不符，JS 載入後才被取代：第 953 行的方程式寫成 `44,050.85 + 0.825 × R&D + 0.024 × Marketing`，資料檔的 train 係數則是 46,346.34、0.7886、0.0326。不執行 JS 時，訪客看到的就是錯的方程式 | `index.html` 的 `getActiveModelData`、`updateDashboard`，以及第 893、953、1044 行 | 5.5（數值全部由資料檔產生，HTML 不寫死數字）、D-6 |
| R-7 | README 所說的 Flask API 不在 GitHub Pages 上運作，只在 Vercel 版執行 | `app.py`、`vercel.json` | D-3 |

## 9. 決定事項（2026-10-14 依建議定案）

使用者 2026-10-14 指示：「後續會先照課堂練習執行，所以上面的先保留起來照你的建議。」各項依先前提出的建議定案（見下表「定案」欄）；D-5 原本只舉例、沒有明確建議，先暫定沿用 week02 的「Momo」，可再改。

| ID | 問題 | 選項 | 定案 |
| --- | --- | --- | --- |
| D-1 | 「最佳 k」與 Exhaustive Search 的選擇標準 | (a) 照參考，用 test RMSE；(b) 用 train 上的 5-fold CV RMSE 選，test 只用來回報 | **定案 (b)**：避免用 test 選模型，與 HW2 的作法一致；網站同時顯示 CV RMSE 與 Test RMSE，並說明數字會與老師版本不同 |
| D-2 | 是否加入預測值的區間 | (a) 不加，與參考相同；(b) Live Predictor 顯示 95% 預測區間（statsmodels `get_prediction`），並加一張實際 vs 預測圖附區間 | **定案 (b)**：老師在 HW2 要求「預測圖加上信賴區間或預測區間」，DIC-2 先練習 |
| D-3 | 是否做 Flask API／Vercel | (a) 只做靜態頁；(b) 另做 Flask 與 Vercel | **定案 (a)**：與 week02 一致，GitHub Pages 即可展示全部功能 |
| D-4 | 資料集與切分 | (a) 與參考相同（50 Startups，`random_state=0`）；(b) 換資料或改切分 | **定案 (a)**：方便與老師的成果對照 |
| D-5 | 網站的顯示名稱與作者資訊 | 例如沿用 week02 的「Momo」 | **暫定「Momo」**（沿用 week02；未明確確認，可再改） |
| D-6 | 「Compare All」的行為 | (a) 照參考，只在圖上疊 5 條線；(b) 另加 5 種方法的比較表，KPI 卡片改顯示比較摘要 | **定案 (b)**：避免 KPI 顯示的數字與畫面上的選擇不符 |

## 10. Further Notes

- 如果之後取得老師 DIC-2 的題目原文，題目優先於本 spec 與參考成果；放入 `doc/requirement/` 後重新核對第 3、4 節。
- 參考的設計靈感來源是 StatsUnlock 的 multiple linear regression calculator；版面可參考，但不複製其商標或文案。
- 完成後在 root `README.md` 的「課堂實作」表新增 DIC-2 一列，連到 `week06/`。
