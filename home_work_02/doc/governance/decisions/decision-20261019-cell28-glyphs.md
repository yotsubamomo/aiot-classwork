# Decision record — #65 R1 F-4／DA O-1：notebook cell 28 圖例缺字

- **紀錄類型**：Design Authority decision record（治理 §2.4、§3.6、§5.3 第 2 類；Bindings b5 §7）
- **日期**：2026-10-19
- **Run**：`run-20261018-hw2-formal`。#65 R1（`audit/issue-65-c1-r1.md` F-4、§7）指明修正前須由 Design Authority 裁決；Orchestrator 依治理 §2.4「已指明 authority，且與本節規則一致」派工（run record §15 最後一點：#67 派工前的前置事項）。
- **問題來源**：`audit/issue-65-c1-r1.md` F-4；我在 `decision-20261019-issue65-labels-figures.md` §7 的 O-1。兩者的敘述只當作待驗證的主張，下文的事實是我自己核對的（第 2 節）。
- **受審 subject**：branch `home_work_02-regrill`，撰寫時 HEAD＝`743441e`；`hw2.ipynb` 在工作樹的版本（73 個 cell）。比對基準：唯一一次正式評估的 commit `052984ba21568499aad4b02e6ba8c564901e8c76`。
- **Binding**：`gov-design-authority`，`claude-opus-5-5`／`high`（Bindings 預設 mapping，沒有 escalation，也沒有替代）。本紀錄不自證 binding，由派工者依 Bindings §3.6 核對。
- **Capability escalation**：不提出。E-DA/D1 不成立：「修正」與「不修正」兩種處理的後果可以用現有證據裁決（第 4 節 G-1、G-2）；可行的修正方式只有一種同時符合凍結條件與 N-3（第 4 節 G-3），沒有兩個後果不同、證據無法分辨的設計。E-DA/D2 不成立：O-1 是觀察，不是裁決；Reviewer F-4 與它一致，沒有推翻或爭議。
- **約束**：CC-1；`decision-20261018-issue64-notebook-rerun.md` N-1～N-6、§9.3 條件 7、8；acceptor 2026-10-18 回覆（run record §14），特別是第 3 點（#67 以 digest／manifest 比對資料、split／fold、winner、alpha、授權模型集合、Test 預測與指標）與結語「不新增功能、不重開設計決策」。

## 1. 問題

1. Cell 28 圖例的缺字是否必須修正。
2. 在凍結範圍（cell 0–45；§9.3 條件 7(b)，經 `decision-20261019-issue65-labels-figures.md` F-4 第 2 點澄清）與單次評估的約束下，修正是否被允許。
3. 若允許：確切能改什麼、由誰改，以及它對凍結範圍比對與 #67 重現核對的影響如何處理。

## 2. 我自己核對的事實

