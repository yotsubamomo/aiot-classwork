# Derivation record — SPEC rev 3（HW2 Multiple Linear Regression，`home_work_02/`）

- **紀錄類型**：Design Authority derivation record（治理 §1.2、§3.4；Bindings b5 §7）
- **日期**：2026-10-18
- **Derived contract**：[`../../spec/SPEC.md`](../../spec/SPEC.md) **rev 3**（＝GitHub issue #59）。本紀錄以 HEAD `c4d5c5b2` 的檔案為準。**rev 4**（2026-10-18）只補記 CC-1 的授權依據與約束，`metric_only` 契約不變；第 11 節依 HEAD `6f14130` 加上工作樹的 CC-1 修改核對。
- **現行 accepted 語義**：Brief @ `dff7c55c`，加上 **CC-1**（[`../outcome-contract.md`](../outcome-contract.md) §4，acceptor 2026-10-18 核准的 contract change）。
- **Outcome Contract**：[`../outcome-contract.md`](../outcome-contract.md)，ACCEPTED 2026-10-18。接受的內容是 `doc/brief/BRIEF.md`、Grill 紀錄 rev 7 與 `CONTEXT.md` 於 commit `dff7c55c` 的版本。
- **上位契約**：`doc/requirement/` 的 SRC-1 轉寫（sha256 `b01c6fb5…4b89`）、SRC-2T（`670cdf28…08ba`）、SRC-3（Brief §2）。
- **相關紀錄**：[`decision-20261018-r4-derived-contracts-disposition.md`](decision-20261018-r4-derived-contracts-disposition.md)、[`decision-20261018-lane.md`](decision-20261018-lane.md)、[`decision-20261018-high-risk-categories.md`](decision-20261018-high-risk-categories.md)、[`../../spec/SPEC-review-2026-10-18.md`](../../spec/SPEC-review-2026-10-18.md)、[`../../../design/WIREFRAME-ACCEPTANCE.md`](../../../design/WIREFRAME-ACCEPTANCE.md)
- **Binding**：`gov-design-authority`，`claude-opus-5-5`／`high`（Bindings §3.1 預設 mapping，沒有 escalation，沒有替代）。本紀錄不自證 binding，由派工者依 Bindings §3.6 核對。
- **Capability escalation**：未提出。(D1) 不成立：各項都能以 Brief、Grill 紀錄與 Spec 的文字裁決；無法裁決的 F-1 屬 boundary 問題，依治理 §2.5 走 routing，不以 escalation 處理。(D2) 不成立。

## 0. MATT 獨立性

Spec rev 3 是 MATT `/to-spec` 依它自己的流程產生的（OC §2；acceptor 2026-10-18）。本紀錄**不改寫 Spec**，只做三件事：確認它在 Outcome Contract 的 boundary 內、分配 acceptance boundary、為 Ticket derivation 寫下有約束力的解讀。發現 Spec 有缺陷時，記為給 acceptor 的 finding（第 7 節），不編輯 `SPEC.md`。Spec 寫明「Brief 與本 Spec 不一致時以 Brief 為準」；Ticket derivation 依這條規則與本紀錄處理差異。

## 1. 效力

- 〔2026-10-18 更新〕CC-1 之後沒有例外：Spec rev 4 全部都是有效的 derived contract（第 11 節）。以下是原判定的文字：在第 3 節的 boundary determination 下，Spec rev 3 自本紀錄起是現行 Outcome Contract 的有效 derived contract。**唯一例外是 F-1 的路徑**（Ridge／Lasso 的 test 評分）：在 acceptor 決定前不在有效範圍內（第 3 節 B-2）。
- 它的接受與授權來自 Outcome Contract，不需要 acceptor 逐份核准（治理 §1.2）。不過 OC §2 目前**沒有授權** `/to-tickets` 與實作，所以本紀錄不使任何實作可以開始。
- 只有一份 Spec。

## 2. 依據的 Outcome Contract 條款

| OC（Brief）條款 | 對應的 Spec 章節 |
| --- | --- |
| §1 目標 | Problem Statement、Solution |
| §2 來源與地位 | Problem Statement；US-1～3、US-15 |
| §3.1 老師要求 | 單元結構與交付物、資料、報告與打包；US-1～20 |
| §3.2 dashboard 與補充建議 | Dashboard、`model_data` 契約、指標與推論、診斷與解釋 |
| §3.3 選配、§3.4 不做 | Dashboard 的選配；Out of Scope |
| §4 資料與前處理 | 資料、計數與前處理；分割與交叉驗證 |
| §5 特徵選擇、模型與比較 | 特徵選擇與模型；指標與推論 |
| §6 預測區間與診斷 | 預測區間；診斷與解釋 |
| §7 Dashboard（含 BR-01、BR-04、Q43） | Dashboard；`model_data` 契約；人工檢查表 |
| §8 交付物、§9 acceptor 輸入 | 單元結構與交付物；報告與打包；Acceptor 輸入與等待 |
| §10 驗證與驗收 | Testing Decisions（主 seam、次 seam、人工檢查表） |
| §11 風險（含 BR-03） | 單元結構與交付物；人工檢查表 Repo |
| §12 HOW | 實作選擇散見各節（seed、5 fold、alpha 網格、group 彙總規則等） |

