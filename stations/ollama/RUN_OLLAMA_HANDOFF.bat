@echo off
echo ============================================
echo  Ollama Session Handoff Summarizer
echo  Uses Mistral via Ollama for real comprehension
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
echo Processing session files...
echo.

cd /d "%~dp0"
py -3 "%~dp0ollama_session_handoff.py" %*

echo.
echo ============================================
echo  Done.
echo  Output: %~dp0EXPORTS\reports\session-handoffs\
echo  Logs: %~dp0EXPORTS\reports\logs\ollama_handoff_*.log
echo ============================================
pause
