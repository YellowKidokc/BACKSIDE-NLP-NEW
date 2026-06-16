@echo off
echo ============================================
echo  Ollama Batch Reprocess — All Archived Sessions
echo  This reprocesses the ARCHIVE folder
echo  Originals are NOT moved or deleted
echo ============================================
echo.

REM Check if Ollama is running
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Ollama is not running. Starting it...
    start "" "C:\Users\lowes\AppData\Local\Programs\Ollama\ollama.exe" serve
    echo Waiting 10 seconds for Ollama to start...
    timeout /t 10 /nobreak >nul
)

echo.
echo Processing all archived sessions...
echo This may take a while — each session takes 30-90 seconds.
echo.

cd /d "%~dp0"
py -3 "%~dp0ollama_session_handoff.py" "X:\session-handoff-drop\ARCHIVE"

echo.
echo ============================================
echo  Done. Summaries in: %~dp0EXPORTS\reports\session-handoffs\
echo ============================================
pause
