param(
  [string]$InputPath = ""
)

$ErrorActionPreference = "Stop"
$packet = "X:\knowledge-refinery\05_WORKFLOW_RUNS\workflow-packets\GTQArticlePublicRefinery"
$script = Join-Path $packet "SCRIPTS\run_refinery.py"
$defaultArticle = "\\dlowenas\HPWorkstation\Desktop\Hero Tempalte bigger\articles\03-first-quantum-state\gtq-03-first-quantum-state.html"
$logRoot = Join-Path $packet "LOGS"
$statusPath = "X:\knowledge-refinery\05_WORKFLOW_RUNS\PUBLIC_ARTICLE_REFINERY_STATUS.md"

New-Item -ItemType Directory -Path $logRoot -Force | Out-Null

if ([string]::IsNullOrWhiteSpace($InputPath)) {
  Write-Host ""
  Write-Host "Public Article Refinery" -ForegroundColor Cyan
  Write-Host "Paste an HTML file or folder path, or press Enter for the GTQ-03 canary." -ForegroundColor Gray
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

if (-not (Test-Path -LiteralPath $script)) {
  Write-Host "Refinery script not found:" -ForegroundColor Red
  Write-Host $script
  exit 3
}

$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$logFile = Join-Path $logRoot "public_article_refinery_$stamp.log"
$output = Join-Path $packet "OUTPUT"
$review = Join-Path $packet "REVIEW"

Write-Host ""
Write-Host "Running article refinery..." -ForegroundColor Cyan
Write-Host "Input:  $InputPath"
Write-Host "Output: $output"
Write-Host "Review: $review"
Write-Host ""

$arguments = @(
  $script,
  "--input", $InputPath,
  "--output", $output,
  "--review", $review
)

& python @arguments 2>&1 | Tee-Object -FilePath $logFile
$code = $LASTEXITCODE

$summary = Join-Path $output "last_run_summary.json"
$status = if ($code -eq 0 -and (Test-Path -LiteralPath $summary)) { "PASS" } else { "FAIL" }
$reviewTarget = ""

if (Test-Path -LiteralPath $summary) {
  try {
    $json = Get-Content -Raw -LiteralPath $summary | ConvertFrom-Json
    if ($json.results.Count -gt 0) {
      $reviewTarget = $json.results[0].review
    }
  } catch {
    $reviewTarget = ""
  }
}

$statusText = @"
# Public Article Refinery Status

Updated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

Status: $status

Input:

```text
$InputPath
```

Summary:

```text
$summary
```

Review:

```text
$reviewTarget
```

Log:

```text
$logFile
```

Exit code: $code
"@

Set-Content -LiteralPath $statusPath -Value $statusText -Encoding UTF8

Write-Host ""
Write-Host "Status: $status" -ForegroundColor $(if ($status -eq "PASS") { "Green" } else { "Red" })
Write-Host "Status file: $statusPath"
Write-Host "Log file:    $logFile"

if ($reviewTarget -and (Test-Path -LiteralPath $reviewTarget)) {
  Write-Host "Opening review folder..." -ForegroundColor Cyan
  Start-Process explorer.exe $reviewTarget
}

exit $code
