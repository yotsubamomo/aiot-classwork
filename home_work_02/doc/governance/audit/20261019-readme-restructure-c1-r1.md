# Audit record — `20261019-readme-restructure` R1（cycle 1）

| 欄位 | 內容 |
| --- | --- |
| Work Contract | Lightweight Outcome Contract：acceptor 2026-10-19 的直接指示，原文引用於 worklog `doc/governance/worklog/20261019-readme-restructure.md` §1（Bindings §2.3）。有約束力的 derived 限制：DA `doc/governance/decisions/decision-20261019-post-merge-ad3-readme.md` 第 3 節（D-R1～D-R5、RT-1～RT-6） |
| 受審 subject | branch `home_work_02-readme-restructure`，最終 commit `dcb605222f99b3e5f469669b0128b4033fdb1723`；implementation commit `ccdc9f25aa5bd56732df9948326d293644e9f4b5`；本 work item 的 delta＝`git diff 1862a41 dcb6052`（parent `1862a41` 是 AD-3 work item，另行審查）。Subject tree `0597b009d7b05f88c07ba65bfbc8d9d2e5f1780c` |
| Audit 種類 | R1（full independent audit of accepted work scope；治理 §4.4）。Lightweight，不適用 Spec Integration Audit（治理 §4.7 末段） |
| Round／cycle | R1／cycle 1 |
| 角色 | `primary_reviewer`（`gov-primary-reviewer`） |
| Audit 依據 | DA 紀錄 §3.5：required（H-2 README 的流程與成果、H-1 學號設定的記載）；R1 要核對 D-R2、RT-1～RT-6，並自行執行 A-4 的學號比對 |

## Assurance（Bindings §5）

**(a) Context independence（治理 §2.3 四項 properties）**

1. **Independent context**：以 Agent tool 派工的非 fork `gov-primary-reviewer` subagent，從空白 context 開始。派工內容只有路徑、識別與 DA 紀錄位置，沒有 Executor 的結論或摘要。Worklog 的陳述（測試數量、反向檢查、目視確認、HW01 結構對照）一律當作待驗證主張，下文的證據都是我自己取得的。
2. **Verifiable binding**：definition frontmatter 綁定 `claude-opus-5-5`／`xhigh`。審查期間以 Bindings §3.6 的方式觀測本 session 的 subagent transcript：agentId `a33ffc18f0df1bd1e`（`meta.json` description「README restructure R1 audit」，`agentType`＝`gov-primary-reviewer`）在觀測當下為 `('claude-opus-5-5', 'xhigh')` 121 則，只有一個元素。全程核對（含之後的訊息）由派工者在採用本 return 前執行。
3. **Autonomous access**：自行以 `git show`／`git diff`／`git cat-file`／`git grep` 讀取 subject 的 commit 物件，不讀工作樹的追蹤檔案作為證據。測試在 `git archive dcb6052` 解出的 scratch 複本上執行。該複本的 tree hash 與 subject 相同（`0597b009…`），並放在 session scratchpad 內獨立的 scratch git repo 中，讓 hygiene 測試的 `git` 指令可以執行。專案 repo 沒有任何 git 寫入；審查前後 `HEAD`＝`dcb6052`，追蹤檔案沒有修改。
4. **Self-written record**：本紀錄由我以 Write 工具寫入 Bindings §7 的路徑。

**(b) Model diversity**

- Executor：`gov-executor`，agentId `ab07c6cd5d35d7f6f`（description「HW2 README restructure Executor」）。我自己掃描該 transcript：`('claude-opus-5-5', 'high')` 95 則，只有一個元素，等於 O-1 mapping。worklog §2 記的是寫 worklog 前的 78 則，派工者的全程核對尚未記入 worklog。
- 本 review：`claude-opus-5-5`／`xhigh`（同上）。
- 兩者同為 `claude-opus-5-5`：**無 model diversity**。依 Bindings §5，這不影響 independence 的判定，也不主張 diversity。

## 1. 審查方法

