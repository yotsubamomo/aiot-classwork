# Decision record — #77 C-1／C-2：最壞情形的取消等待、載入上限與讀取大小（`home_work_02/`，HW2 V2 Enhance）

- **紀錄類型**：Design Authority decision record（治理 §2.4、§3.6、§5.3 第 2 類；Bindings b5 §2.4、§7）。
- **日期**：2026-10-22
- **Run**：`run-20261022-hw2-v2-enhance`（Orchestrator＝root session `37216426-f292-44f9-bad1-e2d862e7b8f1`；run record 第 210 列依治理 §2.4 直接派 DA，與 #77 R1 並行）。
- **來源**：#77 Executor worklog [`../worklog/issue-77.md`](../worklog/issue-77.md) §8 Concern **C-1**、**C-2**（連同 §4 D-9、D-10，§6.5）；#76 R1 [`../audit/issue-76-c1-r1.md`](../audit/issue-76-c1-r1.md) 觀察 **O-1**（§6、§7：交 #77）。
- **Outcome Contract**：[`../outcome-contract.md`](../outcome-contract.md) §5（V2，接受基準 `d7f02d4179d2cb5c2ecf0c39a4643a6ef8287907`）與 §5.2 CC-V2-1；§1–§4（V1）仍有效。
- **相關紀錄**：[`derivation-SPEC-V2.md`](derivation-SPEC-V2.md)（§0、§4 B-3、§7.2 H-3、H-4、H-5(d)、§7.4 #77、I-4）；[`decision-20261022-issue75-lasso-early-stop.md`](decision-20261022-issue75-lasso-early-stop.md)（R4-1 對原因碼枚舉的讀法、R4-2「原因必須如實」）；[`decision-20261022-r1f3-v1-footer.md`](decision-20261022-r1f3-v1-footer.md)（分配先例）。
- **Subject**：branch `home_work_02-v2-enhance`，commit `9d5a840727bf64627c65fa0e81cdfced5735a091`（實作 subject `5219f89`；`git diff --stat 5219f89 9d5a840 -- assets hw2 tests index.html` 為空）。撰寫時 HEAD `8797e2f`，與 `9d5a840` 只差 run record。
- **Binding**：`gov-design-authority`，有效 mapping `claude-opus-5-5`／`high`（Bindings §3.1 預設；沒有 escalation、沒有替代）。撰寫前我自行讀取本 assignment 的 transcript（agentId `ac84eb317f169a98b`，`agentType` `gov-design-authority`）：觀測到 `('claude-opus-5-5', 'high')` 36 則，單一元素。全程核對由派工者依 Bindings §3.6 執行；本紀錄不自證 binding。
- **Capability escalation**：不提出。E-DA/D1 不成立：兩個問題的每一個可行讀法，我都能以 accepted 文字與自己取得的事實裁決，沒有「兩個以上合理設計、後果實質不同、證據無法裁決」的情形（理由見第 4、5 節）。E-DA/D2 不成立：我先前對這兩個問題沒有決定；`derivation-SPEC-V2.md` 與本 run 的兩份 decision records 沒有被 FA ruling 或經 route 的 Reviewer finding 推翻或爭議。
- **獨立性**：Executor 的 worklog、ACCEPTANCE V2-27～V2-34 與 #76 R1 的敘述只當作待驗證主張。第 3 節是我自己讀碼、讀 committed evidence 與執行的結果。本紀錄不審查 #77 的實作（R1 並行進行）；第 3 節的事實只用來確定問題的範圍與票的義務，實作是否符合本紀錄由 #77 的 independent audit 判定。

## 1. 問題

- **C-1**：載入上限維持 Spec 候選值 50,000 列 × 60 欄時，不可略過的 All-in 在最壞情形（全部欄都是 20 層級的類別欄）單一候選要數分鐘；這段期間取消、或改選資料，都要等這個候選算完。這在 accepted 契約（非阻塞、下一個候選邊界取消、「50,000×60 只是候選」、「不承諾未量測的時間」）下是否可接受，或契約要求別的處理？降低載入上限、或新增拒絕規則，會不會改變 accepted 語義？
- **C-2**：URL 與本機檔案的讀取，在整份內容進入記憶體之前沒有位元組上限。accepted 契約是否要求位元組上限？新增 `TOO_LARGE` 式的位元組拒絕是在 boundary 內，還是 contract change？
- 對每一題：語義、#77 結案前是否必須實作任何事（或屬 #78、或無處承接）、是否須交 acceptor。

