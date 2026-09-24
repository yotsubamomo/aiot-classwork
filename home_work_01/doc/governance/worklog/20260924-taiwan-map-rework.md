# Worklog — Taiwan Map 視覺重做（GitHub Issue #28，Lightweight post-baseline work item）

> Governance §3.7 durable worklog。續接 session 更新同一份。本 work item 的契約＝
> acceptor 2026-09-24「Taiwan Map 視覺重做」指示（DR-20 核定文）＋其核定的 Issue #28 §1–§4。
> Lane / boundary / HOW 採納見 `doc/governance/decisions/decision-20260924-taiwan-map-rework.md`（DR-20）。

## Contract reference

- **Outcome Contract（本 work item）**：acceptor 2026-09-24 直接指示（Bindings §2.3 末項、§4 第 3 列）；逐字核定文在 DR-20 §0。**不取代、不修改**既有 Outcome Contract（ACCEPTED 2026-09-23）與 Spec v1.1。
- **Derived governing record**：DR-20（DR-20.1 lane=Lightweight；DR-20.2 boundary B-1..B-16 / X-1..X-8；DR-20.3 提案 HOW P-1..P-13；DR-20.4 底圖不需白名單變更；DR-20.5 A-4 audit 涵蓋整合重驗、不另開 Spec Integration Audit instance；DR-20.6 驗收語義）。
- **不變契約**：Spec v1.1 R-EN-1..R-EN-7、R-SHR-4、R-SEC-1..3、INV-2/5/6/7/9、AC-04(b)、AC-17/18/19、AC-28；DR-1、DR-4、DR-19；high-risk H-2/H-3、A-1、A-4。
- **GitHub Issue #28**（label `ready-for-agent`；Blocked by #24、#25）。

## Executing role and binding reference

- 角色：`gov-executor`（Bindings §3.1：`executor` → `claude-opus-4-8` / `high`）。
- Binding 證據：本 session 的 subagent/transcript meta（派工者依 Bindings §3.4 核對 agentType/model/effort 並記入 run record）。

## Subject identity

- Branch：`home_work_01-hw10-implementation`。
- BASE = HEAD `d23de58d7ef152a0368e1f8ee1d14cc94eefc138`（＝ `origin/home_work_01-hw10-implementation`；#18–#25 CLOSED；phase-accepted subject 仍為 `720c0a0`）。
- 允許的 diff-scope（DR-20 §3.5(A)-1）：`home_work_01/static/**`（含新增 `static/data/`）、`home_work_01/tests/**`（只加強/新增）、`home_work_01/README.md`、`home_work_01/doc/acceptance/**`、`home_work_01/doc/ticket/tickets.md`、`home_work_01/doc/governance/**`（record-only）。任何其他路徑出現即 boundary finding。

## Audit status

- **required（A-4）**：觸及 H-2（頁面概念詞逐字）與 H-3（藥丸值/色直接取 endpoint、導出/相容性標示）。fresh `gov-primary-reviewer` R1；R1 record 依 A-1 明記 H-2/H-3；range 依 DR-20 §3.5(A)。由 Orchestrator/主 session 依 Bindings §3.5 派工。**不得**記為「依 policy 未要求」。
- **cycle 1 R1 結果：BLOCKING**（`doc/governance/audit/issue-28-c1-r1.md`，VERDICT: BLOCKING F-1、F-2、F-4、F-5）＋兩個 routing signals 由 DA 裁決（`decision-20260924-map-rework-rs1-rs2.md`，DR-21.1 RS-1／DR-21.2 RS-2）。已做 **targeted correction**（治理 §4.4）——見下方「## Targeted correction（cycle 1）」。等待 **R2**（同一 Primary Reviewer 續派）。

## Decisions and assumptions（HOW，DR-20 邊界內）

