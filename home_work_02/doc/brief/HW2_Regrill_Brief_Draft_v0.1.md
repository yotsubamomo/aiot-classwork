# HW2 — Re-Grill Brief Draft v0.1

- **狀態**：DISCUSSION DRAFT（2026-10-18）。這是 HW2 重新開始的 Grill 紀錄，不是 Outcome Contract，不是 Spec，不授權任何實作。
- **起點**：branch `home_work_02-regrill`（自 `main` 建立，commit `12fff506`），只含老師的需求來源。
- **舊紀錄**：先前的 Grill（G1–G8、C1–C5）、Outcome Contract r4、Spec v1.1，以及 OC v2 草稿與 F-1～F-7、U-1～U-5 的裁決，都保留在 branch `home_work_02-outcome-contract` 與 `home_work_02-rebaseline-oc-v2`，作為歷史參考。**本次 Grill 不沿用任何舊決定**，除非 acceptor 在本 Brief 中重新確認。
- **撰寫者**：無角色主 session（Bindings b5 §3.5）。Grill 不創造 authority（治理 §3.2）。
- **Governance**：`home_work_02/` governance on（Bindings b5）。本 Grill 收斂到新的 Outcome Contract 草稿。

**Statement classes**：
- **[T]** 老師的 HW2 作業頁文字（SRC-1／SRC-2）；
- **[X]** 老師提供的範例（SRC-3）；
- **[D]** acceptor 在本 Grill 的決定（逐字或忠實摘要，附日期）；
- **[F]** 查證過的事實；
- **[R]** 起草建議，經 acceptor 裁決才有效。

## 1. 來源登錄

| ID | 檔案（`doc/requirement/`） | 性質 | sha256 | 追蹤 |
| --- | --- | --- | --- | --- |
| SRC-1 | `HW2-requirements-Multiple Linear regression.txt` | acceptor 轉寫的 iLearning HW2 作業頁（2026-10-14 版） | `a969e7e2228e97a35027ad63d3747f2e502bdd685cf7cfca30aaab50048761ab`（git blob 內容） | 追蹤 |
| SRC-2 | `HW2-requirements-Multiple Linear regression.pdf` | iLearning HW2 作業頁列印（老師 2026-10-18 更新；列印 2026-10-18 02:59；4 頁）。正文與 SRC-1 相同，另有「==== 補充 ====」段 | `1b3a5aad1c261425eb34f2eb46aebe6a62c73aba4fbf2d67a166fe9df28639d7` | 不追蹤（單元 `.gitignore`；acceptor 2026-10-18 決定不公開） |
| SRC-2T | `HW2-requirements-Multiple Linear regression_SRC-2_2026-10-18.txt` | SRC-2 的忠實、標示頁碼的轉寫 | git blob `d185f89d5a3d923e24bb581eecd95481cfe2f335`；內容 sha256 `e5eb6a315dd5860e7562467012c748911454becb0c6bccde95823d1f0834e77c` | 追蹤 |
| **SRC-3** | `50 Startups_ Multiple Linear Regression & Feature Selection Explorer.pdf` | **需求範例**：老師在 week06 DIC-2 練習提供的成果網站列印檔（5 頁，1,203,722 bytes；PDF CreationDate `D:20261014105849+00'00'`＝2026-10-14 18:58 +0800）。<br>網站 `https://huanchen1107.github.io/AIoT-DIC2-MultipleLR/`；原始碼 `huanchen1107/AIoT-DIC2-MultipleLR`（public），commit `8b65e3bd9745e650ae7bea28f9562c059d5029ed`（2026-10-14 03:59 UTC；2026-10-18 查詢時仍是 HEAD，與 `week06/doc/spec/SPEC.md` 固定的 commit 相同） | `388a78c0af7dcf40996b9068f8d640cda654902023b671d205abdd67998f4789`（與 acceptor `~/Downloads` 的副本相同） | **追蹤**（acceptor 2026-10-18 決定 commit PDF） |

### 1.1 SRC-3 的證據性質