## 2. 依據（全部以接受基準 `d7f02d4` 的文字為準）

| 來源 | 內容 | 用途 |
| --- | --- | --- |
| Brief V2 §5.2；Q8 | 載入限制：「列數與欄數上限（候選值 50,000 列 × 60 欄，**只是候選**，以實測定；超過拒絕，不截斷）」；運算限制「與載入限制分開，不承諾所有演算法都能在載入上限的規模完成」；Q8「不承諾未量測的時間」 | 上限的數字不是 accepted 語義；accepted 的是「列數與欄數」這個量度與「超過拒絕、不截斷」 |
| Brief V2 §5.5；Q19；§11 | 「執行中有可觀察的進度」；「All-in 優先嘗試執行，但不保證任何資料都能成功；不預先承諾 LARS 或任何方法在特定時間內完成」；§11 把「列數上限的最終數字」「運算預算的具體數值與量測方式」列為 HOW | 進度、All-in、時間不承諾 |
| Brief V2 §8 第 5 條；US-18 | 失敗情境各有明確訊息，含「超過載入上限」；「效能只記錄實測、不預設門檻」 | 拒絕情境的枚舉；不設時間門檻 |
| Spec V2「載入契約」 | 「大小：列數與欄數上限為**載入上限**（…最終數字由實測後寫入實作常數並記錄於 ACCEPTANCE）；超過拒絕 `TOO_LARGE`，不截斷」；拒絕原因與 URL 子原因（網路或跨來源限制、HTTP 狀態、逾時、回應不是文字）是枚舉 | C-2 的核心：大小＝列數與欄數 |
| Spec V2「候選有效性、狀態與運算預算」 | 「All-in **永遠**優先嘗試執行」；只有 Forward／Backward／RFE 與 Lasso 的預算被定義，超出者整個方法 `SKIPPED_RESOURCE_LIMIT`；「本 Spec 不承諾任何執行時間」 | All-in 不可被略過 |
| Spec V2 SR-V2-03 | 非阻塞：「頁面的輸入、下拉、取消按鈕與進度顯示必須保持可操作；引擎以步驟為單位讓出控制權（至少每個候選一次），使進度事件與取消請求能被處理」；可終止：「取消請求在下一個候選邊界生效」；資源保護：「引擎在執行前依載入上限與預算估計拒絕或略過…任何方法的非預期例外（含記憶體不足）只讓該方法為 `FAILED`」；「引擎對同一輸入不並行啟動第二次執行（新的提交會先取消進行中的執行）」；進度：「方法、k、已完成比例、**已耗時**；UI 顯示」 | C-1 的核心 |
| Spec V2 US-27 | 「執行時看到進度, so that 我知道頁面沒有卡住」 | 進度顯示的目的 |
| `tickets-v2.md` 調整 B；#77 AC（body sha256 `c9b79356…90fe`，與 derivation §3 相同，2026-10-22 重算） | 取消「下一個候選邊界生效，不寫成瞬間終止」；AC「以候選計數證明不多算、**也不在候選中途中斷**」「執行中再次提交 → 前一次 `CANCELLED`、只剩一個進行中的執行」；人工檢查「進度持續更新」；What to build「讓探索引擎在**任意大小的合法資料集**上都『不卡死、可取消、可重現』」；共同條款「非阻塞的驗收以 UI 實際可操作性為準」 | C-1：取消時點、不並行、進度 |
| derivation §0、§7.2 H-5(d)、§7.4、I-4 | Spec V2 與 #74–#78 的 AC／invariant／gate 同時是 accepted 語義；H-5(d)「過大或過慢的輸入讓頁面卡死或影響 King County」，涵蓋「資源保護與取消」，#77 承接；I-4 報告不含探索結果數字、只引用靜態設定 | 分配與界線 |
| `decision-20261022-issue75-lasso-early-stop.md` R4-1、R4-2 | 新增原因碼會改變 accepted 的枚舉；畫面上的原因必須如實，不得宣稱未確立的原因 | C-2 的原因標示 |

