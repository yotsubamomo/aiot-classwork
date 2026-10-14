# Outcome Contract — HW2 Multiple Linear Regression（`home_work_02/`）

- **狀態**：**DRAFT r2（2026-10-14）——未接受，不構成授權。** 只有 acceptor 在第 9 節留下接受紀錄（原文、日期、所接受的 commit SHA）後才生效（Bindings §2.3）。未接受前不得啟動 Formal run，也不得開始實作。
- **取代**：draft r1（sha256 `c8a0154a50b58cc31350433210787731b77d02dc05b2e80ed999829e4169f0bb`；未 commit）。r1 → r2 的逐條變更見第 10 節。
- **依據**：Minimal Operational Governance v2.2 §1.2、§3.1 七項 properties；Project Bindings **b4**，已於 2026-10-14 核對 `main` `ee5d5b9` 的版本（[`../../../docs/governance/project-bindings.md`](../../../docs/governance/project-bindings.md)）§2.2、§2.3、§2.4、§2.5、§2.6、§4、§5、§7。
- **來源紀錄**：Grill Brief v0.1 → v0.2 → v0.3（[`../brief/HW2_Grill_Brief_Draft_v0.3.md`](../brief/HW2_Grill_Brief_Draft_v0.3.md)）：confirmed decisions G1–G8（原文）、clarification decisions C1–C4（2026-10-14）、資料集核對證據（Brief §10）。Brief 是討論紀錄，不具 authority；**本檔與 Brief 不一致時以本檔為準**。特別是 conformal 的 exchangeability 陳述以本檔第 2.4.2 節為準，取代 Brief v0.3 §5.4 的寫法。
- **撰寫者**：無角色主 session（session `8943ecf6`），依 acceptor 指示起草並依 2026-10-14 independent review 的 F-01～F-04 修訂。起草不構成接受、授權或 Design Authority 裁決（治理 §2.7）。
- **Acceptor**：GitHub `yotsubamomo`（Bindings §2.1）。

## 1. Intent and outcome

以 Kaggle 公開資料集 **House Sales in King County, USA** 完成一份遵循 CRISP-DM 六階段、可重現的多元線性回歸分析，預測房屋成交價 `price`：

- 在 Fit 分區上以 group-aware nested CV，公平比較 multiple LR baseline、forward／backward 特徵選擇的 LR、Ridge、Lasso；
- 凍結選出的 predictor，以獨立的 Calibration 分區產生 95% split conformal 預測區間；
- 只在未碰過的 Test 分區上做一次最終評估。

交付 notebook（主程式）、支援模組與測試、報告 PDF、acceptor 提供的真實 ChatGPT 對話 PDF，以及以學號命名的 ZIP，滿足老師 HW2 的全部要求。

## 2. Scope and boundaries

### 2.1 上位契約

老師文件 `HW2-requirements-Multiple Linear regression.txt`（sha256 `a969e7e2228e97a35027ad63d3747f2e502bdd685cf7cfca30aaab50048761ab`）是本作業的上位契約，對所有 Agent 唯讀（Bindings §2.2）。

- **目前位置**：`home_work_02/docs/`。
- **Bindings §2.2 規定的位置**：`home_work_02/doc/requirement/`。
- **搬移**：屬第 8 節 #1。搬移必須 byte-identical（sha256 不變），由 acceptor 執行或明確授權（RB-5 保護 `doc/requirement/` 內的上位契約）。

### 2.2 Scope classes（Bindings §2.4）

**MVM 必須完整滿足上位契約**。ENHANCED 是 acceptor 授權、超出老師撰寫需求的範圍：必須維持標示，且不得取代、弱化或被呈現為老師要求的行為。

