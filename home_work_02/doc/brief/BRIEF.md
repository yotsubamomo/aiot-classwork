# HW2 Multiple Linear Regression — Brief（Draft，待 acceptor 確認）

- **狀態**：**FINAL DRAFT**，2026-10-18，供 acceptor 確認。MATT Grill 的 frontier 已清空（Round 1–4，Q1–Q43）；Brief Review 的 BR-01～BR-04 全部 Resolved（§13）。尚未授權 Spec、Tickets、實作、commit、push 或 merge。
- **Grill 紀錄**：[`HW2_Regrill_Brief_Draft_v0.1.md`](HW2_Regrill_Brief_Draft_v0.1.md)（來源盤點、各輪決定與 acceptor 原文約束、一致性檢查）。
- **詞彙**：[`../../CONTEXT.md`](../../CONTEXT.md)。本檔的用詞以它為準。
- **來源標記**：[T] 作業頁正文；[S] 作業頁「補充」段；[X] 交付範例 SRC-3；[D Qn] acceptor 在 Grill 第 n 題的決定；[F] 查證過的事實；[A] 起草假設（留給技術設計，可被 Spec 改變）。

## 1. 目標

以 Kaggle **House Sales in King County, USA** 資料集完成一份遵循 CRISP-DM 六階段、可重現的多元線性回歸分析，預測房屋成交價：比較五種特徵選擇方法在 k = 1…18 的表現，以訓練資料的交叉驗證選模，在保留的測試集上做一次評估，為每筆測試交易提供有統計定義的 95% 預測區間，並以靜態互動 dashboard 發布結果。交付老師要求的主程式、PDF 報告、AI 協助證據與學號 ZIP，加上 GitHub Pages 上的 dashboard。[T][D Q1–Q10]

## 2. 來源與地位

| 來源 | 檔案 | 地位 |
| --- | --- | --- |
| 作業頁正文 | `doc/requirement/` SRC-1（`.txt`）、SRC-2T（`_SRC-2_2026-10-18.txt`；SRC-2 PDF 本機保留、不公開，sha256 `1b3a5aad…39d7`） | 正式需求 [T] |
| 作業頁「補充」段 | SRC-2T p.2–p.4 | 建議 [S]；採用與否逐項由 Grill 決定 |
| 交付範例 | SRC-3 `50 Startups_…Explorer.pdf`（老師 DIC-2 網站列印，sha256 `388a78c0…4789`；原始碼 `huanchen1107/AIoT-DIC2-MultipleLR` @ `8b65e3bd`，無授權條款） | 成果形式參考 [X]，Option A：結果類型與呈現可比，資料集／演算法／數值可不同，不複製程式與文案 |
| week06 講義與 DIC-2 實作 | `week05/docs/`（untracked）、`week06/` | 方法與課堂期待；`week06/` 是本專案已驗證的技術前例 |
| 課堂口頭要求 | — | **Classroom Verbal Requirement / User Confirmation**：dashboard 是必要交付。作業頁與講義文字都沒有要求網站，報告不得宣稱有 [F][D] |

## 3. 範圍

### 3.1 必要（老師要求）[T]

| ID | 要求 | 本專案的落實 |
| --- | --- | --- |
| T-資料 | Kaggle 公開資料集，10–20 個特徵；標示來源與連結 | King County，19 個 source features；採正文與補充交集 **14–20**，編碼前計數、不含 `id` 與 `price`；報告引用兩條原文並說明採用的解讀 [D Q1、Q2] |
| T-模型 | 線性回歸預測；必做特徵選擇與模型評估 | §4–§5 |
| T-預測圖 | 預測圖加上信賴區間或預測區間 | 95% 預測區間，§6、§7 [D Q3、Q43] |
| T-CRISP-DM | 六階段說明 | notebook 與報告各有六章 [D Q7、Q42] |
| T-AI | ChatGPT 對話匯出 PDF；NotebookLM 研究摘要 ≥100 字；標示「GPT 輔助內容」「NotebookLM 摘要」 | §9 |
| T-繳交 | 主程式 `<學號>_hw2.ipynb`；PDF 報告（CRISP-DM、GPT 對話、NotebookLM 摘要、主流或更優解法比較）；ZIP `<學號>_hw2.zip` | §8 |
| T-GitHub（optional 條款） | 有 GitHub 時提供連結並在 README 整理流程與成果 | 本專案使用 GitHub，因此必做 [D Q39] |
| T-評分 | 文件 50%／結果 50%；「Kaggle 名次（若有）」 | King County 無競賽名次，報告說明不適用並以預測結果評估替代 [D Q38] |

