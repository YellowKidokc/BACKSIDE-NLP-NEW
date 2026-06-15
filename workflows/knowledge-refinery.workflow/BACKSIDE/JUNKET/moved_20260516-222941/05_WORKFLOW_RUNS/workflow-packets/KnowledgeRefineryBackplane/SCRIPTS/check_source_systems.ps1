$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..")
$registryPath = Join-Path $root "CONFIG\source_registry.example.json"
$registry = Get-Content -LiteralPath $registryPath -Raw | ConvertFrom-Json

$rows = foreach ($source in $registry.sources.PSObject.Properties) {
    $item = $source.Value
    $exists = Test-Path -LiteralPath $item.path
    $listable = $false
    $target = ""
    $errorText = ""
    if ($exists) {
        try {
            $fsItem = Get-Item -LiteralPath $item.path -Force
            if ($fsItem.LinkType) {
                $target = ($fsItem.Target -join "; ")
            }
            Get-ChildItem -LiteralPath $item.path -Force -ErrorAction Stop | Select-Object -First 1 | Out-Null
            $listable = $true
        } catch {
            $errorText = $_.Exception.Message
        }
    }
    [pscustomobject]@{
        Source = $source.Name
        Path = $item.path
        Exists = $exists
        Listable = $listable
        LinkTarget = $target
        Error = $errorText
        Role = $item.role
    }
}

$rows | Format-Table -AutoSize

$blocked = @($rows | Where-Object { -not $_.Exists -or -not $_.Listable })
if ($blocked.Count -gt 0) {
    Write-Host ""
    Write-Host "Blocked source systems: $($blocked.Source -join ', ')" -ForegroundColor Yellow
    exit 2
}

Write-Host ""
Write-Host "All registered source system paths exist and are listable." -ForegroundColor Green
