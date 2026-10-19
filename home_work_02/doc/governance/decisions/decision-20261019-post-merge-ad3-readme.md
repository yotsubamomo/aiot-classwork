# Decision record — 合併後的兩個 Lightweight work items：AD-3 的 D-12 與測試、Pages 載入時間、README 改版與學號設定

- **紀錄類型**：Design Authority decision record（治理 §1.2、§2.4、§3.3、§3.6-A、§5.3 第 2 類；Bindings b5 §2.3、§4、§5、§7）
- **日期**：2026-10-19
- **背景**：HW2 已經由 PR #68 合併進 `main`（merge commit `5d650b1483bb5f5420af40c3bb88b801238b1bfb`）。Formal run `run-20261018-hw2-formal` 已經結束（run record §21）。以下兩個 work item 都走 Lightweight，各自以 acceptor 的直接指示作為 Outcome Contract（Bindings §2.3、§4「已結案工作之後的單點修正」）：
  - `20261019-ad3-pages-check`：branch `home_work_02-ad3-pages-check`，commit `6975e22`，worklog `doc/governance/worklog/20261019-ad3-pages-check.md`。
  - `20261019-readme-restructure`：尚未開始。
- **問題來源**：
  - Q1、Q2：AD-3 Executor 在 worklog §7、§9 提出 B-1 與 C-1，指名要由 Design Authority 判定。
  - Q3：acceptor 2026-10-19 的直接指示改變了我先前 derive 的一項義務。原文逐字：「README的調整, 請調整README , 參考homework 01 ，學號設定（打包用)的資料不要加入，」
- **Binding**：`gov-design-authority`（預設 mapping 是 `claude-opus-5-5`／`high`，沒有 escalation，也沒有替代）。本紀錄不自己證明 binding，由派工者依 Bindings §3.6 核對。
- **Capability escalation**：不提出。
  - E-DA/D1 不成立：三個問題都能用 Spec rev 5、Brief、AD-3 的原文，以及 #67 的先例裁決，沒有「兩種後果不同、而現有證據無法裁決」的設計選擇。
  - E-DA/D2 不成立：我先前的決定沒有被 FA ruling 或經 route 的 Reviewer finding 推翻或爭議。Q3 的起因是 acceptor 的指示，不屬於 D2。
- **獨立性**：派工摘要、Executor 的 worklog 與它擬的 patch，我都只當作待驗證的主張。依據是第 4 節列出、我自己讀過的原文與檔案。

---

## 1. Q1 — AD-3 work item 能否把 D-12 和兩條測試斷言一起更新

### 1.1 依據

| 來源 | 內容 |
| --- | --- |
| OC §4 AD-3（acceptor 原文） | 「GitHub Pages URL 的檢查作為合併進 main 之後的 Lightweight work item（觸及 H-2，需 audit）；#67 與 ACCEPTANCE.md **先記** NOT TESTED（pending merge）。」 |
| AD-3 work item 的 Outcome Contract（worklog §1，acceptor 原文） | 「開始 AD-3：以 Lightweight work item 檢查 GitHub Pages 上的 /home_work_02/ dashboard 與報告的原始碼連結，依 Bindings 派 independent audit。」 |
| Brief §8、§10 | ACCEPTANCE.md 是交付物：每條要求對應到可觀察的檢查與證據位置 |
| `tests/test_report.py:266`、`:281`（`e2780f4`） | `assert "NOT TESTED（pending merge）" in ACCEPTANCE`；`assert statuses["D-12"].startswith("**NOT TESTED（pending merge）**")` |
| 先例 `e2780f4`（#67） | #67 驗證完成後，把 #65 的「驗證前一律不得 PASS」改成「驗證後每列都有狀態與證據」。commit message：the pre-verification guard「becomes, once #67 has verified」the post-verification rule |
| impl-default v2 §5 | 不得以弱化 accepted verification 的方式取得通過；例外要有 accepted contract 或 authorized decision 作為依據 |
| ACCEPTANCE「狀態的規則」 | PASS 的意思是：已在所列 subject 上執行檢查、結果相符、證據位置可以開啟 |

### 1.2 判斷

