# Spec: AIoT Personal Portal & Timekeeper（DIC-1 補齊規格）

- **專案識別**：`AIoT2026-L2Web`
- **依據**：課程規格 Requirements Specification（作者 Huan Chen）；落差盤點見 [`../brief/BRIEF.md`](../brief/BRIEF.md)
- **狀態**：待實作
- **Issue tracker**：尚未設定，此 spec 暫存為檔案

## Problem Statement

目前 `week02/` 的網站只做到「顯示台北時間」這件事：時鐘、日期、三套主題、12／24 小時制、複製時間、一個專注模式。課程規格要求的是一個完整的個人入口網站——可編輯的身分區塊、秒級進度環、即時天氣、作品集抽屜、非同步載入的專案目錄、環境音效與統一的狀態保存。

對使用者來說，現在的問題是：

- 訪客打開網站只看得到時間，看不到「這個人是誰、做過什麼、怎麼聯絡」。
- 網站擁有者無法在頁面上修改自己的名稱與標語，要改就得改程式碼。
- 老師依規格驗收時，23 條功能需求只有 1 條完全符合、6 條部分符合，其餘 16 條沒有實作。
- 作為 DIC-1 的教學里程碑，這份程式碼沒有示範到 Fetch API、JSON 解析、動態 DOM 產生、Web Audio 與完整狀態保存——而這些正是 Lecture 2 的學習目標。

## Solution

把現有單檔網站擴充成規格要求的個人入口網站，維持零依賴、零建構、可直接部署到 GitHub Pages：

- **Hero 保持乾淨**：畫面主體仍是身分與時鐘，其餘內容收在右側滑出的玻璃抽屜裡。
- **時鐘升級**：連續更新的時分秒 + 毫秒 + UNIX timestamp，外圈是 60 秒一圈的 SVG 進度環，旁邊是依時段變化的問候徽章、完整日期、ISO 週數與年積日。
- **身分可編輯**：名稱與標語可直接在頁面上點擊編輯，即時存檔，頭像縮寫同步更新。
- **環境資訊**：串接 Open-Meteo 顯示目前氣溫與天氣，可切換台灣五個科技城市，離線時顯示上次成功的讀數並標示為離線。
- **作品集抽屜**：Projects／About／Connect 三個分頁，專案資料從 `projects.json` 非同步載入後動態產生卡片。
- **環境音效**：以 Web Audio API 合成機械滴答聲，預設靜音，可切換並保存。
- **Zen 模式**：一鍵或按 `Z` 變成純環境桌鐘，`ESC` 或 `Z` 離開，狀態會被保存。
- **統一狀態**：所有偏好合併為單一狀態物件，存在 `localStorage` 的 `aiot_user_state`。

視覺與介面文字全部以規格為準：預設深色 AIoT Cyber Ambient 主題，介面文字為英文。

## User Stories

### 身分與時鐘

1. As a 網站訪客, I want 一進站就看到大而清楚的目前時間, so that 我不需要任何操作就能知道現在幾點。
2. As a 網站訪客, I want 時鐘連續平滑地更新, so that 畫面看起來是活的，而不是每秒跳一次的靜態文字。
3. As a 網站訪客, I want 看到毫秒數字, so that 我能感覺到這個時鐘是即時運算的，而不是伺服器給的固定值。
4. As a 學習 Web 的學生, I want 看到 UNIX timestamp, so that 我能把畫面上的人類可讀時間和程式裡的時間表示法對應起來。
5. As a 網站訪客, I want 時鐘外圈有一個隨秒數填滿的圓環, so that 我能用餘光感知一分鐘走到哪裡，而不必讀數字。
6. As a 網站訪客, I want 切換 12 小時制與 24 小時制, so that 我能用自己習慣的方式讀時間。
7. As a 回訪的訪客, I want 我選的時間格式下次造訪時還在, so that 我不用每次重新設定。
8. As a 網站訪客, I want 看到依現在時段變化的問候語, so that 網站感覺像在對我說話，而不是一塊冷冰冰的面板。
9. As a 網站訪客, I want 看到完整的日期與星期, so that 我知道今天是哪一天。
10. As a 專案管理者, I want 看到 ISO 週數, so that 我能把今天對應到工作週次。
11. As a 學習資料處理的學生, I want 看到年積日（day of year）, so that 我理解日期還有其他常用的表示方式。
12. As a 國外訪客, I want 時間永遠是台北時間並標示 UTC+8, so that 我不會誤以為那是我所在地的時間。
13. As a 網站擁有者, I want 直接點擊頁面上的名字就能修改, so that 我不必動程式碼就能換名字。
14. As a 網站擁有者, I want 同樣能編輯我的標語, so that 我能隨時調整自我介紹的一句話。
15. As a 網站擁有者, I want 名稱改完後頭像縮寫自動跟著換, so that 視覺上不會出現名字與縮寫對不起來的狀況。
16. As a 網站擁有者, I want 編輯完立刻存檔, so that 我不需要找「儲存」按鈕。
17. As a 網站擁有者, I want 編輯時按 Esc 可以取消, so that 我改錯了能退回原本的值。
18. As a 網站訪客, I want 一鍵複製目前時間戳記, so that 我能把它貼到筆記或訊息裡。
19. As a 鍵盤使用者, I want 用快捷鍵完成複製、切換格式與進入 Zen, so that 我不必用滑鼠點按鈕。

