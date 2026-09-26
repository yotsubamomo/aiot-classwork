# Audit record — Issue #39，cycle 1，R2（scoped closure review）

| 欄位 | 內容 |
| --- | --- |
| Work Contract | GitHub Issue **#39**（`yotsubamomo/aiot-classwork`）「地圖圍欄與響應式可用性…」；契約同 R1 record [`issue-39-c1-r1.md`](issue-39-c1-r1.md) 表頭（OC-V2 `69c5a04`；SPEC-V2 **v2.2** §2.6、§5.3、§6.2、§6.3 AC-19；derivation `derivation-SPEC-V2.md`；decision A-1），另加 DA decision **DV-22** [`../decisions/decision-20260926-desktop-representative-marker-density.md`](../decisions/decision-20260926-desktop-representative-marker-density.md) §4.1／§4.2（解決 R1 routing signal R-1；§4.1 (1)～(5) 指定由本 R2 逐項核對）。 |
| 受審 subject | branch `home_work_01-v2-implementation`；BASE **`4651d33`**；R1 subject code anchor `ae0b9dc`；**修正後 code anchor `f3bf2452410811364e20f55f7bf9c015c5ad883a`**；HEAD `3db7582`（`f3bf245..3db7582` 只改 `doc/governance/worklog/issue-39.md`）；審查時本機 HEAD `912c207`（`3db7582..912c207` 只改 run record）——皆 record-only（Bindings §7）。Correction delta `ae0b9dc..f3bf245`：產品與測試只有 `static/app.js`、`static/styles.css`、`README.md`、`tests/test_fence_frontend.py`、`tests/check_fence_browser.py` 與 `doc/acceptance/screenshots/v2/issue-39/*` 證據；其餘為紀錄（R1 record、DV-22、derivation §14 一列、run record、worklog）與 Orchestrator 依 DV-22 §7-2 在 ticket 索引 `doc/ticket/tickets-v2.md` 加的一行（文件索引，不影響受審行為）。`index.html`、伺服器與老師檔案未改（見 §5）。單元目錄外 0 檔。 |
| Audit 種類 | **R2**（治理 §4.4 scoped closure review），**cycle 1**。範圍：R1 blocking **F-1** 是否真正解決；修正是否引入回歸；修正是否直接產生或暴露 blocking defect；另依 DV-22 §4.1 與派工逐項核對 (1)～(5)。不是第二次全面 audit；新的 non-blocking 事項不延長 cycle。 |
| 角色 | `primary_reviewer`（definition `gov-primary-reviewer`；Bindings §3.1 mapping `claude-opus-5-5`／`xhigh`） |
| Binding 證據 | 正式核對由派工者依 Bindings §3.4 記入 run record `run-20260925-hw01-v2-formal.md`（R1 列已記本 Reviewer `a2832f7b12b48dec1`；correction 列記 Executor `af8f083fccf7b5395`）。Reviewer 以 Bindings §3.4 指令自行觀察 harness 紀錄（session `05b8408b-260a-46d3-a4fe-ec07e3ec365a`）：`agent-a2832f7b12b48dec1` `gov-primary-reviewer` `[('claude-opus-5-5', 'xhigh')]`，其 transcript 內含本次 R2 派工訊息（R1 context 延續）；`agent-af8f083fccf7b5395` `gov-executor` `[('claude-opus-5-5', 'high')]`。與 Bindings §3.1 一致。此觀察只供對照，不取代派工者的核對。 |
| Independence（治理 §2.3、§4.6） | (1) **Context**：依治理 §2.3(1)／Bindings §3.5，R2 延續本 Reviewer 自己的 R1 context（未繼承 Executor 對話），並**重讀**修正後的檔案與 diff（`git diff ae0b9dc f3bf245` 的 `app.js`、`styles.css`、`README.md`、`test_fence_frontend.py`、`check_fence_browser.py` 全文 diff；DV-22 全文；worklog 修正段）。Executor 的 C-1～C-7 與 concerns (g)(h)(i) 一律視為待驗證主張。(2) **Binding**：見上一列。(3) **Autonomous access**：自行重跑 pytest、test id 差集、CI log、憑證掃描、全部瀏覽器檢查（輸出導向 scratchpad），並**自寫** probe（`r2probe.py`、`r2follow.py`，另重用 R1 的 `probe.py` 的 `sweep_one`／`dropped` 情境；皆在 scratchpad、未提交）：只沿用單元的 DevTools driver 與未修改 `server.create_app` 的 Rig；地圖讀數取自頁面載入前以 `L.Map.addInitHook` 取得的 Leaflet 實例；代表標記以**座標**對回 `/api/` 回應的 `stationId`（不依標籤文字）；可視比例以元素矩形對每個 overflow 祖先與視窗求交；DV-22 (2) 的碰撞以 44×44 必要可點區自算（0 px 與 2 px 兩種間距各算一次）。(4) **Self-written record**：本紀錄由 Reviewer 以自己的 Write 工具寫入。**Model diversity：`diversity_lost`**——Executor 與 Primary Reviewer 同為 `claude-opus-5-5`（Bindings §5、b2 override；decision A-7）。合法狀態，不減損 §2.3 的 independence。 |
| 日期 | 2026-09-26 |

