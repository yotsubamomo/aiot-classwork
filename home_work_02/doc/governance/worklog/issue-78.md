# Worklog — #78 HW2 V2-T5（README、報告探索模式章節、ACCEPTANCE V2 條目、OV-1／SR-09 重做與 ZIP 重打包）

- **Work item**：GitHub issue #78（V2-T5），Formal lane，run `run-20261022-hw2-v2-enhance`（Orchestrator＝root session `37216426-f292-44f9-bad1-e2d862e7b8f1`；dispatch log 第 20 列）。
- **執行角色**：Executor（治理 §2.1；`gov-executor`，有效 mapping `claude-opus-5-5`／`high`，Bindings b5 §3.1 O-1）。
- **Subject**：branch `home_work_02-v2-enhance`（未 push）。BASE `2b658b3cfaff37fb8ffa93087746ff0c8e3d1398`（#77 結案、run 暫停點）。**實作 commit `f56461b92c08a9ce8ac82dfcb8508be6e553b3b2`**（README、報告模板、新測試；ZIP 由它打包）；之後的紀錄 commit 只改 `doc/`（`doc/acceptance/ACCEPTANCE.md`、本 worklog、`doc/screenshots/v2-issue78/`）。Orchestrator 未 commit 的 run record 修改未動、未 stage。
- **狀態**：實作與 self-verification 完成，待 independent audit（R1）。

## 1. Contract reference

| 契約 | 位置與版本 |
| --- | --- |
| Outcome Contract | `doc/governance/outcome-contract.md` §5（V2 接受紀錄，接受基準 `d7f02d4`）、§5.2 CC-V2-1（本票沒有新增腳本檔，`tests/test_dashboard_static.py` 未動） |
| Ticket | GitHub #78（`gh issue view 78`，2026-10-22 讀取，OPEN，`ready-for-agent`）：What to build、AC 六項（README、報告、ACCEPTANCE V2 條目、ZIP、Pages、不變量）與結案證據 |
| Spec | `doc/spec/SPEC-V2.md` rev 2：「文件、README、報告與打包」、人工檢查表、「離線與請求隔離」、「LARS 退化（A-2）」、「候選有效性、狀態與運算預算」；未提到的事項以 `SPEC.md` rev 5 為準 |
| Brief | `doc/brief/BRIEF-V2.md` rev 2＋E-1：§2（SRC-4 差異）、§3.5（四項覆寫）、§5.6、§6、§7（交付物）、§8（1～9、2a 與數值驗證）；`BRIEF.md`、`CONTEXT.md`、`doc/ticket/tickets-v2.md` |
| DA derivation | `decisions/derivation-SPEC-V2.md`：§4 #78 列（在 boundary 內，附 I-4、B-8、B-10）；I-4（報告與 README 不含探索數字、上限與預算經建置流程帶入或不寫、scope 標示、+1／+2 標為老師要求、解讀與能力集合不得寫成老師要求）；B-8（README「10–20」→「>13」，報告 §1.2 不改）；B-10（Pages 記 NOT TESTED，合併後的 Lightweight item）；§7.4 #78：H-1～H-5，A-1～A-5、A-7～A-9；§9 F-5（報告模板禁止手打數字） |
| DA decisions（分配給 #78） | `decision-20261022-r1f3-v1-footer.md` R3-6（README 頁面層級的請求與資料來源陳述）與第 238 行觀察；`decision-20261022-issue75-lasso-early-stop.md` R4-5（README／報告的 Lasso 說明與 #77 後行為一致）；`decision-20261022-issue77-resource-limits.md` §6 #78 列（限制揭露 (a)(b)）；`decision-20261022-issue77-cancel-final-phase.md` §4 #78 列（取消描述） |
| Audit 分配 | `audit/issue-75-c1-r1.md` R1-F4（兩張替換資料截圖不得作 50 Startups 證據）；`audit/issue-77-c1-r2.md` O-R2-1、O-R2-2（極大檔案可能耗盡記憶體或使頁面數秒不回應） |
| Run invariants | run record §1 designation 第 4–7 點（經 CC-V2-1）：notebook、`hw2/` 正式路徑、`model_data`、`results/`、Test evaluation 紀錄、V1 區塊、V1 腳本與核心模組、`style.css`、既有測試不變；正式報告各章與數字不變、建置流程不變；不重跑 notebook、不做新的 Test evaluation；四個 seams、無 E2E、無 CI；只改 `home_work_02/`、不碰 `doc/requirement/`；追蹤檔案一律 `<學號>`；ZIP 與 `dist/` 不追蹤；不繳交（RB-2） |

