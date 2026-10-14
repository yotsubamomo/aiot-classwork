# Derivation record — SPEC（HW2 Multiple Linear Regression，`home_work_02/`）

- **紀錄類型**：Design Authority derivation record（治理 §1.2、§3.4；Bindings b5 §7；orch-default v2.2 §12）
- **Derived contract**：[`../../spec/SPEC.md`](../../spec/SPEC.md) **v1.0**（2026-10-14）
- **Outcome Contract**：[`../outcome-contract.md`](../outcome-contract.md)，**ACCEPTED**（2026-10-14）。Accepted normative 內容＝第 1–8 節於 commit `e2153254ccf7a97475d1c22e10d6a1e0717c5497`；接受紀錄＝第 9 節於 commit `370c0ae1bf40385baa1d954c6585d1c175b4124b`。本 DA 核對兩個 commit 的第 1–8 節擷取 sha256 相同（`1cb96315…5baa6`），且 `doc/brief/`、`CONTEXT.md`、`doc/requirement/` 自 `e2153254` 起沒有變更。
- **其他依據**：上位契約 [`../../requirement/HW2-requirements-Multiple Linear regression.txt`](../../requirement/HW2-requirements-Multiple%20Linear%20regression.txt)（sha256 `a969e7e2…61ab`，本 DA 重新計算相同）；Brief v0.3（討論紀錄，§10 資料集核對證據）；[`../../../CONTEXT.md`](../../../CONTEXT.md)；Bindings b5；治理 v2.2 §1.2、§1.5、§2.4、§2.5、§3.1、§3.3–§3.6、§4.1、§4.5、§4.7、§5.1–§5.3；impl-default v2 §12；orch-default v2.2 §3、§7、§12。
- **附帶 decision records**：[`decision-20261014-lane.md`](decision-20261014-lane.md)（Formal）；[`decision-20261014-high-risk-categories.md`](decision-20261014-high-risk-categories.md)（H-1～H-4 與 A-1～A-9）。
- **格式參考**：`home_work_01/doc/spec/SPEC.md`、`home_work_01/doc/governance/decisions/derivation-SPEC.md`、`decision-20260923-high-risk-categories.md`（只參考格式，不是 HW2 的要求）。
- **執行角色與 binding**：`gov-design-authority`。Binding 由派工者依 Bindings §3.6 核對並記錄；本紀錄不自證 binding。本次沒有提出 E-DA escalation（第 9 節）。
- **派工指示**：無角色主 session 作為派工介面（治理 §2.7）轉達的 DA assignment（2026-10-14）：lane 判定 → 高風險類別 → Spec derivation → derivation record；本次**不 derive Tickets**。

## 1. 狀態

| 項目 | 內容 |
| --- | --- |
| 效力 | Spec v1.0 自 2026-10-14 起是有效的 derived contract。它的接受與授權來自已接受的 OC，不需要 acceptor 逐份核准（治理 §1.2）。 |
| 未做 | 未 derive Tickets；未建立 GitHub Issues；未實作；未下載資料；未修改 OC、Brief、`CONTEXT.md`、上位契約、Bindings 或單元以外的檔案；未執行任何 git 寫入操作。 |
| 重新 derive 的條件 | 見 Spec §0。 |

## 2. 依據的 Outcome Contract 條款

