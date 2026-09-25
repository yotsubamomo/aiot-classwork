# Decision record — AC-V2-01「選縣往返」的 Ticket 分配（R-1；`home_work_01/`）

- **紀錄類型**：Design Authority decision record（治理 §3.6-A：在不改變任何 accepted 語義的前提下裁決；治理 §2.4「derived contract 的 derivation 與 boundary determination」；治理 §5.3 第 2 類「不改變 accepted 語義的 derived contract 修訂」，須記錄對進行中工作、dependencies 與既有 evidence 的影響）。本紀錄同時是 V2 Ticket derivation 的**分配修訂**：[`derivation-SPEC-V2.md`](derivation-SPEC-V2.md) §15.2、§15.3 與 §14 以參照引用本紀錄。
- **編號**：**DV-20**（延續 `derivation-SPEC-V2.md` §3.2 的 DV-1～DV-19）
- **日期**：2026-09-26
- **來源**：Issue #36 cycle 1 R1 audit record [`../audit/issue-36-c1-r1.md`](../audit/issue-36-c1-r1.md) §4 關切 1／§8 routing signal **R-1**（治理 §4.2：契約不足是 routing signal，不是 blocking finding，不觸發 promotion）；由 Orchestrator 依治理 §2.4 派工，run record [`../run/run-20260925-hw01-v2-formal.md`](../run/run-20260925-hw01-v2-formal.md)。
- **相關契約**：V2 Outcome Contract（ACCEPTED 2026-09-25，normative candidate `69c5a04`）§2.5 **S-3**「切換保留使用者目前地理脈絡（除非某模式確實需要不同的有效視野）」、**S-4** 下鑽、§3 **AB-V2-1**「切換保留地理脈絡（S-3）」、**AB-V2-6**；SPEC-V2 **v2.2** R-V2-MODE-4、**R-V2-MODE-5(a)(c)**、R-V2-DD-4、**R-V2-DD-5**、R-V2-DD-8、R-V2-DD-9(a)、**AC-V2-01**、AC-V2-10、AC-V2-12、§3 開頭「驗證視野」定義、§6.1、§6.2、§6.4；derivation record §3.2 **DV-8**、§15.2、§15.3（AC-V2-01 → #36）、TB-V2-1、**TB-V2-4**；Issue **#38** 與 **#41** body（DA 於 2026-09-26 以 `gh issue view` 讀取）；治理 §1.2、§3.4、§3.8、§4.1、§4.2、§4.7、§5.3。
- **參考 subject**：branch `home_work_01-v2-implementation` HEAD `760027206c53feb076962cecd53f0d0017e76e6b`（#36 已結案，code anchor `f63ebb1`）；`static/app.js:83`（`nowView`）、`:150`（`selectedStationId`）、`:265-277`（`setMode`）、`:346-352`（`restoreNowView`）只作機制 grounding，不作為設計依據。
- **執行角色**：`gov-design-authority`（Bindings §3.1 `design_authority`；binding 核對由派工者依 Bindings §3.4 記入 run record）。
- **效力**：自本紀錄寫入起，Issue #38 的驗證分配依第 4 節擴充；SPEC-V2 文字不變（仍 v2.2）；#36 的分配、evidence 與結案不變、不重開；Spec Integration Audit 的義務不變。本紀錄不修改任何實作或測試。

## 1. 問題

AC-V2-01 的 PASS 條件含一句：「在 Now mode **選一縣**並縮放後往返 Forecast，回到 Now 時**選縣**與視野恢復」（FAIL 例：「往返後選縣丟失」）。它 derive 自 R-V2-MODE-5(a)「Now mode 的選取狀態（**選縣**、選測站）與視野 MUST 在 Now → Forecast → Now 的往返後恢復」與 (c)「回到 Now mode 時 MUST 恢復離開時的 Now 視野」（DV-8；OC S-3）。

