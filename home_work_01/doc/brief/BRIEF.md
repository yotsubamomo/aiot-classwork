# HW10 Taiwan Weather Forecast — Brief（事前盤點）

- **單元**：`home_work_01/`（老師稱 HW10／Part 5；老師的 repo 稱 AIoT L3 CWA HW1）
- **依據**：[`../requirement/REQUIREMENTS.md`](../requirement/REQUIREMENTS.md)（海報 Part A 與 grill 設計 Part B 的轉寫）、[`../requirement/Taiwan_Weather_Forecast_course_overview.md`](../requirement/Taiwan_Weather_Forecast_course_overview.md)、2026-09-23 與 acceptor 的 grill 裁決
- **狀態**：範圍、資料來源（D2，第 4.6 節）與應用架構（A1–A4，第 5.1 節）皆已於 2026-09-23 簽核。本檔記錄事實與裁決，不是 spec。
- **詞彙**：[`../../CONTEXT.md`](../../CONTEXT.md)

## 1. 來源與地位（acceptor 裁決）

| 來源 | 地位 |
| --- | --- |
| Part A 海報＋課程總覽 §1–21 | **上位契約**（Bindings §2.2）。評分 20／20／20／40，地圖為加分。 |
| Part B grill 設計（Windy／FastAPI／React） | 獨立的設計／參考來源。其**做法**可採用（第 6.7 節）；其架構 React／Next.js、FastAPI、Windy 為 REFERENCE／FUTURE，不擴張目前範圍。Leaflet 因架構簽核成為部署版地圖的繪製函式庫（第 5.1 節），不再列於 REFERENCE。 |
| 課程總覽 §22 以後 | 供參考。 |
| 老師 repo `huanchen1107/AIoT_L3_CWA_HW1` | **IMPORTANT CURRENT REFERENCE**（老師的建議／參考實作）：2026-09-23 發現；與海報有實質差異（第 4.4 節）；不取代也不修改上位契約；此分類為 acceptor 裁決，沒有待老師確認的事項。 |

## 2. 範圍分類（acceptor 裁決 2026-09-23）

| Scope class | 項目 |
| --- | --- |
| **MVM REQUIRED** | CWA 資料（原指定 F-A0010-001；相容性替代 F-D0047-091，第 4.6 節）；JSON 取得與解析；六個地區；一週預報；MinT／MaxT 提取；必要的持久化資料路徑（SQLite `data.db`、`TemperatureForecasts`）；重複執行不重複插入；**本機 Streamlit 評分應用程式 `app.py`** 與 **部署於 Vercel 的 dashboard（Flask＋靜態前端）**，兩者行為對等：地區選擇、六區、七天、MinT／MaxT 折線圖、一週表格、只從 SQLite 查詢、基本錯誤狀態；共用查詢語義；GitHub 交付；**Vercel 公開部署 URL** |
| **ENHANCED REQUIRED**（部署的 dashboard） | 改良的 UI／UX；響應式 dashboard；**Leaflet** Taiwan Map；Select Date；dashboard 整合；自動化測試（涵蓋兩個呈現層）；GitHub Actions CI |
| **OPTIONAL** | 排程更新 CWA 資料；非必要的工程改良 |
| **REFERENCE／FUTURE** | React／Next.js、FastAPI、Windy；課程總覽 §22 以後；老師 repo 的 22 縣市／GIS 架構 |

## 3. 技術裁決與文件證據

對每個被點名的技術，依「評分要求／實作指示／課程流程／範例／使用者可見行為」五類證據分析後的裁決：

