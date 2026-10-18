# Outcome Contract v2 — HW2 Multiple Linear Regression（`home_work_02/`）

- **狀態**：**DRAFT r2（2026-10-18）。尚未接受，不具任何效力。**
- **取代**：DRAFT r1（commit `9547f687ef2a636051bdd0f681f5e8506c9a61dd`；檔案 blob `0e4808ecb7077a5f836fdd4a0c6bcf73ae14547f`，內容 sha256 `a578e7c71b3db87b77a24caa252386afdac92a5f4505e84676bfa9fc6c05f748`）。r1 未被接受；逐條變更見第 11 節。r2 依 acceptor 2026-10-18 對 U-1～U-5 的決定（第 12 節，逐字）與 r2 審閱要求修訂，**沒有重新開啟 Grill，也沒有改變 F-1～F-7 的裁決**。
- **定位**：本檔是 Outcome Contract r4（[`outcome-contract.md`](outcome-contract.md)）的**提議後繼契約**。要等 acceptor 依第 9 節完成有效接受，才會成為之後工作的 Outcome Contract。在那之前：
  - r4（ACCEPTED，normative 第 1–8 節 @ `e2153254ccf7a97475d1c22e10d6a1e0717c5497`，接受紀錄 @ `370c0ae1`）仍是 HW2 唯一已接受的 Outcome Contract；
  - 本檔不授權任何規劃、分解、實作、審查或合併。
- **不修改 r4**：r4 的檔案、內容、接受紀錄與 commit identifiers 保持原樣，作為歷史證據。Brief v0.3、Spec v1.1、derivation 與 decision records 也一樣。
- **依據**：
  - Minimal Operational Governance v2.2：§1.2（re-authorization）、§3.1 七項 properties、§5.3（contract change：本檔改變 r4 的 accepted 語義，屬第 1 類，須由 acceptor 重新接受）。
  - Project Bindings **b5**（`main` merge commit `5ebcc58eba1d776cc7380d391ced1dc503a3ee31`）：§2.2、§2.3、§2.4、§2.5（含 SA-3）、§2.6、§4、§5、§7。
- **來源紀錄**：
  - 老師來源：SRC-2 與其轉寫 SRC-2T（第 2.1 節）。
  - Grill Brief Draft v0.4（[`../brief/HW2_Grill_Brief_Draft_v0.4.md`](../brief/HW2_Grill_Brief_Draft_v0.4.md)）§0：acceptor 2026-10-18 的 F-1～F-7 最終裁決，逐字。
  - 需求重新基準化紀錄（[`../brief/HW2_Requirements_Rebaseline_2026-10-18.md`](../brief/HW2_Requirements_Rebaseline_2026-10-18.md)）：需求擷取 T-xx／S-xx 與衝突 X-x。
  - 歷史決定：G1–G8 原文、C1–C4（Brief v0.3 §3、§4）、C5（r4 §4.1）。
  - Brief 是討論紀錄，不具 authority；**本檔與 Brief 不一致時以本檔為準**。
- **撰寫者**：無角色主 session，依 acceptor 2026-10-18 指示「Continue the NCHU AIoT HW2 requirements re-baselining workflow」起草。起草不構成接受、授權或 Design Authority 裁決（治理 §2.7）。
- **Acceptor**：GitHub `yotsubamomo`（Bindings §2.1）。

**標記**：
- 「（沿用 r4）」表示該條語義與 r4 相同，只是重新陳述；
- 「（v2 新增）」或「（v2 修訂）」表示改變了 accepted 語義，逐條差異見第 10 節。

## 1. Intent and outcome

以 Kaggle 公開資料集 **House Sales in King County, USA** 完成一份遵循 CRISP-DM 六階段、可重現的多元線性回歸分析，預測房屋成交價 `price`。（沿用 r4）

- 在 Fit 分區上以 group-aware nested CV，公平比較 multiple LR baseline、forward／backward 特徵選擇的 LR、Ridge、Lasso；（沿用 r4）
- 凍結選出的 predictor，以獨立的 Calibration 分區產生 95% split conformal 預測區間；（沿用 r4）
- 只在未碰過的 Test 分區上做一次最終評估；（沿用 r4）
- 只以 Fit 衍生的資料：
  - 檢驗五個古典回歸假設的診斷面向；
  - 解釋凍結 predictor；
  - 在比較與 Test 報告中加入 Adjusted R²。（v2 新增，F-4～F-6）
- 依老師 2026-10-18 更新的作業頁（SRC-2），對特徵數採用正文與補充條件的交集；報告誠實區分三類內容：老師要求、依老師補充建議、專案延伸。（v2 新增，F-1、F-7）

交付 notebook（主程式）、支援模組與測試、報告 PDF、acceptor 提供的真實 ChatGPT 對話 PDF，以及以學號命名的 ZIP，滿足老師 HW2 的全部要求。（沿用 r4）

## 2. Scope and boundaries

### 2.1 上位契約（v2 修訂）

| ID | 檔案 | sha256 | 角色 |
| --- | --- | --- | --- |
| **SRC-2** | `home_work_02/doc/requirement/HW2-requirements-Multiple Linear regression.pdf`（iLearning 作業頁列印，2026-10-18 02:59，4 頁，1,083,106 bytes） | `1b3a5aad1c261425eb34f2eb46aebe6a62c73aba4fbf2d67a166fe9df28639d7` | **本契約的上位契約**。依 acceptor 2026-10-18 U-4 決定**不公開**：原始檔只保留在 acceptor 本機，由單元 `.gitignore` 排除（理由見 Delta record §1.1） |
| **SRC-2T** | `home_work_02/doc/requirement/HW2-requirements-Multiple Linear regression_SRC-2_2026-10-18.txt`（9,144 bytes；首次納入 commit `9547f687ef2a636051bdd0f681f5e8506c9a61dd`） | git blob `d185f89d5a3d923e24bb581eecd95481cfe2f335`；內容 sha256 `e5eb6a315dd5860e7562467012c748911454becb0c6bccde95823d1f0834e77c`（LF；Windows 工作目錄因 `core.autocrlf` 可能為 CRLF，以 blob 為準） | SRC-2 的忠實、標示頁碼的轉寫，是 git 中追蹤的副本。檔首記錄 SRC-2 的 sha256 與來源。SRC-2T 與 SRC-2 不一致時，以 SRC-2 為準；SRC-2T 的任何修改都受 RB-5 保護，並使上列識別失效 |
| SRC-1 | `home_work_02/doc/requirement/HW2-requirements-Multiple Linear regression.txt` | `a969e7e2228e97a35027ad63d3747f2e502bdd685cf7cfca30aaab50048761ab`（git blob） | 歷史基準（r4 的上位契約），保持原樣。正文與 SRC-2 相同，差別只有「已缴交」人數 |

- 上位契約對所有 Agent 唯讀（Bindings §2.2）；之後任何修改都受 RB-5 保護。
- SRC-2 的「==== 補充 ====」段（SRC-2T p.2–p.4）是老師貼上的 LLM 回答。它的規範力依原文措辭判斷：
  - 特徵數條件依 F-1 處理（第 2.4.1 節）；
  - 其餘內容維持「建議」的分類，**不重新分類為老師要求**（F-1）。
- 採用的建議項目在報告中標為「依老師補充建議」（第 2.4.6 節）。

### 2.2 Scope classes（Bindings §2.4）

**MVM 必須完整滿足上位契約**。ENHANCED 是 acceptor 授權、超出老師要求的範圍：必須維持標示，且不得取代、弱化或被呈現為老師要求的行為。（沿用 r4）

「報告標示」欄是第 2.4.6 節的三種標示，與 scope class 是不同的維度：
- scope class 決定契約義務；
- 報告標示決定報告如何陳述它和老師文件的關係。

