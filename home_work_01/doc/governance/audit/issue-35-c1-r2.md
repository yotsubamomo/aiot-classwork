# Audit record — Issue #35，cycle 1，R2（scoped closure review）

| 欄位 | 內容 |
| --- | --- |
| Work Contract | GitHub Issue **#35**（`yotsubamomo/aiot-classwork`）「伺服器端 Latest Observation 路徑：`/api/` 觀測回應、四類失敗分類與安全邊界 re-scope」；契約同 R1 record `issue-35-c1-r1.md`（V2 Outcome Contract `69c5a04`、SPEC-V2 v2.2、derivation-SPEC-V2、decision `decision-20260923-high-risk-categories.md`）。 |
| 受審 subject | branch `home_work_01-v2-implementation`。修正後 code anchor **`5f0dbc37eb9b6830d1a8e392617e1bd68c810a5f`**；遠端 HEAD **`50ecdbfdc96ff9b4497bb62c83756eab09bbfae0`**（＝`git ls-remote origin`）；本機 HEAD `4a5036d`（未 push，只加入 R1 record 與 run record，record-only）。修正 diff：`git diff bbc1d56 5f0dbc3`：`home_work_01/observation.py`、`home_work_01/tests/test_observation.py`、`home_work_01/README.md`（另有 run record，record-only）。`5f0dbc3..4a5036d` 只動 `doc/governance/**`。R1 subject 為 `08e158e..c9c9ec5`（code anchor `bbc1d56`）。 |
| Audit 種類 | **R2**（治理 §4.4 scoped closure review），**cycle 1**。範圍：(1) R1 blocking finding F-1 是否真正解決；(2) 修正是否造成回歸；(3) 修正是否直接產生或暴露新的 blocking defect。不是第二次全面審查。 |
| 角色 | `primary_reviewer`（definition `gov-primary-reviewer`；Bindings §3.1 mapping `claude-opus-5-5`／`xhigh`） |
| Binding 證據 | 正式核對由派工者記入 run record `run-20260925-hw01-v2-formal.md`。Reviewer 以 Bindings §3.4 的指令再讀 harness 紀錄（session `05b8408b-260a-46d3-a4fe-ec07e3ec365a`）：`agent-ab39e3a58cdb76117` `gov-primary-reviewer` `[('claude-opus-5-5', 'xhigh')]`（本 Reviewer，與 R1 同一 agent）；`agent-a1eef729c5e6bcebf` `gov-executor` `[('claude-opus-5-5', 'high')]`（做修正的 Executor）。兩者與 Bindings §3.1（b2 override）一致。 |
| Independence（治理 §2.3、§4.6） | (1) 本 R2 依 Bindings §3.5 延續 Reviewer 自己的 R1 context，沒有繼承 Executor context；修正後的檔案與 diff 皆從磁碟與 git **重新讀取**（`git diff bbc1d56 5f0dbc3`、`git archive 5f0dbc3` 匯出），worklog 與 run record 的修正敘述只當作待驗證主張。(2) Binding 見上一列。(3) 自主取得：Reviewer 自己重跑測試、R1 的獨立 oracle 與 probe，並新增 per-field 矩陣 probe（`probe_matrix.py`）與反向 mutation 檢查（scratchpad，未提交）。(4) 本紀錄由 Reviewer 以自己的 Write 工具寫入。另確認 R1 record 已由派工者在 `4a5036d` 原樣提交（working tree 與 HEAD 無差異，末行仍為 R1 verdict）。**Model diversity：`diversity_lost`**——Executor 與 Primary Reviewer 同為 `claude-opus-5-5`（Bindings §5；decision A-7）。這是合法狀態，不是缺陷。 |
| 日期 | 2026-09-26 |

## 1. 修正內容（Reviewer 重讀 diff）

- `observation.py`：單一 `SENTINELS` 集合改為依欄位分組的代碼——`MISSING_CODES`＝`{X, -99}`、`PRECIPITATION_CODES`＝`{T, -98}`、`WIND_DIRECTION_CODES`＝`{990}`；`SENTINELS` 保留為五個代碼的聯集，只用於氣溫有效性（R-V2-OBS-2(b)）。`FIELD_SENTINELS` 對應：`airTemperature`＝全部五個；`windDirection`＝`X`／`-99`／`990`；`precipitation`＝`X`／`-99`／`T`／`-98`；`relativeHumidity`、`windSpeed`、`airPressure`、`weather`、`coordinates`＝`X`／`-99`。`normalize_station` 對每個欄位只用該欄位的集合；service 的參數由 `sentinels=` 改為 `field_sentinels=`，key 集合不符時拒絕。取得、分類、重用、log、金鑰讀取的程式沒有改動（diff 只涉及哨兵的傳遞與建構子檢查）。
- `README.md`：哨兵段改為「代碼／意義／適用欄位」表，並寫明其他欄位的 `990.0` 是真實讀值、原樣回傳；對應常數與覆寫方式。
- `tests/test_observation.py`：R1 指出的兩處錯誤斷言已改；新增真實 990.0 氣壓測試、13 例的「代碼只作用於其欄位」衍生測試、可設定性測試、per-field 集合測試與資料標準對照測試；`EXPECTED_STATIONS` 加入 `C0F9I0`。