| OC 條款 | 用途 | 對應 Spec |
| --- | --- | --- |
| §1 Intent and outcome | Problem Statement、Solution；交付物清單 | Spec Problem Statement、Solution、R-NB、R-RPT、R-PKG |
| §2.1 上位契約 | MVM 完整滿足；唯讀 | 來源類型 T；第 8 節 |
| §2.2 Scope classes M1–M10、E1–E9、OPTIONAL、REFERENCE | 每條 R 的 class；第 8 節 | Spec §1 全部 R 的 Class 欄；R-RPT-5；§8 |
| §2.3 Non-scope | 排除項目 | R-DEP-3、R-CAND-8、R-CONF-5、R-PREP-5；§8 |
| §2.4.1 資料、分區與選模（含偏誤陳述） | 分區、隔離、比較、凍結、偏誤陳述 | R-DATA-4、R-PART-\*、R-PREP-3、R-CAND-\*、R-SEL-\*、R-EVAL-3、R-RPT-2；INV-1～INV-3 |
| §2.4.2 Conformal（方法與三層陳述） | 公式與報告措辭的上限 | R-CONF-\*、R-RPT-3、R-DEP-2；INV-5 |
| §2.5 Constraints（MVM、資料 re-pin、不使用憑證、語言 zh-TW） | constraints 的可驗收化 | R-DATA-1、R-DATA-2、R-NB-5、R-RPT-5、R-REPRO-3；AC-29～AC-31 |
| §2.5.1 AI 研究與對話證據 | 允許與禁止的編輯；材料是否公開由 acceptor 決定 | R-AI-1～R-AI-5、R-REPO-3；INV-7、INV-8 |
| §3.1 OC-A1～OC-A8 | 每條 derive 為一條或多條 AC | Spec §2、§7 |
| §3.2 S1–S4 | 完成＝S2；S3、S4 不阻擋 | Spec §6、§9.1 |
| §3.3 acceptor 輸入 | 只停止受影響的 AC；待填位置 | R-RPT-4（draft／final）、Spec §9.1 |
| §3.4 Failure semantics | FAIL 條件轉為 AC 的 FAIL 例；非 FAIL 的結果 | AC-08、AC-14、AC-16、AC-17、AC-23、AC-25、AC-26、AC-29；Spec §9.2 |
| §3.5 Verification intent | 五類驗證 | R-TEST-\*、AC-20、AC-21；Spec §5、§6 |
| §4、§4.1、§4.2；§9（RB-1 一次性授權、Fable fallback、語言） | 授權範圍、git、合併途徑 | Spec §6 Release 列、§8「不由 Agent 執行」 |
| §5 Relevant context（資料事實、八項設計事項） | Spec 須裁決的事項 | Spec §4.3 D-1～D-8 |
| §6 Assurance path | lane、audit、高風險類別 | 兩份 decision records；Spec §6 |

## 3. Boundary determination

**總判定：Spec v1.0 的全部內容都在已接受的 OC（第 1–8 節，`e2153254`）的 boundary 內。沒有任何 R 或 AC 超出 §2.2 的 scope classes、§2.3 的 non-scope、§2.4 的 accepted 語義或 §3 的 acceptance boundary；沒有改變 accepted 語義；沒有重開 G1–G8 或 C1–C5。** 需要判斷的項目如下（逐字轉錄 OC 的項目不列）。

