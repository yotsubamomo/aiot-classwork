# Worklog — #75 HW2 V2-T2（四種特徵選擇方法、候選狀態、winners、Lasso 退化與共線診斷）

- **Work item**：GitHub issue #75（V2-T2），Formal lane，run `run-20261022-hw2-v2-enhance`（Orchestrator＝root session `37216426-f292-44f9-bad1-e2d862e7b8f1`）。
- **執行角色**：Executor（治理 §2.1；`gov-executor`，有效 mapping `claude-opus-5-5`／`high`，Bindings b5 §3.1 O-1）。
- **Subject**：branch `home_work_02-v2-enhance`（未 push）。BASE `3dfba2d9ebf2e4589845b06021693636d7156d27`（#74 結案後）；實作 commit `2069feacdd73968044a83d69dc37bc894dfd8cad`；之後的紀錄 commit 只改 `doc/`（本 worklog、`doc/acceptance/ACCEPTANCE.md` 的 V2-10～V2-17 與 V2-3 的一處指向、`doc/screenshots/v2-issue75/` 的證據），沒有程式、資料或測試的變更。
- **狀態**：實作與 self-verification 完成，待 independent audit（R1）。

## 1. Contract reference

| 契約 | 位置與版本 |
| --- | --- |
| Outcome Contract | `doc/governance/outcome-contract.md` §5（V2 接受紀錄，接受基準 `d7f02d4`）、§5.2 CC-V2-1（只有那一條 `<script src>` 斷言可改；本票沒有新增腳本檔，該斷言未動） |
| Ticket | GitHub #75（body sha256 `834a439c…d5`，DA derivation §3） |
| Spec | `doc/spec/SPEC-V2.md` rev 2；未提到的事項以 `doc/spec/SPEC.md` rev 5 為準 |
| Brief | `doc/brief/BRIEF-V2.md` rev 2＋E-1（§12 A-1～A-3）；`doc/brief/BRIEF.md` |
| DA derivation | `doc/governance/decisions/derivation-SPEC-V2.md`：§4 #75 列；§5.2 G-1（探索區塊的切分限制揭露）、G-2（主 seam (d) 小型案例的四種方法）；§7.4 #75 類別 H-1～H-5、assurance A-1～A-5、A-7～A-9；§8 D-2（輸入衍生字串只當資料）；§9 F-5 |
| DA decision | `doc/governance/decisions/decision-20261022-r1f3-v1-footer.md`：頁尾在探索模式隱藏屬 #76（R3-5）；本票不改頁尾、不改切換流程（R3-2 的行為留給 #76，本票新增的區塊都在 `#explore` 內、隨探索模式顯示／隱藏） |
| Run invariants | run record §1 designation 第 4–7 點（經 CC-V2-1）：正式分析、`hw2/` 正式路徑、`model_data`、`results/`、Test evaluation 紀錄、V1 區塊、V1 腳本與核心模組、既有測試不變（#74 的 V2 測試可延伸）；不重跑 notebook、不做新的 Test evaluation；V1 Spec／tickets／Brief、#59–#67 不動；只有四個 seams；追蹤檔案寫 `<學號>`；只改 `home_work_02/` 且不碰 `doc/requirement/` |
| 不在本票 | R1-F2（一般物件鍵，`audit/issue-74-c1-r1.md`）屬 #76；運算預算、`SKIPPED_RESOURCE_LIMIT`／`FAILED`、取消、可重現性屬 #77；README／報告／ZIP 屬 #78 |

## 2. Binding

| 對象 | 觀測（Bindings §3.6 指令，全部 assistant 訊息） | 結果 |
| --- | --- | --- |
| 本 assignment，agentId `a5dedd102dd077202`（`agentType` `gov-executor`） | `('claude-opus-5-5', 'high')`：286 則（截至寫入本節；return 前由派工者依 §3.6 全程核對） | 單一元素，等於有效 mapping；無 escalation、無替代 |

- Bounded assignments：**未使用**（沒有派 `gov-investigator`／`gov-bounded-worker` 或任何 subagent）。

## 3. Work performed

