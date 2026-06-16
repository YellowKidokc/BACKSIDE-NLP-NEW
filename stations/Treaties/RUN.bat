@echo off
setlocal
echo ============================================
echo  STATION: Treaties
echo  Starts the local FastAPI research engine.
echo ============================================

set "STATION_ROOT=%~dp0"
cd /d "%STATION_ROOT%"

if exist ".venv\Scripts\python.exe" (
  set "PYTHON_EXE=%STATION_ROOT%.venv\Scripts\python.exe"
) else (
  set "PYTHON_EXE=python"
)

"%PYTHON_EXE%" -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
exit /b %ERRORLEVEL%
