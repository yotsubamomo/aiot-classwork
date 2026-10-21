# Decision record — #75 R1-F1：Lasso 路徑的非退化提前結束與目標單位相依（`home_work_02/`，HW2 V2 Enhance）

- **紀錄類型**：Design Authority decision record（治理 §2.4、§3.6、§4.2、§5.3 第 2 類；Bindings b5 §2.4、§7）。
- **日期**：2026-10-22
- **Run**：`run-20261022-hw2-v2-enhance`（Orchestrator＝root session `37216426-f292-44f9-bad1-e2d862e7b8f1`）
- **來源**：#75 R1 audit record [`../audit/issue-75-c1-r1.md`](../audit/issue-75-c1-r1.md)（committed `ee0c481`，VERDICT CLOSURE）finding **R1-F1**（Medium，non-blocking；契約語義 routing signal，治理 §4.2），record §5、§7 指定 authority＝Design Authority；run record 第 164 列依治理 §2.4 直接派工，並把 #75 結案列為待本紀錄（orch-default P6）。
- **Outcome Contract**：[`../outcome-contract.md`](../outcome-contract.md) §5（V2，接受基準 `d7f02d4179d2cb5c2ecf0c39a4643a6ef8287907`）與 §5.2 CC-V2-1；§1–§4（V1）仍有效。
- **相關紀錄**：[`derivation-SPEC-V2.md`](derivation-SPEC-V2.md)（§0、§5.2、§7 H-3(ii)、H-4、A-2(V2)、A-5(V2)、I-5）；[`decision-20261022-r1f3-v1-footer.md`](decision-20261022-r1f3-v1-footer.md)（分配先例）；Executor worklog [`../worklog/issue-75.md`](../worklog/issue-75.md)（D-3、§8 觀察 2、3）。
- **Subject**：branch `home_work_02-v2-enhance`，實作 commit `2069fea`；撰寫時 HEAD `ee0c481`，`git diff --stat 2069fea HEAD -- home_work_02/hw2 home_work_02/assets home_work_02/tests` 為空。
- **Binding**：`gov-design-authority`，有效 mapping `claude-opus-5-5`／`high`（Bindings §3.1 預設；沒有 escalation、沒有替代）。撰寫前我自行讀取本 assignment 的 transcript（agentId `ae5f000e48cc110e8`，`agentType` `gov-design-authority`）：觀測到 `('claude-opus-5-5', 'high')` 49 則，單一元素。全程核對由派工者依 Bindings §3.6 執行；本紀錄不自證 binding。
- **Capability escalation**：不提出。E-DA/D1 不成立：(a) 的可行讀法中只有一種與全部 accepted 文字相容；(b) 的兩種讀法（照抄正式分析的 `lars_path` 呼叫／與單位無關）可以用 accepted 文字與我自己取得的數值證據裁決（第 3、4 節）。E-DA/D2 不成立：我先前對本問題沒有決定；`derivation-SPEC-V2.md` 與 `decision-20261022-r1f3-v1-footer.md` 沒有被 FA ruling 或 Reviewer finding 推翻或爭議。
- **獨立性**：R1-F1 的敘述與探測數字、Executor worklog D-3 與 §8 的說明（包括「正式分析的 `lars_path` 呼叫相同」）都只當作待驗證主張；第 3 節是我自己讀碼與執行所得的證據。

## 1. 問題

Accepted A-2（Brief V2 §12；Spec V2「LARS 退化（A-2）」）只定義一種情形：路徑在 **active set 退化**（新增欄使 active set 秩不足）時停止，保留已求得的路徑段，k 超過該步的 Lasso 候選 `INVALID_MODEL`、原因 `lasso_path_degenerate`，未進入的 group 只作展示、不沿用 V1 的 canonical 補齊。

`2069fea` 的引擎與 Python 參照另把「路徑結束時仍有 group 未進入」一律記為 `cause = 'path_ended'`，套用同一狀態；而 LARS 會在 `alpha = C/n ≤ 1.19e-7`（sklearn 的 `equality_tolerance`，float32 eps）時結束，目標只置中、不縮放，所以這個門檻帶有目標的單位。

要裁決的是：

- **(a)** 非 active-set 退化的提前結束（路徑走到終點仍有 group 未進入、equality tolerance、`alpha_increasing`、`max_iter`、同步多個 drop）是否屬於 A-2 的 `INVALID_MODEL`／`lasso_path_degenerate`；若是，原因如何如實標示。
- **(b)** 路徑的結束判定可以、或必須，與目標的單位無關。
- 後續工作由哪一張票承接（#76 → #77 → #78 尚未執行）；#75 是否需要重開 rework。

