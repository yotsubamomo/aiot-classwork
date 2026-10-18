# HW2 Spec Review 與對帳紀錄（2026-10-18）

- **對象**：[`SPEC.md`](SPEC.md) rev 1（commit `3aacb54`；GitHub issue #59）。
- **來源**：acceptor 轉交的獨立審查候選 findings SR-01～SR-09。依 acceptor 指示，每項先對照已接受的 Brief（commit `dff7c55c`）、`CONTEXT.md`、Grill 決定與 Spec 查證，再分類為 CONFIRMED／PARTIALLY CONFIRMED／NOT A DEFECT，並以最小且不改變契約的方式修正。
- **執行者**：無角色主 session（self-reconciliation；不是 independent audit）。
- **結果**：rev 2 的 SPEC.md 與 issue #59 已同步。沒有任何 Brief 決定被改變；兩項需要 acceptor 確認（SR-06 的 Brief 編輯、SR-09 的門檻數值）。

## 審查表

| ID | 判定 | 嚴重度 | 證據 | 修正 | Brief／Spec 影響 | 需要的授權 | 殘餘風險 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SR-01 選擇與 CV 邊界 | **PARTIALLY CONFIRMED** | Blocking | Spec rev 1「分割與 CV」寫「每個 fold 內的…特徵選擇…只用該 fold 的訓練列」，但「`methods`」區段只匯出單一 groups 與「整個 training set 上重擬合的係數」，沒有說子集是每 fold 重算還是全 training 算一次；若是後者，驗證 fold 參與了子集選擇再被用來評估。Brief Q13 選 (a)「固定 split、training 內 CV、各方法以 CV RMSE 選 k」，並把 nested 留給 Spec；Q4／Q33 要求選擇只用 training | 明寫 **fold-internal selection**：每 fold 在自己的訓練列重算 k=1…18 的子集再評估；驗證列不參與選擇。另定義 **canonical subset**（整個 training set 上算的子集）供 dashboard／預測器／test 使用；契約記錄各 fold 子集與 `folds_agree`。加入選擇偏誤陳述（CV winner 的 CV 分數樂觀偏誤，test 是獨立估計） | Spec：分割與 CV、特徵選擇、契約 `methods`、測試。Brief：不變（在 Q13(a)、Q4、Q33 的邊界內；不是 Brief 延後的 inner-CV nested 設計） | 無。成本影響（路徑計算 ×6）在 Q34 的量測義務內，已於 Further Notes 告知 | 路徑方法的執行時間上升；同一 k 各 fold 子集不同時，報告要解釋 CV 指標評的是程序 |
| SR-02 `model_data` 可重建性 | **CONFIRMED** | Blocking | Spec rev 1 `test` 只有 actual／predicted／lower／upper／covered；Node test 卻要求「對 test 每一筆重算點預測、lower、upper」——沒有原始輸入就只能複製 `predicted`，不是獨立重算 | 新增 `test_inputs`（全部 test 交易的原始 18 個 source feature、列識別、actual）與 `preprocess`（基準日、整修規則、group→欄位對應、canonical order）；不變量改為「只用 `test_inputs`＋`preprocess`＋`fit` 可獨立重算」；pytest 以 numpy 重建設計列、不呼叫匯出程式的預測函式；Node test 從原始值經 dashboard 自己的前處理重算 | Spec：契約、測試。Brief：不變（Q23 本來就要求一致性檢查涵蓋前處理） | 無 | 契約檔變大（約 4,300 列 × 20 欄）；仍遠小於 Pages 限制 |
| SR-03 Ridge／Lasso test schema | **PARTIALLY CONFIRMED** | High | Spec rev 1 的不變量寫「加 Ridge／Lasso 的指標、不含逐筆」，但 `test` 的欄位定義沒有區分，測試也沒有檢查 | `test` 每筆加 `kind`：`ols_subset`（必有 PI、coverage、逐筆）／`metric_only`（Ridge、Lasso；必無）；不變量與 pytest 檢查 kind 與欄位的一致；Node test 對 `metric_only` 不計算 PI | Spec：契約、測試。Brief：不變（Q31） | 無 | 無 |
| SR-04 fold 內秩不足 | **CONFIRMED** | High | Spec rev 1「秩不足時報錯停止」會讓任一 (方法, k, fold) 的常數欄中止整個實驗；也沒有把「fold 缺少某 zipcode 類別」（合法 encoding）與真正的秩不足分開。Brief Q16 要求以實際秩推論、不臨時刪欄；Q34 禁止縮小範圍 | 三類語義：(1) 合法 encoding（fold 訓練列缺類別 → 該欄不存在，未見→基準，記錄筆數）；(2) 無效候選（某 (方法, k, fold) 秩不足 → 該 fold 無效、該 (方法, k) `status=invalid`、不參與 winner、明確標示；不跳過 group）；(3) 實驗層級失敗（All-in 或任何 canonical subset 在整個 training set 秩不足、或某方法沒有有效 k → 停止並回報）。測試各加案例 | Spec：指標與推論、契約 `status`、dashboard 標示、測試。Brief：不變 | 無 | 若實際資料出現大量 invalid，比較表會有洞；這時依 (3) 或 Q34 回報 |
| SR-05 指標來源 | **PARTIALLY CONFIRMED** | High | Spec rev 1 把 CV 的 USD 指標、全訓練集 log 尺度 R²／Adjusted R² 與係數混在同一個 `methods` 項目；dashboard 只標 KPI 為「訓練 CV」，係數表沒有來源標示。Brief Q29 已定尺度規則，但呈現上可能被誤讀 | `methods` 項目分 `cv`（USD）／`fit`（整個 training set，log 尺度統計與係數）／winner 旗標；`test` 另置；dashboard 的 KPI 標「訓練 CV（USD）」、係數表標「全訓練集擬合，R²／Adjusted R² 為 log 尺度」、test 區塊標「Test 評估（USD）」；人工檢查表加來源標示項 | Spec：契約、dashboard、檢查表。Brief：不變 | 無 | 無 |
| SR-06 All-in 用語 | **CONFIRMED** | Medium | Spec rev 1 的 Solution、US-5、US-52 寫「五種特徵選擇方法」「五個方法的 k 路徑」，與 Brief BR-02 的定義（All-in 是單一模型）不一致。Brief §1 也有同一句 | Spec 統一為「四種有 k 路徑的特徵選擇方法＋單一 All-in baseline」；CONTEXT.md 的 All-in baseline 詞條已存在 | Spec：三處用語。**Brief §1 有同樣的編輯性問題，未動** | **Acceptor 決定**是否同步修 Brief §1（編輯性，不改決定） | 無 |
| SR-07 未見 zipcode | **PARTIALLY CONFIRMED** | Medium | Spec rev 1 只寫「未見類別為基準」；沒有說下拉選單的來源、使用者看到什麼、test 中有多少筆 | 下拉只列當前模型 `fit` 的類別＋基準（標明）；不在清單的輸入以基準計算並顯示警告文字；契約記錄 test 內被編為基準的未見 zipcode 筆數；Node 前處理案例加「回報警告旗標」 | Spec：dashboard、契約、測試、檢查表。Brief：不變（Q16、Q32） | 無 | 無 |
| SR-08 涵蓋率不確定性 | **CONFIRMED** | Medium | Spec rev 1 把 1.96√(p(1−p)/n) 寫成「抽樣不確定性」，沒有說明它假設獨立；test 內同一房屋的重複交易相依 | 標明為二項近似、假設獨立、實際略大；契約與報告給出 test 的房屋數與重複交易筆數；與「不宣稱保證 95%」一起說明 | Spec：預測區間、契約 `test_inputs`、pytest。Brief：不變（Q18「抽樣不確定性」未指定方法） | 無 | 只是說明，不改公式；若 acceptor 要 cluster-robust 的估計，屬新增需求 |
| SR-09 UI 效能驗收 | **PARTIALLY CONFIRMED** | Medium | Q43 的「可讀且可操作、不嚴重遮蔽或卡頓」是驗收意圖，但 Spec rev 1 沒有可觀察的檢查；Q43 第 5 點禁止限制實作技術 | 加入五條可觀察檢查 (a)～(e)：3 秒首次繪製、1 秒互動更新且無「沒有回應」提示、預設視圖可分辨、十倍價格區間內可分辨個別線段、游標可讀取單筆；不指定技術 | Spec：dashboard、檢查表。Brief：不變 | **Acceptor 確認門檻數值**（起草者提議） | 參考環境是 acceptor 的電腦，其他機器表現可能不同 |