| Class | 項目 | 依據 |
| --- | --- | --- |
| **MVM REQUIRED** | M1 Kaggle 公開資料集，10–20 個特徵，標明名稱與來源連結 | 老師 §二.1 |
| | M2 以線性回歸預測；執行特徵選擇與模型評估 | 老師 §二.2 |
| | M3 預測圖，附預測區間（老師允許信賴區間或預測區間；本契約選預測區間） | 老師 §二.2 |
| | M4 CRISP-DM 六階段（Business Understanding、Data Understanding、Data Preparation、Modeling、Evaluation、Deployment），notebook 與報告皆涵蓋 | 老師 §二.3、§二.5 |
| | M5 acceptor 與 **ChatGPT** 進行的、與本作業相關的真實對話，以 pdfCrowd 或其他方式匯出為 PDF | 老師 §二.4 |
| | M6 以 NotebookLM 研究網路上同主題的解法，報告中放 100 字以上的摘要，標示「NotebookLM 摘要」 | 老師 §二.4 |
| | M7 報告中明確標示「GPT 輔助內容」 | 老師 §二.4 |
| | M8 報告比較並說明網路上主流或更優的解法 | 老師 §二.5 |
| | M9 主程式 `<學號>_hw2.ipynb`（或 `.py`）與報告 PDF，壓縮為 `<學號>_hw2.zip` | 老師 §二.5 |
| | M10 使用 GitHub（G7），因此提供連結，並在 `home_work_02/README.md` 整理流程與成果 | 老師 §二.5（optional 條款，因 G7 成為必要） |
| **ENHANCED REQUIRED**（acceptor 授權） | E1 比較範圍：multiple LR baseline、forward LR、backward LR、Ridge、Lasso | G1 |
| | E2 60／20／20 Fit／Calibration／Test 分區，Development＝Fit＋Calibration，所有選模與 CV 只在 Fit 內進行 | G2、G4、C1 |
| | E3 依 house `id` 做 group-aware 分區與 CV | C2 |
| | E4 所有候選用同一組 outer 5-fold 比較，inner CV 選特徵數與 hyperparameter；以 USD 的 outer-CV RMSE 排序，另報 R²、MAE、MSE | G2、C3、C4 |
| | E5 以 log(price) 訓練；評估指標以 USD 報告 | C4 |
| | E6 95% split conformal 預測區間：在 log 尺度校準、轉回 USD；報告 Test 實測 coverage 與平均寬度 | G3、C4 |
| | E7 模組化 Python（data、selection、modeling、evaluation、conformal），notebook 為主程式 | G5 |
| | E8 G8 驗證：模組測試、leakage 測試、conformal 計算驗證、notebook 完整重跑、繳交文件檢查 | G8 |
| | E9 資料以 CSV sha256 固定版本（第 5 節）；依 CC0-1.0 可隨繳交附上 | Brief §10 |
| **OPTIONAL** | 其他候選模型的區間；額外的診斷圖 | Brief v0.3 §5.4 |
| **REFERENCE** | `week05/multiple_linear_regression_crisp_dm.ipynb` 與 `week05/docs/` 課程講義；NotebookLM 或網路研究找到的他人解法 | G5；老師 §二.4 |

### 2.3 Non-scope（明確排除）

- Web App、FastAPI、資料庫、完整 MLOps、強制比較非線性或深度學習模型。
- Kaggle 名次：本資料集沒有競賽排行榜，老師條款寫「若有」。
- Auto Regression：資料是截面的房屋交易，不是時間序列，老師條款為「可嘗試」。
- 任何捏造的研究或對話證據：由 Agent 產生的 ChatGPT 對話、NotebookLM 研究或其摘要內容（第 2.5.1 節）。
- 以 Claude 的對話紀錄或任何非 ChatGPT、與本作業無關的對話，替代 M5 的 ChatGPT 對話 PDF。
- 新的 conformal 演算法：第 2.4.2 節之外的方法都是設計變更，須另經 acceptor。
- 修改 `week05/`、其他單元或 root 檔案（RB-5）。
- 把 week05 的參考實作行為當成老師要求，例如 p-value backward elimination、在選模迴圈中列印 Test RMSE、以全部資料重訓。

### 2.4 Accepted 語義（Spec 在此邊界內 derive AC）

#### 2.4.1 資料、分區與選模

- **資料與特徵計數**：資料為 Kaggle `harlfoxem/housesalesprediction` 的 `kc_house_data.csv`。「特徵」指 **source feature**：原始 CSV 中扣除識別碼 `id` 與目標 `price` 的欄位，encode 後的欄位不計。依此規則共 19 個，捨棄 `date` 則為 18 個，都在 10–20 之內。
- **分區與隔離**（E2、E3）：
  - 以固定 seed、以整棟房屋為單位，隨機分成 Fit／Calibration／Test，三者沒有共同的 `id`；
  - 所有有參數的前處理、特徵選擇與 hyperparameter 搜尋，只在當次訓練 fold 的列上 fit；
  - Calibration 只用來計算凍結 predictor 的 conformal quantile；
  - Test 在 predictor 凍結後只評估一次。
