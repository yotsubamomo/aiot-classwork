# Audit record — Spec Integration Audit：SPEC-V2，cycle 1，R1 post-key 證據補完（P-1～P-4）

| 欄位 | 內容 |
| --- | --- |
| Work Contract | **SPEC-V2** v2.2（`home_work_01/doc/spec/SPEC-V2.md`；AC-V2-03、AC-V2-17(c)、AC-V2-22；R-V2-OBS-3／4／6／12／13、R-V2-SEC-3；INV-V2-2／3）。上位：V2 Outcome Contract `doc/governance/outcome-contract-v2.md`（ACCEPTED 2026-09-25，normative candidate `69c5a04`；AB-V2-2／10／13）。本次義務的定義：DA phase acceptance `doc/governance/decisions/phase-acceptance-SPEC-V2.md` §3.3（P-1～P-4 的內容、判準、紀錄位置）與 §2.7（post-key subject 規則）；`doc/acceptance/ACCEPTANCE-V2.md` §6.2（subject 內的計畫）；`decisions/derivation-SPEC-V2.md` §11 #1；decision A-6（`decisions/decision-20260923-high-risk-categories.md`）；#41 R1 F-2 的兩項程序註記（`audit/issue-41-c1-r1.md`）。 |
| 受審 subject | Phase acceptance subject ＝ **`9902026cc41725524f154185aeebd59057fbdadf`**。Preview 服務的 commit ＝ **`e75303c16da66c199e88fb558cb1e45e0434c322`**（branch `home_work_01-v2-implementation`；`git merge-base --is-ancestor 9902026 e75303c` 成立）。Reviewer `git diff --name-only 9902026..e75303c` ＝ `doc/governance/audit/issue-41-c1-r1.md`、`audit/spec-SPEC-V2-c1-r1.md`、`decisions/phase-acceptance-SPEC-V2.md`、`run/run-20260925-hw01-v2-formal.md`、`worklog/issue-41.md`（Bindings §7 record-only）＋ `doc/ticket/tickets-v2.md`（Reviewer 讀 diff：只有 #41 索引列的狀態文字與 commit 欄 `9902026`）；`git diff --stat 9902026 e75303c -- home_work_01 ':!home_work_01/doc'` 為空；`home_work_01/static` tree `a27d174e…` 與 `server.py` blob `0692caee…` 兩側相同——符合 phase acceptance §2.7 的 post-key subject 規則。審查時 HEAD `4299296`（相對 `e75303c` 只多 run record 一行）；`doc/acceptance/` 在 `9902026..4299296` 無任何變更。**部署**：`https://aiot-hw01-weather-8qeq3ey4t-nchu-aiot-class.vercel.app`；GitHub deployment **`6678056047`**（environment Preview、sha `e75303c`、creator `vercel[bot]`、created 2026-09-26T11:07:14Z、status success、`environment_url` ＝ 上述 URL）；Vercel deployment id **`dpl_du45X9VRwcPgRxfZJTnXRrSt7cFr`**（取自服務 HTML 中平台注入標籤的 `data-deployment-id`）。CI（`home_work_01 CI`）對 `e75303c`：`36237807133`、`36237805654` 皆 success。 |
| Audit 種類 | **cycle 1 Spec Integration Audit instance 的 post-key 證據補完**（phase acceptance §3.3「紀錄位置」：不是 R2、不是新 cycle、不是新 round）。範圍限 P-1～P-4、服務 commit 的確認與憑證安全；不重做 SIA 其餘範圍，不重開任何已閉合 finding（F-1 是依治理 §4.7 以新的平台證據對整合 subject 提出的新 finding）。 |
| 角色 | `primary_reviewer`（definition `gov-primary-reviewer`；Bindings §3.1 mapping `claude-opus-5-5`／`xhigh`） |
| Binding 證據 | 正式核對由派工者（Orchestrator）依 Bindings §3.4 記入 run record `doc/governance/run/run-20260925-hw01-v2-formal.md`。Reviewer 另以 Bindings §3.4 指令唯讀自我觀察（session `05b8408b-260a-46d3-a4fe-ec07e3ec365a`）：`agent-a55f579063a0b44bd` `gov-primary-reviewer` `[('claude-opus-5-5', 'xhigh')]`（meta description「Post-key verification P-1..P-4」）；與 SIA Reviewer `ad2f24768b95d2567`、#41 R1 Reviewer `a16d3b7e242f9d1aa` 為不同 instance。只供對照，不取代派工者核對。 |
| Independence（治理 §2.3、§4.6） | (1) **Fresh context**：未繼承 Executor、Orchestrator 或先前 Reviewer 的對話；派工文字、run record「preview obs／radar 200」的陳述、`ACCEPTANCE-V2.md`、#41 R1 與 SIA record 一律視為待驗證主張。(2) **Binding**：見上一列。(3) **Autonomous access**：自讀治理 §2.3、§4.1–§4.7，Bindings b3，Implementation Profile §6–§7，phase acceptance 全文，SPEC-V2 §2.2、§2.4 與 AC 列，derivation §11，OC-V2 AB 列，#35 R1／R2 與 #40 R1 的 F-2，#41 R1 F-2，`ACCEPTANCE-V2.md` §1、§6、§8；程式 `observation.py`、`radar.py`、`server.py`、`api/index.py`、`vercel.json`、`static/app.js` 相關段、README l. 400–420、480–491、570–578；git 歷史與 diff；GitHub deployments 與 CI；自寫 live 探測、瀏覽器檢查（headless Chrome／DevTools protocol）、並行與 stagger 量測，以及對匯出 `e75303c` 樹的本機上游停滯重現。(4) **Self-written record**：本紀錄由 Reviewer 以自己的 Write 工具寫入。**Model diversity：`diversity_lost`**——#35～#41 的 Executor 與本 Reviewer 同為 `claude-opus-5-5`（Bindings §5、b2 override；phase acceptance §2.1 的 harness 核對）；合法，不減損 §2.3 independence。 |
| 日期 | 2026-09-26；live 量測 11:14–11:38Z（19:14–19:38 +08:00） |

