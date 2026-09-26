# Worklog — Issue #40 Radar overlay：`/api/` 代理、顯示／隱藏、雷達時間戳、獨立狀態與 1 km 地理對齊 oracle

- **Work item**：GitHub Issue #40（Formal lane，**V2 Radar**（ENHANCED REQUIRED）；Blocked by #39——已 CLOSED；blocking #41）
- **Executing role**：`executor`，以 `gov-executor` definition 派工（Bindings §3.1 mapping：`claude-opus-5-5`，effort `high`）。本 session 自述的模型為 Opus 5.5；**這不是 binding 證據**。Binding verification 依 Bindings §3.4 由派工者（Orchestrator）從 harness 紀錄核對並記入 run record 或 audit record；本 worklog 不複製 harness 日誌。
- **Branch**：`home_work_01-v2-implementation`；**BASE ＝ `cd5da10`**（#39 結案 commit）
- **Subject**：code anchor ＝ `fedffdd`（BASE `cd5da10`..`fedffdd` 為本票全部產物變更，含 evidence）；其後只改 `doc/governance/**` 的 commit（本 worklog）為 record-only（Bindings §7 P7）。
- **開始／本次更新**：2026-09-26

## Contract reference

- **Outcome Contract**：`home_work_01/doc/governance/outcome-contract-v2.md`（ACCEPTED 2026-09-25；normative candidate `69c5a04`）——S-7、S-11、C-1、C-4、AB-V2-5、AB-V2-9、AB-V2-10；**A-3**（實作期金鑰使用，本票使用，紀錄見下）。A-4 未使用（workflow 未改）。
- **Spec**：`home_work_01/doc/spec/SPEC-V2.md` **v2.2**——§2.7 R-V2-RAD-1～6；§2.5 R-V2-DEG-4；R-V2-SEC-1～3、SEC-5、SEC-7；R-V2-OBS-11／12（雷達路徑）；R-V2-DOC-1(9)、DOC-2；§5.3 對齊儀器與雷達重用上限（≤ 5 分鐘）；§9 已知風險（metadata／影像週期、重投影）。
- **Derivation record**：`derivation-SPEC-V2.md` DV-5（重用上限）、DV-12（預設隱藏、觸發方式 HOW、不輪詢）、DV-13（1 km oracle，含 v2.1 比例性複核）、B-10、B-11、§11 #2（透明變體：本票採用 -006，見 Decisions 1，未 route DA）、§15（本票分配：AC-V2-07（雷達）、09(c)、16（雷達 URL／log）、17(a)(e)（雷達）、18、19、20（範圍）；13、15 只在改變 CRS 時重驗）、TB-V2-7。
- **High-risk**：`decision-20260923-high-risk-categories.md` A-1（本票觸及 **H-1**、**H-3**）；核對材料見下方專節。
- **契約變更**：無。未修改任何 requirement、AC、invariant、gate、oracle。**地圖 CRS 未改變**（仍為 Leaflet 預設 Web Mercator `EPSG:3857`）。§5.3 雷達儀器（參考點、zoom 7／10、1 km）照用；見 Decisions 5 對 §5.3「換算 px」數字的觀察。

## Decisions and assumptions（HOW；Spec §5.2 委派）

