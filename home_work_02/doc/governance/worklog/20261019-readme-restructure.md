# Worklog — README 改版（參考 HW01，不記載學號設定；Lightweight）

| 欄位 | 內容 |
| --- | --- |
| Work item | `20261019-readme-restructure`：單元 `README.md` 改版 |
| Lane | Lightweight（Bindings §4「已結案工作之後的單點修正」；DA `decision-20261019-post-merge-ad3-readme.md` §3.5）。不是 Formal run `run-20261018-hw2-formal` 的一部分 |
| 日期 | 2026-10-19 |
| Branch | `home_work_02-readme-restructure`，自 `1862a41`（AD-3 work item `home_work_02-ad3-pages-check` 的最後 commit）建立，疊在 AD-3 之上；合併順序預定 AD-3 先、本 branch 後。只在本機 commit，未 push |
| 狀態 | 實作與 self-verification 完成；independent audit **required（H-1、H-2）**：R1（`doc/governance/audit/20261019-readme-restructure-c1-r1.md`）有 blocking F-1，已依 §9 做 targeted correction（`706cc8c`），待 R2 closure |

## 1. Contract reference

- **Outcome Contract（Lightweight，Bindings §2.3）**：acceptor 2026-10-19 的直接指示，原文：
  > README的調整, 請調整README , 參考homework 01 ，學號設定（打包用)的資料不要加入，
- **有約束力的 DA 裁決**：`doc/governance/decisions/decision-20261019-post-merge-ad3-readme.md` 第 3 節（Q3）：D-R1（derived 義務修訂：README 不記載學號設定）、D-R2（內容限制 1～7）、D-R3（README 測試 RT-1～RT-6）、D-R4（ACCEPTANCE A-8）、D-R5（打包說明不新增位置）。
- **其他依據**：Brief `doc/brief/BRIEF.md` §3、§8（README 七項）、§11 BR-03；`decision-20261018-issue64-notebook-rerun.md` N-5（Test 評估的寫法）；`decision-20261018-high-risk-categories.md` H-1、H-2、H-4；報告模板 `report/report.md` 的三種標示對照表（作為「已實作功能」「作業要求對應」標示的來源）；參考的版面 `home_work_01/README.md`（`main`）。
- **派工指示的範圍**：只改 `home_work_02/` 內的檔案；不得修改 `home_work_02-ad3-pages-check`；不得 push、merge、rebase、force push。

## 2. Executing role and binding reference

- **角色**：Executor（`gov-executor` subagent，由主 session 派工；definition `.claude/agents/gov-executor.md`）。
- **Binding**（Bindings §3.6）：session `4bbff425-7ff9-4cdc-b64c-cc68e824e1b1`，agentId **`ab07c6cd5d35d7f6f`**，`meta.json` 的 `agentType`＝`gov-executor`（description「HW2 README restructure Executor」）；在第一個 commit `ccdc9f2` 之後、寫本 worklog 前觀測 `('claude-opus-5-5', 'high')` 78 則，全程單一元素，等於 O-1 mapping。全程核對（含之後的訊息）由派工者在採用 return 前執行。
- **Escalation／替代**：無。**Bounded assignments**：未使用。

## 3. Work performed

1. 從 `1862a41` 建立 `home_work_02-readme-restructure`。
2. 依 HW01 README 的結構改寫 `README.md`，內容依 HW2 的實際檔案與既有 README 重寫，不照搬 HW01（§4）。
3. 以 `report/chrome_capture.js`（報告建置用的同一個擷取程式，經 `hw2.report.run_capture("shots", …)`）在本機 Chrome 155.0.8059.80、headless、新 profile、host resolver 封鎖外部網路下，從本單元的 `index.html` 擷取 dashboard 截圖到 session scratchpad（`readme-shots/`），挑兩張複製到 `doc/screenshots/`（§5）。
4. 依 D-R3 修改 `tests/test_report.py` 的 README 測試（§6）；依 D-R4 修改 `doc/acceptance/ACCEPTANCE.md` A-8。
5. Commit `ccdc9f2`（README、截圖、測試、ACCEPTANCE），之後 commit 本 worklog（record-only path）。

## 4. Decisions and assumptions

