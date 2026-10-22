# HW2 V2（Enhance）票務索引（`home_work_02/`）

票本身開在 GitHub Issues；本檔只放索引：編號、標題、依賴、狀態與連結，不複製票的內容（`CLAUDE.md`）。V1 的索引 [`tickets.md`](tickets.md)、Spec rev 5 與 issue #59–#67 **不變**；本檔只涵蓋 V2。

- **來源 Spec**：[`../spec/SPEC-V2.md`](../spec/SPEC-V2.md) **rev 2，ACCEPTED 2026-10-21**（GitHub issue #73，Parent）。
- **契約鏈**：Brief V1（[`../brief/BRIEF.md`](../brief/BRIEF.md)，不變）＋ Brief V2 rev 2 含勘誤 E-1（[`../brief/BRIEF-V2.md`](../brief/BRIEF-V2.md)，ACCEPTED 2026-10-21）→ Spec V2 rev 2。票由 MATT `/to-tickets` 產生（2026-10-22；acceptor 確認 5 張 tracer-bullet 切片與依賴後，依兩項調整——V2 獨立繪圖模組、取消於下一個候選邊界生效——發布）。
- **測試 seams**（acceptor 2026-10-21 確認）：(1) 主 seam＝Exploratory run 結果契約（Node 對 Python 通用參照）；(2) 次 seam＝CSV 載入契約＋mock fetch 請求隔離；(3) 靜態 seam＝離線掃描、King County 不變、內建資料一致；(4) ACCEPTANCE.md 人工檢查表。

| # | 票 | Blocked by | 主要 seams | 狀態 | 連結 |
| --- | --- | --- | --- | --- | --- |
| #74 | V2-T1 Problem 下拉、50 Startups 內建資料與 Exploratory run 的 All-in 垂直切片（含載入契約、三層前處理邊界、V2 獨立繪圖模組、mock fetch 前四條） | — | (1)(2)(3)(4) | 待執行 | <https://github.com/yotsubamomo/aiot-classwork/issues/74> |
| #75 | V2-T2 四種特徵選擇方法、候選狀態、winners、Lasso 退化與共線診斷（含 King County canonical 路徑一致性測試、50 Startups 全部 k 有效由 fixture 證明） | #74 | (1)(4) | 待執行 | <https://github.com/yotsubamomo/aiot-classwork/issues/75> |
| #76 | V2-T3 自訂資料集：URL 與本機檔案輸入、目標選擇、失敗訊息與請求隔離（offline_scan 單檔 `fetch` 例外、mock fetch 第五條、三向切換） | #74（與 #75 獨立） | (2)(3)(4) | 待執行 | <https://github.com/yotsubamomo/aiot-classwork/issues/76> |
| #77 | V2-T4 運算預算、非阻塞、取消（下一個候選邊界生效）、進度與可重現性（非阻塞驗收以 UI 實際可操作性為準） | #75、#76 | (1)(4) | 待執行 | <https://github.com/yotsubamomo/aiot-classwork/issues/77> |
| #78 | V2-T5 README、報告探索模式章節、ACCEPTANCE V2 條目、OV-1／SR-09 重做與 ZIP 重打包（Pages 檢查記 NOT TESTED pending merge） | #77 | (3)(4) | 待執行 | <https://github.com/yotsubamomo/aiot-classwork/issues/78> |

狀態值：待執行／執行中／audit 中／已結案（引用 audit record）／BLOCKED（引用 stop report）。

```text
#74 ─┬→ #75 ─┐
     └→ #76 ─┴→ #77 → #78
```

Bindings 並行度 1：實際執行順序為 #74、#75、#76、#77、#78（#75 與 #76 彼此獨立，依票號先後執行）。

## 共同條款（每張票 body 的「共同條款」）

