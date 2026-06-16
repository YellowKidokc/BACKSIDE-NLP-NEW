@echo off
setlocal
cd /d "%~dp0"
if "%~1"=="" goto usage
if /I "%~1"=="check" (
  powershell -ExecutionPolicy Bypass -File "%~dp0check-env.ps1"
  exit /b %ERRORLEVEL%
)
if /I "%~1"=="gpt" (
  powershell -ExecutionPolicy Bypass -File "%~dp0start-gpt-researcher.ps1"
  exit /b %ERRORLEVEL%
)
if /I "%~1"=="local" (
  powershell -ExecutionPolicy Bypass -File "%~dp0start-local-deep-researcher.ps1"
  exit /b %ERRORLEVEL%
)
:usage
echo Usage: RUN.bat check ^| gpt ^| local
exit /b 0