## 1. 方法與環境

- 環境同 R1（Windows 11；`.venv` Python 3.12；Chrome headless／DevTools protocol）。**未讀取** `home_work_01/.env`、未發出任何 CWA 請求；瀏覽器情境全部對 loopback 上未修改的 `server.create_app`（哨兵金鑰、由已提交消毒樣本衍生的模擬上游）。
- 沒有 git 寫入、沒有修改追蹤中的檔案（本紀錄除外）；結束時 `git status --short` 只有審查前即存在、與本票無關的 `grep.exe.stackdump`。
- Commit 衛生：`f3bf245`、`3db7582` message 格式正確；`grep -icE "claude|co-authored|generated with"` → 0；`git diff --check ae0b9dc f3bf245`（排除 PNG）乾淨。

## 2. F-1 — **RESOLVED**

**修正內容（重讀 diff 確認）**：`styles.css:1041-1101`（≥ 1024 px）Now 面板改為 `height:562px; overflow:hidden` 的 grid，第 1～5 列為標題、Stale／Unavailable 區塊、三個時間、`Refresh`、`County`＋`Back to Taiwan`，第 6 列 `minmax(0,1fr)` 為資訊部分，只有 `#sheet-body` `overflow-y:auto`；欄寬 312 → 360 px。`app.js` 移除 `selectStation`／`selectCounty`／`toggleSheetExpanded` 內所有 `scrollIntoView`，改為只調整 `#sheet-body.scrollTop` 的 `scrollInPanel`（`app.js:1314` 起）；鍵盤焦點在清單項目時仍保持其可見（`:focus-visible` 條件，R-V2-DD-9(e)）。

**獨立驗證（自寫 probe，真實 CDP 滑鼠事件）**：1024×768、1100×900、1280×900 × success／Stale／Unavailable，路徑：全臺（無選取）、全臺＋點地圖代表標記選站、選縣、選縣＋**以滑鼠滾輪捲動資訊部分後點清單下方項目**、選縣＋點地圖縣內標記——共 36 個狀態。

| 量測（每個狀態） | 結果 |
| --- | --- |
| `#obs-time`、`#obs-fetched`、`#refresh-button`、`#mode-now`、`#mode-forecast`、`#county-select` 的可視比例（overflow 祖先＋視窗）與中心命中 | **36／36 全部 1.0 且命中** |
| `#back-to-taiwan`（選縣時）、`#obs-state-chip`（Stale／Unavailable）、`#obs-state-reason`（Stale／Unavailable） | 全部 1.0 且命中 |
| Now 面板 `scrollTop` | 恆為 0 |
| 選站後詳情 `#obs-sel-name` | 1.0 且命中（清單點選的 `detailId` ＝ 被點項目的 `data-station-id`） |
| 資訊部分可捲動區高度 | success 331 px、Stale 209 px、Unavailable 177 px（三個寬度相同）；詳情與清單在其內捲動可讀 |

對照：BASE `4651d33` 100%、R1 subject `ae0b9dc` 0%、修正後 100%——#36／#37 已稽核的「兩個時間與 `Refresh` 可見」行為恢復。自寫截圖 `f1-{1024x768,1100x900,1280x900}-{success,stale}-county-station.png` 目視一致。Executor 的新 F-1 情境（重跑 9／9）與上述結論一致。

**判定**：OC S-1「Observation Time 與 Fetched Time 永遠可見」、R-V2-OBS-4(c)、R-V2-RSP-6（關鍵控制可見可達）、AC-V2-14「桌機面板不遮蔽選取項與關鍵控制」在 R1 指出的全部桌機選取路徑上成立。**F-1 已解決。**（鍵盤路徑見 §6 (g)。）

## 3. DV-22 §4.1 (1)～(5) — 逐項核對（1280 與 375）

