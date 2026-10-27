---
name: excel-live-formulas
description: Build Excel workbooks that stay live. Whenever Claude writes an .xlsx (openpyxl, pandas, any script), every derived number — totals, subtotals, shares, ranks, per-category counts and sums, distinct counts, lookups — is written as an Excel formula over input cells instead of a pasted value; raw data goes in its own sheet as an Excel Table and parameters go in highlighted cells. Also retrofits existing workbooks: scans for hard-coded computed values, proposes formulas, lets the user pick, writes them, and verifies by recalculating.
when_to_use: excel, xlsx, spreadsheet, workbook, openpyxl, pandas to_excel, report in Excel, export to Excel, 試算表, 報表, Excel 報表, 匯出 Excel, 做成 Excel, 公式, 回填公式, Excel 公式, 計算公式, 表格要能計算
---

# excel-live-formulas — every computed number is a formula

A workbook is a calculator, not a screenshot. If a number can be derived from other cells,
write the formula, so the reader can change an input and watch the result follow.

## Mode A — creating a workbook (default; no need to ask)

Apply these rules every time you produce an .xlsx, without being asked:

1. **Separate inputs from results.**
   - Raw records → their own sheet, written as an Excel Table (`openpyxl.worksheet.table.Table`),
     so formulas use structured references (`Votes[Team]`) and grow with the data.
   - Parameters (dates, thresholds, rates, targets) → one labelled cell each, filled light yellow
     (`FFF2CC`). A header cell can be the parameter itself (a real date with number format `m/d "votes"`).
   - Labels and external facts that cannot be recomputed in the workbook stay as values.
2. **Classify every number you are about to write** with the table below. Anything in the left
   column becomes a formula referencing inputs — never a value computed in Python.
3. **Keep Python's numbers as the expected values.** Compute the same results in the script and dump
   them to `expected.json` (`{"sheet": "...", "cells": {"G5": 111, ...}}`).
4. **Verify** with `scripts/recalc_verify.py book.xlsx expected.json --keep book.recalc.xlsx`
   (headless LibreOffice): 0 formula errors and 0 mismatches are required.
5. **Deliver the recalculated copy** (`--keep` output). openpyxl files carry no cached values, so phone
   and mail previews would show blanks; the recalculated copy keeps the formulas *and* the values.
   If LibreOffice is unavailable, set `wb.calculation.fullCalcOnLoad = True` and say previews may be blank.
6. **Report** in one line: formula cells written, verification result, which cells are parameters.

| Derived value | Formula pattern |
|---|---|
| Row / column total, subtotal | `=SUM(E5:E15)`, `=E5+F5` |
| Difference, growth | `=C5-B5`, `=IF(B5=0,0,C5/B5-1)` |
| Share of total, percentage | `=IF($G$16=0,0,G5/$G$16)` + number format `0.0%` |
| Rank (ties share a rank) | `=RANK(G5,$G$5:$G$15)` |
| Count / sum by category or date | `=COUNTIFS(T[Date],E$4,T[Team],$B5)`, `=SUMIFS(T[Amount],T[Team],$B5)` |
| Distinct count | `=SUMPRODUCT(1/COUNTIF(T[Phone],T[Phone]))`; per group: `=SUMPRODUCT((T[Date]=E$4)/COUNTIFS(T[Phone],T[Phone],T[Date],T[Date]))` |
| Lookup by key | `=INDEX(T[Name],MATCH($B5,T[Id],0))&""` (text; `&""` keeps a blank source blank instead of 0); numbers/dates without `&""` |
| Average, min, max | `=AVERAGE(...)`, `=AVERAGEIFS(...)`, `=MAXIFS(...)` |
| Number with a unit ("272 people", "NT$ 1,200") | store the number/formula; unit via number format `0 "people"`, `"NT$ "#,##0` |
| Label built from a parameter | `=TEXT(E$4,"m/d")&" (Sat)"` |
| Tax, discount, instalments | `=ROUND(G5/1.05,0)`, `=G5-H5`; last instalment `=Total-SUM(others)` |
| Chart data | point the chart at the formula cells; it updates by itself |

## Mode B — retrofitting an existing workbook (the user asks to "add formulas")

1. **Scan**: `python3 scripts/audit_hardcoded.py book.xlsx --json candidates.json`. It finds column
   totals, row totals, shares, ranks and numbers hidden in text. Then read the workbook yourself for
   what a scanner cannot see: values that came from raw data that is not in the workbook (counts per
   category, distinct counts) and constants that should become parameters (dates, rates).
2. **Plan**: show a table — cell range, current content, proposed formula — one row per group.
3. **Ask**: `AskUserQuestion` with `multiSelect: true`, one option per group (recommended ones first,
   marked "(Recommended)"); the user can tick, add their own via "Other", or skip. If a group needs data
   that is not in the workbook (e.g. counts from raw records), offer to add a raw-data sheet.
4. **Write** the chosen formulas (and raw-data sheet / parameter cells) on a copy; never overwrite the
   original until verification passes.
5. **Verify** with `recalc_verify.py` using the old values as `expected.json` — the formulas must
   reproduce what was there. Then deliver the recalculated copy and report as in Mode A.

## Pitfalls

- **Codes that look like numbers** ("04", ZIP codes, IDs): write them as text with number format `@`
  on both sides of a COUNTIFS/MATCH, or they turn into 4 and stop matching.
- **Compatibility**: prefer functions that work in Excel 2016+ and LibreOffice — `SUMPRODUCT`,
  `COUNTIFS`, `INDEX/MATCH`, `RANK`. Avoid `XLOOKUP`, `UNIQUE`, `FILTER`, `LET`, `LAMBDA` unless the user
  is on Microsoft 365 (`recalc_verify.py` will flag them as `#NAME?` in older LibreOffice).
- **Dates**: write real `date` objects, not strings, or COUNTIFS on dates silently returns 0.
- **Division**: guard every ratio against a zero total with `IF`.
- **Sort order is static**: formulas update ranks, but rows do not re-sort; say so if order matters.
- **Do not round in Python** before writing — keep full precision in data, round with number formats.
- Formula strings in openpyxl use English function names and commas, regardless of the user's locale.
- openpyxl's `ws.append([])` does not advance `ws.max_row`; compute row numbers explicitly
  (`TOT + 2`) before writing formulas that point at them — verification catches the off-by-one.

## Files

- `scripts/recalc_verify.py` — recalculate with headless LibreOffice, list formula errors, compare with
  expected values; `--keep` saves the recalculated copy to deliver.
- `scripts/audit_hardcoded.py` — Mode B scanner for hard-coded computed values.
- `scripts/excel_recalc.ps1` — optional: recalculate in Microsoft Excel on Windows (`-Save` stores values).
- `examples/build_report.py` — a complete Mode A example (raw-data table, parameters, COUNTIFS,
  distinct counts, RANK, shares, chart, expected values).