## 3. Boundary determination

**總判定**：Spec rev 3 除了 B-2 以外，都在已接受的 Brief boundary 內，沒有改變 accepted 語義。B-2 我無法確立在 boundary 內，所以該路徑 fail-closed 至 acceptor（治理 §1.2）。〔2026-10-18 更新：acceptor 以 CC-1 核准，B-2 已在 boundary 內，見第 11 節。〕

| # | 項目 | 判定 | 依據 |
| --- | --- | --- | --- |
| B-1 | Fold-internal selection 與 canonical subset（SR-01、SR-11） | 在 boundary 內。這是「選擇只用 training」的嚴格落實，不是 Brief 延後的 nested 設計。成本增加約 6 倍，屬 Q34 的量測與回報義務 | Q4、Q13(a)、Q33；Brief §5、§10 |
| B-2 | **Ridge／Lasso 的 test 指標**（Spec「特徵選擇與模型」最後的「Ridge／Lasso 的 test 指標亦各報一次」、`test` 的 `kind = "metric_only"`，以及對應的不變量與測試） | **〔RESOLVED by CC-1，2026-10-18〕現在在 boundary 內**，限 CC-1 的六項約束與範圍限制（第 11 節）。原判定如下：**無法確立在 boundary 內，fail-closed 至 acceptor（F-1）。** Brief §5 與 BR-01 第 3 點寫「Test evaluation **只針對**各方法的 CV winner、All-in baseline 與整體 CV winner」；已接受的 `CONTEXT.md` 寫「No other model is scored on the test set」；Q20、Q31 把 Ridge／Lasso 定位為對照，「只在比較表與圖」。Ridge／Lasso 不是 CONTEXT 定義的 feature-selection method（它們不產生每個 k 的子集），所以不屬於「各方法」。另一種讀法（把 Ridge／Lasso 當成各自的單一模型方法）沒有文字依據。只停止這條路徑：其餘工作照常；Ridge／Lasso 的 CV 對照不受影響 | Brief §5、§7 BR-01；CONTEXT「Test evaluation」；Grill Q20、Q31 |
| B-3 | `model_data` 含全部 test 列的原始值與 `actual_price`（`test_inputs`），以及每個 (方法, k) 的 `fit` | 在 boundary 內，附 Ticket 義務：BR-01 禁止的是**顯示**未授權模型的 test 結果，以及**因 dashboard 操作產生**新的 test evaluation，不是讓 test 資料無法取得（ZIP 本來就含完整 CSV 與 seed）。所以 dashboard 的 UI 程式不得用 `test_inputs` 評估任何模型；test 區塊只讀 `test`。報告與 README 不得宣稱其他模型的 test 結果「在結構上無法取得」（Spec US-33 的措辭只限於 dashboard 的行為） | Brief §7 BR-01、§10 Test 暴露檢查；SR-02 |
| B-4 | 秩不足三類語義、`invalid` 候選、實驗層級失敗時停止並 route（SR-04、SR-10） | 在 boundary 內：不縮小範圍、不臨時刪欄 | Q16、Q34 |
| B-5 | 實際 vs 預測圖的效能門檻 (a)～(g)（SR-09） | 在 boundary 內：acceptor 2026-10-18 以 ACCEPTED WITH CLARIFICATION 接受 | Q43；Spec Further Notes |
| B-6 | 只用 training set 計算的 permutation importance，用於模型解釋 | 在 boundary 內：Brief §8 的 Deployment 要求「特徵重要性」；§3.4 只排除把它當作特徵選擇方法 | Brief §3.4、§8；Q11 H |
| B-7 | OLS 用原始尺度，只有 Ridge／Lasso 標準化 | 在 boundary 內：標準化細節屬 §12 的 HOW；Brief §8「標準化的讀法」適用於 Ridge／Lasso 的係數 | Brief §4、§8、§12 |
| B-8 | 涵蓋率不確定性採二項近似，標明獨立假設，不陳述偏差方向（SR-08、SR-12） | 在 boundary 內 | Q18 |
| B-9 | p-value backward：group F 檢定、門檻 0.05、fold-internal、只列為對照 | 在 boundary 內 | Q11 F；Brief §5、§12 |
| B-10 | Test 評估函式在同一次執行內第二次呼叫時報錯 | 在 boundary 內：落實「只評估一次」 | Brief §4、§5 |
| B-11 | Root `README.md` 與 `CONTEXT-MAP.md` 各加一列 | 在 boundary 內，但屬 RB-5：每次動手前都要取得 acceptor 的逐次授權（OC §2） | Brief §8 Q39 |
| B-12 | Spec Testing 提到「本單元另設自己的 CI 路徑過濾」 | 已由 acceptor 的 N-10 決定取代（第 6 節）：不建立 CI，Tickets 不實作這一項 | acceptor 2026-10-18 |
| B-13 | Wireframe v0.2 的 UI 設計（版面、手機選單、無障礙規則、色彩） | 在 boundary 內：acceptor 2026-10-18 接受它作為 UI Design Reference，不改變功能與統計要求；與 Brief／Spec 衝突時以 Brief／Spec 為準；`mock-data.js` 與 `wireframe.js` 的模擬計算不得沿用為實作或結果 | `design/WIREFRAME-ACCEPTANCE.md` |
| B-14 | Data Understanding 只用 training set 列出極端值 | 在 boundary 內 | Brief §4 異常值、Q33 |
| B-15 | 「NotebookLM 摘要 ≥100 字」的計數方式（Spec 沒有定義） | DA 裁決（治理 §3.6-A）：以漢字計，不含標點、空白、拉丁字母與數字，≥100。這是各種合理讀法中最嚴格的，滿足它就滿足所有讀法 | SRC-1「100 字以上」；Brief §3.1 T-AI |
| B-16 | Brief 固定的路徑（`home_work_02/hw2.ipynb`、`home_work_02/data/`、`home_work_02/index.html`＋`assets/`（含 Chart.js）、`doc/acceptance/ACCEPTANCE.md`、Pages URL） | 在 boundary 內。Spec 只寫概括時，Tickets 使用 Brief 的路徑 | Brief §7、§8 |

