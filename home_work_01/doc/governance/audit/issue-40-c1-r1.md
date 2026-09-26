# Audit record — Issue #40，cycle 1，R1（Formal Ticket independent audit）

| 欄位 | 內容 |
| --- | --- |
| Work Contract | GitHub Issue **#40**（`yotsubamomo/aiot-classwork`）「Radar overlay：`/api/` 代理、顯示／隱藏、雷達時間戳、獨立狀態與 1 km 地理對齊 oracle」（`gh issue view 40`：OPEN，label `ready-for-agent`，blocked-by #39（已 CLOSED），blocking #41）。Scope class **V2 Radar（ENHANCED REQUIRED）**。上位：V2 Outcome Contract `home_work_01/doc/governance/outcome-contract-v2.md`（ACCEPTED 2026-09-25，normative candidate `69c5a04`；S-7、S-11、C-1、C-4、AB-V2-5、AB-V2-9、AB-V2-10；A-3 憑證邊界）；Delta Spec `home_work_01/doc/spec/SPEC-V2.md` **v2.2**（§2.7 R-V2-RAD-1～6、§2.5 R-V2-DEG-4、§2.4 R-V2-SEC-1～3／7、R-V2-OBS-11／12（雷達路徑）、R-V2-DOC-1(9)／DOC-2、§5.3 對齊儀器與雷達重用上限、§9）；derivation record `derivation-SPEC-V2.md`（DV-5、DV-12、DV-13 含 v2.1 比例性複核、B-10、B-11、§11 #2、§15、TB-V2-7）；`decisions/decision-20260923-high-risk-categories.md`（A-1）。本票分配：AC-V2-18、AC-V2-19、AC-V2-07（雷達路徑）、AC-V2-09(c)、AC-V2-16（雷達 URL／執行期 network log）、AC-V2-17(a)(e)（雷達樣本、程式、evidence）、AC-V2-13／15（只在改變 CRS 時重驗）、AC-V2-20（CI 全綠）、README R-V2-DOC-1(9)、DOC-2。Out of scope：透明度滑桿（MAY）；雷達動畫／歷史、雨量圖層、10 分鐘資料集（Later）。 |
| 受審 subject | branch `home_work_01-v2-implementation`；BASE **`cd5da10`** .. HEAD **`9bc1b6b`**；code anchor **`fedffddf96e507a0e0b564aaaa2051ab238ff506`**。`fedffdd..9bc1b6b` 只改 `doc/governance/worklog/issue-40.md`；審查時本機 HEAD `7a42db4`（`9bc1b6b..7a42db4` 只改 run record）——皆 record-only（Bindings §7）。`git diff --name-only cd5da10 7a42db4` 全部在 `home_work_01/` 內（單元目錄外 0 檔）。 |
| Audit 種類 | **R1**（Formal 必做的 Ticket independent audit；治理 §4.1、§4.4），**cycle 1**。不是 Spec Integration Audit。 |
| 角色 | `primary_reviewer`（definition `gov-primary-reviewer`；Bindings §3.1 mapping `claude-opus-5-5`／`xhigh`） |
| Binding 證據 | 正式核對由派工者（Orchestrator）依 Bindings §3.4 記入 run record `home_work_01/doc/governance/run/run-20260925-hw01-v2-formal.md`（2026-09-26 #40 Executor return 列：`aadf0a28e2b419e94` = `gov-executor`、`claude-opus-5-5`／`high`）。Reviewer 另以 Bindings §3.4 指令讀 harness 紀錄（session `05b8408b-260a-46d3-a4fe-ec07e3ec365a`）自行觀察：`agent-a0ea5bfb8f8f1ce75` `gov-primary-reviewer` `[('claude-opus-5-5', 'xhigh')]`（本 Reviewer；第一則訊息即本次 #40 R1 派工）；`agent-aadf0a28e2b419e94` `gov-executor` `[('claude-opus-5-5', 'high')]`（第一則訊息為 #40 派工）。兩者與 Bindings §3.1（b2 override）一致。此觀察只供對照，不取代派工者的核對。 |
| Independence（治理 §2.3、§4.6） | (1) **Fresh context**：未繼承 Executor 對話；worklog `issue-40.md`、commit message、已提交截圖與 `alignment.json`／`browser-check-results.json`／`network-log.json` 一律視為待驗證主張。(2) **Binding**：見上一列。(3) **Autonomous access**：自讀 Issue、OC-V2、SPEC-V2 v2.2、derivation record、decision A-1、#35／#39 audit records、run record、git 歷史與 diff、CI run 與 log；以 `git archive` 匯出 BASE `cd5da10` 與 subject `fedffdd` 到 Reviewer scratchpad；重跑全套 pytest 與 Executor 的 #40 瀏覽器檢查與 #36～#39／V1 檢查（輸出導向 scratchpad，不覆寫已提交證據）；另**自寫** probe（`align_math.py`、`probe_align.py`、`probe_refpts.py`、`probe_h1.py`、`probe_ui.py`、`probe_ui2.py`、`probe_375.py`、`probe_panel.py`，皆在 scratchpad、未提交）：只沿用單元既有的 CDP 傳輸類別（`tests/check_modes_browser.Browser`），**測試台、圖樣、讀數與 oracle 全部自寫**——對齊以 Reviewer 自己的 Web Mercator 公式（Leaflet SphericalMercator，R = 6378137）逐列重算，並以自製的經緯線圖樣在頁面中量測**實際渲染像素**；地圖實例以頁面腳本載入前安裝的 Leaflet 公開 API `L.Map.addInitHook` 取得。(4) **Self-written record**：本紀錄由 Reviewer 以自己的 Write 工具寫入。**Model diversity：`diversity_lost`**——Executor 與 Primary Reviewer 同為 `claude-opus-5-5`（Bindings §5、b2 override；decision A-7）。合法狀態，不減損 §2.3 的 independence。 |
| 日期 | 2026-09-26 |

