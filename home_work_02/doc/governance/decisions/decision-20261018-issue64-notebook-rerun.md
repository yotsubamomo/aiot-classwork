# Decision record — #64 C-1：notebook 的完整重跑與「Test 只評估一次」的關係（另含 C-3）

- **紀錄類型**：Design Authority decision record（治理 §2.4、§3.6、§5.3 第 2 類；Bindings b5 §7）
- **日期**：2026-10-18
- **Run**：`run-20261018-hw2-formal`。Orchestrator 依治理 §2.4「已指明 authority，且與本節規則一致」派工。
- **問題來源**：`doc/governance/worklog/issue-64.md` §4（notebook 的執行方式）與 §7 C-1（required authority＝Design Authority）；連帶 §7 C-3。Worklog 的敘述只當作待驗證的主張，下文的事實是我自行核對的結果（第 3 節）。
- **受審 subject**：branch `home_work_02-regrill`，#64 implementation commit `003b825426a500fa2d11ebea584d48c93cd4635d`（base `b34cc50`）；#63 正式評估產出 `052984ba21568499aad4b02e6ba8c564901e8c76`；撰寫時 HEAD＝`20c7210`（record-only）。
- **Binding**：`gov-design-authority`，`claude-opus-5-5`／`high`（Bindings 預設 mapping，沒有 escalation，也沒有替代）。本紀錄不自證 binding，由派工者依 Bindings §3.6 核對。
- **Capability escalation**：不提出。E-DA/D1 不成立：兩種處理方式（保留「完整重跑＝重現」，或改成重跑時不重新執行評估）的後果不同，但現有證據可以裁決（第 5 節：Brief §10 與 acceptor 接受的 #67 AC 都要求重跑時重算 test 結果並與 #63 比對）。E-DA/D2 不成立：我在 `derivation-SPEC.md` §9.3 的先前決定沒有被 FA ruling 或經 route 的 Reviewer finding 推翻或爭議；Orchestrator 對 #64 的派工約束比 §9.3 更窄，不是爭議（第 4 節 N-6）。

## 1. 問題

正式 test 評估在 #63 執行了一次（run `fe76019b…`）。之後守門旗標是開啟的（`hw2/testgate.py` `OFFICIAL_TEST_GATE_ENABLED = True`），所以從頭完整執行 `hw2.ipynb`（`python -m hw2.run_notebook`）會在 5.4 節的 cell 再開一次守門、再評估一次，並覆寫 `model_data`。#64 的派工約束禁止再執行評估，Executor 因此只做了部分執行：notebook 5.5 節以前的輸出來自 #63 的正式執行，5.6 節與第 6 章的輸出來自 #64 的另一個 kernel。

要決定的是：

1. #67 要求的乾淨環境完整重跑，與「每個模型只做一次最終 Test 評估」（CC-1 第 3 點；票的共同條款「Test 時序」）怎麼並存。
2. #64 的 notebook 輸出來自兩次執行，#64 結案前是否必須處理；#67 之前是否有其他事要先處理。
3. （C-3）#64 AC「報告草稿的解釋段落標示」在報告檔還不存在時怎麼滿足。

## 2. 依據

