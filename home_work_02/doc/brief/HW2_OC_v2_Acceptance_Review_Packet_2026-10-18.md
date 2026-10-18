# HW2 Outcome Contract v2 — Acceptance-review packet（2026-10-18）

- **性質**：給 acceptor 的審閱資料。由無角色主 session 整理，不具 authority，不構成接受。
- **受審對象**：`home_work_02/doc/governance/outcome-contract-v2.md` **DRAFT r1**，位於 commit **`9547f687ef2a636051bdd0f681f5e8506c9a61dd`**（branch `home_work_02-rebaseline-oc-v2`），檔案內容 sha256 `a578e7c71b3db87b77a24caa252386afdac92a5f4505e84676bfa9fc6c05f748`。
- 本 packet 由下一個 commit 加入，那個 commit 只新增本檔，不改變受審對象。

## 1. 新來源基準

| ID | 檔案 | sha256 | 狀態 |
| --- | --- | --- | --- |
| SRC-2 | `doc/requirement/HW2-requirements-Multiple Linear regression.pdf`（iLearning 頁面列印，2026-10-18 02:59，4 頁，1,083,106 bytes） | `1b3a5aad1c261425eb34f2eb46aebe6a62c73aba4fbf2d67a166fe9df28639d7`（與 acceptor 提供的預期值一致） | 提議的新上位契約；只保留在本機，以單元 `.gitignore` 排除 |
| SRC-2T | `doc/requirement/HW2-requirements-Multiple Linear regression_SRC-2_2026-10-18.txt` | `e5eb6a315dd5860e7562467012c748911454becb0c6bccde95823d1f0834e77c`（@ `9547f687` 的 blob 內容） | 追蹤的忠實轉寫 |
| SRC-1 | `doc/requirement/HW2-requirements-Multiple Linear regression.txt` | `a969e7e2228e97a35027ad63d3747f2e502bdd685cf7cfca30aaab50048761ab` | 歷史，未變更 |

**差異**：
- 正文與評分標準相同，只有「已缴交」4人→8人（以程式比對）。
- 新增的是「==== 補充 ====」段：老師的一句提問，加上 LLM 的回答。

## 2. F-1～F-7 最終裁決（原文見 Brief v0.4 §0）

| | 裁決 | 要點 |
| --- | --- | --- |
| F-1 | B | 14–20 個 source features（正文 10–20 與補充 14–39 的交集）；編碼前計數；不含 `id`、`price`；報告說明兩條原文與解讀；補充段維持原分類 |
| F-2 | A | 保留 King County（`harlfoxem/housesalesprediction`）；19 個 source features、18 個建模 group；checksum 與 group-aware 處理不變 |
| F-3 | A | 維持五個候選；不新增 SelectKBest、RFE 或以 permutation importance 選擇；說明 S-09 是建議 |
| F-4 | B | ENHANCED：五個診斷面向；只用 Fit 衍生資料；log 尺度；違反不是 FAIL；與 conformal 假設分開陳述；方法交 DA |
| F-5 | B | ENHANCED：Adjusted R²（outer-CV 與 Test）；n／p 等慣例交 DA；不固定 p；不改變 RMSE 選模 |
| F-6 | B | ENHANCED：Deployment 的模型解釋；log 尺度係數；Fit-only permutation importance；非因果提醒 |
| F-7 | YES | 新檔 OC v2；提議後繼；重新確認 C5／SA-1／SA-2／SA-3／zh-TW／證據規則；不推定 RB-1；#50–#56 不變；三種報告標示 |

## 3. 更新的紀錄

| 檔案 | 版本 | sha256（@ `9547f687`） |
| --- | --- | --- |
| `doc/brief/HW2_Grill_Brief_Draft_v0.4.md` | rev 2（Grill closed；§0 逐字裁決；F-2 事實更正） | `a52aef0c3d879b147ab6bf51588dc4b5c7786c428107bae585cd06bc9c01fefd` |
| `doc/brief/HW2_Requirements_Rebaseline_2026-10-18.md` | rev 2（裁決後的處理；SRC-2 公開性檢查） | `5ec2502908079071a9a1030e3af730244610d5a3caa40e522b7b0b04fdff1384` |
| `doc/brief/HW2_OC_v2_Draft_Consistency_Review_2026-10-18.md` | — | （同 commit） |

## 4. Outcome Contract v2 DRAFT

- 路徑：`home_work_02/doc/governance/outcome-contract-v2.md`
- 狀態：DRAFT r1，未接受
- Commit：`9547f687ef2a636051bdd0f681f5e8506c9a61dd`

## 5. r4 → v2 邊界差異（摘要；完整表見 OC v2 §10）

| 改變 | 不變 |
| --- | --- |
| §2.1 上位契約改為 SRC-2（SRC-2T 追蹤） | 資料集、checksum、group-aware 60／20／20 |
| M1：14–20 source features，報告說明兩條原文 | 五個候選、nested CV、RMSE 選模、tie-break、Fit 上重訓 |
| 新增 E10 診斷、E11 Adjusted R²、E12 模型解釋、E13 三種標示 | log(price) 訓練、USD 指標 |
| 新增 OC-A9～OC-A12；修訂 OC-A1、A3、A4 | §2.4.2 conformal（逐字）、OC-A5 |
| §2.3 新增六項排除 | §2.5.1 證據規則（逐字）、OC-A2、A7、A8 |
| §3.4 新增 FAIL／非 FAIL 條件 | S1～S4（S1 加入新 AC）、§3.3 acceptor 輸入 |
| 「每次執行只做一次 Test 評估」由 Spec 層級提升到 OC | C5、SA-3 opt-in、zh-TW |
| 第一個 PR 的 RB-1 不沿用 | RB-1～RB-6 的保留 |

