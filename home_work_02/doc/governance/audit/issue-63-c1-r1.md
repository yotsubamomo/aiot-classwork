# Audit record — Issue #63，cycle 1，R1

| 欄位 | 內容 |
| --- | --- |
| Work Contract | GitHub issue #63「HW2 T4 Ridge／Lasso 對照、p-value backward、Adjusted R² 與一次性正式 Test 評估」（OPEN，`ready-for-agent`；含 TR-01 的「開啟守門」AC、DA TK-2、TK-4 的 AC；高風險 H-2、H-3）；Parent Spec `home_work_02/doc/spec/SPEC.md` rev 5（#59）；DA derivation `doc/governance/decisions/derivation-SPEC.md` §3 B-2、B-3、B-10，§9.1、§9.3、§9.4、§9.5 TK-2、TK-4，§9.6 TR-01，§11 G-1～G-4；高風險 `decisions/decision-20261018-high-risk-categories.md`（A-1～A-8）與 `decisions/decision-20261018-issue60-a4-student-id.md`（S-1～S-6；§2.2 #63 加標 H-2）；`decisions/decision-20261018-issue62-shared-subset-test-key.md`（D-1～D-4）；`decisions/decision-20261018-issue63-js-tolerance.md`（T-1～T-3；§7 要求 R1 一併審查測試修正）；Outcome Contract `doc/governance/outcome-contract.md`（Brief @ `dff7c55c`＋CC-1、AD-1～AD-3）；Implementation 授權：`doc/governance/run/run-20261018-hw2-formal.md` §1 designation 第 2 點 |
| 受審 subject | branch `home_work_02-regrill`，最終 subject＝`1f8e7c4408dfbd22bc3c11f4d9590dae5cb4431a`；BASE＝`b686b3a`。審查範圍 `b686b3a..1f8e7c4`：`69eb814`（pre-gate 實作，守門關閉）→ `1aefe05`（pre-gate 紀錄）→ `d413e58`（開啟守門）→ `052984b`（唯一一次正式評估的產出）→ `9073927`、`7f0339e`（紀錄）→ `1f8e7c4`（只改三個測試檔的容差修正）。全部路徑在 `home_work_02/` 內，沒有 `doc/requirement/`（`git diff --name-only b686b3a HEAD`）。審查時 HEAD＝`89f944c`；`1f8e7c4..HEAD` 只改 `doc/governance/run/run-20261018-hw2-formal.md` 與 `doc/governance/worklog/issue-63.md`（record-only，Bindings §7）。`git status --short home_work_02` 審查前後皆為空。`origin/home_work_02-regrill`＝`60d7fa67`：範圍內的 commit 都還沒 push |
| Audit 種類 | **R1**（full independent audit of accepted work scope），**cycle 1**。**本 record 不是 Spec Integration Audit**（本 Spec 有多張票，不適用單 Ticket fast path；derivation §9.1、run record §4） |
| 角色 | `primary_reviewer`（definition `gov-primary-reviewer`；Bindings §3.1 R-PR mapping `claude-opus-5-5`／`xhigh`） |
| Assurance (a)：context independence（治理 §2.3；Bindings §3.7） | (1) **Independent context**：Orchestrator 以 Agent tool 派 `gov-primary-reviewer`（非 fork），從空白 context 開始；派工內容只有路徑與識別（Ticket、Spec、DA 紀錄、OC、Brief、CONTEXT、worklog、前票 audit records、branch／SHA 序列）。派工訊息中「之後的 commit 只動 `doc/governance/**`」，以及 worklog、run record、DA 紀錄中 Executor 的敘述與數字，都只當作待驗證主張，已自行核對。(2) **Verifiable binding**：見 (b) 欄。(3) **Autonomous access**：自行讀取 `gh issue view 63`、Spec、DA 紀錄、OC、Brief、前票 audit records、git 歷史與 diff、全部實作、notebook 與測試；自行執行完整 pytest 與 Node test、不 import `hw2` 的獨立重算（test 區段與 training-only 兩部分）、mutation probes（在 `git archive 1f8e7c4` 的 scratchpad 複本上）、以 CDP 驅動的 `file://` 瀏覽器檢查；「只評估一次」另以 Executor subagent transcript 中的 tool-call 紀錄（只機械比對指令文字，不讀其推理）核對（第 1 節 (vi)）。(4) **Self-written record**：本檔由 Reviewer 以自己的 Write 工具寫入 |
| Assurance (b)：model diversity（Bindings §5） | **Executor**：agentId `a9f28ccd59c59b6b3`，`agentType` `gov-executor`，觀測 `('claude-opus-5-5', 'high')` 315 則、單一元素（含 C-1 修正的續派；Reviewer 以 Bindings §3.6 的同一邏輯自行掃描 session `4bbff425-7ff9-4cdc-b64c-cc68e824e1b1` 的 subagent transcript），符合 O-1。（容差裁決的 DA：agentId `a402db018ade125ae`，`gov-design-authority`，`('claude-opus-5-5', 'high')` 43 則、單一元素。）**本 review**：agentId `a45d7b2a500512ef3`，`agentType` `gov-primary-reviewer`，撰寫本 record 前觀測 `('claude-opus-5-5', 'xhigh')` 176 則、單一元素；全程核對由派工者依 Bindings §3.6 在採用本 record 前執行。**無 model diversity**（兩者同為 `claude-opus-5-5`）。Bindings §5 不宣告 diversity 關係，不記 `diversity_lost`（A-8） |
| 日期 | 2026-10-18 |

