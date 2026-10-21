# Derivation record — SPEC V2 rev 2 與 Tickets #74–#78（HW2 V2 Enhance，`home_work_02/`）

- **紀錄類型**：Design Authority derivation record（治理 §1.2、§3.4；orch-default v2.2 §12；Bindings b5 §7）。依 Outcome Contract §5 的授權，本紀錄**同時是** V2 的 lane decision record 與高風險類別 decision record（第 6、7 節；治理 §3.6、§5.1；Bindings §4、§5），以及 D-1、D-2 兩項 decision（第 8 節）。
- **日期**：2026-10-22
- **Run**：`run-20261022-hw2-v2-enhance`（Orchestrator＝root session `37216426-f292-44f9-bad1-e2d862e7b8f1`；本派工是 run record §5 缺口 O-2）
- **Outcome Contract**：[`../outcome-contract.md`](../outcome-contract.md) §5（V2 Enhance，ACCEPTED 2026-10-22；acceptor 原文 §5.1；登錄 commit `4eb03e6`），連同仍有效的 §1–§4（V1：Brief @ `dff7c55c`＋CC-1、AD-1～AD-3）。
- **接受基準**：commit **`d7f02d4179d2cb5c2ecf0c39a4643a6ef8287907`**（branch `home_work_02-v2-enhance`）。本紀錄的檔案判讀一律以 `git show d7f02d4:<path>` 為準；撰寫時 `git diff d7f02d4 HEAD` 只有 `doc/governance/outcome-contract.md` 與 run record（record-only）。
- **上位契約**：`doc/requirement/HW2-req_new-20261021.txt`（SRC-4，sha256 `1bdc7e4a62d548a083825d4f075cd2288959058e8c29886b1fdd8be06c2a41be`，於 `d7f02d4` 加入）；SRC-1、SRC-2T、SRC-3 依 Brief V2 §2 的地位。
- **相關紀錄**：[`derivation-SPEC.md`](derivation-SPEC.md)（V1）、[`decision-20261018-lane.md`](decision-20261018-lane.md)、[`decision-20261018-high-risk-categories.md`](decision-20261018-high-risk-categories.md)、[`decision-20261018-issue60-a4-student-id.md`](decision-20261018-issue60-a4-student-id.md)、[`decision-20261019-phase-acceptance-SPEC.md`](decision-20261019-phase-acceptance-SPEC.md)、[`decision-20261019-post-merge-ad3-readme.md`](decision-20261019-post-merge-ad3-readme.md)、[`../run/run-20261022-hw2-v2-enhance.md`](../run/run-20261022-hw2-v2-enhance.md)
- **Binding**：`gov-design-authority`，有效 mapping `claude-opus-5-5`／`high`（Bindings §3.1 預設，沒有 escalation，沒有替代）。撰寫時我自行讀取本 assignment 的 transcript（agentId `a4e73f0ab2659a956`，`agentType` `gov-design-authority`）：觀測到 `('claude-opus-5-5', 'high')` 38 則，單一元素。全程核對（含之後的訊息）由派工者依 Bindings §3.6 執行；本紀錄不自證 binding。
- **Capability escalation**：不提出。E-DA/D1 不成立：各問題都能以接受基準的原文、既有測試與 repo 事實裁決；唯一無法裁決的 F-1 屬接受語義／boundary 缺口，依治理 §2.5 走 routing（acceptor），不以 escalation 代替。E-DA/D2 不成立：我對本單元先前的決定沒有被 FA ruling 或經 route 的 Reviewer finding 推翻或爭議。
- **獨立性**：派工內容、run record、Brief／Spec／tickets 中的自我陳述（例如「與 Brief 無衝突」「全部有票承接」）都只當作待驗證主張；第 12 節列出我自己取得的證據。

## 0. 本紀錄的地位

- Spec V2 與 Tickets 由 MATT `/to-spec`、`/to-tickets` 依其自身流程產生（OC §2 第 33 列）。本紀錄**不改寫** Brief、Spec、`tickets-v2.md`、GitHub issues 或任何 V1 產物，只做：boundary determination、acceptance boundary 的分配、lane 與高風險類別、對票有約束力的解讀與分配（第 8 節），以及 findings（第 9 節）。
- **V2 的特殊點**：acceptor 在 OC §5 直接接受了 Spec V2 rev 2、`tickets-v2.md` 與 #74–#78（不只 Brief）。因此這些 derived contracts 的 AC、invariant 與 gate **同時是 accepted 語義**。本紀錄的解讀與分配只在不改變它們的前提下作出；任何會改變其 AC／invariant／gate 的修改都依治理 §5.3 第 1 類（contract change）走 acceptor，不由 DA 以第 2 類處理。這是 fail-closed 的讀法。

## 1. 效力

- 在第 4 節的 boundary determination 下，**Spec V2 rev 2 與 Tickets #74–#78 自本紀錄起是 V2 Outcome Contract 的有效 derived contracts**，唯一例外是 F-1 的路徑（第 4 節 B-13、第 9 節）：「在 `index.html` 加入 V2 的 `<script src>` 並因此修改既有測試」在 acceptor 決定前不在有效範圍內。
- 執行授權來自 OC §5.1「EXECUTION AUTHORIZATION」：OC 登錄與本 derivation 完成並經驗證後，Orchestrator 可續行本 run 並派 #74，執行限 #74–#78 與其依賴。本紀錄不授予任何授權，也不驗證自己（驗證屬 Orchestrator，run record §7）。
- V2 只有一份 Spec。V1 的 Spec rev 5 已 phase accepted（2026-10-19），不受本紀錄影響。

## 2. 依據的 Outcome Contract 條款