## 4. Acceptance boundary 的分配

**唯一的一份 Spec（rev 3）分配到 Outcome Contract 的全部 acceptance boundary**（Brief §3、§4–§9、§10、§11 的驗收意圖），〔CC-1 後〕包含 CC-1 的 Ridge／Lasso `metric_only` test 路徑（原文「B-2 的路徑除外」已不適用）。Spec Integration Audit 依治理 §4.7 核對全部覆蓋。下表讓覆蓋可以被觀察；標「T-義務」的是 Spec 沒有寫明、Ticket derivation 必須從 Brief 帶入的項目。

| Brief 的驗收意圖 | Spec 章節 | 驗證方式（Spec Testing Decisions） |
| --- | --- | --- |
| §3.1 T-資料：來源、連結、授權；19／18 與計數規則；引用兩條原文 | 資料、計數與前處理；US-1～3 | pytest `meta`（sha256、清單）；人工檢查表「報告」 |
| §3.1 T-模型：特徵選擇與模型評估 | 特徵選擇與模型；指標與推論 | 次 seam「特徵選擇」「模型與推論」「選模」 |
| §3.1 T-預測圖＋區間 | 預測區間；Dashboard 實際 vs 預測圖 | 主 seam 獨立重算（pytest、Node）；人工檢查表 (a)～(g) |
| §3.1 T-CRISP-DM：notebook 與報告各有六章 | 單元結構與交付物；報告與打包；US-4 | 人工檢查表只寫了報告。**T-義務**：notebook 的六章也要檢查 |
| §3.1 T-AI：ChatGPT PDF、NotebookLM ≥100 字、兩個標示 | 報告與打包；Acceptor 輸入與等待；US-13、40～42 | 人工檢查表「報告」；計數依 B-15 |
| §3.1 T-繳交：`<學號>_hw2.ipynb`、PDF 報告、`<學號>_hw2.zip` | 報告與打包；單元結構 | 人工檢查表「乾淨環境重跑」與打包；ZIP sha256 與檔案清單 |
| §3.1 T-GitHub：README 的流程與成果 | 單元結構；US-47 | **T-義務**：人工檢查 README 的內容項目（Brief §8 README 列） |
| §3.1 T-評分：說明沒有 Kaggle 名次，改以預測結果評估（Q38） | Spec 只在 Out of Scope 列出「Kaggle 競賽名次」 | **T-義務**：報告要有這段說明，並列入檢查（第 7 節 F-4） |
| §3.2 Dashboard（Pages、`home_work_02/index.html`、額外交付） | Dashboard；`model_data` 契約 | Node test；人工檢查表；路徑依 B-16 |
| §3.2 補充建議（Adjusted R²、五大假設、模型解釋、Ridge／Lasso）＋「依老師補充建議」標示 | 指標與推論；診斷與解釋；報告與打包（三種標示） | pytest 秩與 Adjusted R²；人工檢查表「報告」三種標示 |
| §3.3 選配 | Dashboard 的選配 | 不是完成條件 |
| §3.4 不做 | Out of Scope | Review 時核對；B-2 例外 |
| §4 資料 sha256、分組 80／20、fit 只用訓練列、log 目標 | 資料、計數與前處理；分割與交叉驗證 | 次 seam「分割」「前處理」「選擇邊界」 |
| §5 方法、k=1…18、公平性、CV winner、test 只評估授權模型、執行時間 | 特徵選擇與模型；指標與推論 | 次 seam「選模」；pytest `winners`／`test` 鍵集合；`meta` 執行時間 |
| §6 參數式 PI、涵蓋率報告、五大假設 | 預測區間；診斷與解釋 | 次 seam PI 手算；主 seam 逐筆重算；人工檢查表「報告」 |
| §7 BR-01 五點規則與 UI 驗收 | Dashboard（分層規則與來源標示）；`model_data` 不變量 | pytest 不變量；人工檢查表「來源標示」「不同模型提示」；B-3 的 UI 義務 |
| §7 BR-04 完全離線 | Dashboard；報告與打包（解壓驗證） | 人工檢查表「離線」（解壓、斷網、無伺服器、`file://`、零對外請求）；**T-義務**：加上靜態掃描外部資源 URL |
| §7 即時預測器（範圍、預設值、警告、未見 zipcode） | Dashboard 即時預測器 | Node 前處理案例；人工檢查表「預測器輸入與警告」 |
| §7 Q43 逐筆 PI 圖 | Dashboard 實際 vs 預測圖 | 主 seam 逐筆一致；人工檢查表 (a)～(g) |
| §8 交付物（模組、`requirements.txt`、結果產物、pickle、報告、README、ACCEPTANCE.md、ZIP） | 單元結構與交付物；報告與打包 | 人工檢查表；乾淨環境重跑 |
| §9 acceptor 輸入 | Acceptor 輸入與等待 | 缺少時只停止受影響路徑 |
| §10 每一項檢查 | Testing Decisions（主 seam、次 seam、人工檢查表） | 逐項對應如上 |
| §11 BR-03 學號 | 單元結構與交付物；人工檢查表「Repo」 | `git grep`。**T-義務**：Brief 寫「路徑由 Spec 指定」，但 Spec 沒有指定未追蹤設定的路徑，由 Ticket derivation 固定路徑並加入單元 `.gitignore` |
| Wireframe Open Verification Items OV-1～OV-6 | Dashboard；人工檢查表 | 見第 5 節 |

