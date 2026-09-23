# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 專案用途

AIoT 課程的長期 workspace，每週持續加入上課資料、課堂練習、作業、程式碼與報告。

Claude 從專案 root 啟動。Root 是整個課程的 navigation / coordination layer，不綁定任何單一週次。

Root 的 `AGENTS.md` 是給 Codex 用的指示檔，內容是從本檔整理出來的，Claude 不需要讀取。兩者內容不一致時，以本檔為準。

## 目錄組織

- 課程內容依週次放在 `week01/`、`week02/`、`week03/`… 目錄。
- 每個 week 是相對獨立的課程單元，可能包含 lecture material、notes、assignment、source code、dataset、experiment、report / result。各週內部結構不強制統一，以該週實際檔案為準。
- 目前沒有 cross-week 共用程式或共用資源目錄。之後真的出現跨週重用需求時，再依實際情況整理，不預先建立。
- Root 的 `docs/` 放跨週、跨單元通用的文件，依用途分資料夾：`docs/agents/` 是 agent skill 的設定與慣例，`docs/conventions/` 是團隊的工作慣例（例如 git commit 規則）。單元專屬的文件不放這裡，放該單元自己的 `doc/`（單數）。

## 單元文件的存放位置

每個 DIC 或作業單元的文件放在該單元自己的 `doc/` 下，依類型分資料夾。資料夾在真的產出該類文件時才建立，不預先建空的。

```text
weekNN/ 或 home_workNN/
├── doc/
│   ├── requirement/   # 老師提供的題目、講義、規格文件（來源文件，不改寫）
│   ├── brief/         # 事前盤點：落差分析、既有實作與需求的比對
│   ├── spec/          # 實作 spec（`/to-spec` 的產出）
│   ├── ticket/        # 票務索引（`/to-tickets` 的產出摘要）
│   └── acceptance/    # 逐條對應需求的驗收清單與驗證方式
├── CONTEXT.md         # 該單元的專案語彙，留在單元根目錄
├── README.md          # 該單元的說明文件，留在單元根目錄
└── （實作檔案）
```

規則：

- **`doc/` 只放文件**，實作檔案、資料檔與測試留在單元根目錄或其既有位置。
- **`CONTEXT.md` 與 `README.md` 留在單元根目錄**。前者是 `CONTEXT-MAP.md` 指向的詞彙表位置，後者是單元的入口。
- **票開在 GitHub Issues**，`doc/ticket/` 只放索引：編號、標題、依賴關係、狀態與連結。不要把每張票的內容複製成檔案，那會與 tracker 上的狀態不同步。
- **老師提供的原始文件放 `doc/requirement/`**，保持原樣不改寫；需要整理時另外寫成 brief。
- 既有單元 `week02/` 已依此結構整理，可作為範例。

## 尋找某週的作業 context

處理某週任務時，從該週目錄開始，先確認：

1. 題目與要求（作業說明、講義、老師提供的文件）
2. input / dataset
3. 既有 code（starter code、template、notebook）
4. expected output
5. grading / submission 限制（若有）

Repository 裡找不到的項目視為未知，向使用者確認；不要自行補出老師沒有提出的要求。

## 工作邊界

- 處理某週任務時，優先閱讀並只修改該週目錄。
- 可以參考前幾週的資料，但不要因為共用概念就修改歷史週次的作業；任務確實需要跨週修改時，先說明再動手。
- 已有 starter code、template 或 notebook 時，沿用原本的結構、檔名與寫法。

## 技術與環境

- 以各週實際使用的語言、framework、notebook、environment、dependency 為準。
- 不同週可以使用不同技術，各自維持自己的環境與結構。
- 不要為了整理而新增 framework、package layout 或 tooling。

## Commands

目前未發現統一的 project-level command（root 沒有 build / test / dependency 設定檔）。

各週的 install / run / test 方式以該週目錄內的檔案（README、requirements、notebook、設定檔等）為準。之後確認為跨週長期通用的 command，再補到此處。

## Git workflow

Branch 與 commit message 的完整規則見 `docs/conventions/git-commit-rules.md`，重點如下：

- 每個 feature 或 fix 都開新 branch，名稱依實際修改內容取描述性的名字，不直接在 `main` 上 commit。
- Commit message 第一行是 `[Modify] – 主要變更的摘要`（分隔符是 en-dash `–`），接一行空白，之後每項變更各一行，以 `[Additions]`、`[Modification]`、`[Fix]` 三種前綴分類。
- 不在 commit message 加任何 Claude 標記：不寫 `Co-Authored-By: Claude`，也不寫 `🤖 Generated with Claude Code`。此規則優先於工具預設的 attribution 提示。
- 描述聚焦在實際改了什麼與為什麼，清楚且技術上精確。

## Agent skills

### Issue tracker

Issue 與 spec 放在 GitHub Issues（`yotsubamomo/aiot-classwork`），以 `gh` CLI 操作。見 `docs/agents/issue-tracker.md`。

### Triage labels

沿用五個預設標籤名稱，未改名。見 `docs/agents/triage-labels.md`。

### Domain docs

多 context：root 的 `CONTEXT-MAP.md` 指向各單元的 `CONTEXT.md`。見 `docs/agents/domain.md`。

## 維護本檔

本檔只記錄長期有效的資訊。某週的作業進度、TODO、單次 session 的工作內容與尚未確認的推測，不寫入此檔。