1. **產品變體：O-A0058-006**（雷達整合回波圖-臺灣(鄰近地區)_透明底圖）。依 A-3 以一次唯讀 GET 取得 -003、-005、-006 三份 metadata（見 A-3 紀錄）：-003（無地形）範圍 118–124／20.5–26.5 但影像為不透明 RGB（灰陸地、白海、經緯線、logo）會遮蔽底圖；-005 是**較大範圍**（115.00–126.50／17.75–29.25）透明變體；**-006 範圍＝Spec R-V2-RAD-1 的 lon 118.0–124.0／lat 20.5–26.5、3600×3600、RGBA 透明底**（公開影像實測：alpha 0／255，只有 1.3 % 像素不透明），直接滿足 RAD-6「非回波區不遮蔽底圖」，伺服器不需影像處理、不新增相依套件。derivation record §11 #2 的未決事項因此不需 route DA。
2. **Endpoint 形態：一次回應同時帶影像與時間戳**。`GET /api/radar/latest` 成功回 `200 image/png`（影像位元組），雷達產品時間在**同一回應**的 `X-Radar-Time` 標頭（metadata `DateTime` 原樣），另 `X-Radar-Fetched-Time`、`X-Radar-Dataset`、`Cache-Control: no-store`；失敗回非 2xx JSON `{dataset, reason, error}`（四個代碼同觀測路徑，`upstreamStatus` 只在 `upstream_error`）。理由：若以 JSON 回時間、另一請求取影像，在 Vercel 多實例下兩請求可能落在快取不同期的實例，時間與影像會不一致；一次回應使 R-V2-RAD-4「時間戳來自與影像同一次伺服器取得」在任何部署拓撲下成立。前端以 `fetch("/api/radar/latest")` 取回，`URL.createObjectURL(blob)` 後放進圖層（同源 blob URL，不產生網路請求）；`fetch` 的字面目標是 `/api/`（R-V2-SEC-4(b)）。
3. **伺服器 `radar.py`（新模組；#35 pattern）**：metadata 自 `https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/O-A0058-006`（`downloadType=WEB`、`format=JSON`），**金鑰只放在該請求的 `Authorization` 標頭**（A-3 實測 fileapi 接受標頭授權，不需把金鑰放進 URL）；再依 metadata 的 `ProductURL` 取影像，**影像請求不帶任何標頭（金鑰永不送往第三方主機）**。產品檢查（任一不符 → `invalid_response`）：`dataid` ＝ O-A0058-006、`DateTime` 可解析（沿用 `observation.parse_obs_time`）、`LongitudeRange`／`LatitudeRange` 數值等於 118.0–124.0／20.5–26.5、`ImageDimension` 3600×3600、`mimeType` image/png、`ProductURL` 為 https、主機屬 `IMAGE_HOSTS`（只有 `cwaopendata.s3.ap-northeast-1.amazonaws.com`；無 userinfo、無非 443 port——metadata 不能把伺服器導到別處）；影像須為 PNG 簽章且 IHDR 3600×3600、≤ 4 MB（Vercel 回應上限 4.5 MB；實測 ~76–80 KB）。上游有界時間：connect 3 s、read 5 s、metadata＋影像**合計** 8 s（worker thread＋join，同 #35），逾時 → `upstream_unreachable`。重用視窗 **120 s**（上限 300 s，建構子拒絕 > 300），只快取成功；記憶體內。log 只記 reason、數字狀態碼、雷達時間與位元組數；`urllib3` logger 設 ERROR（同 #35）。四個失敗代碼字串自 `observation` 匯入（單一來源）；錯誤文字為固定句（"Radar is unavailable: …"）。
4. **地理對齊（R-V2-RAD-5、AC-V2-19）：分條帶（strip）放置，未改 CRS**。影像是等經緯度格（列依緯度等距，1/600°），地圖是 Web Mercator。`createRadarLayer()`（自訂 `L.Layer`）把影像畫成 **24 條水平條帶**（每條 150 列＝0.25° 緯度）：第 k 條的框放在其上緣緯度與下緣緯度的 Mercator 投影 y 之間，框內放一張整幅影像、以該條帶的列尺度縮放並位移，使該條帶的列恰好填滿框（框邊取整數 px 使相鄰條帶無縫；位移補回取整差）；經度在兩投影皆線性，所以每一欄精確。每次 `zoom`／`viewreset` 重算；縮放動畫期間整層以 `setTransform` 等比縮放（同 Leaflet ImageOverlay）。殘差（以同一 Mercator 公式對每一列重算）：1 條＝3.808 km（＝DA 的 3.8 km）、2 條 1.020、4 條 0.264、8 條 0.067、**24 條 0.0075 km**，與 DA 的分段數字一致。**地圖 CRS 未改變**，所以 AC-V2-13／15 依本票分配不需重驗（仍以 #39 檢查回歸跑過，見 V-6）。
5. **§5.3 對齊儀器的 px 換算**：§5.3 寫「1 km 換算 px：z7 ≈ 0.35 px、z10 ≈ 2.8 px」。以 Web Mercator 公式在 lat 23.5 計算，1 km ≈ **0.89 px（z7）／7.1 px（z10）**（#39 實測 z12 28.95 px/km 亦符合後者）。oracle 本身是**地面距離 1 km**，本票的量測一律以該點緯度的 km/px 換算為 km 判定，不使用上述 px 數字；此差異不影響 PASS／FAIL，只記錄供 Reviewer／DA 參考（不需裁決）。
6. **圖層順序（R-V2-RAD-6）**：新增兩個 Leaflet pane——`backdrop`（z-index 300，放原本兩層不可互動的底圖 GeoJSON）與 `radar`（z-index 350，`pointer-events: none`）；縣界互動圖層留在 Leaflet 的 overlay pane（400），站點標記在 marker pane（600）。因此雷達在底圖之上、縣界互動與標記之下，指標事件穿過雷達到縣界／地圖。底圖只換 pane，樣式與幾何不變；Forecast mode 外觀不變（#36 回歸 PASS）。
7. **控制與狀態（R-V2-RAD-3／4）**：`Refresh` 旁新增真按鈕 `Radar: Off`／`Radar: On`（`aria-pressed`、開啟時填色），**預設 Off**，只在 Now panel（`data-mode="now"`），Forecast mode 沒有控制也沒有圖層；回到 Now mode 時先前顯示的雷達與其時間回來。顯示時才取得。**重新取得的觸發方式（HOW，README 記載）**：(a) 開啟 Radar（關再開即取最新）；(b) Radar 顯示中按 `Refresh`（觀測與雷達各自請求、各自結果）。無 timer、無輪詢。雷達狀態獨立於觀測：`loading`（spinner）、`success`、首次失敗 `unavailable`（無 overlay、"Radar unavailable" ＋類別原因）、已有影像時失敗 `stale`（保留影像與其 Radar Time、"Radar Stale" ＋原因）；下一次成功清除。前端時間上限 20 s（同觀測）；較舊的雷達時間不取代已顯示者（多實例重用時可能發生，顯示 "Already the latest radar image."）。失敗類別文字固定、不顯示任何回應內容。`Radar Time` 在 Refresh 列下方自成一列（`<dt>Radar Time</dt>`），與 `Observation Time`、`Fetched Time` 分開（H-3）。
8. **應用內 CWA 授權標示（R-V2-DOC-2 SHOULD）**：放在地圖下方的 Now mode notes（不放 Leaflet attribution control，避免 #28 F-4 所述的 375 px 標記遮擋）；README 另有完整標示。
9. **版面副作用（記錄）**：375 px 下多一個按鈕使 `Refresh` 列與 `County` 選單不再同列，Radar 關閉時地圖上緣下移約 54 px（Radar 開啟時再多 Radar Time 一列）；≥ 1024 px 的 Now panel 狀態區在 Radar 開啟時多一至兩列，資訊部分（`#sheet-body`）相應變矮。#39 的 F-1 guard（面板不捲動、狀態列固定）與 375 各狀態 `scrollWidth` 回歸皆 PASS（V-6）。`ui-ux-pro-max-skill` 未使用。透明度滑桿（MAY）未做；圖層固定 0.8 不透明度。