1. **Cell 28 的內容**（工作樹與 `052984b` 的完整 JSON 相同，含輸出；cell id `2fc16ee1`，執行序號 18）：`import matplotlib.pyplot as plt`，接著畫 4 種 k 路徑方法的訓練 CV RMSE 對 k 的折線與 All-in baseline 水平線，只 `plt.show()`，不存檔。圖例標籤來自 `label=models.METHOD_LABELS[m]`。軸標題、軸標籤與標題都是英文。
2. **缺字的範圍**：stderr 有 4 個警告，`Glyph 36335`（路）、`24465`（徑）、`25490`（排）、`24207`（序）`missing from font(s) DejaVu Sans`。也就是 `models.METHOD_LABELS["lasso_path"]`＝`"Lasso 路徑排序"` 在圖例中顯示為「Lasso □□□□」。其他三個方法（`Forward SFS`、`Backward SFS`、`RFE`）與 `All-in baseline` 是 ASCII，正常。整份 notebook 的輸出中，只有 cell 28 有「Glyph … missing」警告。stderr 的內容還帶有本機的絕對路徑（`D:\nchu\…\.venv\Lib\site-packages\IPython\core\pylabtools.py`）。
3. **為什麼不能改 `models.METHOD_LABELS`**：`hw2/models.py` 是 §9.3 條件 7(b) 的凍結模組；而且這個字串經 `hw2/selection.py:85` 寫進 `results/model_data.json`（出現 1 次）、`assets/model_data.js`，也出現在 `index.html`、`assets/app.js`。改它會改變 `model_data`，違反 N-3「`model_data` 的其他內容必須相同」，也會改到已審查的 dashboard。
4. **Cell 28 與後續 cell 的關係**：之後的 cell 沒有讀取 cell 28 的圖或 `colors`；`fig`、`ax` 在 cell 31 重新指定；`m`、`cands` 在 cell 35、37、41 是各自迴圈的變數，重新綁定。Cell 28 唯一被後續依賴的是 `import matplotlib.pyplot`：完整執行時，inline backend 的 PNG formatter 由它啟用，cell 47 的 `display(pred_fig)` 依賴這一點（#65 R1 §8 第 1 點；`tests/test_prediction_plot.py:115-129`）。Cell 28 在 4.2 節，位於選擇與評估路徑上游的 cell 之後、不寫任何檔案，也不設定 matplotlib 的全域狀態（`rcParams`、style、字型）。
5. **既有的慣例**：`hw2/diagnostics.py:407` 與 `hw2/prediction_plot.py:31` 的圖都用英文標籤，以避免 CJK 字型依賴；後者把同一方法標為 `"Lasso path ranking"`（我在 `decision-20261019-issue65-labels-figures.md` F-4 第 1 點要求的做法）。
6. **測試**：`tests/` 沒有任何測試讀取 cell 28 或把 notebook 的 cell 與 `052984b` 比對。
7. **契約**：「zh-TW 無缺字」的明文只針對 dashboard（Brief §7 BR-04 的必須正常、§10；Spec US-60、人工檢查表；ACCEPTANCE D-2、OV-1）。Notebook 是主程式與評分對象（SRC-1「結果合理、美觀且具有說服力（15%）」；Brief §3.1 T-CRISP-DM、§8：繳交的 `<學號>_hw2.ipynb` 由 `hw2.ipynb` 產生）。Brief §12 把「診斷的具體統計量與圖」等列為 HOW。

## 3. 依據

| 來源 | 內容 |
| --- | --- |
| SRC-1（作業頁正文） | 必須執行特徵選擇；評分「結果合理、美觀且具有說服力（15%）」；繳交主程式 |
| Brief §3.1、§5、§8、§12 | T-CRISP-DM（notebook 六章）；特徵選擇方法的比較；notebook 是繳交的主程式、單一來源；圖的細節屬 HOW |
| OC §4 CC-1 | 只有一次最終 Test 評估，test 結果不回饋選擇 |
| `decision-20261018-issue64-notebook-rerun.md` | N-1（重現不是第二次評估）、N-3（單一次完整執行是交付物的唯一來源；允許的差異）、N-4、§9.3 條件 7（重跑前的前置核對；(b) 有差異時先 route DA 判定是否影響評估）、條件 8 |
| `decision-20261019-issue65-labels-figures.md` | F-4 第 1 點（圖用英文標籤、不得有「Glyph … missing」）、第 2 點（凍結範圍＝`052984b` 的 cell 0–45）；O-1 |
| `audit/issue-65-c1-r1.md` F-4 | Low、non-blocking，owner #67，修正前須 route DA |
| Acceptor 回覆（run record §14） | 第 3 點的 digest／manifest 比對；「不新增功能、不重開設計決策」 |
| Ticket #67 | 乾淨環境完整重跑；ACCEPTANCE 全部填寫（含 A-4 的 notebook 人工檢查） |

## 4. 裁決

### G-1：必須修正，由 #67 負責

缺字使 4.2 節唯一一張比較 k 路徑方法的圖，無法從圖例辨認 4 條方法曲線中的一條，而那一條正是整體 CV winner（Lasso 路徑排序 k = 17）所屬的方法。這張圖在繳交並評分的主程式中，用途就是比較各方法；圖例認不出其中一條，圖就沒有達成自己的用途。此外，目前的 stderr 會把 4 個警告與本機絕對路徑帶進 `<學號>_hw2.ipynb`。

