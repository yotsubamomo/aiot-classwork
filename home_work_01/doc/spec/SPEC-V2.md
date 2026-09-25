# Delta Spec V2: HW01 Weather Map V2（`home_work_01/`）

- **專案識別**：`home_work_01`（老師稱 HW10／Part 5）；本檔是 **V2 Delta Spec**，以參照繼承 V1 Spec v1.1，只寫 V2 需要新增、延伸、re-scope 或 supersede 的部分。
- **Spec 版本**：**v2.2**（2026-09-25；v2.0 同日 derive，v2.1 與 v2.2 為 acceptor 指示的 DA 修正，見第 10 節版本紀錄）
- **狀態**：**DERIVED — effective as derived contract of the accepted V2 Outcome Contract**（治理 §1.2：derived contract 的成立不需 acceptor 逐份核准）。效力條件與重新 derive 條件見第 0 節。
- **Derived 自**：V2 Outcome Contract [`../governance/outcome-contract-v2.md`](../governance/outcome-contract-v2.md)（**ACCEPTED 2026-09-25**；normative §1–8 ＝ candidate `69c5a049104b2fd96289d10ff938c2c8a6d59bd4`；接受紀錄 commit `f853bcbc69ed75a27b77aeb609daabe103c96a25`）；盤點 [`../brief/BRIEF-V2.md`](../brief/BRIEF-V2.md)（同一 candidate；附錄 A 為非契約建議，本檔不採為需求）。
- **Inherited baseline（以參照繼承，不改寫）**：V1 Outcome Contract [`../governance/outcome-contract.md`](../governance/outcome-contract.md)（ACCEPTED 2026-09-23）；V1 Spec [`SPEC.md`](SPEC.md) **v1.1 EFFECTIVE**；V1 derivation record [`../governance/decisions/derivation-SPEC.md`](../governance/decisions/derivation-SPEC.md)；decision records DR-1～DR-22 與 phase acceptance（含兩份增補）；V1 結案實作 ＝ `main` `ef15d3e`（V1 squash merge）＝ 現行 `main` `8c4667d` 的 `home_work_01/` 內容。
- **上位契約**（唯讀，不變）：[`../requirement/REQUIREMENTS.md`](../requirement/REQUIREMENTS.md) Part A、課程總覽 §1–21。Part B（B2-2～B2-4、B4、B16、B22、B24）只是 V2 構想的來源，經 V2 Outcome Contract 明確採用；Part B 的架構（FastAPI、React／Next.js、Windy）仍為 REFERENCE／FUTURE。
- **Derivation record**：[`../governance/decisions/derivation-SPEC-V2.md`](../governance/decisions/derivation-SPEC-V2.md)（含本次 derive 的 DA 裁決 DV-1～DV-19、boundary determination、高風險類別判定）。
- **治理**：Minimal Operational Governance v2.0；Project Bindings **b3**（RB-3 兩個金鑰授權位置）。
- **Issue tracker**：Tickets 尚未 derive（本檔只做 Spec derivation；Ticket derivation 另行進行並記入 derivation record）。

## 0. 狀態與效力

| 項目 | 內容 |
| --- | --- |
| 效力 | 自 2026-09-25 起為 V2 Outcome Contract 的有效 derived contract。Executor、Reviewer、Orchestrator 以本檔＋V1 Spec v1.1（依第 1 節的繼承規則）為 V2 work item 的契約。 |
| 與 V1 Spec 的關係 | V1 Spec v1.1 **normatively 不變**。本檔第 1 節逐條列出受 V2 影響的 V1 條款及其效果（re-scope／extend／supersede／delta／reaffirm）；未列出的 V1 條款一律原樣有效。本檔條款與 V1 條款對同一事項有不同規定時，**只在第 1 節明列的範圍內**以本檔為準；第 1 節未列的 V1 條款不得被本檔隱性重新解讀。 |
| 重新 derive 條件 | V2 Outcome Contract 的 normative 內容（§1–8）若有 scope、requirement、架構、acceptance boundary 或 authority／authorization 條款的變更，本檔須由 Design Authority 重新 derive 或以 derivation record 修訂確認未受影響。 |
| 不在本檔內 | Ticket；實作；測試；README 變更；`CONTEXT.md` 變更（本檔只規定其義務）；Orchestrator 啟動。 |

**標記約定**

- 來源類型：**OC** V2 Outcome Contract 條款（§2.5 S-n、§2.6 C-n、§3 AB-V2-n、§2.4 表列）｜**V1** 繼承的 V1 條款（Spec v1.1 R／AC／INV、DR-n）｜**G** Grill 裁決（D-n／P-n，只作追溯，OC 已承載其語義）｜**B** Bindings b3｜**DV** 本次 derive 的 DA 裁決（derivation record §3）。
- Scope class：**V2 Core**（ENHANCED REQUIRED）、**V2 Radar**（ENHANCED REQUIRED）。OPTIONAL／Later 只出現在第 8 節。本專案不使用「V2 MVM」；「MVM」專指 Part A 評分基線，V2 不改變它。
- MUST／SHOULD／MAY 依治理用語。SHOULD 偏離須在 worklog 記理由。
- 「Now mode」「Forecast mode」「Latest Observation」「Observation Time」「Fetched Time」「Refresh」「Re-ingestion」「Stale」「Unavailable」依 BRIEF-V2 §9 詞彙 delta（接受後併入 `CONTEXT.md`，R-V2-DOC-4）。
- 「地圖視窗（map viewport）」指 Leaflet 地圖容器的可見區域；「驗證視野」指第 5.3 節的兩個驗證 viewport（桌機 ≥ 1024 px、375 px）。
- 「WHAT」是契約；標示為「HOW」或列於第 4.2 節者交給實作。第 5.3 節的「驗證儀器（verification instrument）」是 DA 為客觀驗收選定的具體數值，**不是產品語義**：Executor 可以選不同數值，只要第 5.3 節列出的產品語義判準仍成立並記錄。

## Problem Statement

V1 已交付並結案：一個產品、兩個呈現層；部署於 Vercel 的 Dashboard 有六區七日預報的 Leaflet Taiwan Map（Forecast 語義、專案推導值）。V2 要把這張地圖升級為 map-first 的互動天氣介面：預設顯示 CWA 測站的 **Latest Observation**（O-A0001-001，逐時），可從全臺下鑽到縣、再到測站，手動 Refresh，永遠看得到 Observation Time 與 Fetched Time，並清楚區分 stale／unavailable；再加一個最新雷達回波 overlay。V1 的六區預報地圖原樣保留為 **Forecast mode**；下方 Forecast dashboard 不變。

這帶來三個必須在契約層處理的變化：(1) 部署的 Dashboard 第一次需要伺服器端向 CWA 取資料與一把金鑰（V1 的「呈現層不呼叫 CWA、部署不需 secret」須 re-scope／supersede，且只限觀測與雷達路徑）；(2) 頁面同時承載兩種語義（CWA 發布的觀測值、專案推導的預報相容性值），必須可見地分開；(3) 三條資料路徑（Observation／Forecast／Radar）必須各自降級，V1 的頁面層級錯誤對應（DR-19）在 V2 有明確的 delta。本檔把 V2 Outcome Contract 的 accepted 語義寫成可逐條驗收、可直接開 Ticket 的 delta 契約。

## Solution

```text
Taiwan Map（Dashboard）
├── Now mode（預設）
│   ├── browser ──/api/──▶ Flask（Vercel 單一 function）──server-side, key──▶ CWA O-A0001-001
│   │                     正規化／裁剪 ──▶ Latest Observation（stations、Observation Time、Fetched Time）
│   ├── Taiwan-wide（每縣 ≤ 1 代表測站）→ County（縣脈絡、測站清單）→ Station（詳情）→ Back to Taiwan
│   ├── Refresh（手動；success／stale／unavailable）
│   └── Radar overlay（顯示／隱藏、時間戳；browser ──/api/──▶ 伺服器端 ──▶ CWA O-A0058 系列）
└── Forecast mode：V1 六區七日預報地圖（Select Date、導出色帶、DERIVED 標示）語義不變
下方 Forecast dashboard：Select Region、Weekly summary、折線圖、表格 —— 不變
Grading App `app.py`、ingestion、`data.db`、共用預報查詢模組、預報 `/api/`、`/api/health` —— 不變
```

**核心設計（契約）**

- **兩種語義、兩個模式。** 觀測值只在 Now mode，標示為 CWA 測站觀測（如發布）；預報相容性值只在 Forecast mode 與下方 dashboard，維持 V1 的 DERIVED／PROJECT-DERIVED 標示；兩者不共用圖例或色階，永不互相流入。
- **伺服器端才碰 CWA，且只為觀測與雷達。** 瀏覽器只呼叫本應用 `/api/`；金鑰只存在於兩個授權位置（未追蹤本機 `.env`、acceptor 填入的 Vercel 專案環境變數），只在伺服器端執行期讀取；預報讀取路徑與 Grading App 仍不需要金鑰、不呼叫 CWA。
- **Latest Observation ＝ latest published, bounded staleness。** 顯示伺服器最近一次成功取得的最新觀測；Observation Time 與 Fetched Time 永遠可見；短暫共用重用視窗有上限；較舊的 Observation Time 永不取代較新；Stale 只以失敗為基準。
- **三條路徑獨立降級。** 觀測失敗只影響 Now mode 的觀測層；預報快照失敗依 V1 語義影響 Forecast mode 與下方 dashboard；雷達獨立；`/api/health` 語義不變。
- **契約不要求持久伺服器狀態。** 快取／重用是 HOW；伺服器只回「成功」或「分類失敗」，Stale 是介面狀態。
- **不列舉 22 個 StationId。** 代表測站以確定性、有文件、可客觀驗證的規則選出。

## User Stories（V2 delta）

1. As a Dashboard 訪客, I want 打開頁面就看到全臺各縣的最新測站氣溫, so that 不用操作就知道現在各地多熱。
2. As a Dashboard 訪客, I want 看到這些觀測是幾點的、伺服器幾點取得的, so that 我知道資料有多新。
3. As a Dashboard 訪客, I want 點一個縣看到縣內測站與最高／最低測站, 再點測站看詳情, 然後回到全臺, so that 我能從全貌下鑽到細節。
4. As a Dashboard 訪客, I want 按 Refresh 拿最新資料；失敗時保留舊資料並看到清楚的 stale 標示, so that 我永遠不會看到空白或誤以為舊資料是新的。
5. As a Dashboard 訪客, I want 打開雷達回波看目前降水在哪裡, so that 氣溫與天氣脈絡一起看。
6. As a Dashboard 訪客, I want 切到 Forecast mode 看 V1 的六區七日預報地圖, so that 老師 Part A 的加分地圖仍在原位。
7. As a 手機使用者, I want 375 px 下地圖仍是主角、縣／測站詳情在可關閉的底部資訊面, so that 手機上也能操作。
8. As a 作業擁有者（acceptor）, I want 金鑰只在 `.env` 與我親自填入的 Vercel 環境變數, 永不進 repo／前端／log／evidence, so that 公開部署不洩漏憑證。
9. As a 授課老師, I want Part A 的評分產物（Grading App、`data.db`、預報 dashboard、加分地圖）完全不變且容易找到, so that V2 不影響評分。
10. As a 維護者, I want V1 自動化測試維持全綠、V2 新增測試不需網路與金鑰, so that CI 穩定。

## 1. 繼承規則與 V1 delta 表

### 1.1 繼承規則

1. V1 Spec v1.1 的全部 R／AC／INV、§4.1 契約固定、§5 測試決定、§6 驗證策略，以及 DR-1～DR-22 與 DR-20／DR-21 核定的 HOW，**原樣有效**，除非在 1.2 表被列為 re-scope／supersede／delta。
2. 「extend」的條款：V1 文字不變，本檔在其上加 V2 的額外義務或適用範圍；兩者同時成立。
3. 「re-scope」的條款：V1 文字不變，但其適用範圍依本表縮小或擴大；縮小的範圍由本檔對應的 R-V2 承接。
4. 「supersede（V2 起）」的條款：對 V2 之後的部署 Dashboard 不再適用，由本檔對應條款取代；對 V1 結案 subject 的歷史 evidence 不回溯。
5. 「delta」的條款：V1 語義在 V2 有明確變更，變更內容以本檔為準。
6. 「reaffirm」的條款：V1 文字與適用範圍完全不變，本檔只重申並要求回歸證據。

### 1.2 受 V2 影響的 V1 條款（與 V2 Outcome Contract §2.4 一致；未列者一律不變）