### 環境資訊（天氣）

20. As a 網站訪客, I want 在時間旁邊看到目前氣溫與天氣狀態, so that 我一眼掌握此刻的環境脈絡。
21. As a 網站訪客, I want 天氣旁邊顯示城市名稱, so that 我知道這個溫度是哪裡的。
22. As a 台灣使用者, I want 在台中、台北、新竹、台南、高雄之間切換, so that 我能看到自己所在城市的天氣。
23. As a 回訪的訪客, I want 我選的城市被記住, so that 我不用每次重選。
24. As a 網路不穩的訪客, I want 取不到天氣時看到上次的讀數並標明是離線資料, so that 我不會把過期資料誤認為即時資料。
25. As a 網站擁有者, I want 天氣服務掛掉時網站其他功能照常運作, so that 單一外部服務不會拖垮整個頁面。
26. As a 學習 Fetch API 的學生, I want 看到一個不需要 API key 的真實 API 串接範例, so that 我能自己動手重現。

### 作品集抽屜

27. As a 網站訪客, I want 主畫面保持乾淨不被作品列表塞滿, so that 我第一眼的注意力在身分與時間上。
28. As a 有興趣的訪客, I want 點按鈕滑出作品集抽屜, so that 我能在需要時才深入了解。
29. As a 潛在合作者, I want 在 Projects 分頁看到作品卡片, so that 我能快速評估這個人做過什麼。
30. As a 訪客, I want 每張卡片標示分類與技術標籤, so that 我能判斷哪些作品與我關心的領域相關。
31. As a 訪客, I want 卡片上有原始碼或 demo 連結, so that 我能直接前往查看。
32. As a 訪客, I want 在 About 分頁看到自我介紹、學歷與研究興趣, so that 我了解這個人的背景。
33. As a 想聯絡的訪客, I want 在 Connect 分頁找到 GitHub、LinkedIn、Email 與課程入口連結, so that 我知道怎麼接觸到本人。
34. As a 訪客, I want 用遮罩點擊、關閉鈕或 Esc 關掉抽屜, so that 我能用任何直覺的方式離開。
35. As a 手機使用者, I want 抽屜在小螢幕上是全螢幕, so that 內容不會被擠在狹窄的側欄裡。
36. As a 鍵盤與螢幕閱讀器使用者, I want 抽屜打開時焦點進入抽屜、關閉後回到原按鈕, so that 我不會迷失在頁面上。

### 資料載入

37. As a 網站擁有者, I want 新增作品時只改資料檔不動 HTML, so that 更新作品集不需要碰版面程式碼。
38. As a 學習非同步的學生, I want 看到 `fetch` 載入 JSON 後動態產生 DOM 的完整流程, so that 我理解資料與畫面是怎麼分離的。
39. As a 訪客, I want 作品資料載入失敗時看到明確訊息, so that 我知道是載入出問題，而不是這個人沒有作品。

### 音效與 Zen 模式

40. As a 網站訪客, I want 網站預設不發出任何聲音, so that 我在公共場合打開不會被嚇到。
41. As a 想要氛圍的訪客, I want 打開滴答聲, so that 這個頁面能當成一個有聲音的桌鐘。
42. As a 回訪的訪客, I want 我的音效設定被記住, so that 我不用每次重開。
43. As a 網站擁有者, I want 音效不依賴任何外部音檔, so that 網站在任何網路環境都能正常運作。
44. As a 想專心的使用者, I want 按 Z 或點圖示進入 Zen 模式, so that 螢幕變成乾淨的環境桌鐘。
45. As a Zen 模式使用者, I want 按 Esc 或 Z 離開, so that 我能快速回到完整介面。
46. As a 長期把這頁當桌鐘的使用者, I want Zen 模式狀態被記住, so that 下次打開就直接是桌鐘。