1. **讀取與基準**：Bindings b5、Implementation Profile §3–§5、§9、治理 §3.5、§3.7、§3.8；OC §5／§5.2；Spec V2、Brief V2 §12、`tickets-v2.md`、DA derivation 與 R1-F3 decision、run record；#74 的 worklog、R1／R2 audit、`assets/explore_*.js`、`hw2/explore_reference.py`、V2 測試；正式套件 `hw2/selection.py`、`models.py`、`preprocess.py`、`ols.py`；已安裝的 sklearn 1.9.1 `lars_path` 原始碼（`_lars_path_solver`、`cholesky_delete`、`min_pos`）。
2. **通用 Python 參照** `hw2/explore_reference.py`（仍只供測試）：四條路徑在每個 fold 的訓練列與整個訓練集上計算；重用 `hw2.selection.GroupGram` 的 `rss` 與 `importance`（以 `object.__new__` 建立、只重寫建構子）、`selection.TIE_RTOL`、`models.METHOD_ORDER`／`PATH_METHODS`／`model_key` 與 `determine_winners` 的規則；Lasso 用正式分析同一個 `sklearn.linear_model.lars_path(method="lasso")` 與正式的標準化與 entry 規則，A-2 以 sklearn 自己的 `verbose=2` 紀錄重建每次加入前的 active set 來判定退化；新增 A-3 相依診斷、`lasso_path`、`winners`（`method_winners`、`overall`、`test_keys`、`test_key_of`）、`dependencies`；`canonical_paths()` 接受現成的編碼表，供 King County 一致性測試使用。
3. **引擎** `assets/explore_engine.js`：Forward／Backward SFS（Gram 上的 RSS，最小範數解）、RFE（`sd(X_g β_g)`）、Lasso（sklearn `lars_path` Gram=None 分支的 JS port，含 Lasso 修正、drop、`cholesky_delete`、`np.around(…, 15)`）；A-2 退化；winner 規則與只對 winner 的 test；A-3 相依；`ENGINE_VERSION` 改為 `explore-engine 2 (V2-T2: five methods)`。新程式以陣列索引與 `Map` 表示 group，沒有新增以使用者欄名為一般物件鍵的地方。
4. **頁面**（只改 `#explore` 子樹、`assets/explore_*.js`、`explore.css`）：`ex-model` 改為方法切換、k 格（winner 綠點、無效紅斜紋）、「比較全部方法」、選取摘要（canonical 與各 fold 子集）、訓練 CV KPI、指標 vs k 圖（`explore_plot.js` 的 `KChart`，以頁面已打包的 Chart.js 繪製；指標可切換）、各方法 winner 與整體 winner 比較表、所選候選的各 fold 與 canonical fit、Lasso 路徑表；`ex-data` 加共線診斷；`ex-predictor` 跟隨所選候選；`ex-test` 依 winner 規則展示並提示；新增 `ex-methods`「方法與限制」區塊（兩個 problem 的語義差異表、逐列切分限制揭露，G-1）。沒有新增腳本檔，`index.html` 的 `<script src>` 清單不變。
5. **測試**：新增 `tests/js/explore_methods.test.js`、`tests/test_explore_kc_consistency.py`；延伸 #74 的 `tests/test_node_explore.py`、`tests/js/explore_contract.test.js`、`tests/js/explore_app.test.js`、`tests/test_explore_static.py`（§4 D-10、D-11）。
6. **ACCEPTANCE**：新增 G 節 V2-10～V2-17；V2-3 的「四種方法：PENDING（#75）」改為指向 V2-10。其他條目不變。
7. **瀏覽器 self-verification**（§6.3）與 **H-5 探測**（§6.4），證據在 `doc/screenshots/v2-issue75/`。

## 4. Decisions and assumptions

都在 accepted contract 的 HOW 範圍內；沒有改變 requirement、AC、invariant 或 gate。

