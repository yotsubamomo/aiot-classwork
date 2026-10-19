# Audit record — Issue #67，cycle 1，R1

| 欄位 | 內容 |
| --- | --- |
| Work Contract | GitHub issue #67「HW2 T8 打包、離線驗收（OV-1～OV-6）、乾淨環境重跑與整合」（OPEN，`ready-for-agent`；高風險 H-1～H-4，A-4、A-6）；Parent Spec `home_work_02/doc/spec/SPEC.md` rev 5（#59）「報告與打包」的打包條款、Dashboard（SR-09 (a)～(g)）、人工檢查表、OV-1～OV-6 的 gate 分類；DA derivation `doc/governance/decisions/derivation-SPEC.md` §9.1（#67）、§9.3 條件 1–6、§9.5 TK-1、TK-2、§9.6 TR-01；DA 紀錄 `decision-20261018-high-risk-categories.md`（A-1～A-8）、`decision-20261018-issue60-a4-student-id.md`（S-4、S-5）、`decision-20261018-issue64-notebook-rerun.md`（N-1、N-3、N-6、§9.3 條件 7、8）、`decision-20261019-cell28-glyphs.md`（G-1～G-5）、`decision-20261019-issue65-labels-figures.md`（O-2）；Outcome Contract `doc/governance/outcome-contract.md`（Brief @ `dff7c55c`＋CC-1、AD-1、AD-3）；Brief §7、§8、§10、§11；`design/WIREFRAME-ACCEPTANCE.md`；上位契約 `doc/requirement/HW2-requirements-Multiple Linear regression.txt` 第 42–49 行；acceptor 指示：run record §14（重跑規則，逐字）、§15（以 shell 寫入交付物）、§19（RB-5 授權與擬稿、學號設定建立）；前票 findings：`audit/issue-64-c1-r1.md` F-1、`audit/issue-65-c1-r1.md` F-4、`audit/issue-66-c1-r1.md` F-1 |
| 受審 subject | branch `home_work_02-regrill`，**最後的實作 commit `e2780f46dbea4d0816a6dcc8bba0725bc6182797`**（BASE＝`ace3958c66072fb8b70b56adbf473919d4ec325d`；range 內 8 個 commit：`e0be302`、`1f3a8b6`、`99a3ed4`、`2cd2a70`、`e2f391a`、`611ad07`、`8a902c2`、`e2780f4`）。審查時 HEAD＝`5aed19f54417c9b4a0fb7415389483e2e8406f38`；`git diff --name-only e2780f4 HEAD` 只有 `doc/governance/run/run-20261018-hw2-formal.md` 與 `doc/governance/worklog/issue-67.md`（record-only，Bindings §7）；`git status --porcelain home_work_02` 審查前後皆為空。`git diff --stat ace3958 e2780f4`：15 個檔案，單元外只有 root `README.md`、`CONTEXT-MAP.md` 各 1 行，沒有 `doc/requirement/`。**未追蹤產物（以 sha256 識別，impl-default §7）**：`dist/<學號>_hw2.zip` `c84a3c5e6d295ed383fc8c085eb68f30aaa9035208cf9ca7eeaa0d9aae763fb6`（81,432,807 bytes，56 個項目，由 `e2f391ae396b2595e53a481c76fc8a7b0c45c142` 打包；`git diff --stat e2f391a e2780f4 -- home_work_02 ':!home_work_02/doc' ':!home_work_02/tests'` 為空，所以 ZIP 的內容來源在最終 subject 上沒有變化）；`dist/<學號>_hw2.ipynb` `2e2f8afc1f67fd51312b894d3a3f4873049defead185b1dd4ca2ab1ace04ff64`；acceptor 材料 `ChatGPT_logs.pdf` `0a5d29e30802270af6a7ff02b692e2bf26e808a5102c6b787adf1ee36a3ca194`、NotebookLM docx `77b8f7e7841418e3187a76bede66b63ca0a284d4e91b6e317f9728feb47e4a96`、`sources.md` `141c211b8993e889b171eb34ecc524c85c44fe83aef962ad64a4a5cb557f5e2b`；derived `gpt_assist.md` `1a9663f750253d983934034b360acce91a85e11730ce4c25bf416f1cc8976023`、`notebooklm_summary.md` `358c78f2d3b735e437c10e365ef66b238a8d56bc01d39472a70b70687ac2731d`、`notebooklm_trace.md` `5cae03568339075430c4e2d5eb9ad791ef955897a04adcc6c55849e30aeeb7b4`（全部是我自己以 `sha256sum`／Python 計算） |
| Audit 種類 | **R1**（full independent audit of accepted work scope），**cycle 1**。**本 record 不是 Spec Integration Audit**（Spec rev 5 有 8 張票，不適用單 Ticket fast path；派工明示 SIA 另外派工） |
| 角色 | `primary_reviewer`（definition `gov-primary-reviewer`；Bindings §3.1 R-PR mapping `claude-opus-5-5`／`xhigh`） |
| Assurance (a)：context independence（治理 §2.3；Bindings §3.7） | (1) **Independent context**：以 Agent tool 派工的 `gov-primary-reviewer`（非 fork），空白 context；派工內容是路徑、識別與審查約束。Worklog、run record §20 中 Executor 與 Orchestrator 的敘述只當作待驗證主張；下文的事實都是我自己核對的。(2) **Verifiable binding**：見 (b) 欄。(3) **Autonomous access**：自行讀取 Bindings、治理 §2.3、§4、impl-default §6–§7、`gh issue view 67`、Spec、全部相關 DA 紀錄、OC、Brief、wireframe acceptance、老師需求轉寫、git 歷史與 diff、修改的程式與測試；自行執行學號比對（S-4）、notebook 的條件 7(b)／G-5／N-3 核對、ZIP 解壓與逐項比對、`model_data` 深度比對、報告 PDF 附錄逐頁像素比對、完整 pytest 與 Node test、離線掃描、Chrome 與 Edge 的獨立離線量測、mutation probes、外部連結核對，以及 Executor 的 scratch 證據檔、clean clone 的 reflog 與 Executor transcript 的 binding。(4) **Self-written record**：本檔由 Reviewer 以自己的 Write 工具寫入 |
| Assurance (b)：model diversity（Bindings §5） | **Executor**：agentId `ae2448c02ec3d8940`，`meta.json` 的 `agentType`＝`gov-executor`；我以 Bindings §3.6 的同一邏輯掃描 session `4bbff425-7ff9-4cdc-b64c-cc68e824e1b1` 的 subagent transcript：`('claude-opus-5-5', 'high')` 332 則、單一元素，符合 O-1（與 run record §20 相同；worklog §10 記 318 則，是寫 worklog 當時的數字）。**本 review**：agentId `af011fa0b337b405e`，`agentType` `gov-primary-reviewer`，撰寫本 record 前觀測 `('claude-opus-5-5', 'xhigh')` 222 則、單一元素；全程核對由派工者依 Bindings §3.6 在採用本 record 前執行。**無 model diversity**（兩者同為 `claude-opus-5-5`）。Bindings §5 不宣告 diversity 關係，不記 `diversity_lost`（A-8） |
| 日期 | 2026-10-19 |

