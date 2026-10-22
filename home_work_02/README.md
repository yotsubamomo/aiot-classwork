# HW2 — King County 房價多元線性回歸

## 專案資料

- **課程名稱**：AIoT 與數據分析（AIoT & Data Analytics, AIoT-DA）
- **作業**：HW2 Multiple Linear Regression（多元線性回歸，依 CRISP-DM 完成分析）
- **完成日期**：2026-10-19（合併進 `main`，PR #68）
- **儲存庫網址**：[github.com/yotsubamomo/aiot-classwork](https://github.com/yotsubamomo/aiot-classwork)（本作業在 `home_work_02/`）
- **Dashboard（GitHub Pages）**：<https://yotsubamomo.github.io/aiot-classwork/home_work_02/>

## Dashboard（課堂口頭要求）

[![Dashboard 的保留 Test 集評估區塊：Test 指標、實際 vs 預測與逐筆 95% 預測區間](./doc/screenshots/dashboard-test.png)](https://yotsubamomo.github.io/aiot-classwork/home_work_02/)

> 點擊圖片可開啟 GitHub Pages 上的 dashboard。截圖是 King County（正式分析）檢視，以報告建置所用的擷取程式 `report/chrome_capture.js`，在本機以 Chrome 從本單元的 `index.html` 擷取；這個檢視只讀取追蹤的匯出結果，所以內容與 Pages 上相同。畫面中的繪製與互動時間是擷取當下的量測。

![Dashboard 的模型選擇與訓練 CV 區塊：方法與 k 切換、CV 指標與指標 vs k 圖](./doc/screenshots/dashboard-model.png)

- GitHub Pages：<https://yotsubamomo.github.io/aiot-classwork/home_work_02/>（發布自 `main`）
- 本機或繳交 ZIP：直接以瀏覽器開啟 `index.html`（`file://`），不需要網路或伺服器；Chart.js 與 50 Startups 範例資料都打包在 `assets/`。
- 網路請求：頁面載入、King County 與 50 Startups 的所有操作、以本機檔案載入自訂資料集，都不發出任何對外請求。唯一的對外請求是使用者在「自訂資料集」貼上 URL 並按「載入 URL」之後，對該 URL 的一次 GET（不帶 cookie 等憑證、不跟隨重新導向、不重試）。
- 頁面頂端的「分析問題（Problem）」下拉切換 King County（正式分析）、50 Startups 與自訂資料集（探索模式，見「探索模式（加分功能）」）。
- King County 檢視只讀取匯出的結果：任意 (方法, k) 顯示訓練 CV 指標與即時預測，Test 區塊只呈現被授權評估的模型，任何操作都不會觸發新的 Test 評估。探索模式在瀏覽器內計算，不讀取也不改寫 `model_data`，它的「探索 test」不是 Test 評估。
- Dashboard 原是老師的課堂口頭要求（舊版作業頁正文沒有要求網站）；2026-10-21 更新的作業頁把主要繳交改為「跟 DIC2 一樣github and web」，所以 GitHub repository 與 Pages 上的 dashboard 現在是主要交付。它不取代任何正文要求的檔案。

## 專案摘要

以 Kaggle「House Sales in King County, USA」資料集，依 CRISP-DM 六階段完成多元線性回歸分析：特徵選擇比較、以房屋分組的交叉驗證選模、只評估一次的保留 Test 集、逐筆 95% 預測區間，並以離線可用的靜態 dashboard 呈現結果。

依 2026-10-21 更新的作業頁的兩項加分，dashboard 另有 problem 下拉與「探索模式」：老師範例的 50 Startups 與使用者輸入的任意 CSV 資料集，在瀏覽器內以同一套特徵選擇與評估方法分析（探索執行，非正式評估；見「探索模式（加分功能）」）。

一份 notebook、三個呈現：

- **主程式** [`hw2.ipynb`](hw2.ipynb)：CRISP-DM 六章，呼叫 [`hw2/`](hw2/) 套件；是所有數字的唯一來源，結果匯出到 [`results/`](results/)。
- **PDF 報告**：由 [`report/report.md`](report/report.md) 建置，數字、表與圖在建置時從匯出結果注入。
- **Dashboard**：[`index.html`](index.html)＋[`assets/`](assets/)。King County 檢視只讀取匯出的 `model_data`；探索模式在瀏覽器內計算，不讀取 `model_data`。

## 目的

- 以房屋的條件（面積、房間數、建築等級、屋齡與整修、位置、交易日期）預測成交價格，並為每一筆預測給出有統計定義的 95% 預測區間。
- 依作業要求執行特徵選擇：比較四種能對每個 k 給出子集的方法（Forward SFS、Backward SFS、RFE、Lasso 路徑排序，k = 1…18；方法取自作業頁「補充」段建議清單的一部分）與單一的 All-in baseline，只用 training set 的交叉驗證選模。
- 交付老師要求的主程式、PDF 報告、AI 協助證據與學號 ZIP，加上課堂口頭要求的互動 dashboard（新版作業頁把 GitHub 與 web 列為主要繳交）。
- 依新版作業頁的兩項加分，讓 dashboard 以下拉呈現兩種 problem，並接受任意輸入的 CSV 資料集，在瀏覽器內完成多元線性回歸的特徵選擇與評估（探索執行，非正式評估）。

## 已實作功能

標示沿用報告的三種標示：〔老師要求〕、〔依老師補充建議〕、〔專案延伸〕；dashboard 是課堂口頭要求。

**分析（notebook＋`hw2/` 套件）**

- 〔老師要求〕CRISP-DM 六章依序執行。
- 〔專案延伸〕載入時核對資料檔的 sha256，不符即停止（本專案的決定，不是作業頁的要求）。
- 〔老師要求〕四種特徵選擇方法對每個 k 給出子集，與 All-in baseline 一起以訓練 CV 選模；方法清單取自補充段建議清單的一部分。
- 〔專案延伸〕以房屋 `id` 分組的切分與交叉驗證、fold 內選擇（每個 fold 只在自己的訓練列上重新選擇）、只評估一次的 Test 協定；以 ln(price) 建模、以 USD 報告。
- 〔老師要求〕實際 vs 預測圖加上逐筆 95% 預測區間；〔專案延伸〕預測區間的經驗涵蓋率驗證。
- 〔依老師補充建議〕Adjusted R²（只對 OLS 子集模型、log 尺度）、五大回歸假設診斷（只用 training set）、Deployment 的預測新樣本（`predict_price()`）與模型解釋、Ridge／Lasso 對照（metric-only）。
- 〔專案延伸〕講義的 p-value backward elimination 對照、permutation importance（只用於解釋）、各方法計算時間的量測、最終模型的 pickle 示範。

**Dashboard（課堂口頭要求）**

- 概覽、模型選擇與訓練 CV、指標 vs k（可比較全部方法）、即時房價預測、保留 Test 集評估、方法與限制。
- 任意 (方法, k) 的 KPI 與係數表使用訓練 CV 與全訓練集擬合，標示「訓練 CV」；Test 區塊標示展示的方法與 k，與目前選取的模型不同時有提示。
- 預測器的輸入檢查與警告（含未見 zipcode）；實際 vs 預測圖可縮放、拖曳、逐筆讀取。
- 完全離線：`file://` 開啟；頁面載入、King County 與 50 Startups 的操作零對外請求，Chart.js 打包在單元內（自訂資料集的 URL 讀取是唯一的對外請求，見上方「網路請求」）。

**探索模式（加分功能）**

- 〔老師要求（新版作業頁的加分）〕下拉呈現兩種 problem：「分析問題（Problem）」下拉有 King County 房價（正式分析）、50 Startups 利潤（探索）與自訂資料集（探索）三項。「兩種 problem＝同一頁以下拉切換兩個資料集」是本專案對老師原文的解讀，老師原文沒有進一步定義。
- 〔老師要求（新版作業頁的加分）〕任意輸入 Dataset：自訂資料集可貼 CSV 的 URL 或選本機 CSV 檔案；預測目標欄預設最後一欄、可改。
- 〔專案延伸〕探索模式的分析能力是本專案的決定，不是老師的要求：逐列切分、只用訓練列的交叉驗證、Forward SFS／Backward SFS／RFE／Lasso 路徑排序與 All-in baseline、各方法與整體 CV winner、只對 winner 計算的探索 test、逐筆預測區間的實際 vs 預測圖、即時預測器、共線診斷、運算預算、進度與取消。
- 〔專案延伸〕老師的範例資料 `50_Startups.csv` 打包在 `assets/data/`，離線與 ZIP 內都能用。

**報告與交付**

- PDF 報告：CRISP-DM 六章、資料來源與研究脈絡、「GPT 輔助內容」、「NotebookLM 摘要」、主流或更優解法比較、dashboard 連結與截圖、附錄 ChatGPT 對話 PDF；前段附三種標示的對照表。
- 繳交檔名 `<學號>_hw2.ipynb`、`<學號>_hw2.zip` 由打包步驟自同一份 notebook 產生。

## 作業要求對應

下表以 2026-10-21 更新的作業頁正文（[`doc/requirement/HW2-req_new-20261021.txt`](doc/requirement/HW2-req_new-20261021.txt)）為準；新版沒有寫、舊版正文有的條目標「新版未載明」，不推定老師已刪除，照原樣交付。

| 作業頁正文的要求 | 本專案 |
| --- | --- |
| 資料來源：Kaggle 公開資料集，>13 個特徵，標示來源與連結 | King County 房屋銷售資料（19 個 source features），見「資料來源與授權」；舊版正文寫 10 至 20 個特徵，報告第一章說明當時與補充段條件的交集 |
| 加分：有下拉視窗呈現兩種 problem | **操作**：開啟 dashboard，在頁面頂端「分析問題（Problem）」下拉選 King County 房價（正式分析）或 50 Startups 利潤（探索）；50 Startups 選取即執行，離線可用。**驗收**：[`ACCEPTANCE.md`](doc/acceptance/ACCEPTANCE.md) G 節 V2-1、V2-2、V2-10、V2-37 |
| 加分：可任意輸入 Dataset（老師的例子是一個 CSV 的 URL） | **操作**：下拉選「自訂資料集（探索）」，在「CSV 的 URL」貼網址並按「載入 URL」，或在「本機 CSV 檔案」選檔；「預測目標欄」預設最後一欄、可改。**驗收**：G 節 V2-18～V2-22、V2-37；GitHub Pages 上的檢查在合併進 `main` 之後進行（V2-42） |
| 分析任務：線性回歸預測，必做特徵選擇與模型評估 | [`hw2.ipynb`](hw2.ipynb) 第 4、5 章；[`hw2/selection.py`](hw2/selection.py)（特徵選擇路徑）、[`hw2/models.py`](hw2/models.py)（分組 CV 與 CV winner）、[`hw2/testgate.py`](hw2/testgate.py)（Test 評估守門） |
| 預測圖加上信賴區間或預測區間 | 逐筆 95% 預測區間：notebook 5.5.1 與 [`results/figures/`](results/figures/)；dashboard 的 Test 區塊 |
| CRISP-DM 流程說明（六階段） | notebook 與報告各有六章，見「流程（CRISP-DM）」 |
| AI 協助要求：ChatGPT 對話 PDF、NotebookLM 摘要（100 字以上）、標示「GPT 輔助內容」與「NotebookLM 摘要」 | 報告的對應兩節與附錄；作者的原始材料只在本機，不進 git |
| 繳交內容：主要繳交「跟 DIC2 一樣github and web」；optional：對話內容、資訊圖表、報告書 | GitHub repository（本單元 `home_work_02/`）與 GitHub Pages 上的 dashboard；另照舊版正文交付 `<學號>_hw2.ipynb`、報告 PDF（含 ChatGPT 對話 PDF）與 `<學號>_hw2.zip`，由作者在本機打包 |
| 報告內容：網路上主流或更優解法之比較與說明（新版未載明） | 〔老師要求〕報告第 8 章「主流或更優解法比較」：使用同一份資料的公開解法、各來源自報的數字與不可比之處，以及與本專案的比較；來源與數字記在 [`report/external_sources.json`](report/external_sources.json) |
| （optional）上傳 GitHub 時提供連結，並在 README 整理流程與成果（新版未載明；新版的主要繳交即 GitHub） | 本檔 |
| 評分：Kaggle 名次（若有）／預測結果評估（新版未載明） | King County 沒有競賽名次，以 Test 評估指標與預測圖呈現，見「成果」 |

- 〔依老師補充建議〕採用的補充建議：Adjusted R²、五大回歸假設診斷、Deployment 的預測新樣本與模型解釋、Ridge／Lasso 對照。它們不是作業頁正文的要求。
- 互動 dashboard 是課堂口頭要求，見「Dashboard（課堂口頭要求）」；新版作業頁把 GitHub 與 web 列為主要繳交。
- 兩項加分的「兩種 problem＝同一頁以下拉切換兩個資料集」是本專案的解讀；探索模式的分析方法是本專案的決定（〔專案延伸〕），見「探索模式（加分功能）」。
- 每條要求與決定的檢查與證據逐條列在驗收清單 [`doc/acceptance/ACCEPTANCE.md`](doc/acceptance/ACCEPTANCE.md)。

## 資料來源與授權

- 資料集：[House Sales in King County, USA](https://www.kaggle.com/datasets/harlfoxem/housesalesprediction)（Kaggle `harlfoxem/housesalesprediction`），授權 CC0: Public Domain。
- 檔案：`data/kc_house_data.csv`（21,613 列 × 21 欄），sha256 `d0875baa0251b21d4bdc9d2ae940a4fe0bb6009824f23dd0e2a5b2bf04557b7e`；載入時先核對 sha256，不符即停止。
- 探索模式的 50 Startups（老師在新版作業頁給的範例資料）：<https://raw.githubusercontent.com/Avik-Jain/100-Days-Of-ML-Code/master/datasets/50_Startups.csv>，取自 GitHub repository `Avik-Jain/100-Days-Of-ML-Code`；該 repository 以 **MIT License** 發布（授權聲明原文在 [`assets/data/50_Startups.LICENSE.md`](assets/data/50_Startups.LICENSE.md)）。逐位元複製為 `assets/data/50_Startups.csv`（50 列、5 欄：`R&D Spend`、`Administration`、`Marketing Spend`、`State`、`Profit`），sha256 `c6075ca5a7551243b31193bad9228f0a1b9468cdde2475c6586c56dcfac5630d`；來源 commit、取得日期與核對方式在 [`assets/data/50_Startups.SOURCE.md`](assets/data/50_Startups.SOURCE.md)。同一文字另內嵌為 `assets/data/startups50.js`，因為 `file://` 開啟的頁面不能以網路 API 讀取本機檔案。這份資料只是示範 problem，不宣稱符合作業的 >13 特徵條件，也不陳述資料的原始出處。

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

## 探索模式（加分功能）

〔老師要求（新版作業頁的加分）〕新版作業頁公告兩項加分：「有下拉視窗呈現兩種problem」與「可任意輸入 Dataset」（老師的例子是 50_Startups.csv 的 URL）。老師沒有進一步定義「兩種 problem」；本專案的解讀是同一個 dashboard 以下拉切換兩個資料集／問題。下列分析方法、評估方式與限制是本專案的決定〔專案延伸〕，不是老師的要求。探索結果的數字不寫進本檔或報告：它們每次在瀏覽器內重新計算。

### 操作方式

1. 開啟 dashboard（GitHub Pages，或 ZIP 內的 `index.html`）。頁面頂端「分析問題（Problem）」下拉有三項：King County 房價（正式分析）、50 Startups 利潤（探索）、自訂資料集（探索）。預設是 King County，內容就是正式分析的 dashboard。
2. 選「50 Startups 利潤（探索）」：以打包在單元內的老師範例資料立即執行，不需要輸入，離線也能用。
3. 選「自訂資料集（探索）」：在「CSV 的 URL」貼網址並按「載入 URL」，或在「本機 CSV 檔案」選檔。「預測目標欄」預設最後一欄，可改選其他數值欄（以同一份資料重新執行，不重新讀取 URL）。URL 讀取失敗時，畫面寫出原因（網路或跨來源限制、HTTP 狀態、逾時、回應不是文字），並提示下載後改以本機檔案載入。
4. 結果依序是：資料與前處理（欄位型態、排除的欄與原因、刪除的缺值列、共線診斷）、模型選擇與訓練 CV（方法與 k、指標 vs k 圖、各方法與整體 CV winner 的比較表、Lasso 路徑）、即時預測、探索 test（實際 vs 預測與逐筆 95% 預測區間）、方法與限制。每個區塊標「探索執行，非正式評估」。
5. 執行中顯示進度與已耗時，可按「取消執行」。切回 King County 時，正式分析的區塊與數字不變。

### 分析方法

- **載入**：UTF-8、逗號分隔、第一列為欄名的 CSV。每個非空儲存格都能解析為有限數字的欄是數值欄，其他是類別欄；含缺值的列整列刪除並顯示筆數；目標必須是數值欄。載入階段只檢查 CSV 結構，不計算任何欄位的分布。
- **切分與前處理**：固定 seed 的逐列隨機切分（訓練與 test），訓練列再分成 fold 做交叉驗證。類別欄的層級數上限與常數欄的排除只用訓練列判定；每個 fold 的 one-hot 層級、基準與 Lasso 的標準化只從該 fold 的訓練列學；test 列在全部選擇固定之後才讀取，只用來評估 winner。
- **特徵選擇**：一個來源欄＝一個 feature group，整組進出。Forward／Backward SFS 以 RSS、RFE 以 group 對擬合值貢獻的標準差 sd(X_g β_g)、Lasso 路徑以 exact LARS 的進入順序，平手依 CSV 欄序；另有 All-in baseline。這些準則與 King County 正式分析相同。
- **候選與 winner**：每個 (方法, k) 候選只有一個狀態——`VALID`、`INVALID_MODEL`（任一 fold 或整個訓練集上設計矩陣秩不足或殘差自由度不足，或 Lasso 路徑停止後的 k）、`SKIPPED_RESOURCE_LIMIT`（超出運算預算，未執行）、`FAILED`（非預期的計算錯誤，只影響該方法）。各方法與整體 CV winner 只從 `VALID` 候選中以 CV RMSE 選出；全部候選都無效時整個執行拒絕，並顯示共線診斷（哪些欄位線性相依、對應哪些 feature group，不指認單一問題欄）。
- **評估**：指標 vs k 圖與 KPI 只用訓練 CV；探索 test 只對各方法與整體 CV winner 計算一次（MAE、MSE、RMSE、R²、逐筆 95% OLS 參數式預測區間與涵蓋率），不回饋任何選擇。即時預測器只對目前選取的 `VALID` 候選提供預測。
- **Lasso 路徑的停止**：路徑結束時若仍有 group 未進入——active set 退化、路徑走到終點時其餘 group 與殘差的相關在數值上為零，或數值停止（alpha 回升、迭代達上限）——一律同樣處理：已求得的路徑段是實際結果；未進入的 group 只依 CSV 欄序列出作展示，不是實際路徑、也不構成選模依據；k 超過已進入 group 數的 Lasso 候選為 `INVALID_MODEL`（`lasso_path_degenerate`）。畫面寫出實際的停止原因，只陳述已確立的事實（例如「走到終點」不代表一定共線）。停止與平手的數值判定在「目標除以它在同一批列上的均方根」的尺度上計算，所以把目標換單位（乘上任何正常數）不改變進入順序、停止點與候選狀態；entry alpha 以目標的原始尺度回報。
- **數值驗證**：pytest 即時產生通用 Python 參照（[`hw2/explore_reference.py`](hw2/explore_reference.py)，只供測試，正式分析不使用它）的結果，Node 測試逐值比對瀏覽器端的引擎；同一份資料、同一目標欄與同一版本重跑，結果相同。

### 與正式分析的差異

| 項目 | King County（正式分析） | 探索模式（50 Startups、自訂資料集） |
| --- | --- | --- |
| 目標尺度 | 以 ln(price) 建模，預測與區間轉回 USD | 原始尺度建模與報告，不取 log |
| 切分 | 以房屋 `id` 分組的切分與分組 fold | 逐列隨機切分與逐列 fold，沒有分組欄 |
| Lasso 路徑沒有讓全部 group 進入時 | 未進入的 group 依欄序補成 k = 1…18 的子集（King County 的選模語義） | 停在已進入的 group；之後的 group 只作展示，k 超過的候選無效 |
| 派生規則 | 交易日期轉天數、整修年拆成旗標與有效年份、zipcode 為類別 | 沒有；一個來源欄就是一個 feature group |
| Test 的地位 | 唯一一次的正式 Test 評估，記錄在案 | 探索 test：每次執行都在瀏覽器內重算、不保存，永遠不是 Test 評估 |

### 限制與揭露

- **逐列切分可能洩漏**：資料中若有重複的列、同一個實體的多筆紀錄（例如同一家公司或同一個人的多次觀測），或時間相依的資料，同一來源的資訊可能同時出現在訓練與 test（或同一 fold 的訓練與驗證）列，使 CV 與 test 指標過度樂觀。探索結果只供操作與比較，**不代表正式研究結論**。
- **不是正式評估**：探索結果不保存（不寫入 localStorage、cookie、URL 參數或檔案）、不進報告數字，也不是 Test 評估；探索程式不讀取 `model_data`，King County 的數字不受影響。CV winner 的 CV 分數帶有樂觀的選擇偏誤。預測區間假設殘差常態、同質變異、彼此獨立，不保證 95% 的經驗涵蓋率。
- **運算預算**：Forward SFS、Backward SFS、RFE 與 Lasso 路徑在執行前依資料大小估計運算量；超過預算的方法整個標 `SKIPPED_RESOURCE_LIMIT`、不執行，其他方法照跑。All-in baseline 一律最先嘗試、不會被略過，但不保證任何資料都能在特定時間內完成。不承諾任何執行時間。
- **取消與改選的生效時點**：執行中按「取消執行」，或改選資料、目標欄或 problem 時，進行中的執行在目前的候選算完後（下一個候選邊界）才停止；全部候選完成之後（計算共線診斷與探索 test 時），則在進行中的步驟完成時停止。新的執行要等前一次停止後才開始（任何時刻只有一個執行）。取消後不顯示任何結果，只顯示「已取消」與已完成的方法數；再次執行從頭開始。切到 King County 時正式分析立即顯示，背景中的執行同樣在下一個邊界停止。在接近載入上限、類別層級多的資料上，單一候選（包括一律嘗試的 All-in）可能需要數分鐘；這段期間頁面仍可操作、進度與已耗時持續更新、King County 可用，但取消或新的執行要等這個候選算完。
- **沒有檔案大小上限**：載入上限只以列數與欄數判定。URL 的回應與本機檔案都整份讀入瀏覽器的記憶體；超過列數或欄數上限的輸入以 `TOO_LARGE` 拒絕、不截斷。極大的檔案可能無法讀取：接近瀏覽器能處理的文字大小（約 512 MiB）時，可能耗盡分頁的記憶體使分頁當掉，而不是顯示訊息；更大的檔案改以位元組逐段檢查，需要數秒，期間頁面不回應輸入。頁面偵測到瀏覽器無法處理這份輸入（例如解碼或配置記憶體失敗）時，畫面如實說明是大小或記憶體的限制，不會說成格式或編碼錯誤。
- **URL 讀取**：對方伺服器必須允許跨來源讀取（CORS），例如 GitHub 上的檔案要用 Raw 連結；需要登入、會重新導向或不允許跨來源的網址會失敗，此時請下載後以本機檔案載入。

### 載入上限與運算預算（實作常數）

| 項目 | 值 | 定義位置 |
| --- | --- | --- |
| 載入上限 | 50,000 列 × 60 欄（超過以 `TOO_LARGE` 拒絕，不截斷）；刪除缺值列後至少 20 列 | `assets/explore_load.js` 的 `LIMITS` |
| 類別欄的層級數上限 | 20（以訓練列計算；超過的欄排除並列出） | `assets/explore_engine.js` 的 `MAX_LEVELS` |
| 運算預算（量度＝預估 OLS 求解次數 × 訓練列數 × 編碼欄數²） | Forward SFS、Backward SFS、RFE 各 `2e11`；Lasso 路徑 `8e10`；All-in 沒有預算 | `assets/explore_engine.js` 的 `BUDGETS`（與 `hw2/explore_reference.py` 相同） |
| 切分 | seed 42；test 占 20%；訓練列 5 fold | `SEED`、`TEST_FRACTION`、`N_FOLDS` |
| 預測區間 | 95% | `PI_LEVEL` |
| URL 讀取逾時 | 20 秒 | `assets/explore_load.js` 的 `URL_TIMEOUT_MS` |

數字由實測決定，不是效能承諾；量測的方法、資料與結果記在驗收清單 [`doc/acceptance/ACCEPTANCE.md`](doc/acceptance/ACCEPTANCE.md) G 節（V2-27、V2-30、V2-32、V2-40）。

## 技術棧

| 層 | 使用技術 |
| --- | --- |
| 分析 | Python 3.11、numpy、pandas、scipy、scikit-learn、matplotlib；版本鎖定在 [`requirements.txt`](requirements.txt) |
| 主程式 | Jupyter notebook [`hw2.ipynb`](hw2.ipynb)；`python -m hw2.run_notebook` 以 nbclient 非互動執行 |
| 分析套件 | [`hw2/`](hw2/)：資料、前處理、分割、特徵選擇、OLS 與預測區間、Test 評估守門、`model_data` 匯出、診斷、解釋、報告建置、打包 |
| Dashboard | 靜態 HTML／CSS／JavaScript，無建構步驟、無後端；Chart.js 打包在 `assets/vendor/`；`assets/hw2core.js` 是 dashboard 自己的前處理與預測計算；探索模式是 `assets/explore_*.js`（載入、引擎、控制器、頁面與繪圖），全部在瀏覽器內計算 |
| 報告 | Markdown 模板 [`report/report.md`](report/report.md) → HTML → PDF；Node.js 驅動 Chrome 或 Edge 擷取 dashboard 截圖與列印 PDF |
| 測試 | pytest（[`tests/`](tests/)）；dashboard 與探索模式的 Node 測試（[`tests/js/`](tests/js/)，引擎與 Python 參照的比對由 pytest 驅動）；dashboard 外部資源靜態掃描（`python -m hw2.offline_scan`，只有探索載入模組可以出現 `fetch(`） |
| 發布 | GitHub Pages（發布自 `main`）；不使用後端、API、資料庫或 Vercel |

## 重跑步驟（Windows，Python 3.11）

在 `home_work_02/` 目錄執行：

```bash
py -3.11 -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
.venv/Scripts/python -m hw2.run_notebook      # 非互動執行 hw2.ipynb，重現唯一一次的 Test 評估，寫出 results/ 與 assets/model_data.js
.venv/Scripts/python -m pytest                # Python 測試（含以 synthetic fixture 與 Python 參照執行的 Node 一致性測試）
.venv/Scripts/python -m hw2.offline_scan      # dashboard 外部資源靜態掃描
node --test tests/js/core.test.js             # dashboard 計算的 Node 測試
node --test tests/js/explore_load.test.js tests/js/explore_boundary.test.js tests/js/explore_app.test.js tests/js/explore_methods.test.js tests/js/explore_custom.test.js tests/js/explore_run.test.js   # 探索模式的 Node 測試
.venv/Scripts/python -m hw2.report            # 建置報告：dist/report/hw2_report.md、.html、.pdf
.venv/Scripts/python -m hw2.package           # 作者繳交前的打包步驟，需要本機、不進 git 的輸入
```

- **報告建置**需要 Node.js 與 Chrome 或 Edge（擷取 dashboard 截圖、列印 PDF；找不到瀏覽器時以環境變數 `HW2_BROWSER` 指定執行檔）。`--no-pdf` 只產生 Markdown 與 HTML；`--final` 在 AI 證據章節仍是【待填】時失敗。建置前會核對匯出的 Test 結果就是唯一一次正式評估的結果，不符就拒絕建置。AI 證據章節（「GPT 輔助內容」的 ChatGPT 部分、「NotebookLM 摘要」、附錄 B 的 ChatGPT 對話 PDF）在建置時讀取本機的 `acceptor_materials/`：材料的 sha256 必須與收件紀錄相同，否則拒絕建置；NotebookLM 摘要必須至少 100 個漢字，且每一句都在對照表中；PDF 版本把 ChatGPT 對話 PDF 的原頁接在報告最後。材料不存在時只有對應章節以【待填】標示，其他章節照常建置。
- **Test 評估只有一次**：唯一一次正式 Test 評估在 notebook 第 5.4 節、全部選擇（各方法 CV winner、整體 CV winner、Ridge／Lasso 的 alpha）只用 training set 固定之後執行，執行識別 `fe76019b9af84b1e8ff46095d5ac0fb2`、Test 結果摘要（`test_inputs` 與 `test` 的 sha256）`b53ff286ae0734add8b272089aba904a1cb7f5aca444a62d356420b25dc3cfc6`；權威紀錄在 `doc/governance/worklog/issue-63.md` §5。`model_data` 的 `meta.test_evaluation` 只記錄**產生目前這份檔案的那次執行**；完整重跑 notebook 是以相同的 seed 與鎖定版本**重現**同一個評估，不是新的評估，結果必須與上述摘要完全相同（bit-exact），不一致時不得採用新數字。同一次執行內第二次評估會被拒絕。
- 四種方法的路徑計算時間每次重跑都會量測，寫在 `model_data` 的 `meta.timing_s`（`path_<方法>`）與 `meta.path_timing_s`，notebook 第 4.2 節與報告也會列出；Ridge／Lasso、p-value backward 與 Test 評估的時間在 `meta.timing_s` 與 `meta.comparison_timing_s`。
- 要在單元目錄**以外**產生一份使用 synthetic fixture 的 dashboard 複本（例如量測繪圖效能；不是正式結果，頁面頂端會顯示警告）：`.venv/Scripts/python -m hw2.fixture <單元以外的輸出目錄>`。
- macOS／Linux 把 `.venv/Scripts/python` 換成 `.venv/bin/python`。

### 本機、不進 git 的材料與輸出

以下路徑都列在 `home_work_02/.gitignore`，不得加入版本控制：

| 路徑 | 內容 |
| --- | --- |
| `acceptor_materials/` | ChatGPT 對話 PDF、NotebookLM 原始輸出與來源清單（作者提供）；`derived/` 是 Claude Code 依這些材料整理的報告章節與 NotebookLM 摘要的對照表，同樣不進 git |
| `dist/` | 建置與打包輸出（`dist/report/` 的報告；`<學號>_hw2.ipynb`、`<學號>_hw2.zip`） |
| `.venv/` | 虛擬環境 |

## 檔案配置

```text
home_work_02/
├── README.md               # 本檔：專案說明
├── CONTEXT.md              # 專案語彙
├── hw2.ipynb               # 主程式（CRISP-DM 六章；唯一的數字來源）
├── hw2/                    # 分析套件
├── requirements.txt        # 鎖定版本的相依套件
├── data/                   # kc_house_data.csv
├── results/                # 匯出結果：model_data.json、split/、tables/、figures/、deployment/
├── index.html · assets/    # Dashboard（assets/model_data.js、hw2core.js、app.js、vendor/；探索模式 explore_*.js、data/）
├── report/                 # 報告來源
├── tests/                  # pytest；tests/js/ 是 dashboard 計算的 Node 測試
└── doc/                    # 題目、brief、spec、票務索引、驗收清單、README 截圖與治理紀錄
```

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
| `index.html`、`assets/` | Dashboard；`assets/hw2core.js` 是 dashboard 自己的前處理與預測計算，`assets/app.js` 是 King County 檢視；Chart.js 4.4.1 打包在 `assets/vendor/`（MIT，授權檔同目錄） |
| `assets/explore_load.js`、`explore_engine.js`、`explore_app.js`、`explore_ui.js`、`explore_plot.js`、`explore.css` | 探索模式：CSV 載入契約與唯一的 URL 讀取（`explore_load.js`）、Exploratory run 引擎（純函式，不碰 DOM 與網路）、控制器（執行、取消、不並行）、頁面與繪圖 |
| `assets/data/` | 50 Startups：`50_Startups.csv`（原始位元組）、`startups50.js`（同一文字內嵌為 JS 全域，供 `file://` 使用）、`50_Startups.SOURCE.md`（來源與 sha256）、`50_Startups.LICENSE.md`（MIT 授權聲明） |
| `hw2/explore_reference.py` | 探索模式的通用 Python 參照，只供測試即時產生比對用的參照結果；正式分析與 notebook 不使用它 |
| `doc/` | 需求（老師原文，唯讀）、Brief、Spec、票務索引、驗收清單 `doc/acceptance/ACCEPTANCE.md`、本檔的 dashboard 截圖 `doc/screenshots/` 與治理紀錄 |

## 驗證紀錄

- `pytest`：資料核對、分組切分、特徵選擇路徑、Test 評估守門、`model_data` 契約、報告建置與數字單一來源、README 的章節與數字、驗收清單的狀態、打包，以及追蹤檔案不含實際學號與作者材料。
- Node 測試：dashboard 的前處理與預測計算與 Python 一致；`hw2.offline_scan` 確認 dashboard 沒有外部資源。
- 探索模式：Node 引擎對 Python 參照（四種方法、winner、聚合與凍結、Lasso 停止與目標單位、共線診斷、預測區間）、CSV 載入與三層前處理邊界、以 mock fetch 驗證的請求隔離、運算預算、失敗隔離、取消與不並行、可重現性，以及 King County 區塊不變的結構快照。
- 乾淨環境重跑（新建虛擬環境、安裝、非互動執行 notebook、測試、建置報告、打包）與 dashboard 人工檢查（含 `file://` 離線與 GitHub Pages）的結果，逐條記在 [`doc/acceptance/ACCEPTANCE.md`](doc/acceptance/ACCEPTANCE.md)，證據在 [`doc/governance/worklog/`](doc/governance/worklog/)。

## 詳細文件

| 文件 | 內容 |
| --- | --- |
| [`CONTEXT.md`](CONTEXT.md) | 專案語彙：分組切分、特徵選擇路徑、CV winner、一次性 Test 評估、metric-only 模型、預測區間等用詞定義 |
| [`doc/requirement/`](doc/requirement/) | 老師的作業頁與講義（原文與逐字轉寫，唯讀） |
| [`doc/brief/BRIEF.md`](doc/brief/BRIEF.md)、[`doc/brief/BRIEF-V2.md`](doc/brief/BRIEF-V2.md) | 需求盤點與範圍決定（V2 是兩項加分的增量） |
| [`doc/spec/SPEC.md`](doc/spec/SPEC.md)、[`doc/spec/SPEC-V2.md`](doc/spec/SPEC-V2.md) | 實作 spec（V2 是探索模式的增量修訂） |
| [`doc/ticket/tickets.md`](doc/ticket/tickets.md)、[`doc/ticket/tickets-v2.md`](doc/ticket/tickets-v2.md) | 票務索引（票本體在 GitHub Issues） |
| [`doc/acceptance/ACCEPTANCE.md`](doc/acceptance/ACCEPTANCE.md) | 逐條驗收清單與證據位置 |
| [`doc/governance/`](doc/governance/) | Outcome Contract、決策紀錄、worklog、audit 與 run 紀錄 |
