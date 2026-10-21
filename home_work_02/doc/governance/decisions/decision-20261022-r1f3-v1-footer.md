# Decision record — R1-F3：探索模式下的 V1 頁尾（`home_work_02/`，HW2 V2 Enhance）

- **紀錄類型**：Design Authority decision record（治理 §2.4、§4.2、§5.3 第 2 類；Bindings b5 §7）。
- **日期**：2026-10-22
- **Run**：`run-20261022-hw2-v2-enhance`（Orchestrator＝root session `37216426-f292-44f9-bad1-e2d862e7b8f1`）
- **來源**：#74 R1 audit record [`../audit/issue-74-c1-r1.md`](../audit/issue-74-c1-r1.md) finding **R1-F3**（Low，non-blocking；契約語義不足，依治理 §4.2 是 routing signal）；record §7、§8 指定 authority＝Design Authority；run record §9 依治理 §2.4 直接派工。
- **Outcome Contract**：[`../outcome-contract.md`](../outcome-contract.md) §5（V2，接受基準 `d7f02d4179d2cb5c2ecf0c39a4643a6ef8287907`）與 §5.2 CC-V2-1；§1–§4（V1）仍有效。
- **相關紀錄**：[`derivation-SPEC-V2.md`](derivation-SPEC-V2.md)（B-1、B-14、D-1、D-2、H-4、H-5、I-5）；run record [`../run/run-20261022-hw2-v2-enhance.md`](../run/run-20261022-hw2-v2-enhance.md) §1 第 4 點。
- **受審 subject 的狀態**：branch `home_work_02-v2-enhance`，撰寫時 HEAD `9e99a10`（R1-F1 的 targeted correction，只改 ACCEPTANCE）；`index.html`、`assets/explore_ui.js`、`assets/explore.css`、`tests/test_explore_static.py` 與 R1 的 subject `f4e487c` 相同。
- **Binding**：`gov-design-authority`，有效 mapping `claude-opus-5-5`／`high`（Bindings §3.1 預設；沒有 escalation、沒有替代）。Binding 的核對由派工者依 Bindings §3.6 執行；本紀錄不自證 binding。
- **Capability escalation**：不提出。E-DA/D1 不成立：兩種讀法（頁尾屬 V1 區塊／屬頁面外框）可以用接受基準的原文與 repo 事實裁決（第 3 節理由）。E-DA/D2 不成立：我先前對本問題沒有決定，`derivation-SPEC-V2.md` 沒有被 FA ruling 或 Reviewer finding 推翻。
- **獨立性**：R1-F3 的敘述、Executor worklog 的 D-9（「V1 的 header、區塊與 footer 不改」）與 `test_explore_static.py` 的 docstring 都只當作主張；第 6 節是我自己取得的證據。

## 1. 問題

`index.html` 的 V1 頁尾（`<footer class="footer small muted">`，與 `d7f02d4` 逐字相同）寫：「本頁讀取主程式 `hw2.ipynb` 匯出的 `model_data`；所有資料與程式庫都在本機，不發出任何對外請求。圖表程式庫：…」。#74 的實作在探索模式只隱藏五個 V1 section（`explore_ui.js` 的 `V1_BLOCKS`）與 `#load-error`，另以 `body.is-exploring` 隱藏 V1 頁內導覽；頁尾在 50 Startups 與自訂資料集兩種模式下仍顯示。

#76 加入「使用者提交 URL 後對該 URL 一次 GET」之後，自訂 URL 模式下「不發出任何對外請求」不再屬實；探索模式下「本頁讀取 … `model_data`」也不是探索區塊的資料來源（探索程式不讀 `model_data`，derivation B-9、A-3）。另一方面，V1 區塊文字不變的不變量（run designation 第 4 點、票的共同條款、Spec V2「V1 區塊的 DOM、文字 … 不變」、`tests/test_explore_static.py` 的快照）鎖定頁尾文字。Spec V2「選 50 Startups 或自訂資料集：隱藏 V1 區塊」沒有說頁尾是否屬於 V1 區塊。

要裁決的是：(1) 頁尾在探索模式如何處理；(2) 頁尾文字可否改變。

## 2. 依據

