# Decision record — #64 R1 R-1：Brief §8「標準化的讀法」的對象

- **紀錄類型**：Design Authority decision record（治理 §2.4、§3.6、§4.2、§5.3 第 2 類；Bindings b5 §7）
- **日期**：2026-10-18
- **Run**：`run-20261018-hw2-formal`。Orchestrator 依治理 §2.4「已指明 authority，且與本節規則一致」派工。
- **問題來源**：`doc/governance/audit/issue-64-c1-r1.md` §7 **R-1**（required authority＝Design Authority；Reviewer 明示它不是 finding、不影響 VERDICT: CLOSURE）。Reviewer 與 Executor 的敘述都只當作待驗證的主張；下文的事實是我自行核對的（第 3 節）。
- **受審 subject**：branch `home_work_02-regrill`，#64 implementation commit `003b825426a500fa2d11ebea584d48c93cd4635d`（notebook `home_work_02/hw2.ipynb` §6.2、`hw2/explain.py`、`results/tables/final_model_coefficients.csv`）；撰寫時 HEAD＝`17de19b`（`003b825..HEAD` 只動 `doc/governance/**`）。
- **Binding**：`gov-design-authority`，`claude-opus-5-5`／`high`（Bindings 預設 mapping，沒有 escalation，也沒有替代）。本紀錄不自證 binding，由派工者依 Bindings §3.6 核對。
- **Capability escalation**：不提出。**E-DA/D1 不成立**：兩種讀法（第 4 節的 (A)、(B)）後果不同，但現有的 accepted 文字足以裁決（第 5 節：Grill Q31、`CONTEXT.md`「Metric-only model」、老師原文「explain the model」）。**E-DA/D2 不成立**：R-1 不是 finding（audit record §7 R-1「為何不是 finding」），也沒有以證據推翻或爭議 B-7 的判定（「OLS 用原始尺度，只有 Ridge／Lasso 標準化」在 boundary 內）；它請求的是對 B-7 理由欄一句話的解讀。本紀錄維持 B-7 的判定，只更正該句理由（第 4 節 R-1.4）。

## 1. 問題

Brief §8「Deployment 階段內容」的模型解釋列出「log 尺度係數的百分比解讀、**標準化／one-hot 的讀法**、特徵重要性」；#64 What to build 寫「標準化與 one-hot 的讀法」。Spec rev 5「診斷與解釋」沒有提到標準化。我在 `derivation-SPEC.md` B-7 的理由欄寫了「Brief §8『標準化的讀法』適用於 Ridge／Lasso 的係數」，並在 §9.1 把 B-7 列為 #64 的 DA 義務。#64 的實作則把「標準化的讀法」做成最終 OLS 模型的「每增加 1 個 training 標準差」百分比，並寫明 Ridge／Lasso 的標準化不用於解讀。

要決定的是（audit record R-1「需要 DA 決定」）：

1. #64 對最終 OLS 模型的每 1 SD 讀法，是否滿足 Brief §8 的「標準化的讀法」。
2. 若 B-7 的意思是要說明 Ridge／Lasso 標準化係數的讀法，這項義務屬 #64 還是 #65，以及在 metric-only（係數不匯出）下如何呈現。

## 2. 依據

