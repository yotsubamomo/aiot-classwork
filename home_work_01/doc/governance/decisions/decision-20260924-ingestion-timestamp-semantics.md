# Decision record — Ingestion 時間戳（`IngestionMetadata.ingestedAt`）的語義（`home_work_01/`）

- **紀錄類型**：Design Authority decision record（治理 §3.6-A：在不改變任何 accepted 語義的前提下裁決既有來源尚未寫明之處；治理 §5.3 第 2 類「不改變 accepted 語義的 derived contract clarification」，須記錄對進行中工作、dependencies 與既有 evidence 的影響）
- **編號**：**DR-17**（延續 [`decision-20260923-spec-interpretation-rulings.md`](decision-20260923-spec-interpretation-rulings.md) 的 DR-1～DR-16）
- **日期**：2026-09-24
- **來源**：Issue #18 cycle 1 R1 audit record [`../audit/issue-18-c1-r1.md`](../audit/issue-18-c1-r1.md) §6 routing signal **R-1**（治理 §4.2：契約不足是 routing signal，不是 blocking finding）；由 Orchestrator 依治理 §2.4 派工，run record [`../run/run-20260924-hw01-formal.md`](../run/run-20260924-hw01-formal.md)
- **相關契約**：Outcome Contract（ACCEPTED 2026-09-23）§2.5；Spec v1.1 R-ING-3、R-ING-4、R-ING-5、R-DB-5、R-SHR-2(f)、R-GA-8、R-DS-2、R-DS-7、AC-24、AC-25、§4.1「Ingestion 中繼資料」；DR-2；`CONTEXT.md`「Ingestion」「Refresh」「Forecast Snapshot」；brief §6.1、§6.2、§6.7；`decision-20260923-high-risk-categories.md` H-3
- **執行角色**：`gov-design-authority`（binding 核對由派工者依 Bindings §3.4 記入 run record）
- **效力**：與 Spec v1.1 同一效力層級，作為 R-DB-5、R-SHR-2(f)、R-DS-2、R-GA-8、R-DS-7、AC-24 的解讀依據；Executor 與 Reviewer 以本紀錄適用該等條款，不得重開。Spec 條文與本紀錄不一致時以 Spec 為準並回報 DA。

## 1. 問題

R-DB-5 要求把「Ingestion 時間（ISO 8601，含 `+08:00`）」記在 `data.db` 內 `TemperatureForecasts` 以外的資料表，供兩個呈現層顯示「最後更新時間」（R-GA-8、R-DS-7、R-SHR-2(f)、R-DS-2、AC-24）。Ingestion 有兩條路徑：online（fetch → save raw JSON → derive → persist）與 offline `--from-json`（從已保存的原始 JSON 重跑 derive → persist；R-ING-5）。契約沒有寫明這個時間戳代表**資料從 CWA 取得的時間**還是**快照列被（重新）建立的時間**。Online 路徑下兩者只差數秒；offline 重建時兩者可以相差任意久。#19、#20 會把這個值顯示給使用者作為「最後更新時間」。

需要裁決：(a) online 路徑、(b) offline 重建路徑各應存哪個時間，並給出 Executor 與 Reviewer 可直接套用、與兩個呈現層的顯示一致的規則。

## 2. 事實（依原始證據，不採用 Executor／Reviewer 的結論）