| 來源 | 內容 | 用途 |
| --- | --- | --- |
| Brief V2 §4（accepted） | 「選 King County 時，頁面就是 V1 的 dashboard：既有區塊的內容與數字逐字相同」；「選 50 Startups 或自訂資料集時，頁面呈現 Exploratory run 的區塊」 | King County 檢視的頁尾逐字保留；探索模式呈現的是探索區塊 |
| Brief V2 §3.5 覆寫 2（accepted） | V1 §7「頁面不發出任何對外網路請求」與 §10 改為 §5.6 的隔離四條 | 覆寫的對象是 V1 Brief 的**需求條款**，不是 V1 dashboard 上的顯示文字；它沒有授權改寫任何 V1 區塊的文字 |
| Brief V2 §5.6 第 1、2 條 | 頁面載入與 King County、50 Startups 的所有操作零對外請求；唯一允許的是自訂模式提交 URL 後的一次讀取 | 頁尾陳述在哪些檢視下屬實 |
| Brief V2 §8 第 1 條 | 選 King County 時既有區塊的內容與數字逐字相同 | 同上 |
| Spec V2「Problem 與頁面結構」第 94–95、98 行 | 選 King County 顯示 V1 的全部區塊；選探索 problem「隱藏 V1 區塊，顯示探索區塊」；「頁面標題與品牌列保留 V1 文字」 | 探索模式下保留可見的 V1 元素只點名標題與品牌列 |
| Spec V2「範圍與不變量」第 88 行；票共同條款；run designation 第 4 點 | V1 dashboard 區塊的 DOM（結構與文字）／行為不變 | 文字鎖定 |
| derivation H-4（V2） | 證據真實性與如實標示，含頁面與 README 的陳述 | 頁面不得在其顯示的檢視下呈現不屬實的陳述 |
| derivation B-9、A-3（V2） | 探索程式完全不讀 `model_data` | 頁尾的資料來源陳述只描述 King County 檢視 |
| Repo 事實 | `d7f02d4:home_work_02/index.html` 第 274–276 行即此頁尾；`tests/test_explore_static.py` 第 98–111 行把 `footer` 列入 `V1_SELECTORS` 並以 `d7f02d4` 的快照鎖定；`assets/explore.css` 第 15 行以 `body.is-exploring` 隱藏 `.topnav`、`.nav-toggle`（V1 元素，未改其 DOM） | 頁尾是基準頁面上的 V1 內容；探索時隱藏 V1 元素而不改其 DOM 的作法已存在 |

## 3. 裁決

### R3-1 頁尾是 V1 區塊

頁尾屬於 Spec V2 所說的「V1 區塊」，同時適用「選 King County：顯示」「選探索 problem：隱藏」與「DOM、文字不變」三條。

理由：
1. 它是接受基準 `d7f02d4` 的 V1 dashboard 既有內容，內容是 King County 正式分析的資料來源與離線陳述（`model_data`、`hw2.ipynb`），不是與 problem 無關的頁面外框。
2. Spec V2 在探索模式下保留 V1 文字的元素只點名「頁面標題與品牌列」（第 98 行）；頁尾不在其中。
3. 另一種讀法（頁尾是外框、探索時照常顯示）會讓頁面在自訂 URL 模式顯示不屬實的「不發出任何對外請求」，在兩種探索模式顯示不適用的「讀取 `model_data`」，與 Brief V2 §5.6 和 H-4 衝突。在兩種讀法中只有本讀法同時滿足全部 accepted 文字，所以這不是 E-DA/D1 的情形。
4. 本讀法與 Executor 自己的快照測試一致（`footer` 已列為 V1 區塊），測試不需修改。

### R3-2 探索模式隱藏頁尾

- 選 **50 Startups** 或 **自訂資料集**（含提交前、載入失敗後、執行完成後、取消後）：頁尾隱藏。
- 選 **King County**（含從探索模式切回）：頁尾照 V1 顯示，與切換前相同，包括 `assets/app.js` 在執行期寫入的 `#chartjs-version` 文字。
- 這是 Spec V2 第 95 行對 V1 區塊既有要求的適用，不是新行為；它和五個 V1 section、頁內導覽在探索時的處理一致。

### R3-3 頁尾文字不得改變