- 底圖採 DR-20 §2.2 vendored 向量方案，執行期零外部請求；不採 OSM/CARTO（X-1）。
- 底圖資料以 `static/data/basemap.js` 同源 `<script>` 設 `window.TAIWAN_BASEMAP = { context, taiwan }` 全域；不用 `fetch`、無絕對 URL、無金鑰。
- 靜態檢查改為遞迴掃描 `static/**`（順修 #24 F-4）；只加強。vendored Leaflet 內既有的非請求常數（`https://leafletjs.com`、`https://bugs.chromium.org/...`、`https://bugzilla.mozilla.org/...`）加入 `_ALLOWED_FRONTEND_URLS`（與既有 `http://www.w3.org/2000/svg` 同類，非請求目標；不放行任何 tile/CDN 請求目標）。

## Work performed

只動 Taiwan Map 卡（DR-20 §3.5(A) diff-scope 內）。

1. **Vendored 向量底圖**（`static/data/basemap.js`，新增，~196 KB ≤ 300 KB）：`window.TAIWAN_BASEMAP = Object.freeze({context, taiwan})`，同源 `<script>` 全域，**不用 fetch、無絕對 URL、無金鑰**。
   - `context`：Natural Earth `ne_50m_admin_0_countries`（public domain），filter CHN/TWN/PHL/JPN/VNM/HKG/MAC，bbox-clip lng 114..127 / lat 17.5..28，Visvalingam 簡化。
   - `taiwan`：內政部「直轄市、縣市界線(TWD97經緯度)」開放資料 v1140318（政府資料開放授權條款；data.gov.tw dataset 7442 → tgos.tw SHP），bbox-clip lng 118..122.5 / lat 21.5..26.5，Visvalingam 簡化。build tool＝`mapshaper`（scratchpad，未進 repo）。取得過程免帳號、免付費。幾何 only（無屬性），`interactive:false` backdrop，不承載縣市層級資料語義（P-2c）。**未帶入樣稿 9.3 MB counties／3.0 MB ne50／`?base=osm|carto`／tile 程式路徑**（P-2d）。
2. **`static/index.html`**：map-first——Taiwan Map 卡移到 `#dashboard` 首位、整寬。浮動資訊面板（`.map-panel--info`，含 `Select Date`＋`DERIVED` chip＋`Forecast Day`＋來源句＋當日兩張 tile＋所選 Region 區塊）；浮動四段圖例（`.map-panel--legend`）＋ R-EN-5 原句；狀態 overlay 只蓋地圖框。controls card 保留 `Select Region`＋ingestion time。載入 `/static/data/basemap.js`。概念詞逐字保留（H-2）。
3. **`static/styles.css`**：always-dark map tokens 移到 `:root`（不被 dark block 覆寫，兩色系皆深色，P-1）；四段 band token `--band-*`；高度 560/440/360（desktop/tablet/375）；藥丸（`L.divIcon`）樣式、hit area ≥44×44（`.pill::before`）、pointer-events 只在藥丸（避免相鄰 icon box 互擋）；tooltip、圖例、面板；375 面板改為地圖上下列。移除舊 `.map-layout/.map-side/.infocard*/.legend-bands*/.mapinfo*` 死 CSS（#24 F-2 先例）。
4. **`static/app.js`**：藥丸＝`L.marker`＋`L.divIcon`，內文 `oneDp(v.derivedMapTemperature)+"°"`、class/底色 `v.colourBand`（前端不重算、不重分帶，H-3）；`aria-label` 含 Region/Date/Min/Max/derived；hover tooltip（`bindOrUpdateTip`，per-marker `tipDir()`——上緣標記向下開，避免裁切，V-3/#24 N-1）；面板 tile 前端對六筆 endpoint 取 max/min（同 #23 先例，無新邏輯）；點藥鈕更新所選 Region 區塊（預設北部地區）；`Select Date` 改動只更新藥丸/tooltip/面板、**不重設視野**（`fitBounds` 只在 init 呼叫一次）。**Init 強化**：`ensureMapSized()`（`ResizeObserver`＋`visibilitychange`，容器非 0 尺寸才初始化）；`invalidateSize()` 後 `fitBounds`。保留 `mapReqSeq` 亂序守衛（#24 F-3）。DR-19：狀態只蓋地圖、`Select Date` 保持可見可操作（P-7b）。移除 inline `TAIWAN_OUTLINE`、circleMarker。
5. **`tests/test_static_checks.py`**：`_static_files()` 改遞迴（順修 #24 F-4，涵蓋 `static/data/`＋`static/vendor/`）；`_ALLOWED_FRONTEND_URLS` 加入 vendored Leaflet 內既有的**非請求**常數（`https://leafletjs.com`、`bugs.chromium.org/...`、`bugzilla.mozilla.org/...`，與 `w3.org/2000/svg` 同類，不放行任何請求目標，AC-04(b) 語義不變）；新增遞迴保護測試。
6. **`tests/test_map_frontend.py`**（新增）：init 強化回歸（ResizeObserver/visibilitychange、`invalidateSize` 先於 `fitBounds`、`fitBounds` 恰一次、代表點有限且在台灣 bbox）＝ NaN/0×0 hazard 的 pytest 驅動回歸測試；H-3/AC-28 前端無重算/重分帶；藥丸 band token == 圖例 `--band-*` token；basemap 全域/無 URL/幾何有限/≤300 KB；面板含 Select Date＋四段圖例。
7. **README**、**ACCEPTANCE.md**（AC-04/17/18/19＋§6 residual F-4/F-5(a)/F-6）、**tickets.md** 更新。

