# Audit record — Issue #20，cycle 1，R2

| 欄位 | 內容 |
| --- | --- |
| Work Contract | GitHub Issue #20（`yotsubamomo/aiot-classwork`）「Dashboard MVM：Flask /api/ 與靜態頁面在本機提供相同的 Region 查詢行為」，Scope class MVM。所屬 Spec：`home_work_01/doc/spec/SPEC.md` v1.1（EFFECTIVE）；Outcome Contract：`home_work_01/doc/governance/outcome-contract.md`（ACCEPTED 2026-09-23）。裁決：DR-1、DR-2、DR-7、DR-8、DR-9、DR-17；高風險 H-1、H-2、A-1。 |
| 受審 subject | branch `home_work_01-hw10-implementation`，commit `0f5f00e3d0667eaad74f46d2a744a2abebd32ec5`，是 R1 subject `72ff874` 的 targeted correction。correction 範圍為 `72ff874..0f5f00e`，共 7 個檔案，全部在 `home_work_01/` 內。 |
| Audit 種類 | **R2**（scoped closure review，治理 §4.4），**cycle 1**。R1 record：`home_work_01/doc/governance/audit/issue-20-c1-r1.md`，結論 `BLOCKING (F-1)` |
| 角色 | `primary_reviewer`（definition `gov-primary-reviewer`；Bindings §3.1 mapping 為 `claude-opus-5-5`／`xhigh`） |
| Binding 證據 | 由派工者（Orchestrator）依 Bindings §3.4 核對，記在 run record `home_work_01/doc/governance/run/run-20260924-hw01-formal.md`。 |
| Independence（治理 §2.3） | R2 延續 Reviewer 自己的 R1 context（治理 §2.1、§2.3(1) 允許），沒有繼承 Executor 的 context。依 §4.4 的要求，**從磁碟重新讀取**修正後的檔案與 `git diff 72ff874..0f5f00e`；worklog §5 的敘述一律當作待驗證的主張。測試、瀏覽器渲染與 mutation 都由 Reviewer 自己執行。本紀錄由 Reviewer 用自己的 Write 工具寫入。 |
| 日期 | 2026-09-24 |

## 1. 範圍與方法

依治理 §4.4，本次 R2 只做三件事：(1) 驗證 F-1 是否真正解決；(2) 驗證修正沒有引入回歸；(3) 檢查修正直接產生或暴露的 blocking defect。Executor 這次一併清掉的 #20-owned Low findings（F-2、F-5、F-7、F-8、F-9），作為 (2) 的一部分核對。本次不做第二次全面審查。

- **確認 subject**：`git rev-parse HEAD` = `0f5f00e3…`。`git status --short` 只列出 Orchestrator 的 run record（record-only path），以及 Reviewer 尚未 commit 的 R1 record。correction 沒有任何路徑在 `home_work_01/` 外面。commit message 沒有 Claude 標記。
- **沒有變動的面**：`git diff 72ff874..0f5f00e` 不包含 `server.py`、`api/`、`vercel.json`、`requirements.txt`、`static/index.html`、`static/styles.css`、`weather_query.py`、`app.py`。`data.db` 的 blob 維持 `687586991ce3…`。
- **環境**：`git archive 0f5f00e home_work_01` 匯出到 scratchpad，匯出的樹沒有 `.env`。使用單元 `.venv`（Python 3.12.14、flask 3.1.2），並沿用 R1 的 `sitecustomize` 網路封鎖。瀏覽器為 Chrome 153 headless。

## 2. F-1 的 closure 驗證