Parent #73；AC 只引用 Spec V2 rev 2（與 Brief V2）；不重開 Q1–Q24、A-1～A-3、SR-V2-01～04、E-1、四個 seams、Tickets Review 的兩項調整；正式分析不變量（主程式、正式套件路徑、`model_data`、結果檔、Test evaluation 紀錄、V1 區塊 DOM／文字／行為、V1 腳本與核心模組、既有測試全部不變；不重跑 notebook、不做新的 Test evaluation）；非阻塞的驗收以 UI 實際可操作性為準；N-10 不設 CI；既有高風險與審查規則、不新增治理規則；push 須 acceptor 明確授權、合併屬 RB-1、root 檔案屬 RB-5；worklog `issue-<n>.md`；追蹤檔案一律 `<學號>`。

## Tickets Review 結果（acceptor 2026-10-22）

- **Verdict：ACCEPTED WITH TWO ADJUSTMENTS**（維持五張、不合併 T4；依賴 T1 → T2／T3 → T4 → T5，T3 不依賴 T2）。
- **調整 A（#74）**：移除「先把 V1 散佈圖抽成共用模組」的 prefactor；V2 用獨立繪圖模組，可用既有圖表函式庫與不修改 V1 行為的通用工具；不重構 V1 已驗證的 dashboard 腳本。
- **調整 B（#77）**：取消語義為「下一個候選邊界生效」，不寫成瞬間終止；執行期間 UI 可操作、取消後不呈現部分結果、重新執行從頭開始。

## 驗收覆蓋（Brief V2 §8 ↔ 票）

| Brief V2 §8 條目 | 票 |
| --- | --- |
| 1 下拉三項；King County 逐字相同 | #74（靜態快照＋人工）；#75、#76、#77、#78 維持不變量 |
| 2 50 Startups 離線完成、五種方法、winner、test、PI 圖、預測器；時間記錄不設門檻 | #74（All-in）、#75（四種方法）、#78（OV-1 重做） |
| 2 補：50 Startups 全部 k 有效由 fixture 證明 | #75 |
| 2a 預測器只在 `VALID` 候選可用 | #74 |
| 3 老師 URL 在 Pages 載入；內容相同時與內建一致 | #76（本機靜態伺服器重現）；Pages 本身記 NOT TESTED pending merge（#78） |
| 4 檔案載入一致 | #76 |
| 5 各失敗訊息；`SKIPPED_RESOURCE_LIMIT` 標示 | #74（拒絕原因碼）、#76（zh-TW 訊息、URL 失敗）、#77（略過與失敗） |
| 6 探索標示；King County 無標示 | #74 |
| 7 零對外請求；自訂 URL 一次 GET | #74（前四條）、#76（第五條＋靜態掃描例外） |
| 8 Node 對 sklearn fixture | #74（載入、三層、All-in、PI）、#75（四種方法、winner、退化、診斷、King County 一致性）、#77（預算、失敗、取消、可重現） |
| 9 OV-1 與 SR-09 重做 | #78（#77 先量測 SR-09 不退步） |
| acceptor 追加：三向切換；URL 失敗後改檔案成功；探索後 King County 不變 | #76；#78 彙整進 ACCEPTANCE |
| 非阻塞與取消（UI 實際可操作） | #77 |
| 可重現性（確定／非確定部分） | #77 |
| README、報告章節、ZIP 同步 | #78 |

Spec V2 rev 2 的 Spec Review 處理（SR-V2-01 三層邊界 → #74；SR-V2-02 聚合與凍結 → #75；SR-V2-03 資源保護／非阻塞／取消 → #77；SR-V2-04 可重現性 → #77）全部有票承接。

## 尚未解決的風險（票開立時）

- 「兩種 problem」的解讀仍是推定（Brief V2 §10）；不阻塞。
- 老師貼的 URL 可能不開跨來源；#76 的檔案載入是出路。
- 瀏覽器端四種方法在中型資料集的耗時未知；#77 的預算與略過處理，數字以實測定。
- Pages URL 上的檢查只能在合併後做；#78 記 NOT TESTED pending merge，合併後另以 Lightweight item 處理（照 V1 AD-3 的做法）。
- 執行與審查依既有 Bindings；本批票不預設任何新的治理安排。尚未授權：實作、commit、push、merge。
