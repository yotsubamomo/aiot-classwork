# Worklog — README 更新（單元與 root）與重新打包 ZIP（Lightweight）

| 欄位 | 內容 |
| --- | --- |
| Work item | `20261019-readme-zip-refresh`：單元 `README.md` 補 R1 F-2、root `README.md` 的 HW2 相關更新、重新打包繳交 ZIP |
| Lane | Lightweight（Bindings §4「已結案工作之後的單點修正」；以 acceptor 的直接指示作為 Outcome Contract）。不是 Formal run `run-20261018-hw2-formal` 的一部分 |
| 日期 | 2026-10-19 |
| Branch | `home_work_02-readme-zip-refresh`，自 `main` `cf7f9098bb7268c661abb9b630202ed10f1ce559` 建立。只在本機 commit，未 push |
| 狀態 | 實作、重新打包與 self-verification 完成；independent audit 依 acceptor 2026-10-19 明確指示未執行（見 §8） |

## 1. Contract reference

- **Outcome Contract（Lightweight，Bindings §2.3）**：acceptor 2026-10-19 的直接指示，原文：
  > 更新README, 包含root 的，然後重新打包ZIP 但是不用觸發audit ，因為只是調整這些而已。然後做完後發pr , push , merge
- **acceptor 對範圍的選擇**（2026-10-19，在對話中以選項回答，由派工者轉達）：
  - 「單元 README 補 F-2」：在「作業要求對應」表補上老師要求「網路上主流或更優解法之比較與說明」，指向報告 §8（`doc/governance/audit/20261019-readme-restructure-c1-r1.md` F-2），標示依老師原文＝〔老師要求〕。
  - 「root 目錄樹加 home_work_02」。
  - 「root 補 week06 以外的其他項」：沒有附具體內容。派工者的界定：只檢查 root `README.md` 中與 HW2 有關、過時或缺漏之處，做最小、事實性的更新；不改 week02／week06／home_work_01 的既有描述；root `README.md` 的修改是 acceptor 在本指示中授權的 RB-5 變更，其他 root 檔案不得修改。
  - Audit：「照你說的不做 audit」。
- **有約束力的 DA 裁決**：`doc/governance/decisions/decision-20261019-post-merge-ad3-readme.md` §3.3 D-R2（README 不得含 `學號設定`、`packaging.json`、`student_id`、`.local/`；三種標示；數字單一來源 RT-5）；`decision-20261018-high-risk-categories.md`（H-1、H-2）。
- **派工指示的範圍**：README 修改先 commit，再以 `python -m hw2.package` 重新打包到未追蹤的 `dist/`；不得重跑 notebook 或任何正式 Test 評估；不得列出 `dist/` 或印出含學號的檔名／路徑；不得 push、開 PR 或 merge（由派工者核對後執行）。
- **上位契約**：`doc/requirement/HW2-requirements-Multiple Linear regression.txt`「5. 繳交內容」的報告內容第 4 項「網路上主流或更優解法之比較與說明」。

## 2. Executing role and binding reference

- **角色**：Executor（`gov-executor` subagent，由主 session 派工；definition `.claude/agents/gov-executor.md`）。
- **Binding**（Bindings §3.6）：session `4bbff425-7ff9-4cdc-b64c-cc68e824e1b1`，agentId **`a24b4c2fd424351fc`**（`meta.json` 的 `agentType`＝`gov-executor`；以 mtime 判定為本次派工的最新一筆），在重新打包之後、寫本 worklog 前觀測 `('claude-opus-5-5', 'high')` 73 則，全程單一元素，等於 O-1 mapping。全程核對（含之後的訊息）由派工者在採用 return 前執行。
- **Escalation／替代**：無。**Bounded assignments**：未使用。

## 3. Work performed

| Commit | 內容 |
| --- | --- |
| `af11736199247b3d7ba87ba57179b11a80ca7b67` | `home_work_02/README.md`：「作業要求對應」表新增一列（見 §4.1）。Root `README.md`：目錄樹加 `home_work_02/`；修正 requirement PDF 的說明句（見 §4.2） |
| （本 worklog 的 commit） | 本檔 |

