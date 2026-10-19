# Decision record — #65 C-1（dashboard 的標示）與 C-2（缺少的結果圖 PNG）

- **紀錄類型**：Design Authority decision record（治理 §2.4、§3.6、§5.3 第 2 類；Bindings b5 §7）
- **日期**：2026-10-19
- **Run**：`run-20261018-hw2-formal`。#65 Executor 對 C-1、C-2 指明 Design Authority，Orchestrator 依治理 §2.4 直接派工（run record §15）。
- **問題來源**：`doc/governance/worklog/issue-65.md` §6 C-1、C-2。Worklog 的敘述只當作待驗證的主張，下文的事實是我自己核對的（第 2 節）。
- **受審 subject**：branch `home_work_02-regrill`，#65 implementation commit `741a21ba29dfb5ad7a2c2d1ac2f02d5eeb20035d`（base `bc56c06`）；撰寫時 HEAD＝`fbd7dec`（之後只有 record-only commit）。
- **Binding**：`gov-design-authority`，`claude-opus-5-5`／`high`（Bindings 預設 mapping，沒有 escalation，也沒有替代）。本紀錄不自證 binding，由派工者依 Bindings §3.6 核對。
- **Capability escalation**：不提出。E-DA/D1 不成立：C-2 的兩種處理（維持現況或補一張靜態圖）後果不同，但 Brief 1d、Q7 與 Brief §8 足以裁決（第 4.2 節）。C-1 只有一種讀法與 accepted 語義相容。E-DA/D2 不成立：C-2 涉及我在 `derivation-SPEC.md` §9.5 TK-2 的分配，但質疑來自 Executor 的 concern，不是 FA ruling 或經 route 的 Reviewer finding；本紀錄補足那項分配，不是推翻它。
- **約束**：acceptor 2026-10-18 的回覆（run record §14）：「請繼續既有 Implementation 流程，不新增功能、不重開設計決策。」以及 CC-1、`decision-20261018-issue64-notebook-rerun.md`（N-1～N-6、§9.3 條件 7、8）。

## 1. 問題

1. **C-1**：互動 dashboard 在三種標示（老師要求／依老師補充建議／專案延伸）中應該標哪一種？報告現在標「老師要求（課堂口頭；作業頁正文沒有）」，而 dashboard 頁面「方法與限制」區塊的圖例把「老師要求」定義為「作業頁正文的要求」。
2. **C-2**：`results/figures/` 沒有 (a) 各方法 k 路徑的 CV RMSE 圖、(b) 實際 vs 預測＋逐筆 PI 的預測圖、(c) Ridge／Lasso 的 alpha CV 曲線；notebook 完全沒有 (b)。要決定：這是否違反已接受的契約（含老師的「預測圖加上區間」與 Q43）；誰負責修正；如何在不做第二次正式 Test 評估的情況下修正。

## 2. 我自己核對的事實