## 2. Binding

| 對象 | 觀測（Bindings §3.6 指令，全部 assistant 訊息） | 結果 |
| --- | --- | --- |
| 本 assignment，agentId `acc8906c845bfc14f`（`agentType` `gov-executor`） | `('claude-opus-5-5', 'high')`：193 則（寫入本節前）；最後一個紀錄 commit 前再核對 217 則，仍為單一元素（return 前由派工者依 §3.6 全程核對） | 單一元素，等於有效 mapping；無 escalation、無替代 |

- Bounded assignments：**未使用**（沒有派 `gov-investigator`／`gov-bounded-worker` 或任何 subagent）。

## 3. Work performed

1. **讀取**：Bindings b5、`gov-executor.md`、Implementation Profile §3–§5、§9、治理 §3.5、§3.7、§3.8；OC §5／§5.2；`gh issue view 78`；Spec V2、Brief V2 全文；derivation 全文；四份分配給 #78 的 DA decision；`audit/issue-75-c1-r1.md` R1-F4、`audit/issue-77-c1-r2.md` O-R2-1～3；run record；`worklog/issue-77.md`（全部）、#67 worklog §8（V1 的 OV-1／SR-09 方法）；`README.md`、`report/report.md`、`doc/acceptance/ACCEPTANCE.md`、`hw2/report.py`、`hw2/package.py`、`tests/test_report.py`、`tests/test_package.py`、`tests/test_explore_static.py`、`index.html` 的探索區塊與 `assets/explore_*.js` 的常數。BASE 的 `python -m pytest -q -rs`：**470 passed**（59.4 s，0 skipped）。
2. **README**（`f56461b`）：
   - Dashboard 一節：截圖說明的主詞改為 King County 檢視；「頁面不發出任何對外請求」改為「頁面載入、King County 與 50 Startups 的所有操作、以本機檔案載入自訂資料集，都不發出任何對外請求；唯一的對外請求是提交 URL 之後對該 URL 的一次 GET（不帶憑證、不跟隨重新導向、不重試）」；「Dashboard 只讀取匯出的結果」改為「King County 檢視只讀取匯出的結果」並說明探索模式不讀不寫 `model_data`、探索 test 不是 Test 評估（DA R3-6）；新版作業頁把 GitHub 與 web 列為主要繳交（Brief V2 §3.5 覆寫 1）。
   - 專案摘要、目的、已實作功能：加入探索模式；「完全離線、零對外請求」改為同樣的範圍；加分兩項標〔老師要求（新版作業頁的加分）〕，「兩種 problem＝同一頁下拉切換兩個資料集」寫明是本專案的解讀、探索能力集合標〔專案延伸〕（DA I-4）。
   - 「作業要求對應」：以 SRC-4 為準，特徵數 >13（DA B-8；舊版 10 至 20 只在說明中提及），繳交內容改為新版的主要繳交，新版沒有的條目標「新版未載明」（Brief V2 §2 Q1），加兩列加分（操作方式與 ACCEPTANCE 位置）。
   - 資料來源：50 Startups 的老師 URL、來源 repository、MIT 授權檔、sha256、`startups50.js` 的用途、不宣稱 >13、不陳述原始出處（DA I-3）。
   - 新增「## 探索模式（加分功能）」：操作方式、分析方法、Lasso 停止（R4-1～R4-4：任何提前結束一律同樣處理、原因如實、單位無關的判定、entry alpha 原尺度）、與正式分析的差異表、限制與揭露（逐列切分洩漏、不是正式評估、運算預算、取消與改選的生效時點（CF-1 與 C1-R1：候選邊界、尾段的步驟邊界、單一候選可能數分鐘、不承諾時間）、沒有檔案大小上限與極大檔案（C2-R1、C2-R3、O-R2-1、O-R2-2）、URL 的 CORS 限制）、實作常數表（載入上限 50,000 × 60、至少 20 列、層級上限 20、預算 `2e11`／`8e10`、seed 42／20%／5 fold、95%、20 秒）。README 不含任何探索結果數字。
   - 技術棧、重跑步驟（新增探索模式的 Node 指令並實際執行，§6.1）、檔案配置、驗證紀錄、詳細文件表加入 V2 的檔案與文件。