### 3.2 必要（課堂口頭要求＋acceptor 決定）

- **Dashboard**：靜態互動頁，GitHub Pages，`home_work_02/index.html`，網址 `https://yotsubamomo.github.io/aiot-classwork/home_work_02/`。額外交付，不取代任何老師要求的檔案 [D 1a–1e、Q40]。
- **採用的補充建議** [S]：Adjusted R²、五大回歸假設診斷、Deployment 的模型解釋、Ridge／Lasso 對照 [D Q9]。報告中標為「依老師補充建議」，不寫成老師要求。

### 3.3 選配

- Dashboard 的係數表、Test 殘差表、全部結果表 [D Q5]。
- 額外的診斷圖（只用 training set）。

### 3.4 不做

- SelectKBest、permutation importance、Exhaustive 作為特徵選擇方法 [D Q11]；在 encoded column 層級選擇 [D Q12]。
- 刪除或截尾異常值 [D Q15]。
- 改用補充段推薦的資料集 [D Q2]。
- 後端、API、資料庫、Vercel [D Q6、Q22]。
- Ridge／Lasso 的即時預測與預測區間 [D Q31]。
- 以 Adjusted R² 選模；在 USD 尺度或對 Ridge／Lasso／CV 聚合值套古典 Adjusted R² [D Q21、Q29]。
- 任何捏造或替代的 ChatGPT、NotebookLM、公開來源證據 [D Q36]。

## 4. 資料與前處理

- **資料** [F]：Kaggle `harlfoxem/housesalesprediction`，`kc_house_data.csv`，CC0-1.0；2026-10-14 驗證：21,613 列 × 21 欄、0 缺值、21,436 個 `id`（177 筆重複交易）、`price` 75,000–7,700,000 USD、`sqft_living = sqft_above + sqft_basement` 對每列成立、`zipcode` 70 個值、`date` 字串。**實作時須重新下載並核對 sha256 與欄位數** [D Q2]。
- **資料檔**：commit 至 `home_work_02/data/`，載入時核對 sha256 `d0875baa0251b21d4bdc9d2ae940a4fe0bb6009824f23dd0e2a5b2bf04557b7e`（若重新下載後不同，記錄為 re-pin）[D Q35]。
- **特徵計數**：source features 19（CSV 欄位扣除 `id`、`price`）；建模 feature groups 18（`sqft_basement` 因完全共線不進模型）。報告同時陳述兩個數字與計數規則 [D Q1、Q16]。
- **固定前處理** [D Q16]：`date` → 距基準日天數；`yr_renovated` → `is_renovated` 旗標＋有效年份；`zipcode` → one-hot，整組視為一個 feature group；`sqft_basement` 不進模型；其餘照原值。所有衍生欄可追溯到其 source feature。需要 fit 的前處理（one-hot 類別、標準化參數）只以當次訓練列 fit [D Q13、Q33]。
- **目標**：以 log(price) 建模；預測、區間與指標以 USD 報告；報告明確區分 exp(ŷ_log)（條件中位數的估計）與條件平均 [D Q14]。
- **異常值**：不刪除；在 Data Understanding 揭露並診斷其影響 [D Q15]。
- **分割**：80/20 train/test，固定 seed，**以房屋 `id` 分組**；CV 折同樣分組。Test 在所有模型選擇固定後只評估一次 [D Q4、Q33]。

## 5. 特徵選擇、模型與比較