| 來源 | 內容 |
| --- | --- |
| Brief §4、§5（`dff7c55c`） | Test 在所有模型選擇固定後只評估一次；test 排名與 CV 不同時不換模型 |
| Brief §10（accepted） | 「固定 seed、鎖版本的 `requirements.txt`、乾淨環境完整重跑後數字一致」 |
| Brief §8（accepted） | 繳交的 `<學號>_hw2.ipynb` 由打包步驟自 `hw2.ipynb` 產生（單一來源，不維護兩份） |
| OC §4 CC-1 第 3、4 點 | 每個 Ridge／Lasso 模型只允許一次最終 Test Evaluation，不得因 dashboard 互動重新測試；test 結果不得回饋任何選擇 |
| Spec rev 5 Problem Statement、Testing「乾淨環境重跑」 | 「每個數字都要能從一次可重現的執行追溯回來」；乾淨環境重跑：新建虛擬環境、安裝、非互動執行 notebook、重跑測試、建置報告、打包；數字與追蹤的結果檔一致 |
| `derivation-SPEC.md` §9.3 | 「每次執行只做一次 test 評估」是每一次執行的不變量；#63 之後的票完整重跑 notebook 時重新執行同一條決定性的評估是重現，不是新的評估，條件 1–5（§9.6 加條件 6） |
| Ticket #67 AC（Tickets Review 時由 TR-01 加入，acceptor 接受） | 「乾淨環境重跑與 ZIP 內 `model_data` 的 `test_inputs` 與 `test`，與 #63 記錄的比對基準一致（§9.3 條件 2；不一致時停止並 route 給 DA）」 |
| 全部票的共同條款「Test 時序（acceptor 2026-10-18）」 | 正式保留 Test set 的評估只在 T4 執行一次 |
| `worklog/issue-63.md` §5 | 唯一一次正式評估的紀錄：run `fe76019b9af84b1e8ff46095d5ac0fb2`、`selection_digest` `44f7723e4023afc3e8e997f42bf4eb59db392af81cced11743757a9857cb4b28`、`result_digest` `b53ff286ae0734add8b272089aba904a1cb7f5aca444a62d356420b25dc3cfc6`、`test` 數值摘要 |
| `decision-20261018-issue63-js-tolerance.md` §8 | §9.3 條件 2 的 `result_digest` 比對是 bit-exact；只差最後幾位時 route 給 DA |

## 3. 我自行核對的事實

1. **完整重跑一定會再評估一次**：`hw2.ipynb` cell 41（5.4 節）依序執行 `gate.open(winners, alphas)`、`gate.evaluate(...)`、`export.build_model_data(...)`、`export.write_model_data(...)`；`hw2/run_notebook.py` 從頭執行全部 cell。旗標開啟時，新的 process 可以再載入一次正式 test 列（`_official_test_rows_loaded` 只限同一 process）。所以每一次完整重跑都會重新評估同一個授權集合，並以新的 `run_id`、`opened_at`／`evaluated_at`、`code_revision` 與時間欄位覆寫 `results/model_data.json`、`assets/model_data.js` 的 `meta.test_evaluation`。
2. **比對基準不在被覆寫的範圍內**：`export.result_digest` 只對 `test_inputs` 與 `test` 取 sha256。目前追蹤的 `results/model_data.json` 重算為 `b53ff286…c3cfc6`，manifest 的 `run_id` 是 `fe76019b…`、`selection_digest` 開頭 `44f7723e4023`、`code_revision` 是 `d413e58`（`package_modified: false`），都與 #63 worklog §5 相同。完整重跑之後，檔案內的 manifest 會改成那次重跑的值，#63 的識別只留在 governance 紀錄（worklog §5）。
3. **#64 沒有改動選擇與評估路徑**：`git diff --stat 052984b 003b825 -- hw2/ requirements.txt` 只有新增 `deployment.py`、`diagnostics.py`、`explain.py`，以及 `__init__.py` 的說明文字與 `paths.py` 的四個新路徑常數。`results/model_data.json`、`assets/model_data.js`、`results/split/`、`comparison.csv`、`alpha_cv.csv`、`cv_by_method_k.csv`、`hw2/testgate.py`、`export.py`、`selection.py`、`models.py`、`comparison.py`、`data.py`、`preprocess.py`、`ols.py` 自 `052984b` 起都沒有改變。
4. **#64 notebook 的實際狀態**：`b34cc50` 有 47 個 cell，`003b825` 有 71 個。cell 0–45 與 `b34cc50` 完全相同（含輸出），notebook metadata 相同；只有 cell 46（原本的「第 6 章尚未完成」佔位）被取代，後面是新增的 cell。Code cell 的執行序號是 `1…28, 25…35`：新 cell 的 25–35 與 #63 的 25–28 重複。Cell 41 的輸出含 `fe76019b` 與 `44f7723e`。這與 worklog §4 的描述相符。
5. **#63 之後的紀錄已經預期重跑**：`worklog/issue-63.md` §8「之後的票」與單元 `README.md` 第 27 行都寫明完整重跑會以相同 seed 與鎖版本重做同一個評估、結果必須一致。不過 README 把比對基準寫成「第一次正式評估記錄的結果（`meta.test_evaluation`）」，而依第 1 點，完整重跑之後 `meta.test_evaluation` 已經是那次重跑的紀錄。README 第 19 行也把 `run_notebook` 寫成「含唯一一次的 Test 評估」。

## 4. 裁決