**採用的 HW01 結構元素**（D-R2 第 7 點）：

| HW01 README | HW2 README 的對應 |
| --- | --- |
| 專案資料（課程、作業、完成日期、儲存庫網址、Live Demo） | `## 專案資料`：課程名稱取自 root `README.md`；完成日期＝PR #68 合併日（`5d650b1` 的 commit 日期 2026-10-19）；Dashboard 的 Pages URL。不含作者姓名或學號 |
| Live Demo（可點擊的截圖＋說明） | 併入 `## Dashboard（課堂口頭要求）`：兩張截圖，第一張連到 Pages；保留原 Dashboard 節的三點並加註課堂口頭要求。合併的理由：Brief §8 的「dashboard 連結」要對應恰好一個 heading（RT-5），另開 `## Live Demo` 會造成兩個 dashboard 區段 |
| 專案摘要 | `## 專案摘要`：原 README 開頭的一段＋「一份 notebook、三個呈現」，不含結果數字 |
| 已實作功能（分組條列） | `## 已實作功能`：分析／Dashboard／報告與交付三組，每點以報告的三種標示標注（來源：`report/report.md` 的標示對照表） |
| 作業要求對應（配分表） | `## 作業要求對應`：作業頁正文各項要求 → 本專案的位置；補充建議與 dashboard 分開註明，不寫成正文要求 |
| 資料來源與標示 | `## 資料來源與授權`（原文不變） |
| 技術棧 | `## 技術棧`：版本只引用 `requirements.txt`，不另寫版本號（Chart.js 4.4.1 仍在檔案配置表，與原 README 相同） |
| 專案結構（樹狀圖） | 併入 `## 檔案配置`：先樹狀圖、再保留原本的表；heading 名稱不變（RT-5） |
| 本機執行 | `## 重跑步驟（Windows，Python 3.11）`：指令區塊不變 |
| 驗證紀錄 | `## 驗證紀錄`：只描述測試涵蓋的面向與 ACCEPTANCE.md／worklog 的位置，**不寫測試數量**（會隨版本過時） |
| 詳細文件（表） | `## 詳細文件`：CONTEXT、requirement、Brief、Spec、票務索引、ACCEPTANCE、governance |

HW01 中沒有對應內容而未採用的：部署（Vercel）、安全性（API key）、技術參考摘要、Taiwan Map 的兩種模式。

**D-R2 的落實**：

- 第 1 點（必須移除）：刪除「學號設定（打包用）」整節（標題與兩段內容，含打包核對與 ZIP 內容的說明）與「本機、不進 git」表的設定列；該表改名為「本機、不進 git 的材料與輸出」並改為 `###`（放在重跑步驟之下）。改版後 README 不含 `學號設定`、`packaging.json`、`student_id`、`.local/`。被移除的打包說明沒有搬到其他追蹤文件（D-R5）。
- 第 2 點（可以保留）：保留 `<學號>_hw2.ipynb`、`<學號>_hw2.zip`、`dist/` 列中的佔位檔名與「學號 ZIP」；`python -m hw2.package` 一行保留，註解只寫「作者繳交前的打包步驟，需要本機、不進 git 的輸入」。
- 第 3 點（必須維持）：Brief §8 七項各有一個 heading（目的、資料來源與授權、流程（CRISP-DM）、成果、重跑步驟、Dashboard（課堂口頭要求）、檔案配置）；三種標示與「課堂口頭要求」；N-5 的 Test 評估段落原文不變；`## 成果` 原文不變；新增區段不陳述 Test 結果數字（測試強制，§6）；沒有 mock、wireframe 或 fixture 的數字或截圖。
- 第 4 點（截圖）：見 §5。
- 第 5 點（非範圍）：沒有修改 `hw2/**`、`.gitignore`、報告、notebook、dashboard、`results/`、root 檔案，沒有重新打包。
- 第 6 點（release gate）：重跑步驟的指令沒有新增或修改，只改了 `hw2.package` 一行的註解（`git show 1862a41:home_work_02/README.md` 與新版的 bash 區塊比對，只有第 9 行註解不同）。依 D-R2 第 6 點引用既有實跑證據：`doc/governance/worklog/issue-67.md` §7、`doc/governance/audit/spec-SPEC-c1-r1.md` §4.1。
- 第 7 點：版面是否符合「參考 homework 01」的期待，由 acceptor 自己檢視。