1. **Dashboard 的圖例**（`index.html:247`）：「〔老師要求〕作業頁正文的要求；〔依老師補充建議〕作業頁『補充』段的建議，本專案採用；〔專案延伸〕本專案自行加入的設計，不是老師的要求。」dashboard 上用到「老師要求」的只有「特徵選擇方法」（`index.html:250`）與「預測區間的統計假設」（`:260`），兩者都是作業頁正文的書面要求。**dashboard 沒有替自己加任何標示。**
2. **報告**（`report/report.md:9`）把〔老師要求〕定義為「作業頁正文的書面要求。唯一的例外是互動 dashboard：它是老師的**課堂口頭要求**……一律註明『課堂口頭』」；對照表（`:28`）、§7.1、§9 的標題都帶「課堂口頭」。`README.md:9` 寫「課堂口頭要求的互動 dashboard」；`ACCEPTANCE.md:6`、B-1 寫明 dashboard 不是作業頁的書面要求。
3. **`results/figures/`**（`741a21b`）只有 7 張 PNG：5 張診斷（`diag_*`）與 2 張解釋（`explain_*`），都由 #64 的 notebook 5.6、6.2 寫出。
4. **Notebook**（71 個 cell）：4.2 的 cell 28 與 4.3 的 cell 31 有 k 路徑與 alpha CV 的內嵌圖，只 `plt.show()`、沒有存檔。第 5 章（cell 34–57）沒有任何預測圖：5.5 的 cell 44 是比較表，cell 45 只印出涵蓋率的文字。Cell 0–45 的 source 與 `052984b`（唯一一次正式評估的 commit，當時 47 個 cell，cell 46 是第 6 章的佔位）完全相同。
5. **報告怎麼呈現 (b)**：§6.3〔老師要求〕逐字引用正文「結果部分需包含請提供預測圖(加上信賴區間或預測區間)」，然後寫「預測圖見第九章的 dashboard 截圖」；第九章〔老師要求（課堂口頭）〕的截圖（`shot:test`）是建置時以 headless 瀏覽器開啟 `index.html` 擷取，不在 `results/` 內。(a)(c) 在報告 §5.1、§5.2 以 CSV 注入的表呈現（`{{table:kpath}}`、`{{table:alpha}}`）。`ACCEPTANCE.md` A-3 的證據只有 dashboard 與截圖。
6. **正式產物沒有改動**：`git diff --quiet 052984b HEAD -- results/model_data.json assets/model_data.js` 無差異。`results/model_data.json` 的 `test` 已含每個 `ols_subset` 模型的逐筆 `predicted`、`lower`、`upper`、`covered`，以及 `coverage`、`n_covered`、`n_test`；`test_inputs` 含 `actual_price`。授權集合是 `allin`、`forward_sfs_k17`（整體 CV winner `lasso_path_k17` 與 `backward_sfs_k17` 共用後者；notebook cell 41、47 的輸出）。
7. **既有的存檔模式**：`hw2/diagnostics.py` 的 `save_figures` 以 `metadata={"Software": None}` 存檔，並由 `check_output_dir` 拒絕非正式資料寫入單元內；圖用英文標籤，避免 CJK 字型依賴（`diagnostics.py:407`）。
8. **Ticket 分配**：`derivation-SPEC.md` §9.5 TK-2 只把「比較表與 test 指標表的 CSV」分給 #63、「診斷與解釋圖的 PNG」分給 #64；#63 的 TK-2 AC 也只要求 CSV。**k 路徑圖、預測圖、alpha 曲線的 PNG 沒有分給任何一張票。**

## 3. 依據

| 來源 | 內容 |
| --- | --- |
| 作業頁正文 SRC-1／SRC-2T | 「結果部分需包含請提供預測圖(加上信賴區間或預測區間)」；繳交內容是主程式與 PDF 報告；評分「預測結果評估(預測圖、評估指標)（10%）」 |
| Grill 紀錄 rev 7，Frontier 1 | 1b：「老師有要求（有出處）」「報告將標『老師要求』」；出處：「Dashboard 的要求來自老師課堂上的口頭說明。」「不得宣稱作業 PDF 或講義明文要求網站。」1d：「網站是額外的交付，主程式 .py/.ipynb、PDF 報告、學號 ZIP 照老師正文都要交。」「網站不取代任何老師正文的必交項目」 |
| Brief §2、§3.1、§3.2 | §2：dashboard 是課堂口頭要求，「報告不得宣稱有」書面要求；§3.1 T-預測圖 →「95% 預測區間，§6、§7 [D Q3、Q43]」；T-CRISP-DM：「notebook 與報告各有六章」；§3.2 標題「必要（課堂口頭要求＋acceptor 決定）」 |
| Brief §7 Q43 | 實際 vs 預測圖的編碼：x＝Predicted、y＝Actual、log、y＝x、每筆垂直 PI 線段、依是否落入著色；全部 test 樣本、不抽樣不聚合；PI 與 Python 匯出一致 |
| Brief §8、Q7、Q24、Q26 | 結果產物「結果表 CSV、圖 PNG」；Notebook「為主要可重現分析程式及 Dashboard 資料產生來源」；報告「數字與圖全部引自匯出結果，不手抄」 |
| Spec rev 5「單元結構與交付物」「報告與打包」 | 結果目錄（CSV、PNG、`model_data`）；「Notebook 是主程式與唯一的數字來源：它呼叫套件、產生全部結果檔」；報告的數字與圖從匯出結果注入或引用；三種標示以對照表＋章節標示 |
| `derivation-SPEC.md` §4、§9.5 TK-2 | T-預測圖 → 預測區間＋dashboard 圖；TK-2 的 PNG 分配（第 2 節第 8 點） |
| `decision-20261018-issue64-notebook-rerun.md` | N-1（重現不是第二次評估）、N-3（#67 的單一次完整執行；PNG、CSV 必須與追蹤檔相同）、N-4（#65 不重跑；必要時部分執行）、§9.3 條件 4、7(b) |
| Ticket #65 AC（DA TK-2） | 「報告引用的每張圖與每個表都對回結果目錄中的 PNG／CSV；缺少者視為 #63／#64 的缺口回報」 |

