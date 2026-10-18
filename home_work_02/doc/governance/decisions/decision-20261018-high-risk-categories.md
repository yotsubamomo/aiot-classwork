# Decision record — 高風險類別與 assurance 要求（`home_work_02/`，現行 Outcome Contract）

- **紀錄類型**：Design Authority decision record（治理 §5.1「DA MUST 決定高風險分類及 assurance 要求」；Bindings b5 §5、§8.2 #4）
- **日期**：2026-10-18
- **適用範圍**：`home_work_02/` 在現行 Outcome Contract（Brief @ `dff7c55c`）下的全部 work items：Spec rev 3 的 Formal Tickets、Spec Integration Audit，以及結案後的 Lightweight 單點修正
- **取代**：r4 下的 `decision-20261014-high-risk-categories.md` 不沿用（處置紀錄 N-3），只作為格式參考
- **Binding**：`gov-design-authority`，`claude-opus-5-5`／`high`（Bindings §3.1 預設 mapping，沒有 escalation，沒有替代）。由派工者依 Bindings §3.6 核對。

高風險類別的效果：(a) 該類別的 blocking finding，Final Adjudicator 不得單獨 defer，必須有 DA 確認（治理 §4.5）；(b) Lightweight 工作觸及該類別時會觸發 audit（Bindings §5）；(c) 第 3 節的核對義務。這些類別不作為 capability escalation trigger（Bindings §3.2、§5）。

## 1. 裁決：採用 H-1～H-4

### H-1 憑證、機密與不得公開的資料

| 項目 | 內容 |
| --- | --- |
| 風險 | (a) 使用憑證或讓憑證外洩：Kaggle token（`~/.kaggle/kaggle.json`、`KAGGLE_USERNAME`／`KAGGLE_KEY`）被 CLI 自動讀取，或寫進檔案或 log。本作業只用匿名公開端點下載資料，不使用任何金鑰；dashboard 是純靜態前端，沒有任何 API key（RB-3）。(b) acceptor 材料（ChatGPT 對話 PDF、NotebookLM 原始輸出與來源清單）或含有這些材料的產物（附 ChatGPT 頁面的報告 PDF、ZIP）進入 git（Brief §9「不進 git」）。(c) **實際學號**出現在任何追蹤檔案、commit message、PR、Issue、log 或 dashboard 中（BR-03） |
| 為何是高風險 | `main` 是 GitHub Pages 的發布來源。內容一旦 push 或合併就會公開，移除需要改寫已 push 的歷史（RB-6），Agent 無法自行補救。學號放在本類而不是 H-4，因為它的風險機制是不可逆的公開，與 (a)(b) 相同；H-4 只交叉引用 |
| 涵蓋位置 | `git ls-files`、staged／committed diff、topic branch、PR、Issue、worklog、audit、run、acceptance 紀錄、notebook 輸出、`model_data`、dashboard 靜態檔、終端輸出 |
| 觸及的工作 | 取得資料；修改單元 `.gitignore`；acceptor 材料的接收、存放與轉換；學號設定與打包；建置報告 PDF 與 ZIP；任何 commit、push 或 PR |

### H-2 老師指定的名稱與格式，以及課堂口頭要求的交付

| 項目 | 內容 |
| --- | --- |
| 風險 | 評分直接依賴的名稱、標示或結構被改動或遺漏 |
| 涵蓋 | `<學號>_hw2.ipynb`（repo 內是 `hw2.ipynb`，打包時由同一個檔案產生）與 `<學號>_hw2.zip`；PDF 報告，內容包含 CRISP-DM、GPT 對話、NotebookLM 摘要與主流解法比較；兩個標示字串「GPT 輔助內容」與「NotebookLM 摘要」；摘要 ≥100 字（計數依 `derivation-SPEC.md` B-15）；notebook 與報告都有 CRISP-DM 六個階段的名稱與順序；資料集名稱與 Kaggle 連結；附預測區間的預測圖；README 的流程與成果；**dashboard**（Classroom Verbal Requirement：`home_work_02/index.html`、Pages URL、在 ZIP 內可以完全離線以 `file://` 使用；不得寫成老師的書面要求） |
| 觸及的工作 | notebook 或報告的章節與標示、預測圖、打包腳本、README、dashboard 的路徑、資源載入方式與離線行為 |