- 讀取：Bindings b5（全文）；治理 v2.2 §2.3、§4.1～§4.7；impl-default v2 §6、§7；DA 紀錄 `decision-20261019-post-merge-ad3-readme.md`（全文，以 Q3 為準）；`decision-20261018-high-risk-categories.md`；`decision-20261018-issue64-notebook-rerun.md` N-5；`decision-20261018-issue60-a4-student-id.md` S-1～S-6；Brief §3、§4、§8；老師原文 `doc/requirement/` 兩份轉寫；`report/report.md` 的標示對照表；`home_work_01/README.md`（subject 中的版本）；worklog（`dcb6052`）。
- Subject：`git diff 1862a41 dcb6052` 的 6 個檔案，以及 README、`tests/test_report.py` 在 `dcb6052` 的全文。
- 自己執行：完整 pytest（scratch 複本）；README 測試的反向檢查（自寫 `mutate_check.py`，只用假數字）；A-4 只輸出計數的學號比對（自寫 `a4_counts.py`）；兩張截圖的 sha256、尺寸、PNG chunk 與目視；截圖與 README 的數字對照匯出結果；README 的相對連結與外部 URL；重跑步驟指令區塊的比對；路徑範圍。

## 2. Accepted scope 與 D-R2 逐項

| 項目 | 結果 | 證據 |
| --- | --- | --- |
| Acceptor 指示：改版 README、參考 HW01 | 符合 | HW01 的 heading 序列（專案資料、Live Demo、專案摘要、已實作功能、作業要求對應、資料來源、技術棧、專案結構、本機執行、驗證紀錄、詳細文件）在新 README 都有對應（README:3、11、24、40、65、82、109、152、121、184、190）。Worklog §4 的對照表與 subject 相符。版面是否符合期待由 acceptor 自己檢視（D-R2 第 7 點），不列入判定 |
| Acceptor 指示：學號設定（打包用）的資料不要加入 | 符合 | 見 D-R2 第 1 點 |
| D-R1（derived 義務修訂） | 符合 | README 不記載學號設定；`.gitignore` 與 `hw2/**` 不在 delta 中（路徑範圍見下） |
| D-R2 第 1 點（必須移除） | 符合 | `git diff 1862a41 ccdc9f2 -- home_work_02/README.md`：「學號設定（打包用）」小節（標題與兩段）與 `.local/packaging.json` 表列已刪除。在 `dcb6052` 的 README 中，`學號設定`、`packaging.json`、`student_id`、`.local/` 都是 0 次。README:142 的表改名為「本機、不進 git 的材料與輸出」，只剩 `acceptor_materials/`、`dist/`、`.venv/` 三列 |
| D-R2 第 2 點（可以保留） | 符合 | README:63、74、149 只用 `<學號>` 佔位；README:38 的「學號 ZIP」；README:133 的註解逐字是「作者繳交前的打包步驟，需要本機、不進 git 的輸入」 |
| D-R2 第 3 點（必須維持） | **部分不符，見 F-1** | 七項 heading 一對一（README:34、82、87、98、121、11、152）；Pages URL 在 README:9、13、19；「唯一一次正式評估、重跑是重現」段（README:137）與 `## 成果`（README:98～107）在 diff 中沒有變動；數字單一來源見第 4 節。三種標示：dashboard 標為課堂口頭要求（README:11、22、53、79），採用的補充建議標「依老師補充建議」（README:50、78）。但 README:46 把專案決定的 sha256 核對標為〔老師要求〕（F-1） |
| D-R2 第 4 點（截圖） | 符合 | 見第 5 節 |
| D-R2 第 5 點（非範圍） | 符合 | `git diff --name-only 1862a41 dcb6052` 的 6 個路徑：`README.md`、`doc/acceptance/ACCEPTANCE.md`、worklog、兩張 PNG、`tests/test_report.py`。沒有 `hw2/**`、`.gitignore`、報告、notebook、dashboard、`results/` 或 root 檔案。單元目錄外的路徑 0 個，`doc/requirement/` 內的路徑 0 個（RB-5） |
| D-R2 第 6 點（release gate） | 符合 | 兩版 README 的 bash 區塊都是 8 行，只有第 8 行（`hw2.package`）的註解不同；去掉註解後的指令完全相同。所以可以引用既有的實跑證據：`worklog/issue-67.md` §5～§7 與 `audit/spec-SPEC-c1-r1.md` §4.1，兩者在 subject 中都存在。Bindings §5：`git ls-tree` 沒有 `.env`；delta 新增行中各種金鑰樣式 0 命中 |
| D-R2 第 7 點（HW01 結構元素記入 worklog） | 符合 | worklog §4 的表 |
| D-R4（ACCEPTANCE A-8） | 符合 | `ACCEPTANCE.md:33`：檢查文字已刪去設定路徑，並加註「不記載學號設定（DA … D-R1）」；狀態指向本 worklog §6。Diff 只改 A-8 一列，A-7、C-16 不變。`tests/` 中沒有任何斷言檢查 A-8 的文字（在 `1862a41` 與 `dcb6052` 都以 grep 確認） |
| D-R5（不另建說明位置） | 符合 | Delta 中沒有新建的說明文件。新增的追蹤檔只有兩張 PNG 與 worklog |

