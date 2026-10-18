# Audit record — Issue #61，cycle 1，R2

| 欄位 | 內容 |
| --- | --- |
| Work Contract | 同 R1（`audit/issue-61-c1-r1.md`）：GitHub issue #61；Spec rev 5（#59）；DA `derivation-SPEC.md`（§9、§9.3、§9.6、§11 G-3）；`decision-20261018-high-risk-categories.md`（A-1～A-8）；`decision-20261018-issue60-a4-student-id.md`（S-1～S-6，§2.2）；Outcome Contract（Brief @ `dff7c55c`＋CC-1、AD-1～AD-3） |
| 受審 subject | branch `home_work_02-regrill`，**修正後的 implementation commit `77b79f4e2b775d331bc7f4be3da42354033b1c0c`**（parent `9b47896`）。R1 的 subject 是 `c9b106c`。`c9b106c..77b79f4` 中的實作 delta 有 8 個檔案：`hw2/testgate.py`、`hw2/contract.py`、`hw2/fixture.py`、`tests/test_testgate.py`、`tests/test_test_section.py`、`hw2.ipynb`、`results/model_data.json`、`assets/model_data.js`；其餘路徑都在 `doc/governance/**`。審查時 HEAD＝`61387af`，`77b79f4..61387af` 只改 `doc/governance/worklog/issue-61.md`（record-only，Bindings §7）。工作樹的實作路徑與 `77b79f4` 相同（`git diff --stat 77b79f4 -- home_work_02 ':(exclude)home_work_02/doc/governance'` 為空；`git status` 乾淨） |
| Audit 種類 | **R2**（closure review），**cycle 1**。範圍限於治理 §4.4：(1) R1 的 blocking finding F-1 是否真正解決；(2) 修正是否引入回歸；(3) 修正是否直接產生或暴露新的 blocking defect。不是第二次全面審查。**本 record 不是 Spec Integration Audit** |
| 角色 | `primary_reviewer`（`gov-primary-reviewer`；R-PR `claude-opus-5-5`／`xhigh`） |
| Assurance (a)：context independence（治理 §2.3；Bindings §3.7） | (1) **Independent context**：R2 延續同一個 Reviewer 的 R1 context（派工者以 SendMessage 續派；治理 §2.3 第 1 項、Bindings §3.7 第 1 項允許），沒有繼承 Executor 的 context。修正後的檔案、diff、notebook 與 `model_data` 都從磁碟與 git 重新讀取（第 1 節）。Worklog §8 的敘述只當作待驗證主張。(2) **Verifiable binding**：見 (b) 欄。(3) **Autonomous access**：自行讀取 `git diff c9b106c 77b79f4`、`git show 77b79f4`、worklog 的修正記錄；以 `git archive 77b79f4` 建立複本並重跑 notebook；自行執行測試、探測、獨立重算、mutation probes 與 CDP 瀏覽器檢查。(4) **Self-written record**：本檔由 Reviewer 以自己的 Write 工具寫入 |
| Assurance (b)：model diversity（Bindings §5） | **Executor**（含修正；worklog §8 記載以 SendMessage 續派同一 agent）：agentId `af27ea1586955f943`，`agentType` `gov-executor`，觀測 `('claude-opus-5-5', 'high')` 285 則、單一元素（Reviewer 以 Bindings §3.6 的邏輯自行掃描 session `4bbff425-7ff9-4cdc-b64c-cc68e824e1b1` 的 subagent transcript），符合 O-1。**本 review**（R1＋R2 同一 agent）：agentId `a68ac8fd770753723`，`agentType` `gov-primary-reviewer`，撰寫本 record 前觀測 `('claude-opus-5-5', 'xhigh')` 213 則、單一元素；全程核對由派工者依 Bindings §3.6 在採用本 record 前執行。**無 model diversity**（兩者同為 `claude-opus-5-5`）；不宣告 diversity 關係，不記 `diversity_lost`（A-8） |
| 日期 | 2026-10-18 |

## 1. 重新取得的證據

Reviewer 的腳本與產物都在 session scratchpad 的 `r1-61-reviewer/r2/`（不在 repo）。工作樹沒有被修改。

- **Diff**：逐行閱讀 `git diff c9b106c 77b79f4`（`testgate.py`、`contract.py`、`fixture.py`、兩個測試檔），commit message 與 worklog §8 的修正記錄。
- **Notebook**：以腳本比較 `c9b106c` 與 `77b79f4` 的 `hw2.ipynb`。34 個 cell；只有 cell 29（§5.3 markdown）的 source 改變。code cell 輸出的差異只在時間值，以及 stream 輸出的分段方式（cells 9、19：文字相同，分行不同）；沒有 error 輸出。
- **追蹤的 `model_data`**：`77b79f4` 與 `c9b106c` 的 `results/model_data.json` 在去掉 `meta.generated_at` 與 `meta.timing_s` 後完全相同。`git archive 77b79f4` 複本刪除產物後重跑 `python -m hw2.run_notebook` → `executed hw2.ipynb in 3.3 s`；與 commit 中的版本相比，也只有這五個時間欄位不同。
- **測試**：
  - 工作樹 `python -m pytest -q -rs -p no:cacheprovider` → **183 passed, 1 skipped**（R1 是 174 passed；skip 仍是 `test_repo_hygiene.py:71`，學號設定尚未提供）。
  - `node --test tests/js/core.test.js` → 7 pass、0 fail、2 skip（fixture 項目）。
  - `python -m hw2.offline_scan` → `scanned 6 files: PASS (0 findings)`。
  - 複本上 `pytest --ignore=tests/test_repo_hygiene.py` → 168 passed。

