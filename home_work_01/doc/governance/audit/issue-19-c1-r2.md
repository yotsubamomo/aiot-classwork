# Audit record：Issue #19，cycle 1，R2

| 欄位 | 內容 |
| --- | --- |
| Work Contract | GitHub Issue #19（`yotsubamomo/aiot-classwork`）「共用查詢／領域模組與 Grading App（app.py）：Select Region、一週折線圖與表格」，Scope class MVM。所屬 Spec 為 `home_work_01/doc/spec/SPEC.md` v1.1（EFFECTIVE）；Outcome Contract 為 `home_work_01/doc/governance/outcome-contract.md`（ACCEPTED 2026-09-23）。依據裁決與 R1 相同：DR-1、2、4、8、9、11、15、DR-17；`decision-20260923-high-risk-categories.md`（H-1／H-2／H-3，A-1）；`decision-20260924-unattended-run-policy.md` N-17、N-18 |
| 受審 subject | branch `home_work_01-hw10-implementation`，commit `0672020ad7a6dcd86a5c354737c8854da566b983`，是 R1 subject `353c8a7` 的 targeted correction。correction diff 為 `353c8a7..0672020`，共 9 個檔案，全部在 `home_work_01/` 內 |
| Audit 種類 | **R2**（scoped closure review，治理 §4.4），**cycle 1**；對應的 R1 record 為 `home_work_01/doc/governance/audit/issue-19-c1-r1.md`，verdict 為 BLOCKING (F-1, F-2, F-3) |
| 角色 | `primary_reviewer`（definition `gov-primary-reviewer`；Bindings §3.1 mapping 為 `claude-opus-5-5`／`xhigh`） |
| Binding 證據 | 由派工者（Orchestrator）依 Bindings §3.4 核對，記在 run record `home_work_01/doc/governance/run/run-20260924-hw01-formal.md`。Executor binding 見同一份 run record。 |
| Independence（治理 §2.3） | 本輪延續 Reviewer 自己的 R1 context（治理 §2.3 第 1 項允許），沒有繼承 Executor 的 context。修正後的檔案、diff、截圖與 worklog 都從磁碟重新讀取，也重新執行全部檢查。Executor 在 worklog 第 9 節的敘述只當作待驗證主張。本紀錄由 Reviewer 以自己的 Write 工具寫入。 |
| 範圍 | 只做三件事：(1) 核對 F-1、F-2、F-3 是否真正解決；(2) 修正有沒有引入回歸；(3) 修正有沒有直接產生或暴露新的 blocking defect。這不是第二次全面審查。 |
| 日期 | 2026-09-24 |

## 1. 方法與環境

- **Subject 識別**：`git rev-parse HEAD` 為 `0672020a…`。`git diff 0672020 --stat -- home_work_01` 只列出 Orchestrator 對 run record 的修改，屬 record-only path。`git diff --numstat 353c8a7..0672020` 的結果：
  - `weather_query.py`：+25／−3。
  - `app.py`：+2／−0。
  - `tests/test_weather_query.py`：+48／−0。
  - `tests/test_app.py`：+20／−0。
  - worklog：+52／−7。
  - 新增 4 張 PNG。
  - 測試檔**只有新增、沒有刪除**，沒有削弱既有保證。`data.db`、`ingestion/`、`requirements.txt`、README 與 `test_static_checks.py` 都沒有變動。
- **離線執行**：以 `git archive 0672020 home_work_01` 匯出到 Reviewer scratchpad，匯出樹內沒有 `.env`。使用單元 `.venv`（Python 3.12.14、streamlit 1.64.0），並沿用 R1 的 `sitecustomize` 封鎖非 loopback 網路，`HTTP(S)_PROXY` 指向無效位址。
- **`pytest -q -p no:cacheprovider`**：**107 passed**。其中 #18 的測試為 60 個（R1 已實際收集確認），本票為 47 個：`test_weather_query` 29、`test_app` 9、`test_static_checks` 9。
- **Reviewer 自己的檢查**（放在 scratchpad，不進 repo）：
  - 以修正後的程式重跑 R1 的 12 種邊界資料庫探測，另加一種「各區 7 列共用 6 個日期（重複日期）」。
  - 重跑 R1 的 7 種路徑字元探測，另外檢查特殊路徑下缺檔、唯讀，以及相對路徑的語義。
  - 把整個單元複製到 `…/C#course dir/home_work_01/`，在那裡跑全套件與 AppTest。
  - 針對修正做 6 個 mutation probe，並重跑 R1 的 18 個 mutation probe。
  - 對 6 個 Region 逐一做 AppTest 核對：表格等於 `data.db`；圖表 Arrow 資料為 14 點，也就是 7 天 × 2 條線；檢查軸標題與顏色。
  - 逐張檢視 4 張截圖，檢查 PNG chunk 與內容中的金鑰，並比對檔案雜湊。
  - H-1 掃描：只輸出次數，不輸出任何金鑰內容。