- **比較與選模**（E4、E5）：
  - 每個候選是一個 candidate procedure（前處理＋選擇＋fit）；
  - 所有候選使用同一組 group-aware outer 5-fold，依 USD 的平均 outer-fold RMSE 排序；
  - 選出的 procedure 在整個 Fit 上重跑，產生凍結 predictor。
- **偏誤陳述**：
  - 每個候選的 outer-CV 分數，估計的是該 procedure 的表現；
  - 從多個候選中取最小者，會使勝出者的 outer-CV 分數產生**樂觀偏誤**；
  - 凍結 predictor 表現的獨立估計是 Test 評估；
  - 報告不得把勝出者的 outer-CV 分數寫成不偏估計，也須說明凍結 predictor 是在整個 Fit 上重訓的。

#### 2.4.2 Conformal 預測區間（E6）

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

### 2.5 Constraints

- MVM 必須完整滿足上位契約；ENHANCED 項目在報告中不得被寫成老師要求。
- 資料版本以 CSV sha256 固定；改用不同檔案是 re-pin，須記錄。
- 不使用任何憑證；資料下載只用匿名公開端點，或本機已固定的副本（RB-3）。
- 報告與 notebook 的語言：**[R] zh-TW**（與老師文件及課程一致）。acceptor 可在接受時改寫。

#### 2.5.1 AI 研究與對話證據

| 證據 | 允許 | 禁止 |
| --- | --- | --- |
| ChatGPT 對話 PDF（M5） | 使用 acceptor 本人與 ChatGPT 進行、與 HW2 相關的真實對話，以 pdfCrowd 或等效方式匯出；acceptor 可決定要遮蔽的個人資訊，並在 PDF 或報告中註明遮蔽 | Agent 產生、改寫或補造任何對話內容；以 Claude 或其他工具的對話紀錄、或與本作業無關的對話，替代 ChatGPT 對話 |
| NotebookLM 研究（M6） | acceptor 在 NotebookLM 進行研究並提供原始材料（NotebookLM 的輸出、來源清單）。Agent 可以**忠實地編輯**這些材料：排版、修正錯字、摘錄、翻譯、縮寫成 ≥100 字的摘要。摘要必須可追溯到原始材料與來源連結；經整理的部分在報告中註明「依 NotebookLM 研究整理」 | 加入原始材料沒有的論點或來源；在沒有原始材料時撰寫摘要；把 Agent 自己的網路研究冒充為 NotebookLM 的結果 |
| 主流或更優解法的比較（M8） | 可以由 Agent 依可查證的公開來源撰寫並附連結；若引用 NotebookLM 材料則依上列規則 | 無來源的主張 |
| 「GPT 輔助內容」標示（M7） | 沿用老師的標示名稱；同時如實揭露實際使用的工具，包括 ChatGPT 與 Claude Code。Claude Code 的使用可以在報告中揭露，作為補充說明 | 把 Claude 的產出寫成 ChatGPT 的產出；以揭露說明替代 M5 的 ChatGPT PDF |

原始材料（NotebookLM 輸出與來源清單、ChatGPT PDF）由 acceptor 提供並保留，報告中的摘要與引用可對回原始材料。這些材料是否放進公開的 Git repository 由 acceptor 決定；放進 ZIP 則是 M5、M9 的要求。

## 3. Acceptance boundary

### 3.1 Acceptance criteria（可觀察的 PASS／FAIL 與證據）

Spec 的具體 AC 由 Design Authority 在本邊界內 derive，並在 derivation record 載明各 Spec 分配到的部分。