## 1. 審查方法與環境

腳本與輸出在 session scratchpad 的 `r67/`（不在 repo）。環境：單元 `.venv`（Python 3.11.2）、全域 Python 3.11.2（pypdfium2，只用於讀取與比對，以 `python -I` 執行）、Node v24.19.0、Chrome 155.0.8059.80、Edge 155.0.4283.62。

**不重新評估**：我沒有執行 `hw2.run_notebook`、任何 notebook cell 或 `hw2.package`，沒有開啟守門，也沒有對 test 列評估任何模型；沒有做獨立的完整重跑（理由見 §3 C-12：Executor 的單一次重跑可以由已提交的產物、clean clone 的 reflog 與 manifest 獨立核對，再跑一次不會增加證據）。我執行的 pytest 由 `tests/conftest.py:21-40` 在整個 process 關閉守門（`pytest_configure` 與 autouse fixture）；唯一把旗標設為 True 的 `tests/test_testgate.py:308-322` 用的是被標成正式身分的 synthetic 資料。pytest 與 Node 只讀匯出的 `test`／`test_inputs`，是 A-2 要求的獨立重算，不是 test 評估。

**學號與材料的處理**：學號只在記憶體中讀自 `home_work_02/.local/packaging.json`（`git check-ignore` 命中 `home_work_02/.gitignore:13`），所有輸出只有計數，或把它遮罩成 `<SID>`。**揭露**：審查途中我有一次以 `ls -la dist` 在終端列出 `dist/` 內容，兩個檔名含實際學號；這只在本 session 的 transcript，本紀錄與任何追蹤檔案都沒有抄錄，之後的輸出一律遮罩。`gh issue view 67` 的輸出含 GitHub 帳號的公開顯示名稱，本紀錄沒有抄錄。我解壓 ZIP 的目錄、mutation 的 scratch 複本與瀏覽器暫存 profile 用畢已刪除；刪除後 `r67/` 內含學號的檔名或內容為 0。

