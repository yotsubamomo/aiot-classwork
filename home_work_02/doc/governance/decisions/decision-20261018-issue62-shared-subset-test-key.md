# Decision record — #62 C-1：多個 CV winner 共用同一 canonical subset 時的「同一模型只評估一次」與授權集合

- **紀錄類型**：Design Authority decision record（治理 §2.4、§3.6、§5.3 第 2 類；Bindings b5 §2.4 第 3 點、§7）
- **日期**：2026-10-18
- **Run**：`run-20261018-hw2-formal`。Orchestrator 依治理 §2.4「已指明 authority，且與本節規則一致」派工。
- **問題來源**：`doc/governance/worklog/issue-62.md` §3.3 與 §7 C-1（Executor 指明 required authority＝Design Authority）。問題以該 worklog 原文為準；worklog 的敘述與 Executor 的結論在本紀錄中只當作待驗證的主張。
- **受審 subject**：branch `home_work_02-regrill`，implementation commit `a2811e9f7191a5729d15f3a20e6eac305f85fad9`（`hw2/models.py::determine_winners`、`hw2/contract.py::validate_winners`、`assets/app.js::renderTest`／`sharedWith`、`assets/hw2core.js::testEntryKey`、`results/model_data.json`）。本紀錄撰寫時 HEAD＝`f6298e9`（record-only commit）。
- **Binding**：`gov-design-authority`，`claude-opus-5-5`（Bindings §3.1 預設 mapping，沒有 escalation，也沒有替代）。本紀錄不自證 binding，由派工者依 Bindings §3.6 核對。
- **Capability escalation**：不提出。E-DA/D1 不成立：兩種讀法的後果雖然不同，但可以用已接受的文字裁決（Brief BR-01 第 3 點與 BR-02、CONTEXT 的定義），不屬於「現有證據無法裁決」。E-DA/D2 不成立：本問題沒有我先前的決定被 FA ruling 或 Reviewer finding 推翻或爭議。

## 1. 問題

授權集合是「各方法 CV winner ∪ {All-in} ∪ {整體 CV winner}，同一模型只評估一次」。多個 winner 的 canonical subset 相同時，「同一模型」的判斷依據應該是哪一個？

- **讀法 S（subset 相同）**，也就是 Executor 實作的讀法：模型＝canonical subset 在整個 training set 上擬合的 OLS。canonical subset 相同就是同一模型，只評估一次；每個 winner 以 `test_model_key` 指向評估它的鍵。
- **讀法 K（鍵相同）**：模型＝`(方法, k)` 鍵。只有鍵相同才去重，實際上只會發生在整體 winner 與某方法 winner 重疊時。同一個擬合模型因此會在多個鍵下各評估一次。

實際資料（我自行讀 `a2811e9:home_work_02/results/model_data.json`）：

- Forward SFS、Backward SFS、Lasso 路徑排序的 winner 都是 k=17，canonical subset 相同。
- RFE 的 winner 是 k=18，canonical subset 與 All-in 相同。
- 整體 winner 是 `lasso_path_k17`。
- 讀法 S 的授權集合是 `['allin', 'forward_sfs_k17']`；讀法 K 是 5 個鍵。
- 我另外比對了這三組共用者的 `fit`：`coef_names` 相同，`coef` 的最大差值與 `s2` 的差值都是 0.0。所以它們在位元層級就是同一個擬合模型。

## 2. 依據

