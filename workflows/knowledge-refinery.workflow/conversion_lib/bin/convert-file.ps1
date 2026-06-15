param(
  [Parameter(Mandatory=$true, Position=0)]
  [string]$Source,
  [string]$Out,
  [string]$Config = "X:\Backside\conversion_lib\config\x_drive.yaml",
  [switch]$Detect
)

$ErrorActionPreference = "Stop"
$LibRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$env:PYTHONPATH = Join-Path $LibRoot "src"

$argsList = @("-m", "theophysics_conversion.convert")
if ($Detect) { $argsList += "--detect" }
$argsList += $Source
if ($Config) { $argsList += @("--config", $Config) }
if ($Out) { $argsList += @("--out", $Out) }

python @argsList

