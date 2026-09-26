# Worklog — WI-UI-THEME-1：頁面 light／dark 切換

- **Work item**：`WI-UI-THEME-1`（**Lightweight**；Bindings §4「已結案工作之後的單點修正，作為新的 work item」）。無 Delta Spec、無 Formal run、無 Ticket。
- **上位契約（不變）**：`doc/governance/outcome-contract-v2.md`、`doc/spec/SPEC-V2.md`（R-V2-MODE-2、R-V2-RSP-3／4、AC-V2-01）、DA decisions P-1／P-13（`decision-20260924-taiwan-map-rework.md`）；前一個 work item `WI-UI-POLISH-1`（`20260926-ui-polish.md`，已合併 `9743024`）。
- **Branch**：`home_work_01-theme-toggle`（SA-1），parent `main` `9743024`。PR 依 SA-2；**不合併**（RB-1 未授權於本 WI）、**不提交**（RB-2）。
- **Binding（Bindings §3.3 direct execution，§3.4）**：Executor = 主 session `de316248-08b6-4df2-b78b-d273bf392565`，transcript 觀察到的 `message.model`／`effort` = `claude-opus-5-5`／`high`，符合 `executor` mapping（b2 override）；未派 subagent。
- **Audit**：Lightweight，**完成且依 policy 未要求 independent audit**（未觸及 H-1：不處理憑證，`theme.js` 不發任何請求；未觸及 H-2：沒有變更任何老師指定或既有釘住的字串／介面，只新增一個按鈕與其標籤）。本紀錄不是 audit PASS。

## Contract reference（Lightweight Outcome Contract，Bindings §2.3）

acceptor 2026-09-26 於本 session 的直接指示（逐字）：

> 好，那我加個需求，我們在最上面或某個地方(你覺的最好的)加個 dark/light 的切換就好 ，這樣就不改了。

此指示是 acceptor 在先前「Do not start another UI work item」之後、自己明確提出的新需求，構成本 WI 的授權；「這樣就不改了」＝本 WI 之外不再有 UI 變更。位置由 acceptor 明確委託 Executor 決定（「你覺的最好的」）。

## 決定（Executor，在委託範圍內）

| # | 決定 | 理由 |
| --- | --- | --- |
| D-1 | **位置**：Taiwan Map 卡標題列的最右端（桌機即頁面主內容區右上角）；DOM 在 mode switch 與 caption 之後。 | 放在 masthead（DOM 在地圖之前）會讓切換鈕成為第一個 Tab stop，改變 V2 已驗證的鍵盤順序（`check_modes_browser.py`「mode switch … first Tab stop」儀器；AC-V2-01 本身只要求「鍵盤可切」）。選擇不動任何既有驗證語義的位置。 |
| D-2 | **行為**：預設跟隨系統（無儲存值時與先前完全相同）；按下在 dark／light 間切換；選擇存在本瀏覽器 localStorage（key `hw01-theme`，值只允許 `dark`／`light`）；storage 不可用時仍可切換、只是不記住。 | 使用者只要求切換；保留「跟隨系統」為預設，不改變既有使用者的初始畫面。 |
| D-3 | **控制形式**：一個真正的 `<button>`，可見文字 **Dark mode**、`aria-pressed` 表示是否為深色；月亮 SVG icon（inline、`aria-hidden`）；≥ 44×44；≤ 560 px 只顯示 icon（文字保留為 accessible name），與 caption 同列。 | 單一 toggle 的標準 a11y 模式；避免與旁邊的 Now／Forecast segmented control 視覺上混淆。 |
| D-4 | **不閃爍**：新增 `static/theme.js`，在 `<head>`、stylesheet 之前同步載入，於首次繪製前套用已存的 `data-theme`；按鈕的接線也在同檔（DOMContentLoaded）。`static/app.js` **零變更**。 | 放在 body 尾端的 app.js 會造成先以系統主題繪製再跳轉的閃爍。 |
| D-5 | **Token**：新增 `:root[data-theme="dark"]` 區塊，宣告與既有 `@media (prefers-color-scheme: dark)` 區塊**完全相同**（測試釘住兩者一致）；`data-theme="light"` 原本就會關閉系統深色區塊。地圖卡的 hero token 不受影響（P-1：地圖卡兩種主題都是深色）。 | 純 CSS 無 build step，只能重複宣告；以測試防止兩份漂移。 |

