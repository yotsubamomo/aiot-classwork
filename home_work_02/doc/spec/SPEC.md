# Spec: HW2 Multiple Linear Regression — King County 房價分析與 Dashboard（`home_work_02/`）

- **來源**：已接受的 [Brief](../brief/BRIEF.md)（commit `dff7c55c`；接受紀錄 [`../governance/outcome-contract.md`](../governance/outcome-contract.md)）。本 Spec 由 MATT `/to-spec` 產生，不重新開啟 Grill 的決定；Brief 與本 Spec 不一致時以 Brief 為準並回報。
- **詞彙**：依 [`../../CONTEXT.md`](../../CONTEXT.md)。
- **版本**：rev 4（2026-10-18）— 依 CC-1（Ridge／Lasso 一次性 test evaluation 的 contract change）補記授權依據與約束，metric_only 契約本身不變；rev 3 依 acceptor 對 SR-06／SR-09 的決定與 Spec Review SR-10～SR-12 修訂；rev 2 依 SR-01～SR-09 修訂（處理紀錄見 [`SPEC-review-2026-10-18.md`](SPEC-review-2026-10-18.md)）；rev 1 為 `/to-spec` 的初版（commit `3aacb54`）。
- **GitHub Issue**：[yotsubamomo/aiot-classwork#59](https://github.com/yotsubamomo/aiot-classwork/issues/59)（label `ready-for-agent`；2026-10-18 發布）。Issue 本文與本檔於發布時相同；之後若修訂，以本檔為準並同步更新 Issue。
- **測試 seams**（acceptor 2026-10-18 確認）：主 seam 是 `model_data` 匯出契約（pytest＋Node test）；次 seam 是 Python 套件的公開函式（pytest）；UI 以人工檢查表驗收。

## Problem Statement

老師的 HW2 要求以 Kaggle 資料集做一份完整的多元線性回歸分析：遵循 CRISP-DM 六階段、必做特徵選擇與模型評估、預測圖附信賴或預測區間、附上 ChatGPT 對話與 NotebookLM 研究、以主程式與 PDF 報告打包成學號 ZIP 繳交。老師另在課堂口頭要求成果要像 DIC-2 範例一樣以互動網站呈現。

現況是 `home_work_02/` 只有老師文件、Brief 與詞彙表，沒有任何分析、資料、dashboard 或報告。前一輪的設計因需求擴散而廢止；這次要在已接受的 Brief 邊界內，把分析、dashboard、報告與繳交套件一次做對，而且每個數字都要能從一次可重現的執行追溯回來。

## Solution

以 King County House Sales 資料集，用一本 notebook 當主程式跑完整個 CRISP-DM 流程：固定的前處理、以房屋分組的 80/20 切分、在 training set 內以分組 5-fold CV 比較四種有 k 路徑的特徵選擇方法在 k = 1…18 的 OLS 模型與單一的 All-in baseline（加 Ridge／Lasso 對照與講義的 p-value backward 對照），以 CV RMSE 選出各方法與整體的 CV winner，只對被授權的模型在 test set 上評估一次，為每筆 test 交易給出參數式 95% 預測區間，做五大假設診斷與模型解釋，並把結果匯出成單一的 `model_data` 契約。

一個離線可用的靜態 dashboard 讀取這份契約：任意 (方法, k) 顯示訓練 CV 指標與即時預測（含 PI），test 區塊只呈現被授權評估的模型，實際 vs 預測圖畫出全部 test 樣本與逐筆 PI。獨立的 PDF 報告引用同一份匯出結果，附上 acceptor 提供的 ChatGPT 與 NotebookLM 證據。最後由打包步驟從同一份 notebook 產生學號命名的 ZIP。

## User Stories

### 評分者（老師）

1. As a 評分者, I want 報告與 notebook 都清楚寫出資料集名稱、Kaggle 連結與授權, so that 我能確認資料來源符合作業要求。
2. As a 評分者, I want 看到 source feature 數量（19）與建模 feature group 數量（18）以及計數規則, so that 我能判定它符合 10–20 的要求與補充的 14–39 條件。
3. As a 評分者, I want 報告引用「10 至 20 個特徵」與「features > 13, < 40」兩條原文並說明採用交集, so that 我知道作者沒有忽略任一條指示。
4. As a 評分者, I want notebook 與報告各有 Business Understanding、Data Understanding、Data Preparation、Modeling、Evaluation、Deployment 六章, so that CRISP-DM 流程完整可循。
5. As a 評分者, I want 看到四種特徵選擇方法在同一組 CV 折上的 RMSE 隨 k 的變化，以及 All-in baseline 的參考線, so that 我能評斷特徵選擇做得是否扎實。
6. As a 評分者, I want 看到講義教的 p-value backward elimination 的結果被拿來對照, so that 我知道作者理解課堂方法與 CV 方法的差別。
7. As a 評分者, I want 看到 Ridge 與 Lasso 和 OLS 的比較, so that 我能評估正則化在這個資料上的效果。
8. As a 評分者, I want 每個 CV winner 在 test set 上的 MAE、MSE、RMSE、R²（USD）, so that 我能看到真正的保留集表現。
9. As a 評分者, I want 一張實際 vs 預測圖，每筆 test 樣本都有自己的 95% 預測區間, so that 「預測圖加上區間」的要求被實際滿足。
10. As a 評分者, I want 報告說明預測區間的統計定義、假設與限制，並列出經驗涵蓋率, so that 我能判斷區間不是用 RMSE 畫的固定寬度帶。
11. As a 評分者, I want 看到線性、誤差獨立、同質變異、殘差常態、多重共線性五項診斷與解讀, so that 補充建議的假設檢驗有被處理。
12. As a 評分者, I want Deployment 章節有預測新樣本的示範與模型解釋, so that 模型不只是數字而是可用、可解釋的。
13. As a 評分者, I want 報告中明確標示「GPT 輔助內容」與「NotebookLM 摘要」兩節, so that AI 協助的要求一目了然。
14. As a 評分者, I want 看到與網路上主流或更優解法的比較，附來源連結, so that 研究脈絡的要求被滿足。
15. As a 評分者, I want 報告清楚區分「老師要求」「依老師補充建議」「專案延伸」, so that 我不會把作者的延伸誤認為必要項目，或反之。
16. As a 評分者, I want 打開 dashboard 網址就能切換方法與 k 並看到結果變化, so that 成果呈現像 DIC-2 範例一樣有互動性。
17. As a 評分者, I want 解壓 ZIP 後在沒有網路的電腦上也能打開 dashboard 使用全部功能, so that 繳交的內容自足、不依賴外部服務。
18. As a 評分者, I want ZIP 的檔名與主程式檔名用學號, so that 符合繳交格式。
19. As a 評分者, I want 在 dashboard 上輸入一棟房子的條件就得到價格預測與區間, so that 我能直觀感受模型的行為。
20. As a 評分者, I want dashboard 與報告都是繁體中文, so that 閱讀與評分順暢。

### Acceptor（作業作者）

21. As an acceptor, I want 所有模型選擇只用 training set 的 CV 決定、test set 只在最後評估一次, so that 結果沒有資料洩漏，而且我能誠實地說明。
22. As an acceptor, I want train/test 與每個 CV 折都以房屋 `id` 分組, so that 同一棟房子的重複交易不會橫跨兩邊。
23. As an acceptor, I want 需要 fit 的前處理只看到當次訓練列, so that 標準化與 one-hot 類別不會偷看驗證折或 test。
24. As an acceptor, I want 選擇單位是 feature group、同一 source feature 的 encoded columns 同進同出, so that k 的意義與老師的特徵數規則一致。
25. As an acceptor, I want 以 log(price) 建模但以 USD 報告, so that 區間較合理，而指標仍是老師看得懂的尺度。
26. As an acceptor, I want 報告明確區分 exp(log 預測) 與條件平均, so that 統計解讀不被挑錯。
27. As an acceptor, I want Adjusted R² 只對 OLS 子集在 log 尺度以實際秩計算、並清楚標示, so that 不會對 Ridge／Lasso 或 CV 聚合值套用不適用的公式。
28. As an acceptor, I want All-in baseline 被當成單一的完整模型而不是 k 路徑, so that 比較的呈現不會誤導。
29. As an acceptor, I want 若 test 排名與 CV 排名不同，模型也不會被換掉, so that 選模的誠實性可被審查。
30. As an acceptor, I want dashboard 任意切換 (方法, k) 時顯示的是訓練 CV 數字, so that test 不會變成互動式選模的依據。
31. As an acceptor, I want test 區塊只對各方法 CV winner、All-in 與整體 CV winner 存在，並清楚標示展示的是哪個模型, so that 瀏覽者不會混淆資料來源。
32. As an acceptor, I want 當選取模型與 test 區塊模型不同時有清楚可見的提示, so that 瀏覽者知道兩者不同。
33. As an acceptor, I want `model_data` 只包含被授權評估模型的 test 結果, so that dashboard 在結構上就做不到瀏覽其他模型的 test。
34. As an acceptor, I want dashboard 的即時預測與 PI 和 Python 匯出的結果逐筆一致（含日期、整修年、zipcode 的轉換）, so that 網頁上的數字就是模型的數字。
35. As an acceptor, I want 即時預測器只顯示當前模型用到的 source feature 原始值輸入，預設 training 中位數、超出範圍有警告但仍計算, so that 使用者能理解且不被阻擋。
36. As an acceptor, I want 固定 seed、鎖版本的相依與乾淨環境重跑一致, so that 任何人都能重現我的數字。
37. As an acceptor, I want 報告與 README 的每個數字都引自匯出結果，而不是手抄, so that 不會出現兩套數字。
38. As an acceptor, I want repo 中的 notebook 不含學號、打包時才命名為學號檔名，而且不維護兩份, so that 公開 repo 不洩露學號，繳交又符合格式。
39. As an acceptor, I want 任何追蹤檔案都不出現實際學號, so that 隱私規則可被 `git grep` 驗證。
40. As an acceptor, I want ChatGPT PDF 與 NotebookLM 原始材料不進 git、只進 ZIP 與報告, so that 我的對話與研究紀錄不公開。
41. As an acceptor, I want agent 對 NotebookLM 材料只做整理、摘要、翻譯，不新增內容或來源, so that 證據保持真實可追溯。
42. As an acceptor, I want 「GPT 輔助內容」節如實揭露 ChatGPT 與 Claude Code 各自的用途, so that 揭露誠實。
43. As an acceptor, I want 異常值不被刪除而是被診斷與說明, so that 不會被質疑挑資料。
44. As an acceptor, I want Backward SFS 與 RFE 的執行時間被量測記錄，成本過高時先收到可行的改善方案, so that 研究範圍不會被默默縮小。
45. As an acceptor, I want 一份 ACCEPTANCE.md 把每條要求與決定對到可觀察的檢查與證據, so that 我能逐條驗收。
46. As an acceptor, I want dashboard 隨 ZIP 交付並完全離線可用（含打包的 Chart.js）, so that 老師不用上網就能看到網站。
47. As an acceptor, I want 單元 README 有目的、資料來源與授權、流程、成果、重跑步驟、dashboard 連結與檔案配置, so that 老師與我自己都能從 README 進入。
48. As an acceptor, I want root README 的作業表與 CONTEXT-MAP 各加一列, so that 整個 repo 的導覽一致（動手前先說明，屬 RB-5）。
49. As an acceptor, I want 五大假設的診斷用最終模型在 training set 的殘差（log 尺度）並討論重複交易的影響, so that 診斷與區間的假設對應。
50. As an acceptor, I want 經驗涵蓋率偏離 95% 時得到分析而不是失敗判定, so that 結果可以誠實呈現。

### Dashboard 使用者

51. As a dashboard 使用者, I want 在方法選單選一個方法、在 k 選單選一個 k 後，KPI、指標 vs k 圖、預測器與 test 區塊同步更新, so that 操作直覺。
52. As a dashboard 使用者, I want 「比較全部」把四個路徑方法的 k 路徑疊在同一張圖（All-in、Ridge、Lasso 為參考線）並列出各方法 CV winner 與 All-in 的比較表, so that 我能一眼看出哪個方法最好。
53. As a dashboard 使用者, I want 指標 vs k 圖上有 All-in、Ridge、Lasso 的參考線, so that 單一模型也能和路徑比較。
54. As a dashboard 使用者, I want 實際 vs 預測圖用 log 刻度、有 y=x 參考線、每筆有垂直 PI 線段、點依是否落入區間著色, so that 我能看出模型哪裡準、哪裡不準。
55. As a dashboard 使用者, I want 實際 vs 預測圖能縮放檢視而且不卡頓, so that 四千多筆資料仍可讀。
56. As a dashboard 使用者, I want 看到 test 的涵蓋計數、n_test、平均寬度與抽樣不確定性, so that 我知道 95% 的宣稱有多可信。
57. As a dashboard 使用者, I want 選到 All-in 時 k 固定、不出現 k 選單的錯覺, so that 不會以為 All-in 有路徑。
58. As a dashboard 使用者, I want 預測器的 zipcode 用下拉選單、日期用日期輸入、整修用「未整修」選項, so that 我填的是看得懂的原始值。
59. As a dashboard 使用者, I want 「方法與限制」區塊說明選模協定、區間假設、使用範圍與非因果提醒, so that 我不會過度解讀。
60. As a dashboard 使用者, I want 頁面所有文字為繁體中文且沒有缺字方塊, so that 閱讀正常。

### 實作者與審查者

61. As an 實作者, I want 一個 `model_data` 契約文件化了每個欄位的意義與單位, so that Python 與 JS 兩側不會各自解讀。
62. As an 實作者, I want 一組 pytest 在匯出後檢查契約的內部一致性, so that 我在改分析程式時立刻知道有沒有弄壞契約。
63. As an 實作者, I want 一組 Node test 以匯出的 test 列為基準核對 JS 預測、PI 與前處理, so that dashboard 的計算與 Python 一致。
64. As an 實作者, I want 分組隔離、fit 只看訓練列、PI 公式與秩檢查都有自動測試, so that 洩漏與公式錯誤會被抓到。
65. As an 審查者, I want 每個 AC 都能對到一個可執行的測試或一條人工檢查, so that 審查不需要猜。
66. As an 審查者, I want 匯出結果有執行時間、seed、套件版本與資料 sha256 的中繼資料, so that 我能核對重現條件。

## Implementation Decisions

### 單元結構與交付物

- 單元 `home_work_02/` 內：主程式 notebook（repo 內不含學號）、Python 分析套件（資料、前處理、分割、特徵選擇、建模、區間、診斷、匯出、打包各一個模組，名稱由實作決定）、Python 測試、資料檔、結果目錄（CSV、PNG、`model_data`）、dashboard 靜態檔（頁面、樣式、腳本、打包的 Chart.js）、Node 測試、報告來源與建置產物、README、ACCEPTANCE.md、鎖版本的 requirements。
- Notebook 是主程式與唯一的數字來源：它呼叫套件、產生全部結果檔與 `model_data`；報告與 README 的數字都從匯出結果引用。打包步驟從同一份 notebook 產生學號命名的副本，並記錄 checksum；實際學號從本機未追蹤的設定讀取，追蹤檔案一律 `<學號>`。
- 單元 `.gitignore` 排除：SRC-2 PDF（已有）、acceptor 材料目錄、打包設定、打包輸出、虛擬環境、notebook checkpoints。
- Root `README.md` 與 `CONTEXT-MAP.md` 各加一列屬 RB-5：在對應的票中先說明再動手，並以單獨的 commit 處理。

### 資料、計數與前處理

- 資料檔 commit 在單元內，載入時先算 sha256 再解析；與固定值不同時以指明預期值與實際值的錯誤停止。重新下載後若不同，依 Brief 記錄為 re-pin。
- 載入後驗證 schema（21 欄、欄位順序）、列數 21,613、唯一 `id` 數 21,436、`sqft_living = sqft_above + sqft_basement` 對每列成立。
- Source features 為 CSV 欄位扣除 `id` 與 `price` 的 19 個；建模 feature groups 為其中 18 個（`sqft_basement` 不進模型）。Canonical order 依 CSV 欄位順序。
- 固定的逐列轉換（不需 fit、對所有候選相同）：`date` → 距固定基準日的天數；`yr_renovated` → `is_renovated` 旗標與有效年份（未整修時為 `yr_built`），兩欄同屬 `yr_renovated` group；`zipcode` 為 nominal；其餘照原值。
- 需要 fit 的前處理放在 pipeline 內、只以當次訓練列 fit：`zipcode` one-hot（類別取自訓練列，drop 第一類，預測時未見類別編為基準類別）；數值欄的標準化只用於 Ridge／Lasso，OLS 子集模型以原始尺度擬合，使係數可直接解讀且 dashboard 不需重做標準化。
- 目標為 ln(price)；點預測 ŷ = exp(f(x))，不作偏誤修正，報告說明它估計的是條件中位數。
- 異常值不刪除；Data Understanding 以 training set 列出極端值並在診斷中討論。

### 分割與交叉驗證

- 80/20 train/test，以房屋 `id` 為 group、固定 seed 的分組隨機分割；三個不變量：兩邊沒有共同 `id`、聯集為全部列、同一 seed 重跑結果相同。
- Training set 內 5 個分組 fold，只產生一次並保存每列的 fold 編號；所有方法、所有 k、Ridge／Lasso 都用同一組 fold。
- 每個 fold 內的前處理、特徵選擇與調參只用該 fold 的訓練列；驗證列只用來算指標。**選擇與評估的邊界**（SR-01）：對每個路徑方法與每個 fold，k = 1…18 的子集序列是**在該 fold 的訓練列上重新計算**的（fold-internal selection），再以該子集在同一 fold 訓練列上擬合 OLS、在驗證列上算指標。驗證列不參與任何子集的選擇；同一個 fold 不會同時用來選子集與評估該子集。因此同一方法同一 k 在不同 fold 的子集可以不同，契約記錄各 fold 的子集與一致的 fold 數。
- **Canonical subset**：每個 (方法, k) 另有一個在**整個 training set** 上以同一方法計算的子集，稱為 canonical subset；它是 dashboard 顯示的 groups、即時預測器與 test 評估所用的模型（在整個 training set 上擬合）。CV 指標估計的是「該方法在 k 下的程序」的表現，不是 canonical subset 本身的表現；報告與 dashboard 的方法說明寫明這一點。
- **選擇偏誤陳述**：在 18 個 k 與多個方法之中取 CV RMSE 最小者，會使 CV winner 的 CV 分數帶有樂觀偏誤；凍結後的 test evaluation 才是 CV winner 表現的獨立估計。報告不得把 CV winner 的 CV 分數寫成不偏估計。

### 特徵選擇與模型

- 正式比較的對象是**四種有 k 路徑的特徵選擇方法**——Forward SFS、Backward SFS、RFE、Lasso 路徑排序取 top-k——加上**單一的 All-in baseline**（全部 18 group 的 OLS，沒有 k 路徑；SR-06）。每個路徑方法在每個 fold 的訓練列上產生 k = 1…18 的巢狀或排序子集（見上節的邊界），每個 k 以 OLS 在 fold 訓練列上擬合、在驗證列上算 USD 指標，CV 指標為 5 折平均（另存各折值與標準差）。
- 選擇單位為 feature group：SFS 與 RFE 每一步加入或移除整個 group；Lasso 路徑以 group 的進入順序（group 內任一欄係數首次非零的 alpha）排序，平手依 canonical order。RFE 的 group 重要度彙總規則由實作決定並寫入方法說明。
- 講義方法對照：p-value backward elimination 以 group 層級的 F 檢定（或等效）、門檻 0.05 執行，**與正式方法同樣採 fold-internal selection**（SR-11）：在每個 fold 的訓練列上消去得到該 fold 的子集、在驗證列上算指標，CV 指標為 5 折平均；另在整個 training set 上執行一次得到 canonical subset 供顯示。它產生**單一子集、沒有 k 路徑**，只列為對照列，不參與 CV winner，也不在 test 上評估。
- 對照模型：Ridge 與 Lasso 用全部 18 group、標準化後以同一組 fold 的 CV 選 alpha（網格由實作決定並記錄）；只報 CV 與 test 指標，不提供 PI 與即時預測。**Test 評估的授權依據是 CC-1**（acceptor 2026-10-18 核准的 contract change，`doc/governance/outcome-contract.md` §4）：每個模型只做一次最終 test evaluation，只報 USD 的 MAE、MSE、RMSE、R²；alpha 只以 training CV 選；不參與整體 CV winner 競爭；test 結果不回饋任何選擇；dashboard 互動不得觸發重新測試；dashboard 與報告中 Ridge／Lasso 的 CV 指標與 test 指標分開標示。
- CV winner：各路徑方法取 CV RMSE 最小的 k（平手取較小的 k）；整體 CV winner 為各方法 CV winner 與 All-in 中 CV RMSE 最小者（平手依方法的固定順序）。被授權在 test 評估的模型集合＝各方法 CV winner ∪ {All-in} ∪ {整體 CV winner}，同一模型只評估一次；Ridge／Lasso 的 test 指標亦各報一次作為對照。
- 最終模型＝整體 CV winner 在整個 training set 上重新擬合；用於 Deployment 的預測函式、pickle 示範、診斷與報告主要結果。
- 執行時間：每個方法的路徑計算時間都量測並寫入匯出中繼資料與 README；若任一方法的時間使整體重跑不可接受，停止並回報改善方案，不縮小 k 範圍或方法集合。

### 指標與推論

- CV 與 test 都報 MAE、MSE、RMSE、R²，以 USD 計算（對 exp 回轉後的預測）。
- Adjusted R² 只對 OLS 子集模型（含 All-in）計算：在 log 尺度、以 n_train 與實際 model rank（含截距）套古典公式，與 log 尺度 R² 並列；Ridge／Lasso 與 CV 聚合值欄位標「不適用」。
- 每個被擬合的 OLS 模型記錄實際 design matrix 的欄數與秩。**秩不足的語義**（SR-04）分三類，都不得以臨時刪欄、合併類別或改變 encoding 處理，也不縮小已接受的方法與 k 範圍：
  - **合法的 encoding 結果**（不是缺陷）：one-hot 類別只取自當次訓練列，所以某個 zipcode 若不在該 fold 的訓練列中，該 fold 的設計矩陣就沒有那一欄；驗證列或 test 中出現時編為基準類別。契約記錄每個 fit 實際使用的類別清單，以及被編為基準的未見類別筆數。
  - **無效候選**（候選層級）：某個 (方法, k, fold) 的設計矩陣（含截距）在該 fold 訓練列上秩不足（例如某欄在該訓練列上為常數或與其他欄完全共線）。該 fold 的指標記為無效並附原因；該 (方法, k) 的 CV 指標若有任一 fold 無效，整個 (方法, k) 標為 `invalid`、不參與 CV winner，並在比較表與 dashboard 以明確標示呈現。路徑方法在該步的選擇照常進行，不跳過 group。
  - **無效候選也包括 canonical fit**（SR-10）：某 (方法, k) 的 canonical subset 在整個 training set 上秩不足時，該 (方法, k) 同樣標為 `invalid`（原因 `canonical_rank_deficient`），沒有 `fit`、不提供即時預測、不參與 winner；其他有效候選照常完成比較與評估。**有效候選**＝CV 全部 fold 有效且 canonical fit 有效；各方法的 CV winner 只在有效候選中選。
  - **實驗層級失敗**（停止並回報）：All-in 在任一 fold 或整個 training set 上秩不足；任一方法沒有任何有效候選（因此沒有 CV winner）；或整體 CV winner 無法決定。這些情況表示資料或固定前處理有結構性問題（例如 `sqft_basement` 誤入模型），notebook 以錯誤停止並列出全部 invalid 候選與原因，route 給 acceptor，不自行修補、不刪除任何 feature group。

### 預測區間

- 對 OLS 子集模型，在 log 尺度計算參數式 95% 預測區間：ŷ_log ± t(0.975, df_resid)·√(s²(1 + x₀ᵀ(XᵀX)⁻¹x₀))，再 exp 回 USD；匯出 s²、df_resid、t 臨界值、(XᵀX)⁻¹ 與係數，使 JS 能重算。
- Test 評估時對每筆 test 交易記錄點預測、下界、上界、是否涵蓋（閉區間）；coverage = 涵蓋筆數 / n_test；平均寬度以 USD 計；抽樣不確定性以 √(p(1−p)/n_test) 的 1.96 倍表示，**並標明它是假設各筆涵蓋事件獨立的二項近似**（SR-08、SR-12）：test 內含同一房屋的重複交易，涵蓋事件不保證獨立，所以這個近似的準確度未經估計；報告**不陳述**偏差的方向或幅度，只說明假設、列出 test 的房屋數與重複交易筆數，並把它與 Brief 的「不宣稱保證 95%」一起說明。群組感知的不確定性估計不在本 Spec 範圍內。
- 報告寫明假設（殘差常態、同質變異、獨立）、特徵選擇後推論與模型誤設的影響，不宣稱保證 95%。

### 診斷與解釋

- 五大假設用最終模型在 training set 的殘差（log 尺度）：線性（殘差 vs 擬合值）、誤差獨立（殘差序列與重複交易的討論，統計量由實作選）、同質變異（尺度—位置圖與一個檢定）、常態（Q–Q 圖與一個檢定）、多重共線性（group 內與 group 間的 VIF 或條件數）。每項輸出圖或數值並有解讀；違反只記錄不判失敗。
- 模型解釋：係數在 log 尺度的百分比效果解讀（含 one-hot 相對基準類別的讀法）、只用 training set 計算的 permutation importance（重複次數與指標由實作定、寫入方法說明）、使用限制與非因果提醒。

### `model_data` 契約（主 seam）

- 單一 JSON 物件，另以 `.js` 包裝成全域變數供 `file://` 載入；兩者內容相同。
- 頂層區段：
  - `meta`：資料集名稱、連結、授權、CSV sha256、列數、source feature 清單、feature group 清單（canonical order）、seed、分割比例與 n_train／n_test、fold 數、套件版本、各方法執行時間、產生時間。
  - `preprocess`（SR-02）：重做前處理所需的中繼資料——`date` 的基準日與天數定義、`yr_renovated` 的旗標與有效年份規則、`sqft_basement` 排除的說明、feature group 與其 encoded columns 的對應、encoded column 的 canonical order。
  - `methods`（SR-05：每個項目分三層，欄位名稱帶尺度）：每個路徑方法的 k = 1…18 項目，各含
    - `canonical_groups`（整個 training set 上計算的子集）、每個 fold 的 `fold_groups` 與 `folds_agree`（與 canonical 相同的 fold 數）、`status`（`valid` 或 `invalid` 與原因）；
    - `cv`：**USD 尺度**的各折與平均／標準差 MAE、MSE、RMSE、R²（來自 fold-internal 程序）；
    - `fit`：canonical subset 在**整個 training set** 上擬合的統計——**log 尺度**的 R² 與 Adjusted R²、n_train、design matrix 欄數與 rank、df_resid、s²、t 臨界值、係數（原始尺度，含截距）、(XᵀX)⁻¹、encoded column 順序、one-hot 類別清單與基準類別；
    - `is_method_winner`。
    `methods` 中沒有任何 test 欄位。
  - `baselines`：All-in（結構同 `methods` 的單一項目：`cv`＋`fit`）、Ridge、Lasso（`cv` 指標與 alpha；沒有 `fit` 的 PI 欄位）、p-value backward 對照（子集與 `cv` 指標）。
  - `winners`：各方法 CV winner 的識別、整體 CV winner 的識別、被授權評估 test 的模型清單。
  - `test_inputs`（SR-02）：全部 test 交易各一列，含列識別（資料列序號與房屋 `id`、交易日期）與全部 18 個建模 source feature 的**原始值**，以及 `actual_price`；另含 test 的房屋數與重複交易筆數（SR-08）。
  - `test`（SR-03）：被授權評估的模型各一筆，每筆有 `kind`：
    - `kind = "ols_subset"`（各方法 CV winner、All-in、整體 CV winner）：USD 尺度的 test MAE、MSE、RMSE、R²、n_test、coverage、涵蓋筆數、平均寬度、二項近似的不確定性，以及與 `test_inputs` 同序的逐筆 `predicted`、`lower`、`upper`、`covered`（全部 test 樣本，不抽樣）；
    - `kind = "metric_only"`（Ridge、Lasso）：USD 尺度的 test MAE、MSE、RMSE、R²；**沒有** PI、coverage 或逐筆欄位。
  - `inputs`：每個 source feature 在 training set 的最小值、最大值、中位數；training set 的 zipcode 類別清單；日期範圍。
- 契約不變量：`methods` 與 `baselines` 中沒有 test 欄位；`test` 中 `ols_subset` 的鍵集合等於 `winners` 的授權清單，`metric_only` 只有 Ridge 與 Lasso；`ols_subset` 必有 PI 欄位、`metric_only` 必無；每筆 `covered` 等於 `lower ≤ actual ≤ upper`；coverage 等於 covered 之和除以 n_test；**任一 `ols_subset` 的逐筆點預測與 PI，都可只用 `test_inputs` 的原始值、`preprocess` 的規則與該模型 `fit` 內的係數、類別、s²、df_resid、t、(XᵀX)⁻¹ 獨立重算**（不依賴 `predicted` 欄位本身）。

### Dashboard

- 靜態頁面，無建置步驟，無後端；Chart.js 打包在單元內；資料以 `.js` 全域變數載入，使 `file://` 可用；頁面不發出任何對外請求。
- 區塊：方法與 k 控制；KPI 卡（標示「訓練 CV」）；指標 vs k 圖（各方法路徑；All-in、Ridge、Lasso 為參考線；「比較全部」疊圖）；即時預測器；test 區塊（test KPI、實際 vs 預測圖、涵蓋統計，標示所展示的方法與 k）；方法與限制。選配：係數表、test 殘差表、全部結果表。
- 分層規則與**來源標示**（SR-05）：任意 (方法, k) 的 KPI 來自 `methods[].cv`，標示「訓練 CV（USD）」；係數表（選配）與預測器來自 `methods[].fit`，係數表標示「全訓練集擬合，R²／Adjusted R² 為 log 尺度」；test 區塊從 `test` 取該方法 CV winner（或 All-in／整體 winner）的資料，標示「Test 評估（USD）」與所展示的方法與 k；選取非 winner 時顯示清楚可見的提示說明 test 區塊展示的是哪個模型；`status = invalid` 的 (方法, k) 在圖與表上以明確標示呈現且不可成為 winner。All-in 選取時 k 控制固定且不可改。 **所有 test 數值只讀自 `model_data`：dashboard 的任何操作（方法／k 切換、比較全部、預測器輸入、縮放）都不觸發新的 test 評估，對 OLS 子集與 Ridge／Lasso 的 `metric_only` 皆然（BR-01；CC-1 第 3 條）。**
- 即時預測器：依當前模型的 canonical groups 動態產生輸入（日期輸入、數值輸入、zipcode 下拉、整修年或「未整修」），預設為 `inputs` 的中位數，超出範圍顯示警告仍計算；JS 依 `preprocess` 重做日期天數、整修旗標與有效年份、one-hot 後計算點預測與 PI。**未見的 zipcode**（SR-07）：下拉選單只列出當前模型 `fit` 的類別清單加上基準類別（標明為基準）；若輸入值不在清單中（例如由網址參數或手動輸入帶入），以基準類別計算並顯示警告「此 zipcode 不在模型的訓練類別中，已以基準類別計算」；契約中記錄 test 內被編為基準的未見 zipcode 筆數，報告說明。
- 實際 vs 預測圖：全部 test 樣本；x 預測、y 實際、log 刻度、y=x 線、每筆垂直 PI 線段、依 covered 著色；支援縮放與檢視；渲染方式由實作決定（可用 canvas 自繪或 Chart.js 外掛），但不得抽樣或聚合，且 log 輸入必須大於零（資料中 price 與預測皆為正）。**可觀察的可讀性與反應性**（SR-09；acceptor 2026-10-18 接受並釐清）：在參考環境（acceptor 的電腦、目前版本的 Chrome 或 Edge）以 `file://` 開啟時，
  (a) **首次繪製 ≤ 3 秒**：起點為瀏覽器的 navigation start，終點為實際 vs 預測圖第一次完整繪製完成（頁面在圖繪製完成的回呼記錄時間戳）；
  (b) **互動更新 ≤ 1 秒**：適用於方法／k 切換、縮放與平移；起點為使用者輸入事件（選單 change、滾輪或拖曳結束），終點為受影響的圖與區塊重繪完成；整個檢查過程沒有瀏覽器的「網頁沒有回應」提示；
  (c) 預設視圖中，y=x 線、區間內與區間外的點以顏色可分辨，圖例與軸標籤可讀；
  (d) 個別 PI 線段的可辨識性以**縮放或游標檢視**驗收：放大到任一價格十倍區間（例如 20 萬～200 萬 USD）後，或以游標停留時，可以分辨個別線段與其端點；**不要求**高密度區域的全部線段在同一畫面下互不重疊；
  (e) 游標停在某一點時可得知該筆的預測、實際與區間；
  (f) 量測紀錄：ACCEPTANCE.md 記錄瀏覽器名稱與版本、作業系統、CPU 與記憶體、n_test、量測方式（頁面內建的時間戳或 DevTools Performance）與各次量測值；
  (g) 達標不得以抽樣、聚合或省略任何 test 樣本與 PI 達成。
- 語言 zh-TW；字型以系統字型為主，必要時打包可離線使用的字型。

### 報告與打包

- 報告以 Markdown 撰寫、建置成 PDF（工具由實作決定）；章節依 Brief §8：CRISP-DM 六章、資料來源與研究脈絡、GPT 輔助內容、NotebookLM 摘要、主流或更優解法比較、dashboard 連結與截圖、附錄 ChatGPT PDF。數字與圖以建置時從匯出結果注入或引用，不手抄。
- 三種標示（老師要求／依老師補充建議／專案延伸）以一張對照表置於報告前段，章節層級再標示。
- 打包：由同一份 notebook 複製為 `<學號>_hw2.ipynb`，連同報告 PDF、ChatGPT PDF、套件、requirements、資料 CSV、README、結果檔、dashboard 靜態檔組成 `<學號>_hw2.zip`；記錄 ZIP 的 sha256 與檔案清單；解壓驗證 dashboard 離線可用。

### Acceptor 輸入與等待

- ChatGPT PDF、NotebookLM 材料、學號設定由 acceptor 放入未追蹤目錄；缺少時只停止對應章節與打包，其餘工作照常。

## Testing Decisions

### 什麼是好的測試

- 只測外部可觀察的行為：匯出契約的內容、公開函式的輸入輸出、JS 計算與 Python 基準的一致性。不測私有函式與中間變數。
- 以真實資料的小子集或固定 fixture 跑得快的測試為主；完整路徑的計算只在 notebook 重跑中驗證。

### 主 seam：`model_data` 契約

- Python（pytest，對匯出的物件）：區段與必要欄位存在；`methods` 每個方法有 k = 1…18；每個項目的 canonical groups 數等於 k，各 fold 的 groups 數也等於 k；`status = invalid` 的項目附原因且不是 winner；`methods` 與 `baselines` 不含 test 欄位；`winners` 與各方法項目的 winner 旗標一致；`test` 的 `ols_subset` 鍵集合等於授權清單，`metric_only` 只有 Ridge 與 Lasso，PI 欄位的有無與 `kind` 一致；逐筆 covered 與上下界一致、coverage 與計數一致、平均寬度一致；**獨立重算**：以 numpy 從 `test_inputs` 的原始值與 `preprocess` 規則重建每個 `ols_subset` 模型的設計列，用 `fit` 的係數、s²、df_resid、t、(XᵀX)⁻¹ 重算全部 test 筆的點預測與 PI，與 `test` 的值逐筆相符（容差 1e-6），且這條重算路徑不呼叫匯出程式的預測函式；`meta` 含 sha256、seed、版本、執行時間；`test_inputs` 的房屋數與重複交易筆數與資料一致。
- JS（Node test，載入 `.js` 契約與 dashboard 計算模組）：對每個 `ols_subset` 模型、`test_inputs` 的每一筆，從原始值經 dashboard 自己的前處理與預測程式重算點預測、lower、upper、covered，與契約值逐筆相符（容差 1e-6）；`metric_only` 模型沒有 PI 可算且 dashboard 不提供其預測；前處理轉換的單元案例：日期 → 天數（含基準日）、整修年 0 → 旗標 0 與有效年份 = 建造年、整修年 > 0 → 旗標 1、已知 zipcode → 對應 one-hot、未知 zipcode → 基準類別並回報警告旗標；預測 = 截距 + Σ 貢獻；All-in 的 k 固定；每個方法的 CV winner 與契約一致；`invalid` 項目不會被選為 winner。
- 前例：`week06/tests/core.test.js`（Node 內建 test runner，以 Python 匯出的 test 列為基準比對 JS 預測與 PI）。

### 次 seam：Python 套件公開函式

- 分割：train/test 無共同 `id`、聯集為全部列、同 seed 重現、比例近似 80/20；fold 兩兩無共同 `id`。
- 前處理：fit 後的類別與統計量只由訓練列決定（改動驗證列不改變它們）；未見類別編為基準；`sale_days` 與整修衍生欄的數值案例。
- 特徵選擇：在小型合成資料上，Forward／Backward／RFE 每步變動恰一個 group；Lasso 排序平手依 canonical order；p-value backward 只移除 p > 門檻的 group。
- 模型與推論：秩不足的語義各有案例，與「指標與推論」一節的 failure semantics 一致——(1) 合法 encoding：fold 訓練列缺少某類別時該 fold 的設計矩陣沒有該欄且 fit 成功；(2) 無效候選：人為使某欄在 fold 訓練列上為常數時該 (方法, k, fold) 標為無效、該 (方法, k) 為 `invalid` 且 CV winner 排除它；**非 winner 的 canonical subset 在整個 training set 上人為共線時，該 (方法, k) 為 `invalid`（`canonical_rank_deficient`）、沒有 `fit`、不被選為 winner，而其他有效候選的 CV 與 test 評估照常完成，不停止**；(3) 實驗層級失敗：All-in 在任一 fold 或整個 training set 上人為共線時、某方法全部候選無效時、或整體 winner 無法決定時，以錯誤停止並列出全部 invalid 候選。Adjusted R² 用實際秩；PI 公式以手算的小例子核對；coverage 計算以已知的上下界核對。
- 選擇邊界：在小型合成資料上，改動某 fold 驗證列的值不改變該 fold 的子集序列（fold-internal selection 只看訓練列，p-value backward 亦同）；canonical subset 只由整個 training set 決定。
- 選模：CV winner 的平手規則；授權評估集合的推導；test 評估函式在同一執行內第二次呼叫時報錯。
- 前例：`home_work_01` 的 pytest 配置與 CI workflow（本單元另設自己的 CI 路徑過濾）。

### 人工檢查表（ACCEPTANCE.md）

- Dashboard 必要區塊、zh-TW 無缺字、方法與 k 切換、比較全部、預測器輸入與警告（含未見 zipcode 的警告）、KPI／係數表／test 區塊的來源標示、test 區塊標示與不同模型提示、`invalid` 候選的標示、實際 vs 預測圖的可讀性與反應性檢查 (a)～(e)、離線（解壓、斷網、無伺服器、`file://`、零對外請求）、Pages URL。
- 報告：章節完整、三種標示、數字與匯出一致（抽查）、附錄 ChatGPT PDF、NotebookLM 摘要字數與可追溯性、主流解法來源連結可開啟。
- Repo：`git grep` 無實際學號；追蹤檔案不含 acceptor 材料、PDF、ZIP、`.env`。
- 乾淨環境重跑：新建虛擬環境、安裝、非互動執行 notebook、重跑測試、建置報告、打包；數字與追蹤的結果檔一致。

## Out of Scope

- 後端、API、資料庫、Vercel、MLOps。
- SelectKBest、permutation importance 作為特徵選擇、Exhaustive search；encoded column 層級的選擇。
- 刪除或截尾異常值；改用其他資料集；Kaggle 競賽名次。
- Ridge／Lasso 的預測區間與即時預測；對 Ridge／Lasso 或 CV 聚合值套用古典 Adjusted R²。
- 對全部 (方法, k) 做 test 評估。
- Conformal 或其他非參數式區間（Brief 選定參數式 OLS PI）。
- Wireframe 的製作（後續 `/ui-ux-pro-max` 步驟）、拆票（`/to-tickets`）、實作、push、merge、繳交。
- 修改 `week05/`、`week06/`、其他單元或 root 檔案（root README 與 CONTEXT-MAP 的一列除外，且須先說明）。

## Further Notes

- **Spec Review 的 acceptor 決定（2026-10-18）**：SR-06 ACCEPTED（Brief §1 已同步編輯為「四種具有 k=1…18 路徑的特徵選擇方法＋單一 All-in baseline」）；SR-09 ACCEPTED WITH CLARIFICATION（量測起訖、適用操作、紀錄要求與「不得以抽樣達標」已寫入 dashboard 一節）。SR-10～SR-12 的處理見 review record。
- **SR-01／SR-11 的成本影響**：fold-internal selection 使每個路徑方法與 p-value backward 的計算從 1 次變成 6 次（5 個 fold＋整個 training set）；這在 Brief Q34 的「量測並回報」義務內，不改變方法與 k 的範圍。

- 下一步工作流程（已確認、尚未授權執行）：`/ui-ux-pro-max` 依本 Spec 產生獨立的靜態 HTML wireframe → wireframe review → `/to-tickets` → implementation。Wireframe 不得改變本 Spec 的功能與統計要求。
- Brief 固定的驗收意圖中，與 UI 最相關的是 BR-01 的分層規則與 Q43 的逐筆 PI 圖；wireframe 需要明確呈現「訓練 CV」與「Test」兩層的視覺區分與提示文字。
- 風險：Backward SFS 與 RFE 的時間；`zipcode` 69 個 dummy 使係數表長、部分 fold 可能缺類別；逐筆 PI 線段的渲染效能。處理方式見 Brief §11。
- 合併進 `main` 不在本 Spec 的完成條件內：Brief 沒有 opt-in SA-3，合併屬 RB-1，由 acceptor 決定。
- 舊的 Issues #50–#56 來自已被取代的 r4 契約；它們的處置（關閉或改寫）會在 `/to-tickets` 前由 Design Authority 判定並回報，本 Spec 不沿用它們。