- 兩條斷言的作用，是把 AD-3「先記 NOT TESTED（pending merge）」這個**過渡狀態**機械化，防止合併前有人把 Pages 項目標成 PASS。它們不是另一條獨立的 accepted verification。「先記」本身就預告：合併、執行檢查之後，狀態要改寫成實際結果。現在合併已經發生，檢查也已在 `5d650b1` 的 Pages 部署上執行，過渡狀態成立的前提已經消失。
- 把 D-12 的檢查結果記進 ACCEPTANCE.md，是 AD-3 work item 結果的一部分。如果 D-12 一直停在 NOT TESTED，交付的驗收清單就會和事實不符。所以更新 D-12 屬於該 work item 的 intent。跟著改兩條斷言，是同一個轉換的必然結果，與 #67 的先例同型。
- 改法不是放寬，而是把「必須仍在等待」換成「必須是有證據、有 subject 的實際結果」，而且合併前的狀態不可能通過新的斷言。這屬於 derived verification 的修訂（治理 §5.3 第 2 類），由本紀錄授權（impl-default §5 所說的 authorized decision）。

### 1.3 裁決

**可以。** AD-3 work item（同一個 worklog identity、同一個 branch）可以把 ACCEPTANCE.md 的 D-12、B-1 狀態欄和 F 節的 Pages 那一點，與 `tests/test_report.py` 這兩條斷言一起更新。條件是同時符合 P-1～P-4，並在 independent audit 的受審 subject 內。

**P-1 新的斷言必須強制以下各點**（寫法屬 Executor 的 HOW，語義不得少於下列各項）：

| # | 取代 | 必須強制的內容 |
| --- | --- | --- |
| T-1 | `:266` | ACCEPTANCE.md 中，A～E 節與 OV 各列（也就是 `statuses` 取得的每一個狀態欄）**都不含** `pending merge`。這同時涵蓋 D-12 與 B-1。「狀態的規則」表中的說明文字不在範圍內。 |
| T-2 | `:281` | `statuses["D-12"]` 以 `**PASS**` 開頭。 |
| T-3 | `:281`（追加） | `statuses["D-12"]` 含 AD-3 worklog 的路徑 `doc/governance/worklog/20261019-ad3-pages-check.md`。 |
| T-4 | `:281`（追加） | `statuses["D-12"]` 以 40 位十六進位的完整 SHA 記錄受檢的 `main` commit（regex `[0-9a-f]{40}`），而且含 `github-pages`，表示受檢的是該 commit 觸發的 Pages 部署。這與 #67 的 subject 斷言採同一個強度。 |
| T-5 | 不變 | 同一個函式中的其他斷言都保留，包括：PASS／FAIL 要有證據 regex、沒有 PENDING、OV-2～OV-4 的 best-effort 記 NOT TESTED、#67 subject 的 40 位 SHA、OV-6 量測表已填。同一個檔案的其他測試也都不得刪除、skip、xfail 或放寬。本 work item 對 `tests/` 的 diff，只限上列兩處斷言，以及隨之更新的 docstring 或註解。 |

**P-2 D-12 等狀態欄的內容**（由 Reviewer 核對，不另寫測試）：

- D-12 寫 PASS，並寫明以下內容：
  - 受檢 subject：`main` @ `5d650b1483bb5f5420af40c3bb88b801238b1bfb` 觸發的 `github-pages` 部署 7170941789，以及 Pages 上的檔案與該 commit 逐一相同。
  - 瀏覽器名稱與版本、條件（新 profile、有網路）。
  - 引用 worklog §4～§6。
  - D-9（fixture 項目）、D-11／OV-1（離線）不適用於 Pages，要寫明。
  - D-10 (a) 依本紀錄第 2 節只記錄數值，要寫明，並附上實測值。
  - `/favicon.ico` 404 是瀏覽器對同一個 origin 自動發出的請求，頁面沒有引用它，所以不是「對外請求」（Brief §7 的對外是指其他 host）。這一點記為觀察。
  - 報告第九章的兩個連結在合併後都可以開啟。
- D-12 **不得寫入會過時的 audit 狀態**，例如「independent audit 待完成」。audit 狀態與 record 路徑由 worklog 承載。B-1 的狀態欄改寫為「Pages URL 見 D-12」，不再重複狀態。
- F 節可以寫「OI-1 在 AD-3 的 audit closure 後結案」這類條件句。
- Executor 在 scratchpad 擬的 `proposed_acceptance.patch`，除了上述兩點（D-12、B-1 的 audit 狀態措辭，以及 D-12 只寫短 SHA `5d650b1`）以外，內容符合本項。