## 實作

- `static/theme.js`（新檔）：套用已存主題、接線 `#theme-toggle`、同步 `aria-pressed`（系統設定在頁面開啟中改變時亦同步）。無 `fetch`／XHR／外部 URL／cookie。
- `static/index.html`：`<head>` 加 `<script src="/static/theme.js"></script>`（在 stylesheet 之前）；地圖卡標題列加 `#theme-toggle` 按鈕。其他標記與所有既有字串未改。
- `static/styles.css`：`:root[data-theme="dark"]` token 區塊；`.theme-toggle` 樣式（地圖卡 token、44×44、focus ring、pressed 狀態）；≤ 560 px 只顯示 icon、`.caption--map` 與按鈕同列（`flex: 1 1 calc(100% - 60px)`）；reduced-motion 下無過渡。
- `README.md`：在「map area is dark in both … colour schemes」後補一句 Dark mode 按鈕的說明。
- 測試：新增 `tests/test_theme_frontend.py`（5 tests）；`tests/test_static_checks.py` 的 `_FIRST_PARTY_FRONTEND` 加入 `theme.js`（同源請求檢查涵蓋新檔，只加強）；`tests/test_secrets.py` 掃描清單加入 `theme.js` 與新測試檔（只加強）；`tests/check_ui_polish_browser.py` 新增 theme scenario（1440／375 × 系統淺／深，共 28 項）。

## Verification

全部在最終程式上執行（`.venv` Python 3.12.14；headless Chrome；browser script 皆為 sentinel key＋committed samples、零外部請求）。Logs：`doc/acceptance/screenshots/ui-theme/regression/`。

| 檢查 | 結果 | 證據 |
| --- | --- | --- |
| pytest（CI suite） | **625 passed**（618＋5 theme tests＋secret scan 新增 2 檔） | `regression/pytest.log` |
| `check_ui_polish_browser.py`（含新 theme scenario） | **111/111**（原 83＋28 theme：1440／375 × 系統淺／深——無儲存時跟隨系統且 `aria-pressed` 正確；可見「Dark mode」、≥ 44×44、首屏可見、無橫捲、mode switch 仍首屏可見；鍵盤第一個 Tab stop 仍為 `#mode-now`、第三個為 `#theme-toggle`；Enter 切換 page token／背景與 `aria-pressed`；地圖卡背景兩主題相同；reload 後記住選擇；再按切回） | `regression/ui-polish.log`、`after/` |
| fence／modes／radar／county／refresh（V2 browser scripts） | **129/129、37/37、47/47、72/72、97/97**（含 modes「AC-V2-01 … first Tab stop」、fence 375 bottom sheet、44×44、無橫捲） | `regression/<name>.log` 與同名資料夾 |
| 非範圍檔案 | `static/app.js`、`server.py`、`api/`、`observation.py`、`radar.py`、`representative.py`、`weather_query.py`、`app.py`、`ingestion/`、`data.db`、`static/data/`、`static/vendor/` 皆未改；無 `.env`、diff 無金鑰字串 | commit diff |

截圖：`after/1440-now-first-screen.png`（按鈕位置）、`after/375-now-first-screen.png`、`after/theme-1440-syslight-flipped-*.png`（淺色系統下切成深色）、`after/theme-1440-sysdark-flipped-*.png`（深色系統下切成淺色）、`after/theme-375-*`。

## Limitations

- 本 WI 只做切換；未新增第三種「跟隨系統」按鈕狀態——一旦按過，該瀏覽器就記住選擇（清除網站資料即回到跟隨系統）。
- 未在 production 驗證（本 WI 未合併；RB-1 保留給 acceptor）。