| 來源 | 內容 |
| --- | --- |
| 老師原文 SRC-2T（`doc/requirement/HW2-requirements-Multiple Linear regression_SRC-2_2026-10-18.txt` 第 146 行） | 「6. Deployment: Predict new samples and explain the model.」全文沒有提到標準化或係數讀法 |
| Grill 紀錄 rev 7 Q25（`dff7c55c`） | Deployment 內容：dashboard 連結與說明；`predict_price()` 示範；模型解釋；使用限制。沒有細分 |
| Brief §8（`dff7c55c`，accepted） | 「模型解釋（log 尺度係數的百分比解讀、標準化／one-hot 的讀法、特徵重要性）」，位於 Deployment 階段內容，與 `predict_price()` 示範並列 |
| Brief §4（accepted） | 「需要 fit 的前處理（one-hot 類別、標準化參數）只以當次訓練列 fit」：Brief 沒有決定哪些模型標準化 |
| Brief §12（accepted） | 「Ridge／Lasso 的 alpha 網格與標準化」留給技術設計（HOW） |
| Grill Q31（accepted） | 只有 OLS 子集模型可即時預測；「Ridge／Lasso 只在比較表與圖」 |
| OC §4 CC-1 第 5 點；Brief §7 BR-01 第 3、4 點 | Ridge／Lasso 仍為 metric_only；test 只報 USD 的 MAE、MSE、RMSE、R²；Ridge／Lasso 的 test 指標只出現在比較表 |
| `CONTEXT.md`「Metric-only model」（CC-1 依 acceptor 指示同步，`84fe922`） | 「A comparison model (Ridge, Lasso) … that reports CV and one-time test metrics only」 |
| Spec rev 5「資料、計數與前處理」 | 數值欄的標準化只用於 Ridge／Lasso，OLS 以原始尺度擬合，「使係數可直接解讀且 dashboard 不需重做標準化」 |
| Spec rev 5「特徵選擇與模型」 | 最終模型＝整體 CV winner 在整個 training set 上重新擬合，「用於 Deployment 的預測函式、pickle 示範、診斷與報告主要結果」；Ridge／Lasso「只報 CV 與 test 指標」 |
| Spec rev 5「`model_data` 契約」 | `metric_only` 只有 USD 的 test 指標，沒有係數 |
| Spec rev 5「報告與打包」 | 報告的數字與圖由建置時從匯出結果注入或引用，不手抄 |
| `derivation-SPEC.md` B-7、§9.1 | B-7 判定與理由（第 1 節所引）；§9.1 把 B-7 列為 #64 的 DA 義務 |
| `decision-20261018-issue64-notebook-rerun.md` I-4 | 報告版的模型解釋段落由 #65 負責，#64 以 notebook 6.2 滿足來源段落 |

## 3. 我自行核對的事實

1. **notebook 6.2（`003b825`，cell 60）**：「係數的讀法」以原始尺度寫每單位 100·(exp(b) − 1)%；「one-hot（zipcode）」相對基準 zipcode；「整修」兩欄一起解讀；「**標準化的讀法**」寫明 OLS 以原始尺度擬合（係數可直接以原始單位解讀、dashboard 不需重做標準化），另列每增加 1 個 training 標準差的 100·(exp(b·sd) − 1)%（sd 來自 training set），並寫明「Ridge／Lasso 的標準化只用於它們自己的擬合（metric-only，係數不匯出），不用於這裡的解讀」。cell 58 的第 6 章導言也列出「標準化與 one-hot 的讀法」。
2. **計算與匯出**：`hw2/explain.py` `coefficient_table`（`003b825`）對每個 numeric 欄以 training 列的 `col.std()`（NumPy 預設 ddof＝0，即母體標準差）計算 `train_sd`，`pct_per_train_sd`＝100·expm1(b·sd)；one-hot 與 `is_renovated` 旗標的 sd 為空。這與 notebook 4.3 Ridge／Lasso 的標準化慣例一致（數值欄以當次訓練列的平均與**母體標準差**標準化、zipcode one-hot 維持 0／1、目標仍是 ln(price)）：b·sd 正是同一欄在 Ridge／Lasso 慣例下的標準化係數。追蹤的 `results/tables/final_model_coefficients.csv` 有 `train_sd`、`pct_per_train_sd` 兩欄。R1 第 1 節 (ii) 已獨立重算這兩欄（最大相對差 1.4e-13），mutation E3（改用 ddof＝1）被測試偵測。
3. **Ridge／Lasso 的係數**：notebook 4.3 寫明兩者 metric-only、「係數不匯出」；`model_data` 的 `metric_only` 項目沒有係數（Spec 契約）。現有的追蹤結果檔中沒有 Ridge／Lasso 的係數。
4. **Dashboard**：選配的係數表沒有每 1 SD 欄（worklog §3 第 50 行：training sd 不在 `model_data` 中）。係數表是 Brief §3.3／§7 的選配 (4)；Brief §8 的模型解釋是 Deployment 階段內容（notebook 與報告），不是 dashboard 的必要區塊。
5. **歷史**：Brief 於 `dff7c55c` 接受時，哪些模型標準化尚未決定（Brief §4 只說「標準化參數只以當次訓練列 fit」，§12 把標準化列為 HOW）。「OLS 原始尺度、只有 Ridge／Lasso 標準化」是 Spec 的 HOW 決定，由 B-7 確認在 boundary 內。