## 1. 審查方法與環境

- **環境**：Windows 11；`home_work_01/.venv` Python 3.12.14；Chrome headless（DevTools protocol，`websocket-client`），deviceScaleFactor 1。
- **憑證**：Reviewer **沒有讀取** `home_work_01/.env`，**沒有發出任何 CWA 或外部請求**（包含公開 S3 影像）。所有 probe 對 loopback 上未修改的 `server.create_app`（真的 `RadarService`／`LatestObservationService`），上游為模擬（已提交的消毒 metadata／觀測樣本＋Reviewer 自製 PNG），金鑰一律為**哨兵**；`probe_h1.py` 另封鎖所有非 loopback 的 DNS／socket。金鑰外洩檢查只用金鑰格式比對與哨兵。
- **不寫入**：沒有 git 寫入、沒有修改追蹤中的檔案（本紀錄除外）；結束時 `git status --short` 只有與本票無關、審查開始前即存在的 `grep.exe.stackdump`。
- **Scratchpad 揭露**：scratchpad 目錄由本 session 各角色共用。審查開始時 Reviewer 在隔離前把 `cd5da10` 解到 `scratchpad/base/`（疊在較早的匯出上）並覆寫了 `scratchpad/base_ids.txt`、`subj_ids.txt`（#39 R1 紀錄曾把同名檔列為未提交證據）；之後 #40 的全部工作都在 `scratchpad/r40rev/`，並以乾淨匯出重做 test id 比對。只影響未追蹤的 scratch 檔。
- **Commit 衛生**：`fedffdd`、`9bc1b6b` message 皆為 `[Modify] – …`＋`[Additions]／[Modification] – …` 格式；`grep -icE "claude|co-authored|generated with"` → 0。`git diff --check cd5da10 fedffdd`（排除 PNG）乾淨。（subject 外的 Orchestrator commit `7a42db4` 內文一行 `[Modification] Update …` 少了 ` – ` 分隔，只記為觀察 O-4。）

## 2. 分配 AC 的逐條結論

