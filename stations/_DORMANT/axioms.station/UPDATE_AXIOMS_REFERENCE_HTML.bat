@echo off
setlocal
title Update Axioms Reference HTML
echo ============================================
echo  UPDATE: Required Axioms / Paper Snapshot HTML
echo ============================================

set ROOT=%~dp0
set PYTHON_EXE=
if exist "C:\Users\lowes\AppData\Local\Programs\Python\Python313\python.exe" set PYTHON_EXE=C:\Users\lowes\AppData\Local\Programs\Python\Python313\python.exe
if not defined PYTHON_EXE if exist "C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe" set PYTHON_EXE=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe
if not defined PYTHON_EXE set PYTHON_EXE=py -3

%PYTHON_EXE% "%ROOT%scripts\update_required_html_outputs.py"
set RC=%ERRORLEVEL%
echo ============================================
echo  Done (rc=%RC%).
echo ============================================
pause
exit /b %RC%