## 1. 方法、環境與憑證安全

- **環境**：Windows 11；`home_work_01/.venv` Python 3.12.14（`requests`、`websocket-client`、Pillow）；Chrome headless（DevTools protocol；全新 profile、無 cookie、`Network.setCacheDisabled`）。Scratch 全在 Reviewer scratchpad 新建的 `postkey/`；repo 內只寫入本紀錄（結束時 `git status --short` ＝ 本紀錄＋審查前即存在的 `grep.exe.stackdump`）。
- **對外請求**：(a) 對上述 public preview 的一般 GET（不登入、不帶 cookie）；(b) `gh api`／`gh run list` 讀 GitHub deployments 與 CI；(c) Vercel **公開文件** 3 頁（`/docs/functions/configuring-functions/duration.md`、`/docs/functions/limitations.md`、`/docs/fluid-compute.md`，皆 `last_updated: 2026-08-24`）。**Reviewer 沒有對 CWA 發出任何請求**（上游請求只由 preview 的伺服器端發出）；**沒有進入 Vercel 後台、沒有使用 Vercel 帳號 API、沒有讀取或列出任何環境變數**（RB-3「第三方帳號操作」；phase acceptance §3.3 P-2）。
- **憑證（RB-3 b3、#41 R1 F-2(b)）**：Reviewer **沒有**要求、讀取、印出、匯出或以 `vercel env pull` 取得 `CWA_API_KEY`；**沒有開啟** `home_work_01/.env`（本機停滯重現在不含 `.env` 的 `git archive` 匯出樹執行，以非金鑰格式的字串作為「已設定金鑰」）。金鑰外洩檢查只用金鑰格式規則：`ingestion/checks.py` 的 `KEY_PATTERN`（strict）與一個更寬的大小寫不敏感版本（broad），並計數 `Authorization`、`Bearer`、上游主機（`opendata.cwa.gov.tw`、`cwaopendata.s3`／`amazonaws`）與上游結構鍵；只輸出命中數（命中時只輸出偏移、sha256 前綴與長度）。掃描器自測：Reviewer 自造的合成 UUID 形字串（非金鑰；不寫入本紀錄以免觸發 repo 的憑證掃描）大寫版 strict 1／broad 1、小寫版 broad 1，一個含 `Authorization` 鍵與非空值的 JSON 片段計 1——規則確實能命中。
- **Preview 請求量**（不輪詢、不壓測）：`/api/observations/latest` 17 次、`/api/radar/latest` 13 次（含頁面自己發出的），其中多數落在伺服器重用視窗內；由此觸發的上游取得（不同的 Fetched Time）觀測 ≥ 5 次、雷達 ≥ 6 次。其餘為 `/`、`/api/health`、預報端點與靜態資產。

## 2. 服務 commit 的確認（phase acceptance §2.7）

| 項目 | 結果 |
| --- | --- |
| Deployment ↔ commit | GitHub deployment `6678056047`：Preview、sha `e75303c`、`vercel[bot]`、success、`environment_url` ＝ 受測 URL（`gh api repos/yotsubamomo/aiot-classwork/deployments?sha=e75303c…` 與 `…/deployments/6678056047/statuses`）。 |
| `e75303c` 與 `9902026` 的關係 | 後代；差異只在 record-only 路徑＋`tickets-v2.md` 狀態列（檔頭）→ 產品碼與 `9902026` 相同。 |
| 服務的靜態資產 | 對 `e75303c` 的 7 個 `home_work_01/static/**` blob（`git show`，原始位元組）逐一比對服務回應：`app.js`（137,047 B，sha256 `37d77e24…`）、`styles.css`（`3dd3dd79…`）、`data/basemap.js`（`fee530cd…`）、`data/counties.js`（`f721710d…`）、`vendor/leaflet.js`（`db49d009…`）、`vendor/leaflet.css`（`337bfca5…`）**位元組相同**；`index.html`（`/` 與 `/static/index.html` 回應相同）與 blob 的唯一差異是檔尾多一行 Vercel 注入的 `<script async data-explicit-opt-in="true" data-deployment-id="dpl_du45X9VRwcPgRxfZJTnXRrSt7cFr" src="https://vercel.live/_next-live/feedback/feedback.js">`（`diff` 只有 `416a417`）——平台注入，不在 subject 內（#41 R1 F-2(a)）。 |
| 行為面 | `/api/observations/latest` 成功本文頂層 7 個鍵 ＝ `observation.py:578–590`；每站 14 個鍵 ＝ `observation.py:352–368`；雷達標頭 `X-Radar-Time`／`X-Radar-Fetched-Time`／`X-Radar-Dataset` ＝ `server.py:238–241`；`/api/health` 本文 `{"forecast_day_count":7,"ingestion_time":"2026-09-24T02:24:50+08:00","region_count":6,"status":"ok"}` ＝ 提交的 `data.db` 快照（phase acceptance §2.3 的 `IngestionMetadata`）。 |