證據類別依 AC-V2-14（瀏覽器驗收＋DOM 量測）。讀數存於 Reviewer scratchpad `r2/p_dv22/r2probe.json`（每個被隱藏者與碰撞對象的矩形），並與 Executor 重跑的 `browser-check-results.json` `dv22` 互相獨立。

| 項目 | 1280×900 | 375×812 | 判定 |
| --- | --- | --- | --- |
| **(1) 集合完整** | 初始、zoom 8、`Back to Taiwan` 後：全臺圖層 22 個標記，以座標對回 `/api/` → 集合 **＝** `representativeStationIds`（22）；13 個被隱藏者皆 `visibility:hidden`、`tabindex=-1`、中心不可點。 | 同上三個狀態：22＝22；17 個被隱藏者皆 inert。 | **PASS** |
| **(2) 隱藏只因碰撞** | 初始：13 個被隱藏者**每一個**的必要可點區（pill 擴為 ≥ 44×44）都與一個顯示中代表的必要可點區重疊——基隆市／新北市／桃園市／新竹市／新竹縣／宜蘭縣 → 臺北市；苗栗縣／彰化縣／南投縣 → 臺中市；雲林縣 → 臺中市、嘉義縣；嘉義市 → 嘉義縣；臺南市／屏東縣 → 高雄市（例：基隆市 l937.1 t311.3 r986.9 b355.3）。以 **0 px** 間距重算亦全部重疊（沒有任何一個只靠 2 px 間距被隱藏）。zoom 8（名稱標籤顯示 10 個）與 `Back to Taiwan` 後同樣全部成立。碰撞框不含名稱標籤（`app.js` `markerBox`）；標籤與顯示中標記或較早標籤重疊時以 `label-off` 讓位（`app.js:1186-1193`、`styles.css:1012`）。2 px 間距記於 README「Marker density」。 | 初始：17 個被隱藏者每一個皆與臺北市／花蓮縣／高雄市之一重疊（0 px 亦成立）；zoom 8、`Back to Taiwan` 後同樣成立。 | **PASS** |
| **(3) 顯示者合規** | 初始與 `Back to Taiwan` 後顯示 9 個：兩兩必要可點區不重疊（0 px）、皆 ≥ 44×44、中心命中、25 點 44×44 網格全數命中、文字存在；zoom 8：10 個顯示中的標籤與其他顯示中標記的可點區及彼此皆不重疊。 | 初始與 `Back to Taiwan` 後顯示 5 個：同樣全部成立。 | **PASS**（zoom 8 的邊緣情形見 §6 (h)） |
| **(4) 確定性與文件** | 同資料同視窗載入 3 次，顯示集合相同（嘉義縣、澎湖縣、臺中市、臺北市、臺東縣、花蓮縣、連江縣、金門縣、高雄市）。README 的排名與 `app.js` `DENSITY_PRIORITY` 逐字一致；README 的「1280 顯示 9／22、手機 5／22」與實測一致。 | 3 次相同（臺北市、花蓮縣、連江縣、金門縣、高雄市）。 | **PASS** |
| **(5) 被隱藏縣的可達性**（抽驗 4 縣，含北部 2 縣） | 新北市：z7 hover 顯示縣名＋突顯、點選選縣、選單選縣、放大到 z11 代表標記出現並點選選站。基隆市：z7 沒有任何內部像素可指（3×3 淨空點 0 個），以滾輪放大到 z9 後 hover 顯示縣名、點選選縣；選單選縣；z9 代表出現並點選選站。南投縣：z7 hover／點選、選單、z9 出現並選站。嘉義市：z9 hover／點選、選單、z11 出現並選站。 | 新北市、基隆市、嘉義市：z8 hover 顯示縣名＋突顯、點選選縣；選單；z10 出現並選站。南投縣：z6 hover／點選、選單、z8 出現並選站。 | **PASS**——R-V2-DD-4 未綁定縮放層級（#38 R1 判斷；DV-22 §4.2(5) 只要求「可經 hover／點選選取」）；初始縮放的多邊形指標可達性仍依 #38 R1 F-2 disposition 交 SIA。 |

**DV-22 §4.1：(1)～(5) 全部 PASS。**

## 4. 修正造成的回歸核對

