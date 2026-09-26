# Audit record — Issue #39，cycle 1，R1（Formal Ticket independent audit）

| 欄位 | 內容 |
| --- | --- |
| Work Contract | GitHub Issue **#39**（`yotsubamomo/aiot-classwork`）「地圖圍欄與響應式可用性：pan／zoom 圍欄、初始視野、375 px 底部資訊面、44×44、768 px 破版檢查」（`gh issue view 39`：OPEN，label `ready-for-agent`，blocked-by #38（已 CLOSED））。上位：V2 Outcome Contract `home_work_01/doc/governance/outcome-contract-v2.md`（ACCEPTED 2026-09-25，normative candidate `69c5a04`；S-1、S-4、S-8、S-9、S-10、AB-V2-7、AB-V2-8）；Delta Spec `home_work_01/doc/spec/SPEC-V2.md` **v2.2**（§2.6 R-V2-MAP-1～5、R-V2-RSP-1～8；R-V2-DD-9(e)；R-V2-DOC-1(8)；§5.3 儀器；§6.2；§6.3 AC-19 列；INV-V2-8／9）；derivation record `derivation-SPEC-V2.md`（DV-8、DV-11、B-4、B-20、TB-V2-6、§15）；V1 Spec v1.1 R-EN-1、R-EN-4、AC-17～AC-19、INV-4；V1 DR-20 P-12；`decisions/decision-20260923-high-risk-categories.md`（A-1）。本票分配：AC-V2-13、AC-V2-14、AC-V2-15（完整：資訊面開合＋resize；#36 模式切換守衛維持）、§6.3 AC-19（R-EN-1 六項、375 無橫向捲動、三種狀態截圖）、AC-V2-20（本票範圍：CI 全綠）、README R-V2-DOC-1(8)。Out of scope：#40 Radar；附錄 A 樣式建議；瀏覽器歷史、`prefers-reduced-motion`。 |
| 受審 subject | branch `home_work_01-v2-implementation`；BASE **`4651d33`** .. HEAD **`049ff6a`**；code anchor **`ae0b9dc7211887b34ec51369509751e0042569c2`**。`ae0b9dc..049ff6a` 只改 `doc/governance/worklog/issue-39.md`；審查時本機 HEAD `55d454f`（`049ff6a..55d454f` 只改 run record）——皆 record-only（Bindings §7）。`git diff --name-only 4651d33 049ff6a` 全部在 `home_work_01/` 內（單元目錄外 0 檔）。 |
| Audit 種類 | **R1**（Formal 必做的 Ticket independent audit；治理 §4.1、§4.4），**cycle 1**。不是 Spec Integration Audit。 |
| 角色 | `primary_reviewer`（definition `gov-primary-reviewer`；Bindings §3.1 mapping `claude-opus-5-5`／`xhigh`） |
| Binding 證據 | 正式核對由派工者（Orchestrator）依 Bindings §3.4 記入 run record `home_work_01/doc/governance/run/run-20260925-hw01-v2-formal.md`（#39 Executor 列：`af8f083fccf7b5395` = `gov-executor`、`claude-opus-5-5`／`high`）。Reviewer 另以 Bindings §3.4 指令讀 harness 紀錄（session `05b8408b-260a-46d3-a4fe-ec07e3ec365a`）自行觀察：`agent-a2832f7b12b48dec1` `gov-primary-reviewer` `[('claude-opus-5-5', 'xhigh')]`（本 Reviewer；第一則訊息即本次 #39 R1 派工）；`agent-af8f083fccf7b5395` `gov-executor` `[('claude-opus-5-5', 'high')]`。兩者與 Bindings §3.1（b2 override）一致。此觀察只供對照，不取代派工者的核對。 |
| Independence（治理 §2.3、§4.6） | (1) **Fresh context**：未繼承 Executor 對話；worklog `issue-39.md`、commit message、已提交截圖與 `browser-check-results.json`／`network-log.json` 一律視為待驗證主張。(2) **Binding**：見上一列。(3) **Autonomous access**：自讀 Issue、OC-V2、SPEC-V2 v2.2、V1 SPEC、derivation record、decision A-1、#37／#38 audit records、run record、git 歷史與 diff、CI run；以 `git archive 4651d33` 匯出 BASE、以 `git archive ae0b9dc` 匯出 subject 到 Reviewer scratchpad；重跑 Executor 的 #39 檢查與 #36／#37／#38／V1 瀏覽器檢查（輸出導向 scratchpad，不覆寫已提交證據）；以 **BASE 版（未修改）** `check_county_browser.py` 對 subject 程式執行；另**自寫** probe（`probe.py`、`probe_drag.py`、`probe_sweep2.py`、`probe_reach.py`、`probe_tw.py`，皆在 scratchpad、未提交）：只沿用單元既有的 DevTools driver（`Browser`）與未修改 `server.create_app` 的測試台（`Rig`），**讀數與 oracle 全部自寫**——地圖視野以頁面腳本載入前安裝的 Leaflet 公開 API `L.Map.addInitHook` 取得地圖實例、直接讀 `getBounds()`／`getCenter()`／`getZoom()`（不經 Executor 的 `.leaflet-proxy` 解析）；圍欄判準依 R-V2-MAP-1 (i)(ii) 自寫（1 CSS px 容差）；可視比例以元素矩形與每個 overflow 祖先及視窗求交自算。(4) **Self-written record**：本紀錄由 Reviewer 以自己的 Write 工具寫入。**Model diversity：`diversity_lost`**——Executor 與 Primary Reviewer 同為 `claude-opus-5-5`（Bindings §5、b2 override；decision A-7）。合法狀態，不減損 §2.3 的 independence。 |
| 日期 | 2026-09-26 |