| # | 項目 | 判定 | 依據 |
| --- | --- | --- | --- |
| B-1 | 只有一份 Spec | 在 boundary 內；見第 4 節的理由。 | 治理 §4.7 |
| B-2 | OC §5 的八項設計事項（Spec §4.3 D-1～D-8） | 在 boundary 內。OC §5 明文由 DA 在 Spec 中決定；每項裁決都在 OC 已接受的語義之內：D-1 保持 source feature 計數在 10–20；D-3 保留 E5「指標以 USD 報告」且對所有候選相同；D-5 符合 OC-A3「合起來涵蓋全部列」；D-6、D-7、D-8 符合 M9、E9、§2.5.1。 | OC §5、§2.2、§2.4、§3.1 |
| B-3 | 固定的參數：`SEED = 2026`、Ridge 與 Lasso 網格、inner-CV 準則（USD RMSE）、18 個 groups、`sale_days` 起始日、`effective_year` | 在 boundary 內。OC E4 要求「inner CV 選特徵數與 hyperparameter」但沒有指定網格或準則；在 Spec 中固定它們，使第一次接觸 Test 時已沒有可依 Test 調整的參數，直接落實 OC §2.4.1 的隔離語義。 | OC §2.4.1、E4；治理 §3.6-B |
| B-4 | Forward／backward 以 source feature 為選擇單位（`zipcode` 為一個 group） | 在 boundary 內。OC 的「特徵」指 source feature（§2.4.1）；以 group 選擇使選擇單位與特徵的定義一致；不改變 E1 的候選範圍。 | OC §2.4.1、E1 |
| B-5 | Data Understanding 的分布性 EDA 只用 Fit | 在 boundary 內。這是 OC「所有選模只在 Fit 內進行」「Test 在凍結後只評估一次」的落實方式；不改變任何交付物，也不是新的 scope。 | OC §2.4.1、E2 |
| B-6 | 報告附錄附上 ChatGPT PDF 的頁面，ZIP 另有獨立的 PDF | 在 boundary 內。老師要求「報告檔…需包含…GPT 對話過程（pdfCrowd 匯出）」，而 G6 與 OC-A8 要求獨立的 ChatGPT PDF；兩者並存才完整滿足 MVM（Bindings §2.4）。頁面原樣附加，不構成 Agent 的改寫（OC §2.5.1）。 | 上位契約 §二.5；OC M5、M9、OC-A7、OC-A8 |
| B-7 | 「100 字以上」以漢字數 ≥ 100 計算 | 在 boundary 內。這是衡量方式的裁決（治理 §3.6-A 類）；漢字數是各種合理讀法中最嚴格的，滿足它就滿足所有讀法（Brief v0.3 §2 [R] 的讀法亦同）。 | OC M6、OC-A7 |
| B-8 | acceptor 原始材料預設不追蹤；`report/report.md`（含摘要與「GPT 輔助內容」的文字）追蹤 | 在 boundary 內。OC §2.5.1 保留給 acceptor 決定的是「原始材料（NotebookLM 輸出與來源清單、ChatGPT PDF）」是否公開；報告中的摘要與說明是報告內容，OC 明文區分兩者（「報告中的摘要與引用可對回原始材料」）。附有 ChatGPT 頁面的報告 PDF 與 ZIP 含原始材料，所以不追蹤。acceptor 若希望摘要也不公開，可以指示，這不是 S2 的條件。 | OC §2.5.1 末段 |
| B-9 | 追蹤的 notebook 名為 `hw2.ipynb`，`<學號>_hw2.ipynb` 只在 ZIP 中 | 在 boundary 內。M9 規定的是繳交檔名；學號在打包前才由 acceptor 提供（OC §3.3、Q5），實作期間無法使用該名稱。ZIP 內的副本與已驗證的 notebook 位元相同。 | OC M9、§3.3 |
| B-10 | ZIP 解壓驗證（R-PKG-4） | 在 boundary 內。它是 OC-A8「ZIP 內含主程式、支援模組、requirements、資料」的證據，也是老師評分「模型正確可執行」的驗證；不新增交付物。 | 上位契約 §三；OC-A8 |
| B-11 | Deployment 章節的內容（frozen predictor＋預測函式＋使用限制） | 在 boundary 內。M4 要求 Deployment 階段有內容；採用 Brief §6 的定義；沒有 Web App、API 或資料庫（OC §2.3）。 | OC M4、§2.3 |
| B-12 | OPTIONAL 不 derive；只允許 Fit 的診斷圖 | 在 boundary 內。OPTIONAL 不是完成條件；其他候選的 Test 區間會增加 Test 的使用，與 OC §2.4.1 的精神衝突，所以不做。 | OC §2.2、§2.4.1 |
| B-13 | 單元 `.gitignore`、`doc/acceptance/ACCEPTANCE.md` | 在 boundary 內；兩者都在單元目錄內（不是 RB-5），分別落實 OC §2.5.1 與 AC coverage 的證據需求。 | Bindings §2.6 RB-5；`CLAUDE.md` 單元結構 |
| B-14 | Python 3.11 與 `==` 固定相依 | 在 boundary 內。E8、E9 與 OC-A6 要求固定相依版本；acceptor 本機為 Python 3.11.2（2026-10-14 DA 核對），week05 參考環境也是 3.11。 | OC E8、E9、OC-A6 |
| B-15 | 報告建置依賴本機的 Edge 或 Chrome | 在 boundary 內。兩者已安裝（2026-10-14 DA 核對），不需要付費（RB-4）或憑證（RB-3）；notebook 重跑（OC-A6）不依賴瀏覽器。 | OC §2.5；Bindings §2.6 |
| B-16 | 由 Executor 以匿名公開端點取得資料一次；失敗時由 acceptor 提供 | 在 boundary 內。OC §2.5 明文允許「匿名公開端點，或本機已固定的副本」；acceptor 提供屬 RB-3 的第三方帳號操作，Spec 只把它列為條件性輸入。 | OC §2.5；RB-3 |
| B-17 | 不建立 CI workflow | 在 boundary 內。OC 沒有要求 CI；`.github/workflows/` 在單元目錄外（RB-5），OC §4.2 也明文不涵蓋單元外的修改。對 release gate 的影響見第 8 節 #2。 | OC §4、§4.2；RB-5 |
| B-18 | 高風險類別：H-1 改寫，新增 H-3、H-4 | 屬 assurance 決定（治理 §5.1；Bindings §5「確認或修改」），內容取自 OC §2.4、§2.5.1、§3.4；不新增 audit round 或 acceptor gate。 | 高風險 decision record 第 4 節 |

