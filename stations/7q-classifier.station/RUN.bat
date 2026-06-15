@echo off
setlocal
cd /d "%~dp0"
set "LOG_DIR=X:\WORKFLOWS\MDA-PUBLICATION\EXPORTS\_LOGS"
set "CLAIMS_DIR=X:\WORKFLOWS\MDA-PUBLICATION\EXPORTS\claims"
set "OUT_DIR=X:\WORKFLOWS\MDA-PUBLICATION\EXPORTS\7q_classified"
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
if not exist "%OUT_DIR%" mkdir "%OUT_DIR%"
for /f %%I in ('C:\WINDOWS\System32\WindowsPowerShell\v1.0\powershell.exe -NoProfile -Command "Get-Date -Format yyyyMMdd_HHmmss"') do set "STAMP=%%I"
set "LOG_FILE=%LOG_DIR%\seven_q_classifier_%STAMP%.log"
set "CLAIMS_JSON="
if not exist "%CLAIMS_DIR%\claims_*.json" (
  echo ERROR: No claims_*.json found in "%CLAIMS_DIR%"
  exit /b 1
)
for %%F in ("%CLAIMS_DIR%\claims_*.json") do set "CLAIMS_JSON=%%~fF"
set "PYTHON_EXE=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe"
if not exist "%PYTHON_EXE%" set "PYTHON_EXE=py -3"
"%PYTHON_EXE%" "%~dp0..\claim-extractor.station\claims_7q_pass.py" "%CLAIMS_JSON%" --out-dir "%OUT_DIR%" %* >> "%LOG_FILE%" 2>&1
set RC=%ERRORLEVEL%
echo Log: %LOG_FILE%
exit /b %RC%