3. **報告**（`f56461b`）：在第 11 章之後、附錄 A 之前新增「## 12. 探索模式（加分功能） 〔老師要求（新版作業頁的加分）〕」：標示表、12.1 加分功能、12.2 分析方法、12.3 與正式分析的差異（含 Lasso 停止段落）、12.4 限制與揭露、12.5 前面各章的範圍（第 7.1 節與第九章是 King County 檢視——處理 R3-6 對第 238 行的觀察，不改正式章節）。唯一的佔位符是 `{{k_range}}`（正式分析的 k 範圍，描述 King County 的補齊規則）；載入上限與預算的數字不寫進報告，指向 README 與 ACCEPTANCE（DA resource-limits §6「可經建置流程或指向引用」）。正式章節、標示對照表、建置程式都沒有修改。
4. **新測試** `tests/test_explore_docs.py`（8 項，延伸 README／報告的既有測試類別，不是新 seam）：README 常數等於 `assets/explore_load.js`／`explore_engine.js` 的值；需求表含 >13 與兩列加分；頁面層級陳述已移除；README 與報告第 12 章含 DA 分配的揭露；第 12 章的位置、標示與佔位符；報告模板除第 12 章外與接受基準 `d7f02d4` 逐字相同。
5. **打包**：commit `f56461b` 之後，把 working copy 中因 `core.autocrlf=true` 而成為 CRLF 的 5 個 dashboard 檔（`index.html`、`assets/app.js`、`hw2core.js`、`model_data.js`、`style.css`）以 `git show HEAD:<path>` 寫回 blob 位元組（內容不變、`git status` 乾淨），使 ZIP 內的 dashboard 與 git blob（＝合併後 Pages 提供的位元組）逐位元相同；`python -m hw2.package`（未修改）重打包（§6.2）。
6. **瀏覽器 self-verification**（§6.3）：解壓 ZIP，在 headless Chrome 與 Edge 上做 OV-1、SR-09 (a)～(g)、下拉與 50 Startups、自訂資料集（URL 失敗→本機檔案）、acceptor 三條、OV-2／OV-4／OV-5、效能紀錄。
7. **ACCEPTANCE**：V2-11、V2-15、V2-17 加 R1-F4 註（替換資料截圖不得作 50 Startups 或 Pages 證據）；新增 V2-35～V2-43、G.1（Brief V2 §8 與 acceptor 追加條目的對照）、G.2（V2 量測紀錄）。

## 4. Decisions and assumptions

都在 accepted contract 的 HOW 範圍內；沒有改變 requirement、AC、invariant 或 gate。

| # | 決定 | 依據 |
| --- | --- | --- |
| D-1 | **報告第 238 行（§7.1）不改**，改在第 12 章 12.5 寫明第 7.1 節與第九章描述的是 King County 檢視。這樣正式章節逐字不變（AC「只有新章節與日期不同」），陳述在所屬檢視下仍屬實（R3-4 的讀法）。不需要 route 到 DA：沒有修改正式章節文字 | #78 AC；DA R3-6 觀察；R3-4 |
| D-2 | **報告不寫探索模式的任何數值常數**（80/20、5 fold、上限、預算、95% 都不寫），用「與正式分析相同」或指向 README／ACCEPTANCE；唯一的佔位符是正式分析的 `{{k_range}}`。理由：`tests/test_report.py` 禁止手打數字（F-5），新增 placeholder 需要改 `hw2/report.py`（建置流程不變）；以中文數字書寫會規避該測試的目的，所以不採用。資料集名稱「50 Startups」中的 50 不是數字，以程式碼字體書寫 | DA I-4、F-5；run invariant「建置流程不變」 |
| D-3 | **README 的數值常數由新測試與程式常數綁定**，避免 README 與程式不一致 | Spec V2「數字…出現在 ACCEPTANCE 與 README」 |
| D-4 | **README「作業要求對應」以 SRC-4 為準**，舊版才有的條目標「新版未載明」並照原樣交付；舊的特徵數只在說明欄提到「舊版正文寫 10 至 20 個特徵」 | Brief V2 §2（Q1）、§3.5；DA B-8 |
| D-5 | **Dashboard 的課堂口頭要求陳述**改為「原是課堂口頭要求；新版作業頁把 GitHub 與 web 列為主要繳交」——原句「它是額外交付」在 SRC-4 後不屬實 | Brief V2 §3.5 覆寫 1；H-4 |
| D-6 | **ZIP 的 dashboard 位元組**：打包前把 working copy 的 CRLF 版本寫回 blob 位元組（不改 `hw2/package.py`，也不改 git 內容），使「ZIP 內 dashboard 與 repo 逐位元相同」在 blob 層面成立，合併後 Pages 提供的就是同一組位元組。README、`hw2/*.py` 等非 dashboard 檔仍是 working copy 的位元組（與 V1 的做法相同） | #78 AC「ZIP」；Spec V2「ZIP 與 Pages 的 dashboard 內容相同」 |
| D-7 | **OV-1 的斷網方式**與 V1 #67 相同（瀏覽器層：DevTools offline＋主機名稱全部無法解析；沒有伺服器），headless 而非可見視窗（V2 #74～#77 的做法）；在 G.2 註明 | AD-1；#67 worklog §8.1 |
| D-8 | **中型資料**：#77 的 `medium.csv` 只記配方，無法逐位元重建，所以以新的 mulberry32(78) 配方產生同規模的 `medium78.csv`（20,000 × 26），記錄配方與 sha256，不進 repo | Spec V2 人工檢查表「效能」 |

