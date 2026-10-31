# Proposal 完成計畫

> 2026-10-31 建立。題目：D1 重機旅遊規劃顧問（見 `architecture-scope.md`）。
> 截止：2026-11-11（週三）。可用時間：10/31–11/1、11/7–8 兩個週末，加上 11/9–11 晚上的檢查。

## 已決定（2026-10-31）

| 項目 | 決定 |
| --- | --- |
| 文件語言 | 中文為主，專有名詞保留英文 |
| 正式專題 repo | 另開新 repo；專題程式、README、DESIGN.md 放新 repo，`aiot-classwork/final_project/` 只留選題與課程文件。2026-10-31 建立 [yotsubamomo/moto-touring-copilot](https://github.com/yotsubamomo/moto-touring-copilot)（公開），本機放在 aiot-classwork 同層 |
| 文件格式 | 用 Word（.docx）撰寫，交 PDF |
| GPX 驗證 | Proposal 階段不做，只寫預期成果；驗證留到期末實作 |
| 封面 | 以組繳交，封面寫組別，不寫學號（`metadata.yaml`） |
| 簡報影片 | 老師要求 Proposal 要交；約 8–10 分鐘（約 12–15 頁、逐字稿約 2,000–2,800 字）；AI 語音（台灣中文神經語音）；投影片與逐字稿由同一份 Markdown 產生，再合成自動播放的 MP4 |
| 影片存放 | MP4 不放進 repo（`.gitignore`），只上傳 YouTube；字幕檔 `.srt` 與 PPT 放進 repo。2026-10-31 上傳：https://youtu.be/9ZBrHomaZoI（依審查修正後重新上傳，取代舊版 8XWvbD2qnNo） |
| 修改方式 | `doc/proposal/` 的 Markdown 是唯一來源（封面在 `metadata.yaml`）；Word 與 PDF 用 `final_project/tools/proposal_build/build.py` 重新產生，不直接改 Word |

## 交付物

| 交付物 | 內容 | 評分 |
| --- | --- | --- |
| ① Proposal 文件 | Abstract、Introduction、Related Work、Deep Research、Proposed Scheme、References | Introduction 20%、Related Work 20%、Deep Research 20%、Agent 與架構 20%、流程圖 + Pseudocode + 可行性 15% |
| ② Proposal PPT | 動機、文獻、Research Gap、Agent 設計、架構圖、流程圖、Pseudocode | 同上內容 |
| ③ GitHub repo | 正式專題 repo | 和 ④ 合計 5% |
| ④ DESIGN.md | 從 Proposal 階段開始維護 | |
| ⑤ 簡報影片 | 投影片 + AI 語音逐字稿的自動播放影片，約 8–10 分鐘 | 老師另外要求 |

### 簡報影片流程

`slides.md`（每頁：投影片內容 + 逐字稿）→ 可編輯的 `.pptx`（逐字稿放備忘稿）→ PowerPoint 輸出每頁圖片 → 逐字稿轉 AI 語音 → 每頁停留時間等於語音長度，加上字幕，合成 1080p MP4。工具：python-pptx、PowerPoint、edge-tts（台灣中文語音 HsiaoChen／HsiaoYu／YunJhe）、imageio-ffmpeg。

## 文件結構（對應作業規範與 A–Z SOP）

| 章節 | 內容 | 對應 |
| --- | --- | --- |
| Abstract | A Attention Getter → B But → C Cure → D Development → E Experiments → F 預期成果（不能寫實驗結果） | A–F |
| 1. Introduction | 動機證據、背景、問題、既有限制、創新、貢獻 | G–L |
| 2. Related Work | 約一半 AI 技術、一半領域知識；Article Summary Table（Ref / Year / Problem / AI Method / Domain Knowledge / Dataset / Findings / Limitation）；Existing Research → Limitations → Research Gap → Our Project | M–O |
| 3. Deep Research | Q1 五個核心思維模式；Q2 三個專業爭論（觀點 A ↔ 觀點 B → 證據 → 共識 → 未解問題）；Q3 十個深度理解問題 | — |
| 4. Proposed Scheme | 有編號的系統架構圖（①–⑧）、多 Agent 分工、流程圖、有行號的 Pseudocode、資料來源、分析方法、評估計畫 | PA–PM |
| References | 所有引用附原始出處 | — |

## 時程

| 時間 | 工作 | 誰 |
| --- | --- | --- |
| 10/31–11/1 | Deep Research 草稿；Related Work 文獻蒐集與比較表；Introduction 證據逐一查證原文 | Claude 起草、你審稿 |
| 11/2–11/6（平日） | 依審稿意見修改；Proposed Scheme 草稿（架構圖、流程圖、Pseudocode） | Claude |
| 11/7–11/8 | 審 Proposed Scheme；寫 Abstract；建立新 repo 與 DESIGN.md；組成 Word 文件；製作 PPT | Claude 起草、你審稿和決定 |
| 11/9–11/11 | 整體檢查、轉 PDF、交件 | 你 |

## 注意事項

- 老師去年要求各組補上「做 PPT 用的提示詞」：AI 使用過程要留紀錄，期末要能交代。
- 老師建議先寫一版有邏輯和研究內容的稿，最後才做 PPT。
- Proposal 只寫預期成果，不能虛構實驗結果。
- GPX 原始檔含住家位置，不放進任何 repo。

## 待決定

- [x] 新 repo 的名稱、公開或私人：moto-touring-copilot，公開
- [ ] Word 範本：用學校或老師的範本，或自訂