### 狀態、視覺與部署

47. As a 回訪的訪客, I want 名稱、標語、主題、時間格式、音效、城市與 Zen 狀態全部被記住, so that 網站保持我上次離開時的樣子。
48. As a 使用無痕視窗或封鎖儲存的訪客, I want 網站在無法存取 localStorage 時仍完全可用, so that 我不會看到壞掉的頁面。
49. As a 網站訪客, I want 預設是深色的 AIoT Cyber Ambient 主題, so that 第一印象符合這是一個 AIoT 主題的網站。
50. As a 網站訪客, I want 切換 Minimal 與 Sunset 主題, so that 我能選自己看得舒服的配色。
51. As a 偏好減少動態效果的使用者, I want 系統設定的 reduced motion 被尊重, so that 動畫不會造成我的不適。
52. As a 手機使用者, I want 在 375px 寬度下版面正常且不橫向捲動, so that 我在手機上也能正常使用。
53. As a 授課老師, I want 網站直接從 GitHub Pages 開啟就能驗收, so that 我不需要在本機安裝任何東西。
54. As a 閱讀程式碼的學生, I want 程式碼有解釋 DOM 操作、fetch 與 JSON、SVG 繪製、localStorage 狀態還原的教學註解, so that 我能照著程式碼學會這堂課的主題。
55. As a 維護這份作業的開發者, I want 純邏輯有自動化測試, so that 我改動時間計算或狀態處理時不會默默弄壞既有行為。

## Implementation Decisions

### 架構與模組切分

- 專案從單一 `index.html` 拆成四個檔案加一個核心模組：頁面結構（`index.html`）、樣式與主題（`style.css`）、應用程式接線（`app.js`）、純邏輯核心（`core.js`）、專案目錄資料（`projects.json`）。
- **`core.js` 是唯一的測試接縫**：只放純函式，不碰 DOM、`localStorage`、`fetch`、`AudioContext` 或 `Date.now()`。所有需要「現在時間」的函式一律由呼叫端把 `Date` 物件傳進來。
- **`app.js` 負責所有副作用**：DOM 查詢與事件、儲存讀寫、網路請求、音訊合成、動畫迴圈。它從 `core.js` 匯入純函式，自己不重複實作邏輯。
- 兩者以 ES module 連接，`index.html` 用 `<script type="module">` 載入。
- 不引入任何套件、建構工具或 `node_modules`，維持 NFR-1。

### 狀態管理

- 單一狀態樹序列化為 JSON，存在 `localStorage` 的 `aiot_user_state`：

  ```typescript
  interface UserState {
    name: string;
    tagline: string;
    theme: "aurora" | "minimal" | "sunset";
    format24h: boolean;
    soundEnabled: boolean;
    selectedCity: string;   // 城市代號，例如 "taichung"
    zenMode: boolean;
  }
  ```

- 主題代號沿用現有的 `aurora`／`minimal`／`sunset`，對應規格的 Cyber Ambient／Swiss Minimalist／Solar Twilight。**預設值改為 `aurora`**（規格要求深色為預設）。
- 讀取時一律經過一個純正規化函式：未知欄位丟棄、型別不符或值不在允許範圍的欄位回退到預設值，確保手動竄改 storage 不會讓頁面壞掉。
- 任何偏好變更都立即整包寫回。storage 讀寫全部包在 try／catch 裡，失敗時退化成記憶體內狀態，功能照常。
- 天氣的快取讀數**不放在 `aiot_user_state`**，另存獨立的快取鍵，避免污染規格定義的 7 個欄位。

### 時鐘與日曆

- 以 `requestAnimationFrame` 驅動渲染迴圈，取代目前的 `setInterval`，滿足 NFR-2 的平滑需求。
- 每一幀更新毫秒與進度環；時／分／秒與日期類資訊只在值改變時才寫入 DOM，避免不必要的重繪。
- 進度環用 SVG `<circle>` 搭配 `stroke-dasharray` 與 `stroke-dashoffset`，進度取自「秒 + 毫秒」在 60 秒週期內的比例，因此走動是連續的而非每秒跳一格。
- 所有時間顯示固定使用 `Intl.DateTimeFormat` 搭配 `timeZone: 'Asia/Taipei'`，不使用裝置時區。
- ISO 週數、年積日、問候語時段判斷、12／24 小時格式化、時間戳記文字組裝全部是 `core.js` 的純函式。
- 問候語時段：05:00–11:59 morning、12:00–17:59 afternoon、18:00–21:59 evening、22:00–04:59 night。

### 身分編輯

