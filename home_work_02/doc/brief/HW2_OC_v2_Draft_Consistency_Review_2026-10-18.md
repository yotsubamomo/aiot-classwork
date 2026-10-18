# HW2 Outcome Contract v2 DRAFT r1 — Draft-level consistency review（2026-10-18）

- **性質**：無角色主 session 對自己起草的 OC v2 DRAFT 做的 self-check。依 acceptor 2026-10-18 的「Part D — Governance and consistency validation」指示進行。**這不是 independent audit**（治理 §2.3、§4；Bindings §3.7），不構成 finding、verdict 或接受。
- **受檢對象**：
  - [`../governance/outcome-contract-v2.md`](../governance/outcome-contract-v2.md) DRAFT r1；
  - SRC-2T；
  - Brief v0.4（rev 2）；
  - Delta record（rev 2）。
- **對照**：
  - SRC-2（sha256 `1b3a5aad1c261425eb34f2eb46aebe6a62c73aba4fbf2d67a166fe9df28639d7`）；
  - F-1～F-7 裁決（Brief v0.4 §0）；
  - G1–G8、C1–C5；
  - Bindings b5；
  - OC r4（@ `e2153254`）與 Spec v1.1；
  - Issues #50–#56。

## 1. 老師需求的涵蓋（Mandatory／Suggested／Optional／Ambiguous → OC v2）

| 來源 | 類別 | OC v2 | Scope class | 報告標示 | AC |
| --- | --- | --- | --- | --- | --- |
| T-01 多元線性回歸＋CRISP-DM | M | §1、M2、M4 | MVM | 老師要求 | OC-A2、OC-A4 |
| T-02 10–20 個特徵 | M（範圍 A） | M1、§2.4.1 | MVM | 老師要求 | OC-A1 |
| T-03 類型不限 | O | §2.4.1（King County） | — | — | OC-A1 |
| T-04 來源與連結 | M | M1 | MVM | 老師要求 | OC-A1 |
| T-05 線性回歸預測 | M | M2 | MVM | 老師要求 | OC-A4 |
| T-06 可嘗試 SLR／MLR／AR | O | §2.3（AR 不做） | — | — | — |
| T-07 特徵選擇與模型評估 | M | M2、E1、E4 | MVM＋ENHANCED | 老師要求（M2） | OC-A4 |
| T-08 預測圖＋區間 | M | M3、E6 | MVM＋ENHANCED | 老師要求（M3） | OC-A5 |
| T-09 CRISP-DM 六階段 | M | M4 | MVM | 老師要求 | OC-A2 |
| T-10 ChatGPT 對話 PDF | M | M5、§2.5.1 | MVM | 老師要求 | OC-A7、OC-A8 |
| T-11 NotebookLM 摘要 ≥100 字 | M | M6、§2.5.1 | MVM | 老師要求 | OC-A7 |
| T-12 兩個標示 | M | M6、M7 | MVM | 老師要求 | OC-A7 |
| T-13 主程式檔名 | M | M9 | MVM | 老師要求 | OC-A8 |
| T-14 報告四項內容 | M | M4～M8 | MVM | 老師要求 | OC-A2、OC-A7 |
| T-15 學號 ZIP | M | M9 | MVM | 老師要求 | OC-A8 |
| T-16 GitHub／README（optional） | O | M10（因 G7） | MVM | 老師要求（條件式條款） | OC-A8 |
| T-17 評分標準 | M（評分依據） | 全部；Kaggle 名次不適用（§2.3） | — | — | — |
| S-01／S-02 14–39 | A | M1、§2.4.1（交集 14–20） | MVM | 補充條件以「依老師補充建議」說明 | OC-A1 |
| S-03 資料集準則 | S | 報告說明（§2.4.1） | — | — | — |
| S-04 選擇後計數 | A | §2.3（不採用） | — | — | OC-A1 FAIL 條件 |
| S-05／S-07／S-10 推薦資料集 | S | §2.3（不採用）；REFERENCE | — | 未採用，可說明理由 | OC-A12 |
| S-06 編碼前計數 | S | §2.4.1 | — | — | OC-A1 |
| S-08a～c | S | M4、E2 | 沿用 | 依各項 | OC-A2 |
| S-08d LR、Ridge、Lasso | S | E1 | ENHANCED | 依老師補充建議 | OC-A4、OC-A12 |
| S-08e Adjusted R² | S | E11、§2.4.4 | ENHANCED | 依老師補充建議 | OC-A10 |
| S-08f 五大假設 | S（內容 A） | E10、§2.4.3 | ENHANCED | 依老師補充建議 | OC-A9 |
| S-08g 預測新樣本與解釋模型 | S | E12、§2.4.5 | ENHANCED | 依老師補充建議 | OC-A11 |
| S-09 方法清單與 k | S | §2.3（不新增）；OC-A4 的說明；permutation importance 只作解釋工具（E12） | — | 未採用的方法不得寫成已完成 | OC-A4、OC-A11、OC-A12 |

