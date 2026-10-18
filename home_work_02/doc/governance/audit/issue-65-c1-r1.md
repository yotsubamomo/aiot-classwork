# Audit record — Issue #65，cycle 1，R1

| 欄位 | 內容 |
| --- | --- |
| Work Contract | GitHub issue #65「HW2 T6 報告 draft（Markdown→PDF）、單元 README 與 ACCEPTANCE.md」（OPEN，`ready-for-agent`；高風險 H-2、H-4）；Parent Spec `home_work_02/doc/spec/SPEC.md` rev 5（#59）「報告與打包」「人工檢查表」、OV gate 分類；DA derivation `doc/governance/decisions/derivation-SPEC.md` §4 T-義務、§5、§7 F-4、§9.1（#65）、§9.3、§9.4 I-2、§9.5 TK-2、TK-3、TK-5、§11 G-4；DA 紀錄 `decision-20261018-high-risk-categories.md`（A-1～A-8）、`decision-20261018-issue60-a4-student-id.md`（S-1～S-6）、`decision-20261018-issue62-shared-subset-test-key.md`（D-2、D-3）、`decision-20261018-issue63-js-tolerance.md`（T-1）、`decision-20261018-issue64-notebook-rerun.md`（N-4、N-5、I-4）、`decision-20261018-issue64-standardized-reading.md`（R-1.1、R-1.3、R-1.5）、`decision-20261019-issue65-labels-figures.md`（L-1～L-3、F-1～F-5、O-1）；Outcome Contract `doc/governance/outcome-contract.md`（Brief @ `dff7c55c`＋CC-1、AD-1～AD-3）；上位契約 `doc/requirement/`；acceptor 指示：run record §14（第 4、7 點）與 §15 的 #65 process note |
| 受審 subject | branch `home_work_02-regrill`，**最終 subject＝修正後的 implementation commit `0b57c0265f01e7732fdd1250e58101819a1b416f`**（第一次 implementation commit `741a21ba29dfb5ad7a2c2d1ac2f02d5eeb20035d`；BASE＝`bc56c064571d19b6d047ac4380540ebd3fac8a19`）。`git log bc56c06..HEAD`：只有 `741a21b` 與 `0b57c02` 改動 `doc/governance/**` 以外的檔案；`6910b87`、`fbd7dec`、`170277e`、`e03fcb0`、`a0a1b70`、`0c46bf3` 都只改 `doc/governance/**`（record-only，Bindings §7）。審查時 HEAD＝`0c46bf3`；`git diff --stat 0b57c02 HEAD -- . ':!home_work_02/doc/governance'` 為空，`git status --porcelain home_work_02` 審查前後皆為空（只有 ignored 檔）。範圍內全部路徑都在 `home_work_02/`，沒有 `doc/requirement/`。`origin/home_work_02-regrill`＝`60d7fa67`，範圍內 commit 都沒有 push |
| Audit 種類 | **R1**（full independent audit of accepted work scope），**cycle 1**。**本 record 不是 Spec Integration Audit**（Spec rev 5 有多張票，不適用單 Ticket fast path；派工也沒有指定兼作） |
| 角色 | `primary_reviewer`（definition `gov-primary-reviewer`；Bindings §3.1 R-PR mapping `claude-opus-5-5`／`xhigh`） |
| Assurance (a)：context independence（治理 §2.3；Bindings §3.7） | (1) **Independent context**：以 Agent tool 派工的 `gov-primary-reviewer`（非 fork），空白 context；派工內容只有路徑與識別。Worklog、run record、DA 紀錄中 Executor 的敘述與數字都只當作待驗證主張，下文的事實都是我自己核對的。(2) **Verifiable binding**：見 (b) 欄。(3) **Autonomous access**：自行讀取 `gh issue view 65`、Spec、DA 紀錄、OC、Brief、CONTEXT、老師需求轉寫、git 歷史與 diff、全部新增與修改的檔案、notebook JSON；自行執行完整 pytest、Node test、離線掃描、報告建置（含 PDF）、獨立的數字交叉核對、預測圖的兩次獨立重產、mutation probes（在 `git archive 0b57c02` 的 scratchpad 複本上），並自行下載、閱讀四個外部來源核對數字。(4) **Self-written record**：本檔由 Reviewer 以自己的 Write 工具寫入 |
| Assurance (b)：model diversity（Bindings §5） | **Executor**：agentId `a4779b376d79e3353`，`agentType` `gov-executor`，Reviewer 以 Bindings §3.6 的同一邏輯自行掃描 session `4bbff425-7ff9-4cdc-b64c-cc68e824e1b1` 的 subagent transcript：`('claude-opus-5-5', 'high')` 284 則、單一元素，符合 O-1（run record §15 記錄的是採用 return 時的 210 則與修正後的 273 則）。**本 review**：agentId `a3ff011d2766ef922`，`agentType` `gov-primary-reviewer`，撰寫本 record 前觀測 `('claude-opus-5-5', 'xhigh')` 217 則、單一元素；全程核對由派工者依 Bindings §3.6 在採用本 record 前執行。**無 model diversity**（兩者同為 `claude-opus-5-5`）。Bindings §5 不宣告 diversity 關係，不記 `diversity_lost`（A-8） |
| 日期 | 2026-10-19 |

## 1. 審查方法與環境

腳本與輸出都在 session scratchpad 的 `r65/`（不在 repo）。環境：單元 `.venv`（Python 3.11.2）、Node v24.19.0、Chrome 155.0.8059.80（headless）。

**不重新評估**：我沒有執行 `hw2.run_notebook` 或任何 notebook cell，沒有開啟守門，也沒有對 test 列評估任何模型。我讀的只有追蹤的匯出結果（`results/model_data.json`、`results/tables/*.csv`、`results/figures/*.png`）。pytest 由 `tests/conftest.py` 的 `pytest_configure` 與 autouse fixture 在整個 process 關閉正式守門（第 21～41 行）。