選縣本身（縣界互動圖層 R-V2-DD-4、選縣與 County 脈絡 R-V2-DD-5、AC-V2-10、AC-V2-12）只在 **#38** 實作，而 #38 依賴 #36。因此在 #36 的 subject 上，這句「選一縣」的字面 oracle **無法執行**；#36 R1 以「選測站＋縮放／平移」驗證了往返恢復機制並對可觀察部分判 PASS。但 derivation record §15.3 把 AC-V2-01 **只**分配給 #36；#38 的分配（AC-V2-10、12、16 部分、20 部分、23 部分）與 #41 的分配（03 preview、16 最終、17(c)(e)、20 完整、21、22）都不含 AC-V2-01；§15.3「R-V2 群組覆蓋」把 MODE 整組給 #36。於是縣選取存在之後，「選縣往返」在 Ticket 層沒有 owner，只剩 Spec Integration Audit（Spec §6.4；治理 §4.7）兜底。

需裁決：由哪張 Ticket 在縣選取存在後重驗 AC-V2-01 的選縣往返（候選 #38），或確認 Spec Integration Audit 是正確且充分的 owner。

## 2. 事實（依原始契約與紀錄，不採用 Executor／Reviewer 的結論）

| # | 事實 | 證據 |
| --- | --- | --- |
| E-1 | AC-V2-01 的 PASS 條件逐字含「在 Now mode 選一縣並縮放後往返 Forecast，回到 Now 時選縣與視野恢復」；FAIL 例含「往返後選縣丟失」；證據類別「瀏覽器驗收＋截圖（桌機、375：Now 預設、Forecast mode）；AC-17／AC-18 重驗清單；DOM 檢查」。對應 AB-V2-1；R-V2-MODE-1、2、3、5。 | `SPEC-V2.md:234` |
| E-2 | R-V2-MODE-5(a) 把「選縣、選測站」與視野並列為往返後 MUST 恢復的 Now 狀態；(c) 回到 Now 時恢復**離開時**的 Now 視野。來源 S-3、P-28、DV-8。 | `SPEC-V2.md:118`；derivation §3.2 DV-8 |
| E-3 | 選縣的實作與驗證條款——R-V2-DD-4（縣界互動圖層）、R-V2-DD-5（選縣與 County 脈絡；(a) 選縣後調整視野）、R-V2-DD-8（Back to Taiwan 清除選縣）、R-V2-DD-9(a)（不經地圖的鍵盤選縣路徑）、AC-V2-10、AC-V2-12——全部分配給 #38；#38 blocked by #36。 | derivation §15.2、§15.3；Issue #38 body「What to build」「Acceptance criteria」「Blocked by」 |
| E-4 | derivation §15.3 AC 表：`01 → #36`（唯一 owner）；#38 的 AC 分配為 10、12、16（縣界圖層）、20（範圍）、23（Back to Taiwan）；#41 為 03（preview）、16（最終 log）、17(c)(e)、20（完整）、21、22。「R-V2 群組覆蓋」：MODE → #36（MODE-6(c) 另 #37）。#38 body 的 Traceability 列 R-V2-MODE-4，不列 R-V2-MODE-5。 | derivation §15.2、§15.3；Issue #38、#41 body |
| E-5 | #36 R1（CLOSURE）：AC-V2-01 對 #36 subject 可觀察的全部部分 PASS；往返機制為模組層級狀態 `nowView`（離開 Now 時保存 center／zoom）與 `selectedStationId`（跨模式保留），`restoreNowView` 以 `setView` 恢復；Reviewer 以兩種獨立操作驗證選測站＋視野往返恢復。R1 判定「這不是 #36 的實作缺陷」，並把分配問題以 R-1 route DA；交接 #38 一句「#38 加入縣選取時須把選縣狀態納入同一往返保存（R-V2-MODE-5(a)）」。 | `issue-36-c1-r1.md` §2 AC-V2-01 列、§4 關切 1、§8；`app.js:83,150,265-277,346-352`（DA 自讀） |
| E-6 | Spec §6.4：Spec Integration Audit 對整合 subject 核「AC-V2-01～23 全部」；治理 §4.7：Spec-level AC coverage——每條 Spec AC 有對應 evidence 與 PASS／FAIL；MUST NOT 重開已閉合的 Ticket finding，除非有新的 integration-level evidence；任何人不得豁免此 audit。 | `SPEC-V2.md:362`；治理 §4.7 |
| E-7 | 治理 §4.1：Formal 下每個 work item 的 independent audit MUST 執行；§3.8：review、verification 與結案版本 MUST 可對應，最終產物須受相應 verification／review coverage；「單張 Ticket 的 PASS 不自動證明整合產物符合跨 Ticket invariants」。§3.4：Tickets MUST 引用有效 Spec 的 verification contract，不得自行重新定義 AC。 | 治理 §3.4、§3.8、§4.1 |
| E-8 | derivation §15.4 TB-V2-4（比例性）：「每票只擁有與其切片實質相關的 AC／INV 證據」；§15.5 第 1 項宣稱「每條 AC-V2-01～23 有 owner」PASS——就 AC-V2-01 的選縣往返而言，owner 只在 #36，而 #36 依構造無法執行它。 | derivation §15.4、§15.5 |
| E-9 | OC S-3 與 AB-V2-1 的文字（E-2 引用的上位語義）在本裁決中不需改動，也沒有任何一方主張改動。 | OC-V2 §2.5 S-3、§3 AB-V2-1 |