## Artifacts（code anchor `fedffdd`；BASE `cd5da10`）

| 檔案 | 動作 |
| --- | --- |
| `home_work_01/radar.py` | 新增：Radar service（metadata＋影像、產品檢查、四類失敗、有界 fetch、重用視窗） |
| `home_work_01/server.py` | 修改：`create_app(..., radar_service=None)`；`GET /api/radar/latest`；docstring |
| `home_work_01/static/app.js` | 修改：Radar 常數與狀態、`toggleRadar`／`loadRadar`／`requestRadar`／`classifyRadarFailure`／`decodeRadar`／`applyRadar`／`applyRadarFailure`／`radarFailureText`／`renderRadar`／`syncRadarLayer`／`createRadarLayer`；`initMap` 的 `backdrop`／`radar` pane；`syncMap` 呼叫 `syncRadarLayer`；Refresh 的點擊處理加一行 |
| `home_work_01/static/index.html` | 修改：`#radar-toggle`、`#radar-info`（`Radar Time`、`#radar-status`）、Now notes 的雷達授權標示 |
| `home_work_01/static/styles.css` | 修改：`.btn--radar`、`.radar-info`、`.radar-status--*`、`.radar-layer*` |
| `home_work_01/tests/test_radar.py` | 新增：70 項（參數化後） |
| `home_work_01/tests/test_radar_frontend.py` | 新增：22 項靜態守衛與幾何證據 |
| `home_work_01/tests/check_radar_browser.py` | 新增：可重現的瀏覽器檢查（pytest 不收集） |
| `home_work_01/tests/fixtures/O-A0058-006_metadata_sample.json` | 新增：消毒真實 metadata 樣本（擷取 2026-09-26 14:51 +08:00，雷達時間 14:40；未縮減，只重新縮排） |
| `home_work_01/tests/test_static_checks.py` | 修改（只加）：`radar.py` 加入 no-SQL／no-`sqlite3` 集合＋一個存在性測試 |
| `home_work_01/tests/test_secrets.py` | 修改（只加）：樣本加入 artifact 掃描；4 個新檔加入 V2 程式憑證掃描；CI 清單含樣本的斷言 |
| `home_work_01/tools/credential_scan.py` | 修改（只加）：`_AUTH_ARTIFACTS` 加入樣本 |
| `home_work_01/README.md` | 修改：新增「Radar endpoint (V2 Radar)」「Now mode — Radar overlay (V2 Radar)」；模式表、CWA 存取句、測試段 |
| `home_work_01/doc/acceptance/screenshots/v2/issue-40/*` | 新增：截圖、`browser-check-results.json`、`alignment.json`、`network-log.json`、`regression-check-issue-{36,37,38,39}-*.json` |