**結論：preview 服務的就是受理 subject `9902026` 的產品碼（經 record-only 後代 `e75303c` 建置）。**

## 3. P-1 — AC-V2-17(c) 觀測、AC-V2-22 觀測部分：**PASS**

- **API**（11:14:39Z，第一個觀測請求）：`GET /api/observations/latest` → **200**，`Content-Type: application/json`，`Cache-Control: no-store`，2.55 s；本文 294,117 B：`dataset` `O-A0001-001`、`observationTime` `2026-09-26T19:00:00+08:00`、`fetchedTime` `2026-09-26T19:14:41+08:00`（＝請求當下，即新取得）、`validStationCount` **840**、`receivedStationCount` 876、`stations[]` 840 筆（22 縣市皆有）、`representativeStationIds` 22 個。每站 14 欄（StationId、名稱、縣、鄉鎮、緯經度、該站 Observation Time、氣溫、六個可選欄位）；`airTemperature` 840 筆皆為有限浮點數；dataset Observation Time ＝ 各站最大值；可選欄位的無效值以 `null` 表示（weather 707、windDirection 8、windSpeed 8、precipitation 2、relativeHumidity 1、airPressure 1），本文中 0 個欄位等於哨兵碼（`X`／`-99`／`-98`／`T`／`990`）。本文不含上游結構鍵（`records`、`WeatherElement`、`cwaopendata`、`GeoInfo`、`ObsTime` 鍵皆 0）、上游主機 0、`Authorization` 0、金鑰格式 strict 0／broad 0；回應標頭同樣 0。
- **瀏覽器 1280×900**（11:17:41Z）：開 `/` → Now mode（`#mode-now` `aria-pressed="true"`）在 **1.69 s** 到達 `data-obs-state="success"`（無 STALE／UNAVAILABLE chip）；`Observation Time` ＝ `2026-09-26 19:00 +08:00`、`Fetched Time` ＝ `2026-09-26 19:14:41 +08:00`、`Valid stations` ＝ `840`——與頁面自己收到的 `/api/` 本文（DevTools `Network.getResponseBody` 讀回；與上項本文位元組相同，sha256 `9601c9e4…`，即 300 s 重用視窗內的同一份回應）逐字相符；兩個標籤逐字；兩個時間在視窗內可見；地圖上 22 個代表標記（DOM），截圖可見其中 9 個（DV-22 的密度規則，與其 §1 記錄的 1280 初始視野 9／22 一致）。
- **瀏覽器 375×812（mobile）**：同樣 success（1.30 s）、兩個時間與有效站數 ＝ 本文、22 個代表標記（DOM）。
- **Network log**：1280 session 15 個同源請求＋1 個同源 `blob:`（雷達影像）；375 session 13 個同源請求；**外部 0**。兩個 session 都沒有出現對 `vercel.live` 的請求（HTML 中有注入標籤；即使出現也屬平台注入，#41 R1 F-2(a)；見 O-2）。Console 只有瀏覽器自動請求 `/favicon.ico` 的 404（同源、非應用程式請求）。
- **`smoke.py`**（`e75303c` 版＝`9902026` 版）：`GET / -> 200  GET /api/health -> 200  (0.6s elapsed)  PASS`，`SMOKE PASS`，exit 0（11:18:45Z）。
- **Deployment ↔ commit**：第 2 節。

## 4. P-2 — AC-V2-17(c) 雷達、INV-V2-2 平台面（H-1）：**PASS**（回應面）；runtime log 面見末段