## 1. 審查方法與環境

- **環境**：Windows 11；`home_work_01/.venv` Python 3.12；Chrome headless（DevTools protocol，`websocket-client`）。
- **憑證**：Reviewer **沒有讀取** `home_work_01/.env`，沒有發出任何 CWA 請求。所有瀏覽器情境對 loopback 上未修改的 `server.create_app`（真的 `LatestObservationService`，上游為由已提交消毒樣本衍生的模擬，哨兵金鑰）。
- **不寫入**：沒有 git 寫入、沒有修改追蹤中的檔案（本紀錄除外）；結束時 `git status --short` 只有與本票無關、審查開始前即存在的 `grep.exe.stackdump`。
- **Commit 衛生**：`ae0b9dc`、`7ed633b`、`049ff6a` 的 message 皆為 `[Modify]／[Additions] – …` 格式、分類行正確；`grep -icE "claude|co-authored|generated with"` → 0。`git diff --check 4651d33 ae0b9dc`（排除 PNG）乾淨。

## 2. 分配 AC 的逐條結論

| AC／項目 | 判定 | 證據（Reviewer 自行取得） |
| --- | --- | --- |
| **AC-V2-13(a)** 初始視窗含本島全部＋澎湖本島（R-V2-MAP-4） | **PASS** | 1280：z7，W–E 116.44–124.05、S–N 21.14–26.76（本島 120.03–122.01E／21.90–25.30N、澎湖本島 119.52–119.70E／23.52–23.66N 皆在內）；375：z6，同樣涵蓋；`Back to Taiwan` 後兩視野同樣成立（Executor 檢查重跑）。自寫 sweep 在 7 個視窗尺寸的初始視野圍欄判準皆 PASS。 |
| **AC-V2-13(b)** zoom 8 與上限四向拖曳到底後：中心在 E、逐軸 ⊆／⊇ | **PASS**（另見 O-2） | Executor 檢查重跑 74/74（`fenceSweeps` 內每次讀數皆 PASS）。自寫 sweep：1280×900、1024×768、1920×1080、768×1024、375×812、375×667、414×896，zoom 6／7／8／10 各向 W／E／N／S／NW／SE 拖曳（真實 CDP 滑鼠事件）＋上限四邊（`setView` 越界後向外拖）＋方向鍵：**靜止後的視野全部 PASS**；上限四邊到邊距離 ≤ 0.0001°。zoom 7／8／10 另含拖曳中取樣 432 次，0 違反。唯一例外為 zoom 6（下限）在 ≥ 768 px 寬的**拖曳進行中**暫態（見 O-2）。 |
| **AC-V2-13(b)** 金門、連江可到達且測站可選取 | **PASS** | Executor 檢查重跑：兩視野 z8 與 z12 以拖曳到達（陸地框在視窗內）並點擊代表標記選取 `467110`／`467990`，圍欄成立。 |
| **AC-V2-13(c)** 下限：本島南北 ≥ 25%、再縮不動、圍欄仍成立；不以 E 全在視窗為條件 | **PASS** | z6：本島南北 168.9 px；1280 地圖 560 px → **30.2%**；375 地圖 360 px → **46.9%**；`−` 停用，`-` 鍵與滾輪不再縮小（Executor 檢查重跑）。自寫量測 Forecast mode 亦停在 6。下限時靜止視野的圍欄判準成立。 |
| **AC-V2-13(d)** 上限：1 km ≥ 20 px、375 px ≥ 5 km、再放不動、臺北市逐站可選 | **PASS** | z12：28.95 px/km（1280）／29.06（375）；375 px ≈ 12.9 km；`+` 停用。臺北市 19 個上圖測站：1280 以點擊選取 16、其餘自清單選取後在地圖上顯示並標示；375 為 11／10；0 問題（Executor 檢查重跑）。靜態守衛 `test_zoom_ceiling_*` 以 E 的南北緯度重算。 |
| **AC-V2-14** 375 資訊面（peek／展開／關閉） | **PASS** | 自寫 probe（375×812、375×667、768×1024）：選縣 → peek，地圖未遮蔽 **52.5%**（172／360 px；768：212／440，52.0%）；`Close`、`Expand`、兩個縮放鈕 `elementFromPoint` 命中；375×812 與 768 下模式切換、`Refresh`、`Back to Taiwan`、兩個時間不需捲動即在畫面內且未被遮蔽（375×667 時頁面為了露出資訊面自動捲動 280 px，模式切換在視窗上方之外、未被遮蔽，捲回即用）；`Expand`（Enter）→ 清單在資訊面內、縮放鈕仍命中；自清單項目按 Esc → 關閉、焦點到 `Details`、選取保留；`Details`（Space）→ 重開、焦點到 `Close`；開啟中點地圖上另一標記 → 標題更新為該站；自 `Close` 起 Tab 8 次皆落在清單項目、皆在畫面內且未被遮蔽。未實作滑動（MAY）；關閉不依賴滑動。 |
| **AC-V2-14** 44×44 | **PASS** | 375／768 的 peek、expanded、closed：`Now` 66.6×44、`Forecast` 93.7×44、`Refresh` 84.7×44、County 126.4×44、`Back to Taiwan` 118.3×44、`Expand` 72.2×44、`Close` 74.1×44、`Details` 69.1×44、縮放鈕 44×44、清單項目最小高 44。標記：Executor 檢查重跑（25 點 `elementFromPoint` 網格，顯示中的標記 44×44 全命中、兩兩不重疊）。 |
| **AC-V2-14** 375 各狀態無橫向捲動、768 無破版 | **PASS** | Executor 檢查重跑（11 個 375 狀態、768 四狀態）；自寫 probe 各狀態 `scrollWidth` ＝ `innerWidth`（375、768）。 |
| **AC-V2-14** 桌機面板不遮蔽選取項與**關鍵控制**；焦點走查 | **FAIL**（**F-1**） | 面板在地圖旁、不覆蓋地圖、選取標記與縮放鈕命中（PASS）；但選縣＋選測站後，面板自身捲動使 `Refresh`、Observation Time、Fetched Time **0% 在可視區**（1024／1100／1280 皆然；BASE 為 100%）。見 F-1。焦點走查：修改後 #38 Tab walk 72/72 通過；自寫 375 Tab walk 無被遮蔽的停駐點。 |
| **AC-V2-14** R-EN-1 六項（V2 介面）；loading／Stale／Unavailable 各一張 | **PASS** | Executor 檢查重跑（h1 逐字、Map 卡在預報區上方、Now 面板有標題、模式切換在首屏；Valid stations 與 Weekly summary；圖表 legend、軸、hover tooltip）；Reviewer 目視重跑產生的 `desktop-states-state-{loading,stale,unavailable}.png` 與 `375-state-*.png`。 |
| **AC-V2-15** 初始化守衛（資訊面開合＋resize；#36 模式切換守衛維持） | **PASS**（另見 F-2） | V1 `tests/test_map_frontend.py` 未修改（`git diff --stat` 空）且通過；新靜態守衛 `test_info_panel_changes_go_through_the_size_guard`、`test_resize_goes_through_the_size_guard`、`test_every_fit_settles_inside_the_fence_at_once` 通過；`fitBounds(` 全檔 1 處、`invalidateSize()` 在前。瀏覽器：Executor 的 15 步（開合、展開、選站、模式往返、五種 resize、容器隱藏時 resize＋開合）重跑無 NaN／0×0；#36 檢查（模式切換路徑）37/37。 |
| **§6.3 AC-19**（R-EN-1 六項、375 無橫向捲動、三種狀態截圖） | **PASS** | 同上三列。 |
| **AC-V2-20**（本票範圍：CI 全綠） | **PASS** | `pytest -q` → **513 passed**（Reviewer 本機）；BASE `4651d33` 的 **494** 個 test id 在 subject **全部存在**（`comm -23` 空），新增 19 個（`test_fence_frontend.py` 16、`test_secrets.py` 參數化 3）；`tests/` 只改 `check_county_browser.py`（見 §6）與 `test_secrets.py`（只加 3 行清單）。CI run `36216924939` headSha ＝ `ae0b9dc…`、success；其後 record-only commits 的 CI 亦 success。`app.py`、`weather_query.py`、`data.db`、`smoke.py` 的 blob 與 `main` 相同；`ingestion/` 與 `main` 無 diff。 |
| **R-V2-DOC-1(8)** README 圍欄與縮放範圍 | **PASS** | README「Now mode — map range, zoom range and layout (V2 Core)」：範圍數值＝E、逐軸行為、Forecast mode 同受限、zoom 6–12 與判準、初始視野、密度規則（22 縣順序）、版面與資訊面操作；數值與實測一致（28.95 px/km、≈ 13 km）。 |

