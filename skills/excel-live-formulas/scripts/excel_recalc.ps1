# Recalculate a workbook in Microsoft Excel (Windows) and print "Sheet!A1<TAB>value" for every formula cell.
# Usage: powershell -ExecutionPolicy Bypass -File excel_recalc.ps1 <full\path\book.xlsx> [-Save]
param([Parameter(Mandatory = $true)][string]$Path, [switch]$Save)
$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$xl = New-Object -ComObject Excel.Application
$xl.Visible = $false
$xl.DisplayAlerts = $false
try {
  $wb = $xl.Workbooks.Open($Path)
  $xl.CalculateFull()
  foreach ($ws in $wb.Worksheets) {
    $used = $ws.UsedRange
    foreach ($c in $used.Cells) {
      if ($c.HasFormula) { "{0}!{1}`t{2}" -f $ws.Name, $c.Address($false, $false), $c.Text }
    }
  }
  if ($Save) { $wb.Save() }  # stores calculated values so previewers (phone, mail) show numbers
  $wb.Close($false)
} finally {
  $xl.Quit()
  [System.Runtime.InteropServices.Marshal]::ReleaseComObject($xl) | Out-Null
}
