# Decision record — SIA-F1：報告前面各章的「課堂口頭」標示與 SRC-4（`home_work_02/`，HW2 V2 Enhance）

- **紀錄類型**：Design Authority decision record（治理 §1.2 allocation、§2.4、§3.8、§4.2、§4.7、§5.3 第 2 類；Bindings b5 §7）。
- **日期**：2026-10-22
- **Run**：`run-20261022-hw2-v2-enhance`（Orchestrator＝root session `37216426-f292-44f9-bad1-e2d862e7b8f1`；run record 第 23 列）
- **來源**：Spec V2 的 Spec Integration Audit record [`../audit/spec-SPEC-V2-c1-r1.md`](../audit/spec-SPEC-V2-c1-r1.md)（cycle 1、R1，`VERDICT: CLOSURE`，committed at `3750de4`）finding **SIA-F1**（Low、non-blocking，Reviewer 判定為 material，§8／§9 指定 authority＝Design Authority）；前身是 #78 R1 F1（[`../audit/issue-78-c1-r1.md`](../audit/issue-78-c1-r1.md) §7、§8）。
- **Outcome Contract**：[`../outcome-contract.md`](../outcome-contract.md) §5（V2，接受基準 `d7f02d4179d2cb5c2ecf0c39a4643a6ef8287907`）、§5.1、§5.2 CC-V2-1；§1–§4（V1）仍有效。
- **相關紀錄**：[`derivation-SPEC-V2.md`](derivation-SPEC-V2.md)（B-1、B-8、B-10、§5、§7.2 H-2／H-4、I-4、I-5）；[`decision-20261022-r1f3-v1-footer.md`](decision-20261022-r1f3-v1-footer.md)（R3-3、R3-6：凍結的 V1 文字與可更新的 V2 交付物之間的同型先例）；[`decision-20261022-issue75-lasso-early-stop.md`](decision-20261022-issue75-lasso-early-stop.md) R4-5；[`decision-20261018-high-risk-categories.md`](decision-20261018-high-risk-categories.md)（V1 H-2、H-4）；run record [`../run/run-20261022-hw2-v2-enhance.md`](../run/run-20261022-hw2-v2-enhance.md)。
- **受審 subject 的狀態**：branch `home_work_02-v2-enhance`，撰寫時 HEAD `3750de4`；`report/report.md`、`README.md`、`tests/` 與 SIA 的 subject `3745e9c` 相同（之後只有 record-only commits）。
- **Binding**：`gov-design-authority`，有效 mapping `claude-opus-5-5`／`high`（Bindings §3.1 預設；沒有 escalation、沒有替代）。撰寫時我自行讀取本 assignment 的 transcript（agentId `a67436700d54c6ca4`，`agentType` `gov-design-authority`）：`('claude-opus-5-5', 'high')` 52 則，單一元素。全程核對由派工者依 Bindings §3.6 執行；本紀錄不自證 binding。
- **Capability escalation**：不提出。E-DA/D1 不成立：「第 12 章需要／不需要說明」兩種處理的後果不同，但可以用 accepted 原文（Brief V2 §2、§3.5 覆寫 1 與 4、§7；Spec V2 報告一節）、H-4 與 R3-6 先例裁決（第 3 節）。E-DA/D2 不成立：我先前沒有對本問題作出決定（R3-6 對報告只留觀察）；B-8 沒有被 FA ruling 或 Reviewer finding 推翻，SIA §2.3 H-2 還引用它為已裁決事項，本裁決也不改變 B-8（第 3 節 S1-3）。
- **獨立性**：SIA record、#78 R1 record、Executor worklog 與派工內容的敘述都只當作待驗證主張；第 7 節是我自己取得的證據。

## 1. 問題

`report/report.md` 的前言、標示對照表、§7.1 與第九章仍以 V1 的事實標示 dashboard：

- 第 9 行：「唯一的例外是互動 dashboard：它是老師的**課堂口頭要求**，作業頁與講義文字都沒有要求網站」；
- 第 28 行（對照表）：「互動 dashboard｜老師要求（課堂口頭；作業頁正文沒有）」；
- 第 236 行 §7.1、第 294 行第九章的標題：〔老師要求（課堂口頭）〕。

