@echo off
setlocal
echo ============================================
echo  STATION: Treaties pipeline
echo  Requires RUN.bat/server to be active.
echo ============================================

set "STATION_ROOT=%~dp0"
cd /d "%STATION_ROOT%"

if exist ".venv\Scripts\python.exe" (
  set "PYTHON_EXE=%STATION_ROOT%.venv\Scripts\python.exe"
) else (
  set "PYTHON_EXE=python"
)

if "%~1"=="" (
  "%PYTHON_EXE%" "%STATION_ROOT%run_pipeline.py"
) else (
  "%PYTHON_EXE%" "%STATION_ROOT%run_pipeline.py" %*
)
exit /b %ERRORLEVEL%
