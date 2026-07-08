@echo off
setlocal
title Brain Workflows Healthcheck
echo ============================================
echo  HEALTHCHECK: Brain Root Workflows
echo ============================================

set ROOT=%~dp0
set PYTHON_EXE=
if exist "C:\Users\lowes\AppData\Local\Programs\Python\Python313\python.exe" set PYTHON_EXE=C:\Users\lowes\AppData\Local\Programs\Python\Python313\python.exe
if not defined PYTHON_EXE if exist "C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe" set PYTHON_EXE=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe
if not defined PYTHON_EXE set PYTHON_EXE=py -3

%PYTHON_EXE% "%ROOT%01_SHARED_SCRIPTS\scripts\workflows_healthcheck.py"
set RC=%ERRORLEVEL%

echo ============================================
echo  Done (rc=%RC%).
echo  Report: %ROOT%WORKFLOWS_HEALTHCHECK_REPORT.latest.md
echo ============================================
pause
exit /b %RC%