| ID | 類別 | PASS | FAIL | 證據要求 |
| --- | --- | --- | --- | --- |
| OC-A1 資料集 | MVM | 報告與 notebook 載明資料集名稱、Kaggle 連結、授權；載入的 CSV sha256 等於固定值，或另有 re-pin 紀錄；以第 2.4.1 節規則陳述 source feature 數量，且落在 10–20 | 缺來源或連結；checksum 不符且無 re-pin 紀錄；以 encode 後欄位計數；數量不在 10–20 | notebook 輸出的 checksum 與欄位清單；報告的資料說明節 |
| OC-A2 CRISP-DM | MVM | notebook 與報告各有六個階段的明確章節，內容對應各階段 | 缺任一階段，或只有標題沒有內容 | 章節清單比對 |
| OC-A3 隔離 | ENHANCED | 自動化測試證明：三個分區沒有共同的 `id`，合起來涵蓋全部列；每個 CV fold 的訓練列與驗證列沒有共同的 `id`；有參數的前處理與特徵選擇只以訓練 fold 的列 fit；凍結 predictor 的識別（例如檔案 hash）在 Test 評估之前已記錄 | 任一測試失敗或不存在；Test 或 Calibration 在凍結前被用於任何選擇 | 測試輸出；凍結 predictor 的識別與 Test 評估的順序 |
| OC-A4 比較與選模 | MVM（M2）＋ENHANCED（E1、E4、E5） | 五個候選都在同一組 outer folds 上有 USD RMSE（另附 R²、MAE、MSE）；特徵數與 `alpha` 由 inner CV 決定；選擇規則與 tie-break 有文件；報告含第 2.4.1 節的偏誤陳述；凍結 predictor 有 Test 的 R²、MAE、MSE、RMSE（USD） | 缺任一候選；folds 不一致；以 p-value 或 Test 選模；把勝出者的 outer-CV 分數寫成不偏估計 | 比較表、選擇紀錄、Test 指標表 |
| OC-A5 預測區間 | MVM（M3）＋ENHANCED（E6） | 有預測圖（實際 vs 預測，附上下界，USD）；conformal quantile 與 coverage 的計算由獨立測試重算且一致；報告分開陳述 nominal target、理論保證及其 exchangeability 假設、observed coverage（含 n_test 與平均寬度），措辭不超過第 2.4.2 節 | 沒有預測圖或區間；計算與獨立重算不一致；陳述理論保證時沒有寫出 exchangeability 假設；把 group-aware 分區或隨機分派寫成已證明 exchangeability；把 observed coverage 寫成保證的證明 | 圖、測試輸出、報告的區間說明節 |
| OC-A6 可重現 | ENHANCED（E7、E8、E9） | 固定 seed 與相依版本；README 有重跑步驟；從乾淨環境完整重跑 notebook 成功，重跑的數值與報告一致；模組測試全部通過 | 重跑失敗；數值與報告不一致；測試失敗 | 重跑紀錄、測試輸出 |
| OC-A7 AI 協助與研究 | MVM（M5–M8） | 符合第 2.5.1 節：報告有「GPT 輔助內容」標示並揭露實際使用的工具；「NotebookLM 摘要」≥ 100 字，可追溯到 acceptor 提供的 NotebookLM 原始材料，經整理處有註明；有附來源的主流或更優解法比較；acceptor 提供的 ChatGPT 對話 PDF 已納入 | 缺任一項；任何對話或研究內容是捏造的；摘要含原始材料沒有的內容；以 Claude 紀錄或無關對話替代 ChatGPT PDF | 報告節次；acceptor 提供的原始材料；摘要與原始材料的對照 |
| OC-A8 繳交套件 | MVM（M9、M10） | ZIP `<學號>_hw2.zip` 內含 `<學號>_hw2.ipynb`、報告 PDF、ChatGPT 對話 PDF、支援模組、requirements、資料（或取得方式）；檔名用 acceptor 提供的實際學號；`home_work_02/README.md` 有流程、成果與 GitHub 連結（指向 `yotsubamomo/aiot-classwork` 的 `home_work_02/`）；ZIP 的 sha256 與檔案清單已記錄；追蹤檔案中沒有秘密 | 學號仍是佔位；缺必要檔案；README 缺流程、成果或連結 | ZIP 檔案清單與 sha256、README |

### 3.2 完成狀態（區分實作、發布與繳交）

| 狀態 | 意義 | 由誰完成 | 證據 | 與其他工作的關係 |
| --- | --- | --- | --- | --- |
| **S1 實作就緒** | OC-A1～A6 PASS；報告中除了 acceptor 證據外的內容完成，待填位置清楚標示 | Agents | 各 AC 的證據 | 不需要等任何 acceptor 輸入 |
| **S2 繳交套件就緒** | OC-A7、OC-A8 也 PASS：acceptor 證據與學號已納入，ZIP 已組好並核對 | Agents（取得 acceptor 輸入後） | ZIP sha256、檔案清單、README | 只受第 3.3 節的 acceptor 輸入影響 |
| **S3 GitHub 已發布** | 內容已合併進 `main`，README 的連結可以開啟 | **Acceptor**（RB-1；G8） | merge commit SHA；連結可開啟的確認 | 不阻擋 S1、S2 |
| **S4 iLearning 已繳交** | ZIP 已上傳到 iLearning | **Acceptor**（RB-2；G8） | acceptor 提供的繳交確認（日期與所上傳 ZIP 的 sha256 或檔名），記入 worklog | 不阻擋 S1、S2 |