## 4. 裁決

### 4.1 C-1：dashboard 標「老師要求（課堂口頭）」，維持 #65 的做法，不需修改

- **L-1**：報告、README、ACCEPTANCE.md 對 dashboard 的標示維持現況：「老師要求」，並在每一處註明「課堂口頭；作業頁正文沒有」。這是唯一同時符合 accepted 語義兩條約束的讀法：Grill 1b 明定「報告將標『老師要求』」，Brief §2 禁止宣稱書面要求。「專案延伸」不採用：它與 1b、Brief §3.2「必要」相反，也與 dashboard 圖例自己的定義（「不是老師的要求」）衝突。
- **L-2**：dashboard 圖例與報告的定義**不衝突，不需要修改 `index.html`**。圖例只說明頁面上出現的標示，而頁面上的「老師要求」只用在作業頁正文的項目；dashboard 從不替自己標示。報告的定義以同樣的書面要求為主，再把唯一的例外寫明。兩者在每個實際標示的項目上給出同樣的結論。改寫圖例不是必要，而且會動到已審查的 dashboard（H-2），依 acceptor 回覆 §14 不做。
- **L-3**：#65 R1 依 H-4（A-1）核對報告每一處提到 dashboard 的地方都帶「課堂口頭」，沒有一處把它寫成作業頁或講義的書面要求。這是本裁決要核對的內容，不是新的 finding。

### 4.2 C-2：(b) 是缺口，(a)(c) 不是

**F-1（(b) 實際 vs 預測＋PI 的預測圖：是缺口）**

判定：老師的「預測圖加上區間」目前只靠 dashboard 滿足。主程式 notebook 沒有這張圖；報告 §6.3〔老師要求〕把讀者轉到第九章〔課堂口頭〕的 dashboard 截圖，所以 PDF 裡唯一的預測圖也是 dashboard 的擷取畫面。依 1d，dashboard 是額外交付，「不取代任何老師正文的必交項目」。所以老師正文要求的結果，必須在老師要求的交付物（主程式與報告）中就能成立，不能依賴課堂口頭要求的那一項。檢驗方式：把 dashboard 拿掉，主程式與報告是否仍有預測圖？目前沒有。另外 Brief §8／Q7／Spec 要求 notebook 產生全部結果檔、報告的圖引自匯出結果；結果產物列有「圖 PNG」，但最核心的這張圖沒有 PNG。

缺口的層級：**Brief 的 accepted 語義本身沒有缺漏**（T-預測圖、Q43、§8 都已涵蓋），缺的是 derived contract：我在 `derivation-SPEC.md` §9.5 TK-2 的 PNG 分配漏了這張圖，所以沒有任何票被要求產出它。**這不是 #63 的缺陷**：#63 的 TK-2 AC 只要求 CSV，它的 closure 與 evidence 不受影響。

**F-2（(a) k 路徑圖、(c) alpha CV 曲線：不是缺口，不補做）**

老師要求的是「必須執行特徵選擇與模型評估」，沒有要求這兩張圖。主程式在 4.2、4.3 已有內嵌圖；報告 §5.1、§5.2 以 `results/tables/` 的 CSV 注入表格，符合 TK-2「每張圖與每個表都對回 PNG／CSV」。拿掉 dashboard 之後，必交項目仍然完整。補做這兩張 PNG 是新增產物，依 acceptor 回覆 §14 不做；而且 cell 28、31 在凍結範圍內（§9.3 條件 7(b)），MUST NOT 為了存檔而修改。第九章的 `shot:compare` 是 Brief Q42「dashboard 連結與截圖」的內容，不需要 PNG。

**F-3（負責的票：#65，以 targeted correction 在 R1 之前完成）**