| 項目 | 結果 | 證據 |
| --- | --- | --- |
| 全套測試與 test id | **PASS** | `pytest -q` → **516 passed**；BASE `4651d33` 的 494 個 id 與 R1 subject 的 513 個 id **全部**仍在（`comm -23` 空），新增 3 個（`test_markers_hide_only_by_required_touch_area_collision`、`test_desktop_status_part_never_scrolls_out_of_view`、`test_deferred_map_steps_are_queued_not_dropped`）。 |
| 靜態守衛未弱化 | **PASS** | `test_fence_frontend.py` 既有斷言只有兩處隨變數改名（`hidden` → `it.hidden`）與一處欄寬（312 → 360 px），檢查的性質不變；`test_map_frontend.py`、`check_county_browser.py`、`test_secrets.py` 本次未改。 |
| 瀏覽器檢查工具未弱化 | **PASS** | `check_fence_browser.py`：`density_and_touch` 的排除條件改為「只有真的疊在地圖上的底部資訊面才排除其下方標記」並加視窗下緣界——R1 版在桌機誤把側欄當成覆蓋物而排除了地圖下半，改正後量測集合變大；其餘為新增 F-1、DV-22 情境。 |
| #39 全部檢查 | **PASS** | Reviewer 重跑 `check_fence_browser.py` → **113/113**：AC-V2-13（初始 1280 z7／375 z6 含本島＋澎湖；下限 30.2 %／46.9 %；上限 28.95／29.06 px/km、375 px ≈ 12.9 km；臺北市 19 站 0 問題；fence sweep 0 失敗）、AC-V2-14（375 資訊面、44×44、11 個 375 狀態無橫向捲動、768 無破版、R-EN-1 六項與三狀態截圖）、AC-V2-15（15 步無 NaN／0×0）。 |
| (i) 欄寬 360 px 後的地圖與圍欄 | **確認** | 地圖寬：1024 → 548 px、1100 → 624、1280／1440／1920 → 644；五個寬度的初始視野皆含本島全部與澎湖本島、圍欄成立。自寫 sweep（1280×900、1024×768；z7、z8、z12；六方向拖曳）156 次讀數 0 違反。 |
| #36／#37／#38／V1 | **PASS** | `check_modes_browser.py` **37/37**、`check_refresh_browser.py` **97/97**、`check_county_browser.py` **72/72**、`check_series_error_visible.py` PASS。 |
| 執行期網路 | **PASS** | 重跑 network log：505 個請求，外部 **0**。 |
| CI | **PASS** | run `36223369715`（head `f3bf245`）success：log `516 passed`、`credential scan passed: 733 tracked files`；其後 `3db7582`、`912c207` 的 CI 亦 success。 |
| 憑證 | **PASS** | `python -m tools.credential_scan` passed（733 files）；`git ls-files` 無 `.env`。 |
| R1 F-2（Low，本次順修） | **已解決** | `ensureMapSized` 改為佇列（`app.js:1966-1985`）。R1 的重現情境（容器 0 尺寸時先關資訊面再切 Forecast）重跑：地圖上 Forecast pill **6**、測站標記 0、縣 path 0（R1 為 0／60／22）。 |
| R1 F-3（Low） | 未改 | 依 R1 disposition 交 SIA 觀察；本次修正未使其惡化。 |

## 5. High-risk 核對段重述（decision A-1；R2 對修正結果重述）

- **H-2**：correction delta 未觸及 `index.html`（`git diff ae0b9dc f3bf245 -- static/index.html` 空）、masthead、Forecast section、`app.py`、`data.db`、`weather_query.py`、`ingestion/`、`requirements.txt`、伺服器檔、`static/data`、`static/vendor`、workflows（皆空 diff）；`app.py`、`weather_query.py`、`data.db`、`smoke.py` blob 與 `main` 相同。#36 檢查（下方 dashboard、`Select Region`、概念詞）37/37；R-EN-1(1) 標題逐字 PASS。**結論不變：PASS。**
- **H-1**（附帶）：伺服器與金鑰路徑未改；憑證掃描 passed。**H-3**（附帶）：密度與標籤讓位只切換可見性，不計算值；County 脈絡未改。

## 6. Executor 新 concerns 的判斷