| Class | 項目 | 依據 | 報告標示 |
| --- | --- | --- | --- |
| **MVM REQUIRED** | M1 Kaggle 公開資料集；source features 數量落在 **14–20**（第 2.4.1 節的計數規則）；標明名稱與來源連結；報告說明兩條原文與採用的解讀（**v2 修訂**） | T-02、T-04；S-01／S-02；F-1 | 老師要求（10–20 與來源連結）；14–39 的補充條件以「依老師補充建議」說明 |
| | M2 以線性回歸預測；執行特徵選擇與模型評估 | T-05、T-07 | 老師要求 |
| | M3 預測圖，附預測區間（老師允許信賴區間或預測區間；本契約選預測區間） | T-08 | 老師要求 |
| | M4 CRISP-DM 六階段，notebook 與報告皆涵蓋 | T-09、T-14 | 老師要求 |
| | M5 acceptor 與 **ChatGPT** 進行的、與本作業相關的真實對話，以 pdfCrowd 或其他方式匯出為 PDF | T-10 | 老師要求 |
| | M6 以 NotebookLM 研究網路上同主題的解法，報告中放 100 字以上的摘要，標示「NotebookLM 摘要」 | T-11、T-12 | 老師要求 |
| | M7 報告中明確標示「GPT 輔助內容」 | T-12 | 老師要求 |
| | M8 報告比較並說明網路上主流或更優的解法 | T-14 | 老師要求 |
| | M9 主程式 `<學號>_hw2.ipynb`（或 `.py`）與報告 PDF，壓縮為 `<學號>_hw2.zip` | T-13、T-15 | 老師要求 |
| | M10 使用 GitHub（G7），因此提供連結，並在 `home_work_02/README.md` 整理流程與成果 | T-16（optional 條款，因 G7 成為必要） | 老師要求（條件式條款） |
| **ENHANCED REQUIRED**（acceptor 授權） | E1 比較範圍：multiple LR baseline、forward LR、backward LR、Ridge、Lasso（**不新增**其他候選，F-3） | G1；F-3 | **逐項標示，不整體歸類**（第 2.4.6 節表 A；**r2 修訂**，U-2）。摘要如下：<br>• 線性回歸與執行特徵選擇的義務：老師要求（M2）；<br>• Ridge、Lasso：依老師補充建議（S-08d；Lasso 亦見 S-09）；<br>• forward／backward 所屬的方法族 Sequential Feature Selection：依老師補充建議（S-09）；<br>• group 層級、以 inner CV 選 k 的具體程序：專案延伸；<br>• 把五者作為 candidate procedures 比較：專案延伸 |
| | E2 60／20／20 Fit／Calibration／Test 分區，Development＝Fit＋Calibration，所有選模與 CV 只在 Fit 內進行 | G2、G4、C1 | 專案延伸 |
| | E3 依 house `id` 做 group-aware 分區與 CV | C2；F-2 | 專案延伸 |
| | E4 所有候選用同一組 outer 5-fold 比較，inner CV 選特徵數與 hyperparameter；以 USD 的 outer-CV RMSE 排序，另報 R²、MAE、MSE（以及 E11 的 Adjusted R²） | G2、C3、C4；F-3 | 專案延伸 |
| | E5 以 log(price) 訓練；評估指標以 USD 報告 | C4 | 專案延伸 |
| | E6 95% split conformal 預測區間：在 log 尺度校準、轉回 USD；報告 Test 實測 coverage 與平均寬度 | G3、C4 | 專案延伸（預測區間本身屬 M3「老師要求」） |
| | E7 模組化 Python（data、selection、modeling、evaluation、conformal），notebook 為主程式 | G5 | 專案延伸 |
| | E8 驗證：模組測試、leakage 測試、conformal 計算驗證、notebook 完整重跑、繳交文件檢查；以及 E10～E12 的對應驗證 | G8；F-4～F-6 | 專案延伸 |
| | E9 資料以 CSV sha256 固定版本（第 5 節）；依 CC0-1.0 可隨繳交附上 | Brief v0.3 §10；F-2 | 專案延伸 |
| | **E10 五個回歸假設的診斷面向**（第 2.4.3 節）（**v2 新增**） | S-08f；F-4 | 檢驗假設：依老師補充建議（S-08f）。只用 Fit、在 log 尺度上分析、與 conformal 假設分開陳述的規則：專案延伸（**r2 修訂**） |
| | **E11 Adjusted R²**（第 2.4.4 節）（**v2 新增**） | S-08e；F-5 | 指標本身：依老師補充建議（S-08e）。DA 定義的 n／p 慣例與適用性：專案延伸（**r2 修訂**） |
| | **E12 凍結 predictor 的解釋**（第 2.4.5 節）（**v2 新增**） | S-08g；F-6 | 解釋模型：依老師補充建議（S-08g）。以 permutation importance 作為解釋工具，是本專案對它的用法（S-09 把它列為特徵選擇方法）：專案延伸 |
| | **E13 三種報告標示**（第 2.4.6 節）（**v2 新增**） | F-7 #8、#9；U-2 | —（標示規則本身） |
| **OPTIONAL** | 其他候選模型的區間；E10 之外的額外診斷圖（只用 Fit） | Brief v0.3 §5.4；Spec v1.1 R-EVAL-4 | 專案延伸 |
| **REFERENCE** | `week05/multiple_linear_regression_crisp_dm.ipynb` 與 `week05/docs/` 課程講義；`week06/` DIC-02 的特徵選擇比較；NotebookLM 或網路研究找到的他人解法；SRC-2 補充段推薦、但未採用的資料集與方法 | G5；T-11；F-2、F-3 | — |

### 2.3 Non-scope（明確排除）

- Web App、FastAPI、資料庫、完整 MLOps、強制比較非線性或深度學習模型。（沿用 r4）
- Kaggle 名次：本資料集沒有競賽排行榜，老師條款寫「若有」。（沿用 r4）
- Auto Regression：資料是截面的房屋交易，不是時間序列，老師條款為「可嘗試」。（沿用 r4）
- 任何捏造的研究或對話證據，包括由 Agent 產生的 ChatGPT 對話、NotebookLM 研究或其摘要內容（第 2.5.1 節）。（沿用 r4）
- 以 Claude 的對話紀錄或任何非 ChatGPT、與本作業無關的對話，替代 M5 的 ChatGPT 對話 PDF。（沿用 r4）
- 新的 conformal 演算法：第 2.4.2 節之外的方法都是設計變更，須另經 acceptor。（沿用 r4）
- 修改 `week05/`、`week06/`、其他單元或 root 檔案（RB-5）。（沿用 r4，加列 `week06/`）
- 把 week05 的參考實作行為當成老師要求，例如 p-value backward elimination、在選模迴圈中列印 Test RMSE、以全部資料重訓。（沿用 r4）
- **（v2 新增）** 改用 SRC-2 推薦清單中的資料集（Predict the Flood 等）。（F-2）
- **（v2 新增）** 新增 SelectKBest、RFE，或以 permutation importance 進行特徵選擇的候選；在 encoded column 層級做特徵選擇；實作補充段列出的每一種方法，或其建議的 k 值（14、20、25、30）。（F-3）
- **（v2 新增）** 以 S-04 的「選擇後」特徵數讀法判斷 M1。（F-1）
- **（v2 新增）** 以 Adjusted R² 作為選模、排序或 tie-break 的依據。（F-5）
- **（v2 新增）** 以 Calibration 或 Test 的觀測做假設診斷、模型解釋或任何設計決定。（F-4、F-6）
- **（v2 新增）** 因果解讀：係數與 permutation importance 不得被陳述為因果效果。（F-6）

### 2.4 Accepted 語義（Spec 在此邊界內 derive AC）

#### 2.4.1 資料、分區與選模

- **資料**（沿用 r4；F-2）：
  - 資料為 Kaggle `harlfoxem/housesalesprediction` 的 `kc_house_data.csv`；target 為 `price`；
  - CSV sha256 固定為 `d0875baa0251b21d4bdc9d2ae940a4fe0bb6009824f23dd0e2a5b2bf04557b7e`；
  - 來源、授權（CC0-1.0）與核對證據沿用 Brief v0.3 §10。
