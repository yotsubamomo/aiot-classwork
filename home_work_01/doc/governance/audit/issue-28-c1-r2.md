# Audit record — Issue #28，cycle 1，R2（A-4 independent audit，scoped closure review）

| 欄位 | 內容 |
| --- | --- |
| Work Contract | GitHub Issue **#28**（Taiwan Map 視覺重做，post-baseline enhancement，Lightweight）。Outcome Contract＝acceptor 2026-09-24 直接指示（DR-20 §0）。Governing decisions：**DR-20** `decision-20260924-taiwan-map-rework.md`；**DR-21** `decision-20260924-map-rework-rs1-rs2.md`（DR-21.1 RS-1 → V-2 的操作規則 OR-V2；DR-21.2 RS-2 → masthead 導言一句在 boundary 內）。不變契約同 R1（Spec v1.1 R-EN-1..7、R-SHR-4、INV-1/2/5/6/7/9、AC-04(b)/14(6)/17/18/19/20/21/27/28；DR-19；H-2、H-3、A-1、A-4）。 |
| 受審 subject | branch `home_work_01-hw10-implementation`；correction subject **`ecdc793597f4f42251ca4ae0dc7c1c59ab580f2a`**；HEAD `e128ac9`（＝`git ls-remote origin`；`git diff --stat ecdc793..e128ac9` 只有 worklog，record-only）。R1 subject `b4549e5`。本次 delta：`git diff b4549e5..ecdc793`，排除 `doc/**` 後只有 `static/app.js`、`static/styles.css`、`tests/test_map_frontend.py`（M）；另有 `doc/acceptance/ACCEPTANCE.md`、`doc/ticket/tickets.md`、15 張 `doc/acceptance/screenshots/issue-28-*.png`（3 張新增）與 record-only 檔。 |
| Audit 種類 | **R2**（scoped closure review，治理 §4.4），**cycle 1**。延續本 Reviewer 的 R1 context；修正後的檔案、diff、測試與渲染結果全部從磁碟與本機重新取得。不是第二次全面審查；也不是 Spec Integration Audit。 |
| 角色 | `primary_reviewer`（`gov-primary-reviewer`；Bindings §3.1 `claude-opus-5-5`／`xhigh`） |
| Binding 證據 | 由派工者依 Bindings §3.4 核對，記入 run record `home_work_01/doc/governance/run/run-20260924-hw01-formal.md`（本次 #28 R2 dispatch）。 |
| Independence | (1) 延續 R1 Reviewer context（§2.3 允許），未繼承 Executor context；worklog「Targeted correction（cycle 1）」、ACCEPTANCE.md 與派工訊息的敘述都當作待驗證主張。派工訊息稱 R1 為「BLOCKING (F-1, F-2, F-3, F-4, F-5)」；R1 實際 verdict 是 **BLOCKING (F-1, F-2, F-4, F-5)**，F-3 為 Medium non-blocking，本 R2 照樣核對了 F-3。(2) Binding 見上一列。(3) 自主取得：`git archive ecdc793` 匯出後自行執行測試與 mutation；在本機啟動 server，用自寫的 Playwright-core 腳本驅動 Chrome 153 headless 量測；查詢 GitHub CI 與 deployment API；對 preview 執行 smoke。腳本放在 scratchpad `pw/`（`r2sweep.js`、`r2east.js`、`r2behave.js`、`r2resize.js`），輸出在 `pw/out-r2/`。(4) 本紀錄由 Reviewer 以自己的 Write 工具寫入。另核對：已 commit 的 `audit/issue-28-c1-r1.md` 與 Reviewer 寫入的原檔相同（工作樹 clean），沒有被改寫。 |
| 日期 | 2026-09-24 |

## 1. 方法與環境

