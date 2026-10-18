# Decision record — r4 衍生契約（Spec v1.1、Issues #50–#56）的處置

- **紀錄類型**：Design Authority decision record（boundary determination；治理 §1.2、§2.4、§5.3；Bindings b5 §7）
- **日期**：2026-10-18
- **派工**：無角色主 session 轉達的 DA assignment（2026-10-18），HEAD `8740a4a7`（branch `home_work_02-regrill`）
- **Binding**：`gov-design-authority`，`claude-opus-5-5`／`high`（Bindings §3.1 預設 mapping，沒有 escalation，沒有替代）。本紀錄不自證 binding，由派工者依 Bindings §3.6 核對 transcript 並記錄。
- **Capability escalation**：未提出。(D1) 不成立：三個問題都能以已接受的契約內容和 repo／tracker 事實裁決。(D2) 不成立：本單元在現行 Outcome Contract 下沒有先前的 DA 決定被推翻或有爭議。

## 1. 依據

| 來源 | 內容 |
| --- | --- |
| 現行 Outcome Contract | [`../outcome-contract.md`](../outcome-contract.md)：acceptor 2026-10-18 接受 `doc/brief/BRIEF.md`、Grill 紀錄 rev 7 與 `CONTEXT.md` 於 commit `dff7c55c` 的版本（§3.1 acceptor 原文） |
| 已接受內容中的明文 | `dff7c55c:home_work_02/doc/brief/HW2_Regrill_Brief_Draft_v0.1.md` 第 5 行：「先前的 Grill（G1–G8、C1–C5）、Outcome Contract r4、Spec v1.1 … 作為歷史參考。**本次 Grill 不沿用任何舊決定**，除非 acceptor 在本 Brief 中重新確認。」 |
| 被取代的契約 | branch `home_work_02-outcome-contract` 上的 OC r4（normative `e2153254`，接受紀錄 `370c0ae`）、Spec v1.1、`derivation-SPEC.md` §13–§14、`tickets.md` |
| Tracker 事實（2026-10-18 以 `gh` 讀取） | #50–#56 全部 OPEN，label 為 `ready-for-agent`，0 則 comment，最後更新 2026-10-14；body 的 Parent 指向 OC r4 與 Spec v1.1 |
| Repo 事實 | 所有 HW2 branch 上都沒有 `worklog/`、`run/`、`audit/`；沒有 HW2 PR；`home_work_02-rebaseline-oc-v2` 上的 OC v2 只是未接受的 DRAFT。上位契約轉寫檔 `HW2-requirements-Multiple Linear regression.txt` 目前的 sha256 是 `b01c6fb5…4b89`，r4 §2.1 固定的是 `a969e7e2…61ab`（老師 2026-10-18 更新了作業頁，另外新增 SRC-2T、SRC-3） |
| 現行 Spec | [`../../spec/SPEC.md`](../../spec/SPEC.md) rev 3（#59）；它的 Further Notes 已聲明「本 Spec 不沿用」#50–#56 |

## 2. 兩份 Spec 的關鍵語義對照

| 面向 | Spec v1.1（r4） | Spec rev 3（Brief @ `dff7c55c`） |
| --- | --- | --- |
| 分區 | 60／20／20 Fit／Calibration／Test（依 House） | 80／20 train／test（依 `id`） |
| CV 協定 | Nested：outer 5-fold 比較候選，inner 5-fold 選 k 與 alpha；選出一個 procedure 後凍結成單一 predictor | 單層分組 5-fold，fold-internal selection；四個路徑方法各有 k=1…18 的完整路徑；canonical subset；各方法 CV winner 加上整體 CV winner |
| 候選 | 5 個：`lr_all`、forward、backward、Ridge、Lasso；R-CAND-8 **禁止** p-value 方法；沒有 RFE，也沒有 Lasso top-k | Forward、Backward、RFE、Lasso top-k（路徑方法）加上 All-in baseline；Ridge／Lasso 為對照；p-value backward 為講義對照 |
| 標準化 | 所有非 one-hot 欄都標準化 | OLS 用原始尺度；只有 Ridge／Lasso 標準化 |
| 區間 | Split conformal（以 Calibration 校準 q̂，對稱的 log 分數） | 參數式 OLS PI（log 尺度，t 分佈）；conformal 明列在 Out of Scope |
| Test 使用 | 只對凍結的單一 predictor 評估一次 | 授權集合＝各方法 CV winner ∪ All-in ∪ 整體 CV winner（同一模型只評估一次），另加 Ridge／Lasso 的 metric-only |
| 交付物 | notebook、`mlr/`、報告 PDF、ZIP；**Web App 是 non-scope**，root `CONTEXT-MAP.md` 不修改 | 另外必須有 dashboard（Pages、`file://` 離線、`model_data` 契約、Node 測試）；root README 與 CONTEXT-MAP 各加一列（RB-5，先說明） |
| Git／合併授權 | SA-3 opt-in；HW2 第一個 PR 的一次性 RB-1 授權；C5 的 push 授權 | 沒有 SA-3 opt-in，合併屬 RB-1；目前不授權 push；`/to-tickets` 尚未授權 |

