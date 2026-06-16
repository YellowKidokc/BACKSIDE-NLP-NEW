param(
  [string]$Root = "X:\WORKFLOWS\MDA-PUBLICATION",
  [string]$DeployPacket = "X:\WORKFLOWS\MDA-PUBLICATION\08_DEPLOY_READY\merged-styled-reader-20260601-175431"
)

$ErrorActionPreference = "Stop"

function New-Result {
  param(
    [string]$Station,
    [string]$Check,
    [string]$Status,
    [string]$Detail
  )
  [pscustomobject]@{
    station = $Station
    check = $Check
    status = $Status
    detail = $Detail
  }
}

function Add-Result {
  param(
    [string]$Station,
    [string]$Check,
    [string]$Status,
    [string]$Detail
  )
  $script:results += New-Result -Station $Station -Check $Check -Status $Status -Detail $Detail
}

function Get-Stem {
  param([string]$FileName)
  [System.IO.Path]::GetFileNameWithoutExtension($FileName)
}

$script:results = @()
$manifestPath = Join-Path $Root "MANIFEST.json"

if (-not (Test-Path -LiteralPath $manifestPath)) {
  throw "Missing MANIFEST.json at $manifestPath"
}

$manifest = Get-Content -Raw -LiteralPath $manifestPath | ConvertFrom-Json
$articles = @($manifest.articles)
$articleStems = @($articles | ForEach-Object { Get-Stem $_.file })

$losslessDir = Join-Path $Root "01_LOSSLESS\articles"
$losslessFiles = @(Get-ChildItem -LiteralPath $losslessDir -File -Filter "*.md" -ErrorAction SilentlyContinue)
$losslessStems = @($losslessFiles | ForEach-Object { $_.BaseName })
$missingLossless = @($articleStems | Where-Object { $_ -notin $losslessStems })
$extraLossless = @($losslessStems | Where-Object { $_ -notin $articleStems })
Add-Result "01_LOSSLESS" "manifest_count_match" $(if ($missingLossless.Count -eq 0 -and $extraLossless.Count -eq 0) { "PASS" } else { "FAIL" }) "manifest=$($articles.Count); lossless_md=$($losslessFiles.Count); missing=[$($missingLossless -join ', ')]; extra=[$($extraLossless -join ', ')]"

$expectedByType = @{
  narrative = 19
  mechanism = 17
  mathematical = 5
  empirical = 8
  resolution = 5
  appendix = 7
}

$classifiedDir = Join-Path $Root "02_CLASSIFIED"
$classificationIssues = New-Object System.Collections.Generic.List[string]
foreach ($type in $expectedByType.Keys) {
  $typeDir = Join-Path $classifiedDir $type
  $files = @(Get-ChildItem -LiteralPath $typeDir -File -Filter "*.md" -ErrorAction SilentlyContinue)
  if ($files.Count -ne $expectedByType[$type]) {
    $classificationIssues.Add("$type expected=$($expectedByType[$type]) actual=$($files.Count)")
  }
}
$classifiedFiles = @(Get-ChildItem -LiteralPath $classifiedDir -Recurse -File -Filter "*.md" -ErrorAction SilentlyContinue)
$classifiedStems = @($classifiedFiles | ForEach-Object { $_.BaseName })
$missingClassified = @($articleStems | Where-Object { $_ -notin $classifiedStems })
$extraClassified = @($classifiedStems | Where-Object { $_ -notin $articleStems })
if ($missingClassified.Count -gt 0) { $classificationIssues.Add("missing=[$($missingClassified -join ', ')]") }
if ($extraClassified.Count -gt 0) { $classificationIssues.Add("extra=[$($extraClassified -join ', ')]") }
Add-Result "02_CLASSIFIED" "type_counts_and_manifest_coverage" $(if ($classificationIssues.Count -eq 0) { "PASS" } else { "FAIL" }) "classified_md=$($classifiedFiles.Count); issues=[$($classificationIssues -join '; ')]"

$reportDir = Join-Path $Root "03_SCORED\openai\article-reports"
$reports = @(Get-ChildItem -LiteralPath $reportDir -File -Filter "*_TWO_LANE_REPORT.md" -ErrorAction SilentlyContinue)
$reportStems = @($reports | ForEach-Object { $_.BaseName -replace "_TWO_LANE_REPORT$", "" })
$missingReports = @($articleStems | Where-Object { $_ -notin $reportStems })
$extraReports = @($reportStems | Where-Object { $_ -notin $articleStems })
Add-Result "03_SCORED" "two_lane_report_coverage" $(if ($missingReports.Count -eq 0) { "PASS" } else { "FAIL" }) "reports=$($reports.Count); missing=[$($missingReports -join ', ')]; extra=[$($extraReports -join ', ')]"

$seriesFlow = $manifest.series_flow
$seriesStatus = "FAIL"
if ($seriesFlow.series_flow_scored -and ($seriesFlow.order_verdict -eq "pass" -or $seriesFlow.order_verdict -eq "waived")) {
  $seriesStatus = "PASS"
} elseif ($seriesFlow.series_flow_scored) {
  $seriesStatus = "REVIEW"
}
Add-Result "03_SCORED\series-flow" "hard_gate" $seriesStatus "verdict=$($seriesFlow.order_verdict); pass_ratio=$($seriesFlow.pass_ratio); required=$($seriesFlow.pass_ratio_required); flagged=$($seriesFlow.flagged_handoffs)"