| # | V1 條款 | 效果 | V2 delta（依據） | 承接的 V2 條款 |
| --- | --- | --- | --- | --- |
| Δ-1 | OC AB-5「兩個呈現層…應用程式不呼叫 CWA API」；Spec INV-6「呈現層不呼叫 CWA」 | **re-scope** | 對預報路徑（Grading App、共用預報查詢模組、預報 `/api/`、`/api/health`、Forecast mode、下方 dashboard）繼續完整有效。部署 Dashboard 新增 server-side 觀測／雷達路徑：瀏覽器 → `/api/` → 伺服器端向 CWA 取得 → 正規化／裁剪。（OC §2.4 列 1；C-1；D-2） | INV-V2-1、R-V2-SEC-1、R-V2-SEC-2 |
| Δ-2 | Spec R-SHR-5、R-DS-5「Python 端不得 import HTTP client…不得含 `opendata.cwa.gov.tw`」；AC-04(a)；R-TC-1 靜態檢查 | **re-scope** | 禁止範圍縮為 `app.py`、`weather_query.py` 及其單元內 import closure；部署 Dashboard 後端得含 V2 伺服器端 CWA 存取。靜態檢查依此 re-scope、只加不減；不要求特定模組結構。瀏覽器端 JS 資料請求仍只指向 `/api/`。（OC §2.4 列 2；D-2、D-17(6)） | R-V2-SEC-2、R-V2-SEC-4、AC-V2-16 |
| Δ-3 | Spec R-DS-8「執行期不需要任何環境變數或 secret」；R-SEC-3「部署的 Dashboard MUST 不需要任何 secret；Vercel 專案不設定 CWA 金鑰」；AC-07(e)；Spec §4.1「憑證…Dashboard 不需 secret」 | **supersede（V2 起）** | 部署的 function 為觀測／雷達路徑自 Vercel 專案環境變數讀取 CWA 金鑰；預報路徑仍不需 secret。金鑰由 acceptor 親自填入，不印出、不匯出、不提交、不進前端、不進 log／evidence。AC-07(e) 的「Vercel 專案不需環境變數」對 V2 部署不再適用，由 AC-V2-17 取代。（OC §2.4 列 3；D-3） | R-V2-SEC-3、INV-V2-2、AC-V2-17 |
| Δ-4 | Bindings RB-3；Spec R-SEC-1「唯一授權位置」；INV-5；OC §2.5、AB-8 | **extend** | Vercel 專案環境變數為第二個授權位置（Bindings b3 已生效）。AB-8 其餘條件（不進 git、log、前端、文件、evidence）不變並適用於 V2；R-SEC-1 的掃描範圍延伸到 V2 新增的樣本、evidence 與程式路徑。（OC §2.4 列 4；D-3） | INV-V2-2、R-V2-SEC-3、R-V2-SEC-5 |
| Δ-5 | OC §2.2 ENHANCED「Leaflet Taiwan Map…」；AB-14；Spec R-EN-3、R-EN-4、AC-17、AC-18；DR-20 全部（含 DR-20.3 核定 HOW、DR-21） | **extend（retain as Forecast mode）** | 這些條款在 **Forecast mode** 內原樣成立（AC-17「初始視野涵蓋六個標記」以進入 Forecast mode 時為準）。Taiwan Map 預設為 Now mode；模式切換必須明顯有標籤；README 與驗收證據必須讓 Forecast mode（老師 Part A 加分地圖）容易找到。不搬移、不移除。（OC §2.4 列 5；D-6） | R-V2-MODE-1～5、AC-V2-01 |
| Δ-6 | Spec R-EN-1（UI 品質清單）、AC-19（三種狀態截圖）；R-EN-7（整合） | **extend** | 清單同樣適用於 V2 的新介面（模式切換、面板、底部資訊面、Now mode 狀態）；「三種狀態」在 Now mode 涵蓋 stale／unavailable。（OC §2.4 列 6；D-11、D-15） | R-V2-RSP-8、AC-V2-14 |
| Δ-7 | Spec R-DS-6；DR-19（預報快照失敗 → 頁面層級 error 遮蔽整個 dashboard） | **delta** | 三條路徑獨立降級：預報快照失敗依 V1 語義影響 Forecast mode 與下方 dashboard（DR-19 的「頁面層級」在 V2 收斂為「預報區段層級」），不得停用健康的 Now mode；觀測失敗只影響 Now mode；雷達獨立。AC-10「頁面顯示錯誤狀態」對受影響部分仍成立。（OC §2.4 列 7；D-13） | R-V2-DEG-1～5、INV-V2-7、AC-V2-09 |
| Δ-8 | Spec R-DS-2、DR-7、DR-9、AC-15、AC-16、AC-22（`/api/health`、smoke） | **reaffirm** | `/api/health` 保持 V1 部署健康語義，永不依賴 CWA 即時可用性或金鑰；觀測／雷達狀態另行揭露；`smoke.py` 與 smoke workflow 不變。（OC §2.4 列 8；P-24） | R-V2-DEG-5、INV-V2-4、AC-V2-09、AC-V2-22 |
| Δ-9 | Spec AC-04(b)、DR-20.4、DR-20 X-1（前端資料請求只指向 `/api/`、零外部請求） | **reaffirm** | Radar 影像與觀測資料皆經 `/api/`；不新增前端外部主機例外；`_ALLOWED_FRONTEND_URLS` 仍只容許非請求常數。（OC §2.4 列 9；D-7） | R-V2-SEC-1、INV-V2-3、AC-V2-16 |
| Δ-10 | Spec §8「REFERENCE／FUTURE：Part B 的測站觀測、heatmap、自動更新、圖層切換」；DR-20 X-4（新資料功能在 #28 之外） | **re-scope** | 測站觀測 → V2 Core；模式／Radar 切換 → V2；heatmap、自動更新仍為 Later。X-4 所指的新資料功能由 V2 Outcome Contract 承載。（OC §2.4 列 10；D-4） | 本檔第 8 節 |
| Δ-11 | Spec §8「不做：離島三縣的任何呈現」 | **re-scope（只限 Now mode）** | Now mode 涵蓋 22 縣市中有有效觀測資料者（含澎湖、金門、連江）；Forecast mode 六區語義與地理不變、仍不呈現離島。（OC §2.4 列 11；P-7） | R-V2-DD-1、R-V2-MODE-3 |
| Δ-12 | DR-20 P-2(c)（vendored 底圖只是 backdrop，不承載縣市層級資料語義） | **extend** | `basemap.js` 仍為 backdrop；V2 另加帶名稱屬性的縣界互動圖層，只作互動幾何，不以資料著色，只在 Now mode 使用。（OC §2.4 列 12；D-8、P-30） | R-V2-DD-4 |
| Δ-13 | Spec INV-7、R-DOC-2、AC-14（標示要求） | **extend** | 觀測值標示為 CWA 測站觀測（如發布），與專案推導的六區預報值可見地分開、不共用圖例或色階；CWA 資料授權標示（政府資料開放授權條款）納入文件要求。AC-14 的八項不變，V2 另加 AC-V2-21 的項目。（OC §2.4 列 13；P-2；C-4） | INV-V2-5、R-V2-DOC-2、R-V2-DOC-5、AC-V2-21 |
| Δ-14 | `CONTEXT.md`「Refresh」「Taiwan Map」詞條 | **glossary delta** | 「Refresh」改為 Now mode 使用者動作，原意改名「Re-ingestion」；「Taiwan Map」增加 Now mode／Forecast mode；新增 Latest Observation、Observation Time、Fetched Time、Stale、Unavailable（BRIEF-V2 §9 逐字）。（OC §2.4 列 14；D-19） | R-V2-DOC-4 |

**明確不變（重申，OC §2.4 末段）**：INV-1、INV-2、INV-3、INV-4、INV-8、INV-9；R-TC-5「測試不需網路與金鑰」；AC-26；R-DS-4、R-DS-7；R-GA-\*、R-ING-\*、R-DER-\*、R-DB-\*；DR-17（取得時間語義與標籤）、DR-22；`data.db` 與 `TemperatureForecasts`；六區推導與 `weather_query.py` 的預報語義；預報 `/api/` endpoint 的語義；下方 Forecast dashboard 與 `Select Region` 行為。V2 對 DR-17 的唯一互動是 R-V2-MODE-6(d)：V2 自己的「Fetched Time」標籤必須與 DR-17 的預報快照取得時間標籤可辨，DR-17 本身不變。

## 2. Requirements（R-V2）

每條標示 ID、來源類型、class、需求、對應（OC 條款／AB-V2／V1 條款／DV）。

### 2.1 模式（Now mode／Forecast mode）

| ID | 類型 | Class | 需求 | 對應 |
| --- | --- | --- | --- | --- |
| R-V2-MODE-1 | OC | V2 Core | Taiwan Map MUST 恰有兩個模式：**Now mode** 與 **Forecast mode**。頁面載入後 MUST 直接處於 Now mode，不需使用者動作，且不因預報快照狀態（`/api/health` 200／503）而改變。 | S-3；AB-V2-1；Δ-5 |
| R-V2-MODE-2 | OC | V2 Core | 模式切換控制 MUST：(a) 在桌機（≥ 1024 px）與 375 px 載入後不捲動即可見；(b) 以可見文字標示兩個模式，文字分別含 `Now` 與 `Forecast`（其餘描述屬 HOW）；(c) 指示目前模式；(d) 可用鍵盤操作。樣式（segmented control 等）屬 HOW。 | S-3、S-10；AB-V2-1、AB-V2-8 |
| R-V2-MODE-3 | V1／OC | V2 Core | **Forecast mode ＝ V1 Taiwan Map，以參照繼承、語義不變**：R-EN-3～R-EN-7、R-SHR-4、AC-17、AC-18、DR-20／DR-21 核定的 HOW 在 Forecast mode 內原樣成立；六個 Region 標記、`Select Date`、四段導出色帶、DERIVED 標示、六區地理（不呈現離島）不變。AC-17「初始視野涵蓋六個標記」以**進入 Forecast mode 時**為準（R-V2-MODE-5）。Forecast mode 內 MUST NOT 出現觀測值、縣下鑽、Refresh、Radar。 | Δ-5、Δ-11；S-3；AB-V2-1 |
| R-V2-MODE-4 | OC | V2 Core | 控制項與圖例的模式歸屬：`Select Date`、導出色帶圖例、DERIVED 面板只在 Forecast mode 可見；Refresh、縣界互動、測站清單／詳情、Radar 控制、觀測圖例（若有）只在 Now mode 可見。下方 Forecast dashboard（`Select Region`、Weekly summary、折線圖、表格、預報快照取得時間）與模式無關、永遠可見、行為不變（V1 R-DS-4、R-DS-7、DR-17）。 | C-4；OC §2.1；Δ-5 |
| R-V2-MODE-5 | OC／DV | V2 Core | **切換保留地理脈絡**：(a) Now mode 的選取狀態（選縣、選測站）與視野 MUST 在 Now → Forecast → Now 的往返後恢復；(b) 進入 Forecast mode 時，若目前視野已顯示全部六個 Region 標記則 MUST 保留視野，否則 MUST 以最小調整使六個標記可見（這是 R-EN-4／AC-17 的「模式確實需要不同的有效視野」）；(c) 回到 Now mode 時 MUST 恢復離開時的 Now 視野。「單一地圖實例」屬 HOW。 | S-3；P-28；DV-8 |
| R-V2-MODE-6 | OC | V2 Core | **兩種語義分開**：(a) 觀測值 MUST 標示為 CWA 測站觀測（如發布），用語為「Latest Observation」；介面文字 MUST NOT 以 `real-time`／`realtime`／`live` 稱呼觀測資料；(b) Now mode 的氣溫著色（若有）MUST 使用自己的圖例與色階，MUST NOT 是 R-SHR-4 的四段導出色帶，且觀測圖例與導出色帶圖例 MUST NOT 同時顯示；(c) 觀測值 MUST NOT 出現在 Forecast mode、下方 dashboard 或任何預報控制項中，預報值 MUST NOT 出現在 Now mode 的觀測面板中；(d) Now mode 的「Fetched Time」標籤 MUST 與下方 dashboard 依 DR-17 §4.5 顯示的預報快照取得時間在文字與位置上可辨，不得讓讀者把兩者當成同一個時間。 | C-4；S-1；INV-7（extend）；DR-17（不變） |

### 2.2 Latest Observation 與 Now mode