`derivation-SPEC.md` §9.5 TK-2 由本紀錄補充：**實際 vs 預測＋逐筆 PI 預測圖的 PNG 分給 #65**。#63、#64 已結案，不重開。理由：#65 是唯一仍在進行、並且引用這張圖的票（報告 §6.3、ACCEPTANCE A-3）；修正只讀已匯出的結果，不碰 #63 的評估路徑。Orchestrator 以 SendMessage 續派同一位 #65 Executor（同一份 worklog），完成後才派 #65 R1，R1 的 subject 是修正後的 commit。

**F-4（要做的事，全部在 `home_work_02/` 內）**

1. **繪圖程式**：新增一個繪圖函式，放在 §9.3 條件 7(b) 列出的模組（`data`、`split`、`preprocess`、`selection`、`models`、`comparison`、`ols`、`metrics`、`contract`、`testgate`、`export`）**之外**，可以新增模組或放在 `deployment`／`diagnostics`／`explain` 中，`paths.py` 可以加常數。輸入只能是 `model_data` 物件：`test[key]` 的 `predicted`、`lower`、`upper`、`covered`、`coverage`、`n_covered`、`n_test`，加上 `test_inputs` 的 `actual_price`。編碼沿用已接受的 Q43：x＝預測、y＝實際、log 刻度、y＝x 參考線、每筆一條垂直 PI 線段、依 `covered` 著色、**全部 `n_test` 筆，不抽樣、不聚合**。對象是 `winners.authorized_test_models` 的每個鍵（目前是 `allin`、`forward_sfs_k17`）；每個面板或檔案標明方法與 k，並依 D-2／D-3 列出共用同一模型的 CV winner（整體 winner `lasso_path_k17`、`backward_sfs_k17`）。標題或說明中的涵蓋率與筆數直接取自匯出欄位，不重新計算任何指標。PNG 的文字不得缺字（建議比照 `diagnostics.py` 用英文標籤；產生時不得出現 matplotlib 的「Glyph … missing」警告）。存檔比照 `diagnostics.save_figures`（`metadata={"Software": None}`）。寫入 `results/figures/` 時必須拒絕 fixture 或非正式資料（TR-01、§9.3 條件 4）；具體做法由 Executor 決定，例如比照 `hw2/report.py`，要求 `export.result_digest(model_data)` 等於 `b53ff286ae0734add8b272089aba904a1cb7f5aca444a62d356420b25dc3cfc6`。
2. **Notebook**：在 cell 45 之後、5.6 標題（cell 46）之前插入新的 cell（說明 markdown＋code），呼叫上述函式、顯示並存檔。**Cell 0–45 的位置與 source 不變。**本紀錄澄清 §9.3 條件 7(b) 的「5.5 節以前各 cell」：指 `052984b` 時已存在的 cell 0–45；插入在其後的新 cell 不屬於凍結範圍，但仍受本節第 3 點約束。新 cell 使用 cell 41 在同一 kernel 產生的 `model_data`，與 cell 44、45 一致；或從 `results/model_data.json` 讀取。兩種寫法在 #67 的完整執行中都會得到同一份資料。
3. **執行方式（N-4，部分執行）**：任何 cell 執行前，先在 process 內把 `OFFICIAL_TEST_GATE_ENABLED` 設為 False；**不執行** cell 41、42、44、45，保留它們的 #63 輸出。若新 cell 需要 `model_data`，以追蹤的 `results/model_data.json` 綁定，並先確認 `result_digest`＝`b53ff286…`、manifest 的 `selection_digest`＝`44f7723e4023afc3e8e997f42bf4eb59db392af81cced11743757a9857cb4b28`。只執行新 cell 與它需要的 import／helper；5.6 以後的 #64 輸出不需要重跑。Notebook 暫時含有三次執行的輸出，依 N-2 屬於過渡狀態，在 #67 由單一次完整執行取代（N-3）。
4. **報告**：§6.3 以 `![…](fig:<新檔名>)` 直接引用新的 PNG，取代「預測圖見第九章的 dashboard 截圖」；第九章的截圖保留。`hw2/report.py` 的 `FIGURES` 清單納入新檔，`tests/test_report.py` 的「每張 PNG 都被引用」照常成立。§6.3 的標示不變：〔老師要求；涵蓋率驗證為專案延伸〕。
5. **ACCEPTANCE.md A-3**：證據改為 notebook 的新 cell、`results/figures/` 的新 PNG、報告 §6.3，以及 dashboard 與第九章截圖，狀態仍是 PENDING。README 若有列出結果檔，同步更新。
6. **測試**：pytest 至少涵蓋三點：(i) 以 fixture 的 `model_data` 呼叫時不寫入單元內；(ii) 圖中的 PI 線段數與點數等於 `n_test`，著色與 `covered` 一致；(iii) 函式不呼叫 `testgate`、不讀資料 CSV、不擬合也不評分。具體寫法由 Executor 決定。