## 2. 依據

| 來源 | 內容 | 用途 |
| --- | --- | --- |
| Brief V2 §12 A-2（accepted） | 保留已成功求得的路徑段；「退化後**無法可靠求得**的候選（k 超過該步）標 `INVALID_MODEL`，原因 `lasso_path_degenerate`」；補齊順序不得稱為實際路徑；「探索模式**不沿用**該補齊作為選模語義」 | (a)：A-2 的操作原則是「路徑沒有可靠給出的候選不成為有效候選，也不以欄序補齊」 |
| Spec V2「Feature group 與特徵選擇」 | Lasso 以 **exact LARS** 的 entry（最大 entry alpha 先）排序；tie 以「**相對**容忍度與正式分析同值」依 CSV 欄序；準則與正式分析相同 | (b)：exact LARS 的路徑對目標乘上正常數是等變的；tie 是相對容忍度 |
| Spec V2「候選有效性、狀態」；US-42 | 狀態四種；`INVALID_MODEL`＝不符合 A-1 或 `lasso_path_degenerate`，「原因碼與涉及的 fold／group 必附」；`FAILED`＝非預期計算失敗（數值例外等），#77 以「該方法 `FAILED`、其他方法照跑」驗收；狀態與原因碼是枚舉 | (a)：可用的狀態與原因碼 |
| Brief V2 §8 數值驗證；Q21 | 非退化資料：entry alpha 相對 1e-6，相差超過容忍度的 group 順序必須相同；完全共線或非唯一解才不以數值當 oracle；entry alpha 的定義與正式分析一致 | (b)：非退化資料必須得到 exact LARS 的進入順序；回報的 alpha 必須是正式分析的尺度 |
| Brief V2 §3.1、§5.3、Q18；§10 | +2「可任意輸入 Dataset」；目標不轉換、以原始尺度建模與報告；「LARS 在使用者資料上**退化**」以 A-2 處理 | (b)：任意資料的任意單位都在 accepted 範圍內；A-2 是對資料退化的處理，不是對單位的處理 |
| Spec rev 5；`hw2/selection.py`（V1，未改） | `lasso_entry` 對 **ln(price)** 置中後呼叫 `lars_path(X, y, method="lasso")`；未進入的 group 依欄序排後（V1 canonical 補齊）；`_pick` 的 tie 為 `TIE_RTOL * max(|best|, 1)` | 正式分析的目標是 ln(price)：價格單位乘上常數只加上常數，置中後消失，所以 V1 的 Lasso 排序與 tie **本來就與價格單位無關**；V2 改用原始目標（Q18）才使絕對門檻帶有單位。A-2 已明定 V2 不沿用 sklearn 對退化的處理（sklearn 跳過該欄繼續）與 V1 的補齊，所以「與正式分析相同」指的是準則，不是逐字照抄 `lars_path` 的呼叫 |
| derivation H-3(ii)、H-4、A-2(V2)、A-5(V2) | A-1～A-3 語義屬評估完整性；頁面與紀錄的陳述必須屬實 | (a) 的原因標示；驗證方式 |
| derivation §0 | Spec V2 與 #74–#78 由 acceptor 直接接受，其 AC／invariant／gate 同時是 accepted 語義；DA 的解讀與分配只能在不改變它們的前提下作出 | 本紀錄的界線（第 6 節） |

## 3. 我自己取得的事實

讀碼（`2069fea`）：

- `assets/explore_engine.js`：常數 `EQ_TOL = 1.1920928955078125e-7`（第 83 行）；`larsLasso` 第 777 行 `if (alpha <= EQ_TOL) break;`（`alpha = C / n`，`C` 是置中原始目標與標準化欄的最大共變）；`alpha_increasing`、`max_iter`、`multiple_drops` 只設 `stop.cause`；`lassoOrder`（約第 901 行）把 `active_set_degenerate` 以外的提前結束一律記為 `path_ended`，k > `nEntered` 的子集為 `null`。tie：`pick` 第 641 行與 LARS 進入時的 `Cov` tie 都是 `TIE_RTOL * Math.max(…, 1)`；entry alpha 的 tie 叢集同樣以 `Math.max(|alpha|, 1)` 為下限。
- `hw2/explore_reference.py`：`lars_segment` 以 sklearn `lars_path` 加上 `_degenerate` 截斷；`lasso_order` 第 682–684 行把其他未進入情形記為 `path_ended`；`_pick` 第 548 行與 V1 相同的 `max(abs(best), 1.0)` 下限。
- `assets/explore_app.js` 第 65 行：`path_ended` 對使用者說「它們與已進入的欄線性相依，或在這些列上沒有變化」。`index.html` `#ex-lasso-card` 第 136 行說明 LARS 的計算方式（「目標只置中、不取 log」）。