- **本 Outcome Contract 的 work item 完成 = S2。** S3、S4 是 acceptor 的發布與繳交行為，分別記錄，不能由 Agent 宣稱已完成，也不屬於 Agent 工作的完成條件。
- S2 的 ZIP sha256 與檔案清單，在 S4 時用來核對所繳交的檔案就是驗證過的那一份。
- 等待 acceptor 動作（S3、S4 或第 3.3 節的輸入）只停止受影響的 AC，其他實作與驗證照常進行（治理 §1.5）。

### 3.3 只能由 acceptor 提供的輸入

| 輸入 | 對應 | 說明 |
| --- | --- | --- |
| ChatGPT 對話 PDF | OC-A7、OC-A8 | 第 2.5.1 節 |
| NotebookLM 原始研究材料（輸出與來源清單） | OC-A7 | 第 2.5.1 節 |
| 學號 | OC-A8 | 打包前提供（Q5） |
| S3 發布、S4 繳交 | 第 3.2 節 | RB-1、RB-2 |

在這些輸入提供前，Agent 完成其餘全部工作，並在報告中保留標示清楚的待填位置，不得以範例文字冒充內容。缺少輸入屬治理 §1.5 第 4 項的 boundary：只停止受影響的 AC。

### 3.4 Failure semantics

- 下列**不是** FAIL：
  - R²、RMSE 未達任何門檻（本契約沒有效能門檻）；
  - observed coverage 不等於 95%；
  - 選出的模型是全特徵 LR；
  - Lasso 把某些特徵係數壓為 0；
  - S3、S4 尚未發生。
- 下列一律是 FAIL：
  - 資料洩漏（OC-A3）；
  - 以 Test 或 Calibration 選模；
  - 計算與獨立重算不一致；
  - 捏造或替代證據（第 2.5.1 節）；
  - 陳述 conformal 保證時沒有寫出 exchangeability 假設，或聲稱它已被證明；
  - 把 ENHANCED 寫成老師要求；
  - 學號佔位進入最終 ZIP；
  - Agent 宣稱 S3、S4 已完成。
- Observed coverage 明顯偏離 95%（超出抽樣誤差）時，報告須說明可能原因，包括 exchangeability 假設可能不成立。這是需要解釋的結果，不是 FAIL，除非原因是計算錯誤或資料洩漏。

### 3.5 Verification intent

依 G8，驗證包括：
- 模組單元測試；
- leakage 測試（OC-A3）；
- conformal 計算的獨立驗證（OC-A5）；
- 從乾淨環境完整重跑 notebook（OC-A6）；
- 繳交文件檢查：OC-A2、A7、A8 要求的章節、標示、檔名、ZIP 內容，以及摘要與原始材料的對照。

具體的測試方法、framework 與 fixtures 屬 Spec／HOW。

## 4. Authority and authorization

| 項目 | 內容 |
| --- | --- |
| 接受前 | **沒有任何授權。** Bindings SA-1、SA-2 只在 Outcome Contract 被接受後適用（Bindings §2.5），所以接受前的 commit、搬移 `doc/requirement/` 與任何 Git 操作，都須由 acceptor 執行或另行明確授權 |
| 接受後的授權 | 在第 2 節的 boundary 內，授權具相應 authority 的 Agents 規劃、分解（由 Design Authority derive Spec 與 Tickets）、實作、審查、修正至 S2，範圍限 `home_work_02/` |
| Git（接受後） | **依 G8，Agents 只在 topic branch 上本機 commit，不 push、不開 PR。** 這是對 Bindings SA-1、SA-2 的收窄；acceptor 若要允許 push／PR，須在第 9 節寫明 |
| 保留給 acceptor | RB-1 合併進 `main`（S3）；RB-2 繳交（S4）；RB-3 憑證與第三方帳號（含 Kaggle、ChatGPT、NotebookLM 帳號）；RB-4 付費；RB-5 單元目錄外的檔案（含 `week05/`、root `CONTEXT-MAP.md`）與 `doc/requirement/`；RB-6 破壞性 git 操作 |
| Acceptor 輸入 | 第 3.3 節 |
| 不保留 | Spec review、獨立的 implementation authorization（Bindings §2.6） |