- **API**（11:14:42Z）：`GET /api/radar/latest` → **200 `image/png`**，72,393 B，PNG IHDR **3600×3600**，`X-Radar-Time: 2026-09-26T19:00:00+08:00`、`X-Radar-Dataset: O-A0058-006`、`X-Radar-Fetched-Time: 2026-09-26T19:14:44+08:00`、`Cache-Control: no-store`，2.30 s。之後 Reviewer 的 11 個雷達請求與頁面的 1 個全部 200 `image/png`（19:20 起 `X-Radar-Time` `19:10:00+08:00`，11:38Z 為 `19:20:00+08:00`）。
- **金鑰／上游／`Authorization` 掃描**：Reviewer 記錄的每一個回應——3 個單一探測、7 個靜態資產＋根頁、頁面收到的觀測本文與標頭、頁面收到的雷達標頭（該雷達本文 DevTools 讀回為 0 B，同一端點的其他 12 個回應本文皆已直接掃描）、17 個並行回應（×4、×4、×6、×3）、6 個 stagger 回應、3 個閒置後回應——本文與標頭的金鑰格式 strict **0**／broad **0**；`Authorization` 字樣 **0**；上游主機 **0**（stagger 的 6 個只做金鑰格式掃描）。回應標頭名稱只有 `Age`、`Cache-Control`、`Content-Encoding`／`Content-Length`／`Content-Type`、`Date`、`Server`、`Strict-Transport-Security`、`Transfer-Encoding`、`X-Robots-Tag`、`X-Vercel-Cache`、`X-Vercel-Id` 與三個 `X-Radar-*`。
- **瀏覽器（1280）**：按 `Radar: Off` → `Radar: On`（`aria-pressed="true"`），**2.73 s** 後 `data-radar-state="success"`；`Radar Time` 顯示 `2026-09-26 19:00 +08:00` ＝ 頁面收到的 `X-Radar-Time`（該回應 `image/png`、`X-Radar-Dataset: O-A0058-006`、`X-Radar-Fetched-Time: 2026-09-26T19:17:49+08:00`）。雷達圖層在 `.leaflet-radar-pane`：24 條 strip 的 `<img>` 全部為同源 `blob:` URL，影像 3600×3600，圖層 opacity 0.8。**圖層順序**（computed z-index）：backdrop **300** ＜ radar **350**（`pointer-events: none`）＜ overlay（22 個縣多邊形）**400** ＜ marker（22 個站標記）**600** ＜ tooltip 650——雷達在底圖之上、在縣界與標記之下。**像素證據**（同一視野，雷達關／開兩張截圖）：地圖區 360,640 px 中 2,773 px 改變（回波所在處；截圖可見馬祖附近、臺灣海峽與東南外海的回波），標記 pill 內部 21,780 px 中只有 34 px（0.16 %，邊緣反鋸齒）改變——標記畫在雷達之上。
- **Vercel runtime log**：acceptor **未提供** log 畫面（派工內容與 run record 皆無）；依 phase acceptance §3.3 P-2 記為「未提供；以本機 DEBUG-log 零洩漏證據（SIA §2 INV-V2-2）為據」——程式面：`observation.py:567–575`、`:592–596` 與 `radar.py:401–421` 只記 reason、上游狀態碼、站數、雷達時間與位元組數。log 面成為 **acceptor 於 release 時自行確認**的項目（V1 #21 F-3 先例），**不阻擋 addendum**。Reviewer 未進入 Vercel 後台。

## 5. P-3 — AC-V2-03 preview 抽樣：**PASS**

Oracle ＝ 頁面自己收到的 `/api/observations/latest` 本文（DevTools 讀回）；比較規則由 Reviewer 獨立寫出（氣溫：`/api/` 數值不變、至少一位小數；其他數值：JavaScript `String(Number(v))`；`null` → 「—」；時間：只重排、不換算），並另以數值相等核對（顯示數值 ＝ `/api/` 值）。

**(a) 全部 22 個代表標記**：pill 文字 ＝ 同站 `airTemperature`——**22／22 相等**（例：臺北 `466920` `28.9°`；阿里山 `467530` `11.9°`；新竹 `467571` `28.0°`；金門 `467110` `26.6°`；馬祖 `467990` `27.3°`；澎湖 `467350` `26.7°`）。截圖可見的 9 個 pill（27.3、28.9、26.6、28.2、28.6、26.7、11.9、27.6、28.6）即馬祖、臺北、金門、臺中、花蓮、澎湖、阿里山、高雄、臺東的 `/api/` 值。

**(b) 8 站的測站詳情**（County 選單 → 測站清單按鈕 → 詳情；全部欄位逐字比對，清單中的氣溫也比對）：