- **(i) 工作樹測試**（工作樹＝`0b57c02`，record-only 差異除外）：`.venv/Scripts/python -m pytest -q -rs -p no:cacheprovider` → **338 passed, 1 skipped**（skip：`tests/test_repo_hygiene.py:71`，學號設定未提供），48.4 s。`node --test tests/js/core.test.js` → 9 pass、0 fail、3 skip（fixture 項目由 pytest 的 `test_node_core.py` 執行；`official: JS prediction, PI and covered reproduce the contract on every test row` 通過）。`python -m hw2.offline_scan` → `scanned 6 files: PASS (0 findings)`。
- **(ii) 報告建置**：`python -m hw2.report --out <scratchpad>/r65/build` → 成功，11.0 s；`hw2_report.md`、`.html`、`.pdf`（**25 頁**）；8 張 `fig:` 圖全部取自 `results/figures/`；5 張截圖由 headless Chrome 以 `file://` 開啟 `home_work_02/index.html` 擷取；`external_requests: []`；`first_draw_ms` 238；pending＝`gpt`、`notebooklm`、`chatgpt_pdf`。我逐章閱讀了渲染後的 Markdown（489 行），並以 `pdftotext` 抽出 PDF 文字核對章節順序與標示。截圖 `test.png` 是正式 dashboard（Lasso 路徑排序 k = 17，n_test 4,323，Test RMSE US$183,370，涵蓋 4,083／4,323），不是 wireframe。
- **(iii) 獨立的數字交叉核對**（`xcheck.py`、`xcheck_comp.py`；自行解析渲染後的 Markdown 表格，不使用 `hw2.report` 的格式化函式）：k 路徑表 72 格與 `cv_by_method_k.csv`（含 ★ 與 `is_method_winner` 一致）；比較表 8 列 × 各欄與 `comparison.csv`，以及 `comparison.csv` 的 Test 值與 `model_data.test` 一致；metric-only 表與 `model_data.test`（`kind`、alpha、RMSE、MAE、R²）；區間表與 `model_data.test`（n_test、涵蓋筆數＝`sum(covered)`、涵蓋率、平均寬度、二項近似半寬＝1.96·√(p(1−p)/n)）；係數表 17 列與 `final_model_coefficients.csv`（係數、每單位 %、`train_sd`、`pct_per_train_sd`；one-hot 不列、sd 欄空白者顯示「—」）；permutation 表與 CSV；alpha 表與 `alpha_cv.csv`（網格點數、選出的 alpha 等於網格最小值、CV RMSE 隨 alpha 單調不減）；正文中的整體 winner Test RMSE、MAE、R²、涵蓋率、Test − CV 差距與它對各折標準差的倍數、資料列數與欄數、Test 房屋數＝`test_inputs` 唯一 `id` 數、重複交易＝列數 − 房屋數；README「成果」段的每個數字。**350 項核對，0 項不符。**
- **(iv) 預測圖（DA F-5 的 A-2 自行重做）**：
  - 正式產物：`results/model_data.json`（sha256 `fa86d76c…b891e3`）、`assets/model_data.js`（`37626bf9…5b29a72`）、`results/tables/` 8 個 CSV、既有 7 張 PNG（`diag_*`、`explain_*`）與 `git show 741a21b:` 的 blob 逐一比對：**17／17 相同**。`git diff --quiet 052984b 0b57c02 -- results/model_data.json assets/model_data.js results/split comparison.csv alpha_cv.csv cv_by_method_k.csv` 成立；`git diff --stat 003b825 0b57c02 -- assets index.html results` 只有新增的 `eval_actual_vs_predicted_pi.png`。
  - `export.result_digest(model_data)`＝`b53ff286ae0734add8b272089aba904a1cb7f5aca444a62d356420b25dc3cfc6`；manifest `run_id` `fe76019b9af84b1e8ff46095d5ac0fb2`、`selection_digest` `44f7723e…4b28`、`official_data` true、`code_revision` `d413e58`（`package_modified: false`）。
  - 凍結模組：`git diff --stat 052984b 0b57c02 -- hw2/{data,split,preprocess,selection,models,comparison,ols,metrics,contract,testgate,export}.py requirements.txt` 為空。
  - Notebook（`git show` 四個版本以 JSON 比對）：`0b57c02` 有 73 個 cell；cell 0–45 的 source 與 `052984b` 相同；cell 0–45 的完整 JSON（含輸出）與 `741a21b`（＝`003b825`）相同；原本 cell 46 之後的 25 個 #64 cell 往後移兩格、完整 JSON 不變；notebook metadata 不變。新增 cell 46（`#### 5.5.1 …（老師要求：預測圖加上預測區間）`，說明只讀已匯出的結果、不開守門）與 cell 47（`prediction_plot.prediction_figure(model_data)`、`display`、`is_formal` 時存檔；不含 `gate.`／`evaluate`）。Cell 47 輸出：`image/png`，兩個面板各 4,323 條 PI 線段與 4,323 個點（`allin` 區間內 4,082、`forward_sfs_k17` 4,083），`written: results/figures/eval_actual_vs_predicted_pi.png`，沒有 stderr。六章標題 `## 1. Business Understanding`…`## 6. Deployment` 位於 cell 2、4、12、20、34、60，順序不變。執行序號 `1…28, 2, 25…35`（DA F-4 第 3 點與 N-2 的過渡狀態，交 #67 N-3）。
  - **決定性**：兩個獨立 process（`python -I -W error`，`Agg`）各自只以追蹤的 `model_data.json` 呼叫 `prediction_figure` 與 `save_prediction_figure`，寫到 scratchpad 的 `det1/`、`det2/`：兩者 sha256 都是 `8afdb90b6aa9f1fce55fc7cf565db6a8ecefa71c136541f49b55dc1a54bc4a39`，等於追蹤檔與 `git cat-file` 的 blob；沒有任何警告。兩個面板的線段數＝點數＝4,323、顏色與 `covered` 逐筆一致。`.gitattributes` 把 `results/figures/*.png` 標為 binary。
  - 圖本身（目視）：x＝Predicted、y＝Actual、log 刻度、y = x 虛線、每筆垂直 PI 線段、依 covered 著色、全部 4,323 筆；左面板標題「All-in baseline = RFE k=18」，右面板「Forward SFS k=17 = Backward SFS k=17 = Lasso path ranking k=17／overall CV winner: Lasso path ranking k=17」，符合 Q43 與 D-2；英文標籤，沒有缺字。