## 3. D-R3 README 測試（RT-1～RT-6）

| # | 結果 | 證據 |
| --- | --- | --- |
| RT-1 | 符合 | `tests/test_report.py:209-220`：「學號設定（打包用）」、`.local/packaging.json` 與 `<學號>` 必須出現的斷言都已移除 |
| RT-2 | 符合 | `:228-230`。反向檢查：舊版 README（`1862a41`），以及分別加入四個字串的變異，都只被這條測試擋下 |
| RT-3 | 符合 | `:235-238`。反向檢查：前綴改成 10 位假數字、不含角括號的「學號」、空前綴、`dist/<假數字>_hw2.zip`，都被擋下；不要求 `<學號>` 出現。失敗訊息只給 offset |
| RT-4 | 符合 | `:241-244`：數字串的起點在「學號」之後 0～12 個字元內就算失敗。這比「整段數字落在 12 個字元內」更嚴。反向檢查：7 位、12 字元內的 8 位、全形數字（Python `\d` 涵蓋）都被擋下；第 13 個字元起的數字不擋，與 DA 的 12 字元界線一致。`tests/test_repo_hygiene.py` 不在 delta 中；`test_no_tracked_file_contains_the_student_id` 在我的執行中是 **PASSED**（設定存在，不是 skip） |
| RT-5 | 符合（有 Low 觀察 F-3） | `README_ITEMS`（`:206`）：每項恰好一個 heading，七個互不相同。反向檢查：多一個 Dashboard heading、刪「檔案配置」、改名「重跑步驟」、刪 Pages URL，都被擋下。`## 成果`、`## 資料來源與授權`、`## 目的` 的 heading 沒有改名，以它們定位的測試沒有變動。`:272-276` 新增 `## 成果` 以外不得出現六個 Test 結果值；反向檢查中，RMSE、涵蓋率、R²（含 4 位小數）、n_test 寫在成果以外都被擋下，成果內多一個數字也被擋下。N-5 與「方法比較不是要求」兩條測試的斷言沒有變動 |
| RT-6 | 符合 | `git diff 1862a41 dcb6052 --stat -- home_work_02/tests` 只有 `test_report.py`（+41／−4）。被刪的 4 行是舊的 heading 清單與兩個 RT-1 要移除的斷言。新增的行中沒有 `skip`／`xfail` |

**完整測試**（scratch 複本，tree＝subject；`home_work_02/.venv` Python 3.11.2；`python -m pytest -q -rs -p no:cacheprovider`）：**396 passed、2 skipped**。兩個 skip 是 `tests/test_report.py:547`、`:584`，原因是作者材料不在 scratch 複本中（未追蹤，Brief §9）。它們不在 delta 中，與 README 無關。Worklog 在有材料的工作樹上記錄 398 passed，兩者一致。`tests/test_repo_hygiene.py` 17 passed，README 測試 7 passed。Node 測試與 `hw2.offline_scan` 沒有另外執行：`git diff --stat 5d650b1 dcb6052 -- index.html assets results hw2.ipynb` 為空，`hw2/` 也不在 delta 中，而 pytest 內含 Node 一致性測試。