V2 的正式需求 SRC-4（`doc/requirement/HW2-req_new-20261021.txt`）寫「主要繳交:   跟 DIC2 一樣github and web」，Brief V2 §3.5 覆寫 1 據此把 dashboard 與 repository 改為主要交付。這些凍結的正式文字受 #78 AC「正式分析各章內容與數字不變（與上一版報告逐章比對，只有新章節與日期不同）」與 I-5（`tests/test_report.py` 鎖定「老師要求（課堂口頭」與 §7.1、第九章的標題）保護。新章第 12 章沒有說明這個差異。報告以 `hw2_report.pdf` 隨 ZIP 交付（`doc/screenshots/v2-issue78/zip_manifest.txt` 第 2 列）。

要裁決的是：在 accepted boundary 內，第 12 章是否**必須**加入說明；若必須，內容為何。

## 2. 依據

| 來源 | 內容 | 用途 |
| --- | --- | --- |
| SRC-4 二.5、三（上位契約） | 「主要繳交:   跟 DIC2 一樣github and web」；「optional :對話內容, 資訊圖表 , 報告書」；二.1「>13 個特徵」 | 現行的作業頁正文 |
| Brief V2 §2（accepted） | SRC-4 是「正式需求 [T4]」；SRC-1／SRC-2T 是「歷史比較來源」；補充段「新版未載明」，不得推定老師已刪除；差異表：特徵數 10–20 → >13「（事實更正）」 | 前面各章所依的是歷史來源；未載明不等於刪除 |
| Brief V2 §3.5 覆寫 1、4（accepted） | Dashboard 與 repository 是主要交付 [T4][D Q24]；「10 至 20 個特徵」→ >13 [T4] | 現行 accepted 語義 |
| Brief V2 §7；Spec V2「文件、README、報告與打包」（accepted） | 報告新增「探索模式」一章；正式分析各章數字不變；報告在 SRC-4 下屬 optional，仍照 V1 交付 | 第 12 章是 V2 唯一可更新的報告位置，且報告仍是交付物 |
| #78 AC「報告」；I-5；run designation 第 4 點 | 正式各章與前言只允許新章節與日期不同；既有測試不變 | 凍結文字不得修改 |
| Bindings §2.4（每份 OC 的固定 constraint） | scope class 標示必須明確，不得混淆 | 標示的如實 |
| derivation §7.2 H-4（V2）、V1 H-4 | 證據真實性與如實標示：含 scope class 標示（I-4）、「三種標示混淆」 | 高風險類別；交付文件不得含與現行上位契約相反、且未加說明的事實陳述 |
| derivation B-8 | README 的「10–20」改為「>13」；報告 §1.2（引用 SRC-1／SRC-2T 原文與交集規則）不改 | 同型的既有分配；本裁決不改變它 |
| `decision-20261022-r1f3-v1-footer.md` R3-3、R3-6 | 凍結的 V1 文字不改；同一問題出現在可更新的 V2 交付物時，在該交付物如實說明（README），屬分配、不是新 AC | 先例 |
| `report/report.md` 第 391–394 行 | 12.5「前面各章的範圍」已存在，用來限定第 7.1 節與第九章陳述的範圍 | 說明的自然位置 |
| `tests/test_report.py` 第 26、48–69 行 | 模板的散文不得有手打數字（日期、「>13」的 13 都會命中；code span、`第 x.y 節`、`SRC-4` 的 4 不命中） | 內容的形式限制 |
| `tests/test_explore_docs.py` 第 112–138 行 | 第 12 章唯一的 placeholder 是 `k_range`；第 12 章以外的模板必須等於接受基準；12.5 須保留「第 7.1 節與第九章」 | 內容的形式限制 |
| `README.md` 第 24 行 | 已如實說明 dashboard 原是課堂口頭要求、新版作業頁把主要繳交改為 github and web（#78 R1 與 SIA 核對過） | 第 12 章與 README 應一致 |