## 2. F-1 closure 核對 — **RESOLVED**

| 檢查 | 結果 | 證據 |
| --- | --- | --- |
| 樣本的兩個真實 `AirPressure "990.0"` | **原樣回傳 `990.0`** | `probe_semantics.py`（對 `git archive 5f0dbc3`）：`C0F9I0 … -> 990.0`、`CAF030 … -> 990.0`。 |
| 全樣本獨立 oracle（R1 自寫、依 SPEC-V2 R-V2-OBS-2／3／4 與 BRIEF-V2 §3.2，不引用 `observation.py`） | **0 差異** | 有效 ID 849 筆相同，dataset Observation Time 相同，所有欄位值與型別差異數由 R1 的 2 變為 **0**。AC-V2-03 以 Reviewer 抽樣的 `C0F9I0` 手算，輸出等於期望。 |
| 發布的 `990.0` 雨量 | 保留為 `990.0` | 同 probe：`C0TB40 precipitation '990.0' -> 990.0`。 |
| 風向 `990`（風向不定） | 仍為 `null` | 同 probe：`windDirection '990' -> None`。 |
| 雨量 `T`／`-98`（R-V2-OBS-6） | 仍為 `null` | `probe_matrix.py`：把 `X`、`-99`、`-99.0`、`T`、`-98`、`-98.0`、`990`、`990.0` 逐一放進 `C0TB40` 的六個可選欄位與氣溫。結果：雨量的 `X`／`-99`／`-99.0`／`T`／`-98`／`-98.0` → `null`；風向的 `X`／`-99`／`-99.0`／`990`／`990.0` → `null`；濕度、風速、氣壓的 `X`／`-99`／`-99.0` → `null`，天氣的 `X`／`-99` → `null`；其他數值組合 → 原樣數值；氣溫放任一代碼 → 該站被排除。**矩陣問題：none**。同一矩陣對修正前的 `bbc1d56` 則列出多個「應為數值卻為 null」。 |
| 哨兵永不成為數值 | 成立 | 同矩陣；樣本回應中沒有任何欄位出現其適用哨兵的數值（`-99`、風向 `990`、雨量 `-98`）。 |
| 被 R1 點名、把錯誤行為固定下來的測試 | 已更正 | `test_every_station_has_the_contract_fields` 的可選欄位斷言改為通用代碼（`-99`／`X`），另對風向 `990`、雨量 `-98`／`T` 分別斷言；原 `test_parse_published_number` 的 `"990"`／`"990.0"`／`"-98"` → `None` 改為依欄位的期望（更名為 `…_generic_codes`，其餘參數保留）。 |
| 新測試能抓到 bug | 能 | 把修正前的 `observation.py`（`bbc1d56`）放回修正後的測試樹：**34 failed**。與行為相關而非只是缺少新 symbol 的失敗包括 `test_sample_normalises_to_hand_computed_stations`（`C0F9I0`）、`test_real_990_air_pressure_is_kept_as_published`、`test_sentinel_applies_only_to_its_fields[AirPressure-990.0…／AirPressure-990…／Precipitation-990.0…]`、`test_parse_published_number_generic_codes[990.0／990／-98]`。反向 mutation（修正後模組，每次只改一處）：氣壓改用全部代碼 → 7 failed；風向拿掉 `990` → 5；雨量拿掉 `T`／`-98` → 5；雨量改用全部代碼 → 3；氣溫只用 `X`／`-99` → 6；氣壓呼叫點誤用氣溫集合 → 4。每一種都被抓到。 |
| 契約 | 符合 | R-V2-OBS-3（有效的可選欄位為數值、無效為 `null`）、R-V2-DD-7（有效時顯示）、R-V2-OBS-6（哨兵→「—」，永不為數值）、R-V2-OBS-2(b)（氣溫有效性用完整集合）、Issue #35 H-3「觀測值『如發布』」、AC-V2-03；哨兵集合仍可設定（`field_sentinels=`）且 README 已文件化到逐欄位（R-V2-OBS-2(b)「可設定、有文件」）。 |

## 3. 回歸核對 — **無回歸**

