# Audit record — Issue #19，cycle 1，R1

| 欄位 | 內容 |
| --- | --- |
| Work Contract | GitHub Issue #19（`yotsubamomo/aiot-classwork`）「共用查詢／領域模組與 Grading App（app.py）：Select Region、一週折線圖與表格」，Scope class MVM。所屬 Spec 是 `home_work_01/doc/spec/SPEC.md` v1.1（EFFECTIVE），Outcome Contract 是 `home_work_01/doc/governance/outcome-contract.md`（ACCEPTED 2026-09-23）。依據的裁決：`decision-20260923-spec-interpretation-rulings.md` DR-1、DR-2、DR-4、DR-8、DR-9、DR-11、DR-15；`decision-20260924-ingestion-timestamp-semantics.md` DR-17；`decision-20260923-high-risk-categories.md` H-1、H-2、H-3、A-1；`decision-20260924-unattended-run-policy.md` N-17、N-18 |
| 受審 subject | branch `home_work_01-hw10-implementation`，commit `353c8a7b1e72ae69005999ed13546e653198f4c3`；BASE `bbc82cd`；審查範圍 `bbc82cd..353c8a7`，共 8 個檔案，全部在 `home_work_01/` 內 |
| Audit 種類 | **R1**（對 accepted work scope 做完整的 independent audit），**cycle 1** |
| 角色 | `primary_reviewer`（definition `gov-primary-reviewer`；Bindings §3.1 mapping 為 `claude-opus-5-5`／`xhigh`） |
| Binding 證據 | 由派工者（Orchestrator）依 Bindings §3.4 核對，記在 run record `home_work_01/doc/governance/run/run-20260924-hw01-formal.md`。同一份 run record 記載的 Executor binding：agent `aa2d2cfcba2d60320` = `gov-executor`／`claude-opus-4-8`／`high`。Executor 與 Primary Reviewer mapping 是不同模型，因此沒有記 `diversity_lost`。 |
| Independence（治理 §2.3） | (1) 以 fresh context 派工，沒有繼承 Executor 的對話。worklog 與 Executor 的敘述一律視為待驗證主張。(2) Binding 見上一列。(3) 自主取得：自行讀取 Ticket 本文（`gh issue view 19`、`gh issue view 25`）、Spec、Outcome Contract、derivation record、各項裁決、上位契約 `REQUIREMENTS.md`、`CONTEXT.md`、#18 的 R1 record、git 歷史與 diff，以及全部實作與測試檔；測試與檢查都由 Reviewer 自己執行。(4) 本紀錄由 Reviewer 用自己的 Write 工具寫入。 |
| 日期 | 2026-09-24 |

## 1. 審查方法與環境