| # | 事實 | 證據 |
| --- | --- | --- |
| E-1 | 現行實作在兩條路徑都以 persist 當下的時鐘作為 `ingestedAt`：`pipeline.ingestion_timestamp()` 回 `datetime.now(TAIPEI_TZ)`，`run_online` 與 `run_offline` 都在 `persist_snapshot` 之前才呼叫它。 | `693c12b:home_work_01/ingestion/pipeline.py`（`ingestion_timestamp`、`run_online`、`run_offline`） |
| E-2 | `persist_snapshot(rows, ingested_at, source_dataset_id, db_path)` 以參數接收時間戳，upsert 到 `IngestionMetadata(id=1, ingestedAt, sourceDatasetId)`；`TemperatureForecasts` DDL 不變。 | `693c12b:home_work_01/ingestion/persist.py`、`config.py` |
| E-3 | 提交的 `data.db` 中 `IngestionMetadata` = `(1, '2026-09-24T01:49:18+08:00', 'F-D0047-091')`；worklog 記載該 `data.db` 是「regenerated offline from the saved JSON with the committed code」。 | DA 於 `data.db` 唯讀查詢；`worklog/issue-18.md` §4 |
| E-4 | 提交的原始 JSON `data/raw/F-D0047-091.json` 在 Executor 工作樹的寫入時間為 `2026-09-24T01:39:31+08:00`（online run 的 `save_raw_json` 寫入；取得成功在此之前不到一秒）；fixture 寫入 `01:41:34`；`data.db` 寫入 `01:49:18`；commit `693c12b` 於 `01:51:06`。即提交快照的 `ingestedAt` 比實際取得時間晚約十分鐘。此時間差**只存在於工作樹的檔案 mtime**，沒有任何被追蹤或持久的紀錄。 | DA 於工作樹 `os.stat`；`git log -1` |
| E-5 | F-D0047-091 回應本體**沒有**任何發布時間或取得時間欄位：全部 JSON key 為 `success`、`result{resource_id, fields}`、`records.Locations[]{DatasetDescription, LocationsName, Dataid, Location[]{LocationName, Geocode, Latitude, Longitude, WeatherElement[]{ElementName, Time[]{StartTime, EndTime, ElementValue}}}}`。因此取得時間無法由 JSON 本身還原，只有 online run 當下知道。 | DA 對提交的原始 JSON 列舉全部 key |
| E-6 | R-ING-4／AC-25 要求原始 JSON「完整」寫出；R1 以「位元組與 `json.dumps(data, indent=2, ensure_ascii=False)` 相同」作為 AC-25 證據。 | Spec R-ING-4、AC-25；R1 §2 AC-25 |
| E-7 | 現有測試：`test_persist.py` 以常數 `INGESTED_AT` 直接呼叫 `persist_snapshot`；`test_pipeline.py` 的 offline 測試不斷言時間戳。沒有測試涉及時間戳的來源。 | `693c12b:home_work_01/tests/test_persist.py`、`test_pipeline.py` |
| E-8 | 契約用語：CONTEXT「Ingestion＝取得（acquires）→ 推導 → 驗證 → 持久化的離線流程」；「Forecast Snapshot＝目前持久化的一週預報…**as last ingested**」；「Refresh＝再跑一次 Ingestion 使持久化的 Forecast Snapshot **變成更新的一份**」。R-ING-5 把 offline 路徑稱為「離線**重建**」。User story 13：「看到這份預報是什麼時候更新的，so that 我知道**資料有多新**」。DR-2(3)：這個時間是「**資料出處標示**」。AC-24 的 FAIL 例：「時間取自檔案 mtime」；DR-2 拒絕 mtime 的理由是「git checkout 與 Vercel 打包後不可靠」。 | `CONTEXT.md`；Spec R-ING-5、User Stories 13、AC-24；DR-2 |
| E-9 | 本裁決採用的「頁面顯示最後更新時間」來自 Part B 的 top bar「CWA Temperature Broadcast \| Last update」，經 brief §6.7 採納、OC §2.5 引入為已裁決前提；來源文件未定義該值。 | `REQUIREMENTS.md` 第 636 行；brief §6.7；OC §2.5 |

## 3. 兩種解讀

- **(A) 建立時間**：`ingestedAt` ＝ persist 執行當下的時鐘（現行實作）。字面上「ingestion 時間」可以這樣讀，實作最簡。但 offline 重建會把顯示給使用者的「最後更新時間」推到重建當下，而資料本身沒有變新；同一份資料在 online 與 offline 路徑會得到不同的標示。
- **(B) 取得時間**：`ingestedAt` ＝ 快照所依據的那份 F-D0047-091 回應從 CWA 取得成功的時間。Offline 重建保留原取得時間；同一份資料無論怎麼重建，標示相同。

## 4. 裁決（DR-17）

### 4.1 語義

