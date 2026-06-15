param(
  [string]$InputPath = "",
  [switch]$SkipPaperGrader
)

$ErrorActionPreference = "Stop"
$packet = "X:\knowledge-refinery\05_WORKFLOW_RUNS\workflow-packets\FolderAutomationPipeline"
$script = Join-Path $packet "SCRIPTS\run_article_manufacturing_line.py"
$defaultArticle = "\\dlowenas\HPWorkstation\Desktop\Hero Tempalte bigger\articles\03-first-quantum-state\gtq-03-first-quantum-state.html"
$statusPath = "X:\knowledge-refinery\05_WORKFLOW_RUNS\FAP_ARTICLE_PIPELINE_STATUS.md"
$logRoot = Join-Path $packet "LOGS"
New-Item -ItemType Directory -Path $logRoot -Force | Out-Null

if ([string]::IsNullOrWhiteSpace($InputPath)) {
  Write-Host ""
  Write-Host "FAP Article Manufacturing Pipeline" -ForegroundColor Cyan
  Write-Host "Paste an HTML/MD/TXT file path, or press Enter for the GTQ-03 canary." -ForegroundColor Gray
  $typed = Read-Host "Path"
  if ([string]::IsNullOrWhiteSpace($typed)) {
    $InputPath = $defaultArticle
  } else {
    $InputPath = $typed.Trim('"')
  }
}

if (-not (Test-Path -LiteralPath $InputPath)) {
  Write-Host "Input path not found:" -ForegroundColor Red
  Write-Host $InputPath
  exit 2
}

$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$logFile = Join-Path $logRoot "fap_article_pipeline_$stamp.log"
$argsList = @($script, "--input", $InputPath)
if ($SkipPaperGrader) {
  $argsList += "--skip-paper-grader"
}

Write-Host ""
Write-Host "Running FAP manufacturing line..." -ForegroundColor Cyan
Write-Host "Input: $InputPath"
Write-Host ""

& python @argsList 2>&1 | Tee-Object -FilePath $logFile
$code = $LASTEXITCODE
$status = if ($code -eq 0) { "PASS" } else { "FAIL" }

$latest = Get-ChildItem -LiteralPath "X:\knowledge-refinery\13_SOURCE_SYSTEMS\FAP\output" -Directory -ErrorAction SilentlyContinue |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 1

$latestPath = if ($latest) { $latest.FullName } else { "" }
$manifestPath = if ($latest) { Join-Path $latest.FullName "job_manifest.json" } else { "" }

$statusText = @"
# FAP Article Pipeline Status

Updated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

Status: $status

Input: $InputPath

Latest output: $latestPath

Manifest: $manifestPath

Log: $logFile

Exit code: $code
"@

Set-Content -LiteralPath $statusPath -Value $statusText -Encoding UTF8

Write-Host ""
Write-Host "Status: $status" -ForegroundColor $(if ($status -eq "PASS") { "Green" } else { "Red" })
Write-Host "Status file: $statusPath"
Write-Host "Log file:    $logFile"

if ($latestPath -and (Test-Path -LiteralPath $latestPath)) {
  Start-Process explorer.exe $latestPath
}

exit $code