- **(g) 1024×768 鍵盤走到清單下方時頁面被捲動** —— **Reviewer 立場：不屬 F-1，不是 finding；記為 O-5。**
  - 量測：自 `Back to Taiwan` 連按 Tab 進清單至第 21 項後 Enter。1024×768：面板 `scrollTop` 恆 0；所有狀態元素在面板內的可視比例恆 1.0（沒有被 app 的容器裁切或被任何面板／overlay 遮蓋）；但瀏覽器自身的焦點捲動把**頁面**捲到 `scrollY` 443（success）／406（Stale），模式切換離開視窗，success 時 Observation Time、Fetched Time 亦離開視窗（`Refresh` 38 %），Stale 時兩個時間仍在視窗內。1100×900 與 1280×900 同一走查 `scrollY` 恆 0、全部可見。
  - 理由：F-1 是 **app 自己的容器捲動**在全部桌機寬度（含整張地圖卡完全放得下的 1280×900）、每一條滑鼠選取路徑上把兩個時間裁出唯一的顯示位置；(g) 是視窗高度（768）小於「卡頭約 300 px＋面板 562 px」時，**瀏覽器對文件的焦點捲動**，效果與使用者用滾輪捲動頁面相同：元素仍在原處、未被隱藏、裁切或遮蓋，把頁面捲回即見。契約的「永遠可見」在本 Spec 從未被解讀為 sticky 固定於視窗（任何票都沒有這樣要求；使用者捲到下方 dashboard 時兩個時間本來就離開視窗）；R-V2-MODE-2(a) 的「不捲動即可見」針對載入時，仍成立；R-V2-RSP-6 規範的是面板與 overlay 的遮蔽，此處沒有。此立場與 R1 對 375×667 頁面自動捲動使模式切換暫離視窗（R1 AC-V2-14 列）的判斷一致。Reviewer 與 Executor 在此沒有分歧，不構成 §4.3 爭議。
  - 附記（O-6，非 finding、非回歸）：鍵盤 Enter 選清單下方項目後，詳情在資訊部分頂端、焦點項目保持可見，因此詳情暫在資訊部分可視區外（三個寬度皆然）。這是 #38 已稽核的鍵盤焦點優先行為（R-V2-DD-9(e)），詳情在同一捲動區內捲回可讀，選取在清單與地圖上可見；供 SIA 知悉。
- **(h) 縮放鈕下的標記保留顯示** —— **可接受，不是 finding；記為 O-7。** 驗收視野的全臺初始與 `Back to Taiwan` 後（1280、375）**沒有**任何顯示中標記在縮放鈕或 attribution 之下。放大後的任意視野才會出現：375 z8 新竹縣（重疊 30 %）與苗栗縣（60 %）在縮放鈕下，皆 `tabindex=-1`；1280 z8 臺東縣 44×44 網格下緣 5 點落在 attribution 控制上（中心命中）。DV-22 §4.1(2) 明文禁止以非碰撞理由隱藏標記，保留顯示是唯一合規做法；被蓋住時不作為 Tab 停駐點維持 R-V2-DD-9(e)；平移即可點選，且該縣仍可經選單與清單選取——與 R1 O-4 同性質（地圖角落控制的一般性質，等同標記位於地圖邊緣）。
- **(i) 欄寬 360 px、1280 地圖約 644 px** —— **確認**：地圖寬 644 px（§4）；AC-V2-13 全部重跑 PASS，自寫 sweep 0 違反，初始視野含本島＋澎湖。

## 7. 修正直接產生或暴露的 blocking defect

無。新的觀察 O-5～O-7 皆為 non-blocking、不延長 cycle；R1 的 O-1～O-4 與 F-3 維持 R1 的處置。

## 8. Evidence（Reviewer scratchpad，未提交）

`C:\Users\yotsu\AppData\Local\Temp\claude\D--nchu-2026-AIoT-git-repository-aiot-classwork\05b8408b-260a-46d3-a4fe-ec07e3ec365a\scratchpad\`：
- `r2probe.py`、`r2/p_f1/`（F-1 36 狀態＋鍵盤走查、(i) 五個寬度的初始視野；截圖 `f1-*.png`）；`r2/p_dv22/`（DV-22 (1)～(5)、sweep）；`r2follow.py`＋`r2/follow/`（基隆市放大後 hover、臺東縣 z8 網格、375 z8 縮放鈕下標記）；`r2/dropped/`（F-2 重現）。
- `r2/fence/`＋`fence.log`（Executor #39 檢查重跑 113/113）；`r2/reg_{modes,refresh,county,series}`（37/37、97/97、72/72、PASS）；`r2/subj_ids.txt`（516）。
- 指令：`pytest -q`；`pytest --collect-only` 差集（對 BASE 494、R1 513）；`gh run view 36223369715 --log`；`python -m tools.credential_scan`；`git diff --stat／--check ae0b9dc f3bf245`；`git rev-parse main:<file>` 與 `f3bf245:<file>`；Bindings §3.4 binding 指令。

VERDICT: CLOSURE
