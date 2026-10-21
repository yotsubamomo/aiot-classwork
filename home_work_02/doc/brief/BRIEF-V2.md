# HW2 Multiple Linear Regression — Brief V2（Enhance）

- **狀態**：**ACCEPTED**（rev 2），acceptor 2026-10-21 最終審查接受（接受項目：V1 不變的增量地位、SRC-4 差異與地位、Q1–Q24 決策紀錄、§3.5 四項覆寫、Exploratory run 的範圍／隔離／驗收、§12 A-1～A-3 最終決策、GitHub＋Web 主要交付與兩項加分目標）。MATT Grill V2 的 frontier 已清空（Round 1–3，Q1–Q24）；acceptor 第一次審閱的修正已套用（§13 末段）。已授權：以 V1＋V2 執行 `/to-spec` 產生既有 Spec 的增量修訂，Spec 完成後先提交審查。未授權：`/to-tickets`、實作、push、merge。**勘誤 E-1**（2026-10-21，§5.2、§5.5；Spec Review SR-V2-01 的資料洩漏修正，紀錄見 §13 末）。
- **與 V1 的關係**：本檔是 [`BRIEF.md`](BRIEF.md)（V1，2026-10-18 接受）的**增量**。V1 原文不改寫；V1 的每一條決定仍然有效，除非本檔在「§3.5 覆寫」明列。本檔沒有提到的事項，一律以 V1 為準。
- **觸發**：老師 2026-10-21 更新 iLearning 作業頁（SRC-4），新增兩項加分與數項正文變更（§2）。
- **詞彙**：[`../../CONTEXT.md`](../../CONTEXT.md)。本檔新用的 **Problem**、**Formal analysis**、**Exploratory run** 與改寫後的 **Dashboard**、**Submission package** 已登錄。
- **來源標記**：[T] V1 作業頁正文（SRC-1／SRC-2T）；[T4] SRC-4 正文；[X] 交付範例 SRC-3；[D Qn] acceptor 在 V2 Grill 第 n 題的決定；[F] 查證過的事實；[A] 起草假設（留給技術設計，可被 Spec 改變）。§12 的 A-1～A-3 原為提案，acceptor 2026-10-21 修改後接受，現為 [D]。

## 1. 目標（V2 增量）

在 V1 已完成並合併的 King County 正式分析之上，讓同一個 dashboard 能 (1) 以下拉切換兩種 problem，(2) 接受使用者任意輸入的資料集並在瀏覽器內完成多元線性回歸的特徵選擇與評估，以取得老師公告的兩項加分（合計 +3，直接計入期末總成績 [D Q6、補充]）。正式分析的所有數字、契約與已驗證產物維持不變。[T4][D Q2、Q4]

## 2. 來源與地位

| 來源 | 檔案 | 地位 |
| --- | --- | --- |
| 作業頁正文（新版） | `doc/requirement/HW2-req_new-20261021.txt`（SRC-4；acceptor 自 iLearning 頁面複製的純文字副本，2026-10-21；**沒有 PDF 列印**，不等待）[D Q1] | **正式需求 [T4]**，本次變更的主要依據 |
| 作業頁正文（舊版） | SRC-1、SRC-2T（V1 §2） | 歷史比較來源；SRC-4 未載明的內容不得推定老師已刪除，標「新版未載明」[D Q1] |
| 作業頁「補充」段 | SRC-2T p.2–p.4 | SRC-4 沒有這一段；地位「新版未載明」。V1 已採用的補充建議（Adjusted R²、診斷、解釋、Ridge／Lasso）不受影響 [D Q1、Q2] |
| 交付範例 | SRC-3（V1 §2）＋老師範例站 live 版與原始碼 `huanchen1107/AIoT-DIC2-MultipleLR` | 成果形式參考 [X]；[F] 老師 repo 於 2026-10-14 改為 Flask＋REST API＋Vercel serverless，其 Pages 版（截至 2026-10-21）沒有兩種 problem 的下拉，也沒有資料集輸入——這兩項功能沒有可參考的實作 |
| 老師給的範例資料 | `https://raw.githubusercontent.com/Avik-Jain/100-Days-Of-ML-Code/master/datasets/50_Startups.csv` | [F] 50 列、4 個來源特徵（R&D Spend、Administration、Marketing Spend 數值；State 類別）＋ Profit；回應標頭 `access-control-allow-origin: *`，瀏覽器可直接抓；來源 repo 為 MIT 授權 |

