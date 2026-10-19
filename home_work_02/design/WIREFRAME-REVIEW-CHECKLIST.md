# HW2 Dashboard Wireframe — Review Checklist（供 acceptor）

> **Review 結果：UI DESIGN ACCEPTED（2026-10-18，acceptor 目視驗收 v0.2 @ `0eb86259`）。** A–G、J、K 的設計項目依 acceptor 的目視確認視為通過；H、I 中屬於 Open Verification Items（真正斷網 `file://`、真實手機與觸控、Safari／Firefox、螢幕閱讀器、對比量測、正式 dashboard 的 PI 渲染效能）**維持 OPEN、不得標 PASS**，帶入後續 Tickets 與 ACCEPTANCE.md。完整紀錄見 [`WIREFRAME-ACCEPTANCE.md`](WIREFRAME-ACCEPTANCE.md)。

開啟方式：直接以瀏覽器開啟 `home_work_02/design/wireframe/index.html`（`file://`，可斷網）。每項勾選 PASS／FAIL／N/A 並附註。

## A. 資料邊界與標示

- [ ] 頁面頂部有持續可見的「示意資料／非實際模型結果」橫幅。
- [ ] 預測結果卡標示「模擬數值」；Test 區塊的數字沒有被寫成真實結果。
- [ ] 沒有任何文字暗示已執行 Python 模型或完成統計驗證。

## B. 模型選擇（Spec 區塊 1）

- [ ] 四種路徑方法＋All-in baseline 可選；用語為「四種有 k 路徑的方法＋單一 All-in」。
- [ ] k = 1…18 可切換；每個方法的 CV winner 有可辨識的標記（不只靠顏色）。
- [ ] 選 All-in 時 k 格子換成單一「k = 18 固定」狀態列，不顯示 1–17（UI 決策 4）。
- [ ] invalid 候選（示意：RFE k=17）有明確標示，KPI 顯示原因，且不會被標成 winner。
- [ ] 「比較全部」能疊出四條路徑並顯示比較表（含 Ridge／Lasso metric-only、講義對照列、整體 winner 標示）。
- [ ] 目前選取摘要列出 canonical subset 與標籤（該方法 winner／整體 winner／invalid）。

## C. 訓練 CV（Spec 區塊 2、3；SR-05）

- [ ] KPI 卡有 MAE、MSE、RMSE、R²，並標示「訓練 CV（USD）」。
- [ ] Adjusted R² 卡標示為 log 尺度、全訓練集擬合（`fit`），不會與 USD 指標混淆。
- [ ] 指標 vs k 圖有四條路徑、All-in／Ridge／Lasso 參考線（線型不同）、winner 與 invalid 標記、圖例。
- [ ] 指標下拉（RMSE／MAE／R²）切換正常。

## D. 即時預測（Spec 區塊 5；Q31、Q32；SR-07）

- [ ] 只顯示目前模型用到的 source feature；輸入為原始值（日期、整修年或未整修、zipcode 下拉…）。
- [ ] 預設值為 training 中位數；欄位旁有 training 範圍說明。
- [ ] 超出範圍時欄位與結果卡都有警告，且仍給出數值。
- [ ] 選擇示意的未見 zipcode（98000）時出現「以基準類別計算」警告。
- [ ] 顯示點預測與 95% PI（不對稱）；Ridge／Lasso 不提供預測的說明存在。
- [ ] 選到 invalid 候選時預測器停用並說明。

## E. Test 評估（Spec 區塊 6；BR-01；Q43；SR-09）

- [ ] Test 區塊在視覺上與訓練 CV 明顯分層（灰底、深色邊、「Test 評估（USD）」標籤）。
- [ ] 顯示展示模型的方法與 k，以及 winner／整體 winner 標籤。
- [ ] 選非 winner 的 k 時，有清楚可見的提示說明 Test 區塊展示的是該方法 winner，且「切換不會觸發新的評估」。
- [ ] Test KPI 四張卡存在並標示 Test。
- [ ] 散佈圖：x 預測、y 實際、log 刻度、y=x 參考線、逐筆垂直 PI 線段、依涵蓋著色、圖例。
- [ ] 滾輪縮放、拖曳平移、放大／縮小／重設按鈕可用；游標停留可讀取單筆（實際、預測、PI、是否涵蓋）。
- [ ] 放大後可分辨個別 PI 線段與端點（Spec SR-09 (d) 的驗收概念）。
- [ ] 涵蓋率、涵蓋筆數／n_test、房屋數與重複交易、平均 PI 寬度、二項近似不確定性五項都有，且說明「不保證 95%」「不陳述偏差方向」。