**N-1（兩項要求的關係；確認 §9.3）**：「每個模型只做一次最終 Test 評估」指的是**評估這個決定事件**：在全部選擇只用 training 固定之後，對授權集合計算一次 test 結果，之後不再以任何理由重新評估、比較或改選。它不是「全部歷史中 `gate.evaluate` 只能被呼叫一次」。在選擇不變的前提下完整重跑 notebook，是以同一 seed 與鎖版本重現同一個決定性的計算，得到的必須是同一組數字；它不產生新的 test 資訊，也不能影響任何選擇。所以這是 §9.3 所說的重現，不是第二次評估，條件是 §9.3 條件 1–6 與下面的條件 7、8 全部成立。條件不成立時（選擇、alpha、前處理、模型集合、授權集合或 PI／指標的計算有任何改變），那次執行就是新的評估，不得執行；已經執行的，結果不得採用，依條件 2 停止並 route 給 DA。

**§9.3 新增的條件（對 #65～#67 與之後的任何完整重跑有約束力）**：

7. **重跑前的前置核對（fail-closed）**：任何完整重跑之前，先在不開啟守門的情況下核對兩件事，記入 worklog：(a) 只用 training 列重算的 `testgate.selection_digest(winners, alphas)` 等於 `44f7723e4023afc3e8e997f42bf4eb59db392af81cced11743757a9857cb4b28`。做法可以沿用 #63 的 `pregate` 或 #64 的部分執行：在 process 內先把 `OFFICIAL_TEST_GATE_ENABLED` 設為 False，再執行 5.4 之前的 cell。(b) `git diff 052984b -- home_work_02/hw2/{data,split,preprocess,selection,models,comparison,ols,metrics,contract,testgate,export}.py home_work_02/requirements.txt` 沒有差異，notebook 5.5 節以前各 cell 的 source 也與 `052984b` 相同，資料 sha256 等於 Brief 釘住的值。(a) 不符合時不得重跑。(b) 有差異時，先 route 給 DA 判定那些改動是否影響評估，再決定能不能重跑。Executor MAY 在程式中加上等效的守門檢查（官方資料時把 digest 與釘住的值比對、不符就拒絕開啟），但這不是必要條件；如果加了，它屬於 H-3 的修改，需要 audit。
8. **比對與記錄**：重跑後依條件 2 比對 `result_digest`，並在 worklog 記錄這次重跑的 manifest（`run_id`、`selection_digest`、`code_revision`）、`result_digest`，以及「本次是 #63 run `fe76019b…` 的重現」。唯一一次正式評估的權威紀錄仍然是 `worklog/issue-63.md` §5，不因重跑而改變。

**N-2（#64：不需要處理，可以照現況結案）**：#64 不需要完整重跑，也不需要修改程式或 notebook。notebook 混合兩次執行的輸出是**過渡狀態**，可以接受，理由如下：#64 的新輸出來自 #63 已凍結的 training 端狀態（Executor 以 kernel 狀態重算的 selection digest 等於 `44f7723e…`，第 3 節第 3 點的模組也沒有改變）；被保留的 #63 輸出沒有被改動。Spec 要求的「一次可重現的執行」是交付時的性質，在 #67 達成（N-3）。#64 R1 MUST NOT 只因 notebook 混合兩次執行或執行序號重複而開 finding。R1 仍然依 A-2 自行核對：cell 0–45 與 `b34cc50` 相同、`model_data` 與 `result_digest` 沒有改變、#64 的新輸出與產物可以重現（worklog V-9 的主張）。Reviewer 若認為重現的證據不足，那是 evidence sufficiency，屬 Reviewer 的範圍。

**N-3（#67：單一次完整執行是交付物的唯一來源）**：#67 的乾淨環境完整重跑是必要的，就是 N-1 所說的重現，並且必須符合條件 7、8。通過條件 2 的比對與 #67 AC「重跑數字與追蹤結果檔、報告、README 一致」之後：

