@echo off
setlocal
chcp 65001 >nul
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
cd /d "%~dp0"
if "%~1"=="" goto usage
if /I "%~1"=="watch" (
  python -m fis.watcher
  exit /b %ERRORLEVEL%
)
if /I "%~1"=="init-db" (
  python -m fis.db.init_db
  exit /b %ERRORLEVEL%
)
if /I "%~1"=="seed" (
  python -m fis.db.seed_codes
  exit /b %ERRORLEVEL%
)
if /I "%~1"=="backfill" (
  shift
  python -m fis.backfill %*
  exit /b %ERRORLEVEL%
)
:usage
echo Usage: RUN.bat watch ^| init-db ^| seed ^| backfill [args]
exit /b 0