| # | 決定 | 依據 |
| --- | --- | --- |
| D-1 | All-in（`VALID` 時）是自己方法的 CV winner，列在 `method_winners.allin`，因此一定在 test 集合中；test 集合＝All-in、各方法 winner、整體 winner，canonical 子集相同者只算一次，代表鍵依 All-in → 各方法依方法順序 → 整體 winner 的先後 | Spec V2「切分與交叉驗證」第 5–7 點沿用正式分析；`hw2/models.py::determine_winners`（`allin.is_method_winner = True`、authorized test set、`test_model_key`）；#74 已把 All-in 放在 test |
| D-2 | `winners` 不含浮點數（只有鍵與 k），讓 Node 與 Python 可逐值比對；方法沒有 `VALID` 候選時其 winner 為 `null` | 結果契約形狀屬 HOW；Spec「winner 只從 VALID 候選選」 |
| D-3 | Lasso 退化（A-2）的操作定義：要加入的欄在已加入欄上的殘差 ≤ 其範數的 1e-6（`LARS_DEGENERATE_RTOL`），或低於 sklearn 自己的 pivot 下限 1e-7；或路徑結束時仍有 group 未進入（`cause = path_ended`）。已進入的 group 數為 `n_entered`，`first_invalid_k = n_entered + 1`，k ≥ 該值的 Lasso 候選 `INVALID_MODEL`／`lasso_path_degenerate`（原因附 scope、fold、`n_groups_entered`、`cause`）；未進入的 group 依 CSV 欄序列在後面、只作展示，不構成任何子集 | Brief V2 §12 A-2（停止、保留已求得段、k 超過者 INVALID、補齊順序不得稱為實際路徑）。sklearn 的 1e-7 絕對門檻在標準化欄（範數² ≈ n）上對完全相依欄不可靠（√(eps·n) 量級），所以加上相對門檻 |
| D-4 | JS 的 Lasso 是 sklearn `lars_path`（Gram=None）的逐步 port；唯一差異：在 `|Cov|` 相差 ≤ TIE_RTOL 的平手中取 CSV 欄序最前的欄（sklearn 取其內部排列的第一個） | Spec「tie 依 canonical 順序＝CSV 欄序（forward／Lasso 先加前者）」；只影響完全平手（例如完全相同的兩欄） |
| D-5 | Lasso 排序：entry alpha 由大到小；相鄰 alpha 差 ≤ TIE_RTOL·max(|α|, 1) 的連鎖視為平手，平手內依 CSV 欄序 | Spec「最大 entry alpha 先；tie（與正式分析同值的相對容忍度）依 canonical 順序」；正式 `TIE_RTOL = 1e-12` |
| D-6 | Forward／Backward／RFE：沿用正式 `GroupGram`（置中、單位範數欄、最小範數解）與 `_pick` 規則；JS 的最小範數解在 Cholesky 樞軸都 > 1e-8·max 對角時用 Cholesky，否則以 Jacobi 特徵分解做 pseudo-inverse（截斷 eps·m·λmax，同 numpy `lstsq` 的 rcond） | 正式準則；HOW |
| D-7 | A-3 診斷：整個訓練集 canonical 編碼的 All-in 設計（截距＋編碼欄），欄等化後依序做兩次 Gram–Schmidt；殘差 ≤ max(n, p)·eps（`hw2/ols.py` 的秩容忍度）的欄形成一組關係（一欄一組）；關係係數正規化為最大絕對值 1、第一個非零為正、|c| ≤ 1e-9 視為 0；每組列出全部涉及的編碼欄、feature group、是否含截距，不指認單一欄。`REJECTED` 的結果也帶 `dependencies`（Spec「全部無效時…並顯示相依診斷」） | Brief V2 §12 A-3；Spec「秩不足與共線診斷」（方法由實作決定） |
| D-8 | 頁面：預設選取整體 CV winner；test 區塊——所選候選是 winner 就展示自己，否則展示該方法 winner 並提示，該方法沒有 `VALID` 候選則展示整體 winner 並提示；比較表常駐顯示，「比較全部方法」控制圖上各方法的強調；指標 vs k 圖放在 V2 繪圖模組（`KChart`），使用頁面已打包的 Chart.js | Spec「選取非 winner 時 test 區塊展示該方法 winner 並提示」；Tickets Review 調整 A（V2 獨立繪圖模組，可用既有圖表函式庫） |
| D-9 | 不新增腳本檔（全部放在既有 V2 檔案），CC-V2-1 的 `<script src>` 斷言與 `tests/test_dashboard_static.py` 不動 | I-5、CC-V2-1 |
| D-10 | #74 的 A-1 fixture 期望由 `REJECTED` 改為 `COMPLETED`（`a1_fold_rank_deficient`、`a1_small_df`、`a1_collinear`）：五種方法上線後較小的子集有效，依 Spec 只有「所有候選皆非 VALID」才拒絕；A-1 原因改在 All-in 候選上核對（規則、fold 不變），`a1_no_groups` 仍是 `REJECTED` | Spec「winner 只從 VALID 候選選；所有候選皆非 VALID 時…拒絕」；這些是 #74 的 V2 測試（可延伸），預期值是 All-in-only 切片的產物 |
| D-11 | 退化 fixture（`degenerate_mixed`、`a1_collinear`）在 Node 對 Python 比較時，把「兩欄完全相同」的 twin 名稱映射到前一欄後再比較，其餘逐值比較（含數值）；twin 安排成最弱的預測欄，使退化步不受浮點平手影響 | AC「不假設 sklearn 在退化情境的最小範數解或唯一順序」；D-4 的平手差異只會改變 twin 的名稱 |
| D-12 | King County 一致性：輸入為正式 split 的訓練列、`fit_preprocessor` 的 18 個 group 編碼（zipcode one-hot 標為 one-hot）、ln(price)；比對正式分析記錄的 `results/tables/cv_by_method_k.csv` 四條 canonical 路徑（k = 1…18），All-in 比對正式 `models.fit_model` 的係數與表中的 R²／Adjusted R²。測試不引用 `model_data` | #75 AC；DA A-3（探索相關檔案不引用 `model_data`）；DA TR-01（只讀訓練列） |

