# Audit record — Issue #64，cycle 1，R1

| 欄位 | 內容 |
| --- | --- |
| Work Contract | GitHub issue #64「HW2 T5 五大假設診斷、模型解釋與 Deployment（predict_price、pickle）」（OPEN，`ready-for-agent`；含 TR-02 的重複交易文字、DA TK-2、I-1／TK-5 的 AC；高風險 H-2、H-3、H-4）；Parent Spec `home_work_02/doc/spec/SPEC.md` rev 5（#59）；DA derivation `doc/governance/decisions/derivation-SPEC.md` §9.1（#64：B-6、B-7）、§9.2、§9.3（條件 1–6）、§9.4 I-1、I-2、§9.5 TK-2、TK-5、§9.6 TR-01、TR-02；高風險 `decisions/decision-20261018-high-risk-categories.md`（A-1～A-8）；`decisions/decision-20261018-issue60-a4-student-id.md`（S-1～S-6；§2.2 #64 加標 H-2）；`decisions/decision-20261018-issue62-shared-subset-test-key.md`（D-2）；`decisions/decision-20261018-issue63-js-tolerance.md`（T-1）；`decisions/decision-20261018-issue64-notebook-rerun.md`（N-1～N-6、條件 7、8、I-4；N-2 規定本 R1 對兩次執行的 notebook 的處理）；Outcome Contract `doc/governance/outcome-contract.md`（Brief @ `dff7c55c`＋CC-1、AD-1～AD-3）；Implementation 授權：`doc/governance/run/run-20261018-hw2-formal.md` §1 designation 第 2 點；前票 follow-up：`audit/issue-63-c1-r1.md` F-1、F-2（owner＝#64） |
| 受審 subject | branch `home_work_02-regrill`，implementation commit **`003b825426a500fa2d11ebea584d48c93cd4635d`**；BASE＝`b34cc50`。範圍 `b34cc50..003b825`：31 個檔案，全部在 `home_work_02/` 內，沒有 `doc/requirement/`（`git diff --name-only b34cc50 HEAD`）。審查時 HEAD＝`443f19e`；`003b825..HEAD` 只改 `doc/governance/worklog/issue-64.md`、`doc/governance/run/run-20261018-hw2-formal.md`、`doc/governance/decisions/decision-20261018-issue64-notebook-rerun.md`（record-only，Bindings §7）。`git diff --quiet 003b825 -- home_work_02` 成立；`git status --short home_work_02` 審查前後皆為空。`origin/home_work_02-regrill`＝`60d7fa67`：範圍內 commit 都沒有 push |
| Audit 種類 | **R1**（full independent audit of accepted work scope），**cycle 1**。**本 record 不是 Spec Integration Audit**（本 Spec 有多張票，不適用單 Ticket fast path；derivation §9.1、run record §4） |
| 角色 | `primary_reviewer`（definition `gov-primary-reviewer`；Bindings §3.1 R-PR mapping `claude-opus-5-5`／`xhigh`） |
| Assurance (a)：context independence（治理 §2.3；Bindings §3.7） | (1) **Independent context**：Orchestrator 以 Agent tool 派 `gov-primary-reviewer`（非 fork），從空白 context 開始；派工內容只有路徑與識別（Ticket、Spec、DA 紀錄、OC、Brief、CONTEXT、worklog、前票 audit record、branch／SHA）。派工訊息中「之後的 commit 只動 `doc/governance/**`」，以及 worklog、run record、DA 紀錄中 Executor 的敘述與數字，都只當作待驗證主張，已自行核對。(2) **Verifiable binding**：見 (b) 欄。(3) **Autonomous access**：自行讀取 `gh issue view 64`、Spec、DA 紀錄、OC、Brief、老師需求轉寫、wireframe 設計文件、git 歷史與 diff、全部新模組、notebook 與測試；自行執行完整 pytest 與 Node test、不 import `hw2` 的獨立重算、`predict_price()`／pickle 對照、training 端的重現、mutation probes（在 `git archive 003b825` 的 scratchpad 複本上）、以 CDP 驅動的 `file://` 瀏覽器檢查；「沒有再評估」另以 Executor subagent transcript 中的 tool-call 文字做機械比對（不讀其推理）並讀其部分執行腳本與 log（產物）（第 1 節 (vi)）。(4) **Self-written record**：本檔由 Reviewer 以自己的 Write 工具寫入 |
| Assurance (b)：model diversity（Bindings §5） | **Executor**：agentId `a2b1c8f4cc400f3be`，`agentType` `gov-executor`，觀測 `('claude-opus-5-5', 'high')` 220 則、單一元素（Reviewer 以 Bindings §3.6 的同一邏輯自行掃描 session `4bbff425-7ff9-4cdc-b64c-cc68e824e1b1` 的 subagent transcript），符合 O-1。（#64 的 DA：agentId `a01ab70cca718e6e7`，`gov-design-authority`，`('claude-opus-5-5', 'high')` 59 則、單一元素。）**本 review**：agentId `a7abd78613bbbdc1d`，`agentType` `gov-primary-reviewer`，撰寫本 record 前觀測 `('claude-opus-5-5', 'xhigh')` 154 則、單一元素；全程核對由派工者依 Bindings §3.6 在採用本 record 前執行。**無 model diversity**（兩者同為 `claude-opus-5-5`）。Bindings §5 不宣告 diversity 關係，不記 `diversity_lost`（A-8） |
| 日期 | 2026-10-18 |