**R-DB-5 的「Ingestion 時間」＝取得時間（acquisition time）**：online Ingestion run 在 R-ING-3 驗證通過（HTTP 200、`success == "true"`、`resource_id == F-D0047-091`）而**實際取得**該份 F-D0047-091 回應的本機時鐘時間，ISO 8601、`+08:00`、至少到秒。它是**所取得原始資料的屬性**，不是 persist 操作的屬性。

R-SHR-2(f)「最後 ingestion 時間」、R-DS-2 的「ingestion 時間」、R-GA-8／R-DS-7「快照的最後 ingestion 時間」、AC-24「最後 ingestion 時間」、brief §6.7「最後更新時間」，一律指這個值。

### 4.2 Online 路徑

1. 時間戳在 `fetch` 成功（回應驗證通過）的當下**取一次**；不得在 persist 時再讀一次時鐘。
2. 同一個值：(a) 寫入 `IngestionMetadata.ingestedAt`；(b) 作為所保存原始 JSON 的**出處紀錄**（provenance record）一併保存，供 offline 重建使用（第 4.4 節）。

### 4.3 Offline 路徑（`--from-json` 或任何等價的離線 derive → persist 介面）

1. `ingestedAt` MUST 是**所載入那份原始 JSON 的取得時間**，來源只能是：該 JSON 的出處紀錄，或呼叫端明確提供的取得時間（例如測試對 fixture 提供）。
2. Offline 路徑 MUST NOT 讀取時鐘作為 `ingestedAt`。
3. 找不到取得時間（沒有出處紀錄、也沒有明確提供）時，MUST 在寫入前以明確訊息失敗：指名缺少什麼、如何提供；結束碼非零；既有快照不變（與 R-DER-7、AC-09、AC-11 同一 fail-closed 姿態；INV-3 不受影響）。不得以「現在時間」或任何推測值代替。

### 4.4 出處紀錄（機制屬 HOW，以下為約束）

- 形式屬 HOW：與原始 JSON 並列的 sidecar 檔（例如 `<raw>.meta.json`）、或文件化的 CLI 參數，或兩者。
- MUST NOT 改動所保存原始 JSON 的內容（R-ING-4／AC-25：原始回應完整、未加工；不得把時間包進 JSON 本體）。
- MUST 位於單元目錄內，並在 README 的「執行 ingestion 的指令（含離線重跑）」段落文件化（R-DOC-1）。
- MUST NOT 含金鑰、`Authorization` 或任何請求標頭（R-SEC-2、H-1）；A-5 的掃描範圍涵蓋它。
- **提交的原始 JSON MUST 連同其出處紀錄一起提交**，使 README 的離線重建指令在乾淨 checkout 下可以執行（AC-12），且重建出的 `data.db` 的 `ingestedAt` 等於提交的 `data.db` 的值。
- 出處紀錄 MAY 另記其他資訊（例如 HTTP `Date` 標頭、重建時間），但這些都不是 `ingestedAt`。

### 4.5 顯示（#19、#20、#24）

- 兩個呈現層顯示的值 MUST 恰等於資料庫內的 `ingestedAt`（AC-24 不變）；`/api/health` 的 ingestion 時間欄位回同一值。
- 標籤文字屬 HOW，但 MUST 把它呈現為「這份快照的資料**從 CWA 取得**的時間」（例如「最後更新時間（資料取得自 CWA）」／「Last updated (data fetched from CWA)」）；MUST NOT 呈現為 CWA 的預報**發布**時間（回應內沒有這個資訊，E-5），也 MUST NOT 呈現為頁面載入或部署時間。
- `IngestionMetadata` MAY 有其他欄位（例如重建時間），但 R-SHR-2(f)／R-DS-2／AC-24 回傳與顯示的只能是 `ingestedAt`；`TemperatureForecasts` 仍不得改動（H-2）。

### 4.6 測試（Reviewer 於 R2 核對）

以下 MUST 有自動化證據（形式屬 HOW；建議與 F-2 的 CLI 層補強同一手法）：

- T-1 Online（mock HTTP，時鐘可控）：`ingestedAt` 等於 fetch 成功當下取得的值，且出處紀錄含同一值。
- T-2 Offline（提供出處紀錄或明確取得時間；時鐘 patch 成可區別的值）：`ingestedAt` 等於提供的取得時間，不等於時鐘值。
- T-3 Offline 無取得時間：非零結束碼、訊息指名缺少出處、資料庫不寫入、既有快照不變。
- T-4 出處紀錄不含金鑰（納入 `test_secrets.py` 的掃描對象）。

