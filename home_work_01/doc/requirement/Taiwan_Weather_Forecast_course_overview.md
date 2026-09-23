# AI 創新微課程：Taiwan Weather Forecast

> 從氣象資料到互動式天氣預報應用  
> CWA API × JSON × Python × SQLite × SQLite × Streamlit

> 來源：老師提供的課程總覽圖片。  
> 說明：以下依圖片內容轉寫；第 22「延伸應用與想法」以及其後內容標示為「供參考」。

---

## 1. 課程介紹

**AI × 資料 × 天氣 × 實作**

- 課程目標
- 學習地圖
- 專案成果展示

## 2. 台灣的天氣與生活

**氣象的重要性**

- 天氣影響生活
- 資料驅動決策
- 智慧應用案例

## 3. 中央氣象署 CWA

**Open Data 平台**

- 註冊帳號
- 取得 API Key
- 選擇資料集

## 4. API 資料取得

**使用 Requests 取得 JSON**

```python
import requests

url = "https://..."
headers = {"Authorization": "..."}
resp = requests.get(url)
data = resp.json()
```

## 5. JSON 資料結構解析

**找到氣溫資料的位置**

```text
locations
└─ locationName: "中部地區"
   └─ weatherElement
      ├─ elementName: "MinT"
      └─ elementName: "MaxT"
```

## 6. 提取最高與最低氣溫

**資料分析與處理**

- 解析 JSON
- 提取 MinT / MaxT
- 轉換成結構化資料

## 7. 資料整理與預覽

**使用 Pandas 觀察資料**

| regionName | dataDate | mint | maxt |
| --- | --- | ---: | ---: |
| 北部地區 | 2026-04-14 | 18 | 26 |
| 中部地區 | 2026-04-14 | 20 | 30 |
| 南部地區 | 2026-04-14 | 22 | 31 |

## 8. 建立 SQLite 資料庫

**儲存氣溫資料**

- 建立資料庫
- 創建資料表
- 插入氣溫資料

資料庫檔案示意：

```text
data.db
```

## 9. 資料庫設計

**TemperatureForecasts**

```sql
id         INTEGER PRIMARY KEY
regionName TEXT
dataDate   TEXT
mint       REAL
maxt       REAL
```

## 10. 查詢資料驗證

**使用 SQL 驗證資料**

```sql
SELECT DISTINCT regionName
FROM TemperatureForecasts;

SELECT *
FROM TemperatureForecasts
WHERE regionName = '中部地區';
```

## 11. Streamlit 入門

**快速建立 Web App**

- 安裝環境
- 基本結構
- Hello World

## 12. 從資料庫讀取資料

**使用 SQL 查詢**

```python
import sqlite3

conn = sqlite3.connect("data.db")

# 使用 SQL 從 TemperatureForecasts 查詢資料
# df = pd.read_sql_query(..., conn)
```

## 13. 下拉選單選擇地區

**互動式操作**

- 提供 `Select Region` 下拉選單
- 讓使用者選擇要查看的地區
- 圖中示意包含北部、南部、東北部、東部、東南部等地區

## 14. 繪製折線圖

**一週最高與最低氣溫**

- `MaxT`
- `MinT`
- 顯示一週日期與溫度變化

## 15. 顯示資料表格

**清楚呈現一週資料**

圖中示意：

| Date | MinT | MaxT |
| --- | ---: | ---: |
| 2026-04-14 | 20 | 30 |
| 2026-04-15 | 21 | 31 |
| 2026-04-16 | 22 | 32 |
| 2026-04-17 | 21 | 30 |

## 16. 整合 Web App 介面

**選地區看氣溫預報**

- `Taiwan Weather Forecast`
- 地區選擇
- 氣溫折線圖
- 氣溫資料表格

## 17. 進階：台灣地圖視覺化

**使用 Folium + Streamlit**

- 在台灣地圖上呈現各地區資料
- 顯示區域位置
- 依平均溫度使用不同顏色

圖中平均溫度色階示意：

| 平均溫度 | 顏色 |
| --- | --- |
| `< 20°C` | 藍色 |
| `20–25°C` | 綠色 |
| `25–30°C` | 黃色 |
| `> 30°C` | 紅色 |

## 18. 選擇日期顯示地圖

**互動式天氣地圖**

- `Select Date`
- 依日期切換地圖資料
- 地圖資訊框示意：
  - 中部地區
  - `Min: 20°C`
  - `Max: 30°C`

## 19. 完整成果展示

**Taiwan Weather Dashboard**

整合：

- 台灣互動式地圖
- 氣溫資料
- 地區資訊
- 日期資訊

## 20. 程式碼品質與優化

**更好的程式設計**

- 程式結構清晰
- 錯誤處理機制
- 重複執行不重複插入
- 良好的註解

## 21. 專案上傳至 GitHub

**版本管理與備份**

- 建立 Repository
- 連結 Git（remote）
- Commit & Push

---

# 供參考

> 以下自第 22 項起屬於延伸、回顧與後續探索資訊，標記為「供參考」，不視為前述核心實作流程的一部分。

## 22. 延伸應用與想法【供參考】

**從天氣氣象資料到更多可能**

- 天氣提醒 LINE Bot
- 旅遊行程建議
- 農業 / 防災應用
- 結合 AI 做分析

## 23. 回顧與重點整理【供參考】

**你學到了什麼？**

- API 資料取得
- JSON 資料分析
- SQLite 資料庫
- Streamlit Web App

## 24. 下一步：繼續探索【供參考】

**AI × Data × Real World**

- 更多公開資料 API
- 資料視覺化應用
- AI 輔助開發
- 打造自己的專案作品

---

## 圖中其他宣傳文案【供參考】

> 技術可以解決問題，但更重要的是，用技術創造更好的未來！

- Learn Today, Build Tomorrow
- AI for Learning
- AI for a Better Taiwan