| OC 條款 | 內容 | 本紀錄的用途 |
| --- | --- | --- |
| §5 表「接受的內容」；§5.1 第 1–4 點 | Brief V2 rev 2（含 E-1）、Spec V2 rev 2、`tickets-v2.md`、#74–#78；V2 驗收條件、四個測試 seams、依賴、V1 保持要求；基準只限 `d7f02d4` | 第 3 節版本；第 4 節判定的上限；第 5 節分配的對象 |
| §5 表「與 V1 的關係」；§5.1 第 5 點與「SA-3 DECISION」第 3 段 | V2 是增量 Enhance scope，不取代 V1；V1 契約對 V1 正式分析仍有效且具權威；只受明確接受的 V2 覆寫約束 | 第 4 節 B-1（只能在 Brief V2 §3.5 四項覆寫內偏離 V1） |
| §5 表「授權」；§5.1「DESIGN AUTHORITY AUTHORIZATION」 | 派 DA 產生本紀錄；判定 lane 與高風險類別，涵蓋使用者 URL fetch；不得預設低風險、不得略過必要審查 | 第 6、7 節 |
| §5.1「EXECUTION AUTHORIZATION」 | 續行 run、派 #74；限 #74–#78；依既有 Bindings、orch-default、independent review 與 evidence 規則；不新增治理規則或 approval gate | 第 1 節；第 7 節只用既有機制 |
| §5 表「SA-3」；§5.1「GIT AUTHORIZATION」 | 沒有 SA-3 opt-in → 合併屬 RB-1；SA-1 本機 commit；不 push、不 merge、不修改凍結的 V1 產物 | 第 6 節配置；第 5.3 節 run 外項目 |
| §1–§3（V1；Brief @ `dff7c55c`、Grill rev 7、`CONTEXT.md`） | V1 的需求、BR-01～BR-04、BR-03 學號、§10 驗證 | V2 未覆寫的部分照舊（Brief V2 §3.5 末段） |
| §4 CC-1 | Ridge／Lasso 各一次 metric_only test 評估與六項約束 | V1 不變量（第 7 節 H-3） |
| §4 AD-1 | OV-1～OV-6 的 gate／best-effort 分類 | V2 新控制項沿用（#74、#78） |
| §4 AD-2（F-3、N-10） | 不新增 CI；PR checks 不是條件 | 票的共同條款；第 6 節 |
| §4 AD-3（V1 先例） | Pages 檢查移到合併後的 Lightweight item | V2 同樣安排的依據（B-10） |
| Bindings §2.4（OC 的固定 constraint） | MVM 完整滿足上位契約；ENHANCED 須明確 scope class 標示、不得冒充老師要求 | I-4 |

## 3. Derived contracts 與版本

| Derived contract | 位置 | 版本識別 |
| --- | --- | --- |
| Spec V2 rev 2 | `doc/spec/SPEC-V2.md` @ `d7f02d4` | sha256 `695161db7c6d356c71b751fff3f9d0988ce774400e7d87a023de627ec287f9a5`。GitHub #73 body 與本檔逐字相同（只差檔尾一個換行；`diff` 核對）；#73 最後編輯 2026-10-21T12:53:14Z，早於 `d7f02d4`（2026-10-21T16:46:32Z） |
| Tickets 索引 | `doc/ticket/tickets-v2.md` @ `d7f02d4` | sha256 `f1e6b1a680fe72d2d3ac7ebd3a02a064a49320adc3cfcd5c495288a86da77aa4` |
| #74 V2-T1 | GitHub issue | body sha256 `49e3cc504e37d4c0c0649c5409e8395a7978405877331b18a07f514551ae1441` |
| #75 V2-T2 | GitHub issue | body sha256 `834a439c0408940b8116bbb3b46077694e3844a282ed97c08e78dc71823aadd5` |
| #76 V2-T3 | GitHub issue | body sha256 `5d121dd9c08ea8fd05155c45aa4670a8d20bfc28cb954814f502be79e74cb2b2` |
| #77 V2-T4 | GitHub issue | body sha256 `c9b79356313a2ae587fe0f679c6fb680fe57abba67ec1ca7a54605d655ca90fe` |
| #78 V2-T5 | GitHub issue | body sha256 `5e31ce341b67409b98126b8d54e13381fa410150986186e248421090f8c233b2` |

- Issue body 的 sha256 以 `gh issue view <n> --json body -q .body | sha256sum` 於 2026-10-22 計算，作為治理 §1.2 對可變來源的快照識別。GraphQL `userContentEdits` 顯示 #74–#78 **從未編輯**（totalCount 0；`createdAt`＝`updatedAt`＝2026-10-21T16:27Z，早於 `d7f02d4`），沒有留言，label 只有 `ready-for-agent`。所以接受時的票文就是上列內容。之後若 body 改變，以上列 sha256 的版本為 accepted 版本。
- 同一 commit 的其他接受內容：`doc/brief/BRIEF-V2.md`（sha256 `27f08b25…3b38`）、`CONTEXT.md`（`4a0ce108…b2c2`，見 B-6）。V1 的 `BRIEF.md`（`b0f68a90…5bec`）、`SPEC.md`（`ed21e324…2ab0`）、`tickets.md` 在 `d7f02d4` 沒有改動（`git show --stat d7f02d4` 只有五個檔案）。
- 依賴（已核對三處一致：`tickets-v2.md`、各票 Blocked by、run record D8-e）：`#74 → {#75, #76} → #77 → #78`；並行度 1，執行順序 #74、#75、#76、#77、#78。

## 4. Boundary determination

**總判定**：Spec V2 rev 2 與 #74–#78 除 B-13 以外都在已接受的 V2 Outcome Contract boundary 內，沒有改變 accepted 語義。B-13 我無法確立在 boundary 內，該路徑 fail-closed 至 acceptor（F-1）。