## 1. 審查方法與環境

Reviewer 的腳本與輸出都在 session scratchpad 的 `r1-63-reviewer/`（不在 repo）。環境：單元 `.venv`（Python 3.11.2；numpy 2.4.6、pandas 3.0.6、scipy 1.17.1、scikit-learn 1.9.1）、Node v24.19.0、Chrome 155.0.8059.80、Edge 155（headless）。

**不重新評估**：依 CC-1 第 3 點、derivation §9.3 與派工限制，我沒有執行 `hw2.run_notebook`、沒有開啟任何守門，也沒有以任何方式對 test 列重新評分。Ridge／Lasso 的 test 指標因此不重算（第 2 節 AC-1 的說明）。OLS 子集模型的逐筆重算只用已匯出的 `test_inputs` 與 `fit`，這正是 Spec 主 seam 要求的驗證路徑，不是新的評估。

- **(i) 工作樹測試**：`python -m pytest -q -rs -p no:cacheprovider` → **281 passed, 1 skipped**（skip：`tests/test_repo_hygiene.py:71`，學號設定未提供），70 s。`node --test tests/js/core.test.js` → 9 pass、0 fail、3 skip（fixture 項目；`tests/test_node_core.py` 以 fixture 執行全部 12 項並斷言 `# skipped 0`、`# fail 0`，已含在 pytest 的 281 項內）。`python -m hw2.offline_scan` → `scanned 6 files: PASS (0 findings)`。
- **(ii) 獨立重算：test 區段**（`indep63_test.py`，不 import `hw2`；只讀 `results/model_data.json`、`assets/model_data.js`、`results/split/split_assignment.csv`，以及為了值的完整性比對而讀 CSV 中 test 位置的原始值——沒有對它們擬合或評分任何模型）：
  - `.json` 與 `.js` 物件相同。
  - 依 Spec 文字自寫 encoding（基準日 2014-01-01、整修旗標與有效年份、zipcode one-hot 以 `fit.zipcode_categories` 判定），以 `math.fsum` 的不同運算順序重算兩個 `ols_subset` 模型 × 4,323 列的點預測、lower、upper：最大相對差 `allin` 2.6e-13、`forward_sfs_k17` 2.7e-13；最大絕對差 2.28e-6 USD（`forward_sfs_k17` 第 1878 列 upper）。以 `Fraction` 精確計算 ŷ 與槓桿值後再取 exp 的「近精確」值，契約值在該列 upper 偏 +2.21e-6、lower −9.3e-7，我的值偏 −7.1e-8、+3.4e-8。這與 DA `decision-20261018-issue63-js-tolerance.md` §3 的結論一致：絕對 1e-6 USD 對千萬美元級的值不是 float64 可以保證的門檻。
  - `covered`：我的區間與契約逐筆相同（8,646 筆），契約的 `covered` 也等於 `lower ≤ actual ≤ upper`；actual 與區間端點的最近相對距離 2.1e-5。`n_covered`、`coverage`、`mean_width`、二項近似半寬（1.96·√(p(1−p)/n)）與 USD 的 MAE／MSE／RMSE／R²（由契約的 `predicted` 與 `actual_price` 計算）全部完全相同（差 0）。
  - `test_inputs`：列位置與 id 等於分割的 test 列（依 CSV 列序）；房屋 4,287、重複交易 36；與 training 的 id 交集 0；未見 zipcode 0（以 training 列的 zipcode 集合自算）；`test_rows_digest` 自算相符。**與 CSV 的原始值比對 86,460 個值，0 筆不符**（含 `actual_price`）。
  - 自算 selection digest（winners＋兩個 alpha 的 sorted-key JSON 的 sha256）＝`44f7723e…4b28`，等於 manifest 與 `1aefe05` 的 pre-gate 紀錄；自算 result digest（`test_inputs`＋`test`）＝`b53ff286…c3cfc6`，等於 worklog §5。
  - 授權集合依 D-1 自算（{All-in} ∪ 各方法 winner ∪ {整體 winner} 中 canonical subset 互異者、代表鍵取首次出現者）＝`['allin', 'forward_sfs_k17']`，各 winner 的 `test_model_key` 也相同；`test` 的 `ols_subset` 鍵＝授權集合，`metric_only`＝{ridge, lasso}。
  - Adjusted R²：`allin`（rank 88）、`forward_sfs_k17`（rank 87）、p-value 對照（rank 86）以 1−(1−R²)(n−1)/(n−rank) 重算，差 0；Ridge／Lasso 為 `null` 並附「not applicable」說明。
  - Metric-only：`ridge`／`lasso` 的 `alpha` 等於 `baselines` 的 training-CV alpha、`mse`＝`rmse`²；`baselines.ridge`／`lasso` 沒有 `fit`、`coef`、`intercept`、`xtx_inv`。
  - worklog §5 的 test 摘要表（四個鍵的 RMSE、MAE、MSE、R²、涵蓋、平均寬度、二項近似）逐項與匯出值相符。