## 3. Spec 條款對照（本票 Traceability）

| 條款 | 結論 | 說明 |
| --- | --- | --- |
| R-V2-MAP-1 | 成立（靜止視野）；O-2 | 見 AC-V2-13(b)。 |
| R-V2-MAP-2、MAP-3、MAP-4 | 成立 | 見 AC-V2-13(a)(c)(d)。 |
| R-V2-MAP-5 | 成立；F-2（Low） | 見 AC-V2-15。 |
| R-V2-RSP-1、RSP-2、RSP-3、RSP-5 | 成立 | 見 AC-V2-14 各列。 |
| R-V2-RSP-4 | 成立 | 標題逐字、地圖為主要內容區、模式切換首屏。 |
| R-V2-RSP-6 | **不成立（桌機關鍵控制）**：F-1 | 手機：選取標記在 peek 上方（Executor 重跑＋屏東縣最南測站情境）；expanded 時見 F-3。Tooltip：桌機四邊（Executor 重跑）與 375 z8 自寫 hover 3／3 皆在地圖內。 |
| R-V2-RSP-7 | 成立（依字面）；**R-1** 交 DA | 顯示中的標記可讀可選、不重疊；地圖可拖曳縮放選取；375 不要求 22 個。桌機全臺初始視野只顯示 9／22 個代表標記，見 R-1。 |
| R-V2-RSP-8 | 成立 | 見 §6.3 AC-19 列。 |
| R-V2-DD-9(e) | 成立 | 被資訊面或告示覆蓋的全臺標記 `tabindex=-1`；鍵盤焦點進入標記時 `reveal`；自寫與 Executor Tab walk 無完全遮蔽的焦點。 |
| R-V2-DOC-1(8) | 成立 | 見上表。 |

