# AIoT-DA 課程實作

本儲存庫收錄「AIoT 與數據分析」課程的每週課堂實作、筆記與相關成果。

## DIC-1 專案資料

- **課程名稱**：AIoT 與數據分析（AIoT & Data Analytics, AIoT-DA）
- **課堂實作**：DIC-1（Do in Class 1）— 個人入口網站與動態時鐘
- **授課單元**：Lecture 2 — 瀏覽器、現代 Web 核心與非同步資料流（L2Web）
- **示範教師**：Huan Chen
- **網站顯示名稱**：Momo
- **完成日期**：2026-09-16
- **儲存庫網址**：[github.com/yotsubamomo/aiot-classwork](https://github.com/yotsubamomo/aiot-classwork)
- **Live Demo Page**：[yotsubamomo.github.io/aiot-classwork/week02/](https://yotsubamomo.github.io/aiot-classwork/week02/)
- **專案位置**：[`week02/`](./week02/)

## Live Demo Snapshot

[![DIC-1 個人入口網站與動態時鐘](./week02/home.jpg)](https://yotsubamomo.github.io/aiot-classwork/week02/)

> 點擊圖片可開啟 Live Demo。

## 今日專案摘要

DIC-1 使用零框架、零建構依賴的 Vanilla HTML、CSS 與 JavaScript，建立可直接部署至 GitHub Pages 的個人入口網站。網站以 `Momo` 為公開顯示名稱，所有日期與時間固定依照 `Asia/Taipei` 計算，不受訪客裝置時區影響。

本次完成的核心功能包括：

- 即時顯示台北日期與秒級時鐘。
- 支援 24 小時制及附 AM／PM 的 12 小時制。
- 提供 `Aurora`、`Minimal`、`Sunset` 三套視覺主題；主題只改變配色、背景與光影，不改變內容結構。
- 使用瀏覽器儲存空間保留主題與時間格式偏好。
- 可複製包含名稱、完整日期、時間與 `Asia/Taipei (UTC+8)` 的文字時間戳，並顯示短暫成功提示。
- 提供暫時性的專注模式，只保留名稱、時鐘、日期及退出控制；可按 `Esc` 離開且不保存模式狀態。
- 採用繁體中文操作文字、語意化按鈕、ARIA 標示、清楚的鍵盤焦點與 reduced-motion 支援。
- 響應式版面支援桌面與手機，不需要安裝套件或執行建構流程。

## 專案結構

```text
aiot-classwork/
├── README.md
└── week02/
    ├── CONTEXT.md   # DIC-1 的專案語彙與已確認行為邊界
    └── index.html   # HTML、CSS 與 JavaScript 單檔網站
```

### 核心檔案

| 檔案 | 用途 |
| --- | --- |
| [`week02/CONTEXT.md`](./week02/CONTEXT.md) | 定義顯示名稱、台北時間、時間格式、視覺主題、保存偏好、專注模式與複製時間。 |
| [`week02/index.html`](./week02/index.html) | 包含語意化頁面結構、三主題樣式、響應式版面與所有瀏覽器端互動。 |

## 技術重點

### 固定台北時區

時鐘透過 `Intl.DateTimeFormat` 並明確指定 `Asia/Taipei`，因此即使訪客位於其他國家，仍會顯示正確的台北時間。

### 三套視覺主題

三個主題共用相同的 Editorial Hello 版面與資訊架構，僅透過 CSS Custom Properties 改變視覺 presentation：

- **Aurora**：深色極光與青綠光感。
- **Minimal**：高對比、克制的黑白視覺。
- **Sunset**：暖灰背景與橘色圓形主視覺，也是首次造訪的預設主題。

### 有界限的偏好保存

網站只保存以下兩項偏好：

```json
{
  "theme": "sunset",
  "format24": true
}
```

專注模式、目前時間及操作提示皆不會保存。

## 本機預覽

本專案為純靜態網站，不需安裝 `node_modules`。建議從 `week02` 啟動本機伺服器：

```powershell
Set-Location week02
python -m http.server 5173
```

接著開啟：<http://localhost:5173>

也可以直接開啟 `week02/index.html`；使用本機伺服器能讓瀏覽器功能的行為更接近 GitHub Pages。

## GitHub Pages

網站不依賴伺服器端程式或絕對資源路徑。當此儲存庫的 GitHub Pages 從 `main` 分支根目錄發布後，DIC-1 位於：

<https://yotsubamomo.github.io/aiot-classwork/week02/>

## 驗證紀錄

- JavaScript 語法檢查通過。
- 實際瀏覽器完成主題、12／24 小時制、複製提示及專注模式測試。
- 375px 行動裝置寬度下無水平捲動，操作控制最小高度為 44px。
- Sunset 與 Aurora 主題已完成桌面視覺檢查。