| # | 項目 | 判定 | 依據 |
| --- | --- | --- | --- |
| B-1 | Spec V2 整體與 V1 的關係 | 在 boundary 內。Spec 自限「只能在 Brief V2 §3.5 四項覆寫內與 rev 5 不同」；我逐項核對它偏離 V1 之處：主要交付（覆寫 1）、請求隔離與靜態掃描例外（覆寫 2）、Submission package（覆寫 3）、>13（覆寫 4）。其餘新增內容（Exploratory run、下拉、50 Startups）是 Brief V2 §3–§8 的增量，不改 V1 語義 | Brief V2 §3.5；OC §5.1 第 5 點 |
| B-2 | 請求隔離與 `offline_scan` 的單檔 `fetch(` 例外；因此修改 `hw2/offline_scan.py` 與新增掃描案例 | 在 boundary 內。`offline_scan` 是 dashboard 的靜態檢查工具，不屬「Python 分析套件的正式路徑」；Spec 與 #76 明定要延伸它。例外只限一個檔案、只限 `fetch(`（I-2） | Brief V2 §5.6、Q14；Spec「離線與請求隔離」；seam (3) |
| B-3 | 非阻塞、取消（`CANCELLED`）、資源保護、可重現性的確定／非確定部分 | 在 boundary 內：acceptor 的 Spec Review（SR-V2-03、SR-V2-04）與 Tickets Review 調整 B 已接受 | Spec rev 2 Further Notes；`tickets-v2.md` |
| B-4 | 通用 Python 參照是單元內的新模組，只供測試；正式路徑不 import 它 | 在 boundary 內 | Spec「通用 Python 參照」；Brief V2 §8 數值驗證 |
| B-5 | 50 Startups 複製進 `assets/`（JS 全域內嵌＋保留 `.csv`），記錄來源、日期、sha256、授權 | 在 boundary 內，附 I-3（授權標示的正確做法） | Brief V2 §3.2（Q12）、§6 |
| B-6 | `CONTEXT.md` 在 `d7f02d4` 的修改（新增 Problem、Formal analysis、Exploratory run；改寫 Dashboard、Submission package；SRC-4） | 在 boundary 內：逐條與 Brief V2 §1、§3.5、§4、§5.6 相符，沒有 Brief V2 以外的語義；Brief V2 檔頭明載這些詞已登錄。OC §5 表沒有逐名列出 `CONTEXT.md`，但它是被接受的 Brief V2 引用的詞彙表，且在接受的 commit 內。兩者不一致時以 Brief V2 為準 | Brief V2 檔頭、§13 末「CONTEXT.md 一致性檢查」；F-4 |
| B-7 | SRC-4 加入 `doc/requirement/`（RB-5 範圍內的檔案） | 已在接受基準 commit 內，由 acceptor 提供（Brief V2 Q1）並隨 `d7f02d4` 一併接受。之後 `doc/requirement/` 仍唯讀 | Bindings §2.2、RB-5；Brief V2 §2 |
| B-8 | 特徵數敘述：README 由「10–20」改為「>13」；報告第 1.2 節（引用 SRC-1／SRC-2T 原文與交集規則）不改 | 在 boundary 內：Brief V2 §2 只要求 README／glossary 更正；#78 要求正式章節不變；King County 19 個 source features 符合 >13。glossary 目前沒有「10–20」字樣，不需修改 | Brief V2 §2 差異表；#78 AC |
| B-9 | 使用者以「自訂資料集」載入 King County CSV（或任何資料）時的探索 test 指標 | 在 boundary 內，**不是** Test evaluation：依 accepted 定義，Exploratory run「is never a test evaluation」，它使用自己的逐列切分，不讀正式 holdout、不評估正式模型。不得為此新增拒絕條件（那會是新的 AC）。對應的約束是探索程式**完全不讀** `model_data`（A-3 V2） | `CONTEXT.md` Exploratory run；Brief V2 §5.6(3)(4)；V1 BR-01／CC-1 |
| B-10 | GitHub Pages URL 上的檢查（Brief V2 §8 第 3 條的「於 Pages 上」、§3.2「Pages 與 ZIP 一致」、§14 P0「Pages 可正常存取」）移到合併後的 Lightweight work item；#78 記 NOT TESTED（pending merge） | 在 boundary 內：`tickets-v2.md` 的驗收覆蓋表與「尚未解決的風險」明載此安排，acceptor 已接受；與 V1 AD-3 相同。該 item 是 tracked item：合併後須有 acceptor 的直接指示作為其 Outcome Contract 才能執行（治理 §1.2；Bindings §4 第 4 列），並需 independent audit（第 7.5 節） | `tickets-v2.md`；OC §4 AD-3 |
| B-11 | #76 AC「在 GitHub Pages 環境載入並顯示結果」 | 在 boundary 內，依 I-1 解讀：合併前以 `http://localhost` 靜態伺服器重現並標明；Pages 本身屬 B-10 | #76 結案證據段；`tickets-v2.md` 覆蓋表第 3 條 |
| B-12 | 自訂 URL 的「一次讀取」遇到 HTTP 重新導向、CORS preflight | 嚴格讀法在 boundary 內；跟隨重新導向我無法確立在 boundary 內 → D-1 採嚴格讀法 | Brief V2 §5.6 第 2 條；Spec「載入契約」入口 |
| B-13 | **既有測試 `tests/test_dashboard_static.py::test_page_loads_data_as_a_js_global_and_the_bundled_chartjs` 斷言 `index.html` 的 `<script src>` 清單「等於」V1 的四個檔案**；V2 必須在頁面載入新模組（內嵌資料、載入模組、引擎、V2 UI 與繪圖） | **無法確立在 boundary 內，fail-closed 至 acceptor（F-1）** | 見第 9 節 F-1 |
| B-14 | 來自使用者資料的字串（欄名、類別層級、檔名、URL、HTTP 狀態文字、含輸入的錯誤訊息）只能當作資料呈現 | 在 boundary 內：這是 accepted 隔離不變量對「任意輸入」必然成立的條件，不是新需求 → D-2 | Brief V2 §3.1「任意輸入」、§5.6 第 2、3 條；Spec「King County 不變」 |

**逐票判定**（每張票的 What to build 與 AC 只引用 Spec V2 rev 2 與 Brief V2；我逐條比對過）：

| 票 | 判定 | 說明 |
| --- | --- | --- |
| #74 | 在 boundary 內，**F-1 路徑除外** | 下拉、內嵌資料、載入契約、三層邊界、All-in 鏈、即時預測器、mock fetch 前四條、V2 獨立繪圖（調整 A）都對應 Spec；「既有全部 pytest 與 Node 測試通過」與共同條款「既有測試全部不變」在加入 `<script src>` 後無法同時成立（F-1） |
| #75 | 在 boundary 內 | 四種方法、winner 規則、A-1～A-3、聚合與凍結、King County 一致性、50 Startups 全部 k 有效由 fixture 證明 |
| #76 | 在 boundary 內，附 I-1、I-2、D-1、D-2 | URL／檔案輸入、目標欄、失敗訊息、mock fetch 第五條、單檔例外、三向切換、不儲存 |
| #77 | 在 boundary 內，附 G-3、G-4 | 預算與略過、失敗隔離、取消於下一個候選邊界（調整 B）、不並行、可重現性、非阻塞以 UI 實際可操作為準 |
| #78 | 在 boundary 內，附 I-4、B-8、B-10 | README、報告探索章節、ACCEPTANCE V2、OV-1／SR-09 重做、ZIP；Pages 記 NOT TESTED |

## 5. Acceptance boundary 的分配

### 5.1 分配原則