- **(iii) 獨立重算：training-only**（`indep63_train.py`，不 import `hw2`；以 `split_assignment.csv` 的 test 位置在 `read_csv(skiprows=…)` 解析時跳過，只讀 17,290 筆 training 列）：
  - Ridge：自寫 encoding 與標準化（fold 訓練列的平均與母體標準差，zipcode 0／1），scikit-learn `Ridge`，**整個 37 點網格**的 5 折 USD CV RMSE 與匯出的 `cv_by_alpha` 最大相對差 3.3e-15。
  - Lasso：以 scikit-learn `Lasso`（座標下降，不是 subject 用的 `lasso_path`）在 7 個網格點（含選定的 1e-8 與兩端）重算，最大相對差 1.8e-10。
  - 兩條匯出曲線都隨 alpha **單調不減**，argmin 在網格下緣（Ridge 1e-4、Lasso 1e-8），與匯出的 `alpha`、`alpha_at_grid_edge: "lower"` 一致；所以下緣選定是 CV 曲線本身的形狀，不是網格太窄造成的（見第 5 節 C-2）。
  - p-value backward：自寫 group partial F 檢定（含截距的 `lstsq` 兩次擬合、q＝秩差、df＝n−rank）：整個 training set 依序移除 `sqft_lot15`（p 0.380415）、`bedrooms`（p 0.068506），canonical k＝16 與匯出相同，剩餘 group 的最大 p 0.00123；5 個 fold 的子集（大小 17／17／16／16／16）與匯出相同；fold-internal CV RMSE 158,584.853 與匯出相對差 5.9e-12。
- **(iv) Mutation probes（verify-the-verification）**：`git archive 1f8e7c4 home_work_02` 解到 scratchpad（加上資料 CSV），每個 mutant 只改一處、跑相關測試檔、還原（`mutants_r1.py`、`js_probes_r1.py`）。基準 85 passed。
  - **偵測到（19／22）**：C2 test 的 metric-only alpha 不必等於 training-CV alpha；C3 `baselines.ridge` 可含 `fit`；C4 D-4 第 3 點（同一模型評兩次）不檢查（#62 R1 F-3 的 C5 mutant，現在被 `test_methods_contract.py::_score_a_shared_model_twice` 偵測）；C6 Ridge／Lasso 可有 Adjusted R²；G1 正式 test 列每個 process 只載入一次不檢查（#61 R1 F-4）；G2 正式資料只以 sha256 識別（#61 R1 F-4）；G3 開啟守門不要求 Lasso alpha；G4 允許第二次評估；G5 metric-only 模型 alpha 不比對凍結值；S2 alpha 搜尋的標準化在整個 training set 上 fit（驗證列洩漏）；S3 p-value 移除最小 p；S4 F 檢定 df 少扣截距；S5 p-value 的 fold 子集改在整個 training set 選；E1 比較表 Ridge／Lasso 的 Test 欄改填 CV 值（混用）；E2 比較表共用說明被移除（#62 R1 F-1）；JS：J1 `sale_days` 加一天、J2 以 1.96 取代 `t_crit`、J3 PI 漏掉槓桿項、J4 整修有效年份忽略 `yr_renovated`——四個都被正式 Node 逐筆重算以相對 1e-6 偵測（J2 的最小相對差 1.9e-5）。
  - **竄改契約值**：某列 upper ×(1＋2e-6) → Node 與 pytest 都失敗；×(1＋5e-7) → 都通過（確認門檻是相對 1e-6，不是空洞的檢查）；翻轉一個 `covered` → 都失敗；第 1878 列 predicted ×(1＋2e-6) → 都失敗。
  - **存活（3）**：C1（契約不檢查 p-value 出現在 `test`）是等價 mutant：任何 `test` 項目都必須是 `ols_subset`（鍵須在授權集合，而 `pvalue_backward` 不是任何候選項目）或 `metric_only`（只能是 ridge／lasso），所以這個不變量仍被其他檢查守住，不是 finding。C5（契約不檢查 alpha 是 CV argmin）與 S1（alpha 平手改取較小者）見 **F-1**。
- **(v) Dashboard（`file://`，CDP，`cdp63.js`）**：Chrome 與 Edge headless 各一次，`--host-resolver-rules="MAP * ~NOTFOUND"`、scratchpad 內的全新 profile，直接開啟 repo 工作樹的 `home_work_02/index.html`。兩者都沒有例外或 console error；請求只有 6 個本機檔，外加瀏覽器自己的 `data:image/svg+xml`。1440／768／375 px 下，五個方法、非 winner（Lasso 路徑排序 k＝3）與「比較全部」共 8 種狀態的頁面水平溢出都是 **0**，Test 區塊都有資料（散佈圖 4,323 點）。細節見第 2、3、4 節。
- **(vi) 「只評估一次」的證據**：
  - Git：`69eb814` 的 `hw2/testgate.py` 為 `OFFICIAL_TEST_GATE_ENABLED = False`；`69eb814→d413e58` 的實作差異只有這個旗標（與一個測試）；`d413e58→052984b` 只有產出（notebook 輸出、`model_data`、結果表）；`052984b→1f8e7c4` 只有三個測試檔。pre-gate 紀錄 `1aefe05`（21:36:19 +0800）早於 `d413e58`（21:36:48）與 manifest 的 `opened_at` 13:37:32Z。`69eb814` 的 notebook 新 cell（29～45）沒有任何輸出；`052984b` 的 notebook 原始碼與 `69eb814` 完全相同，執行序號 1～28 連續、沒有錯誤；只有一個 `gate.open(`、兩個 `gate.evaluate(`（第二個是被拒的那次）。`meta.test_evaluation.code_revision`＝`d413e58`、`package_modified: false`，與 git 一致。
  - Executor transcript（`agent-a9f28ccd59c59b6b3.jsonl` 的 182 個 tool call，只機械比對 Bash 指令文字）：`python -m hw2.run_notebook` 只出現一次（13:36:56Z，在 13:36:31Z 修改旗標之後）。另外兩次 notebook 執行是 `rehearse_nb.py`（13:05Z、13:15Z），它在 notebook 前插入一個 cell 把 `data.load_and_split` 換成 synthetic CSV（21,430 列／21,250 id，與正式結構不同），而且當時旗標仍是 `False`。`pregate.py`、`probe_alpha.py`、`probe_cmp.py` 只用 `prepared.training`，建立的 `TestGate` 沒有開啟（輸出 `official_gate_enabled: false`）。13:37:33Z 之後的指令只讀 `results/model_data.json`。`formal_run.log`：開始 13:36:56Z、HEAD `d413e58`、`executed hw2.ipynb in 36.8 s`、exit 0。
