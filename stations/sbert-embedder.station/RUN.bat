@echo off
setlocal
set "LOG_DIR=X:\WORKFLOWS\MDA-PUBLICATION\EXPORTS\_LOGS"
set "OUTPUT_DIR=X:\WORKFLOWS\MDA-PUBLICATION\EXPORTS\sbert_embeddings"
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
for /f %%I in ('C:\WINDOWS\System32\WindowsPowerShell\v1.0\powershell.exe -NoProfile -Command "Get-Date -Format yyyyMMdd_HHmmss"') do set "STAMP=%%I"
set "LOG_FILE=%LOG_DIR%\sbert_runner_%STAMP%.log"
echo ============================================
echo  Running 02_SBERT
echo ============================================

if defined PYTHON_EXE goto have_python
set "PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe"
goto python_ready

:have_python
set "PYTHON=%PYTHON_EXE%"

:python_ready
if not exist "%PYTHON%" (
  echo ERROR: Python not found at %PYTHON%
  exit /b 1
)

"%PYTHON%" "%~dp0sbert_runner.py" %* >> "%LOG_FILE%" 2>&1
set RC=%ERRORLEVEL%
set RC=%ERRORLEVEL%

echo ============================================
echo  Done (rc=%RC%). Check _LOGS for output.
echo ============================================
echo Log: %LOG_FILE%
exit /b %RC%