| 技術 | 證據摘要 | 裁決 |
| --- | --- | --- |
| **Streamlit** | 40% 項目的標題、學習目標 4、執行步驟 `streamlit run app.py`、套件清單、專案結構、注意事項 2 都點名；只有子配分是行為描述。 | **屬評分契約，維持為必要的評分產物**：`home_work_01/app.py` 是真正的 Streamlit 應用程式，`streamlit run app.py` 維持有效（S1／S3，A1）。因 Vercel 為必要部署目標且無法執行 Streamlit 伺服器，Streamlit 不再是正式部署 runtime——這是相容性安排，不是「Streamlit 從未屬於作業」的主張。不建立為未來專案的通用偏好。 |
| **SQLite** | 30% 配分直接點名；`data.db`、DDL、驗證 SQL 逐字給出；注意事項 2「必須從 SQLite 查詢」。 | **必要技術＋必要資料路徑**；`data.db`、`TemperatureForecasts`、五個欄位名逐字保留；重複安全在 ingestion 實作，不改印出的 DDL（S2）。 |
| **Pandas** | 套件清單與範例；無配分。 | 示範工具；行為（表格資料）才是需求。 |
| **Folium** | 「建議使用 Folium + Streamlit」；地圖無配分。 | 建議而非要求。原 S4 選用 streamlit-folium；**A3 取代**：部署版地圖在瀏覽器以 Leaflet 繪製，本機 Streamlit MVM 不需地圖，Folium／streamlit-folium 不再是必要依賴。 |
| Python | 流程圖、所有指令、所有範例。 | pipeline 語言，不替換。 |
| requests | 主要步驟點名；配分為行為。 | 沿用。 |

## 4. 資料來源盤點（D1／D2）

### 4.1 老師指定

F-A0010-001（一週農業氣象預報）：六大區域、每日 MinT／MaxT、一週。海報範例 URL 截斷於 `datastore/F-A0...`。**此指定保留為原始需求，不因下架而改寫。**

### 4.2 驗證結果（2026-09-23，本專案的 CWA 金鑰，唯讀 GET）

| Endpoint | 無金鑰 | 帶金鑰 |
| --- | --- | --- |
| `api/v1/rest/datastore/F-A0010-001?format=JSON` | 401 "Authorization key is not correct." | **404** `{"message":"Resource not found."}` |
| `fileapi/v1/opendataapi/F-A0010-001?format=JSON` | 401 | **404** `{"message":"Resouce not found."}` |

- 401→404 的變化表示金鑰通過驗證、資源本身不存在。
- data.gov.tw/dataset/9185 標示「資料集已下架，此為歷史資料留存」（本專案直接讀取確認）。
- CWA 公告「7/1 一週農業氣象預報及農業氣象旬報資料下架通知」（2026-06-03）：研究代理回報；CWA 站是 JS 應用，本專案未能直接讀到公告全文——**二手、未逐字驗證**。
- 研究結論：目前沒有任何仍上架的 CWA 產品以六大區域分區提供氣溫預報。

### 4.3 候選替代資料集（研究代理，2026-09-23）

| 資料集 | 名稱 | 層級／粒度 | 溫度欄位 | REST datastore | 狀態 |
| --- | --- | --- | --- | --- | --- |
| **F-D0047-091** | 臺灣各縣市鄉鎮未來1週逐12小時天氣預報 | 22 縣市；12 小時 | `最高溫度`／`最低溫度` | 是 | **上架；本專案已擷取實際回應（第 4.5 節）** |
| F-C0032-005 | 一般天氣預報-一週縣市天氣預報 | 縣市；12 小時 | `MaxT`／`MinT`（舊版 lowercase schema，與海報樹狀圖同形） | 實務上仍回應（2026-09-22 的存檔） | 上架但檔案導向、前景不明；本專案未驗證 |
| F-D0047-089 | 臺灣未來3天天氣預報 | 縣市；3 小時 | 無最高／最低溫 | 是 | 不適用 |
| F-D0047-093 | 全臺灣各鄉鎮市區預報資料 | 鄉鎮 | 有 | 需參數 | 老師 README 記 404 |

