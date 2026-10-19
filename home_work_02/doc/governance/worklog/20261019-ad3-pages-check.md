# Worklog — AD-3：GitHub Pages 上的 dashboard 檢查與報告第九章連結（Lightweight）

| 欄位 | 內容 |
| --- | --- |
| Work item | AD-3 Pages 檢查（DA `decision-20261019-phase-acceptance-SPEC.md` OI-1；同一 work item 核對 SIA `audit/spec-SPEC-c1-r1.md` F-1／DA OI-2 的兩個連結） |
| Lane | Lightweight（Bindings §4「已結案工作之後的單點修正」；AD-3 指定為合併後的 Lightweight work item）。不是 Formal run `run-20261018-hw2-formal` 的一部分 |
| 日期 | 2026-10-19 |
| Branch | `home_work_02-ad3-pages-check`，自 `origin/main` `5d650b1483bb5f5420af40c3bb88b801238b1bfb`（PR #68 的 merge commit）建立；只在本機 commit，未 push |
| 狀態 | Pages 與連結檢查完成（self-verification）；ACCEPTANCE.md 更新 **BLOCKED**（與既有測試衝突，交 Design Authority，§7、§9 B-1）；independent audit **required（H-2）**，尚未派工 |

## 1. Contract reference

- **Outcome Contract（Lightweight，Bindings §2.3）**：acceptor 2026-10-19 的直接指示，原文：
  > 開始 AD-3：以 Lightweight work item 檢查 GitHub Pages 上的 /home_work_02/ dashboard 與報告的原始碼連結，依 Bindings 派 independent audit。
- **安排的依據**：`doc/governance/outcome-contract.md` AD-3（acceptor 2026-10-18：「TK-1 採 (a)：GitHub Pages URL 的檢查作為合併進 main 之後的 Lightweight work item（觸及 H-2，需 audit）；#67 與 ACCEPTANCE.md 先記 NOT TESTED（pending merge）。」）。
- **檢查項目的來源**：Brief `doc/brief/BRIEF.md` @ `dff7c55c` §7（「同一份檢查也在 GitHub Pages 的網址上做一次（有網路）」）、§10（「Pages URL 可開啟、截圖」）；Spec rev 5 `doc/spec/SPEC.md` 人工檢查表與 SR-09；`doc/acceptance/ACCEPTANCE.md` D-1～D-12、E 節 OV-1～OV-6；SIA F-1；DA OI-1、OI-2。
- **高風險類別**：`decision-20261018-high-risk-categories.md` H-2（dashboard 的 Pages URL 是課堂口頭要求的交付）→ §4 觸發 independent audit；A-1（audit record 寫明觸及的類別）、A-4（H-1 學號與禁止檔案核對）。
- **範圍限制（派工指示）**：只在檢查需要時更新 ACCEPTANCE.md 對應項目；不修改 dashboard、報告內容、notebook、結果或其他實作；缺陷記為 follow-up。

## 2. Executing role and binding reference

- **角色**：Executor（`gov-executor` subagent，由主 session 派工；definition `.claude/agents/gov-executor.md`）。
- **Binding**（Bindings §3.6）：session `4bbff425-7ff9-4cdc-b64c-cc68e824e1b1`，agentId **`a8d232aa45e9e1bb9`**，`meta.json` 的 `agentType`＝`gov-executor`；commit 前觀測 `('claude-opus-5-5', 'high')` 110 則，單一元素，等於 O-1 mapping。全程核對由派工者在採用 return 前執行。
- **Escalation／替代**：無。**Bounded assignments**：未使用。

## 3. 環境與方法

- **機器**：Windows 11 專業版 10.0.26200（acceptor 的電腦，同 #67 的參考環境）。Node v24.19.0。
- **瀏覽器**：Google Chrome **155.0.8059.80**、Microsoft Edge **155.0.4283.62**，**可見視窗**（非 headless），每次執行用新建的暫存 profile（未登入），**網路開啟**，沒有 offline 模擬、resolver 規則或 proxy。
- **腳本**（session scratchpad 的 `ad3/`，不在 repo）：
  - `pages_check.js`：由 #67 的 `ex67/ov67.js` 複製後改為 Pages URL；拿掉離線設定，另記錄每個請求的 host 與 HTTP status。以 CDP 送出真實的滑鼠、滾輪、鍵盤事件。檢查內容與 #67 相同：5 次載入的首次繪製、必要區塊、方法／k 切換、比較全部、預測器輸入與外推警告、散佈圖滾輪縮放／拖曳／按鈕／游標提示、Tab 70 次與鍵盤操作、label 與語意、792 個 DOM 文字的對比、DevTools 375×812（mobile、DPR 2、觸控）與 768×1024 各 8 種狀態的水平溢出。
  - `cold.js`：停用 HTTP 快取，連續 5 次載入，記錄首次繪製與 `model_data.js` 的下載時間（資訊性，見 §5）。
  - `link_open.js`：以新 profile 開啟報告第九章的兩個連結，記錄主文件的 HTTP status、最終 URL、標題、頁面文字與截圖。