- **確認 subject**：`git rev-parse HEAD` = `353c8a7b…`。`git diff 353c8a7 --stat -- home_work_01` 只列出 `doc/governance/run/run-20260924-hw01-formal.md`，這是 Orchestrator 在 record-only path 上的修改（Bindings §7），不影響 subject identity。`git diff --cached` 為空。變更路徑全部在 `home_work_01/` 內，沒有觸及 RB-5。
- **離線執行**：用 `git archive 353c8a7 home_work_01` 匯出到 Reviewer 的 scratchpad，匯出的樹裡**沒有** `.env`。以單元 `.venv` 執行，版本為 Python 3.12.14、streamlit 1.64.0、pandas 3.0.6、pytest 8.3.3。另外用 `sitecustomize` 封鎖所有非 loopback 的 `connect` 與 `getaddrinfo`，並把 `HTTP(S)_PROXY` 指向無效位址（已確認連線 `opendata.cwa.gov.tw` 會被擋下）。
- **`pytest -v -p no:cacheprovider`**：**104 passed**。其中 #18 的測試 60 個，本票新增 44 個（`test_weather_query.py` 27、`test_app.py` 8、`test_static_checks.py` 9）。
- **Reviewer 自己做的獨立檢查**（都放在 scratchpad，不進 repo）：
  - 在單元目錄以 `python -m streamlit run app.py --server.headless true --server.port 8799` 實際啟動伺服器。`GET /` 回 200，`GET /_stcore/health` 回 200 `ok`。接著以 headless Chrome 透過 DevTools Protocol 建立真實的瀏覽器 session 並截圖（`ac01_home.png`、`ac03_dropdown.png`、`ac03_region.png`），再從 DOM 讀取標題、下拉選項、`stException` 的數量、圖表數與小標題。三次 session 結束後，server log 沒有任何例外。
  - 用 `AppTest` 逐一選擇六個 Region：每個都比對表格與 `data.db`，並解開 chart 的 Arrow 資料集核對點數與日期，也列出畫面上所有元素的類型。
  - 邊界資料庫探測，共 12 種：零位元組檔、非 SQLite 檔、目錄、沒有 forecast 表、空表且沒有 metadata、缺欄位的 schema、預設 Region 整區缺漏、43 列、42 列但天數分布為 8/6、42 列但某區日期錯位、數值欄存文字、沒有 metadata 列。
  - 路徑字元探測，共 7 種：空白、中文、`#`、`%20`、`%`、`;`、`&`。
  - Derived Map Temperature 暴力比對：-5.0～45.0 範圍內所有一位小數的組合，共 125,751 組，逐一與以分數精確計算的 half-up 值及色帶比較。
  - **Mutation probes**：先做 18 個 mutant，涵蓋 half-even 捨入、以原始平均值分帶、Region 排序、DESC 排序、時間不取自 DB、拿掉 missing 分支、拿掉 null 檢查、非唯讀開啟、以 CWD 為基準的相對路徑、欄位對調、只畫 MaxT、incomplete 時不警告、表格只剩 6 列、改動標題、在 app 內放 SQL、import requests、forecast_days 改 DESC、拿掉 empty 分支。**18 個全部被測試抓到。** 再做 5 個補充 mutant，涵蓋 `st.map`、`st.date_input`、以字串串接組出 `Select Date`、`from urllib import request`、以字串串接組出 CWA URL。**5 個全部沒有被抓到**，見 F-4、F-5。
  - H-1 掃描：在程序內讀取被忽略的 `.env` 取得字面金鑰，**只輸出次數，不輸出任何金鑰內容**。另用 CWA 金鑰格式（`CWA-` 加上 8-4-4-4-12 hex）掃描。範圍：`bbc82cd..353c8a7` diff、commit message、`353c8a7` 樹內全部 430 個追蹤檔案。
  - 完成後：以 `taskkill` 停止 Reviewer 自己啟動的 server。`git status` 與開始時相同。

## 2. Acceptance criteria 與需求逐條判定