- [D] acceptor 2026-10-18：「這一份是需求的範例，來源是week06 的練習項目，最終交付是會需要這個網站一樣的發佈的。」
- [F] 範例網站的內容：
  - 50 Startups 資料集；
  - 比較 Lasso、Forward SFS、RFE、ElasticNet、Exhaustive Search 五種特徵選擇，k = 1～5；
  - 指標 Test RMSE、R²、Adjusted R²、MAE、F-statistic；
  - OLS 方程式與係數表（標準誤、t、p-value、95% 信賴區間、VIF）；
  - 即時預測器；
  - Test 殘差排行；
  - 頁尾的參考資料與致謝。
- [F] 範例 repo 沒有授權條款（GitHub `license: null`），所以只能參考它的形式與呈現，**不能複製程式碼、文案或資料**。它的部署設定包括 GitHub Pages workflow 與 Vercel（`api/`、`vercel.json`）。
- [D] acceptor 2026-10-18 確認：「SRC-3 只當交付形式的範例，內容逐項在 Grill 決定。」範例中的具體項目——資料集、五種方法、k 的範圍、各項指標與圖表——不會自動成為 HW2 的要求。HW2 的作業文字（SRC-1／SRC-2）仍是內容要求的依據。
- [F] 範例網站的資料集（50 Startups，4 個特徵）本身不符合 HW2 的「10 至 20 個特徵」。這也說明它是形式範例，不是 HW2 的解答。

## 2. Frontier 紀錄

### Frontier 1 — 網站交付（已決定；出處待補）

**證據**：
- [T] HW2 正文只寫「(optional) 若上傳至 GitHub，或是以colab撰寫，需提供連結，並在 README.md 中整理流程與成果。」沒有提到網站。
- [X] SRC-3 是發佈的成果網站。
- [F] 本 repo 的 `main` 已以 GitHub Pages 發佈 week06 的同類網站（`/week06/`）。

**acceptor 決定（2026-10-18）**：

| 項目 | 決定 | 說明 |
| --- | --- | --- |
| 1a. SRC-3 的登錄 | [D] 登錄為 SRC-3，PDF 一併 commit | 第 1 節 |
| 1b. 義務的來源 | [D] **老師有要求（有出處）** | 報告將標「老師要求」。**出處尚待 acceptor 提供**（日期、場合或檔案），用來記錄這個要求；在提供前，這一項是「老師要求、出處待補」 |
| 1c. 發佈形式 | [D] **靜態網站＋GitHub Pages** | 比照 week06：結果在分析程式中預先計算並匯出，網站以靜態檔案呈現與互動，發佈在本 repo 的 GitHub Pages。不需要伺服器、部署帳號或金鑰 |

| 1d. 網站和必交項目的關係 | [D] 「網站是額外的交付，主程式 .py/.ipynb、PDF 報告、學號 ZIP 照老師正文都要交。」 | 網站不取代任何老師正文的必交項目 |
| 1e. SRC-3 的定位 | [D] 「SRC-3 只當交付形式的範例，內容逐項在 Grill 決定。」 | 第 1.1 節 |

**1b 的出處（2026-10-18 補上）**：
- [D] 「Dashboard 的要求來自老師課堂上的口頭說明。這是本專案已確認的必要交付項目。」
- 來源標記：**Classroom Verbal Requirement / User Confirmation**。
- [F] 作業頁（SRC-1／SRC-2）與 week06 講義（`week05/docs/` L4-2、L5、L6）的文字都沒有要求網站或 dashboard；子代理 2026-10-18 以 網站／dashboard／GitHub Pages／Streamlit 搜尋，無相符文字。**不得宣稱作業 PDF 或講義明文要求網站。**
- 網站的內容範圍：見 Round 1 Q5。

### Round 1（MATT Grill，2026-10-18）— 全部決定

Acceptor：「Q1–Q10：原則上全部接受你提出的建議方案」，並附下列約束（逐字摘錄於「約束」欄）。