| ID | 類型 | Class | 需求 | 對應 |
| --- | --- | --- | --- | --- |
| R-V2-OBS-1 | OC | V2 Core | 資料來源 MUST 是 CWA **O-A0001-001**（氣象觀測站-全測站逐時氣象資料），由伺服器端以 acceptor 的金鑰取得（R-V2-SEC-3）。產品用語為「Latest Observation」；README 以保守的官方描述記述節奏（逐時，R-V2-DOC-1）。 | S-1；OC §5；AB-V2-2 |
| R-V2-OBS-2 | OC／DV | V2 Core | **有效測站**：一筆測站紀錄有效，若且唯若 (a) 有非空 `StationId`（穩定識別；名稱可重複，不作識別）；(b) 氣溫值可解析為有限十進位數，且不屬於可設定、有文件的哨兵集合（至少 `X`、`-99`、`-98`、`T`、`990`；資料標準 V1.05）；(c) 有 WGS84 座標且緯經度皆為有限數；(d) `CountyName` 逐字屬於 22 縣市（R-V2-DD-1）；(e) 有 CWA 發布的 `ObsTime`，且可解析為一個明確的觀測時刻（至少含日期與時、分）——解析方式屬 HOW，值保留「如發布」的形式、不做正規化；`ObsTime` 的新舊不影響有效性（年齡不是判準，R-V2-OBS-10(d)）。無效測站（含 (e) 缺少或無法解析 `ObsTime` 者）MUST NOT 進入氣溫圖層、代表測站選取、縣脈絡的統計或 dataset-level Observation Time 的計算；MAY 計入診斷用的總數。 | S-1、S-2、S-5；P-1、P-15～P-19；DV-3 |
| R-V2-OBS-3 | OC | V2 Core | **正規化／裁剪**：`/api/` 回給前端的觀測回應 MUST 只含正規化後的欄位（欄位名屬 HOW，README 文件化），MUST NOT 原樣轉發上游 JSON 結構；前端 MUST NOT 解析 CWA 原始結構。成功回應至少承載：資料集識別、dataset-level Observation Time、Fetched Time、有效測站數、每個有效測站的 StationId、測站名、縣、鄉鎮、WGS84 座標、該站 Observation Time、氣溫（數值）、以及 R-V2-DD-7 的可選欄位（有效為數值／文字，無效為 `null`）。 | C-2；S-5；B4-1～B4-6（來源）；AB-V2-2 |
| R-V2-OBS-4 | OC／DV | V2 Core | **Observation Time 與 Fetched Time**：(a) 測站層級 Observation Time ＝ 該站 CWA `ObsTime`（如發布；依 R-V2-OBS-2(e) 對每個有效測站恆存在且可解析）；dataset-level Observation Time ＝ 全部有效測站 `ObsTime` 的最大值（DV-2）——只取有效測站，缺少或無法解析 `ObsTime` 的紀錄不參與；成功回應（≥ 1 有效測站）下恆有定義；(b) Fetched Time ＝ 伺服器成功自上游取得並產生目前回應的本機時鐘時刻，ISO 8601、`+08:00`、至少到秒（與 V1 DR-17／DR-22 的時間表示慣例一致）；(c) Now mode 只要處於顯示資料的狀態（success 或 stale），dataset-level Observation Time 與 Fetched Time MUST 同時可見，標籤逐字為 `Observation Time`、`Fetched Time`，顯示至少到分；Unavailable 狀態下兩個欄位仍存在、值為「—」。 | S-1；D-5；AB-V2-2；DV-2 |
| R-V2-OBS-5 | OC | V2 Core | **成功定義**：一次上游取得成功，若且唯若回應可解析且至少一個有效測站（R-V2-OBS-2）。零有效測站 ＝ 失敗（分類 `invalid_response`，R-V2-OBS-11）。有效測站數少於平常仍是成功；介面 MUST 顯示有效測站數；本檔不設契約最小數量。 | S-2；P-16、P-18 |
| R-V2-OBS-6 | OC | V2 Core | **缺值／哨兵顯示**：任何缺值、哨兵或無效欄位 MUST 顯示為「—」，永不顯示為數值；氣溫以 °C 顯示，數值格式（小數位）屬 HOW 但 MUST 等於 `/api/` 回應值。 | S-2；P-15；AB-V2-2 |
| R-V2-OBS-7 | OC | V2 Core | **Refresh**：(a) Now mode MUST 有可見、文字逐字為 `Refresh`、可鍵盤操作的控制；(b) 只有手動 Refresh，MUST NOT 自動更新或輪詢；(c) Refresh 進行中 MUST 有可見的進行中指示；(d) 每次 Refresh 的結果 MUST 是下列三者之一並可觀察：**newer**（套用新資料）、**not-newer**（保留現有資料並告知已是最新）、**failure**（→ Stale 或 Unavailable，R-V2-OBS-10）；(e) 進行中再次觸發 Refresh MUST 被忽略或合併，且任何情況下回應套用順序不得違反 R-V2-OBS-8（亂序回應不得以較舊資料覆蓋）。 | S-1、S-6；P-20～P-27；AB-V2-3 |
| R-V2-OBS-8 | OC／DV | V2 Core | **取代規則**：成功回應的 dataset-level Observation Time (a) ≥ 目前顯示者 → 套用（資料、Observation Time、Fetched Time 一併更新；相等時亦套用）；(b) < 目前顯示者 → MUST 保留目前顯示的資料與兩個時間不變，並告知使用者顯示的已是最新。回應的 Fetched Time 與目前顯示者相同（重用視窗內）→ 同 (b) 的告知、無變更。頁面存續期間 dataset-level Observation Time 永不遞減（INV-V2-6）。 | S-2、S-6；P-17；AB-V2-3；DV-4 |
| R-V2-OBS-9 | OC／DV | V2 Core | **重用視窗（可觀察層級）**：伺服器 MAY 在成功取得後的一段視窗內對後續請求重用同一份回應（含原 Observation Time 與 Fetched Time），視窗長度屬 HOW、MAY 為 0，但 MUST ≤ **10 分鐘**（契約上限，DV-5）並在 README 文件化。重用的回應 MUST 與原回應在 Observation Time、Fetched Time、測站資料上一致。伺服器 MUST NOT 以重用機制回傳任何在 Fetched Time 之後才失敗的上游狀態（重用只重用成功）。 | S-1、S-6；C-2；P-26；DV-5 |
| R-V2-OBS-10 | OC | V2 Core | **Success／Stale／Unavailable**：(a) **Unavailable** ＝ 沒有可顯示的有效 Latest Observation。首次載入失敗時 MUST：留在 Now mode；地圖與縣界可見；明確的 Latest Observation unavailable 狀態與非機密原因（R-V2-OBS-12）；Refresh 可用；模式切換與 Forecast mode 可見；不自動切換模式；不以任何方式暗示預報資料是觀測。(b) **Stale** ＝ 最近一次 Refresh／上游取得失敗，而介面仍顯示上一次成功的資料。失敗的 Refresh MUST：保留上一次有效資料與其 Observation Time／Fetched Time；顯示明確的 Stale 標示與非機密原因；Refresh 仍可用。(c) 之後成功的 Refresh（newer 或 not-newer）MUST 清除 Stale。(d) Stale 是**純失敗基準**：資料年齡不是契約條件；實作 MAY 顯示年齡提示，但 MUST NOT 稱之為 stale 或以年齡觸發 Stale。(e) Stale／Unavailable 的呈現 MUST 與 success 在視覺與文字上可辨，並各自可截圖。 | S-6；D-11、D-12；P-20～P-25；AB-V2-4 |
| R-V2-OBS-11 | OC／DV | V2 Core | **伺服器端失敗分類**：觀測（與雷達）`/api/` 路徑失敗時 MUST 回非 2xx 的 JSON，至少含機器可讀的 `reason` 與人類可讀的 `error`；`reason` 恰為下列四個代碼之一（逐字，DV-6）：`key_not_configured`（執行環境無金鑰）；`upstream_unreachable`（DNS／連線／讀取逾時等傳輸層失敗）；`upstream_error`（上游回 HTTP 非 2xx，含 401／403 auth 與 429／quota；MAY 附上游 HTTP 狀態碼數字）；`invalid_response`（上游 2xx 但無法解析、`success` 非 `"true"`、結構不符或零有效測站）。伺服器 MUST NOT 回「帶資料的 stale」回應：伺服器回應只有成功（含重用）與分類失敗兩種；Stale 是介面狀態（R-V2-OBS-10）。 | S-6；P-21～P-23；AB-V2-4；DV-6 |
| R-V2-OBS-12 | OC | V2 Core | **非機密錯誤**：使用者可見的訊息、`/api/` 的 `error` 文字與任何回應欄位 MUST NOT 含金鑰、含金鑰的 URL、原始上游 URL、原始上游回應本文或錯誤本文；伺服器 log 亦同（R-V2-SEC-7）。四類失敗在使用者可見層 MUST 各自可辨（至少以類別描述）。 | S-6；C-1；H-1；AB-V2-4 |
| R-V2-OBS-13 | OC／DV | V2 Core | **有界時間**：每次 Refresh（含首次載入）MUST 在有界時間內到達 newer／not-newer／Stale／Unavailable 之一。伺服器對上游請求 MUST 設定逾時（值屬 HOW，README 文件化），且 MUST 小於部署平台的 function 執行上限，使上游停滯以 `upstream_unreachable` 分類回應、而非平台層 gateway 錯誤；前端對任何非 JSON 或平台層錯誤回應仍 MUST 依 failure 處理（不得停在進行中）。驗證儀器：終態在 **30 秒**內（第 5.3 節，DV-7）。 | S-6；P-25；AB-V2-3；DV-7 |

### 2.3 Taiwan → County → Station

| ID | 類型 | Class | 需求 | 對應 |
| --- | --- | --- | --- | --- |
| R-V2-DD-1 | OC／V1 | V2 Core | **22 縣市**：County 的識別 ＝ CWA `CountyName` 字串逐字（「臺」不是「台」）；集合 ＝ V1 R-DER-5 的 19 個成員縣市 ＋ 澎湖縣、金門縣、連江縣。Now mode MUST 涵蓋 22 縣市中有有效觀測資料者（含離島三縣）；縣的名稱屬性圖層（R-V2-DD-4）MUST 與此 22 個字串一對一對應（對應機制屬 HOW）。 | Δ-11；P-7；AB-V2-6 |
| R-V2-DD-2 | OC | V2 Core | **Taiwan-wide 視野**：每縣至多一個**代表性有效測站**的標記，標記顯示該站氣溫；該站的測站名與縣名 MUST 可由 hover、選取或面板取得；介面 MUST NOT 把代表測站的值呈現為「該縣的氣溫」或任何縣層級的值（無縣平均，INV-V2-5）。無有效測站的縣 MUST 沒有代表標記（不是失敗）。 | S-4；P-8～P-10；AB-V2-6 |
| R-V2-DD-3 | OC／DV | V2 Core | **代表測站規則**（機制屬 HOW，以下為 WHAT）：(a) 確定性——同一有效測站集合 MUST 得到同一選取；(b) 只依目前有效測站與有文件的靜態偏好資料（若有），MUST NOT 依賴無效或不存在的測站；(c) 偏好測站本次無效時 MUST 依同一有文件的規則後備到該縣另一有效測站；(d) 規則 MUST 在 README 文件化到讀者可依 `/api/` 回應手算選取結果；(e) MUST 可離線自動化驗證（對消毒樣本與衍生的後備樣本）；(f) 本檔與 README **不列舉 22 個 StationId** 作為契約（偏好資料若含 StationId，屬 HOW 資料、非契約）。 | S-4；P-11～P-14；AB-V2-6；DV-9 |
| R-V2-DD-4 | OC／V1 | V2 Core | **縣界互動圖層**：Now mode MUST 有帶縣名屬性的 22 縣多邊形互動圖層：指標裝置 hover 時 MUST 可見地突顯該縣並顯示縣名；點選／點擊 MUST 選取該縣；MUST NOT 以資料著色（只作互動幾何）；MUST vendored 同源載入、執行期零外部請求（INV-V2-3）；只在 Now mode 作用。V1 `basemap.js` 仍為 backdrop（DR-20 P-2(c) 不變）。 | Δ-12；D-8；P-30；AB-V2-6 |
| R-V2-DD-5 | OC | V2 Core | **選縣與 County 脈絡**：選取縣後 MUST (a) 調整視野使該縣**在地圖上的**有效測站都在地圖視窗內（受 R-V2-MAP-3 上限約束）；(b) 顯示 County 脈絡：縣名、有效測站數（若有測站因 R-V2-DD-11 未上圖，另顯示上圖數或標示）、氣溫最高與最低的測站（名稱／值；平手時以有文件的確定性規則決定，HOW）、含氣溫的測站清單（R-V2-DD-6）；(c) MUST NOT 計算或顯示縣平均或任何觀測聚合值；(d) 該縣全部有效測站 MUST 可到達（地圖上或清單）。零有效測站的縣可選取：脈絡顯示 0 與「—」，不是錯誤。 | S-4；D-9；P-7～P-10；AB-V2-6 |
| R-V2-DD-6 | OC | V2 Core | **測站清單**：列出所選縣全部有效測站（名稱、氣溫；可含鄉鎮），MUST 可鍵盤操作（項目可聚焦、可以 Enter／Space 選取）；選取項目 MUST 更新測站詳情（R-V2-DD-7）；因 R-V2-DD-11 未上圖的測站 MUST 仍在清單並標示未上圖。 | S-4、S-10；P-33；AB-V2-6、AB-V2-8 |
| R-V2-DD-7 | OC | V2 Core | **測站詳情契約**：MUST 顯示——測站名稱與識別（StationId）、縣、鄉鎮、該站 Observation Time、氣溫。有效時顯示、否則「—」——相對濕度、風速、風向、氣壓、雨量（資料集發布的降水欄位，README 註明其意義）、天氣現象。單一可選欄位的缺席不是失敗。 | S-5；D-10；AB-V2-6 |
| R-V2-DD-8 | OC | V2 Core | **Back to Taiwan**：選縣後 MUST 有文字逐字為 `Back to Taiwan`、可鍵盤操作的控制；啟動後 MUST 清除選縣與選測站並回到 Taiwan-wide 視野（R-V2-MAP-4 的初始脈絡或等價的全臺視野）。 | S-4；AB-V2-6 |
| R-V2-DD-9 | OC | V2 Core | **鍵盤等價路徑**：(a) 選縣 MUST 有不經地圖的鍵盤路徑（例如 22 縣的清單或選單，形式 HOW）；(b) 選測站 MUST 有經測站清單的鍵盤路徑；(c) 模式切換、Refresh、Back to Taiwan、Radar 顯示／隱藏、底部資訊面關閉 MUST 可聚焦、可鍵盤啟動；(d) 縣多邊形與測站標記**不必**各自可聚焦；(e) 鍵盤焦點 MUST NOT 被任何面板或 overlay 完全遮蔽。 | S-10；P-33、P-34；AB-V2-8 |
| R-V2-DD-10 | OC | V2 Core | **無選取時的面板**：Now mode 無選縣時 MUST 顯示 dataset-level Observation Time、Fetched Time、Refresh、有效測站數；MAY 顯示全臺最高與最低氣溫測站（名稱／值，取自全部有效測站，標示為測站值）；MUST NOT 顯示平均。 | S-4；AB-V2-2 |
| R-V2-DD-11 | DV | V2 Core | **圍欄範圍外的測站**：座標落在圍欄範圍 E（R-V2-MAP-1）之外的有效測站（例如高雄市所轄的東沙、南沙測站）MUST NOT 放上地圖，但 MUST 計入其縣的有效測站數、出現在測站清單（標示未上圖）並可查看詳情；README 記述此規則。 | S-4、S-10；DV-10 |

### 2.4 伺服器邊界與安全