未修改：`app.py`、`weather_query.py`、`ingestion/**`、`data.db`、`observation.py`、`representative.py`、`api/**`、`smoke.py`、`vercel.json`、`requirements.txt`、`static/data/**`、`static/vendor/**`、`CONTEXT.md`、`.github/workflows/**`、`doc/requirement/**`、#36～#39 的測試與檢查；單元目錄外無變更（RB-5）。

## Verification

環境：Windows 11，`home_work_01/.venv` Python 3.12.14；Chrome headless（DevTools protocol，`websocket-client`）；`node --check static/app.js`。以下 subject 皆為 `fedffdd`；最後一次瀏覽器檢查前後以 sha256 確認 `app.js`／`index.html`／`styles.css`／`radar.py`／`server.py` 未變。

- **V-1 全套**：`python -m pytest -q` → **614 passed**（BASE 516 ＋ `test_radar.py` 70 ＋ `test_radar_frontend.py` 22 ＋ `test_static_checks.py` 1 ＋ `test_secrets.py` 參數化 5）。全離線、無金鑰。
- **V-2 quality floor**：以 `git archive cd5da10` 匯出 BASE 收集 test id：BASE 的 **516** 個 id 在 subject **全部存在**（差集為空）。`test_static_checks.py`／`test_secrets.py`／`credential_scan.py` 唯一被刪的行是 `_NON_SHARED_PYTHON` tuple 的定義行（改為附加 `_RADAR` 的版本）。#36～#39 的測試與檢查、V1 `test_map_frontend.py` 皆空 diff。無 skip、無門檻降低。
- **V-3 CI**：push `fedffdd` 後 workflow「home_work_01 CI」run **`36228258402`** **success**：`614 passed`；`credential scan passed: 779 tracked files …`。Workflow 未修改（A-4 未使用）。
- **V-4 憑證（AC-V2-17(a)(e)）**：`python -m tools.credential_scan` passed；以腳本讀 `.env`（不印出）比對 `git diff --cached --binary` 全文（4,159,056 bytes）→ 真金鑰字面 **False**、金鑰格式 **False**；evidence 目錄 grep 哨兵金鑰、上游標記、`opendata.cwa.gov.tw`、`amazonaws`、`Authorization` → **無命中**；`git ls-files` 無 `.env`。
- **V-5 伺服器路徑（AC-V2-18 API 面、AC-V2-07 雷達、R-V2-RAD-2）**，`tests/test_radar.py`（70）：樣本解析出雷達時間 `2026-09-26T14:40:00+08:00` 與範圍／尺寸／主機；17 個 metadata 反例（別的 dataset、缺／壞／只有日期的 `DateTime`、-005 大範圍、平移範圍、別的尺寸、非 PNG mime、http、別的主機、仿冒主機、userinfo、別的 port、缺／非文字 URL）＋5 個錯誤形狀 → `invalid_response`；6 個非產品影像（空、GIF、半尺寸、少一列、截斷、無 IHDR）＋超過上限 → `invalid_response`。API 成功：`200 image/png`、本文＝上游影像、`X-Radar-Time`＝metadata `DateTime`、`X-Radar-Fetched-Time`＝可控時鐘 `+08:00`、`Cache-Control: no-store`。金鑰只在 metadata 請求的 `Authorization` 標頭；影像請求 `headers == {}`、任何部分無金鑰。重用：119 s 同一物件、120 s 重取、0 每次重取、301 被拒、失敗不重用且不回舊影像、時鐘倒退不延長。**18 個失敗案例**（無金鑰、空白金鑰、metadata 連線錯誤／讀取逾時／非預期例外（訊息含金鑰與主機）、影像連線錯誤、metadata 401／403／429／500、影像 403／500、非 JSON、非 UTF-8、JSON 陣列、大範圍產品、影像非 PNG、尺寸不符）→ 期望的 `reason`，`upstreamStatus` 只在 `upstream_error`；回應本文、標頭、caplog（root DEBUG）、capfd 皆無哨兵金鑰、兩個上游主機、上游本文標記、`Authorization`、`ProductURL`。Loopback 停滯／滴流 → 504 `upstream_unreachable` < 3 s；封網經真實 `requests` → 504、無洩漏；process env 無金鑰 → 503 `key_not_configured`。
- **V-6 AC-V2-09(c) API 面與 INV-V2-1／4**：雷達 502 → 觀測仍 200 且測站相同、`/api/health` 相同（鍵集合不變）；觀測 504 → 雷達 200 PNG；封網無金鑰時雷達失敗後 `/api/health`、`/api/regions`、`/api/days` 仍 200。
- **V-7 A-3 本機實測（README 步驟）**：`python server.py`（金鑰只能來自 `.env`）：`/api/radar/latest` 第一次 **200** `image/png`、**0.5 s**、雷達時間 `2026-09-26T15:10:00+08:00`（fetched 15:20:50）、**75,633 bytes**、PNG 3600×3600、`X-Radar-Dataset: O-A0058-006`、`no-store`；第二次為重用（位元組與 fetched time 相同）；health 200。伺服器 log 10 行；log 與回應標頭：金鑰字面 False、金鑰格式 False、`opendata.cwa.gov.tw` False、S3 主機 False；影像位元組不含金鑰。
- **V-8 AC-V2-19 對齊（方法見 Decisions 4；CRS 未改）**：
  - *幾何證據（CI）*：`test_radar_frontend.py` 以 Web Mercator 公式重算 `_reset` 對影像**全部 3600 列**在 **zoom 6～12** 的放置（靜態守衛鎖定 `app.js` 內的公式片段）：最大 **0.0075 km**（上限 1 km，測試斷言 ≤ 0.05）；同一重算用 1 條＝**3.808 km**（測試斷言 3.5～4.1 km、位於 22.5～24.5°N，即 DA 的數字），證明檢查有鑑別力；欄方向精確（差 < 1e-6 px）。
  - *瀏覽器，DOM 幾何*（`check_radar_browser.py`；合成圖樣 PNG 經真實 endpoint；地圖以 `L.Map.addInitHook` 取得，未改 app）：15 個參考點（四角、四邊中點、中心、臺北、臺中、恆春、花蓮、澎湖馬公、金門）的像素，其畫出位置（該列所屬條帶的 img `getBoundingClientRect`）對地圖對該像素經緯度的投影（`project` − `getPixelOrigin` → `layerPointToContainerPoint`，不取整）：**zoom 7 最大 0.0118 km、zoom 10 最大 0.0048 km**；對 Leaflet 取整的 `latLngToContainerPoint`：z7 最大 0.617 km（整數 px 取整，1 px ≈ 1.1 km）、z10 最大 0.091 km；375 px（zoom 6）最大 0.019 km。以 `+` 動畫縮放與拖曳後圖層重新放置（≤ 0.003 km）。
  - *瀏覽器，實際渲染像素*：同一頁面在雷達 pane 顯示／隱藏下各拍一張（兩張皆隱藏標記），每個方塊變化像素的重心對其中心的投影：**zoom 10 七個完整方塊最大 0.067 km（中位 0.03）**；**zoom 7 三十二個完整方塊最大 0.72 km（中位 0.35；1 px ≈ 1.1 km，§5.3 所稱粗檢）**；四角／邊上方塊被影像邊界裁切，改由 DOM 幾何量測。
  - *鑑別*：檢查在同一地圖放一個同影像的一般 `L.imageOverlay` 並量測 → **3.831 km**（> 1 km，屬 FAIL 型）。
  - *資料事實（不是 oracle；`--coastline`）*：CWA O-A0058-003 變體的黑線像素（海岸線、縣界、1° 格線）對 vendored 內政部縣界多邊形 3,999 個頂點，在等經緯度 118–124／20.5–26.5 假設下：中位距離 **0.075 km**、p90 0.106 km；±2.5 km 試驗平移（步長 0.1）的最佳者為 **（東 0.0、北 0.1）km**；平移 1 km 時中位升至 0.25～0.28 km。產品確為該格網（未發現無法達成 1 km 的系統性偏移，不需 route DA）。視覺：`coastline-003-1280-*.png`（-003 以 0.55 不透明度疊在底圖上）、`real-006-*.png`（真實 -006）。
  - Evidence：`alignment.json`（全部量測）、`1280-z7-radar-{on,hidden}.png`、`1280-alignment-z10-{taipei,penghu}.png`。
