# DIC-1 補齊規格 Brief

本檔記錄 `week02/` 目前的實作與課程規格之間的落差，以及補齊所需的工作項目。

## 1. 依據

- **規格**：Requirements Specification: AIoT Personal Portal & Timekeeper（`AIoT2026-L2Web`，作者 Huan Chen）。
- **老師的參考實作**：<https://github.com/huanchen1107/0916-2>（含 `requirements.md`、`design.md`、`index.html`、`style.css`、`app.js`、`projects.json`）。
- **目前實作**：[`index.html`](./index.html) 單檔，另有 [`CONTEXT.md`](./CONTEXT.md)、[`README.md`](./README.md)。

目前實作是在取得這份規格之前完成的，所以落差不是實作品質問題，而是當初的範圍就比較小。

## 2. 現況總結

規格共 23 條功能需求（FR）：

| 狀態 | 數量 | 項目 |
| --- | --- | --- |
| 完全符合 | 1 | FR-1.3 |
| 部分符合 | 6 | FR-1.1、FR-1.5、FR-3.1、FR-5.1、FR-7.1、FR-7.2 |
| 完全未做 | 16 | FR-1.2、FR-1.4、FR-1.6、FR-2.1～2.4、FR-3.2、FR-3.3、FR-4.1～4.3、FR-5.2、FR-6.1～6.3 |

另外目前的 [`CONTEXT.md`](./CONTEXT.md) 寫著「只有視覺主題與時間格式會被保存」「專注模式永遠不保存」，與 FR-5.2 要求保存 7 個欄位（含 `zenMode`）直接衝突，補齊功能時必須一併改寫。

## 3. 待補項目

### FR-1 Hero 時鐘與個人身分

| 需求 | 目前 | 待補 |
| --- | --- | --- |
| FR-1.1 毫秒與 UNIX timestamp | 只有時分秒，`setInterval` 每秒更新 | 加毫秒與 epoch 秒數顯示；改用 `requestAnimationFrame` 連續更新，整秒才觸發日期與音效 |
| FR-1.2 SVG 秒數進度環 | 無 | 以 `<circle>` + `stroke-dasharray` / `stroke-dashoffset` 畫圓環，依「秒 + 毫秒」計算進度，60 秒一圈 |
| FR-1.3 12／24 小時制切換 | 已完成 | 保留；另補 `T` 快捷鍵（參考實作有） |
| FR-1.4 時段問候徽章 | 無 | 依台北時間的小時數顯示 Good morning／afternoon／evening／night，整秒更新 |
| FR-1.5 ISO 週數與年積日 | 只有日期與星期 | 加 ISO 8601 週數與 day-of-year 計算，顯示成日期列上的標籤 |
| FR-1.6 名稱與標語可直接編輯 | 名稱寫死，沒有標語 | 用 `contenteditable` 做行內編輯，失焦或 Enter 即存入 state；名稱縮寫同步更新到頭像 |

### FR-2 天氣（Open-Meteo）

整組未做，目前檔案內沒有任何 `fetch`。

需要：呼叫 `https://api.open-meteo.com` 取得目前氣溫與天氣代碼，顯示成 `26°C ⛅ · Taichung`；提供 Taichung／Taipei／Hsinchu／Tainan／Kaohsiung 城市選單；失敗時顯示離線或快取狀態。

> **注意**：老師的參考實作 **沒有實作這一組**——`app.js` 與 `index.html` 內找不到任何 weather / open-meteo / city 字串，`design.md` 的狀態樹也沒有 `selectedCity` 欄位。也就是規格有列、示範程式沒做。要不要做需要你決定（見第 5 節）。

### FR-3 抽屜式作品瀏覽

整組未做。需要：右側滑出的 glass 抽屜，含 Projects／About／Connect 三個分頁；由 Hero 上的三顆按鈕開啟；可用遮罩點擊、關閉鈕或 `ESC` 關閉；桌機約 520px 側欄，手機（<600px）全螢幕。

### FR-4 `projects.json` 非同步載入

整組未做，`projects.json` 檔案也不存在。需要：建立 `projects.json`，以 `fetch('./projects.json')` 載入後動態產生卡片，卡片含分類標籤、標題、描述、技術標籤與連結。資料不可寫死在 HTML。

參考實作的欄位格式：