- **(v) 外部來源（H-4；AC「可開啟的來源連結」）**：五個連結（4 個來源與 Kaggle 資料集頁）以 `curl -L` 開啟：GitHub notebook、Atlantis PDF、ASSET DOI → `journal2.upgris.ac.id`、Kaggle 都是 HTTP 200；SciTePress DOI 以 Git 的 curl 會因伺服器憑證鏈不完整失敗，以 Windows `curl.exe`（schannel）開啟為 HTTP 200。各來源的數字我自己下載原文核對（檔案只放在 scratchpad 的獨立目錄，只讀不執行）：
  - [1] Bronner notebook（raw，commit `3e3a260`）：`cross_val_score(..., cv=10, scoring='r2')` 對 `X_train`；輸出「CV score: 0.699 ± 0.017」（2.1，也出現在 2.3.1 Ridge、2.3.2 Lasso）、0.721 ± 0.020（2.3.4 Random Forest）、0.815 ± 0.019（2.4.1 polynomial）；`test_size=0.2, random_state=0`；摘要「0.82」。全部相符。
  - [2] Mao & Yao 2020（Atlantis PDF，`pdftotext`）：Table 2 四列 77.1／77.0／76.6、87.7／87.3／87.4、89.1／90.4／88.2、89.2／89.4／88.5（%）；log 價格；7:3 與 10-fold CV；ASSEHR vol. 496、pp. 347–351。全部相符。
  - [3] Chen 2024（SciTePress PDF）：Table 4「R2 0.613」「Adj R2 0.613」「D-W value 1.983」；F(12, 21600)，即以全部 21,613 列擬合、沒有切分；模型沒有 zipcode、lat、long；pp. 258–263。全部相符。
  - [4] Hartono et al. 2024（ASSET PDF，20 頁）：Table 13 CatBoost 80:20 RMSE 126836.87、MAE 66156.36、R² 0.894；Table 15 Decision Tree 176777.96／90010.28／0.793；Table 17 XGBoost 136841.76／66983.77／0.876；Table 18 是跨切分比例挑選的最佳結果；摘要提到 linear regression baseline，正文沒有它的數字；vol. 6 no. 3、pp. 02403014-01～020。全部相符。
- **(vi) Mock／wireframe（A-5）**：`design/wireframe/mock-data.js` 中 4 位以上的數字與 `0.xxx` 值，在渲染後的報告中命中 7 個（`0.0001`、`2014`、`2015`、`21436`、`21613`、`4287`、`98001`）、README 中 1 個（`21613`），全部也是 `model_data.json` 中的真實值（資料結構事實、alpha 網格下緣、基準 zipcode）；模板 0 個。`hw2/report.py`、`report/report.md`、`report/chrome_capture.js`、`README.md` 都不引用 `wireframe`／`mock`。截圖由 `chrome_capture.js` 開啟 `UNIT_DIR/index.html` 擷取（`hw2/report.py:886`）。
- **(vii) Mutation probes（verify-the-verification）**：`git -c core.autocrlf=false archive 0b57c02 home_work_02` 解到 scratchpad；基準 `tests/test_report.py`＋`tests/test_prediction_plot.py` 24 passed。每個 mutant 只改一處、跑相關測試檔、還原（`mutants.py`）：
  - **DETECTED（6）**：P1 §6.3 改引 `shot:test` 取代 PNG；P2 `save_prediction_figure` 不檢查單元內的正式性；P3 點畫在 lower 而不是 actual；R1 建置不再核對 `result_digest`；R2 刪除「樂觀偏誤／獨立的估計」陳述；A1 ACCEPTANCE OV-6 標成 PASS。
  - **SURVIVED（6）**：L1 §6.4 標示〔依老師補充建議〕→〔老師要求〕；L2 §7.3 同樣改法；L3 §5.2 同樣改法；L4 §9 標題刪除「課堂口頭」；L5 §7.1 標題刪除「課堂口頭」；L6 §1.2 的「作業頁的「補充」段寫：」改成「作業頁正文另寫：」。見 **F-2**。
  - P2 的 mutant 讓 fixture 圖寫進了**複本**的 `results/figures/`；這只發生在 scratchpad 複本，repo 的工作樹沒有變化（`git status --porcelain home_work_02` 為空）。
- **(viii) A-4 掃描**：見第 4 節 H-1。

## 2. Acceptance criteria 逐條判定（#65）