- **特徵計數**（**v2 修訂**；F-1）：
  - 「特徵」指 **source feature**：原始 CSV 中扣除識別碼 `id` 與目標 `price` 的欄位，在類別編碼**之前**計數；encode 後的欄位不計。
  - 依此規則有 **19** 個 source features；建模使用的 source-feature groups 為 **18** 個。
  - 採用的限制是**老師正文「10 至 20 個特徵」與補充條件「> 13, < 40」（14–39 個輸入特徵，不含 target）的交集，即 14–20 個 source features**。19 落在其中。這個限制只針對 source feature 數；建模 group 數（18）是陳述的事實，不另設限制。
  - 報告與 notebook MUST 引用兩條原文（T-02；S-01、S-02），說明採用交集與上述計數方式的理由，並說明補充段 S-04 的「選擇後符合」讀法不被採用。
- **分區與隔離**（E2、E3，沿用 r4）：
  - 以固定 seed、以整棟房屋為單位，隨機分成 Fit／Calibration／Test，三者沒有共同的 `id`；
  - 所有有參數的前處理、特徵選擇與 hyperparameter 搜尋，只在當次訓練 fold 的列上 fit；
  - Calibration 只用來計算凍結 predictor 的 conformal quantile；
  - Test 在 predictor 凍結後只評估一次；
  - **（v2 新增）** E10 的診斷與 E12 的解釋只使用 Fit 衍生的資料。
- **比較與選模**（E1、E4、E5，沿用 r4；F-3）：
  - 每個候選是一個 candidate procedure（前處理＋選擇＋fit）；
  - 特徵選擇以 **source-feature group** 為單位，只在 Fit 內進行；
  - 所有候選使用同一組 group-aware outer 5-fold，inner CV 選特徵數與 hyperparameter；
  - 依 USD 的平均 outer-fold RMSE 排序並選出勝出者，tie-break 沿用已接受的決定；
  - 選出的 procedure 在整個 Fit 上重跑，產生凍結 predictor，之後才進行 calibration。
- **偏誤陳述**（沿用 r4）：
  - 每個候選的 outer-CV 分數，估計的是該 procedure 的表現；
  - 從多個候選中取最小者，會使勝出者的 outer-CV 分數產生**樂觀偏誤**；
  - 凍結 predictor 表現的獨立估計是 Test 評估；
  - 報告不得把勝出者的 outer-CV 分數寫成不偏估計，也須說明凍結 predictor 是在整個 Fit 上重訓的。
- **凍結 predictor 與「每次執行只做一次 Test 評估」**：依 acceptor 2026-10-18 Part C 的保留清單，提升為本契約的 accepted 語義。內容取自 r4 下的 derived contract Spec v1.1 R-SEL-3、R-SEL-4、R-EVAL-1a：
  - 凍結 predictor 在任何 Calibration 或 Test 預測之前固定並記錄其識別；
  - **每次執行**（從分區開始的一次完整流程）恰有一次 Test 評估，在凍結與校準之後；
  - Test 的結果不回饋任何設計或實作決定；
  - 以同一套固定設計重複執行（重現、乾淨環境重跑、解壓驗證）是重現，不是新的評估；
  - 報告的 Test 數值只來自最終驗證執行，不得比較多次執行的 Test 結果並從中挑選。
  - 具體的 manifest、事件與 worklog 要求屬 Spec，由 DA derive。
- **補充段的方法清單**（F-3）：報告 MUST 說明 S-09 的方法清單是建議，不是要求實作其中每一種方法。

#### 2.4.2 Conformal 預測區間（E6）（沿用 r4，未變更）

**方法**（保留 G3、C4，不變）：
- 分數為 Calibration 每一筆交易的 s = |log y − log ŷ|；
- q̂ 取第 ⌈(n_cal+1)(1−α)⌉ 小的分數，α = 0.05；
- USD 區間為 [ŷ·e^(−q̂), ŷ·e^(q̂)]；
- 報告 Test 的實測 coverage 與平均寬度（USD）。

報告必須分開陳述三件事，且不得混為一談：

| 層次 | 內容 |
| --- | --- |
| **Nominal target coverage** | 1 − α = 95%。這是方法的設計參數，不是結果。 |
| **理論保證與其假設** | 若在 Fit 訓練出的 predictor 固定下，Calibration 的分數與一筆新的 Test 交易的分數是 **exchangeable**，則 P(Y ∈ C(X)) ≥ 95%（**marginal**：對 Calibration 與該筆 Test 交易的抽樣平均，不是對特徵值、價格區間或地區的條件保證）；分數沒有 ties 時，上界為 95% + 1/(n_cal+1)。<br>**這個 exchangeability 是假設，不是本設計已證明的性質。**<br>Group-aware 分區只防止同一房屋的交易跨越分區；整棟房屋的隨機分派是與此假設相容的設計措施，但兩者都**不能單獨證明交易層級分數的 exchangeability**：同一房屋的多筆交易彼此相依（177 筆重複交易），各房屋的交易筆數不同，且任何系統性差異都可能破壞此假設。<br>即使假設成立，保證也只適用於本資料集（2014-05～2015-05）中被保留的交易，不延伸到之後的交易、其他地區或市場變化。 |
| **Observed coverage** | Test 交易落在其區間內的比例。這是單次分區的實證估計，有抽樣誤差（n_test 約 4,300 時約 ±0.7 個百分點），本身不證明也不否定理論保證。報告須同時列出 n_test 與平均寬度。 |

- **log 與 exp 轉換**：exp 為單調函數，「落在區間內」這個事件在 log 尺度與 USD 尺度上相同，所以實測 coverage 在兩個尺度上相等，理論陳述也同樣適用。
- **未採用的替代設計**（只是記錄，**不屬本契約**）：以房屋為單位的 conformal（例如每棟房屋只取一筆校準分數），可以更直接對應 group 結構。採用它是 conformal 設計變更，須另經 acceptor 接受。

#### 2.4.3 五個回歸假設的診斷面向（E10）（v2 新增；F-4）

- **涵蓋五個面向**：
  1. 線性（linearity）；
  2. 誤差獨立（error independence）；
  3. 同質變異（homoscedasticity）；
  4. 殘差常態（residual normality）；
  5. 多重共線性（multicollinearity）。
- **資料**：只使用 Fit 衍生的資料。Calibration 與 Test 的觀測 MUST NOT 用於診斷，也 MUST NOT 用於因診斷而作的任何設計決定。
- **尺度**：殘差行為在模型的 **log(price) 尺度**上分析。
- **證據**：每個面向都有適當的數值或圖形證據，以及解讀。
- **違反的語義**：診斷偵測到的違反是要報告並解釋的發現，**不是作業的自動 FAIL**，也不使任何候選或凍結 predictor 失效。
- **兩類假設必須分開陳述**：
  - 古典回歸假設：上列五項，關係到 OLS 推論與係數解讀；
  - split conformal 預測區間所依賴的假設：第 2.4.2 節的 exchangeability。
  - 報告不得暗示五項診斷驗證了 exchangeability，也不得把 conformal 區間的有效性寫成依賴常態或同質變異。
- **交給 Design Authority**：具體的診斷方法、統計量、所用的 Fit 衍生殘差（例如 outer-fold 的 out-of-fold 殘差，或凍結 predictor 在 Fit 上的殘差），以及驗證準則。

#### 2.4.4 Adjusted R²（E11）（v2 新增；F-5）

- 在適用的 outer-CV 比較與 Test 報告中，加入 Adjusted R²。
- Adjusted R² 是對同一表中 R² 的調整；R² 依 C4 的尺度計算。
- **Design Authority 必須在 Spec 中定義**：
  - 樣本數與參數數的慣例；
  - 對 OLS、forward／backward subset 模型、Ridge、Lasso 的適用性；
  - 模型複雜度或有效自由度的處理方式；
  - 跨模型比較與解讀的限制。