**P-3 Self-verification**：在最終 commit 上執行完整的 `pytest`，結果與指令記入 worklog §9。`test_repo_hygiene.py` 的學號比對必須實際執行，不能是 skip（設定檔存在於 acceptor 的電腦）。A-4 的比對範圍要涵蓋本 work item 的全部 commit。

**P-4 Audit**：仍然 **required**（H-2，`decision-20261018-high-risk-categories.md` §4，以及 acceptor 的指示）。受審 subject 是本 branch 含 ACCEPTANCE.md 與測試變更的最終 commit，加上 Pages 部署 `5d650b1`。R1 要以本紀錄 P-1 核對新斷言沒有比 T-1～T-5 更弱，並把本紀錄第 2 節列入 D-10 (a) 的判讀依據。

### 1.4 是否改變 accepted 語義

**否。** AD-3、Brief §7、§10 與 Spec 的人工檢查表都不變。被修訂的，只是 #65、#67 為了 AD-3 過渡狀態寫下的 derived 測試斷言，屬治理 §5.3 第 2 類。不需要 acceptor 核准。

### 1.5 需要的工作與負責人

| 工作 | 負責人 |
| --- | --- |
| 把本紀錄交給 AD-3 Executor，續派同一個 work item（worklog 記錄本紀錄是 B-1 的解除依據） | 派工者（主 session） |
| 依 P-1～P-3 更新 ACCEPTANCE.md 與兩條斷言、執行 self-verification、更新 worklog §7、§9 | AD-3 Executor（`gov-executor`） |
| R1（`gov-primary-reviewer`，fresh context），record 寫在 `doc/governance/audit/20261019-ad3-pages-check-c1-r1.md` | 派工者依 Bindings §3.7 派工；Reviewer 自己寫 record |
| Push（SA-1）；合併（RB-1：OC 沒有 opt-in SA-3） | Push 屬派工者；合併屬 acceptor |

---

## 2. Q2 — 3 秒首次繪製門檻是否適用於 Pages

### 2.1 依據

- **Spec rev 5「Dashboard」SR-09**：「在參考環境（acceptor 的電腦、目前版本的 Chrome 或 Edge）**以 `file://` 開啟時**，(a) 首次繪製 ≤ 3 秒……」。
- **AD-1**（acceptor 原文）：「OV-1 完全離線 file:// 與 OV-6 全部 Test PI 渲染效能，仍為原定硬性 PASS／FAIL gate，不降級。」OV-6 就是 Spec 定義的 SR-09 (a)～(g)（`design/WIREFRAME-ACCEPTANCE.md` 的 OV-6「對應 Spec SR-09」）。
- **Brief §7**：
  - 「同一份檢查也在 GitHub Pages 的網址上做一次（有網路）」放在 BR-04 離線驗收那一組條目裡。該組條目的「同一份檢查」列的是：區塊渲染、方法與 k 切換、預測器、縮放、zh-TW 無缺字、對外請求、資料與程式庫都在包內。**沒有時間門檻。**
  - §7 Q43 的「可讀可操作，不得嚴重遮蔽或卡頓」與環境無關。
- **Spec 人工檢查表**把「(a)～(e)」與「Pages URL」列為兩個不同的項目。
- **AD-3 worklog §5 的實測**：
  - Chrome 新 profile 第一次載入 3,056 ms。這次包含 DNS／TLS，以及下載 9.8 MB 的 `model_data.js`。
  - 停用快取、但連線已建立時：0.7～1.6 s（Chrome）、0.67～2.1 s（Edge）。
  - 有快取時：約 30～44 ms。
  - 互動（方法、k、縮放、拖曳）最長 25.3 ms，長任務 0，沒有對話框。
- **Run record §14 第 8 點後的 acceptor 指示**：「不新增功能、不重開設計決策」。

### 2.2 裁決