**F-5（為什麼這不是第二次正式 Test 評估）**

依 N-1，「評估」是在選擇固定後對授權集合計算 test 結果的那個決定事件。這次修正只把 #63 那一次評估已經匯出的逐筆結果畫成圖，與 dashboard、`hw2/report.py` 讀取同一份匯出結果的方式相同：不開守門、不呼叫 `gate.evaluate`、不從資料 CSV 載入正式 test 列、不擬合、不評分、不產生新的 test 數字，也不回饋任何選擇（CC-1 第 3、4 點）。Executor 必須以下列可核對的條件證明這一點，並記入 worklog；R1 依 A-2 自行重做：

- `results/model_data.json`、`assets/model_data.js`、`results/tables/*.csv`、既有 7 張 PNG 的 sha256 都與 `741a21b` 相同；`export.result_digest`＝`b53ff286…`。
- `git diff 052984b -- home_work_02/hw2/{data,split,preprocess,selection,models,comparison,ols,metrics,contract,testgate,export}.py home_work_02/requirements.txt` 沒有差異；notebook cell 0–45 的 source 與 `052984b` 相同。
- 沒有執行 `hw2.run_notebook`、cell 41、42、44、45，也沒有任何 process 以開啟的守門執行。
- **決定性**（N-3 的前提）：在兩個獨立的 process 中各產生一次新 PNG，兩者 byte-identical，並記錄 sha256。#67 的完整重跑會再產生它，依 N-3 必須與追蹤版相同；不同時依 N-3 停止並 route 給 DA。

### 4.3 對 #67 與 Spec Integration Audit 的影響

- 新的 PNG 屬於 N-3 的「PNG 必須相同」，也屬於 #67 TK-2 的「ZIP 內含結果目錄的 CSV 與 PNG」。不需要新增條款。
- #67 的 §9.3 條件 7(b) 前置核對依第 4.2 節 F-4 第 2 點的澄清執行（cell 0–45）。

## 5. Accepted 語義與 boundary

- **C-1：不改變 accepted 語義。**這是對 Spec「三種標示」的 clarification（治理 §5.3 第 2 類），只確認 Grill 1b 與 Brief §2 的既有規定。
- **C-2：不改變 accepted 語義。**這是治理 §5.3 第 2 類：補足 derived contract 的 Ticket 分配（TK-2），並澄清 §9.3 條件 7(b)。T-預測圖、Q43、Brief §8 的「圖 PNG」與 1d 都是已接受的內容。修正是把已接受的 Q43 圖在必交項目中以靜態方式呈現，沒有新增 requirement、scope 或 AC 語義，也不改變 dashboard、Q43 或任何設計決定。所以它符合 acceptor 回覆 §14「不新增功能、不重開設計決策」。(a)(c) 不補做，正是因為它們會是新增產物。
- **Boundary**：兩項都在 Outcome Contract boundary 內。不需要 acceptor，沒有接受或授權缺口，也不需要 escalation。
- **不需要重新評估**（F-5）。

## 6. 受影響的工作與 evidence