| 檢查 | 結果 | 證據 |
| --- | --- | --- |
| 修正內容 | **正確** | `static/app.js:97-98`：`loadRegion` 在 `fetchJson(".../series")` **之前**執行 `els.panel.hidden = false` 並設定小標題。成功分支（`:109-112`）不再重複設定，`.catch`（`:114-116`）也不再需要自己解除隱藏。`#chart-status` 仍位在 `#region-panel` 內（`index.html` 沒有變動），但現在這個面板在任何結果之前就已經可見。R1 附帶提到的「切換失敗時小標題停留在前一個 Region」也一併修正。 |
| 503（首次載入） | **看得到訊息** | Reviewer 的 harness 只包裝受審的 `create_app`，health 與 regions 照常運作，只對 `/series` 注入故障。渲染後的 DOM：`<section id="region-panel" class="panel">`（沒有 `hidden`），`#chart-status` 沒有 `hidden`，文字為 `injected 503`，小標題為 `Temperature Forecast – 北部地區`。截圖中有藍色 info banner，顯示在小標題下方。 |
| 404（首次載入） | **看得到訊息** | 同樣的方式，面板可見，訊息為「That Region is not available in this snapshot.」。 |
| 網路失敗（首次載入） | **看得到訊息** | Reviewer 另外加了一種故障：`/series` 回 307，轉址到 `127.0.0.1:9` 這個關閉的 port，讓 `fetch` 以網路錯誤 reject。面板可見，訊息為「Cannot load this Region right now. Please try again.」（截圖已確認）。 |
| HTML 500（例如平台錯誤頁） | **看得到訊息** | 另外注入非 JSON 的 500 回應。面板可見，訊息為「The forecast data is currently unavailable.」。 |
| Executor 的 reproducible guard `tests/check_series_error_visible.py` | **有效** | 在修正後的 subject 上執行 → 503 與 404 都印出 visible message，最後為 `PASS`，**exit 0**。在 scratch 副本中把 `static/app.js` 換回 `72ff874` 的版本後，同一個 guard 在 `[503] #region-panel is still hidden — the message is swallowed` 失敗，**exit 1**。guard 包裝的是**未修改**的 `server.create_app`（`:43-53`）。它的檔名不符合 pytest 的收集規則（`pytest.ini` 使用預設 `test_*.py`），所以不會進入離線測試套件，這與 README 和 docstring 的說明一致。 |
| 截圖 `ac10_dashboard_error_series_503.png` | **是真實畫面** | 與 Reviewer 在 `0f5f00e` 上獨立渲染的 503 畫面**大小完全相同**（27353 bytes），內容也相同：標題、`Select Region`、取得時間、可見的面板與訊息 banner。截圖中沒有任何秘密。 |
| 正常路徑（200） | **沒有受影響** | 預設 Region 與 `?region=中部地區` 兩種情境，都是 2 條 polyline、7 列表格，小標題正確，`#chart-status` 為 hidden。Reviewer 在 R1（`72ff874`）與 R2（`0f5f00e`）對預設畫面的渲染結果 **byte-identical**（PNG sha256 前 16 碼 `e25675a42715577e`），`#region-panel` 的 DOM 也完全相同。 |

**結論：F-1 已解決。** R-DS-6 對 series 的 503、404、網路失敗（以及非 JSON 的 5xx）在首次載入時都會顯示明確訊息，不會再出現沒有提示的頁面。

## 3. 回歸驗證

- **全套離線 pytest**：**143 passed**，在網路封鎖、沒有 `.env` 的匯出樹中執行。逐檔：test_app 9、test_dashboard 23、test_derive 19、test_fetch 13、test_persist 5、test_pipeline 19、test_secrets 4、test_static_checks 22、test_weather_query 29。數量變化：134，減去被取代的舊 guard 1 個，加上 F-4 guard 參數化 6 個、benign 參數化 3 個、F-5 的 1 個，等於 143，與實際收集數一致。沒有任何測試被刪除或弱化；被移除的舊 guard 由更強的版本取代（見 §4 F-2）。
- **錯誤狀態**：資料庫缺失時，頁面錯誤狀態的渲染與 R1 **byte-identical**（`8f23b8172a0d5bb3`）。`bootstrap` 與 `showPageError` 都沒有變動，health 與 regions 的錯誤處理不受影響。
- **AC-04(b)**：`app.js` 仍然只有 `fetchJson` 會發出請求，目標仍全部以 `/api/` 開頭。新增的兩行只設定 DOM 屬性與 `textContent`，沒有 `innerHTML`，也沒有新的請求。`test_frontend_*` 三個測試通過。
- **R1 已確認的其他結果**：`server.py`、`index.html`、`vercel.json` 等 runtime 檔案與 `data.db` 都沒有變動（§1），因此 R1 對 AC-02、AC-03、AC-16、AC-24、INV-1、INV-2、R-DS-8 的判定仍然有效。INV-2 測試仍在套件內並且通過。

## 4. Executor 一併清掉的 Low findings（作為回歸的一部分核對）

| R1 finding | 狀態 | 證據 |
| --- | --- | --- |
| F-2（F-4 guard 沒有保護到修正機制） | **已解決** | `test_static_checks.py` 新增 `test_import_check_catches_http_client_from_source`（6 種寫法）與 `test_import_check_allows_benign_imports_from_source`（3 種寫法）。兩者都把片段寫入暫存檔，再經**真正的** `_import_targets` 解析。Reviewer 的 mutant：把 `_import_targets` 的 `module.name` 記錄還原 → **3 failed**；從 dotted set 拿掉 `urllib.request` → **4 failed**；把任何 `urllib` 都判為違規的過寬檢查 → **2 failed**（被 benign 測試抓到）；在 `server.py` 加入 `from urllib import request` → **1 failed**。 |
| F-5（可見文字的回歸保護） | **已解決** | `test_dashboard.py` 的 `test_index_page_has_visible_teacher_text` 斷言頁面含有 `>Taiwan Weather Forecast</h1>`、`>Select Region</label>`，以及 `>Date</th>`、`>MinT</th>`、`>MaxT</th>`。Reviewer 的 mutant：只改 `<h1>`、改 `Select Region` 標籤、改 `MinT` 表頭、改 `Date` 表頭，**四個全部被抓到**（各 1 failed）。 |
| F-7（README 過時文字） | **已解決** | `README.md:54-57` 的 Requirements 已列出 `flask`；`:195-196` 改為「served … by the Flask + static dashboard below (its public Vercel deployment is a later ticket)」；`:289-299` 補充了 Flask test client、INV-2、強化後的靜態檢查，以及需要真實 Chrome、另外執行的瀏覽器檢查。內容與實際的測試與檔案相符。`:196` 是一行較長的 Markdown，只影響原始檔的排版，不影響呈現。 |
| F-8（未使用的常數） | **已解決** | `git grep _BACKEND 0f5f00e -- home_work_01` 只命中 worklog 中描述這次移除的那一行。 |
| F-9（worklog 測試數量） | **已解決** | `worklog/issue-20.md` §3 已改為「BASE `592c9ed` 為 107；… 9 增至 14；107 + 22 + 5 = 134」，並附上更正註記；§5 記載修正後為 143，逐檔數字與 Reviewer 實際收集的結果一致。 |

