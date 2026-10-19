# HW2 驗收清單（ACCEPTANCE.md）

每一條老師要求、已接受的決定與 Spec 檢查 → 可觀察的檢查 → 證據位置。本清單由 #65 建立；逐項執行與填寫狀態屬 #67（打包、離線驗收、乾淨環境重跑與整合），AI 證據章節屬 #66。

- **依據**：Brief（`doc/brief/BRIEF.md` @ `dff7c55c`）＋CC-1、AD-1～AD-3（`doc/governance/outcome-contract.md`）；Spec rev 5（`doc/spec/SPEC.md`，#59）的 Testing Decisions 與人工檢查表；DA `doc/governance/decisions/derivation-SPEC.md`（§4 T-義務、§5 OV、§9、§11 G-1～G-4）與同目錄的 decision records。
- **三種標示**：〔老師要求〕作業頁正文；〔依老師補充建議〕作業頁「補充」段，本專案採用（Brief §3.2）；〔專案延伸〕本專案的設計。Dashboard 是課堂口頭要求，不是作業頁的書面要求。

## 狀態的規則

| 狀態 | 意義 |
| --- | --- |
| PASS | 已在「核對的 subject」欄所列的 commit 上執行檢查，結果符合，證據位置可開啟。**沒有證據不得標 PASS。** |
| FAIL | 已執行，結果不符；附證據與後續處理。 |
| NOT TESTED | 沒有執行環境，或依已接受的決定延後（寫明原因，例如 pending merge）。**Best-effort 項目沒有證據時一律記 NOT TESTED，不得標 PASS。** |
| PENDING | 尚未執行；「執行」欄是負責的票。 |

- 先前票的 audit 與測試是**既有證據**，不等於本清單的 PASS：它們核對的是當時的 subject。#67 在最終 subject 上重新執行後，才填 PASS／FAIL，並記錄「核對的 subject」。
- 量測值（OV-6／SR-09）只記實測，不得沿用 fixture 或 wireframe 的數字。

核對的 subject（#67 填寫）：branch `home_work_02-regrill` @ `e2f391ae396b2595e53a481c76fc8a7b0c45c142`（單元的最後一個實作 commit；ZIP 由它打包）。Root 的兩列在之後的 `611ad07`（RB-5）。乾淨環境：`git clone` 這個 branch、`py -3.11 -m venv`、`pip install -r requirements.txt`；完整重跑在 `1f3a8b6` 執行一次（之後只改 `hw2/package.py`、測試與 `assets/app.js`，都不在選擇與評估路徑上），證據見 `doc/governance/worklog/issue-67.md`。

## A. 老師要求（Brief §3.1）