- **(vii) A-4 掃描**：見第 3 節 H-1。

## 2. Acceptance criteria 逐條判定

| # | AC（#63） | 判定 | 證據 |
| --- | --- | --- | --- |
| AC-1 | Spec rev 5「對照模型」（含 CC-1 六項約束）、「指標與推論」Adjusted R² 規則、`baselines`（Ridge／Lasso 只有 `cv`＋alpha、無 `fit` PI 欄位；p-value 對照）與 `test` 的 `metric_only` 契約成立 | **PASS** | `hw2/comparison.py`：全部 18 group、在每次擬合的列上標準化、同一組 fold 的 USD CV 選 alpha、網格與曲線記錄；整個 training set 重擬合為 metric-only（係數不匯出）。CC-1 (1)：第 1 節 (iii) training-only 重算；(2)：G-2；(3)(4)：G-3 與第 1 節 (vi)；(5)：`baselines.ridge`／`lasso` 的鍵集合沒有 `fit`／係數／PI 欄位，`offers` 三項皆 false，dashboard 方法選單不含它們，`Core.canPredict` 對 metric-only 為 false；(6)：G-4。p-value 對照為 group partial F、門檻 0.05、fold-internal＋canonical、不參與 winner、不在 `test`（第 1 節 (iii)）。Ridge／Lasso 的 test 指標值依 CC-1 第 3 點**不重算**（係數不匯出，重算就是再評估一次）；它們的 `alpha`、`n_test`、`mse`＝`rmse`² 一致，且數值與 alpha≈0 時應接近的 All-in 相符（RMSE 183,596.50／183,596.74 vs 183,596.70） |
| AC-2 | G-1：pytest 證明改動 test 列的值不改變 Ridge／Lasso 選出的 alpha 與 CV 指標 | **PASS** | `tests/test_comparison.py:34-63`（改動全部 test 列的價格與 5 個特徵、zipcode 改為未見類別；alpha、`cv_by_alpha`、CV 平均、p-value 子集、winners 都不變）；`test_model_data_official.py:160-178` 在正式資料上由 training 列重算 alpha、曲線與 p-value；S2 mutant 被偵測 |
| AC-3 | G-2：pytest 斷言 `winners` 的各方法 winner 與整體 winner 都不含 Ridge／Lasso | **PASS** | `test_model_data_official.py:276-286`；`test_comparison.py:137-142`（`determine_winners` 拒絕 `ridge`）；Node `checkPaths`；正式 `winners` JSON 不含 `"ridge"`／`"lasso"` |
| AC-4 | G-3：正式 test 評估在全部 alpha 與 winner 固定之後、同一執行中只執行一次，涵蓋 `ols_subset` 與 `metric_only`；第二次呼叫報錯；worklog 記錄 manifest／時間戳 | **PASS** | `hw2/testgate.py:115-145`（開啟需完整 winners 與兩個有效 alpha，凍結並算 digest）、`:176-256`（只評授權集合與凍結 alpha 的兩個 metric-only，各一次；`finally` 設為 EVALUATED）；`test_testgate.py:95-113`、`:154-175`、`:240-264`；G3、G4、G5 mutant 被偵測；notebook cell 41／42 的輸出（manifest、`evaluations_in_this_run: 1`、第二次呼叫被拒）；worklog §4、§5；第 1 節 (vi) |
| AC-5 | 開啟守門（TR-01）：同一次執行中經守門載入、唯一一次評估、同一匯出寫入正式 `test_inputs` 列與 `test`；`test_inputs` 含 18 個原始特徵、列識別、`actual_price`、房屋數與重複交易數；記錄未見 zipcode 筆數；worklog 記錄開啟時間戳、執行識別與 test 摘要 | **PASS** | notebook cell 41：`gate.open` → `gate.evaluate` → `build_model_data` → `write_model_data` 在同一 cell、同一 process；`test_inputs.fields` 為列識別＋18 個 source feature（`date` 兼列識別）＋`actual_price`；第 1 節 (ii) 的 CSV 值比對 0 筆不符、房屋 4,287／重複 36／未見 zipcode 0；worklog §5（`opened_at`、`run_id` `fe76019b…`、摘要表與 `result_digest`） |
| AC-6 | SR-02 獨立重算改以正式 `test_inputs` 與 `test` 執行：pytest（numpy）與 Node 逐筆相符（容差 1e-6）；`metric_only` 無 PI 可算且 dashboard 不提供其預測 | **PASS**（依 DA T-1：相對 1e-6） | `test_model_data_official.py:102-136`（numpy，不呼叫 `hw2` 的預測函式；`_design` 在 `test_test_section.py:26-47`）、`tests/js/core.test.js:182-205`（dashboard 自己的 `hw2core.js`）；兩者在我的環境都通過；第 1 節 (ii) 我自己的第三條路徑最大相對差 2.7e-13；第 1 節 (iv) 偵測力。`checkTestKeys`（`core.test.js:162-180`）：metric-only 無 PI 欄位、無 `fit`、`canPredict` false、`predict` 拋錯 |
| AC-7 | `ols_subset` 鍵集合等於授權清單；`metric_only` 只有 Ridge 與 Lasso；PI 欄位的有無與 `kind` 一致；coverage＝covered 之和／n_test；平均寬度與二項近似已算出 | **PASS** | `hw2/contract.py:530-590`（`validate_test`）；`test_model_data_official.py:67-81`；第 1 節 (ii) 全部相符 |
| AC-8 | G-4：比較表與報告草稿分欄標示「訓練 CV（USD）」／「Test 評估（USD）」；dashboard 任何操作不觸發重新測試 | **PASS**（比較表、notebook、CSV）；報告版屬 #65 | Dashboard 比較表（CDP 實測）：caption「「訓練 CV（USD）」與「Test 評估（USD）」分欄呈現，不混用。」、兩個 colgroup 表頭 `訓練 CV（USD）[colspan 4]`、`Test 評估（USD）[colspan 5]`、標題兩個 tag；notebook 5.5 以兩組欄呈現；`comparison.csv` 以 `cv_*`／`test_*` 分欄（第 8 節的獨立比對）。不觸發重新測試：`app.js` 對 `MD.test` 只有兩處讀取（`testResult`、`renderTest`），`Core.predict` 只用使用者輸入（`test_dashboard_static.py:106-176`），`hw2core.js` 沒有任何指標或涵蓋程式碼（`:179-182`）；我另外讀過 `app.js` 全部的 Test 區塊與比較表程式碼確認。報告草稿：報告檔由 #65 建立，derivation §9.1 把「G-4（報告）」分配給 #65（同 §9.4 I-3 的處理），所以本票以 notebook 與 CSV 的分欄表格滿足，#65 的 R1 須核對報告版 |
| AC-9 | Adjusted R² 只出現在 log 尺度、OLS 子集與 All-in；Ridge／Lasso 與 CV 聚合值標「不適用」 | **PASS** | `model_data`：`methods[].fit` 與 p-value `fit_summary` 為 log 尺度實際秩（第 1 節 (ii) 重算差 0）；`cv` 物件中沒有任何 adjusted 欄位（自行掃描 0 筆）；Ridge／Lasso `adj_r2_log: null`＋說明；notebook 5.2 表（Ridge／Lasso 與「Adjusted R²（CV 聚合值）」標「不適用」）；dashboard 比較表 Ridge／Lasso 為「不適用」，KPI 狀態文字註明對 CV 聚合值不適用；C6 mutant 被偵測 |
| AC-10 | 執行時間記入 `meta` 與 worklog | **PASS** | `meta.timing_s`（`ridge_total` 1.8631、`lasso_total` 0.8799、`pvalue_backward_total` 1.0868、`test_load_test_rows`、`test_score` 與路徑方法）、`meta.comparison_timing_s`；worklog §5 |
| AC-11 | （DA TK-2）結果表 CSV 至結果目錄，與 `model_data` 一致 | **PASS** | `results/tables/cv_by_method_k.csv`（73 列＝All-in＋4×18，無 test 欄）、`comparison.csv`（8 列）、`alpha_cv.csv`（66 列，選定列為 ridge 1e-4、lasso 1e-8）；`test_model_data_official.py:194-214`；我另外不經 `hw2.export` 直接比對 CSV 與 `model_data`：0 筆不符 |
| AC-12 | （DA TK-4）pytest 斷言 `methods` 與 `baselines` 都不含任何 test 欄位 | **PASS** | `test_model_data_official.py:56-64`、`test_test_section.py` 的 tamper（`test_rmse`、`predicted`、`n_test` 放入 `baselines`／`cv` 被拒）；自行掃描正式檔 0 筆 |

