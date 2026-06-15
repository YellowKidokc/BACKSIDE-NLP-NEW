param(
  [string]$InputPath = ""
)

$ErrorActionPreference = "Stop"
$workflowRoot = Split-Path -Parent $PSScriptRoot
$packet = Join-Path $workflowRoot "BACKSIDE\JUNKET\moved_20260516-222941\05_WORKFLOW_RUNS\workflow-packets\GTQArticlePublicRefinery"
$script = Join-Path $packet "SCRIPTS\run_refinery.py"
$defaultArticle = "\\dlowenas\HPWorkstation\Desktop\Hero Tempalte bigger\articles\03-first-quantum-state\gtq-03-first-quantum-state.html"
$logRoot = Join-Path $packet "LOGS"
$statusPath = Join-Path $workflowRoot "_state\PUBLIC_ARTICLE_REFINERY_STATUS.md"

New-Item -ItemType Directory -Path $logRoot -Force | Out-Null
New-Item -ItemType Directory -Path (Split-Path -Parent $statusPath) -Force | Out-Null

if ([string]::IsNullOrWhiteSpace($InputPath)) {
  Write-Host ""
  Write-Host "Public Article Refinery" -ForegroundColor Cyan
  Write-Host "Paste an HTML file or folder path, or press Enter for the GTQ-03 canary." -ForegroundColor Gray
  $typed = Read-Host "Path"
  if ([string]::IsNullOrWhiteSpace($typed)) { $InputPath = $defaultArticle } else { $InputPath = $typed.Trim('"') }
}

if (-not (Test-Path -LiteralPath $InputPath)) {
  Write-Host "Input path not found:" -ForegroundColor Red
  Write-Host $InputPath
  exit 2
}
if (-not (Test-Path -LiteralPath $script)) {
  Write-Host "Refinery script not found:" -ForegroundColor Red
  Write-Host $script
  exit 3
}

$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$logFile = Join-Path $logRoot "public_article_refinery_$stamp.log"
$output = Join-Path $packet "OUTPUT"
$review = Join-Path $packet "REVIEW"

& python $script --input $InputPath --output $output --review $review 2>&1 | Tee-Object -FilePath $logFile
$code = $LASTEXITCODE
$summary = Join-Path $output "last_run_summary.json"
$status = if ($code -eq 0 -and (Test-Path -LiteralPath $summary)) { "PASS" } else { "FAIL" }

Set-Content -LiteralPath $statusPath -Encoding UTF8 -Value @"
# Public Article Refinery Status

Updated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
Status: $status
Input: $InputPath
Output: $output
Review: $review
Log: $logFile
Exit code: $code
"@

Write-Host "Status: $status"
Write-Host "Status file: $statusPath"
exit $code