重新打包：在 `af11736` 的乾淨工作樹（打包路徑沒有未 commit 的修改）執行 `home_work_02/.venv/Scripts/python -m hw2.package`，exit 0，stderr 空。stdout 存在 scratchpad，先以程式確認不含實際學號（計數 0）再讀取。

## 4. Decisions and assumptions

### 4.1 單元 README（F-2）

- 新增列位於「繳交內容」列之後、「（optional）」列之前，順序與老師原文相同（報告內容列在「5. 繳交內容」之下）。
- 左欄依原文寫「報告內容：網路上主流或更優解法之比較與說明」；右欄以〔老師要求〕開頭，與報告第 8 章標題「主流或更優解法比較 〔老師要求〕」的標示相同（`report/report.md:277`），指向報告第 8 章，並連到 `report/external_sources.json`（README 檔案配置表已描述它是此章的來源檔）。
- 右欄沒有寫任何數字（RT-5：「成果」以外不陳述 Test 結果值）；「第 8 章」的 8 不屬於受檢的 Test 值。
- 評分的「資料集來源與研究脈絡」（F-2 證據第 3 點）沒有另加一列：F-2 本身記錄它已併入第 1 列，acceptor 的選擇只涵蓋「主流或更優解法」這一項。

### 4.2 Root README

| 位置 | 改動 | 理由 |
| --- | --- | --- |
| 目錄樹 | `home_work_01/` 改為 `├──`，新增 `└── home_work_02/    # 作業 2` | acceptor 選項「root 目錄樹加 home_work_02」；`home_work_02/` 已在 `main`，且「作業」表已有它的列，目錄樹缺漏 |
| 「作業」表之後的說明句 | 「其中的 PDF 未納入版本控制」改為「其中作業說明的 PDF 未納入版本控制；`home_work_02/` 另追蹤一份老師範例網站的列印 PDF」 | HW2 加入後原句與事實不符：`home_work_02/doc/requirement/50 Startups_ Multiple Linear Regression & Feature Selection Explorer.pdf` 有被追蹤（`git ls-files`；`home_work_02/.gitignore:5` 的 `!/doc/requirement/*.pdf`），Brief SRC-3 的描述是「老師 DIC-2 網站列印」。作業說明的 PDF 都未追蹤：`home_work_01/` 的 `Part_5…pdf`（root `.gitignore:4`）與 `home_work_02/` 的 `HW2-requirements-Multiple Linear regression.pdf`（`home_work_02/.gitignore:9`），由 `git check-ignore -v` 確認。只改這一句，沒有改各單元的描述 |
| 「作業」表的 HW2 列 | 不改 | 已存在，且連結（`./home_work_02/`、Pages URL）正確 |
| 「GitHub Pages」一節 | 不改 | 第一句是通則（需要瀏覽器展示的單元從 `main` 根目錄發布，網址 `…/<目錄名稱>/`），已涵蓋 `home_work_02/`；HW2 的 Pages URL 已在「作業」表；`home_work_01/` 被點名只因為它是例外。加一句只會重複通則。`https://yotsubamomo.github.io/aiot-classwork/home_work_02/` 回應 HTTP 200（`curl`，2026-10-19） |
| 其他段落 | 不改 | 開頭兩段、「目錄組織」與「課堂實作」表與 HW2 無關或仍正確 |

沒有修改其他 root 檔案（`CONTEXT-MAP.md`、`CLAUDE.md`、`AGENTS.md`、`docs/`、`.claude/`）。`git diff main --stat`：只有 `README.md`、`home_work_02/README.md`（加上本 worklog）。

### 4.3 重新打包

- 依 `hw2/package.py` 的既有流程；沒有重跑 notebook，沒有任何 Test 評估。打包程式只讀追蹤的 notebook 與匯出結果，並以 `report.check_formal_evaluation` 核對匯出的 Test 結果就是唯一一次正式評估（result digest `b53ff286ae0734add8b272089aba904a1cb7f5aca444a62d356420b25dc3cfc6`，與 README 與 `worklog/issue-63.md` §5 相同）。
- 打包的步驟 4 會重新建置報告 PDF（`report.build(final=True)`）。這不是 README 造成的改變，而是 `hw2.package` 的固定流程，所以報告 PDF 的位元組必然不同（見 §6.3 與 §8 Concerns 1）。