## 4. 數字與內容的核對（H-2、H-3、H-4）

- **`## 成果`**：4,323、183,370、78,100、0.783、94.45、4,083、k = 17，等於 `results/model_data.json`（`dcb6052`）的 `test["forward_sfs_k17"]`（`n_test` 4323、`rmse` 183369.78、`mae` 78100.15、`r2` 0.78338、`coverage` 0.94448、`n_covered` 4083）與 `winners.overall`（`lasso_path_k17`）。`meta.fixture` 為 False。
- **成果以外的各節**：我以 `_NUMBER` 擷取各 `##` 節的數字。專案資料只有日期與 PR 編號；Dashboard、專案摘要、已實作功能只有 95（PI 水準）；目的與流程只有設計參數（k 範圍、80/20、5 fold）；作業要求對應只有老師原文的條件（10–20、100 字）與章節號；技術棧、重跑步驟、檔案配置只有版本與章節號；驗證紀錄、詳細文件沒有數字。沒有任何一節在成果以外陳述結果數字。完成日期「2026-10-19」等於 `5d650b1`（PR #68 merge）的 commit 日期。
- **N-5**：README:137 的原文沒有變動，`test_readme_states_the_one_formal_evaluation_and_reruns_as_reproduction` 通過。
- **H-4（mock／wireframe／fixture）**：README 中 `wireframe`、`mock`、`design/` 都是 0 次；`fixture` 4 次都是既有的工具說明（synthetic fixture 複本、Node 一致性測試），不是數字或截圖。
- **連結**：README 的每個相對連結在 `dcb6052:home_work_02/` 都存在（含 `hw2/selection.py`、`models.py`、`testgate.py`，各檔 docstring 與 README 描述的職責相符）。三個外部 URL（Pages、GitHub repo、Kaggle）以 `curl -L` 取得 HTTP 200（2026-10-19）。
- **其他陳述**：dashboard 的六個區塊名稱與 `index.html` 的 section 一致（`#overview`「A · 概覽」、`#model`、`#predictor`、`#test`、`#methods`；「指標 vs k」、「比較全部方法」）；技術棧所列的套件都在 `requirements.txt`；`hw2/run_notebook.py` 使用 nbclient；樹狀圖列出的 `results/`、`assets/` 子項都存在。
- **作者身分**：README 與 delta 中沒有作者姓名或 email。姓名片段只出現在公開 repo 擁有者 handle 內的 URL，與舊版 README 和 HW01 相同。
- **標示**：見 F-1、F-2。

## 5. 截圖（D-R2 第 4 點；H-1、H-4）

| 檔案 | sha256（自行計算） | 尺寸 | PNG chunks | 目視（我自己開啟兩張圖檢視） |
| --- | --- | --- | --- | --- |
| `doc/screenshots/dashboard-test.png` | `bcd23c76bc6e06807d293bed2061fbedac4a93219dee5070a355f24070568f9d`（＝worklog §5） | 1264×1453 | IHDR、IDAT、IEND（沒有 tEXt／iTXt／zTXt／eXIf 等 metadata） | 只有「E · 保留 TEST 集評估」區塊的元素範圍。沒有瀏覽器網址列、分頁、本機路徑、帳號或學號 |
| `doc/screenshots/dashboard-model.png` | `a03ecd5ab12748f3cf989cac89c5b097873b0e24778745d6e0717573c4ae863f`（＝worklog §5） | 1264×1391 | 同上 | 只有「B · 模型選擇／C · 訓練 CV 表現」區塊。同上 |