## 6. 涵蓋矩陣（Mandatory／Suggested／Enhanced）

| 類別 | 項目 | OC v2 |
| --- | --- | --- |
| **老師要求**（M） | T-01、T-02、T-04、T-05、T-07～T-15、T-17 | M1～M10；OC-A1、A2、A4、A5、A7、A8 |
| 老師的 optional（O） | T-03、T-06、T-16 | King County；Auto Regression 不做；GitHub（M10） |
| **依老師補充建議**（採用的 S） | S-08d（LR、Ridge、Lasso）、S-09 的 SFS 與 Lasso、S-08e、S-08f、S-08g | E1、E11、E10、E12；OC-A4、A10、A9、A11 |
| 採用的解讀（A） | S-01／S-02 → 交集 14–20 | M1；OC-A1 |
| 未採用的 S／A | S-04、S-05、S-07、S-10、S-09 的 SelectKBest／RFE／permutation-importance 選擇與 k 值 | §2.3 Non-scope；REFERENCE |
| **專案延伸** | E2～E9（分區、group-aware、nested CV、log 目標、conformal、模組、驗證、checksum），以及 E12 的 permutation importance 方法 | OC-A3、A5、A6 |

完整逐條矩陣見 consistency review §1。

## 7. Git

| 項目 | 值 |
| --- | --- |
| Branch | `home_work_02-rebaseline-oc-v2`（新建，追蹤 `origin/home_work_02-rebaseline-oc-v2`） |
| 基礎 | `home_work_02-outcome-contract` @ `6bc5eca4f745bb85b95de329c84ed4ec717b0679`（未修改，未 rebase） |
| Commit 1（受審對象） | `9547f687ef2a636051bdd0f681f5e8506c9a61dd`：只新增 6 個 `home_work_02/` 內的檔案 |
| Commit 2 | 只新增本 packet（SHA 見 acceptor 收到的回報） |
| Push | 一般 push，沒有 force |
| 未追蹤 | SRC-2 PDF（ignored）；`week05/`、`.claude/settings.json`、`grep.exe.stackdump`（單元外，沒有動） |
| PR | **未開**：SA-2 需要已接受的 OC，而開 PR 也可能被誤讀為準備合併 |

**授權依據**：acceptor 2026-10-18 的指示 Part E：「I authorize the necessary non-destructive Git preparation operations for this HW2 re-baselining task, limited to the approved HW2 unit and its documentation.」新增 SRC-2T 屬 RB-5，依據同一指示的 Part B。

## 8. 權限與保留的動作

| 權限 | 持有者 | 狀態 |
| --- | --- | --- |
| 接受 OC v2（治理 §1.2） | Acceptor | **待執行** |
| 第一個 HW2 PR 的合併（RB-1） | Acceptor | 待決定（U-1） |
| Spec 處置、lane、高風險確認、#50–#56 的處置 | Design Authority（OC v2 接受後） | 未開始 |
| Formal run | Orchestrator（由 acceptor 指定） | 未開始 |
| iLearning 繳交（RB-2）、憑證與第三方帳號（RB-3）、付費（RB-4）、單元外檔案（RB-5）、破壞性 git（RB-6） | Acceptor | 保留 |

## 9. 待 acceptor 決定的事項

| ID | 事項 |
| --- | --- |
| U-1 | 第一個 HW2 PR（diff 含 `doc/requirement/`）的合併：重新授權 Agent 在 gates 通過後合併，或由 acceptor 自己合併 |
| U-2 | 報告標示的逐項對應：E1 的候選標「依老師補充建議」；E2～E9 與 permutation importance 方法標「專案延伸」。這是起草者的提議，請確認或修改 |
| U-3 | r4 的 Fable fallback 決定（Fable 不可用時以 Opus 5.5／`xhigh` 替代）是否在 v2 下沿用 |
| U-4 | SRC-2 原始 PDF 是否公開追蹤（預設：不追蹤） |
| U-5 | （可選）#50–#56 的 `ready-for-agent` label 在 DA 判定前是否維持 |

## 10. 接受 OC v2 所需的下一步

1. 審閱 commit `9547f687` 的 `home_work_02/doc/governance/outcome-contract-v2.md`。需要修改時，指出修改處，由起草者產生 DRAFT r2 與新的 commit。
2. 以明確的原文接受，至少包含：
   - 版本（DRAFT r1）與完整的 commit SHA；
   - 適用的 Project Bindings（b5，`main` `5ebcc58`）；
   - U-1～U-4 的決定（U-5 可省略）。
3. 接受後，由起草者把原文逐字寫入 OC v2 §9，以只改 §9 與檔頭狀態列的 follow-up commit 記錄（與 r4 的程序相同）。
4. 之後才進入 Design Authority 的工作：lane、高風險、Spec v1.1 與 #50–#56 的處置。本 session 不會自行啟動。