## 4. 裁決

**R-1.1（「標準化的讀法」的對象）**：Brief §8 的「標準化／one-hot 的讀法」是 Deployment「模型解釋」的一部分，對象是**被部署與解釋的模型**，也就是最終模型（整體 CV winner 在整個 training set 上重新擬合的 OLS），不是 Ridge／Lasso 對照模型。它要求的是：讀者能正確閱讀最終模型係數所在的尺度，並能以標準化的單位比較不同單位的特徵。在 Spec 的 HOW（OLS 以原始尺度擬合）之下，這一項由兩部分組成：

- (a) 寫明最終模型以原始尺度擬合、係數以原始單位解讀，沒有需要還原的標準化；並寫明 Ridge／Lasso 的標準化只用於它們自己的擬合，不用於解讀。
- (b) 對數值欄提供以 training 標準差為單位的讀法 100·(exp(b·sd) − 1)%，sd 只來自 training set；one-hot 與旗標欄不做標準化，依相對基準或 0／1 解讀。

**R-1.2（#64 是否滿足）**：**滿足。** notebook 6.2 與 `final_model_coefficients.csv` 的 `train_sd`、`pct_per_train_sd` 完全符合 R-1.1 的 (a)、(b)（第 3 節第 1、2 點）。#64 不需要修改，也不需要補做任何 Ridge／Lasso 的讀法。R1 的 AC-1 判定（PASS）不受影響；R-1 以本紀錄結案。Dashboard 的選配係數表不需要每 1 SD 欄（第 3 節第 4 點）；之後若要加，屬 `model_data` 的修改，須另依 H-3 與 TR-01／§9.3 處理，不是本裁決的要求。

**R-1.3（Ridge／Lasso 的係數讀法：不屬任何票）**：Ridge／Lasso 標準化係數的讀法**不是** Brief §8 的義務，也不是 #64 或 #65 的義務。任何票都 MUST NOT 把 Ridge／Lasso 的係數（數值、表或圖）當作交付內容加入 notebook、報告或 dashboard：在 accepted 語義下，metric-only 模型只報 CV 與一次性 test 指標（`CONTEXT.md`；CC-1 第 5 點），只出現在比較表與圖（Q31；BR-01 第 4 點），而且報告的數字必須來自匯出結果（Spec「報告與打包」），Ridge／Lasso 的係數並沒有被匯出。對 Ridge／Lasso **方法**的說明（例如 notebook 4.3「數值欄以當次訓練列的平均與母體標準差標準化、zipcode one-hot 維持 0／1」）是方法敘述，不是係數讀法，照常保留。若之後有人希望呈現 Ridge／Lasso 的係數或其讀法，那會擴大 metric-only 模型的報告內容，屬治理 §5.3 第 1 類 contract change，MUST route 給 acceptor，不得由 Executor 或 DA 自行加入。

**R-1.4（B-7 理由欄的更正）**：B-7 的**判定不變**：OLS 用原始尺度、只有 Ridge／Lasso 標準化，在 boundary 內。B-7 理由欄後半句「Brief §8『標準化的讀法』適用於 Ridge／Lasso 的係數」**不正確，以 R-1.1 取代**：Brief §8 的標準化讀法適用於最終模型；OLS 以原始尺度擬合與它不衝突，因為 R-1.1 的 (a)、(b) 可以在原始尺度的係數上完整提供。這句原本只是 boundary 判定的理由，不是對任何票的義務；§9.1 把 B-7 列為 #64 的 DA 義務，其內容自本紀錄起是：#64 不得以標準化尺度擬合 OLS，並依 R-1.1 提供標準化的讀法。依先前紀錄的做法，`derivation-SPEC.md` 原文不改，本紀錄與 B-7 一起作為有效解讀。