- **V2 的 acceptance boundary**（OC §5：Brief V2 rev 2 的驗收意圖，含 §8 第 1～9、2a 條與數值驗證定義、§5.6 隔離、§7 交付物、§3.5 覆寫；Spec V2 rev 2 的 Testing Decisions 與人工檢查表；四個 seams；依賴；V1 保持要求）**全部分配給 Spec V2 rev 2**，由 #74–#78 承接。
- V1 的 acceptance boundary 仍由 Spec rev 5 承擔（`derivation-SPEC.md` §4；phase accepted 2026-10-19；AD-3 的 Pages 項目已在合併後處理）。V2 對 V1 條款的覆寫（BR-04／OV-1 的「零對外請求」改為 §5.6 四條、主要交付、Submission package、>13）由 Spec V2 承擔其新版本的驗收。
- **合起來的覆蓋**：Spec V2 是同一 Outcome Contract 檔案中最後一份未結的 Spec。它的 Spec Integration Audit 依治理 §4.7 須核對：V1 boundary 依 V1 phase acceptance 紀錄已覆蓋；V2 boundary 依本節覆蓋；V1 保持要求在整合 subject 上成立。

### 5.2 覆蓋核對

我逐列核對 `tickets-v2.md`「驗收覆蓋」表與各票 AC，表內的分配正確。下列是表中沒有、但 Spec V2 或 Brief V2 明列的項目；它們已在 accepted 契約內，**由本紀錄分配**（治理 §1.2 的 allocation；不新增 AC，不修改票文；各票「本票沒有提到的事項以 Spec V2 為準」使它們有約束力）：

| ID | 項目（來源） | 分配 | 驗證方式 |
| --- | --- | --- | --- |
| G-1 | UI 揭露逐列切分的限制：重複列、同一實體多筆、時間相依可能洩漏；探索結果不代表正式研究結論（Spec「切分與交叉驗證」末條、US-37；Brief V2 §5.3） | #75（探索區塊的「方法與限制」並列說明處）；README／報告的揭露已在 #78 | #75 R1 核對文字存在且位於探索區塊；#78 彙整進 ACCEPTANCE 的 V2 條目「探索標示」證據 |
| G-2 | 主 seam 的 (d) 小型邊界案例：恰好 20 列、單一類別欄、全部數值（Spec Testing「主 seam」資料 (d)） | #74（All-in 與載入）；#75（四種方法在 (d) 上的狀態與結果） | Node 對 Python 參照 |
| G-3 | 跨瀏覽器的可重現性比較：以相對 1e-9 比較確定部分並記錄（Spec「可重現性」契約） | #77 | 記錄（Chrome 與 Edge 各一次 50 Startups 的確定部分比較）；不是 gate；沒有第二個瀏覽器時記 NOT TESTED，不得記 PASS（與 AD-1 OV-3 的處理一致） |
| G-4 | 50 Startups 在 `file://`、斷網下五種方法都完成（Brief V2 §8 第 2 條；§6「必須能離線完成分析」）——在**最終的**預算常數下也必須成立 | #77（以最終預算常數對 50 Startups 執行，任何方法都不是 `SKIPPED_RESOURCE_LIMIT`，候選狀態與 #75 的 fixture 相同）；#78（OV-1 重做時確認五種方法都有結果） | Node 測試（使用正式預算常數）；ACCEPTANCE |
| G-5 | 從 King County 切回 50 Startups 時重新執行；切回自訂資料集時要求重新提交（Spec「Problem 與頁面結構」切換行為） | #76（三向切換的人工檢查一併執行） | 人工檢查表 |

### 5.3 不由本 run 承擔的部分（不是分配缺口）

| 項目 | 處理 | Authority |
| --- | --- | --- |
| Pages URL 上的檢查（B-10） | 合併後的 Lightweight work item；#78、Spec Integration Audit 與 phase acceptance 列為 open item | acceptor 指示後執行 |
| 合併進 `main` | RB-1（OC §5 沒有 SA-3 opt-in） | acceptor |
| Push | run designation 選項 (a)：每張票 audit closure 後逐次取得授權 | acceptor |
| iLearning 繳交（Submission package：repository URL＋Pages URL＋ZIP） | RB-2 | acceptor |
| 向老師確認「兩種 problem」（Brief V2 §9） | 可選，不是完成條件 | acceptor |

除上列各項，Brief V2 §3 的必要項目、§8 的每一條與 Spec V2 rev 2 的每一節都至少分配到一張票；沒有造成歧義的重疊。

## 6. Lane determination（V2）

- **問題**：V2 Enhance 的整體工作走 Lightweight 還是 Formal？
- **裁決**：**Formal**（Spec＋Tickets＋Orchestrator），沿用既有 run `run-20261022-hw2-v2-enhance`。
- **理由**（依整體結果判定，治理 §3.3）：
  1. 治理 §3.6-C 成立：五個相依的 execution units（`#74 → {#75, #76} → #77 → #78`），涉及引擎、Python 參照、UI、文件與打包，預期跨多個 Executor／Reviewer session。
  2. 治理 §3.6-B 成立：`LoadResult` 與 `ExploratoryResult` 結果契約、三層前處理邊界、候選狀態枚舉、`offline_scan` 的例外規則，都是其他票依賴、先前沒有 accepted baseline 的新介面、invariant 與 gate。
  3. Lightweight 不適用；不得把它拆成多個 Lightweight 指示（治理 §3.3；Bindings §4）。
- **配置**：

| 項目 | 內容 |
| --- | --- |
| Spec | 一份：Spec V2 rev 2（本紀錄） |
| Orchestrator | 既有 designation（run record §1）；`claude-opus-5-5`／`medium`，E-OR 依 Bindings §3.2 |
| Executor | `gov-executor`（O-1），fallback `gov-executor-fallback` |
| Audit | 每張票 independent audit（R1／R2／一次 Alternate／FA）；**另做 Spec V2 的 Spec Integration Audit**，subject 為 #78 結案時的整合狀態；有五張票，**不適用**單 Ticket fast path（Bindings §5） |
| Phase acceptance | DA，必須引用已 closure 的 Spec Integration Audit record；Pages 檢查列為 open item（B-10） |
| 合併 | RB-1；N-10：PR checks 不是條件 |
| 合併後的 Pages 檢查 | Lightweight work item（Bindings §4 第 4 列），audit 必要（第 7.5 節） |

- **是否改變 accepted 語義**：否。

## 7. 高風險類別與 assurance 要求（V2）

### 7.1 問題與裁決