**SRC-4 相對 SRC-2 的正文差異** [F]：

| 項目 | SRC-2（10-18） | SRC-4（10-21） | 本檔處理 |
| --- | --- | --- | --- |
| 資料集特徵數 | 10 至 20 個 | **>13 個** | King County 19 個 source feature，符合；README／glossary 的「10–20」敘述改為「>13」（事實更正） |
| 繳交內容 | 主程式 `<學號>_hw2.py/.ipynb`、PDF 報告、學號 ZIP | **主要繳交：跟 DIC2 一樣 github and web；optional：對話內容、資訊圖表、報告書** | §7；既有產物全部保留 |
| AI 協助要求 | ChatGPT PDF、NotebookLM 摘要、報告標示 | 同（未改） | **需求歧義**：正文仍要求 GPT 對話 PDF 與 NotebookLM 摘要「放入報告」，繳交清單卻把對話內容與報告書列為 optional。不宣稱取消，照 V1 交付 [D Q2] |
| 評分標準 | 百分比明列 | 百分比移除；「不夠事後可再補 1 次」 | §14 時程；「可補一次」不當第二次正式繳交額度 [D Q6] |
| 加分 | 無 | **+1 有下拉視窗呈現兩種 problem；+2 可任意輸入 Dataset** | §3.1、§4、§5 |
| 補充段 | 有 | 無 | 新版未載明 |

## 3. 範圍

### 3.1 必要（老師要求）[T4]

- **加分 +1**：dashboard 有下拉視窗，可呈現兩種 problem。
- **加分 +2**：可任意輸入 Dataset（老師給的例子是一個 CSV 的 URL）。
- 特徵數條件改為 >13（King County 已符合）。
- 主要繳交：GitHub repository 與 web（§7）。

### 3.2 必要（acceptor 決定）

- 兩項加分**都在本次完成範圍**，不是有空才做（P1；§14）[D 補充]。
- 「兩種 problem」解讀為**同一頁面以下拉切換兩個資料集／問題**：King County 房價（正式分析）與 50 Startups 利潤（探索示範）[D Q3]。老師原文未進一步定義；若有機會向老師一句話確認，但不因此阻塞。
- 「任意輸入 Dataset」以**純瀏覽器端計算**實現：維持靜態頁與 GitHub Pages，不新增後端、API、Flask、Vercel [D Q4]。
- 探索能力集合：Forward SFS、Backward SFS、RFE、Lasso 路徑、All-in；逐筆 95% 預測區間的實際 vs 預測圖；即時預測器 [D Q10]。
- 老師範例資料 `50_Startups.csv` 複製一份進單元 `assets/`，標示來源與授權，使 +1 在 `file://` 離線與 ZIP 內都能用 [D Q12]。
- README、報告（新增探索模式章節）、ZIP 同步更新；Pages 與 ZIP 內的 dashboard 必須一致 [D Q16]。

### 3.3 選配

- 探索模式的係數表、全部結果表（與 V1 §3.3 同樣地位）。

### 3.4 不做 [D Q7、Q10、Q18、Q23、補充]

- 後端、API、資料庫、Vercel（V1 既有；本次再確認）。
- CSV 文字貼上輸入。
- 使用者指定分組欄的分組切分。
- 目標變數的 log 開關或自動 log 轉換。
- Exhaustive search、SelectKBest、permutation importance 作為探索模式的方法。
- 資料清理工具（補值、異常值處理、欄位轉換 UI）。
- 多目標、分類問題、時間序列。
- 儲存、分享或匯出探索結果；探索結果進入正式報告的數字。
- 任何改變 King County 正式分析數字、契約或已驗證產物的事。

### 3.5 覆寫 V1 的條款