## 3. 兩個選項與對照

- **(A) 把 AC-V2-01 的「選縣往返」部分（連同 R-V2-MODE-5(a) 的選縣部分）分配給 #38**，作為 Ticket 層 owner；Spec Integration Audit 仍對整個 AC-V2-01 作 Spec 層核對。
- **(B) 只由 Spec Integration Audit 承接**：不改任何 Ticket 分配。

對照契約與治理：

1. **Owner 跟著狀態走。** 選縣狀態由 #38 引入；R-V2-MODE-5(a) 逐字點名「選縣」必須在往返後恢復。治理 §4.1 要求每個 work item 的 independent audit MUST 執行，§3.8 要求 verification 與結案版本可對應——引入該狀態的 Ticket，其 audit 必須能觀察到該狀態是否在往返後存活。選 (B) 時，#38 可能帶著 R-V2-MODE-5(a) 的違反結案，而該違反要到 #39、#40、#41 全部結案後才在 Spec Integration Audit 首次被觀察到：那時它是對整合 subject 的 integration-level finding，修正是晚期 rework，且可能牽動 #39（圍欄儀器）與 #40 的再驗證——與在 #38 上做一次瀏覽器往返相比，明顯不成比例。
2. **§4.7 的角色是 Spec 層 coverage 與整合，不是單張 Ticket 行為的首次驗證點。** §3.8 說單張 Ticket 的 PASS 不能代替整合驗證；反過來，整合驗證也不是讓單張 Ticket 的自身行為第一次被看見的地方。§4.7 還規定 Spec Integration Audit MUST NOT 重開已閉合的 Ticket finding——如果 #38 的 audit 從未觀察選縣往返，就不會有可重開的 finding，只有一個從未被 Ticket 層驗證的 Spec 條款；這正是 §15.3 覆蓋矩陣應避免的狀態。
3. **比例性（TB-V2-4）成立。** 選縣往返與 #38 的切片實質相關（#38 本來就必須做 AC-V2-10／12 的瀏覽器驗收，往返只是在同一走查裡多切兩次模式）；不要求 #38 重做 AC-V2-01 的其餘部分（載入即 Now、切換控制、AC-17／AC-18 重驗、進入 Forecast 六標記可見、選測站往返），那些已由 #36 的結案 evidence 承接。
4. **(B) 會讓 derivation record 自身留下 coverage 缺口。** E-4／E-8：R-V2-MODE-5(a) 的選縣部分在 §15.3 沒有實作責任票，AC-V2-01 的選縣往返沒有可執行它的 Ticket owner；§15.5 第 1 項的「每條 AC 有 owner」對此句而言只是形式上成立。修正它是 Ticket derivation 的修訂（治理 §5.3 第 2 類），屬 DA 權責。
5. **#36 沒有缺陷、不重開。** 該句在 #36 subject 上無法執行是垂直切片與依賴圖（#38 依賴 #36）的必然結果，不是 #36 的實作或驗證缺失；#36 R1 對可觀察部分的 PASS 與 CLOSURE 維持。