| # | AC | 判定 | 證據 |
| --- | --- | --- | --- |
| AC-1 | Spec rev 5「報告與打包」的報告條款；Brief §8 的章節清單；F-4 補充：Kaggle 名次不適用說明、notebook 六章內容檢查、README 全部項目 | **PASS** | 報告：Markdown → PDF（(ii)）；CRISP-DM 第二～七章依序六階段，含特徵選擇比較 §5.1、假設診斷 §6.4、區間驗證 §6.3、模型解釋 §7.3；資料來源與研究脈絡 §1（兩條特徵數原文與交集 §1.2、Kaggle 名次不適用 §1.4）；主流或更優解法比較 §8（4 個來源，附連結與不可比之處）；dashboard 連結與截圖 §9；GPT 輔助內容 §10、NotebookLM 摘要 §11、附錄 A ChatGPT PDF。對照表在報告前段（`report/report.md:5-34`）。notebook 六章檢查：ACCEPTANCE A-4。README：目的、資料來源與授權、流程、成果、重跑步驟（含報告建置）、學號設定路徑 `.local/packaging.json`、dashboard 連結、檔案配置（`README.md:5-94`） |
| AC-2 | 數字單一來源 | **PASS** | 模板沒有手抄的結果數字（`tests/test_report.py:62-68` 通過）；全部數字、表在建置時由 `model_data.json` 與 `results/tables/` 注入；我的獨立交叉核對 350 項 0 不符（(iii)）；README 成果段的數字由 `tests/test_report.py:216-234` 核對並經我獨立核對 |
| AC-3 | 三種標示以對照表＋章節層級標示呈現，與 Brief 一致；補充建議不寫成老師要求 | **FAIL** | 對照表與 §5.2、§6.4、§7.2、§7.3、§7.1、§9 的標示正確；但第六、七章標題〔老師要求〕下直接引用作業頁「補充」段的文字，沒有出處說明，§6.2 的 Adjusted R² 內容沒有章節層級標示。見 **F-1**（blocking） |
| AC-4 | 主流解法每項有可開啟的來源連結與可比性說明；沒有無來源的主張 | **PASS** | 4 個來源（Brief Q37 的 3–5 個），每項有連結、資料、目標尺度、切分、方法、來源自報的指標與位置、不可比之處；連結全部可開啟；每個數字與原文相符（(v)）。§8「與本專案的比較」的每個陳述都對應到表中的來源或本專案的匯出結果 |
| AC-5 | ACCEPTANCE.md 覆蓋 Brief §3 全部必要項目、Spec 人工檢查表每一項、OV-1～OV-6（含 gate／best-effort 分類與 NOT TESTED 規則） | **PASS** | A-1～A-10（Brief §3.1 全部 T- 項目與主流解法）、B-1～B-6（§3.2 dashboard、四項採用的補充建議、三種標示）、C-1～C-16（Brief §4～§11 與 DA 義務）、D-1～D-22（Spec 人工檢查表 Dashboard 11 項含 Pages、報告 6 項、Repo 2 項、乾淨環境）、E OV-1～OV-6（OV-1／OV-6 硬性 gate；OV-2～OV-5 Required gate，OV-2～OV-4 的 best effort 與 NOT TESTED；量測紀錄表）；狀態規則「best-effort 沒有證據一律 NOT TESTED」；沒有任何 PASS／FAIL；D-12 為 NOT TESTED（pending merge）（AD-3）。引用的 13 個具名測試與全部測試檔都存在 |
| AC-6 | 報告 zh-TW、PDF 可建置；待填位置清楚標示，不含範例文字冒充 | **PASS** | zh-TW；PDF 25 頁（(ii)）；§10、§11、附錄 A 的 `<div class="pending">` 以【待填：作者提供的材料】標示，文字只說明將來的內容並寫明「沒有任何範例或代擬文字」；`--final` 在仍有待填時失敗（`tests/test_report.py:81-88`） |
| AC-7 | （TK-3）exp(ŷ_log) 為條件中位數的估計；CV winner 的 CV 分數有樂觀偏誤、test 為獨立估計 | **PASS** | §4.3「它估計的是**條件中位數**，不是條件平均」、§7.4；§6.2「會使 **CV winner 的 CV 分數帶有樂觀偏誤**，它不是不偏的估計；凍結選擇之後的 Test 評估才是獨立的估計」（mutant R2 被偵測） |
| AC-8 | （TK-2）報告引用的每張圖、每個表都對回結果目錄的 PNG／CSV | **PASS** | 8 張 `fig:` 圖＝`results/figures/` 的全部 8 個檔案（`tests/test_report.py:71-78`）；表取自 `results/tables/*.csv` 或 `results/model_data.json`（(iii)）。DA C-2 的 (b) 缺口已由修正補上並經我重做 F-5 核對（(iv)）；(a)(c) 依 DA F-2 不是缺口，§5.1、§5.2 以 CSV 注入的表呈現 |
| AC-9 | （I-2／TK-5）三種標示的依據是 Brief §3.2 與 Spec，不引用未接受的 OC v2 草稿 | **PASS** | 報告、README、ACCEPTANCE 沒有「OC v2」「S-08」「表 A」（`tests/test_report.py:135`；ACCEPTANCE:6、B-6 引用 Brief §3.2） |

## 3. DA 義務與裁決的核對