## 5. Wireframe Open Verification Items（Ticket derivation 必須放入 AC）

來源：`design/WIREFRAME-ACCEPTANCE.md`，acceptor 原文「請將這些項目保留至後續 Tickets 與 Acceptance Criteria」，並且不得標示為 PASS。

| # | 項目 | 在 AC 中的地位 |
| --- | --- | --- |
| OV-1 | 真正斷網、以 `file://` 開啟 | **PASS／FAIL**：就是 Brief §7 BR-04 的離線驗收 |
| OV-2 | 真實手機與觸控操作 | 必須執行並記錄（裝置、瀏覽器、結果），沒有證據不得標 PASS。是否作為完成 gate 未定（F-5） |
| OV-3 | Safari／Firefox 相容性 | 同 OV-2。參考環境仍是 Chrome／Edge（SR-09） |
| OV-4 | 螢幕閱讀器與完整 accessibility | 同 OV-2 |
| OV-5 | 色彩對比量測 | 同 OV-2。acceptance 紀錄表中的 4.5:1／3:1 是轉錄者寫的表，不是 acceptor 原文 |
| OV-6 | 正式 dashboard 的逐筆 PI 渲染效能 | **PASS／FAIL**：就是 Spec SR-09 的 (a)～(g) |

OV-2～OV-5 是 acceptor 接受的 UI 設計（B-13）的驗證項目，但 Brief 沒有為它們定義 PASS／FAIL 門檻。Tickets 必須執行並記錄它們，不得豁免；在 DA phase acceptance 之前，需要 acceptor 決定它們是不是完成 gate（以及門檻）（F-5）。

## 6. N-10 的決定（acceptor 2026-10-18，由派工 session 轉達）

- 新 Tickets **不得**把「PR checks 成功」列為條件。
- 單元 CI 延後：不修改 `.github/workflows/`（RB-5），Tickets 不實作 Spec Testing 提到的「CI 路徑過濾」（B-12）。
- 驗證改由 Executor 與 Reviewer 在本機執行 pytest、Node test 與 notebook 重跑，並把證據記入 worklog 和 audit record。
- 合併進 `main` 屬 RB-1，由 acceptor 決定（現行 OC 沒有 SA-3 opt-in），所以 Bindings §5 的 SA-3 check 條件不適用。
- 依據：acceptor 的決定由派工 session 轉達；派工者應把 acceptor 原文記入 run record 或本單元的紀錄。

## 7. 接受後修改的確認，與給 acceptor 的 findings

**接受後修改**（`git diff dff7c55c HEAD -- BRIEF.md CONTEXT.md`）：

| 修改 | 判定 |
| --- | --- |
| Brief §1「五種特徵選擇方法」改為「四種具有 k=1…18 路徑的方法＋單一 All-in baseline」（SR-06） | 不改變 accepted 語義：讓 §1 與已接受的 BR-02、§5 一致；acceptor 已接受 SR-06 |
| Brief §5 p-value backward「做一次」改為「產生單一子集、不進 k 路徑（選擇邊界與正式方法相同）」（SR-11） | 不改變 accepted 語義：Q11 F 的地位（講義對照、單一子集、不進 winner、不評估 test）不變；只把計算邊界寫清楚，使 CV 不洩漏（B-1） |
| Brief §14 新增修訂表，原 §14 改為 §15 | 紀錄性修改 |
| `CONTEXT.md`（commit `dea8fd0`）：「Feature-selection method」由「只用 training set、選 source features」改為「只用給定的列、選 feature groups；在 fold 內產生該 fold 的子集，在整個 training set 上產生 canonical subset」；新增「Canonical subset」 | 不改變 accepted 語義：fold 內的列仍然是 training 的列（Q4、Q33），以 group 為選擇單位就是 Q12 的決定；canonical subset 等於 BR-01 第 2 點「在完整 training set 上擬合」的模型。**但這次修改沒有記入 Brief §14**（F-2） |

結論：accepted 語義沒有改變。Tickets 可以引用 HEAD 版本的 Brief 與 `CONTEXT.md`；遇到歧義時，以 `dff7c55c` 的文字加上本表的判定為準。

**Findings（給 acceptor；本紀錄不改 Spec）**：

