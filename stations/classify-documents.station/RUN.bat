@echo off
setlocal
cd /d "%~dp0"

if not exist "_inbox" mkdir "_inbox"
if not exist "_outbox" mkdir "_outbox"
if not exist "_processed" mkdir "_processed"

set "PYTHON_EXE=%PYTHON_EXE%"
if "%PYTHON_EXE%"=="" set "PYTHON_EXE=python"

"%PYTHON_EXE%" "%~dp0pipeline.py" %*
exit /b %ERRORLEVEL%
