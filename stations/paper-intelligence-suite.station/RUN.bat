@echo off
setlocal
cd /d "%~dp0"
call "%~dp0RUN_LOCAL_PAPER_INTELLIGENCE.bat" %*
exit /b %ERRORLEVEL%