| 義務 | 判定 | 證據 |
| --- | --- | --- |
| G-4（報告的結果表分開訓練 CV 與 Test） | 符合 | 比較表的欄位「訓練 CV RMSE（USD）…」與「Test RMSE（USD）…」分欄；Ridge／Lasso 的 Test 指標只在比較表與緊接其後、標明「metric-only，只出現在比較表」的表中，不進區間表或預測圖 |
| D-2、D-3（共用模型的身分與評估數量） | 符合 | 比較表每個 winner 一列、以自己的身分呈現並寫明與哪些 winner 為同一模型；整體 winner 呈現為「Lasso 路徑排序 k = 17」；§6.1 的「2 個不同的 OLS 模型＋2 個 metric-only，共 4 個」由匯出結果計算（`hw2/report.py:286-291`）；預測圖面板標題同（(iv)） |
| N-4（不完整重跑；必要時部分執行） | 符合 | notebook 只新增 cell 46、47；cell 0–45 與 #64 cell 的完整 JSON 不變（(iv)）；正式產物與 `result_digest` 不變 |
| N-5（README 與報告的評估措辭） | 符合 | README:51「重現唯一一次的 Test 評估」、README:59 以 #63 run `fe76019b…`／`result_digest` `b53ff286…` 為唯一一次、`meta.test_evaluation` 只記錄產生目前檔案的那次執行、完整重跑是重現且須 bit-exact；報告 §6.1、附錄 B 同；建置綁定 `FORMAL_EVALUATION`（`hw2/report.py:66-71`、`:123-139`） |
| I-4、R-1.1、R-1.3、R-1.5（模型解釋與標準化讀法） | 符合 | §7.3〔依老師補充建議〕、permutation importance〔專案延伸〕；每單位讀法、one-hot 相對基準 `98001`、標準化讀法（OLS 原始尺度；Ridge／Lasso 的標準化只用於自己的擬合）；每 1 個 training sd 的 % 與 sd 只來自 `final_model_coefficients.csv`（(iii)）；報告沒有 Ridge／Lasso 係數（§5.2「係數也不匯出」；`tests/test_report.py:138-144`） |
| T-1（相對容差 1e-6） | 符合 | ACCEPTANCE A-3、C-11 引用相對容差與 DA 紀錄 |
| L-1～L-3（dashboard 的標示） | 符合 | 每一處**替 dashboard 標示**的地方都帶「課堂口頭」：對照表 `report/report.md:28`、標示說明 `:9`、§7.1 `:232`、§9 `:290`；README:9「課堂口頭要求的互動 dashboard」；ACCEPTANCE:6、B-1。沒有任何一處把它寫成作業頁或講義的書面要求（`grep` 報告、README、ACCEPTANCE 的「書面」「作業頁…要求」）。另見第 8 節第 3 點 |
| F-1～F-5（預測圖） | 符合 | 繪圖程式 `hw2/prediction_plot.py` 在條件 7(b) 的模組之外，輸入只有 `model_data`，Q43 編碼、全部 n_test、依 D-2 標示、英文標籤、`metadata={"Software": None}`、單元內只寫正式結果（`:138-155`）；notebook cell 46、47 在 cell 45 之後；§6.3 直接引用 PNG（`report/report.md:188-190`）、第九章截圖保留；ACCEPTANCE A-3 與 README 同步；`tests/test_prediction_plot.py` 涵蓋 F-4 第 6 點的 (i)(ii)(iii)；F-5 的四項條件我自行重做（(iv)） |
| S-1（學號設定不存在時） | NOT VERIFIED（實際值比對） | 見第 4 節 H-1；不是本票結案的條件 |

## 4. 高風險類別核對（A-1）

本票觸及 **H-2、H-4**（票文），依 DA `decision-20261019-issue65-labels-figures.md` §6 另觸及 **H-3**（預測圖只讀匯出結果），A-4（**H-1**）適用於全部票。

| 類別 | 核對內容 | 結果 |
| --- | --- | --- |
| H-1 | (a) 追蹤檔案：`git ls-files home_work_02` 中的 PDF 只有老師文件 `doc/requirement/50 Startups_ … Explorer.pdf`；`bc56c06..HEAD` 沒有新增 PDF、ZIP、`.env`、`kaggle.json`、`acceptor_materials/`、`.local/`、`dist/`；單元 `.gitignore` 排除 `*.pdf`、`*.zip`、`/.local/`、`/acceptor_materials/`、`/dist/`（`git check-ignore` 確認 `dist/report/hw2_report.pdf`、`.local/packaging.json` 被忽略）；`.local/` 不存在（未建立打包設定）。(b) **S-1 替代證據**（`a4check.py`，只輸出計數與分類，沒有印出任何數字串）：`bc56c06..HEAD` 新增的 2,660 行中「學號」39 次：11 次是 `<學號>`，28 次是敘述用詞，沒有一次後面 14 字內接 7 位以上數字；7 位以上的數字串全部歸類為 sha256／digest 片段、日期 `2026xxxx`、DOI `10.5220/…` 片段、ASSET 頁碼、Atlantis 文章編號，以及 notebook 中 PNG 輸出的 base64 內容（數字以 `#` 遮罩後檢視）；老師範例的學號樣式在新增行與 commit message 中 0 次；範圍內 8 個 commit message 的 7 位以上數字只有紀錄檔名中的日期。(c) **實際學號比對：NOT VERIFIED**（學號設定尚未提供；依 `decision-20261018-issue60-a4-student-id.md` S-1）。S-2～S-5 仍是 run record 的 open 項目；範圍內 commit 都沒有 push（S-3） | PASS（實際值比對 NOT VERIFIED） |
| H-2 | 報告六章名稱與順序（第二～七章）；「GPT 輔助內容」「NotebookLM 摘要」逐字是 §10、§11 的章節標題（`tests/test_report.py:123-124`）；資料集名稱與 Kaggle 連結（§1.1）；**附預測區間的預測圖**現在同時存在於主程式（notebook 5.5.1）與報告 §6.3 的 PNG，不再依賴 dashboard（DA F-1 的檢驗：拿掉 dashboard 後主程式與報告仍有預測圖——成立）；README 的流程與成果；dashboard：`index.html`、`assets/` 自 `003b825` 起沒有改動，`offline_scan` PASS，`file://` 開啟、零對外請求（(ii)）；notebook 六章標題與順序不變（(iv)） | PASS |
| H-3 | 正式產物、`result_digest`、manifest、凍結模組與 notebook cell 0–45 都不變；預測圖由追蹤的 `model_data` 決定性重產、位元相同；`prediction_plot.py` 不 import 資料、守門、建模或評估模組（`tests/test_prediction_plot.py:85-104` 通過；`is_formal` 只以 `export.result_digest` 雜湊匯出內容）；報告建置只讀匯出結果、拒絕非正式結果（mutant R1 被偵測）；`methods`／`baselines` 沒有 test 欄位，`test` 的 `ols_subset` 鍵＝授權清單 `allin`、`forward_sfs_k17`，`metric_only` 只有 `lasso`、`ridge` 且沒有 PI 欄位（A-3，自行檢查）；完整 pytest（含分組隔離、選擇邊界、逐筆獨立重算）與 Node 正式逐筆重算通過（A-2，(i)）；報告與 README 的數字獨立交叉核對 0 不符（(iii)）；選擇偏誤與 PI 假設的陳述在 Spec 允許的範圍內（§6.2、§6.3：不陳述二項近似偏差的方向或幅度、不宣稱保證 95%） | PASS |
| H-4 | 主流解法比較每項有來源，數字逐一與原文相符（(v)）；沒有 mock 數值或 wireframe 截圖（(vi)）；待填位置不冒充內容（AC-6）；ACCEPTANCE 沒有未驗證的 PASS（`tests/test_report.py:261-265`；mutant A1 被偵測）；dashboard 標示依 L-1～L-3 正確。**三種標示**：對照表與大部分章節標示正確，但第六、七章〔老師要求〕下有未註明出處的「補充」段引文，§6.2 的 Adjusted R² 沒有章節層級標示（**F-1**）；章節標示沒有回歸測試（**F-2**）；README:8 的措辭（**F-3**） | **FAIL**（F-1） |