| ID | 要求（來源） | 可觀察的檢查 | 證據位置 | 執行 | 狀態 |
| --- | --- | --- | --- | --- | --- |
| A-1 | T-資料：Kaggle 公開資料集，10–20 個特徵；標示來源與連結〔老師要求〕 | 報告第一章與 notebook 第 1 章有資料集名稱、Kaggle 連結、授權；報告陳述 source features 19 與 feature groups 18 及計數規則；報告逐字引用正文「10 至 20 個特徵」與補充段「features > 13, < 40」兩條原文並說明採用交集 | 報告 §1.1、§1.2（`report/report.md`；引文由建置程式自 `doc/requirement/` 逐字取用）；`tests/test_report.py`；`tests/test_preprocess.py::test_feature_counts_and_canonical_order`；`results/model_data.json` `meta.dataset` | #67 | PASS（#67 worklog §6、§9；final 報告 §1.1、§1.2） |
| A-2 | T-模型：線性回歸預測；必做特徵選擇與模型評估〔老師要求〕 | 四種方法 k = 1…18 的訓練 CV、各方法與整體 CV winner、Test 評估都在 notebook 第 4、5 章與報告第五、六章 | `results/tables/cv_by_method_k.csv`、`comparison.csv`；`tests/test_selection.py`、`test_models.py`、`test_methods_contract.py`；報告 §5、§6 | #67 | PASS（乾淨環境 pytest 395 passed、Node 9 passed，#67 worklog §6） |
| A-3 | T-預測圖：預測圖加上信賴區間或預測區間〔老師要求〕 | 主程式 notebook 5.5.1 從匯出的逐筆結果畫出實際 vs 預測＋全部 Test 樣本的逐筆 95% PI（Q43 編碼，不抽樣、不聚合），存成 `results/figures/eval_actual_vs_predicted_pi.png`，報告 §6.3 直接引用；dashboard 的實際 vs 預測圖同樣畫出全部 Test 樣本與逐筆 PI；PI 與 Python 匯出逐筆一致 | notebook 5.5.1；`results/figures/eval_actual_vs_predicted_pi.png`；`tests/test_prediction_plot.py`；報告 §6.3；`index.html` Test 區塊與報告 §9 的截圖；`tests/test_model_data_official.py::test_independent_recomputation_of_every_official_test_row`、`tests/js/core.test.js`（相對容差 1e-6，DA `decision-20261018-issue63-js-tolerance.md` T-1） | #67 | PASS（#67 worklog §6；notebook 5.5.1 與 PNG 由單一次執行重新產生且逐位元相同，§5；dashboard 見 OV-1） |
| A-4 | T-CRISP-DM：**notebook** 六章〔老師要求〕（DA T-義務） | `hw2.ipynb` 的 `## 1.`～`## 6.` 依序是 Business Understanding、Data Understanding、Data Preparation、Modeling、Evaluation、Deployment，每章有說明與程式；已執行且無錯誤 | `tests/test_notebook_structure.py`（`test_six_crisp_dm_chapters_in_order`、`test_first_three_chapters_have_content_and_code` 等）；人工開啟 notebook 確認各章內容 | #67 | PASS（`test_notebook_structure.py`；單一次完整執行，執行序號 1…40、無錯誤；cell 28 圖例 5 個 ASCII 標籤可讀，#67 worklog §4、§5） |
| A-5 | T-CRISP-DM：**報告**六章〔老師要求〕 | 報告第二～七章依序是六個階段的名稱 | 報告 §2～§7；`tests/test_report.py` | #67 | PASS（乾淨環境 pytest 395 passed、Node 9 passed，#67 worklog §6） |
| A-6 | T-AI：ChatGPT 對話 PDF；NotebookLM 摘要 ≥100 字；報告明確標示「GPT 輔助內容」「NotebookLM 摘要」〔老師要求〕 | 兩個標示字串逐字是章節標題；NotebookLM 摘要以漢字計 ≥100（不含標點、空白、拉丁字母與數字；DA B-15）；摘要只整理 acceptor 提供的原始輸出與來源；ChatGPT PDF 附於報告附錄並放入 ZIP；「GPT 輔助內容」如實揭露 ChatGPT 與 Claude Code 各自的用途；`python -m hw2.report --final` 成功（沒有【待填】） | 報告 §10、§11、附錄 B（PDF 版本在最後接上 ChatGPT 對話 PDF 的原頁）；`hw2/report.py`（材料 sha256 與收件紀錄核對、摘要漢字數、摘要逐句對照表）、`hw2/pdf_append.py`；`tests/test_report.py`、`tests/test_pdf_append.py`；acceptor 材料與 Claude Code 依材料整理的章節（`acceptor_materials/`、`acceptor_materials/derived/`，不進 git）；sha256 與核對紀錄在 `doc/governance/worklog/issue-66.md` | #66 | PASS（final 建置無【待填】；derived 三檔 sha256＝#66 R1 審查版本；報告 PDF 149 頁＝28＋121；ChatGPT PDF sha256＝收件值，#67 worklog §7、§9） |
| A-7 | T-繳交：`<學號>_hw2.ipynb`、PDF 報告、`<學號>_hw2.zip`〔老師要求〕 | ZIP 檔名與主程式檔名用學號（只在本機打包時由 `.local/packaging.json` 讀取）；ZIP 內含主程式、報告 PDF、ChatGPT PDF、`hw2/`、`requirements.txt`、資料 CSV、README、`results/`、dashboard 靜態檔；記錄 ZIP 的 sha256 與檔案清單 | 打包紀錄（#67 worklog） | #67 | PASS（`<學號>_hw2.zip`，56 個項目，sha256 與清單見 #67 worklog §7） |
| A-8 | T-GitHub（optional 條款；本專案使用 GitHub 所以適用）：README 整理流程與成果〔老師要求〕（DA T-義務） | 單元 `README.md` 有：目的、資料來源與授權、流程、成果、重跑步驟（含學號設定路徑 `.local/packaging.json`）、dashboard 連結、檔案配置；成果段的數字與匯出結果一致 | `README.md`；`tests/test_report.py`（README 的章節與數字核對） | #67 | PASS（`tests/test_report.py`；README 加入打包步驟，#67 worklog §3、§6） |
| A-9 | T-評分：「Kaggle 名次（若有）」〔老師要求〕（Q38；DA F-4） | 報告說明本資料集不是競賽、沒有名次，因此不適用，並以預測結果評估（指標、預測圖、PI 涵蓋率）取代 | 報告 §1.4；`tests/test_report.py` | #67 | PASS（乾淨環境 pytest 395 passed、Node 9 passed，#67 worklog §6） |
| A-10 | 報告內容：網路上主流或更優解法之比較與說明〔老師要求〕（Q37） | 3–5 個公開的 King County 解法，每一項有可開啟的連結、方法與來源自報的指標（附在來源中的位置）、不可比之處；沒有無來源的主張 | 報告 §8；`report/external_sources.json`；`tests/test_report.py`；#67 逐一開啟連結 | #67 | PASS（5 個連結都可開啟；SciTePress DOI 以瀏覽器開啟，#67 worklog §9） |

