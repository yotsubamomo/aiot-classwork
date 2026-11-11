# Proposal build

`doc/proposal/` 的 Markdown 是 Proposal 的唯一來源；`proposal.docx` 與 `proposal.pdf` 都由它重新產生。**不要直接改 Word**，重新產生時會被覆蓋。

## 要改內容時

| 要改的 | 檔案 |
| --- | --- |
| 封面（題目、姓名／學號、日期） | `doc/proposal/metadata.yaml` |
| 各章內容 | `doc/proposal/00-abstract.md`–`04-proposed-scheme.md` |
| 架構圖、流程圖 | `04-proposed-scheme.md` 裡的 mermaid 區塊 |
| 參考文獻 | 各章底下的 `## References`；組合時自動合併重複、依第一次出現的順序編號 |

## 重新產生

```bash
python -I build.py
```

會依序：合併各章並統一參考文獻 → 用 mermaid-cli 把圖轉成 PNG → pandoc 轉 Word（中文字型、表格框線）→ 用 Word 更新目錄並輸出 PDF → 把 `proposal.docx`、`proposal.pdf`、`figures/` 寫回 `doc/proposal/`。中間檔放在 `.out/`。

## 需要

- Python 套件：`pypandoc_binary`、`python-docx`
- Node.js（`npx` 會下載 `@mermaid-js/mermaid-cli`）
- Google Chrome（產生圖片用）
- Microsoft Word（更新目錄、輸出 PDF）

## 檔案

| 檔案 | 作用 |
| --- | --- |
| `build.py` | 一次跑完整個流程 |
| `assemble.py` | 合併各章、移除查證表、統一參考文獻、抽出 mermaid 圖 |
| `make_docx.py` | 產生中文字型的 Word 範本，pandoc 轉檔，加表格框線 |
| `mermaid.json` | 圖的主題與字型 |