| ID | 嚴重度 | 內容 | 需要的決定 |
| --- | --- | --- | --- |
| F-1 | High（boundary）— **RESOLVED**（acceptor 選 (a)，CC-1，OC §4；第 11 節） | B-2：Spec 讓 Ridge／Lasso 在 test 上評分（`metric_only`），已接受的 Brief BR-01 與 CONTEXT 只允許 CV winners、All-in 與整體 winner。Wireframe v0.2 的 `mock-data.js` 也有 `TEST.ridge`／`TEST.lasso_ref` | acceptor 二選一：(a) 授權 Ridge／Lasso 各報一次 test 指標作為描述性對照。這會改變 BR-01 第 3 點與 CONTEXT 的 accepted 語義，屬 contract change（治理 §5.3），需要以紀錄寫明。(b) 不授權：Ridge／Lasso 只報 CV。Spec 的 `metric_only`、不變量與測試項需要經 MATT 流程修正，或由 Tickets 依「以 Brief 為準」略過並記錄。在決定前，Tickets 不得實作 Ridge／Lasso 的 test 評分 |
| F-2 | Low — 修訂表部分 **RESOLVED**（Brief §14 已補記 `dea8fd0` 與 CC-1 的 CONTEXT 修訂）；措辭部分仍開放；另有新的編輯性瑕疵，見第 11 節 G-5 | `CONTEXT.md` 的接受後修改（`dea8fd0`）沒有記入 Brief §14 的修訂表；另外 CONTEXT「CV winner」寫「the feature subset with the lowest CV RMSE」，在 fold-internal 下，CV RMSE 屬於 (方法, k) 這個程序，評估與部署的是 canonical subset（Spec 已說明）。語義不受影響 | 補記修訂表；是否調整措辭由 acceptor 決定 |
| F-3 | Low | Spec Testing 的「本單元另設自己的 CI 路徑過濾」已被 N-10 取代，但 Spec 文字仍在 | 是否經 MATT 流程更新 Spec 文字（不影響 Tickets，Tickets 依第 6 節） |
| F-4 | Low | Spec 沒有帶入 Brief Q38（報告說明 Kaggle 名次不適用、改以預測結果評估）、notebook 六章的檢查、README 內容的檢查，以及未追蹤學號設定的路徑 | 不需要 acceptor 決定：依「以 Brief 為準」由 Ticket derivation 帶入（第 4 節 T-義務）。列出來是為了讓 acceptor 知道 |
| F-5 | Medium | OV-2～OV-5 沒有已接受的 PASS／FAIL 門檻（第 5 節） | phase acceptance 前，決定它們是不是完成 gate，以及門檻（例如對比值） |

## 8. 受影響的工作

- #59：內容不變；本紀錄是它的 derivation。
- 舊的 r4 衍生工作：已依處置紀錄關閉（#50–#56），不受本紀錄影響。
- Ticket derivation：依第 3～6 節與 `decision-20261018-high-risk-categories.md`；前置條件見 `decision-20261018-lane.md` 第 4 節。
- Wireframe v0.2：仍是 UI 參考。CC-1 之後，它的 `TEST.ridge`／`TEST.lasso_ref`（metric_only）與現行語義一致；這些仍是 mock 數值。

## 9. Tickets

- **日期**：2026-10-18。**Binding**：`gov-design-authority`，`claude-opus-5-5`／`high`（預設 mapping，沒有 escalation，沒有替代；由派工者依 Bindings §3.6 核對）。
- **依據**：Spec rev 5（#59；HEAD `a1bd0654`）；Brief @ `dff7c55c`＋CC-1；OC §4 的 AD-1（F-5 的 OV gate 分類）、AD-2（F-3、`/to-tickets` 授權）；acceptor 對 8 張 tracer-bullet 票的核准，以及必要修訂「正式 test 評估只在 T4（#63）執行一次」。
- **票的來源**：MATT `/to-tickets` 產生草稿，已發布為 #60–#67（label `ready-for-agent`，Parent #59）。索引在 [`../../ticket/tickets.md`](../../ticket/tickets.md)。本節是這些票的 DA derivation；它們的 authority 來自本節，不來自 skill。各票 AC 寫「AC 只引用 Spec rev 5 與 DA 義務」，所以下文的分配與 9.4 節的解讀對各票有約束力。我沒有修改任何票。

### 9.1 Ticket 清單與分配