| 抽樣理由 | StationId（縣 站名） | `/api/` 值（摘要） | 頁面顯示（摘要） | 結果 |
| --- | --- | --- | --- | --- |
| relativeHumidity 為 null | `C0AC60`（新北市 三峽） | T 27.0、RH **null**、風 1.0／216.0、氣壓 1000.5、雨 0.0、weather null | `27.0 °C`、RH **—**、`1 m/s`、`216°`、`1000.5 hPa`、`0 mm`、weather **—** | 相等 |
| airPressure 為 null | `C2I260`（南投縣 北坑） | T 24.2、RH 89、氣壓 **null** | `24.2 °C`、`89 %`、氣壓 **—** | 相等 |
| windSpeed／windDirection 為 null | `C0TC30`（花蓮縣 虎頭山） | T 20.3、風速 **null**、風向 **null**、氣壓 885.7 | `20.3 °C`、**—**、**—**、`885.7 hPa` | 相等 |
| precipitation 為 null | `C0SE00`（臺東縣 樟原南溪） | T 23.1、雨 **null**、weather 多雲 | `23.1 °C`、雨 **—**、`多雲` | 相等 |
| weather 有值 | `C0AH00`（新北市 汐止） | T 29.3、weather 晴 | `29.3 °C`、`晴` | 相等 |
| 離島（連江縣） | `C0W110`（東莒） | T 27.4、風 3.9／192.0 | `27.4 °C`、`3.9 m/s`、`192°` | 相等 |
| 離島（金門縣） | `C0W240`（九宮） | T 27.1、氣壓 1004.3 | `27.1 °C`、`1004.3 hPa` | 相等 |
| 臺北市 | `C0A980`（社子） | T 28.0、風 0.0／0.0 | `28.0 °C`、`0 m/s`、`0°` | 相等 |

每站的名稱（`<名> station`）、`縣 · 鄉鎮`、StationId、該站 Observation Time（`2026-09-26 19:00 +08:00`）亦逐字相等；抽樣中 10 個 `null` 欄位全部顯示「—」，沒有任何一個以數值呈現。

**哨兵說明**：preview 上不能以金鑰讀取上游原文（RB-3），故「上游哨兵 → `/api/` `null`」的對應不在 preview 重驗，以 AC-V2-03 的離線證據為據（#35、SIA 已獨立驗證）；preview 可觀察的部分是：`/api/` 本文中 0 個欄位等於哨兵碼，且抽樣的全部 `null` 在頁面上都是「—」。

## 6. P-4 — decision A-6 preview 觀測驗證紀錄＋Vercel 時序／並行

### 6.1 A-6 preview 觀測驗證紀錄

URL `https://aiot-hw01-weather-8qeq3ey4t-nchu-aiot-class.vercel.app`；GitHub deployment `6678056047`；Vercel `dpl_du45X9VRwcPgRxfZJTnXRrSt7cFr`；sha `e75303c`（產品碼 ＝ `9902026`）。

| 時間（UTC） | 動作 | 結果 |
| --- | --- | --- |
| 11:14:33–11:14:48 | 單一探測＋資產比對 | health 200、觀測 200、雷達 200；6 個資產位元組相同、`index.html` 只多平台注入一行 |
| 11:17:41–11:17:53 | 瀏覽器 1280／375（P-1、P-2 overlay、P-3） | 22／22 項檢查 PASS |
| 11:18:45 | `smoke.py` | PASS（0.6 s） |
| 11:20:17–11:25:52 | 並行與 stagger（6.2、6.3） | 全部 200；金鑰格式 0 |
| 11:38:00–11:38:10 | 閒置約 12 分鐘後單一觀測、雷達、health | 200（7.69 s）、200（2.33 s）、200（0.32 s） |

### 6.2 量測

| 類別 | 量測 | 說明 |
| --- | --- | --- |
| 冷啟動 | 閒置約 6 分鐘後第一個請求 `/api/health` **6.41 s**（不觸及 CWA）；閒置約 12 分鐘後第一個請求 `/api/observations/latest` **7.69 s**（200，新取得 `19:38:07`） | function 在 `iad1`（`X-Vercel-Id: hkg1::iad1::…`）；冷啟動約 5–6 s |
| 觀測，新取得（warm） | 2.55 s；並行 ×4：2.13–2.47 s；×6 中另一 instance：1.86–2.05 s；stagger 首請求 2.12 s | 上游取得＋正規化＋約 294 KB 回應 |
| 觀測，重用 | 0.34–0.74 s | 300 s 重用視窗 |
| 雷達，新取得 | 2.30 s；×4：2.41–2.42 s；×3：2.50–2.66 s；stagger 首請求 2.30 s；閒置後 2.33 s | metadata＋影像兩次上游請求 |
| 頁面終態 | Now mode success 1.69 s（1280）、1.30 s（375）；Radar success 2.73 s | 頁面上限 20 s（`app.js:263` `OBS_TIMEOUT_MS`、`:297` `RADAR_TIMEOUT_MS`）；最壞的冷啟動觀測 7.69 s 亦在其內 |
| 並行 | 觀測 ×4、×6，雷達 ×4、×3，stagger 觀測與雷達各 3：**23 個回應全部 200**，無平台錯誤頁 | 最長未被平台截斷的 invocation：7.69 s（閒置後單一請求） |

### 6.3 平台的並行模型（新證據）

Stagger（11:25:45Z，所有 instance 的觀測與雷達重用視窗都已過期：之前最後一次觀測取得 `19:20:34`、雷達 `19:22:37`）：請求 0 於 t=0 發出，請求 1、2 於 t=0.8 s、1.4 s 發出。

