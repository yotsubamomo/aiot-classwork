# HW2 需求重新基準化：來源登錄、需求擷取與差異追溯（2026-10-18）

- **狀態**：DISCUSSION RECORD（不具 authority）。本檔是事前盤點：登錄新的老師來源、逐條擷取需求、比對舊基準，並追溯到已接受的契約與 derived contracts。它不是 Outcome Contract、Spec 或 Design Authority 的裁決，也不改變任何已接受的內容。
- **版本**：
  - rev 1（2026-10-18）：盤點與建議。
  - rev 2（2026-10-18）：記錄 acceptor 對 F-1～F-7 的最終裁決（第 5、6 節）；SRC-2 的公開性檢查與轉寫（第 1.1 節）；更正推薦資料集的連結對應（第 3.2 節 S-05）。
- **撰寫者**：無角色主 session（Bindings b5 §3.5），依 acceptor 2026-10-18 的兩次指示起草：「Start a controlled HW2 requirements re-baselining workflow」與「Continue the NCHU AIoT HW2 requirements re-baselining workflow」。
- **配套文件**：
  - Grill Brief Draft v0.4（[`HW2_Grill_Brief_Draft_v0.4.md`](HW2_Grill_Brief_Draft_v0.4.md)）：frontiers 與 acceptor 裁決原文。
  - Outcome Contract v2 DRAFT（[`../governance/outcome-contract-v2.md`](../governance/outcome-contract-v2.md)）。
- **依據**：治理 v2.2 §1.2（re-authorization）、§3.1、§3.2、§5.3（contract change 兩類劃分）；Bindings b5 §2.2、§2.4、§2.6 RB-5、§7。

## 1. 來源登錄（Source baseline registry）

| ID | 檔案 | 性質 | 日期 | sha256 | 狀態 |
| --- | --- | --- | --- | --- | --- |
| **SRC-1** | `doc/requirement/HW2-requirements-Multiple Linear regression.txt` | acceptor 轉寫的 iLearning 作業頁文字（2,432 bytes） | 2026-10-14 納入（commit `1f1a916e`） | `a969e7e2228e97a35027ad63d3747f2e502bdd685cf7cfca30aaab50048761ab`（git blob 內容。Windows 工作目錄因 `core.autocrlf=true` 為 CRLF，檔案 hash 為 `b01c6fb5…4b89`，內容相同） | **歷史基準**。OC r4 §2.1 的上位契約，保持原樣，不刪除、不改寫 |
| **SRC-2** | `doc/requirement/HW2-requirements-Multiple Linear regression.pdf` | 瀏覽器列印的 iLearning 作業頁 `https://lms2020.nchu.edu.tw/course/homework/74761`，4 頁，1,083,106 bytes；PDF CreationDate `D:20261017185958+00'00'`（＝2026-10-18 02:59:58 +0800），Producer Skia/PDF m155 | 老師更新日 2026-10-18（acceptor 陳述）；頁首列印時間 2026/10/18 02:59 | `1b3a5aad1c261425eb34f2eb46aebe6a62c73aba4fbf2d67a166fe9df28639d7`（2026-10-18 兩次核對一致） | **提議的新上位契約**（OC v2 DRAFT §2.1）。原始 PDF 只保留在 acceptor 本機，以單元 `.gitignore` 排除，不進 git（第 1.1 節） |
| **SRC-2T** | `doc/requirement/HW2-requirements-Multiple Linear regression_SRC-2_2026-10-18.txt` | SRC-2 的忠實轉寫：逐頁、標示頁碼、文字照原樣、轉寫註記另外標示、附連結目標 | 2026-10-18 | 由納入的 commit 固定（見 OC v2 §7） | SRC-2 的追蹤副本。正文與 SRC-1 以程式比對，差別只有「已缴交」4人→8人 |

- SRC-2 由 acceptor 放入 `doc/requirement/`。本 session 沒有修改或移動它。
- SRC-2 只帶列印時間，頁面本身沒有「更新時間」欄位。「2026-10-18 更新」以 acceptor 的陳述為準。
- `~/Downloads/確認作業需求HW2.pdf`（2026-10-14，sha256 `e80e41ac…ad1d`）是 acceptor 自己的檔案，不是來源。

### 1.1 SRC-2 的公開性檢查與處理（acceptor 2026-10-18 Part B 指示）

