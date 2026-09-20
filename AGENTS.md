# AGENTS.md

## 指示來源與專案範圍

- Root `CLAUDE.md` 是本專案的主要 project instruction source；本檔是其中適用於 Codex 的長期規則投影。
- 本專案是 AIoT 課程的長期 workspace。Root 是整個課程的主要工作入口與 navigation / coordination layer，不綁定單一週次。

## Weekly organization

- 課程內容依週次放在 `week01/`、`week02/`、`week03/` 等目錄。
- 每個 `weekXX/` 是相對獨立的課程單元，內部結構以該週實際檔案為準，可能包含講義、筆記、作業、程式碼、資料集、實驗與報告或結果。
- 目前沒有 cross-week 共用程式或資源目錄。只有在實際出現跨週重用需求時，才依當時情況整理。

## Unit document layout

每個 DIC 或作業單元的文件放在該單元自己的 `doc/` 下，依類型分資料夾；資料夾在真的產出該類文件時才建立。

```text
weekNN/ 或 home_workNN/
├── doc/
│   ├── requirement/   # 老師提供的題目與講義，保持原樣
│   ├── brief/         # 事前盤點與落差分析
│   ├── spec/          # 實作 spec
│   ├── ticket/        # 票務索引
│   └── acceptance/    # 驗收清單
├── CONTEXT.md         # 單元語彙，留在單元根目錄
├── README.md          # 單元說明，留在單元根目錄
└── （實作檔案）
```

- `doc/` 只放文件；實作檔案、資料檔與測試留在單元根目錄或其既有位置。
- `CONTEXT.md` 與 `README.md` 不進 `doc/`。
- 票開在 GitHub Issues，`doc/ticket/` 只放索引（編號、標題、依賴、狀態、連結），不複製票的內容。
- `week02/` 已依此結構整理，可作為範例。

## Assignment workflow

處理某週任務時，從該週目錄開始，依序確認：

1. 題目與要求，包括作業說明、講義及老師提供的文件。
2. Input 或 dataset。
3. 既有 code，包括 starter code、template 或 notebook。
4. Expected output。
5. Grading 或 submission 限制（若有）。

Repository 中找不到的資訊視為未知，向使用者確認，不自行補出老師未提出的要求。

## Working boundary

- 優先閱讀並只修改任務所屬的 `weekXX/`。
- 可以參考前幾週資料，但不因概念共用而修改歷史週次。任務確實需要跨週修改時，先說明再動手。
- 有 starter code、template 或 notebook 時，沿用原本的結構、檔名與寫法。

## Implementation

- 以各週實際使用的語言、framework、notebook、environment 與 dependency 為準；不同週可各自維持不同技術與結構。
- 不為整理目的新增 framework、package layout 或 tooling。
- Root 目前沒有統一的 project-level build、test 或 dependency 設定。各週的 install、run 與 test 方式只依該週可確認的 README、requirements、notebook 或設定檔執行；未確認的 command 不做假設。

## Agent skills

### Issue tracker

Issue 與 spec 放在 GitHub Issues（`yotsubamomo/aiot-classwork`），以 `gh` CLI 操作。見 `docs/agents/issue-tracker.md`。

### Triage labels

沿用五個預設標籤名稱，未改名。見 `docs/agents/triage-labels.md`。

### Domain docs

多 context：root 的 `CONTEXT-MAP.md` 指向各單元的 `CONTEXT.md`。見 `docs/agents/domain.md`。

本檔只保留跨 session、跨 week 仍成立的資訊，不記錄單週進度、TODO、單次 session 內容或未確認的推測。