| AC／項目 | 判定 | 證據（Reviewer 自行取得） |
| --- | --- | --- |
| **AC-V2-18** 瀏覽器面（控制、預設、鍵盤、開／關、時間戳分開、重新取得觸發、不輪詢、失敗、圖層、地圖可用、Forecast 無 Radar） | **PASS** | 自寫 `probe_ui.py`＋`probe_ui2.py`（1280×900，真實 CDP 滑鼠／鍵盤事件）：載入後 `Radar: Off`、`aria-pressed=false`、按鈕 102.9×44、`#radar-info` 隱藏、**0 個** `/api/radar/` 請求；Tab 聚焦後 **Enter** → `Radar: On`、`pressed=true`、24 條帶附著且可見、`src` 為 `blob:`；`Radar Time` ＝ `2026-09-26 14:40 +08:00`（＝回應 `X-Radar-Time` `2026-09-26T14:40:00+08:00` 的版面重排）；**Space** → `Radar: Off`、圖層移除、資訊列隱藏；關再開 → +1 請求、取得最新（15:00）；顯示中按 `Refresh` → 雷達 +1、觀測 +1、Radar Time 更新（14:50）；**閒置 15 s → 0 個新雷達請求**。雷達 500（已有影像）→ `stale`、24 條帶保留、Radar Time 不變、「Radar Stale … (HTTP 500) — upstream_error」，觀測 state／兩個時間／有效數／57 個標記**全部不變**；首次取得連線失敗 → `unavailable`、無圖層、Radar Time「—」、「Radar unavailable … upstream_unreachable」。Forecast mode：radar 控制不可見、圖層 0、地圖卡內無可見「Radar」文字；回 Now → 圖層與 Radar Time 恢復。圖層：computed z-index backdrop 300 < radar 350（`pointer-events: none`）< overlay 400 < marker 600；在陸地上的雷達像素處 `elementFromPoint` 命中縣界 path（元素堆疊中不含雷達），hover 顯示「南投縣」、點擊選取南投縣；20 個視窗內標記的 hit-test 在雷達關／開時**完全相同**（0 差異），點擊標記選取該站（臺北 466920）；拖曳與 `+` 縮放正常。375×812：鍵盤開啟、`scrollWidth` 375 ≤ 375、按鈕 101.5×44。Executor 的 `check_radar_browser.py` 以 subject 重跑 **47/47**（`--real-image`／`--coastline` 需未提交的真實影像，其 5 項未重跑）。 |
| **AC-V2-18** API 面（image content-type、metadata `DateTime`、四類失敗、重用 ≤ 5 分鐘）；靜態（影像 URL 為 `/api/`） | **PASS** | `probe_h1.py`（真 `requests`、真 werkzeug 伺服器）：成功 `200 image/png`、`X-Radar-Time: 2026-09-26T14:40:00+08:00`（樣本 `DateTime` 原樣）、`Cache-Control: no-store`。四類見 AC-V2-07 列。重用：`REUSE_WINDOW_SECONDS = 120`、建構子拒絕 > 300（`radar.py:361-362`）、`_reusable` 以 `< window` 判定且時鐘倒退不延長（`radar.py:374-380`）；`test_reuse_window_*`／`test_clock_moving_backwards_*` 通過。靜態：`app.js` 唯一的字面請求目標是 `fetch("/api/radar/latest"`；圖層只用該回應的同源 object URL；`L.imageOverlay(`／`L.tileLayer(` 0 次；`_ALLOWED_FRONTEND_URLS` 未變。 |
| **AC-V2-19** 對齊 oracle（≤ 1 km；參考點；zoom 7 與 10；可重現自動化證據；鑑別力） | **PASS** | **Reviewer 自算**（`align_math.py`，照 `app.js` `_reset` 字面佈局——el 位於未取整的 `nw`、條帶框取整、`img.top = y0 − k(y1−y0)`、高 `(y1−y0)·24`——並考慮每個條帶裁切框可顯示的列）：3600 列在 z6／7／10／12 最大誤差 **0.0075 km**；同一計算 1 條（線性貼圖）＝ **3.8079 km @ lat 23.549**（lat 22.0 → 2.807、25.0 → 2.902，與 DV-13 的 3.8／2.8／2.9 一致）；2／3／4／8 條 ＝ 1.020／0.463／0.264／0.067 km（與 DV-13 補充的分段數字一致）；欄方向誤差 5.8e-11 px。**瀏覽器實際渲染像素**（`probe_align.py`：自製 3600×3600 透明圖樣，13 條 7 列粗的紅色緯線、10 條藍色經線，其他 pane 隱藏、白底，量線條強度重心對 Leaflet 未取整投影）：z10 八個視野（含 23.55°N 誤差峰值區、臺北、南部、澎湖、金門、北緣、南緣、東北）最大 **0.064 km**（0.45 px）；z12 最大 **0.010 km**；z7 最大 **0.713 km**（−0.65 px，正負混合、無系統偏移；z7 1 px ≈ 1.1 km，屬 §5.3 所稱粗檢的量化極限）；動畫 `zoomIn` 後、滑鼠拖曳後、Now→Forecast→Now 後、選縣（臺南市，fitBounds）後、視窗改為 1100×800 後：0.011～0.018 km。**鑑別**：同頁面放一般 `L.imageOverlay`（同一 blob、隱藏 app 圖層）量同一批線 → **3.879 km**（23.55°N）、2.896（25.04°N）、2.879（22.0°N）。**AC 參考點 DOM 幾何**（`probe_refpts.py`：依條帶裁切框選取實際顯示該像素的條帶，而非以列號假設）：四角（含圍欄外無法捲到的 NE／SE／SW）、四邊中點、中心、臺北、臺中、恆春、花蓮、馬公——z7 最大 **0.0118 km**、z10 最大 **0.0048 km**。CI 內的自動化幾何證據：`test_radar_frontend.py` 的逐列重算（z6～12）與 1 條 3.5～4.1 km 鑑別測試，另以靜態守衛鎖定 `_reset` 公式片段——與 Reviewer 的獨立計算結果一致。SHOULD 的海岸線目視：Reviewer 檢視已提交的 `coastline-003-1280-taipei-z10.png` 等（-003 黑線與縣界／25°N 格線位置合理）；Executor 的 -003 對內政部縣界數值比對（中位 0.075 km）需未提交的公開影像，Reviewer 未重跑（SHOULD，且 oracle 為幾何性質）。 |
| **AC-V2-07**（雷達路徑：四類、非機密） | **PASS** | `probe_h1.py`（真 HTTP client；metadata 上游**把收到的 `Authorization` 值回寫進本文**；root logger DEBUG；werkzeug request log；父 shell 擷取 stdout／stderr）15 例：無金鑰 → 503 `key_not_configured`；真實 CWA URL（封網）、metadata 停滯、影像停滯 → 504 `upstream_unreachable`（停滯 **5.01／5.02 s**，read timeout 5 s 先於 8 s 總上限）；metadata 401／403／429／500、影像 403 → 502 `upstream_error`＋`upstreamStatus` 數字；metadata 非 JSON、錯誤產品（別的 dataid＋大範圍）、空本文、影像非 PNG、影像 1800×1800 → 502 `invalid_response`。每例：非 2xx JSON、鍵只有 `dataset`／`reason`／`error`（＋`upstreamStatus`）、`error` 為固定句。回應本文與標頭、30 行 log、stdout、stderr 對哨兵金鑰、上游本文標記、`opendata.cwa.gov.tw`、S3 主機、`Authorization`、`ProductURL`、`fileapi`、`auth=` **全部 0 次**；log 只有 `reason=… upstream_status=…` 與成功時的雷達時間／位元組數；影像上游若收到 `Authorization` 會回 418——實際成功 200，證明影像請求不帶金鑰。另 `tests/test_radar.py` 18 個失敗案例（caplog DEBUG＋capfd）通過。 |
| **AC-V2-09(c)** 雷達失敗只改變雷達狀態；反之亦然（＋(a) 的雷達部分） | **PASS** | 兩個方向皆以瀏覽器實測（`probe_ui.py`／`probe_ui2.py`）：雷達 stale／unavailable 時觀測 state、兩個時間、有效數、標記數不變；觀測 Refresh 失敗（→ 觀測 Stale）的同一次 Refresh 中雷達成功並換上新影像（15:10、24 條帶可見）；觀測首次載入 Unavailable 時雷達可開啟成功；預報快照 503（不存在的 DB，`/api/health` 503）時雷達成功、預報區段顯示自己的 `role="alert"` 錯誤。API 面 `test_radar_failure_leaves_observation_and_forecast_answers_unchanged`、`test_observation_failure_leaves_radar_working`、`test_forecast_endpoints_answer_while_the_radar_path_is_air_gapped` 通過。 |
| **AC-V2-16**（本票範圍：雷達影像 URL 為 `/api/`；Radar 顯示中執行期零外部請求） | **PASS** | 自寫 probe 的 network log：25 個請求（含 Radar 顯示、Refresh、Forecast 往返）全部為 loopback 或 `blob:`，外部 **0**；雷達只經 `/api/radar/latest`。靜態：見 AC-V2-18 API 列；`test_static_checks.py` 只把 `radar.py` 加入 no-SQL 集合（唯一刪除行是 `_NON_SHARED_PYTHON` 定義行被延伸版取代），V1 斷言未弱化。 |
| **AC-V2-17(a)(e)**（本票範圍） | **PASS** | `git ls-files` 無 `.env`；`python -m tools.credential_scan` → `credential scan passed: 780 tracked files; no .env tracked (only .env.example); no CWA-key-format string in tracked files or committed history; no Authorization value in fixture/raw JSON.`；`git diff cd5da10 7a42db4 --text` 的 CWA 金鑰格式字串 **0**；evidence 目錄對 `Authorization=`／`opendata.cwa.gov.tw`／`amazonaws` **0 檔**命中；樣本 `O-A0058-006_metadata_sample.json` 無 `Authorization`、只有公開產品欄位（Reviewer 逐欄讀過）；樣本、`radar.py` 與三個新測試檔在 `test_secrets.py`／`credential_scan.py` 範圍內。worklog 與 run record 金鑰格式 0。A-3 使用紀錄存在（3 次 metadata GET 為樣本擷取／選變體、1 次本機定向驗證），用途在 OC A-3 (i)(ii) 內。 |
| **AC-V2-13、AC-V2-15**（只在改變 CRS 時重驗） | **不觸發**（CRS 未改；回歸仍 PASS） | `app.js` 無 `crs`／`EPSG`／`Proj4` 設定（Leaflet 預設 EPSG:3857）；頁面實測 `map.options.crs.code === "EPSG:3857"`；diff 中 `minZoom`／`maxZoom`／`maxBounds`／`fitBounds`／圍欄常數 0 變更。#39 `check_fence_browser.py` 重跑 **113/113**（含 AC-V2-13、AC-V2-15）。 |
| **AC-V2-20**（本票範圍：CI 全綠） | **PASS** | `pytest -q` → **614 passed**（Reviewer 本機，17 s）；乾淨匯出比對：BASE `cd5da10` 的 **516** 個 test id 在 subject **全部存在**，新增 98 個（`test_radar.py` 70、`test_radar_frontend.py` 22、`test_static_checks.py` 1、`test_secrets.py` 參數化 5）。CI run `36228258402`（headSha `fedffdd…`）success、log「614 passed」＋credential scan passed；`9bc1b6b`（`36228379326`）、`7a42db4`（`36228454784`）亦 success。 |
| **README R-V2-DOC-1(9)、R-V2-DOC-2** | **PASS** | README 新增「Radar endpoint (V2 Radar)」與「Now mode — Radar overlay (V2 Radar)」：來源 O-A0058-006 與透明底、對齊方式（等經緯格 vs Web Mercator、24 條帶、線性貼圖約 3.8 km、殘差約 0.01 km、投影未改）、重新取得觸發方式（開啟、顯示中 Refresh；不輪詢）、已知限制（metadata 與影像各自每 10 分鐘覆寫、影像可能比 Radar Time 新一期；產品時間的發布延遲）、失敗代碼、逾時 3／5／8 s、重用 120 s（上限 5 分鐘）；授權標示「交通部中央氣象署 雷達整合回波圖-臺灣(鄰近地區)_透明底圖（O-A0058-006）… 政府資料開放授權條款」，應用內 Now notes 亦標示（SHOULD）。新增文字無 `real-time`／`live`（唯一命中為 `aria-live` 屬性）。 |