1. **SR-09 (a) 的 3 秒門檻，在 Pages 上不是 PASS／FAIL gate。** Spec 原文把它限定在參考環境、以 `file://` 開啟。AD-1 的硬性 gate 指的就是這個定義。Brief §7 要在 Pages 上重做的那份檢查，本身不含時間門檻。這是既有文字只有一種合理讀法而尚未寫明的情況（治理 §3.6-A）。把門檻延伸到 Pages，等於新增一個 gate：它的量測會受網路、DNS、CDN 與快取影響，無法回到參考環境重現。那是新的 requirement，不是對既有語義的解讀。
2. **在 Pages 上仍然適用的是 Brief Q43 的「可讀可操作、不得嚴重遮蔽或卡頓」。** worklog 的 D-10 (b)～(e)(g) 實測（互動最長 25.3 ms、長任務 0、沒有「網頁沒有回應」、逐筆 PI 與游標提示可辨識、`nPoints` 等於 n_test）就是它在 Pages 上的證據。evidence 是否足夠，由 R1 判定。
3. **Pages 上的首次繪製與冷啟動數值一律只作紀錄**：寫在 worklog 與 D-12（P-2），不寫 PASS 或 FAIL，也不建立 follow-up。OV-6 (a) 在 `file://` 上的 PASS（ACCEPTANCE E 節，#67）維持不變。
4. 這項裁決不重開任何設計決定：SR-09、AD-1 與 dashboard 的資料載入方式都不變，符合 run record §14 的 acceptor 指示。如果 acceptor 想對 Pages 的載入時間另訂目標，那是新的 requirement，要以新的 Outcome Contract 由 acceptor 自己提出。本紀錄不把它列為 tracked item。

### 2.3 是否改變 accepted 語義

**否。** 本項只寫明既有門檻的適用範圍（第 3.6-A 類 clarification）。AD-3 worklog 的 C-1 依本項處理，不需要 acceptor。

### 2.4 需要的工作與負責人

- **AD-3 Executor**：依 P-2 在 D-12 寫明 (a) 只作紀錄並引用本紀錄；worklog §7 的 C-1 註記「依本紀錄第 2 節」。
- **R1**：以本項作為判讀依據。

---

## 3. Q3 — README 改版：學號設定這項 derived 義務如何改變

### 3.1 依據

| 來源 | 內容 | 地位 |
| --- | --- | --- |
| Brief §8 README 列（accepted） | 「目的、資料來源與授權、流程、成果、重跑步驟、dashboard 連結、檔案配置」 | accepted 語義，**不含**學號設定 |
| Brief §11 BR-03（accepted） | 追蹤檔案一律 `<學號>`；實際值只放在本機未追蹤的打包設定（路徑由 Spec 指定，並加入單元 `.gitignore`）與繳交 ZIP；打包步驟從設定讀取；驗收時以 `git grep` 確認 | accepted 語義，**不要求** README 記載設定 |
| `derivation-SPEC.md` §4 最後一列、§7 F-4 | T-義務：由 Ticket derivation 固定設定路徑，並加入 `.gitignore` | derived |
| #60 AC（經 derivation §9 採納） | 「本票固定未追蹤學號設定的路徑**並寫入 README 重跑說明**（DA T-義務 BR-03）」 | derived（本項要修訂的對象） |
| #65 本文 | 單元 README 的「重跑步驟含學號設定路徑」 | derived |
| ACCEPTANCE A-8 | 檢查文字是「重跑步驟（含學號設定路徑 `.local/packaging.json`）」 | derived 檢查 |
| `tests/test_report.py:203-212` | 要求 heading「學號設定（打包用）」、`".local/packaging.json" in README` 與 `"<學號>" in README` | derived 測試 |
| `hw2/local_config.py:31`、`hw2/paths.py:29-31`、`hw2/package.py:10`、`.gitignore:13`、`tests/test_repo_hygiene.py` | 設定不存在時，錯誤訊息會寫出路徑與格式；設定被 git 忽略；學號比對涵蓋所有追蹤檔案（含 README） | 實作（不變） |
| acceptor 2026-10-19 指示 | 「學號設定（打包用)的資料不要加入」 | 本 work item 的 Outcome Contract |

### 3.2 判斷