| 對象 | 影響 |
| --- | --- |
| #65 | C-1：不需修改（L-1、L-2），R1 依 L-3 核對。C-2：依 F-3、F-4 做 targeted correction，然後才派 R1。R1 依 A-1 寫明觸及的 H-2（主程式 notebook、報告的預測圖）、H-3（只讀匯出結果、正式產物不變、凍結範圍不變；A-2 自行重做 F-5 的核對）、H-4（§6.3 的圖引自 `results/figures/`、標示、沒有 mock 或 wireframe；A-5） |
| #63 | 不受影響；closure 與 `worklog/issue-63.md` §5 的權威紀錄不變。Executor 稱之為「#63 缺口」，本紀錄更正為 TK-2 分配的缺口（F-1） |
| #64 | 不受影響 |
| #66 | 無 |
| #67 | 第 4.3 節 |
| `derivation-SPEC.md` §9.5 TK-2、§9.3 條件 7(b) | 由本紀錄補充與澄清，原文不改 |
| Spec rev 5、Brief、Outcome Contract、Tickets | 不修改 |
| Orchestrator | 依 F-3 續派 #65 Executor，把本紀錄放進 pack。可以把下面這行逐字附加到 #65 的 AC（不附加也不影響本紀錄的效力）：`- [ ] （DA decision-20261019-issue65-labels-figures.md F-1～F-5）notebook 在 cell 45 後新增實際 vs 預測＋逐筆 95% PI 的圖並存成 results/figures/ 的 PNG（只讀匯出的 model_data，Q43 編碼、全部 n_test 筆），報告 §6.3 直接引用；不重新評估、不改 cell 0–45 與條件 7(b) 的模組、正式產物 sha256 不變、PNG 可決定性重現。` |

## 7. 觀察（不是本紀錄的裁決）

- **O-1**：notebook cell 28（4.2 的 k 路徑內嵌圖）的輸出有 matplotlib 的「Glyph 36335／24465 … missing from font(s) DejaVu Sans」警告，也就是圖例中「Lasso 路徑排序」的中文字顯示為缺字。這個 cell 在凍結範圍內（條件 7(b)），本紀錄不要求、也不授權修改。交 #65 R1 與 #67 的 notebook 人工檢查（ACCEPTANCE A-4）判斷是否構成 finding；若需要修正，先 route 給 DA，因為它會動到 cell 0–45 或它們依賴的設定。
- **O-2**：Executor 的 C-4（dashboard「指標 vs k」圖在 1280 px 截圖中沒有 k 的刻度）不在本次問題範圍內，照 Executor 的安排交 #67。

## 8. Evidence

- 讀取：Bindings b5（§2、§3.2、§7）；治理 v2.2 §5.3；`run/run-20261018-hw2-formal.md`（§1、§12–§15）；`worklog/issue-65.md`；`outcome-contract.md`（CC-1、AD-1～AD-3）；`BRIEF.md` §2、§3、§7、§8、§10；`HW2_Regrill_Brief_Draft_v0.1.md` Frontier 1、Q3、Q5、Q7、Q24、Q26、Q42、Q43；`doc/requirement/` 的 SRC-1 與 SRC-2T 轉寫；`SPEC.md` rev 5（User Stories 9、15；單元結構與交付物；Dashboard；報告與打包；人工檢查表）；`derivation-SPEC.md` §4、§9.1、§9.3、§9.4、§9.5；`decision-20261018-issue64-notebook-rerun.md`；`decision-20261018-high-risk-categories.md`（H-2～H-4、A-1～A-8）；GitHub issues #63、#65、#67；`index.html`（圖例與標示）；`report/report.md`（標示、§5、§6、§9）；`hw2/report.py`（`FIGURES`、`fig:`／`shot:`）；`hw2/diagnostics.py`（存檔與輸出目錄守門）；`README.md`；`doc/acceptance/ACCEPTANCE.md`（A-3、B-1）。
- 執行：`git diff --stat bc56c06 741a21b`；以單元 `.venv` 列出 `hw2.ipynb` 每個 cell 的類型、執行序號與 PNG 輸出數，並讀取 cell 28、31、41、43–45、47、59、63 的 source 與輸出；`git show 052984b:home_work_02/hw2.ipynb` 與現行版比對（`052984b` 有 47 個 cell；cell 0–45 的 source 相同）；`git diff --quiet 052984b HEAD -- results/model_data.json assets/model_data.js`（無差異）；`results/figures/*.png` 的 sha256。
- 沒有執行 `hw2.run_notebook` 或任何會載入正式 test 列的程式。寫入的檔案只有本紀錄；沒有修改程式、測試、notebook、Spec、Brief、Outcome Contract、票或其他紀錄；沒有 commit。

## 9. Required authority

無。兩項裁決都在 DA 權限內，不改變 accepted 語義，不需要 acceptor，不需要重新評估，也不需要 escalation。執行 F-4 的是 #65 Executor（Orchestrator 派工），審查是 #65 R1。