**結論**：
- T-xx 的全部 M 項都有對應的 MVM 項目與 AC。
- S 項目沒有被列為 MVM 或「老師要求」。M1 是 T-02（M）加上 acceptor 的交集解讀，S-01 本身仍分類為 A。
- O 項目依 r4 的處理不變。

## 2. F-1～F-7 的落實

| 裁決 | 子項 | OC v2 位置 | 結果 |
| --- | --- | --- | --- |
| F-1 | 交集 14–20；編碼前；排除 `id` 與 `price`；報告說明兩條原文與解讀；補充段不重新分類 | §2.1、M1、§2.4.1、OC-A1、§2.3 | 符合。自我檢查時修正一處：r1 初稿的 OC-A1 也要求建模 group 數落在 14–20，這超出 F-1 的範圍，已改為只限制 source feature 數（CR-1） |
| F-2 | King County；`price`；19／18；固定 checksum 與來源；group-aware | §1、§2.4.1、E3、E9、§5、§2.3 | 符合 |
| F-3 | 五個候選；group 層級；同一 outer folds；nested inner CV；Fit-only 選擇；RMSE 選模；既有 tie-break；Fit 上重訓再校準；不加 SelectKBest／RFE／permutation importance 選擇；說明 S-09 是建議 | E1、E4、§2.4.1、§2.3、OC-A4 | 符合。「既有 tie-break」以「沿用已接受的決定」表述；tie-break 的實際規則在 Spec v1.1 R-CAND-6、R-SEL-2（r4 下的 derived contract），DA 在新的 derivation 中沿用 |
| F-4 | 五個面向；Fit 衍生資料；log 尺度；數值或圖形證據與解讀；違反不是 FAIL；不用 Calibration／Test；分開兩類假設；方法交 DA | E10、§2.4.3、OC-A9、OC-A3、§3.4、§5 | 符合 |
| F-5 | outer-CV 與 Test；n／p 慣例、適用性、自由度、限制交 DA；不固定 p；不改變選模準則 | E11、§2.4.4、OC-A10、§2.3、§3.4、§5 | 符合。「不適用」的標示是讓 DA 的「適用性」定義可以被觀察，不是新的語義 |
| F-6 | 凍結 predictor 的解讀；log 尺度係數，考慮標準化與編碼；Fit-only permutation importance；預測新樣本；限制與非因果；不是選擇候選；不用 Calibration／Test | E12、§2.4.5、OC-A11、OC-A3、§2.3、§3.4 | 符合 |
| F-7 #1 | 保留歷史文件與 commit identifiers | 檔頭；§10；git（只新增檔案） | 符合：r4、Brief v0.1～v0.3、Spec v1.1、decision records 的工作目錄與 git 內容都沒有變更（第 6 節） |
| F-7 #2、#3 | 新檔；提議後繼；接受後才生效 | 檔頭、§9 | 符合 |
| F-7 #4 | 重新確認 C5、SA-1／SA-2、SA-3 opt-in、zh-TW、證據規則 | §4.1、§4.2、§2.5、§2.5.1 | 符合（重新陳述；接受後才生效） |
| F-7 #5 | 不推定 RB-1 一次性授權 | §4.2「第一個 HW2 PR」、§8 #4、§9 | 符合；列為待決事項 U-1 |
| F-7 #6 | #50–#56 不變 | §4、§5；第 5 節 | 符合 |
| F-7 #7 | iLearning、破壞性 Git、第三方部署帳號保留 | §4、§4.1 | 符合 |
| F-7 #8、#9 | 三種標示；建議不寫成老師要求 | §2.2「報告標示」欄、§2.4.6、OC-A12、§3.4 | 符合；既有項目的標示對應由起草者提議，列為待確認事項 U-2 |

