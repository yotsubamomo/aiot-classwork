# DIC-02 — 50 Startups 多元線性回歸：特徵選擇比較

## 專案資料

- **課程名稱**：AIoT 與數據分析（AIoT & Data Analytics, AIoT-DA）
- **課堂實作**：DIC-02（Do in Class 2）— Multiple Linear Regression 與特徵選擇
- **示範教師**：Huan Chen（參考成果：[AIoT-DIC2-MultipleLR](https://huanchen1107.github.io/AIoT-DIC2-MultipleLR/)）
- **網站顯示名稱**：Momo
- **完成日期**：2026-10-14
- **Live Demo Page**：`https://yotsubamomo.github.io/aiot-classwork/week06/`（合併進 `main` 後生效）

## 專案摘要

以 Kaggle 的 50 Startups 資料集，依 CRISP-DM 流程預測新創公司的 `Profit`。比較五種特徵選擇方法，在選 k = 1～5 個特徵時的表現：

- 5 個候選特徵：`R&D Spend`、`Administration`、`Marketing Spend`、`State_Florida`、`State_New York`。State 做 one-hot，以 California 為基準，兩個 dummy 可以各自被選或不選。
- 80/20 切分（`random_state=42`），train 40 筆、test 10 筆。
- 五種方法：Exhaustive Search、Forward SFS、Lasso（L1）Top-k、RFE、Elastic Net Top-k。每個子集都用 OLS（`LinearRegression`）重新擬合，讓比較公平。
- **只在 train 上做巢狀交叉驗證**：
  - outer 5-fold 評估表現；
  - 每個 outer-train fold 內，再用 inner 5-fold 選特徵、調整懲罰。
- 最佳 k 只依 CV RMSE 選擇；test 只在最後評估一次，不參與任何選擇。
- 互動式網頁（`index.html`）呈現全部結果，並提供附 95% 預測區間的即時預測。

## 主要結果

各方法的最佳 k（依 CV RMSE），以及在 held-out test 上的表現：

| 方法 | 最佳 k | 選到的特徵 | CV RMSE | CV R² | Test RMSE | Test R² |
| --- | --- | --- | --- | --- | --- | --- |
| Exhaustive Search | 3 | R&D、Administration、Marketing | 9,266.78 | 0.9381 | 8,995.91 | 0.9001 |
| Forward SFS | 3 | R&D、Administration、Marketing | 9,266.78 | 0.9381 | 8,995.91 | 0.9001 |
| Lasso (L1) Top-k | 2 | R&D、Marketing | 9,186.68 | 0.9416 | 8,206.33 | 0.9168 |
| RFE | 3 | R&D、Administration、Marketing | 9,104.68 | 0.9399 | 8,995.91 | 0.9001 |
| Elastic Net Top-k | 3 | R&D、Marketing、Administration | **9,094.30** | 0.9424 | 8,995.91 | 0.9001 |

完整的 25 組結果見 `results/nested_cv/all_25_results.csv` 或網頁的表格。對照組（全部 5 個特徵、不做選擇）的 test RMSE 為 9,055.96。

**限制**：

- **資料很少**：50 筆資料、test 只有 10 筆，CV 差幾百美元都在雜訊範圍內。
- **CV 分數評估的是整個選擇程序**：各 outer fold 選到的子集可能不同，所以最終子集一樣的方法，CV RMSE 也會不同。
- **RFE 與 RFECV**：RFE 固定 k；RFECV 會自己用 CV 決定 k，只列為參考，它選的是 k=3。
- **Lasso／Elastic Net 的 Top-k**：只拿係數大小排序，再用 OLS 重新擬合；係數被壓成 0 的特徵之間是平手，依欄位順序決定。

## 資料夾結構

```text
week06/
├── index.html                  # 互動式網頁入口（GitHub Pages: /week06/）
├── assets/
│   ├── style.css               # 版面與亮色／暗色配色
│   ├── core.js                 # 純計算函式（預測值、95% 預測區間、最佳 k、格式化）
│   ├── app.js                  # 互動、表格與 Chart.js 圖表
│   ├── model_data.js           # 網頁資料（由 nested_cv_comparison.py 產生，勿手改）
│   └── model_data.json         # 同內容，供測試使用
├── analysis/
│   ├── common.py               # 共用：路徑、資料前處理、80/20 切分
│   ├── full_model.py           # 全部 5 個特徵的 OLS（對照組）
│   ├── selection_paths.py      # 五種選擇方法的 k = 1～5 路徑（一般 5-fold CV，探索用）
│   └── nested_cv_comparison.py # 本次 DIC-02 主分析：巢狀 CV 比較，並產生網頁資料
├── data/
│   └── 50_Startups.csv         # Kaggle 50 Startups（50 列 × 5 欄）
├── results/
│   ├── full_model/             # predictions.csv、actual_vs_predicted.png、residuals.png
│   ├── selection_paths/        # all_schemes_progression.csv 與各方法的圖
│   └── nested_cv/              # all_25_results.csv、best_models_summary.csv、cv_rmse_r2_comparison.png
├── tests/
│   └── core.test.js            # 核對 JS 的預測與預測區間是否與 Python 一致
├── doc/spec/SPEC.md            # DIC-2 網站規格（依老師成果整理）
├── requirements.txt            # 固定版本的 Python 套件
└── README.md
```

## 重新執行

以下指令都在 **repo 根目錄** 執行（Python 3.11）：

```bash
python -m venv .venv-week06
.venv-week06/Scripts/python -m pip install -r week06/requirements.txt   # macOS/Linux: .venv-week06/bin/python

.venv-week06/Scripts/python week06/analysis/full_model.py              # 對照組
.venv-week06/Scripts/python week06/analysis/selection_paths.py         # 選擇路徑（探索）
.venv-week06/Scripts/python week06/analysis/nested_cv_comparison.py    # 主分析，約 10 秒；更新 assets/model_data.js

node --test week06/tests/core.test.js                                  # 前端計算測試（Node 18+）
```

查看網頁時，用本機伺服器開啟，與 GitHub Pages 的環境相同：

```bash
python -m http.server 8000 --directory week06
```

然後開啟 <http://127.0.0.1:8000/>。網址可以帶參數直接開到特定畫面，例如 `?scheme=RFE&k=2`、`?scheme=all`。圖表的 Chart.js 從 CDN 載入，需要網路。

`random_state` 全部固定為 42：同一組套件版本下重跑，所有 CSV 與 `model_data.json` 會逐位元相同。