- **問題**：V2 適用哪些高風險類別、需要哪些 assurance？特別是使用者提供 URL 的 fetch 能力（以及 `offline_scan` 的 `fetch` 例外）。依 acceptor 指示，不預設低風險。
- **裁決**：V1 的 **H-1～H-4 全部沿用並擴充涵蓋範圍到 V2**；另新增 **H-5「使用者提供的資料來源與網路請求邊界」**。這是 Bindings §5「每份作業第一次正式 audit 或 Formal activation 前，由 DA 確認或修改」的類別決定（`home_work_01` 新增 H-3 是先例），不是新的治理規則、gate 或角色。
- **效果只有既有機制**：(a) 該類別的 blocking finding，Final Adjudicator 不得單獨 defer，須有 DA 確認（治理 §4.5；A-7）；(b) Lightweight 工作觸及時觸發 audit（Bindings §5）；(c) 第 7.3 節的核對內容在**既有**的 R1／R2／Spec Integration Audit 內執行，不新增 audit round、seam 或 acceptor gate。類別不作為 capability escalation trigger（Bindings §3.2、§5；A-8）。
- **適用範圍**：本紀錄適用 V2（Spec V2 與 #74–#78、其 Spec Integration Audit、phase acceptance、合併後的 V2 Lightweight items）。`decision-20261018-high-risk-categories.md` 的 H-1～H-4 定義與 A-1～A-8 不變；本節只增列 V2 的涵蓋範圍與 H-5。

### 7.2 類別

**H-1 憑證、機密與不得公開的資料**（沿用）。V2 增列涵蓋：URL 讀取不帶憑證（`credentials: 'omit'`）、沒有任何 API key（RB-3）；使用者提供的 URL 與資料內容不進入追蹤檔案、worklog、audit、run、ACCEPTANCE 或 evidence——只允許老師公開的範例 URL 與 synthetic／公開 fixture。學號規則（BR-03）與 `.local/packaging.json` 照舊（A-4；S-1～S-6）。觸及：全部票（任何 commit；#78 的 ZIP）。

**H-2 老師指定的名稱與格式，以及課堂口頭要求的交付**（沿用）。V2 增列涵蓋：加分 +1（下拉呈現兩種 problem）與 +2（可任意輸入 Dataset，含老師範例 URL）；SRC-4 的主要繳交「github and web」（Pages URL、README「作業要求對應」的兩列）；>13 敘述；`file://` 完全離線（OV-1）在 King County 與 50 Startups 上的保持；請求隔離作為 BR-04 的 V2 版本；`offline_scan` 規則；ZIP 內容。觸及規則沿用 `decision-20261018-issue60-a4-student-id.md` §2.2（任何修改 dashboard 靜態檔、README、報告、打包者）→ 全部票。

**H-3 評估完整性**（沿用）。V2 增列涵蓋：
- (i) **正式分析不變**：`model_data`、結果檔、Test evaluation 紀錄、V1 區塊與 V1 腳本不變；不重跑 notebook、不做新的 Test evaluation；探索程式不讀 `model_data`（B-9）。
- (ii) **探索評估的完整性**：三層前處理邊界（SR-V2-01）、fold-internal selection、CV 聚合、winner 凍結後才讀 test、test 只對 winner（SR-V2-02）、PI 公式、A-1～A-3 語義、`SKIPPED_RESOURCE_LIMIT`／`FAILED`／`CANCELLED` 永遠不產生 winner、test 或預測、Python 參照獨立於 JS、Node 對 Python 的容忍度、可重現性的確定部分。這些錯誤不會讓程式失敗，只會讓結果看起來正確。
- (iii) 報告與 README 不含探索結果的數字（I-4）。
觸及：全部票。

**H-4 證據真實性與如實標示**（沿用）。V2 增列涵蓋：ACCEPTANCE V2 條目的狀態與證據（含 Pages 的 NOT TESTED、best-effort 項目）；執行時間、預算常數與載入上限的實測紀錄；「50 Startups 全部 k 有效」不成立時如實記錄；截圖標明環境（`file://`、`http://localhost`、Pages）；50 Startups 的來源、取得日期、sha256、授權的可追溯性（I-3）；scope class 標示（I-4）。觸及：全部票（每張票都填寫 ACCEPTANCE 條目）。

**H-5 使用者提供的資料來源與網路請求邊界（新增）**

| 項目 | 內容 |
| --- | --- |
| 風險 | (a) **請求邊界**：頁面在使用者未提交時發出請求、一次提交發出多個請求（重試、重新導向、preflight、第二個 API）、或 `offline_scan` 的例外被放寬到第二個檔案或第二種網路 API。(b) **不受信任的內容**：任意第三方的 CSV 文字與 URL 字串進入公開的頁面；若被當成 HTML、script、style 或要載入的 URL，就能在 `yotsubamomo.github.io` 這個由本 repo 全部單元共用的 origin 上執行程式，繞過隔離（再發請求）並竄改 King County 區塊的顯示。(c) **持久化**：URL 或內容被寫入任何儲存。(d) **資源**：過大或過慢的輸入讓頁面卡死或影響 King County |
| 為何是高風險 | 使用良性 fixture 的測試全部通過時，漏洞仍然存在，錯誤是靜默的；頁面公開發布，老師會實際貼入 URL；H-1～H-4 都沒有涵蓋「不受信任的外部輸入」這個風險機制（H-1 是機密外洩，H-2 是名稱與格式，H-3 是統計評估，H-4 是紀錄真實性） |
| 涵蓋 | 探索載入模組與其 `fetch` 呼叫；URL 輸入與檔案選擇；把輸入衍生字串寫入 DOM 的全部程式（欄位清單、排除清單、類別下拉、預測器輸入、診斷、圖表標籤、錯誤訊息）；`hw2/offline_scan.py` 的規則與例外；mock fetch 測試；不儲存的保證；資源保護與取消 |
| 觸及的工作 | #74（載入契約、欄名與層級的呈現、mock fetch 前四條）、#75（診斷與圖表中的 group／欄名）、#76（fetch、輸入面板、錯誤訊息、掃描例外）、#77（資源保護、不並行、取消）、#78（OV-1 重做、最終掃描、ZIP） |

### 7.3 Assurance 要求

A-1、A-4、A-6、A-7、A-8 **原文沿用**（`decision-20261018-high-risk-categories.md` §3）。A-2、A-3、A-5 依下列 V2 讀法適用；A-9 新增於 H-5。全部在既有 audit 內執行。