## 1. 審查方法與環境

Reviewer 的腳本與輸出都在 session scratchpad 的 `r1-64/`（不在 repo）。環境：單元 `.venv`（Python 3.11）、Node v24.19.0、Chrome 155.0.8059.80、Edge 155.0.4283.62（headless）。

**不重新評估**：依 CC-1 第 3 點、derivation §9.3、DA #64 裁決與派工限制，我沒有執行 `hw2.run_notebook`、沒有開啟任何守門，也沒有對 test 列評估任何模型。我自己的腳本讀 CSV 時在解析階段就跳過 `split_assignment.csv` 的 4,323 個 test 位置；需要 import `hw2` 的兩個腳本（pickle 對照、重現）在任何 `hw2` 程式執行前先把 `OFFICIAL_TEST_GATE_ENABLED` 設為 `False`，結束時確認 `_official_test_rows_loaded` 為 `False`。

- **(i) 工作樹測試**：`python -m pytest -q -rs -p no:cacheprovider` → **314 passed, 1 skipped**（skip：`tests/test_repo_hygiene.py:71`，學號設定未提供），45.9 s。`node --test tests/js/core.test.js` → 9 pass、0 fail、3 skip（fixture 項目，由 pytest 的 `test_node_core.py` 執行）。`python -m hw2.offline_scan` → `scanned 6 files: PASS (0 findings)`。執行後工作樹沒有變化。
- **(ii) 獨立重算：training-only**（`indep64.py`，不 import `hw2`；只解析 17,290 筆 training 列）：
  - `model_data` 的 result digest（`test_inputs`＋`test` 的 sorted-key JSON）＝`b53ff286…c3cfc6`；manifest `run_id` `fe76019b…`、`selection_digest` `44f7723e…4b28`、`code_revision` `d413e58`（`package_modified: false`），都等於 #63 的紀錄。
  - 最終模型：整體 CV winner＝`lasso_path_k17`（`test_model_key` `forward_sfs_k17`；同一擬合模型的其他 winner 為 Forward SFS、Backward SFS k=17）。依 Spec 文字自寫 encoding（基準日 2014-01-01、整修旗標與有效年份、zipcode one-hot 以 `fit.zipcode_categories` 判定），以欄位單位化的 QR 自行擬合：係數與匯出 `fit` 最大相對差 7.0e-10，s² 相對差 8.3e-16，rank 87、df 17,203；以 QR 算的槓桿值與以匯出 (XᵀX)⁻¹ 算的最大絕對差 3.5e-12。
  - **五大假設**：`diagnostics_summary.csv` 的 17 個統計量全部與我的計算相符（最大相對差 9.6e-13）：RESET F 166.416（df 2、17,201，p 2.6e-72；我用與標準化 z²、z³ 相同的欄空間）；20 個等量分箱的最大平均殘差 0.0366；依交易日期（平手依 CSV 列）的 Durbin–Watson 1.9664；training 重複交易 141＝17,290 − 17,149，涉及 140 棟（281 列），相鄰交易 141 對、殘差相關 r＝0.3353（p 4.8e-5），平均變化 +0.355；全資料背景 177（21,613 − 21,436）；Breusch–Pagan（Koenker）n·R² 1297.84、df 86、p 1.5e-215，只對擬合值 4.004、df 1、p 0.045；Jarque–Bera 以我自己的母體動差公式 6897.78、偏態 −0.4037、超額峰態 2.9871；|studentized| > 1.96 為 5.76%、> 2.576 為 2.30%；相關矩陣條件數 47.137；含截距單位長度設計矩陣條件數 27,785。GVIF 以行列式公式重算，與 `diagnostics_vif_by_group.csv` 最大相對差 1.5e-15；欄位 VIF 以輔助回歸直接重算（lat 64.43、yr_built 38.30、long 33.85、sqft_living 8.83、yr_renovated_effective 37.52、zipcode_98039 1.99）與 `diagnostics_vif_by_column.csv` 相同。
  - **係數表**：`final_model_coefficients.csv` 的係數以 round-trip 解析後與匯出 `fit` 位元相同；標準誤 √(s²·[(XᵀX)⁻¹]ⱼⱼ) 最大相對差 2.7e-13、每單位百分比 2.6e-15、95% 區間端點 8.6e-15、training 標準差與每 1 SD 百分比 1.4e-13；69 個 one-hot 標「相對基準 zipcode 98001」、標準差欄為空。
  - **Permutation importance**：依模組說明的規則自行重做（`SeedSequence([seed, 2])`、每個 group 的全部欄位以同一個列排列一起打亂、10 次、依 canonical group 順序）：排名完全相同，平均增加最大相對差 5.5e-14、標準差 3.6e-13；未打亂的 in-sample log RMSE 0.18258。
