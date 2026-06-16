@echo off
setlocal
title Axiom Rigor Gate
echo ============================================
echo  RIGOR GATE: Axioms
echo ============================================
echo This does not prove anything in Lean 4.
echo It checks whether graded papers have enough proof-discipline
echo to be reused downstream.
echo.

set ROOT=%~dp0
set PYTHON_EXE=
if exist "C:\Users\lowes\AppData\Local\Programs\Python\Python313\python.exe" set PYTHON_EXE=C:\Users\lowes\AppData\Local\Programs\Python\Python313\python.exe
if not defined PYTHON_EXE if exist "C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe" set PYTHON_EXE=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe
if not defined PYTHON_EXE set PYTHON_EXE=py -3

%PYTHON_EXE% "%ROOT%scripts\axiom_rigor_gate.py"
set RC=%ERRORLEVEL%

echo ============================================
echo  Done (rc=%RC%).
echo  Manifest: %ROOT%06_RIGOR_GATES\AXIOM_RIGOR_MANIFEST.md
echo ============================================
pause
exit /b %RC%