**觀察（給 Reviewer，不需決定）**：完全相同的兩欄若有一欄是**較早**進入的強預測欄，twin 會在之後每個節點與新進入的欄平手；JS 依 D-4 先試 twin 而在 k = 2 停止，sklearn 依內部順序可能先加其他欄、較晚才遇到退化。兩者都標退化，只是退化步不同（以 `x1, twin=x1, x2, x3` 實測：JS 的 canonical 路徑停在 1 個 group，Python 參照 3 個）。這正是 Brief V2 §8「不假設 sklearn 唯一順序」所指的情形；這類資料的 JS 行為由 `tests/js/explore_methods.test.js` 的 A-2 twin 測試固定，主 seam 的退化 fixture 不使用這種配置。

## 5. Artifacts

實作 commit `2069feacdd73968044a83d69dc37bc894dfd8cad`（13 個檔案，+2,454／−203，`git diff --shortstat 3dfba2d 2069fea`；全部在 `home_work_02/` 內，不含 `doc/`）：

- 修改：`assets/explore_engine.js`、`explore_app.js`、`explore_ui.js`、`explore_plot.js`、`explore.css`、`index.html`（只在 `#explore` 子樹內新增／修改）、`hw2/explore_reference.py`、`tests/test_node_explore.py`、`tests/js/explore_contract.test.js`、`tests/js/explore_app.test.js`、`tests/test_explore_static.py`。
- 新增：`tests/js/explore_methods.test.js`、`tests/test_explore_kc_consistency.py`。
- 不變：`assets/app.js`、`hw2core.js`、`model_data.js`、`style.css`、`vendor/`、`results/`、`hw2.ipynb`、其他 `hw2/*.py`、`tests/test_dashboard_static.py` 與其他既有測試、`doc/spec/`、`doc/ticket/`、`doc/brief/`、`doc/requirement/`、`.gitattributes`。

紀錄 commit：本 worklog；`doc/acceptance/ACCEPTANCE.md`（V2-10～V2-17、V2-3 一處指向）；`doc/screenshots/v2-issue75/` 五張截圖（256 色量化）與四份 `ui_check_*.json`（不含本機路徑）。

## 6. Verification

### 6.1 自動測試

