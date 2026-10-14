# Decision record — 高風險類別與 assurance 要求（`home_work_02/`）

- **紀錄類型**：Design Authority decision record（治理 §5.1「Design Authority MUST 決定專案適用的高風險分類及 assurance 要求」；Bindings b5 §5、§8.2 #4；Outcome Contract §6、§8 #5）
- **日期**：2026-10-14
- **適用範圍**：`home_work_02/` 的全部 work items：Formal 主體（Spec v1.0 與其 Tickets），以及結案後的 Lightweight 單點修正。
- **相關契約**：Outcome Contract（第 1–8 節於 `e2153254`，接受紀錄第 9 節於 `370c0ae`）；[`../../spec/SPEC.md`](../../spec/SPEC.md) v1.0；lane 裁決 [`decision-20261014-lane.md`](decision-20261014-lane.md)。
- **執行角色**：`gov-design-authority`。Binding 由派工者依 Bindings §3.6 核對；本紀錄不自證 binding。

## 1. 問題

Bindings b5 §5 的初始候選是 H-1（憑證與機密）與 H-2（老師指定的介面或資料格式），要求每份作業在第一次正式 audit 或 Formal activation 前，由 DA 確認或修改。OC §6 列出四個起草候選：H-2 名稱與格式、評估完整性、證據真實性、H-1 憑證（預期不適用）。這些候選只是輸入，需要 DA 決定：採用哪些類別、各涵蓋什麼、各要求什麼 assurance。

高風險類別在本治理中的效果是：(a) 治理 §4.5：該類 blocking finding 的 deferral 須另有 DA 確認，Final Adjudicator 不得單獨 defer；(b) Bindings §5：變更涉及該類時，Lightweight audit 被觸發；(c) 本紀錄第 3 節的 audit 核對義務。Bindings §5 明定高風險類別不作為 capability escalation trigger，本紀錄也不改變這一點。

## 2. 裁決

採用四個類別。編號只在本單元內有效，與 `home_work_01/` 的 H-3 無關。

### 2.1 H-1 憑證與 acceptor 控制的材料 — **修改**（候選 H-1 的範圍改寫）

| 項目 | 內容 |
| --- | --- |
| 風險 | (a) 憑證（例如 Kaggle API token、`~/.kaggle/kaggle.json`）被使用或進入任何可公開的位置；OC §2.5 規定本作業不使用任何憑證。(b) acceptor 控制的原始材料（ChatGPT 對話 PDF、NotebookLM 輸出與來源清單），或內含它們的建置產物（附有 ChatGPT 頁面的報告 PDF、ZIP），在 acceptor 決定公開前，進入 git 追蹤檔案、已 push 的 branch、PR 或 log。OC §2.5.1 末段規定「是否放進公開的 Git repository 由 acceptor 決定」。 |
| 為何是高風險 | 一旦 push 到公開 repository，移除需要改寫已 push 的歷史（RB-6），Agent 無法自行回復，而且 PR 的 diff 審查可能看不出二進位 PDF 的內容。原本候選 H-1 的「API key」部分在本作業不適用：資料已隨附並固定（Spec R-DATA-1），執行期不連網；但「不使用憑證」仍是 OC constraint，取得資料時有可能誤用 Kaggle CLI 自動讀取的 token，所以保留於本類。 |
| 涵蓋位置 | git 追蹤檔案（`git ls-files`）；staged／committed diff；pushed topic branch；PR 描述與 comment；Issue；worklog、audit、acceptance 紀錄；終端與 notebook 輸出。 |
| 不涵蓋 | 學號。OC 只把學號列為 acceptor 輸入（§3.3），沒有規定保密；ZIP 檔名與 OC-A8 要求的檔案清單紀錄必然含學號。Spec 讓 tracked 的 notebook 不含學號（R-REPO-1），原因是學號在實作開始時還沒有提供，不是保密要求。 |
| 觸及的工作 | 取得資料集；建立或修改單元 `.gitignore`；接收、存放、轉換 acceptor 材料；建置報告 PDF 與 ZIP；commit、push、開 PR、合併。 |
| 對應 Spec | R-DATA-2、R-AI-5、R-REPO-2、R-REPO-3、R-PKG-3；AC-25（provenance）、AC-28、AC-31；INV-8 |

### 2.2 H-2 老師指定的名稱與格式 — **確認**，內容列舉

| 項目 | 內容 |
| --- | --- |
| 風險 | 評分直接依賴的名稱、標示或結構被改動或遺漏，評分項目因而找不到對應產物。 |
| 涵蓋項目 | `<學號>_hw2.ipynb`、`<學號>_hw2.zip`（學號為 acceptor 提供的實際值，無佔位）；報告為 PDF；「GPT 輔助內容」與「NotebookLM 摘要」兩個標示字串；摘要 ≥ 100 字；CRISP-DM 六個階段名稱與順序（notebook 與報告）；資料集名稱與 Kaggle 連結；預測圖附預測區間；ZIP 內含 ChatGPT 對話 PDF；README 的 GitHub 連結。 |
| 觸及的工作 | 任何改動 notebook 章節、報告章節或標示、預測圖、打包腳本、README 的變更。 |
| 對應 Spec | R-DATA-4、R-NB-1、R-RPT-1、R-RPT-4、R-AI-1、R-AI-2、R-PKG-1、R-PKG-2、R-REPO-4；AC-01、AC-03、AC-04、AC-05、AC-15、AC-22、AC-23、AC-26、AC-27；INV-6 |