仍由各自 owner 追蹤、不屬於本 cycle 的項目：**F-3**（非 SQLite 檔回 HTML 500，owner #25）；**F-4**（AC-10 的自動化證據只涵蓋部分情境，owner #25）；**F-6**（Flask 的 dotenv 自動載入，owner #21／#25）。O-1 不需要處理。

## 5. 高風險類別核對（A-1：只重述受修正影響的部分）

### H-1 憑證與機密

- **核對內容**：correction 新增或修改的檔案（`static/app.js`、`tests/check_series_error_visible.py`、`tests/test_dashboard.py`、`tests/test_static_checks.py`、`README.md`、worklog、新截圖）。以字面金鑰（從被忽略的 `.env` 在程序內取得，只輸出次數）與 CWA 金鑰格式，掃描 `72ff874..0f5f00e` diff、`0f5f00e` 的 commit message，以及 `0f5f00e` 樹內 450 個追蹤檔案。grep `opendata`、`CWA_API_KEY`、`environ`、`getenv`、`dotenv`、`Authorization`。
- **結果**：字面金鑰 0 筆，金鑰格式 0 筆，沒有追蹤任何 `.env`。grep 命中的只有 R1 已知的兩行 docstring，以及 `check_series_error_visible.py:57` 的 `os.environ.get("CHROME")`：這讀的是瀏覽器路徑，不是秘密，而且只屬於開發用的檢查工具，不在 Dashboard runtime 中。新截圖只有公開資料、取得時間與注入的測試訊息。**H-1 沒有 blocking**，R1 的結論不變。F-6 仍在追蹤。

### H-2 老師指定的介面或資料格式

- **核對內容**：`index.html` 沒有變動。修正後的頁面在正常、503、404、網路失敗各情境中，`Taiwan Weather Forecast`、`Select Region`、`Date`／`MinT`／`MaxT`、圖例 `MaxT`／`MinT` 與 Region 名稱都逐字出現（DOM 與截圖）。小標題維持 `Temperature Forecast – <Region>`。`data.db` 的 blob 與 DDL 沒有變動。F-5 新增的斷言現在能以自動化方式保護這些字樣。
- **結果**：全部符合，**H-2 沒有 blocking**，而且回歸保護比 R1 時更強。

## 6. 修正直接產生或暴露的缺陷

沒有 blocking。以下是 non-blocking 的新 findings，依治理 §4.4 不延長本 cycle：

- **N-1（Low，non-blocking）**：修正後，小標題在 `fetch` **之前**就改成新的 Region，但圖與表要等成功回應後才會重畫（`app.js:98`、`:111-112`）。因此在網路較慢時切換 Region，會有一小段時間小標題顯示新的 Region，圖與表仍是前一個 Region 的值。這是從程式碼推得的結論：headless 的 virtual time 無法擷取這段中間狀態。最終狀態正確；失敗時 `showChartStatus` 會清空圖與表，所以不會殘留。R-EN-1(5) 的 loading 狀態屬於 ENHANCED，可以一併處理，例如在發出請求時清空或標示載入中。Owner：**#24**（UI／UX 的 loading 狀態），#20 也可以選擇處理。
- **N-2（Low，non-blocking）**：`worklog/issue-20.md` §3 對初次 subject 的敘述，仍然引用已被取代的測試名稱 `test_import_check_catches_from_urllib_import_request`。§5 已記載新的測試與取代的原因，因此不影響可追溯性。Owner：#20（可選）。
- **觀察**：Executor 的 guard 只涵蓋 503 與 404，網路失敗的情況由 Reviewer 以轉址故障另外驗證（§2）。

## 7. 需要其他 authority 的事項

無。F-1 已在契約內解決；N-1 與 N-2 都是 non-blocking，已記錄 owner。

## 8. 結論

- F-1 已解決：首次載入時，series 的 503、404、網路失敗與非 JSON 5xx 都會在可見的面板中顯示明確訊息。Reviewer 在自己的瀏覽器渲染中確認了這一點，Executor 的 guard 也確實能抓到回歸：修正前 exit 1，修正後 exit 0。
- 沒有回歸：143 個離線測試全部通過；正常路徑與資料庫缺失路徑的渲染與 R1 byte-identical；runtime 的其他檔案與 `data.db` 都沒有變動。
- F-2、F-5、F-7、F-8、F-9 都已解決，並以 mutation 或內容比對驗證。
- H-1 與 H-2 維持沒有 blocking。

VERDICT: CLOSURE