## 3. 高風險類別核對（A-1）

| 類別 | 核對內容 | 結果 |
| --- | --- | --- |
| **H-2**（票已標示；DA `decision-20261018-issue60-a4-student-id.md` §2.2 的必核項） | notebook 六章：`## 1. Business Understanding`…`## 6. Deployment` 的名稱與順序與 BASE `b686b3a` 完全相同；`python -m hw2.offline_scan` PASS（6 個檔、0 findings），CDP 實測只請求 6 個本機檔、沒有新增任何對外資源；`file://` 在 Chrome 與 Edge 都正常載入、沒有例外；`home_work_02/index.html` 路徑不變（`index.html` 只改了 aria-label 與說明文字）；預測圖（實際 vs 預測）以全部 4,323 筆正式 test 樣本繪製；README 只改檔案配置與說明，沒有抄寫數字 | PASS |
| **H-3**（票已標示） | A-2：自行執行完整 pytest（含分組隔離 `test_split.py`、選擇邊界 `test_selection.py`、`test_comparison.py` 的 fold-internal 測試）與 Node；PI／coverage 的獨立重算（第 1 節 (ii)，第三條運算路徑）；Ridge／Lasso alpha 與 p-value 的 training-only 獨立重算（第 1 節 (iii)）；README 沒有數字、報告尚未建立；worklog §5 的數字與匯出相符。A-3：`methods`／`baselines` 無 test 欄位；`test` 鍵集合＝授權清單＋{ridge, lasso}；dashboard UI 不以 `test_inputs` 評估任何模型（`app.js` 只在 `testRows()` 讀識別與實際價格，供散佈圖繪製；B-3）。CC-1 六項：第 2 節 AC-1。單次評估：第 1 節 (vi)。Test 結果沒有回饋：`052984b` 之後的實作差異只有 `1f8e7c4` 的三個測試檔，且只改比較方式（DA T-3）。另見 F-1、F-2 | PASS（F-1、F-2 為 Low） |
| **H-1**（A-4，全部票） | 追蹤檔中的 PDF 只有老師文件（`doc/requirement/50 Startups_…Explorer.pdf`）；沒有 `.zip`、`.env`、`kaggle`、`.local/`、`acceptor_materials/`、`dist/`；`.local/packaging.json` 不存在。範圍 `b686b3a..HEAD` 新增行中「學號」6 次，都是紀錄的敘述用詞，後面沒有數字；排除 `model_data`、notebook、結果表後，新增行中 7 位以上的數字串只有日期 `20261018`、commit SHA 與 sha256 片段（`21568499`、`9073927`、`5862486`、`3312006`、`11743757`、`25832288`）、R² 與 MSE 的小數位數（如 `783384654`、`3707750015`）、PI 端點的小數位數（`087959025`、`029064301`）；commit messages 中只有 `20261018`。過程中沒有印出任何疑似值。**實際學號比對 NOT VERIFIED**（學號設定尚未提供；依 `decision-20261018-issue60-a4-student-id.md` S-1）。範圍內 commit 都未 push（S-3 適用） | 替代證據滿足結案條件；實際值比對 NOT VERIFIED（S-1） |
| A-7 | 本票沒有 blocking finding；若之後 H-2／H-3 的 finding 被 defer，須有 DA 確認 | — |
| A-8 | 見表頭 (b) 欄 | — |

