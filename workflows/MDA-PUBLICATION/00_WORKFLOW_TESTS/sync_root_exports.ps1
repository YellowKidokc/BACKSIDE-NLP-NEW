param(
  [string]$Root = "X:\WORKFLOWS\MDA-PUBLICATION",
  [string]$DeployPacket = "X:\WORKFLOWS\MDA-PUBLICATION\08_DEPLOY_READY\merged-styled-reader-20260601-175431"
)

$ErrorActionPreference = "Stop"

function Ensure-Dir {
  param([string]$Path)
  New-Item -ItemType Directory -Force -Path $Path | Out-Null
}

function Clear-Dir {
  param([string]$Path)
  Ensure-Dir $Path
  Assert-UnderExportRoot $Path
  Get-ChildItem -LiteralPath $Path -Force -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -notin @(".gitkeep") } |
    Remove-Item -Recurse -Force
}

function Assert-UnderExportRoot {
  param([string]$Path)
  $resolved = (Resolve-Path -LiteralPath $Path).Path.TrimEnd("\")
  if (-not (
    $resolved.Equals($script:exportRootResolved, [System.StringComparison]::OrdinalIgnoreCase) -or
    $resolved.StartsWith($script:exportRootResolved + "\", [System.StringComparison]::OrdinalIgnoreCase)
  )) {
    throw "Refusing to clear path outside export root: $resolved"
  }
}

function Copy-Files {
  param(
    [string]$Source,
    [string]$Destination,
    [string]$Filter = "*",
    [switch]$Recurse
  )
  Ensure-Dir $Destination
  if (-not (Test-Path -LiteralPath $Source)) { return 0 }
  $items = Get-ChildItem -LiteralPath $Source -File -Filter $Filter -Force -ErrorAction SilentlyContinue
  if ($Recurse) {
    $items = Get-ChildItem -LiteralPath $Source -File -Filter $Filter -Recurse -Force -ErrorAction SilentlyContinue
  }
  $copied = 0
  foreach ($item in $items) {
    if ($item.Name.StartsWith("~$")) { continue }
    if (($item.Attributes -band [IO.FileAttributes]::Hidden) -ne 0) { continue }
    if ($Recurse) {
      $rootPath = (Resolve-Path -LiteralPath $Source).Path
      $relative = $item.FullName.Substring($rootPath.Length).TrimStart("\")
      $target = Join-Path $Destination $relative
      Ensure-Dir ([IO.Path]::GetDirectoryName($target))
    } else {
      $target = Join-Path $Destination $item.Name
    }
    Copy-Item -LiteralPath $item.FullName -Destination $target -Force
    $copied += 1
  }
  return $copied
}

function Get-Stem {
  param([string]$FileName)
  [IO.Path]::GetFileNameWithoutExtension($FileName)
}

$exportRoot = Join-Path $Root "EXPORTS"
$script:exportRootResolved = (Resolve-Path -LiteralPath $exportRoot).Path.TrimEnd("\")
$control = Join-Path $exportRoot "00_CONTROL"
$sourceOut = Join-Path $exportRoot "01_SOURCE_SPINE\articles"
$readingOut = Join-Path $exportRoot "02_READING_LEVELS"
$reportsOut = Join-Path $exportRoot "03_TWO_LANE_REPORTS"
$htmlOut = Join-Path $exportRoot "04_READER_HTML"
$deployOut = Join-Path $exportRoot "05_DEPLOY_PACKET"
$analyticsOut = Join-Path $exportRoot "06_ANALYTICS"
$lexiconOut = Join-Path $exportRoot "07_LEXICON_MAPS"
$runbooksOut = Join-Path $exportRoot "08_RUNBOOKS"
$nonManifestOut = Join-Path $control "non_manifest"

foreach ($dir in @($control, $sourceOut, $readingOut, $reportsOut, $htmlOut, $deployOut, $analyticsOut, $lexiconOut, $runbooksOut, $nonManifestOut)) {
  Ensure-Dir $dir
}

$manifestPath = Join-Path $Root "MANIFEST.json"
if (-not (Test-Path -LiteralPath $manifestPath)) {
  throw "Missing manifest: $manifestPath"
}

$manifest = Get-Content -Raw -LiteralPath $manifestPath | ConvertFrom-Json
$articleStems = @($manifest.articles | ForEach-Object { Get-Stem $_.file })

Clear-Dir $sourceOut
Clear-Dir $readingOut
Clear-Dir $reportsOut
Clear-Dir $htmlOut
Clear-Dir $deployOut
Clear-Dir $analyticsOut
Clear-Dir $runbooksOut
Clear-Dir $nonManifestOut
Ensure-Dir $lexiconOut

Copy-Item -LiteralPath (Join-Path $Root "WORKFLOW.md") -Destination (Join-Path $control "WORKFLOW.md") -Force
Copy-Item -LiteralPath $manifestPath -Destination (Join-Path $control "MANIFEST.json") -Force
Copy-Item -LiteralPath (Join-Path $Root "00_WORKFLOW_TESTS\MDA_WORKFLOW_APP_CONTRACT_20260602.md") -Destination (Join-Path $control "MDA_WORKFLOW_APP_CONTRACT_20260602.md") -Force
Copy-Item -LiteralPath (Join-Path $Root "00_WORKFLOW_TESTS\STATION_QUEUE_20260602.md") -Destination (Join-Path $control "STATION_QUEUE_20260602.md") -Force
Copy-Item -LiteralPath (Join-Path $Root "00_WORKFLOW_TESTS\TWO_COMMAND_LINE_SPLIT_20260603.md") -Destination (Join-Path $control "TWO_COMMAND_LINE_SPLIT_20260603.md") -Force

$latestHarness = Get-ChildItem -LiteralPath (Join-Path $Root "00_WORKFLOW_TESTS") -File -Filter "workflow_test_results_*.md" |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 1
if ($latestHarness) {
  Copy-Item -LiteralPath $latestHarness.FullName -Destination (Join-Path $control "LATEST_WORKFLOW_TEST_RESULTS.md") -Force
  $jsonTwin = [IO.Path]::ChangeExtension($latestHarness.FullName, ".json")
  if (Test-Path -LiteralPath $jsonTwin) {
    Copy-Item -LiteralPath $jsonTwin -Destination (Join-Path $control "LATEST_WORKFLOW_TEST_RESULTS.json") -Force
  }
}

$sourceCount = Copy-Files -Source (Join-Path $Root "01_LOSSLESS\articles") -Destination $sourceOut -Filter "*.md"
$readingCount = Copy-Files -Source (Join-Path $Root "05_READING_LEVELS") -Destination $readingOut -Filter "*"

$reportSource = Join-Path $Root "03_SCORED\openai\article-reports"
$reportCount = 0
$nonManifestReportCount = 0
if (Test-Path -LiteralPath $reportSource) {
  foreach ($report in Get-ChildItem -LiteralPath $reportSource -File -Filter "*_TWO_LANE_REPORT.md") {
    $stem = $report.BaseName -replace "_TWO_LANE_REPORT$", ""
    if ($stem -in $articleStems) {
      Copy-Item -LiteralPath $report.FullName -Destination (Join-Path $reportsOut $report.Name) -Force
      $reportCount += 1
    } else {
      Copy-Item -LiteralPath $report.FullName -Destination (Join-Path $nonManifestOut $report.Name) -Force
      $nonManifestReportCount += 1
    }
  }
}

$htmlCount = Copy-Files -Source (Join-Path $Root "06_HTML_BUILD\reader_combined") -Destination $htmlOut -Filter "*.html"
$deployCount = Copy-Files -Source $DeployPacket -Destination $deployOut -Filter "*" -Recurse

Ensure-Dir (Join-Path $analyticsOut "series-flow")
Ensure-Dir (Join-Path $analyticsOut "pipeline")
$seriesCount = Copy-Files -Source (Join-Path $Root "03_SCORED\series-flow") -Destination (Join-Path $analyticsOut "series-flow") -Filter "*"
$pipelineCount = Copy-Files -Source (Join-Path $Root "09_EXPORT_PACKET\06_PIPELINE_ANALYTICS") -Destination (Join-Path $analyticsOut "pipeline") -Filter "*" -Recurse
$paperRows = Join-Path $analyticsOut "pipeline\paper_rows.json"
if (Test-Path -LiteralPath $paperRows) {
  Copy-Item -LiteralPath $paperRows -Destination (Join-Path $analyticsOut "paper_rows.json") -Force
}

Copy-Item -LiteralPath (Join-Path $exportRoot "EXPORT_LEXICON.md") -Destination (Join-Path $lexiconOut "EXPORT_LEXICON.md") -Force
Copy-Files -Source (Join-Path $Root "00_WORKFLOW_TESTS") -Destination $runbooksOut -Filter "*.ps1" | Out-Null
Copy-Files -Source (Join-Path $Root "05_HTML_BUILD") -Destination $runbooksOut -Filter "*.py" | Out-Null
Copy-Files -Source (Join-Path $Root "READING_LEVEL_GENERATOR") -Destination $runbooksOut -Filter "*.py" | Out-Null
Copy-Files -Source (Join-Path $Root "READING_LEVEL_GENERATOR") -Destination $runbooksOut -Filter "*.ps1" | Out-Null
Copy-Files -Source (Join-Path $Root "READING_LEVEL_GENERATOR") -Destination $runbooksOut -Filter "*.bat" | Out-Null

$summary = [ordered]@{
  generated_at = (Get-Date).ToString("s")
  root = $Root
  export_root = $exportRoot
  manifest_articles = $articleStems.Count
  source_spine_articles = $sourceCount
  reading_files = $readingCount
  manifest_two_lane_reports = $reportCount
  non_manifest_reports = $nonManifestReportCount
  reader_html_files = $htmlCount
  deploy_packet_files = $deployCount
  series_flow_files = $seriesCount
  pipeline_files = $pipelineCount
}

$summary | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $exportRoot "EXPORT_SYNC_MANIFEST.json") -Encoding UTF8

$statusLines = @(
  "# Root Export Sync Status",
  "",
  "- Generated: $($summary.generated_at)",
  "- Manifest articles: $($summary.manifest_articles)",
  "- Source spine articles: $($summary.source_spine_articles)",
  "- Manifest two-lane reports: $($summary.manifest_two_lane_reports)",
  "- Non-manifest reports preserved: $($summary.non_manifest_reports)",
  "- Reader HTML files: $($summary.reader_html_files)",
  "- Deploy packet files: $($summary.deploy_packet_files)",
  "",
  "Judged surface: `EXPORTS`.",
  "Working station folders remain source-of-generation, not final judgment."
)
$statusLines | Set-Content -LiteralPath (Join-Path $exportRoot "CURRENT_STATUS.md") -Encoding UTF8

$summary | Format-List