- `git archive ecdc793 home_work_01` 匯出到 scratchpad，沒有 `.env`。執行時 unset `CWA_API_KEY`，並設 `HTTP(S)_PROXY=http://127.0.0.1:9`。使用 repo 的 Python 3.12.14 venv。
- 本機 server 為匯出 subject 的 `server.app`，在 `127.0.0.1:5077`。瀏覽器量測涵蓋 29 個寬度：360、375、390、414、480、600、640、641、700、768、800、820、834、880、900、960、1023、1024、1100、1179、1180、1181、1200、1280、1366、1440、1600、1920、2560，使用 dark scheme；H-3 另外加 light 375。
- 遮擋的判定方式：pill 與 tooltip 的 rect 是否和「浮動中的面板／圖例、zoom 控制、attribution control」相交；pill 中心用 `elementFromPoint` 確認是否命中自己；tooltip 另做逐字元（glyph）層級的遮擋檢查；DR-19 狀態訊息用文字 client rects 檢查。
- 結束時已停止 Reviewer 啟動的 server；`git status` 只有本紀錄檔（新增）。

## 2. R1 findings 逐項核對

### R1 F-1（High，blocking）— **RESOLVED**

- **修正內容**：非浮動（堆疊）版面的 breakpoint 由 `max-width:640px` 提高到 **`max-width:1179px`**（`styles.css:649-661`）。1179px 以下，資訊面板在地圖上方、圖例在地圖下方，都是 `position:static`。1180px 以上才浮動，並由 `fitToMarkers()` 依寬度預留面板與圖例的 padding（`app.js:658-673`：`[392,64]`／`[300,56]`）。
- **驗證**（`r2sweep.js`）：29 個寬度全部符合下列各點。
  - 六個 pill 都在 `#map-frame` 內，不與任何 overlay 相交，pill 中心 `elementFromPoint` 都命中自己。
  - 641–1179 皆為 `float=false`（堆疊），1180 起為 `float=true`；地圖高度 360（≤640）、440（641–1023）、560（≥1024）。
  - `scrollWidth` 等於視窗寬度。
  - 截圖 `out-r2/w1180.png`：1180px 浮動版面下，六個 pill 都在面板與圖例之外。
  - resize 跨越 1180 breakpoint（1100→1280→900→1440→1179→1180）後，每一步都沒有 pill 被遮或裁切（`r2behave.js` resize seq）。
- **R1 closure 條件**：641–1023（實測 641／700／768／800／820／834／880／900／960／1023）沒有 pill 被遮，且皆可點；tablet 寬度下的 DR-19 狀態訊息也沒有被遮。**全部達成。**

### R1 F-2（Medium，blocking）— **RESOLVED**

- **驗證**：29 個寬度下，六個 tooltip 的 box 都在 frame 內，也不與面板、圖例、attribution 相交。1024 與 1100 改為堆疊版面，面板不再蓋住 tooltip；1180 起的浮動版面有 padding 預留。
- 唯一重疊是 375／390／360 時，東部 tooltip 右上角 padding 與 zoom 控制重疊。逐字元檢查（`r2east.js`，DPR 3）壓在 zoom 控制下的字元為空字串，文字完整可見（截圖 `out-r2/east-375.png`）。
- Executor 提交的 `issue-28-desktop-1024-hover-south.png` 與本機渲染一致，可看到「南部地區」全名。
- **V-3 在 375 與桌機（≥1024）成立。** ACCEPTANCE §6 對 #24 F-5(a) 的敘述已更正。

### R1 F-3（Medium，non-blocking）— **RESOLVED**

- 以伺服器實際的長 error 訊息測 error，另測 empty 與 loading（延遲 6s），29 個寬度皆如下：
  - 狀態文字全部在 frame 內，與面板或圖例的交集為 0。
  - `Select Date` 可見，且中心 `elementFromPoint` 命中自己。
- 浮動寬度下，`.map-status` 的左右 padding（`styles.css:436-441`）讓訊息置中且避開面板（截圖 `out-r2/state-error-1180.png`）。

### R1 F-4（Medium，blocking）— **RESOLVED**