## B. 課堂口頭要求與採用的補充建議（Brief §3.2）

| ID | 要求（來源） | 可觀察的檢查 | 證據位置 | 執行 | 狀態 |
| --- | --- | --- | --- | --- | --- |
| B-1 | Dashboard（課堂口頭要求）：`home_work_02/index.html`；Pages URL；ZIP 內完全離線可用 | 見 D 節（dashboard 人工檢查）與 E 節 OV-1；報告與 README 不把 dashboard 寫成作業頁的書面要求 | `index.html`、`assets/`；報告 §7.1、§9 與標示對照表 | #67 | PASS（ZIP／`file://`，見 OV-1）；Pages URL 見 D-12（NOT TESTED，pending merge） |
| B-2 | Adjusted R²〔依老師補充建議〕 | 只對 OLS 子集模型在 log 尺度、以 n_train 與實際秩計算；Ridge／Lasso 與 CV 聚合值標「不適用」 | `tests/test_ols.py::test_adjusted_r2_uses_the_actual_rank_not_the_column_count`；`comparison.csv`；報告 §6.2 | #67 | PASS（乾淨環境 pytest 395 passed、Node 9 passed，#67 worklog §6） |
| B-3 | 五大回歸假設診斷〔依老師補充建議〕 | 線性、誤差獨立（含 training 實際的重複交易）、同質變異、常態、多重共線性各有圖或數值與解讀；只用 training 殘差；違反只揭露 | `results/figures/diag_*.png`、`results/tables/diagnostics_*.csv`；`tests/test_diagnostics.py`；notebook 5.6；報告 §6.4 | #67 | PASS（乾淨環境 pytest 395 passed、Node 9 passed，#67 worklog §6） |
| B-4 | Deployment 的預測新樣本與模型解釋〔依老師補充建議〕 | `predict_price()` 示範；係數的百分比讀法、one-hot 相對基準、標準化讀法（OLS 原始尺度；每 1 個 training sd 的百分比只引自 `final_model_coefficients.csv`）；permutation importance 標「專案延伸」；非因果提醒；報告不呈現 Ridge／Lasso 的係數（DA R-1.1、R-1.3、R-1.5） | notebook 6.2～6.5；`tests/test_deployment.py`；報告 §7.2、§7.3 | #67 | PASS（乾淨環境 pytest 395 passed、Node 9 passed，#67 worklog §6） |
| B-5 | Ridge／Lasso 對照〔依老師補充建議〕（CC-1） | alpha 只以 training CV 選；不參與 winner；Test 各一次、只報 USD 的 MAE、MSE、RMSE、R²；沒有 PI、涵蓋率、即時預測；訓練 CV 與 Test 指標分開標示（G-1～G-4） | `tests/test_comparison.py`、`test_testgate.py`、`test_test_section.py`；`comparison.csv`；dashboard 比較表；報告 §5.2、§6.2 | #67 | PASS（乾淨環境 pytest 395 passed、Node 9 passed，#67 worklog §6） |
| B-6 | 三種標示 | 報告前段有對照表，章節層級有標示；補充建議不寫成老師要求；依據是 Brief §3.2 與 Spec「報告與打包」，不引用未接受的 OC v2 草稿（DA I-2） | 報告「標示說明與對照表」與各章標題；`tests/test_report.py` | #67 | PASS（乾淨環境 pytest 395 passed、Node 9 passed，#67 worklog §6） |