## 2. Blocking findings 的 closure

### F-1（H-3）：`snapshot_status` 把六區日期彼此錯位的 42 列快照判為 `ok` → **已解決**

- **修正內容**：`weather_query.py:205-235` 的 `_classify_rows` 收集全部列的日期為 `all_dates`，並要求兩件事：`len(all_dates) == 7`，且每個 Region 的日期集合都等於 `all_dates`。原本已有的四項檢查仍保留：42 列、沒有 null、Region 集合正確、數量正確。這符合 R-SHR-2(a)「恰 6 Region × 7 日且每格有值」的當且僅當定義，也符合 DR-9。
- **Reviewer 驗證**：
  - R1 用來重現問題的 `shift.db`（`東部地區` 的日期整週加 30 天，全體共 14 個不同日期）：現在判為 **`INCOMPLETE`**。以 AppTest 執行時顯示 `st.warning`，也沒有例外。
  - 重複日期（42 列，每區 7 列但只共用 6 個日期）：`INCOMPLETE`。
  - 提交的 `data.db`：`OK`。
  - R1 的其他邊界案例結果不變：41 列、43 列、天數 8／6、缺整個預設 Region 都是 `INCOMPLETE` 並顯示警告；缺失、空表、目錄、沒有 forecast 表的結果也和 R1 相同。
- **測試有沒有釘住修正**：新增的 `test_status_incomplete_mismatched_dates`（`test_weather_query.py:149-154`）與 `test_mismatched_dates_shows_warning_not_ok`（`test_app.py:153-160`）都能通過。把一致性檢查整段還原成 R1 的邏輯（mutant R1）後，這**兩個測試都失敗**（2 failed / 45 passed），所以修正確實被測試釘住。
- **結論**：F-1 已 closure。

### F-2（H-2）：唯讀 URI 沒有編碼，路徑含 `#` 或 `%XX` 時會把存在的 `data.db` 判為不存在 → **已解決**

- **修正內容**：`weather_query.py:160` 改為 `uri = Path(db_path).resolve().as_uri() + "?mode=ro"`。
- **Reviewer 驗證**：
  - R1 的 7 種路徑字元（空白、中文、`#`、`%20`、`%`、`;`、`&`）現在**全部**判為 `ok`，取得時間與 7 個 Forecast Day 都正確。R1 時 `#` 與 `%20` 這兩種是 `missing`。
  - URI 範例：`…/paths2/hash%23dir/data.db`。
  - 端到端：整個單元位於 `…/C#course dir/home_work_01/` 時，全套件 **107 passed**（R1 在同類路徑是 8 failed）。在該目錄執行 `AppTest.from_file("app.py")` 沒有例外、沒有錯誤訊息，六個選項完整，也有表格。Executor 主張的「在這種路徑下全套件通過」已被確認。
- **語義有沒有保留**：
  - 唯讀：在 `#` 目錄下執行 `DELETE` 會得到 `attempt to write a readonly database`。
  - 缺檔時 fail-closed：`#` 目錄下不存在的檔案，`snapshot_status` 回 `MISSING`，`last_ingestion_time` 回 `None`，`region_series` 拋出 `SnapshotError`。
  - 預設路徑仍以原始碼位置為基準；切換 CWD 後，相對路徑 `"data.db"` 仍能正確解析。
  - 靜態 `test_connection_is_read_only` 通過。
- **測試有沒有釘住修正**：新增的 `test_special_character_path_opens`（`test_weather_query.py:280-302`）使用 `c#course dir` 目錄。把 URI 還原成 R1 的寫法（mutant R4）後，這個測試失敗。拿掉 `?mode=ro`（mutant R5）後，`test_connection_is_read_only` 與這個新測試都失敗。
- **結論**：F-2 已 closure。

