@echo off
setlocal
title Full Workflow - Paper to Production Draft
echo ============================================================
echo  Full Workflow - End-to-End Paper Manufacturing
echo  intake -^> FAP spine -^> stations (Ollama) -^> scorecard
echo         -^> draft HTML (Kimi staging shape) -^> batch index
echo ============================================================
echo.
set PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python313\python.exe
set SCRIPT=X:\knowledge-refinery\full_workflow\scripts\batch_orchestrator.py

REM Quick Ollama probe — if it's not up, try to start it
curl -s -m 2 http://localhost:11434/api/tags >NUL 2>&1
if errorlevel 1 (
  echo Ollama not running. Starting it...
  start "" /b "C:\Users\lowes\AppData\Local\Programs\Ollama\ollama.exe" serve
  echo Waiting 5s for Ollama to come up...
  timeout /t 5 /nobreak >NUL
)

"%PYTHON%" "%SCRIPT%" %*
set EXITCODE=%ERRORLEVEL%

echo.
if %EXITCODE% EQU 0 (
  echo Full workflow completed. See X:\knowledge-refinery\full_workflow\output\_LATEST.txt
) else (
  echo Full workflow exited with code %EXITCODE%. See logs in full_workflow\logs\.
)

pause
exit /b %EXITCODE%