沒有任何明文 AC 被違反（「無缺字」的明文只針對 dashboard），所以這不是 #65 或任何已結案票的缺陷，也不追溯影響它們的 closure。但它是主程式交付物的已知缺陷，修正的成本與風險都很低（G-2、G-3），而 #67 的單一次完整執行本來就會重新產生 cell 28 的輸出。因此我把它定為 **#67 的 derived 義務**（治理 §5.3 第 2 類）。

### G-2：在 G-3 的範圍內，修正被允許，不構成第二次評估，也不是新功能

- **不是評估**（N-1、CC-1）：修正只改圖例的文字。Cell 28 不讀取 test 列、不開守門、不擬合、不評分，也不寫任何檔案；它在選擇之後只畫已算好的訓練 CV 數字。修正後，cell 28 執行完的 kernel 狀態與修正前只差在一個圖物件的圖例字串，而之後沒有任何 cell 讀取那個圖物件（第 2 節第 4 點）。所以選擇、alpha、授權集合、`model_data`、結果檔都不可能因此改變。
- **§9.3 條件 7(b) 的判定**：條件 7(b) 規定凍結範圍的 source 有差異時，先由 DA 判定是否影響評估。**本紀錄就是對 G-3 那一個差異的判定：不影響評估，可以重跑。** G-3 以外的任何差異仍依條件 7(b) 先 route DA。
- **不是新功能，也不重開設計決策**（acceptor §14）：沒有新增產物、cell 或行為；圖例用英文標籤是 notebook 圖的 HOW（Brief §12），與 `diagnostics.py`、`prediction_plot.py` 的既有做法一致。方法的 zh-TW 名稱「Lasso 路徑排序」在 `model_data`、dashboard、報告與 notebook 的其他地方都不變。

### G-3：確切允許的修改

**唯一允許的修改**：`hw2.ipynb` cell 28（id `2fc16ee1`）的 source 中，把 `ax.plot(...)` 的這一行

```python
            label=models.METHOD_LABELS[m])
```

改為

```python
            label="Lasso path ranking" if m == "lasso_path" else models.METHOD_LABELS[m])
```

另外 MAY 在 cell 28 內加一行以 `#` 開頭的整行註解（例如 `# English legend label: no CJK font dependency (DA decision-20261019-cell28-glyphs.md)`）。修改後的圖例依序是 `Forward SFS`、`Backward SFS`、`RFE`、`Lasso path ranking`、`All-in baseline`，全部是 ASCII。

**不允許**（任何一項都會使 G-2 的判定失效，須另行 route DA）：

1. 修改 `hw2/models.py` 的 `METHOD_LABELS`，或條件 7(b) 列出的任何模組、`requirements.txt`（第 2 節第 3 點）。
2. 設定字型、`rcParams`、style，或新增字型檔、套件：結果會依機器的系統字型而不同，而且全域狀態會影響之後寫入 `results/figures/` 的 PNG，違反 N-3。
3. 刪除或移動 `import matplotlib.pyplot as plt`（第 2 節第 4 點）；改動 cell 28 的其他任何一行，包括畫的資料、顏色、尺寸、軸、標題；在 cell 28 存檔（`savefig`）。
4. 改動 cell 0–45 中的其他 cell、cell 的數量、順序、id，或 notebook metadata。
5. 為了這項修正在完整重跑之外執行任何 notebook cell（含部分執行）。

### G-4：由誰、何時、怎麼做

