# Proposal 驗收清單

> 檢查日期：2026-10-31。依據：`final_project/docs/requirements_proposal.txt`（作業規範）、`Part_3._課程專題說明.pdf`（①–⑩ 架構）、`L4-1_期末計劃Proposal_寫作方法_.pdf`（A–Z SOP）。
> 對象：`doc/proposal/00-abstract.md`–`04-proposed-scheme.md`、`proposal.docx`／`pdf`、`slides.md`、`proposal-slides.pptx`、`proposal-video`。
> 狀態：✅ 符合、⚠️ 部分符合或建議補強、❌ 缺少。

## 1. 作業規範：Proposal 四部分

| # | 要求 | 位置 | 狀態 | 說明 |
| --- | --- | --- | --- | --- |
| R1 | Abstract 採 A–F 六段（Attention Getter → But → Cure → Development → Experiments → Findings） | 00-abstract.md | ✅ | 三段落涵蓋 A–F；F 寫預期成果並聲明不含實驗結果 |
| R2 | A 段用 2025–2026 證據，不只寫「AI 快速發展」 | 00-abstract.md、01 §A | ✅ | 道安資訊查詢網 2025 年死亡數、機車占比；公路局 2025 年登記數 |
| R3 | F 段不得虛構實驗結果 | 全文 | ✅ | 全文未出現實驗結果；範例段落標明為示意 |
| R4 | Introduction 回答 Why，分 A–F（Attention、Background、Problem、Limitations、Innovation、Contributions） | 01-introduction.md | ✅ | 六節齊全 |
| R5 | Introduction 重要論述有客觀證據與來源 | 01 證據查證表 | ✅ | 19 筆證據逐一查證；交通部對機車族群的說法僅新聞層級，已照原文用詞 |
| R6 | Related Work 約一半 AI、一半領域知識 | 02-related-work.md | ✅ | 摘要表 12 篇：AI 6、領域 6 |
| R7 | Article Summary Table 欄位：Ref／Year／Problem／AI Method／Domain Knowledge／Dataset／Findings／Limitation | 02 §2.5 | ✅ | 欄位完全一致 |
| R8 | 歸納 Existing Research → Limitations → Research Gap → Our Project | 02 §2.7 | ✅ | 四列齊全 |
| R9 | Deep Research Q1：五個核心思維模式，各含意義、證據、對系統設計的影響 | 03 Q1 | ✅ | M1–M5，每項都寫出影響的 Agent 或規則 |
| R10 | Q2：三個爭論，觀點 A ↔ B → 證據 → 共識 → 未解問題 | 03 Q2 | ✅ | C1–C3 |
| R11 | Q3：十個問題，涵蓋 Why／What-if／Trade-off／Failure Case／Evidence／Comparison／Design Decision／Real-world Scenario | 03 Q3 | ✅ | 10 題，八種類型都有 |
| R12 | Proposed Scheme 依 ①–⑧ 基本架構（情境、輸入、Planner、資料取得、分析、領域知識、決策、輸出） | 04 §4.4 | ✅ | 架構圖與模組表逐一對應 |
| R13 | 完整架構圖，模組以 ①②③… 編號並在正文逐一說明 | 04 §4.4、圖 1 | ✅ | |
| R14 | Flowchart：Input → Processing → AI/Analytics → Decision → Output，必要時含 Decision、Loop、Exception、Human Interaction | 04 §4.7、圖 2 | ✅ | 含資訊不足時追問、驗證不通過重新規劃、API 失敗的例外處理 |
| R15 | 有行號的 Pseudocode（Input／Output） | 04 §4.8 | ✅ | Algorithm 1（21 行）、Algorithm 2（9 行） |
| R16 | 資料來源類型（IoT、DB、CSV、API、Web、Open Data、PDF、KB、Vector DB） | 04 §4.10 | ✅ | GPX、API、開放資料、知識庫；向量資料庫未明寫，屬實作細節 |
| R17 | References | proposal.docx 參考文獻 | ✅ | 45 篇，依出現順序統一編號 |

## 2. 作業規範：繳交物