| V1 條款 | V2 |
| --- | --- |
| §3.2「Dashboard：額外交付，不取代任何老師要求的檔案」 | Dashboard 與 repository 是**主要交付**；仍不取代任何正文要求的檔案 [T4][D Q24] |
| §7「頁面不發出任何對外網路請求」、§10「對外請求為零」（BR-04／OV-1） | 改為 §5.6 的隔離四條：頁面載入與 King County、50 Startups 的所有操作零對外請求；唯一允許的對外請求是使用者在自訂模式提交 URL 後對該 URL 的一次讀取 [D Q14] |
| §8「ZIP」列與 glossary **Submission package** | iLearning 繳交＝repository URL ＋ Pages URL ＋ 更新後的學號 ZIP [D Q24] |
| §3.1「10 至 20 個特徵」 | >13 [T4] |

其餘 V1 條款全部不變，特別是 BR-01／CC-1（Test evaluation 只對被授權模型、dashboard 操作不觸發新評估）、BR-03（學號不進追蹤檔案）、SR-04 的秩不足三類、SR-09 的反應性驗收。

## 4. Problem 與下拉 [D Q3、Q13]

- 下拉三項：**King County**（正式分析）／**50 Startups**（探索）／**自訂資料集**（探索）。
- 選 King County 時，頁面就是 V1 的 dashboard：既有區塊的內容與數字逐字相同，資料仍只來自 `model_data`。
- 選 50 Startups 或自訂資料集時，頁面呈現 Exploratory run 的區塊（§5），每個區塊標示「探索執行，非正式評估」；King County 的區塊沒有這個標示。
- 選自訂資料集時才出現 URL 與檔案輸入。
- 50 Startups 不宣稱符合正文的 >13 特徵條件；它是老師範例資料的示範 problem。

## 5. Exploratory run

### 5.1 資料輸入 [D Q7、Q9]

- 兩種輸入：**URL**（瀏覽器直接讀取）與**本機 CSV 檔案選擇**。URL 讀取失敗（含跨來源限制、404、逾時、非 CSV 回應）時，顯示明確原因並說明可下載後以檔案載入。
- 預測目標預設最後一欄，使用者可用下拉改。預設欄不是數值時，明確提示選擇有效的數值目標，不可靜默執行。

### 5.2 支援範圍與拒絕條件 [D Q8]

分兩層，Spec 必須各自定義明確的拒絕條件與訊息：

- **載入限制**（CSV 結構檢查，可看全部列）：UTF-8、逗號分隔、第一列為欄名的 CSV；其他格式拒絕。列數與欄數上限（候選值 50,000 列 × 60 欄，**只是候選**，以實測定；超過拒絕，不截斷）。全部可轉成數字的欄為數值欄；其餘為類別欄。含缺值的列整列刪除並顯示刪除筆數；刪完不足 20 列拒絕。目標必須是數值欄。
- **訓練列決定的模型決策**（切分後、只用訓練列；勘誤 E-1，SR-V2-01）：類別欄以訓練列計算的層級數 ≤ 20 才 one-hot，超過的欄自動排除並列出；在訓練列上為常數的欄排除並列出。上限 20、排除原因與列出方式不變，只是改在切分後以訓練列判定。
- **運算限制**（§5.4）：與載入限制分開，不承諾所有演算法都能在載入上限的規模完成。

### 5.3 前處理與語義（沿用正式分析）[D Q17、Q18、Q23]

- **Feature group**：一個來源欄＝一個 group；數值欄一欄，類別欄為其全部 one-hot 欄（基準層級＝訓練列中最先出現的層級；層級只從當次訓練列學；驗證列或 test 出現未見層級編為基準並計數）。四種方法整個 group 進出，k 數 group。
- RFE 的 group importance、tie 規則（canonical＝CSV 欄序）、Lasso 路徑（exact LARS，Ridge／Lasso 標準化）與正式分析相同。
- **沒有任何資料專屬的派生規則**（King County 的日期→天數、整修年→旗標等不適用）；一欄就是一欄。
- **目標不轉換**：一律以原始目標建模與報告；不自動取 log，沒有開關。
- **切分**：固定 seed 的逐列隨機 80/20；訓練列固定 seed 的 5-fold。沒有分組概念。UI 與報告揭露：重複列、同一實體多筆、時間相依資料可能造成洩漏，探索結果不代表正式研究結論。

