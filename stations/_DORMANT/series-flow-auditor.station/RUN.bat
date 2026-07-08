@echo off
setlocal
cd /d "%~dp0"
if "%~1"=="" (
  echo Usage:
  echo   RUN.bat "PATH_TO_SERIES_DIR" ["PATH_TO_OUTPUT"]
  exit /b 2
)
set "OUT=%~2"
if "%OUT%"=="" set "OUT=%cd%\EXPORTS\latest"
python scripts\series_flow_auditor.py --series-dir "%~1" --out "%OUT%"