**未在 boundary 內而未 derive 的事項**：無。**需要 contract change 的事項**：無。**fail-closed 至 acceptor 的 boundary 問題**：無。

**OC 內部一致性核對**：未發現使 Spec 無法 derive 的矛盾。有一處措辭需要裁決：OC-A7 的「ChatGPT 對話 PDF 已納入」可以讀成「納入報告」或「納入 ZIP」；B-6 的做法同時滿足兩種讀法，不需要選擇其一。

## 4. Spec 分配到的 acceptance boundary

**只有一份 Spec（SPEC v1.0）。分配：OC-A1～OC-A8 全部。** 它同時是同一 OC 的第一份與最後一份 Spec，所以「全部 derived Specs 合起來涵蓋整個 acceptance boundary」的核對（治理 §4.7 第五項）在本 Spec 的 Spec Integration Audit 中執行。

| OC-A | 分配 | Spec AC | 高風險類別 |
| --- | --- | --- | --- |
| OC-A1 資料集 | SPEC v1.0 | AC-01、AC-02、AC-03 | H-2 |
| OC-A2 CRISP-DM | SPEC v1.0 | AC-04、AC-05、AC-18（Deployment 內容） | H-2 |
| OC-A3 隔離 | SPEC v1.0 | AC-06、AC-07、AC-08、AC-09 | H-3 |
| OC-A4 比較與選模 | SPEC v1.0 | AC-07、AC-10、AC-11、AC-12、AC-13、AC-14 | H-3 |
| OC-A5 預測區間 | SPEC v1.0 | AC-15、AC-16、AC-17、AC-18 | H-2、H-3 |
| OC-A6 可重現 | SPEC v1.0 | AC-19、AC-20、AC-21 | H-3 |
| OC-A7 AI 協助與研究 | SPEC v1.0 | AC-22、AC-23、AC-24、AC-25 | H-2、H-4、H-1（AC-25） |
| OC-A8 繳交套件 | SPEC v1.0 | AC-26、AC-27、AC-28 | H-1、H-2 |
| 非 OC-A 的 OC constraints（§2.2、§2.5、§3.4） | SPEC v1.0 | AC-29、AC-30、AC-31 | H-4、H-1 |

AC-29～AC-31 不擴張 boundary，只讓 OC 已接受的 constraints 可以驗收。重疊（AC-07 同時屬 OC-A3 與 OC-A4；AC-18 同時屬 OC-A2 與 OC-A5）都在同一份 Spec 內，不造成分配歧義。

**為何不拆成多份 Spec**：可以考慮的拆法是「分析」（OC-A1～OC-A6，對應 S1）與「繳交」（OC-A7、OC-A8，等待 acceptor 輸入）兩份。不採用，因為：(a) 報告橫跨兩邊：OC-A2、OC-A4、OC-A5、OC-A6 的報告內容與 OC-A7 的章節在同一份 PDF 中，數值單一來源（INV-4）與標示（INV-6、INV-7）會變成跨 Spec 的 invariant，而 Spec Integration Audit 以單一 Spec 為 subject；(b) acceptor 輸入只阻擋少數 Tickets，Orchestrator 依治理 §1.5 只停止該路徑，不需要以 Spec 分界；(c) 工作量由 Tickets 分解承擔，不由 Spec 數量承擔。

## 5. Implementation-readiness 核對（治理 §3.4）

| 條件 | 狀態 |
| --- | --- |
| 沒有把必要設計留待下游 | OC §5 的八項全部在 Spec §4.3 裁決；所有被其他工作依賴的介面與語義都已固定（Spec §4.1）。Spec §4.2 的委派項目都是單一 Ticket 內的 HOW，不被其他 Ticket 依賴，也不改變 AC。 |
| 每條 AC 有可觀察的 PASS／FAIL 與證據 | Spec §2 的 AC-01～AC-31 各有 PASS 條件、FAIL 例、證據與方法。 |
| Invariants 明確 | Spec §3 INV-1～INV-9。 |
| Dependencies 可辨識 | 第 7 節列出預期的分解與依賴；正式的 dependencies 在 Ticket derivation 時決定。 |
| Verification contract 不由下游重新定義 | Spec §5、§6；Tickets 只能引用。 |