## 3. 我自己取得的事實

讀碼（`9d5a840`，`assets/` 與 `5219f89` 相同）：

- `assets/explore_load.js` 第 73 行 `LIMITS = { maxRows: 50000, maxColumns: 60, minRows: 20 }`；`inspectCsv()` 先以 `decodeUtf8Strict()`（`TextDecoder` fatal）把整份位元組解碼成字串，**任何**例外都回報 `ENCODING`／`not_utf8`（`try { … } catch (e) { return … reject('ENCODING', { problem: 'not_utf8' }, sha256Hex(bytes)) }`）；之後 `sha256Hex()` 另配置一份與內容同大的陣列；列數超過上限在 `readRecords()` 解析中途判定為 `TOO_LARGE`（`rows_over`）。
- `fetchCsvBytes()`：`response.arrayBuffer()` 讀完整份本文；本文讀取的任何失敗都落到 `.then(null, function () { done(urlFailure('network')); })`，即 `URL_FETCH_FAILED`／`network`（訊息為網路或跨來源限制）。逾時 20 s（`URL_TIMEOUT_MS`）。`assets/explore_ui.js` `readFile()` 以 `file.arrayBuffer()` 讀整份檔案；失敗時顯示「無法讀取這個本機檔案（瀏覽器拒絕讀取）」。
- 進度：引擎只在開始、每個候選邊界與診斷前呼叫 `onProgress`（`explore_engine.js` 第 90、1297 行）；控制器只在收到這些事件時 `render({mode:'progress'})`（`explore_app.js` `execute()`）；`explore_ui.js` 沒有其他更新進度列的計時器。按下取消後進度列改為固定文字「取消中：目前的候選算完後（下一個候選邊界）停止。」，之後的進度事件不再寫入（`if (!byId('ex-cancel').disabled)`）。等待前一次執行停止的新請求顯示固定文字「等待前一次執行在候選邊界停止…」。`explore_ui.js` 檔頭註解寫「the progress line keeps updating」。

Committed evidence（`doc/screenshots/v2-issue77/chrome_subject_heavy.json`，Executor 的 headless Chrome 155）：

- 合成 50,000 列 × 60 欄（59 個 20 層級類別），訓練編碼 1,121 欄、237 個候選。執行面板 463 ms 出現；**第 8 秒的進度列**是「執行中（準備完成，開始計算候選）：已完成 0／237 個候選、0／5 個方法（0%），已耗時 0.2 秒」。取消 88 ms 後顯示「取消中…」，268,792 ms 後才結束為 `CANCELLED`（1／237）。全程輸入延遲最大 12.3 ms、畫格間隔 p95 12.7 ms；同時切到 King County 的方法切換 22.2／16.7 ms、long task 0。對外請求 0、dialog 0、例外 0。

我的執行（Node v24.19.0，V8，與 Chrome 相同的字串長度上限；scratchpad 外不留檔）：

- `buffer.constants.MAX_STRING_LENGTH` = 536,870,888；對 536,871,888 位元組、全部是 `a` 的**合法** UTF-8 以 `new TextDecoder('utf-8', { fatal: true, ignoreBOM: true }).decode()` 解碼，拋出 `Error: Cannot create a string longer than 0x1fffffe8 characters`（不是 fatal 解碼錯誤的 `TypeError`）。依上面的讀碼，`inspectCsv()` 會把這種輸入回報為 `ENCODING`／`not_utf8`。

## 4. C-1 的裁決

### C1-R1 最壞情形的取消等待本身符合 accepted 語義

在載入上限內，單一候選（例如不可略過的 All-in）可能算上數分鐘，而取消、改選資料或新的提交要等到這個候選結束才生效——這是下列 accepted 條款共同的直接結果，不是契約缺口：