- **(iii) `predict_price()` 與 pickle**（`pickle64.py`；import `hw2` 只為了反序列化）：追蹤的 `results/deployment/final_model.pkl` 是 `lasso_path_k17`、標籤「Lasso 路徑排序 · k = 17」、`test_model_key` `forward_sfs_k17`、`shared_with`＝Forward SFS、Backward SFS k=17、`n_train` 17,290；其 `fit` 的 coef、(XᵀX)⁻¹、s²、t、欄名、zipcode 類別與匯出 `fit` 完全相同；`input_ranges` 等於 `model_data.inputs`（training）；物件只含模型參數與 training 範圍（前處理器只有 groups、類別、基準、欄位與對應），沒有任何資料列。以我自己的 encoding 從**匯出的 `fit`** 直接計算，對 4 筆人工構造的列（ISO 與 CSV 日期、整修與未整修、已見與未見 zipcode、低於 training 範圍的值）與**全部 17,290 筆 training 列**：點預測、lower、upper 的最大相對差都是 **0**。未見 zipcode 只標在 `12345` 那一列；低於範圍的列標出 date、sqft_living、sqft_lot、sqft_above、yr_built、lat、long、sqft_living15；training 列沒有任何標示。
- **(iv) 重現（DA N-2；worklog V-9 的主張）**（`repro64.py`）：全新 process，守門旗標先設為 `False`，只走 training 端（`data.load_and_split` → `fit_allin` → `run_path_methods` → `determine_winners` → `run_metric_only`）：selection digest＝`44f7723e…4b28`（＝#63 pre-gate 值）；再以 `final_model` → `diagnostics` → `explain` 把產物寫到 scratchpad：**13／13 個檔案（7 張 PNG、5 個 CSV、pickle）與追蹤的檔案位元相同**；正式 test 列未載入。
- **(v) Notebook**：`b34cc50` 有 47 個 cell、`003b825` 有 71 個；cell 0–45 與 `b34cc50` 的 JSON 完全相同（含輸出），notebook metadata 相同；cell 46（原佔位）被 5.6 取代；執行序號 `1…28, 25…35`；`nbformat.validate` 通過；11 個新 code cell 都有輸出、沒有錯誤；印出的數字與 (ii)(iii) 相符；cell 41 的輸出仍是 `fe76019b…` 與 `44f7723e…`。六章標題 `## 1. Business Understanding`…`## 6. Deployment` 與 `b34cc50` 相同。新 cell 的輸出、7 張 PNG 與 pickle 都不含本機路徑或使用者名稱。
- **(vi) 「沒有再評估」的證據**：
  - Git：`052984b`→`003b825` 之間 `results/model_data.json`、`assets/model_data.js`、`results/split/split_assignment.csv`、`comparison.csv`、`alpha_cv.csv`、`cv_by_method_k.csv` 與 `hw2/` 的 `testgate`、`export`、`selection`、`models`、`comparison`、`data`、`preprocess`、`ols`、`metrics`、`contract`、`split`、`run_notebook`，以及 `requirements.txt` 的 blob 全部相同；`hw2/` 的差異只有新增 `deployment.py`、`diagnostics.py`、`explain.py` 與 `__init__.py`、`paths.py` 的說明與路徑常數。
  - Executor transcript（`agent-a2b1c8f4cc400f3be.jsonl` 的 130 個 tool call，只機械比對指令與寫入內容的文字）：沒有任何 `hw2.run_notebook`、`gate.open(`、`.evaluate(` 的執行；命中樣式的 10 個 tool call 是：讀檔或 grep、測試程式碼與 worklog 的文字、mutation 腳本，以及第一個動作就是把 `OFFICIAL_TEST_GATE_ENABLED` 設為 `False` 的 scratchpad 腳本（`state.py`、`run_partial.py`）與對它們的 `sed` 修改。
  - 部分執行的產物 `ex64/run_partial.py` 與 `run_partial.log`：kernel 的前置 cell 先把旗標設為 `False`；略過 cell 41、42、44、45；結束時「official test rows loaded in this kernel: False」、kernel 中沒有 `gate`／`evaluation`／`model_data` 名稱、selection digest＝`44f7723e…`。