- **修正內容**：
  - `.pill-icon { pointer-events: none !important; }`（`styles.css:552-563`）。computed 值：icon 為 `none`、pill 為 `auto`，360 到 1280 皆同。
  - click listener 改掛在 `.pill`（`app.js:611`）。
  - attribution 縮短為 `Natural Earth · 內政部 open data`（`app.js:569-572`）。375 下它是右下角單行（`[152,613,342,630]`），不在任何 pill 的 44×44 區內。
- **真實點擊**（`r2behave.js`）：在 360、375、390、414、768、1024、1280 下，對每個 pill 點擊以下位置，選到的都是**自己的 Region**，錯選 0 次：
  - 垂直中線上的左緣 +2、中心、寬度 88% 處、右緣 −2；
  - 右緣 −3 那一欄的上緣 +2 與下緣 −2。
  - 以上涵蓋 R1 的失敗情境：375 下點南部 pill 右緣。
- **44×44 取樣**：7 個寬度 × 6 個 pill 全部 **225／225** 命中自己，沒有命中鄰近 icon box 或 attribution。`::before` hit area 為 54.3×44 px，連同 pill 本體的可點區 ≥ 44×44。
- **V-4 成立。**

### R1 F-5（Medium，blocking）— **RESOLVED**

- 兩個重寫的測試都限定在函式本體內（`_function_body()` 做括號配對並略過字串與註解，`_strip_comments()` 移除註解；`test_map_frontend.py:40-117, 121-165`）。`test_ensuremapsized_guards_on_nonzero_container_size` 讀 `ensureMapSized` 的本體，`test_fittomarkers_invalidatesize_precedes_fitbounds` 讀 `fitToMarkers` 的本體。
- **Mutation**（Reviewer 在 ecdc793 匯出副本上自行執行）：

| 突變 | 結果 |
| --- | --- |
| (a) `fitToMarkers` 內把 `invalidateSize()` 移到 `fitBounds()` 之後 | `test_fittomarkers_invalidatesize_precedes_fitbounds` **FAILED**，1 failed、10 passed |
| (b) `if (sized()) { cb(); return; }` 改為 `cb(); return;` | `test_ensuremapsized_guards_on_nonzero_container_size` **FAILED** |
| (a)+(b) | 2 failed |
| (c) 保留 guard 字面，但讓 `sized()` 恆回傳 `true` | 仍 **FAILED**（非零尺寸判斷式只留在註解內，被移除註解後找不到） |
| 未突變 | 全數 PASS |

- 行為面也再驗證一次：`#map-frame` `display:none` 2s，以及 `.map` 高度 0 持續 1.5s。兩種情況下，容器為 0 尺寸時 pill 數為 0；顯示後六個 pill 都在 frame 內，沒有 console error 或 pageerror。

### R1 Low findings 與殘留項

- **F-6 — RESOLVED**：`colourLegend()` 在 DOMContentLoaded 就呼叫（`app.js:157-159`）。29 個寬度的 error、empty、loading 狀態下，四個 swatch 都是不同顏色。
- **F-8 — RESOLVED**：`keyboard:false`（`app.js:600-603`）。地圖內的 tab stop 只剩 6 個 `.pill`，外層 icon 沒有 `role`。Tab 到 pill 後按 Enter 可正常選取（中部地區）。
- **F-9 — RESOLVED**：新增 `issue-28-desktop-light-hover-tooltip.png`，頁面背景為淺色（取樣 `(237,240,245)`）。
- **F-7／F-10／F-11 — 仍存在，依 R1 disposition 不處理**：
  - F-7：切到失敗日期時，面板仍保留前一天的值。
  - F-10：面板與表格用兩種數字格式，屬 SHOULD。
  - F-11：360px 下南部與東北部 tooltip 被容器裁切，在 V-3 的 375 判準之外。

## 3. DR-21 條件核對