1. 取消「在下一個候選邊界生效」，「不寫成瞬間終止」（Spec SR-V2-03；調整 B），且「不在候選中途中斷」（#77 AC）；
2. 「只剩一個進行中的執行」（#77 AC「不並行」），所以新的執行只能在前一次停止後開始；
3. 「All-in 永遠優先嘗試執行」（Spec），預算只定義在四個路徑方法；
4. 不承諾任何執行時間、不設效能門檻（Brief Q8、§5.5、US-18；Spec）。

非阻塞的 accepted 判準是 UI 實際可操作（共同條款）；取消的 accepted 判準是候選邊界與候選計數，不是等待時間。所以契約**不要求**降低載入上限，也不要求新的拒絕規則來縮短這段等待。

### C1-R2 載入上限的數字：50,000 × 60 在 boundary 內，維持

- 數字不是 accepted 語義：Brief 明寫「只是候選，以實測定」，§11 列為 HOW；Spec「最終數字由實測後寫入實作常數並記錄於 ACCEPTANCE」。accepted 的是量度（列數與欄數）與「超過拒絕 `TOO_LARGE`、不截斷」。
- 「以實測定」的判準（本紀錄的釐清，不是新 AC）：在參考環境、上限規模的最壞輸入上，觀察到 accepted 的性質成立——頁面可操作、取消在候選邊界生效、預算照估計略過、例外隔離、頁面與分頁沒有崩潰。**時間不是判準**（Q8、US-18）。V2-32 的實測顯示 50,000 × 60 在這些性質上成立（C1-R3 的進度顯示另論，那是 UI 的修正，不是上限的問題），所以維持。
- 之後若有實測依據要調整這個數字，屬治理 §5.3 第 2 類，由 DA 判定。但以「保證取消等待或完成時間不超過某值」為目的訂定上限，等於設立 accepted 契約明確拒絕的時間門檻，且為了把最壞情形縮到數十秒，上限必須降到會拒絕與 King County 同級（約兩萬列、二十餘欄）的資料，這是對 +2「可任意輸入 Dataset」支援範圍的取捨，沒有 accepted 依據——**我無法確立那種調整在 boundary 內**；若要做，屬 contract change，由 acceptor 決定（見 C1-R4）。

### C1-R3 契約要求：執行進行中的進度顯示必須保持即時

這一點是 accepted 契約在 C1-R1 所容許的長候選情形下**仍然要求**、而 C-1 沒有談到的部分。

- **語義**：一次執行在進行中的期間——包括單一候選持續很久、使用者已按取消而等待候選邊界、以及新的請求在等待前一次停止——頁面顯示的進度必須保持即時：至少「已耗時」要持續前進，使使用者能看出執行仍在進行。已完成比例、候選數與方法數可以維持候選邊界的粒度；**不要求**候選內部的比例，不改變取消的時點、不並行規則或任何狀態語義；進度與耗時屬非確定部分，不影響結果契約與可重現性。
- **依據**：Brief §5.5「執行中有可觀察的進度」；Spec 進度內容包含「已耗時」且「UI 顯示」、「進度顯示必須保持可操作」；US-27 的目的「我知道頁面沒有卡住」；#77 What to build「在任意大小的合法資料集上都『不卡死』」與 AC「進度持續更新」。只在候選邊界更新的讀法，會讓頁面在數分鐘內一直顯示「已耗時 0.2 秒、0%」——顯示的已耗時不再是事實，使用者也無從分辨頁面是否卡住，與上列每一條的目的衝突。所以這不是兩種同樣合理的讀法，而是 accepted 文字只有一種讀法能全部滿足；它不新增 AC、seam 或 gate，「進度持續更新」本來就是 #77 的 AC，中型資料集是它的檢查情境，不是它的適用上限。
- **做法**是 HOW（例如 UI 端的計時器，或在讓出點發出進度事件），由 Executor 決定，只限 V2 檔案。

### C1-R4 會改變 accepted 語義的選項（都不需要；只有 acceptor 能選）

下列任一項都是治理 §5.3 第 1 類 contract change，DA 不得自行採用；本紀錄不建議，也不是任何票的完成條件：