- **來源是真實 dashboard，不是 fixture 或 mock**：截圖中的數字我逐一與 `model_data.json` 對照，全部相同。Test 部分：RMSE US$183,370、MAE US$78,100、MSE 3.362×10^10、R² 0.7834、涵蓋率 94.45%、4,083／4,323、平均區間寬度 US$401,052、二項近似 ±0.68%、4,287／36 棟／重複交易、未見 zipcode 0。CV 部分：RMSE US$157,254 ± 35,631、MAE US$75,670 ± 1,060、MSE 2.574×10^10 ± 1.207×10^10、R² 0.8034 ± 0.0847；各方法 CV winner 與 All-in／Ridge／Lasso 的 CV RMSE 158,098／158,098／158,154／157,254／158,154／158,154／158,155。全訓練集擬合：R² 0.8791、Adjusted R² 0.8785、n_train 17,290、87／87、df_resid 17,203、s² 0.033503、t 1.9601。Synthetic fixture 不會產生這組值。
- **不得來自解壓後的 ZIP**：圖中沒有任何路徑或網址列，所以 DA 指出的風險機制（路徑含實際學號）在圖中不存在。擷取來源是否為 repo 內的 `index.html`，我無法從圖本身證明；但影像內容不帶路徑，這一點不影響 H-1 判定。
- **「內容與 Pages 上相同」**（README:15）：`git diff --stat 5d650b1 dcb6052 -- home_work_02/index.html home_work_02/assets home_work_02/results home_work_02/hw2.ipynb` 為空，而 Pages 發布自 `5d650b1`。成立。

## 6. 高風險類別（`decision-20261018-high-risk-categories.md`）

| 類別 | 觸及 | 核對內容與結果 |
| --- | --- | --- |
| H-1 | 是（學號設定的記載、截圖、commit） | **A-4 學號比對（自行執行，只輸出計數）**：比對值從 `home_work_02/.local/packaging.json` 讀取（存在、`git check-ignore` 確認被 `.gitignore:13` 忽略、`git ls-files` 0 個）。範圍是 `origin/main`（`5d650b1`）..`dcb6052` 的 6 個 commit（`6975e22`、`2bd1aeb`、`484f7fd`、`1862a41`、`ccdc9f2`、`dcb6052`），涵蓋 S-2 的 (i)～(iii)：(i) 每個 commit 的 tree，`git grep -F -a` 精確與不分大小寫各 0；(ii) 每個 commit message 0；每個 commit 的 patch（`--text`，含 PNG 的 bytes）在精確、不分大小寫、數字間夾空白／`-`／`_`／`.` 的變形下都是 0；(iii) `test_no_tracked_file_contains_the_student_id` PASSED。兩張 PNG 的原始 bytes 與解壓後的 IDAT 串流也是 0，並且沒有文字 metadata chunk；影像中的文字以目視確認沒有學號（第 5 節）。正向對照：同一種 `git grep -c -a` 寫法在 README 中找到已知字串 `4,323` 2 次；計數函式在合成資料上可以偵測到值與其空白變形。**結果：已核對、無命中。** A-4 的其他項目（作者材料、打包設定與輸出、`.pdf`、`.zip`、`kaggle.json`、金鑰）：`test_no_forbidden_files_are_tracked` 與 `test_untracked_locations_are_ignored` 通過，delta 新增的追蹤檔只有兩張 PNG 與 md／py；金鑰樣式 0。Executor transcript 的觀察見 F-4 |
| H-2 | 是（README 的流程與成果、繳交檔名） | 七項 heading、Pages URL、六個 CRISP-DM 階段、`<學號>_hw2.ipynb`／`<學號>_hw2.zip` 的佔位、`python -m hw2.report`，都由測試強制並通過（第 3 節）；`## 流程（CRISP-DM）`、`## 成果` 沒有變動；dashboard 沒有寫成老師的書面要求（README:22）。合格 |
| H-3 | 間接（README 的數字） | 第 4 節：成果數字等於匯出值；成果以外沒有結果數字；新增的守門有部分缺口（F-3，Low） |
| H-4 | 是（三種標示、截圖） | 截圖是真實匯出的數字（第 5 節）；沒有 mock 或 wireframe；三種標示有一處不實（F-1） |