**未採用 (B) 的理由**：它只保證「最終會被看到」，不保證「在引入它的變更被審查時被看到」；治理 §4.1／§3.8 要求後者。**未採用的第三種做法**：把整個 AC-V2-01 改分配給 #38 或 #41 重做——違反 TB-V2-4 比例性，且會讓 #36 已結案的 evidence 被無謂重複。

## 4. 裁決（DV-20）

1. **Issue #38 是 AC-V2-01「選縣往返」部分的 Ticket 層 owner**，同時是 **R-V2-MODE-5(a) 選縣部分**的實作責任票。#38 的驗證分配依第 4.1 節擴充。
2. **Spec Integration Audit 仍是 AC-V2-01 整條的 Spec 層 owner**（Spec §6.4；治理 §4.7），對整合後的最終 subject 核對 AC-V2-01 全部（含 #39 圍欄儀器與 #40 可能的 CRS 變更之後的往返行為）。此義務不變、不被豁免；但它**單獨不足以**作為 Ticket 層 owner（第 3 節第 1、2 點）。
3. **#36 的分配、evidence 與結案不變。** #36 R1 的 R-1 由本紀錄解決；Reviewer 不需補記。#36 對 AC-V2-01 的義務範圍確認為「#36 subject 上可觀察的全部部分」。
4. **#39、#40 不新增分配。** 兩票不引入新的選取狀態；R-V2-MODE-5 作為 Spec 條款對整合產品仍然有效，若兩票的變更（圍欄儀器、resize 路徑、CRS）破壞往返恢復，屬其 Ticket audit 可提出的 regression finding 或 Spec Integration Audit 的整合 finding，不需事先分配。
5. **#41 不新增分配。** #41 既有的 R-V2-DOC-3／AC-V2-21(14) 義務（V2 驗收文件逐條對應 AC-V2-01～23、以引用各票證據彙整）自然涵蓋：AC-V2-01 的證據引用 #36 R1／worklog（可觀察部分）與 #38 R1／worklog（選縣往返部分）。
6. **其他一律不變**：AC-V2-01 的文字、PASS 條件、FAIL 例、證據類別；R-V2-MODE-5；#38 的「What to build」；沒有新增任何 R／AC／INV／oracle／截圖集合。

### 4.1 #38 追加的驗證分配（逐字可引用；Orchestrator 於 #38 派工與 ticket 索引引用本節）

> **AC-V2-01（選縣往返部分；decision DV-20）**——在 #38 的 subject 上：Now mode 下選取一個縣（路徑屬 HOW：縣界圖層點選或 R-V2-DD-9(a) 的不經地圖鍵盤路徑皆可），之後改變縮放，使視野不同於 R-V2-DD-5(a) 選縣時套用的縣視野；切換到 Forecast mode；再切回 Now mode。**PASS**：回到 Now mode 時 (i) 該縣仍為選取狀態，County 脈絡（R-V2-DD-5(b)）仍顯示同一縣；(ii) 視野等於離開 Now mode 時的視野（R-V2-MODE-5(c)「恢復離開時的 Now 視野」——不是重新套用 DD-5(a) 的縣視野，也不是初始視野）；(iii) 若離開前同時選了該縣內的測站，測站選取與詳情亦恢復（R-V2-MODE-5(a)「選縣、選測站」）。**FAIL 例**（Spec 原文）：往返後選縣丟失。**證據**（依 AC-V2-01 證據欄，不新增類別）：瀏覽器驗收紀錄——離開前與返回後的視野讀數（中心／zoom）對照、選取狀態對照；截圖至少一張（桌機，回到 Now mode 後、含 County 脈絡）；於 Spec §3 定義的兩個驗證視野（桌機 1280、375）各執行一次，375 以走查紀錄與讀數為證即可（§6.2 的必要截圖集合不變）。Executor self-verification 記入 `worklog/issue-38.md`；**#38 R1 Reviewer 獨立重做**。AC-V2-01 的其餘部分（載入即 Now、切換控制、AC-17／AC-18 重驗、進入 Forecast 六標記可見、選測站往返）已由 #36 結案 evidence 承接，#38 不重做；#38 R1 MAY 順帶抽驗其未被 #38 的變更破壞。
>
> **R-V2-MODE-5(a)（選縣部分）**——#38 的實作 MUST 讓選縣狀態納入 Now → Forecast → Now 的往返保存（與 #36 已建立的視野／選測站保存為同一機制或等價機制；機制屬 HOW）。

