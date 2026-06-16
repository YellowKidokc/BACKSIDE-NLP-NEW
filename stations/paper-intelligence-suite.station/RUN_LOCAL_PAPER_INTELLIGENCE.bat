@echo off
setlocal

set "ROOT=%~dp0"
set "PY=%ROOT%.venv\Scripts\python.exe"
set "INPUT_DIR=X:\WORKFLOWS\MDA-PUBLICATION\01_LOSSLESS\articles"
set "OUTPUT_DIR=X:\WORKFLOWS\MDA-PUBLICATION\EXPORTS\paper_intelligence"
set "LOG_DIR=X:\WORKFLOWS\MDA-PUBLICATION\EXPORTS\_LOGS"

if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
for /f %%I in ('C:\WINDOWS\System32\WindowsPowerShell\v1.0\powershell.exe -NoProfile -Command "Get-Date -Format yyyyMMdd_HHmmss"') do set "STAMP=%%I"
set "LOG_FILE=%LOG_DIR%\paper_intelligence_%STAMP%.log"

if not exist "%PY%" (
  echo Missing virtual environment: "%PY%"
  echo Rebuild it with:
  echo   py -3.11 -m venv "%ROOT%.venv"
  echo   "%ROOT%.venv\Scripts\python.exe" -m pip install -r "%ROOT%requirements-docker.txt"
  exit /b 1
)

"%PY%" "%ROOT%00_ORCHESTRATOR\run_pipeline.py" --series "%INPUT_DIR%" --output "%OUTPUT_DIR%" --pattern "*.md" %* >> "%LOG_FILE%" 2>&1
set RC=%ERRORLEVEL%
echo Log: %LOG_FILE%
exit /b %RC%