| # | 題目 | 決定 [D] | 約束（acceptor 原文） |
| --- | --- | --- | --- |
| Q1 | 特徵數規則 | 正文 10–20 與補充 14–39 的交集 | 「採用 14–20 個原始輸入特徵，編碼前計數，不含 ID 與 Target。」 |
| Q2 | 資料集 | King County House Sales（Kaggle `harlfoxem/housesalesprediction`） | 「暫定 King County House Sales；請保留資料集來源、授權及實際欄位數驗證證據。」[F] 2026-10-14 驗證：CC0-1.0；`kc_house_data.csv` sha256 `d0875baa0251b21d4bdc9d2ae940a4fe0bb6009824f23dd0e2a5b2bf04557b7e`；21,613 列 × 21 欄；原始特徵 19 個（扣除 `id`、`price`）；實作時須重新核對 |
| Q3 | 區間類型 | 95% 預測區間 | 「區間必須有正確的統計定義，不能只是以 RMSE 畫出固定寬度的帶狀區間。」 |
| Q4 | 評估協定 | 固定 train/test split | 「特徵選擇與調參僅使用 training data，test set 保留至最終評估。」 |
| Q5 | Dashboard 區塊 | 必要：1 控制、2 KPI、3 指標 vs k 圖、5 即時預測器（含區間）、6 實際 vs 預測圖（含區間）、9 方法與限制 | 「4 係數表、7 Test 殘差表、8 全部結果表為選配。」 |
| Q6 | 技術堆疊 | 沿用 week06：Python＋Vanilla JS＋Chart.js 靜態部署 | 「優先沿用 week06 已驗證的 … 架構。」 |
| Q7 | 主程式 | Notebook 為主程式與 dashboard 資料來源 | 「Notebook 為主要可重現分析程式及 Dashboard 資料產生來源。」 |
| Q8 | 語言 | zh-TW | 「Notebook、報告與 Dashboard 使用繁體中文。」 |
| Q9 | 補充段評估項目 | Adjusted R²、模型解釋、五大假設診斷、Ridge／Lasso 比較都納入 | 「假設違反應揭露及分析，不直接判定作業失敗。」 |
| Q10 | 可重現 | 固定 seed、鎖版本、乾淨環境重現、Python／JS 預測一致性測試 | — |

**Acceptor 另提供的事實**：
- 學號（acceptor 已於 2026-10-18 提供；依 BR-03 不記錄在追蹤檔案中，以 `<學號>` 代替）：主程式 `<學號>_hw2.ipynb`；繳交檔 `<學號>_hw2.zip`；其餘檔名依老師要求與專案慣例。
- SRC-3 採 **Option A**：結果類型與呈現可比；資料集、演算法、特徵組合可以不同；不把範例數值當成實驗結果。

**Acceptor 指定的 Round 2 優先議題**：(1) 具體特徵選擇方法與比較公平性；(2) King County 的目標轉換、異常值處理及其對預測區間的影響；(3) 95% 預測區間的建構、驗證與假設限制；(4) Dashboard 各操作的預期行為與驗收；(5) 要比較的模型、特徵組合與輸出；(6) Deployment 階段與正式報告的交付邊界。只影響 HOW 的事項留給技術設計。

### Round 2（2026-10-18）— 全部決定

Acceptor：「Q11–Q28: Accept your recommended options, subject to the corrections and qualifications below.」「約束」欄為 acceptor 原文（英文逐字）。

