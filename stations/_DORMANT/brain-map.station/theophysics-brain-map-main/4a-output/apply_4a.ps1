param(
  [string]$XRoot = "X:\",
  [switch]$Apply
)

$ErrorActionPreference = "Stop"

$ArtifactRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$Mode = if ($Apply) { "APPLY" } else { "DRY-RUN" }
$ReportRows = New-Object System.Collections.Generic.List[string]
$PlannedDirectories = New-Object System.Collections.Generic.HashSet[string]

function Add-Report {
  param(
    [string]$Status,
    [string]$Action,
    [string]$Detail
  )
  $line = "| $Status | $Action | $($Detail -replace '\|','\|') |"
  $ReportRows.Add($line) | Out-Null
  Write-Host "[$Status] $Action - $Detail"
}

function Ensure-Directory {
  param([string]$Path)
  if (Test-Path -LiteralPath $Path) {
    return
  }
  if (-not $Apply -and $PlannedDirectories.Contains($Path)) {
    return
  }
  $PlannedDirectories.Add($Path) | Out-Null
  Add-Report "PLAN" "create-directory" $Path
  if ($Apply) {
    New-Item -ItemType Directory -Path $Path -Force | Out-Null
  }
}

function Copy-GeneratedFile {
  param(
    [string]$Source,
    [string]$Destination
  )
  if (-not (Test-Path -LiteralPath $Source)) {
    Add-Report "SKIP" "missing-generated-file" $Source
    return
  }
  $parent = Split-Path -Parent $Destination
  Ensure-Directory $parent
  Add-Report "PLAN" "copy-file" "$Source -> $Destination"
  if ($Apply) {
    Copy-Item -LiteralPath $Source -Destination $Destination -Force
  }
}

function New-Junction {
  param(
    [string]$Path,
    [string]$Target
  )
  Add-Report "PLAN" "create-junction" "$Path -> $Target"
  if ($Apply) {
    $result = cmd /c mklink /J "$Path" "$Target" 2>&1
    if ($LASTEXITCODE -ne 0) {
      throw "mklink failed for $Path -> $Target`n$result"
    }
  }
}

function Move-LegacyIntakeToDrop {
  param(
    [string]$Workflow,
    [string]$LegacyName
  )

  $workflowRoot = Join-Path $XRoot $Workflow
  $drop = Join-Path $workflowRoot "00_DROP"
  $legacy = Join-Path $workflowRoot $LegacyName

  if (-not (Test-Path -LiteralPath $workflowRoot)) {
    Add-Report "FAIL" "missing-workflow-root" $workflowRoot
    return
  }

  Ensure-Directory $drop

  if (-not (Test-Path -LiteralPath $legacy)) {
    New-Junction $legacy $drop
    return
  }

  $legacyItem = Get-Item -LiteralPath $legacy -Force
  if ($legacyItem.LinkType -eq "Junction" -or $legacyItem.LinkType -eq "SymbolicLink") {
    Add-Report "OK" "legacy-already-link" "$legacy -> $($legacyItem.Target)"
    return
  }

  if (-not $legacyItem.PSIsContainer) {
    Add-Report "FAIL" "legacy-path-not-directory" $legacy
    return
  }

  $conflictRoot = Join-Path $workflowRoot ("ARCHIVE\4a_migration_conflicts_$Stamp\$LegacyName")
  $children = @(Get-ChildItem -LiteralPath $legacy -Force)

  foreach ($child in $children) {
    $destination = Join-Path $drop $child.Name
    if (Test-Path -LiteralPath $destination) {
      Ensure-Directory $conflictRoot
      $conflictDestination = Join-Path $conflictRoot $child.Name
      Add-Report "PLAN" "move-conflict-to-archive" "$($child.FullName) -> $conflictDestination"
      if ($Apply) {
        Move-Item -LiteralPath $child.FullName -Destination $conflictDestination
      }
    } else {
      Add-Report "PLAN" "move-legacy-child-to-00_DROP" "$($child.FullName) -> $destination"
      if ($Apply) {
        Move-Item -LiteralPath $child.FullName -Destination $destination
      }
    }
  }

  $preserved = Join-Path $workflowRoot "$LegacyName.PRE_4A_MIGRATION_$Stamp"
  Add-Report "PLAN" "preserve-empty-legacy-folder" "$legacy -> $preserved"
  if ($Apply) {
    Rename-Item -LiteralPath $legacy -NewName (Split-Path -Leaf $preserved)
  }

  New-Junction $legacy $drop
}