- **(i) 學號比對（S-4）**：見 §4 H-1。
- **(ii) 測試**（工作樹＝`e2780f4`，record-only 差異除外）：`.venv/Scripts/python -m pytest -q -rs -p no:cacheprovider` → **395 passed**，0 skipped（48.4 s；學號設定與材料存在，所以 `test_no_tracked_file_contains_the_student_id` 與 `test_the_reviewed_derived_sections_on_this_machine_when_present` 都有執行）。`node --test tests/js/core.test.js` → 12 tests，**9 pass、0 fail**，3 skipped（fixture 版，需環境變數；fixture 版由 `tests/test_node_core.py` 執行，在上面的 395 之內）。`python -m hw2.offline_scan` → `scanned 6 files: PASS (0 findings)`。
- **(iii) Notebook**（`git show` 各版本以 JSON 比對；`nb_check.py`、`nb_outdiff.py`）：見 §3。
- **(iv) ZIP**（`zip_check.py`；以 Python `zipfile` 解壓到新的空目錄，路徑先檢查沒有 `..`）：見 §2 AC-1、§3 TK-2、§4 H-2。
- **(v) `model_data`**（`md_compare.py`；對 `052984b`（#63 正式評估）深度比對，`result_digest` 依 `hw2/export.py` 的規則自行重寫計算）：見 §3。
- **(vi) 報告**（`report_check.py`）：ZIP 內 `hw2_report.pdf` 與 `dist/report/hw2_report.pdf` 相同（`8778b459…`）；pypdfium2 以 0.4 倍渲染報告第 29–149 頁與 `ChatGPT_logs.pdf` 第 1–121 頁，**121／121 逐頁像素相同**，報告共 149 頁；建置出的 Markdown 中【待填】0 處、學號 0 次；`derived/gpt_assist.md` 10／10 行、`notebooklm_summary.md` 本文 5／5 段逐字出現在建置出的 Markdown（另 2 行是 front-matter 的鍵）；報告的 8 張圖與 `results/figures/` 逐位元相同。
- **(vii) 獨立離線量測**（`ov_r1.mjs`，我自己寫的 CDP 腳本，不使用 Executor 的 `ov67.js`）：對我自己解壓的 ZIP，以 headless Chrome 與 Edge、全新暫存 profile、`Network.emulateNetworkConditions(offline)`、`--host-resolver-rules=MAP * ~NOTFOUND`、`--proxy-server=http://127.0.0.1:9` 開啟 `file://` 的 `index.html`。結果見 §2 AC-2、AC-3。
- **(viii) Mutation probes**（`mutants_r1_67.py`；`git archive e2780f4 home_work_02` 解到 scratchpad，`git init`／`git add` 使 `git ls-files` 可用，每個 mutant 只改一處、跑相關測試檔、還原）：基準 84 passed、2 skipped（scratch 複本沒有材料與學號設定）。**12 個 mutant，10 個被偵測**：D2 低於 training 下界不標示、D4 All-in 的 `shared_with` 分支關閉、E1 group 內各欄獨立打亂、P1 不檢查執行序號、P2 不檢查 run id、P3 不比對 ZIP 項目的 sha256、P4 不檢查錯誤輸出、P5 跳過正式評估核對、R1 derived 釘值不比較、R2 final 建置不呼叫 derived 核對。**存活 2 個**：P6（`hw2/package.py:111` 的 `if dirty:` 改為 `if False:`）見 **F-1**；R3（改動 `DERIVED_REVIEWED` 的一個釘值）只因 scratch 複本沒有材料、對應的本機測試 skip 而存活，在 repo 中該測試有執行並通過（(ii)），不是缺口。
- **(ix) Executor 證據的核對**（只讀）：clean clone `ex67/clean` 的 reflog：`1f3a8b6` clone 於 16:06:50（+08:00）→ fast-forward 到 `2cd2a70`（16:15:13）→ `e2f391a`（16:25:53）；`.venv/pyvenv.cfg` 建於 16:06:58（clone 之後，Python 3.11.2，新建的虛擬環境）；`cond7a.json` 寫於 16:11:12，`full_run.log` 記 08:11:26Z 開始、08:12:07Z 結束、exit 0，所以條件 7(a) 在完整重跑之前；`pip_freeze.txt` 中 `requirements.txt` 的 11 個鎖定版本全部相符；`ex67/run_outputs/` 的 21 個執行產物與 `2cd2a70` 的追蹤版 20 個逐位元相同、1 個只差 EOL。Executor 的 `chrome_result.json`、`edge_result.json`、`firefox_result.json` 與截圖存在，內容與 worklog §8 相符。

## 2. Ticket AC 逐項