| # | 題目 | 決定 [D] | 約束（acceptor 原文） |
| --- | --- | --- | --- |
| Q11 | 特徵選擇方法 | A All-in、B Forward SFS、C Backward SFS、D RFE、E Lasso 路徑 top-k 為正式比較；F p-value backward 為講義方法對照；不做 G SelectKBest、H permutation importance、I Exhaustive | "F as a separate lecture-method reference. Exclude G/H/I." |
| Q12 | 選擇單位 | Source feature | "Encoded columns belonging to one source feature must be selected or excluded together." |
| Q13 | 公平比較 | 同一 train/test split、train 內同一組 CV 折、同樣前處理；各方法以 CV RMSE 選 k | "Test data must not influence model or feature selection." |
| Q14 | 目標轉換 | log(price) 建模；預測與指標以 USD 報告 | "Explicitly distinguish exp(log prediction) from the conditional mean on the original scale. Preserve consistent statistical interpretation across point predictions and intervals." |
| Q15 | 異常值 | 不刪除；記錄並診斷其影響 | "Do not remove outliers. Document and diagnose their effects." |
| Q16 | 固定前處理 | `sqft_basement` 不進模型；`date` → 天數；`yr_renovated` → 旗標＋有效年份；`zipcode` one-hot 為一個 source feature group | "Ensure all derived columns and transformations are traceable to their source features. The actual design-matrix rank and degrees of freedom must be used for statistical inference, not the source-feature count." |
| Q17 | 預測區間建構 | 參數式 OLS 預測區間為主 | "Report the assumptions and limitations, including effects of feature selection and possible model misspecification. Do not claim guaranteed 95% empirical coverage." |
| Q18 | 預測區間驗證 | 報告 test 涵蓋率、涵蓋計數、n_test、平均寬度、抽樣不確定性 | "Coverage deviation requires analysis, not automatic rejection." |
| Q19 | 假設診斷 | 最終模型的 train 殘差（log 尺度） | "discuss the implications of repeated property transactions." |
| Q20 | 模型與最佳定義 | (a)：各方法各 k fit OLS；Ridge／Lasso 為對照；各方法最佳＝CV RMSE 最小的 k；整體最佳＝各方法最佳中 CV RMSE 最小者；test 對各方法最佳各報一次 | "Use CV for model selection; test results must not feed back into selection. Clearly distinguish the overall CV-selected winner from final test evaluation." |
| Q21 | 指標 | MAE、MSE、RMSE、R² 以 USD 尺度 | "For OLS, compute Adjusted R² using the appropriate sample size and actual model rank. Do not apply a common ordinary OLS Adjusted R² formula indiscriminately to Ridge, Lasso, or aggregated CV results. Any alternative statistic must be explicitly defined and labeled." |
| Q22 | Dashboard 操作 | (1) 選方法＋k 同步更新；(2) 比較全部；(3) 預測器只顯示當前模型的特徵，預設 train 中位數、範圍 train min–max、超出範圍警告仍計算；(4) 無後端 | "Distinguish opening from file:// with network access from fully offline operation. If full offline support is claimed, bundle the required frontend dependencies." |
| Q23 | Dashboard 驗收 | 自動測試＋人工檢查表 | "Python/JS consistency checks must cover point predictions, applicable intervals, and relevant preprocessing behavior." |
| Q24 | 輸出產物 | CSV、PNG、JSON/JS、示範用 pickle pipeline | — |
| Q25 | Deployment 內容 | dashboard 連結與說明；`predict_price()` 示範；模型解釋；使用限制 | — |
| Q26 | 報告 | 獨立 PDF 報告 | "with results derived from the reproducible analysis rather than manually maintained numerical copies." |
| Q27 | 材料與學號 | ChatGPT／NotebookLM 材料不進 git；repo 內 notebook 為 `hw2.ipynb`；繳交時為 `<學號>_hw2.ipynb`、`<學號>_hw2.zip` | "Ensure packaging does not create two independently maintained versions of the notebook." |
| Q28 | ZIP 內容 | 含靜態 dashboard 與其他必交產物 | — |

### Round 2 後的一致性檢查（acceptor 要求；起草者自查）