| 檢查項目 | 結果 |
| --- | --- |
| 個人資料 | 未發現。PDF metadata 沒有 Author；頁面沒有使用者名稱或學號（學號只有範例 `7114056XXX`）；「已缴交 8人」與「线上：585 人」是網站計數 |
| 受限或第三方內容 | (1) iLearning 是登入後才能看到的課程頁面；(2) 頁尾有「© Copyright since 2020 by National Chung Hsing University. All rights reserved.」；(3) 嵌入 5 張圖片，是推薦資料集的縮圖（第三方內容） |
| 公開範圍 | `yotsubamomo/aiot-classwork` 是 **PUBLIC** repository；topic branch push 後即可公開取得 |
| 既有慣例 | HW01 的老師 PDF 以 root `.gitignore` 排除（commit `c212d30`）；HW2 的 SRC-1 只追蹤文字轉寫；Spec v1.1 R-REPO-3 也規定追蹤檔案不含 PDF，除非 acceptor 明確決定公開 |

**處理**：
- 原始 PDF 不追蹤。新增單元 `.gitignore`（`home_work_02/.gitignore`），只排除這個檔案，避免誤加入。Root `.gitignore` 屬 RB-5 的單元外檔案，本次不修改。
- 改以 SRC-2T 追蹤文字內容，並記錄 SRC-2 的 sha256。
- 若 acceptor 決定公開原始 PDF，需要一次明確決定。屆時刪除單元 `.gitignore` 的該行並 commit PDF；這是公開揭露的決定，Agent 不推定。

**授權依據**：
- 在 `doc/requirement/` 新增 SRC-2T，以及新增單元 `.gitignore`，都屬於修改單元內檔案。前者另受 RB-5（修改 `doc/requirement/`）保護。
- 兩者的依據是 acceptor 2026-10-18 的明確指示：「Otherwise preserve the PDF locally and create a faithful text extraction with source-page references and a recorded source SHA-256.」以及 Part E 對 HW2 單元文件 Git 準備動作的授權。Bindings §2.1：reserved boundaries 由 acceptor 在對話中明確指示。

## 2. SRC-1 與 SRC-2 的差異

**比對方法**：
- rev 1：以 PDF 頁面文字與 SRC-1 逐行人工比對。
- rev 2：轉寫 SRC-2T 後，再以程式（difflib）比對 SRC-1 與 SRC-2T「補充」之前的正文。

| 區段 | 結果 |
| --- | --- |
| 抬頭（類型、開放繳交 2025-10-15、期限 2026-11-04、允許遲交、比重 10%、評分方式） | 相同 |
| 「已缴交」人數 | 4人 → 8人（非規範性） |
| 一、作業目標 | 相同 |
| 二、作業內容 1–5 | 相同 |
| 三、評分標準 | 相同 |
| **「==== 補充 ====」以下** | **全部是新內容**（SRC-2 p.2 中段～p.4） |

**結論**：正文（含評分標準）沒有變更。新增的只有「補充」段。

### 2.1 「補充」段的證據性質（evidence class）

| 觀察 | 位置 |
| --- | --- |
| 第一行是一句英文提問「list kaggle multiple linear regression problems , choose features > 13, < 40」 | SRC-2 p.2 |
| 其後是對提問的回答，以第二人稱稱呼提問者（「你希望找…」、「不符合你的原始特徵數限制」、「meet your constraint」） | p.2–p.4 |
| 有聊天介面網頁搜尋的引用標記殘留（「Kaggle +1」、「Kaggle +5」），也有數學式重複渲染的殘字 | p.2–p.3 |
| 用語是建議（「建議優先選擇」、「Recommended」、「My Top 3 for Teaching」、「Suggested Assignment」、「students can complete」、「My first choice」） | p.2–p.4 |

**判讀**：
- 「補充」段是老師貼在作業頁上的一段 LLM 對話輸出；提問句是老師寫的，其餘是 LLM 的回答。
- 它屬於上位契約檔案的一部分，但規範力依原文措辭判斷。
- Acceptor 已裁決（F-1＝B）：特徵數條件以正文與補充的交集處理；補充段其餘內容依原文措辭維持 S（建議）的分類，不重新分類為老師要求。

## 3. 需求擷取與分類