- 本契約**不預先固定** p 的定義（例如不固定為非零係數數）。
- DA 判定某個候選不適用時，報告標示「不適用」並寫明理由，不寫數值。
- **不改變選模準則**：outer-CV 的平均 USD RMSE 仍是唯一的選模依據（第 2.4.1 節）；Adjusted R² 只是報告的指標。

#### 2.4.5 凍結 predictor 的解釋（E12，Deployment 階段）（v2 新增；F-6）

Deployment 章節 MUST 包含：
- **凍結 predictor 的解讀**；
- **係數**：在 log(price) 尺度上的適當解讀，考慮標準化與類別編碼（例如標準化後係數的單位，以及 one-hot 欄相對於基準類別的意義）；
- **Permutation importance**：只以 Fit 計算，作為**解釋工具**。它**不是**特徵選擇的候選，也不改變凍結 predictor；
- **預測新樣本**：沿用 r4 的示範（Deployment 章節以人工建構的範例或 Fit 的列示範預測函式，回傳點預測與區間）；
- **模型限制與因果解讀的提醒**：係數與 importance 描述的是模型中的關聯，不是因果效果；並陳述資料範圍的使用限制（King County、2014-05～2015-05、外推、第 2.4.2 節的 marginal coverage 與 exchangeability 假設）。

解釋 MUST NOT 使用 Calibration 或 Test。

#### 2.4.6 報告的三種標示（E13）（v2 新增；F-7 #8、#9；r2 依 U-2 修訂）

報告的做法與內容，依第 2.2 節「報告標示」欄與下方表 A，標為以下三種之一：

| 標示 | 意義 | 來源 |
| --- | --- | --- |
| **老師要求** | 老師正文的要求（mandatory teacher requirement） | SRC-2 正文（＝SRC-1） |
| **依老師補充建議** | 採用的補充段建議（adopted supplemental suggestion） | SRC-2 補充段 |
| **專案延伸** | 本專案自行定義的延伸（project-defined enhancement） | acceptor 授權的 ENHANCED |

**分類的單位是方法或義務，不是候選或章節的整體**（U-2）。同一個候選可以同時含有不同來源的成分；五個候選 MUST NOT 被整體歸為「依老師補充建議」。

**表 A — 方法與義務的來源對照**（r2 新增）

| 方法或義務 | 標示 | 依據 |
| --- | --- | --- |
| 以線性回歸（Linear Regression）預測；多元線性回歸的完整分析 | 老師要求 | T-01、T-05 |
| 執行特徵選擇（Feature Selection）與模型評估（Model Evaluation） | 老師要求 | T-07 |
| 預測圖附區間（老師允許信賴區間或預測區間；選擇預測區間屬專案的選擇，方法見下方 conformal 列） | 老師要求 | T-08 |
| CRISP-DM 六階段；資料集來源與連結；10–20 個特徵 | 老師要求 | T-02、T-04、T-09 |
| 特徵數 14–39 的補充條件（與正文取交集為 14–20） | 依老師補充建議 | S-01、S-02；F-1 |
| Ridge、Lasso | 依老師補充建議 | S-08d（Lasso 亦見 S-09） |
| Sequential Feature Selection（forward／backward 所屬的方法族） | 依老師補充建議 | S-09 |
| MAE、MSE、RMSE、R² 的比較 | 依老師補充建議 | S-08e（「模型評估」本身是老師要求） |
| Adjusted R² | 依老師補充建議 | S-08e |
| 檢驗五大回歸假設 | 依老師補充建議 | S-08f |
| 預測新樣本、解釋模型 | 依老師補充建議 | S-08g |
| 五個 candidate procedures 的組成與比較方式（C1 全 group OLS、group 層級的 forward／backward、inner CV 選 k 與 `alpha`、tie-break、在 Fit 上重訓） | 專案延伸 | G1、C3；F-3 |
| 60／20／20 分區、group-aware（house `id`）分區與 CV、nested CV、以 USD outer-CV RMSE 選模、偏誤陳述 | 專案延伸 | G2、G4、C1～C4 |
| log(price) 目標與 USD 指標 | 專案延伸 | C4 |
| 95% split conformal（校準、區間、coverage 陳述）；凍結 predictor 與每次執行單次 Test 評估 | 專案延伸 | G3、C4 |
| E10 的 Fit-only 與 log 尺度規則；E11 的 n／p 慣例；E12 以 permutation importance 作為解釋工具 | 專案延伸 | F-4～F-6 |
| 模組化程式、測試、checksum、重跑驗證 | 專案延伸 | G5、G8、E9 |

**標示的粒度**（r2 新增）：
- 報告以**方法／要求對照表**（例如報告中的一張表 A 對照），或**章節層級的標示**，就足以滿足 E13。
- 不要求逐句或逐行重複標示。
- 一個章節同時含不同來源的內容時，該章節的標示或對照表 MUST 能讓讀者分辨各方法或義務的來源。

**其他規則**：
- 補充段的建議 MUST NOT 被寫成老師要求。
- 未採用的建議，例如推薦資料集、SelectKBest、RFE、建議的 k 值，不得寫成已完成；報告可以說明未採用的理由。

### 2.5 Constraints（沿用 r4）

- MVM 必須完整滿足上位契約；ENHANCED 項目在報告中不得被寫成老師要求。
- 資料版本以 CSV sha256 固定；改用不同檔案是 re-pin，須記錄。
- 不使用任何憑證；資料下載只用匿名公開端點，或本機已固定的副本（RB-3）。
- 報告與 notebook 的語言：**zh-TW**；技術名詞與程式識別字可保留英文。

#### 2.5.1 AI 研究與對話證據（沿用 r4，未變更）

| 證據 | 允許 | 禁止 |
| --- | --- | --- |
| ChatGPT 對話 PDF（M5） | 使用 acceptor 本人與 ChatGPT 進行、與 HW2 相關的真實對話，以 pdfCrowd 或等效方式匯出；acceptor 可決定要遮蔽的個人資訊，並在 PDF 或報告中註明遮蔽 | Agent 產生、改寫或補造任何對話內容；以 Claude 或其他工具的對話紀錄、或與本作業無關的對話，替代 ChatGPT 對話 |
| NotebookLM 研究（M6） | acceptor 在 NotebookLM 進行研究並提供原始材料（NotebookLM 的輸出、來源清單）。Agent 可以**忠實地編輯**這些材料：排版、修正錯字、摘錄、翻譯、縮寫成 ≥100 字的摘要。摘要必須可追溯到原始材料與來源連結；經整理的部分在報告中註明「依 NotebookLM 研究整理」 | 加入原始材料沒有的論點或來源；在沒有原始材料時撰寫摘要；把 Agent 自己的網路研究冒充為 NotebookLM 的結果 |
| 主流或更優解法的比較（M8） | 可以由 Agent 依可查證的公開來源撰寫並附連結；若引用 NotebookLM 材料則依上列規則 | 無來源的主張 |
| 「GPT 輔助內容」標示（M7） | 沿用老師的標示名稱；同時如實揭露實際使用的工具，包括 ChatGPT 與 Claude Code。Claude Code 的使用可以在報告中揭露，作為補充說明 | 把 Claude 的產出寫成 ChatGPT 的產出；以揭露說明替代 M5 的 ChatGPT PDF |

原始材料（NotebookLM 輸出與來源清單、ChatGPT PDF）由 acceptor 提供並保留，報告中的摘要與引用可對回原始材料。這些材料是否放進公開的 Git repository 由 acceptor 決定；放進 ZIP 則是 M5、M9 的要求。

## 3. Acceptance boundary

### 3.1 Acceptance criteria（可觀察的 PASS／FAIL 與證據）

Spec 的具體 AC 由 Design Authority 在本邊界內 derive，並在 derivation record 載明各 Spec 分配到的部分。OC-A1～OC-A8 沿用 r4 的編號；標「v2 修訂」者改變了 PASS／FAIL；OC-A9～OC-A12 是 v2 新增。

