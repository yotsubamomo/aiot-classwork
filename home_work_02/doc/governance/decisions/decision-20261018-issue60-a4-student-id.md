# Decision record — #60 R1 的 R-1（A-4 實際學號比對的時點）與 F-5（H-2 標示）

- **紀錄類型**：Design Authority decision record（治理 §2.4、§3.6、§5.1、§5.3 第 2 類；Bindings b5 §5、§7）
- **日期**：2026-10-18
- **Run**：`run-20261018-hw2-formal`。Orchestrator 依治理 §2.4「已指明 authority，且與本節規則一致」派工。
- **問題來源**：`doc/governance/audit/issue-60-c1-r1.md` §5 R-1（required authority＝Design Authority）與 §4 F-5（required authority＝Design Authority）。問題以該 record 原文為準。
- **受審 subject**：branch `home_work_02-regrill`，implementation commit `f20d70ebdc76ba7e1fd244769fa141fa23bf0641`；本紀錄撰寫時 HEAD＝`3bb88ad`，`origin/home_work_02-regrill`＝`60d7fa67`（`e2d3e0b`、`f20d70e`、`786d46b`、`7fe5ac2`、`3bb88ad` 都還沒 push）。
- **Binding**：`gov-design-authority`，`claude-opus-5-5`／`high`（Bindings §3.1 預設 mapping，沒有 escalation，沒有替代）。本紀錄不自證 binding，由派工者依 Bindings §3.6 核對。
- **Capability escalation**：不提出。E-DA/D1 不成立：R-1 的各種讀法可以用 Spec「Acceptor 輸入與等待」、derivation §9.2、designation 第 5 點、Brief §11 BR-03 與 H-1 的風險機制裁決，不是證據無法裁決的設計選擇。E-DA/D2 不成立：R1 Reviewer 指出的是 A-4 沒有寫明時點的契約缺口（治理 §4.2 routing signal），沒有以證據推翻或爭議 A-4 的內容；A-4 的原作者就是 DA，本紀錄是對它的釐清。

## 1. R-1：學號設定還不存在時，A-4／#60 AC-8 的實際學號比對

### 1.1 依據（原始契約與證據）

| 來源 | 內容 |
| --- | --- |
| Brief §11 BR-03（accepted 語義） | 追蹤檔案一律寫 `<學號>`，實際值只放本機未追蹤的打包設定與繳交 ZIP；「**驗收時**以 `git grep` 確認追蹤檔案沒有實際學號」 |
| Brief §9、OC §2 | 學號是 acceptor 專屬輸入，用途是「繳交檔名」 |
| Spec rev 5「Acceptor 輸入與等待」 | 學號設定由 acceptor 放入未追蹤目錄；「缺少時只停止對應章節與打包，其餘工作照常」 |
| Spec rev 5 人工檢查表「Repo」 | `git grep` 無實際學號（#67 執行） |
| derivation §9.2、`tickets.md` | #67 另需學號設定 |
| Run record §1 designation 第 5 點（acceptor 原文） | 「Acceptor 輸入（學號、ChatGPT PDF、NotebookLM 材料）我會在 #66／#67 之前提供。」 |
| Run record §1、§5 | Push 採選項 (a)：每張票 audit closure 後逐次向 acceptor 取得一般 fast-forward push 授權；run-to-completion 指示沒有改變這一點 |
| `decision-20261018-high-risk-categories.md` H-1 | 學號歸在 H-1，理由是「內容一旦 push 或合併就會公開，移除需要改寫已 push 的歷史（RB-6）」；涵蓋位置含 commit message、Issue、PR |
| 同紀錄 A-4（DA 的 assurance 要求） | 每張票結案前與 Spec Integration Audit 時以 `git grep` 比對實際學號，比對值從本機未追蹤設定讀取 |
| Bindings §2.5 SA-1 | 排除「刪除或改寫既有歷史」 |
| Subject 的實作（我自行讀取 `f20d70e`） | `tests/test_repo_hygiene.py::test_no_tracked_file_contains_the_student_id` 只對**工作樹的追蹤檔案**（`git grep -F … -- :/`）比對，不涵蓋 commit 歷史或 commit message；設定不存在時 skip |

### 1.2 判斷

