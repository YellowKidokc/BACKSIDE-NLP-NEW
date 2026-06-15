$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..")
$registryPath = Join-Path $root "CONFIG\model_stations.example.json"
$registry = Get-Content -LiteralPath $registryPath -Raw | ConvertFrom-Json

$rows = foreach ($station in $registry.stations) {
    $exists = Test-Path -LiteralPath $station.path
    [pscustomobject]@{
        Station = $station.name
        Path = $station.path
        Exists = $exists
        Purpose = $station.purpose
    }
}

$rows | Format-Table -AutoSize

$missing = @($rows | Where-Object { -not $_.Exists })
if ($missing.Count -gt 0) {
    Write-Host ""
    Write-Host "Missing model station folders: $($missing.Station -join ', ')" -ForegroundColor Yellow
    exit 2
}

Write-Host ""
Write-Host "All registered model station folders exist." -ForegroundColor Green