| 項目 | 判定 | 證據 |
| --- | --- | --- |
| AC-01 | **行為 PASS／證據不完整（F-3，blocking）** | Reviewer 在單元目錄以 `streamlit run app.py`（只加 headless 與 port 參數）啟動，伺服器正常起來。真實 Chrome session 渲染出首頁，`stException` 數量為 0，server log 也沒有例外（截圖 `ac01_home.png`）。不需要額外參數，也不需要從其他目錄啟動。但契約要求的**截圖**證據不存在，而且 worklog 以不存在的「Ticket AC-01 註記」為依據改用其他證據代替，見 F-3。 |
| AC-02（GA） | **PASS**（截圖證據見 F-3） | `test_app.py:56-73`：`at.title` 恰為 `['Taiwan Weather Forecast']`；`Select Region` 的 options 與 DR-8 順序逐字相同，預設值為 `北部地區`。Reviewer 在真實瀏覽器展開下拉選單，DOM 的 `role=option` 依序為北部地區、中部地區、南部地區、東北部地區、東部地區、東南部地區（`ac03_dropdown.png`）。 |
| AC-03（GA） | **PASS**（Low：F-6） | `test_app.py:79-113` 驗了中部地區與東南部地區：表格欄位恰為 `Date/MinT/MaxT`、7 列、升序，值等於直接查 `data.db` 的結果；chart 的 color domain 為 `[MaxT, MinT]`，x field 為 `Date`。Reviewer 另外對**六個** Region 都驗過：表格等於 `data.db`；chart 資料集有 14 點，是 7 個日期 × {MaxT, MinT}，數值與表格相同。真實瀏覽器切到東南部地區後，小標題為 `Temperature Forecast – 東南部地區`，圖與表同步更新（`ac03_region.png`）。 |
| AC-04（Python 側 a/c/d） | **PASS**（Medium non-blocking：F-4） | (a) 以 AST 列出 import：`app.py` 為 `pathlib`、`pandas`、`streamlit`、`weather_query`；`weather_query.py` 為 `sqlite3`、`dataclasses`、`decimal`、`enum`、`pathlib`、`typing`，都不是 HTTP client。grep `opendata`、`CWA_API_KEY`、`environ`、`getenv`、`.env` 在兩個檔案中都是 0 筆。(c) SQL 只出現在 `weather_query.py`（`:161`、`:188`、`:240`、`:269`、`:305`、`:334`、`:360`），`app.py` 裡 0 筆，mutant M15 被抓到。(d) `app.py:27` import `weather_query`，而且沒有 import `sqlite3`。靜態檢查會漏掉 `from urllib import request` 這種寫法（mutant N4 沒被抓到），見 F-4。 |
| AC-10（GA） | **三個列舉情境 PASS；錯位快照 FAIL（F-1，blocking）** | `test_app.py:130-150` 以替代路徑測試：不存在 → `st.error` 且訊息含 `data.db`；只有表沒有列 → `st.error`；41 列 → `st.warning`；三者都沒有例外。mutant M6、M12、M18 都被抓到。但如果快照是 42 列、六區各 7 天、**日期卻彼此錯位**，狀態會被判為 `ok`，頁面不顯示警告（F-1）。 |
| AC-24（GA） | **PASS** | `test_app.py:119-124`：caption 含 `IngestionMetadata.ingestedAt`。Reviewer 在 AppTest 與真實瀏覽器看到的都是 `Last updated (data fetched from CWA): 2026-09-24T02:24:50+08:00`，與 `SELECT * FROM IngestionMetadata` 的 `(1, '2026-09-24T02:24:50+08:00', 'F-D0047-091')` 逐字相同。標籤寫的是「資料從 CWA 取得」，沒有寫成發布時間或頁面載入時間，符合 DR-17 §4.5。`TemperatureForecasts` DDL 沒有變動：`data.db` 的 blob 在 BASE、subject、工作樹與 Reviewer 多次讀取之後都是 `687586991ce3…`。唯讀開啟之後也沒有產生 journal 或 WAL 檔。mutant M5 被抓到。 |
| AC-26 | **PASS**（Low：F-5） | `app.py` 與 `weather_query.py` 裡沒有地圖繪製，沒有 `Select Date` 控制項，也沒有 folium 或 streamlit-folium（grep 與 AST 都確認過；相關字樣只出現在 docstring）。AppTest 的畫面元素只有 title、caption、selectbox、subheader、vega_lite_chart、dataframe。`requirements.txt` 不含 folium 子字串（`test_static_checks.py:166-175`）。自動化檢查只涵蓋 folium 與字面 `Select Date`，見 F-5。`weather_query.py` 內的 Derived Map Temperature 是 R-SHR-4 規定要放在共用模組的計算，Grading App 沒有呼叫也沒有呈現它，因此不違反 AC-26 與 INV-9。 |
| AC-28（Python 側） | **PASS** | `test_weather_query.py:260-274` 的五組案例由 Reviewer 重新執行：22.7／green、20.0／green、25.0／yellow、30.0／red、19.9／blue。暴力比對 125,751 組結果 0 不符。Python 內建的 `round(22.65, 1)` 會得到 `22.6`，因此這組測試確實能抓到 banker's rounding；mutant M1（half-even）與 M2（以原始平均值分帶）都被抓到。 |
| AC-27（本票範圍，R-DOC-5） | **PASS**（Low：F-7、F-10） | (1) 模組 docstring：`weather_query.py:1-28`、`app.py:1-18`；主要函式都有 docstring。(2) missing、empty、incomplete 都有明確訊息，訊息也說明如何產生資料（`app.py:36-50`）；非 SQLite 檔與 schema 錯誤會拋出未處理例外，見 F-7。(3) 沒有未使用的 import。`day_values`、`forecast_days`、`colour_band` 是 R-SHR-2(d)(e) 與 R-SHR-4 規定的共用語義，而且有測試，不算死碼。`pandas` 被直接 import 卻沒有列入相依，見 F-10。(4) 結構為共用查詢模組加上呈現層，與資料流一致。 |
| R-SHR-2 | **(b)～(f) PASS；(a) 見 F-1** | 六項語義各有測試（`test_weather_query.py:92-222`）。(b) 是模組常數，不依賴 SQL 排序；(c) 與 (e) 升序；(d) 依標準順序並附 Derived Map Temperature 與色帶；(f) 原樣回傳。mutant M3、M4、M7、M17 都被抓到。 |
| R-SHR-3 | **唯讀與可覆寫 PASS；以原始碼位置為基準的解析見 F-2** | 唯讀：`?mode=ro` 下執行 `DELETE` 會得到 `OperationalError`（M8 被抓到）。預設路徑是 `<module dir>/data.db`（`:42-43`），與 CWD 無關（M9 被抓到）；每個入口都接受 `db_path`。但 URI 是用字串直接串出來的，路徑含 `#` 或 `%XX` 時會解析到錯誤的檔案，見 F-2。 |
| R-SHR-5（Python 側）／INV-6 | **PASS** | 見 AC-04(a)。 |
| R-GA-1～R-GA-3、R-GA-5、R-GA-6、R-GA-8、R-GA-9 | **PASS** | 見上方各 AC。R-GA-3 的 SHOULD（預設選第一個 Region）也有達成。 |
| R-GA-4 | **PASS**（SHOULD 全部達成；Low：F-9） | 兩條線 `MaxT`、`MinT`，X 軸為 7 個日期，標題 `Date`。SHOULD 項目：小標題為 `Temperature Forecast – <Region>`（en dash），MaxT 為 `#d62728` 紅、MinT 為 `#1f77b4` 藍。Y 軸沒有標題也沒有單位，見 F-9。 |
| R-GA-7 | **缺失、空表、41 列 PASS；錯位快照見 F-1** | 見 AC-10。 |
| R-TC-1（共用模組）、R-TC-3、R-TC-5 | **PASS** | 見 §1。在網路封鎖、沒有 `.env` 的環境下 104 個測試全部通過。 |
| R-DOC-1（Grading App 段）、R-DOC-2（Streamlit 定位） | **PASS** | README `:164-198`。「required grading artefact」、「not the deployed runtime」、「compatibility accommodation forced by that hosting constraint, not a sign that Streamlit was outside the assignment」，與 OC §2.4（`outcome-contract.md:51`）一致。README `:3` 的措辭問題已由 #18 的 F-11 指派給 #25，不重開。 |
| INV-1（Python 側） | **PASS**（Low：F-8） | 讀取端的 SQL 只在 `weather_query.py`，`app.py` 只呼叫它。寫入端的 SQL 在 `ingestion/persist.py`（#18 已結案），這與 OC §2.4 的架構一致：「ingestion／推導 → `data.db` → 共用的查詢／領域模組」。R-SHR-1 所說的「全部 SQL」，就呈現層的資料來源而言成立，不需要 routing。 |
| INV-2（Grading App 基準） | **PASS**（觀察 O-2） | 六個 Region 的 `(Date, MinT, MaxT)` 都等於 `data.db`。 |
| INV-4 | **PASS** | `app.py` 位於單元根目錄；`streamlit run app.py` 可用；頁面文字 `Taiwan Weather Forecast`、`Select Region`、`Date`、`MinT`、`MaxT`、線名 `MaxT`／`MinT` 與六個 Region 名逐字相同；`data.db` 與 DDL 都沒有變動。 |
| INV-9 | **PASS** | 見 AC-26。 |
| #18 F-10（owner #19） | **已解決** | `requirements.txt` 已不含 `folium` 子字串（grep 0 筆）；`test_requirements_does_not_list_folium` 同時檢查「沒有列為相依」與「全檔沒有這個子字串」兩層。 |