| # | 要求 | 適用範圍 |
| --- | --- | --- |
| A-1 | （沿用）R1 audit record 對觸及的每個類別（含 H-5）各有一節：核對內容與結果；R2 重述修正結果；不新增 round | 全部票 |
| A-2（V2） | H-3：Reviewer **自己執行** pytest 與 Node 測試，包括三層邊界、聚合與凍結、King County 一致性、取消／失敗／略過、可重現性；並依結果契約不變量，至少對一個 winner 的逐筆 PI 與 coverage 自行重算；自行比對報告與 README 中沒有探索結果數字 | 觸及 H-3 的票；Spec Integration Audit |
| A-3（V2） | H-3 正式分析不變：對照接受基準 `d7f02d4`，核對 `assets/app.js` sha256 `c1ab3f21cd9cc324ad820c46621c985bf8728a511d6db9a7f286fd7e57c982ad`、`assets/hw2core.js` `e75c5d48b84031ebfcb01bcd41ef6dfa84ba3edf3d5f6a554f97e67b3af22c14`、`assets/model_data.js` `6cf0c11eec941c210a263bceaed7deede482181f99d74cae933f872d09c3a7ac`、`results/model_data.json` `69dc1465ac5f2b067056aa4690fe607876761d9e0f340a0eccb9f37afcc18e61` 不變；`git diff d7f02d4 <subject> -- home_work_02/results home_work_02/hw2.ipynb` 為空；既有 `hw2/` 模組除 `offline_scan.py`（#76）外不變，若有其他修改須在 worklog 說明它不在正式分析路徑上並由 Reviewer 判定；Test evaluation 紀錄（run designation 第 4 點的 `fe76019b…`／`b53ff286…`）不變；探索相關檔案不含對 `MODEL_DATA`、`model_data`、`test_inputs` 的任何引用 | 全部票；Spec Integration Audit |
| A-4 | （沿用）H-1 學號與材料核對（S-1～S-6）；另核對追蹤檔案與紀錄中沒有老師範例以外的使用者 URL 或資料內容 | 全部票；合併前 |
| A-5（V2） | H-4：ACCEPTANCE 狀態與證據逐條相符，沒有證據者不得 PASS；50 Startups 的 sha256 由 Reviewer 從 git blob（`git show <subject>:<path>`）重算並與紀錄值、內嵌文字相符；授權陳述可追溯到來源 repo 的 LICENSE（I-3）；截圖的環境標示正確；scope class 標示（I-4）；#78 另核對 ChatGPT PDF 與 NotebookLM 材料的 sha256 照舊 | 全部票；Spec Integration Audit |
| A-6 | （沿用）H-2／OV-1：Spec Integration Audit 核對 ZIP 檔名、內容與 sha256，解壓後斷網 `file://` 下拉與 50 Startups 可用、零對外請求、靜態掃描 | Spec Integration Audit |
| A-7 | （沿用）H-1～H-5 的 blocking finding 由 FA defer 時須有 DA 確認 | 全部 |
| A-8 | （沿用）不宣告 model diversity；類別不作 escalation trigger | 全部 |
| **A-9** | **H-5**：Reviewer 自行列舉 V2 檔案中所有 DOM 寫入點與可發出請求或執行字串的 API（例如 `innerHTML`、`outerHTML`、`insertAdjacentHTML`、`document.write`、`DOMParser`、`createContextualFragment`、`srcdoc`、`eval`、`new Function`、字串型 `setTimeout`／`setInterval`、`import(`、`Worker`、`importScripts`、`fetch`、`XMLHttpRequest`、`WebSocket`、`EventSource`、`sendBeacon`、對 `src`／`href`／`location` 的指派），確認輸入衍生字串只進入文字型寫入（D-2）；確認 `fetch` 只在探索載入模組、只由提交處理程序呼叫、選項符合 D-1；確認 `offline_scan` 的例外以單一檔案路徑與 `fetch(` 為鍵，其他規則（含 external-url）仍適用於該檔（I-2）；執行 mock fetch 測試；並在瀏覽器以本機檔案載入一份**刻意構造**的 CSV（欄名與類別值含 `<img src=x onerror=…>`、`</script>`、`javascript:` 等字串）做一次探測，確認全部以字面文字顯示、網路面板零請求、King County 區塊不變。探測是 R1 的證據，不是新的 test seam 或 AC；Executor 依治理 §3.5 在 self-verification 中驗證同一風險並記入 worklog | 觸及 H-5 的票（全部）；Spec Integration Audit |

### 7.4 逐票的類別與 assurance

| 票 | 類別 | Assurance | 本紀錄的票義務 |
| --- | --- | --- | --- |
| #74 | H-1、H-2、H-3、H-4、H-5 | A-1、A-2、A-3、A-4、A-5、A-9、A-7、A-8 | F-1（等 acceptor）；G-2；I-2、I-3、I-5；D-2 |
| #75 | H-1、H-2、H-3、H-4、H-5 | A-1、A-2、A-3、A-4、A-5、A-9、A-7、A-8 | G-1、G-2；D-2；I-5 |
| #76 | H-1、H-2、H-3、H-4、H-5 | A-1、A-2、A-3、A-4、A-5、A-9、A-7、A-8 | D-1、D-2；I-1、I-2、I-5；G-5 |
| #77 | H-1、H-2、H-3、H-4、H-5 | A-1、A-2、A-3、A-4、A-5、A-9、A-7、A-8 | G-3、G-4；D-1（新提交時每次提交至多一次讀取）；I-5 |
| #78 | H-1、H-2、H-3、H-4、H-5 | A-1、A-2、A-3、A-4、A-5、A-9、A-7、A-8 | I-4、I-5；G-4（OV-1 重做）；B-8、B-10 |
| Spec Integration Audit（Spec V2） | H-1～H-5 | A-2、A-3、A-4、A-5、A-6、A-9、A-7 | 第 5.1 節合起來的覆蓋；B-10 列為 open item |

### 7.5 Lightweight 的 audit 觸發（V2 增列）

`decision-20261018-high-risk-categories.md` §4 照舊，另加：修改探索載入模組、URL／檔案輸入、`fetch` 選項、輸入衍生字串的呈現、`offline_scan` 的規則或例外（H-5）；修改探索引擎、Python 參照或其測試（H-3）；合併後的 Pages 檢查 item（H-2、H-5；與 V1 AD-3 相同，需 audit）。無法判定時視為觸發；Executor 不得自行降級。

## 8. Decisions 與對票有約束力的解讀

### D-1 「對該 URL 的一次讀取」的範圍

- **問題**：Brief V2 §5.6 第 2 條與 Spec「載入契約」（「對該 URL 一次、GET、不重試、不帶憑證」）是否允許瀏覽器跟隨 HTTP 重新導向，或發出 CORS preflight？兩種讀法都會影響實作。
- **裁決**：採**嚴格讀法**——每次使用者提交，最多一個 HTTP 請求，且對象就是提交的 URL：
  1. 單一 `fetch` 呼叫，`GET`，`credentials: 'omit'`，**不跟隨重新導向**（`redirect: 'error'` 或等效作法）；重新導向的結果以既有的 `URL_FETCH_FAILED` 與既有子原因之一回報（不新增原因碼），並照常給出「下載後以檔案載入」的指引。
  2. 不設任何自訂 request header，使它是 CORS simple request、不觸發 preflight。
  3. 不重試；逾時以 abort 結束，不再發請求。新的使用者提交是新的一次讀取（#77 的「新提交先取消進行中的執行」不構成重試）。
  4. #76 的 mock fetch 第五條以呼叫的 init 參數驗證上列選項（這是現有 AC「恰發一次 GET，不重試、不帶憑證」的驗證細節，不是新 AC）。