## 5. 依據

1. **契約用語指向資料的取得。** CONTEXT 把 Ingestion 定義為「取得→推導→驗證→持久化」的一次流程，Forecast Snapshot 是「as last ingested」的那一份，Refresh 是「再跑 Ingestion 使快照變成更新的一份」；R-ING-5 把 offline 路徑稱為「離線重建」——重建的是同一份 ingestion 的結果，不是新的 ingestion（E-8）。在這套詞彙下，快照的「ingestion 時間」錨定在取得資料的那次 run；offline 重建不產生新的取得，就不應產生新的時間。
2. **顯示目的是資料新鮮度與出處。** User story 13「我知道資料有多新」與 DR-2(3)「資料出處標示」只有在值代表取得時間時才成立；重建時間對資料新鮮度沒有資訊量，卻會讓使用者高估新鮮度（E-8）。
3. **AC-24 已排除同類的人為時間。** AC-24 以「取自檔案 mtime」為 FAIL 例，DR-2 拒絕 mtime 的理由是它反映檔案處理的副作用而非資料的屬性；persist 當下的時鐘在 offline 重建時屬同一類（反映有人何時執行了指令）。既有契約已對這類值表達了否定，(B) 是與之一致的唯一讀法。
4. **H-3 誠實標示。** 高風險類別 H-3 的風險描述包含「文件把專案推導值寫成 CWA 發布值」這種標示失真；MVM 交付的是**提交到 git 的準備好的快照**（brief §6.1、R-DB-6），日後為了可重現性、CI 或維護而離線重建是可預期的正常操作——(A) 會在每次重建時把一個失真的「最後更新時間」寫進公開 dashboard。(B) 消除這個風險，且不新增任何使用者可見功能。
5. **兩條路徑對同一資料應得到同一標示。** (B) 使 online 與 offline 對同一份原始 JSON 得到相同的 `ingestedAt`，也讓「從提交的原始 JSON 離線重建」能重現提交的 `data.db`（含中繼資料），這正是 R-ING-5「離線重建」與 AC-12「離線重跑」的用途。
6. **(A) 的唯一優點是實作最簡**，但 (B) 的額外成本只是保存一個時間戳並在 offline 路徑讀回，機制仍屬 HOW（Spec §4.2「Ingestion 的檔案切分與 CLI 介面…原始 JSON 的保存檔名」）。
7. **Fail-closed 的依據**：Spec 對 ingestion 一貫要求「驗證失敗不寫入、非零結束碼、明確訊息」（R-DER-7、AC-09、AC-11、§5.1）；缺少取得時間就是缺少一個 MUST 記錄的值（R-DB-5），以推測值補上會違反第 4 點。

## 6. 是否改變 accepted 語義

**否。** Outcome Contract 對這個值只有 §2.5 → brief §6.7「頁面顯示最後更新時間」，沒有任何 AB 定義它代表什麼；intent、scope、constraints、acceptance boundary 都不受影響。Spec 已要求的欄位、格式（ISO 8601 `+08:00`）、儲存位置（`TemperatureForecasts` 以外）、兩層顯示義務全部不變；本裁決只確定「已被要求記錄的那個值」代表什麼，並禁止 offline 路徑捏造它。沒有新增 requirement、AC、invariant 或 gate；沒有新增 audit round。屬治理 §5.3 第 2 類，不觸發 acceptor 核准。

不是新的設計基線：#19、#20 依賴的介面（R-SHR-2(f) 回傳一個 ISO 字串、R-DS-2 的欄位、`IngestionMetadata.ingestedAt` 的存在與格式）完全不變，兩票只是把值原樣傳遞與顯示。

Boundary determination（治理 §1.2）：在已接受的 Outcome Contract boundary 內；不需 acceptor；不涉及任何 reserved boundary（第 7 節的一次 online 重跑使用既有未追蹤 `.env`，屬 OC AB-8／§5 已授權的正常操作，RB-3 只保留申請、輪替、填寫；見 `decision-20260924-unattended-run-policy.md` N-10）。