- A-4 的「每張票結案前」是我在 accepted 的 BR-03（驗收時比對）之上加的 assurance 時點，屬 DA 依治理 §5.1 決定的 assurance 要求，不是 accepted 語義。它和同一條契約鏈中「學號設定在 #67 前提供、缺少時只停止打包」互相衝突；這是我起草 A-4 時沒有寫明時點的缺陷。讀法 (i)（#60 結案前必須取得設定）會讓 run 在 #60 停住，違反 Spec「其餘工作照常」與 acceptor 自己排定的輸入時點，所以不採用。
- H-1 的風險在**公開**時才變成不可逆，公開點是 push（topic branch 推上 origin）或合併。本機 commit 與票的結案本身不公開任何內容。因此，比對最有保護效果的位置是每次 push 之前，而且範圍要涵蓋**將被 push 的全部 commit**（每個 commit 的樹與 commit message），不只是 tip 的工作樹。這比 A-4 原文（每張票結案時對工作樹 `git grep`）更嚴格。
- 因此採讀法 (ii)，並把權威比對綁在 push 上。這樣 A-4 防的風險沒有減少，BR-03 的驗收比對也沒有改變。

### 1.3 裁決（對 #60～#67、Spec Integration Audit 與本 run 的 push 有約束力）

| # | 內容 |
| --- | --- |
| S-1 | **票的結案（學號設定不存在時）**：A-4 的實際學號部分在票結案時，以 Reviewer 自己取得的替代證據滿足結案條件。Audit record 與 worklog 記為「實際值比對 NOT VERIFIED（學號設定尚未提供；依 `decision-20261018-issue60-a4-student-id.md` S-1）」，**不得記為 PASS**。替代證據至少包括：受審 range 新增的內容中「學號」只以 `<學號>` 佔位或敘述用詞出現；每段 7 位以上的數字串都歸類為非學號（hash、`id`、日期、資料值等）；range 內每個 commit message 也同樣核對；過程中不印出任何疑似值。A-4 的其他項目（acceptor 材料、打包設定與輸出、PDF、ZIP、`kaggle.json`、金鑰）照原文執行，不受本項影響。學號設定存在時，A-4 照原文執行，不適用本項 |
| S-2 | **Backlog 比對（權威比對）**：學號設定第一次存在時，以設定中的值（`git grep -F`，不印出值）比對：(i) `origin/main..HEAD` 每個 commit 的樹（例如對 `git rev-list origin/main..HEAD` 的每個 commit 執行 `git grep -F -q`）；(ii) 同一 range 的全部 commit message；(iii) 工作樹的追蹤檔案（現有的 hygiene 測試）；(iv) 本 run 的 GitHub Issues #59～#67 的本文與留言，以及本 branch 已開的 PR（這些已經公開，所以這一項只是偵測，不是防止公開）。紀錄只寫「已核對、無命中」，加上涵蓋 range 的起點與終點 SHA。之後每次比對涵蓋上次已核對的終點之後的新 commit |
| S-3 | **Push gate**：任何會把未經 S-2 比對的 commit 推上 origin 的 push，執行前都必須完成 S-2 且無命中。這是確定性的機械檢查（只有命中或無命中），由 Orchestrator 執行並把結果記入 run record，不涉及 evidence sufficiency 的判斷。學號設定不存在時，Orchestrator 向 acceptor 請求 push 授權時必須寫明：「實際學號比對尚未執行；需要先在 `home_work_02/.local/packaging.json` 放入學號設定，才能執行 push」。一般性的 push 授權（例如「push 選項 (a)」或某張票的 push 授權）**不視為**豁免這項比對。只有 acceptor 針對這項未比對狀態的明確指示，才可能改變這一點；那是 acceptor 的決定，Agents 不得推定 |
| S-4 | **Reviewer 覆核**：學號設定存在後派出的第一個 Ticket R1（如果當時已沒有 Ticket R1 要派，則由 Spec Integration Audit）必須在其 A-1 節自己重做 S-2，範圍從 `origin/main` 到它的受審 subject，包含 Orchestrator 先前已機械比對過的 range，並依 A-4「Reviewer 仍要自行判斷」核對可能的變形（例如大小寫或前後綴）。此後各票照 A-4 原文執行 |
| S-5 | **最終 gate 不變**：#67 結案、Spec Integration Audit closure、DA phase acceptance 與任何合併之前，S-2 必須已經涵蓋到該時點的 subject，並且無命中；學號設定仍不存在時，這些都不能完成。這就是 Brief BR-03 的驗收比對（Spec 人工檢查表「Repo」），本紀錄沒有放寬它 |
| S-6 | **命中時**：屬 H-1 事件。停止受影響的路徑（push、合併，以及依賴該 range 的後續 commit），寫 stop report，route 給 acceptor（治理 §1.5）。未 push 的 commit 要移除也必須改寫本機歷史，這不在 SA-1 範圍內；已 push 的屬 RB-6。Agents 不得自行改寫歷史、force push，也不得在任何紀錄中印出命中的值 |

