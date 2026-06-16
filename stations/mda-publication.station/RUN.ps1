param(
    [ValidateSet("route", "route-whatif", "regen-scorecards")]
    [string]$Task = "route-whatif"
)

$ErrorActionPreference = "Stop"
$StationRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

switch ($Task) {
    "route" {
        & (Join-Path $StationRoot "scripts\ROUTE_MDA_OUTPUTS.ps1")
    }
    "route-whatif" {
        & (Join-Path $StationRoot "scripts\ROUTE_MDA_OUTPUTS.ps1") -WhatIf
    }
    "regen-scorecards" {
        $python = "C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe"
        & $python (Join-Path $StationRoot "scripts\REGEN_SCORECARDS.py")
    }
}