- **輸出**：`ad3/chrome/chrome_result.json`、`ad3/edge/edge_result.json`（含每個請求的 URL 與 status）、`ad3/cold_chrome.json`、`ad3/cold_edge.json`、`ad3/links/{chrome,edge}_links.json` 與各處截圖（`ad3/chrome/*.png`、`ad3/edge/*.png`、`ad3/links/*.png`）、`ad3/fetch/`（以 curl 取得的 Pages 檔案）。
- **時間（UTC）**：Chrome 主檢查 10:10:17～10:11:00；Edge 10:11:40～10:12:23；冷啟動量測 10:12:55～10:13:17；連結開啟 10:14:34 起。

## 4. 部署與內容的識別

| 檢查 | 結果 |
| --- | --- |
| `origin/main` | `5d650b1483bb5f5420af40c3bb88b801238b1bfb`（`git fetch` 後；PR #68 的 merge commit） |
| Pages 設定（`gh api repos/.../pages`） | `status: built`，source `main` `/`，`html_url` `https://yotsubamomo.github.io/aiot-classwork/` |
| 最新 Pages build | commit `5d650b1…`，`built`，2026-10-19T10:04:41Z～10:05:38Z |
| GitHub deployments（該 merge commit） | `github-pages` 7170941789：`success`（10:05:46Z）；Vercel `Production` 7170940975：`success`（home_work_01 的專案，與本單元無關，只記錄） |
| Pages 上的檔案 vs `5d650b1` | `index.html`、`assets/style.css`、`assets/vendor/chart.umd.js`、`assets/model_data.js`（9,787,856 bytes）、`assets/hw2core.js`、`assets/app.js`：HTTP 200，**sha256 與 `git show origin/main:home_work_02/<path>` 逐一相同**（例如 `index.html` `1d124102…58f5`、`model_data.js` `6cf0c11e…a7ac`）。`index.html` 只引用這 5 個資源（`grep src=/href=`） |
| `…/home_work_02`（無結尾斜線） | 301 → `…/home_work_02/` |

## 5. Dashboard 檢查（D-1～D-12；E 節在有網路的 Pages 上適用的部分）