### 5.4 評估協定 [D Q11]

- 只用訓練列做 5-fold CV：每個 (方法, k) 的 CV 指標；每個方法的 CV winner；整體 CV winner。
- 只有各方法的 CV winner 與整體 winner 計算 test 指標；test 指標不回饋任何選擇。
- 指標：MAE、MSE、RMSE、R²（目標單位）＋訓練 Adjusted R²。
- 實際 vs 預測圖與逐筆 95% PI：對 test 列、對被選出的 winner，用正式分析同一個 OLS 參數式 PI 公式。
- 即時預測器：對目前選取的 (方法, k) 在整個訓練集上擬合的 OLS；輸入為該模型用到的來源欄原始值。**只對 `VALID` 且已完成擬合的候選提供預測**；目前選取的候選是 `INVALID_MODEL`、`SKIPPED_RESOURCE_LIMIT` 或 `FAILED` 時，預測器停用並顯示該狀態與原因，不得給出任何預測值或區間。
- 同一份資料、同一設定、同一 seed → 相同結果（可重跑）。

### 5.5 運算限制與候選狀態 [D Q19、Q20]

- **逐方法運算預算**：以編碼後欄數與訓練列數定，數字由實測與演算法複雜度決定，寫進 Spec；目的是不阻塞 UI。
- 執行中有可觀察的進度。
- 每個 (方法, k) 候選有一個狀態：
  - `VALID`：可比較、可成為 winner；
  - `INVALID_MODEL`：不符合有效性條件（任一 fold 的訓練列或整個訓練集上設計矩陣秩不足、自由度不足等；原因必附）；
  - `SKIPPED_RESOURCE_LIMIT`：超出該方法的運算預算，未執行；
  - `FAILED`：非預期計算失敗（原因必附）。
- All-in 優先嘗試執行，但不保證任何資料都能成功；不預先承諾 LARS 或任何方法在特定時間內完成。
- **秩不足**：候選層級標 `INVALID_MODEL`；All-in 可以是 invalid；winner 只從 `VALID` 候選選；**全部候選無效才拒絕整個探索執行**。共線診斷呈現可驗證的線性相依關係，涉及的編碼欄映射回來源 Feature group，不得在原因不唯一時指認單一問題欄（§12 A-3）。
- **CV 資料量**：不採用「n_train < 10 × (p_enc + 1) 就拒絕」這類資料集層級門檻（會讓 50 Startups 無法執行）；有效性以候選層級的樣本數、自由度與秩條件定義（§12 A-1，已接受）。
- **處理順序**（勘誤 E-1，SR-V2-01；與 Spec V2 rev 2 的三層邊界一致）：(1) CSV 結構檢查與缺值刪列（載入層，可看全部列，不計算任何分布）→ (2) 固定 seed 的 80/20 切分 → (3) 只用整個訓練集決定類別層級數上限與常數欄排除，得到 Feature group 集合 → (4) 訓練列的固定 seed 5-fold → (5) 每個 fold 的類別層級、基準、one-hot 與標準化只從該 fold 的訓練列學；canonical 路徑與最終擬合只從整個訓練集學；test 列在所有選擇完成前不被讀取。這個順序由 Spec 固定，避免洩漏（A-1）。
- **退化後的 Lasso 候選**：§12 A-2。

### 5.6 隔離 [D Q5、Q14]

1. 頁面載入與 King County、50 Startups 兩個 problem 的所有操作：零對外請求（V1 的 OV-1 以原有強度繼續適用）。
2. 唯一允許的對外請求：使用者在自訂模式輸入 URL 並提交後，對該 URL 的一次讀取。
3. Exploratory run 不讀寫、不覆蓋正式分析的匯出結果；King County problem 的所有數字仍只來自 `model_data`（BR-01／CC-1 不變）。
4. 探索結果的每個區塊標示「探索執行，非正式評估」；探索結果每次重算、不保存、不進報告數字、不是 Test evaluation。