## 3. 裁決

### S1-1 第 12 章必須加入說明（需要 rework）

**裁決：需要。** 這是對既有 accepted 內容的分配（治理 §1.2），不是新 AC。

理由：
1. **交付物內有與現行上位契約相反、且沒有任何說明的事實陳述。** 第 9 行「作業頁…文字都沒有要求網站」與第 28 行「作業頁正文沒有」以現在式描述作業頁；V2 的正式需求是 SRC-4，它的正文把 web 列為主要繳交。報告隨 ZIP 交付給評分者，讀者看到的是一句與老師現行作業頁相反的陳述。這落在 H-4（如實標示）與 Bindings §2.4 的範圍內；H-4 是 DA 宣告的高風險類別。
2. **accepted 語義已經決定了正確的事實。** Brief V2 §3.5 覆寫 1 把 dashboard 改為主要交付，§2 把 SRC-1／SRC-2T 定為歷史來源。說明只是把 accepted 的事實寫進 V2 的交付物，不新增 requirement、AC、scope、gate 或 seam。
3. **凍結文字不能改，所以唯一在 boundary 內的位置是第 12 章。** 這與 R3-3／R3-6 的處理相同：凍結的 V1 文字保持不變，在可更新的 V2 交付物如實說明。第 12 章已有 12.5「前面各章的範圍」，用途正是限定前面各章陳述的範圍。
4. **不處理的代價不對稱。** 修正只需第 12 章的一個段落，不改正式章節、不改既有測試；不處理則 V2 的交付報告在宣告的高風險類別上留有一句未加說明的錯誤陳述。

Reviewer 判定它不 blocking 的理由（標示類別「老師要求」仍正確、方向是低估、README 已正確、報告屬 optional）我都同意；它們說明風險低，但不使這句陳述成為如實。是否 blocking 屬 Reviewer；本裁決只作 allocation，不改變 SIA 的 verdict。

### S1-2 必須的內容（C-1～C-4）

在 `report/report.md` **第 12.5 節「前面各章的範圍」**新增條目（放在既有兩條之前或之後皆可），內容**必須**涵蓋：

| # | 必須陳述 |
| --- | --- |
| **C-1** 範圍 | 前面各章（標示說明與對照表、第一章到第十一章、附錄）引用或描述的作業頁內容，依的是撰寫正式分析時的**舊版作業頁**；為了讓正式分析的內容不變，這些引用與標示保留原文。 |
| **C-2** Dashboard（SIA-F1 本身） | (a) 標示說明與對照表、第 7.1 節與第九章的「課堂口頭」標示與「作業頁正文沒有要求網站」的說法，只描述舊版作業頁；(b) 更新後的作業頁（SRC-4）正文把主要繳交列為「跟 DIC2 一樣github and web」（引用原文字串，與 README 第 24 行相同）；(c) 本專案的 web 交付就是 GitHub Pages 上的這個 dashboard，所以 GitHub repository 與這個 dashboard 現在是作業頁正文列出的主要繳交；(d) dashboard 的標示類別仍是「老師要求」，改變的只是它在作業頁上的來源。「web＝Pages 上的 dashboard」必須寫成本專案的對應（主詞是本專案），不得寫成老師原文的內容。 |
| **C-3** 特徵數 | 更新後的作業頁把特徵數條件改為「>13 個特徵」；第 1.2 節的交集條件依舊版作業頁；King County 的 source feature 數也符合新條件（不寫出數字）。 |
| **C-4** 未載明的內容 | 不得陳述或暗示老師刪除了新版作業頁沒有載明的內容（舊版的「補充」段與評分標準的原文）。可以寫「更新後的作業頁沒有載明」，或完全不提。 |

C-3 的理由：同一份交付報告的第 1.2 節以「作業頁正文寫：」引用舊版的「10 至 20」，與 SIA-F1 是同一類陳述，Brief V2 §2 已把 10–20 → >13 定為「事實更正」。只更正 dashboard 而在同一段落略過它，會讓 12.5 的範圍說明選擇性地不完整。C-3 不改 B-8：第 1.2 節仍不改，README 的更正照舊；本裁決只在第 12 章加一句說明。