## 4. Invariants

| INV | 結論 | 證據 |
| --- | --- | --- |
| **INV-V2-8** V1 不變量與產物不變 | **HOLDS** | `git diff --stat 4651d33 ae0b9dc` 對 `app.py`、`weather_query.py`、`ingestion/`、`data.db`、`smoke.py`、`vercel.json`、`requirements.txt`、`server.py`、`api/`、`observation.py`、`representative.py`、`.github/`、`doc/requirement/`、`static/data/`、`static/vendor/`、`CONTEXT.md`、`tests/test_map_frontend.py` → 空；四個關鍵 blob 與 `main` 相同。`index.html` 的 diff 只在 Taiwan Map 卡內（Now 面板與新增 `.now-notes`），下方 Forecast section 未動；#36 檢查（下方 dashboard 兩模式相同、`Select Region` 六名、七列）37/37。 |
| **INV-V2-9** Scope class 分明 | **HOLDS** | README 新段落標示「(V2 Core)」；無任何文字把圍欄／資訊面呈現為老師要求；Part A 產物不變（上列）。 |
| **V1 INV-4** 老師指定名稱不變 | **HOLDS** | 見 §5 H-2。 |
| INV-V2-3（附帶） | HOLDS | Reviewer 重跑的 network log：224 個請求全部 loopback、外部 0；路徑只有 `/`、`/static/{app.js,styles.css,vendor/leaflet.{js,css},data/basemap.js,data/counties.js}`、`/api/{observations/latest,health,regions,regions/…/series,days,days/…}`、`/favicon.ico`。 |

## 5. High-risk 核對段（decision A-1）