## 7. Findings

### F-1 — Medium，**blocking**：README 把專案決定的 sha256 核對標為〔老師要求〕

- **證據**：
  - `dcb6052:home_work_02/README.md:46`：「- 〔老師要求〕載入時核對資料檔的 sha256，不符即停止；CRISP-DM 六章依序執行。」
  - 同檔 README:42 說「標示沿用報告的三種標示」。`report/report.md:9` 的定義是「〔老師要求〕作業頁正文的書面要求」，`:11` 是「〔專案延伸〕本專案自行加入的設計，不是老師的要求」。
  - 老師原文 `doc/requirement/HW2-requirements-Multiple Linear regression.txt:21-24`（資料來源）只要求 Kaggle 資料集、10～20 個特徵、標示來源與連結，沒有任何資料檔核對的要求；SRC-2 轉寫也沒有。
  - Brief §4（`BRIEF.md:60`）把「載入時核對 sha256」標為 **[D Q35]**，也就是 acceptor 在 Grill 的決定，不是 [T]。報告標示對照表（`report.md:15-34`）沒有把這一項列為老師要求。
  - 對照：同一節 README:47 的特徵選擇以〔老師要求〕標示，與報告對照表 `:16-17` 一致，並註明方法取自補充段，所以不列入本 finding。
- **依據的契約條款**：
  - Bindings §2.4（每份 Outcome Contract 的 constraints）：ENHANCED／專案範圍「必須維持明確的 scope class 標示，且不得……被呈現為老師要求的行為」。
  - DA D-R2 第 3 點：「三種標示」必須維持，仿 HW01 新增的內容同樣受此約束。
  - 高風險類別 H-4：「三種標示（老師要求／依老師補充建議／專案延伸）混淆」。自動化測試無法檢查這一點，只能靠審查。
- **為何 blocking**：這是 accepted contract constraint 的具體違反，在宣告的高風險類別內，而且出現在老師評分的交付物（README；H-2「README 的流程與成果」）。新增的「已實作功能」是逐點標示，讀者會把這一點讀成老師的書面要求。Branch 尚未合併，修正範圍只有這一行。
- **Closure 條件**：README 不再把 sha256 核對呈現為〔老師要求〕，例如拆成兩點，sha256 核對以報告定義下正確的標示呈現；其他標示不變。依治理 §4.4 做 targeted correction，並重跑 README 測試與完整 pytest。
- **Owner**：Executor（targeted correction）。Required authority：無（不是契約語義不足，報告已定義標示，Brief 已標明來源）。

### F-2 — Low，non-blocking：「作業要求對應」表沒有列出正文的「網路上主流或更優解法之比較與說明」

- **證據**：
  - README:67-76 的表頭是「作業頁正文的要求」，共 8 列。
  - 老師原文 `:44-48`（繳交內容的報告內容）有「網路上主流或更優解法之比較與說明」，在表中沒有對應列。
  - 評分 `:57` 的「資料集來源與研究脈絡」也沒有單獨一列，但已併入第 1 列（「標示來源與連結」）與報告第一章。
  - 這兩項都已實作：報告 §8、§1，README:62 的「報告與交付」也提到它們。
- **依據**：D-R2 第 7 點，這是 HOW；README:80 說明逐條檢查在 ACCEPTANCE.md。這不違反任何條款，只是表格的完整性問題。
- **Disposition**：記錄給 acceptor 依 D-R2 第 7 點檢視版面時參考。本 audit 不要求後續工作，也不延長 cycle。依治理 §4.4，F-1 的 targeted correction 不得夾帶這一項，除非 acceptor 另行指示。

### F-3 — Low，non-blocking：RT-5 的「成果以外」守門只涵蓋六個 Test 值；截圖中的結果數字不在自動核對範圍內

- **證據**：
  - 我的反向檢查（`mutate_check.py`）中，在成果以外寫入 CV RMSE「157,254」、Test MSE「3.362 × 10^10」或「整體 CV winner … k = 17」，都**不會**被任何測試擋下。
  - 兩張截圖顯示許多結果數字（第 5 節），影像無法被 `test_readme_results_numbers_equal_the_exports` 核對。