**已在樹上（中斷前）**：static 三檔＋basemap.js＋兩測試檔的實作、README/ACCEPTANCE/tickets/decision-record/worklog（本次補完 worklog 四節、重驗、重截圖）。**本次補完**：V-1..V-5 量測、七日 parity、零外部請求 log、最終截圖（依最終程式重截）、commit/push/CI。

## Verification

環境：本機 `.venv` Python 3.12.14（AC-23）；headless Chromium（Playwright，scratchpad build tool）；Flask `server.py` @127.0.0.1:5000。全程無網路資料相依、無 `.env`。

- **完整 offline pytest**：`163 passed`（baseline 152 ＋ 新增 11：`test_map_frontend.py` 9、`test_static_checks.py` 遞迴保護 1、其餘既有）。無網路、無 `.env`。
- **零外部請求（INV-6）**：Playwright 攔截全部 request＝13 筆，external＝0，origin 只有 `http://127.0.0.1:5000`（含兩次 `Select Date` 切換）。前端無絕對 URL（`test_frontend_makes_no_external_absolute_url_requests` 遞迴後仍綠）、資料請求只到 `/api/`（AC-04b）。
- **七日 endpoint parity（H-3）**：對 `/api/days` 七天各取 `/api/days/<date>`，六藥丸 DOM 內文＝`oneDp(derivedMapTemperature)`、class/底色＝`colourBand`，與 endpoint 逐筆一致。本快照七天六區皆 yellow band；值（2026-09-24 例）北27.2/中28.8/南29.2/東北26.5/東27.0/東南27.5，與 endpoint 相同。完整七日列於本 session 的 `/api/days/*` 擷取（DOM 藥丸 aria-label 亦含同值）。
- **V-1（字級 ≥12 px 固定 px，地圖卡）**：藥丸 14、Region 標籤 12、圖例 list 12/title 13/note 12、面板 title 15/chip 12/control label 12/select 14/meta 12/source 12、tile label 12/value 22/unit 12/region 12、sel name 15/row 13/derived 13–16/note 12、tooltip 13、Leaflet attribution 12。全部 ≥12 px。（頁面其餘段落 ≥16 px 由 #23/#25 既驗，本卡不適用該規則，P-13。）
- **V-2（對比）→ 見「## Targeted correction（cycle 1）」的「### V-2（依 DR-21.1 / OR-V2 重寫）」。** 本行 R1 前的「PASS with border rationale」措辭**作廢**：DR-21.1 裁定 V-2 採「標記整體對底圖」讀法，判定為 **PASS（DR-21.1）**，並在該節列出填色與 2 px 描邊對海/台灣陸/周邊陸（含作用態）的完整數值。
- **V-3（tooltip 不裁切）→ 以 correction 節為準。** 本行 R1 前只在 1280／375 量、未計浮動面板（R1 F-2 指出 1024–1150 南部 tooltip 被面板遮）。correction 後於 641→1920 各寬度六 tooltip 皆不裁切、不被面板/圖例遮（見 correction 節）。
- **V-4（可點區 ≥44×44）→ 以 correction 節為準。** 本行 R1 前的「pointer-events:none，相鄰標記不互擋」敘述被 R1 F-4 推翻（Leaflet `.leaflet-interactive` 蓋過，未加 !important）。correction 後改 `!important` 並縮短 attribution，375/360 右緣點擊皆選到正確 Region（見 correction 節）。
- **V-5（截圖）**：light＋dark × desktop(≥1024)＋375，含 hover；`issue-28-*`（見 Artifacts）。375 `document.documentElement.scrollWidth == innerWidth == 375`（無橫向捲動）；desktop 1280==1280。map 高度量測 desktop 560 / 375 360。
- **DR-19 三狀態**：以 Playwright route 攔截 `/api/days/<date>` 造 503（error）、200 空 values（empty）、4s 延遲（loading）；三狀態下 `#date-select` 皆 `dateVisible=true`（可見可操作，P-7b），地圖卡不空白（狀態訊息覆蓋地圖框、面板/圖例仍在）。截圖 `issue-28-state-{error,empty,loading}.png`。
- **AC-17/18/19 重驗**：見 ACCEPTANCE.md 對應列（PASS，附 #28 證據）。
- **不回歸**：`fitBounds` 恰一次（切日不重設視野，AC-18/P-12）；`mapReqSeq` 亂序守衛保留（#24 F-3）；`>Select Date</label>`／`>Select Region</label>`／表頭字串保留（`test_dashboard.py` 綠，H-2）；`app.py`/`server.py`/`weather_query.py`/`api/`/`vercel.json`/`data.db`/`requirements.txt`/`.github` 未觸及（INV-2/INV-9）。
- **CI**：push 後 `gh run watch`（見末尾 commit/CI 段補記）。