- **觸及類別**：**H-2**（老師指定的介面／頁面文字／Grading App）。H-1、H-3 未實質觸及（附帶核對如下）。
- **H-2 核對了什麼**：(a) `app.py` blob `5693be8…`、`data.db` blob `6875869…`、`weather_query.py` blob `4d2e92f…` 與 `main` 相同；`requirements.txt`、`ingestion/` 無 diff；(b) `index.html` diff 三個 hunk 皆在 Taiwan Map 卡（`map-shell`、Now 面板、`.now-notes`），`<title>`、`<h1>Taiwan Weather Forecast</h1>`、masthead 導言文字、Forecast mode 面板（`Select Date`、`Date`、`Min`、`Max`）與下方 Forecast section（`Select Region`、`MinT`、`MaxT`、`Date`）**未改**；`styles.css` 對 masthead 只在 ≤ 640 px 改字級；(c) 全套 513 測試（含 V1 標籤逐字與 AppTest 類測試）通過；#36 瀏覽器檢查 37/37（下方 dashboard 與 `Select Region`）；Executor 檢查 R-EN-1(1) 讀 h1 逐字 PASS。
- **H-2 結果**：**PASS**——沒有任何老師指定的名稱、檔案、資料表或頁面文字被改動。
- **H-1（附帶）**：伺服器與金鑰路徑未改；`python -m tools.credential_scan` → passed（720 tracked files）；`git ls-files` 無 `.env`；已提交 evidence JSON 無 `opendata.cwa`／`Authorization=`／金鑰格式字串。
- **H-3（附帶）**：密度規則只切換標記可見性，不計算值；County 脈絡計算未改；狀態行加的原因是固定類別文字、`failureText(…, true)` 不附數字（DV-21 §4.2 維持）。

## 6. 變更風險（治理 §4.4）：#36／#37／#38 的回歸

- **重跑既有瀏覽器檢查（subject 工作樹，輸出到 scratchpad）**：#36 `check_modes_browser.py` 第一次 36/37（失敗項「B-desktop AC-V2-09(a) Refresh works while the forecast snapshot is unavailable」＝#38 R2 N-1 已知的同秒 Fetched Time 偽陽性），再跑兩次 **37/37**、**37/37**；#37 `check_refresh_browser.py` **97/97**；#38 `check_county_browser.py`（已修改版）**72/72**；V1 `check_series_error_visible.py` PASS。
- **以 BASE 版（未修改）`check_county_browser.py` 對 subject 程式執行**（scratch 匯出樹）：**67/72**。5 個失敗與 worklog Decisions 12 的四處修改一一對應：(a) 桌機「浮動面板下的標記取得焦點被帶出」——浮動 Now 面板已移除，無此情境；(b) 1280 與 375 Tab walk「22 個標記停駐點」——實得 9 與 5（密度規則），同一檢查的其他斷言全部成立（0 個縣 path 停駐點、只有標記＋縮放鈕、`hidden: []`）；(c)(d) 375 自 `Back to Taiwan` Tab 一次進清單——焦點先到資訊面的 `Expand`（可見）。修改後的檢查保留原性質（無 path 停駐點、焦點可見、清單可達）並多驗中間停駐點——**未弱化**。
- **未被任何檢查捕捉的回歸**：桌機面板內 Observation Time／Fetched Time／`Refresh` 在選縣＋選測站後離開可視區（#36／#37 已稽核行為的回歸）——見 **F-1**。

## 7. Executor 自述 concerns 的獨立判斷

1. **Leaflet 內部 API（`_limitCenter`、`L.Tooltip.prototype._setPosition`）** → **O-1**（robustness note，不是 finding）。Leaflet 為 vendored、pinned 1.9.4（`static/vendor/` 無 diff）；靜態守衛確認兩者被使用；tooltip 包裝在方法不存在時直接略過（`app.js:2121` 起），`reveal` 在 `_limitCenter` 不存在時才會丟例外——只在更換 Leaflet 版本時相關。
2. **圍欄與縮放範圍也作用於 Forecast mode** → **不是與 accepted 語義的衝突，不需 Design Authority。** 證據：(a) 自寫 probe 在 375、768、1180、1280、1440 進入 Forecast mode，六個 pill 全在地圖內且 `elementFromPoint` 命中（未被浮動面板或圖例蓋住）；下限／上限 6／12 時六個 pill 仍全數命中；BASE（V1 行為）為 0／無上限、無 `maxBounds`，同樣六個可見；(b) #36 檢查（含 AC-17／AC-18 逐字重驗：色帶＝endpoint、`Select Date` 七日、圖例四段＋導出說明）37/37；(c) V1 R-EN-4／AC-17／AC-18、DR-20／DR-21 核定的 HOW 沒有任何「可無限縮放或任意平移」的條款，「可縮放」在 6–12 下成立；(d) R-V2-MAP-1～3 的文字不以模式限定，而同節的 R-V2-MAP-4 明文限定「Now mode 初始」——起草者需要限定時有限定；OC §2.2(c)「地圖圍欄」是與 (a) Now mode、(b) Forecast mode 並列的 V2 Core 項目。Forecast 進入視野與 BASE 不同（≥ 1180 px：subject z7 以 E 置中，BASE z6 偏西），但 AC-17 不固定特定視野，進入規則（DV-8）屬 #36、其檢查通過。另：`.leaflet-control-zoom a` 44×44 也套用到 Forecast mode（外觀變化，無 V1 條款受影響）。
3. **桌機 Now 面板改到地圖旁** → 面板位置屬 HOW（R-V2-RSP-6「面板位置屬 HOW」；附錄 A 為 advisory，B-20、TB-V2-6），放在旁邊本身**不違反**任何有約束力的條款；但該欄位的面板內捲動造成 **F-1**。
4. **修改了 #38 已稽核的程式與檢查** → 見 §6：修改後檢查未弱化；#36／#37／#38 行為無其他回歸；F-1 是唯一實現的變更風險。
5. **#38 F-2（初始縮放的縣多邊形指標可達性）** → 依 #38 R1 disposition 屬 **Spec Integration Audit**。供 SIA 參考的 Reviewer 量測（3 px 網格、以地圖實例把 path 對到縣名）：初始視野 0 像素可指的縣——subject 1280 z7：嘉義市、臺北市；375 z6：新北市、臺北市、金門縣；BASE 1280：嘉義市、基隆市、新竹市、臺北市；BASE 375：18 縣。明顯改善；選單路徑（DD-9(a)）對 22 縣可用。
6. **375 大縣在 peek 下只顯示少數標記** → 屬密度管理 HOW（OC S-4「中間縮放層級的密度管理屬 HOW」；R-V2-RSP-7 只要求顯示者可讀可選、地圖不可用不得發生；R-V2-DD-5(d) 由清單滿足；DD-5(a) 上圖測站在視窗內成立）。**不是缺陷。**

