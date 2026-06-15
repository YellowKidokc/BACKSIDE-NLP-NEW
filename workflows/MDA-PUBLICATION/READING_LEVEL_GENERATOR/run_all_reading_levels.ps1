param(
    [string]$Model = "gpt-4o",
    [switch]$UseMini,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$root = Resolve-Path "$PSScriptRoot\.."
$articles = Join-Path $root "01_LOSSLESS\articles"
$outdir = Join-Path $root "05_READING_LEVELS"

if ($UseMini) {
    $env:OPENAI_MODEL = "gpt-4o-mini"
} else {
    $env:OPENAI_MODEL = $Model
}

New-Item -ItemType Directory -Force -Path $outdir | Out-Null

$files = Get-ChildItem $articles -Filter *.md | Sort-Object Name
Write-Host "Reading-level batch"
Write-Host "Articles: $($files.Count)"
Write-Host "Model: $env:OPENAI_MODEL"
Write-Host "Output: $outdir"

foreach ($file in $files) {
    $academic = Join-Path $outdir "$($file.BaseName)_ACADEMIC.md"
    $easy = Join-Path $outdir "$($file.BaseName)_EASY.md"
    if ((Test-Path $academic) -and (Test-Path $easy)) {
        Write-Host "SKIP complete: $($file.Name)"
        continue
    }

    $cmd = @("python", (Join-Path $PSScriptRoot "generate_reading_levels.py"), $file.FullName, "--api", "openai", "--outdir", $outdir)
    if ($DryRun) {
        Write-Host "DRYRUN $($cmd -join ' ')"
    } else {
        Write-Host "RUN $($file.Name)"
        & $cmd[0] $cmd[1] $cmd[2] $cmd[3] $cmd[4] $cmd[5] $cmd[6]
    }
}

Write-Host "Done."