## 6. 老師範例 50 Startups [D Q12、Q22]

- CSV 複製進 `assets/`，README 資料來源一節標示來源 repo 與 MIT 授權。
- 以 Exploratory run 引擎執行，與自訂資料集走同一條路；必須能在符合支援條件的環境下**離線**完成分析。
- 驗收用的對照：以老師給的 URL 載入、以本機檔案載入、以內建項目載入，在**資料內容相同**（sha256 相同）時數字必須一致；資料內容不同時，不得只憑 URL 相同宣稱一致。

## 7. 交付物變更 [D Q16、Q24]

| 交付物 | V2 變更 |
| --- | --- |
| Submission package | iLearning：repository URL ＋ Pages URL（主要繳交）＋ 更新後的 `<學號>_hw2.zip`（涵蓋 optional 的報告書、對話內容）。 |
| Dashboard | 下拉與探索模式；50_Startups.csv 進 `assets/`；Pages 與 ZIP 一致。 |
| README | 功能說明、加分對應表（兩項加分 → 操作方式）、探索模式的限制與揭露、50 Startups 來源與授權、特徵數條件改 >13。 |
| 報告 | 新增「探索模式」章節：加分功能、分析方法、與正式分析的差異、限制；正式分析各章數字不變。建置流程不變。 |
| ACCEPTANCE.md | 既有條目保留；新功能另加獨立條目（§8）。 |
| ZIP | 重新打包；sha256 與清單照 V1 規則記錄。 |

學號規則（BR-03）不變。

## 8. 驗證與驗收（新增條目）[D Q15、Q21、Q22]

**可觀察條目**：

1. 下拉三項；選 King County 時既有區塊的內容與數字逐字相同（`model_data` 不變＋區塊比對）。
2. 50 Startups：`file://`、斷網下選取即執行完成，顯示五種方法的指標 vs k、各方法 CV winner、整體 winner 的 test 指標、實際 vs 預測＋95% PI 圖、即時預測器；**執行時間記錄，不預設門檻**。「50 Startups 在 A-1 下全部 k 有效」**由 fixture 的候選狀態證明**（Python 參照與 Node 結果都列出每個 (方法, k) 的狀態），不由 n=50、p_enc=5 推定。
2a. 即時預測器只在目前候選為 `VALID` 時可用；切到 `INVALID_MODEL`、`SKIPPED_RESOURCE_LIMIT` 或 `FAILED` 的候選時，預測器停用並顯示狀態與原因（§5.4）。
3. 自訂 URL：貼老師範例 URL，於 Pages 上載入成功；內容 sha256 與內建檔相同時，數字與內建 50 Startups 一致。
4. 自訂檔案：同一份 CSV 以檔案載入，數字一致。
5. 失敗情境各有明確訊息：非 CSV、無欄名、目標非數值、列數不足、超過載入上限、URL 讀取失敗（含跨來源）、全部候選無效；超出運算預算的方法標示 `SKIPPED_RESOURCE_LIMIT`。
6. 每個探索區塊有「探索執行，非正式評估」標示；King County 區塊沒有。
7. 網路：頁面載入與 King County／50 Startups 操作零對外請求；自訂 URL 模式只有一次對該 URL 的讀取。
8. Node 測試對 Python/sklearn 參照 fixture：OLS 係數、PI、指標、四種路徑、CV 切分、Feature group 編碼。
9. V1 的 OV-1（完全離線）與 SR-09（King County 的 1 秒反應性）因 UI 變動重做並記錄。

**數值驗證的定義**：