- acceptor 引用的，正是 README 現有小節的標題「學號設定（打包用）」。「不要加入」最合理的讀法是：改版後的 README 不帶入這部分內容。我沒有找到第二種會導致不同交付的合理讀法。另一種讀法是「不要在仿 HW01 的『專案資料』中加入學號」；在這種讀法下，同樣要求 README 不含學號設定資料，結論相同。
- 要求 README 記載設定路徑，只是 #60、#65 的 derived 義務。Brief §8、BR-03 都沒有這項要求。BR-03 的保護靠的是 `.gitignore`、`git grep` 比對與打包程式拒收佔位值，這些都不依賴 README。因此移除這項記載不改變 accepted 語義，而且 H-1 的控制沒有減少：真正的學號比對 `test_no_tracked_file_contains_the_student_id` 不變，而且仍然涵蓋 README。
- 打包只由 acceptor 本人在自己的電腦執行，設定檔已經存在（run record §19）。設定缺少時，`hw2/local_config.py` 的錯誤訊息會寫出路徑與格式。所以 README 不再記載，不影響可操作性。

### 3.3 裁決

**D-R1 derived 義務的修訂**（治理 §5.3 第 2 類，自本紀錄起適用於 `20261019-readme-restructure` 與之後的工作）：

- #60 AC 中「並寫入 README 重跑說明」、#65 的「重跑步驟含學號設定路徑」，以及 ACCEPTANCE A-8 的「（含學號設定路徑 `.local/packaging.json`）」，**改為：單元 README 不記載學號設定。**
- 「固定設定路徑並加入 `.gitignore`」這個部分不變。
- 已結案的 #60、#65 不重開，也不修改票文。它們對當時 subject 的結案證據仍然有效。

**D-R2 README 的內容限制**（屬於改版 work item 的範圍）：

1. **必須移除**：
   - 「學號設定（打包用）」這個小節（標題與內容）。
   - 「本機、不進 git 的設定與材料」表中的 `.local/packaging.json` 列。
   - 任何設定檔的路徑、檔名、JSON 鍵或格式，以及建立或填寫設定的說明。
   - 改版後的 README 不得含有字串 `學號設定`、`packaging.json`、`student_id`、`.local/`。
2. **可以保留**（Executor 自行決定）：
   - 交付物檔名的 `<學號>` 佔位，例如 `<學號>_hw2.zip`。
   - 敘述性的「學號 ZIP」。
   - `python -m hw2.package` 這一行。如果保留，只能寫成「作者繳交前的打包步驟，需要本機、不進 git 的輸入」，不得帶出第 1 點的任何內容。
3. **必須維持**：
   - Brief §8 README 的七項：目的、資料來源與授權、流程（CRISP-DM）、成果、重跑步驟、dashboard 連結（Pages URL）、檔案配置。
   - 三種標示：dashboard 是課堂口頭要求；採用的補充建議標「依老師補充建議」。
   - 「唯一一次正式評估、重跑是重現」的陳述。
   - 數字單一來源（C-13）。
   - 不含 mock、wireframe 或 fixture 的數字或截圖（H-4）。
   - 仿 HW01 新增的內容（例如專案資料、Live Demo、作業要求對應、技術棧）同樣受上述規則約束。新增的區段如果陳述結果數字，必須被數字核對測試涵蓋（RT-5）。
4. **截圖**（如果仿 HW01 加入）：
   - 只能擷取自真實的 dashboard：Pages URL，或 repo 內的 `index.html`。
   - **不得擷取自解壓後的 ZIP 資料夾**：路徑含實際學號（參照 #67 R1 F-2）。也不得擷取自 `hw2.fixture` 的複本。
   - 畫面不得含瀏覽器網址列、本機路徑或帳號。
   - 圖檔放在單元目錄內，加入前要逐張目視確認沒有學號（A-4 的 byte 比對看不到圖片中的文字）。
5. **非範圍**：
   - `hw2/**`（含 `package.py`、`local_config.py`）、`.gitignore`、報告、notebook、dashboard、results、root 檔案（RB-5），以及重新打包。
   - OI-3、OI-4 不因本 work item 處理。
6. **Release gate**（Bindings §5）：
   - 如果重跑步驟的指令只是移除或沿用（不新增、不修改任何指令），引用既有的實跑證據（`worklog/issue-67.md` §7、SIA §4.1）即可。
   - 任何新增或修改的指令都必須實際執行，結果記入 worklog。
7. **HW01 風格**：
   - 「參考 homework 01」的結構選擇屬 HOW。worklog 要列出採用了 HW01 README 的哪些結構元素。
   - 版面是否符合 acceptor 的期待，由 acceptor 自己檢視，不是設計語義的判準。