## 5. Relevant context

- **資料集核對證據**：Brief v0.3 §10。CSV sha256 `d0875baa0251b21d4bdc9d2ae940a4fe0bb6009824f23dd0e2a5b2bf04557b7e`；CC0-1.0；21,613 列 × 21 欄；0 缺值；21,436 個 `id`（177 筆重複交易）；`sqft_living = sqft_above + sqft_basement` 對全部列成立。
- **Spec 需處理的已知設計事項**（由 Design Authority 決定）：
  - 完全共線的處理方式；
  - `date` 與 `zipcode` 的處理；
  - 轉回 USD 時的偏誤修正；
  - 選模的 tie-break；
  - 離群值處理；
  - 報告 PDF 的產生方式；
  - 資料取得方式（隨附 CSV，或下載後核對）；
  - acceptor 原始材料在 repo 或 ZIP 中的存放位置。
- **參考**：`week05/multiple_linear_regression_crisp_dm.ipynb`（REFERENCE）；`week05/docs/` 課程講義（CRISP-DM、L6 multiple linear regression）。
- **期限**：2026-11-04（老師文件）。

## 6. Assurance path

- **Lane**：預期為 **Formal**（Spec＋Tickets＋Orchestrator）。工作包含多個彼此相依的 execution units（資料、選模、conformal、notebook、報告、打包），且需要等待 acceptor 的輸入（治理 §3.6-C；Bindings §4）。由 Design Authority 判定並留紀錄。
- **Audit**：Formal 下每個 Ticket 做 independent audit，每份 Spec 做 Spec Integration Audit；只有一張 Ticket 的 Spec 可以用 fast path（Bindings §5）。
- **高風險類別**：第一次正式 audit 前，由 Design Authority 為本單元確認（Bindings §5）。起草建議的候選：
  - H-2 老師指定的名稱與格式：`<學號>_hw2.ipynb`、`<學號>_hw2.zip`、「GPT 輔助內容」與「NotebookLM 摘要」標示、六個 CRISP-DM 階段；
  - 評估完整性：分區隔離、Test 只用一次、conformal 計算與假設陳述；
  - 證據真實性：第 2.5.1 節；
  - H-1 憑證：本作業不使用金鑰，預期不適用。
- **Release gate**：合併進 `main`（S3）前，須符合 Bindings §5 的 integration／release gates。

## 7. Stable reference

接受時以 commit SHA 固定本檔第 1–8 節與 Brief v0.3 的內容。本 draft 尚未 commit；接受用 commit 應包含的檔案見第 8 節 #2。

## 8. Activation preconditions（接受前或啟動 Formal run 前）

| # | 項目 | 狀態 |
| --- | --- | --- |
| 1 | **文件搬移**（Bindings §2.2；`CLAUDE.md` 單元文件位置），byte-identical：<br>`home_work_02/docs/HW2-requirements-Multiple Linear regression.txt` → `home_work_02/doc/requirement/`（sha256 須仍為 `a969e7e2…61ab`）<br>`home_work_02/docs/HW2_Grill_Brief_Draft_v0.1.md`、`v0.2.md`、`v0.3.md` → `home_work_02/doc/brief/`<br>搬完後刪除空的 `home_work_02/docs/`；本檔檔頭連結 `../../docs/HW2_Grill_Brief_Draft_v0.3.md` 改為 `../brief/HW2_Grill_Brief_Draft_v0.3.md` | 待 acceptor 執行或明確授權 |
| 2 | **接受用 commit**（topic branch，例如 `home_work_02-outcome-contract`），只包含：<br>`home_work_02/doc/requirement/HW2-requirements-Multiple Linear regression.txt`<br>`home_work_02/doc/brief/HW2_Grill_Brief_Draft_v0.1.md`、`v0.2.md`、`v0.3.md`<br>`home_work_02/doc/governance/outcome-contract.md`（本檔，含 #1 的連結修正）<br>`home_work_02/CONTEXT.md`<br>不包含：`week05/`（另一單元，governance off）、`grep.exe.stackdump`、root `CONTEXT-MAP.md`（RB-5；另案處理） | 待 acceptor 執行或明確授權（SA-1 在接受前不適用） |
| 3 | 第 9 節接受紀錄：acceptor 原文、日期、#2 的 commit SHA；同時確認第 4 節的 Git 收窄與第 2.5 節的語言 | 待 acceptor |
| 4 | Bindings §8.2 #3：Fable alias 實測未完成（HTTP 429）；是否阻擋第一次正式 audit 由 acceptor 決定 | 待 acceptor |
| 5 | Design Authority 確認 lane 與高風險類別（第 6 節） | 接受後 |

