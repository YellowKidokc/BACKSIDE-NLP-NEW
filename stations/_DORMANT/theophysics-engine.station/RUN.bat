@echo off
setlocal
cd /d "%~dp0"
if "%~1"=="" goto usage
if /I "%~1"=="check" (
  npm run check
  exit /b %ERRORLEVEL%
)
if /I "%~1"=="dev" (
  npm run dev
  exit /b %ERRORLEVEL%
)
if /I "%~1"=="build" (
  npm run build
  exit /b %ERRORLEVEL%
)
:usage
echo Usage: RUN.bat check ^| dev ^| build
exit /b 0