| 時點／subject | 指令 | 結果 |
| --- | --- | --- |
| BASE `3dfba2d`（修改前，#74 結案紀錄） | `.venv/Scripts/python -m pytest -q -rs` | 433 passed、0 skipped（R2 紀錄；本票開始時的基準） |
| 工作目錄＝`2069fea`（`git status` 對 `home_work_02/` 為空） | `.venv/Scripts/python -m pytest -q -rs`（Python 3.11.2） | **442 passed，0 skipped**，53.57 s |
| 同上 | `node --test --test-reporter=tap tests/js/<f>.test.js`（Node v24.19.0） | `explore_load` 15、`explore_boundary` 7、`explore_app` 12、`explore_methods` 7 pass；皆 0 fail、0 skipped |
| 同上，參照寫到 scratchpad 後直接執行 | `HW2_EXPLORE_REFERENCE=<dir> node --test tests/js/explore_contract.test.js` | **16 pass，0 fail，0 skipped**（PRNG、載入對照、winner 注入案例、10 個 case、A-1、50 Startups 狀態、內嵌文字） |
| 同上 | `python -m hw2.offline_scan` | `scanned 13 files: PASS (0 findings)` |

主 seam 的 case：(a) 50 Startups；(b) synthetic 非退化（`synthetic_mixed`、`edge_all_numeric`）；(c) synthetic 退化 `degenerate_mixed`（`x_sum = x1 + x2`、`dup_b = dup_a`、All-in 無效）與 `a1_collinear`；(d) G-2 的恰好 20 列、單一類別欄、全部數值；A-1 的 fold 秩不足、df_resid < 3、無 feature group。每個 case 比對載入、切分、欄位狀態、每個候選（All-in 與 4×p 個 (方法, k)）的狀態與原因、各 fold 子集／層級／指標／係數、CV 平均與標準差、canonical 子集與 fit、Lasso 路徑（訓練集與五個 fold 的 entry alpha 與順序、未進入、退化）、相依診斷、winners、test（1e-6；covered 逐值）。Lasso drop（Lasso 修正）在 `a1_small_df` 的路徑中出現 5 次，JS 與 sklearn 相同。

其他：聚合（以閉式簡單回歸手算五個 fold 的指標，CV 平均與樣本標準差相符；Python 端對所有 case 的 `VALID` 候選核對算術平均）；凍結（JS 與 Python 各一：改動 test 列目標值，候選、winner、Lasso 路徑、相依診斷完全不變，只有 test 數字改變）；三層邊界延伸到路徑（fold 3 的驗證列改值與新層級不改變 fold 3 的子集、fit、層級與 Lasso 路徑；test 列改動不改變任何 canonical 子集、fit、路徑與 winner）；winner 平手（注入候選：同 RMSE 取較小 k、方法間依方法順序、共用模型只算一次；Node 與 Python 一致）；King County 一致性（四條 canonical 路徑 72 個子集全部與記錄相同；All-in 係數 rtol 1e-12、R²／Adjusted R² rel 1e-12）。

**Mutation 檢查**（事後以備份還原並 `cmp` 確認）：JS entry alpha 錯一個節點 → 1 失敗；JS 方法內平手改取較大 k → 2 失敗；JS 平手方向反轉 → 1 失敗；Python 方法內平手改取較大 k → 2 失敗；關掉 JS 的退化檢查 → 起初 0 失敗（fixture 都以 `path_ended` 結束，沒有「嘗試加入時退化」的案例），因此新增 `explore_methods` 的 A-2 twin 測試，之後 → 1 失敗。RFE importance 改成變異數而非標準差 → 0 失敗（同序的等價變異，不影響排序）。

**50 Startups 候選狀態**（Python 參照與 JS 相同；數字只作 self-verification 證據，不進 README 或報告，I-4）：

| 方法 | k = 1 | k = 2 | k = 3 | k = 4 |
| --- | --- | --- | --- | --- |
| All-in | — | — | — | VALID（R&D Spend、Administration、Marketing Spend、State） |
| Forward SFS | VALID（R&D Spend） | VALID（＋Marketing Spend） | VALID（＋State） | VALID（全部） |
| Backward SFS | VALID | VALID | VALID | VALID |
| RFE | VALID | VALID | VALID | VALID |
| Lasso 路徑排序 | VALID | VALID | VALID | VALID |

四種方法的路徑相同；方法 winner 都是 k = 1（CV RMSE 相同），整體 winner 依方法順序為 Forward SFS k = 1；All-in 也是自身 winner；test 只算 `allin` 與 `forward_sfs_k01` 兩個模型。Lasso 在訓練集與五個 fold 都沒有退化；相依診斷 0 組。

