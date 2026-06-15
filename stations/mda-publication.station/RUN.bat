@echo off
setlocal
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0RUN.ps1" %*
exit /b %ERRORLEVEL%