上段只引用 SPEC-V2 v2.2 既有條款並限定 #38 承接的部分（TB-V2-1 的「範圍說明」形式）；(ii) 括號內是對 R-V2-MODE-5(c) 既有文字的引用與釐清（既有來源只有一種合理解讀：離開時的視野），不是新的 oracle。

## 5. 是否改變 accepted 語義：**否**

- **Outcome Contract**：S-3「切換保留使用者目前地理脈絡」、S-4、AB-V2-1「切換保留地理脈絡」、AB-V2-6 的文字與語義不變；選縣往返是 S-3 與 S-4 兩個已接受 outcome 的交集，早已在 acceptance boundary 內（AB-V2-1 與 AB-V2-6 皆分配給 SPEC-V2，derivation §4）。
- **Derived contract**：SPEC-V2 v2.2 文字不變；沒有新增、刪除或弱化任何 R／AC／INV／oracle／證據類別；AC-V2-01 的 PASS 條件與 FAIL 例逐字維持。
- **變更性質**：只修正 Ticket 的驗證分配與實作責任分配（治理 §5.3 第 2 類；與 §14「Tickets（V2）依賴圖修正」同類）。不改 #38 的「What to build」（選縣本來就是 #38 的範圍；「選縣必須在往返後存活」是 R-V2-MODE-5(a) 對整合產品既有的 MUST）。
- **Boundary determination**：本裁決所涉的 derived-contract 修訂在 V2 Outcome Contract boundary 內；**不需 acceptor**；沒有 fail-closed 路徑。

## 6. 受影響 work items 與 evidence

| 對象 | 影響 |
| --- | --- |
| **#36**（已結案） | 無。分配、evidence、CLOSURE 不變；R1 的 R-1 由本紀錄解決。 |
| **#38**（待執行；READY） | 驗證分配擴充（第 4.1 節）；實作責任加 R-V2-MODE-5(a) 選縣部分。Ticket body 的修改與派工由 Orchestrator 執行（第 7 節）。#38 的 R1 audit record 須對第 4.1 節逐項 PASS／FAIL。 |
| **#39、#40**（待執行） | 不新增分配（第 4 節第 4 點）。 |
| **#41**（待執行） | 不新增分配；既有 R-V2-DOC-3／AC-V2-21(14) 的對照把 AC-V2-01 引用到 #36 與 #38 兩處 evidence（第 4 節第 5 點）。 |
| **Spec Integration Audit** | 義務不變（Spec §6.4；治理 §4.7）；核對 AC-V2-01 時預期在 #36 R1 與 #38 R1 兩份 record 找到 Ticket 層 evidence。 |
| **derivation-SPEC-V2.md** | §15.2 #38 列、§15.3 AC 表 01 列、§15.3「R-V2 群組覆蓋」MODE 列與 §14 修訂紀錄依本紀錄同步（DA 於本次一併以最小修改更新；只加不減）。 |
| **`doc/ticket/tickets-v2.md`** | 「實作過程中的調整」段由 Orchestrator 補一列引用本紀錄（索引由派工者維護）。 |
| **既有 evidence** | #35、#36 的 audit records、worklogs、截圖、network log 全部沿用；沒有任何既有 evidence 因本裁決失效。 |
| **Dependencies** | 依賴圖 7 條邊不變；#38 仍只 blocked by #36。 |