兩者在分區、選模協定、區間方法、Test 使用規則與交付物上互相排斥。它們不可能同時是同一單元、同一批交付物（`<學號>_hw2.zip` 等）的有效契約。

## 3. 判定

### (1) Spec v1.1 不是任何已接受 Outcome Contract 的有效 derived contract

- Derived contract 的接受與授權只來自它的 Outcome Contract（治理 §1.2）。Spec v1.1 唯一的來源是 OC r4。
- 現行 Outcome Contract 的已接受內容明文寫出不沿用 r4 與 Spec v1.1 的任何決定（第 1 節引文），而且 acceptor 接受的 Brief 對同一批交付物定義了互斥的語義（第 2 節）。所以 r4 已經不界定 HW2 之後的工作，Spec v1.1 也就失去了 authority 的來源。
- Spec v1.1 也不在現行 Outcome Contract 的 boundary 內：照它執行會產出 Brief 已排除或沒有授權的結果（conformal、60／20／20、nested CV 的單一凍結 predictor、沒有 dashboard）。DA 不能替它作出 in-boundary determination。
- 這個判定是限縮方向的（停止舊路徑），沒有新增或改變 accepted 語義，不是 contract change，也沒有重開 acceptor 在 Brief 中的任何決定。r4、Spec v1.1、它們的 derivation／decision records 與 `tickets.md` 留在原 branch 作為歷史，不修改、不刪除（依現行 OC 檔頭）。
- 若有人主張 r4 與現行契約同時有效，那是 Outcome Contract 本身的接受問題，屬 acceptor（治理 §1.5 第 1 項）。在 acceptor 決定之前，依 r4 的工作一律 fail-closed，不得執行。

### (2) #50–#56：移除 `ready-for-agent`、加上 `wontfix`、以 not planned 關閉，並留下 pointer comment

理由：

- **不能維持現狀**：OPEN 加上 `ready-for-agent`，代表「規格完整、可由 AFK agent 執行」。這些票的 Parent 是已失效的契約，執行它們就是在 boundary 外工作；body 引用的 OC §4.2／§9 授權（SA-3、一次性 RB-1）在現行契約下也不存在。
- **不採用「保持 open、只改 label」**：open 的 issue 代表還有待辦。這七張票沒有任何可以接續的狀態（沒有 worklog、audit、PR 或 branch），保持 open 只會讓 `/to-tickets` 和 Orchestrator 同時面對兩套票。
- **不改寫成新票**：body 是 OC r4 衍生契約的持久紀錄，舊 `derivation-SPEC.md` §13 以編號引用它們。改寫會讓歷史紀錄指向不同的內容，並把兩份契約的 traceability 混在同一個 ID 上（治理 §1.2 對持久紀錄的要求；§3.6 不藉換 ID 改寫歷史）。新票由 Spec rev 3 另外 derive，用新的編號開立。
- 關閉是可逆的 tracker 操作，不刪除任何紀錄。

建議的 GitHub 操作（七張相同，`<n>` ∈ {50, 51, 52, 53, 54, 55, 56}）：

```bash
gh issue edit <n> --repo yotsubamomo/aiot-classwork --remove-label ready-for-agent --add-label wontfix
gh issue comment <n> --repo yotsubamomo/aiot-classwork --body-file <存放下方 comment 內容的檔案>
gh issue close <n> --repo yotsubamomo/aiot-classwork --reason "not planned"
```

（`gh issue close` 沒有 `--comment-file`，所以先用 `--body-file` 留言再關閉，避免在 shell 中跳脫多行文字。）

Comment 內容（七張相同，逐字）：

```markdown
本票不再執行：它所依據的契約已被取代。

- 本票是從 HW2 Outcome Contract r4（2026-10-14 接受；branch `home_work_02-outcome-contract`）衍生的 Spec v1.1 derive 出來的。
- 2026-10-18 acceptor 接受了新的 HW2 Outcome Contract：`home_work_02/doc/brief/BRIEF.md` @ `dff7c55c`（接受紀錄在 `home_work_02/doc/governance/outcome-contract.md`，branch `home_work_02-regrill`）。它已接受的 Grill 紀錄明定不沿用 r4 與 Spec v1.1 的決定。現行 Spec 是 rev 3（#59）。
- Design Authority 判定：Spec v1.1 和本票都已經不是任何已接受 Outcome Contract 的有效 derived contract。本票的 AC、60／20／20 分區、nested CV、split conformal，以及 r4 的 SA-3 opt-in 與一次性 RB-1 合併授權，都不再適用。紀錄：`home_work_02/doc/governance/decisions/decision-20261018-r4-derived-contracts-disposition.md`（branch `home_work_02-regrill`）。
- 本票沒有任何實作、worklog 或 audit。新的 Tickets 會由 Spec rev 3 另外 derive，並以新編號開立；本票不改寫、不重開，也不會拿來承載新票。
- r4、Spec v1.1 和它們的 derivation record 保留在 branch `home_work_02-outcome-contract` 作為歷史。
```

