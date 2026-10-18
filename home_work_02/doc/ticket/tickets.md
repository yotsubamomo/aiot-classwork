# HW2 票務索引（`home_work_02/`）

票本身開在 GitHub Issues；本檔只放索引：編號、標題、依賴、狀態與連結，不複製票的內容（Bindings b5 §7；`CLAUDE.md`）。

- **來源 Spec**：[`../spec/SPEC.md`](../spec/SPEC.md) **rev 5**（GitHub issue #59，Parent）。
- **契約鏈**：Brief @ `dff7c55c`＋CC-1 → Spec rev 5 → DA [`../governance/decisions/derivation-SPEC.md`](../governance/decisions/derivation-SPEC.md)（§9 Tickets 的分配與覆蓋）。票由 MATT `/to-tickets` 產生草稿（2026-10-18，acceptor 確認 8 張 tracer-bullet 切片與 Test 時序修訂後發布）；票的 authority 來自 DA derivation，不來自 skill。
- **前一代票**：#50–#56（r4／Spec v1.1）已於 2026-10-18 關閉為 not planned，見 [`decision-20261018-r4-derived-contracts-disposition.md`](../governance/decisions/decision-20261018-r4-derived-contracts-disposition.md)。

| # | 票 | Blocked by | 高風險 | 狀態 | 連結 |
| --- | --- | --- | --- | --- | --- |
| #60 | T1 資料基線、分組切分與 model_data 契約骨架（`test_inputs` 只建 schema 與 fixture；分割只提供 test 列識別與 n_test） | — | H-1、H-2、H-3 | 已結案（`../governance/audit/issue-60-c1-r1.md` CLOSURE；DA `decision-20261018-issue60-a4-student-id.md` S-1） | <https://github.com/yotsubamomo/aiot-classwork/issues/60> |
| #61 | T2 All-in baseline 端到端：fit、PI、test 守門、dashboard 垂直切片（fixture 驗證 test 流程，不評估正式 test） | #60 | H-2、H-3 | 已結案（`../governance/audit/issue-61-c1-r2.md` CLOSURE） | <https://github.com/yotsubamomo/aiot-classwork/issues/61> |
| #62 | T3 四種特徵選擇方法 k=1…18、canonical subsets 與 CV winners（不評估正式 test） | #61 | H-2、H-3 | 已結案（`../governance/audit/issue-62-c1-r1.md` CLOSURE） | <https://github.com/yotsubamomo/aiot-classwork/issues/62> |
| #63 | T4 Ridge／Lasso 對照、p-value backward、Adjusted R² 與**一次性正式 Test 評估**（G-3 守門在此開啟；正式 `test_inputs` 列與 `test` 在此寫出） | #62 | H-2、H-3 | 待執行 | <https://github.com/yotsubamomo/aiot-classwork/issues/63> |
| #64 | T5 五大假設診斷、模型解釋與 Deployment | #62 | H-2、H-3、H-4 | 待執行 | <https://github.com/yotsubamomo/aiot-classwork/issues/64> |
| #65 | T6 報告 draft、單元 README 與 ACCEPTANCE.md | #63、#64 | H-2、H-4 | 待執行 | <https://github.com/yotsubamomo/aiot-classwork/issues/65> |
| #66 | T7 Acceptor 證據整合與 final 報告 | #65；acceptor 輸入（ChatGPT PDF、NotebookLM 材料） | H-1、H-2、H-4 | 待執行（等待 acceptor 輸入） | <https://github.com/yotsubamomo/aiot-classwork/issues/66> |
| #67 | T8 打包、離線驗收（OV-1～OV-6）、乾淨環境重跑與整合 | #66；acceptor 輸入（學號）；root 檔案一列另需 RB-5 授權 | H-1～H-4 | 待執行（等待 acceptor 輸入） | <https://github.com/yotsubamomo/aiot-classwork/issues/67> |

狀態值：待執行／執行中／audit 中／已結案（引用 audit record）／BLOCKED（引用 stop report）。

```text
#60 → #61 → #62 → #63 ─┐
                 └→ #64 ─┴→ #65 → #66 → #67
                          ↑        ↑
             acceptor：ChatGPT PDF、NotebookLM    acceptor：學號；root 檔案 RB-5
```

Bindings 並行度 1：實際執行順序為 #60、#61、#62、#63、#64、#65、#66、#67（#63 與 #64 彼此獨立，依票號先後執行）。

## 共同義務（每張票 body 的「共同條款」）

Parent #59；AC 只引用 Spec rev 5 與 DA 義務；不重開已接受的決定；Wireframe v0.2 只作 UI 參考；正式 Test 評估只在 #63 一次執行；N-10 不設 CI、不以 PR checks 為條件；高風險 A-1～A-8；push 須 acceptor 明確授權、合併屬 RB-1；worklog `issue-<n>.md`。

## Tickets Review 結果（acceptor 2026-10-18）

- **Verdict：ACCEPTED**（acceptor「APPROVED WITH ONE REQUIRED CLARIFICATION」→ TR-01、TR-02 依 DA `derivation-SPEC.md` §9.6 處理後，無新的 Blocking／High finding）。
- **TR-01（High）Test 資料隔離**：DA 判定為票的文字澄清（§5.3 第 2 類），不改 Spec、不改契約：#60 只建 `test_inputs` schema 與 fixture、分割只提供 test 列識別與 n_test；正式 test 列的特徵與 `price` 只能經 G-3 守門載入，守門只在 #63 開啟；正式 `test_inputs` 列與 `test` 由同一匯出程式在 #63 同一次執行寫出；#60～#62 只用 synthetic fixture 或 training 子集；fixture 的 `model_data` 不進追蹤路徑；最終契約、test 列數、CC-1 授權集合不變。已以「Test 資料隔離」共同條款寫入全部 8 張票，並修訂 #60、#61、#62、#63、#67 的 AC。
- **TR-02（Low）**：#64 改為以 training set 實際的重複交易筆數為準、程式計算後引用；全資料集 177 筆只作背景並標明層級。
- **TK-1**：見上方合併後 work item。

## 覆蓋摘要（DA §9 為準）

- DA G-1～G-4：#63（G-1、G-2、G-3、G-4，含守門開啟與正式 `test_inputs`）；#61 建立 G-3 守門（保持關閉）；#62 斷言 G-2。
- OV-1～OV-6：#67 驗收；#60 靜態掃描前置；#61 內建 OV-6 量測。
- F-4 補充義務（Kaggle 名次說明、notebook 六章、README、學號設定路徑）：#60、#65。
- Acceptor 輸入：#66（ChatGPT PDF、NotebookLM）、#67（學號、root 檔案 RB-5）。
- **合併後的 Lightweight work item（不在本批票內）**：GitHub Pages URL 上的 dashboard 檢查（Brief §7／§10）；acceptor 2026-10-18 TK-1 決定採 (a)：合併進 `main` 後執行，觸及 H-2 需 audit；#67 與 ACCEPTANCE.md 先記 NOT TESTED（pending merge）。見 `../governance/outcome-contract.md` §4 AD-3。
