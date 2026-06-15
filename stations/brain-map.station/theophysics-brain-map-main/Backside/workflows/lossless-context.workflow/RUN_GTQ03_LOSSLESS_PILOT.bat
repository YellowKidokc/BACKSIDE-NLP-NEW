@echo off
setlocal

set "REPO=D:\GitHub\theophysics-brain-map"
set "SOURCE=\\dlowenas\HPWorkstation\Desktop\Master HTMl\K-Production-Ready\02-genesis-to-quantum\gtq-03-first-quantum-state.html"
set "EXPORT_ROOT=X:\EXPORTS\lossless-context\gtq-03-pilot"
set "STATE_ROOT=X:\Backside\_state\lossless-context\gtq-03-pilot"

for /f %%I in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd-HHmmss"') do set "RUN_ID=%%I"
set "RUN_DIR=%EXPORT_ROOT%\%RUN_ID%"
set "STATE_DIR=%STATE_ROOT%\%RUN_ID%"
set "MD=%RUN_DIR%\gtq-03-first-quantum-state.canonical.md"

mkdir "%RUN_DIR%" >nul 2>nul
mkdir "%STATE_DIR%" >nul 2>nul

cd /d "%REPO%"
set "PYTHONPATH=%REPO%\Backside\conversion_lib\src"

echo [1/2] Converting HTML to canonical Markdown...
python -m theophysics_conversion.convert "%SOURCE%" --out "%MD%"
if errorlevel 1 exit /b %errorlevel%

set "PYTHONPATH=%REPO%"
echo [2/2] Running lossless context pipeline...
python -m Backside.lossless_context_pipeline.cli run --input "%MD%" --out "%RUN_DIR%\lossless" --vault-id theophysics-brain --embeddings none
if errorlevel 1 exit /b %errorlevel%

echo.
echo Done.
echo Export: %RUN_DIR%
echo State:  %STATE_DIR%