1. **執行者**：#67 Executor。#65、#66 MUST NOT 修改 cell 28；#65 R2 的 closure 條件不變。
2. **時點**：以一個獨立的 commit 只修改 cell 28 的 source（不清除、不改動任何輸出；這次 commit 時 cell 28 的輸出暫時仍是舊的），放在 §9.3 條件 7 的前置核對與完整重跑**之前**。Cell 28 的新輸出只來自 #67 的那一次乾淨環境完整執行（N-3）。
3. **事前確認（MAY）**：Executor 可以在 notebook 之外、不讀任何資料的 scratch process 中，以 `-W error::UserWarning` 畫一張只有這 5 個圖例標籤的空圖，確認沒有缺字警告。
4. **Worklog**：記錄這個 commit、cell 28 的 source 與 `052984b` 的 unified diff，以及第 4 節 G-5 的核對結果。

### G-5：對凍結範圍比對與 #67 重現核對的影響

| 核對 | 處理 |
| --- | --- |
| §9.3 條件 7(a)（selection digest＝`44f7723e…`） | 不變，照常執行 |
| §9.3 條件 7(b)（cell 0–45 的 source 與 `052984b` 相同） | 改為：cell 0–27、29–45 的 source 與 `052984b` 相同；cell 28 與 `052984b` 的差異**恰好**是 G-3 的那一行替換，加上至多一行允許的註解。可機械核對：去掉新增的整行註解、把新的 `label=` 行換回原文後，cell 28 的 source 與 `052984b` 完全相同。凍結模組與 `requirements.txt` 的 diff 仍必須為空。超出這個範圍的差異依條件 7(b) 先 route DA |
| §9.3 條件 2、條件 8；acceptor §14 第 3 點（資料、split／fold、winner、alpha、授權集合、Test 預測與指標的 digest／manifest 比對） | 不變。`result_digest` 必須＝`b53ff286…c3cfc6`，manifest 的 `selection_digest`＝`44f7723e…`；比對的項目都不受 cell 28 影響 |
| N-3「PNG、CSV、pickle、`model_data` 的其他內容必須相同」 | 不變（cell 28 不寫任何檔案） |
| N-3 的 notebook 輸出 | 在 N-3 已允許的差異之外，**只**另外允許 cell 28 的輸出不同：stderr stream 消失（輸出由 2 個變成 1 個），`display_data` 的 `image/png` 不同；它的 `text/plain`（`<Figure size 900x450 with 1 Axes>`）應相同。其他 cell 的輸出差異照 N-3 處理 |
| N-3 單一次執行的判準（執行序號 1…N 連續、cell 41 的 `run_id` 等於追蹤的 manifest） | 不變 |
| 新增的必要核對 | 完整重跑之後：(i) 整份追蹤的 notebook 的輸出中沒有任何「Glyph」或「missing from font」字串；(ii) cell 28 有 `image/png` 輸出，圖例的 5 個標籤可讀（ACCEPTANCE A-4 的人工檢查，記入 #67 worklog）。Executor MAY 把 (i) 寫成 pytest，但不是必要條件 |
| 失敗時 | 完整重跑後 (i) 或 (ii) 不成立時，不得再改 cell 28 後直接採用，停止這條路徑並 route DA。重跑的數字比對失敗仍依條件 2 處理，與本紀錄無關 |

**審查**：#67 R1 依 A-2 自行重做第一列以外的核對，特別是條件 7(b) 的修正版與新增的 (i)(ii)；cell 28 屬主程式（H-2），R1 依 A-1 在 H-2、H-3 下寫明。Spec Integration Audit 依 `decision-20261018-issue64-notebook-rerun.md` 第 7 節核對時，cell 28 的差異以本紀錄為準。

## 5. Accepted 語義與 boundary

- **不改變 accepted 語義。**這是治理 §5.3 第 2 類：分配一項 derived 義務給 #67（G-1），並對我自己在 derived contract 中設的 §9.3 條件 7(b) 與 N-3 加上一個有界的例外（G-2、G-5）。Brief、CC-1、Q1–Q43、BR、SR、UI 決策都不變；acceptor §14 第 3 點列出的比對項目一項都不受影響，也沒有新增功能。
- **Boundary**：在 Outcome Contract boundary 內。不需要 acceptor，沒有接受或授權缺口，也不需要 escalation。
- **不需要重新評估**（G-2）。

## 6. 受影響的工作與 evidence