### 4.4 老師目前 repo 的做法（`huanchen1107/AIoT_L3_CWA_HW1`，五個 gate 於 2026-09-23 標記 PASS）

| | 海報（上位契約） | 老師 repo |
| --- | --- | --- |
| 資料集 | F-A0010-001 | F-D0047-091（README：workflow 指定 F-D0047-093，404，091 為「已發布的等價 dataset」） |
| 地理 | 六大區域 | 22 縣市，無分區聚合 |
| 要素 | MinT／MaxT | T、MaxT、MinT、Wx、PoP12h |
| 儲存 | SQLite `data.db` | SQLite `data.db` |
| Web App | Streamlit | `server.py`＋`static/`＋`api/index.py`；Leaflet／OpenStreetMap GIS |
| 部署 | 未述 | GitHub＋Vercel serverless |

Repo 未提及 F-A0010-001、六大區域或 Streamlit。所引用的「workflow spec」未在本專案的 `doc/requirement/` 內。

### 4.5 F-D0047-091 實際結構（2026-09-23 擷取；HTTP 200，686 KB；回應內不含金鑰）

```text
success: "true"
result.resource_id: "F-D0047-091"
records.Locations[0]
  .DatasetDescription = "臺灣各縣市鄉鎮未來1週逐12小時天氣預報"
  .LocationsName = "台灣", .Dataid = "D0047-091"
  .Location[]  （22 筆）
     .LocationName, .Geocode, .Latitude, .Longitude
     .WeatherElement[]
        .ElementName ∈ {平均溫度, 最高溫度, 最低溫度, 平均露點溫度, 平均相對濕度, 最高體感溫度,
                       最低體感溫度, 最大舒適度指數, 最小舒適度指數, 風速, 風向, 12小時降雨機率,
                       天氣現象, 紫外線指數, 天氣預報綜合描述}
        .Time[]  （最高溫度／最低溫度各 15 筆，22 個縣市皆同）
           .StartTime / .EndTime  ISO 8601 +08:00；期間只有 06:00–18:00 與 18:00–06:00 兩種
           .ElementValue[0].MaxTemperature 或 .MinTemperature  （字串，例 "26"）
```

- `LocationName` 22 筆：連江縣、金門縣、宜蘭縣、新竹縣、苗栗縣、彰化縣、南投縣、雲林縣、嘉義縣、屏東縣、臺東縣、花蓮縣、澎湖縣、基隆市、新竹市、嘉義市、臺北市、高雄市、新北市、臺中市、臺南市、桃園市（含三個離島縣）。
- 擷取當日 18:00 起算：第一筆是當日 18:00–翌日 06:00，其後 14 筆完整日；以 `StartTime` 日期計有 **8** 個不同日期，其中第一天只有夜間一段。「一週＝7 天」的日界與首日處理是 parser 設計項目，**尚未裁決**。
- 這份回應存於本 session 的 scratchpad；正式 fixture 於 D2 裁決後由實作再擷取。

### 4.6 D2 裁決：六區相容性推導（acceptor 2026-09-23，**CLOSED**）

Acceptor 裁定此相容性決定屬本專案，不需老師確認；產品維持上位契約的六區／七天／MinT–MaxT 行為，不因替代資料集是縣市層級就改成 22 縣市。

```text
F-D0047-091
→ 縣市 12 小時預報值
→ 專案定義的六區推導
→ 七個完整 Forecast Day
→ SQLite TemperatureForecasts
→ 應用程式
```

**推導順序（固定）**