```json
{
  "id": "edge-vision-defect-detection",
  "title": "Edge AI Industrial Vision Inspection",
  "category": "Edge Computing",
  "badge": "Featured",
  "description": "…",
  "techStack": ["YOLOv8", "TensorRT", "Jetson Orin"],
  "githubUrl": "https://github.com",
  "demoUrl": "#"
}
```

### FR-5 統一狀態管理

| 需求 | 目前 | 待補 |
| --- | --- | --- |
| FR-5.1 單一 state 物件、key 為 `aiot_user_state` | 有存，但 key 是 `momo-preferences` | 改 key 與結構；沿用現有的 try／catch 保護 |
| FR-5.2 保存 7 個欄位 | 只存 `theme`、`format24` | 補 `name`、`tagline`、`soundEnabled`、`selectedCity`、`zenMode`，並把欄位名對齊規格（`format24h`） |

> 規格的 FR-5.2 有 `selectedCity`，但參考實作的 `design.md` 狀態樹沒有這個欄位——跟 FR-2 是同一個取捨。

### FR-6 Web Audio 滴答聲

整組未做。需要：導覽列的靜音切換鈕（🔊／🔇，預設靜音）；用 Web Audio API 合成滴答聲，不載入任何音檔；狀態存入偏好。參考實作的作法是 sine 振盪器從 1400Hz 在 25ms 內指數下滑到 300Hz，音量同步衰減。

### FR-7 Zen 模式

目前的「專注模式」已經達成「隱藏控制項、只留時鐘」的效果，但差三點：沒有 `Z` 快捷鍵、沒有 Zen 圖示鈕（目前是文字按鈕）、狀態刻意不保存（FR-5.2 要求保存 `zenMode`）。

## 4. 非功能需求待補

- **NFR-1 零依賴**：目前 HTML 連外載入 Google Fonts，離線雙擊開啟時字型會失效。要嚴格符合「double-clickable」就得改用系統字型堆疊。
- **NFR-2 效能**：60fps 的秒環動畫要等 FR-1.2 做完才能驗；目前 1 秒一次的更新頻率不符合「smooth」。
- **NFR-3 視覺**：規格要求預設為 **AIoT Cyber Ambient 深色主題**，含會動的發光漸層球。目前預設是淺色 `Sunset`，光暈是靜態的。主題名稱 `aurora`／`minimal`／`sunset` 與參考實作一致，不需改名。
- **NFR-4 教學註解**：規格要求對四類主題有教學註解——DOM 選取與事件、非同步 `fetch` 與 JSON 解析、Canvas／SVG 繪製、localStorage 序列化與狀態還原。目前只有三處零星註解。

## 5. 需要你決定的事

1. **FR-2 天氣要不要做？** 規格有列，但老師的示範沒做。做了是加分，不做則與示範一致。
2. **視覺要照規格改成深色預設嗎？** 現有三主題可保留成替代主題，只調整預設值與加上動態光暈。
3. **介面語言？** 目前全繁體中文，規格與參考實作都是英文（`Good morning`、`Week 38`）。
4. **檔案要不要拆開？** 目前是單一 `index.html`；參考實作的 `design.md` 拆成 `index.html` + `style.css` + `app.js` + `projects.json`。拆開較貼近課程的教學進程，也是 FR-4 的前提之一（`projects.json` 一定要獨立檔案）。

## 6. 需要你提供的素材

- Projects：作品名稱、分類、描述、技術標籤與連結。
- About：自我介紹、學歷背景、研究興趣、技能標籤。
- Connect：GitHub、LinkedIn、Email、課程入口的實際網址。
- 名稱與標語的預設值（目前是 `Momo`，沒有標語）。

未提供前先放可辨識的佔位內容，不會冒充成真實資料。

## 7. 建議施作順序

1. 狀態層先改（FR-5）：換成 `aiot_user_state` 單一狀態樹，後面每個功能都掛在上面。
2. 時鐘強化（FR-1.1、1.2、1.4、1.5）。
3. 抽屜與資料載入（FR-3、FR-4，含新增 `projects.json`）。
4. 行內編輯與音效（FR-1.6、FR-6）。
5. Zen 模式補齊與快捷鍵（FR-7）。
6. 視覺與教學註解收尾（NFR-3、NFR-4），同步更新 `CONTEXT.md` 與 `README.md`。
7. 視第 5 節的決定再處理 FR-2。