| 主題 | 檢查結果 | 處理 |
| --- | --- | --- |
| Source feature 計數 vs 實際模型複雜度 | 計數規則給 19 個 source features（含不進模型的 `sqft_basement`），建模 group 18 個；design matrix 約 87 欄（`zipcode` 69 個 dummy＋其餘）。兩者用途不同：前者回答老師的特徵數條件，後者決定秩與自由度。**不矛盾，但報告與 dashboard 的「k」一律指 source feature 數，自由度與 Adjusted R² 一律用實際秩。** | 已寫入 CONTEXT.md（Model rank） |
| log 尺度建模 vs USD 點預測與區間 | exp(ŷ_log) 估計的是條件中位數（log 誤差對稱時），不是條件平均；log 尺度的 t 預測區間經 exp 回轉後仍是 price 的有效預測區間（單調轉換），但不對稱。USD 的 R² 是以回轉後預測算的，**不等於 log 模型自己的 R²**。 | **有一處需決定**：Adjusted R² 要以哪個尺度的 R² 計算（Round 3 Q29） |
| 模型選擇 vs 最終 test 評估 | 選擇只用 CV；test 對各方法最佳各報一次，是描述性比較；整體最佳不因 test 改變。 | 不矛盾；Brief 寫明「test 排名與 CV 排名不同時不換模型」 |
| 比較指標的統計效度 | 各方法共用同一組折 → CV RMSE 可比。Adjusted R² 只對 OLS 子集模型定義；Ridge／Lasso 與 CV 聚合值不套用。 | 不矛盾；與 Q29 一併定案 |
| 靜態託管 vs 離線可用 | week06 的 Chart.js 來自 CDN：Pages 與 `file://` 都要網路。ZIP 內的 dashboard 若要離線開啟，必須把前端相依打包。 | **需決定**（Round 3 Q30） |
| 預測輸入 vs 衍生特徵轉換 | 預測器若接受 source feature 的原始值（日期、整修年份、zipcode），JS 必須重做 Q16 的轉換；Ridge／Lasso 另需標準化參數。 | **需決定**（Round 3 Q31、Q32） |

### Round 3（2026-10-18）— 全部決定

Acceptor：「Q29～Q42 全部依本輪建議採納」，另附三項執行邊界（逐字於「約束」欄）。

| # | 題目 | 決定 [D] | 約束（acceptor 原文） |
| --- | --- | --- | --- |
| Q29 | Adjusted R² 的尺度 | 只對 OLS 子集模型、在 log 尺度以古典公式（n_train、實際秩）計算，與 log 尺度 R² 並列；USD 尺度只報 R²，標為「以回轉後預測計算的 USD R²」 | — |
| Q30 | 離線可用 | 把 Chart.js 打包進單元 `assets/`；Pages、`file://`、ZIP 都完全離線可用 | — |
| Q31 | 預測器的模型範圍 | 只有 OLS 子集模型（各方法各 k）可即時預測，含點預測＋95% PI；Ridge／Lasso 只在比較表與圖 | — |
| Q32 | 預測器輸入 | 使用者填 source feature 的原始值；JS 重做 Q16 的全部轉換，由 Python/JS 一致性測試覆蓋 | — |
| Q33 | Train/test 分割 | 80/20、固定 seed、以房屋 `id` 分組；CV 折同樣分組 | 「Train/Test 及 CV 都必須以房屋 id 分組；特徵選擇、標準化及其他需要 fit 的前處理不得使用驗證折或 Test 資料。不要把『只多一行程式』當成已驗證的實作成本。」 |
| Q34 | k 的範圍 | 各方法完整路徑 k = 1…18 | 「不要預先宣稱 Backward SFS、RFE 在幾分鐘內完成。實際執行時間需要量測；若計算成本過高，先回報可行的改善方案，不自行縮小已決定的研究範圍。」 |
| Q35 | 資料檔 | commit `kc_house_data.csv`（CC0）至 `home_work_02/data/`，載入時核對 sha256 | — |
| Q36 | AI 證據分工 | ChatGPT PDF＝acceptor 本人的真實對話；NotebookLM＝acceptor 操作並提供原始輸出與來源；agent 只整理、摘要、翻譯；「GPT 輔助內容」如實揭露 ChatGPT 與 Claude Code 的用途 | 「ChatGPT PDF、NotebookLM 研究與公開來源比較都必須使用真實且可追溯的證據，不得補造內容或來源。」 |
| Q37 | 主流解法比較 | 3–5 個公開的 King County 解法，附連結，比較方法與自報指標並註明不可比之處 | — |
| Q38 | Kaggle 名次 | 不適用；報告在評分對應處說明並以預測結果評估替代 | — |
| Q39 | README 與 root 檔案 | 單元 README 含目的、資料來源與授權、流程、成果、重跑、dashboard 連結、檔案配置；root `README.md` 作業表與 `CONTEXT-MAP.md` 加一列，納入範圍，動手前先說明 | — |
| Q40 | Dashboard 位置 | `home_work_02/index.html`＋`assets/`；`https://yotsubamomo.github.io/aiot-classwork/home_work_02/` | — |
| Q41 | 驗收清單 | `doc/acceptance/ACCEPTANCE.md`：要求與決定 → 可觀察檢查 → 證據位置 | — |
| Q42 | 報告章節 | CRISP-DM 六章（含特徵選擇比較、假設診斷、區間驗證、模型解釋）、資料來源與研究脈絡、GPT 輔助內容、NotebookLM 摘要、主流解法比較、dashboard 連結與截圖、附錄 ChatGPT PDF | — |