### 6.2 不變量核對（A-3、I-5、CC-V2-1）

- `git diff --name-only 3dfba2d 2069fea`：13 個路徑全部在 `home_work_02/`；對 `doc/`、`results/`、`hw2.ipynb`、`assets/app.js`、`hw2core.js`、`model_data.js`、`style.css`、`vendor/` 為空；既有 `hw2/*.py` 只有 `explore_reference.py`（#74 新增的參照模組）變更；既有測試中被修改的只有 #74 新增的 V2 測試。
- `tests/test_explore_static.py`：V1 區塊結構快照相同、V1 檔案 sha256 等於 A-3 值、`git diff d7f02d4` 對 V1 檔案為空、探索檔案不含 `model_data`／`MODEL_DATA`／`test_inputs`／`HW2Core` 與寫入 markup 或執行字串的 API、沒有 `fetch(`、正式路徑不 import 參照。
- 學號：`tests/test_repo_hygiene.py` 通過（包含在 442 中）。

### 6.3 瀏覽器（AC「UI（人工檢查表）」；Executor self-verification）

- **方法**：scratchpad 的 `ui_check.js`，以 DevTools Protocol 驅動 headless Google Chrome 155.0.8059.85 與 Microsoft Edge 155.0.4283.62，開啟 `2069fea` 的 `git archive` 匯出（`index.html`＋`assets/`）的 `file://` 頁面；網路以 `Network.emulateNetworkConditions` offline、`--host-resolver-rules=MAP * ~NOTFOUND`、無效 proxy 三種方式封鎖，記錄每個請求、例外、console 錯誤與 dialog。Windows 11 Pro 10.0.26200，Intel Core i9-13900HX。另以同一匯出、只替換內嵌資料的兩份頁面（合成退化資料、H-5 探測資料）執行。報告：`doc/screenshots/v2-issue75/ui_check_startups50_chrome.json`、`ui_check_startups50_edge.json`、`ui_check_degenerate_chrome.json`、`ui_check_h5_probe_chrome.json`。
- **50 Startups（Chrome 與 Edge 相同）**：五個方法按鈕；預設選取整體 winner Forward SFS k = 1；比較表 5 列，訓練 CV 與探索 test 分欄；指標 vs k 圖已繪製（非白像素 Chrome 16,157、Edge 16,040），切到 R² 摘要改變；「比較全部方法」按下時淡化圖例 0、放開 3；四個路徑方法選 k = 2 時 test 區塊展示該方法 k = 1 的 winner 並顯示提示，選 winner 時沒有提示；預測器跟隨所選候選（k = 1 一個輸入、k = 2 兩個、All-in 四個）；比較表的方法按鈕選取該 winner；非 winner 有 test 數字的候選 0 個；六個探索區塊標題都有「探索執行，非正式評估」。**執行時間**（頁內 change handler，連續 5 次，含載入、五種方法與繪製）：Chrome 10.3～42.6 ms、Edge 13.5～44.4 ms；最後一次 controller（載入＋引擎）Chrome 4.4 ms、Edge 6.7 ms。不設門檻。
- **合成退化資料（Chrome）**：k 格無效標示 Forward／Backward／Lasso k = 6、7，RFE k = 5、6、7；All-in 無效，比較表該列「沒有有效（VALID）的候選」；選 All-in 時 test 區塊展示整體 winner 並提示；選 Lasso k = 6：KPI 區顯示「無訓練 CV 指標」與 6 條 `lasso_path_degenerate` 原因，預測器 `aria-disabled=true`、無數值，圖上該點為叉號加選取圓圈；Lasso 表 5 列實際路徑、x_sum 與 dup_b 標「未進入（退化後，只作展示）」；共線診斷 2 組（`x1 + x2 − x_sum ≈ 0`、`dup_a − dup_b ≈ 0`）；change handler 30.7～72.4 ms，engine 19.5 ms。
- **共通**：375／768 px 水平溢出皆 0（三份頁面）；探索區塊可見文字最低對比 6.49:1（50 Startups，341 處）、6.47:1（退化資料，380 處）；對外請求 0（非 `file:`／`data:`）、例外 0、console 錯誤 0、dialog 0；切回 King County 後五個 V1 區塊 `innerText` 與切換前逐字相同、沒有「探索」字樣。
- 截圖：`chrome_startups50_1280_full.png`、`chrome_startups50_nonwinner_1280_full.png`、`chrome_startups50_375_full.png`、`chrome_degenerate_invalid_1280_full.png`、`chrome_h5_probe_1280_full.png`。目視沒有缺字方塊；頁尾在探索模式仍顯示（R3-2 屬 #76）。
- 限制：headless 瀏覽器由 Executor 驅動，不是 acceptor 的人工操作；真實觸控、螢幕閱讀器、Firefox／Safari 未測（AD-1 best-effort）。

