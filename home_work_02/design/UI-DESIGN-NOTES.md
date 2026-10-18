# HW2 Dashboard — UI Design Notes（Wireframe v0.2，2026-10-18）

> v0.2：依 acceptor 的 Wireframe Review 七項 UI 決策（§8）做最小修正：All-in 只顯示固定 k = 18；手機導覽改為可展開選單（含鍵盤、焦點與 `aria-expanded`）。其餘決策確認既有做法。

- **目的**：依已接受的 Brief（`doc/brief/BRIEF.md` @ `dff7c55c`）與 Spec rev 3（`doc/spec/SPEC.md`，issue #59）設計 dashboard 的高保真靜態 wireframe，供 Wireframe Review 與後續 UI 實作參考。**不改變** Brief／Spec 的功能與統計要求。
- **產物**：[`wireframe/index.html`](wireframe/index.html)、[`wireframe/wireframe.css`](wireframe/wireframe.css)、[`wireframe/wireframe.js`](wireframe/wireframe.js)、[`wireframe/mock-data.js`](wireframe/mock-data.js)；設計系統 [`design-system/hw2-king-county-dashboard/MASTER.md`](design-system/hw2-king-county-dashboard/MASTER.md)（由 `/ui-ux-pro-max` 產生並持久化）。
- **資料邊界**：全部數字由固定種子亂數產生（`mock-data.js`），頁面頂部與結果區都標示「示意資料／非實際模型結果」。沒有執行 Python 模型，沒有統計驗證，涵蓋率不代表真實結果。
- **離線**：不載入任何外部資源（無 CDN、無字型下載、無 fetch）；資料以 `.js` 全域變數載入，可在 `file://` 與斷網環境開啟。
- **視覺參考**：week06 DIC-02 頁面與 SRC-3 只作為「成果類型與呈現」的參考；本 wireframe 的配色、版面、文案與程式碼皆為新作，未複製任何無授權的程式、CSS 或文案。

## 1. 設計原則（`/ui-ux-pro-max` 設計系統）

| 項目 | 決定 | 依據 |
| --- | --- | --- |
| 風格 | **Minimalism & Swiss**：乾淨、網格、留白、高對比、無裝飾 | 設計系統建議（dashboards／professional tools）；acceptor 指定 professional／academic |
| 色彩 | 主色 navy `#1E40AF`、背景 `#F6F8FB`、表面白、文字 `#0F172A`、邊框 `#D9E2EF`；強調 amber `#B45309`（警告、區間外、mock 標示）；danger `#B91C1C`（invalid）；success `#166534`（winner） | 設計系統「Blue data + amber highlights」；amber 加深以達 4.5:1 文字對比 |
| 資料系列 | Forward `#1E40AF`、Backward `#0E7490`、RFE `#6D28D9`、Lasso 路徑 `#C2410C`；All-in `#334155` 虛線、Ridge `#64748B` 點線、Lasso 對照 `#A16207` 點線 | 四條路徑色相分離；參考線以線型區分，不只靠顏色 |
| 字型 | 系統字型堆疊：`Noto Sans TC`、`Microsoft JhengHei`、`PingFang TC`、`Segoe UI`、system-ui；數字 `font-variant-numeric: tabular-nums`；等寬用於識別字 | 設計系統建議 Fira 系列需下載，與離線要求衝突；zh-TW 以系統 CJK 字型最穩定 |
| 間距與圓角 | 4/8 px 節奏；卡片 8 px 圓角、1 px 邊框、極淡陰影 | 設計系統 density 7（標準） |
| 動效 | 只有 150–220 ms 的 hover／切換淡入；`prefers-reduced-motion` 全關 | 設計系統 motion 2（subtle）；Spec 不要求動畫 |
| 無障礙 | 跳到主要內容；全部控制 ≥ 44 px；可見 focus ring；`aria-pressed` 區段按鈕；預測結果 `aria-live`；警告以圖示＋文字、不只靠顏色；表單欄位都有 `<label>` 與 `aria-describedby` 警告 | Quick Reference §1、§2、§8 |

## 2. 版面