**其他決定**：

- 截圖放在 `doc/screenshots/`，不放 `assets/`：`assets/` 屬於 dashboard 並會被打包進 ZIP（D-R2 第 5 點把 dashboard 列為非範圍）。限制：繳交 ZIP 不含 `doc/`，所以 ZIP 內的 README 若是新版，圖片會缺；目前不重新打包（DA §5 第 2 點），這只在 acceptor 決定重新打包時才相關。
- README 的 Dashboard 說明寫「截圖從本單元的 `index.html` 擷取，內容與 Pages 上相同」：`git diff --stat 5d650b1 HEAD -- index.html assets results hw2.ipynb` 為空，Pages 發布自 `5d650b1`，dashboard 只讀取追蹤的匯出結果。畫面中的繪製時間是擷取當下的量測，README 已註明。
- 「作業要求對應」的連結選用 `hw2/selection.py`、`hw2/models.py`、`hw2/testgate.py`，依各檔 docstring 確認其職責。

**需要 authority 的決定**：無新的。D-R1～D-R5 由 DA 紀錄授權；本 work item 沒有遇到語義缺口或 boundary 疑義。

## 5. 截圖（D-R2 第 4 點）

| 檔案 | 來源 | sha256 | 目視確認 |
| --- | --- | --- | --- |
| `doc/screenshots/dashboard-test.png` | scratchpad `readme-shots/test.png`（`#test` 區塊：保留 Test 集評估） | `bcd23c76bc6e06807d293bed2061fbedac4a93219dee5070a355f24070568f9d` | 已逐張檢視：沒有學號、瀏覽器網址列、本機路徑或帳號；只有 dashboard 的內容 |
| `doc/screenshots/dashboard-model.png` | scratchpad `readme-shots/model.png`（`#model` 區塊：模型選擇與訓練 CV） | `a03ecd5ab12748f3cf989cac89c5b097873b0e24778745d6e0717573c4ae863f` | 同上 |

- 來源是 repo 內的 `index.html`（`file://`），不是解壓後的 ZIP 資料夾，也不是 `hw2.fixture` 的複本。擷取結果：`external_requests` 為空、`overall_method`＝`lasso_path`、`first_draw_ms` 308。
- 擷取程式的 `shots` 只截取元素範圍（CDP `Page.captureScreenshot` 的 clip），不含瀏覽器框。
- 另三張（`overview`、`compare`、`methods`）也已目視，沒有採用；它們只留在 scratchpad。

## 6. Verification

**README 測試的修改（D-R3）**：

| # | 實作 |
| --- | --- |
| RT-1 | `test_readme_has_every_required_item`：刪除 heading「學號設定（打包用）」與 `.local/packaging.json`、`<學號>` 必須出現的斷言 |
| RT-2 | 新增 `test_readme_does_not_record_the_student_id_setting`：四個字串都不出現 |
| RT-3 | 新增 `test_readme_submission_file_names_use_only_the_placeholder`：每個 `…_hw2.ipynb`／`…_hw2.zip` 的前綴（以空白、`/`、反引號、引號、括號、標點、`|`、`*`、方括號為界）必須正好是 `<學號>`；不要求 `<學號>` 出現 |
| RT-4 | 新增 `test_readme_has_no_digit_run_after_the_word_student_id`：每個「學號」之後，起點在 12 個字元以內的 7 位連續數字一律失敗。`tests/test_repo_hygiene.py` 未修改 |
| RT-5 | 七項改為 `README_ITEMS` 清單，每項恰好對應一個 heading、七個互不相同；Pages URL、`python -m hw2.report`、六個 CRISP-DM 階段保留；`## 成果`、`## 資料來源與授權`、`## 目的` 的 heading 未改名，以它們定位的測試不變。數字核對加一段：`## 成果` 以外不得出現 `n_test`、RMSE、MAE、R²、涵蓋率、涵蓋筆數的匯出值，使「每一個陳述結果數字的區段」就是被核對的那一節 |
| RT-6 | 其他測試沒有刪除、skip、xfail 或放寬；`tests/` 的 diff 只在 README 測試區段（`git show ccdc9f2 -- home_work_02/tests/test_report.py`） |