## 5. 舊 ZIP（被覆蓋前）

- `dist/<學號>_hw2.zip`：sha256 **`c84a3c5e6d295ed383fc8c085eb68f30aaa9035208cf9ca7eeaa0d9aae763fb6`**，81,432,807 bytes，56 個項目（等於 run record §19／`worklog/issue-67.md` §5 記錄的值）。
- 覆蓋前另以中性檔名複製到 session scratchpad 供比對（不在 repo 內）。

## 6. Verification

### 6.1 測試（subject：`af11736` 的工作樹；`.local/packaging.json` 存在）

- 完整 pytest：`home_work_02/.venv/Scripts/python -m pytest -q -rs` → **398 passed**，沒有 skip。
- 學號比對實際執行：`tests/test_repo_hygiene.py::test_no_tracked_file_contains_the_student_id` **PASSED**（不是 skip）；`test_read_student_id_rejects_missing_and_placeholder` PASSED。
- README 測試 7 個全部 PASSED：`test_readme_has_every_required_item`、`test_readme_does_not_record_the_student_id_setting`、`test_readme_submission_file_names_use_only_the_placeholder`、`test_readme_has_no_digit_run_after_the_word_student_id`、`test_readme_states_the_one_formal_evaluation_and_reruns_as_reproduction`、`test_readme_results_numbers_equal_the_exports`、`test_readme_does_not_present_the_method_comparison_as_a_requirement`。
- 學號計數（只印計數；從 `.local/packaging.json` 讀實際值，在程式內比對）：root `README.md` 0、`home_work_02/README.md` 0、README diff 0；整個 repo 的追蹤檔案（1,469 個）中含實際值的 0 個。單元 README 中 `學號設定`、`packaging.json`、`student_id`、`.local/` 的出現次數都是 0（另由上面的 README 測試強制）。
- Root README 的路徑與連結：`week02/`、`week06/`、`home_work_01/`、`home_work_02/` 都存在；單元 README 新增的連結 `report/external_sources.json` 存在且被追蹤；root 說明句提到的追蹤 PDF 被追蹤、兩份作業說明 PDF 被忽略（`git check-ignore -v`）。
- Release gate（Bindings §5）：README 的安裝與執行步驟沒有改動（沒有新增或修改指令），不需重跑；`git ls-files` 不含 `.env`；diff 內沒有金鑰字串。

### 6.2 新 ZIP

- `hw2.package` 的摘要：ZIP sha256 **`c76272b39373622162f252163c76bb8ba88c76d0abf9ce836f4c6b759b88a146`**，81,435,487 bytes，**56 個項目**，頂層資料夾 `<學號>_hw2/`，打包自 commit `af11736199247b3d7ba87ba57179b11a80ca7b67`；`dist/<學號>_hw2.ipynb` sha256 `2e2f8afc1f67fd51312b894d3a3f4873049defead185b1dd4ca2ab1ace04ff64`（與舊版相同）。打包程式自己的讀回核對（每個項目的 sha256＝來源）通過。
- 獨立核對（scratchpad 的程式，不使用 `hw2.package`；在記憶體中讀 ZIP，輸出前把實際值換成佔位，並確認輸出檔不含實際值）：
  - 只有一個 `*_hw2.zip`；sha256 與 `hw2.package` 的摘要相同。
  - 項目名稱與順序和舊 ZIP 完全相同（56 個）。
  - 與舊 ZIP 內容不同的項目只有兩個：`<學號>_hw2/README.md` 與 `<學號>_hw2/hw2_report.pdf`。其他 54 個項目（含 notebook、ChatGPT PDF、`hw2/`、`results/`、`assets/`、`index.html`、資料 CSV、`requirements.txt`）的 sha256 與舊 ZIP 相同。
  - ZIP 內的 `README.md` 等於工作樹的 `home_work_02/README.md`（位元組相同）；把 CRLF 換成 LF 後等於 `af11736` 的 blob（工作樹是 CRLF checkout，202 行）。舊 ZIP 的 README 以同樣方式等於 `e2f391a` 的 blob，所以 EOL 處理與前一版相同。
  - 打包範圍內的追蹤路徑，`e2f391a`（舊 ZIP 的打包 commit）到 `main` 之間只有 `README.md` 有差異（`git diff --stat`），與上面的結果一致。