## 3. Spec 條款對照（本票 Traceability）

| 條款 | 結論 | 說明 |
| --- | --- | --- |
| R-V2-RAD-1 | 成立 | O-A0058-006，範圍與尺寸由伺服器逐項驗證（`radar.py:184-228`），不符 → `invalid_response`。非回波區透明：已提交 `real-006-*.png` 可見底圖（Reviewer 未另取真實影像）。 |
| R-V2-RAD-2 | 成立 | 影像與時間戳同一回應經 `/api/`；metadata 金鑰只在伺服器端 `Authorization` 標頭；重用 120 s ≤ 300 s。 |
| R-V2-RAD-3 | 成立 | 見 AC-V2-18 瀏覽器列；觸發方式與 README 一致。 |
| R-V2-RAD-4 | 成立 | Radar Time 來自同一回應；stale／unavailable 與觀測獨立；已知限制已記述。 |
| R-V2-RAD-5 | 成立 | 見 AC-V2-19；CRS 未改。 |
| R-V2-RAD-6 | 成立 | 圖層順序、指標穿透、標記可讀可點、地圖可拖曳縮放。透明度滑桿未做（MAY）。 |
| R-V2-DEG-4、INV-V2-7 | 成立 | 見 AC-V2-09(c)。 |
| R-V2-SEC-1／2／3／7、R-V2-OBS-11／12（雷達） | 成立 | 見 AC-V2-07、16、17 與 §5。 |
| R-V2-OBS-13（雷達適用） | 成立（另見 F-2） | 上游 connect 3 s／read 5 s／總 8 s；前端 20 s 上限（`RADAR_TIMEOUT_MS`）後以 `no_response` 到達終態。 |
| R-V2-DOC-1(9)、DOC-2 | 成立 | 見上表。 |