| # | AC | 判定 | 證據（我自己取得） |
| --- | --- | --- | --- |
| AC-1 | 「報告與打包」的打包條款；Brief §8 ZIP 內容；學號只在 ZIP 與未追蹤設定，`git grep` 無實際學號（BR-03） | **PASS** | ZIP 檔名等於學號＋`_hw2.zip`、唯一的頂層資料夾等於學號＋`_hw2`（記憶體中比對）；`testzip` 無錯；56 個項目：`<學號>_hw2.ipynb`、`hw2_report.pdf`、`ChatGPT_logs.pdf`、`README.md`、`requirements.txt`、`index.html`、`assets/`（含 vendor Chart.js 與授權檔）、`data/kc_house_data.csv`、`hw2/` 24 個模組、`results/`（pickle、8 張 PNG、split CSV、8 個 tables CSV、`model_data.json`）——Brief §8 的九類全在；除了兩個 PDF，每個項目與 `e2f391a` 的 blob 相同（PNG、pickle、資料 CSV、vendor 逐位元，其餘只差 EOL）；`ChatGPT_logs.pdf` sha256＝收件值；沒有 `tests/`、`doc/`、`.local`、`acceptor_materials`、`derived`、`__pycache__`。`hw2/package.py`（`:107-233`）不執行 notebook，只核對（已 commit、單一次執行、正式評估）後建置報告、複製 notebook、寫 ZIP 並讀回比對。`dist/hw2_package_manifest.json` 的 56 個項目 sha256 與我解壓的檔案全部相同，`commit`＝`e2f391a`，學號 0 次。老師的繳交要求（需求轉寫第 42–49 行：學號命名的主程式、PDF 報告含 GPT 對話過程、學號命名的 zip）滿足。學號：§4 H-1 |
| AC-2 | OV-1（硬性 gate）：解壓、斷網、無伺服器、`file://`；必要區塊渲染；方法與 k 切換、預測器、散佈圖縮放；零對外請求；靜態掃描無外部 URL | **PASS** | 我的獨立量測（§1 (vii)）：Chrome 與 Edge 各載入 3 次與 10 次互動，請求 21 個，全部是 `file`（18）或 `data`（3）；**非 file／data 0**、`loadingFailed` 0、例外 0、console error 0；載入的檔案只有 `index.html`、`style.css`、`chart.umd.js`、`model_data.js`、`hw2core.js`、`app.js`；方法按鈕 5、KPI 4、canvas 2、預測器輸入 19、載入錯誤區塊隱藏、文字中 □／U+FFFD 0 個；5 次方法切換與 5 次 k 切換都記錄到重繪。`offline_scan` PASS；`index.html`、`assets/` 的 `http(s)://` 只有說明文字中的超連結（`grep`）。Executor 的可見視窗紀錄另外涵蓋預測器輸入、滾輪／拖曳／按鈕縮放、zh-TW 截圖（我看了 `chrome_sec_model_compare.png`、`chrome_scatter_default.png`、`chrome_scatter_zoom8.png`、`chrome_w375_test.png`：沒有缺字方塊）。斷網方式的充分性見 §7 C-1 |
| AC-3 | OV-6（硬性 gate）：SR-09 (a)～(g) | **PASS** | (a) 我的量測 `HW2_PERF.firstDraw`：Chrome 244（冷啟動）、75、78.5 ms；Edge 229（冷啟動）、83、83 ms（≤ 3,000）。(b) 方法切換最大 18 ms、k 切換最大 9.2 ms（≤ 1,000）；Executor 另有滾輪 34.2 ms、拖曳 4.4 ms、按鈕 4.0 ms 與 longtask 紀錄。(c) `chrome_scatter_default.png`：y=x 虛線、區間內藍色圓點與區間外橙色方塊可分辨，刻度「10 萬／100 萬／1,000 萬」。(d) `chrome_scatter_zoom8.png`（約 55 萬～230 萬）：個別 PI 線段與端點可分辨。(e) 游標提示是 DOM 元素，不在 canvas 截圖內；`chrome_result.json` 的 `hoverTip` 文字含預測、實際、95% PI 與是否落入。(f) ACCEPTANCE E 節的表：瀏覽器版本、Windows 11 10.0.26200、i9-13900HX 24 核／32 執行緒、31.7 GB 都與本機 `Get-CimInstance` 相符；n_test、量測方式與各次數值齊全。(g) 我的量測 `firstDraw.nPoints`＝`nTestPoints`＝`test_inputs.rows` 筆數＝4,323 |
| AC-4 | OV-2 required：375／768 px 無水平溢出、主要功能可操作；真實觸控 NOT TESTED | **PASS** | 我的量測：375 px 與 768 px（mobile、DPR 2）`scrollWidth − clientWidth`＝0（Chrome、Edge）。Executor 紀錄 8 種狀態、Test 區塊有正式資料（#62 R1 F-2）；`chrome_w375_test.png` 目視可讀。真實觸控記 NOT TESTED |
| AC-5 | OV-3 required：Chrome 或 Edge PASS；Firefox／Safari best effort | **PASS** | Chrome 155、Edge 155 由我與 Executor 各自量測。Firefox 123.0.1 有環境與證據（`firefox_result.json`：`moz:headless` false、首次繪製 212 ms、方法切換與預測器），ACCEPTANCE 記「best effort PASS（核心項目）」並列出限制，沒有超出證據；Safari NOT TESTED |
| AC-6 | OV-4 required：鍵盤、focus 可見、label、`aria-expanded`、基本語意；螢幕閱讀器 NOT TESTED | **PASS** | Executor 的 `chrome_result.json` `keyboard`／`semantics`：70 個 Tab 停留點的 `:focus-visible` 與 outline 逐一記錄；唯一 outline 為 none 的是日期輸入內部段落（以反白呈現，ACCEPTANCE 與 worklog 如實寫明）；Enter／Space 操作、`aria-expanded` 切換、landmarks。我沒有重做鍵盤巡覽；證據是逐一停留點的機器紀錄，足以支持 required gate |
| AC-7 | OV-5 required：一般文字 ≥ 4.5:1、大字 ≥ 3:1；不只靠顏色 | **PASS** | 我以 WCAG 公式重算最低值：`rgb(22,101,52)` on `rgb(220,252,231)`＝6.49；canvas `#475569`／`#334155`／`#666` on 白＝7.58／10.35／5.74，與紀錄相同。散佈圖以形狀（圓點／方塊）區分涵蓋狀態（截圖） |
| AC-8 | 乾淨環境重跑：全部 pytest 與 Node test 通過；重跑數字與追蹤結果檔、報告、README 一致（A-2） | **PASS** | §1 (ii)、(ix)；README 成果段 183,370、78,100、0.783、94.45%、4,083／4,323 等於 `test.forward_sfs_k17`（整體 winner 的 test 鍵）；建置出的報告引用的路徑時間 8.16、7.06、4.02 s 來自這次重跑的 `meta.path_timing_s`，不是舊值 |
| AC-9 | 重跑與 ZIP 內 `model_data` 的 `test_inputs`／`test` 與 #63 基準一致；沒有 fixture 產生的 `model_data`（TR-01） | **PASS** | ZIP 的 `results/model_data.json` 與 `assets/model_data.js` 解析後是同一物件，也等於追蹤的 `e2780f4` 版本；`result_digest`（自行計算）＝`b53ff286ae0734add8b272089aba904a1cb7f5aca444a62d356420b25dc3cfc6`＝`052984b`；`test`、`test_inputs`、`winners` 整段相同；`meta.fixture` false、`manifest.official_data` true；ZIP 與追蹤樹中的 `model_data` 只有這兩個正式路徑 |
| AC-10 | ACCEPTANCE.md 每一項有狀態與證據位置；best effort 沒有證據一律 NOT TESTED | **PASS** | 我讀完全部列：A～E 節每列都是 PASS／NOT TESTED，PASS 都指向 worklog 節次、測試或其他列；D-12 為 NOT TESTED（pending merge）；真實觸控、Safari、螢幕閱讀器 NOT TESTED；OV-1 列寫明「瀏覽器層斷網」的方式。`tests/test_report.py::test_acceptance_statuses_are_filled_with_evidence` 機械核對這些規則（§7 C-3） |
| AC-11 | Root README／CONTEXT-MAP 一列：取得 RB-5 授權後才修改，獨立 commit | **PASS** | `611ad07` 只改 `README.md`、`CONTEXT-MAP.md`，各新增 1 行、刪除 0 行；兩行與 run record §19 擬稿**逐字相同**（以程式擷取比對），位置分別在 `home_work_01/` 列與 HW10 列之後；擬稿行在 `cf266d4`、`cbb895d`、`e2780f4`、`HEAD` 的 sha256 都相同（授權後沒有改動）；授權紀錄 `cbb895d`（15:50）早於 `611ad07`（16:32） |
| AC-12 | （TK-2）ZIP 內含結果目錄的 CSV 與 PNG，與報告引用一致 | **PASS** | 建置出的報告以 `fig:` 引用 8 張圖，都在 ZIP 的 `results/figures/` 且與報告建置用的複本逐位元相同；表格在建置時由 `results/tables/` 與 `model_data` 注入，8 個 CSV 都在 ZIP |
| AC-13 | （TK-1／AD-3）Pages 不是完成條件；記 NOT TESTED（pending merge） | **PASS** | ACCEPTANCE D-12 與 F 節；worklog §8.7 |

