@echo off
setlocal
set WORKFLOW_ROOT=%~dp0
set LIB_ROOT=X:\Conversions\conversion-layer
set PYTHONPATH=%LIB_ROOT%\src
set CONFIG=%LIB_ROOT%\config\x_drive.yaml

if not exist "%WORKFLOW_ROOT%00_DROP" mkdir "%WORKFLOW_ROOT%00_DROP"
if not exist "%WORKFLOW_ROOT%OUTPUT" mkdir "%WORKFLOW_ROOT%OUTPUT"
if not exist "%WORKFLOW_ROOT%ARCHIVE" mkdir "%WORKFLOW_ROOT%ARCHIVE"

for %%F in ("%WORKFLOW_ROOT%00_DROP\*") do (
  if exist "%%~fF" (
    python -m theophysics_conversion.convert "%%~fF" --config "%CONFIG%" > "%WORKFLOW_ROOT%OUTPUT\%%~nF.latest.txt"
    move "%%~fF" "%WORKFLOW_ROOT%ARCHIVE\" >nul
  )
)

echo Conversion layer complete.