## 7. Orchestrator／tracker 動作（本紀錄指定；DA 不執行）

1. **Issue #38 body（`gh issue edit 38`）**，只改下列三處、其餘逐字不變（以 diff 證明）：
   - 「Acceptance criteria」清單加一行：`- [ ] AC-V2-01（選縣往返部分；R-V2-MODE-5(a) 選縣部分——依 decision DV-20 \`home_work_01/doc/governance/decisions/decision-20260926-ac-v2-01-county-round-trip-allocation.md\` §4.1；其餘部分已由 #36）`。
   - 「Traceability」的 **R** 列加 `R-V2-MODE-5(a)（選縣部分）`；**AC** 列加 `01（選縣往返部分）`；**AB** 列加 `AB-V2-1（選縣往返部分）`。
   - 「Spec／worklog」的 Decisions 列加本紀錄路徑（DV-20）。
2. **`doc/ticket/tickets-v2.md`**：「實作過程中的調整」段加一列：2026-09-26，DV-20（本紀錄路徑），#38 追加 AC-V2-01 選縣往返部分與 R-V2-MODE-5(a) 選縣部分；#36 不變。
3. **#38 派工**：Executor 與 R1 的 bounded pack 皆列入本紀錄路徑，並引用第 4.1 節；不改派工的其他內容。
4. **Run record**：在 checkpoints／routing 記本次 DA 派工結果（R-1 resolved by DV-20）與 DA binding 核對（Bindings §3.4）。
5. **Commit**：本紀錄與 `derivation-SPEC-V2.md` 的最小修改依 SA-1 由派工者原樣 commit（`doc/governance/**` record-only）。

## 8. Evidence（DA 自行執行，全部唯讀；未讀取 `.env`、未使用任何金鑰、未呼叫 CWA）

- 讀取：Bindings b3 全文；治理 §1.2、§1.5、§2.1、§2.3、§2.4、§3.3–§3.6、§3.8、§4.1–§4.3、§4.6、§4.7、§5.1–§5.4；`SPEC-V2.md` §2.1（MODE-1～6）、§2.3（DD-1～11）、§3（AC-V2-01～23 全表）、§5.3、§6.1–§6.4；`derivation-SPEC-V2.md` 全文（§1–§15）；`issue-36-c1-r1.md` 全文；`gh issue view 38`、`gh issue view 41`（body、state OPEN、label `ready-for-agent`）；`tickets-v2.md` 全文；run record「Work item status／frontier」與 2026-09-26 各 checkpoint；OC-V2 §2.5 S-3／S-4、§3 AB-V2-1／AB-V2-6（grep）；先例格式 `decision-20260924-dashboard-state-mapping.md`。
- 實作 grounding（只讀）：`static/app.js:83`（`nowView`）、`:150`（`selectedStationId`，註解「kept across mode switches」）、`:265-277`（`setMode` 離開 Now 時保存 center／zoom）、`:346-352`（`restoreNowView`）、`:559-560`（代表站集合不含已選站時清除選取）。
- Git（read-only）：HEAD `760027206c53feb076962cecd53f0d0017e76e6b`（`home_work_01-v2-implementation`）；`git status --porcelain` 只有既存的工具殘留 `grep.exe.stackdump`；`derivation-SPEC-V2.md` 最後一次修改為 `dd4cc6b`（依賴圖修正）。
- 寫入：本紀錄（新增）；`derivation-SPEC-V2.md` §15.2 #38 列、§15.3 AC 表 01 列、§15.3 MODE 群組列、§14 新增一列（Edit 局部修改）。未修改 SPEC-V2、OC-V2、任何 audit record、worklog、實作或測試；未 commit（派工者依 SA-1 處理）；未動 GitHub Issue。
- 產出不含任何金鑰格式字串。