- **V-9 瀏覽器行為（AC-V2-18、09(c)、16；`python tests/check_radar_browser.py --real-image … --coastline …` → 52/52 PASS**，evidence `home_work_01/doc/acceptance/screenshots/v2/issue-40/`）：
  - 預設：`Radar: Off`、`aria-pressed=false`、無 `/api/radar/latest` 請求、無圖層；按鈕 ≥ 44×44（1280 與 375）。
  - Enter 顯示：圖層 24 條、blob URL、`Radar Time`＝回應 `X-Radar-Time`（`2026-09-26 14:40 +08:00`）、content type image/png；`Radar Time` 列與 `Observation Time`／`Fetched Time` 為不同元素且三者皆可見；Space 隱藏（圖層移除、列隱藏）。
  - 圖層順序（computed z-index）：backdrop 300 < radar 350 < overlay 400 < marker 600；雷達 pane 與影像 `pointer-events: none`；22 條可互動縣界。陸地上的雷達像素處 `elementFromPoint` 命中縣界（非雷達），hover 顯示縣名 tooltip、點擊選取該縣；站點標記在上層（命中、opacity 1），點擊選取測站；地圖可拖曳（zoom 8）與縮放（動畫 `+`）。
  - RAD-6 透明：雷達改變的地圖像素全部屬於圖樣方塊（13 個 blob、0 個無主、970／360,640 像素）。
  - 重新取得：再次開啟 → 請求 +1、新雷達時間；顯示中按 Refresh → 雷達與觀測各 +1；閒置 12 s → 無請求（不輪詢）；較舊雷達時間不取代較新（"Already the latest radar image."）。
  - Forecast mode：無 Radar 控制、無圖層、地圖卡文字無 "Radar"；回 Now 後雷達與時間恢復。
  - 失敗（首次取得）：`key_not_configured`、`upstream_unreachable`、`upstream_error`（403）、`invalid_response`、平台 HTML 502（`unexpected_response`）→ radar unavailable、無圖層、Radar Time「—」、類別原因，五種文字互異；觀測狀態、時間、數目與標記不變。伺服器停滯 → unavailable（`upstream_unreachable`）< 30 s。成功後 Refresh 遇 500 → stale：同一 blob、同一 Radar Time、「Radar Stale … (HTTP 500) — upstream_error」；觀測仍 success。超過頁面上限的請求 → 保留 stale（no_response）< 30 s；下一次成功清除。觀測失敗（Refresh → 觀測 Stale）→ 雷達 success 且為新影像；觀測首次載入即 Unavailable → 雷達可顯示。預報快照 503（DB 不存在）→ 預報區段顯示其錯誤、雷達可用（AC-V2-09(a) 的雷達部分）。
  - 375：預設／開啟（鍵盤）／stale／unavailable，`scrollWidth` 皆 ≤ 375。
  - AC-V2-16：全部瀏覽器請求皆為 loopback 或同源 `blob:`；雷達影像來自 `/api/radar/latest`；外部請求 0。H-1：頁面文字、請求 URL、伺服器 log（root DEBUG）無哨兵金鑰、上游主機、上游本文或平台標記。Console：無例外、NaN、Invalid LatLng。