- 那一次執行產生的已執行 notebook 與結果檔（`results/`、`assets/model_data.*`），就是 #67 結案時追蹤的版本；`<學號>_hw2.ipynb` 由這份已追蹤的 notebook 產生（Brief §8 單一來源）。不得把混合輸出的 notebook 打包，也不得讓追蹤版與打包版來自不同次執行。
- 單一次執行的可觀察判準：全部 code cell 都有執行序號，而且依序是 1…N、連續、沒有重複；cell 41 輸出中的 `run_id` 等於追蹤的 `model_data` 的 `meta.test_evaluation.manifest.run_id`。
- 與目前追蹤檔相比，只允許記錄執行識別、時刻或耗時的欄位不同。在目前的 `model_data` 中，這些欄位是 `meta.generated_at`、`meta.timing_s`、`meta.path_timing_s`、`meta.comparison_timing_s`、`baselines.pvalue_backward.timing_s`，以及 `meta.test_evaluation` 的 `opened_at`、`evaluated_at`、`timing_s`、`code_revision` 與 manifest 的 `run_id`、`opened_at`、`evaluated_at`。`meta.versions` 中不受 `requirements.txt` 鎖定的項目（例如 Python 的 patch 版本）也可以不同，但要在 worklog 記錄。此外允許 notebook 中印出這些值的輸出與執行序號不同。PNG、CSV、pickle 以及 `model_data` 的其他內容必須相同。出現其他差異時停止，route 給 DA，不得直接採用新檔。
- 比對不一致（條件 2）或前置核對失敗（條件 7）時，#67 只停止這一條路徑，繳交與 phase acceptance 都不得以混合輸出的 notebook 替代。

**N-4（#65、#66：不重跑）**：在 #67 之前，#65 與 #66 不需要、也 SHOULD NOT 做完整重跑。只要不改動 5.5 節以前的 cell，就不需要重新執行 notebook。若必須重新執行 5.6 節以後的 cell，沿用 #64 的部分執行方法：同一個 kernel；任何 cell 執行前先在 process 內把旗標設為 False；不執行 cell 41、42、44、45，並保留它們的 #63 輸出；重算 selection digest，確認等於 `44f7723e…`；在 worklog 記錄。若某張票確實需要完整重跑，必須符合 §9.3 條件 1–8，並在 worklog 記錄理由。

**N-5（README 的措辭，分配給 #65；H-4）**：#65 改寫單元 README 時：

- 不得把 `meta.test_evaluation` 說成「第一次正式評估的紀錄」。要寫明：唯一一次正式評估是 #63 的那次（run `fe76019b…`、`result_digest` `b53ff286…`，權威紀錄在 `doc/governance/worklog/issue-63.md` §5）；`meta.test_evaluation` 記錄的是產生目前這份檔案的那次執行；完整重跑是對同一評估的重現，結果必須與該基準 bit-exact 一致。
- 重跑步驟中 `run_notebook` 的說明，改為「重現唯一一次的 Test 評估」或等義的寫法，不得讓人以為每次執行都是新的評估。
- 報告（#65、#66）提到 test 評估時同樣以 #63 為那一次評估；若提到重跑，寫成重現。

**N-6（派工約束）**：Orchestrator 對 #64 的約束「不得再執行」比 §9.3 更窄，與 §9.3 並不衝突。Executor 遵守它，並且以部分執行的方式完成，處理正確。之後的派工可以沿用 N-4。#67 必須依 N-3 完整重跑，這次派工 MUST NOT 再沿用「不得執行」的約束，改以條件 7、8 與 N-3 取代。

**I-4（C-3 的解讀，對 #64、#65 有約束力）**：#64 AC「報告草稿的解釋段落標『依老師補充建議』與『專案延伸』」，報告檔要到 #65 才建立（`derivation-SPEC.md` §9.1；與 §9.4 I-3 同型）。#64 把這兩個標示放在 notebook 6.2 節，也就是報告的來源段落，這樣就滿足這條 AC。報告版的模型解釋段落與它的標示（6.2 的模型解釋標「依老師補充建議」，permutation importance 的用法標「專案延伸」）由 #65 負責，屬於 #65 既有的「三種標示」AC 與 Brief §8 的章節清單，不是新增的義務。#64 R1 核對的是 notebook 6.2 的標示。

## 5. 理由