1. 解析 F-D0047-091（結構見 4.5）。
2. 依 **W1** 分組：每個 12 小時期間歸屬其 `StartTime` 的日期 D。Forecast Day D ＝ D 06:00–18:00 ＋ D 18:00–D+1 06:00，是專案的相容性視窗，**不是 00:00–24:00 的曆日**，也不是 CWA 獨立發布的每日 MinT／MaxT。兩段都存在才算完整；擷取開頭只有 18:00–06:00 的那個日期丟棄，保留其後七個完整日期。
3. 每個縣市、每個 Forecast Day：縣市 MinT ＝ 該日各期間 `MinTemperature` 的最小值；縣市 MaxT ＝ 各期間 `MaxTemperature` 的最大值。
4. 每個 Region（**專案定義的相容性對應，不是 CWA 權威分區**）：
   - 北部地區 ＝ 基隆市、臺北市、新北市、桃園市、新竹市、新竹縣、苗栗縣
   - 中部地區 ＝ 臺中市、彰化縣、南投縣、雲林縣、嘉義市、嘉義縣
   - 南部地區 ＝ 臺南市、高雄市、屏東縣
   - 東北部地區 ＝ 宜蘭縣；東部地區 ＝ 花蓮縣；東南部地區 ＝ 臺東縣
   - 澎湖縣、金門縣、連江縣不屬於任何 Region
   Region MinT ＝ 成員縣市 MinT 的算術平均；Region MaxT ＝ 成員縣市 MaxT 的算術平均。
5. 四捨五入到小數一位。
6. 把六區 × 七天的相容性快照寫入 `TemperatureForecasts`。

**驗證要求**：恰好 7 個完整 Forecast Day（逐日檢查兩段都在，不是取前七個標籤）；恰好 6 個 Region；每個保留的 Region／Day 都有 MinT 與 MaxT；產生 Region 值前，其全部成員縣市都必須存在；縣市資料缺漏須明確報錯，不得默默改變平均的分母。

**標示要求**：這些區域值是 **PROJECT-DERIVED COMPATIBILITY VALUES**，技術文件不得寫成 CWA 發布的六區預報；對應表不得寫成 CWA 權威分區（除非另行以 CWA 一手來源驗證）。

**以 2026-09-23 樣本驗算**：W1 得到 24–30 Sep 七個完整日、丟棄 23 Sep；六區 × 7 ＝ 42 列；被拒的替代方案（夜間期間歸屬 `EndTime` 日期；苗栗→中部／嘉義→南部；極值 envelope）對樣本的影響 ≤ 0.6 °C（envelope 使北部兩端各寬約 1 °C），皆記入以供 derivation record 引用。

### 4.7 來源地位摘要

| 層次 | 內容 |
| --- | --- |
| 老師指定 | F-A0010-001（保留為原始需求） |
| 已驗證可用性 | 2026-07-01 下架；2026-09-23 帶金鑰 404（4.2） |
| 核准的相容性替代 | F-D0047-091 ＋ 4.6 的推導規則（acceptor 2026-09-23） |
| 是否仍需老師確認 | **否**（acceptor 裁定為專案內部決定）；老師 repo 只是 IMPORTANT CURRENT REFERENCE |

## 5. 部署與應用架構（2026-09-23 更新）

### 5.1 架構裁決（A1–A4，acceptor 2026-09-23，**CLOSED**）

- **Vercel 是必要的公開部署目標**。原 R1（Streamlit Community Cloud 首選、Render 備援）**撤回**。
- **一個產品、兩個呈現層**（V3）：

  ```text
  ingestion / 推導
      ↓
  data.db
      ↓
  共用的查詢／領域模組
      ├─ 本機 Streamlit 評分應用程式  app.py（streamlit run app.py）
      └─ 部署的 Flask API → 靜態 HTML／JS dashboard（Vercel）
  ```

  SQL／查詢語義與預報業務邏輯只寫一份；本機 Streamlit 應用程式與部署版使用相同的持久化資料與共用查詢邏輯。
