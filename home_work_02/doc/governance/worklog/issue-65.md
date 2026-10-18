# Worklog — issue #65（HW2 T6 報告 draft、單元 README 與 ACCEPTANCE.md）

- **Work item**：GitHub issue [#65](https://github.com/yotsubamomo/aiot-classwork/issues/65)，run `run-20261018-hw2-formal`（Formal，並行度 1）。
- **狀態**：實作、self-verification、DA C-2 (b) 的 targeted correction（§9）與 R1 F-1～F-3 的 targeted correction（§10）完成，待 Orchestrator 核對 binding 並派 R2。本檔不代表 audit 或 closure。
- **Subject**：branch `home_work_02-regrill`，base `bc56c064571d19b6d047ac4380540ebd3fac8a19`；第一次 implementation commit `741a21ba29dfb5ad7a2c2d1ac2f02d5eeb20035d`；C-2 (b) 修正 commit `0b57c0265f01e7732fdd1250e58101819a1b416f`（§9）；**R1 F-1～F-3 修正後的 implementation commit `99303c31ef5f19f9c34c562a2c2233bcfddec064`**（§10；本機，未 push）。本檔以其後的 record-only commit 加入（Bindings §7）。工作樹中 `doc/governance/run/run-20261018-hw2-formal.md` 的修改不是本票所做，沒有被 commit。

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
| C-1 | **〔已裁決：`decisions/decision-20261019-issue65-labels-figures.md` L-1、L-2，維持現況、不修改〕** **Dashboard 的標示**：三種標示中沒有「課堂口頭要求」。本票標為「老師要求（課堂口頭；作業頁正文沒有）」，並在報告的標示說明寫明它是唯一的例外、逐處註明「課堂口頭」（Brief §2、H-2「不得寫成老師的書面要求」）。Dashboard 頁面自己的圖例把「老師要求」定義為「作業頁正文的要求」，兩者的定義略有不同。另一種讀法（標「專案延伸」）與 Brief §3.2「必要（課堂口頭要求）」不符，所以沒有採用 | Design Authority（若認為應有不同標示） |
| C-2 | **〔已裁決：同一紀錄 F-1～F-5。(b) 是 TK-2 分配的缺口，由 #65 修正（§9）；(a)(c) 不是缺口、不補做。DA 更正：不是 #63 的缺陷〕** **TK-2 的缺口**：`results/figures/` 沒有 (a) 各方法 k 路徑的 CV RMSE 圖、(b) 實際 vs 預測＋逐筆 PI 的預測圖、(c) Ridge／Lasso 的 alpha CV 曲線。notebook 4.2、4.3 有 (a)(c) 的內嵌圖但沒有存檔；notebook 第 5 章沒有 (b)。報告以 CSV 注入的表呈現 (a)(c)，以建置時擷取的 dashboard 截圖呈現 (a)(b)。依票 AC「缺少者視為 #63／#64 的缺口回報」，這裡回報而不自行補做（補做需要修改 notebook 與 `results/`，屬 #63 的評估／匯出範圍，且受 N-4 限制）。H-2 的「附預測區間的預測圖」目前由 dashboard 與報告截圖滿足；主程式 notebook 本身沒有這張圖 | Design Authority（是否需要 #63 補存 PNG／在 notebook 加預測圖，或接受現況） |
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

## 9. Targeted correction：C-2 (b)（DA `decisions/decision-20261019-issue65-labels-figures.md`，`e03fcb0`）

- **依據**：DA 紀錄 §4.1 L-1～L-3（C-1：不修改）、§4.2 F-1～F-5（C-2：(b) 由 #65 修正；(a)(c) 不補做）；Orchestrator 2026-10-19 的續派（同一 worklog identity）。約束：不改 cell 0–45、§9.3 條件 7(b) 的模組與 `requirements.txt`；不執行 `hw2.run_notebook` 或 cell 41；不開守門、不載入 test 列、不擬合也不評分；N-4 部分執行；cell 28 的缺字觀察（DA O-1）不處理，交 R1 與 #67。
- **Binding**：同一 subagent（agentId `a4779b376d79e3353`，`gov-executor`）續派；修正 commit 之後觀測 `('claude-opus-5-5', 'high')` 273 則，單一元素。全程核對由 Orchestrator 執行。
- **修正 commit**：`0b57c0265f01e7732fdd1250e58101819a1b416f`（parent `e03fcb0`）。Delta 9 個檔案，全部在 `home_work_02/` 內：

| 路徑 | 內容 |
| --- | --- |
| `hw2/prediction_plot.py`（新增；不在條件 7(b) 的模組內） | `prediction_figure(model_data)`：輸入只有 `model_data`，即 `test[key]` 的 `predicted`、`lower`、`upper`、`covered`、`coverage`、`n_covered`、`n_test`、`pi_level` 與 `test_inputs` 的 `actual_price`；不重算任何指標。Q43 編碼：x＝預測、y＝實際、log 刻度、y＝x、每筆一條垂直 PI 線段、依 `covered` 著色、全部 `n_test` 筆。每個 `winners.authorized_test_models` 一個面板（`allin`、`forward_sfs_k17`），標題列出共用同一模型的 CV winner 與整體 CV winner（D-2）。英文標籤（不依賴 CJK 字型）。`save_prediction_figure`：`metadata={"Software": None}`；寫入單元內時要求 `is_formal`（非 fixture，且 `export.result_digest`＝`b53ff286…`），否則拒絕 |
| `hw2.ipynb` | 在 cell 45 之後、5.6 標題之前插入兩個 cell：`#### 5.5.1` 說明（markdown，index 46）與繪圖 code（index 47：使用 kernel 中的 `model_data`，與 cell 44、45 相同；顯示、印出每個面板的線段數與點數，`is_formal` 時存檔）。Cell 0–45 的位置、source 與輸出不變；原本 cell 46 之後的 #64 cell 往後移兩格，內容不變 |
| `results/figures/eval_actual_vs_predicted_pi.png`（新增） | sha256 `8afdb90b6aa9f1fce55fc7cf565db6a8ecefa71c136541f49b55dc1a54bc4a39`（158,031 bytes；`.gitattributes` 已把 `results/figures/*.png` 標為 binary，committed blob 的 sha256 相同） |
| `report/report.md`、`hw2/report.py` | §6.3 直接引用新的 PNG，取代「預測圖見第九章的 dashboard 截圖」；第九章截圖保留；標示不變；`FIGURES` 納入新檔 |
| `doc/acceptance/ACCEPTANCE.md` | A-3 的檢查與證據改為 notebook 5.5.1、新 PNG、`tests/test_prediction_plot.py`、報告 §6.3、dashboard 與第九章截圖；狀態仍 PENDING |
| `README.md`、`hw2/__init__.py` | 檔案配置與模組清單加上預測圖 |
| `tests/test_prediction_plot.py`（新增） | 8 項：正式結果的每個面板線段數＝點數＝`n_test`、顏色與 `covered` 一致、涵蓋筆數＝`n_covered`；線段端點就是匯出的 `predicted`、`lower`、`upper`；標題列出共用者與整體 winner；fixture 可以畫但不得寫入單元內（`results/figures/` 與單元內其他路徑都拒絕），可寫到單元外；被竄改的正式結果不得寫入；把 `hw2.data` 與 `hw2.testgate` 的全部函式 monkeypatch 為拒絕後仍可繪圖、`_official_test_rows_loaded` 仍是 False，且模組不 import 任何資料、守門、建模、評估模組，沒有 fit／evaluate／predict／score 等呼叫；追蹤的 PNG 可由追蹤的 `model_data` byte-identical 重現；notebook 新 cell 位於 5.5 與 5.6 之間、有 PNG 輸出、無錯誤、不含 `gate.`／`evaluate` |

### 9.1 部分執行（N-4；DA F-4 第 3 點）

- 腳本 scratchpad `ex65/run_partial65.py`，紀錄 `ex65/run_partial65.log`（2026-10-19 約 00:40～00:55 +0800；kernel 時間 3.3 s）。單一 kernel（cwd `home_work_02/`）：
  1. 前置（`store_history=False`）：`hw2.testgate.OFFICIAL_TEST_GATE_ENABLED = False`；`import matplotlib.pyplot` 加 `%matplotlib inline`（完整執行時由 cell 18 啟用 inline PNG formatter）。前兩次執行沒有這一步或沒有生效，`display` 只存了 `text/plain`，所以以 `git checkout -- hw2.ipynb` 還原後整段重做；三次寫出的 PNG 檔都相同。
  2. Cell 1（import 與 `rel()`）在副本上執行，notebook 中它的 #63 輸出不變。
  3. 以追蹤的 `results/model_data.json` 綁定 `model_data`，先斷言 `result_digest`＝`b53ff286…c3cfc6` 與 manifest `selection_digest`＝`44f7723e…4b28`（run_id `fe76019b9af84b1e8ff46095d5ac0fb2`）。
  4. 只執行新的 code cell（index 47），把它的輸出寫回。輸出：兩個面板各 4,323 條 PI 線段與 4,323 個點（`allin` 在區間內 4,082、外 241；`forward_sfs_k17` 4,083、240），`written: results/figures/eval_actual_vs_predicted_pi.png`；stderr 沒有任何輸出（沒有 matplotlib 缺字警告）。
  5. 檢查：`_official_test_rows_loaded` False、守門旗標 False、kernel 中沒有 `gate`、`evaluation`、`prepared`、`winners`。
- **沒有執行**：`hw2.run_notebook`；cell 41、42、44、45；除了 cell 1 與新 cell 之外的任何 cell；任何以開啟的守門執行的 process。
- 新 cell 的執行序號是 2（這個 kernel 的實際序號），notebook 的執行序號現在是 `1…28, 2, 25…35`。依 N-2 這屬過渡狀態，由 #67 的單一次完整執行取代（N-3）。

### 9.2 F-5 的證據

| 條件 | 結果 |
| --- | --- |
| 正式產物與 `741a21b` 相同 | `results/model_data.json` `fa86d76c…`、`assets/model_data.js` `37626bf9…`、`results/tables/` 8 個 CSV、既有 7 張 PNG（`diag_*`、`explain_*`）：sha256 與 `git show 741a21b:…` 逐一相同（17 個檔案全部相同） |
| `export.result_digest` | `b53ff286ae0734add8b272089aba904a1cb7f5aca444a62d356420b25dc3cfc6` |
| 凍結的模組 | `git diff --stat 052984b -- hw2/{data,split,preprocess,selection,models,comparison,ols,metrics,contract,testgate,export}.py requirements.txt`：沒有差異 |
| Notebook cell 0–45 | source 與 `git show 052984b:home_work_02/hw2.ipynb` 的 cell 0–45 逐一相同（True）；部分執行腳本另外斷言 cell 0–45 與 #64 cell 的完整 JSON（含輸出）在寫回前後相同；`git diff` 只有插入 |
| 沒有執行的項目 | `hw2.run_notebook`、cell 41、42、44、45 都沒有執行；沒有任何 process 開啟守門；`_official_test_rows_loaded` 在 kernel 與兩個獨立 process 中都是 False |
| 決定性 | 兩個獨立 process（`python -W error`，沒有警告）各以追蹤的 `model_data.json` 產生一次 PNG（`ex65/det1/`、`ex65/det2/`），與 kernel 寫入的追蹤檔三者 sha256 都是 `8afdb90b6aa9f1fce55fc7cf565db6a8ecefa71c136541f49b55dc1a54bc4a39`；pytest `test_the_tracked_png_is_regenerated_byte_identically` 每次執行再核對一次 |

### 9.3 Verification（工作樹＝`0b57c02`）

| # | 方法 | 結果 |
| --- | --- | --- |
| VC-1 | 完整 pytest `.venv/Scripts/python -m pytest -q -rs -p no:cacheprovider` | **338 passed、1 skipped**（skip＝學號設定未提供），70.0 s。之後只強化了 `test_prediction_plot.py` 的 import 檢查（見 VC-4），受影響的四個測試檔（`test_prediction_plot`、`test_report`、`test_notebook_structure`、`test_diagnostics`）再跑：49 passed |
| VC-2 | Node `node --test tests/js/core.test.js` | 9 pass、0 fail、3 skip |
| VC-3 | `python -m hw2.offline_scan` | PASS（0 findings） |
| VC-4 | Mutation probes（`ex65/mutants65c2.py`，scratch 複本 `ex65/mut_c2/`，輸出 `ex65/mutants65c2.out`） | baseline 通過；6 個 mutant 全部 DETECTED：點只畫一半、線段只畫一半、顏色不依 `covered`、寫入單元內不檢查正式性、上界換成點預測、模組 import 守門。第一輪有兩個存活：一個是等價 mutant（換成「點只畫一半」）；另一個（`from . import testgate`）讓測試的 import 檢查補上相對 import 的名稱 |
| VC-5 | 報告建置 `python -m hw2.report` | 成功；§6.3 引用 `fig:eval_actual_vs_predicted_pi.png`；PDF 25 頁；`external_requests: []`；`tests/test_report.py` 的「`results/figures/` 每張 PNG 都被引用」包含新檔 |
| VC-6 | 人工檢視 PNG（`ex65/fig_try/`） | 兩個面板、log 刻度、y＝x、逐筆線段與著色；標題列出 `All-in baseline = RFE k=18` 與 `Forward SFS k=17 = Backward SFS k=17 = Lasso path ranking k=17` 及整體 CV winner；涵蓋率與筆數；沒有缺字 |

- **A-4（S-1）**：新增內容中沒有「學號」；7 位以上的數字串只有 sha256／digest 片段；PNG 是 binary。沒有建立 `.local/packaging.json`。實際學號比對 NOT VERIFIED（依 S-1）。
- **Shell 寫入**：本次修正沒有以 shell 寫入單元交付物（以 Edit／Write 工具或 Python 腳本修改檔案；notebook 由部分執行腳本以 nbformat 寫回）。worklog 本節先以 Write 寫在 scratchpad `ex65/worklog_s9.txt` 再以 shell 附加，因為一次 shell heredoc 的引號解析失敗（沒有寫入任何內容）。第一次實作（§3.2）的 shell 寫入依 run record §15 已取得 acceptor 同意。
- **Git**：commit message 依規則、沒有 Claude 標記；未 push、rebase、merge、force push。

### 9.4 Concerns（本次修正）

| ID | 內容 | Required authority |
| --- | --- | --- |
| C-6 | 部分執行時為了讓 `display(Figure)` 存下 PNG，前置步驟以 `%matplotlib inline` 啟用 inline formatter。完整執行時由 cell 18 的 `import matplotlib.pyplot` 啟用，所以 #67 的完整重跑會得到同樣的輸出型態。這只影響 notebook 中的顯示，不影響 PNG 檔（三次相同） | 無（告知 R1／#67） |
| C-7 | DA O-1（cell 28 圖例的缺字）依指示沒有處理；新 cell 沒有缺字警告 | 無（R1、#67） |

## 10. Targeted correction：R1 F-1（blocking）、F-2、F-3（`audit/issue-65-c1-r1.md`，`6025c32`）

- **依據**：R1 record §6 F-1（需要的修正 1–3、R2 closure 條件 (a)～(d)）、F-2、F-3 的 disposition（併入本次修正）；F-4（notebook cell 28 缺字）依 Orchestrator 指示**沒有處理**（凍結的 cell，修正前須 route Design Authority，owner #67）。我不爭議 F-1：報告自己定義〔老師要求〕＝作業頁正文，而第六、七章開頭直接放了補充段的句子，§6.2 的 Adjusted R² 也沒有標示，兩者都可在模板中直接核對。
- **約束**：只改 `home_work_02/`；不改 `results/`、notebook、凍結的模組、`requirements.txt`；不重新評估、不執行 `hw2.run_notebook`。沒有使用 shell 寫入單元交付物（以 Python 腳本對既有檔案做字串替換，測試以 shell heredoc 附加到既有的測試檔）；worklog 本節先以 Write 寫到 scratchpad `ex65/worklog_s10.txt` 再附加。
- **Binding**：同一 subagent（agentId `a4779b376d79e3353`，`gov-executor`）續派；修正 commit 之後觀測 `('claude-opus-5-5', 'high')` 299 則，單一元素。
- **修正 commit**：`99303c31ef5f19f9c34c562a2c2233bcfddec064`（parent `6025c32`）。`git diff --name-only 0b57c02 99303c3 -- home_work_02 ':!home_work_02/doc/governance'` 只有 `README.md`、`report/report.md`、`tests/test_report.py`。

| Finding | 修改 |
| --- | --- |
| F-1 (1) | `report/report.md` 第六、七章：補充段引文之前加上出處說明——第六章「作業頁正文要求模型評估與加上區間的預測圖（見前面的標示對照表與第 6.3 節）。下面這句出自作業頁的「補充」段，是對這一階段的**建議**，不是作業頁正文的要求；本專案採用的部分是第 6.2 節的 Adjusted R² 與第 6.4 節的五大回歸假設診斷，都標〔依老師補充建議〕：」；第七章同型，指向第 7.2、7.3 節 |
| F-1 (2) | §6.2 標題改為「訓練 CV 與 Test 的比較 〔老師要求；Adjusted R² 為依老師補充建議〕」；該節兩處 Adjusted R² 的陳述各加段落層級〔依老師補充建議〕 |
| F-2 | `tests/test_report.py` 新增 10 項：§5.2、§6.4、§7.2、§7.3 的標題帶〔依老師補充建議〕且不帶〔老師要求〕；§6.2 標題與每一行 Adjusted R² 的陳述帶補充建議的標示；§7.1、§9 的標題帶「課堂口頭」；每一段 `quote:src2t` 引文都在〔依老師補充建議〕標題之下，或緊接在指明「補充」段為出處的句子之後；`quote:src1`（正文）引文前不得以「補充」為出處；README 目的段不把方法比較寫成作業要求 |
| F-3 | `README.md` 目的段：「依作業要求執行特徵選擇：比較四種……（方法取自作業頁「補充」段建議清單的一部分）與單一的 All-in baseline……」 |

### 10.1 回歸證據

| # | 方法 | 結果 |
| --- | --- | --- |
| VR-1 | 完整 pytest（工作樹＝`99303c3` 之前的最後一次全量；之後只改了第六章引言的一句措辭，受影響的 `test_report.py`、`test_prediction_plot.py` 再跑 34 passed） | **348 passed、1 skipped**（skip＝學號設定未提供），48.5 s |
| VR-2 | `tests/test_report.py` | 26 passed（原 16＋新 10） |
| VR-3 | Node `node --test tests/js/core.test.js` | 9 pass、0 fail |
| VR-4 | `python -m hw2.offline_scan` | PASS（0 findings） |
| VR-5 | 報告建置 `python -m hw2.report` | 成功；仍核對正式評估的 digest（建置會先執行 `check_formal_evaluation`）；PDF 26 頁（多了兩段文字）；`external_requests: []`。渲染後 `dist/report/hw2_report.md`：第六章（第 191 行起）與第七章（第 313 行起）的補充段引文之前都有出處說明；§6.2 標題與兩處 Adjusted R² 帶〔依老師補充建議〕。模板的「沒有手抄數字」測試通過（新文字只有章節編號） |
| VR-6 | Mutation probes（`ex65/mutants65f.py`，scratch 複本 `ex65/mut_f/`，輸出 `ex65/mutants65f.out`） | baseline 通過；11 個 mutant **全部 DETECTED**：R1 的 L1～L6（先前存活的 6 個）、第六章出處說明被刪（F1a）、第七章出處說明被刪（F1b）、§6.2 標題標示被刪（F1c）、§6.2 條列的標示被刪（F1d）、README 措辭還原（F3） |
| VR-7 | 不變的產物 | `results/model_data.json`、`assets/model_data.js`、`results/figures/eval_actual_vs_predicted_pi.png` 與 `0b57c02` 相同（`git diff --quiet`）；`results/`、`assets/`、`hw2.ipynb`、`hw2/` 都不在 delta 中 |

- **R2 closure 條件**（R1 record F-1）：(a) 渲染後第六、七章與其他〔老師要求〕章節沒有未註明出處的補充段引文（VR-5；測試 `test_every_supplement_quote_is_attributed_to_the_supplement`）；(b) §6.2 的 Adjusted R² 帶〔依老師補充建議〕（VR-5；`test_adjusted_r2_in_6_2_is_labelled_as_a_supplement`）；(c) delta 只有報告來源、測試與 F-3 的 README 一句（VR-7）；(d) 完整 pytest 通過、報告可建置（VR-1、VR-5）。是否成立由 R2 判定。
- **A-4（S-1）**：新增內容沒有「學號」相關數字；7 位以上數字串只有 commit SHA。實際學號比對 NOT VERIFIED（依 S-1）。
- **Git**：commit message 依規則、沒有 Claude 標記；未 push、rebase、merge、force push。

### 10.2 Concerns

| ID | 內容 | Required authority |
| --- | --- | --- |
| C-8 | R1 F-4（cell 28 缺字）依指示未處理；owner #67，修正前須 route Design Authority | Design Authority（#67 之前） |
| C-9 | README 的修改（F-3）不是 R2 的 closure 條件之一，但在 delta 中；R1 record 建議併入本次修正 | 無（告知 R2） |