## 4. Invariants

| INV | 結論 | 證據 |
| --- | --- | --- |
| **INV-V2-2** 金鑰零外洩、兩個授權位置 | **HOLDS** | 見 §5 H-1。 |
| **INV-V2-3** 瀏覽器只呼叫 `/api/`、零外部請求 | **HOLDS** | 自寫 network log 外部 0；Executor `network-log.json` 同。 |
| **INV-V2-7** 三條路徑獨立降級 | **HOLDS** | 見 AC-V2-09(c) 列（雙向＋預報 503）。 |
| INV-V2-1／4（附帶） | HOLDS | 預報 endpoint 與 `/api/health` 在封網無金鑰、雷達失敗後仍 200；`/api/health` 鍵集合不變（測試）；`server.py` diff 只新增雷達路由與參數。 |
| INV-V2-8（附帶） | HOLDS | `git diff --stat cd5da10 7a42db4` 對 `app.py`、`weather_query.py`、`ingestion/`、`data.db`、`observation.py`、`representative.py`、`api/`、`smoke.py`、`vercel.json`、`requirements.txt`、`static/data/`、`static/vendor/`、`CONTEXT.md`、`.github/`、`doc/requirement/`、`tests/test_map_frontend.py` → 空。 |

## 5. High-risk 核對段（decision A-1）

