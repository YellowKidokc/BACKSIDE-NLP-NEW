@echo off
setlocal
cd /d "%~dp0"
call "%~dp0RUN_MATH_TTS_WORKFLOW.bat" %*
exit /b %ERRORLEVEL%