| ID | 類型 | Class | 需求 | 對應 |
| --- | --- | --- | --- | --- |
| R-V2-SEC-1 | OC／V1 | V2 Core | **瀏覽器邊界**：瀏覽器端的觀測、雷達（影像與時間戳）與預報資料請求 MUST 只指向本應用 `/api/`；靜態資源只同源；執行期 MUST 零外部請求（含 Radar 影像、tile、CDN、字型）；瀏覽器永不取得或持有金鑰。V1 AC-04(b)、DR-20.4、X-1 原樣有效。 | C-1；Δ-1、Δ-9；AB-V2-9、AB-V2-10 |
| R-V2-SEC-2 | OC／V1 | V2 Core | **CWA 存取只在觀測／雷達路徑**：(a) 伺服器端 CWA 存取只允許存在於部署 Dashboard 後端為觀測與雷達服務的程式（模組結構屬 HOW）；(b) `app.py`、`weather_query.py` 及其單元內 import closure MUST 維持不 import HTTP client、不含 `opendata.cwa.gov.tw` 或 `CWA_API_KEY` 字串（V1 R-SHR-5／AC-04(a) 的 re-scope 適用範圍）；(c) 預報 `/api/` endpoint（`/api/health`、`/api/regions*`、`/api/days*`）在處理請求時 MUST NOT 發出任何對外網路請求、MUST NOT 需要金鑰——以封鎖網路且無金鑰的測試證明行為不變。 | C-1；Δ-1、Δ-2；INV-V2-1；AB-V2-10 |
| R-V2-SEC-3 | OC／B | V2 Core | **金鑰處理（b3）**：(a) 伺服器只在執行期從 process 環境變數 `CWA_API_KEY`（與 V1 `.env.example` 同名）讀取金鑰；(b) 本機執行時的來源是單元目錄內未追蹤的 `.env`（載入機制屬 HOW，README 文件化；MUST NOT 讀取其他位置）；(c) 部署時的來源是 acceptor 親自填入的 Vercel 專案環境變數（Agents 不得填入、讀出、印出或匯出其值）；(d) 金鑰 MUST NOT 出現在 git、前端資產、`/api/` 回應、build／runtime log、evidence；(e) 缺金鑰時觀測／雷達路徑回 `key_not_configured`，預報路徑與 `/api/health` 不受影響；(f) Grading App 與預報路徑永不需要金鑰。 | C-1、C-3；A-1～A-3；Δ-3、Δ-4；RB-3（b3）；AB-V2-10 |
| R-V2-SEC-4 | V1／OC | V2 Core | **靜態檢查 re-scope（只加不減）**：(a′) HTTP client／CWA 字串禁止的 Python 檔集合改為 `app.py`、`weather_query.py` 與其單元內 import closure；`server.py`、`api/index.py` 與 V2 觀測／雷達模組退出此集合，但 MUST 通過憑證掃描（R-V2-SEC-5）；(b) 前端檢查不變並延伸：任何請求形式（`fetch`、`Image.src`、`L.imageOverlay`、`L.tileLayer`、`<img>`／`<script>`／`<link>` 的 `src`／`href`）的字面目標只得為同源 `/api/` 或 `/static/`；絕對 URL 白名單維持「非請求常數」性質，不得加入任何請求目標；(c) SQL 只在 `weather_query.py`（新模組亦不得含 SQL）；(d) 不變。 | Δ-2；AC-04；DR-20 P-3；AB-V2-10 |
| R-V2-SEC-5 | V1／OC | V2 Core | **憑證掃描延伸**：V1 R-SEC-1／AC-07(b)(c)(d)(f) 的掃描範圍 MUST 涵蓋 V2 新增的程式、消毒樣本、雷達樣本、截圖與 evidence；消毒樣本 MUST 不含金鑰或非空 `Authorization` 值；`tools/credential_scan.py` 的 artifact 清單依此延伸（工具形式 HOW）。 | Δ-4；H-1；AB-V2-10 |
| R-V2-SEC-6 | OC | V2 Core | **A-3 實作期金鑰使用**：只以未追蹤 `.env` 的既有金鑰做 (i) 擷取必要上游樣本、(ii) 對已接受的 V2 資料路徑做定向即時驗證；只唯讀 GET；不輪詢、不壓測；不印出、不匯出；CI 與自動化測試 MUST NOT 依賴即時憑證或網路（V1 R-TC-5 不變）。 | A-3；R-TC-5；AB-V2-10 |
| R-V2-SEC-7 | OC | V2 Core | **Log**：伺服器在任何路徑（含四類失敗）MUST NOT 記錄金鑰、含金鑰的 URL、請求標頭或原始上游回應本文；以哨兵金鑰在測試中證明輸出不含它。 | C-1；S-6；H-1 |

### 2.5 獨立降級

| ID | 類型 | Class | 需求 | 對應 |
| --- | --- | --- | --- | --- |
| R-V2-DEG-1 | OC | V2 Core | 三條資料路徑（Observation、Forecast snapshot、Radar）MUST 各自載入、各自失敗、各自恢復；任一路徑的失敗 MUST NOT 使另外兩條的健康內容不可用或被隱藏。Now mode 的觀測載入 MUST NOT 以 `/api/health` 成功為前提。 | S-7；D-13；AB-V2-5 |
| R-V2-DEG-2 | OC | V2 Core | **觀測失敗**只影響 Now mode 的觀測層（標記、面板資料、脈絡）：地圖、縣界互動、模式切換、Forecast mode、下方 dashboard、Radar 全部維持可用；狀態依 R-V2-OBS-10。 | S-7；AB-V2-5 |
| R-V2-DEG-3 | OC／V1 | V2 Core | **預報快照失敗**（`/api/health`／預報 endpoint 非 2xx 或網路失敗）：Forecast mode 內容與下方 dashboard 依 V1 DR-19 的條件→狀態規則顯示 error（含伺服器 `error` 訊息、`role="alert"` 等 V1 既有呈現），**範圍為預報區段層級而非整頁**：Now mode（觀測、縣下鑽、Refresh、Radar）與模式切換 MUST 維持可用；此時切到 Forecast mode，地圖區 MUST 顯示 inline error（DR-19 per-Region 規則），`Select Date` 可隱藏或停用（無可列日期）。V1 AC-10「頁面顯示錯誤狀態」對受影響部分（Forecast mode、下方 dashboard）仍成立。 | Δ-7；DR-19（delta）；AC-10；AB-V2-5 |
| R-V2-DEG-4 | OC | V2 Radar | **雷達失敗**只影響雷達狀態（overlay 與其時間戳），依 R-V2-RAD-4；觀測與預報不受影響，反之亦然。 | S-7、S-11；AB-V2-5、AB-V2-9 |
| R-V2-DEG-5 | V1 | V2 Core | `/api/health` 語義不變：200 若且唯若預報快照 ok，503 否則；MUST NOT 依賴 CWA 即時可用性或金鑰；`smoke.py` 與 smoke workflow 不變；觀測／雷達狀態由各自的 `/api/` 回應揭露，不併入 `/api/health`。 | Δ-8；R-DS-2、DR-7；AB-V2-5、AB-V2-13 |

### 2.6 地圖圍欄與響應式可用性

| ID | 類型 | Class | 需求 | 對應 |
| --- | --- | --- | --- | --- |
| R-V2-MAP-1 | OC／DV | V2 Core | **Pan 圍欄**：定義**圍欄範圍 E** ＝ 涵蓋 22 縣市本土與主要離島（含金門、連江、澎湖、蘭嶼、綠島）的經緯度矩形，代表「有用的臺灣範圍」（值為驗證儀器，第 5.3 節）。使用者 MUST NOT 能把視野拖曳到有用的臺灣範圍之外而讓無意義空白主導：任何可到達的視野 MUST 同時滿足 (i) 地圖視窗中心落在 E 內；(ii) 在經度與緯度**每一軸**上，視窗落在 E 之內，或——若視窗在該軸上比 E 更寬／更高——E 在該軸上整體位於視窗內（E 不得被推出視窗）。金門與連江 MUST 可藉合法的拖曳／縮放到達：存在可到達的視野使該縣陸地位於視窗內且其測站可選取。彈性回彈、viscosity、margin 屬 HOW。 | S-8；D-14；AB-V2-7；DV-11 |
| R-V2-MAP-2 | OC／DV | V2 Core | **Zoom-out 下限**：MUST 存在縮小下限，使縮小在臺灣變得小到無用、或無意義空白主導之前停止。客觀判準：在下限，臺灣本島南北向在地圖視窗高度中的占比 MUST ≥ 25%；下限下的任何視野仍受 R-V2-MAP-1 的圍欄約束（有用的臺灣範圍仍有意義地存在）。**不要求**在下限或任何縮放層級讓 E 的全部或 22 縣市同時在視窗內；「初始視野即最寬視野」不是需求（R-V2-MAP-4）。在兩個驗證視野各驗一次。 | S-8；D-14；AB-V2-7；DV-11 |
| R-V2-MAP-3 | OC／DV | V2 Core | **Zoom-in 上限**：MUST 存在放大上限；上限 MUST 足以在最密的縣（樣本中為臺北市）於地圖上個別選取測站（第 5.3 節儀器：1 km 地面距離 ≥ 20 CSS px）；MUST NOT 允許無意義的過度放大（第 5.3 節儀器：375 px 寬的視窗在上限仍跨 ≥ 5 km）。 | S-8；D-14；AB-V2-7；DV-11 |
| R-V2-MAP-4 | OC | V2 Core | **初始視野**：Now mode 初始（與 Back to Taiwan 後）的視窗 MUST 同時含臺灣本島全部與澎湖縣本島；不要求含金門、連江；「初始視野即最寬視野」不是需求。兩個驗證視野各驗一次。 | S-8；P-29；AB-V2-7 |
| R-V2-MAP-5 | V1／OC | V2 Core | **非零尺寸初始化回歸保護**：V1 #28 建立的「容器尺寸非 0 才初始化、`invalidateSize()` 先於 `fitBounds`」保護 MUST 在 V2 的全部初始化路徑（頁面載入的 Now mode、模式切換、底部資訊面開合、視窗 resize）維持，並有可由 Reviewer 重現的自動化證據。 | S-10（末項）；DR-20 P-12；AB-V2-8 |
| R-V2-RSP-1 | OC | V2 Core | **驗證視野**：桌機 ≥ 1024 px（驗收用 1280 px）與 375 px 為必驗；768 px 只做破版檢查（無控制項重疊、無橫向捲動、地圖可操作）。 | S-10；AB-V2-8 |
| R-V2-RSP-2 | V1／OC | V2 Core | 375 px 下 `document.documentElement.scrollWidth` MUST ≤ 視窗寬度（無不必要橫向捲動；V1 AC-19 的檢查沿用），在 Now mode 各狀態（success、stale、unavailable、選縣、選測站、資訊面展開、Radar 顯示）皆成立。 | R-EN-1(6)；AB-V2-8 |
| R-V2-RSP-3 | OC | V2 Core | **44×44**：Now mode 的互動控制（模式切換、Refresh、Back to Taiwan、Radar、資訊面關閉、清單項目）與測站／代表標記的可點區 MUST ≥ 44×44 CSS px（承接 V1 #28 V-4 為 V2 產品 outcome）。 | AB-V2-8；DR-20 P-13 |
| R-V2-RSP-4 | OC | V2 Core | 地圖 MUST 是頁面的主要內容區；模式切換不捲動即可見（R-V2-MODE-2）；頁面標題逐字 `Taiwan Weather Forecast`（V1 INV-4／H-2）。masthead 導言文字 MAY 更新為描述兩種模式（DR-21.2 先例），概念詞不變。 | S-10；P-32；INV-4 |
| R-V2-RSP-5 | OC | V2 Core | **375 px 底部資訊面**（縣／測站詳情）MUST：(a) 可關閉；(b) normal／peek 狀態下地圖仍可見（第 5.3 節儀器：至少一半地圖視窗高度未被遮蔽）；(c) 需要時可展開以顯示測站清單；(d) 有一個清楚可見、可鍵盤操作的關閉控制；(e) 滑動 MAY 有，但 MUST NOT 是唯一關閉方式；(f) 開啟中選另一測站或另一縣即更新內容；(g) 關鍵地圖控制（縮放、模式切換、Refresh、Back to Taiwan）不被完全遮蔽、仍可用。函式庫、高度、動畫、snap 點、CSS 屬 HOW。 | S-9；D-15；AB-V2-8 |
| R-V2-RSP-6 | OC | V2 Core | **面板與 overlay**（桌機與手機）MUST NOT 使地圖不可用：目前選取項（選中的縣或測站標記）與關鍵控制 MUST 可見可達；鍵盤焦點永不被完全遮蔽（R-V2-DD-9(e)）；tooltip／詳情不得被容器裁切到不可讀。面板位置屬 HOW。 | S-10；P-32、P-34；AB-V2-8 |
| R-V2-RSP-7 | OC | V2 Core | **標記可讀與密度**：在驗證視野下，每個可見標記的文字 MUST 可讀且標記可選取；密度管理（HOW）MUST NOT 使地圖不可拖曳、不可縮放或不可選取；375 px 全臺視野**不要求**同時顯示 22 個代表標記，但被顯示者須滿足本條，且選縣仍有 R-V2-DD-9(a) 的路徑。 | S-10；P-29～P-31；AB-V2-8 |
| R-V2-RSP-8 | V1／OC | V2 Core | V1 R-EN-1 六項品質清單 MUST 對 V2 介面（模式切換、Now mode 面板、底部資訊面、Radar 控制）成立；R-EN-1(5)「三種狀態」在 Now mode 為 loading、Stale、Unavailable（各一張截圖），Forecast mode 與下方 dashboard 的三種狀態依 V1 DR-19。 | Δ-6；AC-19；AB-V2-8、AB-V2-11 |

### 2.7 Radar

| ID | 類型 | Class | 需求 | 對應 |
| --- | --- | --- | --- | --- |
| R-V2-RAD-1 | OC | V2 Radar | **來源**：CWA **O-A0058 系列**雷達整合回波圖（臺灣鄰近區域，PNG 3600×3600，範圍 lon 118.0–124.0／lat 20.5–26.5；產品變體屬 HOW，但 MUST 使非回波區在地圖上不遮蔽底圖，R-V2-RAD-6）。每次取得 MUST 是當時最新一期影像及其產品時間（metadata `DateTime`）。 | S-11；OC §5；AB-V2-9 |
| R-V2-RAD-2 | OC | V2 Radar | **代理**：影像位元組與時間戳 MUST 經本應用 `/api/` 由伺服器端向 CWA 取得後提供（metadata 需金鑰，只在伺服器端）；失敗分類與非機密要求同 R-V2-OBS-11／12；伺服器 MAY 重用一期影像與時間戳，重用視窗 MUST ≤ **5 分鐘**（DV-5）。 | S-11；C-1；D-7；AB-V2-9 |
| R-V2-RAD-3 | OC／DV | V2 Radar | **顯示／隱藏**：Now mode MUST 有可見、有文字標籤、可鍵盤操作、指示目前狀態的顯示／隱藏控制；預設**隱藏**（DV-12）；顯示時才取得影像。顯示中重新取得最新影像的觸發方式（例如再次切換顯示、或由 Now mode 的 Refresh 一併觸發）屬 HOW：MUST 由使用者動作觸發、MUST NOT 自動更新或輪詢（OC §2.3），且 MUST 維持 R-V2-RAD-4 的獨立狀態與時間戳語義；所採方式在 README 記載（R-V2-DOC-1(9)）。Forecast mode 下 Radar overlay 與控制不出現（R-V2-MODE-4）。 | S-11；OC §2.3；AB-V2-9；DV-12 |
| R-V2-RAD-4 | OC | V2 Radar | **時間戳與狀態獨立**：Radar 顯示中 MUST 可見其產品時間戳（來自與影像同一次伺服器取得的 metadata），標示為雷達時間、與 Observation Time／Fetched Time 分開；Radar 的 Stale／Unavailable 語義與 R-V2-OBS-10 同構但獨立（首次取得失敗 → 不顯示 overlay、顯示 radar unavailable 與非機密原因；重新取得失敗而已有 overlay → 保留並標示 stale）。metadata 時間與影像可能短暫不一致為已知限制，README 記述。 | S-11；S-7；OC §5；AB-V2-9 |
| R-V2-RAD-5 | OC／DV | V2 Radar | **地理對齊（有意義；不預先接受實質偏移）**：overlay 的每個影像像素 MUST 落在地圖對該像素經緯度（依產品範圍與等經緯度像素格）投影位置的 **1 km** 地面距離內（DV-13 的驗證 oracle）。DA 已計算：把等經緯度影像以線性方式拉伸貼在 Web Mercator 的 lat 20.5–26.5 之間，中緯度誤差達約 3.8 km，**不符**本條；重投影方式或地圖 CRS 的選擇屬 HOW。實作若發現無法達成本條的系統性偏移，MUST route DA。 | S-11；D-7；P-36；AB-V2-9；DV-13 |
| R-V2-RAD-6 | OC | V2 Radar | **圖層與可用性**：overlay MUST 在底圖之上、測站標記與縣界互動之下；顯示中地圖 MUST 仍可拖曳、縮放、選縣、選站；標記文字仍可讀。透明度調整 MAY 提供（只在代價微小時），不是完成條件。 | S-10、S-11；OC §2.2 |