**形式限制**（現有測試與 accepted 不變量；違反任一項即不符本裁決）：
- 散文不得有手打數字：日期不得寫成數字（用「更新後的作業頁（SRC-4）」，與第 12 章開頭相同）；「>13」寫在 code span 內（例如 `` `>13` ``）或以中文數字表達；不得寫 King County 的特徵數；不得用「(1)」「(2)」這類編號（`2` 會命中）。`SRC-4`、`DIC2`、`第 x.y 節`、中文章號不會命中。
- 不新增 placeholder（第 12 章唯一的 placeholder 仍是 `{{k_range}}`）。
- 12.5 既有兩條保留，「第 7.1 節與第九章」字樣仍在。
- 不得提「講義」（SRC-4 不涉及講義，前言對講義的陳述不受影響）。
- 不得使用「新版作業頁要求了 dashboard 的某項功能」這類超出 SRC-4 原文的說法。

**參考文字**（符合 C-1～C-4 與形式限制；Executor 可改寫，但改寫後仍須逐項符合）：

> - 前面各章（標示說明與對照表、第一章到第十一章與附錄）引用或描述的作業頁內容，依的是撰寫正式分析時的舊版作業頁；為了讓正式分析的內容不變，這些引用與標示保留原文。更新後的作業頁（SRC-4）有兩處與此不同。一是主要繳交改為「跟 DIC2 一樣github and web」：本專案的 web 交付就是 GitHub Pages 上的這個 dashboard，所以 GitHub repository 與這個 dashboard 現在是作業頁正文列出的主要繳交；標示說明與對照表、第 7.1 節與第九章的「課堂口頭」標示與「作業頁正文沒有要求網站」只描述舊版作業頁，dashboard 的標示類別仍是老師要求，改變的只是來源。二是特徵數條件改為 `>13` 個特徵；第 1.2 節的交集條件依舊版作業頁，King County 的 source feature 數也符合新條件。舊版的「補充」段在更新後的作業頁沒有載明，本報告不推定老師已刪除它。

### S1-3 必須不變

- 第 12 章以外的 `report/report.md`（前言、對照表、第一章到第十一章、附錄）逐字不變；第 12 章的標題、標示、開頭兩段、標示表與 12.1～12.4 不因本裁決改變（SIA-F2 的選擇性處理見 S1-6）。
- `tests/test_report.py`、`tests/test_explore_docs.py` 與其他既有及 V2 測試不改（I-5；V2 測試不需要為本條目修改；若 Executor 認為需要新增斷言，只能擴充，不得削弱）。
- `index.html`、`assets/`、`hw2/`、`results/`、`hw2.ipynb`、`README.md`（S1-6 例外）不改；ZIP 內 dashboard 的位元組因此與已驗證的 ZIP 相同。
- 建置流程（`hw2/report.py`、`hw2/package.py`、`hw2/pdf_append.py`、`report/` 其他檔）不改。
- B-8 不變；Outcome Contract、Brief、Spec、`tickets-v2.md`、GitHub issues 不改。

### S1-4 交付物的連帶更新（同一 rework）

報告的交付形式是 ZIP 內的 `hw2_report.pdf`，所以只改模板不夠。同一 rework 必須：
1. 以既有建置流程重建報告 PDF，並以既有打包流程重新打包 `dist/<學號>_hw2.zip`（學號只在 `.local/packaging.json`，BR-03）。
2. 更新 ACCEPTANCE 中受影響的 V2 條目（報告 V2-36、ZIP V2-41 的 sha256 與清單；其他條目的證據若引用舊 ZIP 的 sha256，註明新舊對應），並更新 `doc/screenshots/v2-issue78/` 的 ZIP 清單或另存新清單，舊紀錄保留可追溯。
3. 依 SIA-F3 的條件核對：新 ZIP 內 `index.html` 與 `assets/` 每個檔的 sha256 等於 rework commit 的 blob；並與已驗證的 ZIP（sha256 `57e1e4a4…bcd11`）的對應項目逐一比對，記錄除 `hw2_report.pdf` 外有哪些項目改變（預期：沒有）。
4. Worklog `doc/governance/worklog/issue-78.md` 以同一 worklog identity 續寫：Contract reference 引用本紀錄；記錄 rework 的 commit、self-verification（全部 pytest 與 Node，0 skipped；報告建置；ZIP 核對；A-4 學號核對）與 binding。