## 4. 前票 follow-up（owner＝#63）

| 來源 | 處理 | 判定 |
| --- | --- | --- |
| #61 R1 F-4（正式資料「每個 process 只載入一次」沒有測試；只以 sha256 識別） | `testgate.py:57-71` 的 `is_official` 另以官方路徑或官方結構（21,613 列、21,436 id）判定；`test_testgate.py:277-331` 以 monkeypatch 的 `EXPECTED_SHA256` 在 synthetic 資料上測旗標關閉時拒絕、開啟時第一個 gate 評估、第二個 gate「already loaded」被拒，以及結構／路徑識別。G1、G2 mutant 被偵測 | **resolved** |
| #62 R1 F-1（代表鍵所屬 winner 的共用說明不完整） | `app.js:217` 的 `sharedWinners` 對每個 winner 列出全部共用者。CDP 實測 Test 區塊：All-in「（與 RFE · k = 18 為同一模型（canonical subset 相同），Test 只評估一次）」；Forward SFS「（與 Backward SFS · k = 17、Lasso 路徑排序 · k = 17 為同一模型…）」；Lasso 路徑排序標「整體 CV winner」並列出 Forward 與 Backward；比較表各列與 `comparison.csv` 的 notes 同樣列出。D-2：代表鍵 Forward 沒有被當成 Lasso 的身分。E2 mutant 被偵測 | **resolved** |
| #62 R1 F-2（Test 區塊 375 px 溢出 44 px） | `style.css:227`、`:229` 加 `grid-template-columns: minmax(0, 1fr)`。正式頁面（Test 區塊有資料）在 Chrome 與 Edge 的 1440／768／375 px、8 種狀態，頁面溢出都是 0；比較表在 `.tablewrap` 容器內捲動（1440 px 40 px、768 px 381 px、375 px 774 px），頁面不溢出。OV-2 的正式量測仍屬 #67 | **resolved**（本票範圍內） |
| #62 R1 F-3（D-4 第 3 點沒有測試） | `test_methods_contract.py:120`、`:168` 的 tamper；C4 mutant（即 #62 R1 的 C5）被偵測 | **resolved** |

## 5. DA 裁決與 Executor 的 concerns