| 選項 | 衝突的 accepted 條款 |
| --- | --- |
| 依編碼後設計矩陣大小或 All-in 估計量，在執行前拒絕整個執行（新的 `REJECTED` 原因或新的載入拒絕） | 新增拒絕情境與原因碼（Brief §5.2、§8 第 5 條；Spec 原因枚舉；R4-1 的讀法） |
| 讓 All-in 也有預算、可被 `SKIPPED_RESOURCE_LIMIT` | Spec「All-in 永遠優先嘗試執行」；Brief §5.5 |
| 在候選中途中止，或放棄被取消的執行、不等它到邊界就開始新的執行 | #77 AC「不在候選中途中斷」「只剩一個進行中的執行」；調整 B |
| 以時間上限為判準訂定載入上限 | Brief Q8、§5.5、US-18；Spec「不承諾任何執行時間」 |

### C-1 小結

- **是否改變 accepted 語義**：否。C1-R1、C1-R2 是 accepted 文字的直接結果與「以實測定」的釐清；C1-R3 是 accepted 進度語義在長候選情形的唯一一致讀法。
- **#77**：**需要 rework**（C1-R3）。依第 3 節的讀碼與 committed evidence（第 8 秒仍是「已耗時 0.2 秒」，取消後與等待中的文字固定），`5219f89` 在長候選、取消中與等待中都沒有即時進度；是否已符合 C1-R3 的最終判定屬 #77 的 independent audit。
- **#78**：揭露（第 6 節）。
- **Acceptor**：不需要。C1-R4 是 acceptor 若想縮短最壞等待時可選的 contract change，不是待決項目。

## 5. C-2 的裁決

### C2-R1 accepted 契約不要求位元組上限

accepted 的「大小」只有列數與欄數（Spec「載入契約」大小一條；Brief §5.2）。Brief、Spec、#74–#78 都沒有位元組數、檔案大小或下載量的限制，也沒有對應的拒絕訊息。derivation H-5(d) 把「過大的輸入」列為高風險機制，作用是要求審查核對資源保護，不新增需求（derivation §7.1：類別只啟動既有機制）。

### C2-R2 以位元組數拒絕在上限內的輸入是 contract change

對一份列數與欄數都在載入上限內、瀏覽器也讀得進來的輸入，因位元組數而拒絕（不論叫 `TOO_LARGE` 或其他名稱），是 accepted 載入契約沒有的拒絕條件，會讓 accepted 契約下應該載入成功的輸入改為失敗——治理 §5.3 第 1 類，只有 acceptor 能決定。它不是 V2 的完成條件，**不得**在 #77 或其他票中實作，除非 acceptor 另行核准。Executor D-10 不加位元組上限的判斷正確。

### C2-R3 契約在讀取階段實際要求的事（既有語義，不是新規則）

不設位元組上限，不代表讀取階段可以對大型輸入給出任意結果。下列兩點是既有 accepted 語義在大型輸入上的適用：

- **(a) 超過列數或欄數上限的輸入，只要頁面取得了它的位元組，就以 `TOO_LARGE` 拒絕，不論位元組數多大。** 依據：Spec「超過拒絕 `TOO_LARGE`」與 Brief §8 第 5 條「超過載入上限」各有明確訊息；+2 的輸入是任意的。
- **(b) 不得回報未確立的原因。** 因輸入大小造成的環境失敗（配置失敗、超過瀏覽器的字串長度上限等）不得被回報為 `ENCODING`／`not_utf8`（內容其實是合法 UTF-8），也不得被回報為 `URL_FETCH_FAILED` 的網路或跨來源限制（本文其實已收到）。瀏覽器無法取得或處理輸入、因而無法確立 `TOO_LARGE` 或其他原因時，頁面如實說明是瀏覽器因輸入大小或記憶體無法處理——這是報告實際發生的環境失敗，不是新的拒絕規則，**不新增原因碼或 URL 子原因**（沿用既有「無法讀取這個本機檔案」這類不在原因枚舉內的訊息形式）。依據：Spec 原因與子原因的枚舉語義、Brief §8 第 5 條、R4-2「畫面不得宣稱未確立的原因」、derivation H-4。
- **限制**：在現行實作已能處理的範圍（位元組可解碼成字串的輸入），`LoadResult` 的結果（原因、detail、sha256、欄位與資料）必須與現在相同；修改只影響目前會失敗或被誤標的大型輸入。做法（例如在解碼前以位元組層的 RFC 4180 記錄計數提前判定 `TOO_LARGE`、分段解碼、或以 `File.stream()`／`response.body` 串流讀取，並區分解碼錯誤的例外型別）是 HOW，由 Executor 決定，只限 V2 檔案；串流或提前判定本身不是要求，只是可用的手段。
- **與第 3 節事實的關係**：V8 在解碼超過 536,870,888 字元的合法 UTF-8 時拋出的是一般 `Error`，而 `inspectCsv()` 把任何解碼例外都回報為 `not_utf8`；所以一份大於約 512 MiB 的合法 CSV（例如列數遠超上限的大型公開資料集）在 `5219f89` 會被說成「不是 UTF-8」，而不是 `TOO_LARGE`；URL 本文讀取的配置失敗會被說成網路或跨來源限制。這不是 #76 已驗證範圍內的缺陷（#76 R1／R2 驗證的輸入都在這個大小以下，#76 的結案不重開），而是 O-1 交給 #77 的資源保護範圍（derivation §7.2 H-5(d)、§7.4）。是否已符合 C2-R3 的最終判定屬 #77 的 independent audit。