- **(vii) Mutation probes（verify-the-verification）**：`git -c core.autocrlf=false archive 003b825 home_work_02` 解到 scratchpad，每個 mutant 只改一處、跑相關測試檔、還原（`mutants_r1_64.py`、`mutants2.py`）。基準 91 passed。**28 個 mutant，25 個被偵測**：D1 `training_rows` 不檢查 test 列、D3 最終模型改成 Forward 的身分（D-2）、D5 ISO 日期晚一天、D6 pickle 載入任意物件、D7 非正式 pickle 可寫入單元、G1 training 重複交易改用全資料數字（TR-02）、G2 BP df 少減 1、G3 RESET 只加 z²、G4 GVIF 少乘其餘行列式、G5 JB 用 studentized 殘差、G6 違反寫成「失敗」、G7 DW 依 CSV 列序、G8 studentized 不含槓桿、E2 permutation 依 USD 排序、E3 每 SD 讀法用 ddof=1、E4 標準誤少乘 s²、H1 係數表預設展開、H2 協定段標成「老師要求」、H3 係數表讀 `MD.test`、H4 PI 段刪除「不宣稱保證 95%」、H5 限制段刪除「不是因果效果」、N1 5.6 的 code cell 讀 `model_data`、F1a alpha 平手取較小者、F1b 契約不檢查 argmin、F2 移除 `pytest_configure` 的關閉。**存活 3 個**：D2、D4、E1，見 **F-1**。
- **(viii) Dashboard（`file://`，CDP，`cdp64.js`）**：Chrome 與 Edge headless 各一次，`--host-resolver-rules="MAP * ~NOTFOUND"`、scratchpad 內的全新 profile，直接開啟 repo 工作樹的 `home_work_02/index.html`。請求只有 6 個本機檔（`index.html`、`style.css`、`chart.umd.js`、`model_data.js`、`hw2core.js`、`app.js`）加上瀏覽器自己的 `data:image/svg+xml`；沒有例外、console error 或任何非 `file:` 請求。1440／768／375 px 下 9 種狀態（初始、鍵盤 Enter 展開、Lasso 路徑排序 winner、Lasso k=3、Forward winner、RFE winner、比較全部、All-in、鍵盤 Space 收合）的頁面水平溢出都是 **0**。係數表：初始收合（沒有 `open`），在 `<summary>` 上 Enter 展開、Space 收合；列數隨所選模型（All-in 88、k=17 87、k=3 4，＝係數數）；caption「來源：所選模型的 fit（全訓練集擬合），不含任何 Test 資料。」；摘要「係數表（選配） 全訓練集擬合，R²／Adjusted R² 為 log 尺度」；375 px 時表格在自己的容器內捲動（348 px），頁面不溢出。方法與限制：4 段，各有一個標示（特徵選擇方法〔老師要求〕、訓練 CV／Test 協定〔專案延伸〕、預測區間的統計假設〔老師要求〕、限制與非因果解讀〔依老師補充建議〕）、三種標示的圖例、適用範圍由 `MD.inputs.date_range` 填入「2014-05-02 至 2015-05-27」、導覽有 `#methods` 連結；1440 px 兩欄、≤768 px 一欄。
- **(ix) A-4 掃描**：見第 3 節 H-1。

## 2. Acceptance criteria 逐條判定