$readingDir = Join-Path $Root "05_READING_LEVELS"
$easy = @(Get-ChildItem -LiteralPath $readingDir -File -Filter "*_EASY.md" -ErrorAction SilentlyContinue | ForEach-Object { $_.BaseName -replace "_EASY$", "" })
$academic = @(Get-ChildItem -LiteralPath $readingDir -File -Filter "*_ACADEMIC.md" -ErrorAction SilentlyContinue | ForEach-Object { $_.BaseName -replace "_ACADEMIC$", "" })
$terms = @(Get-ChildItem -LiteralPath $readingDir -File -Filter "*_TERM_INVENTORY.json" -ErrorAction SilentlyContinue | ForEach-Object { $_.BaseName -replace "_TERM_INVENTORY$", "" })
$missingEasy = @($articleStems | Where-Object { $_ -notin $easy })
$missingAcademic = @($articleStems | Where-Object { $_ -notin $academic })
$missingTerms = @($articleStems | Where-Object { $_ -notin $terms })
$readingStatus = if ($missingEasy.Count -eq 0 -and $missingAcademic.Count -eq 0 -and $missingTerms.Count -eq 0) { "PASS" } elseif ($missingAcademic.Count -eq 0 -and $missingTerms.Count -eq 0) { "REVIEW" } else { "FAIL" }
Add-Result "05_READING_LEVELS" "variant_coverage" $readingStatus "easy=$($easy.Count); academic=$($academic.Count); terms=$($terms.Count); missing_easy=[$($missingEasy -join ', ')]; missing_academic=[$($missingAcademic -join ', ')]; missing_terms=[$($missingTerms -join ', ')]"

$readerDir = Join-Path $Root "06_HTML_BUILD\reader_combined"
$readerHtml = @(Get-ChildItem -LiteralPath $readerDir -File -Filter "*.html" -ErrorAction SilentlyContinue)
$readerStems = @($readerHtml | Where-Object { $_.BaseName -ne "index" } | ForEach-Object { $_.BaseName })
$missingReader = @($articleStems | Where-Object { $_ -notin $readerStems })
Add-Result "06_HTML_BUILD" "reader_html_coverage" $(if ($missingReader.Count -eq 0) { "PASS" } else { "FAIL" }) "reader_html=$($readerHtml.Count); missing=[$($missingReader -join ', ')]"

$modeIssues = New-Object System.Collections.Generic.List[string]
foreach ($file in $readerHtml | Where-Object { $_.BaseName -ne "index" }) {
  $text = Get-Content -Raw -LiteralPath $file.FullName
  if ($text -notmatch 'data-mode="easy"' -or $text -notmatch 'data-mode="standard"' -or $text -notmatch 'data-mode="academic"' -or $text -notmatch 'data-mode="proof"') {
    $modeIssues.Add($file.Name)
  }
}
Add-Result "06_HTML_BUILD" "reader_mode_controls" $(if ($modeIssues.Count -eq 0) { "PASS" } else { "FAIL" }) "missing_controls=[$($modeIssues -join ', ')]"

if (Test-Path -LiteralPath $DeployPacket) {
  $deployHtml = @(Get-ChildItem -LiteralPath $DeployPacket -Recurse -File -Filter "*.html" -ErrorAction SilentlyContinue)
  $deployStems = @($deployHtml | ForEach-Object { $_.BaseName })
  $missingDeploy = @($articleStems | Where-Object { $_ -notin $deployStems })
  Add-Result "08_DEPLOY_READY" "manifest_page_coverage" $(if ($missingDeploy.Count -eq 0) { "PASS" } else { "FAIL" }) "deploy_html=$($deployHtml.Count); missing=[$($missingDeploy -join ', ')]"
} else {
  Add-Result "08_DEPLOY_READY" "manifest_page_coverage" "FAIL" "deploy packet not found: $DeployPacket"
}

$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$outJson = Join-Path $Root "00_WORKFLOW_TESTS\workflow_test_results_$timestamp.json"
$outMd = Join-Path $Root "00_WORKFLOW_TESTS\workflow_test_results_$timestamp.md"

$results | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $outJson -Encoding UTF8

$lines = New-Object System.Collections.Generic.List[string]
$lines.Add("# MDA Workflow Test Results")
$lines.Add("")
$lines.Add("Run: $timestamp")
$lines.Add("Root: ``$Root``")
$lines.Add("")
$lines.Add("| Station | Check | Status | Detail |")
$lines.Add("|---|---|---|---|")
foreach ($r in $results) {
  $detail = ($r.detail -replace "\|", "/")
  $lines.Add("| $($r.station) | $($r.check) | $($r.status) | $detail |")
}
$lines | Set-Content -LiteralPath $outMd -Encoding UTF8

$results | Format-Table -AutoSize
Write-Host ""
Write-Host "Wrote: $outJson"
Write-Host "Wrote: $outMd"