我的探測（scratchpad，以 subject 的 Python 參照執行，未修改 repo）：

| 情境（50 Startups，只把 Profit 乘上 c） | 結果 |
| --- | --- |
| c＝1、1e-6、1e6 | Lasso 在訓練集與五個 fold 全部 group 進入；四條路徑與 c＝1 相同 |
| c＝1e-9 | fold 0、3 的 Lasso 只進入 3 個 group（`path_ended`） |
| c＝1e-10 | 訓練集與五個 fold 都只進入 2 個（`path_ended`）；**Forward 與 Backward 的路徑也改變** |
| c＝1e-12 | 訓練集與五個 fold 都 0 個進入；Forward、Backward 改變 |
| 同上，但 LARS 在「置中目標 ÷ 同一批列上的均方根」上計算、entry alpha 乘回 | c＝1e-12～1e6 全部 group 進入，進入順序與 c＝1 相同 |
| 同上，`_pick` 的 tie 改為純相對（`TIE_RTOL·|best|`，只作診斷） | c＝1e-10、1e-12 的 Forward／Backward／RFE 路徑與 c＝1 相同 → Forward／Backward 的改變來自 tie 的 `max(…, 1)` 下限 |
| King County 一致性（`tests/test_explore_kc_consistency.py` 的同一輸入：正式訓練表、ln(price)） | 以上兩種與單位無關的作法（LARS 對目標縮放；tie 純相對，或全部準則在縮放後的目標上計算）都**仍重現**正式分析四條 canonical 路徑 k＝1…18；Lasso 18 個 group 全部進入，最小 entry alpha 6.83e-4，遠高於門檻 |
| 合成資料 `y = 2·x1 + 3`、`x2` 與 `x1` 無關（訓練列相關 −0.05） | `x2` 未進入、`cause = path_ended`：原因是已進入的欄完全擬合目標、殘差為零，**不是**共線或無變化 → 第 65 行的說明在原尺度、無任何數值問題時也可能不屬實 |

R1-F1 的 JS 側探測我沒有重跑；JS 與參照在上述程式點的公式相同，R1 已記錄 JS 在 ×1e-10 得到相同的 Lasso 結果。

## 4. 裁決

### R4-1 （a）分類：路徑在任何原因下提前結束，都套用 A-2 的處理

在某一批列（某 fold 的訓練列，或整個訓練集）上，LARS 路徑結束時若仍有 Feature group 未進入——不論原因是 active set 退化、路徑走到終點時其餘 group 與殘差的相關已為零，或數值上的提前停止（`alpha_increasing`、`max_iter`、同步多個 drop）——一律：

1. 已求得的路徑段（entry alpha 與順序）是實際結果，照常比對；
2. k 超過該批列上已進入 group 數的 Lasso 候選為 `INVALID_MODEL`，原因碼 `lasso_path_degenerate`，並附 scope、fold、已進入數與**真實的停止原因**（R4-2）；
3. 未進入的 group 只作展示並標示未進入，不得稱為實際路徑，不構成任何子集或選模依據；**不得**以 V1 的欄序補齊、不得標 `VALID`、不得改標 `FAILED`、不新增原因碼。

理由：A-2 的操作原則是「路徑沒有可靠給出的候選，不成為有效候選，也不以欄序補齊」，最後一句明定探索模式不沿用補齊——這不限於退化一種情形。其他選項都與 accepted 文字衝突：補齊違反 A-2；`VALID` 沒有子集可擬合；`FAILED` 在 Spec 與 #77 是「非預期例外、整個方法」的狀態，會丟掉 A-2 要求保留的已求得段，而這些停止是確定性的；新增原因碼會改變 accepted 的枚舉。`2069fea` 在這一點上已符合本裁決，不需修改。

### R4-2 （a）原因必須如實，畫面不得宣稱未確立的原因