## 8. Findings

### F-1 — 桌機（≥ 1024 px）選縣＋選測站後，Now 面板自身捲動使 Observation Time、Fetched Time 與 `Refresh` 完全離開可視區（Medium，**blocking**）

- **證據**：
  - 自寫量測（元素可視比例，計入 overflow 祖先與視窗）：1024×768、1100×900、1280×900，選 `臺中市` 後再選一站（清單點選，或在縣視野**點地圖標記**）→ `#obs-time`、`#obs-fetched`、`#refresh-button` **0%**；Stale 狀態下同一情境另 `#obs-state-chip`、`#obs-state-reason` 0%（County 狀態行 `#county-state` 100%）。只選縣：三者 100%；全臺選站：100%。**BASE `4651d33` 同樣三個寬度、同樣情境：三者 100%。**
  - Executor 自己提交的 `doc/acceptance/screenshots/v2/issue-39/desktop-desktop-panel-county-station.png` 與 `desktop-density-county.png`（1280）即呈現此狀態：面板頂端只露出 County 選單下半部，`Latest Observation` 標題、兩個時間、`Valid stations`、`Refresh` 皆不在畫面內。Reviewer 截圖 `panelvis-1280x900.png`、`panelvis-stale-1280x900.png`（subject）對照 BASE `panelvis-1280x900.png`。
  - 原因：`styles.css:1045-1055`（≥ 1024 px Now 面板 `max-height: 562px; overflow-y: auto`），加上選測站時 `app.js:1124-1131`（清單點選 `focused.scrollIntoView`、地圖點選 `els.obsSelected.scrollIntoView`）與選縣時 `app.js:1444-1445` 的程式捲動；面板高度容不下「狀態區＋County 脈絡＋詳情」，捲動把狀態區推出。
- **契約依據**：OC **S-1**「Observation Time 與 Fetched Time **永遠可見**」；SPEC-V2 **R-V2-OBS-4(c)**「Now mode 只要處於顯示資料的狀態（success 或 stale），dataset-level Observation Time 與 Fetched Time MUST 同時可見」；**R-V2-RSP-6**「面板與 overlay（桌機與手機）…目前選取項與**關鍵控制** MUST 可見可達」（`Refresh` 屬關鍵控制，R-V2-RSP-5(g) 列舉）；**AC-V2-14**「桌機面板不遮蔽選取項與關鍵控制」；並回歸 #36／#37 已稽核的 AC-V2-04 瀏覽器面（#37 R1 以「1280×900 選取測站＋Stale 時兩個時間、`Refresh` 無需捲動即可見」作為證據，並把 ≥ 1180 px 面板捲動交給 #39 的 RSP-6／AC-V2-14 判斷）。
- **為何 blocking**：由本票的版面變更引入；在主要驗證視野（1280）與全部桌機寬度的核心下鑽狀態（縣→站，正是 AC-V2-14 要求截圖的狀態），畫面上沒有任何 dataset-level 資料新鮮度（Fetched Time 完全不在視野；只剩該站自己的 Observation Time）與 `Refresh`，直接違反「永遠可見」的自然文義。這與 #38 F-3 不同：F-3 涉及的是原因文字，且 Stale **標示**仍在他處可見、該條款沒有「永遠」；此處受影響的正是 OC 以「永遠可見」保護的兩個時間，且畫面上沒有其他副本。修正在契約內（HOW 由 Executor 選擇，例如讓狀態區在面板內保持可見、或只捲動詳情區），同時須維持 R-V2-RSP-6「詳情不被裁切到不可讀」與 AC-V2-14 其餘項目。
- **修正後須提供的驗證**：桌機 1024／1280 在 success 與 Stale 下，選縣、選縣＋選測站（清單與地圖兩種路徑）時兩個時間與 `Refresh` 在可視區；詳情仍可讀；AC-V2-14 相關截圖更新；#36／#37／#38／#39 檢查無回歸。
- **爭議處理**：若 Executor 或 Orchestrator 對「可見」須為「在可視區」有異議，屬 blocking 爭議，依治理 §4.3 交 Final Adjudicator；爭議實質涉及設計語義時先交 Design Authority。