## 2. F-1 的 closure 條件（R1 §5 F-1）

| 條件 | 判定 | 證據 |
| --- | --- | --- |
| (a) Ridge 或 Lasso 任一個 alpha 未固定——含兩個都沒傳與只傳一個——守門就拒絕開啟 | **成立** | `hw2/testgate.py` `open()` 改為對 `METRIC_ONLY_MODELS` 的**每一個**取 `alphas.get(name)`，要求有限且大於 0，否則拋 `TestGateError`；`alphas` 為 `None` 時視為 `{}`。Reviewer 探測（synthetic）：`{}`、`None`、只給 ridge、只給 lasso、lasso 為 `None`、ridge 為 `inf`、lasso 為負值都 REFUSED，而且狀態仍是 `closed`；多出未知鍵 `enet` 也 REFUSED。R1 的 P1、P2 在修正後都是 REFUSED |
| (b) `evaluate` 只在兩個 metric-only 模型都提供時才執行 | **成立** | 凍結的 alpha 集合現在恆為 {ridge, lasso}；既有的 `sorted(metric_only) != sorted(self._alphas)` 檢查因此要求兩者都提供。探測：不提供 metric-only、只提供 ridge、lasso 的 alpha 與凍結值不同都 REFUSED，狀態仍是 `open`（拒絕不消耗本次執行）；兩者都提供時 ALLOWED（5 個 OLS＋ridge＋lasso）；第二次評估 REFUSED |
| (c) pytest 以 fixture 驗證兩種省略都被拒絕 | **成立** | `tests/test_testgate.py::test_gate_refuses_to_open_unless_both_metric_only_alphas_are_fixed`，6 個參數化案例：none、ridge-only、lasso-only、lasso-none、ridge-nan、ridge-zero。每個案例都斷言拒絕、狀態 `closed`、`evaluate` 被拒，而且之後仍可正常開啟。`test_metric_only_models_go_through_the_same_gate_once` 加了「兩個都沒提供」的評估拒絕；`test_fixture_run_scores_both_metric_only_stand_ins_once` 檢查 fixture 流程。**Fix-revert mutants**（scratchpad 複本，完整 suite）：N1 恢復成只檢查有傳入的 alpha → 3 failed（none、ridge-only、lasso-only）；N2 契約恢復成接受 metric_only 子集 → 2 failed；N3 `evaluate` 接受缺少的 metric-only 模型 → 1 failed |
| (d) notebook §5.3 的文字與程式的實際行為一致 | **成立** | Cell 29 改為「兩個 metric-only 模型（Ridge 與 Lasso）的 alpha 都已以 training CV 固定之後才能開啟（省略其中任何一個，或兩個都省略，守門都拒絕開啟）；……只評估授權清單中的 OLS 子集模型與這兩個 metric-only 模型（各一次）」，與 (a)(b) 的實測行為一致。Cell 30 對正式資料的示範仍被 TR-01 旗標先擋下（輸出 `open refused: the official test gate stays closed …`），與文字不衝突。`testgate.py` 的模組說明同步更新；worklog §3.3 加了更正註記 |
| (e) 沒有回歸 | **成立** | 見第 3 節 |

R1 探測 C3（只有 ridge 的 `metric_only` 被契約接受）在這次修正中一併處理：`contract.validate_test` 要求 `metric_only` 鍵**恰好**是 {ridge, lasso}。探測結果：少 lasso、兩個都移除、多一個 `enet` 都被拒絕；完整的 fixture `model_data` 通過。

**F-1：RESOLVED。**

## 3. 回歸核對

- **正式守門與 TR-01**：`OFFICIAL_TEST_GATE_ENABLED` 仍為 `False`。以模擬的正式資料（在探測程序內把 `EXPECTED_SHA256` 指向 synthetic 檔；沒有開啟真實 CSV）核對：
  - 旗標為 False 時，即使給齊兩個 alpha，`open` 與 `load_test_rows` 仍被拒；
  - 旗標為 True 時，第一次評估 ALLOWED，同一個 process 的第二個 gate → `already loaded`（R1 P4 行為不變）。

  追蹤的 `model_data` 仍沒有 `test`，`test_inputs` 0 列（第 1 節）。修正沒有載入任何正式 test 列：正式資料只出現在斷言拒絕的測試中，Reviewer 的腳本也沒有讀取正式 test 列。