頁尾的靜態 DOM 與文字逐字不變。Brief V2 §3.5 覆寫 2 改的是 V1 Brief 的網路需求，不是 V1 dashboard 的顯示文字；沒有任何 accepted 文字授權改寫 V1 區塊文字，而 Brief V2 §4、§8 第 1 條與 designation 第 4 點明確要求逐字相同。改寫頁尾（包括只在 King County 檢視改寫、以 V2 程式在執行期替換其文字或加註）會改變 accepted 的 V1 區塊不變量，屬治理 §5.3 第 1 類，須 acceptor 核准。本裁決**不**採用、也**不**建議這條路：R3-2 已消除不屬實的顯示，不需要改字。

### R3-4 King County 檢視中的頁尾陳述

頁尾只在 King County 檢視顯示。依 Brief V2 §4，此時「頁面就是 V1 的 dashboard」；依 §5.6 第 1 條，頁面載入與 King County 的所有操作零對外請求。所以頁尾的陳述讀作對其所在的 King County 檢視的描述，在 V2 下仍然屬實，包括同一工作階段先前在自訂模式提交過 URL 再切回的情形（那一次讀取屬自訂模式，不是 King County 檢視發出的）。Acceptor 同時接受了「King County 檢視逐字保留 V1 區塊」與覆寫 2，這是已接受的結果，不是需要 acceptor 另行決定的缺口。

### R3-5 實作約束與分配

| 項目 | 內容 |
| --- | --- |
| 分配 | **#76**（V2-T3：自訂資料集與 URL 請求、切換 AC「V1 區塊始終不變」都在這張票；它本來就修改 `explore_ui.js` 的切換程式）。須在 #76 結案前完成。不併入 #74 的 R1-F1 targeted correction（R1 已限定該修正的 diff 範圍；治理 §4.4），也不重開 #74：R1 已把 R1-F3 列為 non-blocking routing signal，在 #74 的 operating scope 內頁尾陳述仍屬實 |
| 必須不變 | `index.html` 中頁尾元素的靜態 DOM 與文字；`assets/style.css`、`assets/app.js`（A-3 與快照的 sha256 鎖定）；`tests/test_explore_static.py` 的快照與 `V1_SELECTORS`；其他既有測試（I-5） |
| 隱藏的方式 | HOW，由 Executor 決定，但只能在 V2 檔案中實現（例如與五個 section 相同的 `hidden` 屬性切換，或 `assets/explore.css` 中以 `body.is-exploring` 為前提的規則，與既有的導覽處理相同）；切回 King County 必須還原原狀 |
| 不要求的事 | 本裁決不要求在探索區塊新增任何取代頁尾的說明文字。Executor 若在探索子樹加入關於請求的說明，屬 V2 UI 的範圍，內容必須符合 §5.6 與 D-1（自訂 URL：提交後一次 GET；其他操作零請求），並遵守 D-2 |
| 驗證 | #76 既有的「切換（人工檢查表）」AC 已涵蓋「V1 區塊始終不變」，頁尾是 V1 區塊，所以同一檢查須記錄：兩種探索模式下頁尾不顯示、切回 King County 後頁尾與切換前相同。#76 R1（H-2、H-4、H-5）在瀏覽器核對；Spec Integration Audit 對整合 subject 再核對。是否另加靜態或 Node 斷言由 Executor 決定，不是新 AC、不是新 seam |

### R3-6 相關分配：README 的頁面層級陳述（#78）

同一個問題也出現在不受 V1 文字不變量約束的 README。撰寫時 `README.md` 第 20 行「頁面不發出任何對外請求」、第 59 行「完全離線：`file://` 開啟、零對外請求」、第 21 行「Dashboard 只讀取匯出的結果」以整個頁面為主詞；#76 之後它們不再完全屬實。README 是 V2 要求更新的交付物（Brief V2 §7；Spec V2「文件、README」），不屬凍結的 V1 產物。分配給 **#78**：README 的這些陳述須依 Brief V2 §3.5 覆寫 2 與 §5.6 重寫（King County、50 Startups 與本機檔案載入零對外請求；自訂 URL 在提交後對該 URL 一次 GET），由 #78 R1 依 H-4、A-5 核對。這是對既有 accepted 內容的分配，不是新 AC。