## 6. 高風險類別與 assurance

見 [`decision-20261014-high-risk-categories.md`](decision-20261014-high-risk-categories.md)：H-1 改寫為「憑證與 acceptor 控制的材料」，確認 H-2，新增 H-3「評估完整性」與 H-4「證據真實性與標示」；A-1～A-9 規定 audit 的核對義務。Spec §6 的 Verification Strategy 引用之。

## 7. 受影響工作

| 工作 | 影響 |
| --- | --- |
| 進行中的 work item | 無。`home_work_02/` 目前只有文件，沒有實作與 Ticket。 |
| Tickets | 尚未 derive。下列是**不具約束力**的預期分解，供 Ticket derivation 參考；並行度 1（Bindings §6）。 |
| Outcome Contract、Brief、`CONTEXT.md`、Bindings | 不修改。 |
| OC §8 #5 | 「DA 確認 lane 與高風險類別」由兩份 decision record 完成。 |

**預期分解（不具約束力）**

| 暫定 | 內容 | 主要 AC | 高風險 | 依賴 |
| --- | --- | --- | --- | --- |
| T-1 資料與分區 | 取得並固定 CSV；`mlr/data.py`；分區、folds；單元 `.gitignore`；R-TEST-2、R-TEST-3（分區與 folds 部分）、R-TEST-5 | AC-02、AC-06、AC-07（folds 產生）、AC-28（檢查建立）、AC-31 | H-1、H-3 | — |
| T-2 前處理、候選與選模 | `mlr/selection.py`、`mlr/modeling.py`；nested CV；比較與凍結；R-TEST-3（fit 範圍）、R-TEST-6 | AC-07、AC-08、AC-10、AC-11、AC-12 | H-3 | T-1 |
| T-3 Conformal、評估與 Deployment 函式 | `mlr/conformal.py`、`mlr/evaluation.py`；manifest 守門；預測圖；R-TEST-4 | AC-09、AC-14、AC-15、AC-16、AC-18 | H-2、H-3 | T-2 |
| T-4 Notebook 與可重現 | `hw2.ipynb`（六階段）；結果 artifact；`requirements.txt`；README；乾淨環境重跑 | AC-01、AC-03、AC-04、AC-12～AC-14（notebook 部分）、AC-19、AC-20、AC-21、AC-27、AC-30 | H-2、H-3 | T-3 |
| T-5 報告（draft） | `report/report.md`、`tools/build_report.py`；acceptor 證據以外的全部章節（含 M8 比較、scope class 標示、三層陳述） | AC-05、AC-13、AC-15、AC-17、AC-24、AC-29、AC-30 | H-2、H-3、H-4 | T-4 |
| T-6 acceptor 證據整合（final 報告） | 「GPT 輔助內容」、「NotebookLM 摘要」與對照表、ChatGPT 附錄、final 模式 | AC-22、AC-23、AC-25 | H-1、H-2、H-4 | T-5；acceptor 輸入 #1、#2 |
| T-7 打包與整合驗收 | `tools/package_submission.py`；ZIP；解壓驗證；`doc/acceptance/ACCEPTANCE.md`；最終的乾淨環境重跑與全部 AC 對照（Spec Integration Audit 的 subject） | AC-26、AC-28；全部 AC 的最終對照 | H-1～H-4 | T-6；acceptor 輸入 #3 |

## 8. 需要其他 authority 或留給 Ticket derivation 的事項

以下都不是 contract change，也不是 fail-closed 的 boundary 問題；OC 已接受的語義不變。

