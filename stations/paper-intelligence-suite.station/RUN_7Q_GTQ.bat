@echo off
title GTQ — OpenAI 7Q Analysis
color 0A

:: Pull API key from user environment
for /f "tokens=*" %%i in ('powershell -command "[System.Environment]::GetEnvironmentVariable(\"OPENAI_API_KEY\",\"User\")"') do set OPENAI_API_KEY=%%i

if "%OPENAI_API_KEY%"=="" (
    echo.
    echo  ERROR: OPENAI_API_KEY not found in environment.
    echo  Run SET_OPENAI_KEY.ps1 first.
    pause
    exit /b 1
)

echo.
echo  Key found. Starting 7Q analysis on Genesis to Quantum series...
echo  This will take 3-5 minutes. Watch results below.
echo.

python "C:\Users\lowes\AppData\Local\Temp\run_7q.py"

echo.
echo  Done. Check the _7Q_ANALYSIS folder in the series directory.
pause