| 來源 | 內容 |
| --- | --- |
| Brief BR-01 第 3 點（accepted 語義；acceptor 原文見 `HW2_Regrill_Brief_Draft_v0.1.md` 第 179 行） | 「Test evaluation 僅針對各方法 CV winner、All-in baseline 及整體 CV winner（**若為相同模型，不重複評估**）」 |
| Brief BR-01 第 2 點 | 即時預測器使用選取的 (方法, k)「在完整 Training set 上擬合的 OLS 模型」。模型就是這個擬合物 |
| Brief §5 BR-02（accepted 語義） | All-in「是**單一模型**——以全部 18 個 feature group 擬合的 OLS……**它等於 B、C、D 路徑在 k = 18 的端點**」 |
| Brief §5 最佳的定義 | 「同一模型不重複評估；BR-01」 |
| `CONTEXT.md`（accepted，與 Brief 同在 `dff7c55c`） | Feature-selection method：「_Avoid_: Model (a method yields subsets; **a model is fitted on one subset**)」。Canonical subset：「what is evaluated on the test set when it is a CV winner」。Test evaluation：「(**a model shared between these is scored once**)」。All-in baseline：「it equals the k = 18 endpoint of the forward, backward and RFE paths」 |
| Spec rev 5「分割與交叉驗證」 | canonical subset「是 dashboard 顯示的 groups、即時預測器與 **test 評估所用的模型**（在整個 training set 上擬合）」；CV 指標估計的是「該方法在 k 下的程序」，不是 canonical subset 本身 |
| Spec rev 5「特徵選擇與模型」 | 授權集合的定義，以及「同一模型只評估一次」 |
| Spec rev 5 `model_data` 契約不變量 | `test` 中 `ols_subset` 的鍵集合等於 `winners` 的授權清單 |
| Subject 程式（自行讀取 `a2811e9`） | `fit_model(training, canonical)` 只依賴 training 列與 canonical groups，不依賴方法（`models.py` 第 113 行、第 222 行）。canonical groups 一律整理成 canonical order（第 181 行）。`determine_winners` 依 All-in → 方法順序 → 整體 winner 的順序，取每個 subset 第一次出現的鍵當代表。`validate_winners` 核對：每個 winner 與其 `test_model_key` 的 canonical subset 相同；授權集合等於所有 winner 的 `test_model_key` 集合；授權集合內沒有重複的 subset |

## 3. 裁決

**D-1（模型的識別）**：「同一模型」以讀法 S 判斷。對 test 評估而言，模型就是 canonical subset 在整個 training set 上擬合的 OLS。兩個 winner 的 canonical subset（canonical order 下的 group 集合）相同時，就是同一模型；這包括路徑方法的 k=18 與 All-in。授權集合是 {All-in} ∪ 各方法 winner ∪ {整體 winner} 中**互不相同的模型**，每個模型只在一個代表鍵下評估一次。代表鍵依固定順序取第一個出現者：All-in、方法順序、整體 winner。每個 winner（含 All-in 與整體 winner）都在 `winners` 中以 `test_model_key` 記錄它的模型是在哪個鍵下評估的。讀法 K 不採用。

**D-2（winner 的身分不因共用而改變）**：共用模型只表示 test 結果共用，不表示 winner 的身分合併。以下各點都必須成立：

- 每個 winner 保留自己的方法、k、`model_key`、CV 指標與 winner 標記。
- 任何呈現 winner 的 test 結果時（dashboard 的 Test 區塊與比較表、結果表 CSV、notebook、報告），都以**該 winner 自己的身分**標示，數值經 `test_model_key` 取得，並明確寫出它與哪些 winner 是同一模型、Test 只評估一次。
- 代表鍵所屬的方法不得被當成其他 winner 的身分。例如在實際資料上，整體 CV winner 是「Lasso 路徑排序 k=17」，不得呈現為「Forward SFS k=17」。
- 共用模型的幾個 winner 可能有不同的 CV RMSE。這是 fold-internal 程序的差異（Spec「分割與交叉驗證」），不是不同模型的差異。報告與 dashboard 的方法說明不得把它寫成同一個擬合模型有兩個 CV 分數。

**D-3（數量的陳述）**：只要陳述「在 test 上評估了幾個模型」，指的都是授權集合中互不相同的 OLS 模型數，再加上 Ridge、Lasso 兩個 metric-only，不是 winner 的數量。這個數字必須由匯出結果計算後引用，不寫死。

**D-4（不變量；`a2811e9` 已實作，Reviewer 依 A-1～A-3 核對）**：

1. 每個 winner 的 `canonical_groups` 等於其 `test_model_key` 項目的 `canonical_groups`。
2. 授權集合＝所有 winner 的 `test_model_key` 的集合。
3. 授權集合內任兩個鍵的 canonical subset 都不同。
4. `test` 中 `ols_subset` 的鍵集合＝授權集合（Spec 契約不變量不變）。
5. G-3 的「每個模型只評估一次」以 D-1 的模型為單位。

## 4. 理由

