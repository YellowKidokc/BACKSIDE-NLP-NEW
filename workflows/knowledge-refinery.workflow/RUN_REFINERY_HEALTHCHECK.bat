@echo off
setlocal
title Knowledge Refinery Healthcheck
set ROOT=%~dp0
set PYTHON=
if exist "C:\Python314\python.exe" set PYTHON=C:\Python314\python.exe
if not defined PYTHON if exist "C:\Users\lowes\AppData\Local\Programs\Python\Python313\python.exe" set PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python313\python.exe
if not defined PYTHON if exist "C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe" set PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe
if not defined PYTHON set PYTHON=python

%PYTHON% "%ROOT%scripts\refinery_healthcheck.py"
set RC=%ERRORLEVEL%
echo.
echo Done. rc=%RC%
echo Report: %ROOT%12_HEALTH\REFINERY_HEALTHCHECK.latest.md
pause
exit /b %RC%