## 5. Executor 的 concerns 與前票的 follow-up

- **C-1**（dashboard 的標示）：DA L-1、L-2 維持現況；我依 L-3 核對，符合（第 3 節）。
- **C-2**（缺少的結果圖）：DA F-1～F-5；(b) 已由 `0b57c02` 補上並經我重做 F-5（(iv)）；(a)(c) 依 F-2 不補做。
- **C-3**（Pages URL 404）：AD-3，ACCEPTANCE D-12 記 NOT TESTED（pending merge），合併後的 Lightweight work item。
- **C-4**（「指標 vs k」截圖沒有 k 刻度）：DA O-2 交 #67（D-1、D-4）；不在本票範圍。
- **C-5**（PDF 建置需要 Node 與 Chrome／Edge）：README:58 已寫明；我的建置使用同樣的工具鏈（(ii)）。
- **C-6**（部分執行時以 `%matplotlib inline` 啟用 PNG formatter）：見第 8 節第 1 點。
- **C-7**（DA O-1，cell 28 缺字）：見 **F-4**。
- **前票交給 #65 的事項**：#63 worklog C-2（alpha 在網格下緣）→ §5.2 列出網格、選出的 alpha 與位置，並由 `check_claims` 核對 CV 單調、`alpha_at_grid_edge`＝lower、不低於 All-in（`hw2/report.py:407-433`；我在 (iii) 另行核對）；#63 C-3（Test RMSE 高於 CV）→ §6.2 的差距與倍數由匯出值計算、TK-3 說明；#64 C-3（I-4）→ §7.3 標示；#64 C-4（五項診斷都偏離）→ §6.3、§6.4 揭露並連到區間，不宣稱保證。

## 6. Findings

### F-1 — 作業頁「補充」段的引文放在〔老師要求〕章節標題下，沒有註明出處；§6.2 的 Adjusted R² 沒有章節層級標示

- **Severity**：Medium。**Blocking**：**是**。觸及 H-4（A-7 適用：deferral 需要 DA 確認）。
- **證據**：
  - `report/report.md:160-162`：`## 6. Evaluation 〔老師要求〕` 之下直接是 `> {{quote:src2t:5. Evaluation: Compare MAE}}`，渲染為「5. Evaluation: Compare MAE, MSE, RMSE, R² and Adjusted R²; check the five regression assumptions.」（渲染後的 `hw2_report.md` 與 PDF 文字第 268–270 行：「6. Evaluation 老師要求」→ 該引文 → 「6.1 評估協定 專案延伸」）。
  - `report/report.md:228-230`：`## 7. Deployment 〔老師要求〕` 之下直接是 `> {{quote:src2t:6. Deployment: Predict new samples}}`，渲染為「6. Deployment: Predict new samples and explain the model.」（PDF 文字第 581–582 行）。
  - 這兩句都在老師需求轉寫的「補充」段（`doc/requirement/HW2-requirements-Multiple Linear regression_SRC-2_2026-10-18.txt:81` 的 `==== 補充 ====` 之後，第 145、146 行），不是作業頁正文（正文的 CRISP-DM 只有六個階段名稱，SRC-1 第 30–36 行）。引文產生器只回傳該行文字，不加出處（`hw2/report.py:633-641`）。
  - 報告自己的定義：〔老師要求〕＝「作業頁正文的書面要求」、〔依老師補充建議〕＝「作業頁『補充』段的建議」（`report/report.md:9-10`）；對照表把 Adjusted R²、五大回歸假設診斷、Deployment 的預測新樣本與模型解釋列為〔依老師補充建議〕（`:24-26`）。報告在其他地方引用補充段時都註明出處或放在〔依老師補充建議〕之下（`:52`「作業頁的「補充」段寫：」、`:120`「老師的補充段建議比較下列方法：」、`:136-138` §5.2）；而正文引文放在〔老師要求〕之下（§1.4、§6.3、§8、§10）。依報告自己建立的「標示＋其下引文＝該標示的出處」慣例，第六、七章把補充段的文字呈現為〔老師要求〕的出處，讀者會讀成老師以書面要求了 Adjusted R²、五大假設、預測新樣本與解釋模型。
  - §6.2（`report/report.md:170-182`）沒有章節層級標示，依附在〔老師要求〕的第六章之下，而它的內容包含 Adjusted R²（`:172`、`:182`，以及比較表的 Adjusted R² 欄），對照表把它列為〔依老師補充建議〕。
  - 現有測試只檢查 `##` 章標題有標示、對照表的列與「課堂口頭」這個字串存在（`tests/test_report.py:116-135`），所以這個問題沒有被發現（見 F-2）。