### 2.8 文件與標示

| ID | 類型 | Class | 需求 | 對應 |
| --- | --- | --- | --- | --- |
| R-V2-DOC-1 | OC | V2 Core | 單元 README MUST 增補（措辭 HOW）：(1) Now mode／Forecast mode 的說明，且 **Forecast mode（老師 Part A 加分地圖）有自己的標題、容易找到**；(2) Latest Observation 來源 O-A0001-001 與逐時節奏（保守官方描述）；(3) 代表測站規則（R-V2-DD-3(d)）與圍欄外測站規則（R-V2-DD-11）；(4) 觀測值＝CWA 測站觀測（如發布）、預報值＝專案推導，兩者標示的差異；(5) CWA 資料授權標示（R-V2-DOC-2）；(6) Vercel 金鑰設定步驟（環境變數名、適用的部署環境、由 acceptor 填入；**不含值**）與本機 `.env` 用法；(7) 觀測／雷達 `/api/` endpoint 與回應欄位、失敗代碼、逾時與重用視窗；(8) 地圖圍欄與縮放範圍說明；(9) Radar 來源、對齊方式、重新取得的觸發方式與 metadata／影像週期的已知限制；(10) 接受的 Later 項目清單（第 8 節）；(11) 既有段落中與 V2 矛盾的敘述（例如「執行期不需環境變數」）修正為 V2 事實，並保留 V1 預報路徑不需 secret 的敘述。 | AB-V2-12；V1 R-DOC-1（extend） |
| R-V2-DOC-2 | OC | V2 Core | **CWA 授權標示（法遵／文件 constraint，不是產品功能）**：README MUST 依政府資料開放授權條款標示「交通部中央氣象署 [資料名稱]」——至少對 O-A0001-001 與所用的 O-A0058 產品各一；應用內（例如地圖 attribution control）SHOULD 亦標示，位置屬 HOW。 | C-4；Δ-13；AB-V2-12 |
| R-V2-DOC-3 | V1／OC | V2 Core | `doc/acceptance/` MUST 有 V2 驗收文件（檔名 HOW，建議 `ACCEPTANCE-V2.md`），逐條對應 AC-V2-01～AC-V2-23 與第 6.3 節的定向 V1 重驗項目，記錄狀態、驗證方式與證據引用；V1 `ACCEPTANCE.md` 的既有條目不改寫，只加指向 V2 文件的參照。 | AB-V2-12；R-DOC-4（extend） |
| R-V2-DOC-4 | OC | V2 Core | `CONTEXT.md` MUST 併入 BRIEF-V2 §9 的詞彙 delta（逐字）：「Refresh」改為 Now mode 動作、原詞條改名「Re-ingestion」；「Taiwan Map」加兩個模式；新增 Latest Observation、Observation Time、Fetched Time、Stale、Unavailable、Now mode、Forecast mode。 | Δ-14；AB-V2-12 |
| R-V2-DOC-5 | OC／V1 | V2 Core | **標示（H-3 延伸）**：README、頁面文字、驗收文件中 MUST NOT 有任何地方 (a) 把觀測值寫成預報或把預報值寫成觀測；(b) 把代表測站值寫成縣的氣溫或平均；(c) 以 `real-time`／`live` 稱呼 Latest Observation；(d) 把 Fetched Time 與預報快照取得時間混為同一概念。V1 AC-14 的八項不變。 | C-4；INV-7（extend）；AB-V2-12 |
| R-V2-DOC-6 | V1 | V2 Core | V1 R-DOC-5 程式品質四項適用於全部 V2 新增程式（說明、錯誤處理、無死碼、結構對應資料流）。 | R-DOC-5；AC-27 |

### 2.9 測試、CI 與部署

| ID | 類型 | Class | 需求 | 對應 |
| --- | --- | --- | --- | --- |
| R-V2-TC-1 | OC | V2 Core | **離線自動化涵蓋**（框架、檔名、fixture 處理屬 HOW）：正規化與有效測站規則（含每種哨兵、缺座標、未知縣、缺少或無法解析的 `ObsTime`、零有效）；dataset-level Observation Time（含排除壞 `ObsTime` 測站後的最大值）；四類失敗分類（模擬上游回應：無金鑰、連線／逾時、401／403／429／500、非 JSON／`success` 非 true／零有效）與非機密輸出（哨兵金鑰）；重用視窗（可控時鐘：視窗內同 Fetched Time、視窗外重新取得）；取代規則（較舊 Observation Time 不取代——若規則在瀏覽器端實作，以瀏覽器自動化或靜態守衛提供等價證據）；代表測站規則（樣本＋後備樣本）；預報 endpoint 封網無金鑰不變；靜態檢查（R-V2-SEC-4）；Radar 對齊 oracle（R-V2-RAD-5）；R-V2-MAP-5 初始化守衛；V1 全套維持全綠。 | AB-V2-2～5、AB-V2-9～11；R-TC-1（extend） |
| R-V2-TC-2 | OC | V2 Core | **消毒真實樣本**：O-A0001-001 一份真實回應（依 A-3 於實作期擷取一次；MAY 忠實縮減；提交前自動檢查無金鑰）；Radar metadata 一份真實樣本；Radar 影像不要求提交真實檔（對齊 oracle 為幾何性質，MAY 用合成或裁切影像）；反例由正例衍生。README 記錄擷取日期與是否縮減。 | AB-V2-2；R-TC-2（同構）；A-3 |
| R-V2-TC-3 | V1 | V2 Core | 全部自動化測試 MUST 不需網路與金鑰（R-TC-5 不變）；CI workflow 預期**不需修改**（既有 `home_work_01/**` 觸發涵蓋新測試）；若確有必要，只在 A-4 的窄授權內修改既有兩個 workflow，否則不動。 | R-TC-5、R-TC-6；A-4；AB-V2-11 |
| R-V2-TC-4 | OC | V2 Core | **瀏覽器驗收（精簡）**：第 6.2 節列出的截圖與 DOM 檢查為必要集合；瀏覽器自動化只在需要時採用；執行期 network log 零外部請求為必要證據之一。 | AB-V2-1、6、7、8、9、11 |
| R-V2-ENV-1 | OC | V2 Core | **部署**：維持 Vercel 單一 Python function 與 `home_work_01` Root Directory（V1 R-DS-8 其餘部分不變）；function 設定（逾時等）屬 HOW 但 MUST 在單元目錄內；Python 3.12 三處一致（INV-8）；預覽與正式部署 MUST 提供 V2 dashboard；acceptor 填入金鑰後，部署上的 Now mode MUST 回傳 Latest Observation；部署 commit 與受審 subject 對應（V1 DR-12 方式）。 | AB-V2-13；C-2；A-2 |
| R-V2-ENV-2 | OC | V2 Core | **額度與濫用（風險處理，不新增功能）**：不輪詢、不自動更新；重用視窗（R-V2-OBS-9、RAD-2）與逾時是唯一的契約內節制；上游額度耗盡以 `upstream_error` 分類、介面轉 Stale／Unavailable；README 記述額度事實與行為。速率限制不在本檔內（Later 若需）。 | OC §5；S-6 |

## 3. Acceptance Criteria（AC-V2）

每條給出可觀察 PASS 條件、FAIL 例、證據類別與驗證方式，並對應 AB-V2。「驗證視野」＝桌機 1280 px 與 375 px。「樣本」＝R-V2-TC-2 的消毒真實樣本。