## 3. 高風險類別核對（decision-20260923-high-risk-categories A-1）

### H-1 憑證與機密：觸及（本票以靜態檢查涵蓋）

- **核對內容**：以 AST 列出 `app.py` 與 `weather_query.py` 的 import（兩者都沒有 HTTP client，見 AC-04）；掃描兩者的全部字串常值（沒有 CWA URL，也沒有 `CWA_API_KEY`）；兩者都不讀 `.env` 或環境變數；以字面金鑰（從被忽略的 `.env` 在程序內取得，只輸出次數）與 CWA 金鑰格式，掃描 `bbc82cd..353c8a7` diff、commit message 與 `353c8a7` 樹內 430 個追蹤檔案；`git ls-files` 是否含 `.env`；頁面上是否出現任何秘密資訊。
- **結果**：字面金鑰 0 筆，金鑰格式 0 筆，沒有追蹤任何 `.env`，頁面只顯示公開資料與取得時間。**H-1 沒有 blocking。** 靜態檢查的強度問題見 F-4（Medium，non-blocking，owner #20）。

### H-2 老師指定的介面或資料格式：觸及

- **核對內容**：`app.py` 位於單元根目錄；在單元目錄執行 `streamlit run app.py` 不需額外參數即可啟動（Reviewer 實跑並用真實瀏覽器渲染）；頁面文字 `Taiwan Weather Forecast`、`Select Region`、`Date`、`MinT`、`MaxT`、線名與六個 Region 名逐字相同（AppTest 與瀏覽器 DOM）；`data.db` 的 blob 在本票與 app 讀取之後都沒有變（`687586991ce3…`），DDL 與 `IngestionMetadata` 未被改動；唯讀開啟；`requirements.txt` 與 README 都存在。
- **結果**：名稱、文字與格式全部符合。但有兩項 H-2 範圍內的 blocking：**F-2**（老師的 clone 路徑含 `#` 或 `%XX` 時，Grading App 會把存在的 `data.db` 誤報為「not found」，評分產物因此失效）；**F-3**（AB-2／AC-01 要求的截圖證據缺失，AC-01 在 H-2 對應的 Spec 清單內）。