## 5. Artifacts

- 實作 commit `f56461b`：`README.md`（+98／−21）、`report/report.md`（+58／−0，第 12 章）、新增 `tests/test_explore_docs.py`（135 行）。`git diff --name-status 2b658b3 f56461b`：只有這三個路徑。
- 紀錄 commit：`doc/acceptance/ACCEPTANCE.md`、本 worklog、`doc/screenshots/v2-issue78/`（`ov78_chrome.json`、`ov78_edge.json`、`chrome_kc_scatter_default.png`、`chrome_kc_scatter_zoom.png`、`chrome_kc_test_block.png`、`chrome_startups50_1280.png`、`chrome_startups50_375.png`、`chrome_custom_url_failure.png`、`chrome_custom_file_after_url_failure.png`、`node_explore_tap.txt`、`zip_manifest.txt`）。JSON 只有本機檔案的檔名與老師公開的範例 URL，沒有本機路徑或學號。
- 不追蹤：`dist/<學號>_hw2.zip`、`dist/<學號>_hw2.ipynb`、`dist/report/`、`dist/hw2_package_manifest.json`。
- 不變：`index.html`、`assets/`、`hw2/`、`results/`、`hw2.ipynb`、既有測試、`doc/requirement/`、`doc/spec/`、`doc/brief/`、`doc/ticket/`、`CONTEXT.md`（glossary 沒有「10–20」字樣，DA B-8）。

## 6. Verification

### 6.1 自動測試

| 時點／subject | 指令 | 結果 |
| --- | --- | --- |
| BASE `2b658b3` | `.venv/Scripts/python -m pytest -q -rs`（Python 3.11.2） | 470 passed，59.4 s |
| `f56461b`（working tree＝commit） | `.venv/Scripts/python -m pytest -q -rs` | **478 passed，0 skipped**，56.2 s（新增 `test_explore_docs.py` 8 項） |
| 同上 | `node --test tests/js/explore_load.test.js tests/js/explore_boundary.test.js tests/js/explore_app.test.js tests/js/explore_methods.test.js tests/js/explore_custom.test.js tests/js/explore_run.test.js`（Node v24.19.0；README 新增的指令） | **88 pass、0 fail、0 skipped**（15＋7＋12＋7＋16＋31；TAP `doc/screenshots/v2-issue78/node_explore_tap.txt`） |
| 同上 | `node --test tests/js/core.test.js`（README 既有指令） | 9 pass、0 fail、3 skipped：3 個 fixture 案例需要 `HW2_FIXTURE_MODEL_DATA`，由 pytest 的 `test_node_core.py` 執行（包含在 478 中）；與 V1 相同的既有行為 |
| 同上 | `explore_contract.test.js`（需要 pytest 產生的參照） | 由 `tests/test_node_explore.py` 驅動，包含在 478 中 |
| 同上 | `python -m hw2.offline_scan` | `scanned 13 files: PASS (0 findings)` |
| 新測試的靈敏度（scratchpad，記憶體中變造，不改檔） | 改正式章節一句、改 README 的 Lasso 預算、加回「頁面不發出任何對外請求」、刪掉「沒有檔案大小上限」 | 四種變造都讓對應測試失敗 |

### 6.2 打包與 ZIP（V2-41）