| # | 要求 | 位置 | 狀態 | 說明 |
| --- | --- | --- | --- | --- |
| D1 | ① Proposal Document | proposal.docx／pdf（40 頁，含附錄 A） | ✅ | 2026-10-31 封面填上第 12 組；同日依獨立審查修正後重新產生（見第 6 節） |
| D2 | ② Proposal PPT：研究動機、文獻、Research Gap、Agent Design、Architecture、Flowchart、Pseudocode | proposal-slides.pptx（16 頁） | ✅ | 七項內容都有；2026-10-31 頁尾填上第 12 組並重新產生；同日依審查修正第 10、15 頁 |
| D3 | ③ GitHub Repository：建立正式專題 repo | [moto-touring-copilot](https://github.com/yotsubamomo/moto-touring-copilot) | ✅ | 2026-10-31 建立（公開）：README、DESIGN.md、Proposal PDF／PPTX、圖；`.gitignore` 排除原始 GPX。PDF／PPTX 是組號填寫前的版本，重新產生後要同步 |
| D4 | ④ DESIGN.md：從 Proposal 階段開始維護 | moto-touring-copilot/DESIGN.md | ✅ | Problem → Requirements → Architecture → Components → Data → AI/Analytics → Domain Knowledge → Algorithm → Implementation Mapping → How to Run → Results → Limitations；尚未實作的部分標明為規劃或 TBD |
| D5 | 簡報影片（老師另外要求） | proposal-video.mp4（9 分 59 秒） | ⚠️ | 2026-10-31 依審查修正第 10、15 頁後重新產生；舊版 https://youtu.be/8XWvbD2qnNo 的第 15 頁仍是舊的 E2 指標，需重新上傳並更新連結 |

## 3. 課程專題說明（Part 3，①–⑩）

| # | 要求 | 位置 | 狀態 | 說明 |
| --- | --- | --- | --- | --- |
| P1 | ① 先定義：Agent 是誰、服務誰、解決什麼真實問題 | 01 §B–C、04 §4.1 | ✅ | |
| P2 | ③ 標準 Agent Workflow：Understand → Plan → Acquire → Analyze → Generate → Interact | 04 §4.4.2 | ✅ | 2026-10-31 補上六階段對照表 |
| P3 | ④ 六大能力 TALK × KNOW × SENSE × ANALYZE × THINK × SHOW（老師說適合當評分指標） | 04 §4.4.2、簡報第 9 頁 | ✅ | 2026-10-31 補上對照表與簡報頁 |
| P4 | ⑥ LLM 負責理解推理，Analytics Engine 負責計算與證據 | 04 §4.3、§4.4.1 | ✅ | |
| P5 | ⑦ 專業介面，不只是聊天視窗 | 04 §4.4 ⑧ | ✅ | Google Maps 行程儀表板 |
| P6 | ⑨ Level 1／2／3 | 04 §4.4.2、簡報第 9 頁 | ✅ | 2026-10-31 補上各 Level 在本專題的內容與範圍 |
| P7 | ⑩ 成功作品的六項成果 | 04 §4.11 | ✅ | 評估計畫 E1–E4 |

## 4. A–Z SOP（建議項目）

| # | 項目 | 狀態 | 說明 |
| --- | --- | --- | --- |
| S1 | Abstract 精簡（SOP 建議 150–250 字為主） | ✅ | 2026-10-31 由約 739 字精簡為約 496 字（含引用標號），保留 A–F |
| S2 | L：Introduction 最後交代文章結構 | ⚠️ | 沒有章節導讀段落 |
| S3 | M–O：Related Work 分類、近期方法、比較表 | ✅ | |
| S4 | PA–PL | ✅ | |
| S5 | PM：數學證明，或以複雜度分析代替 | ⚠️ | 未寫；SOP 說非理論型研究可省略或改寫複雜度分析 |
| S6 | Q–V：評估指標、比較方法、實驗設定 | ✅ | Proposal 階段以評估計畫呈現 |

## 5. 其他

| # | 項目 | 狀態 | 說明 |
| --- | --- | --- | --- |
| O1 | AI 使用規範：能解釋 AI 做了什麼、為什麼這樣設計、如何驗證 | ⚠️ | 2026-10-31 新增附錄 A（`05-ai-usage.md`）與提示詞紀錄（`ai-usage-log.md`）；內容待組員確認 |
| O2 | Word 內殘留的查證標記 | ✅ | 2026-10-31 已改寫 DeepTTE 的 Dataset 欄 |
| O3 | 草稿標記、TODO | ✅ | 組成的文件中沒有 |

## 6. 獨立審查（2026-10-31）

另一個 session 對 Proposal 做了一次獨立審查（PASS WITH ISSUES，F-01…F-23、N-01…N-06）。修正分兩批：

| 項目 | 處理 | 位置 |
| --- | --- | --- |
| F-01 配速模型以速度分位數換算時間，P90 時間實為最樂觀值 | 已修：改為直接預測路段移動時間的對數 | 04 §4.5、§4.6；Alg 2 line 07；簡報第 10 頁；DESIGN.md §6 |
| F-02 各點抵達時刻未定義 P90 | 已修：新增 ETA^(0.5)、ETA^(0.9) 定義；規則 2、3 改用抵達時刻 | 04 §4.4.1、§4.6、Alg 1 lines 09–13；DESIGN.md §4.1、§4.2 |
| F-05 E2 以規則 1–5 評分會循環驗證 | 已修：改以獨立 oracle 評分（違規率、時間誤差、一致率、拒答率） | 04 §4.11、§4.12；Abstract；Introduction F4；簡報第 15 頁；DESIGN.md §6 |
| F-20 DESIGN.md 的 Algorithm 1 與 Proposal 不一致 | 已修：改為 Proposal 的 21 行版本 | DESIGN.md §8 |
| F-03、F-04、F-06～F-12 等其餘 Major | 不改 Proposal，留到實作 Spec 階段 | 審查報告 |

第一批（F-01、F-02、F-05）在 PR #82 commit 0e97ed3 與 moto-touring-copilot PR #3；第二批（簡報、影片、DESIGN.md Algorithm 1）在本次 commit 與 moto-touring-copilot 分支 `docs-review-sync-alg1-slides`。

## 待處理清單

| 優先 | 項目 | 需要誰 |
| --- | --- | --- |
| ~~必要~~ 已完成 | D3、D4：正式專題 repo 與 DESIGN.md | — |
| ~~必要~~ 已完成 | D1、D2、D5：填第 12 組，重新產生文件、簡報與影片，新的 PDF／PPTX 複製到 moto-touring-copilot | — |
| ~~必要~~ 已完成 | D5：上傳 YouTube（https://youtu.be/8XWvbD2qnNo），連結補進 moto-touring-copilot README | — |
| ~~建議~~ 已完成 | P2、P3、P6：Proposed Scheme §4.4.2 與簡報第 9 頁 | — |
| ~~建議~~ 已完成 | S1：Abstract 約 496 字 | — |
| 必要 | D5：重新上傳修正後的影片，更新 moto-touring-copilot README 與本清單的連結 | 你上傳 |
| 建議 | O1：附錄 A 與提示詞紀錄已起草，待確認內容 | 你確認 |
| ~~建議~~ 已完成 | O2：DeepTTE Dataset 欄 | — |
| 可選 | S2：Introduction 加章節導讀段落 | Claude |
| 可選 | S5：Proposed Scheme 補簡短的複雜度分析 | Claude |