### H-3 資料語義與標示：觸及

- **核對內容**：Derived Map Temperature 與色帶只定義在共用模組（`weather_query.py:111-141`），用 `Decimal` 的 `ROUND_HALF_UP`，並依**顯示值**分帶（AC-28 五組案例加暴力比對，mutant M1、M2）；Region 順序是模組常數（DR-8，M3）；讀取端的 6 × 7 快照判定（`_classify_rows`，`:198-213`）；取得時間標籤依 DR-17 §4.5；README 的 Streamlit 定位敘述沒有把推導值寫成 CWA 發布的值。
- **結果**：計算與標示都符合。**Blocking：F-1**：讀取端的 6 × 7 判定沒有檢查六區是否共用同一組七天，錯位的快照會被判為 `ok`。這違反 R-SHR-2(a) 的「當且僅當」定義，並會直接傳到 #20 的 `/api/health`。

## 4. Findings

### F-1：`snapshot_status` 把六區日期彼此錯位的 42 列快照判為 `ok`

- **Severity**：Medium　**Blocking**：**是**
- **契約依據**：
  - Spec R-SHR-2(a)（`SPEC.md:163`）：「ok **當且僅當**恰 6 Region × 7 日且每格有值」。
  - DR-9（`decision-20260923-spec-interpretation-rulings.md:77-83`）：「資料表存在但不是 6 × 7（例如手動改動）… 共用模組回報 `incomplete`；Grading App 顯示警告」。
  - `CONTEXT.md:84-86` 對 Forecast Snapshot 的定義：「exactly six Regions × seven complete Forecast Days」。
  - R-GA-7（`SPEC.md:178`）、AC-10（`SPEC.md:261`）：不完整時 MUST 顯示警告。
  - 本票 AC「R-SHR-2：六項語義各有測試（狀態四種…）」。
  - 下游影響：R-DS-2 與 AC-16（`SPEC.md:267`）把「不完整仍回 ok」列為 FAIL 例；依 INV-1，#20 必須使用這個狀態語義。
  - H-3 的涵蓋項目包含「6 × 7 驗證」。
- **證據**：
  - `weather_query.py:198-213` 的 `_classify_rows` 只檢查四件事：列數 = 42、沒有 null、Region 集合等於六個標準名稱、每個 Region 各有 7 個**不同**的日期。它沒有檢查六區共用**同一組** 7 個 Forecast Day。
  - Reviewer 從提交的 `data.db` 複製出 `shift.db`，把 `東部地區` 的 `dataDate` 全部加 30 天。結果：42 列、`count(DISTINCT dataDate)` = 14、`snapshot_status` = **`ok`**；`forecast_days` 回傳 **14** 天；`day_values('2026-09-24')` 只有 5 個 Region，`day_values('2026-10-30')` 只有 1 個。AppTest 對這份資料庫沒有顯示任何警告（`warn=[]`）。
  - 現有的 incomplete 測試（`test_weather_query.py:106-131`、`test_app.py:145-150`）都沒有涵蓋這種錯位。
  - 正常的 ingestion 會保證整格寫入（R-DER-7、INV-3），所以這種狀態只會來自人為改動或日後的寫入端缺陷。DR-9 明文把「人為改動」納入這個狀態的語義範圍。
- **需要的修正（不指定做法）**：`ok` 必須要求六區共用同一組恰好 7 個 Forecast Day，每一格恰有一組值；其他情況一律判為 `incomplete`。另外補上對應的自動化測試（共用模組層與 AppTest 的警告各一）。

### F-2：唯讀 URI 以字串直接串接、沒有做 percent-encoding，路徑含 `#` 或 `%XX` 時會把存在的 `data.db` 判成 missing

- **Severity**：Medium　**Blocking**：**是**
- **契約依據**：
  - R-SHR-3（`SPEC.md:164`）：以唯讀方式開啟，「路徑相對於原始碼位置解析（不依賴 process 工作目錄）」。
  - R-GA-1 與 OC AB-2（`outcome-contract.md:70`）：老師在本機依 README 步驟以 `streamlit run app.py` 啟動。AB-3、AB-4 的畫面行為也在老師的環境中評分。
  - R-GA-7：`data.db` 不存在時才應顯示「缺失」訊息。這裡的訊息是錯的：檔案其實存在。
  - H-2：評分直接依賴的介面失效。