- **獨立重算（A-2）**：以修正後的 `hw2.fixture` 產生 fxA（1,500＋40，seed 20261018）與 fxB（2,500＋120，seed 777）。獨立腳本不 import `hw2`，從 synthetic CSV 重新擬合。
  - 5 個 `ols_subset` 模型的逐筆 predicted／lower／upper 最大絕對差 ≤ 2.3e-7 USD；`covered` 逐筆相同；n_covered 相同。這些數值與 R1 的同 seed 結果完全一樣，所以 OLS 路徑沒有變動。
  - 兩個 `metric_only` stand-in：鍵只有 {alpha, kind, mae, model_key, mse, n_test, r2, rmse, scale}，沒有 PI 或逐筆欄位；MAE、RMSE、R² 與 Reviewer 以「training 列 mean ln(price) 的 exp」重算的常數預測相同（相對差 0）。
  - Node：`HW2_FIXTURE_MODEL_DATA=<fxA|fxB>` → 9 pass、0 fail、0 skip（`core.test.js` 略過非 `ols_subset` 項目）。
- **Dashboard（BR-01 第 4 點）**：修正後的 fixture 已含 ridge／lasso 的 `metric_only`（`python -m hw2.fixture`，n_test 4,291，`test` 鍵含 `lasso`、`ridge`）。以 headless Chrome、`file://`、所有主機名稱無法解析、CDP 核對：
  - 沒有例外或 console error；只請求 6 個本機檔，外加 Chrome 自己的日期選擇器 `data:` 圖示。
  - Test 區塊在 All-in、Forward SFS winner、非 winner k = 1 三種選取下都只顯示 `ols_subset` 模型；`#test` 區段文字不含 Ridge／Lasso。非 winner 的提示、「訓練 CV（USD）」與「Test 評估（USD）」標示不變。
  - firstDraw 的 `nPoints` 4,291；方法、k、wheel 互動都被記錄。`app.js` 與 `hw2core.js` 在 `c9b106c..77b79f4` 沒有修改。
- **R1 的 16 個 mutants** 在修正後的複本上重跑：**16／16 仍被偵測**。
- **H-2**：notebook 六章的標題與順序未變（只有 cell 29 的 source 改變）；`offline_scan` PASS；`index.html` 與 `assets/` 沒有修改；`file://` 載入正常。
- **H-1（A-4）**：
  - `git ls-tree -r 77b79f4 -- home_work_02` 唯一的 PDF 仍是老師文件 SRC-3；沒有 `.zip`、`.env`、`kaggle.json`、`.local/`、`acceptor_materials/`、`dist/`；沒有單元以外或 `doc/requirement/` 的變更。
  - 修正 commit `9b47896..77b79f4`（205 行新增）沒有任何 7 位以上的數字串，沒有出現「學號」，commit message 也沒有 7 位以上數字（Reviewer 的遮罩掃描，沒有印出任何值）。
  - 學號實際值比對仍是 **NOT VERIFIED**（學號設定不存在；S-1），不是 PASS。
- **Git**：commit message 符合 git 規則（`[Modify] –` 加上 `[Fix]`／`[Additions]`／`[Modification]`），沒有 Claude 標記；未 push。

## 4. 修正是否直接產生或暴露新的 blocking defect

**沒有。** 核對過的點：

- Fixture 新增的 `StandInMetricOnly` 只用 `prepared.training` 計算常數，沒有用到 test 列。Fixture 的 `fixture_note` 標明 stand-in，輸出仍受 `_outside_unit` 限制（DA §9.3 條件 4）。
- 契約改成「恰好 ridge 與 lasso」之後，只在 `test` 存在時適用；追蹤的正式 `model_data` 沒有 `test`，所以 #62 之前的正式流程不受影響。
- 以字串 `"1.0"` 傳入的 alpha 會被接受並以 `float` 凍結為 1.0。這仍是固定的值，不構成缺陷。

本次沒有新的 finding。

## 5. R1 的 non-blocking findings（不在 R2 範圍，disposition 不變）

- F-2（Medium）：`evaluate_candidate` 截斷長度不符的 `fold_groups`；owner #62。
- F-3（Low）：契約沒有核對授權清單等於聯集，dashboard 有顯示舊數字的風險；owner #62。
- F-4（Low）：正式資料「每個 process 只載入一次」沒有測試，正式資料只以 sha256 識別；owner #63。

修正沒有改動它們涉及的程式（`models.py`、`app.js`），也沒有擴大或縮小它們的影響。

## 6. 結論

- F-1：**RESOLVED**（closure 條件 (a)～(e) 全部成立）。
- 回歸：無。
- 修正產生或暴露的新 blocking defect：無。
- 剩餘的 non-blocking findings：F-2、F-3（owner #62）、F-4（owner #63），依 R1 的 disposition。
- A-4 學號：NOT VERIFIED（S-1），不是本票結案的條件；S-2～S-5 仍是 run record 的 open 項目。
- Routing：無。

VERDICT: CLOSURE