Write-Host "4a rollout mode: $Mode"
Write-Host "Artifact root: $ArtifactRoot"
Write-Host "X root: $XRoot"
Write-Host ""

$readmeFolders = @(
  "C4C", "C4C-wiki", "captures", "digests", "embeddings", "FAP", "github",
  "link-pull-drop", "models", "ollama", "proof-architecture", "proof-explorer",
  "ratings", "session-handoff-drop", "theophysics-comms-hub"
)

foreach ($folder in $readmeFolders) {
  Copy-GeneratedFile `
    (Join-Path $ArtifactRoot "$folder\README.md") `
    (Join-Path $XRoot "$folder\README.md")
}

$activeWorkflows = @(
  "axioms", "knowledge-refinery", "paper-proof-grader", "link-pull-drop",
  "session-handoff-drop", "ai-portal-generator", "ollama"
)

foreach ($workflow in $activeWorkflows) {
  $sourceBase = Join-Path $ArtifactRoot $workflow
  $destinationBase = Join-Path $XRoot $workflow

  if (-not (Test-Path -LiteralPath $destinationBase)) {
    Add-Report "FAIL" "missing-workflow-root" $destinationBase
    continue
  }

  Copy-GeneratedFile (Join-Path $sourceBase "_AGENT_BRIEF.md") (Join-Path $destinationBase "_AGENT_BRIEF.md")
  Copy-GeneratedFile (Join-Path $sourceBase "RUN_AGENT.bat") (Join-Path $destinationBase "RUN_AGENT.bat")
  Copy-GeneratedFile (Join-Path $sourceBase "health_check.bat") (Join-Path $destinationBase "health_check.bat")
  Ensure-Directory (Join-Path $destinationBase "prompts")
  Copy-GeneratedFile (Join-Path $sourceBase "prompts\.gitkeep") (Join-Path $destinationBase "prompts\.gitkeep")
}

$intakeMaps = @(
  @{ Workflow = "axioms"; LegacyName = "00_INBOX_DROP_PAPERS_HERE" },
  @{ Workflow = "knowledge-refinery"; LegacyName = "00_INTAKE" },
  @{ Workflow = "paper-proof-grader"; LegacyName = "INPUT" },
  @{ Workflow = "paper-proof-grader"; LegacyName = "DROP_PAPERS_HERE" },
  @{ Workflow = "session-handoff-drop"; LegacyName = "DROP_HERE" }
)

foreach ($map in $intakeMaps) {
  Move-LegacyIntakeToDrop $map.Workflow $map.LegacyName
}

$reportDir = Join-Path $XRoot "_LOGS"
if (-not (Test-Path -LiteralPath $reportDir)) {
  $reportDir = $ArtifactRoot
}
$reportPath = Join-Path $reportDir "prompt_4a_apply_report_$Stamp.md"
$report = @(
  "# 4a Apply Report",
  "",
  "- Mode: $Mode",
  "- Generated: $(Get-Date -Format s)",
  "- Artifact root: ``$ArtifactRoot``",
  "- X root: ``$XRoot``",
  "",
  "| Status | Action | Detail |",
  "|---|---|---|"
) + $ReportRows

Add-Report "PLAN" "write-report" $reportPath
if ($Apply) {
  $report | Set-Content -LiteralPath $reportPath -Encoding UTF8
} else {
  $localReport = Join-Path $ArtifactRoot "prompt_4a_apply_report_DRY_RUN_$Stamp.md"
  $report | Set-Content -LiteralPath $localReport -Encoding UTF8
  Write-Host ""
  Write-Host "Dry-run report: $localReport"
}

if (-not $Apply) {
  Write-Host ""
  Write-Host "Dry run only. Re-run with -Apply after reviewing the plan."
}
