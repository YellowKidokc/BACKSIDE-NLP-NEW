# Case for Christ -> LLM Wiki Compiler
# PowerShell version — handles the space in path correctly

$wiki = "D:\C4C-wiki"
$src = "O:\_ Theophysics_Case_for_Christ"
$raw = "$wiki\raw"

Write-Host "============================================"
Write-Host "  Case for Christ -> LLM Wiki Compiler"
Write-Host "============================================"
Write-Host ""

# Copy all .md files, flattened into raw/
Write-Host "Copying .md files from Case for Christ vault..."
$files = Get-ChildItem -LiteralPath $src -Recurse -Filter "*.md" -File |
    Where-Object { $_.DirectoryName -notmatch '\.obsidian|\.git|\.trash|_ARCHIVE' }

$count = 0
foreach ($f in $files) {
    $dest = Join-Path $raw $f.Name
    # Handle name collisions by prefixing parent folder
    if (Test-Path $dest) {
        $parent = Split-Path (Split-Path $f.FullName) -Leaf
        $dest = Join-Path $raw "$parent`_$($f.Name)"
    }
    Copy-Item -LiteralPath $f.FullName -Destination $dest -Force
    $count++
}
Write-Host "  Copied $count .md files to raw/"
Write-Host ""

# Run olw
Write-Host "Starting olw compiler..."
Write-Host "  auto_approve=true, auto_maintain=true"
Write-Host "  This will take HOURS for a large vault."
Write-Host "  Go to sleep. Check D:\C4C-wiki\wiki\ when you wake up."
Write-Host ""

Set-Location $wiki
& olw run

Write-Host ""
Write-Host "============================================"
Write-Host "  Done. Open D:\C4C-wiki\wiki\ in Obsidian."
Write-Host "============================================"
