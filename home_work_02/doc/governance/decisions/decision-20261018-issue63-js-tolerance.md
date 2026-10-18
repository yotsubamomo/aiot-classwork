# Decision record — #63 C-1：主 seam 逐筆重算「容差 1e-6」的語義（Python／JS）

- **紀錄類型**：Design Authority decision record（治理 §2.4、§3.6、§5.3 第 2 類；Bindings b5 §7）
- **日期**：2026-10-18
- **Run**：`run-20261018-hw2-formal`。Orchestrator 依治理 §2.4「已指明 authority，且與本節規則一致」派工。
- **問題來源**：`doc/governance/worklog/issue-63.md` §7 C-1（連帶 C-4），證據在同檔 §5、§6 V-3（Executor 指明 required authority＝Design Authority）。Worklog 的敘述、數字與 Executor 提出的讀法，本紀錄只當作待驗證的主張；下文數字是我自行重算的結果。
- **受審 subject**：branch `home_work_02-regrill`，最終 implementation commit `052984ba21568499aad4b02e6ba8c564901e8c76`（pre-gate `69eb814`、開啟守門 `d413e58`）；撰寫時 HEAD＝`9073927`（record-only）。相關檔案：`assets/hw2core.js::predict`、`hw2/ols.py::log_interval`／`usd_interval`、`tests/js/core.test.js`、`tests/test_node_core.py`、`tests/test_model_data_official.py`、`tests/test_test_section.py`、`assets/model_data.js`。
- **Binding**：`gov-design-authority`，`claude-opus-5-5`（Bindings 預設 mapping，沒有 escalation，也沒有替代）。本紀錄不自證 binding，由派工者依 Bindings §3.6 核對。
- **Capability escalation**：不提出。E-DA/D1 不成立：兩種讀法的後果不同，但可以用現有證據裁決（第 3 節的精確計算證明其中一種讀法在 float64 下無法作為保證）。E-DA/D2 不成立：本問題沒有我先前的決定被 FA ruling 或 Reviewer finding 推翻或爭議（#61 worklog 採「絕對 USD」是 Executor 的 HOW 選擇，不是 DA 裁決）。

## 1. 問題

Spec rev 5「Testing Decisions／主 seam」對 pytest（numpy）與 Node（dashboard 自己的程式）兩條獨立重算都寫「與 `test` 的值逐筆相符（容差 1e-6）」，ticket #63 AC 同樣寫「逐筆相符（容差 1e-6）」。文字沒有寫單位，也沒有寫是絕對或相對。點預測、lower、upper 都是 USD 值。這個 1e-6 是：

- **讀法 A（絕對）**：|重算值 − 契約值| ≤ 1e-6 USD。這是 #61 Executor 自選的「最嚴格讀法」，目前 `tests/js/core.test.js`、`tests/test_model_data_official.py`、`tests/test_test_section.py` 都這樣實作。
- **讀法 R（相對）**：|重算值 − 契約值| ≤ 1e-6 × |契約值|。
- **讀法 C（組合，Executor 提及）**：例如「絕對 1e-6 或相對 1e-12」。

## 2. 依據

| 來源 | 內容 |
| --- | --- |
| Brief §10（accepted 語義，`dff7c55c`） | 「Python/JS 一致性測試：點預測、PI 上下界、涵蓋狀態、前處理轉換（日期、整修年、zipcode one-hot）逐筆比對。」**沒有任何數值容差** |
| Brief §7 Q43（accepted） | 「PI 上下界、涵蓋狀態與 coverage 統計和 Python 匯出一致」 |
| Spec rev 5 user stories 34、63 | 目的：「網頁上的數字就是模型的數字」；「dashboard 的計算與 Python 一致」 |
| Spec rev 5 主 seam（第 215、216 行） | pytest 與 Node 各「逐筆相符（容差 1e-6）」；pytest 的重算「不呼叫匯出程式的預測函式」 |
| Ticket #63 AC（SR-02 那一項） | 「pytest（numpy）與 Node 對每個 `ols_subset` 模型的全部 test 筆逐筆相符（容差 1e-6）」 |
| Outcome Contract CC-1 第 3 點；derivation §9.3 | 正式 Test Evaluation 只執行一次；之後不得以 test 結果改變選擇、alpha、前處理或模型集合 |
| `decision-20261018-high-risk-categories.md` | 「Python 與 JS 不一致」列為 H-3 風險；A-2 要求 Reviewer 自己執行 pytest 與 Node 的獨立重算 |
| Grill 紀錄 `HW2_Regrill_Brief_Draft_v0.1.md` | 搜尋「1e-6」「容差」「toleran」都沒有結果；1e-6 是 `/to-spec` 產生的 derived contract 內容，不是 acceptor 接受的數值 |

## 3. 我自行核對的證據