| ID | 類別 | PASS | FAIL | 證據要求 |
| --- | --- | --- | --- | --- |
| OC-A1 資料集（**v2 修訂**） | MVM | 報告與 notebook 載明資料集名稱、Kaggle 連結、授權；載入的 CSV sha256 等於固定值，或另有 re-pin 紀錄；以第 2.4.1 節規則陳述 source feature 數量（19，須落在 **14–20**），並陳述建模使用的 group 數量（18）；報告引用 T-02 與 S-01／S-02 兩條原文，並說明採用交集與計數方式的理由 | 缺來源或連結；checksum 不符且無 re-pin 紀錄；以 encode 後的欄位或選擇後的特徵計數；數量不在 14–20；缺兩條原文或採用解讀的說明 | notebook 輸出的 checksum 與欄位清單；報告的資料說明節 |
| OC-A2 CRISP-DM（沿用 r4） | MVM | notebook 與報告各有六個階段的明確章節，內容對應各階段 | 缺任一階段，或只有標題沒有內容 | 章節清單比對 |
| OC-A3 隔離（**v2 修訂**） | ENHANCED | 自動化測試證明：三個分區沒有共同的 `id`，合起來涵蓋全部列；每個 CV fold 的訓練列與驗證列沒有共同的 `id`；有參數的前處理與特徵選擇只以訓練 fold 的列 fit；凍結 predictor 的識別（例如檔案 hash）在 Test 評估之前已記錄；**E10 診斷與 E12 解釋（含 permutation importance）的計算只接收 Fit 衍生的資料** | 任一測試失敗或不存在；Test 或 Calibration 在凍結前被用於任何選擇；Test 或 Calibration 被用於診斷或解釋 | 測試輸出；凍結 predictor 的識別與 Test 評估的順序 |
| OC-A4 比較與選模（**v2 修訂**） | MVM（M2）＋ENHANCED（E1、E4、E5、E11） | 五個候選（且只有這五個）都在同一組 outer folds 上有 USD RMSE（另附 R²、MAE、MSE）；特徵數與 `alpha` 由 inner CV 決定；選擇規則與 tie-break 有文件；報告含第 2.4.1 節的偏誤陳述；凍結 predictor 有 Test 的 R²、MAE、MSE、RMSE（USD）；報告說明 S-09 的方法清單是建議 | 缺任一候選；folds 不一致；以 p-value、Test 或 Adjusted R² 選模；把勝出者的 outer-CV 分數寫成不偏估計；新增第 2.3 節排除的候選 | 比較表、選擇紀錄、Test 指標表 |
| OC-A5 預測區間（沿用 r4） | MVM（M3）＋ENHANCED（E6） | 有預測圖（實際 vs 預測，附上下界，USD）；conformal quantile 與 coverage 的計算由獨立測試重算且一致；報告分開陳述 nominal target、理論保證及其 exchangeability 假設、observed coverage（含 n_test 與平均寬度），措辭不超過第 2.4.2 節 | 沒有預測圖或區間；計算與獨立重算不一致；陳述理論保證時沒有寫出 exchangeability 假設；把 group-aware 分區或隨機分派寫成已證明 exchangeability；把 observed coverage 寫成保證的證明 | 圖、測試輸出、報告的區間說明節 |
| OC-A6 可重現（沿用 r4；涵蓋 E10～E12） | ENHANCED（E7、E8、E9） | 固定 seed 與相依版本；README 有重跑步驟；從乾淨環境完整重跑 notebook 成功，重跑的數值（含 E10～E12 的數值）與報告一致；模組測試全部通過 | 重跑失敗；數值與報告不一致；測試失敗 | 重跑紀錄、測試輸出 |
| OC-A7 AI 協助與研究（沿用 r4） | MVM（M5–M8） | 符合第 2.5.1 節：報告有「GPT 輔助內容」標示並揭露實際使用的工具；「NotebookLM 摘要」≥ 100 字，可追溯到 acceptor 提供的 NotebookLM 原始材料，經整理處有註明；有附來源的主流或更優解法比較；acceptor 提供的 ChatGPT 對話 PDF 已納入 | 缺任一項；任何對話或研究內容是捏造的；摘要含原始材料沒有的內容；以 Claude 紀錄或無關對話替代 ChatGPT PDF | 報告節次；acceptor 提供的原始材料；摘要與原始材料的對照 |
| OC-A8 繳交套件（沿用 r4） | MVM（M9、M10） | ZIP `<學號>_hw2.zip` 內含 `<學號>_hw2.ipynb`、報告 PDF、ChatGPT 對話 PDF、支援模組、requirements、資料（或取得方式）；檔名用 acceptor 提供的實際學號；`home_work_02/README.md` 有流程、成果與 GitHub 連結（指向 `yotsubamomo/aiot-classwork` 的 `home_work_02/`）；ZIP 的 sha256 與檔案清單已記錄；追蹤檔案中沒有秘密 | 學號仍是佔位；缺必要檔案；README 缺流程、成果或連結 | ZIP 檔案清單與 sha256、README |
| **OC-A9 回歸假設診斷**（v2 新增） | ENHANCED（E10） | notebook 與報告對五個面向（線性、誤差獨立、同質變異、殘差常態、多重共線性）各有數值或圖形證據與解讀；寫明所用的資料是 Fit 衍生的，殘差在 log(price) 尺度；偵測到的違反有說明；報告有一節分開陳述古典回歸假設與 split conformal 所依賴的 exchangeability 假設 | 缺任一面向，或只有圖沒有解讀；使用 Calibration 或 Test；把違反寫成作業失敗或隱藏違反；暗示五項診斷驗證了 exchangeability，或把 conformal 區間的有效性寫成依賴常態或同質變異 | notebook 輸出與圖；報告的診斷節；OC-A3 的隔離測試 |
| **OC-A10 Adjusted R²**（v2 新增） | ENHANCED（E11） | 每個候選在 outer-CV 比較表中有 Adjusted R²，凍結 predictor 在 Test 指標表中有 Adjusted R²，或依 DA 的定義標示「不適用」並寫明理由；notebook 與報告寫明 DA 定義的 n 與 p 慣例、各類模型的適用性、複雜度的處理與比較限制；數值與獨立重算一致；選擇紀錄顯示選模只依 outer-CV 平均 USD RMSE | 缺數值且沒有「不適用」的理由；定義未寫明；與獨立重算不一致；Adjusted R² 影響選模或 tie-break | 比較表、Test 指標表、選擇紀錄、測試輸出 |
| **OC-A11 模型解釋**（v2 新增） | ENHANCED（E12） | Deployment 章節（notebook 與報告）有：凍結 predictor 的解讀；係數在 log(price) 尺度的解讀，含標準化與類別編碼的說明；只以 Fit 計算的 permutation importance，寫明所用的資料與指標；預測新樣本的示範（點預測與區間）；模型限制與「非因果」的提醒 | 缺任一項；使用 Calibration 或 Test；把係數或 importance 寫成因果效果；以 permutation importance 選特徵或改變凍結 predictor | notebook 輸出；報告的 Deployment 節；OC-A3 的隔離測試 |
| **OC-A12 來源與標示**（v2 新增；**r2 修訂**） | MVM（AC 的誠實性）＋ENHANCED（E13） | 報告以方法／要求對照表或章節層級標示，使用三種標示，且與第 2.4.6 節表 A 一致；五個候選沒有被整體歸為單一來源；每個「依老師補充建議」項目可對回 SRC-2 補充段的原文；正文沒有把補充段的建議或 ENHANCED 做法寫成「老師要求」；未採用的建議沒有被寫成已完成 | 把建議寫成老師要求；標示與表 A 不符；五個候選被整體歸類；缺標示，或讀者無法從對照表或章節標示分辨各方法的來源 | 報告的對照表或章節標示；Reviewer 逐項核對表 A（不要求逐句標示） |

### 3.2 完成狀態（區分實作、發布與繳交）（沿用 r4；S1 加入 OC-A9～A12）

