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
- **V-2（對比，token 值計算，WCAG）**：
  - 藥丸內文 vs 藥丸底（≥4.5）：blue #2b6cb0/#fff = **5.42**；green #2f855a/#fff = **4.54**；yellow #d69e2e/#1a2230 = **6.68**；red #c53030/#fff = **5.47**。全部 PASS。
  - 四段色帶 vs 底圖（≥3）：vs 海 #0f1927 → blue **3.26**、green **3.89**、yellow **7.39**、red **3.23**（全 ≥3，PASS，海為地圖 base 背景）。vs 台灣陸 #25324a → blue 2.37、green 2.83、red 2.35、yellow 5.38（blue/green/red <3）；此三段以藥丸 **2 px 純白描邊**（#fff 對海與陸皆 ~10:1）界定標記與底圖的邊緣，滿足 WCAG 1.4.11 非文字對比 ≥3。記為 PASS with border rationale。
- **V-3（tooltip 不裁切）**：desktop(1280) 與 375 各對六標記逐一開 tooltip，量測 tooltip rect 皆在 `.leaflet-container` 內（最小邊距 4.2 px，`clippedAny=false`）。上緣標記（北部/南部/東南部）以 `tipDir()` 向下開避免上緣裁切。
- **V-4（可點區 ≥44×44）**：`.pill::before` 置中 44 px 高、≥44 px 寬透明 hit target；`.pill-icon`/`.rlabel` pointer-events:none，相鄰標記不互擋（Playwright 逐一 hover 六標記皆命中）。
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
- Subject SHA、CI run URL：見下方 commit/CI 段。

## Remaining work

- 本 work item 的實作與 self-verification 完成（`DONE`）。**A-4 independent audit 必做**（fresh `gov-primary-reviewer` R1，範圍含 DR-20 §3.5(A)），由 Orchestrator/主 session 依 Bindings §3.5 派工；本 worklog 的 Audit status＝required（A-4），**未**自證通過。
- 不合併 `main`（RB-1）、不繳交（RB-2）、不動 Vercel/repository variable（RB-3）。
- 無未解 concern；無 BLOCKED（未觸及需外部 tile/CDN 的情況，底圖走 vendored 向量方案）。
- V-2 唯一需 Reviewer 注意處：三段色帶 fill 對「台灣陸 #25324a」<3:1，靠藥丸 2 px 白描邊達成標記界定（對海 ≥3、white border ~10:1）；如 Reviewer 認為「底圖」須以陸地色計且不接受 border rationale，屬 boundary/驗收語義疑義 → route DA（不自行改 DR-20 P-2 的陸地色）。