- `PYTHONIOENCODING=utf-8 .venv/Scripts/python -m hw2.package`（09:44:33–09:44:48，exit 0），打包 commit `f56461b`：
  - `<學號>_hw2.zip`：**sha256 `57e1e4a415f891e2495ce00519a0b5c638989e0067cecc47b639a033a87bcd11`**，81,620,529 bytes，67 個項目，頂層資料夾 `<學號>_hw2/`；上一版（V1 refresh）為 `c76272b39373622162f252163c76bb8ba88c76d0abf9ce836f4c6b759b88a146`、56 個項目。
  - `<學號>_hw2.ipynb` sha256 `2e2f8afc1f67fd51312b894d3a3f4873049defead185b1dd4ca2ab1ace04ff64`（與上一版相同；notebook 單次完整執行 40 個 code cell，`run_id` `5e74d03d6c81499f913532a551af3e6d`，`result_digest` `b53ff286…`）。
  - 報告 PDF：152 頁，sha256 `91bdf53e68daaaee212a999512f4c5c3d6e0af6119966d01886f718711ca4b2f`；ChatGPT PDF `0a5d29e30802270af6a7ff02b692e2bf26e808a5102c6b787adf1ee36a3ca194`。
  - 新增項目（11）：`assets/data/50_Startups.csv`（`c6075ca5…630d`）、`50_Startups.LICENSE.md`、`50_Startups.SOURCE.md`、`startups50.js`、`assets/explore.css`、`explore_app.js`、`explore_engine.js`、`explore_load.js`、`explore_plot.js`、`explore_ui.js`、`hw2/explore_reference.py`。完整清單（路徑、大小、sha256，名稱以 `<學號>` 遮蔽）：`doc/screenshots/v2-issue78/zip_manifest.txt`。
- 讀回：`zipfile.testzip()` 無錯誤；解壓後 `index.html` 與 `git ls-files assets` 的 16 個檔，共 17 個，與 `git show f56461b:` 的 blob sha256 全部相同。
- 報告逐章比對：以 `d7f02d4` 的模板經同一個 `render_markdown()`（含作者材料）渲染，與 `dist/report/hw2_report.md` 比較：14 個 `## ` 章節逐字相同、前言相同，只多出第 12 章；沒有日期差異。
- 作者材料：`ACCEPTOR_MATERIALS` 三檔 sha256 與收件紀錄相同；`check_derived_reviewed()`＝`DERIVED_REVIEWED`。
- 學號：以 `.local/packaging.json` 的值 `git grep -F`（不印出值）0 個檔案命中；`git log --all --format=%B` 0 命中；兩份瀏覽器 JSON 0 命中。

### 6.3 瀏覽器（V2-37～V2-40）