- **行為對等**：兩個呈現層都滿足全部 MVM 行為；部署的 dashboard 另加 ENHANCED（改良 UI／UX、響應式、`Select Date`、Leaflet Taiwan Map、Derived Map Temperature），可以更豐富但 MVM 不得更弱。
- **Streamlit 的定位**：仍是必要的評分產物（`app.py`）；不再是正式部署 runtime，此為 Vercel 限制造成的相容性安排（第 3 節）。
- **Flask** 為部署的 Python 應用程式；採與老師已驗證模式（5.2）一致、符合目前 Vercel 支援的最小結構。概念上的檔案配置（`app.py`、`server.py`、`api/index.py`（若需要）、`public/`、`queries.py`、`data.db`）只是概念示意；除老師指定的 `app.py` 外，確切檔名、路由與模組切分由 Design Authority 的 Spec 決定。
- **Python 3.12** 本機、CI、Vercel 一致（Vercel 不提供 3.11）。
- **被評估後拒絕的選項**（研究事實見 5.3）：Streamlit 伺服器部署於 Vercel（不可行）；stlite 靜態（Streamlit 於瀏覽器：約 50 MB、首次載入 10–30 秒、行動裝置差、Folium 未驗證）；Next.js＋sql.js（工具鏈與雙語言成本，UI 優勢非必要）；只做 Flask＋靜態而不保留 Streamlit（放棄海報逐字可對應的評分產物）。
- 已驗證的 Vercel 事實：Python 3.12（預設）／3.13／3.14；entry 檔案的頂層 `app`（Flask／FastAPI）接收全部請求，`public/` 由 CDN 提供；唯讀檔案系統、`/tmp` 可寫、程式旁的檔案自動打包；Hobby 免費、300 秒上限、2 GB、冷啟動約 1.3–2.8 秒、閒置兩週封存；Root Directory 可設 `home_work_01`，其外檔案不可見。SQLite 唯讀讀取：Vercel 文件未提及，以老師 repo 的成功部署為證據。Hobby 是否需信用卡：未驗證。

### 5.2 老師 repo 已驗證的 Vercel 模式（IMPORTANT CURRENT REFERENCE，2026-09-23 直接讀取）

- `server.py`：Flask＋Flask-CORS；`GET /` 回 `static/index.html`，`GET /<path>` 回靜態檔，`GET /api/weather` 回 JSON。
- `data.db` 以唯讀 URI 開啟：`sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)`，路徑為 `os.path.join(BASE_DIR, 'data.db')`，`BASE_DIR` 是程式檔所在目錄——對應 Vercel 的唯讀檔案系統。
- `api/index.py`：把上層目錄加入 `sys.path` 後 `from server import app`；`vercel.json`：`builds: [{src: "api/index.py", use: "@vercel/python"}]`，`routes` 把 `/api/weather` 與 `/(.*)` 都導向 `api/index.py`。
- 即：**單一 Vercel 專案，一個 Python function 同時提供 API 與靜態前端**。

### 5.3 研究事實（2026-09-23；提交前再驗證）

- **Streamlit 伺服器於 Vercel**：不可行——沒有 ASGI／WSGI `app`；WebSocket 在函式時限（Hobby 300 秒）中斷且不保證同一實例；容器須無狀態、閒置五分鐘縮為零。
- **stlite**：仍在維護（1.9.2，2026-09-23；Streamlit 1.62 fork）；純靜態；Pyodide 有 `sqlite3`（需載入）與 pandas；`folium`／`streamlit-folium` 有純 Python wheel 但無公開的 stlite 範例；約 50 MB 首次下載、10–30 秒首次載入、手機明顯較差（社群數據）。
- **Next.js＋SQLite**：`sql.js`（wasm）可靠；原生 `better-sqlite3` 常有相容問題。
- 已撤回的主機（保留作紀錄）：Streamlit Community Cloud（免費、子目錄 entrypoint、`config.toml` 須在 root、12 小時休眠）；Render free（不需信用卡、Root Directory、15 分鐘休眠）。

### 5.4 環境

Python：**3.12**，本機、CI、Vercel 一致（A2；本機須安裝 3.12）。免費方案的限制只作部署備註，不寫成產品需求。