## 9. 接受紀錄

| 項目 | 內容 |
| --- | --- |
| 狀態 | **未接受** |
| Acceptor | — |
| Acceptor 原始指示（引用原文） | — |
| 日期 | — |
| 接受的 commit SHA | — |
| 接受時的修訂（若有） | — |

## 10. 修訂紀錄

### r1 → r2（2026-10-14；依 independent review F-01～F-04）

| Finding | 位置 | 變更 |
| --- | --- | --- |
| — | 檔頭 | 狀態改為 DRAFT r2；新增「取代 r1」與 r1 sha256；依據改為「核對 `main` `ee5d5b9` 的 Bindings b4」，並加列 §2.2、§2.5；聲明本檔與 Brief 不一致時以本檔為準 |
| F-01 | §2.4（拆為 2.4.1、2.4.2） | r1 的「exchangeability 來自整棟房屋的隨機分派」**已移除**。新增三層陳述：nominal target、理論保證與其假設、observed coverage。明寫 exchangeability 是假設，group-aware 分區與隨機分派都不能單獨證明交易層級分數的 exchangeability。補充 log 與 exp 轉換對 coverage 的影響；把以房屋為單位的 conformal 列為「未採用的替代設計」。方法本身（60／20／20 group-aware、95% split conformal、log 尺度校準、實測 coverage 與寬度）不變 |
| F-01 | §2.3、§3.1 OC-A5、§3.4 | Non-scope 加「新的 conformal 演算法」。OC-A5 的 PASS／FAIL 加入三層陳述與假設措辭。Failure semantics 加入相應的 FAIL 條件，以及偏離時須說明「假設可能不成立」 |
| F-02 | §2.2 M5、§2.3、新增 §2.5.1、§3.1 OC-A7、§3.4 | M5 明確為「acceptor 與 ChatGPT 進行、與本作業相關的真實對話」。新增 §2.5.1 證據規則：允許忠實編輯 NotebookLM 原始材料（排版、修錯字、摘錄、翻譯、縮寫），須可追溯並註明整理；禁止捏造研究與對話；禁止以 Claude 紀錄或無關對話替代 ChatGPT PDF；Claude Code 的使用只作補充揭露。r1「Agent 不得撰寫摘要內容」改為「不得在沒有原始材料時撰寫，也不得加入原始材料沒有的內容」 |
| F-03 | 新增 §3.2；§3.1 OC-A8；§3.3（原 3.2）；§4 | 新增完成狀態 S1～S4：實作就緒、繳交套件就緒、GitHub 已發布（acceptor）、iLearning 已繳交（acceptor）。work item 完成＝S2；S3、S4 不阻擋 S1、S2，Agent 不得宣稱其完成。OC-A8 改名「繳交套件」，加入 ZIP sha256 與檔案清單，以及連結的指向。S4 的繳交確認用於核對所繳交的 ZIP |
| F-04 | 檔頭、§2.1、§4、§7、§8 | 核對 `main` `ee5d5b9` 的 Bindings b4。§4 新增「接受前沒有任何授權」（SA-1、SA-2 只在接受後適用）。§8 #1 列出精確的搬移（含老師文件 sha256 與連結修正），#2 列出接受用 commit 的精確檔案清單與排除項目。本次未搬移任何檔案、未 commit、未修改單元外的檔案 |
| — | §3.5（原 3.4） | 驗證加入「摘要與原始材料的對照」 |
| — | §5 | Spec 事項加入「acceptor 原始材料的存放位置」 |

G1–G8 原文與 C1–C4 未變更（見 Brief v0.3 §3、§4）；本檔沿用其內容，未改寫。