| 路徑 | 請求 | 開始 | 結束 | 耗時 | 伺服器 Fetched Time |
| --- | --- | --- | --- | --- | --- |
| 觀測 | 0／1／2 | 0.000／0.802／1.401 s | 2.119／2.100／1.737 s | 2.119／1.299／0.336 s | 三者皆 `19:25:47` |
| 雷達 | 0／1／2 | 0.001／0.801／1.401 s | 2.303／2.306／2.285 s | 2.302／1.505／0.884 s | 三者皆 `19:25:50` |

新取得在此部署至少需約 1.8 s（觀測）／2.3 s（雷達）；請求 1、2 耗時更短且與請求 0 同一個 Fetched Time（雷達三者結束時間相差 21 ms 內），表示它們沒有自行取得，而是在**請求 0 所在的同一個 instance** 上等待 `self._lock`（`observation.py:549`、`radar.py:384`）或取用其剛寫入的快取——當時其他 instance 的快取都已過期，落在別的 instance 就必須自行取得。因此**這個部署有 in-function concurrency**（Vercel Fluid compute 的 optimized concurrency；公開文件：Python 可用、2025-04-23 起新專案預設啟用）。佐證：×6 並行中 4 個取用 `19:20:19` 的快取、2 個來自另一 instance 的 `19:20:34`（路由分散到 ≥ 2 個 instance，但同時請求會共用 instance）。排除 edge 層合併：觀測與雷達回應都帶 `Cache-Control: no-store`（`server.py:218`、`:242`），已記錄其快取標頭的回應為 `X-Vercel-Cache: MISS`，且同一波並行得到兩個不同的 Fetched Time。

### 6.4 平台時限

- **Reviewer 無法直接讀取**專案的 function 時限設定（Fluid 開關、Default Max Duration 只在 Vercel 後台／帳號 API；RB-3，未接觸）。`vercel.json` 只有 legacy `builds`／`routes`，沒有 `functions`／`maxDuration`。
- **公開文件**（2026-08-24）：Fluid compute 下 max duration 預設 **300 s**（Hobby 預設＝上限 300 s；Pro／Enterprise 預設 300 s、上限 800 s）；逾時回 504 `FUNCTION_INVOCATION_TIMEOUT`；預設 region `iad1`（與 `X-Vercel-Id` 相符）。6.3 顯示本部署是 Fluid 行為，故適用的文件預設為 300 s。
- **觀察**：30 個以上的 API 回應無平台逾時，最長 7.69 s（含冷啟動）。
- **判定**：8 s 上游上限 ＜ 300 s（也 ＜ README 保守引用的 10 s）；**「平台時限等於或低於 8 s 上限」的 DA flag 條件未成立**（derivation §11 #1 的時限衝突不存在）。殘餘不確定：後台層級把 Default Max Duration 設到 ≤ 8 s 的覆寫無法由 Reviewer 排除，但沒有任何跡象（包括 7.69 s 的 invocation 未被截斷）；acceptor 可於 release 時在後台順便確認（非必要）。

### 6.5 上游停滯＋並行（#35 R1 F-2、#40 R1 F-2）

- 在 live preview 上**無法**讓 CWA 停滯（需改動 subject 或上游），故以 subject 自己的程式在本機重現：匯出 `e75303c` 樹（無 `.env`），`server.create_app` 注入以模擬停滯上游（sleep 遠超 deadline）建構的 `LatestObservationService`／`RadarService`，以 threaded WSGI server 在 loopback 上服務（＝一個 instance 同時處理多個 invocation）：單一觀測 8.03 s → 504 `upstream_unreachable`；**4 個並行觀測 → 8.01／16.02／24.04／32.05 s**，皆 504 `upstream_unreachable`；**3 個並行雷達 → 8.02／16.03／24.03 s**；上游嘗試 8 次（1＋4＋3：失敗不快取，排隊的每個請求都再試一次）。
- 與 6.3、6.4 合併：在此平台上，CWA 停滯時同一 instance 的第 k 個並行請求約在 8k s 回答；在文件的 300 s 時限內可容納 k ≤ 37（38 × 8 = 304 s），超過才會變成平台 504。每個頁面請求都另被頁面 20 s 上限帶到終態（Stale／Unavailable，＜ §5.3 的 30 s 儀器）；但第 3 個以後（≥ 24 s）的排隊請求，頁面顯示的是它自己的「沒有回應」類別，而非伺服器的 `upstream_unreachable`；頁面放棄的請求仍在伺服器端佔住佇列。→ 見 F-1。

### 6.6 P-4 的 DA 判定

- 派工所列的 DA flag 條件（平台時限 ≤ 8 s 上限的假設）**未觸發**。
- 但 #35 R1 F-2 的 non-blocking 理由所依據的部署模型前提（「每個 instance 一次只處理一個請求」）經 6.3 證實**不成立**，而 #35 R2 約定「若平台證據顯示會超過界限，依 derivation §11 #1 route Design Authority」、phase acceptance §3.3 P-4 列把平台時序議題的處理交給 DA——因此以 F-1 記錄並交 **Design Authority** 在 addendum 中處置（non-blocking，不是時限衝突）。

## 7. 高風險類別核對（decision A-1；derivation §6）