- **觸及類別**：**H-1**（憑證與機密）、**H-3**（資料語義與標示）。H-2 附帶核對。
- **H-1 核對了什麼**：(a) 兩個授權位置：`radar.py` 每次請求由 `self._env.get("CWA_API_KEY")`（`ENV_KEY_NAME` 自 `observation` 匯入）讀取、不存於物件（`radar.py:386`；`test_key_is_read_at_request_time_and_never_stored`）；預設 `env` 為 process 環境（`radar.py:363`）；本機 `.env` 載入沿用 `server.py` `__main__` 既有機制（本票未改）；Vercel 未觸及（RB-3 未觸發）。(b) 金鑰只送往 metadata 請求的 `Authorization` 標頭，影像請求 `headers={}`（`radar.py:284-292`），Reviewer 以「收到金鑰即回 418」的影像上游實證未送出。(c) 回應、標頭、log（root DEBUG）、stdout／stderr：Reviewer 哨兵 probe 15 例 0 命中（含回寫金鑰的上游本文與封網例外訊息）；`urllib3` logger 設 ERROR（`radar.py:73`）；例外一律 `raise … from None`、失敗文字固定。(d) git／樣本／evidence：`.env` 未追蹤；credential scan 0；diff 金鑰格式 0；樣本無 `Authorization`；evidence 無上游主機或 `Authorization=`。(e) 前端：頁面 HTML 無哨兵、無上游主機；失敗文字只來自固定表，不顯示回應內容（`classifyRadarFailure` 只讀 `reason` 與數字 `upstreamStatus`）。(f) SSRF 面：ProductURL 必須是 `https`、主機屬白名單、無 userinfo、port 443（17 個 metadata 反例測試）。
- **H-1 結果**：**PASS**。
- **H-3 核對了什麼**：(a) 雷達時間逐字標為 `Radar Time`、自成 `<dt>/<dd>`（`#radar-time`，位於 `#radar-info`），與 `Observation Time`（`#obs-time`）、`Fetched Time`（`#obs-fetched`）是不同元素、不同標籤（Reviewer DOM 讀取）；桌機與 375 截圖三者並列可辨。(b) Radar Time 為 metadata `DateTime` 原樣（只做版面重排），來自與影像同一回應。(c) 雷達不計算任何值，不改變觀測或預報數值；雷達失敗不改動觀測顯示（實測）。(d) CWA 授權標示：README 兩處＋應用內 Now notes；Forecast mode 中不可見。(e) 新增文字無 `real-time`／`live`。
- **H-3 結果**：**PASS**。
- **H-2（附帶）**：老師指定的檔案與頁面文字未動（§4 INV-V2-8 列）；#36 檢查（下方 dashboard、`Select Region`、AC-17／18 重驗）37/37。**PASS**。

## 6. 變更風險（治理 §4.4）：#36～#39 的回歸

- **重跑既有瀏覽器檢查（subject 工作樹，輸出到 scratchpad）**：#36 `check_modes_browser.py` **37/37**（一次即過）；#37 `check_refresh_browser.py` **97/97**；#38 `check_county_browser.py` **72/72**；#39 `check_fence_browser.py` **113/113**（第一次因 console 編碼 cp950 無法印出 U+2212 而中止，以 `PYTHONIOENCODING=utf-8` 重跑；非產品問題）；V1 `check_series_error_visible.py` PASS。
- **底圖改換 pane**：兩層 backdrop GeoJSON 由 overlay pane（400）移到新 `backdrop` pane（300），相對於縣界互動圖層（400）與標記（600）的順序不變；Forecast mode 回歸（#36）通過。
- **#39 F-1 的回歸風險（雷達新增的狀態列）**：自寫 `probe_panel.py`，1024×768、1280×900、1280×720，雷達開啟＋選縣（臺中市）＋清單選站，success 與雷達 stale：`Observation Time`、`Fetched Time`、`Refresh`、雷達按鈕、`Radar Time`、雷達狀態、County 選單可視比例皆 **100%**；測站詳情可視 254 px（success）／181 px（stale，狀態文字較長）。#39 檢查本身不含雷達情境，此項由 Reviewer 補驗。**無回歸**。

## 7. Executor 自述 concerns 的獨立判斷