| # | AC（#64） | 判定 | 證據 |
| --- | --- | --- | --- |
| AC-1 | Spec rev 5「診斷與解釋」全部條款；古典回歸假設與參數式 PI 的假設分開陳述，不暗示診斷證明了區間保證（SR-08／SR-12） | **PASS** | 五大假設都用最終模型的 training 殘差（log 尺度）：線性＝殘差 vs 擬合值＋RESET；獨立＝依日期的殘差序列＋DW＋重複交易討論（TR-02：training 141 筆由程式計算；177 只作背景並標「全資料層級」）；同質變異＝尺度—位置圖＋Koenker BP；常態＝Q–Q 圖＋JB；多重共線性＝group 內 VIF 與 group 間 GVIF、欄位 VIF、條件數。每項有圖或數值與解讀，違反一律「揭露，不判失敗」（`summary_table`；G6 被偵測）。模型解釋：log 尺度百分比讀法（含 one-hot 相對基準）、只用 training 的 permutation importance（10 次、log RMSE 指標，寫入 6.2 與模組說明）、6.5 使用限制、6.2 末段與 dashboard 的非因果提醒。5.6 末段「古典回歸假設與預測區間的假設分開陳述……既不能證明、也不能否定預測區間的 95% 涵蓋，不宣稱保證 95% 的經驗涵蓋率」；6.5 與 dashboard PI 段同義；沒有陳述二項近似偏差的方向或幅度（SR-12）。數值見第 1 節 (ii)。「標準化的讀法」見第 7 節 R-1 |
| AC-2 | 診斷與 permutation importance 的輸入只來自 training set | **PASS** | `diagnostics.run`、`explain.coefficient_table`、`explain.permutation_importance` 只接收資料階段的 `PreparedData`（只有 training 列與 test 識別），並經 `deployment.training_rows` 拒絕含 test 位置的列（D1 被偵測）；`test_changing_the_test_rows_changes_no_diagnostic_or_explanation`（改動全部 test 列的價格、7 個特徵、zipcode 與日期，全部數字不變）；`test_the_diagnostics_and_deployment_cells_use_training_objects_only`（N1 被偵測）；我的 (ii) 只解析 training 列就重現了全部官方數字 |
| AC-3 | `predict_price()` 對人工構造的列與 training 的列回傳點預測與區間，等於以 `fit` 直接計算的值；示範不使用 test 列 | **PASS** | `tests/test_deployment.py:58-79` 以自寫 encoding 從 `fit` 直接計算（不呼叫 `hw2` 前處理或預測），人工列與 training 列 rtol 1e-12（D5 被偵測）；我的 (iii) 在正式 pickle 上對 4 筆人工列與全部 17,290 筆 training 列相對差 0；notebook 6.3 的示範只用兩筆人工列與 `train.head(2)`，並以 `fit` 核對 |
| AC-4 | Pickle 示範可載入並重現同一筆預測；不納入 dashboard 契約 | **PASS** | `test_pickle_round_trip_reproduces_the_prediction`、`test_the_tracked_pickle_is_the_official_final_model`；notebook 6.4（`assert_frame_equal`）；(iii) 載入追蹤的 pickle 重現預測；`model_data` 的 blob 未變，`index.html`／`app.js`／`hw2core.js` 沒有任何 `pkl`／`pickle`／`final_model` 字樣；非正式 pickle 不得寫入單元（D7 被偵測） |
| AC-5 | Notebook Evaluation／Deployment 章節內容對應 Spec 清單；dashboard 方法與限制區四段文字與三種標示；係數表預設收合（UI 決策 5） | **PASS** | Notebook 5.6（最終模型＋5.6.1～5.6.5）、第 6 章 6.1 dashboard、6.2 模型解釋、6.3 `predict_price()`、6.4 pickle、6.5 使用限制，對應 Spec「診斷與解釋」與 Brief §8 的 Deployment 內容；dashboard 四段與三種標示、係數表收合與標示見第 1 節 (viii)；`test_dashboard_static.py` 的兩個新測試（H1～H5 被偵測） |
| AC-6 | 報告草稿的解釋段落標「依老師補充建議」與「專案延伸」（permutation importance 的用法） | **PASS**（依 DA I-4：notebook 6.2）；報告版屬 #65 | Notebook 6.2「**標示：依老師補充建議**（Deployment 的模型解釋）」與「**Permutation importance — 標示：專案延伸**」；I-2 的 ID 改讀為 Brief §3.2 與 Spec 的三種標示表 |
| AC-7 | （DA TK-2）診斷圖與解釋圖的 PNG 至結果目錄 | **PASS** | `results/figures/` 7 張 PNG（5 張診斷、2 張解釋），`.gitattributes` 標為 binary；(iv) 由 training 端重現位元相同；我看過其中兩張（獨立性、係數），標題、軸與數字與表一致 |
| AC-8 | （DA I-1／TK-5）「Fit」一律指 training set；標示依據為 Brief §3.2 與 Spec 的三種標示表（不引用未接受的 OC v2 草稿） | **PASS** | 模組、notebook、dashboard 都寫「training set」「全訓練集擬合」；`git diff b34cc50 003b825` 中沒有 `S-08`、`OC v2`、`2.4.6` 字樣 |

## 3. 高風險類別核對（A-1）