| 寬度 | 版面 |
| --- | --- |
| **Desktop ≥ 1181 px** | 內容最大 1440 px；B＋C 為「左 320 px 固定控制面板（sticky）＋右側 KPI 與圖」；KPI 5 欄；預測器「欄位 3 欄＋右側 360 px sticky 結果卡」；Test 區塊全寬、灰底＋左側深色邊；方法與限制 2 欄 |
| **Tablet 769–1024 px** | 控制面板移到內容上方（不 sticky）；KPI 3 欄；預測器欄位 2 欄、結果卡在下方；k 按鈕 9 欄；方法與限制 1 欄 |
| **Mobile ≤ 768 px** | 全部單欄；頂部導覽收進「選單」按鈕（`aria-expanded`／`aria-controls`，展開為直向錨點清單，Enter／Space 開關、Escape 關閉並回焦、點選錨點後關閉、Tab 離開時關閉）；KPI 2 欄（≤ 480 px 時 1 欄）；k 按鈕 6 欄；散佈圖改 4:3 |

## 3. 區塊對應 Spec

| Wireframe 區塊 | Spec 依據 | 要點 |
| --- | --- | --- |
| A 概覽 | Problem／Solution、§2 來源、資料事實 | 資料集、19／18、14–20 交集、三種標示的圖例 |
| B 模型選擇 | Dashboard 區塊 (1)；SR-06；SR-04／SR-10 | 四種路徑方法＋All-in（選 All-in 時 k 格子換成單一「k = 18 固定」狀態列，不顯示 1–17）；k 格子標 winner（綠點）與 invalid（紅斜紋）；「比較全部」切換；目前選取摘要（canonical subset、fold 一致數、標籤） |
| C 訓練 CV | 區塊 (2)(3)；BR-01；SR-05 | KPI 標「訓練 CV（USD）」，Adjusted R² 卡標 `fit`／log 尺度；指標 vs k 圖含四條路徑、三條參考線、winner 圓環、invalid 叉號、選取圓圈；指標下拉（RMSE／MAE／R²）；比較表含 metric-only 與講義對照列 |
| D 即時預測 | 區塊 (5)；Q31、Q32；SR-07 | 只列目前模型 canonical subset 的 source feature；日期、數值、下拉、整修「未整修」勾選、zipcode 下拉（含一個示意未見類別）；超出範圍與未見 zipcode 的欄位內警告＋結果卡彙總；結果卡標「模擬數值」、PI 以 log 尺度長條示意；invalid 候選時停用 |
| E Test 評估 | 區塊 (6)；BR-01；Q43；SR-03、SR-09、SR-12 | 獨立灰底區塊＋「Test 評估（USD）」標籤；展示模型名稱與 k、winner／整體 winner 標籤；非 winner 時顯示黃色提示；Test KPI；canvas 散佈圖（log-log、y=x、逐筆 PI 線段、涵蓋著色、滾輪縮放、拖曳平移、游標讀取、放大／縮小／重設按鈕、首次繪製時間顯示）；涵蓋率五卡與二項近似說明 |
| F 方法與限制 | 區塊 (9) | 方法、協定、PI 假設、限制與非因果；段落帶三種標示 |
| 選配 | 區塊 (4)(7)(8) | 三個 `<details>`：係數表（標 log 尺度）、Test 殘差表、全部結果表（含 invalid 列） |

## 4. 已完成的 Mock Interactions

- 方法切換、k 切換（All-in 時只顯示固定 k = 18）、「比較全部」疊圖＋比較表。
- 手機「選單」按鈕展開頁內錨點（鍵盤、焦點、`aria-expanded` 狀態）。
- KPI、圖、選取摘要、預測器欄位、Test 區塊同步更新；非 winner k 時 Test 區塊顯示該方法 winner 並提示。
- invalid 候選（示意：RFE k=17）：k 格子紅斜紋、KPI 顯示原因、預測器停用、圖上叉號、不可成為 winner。
- 預測器：輸入即時重算；超出 training 範圍警告（仍計算）；整修年「未整修」切換；未見 zipcode 警告。
- 散佈圖：4,287 筆逐筆 PI 線段；滾輪縮放（以游標為中心）、拖曳平移、按鈕縮放／重設、游標停留讀取單筆、首次繪製耗時顯示。
- 指標下拉切換圖的 y 軸。

