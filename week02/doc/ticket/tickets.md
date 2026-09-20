# DIC-1 票務索引

票本身開在 GitHub Issues，這份索引記錄拆票結果、依賴關係與最終狀態，讓 repo 裡看得到全貌。

- **Repository**：<https://github.com/yotsubamomo/aiot-classwork>
- **Parent issue**：[#1 Spec: AIoT Personal Portal & Timekeeper](https://github.com/yotsubamomo/aiot-classwork/issues/1) — 已關閉
- **來源 spec**：[`../spec/SPEC.md`](../spec/SPEC.md)
- **拆票日期**：2026-09-20　**完成日期**：2026-09-21

依賴關係使用 GitHub 原生的 issue dependencies，共 20 條邊；下表的「Blocked by」即為當時建立的阻擋關係。

| # | 票 | Blocked by | 狀態 | Commit |
| --- | --- | --- | --- | --- |
| [#2](https://github.com/yotsubamomo/aiot-classwork/issues/2) | Prefactor：拆成四檔並建立純邏輯測試接縫 | — | 已完成 | `935c996` |
| [#3](https://github.com/yotsubamomo/aiot-classwork/issues/3) | 視覺基礎改版：深色預設、動態光暈與英文介面 | #2 | 已完成 | `6e6092d` |
| [#4](https://github.com/yotsubamomo/aiot-classwork/issues/4) | 統一狀態樹 `aiot_user_state` | #2 | 已完成 | `05cde41` |
| [#5](https://github.com/yotsubamomo/aiot-classwork/issues/5) | 時鐘升級：連續更新、毫秒、UNIX timestamp 與 SVG 秒環 | #2、#3 | 已完成 | `610bba2` |
| [#6](https://github.com/yotsubamomo/aiot-classwork/issues/6) | 日曆資訊與時段問候徽章 | #3 | 已完成 | `877efa1` |
| [#7](https://github.com/yotsubamomo/aiot-classwork/issues/7) | 可編輯的名稱與標語 | #4 | 已完成 | `52f0ebc` |
| [#8](https://github.com/yotsubamomo/aiot-classwork/issues/8) | 抽屜外殼與 About／Connect 分頁 | #3 | 已完成 | `c8cde93` |
| [#9](https://github.com/yotsubamomo/aiot-classwork/issues/9) | Projects 分頁：非同步載入專案目錄 | #8 | 已完成 | `adf6ab4` |
| [#10](https://github.com/yotsubamomo/aiot-classwork/issues/10) | 即時天氣與城市選單 | #3、#4 | 已完成 | `9e7fd47` |
| [#11](https://github.com/yotsubamomo/aiot-classwork/issues/11) | Zen 模式補齊與鍵盤快捷鍵 | #4、#8 | 已完成 | `d4fcf87` |
| [#12](https://github.com/yotsubamomo/aiot-classwork/issues/12) | Web Audio 滴答音效 | #4、#5 | 已完成 | `77245e8` |
| [#13](https://github.com/yotsubamomo/aiot-classwork/issues/13) | 收尾：教學註解、文件同步與驗收清單 | #5、#6、#7、#9、#10、#11、#12 | 已完成 | `8fe47ef` |

## 拆票原則

每張票是一條垂直切片：完成後可以單獨展示或驗證，而不是某一層的水平切分。唯一的例外是 #2——它沒有使用者可見的變化，但後續每張票都需要它建立的模組邊界與測試接縫，所以排在最前面。

票 #3（視覺基礎）刻意排在功能票之前，讓後續新增的 UI 直接長在最終視覺上，不必回頭重調。

## 實作過程中的調整

- **#8 順帶完成了 #11 的一條 AC**：`ESC` 的優先順序（抽屜開著先關抽屜）與 Zen 共用同一個 keydown 處理，分開做會互相打架。
- **#4 順帶完成了 #11 的另一條 AC**：`zenMode` 的保存與還原。欄位只寫不讀會讓儲存內容與實際行為對不上。
- **三個不在票裡的既有問題**在過程中被發現並修掉：裝飾圓盤造成的版面偏移（#3）、`projects.json` 的 HTTP 快取導致改檔看不到效果（#9）、城市選單觸控目標不足 44px（#13）。