## 3. 歷史決定 G1–G8、C1–C5

| ID | OC v2 | 結果 |
| --- | --- | --- |
| G1 | §1、E1、§2.4.1 | 保留 |
| G2 | E2、E4 | 保留；Adjusted R² 只加入報告指標 |
| G3 | E6、§2.4.2（逐字沿用） | 保留 |
| G4 | E2、§2.4.1 | 保留 |
| G5 | E7 | 保留 |
| G6 | M5、§2.5.1 | 保留 |
| G7 | M10 | 保留 |
| G8 | E8、§3.5、§4.1（原文保留） | 保留；驗證範圍擴充 |
| C1～C4 | E2～E6 | 保留 |
| C5 | §4.1 | 保留（重新陳述） |

沒有任何 G／C 決定被刪除或靜默改變。

## 4. 已接受語義的保留（Part C 保留清單；與 r4 機械比對）

| Part C 保留項目 | OC v2 | 檢查方法與結果 |
| --- | --- | --- |
| King County 來源與 checksum | §2.4.1、§5 | sha256 `d0875baa…7b7e` 與 r4 相同 |
| 60／20／20 group-aware 分區 | E2、E3、§2.4.1 | 文字與 r4 相同 |
| Nested CV、隔離與 leakage 控制 | E4、§2.4.1、OC-A3 | r4 的條件全部保留；OC-A3 只增加條件 |
| log(price) 訓練與 USD 評估 | E5、C4 | 不變 |
| 95% split conformal 與 exchangeability 限定 | §2.4.2 | **程式比對：與 r4 §2.4.2 逐字相同**；OC-A5 的 PASS／FAIL／證據逐字相同 |
| 凍結 predictor 與每次執行單次 Test 評估 | §2.4.1 | r1 初稿寫成「交 DA 確認」，弱化了這項保留；已改為 accepted 語義，內容取自 Spec v1.1 R-SEL-3、R-SEL-4、R-EVAL-1a（CR-2） |
| CRISP-DM 六階段 | M4、OC-A2 | OC-A2 逐字相同 |
| 真實的 ChatGPT／NotebookLM 證據 | §2.5.1、OC-A7 | **程式比對：§2.5.1 與 OC-A7 逐字相同** |
| GitHub／ZIP 交付 | M9、M10、OC-A8 | OC-A8 逐字相同 |
| S1～S4 | §3.2 | S2～S4 文字相同；S1 加入 OC-A9～A12 |
| Git 授權邊界 | §4.1、§4.2 | C5 與 SA-3 opt-in 相同；第一個 PR 依 F-7 #5 修訂 |
| zh-TW | §2.5 | 相同 |

**沒有誇大保證**：
- conformal 陳述逐字沿用；
- §2.4.3 明確禁止以五項診斷暗示 exchangeability 成立，也禁止把區間有效性寫成依賴常態或同質變異；
- 隔離只增加條件，沒有放寬。

## 5. 授權與 Bindings b5

| 動作 | 依據 | 結果 |
| --- | --- | --- |
| 新增 `doc/requirement/` 的 SRC-2T | RB-5 保留；acceptor 2026-10-18 Part B 的明確指示（忠實轉寫加 sha256） | 只新增檔案；SRC-1 未變；PDF 未移動 |
| 新增 `home_work_02/.gitignore`（只有 SRC-2 PDF 一行） | 單元內檔案；Part B（不追蹤 PDF）＋Part E | 不修改 root `.gitignore`（RB-5，單元外） |
| 建立 topic branch、commit、push | SA-1 需要已接受的 OC，而本工作在 r4 的範圍外；改以 acceptor 2026-10-18 Part E 的逐次明確授權（Bindings §2.1） | 非破壞性：自 `6bc5eca` 建立新 branch，不 force、不 reset、不 rebase、不刪 branch |
| 開 PR | SA-2 需要已接受的 OC；Part E 要求先核對效果與權限 | **不開**：開 PR 不是本階段必要；若開，PR 會含 `doc/requirement/`，之後的合併屬 RB-1，且可能被誤讀為準備合併 |
| 合併、iLearning、Kaggle 或部署帳號 | RB-1、RB-2、RB-3 | 未執行 |
| 自我接受 OC v2 | 治理 §1.2、§5.3；Bindings §2.1 | 未執行；§9 保持空白 |
| Spec derivation、Ticket 修訂、實作、Orchestrator | 本階段明確排除 | 未執行 |