## 5. 只能示意、尚未實作

- 所有數值（CV、test、係數、涵蓋率、執行時間）皆為模擬；真實數字來自 notebook 匯出的 `model_data`。
- 預測公式是示意線性組合，不是 OLS；PI 寬度是示意常數。
- 散佈圖的鍵盤替代（Spec 要求可觀察的檢視）：目前只有按鈕縮放／重設與游標讀取；鍵盤逐點瀏覽未做。
- 「比較全部」的 fold 標準差帶、Ridge／Lasso 的 alpha 曲線未呈現。
- 主題切換、網址參數深連結（HOW，不在需求內）。
- 真實 375 px 裝置與 Safari／Firefox 的檢查未做（本次在 Chromium 內建瀏覽器以 1024／1440 與 375 模擬寬度檢查）。

## 6. 本機預覽與離線測試（2026-10-18）

- 靜態掃描：html／css／js 內沒有 `http(s)://` 或 `url(`；`node --check` 兩個 JS 檔通過。
- 以本機 `http.server` 開啟（內建瀏覽器無法直接渲染 `file://`）：網路面板只有 4 個本機檔案請求，沒有對外請求；console 無錯誤。
- 區塊渲染：CV KPI 5、Test KPI 4、預測欄位依模型 k 變化、chart 4 條路徑、散佈圖 4,287 筆；首次繪製約 9–243 ms（取決於是否首次佈局）。
- 互動以 DOM 驗證：非 winner 提示、invalid 狀態、比較全部表（8 列）、未見 zipcode 與超出範圍警告、All-in 停用 17 個 k 都正確。
- 1440 px：雙欄＋sticky 控制面板正常；模擬 375 px：無水平捲動，k 按鈕與方法按鈕高度 44 px。

## 7. UI 問題（v0.1 提出）→ 見 §8 的 acceptor 決策

v0.1 提出七個待決 UI 問題；acceptor 於 2026-10-18 Wireframe Review 全部裁決，結果與落實記錄在 §8。

## 8. Acceptor 的 UI 決策（2026-10-18）與落實

| # | 決策（acceptor 原文摘要） | 落實 |
| --- | --- | --- |
| 1 | 非 winner：保留該方法 CV winner 的 Test 圖與 KPI，顯示清楚可見的黃色提示 | 維持 v0.1 行為 |
| 2 | Invalid candidate：保持可選取，展示 invalid 原因，但停用即時預測 | 維持 v0.1 行為（KPI 區顯示原因、預測器顯示「invalid 候選：無預測」） |
| 3 | PI 篩選開關：本階段不增加，保留完整逐筆 PI、縮放及游標檢視 | 不新增任何篩選；逐筆資料不抽樣 |
| 4 | All-in：改為只顯示固定 k=18，不再顯示 1–17 的 disabled 按鈕 | **已修正**：選 All-in 時 k 格子換成單一「k = 18」狀態列與說明，圖例隱藏 |
| 5 | 係數表：預設收合 | 維持 |
| 6 | 字型：維持系統 CJK 字型，不增加外部相依 | 維持 |
| 7 | 手機導覽：改為可展開選單，提供頁內錨點 | **已修正**：≤768 px 顯示「選單」按鈕（`aria-expanded`、`aria-controls`），展開直向錨點；Enter／Space 開關、開啟時焦點移到第一個連結、Escape 關閉並回到按鈕、點選錨點後關閉、Tab 離開時關閉、放大視窗時自動收合 |

同時確認：Mock Data 橫幅持續置於頂部並與預測結果卡的「模擬數值」標籤並存；沒有修改 Brief、Spec 或任何模型計算邏輯；新增的 UI 操作沒有改變訓練 CV／Test 的分層（手機選單只做頁內跳轉）；wireframe 的模擬計算不是正式模型實作。