- 停止原因至少分為：`active_set_degenerate`（A-2 原義）；路徑走到終點（結束判定見 R4-3）時其餘 group 與殘差的相關在數值上為零；以及各自標示的數值停止（`alpha_increasing`、`max_iter`、`multiple_drops`）。原因值的名稱是實作細節，不是新的原因碼。
- 每一種原因對使用者的說明只能陳述已確立的事實。「走到終點」這一類**不得**斷言共線或無變化：它只確立「其餘 group 與殘差的相關在數值上為零，exact LARS 不會讓它們進入」；可能的情形（與已進入的欄線性相依、在這些列上沒有變化、已進入的欄已完全擬合目標）只能以「例如」列出。數值停止的說明必須說明是數值或迭代上限造成，不得說成資料性質。
- Python 參照在能偵測的範圍內給出相同的原因（例如 sklearn 的提前停止警告、迭代數達上限）；參照無法偵測的 JS 停止（`multiple_drops`，worklog §8 觀察 3）照 Brief V2 §8「退化情境不假設 sklearn 的行為」在 worklog 記明差異。**不要求**為每一種數值停止另造 fixture，這不是新 AC。
- `index.html` `#ex-lasso-card` 對 LARS 計算方式與停止的說明（第 136 行）在 R4-3／R4-4 實作後必須仍然屬實（H-4）；這是 V2 探索子樹的文字，不受 V1 文字不變量約束。

### R4-3 （b）結束判定**必須**與目標的單位無關

**要求的性質**：對任何正常數 c，以目標 c·y 執行 Exploratory run，與以 y 執行相比，每一批列上 Lasso 路徑的結束點、已進入數、進入順序（含 tie 叢集）、停止原因、候選狀態與原因都相同，entry alpha 為原值乘以 c；只要 c·y 與中間量仍在 double 的正常有限範圍內。

**約束**：

1. 回報的 entry alpha 維持 accepted 的定義與尺度：sklearn 的 alpha、對**原始目標置中**的路徑（Q21；V1 `lasso_entry`）。
2. 演算法仍是 exact LARS（含 Lasso 修正），A-2 的退化判定照舊。可行的作法例如：以同一批列計算的正值尺度（例如置中目標的均方根）除目標後執行 LARS，再把 alpha 乘回——exact LARS 的路徑對目標縮放等變，節點、順序與係數比例不變，只有數值門檻變成無單位。**只把 `EQ_TOL` 換成另一個絕對值不符合本裁決。**具體作法是 HOW，由 Executor 決定。
3. 尺度若需要統計量，只能取自與該路徑相同的列（第三層：該 fold 的訓練列；canonical：整個訓練集），不得讀驗證列或 test 列（SR-V2-01）；必須是確定性的（可重現性的確定部分）。目標在該批列上沒有變化時不得除以零，Lasso 沒有 group 進入，原因如實說明。
4. JS 引擎與 Python 參照採用相同的判定；Node 對 Python 的 entry alpha 相對 1e-6 照舊。
5. 正式分析不變：`hw2/selection.py` 與其他正式路徑模組不修改；`tests/test_explore_kc_consistency.py` 不修改且必須通過（第 3 節已確認兩種作法都可行）。
6. 50 Startups（c＝1）在原尺度的 17 個候選狀態不因此改變（G-4 的前提照舊）。

**理由（為何是「必須」而不只是「可以」）**：

- Spec 要求 exact LARS 的進入順序；exact LARS 對目標縮放等變，絕對門檻造成的截斷不是 exact LARS 的結果，而是 sklearn 為接近單位尺度的資料設計的數值保護。
- Brief V2 §8 要求非退化資料得到 exact LARS 的順序；第 3 節的 50 Startups ×1e-10 沒有任何退化，卻有候選被標 `INVALID_MODEL`——這不符合 `INVALID_MODEL`「不符合有效性條件」的定義，頁面原因也不屬實（H-4）。+2 的「任意輸入」包含任意單位（Q18 不轉換目標）。
- 「與正式分析相同」不支持另一種讀法：正式分析的目標是 ln(price)，其排序本來就與價格單位無關；A-2 已明定 V2 不照抄 sklearn 對退化的處理。要求單位無關，正是使 V2 在原始目標上保有正式分析所具有的性質。
- 兩種讀法中只有本讀法與全部 accepted 文字相容，所以不是 E-DA/D1。

### R4-4 同一原則適用於以容忍度判定的 tie

R1-F1 只問 Lasso 的結束判定，但第 3 節顯示同一個單位相依也出現在 tie：`TIE_RTOL * max(|v|, 1)` 的下限使準則值小於 1 時 tie 變成絕對容忍度，50 Startups ×1e-10 時 Forward／Backward 的路徑因此改變。Spec 寫的是「**相對**容忍度與正式分析同值」；V1 的準則（ln(price) 上的 RSS、importance、path index）無單位，下限從未造成單位相依。所以：