## C. 已接受的決定與驗證（Brief §4～§7、§10、§11；DA 義務）

| ID | 要求（來源） | 可觀察的檢查 | 證據位置 | 執行 | 狀態 |
| --- | --- | --- | --- | --- | --- |
| C-1 | 資料 sha256 與結構（Brief §4） | 載入時先核對 sha256 再解析；21 欄、21,613 列、21,436 個唯一 `id`、`sqft` 恆等式 | `tests/test_data.py` | #67 | PASS（乾淨環境 pytest 395 passed、Node 9 passed，#67 worklog §6） |
| C-2 | 以 `id` 分組的 80/20 切分與分組 fold（Brief §4、§10） | train/test 無共同 `id`、聯集為全部列、同 seed 重現；fold 兩兩無共同 `id` | `tests/test_split.py` | #67 | PASS（乾淨環境 pytest 395 passed、Node 9 passed，#67 worklog §6） |
| C-3 | 需要 fit 的前處理只看當次訓練列（Brief §4、§10） | 改動驗證列不改變類別與統計量；未見 zipcode 編為基準 | `tests/test_preprocess.py`、`test_models.py::test_cv_fold_uses_only_its_training_rows` | #67 | PASS（乾淨環境 pytest 395 passed、Node 9 passed，#67 worklog §6） |
| C-4 | fold 內選擇與 canonical subset（Spec「分割與交叉驗證」） | 改動某 fold 的驗證列不改變該 fold 的子集；canonical subset 只由整個 training set 決定 | `tests/test_selection.py`、`test_comparison.py::test_pvalue_selection_boundary_is_fold_internal` | #67 | PASS（乾淨環境 pytest 395 passed、Node 9 passed，#67 worklog §6） |
| C-5 | 以 ln(price) 建模、USD 報告；exp(ŷ_log) 是條件中位數的估計（Brief §4；DA TK-3） | 報告寫明 exp(ŷ_log) 估計的是條件中位數，不是條件平均 | 報告 §4.3、§7.4；`tests/test_report.py` | #67 | PASS（乾淨環境 pytest 395 passed、Node 9 passed，#67 worklog §6） |
| C-6 | CV winner 的選擇偏誤（Spec「分割與交叉驗證」；DA TK-3） | 報告寫明 CV winner 的 CV 分數帶有樂觀偏誤、Test 是獨立估計；不把 CV 分數寫成不偏估計 | 報告 §6.2；`tests/test_report.py` | #67 | PASS（乾淨環境 pytest 395 passed、Node 9 passed，#67 worklog §6） |
| C-7 | Test 只評估一次，只評估授權集合（Brief §5、BR-01；CC-1；DA G-3、D-1～D-3） | 守門在 alpha 與 winner 固定後才開啟，每個模型一次；`test` 的 `ols_subset` 鍵＝授權清單、`metric_only` 只有 Ridge／Lasso；報告與 README 以 #63 那一次為唯一的正式評估（run `fe76019b…`、`result_digest` `b53ff286…`），重跑是重現（DA N-5） | `tests/test_testgate.py`、`test_model_data_official.py`；`doc/governance/worklog/issue-63.md` §5；報告 §6.1、附錄 A；README「重跑步驟」；報告建置程式核對 `result_digest` | #67 | PASS（重現的 `result_digest`＝`b53ff286…`、`selection_digest`＝`44f7723e…`，`evaluations_in_this_run` 1，#67 worklog §4、§5） |
| C-8 | 共用模型的呈現與評估數量（DA D-2、D-3） | 每個 winner 以自己的身分呈現並標明與哪些 winner 為同一模型；「評估了幾個模型」指互不相同的 OLS 模型數加 Ridge、Lasso，由匯出結果計算 | 報告 §5.1、§6.1、§6.2；dashboard 比較表與 Test 區塊 | #67 | PASS（乾淨環境 pytest 395 passed、Node 9 passed，#67 worklog §6） |
| C-9 | `methods`／`baselines` 沒有 test 欄位；dashboard 的 UI 不以 `test_inputs` 評估任何模型（Spec 不變量；DA B-3、TK-4） | pytest 與靜態檢查 | `tests/test_model_data_official.py::test_sections_and_no_test_field_outside_test`；`tests/test_dashboard_static.py::test_ui_predicts_only_from_user_inputs_and_never_from_test_inputs` | #67 | PASS（乾淨環境 pytest 395 passed、Node 9 passed，#67 worklog §6） |
| C-10 | 參數式 PI；涵蓋率、計數、平均寬度、二項近似（Brief §6；SR-08、SR-12） | 逐筆獨立重算一致；報告列出涵蓋率、計數、n_test、平均寬度、二項近似並標明獨立假設，列出 Test 的房屋數與重複交易筆數，不陳述偏差的方向或幅度；不宣稱保證 95%；偏離時分析原因 | `tests/test_ols.py`、`test_test_section.py`；報告 §6.3 | #67 | PASS（乾淨環境 pytest 395 passed、Node 9 passed，#67 worklog §6） |
| C-11 | Python／JS 一致性（Brief §10） | 點預測、PI、涵蓋狀態、前處理（日期、整修年、zipcode）逐筆一致（相對容差 1e-6；涵蓋狀態完全相等） | `tests/js/core.test.js`、`tests/test_node_core.py` | #67 | PASS（乾淨環境 pytest 395 passed、Node 9 passed，#67 worklog §6） |
| C-12 | 固定 seed、鎖版本、乾淨環境重跑一致（Brief §10；DA §9.3 條件 1～8、N-3） | 完整重跑前核對 selection digest＝`44f7723e…` 與選擇／評估模組未改；新建虛擬環境、安裝、非互動執行 notebook、重跑測試、建置報告、打包；`result_digest` 與 #63 bit-exact 一致；notebook 執行序號 1…N 連續；只有 N-3 列出的時間與識別欄位可以不同 | #67 worklog；`results/model_data.json` `meta.test_evaluation` | #67 | PASS（條件 7 (a)(b) 在重跑前成立；新建 venv、安裝、非互動執行一次、測試、建報告、打包；只有 N-3 欄位不同，#67 worklog §4–§7） |
| C-13 | 報告與 README 的數字都引自匯出結果（Brief §8 Q26；Spec「報告與打包」） | 報告的數字、表與圖在建置時注入；模板沒有手抄的結果數字；README 成果段的每個數字與匯出結果一致；報告引用的每張分析圖是 `results/figures/` 的檔案、每張表來自 `results/tables/` 或 `model_data`（DA TK-2） | `hw2/report.py`；`tests/test_report.py`；#67 抽查 | #67 | PASS（乾淨環境 pytest 395 passed、Node 9 passed，#67 worklog §6） |
| C-14 | 不得使用 mock 數值或 wireframe 截圖（H-4；A-5） | 報告、README、dashboard 沒有 `design/wireframe/mock-data.js` 的數值或 wireframe 截圖；報告的截圖在建置時擷取自 `index.html` | `hw2/report.py`、`report/chrome_capture.js`；#67 與 Reviewer 抽查 | #67 | PASS（mock-data.js 的數字在報告、README、dashboard 中只有巧合的真實值；#67 worklog §9） |
| C-15 | 執行時間量測（Brief §5 Q34） | 每個方法的路徑時間寫入 `meta.timing_s`／`meta.path_timing_s`，報告與 README 引用位置 | `tests/test_selection.py::test_run_path_methods_times_every_method`；報告 §5.4 | #67 | PASS（乾淨環境 pytest 395 passed、Node 9 passed，#67 worklog §6） |
| C-16 | 學號（Brief §11 BR-03；DA S-1～S-6） | 追蹤檔案、commit 歷史與 commit message 都沒有實際學號（以 `.local/packaging.json` 的值 `git grep -F`，不印出值）；任何追蹤檔案一律寫 `<學號>` | `tests/test_repo_hygiene.py::test_no_tracked_file_contains_the_student_id`；S-2 比對紀錄（run record） | #67 | PASS（`git grep -F` 0 命中；本票 commit 內容與訊息 0 命中；只輸出計數，#67 worklog §9） |