### H-3 評估完整性

| 項目 | 內容 |
| --- | --- |
| 風險 | 這類錯誤不會讓程式失敗，只會讓數字看起來更好：以 `id` 分組的隔離（train／test、CV fold）被破壞；需要 fit 的前處理看到驗證列或 test；fold-internal selection 被改成在整個 training set 上只選一次；用 test 選模或換模型；在授權集合以外評估 test（含 dashboard 操作引發的評估）；PI、coverage 或 Adjusted R² 的計算或秩錯誤；Python 與 JS 不一致；秩不足的語義被改成刪欄、縮小範圍或默默跳過；報告或 README 的數字不是來自匯出結果；選擇偏誤與 PI 假設的陳述超出 Spec 允許的範圍 |
| 涵蓋 | Spec rev 3 的「分割與交叉驗證」「特徵選擇與模型」「指標與推論」「預測區間」「`model_data` 契約」的不變量、dashboard 的分層規則與來源標示（BR-01）、測試與它們的期望值；CC-1 的六項約束（Ridge／Lasso 各一次 metric_only 的 test 評估；2026-10-18 更新，原文為「在 acceptor 決定前不得評分」；見 `derivation-SPEC.md` 第 11 節） |
| 觸及的工作 | 分割、前處理、特徵選擇、建模、PI、test 評估、匯出、dashboard 的計算與 test 區塊、對應的測試、notebook 的建模與評估流程、報告的方法與結果章節 |

### H-4 證據真實性與如實標示

| 項目 | 內容 |
| --- | --- |
| 風險 | Agent 產生、改寫或補造 ChatGPT 對話或 NotebookLM 內容；摘要加入原始材料沒有的論點或來源；把 Claude Code 的產出寫成 ChatGPT 的產出；主流解法比較沒有附來源；三種標示（老師要求／依老師補充建議／專案延伸）混淆，或把 dashboard 寫成老師的書面要求；**wireframe 的 mock data 被當成結果**（`mock-data.js`／`wireframe.js` 的數值或截圖進入報告、README 或 dashboard）；沒有證據的驗證被標為 PASS（OV-1～OV-6、SR-09 的量測值） |
| 為何是高風險 | 屬學術誠信，無法以重跑修正；自動化測試只能檢查標示存在，無法檢查內容是否忠實 |
| 涵蓋 | 報告的「GPT 輔助內容」「NotebookLM 摘要」、主流解法比較、三種標示的對照表、dashboard 截圖、ACCEPTANCE.md 的狀態與量測紀錄；學號規則交叉引用 H-1 |
| 觸及的工作 | 撰寫或修改上述報告章節、處理 acceptor 材料、建置報告、更新 ACCEPTANCE.md、加入截圖 |

### 不採用為獨立類別

- 部署可用性：沒有後端；合併屬 RB-1，由 acceptor 決定。
- 視覺品質與 OV-2～OV-5：屬一般審查判斷；是否作為 gate 待 acceptor 決定（`derivation-SPEC.md` F-5）。

## 2. 對 Tickets 的要求

每張票都要標示它觸及的類別（依各類別的「觸及的工作」），並引用本紀錄。

## 3. Assurance 要求