觀察（不裁決）：`report/report.md` 第 238 行「Dashboard 的任何操作都只讀取匯出的結果」在正式分析章節內，描述的是 King County dashboard。它是否需要在 #78 註明範圍，由 #78 依 I-4 與「正式分析各章數字不變」處理；若 Executor 或 Reviewer 認為需要修改正式章節的文字而無法確定是否在 boundary 內，route 至 Design Authority。

## 4. 是否改變 accepted 語義

**否。** 
- R3-1 是依 accepted 原文（Brief V2 §4、Spec V2 第 94–98 行、designation 第 4 點）對「V1 區塊」的解讀，兩種讀法中只有它與全部 accepted 文字相容。
- R3-2 是 Spec V2 對 V1 區塊既有要求的適用。
- R3-3 維持 accepted 的文字不變量。
- R3-4 是 accepted 結果的說明。
- R3-5、R3-6 是分配，不新增 AC、seam、gate 或 scope。

本紀錄屬治理 §5.3 第 2 類，不需 acceptor 核准。會改變 accepted 語義、因而須 acceptor 的只有 R3-3 所述的改字路徑；本裁決不走該路徑。沒有無法確立在 boundary 內的事項，不需 fail-closed。

## 5. 受影響的 work items 與 evidence

| 對象 | 影響 |
| --- | --- |
| **#76** | 新增義務 R3-5（在探索模式隱藏 V1 頁尾，切回 King County 還原；頁尾 DOM／文字不變）。排入 #76 的派工 pack，#76 R1 核對 |
| **#78** | 義務 R3-6（README 頁面層級的網路與資料來源陳述依 §5.6 重寫）；report 第 238 行為觀察 |
| **#74** | 不重開，不影響 R1-F1 的 R2 範圍與 #74 結案。#74 的截圖 `chrome_startups50_1280_full.png`、`chrome_custom_1280.png` 底部可見頁尾，是 #74 subject 的如實證據，不需重拍；#76 之後的行為以 #76 的證據為準 |
| #75、#77 | 無影響（#77 若修改切換或取消流程，須保持 R3-2 的行為） |
| `tests/test_explore_static.py`、快照 | 不變；本裁決與其 `V1_SELECTORS` 一致 |
| Spec Integration Audit（Spec V2） | 核對整合 subject 上 R3-2、R3-3、R3-6 成立 |
| Outcome Contract、Brief、Spec、tickets、GitHub issues | 不修改 |

## 6. Evidence

- 讀取：治理 v2.2 §1.2、§2.4、§4.2、§5.3；Bindings b5 §7（命名）；`outcome-contract.md` §5、§5.1、§5.2；`BRIEF-V2.md` §3.5、§4、§5.6、§7、§8；`SPEC-V2.md`（全文，特別是第 85–98、211–216、265 行）；`derivation-SPEC-V2.md`（全文）；run record（全文）；`audit/issue-74-c1-r1.md` §6 R1-F1～R1-F3、§7、§8；`gh issue view 76`（body sha256 `5d121dd9…b2b2`，與 derivation §3 記錄的 accepted 版本相同）、`gh issue view 74` 的相關段落。
- 檔案：`index.html` 第 375–377 行（頁尾）與 `git show d7f02d4:home_work_02/index.html` 第 274–276 行（逐字相同）；`assets/explore_ui.js` 第 1–60 行（`V1_BLOCKS`、`setExploring`）；`assets/explore.css` 第 1–15 行（`body.is-exploring` 隱藏導覽）；`tests/test_explore_static.py` 第 1–200 行（`V1_SELECTORS` 含 `footer`、快照測試）；`assets/app.js` 第 1015 行（`#chartjs-version` 的執行期寫入）；`assets/style.css` 第 96 行；`README.md` 第 15–25、55–62 行；`report/report.md` 第 238 行；`doc/governance/worklog/issue-74.md` D-9；`doc/ticket/tickets-v2.md` 第 28 行。
- `git log --oneline -3`（HEAD `9e99a10`）；`git status --short`。
- 寫入的檔案只有本紀錄；沒有修改契約、Spec、票、程式、測試或其他紀錄；沒有 commit。