## 7. 對 #18 的實作要求（cycle 1 targeted correction 內的契約內 rework）

本節是治理 §3.8「審後變更需要相應驗證」的具體內容，與 F-1、F-2 的修正一併進行；它不是 scope expansion（同一 AC-24 資料面、同一 subject），也不重新設計。

| # | 要求 | 位置（現行結構，HOW 可調整） |
| --- | --- | --- |
| I-1 | `run_online`：在 `fetch_raw` 回傳（驗證通過）後立即取一次時間戳；把它寫成所保存原始 JSON 的出處紀錄（第 4.4 節），並把**同一值**傳給 `persist_snapshot`。終端輸出可沿用「ingested at …」。 | `ingestion/pipeline.py` |
| I-2 | `run_offline`：從出處紀錄或明確參數取得該 JSON 的取得時間；移除對時鐘的讀取；缺少時在 derive／persist 前以 `Ingestion failed: …` 類訊息失敗、結束碼非零、不寫入。 | `ingestion/pipeline.py`（CLI 參數形式屬 HOW） |
| I-3 | README：出處紀錄的位置與內容、離線重建指令如何取得時間、離線重建與 online 取得的關係（重建不更新「最後更新時間」）。 | `README.md` ingestion 段 |
| I-4 | **提交的資料集合必須一致**：提交的 `data.db` 的 `ingestedAt` MUST 等於提交的原始 JSON 的出處紀錄中的取得時間。提交的原始 JSON 目前**沒有**持久的出處紀錄（E-4、E-5），因此 Executor MUST 以修正後的 pipeline **執行一次 online ingestion**，把該次 run 產生的原始 JSON、出處紀錄與 `data.db` 一起提交（worklog 記錄，不含金鑰；AC-07(a) 的證據隨之更新）。Fixture MAY 維持現有 2026-09-24 01:41 的縮減版（R-TC-2；測試的手算期望值對照的是 fixture，不是原始觀察檔）；若 Executor 選擇重新產生 fixture，手算期望值 MUST 依新 fixture 重算並註明。 | `data/raw/`、`data.db`、`worklog/issue-18.md` |
| I-5 | **僅當** CWA 在 `decision-20260924-unattended-run-policy.md` §5 定義的合理重試後仍無法取得（S-10）時的替代：保留現有原始 JSON，以其在 Executor 工作樹的原始寫入時間 `2026-09-24T01:39:31+08:00`（E-4；online run 寫檔時間，晚於取得成功不到一秒）作為取得時間建立出處紀錄並離線重建；worklog MUST 引用 `stat` 證據並說明此值由檔案寫入時間佐證。這是有界（同日、分鐘級）且有證據的替代，不是推測。 | 同上 |
| I-6 | 測試 T-1～T-4（第 4.6 節）。 | `tests/` |

不變的部分：`persist_snapshot` 的介面與 `IngestionMetadata` 的 `ingestedAt`／`sourceDatasetId` 欄位、`TemperatureForecasts` DDL、R-DER 全部規則。

## 8. 對 #19、#20、#24、#25 的影響

- **#19**（R-SHR-2(f)、R-GA-8、AC-24 Grading App）：共用模組原樣回傳 `ingestedAt`；`app.py` 的標籤依第 4.5 節；AC-24 測試維持「顯示值等於資料庫值」。Ticket 本文的「最後 ingestion 時間」依 DR-17 解讀，不需改票。
- **#20**（R-DS-2、R-DS-7、AC-16、AC-24 Dashboard）：`/api/health` 與頁面顯示同一值；標籤依第 4.5 節。
- **#24**（ENHANCED UI）：若摘要區重複顯示此值，同一約束；沒有新義務。
- **#25**（AC-12 README 實跑含離線重跑、AC-24 最終核對、AC-14 文件審查）：離線重跑 MUST 由提交的出處紀錄重現提交 `data.db` 的 `ingestedAt`；AC-14 文件審查時一併核對第 4.5 節的標籤措辭與 README 說明（不新增 AC，屬 R-DOC-2「誠實記述」與 H-3 標示核對的一部分）。
- Ticket 索引與 Issues：由 Orchestrator 以 comment 引用本紀錄（控制面 bookkeeping，N-22）；不改票的 AC。