- **DR-21.1／OR-V2（V-2）— PASS（DR-21.1）**。Reviewer 用 WCAG 2.x 公式自算：

  | 項目 | 海 `#0f1927` | 台灣陸 `#25324a` | 周邊陸 `#1a2331` |
  | --- | --- | --- | --- |
  | 預設白描邊 `#fff` | 17.67 | 12.85 | 15.81 |
  | 作用態描邊 `#9ed0ff` | 10.87 | 7.91 | 9.72 |
  | 填色（藍／綠／黃／紅） | 3.26／3.89／7.39／3.23 | 2.37／2.83／5.38／2.35 | 2.92／3.48／6.62／2.89 |

  - 內文對填色為 5.42、4.54、6.68、5.47，全部 ≥ 4.5。
  - 每一色帶對每一底圖色，「填色或描邊」至少一項 ≥ 3；描邊在四種狀態皆 ≥ 3。
  - computed style 確認四種狀態的四邊描邊都是 `2px solid`：預設 `rgb(255,255,255)`；hover、focus、選取（含預設被選的北部）為 `rgb(158,208,255)`。
  - token 未改：`--band-blue #2b6cb0`、`--band-green #2f855a`、`--band-yellow #d69e2e`、`--band-red #c53030`、`--map-sea #0f1927`。diff 沒有觸及 `BAND_COLOURS`、`BAND_TEXT`、底圖 fill 或 border。
  - worklog 的 V-2 段已依 OR-V2 重寫（三種底圖色 × 填色與描邊、判定寫「PASS（DR-21.1）」、明示只列對海的數字不足以證明）。ACCEPTANCE.md 的 AC-19 列寫明「V-2 = PASS per DR-21.1 / OR-V2」。
  - 小瑕疵見 N-3。
- **DR-21.2（masthead 導言）— 條件成立**：
  - `index.html` 在 `b4549e5..ecdc793` 沒有任何變更，masthead 沒有再被改動（DR-21.2(a)）。
  - worklog「附帶改動（地圖卡以外）」段補記該句，並引用 DR-21.2，標明是唯一附帶改動（DR-21.2(b)）。
  - Reviewer 對此 boundary 沒有異議，**RS-2 關閉**；RS-1 依 DR-21.1 關閉。依 DR-20 §3.5 fail-safe，不觸發補充 Spec Integration Audit。

## 4. 不回歸核對與 H-2／H-3（A-1）

- **Diff-scope**：`git diff --name-only b4549e5..ecdc793`，排除 `doc/**` 後只有 `static/app.js`、`static/styles.css`、`tests/test_map_frontend.py`。`index.html`、`static/data/**`、`README.md`、`test_static_checks.py`、`test_dashboard.py`、`app.py`、`server.py`、`weather_query.py`、`api/`、`vercel.json`、`data.db` 都沒有變更（檢查結果 0 行）。INV-2、INV-9 維持，`/api/` 形狀沒有變。
- **H-2 — HOLDS**：`index.html` 未變，所以 `Taiwan Weather Forecast`、`Select Region`、`Select Date`、`Date`、`MinT`、`MaxT`、`Min`、`Max` 與六個 Region 中文名，都與 R1 §2.5 逐字核對的結果相同。`test_dashboard.py::test_index_page_has_visible_teacher_text` 與 `test_index_has_map_panel_select_date_and_legend` PASS。pill 標籤、tooltip、`aria-label` 的 Region 名仍取自 `REGION_ORDER`。
- **H-3 — HOLDS**：
  - 在 1280 dark、375 light、768 dark 三個 context，對七個 Forecast Day 各取 `/api/days/<date>`，與 DOM 逐一比對六個 pill 的文字（`derivedMapTemperature.toFixed(1)+"°"`）、class（`pill pill--<colourBand>`）、`aria-label`、tile max／min 與所選 Region 區塊。共 126 個 pill 比對，**0 筆不符**。
  - `git grep` 在 `static/app.js` 找不到 `mint + maxt` 或 20／25／30 門檻，前端沒有重算。`test_frontend_does_not_re_derive_or_re_band` PASS。
  - 標示文字沒有變動：chip、來源句、圖例註記與「(derived …)」都未改。