## 3. DA 義務（G-3／G-5、N-3、§9.3 條件 7、8、TR-01）

| 義務 | 判定 | 證據 |
| --- | --- | --- |
| G-3：cell 28 獨立 commit、只改一行 | 符合 | `e0be302` 只改 `hw2.ipynb` 1 行（`git show`）：`label=models.METHOD_LABELS[m])` → `label="Lasso path ranking" if m == "lasso_path" else models.METHOD_LABELS[m])`，沒有加註解；commit 早於 `1f3a8b6` 與完整重跑 |
| 條件 7(b)（G-5 修正版） | 符合 | 我對 `1f3a8b6`、`2cd2a70`、`e2f391a`、`e2780f4` 各做一次：cell 0–27、29–45 的 source、id、型態與 `052984b` 相同（45 格）；cell 28 恰有 1 處新行、0 行新增註解，換回原文後與 `052984b` 完全相同；notebook metadata 相同；凍結模組 `hw2/{data,split,preprocess,selection,models,comparison,ols,metrics,contract,testgate,export}.py` 與 `requirements.txt` 對 `052984b` 的 diff 在四個版本都為空；資料 blob 的 sha256＝Brief 釘值 |
| 條件 7(a)：重跑前、不開守門的 selection digest | 符合（依紀錄） | `cond7a.json`：`selection_digest`＝`44f7723e…4b28`、`official_test_rows_loaded` false、`gate_enabled` false；`cond7a.py` 只執行 cell 41 之前的 code cell，先在 kernel 內把旗標設為 False；時序在重跑之前（§1 (ix)）。重跑的 manifest `selection_digest` 也是 `44f7723e…` |
| 條件 8、N-1：單次評估、只評估授權集合、記錄重現 | 符合 | manifest：`evaluations_in_this_run` 1、`scored.ols_subset`＝`allin`、`forward_sfs_k17`＝`winners.authorized_test_models`、`metric_only`＝`lasso`、`ridge`；`run_id` `5e74d03d…`、`code_revision` `1f3a8b6`（`package_modified` false，與 reflog 相符）；worklog §5 記錄「#63 run `fe76019b…` 的重現」；README 與報告附錄 A 仍以 `fe76019b…` 為唯一一次正式評估（N-5） |
| N-3：單一次執行是追蹤版與打包版的唯一來源 | 符合 | `e2780f4` 的 notebook：40 個 code cell，執行序號 1…40 連續、錯誤輸出 0；評估 cell（41，唯一含 `gate.open(` 的格）印出的 `run_id` 等於追蹤 `model_data` 的 manifest；`dist/<學號>_hw2.ipynb`、ZIP 項目與工作樹 `hw2.ipynb` 的 sha256 都是 `2e2f8afc…`，與追蹤 blob 只差 EOL。對 `052984b` 的 `model_data` 有 70 個不同的葉節點，**全部**在 N-3 允許的欄位內（`meta.generated_at`、`meta.timing_s`、`meta.path_timing_s`、`meta.comparison_timing_s`、`baselines.pvalue_backward.timing_s`、`meta.test_evaluation` 的時刻／耗時／`code_revision`、manifest 的 `run_id`／時刻）；`meta.versions` 相同（#60 R1 F-4：無版本漂移）。PNG、CSV、pickle 在 `ace3958..e2780f4` 沒有 git delta。Notebook 輸出與 `ace3958`（混合執行版）相比，只有 cell 5、21、25、30、33（耗時）、28（G-5）、41（印出的檔案大小與 manifest，大小由允許欄位的文字長度決定）以及 49、72（`execute_result` 的執行序號）不同；cell 46 之後由 #64／#65 部分執行產生的輸出在這次完整執行中逐字重現 |
| G-5 (i)(ii) | 符合 | 整份 notebook 輸出「Glyph」0 次、「missing from font」0 次、stderr 0 個、本機絕對路徑 0 個；cell 28 只有 1 個 `display_data`（`image/png`＋`text/plain`＝`<Figure size 900x450 with 1 Axes>`）；我把 PNG 解出目視：圖例 5 個標籤 `Forward SFS`、`Backward SFS`、`RFE`、`Lasso path ranking`、`All-in baseline` 都可讀 |
| N-6 | 符合 | 派工沒有沿用「不得執行」；完整重跑只一次（reflog 與 `full_run.log`；`package.py` 不執行 notebook） |
| TR-01、§9.3 條件 3、4 | 符合 | 見 AC-9；#67 沒有改動選擇、alpha、前處理、模型集合或授權集合的程式（條件 7(b)） |

## 4. 高風險類別（A-1）