1. **重現差異**（scratchpad `da63/jsdiff.js`，以 `052984b` 的 `assets/hw2core.js` 與 `assets/model_data.js`，Node v24）：2 個模型 × 4,323 列 × 3 個值＝25,938 個數值。超過絕對 1e-6 的只有 2 個，都在 `forward_sfs_k17` 第 1878 列：lower 差 1.33e-6（契約值 9,370,545.029064301），upper 差 2.90e-6（契約值 19,433,214.087959025）。全部數值的最大絕對差 2.90e-6、最大相對差 2.63e-13。`covered` 8,646 筆全部一致。與 worklog V-3 相符。
2. **精確值**（scratchpad `da63/row1878.json`，Python `decimal`，60 位有效數字）：以契約匯出的 `coef`、`xtx_inv`、`s2`、`t_crit`（JSON 以 `repr` 寫出，與記憶體中的 float64 完全相同；`hw2/models.py` 第 96～97 行沒有捨入）與該列的設計向量精確計算：
   - 契約匯出值本身與精確值相差：predicted +4.2e-8、lower −1.13e-6、upper +2.47e-6。
   - JS 的值與精確值相差：lower +2.0e-7、upper −4.3e-7。JS 在這一列比匯出值更接近精確值。
   - Worklog 寫的是 9.4e-7（lower）與 2.26e-6（upper）。我的數字略有不同，可能是設計向量或計算方式的差異；結論一樣：upper 的匯出值本身就偏離精確值超過 1e-6 USD。
3. **原因**：log 尺度上 ŷ ≈ 16.42，但截距約 −64.3，加上 `sale_days`、`yr_built`、`lat`／`long` 等量級不同的項，總和有消去。float64 的捨入在 log 尺度約 1e-13（約數十個 ulp），經 exp 放大到千萬美元級的值時就是 1e-6 USD 的量級。numpy 的 pytest 重算能在絕對 1e-6 內通過，是因為它和匯出用同一個運算式（`einsum`、相同的運算順序）；JS 的運算順序不同。這是數值精度的極限，不是任何一邊的缺陷。
4. **相對 1e-6 仍然能抓到真正的缺陷**（以正式 `fit` 估算）：`sale_days` 差一天 → 相對約 2.2e-4；用 z＝1.96 取代 t（df≈17,200）→ PI 端點相對約 2.6e-5；整修旗標、zipcode one-hot、單位或欄位錯置都是 1e-2 以上。這些都比 1e-6 大一個數量級以上。
5. **`covered` 不在容差邊緣**：全部授權模型與全部 test 列中，actual price 與 lower／upper 的最近相對距離是 2.1e-5，遠大於 1e-6；涵蓋狀態的比對維持完全相等就有意義。

## 4. 裁決

**T-1（容差的語義）**：Spec 主 seam 與 ticket #63 的「逐筆相符（容差 1e-6）」，對 USD 尺度的點預測、lower、upper，指**相對容差 1e-6**：

> |重算值 − 契約值| ≤ 1e-6 × |契約值|（契約值必須是有限且大於 0 的數）

這同時適用於 pytest（numpy）與 Node 兩條重算路徑，正式資料與 fixture 都一樣。讀法 A、C 不採用。

**T-2（不放寬的部分）**：

- `covered` 逐筆**完全相等**（不套用容差）；`n_covered`、`coverage`、`mean_width`、MAE／MSE／RMSE／R²、二項近似的既有檢查不變。
- 每個 `ols_subset` 模型 × 全部 test 列都要比對（列數與模型數的斷言不變）；不得抽樣、略過或只比對部分列。
- 前處理單元案例與其他斷言（含 `core.test.js` 第 93 行的 `exp` 單元檢查）不在本裁決範圍，不變。
- 測試 MAY 比 T-1 更嚴格，但不符合更嚴格的檢查、而符合 T-1 的情況，不構成契約失敗。

**T-3（正式評估的結果有效）**：`052984b` 的 `test` 與 `test_inputs` 依 T-1 與 Python／JS 逐筆一致，不需要也不得重新評估。本裁決只改變驗證的比較方式，不改變任何選擇、alpha、前處理、模型集合或匯出的數字，所以不屬於 CC-1、§9.3 禁止的「以 test 結果回饋」。

## 5. 理由

- **讀法 A 不是「一致」的合理解讀**。在正式資料上，契約匯出值本身就和精確答案差 2.47e-6 USD。照讀法 A，完全正確的實作也可能因為運算順序不同而失敗，能通過的只有與匯出程式運算順序相同的重算，這正好違背 Spec 要求的「獨立」重算。這樣的檢查測的是浮點運算順序，不是 Brief §10 要求的一致性。
- **讀法 R 符合已接受的目的**。Brief §10 與 user stories 34、63 要的是 dashboard 的數字就是模型的數字。相對 1e-6 對 USD 價格約 6 位有效數字，遠低於報告與 dashboard 的顯示精度，又比任何實際缺陷造成的差異小一個數量級以上（第 3 節第 4 點）。
- **讀法 C 引入了 Spec 沒有的新門檻**（1e-12）。它只比觀察到的最大相對差 2.6e-13 大約 4 倍，在不同機器、Node 或 numpy 版本下容易誤報，影響 #64～#67 的乾淨環境重跑。Spec 只給了一個數字 1e-6，保留這個數字、只確定它的意義，是最小的 clarification。
- **這屬於 DA 的範圍**：這是 derived contract（Spec 主 seam、ticket AC）中驗證門檻的 measurement 語義，有兩種會影響實作的合理解讀（治理 §3.6），Executor 不得自行選擇放寬。Executor 維持測試並如實回報失敗是正確的處理。

