# HW2 — King County 房價多元線性回歸

以 Kaggle「House Sales in King County, USA」資料集，依 CRISP-DM 六階段完成多元線性回歸分析：特徵選擇比較、以房屋分組的交叉驗證選模、一次性的 Test 評估、逐筆 95% 預測區間，並以離線可用的靜態 dashboard 呈現結果。

> 本 README 目前只涵蓋資料階段與重跑方式；目的、流程、成果與 dashboard 連結等完整內容會在後續步驟補齊。

## 資料來源與授權

- 資料集：[House Sales in King County, USA](https://www.kaggle.com/datasets/harlfoxem/housesalesprediction)（Kaggle `harlfoxem/housesalesprediction`），授權 CC0: Public Domain。
- 檔案：`data/kc_house_data.csv`（21,613 列 × 21 欄），sha256 `d0875baa0251b21d4bdc9d2ae940a4fe0bb6009824f23dd0e2a5b2bf04557b7e`；載入時先核對 sha256，不符即停止。

## 重跑步驟（Windows，Python 3.11）

在 `home_work_02/` 目錄執行：

```bash
py -3.11 -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
.venv/Scripts/python -m hw2.run_notebook      # 非互動執行 hw2.ipynb，寫出 results/ 與 assets/model_data.js
.venv/Scripts/python -m pytest                # Python 測試（含以 synthetic fixture 執行的 Node 一致性測試）
.venv/Scripts/python -m hw2.offline_scan      # dashboard 外部資源靜態掃描
node --test tests/js/core.test.js             # dashboard 計算的 Node 測試（前處理案例；fixture 部分由 pytest 執行）
```

四種特徵選擇方法各自的路徑計算時間（5 個 fold＋整個 training set 的選擇，以及 k = 1…18 的 CV 與全訓練集擬合）每次重跑都會量測，寫在 `model_data` 的 `meta.timing_s`（`path_<方法>`）與 `meta.path_timing_s`，notebook 第 4.2 節也會列出；本 README 不抄寫數字。

Test 區塊與實際 vs 預測圖在正式 Test 評估執行之前沒有資料。要檢視它們的行為或量測繪圖效能，可以在單元目錄**以外**產生一份使用 synthetic fixture 的 dashboard 複本（不是正式結果，頁面頂端會顯示警告）：

```bash
.venv/Scripts/python -m hw2.fixture <單元以外的輸出目錄>
```

macOS／Linux 把 `.venv/Scripts/python` 換成 `.venv/bin/python`。Dashboard 直接以瀏覽器開啟 `index.html`（`file://` 即可，不需要伺服器或網路）。

## 本機、不進 git 的設定與材料

以下路徑都列在 `home_work_02/.gitignore`，不得加入版本控制：

| 路徑 | 內容 |
| --- | --- |
| `.local/packaging.json` | 打包設定：`{"student_id": "<學號>"}`，填入實際學號。只有打包步驟讀取它；任何追蹤檔案一律寫 `<學號>` |
| `acceptor_materials/` | ChatGPT 對話 PDF、NotebookLM 原始輸出與來源清單 |
| `dist/` | 打包輸出（`<學號>_hw2.ipynb`、`<學號>_hw2.zip`、報告 PDF） |
| `.venv/` | 虛擬環境 |

## 檔案配置（目前）

| 路徑 | 說明 |
| --- | --- |
| `hw2.ipynb` | 主程式（CRISP-DM 六章；唯一的數字來源） |
| `hw2/` | 分析套件：資料、前處理、分割、四種特徵選擇方法的 k 路徑（`selection`）、OLS 與預測區間、模型候選與 CV winner、Test 評估守門、`model_data` 契約與匯出、synthetic fixture、離線掃描 |
| `tests/` | pytest；`tests/js/` 是 dashboard 計算的 Node 測試 |
| `data/kc_house_data.csv` | 資料檔 |
| `results/model_data.json`、`assets/model_data.js` | 匯出的 `model_data`（同一物件；`.js` 供 `file://` 載入） |
| `results/split/split_assignment.csv` | 每筆交易屬於 training 或 Test 與其 fold（只有識別，沒有特徵或價格） |
| `index.html`、`assets/` | Dashboard；`assets/hw2core.js` 是 dashboard 自己的前處理與預測計算，`assets/app.js` 是頁面；Chart.js 4.4.1 打包在 `assets/vendor/`（MIT，授權檔同目錄） |