| 票 | 主要 Spec rev 5 章節 | Brief 驗收意圖 | DA 義務（T-義務／G／OV） | 高風險／assurance |
| --- | --- | --- | --- | --- |
| #60 T1 | 資料、計數與前處理；分割與交叉驗證；`model_data` 的 `meta`／`preprocess`／`inputs`／`test_inputs`；單元結構（`.gitignore`、`requirements.txt`）；dashboard 骨架 | §3.1 T-資料、§4、§10 隔離與鎖版本、§11 BR-03、§7 BR-04（骨架） | T-義務：學號設定路徑（BR-03）、notebook 六章標題、外部 URL 靜態掃描（OV-1 前置）；B-14（極端值只用 training）；B-16 路徑 | H-1、H-3；A-1、A-2、A-4 |
| #61 T2 | 指標與推論（秩不足三類）；預測區間；`baselines.allin`／`winners`／`test[ols_subset]` 的結構；dashboard 的 KPI、預測器、test 區塊、Q43 圖 | §3.1 T-預測圖、§6、§7 BR-01、Q43、即時預測器 | G-3 守門（以 fixture 驗證）；OV-6 量測方式內建；B-3（UI 不以 `test_inputs` 評估）；只用 fixture，不碰正式 test | H-2、H-3；A-1～A-3 |
| #62 T3 | 特徵選擇與模型（四個路徑方法、canonical subset、CV winner）；選擇邊界；秩不足；`methods`／`winners`；dashboard 的方法、k、比較全部、提示 | §5、§7 BR-01 第 1、5 點、§10 分組隔離、Q34 | G-2（斷言）；B-1；執行時間（Q34）；只用 fixture | H-3；A-1～A-3 |
| #63 T4 | 對照模型（Ridge／Lasso，CC-1）；p-value backward；Adjusted R²；**唯一一次正式 test 評估**（`ols_subset`＋`metric_only`）；`test` 的不變量；比較表 | §5 最佳定義、指標；§7 BR-01 第 3、4 點；§10 Test 暴露檢查、Python／JS 一致性 | G-1～G-4；B-2（CC-1）；B-3 | H-3；A-1～A-3、A-7 |
| #64 T5 | 診斷與解釋；最終模型；`predict_price()`；pickle；dashboard「方法與限制」；選配係數表 | §3.2 補充建議（五大假設、模型解釋）；§6 診斷；§8 Deployment | B-6（permutation importance 只用於解釋）、B-7 | H-3、H-4；A-1、A-2、A-5 |
| #65 T6 | 報告與打包的報告條款；單元 README；ACCEPTANCE.md | §3.1 T-CRISP-DM、T-GitHub、T-評分（Q38）、§3.2 三種標示、§8、§10 ACCEPTANCE | F-4 的全部 T-義務（Q38、notebook 六章檢查、README 內容檢查）；OV 分類與 NOT TESTED 規則寫入 ACCEPTANCE.md；G-4（報告） | H-2、H-4；A-1、A-5 |
| #66 T7 | Acceptor 輸入與等待；報告 AI 章節 | §3.1 T-AI、§9 | B-15（以漢字計 ≥100） | H-1、H-4；A-4、A-5 |
| #67 T8 | 報告與打包的打包條款；乾淨環境重跑；人工檢查表的全部項目；root 兩列（RB-5） | §3.1 T-繳交、§7 BR-04、§10 全部、§11 BR-03 | OV-1～OV-6（依 AD-1）；B-11（RB-5 逐次授權） | H-1～H-4；A-4、A-6；Spec Integration Audit 的 subject |

A-7（deferral 需要 DA 確認）與 A-8（不宣告 model diversity）適用於全部票。Spec Integration Audit 另外派工（有多張票，不適用 fast path），subject 是 #67 結案時的整合狀態，依 A-2、A-3、A-5、A-6 必核。

### 9.2 依賴

`#60 → #61 → #62 → {#63, #64} → #65 → #66 → #67`。#66 另需 acceptor 輸入（ChatGPT PDF、NotebookLM 材料）；#67 另需學號設定，root 兩列另需 RB-5 授權。並行度 1，執行順序是票號順序。#64 只依賴 #62：最終模型（整體 CV winner）在 #62 就已決定，不需要 test；#64 的 AC 也禁止使用 test 列。

### 9.3 Test 時序的 boundary determination

**判定：在 boundary 內。** 把正式的保留 test 評估延到 #63 一次執行，#61、#62 只用 synthetic fixture 驗證 test 的流程、守門與分層，與已接受的語義一致：

- Brief §4、§5（Q4、Q33、Q20）與 CC-1 (3)(4) 要求 test 在**全部**模型選擇固定之後才評估。Ridge／Lasso 的 alpha 要到 #63 才固定，所以正式評估不可能更早；分散到 #61、#62 反而會違反「選擇固定後」。
- 「每次執行只做一次 test 評估」是**每一次執行**的不變量（Spec 的守門：同一執行內第二次呼叫報錯）。#63 之後的票（#64～#67）在完整重跑 notebook 時會重新執行同一條決定性的評估；這是重現，不是新的評估，條件如下（對各票有約束力）：
  1. 每次完整執行仍然只評估一次，且只評估授權集合（含 CC-1 的 `metric_only`）。
  2. 重跑的 test 結果必須和 #63 記錄的一致（固定 seed 與鎖版本）。若不一致，屬 H-3 事件：停止並 route 給 DA，不得直接採用新數字。
  3. #63 之後，任何會改變 CV 選擇、alpha、前處理、模型集合或授權集合的修改，都不得以 test 結果為理由。這類修改要在 worklog 寫明非 test 的理由，並 route 給 DA 判定是否需要重新評估。
  4. #61、#62 的 fixture 只能出現在測試與暫存產物中；被追蹤的 `model_data`、報告與截圖不得含 fixture 的 test 數字（H-4：mock 或 fixture 不得當成結果）。
  5. #61、#62 執行期間不得讀取正式 test 列做任何評估或決定（兩票的 AC 已要求在 worklog 記錄）。

### 9.4 對票文字的有約束力解讀

