@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0"

echo ================================================
echo  CLAIM EXTRACTOR -- Drop papers, get extracted claims
echo ================================================
echo  Drop paper.md files into _inbox\ then press any key
echo  Results will appear in _outbox\
echo ================================================

if not exist "_inbox" mkdir "_inbox"
if not exist "_outbox" mkdir "_outbox"
if not exist "_processed" mkdir "_processed"

if exist "FETCH_SOURCE.txt" (
  set /p FETCH_SOURCE=<FETCH_SOURCE.txt
  if not "!FETCH_SOURCE!"=="" (
    echo Copying source files from !FETCH_SOURCE! to _inbox\ ...
    xcopy "!FETCH_SOURCE!\*" "_inbox\" /Y /I >nul
  )
)

pause
call "%~dp0RUN.bat"
set RC=%ERRORLEVEL%
echo.
echo Done (rc=%RC%). Check _outbox\ for results.
pause
exit /b %RC%
