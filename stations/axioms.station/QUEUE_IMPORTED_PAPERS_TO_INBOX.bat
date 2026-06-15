@echo off
setlocal
title Queue Imported Papers To Axioms Inbox
echo ============================================
echo  QUEUE: Imported Papers To Axioms Inbox
echo ============================================
echo This copies canonical imported paper files into 00_INBOX_DROP_PAPERS_HERE.
echo Backup/system folders are skipped.
echo.

set ROOT=%~dp0
set PYTHON_EXE=
if exist "C:\Users\lowes\AppData\Local\Programs\Python\Python313\python.exe" set PYTHON_EXE=C:\Users\lowes\AppData\Local\Programs\Python\Python313\python.exe
if not defined PYTHON_EXE if exist "C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe" set PYTHON_EXE=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe
if not defined PYTHON_EXE set PYTHON_EXE=py -3

%PYTHON_EXE% "%ROOT%scripts\queue_imported_papers.py"
set RC=%ERRORLEVEL%
echo ============================================
echo  Done (rc=%RC%).
echo  Next: run RUN_AXIOMS_WORKFLOW.bat
echo ============================================
pause
exit /b %RC%