**分類**（acceptor 指定）：
- **M**＝Mandatory：「必須」、「需」、「請…」等明確要求，或評分直接依賴。
- **S**＝Suggested：建議、推薦、範例。
- **O**＝Optional：老師明示「可」、「optional」。
- **A**＝Ambiguous：多種解讀，且選擇會改變交付內容或評分對象。

原文照錄，不改寫；說明放在「備註」欄。「處理」欄是 acceptor 裁決後的結果（第 5 節）。頁碼指 SRC-2T 的頁面標記。

### 3.1 正文（SRC-1＝SRC-2 p.1–p.2）

| ID | 原文 | 類別 | 備註 | 處理（OC v2 DRAFT） |
| --- | --- | --- | --- | --- |
| T-01 | 本次作業延伸自 HW1，目標是讓同學能夠以實際資料集進行「多元線性回歸 (Multiple Linear Regression)」的完整分析，並遵循 CRISP-DM 流程完成從資料理解、建模到評估的全過程。 | M | 作業目標；題名也是 Multiple Linear regression | MVM |
| T-02 | 至 Kaggle 選擇一個具有 10 至 20 個特徵 (features) 的公開資料集。 | M（範圍 A） | 與 S-01／S-02 的 14–39 衝突（X-1） | MVM；F-1＝B：採交集 14–20 |
| T-03 | 類型不限（可為房價預測、醫療、車輛效能等主題）。 | O | 主題自由 | F-2＝A：King County |
| T-04 | 請明確標示資料集來源與連結。 | M | | MVM |
| T-05 | 使用線性回歸 (Linear Regression) 模型進行預測。 | M | | MVM |
| T-06 | 可嘗試單純線性回歸、多元線性回歸或 Auto Regression。 | O | T-01 使多元線性回歸成為實質必要 | Auto Regression 不做（Non-scope，沿用 r4） |
| T-07 | 必須執行 特徵選擇 (Feature Selection) 與 模型評估 (Model Evaluation)。 | M | 方法未指定 | MVM（F-3＝A：五個候選） |
| T-08 | 結果部分需包含請提供預測圖(加上信賴區間或預測區間) | M | 擇一 | MVM（預測區間，沿用 r4） |
| T-09 | CRISP-DM 流程說明：Business Understanding／Data Understanding／Data Preparation／Modeling／Evaluation／Deployment | M | 六階段 | MVM |
| T-10 | 所有與 ChatGPT 的對話請以 pdfCrowd 或其他方式須匯出為 PDF | M | | MVM |
| T-11 | 請使用 NotebookLM 對網路上同主題的解法進行研究，並撰寫一份 100 字以上的摘要，放入報告中。 | M | | MVM |
| T-12 | 請在報告中明確標示「GPT 輔助內容」與「NotebookLM 摘要」 | M | | MVM |
| T-13 | 主程式：7114056XXX_hw2.py/.ipynb | M | | MVM |
| T-14 | 報告檔： PDF，需包含以下內容：按照 CRISP-DM 說明的分析流程／GPT 對話過程（pdfCrowd 匯出）／NotebookLM 研究摘要／網路上主流或更優解法之比較與說明 | M | | MVM |
| T-15 | 以上檔案與資料夾請壓縮為學號命名的一個zip（例如 7114056XXX_hw2.zip）上傳。 | M | | MVM |
| T-16 | (optional) 若上傳至 GitHub，或是以colab撰寫，需提供連結，並在 README.md 中整理流程與成果。 | O | 因 G7 使用 GitHub | MVM（沿用 r4 M10） |
| T-17 | 評分標準：文件說明 50%（CRISP-DM 25%、GPT 與 NotebookLM 15%、資料集來源與研究脈絡 10%）；結果呈現 50%（模型正確可執行，具特徵選擇與評估 25%、結果合理美觀具說服力 15%、呈現出Kaggle名次(若有)/預測結果評估(預測圖、評估指標) 10%） | M（評分依據） | 「Kaggle名次(若有)」是條件式 | 名次不適用（King County 沒有競賽排行榜） |
| T-18 | 缴交期限 2026-11-04；允许迟交 是；成绩比重 10% | — | 背景資訊 | — |

### 3.2 補充（SRC-2 p.2–p.4 新增）