| # | 票的文字 | 解讀 |
| --- | --- | --- |
| I-1 | #64：「只用 Fit 的 permutation importance」 | 「Fit」是 r4 的用語（處置紀錄 N-4）；這裡的意思是只用 **training set** |
| I-2 | #64：「依老師補充建議（S-08f、S-08g）」；#65：「與 Brief §2.4.6 表 A 一致」 | 這些 ID 只存在於未接受的 OC v2 草稿（branch `home_work_02-rebaseline-oc-v2`），沒有 authority。改讀為：Brief §3.2（Q9 的補充建議：五大假設、Deployment 的模型解釋）與 Spec「報告與打包」的三種標示對照表。內容一致，只是引用錯誤 |
| I-3 | #61：在報告草稿中寫 PI 的陳述 | 報告檔由 #65 建立；#61 先把陳述寫在 notebook，報告版由 #65 負責 |

### 9.5 覆蓋核對

**Spec rev 5 → 票**：每一節都至少分配到一張票。

- 單元結構與交付物：#60、#65、#67。
- 資料、計數與前處理：#60。
- 分割與交叉驗證：#60、#62。
- 特徵選擇與模型：#61～#64。
- 指標與推論：#61、#63。
- 預測區間：#61、#63。
- 診斷與解釋：#64。
- `model_data`：#60～#63。
- Dashboard：#60～#64、#67。
- 報告與打包：#65～#67。
- Acceptor 輸入：#66、#67。
- 主 seam：#61、#62、#63。
- 次 seam：#60～#64。
- 人工檢查表與 OV 分類：#65 建立，#67 執行。

**Brief §3 必要項目 → 票**：

- T-資料：#60、#65。
- T-模型：#61～#63。
- T-預測圖：#61、#63。
- T-CRISP-DM：#60、#64、#65。
- T-AI：#66。
- T-繳交：#67。
- T-GitHub：#65。
- T-評分（Q38）：#65。
- Dashboard：#60～#64、#67。
- 補充建議（Adjusted R²：#63；五大假設與模型解釋：#64；Ridge／Lasso：#63）與它們的標示：#64、#65。

**缺口（findings）**：

| ID | 嚴重度 | 缺口 | DA 的處理或需要的決定 |
| --- | --- | --- | --- |
| TK-1 | Medium | **GitHub Pages 上的檢查沒有分配給任何票。** Brief §7 要求「同一份檢查也在 GitHub Pages 的網址上做一次」，§10 要求「Pages URL 可開啟」。Pages 只發布 `main`，合併屬 RB-1（acceptor），所以 #67 在合併前無法完成這項檢查 | 需要 acceptor 決定：(a) 合併後由新的 Lightweight work item 執行 Pages 檢查（觸及 H-2，依高風險紀錄第 4 節要做 audit）；或 (b) 其他安排。在決定前，#67 的 ACCEPTANCE.md 把 Pages 一項記為 NOT TESTED（待合併），不得標 PASS；Spec Integration Audit 與 phase acceptance 都要把這項列為待完成 |
| TK-2 | Low | Brief §8 的「結果表 CSV、圖 PNG」（ZIP 也要含結果檔）沒有一張票明確要求產出 | DA 分配：比較表與 test 指標表的 CSV 由 #63 匯出；診斷與解釋圖的 PNG 由 #64 匯出；#65 核對報告引用的圖都來自這些檔案；#67 核對 ZIP 內含它們。建議派工者在 #63、#64、#65 的 body 補上一句（我不改票） |
| TK-3 | Low | 報告必須寫入的兩項陳述沒有在票中點名：exp(ŷ_log) 估計的是條件中位數而不是條件平均（Brief §4、US-26）；CV winner 的 CV 分數有樂觀偏誤，test 才是獨立估計（Spec「分割與交叉驗證」） | DA 分配給 #65（報告），notebook 版由 #61、#62 負責。屬 H-3 與 H-4 的核對範圍 |
| TK-4 | Low | 契約不變量「`methods`／`baselines` 不含任何 test 欄位」沒有明確列在任何一張票的 AC | DA 分配給 #63（主 seam pytest）；結構由 #61、#62 遵守；A-3 本來就要求 Reviewer 核對 |
| TK-5 | Low | #64、#65 引用了未接受草稿的 ID，以及 r4 的用語「Fit」 | 依 9.4 節 I-1、I-2 解讀；建議派工者修正票的文字（我不改票） |

除了上列各項，Spec rev 5 的每條要求與 Brief §3 的每個必要項目都至少對應到一張票。Optional 的 (7) test 殘差表與 (8) 全部結果表沒有分配，因為它們不是完成條件（Brief §3.3）。

## 10. Evidence

