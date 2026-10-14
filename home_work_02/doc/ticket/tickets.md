# HW2 票務索引（`home_work_02/`）

票本身開在 GitHub Issues；本檔只放索引：編號、標題、依賴、狀態與連結，不複製票的內容（Bindings b5 §7；`CLAUDE.md`）。

- **來源 Spec**：[`../spec/SPEC.md`](../spec/SPEC.md) v1.0（EFFECTIVE；commit `b012e4f9`）
- **Derivation record**：[`../governance/decisions/derivation-SPEC.md`](../governance/decisions/derivation-SPEC.md) §13（Tickets 的分配、依賴與 boundary determination）
- **拆票**：2026-10-14，Design Authority，Issues #50–#56

| # | 標題 | Blocked by | 狀態 | 連結 |
| --- | --- | --- | --- | --- |
| #50 | HW2 資料固定與分區：以 sha256 固定隨附的 King County CSV、mlr/data.py 載入驗證、group-aware Fit／Calibration／Test 分區與 outer／inner folds | — | 待執行 | <https://github.com/yotsubamomo/aiot-classwork/issues/50> |
| #51 | HW2 前處理、五個 candidate procedures 與 nested CV 選模：source-feature group 選擇、inner CV 調參、outer-CV 比較與凍結 | #50 | 待執行 | <https://github.com/yotsubamomo/aiot-classwork/issues/51> |
| #52 | HW2 Conformal 校準、單次 Test 評估、預測圖與 Deployment 預測函式 | #51 | 待執行 | <https://github.com/yotsubamomo/aiot-classwork/issues/52> |
| #53 | HW2 主程式 notebook hw2.ipynb（CRISP-DM 六階段）、結果 artifact、README 與乾淨環境重跑 | #52 | 待執行 | <https://github.com/yotsubamomo/aiot-classwork/issues/53> |
| #54 | HW2 報告（draft）：Markdown 範本與 HTML→PDF 建置、acceptor 證據以外的全部章節與主流解法比較 | #53 | 待執行 | <https://github.com/yotsubamomo/aiot-classwork/issues/54> |
| #55 | HW2 acceptor 證據整合與 final 報告：「GPT 輔助內容」、「NotebookLM 摘要」與 ChatGPT 對話附錄（等待 acceptor 輸入） | #54；acceptor 輸入 Spec §9.1 #1、#2 | 待執行（等待 acceptor 輸入） | <https://github.com/yotsubamomo/aiot-classwork/issues/55> |
| #56 | HW2 打包與整合驗收：學號 ZIP、解壓驗證、ACCEPTANCE.md 與最終乾淨環境重跑（等待學號） | #55；acceptor 輸入 Spec §9.1 #3 | 待執行（等待 acceptor 輸入） | <https://github.com/yotsubamomo/aiot-classwork/issues/56> |

狀態值：待執行／執行中／audit 中／已結案（引用 audit record）／BLOCKED（引用 stop report）。

```text
#50 → #51 → #52 → #53 → #54 → #55 → #56
                                  ↑      ↑
                    acceptor #1、#2    acceptor #3（學號）
```