| ID | Class | 對應 | PASS 條件 | FAIL 例 | 證據類別／驗證方式 |
| --- | --- | --- | --- | --- | --- |
| AC-V2-01 | V2 Core | AB-V2-1；R-V2-MODE-1、2、3、5 | 載入即為 Now mode（無使用者動作；`/api/health` 200 與 503 兩種情況皆是）；切換控制在兩個驗證視野不捲動可見、文字含 `Now`／`Forecast`、鍵盤可切；切到 Forecast mode 後 V1 AC-17、AC-18 逐字重驗 PASS（六標記可見、色帶＝endpoint、Select Date 七日切換、圖例四段＋導出說明）；在 Now mode 選一縣並縮放後往返 Forecast，回到 Now 時選縣與視野恢復；進入 Forecast 時六標記可見。 | 載入為 Forecast；切換只有圖示無文字；往返後選縣丟失；Forecast mode 出現觀測值。 | 瀏覽器驗收＋截圖（桌機、375：Now 預設、Forecast mode）；AC-17／AC-18 重驗清單；DOM 檢查（切換控制在初始視窗內）。 |
| AC-V2-02 | V2 Core | AB-V2-1；C-4；R-V2-MODE-4、6；R-V2-DOC-5 | Now mode 不出現 `Select Date`、DERIVED 圖例、預報值；Forecast mode 不出現 Refresh、Radar、縣脈絡、觀測值；觀測圖例（若有）與導出色帶圖例不同時顯示且色階定義不同；頁面文字中觀測標示為 Latest Observation／CWA 測站觀測，無 `real-time`／`realtime`／`live`；Now mode 的 `Fetched Time` 與下方 dashboard 的預報快照取得時間標籤可辨。下方 dashboard 在兩模式下相同。 | 兩張圖例同時出現；觀測值出現在 Weekly summary；`live` 字樣。 | 瀏覽器截圖（兩模式）；DOM 文字檢查（靜態原始檔或瀏覽器自動化）；Reviewer 對照。 |
| AC-V2-03 | V2 Core | AB-V2-2；R-V2-OBS-1、3、6 | 以樣本離線執行正規化：抽樣 ≥ 5 個測站（含至少一個哨兵氣溫、一個哨兵可選欄位、一個離島縣）的輸出等於依樣本手算的期望（StationId、名稱、縣、鄉鎮、座標、ObsTime、氣溫、可選欄位或 `null`）；回應不含上游原始結構鍵（例如 `records`、`WeatherElement`）；瀏覽器抽樣 ≥ 3 站顯示值＝`/api/` 回應；哨兵在畫面顯示為「—」。preview 部署上同樣抽樣一次（金鑰填入後）。 | 哨兵 `-99` 顯示為 −99 °C；前端直接讀 `WeatherElement`；名稱作為識別。 | 離線自動化（樣本＋手算期望寫在測試內）；API 驗證；瀏覽器抽樣紀錄；preview 驗證紀錄。 |
| AC-V2-04 | V2 Core | AB-V2-2；R-V2-OBS-4 | API：回應的 dataset-level Observation Time ＝ 樣本有效測站 `ObsTime` 最大值；Fetched Time 為 ISO 8601 `+08:00`、至少到秒、等於可控時鐘值。瀏覽器：Now mode success 與 stale 狀態下 `Observation Time`、`Fetched Time` 兩個標籤逐字可見且值等於回應；unavailable 狀態下兩欄位存在、值「—」。 | 只顯示一個時間；Fetched Time 取自瀏覽器時鐘；標籤寫「updated at」。 | API 驗證（可控時鐘）；瀏覽器截圖（success、stale、unavailable）。 |
| AC-V2-05 | V2 Core | AB-V2-2、AB-V2-3；R-V2-OBS-2、4、5 | 衍生反例各自產生要求的結果：(1) 氣溫 `-99`／`X`／空字串／非數字 → 該站不在氣溫圖層、不影響其他站；(2) 缺 WGS84 或座標非有限 → 同上；(3) `CountyName` 非 22 縣 → 同上；(4) 全部測站無效 → 失敗 `invalid_response`（非 2xx JSON）；(5) 刪去一半測站 → 成功、有效測站數等於剩餘有效數；(6) 同名不同 StationId 的兩站 → 各自獨立；(7) `ObsTime` 缺少、空字串或無法解析（例如 `not-a-time`）→ 該站不在氣溫圖層、不進代表測站選取、不計入該縣有效測站數、不參與 dataset-level Observation Time；其中一例把樣本中 `ObsTime` 最新的測站改壞 → dataset-level Observation Time 等於其餘有效測站 `ObsTime` 的最大值；其他站不受影響；(8) 全部測站的 `ObsTime` 皆缺少或無法解析 → 零有效、失敗 `invalid_response`。 | 零有效測站回 200 空清單；缺座標的站被放到 (0,0)；壞 `ObsTime` 的站仍計入有效數、仍被選為代表站，或其值仍決定 dataset-level Observation Time。 | 離線自動化（衍生樣本）；Reviewer 對照清單。 |
| AC-V2-06 | V2 Core | AB-V2-3；R-V2-OBS-7、8、9、13 | API（可控時鐘、模擬上游回應）：視窗內第二次請求回同一 Fetched Time 與同一資料；視窗外重新取得、Fetched Time 更新；視窗長度 ≤ 10 分鐘且 README 記載值。瀏覽器模擬：(a) 回應 Observation Time 較新 → 資料與兩個時間更新；(b) 回應 Observation Time 較舊 → 顯示不變、出現「已是最新」類告知、無 stale；(c) 回應 Fetched Time 相同 → 同 (b)；(d) 進行中連按 Refresh → 只有一個結果被套用、無亂序覆蓋；(e) 上游停滯模擬 → 30 秒內出現 Stale（有資料）或 Unavailable（無資料），回應為 `upstream_unreachable` 分類 JSON 而非平台 gateway 頁；(f) 平台層非 JSON 5xx 模擬 → 仍到達 Stale／Unavailable。 | 較舊 Observation Time 覆蓋較新；Refresh 卡在 spinner 超過 30 秒；重用回應帶新 Fetched Time 但舊資料。 | API 驗證（含反例）；瀏覽器模擬（攔截／替換 `/api/` 回應）與計時紀錄。 |
| AC-V2-07 | V2 Core | AB-V2-4；R-V2-OBS-11、12；R-V2-SEC-7 | API 以模擬上游回應與哨兵金鑰分別觸發：無金鑰 → `key_not_configured`；連線失敗／逾時 → `upstream_unreachable`；HTTP 401、403、429、500 → `upstream_error`（MAY 附狀態碼）；非 JSON、`success` ≠ `"true"`、零有效 → `invalid_response`。每例：非 2xx、JSON 含 `reason` 與人類可讀 `error`；回應本文、擷取的 log、stdout／stderr 不含哨兵金鑰、上游 URL、上游回應本文。Radar 路徑同樣四類。 | 四類都回同一 `reason`；錯誤訊息含 `Authorization=`；log 印出上游 URL。 | API 驗證（模擬上游回應、哨兵金鑰）；log 擷取斷言。 |
| AC-V2-08 | V2 Core | AB-V2-4；R-V2-OBS-10 | 瀏覽器模擬：(a) 首次載入觀測失敗 → 留在 Now mode、地圖與縣界可見、Unavailable 狀態與類別原因可見、Refresh 可用、模式切換可見、未自動切換、無任何預報值被當成觀測；(b) 成功後 Refresh 失敗 → 資料、Observation Time、Fetched Time 保留，Stale 標示與原因可見，Refresh 可用；(c) 再次 Refresh 成功 → Stale 清除；(d) Stale 不因時間流逝出現（可控時鐘前進 > 2 小時無失敗 → 仍為 success）。四類失敗至少各一次在 (a) 或 (b) 中呈現且可辨。 | 首次失敗自動跳 Forecast mode；失敗後清空資料；年齡觸發 stale。 | 瀏覽器模擬＋截圖（stale、unavailable 各至少一張，桌機與 375）。 |
| AC-V2-09 | V2 Core／V2 Radar | AB-V2-5；R-V2-DEG-1～5 | 瀏覽器模擬：(a) 預報快照 503（替代 DB）＋觀測正常 → Now mode 完整可用（標記、下鑽、Refresh、Radar）、模式切換可用，Forecast mode 內顯示 inline error 含伺服器 `error` 訊息，下方 dashboard 顯示 V1 error 狀態（`role="alert"`），無整頁遮蔽；(b) 觀測失敗＋預報正常 → Forecast mode 與下方 dashboard 完全正常；(c) 雷達失敗 → 只有雷達狀態改變。API：`/api/health` 對 ok 快照回 200（觀測路徑無金鑰或封網時亦然），對缺失／空／不完整回 503（V1 AC-16 測試不變）；`smoke.py` 對 preview 通過。 | 觀測失敗讓下方表格消失；`/api/health` 因無金鑰回 503；預報 503 時 Now mode 被整頁 error 蓋住。 | 瀏覽器模擬＋截圖（預報 503 且 Now 正常）；既有 V1 API 回歸測試（AC-16，Flask test client，維持通過）＋封網無金鑰的 API 驗證；smoke 輸出。 |
| AC-V2-10 | V2 Core | AB-V2-6；R-V2-DD-1、2、4、5、10 | 桌機：hover 一縣 → 突顯＋縣名；點選 → 視野含該縣上圖測站、脈絡顯示縣名、有效測站數、最高／最低測站（名稱／值）等於對該縣 `/api/` 有效測站手算的極值、測站清單完整；以臺北市（最密）、澎湖縣或金門縣（離島）、一個零有效或最少測站的縣（若樣本有）各驗一次。無選取時面板顯示 Observation Time、Fetched Time、Refresh、有效測站數。DOM 全文無「平均」「mean」「average」用於觀測值（Forecast mode 的導出「Average」註記除外）。 | 縣脈絡顯示平均；最高測站與 `/api/` 不符；離島縣不可選。 | 瀏覽器驗收＋截圖（縣脈絡）；極值對照表附 `/api/` 值；DOM 文字檢查。 |
| AC-V2-11 | V2 Core | AB-V2-6；R-V2-DD-3 | 離線自動化：對樣本執行代表測站選取，每縣 ≤ 1 站且皆為有效站；同一輸入重複執行結果相同；衍生樣本把 ≥ 3 個縣的被選站設為無效 → 後備到該縣另一有效站、其他縣不變；零有效的縣無代表。README 記述規則；Reviewer 依 README 規則對 ≥ 3 縣手算並與 `/api/`／畫面一致。Spec 與 README 不含 22 個 StationId 的契約列表。 | 規則依賴寫死且本次無效的站而留空；README 無法手算；兩次執行結果不同。 | 離線自動化；README 文件審查；Reviewer 手算紀錄。 |
| AC-V2-12 | V2 Core | AB-V2-6、AB-V2-8；R-V2-DD-6～9、11 | 桌機與 375：選縣後測站清單可 Tab 到、Enter 選取 → 詳情顯示必要欄位（名稱、StationId、縣、鄉鎮、該站 Observation Time、氣溫）與可選欄位（有效值或「—」）；`Back to Taiwan` 逐字可見、鍵盤可啟動、啟動後選取清除且視野符合 R-V2-MAP-4；不經地圖的鍵盤路徑可選任一縣；圍欄外測站（樣本中若有，例如高雄市東沙）在清單中標示未上圖且可看詳情、不在地圖上。 | 詳情缺 StationId；Back to Taiwan 只回視野不清選取；只能靠點多邊形選縣。 | 瀏覽器鍵盤走查紀錄＋截圖（測站詳情、Back to Taiwan）。 |
| AC-V2-13 | V2 Core | AB-V2-7；R-V2-MAP-1～4 | 兩個驗證視野各驗：(a) 初始視窗含本島全部與澎湖本島；(b) 在中等縮放（儀器：zoom 8）與上限各往四個方向拖曳到底後，讀取地圖視窗範圍與中心：中心在 E 內；每一軸上視窗在 E 內、或（視窗大於 E 的軸）E 整體在視窗內；可藉拖曳／縮放到達金門與連江（各一張截圖：該縣陸地在視窗內且測站可選取）；(c) 縮到下限：本島南北占視窗高度 ≥ 25%，且 (b) 的圍欄判準仍成立；再縮不動；**不以「E 全部或 22 縣市同時在視窗內」為 PASS 條件**；(d) 放到上限：儀器檢查（1 km ≥ 20 CSS px；375 px 視窗跨 ≥ 5 km）成立、再放不動；在臺北市上限下每個上圖測站可個別點選（或以清單選取後在地圖上被指示）。 | 可拖到只剩海或只剩鄰國海岸而不見臺灣範圍；縮到臺灣成一點；可無限放大到空白多邊形；金門或連江無法置於視窗內。 | 瀏覽器驗收＋截圖（下限、上限、金門、連江、拖曳到底）；儀器數值記錄（zoom、視窗中心與 bounds 對 E 的逐軸比較）。 |
| AC-V2-14 | V2 Core | AB-V2-8；R-V2-RSP-1～8；R-V2-DD-9(e) | 桌機 1280 與 375 各一組截圖（Now mode success、選縣、選測站、stale、unavailable；375 另含資訊面 peek／展開／關閉）；768 px 破版檢查通過；375 px 各狀態 `scrollWidth` ≤ 視窗寬；44×44 對列出的控制與標記以 DOM 量測 PASS；375 資訊面 peek 時地圖 ≥ 一半高度可見、關閉控制可見可鍵盤、開啟中選另一站即更新、滑動非唯一關閉方式、縮放／模式切換／Refresh／Back to Taiwan 可用；桌機面板不遮蔽選取項與關鍵控制；焦點走查中無焦點被完全遮蔽；R-EN-1 六項對 V2 介面逐項 PASS；loading／Stale／Unavailable 各一張。 | 375 出現橫向捲軸；關閉只能滑動；資訊面全螢幕蓋住地圖無法關閉；768 控制項重疊。 | 瀏覽器驗收清單＋截圖；DOM 量測（`scrollWidth`、`getBoundingClientRect`）。 |
| AC-V2-15 | V2 Core | AB-V2-8；R-V2-MAP-5 | V1 `test_map_frontend.py` 的初始化守衛測試維持通過或以等價守衛取代（只加不減）；新增證據涵蓋模式切換與資訊面開合後無 `Invalid LatLng (NaN, NaN)`／0×0 標記（瀏覽器自動化或靜態守衛，Reviewer 可重現）。 | 守衛被移除；切換模式後標記消失。 | 既有 V1 自動化守衛維持通過；新增自動化守衛或瀏覽器自動化紀錄。 |
| AC-V2-16 | V2 Core | AB-V2-10；R-V2-SEC-1、2、4；INV-V2-3 | 靜態檢查通過：(a′) `app.py`、`weather_query.py` 與其單元內 import closure 無 HTTP client、無 CWA 字串；(b) `static/**` 遞迴無 CWA 字串／`CWA_API_KEY`，所有請求形式的字面目標只為 `/api/` 或 `/static/`，絕對 URL 只有既有非請求常數；(c) SQL 只在 `weather_query.py`；(d) 不變。行為檢查：封鎖 socket／HTTP client 且無 `CWA_API_KEY` 時，`/api/health`、`/api/regions*`、`/api/days*` 回應與 V1 相同。執行期 network log（Now mode 含 Radar 顯示、Forecast mode）零外部請求。V1 靜態檢查的其餘斷言未弱化（Reviewer diff 對照）。 | 前端以 `new Image().src = "https://…cwa…"` 載雷達；白名單加入 tile URL；預報 endpoint 在封網時 500。 | 靜態檢查（既有 V1 pytest 靜態檢查的 re-scope，diff 由 Reviewer 審）；封網無金鑰的 API 驗證；瀏覽器 network log。 |
| AC-V2-17 | V2 Core | AB-V2-10、AB-V2-13；R-V2-SEC-3、5、6、7；INV-V2-2 | (a) `git ls-files` 不含 `.env`；憑證掃描（含新程式、樣本、截圖、evidence 路徑）零命中；樣本無 `Authorization` 值；(b) 伺服器只從 `CWA_API_KEY` 環境變數讀金鑰（程式審查）；本機以 `.env` 執行時 Now mode 成功且終端無金鑰（worklog）；(c) acceptor 填入 Vercel 環境變數後，preview 部署的觀測 `/api/` 回 200 含測站、雷達 `/api/` 回影像與時間戳，回應與 Reviewer 紀錄無金鑰；(d) 未填金鑰的環境（本機無 `.env`）→ `key_not_configured`、預報路徑正常；(e) worklog／audit／acceptance／截圖不含金鑰；A-3 使用只限樣本擷取與定向驗證且有紀錄。 | Vercel build log 印出金鑰；`.env` 進 git；evidence 貼出含金鑰的 curl。 | 憑證掃描；程式審查；preview 驗證紀錄（Reviewer 重現）；worklog 審查。 |
| AC-V2-18 | V2 Radar | AB-V2-9；R-V2-RAD-1～4、6；R-V2-DEG-4 | 瀏覽器：Radar 控制有文字標籤、預設隱藏、鍵盤可切；開啟 → overlay 出現、雷達時間戳可見且與 Observation Time 分開；關閉 → overlay 消失；重新取得最新影像的觸發方式（再次開啟、Refresh 或其他使用者動作，HOW）與 README 記載一致、可觀察、不自動輪詢；雷達失敗模擬 → 雷達 unavailable（無 overlay）或 stale（保留舊 overlay＋標示），觀測面板不受影響；overlay 在標記之下、地圖仍可拖曳縮放選站；Forecast mode 無 Radar。API：雷達 `/api/` 回影像（image content-type）與時間戳（metadata `DateTime`）；四類失敗同 AC-V2-07；重用 ≤ 5 分鐘。靜態：影像 URL 為 `/api/`。 | 前端直接取 S3 URL；時間戳與 Observation Time 共用一欄；雷達失敗讓觀測變 stale。 | 瀏覽器截圖（開／關、失敗）；API 驗證；靜態檢查。 |
| AC-V2-19 | V2 Radar | AB-V2-9；R-V2-RAD-5 | 對齊 oracle：對產品範圍的 ≥ 9 個參考點（四角、四邊中點、中心）與 ≥ 3 個本島內參考點（例如臺北、臺中、恆春附近的經緯度），在 zoom 7 與 zoom 10（儀器）下，overlay 中該經緯度對應像素的畫面位置與地圖 `latLng → containerPoint` 的投影位置相距 ≤ 1 km 地面距離（換算為該 zoom 的 px）；自動化證據可由 Reviewer 重現（瀏覽器自動化量測，或對重投影／定位函式的自動化幾何證據加一次瀏覽器抽驗）。視覺抽驗：以含海岸線的變體或已知位置的回波邊緣確認無明顯錯位（SHOULD）。 | 以 `L.imageOverlay` 線性貼圖於 Mercator（DA 計算最大誤差約 3.8 km）；只有截圖無量測。 | 自動化幾何驗證；瀏覽器量測紀錄；截圖。 |
| AC-V2-20 | V2 Core | AB-V2-11；R-V2-TC-3；INV-V2-8 | CI 對 V2 subject 全綠：V1 既有測試全部保留且未弱化（Reviewer 以 parent 與 subject 的測試名與斷言 diff 核對）＋V2 新測試；`app.py`、`weather_query.py`、`ingestion/**`、`data.db`、預報 `/api/` 回應形狀與 V1 結案版相同（blob 或 diff 證明；`weather_query.py`／`app.py` 未變）；定向重驗：第 6.3 節清單各一次；不重做整套 V1 evidence。 | 刪除 V1 靜態檢查而非 re-scope；`data.db` 被重新產生；`app.py` 有 diff。 | CI run；blob／diff 證明；第 6.3 節重驗紀錄與選定截圖。 |
| AC-V2-21 | V2 Core | AB-V2-12；R-V2-DOC-1～5 | 文件審查清單全部 PASS（逐項引用行號）：(1) Now／Forecast mode 說明且 Forecast mode 有專屬標題、從目錄可直接找到；(2) O-A0001-001 來源與逐時節奏（保守描述）；(3) 代表測站規則可手算；(4) 圍欄外測站規則；(5) 觀測（如發布）與推導值標示分開、無 R-V2-DOC-5 (a)–(d) 的反例；(6) CWA 授權標示兩個資料集；(7) Vercel 金鑰步驟含變數名、環境、acceptor 填入，**不含值**，本機 `.env` 說明；(8) 觀測／雷達 endpoint、失敗代碼、逾時、重用視窗；(9) 圍欄／縮放說明；(10) Radar 來源、對齊方式、重新取得觸發方式、已知限制；(11) Later 清單；(12) 與 V2 矛盾的舊敘述已修正、V1 預報路徑不需 secret 的敘述保留；(13) `CONTEXT.md` 詞彙 delta 逐字併入；(14) V2 驗收文件存在並逐條對應 AC-V2 與第 6.3 節；V1 `ACCEPTANCE.md` 未改寫。 | README 貼出金鑰；Forecast mode 只在段落中間一句帶過；CONTEXT 仍把 Refresh 定義為重跑 ingestion。 | Reviewer 文件審查（逐項行號）。 |
| AC-V2-22 | V2 Core | AB-V2-13；R-V2-ENV-1；R-V2-DEG-5 | 對受審 commit 的 Vercel 部署（不需登入）：`GET /` 200 含 `Taiwan Weather Forecast` 且頁面為 V2（Now mode 控制存在）；`GET /api/health` 200（`smoke.py` 90 秒內 PASS）；acceptor 填入金鑰後觀測 `/api/` 200 含測站、Now mode 於瀏覽器顯示 Latest Observation；部署 id ↔ commit 對應（V1 DR-12／AC-15 方式）；production 於合併後重跑為 release evidence（不是完成條件）。 | preview 需登入；health 依賴金鑰；部署 commit 與受審 subject 不符。 | smoke 輸出；preview 驗證紀錄（Reviewer 重現）。 |
| AC-V2-23 | V2 Core | AB-V2-1、AB-V2-2、AB-V2-6；R-V2-MODE-2、R-V2-OBS-4、7、R-V2-DD-8、R-V2-RSP-4 | 頁面文字錨點逐字存在：`Taiwan Weather Forecast`（標題）、`Now`、`Forecast`（模式切換）、`Latest Observation`、`Observation Time`、`Fetched Time`、`Refresh`、`Back to Taiwan`（選縣後）；V1 概念詞（`Select Region`、`Select Date`、`Date`、`MinT`、`MaxT`、六 Region 中文名）不變；無 `real-time`／`realtime`／`live` 指稱觀測。 | 標籤改成 `Observed at`；標題被改。 | 靜態 DOM／文字檢查（讀取頁面原始檔或瀏覽器 DOM）。 |