- **執行者與時機**：這是不屬任何 reserved boundary 的 tracker 維護，不需要變更 Outcome Contract。不過現行 OC §2 把這次的授權限定在接受紀錄與 `/to-spec`，acceptor 也要求「不得自行擴大授權」，所以由派工 session 在 acceptor 同意後執行，而且 MUST 在 `/to-tickets` 發布新票之前完成。DA 不執行 GitHub 操作。
- #59 不在這次處置的範圍內，不動。
- 舊 `tickets.md` 只存在於 `home_work_02-outcome-contract`，不修改。`home_work_02-regrill` 上的新索引由 Ticket derivation 建立。

### (3) 不得默默沿用、以及可以有意識重用的內容

**不得默默沿用**：Spec rev 3 與 Ticket derivation 都不得以 v1.1 或 #50–#56 為依據引入以下內容；需要時，依現行契約重新決定。

| # | 內容 | 理由 |
| --- | --- | --- |
| N-1 | OC r4 §4.2 的 SA-3 opt-in、§9 的一次性 RB-1 合併授權、C5 的 push 授權 | 現行 OC §2：沒有 SA-3 opt-in，合併屬 RB-1；目前不授權 push。新票的「不由本票執行」與合併條款以現行 OC 為準 |
| N-2 | r4 §9 的 Fable fallback 決定（DA 與 reviews 改用 Opus 5.5／`xhigh`） | 這是 r4 接受時的 acceptor 決定，不在現行契約內。替代一律依 Bindings §3.1 O-2 與當次的可用性證據 |
| N-3 | `decision-20261014-lane.md`、`decision-20261014-high-risk-categories.md`（H-1～H-4、A-1～A-9） | 這些是 r4 下的 DA 決定。現行 OC §2 要求 DA 重新判定 lane 與高風險類別並留下紀錄（Bindings §5、§8.2 #4）；舊紀錄只能作參考 |
| N-4 | 60／20／20、Calibration、outer／inner nested CV、`frozen` manifest 事件鏈、split conformal 公式與 R-CONF-\*、R-SEL-2 的 0.5 USD 平手規則 | 與 Brief §4–§6 和 Spec rev 3 互斥 |
| N-5 | R-CAND-8「禁止 p-value 方法」；五個候選的定義；以 inner CV 選 k | Brief §5 已把 p-value backward 列為講義對照，k 路徑則是 1…18 全部報告 |
| N-6 | 所有非 one-hot 欄都標準化 | Spec rev 3：OLS 用原始尺度，只有 Ridge／Lasso 標準化 |
| N-7 | Web App 是 non-scope；「root `CONTEXT-MAP.md` 不修改」 | Brief §3.2、§8 已改為必須有 dashboard，root 兩個檔案各加一列（RB-5，先說明） |
| N-8 | S1～S4 完成狀態，以及 OC-A1～OC-A8、AC-01～AC-31、INV-1～INV-9 的編號與 PASS／FAIL | 這些屬於 r4 的 acceptance boundary；新票只能引用 Spec rev 3 的 verification contract |
| N-9 | 上位契約的 sha256 `a969e7e2…61ab` | 現行轉寫檔已更新（`b01c6fb5…4b89`），另有 SRC-2T、SRC-3；以 Brief §2 為準 |
| N-10 | 舊 B-17 的「不建立 CI」，或反過來的「另設 CI」 | Spec rev 3 的 Testing 一節提到「本單元另設自己的 CI 路徑過濾」，但 `.github/workflows/` 在單元目錄外，屬 RB-5。Ticket derivation 必須明確處理：要建 CI，先依 RB-5 取得 acceptor 授權；不建，就不得把「PR checks 成功」列為該票的條件 |
| N-11 | 舊 R-RPT／R-PKG 中以實際學號命名追蹤檔或驗收的寫法 | BR-03：追蹤檔案一律寫 `<學號>`，實際值只放在未追蹤的設定與 ZIP 中 |

**可以有意識地重用**：以下內容只當參考或 HOW 前例。派工時要重新核對，並在新的 derivation record 寫明來源；它們不構成契約。

