# Worklog — issue #65（HW2 T6 報告 draft、單元 README 與 ACCEPTANCE.md）

- **Work item**：GitHub issue [#65](https://github.com/yotsubamomo/aiot-classwork/issues/65)，run `run-20261018-hw2-formal`（Formal，並行度 1）。
- **狀態**：實作與 self-verification 完成，待 Orchestrator 核對 binding 並派 R1。本檔不代表 audit 或 closure。
- **Subject**：branch `home_work_02-regrill`，base `bc56c064571d19b6d047ac4380540ebd3fac8a19`；**implementation commit `741a21ba29dfb5ad7a2c2d1ac2f02d5eeb20035d`**（本機，未 push）。本檔以其後的 record-only commit 加入（Bindings §7）。工作樹中 `doc/governance/run/run-20261018-hw2-formal.md` 的修改不是本票所做，沒有被 commit。

## 1. Contract reference

| 項目 | 內容 |
| --- | --- |
| Ticket | #65（OPEN，`ready-for-agent`；高風險 H-2、H-4）；索引 `doc/ticket/tickets.md` |
| Spec | `doc/spec/SPEC.md` rev 5（#59）：「報告與打包」的報告條款、「人工檢查表（ACCEPTANCE.md）」、OV-1～OV-6 的 gate 分類、「分割與交叉驗證」的選擇偏誤陳述、「預測區間」（SR-08／SR-12）、「資料、計數與前處理」（exp(ŷ_log) 為條件中位數） |
| DA derivation | `decisions/derivation-SPEC.md` §4 T-義務、§5 OV、§7 F-4、§9.1（#65 的分配）、§9.3、§9.4 I-2、§9.5 TK-2、TK-3、§11 G-4 |
| 其他 DA 紀錄 | `decision-20261018-high-risk-categories.md`（H-2、H-4；A-1、A-5、A-7、A-8）；`decision-20261018-issue60-a4-student-id.md`（S-1～S-6、§2.2）；`decision-20261018-issue62-shared-subset-test-key.md`（D-2、D-3）；`decision-20261018-issue63-js-tolerance.md`（T-1）；`decision-20261018-issue64-notebook-rerun.md`（N-4、N-5、I-4）；`decision-20261018-issue64-standardized-reading.md`（R-1.1、R-1.3、R-1.5） |
| 前票 concerns（指向 #65） | `worklog/issue-63.md` C-2、C-3；`worklog/issue-64.md` C-3、C-4（處理見 §3.4） |
| Outcome Contract | `doc/governance/outcome-contract.md`：Brief @ `dff7c55c`＋CC-1、AD-1、AD-3 |
| 授權與派工約束 | `run/run-20261018-hw2-formal.md` §1（Implementation；SA-1 本機 commit；不 push、rebase、merge、force push）；Orchestrator 2026-10-18 派工約束：只改 `home_work_02/`（不含 `doc/requirement/`）；不得重新執行正式 Test 評估、不得全量重跑 notebook（N-4）；報告數字只取自追蹤的匯出結果，不得用 mock 或 wireframe 截圖（A-5）；acceptor 材料屬 #66，只留標示的位置；不寫入實際學號、acceptor 材料、金鑰；不建立 `.local/packaging.json` |
| Bindings | b5；HOW `impl-default` v2（overrides none） |

## 2. Executing role and binding

- **角色**：Executor（`gov-executor` subagent，由 Orchestrator 派工）。
- **Binding 觀測**（Bindings §3.6 的同一邏輯，掃描本 subagent 的 transcript `subagents/agent-a4779b376d79e3353.jsonl`，`meta.json` 的 `agentType`＝`gov-executor`）：implementation commit 之前觀測 `('claude-opus-5-5', 'high')` 204 則，單一元素，等於 O-1 mapping。全程核對由 Orchestrator 在採用 return 前執行。
- **Escalation／替代**：無。**Bounded assignments**：未使用。

## 3. Work performed

### 3.1 產物（commit `741a21b`，8 個檔案，全部在 `home_work_02/` 內，沒有 `doc/requirement/`）

| 路徑 | 內容 |
| --- | --- |
| `report/report.md`（新增） | 報告 draft（zh-TW Markdown）。章節：標示說明與三種標示對照表；1 資料來源與研究脈絡（資料集、連結、授權、sha256；19／18 與計數規則；兩條特徵數原文逐字引用與交集；研究脈絡；Kaggle 名次不適用、以預測結果評估取代）；2～7 CRISP-DM 六章（特徵選擇比較、Ridge／Lasso、p-value 對照、計算時間、評估協定、訓練 CV 與 Test 分欄比較、區間驗證、五大假設診斷、Deployment 的預測新樣本與模型解釋、使用限制）；8 主流或更優解法比較；9 dashboard 連結與截圖；10 GPT 輔助內容、11 NotebookLM 摘要、附錄 A ChatGPT PDF（三處【待填】，沒有範例或代擬文字）；附錄 B 重現資訊。模板中沒有任何結果數字，全部是佔位符 |
| `hw2/report.py`（新增） | 建置程式 `python -m hw2.report`：從 `results/model_data.json` 與 `results/tables/*.csv` 注入數字與表；分析圖只引用 `results/figures/`；老師原文由 `doc/requirement/` 的轉寫逐字取用（特徵數的交集也由原文解析計算）；建置前核對 `export.result_digest` 與 selection digest 等於 #63 唯一一次正式評估的值，不符就拒絕；以 claim check 核對模板的定性陳述（alpha 在網格下緣且 CV 單調、Test RMSE 高於 CV、permutation 第一名是 zipcode、五項診斷都偏離、沒有 invalid 候選、沒有缺值）；Markdown → HTML（自帶的小型轉換器，不新增套件、不改 `requirements.txt`）→ PDF；`--no-pdf`、`--final`（仍有【待填】時失敗） |
| `report/chrome_capture.js`（新增） | 建置時以 headless Chrome／Edge（DevTools protocol，所有主機名稱無法解析、記錄任何非 file 請求）開啟真正的 `index.html` 擷取 5 張截圖（overview、整體 winner 方法的 model 區、比較全部、Test 區、方法與限制），並把報告 HTML 列印成 PDF |
| `report/external_sources.json`（新增） | 主流或更優解法：4 個公開 King County 解法（Bronner GitHub notebook；Mao & Yao 2020 Atlantis Press；Chen 2024 SCITEPRESS；Hartono et al. 2024 ASSET）。每一項有連結、資料、目標尺度、切分、方法、來源自報的指標與它在來源中的位置、不可比之處。數字都是我開啟來源逐一讀到的值（§3.3） |
| `doc/acceptance/ACCEPTANCE.md`（新增） | 狀態規則（PASS 需證據；best-effort 沒有證據一律 NOT TESTED；PENDING）；A 老師要求（Brief §3.1 全部 T- 項目，含 notebook 六章與 README 內容的 T-義務、Kaggle 名次）；B 課堂口頭要求與補充建議；C 已接受的決定與 DA 義務（G-1～G-4、TK-2、TK-3、D-2／D-3、T-1、N-3／N-5、R-1.x、B-3、S-x）；D Spec 人工檢查表（dashboard、報告、repo、乾淨環境）；E OV-1～OV-6 的 gate／best-effort 分類與 OV-6 量測紀錄表（#67 填寫）；Pages 檢查記 NOT TESTED（pending merge）（AD-3） |
| `README.md` | 改寫：目的、資料來源與授權、流程（CRISP-DM 六章）、成果（數字由 pytest 核對與匯出一致）、dashboard 連結、重跑步驟（新增報告建置步驟）、學號設定路徑 `.local/packaging.json`、本機不進 git 的材料、檔案配置。依 DA N-5 改寫 Test 評估的說明：唯一一次是 #63（run `fe76019b…`、`result_digest` `b53ff286…`，權威紀錄 `worklog/issue-63.md` §5），`meta.test_evaluation` 只記錄產生目前檔案的那次執行，完整重跑是重現；`run_notebook` 一行改為「重現唯一一次的 Test 評估」 |
| `tests/test_report.py`（新增） | 16 項：模板沒有手抄數字；每個佔位符可解析、`results/figures/` 的每張 PNG 都被引用；【待填】標示與 `--final` 失敗；關鍵數字等於匯出值；老師原文逐字；六章順序與章節標示、必要陳述（條件中位數、樂觀偏誤、不宣稱保證、Kaggle 名次不適用、二項近似的獨立假設、非因果、課堂口頭）、標示對照表；沒有 Ridge／Lasso 係數；建置拒絕非正式評估的結果與不再成立的定性陳述；外部來源欄位完整；Markdown 轉換；README 的項目、N-5 措辭、成果段數字；ACCEPTANCE 的覆蓋、OV 分類、沒有未驗證的 PASS |
| `hw2/__init__.py` | 模組清單加 `report` |

### 3.2 重要決定（HOW）

- **數字單一來源**的實作：模板只放佔位符；`tests/test_report.py` 掃描模板的散文（去掉佔位符、code、連結目標），除了章節編號、notebook 節號、來源編號 `[n]`、`GVIF^(1/(2·df))`、`√10` 與讀法中的「1」之外不得有數字。外部來源的數字放在 `external_sources.json`，標明是來源自報的值。README 不能在建置時注入，所以以 pytest 核對「成果」段每個數字等於匯出值，且該段不得有其他數字。
- **正式評估的核對**：報告建置綁定 #63 的 `result_digest` 與 selection digest（N-1、N-5、§9.3 條件 2）。讀取匯出結果不是 Test 評估：不擬合、不評分、不載入正式 test 列。
- **三種標示的依據**是 Brief §3.1／§3.2 與 Spec「報告與打包」（DA I-2），沒有引用 OC v2 草稿。補充建議（Adjusted R²、五大假設、Deployment 的預測新樣本與模型解釋、Ridge／Lasso）標「依老師補充建議」；協定、log 目標、涵蓋率驗證、p-value 對照、permutation importance、時間量測標「專案延伸」；dashboard 標「老師要求（課堂口頭；作業頁正文沒有）」（見 C-1）。
- **D-2／D-3**：比較表每個 winner 一列、以自己的身分呈現並列出共用者；評估數量由匯出結果計算（2 個 OLS＋2 個 metric-only）。
- **R-1.5**：係數表只引自 `final_model_coefficients.csv`（含 `train_sd`、`pct_per_train_sd`）；標準化的讀法依 R-1.1；沒有 Ridge／Lasso 係數（測試檢查）。
- **Dashboard 截圖**在建置時擷取（不追蹤 PNG），讀取同一份匯出結果；不使用 wireframe 或 mock。
- **PDF 工具**：Node＋Chrome／Edge（`Page.printToPDF`），不新增 Python 套件；`requirements.txt` 與 DA N-4 條件 7(b) 列出的選擇／評估模組都沒有改動。
- **過程說明**：本 subagent 的 Write 工具拒絕直接寫入名為 `report/report.md` 的檔案（工具對「報告檔」的限制），所以 `report.md`、`README.md`、`ACCEPTANCE.md` 先寫在 scratchpad（`ex65/report_template.txt`、`readme.txt`、`acceptance.txt`）再以 shell 複製到單元內。內容是本票的交付物，不是給派工者的摘要。

### 3.3 主流解法來源的核對（H-4）

每個來源都由我開啟並讀取原文；連結以 `curl -L` 確認 HTTP 200（2026-10-19）。

| 來源 | 讀取方式 | 核對的數字 |
| --- | --- | --- |
| [1] Bronner notebook（GitHub commit `3e3a260`） | `raw.githubusercontent.com` 下載 `.ipynb`，逐 cell 讀程式與輸出（scratchpad `ex65/src/bronner.ipynb`） | 2.1 OLS CV R² 0.699 ± 0.017；Ridge／Lasso 0.699；RF 0.721 ± 0.020；二次多項式＋標準化 0.815 ± 0.019；`train_test_split(test_size=0.2, random_state=0)`；`X = df.drop('price')`（含 `id`） |
| [2] Mao & Yao 2020 | Atlantis Press PDF（WebFetch 存檔後以 Read 讀取全文） | Table 2 四列 training／test／CV R²；ln(price)；7:3 |
| [3] Chen 2024 | SCITEPRESS 全文（WebFetch，要求逐字引用） | R² 0.613、Adj R² 0.613、D-W 1.983；沒有切分；DOI 10.5220/0013055900004601 |
| [4] Hartono et al. 2024 | 期刊 PDF（WebFetch 存檔後以 Read 讀取全文，20 頁） | Table 13（CatBoost 80:20 Test RMSE 126836.87、MAE 66156.36、R² 0.894）、Table 15、Table 17；正文沒有線性回歸 baseline 的數字 |

未採用：Kaggle notebook（頁面需 JS，Kaggle API 需要金鑰，H-1 不使用）、Scribd 文件（來源不可核對）、Puget Systems、mlr3 gallery（沒有可比的回歸指標）。

### 3.4 前票 concerns 的處理

| Concern | 處理 |
| --- | --- |
| #63 C-2（alpha 在網格下緣） | 報告 §5.2：表列網格、選出的 alpha、位置；陳述「正則化在此資料上沒有改善 CV」並以 claim check 核對（CV RMSE 隨 alpha 單調不減、`alpha_at_grid_edge` 為 lower、不低於 All-in） |
| #63 C-3（Test RMSE 高於 CV） | 報告 §6.2：差距與它相對於各折標準差的倍數由匯出值計算；說明 CV winner 的樂觀偏誤與 Test 是獨立估計（TK-3）、USD RMSE 受高價房屋主導；依協定不換模型 |
| #64 C-3（報告的解釋段落標示，I-4） | 報告 §7.3 標「依老師補充建議」，permutation importance 標「專案延伸」 |
| #64 C-4（五項診斷都偏離，連到涵蓋率） | 報告 §6.3、§6.4：五項逐一揭露並連到區間的假設；不宣稱保證 95%，不以診斷修正區間 |

## 4. Verification

環境：Windows 11、Python 3.11.2（單元 `.venv`）、Node v24.19.0、Chrome 155.0.8059.80。腳本與輸出在 session scratchpad `ex65/`。

| # | 方法 | 結果 |
| --- | --- | --- |
| V-1 | 完整 pytest `.venv/Scripts/python -m pytest -q -rs -p no:cacheprovider`（工作樹＝`741a21b`） | **330 passed、1 skipped**（skip＝學號設定未提供），49.7 s（baseline 314＋本票 16） |
| V-2 | `tests/test_report.py` | 16 passed，1.0 s |
| V-3 | Node `node --test tests/js/core.test.js` | 9 pass、0 fail、3 skip（fixture 項目由 pytest 執行） |
| V-4 | `python -m hw2.offline_scan` | `scanned 6 files: PASS (0 findings)` |
| V-5 | 報告建置 `python -m hw2.report`（預設輸出 `dist/report/`，被 `.gitignore` 排除） | 成功，11.4 s：`hw2_report.md`、`.html`、`.pdf`（25 頁，約 2.5 MB）；5 張 dashboard 截圖；`external_requests: []`；首次繪製 299 ms；pending＝gpt、notebooklm、chatgpt_pdf。`--final` 依設計失敗（V-2）。另以 `--out` 在 scratchpad 建置兩次（`ex65/build1`、`build2`）並以截圖逐頁檢視 HTML（`ex65/prev/`） |
| V-6 | 正式產物不變 | `results/model_data.json` sha256 `fa86d76c…b891e3`、`assets/model_data.js` `37626bf9…5b29a72`（與 #63／#64 相同）；`export.result_digest`＝`b53ff286ae0734add8b272089aba904a1cb7f5aca444a62d356420b25dc3cfc6` |
| V-7 | Mutation probes（`ex65/mutants65.py`，單元的 scratch 複本，只跑 `tests/test_report.py`） | baseline 通過；12 個 mutant **全部 DETECTED**：模板手抄數字、README 數字改變、README 多一個數字、ACCEPTANCE 未驗證就標 PASS、OV-3 的 best effort 被移除、少引用一張圖、標示對調、條件中位數陳述被刪、釘住的 digest 被改、README 的 N-5 措辭還原、Kaggle 名次說明被刪、【待填】的說明被改 |
| V-8 | 人工核對 | 渲染後的報告全文逐章閱讀（`ex65/build1/hw2_report.md`）；截圖 `test.png`、`compare.png` 確認是正式 dashboard（n_test 4,323、整體 winner 的身分與共用標示）；README 的重跑步驟：新增的報告建置、pytest、Node、離線掃描都實際執行過（V-1～V-5）；`run_notebook` 一行只改措辭，**依 N-4 沒有執行**（完整重跑屬 #67） |

- **A-4（S-1）**：沒有建立 `.local/packaging.json`；追蹤樹沒有新增 PDF、ZIP、`.env`、`kaggle`、`acceptor_materials/`、`dist/`（`dist/report/` 被忽略）。新增內容中「學號」只以 `<學號>` 或敘述用詞出現；7 位以上的數字串全部歸類為非學號：sha256／commit SHA／digest 的片段、日期 `20261018`、DOI `10.5220/0013055900004601` 的片段、期刊頁碼 `02403014`、Atlantis 文章編號 `125948987`；沒有使用老師範例中的學號樣式。Commit message 沒有長數字。過程中沒有印出任何疑似值。**實際學號比對 NOT VERIFIED**（學號設定尚未提供；依 S-1）。
- **H-2**：notebook、`index.html`、`assets/` 沒有改動；兩個標示字串「GPT 輔助內容」「NotebookLM 摘要」逐字是報告的章節標題；報告六章名稱與順序由測試核對。
- **Git**：commit message 依 `docs/conventions/git-commit-rules.md`，沒有 Claude 標記；未 push、rebase、merge、force push。

## 5. Audit status

Required（Formal；H-2：報告章節與老師要求的標示、README、預測圖；H-4：三種標示、主流解法來源、沒有 mock 或 wireframe、待填位置不冒充內容、ACCEPTANCE 的狀態）。依 A-1 需要 R1 record 的類別核對節；依 A-5 Reviewer 自行開啟來源比對 `external_sources.json`、核對報告與 README 沒有 mock 數值或 wireframe 截圖；依 A-2 自行比對報告、README 的數字與匯出結果。尚未派工（由 Orchestrator 依 Bindings §3.7）。本檔的 self-verification 不是 audit。

## 6. Concerns 與所需 authority

| ID | 內容 | Required authority |
| --- | --- | --- |
| C-1 | **Dashboard 的標示**：三種標示中沒有「課堂口頭要求」。本票標為「老師要求（課堂口頭；作業頁正文沒有）」，並在報告的標示說明寫明它是唯一的例外、逐處註明「課堂口頭」（Brief §2、H-2「不得寫成老師的書面要求」）。Dashboard 頁面自己的圖例把「老師要求」定義為「作業頁正文的要求」，兩者的定義略有不同。另一種讀法（標「專案延伸」）與 Brief §3.2「必要（課堂口頭要求）」不符，所以沒有採用 | Design Authority（若認為應有不同標示） |
| C-2 | **TK-2 的缺口**：`results/figures/` 沒有 (a) 各方法 k 路徑的 CV RMSE 圖、(b) 實際 vs 預測＋逐筆 PI 的預測圖、(c) Ridge／Lasso 的 alpha CV 曲線。notebook 4.2、4.3 有 (a)(c) 的內嵌圖但沒有存檔；notebook 第 5 章沒有 (b)。報告以 CSV 注入的表呈現 (a)(c)，以建置時擷取的 dashboard 截圖呈現 (a)(b)。依票 AC「缺少者視為 #63／#64 的缺口回報」，這裡回報而不自行補做（補做需要修改 notebook 與 `results/`，屬 #63 的評估／匯出範圍，且受 N-4 限制）。H-2 的「附預測區間的預測圖」目前由 dashboard 與報告截圖滿足；主程式 notebook 本身沒有這張圖 | Design Authority（是否需要 #63 補存 PNG／在 notebook 加預測圖，或接受現況） |
| C-3 | GitHub Pages URL 目前回應 404（尚未合併進 `main`）。報告與 README 列出 Brief 固定的網址；ACCEPTANCE D-12 記 NOT TESTED（pending merge）（AD-3） | 無（合併後的 Lightweight work item） |
| C-4 | 觀察（不在本票範圍、沒有修改）：dashboard「指標 vs k」圖在 1280 px 的截圖中，x 軸沒有顯示 k 的刻度數字（`ex65/build2/shots/compare.png`）。#67 的 dashboard 人工檢查（D-1、D-4）可一併確認 | 無（告知 #67／Reviewer） |
| C-5 | 報告 PDF 的建置需要 Node.js 與 Chrome 或 Edge（README 已寫明，可用 `HW2_BROWSER` 指定）；報告 PDF 與截圖只在 `dist/report/`，不進 git | 無 |

## 7. Remaining work

- #65 R1（Orchestrator 派工）。學號比對 S-2～S-5；push 依 run record 選項 (a)。
- #66：報告 §10、§11、附錄 A 的 acceptor 材料；之後 `python -m hw2.report --final` 必須成功。
- #67：ACCEPTANCE.md 逐項執行與填寫（含 OV-1～OV-6、量測紀錄表）；乾淨環境完整重跑（N-3、§9.3 條件 7、8）後重新建置報告；打包時把 `dist/report/hw2_report.pdf` 放入 ZIP。
- C-2 依 DA 決定處理。
- **Scratchpad 產物**（不在 repo）：`ex65/`——`src/`（`bronner.ipynb`、`bronner.txt`、`hartono.pdf`、`hartono.html`）、`report_template.txt`、`readme.txt`、`acceptance.txt`、`build1/`、`build2/`、`preview.js`、`prev/`、`mutants65.py`、`mut_unit/`。

## 8. 執行時間量測

- 工作時間：2026-10-18 約 23:40 至 2026-10-19 00:35 +0800。
- 報告建置（含 5 張截圖與 PDF）約 11.4 s；只產生 Markdown／HTML 約 1 s。完整 pytest 49.7 s。Mutation probes 12 個約 1 分鐘。來源查證（4 個採用、5 個未採用）是本票最耗時的部分。
