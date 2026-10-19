# Worklog — issue #66（HW2 T7 Acceptor 證據整合與 final 報告）

- **Work item**：GitHub issue [#66](https://github.com/yotsubamomo/aiot-classwork/issues/66)，run `run-20261018-hw2-formal`（Formal，並行度 1）。
- **狀態**：實作與 self-verification 完成，待 Orchestrator 核對 binding 並派 R1。本檔不代表 audit 或 closure。
- **Subject**：branch `home_work_02-regrill`，base `752791b8b1d3a11bade1e976b8da524642f66b89`；implementation commit **`d379732983e0f446cc443d95a5f70d5e68209b17`**（本機，未 push）。本檔以其後的 record-only commit 加入（Bindings §7）。

## 1. Contract reference

| 項目 | 內容 |
| --- | --- |
| Ticket | #66（OPEN；高風險 H-1、H-2、H-4）；索引 `doc/ticket/tickets.md` |
| Spec | `doc/spec/SPEC.md` rev 5：「報告與打包」的報告條款（章節依 Brief §8、附錄 ChatGPT PDF）、「Acceptor 輸入與等待」（缺少時只停止對應章節）、人工檢查表「報告」 |
| Brief | `doc/brief/BRIEF.md` §8（PDF 報告章節）、§9（acceptor 專屬輸入；agent 只整理、摘要、翻譯，不新增內容或來源；「GPT 輔助內容」如實揭露 ChatGPT 與 Claude Code 各自的用途） |
| 上位契約 | `doc/requirement/HW2-requirements-Multiple Linear regression.txt` 第 39–41、44–47、56 行（ChatGPT 對話匯出 PDF；NotebookLM 研究與 100 字以上摘要；兩個標示；報告檔需包含 GPT 對話過程） |
| DA records | `derivation-SPEC.md` §9.1（#66 的分配）、B-15（漢字計 ≥100）；`decision-20261018-high-risk-categories.md`（H-1、H-4；A-4、A-5）；`decision-20261018-issue60-a4-student-id.md`（S-1～S-6、§2.2：#66 加 H-2，R1 核對兩個標示與 B-15）；`decision-20261018-issue62-shared-subset-test-key.md`（D-2、D-3，未觸及）；`decision-20261018-issue64-notebook-rerun.md`（N-4：不全量重跑）；`decision-20261018-issue64-standardized-reading.md`（未觸及）；`decision-20261019-issue65-labels-figures.md`（未觸及）；`decision-20261019-cell28-glyphs.md`（#66 不改 cell 28：未改） |
| Outcome Contract | `doc/governance/outcome-contract.md`：Brief @ `dff7c55c`＋CC-1、AD-1～AD-3 |
| 授權與派工約束 | Run record §1（Implementation；SA-1 本機 commit；不 push、rebase、merge、force push）；§14 第 5 點（不可自行生成或替代證據）；§15（shell 寫入交付物的 workaround 已獲 acceptor 同意）；§17（材料收件）。Orchestrator 派工約束：只改 `home_work_02/` 追蹤檔案、不改 `doc/requirement/`、notebook cells 0–45、凍結模組、`requirements.txt`、`results/`、`assets/`；不重新執行正式 Test 評估、不全量重跑 notebook；材料、PDF、ZIP、實際學號不進追蹤檔案或 commit message；不建立 `.local/packaging.json`；報告 PDF 只在未追蹤的 `dist/` |
| 前票 | `worklog/issue-65.md`（報告建置方式、三個【待填】位置）；`audit/issue-65-c1-r1.md`、`issue-65-c1-r2.md` |
| Bindings | b5；HOW `impl-default` v2（overrides none） |

## 2. Acceptor 材料收件與核對（H-1、A-5）

依 run record §17 的收件紀錄，於 2026-10-19 14:47 +0800 重新計算 sha256（`sha256sum`），三個檔案都與收件紀錄相同。全部在未追蹤的 `home_work_02/acceptor_materials/`（`git check-ignore` 命中 `home_work_02/.gitignore:16`）。

| 檔案 | 收件（run record §17） | 大小 | sha256（本票核對） |
| --- | --- | --- | --- |
| `acceptor_materials/ChatGPT_logs.pdf` | 2026-10-19（檔案時間 09:58:36 +0800） | 41,784,474 bytes，121 頁 | `0a5d29e30802270af6a7ff02b692e2bf26e808a5102c6b787adf1ee36a3ca194` |
| `acceptor_materials/notebooklm/notebooklm_report_v2_2026-10-19.docx` | 2026-10-19（14:34:00 +0800） | 16,794 bytes | `77b8f7e7841418e3187a76bede66b63ca0a284d4e91b6e317f9728feb47e4a96` |
| `acceptor_materials/notebooklm/sources.md` | 2026-10-19（14:34:00 +0800；7 個來源，Orchestrator 依 acceptor 指示去重複的轉錄） | 1,951 bytes | `141c211b8993e889b171eb34ecc524c85c44fe83aef962ad64a4a5cb557f5e2b` |

- `acceptor_materials/notebooklm_v1_superseded/` 是 acceptor 放棄的第一版：**沒有讀取、沒有使用**。
- 報告建置程式把上表三個 sha256 釘在 `hw2/report.py` 的 `ACCEPTOR_MATERIALS`：檔案不同就拒絕建置（route acceptor）；檔案不存在時只有對應章節以【待填】標示。
- 讀取方式：ChatGPT PDF 是 Microsoft Print to PDF 的影像頁（沒有文字層），以 pypdfium2（全域 Python，不在單元環境）渲染全部 121 頁到 session scratchpad 逐頁閱讀；docx 以 python-docx（全域）擷取文字到 scratchpad。兩者都不在 repo 內。

## 3. Executing role and binding

- **角色**：Executor（`gov-executor` subagent，由 Orchestrator 派工）。
- **Binding 觀測**（Bindings §3.6 同一邏輯，掃描 `subagents/agent-ae6f6de8468402cf7.jsonl`，`meta.json` 的 `agentType`＝`gov-executor`）：implementation commit 之後觀測 `('claude-opus-5-5', 'high')` 276 則，單一元素，等於 O-1 mapping。全程核對由 Orchestrator 在採用 return 前執行。
- **Escalation／替代**：無。**Bounded assignments**：未使用。

## 4. Work performed

### 4.1 追蹤的產物（commit `d379732`，9 個檔案，全部在 `home_work_02/`，沒有 `doc/requirement/`）

| 路徑 | 內容 |
| --- | --- |
| `hw2/pdf_append.py`（新增） | 把一個 PDF 的頁面原樣接在另一個 PDF 之後：解析 classic xref（含 `/Prev` 增量更新；容忍 xref offset 指在物件標頭前的換行，Microsoft Print to PDF 有此情形）、只複製附加檔頁面樹可達的物件並平移物件編號（以 tokenizer 改寫 `n g R`，字串內容不動，stream 位元組不動）、新增根 `/Pages` 節點收兩棵原頁面樹、保留 base 的 catalog 與 `/Info`；xref stream／object stream 一律拒絕（`PdfError`）。`page_count()`、`document_info()`。不新增套件 |
| `hw2/report.py` | 新增 `{{evidence:…}}`（`gpt`、`notebooklm`、`chatgpt_pdf`、`status`）取代 `{{pending:…}}`；`load_evidence()` 讀未追蹤的 `acceptor_materials/`：材料 sha256 對收件紀錄、`derived/` 的章節；NotebookLM 區塊＝「依 NotebookLM 研究整理」說明＋摘要本文（`count_hanzi` ≥ 100，DA B-15）＋來源表（由 `sources.md` 原表解析）；`check_notebooklm_trace()`：摘要每一句都依序出現在對照表、位置／依據／來源欄非空；ChatGPT 附錄區塊（檔名、頁數、sha256、PDF 建立時間與 Producer）；`attach_chatgpt_appendix()`：PDF 建置後把 ChatGPT PDF 原頁接在報告頁之後並核對頁數；報告狀態行依是否仍有待填切換 final／draft |
| `report/report.md` | 狀態行改為 `{{evidence:status}}`；第十章加引言、10.1 ChatGPT（`{{evidence:gpt}}`）、10.2 Claude Code（追蹤的揭露文字，只寫 repo 可核對的用途，不含材料內容）；第十一章加老師原文引用與 `{{evidence:notebooklm}}`；附錄改為「附錄 A：重現資訊」「附錄 B：ChatGPT 對話 PDF」（B 放最後，PDF 原頁才能緊接其後），附錄 B 加老師原文引用 |
| `tests/test_pdf_append.py`（新增） | 9 項（合成 PDF）：兩檔頁面依序且內容不變、xref offset 正確、base catalog／Info 保留與新根節點、字串中的參照樣式不被改寫、增量更新取最新定義、版本取較高者、拒絕不支援的輸入、Info 字串解碼、物件標頭前的空白 |
| `tests/test_report.py` | 既有測試改以「沒有材料」的 `Evidence()` 執行（不受本機是否有材料影響）並加狀態行斷言；新增 13 項：漢字計數、合成材料的完整渲染與 `--final` 建置、附錄 B 是最後一節、材料 sha256 不符停止、缺材料只停止自己的章節（三種組合）、摘要句未依序對照停止、句外文字停止、99／100 漢字邊界、對照表空欄停止、來源表格式錯誤停止、附錄頁接在報告頁後且內容不變、頁數不符停止、本機有真實材料時核對（無材料時 skip） |
| `tests/test_repo_hygiene.py` | ignore 探針加 `acceptor_materials/derived/notebooklm_summary.md` |
| `README.md` | 報告建置說明加 AI 證據章節的讀取、核對與附錄行為；本機不進 git 的表格註明 `acceptor_materials/derived/` |
| `doc/acceptance/ACCEPTANCE.md` | A-6 的證據位置（§10、§11、附錄 B、核對程式與測試、worklog）與狀態說明（仍 PENDING，待審查與 #67 驗收）；C-7 的「附錄 B」改為「附錄 A」（重現資訊）；F 節 AI 證據的交接說明 |
| `hw2/__init__.py` | 模組清單加 `pdf_append` |

### 4.2 未追蹤的產物（不進 git；`acceptor_materials/derived/`，由本票 Executor 依材料整理）

| 檔案 | sha256 | 內容 |
| --- | --- | --- |
| `gpt_assist.md` | `1a9663f750253d983934034b360acce91a85e11730ce4c25bf416f1cc8976023` | 報告 10.1：ChatGPT 在對話中的用途（五類，附原 PDF 頁碼）；有一部分作者決定採用 ChatGPT 建議或其起草回覆的揭露（例：OC 的 CC-1 決定文字與 PDF 第 90 頁 ChatGPT 起草的回覆開頭相同，已逐字比對 `outcome-contract.md` 第 95 行）；ChatGPT 在該對話中沒有寫程式、沒有計算分析結果 |
| `notebooklm_summary.md` | `358c78f2d3b735e437c10e365ef66b238a8d56bc01d39472a70b70687ac2731d` | 報告第十一章的摘要本文：11 句、5 段，漢字 523 |
| `notebooklm_trace.md` | `5cae03568339075430c4e2d5eb9ad791ef955897a04adcc6c55849e30aeeb7b4` | 對照表：每一句 → docx 的章節位置、原文摘錄、`sources.md` 編號；材料內部不一致與未採用內容 X-1～X-5 |

建置輸出（不進 git）：`dist/report/hw2_report.{md,html,pdf}`。最後一次 `python -m hw2.report --final`（2026-10-19 15:13 +0800 左右，commit `d379732` 的程式）：pending 無、evidence＝gpt／notebooklm／chatgpt_pdf、報告 28 頁＋附錄 121 頁＝149 頁、PDF sha256 `670f5aa23df7913bd12790b2854293efb57f88c8f24a269daa6a164a0ce8ddeb`（Chrome 的 CreationDate 每次不同，所以每次建置的 sha256 不同）、`external_requests: []`、Chrome 155.0.8059.80。

### 4.3 重要決定（HOW）與理由

- **材料衍生的文字放在未追蹤位置**：「GPT 輔助內容」的 ChatGPT 部分、NotebookLM 摘要與其對照表都由材料衍生（描述作者的對話、摘錄 NotebookLM 報告）。Brief §9 與 US-40 要求材料「不進 git、只進 ZIP 與報告」，H-1 (b) 把「含有這些材料的產物」也列為風險；衍生摘要是否算「材料」有兩種讀法，放在未追蹤的 `acceptor_materials/derived/` 同時滿足兩種讀法，不需要裁定。追蹤的模板只留佔位符；10.2 Claude Code 的揭露只寫 repo 可核對的事實，所以放在追蹤的模板。代價：報告的這三個章節只能在有材料的機器上重建（ChatGPT 附錄本來就如此）。見 C-1。
- **ChatGPT PDF 併入報告 PDF**：作業頁「報告檔：PDF，需包含……GPT 對話過程」；Brief §8「附錄 ChatGPT PDF」。以 `hw2/pdf_append.py` 逐物件複製原頁（不重新渲染），所以附錄與原檔逐頁相同（§5 V-6 以像素比對證明）；ZIP 另放原檔屬 #67。`requirements.txt` 凍結，所以沒有使用 pypdf 等套件。
- **附錄順序**：PDF 原頁只能接在報告最後，所以把 ChatGPT 附錄改為最後一節「附錄 B」，重現資訊改為「附錄 A」；ACCEPTANCE 的對應引用同步更新。章節名稱「GPT 輔助內容」「NotebookLM 摘要」不變（H-2）。
- **摘要的寫法**：每一句以「該報告指出」等方式歸屬於 NotebookLM 報告；只用報告中有明確模型歸屬的數字（§3 表與「內文深度分析」），不採用 §6 綜合摘要中合併不同模型的句子（X-1、X-2）；不寫報告對 Hartono 論文「未載明具體數值」的說法（X-3）。這些是摘要的取捨，不是對材料正確與否的裁定；全部記在對照表與 §7 C-2。
- **機械核對寫進建置**：材料 sha256、摘要漢字數、逐句對照、來源表格式都在 `load_evidence()` 檢查，任一不成立就停止建置，Reviewer 與 #67 重建時都會重做。
- **寫檔方式**：交付物以 Edit／Write 工具或 Python 腳本修改；新增的測試段落先寫在 scratchpad 再以 shell 附加到 `tests/test_report.py`（run record §15 已同意的 workaround 範圍內）。

## 5. Verification

環境：Windows 11、Python 3.11.2（單元 `.venv`）、Node v24.19.0、Chrome 155.0.8059.80；檢查腳本與輸出在 session scratchpad `ex66/`（`tools/`、`mutants66.out`、`final_pages/`、`clean/`）。

| # | 方法 | 結果 |
| --- | --- | --- |
| V-1 | 基準：開工前完整 pytest（base `752791b`） | 348 passed、1 skipped |
| V-2 | 完整 pytest（工作樹＝`d379732`，本機有材料） | **371 passed、1 skipped**（skip＝學號設定未提供），48.0 s；真實材料測試有執行 |
| V-3 | 乾淨副本：`git archive HEAD home_work_02` 解到 scratchpad（只補未追蹤的資料 CSV；沒有 `acceptor_materials/`），以 scratchpad 內新建的 git repo 執行完整 pytest | **370 passed、2 skipped**（學號設定、真實材料）。第一次在非 git 目錄執行時 15 個 hygiene 測試因為沒有 git work tree 而失敗，與本票無關；加 `git init` 後全部通過。同一副本 `python -m hw2.report --no-pdf` 成功並標示三個章節待填、狀態行 draft；`--final` 依設計失敗 |
| V-4 | `node --test tests/js/core.test.js`；`python -m hw2.offline_scan` | 9 pass、0 fail、3 skip；PASS（0 findings） |
| V-5 | 報告建置 `python -m hw2.report --final` | 成功（§4.2）。渲染後逐頁檢視第 25、26、28 頁（10.1／10.2、第十一章、附錄 A／B）的版面與文字 |
| V-6 | 附錄完整性：pypdfium2 以相同倍率渲染最終 PDF 的第 29～149 頁與 `ChatGPT_logs.pdf` 的第 1～121 頁，逐頁比對點陣圖 sha256 | **121 頁全部相同**（`tools/verify_final.py`）。開發中另以 #65 的舊報告 PDF 合併試驗，報告頁與附錄頁 147 頁全部相同（`tools/pixcompare.py`） |
| V-7 | NotebookLM 摘要漢字數：建置程式 `count_hanzi` 與獨立方法（`unicodedata` 名稱為 CJK UNIFIED IDEOGRAPH 的字元） | 兩者都是 **523**（≥ 100；B-15）；11 句全部在對照表 |
| V-8 | 對照表的原文摘錄：腳本把對照表「報告原文依據」欄每個「」引文（以「……」分段）與 docx 全文比對 | 39 段全部逐字出現在 docx（`tools/check_trace_quotes.py`）。第一次比對有 11 段因 Word 在粗體邊界插入空白而不相符，已改為 docx 原樣 |
| V-9 | 人工核對：摘要 11 句逐句對回 docx 的章節與數字（N01～N11）；ChatGPT 用途表的頁碼逐一回看 PDF 頁面；10.1 的 CC-1 例子與 `outcome-contract.md` 第 95 行逐字相同 | 相符 |
| V-10 | 來源網址（`sources.md` 的 7 個；`curl -L`，2026-10-19 15:04 +0800） | #1～#4、#6、#7 HTTP 200；#5 DOI 轉址到 SciTePress `Link.aspx` 後停在 302（同一 DOI 也是 #65 第八章的來源 [3]）。見 C-3 |
| V-11 | Mutation probes（`tools/mutants66.py`；單元的 scratch 複本；只跑 `test_report.py`、`test_pdf_append.py`） | baseline 通過；**22 個 mutant 全部 DETECTED**：漢字計入英文、門檻改 99、對照順序不查、空欄放行、sha256 不查、gpt 章節不需 PDF、狀態恆為 final、句外文字放行、註解不剝除、引用標示全標、附錄頁數核對拿掉、附錄未寫回、字串內參照被改寫、舊根缺 `/Parent`、附錄樹排前面、舊 xref 優先、物件標頭前空白不容忍、版本只取 base、UTF-16 不解碼、接受 xref stream、模板改回 pending、附錄 A 改名。第一輪有 3 個存活：頁數核對（補了 monkeypatch 測試）、字串改寫的 mutant 寫法無效（改為對原位元組做 regex 取代後偵測到）、UTF-16 mutant 的比對字串錯誤（修正後偵測到） |
| V-12 | 凍結範圍 | `git diff 752791b d379732` 沒有 `results/`、`assets/`、`hw2.ipynb`、`requirements.txt`、`doc/requirement/` 與凍結模組；`results/model_data.json` sha256 `fa86d76c…b891e3`、`assets/model_data.js` `37626bf9…5b29a72`（與 #63／#64 相同）；建置仍先核對 `result_digest`＝`b53ff286…c3cfc6`。沒有執行 `hw2.run_notebook` 或任何 notebook cell，沒有開守門 |

- **A-4（S-1）**：沒有建立 `.local/packaging.json`；追蹤樹沒有新增 PDF、ZIP、`.env`、`kaggle`、`acceptor_materials/`、`dist/`（`git status` 與 hygiene 測試）。新增的追蹤內容沒有「學號」；7 位以上的數字串只有：xref 的 `0000000000`、PDF 日期 `20261019095836`、日期 `20261018`、sha256 片段、Unicode 範圍 `00020000`／`00030000`／`0003134`。Commit message 沒有長數字。ChatGPT PDF 中出現作者的實際學號與姓名（PDF 內容與 metadata）：只存在於未追蹤的材料與 `dist/` 的報告 PDF 附錄中，沒有寫進任何追蹤檔案、本 worklog、commit message 或終端指令；`document_info` 的結果在報告中只使用 CreationDate 與 Producer。**實際學號比對 NOT VERIFIED**（學號設定尚未提供；依 S-1）。
- **H-2**：兩個標示字串仍逐字是第十、十一章的標題（`test_report_chapters_labels_and_required_statements`）；摘要依 B-15 計 523 漢字；notebook、`index.html`、`assets/` 沒有改動，離線掃描 PASS。
- **H-4**：ChatGPT 對話內容沒有被改寫成對話或代為產生；附錄是原頁（V-6）；10.1 是用途說明並附頁碼。NotebookLM 摘要沒有加入材料以外的論點、數字或來源（V-8、V-9）；第八章的公開解法沒有改動。
- **Git**：commit message 依 `docs/conventions/git-commit-rules.md`，沒有 Claude 標記；未 push、rebase、merge、force push。

## 6. Audit status

Required（Formal；H-1：材料的接收、存放與報告 PDF；H-2：兩個標示與 ≥100 字；H-4：AI 章節的真實性）。依 A-1 需要 R1 record 的類別核對節；依 A-5 Reviewer 直接讀 `acceptor_materials/` 的原始材料自行比對摘要與 10.1，不只依本檔與對照表，並核對 ChatGPT PDF 的 sha256 與 §2 相同；依 DA `decision-20261018-issue60-a4-student-id.md` §2.2，R1 核對兩個標示字串逐字正確與 B-15 計數。尚未派工（由 Orchestrator 依 Bindings §3.7）。本檔的 self-verification 不是 audit。

## 7. Concerns 與所需 authority

| ID | 內容 | Required authority |
| --- | --- | --- |
| C-1 | **衍生章節不追蹤**（§4.3 第一點）：10.1 與第十一章的文字只在 `acceptor_materials/derived/`。若 Design Authority 認為 NotebookLM 摘要或 ChatGPT 用途說明應進追蹤的模板（例如摘要不算「材料」），只需把文字搬進 `report/report.md`，建置程式不必改 | Design Authority（若需不同處理；目前做法對兩種讀法都成立） |
| C-2 | **材料內部的不一致**（對照表 X-1～X-5）：NotebookLM 報告 §6 的綜合摘要把未正則化的 2 次多項式（R² 0.822、RMSE 151,200.970）與 Ridge α=50,000（R² 0.801、RMSE 159,872.572）合併寫成「正則化模型 0.80~0.82」；單變數 R² 範圍寫法與表不同；對 Hartono 論文寫「來源未載明具體數值」，與報告第八章（#65 依論文原文列出 CatBoost 自報指標）不同；「預測溫度」語意不明；`sources.md` 的 #5～#7 不在該報告的文獻清單。摘要只用有明確歸屬的數字、不寫 X-3 的說法，來源表照原表列出 7 個並標示「報告引用」。沒有裁定哪個說法正確 | Reviewer（A-5 核對）；若需裁定則 Design Authority |
| C-3 | 來源 #5 的 DOI 在 `curl` 下停在 SciTePress 的 302（可能需要瀏覽器 cookie）；沒有改動來源清單 | 無（#67 的人工檢查 D-18 可在瀏覽器確認） |
| C-4 | 10.1 揭露 Brief／Spec／Tickets／OC 中部分作者決定採用了 ChatGPT 的建議或其起草回覆（附例）。這是 Brief §9「如實揭露」的直接結果，內容只出現在報告 PDF；若 acceptor 不希望報告寫到這個程度，屬 acceptor 對自己材料的決定 | Acceptor（只在有異議時） |
| C-5 | 附錄 PDF 原頁的頁尾有 ChatGPT 對話的網址與原頁碼，metadata 有作者姓名；這些都是 acceptor 提供的原件內容，只進報告 PDF 與 ZIP（不進 git） | 無 |

## 8. Remaining work

- #66 R1（Orchestrator 派工）。學號比對 S-2～S-5；push 依 run record 選項 (a)。
- #67：乾淨環境完整重跑（N-3、§9.3 條件 7、8；cell 28 依 DA G-3）後，在有 `acceptor_materials/` 的機器上以 `python -m hw2.report --final` 重建報告 PDF 放入 ZIP，ZIP 另放 `ChatGPT_logs.pdf` 原檔；ACCEPTANCE A-6、D-13、D-16、D-17 的人工驗收。
- **Scratchpad 產物**（不在 repo）：`ex66/`——`pages/`、`pairs/`（ChatGPT PDF 的頁面渲染）、`nlm_v2_paragraphs.txt`、`tools/`（`pixcompare.py`、`verify_final.py`、`check_trace_quotes.py`、`fix_trace_quotes.py`、`mutants66.py`）、`mutants66.out`、`final_pages/`、`final_build.json`、`clean/`、`b1/`、`trymerge.pdf`。

## 9. 執行時間量測（Q34）

- 工作時間：2026-10-19 約 14:40 至 15:20 +0800。
- 閱讀 ChatGPT PDF（121 頁影像）與 NotebookLM 報告是最耗時的部分。報告建置（含截圖、列印與附錄合併）約 11 s；附錄合併本身約 0.2 s；完整 pytest 約 48 s；22 個 mutation probes 約 72 s。
