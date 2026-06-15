@echo off
setlocal
cd /d "%~dp0"
echo Edge TTS runner
echo Inbox:    %CD%\inbox
echo Outbox:   %CD%\outbox
echo Processed:%CD%\processed
echo.
echo Drop .md/.txt files into inbox, then press Enter.
pause >nul
echo.
echo Starting now. Progress will show below.
echo If it says another run is active, wait for that window to finish.
echo.
python run_tts.py
echo.
echo Finished. Press Enter to close.
pause >nul