## D. Spec 人工檢查表

### D.1 Dashboard

| ID | 檢查 | 證據位置 | 執行 | 狀態 |
| --- | --- | --- | --- | --- |
| D-1 | 必要區塊 (1) 方法與 k 控制、(2) KPI 卡、(3) 指標 vs k 圖、(5) 即時預測器、(6) 實際 vs 預測圖、(9) 方法與限制都存在並渲染 | 截圖與瀏覽器紀錄 | #67 | PASS（Chrome 155／Edge 155 截圖與 CDP 紀錄，#67 worklog §8） |
| D-2 | zh-TW，沒有缺字方塊（含圖表文字） | 截圖 | #67 | PASS（截圖目視：沒有缺字方塊；k 軸刻度與價格刻度已修正，#67 worklog §3、§8） |
| D-3 | 方法與 k 切換：KPI、指標 vs k 圖、預測器、Test 區塊同步更新；All-in 時 k 固定、不可改 | 操作紀錄 | #67 | PASS（#67 worklog §8） |
| D-4 | 「比較全部」：四個路徑方法的 k 路徑疊圖（All-in、Ridge、Lasso 為參考線）與比較表 | 截圖 | #67 | PASS（#67 worklog §8） |
| D-5 | 預測器：只顯示當前模型用到的 source feature；預設 training 中位數；超出範圍有警告仍計算；zipcode 下拉、日期輸入、「未整修」選項；未見 zipcode 的警告「此 zipcode 不在模型的訓練類別中，已以基準類別計算」 | 操作紀錄 | #67 | PASS（#67 worklog §8） |
| D-6 | 來源標示：KPI「訓練 CV（USD）」；係數表「全訓練集擬合，R²／Adjusted R² 為 log 尺度」；Test 區塊「Test 評估（USD）」並標示所展示的方法與 k | 截圖；`tests/test_dashboard_static.py` | #67 | PASS（#67 worklog §8） |
| D-7 | 比較表的「訓練 CV（USD）」與「Test 評估（USD）」分欄；Ridge／Lasso 的 Test 指標只出現在比較表，不進 Test 區塊、KPI 或實際 vs 預測圖（DA G-4） | 截圖；`tests/test_dashboard_static.py::test_comparison_table_separates_training_cv_and_test_columns` | #67 | PASS（#67 worklog §8） |
| D-8 | 選取非 winner 時，有清楚可見的提示說明 Test 區塊展示的是哪個模型；dashboard 操作不觸發新的 Test 評估 | 操作紀錄；`tests/test_dashboard_static.py::test_test_numbers_are_read_only_from_the_exported_test_section` | #67 | PASS（#67 worklog §8） |
| D-9 | `invalid` 候選以明確標示呈現且不可成為 winner（正式資料沒有 invalid 候選；以 fixture 驗證） | `tests/js/core.test.js`（fixture）；`tests/test_models.py::test_invalid_candidates_never_win_even_with_the_lowest_rmse` | #67 | PASS（乾淨環境 pytest 395 passed、Node 9 passed，#67 worklog §6） |
| D-10 | 實際 vs 預測圖的可讀性與反應性 SR-09 (a)～(e)：即 E 節 OV-6 | E 節 | #67 | PASS（見 OV-6） |
| D-11 | 離線：即 E 節 OV-1 | E 節 | #67 | PASS（見 OV-1） |
| D-12 | GitHub Pages URL 上重做同一份檢查（Brief §7、§10；DA TK-1；AD-3） | 合併進 `main` 後的 Lightweight work item（觸及 H-2，需 audit） | 合併後的 work item | **NOT TESTED（pending merge）** |