| 類別 | 核對內容 | 結果 |
| --- | --- | --- |
| **H-1** 不得公開的資料 | **S-4（DA `decision-20261018-issue60-a4-student-id.md`）我自己重做 S-2**，比對值只在記憶體中讀自 `.local/packaging.json`（10 字元），只輸出計數（`sid_check.py`）：(i) `origin/main`（`5be4d394`）`..HEAD`（`5aed19f`）共 **88 個 commit 的樹**，每個 commit 以 `git grep` 比對完全相同、不分大小寫、全形數字、千分位分組，以及字元之間允許空白、`_`、`.`、`,`、`/`、`-` 的變形：**0 命中**（grep 錯誤 0）；(i-b) 同一 range 每個 commit 的 patch（含 `--binary`）：**0**；(ii) 每個 commit 物件全文（含 author／committer 標頭與訊息）：**0**；(iii) 工作樹的 1,458 個追蹤檔案：**0**；ref 名稱：0；(iv) GitHub issues #59～#67 的標題、本文與留言：**0**；本 branch 的 PR：0 個。另外以前 7、8 碼與後 7、8 碼做部分比對（前後綴變形）：追蹤檔案 0。**正向對照**：在 scratch 中建立含該值（含一個分隔變形）的暫時 repo，同樣的樹、分隔變形與訊息比對全部偵測到。結論：**已核對、無命中**，範圍 `origin/main`..`5aed19f`（含 `e2780f4`）。ZIP 名稱與頂層資料夾含學號（打包規則要求）；`dist/hw2_package_manifest.json`、建置出的報告 Markdown／HTML：0 次。(b) 追蹤檔案：PDF 只有 `doc/requirement/` 的老師文件；沒有 `.zip`、`.env`（只有 `home_work_01/.env.example` 範本，單元外）、`kaggle.json`、`.local/`、`dist/`、`acceptor_materials/`。(c) ChatGPT PDF metadata 的作者姓名（記憶體中比對，不印出）：ZIP 內 45 個非 PDF 項目 0、追蹤檔案 0、`ace3958..HEAD` 的 commit message 0；ZIP 文字項目中的本機絕對路徑 0。(d) 作者材料只在 ignored 的 `acceptor_materials/` 與 `dist/`。(e) Scratch 衛生：見 **F-2** | 符合（S-4 無命中；F-2 Low） |
| **H-2** 老師指定的名稱與格式、dashboard | `<學號>_hw2.ipynb`、`<學號>_hw2.zip`、單一頂層資料夾（AC-1）；報告章節：建置出的 Markdown 有標示對照表、第 1～11 章（第 2～7 章依序是六個 CRISP-DM 階段）、附錄 A、B，「GPT 輔助內容」「NotebookLM 摘要」是第 10、11 章標題（逐字）；notebook 六章名稱與順序沒有改動（`test_notebook_structure.py` 通過；cell 0–45 source 與凍結版相同）；附 PI 的預測圖在 ZIP 與報告中；dashboard 路徑 `home_work_02/index.html` 不變，`file://` 離線（AC-2），沒有新增資源（`index.html`、`style.css`、`hw2core.js`、vendor 無 diff）。`app.js` 的兩處修改（`e2f391a`）只改刻度：「指標 vs k」以 `afterBuildTicks` 在 k = 1…18 放刻度；價格 ≥ 1,000 萬時以整數萬顯示。它們不讀 `test`／`test_inputs`、不新增 URL，來源是 #65 C-4／DA O-2（交 #67 D-1、D-4）與 #65 R1 §8 第 4 點，屬 #67 的檢查範圍；截圖確認兩者生效（`chrome_sec_model_compare.png` 的 k 刻度 1～18；`chrome_scatter_default.png` 的「1,000 萬」）。Cell 28 的英文圖例在主程式中（DA G-5 審查要求） | 符合 |
| **H-3** 評估完整性 | A-2：自行執行完整 pytest（395 passed，含 `test_model_data_official.py::test_independent_recomputation_of_every_official_test_row` 的逐筆 PI 重算、分組隔離、選擇邊界）與 Node（官方逐筆重算 pass）；自行比對匯出結果與 README、報告的數字（AC-8）。A-3：`methods`／`baselines` 沒有任何 `test*` 欄位；`test` 的鍵＝`allin`、`forward_sfs_k17`（`ols_subset`）＋`lasso`、`ridge`（`metric_only`）；`app.js` 只在 `testRows()`（`:658-666`）讀 `test_inputs` 的識別與實際價格供繪圖，#67 的 `app.js` delta 不涉及。單次評估與重現：§3。凍結模組沒有改動 | 符合 |
| **H-4** 證據真實性與如實標示 | ACCEPTANCE.md 的每個 PASS 都有我能對應的證據（AC-10），best effort 沒有證據的記 NOT TESTED，Firefox 的部分驗證如實寫出限制，OV-1 如實寫出斷網方式；OV-6 只記實測值（我的量測與 Executor 的數值同一量級，沒有 fixture 或 wireframe 數字）。A-5：ChatGPT PDF sha256＝收件值；derived 三檔 sha256＝#66 R1 審查版本，final 建置由 `hw2/report.py` 的 `DERIVED_REVIEWED`（`:127-134`）與 `check_derived_reviewed()`（`:527-543`、`:1130-1131`）強制，我的 R1、R2 mutant 被偵測；`report/` 的模板在 `ace3958..e2780f4` 沒有變更，第 1～9 章與 #66 R1 審查的建置相同，所以 mock 數值的狀態不變；`app.js` 與 README 的 delta 沒有結果數字。報告附錄 121 頁與 ChatGPT PDF 逐頁像素相同（§1 (vi)） | 符合 |

其他 assurance：A-6 屬 Spec Integration Audit，本 record 的 AC-1、AC-2、§1 (iv)(vii) 可作為其引用的入口，但不取代它；A-7 適用（本 record 沒有 blocking finding）；A-8 見表頭 (b)。