### 6.4 H-5 探測（A-9 的同一風險；self-verification，不是 R1 證據）

探測頁的欄名為 `<img src=x onerror="document.title=1">`、`</script><b>bold</b>`、`javascript:alert(1)`，類別值為 `<svg onload=alert(1)>`、`a&amp;b`、`"><iframe src=//evil.example>`（RFC 4180 引號）。Chrome、斷網：`run = COMPLETED`（17 個候選；整體 winner 為 All-in，屬方法間平手依方法順序）；這些字串在選取摘要、比較表、各 fold 子集、Lasso 表、預測器 label 與下拉中都以字面文字出現；`#explore` 內 img／svg／iframe／script／b 元素 0；`document.title` 未變；dialog 0、例外 0、對外請求 0；切回 King County 內容逐字不變。新程式寫入 DOM 只用 `textContent`、`createTextNode`、`<option>.text` 與非 URL 屬性；圖表標籤經 Chart.js 的文字選項；`tests/test_explore_static.py` 的 API 禁用清單照常通過。

## 7. Audit status

- Formal：本票 independent audit **required**（Bindings §5；治理 §4.1；DA derivation §7.4：H-1～H-5，A-1～A-5、A-7～A-9）。由 Orchestrator 依 Bindings §3.7 派工；本 worklog 不記錄 audit 結果。
- 以上 §6 全部是 Executor self-verification，不是 audit。

## 8. Remaining work and concerns

- **本票範圍內**：無未完成項目。
- **留給後續票（依 tickets-v2 與 DA 分工）**：R1-F2 一般物件鍵（`levelsOf`、`inputsOf`、`n_unseen_by_group`、`explore_load.js` 的 `seen`，皆為 #74 既有程式；本票新程式未新增此類用法）與 R3-2 頁尾隱藏（#76）；運算預算與 `SKIPPED_RESOURCE_LIMIT`／`FAILED`、取消、非阻塞、可重現性（#77；目前中型以上的自訂資料沒有預算保護，四種方法在瀏覽器內同步執行）；README、報告探索章節、ACCEPTANCE 彙整、OV-1 重做、ZIP（#78）。
- **觀察（給 Orchestrator／Reviewer，不需決定）**：
  1. §4 的 D-4／D-11 與「觀察」：完全相同兩欄的 LARS 平手，JS 依 Spec 取 CSV 欄序，sklearn 依內部順序；比較只在 twin 名稱上放寬。
  2. Lasso 沿用 sklearn 的 `equality_tolerance`（alpha ≤ float32 eps 即停止）。目標尺度極小（例如 |y| 約 1e-7 以下）的資料，Lasso 路徑會立即結束，Lasso 候選全部 `lasso_path_degenerate`；正式分析的 `lars_path` 呼叫相同。50 Startups 與 fixture 不受影響。
  3. JS 在同一步有多個係數同時歸零（`multiple_drops`）時停止路徑，sklearn 會繼續（其狀態在該情形下不一致）；實務上不會出現，參照沒有對應的偵測。
  4. 執行環境副作用：瀏覽器檢查除錯期間，我在 shell 執行了 `taskkill /F /IM chrome.exe`，這會結束本機所有 Chrome 行程（包括 acceptor 可能開著的視窗），不只 headless 實例。對 repo 沒有影響；之後的檢查只以 PID 結束自己啟動的行程。
- **Push**：未 push（OC §5.1 未授權）。