- **H-1 — HOLDS**：CI credential scan 綠（見下）。
- **R-SEC-1／INV-6（零外部請求）— HOLDS**：
  - 每個 context 載入加 7 次切日共 18 個請求，全部是同源 `http://127.0.0.1:5077`，外部 0。
  - 29 個寬度的 sweep 外部請求皆為 0。
  - preview 部署提供的就是 correction 版本：`/static/app.js` 含 `fitToMarkers`，`/static/styles.css` 含 `pointer-events: none !important`。
- **P-12 — HOLDS**：使用者先放大地圖，再切換 7 天日期，map pane 與六個 marker 的 transform 完全不變，視野沒有重設；`fitBounds(` 全檔只有一處。這項檢查在三個 context 都做過。
- **DR-19 與 P-7(b) — HOLDS**：對 2026-09-26 模擬 503、network abort、2xx 空值、2xx 非 JSON，都顯示對應的 inline 狀態，`Select Date` 可見且未停用；改選 2026-09-27 後恢復正常。
- **#24 F-3（亂序回應）— HOLDS**：2026-09-25 延遲 2.5s 後改選 2026-09-28，最後畫面仍是 2026-09-28，北部為 28.4°，等於 endpoint 值。
- **#24 F-1**：tooltip 與所選區塊在切換日期時更新的相關程式碼（`bindOrUpdateTip`、`renderDay`、`updateSelectedBlock`）在本次 diff 中未改動；它們只改由 `refreshMapChrome` 在 `moveend` 呼叫。
- **測試與 CI**：
  - 乾淨匯出版本、無網路：**164 passed in 4.29s**。與 `b4549e5` 的 163 個測試相比，少了兩個舊測試名，多了三個新測試（兩個是重寫），沒有刪除其他測試。
  - CI：`ecdc793` 的 push `35965840014` 與 pull_request `35965842100` 皆 success。log 顯示 checkout `ecdc7935…`、`164 passed in 4.22s`、`credential scan passed: 535 tracked files; no .env tracked …; no CWA-key-format string …`。`e128ac9` 的兩個 run 亦 success。
- **AC-15（preview）**：deployment `6631867697`（sha `ecdc793`，success）→ `https://aiot-hw01-weather-oqntcs471-nchu-aiot-class.vercel.app`。subject 的 `smoke.py` 結果為 `[2026-09-24T06:58:43Z] SMOKE PASS … (1.1s)`，`GET /` 與 `/api/health` 皆 200。

## 5. 本次修正直接產生或暴露的新 findings

### N-1 — Medium — **blocking**：AC-19 的 loading 狀態截圖在修正後被換成已載入完成的地圖

- **證據**：
  - `md5sum doc/acceptance/screenshots/issue-28-*.png` 顯示 `issue-28-state-loading.png` 與 `issue-28-desktop-dark-ac17.png` 的 md5 都是 **`45ceda3aa14644c002027c3379d669ad`**，兩者 byte 完全相同。
  - 打開該檔可見完整渲染的地圖：六個 pill、面板有值、Forecast Day 為 2026-09-24，沒有任何 loading 狀態。
  - `b4549e5` 版的同名檔 md5 為 `a7544ad0…`，是真正的 loading 截圖。所以這是本次 correction 重拍時造成的回歸。
  - `ACCEPTANCE.md` 的 AC-19 列把 `issue-28-state-loading.png` 列為 loading 狀態的截圖；worklog「重拍的截圖」也列出 `issue-28-state-error/empty/loading`。
  - 產品行為本身沒有問題：Reviewer 自己在 29 個寬度量測 loading 狀態，都能正常呈現。