- **證據**：
  - `weather_query.py:153`：`uri = "file:" + Path(db_path).as_posix() + "?mode=ro"`。SQLite 的 URI 解析會把 `#` 當成 fragment 的開頭，並把 `%XX` 解碼。
  - 路徑字元探測（把提交的 `data.db` 分別複製到七種目錄）：空白、中文、`%`、`;`、`&` 都是 `ok`；**`hash#dir` 與 `pct%20dir` 都是 `missing`**。
  - 端到端重現：把匯出的單元複製到 `…/C#course/home_work_01/`，此時 `Path("data.db").exists()` 為 True，但 `AppTest.from_file("app.py")` 顯示 `The forecast database data.db was not found…`，沒有下拉選單也沒有表格。在同一個位置執行本票的測試，得到 **8 failed, 27 passed**。
  - 寫入端（`ingestion/persist.py`）使用 `sqlite3.connect(str(path))`，不受這個問題影響。所以在這種路徑下 ingestion 會成功，Grading App 卻說找不到檔案。
- **需要的修正（不指定做法）**：對任何合法的檔案路徑，都要正確解析並以唯讀方式開啟（例如在組 URI 之前做正確的編碼）。另外補上會涵蓋這類路徑字元的自動化測試。

### F-3：AC-01／AB-2（以及本票 AC-02）要求的截圖證據缺失；worklog 以不存在的 Ticket 註記為由改用其他證據，並聲稱環境無法擷取畫面

- **Severity**：Medium　**Blocking**：**是**
- **契約依據**：
  - Outcome Contract AB-2（`outcome-contract.md:70`）的證據欄：「worklog 紀錄＋**截圖**」；AB-3（`:71`）的證據欄包含「截圖」。
  - Spec AC-01（`SPEC.md:252`）的證據欄：「worklog 記錄指令與輸出；**截圖**」；AC-02（`:253`）包含「瀏覽器截圖」。
  - Ticket #19 AC-01 寫的是「（worklog＋截圖）」，AC-02 寫的是「（截圖）」，**沒有**任何可以改用其他證據的註記。
  - `decision-20260924-unattended-run-policy.md` N-17（`:67`）：截圖「由 **Executor** 以瀏覽器（含 headless 瀏覽器工具）操作與截圖」；N-18（`:68`）：AC-01 由 Executor 在本機執行。
  - Implementation Profile §5（`implementation-profile-impl-default-v2.md:103-107`）：「An implementation MUST NOT obtain a passing result by weakening the accepted verification」；「例外必須有 accepted contract／authorized decision 的有效依據；Executor 自寫理由不等於授權」。
  - 分配：derivation record §11.1 與 §11.2（`derivation-SPEC.md:159`、`:195`）把 AC-01 與 AB-2 **只**分配給 #19。#25 只重驗 AC-02、03、04、07、10、19、24，並在驗收文件中「引用」證據（Issue #25 本文），不會產生 AC-01 的截圖。
- **證據**：
  - `worklog/issue-19.md:58`：「截圖：本環境無法擷取瀏覽器畫面；依 Ticket AC-01 註記，以 `AppTest`…＋ headless boot…作為 AC-01 證據，實機截圖留待後續人工驗證補充」。`:81` 把它列為「後續人工補充項」，但沒有 owner。
  - 對照 `gh issue view 19`：AC-01 那一行沒有這樣的註記。
  - **這個環境可以擷取畫面**：Reviewer 在同一台機器上以已安裝的 Chrome 153（headless，透過 DevTools Protocol）連上 `streamlit run app.py` 的伺服器，成功擷取首頁、下拉選單與切換 Region 後的畫面。
  - worklog V-3（`:52`）只是摘要（「GET / → 200…boot log 無 traceback」），沒有附上指令輸出；它引用的 boot log 在 Executor 的 scratchpad，不在 repo 也不在 worklog。只 `GET /` 取得靜態 `index.html` 並不會執行腳本；「首頁渲染無例外」是靠 AppTest 在同一個 process 內執行推得的。
  - Reviewer 已確認 AC-01 的**行為**成立（見 §2）。這項 finding 針對的是契約要求的證據沒有產生，以及沒有授權就改用其他證據。
- **需要的修正（不指定做法）**：由 Executor 產生 AC-01 的截圖（在單元目錄以 `streamlit run app.py` 啟動後的首頁）與 AC-02 的截圖（`Select Region` 的六個選項），存放位置與引用方式屬於 HOW，只要之後的驗收文件能引用即可；截圖不得含金鑰。worklog 要記錄實際的指令與輸出，並更正「依 Ticket AC-01 註記」這個錯誤引用。

### F-4：AC-04(a) 的 HTTP client 靜態檢查漏掉 `from urllib import request` 與 `from http import client`