**沒有推定的授權**：
- OC v2 的 §4 寫明「本檔沒有任何授權」；
- §8 #2 記錄本次 Git 動作的依據是 acceptor 的逐次授權，不是 OC v2。

## 6. 歷史紀錄未被修改

`git diff --stat` 對下列已追蹤路徑沒有輸出（commit 前檢查，見 acceptance-review packet）：
- `doc/governance/outcome-contract.md`
- `doc/governance/decisions/`
- `doc/spec/`
- `doc/ticket/`
- `doc/brief/HW2_Grill_Brief_Draft_v0.1～v0.3.md`
- `doc/requirement/HW2-requirements-Multiple Linear regression.txt`
- `CONTEXT.md`

## 7. Issues #50–#56

| # | 狀態（2026-10-18 讀取） | 最後更新 |
| --- | --- | --- |
| #50～#56 | 全部 OPEN，label `ready-for-agent` | 2026-10-14T06:13:47Z～06:13:55Z |

- 本次沒有修改。
- OC v2 DRAFT 沒有重新授權它們：§4 寫明它們在 DA 判定前不得作為任何 run 的依據。
- 預期影響見 Delta record §6.3。

## 8. 發現與處置

| ID | 發現 | 處置 |
| --- | --- | --- |
| CR-1 | OC-A1 初稿把建模 group 數也限制在 14–20，超出 F-1 | 已修正（r1 commit 前） |
| CR-2 | 單次 Test 評估的語義初稿交 DA 確認，弱化了 Part C 的保留項目 | 已修正（r1 commit 前） |
| CR-3 | Brief v0.4 rev 1 的 F-2 事實表把 Predict the Flood 誤認為 Playground S4E5，並引用了非 SRC-2 連結的 Flood 資料集 | 已依 PDF link annotation 更正（Brief rev 2、Delta record rev 2）；不影響 F-2＝A |
| CR-4 | Brief v0.4 rev 1 的 F-7(a) 建議追蹤 PDF；Part B 要求先做公開性檢查 | 依 Part B 處理：不追蹤 PDF，追蹤 SRC-2T（Delta record §1.1） |

## 9. 待 acceptor 決定的事項（沒有自行補出）

| ID | 事項 | 為什麼需要 acceptor |
| --- | --- | --- |
| U-1 | 第一個 HW2 PR 的合併授權：diff 含 `doc/requirement/`，屬 RB-1 | F-7 #5 禁止推定沿用 r4 的一次性授權 |
| U-2 | 既有 ENHANCED 項目的報告標示對應：E1 的候選標「依老師補充建議」（S-08d、S-09），E2～E9 標「專案延伸」，E12 的 permutation importance 方法標「專案延伸」 | 標示決定報告如何描述與老師文件的關係（評分相關）；F-7 #8 只給了三個類別，沒有逐項指定 |
| U-3 | r4 接受紀錄中的 Fable fallback 決定（Fable 不可用時，DA 與 review 以 Opus 5.5／`xhigh` 替代）是否在 v2 下沿用 | 這是 r4 接受時的 acceptor 決定，不屬 Bindings；v2 的 DA 派工會需要它 |
| U-4 | SRC-2 原始 PDF 是否公開追蹤 | 公開揭露的決定（NCHU 版權聲明、LMS 頁面、第三方縮圖）；預設不追蹤 |
| U-5 | （可選）#50–#56 的 `ready-for-agent` label 在 DA 判定前是否維持 | 依 F-7 #6 維持不變；只提醒這個 label 的字面意思是可以開工 |