- **正式比較的方法** [D Q11]：A All-in（baseline）、B Forward SFS、C Backward SFS、D RFE、E Lasso 路徑排序取 top-k。**講義方法對照**：F p-value backward elimination，做一次、不進 k 路徑。
- **All-in baseline 的定義**（BR-02）：A 是**單一模型**——以全部 18 個 feature group 擬合的 OLS，沒有 k 路徑；它等於 B、C、D 路徑在 k = 18 的端點。比較方式：A 的 CV 指標在「指標 vs k 圖」中以水平參考線呈現，在比較表中佔一列；A 本身就是它的 CV winner，所以與其他方法的 CV winner 一起競爭整體 CV winner，並在 test 上評估一次。Dashboard 的方法選單中，A 的 k 固定為 18，不提供 k 切換。
- **選擇單位**：feature group；同一 source feature 的 encoded columns 同進同出 [D Q12]。
- **k 的範圍**：每個方法 k = 1…18 的完整路徑 [D Q34]。**執行時間必須量測並記錄；若成本過高，先回報可行的改善方案，不自行縮小範圍。**
- **公平性** [D Q13]：同一 train/test split、training set 內同一組分組 CV 折、同樣的前處理規則；每個 k 以 CV RMSE（USD）評分。
- **模型**：每個方法的每個 k 都 fit OLS（log 尺度）；Ridge 與 Lasso 用全部 group、alpha 以 training CV 選，作為對照 [D Q20]。
- **最佳的定義** [D Q20]：各方法的 **CV winner**＝CV RMSE 最小的 k；整體 CV winner＝各方法 CV winner 中 CV RMSE 最小者。Test evaluation 只對各方法的 CV winner、All-in baseline 與整體 CV winner 各報一次（同一模型不重複評估；BR-01），是描述性比較；**test 排名與 CV 排名不同時不換模型**。
- **最終模型** [A]：整體 CV winner 在整個 training set 上重新擬合，用於 Deployment、`predict_price()`、pickle 與報告主要結果。
- **指標** [D Q21、Q29]：CV 與 test 都報 MAE、MSE、RMSE、R²（USD 尺度，以回轉後預測計算，標明）。Adjusted R² 只對 OLS 子集模型、在 log 尺度以古典公式（n_train、實際 model rank）計算，與 log 尺度 R² 並列；Ridge／Lasso 與 CV 聚合值不套用；任何替代統計量都要明確定義並標示。
- **統計推論**：自由度與秩一律以實際 design matrix 為準，不是 source feature 數 [D Q16]。

## 6. 預測區間與診斷

- **方法** [D Q17]：參數式 OLS 預測區間，log 尺度：ŷ ± t·√(s²(1 + x₀ᵀ(XᵀX)⁻¹x₀))，exp 回 USD（不對稱）。只提供給 OLS 子集模型。
- **陳述限制**：假設殘差常態、同質變異、獨立；特徵選擇後的推論與可能的模型誤設會影響名目涵蓋率；**不宣稱保證 95% 經驗涵蓋率** [D Q17]。
- **驗證** [D Q18]：報告 test 經驗涵蓋率、涵蓋計數、n_test、平均寬度（USD）、抽樣不確定性。偏離 95% 需分析原因（連到診斷），不自動判定失敗。
- **五大假設診斷** [D Q9、Q19]：線性、誤差獨立、同質變異、殘差常態、多重共線性；用最終模型在 training set 的殘差（log 尺度）；每項有數值或圖形證據與解讀；討論 177 筆重複交易對獨立性的影響；違反只需揭露與分析，不算失敗。具體統計量屬 Spec [A]。

## 7. Dashboard