| 項目 | Chrome 155.0.8059.80 | Edge 155.0.4283.62 |
| --- | --- | --- |
| D-1 必要區塊 | (1) 方法 5 個、路徑方法 k 18 個、All-in 時沒有 k 按鈕；(2) KPI 4 張；(3) 指標 vs k 圖（Chart.js 實例，7 個 dataset，比較全部時 8 個）；(5) 預測器 18 個輸入、預設點預測 US$503,564、PI US$351,404–US$721,610；(6) 散佈圖 4,323 點與 Test 區塊；(9) 方法與限制（1,788 字）；`load-error` 隱藏；`lang="zh-Hant-TW"` | 同左 |
| D-2 zh-TW 無缺字 | 截圖目視（全頁、模型、Test、預測器、比較全部、375 px Test、散佈圖縮放）：沒有缺字方塊；k 軸 1～18、價格刻度「10 萬／100 萬／1,000 萬」 | 比較全部截圖目視：同左 |
| D-3 方法與 k 切換 | forward、backward、rfe、lasso 切換與 k＝1、9、17、18：KPI、指標圖、預測器欄位數（17／18／1／9）、Test 區塊同步；All-in 時 k 固定 | 同左（數值相同） |
| D-4 比較全部 | 開啟後比較表 8 列、指標圖加上目前選取的 dataset；關閉後隱藏 | 同左 |
| D-5 預測器 | sqft_living 3500 → US$611,588（PI US$426,669–US$876,651）；90000 → 外推警告「超出 training 範圍（290–13540），仍照常計算，屬於外推。」且照常計算 | 同左 |
| D-6、D-7 來源標示與比較表分欄 | 截圖：KPI「訓練 CV（USD）」、全訓練集擬合「R²／Adjusted R² 為 log 尺度」、Test 區塊「Test 評估（USD）」與展示的方法與 k；比較表「訓練 CV（USD）」「Test 評估（USD）」分欄，Ridge／Lasso 只在比較表 | 比較全部截圖：同左 |
| D-8 非 winner 提示 | Lasso k＝1、9、18 時出現提示（Test 區塊展示 Lasso k＝17），k＝17 時沒有；Test 數字只讀自匯出結果（檔案與 `5d650b1` 相同，§4） | 同左 |
| D-9 invalid 候選 | 正式資料沒有 invalid 候選，這一項以 fixture 測試驗證，Pages 上無法重做；Pages 上的程式與資料檔和 `5d650b1` 逐位元相同（§4） | — |
| D-10／OV-6 (b) 互動 | 方法 6 次最大 13.7 ms、k 3 次 7.5 ms、滾輪縮放 10 次 19.2 ms、拖曳 3 次 2.4 ms、縮放按鈕 5 次 ≤ 1.6 ms；互動期間長任務 0；沒有對話框 | 10.3、7.1、25.3、4.0、≤ 3.7 ms；長任務 0；對話框 0 |
| D-10／OV-6 (c)(d)(e)(g) | 預設視圖 y=x 虛線、區間內藍色圓點與區間外橙色方塊可分辨（`chrome_sec_test_lasso_k18_notice.png`）；滾輪 4 次與 8 次後可分辨個別 PI 線段與端點（`chrome_scatter_zoom4.png`、`chrome_scatter_hover.png`）；游標提示「第 15,120 列（房屋 2533300680）預測 US$967,938、實際 US$1,225,000、95% PI US$675,209 – US$1,387,576、落入區間」；`nPoints`＝4,323＝n_test | 同左（提示文字相同；`nPoints` 4,323） |
| D-10／OV-6 (a) 首次繪製（**資訊性**） | 新 profile 第 1 次（含 DNS／TLS 與 9.8 MB 下載）**3,056 ms**；之後 4 次（有快取）38.9、29.6、32.1、35.4 ms；停用快取 5 次：1,631.5、831.3、777.4、712.6、803.0 ms | 新 profile 第 1 次 1,963.6 ms；之後 44.2、35.8、42.1、34.5 ms；停用快取：2,095.2、882.7、1,022.8、833.8、667.3 ms |
| D-11／OV-1 | 離線檢查不適用於有網路的 Pages URL；Pages 對應的是「沒有對外 host 的請求」，見下一列 | — |
| 請求（整段 session） | 64 個：https 55、data 9；https 全部到 `yotsubamomo.github.io`：6 個單元檔案（200，之後的載入來自快取）與瀏覽器自動請求的 **`/favicon.ico` 404**（頁面沒有引用 favicon）；其他 host 0；`loadingFailed` 0 | 同左（64：55／9；其他 host 0） |
| 例外、console error、對話框 | 0、1（就是上面的 favicon 404，來源 `network`）、0 | 0、1（同左）、0 |
| OV-2 375／768 px | 兩個寬度各 8 種狀態水平溢出 **0 px**，沒有超出視窗的元素（`.tablewrap` 除外）；導覽按鈕 `aria-expanded` false →（點擊）true →（Escape）false；預測器 2500 → US$541,221 | 同左 |
| OV-4 | Tab 70 次：69 個停留點（1 次在頁面外）；除了日期輸入（computed outline none，#67 已以截圖確認月日段落反白，本次未重新目視），其餘都是 `:focus-visible`；RFE 按 Enter → rfe；k＝7 按 Space → 7；canvas 上 `+`、`←`、`0` → 3 次互動；比較全部按 Space → `aria-pressed` true；8 個控制項都有 label、28 個按鈕都有名稱、24 個 `aria-pressed`；landmarks 各 1、h1 1、兩個 canvas `role="img"` 並有說明；skip link 存在 | 同左 |
| OV-5 | 792 個 DOM 文字：一般文字最低 6.49:1（winner 標籤 `rgb(22,101,52)` on `rgb(220,252,231)`）、大字最低 16.78:1，不合格 0 | 同左 |