### S1-5 必要的審後驗證與 audit coverage（phase acceptance 的前提）

這個 rework 發生在 #78 R1 與 Spec Integration Audit R1 都已 closure 之後，修改的是 H-2、H-4 涵蓋的交付物（報告與 ZIP），會影響 SIA record 的 S-32、S-34 與其受審 subject identity。依治理 §3.8（「可能影響原 review 結論者，由 Reviewer／Design Authority 判定必要後續」）、§4.7 與 orch-default v2.2 §6（Spec Integration Audit 的 finding 修正是契約內 rework，同一 Ticket worklog identity，審後驗證）、§7 P7，我判定：

- **必要**：由 `gov-primary-reviewer` 對 rework 的 delta 作 independent review，作為 **同一 Spec Integration Audit instance（cycle 1）的 R2**（Bindings §7：`audit/spec-SPEC-V2-c1-r2.md`）。這不是新的 cycle（本裁決不是 contract change，也沒有 FA 授權；治理 §4.5），也不是任何 Ticket audit 的 R3。R2 依治理 §4.4 限於：
  1. 第 12 章的新條目逐項符合 S1-2（C-1～C-4 與形式限制）與 S1-3，且陳述與 SRC-4、Brief V2 §2／§3.5 相符（H-4、A-5(V2)）；
  2. 沒有回歸：`git diff --name-only 3745e9c <新 subject>` 中非 record-only 的路徑只有 `report/report.md`、`doc/acceptance/`、`doc/screenshots/`（以及 S1-6 若採用時的 `README.md`）；第 12 章以外的模板與接受基準相同；Reviewer 自行執行全部 pytest 與 Node 測試；
  3. ZIP（A-6、H-1／A-4）：檔名、sha256 與清單；`hw2_report.pdf` 含新條目；dashboard 項目與新 subject 的 blob 逐位元相同、與已驗證 ZIP 的對應項目相同；追蹤檔案與 ZIP 內容沒有實際學號。舊 ZIP 上已做的 OV-1／SR-09 證據能否延用，由 Reviewer 依上述比對判定（evidence sufficiency 屬 Reviewer）；
  4. 若採用 S1-6，核對 SIA-F2 的修正。
- R2 的 record 必須寫明新的最終 subject（commit SHA），使 phase acceptance 引用的 Spec Integration Audit closure 涵蓋最終整合 subject。
- **不另要求** #78 的另一輪 Ticket audit：#78 R1 已 closure，rework 的 delta 小且完全由上列 R2 涵蓋；同一 delta 審兩次不增加保證。

### S1-6 SIA-F2 可以一併處理（不要求）

SIA-F2（README 與報告 12.3 對 Lasso 停止原因的列舉缺 `multiple_drops`、`target_constant`，尺度寫「除以均方根」而實作是「置中並除以均方根」）的內容屬 R4-5 已分配給 #78 的既有義務，所以修正它是契約內 rework，不是新工作。SIA record §8 的 disposition 是「不需本 cycle 修正；若修改 README／第 12 章，順帶補上」。本裁決**不要求**它，phase acceptance 也不以它為前提；Orchestrator **可以**把它放進同一次派工。若採用，必須：
- README「探索模式（加分功能）」的「Lasso 路徑的停止」條目與報告 12.3「Lasso 路徑的停止」段落一致地修改，兩處都只改這兩點：(a) 停止原因的列舉加入「同一步有多個 group 同時離開路徑」與「預測目標在這些列上沒有變化」，或把列舉改寫成明示不完整的「例如」；(b) 尺度改為「目標在同一批列上置中後除以其均方根」（與 `assets/explore_engine.js` 檔頭、`index.html` `#ex-lasso-card` 相同）；
- 不改 `index.html` 與 `assets/`（`#ex-lasso-card` 的列舉也不完整，但改它會動到 dashboard 位元組與 OV-1 證據，不在本次範圍）；
- `test_exploratory_limits_are_disclosed` 要求的字樣（「均方根」「不改變進入順序、停止點與候選狀態」「實際的停止原因」等）保留；
- 由 S1-5 的 R2 核對。若不採用，SIA-F2 維持 tracked item。