- **方法**：scratchpad 的 `ov78.js` 以 DevTools Protocol 驅動 headless Google Chrome 155.0.8059.85（PID 33588）與 Microsoft Edge 155.0.4283.62（PID 29700），各用全新的 scratchpad `--user-data-dir`；頁面為 ZIP 解壓到 scratchpad 的 `index.html`（`file://`）；`Network.emulateNetworkConditions` offline＋`--host-resolver-rules=MAP * ~NOTFOUND`；`Input.dispatchMouseEvent`／`dispatchKeyEvent`／`insertText` 送真實輸入；`DOM.setFileInputFiles` 選檔；`PerformanceObserver('longtask')`；`HW2_PERF` 與 `HW2_EXPLORE` 只讀取。每個瀏覽器結束時以 `taskkill /PID <pid> /T /F` 停止。Chrome 的 PID 事後查無程序；Edge 則留下一個父程序已結束、因而不在樹內的 `msedge.exe`（PID 30592，連同 7 個子程序，命令列都是本票的 scratchpad profile）——清理 profile 時發現，以 `Win32_Process` 的命令列（只比對本 session 的 scratchpad profile 路徑）找出後以 `taskkill /PID 30592 /T /F` 停止，之後剩餘 0。沒有以映像名稱停止任何程序，也沒有在 acceptor 的預設 profile 上啟動任何瀏覽器。另以 `shot_test.js`（同樣做法，PID 3240）擷取 King County 的 Test 區塊截圖。
- **第一次 Chrome 執行（不作證據）**：`style.css` 的 `scroll-behavior: smooth` 使 `scrollIntoView` 後量到的座標錯位，滾輪、拖曳與部分按鈕沒有落在元素上（與 #77 記錄的「滾輪縮放與拖曳平移未被頁面記錄」同一原因）；另有目標欄選項比對與焦點兩個腳本錯誤。修正腳本（`behavior: 'instant'`、以選項文字找 State、先聚焦下拉）後重跑 Chrome 與 Edge，以下是重跑的結果。
- **結果**（`ov78_chrome.json`、`ov78_edge.json`；兩個瀏覽器相同處合併寫）：
  - OV-1：King County 方法 5、KPI 4、預測器 19 個輸入、US$503,564（PI US$351,404 – US$721,610）、散佈圖 4,323 點；50 Startups `COMPLETED`、17 個 `VALID`、方法按鈕 5、比較表 5 列、探索 test KPI、兩張圖已繪製、預測器有值、五個區塊皆標示、V1 區塊與頁尾隱藏。對外請求只有兩次按「載入 URL」時對老師範例 URL 的各一個 GET；其餘 0。頁面讀取 13 個本機檔。例外 0、對話框 0。解壓副本 `offline_scan.scan()` 13 檔 0 findings。
  - acceptor 三條：三向切換、URL 失敗後、目標欄 `TARGET_NOT_NUMERIC` 後切回 King County，五個 V1 區塊與頁尾文字逐字相同；URL 失敗訊息含 `URL_FETCH_FAILED，network` 與本機檔案指引；之後以解壓副本的 `50_Startups.csv` 載入 `COMPLETED`、顯示與內建相同、新增請求 0。
  - SR-09：見 ACCEPTANCE V2-38 與 G.2（首次繪製最大 265.1 ms、互動最大 12.6 ms、long task 0；滾輪 10 次、拖曳 3 次都被頁面記錄）。截圖 `chrome_kc_scatter_default.png`、`chrome_kc_scatter_zoom.png`、`chrome_kc_test_block.png` 我逐張目視：y=x、圓點與方塊、圖例與軸標籤可讀、放大後線段可分辨、zh-TW 無缺字方塊；`chrome_startups50_1280.png` 全頁無缺字方塊。
  - OV-2／OV-4／OV-5：見 V2-39。
  - 效能：見 V2-40（50 Startups 56.3／58.7 ms；中型資料 Chrome 17.4 s、Edge 14.1 s；第一次 Chrome 執行同一資料 13.2 s）。
  - 中型資料 `medium78.csv`：`gen_medium.js`，mulberry32(78)；x0～x19＝(12 個均勻數和 − 6)×10 四捨五入到 0.01；c0～c4 各 10 層級；y＝50＋Σ((j mod 7) − 3)·0.8·x_j＋層級效果((l·(c+3)) mod 11 − 5)＋(12 個均勻數和 − 6)·5；2,757,134 bytes，sha256 `acd13ce2730b350f08ace31f6b83efc6c0b543252e32fa91d7f90aff406795a7`。只在 scratchpad。
- **限制**：headless 瀏覽器由 Executor 驅動，不是 acceptor 的人工操作；headless 不會顯示「網頁沒有回應」，以 long task 與對話框事件替代；原生下拉以鍵盤（ArrowDown／Home／End）操作；真實觸控、Firefox、Safari、螢幕閱讀器沒有環境（NOT TESTED）。

### 6.4 不變量（A-3、I-5、CC-V2-1）

- `git show f56461b:<path> | sha256sum`：`assets/app.js` `c1ab3f21…82ad`、`hw2core.js` `e75c5d48…2c14`、`model_data.js` `6cf0c11e…a7ac`、`results/model_data.json` `69dc1465…6e61`、`style.css` `60a27016…3f3f`——與 A-3 相同。
- `git diff --name-status d7f02d4 f56461b -- results hw2.ipynb assets/app.js assets/hw2core.js assets/model_data.js assets/style.css assets/vendor doc/requirement doc/spec doc/brief doc/ticket hw2/selection.py tests/snapshots`：只有 #74 新增的 `tests/snapshots/v1_dashboard_blocks.json`。`hw2/` 自 `d7f02d4` 只有 `explore_reference.py`、`offline_scan.py`；`tests/` 既有檔只有 `test_dashboard_static.py`（CC-V2-1）。`git diff --stat 64b2dfd f56461b -- assets index.html hw2` 為空（#77 之後頁面與程式沒有改）。
- 沒有重跑 notebook、沒有新的 Test evaluation（打包核對 notebook 是既有的單次執行，`result_digest` 照舊）；沒有新增腳本檔；V1 快照測試通過。

### 6.5 Self-review