| 類別 | 核對內容 | 結果 |
| --- | --- | --- |
| **H-2**（`decision-20261018-issue60-a4-student-id.md` §2.2 的必核項） | notebook 六章標題的名稱與順序與 BASE `b34cc50` 完全相同；`python -m hw2.offline_scan` PASS（6 個檔、0 findings），CDP 實測只請求 6 個本機檔，沒有新增任何對外資源（新區塊不含任何 URL，`test_methods_and_limitations…` 也斷言區塊內沒有 `http`）；`file://` 在 Chrome 與 Edge 都正常載入、沒有例外；`home_work_02/index.html` 路徑不變；必要區塊 (9)「方法與限制」現在存在並渲染；README 只在檔案配置表加列，安裝與執行步驟與數字都沒有改變 | PASS |
| **H-3** | A-2：自行執行完整 pytest 與 Node；training-only 的獨立重算（最終模型、五大假設、係數表、permutation importance）全部相符；`predict_price()` 對匯出 `fit` 的獨立計算相對差 0；training 端重現 13／13 位元相同；README 沒有數字、報告尚未建立。A-3：`model_data` 的 blob 與 #63 相同（`methods`／`baselines` 無 test 欄位、`test` 鍵集合不變，已由 #63 R1 核對）；新的 dashboard 程式（`renderCoef`、`renderMethods`）只讀 `entry.fit` 與 `MD.inputs`，不讀 `MD.test` 或 `test_inputs`（H3 被偵測）。**沒有再評估**：第 1 節 (vi)。§9.3 條件 3：選擇、alpha、前處理、模型集合的程式自 `052984b` 未變；條件 4：追蹤的 #64 產物由正式資料重現（不是 fixture），fixture 產物被拒絕寫入單元（D7、`test_non_official_outputs_never_reach_the_unit`）；條件 6：沒有載入正式 test 列。D-2：最終模型以「Lasso 路徑排序 · k = 17」的身分呈現，列出 Forward、Backward 為同一擬合模型，Test 鍵只作引用（D3 被偵測） | PASS（另見 F-1，Low） |
| **H-4** | 三種標示：notebook 6.2 依 I-4 標示；dashboard 四段的標示與 Brief §3 的來源標記一致（特徵選擇是 [T]「必做特徵選擇」、PI 是 [T]「預測圖加上信賴區間或預測區間」、五大假設與模型解釋是 §3.2 採用的 [S]、分組 CV／一次性 Test 協定是 [D] 的設計並在段內寫明「模型評估是老師的要求；下面的評估協定是本專案的設計」）；沒有把 dashboard 寫成老師的書面要求。非因果：6.2 末段、6.5、dashboard 限制段與係數表讀法。不宣稱保證 95%：5.6、6.5、dashboard PI 段（H4 被偵測）。A-5：dashboard 新內容沒有數字（日期範圍由 `MD.inputs` 填入），README 沒有數字，沒有 wireframe 的 mock 數值或截圖；worklog 沒有把任何 OV 項目標為 PASS | PASS |
| **H-1**（A-4，全部票；`decision-20261018-issue60-a4-student-id.md` S-1） | 追蹤檔中的 PDF 只有老師文件（`doc/requirement/50 Startups_…Explorer.pdf`）；沒有 `.zip`、`.env`、`kaggle`、`.local/`、`acceptor_materials/`、`dist/`；`home_work_02/.local/` 不存在。範圍 `b34cc50..HEAD` 新增的 4,052 行（二進位檔除外）中「學號」出現在 8 行（DA #64 紀錄 4 行、worklog 4 行），其中 4 次是 `<學號>` 佔位，其餘是敘述用詞，「學號」後 12 個字元內沒有 7 位以上數字；新增行中 7 位以上的數字串全部歸類：日期 32、sha／hex 片段 4、PNG base64 20、小數位數 880，**未歸類 0**；3 個 commit message 中只有一個 7 位以上數字串，是日期 `20261018`；沒有 Claude 標記。過程中沒有印出任何疑似值。**實際學號比對 NOT VERIFIED**（學號設定尚未提供；依 `decision-20261018-issue60-a4-student-id.md` S-1）。範圍內 commit 都未 push（S-3 適用） | 替代證據滿足結案條件；實際值比對 NOT VERIFIED（S-1） |
| A-7 | 本票沒有 blocking finding；若之後 H-2～H-4 的 finding 被 defer，須有 DA 確認 | — |
| A-8 | 見表頭 (b) 欄 | — |

## 4. 前票 follow-up（`audit/issue-63-c1-r1.md`，owner＝#64）

| 來源 | 處理 | 判定 |
| --- | --- | --- |
| #63 R1 F-1 (1)：平手測試沒有呼叫被測程式 | `tests/test_comparison.py` 新的 `test_select_alpha_breaks_a_real_tie_toward_the_larger_alpha`：monkeypatch `_fit_coefs` 讓每個 alpha 得到相同擬合，先斷言曲線真的平手，再由 `select_alpha` 本身選出最大 alpha（Ridge、Lasso 各一次）；原本自行計算平手的部分已移除。我的 F1a（`hw2/comparison.py:222` 改為平手取較小 alpha）被偵測 | **resolved** |
| #63 R1 F-1 (2)：沒有只違反 argmin 的竄改 | `test_an_alpha_that_is_not_the_cv_argmin_is_rejected`：以 `dataclasses.replace(sel, alpha=內部點)` 產生 `cv` 與邊界旗標都一致、只有 argmin 不成立的 entry，並斷言錯誤訊息是 argmin 那一條。我的 F1b（`hw2/contract.py:458` 改為 `if False:`）被偵測 | **resolved** |
| #63 R1 F-2：conftest 不涵蓋 session／module 範圍的 fixture | `tests/conftest.py` 加 `pytest_configure`，在任何 fixture 之前關閉正式守門；function 範圍的還原保留；docstring 改為實際的保證；`test_testgate.py` 新增以 session 與 module fixture 讀取旗標的測試（兩者都是 `False`）。我的 F2（`pytest_configure` 不再關閉）被偵測 | **resolved** |

