# Slides and video build

`doc/proposal/slides.md` 是簡報與逐字稿的唯一來源；`proposal-slides.pptx`、`proposal-video.mp4`、`proposal-video.srt` 都由它重新產生。**不要直接改 PPT**，重新產生時會被覆蓋。

## slides.md 的格式

- 開頭的 front matter：`title`、`subtitle`、`footer`（每頁頁尾與封面下方文字）、`voice`（語音）。
- 每頁以 `## 標題` 開頭；`layout:` 指定版型：`title`、`bullets`、`figure`、`table`、`code`。
- `figure` 版型可以放 `![說明](figures/xxx.png)`，或直接寫 ```` ```mermaid ```` 區塊（建議橫向排版，適合 16:9）。
- `來源：` 開頭的一行以小字放在投影片底部。
- `### 逐字稿` 之後是旁白：放進 PPT 備忘稿，並轉成語音與字幕。約每分鐘 260–300 字。

## 重新產生

```bash
python -I build_slides.py            # PPT + 語音 + 字幕 + 影片
python -I build_slides.py --pptx-only # 只產生 PPT（改版面時用，快很多）
```

流程：解析 slides.md → mermaid-cli 畫圖 → python-pptx 產生 16:9 PPT（逐字稿放備忘稿）→ PowerPoint 匯出每頁 1920×1080 圖片 → edge-tts 產生每頁語音 → ffmpeg 把每頁放在畫面上方 1600×900、下方深色字幕帶，合成 1080p MP4 並燒入字幕。每頁停留時間 = 0.4 秒 + 語音長度 + 0.7 秒。中間檔放在 `.out/`。

字幕時間是依每句字數在該頁語音長度內等比例分配，不是逐字對齊；同時輸出 `.srt`，上傳 YouTube 時可以另外附上。

## 可選的語音

`zh-TW-HsiaoChenNeural`（女，預設）、`zh-TW-HsiaoYuNeural`（女）、`zh-TW-YunJheNeural`（男）。改 slides.md 的 `voice:` 即可。edge-tts 使用微軟 Edge 的線上朗讀服務，產生語音時需要連網。

## 需要

- Python 套件：`python-pptx`、`edge-tts`、`imageio-ffmpeg`（內含 ffmpeg）、`Pillow`
- Node.js（`npx` 會下載 `@mermaid-js/mermaid-cli`）、Google Chrome
- Microsoft PowerPoint（匯出投影片圖片）
