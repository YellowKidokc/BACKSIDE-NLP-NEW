@echo off
setlocal
cd /d "%~dp0"

set "ROOT=%~dp0"
set "ROOT=%ROOT:~0,-1%"
set "NODE_SCRIPT=%ROOT%\scripts\prepare-tts-workflow.js"
set "DEFAULT_OUT=%ROOT%\workflow_output\first-layer-sweep"

if "%~1"=="" (
  echo Usage:
  echo   RUN_FIRST_LAYER_SWEEP.bat ^<file-or-folder^> [run-id] [out-dir]
  echo   RUN_FIRST_LAYER_SWEEP.bat --list ^<list-file^> [run-id] [out-dir]
  echo.
  echo This is non-interactive: math translation only, no TTS.
  exit /b 0
)

if not exist "%ROOT%\node_modules" (
  echo Installing Math Translation Layer packages...
  call npm.cmd install
  if errorlevel 1 exit /b %ERRORLEVEL%
)

if not exist "%ROOT%\dist\src\core\index.js" (
  echo Building Math Translation Layer...
  call npm.cmd run build
  if errorlevel 1 exit /b %ERRORLEVEL%
)

set "RUN_ID=%~2"
if "%RUN_ID%"=="" for /f %%I in ('powershell -NoProfile -ExecutionPolicy Bypass -Command "Get-Date -Format yyyyMMdd-HHmmss"') do set "RUN_ID=%%I"

set "OUT_DIR=%~3"
if "%OUT_DIR%"=="" set "OUT_DIR=%DEFAULT_OUT%"

if /I "%~1"=="--list" (
  if "%~2"=="" (
    echo ERROR: --list requires a list-file argument.
    exit /b 2
  )
  set "LIST_FILE=%~2"
  set "RUN_ID=%~3"
  if "%RUN_ID%"=="" for /f %%I in ('powershell -NoProfile -ExecutionPolicy Bypass -Command "Get-Date -Format yyyyMMdd-HHmmss"') do set "RUN_ID=%%I"
  set "OUT_DIR=%~4"
  if "%OUT_DIR%"=="" set "OUT_DIR=%DEFAULT_OUT%"
  node "%NODE_SCRIPT%" --list "%LIST_FILE%" --out "%OUT_DIR%" --run-id "%RUN_ID%" --types html --copy-source --markdown
  exit /b %ERRORLEVEL%
)

node "%NODE_SCRIPT%" --input "%~1" --out "%OUT_DIR%" --run-id "%RUN_ID%" --types html --copy-source --markdown
exit /b %ERRORLEVEL%