| ID | 原文 | 類別 | 備註 | 處理（OC v2 DRAFT） |
| --- | --- | --- | --- | --- |
| S-01 | list kaggle multiple linear regression problems , choose features > 13, < 40 | **A** | 老師寫的提問句 | F-1＝B：與 T-02 取交集 |
| S-02 | 也就是 14–39 個輸入特徵，不包含 Target（預測目標）。 | **A** | LLM 對 S-01 的轉述 | 同上；不含 target |
| S-03 | 建議優先選擇連續數值預測（Regression）、可使用 sklearn.LinearRegression 、適合進行 Feature Selection、MSE、RMSE、R² 與五大回歸假設檢驗的資料集。 | S | 資料集的選擇準則 | King County 符合這些準則（報告說明） |
| S-04 | 特別注意：Kaggle 上常見的 House Prices — Advanced Regression Techniques 有 79 個原始特徵，不符合你的原始特徵數限制，但可以透過特徵選擇建立 14–39 特徵的練習版本。 | **A** | 兩種計數方式並存 | F-1＝B：只採編碼前、選擇前的 source feature 計數 |
| S-05 | Recommended Kaggle Regression Problems（6 列，見 SRC-2T p.2–p.3） | S | 推薦清單，不是限定清單。**rev 2 更正連結對應**（取自 PDF link annotation）：Predict the Flood → `competitions/predictheflood`；Flood Prediction Dataset → `competitions/playground-series-s4e5`；Istanbul → `datasets/brahimenesulusoy/istanbul-apartment-prices-2026`；Swiss Housing → `competitions/i3-ml-21-22-mini-project`；Human–AI Interaction → `dsv/13207192`；House Prices → `competitions/house-prices-advanced-regression-techniques` | F-2＝A：不採用，保留 King County |
| S-06 | \*Istanbul 資料集描述為 30 欄，包含價格等欄位；精確輸入特徵數需檢查 CSV。上述資料集的特徵數以來源描述為準，類別編碼後可能增加。 | S（計數說明） | 支持以編碼前計數 | 與 F-1 一致 |
| S-07 | My Top 3 for Teaching：1. Predict the Flood、2. Istanbul Apartment Prices、3. Human–AI Interaction | S | | 不採用（F-2＝A） |
| S-08a | Business Understanding: Define the continuous prediction target. | S | 已涵蓋 | MVM（M4） |
| S-08b | Data Understanding: Verify sample size, feature count, missing values and correlations. | S | 大致涵蓋 | 沿用 r4；Spec 細節交 DA |
| S-08c | Data Preparation: Train/test split, missing-value handling and categorical encoding. | S | 已涵蓋 | 沿用 r4 |
| S-08d | Modeling: Train LinearRegression , Ridge and Lasso. | S | 已涵蓋（E1） | 沿用 r4 E1（F-3＝A）；報告標「依老師補充建議」 |
| S-08e | Evaluation: Compare MAE, MSE, RMSE, R² and Adjusted R² | S | Adjusted R² 是新項目 | **F-5＝B：ENHANCED REQUIRED** |
| S-08f | check the five regression assumptions. | S（內容 A） | 新項目；五項未定義 | **F-4＝B：ENHANCED REQUIRED，五個診斷面向** |
| S-08g | Deployment: Predict new samples and explain the model. | S | 「explain the model」是新項目 | **F-6＝B：ENHANCED REQUIRED** |
| S-09 | For Feature Selection, compare SelectKBest, RFE, Sequential Feature Selection, Lasso and permutation importance, selecting 14, 20, 25 or 30 features using training data only. | S | 方法清單與 k 值是新的 | **F-3＝A**：不新增候選；permutation importance 只作 F-6 的解釋工具；報告說明此清單是建議 |
| S-10 | My first choice is Predict the Flood, because its 20 numerical features meet your constraint directly and avoid the extra complexity of categorical encoding. | S | | 不採用（F-2＝A） |

## 4. 衝突與落差

