@echo off
setlocal
title Session Handoff Pipeline (Combined)
echo ============================================
echo  SESSION HANDOFF PIPELINE (Combined)
echo.
echo  Stage 1: Ollama summarizes raw chat
echo  Stage 2: Mirror, vectorize, Postgres, archive
echo.
echo  1. Put full chat/session files in DROP_HERE
echo  2. Run this script
echo  3. DROP_HERE is emptied after processing
echo ============================================
echo.

REM Check if Ollama is running
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Ollama is not running. Starting it...
    start "" "C:\Users\lowes\AppData\Local\Programs\Ollama\ollama.exe" serve
    echo Waiting 10 seconds for Ollama to start...
    timeout /t 10 /nobreak >nul
    echo.
)

REM Find Python
set PYTHON_EXE=
if exist "C:\Users\lowes\AppData\Local\Programs\Python\Python313\python.exe" set PYTHON_EXE=C:\Users\lowes\AppData\Local\Programs\Python\Python313\python.exe
if not defined PYTHON_EXE if exist "C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe" set PYTHON_EXE=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe
if not defined PYTHON_EXE if exist "C:\Python314\python.exe" set PYTHON_EXE=C:\Python314\python.exe

:loop
for /f %%C in ('powershell -NoProfile -Command "$ext=@('.txt','.md','.html','.htm'); (Get-ChildItem -LiteralPath '\\dlowenas\brain\session-handoff-drop\DROP_HERE' -File -ErrorAction SilentlyContinue | Where-Object { $ext -contains $_.Extension.ToLowerInvariant() } | Measure-Object).Count"') do set COUNT=%%C
if "%COUNT%"=="0" (
    set RC=0
    goto done
)

echo.
echo Processing %COUNT% file(s)...
if defined PYTHON_EXE (
    "%PYTHON_EXE%" "%~dp0pipeline_combined.py" %*
) else (
    py -3 "%~dp0pipeline_combined.py" %*
)
set RC=%ERRORLEVEL%
if not "%RC%"=="0" goto done
goto loop

:done
echo.
echo ============================================
echo  Done (rc=%RC%).
echo  Output: \\dlowenas\brain\session-handoff-drop\OUTPUT\
echo  Logs:   \\dlowenas\brain\_LOGS\session_handoff_*.log
echo ============================================
pause
exit /b %RC%