| # | 內容 | 條件 |
| --- | --- | --- |
| U-1 | 資料事實與 CSV sha256 `d0875baa…7b7e`、R-DATA-3 的 21 欄順序、列數與 `id` 數的驗證、`sqft` 恆等式 | 與 Brief §4 一致；Brief 要求實作時重新下載並核對 |
| U-2 | R-DATA-2 的取得原則：只用匿名公開端點，不使用 Kaggle 憑證，失敗時停止並由 acceptor 提供檔案（RB-3） | 符合 Bindings RB-3 與 H-1 的關注點；新票可以採用，但要在新的高風險決定下重新寫出 |
| U-3 | `sale_days` 基準日、`is_renovated`／`effective_year`（未整修時＝`yr_built`）、one-hot drop first、未見類別編為基準 | 與 Spec rev 3「資料、計數與前處理」相容；基準日由 Spec rev 3 的 `preprocess` 決定並匯出 |
| U-4 | 報告建置的環境事實（2026-10-14：Edge 與 Chrome 已安裝，pandoc 與 xelatex 未安裝；Python 3.11.2） | 只是舊證據，派工時要重新核對；工具選擇屬 HOW（Spec rev 3） |
| U-5 | 票的結構：AC 只引用、不重述；有高風險節；等待 acceptor 輸入的票只停止受影響路徑（#55、#56 的做法）；打包工具拒絕佔位學號 | 只是格式前例，內容以 Spec rev 3 為準 |
| U-6 | 舊 derivation 中的「ChatGPT PDF 同時放在報告附錄與 ZIP」（B-6）、「100 字以漢字數計算」（B-7） | 這些是 r4 下的 DA 解讀。Spec rev 3 的 derivation record 可以重新作出相同的判定，但必須在現行契約下重新寫出，不得以舊紀錄為依據 |

## 4. 對進行中工作與 evidence 的影響

- **進行中的工作**：沒有。#50–#56 從未執行，也沒有 worklog、run record、audit、PR 或實作 commit，所以沒有 evidence 需要轉移或重新評估，也沒有 findings 需要保留。
- **Spec rev 3**：本判定不修改它。它是 MATT `/to-spec` 的產物；依現行 OC §2，它進入治理後，DA 與 review 的邊界照常適用。**在 derive Tickets 之前，Spec rev 3 還需要 DA 的 derivation record**（`derivation-SPEC.md`：依據、boundary determination、acceptance boundary 的分配、受影響的工作；治理 §1.2、§3.4），才是有效的 derived contract。該紀錄還應確認兩件事：一是 Brief 與 `CONTEXT.md` 在 `dff7c55c` 之後的修改不改變 accepted 語義（`git diff dff7c55c HEAD` 顯示兩個檔案都有修改；Brief §14 把它們標為 SR-06／SR-11 的編輯性修訂）；二是上表的 N-10。
- **`/to-tickets` 的前置條件**：(a) acceptor 授權 `/to-tickets`（現行 OC §2 尚未授權）；(b) Spec rev 3 的 derivation record；(c) DA 在現行契約下的 lane 與高風險類別 decision records（N-3）；(d) 已完成本紀錄第 3 節 (2) 的 GitHub 操作。
- **不受影響**：Wireframe v0.2 的接受紀錄（`design/WIREFRAME-ACCEPTANCE.md`）、#59、Bindings、老師文件。

## 5. 是否改變 accepted 語義，以及需要的 authority

- 不改變任何 accepted 語義，不是 contract change，本判定不需要 acceptor 核准。
- 需要 acceptor 的只有兩件事：同意執行第 3 節 (2) 的 tracker 操作（因為現行授權範圍較窄），以及之後授權 `/to-tickets`。若 acceptor 認為 r4 應該繼續與現行契約同時有效，那是 Outcome Contract 的接受問題，由 acceptor 決定；在那之前依本紀錄 fail-closed。

## 6. 受影響的 work items

#50、#51、#52、#53、#54、#55、#56（關閉）；Spec rev 3 的 derivation record 與後續的 Ticket derivation（前置條件）；#59（不動）。

## 7. Evidence

- `gh issue view 50…56,59 --json …`（2026-10-18）：狀態、label、comment 數、更新時間；#50 與 #56 的 body 全文。
- `git show home_work_02-outcome-contract:` 下的 `outcome-contract.md`、`spec/SPEC.md`、`ticket/tickets.md`、`decisions/derivation-SPEC.md`。
- `git show dff7c55c:home_work_02/doc/brief/HW2_Regrill_Brief_Draft_v0.1.md` 第 5 行。
- 對各 HW2 branch 執行 `git ls-tree -r`：沒有 `worklog/`、`run/`、`audit/`。`gh pr list`：沒有 HW2 PR。
- `sha256sum home_work_02/doc/requirement/*.txt`；`git diff --stat dff7c55c HEAD -- home_work_02/doc/brief home_work_02/CONTEXT.md`。
- 寫入的檔案只有本紀錄；沒有修改 GitHub、Spec、Brief 或其他檔案；沒有 commit。