- Forward／Backward 的 RSS、RFE 的 importance、LARS 進入時的共變 tie、entry alpha 的 tie 叢集，判定結果都必須符合 R4-3 的性質（與目標單位無關）。可行作法例如在 R4-3 縮放後的目標上計算全部準則，或改用純相對容忍度；`TIE_RTOL = 1e-12` 的值不變。HOW 由 Executor 決定，R4-3 的約束 3～6 同樣適用。
- Winner 的比較（CV RMSE 完全相等才平手、取較小 k、方法順序）是 accepted 規則，不受本條影響。

### R4-5 分配：#77 承接

| 對象 | 義務 |
| --- | --- |
| **#77**（V2-T4） | 實作 R4-2、R4-3、R4-4：`assets/explore_engine.js`、`hw2/explore_reference.py`、`assets/explore_app.js` 的原因說明、`index.html` `#ex-lasso-card` 的計算說明，以及對應的 V2 測試。驗證（Executor self-verification，#77 R1 依 H-3 A-2(V2)、H-4 A-5(V2) 自行核對）：50 Startups 目標乘上 c（至少 1e-12、1e-10、1e-9、1e6）時 JS 與 Python 都得到與 c＝1 相同的狀態、子集、進入順序與停止原因，entry alpha 按比例；King County 一致性測試不改且通過；R4-2 的說明屬實（含第 3 節 `y = 2·x1 + 3` 一類「完全擬合」的情形）。這是主 seam 既有要求（exact LARS 進入順序、狀態與原因與參照相同）在 accepted 輸入範圍上的驗證，不是新 AC、新 seam 或新 gate；是否寫成 Node 測試由 Executor 決定（建議寫：R1-F2 已顯示未經測試的分支在 mutation 下存活）。#74、#75 的 V2 測試只能擴充，任何期望值的修改須在 worklog 說明理由，且不得削弱檢查（I-5 只鎖定接受基準的既有測試） |
| **#76**（V2-T3） | 不實作本紀錄的內容。#76 開放任意目標後，小單位目標在 #77 結案前仍會出現 R1-F1 的行為；這是已分配給 #77 的已知項目，不是 #76 的範圍。#76 R1 對它的判斷權照舊，可引用本紀錄 |
| **#78**（V2-T5） | 報告「探索模式」章節與 README 對 Lasso 退化語義的說明，須與 R4-1～R4-4 實作後的行為一致（A-2 的處理涵蓋任何提前結束；停止判定與目標單位無關；原因如實），並照 I-4 不含探索結果數字。這是 #78 既有義務（「Lasso 退化語義」）的內容，不是新 AC |
| **Spec Integration Audit**（Spec V2） | 在整合 subject 上核對 R4-1～R4-4 成立；R1-F2 的知悉事項照 #75 R1 record §6 |
| Orchestrator | 把本紀錄列入 #77 的派工 pack（主要）與 #76、#78 的 pack（知悉） |

選 #77 而不是 #76 的理由：#77 的主題是讓引擎在任意合法資料上穩健、可重現（確定部分），本來就修改引擎的方法迴圈與參照；#76 是輸入、請求隔離與切換。執行順序 #76 → #77 → #78 讓修正在 #78 與 Spec Integration Audit 之前完成。V2 在 #78、Spec Integration Audit、phase acceptance 與 acceptor 的 push／merge 之前不對外發布（OC §5.1），所以 #76 與 #77 之間的落差不會到達使用者。

### R4-6 #75 不重開，可以結案

- #75 R1 為 CLOSURE、沒有 blocking finding；R1-F1 是 routing signal（治理 §4.2），本紀錄已裁決，P6 的「已 route 的 design question 皆有 decision record」由本紀錄滿足。
- R4-1 的分類 `2069fea` 已符合。R4-2～R4-4 的義務由本紀錄分配給 #77，不屬於 #75 被分配的 Work Contract；#75 的 AC 依 R1 record 全部滿足。
- 在 #75 的 subject 內，頁面只能載入原尺度的 50 Startups（17 個候選全部 `VALID`，第 3 節 c＝1 重現）；退化 fixture 中未進入的 group 確實是共線欄。使用者在 #75 的頁面上看不到不屬實的原因。
- 這是同一份 Spec 內的契約內 rework，分配給後續票，不是新工作（治理 §1.2），與 `decision-20261022-r1f3-v1-footer.md` R3-5 的處理相同（不重開已 closure 的票，由後續票的 R1 與 Spec Integration Audit 核對）。