### C-2 小結

- **是否改變 accepted 語義**：否。C2-R1、C2-R2 是 accepted 文字的讀法；C2-R3 是既有載入與原因語義在大型輸入上的適用，不新增拒絕條件、原因碼或子原因。
- **#77**：**需要 rework**（C2-R3 (a)(b)）；**不得**實作位元組上限（C2-R2）。
- **#78**：揭露（第 6 節）。
- **Acceptor**：不需要（有在 boundary 內可行的處理）。若 acceptor 希望以位元組數拒絕輸入，是 C2-R2 所述的 contract change，屬 acceptor 的選擇，不是待決項目。

## 6. 受影響的工作與各自的義務

| 對象 | 義務 |
| --- | --- |
| **#77**（結案前） | (1) **C1-R3**：執行進行中（含長候選、取消中、等待前一次停止）的進度顯示保持即時，至少已耗時持續前進；不改取消時點、不並行規則與結果契約。(2) **C2-R3**：超過列數或欄數上限、且位元組已取得的輸入以 `TOO_LARGE` 拒絕，不論大小；大小造成的環境失敗如實說明，不標為 `ENCODING`／`not_utf8` 或網路／跨來源；不新增原因碼或子原因；現行可處理範圍內的 `LoadResult` 不變。(3) 不實作位元組上限（C2-R2）。(4) 紀錄更正：worklog D-9、D-10 與 §8、ACCEPTANCE V2-32（及 V2-30 若受影響）、`explore_ui.js` 檔頭關於進度的註解，與修正後的證據一致。(5) **證據**（Executor self-verification；做法由 Executor 決定，不是新 seam 或新 AC）：一份單一候選耗時夠長的資料（V2-32 的極大資料，或較小但足以觀察的類別資料）上，執行中、取消中與等待中的已耗時都在前進，取消仍在候選邊界生效；一份列數超過上限、且大於約 512 MiB 的合法 UTF-8 輸入得到 `TOO_LARGE`；一個被迫在大小上失敗的讀取或解碼（可注入）不被標為 `ENCODING` 或網路；全部 pytest 與 Node 測試通過、0 skipped；A-3 sha256 與 V1 區塊不變；既有測試（I-5）不改，V2 測試只擴充（R4-5 的規則）。(6) 修正受 #77 的 independent audit 覆蓋（Bindings §5；治理 §3.8、§5.3 第 2 類）：Orchestrator 把本紀錄放入 #77 R1／R2 的 pack，R1 若已作成 verdict，由同一 cycle 的後續審查核對，不另設 gate |
| **#78** | README 與報告「探索模式」章節的「限制」（#78 既有 AC「探索模式的限制與揭露」「限制與揭露」，不是新 AC）加入：(a) 取消與改選資料在下一個候選邊界生效，在載入上限規模、類別層級多的資料上，單一候選（包括一律嘗試的 All-in）可能需要數分鐘，頁面在此期間仍可操作、King County 可用，不承諾任何時間；(b) 載入上限以列數與欄數判定，沒有檔案大小上限，輸入會整份讀入瀏覽器記憶體，超過瀏覽器能力的極大檔案可能無法讀取。報告依 I-4 不手抄實測數字（實測值留在 ACCEPTANCE V2-32，可經建置流程或指向引用）；載入上限與預算常數照 I-4 帶入 |
| **#76** | 不重開；其 AC 證據對其驗證的輸入仍然成立 |
| **Spec Integration Audit（Spec V2）** | 依 H-5、H-4 核對 C1-R3、C2-R3 在整合 subject 上成立，以及 #78 的揭露 |
| **Run record** | Orchestrator 記錄本紀錄的路徑與 #77 的 rework 需求；把本紀錄放入 #77 審查與 Spec Integration Audit 的 pack |
| **Outcome Contract、Brief、Spec、tickets、GitHub issues** | 不修改 |