- **不能兩者擇一**。Brief §10 要求乾淨環境完整重跑後數字一致，Brief §4、§5 與 CC-1 要求 test 只評估一次，兩者都是 accepted 語義。notebook 是主程式，評估就在其中，所以完整重跑必然重算 test 結果。若把「一次」讀成「`evaluate` 在全部歷史中只能被呼叫一次」，Brief §10 就無法滿足，test 數字也永遠無法被獨立重現。acceptor 接受的 #67 AC 也明確要求把重跑的 `test_inputs`／`test` 與 #63 的基準比對，這只有在重跑會重算 test 結果時才有意義。所以 accepted 語義只容許 N-1 的讀法。這也是 §9.3 的原意，本紀錄只是確認它並補齊細節。
- **另一種設計不採用**：讓重跑時不執行評估、直接沿用 #63 的 `model_data`（replay）。這樣 test 數字就不再被重現：#67 AC 的比對沒有對象，Brief §10 的「數字一致」對 test 結果也就沒有被驗證。它還需要修改已經審查過的評估路徑。所以不採用。
- **條件 7 的作用**：§9.3 條件 2 是事後比對。若選擇在 #63 之後被無意改動，完整重跑會先在 test 上評估一個未授權的模型，然後才被發現，這時 test 已經暴露給未授權的模型（H-3，BR-01）。前置核對把它改成事前阻擋，而且不需要修改已審查的守門程式。這延續了 #63 自己的 pre-gate 做法。
- **N-3 的作用**：Spec 要求每個數字都能追溯到一次可重現的執行，Brief §8 要求打包版與追蹤版是同一份檔案。目前只有 #67 的乾淨環境重跑同時滿足兩者。把它定為交付物的唯一來源之後，#64 的過渡狀態就有了明確的結束點，也可以被觀察。
- **N-4 的作用**：減少重跑的次數，追蹤的 manifest 在 #67 之前就一直是 #63 自己的紀錄。
- **N-5 的作用**：重跑之後，`meta.test_evaluation` 記的是那次重跑，README 原本的說法會變成不實的來源說明（H-4）。

## 6. Accepted 語義與 boundary

- **不改變 accepted 語義**。這是治理 §5.3 第 2 類：對 derived contract（`derivation-SPEC.md` §9.3、ticket #64、#65、#67 的 AC）的 clarification 與 Ticket 義務分配。沒有新增或移除 Brief 的 requirement、scope、constraint 或 acceptance semantics。N-1 是 Brief §4／§5／§10 與 CC-1 唯一能同時成立的讀法。條件 7、8 與 N-3～N-5 只把既有的「一次評估」、「重跑一致」、「單一來源」與 H-3／H-4 落實成可核對的步驟，只會更嚴格，不會放寬。
- **Boundary**：在 Outcome Contract boundary 內。不需要 acceptor，也沒有接受或授權缺口。CC-1 第 3 點限制的是重新評估的決定（「不得因 Dashboard 互動而重新測試」），不是決定性的重現；acceptor 接受的 #67 AC 本身就預設了這個重現。
- **不需要重新評估**：本紀錄不要求執行 `hw2.run_notebook`、不要求改動 `results/`、`assets/model_data.*`、`hw2/`、notebook 或測試。#64 照現況繼續走 R1。

## 7. 對各工作的要求

| 對象 | 要求 |
| --- | --- |
| #64 | 不需要修改（N-2）。C-1 由本紀錄結案；C-3 依 I-4 結案。R1 依 N-2 審查（A-2 的自行核對照常）。Worklog 可以在之後的 record-only 更新中引用本紀錄 |
| #65 | N-4（不重跑；必要時部分執行）；N-5（README 與報告的措辭）；I-4（報告中模型解釋段落的標示） |
| #66 | N-4；報告依 N-5 的最後一點 |
| #67 | N-3（單一次完整執行是追蹤版與打包版的唯一來源、可觀察判準、允許差異的欄位）；§9.3 條件 7、8；N-6（派工不得沿用「不得執行」） |
| Spec Integration Audit（subject：#67 結案時的狀態） | 依 A-2 核對：追蹤的 `hw2.ipynb` 與 ZIP 內的 `<學號>_hw2.ipynb` 符合 N-3 的單一執行判準；`result_digest` 等於 `b53ff286…`；manifest 的 `selection_digest` 等於 `44f7723e…`；條件 7 的前置核對在評估之前就已記錄；README 符合 N-5 |
| Orchestrator | 派 #65～#67 時，把本紀錄放進 bounded pack；派 #67 時依 N-6 改用條件 7、8 與 N-3 |

**建議的票文字**（我不修改票，由派工者逐字附加；不附加也不影響本紀錄的效力）：