### 全樹檢查（Round 3 後）

**留給技術設計的 HOW**（不影響範圍、驗收或可觀察行為；Brief 只記錄為假設）：
- seed 值；CV 折數（假設 5）；Ridge／Lasso 的 alpha 網格與標準化細節；
- Lasso 路徑與 p-value backward 在 feature group 層級的彙總規則（例如 group 進入順序、group F 檢定）；
- 假設診斷的具體統計量與圖（Q–Q、殘差 vs 擬合值、VIF、Durbin–Watson 等）；
- 報告 PDF 的產生工具；dashboard 的字型、主題、URL 參數；
- 打包腳本如何由 `hw2.ipynb` 產生 `<學號>_hw2.ipynb`（Q27 的單一來源要求以 checksum 記錄）。

**已隱含、在 Brief 中明寫的假設**：
- 「最終模型」（Deployment 的 `predict_price()`、pickle、報告主要結果）＝整體 CV winner，在整個 training set 上重新擬合。
- Dashboard 的「指標 vs k 圖」中，Ridge／Lasso 沒有 k，以參考線呈現。
- 發布到 Pages 需要合併進 `main`；合併是 acceptor 保留的動作，不屬於本 Brief 的工作完成條件。

### Round 4（2026-10-18）— Q43，frontier 清空

| # | 題目 | 決定 [D] | 約束（acceptor 原文） |
| --- | --- | --- | --- |
| Q43 | 實際 vs 預測圖的區間呈現 | (a)：x＝Predicted Price、y＝Actual Price、log scale、y＝x 參考線、每筆 test 樣本的垂直 PI 線段、依實際價格是否落入 PI 著色、支援縮放與檢視 | 驗收條件：「1. 所有 Test 樣本與逐筆 PI 資料都必須保留，不可透過抽樣或聚合取代。2. 圖表必須可讀且可操作，避免大量區間線段造成嚴重遮蔽或瀏覽器卡頓。3. PI 上下界、涵蓋狀態及 Coverage 統計必須與 Python 模型匯出結果一致。4. Log scale 的輸入值必須有效且大於零。5. 不限制具體繪圖最佳化技術，實作方式留給後續設計與 Executor。」 |

Frontier 已清空；Brief Draft 見 [`BRIEF.md`](BRIEF.md)。

### Brief Review（acceptor，2026-10-18）— BR-01～BR-04

Acceptor 審閱 BRIEF.md 後提出四項 finding，並規定：只修正有實質影響的問題；會改變 Q1–Q43 決定者先提選項；區分 Requirement／Acceptance 與 HOW；更新 Brief、本紀錄與詞彙。

