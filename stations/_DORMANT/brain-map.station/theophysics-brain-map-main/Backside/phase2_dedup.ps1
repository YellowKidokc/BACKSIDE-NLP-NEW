$ErrorActionPreference = 'Continue'
$skipDirs = @('#recycle','_LOGS','embeddings','models','_brain_DEPRECATED_20260516','captures','digests')
$skipDirPattern = ($skipDirs | ForEach-Object { [regex]::Escape($_) }) -join '|'
$minSize = 1MB
$report = [System.Collections.ArrayList]@()

[void]$report.Add("# X:\ Dedup Report - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')")
[void]$report.Add("")
[void]$report.Add("Scope: files >= 1 MB on X:\, skipping churn dirs ($($skipDirs -join ', ')), Backside\archives, Backside\_ARCHIVE_*.")
[void]$report.Add("")

# Section 1: Within-X duplicates
[void]$report.Add("## Section 1: Within-X duplicates (size >= 1 MB)")
[void]$report.Add("")
$startTime = Get-Date
Write-Host "Scanning X:\ for files >= 1MB..."
$allFiles = Get-ChildItem -LiteralPath 'X:\' -Recurse -File -Force -ErrorAction SilentlyContinue |
  Where-Object {
    $_.Length -ge $minSize -and
    $_.FullName -notmatch "X:\\($skipDirPattern)\\" -and
    $_.FullName -notmatch 'X:\\Backside\\archives\\' -and
    $_.FullName -notmatch 'X:\\Backside\\_ARCHIVE_'
  }
Write-Host "Found $($allFiles.Count) files >= 1MB to hash"

$hashGroups = @{}
$i = 0
foreach ($f in $allFiles) {
  $i++
  if ($i % 200 -eq 0) { Write-Host "  hashing $i / $($allFiles.Count)..." }
  try {
    $h = (Get-FileHash -LiteralPath $f.FullName -Algorithm MD5 -ErrorAction Stop).Hash
    if (-not $hashGroups.ContainsKey($h)) { $hashGroups[$h] = [System.Collections.ArrayList]@() }
    [void]$hashGroups[$h].Add(@{Path=$f.FullName; Size=$f.Length; MTime=$f.LastWriteTime})
  } catch {
    # skip unreadable
  }
}
$dupGroups = @($hashGroups.GetEnumerator() | Where-Object { $_.Value.Count -ge 2 })
$elapsed = (Get-Date) - $startTime
Write-Host "Hashing done in $($elapsed.TotalMinutes.ToString('N1')) min. Duplicate groups: $($dupGroups.Count)"
[void]$report.Add("Files hashed: $($allFiles.Count)")
[void]$report.Add("Duplicate groups: $($dupGroups.Count)")
[void]$report.Add("")
if ($dupGroups.Count -gt 0) {
  $totalWaste = 0
  foreach ($g in $dupGroups) {
    $items = $g.Value
    $size = $items[0].Size
    $waste = $size * ($items.Count - 1)
    $totalWaste += $waste
    [void]$report.Add(("- {0} copies, {1:N1} MB each, {2:N1} MB recoverable:" -f $items.Count, ($size/1MB), ($waste/1MB)))
    foreach ($it in $items) {
      [void]$report.Add(("    {0}  ({1})" -f $it.Path, $it.MTime.ToString('yyyy-MM-dd HH:mm')))
    }
    [void]$report.Add("")
  }
  [void]$report.Add(("**Total recoverable space:** {0:N1} MB" -f ($totalWaste/1MB)))
} else {
  [void]$report.Add("No size-1MB+ duplicates found within X:\.")
}
[void]$report.Add("")

# Section 2: Folder name collisions
[void]$report.Add("## Section 2: Folder name collisions (same name, different paths)")
[void]$report.Add("")
Write-Host "Scanning for folder name collisions..."
$allDirs = Get-ChildItem -LiteralPath 'X:\' -Recurse -Directory -Force -ErrorAction SilentlyContinue |
  Where-Object {
    $_.FullName -notmatch "X:\\($skipDirPattern)\\" -and
    $_.FullName -notmatch 'X:\\Backside\\archives\\' -and
    $_.FullName -notmatch 'X:\\Backside\\_ARCHIVE_'
  }
$nameGroups = @($allDirs | Group-Object Name | Where-Object {
  $_.Count -ge 2 -and $_.Name -notmatch '^(\.git|__pycache__|node_modules|\.obsidian|\.vscode|stations)$'
})
Write-Host "Folder name groups with collisions: $($nameGroups.Count)"
[void]$report.Add("Folder name groups with >= 2 instances: $($nameGroups.Count)")
[void]$report.Add("")
foreach ($g in ($nameGroups | Sort-Object Count -Descending | Select-Object -First 30)) {
  [void]$report.Add(("- ``{0}`` x{1}:" -f $g.Name, $g.Count))
  foreach ($d in $g.Group) {
    [void]$report.Add(("    {0}" -f $d.FullName))
  }
  [void]$report.Add("")
}
if ($nameGroups.Count -gt 30) { [void]$report.Add(("(showing top 30 of $($nameGroups.Count))")) }
[void]$report.Add("")

# Section 3: Cross-drive (D: <-> X:) for high-overlap candidates
[void]$report.Add("## Section 3: Cross-drive overlap (D: <-> X:)")
[void]$report.Add("")
$candidates = @(
  @{d='D:\BIL';   x='X:\BIL'},
  @{d='D:\FAP';   x='X:\FAP'},
  @{d='D:\brain'; x='X:\'}
)
foreach ($c in $candidates) {
  [void]$report.Add(("### {0} vs {1}" -f $c.d, $c.x))
  $dCount = if (Test-Path -LiteralPath $c.d) { @(Get-ChildItem -LiteralPath $c.d -Recurse -File -Force -ErrorAction SilentlyContinue).Count } else { 0 }
  $xCount = if (Test-Path -LiteralPath $c.x) { @(Get-ChildItem -LiteralPath $c.x -Recurse -File -Force -ErrorAction SilentlyContinue).Count } else { 0 }
  [void]$report.Add(("- D: file count: {0}" -f $dCount))
  [void]$report.Add(("- X: file count: {0}" -f $xCount))
  [void]$report.Add("")
}

$report -join "`r`n" | Set-Content -LiteralPath 'X:\Backside\DEDUP_REPORT_20260516.md' -Encoding UTF8
Write-Host ""
Write-Host "Report: X:\Backside\DEDUP_REPORT_20260516.md"
Write-Host "Elapsed: $(((Get-Date) - $startTime).TotalMinutes.ToString('N1')) min"