| ID | 主題 | 舊基準（SRC-1、OC r4） | 新來源（SRC-2） | King County 的事實 | Acceptor 裁決 |
| --- | --- | --- | --- | --- | --- |
| X-1 | 特徵數範圍 | T-02：10–20；source feature 計數 | S-01／S-02：14–39，不含 target；S-04 另有「選擇後符合」的說法 | 19 個 source features（建模用 18 個 group）；10–20 與 14–39 的交集 14–20 | F-1＝B |
| X-2 | Adjusted R² | 沒有 | S-08e 建議 | p 的定義會影響數值 | F-5＝B；p 等慣例交 DA；不改變選模準則 |
| X-3 | 五大回歸假設 | OPTIONAL 診斷圖 | S-03、S-08f 建議，未列五項 | 以 log 尺度；重複交易與地理鄰近影響「獨立」 | F-4＝B；五個面向由 acceptor 指定；方法交 DA |
| X-4 | 推薦資料集 | G1：King County | S-05、S-07、S-10 | King County 在兩種讀法下都符合；推薦清單不是限定清單 | F-2＝A |
| X-5 | 特徵選擇方法與 k | E1 的五個候選；k 由 inner CV 選 | S-09 | 18 個 group，k = 20、25、30 不存在 | F-3＝A |
| X-6 | 模型解釋 | 沒有 | S-08g | | F-6＝B |
| X-7 | 報告標示 | MVM／ENHANCED；AC-29 | 部分項目同時是老師建議 | | F-7：三種標示「老師要求」「依老師補充建議」「專案延伸」 |
| X-8 | Kaggle 名次 | 不適用 | Predict the Flood 等是競賽 | 只在改用競賽資料集時相關 | F-2＝A：仍不適用 |

## 5. 舊決定的處理（G1–G8、C1–C5）——acceptor 裁決後

舊決定是**待重新檢視的歷史決定**，不自動約束新的 Outcome Contract。下表依 acceptor 2026-10-18 的 F-1～F-7 裁決（原文見 Brief v0.4 §0）記錄每一項在 OC v2 DRAFT 中的處理。

| ID | 原決定（摘要；原文見 Brief v0.3 §3、§4 與 OC r4 §4.1） | 處理 | 依據 |
| --- | --- | --- | --- |
| G1 | King County；target `price`；LR baseline＋forward／backward＋Ridge／Lasso | **保留**（資料集、target、五個候選） | F-2＝A、F-3＝A |
| G2 | 80／20 Development／Test；Fit 內 5-fold CV；CV RMSE 排序；另報 R²／MAE／MSE | **保留**；指標加入 Adjusted R²，但不影響 RMSE 排序 | F-5＝B |
| G3 | 95% split conformal 預測區間 | **保留**；與古典回歸假設分開陳述 | F-4＝B |
| G4 | 60／20／20 Fit／Calibration／Test | **保留** | Part C 保留清單 |
| G5 | 模組化 Python＋notebook | **保留** | 未受影響 |
| G6 | 報告 PDF＋真實的 ChatGPT 對話 PDF | **保留** | Part C 保留清單 |
| G7 | GitHub repo 的 HW2 子資料夾；ZIP 是正式繳交 | **保留** | Part C 保留清單 |
| G8 | 五項驗證；Git push（已由 C5 釐清）與 iLearning 繳交保留 | **保留**；驗證範圍涵蓋新的交付項目 | F-4～F-6 |
| C1 | Development＝Fit＋Calibration | **保留** | 未受影響 |
| C2 | 依 house `id` 做 group-aware 分區與 CV | **保留** | F-2＝A |
| C3 | 同一組 outer 5-fold；inner CV 選 k 與 `alpha` | **保留** | F-3＝A |
| C4 | `log(price)` 訓練；log 尺度校準；USD 指標 | **保留**；診斷在 log 尺度上做 | F-4＝B |
| C5 | Git 授權 | **保留**，在 OC v2 重新陳述，待 acceptor 重新接受 | F-7 #4 |

## 6. 追溯：受影響的已接受契約與 derived contracts

本節只做影響盤點。**沒有修改任何既有紀錄，沒有關閉或取消任何 Issue，沒有開始實作。**

### 6.1 Outcome Contract r4 → v2 DRAFT

r4（ACCEPTED，normative 第 1–8 節 @ `e2153254`；接受紀錄 @ `370c0ae`）不修改。v2 DRAFT 是提議的後繼契約，只在 acceptor 有效接受後才對之後的工作生效。逐條的邊界差異見 OC v2 DRAFT 第 10 節；摘要如下：