## 5. 前票 findings（owner #67）

| 來源 | 內容 | 狀態 |
| --- | --- | --- |
| `issue-64-c1-r1.md` F-1 | D2、D4、E1 三項行為沒有被測試守住 | **resolved**：`tests/test_deployment.py` 新增 `test_predict_price_flags_values_below_the_training_minimum`、`test_shared_with_lists_the_allin_baseline_when_the_overall_winner_is_that_model`；`tests/test_diagnostics.py` 新增 `test_permutation_moves_a_groups_columns_together`。我重做的 D2、D4、E1 mutant 都被偵測（§1 (viii)） |
| `issue-65-c1-r1.md` F-4 | cell 28 圖例缺字 | **resolved**：依 DA G-3 修正，G-5 (i)(ii) 成立（§3） |
| `issue-66-c1-r1.md` F-1 | derived 文字沒有被釘住 | **resolved**：實作選擇以追蹤的釘值強制（會留下 git delta）；final 建置前核對；現在三檔 sha256＝#66 R1 表頭；ZIP 的報告由這三檔建置（§1 (vi)）。Spec Integration Audit 仍依 #66 R1 的 disposition 核對 |
| `issue-66-c1-r1.md` F-2 | `pdf_append.py` 的輸入範圍 | 不需處理（材料 sha256 未變） |
| `issue-62-c1-r1.md` F-2、`issue-60-c1-r1.md` F-4、#65 C-4／R1 §8 第 4 點、#66 C-3 | OV-2 在 Test 有資料時量測；版本漂移；k 刻度與價格刻度；SciTePress DOI | 皆已處理：AC-4；§3 N-3（`meta.versions` 相同）；§4 H-2；外部來源 4 個連結與 Kaggle 資料集頁我自己核對：3 個 `curl -L` 200，SciTePress DOI 在 curl 下停在 302，以 headless Chrome 開啟解析到標題「SciTePress - Publication Details」、內容含「Influencing Factors of Housing Price」；Kaggle 200 |

## 6. Findings

### F-1 — Low，non-blocking：`hw2/package.py` 的「打包的追蹤檔案都已 commit」核對沒有被測試守住（mutation probe P6 存活）

- **證據**：`hw2/package.py:107-112` 的 `check_committed()` 是 ZIP 能追溯到 manifest 所記 commit 的前提（模組說明第 2 點，`:13-14`）。我把 `:111` 的 `if dirty:` 改為 `if False:`，`tests/test_package.py` 17 passed（§1 (viii)）；`tests/` 中沒有任何測試呼叫 `check_committed` 或 `package()`。
- **契約條款**：Spec rev 5「報告與打包」（記錄 ZIP 的 sha256 與檔案清單）；impl-default §5 quality floor 與 §7（結果要能識別其 subject）。
- **風險判斷**：若這個核對日後壞掉，從未 commit 的工作樹打包時不會被擋下，而 manifest 仍寫 `HEAD` 的 commit，ZIP 內容與所記 commit 就可能不一致。**本次交付不受影響**：我把 ZIP 的每個追蹤來源項目與 `e2f391a` 的 blob 逐一比對，全部相同（AC-1）。因此判為 Low。
- **Disposition**：不延長 cycle，本票不需修改。Owner＝**之後任何修改 `hw2/package.py` 或重新打包的 work item**：補一個在暫時 git repo 中製造未 commit 修改、斷言 `check_committed()` 拒絕的測試。目前不需行動。

### F-2 — Low，non-blocking：session scratchpad 中 Executor 的瀏覽器暫存 profile 仍含實際學號的痕跡；worklog §9 的陳述不完全

- **證據**（只輸出計數）：`ex67/ov2/prof-chrome`（303 個檔，4 個含學號）、`ex67/ov2/prof-edge`（291／3）、`ex67/ov2/prof-firefox`（96／3）、`ex67/ov2/prof-date`（302／2）、`ex67/ov/prof-chrome`（303／4）；推測是瀏覽紀錄或工作階段中的 `file://` 路徑（解壓資料夾以學號命名）。`ex67/` 其餘 5,633 個檔（不含 profile 與 venv）：檔名 0、內容 0，clean clone 沒有 `.local`、`acceptor_materials`、`dist`——worklog §9 所列的複本確實已刪除。但 worklog §9 寫「ZIP 與 `dist/` 以外沒有寫出含學號的檔案」，與這些 profile 不符。
- **契約條款**：`decision-20261018-high-risk-categories.md` H-1（涵蓋位置含 log 與終端輸出）；Brief §11 BR-03。
- **風險判斷**：這些檔案在本機暫存目錄，不在 repo、不被追蹤，也不在任何 push 或合併的路徑上；H-1 的風險機制（公開後不可逆）沒有被觸發。屬本機衛生與紀錄準確度，判為 Low。我自己審查時產生的同類檔案（解壓目錄、瀏覽器 profile、scratch 複本）已刪除（§1）。
- **Disposition**：不延長 cycle，不是 #67 的結案條件，也不改變受審 subject。Owner＝**Orchestrator**（控制面清理，不涉及追蹤檔案）：刪除上列 5 個 profile 目錄並在 run record 記錄，同時註明 worklog §9 該句的範圍不含瀏覽器 profile。

### F-3 — Low，non-blocking：ZIP 內 README 的「重跑步驟」以 repo 的配置為前提，在解壓後的 ZIP 中不能照做