## 4. Invariants（INV-V2；Spec Integration Audit 必核，與 V1 INV-1～INV-9 並列）

| ID | Invariant | 依據 |
| --- | --- | --- |
| INV-V2-1 | **預報路徑 CWA-free 且 key-free**（V1 INV-6 的 re-scope 形式）：Grading App、共用預報查詢模組、預報 `/api/` endpoint、`/api/health`、Forecast mode、下方 dashboard 永不呼叫 CWA、永不需要金鑰。 | Δ-1、Δ-2；C-1；AB-V2-10 |
| INV-V2-2 | **金鑰零外洩、兩個授權位置**（V1 INV-5 的 extend 形式）：金鑰只在未追蹤 `home_work_01/.env` 與 acceptor 填入的 Vercel 專案環境變數；不進 git（追蹤檔案與 diff）、前端、`/api/` 回應、log、文件、fixture／樣本、evidence；伺服器只在執行期讀 `CWA_API_KEY`。 | Δ-3、Δ-4；C-3；b3 RB-3；H-1 |
| INV-V2-3 | **瀏覽器只呼叫 `/api/`、執行期零外部請求**（含 Radar 影像）；靜態資源同源；`_ALLOWED_FRONTEND_URLS` 只含非請求常數。 | Δ-9；AC-04(b)；DR-20.4、X-1 |
| INV-V2-4 | **`/api/health`、smoke、預報 endpoint 語義不變**，永不依賴 CWA 即時可用性或金鑰。 | Δ-8；R-DS-2、DR-7 |
| INV-V2-5 | **兩種語義分開、觀測不聚合**：觀測值＝CWA 測站觀測（如發布），預報值＝專案推導；不共用圖例或色階；沒有縣平均或任何觀測聚合推導值；代表測站值永不被標示為縣值；用語 Latest Observation，不用 realtime／live。 | C-4；S-4；Δ-13；H-3（extend） |
| INV-V2-6 | **新鮮度單調**：頁面存續期間顯示的 dataset-level Observation Time 永不遞減；Stale 只以失敗為基準、永不以年齡為基準；伺服器回應只有成功（含重用）與分類失敗。 | S-1、S-2、S-6 |
| INV-V2-7 | **三條路徑獨立降級**：Observation、Forecast snapshot、Radar 任一失敗不使其他兩者的健康內容不可用；Now mode 不以 `/api/health` 成功為前提。 | S-7；Δ-7 |
| INV-V2-8 | **V1 不變量與產物不變**：INV-1、INV-2、INV-3、INV-4、INV-7（extend 後）、INV-8、INV-9 原樣成立；`app.py`、`weather_query.py`、ingestion、`data.db`、預報 `/api/` 回應形狀、下方 dashboard 與 `Select Region` 行為與 V1 結案版相同。 | OC §2.1；Δ 表末段 |
| INV-V2-9 | **Scope class 分明**：V2 全部項目為 ENHANCED（V2 Core／V2 Radar）、只在部署的 Dashboard；不取代、弱化或被呈現為老師要求的行為；Part A 評分項目與 MVM 行為不變。 | OC §1；Bindings §2.4；INV-9 |

## 5. Implementation Decisions

### 5.1 契約固定（Executor 不得自行改變）

- **模式與預設**：兩個模式；載入即 Now mode；切換文字含 `Now`／`Forecast`；Forecast mode ＝ V1 地圖原樣（含 DR-20／21 核定 HOW）。
- **資料集**：觀測 O-A0001-001；雷達 O-A0058 系列（變體 HOW）。
- **時間表示**：Fetched Time ISO 8601 `+08:00` 至少到秒；Observation Time 如 CWA 發布；dataset-level Observation Time ＝ 有效測站 `ObsTime` 最大值。
- **文字錨點**：`Observation Time`、`Fetched Time`、`Refresh`、`Back to Taiwan`、`Latest Observation`、`Now`、`Forecast`；標題 `Taiwan Weather Forecast`；V1 概念詞不變。
- **有效測站定義**、**成功定義**（≥ 1 有效）、**取代規則**、**四個失敗代碼字串**、**非 2xx JSON 含 `reason`／`error`**、**伺服器不回帶資料的 stale**。
- **重用視窗上限**：觀測 ≤ 10 分鐘、雷達 ≤ 5 分鐘（實際長度 HOW，MAY 0）。
- **上游逾時存在且小於平台上限**；有界時間驗證儀器 30 秒。
- **22 縣市**＝V1 R-DER-5 的 19 ＋ 澎湖縣、金門縣、連江縣，識別為 CWA `CountyName` 逐字。
- **代表測站規則的性質**（確定性、只依有效站、有文件、可離線驗證、不列 StationId）；**無縣平均**。
- **測站詳情必要欄位**；可選欄位「—」。
- **圍欄三項的產品語義**（第 2.6 節）與**圍欄外測站規則**；初始視野含本島＋澎湖。
- **金鑰**：環境變數名 `CWA_API_KEY`；兩個授權位置；只在伺服器端執行期讀取。
- **靜態檢查 re-scope 的檔案集合**（R-V2-SEC-4）；預報路徑封網無金鑰不變。
- **`/api/health` 不變**；觀測／雷達狀態不併入。
- **Radar 對齊 oracle**（≤ 1 km）；overlay 在底圖之上、標記之下；預設隱藏。
- **技術棧不變**：Flask、Vercel 單一 function、Leaflet（vendored）、SQLite 預報快照、Streamlit Grading App、既有 CI；無新雲端基礎設施、無持久伺服器狀態要求。
- **文件義務**（第 2.8 節）與 CWA 授權標示。

### 5.2 交給實作（HOW）

- 觀測／雷達 `/api/` 的確切路徑、回應欄位名、HTTP 快取標頭；伺服器模組結構（不要求「觀測模組」或「唯一呼叫者」）；`.env` 載入機制；上游逾時值；重用視窗長度與快取機制（記憶體、無持久狀態）；HTTP client 選擇。
- 代表測站的具體機制（偏好清單、最中心、海拔最低、StationId 排序等）與後備順序；平手規則；密度管理（中間縮放層級的聚合／隱藏）；縣脈絡極值的平手規則。
- 帶屬性縣界圖層的建置方式與資料大小預算（SHOULD 保持精簡）；hover／選取樣式；觀測氣溫色階（若有）；標記樣式；面板位置與版面；底部資訊面的實作、高度、snap 點、動畫；segmented control 樣式；「單一地圖實例」與模式切換的視野保存機制。
- Leaflet 常數：`minZoom`、`maxZoom`、`maxBounds`、viscosity、padding、初始 `fitBounds` 範圍（受第 5.3 節產品語義約束）。
- Radar 變體、重投影技術或地圖 CRS、影像快取、透明度滑桿（MAY）。
- 測試框架、檔名、fixture 縮減方式、mock 架構、headless 工具；Ticket 粒度與順序；瀏覽器歷史、`prefers-reduced-motion`、可選年齡提示（不得重定義 stale）；CWA 授權標示在應用內的位置。
- README 措辭；V2 驗收文件檔名。

### 5.3 驗證儀器（DA 為客觀驗收選定；不是產品語義）

| 產品語義（契約） | 儀器（建議值；Executor 可改，須仍滿足語義並記錄） | PASS 檢查 |
| --- | --- | --- |
| R-V2-MAP-1 圍欄範圍 E | E ＝ lon 117.6–122.9、lat 21.2–26.7（涵蓋金門 118.2E、連江東引 26.4N、蘭嶼 121.6E、澎湖 119.3E）；Leaflet `maxBounds` ＝ E——其逐軸行為（視窗小於界時限制在界內、視窗大於界時把界置中；vendored Leaflet 1.9.4 `_getBoundsOffset`／`_rebound`）即同時滿足 R-V2-MAP-1 (i)(ii)；viscosity 屬 HOW | 拖曳到底後讀取視窗中心與 bounds：中心在 E 內；每一軸視窗 ⊆ E 或 E ⊆ 視窗；金門、連江可置於視窗內且測站可選取（zoom 8 與上限各驗） |
| R-V2-MAP-2 下限 | `minZoom` ＝ 6（DA 計算：z6 時本島南北 174 px：桌機 560 px 高視窗占 31%、375×360 視窗占 48%；z5 為 87 px、15%，FAIL；z7 亦滿足）。儀器只證明 25% 判準與圍欄仍成立；**不**藉此要求 E 或 22 縣市同時在視窗內 | 下限時本島南北 ≥ 25% 視窗高、圍欄判準成立；再縮不動 |
| R-V2-MAP-3 上限 | `maxZoom` ＝ 12（可接受 12–13；z12 時 1 km ≈ 24 px、375 px 視窗 ≈ 16 km；z11 時 1 km ≈ 12 px FAIL；z14 時 375 px ≈ 4 km FAIL） | 上限時 1 km ≥ 20 CSS px 且 375 px 視窗 ≥ 5 km；臺北市測站可個別選取 |
| R-V2-MAP-4 初始視野 | `fitBounds` 於 lon 119.25–122.05、lat 21.85–25.35（本島＋澎湖）加面板 padding | 兩個驗證視野的初始視窗含本島與澎湖 |
| R-V2-OBS-13 有界時間 | 終態 ≤ 30 秒；上游逾時建議 ≤ 10 秒且小於 Vercel function `maxDuration` | 停滯模擬 30 秒內到達 Stale／Unavailable 且回應為分類 JSON |
| R-V2-OBS-9 重用視窗 | 觀測 ≤ 10 分鐘、雷達 ≤ 5 分鐘（上限為契約；長度 HOW） | 可控時鐘測試 |
| R-V2-RAD-5 對齊 | 參考點：產品範圍四角、四邊中點、中心，加本島內 ≥ 3 點；zoom 7 與 10 | 每點誤差 ≤ 1 km（換算 px：z7 ≈ 0.35 px、z10 ≈ 2.8 px；以 zoom 10 為主要判定，zoom 7 作粗檢） |
| R-V2-RSP-5(b) 資訊面 peek | 地圖視窗高度 ≥ 50% 未被遮蔽 | DOM 量測 |
| R-V2-RSP-3 44×44 | `getBoundingClientRect` 或 hit-area 量測 | 列出的控制與標記 ≥ 44×44 |
| R-V2-RSP-1 視野 | 1280×(map 高度)、375×(map 高度)、768 破版 | 截圖與 DOM 檢查 |

## 6. Verification Strategy（精簡；證明 V2 delta、相關失敗行為、V1 回歸）

### 6.1 各層方法