| 狀態 | 意義 | 由誰完成 | 證據 | 與其他工作的關係 |
| --- | --- | --- | --- | --- |
| **S1 實作就緒** | OC-A1～A6、OC-A9～A12 PASS；報告中除了 acceptor 證據外的內容完成，待填位置清楚標示 | Agents | 各 AC 的證據 | 不需要等任何 acceptor 輸入 |
| **S2 繳交套件就緒** | OC-A7、OC-A8 也 PASS：acceptor 證據與學號已納入，ZIP 已組好並核對 | Agents（取得 acceptor 輸入後） | ZIP sha256、檔案清單、README | 只受第 3.3 節的 acceptor 輸入影響 |
| **S3 GitHub 已發布** | 內容已合併進 `main`，README 的連結可以開啟 | 依第 4.2 節：在 SA-3 條件下由 Orchestrator（Formal）或 direct-execution Executor（Lightweight）合併；否則由 acceptor（RB-1） | Bindings b5 §7 的 Merge record：合併前的 gate 證據在 run record 或 worklog；merge commit SHA 與合併後驗證結果在該 PR 的 comment；連結可開啟的確認 | 不阻擋 S1、S2 |
| **S4 iLearning 已繳交** | ZIP 已上傳到 iLearning | **Acceptor**（RB-2；G8） | acceptor 提供的繳交確認（日期與所上傳 ZIP 的 sha256 或檔名），記入 worklog | 不阻擋 S1、S2 |

- **本 Outcome Contract 的 work item 完成 = S2。** S3、S4 分別記錄，不屬於 Agent 工作的完成條件。Agent 只能記錄實際發生、且有上述證據的 S3、S4，不得宣稱未發生的 S3、S4。
- S2 的 ZIP sha256 與檔案清單，在 S4 時用來核對所繳交的檔案就是驗證過的那一份。
- 等待 acceptor 動作（S3、S4 或第 3.3 節的輸入）只停止受影響的 AC，其他實作與驗證照常進行（治理 §1.5）。

### 3.3 只能由 acceptor 提供的輸入（沿用 r4）

| 輸入 | 對應 | 說明 |
| --- | --- | --- |
| ChatGPT 對話 PDF | OC-A7、OC-A8 | 第 2.5.1 節 |
| NotebookLM 原始研究材料（輸出與來源清單） | OC-A7 | 第 2.5.1 節 |
| 學號 | OC-A8 | 打包前提供 |
| S4 繳交（S3 依第 4.2 節，不需要 acceptor 輸入，除非 SA-3 條件不成立而回到 RB-1） | 第 3.2 節 | RB-2；RB-1（第 4.2 節） |

在這些輸入提供前，Agent 完成其餘全部工作，並在報告中保留標示清楚的待填位置，不得以範例文字冒充內容。缺少輸入屬治理 §1.5 第 4 項的 boundary：只停止受影響的 AC。

### 3.4 Failure semantics

- 下列**不是** FAIL：
  - R²、Adjusted R²、RMSE 未達任何門檻（本契約沒有效能門檻）；
  - observed coverage 不等於 95%；
  - 選出的模型是全特徵 LR；
  - Lasso 把某些特徵係數壓為 0；
  - **（v2 新增）** E10 的診斷偵測到任何假設違反（須報告並解釋）；
  - **（v2 新增）** DA 判定 Adjusted R² 對某個候選不適用並寫明理由；
  - S3、S4 尚未發生。
- 下列一律是 FAIL：
  - 資料洩漏（OC-A3）；
  - 以 Test 或 Calibration 選模；
  - **（v2 新增）** 以 Test 或 Calibration 做假設診斷、模型解釋或任何設計決定；
  - **（v2 新增）** 以 Adjusted R² 選模或 tie-break；
  - 計算與獨立重算不一致；
  - 捏造或替代證據（第 2.5.1 節）；
  - 陳述 conformal 保證時沒有寫出 exchangeability 假設，或聲稱它已被證明；
  - 把 ENHANCED 寫成老師要求；**（v2 新增）** 把補充段的建議寫成老師要求；
  - **（v2 新增）** 把係數或 permutation importance 陳述為因果效果；
  - 學號佔位進入最終 ZIP；
  - Agent 宣稱未實際發生的 S3、S4；
  - 不符合 Bindings b5 SA-3 條件、也沒有 acceptor RB-1 授權的合併進 `main`。
- Observed coverage 明顯偏離 95%（超出抽樣誤差）時，報告須說明可能原因，包括 exchangeability 假設可能不成立。這是需要解釋的結果，不是 FAIL，除非原因是計算錯誤或資料洩漏。（沿用 r4）

### 3.5 Verification intent

依 G8，驗證包括：
- 模組單元測試；
- leakage 測試（OC-A3，含 E10 與 E12 只接收 Fit 衍生資料的測試）；
- conformal 計算的獨立驗證（OC-A5）；
- **（v2 新增）** Adjusted R² 的獨立重算（OC-A10）；
- 從乾淨環境完整重跑 notebook（OC-A6）；
- 繳交文件檢查：OC-A2、A7、A8、A9、A11、A12 要求的章節、標示、檔名、ZIP 內容，以及摘要與原始材料的對照。

具體的測試方法、framework 與 fixtures 屬 Spec／HOW。

## 4. Authority and authorization

| 項目 | 內容 |
| --- | --- |
| 接受前（本 DRAFT 的狀態） | **本檔沒有任何授權。** HW2 已接受的 Outcome Contract 仍是 r4。本檔不重新授權 Spec v1.1、Issues #50–#56 或任何 Formal run。本次重新基準化的 Git 準備動作，依據是 acceptor 2026-10-18 的逐次明確授權（第 8 節 #2），不是本檔 |
| 接受後的授權 | 在第 2 節的 boundary 內，授權具相應 authority 的 Agents 規劃、分解（由 Design Authority derive Spec 與 Tickets，或修訂既有的 derived contracts）、實作、審查、修正至 S2，範圍限 `home_work_02/` |
| Git（接受後） | 見第 4.1、4.2 節 |
| 保留給 acceptor | RB-1 合併進 `main`，但 SA-3 涵蓋的合併除外（第 4.2 節）；RB-2 繳交（S4）；RB-3 憑證與第三方帳號（含 Kaggle、ChatGPT、NotebookLM 帳號，以及部署平台帳號的操作）；RB-4 付費；RB-5 單元目錄外的檔案（含 `week05/`、`week06/`、root `CONTEXT-MAP.md`、root `.gitignore`）與 `doc/requirement/`；RB-6 破壞性 git 操作 |
| Acceptor 輸入 | 第 3.3 節 |
| 不保留 | Spec review、獨立的 implementation authorization（Bindings §2.6） |
| **既有 derived contracts 的處置**（r2 依 U-5 修訂） | 本檔接受後，由 Design Authority 判定 Spec v1.1 與 #50–#56 的處置（沿用、修訂或作廢），並寫 derivation record。在 DA 判定前：<br>• #50–#56 保持不變，**包括現有 label**（`ready-for-agent`）；<br>• 任何 Formal run 或實作都**不得**使用這些舊 Tickets（F-7 #6；U-5）。<br>`ready-for-agent` label 不構成授權，也不推翻本條 |

### 4.1 Git 授權 C5（沿用 r4，重新確認；F-7 #4）

G8 的原文保留不變（Brief v0.3 §3）：「Standard verification: module tests, leakage tests, conformal calculation verification, full notebook rerun, and submission document checks; Git push and iLearning submission reserved for human operation」。

C5 釐清 G8 的 Git 部分（acceptor 2026-10-14 決定，本檔重新陳述）：
- Agents 可以建立 branch、commit、push topic branch、開 PR，並執行已授權的合併；
- 不得自主執行破壞性 Git 操作；
- iLearning 繳交保留給 acceptor。

合併的授權來自本契約對 Bindings b5 SA-3 的明確引用（第 4.2 節）。

- **被取代的部分**：G8 的「Git push … reserved for human operation」。
- **不變的部分**：G8 的五項驗證，以及「iLearning submission reserved for human operation」。

C5 只能在上位規則允許的範圍內生效（治理 §5.3：治理本文 ＞ Bindings ＞ Accepted Work Contract）。本契約不能放寬 Bindings 的 reserved boundaries，只能 opt-in Bindings 已宣告的 SA-3。