- **(a) §5.3 的 px 換算註記** → **(i) 無害；非 blocking；建議 Design Authority 做文字澄清（R-1）**。Reviewer 自算 Web Mercator 在臺灣緯度的 1 km：z7 **0.873～0.914 px**（23.5°N 0.892）、z10 **6.98～7.31 px**（7.133）、z12 27.9～29.2 px，與 §5.3 的「z7 ≈ 0.35 px、z10 ≈ 2.8 px」差約 2.5 倍；DV-13「1 km … 在 zoom 10 約 2.8 CSS px」同。契約 oracle 是**地面距離 1 km**（R-V2-RAD-5、AC-V2-19「≤ 1 km 地面距離（換算為該 zoom 的 px）」），§0 明文儀器不是產品語義，因此不改變本票任何判定。即使有人把 px 註記字面當門檻（約 0.39 km），DOM 幾何（z7 0.0118 km、z10 0.0048 km）與 z10 渲染量測（0.45 px < 2.8 px）仍通過；只有 z7 的渲染像素量測（0.65 px）會超過 0.35 px——那是 1 px ≈ 1.1 km 的量化極限，正是 §5.3 把 z7 定為粗檢的原因。
- **(b) 375 px 地圖下移** → **可接受；記為 F-1（Low，non-blocking）**。見 §8。
- **(c) metadata 與影像各自每 10 分鐘覆寫** → **可接受，不是 finding**。R-V2-RAD-4 已明文把「metadata 時間與影像可能短暫不一致」定為須在 README 記述的已知限制；實作緊接讀取、單一回應回傳，README 已記述「影像可能比 Radar Time 新一期直到下次取得」。
- **(d) Vercel 行為未驗證** → **屬 #41**（AC-V2-17(c)、AC-V2-22 分配給 #41，且需 acceptor 填入金鑰）；不在本票分配。`vercel.json` 未設 `maxDuration`，README 以「低於 10 s」描述上游上限，是否成立由 #41 preview 驗證（與 #35 F-2 同一追蹤，見 F-2）。
- **(e) Leaflet 內部 `_latLngToNewLayerPoint`** → **robustness 觀察（O-1），不是 finding**。vendored Leaflet 1.9.4（`static/vendor/` 無 diff）內存在此方法，且 Leaflet 自己的 marker／popup／image overlay 縮放動畫都使用它；只在更換 Leaflet 版本時需重驗縮放動畫（Reviewer 已實測動畫 `zoomIn` 後對齊 0.011 km）。

## 8. Findings

### F-1 — 375 px 時雷達控制使地圖在首屏的可見高度減少（Low，non-blocking）

- **證據**：自寫 `probe_375.py`，同一模擬資料下比較 BASE `cd5da10` 與 subject（地圖高 360 px；數值為地圖頂端 y／首屏可見地圖高度）：375×812——BASE 554／258 px；subject 雷達關 610／202、雷達開 642／170、雷達 stale 715／97。375×667——BASE 113 px；subject 關 57、開 25、stale 0。原因：`Refresh` 旁新增按鈕使 County 選單換到下一列（約 +56 px），雷達開啟再加 `Radar Time` 列，stale 時加 3～4 行原因文字（已提交 `375-radar-stale.png` 可見）。
- **契約**：R-V2-MODE-2(a) 模式切換不捲動可見——成立；R-V2-RSP-2（`scrollWidth`）、RSP-3（44×44）——成立；R-V2-RSP-4「地圖 MUST 是頁面的主要內容區」沒有首屏量化判準，且 BASE 在 375 已有部分地圖在首屏之外；R-V2-RSP-5 的資訊面判準不受影響。無契約違反。
- **為何 non-blocking**：可用性退化而非契約違反；stale 是使用者開啟雷達後才會出現的失敗狀態。
- **Disposition**：本票不需修改。**Owner：Spec Integration Audit**——作為整合層觀察，評估 #36～#40 累積在 375 地圖上方的控制高度對 R-V2-RSP-4「主要內容區」與 User Story 7 的影響；若 SIA 或 DA 認為需要壓縮（例如雷達按鈕與 County 同列、縮短 stale 文字），屬 HOW，只能在後續合法授權的變更中處理。

### F-2 — 雷達服務在整個上游取得期間持鎖，並行停滯請求被序列化（Low，non-blocking；與 #35 F-2 同型）

- **證據**：`RadarService.latest()` 以 `with self._lock:` 包住 `fetch_product`（`radar.py:384-399`，上限 8 s），失敗不快取。Reviewer probe：3 個同時請求、停滯上游、deadline 1.0 s → **1.02／2.02／3.03 s** 完成（皆 `upstream_unreachable`）。以預設 8 s 推算，同一 instance 的第 2 個並行請求約 16 s，可能超過平台時限而變成平台層錯誤。
- **契約**：R-V2-OBS-13（雷達適用）。前端 20 s 上限與 `unexpected_response`／`no_response` 分類使 UI 仍在 30 s 內到達終態（Executor 檢查的停滯／超時情境與 Reviewer 閱讀 `requestRadar` 一致）。
- **為何 non-blocking**：與 #35 R1 F-2（觀測路徑，Medium non-blocking）同一模式；在每個 instance 一次處理一個請求的部署模型下不發生；平台並行與時限本就由 #41 preview 驗證。本票前端已提供契約要求的平台錯誤處理，故以 Low 記。
- **Disposition／owner**：併入 #35 F-2 既有追蹤——**#41**（preview 驗證 Vercel 時限與並行行為）；平台證據若顯示超出界限，依 derivation §11 #1 route **Design Authority**。修正方式（不跨上游呼叫持鎖、single-flight 等）屬 HOW，只能在後續合法授權的變更中處理。