- **技術** [D Q6、Q30、Q40]：Python 匯出 `model_data.json/js` → vanilla HTML/CSS/JS＋Chart.js；Chart.js 打包在 `home_work_02/assets/`，Pages、`file://`、ZIP 都完全離線可用；無後端。
- **完全離線的驗收**（BR-04；Requirement／Acceptance，不是 HOW）：
  - 條件：把繳交 ZIP 解壓到一台**網路已停用**、沒有任何本機伺服器的機器上，以瀏覽器直接開啟解壓後的 `index.html`（`file://`）。
  - 必須正常：必要區塊 (1)(2)(3)(5)(6)(9) 全部渲染；方法與 k 切換有效；即時預測器輸入後給出點預測與 95% PI；實際 vs 預測圖可縮放檢視；圖表有 zh-TW 文字且無缺字。
  - 必須成立：頁面不發出任何對外網路請求（以瀏覽器開發者工具的網路面板核對為零，或以靜態掃描確認 html/js/css 中沒有外部資源 URL；文件內的超連結不算資源）；所有資料與程式庫都在 ZIP 內。
  - 由此而來的限制：資料載入方式必須在 `file://` 下可用（瀏覽器在 `file://` 封鎖 `fetch` 本機 JSON，所以資料以 `.js` 內嵌或等效方式提供——這是 HOW，但「`file://` 可用」是驗收）。
  - 同一份檢查也在 GitHub Pages 的網址上做一次（有網路）。
- **語言**：zh-TW [D Q8]。
- **必要區塊** [D Q5]：(1) 方法與 k 的控制；(2) KPI 卡；(3) 指標 vs k 圖（Ridge／Lasso 以參考線呈現 [A]）；(5) 即時預測器；(6) 實際 vs 預測圖；(9) 方法與限制。選配：(4) 係數表、(7) Test 殘差表、(8) 全部結果表。
- **操作行為** [D Q22]：選方法＋k → KPI、圖、預測器、實際 vs 預測圖同步更新；「比較全部」→ 各方法 k 路徑疊圖與各方法 CV winner 比較表。
- **資料來源與操作行為的分層規則**（BR-01，**Resolved**：acceptor 2026-10-18 確認方案 A）[D BR-01]：
  1. 任意 (方法, k) 的模型比較與 KPI 使用 **training CV** 結果（CV RMSE／MAE／MSE／R²、log 尺度 Adjusted R²），標示「訓練 CV」。
  2. 即時預測器使用目前選取的 (方法, k) 在**完整 training set 上擬合的 OLS 模型**。
  3. **Test evaluation 只針對**各方法的 CV winner、All-in baseline 與整體 CV winner；若為同一模型，不重複評估。
  4. Test KPI、實際 vs 預測圖、逐筆 95% PI 與 coverage 統計只使用第 3 點的 test 結果。
  5. 選取非 CV winner 的 k 時，test 區塊展示該方法 CV winner 的結果。
  - **UI 驗收**（acceptor 原文）：「Test 區塊必須明確標示正在展示的模型方法與 k。當目前選取模型不同於 Test 區塊模型時，應以清楚可見的提示說明兩者不同。Training CV 與 Test Evaluation 的資料來源標示必須清晰，不得混淆。不允許因 Dashboard 切換操作而產生新的 Test evaluation。model_data 僅包含已授權評估模型的 Test 結果，避免 Test 資料被當作互動式選模依據。」
  - 本規則細化 Q22 的「同步更新」，不改變 Q20；Q43 的逐筆 PI 驗收對每個被評估模型的全部 test 樣本成立。
- **即時預測器** [D Q22、Q31、Q32]：只對 OLS 子集模型；輸入為當前模型用到的 source feature 原始值（日期、建造年、整修年或未整修、zipcode 下拉、lat/long…），預設 training 中位數、範圍 training min–max，超出範圍警告但仍計算；JS 重做 §4 的全部轉換；輸出點預測＋95% PI（USD）。
- **實際 vs 預測圖** [D Q43]：對象為被授權評估 test 的模型（各方法 CV winner、All-in、整體 CV winner；BR-01）；全部 test 樣本；x＝Predicted Price、y＝Actual Price、log scale、y＝x 參考線、每筆的垂直 PI 線段、依實際價格是否落入 PI 著色、支援縮放與檢視。驗收：不得以抽樣或聚合取代逐筆資料；可讀可操作，不得嚴重遮蔽或卡頓；PI 上下界、涵蓋狀態與 coverage 統計和 Python 匯出一致；log 輸入值有效且大於零；繪圖最佳化技術不限。

## 8. 交付物與檔案