- 參照 fixture 由同一份 Python 套件產生（50 Startups ＋ 至少兩組 synthetic：一組非退化、一組刻意含完全共線與相等 entry）。
- 非退化資料：依固定前處理與數值容忍度比對（係數、PI、指標；Lasso 的 group entry alpha 相對誤差 ≤ 1e-6，entry alpha 相差超過容忍度的 group 順序必須相同）。
- Alpha 在容忍度內的 tie：依 canonical 規則。
- 完全共線或非唯一解：**不假設 sklearn 保證最小範數解或唯一進入順序**；退化 fixture 驗的是有效性狀態與原因（含退化前已求得路徑段的 entry alpha），不以未經證明的數值結果當 oracle（§12 A-2）。
- 共線診斷：fixture 以已知的線性相依關係（例如一欄是另兩欄之和）驗證報告的相依欄位組與其 Feature group 映射（§12 A-3）。
- Group entry alpha 的定義與正式分析一致。
- 效能只記錄實測，不設未經證明的門檻。
- 新增功能的數值與行為驗證都可重跑。

## 9. 只能由 acceptor 提供的輸入

本次沒有新增。可選：向老師確認「兩種 problem」的意思（§3.2）。iLearning 繳交與合併進 `main` 仍是 acceptor 的動作。

## 10. 已知風險與處理

| 風險 | 處理 |
| --- | --- |
| 「兩種 problem」解讀錯誤（例如老師指回歸／分類） | 有機會就一句話問老師；不阻塞。若錯誤，+1 重做，+2 與探索引擎不受影響 |
| 老師貼的 URL 不開跨來源（Kaggle 下載頁等） | 檔案載入是唯一出路；錯誤訊息把這條路寫清楚 |
| 瀏覽器端 Forward／Backward／RFE 在中型資料集過慢 | 逐方法預算與 `SKIPPED_RESOURCE_LIMIT`；哪些方法能完成由運算預算與候選有效性判定，沒有任何方法保證完成；進度顯示 |
| 探索模式的 UI 讓 test 曲線太顯眼，與報告第 8 章「不以 test 選模」的立場矛盾 | §5.4 只對 winner 顯示 test；Spec 守住 |
| 範圍膨脹成通用 ML 平台 | §3.4 不做清單；優先確保老師能操作下拉、輸入資料集、完成回歸分析並看到正確結果 |
| 加下拉動到頁面頂部，King County「逐字相同」的驗收 | 驗收用「既有區塊內容與數字逐字相同」，不用整頁截圖逐位元相同 |
| LARS 在使用者資料上退化 | §12 A-2 的狀態語義；數值只在非退化情境驗 |

## 11. 留給技術設計的事項（HOW）[A]

探索引擎的模組切分與是否使用 Web Worker；進度顯示的形式；運算預算的具體數值與量測方式；CSV 解析器；類別層級上限 20 與列數上限的最終數字；pivoted QR 或等價方法做秩與相依診斷；LARS 的數值實作細節；fixture 的 schema；下拉切換時 King County 區塊的掛載方式；探索模式的 URL 參數（若有）。

## 12. 提案 A-1～A-3（acceptor 2026-10-21 修改後接受）[D]

- **A-1 候選有效性（取代資料集層級 CV 門檻）**：某 (方法, k) 在每個 fold 的訓練列上與整個訓練集上，設計矩陣（含截距）滿秩且殘差自由度 ≥ 3，才是 `VALID`；否則 `INVALID_MODEL` 並附原因。資料集層級只保留 §5.2 的「刪缺值後 ≥ 20 列」。資料切分、缺值處理、類別編碼與 CV 的順序由 Spec 固定（§5.5「處理順序」），避免洩漏。「50 Startups 在此定義下全部 k 有效」必須由實際 fixture 的候選狀態證明（§8 第 2 條），不由 n=50、p_enc=5 推定。
- **A-2 LARS 退化語義**：Lasso 路徑在訓練列上遇到 active set 退化時，**保留已成功求得的路徑段**（這一段的 entry alpha 與順序是實際 LARS 結果，照常驗證）；退化後無法可靠求得的候選（k 超過該步）標 `INVALID_MODEL`，原因 `lasso_path_degenerate`。退化後未進入的 group 若為了顯示而以欄序排列，**只是展示順序，不得稱為實際 LARS 路徑，也不構成選模依據**。正式分析（V1）既有的 canonical 補齊規則（未進入的 group 依欄序排後、構成 k=1…18 的子集）是 King County 正式分析的選模語義，維持不變；探索模式不沿用該補齊作為選模語義。
- **A-3 共線診斷的證據形式**：報告可驗證的線性相依關係（哪些編碼欄構成一組相依，以及相依的形式），並把涉及的編碼欄映射回來源 Feature group；原因不唯一時不指認單一問題欄。用 pivoted QR 或等價方法由 Spec 決定。