### F-2 — `ensureMapSized` 在地圖容器為 0 尺寸時丟棄第二個、不同的延後步驟，可使模式與地圖圖層不同步（Low，non-blocking）

- **證據**：`app.js:1944`「`if (mapInitScheduled) return; // already waiting; the pending step reads current state`」。BASE 的呼叫者只有 `bringUpMap`（讀取目前狀態的同一步驟），此註解成立；本票新增 `ensureMapSized(resizeMap)`（`app.js:410`）與 `afterSheetChange` 的閉包（`app.js:1334`），它們不執行 `syncMap`。Reviewer probe：375 選縣 → 把 `#map-frame` 設 `display:none` → 按 `Close`（排入 `afterSheetChange` 的步驟）→ 按 `Forecast`（`bringUpMap` 被丟棄）→ 恢復顯示：`#mode-forecast` `aria-pressed=true`、Forecast 面板顯示，但地圖上 **0 個** Forecast pill、仍有 60 個測站標記與 22 個縣 path（`dropped-step.png`）。
- **判定**：產品 UI 在初始化後不會使 `#map` 變成 0 尺寸（高度由 CSS 固定、寬度隨版面），所以在宣告的運作範圍內不可到達；R-V2-MAP-5 的 NaN／0×0 守衛本身成立（AC-V2-15 PASS）。屬 robustness，非契約違反。
- **Disposition**：不延長本 cycle。Owner：Executor 可在 F-1 的 targeted correction 中順修（本票新增的程式；例如排隊而非丟棄，或延後步驟一律走 `syncMap`）；否則交 Spec Integration Audit 記為已知 robustness 事項。

### F-3 — < 1024 px 的 **expanded** 資訊面中自清單選站後，選取的標記留在資訊面下、詳情在資訊面捲動區外（Low，non-blocking）

- **證據**：自寫 probe：expanded 狀態點清單第 5 項 → 選取標記底緣 571.4 px ＞ 資訊面頂緣 556 px、`elementFromPoint` 未命中（375×812；375×667：426.4 ＞ 411；768：718.4 ＞ 667.9）；資訊面保持焦點所在的清單項目在視野（`app.js:1124-1126`），詳情在其上方、需向上捲動。按 `Collapse` 後 `reveal` 把標記帶到 peek 上方（Executor 檢查重跑 PASS）。
- **判定**：R-V2-RSP-5(b) 的「地圖仍可見」只要求 normal／peek；RSP-5(f) 的「即更新內容」成立（資訊面標題可見地改為該站、詳情已更新）；expanded 是使用者為了看清單而選的狀態。可用性上的弱點，不是契約違反。
- **Disposition**：不延長本 cycle；Executor 可順修（例如 expanded 中選站後捲到詳情，同時維持焦點可見），否則交 SIA 觀察。

## 9. Routing signals（治理 §4.2；不是 blocking finding）

### R-1 — 桌機全臺初始視野可否由密度規則隱藏代表標記（required authority：**Design Authority**）