| # | 事項 | Authority | 理由 |
| --- | --- | --- | --- |
| 1 | acceptor 輸入：ChatGPT PDF、NotebookLM 材料、學號；條件性的資料檔；可選的公開決定 | acceptor | OC §3.3；Spec §9.1。只阻擋 T-6、T-7（及條件性的 T-1）。 |
| 2 | **Release gate 的 check 條件**：Bindings §5 SA-3 merge gates 要求 PR head 上的 checks 全部成功，且「沒有任何 check 回報時視為未滿足」；OC §9 的一次性 RB-1 授權也以「integration checks」通過為條件。本 Spec 不建立 CI（B-17）。HW2 的 PR 是否會有任何 check（例如 Vercel 對 `home_work_01` 專案的 preview）尚未核對；若沒有，SA-3 的條件無法成立，合併會回到 RB-1（OC §4.2「退回 RB-1」）。這不影響 S2。 | Orchestrator 在合併前核對並依 OC §4.2 處理；若需要解釋 OC §9「applicable integration checks」的範圍，屬 acceptor 的授權範圍問題 | 治理 §1.2、§5.2；Bindings §2.5、§5；OC §4.2、§9 |
| 3 | M8 比較需要可查證的網路來源：Executor 是否有網路讀取工具，須在 T-5 派工時確認；沒有時改用 acceptor 的 NotebookLM 來源清單；兩者都沒有時，AC-24 的路徑停止並 route。 | Ticket derivation（DA）；Orchestrator | R-AI-3 |
| 4 | 每張票標示觸及的高風險類別並引用高風險 decision record；acceptor 輸入的票標示為等待輸入，只停止該路徑。 | Ticket derivation（DA） | 高風險 decision record 第 5 節 |
| 5 | Spec 有多張 Tickets，所以單 Ticket fast path 不適用；Spec Integration Audit 另行派工。 | Orchestrator | Bindings §5；治理 §4.7 |
| 6 | DA 的 Fable fallback 與替代紀錄 | 派工者 | OC §9；Bindings §3.1 O-2 |

## 9. Capability escalation 檢查

本次所有設計問題都已裁決，沒有提出 E-DA：

- **(D1)**：考慮過、後果可能不同的問題有偏誤修正（D-3）、離群值（D-5）、共線欄的選擇（D-1）、選擇單位（B-4）。各題都能以 OC 的條款與資料事實裁決：D-3 由 OC §2.4.2 的對稱分數與 INV-3 決定，影響小且不改變任何驗收條件；D-5 由 OC-A3「涵蓋全部列」決定；D-1 的兩個選項對預測等價；B-4 由 OC 的 source feature 定義決定。沒有「後果實質不同、且以現有證據無法裁決」的問題。
- **(D2)**：本單元沒有先前的 DA 決定被 FA ruling 或 Reviewer finding 推翻或爭議。

## 10. Evidence

- 讀取：`docs/governance/project-bindings.md`（b5）；治理 v2.2 §1–§5（相關條文）；impl-default v2 §3、§12；orch-default v2.2 §3、§7、§12、§13；Model Profile v2.5 §3 E-DA；`home_work_02/doc/governance/outcome-contract.md`（`370c0ae`）；上位契約；Brief v0.3（全文）；`CONTEXT.md`；`home_work_01` 的 Spec、derivation record 與高風險 decision record（只參考格式）；`week05/multiple_linear_regression_crisp_dm.ipynb` 的結構與 import（REFERENCE）、`week05/requirements.txt`。
- `git`：HEAD `370c0ae1bf40385baa1d954c6585d1c175b4124b`；`git diff e2153254 370c0ae` 只改 OC 檔頭狀態列與第 9 節；第 1–8 節擷取比對相同；`doc/brief`、`CONTEXT.md`、`doc/requirement` 自 `e2153254` 起無變更。
- 環境：本機 Python 3.11.2；Edge 與 Chrome 已安裝；pandoc、xelatex 未安裝；root `.gitignore` 不忽略 PDF、ZIP、CSV。
- 上位契約 sha256 重新計算：`a969e7e2228e97a35027ad63d3747f2e502bdd685cf7cfca30aaab50048761ab`（與 OC §2.1 相同）。
- 未下載資料、未讀取任何憑證、未呼叫外部 API。

## 11. 寫入的檔案

| 檔案 | 動作 |
| --- | --- |
| `home_work_02/doc/governance/decisions/decision-20261014-lane.md` | 新增 |
| `home_work_02/doc/governance/decisions/decision-20261014-high-risk-categories.md` | 新增 |
| `home_work_02/doc/spec/SPEC.md` | 新增（v1.0） |
| `home_work_02/doc/governance/decisions/derivation-SPEC.md` | 新增（本檔） |

未 commit；git 操作由派工者依 SA-1 處理。

## 12. 修訂紀錄

| 版本 | 日期 | 依據 | 變更 |
| --- | --- | --- | --- |
| 初版（Spec v1.0） | 2026-10-14 | DA 派工（lane、高風險類別、Spec derivation；不含 Tickets） | 初版 derive。 |