**OV-6 (a) 的判讀**：Spec rev 5 SR-09 的門檻寫明「在參考環境（acceptor 的電腦、目前版本的 Chrome 或 Edge）以 `file://` 開啟時」，OV-6 已在 #67 以 `file://` 通過（ACCEPTANCE E 節）。Brief §7 要求在 Pages 上重做的是同一節列出的離線驗收項目（區塊渲染、方法與 k 切換、預測器、縮放、zh-TW 無缺字、對外請求），不含時間門檻。因此 Pages 上的首次繪製只記錄、不作 PASS／FAIL 判定。Chrome 新 profile 的第一次載入 3,056 ms 超過 3 秒，主要是首次連線與下載 9.8 MB 的 `model_data.js`（Chrome `domContentLoaded` 3,056 ms；停用快取但連線已建立時 0.7～1.6 s）。我把這個判讀列為 concern C-1，供 Reviewer 檢查。

## 6. 報告第九章的連結（SIA F-1；DA OI-2）

| 檢查 | 結果 |
| --- | --- |
| 連結的來源 | `report/report.md` 第九章使用 `{{dashboard_url}}`、`{{repo_url}}`；`hw2/report.py:76-77` 定義為 `https://yotsubamomo.github.io/aiot-classwork/home_work_02/` 與 `https://github.com/yotsubamomo/aiot-classwork/tree/main/home_work_02` |
| 建置出的報告 | 本機 `dist/report/hw2_report.md` 與 `hw2_report.html`（不進 git）各含這兩個 URL 1 次。繳交 ZIP（sha256 `c84a3c5e…3fb6`，與 SIA 記錄的值相同）內的報告 PDF（sha256 `8778b459…bbfe`，與 SIA 相同）有這兩個 URL 的連結註記各 1 個（以 Python 在記憶體中讀 ZIP，檔名不輸出） |
| Dashboard 連結 | curl：200，沒有轉址，標題「King County 房價多元線性回歸分析 — HW2 Dashboard」；Chrome 與 Edge 新 profile：主文件 200、最終 URL 等於連結、標題同上；內容就是 §4、§5 的部署 |
| 原始碼連結 | curl：200，標題「aiot-classwork/home_work_02 at main · yotsubamomo/aiot-classwork · GitHub」；repo 是 `public`（`gh api`），未登入的新 profile（Chrome、Edge）可開啟，主文件 200、最終 URL 等於連結；頁面列出 `assets`、`data`、`design`、`doc`、`hw2`、`report`、`results`、`tests`、`hw2.ipynb`、`index.html`、`README.md`、`requirements.txt` 等，與 `gh api …/contents/home_work_02?ref=main` 一致（`links/chrome_link2.png`） |
| 報告的文字「發布自 repo 的 `main` 分支」 | 與 Pages 設定（source `main` `/`）相符 |
| Dashboard 內的外部連結 | 只有資料集連結 `https://www.kaggle.com/datasets/harlfoxem/housesalesprediction`（curl 200）；其餘是頁內錨點 |
| 結論 | 兩個連結在合併後都可開啟，指向正確內容。SIA F-1 指出的「合併前 404」已不成立；報告是否要加註屬 OI-2 的 acceptor 決定，本 work item 不修改報告 |

## 7. Decisions and assumptions

- 檢查清單沿用 #67 的 D-1～D-11 與 OV-1～OV-6 作法，只把離線條件換成 Pages 的有網路條件；這是 HOW，沒有新增或刪減驗收項目。
- OV-6 (a) 的時間門檻不適用於 Pages（依 Spec SR-09 的明文，§5）。這不是改變語義；若 Reviewer 或 DA 認為 Brief §7 的「同一份檢查」包含 SR-09 (a)，Pages 上的冷啟動數值已全部記錄。
- `/favicon.ico` 404 是瀏覽器對網站根目錄的自動請求，頁面沒有引用；它不屬於任何驗收項目（對外請求為零的要求針對其他 host）。只記為觀察 O-1，沒有修改。
- 不修改 dashboard、報告、notebook、結果或其他實作。
- **ACCEPTANCE.md 沒有更新（停止該部分，BLOCKED → Design Authority）**：我先起草了 B-1 狀態欄、D-12 與 F 節的更新，再跑 `tests/test_report.py`，結果 2 個測試失敗：`test_acceptance_covers_the_brief_spec_and_ov_items`（`tests/test_report.py:266`，要求全文含「NOT TESTED（pending merge）」）與 `test_acceptance_statuses_are_filled_with_evidence`（`:281`，要求 D-12 的狀態以 `**NOT TESTED（pending merge）**` 開頭）。這兩條斷言把 D-12 的狀態固定為合併前的值；要更新 D-12，就得同時修改這些測試。派工指示只授權更新 ACCEPTANCE.md，不授權修改測試或其他實作；修改驗證斷言也可能被視為改變已接受的 verification（impl-default §5）。所以我還原了 ACCEPTANCE.md（`git restore`；還原後 `tests/test_report.py` 42 passed），把起草的變更存成 scratchpad 的 `ad3/proposed_acceptance.patch`（sha256 `66dd694a…bc99`），並把「本 work item 能否修改這兩條斷言（例如改成接受 pending merge 或 AD-3 的結果），還是另開 work item」交給 Design Authority 作 boundary determination。

