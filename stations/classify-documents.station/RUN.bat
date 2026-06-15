@echo off
setlocal
set "LOG_DIR=X:\WORKFLOWS\MDA-PUBLICATION\EXPORTS\_LOGS"
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
for /f %%I in ('C:\WINDOWS\System32\WindowsPowerShell\v1.0\powershell.exe -NoProfile -Command "Get-Date -Format yyyyMMdd_HHmmss"') do set "STAMP=%%I"
set "LOG_FILE=%LOG_DIR%\classify_documents_%STAMP%.log"
echo ============================================
echo  STATION: classify-documents
echo  text files -^> vectors + labels -^> JSON sidecars + CSV summary
echo ============================================

set PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python313\python.exe
if not exist "%PYTHON%" set PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe
if not exist "%PYTHON%" set PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python311\python.exe
if not exist "%PYTHON%" set PYTHON=py -3

"%PYTHON%" "%~dp0pipeline.py" >> "%LOG_FILE%" 2>&1
set RC=%ERRORLEVEL%

echo ============================================
echo  Done (rc=%RC%). See X:\Backside\_logs\workflow_classify-documents_*.log
echo ============================================
echo Log: %LOG_FILE%
exit /b %RC%