| Finding | acceptor 原文（摘） | 處理 | 對既有決定的影響 |
| --- | --- | --- | --- |
| BR-01 [High] | 「§5 的 Test set 使用限制，與 §7 任意方法＋k 切換時的 KPI／預測圖更新行為，可能存在衝突。請提出資料來源及操作行為一致的修正方案，保留 Training CV 選模、Test 不參與選模，以及 Q43 的逐筆 PI 驗收意圖。」 | BRIEF.md §7 提出方案 A（分層：任意 (方法, k) 顯示 training CV 數字；test 區塊只對各方法 CV winner，含逐筆 PI 圖）與方案 B（全部候選評估 test 並標示）。暫以 A 撰寫 | A：細化 Q22 的「同步更新」，不改 Q20。B：改變 Q20「test 只對 CV winner 各評估一次」。**待 acceptor 選擇** |
| BR-02 [Medium] | 「All-in baseline 是完整模型，不應在未定義其含義的情況下被當成一般 k=1…18 的特徵選擇路徑。」 | 定義為單一模型（全部 18 group 的 OLS，等於 k=18 端點），以參考線與比較表一列呈現，參與整體 CV winner；CONTEXT.md 新增 All-in baseline | 不改 Q11 |
| BR-03 [Medium] | 「Brief 宣稱公開 Repo 不出現學號，但 BRIEF.md 本身已有學號。」 | 本紀錄、BRIEF.md、CONTEXT.md 中的實際學號全部改為 `<學號>`；規則：追蹤檔案一律佔位，實際值只在本機未追蹤的打包設定與 ZIP；驗收以 `git grep` | 不改 Q27 |
| BR-04 [Medium] | 「完全離線 Dashboard 應有對應驗收，包含 ZIP 解壓後、無網路、無後端環境下，必要圖表與互動預測功能正常運作。」 | BRIEF.md §7 新增離線驗收條件，§10 新增檢查 | 不改 Q30 |

**BR-01 裁決（acceptor 2026-10-18，Resolved）**：「確認採用方案 A（分層顯示）。」同意的行為（原文）：「1. 任意 (方法, k) 的模型比較與 KPI 使用 Training CV 結果。2. 即時預測器使用目前選取的 (方法, k) 在完整 Training set 上擬合的 OLS 模型。3. Test evaluation 僅針對各方法 CV winner、All-in baseline 及整體 CV winner（若為相同模型，不重複評估）。4. Test KPI、Actual vs Predicted 圖、逐筆 95% PI 與 Coverage 統計只使用符合上述條件的 Test 結果。5. 若選取非 CV winner 的 k，Test 區塊展示該方法 CV winner 的結果。」補充 UI Acceptance 五條見 BRIEF.md §7。效果：細化 Q22，不改 Q20。

**BR-01 當時提出的選項（紀錄）**：
- **A（建議）**：分層顯示。任意 (方法, k)：KPI／係數／即時預測器來自整個 training set 的擬合與 training CV，標示「訓練 CV」。Test KPI、實際 vs 預測圖（逐筆 PI、全部 test 樣本）、涵蓋率只對各方法的 CV winner、All-in 與整體 CV winner；選到非 winner 時顯示說明並呈現該方法 CV winner 的 test 圖。`model_data` 只匯出 CV winner 的 test 結果。
- **B**：全部 (方法, k) 都匯出並顯示 test 指標與逐筆 PI，頁面與報告註明選模只依 training CV。改變 Q20 的 test 評估次數語義。

## 3. Revision history

| Version | Date | Change |
| --- | --- | --- |
| v0.1 | 2026-10-18 | 重新開始的 Grill：來源登錄 SRC-1～SRC-3；Frontier 1 的 1a～1c 決定 |
| v0.1（rev 2） | 2026-10-18 | Frontier 1 的 1d、1e 決定；SRC-3 定位確認；1b 出處列為待補 |
| v0.1（rev 3） | 2026-10-18 | 改用 MATT Grill：來源盤點結果；1b 出處補為 Classroom Verbal Requirement / User Confirmation；Round 1 Q1–Q10 決定與約束；學號；Round 2 議題 |
| v0.1（rev 4） | 2026-10-18 | Round 2 Q11–Q28 決定與約束；一致性檢查（兩項待 Round 3 決定） |
| v0.1（rev 5） | 2026-10-18 | Round 3 Q29–Q42 決定與三項執行邊界；全樹檢查：HOW 清單、隱含假設、剩餘一題 |
| v0.1（rev 6） | 2026-10-18 | Round 4 Q43 與其驗收條件；Brief Review BR-01～BR-04 的處理與 BR-01 選項；學號改為 `<學號>` 佔位 |
| v0.1（rev 7） | 2026-10-18 | BR-01 裁決（方案 A＋UI 驗收）記錄為 Resolved；BRIEF.md 升為 FINAL DRAFT |