### 2.3 H-3 評估完整性 — **新增**（起草候選「評估完整性」）

| 項目 | 內容 |
| --- | --- |
| 風險 | 分區或 CV 的隔離被默默破壞（洩漏），Test 或 Calibration 在凍結前影響選擇，各候選的比較條件不一致，conformal 的計算錯誤，或報告的數字與重跑不一致，而測試仍然全綠。這類錯誤不會使程式失敗，只會讓數字看起來更好。另一類風險是報告對 conformal 保證或 outer-CV 分數的陳述超出 OC §2.4 允許的範圍。 |
| 為何是高風險 | OC §3.4 把資料洩漏、以 Test 或 Calibration 選模、計算與獨立重算不一致、陳述保證時漏寫 exchangeability 假設，都列為一律 FAIL。這些錯誤難以由後續步驟發現（治理 §2.5 選型原則 1 的同一理由），而且是本作業「結果」配分的核心。 |
| 涵蓋項目 | 分區與 folds；有參數的前處理、特徵選擇、hyperparameter 搜尋的 fit 範圍；candidate procedure 的定義與共用條件；選模規則與 tie-break；凍結與 Test 評估的順序；conformal quantile、coverage、寬度的計算；結果 artifact 與報告數值的單一來源；報告的偏誤陳述與三層 conformal 陳述；測試期望值。 |
| 觸及的工作 | 任何改動 `mlr/` 的 data、selection、modeling、evaluation、conformal 模組、相關測試或其期望值、notebook 的建模與評估流程、結果 artifact 格式、報告的方法與結果章節的變更。 |
| 對應 Spec | R-PART-\*、R-PREP-\*、R-CAND-\*、R-SEL-\*、R-CONF-\*、R-EVAL-\*、R-RPT-2、R-RPT-3、R-REPRO-\*；AC-06～AC-18、AC-20；INV-1～INV-5、INV-9 |

### 2.4 H-4 證據真實性與標示 — **新增**（起草候選「證據真實性」）

| 項目 | 內容 |
| --- | --- |
| 風險 | Agent 產生、改寫或補造 ChatGPT 對話或 NotebookLM 內容；摘要加入原始材料沒有的論點或來源；以 Claude 或無關的對話替代 ChatGPT PDF；把 Claude 的產出寫成 ChatGPT 的產出；把 Agent 自己的網路研究冒充 NotebookLM 結果；M8 比較寫出無來源的主張；把 ENHANCED 寫成老師要求。 |
| 為何是高風險 | OC §3.4 把捏造或替代證據、把 ENHANCED 寫成老師要求列為一律 FAIL；這是學術誠信問題，事後無法以重跑修正，而且自動化測試只能檢查標示是否存在，無法檢查內容是否忠實。 |
| 涵蓋項目 | 報告的「GPT 輔助內容」節、「NotebookLM 摘要」節、主流或更優解法比較節、scope class 標示；ChatGPT PDF 的納入與 provenance；摘要與原始材料的對照表。 |
| 觸及的工作 | 任何撰寫或修改上述報告章節、處理 acceptor 材料、建置附有 ChatGPT 頁面的報告 PDF 的變更。 |
| 對應 Spec | R-AI-1～R-AI-5、R-RPT-5；AC-22～AC-25、AC-29；INV-7 |

### 2.5 不採用為獨立類別的候選與事項

- **候選 H-1 原文「API key 是否進入瀏覽器端程式」**：本作業沒有瀏覽器端程式，也沒有 API key。剩下的憑證風險併入新的 H-1（2.1 節）。
- **部署可用性**：本作業沒有部署的應用程式。合併後的 GitHub Pages 與 Vercel 驗證由 Bindings §5 SA-3 合併後驗證處理，不需要另列高風險類別。
- **視覺品質（「結果美觀」）**：屬 Reviewer 的一般判斷，失敗可觀察，不列。

## 3. Assurance 要求