## 5. DA 裁決與 Executor 的 concerns

- **DA `decision-20261018-issue64-notebook-rerun.md`**：依 N-2，我沒有因 notebook 混合兩次執行或執行序號重複而開 finding。N-2 要求的三項自行核對都已完成：cell 0–45 與 `b34cc50` 相同（第 1 節 (v)）、`model_data` 與 result digest 未變（(ii)、(vi)）、#64 的新輸出與產物可以重現（(iv)：13／13 位元相同，selection digest 等於 `44f7723e…`）。I-4：AC-6 依 notebook 6.2 判定。
- **C-1**：由上述 DA 紀錄結案。
- **C-2（「方法與限制」四段的標示分配）**：我核對了老師原文（SRC-2T：正文「必須執行 特徵選擇 與 模型評估」「預測圖(加上信賴區間或預測區間)」；補充段的 Train/test split、五大假設、Deployment 的解釋）與 Brief §3 的來源標記。Executor 的分配與 Brief §3.1／§3.2 一致；分組 CV／一次性 Test 協定在 Brief 中是 [D]（Q4、Q33、Q20）而不是 §3.2 採用的 [S]，標「專案延伸」並在段內寫明模型評估本身是老師要求，沒有把延伸寫成要求。Wireframe 把特徵選擇段標成「依老師補充建議」，但 wireframe 只是 UI 參考，與 Brief／Spec 衝突時以 Brief／Spec 為準（derivation B-13）。限制段（標「依老師補充建議」）的首句寫明是五大假設與模型解釋的補充建議，其餘是解釋的使用限制。**不是 finding**。
- **C-3**：依 I-4 結案。
- **C-4**：五項診斷都偵測到偏離，依規則揭露；報告的連結屬 #65。不是 finding。

## 6. Findings

### F-1 — 新模組的三項行為沒有被測試守住（mutation probes D2、D4、E1 存活）

- **Severity**：Low。**Blocking**：否。觸及 H-3（D-2 身分、只用於解釋的 permutation importance），A-7 適用。
- **證據**（第 1 節 (vii)，每個 mutant 只改一處、跑相關測試檔）：
  - **D2**：`hw2/deployment.py:127` 的超出範圍判斷改為只看上界（`outside = (values > info["max"])`）→ `tests/test_deployment.py` 10 passed。`constructed_rows`（`:85-94`）只構造了高於範圍的列；低於 training 下界的外推不會被標示，而測試不會發現。
  - **D4**：`hw2/deployment.py:205` 的 All-in 共用判斷改為 `if False:` → 10 passed。`test_final_model_is_the_overall_cv_winner_refitted_on_the_training_rows`（`:113-115`）只比對方法 winner 的數量；`test_the_tracked_pickle_is_the_official_final_model`（`:269-273`）雖然寫了 All-in 分支，但正式資料的整體 winner 不與 All-in 共用，所以這個分支沒有被執行。這個分支若被改壞，整體 winner 與 All-in 為同一模型時 `shared_with` 會漏列 All-in（D-2「明確寫出它與哪些 winner 是同一模型」），而測試不會發現；目前的程式碼本身正確。
  - **E1**：`hw2/explain.py:108` 改為對 group 的每一欄各自獨立打亂（不再以同一個列排列一起打亂）→ `tests/test_diagnostics.py` 14 passed。模組說明的規則（「the group's encoded columns are permuted together」）對 69 欄的 `zipcode` 與 2 欄的 `yr_renovated` 有實質影響，現有測試只檢查排名的大致結構。
- **契約條款**：Spec rev 5「診斷與解釋」（permutation importance 的方法寫入方法說明）；DA D-2；Brief §8 Deployment（`predict_price()` 示範、使用限制中的外推）。
- **風險判斷**：正式產物不受影響——我依規則獨立重做的 permutation importance 與追蹤的表完全相同（第 1 節 (ii)），正式的整體 winner 不與 All-in 共用，我的低於範圍人工列被正確標示（(iii)）。缺的是日後改動這三處時，現有測試不會發現；而 #67 的完整重跑依 DA N-3 會逐位元比對 PNG、CSV 與 pickle，能抓到正式產物的改變。因此判為 Low。
- **Disposition**：本票不需修改，不延長 cycle。建議 follow-up，Owner＝**#67**（整體測試整理；若 Orchestrator 認為有更早修改 `hw2/` 測試的票，可改交該票）：(1) 人工列加一筆低於 training 下界的值並斷言被標示；(2) 以 synthetic 資料構造整體 winner 與 All-in 為同一模型的情況，斷言 `shared_with` 含 All-in；(3) 斷言 permutation 時 group 內各欄使用同一個列排列（例如以兩欄完全相同的 group 檢查打亂後仍相同）。

## 7. Routing（需要其他 authority）

### R-1 — 「標準化的讀法」的對象（required authority：**Design Authority**）