| 交付物 | 內容 | 來源 |
| --- | --- | --- |
| 主程式 | repo 內 `home_work_02/hw2.ipynb`；繳交時為 `<學號>_hw2.ipynb`，由打包步驟自同一檔產生（單一來源，不維護兩份）[D Q7、Q27] | T、D |
| 輔助模組與測試 | 單元內 Python 模組、`requirements.txt`（鎖版本）、Python 測試與 JS 一致性測試 | D Q10、Q23 |
| 結果產物 | 結果表 CSV、圖 PNG、`model_data.json/js`、示範用 pickle pipeline（Deployment 示範，不進 dashboard）[D Q24] | D |
| Dashboard | `index.html`＋`assets/`（含打包的 Chart.js） | D |
| PDF 報告 | 獨立文件（Markdown → PDF）；數字與圖全部引自匯出結果，不手抄 [D Q26]。章節：CRISP-DM 六章（含特徵選擇比較、假設診斷、區間驗證、模型解釋）、資料來源與研究脈絡、GPT 輔助內容、NotebookLM 摘要、主流或更優解法比較（3–5 個公開 King County 解法，附連結與不可比之處 [D Q37]）、dashboard 連結與截圖、附錄 ChatGPT PDF [D Q42] | T、D |
| README | 單元 `README.md`：目的、資料來源與授權、流程、成果、重跑步驟、dashboard 連結、檔案配置；root `README.md` 作業表與 `CONTEXT-MAP.md` 各加一列（root 檔案，動手前先說明）[D Q39] | T、D |
| 驗收清單 | `doc/acceptance/ACCEPTANCE.md`：每條要求與決定 → 可觀察檢查 → 證據位置 [D Q41] | D |
| ZIP | `<學號>_hw2.zip`：主程式（學號檔名）、報告 PDF、ChatGPT PDF、輔助模組、`requirements.txt`、資料 CSV、README、結果檔、dashboard 靜態檔 [D Q28] | T、D |

**Deployment 階段內容** [D Q25]：dashboard 連結與說明；`predict_price()` 示範預測新樣本；模型解釋（log 尺度係數的百分比解讀、標準化／one-hot 的讀法、特徵重要性）；使用限制（地區、期間、外推、區間假設）。

## 9. 只能由 acceptor 提供的輸入 [D Q27、Q36]

| 輸入 | 用途 | 規則 |
| --- | --- | --- |
| ChatGPT 對話 PDF | 報告附錄、ZIP | acceptor 本人與 ChatGPT 的真實對話匯出；不進 git |
| NotebookLM 原始輸出與來源清單 | 「NotebookLM 摘要」≥100 字 | acceptor 操作並提供；agent 只整理、摘要、翻譯，不新增內容或來源；不進 git |
| 學號 | 繳交檔名 | acceptor 已於 2026-10-18 提供；依 BR-03，追蹤檔案一律寫 `<學號>`，實際值只放本機未追蹤的打包設定與繳交 ZIP |
| iLearning 繳交、合併進 `main` | 發布與繳交 | acceptor 的動作 |

「GPT 輔助內容」節如實揭露 ChatGPT 與 Claude Code 各自的用途。所有證據必須真實且可追溯。

## 10. 驗證與驗收 [D Q10、Q23、Q41]

- 固定 seed、鎖版本的 `requirements.txt`、乾淨環境完整重跑後數字一致。
- 分組隔離測試：train/test 與每個 CV 折之間沒有共同的 `id`；需要 fit 的前處理只看到當次訓練列。
- Python/JS 一致性測試：點預測、PI 上下界、涵蓋狀態、前處理轉換（日期、整修年、zipcode one-hot）逐筆比對。
- Dashboard 人工檢查表：必要區塊、zh-TW 無缺字、Pages URL 可開啟、截圖。
- **完全離線檢查**（BR-04，§7）：ZIP 解壓、網路停用、無伺服器、`file://` 開啟；必要區塊與即時預測、縮放都正常；對外請求為零。
- **Test 暴露檢查**（BR-01）：匯出的 `model_data` 只含被授權評估模型（各方法 CV winner、All-in、整體 CV winner）的 test 結果；非 winner 的 (方法, k) 沒有 test 數字可顯示；dashboard 切換不觸發任何新的 test 計算。
- **資料來源標示檢查**（BR-01 UI 驗收）：test 區塊標示所展示的方法與 k；選取模型與 test 區塊模型不同時有清楚可見的提示；「訓練 CV」與「Test」標示不混淆。
- ACCEPTANCE.md 逐條對應老師要求與 Grill 決定。