| r4 位置 | v2 DRAFT | 性質（治理 §5.3） |
| --- | --- | --- |
| §2.1 上位契約 | SRC-2（以 SRC-2T 追蹤）；SRC-1 為歷史 | 第 1 類 |
| §2.2 M1、§2.4.1、OC-A1 | 特徵數 14–20（交集），報告說明兩條原文與採用的解讀 | 第 1 類 |
| §2.2 新增 E10～E13 | 五個診斷面向、Adjusted R²、模型解釋、三種報告標示 | 第 1 類（新增 requirement 與 AC） |
| §3.1 新增 OC-A9～OC-A11；OC-A4、OC-A7 修訂 | 新交付項目的 PASS／FAIL；標示規則 | 第 1 類 |
| §3.4 | 新的 FAIL／非 FAIL 條件 | 第 1 類 |
| §5 | DA 需處理的新設計事項 | 第 1 類的一部分 |
| §2.2 E1、§2.4.1 比較與選模、§2.4.2、§2.5、§2.5.1、§3.2、§3.3、§4 | **語義不變**，重新陳述 | 不變 |
| §9 接受紀錄與 RB-1 一次性授權 | 不沿用；v2 有自己的接受紀錄欄位，第一個 PR 的合併授權待 acceptor 決定 | 不推定 |

### 6.2 Spec v1.1 與 derivation records

- Spec v1.1 是 r4 的 derived contract，**保持不變**。
- OC v2 被接受後，由 Design Authority 判定 Spec 的處置（修訂或重新 derive），並在新的 derivation record 中記錄各項的沿用、修改或作廢。**本階段不 derive。**
- 預期影響（供 DA 參考，不是裁決）：

| 範圍 | 預期 |
| --- | --- |
| R-DATA、R-PART、R-PREP、R-CAND、R-CONF、INV-1～INV-3、INV-5、INV-9 | 大致沿用（F-2＝A、F-3＝A） |
| R-SEL-1、R-SEL-2、AC-10 | 比較表加入 Adjusted R²，排序規則不變（F-5） |
| R-EVAL-1、AC-14 | Test 指標加入 Adjusted R²（F-5） |
| R-EVAL-4 | 由 OPTIONAL 改為有 AC 的五個診斷面向（F-4） |
| R-DEP、AC-18 | 加入模型解釋與 permutation importance（F-6） |
| R-DATA-4、AC-03 | 特徵數陳述與兩條原文的說明（F-1） |
| R-RPT-5、AC-29 | 三種報告標示（F-7 #8） |
| R-REPO-1、R-REPO-2 | 單元 `.gitignore` 已存在，含 SRC-2 PDF 一行；實作時加入 R-REPO-2 的其他項目 |

- 既有 decision records（lane、高風險 H-1～H-4、Spec v1.1 review findings）保持原樣。新的 lane 與高風險判定由 DA 在 OC v2 接受後重新確認。

### 6.3 GitHub Issues #50–#56

目前全部 OPEN、ready-for-agent，指向 Spec v1.1。**本階段不關閉、不取消、不修改**（F-7 #6）。預期（DA 判定前的參考）：

| # | 預期 |
| --- | --- |
| #50 資料固定與分區 | 大致不受影響 |
| #51 前處理、候選與 nested CV | 比較表加入 Adjusted R² |
| #52 Conformal、Test 評估、預測圖、Deployment | Adjusted R²（Test）、模型解釋 |
| #53 notebook | 五個診斷面向與模型解釋的章節內容 |
| #54 報告 draft | 診斷、Adjusted R²、解釋、特徵數說明、三種標示 |
| #55 acceptor 證據整合 | 大致不受影響 |
| #56 打包與整合驗收 | 驗收清單隨新 AC 擴充 |

**注意**：#50–#56 仍標為 ready-for-agent。OC v2 接受並由 DA 決定處置前，不得以它們啟動任何 Formal run（F-7 #6）。它們的授權來自 r4 與 Spec v1.1；OC v2 DRAFT 不重新授權它們。

## 7. 本次沒有做的事（對照 acceptor 的限制）

- 沒有刪除或改寫 OC r4、Brief v0.1～v0.3、Spec v1.1、derivation 與 decision records。
- 沒有關閉、取消或修改 #50–#56。
- 沒有實作、沒有 dispatch Orchestrator、沒有 derive Spec 或 Tickets。
- 沒有把老師的建議當成必要（第 3.2 節維持 S 或 A 的分類；採用的項目在報告中標「依老師補充建議」）。
- 沒有自動沿用舊決定（第 5 節逐項列出處理與依據）。
- 沒有修改 root 或其他單元的檔案。
- 沒有接受 OC v2。