### S1-7 不採用的路徑（屬 acceptor）

修改凍結的正式文字（前言第 9 行、對照表第 28 行、§7.1 與第九章的標題）或 `tests/test_report.py` 的斷言，會改變 #78 AC 與 I-5 的 accepted 不變量，屬治理 §5.3 第 1 類 contract change，須 acceptor 核准。本裁決**不走、也不建議**這條路：S1-2 已在 boundary 內讓交付報告如實。沒有需要 fail-closed 的事項。

## 4. 是否改變 accepted 語義

**否。** S1-1～S1-6 屬治理 §5.3 第 2 類：
- S1-1、S1-2 是把 accepted 的事實（Brief V2 §2、§3.5 覆寫 1 與 4）依 H-4 與 Bindings §2.4 分配到 V2 交付報告的新章節；與 R3-6 同型，不新增 requirement、AC、scope、gate 或 seam，不改 #78 AC（新條目在新章節內）。
- S1-3 維持 accepted 不變量。
- S1-4、S1-5 是 #78 既有交付（報告、ZIP、ACCEPTANCE）的連帶更新與治理 §3.8 的審後驗證。
- S1-6 是 R4-5 的既有內容，選擇性處理。

唯一會改變 accepted 語義的路徑（S1-7）沒有採用，不需 acceptor。

## 5. Phase acceptance（Spec V2 rev 2，#73）：**DEFERRED PENDING REWORK**

依派工規則，Part A 需要 rework，所以本次**不作** phase acceptance，也不寫 phase-acceptance record。Phase acceptance 等待：

1. S1-2～S1-4 的 rework 在 `home_work_02-v2-enhance` 上完成（同一 #78 worklog identity），含 Executor 的 binding 核對；
2. S1-5 的 Spec Integration Audit cycle 1 R2 record 存在且為 `VERDICT: CLOSURE`，subject 為 rework 後的最終整合 subject；Reviewer 的 binding 已依 Bindings §3.6 核對；
3. Orchestrator 依 orch-default §7 P7 核對 R2 subject 與 phase acceptance 時的 HEAD 之間只有 record-only delta；
4. 之後重新派工 Design Authority 作 phase acceptance。屆時的 record 必須引用 `audit/spec-SPEC-V2-c1-r1.md` 與 R2 record，並引用本紀錄。

**Phase acceptance 時必須明列、不得當作 PASS 的 open items**（目前狀態；屆時重新核對）：

| 項目 | 狀態 | Authority／owner |
| --- | --- | --- |
| B-10：GitHub Pages URL 上的檢查（Brief V2 §8 第 3 條「於 Pages 上」、§3.2「Pages 與 ZIP 一致」、§14 P0；ACCEPTANCE V2-42 NOT TESTED（pending merge）） | 合併後的 Lightweight work item，需 acceptor 的直接指示作為其 Outcome Contract；觸及 H-2、H-5，需 independent audit（derivation §7.5） | acceptor 指示後執行 |
| SIA-F2 | tracked item（除非依 S1-6 處理並經 R2 核對） | Orchestrator |
| SIA-F3（重新打包須核對 dashboard 位元組等於 blob） | tracked item；本次 rework 依 S1-4 第 3 點適用；之後任何重新打包（含繳交前）照同一條件 | Orchestrator（completion report 告知 acceptor） |
| SIA-F4（參照的 active-set 退化分支無測試） | tracked item；新的工作須依治理 §1.2 取得接受 | Orchestrator |
| SIA-F5（晚到 URL 回應的世代檢查無測試偵測） | tracked item；同上 | Orchestrator |
| Push | 未執行；run designation 第 6 點選項 (a)：須 acceptor 逐次授權 | acceptor |
| 合併進 `main` | RB-1（OC §5 沒有 SA-3 opt-in） | acceptor |
| iLearning 繳交（repository URL＋Pages URL＋ZIP） | RB-2 | acceptor |
| GitHub issues #73–#78 | 仍為 OPEN：commits 未 push；權威結案紀錄是 run record 與 audit records | Orchestrator，於 acceptor 的 push／merge 決定時同步 |
| 向老師確認「兩種 problem」 | 可選，不是完成條件（Brief V2 §9） | acceptor |