- 新測試的失敗訊息只給 offset，不印出 README 的文字，避免把實際值帶進 log。

**執行結果**：

| 檢查 | Subject | 結果 |
| --- | --- | --- |
| 完整 `pytest`（`.venv/Scripts/python -m pytest -q -rs`，在 `home_work_02/`） | 工作樹（commit 前）與 `ccdc9f2` | 兩次都是 **398 passed**，0 skipped、0 failed（本 work item 新增 3 個測試函式） |
| `tests/test_repo_hygiene.py`（含 `test_no_tracked_file_contains_the_student_id`，`.local/packaging.json` 存在） | `ccdc9f2`（截圖已追蹤） | 17 passed，0 skipped；學號測試單獨再跑一次 1 passed |
| A-4：本 work item 的 commit 內容與訊息 | `1862a41..ccdc9f2`（1 個 commit） | 以設定值比對 `git log -p --format=%H%n%B`：0 命中（只輸出計數，不印出值）。PNG 的文字不在 byte 比對範圍內，以 §5 的目視確認 |
| README 測試的反向檢查（scratchpad `mutate_readme.py`：把 `tests.test_report.README` 換成變異版本後呼叫測試函式） | 工作樹 | 舊版 README（`1862a41`）、加入 `.local/packaging.json`、加入 `student_id`、繳交檔名前綴改為 7 位數字、前綴改為不含角括號的「學號」、「學號」後接 7 位數字、「學號」後 12 字元內接 8 位數字、在 `## 成果` 外寫 RMSE、在 `## 成果` 外寫涵蓋率、刪除「檔案配置」heading、多一個「Dashboard」heading：11 種變異都被對應的測試擋下；未變異的 README 全部通過。（舊版 README 仍通過七項 heading 測試，這是預期：舊版本來就有七個 heading，它由 RT-2 擋下） |
| README 的連結與路徑 | 工作樹 | 每個 Markdown 相對連結都存在；反引號中的路徑逐一核對存在（`results/tables/` 的八個 CSV、`report/` 的三個檔、`assets/vendor/`、`tests/js/` 等）；三個外部 URL（Pages、GitHub repo、Kaggle 資料集頁）以 `curl` 取得 HTTP 200 |
| 禁用字串 | 工作樹 | `學號設定`、`packaging.json`、`student_id`、`.local/` 都不在 README |
| 重跑步驟 | — | 未重新執行：指令沒有新增或修改（§4 第 6 點），引用 `issue-67.md` §7、SIA §4.1 |

- **未執行**：Node 測試與 `hw2.offline_scan`（dashboard、`hw2/` 都沒有改動，且 pytest 內的 Node 一致性測試已執行）；以瀏覽器檢視 README 在 GitHub 上的呈現（branch 未 push）。

## 7. Artifacts

| 檔案 | 變更 | Commit |
| --- | --- | --- |
| `home_work_02/README.md` | 改版（§4） | `ccdc9f2` |
| `home_work_02/doc/screenshots/dashboard-test.png`、`dashboard-model.png` | 新增（§5） | `ccdc9f2` |
| `home_work_02/tests/test_report.py` | README 測試（§6） | `ccdc9f2` |
| `home_work_02/doc/acceptance/ACCEPTANCE.md` | A-8 的檢查文字（刪去設定路徑、加註 D-R1）、測試欄、票欄與狀態（指向本 worklog §6）；A-7、C-16 與其他列不變 | `ccdc9f2` |
| `home_work_02/doc/governance/worklog/20261019-readme-restructure.md` | 本 worklog | 下一個 commit（record-only） |

## 8. Audit status、concerns 與 remaining work