## F. 方法與限制（Spec 區塊 9）

- [ ] 四段：特徵選擇方法、訓練 CV／Test 協定、PI 統計假設、限制與非因果；各段有三種標示之一。

## G. 選配區塊

- [ ] 係數表、Test 殘差表、全部結果表為可展開區塊，沒有擠掉必要內容；係數表標示 log 尺度。

## H. 版面、可用性與無障礙

- [ ] Desktop（≥1181 px）：控制面板 sticky、KPI 5 欄、預測器雙欄。
- [ ] Tablet（≈768–1024 px）：單欄堆疊、KPI 3 欄、無水平捲動。
- [ ] Mobile（375 px，實機或 DevTools）：無水平捲動、按鈕 ≥ 44 px、文字 ≥ 16 px、圖表可讀。
- [ ] Mobile 導覽（UI 決策 7）：「選單」按鈕可見；Enter／Space 展開與收合；`aria-expanded` 隨狀態切換；展開時焦點移到第一個錨點；Escape 關閉並回到按鈕；點選錨點後關閉並跳到區塊；Tab 離開選單時關閉。
- [ ] 鍵盤：Tab 順序合理、focus ring 可見、「跳到主要內容」可用；方法／k 按鈕以 Enter／Space 操作。
- [ ] 文字對比目測足夠（深色文字於淺底；警告文字為深琥珀色）。
- [ ] 全頁 zh-TW，無缺字方塊；數字使用等寬數字對齊。
- [ ] `prefers-reduced-motion` 開啟時沒有動畫。

## I. 離線

- [ ] 斷網、無伺服器、`file://` 開啟：全部區塊渲染、互動可用。
- [ ] 瀏覽器開發者工具網路面板：除本機 4 個檔案外沒有任何請求。

## J. 對 Spec 的忠實度

- [ ] 沒有新增 Spec 以外的功能（例如 Ridge／Lasso 預測、k 以外的選擇、抽樣）。
- [ ] 沒有刪減必要區塊 (1)(2)(3)(5)(6)(9)。
- [ ] 三種報告標示用語正確：老師要求／依老師補充建議／專案延伸。

## K. UI 決策（acceptor 2026-10-18；見 UI-DESIGN-NOTES.md §8）— 核對落實

- [ ] 1 非 winner：保留 winner 的 Test 圖與 KPI＋黃色提示
- [ ] 2 invalid：可選取、顯示原因、即時預測停用
- [ ] 3 無 PI 篩選開關；逐筆 PI 完整
- [ ] 4 All-in 只顯示固定 k = 18
- [ ] 5 係數表預設收合
- [ ] 6 系統 CJK 字型、無外部相依
- [ ] 7 手機可展開選單（見 H）

## L. 自動與半自動檢查結果（起草者，2026-10-18，v0.2）

| 檢查 | 結果 |
| --- | --- |
| 靜態掃描外部資源（`http(s)://`、`url(`） | 無 |
| `node --check` 兩個 JS 檔 | 通過 |
| 本機伺服器開啟：console 錯誤 | 無 |
| 網路面板 | 只有 4 個本機檔案 |
| DOM：All-in 時 k 格子為單一固定狀態列、圖例隱藏 | 見回報 |
| DOM：手機選單 `aria-expanded` 切換、Escape 關閉、焦點位置 | 見回報 |
| DOM：非 winner 提示、invalid 狀態、兩種警告、比較表 | 通過（v0.1 已驗證，v0.2 重跑） |
| 模擬 375 px 無水平捲動、按鈕 44 px | 通過 |

**未實測（需人工）**：真實 375 px 裝置、Safari／Firefox、`file://` 直接開啟（內建瀏覽器無法渲染本機檔案，改以本機伺服器檢查）、螢幕閱讀器朗讀、`prefers-reduced-motion` 實機、色彩對比的量測值、觸控裝置的拖曳與滾輪縮放。

**Review 結論**：☑ 通過（UI DESIGN ACCEPTED，2026-10-18）　☐ 修改後再審　☐ 退回

**Open Verification Items（不得標 PASS，帶入 Tickets）**：OV-1 真正斷網 `file://`；OV-2 真實手機與觸控；OV-3 Safari／Firefox；OV-4 螢幕閱讀器與完整 accessibility；OV-5 色彩對比量測；OV-6 正式 dashboard 的逐筆 PI 渲染效能（SR-09）。