- 名稱與標語使用 `contenteditable`，Enter 或失焦提交、Esc 取消。
- 提交前經過純清理函式：去除換行與前後空白、限制長度、空字串視為無效並還原前值。
- 頭像縮寫由名稱推導，也是純函式（取前兩個字的首字元，單字時取前兩個字元）。
- 編輯狀態下全域快捷鍵停用，避免打字時觸發 Z／T／C。

### 天氣

- 資料來源 Open-Meteo 的 forecast 端點，查詢目前氣溫與 WMO weather code，不需要 API key。
- 五個城市的經緯度以常數表維護：Taichung、Taipei、Hsinchu、Tainan、Kaohsiung。城市清單與座標定義在 `core.js`。
- WMO weather code 轉成圖示與描述是純函式，涵蓋晴、多雲、陰、霧、雨、陣雨、雷雨、雪等主要分組，未知代碼回退到一個中性圖示。
- 成功取得後把讀數與取得時間寫入快取鍵；請求失敗、逾時或離線時讀取快取並在 UI 上標示為離線與該筆資料的時間。完全沒有快取時顯示 unavailable，不顯示假資料。
- 請求帶逾時控制（`AbortController`），避免長時間吊住。
- 切換城市即觸發一次新請求並更新狀態。

### 抽屜與專案資料

- 抽屜為右側滑出面板，桌機約 520px、螢幕寬度小於 600px 時全螢幕；`role="dialog"`、`aria-modal="true"`，開啟時焦點移入、關閉後焦點回到觸發按鈕。
- 三個分頁 Projects／About／Connect 以 tab 模式切換，符合 `role="tablist"` 的鍵盤行為。
- 關閉途徑：遮罩點擊、關閉鈕、`ESC`。`ESC` 的優先順序是「先關抽屜，抽屜沒開才離開 Zen 模式」。
- 專案資料以 `fetch('./projects.json')` 載入，HTML 內不得有任何硬編碼的專案內容。
- `projects.json` 的每筆資料包含：`id`、`title`、`category`、`badge`、`description`、`techStack`、`githubUrl`、`demoUrl`。
- 載入後先經過純驗證／正規化函式，丟棄結構不符的項目，再由 `app.js` 產生卡片 DOM。
- 卡片文字一律以 `textContent` 寫入，不使用 `innerHTML` 組字串，避免資料內容被當成標記解析。
- 載入失敗時在 Projects 分頁顯示錯誤訊息與重試按鈕。
- About／Connect 的內容在素材到位前使用明顯可辨識的佔位文字，不冒充成真實經歷或連結。

### 音效

- 以 `AudioContext` 合成滴答聲，不載入任何音檔。單次滴答為 sine 振盪器在約 25ms 內由高頻指數下滑，音量同步衰減到接近零。
- 預設靜音。因為瀏覽器的自動播放政策，`AudioContext` 必須在使用者第一次互動（點擊音效鈕）時才建立或 resume。
- 音效開啟時，每個整秒邊界播放一次滴答；Zen 模式與一般模式行為相同。

### 視覺與介面語言

- 介面文字改為英文，與規格範例一致（`Good morning`、`Week 38`、`26°C ⛅ · Taichung`）。`lang` 屬性同步改為 `en`。
- 預設主題 `aurora` 為深色，背景加上緩慢移動的發光漸層球；`prefers-reduced-motion` 下停用動畫但保留靜態光暈。
- 玻璃質感（`backdrop-filter`）用於 Hero 卡片、控制列與抽屜。
- 保留既有的響應式斷點策略、`:focus-visible` 樣式與 44px 最小點擊尺寸。
- 目前由 Google Fonts CDN 載入的字型改為系統字型堆疊，去除唯一的外部資源依賴。

### 教學註解（NFR-4）

程式碼以區段註解組織，至少涵蓋四類說明：DOM 選取與事件處理、非同步 `fetch` 與 JSON 解析、SVG 進度環的程序化繪製、localStorage 的序列化與狀態還原。

### 文件同步

- `CONTEXT.md` 需改寫：目前寫的「只有主題與時間格式會被保存」「專注模式永遠不保存」與 FR-5.2 衝突，改為 7 欄位狀態樹的定義，並補上天氣、抽屜、專案卡片等新概念的詞彙。
- `README.md` 的功能清單、專案結構與本機預覽說明需同步更新。

## Testing Decisions

### 什麼是好的測試

