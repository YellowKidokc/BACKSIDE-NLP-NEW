@echo off
setlocal
cd /d "%~dp0"
if "%STATIONS_ROOT%"=="" (
  echo STATIONS_ROOT is not set. Cannot sync to station drive.
  pause
  exit /b 1
)
set "TARGET=%STATIONS_ROOT%\TTS_EDGE"
echo Syncing TTS kit to:
echo %TARGET%
echo.
robocopy "%CD%" "%TARGET%" /E /XD inbox outbox processed logs
if not exist "%TARGET%\inbox" mkdir "%TARGET%\inbox"
if not exist "%TARGET%\outbox" mkdir "%TARGET%\outbox"
if not exist "%TARGET%\processed" mkdir "%TARGET%\processed"
if not exist "%TARGET%\logs" mkdir "%TARGET%\logs"
echo.
echo Done. Press Enter to close.
pause >nul