- 對照 #78 AC 六項：README（V2-35）、報告（V2-36）、ACCEPTANCE V2 條目（G.1 逐條有狀態與證據位置，V2-37～V2-43）、ZIP（V2-41）、Pages（V2-42 NOT TESTED）、不變量（V2-43）。
- 對照分配項目：(1) R3-6——README 第 15、20、21、32、59 行的頁面層級陳述全部改寫，報告第 238 行依 D-1 處理；(2) R1-F4——V2-11、V2-15、V2-17 加註，新條目沒有引用那兩張截圖；(3) R4-1～R4-4——README 與報告的 Lasso 段落（任何提前結束、真實原因、單位無關、alpha 原尺度），與 `index.html` 第 162、229 行的頁面說明一致；(4) resource-limits §6——兩處「限制」都有 (a)(b)，沒有承諾時間；(5) CF-1——取消描述含尾段的步驟邊界與「取消後不顯示任何結果」；(6) O-R2-1／O-R2-2——「接近瀏覽器文字上限（約 512 MiB）可能耗盡記憶體使分頁當掉」「更大的檔案以位元組檢查需數秒、期間頁面不回應」。
- I-4：README 與報告沒有 50 Startups 或任何探索結果數字（以 50 Startups 的探索 KPI 字串 `9,850`、`8,351`、`97,026,682`、`0.9399`、`8,917`、`0.9425` 以 `grep -F` 搜尋 README 與模板：全部 0 命中）；scope 標示齊備。
- 品質下限：沒有刪除、跳過或放寬任何測試；`tests/test_report.py` 未改。

## 7. Audit status

- Formal：本票 independent audit **required**（Bindings §5；治理 §4.1；DA derivation §7.4：H-1～H-5，A-1～A-5、A-7～A-9）。由 Orchestrator 依 Bindings §3.7 派工；之後是 Spec V2 的 Spec Integration Audit 與 DA phase acceptance（B-10 Pages 為 open item）。
- §6 全部是 Executor self-verification，不是 audit。

## 8. Remaining work and concerns

- **本票範圍內**：沒有未完成的實作或驗證。
- **Pages**（V2-42）：NOT TESTED（pending merge）；合併屬 RB-1，合併後依 B-10 以 acceptor 指示的 Lightweight work item 執行（需 audit）。
- **Push／merge／繳交**：未執行、未授權（OC §5.1；RB-1、RB-2）。新的 ZIP 只在 `dist/`。
- **觀察（不需決定）**：(1) working copy 中 5 個 V1 dashboard 檔現在是 LF（＝blob），`git status` 乾淨；下次 checkout 時 git 可能再轉成 CRLF，那時重新打包需要同樣的處理才能讓 ZIP 與 blob 逐位元相同（`hw2/package.py` 讀 working copy）。(2) `node --test tests/js/core.test.js` 單獨執行時 3 個 fixture 案例 skipped 是 V1 既有行為（pytest 會執行它們）。

## 9. 執行時間

- 開始：2026-10-22 09:33（+08:00）；BASE pytest 09:33–09:35；README、報告與測試至約 09:43（commit `f56461b`）；打包 09:44:33–09:44:48；瀏覽器檢查 09:48–09:54（每個瀏覽器約 35～40 s）；ACCEPTANCE 與本 worklog 至約 10:05。
- 收尾（約 10:10）：提交紀錄 commit 後全部 pytest 再跑一次 478 passed、0 skipped；刪除 scratchpad 的解壓 ZIP 與瀏覽器 profile（中型資料 2.8 MB 與腳本保留在 scratchpad，不進 repo）。

## 10. Contract-internal rework — SIA-F1、SIA-F2（2026-10-22）