## 13. Grill V2 決策紀錄（Round 1–3，2026-10-21）

| # | 題目 | 決定 |
| --- | --- | --- |
| Q1 | 新版來源地位 | 登錄 SRC-4，純文字副本、無 PDF、不等待；補充段「新版未載明」；不得自行補入新版沒有的內容 |
| Q2 | Grill 範圍 | 整頁重新 baseline；GitHub＋Web 升為主要交付；既有產物保留；GPT／NotebookLM 與 optional 清單的矛盾記為歧義 |
| Q3 | 兩種 problem | (a) 同頁下拉切換 King County（正式）與 50 Startups（探索） |
| Q4 | 架構 | (A) 純瀏覽器端；不新增後端、Flask、Vercel、API；技術限制在 Spec 定義 |
| Q5 | 詞彙 | 接受 **Exploratory run**；可切分、可算 test 指標；不覆寫正式結果、不進報告、不等同正式評估；Test evaluation 定義不變 |
| Q6 | 繳交策略 | (a) 一次交；內部目標 10-31；「可補一次」不當保證。加分計入期末總成績 → P0 必要交付、P1 兩項加分都在範圍 |
| Q7 | 輸入方式 | (b) URL ＋ 本機檔案；不做貼上 |
| Q8 | 支援範圍 | 有條件接受：基本邊界採用；50,000×60 只是候選；載入限制與運算限制分開；不承諾未量測的時間 |
| Q9 | 目標欄 | (b) 預設最後一欄、可改；不適合時明確提示 |
| Q10 | 方法與能力 | 原則 (a)：四種方法＋All-in、PI 圖、即時預測器；加運算邊界；不要求所有方法在所有資料上都能執行；類別群組語義在 Spec 明定 |
| Q11 | 評估協定 | (b) 固定 seed 80/20；只用 training 做 5-fold CV；winner 才算 test；test 不回饋選擇；資料不足時明確拒絕或說明 |
| Q12 | 50 Startups 存放 | (a) 複製進 assets，標示來源與授權，離線可用 |
| Q13 | 下拉項目 | (a) 三項：King County／50 Startups／自訂資料集 |
| Q14 | 隔離 | 接受四條；只有使用者主動提交 URL 才允許對該 URL 讀取 |
| Q15 | 驗證證據 | (a) sklearn fixture ＋ Node 比對，條件修正：Lasso 不要求跨實作順序完全一致，先固定定義再定容忍度；退化情境明確定義；OV-1、SR-09 重做 |
| Q16 | 報告／README／ZIP | (a) 三者同步；報告加探索模式章節；Pages 與 ZIP 一致 |
| Q17 | 類別群組語義 | 沿用 Feature group、RFE importance、canonical tie、train-only encoding；無 King County 派生規則 |
| Q18 | 目標尺度 | (a) 原始目標，不 log |
| Q19 | 運算限制 | 有條件 (b)：逐方法限制、進度顯示；狀態三分 `SKIPPED_RESOURCE_LIMIT`／`INVALID_MODEL`／`FAILED`；All-in 先試不保證 |
| Q20 | CV 不足與秩不足 | 寬鬆處理；**拒絕** n_train < 10×(p_enc+1) 門檻；有效性依 fold 樣本數、自由度、秩定義；All-in 可 invalid；全部無效才拒絕；共線診斷要有證據、不指認單一欄 |
| Q21 | Lasso 驗收 | 沿用 exact LARS；退化情境不假設 sklearn 的最小範數或唯一順序；entry alpha 定義與正式分析一致 |
| Q22 | 驗收清單 | 原則接受九條與指標集合；補充：50 Startups 離線必須完成、三路在內容相同時一致、King County 契約不變、效能只記錄、驗證可重跑 |
| Q23 | 切分語義 | 固定 seed 逐列切分；揭露洩漏風險；不做分組欄 |
| Q24 | 繳交內容 | (a) repo URL ＋ Pages URL ＋ 更新 ZIP；Dashboard 與 Submission package 重新定義 |