## 9. Routing signals（治理 §4.2；不是 blocking finding）

### R-1 — §5.3 雷達對齊列與 DV-13 的 px 換算數值與 Web Mercator 不符（required authority：**Design Authority**）

- **具體事實**：SPEC-V2 §5.3 R-V2-RAD-5 列「換算 px：z7 ≈ 0.35 px、z10 ≈ 2.8 px」與 derivation record DV-13「1 km … 在 zoom 10 約 2.8 CSS px」；Reviewer 以 Leaflet EPSG:3857 公式在 lat 20.5～26.5 計算為 z7 0.87～0.91 px／km、z10 6.98～7.31 px／km，頁面量測一致（#39 實測 z12 28.95 px／km 亦同尺度）。同表 R-V2-MAP-3 列「z12 時 1 km ≈ 24 px」亦低於實測（28.5～29.2），方向不影響 #39 的 PASS。
- **Ambiguity**：讀者若把 §5.3 的 px 註記當作 AC-V2-19 的換算門檻，會套用約 0.39 km 而非 1 km；DV-13 比例性複核中「200 m 在 zoom 10 不足 1 px」的前提亦以錯誤尺度計算（實為約 1.4 px），但保留 1 km 的結論不受影響。
- **對本 audit 的影響**：無。oracle 為地面距離，本票以 km 判定並在任一讀法下的主要判定（DOM 幾何、z10）皆通過。建議 DA 以治理 §5.3 允許的非語義修訂更正 §5.3 註記（與 DV-13 的對應句），由 DA 決定是否及何時處理；不阻擋本票。

## 10. Observations（不是 findings）

- **O-1**：Leaflet 內部 API `_latLngToNewLayerPoint`（見 §7(e)）。更換 Leaflet 版本時須重驗雷達縮放動畫。
- **O-2**：`fetch_product` 的 worker 內 `except Exception` 會把 metadata 解析中的非預期例外（例如極深巢狀 JSON 的 `RecursionError`）歸為 `upstream_unreachable` 而非 `invalid_response`；CWA 實際 metadata 碰不到，四類代碼仍在集合內、非機密。記錄即可。
- **O-3**：伺服器只對 ProductURL 做主機白名單；`requests` 會跟隨影像主機的重新導向（不帶金鑰；`requests` 對跨主機重新導向亦會移除 `Authorization`）。不在契約範圍，記錄供 SIA 知悉。
- **O-4**：subject 外的 Orchestrator commit `7a42db4` 內文 `[Modification] Update …` 缺少 ` – ` 分隔（`docs/conventions/git-commit-rules.md` 範例格式）。
- **O-5**：#36 N-1（同秒 Fetched Time 偽陽性）本輪未重現（37/37 一次即過）；owner 依 #38 R2 不變。

## 11. Evidence（Reviewer scratchpad，未提交）

`C:\Users\yotsu\AppData\Local\Temp\claude\D--nchu-2026-AIoT-git-repository-aiot-classwork\05b8408b-260a-46d3-a4fe-ec07e3ec365a\scratchpad\r40rev\`：
- `base/`（`git archive cd5da10`）、`subj/`（`git archive fedffdd`）；`base_ids.txt`／`subj_ids.txt`（516／614，差集 0）。
- `align_math.py`（逐列對齊與線性貼圖、分段數、px／km）；`probe_align.py`＋`align_out/`（渲染像素量測、互動後量測、線性貼圖鑑別，`results.json` 與截圖）；`probe_refpts.py`（AC 參考點 DOM 幾何）。
- `probe_h1.py`＋`h1.out`／`h1.err`（四類失敗、哨兵、DEBUG log、stdout／stderr）。
- `probe_ui.py`＋`ui.log`（第一版；7 個 FAIL 為 Reviewer probe 自身的讀數錯誤——以 0×0 的圖層外框判斷可見，及不公平的標記 hit 讀法——已由 `probe_ui2.py`＋`ui2.log` 以條帶可見性與雷達關／開同點 hit-test 重做，8/8）；`ui_out/`（截圖）。
- `probe_375.py`＋`l375-*.png`（F-1）；`probe_panel.py`＋`ui_out/panel-*.png`（#39 F-1 回歸）。
- `ex_radar/`＋`ex_radar.log`（Executor #40 檢查重跑 47/47）；`reg_modes`、`reg_refresh`、`reg_county`、`reg_fence`、`reg_series.log`、`reg_summary.txt`（#36～#39、V1 重跑）。
- 指令：`pytest -q`（614 passed）；`pytest --collect-only` 差集；`gh run list`／`gh run view 36228258402 --log`；`python -m tools.credential_scan`；`git diff --stat／--check／--name-only`；Bindings §3.4 binding 指令。

VERDICT: CLOSURE
