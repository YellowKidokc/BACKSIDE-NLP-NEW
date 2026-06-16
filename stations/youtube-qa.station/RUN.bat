@echo off
setlocal
echo ============================================
echo  STATION: youtube-qa
echo  transcript -> QA JSON + Markdown + CSV/XLSX + snapshot partial
echo ============================================

set PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python313\python.exe
if not exist "%PYTHON%" set PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe
if not exist "%PYTHON%" set PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python311\python.exe
if not exist "%PYTHON%" set PYTHON=py -3

set CONFIG=%~dp0config.json
for /f "usebackq delims=" %%I in (`powershell -NoProfile -Command "(Get-Content '%CONFIG%' | ConvertFrom-Json).input_dir"`) do set INPUT_DIR=%%I
for /f "usebackq delims=" %%I in (`powershell -NoProfile -Command "(Get-Content '%CONFIG%' | ConvertFrom-Json).workflow_root"`) do set WORKFLOW_ROOT=%%I
for /f "usebackq delims=" %%I in (`powershell -NoProfile -Command "(Get-Content '%CONFIG%' | ConvertFrom-Json).metadata_json"`) do set METADATA_JSON=%%I
for /f "usebackq delims=" %%I in (`powershell -NoProfile -Command "(Get-Content '%CONFIG%' | ConvertFrom-Json).write_xlsx"`) do set WRITE_XLSX=%%I
for /f "usebackq delims=" %%I in (`powershell -NoProfile -Command "(Get-Content '%CONFIG%' | ConvertFrom-Json).write_snapshot_partial"`) do set WRITE_SNAPSHOT=%%I

set EXTRA_ARGS=
if not "%WORKFLOW_ROOT%"=="" set EXTRA_ARGS=%EXTRA_ARGS% --workflow-root "%WORKFLOW_ROOT%"
if /I "%WRITE_XLSX%"=="True" set EXTRA_ARGS=%EXTRA_ARGS% --xlsx
if /I "%WRITE_SNAPSHOT%"=="True" set EXTRA_ARGS=%EXTRA_ARGS% --snapshot-partial
if not "%METADATA_JSON%"=="" set EXTRA_ARGS=%EXTRA_ARGS% --metadata-json "%METADATA_JSON%"

"%PYTHON%" "%~dp0scripts\extract_youtube_qa.py" "%INPUT_DIR%" %EXTRA_ARGS%
set RC=%ERRORLEVEL%

echo ============================================
echo  Done (rc=%RC%)
echo ============================================
exit /b %RC%