| # | 要求 | 適用 | 依據 |
| --- | --- | --- | --- |
| A-1 | **Ticket audit record 的類別節**：Ticket 觸及 H-1～H-4 任一類別時，R1 audit record MUST 有一節寫明觸及的類別、核對的內容與結果；R2 對該節的修正結果重述。不新增 audit round。 | 全部 Formal Tickets | 治理 §4.6；orch-default §7「不新增 round」 |
| A-2 | **H-3 的獨立重算**：觸及 H-3 的 Ticket 與 Spec Integration Audit，Reviewer MUST 自行執行（不只閱讀 Executor 的輸出）leakage 測試與 conformal 獨立重算測試（Spec AC-06～AC-09、AC-16），並自行比對結果 artifact 與報告、README 的數值（AC-20）。 | Formal | 治理 §2.3 第 3 項 autonomous access |
| A-3 | **H-4 的原始材料對照**：審查 AC-23、AC-25 時，Reviewer MUST 直接讀 `acceptor_materials/` 內的原始材料，自行比對摘要與材料，不得只依 Executor 的對照表；並核對 ChatGPT PDF 的 sha256 與 worklog 記錄的 acceptor 提供版本相同。 | Formal | 治理 §2.3；OC §2.5.1 |
| A-4 | **H-1 的追蹤檔案檢查**：每個 Ticket 結案前與 Spec Integration Audit 時，對受審 subject 檢查：`git ls-files home_work_02` 不含 `acceptor_materials/`、`dist/` 下的任何檔案、不含任何 `.pdf`、`.zip`；追蹤檔案與 diff 不含 `kaggle.json` 檔案、`KAGGLE_KEY`／`KAGGLE_USERNAME` 的指派，或 Kaggle token 格式（`"key"` 後接 32 位十六進位字串）。這項檢查以 `tests/` 內的自動化測試實作（Spec R-TEST-5），Reviewer 仍自行判斷。若 acceptor 決定公開某項材料（R-REPO-3），本檢查依該決定的紀錄調整，不由 Agent 自行放寬。 | Formal；合併前 | 治理 §5.4「已可由 tooling 檢查者 SHOULD 使用」；Bindings §5 release gate |
| A-5 | **Spec Integration Audit 的必核項**：逐項核對 INV-1～INV-9；從乾淨環境實際重跑一次 notebook 與全部測試（或核對 Executor 的重跑紀錄，並自行重跑 conformal 與 leakage 測試）；對最終 ZIP 檢查檔案清單、檔名、sha256 與佔位（AC-26）。 | Spec v1.0 | 治理 §4.7 |
| A-6 | **Deferral**：H-1～H-4 的 blocking finding，Final Adjudicator 不得單獨 defer，須另有 DA 確認並記入 disposition。 | 全部 | 治理 §4.5（重申，不是新增） |
| A-7 | **Lightweight audit 觸發**：結案後的 Lightweight 單點修正（Bindings §4 第 4 列），若觸及 2.1～2.4 列的「觸及的工作」，MUST 執行 independent audit；worklog 不得標「依 policy 未要求」。依 SA-3 自主合併的 Lightweight 工作則一律觸發（Bindings §5）。 | 結案後 | Bindings §5 觸發條件 |
| A-8 | **Release gate 的附加證據**：合併進 `main` 之前，無論依 SA-3 還是 OC §9 的一次性 RB-1 授權合併，gate 證據（run record）MUST 另外引用 A-4 檢查在 PR head SHA 上的結果。 | Release | Bindings §5；OC §4.2、§9 |
| A-9 | **Model diversity**：維持 Bindings §5，不宣告任何 diversity 關係；本單元沒有要求恢復 diversity 才能 audit 的類別；不以高風險類別作為 escalation trigger。 | 全部 | Bindings §3.2、§5 |

## 4. 是否改變 accepted 語義

**否。** 本裁決只決定 assurance 分類與核對義務，不改變 OC 的 intent、scope、constraints 或 acceptance semantics，也不新增 audit round 或 acceptor gate。H-1 的改寫、H-3 與 H-4 的新增，都是治理 §5.1 授予 DA 的決定（Bindings §5「確認或修改」）；其內容全部取自 OC 已接受的條款（§2.4、§2.5、§2.5.1、§3.4）。A-4 的追蹤檔案檢查落實 OC §2.5.1 末段與 Bindings §5 release gate，不是新的 requirement。

## 5. 受影響 work items

- **Tickets**（尚未 derive）：derive 時每張票 MUST 標示觸及的類別（依 2.1～2.4 的「觸及的工作」），並在票內引用本紀錄。
- **Reviewer 的 audit record**：依 A-1 增加類別節，並依 A-2～A-5 執行核對。
- **Orchestrator run record**：依 A-6 在 disposition 時核對 DA 確認存在（只核對存在）；依 A-8 在合併前記錄 A-4 檢查結果的引用。
- **Bindings**：不需修改；§5 的候選列表在本單元由本紀錄取代為有效分類。
- **Outcome Contract**：不修改；§8 #5 的「高風險類別」部分由本紀錄完成。

## 6. Evidence

- Bindings b5 §3.2、§4、§5、§8.2；治理 v2.2 §2.3、§4.5、§4.6、§4.7、§5.1、§5.4。
- OC（`e2153254`）§2.4、§2.5、§2.5.1、§3.1 OC-A1～OC-A8、§3.4、§6；§9（`370c0ae`）。
- Brief v0.3 §10（資料集可匿名取得、CC0-1.0）；root `.gitignore`（只忽略 `.env`、`receipts/`、`__pycache__/` 等，不忽略 PDF、ZIP）。
