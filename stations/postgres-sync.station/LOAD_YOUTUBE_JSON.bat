@echo off
setlocal
echo ============================================
echo  Bulk-load YouTube apologetics JSON into Postgres
echo ============================================

set PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe

REM Default to the bundled package; override with arg 1 if provided.
if "%~1"=="" (
    set JSON=%~dp0DROP_HERE\youtube_apologetics_data.json
) else (
    set JSON=%~1
)

if not exist "%JSON%" (
    echo ERROR: file not found: %JSON%
    echo Pass a path: LOAD_YOUTUBE_JSON.bat C:\path\to\youtube_apologetics_data.json
    pause & exit /b 1
)

echo Loading: %JSON%
"%PYTHON%" "%~dp0db_utils.py" load-youtube-json "%JSON%"
set RC=%ERRORLEVEL%

if %RC%==0 (echo PASS) else (echo FAIL rc=%RC%)
pause
exit /b %RC%