- **理由**：嚴格讀法逐字符合 accepted 文字，也滿足全部 AC（老師的範例 URL 直接回應，沒有重新導向）；URL 失敗本來就是 accepted 的情境（Brief V2 §5.1、§10，以檔案載入為出路）。跟隨重新導向會讓頁面對使用者沒有提交的 URL 發出請求，我無法確立它在 boundary 內。若 acceptor 希望允許重新導向，屬 contract change（治理 §5.3）。
- **是否改變 accepted 語義**：否。**受影響**：#76（主要）、#77（第 3 點）。

### D-2 輸入衍生字串一律當作資料

- **問題**：Spec 沒有明寫使用者資料中的字串如何寫入頁面。
- **裁決**：來自 CSV（欄名、類別層級、儲存格值）、檔名、URL 字串、HTTP 狀態文字，以及含有這些字串的錯誤訊息，只能經由文字型 API 寫入 DOM（例如 `textContent`、`createTextNode`、非 URL 屬性的 `setAttribute`、`<option>` 的 `text`），不得被解讀為 HTML、script、CSS 或要載入的 URL，也不得傳給任何會執行字串的 API。數值解析只做字面數字判定，不求值運算式。圖表標籤經由繪圖函式庫的文字選項傳入。
- **理由**：Brief V2 §5.6 的「唯一允許的對外請求」與「King County 數字不變」必須對**任意**輸入成立（+2 的條件就是任意輸入）；只要輸入能成為 markup，兩條都可被一份 CSV 打破。這是 accepted 不變量的必要條件，不是新需求（B-14）。
- **是否改變 accepted 語義**：否。**受影響**：#74、#75、#76、#77；A-9。

### 對票文字的解讀與分配

| # | 對象 | 解讀 |
| --- | --- | --- |
| I-1 | #76 AC「在 GitHub Pages 環境載入並顯示結果」 | 合併前以 `http://localhost` 的靜態伺服器（http origin，與 Pages 同一種瀏覽器安全模型，不是 `file://`）重現，截圖與 ACCEPTANCE 明確標示環境；Pages URL 本身屬合併後的 item（B-10）。不得把 localhost 的結果記為 Pages PASS |
| I-2 | 靜態掃描的例外與來源 URL 的記錄位置（Spec「離線與請求隔離」「既有規則不變」） | 唯一新增的例外是「探索載入模組這一個檔案可出現 `fetch(`」，以該檔路徑為鍵。不得擴充 `ALLOWED_DATA_URLS`、`DATA_FILES` 或新增其他例外；探索載入模組本身仍受 external-url 等規則約束，不得寫死任何 URL（包括老師的範例 URL 作為預設值）。50 Startups 的來源 URL 記在 README、ACCEPTANCE 或掃描範圍外的說明檔；在頁面上只能以 `<a href>` 超連結出現（既有規則 (a) 允許） |
| I-3 | #74「記錄來源 URL、取得日期、sha256、MIT 授權」；Brief V2 §6「標示來源 repo 與 MIT 授權」 | 複製的 CSV 隨附來源 repo 的 MIT 著作權與許可聲明（例如與 CSV 同目錄的授權說明檔，與 V1 的 `chart.js.LICENSE.md` 相同做法），使 Pages 與 ZIP 中的副本符合 MIT 的保留聲明條件。陳述只寫可查證的事實：「取自 `Avik-Jain/100-Days-Of-ML-Code`（該 repo 以 MIT 授權發布）」，不宣稱資料的原始出處。我查得的事實（Executor 取得時須自行重查並記錄）：GitHub API 回報該 repo 授權為 MIT（`LICENSE` blob `005423138e7fa4fb18de5ab6533da00a09961731`）；最近一次修改 `datasets/50_Startups.csv` 的 commit 為 `5cd8936afb3aab9e7029ce21413cb32766153a74`。位元固定的新資料檔應避免 checkout 的換行轉換，否則 sha256 會因環境而不同（HOW） |
| I-4 | #78 報告「探索模式」章節與 README 的加分對應表 | 章節**不含任何探索結果數字**（包括 50 Startups 的指標、k、係數），只有方法、差異、限制與揭露；可引用的數字限於匯出結果與探索模式的靜態設定（載入上限、預算常數，經由建置流程帶入，不手抄）。章節標題帶既有的三種 scope 標示之一。+1、+2 標為老師要求（SRC-4 加分）；「兩種 problem＝同頁下拉切換兩個資料集」是 acceptor 的解讀（Brief V2 §3.2「老師原文未進一步定義」），探索能力集合是 acceptor 的決定，兩者都不得寫成老師的要求（Bindings §2.4；V1 的三種標示規則照舊） |
| I-5 | 共同條款「既有測試全部不變」（F-1 路徑以外） | 除 F-1 所指的那一個斷言（待 acceptor 決定）以外，既有測試檔逐位元不變。V2 的 DOM 子樹與檔案配置必須讓既有以區段切片斷言的測試（例如 `id="methods"` 區段到 `</main>` 恰有四個 `<article>`、`kchart-card` 到 `compare-card` 的內容）在不修改的情況下繼續成立 |

## 9. Findings