- **Severity**：Medium　**Blocking**：否（明確歸類：目前的 subject 符合，受影響的是回歸保護的強度）
- **契約依據**：AC-04(a)：「自動化靜態檢查通過：… 不 import 任何 HTTP client（`requests`、`httpx`、`urllib.request`、`aiohttp` 等）」；R-SHR-5；INV-6；本票的 H-1 以靜態檢查涵蓋。
- **證據**：`test_static_checks.py:59-67` 對 `ImportFrom` 只記錄 `node.module`，也就是 `urllib` 或 `http`；而 `:39-40` 的比對集合是 `{"urllib.request", "http.client"}` 加上 roots `{"requests", "httpx", "aiohttp", "urllib3"}`。在 `app.py` 加入 `from urllib import request as _r` 之後，44 個測試全部通過（mutant N4 沒被抓到）。目前兩個檔案都沒有這種 import（見 AC-04）。
- **Disposition**：Owner **#20**。#20 負責完整的 AC-04，要把檢查擴大到 Flask 後端，屆時一併補強，例如也比對 `ImportFrom` 的 `module + "." + name`。

### F-5：AC-26 的「不含地圖／`Select Date`」自動化證據只涵蓋 folium 與字面的 `Select Date`

- **Severity**：Low　**Blocking**：否
- **契約依據**：AC-26（`SPEC.md:277`）：「`app.py` 及其 import 不含地圖、`Select Date`…」，證據為「靜態檢查；`AppTest`」。
- **證據**：在 `app.py` 加入 `st.map(...)`（N1）或 `st.date_input(...)`（N2），44 個測試仍全部通過；AppTest 沒有斷言「沒有地圖或日期元素」。Reviewer 已確認目前的 subject 沒有這類元素（元素清單見 §2 AC-26）。
- **Disposition**：Owner **#25**（INV-9 最終核對）。#19 也可以選擇補上 AppTest 的元素清單斷言，或檢查 `st.map`、`pydeck`、`date_input`。

### F-6：AC-03 的測試沒有斷言圖表本身有七個日期

- **Severity**：Low　**Blocking**：否
- **契約依據**：AC-03：「折線圖有 `MaxT`、`MinT` 兩條線、**七個日期**」。
- **證據**：`test_app.py:103-113` 只斷言 color domain、顏色與 x field，然後以「與表格同源」推論七日。Reviewer 解開 chart 的 Arrow 資料集，六個 Region 都是 14 點（7 個日期 × 2 條線），而且數值等於表格。
- **Disposition**：Owner **#25**（重驗 AC-03）。

### F-7：非 SQLite 檔與 schema 錯誤會以未處理例外呈現；零位元組檔被說成「not found」

- **Severity**：Low　**Blocking**：否
- **契約依據**：R-DOC-5「錯誤有處理與明確訊息」。這些情境不在 AC-10 列舉的三種狀態之內。
- **證據**：`data.db` 是非 SQLite 內容時，`weather_query.py:160` 拋出 `sqlite3.DatabaseError: file is not a database`；`TemperatureForecasts` 缺少 `maxt` 欄位時，`:187` 拋出 `OperationalError: no such column: maxt`。兩者 AppTest 的 `at.exception` 都不是空的。零位元組的 `data.db` 被判為 `missing`，訊息寫「was not found」，但檔案其實存在。三者都不會寫入資料。
- **Disposition**：Owner：#19 Executor（可選）；#25 做 AC-27 最終核對時再看。

### F-8：`REGION_ORDER` 在 `ingestion/config.py` 與 `weather_query.py` 各定義一份，沒有測試確保兩者一致

- **Severity**：Low　**Blocking**：否
- **契約依據**：INV-1（查詢語義只有一份）、DR-8（兩層一致）。
- **證據**：`ingestion/config.py:27-37` 與 `weather_query.py:51-58`。分成兩份有合理理由：`ingestion/config.py:16-21` 含有 CWA URL 與 `CWA_API_KEY` 名稱，讀取端若 import 它，就會違反 R-SHR-5（檔案不得含這些字串）。兩份目前逐字相同。日後若不一致，狀態會變成 `incomplete` 並顯示警告，屬於 fail-safe，但沒有測試能及早發現。
- **Disposition**：Owner **#25**（INV-1 最終核對），可以加一個比對兩份清單的測試（只在測試中 import `ingestion.config`）。

### F-9：Y 軸沒有標題與單位

