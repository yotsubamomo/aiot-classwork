# Spec V2: HW2 Enhance — 兩種 problem 的下拉與任意資料集的 Exploratory run（`home_work_02/`）

- **來源**：已接受的 [Brief V1](../brief/BRIEF.md)（不變）＋ [Brief V2（Enhance，rev 2，ACCEPTED 2026-10-21）](../brief/BRIEF-V2.md)。本 Spec 由 MATT `/to-spec` 產生，是 [Spec rev 5](SPEC.md) 的**增量修訂**：rev 5 原文不改，本檔沒有提到的事項一律以 rev 5 為準；兩者衝突時以本檔為準，但本檔只能在 Brief V2 §3.5 列出的四項覆寫範圍內與 rev 5 不同。Brief 與本 Spec 不一致時以 Brief 為準並回報。
- **詞彙**：依 [`../../CONTEXT.md`](../../CONTEXT.md)（Problem、Formal analysis、Exploratory run、Dashboard、Submission package 已於 2026-10-21 更新）。
- **版本**：rev 2（2026-10-21）— **ACCEPTED**（acceptor 2026-10-21：rev 2 審查 CONDITIONALLY ACCEPTED，條件為 Brief V2 §5.2／§5.5 的勘誤 E-1；勘誤完成且無剩餘契約衝突後標記 ACCEPTED）。rev 2 依 acceptor Spec Review（CHANGES REQUESTED）處理 SR-V2-01～SR-V2-04（處理紀錄見 Further Notes「Spec Review 的處理」）；rev 1（2026-10-21）為 `/to-spec` 初版。下一步 `/to-tickets` 尚未授權。
- **GitHub Issue**：[yotsubamomo/aiot-classwork#73](https://github.com/yotsubamomo/aiot-classwork/issues/73)（label `ready-for-agent`；2026-10-21 發布，待 acceptor 審查）。Issue 本文與本檔於發布時相同；之後若修訂，以本檔為準並同步更新 Issue。
- **測試 seams**（acceptor 2026-10-21 確認，ACCEPTED WITH CLARIFICATIONS）：(1) 主 seam＝Exploratory run 的結果契約（純函式引擎，Node 對 Python 通用參照 fixture；「與 `model_data` 同構」指沿用相同的分析概念與指標定義，不強制相同的 JSON schema）；(2) 次 seam＝CSV 載入契約（純函式；明確區分 parsing 與 train-only preprocessing；另加 mock fetch 的輕量 Node 行為測試驗證請求隔離）；(3) 靜態 seam＝`offline_scan` 只對探索載入模組開放受限的 `fetch` 例外；(4) UI＝ACCEPTANCE.md 人工檢查表。不新增第五個 seam，不引入瀏覽器 E2E 框架。
- **不變的檔案**：rev 5 的 Spec、V1 的票務索引與 issue #59；V2 的票用新檔與新 issue。

## Problem Statement

老師在 2026-10-21 更新了 HW2 作業頁（SRC-4）：主要繳交改為「跟 DIC2 一樣 GitHub and web」，並公告兩項直接計入期末總成績的加分——(+1) 有下拉視窗呈現兩種 problem；(+2) 可任意輸入 Dataset（老師給的例子是一個 CSV 的 URL）。

現在的 dashboard 只會呈現 King County 這一個 problem，所有數字都來自主程式一次性匯出的 `model_data`；它沒有任何在瀏覽器裡做分析的能力，也沒有任何資料輸入。老師範例站的 Pages 版沒有這兩項功能可參考，老師自己的新版是用 Flask 後端做的，而本專案的契約不做後端。

同時，正式分析已經完成、合併、驗證過：唯一一次 Test evaluation、BR-01／CC-1 的 test 隔離、OV-1 的完全離線 gate 都是已交付的事實，任何新增功能都不能動到它們。

## Solution

在同一個 dashboard 頁面加一個 problem 下拉，有三項：**King County**（正式分析，頁面就是現在的 dashboard，既有區塊的內容與數字逐字相同）、**50 Startups**（老師範例資料，打包在單元內，離線可用）、**自訂資料集**（使用者貼 URL 或選本機 CSV）。後兩項由一個純瀏覽器端的 **Exploratory run** 引擎處理：載入並檢查 CSV、辨識數值與類別欄、固定 seed 的逐列 80/20 切分、只用訓練列的 5-fold CV 跑 Forward SFS、Backward SFS、RFE、Lasso 路徑（exact LARS）與 All-in，依 CV 選出各方法與整體的 winner，只對 winner 算 test 指標、逐筆 95% 預測區間與實際 vs 預測圖，並提供即時預測器。

探索引擎沿用正式分析的全部語義（Feature group 整組進出、RFE 的 group importance、canonical tie、train-only encoding、OLS 參數式 PI），但沒有任何 King County 專屬的派生規則，目標不取 log，切分不分組。每個探索區塊標示「探索執行，非正式評估」；探索結果每次重算、不保存、不進報告數字，也永遠不是 Test evaluation。

頁面載入與 King County、50 Startups 的所有操作維持零對外請求；唯一允許的對外請求是使用者在自訂模式提交 URL 後對該 URL 的一次讀取。無後端、無建置步驟、GitHub Pages 不變；README、報告（新增探索模式章節）與學號 ZIP 同步更新，Pages 與 ZIP 內的 dashboard 一致。

## User Stories

### 評分者（老師）

1. As an 評分者, I want 在 dashboard 上看到一個下拉視窗，裡面有兩種 problem（King County 房價、50 Startups 利潤）, so that 我能確認 +1 的加分條件成立。
2. As an 評分者, I want 把我公告的範例 URL 貼進 dashboard 就跑出回歸分析結果, so that 我能確認 +2 的加分條件成立，不需要安裝任何東西。
3. As an 評分者, I want 用 GitHub repository 連結與 web 連結就能看到完整成果, so that 這份作業符合「跟 DIC2 一樣 github and web」的主要繳交方式。
4. As an 評分者, I want 切換到 50 Startups 時看到特徵選擇方法的比較、最佳 k、test 指標、預測圖與即時預測器, so that 它和我在 DIC-2 示範的成果形式可比。
5. As an 評分者, I want 探索結果清楚標示「探索執行，非正式評估」, so that 我不會把它和作業的正式分析結果混在一起。
6. As an 評分者, I want 在 King County 這個 problem 看到的內容與數字和加分功能加入前完全相同, so that 正式分析的可信度不因新功能而改變。
7. As an 評分者, I want 離線解壓 ZIP 開啟 `index.html` 也能切換 King County 與 50 Startups, so that 加分功能不依賴網路。
8. As an 評分者, I want 報告裡有一章說明探索模式的功能、方法與限制, so that PDF 也記錄了加分功能的存在與邊界。

### Acceptor（作業作者）

9. As an acceptor, I want 兩項加分功能都在本次完成範圍內, so that 期末總成績的 +3 不被當成「有空才做」。
10. As an acceptor, I want 正式分析的數值、`model_data`、Test evaluation 紀錄與已驗證產物逐位元不變, so that V1 的全部 audit 與驗收仍然有效。
11. As an acceptor, I want 探索引擎的每個數值結果都有 Python 參照 fixture 可比對, so that 加分功能的正確性不是交給老師發現。
12. As an acceptor, I want 一條一致性測試證明通用參照在 King County 訓練表上重現正式分析的 canonical 路徑, so that 兩個 problem 的選模語義是同一套，而不只是名字一樣。
13. As an acceptor, I want 50 Startups 在 A-1 的有效性規則下「全部 k 有效」由 fixture 證明, so that 這個結論不是從 n=50、p_enc=5 推定出來的；若不成立，依 A-1 分析，不為了讓 fixture 通過而改契約。
14. As an acceptor, I want 切分前允許的資料檢查和只能由訓練 fold 學習的前處理統計量在 Spec 中分開列出, so that 探索模式沒有資料洩漏。
15. As an acceptor, I want 請求隔離有 mock fetch 的行為測試而不只有靜態掃描, so that 「只有提交 URL 才發請求」是被證明的，不是被宣稱的。
16. As an acceptor, I want README、報告、ZIP 與 Pages 同步, so that 老師從任何一個入口看到的都是同一版 dashboard。
17. As an acceptor, I want 探索模式的範圍被「不做」清單封住, so that 專案不會膨脹成通用機器學習平台。
18. As an acceptor, I want 效能只記錄實測、不預設門檻, so that 驗收不建立在未經證明的承諾上。
19. As an acceptor, I want V1 的 Spec、票務索引與 issue #59 原樣保留，V2 用新檔與新 issue, so that 歷史紀錄可追溯。

### Dashboard 使用者

20. As a dashboard 使用者, I want 選 50 Startups 後不需要任何輸入就看到完整結果, so that 我能先了解探索模式會給什麼。
21. As a dashboard 使用者, I want 在自訂模式貼一個 CSV 的 URL 並按下載入, so that 我能用自己的資料做多元線性回歸。
22. As a dashboard 使用者, I want URL 讀取失敗時看到明確原因（跨來源限制、找不到、逾時、不是 CSV）與「下載後用檔案載入」的指引, so that 我知道下一步怎麼做。
23. As a dashboard 使用者, I want 選本機 CSV 檔案載入, so that 不開放跨來源的資料集也能分析，而且離線也能用。
24. As a dashboard 使用者, I want 目標欄預設是最後一欄且可以用下拉改, so that 貼老師範例直接出結果，目標不在最後一欄的資料也能用。
25. As a dashboard 使用者, I want 目標欄不是數值時得到明確提示, so that 不會靜默跑出錯誤分析。
26. As a dashboard 使用者, I want 看到哪些欄被當成數值、哪些是類別、哪些被排除及原因、刪了幾列缺值, so that 我知道引擎用了什麼資料。
27. As a dashboard 使用者, I want 執行時看到進度, so that 我知道頁面沒有卡住。
28. As a dashboard 使用者, I want 超出運算預算的方法被標示「超出運算限制」而其他方法照常完成, so that 中型資料集至少有結果。
29. As a dashboard 使用者, I want 無效候選（秩不足、自由度不足）被標示並附原因，winner 只從有效候選中選, so that 我不會被無效模型誤導。
30. As a dashboard 使用者, I want 共線診斷告訴我哪一組欄位線性相依、對應到哪些來源特徵, so that 我能理解為什麼某些模型無效，而不是被指認某一欄「有問題」。
31. As a dashboard 使用者, I want 指標 vs k 圖與 KPI 用訓練 CV，test 指標只出現在各方法 winner 與整體 winner, so that 我學到「不用 test 選模」，與正式分析一致。
32. As a dashboard 使用者, I want 實際 vs 預測圖有逐筆 95% 預測區間, so that 我看得到每筆預測的不確定性。
33. As a dashboard 使用者, I want 即時預測器讓我輸入來源欄的值得到點預測與區間, so that 我能試用選出的模型。
34. As a dashboard 使用者, I want 選到無效、被略過或失敗的候選時，預測器停用並顯示狀態與原因, so that 不會得到沒有根據的預測。
35. As a dashboard 使用者, I want 同一份資料重跑得到相同結果, so that 我能重現並比對。
36. As a dashboard 使用者, I want 切回 King County 時看到原本的正式 dashboard, so that 探索不會污染正式結果。
37. As a dashboard 使用者, I want 頁面揭露逐列切分的限制（重複列、同一實體多筆、時間相依資料可能洩漏）, so that 我不會把探索結果當成正式研究結論。

### 實作者與審查者

38. As an 實作者, I want 探索引擎是不碰 DOM、不碰網路的純函式, so that 它能在 Node 跑並對 fixture 驗證。
39. As an 實作者, I want 載入契約是純函式（CSV 文字 → 表格、型態、排除清單、拒絕原因）, so that URL 與檔案只是兩個餵文字的入口。
40. As an 實作者, I want 通用 Python 參照重用正式分析已 group-generic 的數學準則, so that 不維護第二套語義。
41. As an 審查者, I want 離線靜態掃描只對一個探索載入模組開放 `fetch` 例外，其他檔案照舊禁止, so that 例外是可枚舉、可檢查的。
42. As an 審查者, I want 候選狀態與原因碼是枚舉, so that 失敗語義可以逐條驗證。
43. As an 審查者, I want King County 區塊的 DOM 與 `model_data` 不變有自動化證據, so that 「逐字相同」不只靠人眼。

## Implementation Decisions

### 範圍與不變量

- 本 Spec 只新增：problem 下拉、Exploratory run 引擎（含載入、分析、呈現）、50 Startups 內建資料、通用 Python 參照與其測試、README／報告／ACCEPTANCE／打包的對應更新。
- **正式分析不變量**：主程式、Python 分析套件的正式路徑、`model_data`、結果檔、Test evaluation 紀錄、V1 的 dashboard 區塊（DOM 結構與文字）全部不變。通用 Python 參照是新的模組，只被測試與 fixture 使用，正式路徑不 import 它。
- 兩項加分是同一個工作項目的兩個可觀察結果，不拆成兩套實作。

### Problem 與頁面結構

- 頁面頂部（控制列）新增 **problem 下拉**，三項依序：King County（正式分析）、50 Startups（探索）、自訂資料集（探索）。預設 King County。
- 選 King County：顯示 V1 的全部區塊，隱藏探索區塊。V1 區塊的 DOM、文字、資料來源（`model_data`）與行為不變；V1 的區塊 id、分層規則（BR-01）、SR-09 的量測機制照舊。
- 選 50 Startups 或自訂資料集：隱藏 V1 區塊，顯示探索區塊。探索區塊是獨立的 DOM 子樹，有自己的 id 命名空間，不重用 V1 區塊的元素。
- 探索區塊的每一個區塊標題帶「探索執行，非正式評估」標示；King County 區塊沒有這個標示。
- 切換行為：選 50 Startups 即以內建資料執行一次探索；選自訂資料集只顯示輸入面板，提交後才執行；從探索切回 King County 時探索區塊隱藏、其結果留在記憶體但不顯示；再切回探索 problem 時重新執行（50 Startups）或要求重新提交（自訂）。探索結果不寫入任何儲存（localStorage、URL 參數、檔案）。
- 頁面標題與品牌列保留 V1 文字；下拉的可及性遵守 OV-4（label、鍵盤操作、`aria` 狀態）。

### 50 Startups 內建資料

- 老師範例 CSV 複製一份進單元的靜態資源：以 **JS 全域變數內嵌 CSV 文字**（與 `model_data` 相同的載入方式），因為 `file://` 下不能 `fetch` 本機檔案；同時保留一份原始 `.csv` 供人閱讀與 ZIP 內追溯。測試驗證兩者內容相同。
- 記錄來源 URL、取得日期、內容 sha256 與授權（來源 repo 為 MIT）；README 的資料來源一節標示。
- 50 Startups 走與自訂資料集完全相同的載入契約與引擎，沒有專屬分支。它不宣稱符合正文的 >13 特徵條件。

### 載入契約（次 seam）

純函式：CSV 文字 → `LoadResult`。成功時含表格與欄位描述，失敗時含拒絕原因。**載入階段只做 CSV 結構檢查**（SR-V2-01）：每一項都是逐儲存格或逐列的格式判定，不計算任何欄位的分布、相異值數或變異，所以可以看全部列而不影響選模。凡是會決定「哪些欄成為 Feature group、以何種方式編碼」的判斷，都不在載入階段，而在切分後只用訓練列決定（見「前處理與洩漏邊界」）。

- 格式：UTF-8（接受 BOM）、逗號分隔、第一列為欄名、每列欄數與欄名數相同、引號依 RFC 4180 處理。不符合者拒絕：`NOT_CSV`、`NO_HEADER`、`RAGGED_ROWS`、`ENCODING`。
- 大小：列數與欄數上限為**載入上限**（候選值 50,000 列 × 60 欄；最終數字由實測後寫入實作常數並記錄於 ACCEPTANCE）；超過拒絕 `TOO_LARGE`，不截斷。
- 欄位型態：每個非空儲存格都能解析為有限數字的欄＝**數值欄**；其餘＝**類別欄**（去除前後空白後的字串）。這是逐儲存格的格式判定，不是分布統計。
- 缺值：任一欄為空的列整列刪除，回報刪除筆數；刪完不足 20 列拒絕 `TOO_FEW_ROWS`。
- 目標：預設最後一欄；可指定任一欄。目標必須是數值欄，否則拒絕 `TARGET_NOT_NUMERIC`（UI 以此提示使用者重選）。目標欄不進特徵。
- 重複的欄名：拒絕 `DUPLICATE_COLUMN`。
- **不在載入階段做的事**：類別層級數上限、常數欄排除、層級清單與基準、標準化參數、任何相依或秩的判斷。rev 1 把層級數與常數欄放在載入層（看全部列）是 SR-V2-01 指出的洩漏，rev 2 移到訓練列層。
- 輸出：欄位清單（名稱、型態）、保留列的表格、刪除筆數、內容 sha256（對原始文字）。欄位的「保留／排除」狀態不在 `LoadResult`，而在引擎以訓練列決定後寫入結果契約。
- 入口：URL 與本機檔案只是取得文字的兩種方式，取得後同一條路徑。URL 讀取失敗回報 `URL_FETCH_FAILED` 並附子原因（網路或跨來源限制、HTTP 狀態、逾時、回應不是文字），訊息同時給出「下載後以檔案載入」的指引。URL 讀取只在使用者提交時發生、對該 URL 一次、GET、不重試、不帶憑證。

### 前處理與洩漏邊界

明確分成三層（acceptor 2026-10-21 要求；SR-V2-01）。每一層只能看它被允許的列，後一層不得回頭改前一層的決定：

- **第一層：CSV 結構檢查**（載入契約，切分前，對全部列）：格式、欄數、欄位型態（逐儲存格解析）、缺值刪列、目標型態、重複欄名、大小上限、內容 sha256。不計算任何分布、相異值數或變異。
- **第二層：訓練集層的前處理決定**（切分後，只用**整個訓練集**的列；對所有 fold 與 canonical 共用，因為它決定的是 Feature group 的集合）：
  - 類別欄的層級數：以訓練列計算的相異值數 ≤ 20 才保留，超過的欄排除（`EXCLUDED_TOO_MANY_LEVELS`）；
  - 常數欄：在訓練列上只有一個相異值的欄排除（`EXCLUDED_CONSTANT`）；
  - 由此得到 Feature group 清單與 canonical 順序（CSV 欄序）。
  - test 列對這些決定沒有任何影響：一個只在 test 列上才有變化或才有新層級的欄，其在訓練列上的狀態就是它的狀態。
- **第三層：每個 CV fold 的前處理與選擇**（只用該 fold 的訓練列）：類別欄的層級清單與基準（基準＝該 fold 訓練列中最先出現的層級）、one-hot 欄的存在與否、Lasso 路徑的標準化均值與標準差、路徑的每一步、該 fold 的 OLS 係數與推論量。驗證列只用來算指標，出現未見層級時編為基準並計數。
- **Canonical 與最終擬合**：同樣的第三層規則，但只用整個訓練集；canonical 路徑、canonical fit、即時預測器與 test 評估用的 fit 都來自這裡。
- **test 列的讀取時點**：在第二層與第三層的全部決定（group 集合、各 fold 與 canonical 的路徑、所有 winner）固定之後才讀取；之後只用於 winner 的指標、逐筆預測與 PI。
- 未見層級：驗證列或 test 列出現該次訓練列沒有的層級時編為基準並計數；即時預測器只列出 canonical fit 的訓練層級加基準。
- 無任何資料專屬派生（無日期轉換、無整修旗標、無 `id` 概念）；目標不轉換（原始尺度建模與報告）。

### 切分與交叉驗證

- 固定 seed 的逐列隨機 80/20 切分（無分組）；訓練列再固定 seed 分成 5 fold。
- 亂數：使用一個**可在 JS 與 Python 以相同演算法實作的簡單 PRNG**（演算法由實作決定並記錄）與 Fisher–Yates 洗牌；seed 為固定常數。Python 參照以同一演算法產生相同的切分，測試驗證兩邊的切分指標相同。引擎另接受外部指定的切分指標（只供測試注入）。
- UI 的任何操作都不改變 seed；可重現性契約見「可重現性」。
- UI 與報告揭露逐列切分的限制：重複列、同一實體多筆、時間相依資料可能洩漏；探索結果不代表正式研究結論。

**候選、fold 子集、聚合、winner 與 test 的關係**（SR-V2-02；全部沿用 rev 5「分割與交叉驗證」「指標與推論」與正式分析套件的既有定義，不另發明）：

1. **fold 子集**：對每個路徑方法 m、每個 fold f，k = 1…p 的子集序列 S(m, k, f) 在 fold f 的訓練列上重新計算（fold-internal selection）；All-in 在每個 fold 的子集都是全部 group。驗證列不參與任何子集的選擇。
2. **fold 指標**：以 S(m, k, f) 在 fold f 訓練列上擬合 OLS（第三層前處理），在 fold f 的驗證列上算 MAE、MSE、RMSE、R²（目標原始單位）。
3. **CV 指標的聚合**：候選 (m, k) 的 CV 指標＝五個 fold 指標的**算術平均**，並附各 fold 值與標準差——與正式分析套件的候選 CV 聚合相同（`mean` 與 `std` 欄位、各 fold 的表）。任一 fold 不符合 A-1 時整個候選為 `INVALID_MODEL`，沒有 CV 指標。
4. **Canonical 子集與 fit**：候選 (m, k) 另有在整個訓練集上以同一方法計算的 canonical 子集 S(m, k) 與其 canonical fit。CV 指標估計的是「方法 m 在 k 下的程序」的表現，不是 canonical 子集本身的表現；UI 的方法說明與報告寫明這一點（rev 5 的選擇偏誤陳述同樣適用）。
5. **方法 CV winner**：該方法 `VALID` 候選中 CV RMSE 最小者；平手取較小的 k（正式分析的 `tie_break.method_winner`）。
6. **整體 CV winner**：各方法 winner 與 All-in（若 `VALID`）之中 CV RMSE 最小者；平手依固定的方法順序 All-in、Forward SFS、Backward SFS、RFE、Lasso 路徑（正式分析的 `METHOD_ORDER`）。
7. **凍結與 test**：第 1～6 點全部完成後，winner 集合凍結；只有此時才讀取 test 列，對每個 winner 的 **canonical fit** 計算 test 指標、逐筆預測與 PI。同一模型被多個 winner 共用時只算一次並記錄對應。test 結果不回饋第 1～6 點的任何決定；UI 的任何操作都不重算 test。

### Feature group 與特徵選擇

- Feature group：一個來源欄＝一個 group；數值欄一欄；類別欄＝其訓練層級的 one-hot 欄（基準層級不設欄）。選擇整組進出，k 數 group；k = 1…p（p＝保留的 group 數）。
- 方法：Forward SFS、Backward SFS、RFE、Lasso 路徑排序、All-in baseline。準則與正式分析相同：Forward／Backward 以 RSS；RFE 的 group importance＝`sd(X_g β_g)`（該 group 對擬合值的貢獻在訓練列上的標準差）；Lasso 以 exact LARS 的 entry（最大 entry alpha 先）排序；tie（相對容忍度與正式分析同值）依 canonical 順序＝CSV 欄序（forward／Lasso 先加前者，backward／RFE 先移後者）。
- 選擇邊界與正式分析同：每個 fold 的路徑只用該 fold 的訓練列；canonical 路徑只用整個訓練集；fold 子集可與 canonical 子集不同。
- 秩不足不中斷路徑：準則用最小範數最小平方解；能否擬合由候選有效性決定。
- **LARS 退化（A-2）**：路徑計算在 active set 退化（新增欄使 active set 秩不足）時停止；已求得的路徑段（entry alpha 與順序）是實際結果；退化後的 group 以欄序排在後面**只作展示**，標記為「未進入（退化後）」；k 超過退化步的 Lasso 候選為 `INVALID_MODEL`，原因 `lasso_path_degenerate`。這與正式分析的 canonical 補齊規則（未進入的 group 依欄序補成 k=1…18 的子集，是 King County 的選模語義）不同，兩者在 UI 與報告中分開說明。

### 候選有效性、狀態與運算預算

- 候選＝(方法, k)，加 All-in。每個候選有唯一狀態：
  - `VALID`：每個 fold 的訓練列與整個訓練集上，設計矩陣（含截距）滿秩且殘差自由度 ≥ 3（A-1）；有 CV 指標與 canonical fit。
  - `INVALID_MODEL`：不符合 A-1，或 `lasso_path_degenerate`；原因碼與涉及的 fold／group 必附；沒有 fit、不參與 winner、預測器停用。
  - `SKIPPED_RESOURCE_LIMIT`：該方法在執行前依運算預算估計為超出，未執行；原因附估計值與預算。
  - `FAILED`：非預期計算失敗（數值例外等）；原因附訊息；不參與 winner。
- **運算預算**：以「預估的 OLS 求解次數 × 訓練列數 × 編碼欄數²」為量度，每個方法各有預算；數字由實作在參考環境實測後定，記錄於 ACCEPTANCE；本 Spec 不承諾任何執行時間。All-in 永遠優先嘗試執行；Forward／Backward／RFE 的預算以 O(p²) 次求解估計、Lasso 以 O(p) 步估計；超出者整個方法標 `SKIPPED_RESOURCE_LIMIT`，其他方法照跑。**預算判定只依估計量**（訓練列數、編碼欄數、方法的複雜度），在該方法執行前完成，不依實際耗時；因此同一輸入的判定結果是確定的（見「可重現性」）。
- **資源保護、非阻塞與可終止**（SR-V2-03；具體技術由實作決定，本 Spec 不指定 Worker 或任何特定機制）：
  - **非阻塞**：探索執行期間，頁面的輸入、下拉、取消按鈕與進度顯示必須保持可操作；引擎以步驟為單位讓出控制權（至少每個候選一次），使進度事件與取消請求能被處理。
  - **可終止**：UI 有「取消」；取消請求在下一個候選邊界生效；取消後執行狀態為 `CANCELLED`，已算出的部分結果**不呈現為結果**（不顯示 winner、test、預測器），只顯示「已取消」與已完成的方法數；再次執行從頭開始。
  - **資源保護**：引擎在執行前依載入上限與預算估計拒絕或略過，執行中不分配超過估計的矩陣（設計矩陣與 (XᵀX) 的大小由編碼欄數與列數決定、可事前計算）；任何方法的非預期例外（含記憶體不足）只讓該方法為 `FAILED`，不讓整個執行中止，其他方法照跑；引擎對同一輸入不並行啟動第二次執行（新的提交會先取消進行中的執行）。
  - **進度**：引擎以事件回報進度（方法、k、已完成比例、已耗時）；UI 顯示。進度與耗時是非決定性資訊，不屬於結果契約的確定部分（見「可重現性」）。
- **秩不足與共線診斷（A-3）**：對整個訓練集的 All-in 設計矩陣做一次相依分析（方法由實作決定，例如 pivoted QR），輸出零或多組「線性相依欄位組」，每組列出涉及的編碼欄與它們映射回的 Feature group，以及相依形式的描述；不指認單一問題欄。這份診斷顯示在探索區塊並附在結果契約中。
- winner：各方法的 CV winner＝該方法 `VALID` 候選中 CV RMSE 最小者；整體 CV winner＝各方法 winner 與 All-in（若 `VALID`）之中 CV RMSE 最小者；平手規則沿用正式分析。所有候選皆非 `VALID` 時整個探索執行拒絕 `ALL_CANDIDATES_INVALID`，並顯示相依診斷。

### 評估、預測區間與即時預測器

- 指標（目標原始單位）：MAE、MSE、RMSE、R²；訓練 Adjusted R² 用實際秩。CV 指標＝5 fold 驗證列的指標平均（與正式分析同一聚合規則）。
- test：只對各方法 CV winner 與整體 winner（同一模型只算一次）在 test 列上計算指標、逐筆點預測、95% PI 上下界、covered 與 coverage。其他候選沒有 test 數字。test 指標不回饋任何選擇。
- PI：OLS 參數式 95% 預測區間 `ŷ ± t(0.975, df_resid)·√(s²(1 + x₀ᵀ(XᵀX)⁻¹x₀))`，在原始目標尺度，不取 exp。
- 實際 vs 預測圖：test 列全部、每筆垂直 PI 線段、依 covered 著色、y=x 線；軸為線性刻度（目標可為負或零，不用 log）；縮放與游標檢視沿用 V1 的繪圖元件行為。
- 即時預測器：只對目前選取且 `VALID` 的候選；輸入依該候選的 group 動態產生（數值欄：訓練 min／max／median 預設與超範圍警告；類別欄：訓練層級下拉加基準，未見層級以基準計算並警告）；輸出點預測與 PI。目前候選為 `INVALID_MODEL`、`SKIPPED_RESOURCE_LIMIT` 或 `FAILED` 時，預測器停用並顯示狀態與原因，不產生任何預測值或區間。
- 指標 vs k 圖與 KPI 只用訓練 CV 並標示「訓練 CV」；test 區塊標示「探索 test（非正式評估）」與所展示的方法與 k；選取非 winner 時 test 區塊展示該方法 winner 並提示。

### Exploratory run 結果契約（主 seam）

純函式引擎：輸入＝`LoadResult` 的表格與欄位描述、目標欄、seed（預設常數）、運算預算、（測試用）外部切分；輸出＝`ExploratoryResult`。它沿用 `model_data` 的分析概念與指標定義，schema 不必相同。內容：

- `run`：執行狀態 `COMPLETED`／`CANCELLED`／`REJECTED`（含拒絕原因碼）。只有 `COMPLETED` 的結果才有 `candidates` 以下的內容。
- `meta`：problem 識別、來源種類（內建／URL／檔案）、內容 sha256、載入列數、刪除筆數、seed、預算、引擎版本（以上為確定部分），以及各方法計時與執行時間戳（非確定部分，見「可重現性」）。
- `columns` 與 `groups`：欄位型態；以訓練列決定的狀態（保留／`EXCLUDED_TOO_MANY_LEVELS`／`EXCLUDED_CONSTANT`）；group 清單與 canonical 順序；canonical fit 的訓練層級與基準。
- `split`：訓練與 test 的列索引、fold 指派。
- `candidates`：每個 (方法, k) 與 All-in 的狀態、原因、各 fold 的子集與指標、CV 指標（平均與標準差）、canonical 子集；`VALID` 者另有 fit（編碼欄清單、係數、s²、df_resid、t 臨界值、(XᵀX)⁻¹、訓練層級與基準、訓練 Adjusted R²）。
- `lasso_path`：每個 group 的 entry alpha（已求得段）、退化步（若有）。
- `winners`：各方法 winner、整體 winner、共用模型的對應。
- `test`：只有 winner 的 test 指標、逐筆 predicted／lower／upper／covered、coverage。
- `dependencies`：相依欄位組與 group 映射。
- 契約不變量：非 winner 沒有 test 欄位；`VALID` ⇔ 有 fit；任一 test 逐筆的點預測與 PI 可只用 test 列原始值、`groups` 的編碼規則與該 fit 獨立重算；`covered` 等於 `lower ≤ actual ≤ upper`；coverage 等於 covered 之和除以 n_test；每個候選恰有一個狀態；`SKIPPED_RESOURCE_LIMIT` 與 `FAILED` 沒有 CV 指標；`CANCELLED` 與 `REJECTED` 的結果沒有 `candidates`、`winners`、`test`。

### 可重現性

（SR-V2-04）結果契約分成**確定部分**與**非確定部分**：

- **確定部分**：`run` 的狀態與原因、`meta` 的 sha256／列數／seed／預算／引擎版本、`columns`、`groups`、`split`、`candidates`（含各狀態與原因、各 fold 子集與指標、CV 指標、canonical 子集與 fit）、`lasso_path`、`winners`、`test`、`dependencies`。
- **非確定部分**：`meta` 的各方法計時、執行時間戳；進度事件；UI 顯示的耗時。
- **契約**：同一份內容（sha256 相同）、同一目標欄、同一 seed、同一引擎版本與同一組預算常數 → 確定部分逐值相同（浮點數逐位相同；同一引擎在同一瀏覽器下應為位元相同，跨瀏覽器以相對 1e-9 比較並記錄）。內建、URL、檔案三種來源只是文字的入口，內容相同即確定部分相同。
- 不屬於契約的事：執行時間、進度的時間點、取消發生的時點。`SKIPPED_RESOURCE_LIMIT` 由估計量決定，因此屬於確定部分；`FAILED` 的發生若來自環境（記憶體不足）可能不可重現，其原因訊息記錄環境資訊；`CANCELLED` 由使用者動作決定，不是可重現性的對象。
- 任何「重跑得到相同結果」的驗收與測試都只比較確定部分。

### 離線與請求隔離

- 頁面載入、King County 的所有操作、50 Startups 的執行與操作、本機檔案載入：零對外請求。
- 自訂 URL：使用者提交後對該 URL 一次 GET；此外沒有其他請求。
- 靜態掃描的既有規則不變，唯一新增：**只有探索載入模組這一個檔案允許出現 `fetch(`**；V1 的 dashboard 腳本、核心模組、引擎模組與其他檔案照舊禁止網路 API。
- 載入模組以可注入的方式取得 `fetch`，使 Node 行為測試能以 mock 驗證（見 Testing Decisions）。

### 通用 Python 參照

- 新增一個通用（不綁 King County 欄位）的 Python 參照實作，接受任意表格與目標欄，依本 Spec 的載入契約、前處理邊界、切分、方法、有效性、指標、PI 與診斷規則產生與 `ExploratoryResult` 同概念的參照結果。
- 它**重用**正式分析套件中已 group-generic 的數學準則（RSS 步驟、`sd(X_g β_g)`、LARS entry 與 tie 規則、PI 公式、指標），不重寫第二套；需要 King County 專屬輸入的函式不被重用。它不依賴任何 JS 結果。
- 只用於 fixture 與一致性測試；正式分析路徑、notebook、報告數字都不 import 它。

### 文件、README、報告與打包

- README：功能說明；「作業要求對應」表加兩列（+1、+2 → 操作方式與驗收位置）；探索模式的限制與揭露；50 Startups 來源與授權；特徵數條件由「10–20」改為「>13」。
- 報告：新增「探索模式」一章（加分功能、分析方法、與正式分析的差異——目標尺度、切分、Lasso 退化語義、無派生規則——限制與洩漏揭露）；正式分析各章數字不變；建置流程不變。報告在 V2 的 SRC-4 下屬 optional，仍照 V1 交付。
- ACCEPTANCE.md：既有條目保留；新增 V2 條目（Brief V2 §8 的 1～9 與 2a，加上 acceptor 的三條：三向切換 King County→50 Startups→自訂→King County；URL 失敗後改以本機 CSV 成功；探索執行或失敗後 King County 內容與數值不變）。
- 打包：新增的靜態資源隨既有的追蹤項目進入 ZIP；ZIP 與 Pages 的 dashboard 內容相同；記錄 sha256 與清單。
- 單元 `.gitignore` 不需改；學號規則（BR-03）不變。

## Testing Decisions

### 什麼是好的測試

- 只測外部可觀察的行為與契約：給定輸入（CSV 文字、目標、seed）→ 結果契約的值與狀態；不測內部函式的呼叫方式。
- 參照值由 Python 獨立產生，測試時在 pytest 內即時產生並寫到暫存路徑，不追蹤 fixture 檔案（沿用 V1 的 fixture 慣例）。
- 失敗語義逐條有案例：每個拒絕原因、每個候選狀態、退化與相依情境各至少一個案例。
- 容忍度先固定定義再比較：係數、PI、指標為相對 1e-6（沿用 V1 的 JS 容忍度決定）；Lasso entry alpha 相對 1e-6；entry alpha 相差超過容忍度的 group 順序必須相同，容忍度內視為 tie 依 canonical 規則。

### 主 seam：Exploratory run 結果契約（Node 對 Python 參照）

- 資料：(a) 50 Startups；(b) synthetic 非退化（固定 seed 產生，entry 分明、含數值與類別欄）；(c) synthetic 退化（含完全共線的欄、一欄為另兩欄之和、相等 entry）；(d) 小型邊界案例（恰好 20 列、單一類別欄、全部數值）。
- 驗證：欄位型態與（以訓練列決定的）狀態；切分與 fold 指派相同；每個候選的狀態與原因相同；`VALID` 候選的各 fold 子集、各 fold 指標、CV 平均與標準差、canonical 子集、係數、s²、df_resid；winners（含平手案例：同 RMSE 取較小 k、整體平手依方法順序）；test 指標、逐筆 PI 與 covered，且 test 值只對 winner 存在；相依欄位組與 group 映射；Lasso 的 entry alpha 與順序（非退化）或退化步與其後候選狀態（退化）。
- **聚合與凍結**（SR-V2-02）：以可手算的小型案例驗證 CV 指標等於各 fold 指標的算術平均；驗證改動 test 列的目標值不改變任何候選的狀態、CV 指標、canonical 子集與 winner（只改變 test 指標與逐筆結果）。
- **可重現性**（SR-V2-04）：同一輸入執行兩次，確定部分逐值相同；以 URL 文字、檔案文字與內建文字三種入口餵同一內容，確定部分相同；非確定部分（計時）允許不同。
- **取消與失敗**（SR-V2-03）：注入在第 n 個候選後發出的取消請求，結果為 `CANCELLED`、沒有 `candidates`／`winners`／`test`；注入某方法在某候選拋出例外，該方法為 `FAILED`、其他方法照常完成且 winner 只從其他方法選；預算估計超出時該方法為 `SKIPPED_RESOURCE_LIMIT` 且未被執行（以計數驗證）。
- **50 Startups 全部 k 有效**：由 (a) 的候選狀態證明（Python 參照與 JS 結果都列出每個候選的狀態）；若不成立，依 A-1 分析並如實記錄，不改契約。
- **King County 一致性**：通用參照套在正式分析已前處理的 King County 訓練表（以正式分析的 Feature group 與 ln(price) 作為輸入）必須重現正式分析的四條 canonical 路徑與 All-in；這證明準則共用，**不取代** (a)～(d) 的獨立驗證。
- 契約不變量以通用檢查函式對每份結果驗證。
- 前例：V1 的 Node 核心測試與 pytest 驅動 Node 的方式；V1 的 synthetic fixture 產生器。

### 次 seam：載入契約與請求隔離（Node）

- 載入：每個拒絕原因一個案例；BOM、引號、空白、科學記號、負數、空儲存格；缺值刪列與不足 20 列；目標預設與指定；重複欄名。載入結果**不含**任何欄位的保留／排除狀態（SR-V2-01）。
- **三層邊界**（SR-V2-01）：
  - 第二層只看訓練列：層級數邊界 20／21 以訓練列計算——一個欄在訓練列上 20 個層級、在 test 列另有第 21 個層級時仍保留；一個欄只在 test 列上有變化、在訓練列上為常數時被排除；反之只在 test 列為常數的欄保留。改動 test 列（值、層級、常數化）不改變 group 清單與 canonical 順序；改動訓練列會改變。
  - 第三層只看該 fold 的訓練列：改動某 fold 驗證列的值（含加入新層級）不改變該 fold 的層級清單、基準、標準化參數與子集序列；改動該 fold 的訓練列會改變；其他 fold 不受影響。沿用 V1「選擇邊界」測試的形式。
  - canonical 只看整個訓練集：改動 test 列不改變 canonical 子集、fit 與即時預測器的層級下拉。
- **請求隔離（mock fetch）**：以可注入的 fetch 替身驗證——初始化不發請求；選 King County 不發請求；選 50 Startups 不發請求；本機 CSV 載入不發請求；只有提交自訂 URL 時對該 URL 恰發一次 GET，不重試；fetch 失敗時回報 `URL_FETCH_FAILED` 與子原因且不再發請求。這個測試在載入契約 seam 內，不是新的 seam。

### 靜態 seam

- 離線靜態掃描：既有測試照跑；新增案例驗證「只有探索載入模組允許 `fetch(`」——在其他任何檔案出現網路 API 即為 finding。
- King County 不變：既有的正式 `model_data` 測試照跑；新增測試驗證 V1 區塊的 DOM 結構與靜態文字與基準相同（以結構快照比對，不含探索區塊）。
- 內建資料一致：JS 內嵌的 50 Startups 文字與保留的 `.csv` 內容相同，sha256 與記錄值相同。
- 既有的 dashboard 靜態測試（分層、test 數字只讀自 `model_data`、核心模組不含指標或選擇程式碼）照跑；探索引擎是獨立模組，不違反「核心模組不含選擇程式碼」的既有測試。

### 人工檢查表（ACCEPTANCE.md 的 V2 條目）

- Brief V2 §8 的 1～9 與 2a，逐條：下拉三項與 King County 逐字相同；50 Startups 離線完成（記錄時間）；老師 URL 在 Pages 上載入並與內建結果一致（內容 sha256 相同時）；檔案載入一致；各失敗訊息；探索標示；網路面板零請求與一次 GET；Node 測試通過；OV-1 與 SR-09 重做。
- acceptor 追加：King County→50 Startups→自訂→King County 的切換；URL 失敗後改以本機 CSV 成功；探索執行或失敗後 King County 內容與數值不變。
- 效能：記錄 50 Startups 與一份中型資料集的實測時間、瀏覽器、硬體；不設門檻。
- 非阻塞與取消（SR-V2-03）：在中型資料集執行中，下拉、輸入與取消按鈕可操作、進度持續更新、沒有瀏覽器「網頁沒有回應」提示；按取消後顯示「已取消」且沒有任何結果區塊；再次執行從頭開始。
- 可重現性（SR-V2-04）：同一份資料連續執行兩次，確定部分的顯示數字相同；耗時可不同。
- OV-2～OV-5 對新增的控制項與區塊照 V1 的 gate 分類執行。

## Out of Scope

- 後端、API、資料庫、Vercel；任何伺服器端計算。
- CSV 文字貼上輸入；使用者指定分組欄；目標的 log 開關或自動轉換；Exhaustive search、SelectKBest、permutation importance；資料清理工具；多目標、分類、時間序列；儲存、分享或匯出探索結果；探索結果進入正式報告的數字。
- 改變 King County 正式分析的任何數字、契約、`model_data`、結果檔、Test evaluation 紀錄或 V1 區塊。
- 重跑 notebook 或任何新的 Test evaluation。
- 新的 CI workflow、瀏覽器 E2E 框架、第五個測試 seam。
- 向老師確認「兩種 problem」的意思（acceptor 可選擇做，不是本 Spec 的工作）。
- 修改 rev 5 的 Spec、V1 票務索引、issue #59，或 root 檔案（RB-5 另議）。

## Further Notes

- **優先順序**：P0＝正式交付不變、GitHub 與 Pages 可存取；P1＝兩項加分都做完。內部目標 2026-10-31，老師截止 2026-11-04。
- **複雜度上限**：優先確保老師能操作下拉、輸入資料集、完成回歸分析並看到正確結果；任何超出此目的的能力先問「不做清單」。
- **兩個 problem 的語義差異**要在 UI 的「方法與限制」與報告的探索模式章節並列說明：目標尺度（ln(price) vs 原始）、切分（House 分組 vs 逐列）、Lasso 退化（canonical 補齊 vs `INVALID_MODEL`）、派生規則（有 vs 無）。
- **「同構」的界線**：探索結果契約與 `model_data` 共用指標定義、PI 公式、候選／winner／test 的概念與不變量；欄位名稱與巢狀結構可不同。V1 的 Node 核心測試不對探索結果執行。
- **運算預算與載入上限的數字**是實作常數，由實測決定並記錄；它們出現在 ACCEPTANCE 與 README，不出現在本 Spec。
- **治理**：本單元 governance on；進入實作時依既有 Bindings 處理，本 Spec 不新增 gate、角色或授權要求。
- **Spec Review 的處理**（acceptor 2026-10-21，CHANGES REQUESTED → rev 2）：

  | Finding | 處理 | 所在節 |
  | --- | --- | --- |
  | SR-V2-01（High）全資料常數欄與層級數判定造成洩漏 | 載入契約只做 CSV 結構檢查，不再輸出保留／排除狀態；層級數上限與常數欄排除移到「第二層：訓練集層」只用訓練列；三層邊界（結構檢查／訓練集層決定／每個 fold）各自列出能看的列；test 列讀取時點明定 | 載入契約；前處理與洩漏邊界；次 seam「三層邊界」測試 |
  | SR-V2-02（High）fold 子集、聚合、winner、canonical 與 test 的關係 | 以七點沿用 rev 5 與正式分析套件的定義：fold-internal selection、fold 指標、CV＝fold 算術平均（附 std）、canonical 子集與 fit、方法 winner 平手取較小 k、整體 winner 平手依 All-in→Forward→Backward→RFE→Lasso、凍結後才讀 test 並只對 winner 的 canonical fit 評估 | 切分與交叉驗證；主 seam「聚合與凍結」測試；`candidates` 加各 fold 子集與指標 |
  | SR-V2-03（High）資源保護、非阻塞、可終止 | 保留逐方法預算與 All-in 優先；預算只依估計量；新增非阻塞（候選邊界讓出控制權）、取消（候選邊界生效、`CANCELLED`、部分結果不呈現）、資源保護（事前估計矩陣大小、例外只讓該方法 `FAILED`、不並行第二次執行）；不指定 Worker | 候選有效性、狀態與運算預算；`run` 狀態；主 seam「取消與失敗」測試；人工檢查表 |
  | SR-V2-04（Medium）可重現性契約 | 新增「可重現性」一節：確定部分（狀態、切分、候選、winner、test、診斷）逐值相同，非確定部分（計時、進度、時間戳）不在契約；`SKIPPED_RESOURCE_LIMIT` 屬確定、`FAILED`（環境）與 `CANCELLED` 不屬可重現性對象 | 可重現性；主 seam「可重現性」測試；人工檢查表 |

- **與 Brief V2 的差異（已結案）**：rev 2 依 SR-V2-01 把「類別層級 ≤ 20」與「常數欄排除」移到切分後的訓練集層，與 Brief V2 §5.2／§5.5 原文不一致；acceptor 2026-10-21 授權對 Brief V2 做最小勘誤 **E-1**（§5.2 新增「訓練列決定的模型決策」、§5.5 處理順序改為三層；上限 20、排除原因與驗收目標不變；記於 Brief V2 §13 末）。勘誤後 Brief 與本 Spec 沒有剩餘的契約衝突。
- **下一步**：`/to-tickets`（新檔、新 issue）→ 實作。兩步都尚未授權。