### D.2 報告

| ID | 檢查 | 證據位置 | 執行 | 狀態 |
| --- | --- | --- | --- | --- |
| D-13 | 章節完整：CRISP-DM 六章（含特徵選擇比較、假設診斷、區間驗證、模型解釋）、資料來源與研究脈絡（含 Kaggle 名次不適用）、GPT 輔助內容、NotebookLM 摘要、主流或更優解法比較、dashboard 連結與截圖、附錄 ChatGPT PDF | `report/report.md`；`dist/report/hw2_report.pdf`（本機建置，不進 git） | #66、#67 | PASS（final 報告章節，#67 worklog §7、§9） |
| D-14 | 三種標示：見 B-6 | — | #67 | PASS（乾淨環境 pytest 395 passed、Node 9 passed，#67 worklog §6） |
| D-15 | 數字與匯出一致（抽查）：見 C-13 | — | #67 | PASS（乾淨環境 pytest 395 passed、Node 9 passed，#67 worklog §6） |
| D-16 | 附錄 ChatGPT PDF：見 A-6 | — | #66 | PASS（見 A-6） |
| D-17 | NotebookLM 摘要字數（B-15）與可追溯性：見 A-6 | — | #66 | PASS（見 A-6） |
| D-18 | 主流解法的來源連結可開啟：見 A-10 | — | #67 | PASS（見 A-10） |
| D-19 | 報告為 zh-TW，可建置為 PDF（`python -m hw2.report`）；待填位置清楚標示、不含範例文字 | `dist/report/`；`tests/test_report.py` | #67 | PASS（乾淨環境 pytest 395 passed、Node 9 passed，#67 worklog §6） |