- **為何不 blocking**：DA 對 RT-5 的要求（D-R2 第 3 點末句）是有條件的：「新增的區段**如果**陳述結果數字，必須被數字核對測試涵蓋」。在本 subject 上，成果以外的文字沒有任何結果數字（第 4 節），條件不成立，所以 RT-5 已滿足；新增的六值守門是額外的保護。截圖是 D-R2 第 4 點明確允許的，其中的數字我已逐一對照匯出值，全部相同。Test 結果受一次評估與 bit-exact 重現約束（N-5），截圖過時的風險只會在匯出結果改變時出現，而那需要新的 work item 與 audit。
- **Disposition**：不需要處理。之後修改 README 的 work item，如果在成果以外加入結果數字，或匯出結果改變，依 D-R2 第 3 點擴充核對，並重新擷取或核對截圖。目前沒有 owner。

### F-4 — Low，non-blocking：Executor transcript 的一筆工具輸出含有實際學號（本機、未追蹤）

- **證據**（只輸出計數）：
  - `~/.claude/projects/…/4bbff425-…/subagents/agent-ab07c6cd5d35d7f6f.jsonl` 中只有 **1 筆** record 含有該值，類型是 `user`／`tool_result`。沒有任何 assistant 訊息（含最後的 return）含有該值。
  - 這與 worklog §8 concern 1 的自我揭露（一次 `ls home_work_02/dist` 的輸出）一致。
  - Subject 的追蹤檔案、commit 與 commit message 都是 0 命中（第 6 節 H-1）。
- **依據**：高風險類別 H-1 的涵蓋位置包括「終端輸出」，A-4 要求比對值不在終端、log 或紀錄中印出。
- **為何不 blocking**：這不是 subject 的缺陷。該 transcript 在本機、不進 git、不會 push。H-1 不可逆的公開機制（push／合併）沒有被觸發。
- **Disposition**：Owner＝acceptor 或派工者，自行決定是否處理本機 transcript（例如不分享或匯出）。之後的派工可以要求不要列出 `dist/` 的內容。這不延長 cycle，也不影響 subject。

### 未列為 finding 的觀察

- **ZIP 內的 README**：`hw2/package.py:52-53` 的 `TRACKED_ITEMS` 不含 `doc/`。如果之後重新打包，ZIP 內新版 README 的兩張截圖（以及指向 `doc/` 的連結）會失效。目前的 ZIP 不受影響。是否重新打包是 acceptor 的保留事項，並且會是新的 work item（DA 紀錄 §5 第 2 點；worklog §8 concern 2）。
- **Worklog 的 binding 欄位**：記的是寫 worklog 前的 78 則。全程核對要由派工者補記（Bindings §3.6），我觀測到的是 95 則、單一元素（見 Assurance (b)）。
- **ACCEPTANCE A-8 的狀態**寫「在 branch `home_work_02-readme-restructure` 重新核對」。合併後這個 branch 名稱仍然可以從 worklog 追溯，不構成問題。
- **樹狀圖**（README:154-167）沒有列出 `design/`、`.gitattributes`、`.gitignore`、`pytest.ini`；舊版的表也沒有列 `design/`。這屬於 HOW，不影響 H-4（README 沒有引用 wireframe）。

## 8. Routing

- 不需要 Design Authority：F-1 的標示定義與來源都已在報告與 Brief 中寫明，不是契約語義不足；也沒有 boundary 疑義。
- 不需要 acceptor 的新決定。F-2 供 acceptor 檢視版面時參考；F-4 的本機 transcript 由 acceptor 或派工者自行處置。合併（RB-1）與是否重新打包仍是 acceptor 的既有保留事項。
- 下一步：Executor 對 F-1 做 targeted correction，然後派 R2（治理 §4.4）。

## 9. Closure evidence

本 cycle 未達 closure：F-1 是 blocking。

VERDICT: BLOCKING (F-1)