- 只測外部行為：給定輸入得到什麼輸出，不測函式內部怎麼算。
- 測試不碰 DOM、網路、儲存與音訊；需要時間的測試一律傳入固定的 `Date`，不依賴執行當下的時間。
- 一個測試一個行為，名稱直接描述該行為。
- 邊界值優先：跨年的 ISO 週數、閏年的年積日、午夜與正午的 12 小時制、問候語的時段交界、進度環在 0 秒與 59.999 秒、狀態欄位型別錯誤或超出允許值、天氣代碼未知值、專案資料缺欄位。

### 測試範圍

- **受測模組**：只有 `core.js`。它是整個專案唯一的測試接縫，所有邏輯決策都集中在這裡。
- **不寫自動化測試的部分**：`app.js` 的 DOM 接線、抽屜動畫、音訊輸出、實際網路請求。這些以瀏覽器手動驗收清單覆蓋。
- **執行方式**：Node 內建的測試執行器（`node --test`），測試檔以 `.test.mjs` 命名，放在 `week02/` 下的測試目錄。不安裝任何套件，`node_modules` 仍然不存在，瀏覽器端的零依賴不受影響。

### 具體測試項目

- 時間格式化：24 小時制與 12 小時制（含 AM／PM 與午夜／正午）。
- ISO 週數：年初、年末、跨年週、閏年。
- 年積日：平年與閏年的 3 月 1 日、12 月 31 日。
- 問候語：四個時段與交界值。
- 進度環比例：0 秒、30 秒、59.999 秒。
- 狀態正規化：空物件、缺欄位、型別錯誤、未知主題值、多餘欄位。
- 時間戳記文字組裝：兩種時間格式下的輸出。
- 名稱清理與縮寫推導：空白、換行、超長、單一字、中英文名。
- WMO 天氣代碼對應：各主要分組與未知代碼。
- 專案資料正規化：完整資料、缺必要欄位、`techStack` 型別錯誤、空陣列。

### 既有做法

這個 repository 目前沒有任何測試，沒有可參照的前例。本 spec 建立的測試即為 `week02/` 的第一份，後續週次若需要測試可沿用同樣的模式：純邏輯集中在一個可匯入的模組、用 Node 內建測試執行器驗證、副作用留在瀏覽器端手動驗收。

## Out of Scope

- **Projects／About／Connect 的真實內容**：作品、學經歷、聯絡連結由使用者提供，本次以佔位內容實作，替換內容不需要改程式。
- **GitHub Pages 的啟用設定**：屬於 repository 設定操作，不是程式碼工作；本 spec 只確保產出的檔案可直接被 Pages 發布。
- **多時區切換**：時間固定為 `Asia/Taipei`，城市選擇只影響天氣，不影響時鐘。
- **介面語言切換**：本次直接改為英文單一語言，不做 i18n 機制。
- **後端、資料庫、使用者帳號**：全部不在範圍內，狀態只存在瀏覽器。
- **跨週共用元件**：不為了重用而把程式碼抽到 `week02/` 之外。
- **其他週次與作業目錄**：本 spec 只涵蓋 `week02/`。

## Further Notes

- **規格內部有一處矛盾**：NFR-1 要求「double-clickable locally」，但 FR-4.2 指定 `fetch('./projects.json')`，而瀏覽器會擋下 `file://` 協定的 fetch。也就是說在採用 ES module 之前，這個專案就已經需要本機伺服器才能完整運作。文件會明確寫出「用 `python -m http.server` 預覽或直接看 GitHub Pages」，並在 fetch 失敗時給出清楚訊息而不是空白畫面。
- **FR-2 在老師的參考實作中並未實作**：比對 <https://github.com/huanchen1107/0916-2> 的 `app.js` 與 `index.html`，找不到任何 weather／open-meteo／city 的程式碼，其 `design.md` 的狀態樹也沒有 `selectedCity`。我們選擇完整實作這四條，因此這部分沒有示範程式可對照，介面呈現方式由本 spec 自行定義。
- **參考實作只用於比對規格**，不複製其程式碼。主題代號一致是因為規格本身就定義了三套主題。
- **既有實作中值得保留的部分**：`Intl.DateTimeFormat` 固定台北時區的做法、剪貼簿複製的 fallback、toast 提示、`prefers-reduced-motion` 支援、375px 響應式處理與 `:focus-visible` 樣式，這些在重構後繼續沿用。
- **無障礙注意事項**：時鐘本身不設 `aria-live`，否則螢幕閱讀器會每秒朗讀一次；狀態變更（複製成功、主題切換、天氣更新）透過既有的 polite 狀態區宣告。
- **Issue tracker 未設定**：此 spec 目前以檔案形式保存。設定好 tracker 後可直接貼上並標記 `ready-for-agent`。
