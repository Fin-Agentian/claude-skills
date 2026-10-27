# Fin.Agentian Claude Skills

Agent skills for [Claude Code](https://claude.com/claude-code) and other agents that read `SKILL.md`.

| Skill | What it does |
|---|---|
| [excel-live-formulas](skills/excel-live-formulas/) | Every computed number in an Excel workbook is written as a formula — totals, shares, ranks, COUNTIFS/SUMIFS over a raw-data table, distinct counts — and verified by recalculating. Also retrofits existing workbooks: scan → propose → user picks → write → verify. |

## Install

```bash
git clone https://github.com/Fin-Agentian/claude-skills.git
cp -r claude-skills/skills/excel-live-formulas ~/.claude/skills/
```

Claude Code picks the skill up automatically whenever it is about to create or edit an `.xlsx`.
You can also call it directly: `/excel-live-formulas`.

## Requirements (excel-live-formulas)

- Python 3.9+ with `openpyxl`
- LibreOffice Calc (headless) for recalculation and verification — `apt install libreoffice-calc`,
  `brew install --cask libreoffice`, or the Windows installer
- Optional: Microsoft Excel on Windows for `excel_recalc.ps1`

## 中文說明

**excel-live-formulas**：讓 AI 做出來的 Excel 是「真正能計算的表」。

- **製作 Excel 時自動套用**：合計、得票率、名次、依日期或分類的計數加總、不重複人數等計算值，一律寫成公式。原始資料放在獨立的 Excel 表格，參數放在黃底格。完成後用 LibreOffice 重算，逐格和預期值比對。
- **回填既有 Excel**：先掃描寫死的計算值並列出規劃，由使用者勾選、新增或略過，再寫入公式，最後重算驗證結果和原本的值一致。

## License

MIT
