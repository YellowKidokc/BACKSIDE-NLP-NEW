@echo off
setlocal
title Full Paper Intelligence Bridge

set ROOT=%~dp0
set PYTHON_EXE=
if exist "C:\Users\lowes\AppData\Local\Programs\Python\Python313\python.exe" set PYTHON_EXE=C:\Users\lowes\AppData\Local\Programs\Python\Python313\python.exe
if not defined PYTHON_EXE if exist "C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe" set PYTHON_EXE=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe
if not defined PYTHON_EXE if exist "C:\Users\lowes\AppData\Local\Programs\Python\Python311\python.exe" set PYTHON_EXE=C:\Users\lowes\AppData\Local\Programs\Python\Python311\python.exe
if not defined PYTHON_EXE set PYTHON_EXE=python

if "%~1"=="" (
  echo Usage:
  echo   %~nx0 "C:\path\to\paper.md"
  echo   %~nx0 "C:\path\to\series-folder" --series
  echo.
  echo Outputs:
  echo   X:\Backside\workflows\axioms.workflow\07_FULL_PAPER_INTELLIGENCE
  exit /b 1
)

if /I "%~2"=="--series" (
  "%PYTHON_EXE%" "%ROOT%scripts\run_full_paper_intelligence.py" --series "%~1" --copy-input
) else (
  "%PYTHON_EXE%" "%ROOT%scripts\run_full_paper_intelligence.py" --paper "%~1" --copy-input
)

set RC=%ERRORLEVEL%
echo Done rc=%RC%
exit /b %RC%