## 6. Accepted 語義與 boundary

- **不改變 accepted 語義**。這是治理 §5.3 第 2 類（在 Formal 中以 DA decision record 承載的 clarification，性質等同 §3.6-A）。Accepted 的 Brief §10 只要求「逐筆比對」，沒有數值容差；「容差 1e-6」是 `/to-spec` 產生的 derived contract 內容，沒有經 acceptor 以數值方式接受。本裁決沒有新增或移除 requirement、AC、invariant 或 gate：比對仍然是逐筆、全部列、兩條獨立路徑，涵蓋狀態仍然完全相等。
- **Boundary**：在 Outcome Contract boundary 內。不需要 acceptor，也沒有接受或授權缺口。
- **不需要重新評估**：正式 test 評估已執行一次，本裁決不要求再執行 `hw2.run_notebook`、開啟或重新開啟守門，也不要求改動 `results/`、`assets/model_data.*` 或 notebook。
- **Spec 與 ticket**：不需要現在修訂。之後若 Spec 因其他原因修訂，SHOULD 在主 seam 兩處把「容差 1e-6」改為「相對容差 1e-6」並引用本紀錄（editorial）。在那之前，本紀錄就是 #63～#67、Reviewer 與 Spec Integration Audit 對這兩處與 ticket #63 AC 的有效解讀。

## 7. 對實作的要求（給 Executor 的 targeted correction，只改測試）

範圍限於 `home_work_02/tests/`。**不得**修改 `hw2/`、`assets/`、`results/`、`hw2.ipynb`、`index.html`；**不得**執行 `hw2.run_notebook` 或任何會載入正式 test 列的程式；`OFFICIAL_TEST_GATE_ENABLED` 不動。

1. **`tests/js/core.test.js`**：`recomputeAll` 中 prediction、lower、upper 與契約值的比較改用 T-1 的相對判斷（例如 `Math.abs(a − b) <= 1e-6 * Math.abs(b)`，並先斷言 `b` 是有限且大於 0 的數）。正式與 fixture 兩個 test 都經過這個函式，兩者一起適用。`covered` 的 `assert.equal`、列數與模型數的斷言不變。檔頭註解改為相對容差並引用本紀錄。失敗訊息 SHOULD 同時印出絕對差與相對差。
2. **`tests/test_model_data_official.py`（第 119～121 行）與 `tests/test_test_section.py`（第 144～146 行）**：`assert_allclose(..., rtol=0, atol=TOL)` 改為 `rtol=1e-6, atol=0`，讓兩條重算路徑使用同一個判斷（T-1）；`TOL` 旁的「USD」註解改為相對並引用本紀錄。其他斷言（covered、coverage、mean_width、指標、二項近似）不變。
3. **Verification**（記入 `worklog/issue-63.md`，並以本紀錄結束 C-1、C-4）：
   - `node --test tests/js/core.test.js`：正式 test 通過；記錄全部 25,938 個數值的最大絕對差與最大相對差。
   - 完整 pytest（含 `test_node_core.py`）：除了學號設定的 skip 之外全部通過。
   - 偵測力：至少一個 JS 端的 mutant 在 scratchpad 的單元複本上仍被正式 recompute 偵測，例如 `sale_days` 差一天，或以 1.96 取代 `t_crit`。不得改動 repo 中的 `assets/hw2core.js`。
   - 確認 `results/model_data.json` 與 `assets/model_data.js` 的 sha256 與 `052984b` 相同，`export.result_digest` 仍等於 `b53ff286…c3cfc6`。
4. 這個修正是 #63 契約內的 rework，不是新工作，也不是重新評估。它在 #63 R1 之前完成，由 R1 一併審查。

## 8. 受影響的工作與 evidence

| 對象 | 影響 |
| --- | --- |
| #63 | C-1、C-4 由本紀錄裁決；依第 7 節修改測試後重新驗證。§5 的正式評估結果、manifest 與 `result_digest` 有效，不受影響。R1 依 A-2 自行執行 pytest 與 Node，比對方式依 T-1、T-2 |
| #61、#62 的 closure evidence | 不受影響。它們以絕對 1e-6 USD 通過；對 1 USD 以上的值，這比 T-1 更嚴格，所以仍然滿足 T-1 |
| #64～#67 | 乾淨環境重跑時的主 seam 比對依 T-1。§9.3 條件 2「重跑結果與 #63 一致」（`result_digest` bit-exact；只差最後幾位時 route 給 DA）是另一項檢查，本紀錄不改變它 |
| Spec Integration Audit | 引用本紀錄，作為主 seam「容差 1e-6」的解讀 |
| Spec rev 5、ticket #63、Outcome Contract | 不修改（第 6 節） |

## 9. Required authority

無。本裁決在 DA 權限內，不改變 accepted 語義，不需要重新評估，不需要 acceptor，也不需要 escalation。第 7 節的修正由 Orchestrator 派回 #63 的 Executor。