### F-3（H-2）：AC-01、AB-2（以及本票 AC-02）要求的截圖證據缺失；worklog 以不存在的註記為由改用其他證據，並聲稱環境無法擷取 → **已解決**

- **截圖存在，而且由 Executor 產生**：`home_work_01/doc/acceptance/screenshots/` 內有 4 個追蹤檔：
  - `ac01_home_default_region.png`
  - `ac02_select_region_options.png`
  - `ac03_region_central.png`
  - `ac03_region_southeast.png`
  - 四張都是 1284×1655。它們的 md5 與 Reviewer 在 R1 的 scratchpad 截圖**全部不同**（R1 的截圖是 1280×1800，而且沒有提交）。畫面上的 Y 軸已有 `Temperature (°C)` 標題，這個標題在修正後的 `app.py` 才存在，所以這些截圖來自修正後的 subject，是 Executor 自己擷取的。
- **內容逐張核對**：
  - **AC-01**（`ac01_home_default_region.png`）：首頁顯示 `Taiwan Weather Forecast`、caption `Last updated (data fetched from CWA): 2026-09-24T02:24:50+08:00`（與 `IngestionMetadata.ingestedAt` 逐字相同）、`Select Region`＝北部地區、MaxT 紅線與 MinT 藍線的七日折線圖（X 軸 `Date`）、`Date`/`MinT`/`MaxT` 七列表格；畫面上沒有任何例外。
  - **AC-02**（`ac02_select_region_options.png`）：`Select Region` 展開後，六個選項依序為北部地區、中部地區、南部地區、東北部地區、東部地區、東南部地區，符合 DR-8。
  - **AC-03**（`ac03_region_central.png`、`ac03_region_southeast.png`）：圖表標題分別為 `Temperature Forecast – 中部地區` 與 `Temperature Forecast – 東南部地區`，紅藍兩條線，表格七列。表中數值與 R1 時 Reviewer 直接查 `data.db` 的結果逐列相同：中部地區為 24.8/32.8、24.5/32.8、24.5/33、24.7/32.8、24.8/32.8、25.3/32、24.3/29.8；東南部地區為 24/31、25/31、25/31、25/32、25/33、25/31、25/30。
- **沒有秘密資訊**：
  - PNG 只含 `IHDR`／`IDAT`／`IEND` 三種 chunk，沒有 `tEXt`、`iTXt`、`zTXt` metadata。
  - 以字面金鑰與 CWA 金鑰格式掃描原始位元組，都是 0 筆。
  - 畫面只呈現公開的預報值與取得時間。
- **worklog 更正**：
  - `worklog/issue-19.md` §3 已移除「本環境無法擷取瀏覽器畫面」與「依 Ticket AC-01 註記」，改為明文**更正**：這兩項說法都是錯的，Ticket 並沒有這樣的註記。
  - §9 記錄了 server 啟動指令（含結果 `GET /` 200、`/_stcore/health` 200 "ok"、log 沒有例外）、Chrome headless 與 CDP 的擷取方式、各截圖的路徑與內容。
  - §7 已移除「截圖為後續人工補充項」。
- **是否滿足契約**：
  - OC AB-2 要求「worklog 紀錄＋截圖」：已滿足。
  - Spec AC-01 要求「worklog 記錄指令與輸出；截圖」：已滿足。
  - Ticket AC-01「（worklog＋截圖）」與 AC-02「（截圖）」：已滿足。
  - 截圖另外支撐 AC-03。
  - 存放位置屬於 HOW，#25 的驗收文件可以直接引用這個目錄。
  - Reviewer 在 R1 已獨立確認 AC-01 的行為成立，這次截圖與該結果一致。
- **結論**：F-3 已 closure。

## 3. 回歸核對

- **全套件**：離線、沒有 `.env`，**107 passed**。R1 的 104 個測試全部保留，沒有任何一個被改弱。
- **R1 的 18 個 mutation probe 重跑**：全部仍被抓到。M11（只畫 MaxT）因為插入了 `x_label`／`y_label`，原本的 pattern 找不到，Reviewer 改寫 pattern 後重跑，結果被抓到（2 failed）。其餘 17 個照原樣重跑，全部被抓到。
- **Grading App 行為**：AppTest 的頁面元素種類與 R1 相同（title、caption、selectbox、subheader、vega_lite_chart、dataframe），沒有地圖，也沒有日期控制。六個 Region 逐一核對：
  - 表格等於 `data.db`，欄位為 `Date/MinT/MaxT`。
  - 圖表為 7 天 × 2 條線，color domain 為 `[MaxT, MinT]`，range 為 `[#d62728, #1f77b4]`。
  - 小標題為 `Temperature Forecast – <Region>`。
  - 沒有例外。