| 操作 | 接受後的效力 | 依據 |
| --- | --- | --- |
| 建立 topic branch | **授權** | Bindings SA-1 |
| 在 topic branch 上 commit | **授權** | Bindings SA-1 |
| Push topic branch 到 `origin` | **授權** | Bindings SA-1（C5 取消 G8 對它的收窄） |
| 從 topic branch 對 `main` 開 PR | **授權** | Bindings SA-2 |
| 合併進 `main` | **授權，限 SA-3 條件成立時**（第 4.2 節） | Bindings b5 §2.5 SA-3（本契約 opt-in）、§5 SA-3 merge gates 與合併後驗證、§7 Merge record |
| 在 `main` 上 commit、force push、改寫已 push 的歷史、刪除 topic branch 或非本次 run 建立的分支、squash 或 rebase 合併 | 不授權 | SA-1 的排除項；SA-3 的排除項；RB-6 |
| iLearning 繳交 | 不授權，保留給 acceptor | RB-2；G8 |
| 部署平台與其他第三方帳號的操作 | 不授權，保留給 acceptor | RB-3；F-7 #7 |

SA-1、SA-2 只涵蓋 `home_work_02/` 範圍內的 work item，commit message 與 PR 描述依 `docs/conventions/git-commit-rules.md`。

### 4.2 合併進 `main`（S3）的授權：Bindings b5 SA-3 opt-in（沿用 r4，重新確認）

**本 Outcome Contract 明確引用 Project Bindings b5 §2.5 SA-3（opt-in）。** 適用於本契約範圍內 `home_work_02/` 的 work items：在 Bindings b5 §2.5 SA-3 的全部條件成立時，由 Formal 的 Orchestrator，或 Lightweight 的 direct-execution Executor，經 SA-2 開的 PR，以 merge commit 把 `home_work_02/` 的 topic branch 合併進 `main`。

- **Gates**：Bindings b5 §5 的 integration／release gates，加上 SA-3 merge gates，包括：
  - 治理 §3.8 的完成條件與必要 audit；
  - Lightweight work item 須另有 independent audit closure；
  - 以本契約**已接受版本**核對 opt-in；
  - 受審 head SHA 與合併的 head SHA 相同，合併指令綁定該 SHA；
  - diff 只在 `home_work_02/` 內，且不含 `home_work_02/doc/requirement/`；
  - PR head 上所有 checks 都已完成且成功；
  - 只用 merge commit，不刪除 topic branch。
- **合併後驗證**：依 Bindings b5 §5，核對 GitHub Pages 與 Vercel production 部署的狀態，並執行已部署單元既有的 smoke 檢查。任一失敗時寫 stop report 交 acceptor，不自行回滾、重新部署或改寫歷史（RB-3、RB-6）。
- **紀錄**：Bindings b5 §7 Merge record。
  - 合併前的 gate 證據、本 opt-in 條款與本契約接受的 commit SHA，記在 run record 或 worklog；
  - merge commit SHA 與合併後驗證結果，記在該 PR 的 comment。
- **退回 RB-1**：SA-3 任一條件不成立時，合併屬 RB-1 保留給 acceptor 的動作；Agent 只停止該路徑並寫 stop report（治理 §1.5 第 3 項），可由 acceptor 逐次明確授權。
- **第一個 HW2 PR**（**v2 修訂**；F-7 #5；**r2 依 U-1 修訂**）：
  - HW2 的第一個 PR，其 diff 必然包含 `home_work_02/doc/requirement/`（SRC-1、SRC-2T），不在 SA-3 範圍內，屬 RB-1。
  - r4 接受紀錄中的一次性 RB-1 授權**不被推定涵蓋**新基準或其第一個 PR（F-7 #5）。取而代之的是 acceptor 2026-10-18 的 **U-1 一次性 RB-1 授權**（原文見第 12 節）。
  - **範圍**：HW2 第一個合併進 `main` 的 PR，限於本次 HW2 重新基準化與實作交付。
  - **執行者**：獲授權的 Agent。Formal 下是 Orchestrator（Bindings §3.5）。
  - **條件**（全部成立才可合併）：
    - 適用的 independent audits 全部通過；
    - Spec Integration Audit 已 closure；
    - Design Authority 的 phase acceptance 已完成；
    - Bindings b5 §5 的 integration／release gates 滿足；
    - PR checks 全部完成且成功；
    - 以 merge commit 合併；
    - 不繞過失敗的 check；
    - PR 不修改無關的檔案：diff 只含 `home_work_02/`；
    - 不執行破壞性 Git 操作。
  - **證據與合併後驗證**：沿用 SA-3 的 subject identity（受審 head SHA＝合併的 head SHA，合併指令綁定該 SHA），以及 Bindings b5 §7 Merge record 與合併後驗證的做法，並在紀錄中寫明依據是 U-1，不是 SA-3。
  - **性質**：一次性授權，**不是 SA-3 或 Project Bindings 的變更**，不構成常設合併權限。之後的 PR 依本節 SA-3 處理。
  - **生效**：U-1 是 acceptor 對 RB-1 的明確授權（Bindings §2.1）。它所授權的合併只會發生在本契約接受、且上列條件全部成立之後；它**不授權**本準備階段開 PR 或合併。
- **不在此授權內**：對單元目錄以外（含 `docs/governance/`、`.claude/`、root、其他單元）的修改，或對 `doc/requirement/` 的修改，都不在 SA-3 範圍內，依 RB-5 另行處理。
- **合併的時機**：合併進 `main`（S3）不是 work item 完成（S2）的條件；S4 iLearning 繳交仍保留給 acceptor（RB-2）。

## 5. Relevant context

- **資料集核對證據**（沿用 r4）：Brief v0.3 §10。
  - CSV sha256 `d0875baa0251b21d4bdc9d2ae940a4fe0bb6009824f23dd0e2a5b2bf04557b7e`；CC0-1.0；
  - 21,613 列 × 21 欄；0 缺值；
  - 21,436 個 `id`（177 筆重複交易）；
  - `sqft_living = sqft_above + sqft_basement` 對全部列成立。
- **Spec 需處理的設計事項**（由 Design Authority 決定）：
  - 沿用 r4，Spec v1.1 已有 r4 下的裁決，DA 判定是否沿用：
    - 完全共線的處理方式；
    - `date` 與 `zipcode` 的處理；
    - 轉回 USD 時的偏誤修正；
    - 選模的 tie-break；
    - 離群值處理；
    - 報告 PDF 的產生方式；
    - 資料取得方式；
    - acceptor 原始材料的存放位置。
  - **（v2 新增）**：
    - E10 每個診斷面向的方法、所用的 Fit 衍生殘差與驗證準則；
    - E11 的 n 與 p 慣例、各類模型的適用性、複雜度或有效自由度的處理、比較限制；
    - E12 係數解讀的呈現方式、permutation importance 的資料、指標與重複次數；
    - 新增工作的計算預算（Spec v1.1 §4.5）；
    - 「每次執行只做一次 Test 評估」（第 2.4.1 節）的 manifest、事件與 worklog 細節。
- **既有 derived contracts**：Spec v1.1（EFFECTIVE under r4）與 Issues #50–#56（OPEN）是 r4 的 derived contracts，保留為歷史參考；處置見第 4 節。
- **參考**：
  - `week05/multiple_linear_regression_crisp_dm.ipynb`（REFERENCE）；
  - `week05/docs/` 課程講義（CRISP-DM、L6 multiple linear regression）；
  - `week06/`（DIC-02 特徵選擇比較，REFERENCE）。
- **期限**：2026-11-04（老師文件）。

## 6. Assurance path