### D.3 Repo

| ID | 檢查 | 證據位置 | 執行 | 狀態 |
| --- | --- | --- | --- | --- |
| D-20 | `git grep` 無實際學號：見 C-16 | — | #67 | PASS（見 C-16） |
| D-21 | 追蹤檔案不含 acceptor 材料、PDF（老師文件除外）、ZIP、`.env`、`kaggle.json`、打包設定與輸出 | `tests/test_repo_hygiene.py::test_no_forbidden_files_are_tracked`；`git ls-files` | #67 | PASS（乾淨環境 pytest 395 passed、Node 9 passed，#67 worklog §6） |

### D.4 乾淨環境重跑

| ID | 檢查 | 證據位置 | 執行 | 狀態 |
| --- | --- | --- | --- | --- |
| D-22 | 新建虛擬環境、安裝、非互動執行 notebook、重跑測試、建置報告、打包；數字與追蹤的結果檔一致：見 C-12 | #67 worklog | #67 | PASS（見 C-12） |

## E. Open Verification Items（OV-1～OV-6；Spec rev 5、AD-1）

| ID | 項目 | 分類 | 可觀察的檢查 | 證據位置 | 執行 | 狀態 |
| --- | --- | --- | --- | --- | --- | --- |
| OV-1 | 完全離線 `file://` | **硬性 PASS／FAIL gate** | 把繳交 ZIP 解壓到網路停用、沒有本機伺服器的機器，以瀏覽器開啟 `index.html`：必要區塊全部渲染、方法與 k 切換有效、預測器給出點預測與 95% PI、實際 vs 預測圖可縮放、zh-TW 無缺字；對外請求為零（DevTools 網路面板）；`python -m hw2.offline_scan` PASS | #67 worklog；截圖；`hw2/offline_scan.py` | #67 | **PASS**（ZIP 解壓後 `file://`，Chrome 155 與 Edge 155 可見視窗；瀏覽器層斷網：DevTools offline、主機名稱全部無法解析、無效 proxy；對外請求 0；extracted 副本靜態掃描 PASS，#67 worklog §8.1） |
| OV-2 | 手機／觸控 | **Required gate**：Chrome DevTools 375 px 與 768 px 無水平溢出、主要功能可操作。真實觸控裝置：有環境時補測（best effort） | DevTools 量測紀錄；真實裝置紀錄 | #67 worklog | #67 | **PASS**（required：375／768 px 各 8 種狀態水平溢出 0 px、主要功能可操作，#67 worklog §8.2）；真實觸控裝置 **NOT TESTED**（無環境） |
| OV-3 | 跨瀏覽器 | **Required gate**：Chrome 或 Edge PASS。Firefox／Safari：best effort | 各瀏覽器名稱與版本、結果 | #67 worklog | #67 | **PASS**（required：Chrome 155.0.8059.80、Edge 155.0.4283.62）；Firefox 123.0.1 best effort PASS（核心項目，#67 worklog §8.3）；Safari **NOT TESTED**（無環境） |
| OV-4 | Accessibility | **Required gate**：鍵盤操作、focus visibility、正確 label、選單狀態（`aria-expanded`）與基本語意。螢幕閱讀器：best effort | 鍵盤與 DOM 檢查紀錄 | #67 worklog | #67 | **PASS**（required：鍵盤、focus、label、`aria-expanded`、基本語意，#67 worklog §8.4）；螢幕閱讀器 **NOT TESTED**（無環境） |
| OV-5 | 色彩對比 | **Required gate**：一般文字 ≥ 4.5:1、大字 ≥ 3:1；重要狀態與圖表不可只靠顏色辨識 | 對比量測值與方法 | #67 worklog | #67 | **PASS**（DOM 文字 792 處最低 6.49:1；canvas 文字最低 5.74:1；Test 圖以形狀區分涵蓋狀態，#67 worklog §8.5） |
| OV-6 | 全部 Test 逐筆 PI 的渲染效能 | **硬性 PASS／FAIL gate**（SR-09 (a)～(g)） | (a) 首次繪製 ≤ 3 秒（navigation start → 實際 vs 預測圖第一次完整繪製，頁面 `window.HW2_PERF.firstDraw`）；(b) 方法／k 切換、縮放與平移的互動更新 ≤ 1 秒，沒有「網頁沒有回應」；(c) 預設視圖中 y=x 線、區間內外的點可分辨，圖例與軸標籤可讀；(d) 放大到任一價格十倍區間或游標停留時可分辨個別線段與端點；(e) 游標停留可得知該筆的預測、實際與區間；(f) 記錄於下表；(g) 不得以抽樣、聚合或省略任何 Test 樣本與 PI 達成 | 下表；#67 worklog | #67 | **PASS**（下表；#67 worklog §8.6） |