## 7. 是否改變 accepted 語義、是否須交 acceptor

- **否**。本紀錄屬治理 §5.3 第 2 類：C1-R1、C1-R2、C2-R1、C2-R2 是 accepted 文字的讀法；C1-R3、C2-R3 是既有 accepted 語義（進度、`TOO_LARGE`、原因如實）在大型輸入與長候選上的唯一一致讀法，不新增 requirement、AC、invariant、gate、原因碼或 seam。
- **沒有 fail-closed 的項目**：兩題都有在 boundary 內可行的處理，不需要 acceptor 的決定才能完成 V2。
- 會改變 accepted 語義的選項（C1-R4 全部、C2-R2）只列出供 acceptor 知悉；DA 不採用，也不 route 為待決項目。若之後 Executor 或 Reviewer 發現 C1-R3 或 C2-R3 唯一可行的做法需要新增原因碼、改變 `LoadResult` 在現行可處理範圍內的結果、或改變取消與不並行的語義，該路徑即超出本紀錄，須 route 回 Design Authority（可能需 acceptor）。

## 8. Evidence

- 讀取：Bindings b5 全文；治理 v2.2 §1.2、§1.4、§1.5、§2.1、§2.4、§2.5、§3.3–§3.6、§5.3；`outcome-contract.md` §5、§5.1、§5.2；`d7f02d4` 時點內容的 `BRIEF-V2.md`（§3、§5、§8、§10–§13）、`SPEC-V2.md`（載入契約、前處理、候選有效性與運算預算、結果契約、可重現性、Testing Decisions、人工檢查表）、`tickets-v2.md`；`gh issue view 77`、`gh issue view 78`（body sha256 `c9b79356…90fe`、`5e31ce34…33b2`，與 derivation §3 相同）；`derivation-SPEC-V2.md` 全文；`decision-20261022-issue75-lasso-early-stop.md`（第 1–3 節、R4-1～R4-5）；`audit/issue-76-c1-r1.md` 全文；`worklog/issue-77.md` 全文；`doc/acceptance/ACCEPTANCE.md` V2-27～V2-34；run record 第 193–210 列。
- 讀碼：`assets/explore_load.js`（第 73、100–155、205–262、330–405 行）、`assets/explore_app.js`（第 95–115、380–520 行）、`assets/explore_ui.js`（第 1–40、100–115、495–530、600–640 行）、`assets/explore_engine.js` 的 `onProgress` 呼叫點。
- Committed evidence：`doc/screenshots/v2-issue77/chrome_subject_heavy.json`（`checks.heavy_cancel`、`kc_while_background`）。
- 執行：`git diff --stat 5219f89 9d5a840 -- assets hw2 tests index.html`（空）；`git show 9d5a840:home_work_02/assets/explore_load.js | sha256sum`（`0526faa2…ac0b`）；Node v24.19.0 的 `TextDecoder` 字串長度上限檢查（第 3 節）；本 assignment 的 transcript binding。
- 寫入的檔案只有本紀錄；沒有修改 Outcome Contract、Brief、Spec、票、GitHub、實作或測試；沒有 commit。