## 11. 已知風險與處理

| 風險 | 處理 |
| --- | --- |
| Backward SFS、RFE 在 18 個 group × 分組 5 折 × k 路徑的執行時間 | 實作時量測並記錄；過高時回報改善方案給 acceptor，不自行縮小範圍 [D Q34] |
| 參數式 PI 的假設在房價資料上可能不成立，經驗涵蓋率偏離 95% | 報告分析原因並連到診斷；不宣稱保證 [D Q17、Q18] |
| `zipcode` 70 個 dummy 使係數表很長、部分 CV 折可能缺少某些類別 | 係數表是選配；one-hot 類別只取自訓練列，未見類別編為基準；秩檢查用實際矩陣 |
| 約 4,300 筆逐筆 PI 線段的渲染效能 | Q43 允許任何繪圖最佳化，但不得抽樣或聚合 |
| 公開 repo 與學號 | **規則（BR-03）**：任何追蹤檔案（含本 Brief、Grill 紀錄、CONTEXT.md、README、notebook、程式與測試）一律以 `<學號>` 佔位，不寫實際值；實際學號只存在於本機未追蹤的打包設定（路徑由 Spec 指定，並加入單元 `.gitignore`；目前的單元 `.gitignore` 只排除 SRC-2 PDF）與繳交 ZIP 的檔名。打包步驟從該設定讀取學號；驗收時以 `git grep` 確認追蹤檔案沒有實際學號 |

## 12. 留給技術設計的事項（HOW）[A]

seed 值；CV 折數（假設 5）；Ridge／Lasso 的 alpha 網格與標準化；Lasso 路徑與 p-value backward 在 group 層級的彙總規則；診斷的具體統計量與圖；報告 PDF 的產生工具；dashboard 字型、主題、URL 參數；打包腳本與 checksum 記錄方式；`model_data` 的 schema。

## 13. Brief Review 的處理（2026-10-18）

| Finding | 處理 | 狀態 |
| --- | --- | --- |
| BR-01 [High] Test 使用限制 vs 任意 (方法, k) 切換 | acceptor 確認方案 A（分層顯示）並補五條 UI 驗收；§7 寫入五點規則與 UI 驗收；§5 不變；§10 加 test 暴露與資料來源標示檢查；CONTEXT.md 的 Test evaluation 詞條補「只對被授權評估的模型」 | **Resolved**（2026-10-18） |
| BR-02 [Medium] All-in baseline 的含義 | §5 定義為單一模型（全部 18 group 的 OLS，等於 k=18 端點）；以參考線與比較表一列呈現；參與整體 CV winner 競爭；dashboard 中 k 固定；CONTEXT.md 加詞條 | 已處理，不改變 Q11 |
| BR-03 [Medium] 公開 repo 不出現學號 vs Brief 含學號 | 三份追蹤文件中的實際學號全部改為 `<學號>`；§11 寫明規則與驗收方式（`git grep`）；實際值只在本機未追蹤設定與 ZIP | 已處理，不改變 Q27 |
| BR-04 [Medium] 完全離線缺驗收 | §7 新增離線驗收條件（解壓、斷網、無伺服器、`file://`、必要功能、零對外請求、`file://` 可用的資料載入）；§10 加入檢查 | 已處理，不改變 Q30 |

## 14. 下一步（待 acceptor 確認本 Brief 後）

1. acceptor 確認本 Brief（或指出修改）。
2. 依 MATT 流程以本 Brief 產生 Spec（`/to-spec`），再拆 Tickets（`/to-tickets`）。這兩步與實作都尚未授權。