- **來源與 authority**：Spec Integration Audit `audit/spec-SPEC-V2-c1-r1.md`（CLOSURE）的 SIA-F1、SIA-F2；DA `decisions/decision-20261022-sia-f1-dashboard-wording.md`（S1-1～S1-6；不改變 accepted 語義）。Orchestrator 派工，BASE `cec4c93`，同一 worklog identity；SIA-F2 由 Orchestrator 依 S1-6 納入本次派工。
- **修改**（commit `69f8e0794ec0fb5b4f1fcda7a1f62bc74912a89d`；`git diff --name-status cec4c93 69f8e07`：`M README.md`、`M report/report.md`，+3／−2 行）：
  - 報告 12.5 新增一條（S1-2，採 DA 的參考文字）：C-1 前面各章依舊版作業頁、保留原文；C-2 更新後的作業頁（SRC-4）主要繳交「跟 DIC2 一樣github and web」，本專案的 web 交付是 Pages 上的這個 dashboard（主詞是本專案），前言／對照表／第 7.1 節／第九章的「課堂口頭」標示只描述舊版，標示類別仍是老師要求；C-3 特徵數 `>13`（code span），第 1.2 節依舊版，不寫數字；C-4 舊版「補充」段新版未載明、不推定已刪除。形式：沒有手打數字、沒有新 placeholder、12.5 既有兩條保留、沒有「講義」、沒有超出 SRC-4 原文的說法。
  - README「Lasso 路徑的停止」與報告 12.3 同一段（S1-6，兩處只改兩點）：停止原因加入「同一步有多個 group 同時離開路徑」「預測目標在這些列上沒有變化」；尺度改為「目標在同一批列上置中後除以其均方根」。
  - 未改：第 12 章以外的模板、測試、`index.html`、`assets/`、`hw2/`、`results/`、notebook、建置與打包程式。
- **自動測試**（working tree＝`69f8e07`）：`python -m pytest -q -rs` **478 passed、0 skipped**（114 s）；Node 探索模式 6 檔 **88 pass、0 fail、0 skipped**；`core.test.js` 單獨 9 pass、0 fail、3 skipped（fixture 案例由 pytest 執行，同 §6.1）；`offline_scan` 13 files PASS。`test_explore_docs.py` 與 `test_report.py` 未改且通過（第 12 章以外與 `d7f02d4` 相同；第 12 章唯一的 placeholder 仍是 `k_range`）。
- **報告與 ZIP**（S1-4、SIA-F3）：打包前比對 working copy 與 `69f8e07` 的 blob：`index.html` 與 `assets/` 17 檔相同（前次寫回的 LF 位元組仍在），不需改寫，`git status` 乾淨。`python -m hw2.package`（11:10:55–11:11:13，exit 0）：`dist/<學號>_hw2.zip` **sha256 `8a51fc1ca26d176f3edb075f7f8aeda7a0dc659531484c10e695bc3800d08f8d`**，81,624,097 bytes，67 個項目；報告 PDF 152 頁，sha256 `ba56dc5bbb466dc3f9d7ea77ca6b464a2d5fc3374d912180c767307bfdf7f9fe`，建置後的 Markdown 含 12.5 新條目與 12.3 的新文字。讀回：`testzip()` 無錯；ZIP 內 `index.html` 與 `assets/` 17 檔與 `69f8e07` 的 blob 逐位元相同。與舊 ZIP `57e1e4a4…bcd11` 的清單逐項比對：項目名稱與順序相同，sha256 不同的只有 `hw2_report.pdf` 與 `README.md`（S1-6 的 README 修改；DA S1-4 第 3 點預期只有 PDF，是因為 S1-6 也被採用）。notebook `2e2f8afc…ff64`、ChatGPT PDF `0a5d29e3…a194` 照舊。新清單：`doc/screenshots/v2-issue78/zip_manifest_rework_69f8e07.txt`（舊的 `zip_manifest.txt` 保留）。
- **A-4 學號**：以 `.local/packaging.json` 的值 `git grep -F` 0 個檔案、`git log --all --format=%B` 0、新清單 0（不印出值）。
- **ACCEPTANCE**：V2-35、V2-36、V2-37、V2-41 加上 rework 註（新 subject、新 ZIP 與 PDF 的 sha256、新舊 ZIP 的對應）。
- **程序**：本次沒有直接啟動瀏覽器；報告建置由 `hw2.report` 在系統暫存的全新 profile 啟動 headless Chrome（用完自動刪除）。事後以命令列核對：含本 session scratchpad 路徑或 `hw2-report-browser` 的 chrome／msedge／node 程序 0 個，暫存 profile 目錄 0 個。
- **Binding**：agentId `acc8906c845bfc14f`（`gov-executor`），`('claude-opus-5-5', 'high')`：243 則，單一元素（return 前由派工者全程核對）。
- **Audit status**：依 DA S1-5，由 Spec Integration Audit cycle 1 R2（`audit/spec-SPEC-V2-c1-r2.md`）審查本 rework；本節是 Executor self-verification。
- **剩餘**：無需要 authority 的事項。`index.html` `#ex-lasso-card` 的停止原因列舉仍不完整（DA S1-6 明定不在本次範圍）。時間：約 11:00～11:20（+08:00）。