## 6. 受影響的 work items 與 evidence

| 對象 | 影響 |
| --- | --- |
| **#78** | 契約內 rework（S1-2～S1-4，選擇性 S1-6），同一 worklog identity；#78 R1 的結論不重開 |
| **Spec V2 Spec Integration Audit** | 需要 cycle 1 R2（S1-5）；R1 record 不改寫；SIA-F1 由 R2 核對修正 |
| **Phase acceptance（#73）** | 延後至第 5 節第 1–4 點完成 |
| ACCEPTANCE V2-36、V2-41（與引用舊 ZIP sha256 的條目） | 依 S1-4 更新；舊紀錄可追溯 |
| `dist/<學號>_hw2.zip`、`hw2_report.pdf`（未追蹤） | 重建與重新打包；舊 ZIP 的 sha256 `57e1e4a4…bcd11` 不再是最終繳交物 |
| `README.md` | 不改（S1-6 例外）；第 24 行已如實 |
| `index.html`、`assets/`、測試、V1 產物、契約、Spec、票、GitHub | 不改 |
| #74–#77 | 無影響 |
| B-8、R3-6、R4-5 | 不變；本紀錄引用之 |

## 7. Evidence

- 讀取：Bindings b5 全文；治理 v2.2 §1.1–§1.5、§2.1、§2.4、§2.5、§3.3–§3.8、§4.1–§4.7、§5.1–§5.4；orch-default v2.2 §6、§7（P7）；`outcome-contract.md` 全文；`BRIEF-V2.md` 全文；`SPEC-V2.md` 全文；`gh issue view 78`（body）；`derivation-SPEC-V2.md` 全文；`decision-20261022-r1f3-v1-footer.md` 全文；`decision-20261022-issue75-lasso-early-stop.md` R4-5；`decision-20261018-high-risk-categories.md` 全文；`audit/spec-SPEC-V2-c1-r1.md` 全文；`audit/issue-78-c1-r1.md` F1 與 disposition（第 55–56、93、109、131、165、173 行）；run record 第 1–30 行與 P9／第 22–23 列。
- 上位契約：`doc/requirement/HW2-req_new-20261021.txt` 全文（「主要繳交:   跟 DIC2 一樣github and web」「>13 個特徵」「optional :對話內容, 資訊圖表 , 報告書」）。
- 受審檔案：`report/report.md` 第 1–40、40–75、225–409 行；`README.md` 第 1–40、140–170 行；`assets/explore_engine.js` 第 40–60 行；`assets/explore_app.js` 第 90–94 行；`index.html` 第 162 行；`doc/screenshots/v2-issue78/zip_manifest.txt`（`hw2_report.pdf` 在 ZIP 內，`report/report.md` 不在）。
- 測試：`tests/test_report.py` 第 1–100、125–145、360–375 行（`_NUMBER`、`_STRUCTURAL`、`_ALLOWED_LITERALS`、「課堂口頭」斷言）；`tests/test_explore_docs.py` 全文（第 12 章 placeholder 只限 `k_range`、第 12 章以外等於 `d7f02d4`、必要字樣）。
- `git log --oneline -3`（HEAD `3750de4`）；`git status --short home_work_02`（空）。
- Binding：本 assignment transcript（agentId `a67436700d54c6ca4`）以 Bindings §3.6 的方法掃描。
- 寫入的檔案只有本紀錄；沒有修改契約、Spec、票、程式、測試或其他紀錄；沒有 commit。