| 類別 | 觸及方式 | 核對了什麼 | 結果 |
| --- | --- | --- | --- |
| H-1 憑證與機密 | P-2（INV-V2-2 平台面，DA 指定為必要） | 所有記錄的回應本文與標頭、服務的前端資產與 HTML、Reviewer 全部 evidence 檔案與本紀錄的金鑰格式掃描；瀏覽器只呼叫同源 `/api/`（外部 0），影像為同源 `blob:`；回應無上游 URL、無 `Authorization` | **成立**（回應面）；Vercel runtime log 面待 acceptor（第 4 節末段） |
| H-2 老師指定介面 | 部署上的既有介面 | `/api/health` 200 與本文 ＝ 提交快照；`smoke.py` PASS；頁面 session 中 `/api/regions`、`/api/regions/<Region>/series`、`/api/days`、`/api/days/<date>` 皆由同源載入；產品碼 ＝ `9902026`（SIA／DA 的老師 SQL 與 blob 比對適用） | **成立** |
| H-3 資料語義與標示 | P-1、P-3 | `Observation Time`、`Fetched Time` 標籤逐字且可見；標記為單站值（22／22 ＝ `/api/`）；值「如發布」、`null` 顯示「—」；`Radar Time` 與觀測時間分開標示 | **成立** |

## 8. Findings 與觀察

### F-1（Low，non-blocking）——部署確有 in-function concurrency：#35／#40 R1 F-2 的鎖序列化在 preview 上可達

- **證據**：6.3 的 stagger（同一 instance 共用一次取得，雷達三者 21 ms 內結束）與 ×6 並行；6.5 的本機重現（8.01／16.02／24.04／32.05 s；8.02／16.03／24.03 s；上游嘗試 8 次）；`observation.py:549`（`with self._lock:` 涵蓋 `fetch_upstream`）、`radar.py:384`（涵蓋 `fetch_product`）；Vercel 文件（Fluid optimized concurrency 適用 Python、新專案預設啟用、預設時限 300 s）。
- **契約**：R-V2-OBS-13（伺服器逾時 ＜ 平台時限、停滯以 `upstream_unreachable` 分類而非平台 gateway 錯誤、前端把非 JSON／平台錯誤當 failure、終態 30 s 儀器）；R-V2-OBS-12（四類失敗在使用者可見層可辨）；雷達依 R-V2-RAD-4 同樣適用。
- **為何 non-blocking**：契約保證仍成立——8 s ＜ 300 s；排隊請求在 k ≤ 37 時仍由伺服器以 `upstream_unreachable` JSON 回答（不是平台錯誤）；每個頁面請求在 20 s 內到達終態。殘餘只在「CWA 停滯＋同一 8 s 視窗內 ≥ 3 個並行請求落在同一 instance」時出現：第 3 個以後的使用者看到的是頁面的「沒有回應」類別而非 `upstream_unreachable`，且持續流量下伺服器端佇列會累積（頁面放棄的請求仍佔位）。本 finding 不主張違反任何契約條款。先前的處置（#35 R1 F-2 Medium → #35 R2 帶到 #41；#40 R1 F-2 Low；phase acceptance §5.3「修正屬 HOW，只能在後續合法授權的變更中處理」）的**前提**改變：當時假設「同一 instance 同時處理多個請求」在部署上不發生，現已證實會發生；另一方面當時擔心的「第 2 個請求 16 s 超過 10 s 平台時限」因文件時限為 300 s 而不成立。
- **Disposition**：Owner **Design Authority**——在 `phase-acceptance-SPEC-V2-addendum-<date>-postkey.md` 決定是否維持 §5.3 的既有處置（任何修正都是結案後、需 acceptor 直接指示的變更，phase acceptance §10）。不延長本 cycle；不影響 P-1～P-3 的判定。

### O-1（觀察，無契約影響）——README 的平台時限用語

README l. 409–410、487–488「below Vercel's smallest default function duration (10 s)」與 l. 574「The server itself answers within about 8 s even when CWA stalls」：前者相對目前文件（Fluid 預設 300 s）是保守的舊值、結論（8 s ＜ 時限）仍正確；後者對單一請求成立，對 F-1 的排隊請求不成立（README 同段已寫明頁面 20 s 上限與「the platform holds the request」的處理）。R-V2-OBS-13 只要求 README 記載逾時值，已記載。若 acceptor 想更新措辭，是結案後的 Lightweight 文件修正（phase acceptance §10）。

### O-2（觀察）——平台注入的 `vercel.live` toolbar

服務的 HTML 含注入標籤（第 2 節），但兩個 headless session 都沒有對 `vercel.live` 發出請求；不論是否請求，都屬平台注入而非 AC-V2-16／INV-V2-3 的前端違規（#41 R1 F-2(a)）。應用程式本身的外部請求為 0。

### 其他

