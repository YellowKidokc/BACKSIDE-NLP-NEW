@echo off
setlocal
cd /d "%~dp0"
set "LOG_DIR=X:\WORKFLOWS\MDA-PUBLICATION\EXPORTS\_LOGS"
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
for /f %%I in ('C:\WINDOWS\System32\WindowsPowerShell\v1.0\powershell.exe -NoProfile -Command "Get-Date -Format yyyyMMdd_HHmmss"') do set "STAMP=%%I"
set "LOG_FILE=%LOG_DIR%\claim_extractor_%STAMP%.log"
set PYTHON_EXE=C:\Users\lowes\AppData\Local\Programs\Python\Python313\python.exe
if not exist "%PYTHON_EXE%" set PYTHON_EXE=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe
if not exist "%PYTHON_EXE%" set PYTHON_EXE=py -3

set "INPUT_DIR=X:\WORKFLOWS\MDA-PUBLICATION\01_LOSSLESS\articles"

"%PYTHON_EXE%" "%~dp0extract.py" "%INPUT_DIR%" --recursive --format md %* >> "%LOG_FILE%" 2>&1
set RC=%ERRORLEVEL%
echo Log: %LOG_FILE%
exit /b %RC%