| # | 要求 | 適用範圍 |
| --- | --- | --- |
| A-1 | 票觸及任一類別時，R1 audit record 要有一節寫明觸及的類別、核對內容與結果；R2 重述修正結果。不新增 audit round | 全部 Tickets |
| A-2 | H-3：Reviewer 要**自己執行**分組隔離測試、選擇邊界測試，以及 PI／coverage 的獨立重算（pytest 與 Node），並自己比對匯出結果與報告、README 的數字 | 觸及 H-3 的票；Spec Integration Audit |
| A-3 | H-3／BR-01：核對 `model_data` 中 `methods`／`baselines` 沒有 test 欄位、`test` 的鍵集合等於授權清單，並確認 dashboard 的 UI 程式不以 `test_inputs` 評估任何模型（`derivation-SPEC.md` B-3） | dashboard 與匯出相關的票；Spec Integration Audit |
| A-4 | H-1：每張票結案前與 Spec Integration Audit 時，對受審 subject 核對：追蹤檔案不含 acceptor 材料目錄、打包設定與輸出、`.pdf`（老師文件除外）、`.zip`、`kaggle.json`、Kaggle 金鑰的設定；以 `git grep` 確認沒有實際學號（從本機未追蹤的學號設定讀取比對值，不在終端、log 或紀錄中印出；紀錄只寫「已核對、無命中」）。可行時以自動化測試實作，Reviewer 仍要自行判斷 | 全部 Tickets；合併前 |
| A-5 | H-4：審查摘要時，Reviewer 直接讀 acceptor 的原始材料自行比對，不只依 Executor 的對照表；核對 ChatGPT PDF 的 sha256 與 worklog 記錄的 acceptor 提供版本相同；核對報告、README 與 dashboard 中沒有 mock 數值或 wireframe 截圖 | 報告與證據相關的票；Spec Integration Audit |
| A-6 | H-2／OV-1：Spec Integration Audit 要親自或依完整紀錄核對 ZIP 的檔名、內容與 sha256，以及解壓後在斷網、`file://` 下的檢查與零對外請求的靜態掃描 | Spec Integration Audit |
| A-7 | Deferral：H-1～H-4 的 blocking finding 由 Final Adjudicator defer 時，必須有 DA 確認並記入 disposition | 全部 |
| A-8 | Model diversity：維持 Bindings §5，不宣告 diversity 關係；不以類別作為 escalation trigger | 全部 |

## 4. 哪些 Lightweight work items 會觸發 independent audit（Bindings §5）

觸發條件：acceptor 要求、DA 裁決要求，或觸及下列任一項。本單元沒有 SA-3 opt-in，所以「依 SA-3 自主合併」不適用。

| 觸發（必須 audit） | 不觸發（worklog 如實寫「完成且依 policy 未要求 independent audit」） |
| --- | --- |
| 修改分割、前處理、選擇、建模、PI、test 評估、匯出或其測試（H-3） | 修改不含評分標示、數字或方法陳述的文件文字（例如 README 的錯字、單元內的導覽說明） |
| 修改 dashboard 的計算、資料載入、test 區塊、來源標示或提示文字，或新增任何資源引用（H-2、H-3） | 只調整 dashboard 的顏色、間距或字級，而且不新增任何 URL 或資源；self-verification 仍要重跑「零對外請求」的靜態掃描 |
| 修改報告的 AI 章節、標示、主流解法比較、數字或截圖（H-2、H-4） | 修改 governance 紀錄（record-only paths） |
| 修改 `.gitignore`、打包腳本、學號設定的讀取或 ZIP 內容（H-1、H-2） | — |
| 處理任何 acceptor 材料（H-1、H-4） | — |
| Root `README.md` 或 `CONTEXT-MAP.md` 的修改：屬 RB-5，要 acceptor 逐次授權；只有內容觸及上列項目時才 audit | — |

無法判定時視為觸發。這一點由 DA 判定，Executor 不得自行降級。

## 5. 是否改變 accepted 語義

否。本紀錄只決定 assurance 分類與核對義務，內容取自已接受的 Brief（§3、§7、§9、§10、§11 BR-03）、Bindings RB-3／RB-5／RB-6 與 wireframe 的接受紀錄。沒有新增 requirement、audit round 或 acceptor gate。