| 層 | 方法 | 必測 |
| --- | --- | --- |
| 觀測正規化與規則 | 離線自動化驗證，消毒樣本＋衍生反例（框架 HOW） | AC-V2-03、04、05、11 |
| 伺服器失敗分類、重用、逾時、log | 離線 API 驗證，模擬上游回應、可控時鐘、哨兵金鑰（模擬方式 HOW） | AC-V2-06（API 面）、07、18（API 面） |
| 預報路徑不變 | 既有 V1 API 回歸測試（pytest／Flask test client，既有事實，維持通過）＋封網無金鑰的 API 驗證 | AC-V2-09（API 面）、16、20 |
| 靜態與安全 | 靜態檢查（既有 V1 pytest 靜態檢查的 re-scope，既有事實）；憑證掃描（既有工具延伸） | AC-V2-16、17、23 |
| Radar 對齊 | 幾何自動化（重投影／定位函式的自動化證據或瀏覽器量測） | AC-V2-19 |
| 初始化守衛 | 既有 V1 靜態守衛（既有事實）＋瀏覽器自動化 | AC-V2-15 |
| 瀏覽器行為與狀態 | 手動驗收清單＋截圖；以攔截／替換 `/api/` 回應模擬失敗；network log（工具 HOW） | AC-V2-01、02、06（UI 面）、08、09、10、12、13、14、18 |
| 部署 | `smoke.py`＋preview 驗證（acceptor 填金鑰後） | AC-V2-22、17(c) |
| 文件 | Reviewer 逐項審查 | AC-V2-21 |

### 6.2 必要截圖／紀錄集合（精簡）

桌機 1280：Now mode 預設；選縣（臺北市）脈絡；測站詳情；Stale；Unavailable；預報 503 且 Now 正常；Forecast mode（AC-17／AC-18 重驗兩張）；Radar 開／關；縮放下限；縮放上限（臺北市）；金門或連江到達。375：Now mode 預設；資訊面 peek／展開／關閉；Stale；Unavailable；Forecast mode。768：一張破版檢查。紀錄：network log 零外部請求（Now 含 Radar、Forecast）；鍵盤走查；儀器數值（zoom、bounds、對齊誤差、scrollWidth、44×44）。

### 6.3 定向 V1 重驗（只在 V2 可能實質影響處；不重做整套 V1 evidence）

| V1 項目 | 為何重驗 | 方式 |
| --- | --- | --- |
| AC-17、AC-18 | 地圖改為雙模式、Forecast mode 為 V1 地圖 | Forecast mode 內逐字重驗（AC-V2-01） |
| AC-19（R-EN-1 六項、375 無橫向捲動、三種狀態） | 版面新增模式切換、面板、資訊面 | AC-V2-14 |
| AC-02、AC-03（Dashboard 側）、AC-24（Dashboard 側） | 下方 dashboard 應不變；Fetched Time 標籤需可辨 | 自動化（V1 測試）＋一張截圖對照 AC-V2-02 |
| AC-04 | 靜態檢查 re-scope | AC-V2-16 |
| AC-07(b)(c)(d)(f)；AC-07(e) | 掃描範圍延伸；(e) supersede | AC-V2-17 |
| AC-10（Dashboard 側） | 頁面層級 error → 預報區段層級 | AC-V2-09 |
| AC-14 | 文件新增標示項 | AC-V2-21（八項不變＋新項） |
| AC-15、AC-16、AC-22(a) | 部署與 health 不變 | AC-V2-22、AC-V2-09（API 面） |
| AC-26、INV-9 | Grading App 不變 | 自動化＋blob／diff（AC-V2-20） |
| 標題與 masthead | 版面改動 | AC-V2-23 |

其餘 V1 AC（AC-01、AC-05、AC-06、AC-08、AC-09、AC-11、AC-12（除 README 新步驟外）、AC-13、AC-20、AC-21、AC-23、AC-25、AC-27（新程式除外）、AC-28、AC-29、AC-30）以 CI 全綠與 blob／diff 不變證明，不另重驗；其 V1 evidence 沿用。

### 6.4 誰在什麼時候看什麼

| 階段 | 動作 | 依據 |
| --- | --- | --- |
| Executor self-verification（每 Ticket） | 跑 Ticket 引用的 AC-V2 對應測試與清單；worklog 引用結果；不得以弱化測試取得通過；觸及金鑰的動作依 A-3 記錄。 | 治理 §3.5；impl-default |
| Ticket independent audit（R1／R2） | Reviewer 依 Ticket 引用的 AC-V2 逐條 PASS／FAIL；觸及 H-1／H-2／H-3 的 Ticket，audit record 依 decision A-1 明記核對段（H-1 含 b3 兩個位置與 log／回應；H-3 含觀測／推導語義分開與代表測站不當縣值）。 | 治理 §4；Bindings §5；derivation record §6 |
| Spec Integration Audit（全部 Ticket 結案後） | 對整合 subject 核 INV-V2-1～9 與 V1 INV-1～9、AC-V2-01～23 全部、第 6.3 節重驗、AB-V2-1～13 的涵蓋、第 1.2 節 delta 表的一致性、traceability；同時核對本 Delta Spec 為 V2 Outcome Contract 唯一的 derived Spec 且涵蓋整個 acceptance boundary。 | 治理 §4.7；derivation record §4 |
| DA phase acceptance | 引用已 closure 的 Spec Integration Audit record。 | 治理 §3.8 |
| Release（acceptor） | 合併前：Bindings §5 gate（全部 Ticket 結案、Spec Integration Audit closure、phase acceptance、README 實跑、無追蹤中的機密）＋ acceptor 已填 Vercel 金鑰的 preview 驗證；合併後對 production 重跑 smoke 與觀測抽樣為 release evidence。 | Bindings §5；RB-1；OC §6 |

## 7. 對應矩陣（AB-V2 → AC-V2 → R-V2）

| AB-V2 | AC-V2 | 主要 R-V2 |
| --- | --- | --- |
| AB-V2-1 | AC-V2-01、AC-V2-02、AC-V2-23 | MODE-1～6 |
| AB-V2-2 | AC-V2-03、AC-V2-04、AC-V2-05、AC-V2-23 | OBS-1～6、DD-10 |
| AB-V2-3 | AC-V2-05、AC-V2-06 | OBS-5、7、8、9、13 |
| AB-V2-4 | AC-V2-07、AC-V2-08 | OBS-10、11、12、SEC-7 |
| AB-V2-5 | AC-V2-09 | DEG-1～5 |
| AB-V2-6 | AC-V2-10、AC-V2-11、AC-V2-12、AC-V2-23 | DD-1～11 |
| AB-V2-7 | AC-V2-13 | MAP-1～4 |
| AB-V2-8 | AC-V2-12、AC-V2-14、AC-V2-15 | RSP-1～8、MAP-5、DD-9 |
| AB-V2-9 | AC-V2-18、AC-V2-19 | RAD-1～6、DEG-4 |
| AB-V2-10 | AC-V2-16、AC-V2-17 | SEC-1～7 |
| AB-V2-11 | AC-V2-20（含第 6.3 節） | TC-1～4、DOC-6；INV-V2-8 |
| AB-V2-12 | AC-V2-21 | DOC-1～5 |
| AB-V2-13 | AC-V2-22、AC-V2-17(c) | ENV-1、DEG-5 |
| OC C-1～C-4（constraints） | AC-V2-02、16、17 | SEC-\*、MODE-6、DOC-2、DOC-5 |
| OC §5 風險（額度、平台限制） | AC-V2-06(e)(f)、AC-V2-07 | ENV-2、OBS-13 |

## 8. Out of Scope

- **OPTIONAL／Later（V2 Outcome Contract §2.2 明列；不在接受範圍，不得成為完成條件；日後要做須新的 Outcome Contract 或 acceptor 指示）**：獨立雨量圖層（O-A0002-001）；雷達動畫／歷史回放；heatmap；自動更新／輪詢；縣市篩選與測站搜尋；URL deep-linking；10 分鐘資料集（O-A0003-001）升級；歷史觀測儲存；Windy；22 縣市預報；Grading App 的任何 V2 行為；速率限制；瀏覽器歷史整合。
- **Non-scope（OC §2.3）**：任何持久化伺服器狀態、Redis／Postgres、queue、背景 worker、新雲端基礎設施；瀏覽器直接呼叫 CWA 或任何外部主機（含 Radar）；專案推導的縣平均或任何觀測聚合值；以年齡為契約的 stale；修改 V1 Outcome Contract、Spec v1.1、derivation record 的 normative 文字。
- **REFERENCE／FUTURE**：Part B 的 FastAPI、React／Next.js、Windy、Redis；老師 repo 架構。
- **不由 Agent 執行（reserved）**：填入 Vercel 環境變數（RB-3）；建立／更換憑證（RB-3）；合併進 `main`（RB-1）；繳交（RB-2）；付費（RB-4）；單元目錄外檔案（RB-5，A-4 窄授權除外）；破壞性 git（RB-6）。

## 9. Further Notes

### 前置條件（acceptor 動作；缺任一項時只停止受影響路徑）

| # | 動作 | 影響的 AC | 保留依據 |
| --- | --- | --- | --- |
| 1 | 部署階段在 Vercel 專案填入 `CWA_API_KEY`（適用 preview 與 production 環境）；不印出、不匯出。 | AC-V2-17(c)、AC-V2-22（觀測部分） | A-2；RB-3（b3） |
| 2 | 受審 commit 的部署不需登入可存取（V1 既有設定沿用）。 | AC-V2-22 | RB-3 |
| 3 | 開符合 `orchestrator` mapping 的主 session 啟動 Formal run（Ticket derivation 之後）。 | 全部 | Bindings §3.3 |

其餘 activation 前提（OC §8 #1–#3）已於 2026-09-25 滿足（接受紀錄、b3、b2 dry-run）。

### 已知風險與處理

- **Vercel function 執行時間與回應大小**（OC §5）：實作期驗證；若上游逾時無法設在平台上限之內或觀測回應超過平台限制，route DA（可能調整第 5.3 節儀器或裁剪策略，不改變語義）。
- **O-A0001-001 可能下架**：以 `upstream_error`／`invalid_response` 明確失敗、保留資料；不寫入任何持久狀態。
- **上游額度**（一般會員 20,000 次／日）：公開 endpoint 由使用者手動 Refresh 觸發；重用視窗與逾時是唯一契約內節制；耗盡即 `upstream_error` → Stale。速率限制為 Later。
- **雷達 metadata 與影像的週期不一致**：README 記為已知限制；時間戳來自與影像同一次取得。
- **雷達重投影**：線性貼圖不符 R-V2-RAD-5（DA 已計算 ≈ 3.8 km）；重投影或 CRS 選擇屬 HOW；系統性偏移無法解決時 route DA。
- **測站座標在圍欄外**（東沙、南沙等）：依 R-V2-DD-11 處理，不是缺陷。
- **`app.py` 與 `weather_query.py` 的靜態檢查集合**：任何把觀測程式碼放進這兩個檔的做法都會使 AC-V2-16 FAIL；觀測程式放在其他模組（結構 HOW）。

### 詞彙

以 `CONTEXT.md`（V1）＋ BRIEF-V2 §9（V2 delta，R-V2-DOC-4 併入後）為準：Now mode、Forecast mode、Latest Observation、Observation Time、Fetched Time、Refresh、Re-ingestion、Stale、Unavailable、Taiwan Map、County、Region、Derived Map Temperature、Forecast Snapshot、Grading App、Dashboard、MVM、Scope class。

## 10. 版本紀錄

| 版本 | 日期 | 變更 | 性質 |
| --- | --- | --- | --- |
| v2.0 | 2026-09-25 | 初版 derive（V2 Outcome Contract ACCEPTED，candidate `69c5a04`，接受紀錄 `f853bcb`；Bindings b3）。 | derived contract（治理 §1.2）；不改變 V1 Spec v1.1 任何文字 |
| v2.1 | 2026-09-25 | acceptor 指示的 DA 修正（PR #34 未合併；OC-V2 不變）：(1) R-V2-MAP-2、AC-V2-13(c)、§5.3——移除「E 全部／22 縣市同時在視窗內」的下限 PASS 條件（超出 S-8／D-14 的接受語義），下限只以本島 ≥ 25% 視窗高與圍欄判準驗證；`minZoom` 6 保留為儀器。(2) R-V2-MAP-1、AC-V2-13(b)、§5.3——pan oracle 由「視窗 ∩ E ≠ ∅」改為「中心在 E 內＋逐軸視窗 ⊆ E 或 E ⊆ 視窗」，並要求金門／連江以截圖證明可達。(3) R-V2-RAD-3、AC-V2-18、R-V2-DOC-1(9)、AC-V2-21(10)——移除「Refresh MUST 一併重取雷達」的耦合；重新取得的觸發方式改為 HOW（使用者動作、不輪詢、狀態獨立、README 記載）。(4) R-V2-TC-1、§6.1、AC-V2-02／06／07／09／15／16／19／23 證據欄——新 V2 驗證改為框架中立的證據類別用語；V1 既有 pytest／Flask test client／靜態守衛只以既有回歸事實命名；PASS／FAIL oracle 未弱化。(5) Radar 1 km 對齊 oracle 經比例性複核後保留（derivation record DV-13 補充）。 | 治理 §5.3 第 2 類（不改變 accepted 語義的 derived contract 修訂）；不改變 V1 Spec v1.1 任何文字；詳見 derivation record §14 |
| v2.2 | 2026-09-25 | acceptor 指示的最終一致性修正（OC-V2 不重開）：v2.1 的 R-V2-OBS-2 未要求有效測站具可解析的 `ObsTime`，使 R-V2-OBS-4 的最大值與 R-V2-DD-7 的測站 Observation Time 可能對某站無定義。修正：R-V2-OBS-2 新增 (e)「有 CWA 發布且可解析的 `ObsTime`（如發布、不正規化；解析方式 HOW；新舊不影響有效性）」，缺少或無法解析者不進氣溫圖層、代表測站選取、縣統計與 dataset-level Observation Time；R-V2-OBS-4(a) 明示只取有效測站、成功回應下恆有定義；AC-V2-05 新增反例 (7)(8)（含「最新 `ObsTime` 的站改壞 → 最大值落到其餘有效站」）；R-V2-TC-1 涵蓋範圍同步。 | 治理 §5.3 第 2 類（derived-contract 一致性修正；S-1／S-2／S-5 的接受語義不變——S-2 的規則是最小集合，S-1「Observation Time 永遠可見」與 S-5「詳情含 Observation Time」已蘊含此條件）；不改變 V1 任何文字；詳見 derivation record DV-3、B-18、§14 |