### OV-6 量測紀錄（SR-09 (f)；#67 填寫，只記實測值）

| 項目 | 值 |
| --- | --- |
| 瀏覽器名稱與版本 | Google Chrome 155.0.8059.80；Microsoft Edge 155.0.4283.62（可見視窗，非 headless） |
| 作業系統 | Windows 11 專業版 10.0.26200（acceptor 的電腦） |
| CPU 與記憶體 | 13th Gen Intel Core i9-13900HX（24 核／32 執行緒）；31.7 GB |
| n_test（全部繪製的 Test 筆數） | 4,323（`HW2_PERF.firstDraw.nPoints`；全部繪製，不抽樣、不聚合） |
| 量測方式（頁面內建時間戳或 DevTools Performance） | 頁面內建時間戳 `window.HW2_PERF`（首次繪製：navigation start → 散佈圖第一次完整繪製；互動：輸入事件 `timeStamp` → 受影響區塊重繪完成），以 CDP 送出真實的滑鼠、滾輪與鍵盤事件；另以 `PerformanceObserver('longtask')` 記錄長任務；解壓後的 ZIP，`file://` |
| 首次繪製（各次） | Chrome：254（冷啟動）、78.1、81.2、79.7、80.1 ms；Edge：251.6（冷啟動）、90.3、88.5、88.4、85.3 ms（門檻 3,000 ms） |
| 互動更新：方法／k 切換、縮放、平移（各次） | Chrome 最大值：方法切換 14.3 ms（6 次）、k 切換 7.5 ms（3 次）、滾輪縮放 34.2 ms（10 次）、拖曳平移 4.4 ms（3 次）、縮放按鈕 4.0 ms（5 次）；Edge 最大值：16.5、3.7、30.2、3.9、3.6 ms（門檻 1,000 ms）。互動期間長任務 0 個，沒有「網頁沒有回應」提示或對話框。各次數值見 #67 worklog §8.6 |

## F. 待決與交接

- **Pages 檢查（D-12）**：依 AD-3 在合併進 `main` 之後以獨立的 Lightweight work item 執行；Spec Integration Audit 與 phase acceptance 把它列為 open item。
- **AI 證據（A-6、D-13、D-16、D-17）**：#66 已以 acceptor 2026-10-19 提供的 ChatGPT PDF 與 NotebookLM 材料整合（`doc/governance/worklog/issue-66.md`）；報告 PDF 的最終建置與 ZIP 內容已由 #67 驗收（A-6、A-7）；final 建置只接受 #66 R1 審查過的 derived 版本（`hw2/report.py` 的 `DERIVED_REVIEWED`）。
- **學號（A-7、C-16、D-20）**：acceptor 已提供 `.local/packaging.json`（run record §19）；#67 已核對（C-16）。DA S-4、S-5 的比對由 #67 R1、Spec Integration Audit 與合併前各自重做。
- **OV best-effort 項目**：真實觸控裝置、Safari、螢幕閱讀器沒有環境，記 NOT TESTED（AD-1）。