- **Lane**：預期為 **Formal**（Spec＋Tickets＋Orchestrator）：多個彼此相依的 execution units，且需要等待 acceptor 的輸入（治理 §3.6-C；Bindings §4）。由 Design Authority 在本契約接受後重新判定並留紀錄。
- **Audit**：Formal 下每個 Ticket 做 independent audit，每份 Spec 做 Spec Integration Audit；只有一張 Ticket 的 Spec 可以用 fast path（Bindings §5）。
- **高風險類別**：DA 在 r4 下確認了 H-1～H-4（`decisions/decision-20261014-high-risk-categories.md`）。本契約接受後、第一次正式 audit 前，由 DA 確認它們是否適用於 v2。起草建議：E10～E12 的「只用 Fit」屬 H-3 評估完整性；E13 的標示屬 H-4 證據真實性與標示誠實。
- **Release gate**：合併進 `main`（S3）前，須符合 Bindings b5 §5 的 integration／release gates；依 SA-3 合併時另須 SA-3 merge gates（第 4.2 節）。

## 7. Stable reference

- 接受時以 commit SHA 固定本檔第 1–8 節，以及 SRC-2T、Brief v0.4、Delta record 的內容。
- SRC-2 本身以 sha256 `1b3a5aad…39d7` 固定，原始檔在 acceptor 本機。
- 本 DRAFT 所在的 commit 記錄在第 8 節 #2 與 acceptance-review packet。之後若修訂，以新的 commit 為接受用的 commit。

## 8. Activation preconditions（接受前或啟動 Formal run 前）

| # | 項目 | 狀態 |
| --- | --- | --- |
| 1 | SRC-2 sha256 核對與 SRC-2T 轉寫；原始 PDF 的公開性檢查 | **完成**（2026-10-18；Delta record §1、§1.1） |
| 2 | **文件基準 commit**：topic branch `home_work_02-rebaseline-oc-v2`（自 `home_work_02-outcome-contract` 的 `6bc5eca` 建立，非破壞性），commit SRC-2T、單元 `.gitignore`、Brief v0.4、Delta record、本檔與 consistency review，並 push。依據：acceptor 2026-10-18「Part E — Git workflow」的明確授權（「I authorize the necessary non-destructive Git preparation operations for this HW2 re-baselining task, limited to the approved HW2 unit and its documentation.」）；新增 SRC-2T 屬 RB-5，依據為同一指示的 Part B | **完成**（commit SHA 見 acceptance-review packet） |
| 3 | 第 9 節接受紀錄：acceptor 原文、日期、接受的 commit SHA | **待 acceptor** |
| 4 | 第一個 HW2 PR 的 RB-1 授權（第 4.2 節） | **待 acceptor**（接受時決定，或之後逐次決定） |
| 5 | r4 接受時的 Fable fallback 決定（r4 §9）是否在本契約下沿用 | **待 acceptor**（見 packet 的待決事項） |
| 6 | Design Authority 確認 lane、高風險類別，並判定 Spec v1.1 與 #50–#56 的處置 | 接受後 |
| 7 | 常設合併授權：Bindings b5 SA-3 已生效（`5ebcc58`），本契約於第 4.2 節 opt-in | **完成**（opt-in 在接受後才生效） |

## 9. 接受紀錄

| 項目 | 內容 |
| --- | --- |
| 狀態 | **未接受（DRAFT r1）** |
| Acceptor | — |
| Acceptor 原始指示（引用原文） | — |
| 日期 | — |
| 接受的 commit SHA | — |
| 接受時的修訂 | — |
| RB-1（第一個 HW2 PR） | — |

本節只能在 acceptor 明確接受後，依其原文填寫。Agent 代寫的接受紀錄不等於取得授權（治理 §1.2、§5.3）。

## 10. r4 → v2 邊界差異

| r4 位置 | r4 | v2 DRAFT | 依據 |
| --- | --- | --- | --- |
| 檔頭、§7、§9 | ACCEPTED；r4 的接受紀錄 | 提議後繼；未接受；新的 stable reference 與接受紀錄欄位 | F-7 #2、#3 |
| §1 | 比較、conformal、Test | 加入診斷、解釋、Adjusted R²、特徵數解讀與三種標示 | F-1、F-4～F-7 |
| §2.1 | SRC-1 | SRC-2（以 SRC-2T 追蹤）；SRC-1 為歷史；補充段的規範力 | F-1；Part B |
| §2.2 M1 | 10–20 | **14–20**（交集），含兩條原文與解讀的說明 | F-1 |
| §2.2 M2～M10 | — | 不變 | — |
| §2.2 E1～E9 | — | 語義不變；E4 列出 Adjusted R²；E8 涵蓋新的驗證；E1 的報告標示改為「依老師補充建議」 | F-3、F-5、F-7 #8 |
| §2.2 E10～E13 | 無 | 新增 | F-4～F-7 |
| §2.2 OPTIONAL、REFERENCE | 額外診斷圖；week05 | 額外診斷圖限 E10 之外；REFERENCE 加入 `week06/` 與未採用的補充建議 | F-4、F-2、F-3 |
| §2.3 | 八項 | 沿用八項（RB-5 加列 `week06/`），新增六項排除 | F-1～F-6 |
| §2.4.1 | 計數 19（或 18），10–20；「Test 在 predictor 凍結後只評估一次」 | 計數規則明確為編碼前；source features 19 須在 14–20；報告說明；E10／E12 只用 Fit；S-09 的說明；**「每次執行只做一次 Test 評估」由 Spec v1.1 的 derived 定義提升為 accepted 語義**（語義與 r4 下的實際設計相同，只是位階提高） | F-1～F-3；Part C 保留清單 |
| §2.4.2 | conformal | **不變**（逐字沿用） | — |
| §2.4.3～§2.4.6 | 無 | 新增 | F-4～F-7 |
| §2.5、§2.5.1 | — | **不變** | F-7 #4 |
| §3.1 OC-A1 | 10–20 | 14–20；兩條原文；禁止選擇後計數 | F-1 |
| §3.1 OC-A3 | 分區與 fold 隔離 | 加入 E10、E12 只接收 Fit 衍生資料 | F-4、F-6 |
| §3.1 OC-A4 | 五個候選 | 五個且只有五個；禁止以 Adjusted R² 選模；S-09 的說明 | F-3、F-5 |
| §3.1 OC-A2、A5、A6、A7、A8 | — | 不變（A6 的「數值一致」涵蓋 E10～E12 的數值） | — |
| §3.1 OC-A9～A12 | 無 | 新增 | F-4～F-7 |
| §3.2 | S1＝A1～A6 | S1＝A1～A6、A9～A12；S2～S4 不變 | — |
| §3.3 | — | 不變 | — |
| §3.4 | — | 新增兩項非 FAIL、五項 FAIL | F-1、F-4～F-7 |
| §3.5 | 五項驗證 | 加入 Adjusted R² 重算與新的隔離測試、文件檢查 | F-4～F-6 |
| §4 | 接受後的授權；C5；SA-3 | 不變；加入「本 DRAFT 沒有授權」、既有 derived contracts 的處置、RB-3 部署帳號 | F-7 #4、#6、#7 |
| §4.2 第一個 PR | （r4 §9 的一次性 RB-1 授權） | 不推定沿用；待 acceptor | F-7 #5 |
| §5 | 八項設計事項 | 加入 E10～E12 的設計事項、計算預算、單次 Test 評估的實作細節 | F-4～F-6 |
| §6 | H-1～H-4 待確認 | DA 重新確認 H-1～H-4 是否適用 | — |
| §8 | r4 的前置條件 | 新的前置條件 #1～#7 | — |

**刻意沒有擴大的範圍**：
- 沒有新增候選、資料集或 conformal 方法；
- 沒有新增效能門檻；
- 沒有改變分區比例、seed 政策、log 目標、USD 指標、選模準則、Test 單次評估或 acceptor 證據規則；
- 沒有新增 acceptor 輸入。

## 11. 修訂紀錄

| 版本 | 日期 | 變更 |
| --- | --- | --- |
| DRAFT r1 | 2026-10-18 | 依 SRC-2 與 acceptor 2026-10-18 的 F-1～F-7 裁決起草。r4 的語義除第 10 節所列以外全部沿用 |