**D-R3 README 測試必須強制的內容**（修改 `tests/test_report.py` 的 README 測試；寫法屬 HOW）：

| # | 內容 |
| --- | --- |
| RT-1 | 從 `test_readme_has_every_required_item` 移除 heading「學號設定（打包用）」，以及 `.local/packaging.json`、`<學號>` 必須出現的斷言。 |
| RT-2 | 新增：README 不含 `學號設定`、`packaging.json`、`student_id`、`.local/`。 |
| RT-3 | 新增佔位規則：README 中每個帶前綴的繳交檔名（`…_hw2.ipynb`、`…_hw2.zip`），前綴都必須正好是 `<學號>`。`<學號>` 本身是否出現**不再要求**；如果出現，只能是這個佔位形式。 |
| RT-4 | 新增不依賴設定檔的防線：README 中「學號」之後 12 個字元以內，沒有 7 位以上連續數字。實際值的精確比對仍由 `tests/test_repo_hygiene.py::test_no_tracked_file_contains_the_student_id` 負責（不修改；涵蓋 README）。Executor 與 Reviewer 的驗證中，它必須實際執行，不得是 skip。 |
| RT-5 | 保留：Brief §8 七項各對應一個 README heading（一對一，七個互不相同的 heading；改名時更新清單，不得合併或刪去任何一項）、Pages URL、`python -m hw2.report`、六個 CRISP-DM 階段名稱。以 heading 定位區段的測試（`## 成果`、`## 資料來源與授權`、`## 目的`）可以改指向改名後的同一內容區段，斷言不得減少。數字核對必須涵蓋 README 中每一個陳述結果數字的區段。`test_readme_states_the_one_formal_evaluation_and_reruns_as_reproduction` 與 `test_readme_does_not_present_the_method_comparison_as_a_requirement` 的斷言不變。 |
| RT-6 | 其他測試都不得刪除、skip、xfail 或放寬。 |

**D-R4 ACCEPTANCE.md A-8**：

- 檢查文字刪去「（含學號設定路徑 `.local/packaging.json`）」，並在要求清單後加註「不記載學號設定（DA `decision-20261019-post-merge-ad3-readme.md` D-R1）」。
- 狀態以本 work item 在新 subject 上的證據（worklog）重新填寫。
- A-7、C-16 不變：ACCEPTANCE.md 不是 README，acceptor 的指示只涉及 README。
- 如果 A-8 的文字被 `test_report.py` 檢查，依 RT-6 同步，不得放寬。

**D-R5 打包說明的位置**：**不新增任何地方。** 它留在原本就有的位置：

- `hw2/local_config.py`：docstring，以及設定缺少時的錯誤訊息（含路徑與格式）。
- `hw2/paths.py` 的註解、`hw2/package.py` 的 docstring。
- `.gitignore`。
- `tests/test_repo_hygiene.py`。
- ACCEPTANCE A-7、C-16。
- 治理紀錄：`decision-20261018-issue60-a4-student-id.md` S-3、run record §19。

不得另建追蹤文件來搬移被移出 README 的內容，因為那等於換一個地方「加入」。也不需要建立未追蹤的說明檔。

### 3.4 是否改變 accepted 語義

**否。** Brief §8 的 README 項目、BR-03 的規則與 `git grep` 驗收都不變。被修訂的是 derived 義務（#60、#65 的 README 部分、ACCEPTANCE A-8 的檢查文字、README 測試），屬治理 §5.3 第 2 類。

acceptor 的指示是這個 work item 的 Outcome Contract，本紀錄只讓 derived contract 與它一致。修改測試與 A-8，是完成這個 work item 的必然結果，仍在 boundary 內。

### 3.5 Lane、assurance、負責人

- **Lane**：Lightweight。一個 execution unit，契約在本紀錄的限制下已經清楚。
- **Audit**：**required**。觸及 H-2（README 的流程與成果）與 H-1（學號設定的記載）。
  - R1 由 `gov-primary-reviewer` 執行，record 寫在 `doc/governance/audit/20261019-readme-restructure-c1-r1.md`。
  - R1 要核對 D-R2、RT-1～RT-6，並自己執行 A-4 的學號比對。