| ID | 嚴重度 | 內容 | Routing／需要的決定 |
| --- | --- | --- | --- |
| **F-1** | **High（boundary；fail-closed）** | `tests/test_dashboard_static.py` 第 24–30 行的 `test_page_loads_data_as_a_js_global_and_the_bundled_chartjs` 斷言 `re.findall(r'<script\s+src="([^"]+)"', html) == ["assets/vendor/chart.umd.js", "assets/model_data.js", "assets/hw2core.js", "assets/app.js"]`。Spec V2 要求同一頁面載入新的模組（內嵌 50 Startups、探索載入模組、引擎、V2 UI 與繪圖），而 V1 腳本與 `model_data.js` 都以 sha256 鎖定、不能代為載入。另一方面，票的共同條款（acceptor 接受）與 run designation 第 4 點（違反即停止）都寫「既有測試全部不變」，#74 AC 要求「既有全部 pytest 與 Node 測試通過」。兩項 accepted 要求在這一點上不能同時成立。Spec V2 本身只要求列名的幾類既有靜態測試「照跑」，沒有列入這一條；但票與 designation 的文字是逐字的不變量。我無法確立「修改這條斷言」在 boundary 內；以重排屬性、內嵌整個引擎或執行期注入 `<script>` 等方式讓斷言不再看到新腳本，等於規避該不變量的目的，**也不在 boundary 內** | **Acceptor**（治理 §1.2、§5.3 第 1 類）。受影響路徑：#74 在 `index.html` 加入 V2 腳本、以及 #74 的結案；其依賴 #75–#78 的結案。其餘不預判此決定的工作（載入契約、引擎、Python 參照、Node 與 pytest 新測試）可以先做（治理 §1.5）。選項：(a)〔DA 建議〕授權只修改這一條斷言：前四個 `<script src>` 必須仍是 V1 的四個檔案、順序不變，其後**逐一列出** V2 的腳本（比現況更嚴格），其他既有測試不變；修改在 #74 R1 以 H-2 核對。(b) 維持測試逐位元不變——我找不到不規避斷言的合法做法，不建議 |
| F-2 | Low | 第 5.2 節 G-1～G-5：Spec／Brief 明列、但票的 AC 與 `tickets-v2.md` 覆蓋表沒有點名的項目 | 已由本紀錄分配，不需 acceptor 決定；不修改票文。列出以便 Orchestrator 與 Reviewer 引用 |
| F-3 | Low | 接受基準中的狀態文字已過時：Spec V2 檔頭「下一步 `/to-tickets` 尚未授權」、「GitHub Issue … 待 acceptor 審查」；`tickets-v2.md`「尚未授權：實作、commit、push、merge」 | 不影響語義：現行授權以 OC §5.1 為準。因接受基準不得替換，不建議修改；acceptor 若要更新，屬 accepted 內容的編輯，由 acceptor 決定 |
| F-4 | Low | OC §5 表的「接受的內容」沒有逐名列出 `CONTEXT.md`，但 `d7f02d4` 修改了它 | DA 判定在 boundary 內（B-6）。不需決定；acceptor 若要明確納入，可在下一次紀錄時說明 |
| F-5 | Low（觀察，給 Executor 的 HOW 提示，非約束） | 既有 `tests/test_report.py::test_template_has_no_hand_typed_result_numbers` 禁止報告模板出現手打數字；探索章節若需提到上限或預算，須經建置流程的 placeholder 帶入（I-4）。新增的位元固定資料檔需要避免換行轉換（I-3） | 無需決定；Executor self-verification 與 Reviewer 照常處理 |

## 10. 是否改變 accepted 語義

否。本紀錄只作 boundary determination、分配、lane、高風險分類與 assurance、對票的解讀，以及 D-1（採 accepted 文字的嚴格讀法）、D-2（accepted 不變量的必要條件）。H-5 是 DA 的分類決定（治理 §5.1），只啟動既有機制。唯一可能改變 accepted 語義的事項 F-1 **沒有裁決**，交 acceptor。

## 11. 受影響的工作

- **#73（Spec V2）、#74–#78**：內容不變；本紀錄是它們的 derivation。各票的類別與 assurance 依第 7.4 節，義務依第 5.2、8 節。
- **#74**：F-1 路徑等待 acceptor；其他部分可依 run 的安排進行。
- **Run record**：缺口 O-2 由本紀錄填補（lane、高風險、derivation），附 F-1 的 fail-closed 路徑；是否據此派 #74 由 Orchestrator 依 orch-default §3 與 OC §5.1 判斷。
- **Spec Integration Audit（Spec V2）與 DA phase acceptance**：依第 5.1、6、7.4 節；B-10 列為 open item。
- **V1**：Spec rev 5、`tickets.md`、#59–#67、`derivation-SPEC.md`、`decision-20261018-high-risk-categories.md` 不修改；後者對 V1 仍有效，本紀錄只對 V2 增列。
- **合併後的 Pages 檢查**：tracked item，等 acceptor 合併並給予直接指示。

## 12. Evidence

- 讀取：Bindings b5 全文；治理 v2.2 §1.2、§1.5、§2.1、§2.4–§2.7、§3.1、§3.3–§3.6、§4.1–§4.7、§5.1–§5.4；orch-default v2.2 §12；`outcome-contract.md`（HEAD `4eb03e6`，含 §5.1 原文）；run record `run-20261022-hw2-v2-enhance.md`；`d7f02d4` 的 `BRIEF-V2.md`、`SPEC-V2.md`、`tickets-v2.md`、`CONTEXT.md`、`doc/requirement/HW2-req_new-20261021.txt`；V1 的 `derivation-SPEC.md`、`decision-20261018-lane.md`、`decision-20261018-high-risk-categories.md`、`decision-20261018-issue60-a4-student-id.md` §2、`decision-20261019-phase-acceptance-SPEC.md`、`decision-20261019-post-merge-ad3-readme.md`（開頭）。
- `gh issue view 73..78`（body、狀態、label、時間）；GraphQL `userContentEdits`、`lastEditedAt`、`comments`；body 的 sha256；`diff` SPEC-V2.md 與 #73 body。
- `git show --stat d7f02d4`、`git log d7f02d4..HEAD`、`git diff --stat d7f02d4 HEAD`、`git diff 392e9df d7f02d4 -- home_work_02/CONTEXT.md`；第 3、7.3 節所列檔案在 `d7f02d4` 的 sha256。
- Repo 事實：`hw2/offline_scan.py`（規則與 `ALLOWED_DATA_URLS`、`DATA_FILES`）；`tests/test_dashboard_static.py`（第 16–30、106–200 行）；`tests/test_report.py`（第 60–145、201–253 行）；`tests/test_package.py`（第 120–146 行）；`tests/test_repo_hygiene.py`（第 50–70 行）；`.gitattributes`；`hw2/package.py`（以 `git ls-files` 決定打包內容）；`assets/app.js` 沒有 `innerHTML`；README 第 70 行的「10–20」；`report/report.md` 第 1.2 節。
- `gh api repos/Avik-Jain/100-Days-Of-ML-Code/license`、`…/commits?path=datasets/50_Startups.csv`（I-3）。
- 本 assignment 的 transcript binding（標頭）。
- 寫入的檔案只有本紀錄；沒有修改 Outcome Contract、Brief、Spec、`CONTEXT.md`、票、GitHub 或任何 V1 產物；沒有 commit。
