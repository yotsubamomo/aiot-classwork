# HW2 — King County 房價多元線性回歸

以 Kaggle「House Sales in King County, USA」資料集，依 CRISP-DM 六階段完成多元線性回歸分析：特徵選擇比較、以房屋分組的交叉驗證選模、只評估一次的保留 Test 集、逐筆 95% 預測區間，並以離線可用的靜態 dashboard 呈現結果。

## 目的

- 以房屋的條件（面積、房間數、建築等級、屋齡與整修、位置、交易日期）預測成交價格，並為每一筆預測給出有統計定義的 95% 預測區間。
- 依作業要求執行特徵選擇：比較四種能對每個 k 給出子集的方法（Forward SFS、Backward SFS、RFE、Lasso 路徑排序，k = 1…18；方法取自作業頁「補充」段建議清單的一部分）與單一的 All-in baseline，只用 training set 的交叉驗證選模。
- 交付老師要求的主程式、PDF 報告、AI 協助證據與學號 ZIP，加上課堂口頭要求的互動 dashboard。

## 資料來源與授權

- 資料集：[House Sales in King County, USA](https://www.kaggle.com/datasets/harlfoxem/housesalesprediction)（Kaggle `harlfoxem/housesalesprediction`），授權 CC0: Public Domain。
- 檔案：`data/kc_house_data.csv`（21,613 列 × 21 欄），sha256 `d0875baa0251b21d4bdc9d2ae940a4fe0bb6009824f23dd0e2a5b2bf04557b7e`；載入時先核對 sha256，不符即停止。

## 流程（CRISP-DM）

主程式 `hw2.ipynb` 依序是六章，每一章呼叫 `hw2/` 套件的公開函式：

1. **Business Understanding**：預測目標、使用者與成功的衡量。
2. **Data Understanding**：結構核對（sha256、欄位、列數、唯一 `id`、`sqft` 恆等式）；分布與極端值只用 training set 檢視，異常值不刪除。
3. **Data Preparation**：固定轉換（交易日期 → 天數、整修年 → 旗標＋有效年份、zipcode 為類別）；以房屋 `id` 分組的 80/20 切分與 training 內的 5 個分組 fold；需要 fit 的前處理只看當次訓練列；以 ln(price) 建模、USD 報告。
4. **Modeling**：四種特徵選擇方法在每個 fold 的訓練列上重新選出 k = 1…18 的子集（fold 內選擇），All-in baseline；Ridge／Lasso 對照（依老師補充建議，metric-only）；講義的 p-value backward 對照。
5. **Evaluation**：各方法與整體 CV winner；全部選擇固定後，保留 Test 集只評估一次（各方法 CV winner、All-in、整體 CV winner，加上 Ridge／Lasso 各一次）；逐筆 95% 預測區間與經驗涵蓋率；Adjusted R² 與五大回歸假設診斷（依老師補充建議，只用 training set）。
6. **Deployment**：dashboard；`predict_price()` 預測新樣本；模型解釋（係數的百分比讀法、標準化與 one-hot 的讀法、permutation importance）；pickle 示範；使用限制。

## 成果

數字取自匯出結果 `results/model_data.json`（`tests/test_report.py` 核對本節的每個數字與匯出結果一致）；完整的表與圖見報告與 `results/`。

- **整體 CV winner（最終模型）**：Lasso 路徑排序 k = 17（canonical subset 與 Forward SFS k = 17、Backward SFS k = 17 相同，是同一個模型）。
- **保留 Test 集**（4,323 筆，只評估一次）：RMSE 183,370 USD、MAE 78,100 USD、R² 0.783（USD 尺度）。
- **95% 預測區間的經驗涵蓋率**：94.45%（4,083／4,323）。
- 五大回歸假設在 training 殘差上都偵測到偏離，依規則揭露、不判定失敗；所以不宣稱保證 95% 的涵蓋率。

報告（PDF）由 `python -m hw2.report` 建置，數字、表與圖全部在建置時從匯出結果注入。

## Dashboard

- GitHub Pages：<https://yotsubamomo.github.io/aiot-classwork/home_work_02/>（發布自 `main`；合併進 `main` 後才會更新）
- 本機或繳交 ZIP：直接以瀏覽器開啟 `index.html`（`file://`），不需要網路或伺服器；Chart.js 打包在 `assets/vendor/`，頁面不發出任何對外請求。
- Dashboard 只讀取匯出的結果：任意 (方法, k) 顯示訓練 CV 指標與即時預測，Test 區塊只呈現被授權評估的模型，任何操作都不會觸發新的 Test 評估。

## 重跑步驟（Windows，Python 3.11）

在 `home_work_02/` 目錄執行：

```bash
py -3.11 -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
.venv/Scripts/python -m hw2.run_notebook      # 非互動執行 hw2.ipynb，重現唯一一次的 Test 評估，寫出 results/ 與 assets/model_data.js
.venv/Scripts/python -m pytest                # Python 測試（含以 synthetic fixture 執行的 Node 一致性測試）
.venv/Scripts/python -m hw2.offline_scan      # dashboard 外部資源靜態掃描
node --test tests/js/core.test.js             # dashboard 計算的 Node 測試
.venv/Scripts/python -m hw2.report            # 建置報告：dist/report/hw2_report.md、.html、.pdf
.venv/Scripts/python -m hw2.package           # 打包：dist/<學號>_hw2.ipynb、dist/<學號>_hw2.zip（需要學號設定與 AI 證據材料）
```

- **報告建置**需要 Node.js 與 Chrome 或 Edge（擷取 dashboard 截圖、列印 PDF；找不到瀏覽器時以環境變數 `HW2_BROWSER` 指定執行檔）。`--no-pdf` 只產生 Markdown 與 HTML；`--final` 在 AI 證據章節仍是【待填】時失敗。建置前會核對匯出的 Test 結果就是唯一一次正式評估的結果，不符就拒絕建置。AI 證據章節（「GPT 輔助內容」的 ChatGPT 部分、「NotebookLM 摘要」、附錄 B 的 ChatGPT 對話 PDF）在建置時讀取本機的 `acceptor_materials/`：材料的 sha256 必須與收件紀錄相同，否則拒絕建置；NotebookLM 摘要必須至少 100 個漢字，且每一句都在對照表中；PDF 版本把 ChatGPT 對話 PDF 的原頁接在報告最後。材料不存在時只有對應章節以【待填】標示，其他章節照常建置。
- **Test 評估只有一次**：唯一一次正式 Test 評估在 notebook 第 5.4 節、全部選擇（各方法 CV winner、整體 CV winner、Ridge／Lasso 的 alpha）只用 training set 固定之後執行，執行識別 `fe76019b9af84b1e8ff46095d5ac0fb2`、Test 結果摘要（`test_inputs` 與 `test` 的 sha256）`b53ff286ae0734add8b272089aba904a1cb7f5aca444a62d356420b25dc3cfc6`；權威紀錄在 `doc/governance/worklog/issue-63.md` §5。`model_data` 的 `meta.test_evaluation` 只記錄**產生目前這份檔案的那次執行**；完整重跑 notebook 是以相同的 seed 與鎖定版本**重現**同一個評估，不是新的評估，結果必須與上述摘要完全相同（bit-exact），不一致時不得採用新數字。同一次執行內第二次評估會被拒絕。
- 四種方法的路徑計算時間每次重跑都會量測，寫在 `model_data` 的 `meta.timing_s`（`path_<方法>`）與 `meta.path_timing_s`，notebook 第 4.2 節與報告也會列出；Ridge／Lasso、p-value backward 與 Test 評估的時間在 `meta.timing_s` 與 `meta.comparison_timing_s`。
- 要在單元目錄**以外**產生一份使用 synthetic fixture 的 dashboard 複本（例如量測繪圖效能；不是正式結果，頁面頂端會顯示警告）：`.venv/Scripts/python -m hw2.fixture <單元以外的輸出目錄>`。
- macOS／Linux 把 `.venv/Scripts/python` 換成 `.venv/bin/python`。

### 學號設定（打包用）

繳交檔名 `<學號>_hw2.ipynb`、`<學號>_hw2.zip` 的學號只從本機、不進 git 的 `.local/packaging.json` 讀取，內容是 `{"student_id": "<學號>"}`（填入實際學號）。任何追蹤的檔案一律寫 `<學號>`。

`python -m hw2.package` 在寫出任何檔案之前先核對：打包的追蹤檔案都已 commit；`hw2.ipynb` 是一次完整執行的結果（code cell 的執行序號依序是 1…N、沒有錯誤輸出，Test 評估那一格印出的執行識別等於 `model_data` 的 manifest），而且匯出的 Test 結果就是唯一一次正式評估；報告以 `--final` 重新建置（AI 證據章節不得是【待填】，依材料整理的章節必須是審查過的版本）。之後把 `hw2.ipynb` 原樣複製為 `dist/<學號>_hw2.ipynb`，並寫出 `dist/<學號>_hw2.zip`：ZIP 內有一個資料夾 `<學號>_hw2/`，含主程式 `<學號>_hw2.ipynb`、報告 `hw2_report.pdf`、ChatGPT 對話 PDF、`hw2/`、`requirements.txt`、`data/kc_house_data.csv`、`README.md`、`results/` 與 dashboard（`index.html`、`assets/`）。ZIP 寫出後逐一讀回核對 sha256；檔案清單與 sha256 寫在 `dist/hw2_package_manifest.json`（名稱以 `<學號>` 表示）。解壓後直接開啟 `<學號>_hw2/index.html` 即可離線使用 dashboard。

## 本機、不進 git 的設定與材料

以下路徑都列在 `home_work_02/.gitignore`，不得加入版本控制：

| 路徑 | 內容 |
| --- | --- |
| `.local/packaging.json` | 打包設定（學號，見上節）。只有打包步驟讀取它 |
| `acceptor_materials/` | ChatGPT 對話 PDF、NotebookLM 原始輸出與來源清單（作者提供）；`derived/` 是 Claude Code 依這些材料整理的報告章節與 NotebookLM 摘要的對照表，同樣不進 git |
| `dist/` | 建置與打包輸出（`dist/report/` 的報告；`<學號>_hw2.ipynb`、`<學號>_hw2.zip`） |
| `.venv/` | 虛擬環境 |

## 檔案配置

| 路徑 | 說明 |
| --- | --- |
| `hw2.ipynb` | 主程式（CRISP-DM 六章；唯一的數字來源） |
| `hw2/` | 分析套件：資料、前處理、分割、四種特徵選擇方法的 k 路徑（`selection`）、OLS 與預測區間、模型候選與 CV winner、Ridge／Lasso 對照與講義的 p-value backward（`comparison`）、Test 評估守門、`model_data` 契約與匯出、最終模型與 `predict_price()`（`deployment`）、五大假設診斷（`diagnostics`）、模型解釋（`explain`）、預測圖（`prediction_plot`）、報告建置（`report`）、打包（`package`）、synthetic fixture、離線掃描 |
| `report/` | 報告來源：`report.md`（zh-TW Markdown；數字以佔位符在建置時注入）、`external_sources.json`（主流解法比較的公開來源與其自報數字）、`chrome_capture.js`（建置時擷取 dashboard 截圖與列印 PDF） |
| `tests/` | pytest；`tests/js/` 是 dashboard 計算的 Node 測試 |
| `data/kc_house_data.csv` | 資料檔 |
| `results/model_data.json`、`assets/model_data.js` | 匯出的 `model_data`（同一物件；`.js` 供 `file://` 載入） |
| `results/split/split_assignment.csv` | 每筆交易屬於 training 或 Test 與其 fold（只有識別，沒有特徵或價格） |
| `results/tables/` | 結果表 CSV：`cv_by_method_k.csv`（各方法各 k 的訓練 CV）、`comparison.csv`（各方法 CV winner、All-in、Ridge、Lasso 與 p-value 對照；`cv_*` 為訓練 CV、`test_*` 為 Test 評估，分欄）、`alpha_cv.csv`（Ridge／Lasso 的 alpha 交叉驗證曲線）；最終模型（只用 training set）的 `diagnostics_summary.csv`、`diagnostics_vif_by_group.csv`、`diagnostics_vif_by_column.csv`、`final_model_coefficients.csv`、`permutation_importance_training.csv` |
| `results/figures/` | 實際 vs 預測＋逐筆 95% 預測區間的預測圖（notebook 5.5.1，只讀匯出的 Test 結果）、診斷圖與解釋圖（notebook 5.6 與第 6 章）PNG；報告引用 |
| `results/deployment/final_model.pkl` | 最終模型的 pipeline（Deployment 的 pickle 示範；dashboard 不讀取它）。pickle 載入時會執行程式碼，只載入本專案 notebook 產生的檔案 |
| `index.html`、`assets/` | Dashboard；`assets/hw2core.js` 是 dashboard 自己的前處理與預測計算，`assets/app.js` 是頁面；Chart.js 4.4.1 打包在 `assets/vendor/`（MIT，授權檔同目錄） |
| `doc/` | 需求（老師原文，唯讀）、Brief、Spec、票務索引、驗收清單 `doc/acceptance/ACCEPTANCE.md` 與治理紀錄 |