## 第二輪：acceptor 決定與 SR-10～SR-12（2026-10-18）

**Acceptor 決定**：SR-06 ACCEPTED（Brief §1 編輯性修正已套用）；SR-09 ACCEPTED WITH CLARIFICATION（1 秒適用於方法／k 切換、縮放、平移；定義量測起訖；記錄瀏覽器、硬體、資料筆數、量測方式；不得以抽樣或聚合達標；線段可辨識性以縮放或游標驗收，不要求高密度區域全部不重疊）——已寫入 Spec rev 3 的 dashboard 一節 (a)～(g)。

| ID | 判定 | 嚴重度 | 證據 | 修正 | Brief／Spec 影響 | 需要的授權 | 殘餘風險 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SR-10 canonical subset 秩不足 | **CONFIRMED** | High | rev 2「實驗層級失敗」含「任何方法的 canonical subset 在整個 training set 上秩不足」，與同節「無效候選不阻止其他候選」的語義衝突：一個非 winner 的 (方法, k) 就能中止全部實驗 | canonical fit 秩不足 → 該 (方法, k) `invalid`（`canonical_rank_deficient`），沒有 `fit`、無預測、不參與 winner；**有效候選**＝CV 全 fold 有效且 canonical fit 有效；winner 只在有效候選中選。停止條件縮為：All-in 秩不足、任一方法沒有有效候選、整體 winner 無法決定；停止時列出全部 invalid 與原因，不刪 group。測試加對應案例 | Spec：指標與推論、測試。Brief：不變（Q16、Q34） | 無 | 無 |
| SR-11 p-value backward 的 CV 洩漏 | **CONFIRMED** | Medium | rev 2 在整個 training set 上做一次消去，再用同一組 fold 算 CV：每個驗證 fold 都參與了子集的選擇，CV 指標樂觀 | 改為 fold-internal（每 fold 訓練列消去、驗證列評估），另在整個 training set 上得 canonical subset 供顯示；仍是單一子集、無 k 路徑、只作對照、不進 winner、不評估 test | Spec：方法、測試。**Brief §5 編輯**：「做一次」→「產生單一子集、不進 k 路徑（選擇邊界與正式方法相同，由 Spec 定）」——「做一次」原意是單一子集，不是單次計算；Q11 的決定（F 為講義方法對照、不進正式比較）不變 | Acceptor 已允許必要的 Brief 編輯性文字；已記入 Brief §14 | 計算 ×6（在 Q34 義務內） |
| SR-12 涵蓋率不確定性的方向宣稱 | **CONFIRMED** | Medium | rev 2 寫「實際不確定性略大於此近似」；群組相依只說明獨立假設不成立，方向與幅度未經估計 | 改為：涵蓋事件不保證獨立，近似的準確度未經估計；報告不陳述方向或幅度，只說明假設並列出房屋數與重複交易筆數；群組感知估計不在範圍內 | Spec：預測區間。Brief：不變（Q18） | 無 | 無 |