- **V-10 回歸（#36～#39 的檢查未修改，對 subject `fedffdd` 執行）**：#37 `check_refresh_browser.py` **97/97**；#38 `check_county_browser.py` **72/72**；#39 `check_fence_browser.py` **113/113**（含 AC-V2-13 圍欄／下限／上限／金門・連江到達、AC-V2-14、AC-V2-15 初始化守衛——CRS 未改，此處只是回歸）；V1 `check_series_error_visible.py` PASS；#36 `check_modes_browser.py` 3 次：**37/37** 一次、36/37 兩次——兩次失敗項皆為「B-375／B-desktop AC-V2-09(a) Refresh works while the forecast snapshot is unavailable」，即 #38 R2 audit 記為 N-1 的既有時序偽陽性（該 audit 6 次中 3 次同項失敗；#39 亦同）。結果複製為 `regression-check-issue-{36,37,38,39}-*.json`（#36 為 37/37 那次）。
- **V-11 自我驗證：mutation checks**（scratchpad `mut40.py`：改一行、跑雷達與相關前端測試檔、以 sha256 確認還原；**非正式 audit**）：M1 一條 → 7 失敗；M2 兩條 → 7；M3 無逐條位移 → 1；M4 雷達 pane 接收指標 → 1；M5 雷達在縣界之上 → 1；M6 失敗丟棄影像 → 1；M7 頁面載入即取得 → 1；M8 預設開啟 → 1；M9 金鑰送往影像主機 → 1；M10 log 影像 URL → 1；M11 不檢查範圍 → 2；M12 任意影像主機 → 2；M13 重用 600 s → 收集階段錯誤；M14 重用失敗 → 1；M15 log metadata URL → 19；M16 較舊取代較新 → 1；M17 不檢查尺寸 → 7。每個 mutation 皆被抓到。
- **V-12 H-2／不變產物**：`git diff --stat cd5da10` 對 `app.py`、`weather_query.py`、`ingestion/`、`data.db`、`observation.py`、`representative.py`、`api/`、`smoke.py`、`vercel.json`、`requirements.txt`、`static/data/`、`static/vendor/`、`CONTEXT.md`、`.github/`、`doc/requirement/` 與 #36～#39 的測試／檢查檔 → 空。
- **未執行／限制**：(a) 未做 Vercel preview（#41；部署環境的 fileapi 可達性、時限與大小未驗證）；(b) 只測 Chromium headless、合成滑鼠事件，無實體觸控／pinch、無螢幕閱讀器；(c) zoom 7 的渲染像素量測受約 1.1 km/px 量化（§5.3 以 zoom 7 為粗檢，判定以 zoom 10 與 DOM 幾何為主）；(d) 真實雷達影像（-006／-003）只下載一次存於 scratchpad、未提交，`--real-image`／`--coastline` 需另外提供；(e) 瀏覽器檢查不在 CI（需 Chrome），由 Reviewer 本機重現。