- 讀取：Bindings b5；治理 v2.2 §1.2、§2.4、§2.5、§3.3–§3.6、§4.7、§5.1–§5.3；`outcome-contract.md`；`BRIEF.md`（HEAD 與 `dff7c55c`）；`dff7c55c` 的 Grill 紀錄（Q9、Q11、Q20、Q31 等）；`CONTEXT.md`；`SPEC.md` rev 3；`SPEC-review-2026-10-18.md`；`design/WIREFRAME-ACCEPTANCE.md`、`UI-DESIGN-NOTES.md`、`WIREFRAME-REVIEW-CHECKLIST.md`；`design/wireframe/mock-data.js`（第 188–189 行）；SRC-1 轉寫。
- `git diff dff7c55c HEAD -- home_work_02/doc/brief/BRIEF.md home_work_02/CONTEXT.md`；`git log -- home_work_02/CONTEXT.md`（`dea8fd0`）；`sha256sum doc/requirement/*.txt`。
- 寫入的檔案只有本紀錄與兩份同日 decision records；沒有修改 Spec、Brief、CONTEXT、GitHub 或其他檔案；沒有 commit。
- 第 11 節：`outcome-contract.md` §4 CC-1（acceptor 原文）；工作樹對 HEAD `6f14130` 的 `git diff`（BRIEF.md §5、§7 BR-01 第 3–4 點、§14；CONTEXT.md 的 Test evaluation 與 Metric-only model；SPEC.md rev 4）。

## 11. CC-1 的處理（2026-10-18 更新）

- **Binding**：`gov-design-authority`，`claude-opus-5-5`／`high`（預設 mapping，沒有 escalation，沒有替代；由派工者依 Bindings §3.6 核對）。
- **Boundary determination（重述 B-2）**：Ridge 與 Lasso 各做一次最終 test evaluation、只報 USD 的 MAE、MSE、RMSE、R²（`kind = "metric_only"`），**在現行 accepted boundary 內**，條件是同時符合 CC-1 的六項約束：(1) alpha 只用 training CV 選；(2) 不參與整體 CV winner；(3) 每個模型只做一次 test evaluation，dashboard 互動不得重新測試；(4) test 結果不回饋任何選擇；(5) 仍為 metric_only，沒有 PI、coverage 或即時預測；(6) dashboard 與報告清楚區分訓練 CV 指標與 test 指標。範圍只到 F-1：其他模型（含 p-value 對照）、其他 test 結果、任意 k 的 test evaluation 都仍在 boundary 外。CC-1 是 acceptor 核准的 contract change，本紀錄只是承接它，不由 DA 授權。
- **Spec rev 4 與 CC-1 的一致性核對**：契約的形狀是完整的。`test` 的 `metric_only` 只允許 Ridge／Lasso，不含 PI、coverage 或逐筆欄位；`baselines` 中的 Ridge／Lasso 只有 `cv` 與 alpha，沒有 `fit`，所以 dashboard 無法自行重算它們的 test；pytest 會檢查 kind 與欄位一致；Node test 會檢查 `metric_only` 沒有 PI 也不提供預測；Out of Scope 排除「全部 (方法, k) 的 test 評估」。下列是精確的缺口，都不必修改 Spec，由 Ticket derivation 依「以 Brief 為準」補成 AC 或測試：

| # | CC-1 約束 | Spec rev 4 的缺口 | Ticket 義務 |
| --- | --- | --- | --- |
| G-1 | (1) | 沒有測試證明 Ridge／Lasso 的 alpha 搜尋只看到 training 的列 | 次 seam 加一項：改動 test 列的值，選出的 alpha 與 CV 指標都不變 |
| G-2 | (2) | `winners` 不含 Ridge／Lasso 只是由定義推得，沒有明確的測試 | pytest：`winners` 的各方法 winner 與整體 winner 都不含 Ridge／Lasso |
| G-3 | (3)(4) | 「test 評估函式第二次呼叫時報錯」沒有寫明涵蓋 `metric_only`；也沒有寫 test 評估必須在全部 alpha 與 winner 固定之後才執行 | 這個守門條件同樣適用於 Ridge／Lasso；pytest 驗證 test 評估在 alpha 與 winner 固定之後才發生，且每個模型只發生一次；dashboard 不含任何計算 test 指標的程式碼（人工檢查加靜態檢查） |
| G-4 | (6) | Dashboard 一節與人工檢查表的「來源標示」只列 KPI、係數表與 test 區塊，沒有涵蓋放 Ridge／Lasso test 指標的**比較表**；也沒有寫明報告中的標示 | 人工檢查表加一項：比較表的「訓練 CV（USD）」與「Test 評估（USD）」分欄標示；Ridge／Lasso 的 test 指標只出現在比較表（BR-01 第 4 點），不進 test 區塊、KPI 或實際 vs 預測圖。報告的結果表也照同樣方式分開 |
| G-5 | — | `CONTEXT.md` 工作樹中 Test evaluation 詞條的 `_Avoid_: Validation, benchmark` 出現在 Metric-only model 詞條的前後各一次，等於 Metric-only model 底下有兩行 `_Avoid_`（第二行是 Test evaluation 原本的那行沒有刪掉）。這是編輯性瑕疵，不影響語義 | 請派工者或 acceptor 修正；DA 不修改 CONTEXT.md |

- **對 Tickets 的約束**：負責 test 評估的票要把 Ridge／Lasso 的一次性評估納入同一個守門條件（G-3）；負責匯出的票要涵蓋 G-1、G-2；負責 dashboard 與報告的票要涵蓋 G-4，以及「互動不得重新測試」。這些都屬 H-3（高風險紀錄 A-2、A-3）。
- **F-2**：Brief §14 已補記 `dea8fd0` 與 CC-1 對 CONTEXT 的修訂，修訂表部分結案。CONTEXT「CV winner」的措辭建議仍開放（Low，由 acceptor 決定）。