## 8. Artifacts

| 檔案 | 變更 |
| --- | --- |
| `home_work_02/doc/governance/worklog/20261019-ad3-pages-check.md` | 新增（本檔） |
| `home_work_02/doc/acceptance/ACCEPTANCE.md` | **未修改**（見 §7）；擬議的變更在 `ad3/proposed_acceptance.patch`，D-12 擬寫為 PASS（AD-3 self-verification，audit 待完成），附 subject 與 §4～§6 的結果 |

證據檔都在 session scratchpad 的 `ad3/`，不進 git。

## 9. Verification、audit status、concerns 與 remaining work

- **Verification**：§4～§6。沒有執行的部分：D-9（fixture 項目，Pages 上無法重做）、D-11／OV-1（離線，不適用）、Firefox／Safari、真實觸控裝置、螢幕閱讀器（AD-1 的 best-effort 項目，本 work item 沒有重做）。
- **H-1／A-4 核對**：commit 前以 `.local/packaging.json` 的值（只在記憶體中讀取，不輸出）對全部追蹤檔案與本 branch 的 diff 做 `git grep -F`／比對：結果見本節最後一列。追蹤檔案不含 PDF（老師文件除外）、ZIP、acceptor 材料；本 work item 沒有新增這些檔案。
- **Audit status**：**required**（H-2；`decision-20261018-high-risk-categories.md` §4；acceptor 的指示「依 Bindings 派 independent audit」）。依 Bindings §3.7，由主 session 派 `gov-primary-reviewer`；Executor 不自行派工。受審 subject：branch `home_work_02-ad3-pages-check` 的 commit（見 return）＋ Pages 部署 `5d650b1`。Audit record 位置：`doc/governance/audit/20261019-ad3-pages-check-c1-r1.md`。尚未派工。
- **Concerns**：
  - **C-1**：OV-6 (a) 是否適用於 Pages 的判讀（§5、§7）。依 Spec 明文判為不適用；若有不同解讀，屬 Design Authority 的語義裁決。
  - **C-2**：本 work item 的一次 `ls dist/` 把含學號的 ZIP 檔名印到這個 subagent 的終端輸出（session transcript，本機 `~/.claude/projects/…`，不在 repo、不在任何證據檔）。沒有寫入任何追蹤檔案或 scratchpad 的證據檔；之後所有讀 ZIP 的指令都不輸出檔名。依 H-1 的「終端輸出」涵蓋範圍如實記錄。
  - **O-1**（觀察，非缺陷）：瀏覽器自動請求 `https://yotsubamomo.github.io/favicon.ico` 得到 404，console 記 1 則 network error。若 acceptor 要消除，需要新增 favicon 或 `<link rel="icon">`，屬修改 dashboard 的新 work item（H-2 → audit）。
  - **B-1（BLOCKED，required authority＝Design Authority）**：ACCEPTANCE.md D-12 的更新與 `tests/test_report.py:266`、`:281` 衝突（§7）。DA 需要判定這兩條斷言的修改是否在本 work item 的 boundary 內；若不在，由新的 work item（或 acceptor 的重新授權）處理。在此之前 ACCEPTANCE.md 的 D-12 仍記 NOT TESTED（pending merge），Pages 檢查的結果以本 worklog 為準。
- **Remaining work**：B-1 的 DA 判定與之後的 ACCEPTANCE.md 更新；independent audit（R1）派工與 closure（主 session，Bindings §3.7）；之後 OI-1 才可結案；OI-2 是否在報告加註仍由 acceptor 決定。本 branch 未 push（push 屬 SA-1，由派工者決定）。
- **學號核對結果（A-4）**：已核對、無命中——全部追蹤檔案 `git grep -c -F` 0 個檔案；本次 staged diff 0；scratchpad `ad3/` 的 60 個證據檔（不含瀏覽器暫存 profile）0；`git ls-files` 中 `.zip`、`acceptor_materials`、`packaging.json` 0。比對值只在記憶體中讀自 `.local/packaging.json`。