## Artifacts

- 新增：`static/data/basemap.js`（vendored 向量底圖，~196 KB）；`tests/test_map_frontend.py`。
- 修改：`static/index.html`、`static/app.js`、`static/styles.css`、`tests/test_static_checks.py`、`README.md`、`doc/acceptance/ACCEPTANCE.md`、`doc/ticket/tickets.md`。
- 截圖 `doc/acceptance/screenshots/`（依最終程式重截）：`issue-28-desktop-dark-ac17.png`、`issue-28-desktop-light-ac17.png`、`issue-28-desktop-dark-fullpage-ac19.png`、`issue-28-375-dark-ac19.png`、`issue-28-375-light-ac19.png`、`issue-28-desktop-hover-tooltip.png`、`issue-28-375-hover-tooltip.png`、`issue-28-desktop-date1-ac18.png`、`issue-28-desktop-date2-ac18.png`、`issue-28-state-error.png`、`issue-28-state-empty.png`、`issue-28-state-loading.png`。
- 記錄（record-only）：本 worklog；`decision-20260924-taiwan-map-rework.md`（DR-20，DA 產出，Executor 未改）。
- **Subject（A-4 audit 對象）**：commit `b4549e5`（branch `home_work_01-hw10-implementation`，pushed to `origin`；SA-1）。`git diff --name-only 720c0a0..b4549e5`（排除 `doc/governance/**`）僅落在 `static/**`（含新增 `static/data/`）、`tests/**`、`README.md`、`doc/acceptance/**`、`doc/ticket/tickets.md`——符合 DR-20 §3.5(A)-1 diff-scope。本 worklog 的 SHA 更新為其後的 record-only commit（不改受審 implementation delta）。
- **CI**：push run [35960925910](https://github.com/yotsubamomo/aiot-classwork/actions/runs/35960925910) 與 PR run [35960928988](https://github.com/yotsubamomo/aiot-classwork/actions/runs/35960928988) 皆 **success**；log 顯示 `163 passed`（Python 3.12）＋ credential scan 通過（530 tracked files、無 `.env`、無 CWA key、無 Authorization 值）。

## Remaining work

- 本 work item 的實作與 self-verification 完成（`DONE`）。**A-4 independent audit 必做**（fresh `gov-primary-reviewer` R1，範圍含 DR-20 §3.5(A)），由 Orchestrator/主 session 依 Bindings §3.5 派工；本 worklog 的 Audit status＝required（A-4），**未**自證通過。
- 不合併 `main`（RB-1）、不繳交（RB-2）、不動 Vercel/repository variable（RB-3）。
- 無未解 concern；無 BLOCKED（未觸及需外部 tile/CDN 的情況，底圖走 vendored 向量方案）。
- V-2 唯一需 Reviewer 注意處：三段色帶 fill 對「台灣陸 #25324a」<3:1，靠藥丸 2 px 白描邊達成標記界定（對海 ≥3、white border ~10:1）；如 Reviewer 認為「底圖」須以陸地色計且不接受 border rationale，屬 boundary/驗收語義疑義 → route DA（不自行改 DR-20 P-2 的陸地色）。

---

## Targeted correction（cycle 1）

治理 §4.4：只修 R1 blocking findings（F-1、F-2、F-4、F-5）＋ DA 記錄修正（DR-21.1 / DR-21.2），附 closure 與回歸證據；不弱化任何測試、不擴張 scope（仍只動地圖卡）、不改核定 token。順修的 Low findings 見末段。BASE 仍 `d23de58`；上一 subject `b4549e5`；本 correction 的新 subject SHA 見「Subject / CI（correction）」。

### 修了什麼（實作，仍在 DR-20 §3.5(A) diff-scope 內）

- **F-1 / F-2 / F-3（同一根因：浮動面板／圖例遮住 pill、tooltip、狀態訊息）**：
  - `styles.css`：把「不浮動、堆疊」版面的 breakpoint 由 `max-width:640` 提高到 **`max-width:1179`**——375 px、平板、窄桌機（≤1179）都改成資訊面板在地圖上方、圖例在下方（`position:static`），完全不疊在地圖上；浮動版面（預設規則）只在 **≥1180 px** 生效。地圖高度分開處理（≤640 → 360）。
  - `app.js`：新增唯一的 fit 函式 `fitToMarkers()`（取代 initMap 內的 `fitBounds`），依寬度算 padding——floating（≥1180）時 `paddingTopLeft:[392,64]`／`paddingBottomRight:[300,56]` 預留左上面板與右下圖例的空間，使六個標記與 tooltip 都落在面板外；<1180（堆疊）用 `[26,52]/[26,44]`。`fitToMarkers()` 在 init 與 resize 呼叫（resize 跨 1180 breakpoint 會重 fit），**切日不 fit**（view 不重設，P-12）；`fitBounds(` 全檔仍只一處（`test_fitbounds_called_exactly_once` 綠）。
  - `styles.css`：floating（≥1180）時 `.map-status { padding-left:320px; padding-right:260px }`，讓置中的 DR-19 狀態訊息避開左上面板（F-3）；<1180 面板在地圖上方，訊息不會被遮。
- **F-4（375 px 相鄰標記透明 icon box 攔截點擊，點南部右緣選到東南部）**：
  - 根因是 Leaflet `.leaflet-marker-icon.leaflet-interactive { pointer-events:auto }`（specificity 0,2,0）蓋過我的 `.pill-icon{pointer-events:none}`（0,1,0）。改為 **`.pill-icon { pointer-events:none !important }`**（!important 勝過非 important），只有 `.pill`（＋其 `::before` 44×44 hit target）可互動；label pointer-events:none。click listener 掛在 `.pill` 上（仍冒泡）。
  - 另把地圖 attribution 文字縮短為 `Natural Earth · 內政部 open data`（完整來源／授權在 README，P-2a），使 attribution control 不再橫跨到南部/東南部 pill 的 44×44 區。
- **F-5（init hazard 回歸測試無偵測力）**：`tests/test_map_frontend.py` 重寫兩個測試為**限定函式本體**（`_function_body()` brace-match + `_strip_comments()`）：`test_ensuremapsized_guards_on_nonzero_container_size`（regex 要求 `if (sized()) { cb(); return; }` 存在，且每個 `cb()` 前都有 `sized()`）、`test_fittomarkers_invalidatesize_precedes_fitbounds`（`invalidateSize()` index < `fitBounds(` index）；另加 `test_init_path_is_wired_through_the_guard_and_single_fit`。
- **順修 Low（clean，非必須）**：F-6（`colourLegend()` 移到 DOMContentLoaded，狀態下圖例已上色）、F-8（`L.marker keyboard:false`，只留 `.pill` 一個 tab stop）、F-9（補淺色 hover 截圖）。F-7/F-10/F-11 未改（SHOULD／判準外，記錄於 R1）。

### DR-21 記錄修正

- **DR-21.1 / OR-V2（V-2 採「標記整體對底圖」讀法；不改任何 token）**：見下方「### V-2（依 DR-21.1 / OR-V2 重寫）」。ACCEPTANCE.md V-2 列引用 DR-21.1。藥丸 **2 px 白色實線描邊在四種狀態（預設/hover/focus/選取）都保留**（hover/focus/選取改色為 `#9ed0ff`、寬度仍 2 px 實線；`styles.css`）。未加 halo、未改 P-2 陸地色、未改 P-4 色帶／文字色。
- **DR-21.2（masthead 導言一句為附帶改動，在 boundary 內，不還原）**：見下方「### 附帶改動（地圖卡以外）」。

### V-2（依 DR-21.1 / OR-V2 重寫）

WCAG 2.x 相對亮度公式、token 值計算（與 DR-21 §7 及 R1 §2.4 一致）。**判定：PASS（DR-21.1）**。

- **文字句**（藥丸內文對藥丸填色 ≥ 4.5，黃色帶以深字計）：blue/white **5.42**、green/white **4.54**、yellow/`#1a2230` **6.68**、red/white **5.47** — 全 PASS。
- **標記句**（每一色帶 b 與標記可能疊上的每個底圖色 c：CR(填色,c) ≥ 3 **或** CR(界定描邊,c) ≥ 3；界定描邊＝2 px 實線，適用每一狀態）：

  | 底圖色 c | fill blue | fill green | fill yellow | fill red | 描邊 #fff（預設/hover） | 描邊 #9ed0ff（focus/選取） |
  | --- | --- | --- | --- | --- | --- | --- |
  | 海 `#0f1927` | 3.26 ✓ | 3.89 ✓ | 7.39 ✓ | 3.23 ✓ | 17.67 ✓ | 10.87 ✓ |
  | 台灣陸 `#25324a` | 2.37 | 2.83 | 5.38 ✓ | 2.35 | **12.85 ✓** | 7.91 ✓ |
  | 周邊陸 `#1a2331` | 2.92 | 3.48 ✓ | 6.62 ✓ | 2.89 | 15.81 ✓ | 9.72 ✓ |

  每一色帶對每一底圖色都至少一項 ≥ 3：黃色帶填色本身即 ≥ 3；藍/綠/紅在台灣陸與周邊陸上以 2 px 白描邊（12.85／15.81）達成，作用態描邊 `#9ed0ff`（7.91／9.72）亦 ≥ 3。六個代表點皆落在台灣縣市多邊形內（藥丸相鄰底色是台灣陸 `#25324a`）。**只列「對海」的數字不足以證明 V-2**（DR-21.1 §3 明示；已同時列三個底圖色）。→ **V-2 PASS（DR-21.1）**；由 R2 自行核算後於 audit record 記錄。

### 附帶改動（地圖卡以外）

- **masthead 導言一句**（`static/index.html`，`.masthead__lead`）：由「…pick a region to see its temperature trend, daily table and weekly summary.」改寫為「…read the derived map temperature for a day on the Taiwan map, then pick a region below for its temperature trend, daily table and weekly summary.」，配合 map-first 版面描述頁面閱讀順序。DA 依 **DR-21.2** 判定此一句在本 work item boundary 內（附帶、與核定 map-first 方向一致，非 X-3「重做 masthead」）；概念詞 `Taiwan Weather Forecast`、eyebrow、`<h1>`、masthead 版面/CSS **一字/一處未動**。此為地圖卡以外的**唯一**附帶改動。

### 驗證（correction；headless Chromium via Playwright，本機 Flask，無網路/無 .env）

- **完整 offline pytest**：**164 passed**（新增 `test_init_path_is_wired_through_the_guard_and_single_fit`；F-5 兩個測試重寫）。
- **F-5 mutation 證明**（scratchpad subject 副本）：(a) 把 `invalidateSize()` 移到 `fitBounds` 之後 → `test_fittomarkers_invalidatesize_precedes_fitbounds` **FAIL**；(b) 移除 `if (sized())` guard（`cb(); return;`）→ `test_ensuremapsized_guards_on_nonzero_container_size` **FAIL**；未突變的副本三個 init 測試 PASS。即測試在 hazard 重新引入時會 FAIL。
- **F-1 / F-2（版面掃描，dark，寬度 641/700/768/800/820/834/880/900/960/1023/1024/1100/1179/1180/1280/1440/1920）**：每個寬度**六個 pill 皆不與資訊面板或圖例相交**（occludedPills=0）、**六個 tooltip 皆不被面板/圖例遮、不被容器裁切**（tooltip clip/occlude=0）。<1180 面板堆疊在地圖上方（`position:static`），≥1180 浮動且 padding 預留其空間。截圖：`issue-28-tablet-768-dark-ac17.png`（768 六 pill 全可見，對照 baseline 768 只見一顆）、`issue-28-desktop-1024-hover-south.png`（1024 南部 tooltip「南部地區」全名可見，F-2）。
- **F-3（狀態訊息不被遮）**：1280（floating）error／empty 狀態，狀態文字 rect 與面板 rect 交集 **0 px²**（`padding-left:320`），`Select Date` 可見可操作、地圖卡不空白。截圖 `issue-28-state-error.png`（完整訊息「The forecast snapshot is incomplete — …」可見）、`issue-28-state-empty.png`、`issue-28-state-loading.png`。
- **F-4（點擊選到正確 Region）**：捲動地圖入視窗後，641/768/1024/1100/375/414 每個 pill 可見範圍取樣（含右緣 fx=0.9）**全部命中該 pill**（wrongClick=0）；375 與 360 真實滑鼠點擊每個 pill 的**右緣**（fx=0.88）→ `#sel-region` 選到該 pill 自己的 Region（南部→南部地區、東南部→東南部地區…）。
- **V-4 44×44 hit grid**（375、1280）：每個 pill 中心 44×44 取樣 210–225/225 命中自己，**0 個命中其他 Region**、**0 個被 attribution 攔截**（縮短 attribution 後 東南部由 180 → 210）；少數邊緣點落在 map/label（非互動、非誤選），hit area（`.pill::before` 58×44）≥ 44×44。
- **V-3（tooltip 完整可見）**：上述掃描已含——六 tooltip 在 375→1920 全部不裁切、不被面板/圖例遮（`tipDir()` 讓上緣標記向下開）。**更正 R1 前 worklog／ACCEPTANCE 只在 1280 量、未計面板的敘述**：V-3 現於各寬度成立。
- **七日 endpoint parity（H-3，未回歸）**：七天 × 六 pill DOM 文字＝`derivedMapTemperature.toFixed(1)+"°"`、class＝`pill--<colourBand>`，**0 筆不符**。
- **零外部請求（未回歸）**：載入＋七次切日，全部 request origin 只有 `http://127.0.0.1:5000`，external=0。
- **不回歸**：`fitBounds` 一處（切日不重設視野）、`mapReqSeq` 守衛、`>Select Date</label>`/`>Select Region</label>`/表頭字串、`app.py`/`server.py`/`weather_query.py`/`api/`/`vercel.json`/`data.db` 未觸及（INV-2/9）。375 `scrollWidth==innerWidth==375`。

### 重拍的截圖（依 correction 後程式）

`issue-28-desktop-dark-ac17`、`issue-28-desktop-light-ac17`、`issue-28-desktop-dark-fullpage-ac19`、`issue-28-tablet-768-dark-ac17`（新，F-1）、`issue-28-desktop-1024-hover-south`（新，F-2）、`issue-28-375-dark-ac19`、`issue-28-375-light-ac19`、`issue-28-desktop-hover-tooltip`、`issue-28-desktop-light-hover-tooltip`（新，F-9 淺色 hover）、`issue-28-375-hover-tooltip`、`issue-28-desktop-date1/2-ac18`、`issue-28-state-error/empty/loading`。

### Subject / CI（correction）

- 新 subject SHA 與 CI run URL：見本節結尾補記（commit 後填）。