- **契約**：
  - Spec **AC-19** 的證據要求「loading／empty／error 三種狀態各一張截圖」；DR-20 §3.5(A)-3 與 DR-20.6(4) 都要求 AC-19 重驗。
  - `ACCEPTANCE.md` 是交付物（R-DOC-4），不是 record-only 路徑。
  - 在交付的驗收文件中引用不是 loading 狀態的截圖作為 loading 證據，等於 AC-19 的證據不成立；治理 §4.5 也禁止虛報 verification。
- **Closure 條件**：
  - 以 `ecdc793` 或其後的 subject 重拍一張真正的 loading 狀態截圖，畫面要看得到地圖卡的 inline loading 訊息，且 `Select Date` 可見。
  - 重拍後的檔案 md5 不得與其他截圖相同。
  - ACCEPTANCE.md 與 worklog 的引用要和實際檔案一致。
  - 不需要修改任何實作。

### N-2 — Medium — non-blocking：只改變視窗高度也會重新 fit，使用者的縮放被重設

- **證據**（`r2resize.js`）：
  - 375×812：放大後北部與南部 pill 的距離由 245px 變為 490px；只把視窗高度改為 740，距離回到 **245**，縮放被重設。
  - 1280×900 改為 1280×820：結果相同。
  - 切換 `Select Date` 則**不會**重設（490 維持 490）。
  - 原因：resize handler 由 `map.invalidateSize()` 改為 `fitToMarkers()`（`app.js:146-154`），任何 `resize` 事件都會重新 fit，包括只有高度改變的情況。
  - 行動瀏覽器在捲動時工具列收合或展開，常會觸發只改變高度的 `resize`。結果是：在 375px 放大地圖後，往上捲去看面板，縮放就會被還原。
- **契約影響**：R-EN-4／AC-17「可縮放」仍成立；P-12 只規定切換 Select Date 不得重設視野，這點成立。沒有契約條款被違反，但這是修正本身引入的行動裝置可用性退步。
- **Disposition**：owner＝Executor。建議只在寬度改變或堆疊／浮動版面切換時才重新 fit。可在處理 N-1 時一併修，不延長 cycle。
- **附記（未驗證，不列為 finding）**：JS 用 `window.innerWidth >= 1180` 判斷，CSS 用 `max-width:1179px`，兩者在整數寬度下一致；若瀏覽器縮放產生 1179 到 1180 之間的小數寬度，兩者可能不一致。可考慮改用 `matchMedia('(min-width:1180px)')`。

### N-3 — Low — non-blocking：worklog V-2 表格把 hover 狀態放在錯誤的描邊欄

- **證據**：worklog 的 OR-V2 表把 hover 歸在「描邊 #fff（預設/hover）」欄。實際 hover 的 computed 描邊是 `rgb(158,208,255)`（`#9ed0ff`，`styles.css` 的 `.pill-icon:hover .pill`）；同一份 worklog 的「DR-21 記錄修正」段也寫 hover 為 `#9ed0ff`。
- 兩種描邊對三個底圖色都 ≥ 3，V-2 結論不受影響。
- **Disposition**：owner＝Executor，修 N-1 時順手更正措辭。

## 6. 結論

- R1 的 blocking findings **F-1、F-2、F-4、F-5 全部已解決**；F-3、F-6、F-8、F-9 已解決；RS-1、RS-2 已依 DR-21 關閉，V-2 依 OR-V2 為 PASS。
- 契約不回歸：H-2、H-3（七日 parity、前端不重算）、INV-2／INV-9、零外部請求、P-12、DR-19、#24 F-3、測試 164 passed 與 CI 皆成立。
- 本次修正直接產生一個 blocking 的證據缺陷 **N-1**：AC-19 的 loading 截圖不是 loading 狀態，與 AC-17 截圖 byte 相同。依治理 §4.4，R2 仍有 blocking，下一步是 exactly one Alternate Review，不是 R3。N-1 的修正只需重拍截圖並更新引用，不需改實作。
- N-2、N-3 為 non-blocking，已記錄 owner。

VERDICT: BLOCKING (N-1)
