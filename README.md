# Fin.Agentian Claude Skills

Agent skills for [Claude Code](https://claude.com/claude-code) and other agents that read `SKILL.md`.

| Skill | What it does |
|---|---|
| [ai-short-film](skills/ai-short-film/) | Produce a short AI film end to end — script, storyboard as data, character/location lock, image-to-video, edit, sound, QC, delivery — with client sign-off gates before any expensive generation. Includes a tested local Apple Silicon toolchain (FLUX.2-klein, MiniMax H3, LTX-2.5, Music3, Kokoro, Whisper, ffmpeg) and a clip QC script. |
| [excel-live-formulas](skills/excel-live-formulas/) | Every computed number in an Excel workbook is written as a formula — totals, shares, ranks, COUNTIFS/SUMIFS over a raw-data table, distinct counts — and verified by recalculating. Also retrofits existing workbooks: scan → propose → user picks → write → verify. |

## Install

```bash
git clone https://github.com/Fin-Agentian/claude-skills.git
cp -r claude-skills/skills/excel-live-formulas ~/.claude/skills/
cp -r claude-skills/skills/ai-short-film ~/.claude/skills/
```

Claude Code picks each skill up automatically when the task matches it: `excel-live-formulas`
when it is about to create or edit an `.xlsx`, and `ai-short-film` when you ask for an AI video.
You can also call them directly: `/excel-live-formulas`, `/ai-short-film`.

## Requirements (excel-live-formulas)

- Python 3.9+ with `openpyxl`
- LibreOffice Calc (headless) for recalculation and verification — `apt install libreoffice-calc`,
  `brew install --cask libreoffice`, or the Windows installer
- Optional: Microsoft Excel on Windows for `excel_recalc.ps1`

## Requirements (ai-short-film)

- ffmpeg/ffprobe on PATH for `scripts/qc_sheet.py` (Python 3.9+, no other packages)
- The local toolchain in `references/local-mac-toolchain.md` is optional; the workflow, gates and
  templates apply to cloud tools too

## 中文說明

**ai-short-film**：用 AI 做短片（廣告、微電影、比賽作品）的完整流程，從一次真實的 60 秒製作蒸餾而來。

- **先鎖樣子再生成**：G0 需求與規則 → G1 劇本 → G2 畫風、角色定妝、場景 → G3 動態預覽 → G4 粗剪，每一關都要委託人確認才往下，避免生成好幾個小時後才換風格。
- **寫模型做得到的故事**：避開可讀文字、精確數量、兩人交遞、大遠景多人、走向鏡頭；一鏡一動作一運鏡。
- **資料化分鏡**：生成層（gens）和剪輯層（shots）兩份 JSON，一段素材可剪成多個鏡頭。
- **QC 與剪輯**：`qc_sheet.py` 產生聯絡表並找出片段中途換構圖；ffmpeg 字幕（不需 libass）、室內底噪、配樂躲對白、−16 LUFS。
- **本機 Mac 工具鏈**：FLUX.2-klein、MiniMax H3、LTX-2.5、Music3、Kokoro、Whisper 的實測參數與速度。


**excel-live-formulas**：讓 AI 做出來的 Excel 是「真正能計算的表」。

- **製作 Excel 時自動套用**：合計、得票率、名次、依日期或分類的計數加總、不重複人數等計算值，一律寫成公式。原始資料放在獨立的 Excel 表格，參數放在黃底格。完成後用 LibreOffice 重算，逐格和預期值比對。
- **回填既有 Excel**：先掃描寫死的計算值並列出規劃，由使用者勾選、新增或略過，再寫入公式，最後重算驗證結果和原本的值一致。

## License

MIT