- **兩份已接受的文字都直接回答了「模型」是什麼**。CONTEXT 把方法與模型分開定義（方法產生 subset，模型擬合在一個 subset 上），並寫明 canonical subset 就是 test 評估的對象。BR-02 寫明 All-in 是「單一模型」且「等於」k=18 端點。依這兩項，RFE k=18 與 All-in 是同一模型；同理，canonical subset 相同的 Forward k=17 與 Lasso 路徑 k=17 也是同一模型。程式證據與這一點相符：擬合只依賴 subset，實際資料上共用者的擬合結果完全相同。
- **讀法 K 抵觸 acceptor 原文**。它會把同一個擬合模型評估多次，違反「若為相同模型，不重複評估」。它也會讓這句話幾乎沒有作用：整體 winner 本來就一定是候選之一，鍵相同的重疊永遠存在，不需要特別寫出。
- **讀法 S 沒有減少 acceptor 要求呈現的資訊**。BR-01 第 4、5 點要求 Test 區塊展示每個方法的 winner 結果。每個 winner 都能經 `test_model_key` 取得它自己模型的 test 結果，數值與讀法 K 相同；差別只在於沒有重複評估。BR-01 的 UI 驗收要求 Test 區塊「明確標示正在展示的模型方法與 k」，D-2 保證標示的是選取方法的 winner，並另外說明它與哪些 winner 共用。
- 這不是 Executor 的 HOW：它決定 #63 寫出的 `test` 鍵集合、報告的呈現與 test 評估的次數，屬於識別語義（治理 §3.6「identity 語義」），所以由 DA 裁決並留下紀錄。

## 5. Accepted 語義與 boundary

- **不改變 accepted 語義**。這是治理 §5.3 第 2 類：依 Brief BR-01、BR-02 與 CONTEXT 的已接受文字，釐清 derived contract（Spec「特徵選擇與模型」的授權集合、`winners` 契約）。它不增加或移除任何被評估的模型，也不改變任何 AC、invariant 或 gate。TR-01 的「CC-1 授權集合不變」仍然成立，因為集合的定義沒有改變，本紀錄只確定「同一模型」的識別。
- **Boundary**：在 Outcome Contract boundary 內。不需要 acceptor，沒有接受或授權缺口。
- **Spec**：不需要修訂。Spec 的文字與 D-1 一致；`test_model_key` 是 `winners`「被授權評估 test 的模型清單」的實作細節。之後若 Spec 因其他原因修訂，SHOULD 在 `winners` 一項加註 `test_model_key` 並引用本紀錄（editorial）。在那之前，本紀錄就是 #63～#67 與 Spec Integration Audit 依循的 clarification。

## 6. 對實作的要求

- **#62（`a2811e9`）不需要修改**。`determine_winners` 的 S 讀法、`validate_winners` 的檢查（D-4 第 1～3 點）與 dashboard 的標示（`renderTest` 以選取方法的 winner 為 `shown`，共用時附「與 … 為同一模型，Test 只評估一次」；`sharedWith`；整體 winner 標籤）都符合 D-1、D-2。這是設計層級的判斷，不取代 R1 的 audit：實作是否正確、測試是否足夠，仍由 Reviewer 依 A-1～A-3 判斷。
- 可選、非必要的強化（由 Executor 依 HOW 自行決定，不是 closure 條件）：`validate_winners` 在 `complete` 時可以要求每個 winner 都有 `test_model_key`，不再預設回自己的 `model_key`。目前的預設不會造成漏洞，因為預設鍵如果不在授權集合中，檢查就會失敗。

## 7. 受影響的工作與 evidence

| 對象 | 影響 |
| --- | --- |
| #62 | C-1 由本紀錄結案；實作不變。R1 依 D-4 核對，並依 D-2 核對 dashboard 的標示（含整體 winner 是 Lasso 路徑 k=17 時的標籤）。Worklog V-4、V-5、V-7、V-10 的證據可以沿用 |
| #63 | 開啟守門時，以授權集合（D-1）的鍵評估 `ols_subset`。G-3「每個模型只一次」以 D-1 的模型為單位。比較表的 Test 欄與 TK-2 結果表 CSV：每個 winner 各佔一列，test 指標經 `test_model_key` 取得，並標明共用（D-2）。不得為了讓每個 winner 都有自己的鍵而重複評估 |
| #64 | 整體 CV winner 的最終模型就是它的 canonical model；以「Lasso 路徑排序 k=17」（或屆時的整體 winner）的身分呈現（D-2） |
| #65、#66 | 報告、README、ACCEPTANCE 依 D-2、D-3 呈現共用模型與評估數量；TK-3 的選擇偏誤陳述照常 |
| #67、Spec Integration Audit | 核對 D-4，以及 dashboard、報告的共用標示 |
| #60、#61 的 closure evidence | 不受影響（#61 R1 F-3 由 #62 處理，本紀錄與該處理一致） |

## 8. Required authority

無。本裁決在 DA 權限內，不需要 acceptor，也不需要 escalation。
