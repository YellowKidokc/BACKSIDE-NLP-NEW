@echo off
setlocal
cd /d "%~dp0"

if exist ".venv\Scripts\pqa.exe" (
  ".venv\Scripts\pqa.exe" %*
  exit /b %ERRORLEVEL%
)

where pqa >nul 2>&1
if %ERRORLEVEL%==0 (
  pqa %*
  exit /b %ERRORLEVEL%
)

echo PaperQA2 station is present, but the pqa CLI is not installed in a local .venv or PATH.
echo Install with the repo instructions, then run this station again.
exit /b 1