- `ACCEPTANCE-V2.md` §1／§5／§6.2／§7 的 BLOCKED 字樣與 #41 R1 F-1 的數字：Reviewer 唯讀，未修改；審查時 `doc/acceptance/` 無 post-key delta。若之後有人依 phase acceptance §3.3 更新該檔，那個 delta 不在本紀錄的涵蓋內，須依該節另行確認只含狀態與引用文字。
- 沒有需要 route Design Authority 的契約語義不足或 boundary 疑義；沒有 blocking finding。

## 9. 需要其他 authority 的事項

| 事項 | Authority | 理由 |
| --- | --- | --- |
| 寫 addendum 結清 P-1～P-4，並處置 F-1 | **Design Authority**（Orchestrator 派工） | phase acceptance §3.3「結清」列、P-4 列（平台時序議題由 DA 處理）；#35 R2 的 route 約定 |
| Vercel runtime log 的金鑰格式自查（P-2 log 面） | acceptor（release 時） | phase acceptance §3.3 P-2；Reviewer 不得進入 Vercel 後台（RB-3） |
| （選擇性）在後台確認 Fluid 與 Default Max Duration | acceptor | 6.4 的殘餘不確定；非 P-4 判定的必要條件 |
| 原樣 commit 本紀錄；在 run record 記 binding 核對；`worklog/issue-41.md` 補指向本紀錄的一列 | Orchestrator | Bindings §3.5 第 4 點；phase acceptance §3.3「紀錄位置」 |
| 合併（RB-1）、繳交（RB-2）、合併後 production smoke 與觀測抽樣（AC-V2-22 release evidence） | acceptor | Bindings §2.6；SPEC-V2 §6.4 |

## 10. Evidence（全部唯讀或只寫入 Reviewer scratchpad；未提交）

- Scratchpad `postkey/`：`pk_common.py`（掃描規則）；`pk_probe1.py` → `probe1.json`、`obs1.json`（sha256 `9601c9e4…`）、`radar1.bin`（sha256 `e99a505d…`）、`served_root.html`、`blob_index.html`；`pk_browser.py` → `browser_results.json`（22 項檢查）、`page_obs_body_1280.json`、`shot_1280_radar_off.png`、`shot_1280_radar_on.png`、`shot_375_now.png`；`pk_concurrency.py` → `p4_bursts.json`、`p4_cold.json`；`p4_radar_burst2.json`；`pk_stagger.py` → `p4_stagger_1125.json`；`pk_local_stall.py` → `p4_local_stall.json`（匯出樹 `subject/home_work_01`）；`docs_duration.md`、`docs_limits.md`、`docs_fluid.md`；`pk_scan_all.py`。
- **最終金鑰格式掃描**（`pk_scan_all.py`，於本紀錄定稿後執行：`postkey/` 全部檔案〔不含匯出樹〕、本紀錄，以及 session `tasks/*.output`）：唯一命中在本 Reviewer 自己的 harness transcript（`tasks/a55f579063a0b44bd.output`），sha256 前綴 `60723d23`／`626ee905`、長度 40——與 Reviewer 自造的合成自測字串（大寫／小寫）的 sha256 前綴與長度完全相同，即第 1 節的掃描器自測輸入，不是金鑰；其餘所有 evidence 檔案、所有 preview 回應與本紀錄 **0 命中**。本紀錄另以 repo 的 `ingestion.checks.scan_file` 檢查（金鑰格式與非空 `Authorization` 值）：無 finding。
- 指令（摘要）：`git diff --name-only 9902026..e75303c`、`git diff 9902026..e75303c -- home_work_01/doc/ticket/tickets-v2.md`、`git rev-parse e75303c:home_work_01/static 9902026:home_work_01/static`、`git merge-base --is-ancestor 9902026 e75303c`、`git ls-tree -r --name-only e75303c home_work_01/static`、`git show e75303c:<path>`、`git archive e75303c home_work_01`；`gh api repos/yotsubamomo/aiot-classwork/deployments?sha=e75303c…`、`gh api …/deployments/6678056047/statuses`、`gh run list --commit e75303c…`；`python smoke.py <preview>`；Bindings §3.4 核對指令（只讀本 agent 的 meta 與 jsonl）。

## 11. 結論

P-1（AC-V2-17(c) 觀測、AC-V2-22 觀測部分）**PASS**；P-2（AC-V2-17(c) 雷達、INV-V2-2 回應面）**PASS**，runtime log 面依 phase acceptance §3.3 交 acceptor 於 release 自查、不阻擋 addendum；P-3（AC-V2-03 preview 抽樣）**PASS**；P-4 **已記錄**（冷啟動 6.41／7.69 s、新取得約 2–2.7 s、重用 0.3–0.7 s、頁面終態 ≤ 2.73 s、並行 23 個回應全部 200；平台有 in-function concurrency；文件時限 300 s，8 s 上限的 DA flag 條件未觸發）。服務的 deployment 對應受理 subject 的產品碼；Reviewer 未讀取、印出或匯出任何金鑰，所有回應與 evidence 的金鑰格式掃描為 0。F-1（Low，non-blocking）交 Design Authority 於 addendum 處置。

P-1..P-3 PASS + P-4 recorded（residue verified）

VERDICT: CLOSURE
