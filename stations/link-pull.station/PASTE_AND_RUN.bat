@echo off
setlocal
echo ============================================
echo  WORKFLOW: Link Pull Drop
echo  Copy a list of links first, then run this.
echo ============================================

set DROP=%~dp0DROP_HERE
if not exist "%DROP%" mkdir "%DROP%"

for /f %%I in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd_HHmmss"') do set STAMP=%%I
set OUT=%DROP%\LINKS_%STAMP%.txt

powershell -NoProfile -ExecutionPolicy Bypass -Command "$text = Get-Clipboard -Raw; if ([string]::IsNullOrWhiteSpace($text)) { Write-Error 'Clipboard is empty. Copy the links first.'; exit 2 }; Set-Content -LiteralPath '%OUT%' -Value $text -Encoding UTF8"
if errorlevel 1 (
  echo ERROR: Could not save clipboard links.
  pause
  exit /b 1
)

echo Saved clipboard links to:
echo %OUT%
call "%~dp0RUN.bat"
exit /b %ERRORLEVEL%