- **具體事實**：subject 在 1280×900 與 1920×1080 的全臺初始視野（z7）只顯示 **9／22** 個代表標記（臺北市、臺中市、嘉義縣、高雄市、花蓮縣、臺東縣、澎湖縣、金門縣、連江縣）；新北市、桃園市、新竹縣／市、苗栗縣、彰化縣、南投縣、雲林縣、嘉義市、臺南市、屏東縣、宜蘭縣、基隆市的代表標記須放大才出現（375 z6：5／22）。BASE（#38）三個尺寸皆 22／22。README 已揭露此行為。
- **Ambiguity**：OC S-4「Taiwan-wide 視野每縣至多一個代表性有效測站；…**中間縮放層級**的密度管理屬 HOW」與 S-10／R-V2-RSP-7「**不要求 375 px** 全臺視野同時顯示 22 個代表 pill」。讀法 A（Executor）：密度管理在任何縮放層級皆屬 HOW，375 一句只是舉例放寬；讀法 B：只對 375 明文放寬、且 HOW 限於「中間縮放層級」，因此桌機驗證視野的全臺初始視野應顯示每個有有效資料的縣之代表標記（與 SPEC-V2 User Story 1「打開頁面就看到全臺各縣的最新測站氣溫」一致）。兩種讀法都說得通，選擇會改變桌機訪客開頁看到的內容，屬契約語義，Reviewer 不自行補寫需求。
- **對本 audit 的影響**：依治理 §4.2 不作為 blocking。若 Design Authority 採讀法 B，R-V2-RSP-7／AC-V2-14 對本 subject 的結論須重做；建議 Orchestrator 在派 F-1 的 targeted correction 之前或同時 route R-1，使同一次修正可一併處理。

## 10. Observations（不是 findings）

- **O-1**：Leaflet 內部 API 依賴（見 §7-1）。更換 Leaflet 版本時須重驗 `reveal` 與 tooltip 夾限。
- **O-2**：zoom 6（下限）且地圖寬 ≥ 768 px 時，**按住滑鼠拖曳的過程中**視窗中心可離開 E（1280：拖曳中最遠至 115.29E／125.20E／26.82N／21.08N，按住 1 秒不回），但 E 在兩軸上始終整體位於視窗內（判準 (ii) 成立）；放開後 Leaflet 以 `panInsideBounds` 彈回 E 置中，靜止視野全部 PASS。375／414 與 zoom ≥ 7 皆無此現象（拖曳中取樣 0 違反）。成因是 Leaflet 1.9.4 拖曳中的 `_offsetLimit` 只保證「界不出視窗」、置中只在 `moveend` 時套用；SPEC-V2 §5.3 對 `maxBounds` 行為「即同時滿足 (i)(ii)」的描述只對靜止視野精確。R-V2-MAP-1 明列「彈性回彈、viscosity、margin 屬 HOW」，AC-V2-13 以「拖曳到底後」讀取，且暫態中有用範圍始終整體可見——在 HOW 內，不需處置；供 SIA 知悉。
- **O-3**：#36 N-1（同秒 Fetched Time 偽陽性）本輪再現一次，owner 依 #38 R2（#41 或下一位修改 `check_modes_browser.py` 者）。
- **O-4**：375 z8 地圖右上角的標記可能位於縮放控制之下而無法 hover（Leaflet 控制的一般性質）；平移即可操作，不影響 RSP-7。

## 11. Evidence（Reviewer scratchpad，未提交）

`C:\Users\yotsu\AppData\Local\Temp\claude\D--nchu-2026-AIoT-git-repository-aiot-classwork\05b8408b-260a-46d3-a4fe-ec07e3ec365a\scratchpad\`：
- `base/`（`git archive 4651d33`）、`subjtree/`（`git archive ae0b9dc`＋BASE 版 `check_county_browser.py`）；`base_ids.txt`／`subj_ids.txt`（494／513）。
- `fence/`＋`fence.log`（Executor #39 檢查重跑 74/74，含 `browser-check-results.json`、`network-log.json`、截圖）。
- `reg_modes*`、`reg_refresh`、`reg_county`、`reg_series`（#36、#37、#38、V1 重跑）；`oldcheck38.log`（BASE 版 #38 檢查對 subject：67/72）。
- `probe.py`、`probe_subj/`、`probe_subj2/`、`probe_base/`、`probe_base2/`（Forecast、往返、sweep、密度、資訊面、tooltip、延後步驟、面板可視比例；BASE 對照）；`probe_drag.py`＋`probe_drag_out/`（O-2）；`probe_sweep2.py`＋`probe_sweep2_out/`（zoom 7／8／10 拖曳中 0 違反）；`probe_reach.py`＋`reach_subj/`、`reach_base/`（§7-5）；`probe_tw.py`（F-1 其他路徑）。
- 指令：`pytest -q`（513 passed）；`pytest --collect-only` 差集；`gh run view 36216924939`；`python -m tools.credential_scan`；`git diff --stat／--check`、`git rev-parse main:<file>` 與 `ae0b9dc:<file>`。

VERDICT: BLOCKING (F-1)