- **Audit**：**required**（DA `decision-20261019-post-merge-ad3-readme.md` §3.5：H-2 README 的流程與成果、H-1 學號設定的記載）。尚未派工。R1 由派工者依 Bindings §3.7 派 `gov-primary-reviewer`，record 寫在 `doc/governance/audit/20261019-readme-restructure-c1-r1.md`；R1 要核對 D-R2、RT-1～RT-6，並自行執行 A-4 的學號比對。受審 subject：本 branch 的最終 commit。本 worklog 不是 audit record，也不是 audit PASS。
- **Concerns**：
  1. 本 Executor 的 session 中，一次 `ls home_work_02/dist` 的輸出顯示了打包輸出的檔名，因而在 Executor 的 subagent transcript（本機 `~/.claude/projects/…/subagents/agent-ab07c6cd5d35d7f6f.jsonl`，不追蹤、不 push）出現一次實際值。沒有寫入任何追蹤檔案、commit、紀錄或 log；A-4 比對 0 命中。只是如實記錄，是否需要處理由派工者或 acceptor 判斷。
  2. 繳交 ZIP 內的 README 是舊版（含佔位的學號設定小節，沒有實際值）；新版 README 的截圖在 `doc/` 中，不在 ZIP 的打包範圍。是否重新打包是 acceptor 的保留事項（DA §5 第 2 點）。
  3. 本 branch 疊在 AD-3 branch 之上（含 AD-3 的 `ACCEPTANCE.md`、`tests/test_report.py` 變更）；若 AD-3 在 audit 中被修改，本 branch 需要在其之上重新整合，屬派工者的控制面安排。
- **Remaining work**：
  - 派工者：binding 全程核對、派 R1、push（SA-1）。
  - acceptor：合併（RB-1；預定 AD-3 先、本 branch 後）；檢視版面是否符合「參考 homework 01」的期待；是否重新打包 ZIP。

## 9. Targeted correction — cycle 1（R1 F-1）

- **依據**：R1 record `doc/governance/audit/20261019-readme-restructure-c1-r1.md`（commit `1b7689e`）的 F-1（Medium，blocking）與其 closure 條件：「README 不再把 sha256 核對呈現為〔老師要求〕……以報告定義下正確的標示呈現；其他標示不變」。派工者 2026-10-19 的續派指示：只處理 F-1；F-2 不處理（需要 acceptor 另行指示）；F-3、F-4 不處理。
- **是否爭議**：不爭議。Brief §4 把「載入時核對 sha256」標為 [D Q35]（acceptor 在 Grill 的決定），作業頁正文（`doc/requirement/HW2-requirements-Multiple Linear regression.txt` 資料來源段）沒有這項要求；報告的標示定義中，不是老師要求的本專案設計屬〔專案延伸〕（`report/report.md:11`）。
- **修正**（commit `706cc8c`，只改 `README.md` 一行，拆成兩點）：
  - 原：「〔老師要求〕載入時核對資料檔的 sha256，不符即停止；CRISP-DM 六章依序執行。」
  - 新：「〔老師要求〕CRISP-DM 六章依序執行。」與「〔專案延伸〕載入時核對資料檔的 sha256，不符即停止（本專案的決定，不是作業頁的要求）。」
  - CRISP-DM 六章維持〔老師要求〕（作業頁正文第 3 點、報告對照表「CRISP-DM 六階段｜老師要求」）。其他標示、測試、ACCEPTANCE.md 都沒有改動（`git show --stat 706cc8c`：只有 `home_work_02/README.md`，+2／−1）。
- **回歸證據**（subject：`706cc8c` 的工作樹；`.local/packaging.json` 存在）：
  - README 測試 `pytest -q -rs tests/test_report.py -k readme`：7 passed。
  - `tests/test_repo_hygiene.py::test_no_tracked_file_contains_the_student_id`：1 passed（實際執行，不是 skip）。
  - 完整 `pytest -q -rs`：**398 passed**，0 skipped、0 failed。
  - A-4：`1862a41..HEAD` 全部 commit 的內容與訊息，以設定值比對只輸出計數：在 `ee55769`（含本次兩個 commit）上，`1862a41..ee55769` 的 5 個 commit（`ccdc9f2`、`dcb6052`、`1b7689e`、`706cc8c`、`ee55769`）**0 命中**；同一時點 `tests/test_repo_hygiene.py` 17 passed。本次沒有列出 `dist/`，也沒有印出任何含學號的檔名。
- **Binding**：同一個 agentId `ab07c6cd5d35d7f6f`（`gov-executor`，以 SendMessage 續派）；全程核對由派工者在採用 return 前執行。