## 修正後的新矛盾檢查

- SR-01 與 SR-02：canonical subset 是 test 評估與 JS 重算的對象，`test_inputs`＋`fit` 足以重算；fold 子集只進比較資料，不進預測器。一致。
- SR-01 與 Brief Q20：CV winner 仍以 CV RMSE 選，test 只對授權模型；新增的偏誤陳述與 Q20「test 排名不同不換模型」相容。
- SR-03 與 BR-01：`metric_only` 模型不在 test 區塊的逐筆圖中，Ridge／Lasso 的 test 指標只出現在比較表；與 Q31（無 PI、無即時預測）一致。
- SR-04 與 Q34：`invalid` 不縮小範圍，只標示；實驗層級失敗才停止。一致。
- SR-05 與 Q29：Adjusted R² 仍只在 log 尺度、只對 OLS；USD 只有 R²。一致。
- SR-07 與 Q16：encoding 設計不變，只補使用者可見行為。一致。
- SR-08 與 Q18：公式不變，只補假設說明與輔助數字。一致。

- SR-10 與 SR-04：三類語義保留；只把 canonical 秩不足從「實驗層級」移到「無效候選」，停止條件改以 All-in、方法有效性與整體 winner 可決定為準。一致。
- SR-11 與 Q11／BR-02：p-value backward 仍不進正式比較；fold-internal 使它的 CV 指標與正式方法可比，但它沒有 k 路徑也不評估 test。一致。
- SR-12 與 SR-08：公式不變，只刪去方向宣稱。一致。
- SR-09 (g) 與 Q43 第 1 條：相同要求，重申於效能驗收內。一致。

## Final Spec Review Verdict（2026-10-18）

- Blocking：SR-01、SR-02 — **CLOSED**（rev 2）。
- High：SR-03、SR-04、SR-05 — **CLOSED**（rev 2）；SR-10 — **CLOSED**（rev 3）。
- Medium：SR-06、SR-07、SR-08、SR-09 — **CLOSED**（rev 2；SR-06、SR-09 於 rev 3 依 acceptor 決定定案）；SR-11、SR-12 — **CLOSED**（rev 3）。
- 沒有新的 Blocking／High finding。殘餘風險只有計算時間（Q34 已有義務）與參考環境的機器差異（SR-09 已要求記錄）。
- **Verdict：Spec rev 3 可進入下一階段（`/ui-ux-pro-max` wireframe），待 acceptor 指示。** 本紀錄是起草者的 self-reconciliation，不是 independent audit。

## 未改變的事項

- Brief 的所有決定（Q1–Q43、BR-01～BR-04）與 Outcome Contract 接受紀錄。
- 治理規則、Bindings、Issues #50–#56。
- 沒有產生 Tickets、wireframe 或實作。