### 1.4 對 #60 的適用：完成需要什麼

- **#60 不需要等待學號設定就能結案。** AC-8 依 S-1 判定：PDF／ZIP／金鑰部分已在 R1 record 第 2 節 AC-8、第 3 節 H-1 (a)(b) 判為 PASS；實際學號部分以 R1 record 第 2 節 AC-8 的替代證據滿足結案條件，記為 NOT VERIFIED（依 S-1），不記 PASS。我另外做了只輸出計數的核對（第 4 節），結果與 Reviewer 的替代證據一致，沒有發現 7 位以上數字緊接在「學號」之後的內容。
- #60 的其他完成條件依治理 §3.8 照常核對（R1 已 CLOSURE、沒有 blocking；F-1～F-4 的 disposition 依 R1 record；F-5 見第 2 節）。本裁決解決了 R-1 這個與完成有關的未決 design ambiguity。
- **#60 的 push**：#60 的 commit（`e2d3e0b`～`3bb88ad` 及之後的紀錄 commit）在 S-2 完成且無命中之前不得 push（S-3）。所以 acceptor 要在授權 #60 的 push 之前，或同時，放入學號設定。這不是新的 acceptor gate：push 本來就由 acceptor 逐次授權（run record §1），學號本來就是 accepted 的 acceptor 輸入（Brief §9）。這只是把該輸入需要到位的時點，從「#66／#67 之前」提前到「第一次 push 之前」。如果 acceptor 不 push，run 可以照常進行到 #66（S-1）。
- #60 worklog 第 7 節寫的「required authority：acceptor 提供輸入」不是 #60 結案的條件；這項輸入只在 S-3、S-5 的時點需要。
- 待追蹤的義務（由 Orchestrator 記入 run record）：S-2、S-3 的 push gate；S-4 的 Reviewer 覆核；S-5 的最終 gate。

### 1.5 是否改變 accepted 語義

**否。** Brief BR-03 的規則與驗收比對（「驗收時以 `git grep`」）沒有改變，而且 S-2、S-3 把比對提前到 push，並擴大到 commit 歷史、commit message 與 Issue／PR 文字，只有更嚴格。被釐清的是 DA 自己的 assurance 要求 A-4 的時點，以及 derived AC #60 AC-8 的判定方式，屬治理 §5.3 第 2 類，不需要 acceptor 核准。對進行中工作的影響見第 3 節。

## 2. F-5：#60 的 H-2 標示

### 2.1 裁決

- **確認 F-5。** 依 `decision-20261018-high-risk-categories.md` H-2 的「觸及的工作」，#60 建立了 notebook 六個 CRISP-DM 章節的名稱與順序、單元 README、`home_work_02/index.html` 的路徑、資源載入方式（`.js` 全域變數、打包的 Chart.js）與 `file://` 離線行為，所以觸及 H-2。derivation §9.1 只標 H-1、H-3，是我在 Ticket derivation 時漏標。
- **更正後 #60 的標示**：H-1、H-2、H-3；assurance A-1、A-2、A-4，以及適用全部票的 A-7、A-8。
- **#60 的覆蓋已足夠，不需要另外 audit。** R1 record 第 3 節已有 H-2 一列（notebook 六章的名稱與順序、`home_work_02/index.html` 路徑、`file://` 載入與零對外資源、README、資料集名稱與 Kaggle 連結、兩條老師原文逐字正確），結果 PASS，滿足 A-1 對 H-2 的要求。不需要修改實作，不新增 audit round，也不重開 R1。A-7 自本紀錄起明確適用於 #60（如果之後出現 H-2 的 blocking finding，要 defer 必須有 DA 確認）。

### 2.2 標示規則的釐清（適用於全部票）