**R-1.5（#65：報告版的讀法，既有義務的釐清）**：報告的「模型解釋」段落（Brief §8 報告章節清單；`decision-20261018-issue64-notebook-rerun.md` I-4）由 #65 負責，內容依 R-1.1：每單位百分比讀法、one-hot 相對基準的讀法，以及 (a)、(b) 的標準化讀法。每 1 SD 的數字與 sd 只能從 `results/tables/final_model_coefficients.csv` 的 `train_sd`、`pct_per_train_sd` 注入或引用（Spec「報告與打包」；DA TK-2），不手抄、不重算成另一套數字；報告中不得出現 Ridge／Lasso 的係數或係數讀法（R-1.3）。這是 #65 既有的 Brief §8 章節義務與數字單一來源 AC 的釐清，不是新增的義務。

## 5. 理由

- **(A) 實作的讀法 vs (B) Ridge／Lasso 係數的讀法，後果不同，但 accepted 文字可以裁決：**
  - Brief §8 的模型解釋屬於 Deployment，與 `predict_price()` 並列；老師原文是「Predict new samples and explain **the model**」。被預測、被部署、被解釋的是同一個模型。Spec 也把最終模型定為「Deployment 的預測函式、pickle 示範、診斷與報告主要結果」所用的模型。
  - Ridge／Lasso 在 accepted 語義中是對照：Q31「只在比較表與圖」，CC-1 第 5 點與 `CONTEXT.md` 的 metric-only「只報 CV 與一次性 test 指標」。讀法 (B) 會讓 metric-only 模型多出係數這一類報告內容，超出這些文字。所以 (B) 不能是 Brief §8 的意思；若要 (B)，必須由 acceptor 變更契約（R-1.3）。
  - Brief 接受時，標準化的範圍還是 HOW（Brief §4、§12）。Brief §8 的「標準化的讀法」只能指「無論最終採用哪種尺度，都要說明怎麼讀」，不可能預先指定 Ridge／Lasso。Spec 選了原始尺度之後，這項要求的內容就是 R-1.1 的 (a)、(b)。
  - 「標準化係數」在迴歸解釋中的通常意思，就是以自變數的標準差為單位的效果（目標維持原尺度時為 b·sd_x）。#64 的每 1 SD 讀法正是這個量，而且所用的母體標準差與 Ridge／Lasso 自己的標準化慣例相同（第 3 節第 2 點），兩者沒有矛盾。
- **為什麼要更正 B-7 的理由，而不是只說「兩種都可以」**：#65 的報告會依 §9.1 與 B-7 撰寫。若 B-7 的那句話保持原樣，#65 可能被讀成必須說明 Ridge／Lasso 的係數，而這些係數沒有匯出，報告的單一來源規則無法滿足，也會與 metric-only 衝突。明確更正可以避免把一個不存在的義務帶進後面的票。
- **為什麼 #64 不需要改**：R-1.1 的兩部分都已經在 notebook 6.2 與追蹤的 CSV 中，並已由 R1 獨立重算。

## 6. Accepted 語義與 boundary

- **不改變 accepted 語義**。這是治理 §5.3 第 2 類：對 derived contract（`derivation-SPEC.md` B-7 的理由與 §9.1 的 #64 義務、ticket #64、#65 的文字）的 clarification。Brief §8 的要求原樣保留並得到具體內容（R-1.1）；Ridge／Lasso 的 metric-only 範圍原樣保留（R-1.3 只是重述其界線）。沒有新增或移除任何 requirement、AC、invariant 或 gate。
- **Boundary**：在 Outcome Contract boundary 內。不需要 acceptor，也沒有接受或授權缺口。唯一可能需要 acceptor 的情況，是有人要加入 Ridge／Lasso 的係數呈現（R-1.3）；本裁決不要求、也不容許任何票這樣做。
- **不需要重新評估**：本紀錄不要求執行 `hw2.run_notebook`，也不要求改動 `results/`、`assets/model_data.*`、`hw2/`、notebook 或測試。

## 7. 對各工作的要求