## 9. 對既有 evidence 與 audit coverage 的影響（治理 §5.3 第 2 類、§3.8）

- **R1 record `issue-18-c1-r1.md`**：AC-24（資料面）的 PASS 明記「語義上的疑問見 §6 R-1」，其對格式、位置、DDL 不變的判定仍有效；語義符合性（第 4.2–4.4 節）由 **R2 在同一 cycle 內**作為審後變更驗證核對（DA 依 §3.8 判定的必要後續）。這不是新 cycle：subject 的改變是有界的（時間戳來源、出處紀錄、測試、依 I-4 重新產生的資料集合），不構成 §4.5 的 material rework 起點；R2 仍依 §4.4 只做 closure review，不做第二次全面 audit。
- **依 I-4 重新產生原始 JSON 與 `data.db` 時**，R1 中綁定於原提交資料的證據（AC-05 對提交 `data.db` 的兩句 SQL、AC-08 獨立推導與提交 `data.db` 的一致、AC-25 位元組比對、AC-07(c)(d) 掃描、A-5）需由 R2 對新的提交集合重新建立——這是 R2 第 (2) 項「修正未引入回歸」的範圍，Reviewer 自行判定證據充分性；DA 不預判結果。
- **Worklog `issue-18.md`**：§3 的 Metadata 決定改引 DR-17；§4、§5 更新產物與驗證；§8 說明資料集合是否重新產生。
- **Spec v1.1 文字不變**：R-DB-5、R-SHR-2(f)、R-DS-2、R-GA-8、R-DS-7、AC-24 依本紀錄解讀（與 DR-1～DR-16 相同機制）。Spec 下次一致性修訂 MAY 在這些條款加註 DR-17（metadata 層級，DA）。
- **`doc/acceptance/`**（#25 建立）：AC-24 條目引用 DR-17。

## 10. 受影響 work items

- **#18**：進行中（cycle 1 targeted correction）——第 7 節。
- **#19、#20**：pending——第 8 節（解讀，不改票）。
- **#24、#25**：pending——第 8 節。
- **#21、#22、#23**：不受影響。

## 11. 需要其他 authority 的事項

無。不需 acceptor（不改變 accepted 語義、不觸及 reserved boundary）；不需 Final Adjudicator（沒有 routing 或 review 爭議）。若 Reviewer 在 R2 對第 9 節「同一 cycle 內驗證」的處理有異議，依治理 §4.3／§4.5 交 Final Adjudicator 裁決程序問題；本裁決的語義部分不因此重開。

## 12. Evidence

- 治理 v2.0 §1.2、§2.4、§3.6-A、§3.8、§4.2、§4.4、§5.3；Bindings b1 §2.4、§2.6、§7。
- Outcome Contract §2.5、§4、§5、AB-8；brief §6.1、§6.2、§6.7；`REQUIREMENTS.md` 第 636 行（Part B「Last update」）。
- Spec v1.1 R-ING-3、R-ING-4、R-ING-5、R-DB-5、R-DB-6、R-SHR-2(f)、R-GA-8、R-DS-2、R-DS-7、R-SEC-2、R-DOC-1、AC-09、AC-11、AC-12、AC-24、AC-25、§4.1、§4.2、§5.1、User Story 13。
- `CONTEXT.md`「Ingestion」「Refresh」「Forecast Snapshot」。
- `decision-20260923-spec-interpretation-rulings.md` DR-2；`decision-20260923-high-risk-categories.md` H-3、A-5；`decision-20260924-unattended-run-policy.md` N-10、§5。
- `issue-18-c1-r1.md` §2 AC-24／AC-25、§6 R-1；`worklog/issue-18.md` §3–§5。
- Subject `693c12b`：`ingestion/pipeline.py`、`persist.py`、`config.py`、`fetch.py`、`tests/test_persist.py`、`tests/test_pipeline.py`；DA 對提交 `data.db` 的唯讀查詢、原始 JSON key 列舉、工作樹 mtime（E-3～E-5）。