**同一個漏標也出現在其他票，所以一併處理。** 票只要建立或修改下列任何一項，就觸及 H-2：notebook 的章節標題與順序；README；dashboard 靜態檔（`index.html`、`assets/**`，含打包的程式庫）的路徑、資源載入方式或離線行為；預測圖；報告的章節或老師要求的標示（含「GPT 輔助內容」「NotebookLM 摘要」與摘要 ≥100 字）；打包腳本、繳交檔名或 ZIP 內容。

依此規則核對 #61～#67 的票文（`gh issue view`）：

| 票 | 現有標示 | 觸及 H-2 的內容 | 更正後 |
| --- | --- | --- | --- |
| #61 | H-2、H-3 | — | 不變 |
| #62 | H-3 | dashboard 新增方法選單、k 格子、指標 vs k 圖、比較全部、提示（資源載入與離線行為） | **H-2**、H-3 |
| #63 | H-3 | dashboard 參考線、比較表、Test 區塊改讀正式結果 | **H-2**、H-3 |
| #64 | H-3、H-4 | notebook Evaluation／Deployment 章節；dashboard「方法與限制」區塊與係數表 | **H-2**、H-3、H-4 |
| #65 | H-2、H-4 | — | 不變 |
| #66 | H-1、H-4 | 報告的「GPT 輔助內容」「NotebookLM 摘要」兩個標示與 ≥100 字（H-2「涵蓋」明列） | H-1、**H-2**、H-4 |
| #67 | H-1～H-4 | — | 不變 |

**#62、#63、#64、#66 的 R1 record** 依 A-1 要有 H-2 一節，至少核對：notebook 六章的名稱與順序沒有被改動；`python -m hw2.offline_scan` PASS 且沒有新增任何對外資源；`file://` 載入仍然可用；`home_work_02/index.html` 路徑不變。#66 另外核對兩個標示字串逐字正確，以及摘要依 B-15 計數 ≥100。這些都是在既有的 R1 內核對，不新增 audit round（A-1）。

### 2.3 是否改變 accepted 語義

**否。** 高風險分類與 assurance 要求由 DA 決定（治理 §5.1），本節只更正 derived 票的標示，並把 H-2「觸及的工作」寫成可操作的規則。H-2 的內容、A-1～A-8 與 accepted 語義都不變（治理 §5.3 第 2 類）。

## 3. 受影響的 work items 與要套用的文字

我不修改票、Spec、Outcome Contract 或索引。以下由派工者**逐字套用**；這是控制面的轉錄，不是決定。

| 對象 | 套用內容 |
| --- | --- |
| Issue #60 本文 | 「**高風險**：H-1（憑證、學號、材料目錄）、H-3（隔離）。」改為「**高風險**：H-1（憑證、學號、材料目錄）、H-2（notebook 六章名稱與順序、README、dashboard 路徑與離線載入；DA `decision-20261018-issue60-a4-student-id.md` F-5）、H-3（隔離）。A-4 的實際學號比對依同一紀錄 S-1～S-6。」 |
| Issue #62 本文 | 「**高風險**：H-3。」改為「**高風險**：H-2（dashboard 的資源載入與離線行為；DA `decision-20261018-issue60-a4-student-id.md` F-5）、H-3。」 |
| Issue #63 本文 | 「**高風險**：H-3（CC-1 約束、單次評估）。」改為「**高風險**：H-2（dashboard 的資源載入與離線行為；DA `decision-20261018-issue60-a4-student-id.md` F-5）、H-3（CC-1 約束、單次評估）。」 |
| Issue #64 本文 | 「**高風險**：H-3（只用 training）、H-4（標示誠實、非因果）。」改為「**高風險**：H-2（notebook Evaluation／Deployment 章節名稱與順序、dashboard 的資源載入與離線行為；DA `decision-20261018-issue60-a4-student-id.md` F-5）、H-3（只用 training）、H-4（標示誠實、非因果）。」 |
| Issue #66 本文 | 「**高風險**：H-1（材料不公開）、H-4（證據真實）。」改為「**高風險**：H-1（材料不公開）、H-2（「GPT 輔助內容」「NotebookLM 摘要」兩個標示與 ≥100 字；DA `decision-20261018-issue60-a4-student-id.md` F-5）、H-4（證據真實）。」 |
| `doc/ticket/tickets.md` 高風險欄 | #60「H-1、H-2、H-3」；#62「H-2、H-3」；#63「H-2、H-3」；#64「H-2、H-3、H-4」；#66「H-1、H-2、H-4」 |
| Run record | 記錄本裁決；把 S-2～S-5 列為 open 的 gate／義務（push 前、第一個學號設定存在後的 R1 或 Spec Integration Audit、#67、Spec Integration Audit、phase acceptance、合併）；對 acceptor 的 #60 push 授權請求依 S-3 寫明學號設定的需求 |