| 對象 | 要求 | Owner |
| --- | --- | --- |
| #64 | 不需要修改（R-1.2）。R-1 由本紀錄結案；R1 的 VERDICT: CLOSURE 與 AC-1 判定不受影響 | — |
| #65 | 報告的模型解釋段落依 R-1.5；不呈現 Ridge／Lasso 的係數或係數讀法（R-1.3） | #65 Executor；#65 R1 核對 |
| #67、Spec Integration Audit | 核對報告的標準化讀法來自 `final_model_coefficients.csv`，且報告、notebook、dashboard 都沒有 Ridge／Lasso 係數 | #67 R1；Spec Integration Audit（A-5 範圍內） |
| Orchestrator | 派 #65、#67 與 Spec Integration Audit 時，把本紀錄放進 bounded pack | Orchestrator |

**建議的票文字**（我不修改票，由派工者逐字附加；不附加也不影響本紀錄的效力）：

#65，在 AC 最後：

```markdown
- [ ] （DA `decision-20261018-issue64-standardized-reading.md` R-1.1、R-1.3、R-1.5）報告的模型解釋段落對最終模型提供每單位百分比、one-hot 相對基準，以及標準化的讀法：寫明 OLS 以原始尺度擬合、Ridge／Lasso 的標準化只用於它們自己的擬合；數值欄每增加 1 個 training 標準差的百分比與 sd 只從 `results/tables/final_model_coefficients.csv` 的 `pct_per_train_sd`、`train_sd` 引用。報告不呈現 Ridge／Lasso 的係數或係數讀法。
```

#64：不需要修改票文字。

## 8. 受影響的工作與 evidence

| 對象 | 影響 |
| --- | --- |
| `derivation-SPEC.md` B-7、§9.1 | B-7 判定不變；理由欄後半句由 R-1.4 更正；原文不改，本紀錄與 B-7 一起作為有效解讀 |
| #64 的 evidence（`003b825`、worklog、R1 record） | 有效，不需要補做。R1 的 R-1 routing 由本紀錄回答 |
| #65～#67、Spec Integration Audit | 依第 7 節 |
| Spec rev 5、Brief、Outcome Contract、tickets、程式、notebook 與結果檔 | 不修改 |
| 高風險 | H-4（標示與解釋的誠實：報告不出現沒有匯出來源的係數數字，R-1.3、R-1.5）；H-3 不受影響（不讀任何 test 結果） |

## 9. Evidence

- 讀取：Bindings b5（§3.2 E-DA）；治理 v2.2 §1.2、§2.4、§2.5、§3.6、§4.2、§5.3；`audit/issue-64-c1-r1.md`（全文，含 §7 R-1）；`outcome-contract.md`（CC-1、AD-1～AD-3）；`BRIEF.md` §3.2、§4、§5、§7、§8、§12（含 `dff7c55c` 版本的 §4、§8、§12）；Grill 紀錄 rev 7 的 Q9、Q20、Q25、Q31、Q33；`CONTEXT.md`（現行版與 `dff7c55c` 版，以及 `84fe922` 對「Metric-only model」的新增）；`SPEC.md` rev 5（前處理、特徵選擇與模型、診斷與解釋、`model_data`、Dashboard、報告與打包）；`derivation-SPEC.md` §3 B-7、§9.1、§9.4；`decision-20261018-issue64-notebook-rerun.md`；`worklog/issue-64.md`；GitHub issues #64、#65；老師原文 SRC-2T 的 Deployment 條。
- 核對：`git show 003b825:home_work_02/hw2.ipynb` 的 cell 14、24、29、46、58～60、69；`git show 003b825:home_work_02/hw2/explain.py` 的 `coefficient_table`；`results/tables/final_model_coefficients.csv` 的欄名。
- 沒有執行 notebook、`hw2.run_notebook` 或任何會載入正式 test 列的程式。寫入的檔案只有本紀錄；沒有修改程式、測試、notebook、Spec、Brief、Outcome Contract、票或其他紀錄；沒有 commit 或 push。

## 10. Required authority

無。本裁決在 DA 權限內，不改變 accepted 語義，不需要 acceptor，不需要重新評估，也不需要 escalation。只有在有人提議呈現 Ridge／Lasso 的係數時（R-1.3），required authority＝acceptor（治理 §5.3 第 1 類）。
