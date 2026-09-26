# AIoT-DA 課程實作

本儲存庫收錄「AIoT 與數據分析」（AIoT & Data Analytics, AIoT-DA）課程的每週課堂實作、作業與相關成果。

本檔是整個儲存庫的索引；各單元的題目、做法與結果寫在該單元自己的 `README.md`。

## 目錄組織

- `weekNN/` — 每週課堂實作（Do in Class，DIC）。
- `home_workNN/` — 每次作業（Homework）。

每個目錄是相對獨立的單元，內部結構以該單元實際檔案為準，可能包含說明文件、程式碼、資料集、實驗與結果。單元之間目前沒有共用程式或共用資源目錄。

```text
aiot-classwork/
├── README.md        # 本檔：全課程索引
├── CLAUDE.md        # 給 Claude Code 的長期專案指示
├── AGENTS.md        # 給 Codex 的長期專案指示
├── week02/          # DIC-1
└── home_work_01/    # 作業 1
```

## 課堂實作（Do in Class）

| 目錄 | 課堂實作 | 授課單元 | 內容 | Live Demo |
| --- | --- | --- | --- | --- |
| [`week02/`](./week02/) | DIC-1 | Lecture 2 — 瀏覽器、現代 Web 核心與非同步資料流（L2Web） | 個人入口網站與動態時鐘：Vanilla HTML／CSS／JS 單檔靜態網站，固定顯示 `Asia/Taipei` 時間，三套視覺主題、12／24 小時制切換與專注模式。 | [開啟](https://yotsubamomo.github.io/aiot-classwork/week02/) |

## 作業（Homework）

| 目錄 | 作業 | 內容 | Live Demo |
| --- | --- | --- | --- |
| [`home_work_01/`](./home_work_01/) | HW10 Taiwan Weather Forecast（CWA API 天氣預測） | CWA API × JSON × Python × SQLite × Streamlit：推導六大區域一週 MinT／MaxT 存入 SQLite，Streamlit 評分應用程式提供區域選單、折線圖與表格；另部署 Flask dashboard，含 Taiwan Map 的 Now mode（CWA 測站最新觀測、縣市下鑽、雷達）與 Forecast mode（六區預報地圖）。 | [開啟](https://aiot-hw01-weather.vercel.app) |

作業說明文件放在各作業目錄的 `doc/requirement/`，其中的 PDF 未納入版本控制。

## GitHub Pages

需要瀏覽器展示的單元從 `main` 分支根目錄發布，網址為 `https://yotsubamomo.github.io/aiot-classwork/<目錄名稱>/`。

`home_work_01/` 需要伺服器端程式（Flask 與 CWA API 金鑰），所以不走 GitHub Pages，而是部署在 Vercel：<https://aiot-hw01-weather.vercel.app>（`main` 合併後更新）。