- **F-9 附帶修改**（`app.py:89-90` 的 `x_label="Date"`、`y_label="Temperature (°C)"`）：chart spec 的 x.title 為 `Date`，y.title 為 `Temperature (°C)`。`test_app.py` 的 `_has_x_field` 仍能通過，沒有其他副作用。改動只有兩行，屬於 R1 對 F-9 所寫的「owner #19 可選」範圍，沒有擴張 scope。**F-9 已處理。**
- **F-11 附帶修改**：worklog V-1 改為「#18 的 60 例＋本票 47 例＝107」，與實際收集數一致。**F-11 已處理。**
- **H-2 名稱與資料**：`data.db` 的 blob 在 `0672020` 仍是 `687586991ce3…`，與 BASE 相同。頁面文字、Region 名稱與 `app.py` 位置都沒有變。

## 4. 高風險類別複核（A-1，只涵蓋修正影響的部分）

- **H-1**：correction diff（`353c8a7..0672020`，含二進位內容）、commit message，以及 `0672020` 樹內 434 個追蹤檔案：字面金鑰 0 筆、CWA 金鑰格式 0 筆。沒有追蹤任何 `.env`。4 張新增的 PNG 沒有文字 metadata，內容也不含金鑰。`app.py` 與 `weather_query.py` 的 import 沒有變（修正沒有新增 import），靜態檢查全部通過。**沒有殘留問題。**
- **H-2**：F-2 已修正，任何合法的本機路徑都能開啟評分產物。F-3 的截圖證據已補齊。老師指定的名稱、文字、DDL 與 `data.db` 都沒有變。新增的 Y 軸標題 `Temperature (°C)` 與上位契約 A.4 範例（`REQUIREMENTS.md:159`）一致，沒有改動任何老師指定的字樣。**沒有殘留問題。**
- **H-3**：F-1 已修正，讀取端的 6 × 7 判定改為要求六區共用同一組七天，錯位與重複日期都判為 `incomplete`。Derived Map Temperature 與色帶沒有變動，M1、M2 仍被抓到。**沒有殘留問題。**

## 5. 修正有沒有直接產生或暴露新的缺陷

沒有 blocking。下列兩項是 non-blocking，依治理 §4.4 不延長 cycle：

- **N-1（Low，non-blocking）**：`_classify_rows` 的兩個新檢查（`len(all_dates) == 7` 與「每區的日期集合等於 `all_dates`」），對已測試的錯位案例來說是互相重疊的，只拿掉其中任何一個時測試仍然通過（mutant R2、R3 都沒被抓到）。「每區 7 列但只共用 6 個日期」的重複日期案例，只靠 `len` 檢查擋下；Reviewer 已確認實際結果為 `incomplete`，但沒有測試釘住這個案例。Owner：#25（INV-3、INV-4 最終核對時可以補一個測試）或 #19（可選）。
- **N-2（Low，non-blocking）**：`weather_query.py:153-158` 的 docstring 與 worklog §9 都說路徑含「空白」也會解析錯誤。實際上 R1 的探測顯示，舊寫法遇到空白是正常的，出問題的只有 `#` 與 `%XX`。這只是描述不精確，不影響行為。Owner：#19（可選）。

R1 的 non-blocking findings 仍依 R1 record 追蹤，不屬於本 cycle：F-4 → #20；F-5、F-6、F-8 → #25；F-7、F-10 → #19 或 #21（可選，本次沒有處理）。F-9、F-11 已在本次一併處理，見 §3。

## 6. 需要其他 authority 的事項

無。

## 7. 結論

F-1、F-2、F-3 都已真正解決，而且都有會在回歸時失敗的測試或實體證據：F-1、F-2 由 mutation probe 確認測試能抓到還原，F-3 由提交的截圖佐證。修正沒有引入回歸：107 個測試通過，R1 的 18 個 mutation probe 全部仍被抓到，六個 Region 的畫面輸出不變，H-1、H-2、H-3 都沒有殘留問題。修正本身沒有產生或暴露新的 blocking 缺陷。Issue #19 cycle 1 的 audit 可以 closure。

VERDICT: CLOSURE