- **負責人**：
  - Executor（`gov-executor`，或符合 Bindings §3.5 條件的 direct-execution session）：在 worklog 逐字引用 acceptor 原文。
  - 派工者：派 R1、push（SA-1）。
  - acceptor：合併（RB-1）。
- **與 AD-3 的重疊**：兩個 work item 都會修改 `tests/test_report.py`（不同的函式）與 `ACCEPTANCE.md`（不同的列）。派工者要安排先後，或者在後合併的那一個處理衝突。這屬於控制面的 HOW。

---

## 4. 受影響的 work items 與 evidence

| 對象 | 影響 |
| --- | --- |
| `20261019-ad3-pages-check` | B-1 解除（第 1 節）。C-1 依第 2 節處理。依 P-1～P-4 續做，audit 照常 required。OI-1 在 R1 closure 後結案 |
| `20261019-readme-restructure` | 依第 3 節執行。audit required |
| #60、#65（CLOSED） | 不重開。README 的那部分 derived 義務自本紀錄起被 D-R1 取代，既有結案證據仍然有效 |
| `ACCEPTANCE.md` | D-12、B-1、F（AD-3 work item 負責）；A-8（README work item 負責） |
| `tests/test_report.py` | `:266`、`:281`（AD-3）；README 測試（README work item） |
| 繳交 ZIP（`c84a3c5e…3fb6`） | 不受影響。其中的 README 是舊版，含學號設定小節，但只有 `<學號>` 佔位、沒有實際值（SIA H-1、S-5） |
| Spec、Brief、Outcome Contract、`derivation-SPEC.md`、程式 | 不修改 |

## 5. 需要其他 authority

- **Acceptor（既有保留事項，不是本紀錄新增的 gate）**：
  1. 兩個 work item 的合併（RB-1：OC 沒有 opt-in SA-3）。
  2. **是否重新打包 ZIP**，讓繳交物帶上改版後的 README。目前的 ZIP 不含實際學號，不重新打包也不違反 BR-03。如果要重新打包，那是新的 work item，觸及 H-1、H-2 與 OI-3，需要 audit。繳交本身屬 RB-2。
  3. README 改版是否符合「參考 homework 01」的期待，由 acceptor 自己檢視。
- 不需要 contract change，不需要 escalation。

## 6. Evidence

- **讀取**：
  - Bindings b5（全文）；治理 v2.2 §1.2、§1.5、§2.1、§2.4、§2.5、§3.1、§3.3～§3.6、§3.8、§5.1～§5.3；impl-default v2 §5。
  - `outcome-contract.md`（CC-1、AD-1～AD-3）；`BRIEF.md`（全文）；`SPEC.md` rev 5（Dashboard、報告與打包、Acceptor 輸入、Testing Decisions、人工檢查表）；`design/WIREFRAME-ACCEPTANCE.md`。
  - `derivation-SPEC.md`（全文）；`decision-20261018-issue60-a4-student-id.md`；`decision-20261018-high-risk-categories.md`；`decision-20261019-phase-acceptance-SPEC.md`；`audit/spec-SPEC-c1-r1.md`（F-1、H-1、H-2、§3.2）；run record §1、§14、§19～§21。
  - `worklog/20261019-ad3-pages-check.md`；scratchpad `ad3/proposed_acceptance.patch`。
  - `ACCEPTANCE.md`；`README.md`；`tests/test_report.py:1-60、195-285、340-350`；`tests/test_repo_hygiene.py`；`hw2/local_config.py`、`hw2/paths.py`、`hw2/package.py` 中學號相關的行；`git show origin/main:home_work_01/README.md`。
  - `gh issue view 60／65／67` 中 README、學號設定與 Pages 相關的 AC。
- **Git**：
  - `git log -S` 確認 `:266`、`:281` 的斷言來自 `741a21b`（#65）與 `e2780f4`（#67）。
  - `git show e2780f4`（#67 把驗證前規則改為驗證後規則的先例）。
  - `home_work_02-ad3-pages-check` 的 HEAD 是 `6975e22`，其 parent 是 `5d650b1`。
- **寫入**：只寫入本紀錄（未 commit）。沒有修改程式、測試、票、Spec、Outcome Contract、ACCEPTANCE.md 或其他紀錄。
