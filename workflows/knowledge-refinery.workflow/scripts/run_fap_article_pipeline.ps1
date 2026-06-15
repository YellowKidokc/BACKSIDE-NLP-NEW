param(
  [string]$InputPath = "",
  [switch]$SkipPaperGrader
)

$ErrorActionPreference = "Stop"
$workflowRoot = Split-Path -Parent $PSScriptRoot
$packet = Join-Path $workflowRoot "BACKSIDE\JUNKET\moved_20260516-222941\05_WORKFLOW_RUNS\workflow-packets\FolderAutomationPipeline"
$script = Join-Path $packet "SCRIPTS\run_article_manufacturing_line.py"
$defaultArticle = "\\dlowenas\HPWorkstation\Desktop\Hero Tempalte bigger\articles\03-first-quantum-state\gtq-03-first-quantum-state.html"
$logRoot = Join-Path $packet "LOGS"
$statusPath = Join-Path $workflowRoot "_state\FAP_ARTICLE_PIPELINE_STATUS.md"

New-Item -ItemType Directory -Path $logRoot -Force | Out-Null
New-Item -ItemType Directory -Path (Split-Path -Parent $statusPath) -Force | Out-Null

if ([string]::IsNullOrWhiteSpace($InputPath)) {
  Write-Host ""
  Write-Host "FAP Article Manufacturing Pipeline" -ForegroundColor Cyan
  Write-Host "Paste an HTML/MD/TXT file path, or press Enter for the GTQ-03 canary." -ForegroundColor Gray
  $typed = Read-Host "Path"
  if ([string]::IsNullOrWhiteSpace($typed)) { $InputPath = $defaultArticle } else { $InputPath = $typed.Trim('"') }
}

if (-not (Test-Path -LiteralPath $InputPath)) {
  Write-Host "Input path not found:" -ForegroundColor Red
  Write-Host $InputPath
  exit 2
}
if (-not (Test-Path -LiteralPath $script)) {
  Write-Host "FAP script not found:" -ForegroundColor Red
  Write-Host $script
  exit 3
}

$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$logFile = Join-Path $logRoot "fap_article_pipeline_$stamp.log"
$argsList = @($script, "--input", $InputPath)
if ($SkipPaperGrader) { $argsList += "--skip-paper-grader" }

& python @argsList 2>&1 | Tee-Object -FilePath $logFile
$code = $LASTEXITCODE
$status = if ($code -eq 0) { "PASS" } else { "FAIL" }
$latest = Get-ChildItem -LiteralPath (Join-Path $packet "output") -Directory -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1
$latestPath = if ($latest) { $latest.FullName } else { "" }
$manifestPath = if ($latest) { Join-Path $latest.FullName "job_manifest.json" } else { "" }

Set-Content -LiteralPath $statusPath -Encoding UTF8 -Value @"
# FAP Article Pipeline Status

Updated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
Status: $status
Input: $InputPath
Latest output: $latestPath
Manifest: $manifestPath
Log: $logFile
Exit code: $code
"@

Write-Host "Status: $status"
Write-Host "Status file: $statusPath"
exit $code