- `dist/` 中其他改變的檔案：`hw2_package_manifest.json`、`report/hw2_report.pdf`、`report/shots/test.png`；`report/hw2_report.md`、`.html` 與 notebook 複本沒有改變。

### 6.3 報告 PDF（舊 sha256 `8778b459005efda573f4028ef47417d936b24b8ba7b24edc7aaf7979556fbbfe` → 新 `e3ced571834c16759c1237b3104d00a9d8f87302cac9a6d61560dc688469d3c0`）

以 pypdfium2 比較兩份 PDF（只讀 ZIP 內容，不輸出檔名）：

- 頁數 149／149（報告 28 頁＋附錄 121 頁），與舊版相同。
- **149 頁的文字層全部相同**。
- 以相同倍率渲染逐頁比對點陣圖：只有第 24 頁不同。差異範圍是一行（2 倍渲染時 x 182–556、y 1035–1046），我把兩版的該區域裁切出來目視：是報告內 dashboard 截圖的量測說明，舊版「繪製：248 ms……最近一次互動（method）：12.3 ms」，新版「254 ms……13.2 ms」。這是建置時擷取 dashboard 當下的量測（README 截圖說明與報告都已說明這是擷取當下的量測），不是結果數字。
- Metadata 只有 CreationDate／ModDate 不同（Chrome 每次列印都不同，`worklog/issue-66.md` 已記錄這個行為）；Title、Creator、Producer 相同。
- 第 29～149 頁（ChatGPT 附錄，含作者個資）沒有開啟檢視，只做了文字與點陣圖的雜湊比對，全部相同。

### 6.4 未執行

- Node 測試、`hw2.offline_scan`：dashboard 與 `hw2/` 沒有改動；pytest 內的 Node 一致性測試已執行。
- 在 GitHub 上檢視 README 的呈現：branch 未 push。

## 7. Artifacts

- 追蹤：`README.md`（root）、`home_work_02/README.md`、本 worklog。
- 未追蹤：`home_work_02/dist/<學號>_hw2.zip`（sha256 `c76272b3…a146`）、`dist/<學號>_hw2.ipynb`、`dist/hw2_package_manifest.json`、`dist/report/`。
- 核對程式與輸出在 session scratchpad（不進 git）：`zipcheck/snap.py`、`zipcheck/cmp_pdf.py`、`before.json`、`after.json`、`cmp_out.txt`、`package_stdout.json`。

## 8. Audit status、concerns 與 remaining work

- **Audit**：依 acceptor 2026-10-19 明確指示未執行 independent audit（本變更依 DA 高風險表屬 H-1／H-2：README 與 ZIP 內容）。這不是 audit PASS；本檔的 self-verification 不是 audit。
- **Concerns**：
  1. 派工指示預期「報告 PDF 不變」，但 `hw2.package` 每次都重新建置報告，所以 PDF 的 sha256 必然改變。內容層面的差異只有第 24 頁 dashboard 截圖中的量測時間（248→254 ms、12.3→13.2 ms）與 PDF 建立時間；文字層 149 頁全同，附錄全同。依既有流程，這無法避免；如果要求 PDF 位元組相同，需要另改打包流程，不在本 work item 範圍。
  2. 「GitHub Pages」一節依 §4.2 判斷不改；如果 acceptor 希望明列 `home_work_02/`，可以另行指示。
  3. ZIP 不含 `doc/`，所以 ZIP 內 README 的 dashboard 截圖（`doc/screenshots/`）會缺圖；這是 `20261019-readme-restructure` worklog 已記錄的既有限制，本次沒有改變打包範圍。
  4. 依 Bindings 第 5 節，本 work item 沒有 SA-3 opt-in，也沒有 independent review，合併屬 RB-1。acceptor 的指示包含「發pr , push , merge」，由派工者依其 authority 處理。
- **Remaining work**（派工者／acceptor）：push（SA-1）、開 PR（SA-2）、合併（RB-1，acceptor 的指示）；合併後如需要，核對 Pages 部署。iLearning 繳交（RB-2）由 acceptor 進行，繳交檔是新 ZIP（sha256 `c76272b3…a146`）。
