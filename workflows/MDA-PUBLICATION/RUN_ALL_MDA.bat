@echo off
setlocal

set "ROOT=X:\WORKFLOWS\MDA-PUBLICATION"
set "LOG_DIR=%ROOT%\EXPORTS\_LOGS"
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
for /f %%I in ('C:\WINDOWS\System32\WindowsPowerShell\v1.0\powershell.exe -NoProfile -Command "Get-Date -Format yyyyMMdd_HHmmss"') do set "STAMP=%%I"
set "MASTER_LOG=%LOG_DIR%\RUN_ALL_MDA_%STAMP%.log"

call :log Starting MDA station sequence.

call "X:\Backside\stations\sbert-embedder.station\RUN.bat"
set "RC=%ERRORLEVEL%"
if not "%RC%"=="0" exit /b %RC%

call :log sbert-embedder completed.
call "X:\Backside\stations\classify-documents.station\RUN.bat"
set "RC=%ERRORLEVEL%"
if not "%RC%"=="0" exit /b %RC%

call :log classify-documents completed.
call "X:\Backside\stations\claim-extractor.station\RUN.bat"
set "RC=%ERRORLEVEL%"
if not "%RC%"=="0" exit /b %RC%

call :log claim-extractor completed.
call "X:\Backside\stations\7q-classifier.station\RUN.bat"
set "RC=%ERRORLEVEL%"
if not "%RC%"=="0" exit /b %RC%

call :log 7q-classifier completed.
call "X:\Backside\stations\paper-intelligence-suite.station\RUN_LOCAL_PAPER_INTELLIGENCE.bat"
set "RC=%ERRORLEVEL%"
if not "%RC%"=="0" exit /b %RC%

call :log paper-intelligence-suite completed.
call :log All MDA stations completed successfully.
exit /b 0

:log
echo %~1
>> "%MASTER_LOG%" echo %~1
exit /b 0
