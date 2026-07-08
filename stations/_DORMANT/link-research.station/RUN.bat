@echo off
setlocal
cd /d "%~dp0"
if exist "%~dp0run_engine.bat" (
  call "%~dp0run_engine.bat" %*
) else (
  echo Missing run_engine.bat
  exit /b 1
)