- **DA `decision-20261018-issue63-js-tolerance.md`（T-1～T-3）與 `1f8e7c4`（§7 要求 R1 一併審查）**：`1f8e7c4` 只改 `tests/js/core.test.js`、`tests/test_model_data_official.py`、`tests/test_test_section.py`。Node 的 `closeRel` 先斷言契約值有限且 > 0，再判斷 |js − 契約| ≤ 1e-6·|契約|，失敗訊息印出絕對差與相對差；pytest 兩處改為 `rtol=1e-6, atol=0`（DA §7 第 2 點的字面要求）；`covered` 仍完全相等，列數 × 模型數的斷言、`core.test.js:99` 的 `exp` 單元檢查（絕對）與 coverage、寬度、指標、二項近似的斷言都沒有改變（T-2）。`hw2/`、`assets/`、`results/`、notebook、`index.html` 沒有變更；`results/model_data.json` sha256 `fa86d76c…b891e3`、`assets/model_data.js` `37626bf9…5b29a72` 與 `git show 052984b:` 相同；result digest 不變（T-3）。偵測力見第 1 節 (iv)。符合 T-1～T-3。
- **D-1～D-4**：授權集合與 `test_model_key` 由我依 D-1 自算相符；D-2 的身分與共用標示見第 4 節；D-3：notebook 印出「2 distinct OLS subset models + 2 metric-only models」，由匯出計算；D-4 (1)～(5) 由契約檢查守住並有測試（C4 被偵測）。
- **C-1、C-4**：已由 DA 裁決，修正後我自己執行的 Node 與 pytest 都通過。
- **C-2（alpha 落在網格下緣）**：我獨立重算整條 Ridge 曲線與 Lasso 7 點，兩條曲線都隨 alpha 單調不減，下緣就是 argmin；網格屬 Brief §12 的 HOW（「Ridge／Lasso 的 alpha 網格與標準化」），只以 training 列決定（`probe_alpha.py` 只用 `prepared.training`），並以 `alpha_grid`、`cv_by_alpha`、`alpha_at_grid_edge` 記錄。符合 CC-1 第 1 點與 Spec「網格由實作決定並記錄」，不是 finding。報告如實說明「正則化在此資料上沒有改善 CV」屬 #65。
- **C-3（Test RMSE 約 183k 高於 CV RMSE 約 157k–158k）**：我的獨立重算確認這些 test 數字就是模型在 test 列上的結果；走不同程式路徑的 Ridge 與 Lasso 也得到同樣量級（183,596），fold 間 CV RMSE 標準差約 35,900 USD。這是描述性事實，依協定不換模型；說明屬 #65。不是 finding。
- **C-5（比較表在容器內橫向捲動）**：頁面不溢出；OV-2 的正式量測屬 #67。不是 finding。

## 6. Findings

### F-1 — alpha 選擇規則的兩個檢查沒有被測試獨立守住（平手測試沒有呼叫被測程式）

- **Severity**：Low。**Blocking**：否。觸及 H-3（CC-1 第 1 點），A-7 適用。
- **證據**：
  - `tests/test_comparison.py:88-96` `test_alpha_is_the_lowest_cv_rmse_and_ties_go_to_the_larger_alpha` 的平手部分（`:93-94`）把 `sel.cv_by_alpha` 全設為 1.0 後，用測試**自己的** `min(..., key=lambda r: (r["rmse"], -r["alpha"]))` 計算，沒有再呼叫 `comparison.select_alpha`。mutant S1（`hw2/comparison.py:222` 改為平手取較小 alpha）在 `tests/test_comparison.py` 下存活（16 passed）。
  - mutant C5（`hw2/contract.py:458` 的「alpha 必須是 CV RMSE 的 argmin」檢查改為 `if False:`）在 `tests/test_comparison.py` 下存活：`test_metric_only_entry_violations_are_rejected` 的 `alpha` 與 `cv_by_alpha` 兩種竄改都會先被 `alpha_at_grid_edge`（`:463`）或「`cv.mean` 等於曲線在 alpha 的值」的檢查攔下，沒有一種只違反 argmin 這一條（例如把 alpha 換成網格內部、同時讓 `cv` 與邊界旗標保持一致）。
- **契約條款**：CC-1 第 1 點（alpha 只以 training CV 選）；Spec rev 5「對照模型」（以 CV 選 alpha）；DA §11 G-1。
- **風險判斷**：正式結果不受影響——第 1 節 (iii) 獨立確認正式的兩個 alpha 就是整條曲線的 argmin，`test_model_data_official.py:160-171` 也以 training 列重算 alpha 與正式檔比對；精確平手在實際資料上幾乎不可能發生，平手規則本身屬 HOW。缺的是：日後若契約檢查或平手規則被改壞，現有 synthetic 測試不會發現。因此判為 Low。
- **Disposition**：本票不需修改，不延長 cycle。建議 follow-up，Owner＝**#64**（下一張 Executor pack；若 Orchestrator 認為不屬 #64 的範圍，可改交 #67 的整體測試整理）：(1) 平手測試改為建構真正的平手並呼叫 `select_alpha`（或其選擇函式）；(2) 在 `test_metric_only_entry_violations_are_rejected` 加一個只違反 argmin 的竄改（把 `alpha` 換成網格內部的一點，同時把 `cv` 換成該點的曲線值）。

### F-2 — conftest 的「測試中正式守門一律關閉」不涵蓋 session／module 範圍的 fixture