- **證據**：`README.md:44-57` 寫「在 `home_work_02/` 目錄執行」`python -m hw2.run_notebook`、`pytest`、`node --test tests/js/core.test.js`。`hw2/run_notebook.py:10` 執行 `UNIT_DIR / "hw2.ipynb"`，而 ZIP 中的主程式是 `<學號>_hw2.ipynb`（ZIP 沒有 `hw2.ipynb`）；ZIP 也沒有 `tests/` 與 `pytest.ini`（AC-1 的項目清單）。所以評分者在解壓的資料夾照 README 執行時，第一個指令就會找不到檔案。直接以 Jupyter 開啟 `<學號>_hw2.ipynb` 不受影響（`hw2/`、`data/`、`results/` 都在 ZIP 內）。
- **契約條款**：Brief §8 的 ZIP 內容清單（不含測試）與 README 的「重跑步驟」；Brief §10 的乾淨環境重跑是對 repo 執行（Spec「人工檢查表」的乾淨環境重跑包含「打包」），沒有要求 ZIP 本身可照 README 重跑。所以沒有違反 accepted 條款。
- **風險判斷**：只影響評分者的使用體驗；判為 Low。
- **Disposition**：不延長 cycle，本票不需修改。是否在繳交前為 ZIP 補一句說明（例如「以下步驟在 repo 中執行；ZIP 內請直接開啟 `<學號>_hw2.ipynb`」）由 **acceptor** 決定（繳交屬 RB-2）；若要修改，以新的 work item 處理（修改 README 與重新打包觸及 H-2）。

## 7. Executor concerns（worklog §11）的審查意見

| ID | 意見 |
| --- | --- |
| C-1（OV-1 以瀏覽器層斷網） | **我判定證據足以支持 OV-1 PASS**（evidence sufficiency 屬 Reviewer）。Brief §7 BR-04 的可觀察結果是：必要區塊與互動正常，且頁面不發出對外請求，「以瀏覽器開發者工具的網路面板核對為零，或以靜態掃描確認」。DevTools offline、所有主機名稱無法解析、無效 proxy 三者並用，頁面發出的任何網路請求都會失敗，與停用網卡時頁面看到的條件相同；載入的 6 個資源都是 `file://`，靜態掃描 0 findings，我以獨立腳本在兩個瀏覽器重做也得到同樣結果（AC-2）。網卡層級是否停用不改變 `file://` 頁面的可觀察行為。ACCEPTANCE OV-1 列如實寫出方式，沒有把它寫成「網卡停用」。我不把這視為契約語義不足，不需要 route；acceptor 若希望另外實體斷網目視一次，那是 acceptor 自己的選擇，不是本票的結案條件 |
| C-2（`app.js` 兩處修正） | 我讀了 diff（`e2f391a`，`:389-393`、`:789-795`）：只改刻度的產生與顯示，不碰計算、資料或資源；截圖確認效果。屬 #67 被指派的 D-1／D-4／OV-6 (c) 檢查範圍內的 HOW，之後的 OV 檢查全部在新 ZIP 上重做（Executor 結果檔的時間晚於打包，我的量測也在這個 ZIP 上）。不構成 finding |
| C-3（ACCEPTANCE 測試規則的替換） | 舊測試 `test_acceptance_marks_nothing_pass_before_it_is_verified` 的語義就是「#67 驗收之前」；#67 的 AC 要求填寫狀態，舊規則必然失敗。新規則要求每列有 PASS／FAIL／NOT TESTED、沒有 PENDING、PASS／FAIL 有證據位置、D-12 與三個 best-effort 項目為 NOT TESTED、subject 與 OV-6 紀錄已填。這是契約狀態的轉換，不是放寬 |
| C-4（manifest 的 `code_revision` 與 ZIP 來源 commit 不同） | 我核對了 `1f3a8b6..e2f391a` 的 delta：`hw2/package.py`、`tests/test_package.py`、`assets/app.js` 與這次執行的產物；選擇與評估的模組、notebook source 都沒有變（§3）。`code_revision` 屬 N-3 允許的欄位；ZIP 的 commit 記在 `dist/hw2_package_manifest.json`，ACCEPTANCE 的 subject 行也寫明兩者的關係。追溯完整，不構成 finding |
| C-5（Firefox 的限制） | Best effort，ACCEPTANCE 如實列出限制（零對外請求以 Chrome／Edge 與靜態掃描為準）；不影響 required gate |

## 8. Routing

沒有需要其他 authority 的事項：沒有契約語義不足或 boundary 疑義（C-1 是 evidence sufficiency，由本 record 判定），也沒有 blocking finding。F-1～F-3 的 owner 見各自的 disposition（F-3 的修改與否屬 acceptor 的 RB-2 範圍，不是授權缺口）。

## 9. Closure evidence

- 13 條 AC 全部 PASS；DA 義務 G-3、G-5、條件 7、8、N-1、N-3、N-6、TR-01 符合；H-1～H-4 核對符合。
- **S-4 已由本 R1 重做**：`origin/main`..`5aed19f` 的 88 個 commit 的樹、patch 與 commit 物件，工作樹追蹤檔案，issues #59～#67，以及本 branch 的 PR（0 個），含變形比對，**已核對、無命中**。S-5 的其餘時點（Spec Integration Audit、phase acceptance、合併）仍須各自涵蓋到其 subject。
- 前票 findings：#64 R1 F-1、#65 R1 F-4、#66 R1 F-1 resolved。
- Blocking findings：無。Non-blocking：F-1（Low，owner 之後修改打包程式的 work item）、F-2（Low，owner Orchestrator）、F-3（Low，acceptor 決定是否處理）。
- 受審 subject：`e2780f46dbea4d0816a6dcc8bba0725bc6182797`，加上表頭以 sha256 識別的 ZIP 與其他未追蹤產物。Pages 檢查依 AD-3 仍是合併後的 open item。

VERDICT: CLOSURE