## 6. 其他已裁決的實作前提

1. **資料新鮮度**：MVM 用準備好的 Forecast Snapshot（本機跑 pipeline、commit `data.db`）；排程更新為 OPTIONAL；不把 GitHub Actions 更新、伺服器排程或自動重建資料庫列為必要。
2. **`TemperatureForecasts` 語義**：目前一週預報的快照，不是歷史；重跑 ingestion 不產生重複邏輯紀錄；採與老師 DDL 一致的最簡作法。
3. **路徑處理**：不依賴 process 工作目錄，應用程式檔案相對於原始碼位置解析（概念上 `APP_DIR = Path(__file__).resolve().parent`；`DB_PATH = APP_DIR / "data.db"`），`data.db` 以唯讀方式開啟；`requirements.txt` 與部署設定留在 `home_work_01/`（Vercel 專案 Root Directory 指向該目錄）。原 R1 對 root `.streamlit/config.toml` 的授權隨 R1 撤回而失效；除非架構簽核另有需要，root 不放本單元的部署檔。
4. **UI／UX**（ENHANCED，framework-agnostic 描述）：保留老師可見的概念 `Taiwan Weather Forecast`、`Select Region`、`Select Date`、`Date`、`MinT`、`MaxT` 與中文地區名；清楚的視覺層級、響應式版面、摘要資訊、可互動且易讀的圖表、明確的 loading／empty／error 狀態、375 px 寬不出現不必要的橫向捲動。UI/UX Pro Max 只是設計／實作階段的輔助。
5. **Taiwan Map 的溫度**：`derived_map_temperature = (MinT + MaxT) / 2`，顯示到小數一位；色帶 `< 20` 藍、`20 – < 25` 綠、`25 – < 30` 黃、`≥ 30` 紅；文件必須說明它是由預報 MinT／MaxT **導出**，不是觀測日均溫。
6. **測試與 CI**（ENHANCED）：GitHub Actions 每次 push 跑自動化測試，涵蓋兩個呈現層——pytest（ingestion、D2 推導與驗證、SQLite、共用查詢層）、Streamlit `AppTest`（本機評分應用程式）、Flask test client（部署 API 行為）；瀏覽器／UI 測試只在 ENHANCED UI 驗收條件需要時採用。部署 smoke test 與 push CI 分開：本機／手動、`workflow_dispatch`、部署 URL 存 repository variable、最多 90 秒暖機重試、檢查公開根路徑與 Flask 健康 endpoint（例如 `GET /api/health`，確切路徑由 Spec 決定）。Streamlit Community Cloud 專屬的 `/_stcore/health` 檢查已撤回。
7. **採用的 Part B 做法**：金鑰只在伺服器端且不進 git；`.env.example`；可設定的無效值解析；頁面顯示最後更新時間；明確的 stale／empty／error 訊息；客觀的驗收清單。
8. **憑證**：CWA 金鑰在未追蹤的 `home_work_01/.env`（已確認被 `.gitignore:11` 忽略）；`home_work_01/.env.example` 只有變數名。Windy 憑證不在目前實作內。原 `backend/`、`frontend/` 目錄（只含 `.env`）已刪除。
9. **GitHub 交付**：從本 public monorepo 部署；資料夾維持 `home_work_01`，README 說明與老師 `HW10_Weather/` 結構的對應。

## 7. 待辦

| # | 事項 | 負責 |
| --- | --- | --- |
| 1 | 治理採用前置作業：合併 bindings PR、重開載入 `gov-*` definitions 的 session、binding dry-run | acceptor |
| 2 | 接受 Outcome Contract（[`../governance/outcome-contract.md`](../governance/outcome-contract.md)） | acceptor |
| 3 | Design Authority derive Spec 與 Tickets（Formal lane） | `gov-design-authority` |
| 4 | 本機安裝 Python 3.12 | acceptor |