| 對象 | 影響 |
| --- | --- |
| #67 | G-1、G-3～G-5：新的 derived 義務；§9.3 條件 7(b) 與 N-3 的核對依 G-5 執行 |
| #65 | 不受影響；不得修改 cell 28；R2 closure 條件不變。R1 F-4 的處置由本紀錄確定（owner #67） |
| #66 | 不得修改 cell 28 |
| #60～#64 | 不受影響，closure 與 evidence 不變 |
| `decision-20261018-issue64-notebook-rerun.md` §9.3 條件 7(b)、N-3 | 由本紀錄補充一個有界的例外；原文不改 |
| `decision-20261019-issue65-labels-figures.md` O-1 | 由本紀錄處置 |
| Spec Integration Audit | 依 G-5 最後一段 |
| Spec rev 5、Brief、Outcome Contract、Tickets、程式、notebook | 本紀錄不修改 |
| 高風險 | H-2（主程式 notebook）；H-3（凍結範圍與重現核對） |
| Orchestrator | 派 #67 時把本紀錄放進 bounded pack |

**建議的票文字**（我不修改票，由派工者逐字附加；不附加也不影響本紀錄的效力）：

```markdown
- [ ] （DA `decision-20261019-cell28-glyphs.md` G-1～G-5）完整重跑之前，以獨立 commit 只把 `hw2.ipynb` cell 28 的 `label=models.METHOD_LABELS[m])` 改為 `label="Lasso path ranking" if m == "lasso_path" else models.METHOD_LABELS[m])`（可加一行註解），不改 `hw2/models.py`、不設定字型或 rcParams、不另外執行 cell；條件 7(b) 的 source 核對依 G-5 修正版；完整重跑後整份 notebook 輸出沒有「Glyph」／「missing from font」，cell 28 的圖例可讀，記入 worklog。
```

## 7. Evidence

- 讀取：Bindings b5（§2、§3.2、§7）；治理 v2.2 §1.2、§2.4、§2.5、§3.6、§5.3；`run/run-20261018-hw2-formal.md`（§1、§14、§15）；`audit/issue-65-c1-r1.md`（全文，特別是 F-4、§7、§8 第 1 點）；`decision-20261019-issue65-labels-figures.md`；`decision-20261018-issue64-notebook-rerun.md`；`BRIEF.md` §7、§10、§11、§12；`SPEC.md`（US-60、Dashboard、人工檢查表）；`doc/acceptance/ACCEPTANCE.md`（A-4、D-2、OV-1）；`doc/requirement/` 的評分條文；GitHub issue #67；`requirements.txt`；`hw2/models.py`（`METHOD_LABELS`）、`hw2/selection.py`、`hw2/prediction_plot.py`、`hw2/diagnostics.py`。
- 執行：以單元 `.venv` 讀取 `hw2.ipynb` cell 26–31 的 source 與輸出；掃描全部 code cell 的輸出中的「Glyph／missing from font」（只有 cell 28）；列出 cell 28 之後引用 `fig`、`ax`、`colors`、`m`、`cands` 的 cell 並讀取相關行；`git show 052984b:home_work_02/hw2.ipynb` 與工作樹比對（`052984b` 有 47 個 cell；cell 0–45 的 source 相同；cell 28 完整 JSON 相同）；`grep` `results/model_data.json`、`assets/`、`index.html` 中的「Lasso 路徑排序」；`grep` `tests/` 中對 cell 28 或 `052984b` 的引用（沒有）。
- 沒有執行 notebook、`hw2.run_notebook` 或任何會載入正式 test 列的程式。寫入的檔案只有本紀錄；沒有修改程式、測試、notebook、Spec、Brief、Outcome Contract、票或其他紀錄；沒有 commit。

## 8. Required authority

無。裁決在 DA 權限內，不改變 accepted 語義，不需要 acceptor，不需要重新評估，也不需要 escalation。執行者是 #67 Executor（Orchestrator 派工），審查是 #67 R1 與 Spec Integration Audit。