- **契約條款**：Ticket #65 AC「三種標示（老師要求／依老師補充建議／專案延伸）以對照表＋章節層級標示呈現……；補充建議不寫成老師要求」（依據依 DA I-2 讀為 Brief §3.2 與 Spec）；Brief §3.2「採用的補充建議 [S]：Adjusted R²、五大回歸假設診斷、Deployment 的模型解釋、Ridge／Lasso 對照……報告中標為『依老師補充建議』，**不寫成老師要求**」；Spec rev 5「報告與打包」「三種標示……以一張對照表置於報告前段，**章節層級再標示**」；DA `decision-20261018-high-risk-categories.md` H-4 的風險「三種標示（老師要求／依老師補充建議／專案延伸）混淆」。
- **為何 blocking**：違反的是 accepted contract 的明文條款（不是偏好），位置在評分直接依據的 PDF 報告（「文件說明 50%」），屬 DA 宣告的高風險類別 H-4；DA 把 H-4 列為高風險的理由正是「自動化測試只能檢查標示存在，無法檢查內容是否忠實」，這一項只能由 R1 抓到。對照表與子章節的標示雖然正確，但不能抵銷章節開頭的錯誤歸屬：同一份報告在同一位置給出相反的出處。
- **為何不是契約語義問題**：〔老師要求〕與〔依老師補充建議〕的定義在 Brief §2、§3.2 與報告自己的說明（`:9-10`）都明確，沒有需要 Design Authority 裁決的歧義；DA 的 C-1 裁決只涉及 dashboard 的標示，不涵蓋本項。
- **需要的修正**（targeted correction，Owner＝**#65 Executor**；只動 `report/report.md`，可附測試；不改結果、notebook、dashboard、`model_data`，不執行 notebook，不重新評估）：
  1. 第六、七章開頭的兩段補充段引文明確註明出處（例如引文前加「作業頁『補充』段對這一階段的建議（本專案採用的部分見 §6.4／§7.2、§7.3〔依老師補充建議〕）：」或等義的寫法），或把它們移到對應的〔依老師補充建議〕章節之下，使沒有任何補充段文字以〔老師要求〕的出處呈現。
  2. §6.2 中 Adjusted R² 的內容在章節或段落層級標示〔依老師補充建議〕。
  3. 重新建置報告，確認 `tests/test_report.py` 仍通過（新文字不得含手抄數字）、建置仍核對正式評估的 digest。
- **R2 的 closure 條件**：(a) 渲染後的報告中，第六、七章與其他任何〔老師要求〕章節開頭沒有未註明出處的補充段引文；(b) §6.2 的 Adjusted R² 帶〔依老師補充建議〕；(c) 其他標示、數字、圖與 `results/`、`assets/`、notebook 不變（`git diff 0b57c02..<修正>` 只有報告來源，以及選擇加入的測試）；(d) 完整 pytest 通過、報告可建置。F-2、F-3 的處理不是 R2 的 closure 條件。

### F-2 — 章節層級的標示與「課堂口頭」沒有回歸測試（mutation probes L1～L6 存活）

- **Severity**：Low。**Blocking**：否。觸及 H-4。
- **證據**（第 1 節 (vii)）：把 §6.4、§7.3、§5.2 的〔依老師補充建議〕改成〔老師要求〕（L1～L3）、刪除 §9、§7.1 標題中的「課堂口頭」（L4、L5）、把 §1.2 的「作業頁的「補充」段寫：」改成「作業頁正文另寫：」（L6），`tests/test_report.py` 全部仍通過。現有測試只檢查 `##` 章標題有任一種標示、對照表的五列，以及「課堂口頭」字串在全文出現一次（`tests/test_report.py:116-135`）。
- **契約條款**：Ticket #65 AC（三種標示，章節層級）；Spec「報告與打包」；DA H-4；DA L-1（dashboard 每一處標示都註明「課堂口頭」）。
- **風險判斷**：目前這幾處的標示本身正確（F-1 的兩處與 §6.2 除外）。缺的是 #66（會編輯報告的 AI 章節）與 #67 再改報告時，標示被改壞不會被發現；#67 的人工檢查表 B-6、D-14 是最後一道人工防線。因此判為 Low。
- **Disposition**：不延長 cycle。Owner＝**#65 Executor**，建議在 F-1 的修正中一併加入（同一檔案、同一 root cause）：例如斷言對照表列為〔依老師補充建議〕的項目（Adjusted R²、五大回歸假設診斷、Deployment 的預測新樣本與模型解釋、Ridge／Lasso 對照）所在章節帶該標示、§7.1 與 §9 的標題帶「課堂口頭」、每段 `quote:src2t` 引文都在〔依老師補充建議〕之下或前面有補充段的出處說明。若未在 #65 完成，轉交 **#66**（下一張修改報告的票）。這不是 F-1 的 R2 closure 條件。

### F-3 — README 把「比較特徵選擇方法」寫成作業要求

- **Severity**：Low。**Blocking**：否。觸及 H-4（標示的精確度）。
- **證據**：`README.md:8`「依作業要求比較特徵選擇方法：四種能對每個 k 給出子集的方法（Forward SFS、Backward SFS、RFE、Lasso 路徑排序，k = 1…18）與單一的 All-in baseline」。作業頁正文要求的是「必須執行特徵選擇」（SRC-1 第 28 行）；比較這些方法來自補充段（SRC-2T 第 147 行）與 acceptor 的 Grill 決定（Brief §5 [D Q11]）。報告自己的對照表把這一點分得較清楚（`report/report.md:17`「老師要求的特徵選擇；方法取自補充段建議清單的一部分」）。README 的其他標示（`:23-24` 的 Ridge／Lasso、Adjusted R²、五大假設〔依老師補充建議〕、`:9` 的課堂口頭）正確。
- **契約條款**：Brief §2（補充段是建議）、§3.2「不寫成老師要求」（該句明文針對報告；README 屬 Brief §8 的交付物）。
- **風險判斷**：只是一句目的說明的措辭，README 不承載三種標示的對照表，其他段落正確；判為 Low。
- **Disposition**：不延長 cycle。可以在 F-1 的修正中一併改寫（例如「依作業要求執行特徵選擇，比較……」），同一 root cause；否則 Owner＝**#67**（ACCEPTANCE A-8 的 README 人工檢查）。

### F-4 — Notebook cell 28（4.2 的 k 路徑內嵌圖）圖例缺字（DA O-1）