acceptor 的整體約束（原文要旨）：兩項加分直接影響期末總成績，都屬本次預定完成範圍；控制複雜度，不要為探索模式重建一套超出老師要求的通用機器學習平台；優先確保老師能實際操作下拉、輸入資料集、完成回歸分析並看到正確結果；不開始實作、不修改治理規則。

**第一次審閱（2026-10-21）的決定與套用處**：

| 決定 | 套用 |
| --- | --- |
| A-1 修改後接受：候選層級滿秩＋殘差自由度 ≥ 3；50 Startups 全部 k 有效須由 fixture 證明；切分、缺值、編碼、CV 的順序在 Spec 固定 | §12 A-1、§5.5「處理順序」、§8 第 2 條 |
| A-2 修改後接受：保留已求得的路徑段；退化後候選 `INVALID_MODEL`／`lasso_path_degenerate`；補齊順序不得稱為實際 LARS 路徑；與 V1 canonical 補齊規則區分展示與選模語義 | §12 A-2、§8 數值驗證 |
| A-3 原則接受：可驗證的相依關係、映射回 Feature group、不指認單一欄；方法留給 Spec | §12 A-3、§5.5、§8 數值驗證 |
| 刪除「Lasso＋All-in 幾乎一定完成」的保證 | §10 |
| 即時預測器只用 `VALID` 且已擬合的候選 | §5.4、§8 第 2a 條 |
| V1 不變；正式分析的數值、契約、驗證產物不變；CONTEXT.md 與本檔一致 | §3.5；CONTEXT.md 無需再改（§13 末） |

CONTEXT.md 一致性檢查：**Problem**、**Formal analysis**、**Exploratory run**、**Dashboard**、**Submission package**、**Assignment page** 的定義與本檔 rev 2 相符；候選狀態（`VALID` 等）是 Spec 層的實作語彙，不入 glossary。

**勘誤 E-1（2026-10-21，Spec Review SR-V2-01 的資料洩漏修正，不是新需求）**：acceptor 在 Spec V2 rev 1 審查指出，§5.2 把「類別層級 ≤ 20」與「常數欄排除」放在載入層（看全部列）會讓 test 列影響 Feature group 的集合。依 acceptor 2026-10-21 的授權做最小勘誤：§5.2 把這兩項移到「訓練列決定的模型決策」（切分後、只用訓練列）；§5.5 的處理順序改為與 Spec V2 rev 2 的三層邊界一致。上限 20、資料輸入能力、排除原因、列出方式與所有驗收目標都不變。

## 14. 優先順序與時程 [D Q6、補充]

- **P0 必要交付**：符合 SRC-4 基本要求；King County 正式分析完整且正確；GitHub 與 Pages 可正常存取；正式分析與驗證結果不受新功能影響。
- **P1 加分目標**：下拉切換兩種 problem；任意輸入 Dataset；使用者能完成可觀察、可驗證的 Exploratory run。
- 內部完成目標 2026-10-31；老師截止 2026-11-04。10-31 未完成時重新評估先提交符合必要要求的版本。
- P0／P1 只是本次工作的執行優先順序，不新增治理層級、審核 gate 或授權規則。

## 15. 下一步

1. acceptor 最終確認本 Brief V2 rev 2（或指出修改）。
2. 依 MATT 流程以 V1＋V2 產生 Spec（`/to-spec`，預期為 Spec rev 6 的增量），再拆 Tickets（`/to-tickets`）。這兩步與實作都尚未授權。
3. 單元內的實作仍屬 governance on 範圍；進入實作時依 `docs/governance/project-bindings.md` 處理，不在本檔預設任何治理安排。