- **具體 ambiguity**：Brief §8 Deployment 的模型解釋包含「標準化／one-hot 的讀法」，#64 What to build 同樣寫「標準化與 one-hot 的讀法」；Spec rev 5「診斷與解釋」沒有提到標準化。DA `derivation-SPEC.md` B-7（§9.1 列為 #64 的 DA 義務）判定「OLS 用原始尺度，只有 Ridge／Lasso 標準化」在 boundary 內，理由之一是「Brief §8「標準化的讀法」適用於 Ridge／Lasso 的係數」。實作的讀法不同：notebook 6.2「標準化的讀法」列出最終 OLS 模型每增加 1 個 training 標準差的百分比 100·(exp(b·sd) − 1)%（`explain.coefficient_table` 的 `pct_per_train_sd`、解釋圖左半），並寫明「Ridge／Lasso 的標準化只用於它們自己的擬合（metric-only，係數不匯出），不用於這裡的解讀」。兩種讀法會改變交付內容：B-7 的讀法下，Deployment（以及之後的報告）可能需要說明 Ridge／Lasso 標準化係數的讀法；實作的讀法下，最終模型的每 SD 讀法就滿足這一項。
- **為何不是 finding**：AC-1 引用的 Spec 條款不含標準化；票文的「標準化與 one-hot 的讀法」可以合理讀成實作的做法；B-7 的文字是對 Spec 設計的 boundary 理由，沒有明寫 #64 必須產出 Ridge／Lasso 係數的讀法。這屬於契約語義不足（治理 §4.2），交 Design Authority 判定，不是對實作的 blocking finding，也不影響本 verdict。
- **需要 DA 決定**：#64 的每 1 SD 讀法是否滿足 Brief §8「標準化的讀法」；若 B-7 的意思是要說明 Ridge／Lasso 標準化係數的讀法，這項義務屬 #64 還是 #65（報告），以及在 CC-1 metric-only（係數不匯出）下如何呈現。

### 其他

- 學號（A-4）：依 S-1 記 NOT VERIFIED，不是本票結案的條件。S-2～S-5 仍是 run record §8 的 open 項目；範圍內的 commit 都還沒 push（S-3 適用）。

## 8. 其他核對與備註（不是 finding）

- **Worklog 的主張**：§3.1 的產物清單、§3.3 的數字（RESET 顯著、r＝0.335、141 對、141 筆／140 棟、DW 1.966、BP、JB、超額峰態約 3、`lat`／`yr_built`／`long` 超過 √10、條件數 47.1、permutation 第一名 `zipcode`）、§4 的部分執行方式、§5 的 V-1～V-3、V-4、V-6、V-7、V-9、V-11 都已由 Reviewer 重做或以獨立方式核對。V-10 的 20 個 mutant 沒有逐一重做，改以我自己的 28 個 mutant 取代（不同的變異點；結果見第 1 節 (vii) 與 F-1）。
- **範圍外的觀察（供 Orchestrator 轉交 #67 參考）**：cell 28（#62 的「指標 vs k」圖，不在本票的變更內，與 `b34cc50` 相同）的 stderr 輸出含 matplotlib 的 CJK 缺字警告（DejaVu Sans 沒有「路徑」等字），以及單元 `.venv` 的本機路徑（不含使用者名稱或學號）。#64 自己的圖改用英文標籤，沒有這個問題。#67 的單一完整執行會重新產生 cell 28；是否處理缺字屬 #67／其 R1 的判斷。
- **`.gitattributes`**：新 PNG 與 pickle 標為 binary，避免 `core.autocrlf` 改動位元組。
- **範圍與 git**：沒有單元目錄以外的變更，沒有修改 `doc/requirement/`（RB-5）；`requirements.txt`、`.gitignore`、`assets/vendor/`、`assets/hw2core.js` 沒有變更。範圍內 3 個 commit 的第一行都是 `[Modify] –`，沒有 Claude 標記；未 push、rebase、merge 或 force push。
- **Reviewer 的 test 隔離**：我沒有執行 notebook、沒有開啟任何守門，也沒有讀取或評估任何 test 列；scratchpad 複本上的 mutation probes 只跑 synthetic 與 training 的測試，以及讀取已匯出檔案的測試。

## 9. 結論

- Blocking findings：無。
- Non-blocking findings：F-1（Low，owner #67）。
- Routing：R-1 → **Design Authority**（「標準化的讀法」的對象；不影響本 verdict）。
- 前票 follow-up：#63 R1 F-1、F-2 已處理。
- DA #64 裁決：N-2 的三項自行核對完成；I-4 依 notebook 6.2 判定。
- 正式 Test 評估：沒有被再執行；`model_data` 與 result digest `b53ff286…` 不變。
- A-4 學號：NOT VERIFIED（S-1），不是本票結案的條件。

VERDICT: CLOSURE