- **Severity**：Low。**Blocking**：否。**不是 #65 的變更造成**：cell 28 在 cell 0–45 的凍結範圍內，與 `052984b` 相同。
- **證據**：`hw2.ipynb` cell 28（執行序號 18，`import matplotlib.pyplot as plt`）的 stderr 輸出含「UserWarning: Glyph 36335 (\N{CJK UNIFIED IDEOGRAPH-8DEF}) missing from font(s) DejaVu Sans」等（「Lasso 路徑排序」的「路」「序」），即圖例中該方法的名稱顯示為缺字；cell 31 的 alpha 圖沒有這個警告。報告不使用這張內嵌圖（§5.1 以 CSV 注入表格）。
- **契約條款**：主程式是評分對象（SRC-1「結果合理、美觀且具有說服力（15%）」；Brief §3.1 T-CRISP-DM notebook 六章）。Brief／Spec 的「zh-TW 無缺字」明文只針對 dashboard（Spec US-60、Brief §7 BR-04、§10），所以對 notebook 沒有明確的 AC 被違反。
- **風險判斷**：只影響主程式一張內嵌圖的一個圖例標籤；判為 Low。
- **Disposition**：不延長 cycle。Owner＝**#67**（ACCEPTANCE A-4 的 notebook 人工檢查；N-3 的單一完整執行會重新產生 cell 28）。任何修正都會動到 cell 0–45 或它們依賴的設定（§9.3 條件 7(b)，經 DA F-4 第 2 點澄清），所以**修正前須先 route Design Authority**（DA O-1）。

## 7. Routing（需要其他 authority）

- **F-1**：不需要其他 authority；是 accepted contract 內的 targeted correction，由 Orchestrator 派回 #65 Executor，之後 R2。
- **F-4**：若 #67 決定修正，required authority＝**Design Authority**（修正會動到凍結的 cell 0–45；DA O-1）。
- **學號（A-4）**：依 S-1 記 NOT VERIFIED，不是本票結案的條件；S-2～S-5 仍 open（push 前、#67、Spec Integration Audit、phase acceptance、合併）。
- 沒有需要 Design Authority 裁決的契約歧義，也沒有 boundary 疑義。

## 8. 其他核對與備註（不是 finding）

1. **C-6（`display(Figure)` 在完整執行中的輸出）**：cell 47 以 `display(pred_fig)` 顯示 `matplotlib.figure.Figure`；完整執行時 PNG formatter 由 cell 28 的 `import matplotlib.pyplot` 在 inline backend 下啟用（部分執行時 Executor 以 `%matplotlib inline` 補上）。若 #67 的完整重跑沒有產生 `image/png`，`tests/test_prediction_plot.py:115-129` 會失敗，所以這一點在 #67 有自動化的防線。PNG 檔本身與顯示無關（決定性已核對）。
2. **Process note（以 shell 寫入 `report/report.md`）**：acceptor 2026-10-19 的同意記在 run record §15；被拒絕的原因是 harness 對 subagent 的檔名規則，不是 Bindings 的 boundary。三個檔案的內容我都逐行讀過（模板全文、README 全文、ACCEPTANCE 全文），內容的問題已列在 F-1～F-3；寫入方式本身不構成 finding。
3. **L-3 的字面讀法**：§5.1（`report/report.md:126`）、§6.3（`:188`）、§7.2（`:238`）有幾處只是描述性地提到 dashboard（「dashboard 顯示」「互動版本見第九章的 dashboard」「dashboard 不讀取 pickle」），沒有逐處加「課堂口頭」。DA L-1 的對象是「對 dashboard 的標示」，DA 在 `741a21b`（已含這些描述性提及）上判定維持現況、不需修改；這些提及都沒有把 dashboard 寫成書面要求，所以符合 L-1～L-3。
4. **範圍外的觀察（供 #67）**：dashboard Test 區塊的 log 軸刻度在截圖中顯示為「1.00e+3 萬」等格式（`shots/test.png`），與 C-4 的 k 刻度一起屬 #67 的 D-2、D-4、OV-6 (c) 人工檢查；不在本票範圍，dashboard 自 `003b825` 起沒有改動。
5. **Worklog 的主張**：§3.1 的產物清單、§3.3 的來源數字、§4 V-1～V-6、§9.1 部分執行的結果、§9.2 F-5 的證據、§9.3 VC-1～VC-3、VC-5、VC-6 都已由我重做或以獨立方式核對。V-7／VC-4 的 mutation probes 沒有逐一重做，改以我自己的 12 個 mutant 取代（不同的變異點；結果見 (vii) 與 F-2）。
6. **範圍與 git**：沒有單元目錄以外的變更，沒有修改 `doc/requirement/`（RB-5）；`requirements.txt`、`.gitignore`、`assets/`、`index.html` 沒有變更；範圍內兩個 implementation commit 的訊息依 `docs/conventions/git-commit-rules.md`（`[Modify] –` 開頭、`[Additions]`／`[Modification]` 分類），沒有 Claude 標記；未 push、rebase、merge 或 force push。
7. **Reviewer 的 test 隔離**：我沒有執行 notebook、沒有開啟任何守門，也沒有讀取或評估任何 test 列；報告建置與預測圖重產只讀已匯出的結果；mutation probes 只在 scratchpad 複本上執行。

## 9. 結論

- Blocking findings：**F-1**（Medium；第六、七章〔老師要求〕下的補充段引文未註明出處，§6.2 的 Adjusted R² 沒有章節標示）。Owner＝#65 Executor，targeted correction 後 R2。
- Non-blocking findings：F-2（Low，owner #65，未完成則 #66）、F-3（Low，可併入 F-1 修正，否則 #67）、F-4（Low，owner #67；修正前須 route Design Authority）。
- 其餘 AC（AC-1、AC-2、AC-4～AC-9）PASS；DA 義務（G-4、D-2／D-3、N-4、N-5、I-4、R-1.x、T-1、L-1～L-3、F-1～F-5）符合；正式 Test 評估沒有被再執行，`model_data` 與 `result_digest` `b53ff286…` 不變，新預測圖可由匯出結果決定性重產。
- A-4 學號：NOT VERIFIED（S-1），不是本票結案的條件。

VERDICT: BLOCKING (F-1)