### A-3 金鑰使用紀錄

| # | 時間（+08:00） | 目的 | 動作 | 帶金鑰的上游 GET | 輸出 |
| --- | --- | --- | --- | --- | --- |
| 1 | 2026-09-26 14:50:57 | (i) 擷取樣本／選變體 | scratchpad `capture_meta.py`：讀 `.env`（不印出），O-A0058-005、O-A0058-003 metadata 各一次唯讀 GET（`Authorization` 標頭）；寫檔前比對金鑰字面 | 2 | 只印 status、bytes、「key literal in body: False」與結構欄位 |
| 2 | 2026-09-26 14:51:07 | (i) 擷取樣本 | 同上，O-A0058-006 metadata 一次；`scan_text(key=...)` 無發現後寫入 fixture | 1 | 同上 |
| 3 | 2026-09-26 15:20:49 | (ii) 本機定向驗證 | scratchpad `live_local_check.py`：`python server.py`（子行程環境先移除 `CWA_API_KEY`，金鑰只能來自 `.env`），`/api/radar/latest` 兩次（第二次為重用）、`/api/health` 一次 | 1（第二次重用，未呼叫上游） | 只印非機密摘要與布林檢查 |

另：公開影像（不需金鑰、不帶任何標頭）自 CWA 公開 S3 下載 -006、-003 各一次，只存於 scratchpad（視覺與資料事實檢查用），未提交。無輪詢、無壓測；未觸及 Vercel（RB-3）；未遇到需帳號或付費的來源（RB-3／RB-4 未觸發）。CI 與自動化測試不依賴金鑰或網路。

## High-risk 核對材料（decision A-1；供 R1 明記 H-1／H-3 核對段）