## 5. 是否改變 accepted 語義

**否。**

- R4-1：在 accepted 的狀態與原因碼枚舉內，把 A-2 的操作原則（無法可靠求得的候選無效、不補齊）套用到 accepted 文字沒有寫到的情形；沒有改變 A-2、Spec V2 或任何 AC 的文字，沒有新增狀態或原因碼。
- R4-2：依 H-4 與 Spec「原因必附」對原因標示的要求；原因值是原因碼之下的實作細節。
- R4-3、R4-4：是 accepted 文字（exact LARS、相對容忍度、非退化資料的順序、`INVALID_MODEL` 的定義、任意輸入）的必要條件，兩種讀法中只有它與全部文字相容；回報尺度與 tie 容忍度的值不變；正式分析不變，King County 一致性 AC 不受影響（第 3 節）。
- R4-5、R4-6：分配，不新增 AC、seam、gate 或 scope。

本紀錄屬治理 §5.3 第 2 類，不需 acceptor 核准。沒有我無法確立在 Outcome Contract boundary 內的事項，不需 fail-closed。若之後 #77 的 Executor 或 Reviewer 發現唯一可行的作法會改變回報的 entry alpha 尺度、修改正式分析模組或 King County 一致性測試，該路徑即超出本裁決，須 route 回 Design Authority（可能需 acceptor）。

## 6. 受影響的 work items 與 evidence

| 對象 | 影響 |
| --- | --- |
| **#75** | 不重開；可依 orch-default §7 結案（本紀錄滿足 P6）。其 evidence 對 `2069fea`／`ded2769` 仍有效；#77 修改的部分由 #77 R1 重新驗證 |
| **#77** | 新增分配 R4-2～R4-4 與驗證（R4-5）；G-4 照舊 |
| **#76** | 無實作義務；知悉 |
| **#78** | 報告與 README 的 Lasso 退化說明依 R4-5 |
| Spec Integration Audit、DA phase acceptance | 核對 R4-1～R4-4 在整合 subject 上成立 |
| `hw2/selection.py`、正式分析、`tests/test_explore_kc_consistency.py`、V1 產物 | 不修改 |
| Outcome Contract、Brief、Spec、`tickets-v2.md`、GitHub issues | 不修改 |

## 7. Evidence

- 讀取：Bindings b5 全文；治理 v2.2 §1.2、§2.1、§2.4、§2.5、§3.3–§3.6、§3.8、§4.2、§5.3；orch-default v2.2 P6 列；`outcome-contract.md` §5、§5.1、§5.2；`BRIEF-V2.md` 全文（§3、§5、§8、§10、§12、§13）；`SPEC-V2.md` 全文；`SPEC.md` rev 5 的 Lasso／tie 相關段落；`derivation-SPEC-V2.md` 全文；`decision-20261022-r1f3-v1-footer.md` 全文；`audit/issue-75-c1-r1.md` 全文；`worklog/issue-75.md` §4 D-3、§8；run record 第 21、139–164 列；`gh issue view 75`／`76`／`77`／`78`（body 與狀態，皆 OPEN）。
- 程式（`git show 2069fea:<path>`）：`assets/explore_engine.js` 第 74–83、619–905 行；`hw2/explore_reference.py` 第 84–101、544–720 行；`assets/explore_app.js` 第 50–80 行；`index.html` 的 Lasso／退化說明（第 126、136、195–203 行）；`hw2/selection.py` 第 1–56、108–118、222–257 行；`tests/test_explore_kc_consistency.py` 第 1–60 行。
- 執行（`.venv` 的 Python；腳本在 session scratchpad `da_r1f1/`，不進 repo，只讀 repo）：50 Startups 目標縮放探測（`probe.py`）；King County 一致性在兩種單位無關作法下的重現（`kc.py`，讀正式訓練列，不讀 test 列）；完全擬合合成資料（`exactfit.py`）。結果見第 3 節。
- `git log --oneline -3`（HEAD `ee0c481`）；`git diff --stat 2069fea HEAD -- home_work_02/hw2 home_work_02/assets home_work_02/tests`（空）。
- 本 assignment 的 transcript binding（標頭）。
- 寫入的檔案只有本紀錄；沒有修改契約、Spec、票、程式、測試或其他紀錄；沒有 commit。