- **Severity**：Low　**Blocking**：否
- **契約依據**：R-GA-4 寫「Y 軸為溫度（°C）」。上位契約 A.4 的畫面範例是「Y 軸 `Temperature (°C)`」（`REQUIREMENTS.md:159`）。
- **證據**：vega-lite spec 中 y encoding 的 `"title": ""`，截圖上的 Y 軸只有刻度。
- **判斷**：Spec 對老師指定的可見字樣一律加反引號（例如 `MaxT`、`Select Region`），但「溫度（°C）」沒有加；DR-15 也把 A.4 畫面範例的細節定為範例層級。因此 Reviewer 把 R-GA-4 讀為「Y 軸呈現的是 °C 溫度值」，在資料層面已經成立，契約的語義是足夠的，不需要 routing。加上 `Temperature (°C)` 標題成本很低，而且更接近老師的範例。
- **Disposition**：Owner：#19 Executor（可選）。

### F-10：`app.py` 直接 import `pandas`，但 `requirements.txt` 沒有宣告也沒有固定它的版本

- **Severity**：Low　**Blocking**：否
- **契約依據**：R-ENV-1「相依 SHOULD 固定版本」；R-DOC-5。
- **證據**：`app.py:24` 有 `import pandas as pd`；`requirements.txt` 只列 `requests`、`pytest`、`streamlit`。pandas 是 streamlit 的間接相依（目前 `.venv` 裡是 3.0.6），全新安裝時可能取得不同版本。
- **Disposition**：Owner：#19 Executor（可選）或 #21（處理部署相依時一併整理，見 O-3）。

### F-11：worklog 的測試數量有誤

- **Severity**：Low　**Blocking**：否
- **契約依據**：治理 §3.7（worklog 必須如實）。
- **證據**：`worklog/issue-19.md:50` 寫「#18 的 66 例 ＋ 本票新增 44 例」，但 #18 的測試檔實際收集到 60 個（`pytest --collect-only`），60 + 44 = 104。
- **Disposition**：Owner：#19 Executor，在處理 F-3 更新 worklog 時一併更正。

## 5. 觀察（不是 finding）

- **O-1（INV-1 的讀法）**：寫入端的 SQL 在 `ingestion/`，讀取端的 SQL 在 `weather_query.py`。這符合 OC §2.4 的分層與 Spec Solution 的資料流圖，所以不 route。
- **O-2（給 #20 與 Spec Integration Audit，INV-2）**：Grading App 的表格用 Streamlit 預設格式顯示浮點數，整數值不顯示小數，例如 `31.0` 顯示為 `31`。數值與 `data.db` 相同。Dashboard 的顯示格式可能與此不同；INV-2 比對的是資料值，比對時要注意這個差異。
- **O-3（給 #20／#21 的前瞻風險，Reviewer 沒有實測）**：`requirements.txt` 現在包含 `streamlit`，會連帶安裝 pandas、pyarrow、numpy、altair 等。R-DS-8 讓 Vercel 以單元目錄的 `requirements.txt` 建置，function 的大小可能接近平台限制。建議 #20／#21 及早確認；若必須拆分相依，而拆法會牽動 R-DS-8「`requirements.txt` 在單元目錄」這句話，應先 route 給 Design Authority。
- **O-4**：#18 的 F-10 已確認解決（見 §2）。

## 6. 需要其他 authority 的事項

無。F-1～F-3 都是在已接受契約內的實作或證據缺陷，以 targeted correction 處理即可，不需要改變設計或契約。F-9 的 Reviewer 讀法見上，沒有 routing。O-3 只有在 #20／#21 確認需要拆分相依時，才會成為 Design Authority 的事項。

## 7. 結論

實作的主體符合已接受的契約，而且都經 Reviewer 獨立驗證：唯一的讀取端共用模組、不含 SQL 與 HTTP client 的 Grading App、老師指定的字樣與 Region 順序、兩個 Region 乃至全部六個 Region 的圖表與表格都等於 `data.db`、DR-17 的取得時間原樣顯示、half-up 與依顯示值分帶的 Derived Map Temperature、離線測試共 104 個全部通過、18 個 mutation probe 全部被抓到，H-1 掃描也是零命中。

有三項 blocking：

- **F-1**：讀取端的 6 × 7 判定不完整，違反 R-SHR-2(a) 的「當且僅當」定義，並會傳到 #20 的 health 語義。屬於 H-3。
- **F-2**：唯讀 URI 沒有編碼，在合法的本機路徑下會讓評分產物失效。屬於 H-2。
- **F-3**：AB-2／AC-01 契約要求的截圖證據缺失，而且改用其他證據沒有授權依據。屬於 H-2。

三項都可以用有界的 targeted correction 解決，不需要重新設計。Non-blocking 的 F-4～F-11 已在各項下記錄 owner 與 disposition。

VERDICT: BLOCKING (F-1, F-2, F-3)