- **H-1 憑證**：金鑰只由 `radar.RadarService.latest()` 每次請求自 `env.get("CWA_API_KEY")` 讀取，不存於物件（`test_key_is_read_at_request_time_and_never_stored`）；本機來源只有 `.env`（沿用 `observation.load_local_env`，未改）；部署來源為 Vercel 專案環境變數（本票未觸及）。金鑰**只送往** metadata 請求的 `Authorization` 標頭，影像請求 `headers == {}`（`test_key_goes_only_to_the_metadata_request_as_a_header`）。回應、標頭、log（root DEBUG）、stdout／stderr 對 18 個失敗案例與成功路徑皆無哨兵金鑰、兩個上游主機名、上游本文標記、`Authorization`、`ProductURL`（`test_failure_class_through_the_api`、`test_success_is_the_png_…`、`test_radar_with_network_blocked_…`）；瀏覽器檢查對頁面文字、請求 URL 與伺服器 DEBUG log 同樣斷言；A-3 實測終端與回應標頭無金鑰字面／格式。樣本與新程式在 `test_secrets.py` 與 `tools/credential_scan.py` 範圍內。可核對點：`_FAILURES` 固定文字；`except requests.RequestException: raise … from None`；log 只含 reason／status／雷達時間；`urllib3` logger ERROR；`IMAGE_HOSTS` 白名單。
- **H-3 語義與標示**：雷達時間逐字標為 `Radar Time`、自成一列、與 `Observation Time`／`Fetched Time` 不同元素不同標籤（靜態守衛＋瀏覽器檢查）；雷達時間取自與影像同一回應的 `X-Radar-Time`（metadata `DateTime` 原樣，只做 `formatObsTime` 版面重排）；雷達不計算任何值、不改變任何觀測或預報數值；CWA 授權標示（README 兩處＋應用內 Now notes）：「交通部中央氣象署 雷達整合回波圖-臺灣(鄰近地區)_透明底圖（O-A0058-006）」、政府資料開放授權條款；頁面無 `real-time`／`live`（瀏覽器檢查）。
- **H-2（附帶）**：`app.py`、`weather_query.py`、`data.db`、Forecast section、masthead、`Select Region` 等未改（V-8）；#36 回歸（下方 dashboard、概念詞）。
- **Diversity**：Executor 與 Primary Reviewer 同為 `claude-opus-5-5` 時，audit record 記 `diversity_lost`（Bindings §5）。

## Audit status

- **Required**：Formal mandatory independent audit（治理 §4.1；Bindings §5）。本 worklog 的測試、瀏覽器檢查、幾何重算與 mutation checks 皆為 Executor self-verification，**不是**正式 audit。
- **Records**：尚無。待 Orchestrator 派 R1（`gov-primary-reviewer`）。

## Remaining work

1. **正式 audit**：R1（Orchestrator 派工）；結案條件依治理 §3.8。
2. **Concerns（交有權角色判斷；Executor 未自行裁決）**：
   - (a) **§5.3 px 換算數字**（Decisions 5）：與 Web Mercator 計算不一致（約差 2.5 倍）；本票以 km 判定、不受影響。若需修正 Spec 文字，authority：Design Authority（非阻擋）。
   - (b) **375 px 地圖位置下移**（Decisions 9）：新控制使 Refresh 與 County 分兩列，375 首屏地圖少約 54 px（Radar 開啟時更多）。契約條件（RSP-2／3／5／7、MAP-4）回歸 PASS；可用性判斷交 R1。
   - (c) **metadata 與影像的週期不一致**（R-V2-RAD-4 已知限制）：兩個 CWA 檔案各自每 10 分鐘覆寫，伺服器緊接著讀，但無法保證同一週期；README 已記述。無可在契約內消除的做法。
   - (d) **Vercel 實測**（時限、fileapi 在部署環境的可達性、回應大小）屬 #41 的 preview 驗證（AC-V2-17(c)、22）；本機實測 0.5 s、~76 KB。
   - (e) 使用 vendored Leaflet 1.9.4 的 `map._latLngToNewLayerPoint`（縮放動畫，同 Leaflet 自家 ImageOverlay 的作法）；版本已 pin。
3. **後續票**：#41（preview 驗證含雷達 `/api/`（AC-V2-17(c)）、README 其餘項目、V2 驗收文件；AC-V2-18／19 的證據引用本票）。