即使上列文字尚未套用，本紀錄對各票也有約束力（各票的共同條款：「AC 只引用 Spec rev 5 與 DA 義務」）。

我在自己的兩份紀錄加上指向本紀錄的註記（不改原文）：`derivation-SPEC.md` §9.1 表下、`decision-20261018-high-risk-categories.md` §3 表下。

| Work item | 影響 |
| --- | --- |
| #60 | 可依 S-1 結案（其他 §3.8 條件照常）；標示更正為 H-1、H-2、H-3，R1 的 H-2 覆蓋已足夠；push 受 S-3 約束 |
| #61～#66 | 學號設定存在前結案的票都適用 S-1；設定存在後的第一個 R1 執行 S-4；#62、#63、#64、#66 加標 H-2，R1 要有 H-2 一節 |
| #67 | S-5（BR-03 驗收比對；學號設定本來就是 #67 的前提）；不變 |
| Spec Integration Audit、DA phase acceptance、合併 | S-5；如果到那時都沒有 Ticket R1 執行過 S-4，就由 Spec Integration Audit 執行 |
| 既有 evidence | `issue-60-c1-r1.md` 的結論與 coverage 仍然有效；不重開任何 finding |

## 4. 需要其他 authority

- **#60 的結案不需要 acceptor**；本紀錄沒有 contract change，也沒有 boundary 疑義。
- **Acceptor 輸入（不是授權缺口）**：本 run 的第一次 push 之前，或與該次 push 授權同時，acceptor 需要放入 `home_work_02/.local/packaging.json`（S-3）。這項輸入本來就屬 acceptor（Brief §9）；Agents 不得自己建立它，也不得從任何對話紀錄取出學號。
- **Acceptor 決定（只在發生時）**：S-6 命中；或 acceptor 想在沒有學號設定的情況下 push（S-3 末句）。

## 5. Evidence

- 讀取：Bindings b5（全文）；治理 v2.2 §1.2、§1.4、§1.5、§2.1、§2.3～§2.5、§3.6～§3.8、§4.1～§4.5、§4.7、§5.1～§5.3；`.claude/agents/gov-design-authority.md`；`audit/issue-60-c1-r1.md`；`worklog/issue-60.md`；`run/run-20261018-hw2-formal.md`；`decisions/decision-20261018-high-risk-categories.md`；`decisions/derivation-SPEC.md`（全文）；`outcome-contract.md`；`BRIEF.md` §9～§15；`SPEC.md` 中學號相關條款（第 65～66、106、200、202～204、233 行）；`doc/ticket/tickets.md`；`gh issue view 60`，以及 #61～#67 的 What to build 與高風險行；`git show f20d70e:` 的 `tests/test_repo_hygiene.py`、`hw2/local_config.py`、`.gitignore`。
- Git 狀態：`git rev-parse origin/home_work_02-regrill`＝`60d7fa67…`；`git log origin/home_work_02-regrill..HEAD` 共 5 個 commit，都還沒 push；`git rev-list --count origin/main..HEAD`＝24；merge-base `5be4d394`。
- 只輸出計數的核對（我沒有學號，所以這只是啟發式檢查，**不是** A-4 比對，也不是 S-2）：(a) `origin/home_work_02-regrill` 上 `home_work_02/` 的完整 diff 歷史中，「學號」後 12 個字元內接 7 位以上數字的新增或刪除行：0；(b) HEAD 的追蹤樹中同一樣式：0 個檔案；(c) `e2d3e0b..HEAD` 新增的行中，「學號」不是 `<學號>` 形式的共 11 行，把數字遮罩後檢查，全部是敘述用詞（R-1、A-4、README 與 worklog 的說明），沒有 7 位以上的數字；(d) `origin/main..HEAD` 的 commit message 中有 7 位以上數字的 4 行，遮罩後全部是紀錄檔名中的日期 `20261018`。過程中沒有印出任何疑似學號的值。
- 寫入的檔案：本紀錄；`derivation-SPEC.md` 與 `decision-20261018-high-risk-categories.md` 各加一行指向本紀錄的註記。沒有修改票、Spec、Outcome Contract、索引、實作或測試；沒有 commit 或 push。