- **Severity**：Low。**Blocking**：否。觸及 H-3（derivation §9.3 條件 1、TR-01），A-7 適用。
- **證據**：`tests/conftest.py:18-23` 的 `official_gate_stays_closed` 是 function 範圍的 autouse fixture；pytest 先建立較高範圍的 fixture，所以 session／module 範圍的 fixture 執行時，`hw2/testgate.py:42` 的 `OFFICIAL_TEST_GATE_ENABLED = True` 仍然有效。我在 scratchpad 複本加一個暫時的 probe 測試實測：session fixture 中為 `True`、module fixture 中為 `True`、測試本體中為 `False`（probe 已刪除）。conftest 的 docstring（`:4-6`）寫「keeps the official gate closed in every test, so no test can open it or load an official test row」，對這兩種 fixture 不成立。
- **目前的暴露**：無。現有的 session／module fixture（`prepared_real`、`fixture_run`、`fixture_model_data`、`official`，以及 `test_comparison.py`、`test_models.py`、`test_selection.py`、`test_split.py` 的 module fixture）都不會對正式資料開啟守門：`prepared_real` 只做資料階段，其餘都用 synthetic 資料（`is_official` 為 false）或只讀匯出檔。我的完整 pytest 執行沒有載入任何正式 test 列（工作樹與 `model_data` 都沒有變化）。
- **契約條款**：derivation §9.3 條件 1（每次完整執行只評估一次）；TR-01（正式 test 列只能經守門載入）；`decision-20261018-high-risk-categories.md` H-3（在授權範圍外評估 test）。
- **風險判斷**：守門自 #63 起保持開啟（§9.3 預期 #64～#67 重跑 notebook 時重做同一個評估）。之後的票若新增一個在正式資料上走完整流程的 session／module fixture，就會在測試 process 中再做一次正式評估，而現有的 guard 不會阻止，docstring 也會讓人誤以為已受保護。目前沒有這樣的 fixture，因此判為 Low。
- **Disposition**：本票不需修改。Owner＝**#64**（下一張新增測試的票）：把 guard 改為涵蓋全部範圍（例如在 `pytest_configure` 或 session 範圍的 autouse fixture 中關閉旗標，並保留 function 範圍的還原），或至少把 docstring 改成實際的保證範圍；#64～#67 的 Executor 新增 session／module fixture 時不得在正式資料上開啟守門。

## 7. Routing（需要其他 authority）

- 目前沒有必要的 routing。
- AC-8 的「報告草稿」：依 derivation §9.1（「G-4（報告）」分配給 #65）與 §9.4 I-3 的同型處理，解讀為報告版由 #65 負責；這是既有 DA 紀錄的直接適用，不是新的語義判斷。若 Orchestrator 或 #65 對此有不同解讀，交 **Design Authority**。
- 學號（A-4）：依 S-1 記 NOT VERIFIED，不是本票結案的條件。S-2～S-5 仍是 run record §8 的 open 項目；範圍內的 commit 都還沒 push（S-3 適用）。

## 8. 其他核對與備註（不是 finding）

- **Worklog 的主張**：§4 的 pre-gate 選擇結果、digest 與 gate 狀態（以 `pregate.py`／`pregate.json` 與 `1aefe05` 核對）、§5 的執行紀錄與 test 摘要、§6 的 V-1、V-2、V-4、V-5（以我自己的 CDP 檢查取代）、V-6、§9 的 C1-1～C1-5 都已由 Reviewer 重現或核對。V-3 的「匯出值本身與精確值相差 2.26e-6（upper）、9.4e-7（lower）」與我的近精確計算（+2.21e-6、−9.3e-7）一致；DA 紀錄 §3 的數字（2.47e-6、−1.13e-6）略有不同，結論相同。Executor 的 mutation probes 沒有逐一重做，改以我自己的 22 個 mutant 與 4 個契約竄改取代。
- **`assert_allclose` 的相對基準**：pytest 兩處 `assert_allclose(契約值, 重算值, rtol=1e-6)` 的相對基準是重算值，而 T-1 寫的是契約值；兩者只在 1e-12 的二階差異，且 `rtol=1e-6, atol=0` 正是 DA §7 第 2 點的字面指示。不影響判定。
- **README**：「完整重跑 notebook 會以相同的 seed 與鎖版本重做同一個評估，其結果必須與第一次正式評估記錄的結果一致」與 derivation §9.3 條件 2 一致；比對基準是 worklog §5 的摘要與 `result_digest`。README 的最終內容屬 #65。
- **`archive` 的行尾**：`git archive` 依 `core.autocrlf=true` 把 `model_data.json` 等檔轉成 CRLF，所以 scratchpad 複本的位元組 sha256 與 blob 不同；工作樹的檔案與 `git show 052984b:` 的 blob 相同（第 5 節）。不影響任何結論。
- **範圍與 git**：沒有單元目錄以外的變更，沒有修改 `doc/requirement/`（RB-5）；`requirements.txt`、`.gitignore`、`assets/vendor/` 沒有變更。9 個 commit 的第一行都是 `[Modify] –`，沒有 Claude 標記；未 push、rebase、merge 或 force push。
- **Reviewer 的 test 隔離**：我沒有執行 notebook、沒有開啟任何守門，也沒有對 test 列評分任何模型。讀取 CSV 中 test 位置的原始值只用於與已追蹤的 `test_inputs` 逐值比對（這些值已在追蹤的 `model_data` 中）。

## 9. 結論

- Blocking findings：無。
- Non-blocking findings：F-1（Low，owner #64）、F-2（Low，owner #64）。
- 前票 follow-up：#61 R1 F-4、#62 R1 F-1、F-2、F-3 已處理。
- DA T-1～T-3 的測試修正（`1f8e7c4`）：符合，且偵測力已驗證。
- 正式 Test 評估：唯一一次（run `fe76019b…`、selection digest `44f7723e…`、result digest `b53ff286…`），我的獨立重算與其匯出值一致。
- Routing：無（AC-8 報告版的解讀若有爭議，交 Design Authority）。
- A-4 學號：NOT VERIFIED（S-1），不是本票結案的條件。

VERDICT: CLOSURE