| 項目 | 結果 | 證據 |
| --- | --- | --- |
| 全套離線測試 | PASS | working tree（code 與 `5f0dbc3` 相同）：`pytest` → **424 passed**。 |
| V1 測試保留 | PASS | BASE 的 259 個 test id 全部仍在（`comm -23` 空）。相對 `bbc1d56` 消失的 id 只有 #35 自己的 `test_parse_published_number[...]`，它們改名為 `test_parse_published_number_generic_codes`，錯誤的四個期望依欄位改寫；其餘參數保留，`T` 由 per-field 測試涵蓋。 |
| 靜態檢查 re-scope 仍只加不減 | PASS | `tests/test_static_checks.py`、`tests/test_secrets.py`、`tools/credential_scan.py`、`server.py`、`api/`、`.github/` 在 `bbc1d56..4a5036d` **無 diff**；R1 第 4 節結論不變。 |
| 四類失敗、零洩漏（H-1） | PASS | 對 `git archive 5f0dbc3` 重跑 R1 的 `probe_failures.py`（真實 Flask＋`requests`、loopback 上游回顯 `Authorization`、root DEBUG、fd 層級擷取）：17 個情境的 reason／狀態與 R1 相同（503 `key_not_configured`；504 `upstream_unreachable`；502 `upstream_error`＋`upstreamStatus`；502 `invalid_response`；200 success），回應、標頭、log、stdout、stderr 的洩漏檢查全部 **none**。 |
| H-1 git／evidence | PASS | `python -m tools.credential_scan`（HEAD `4a5036d`）→ `credential scan passed: 559 tracked files; no .env tracked (only .env.example); no CWA-key-format string in tracked files or committed history; no Authorization value in fixture/raw JSON.`；`git ls-files` 只有 `.env.example`。`git diff bbc1d56 4a5036d` 唯一的金鑰格式字面是 R1 record 引用的文件化假金鑰 `CWA-1234-5678-90ab-cdef`（V1 allowlist）。 |
| H-2 | PASS | `app.py` `5693be8`、`weather_query.py` `4d2e92f`、`data.db` `6875869`、`ingestion/` `91df24e`、`static/` `c8c367b` 在 `5f0dbc3` 與 `4a5036d` 皆與 R1（亦即 BASE／V1）相同；`data.db` 未變，老師兩句 SQL 的 6／7 列結果沿用 R1 的執行。單元目錄外無變更。 |
| 預報 endpoint byte 相同（封網、無金鑰） | PASS | 以 R1 的 `dump_forecast.py` 對 `git archive 5f0dbc3` 重跑，輸出與 BASE 的輸出檔 **`cmp` 相同**。 |
| INV-V2-1／2／4／6／8 | HOLDS | 修正未碰取得、分類、重用、`/api/health`、預報 route 或金鑰讀取（見第 1 節）；上述 byte 對照、洩漏 probe、測試全綠成立。 |
| AC-V2-05 八個反例仍由未改動的樣本衍生 | PASS | 樣本 blob `6d4f174` 在 `bbc1d56`、`5f0dbc3`、`4a5036d` 相同；反例測試全部通過。 |
| CI | PASS | run `36164066306`（`d876577`，含 `5f0dbc3`）與 `36164186012`（`50ecdbf`）皆 success，log 為 `424 passed` 與 credential scan passed；workflow 檔未改。 |
| 修正範圍 | 符合 targeted correction | code 只動 `observation.py`、`test_observation.py`、`README.md` 的哨兵相關部分；沒有夾帶 F-2／F-3 或其他範圍擴張。commit message 格式正確、無 Claude 標記。 |

**修正產生或暴露的 blocking defect：無。** 附帶觀察（不是 finding）：座標現在只套用 `X`／`-99`，所以理論上的 `-98`／`990` 座標會被當成有限數字接受。R-V2-OBS-2(c) 只要求「有限數」，依資料標準這些代碼也不是座標代碼，CWA 實際不會這樣發布；圍欄外測站的處理屬 R-V2-DD-11（#38）。因此不構成契約偏離。

## 4. 殘留的 non-blocking 項目（R1 已記錄，本 R2 不延長 cycle）

| ID | 狀態 | Owner／disposition |
| --- | --- | --- |
| F-2（Medium）並行請求在上游停滯時被鎖序列化 | 未變（修正後 probe 仍為 1.00／2.01／3.01 s）；修正沒有使它惡化 | Orchestrator 帶到 **#37**（AC-V2-06(e) 前端 30 秒終態）與 **#41**（Vercel 時限與並行 preview 驗證）；若平台證據顯示會超過界限，依 derivation §11 #1 route Design Authority。 |
| F-3（Low）單筆不可雜湊的 `CountyName` 造成整體 `invalid_response` | 未變（probe 仍為 502） | 記錄即可，不需後續處理；日後若修改 `normalize_station`，owner 為該次變更的 Executor。 |
| F-4（Low）README 部署段仍寫「function 不需環境變數與 secret」 | 未變（`README.md` 部署段） | **#41**（R-V2-DOC-1(6) Vercel 部分與 (11)；AC-V2-21(12)）。 |

雜項（不是 finding）：`git diff --check bbc1d56 4a5036d` 只報告 `doc/governance/worklog/issue-35.md:126` 檔尾多一個空行。這是 record-only 路徑的格式問題，不影響 subject。

## 5. Routing

- Design Authority：不需要（F-1 已依資料標準的逐欄位語義解決，沒有待裁決的語義爭議）。
- Acceptor：沒有觸發任何 reserved boundary。

VERDICT: CLOSURE