#67，在「乾淨環境重跑與 ZIP 內 `model_data` …」那一條 AC 之後：

```markdown
- [ ] （DA `decision-20261018-issue64-notebook-rerun.md` N-3、§9.3 條件 7、8）完整重跑前，在不開啟守門的情況下核對 selection digest＝`44f7723e…`，並確認選擇與評估相關的模組、`requirements.txt`、notebook 5.5 節以前的 cell 自 `052984b` 未改，結果記入 worklog；這一次乾淨環境完整執行的 notebook 與結果檔就是結案時追蹤的版本，`<學號>_hw2.ipynb` 由它產生；code cell 執行序號為連續的 1…N、沒有重複，cell 41 的 `run_id` 等於追蹤 `model_data` 的 manifest；除了 N-3 列出的執行識別、時刻與耗時欄位，其他產物與重跑前相同。
```

#65，在 AC 最後：

```markdown
- [ ] （DA `decision-20261018-issue64-notebook-rerun.md` N-4、N-5、I-4）不做完整重跑；README 與報告寫明唯一一次正式評估是 #63（run `fe76019b…`、`result_digest` `b53ff286…`，`worklog/issue-63.md` §5），`meta.test_evaluation` 只記錄產生目前檔案的那次執行，完整重跑是重現；報告的模型解釋段落標「依老師補充建議」，permutation importance 的用法標「專案延伸」。
```

## 8. 受影響的工作與 evidence

| 對象 | 影響 |
| --- | --- |
| `derivation-SPEC.md` §9.3 | 由本紀錄補充條件 7、8；原文不改。本紀錄與 §9.3 一起作為有效解讀 |
| #63 的 closure evidence | 不受影響。§5 仍是唯一一次正式評估的權威紀錄與比對基準 |
| #64 的 evidence（worklog §4、§5） | 有效。部分執行的方法被認可為過渡做法（N-2、N-4） |
| #65～#67、Spec Integration Audit | 依第 7 節 |
| Spec rev 5、Brief、Outcome Contract、tickets、程式與結果檔 | 不修改 |
| 高風險 | H-3（評估完整性：條件 7、8、N-3）；H-4（來源說明：N-5、I-4） |

## 9. Evidence

- 讀取：Bindings b5；治理 v2.2 §1.2、§2.4、§2.5、§3.6、§5.3；`outcome-contract.md`（CC-1、AD-1～AD-3）；`BRIEF.md` §4、§5、§8、§10；`SPEC.md` rev 5（Problem Statement、Testing Decisions）；`derivation-SPEC.md` §9.1、§9.3、§9.4、§9.6；`decision-20261018-issue63-js-tolerance.md`；`decision-20261018-high-risk-categories.md`（A-2、A-7）；`run/run-20261018-hw2-formal.md`；`worklog/issue-63.md` §3–§9；`worklog/issue-64.md`；GitHub issues #64、#65、#67；`doc/ticket/tickets.md`；`hw2/testgate.py`、`hw2/run_notebook.py`、`hw2/export.py`（`result_digest`、`meta.test_evaluation`）；`README.md`；`hw2.ipynb`（`b34cc50` 與 `003b825`）。
- 執行：`git diff --stat b34cc50 003b825`；`git diff --stat 052984b 003b825 -- hw2/ requirements.txt`；`git diff --quiet 052984b 003b825 --` 正式產物與選擇／評估模組（無差異）；以 Python 逐 cell 比對兩個版本的 notebook（cell 0–45 相同，cell 46 被取代，執行序號 `1…28, 25…35`）；以單元 `.venv` 對追蹤的 `results/model_data.json` 重算 `export.result_digest`（`b53ff286…c3cfc6`），並讀出 manifest（`fe76019b…`、`44f7723e4023…`、`d413e58`）；掃描 `model_data` 中記錄執行識別、時刻或耗時的鍵（N-3 的清單）；確認 `results/tables/*.csv` 的欄名沒有時間欄位。
- 沒有執行 `hw2.run_notebook`，也沒有執行任何會載入正式 test 列的程式。寫入的檔案只有本紀錄；沒有修改程式、測試、Spec、Brief、Outcome Contract、票或其他紀錄；沒有 commit。

## 10. Required authority

無。本裁決在 DA 權限內，不改變 accepted 語義，不需要 acceptor，不需要重新評估，也不需要 escalation。
