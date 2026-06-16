@echo off
setlocal
echo ============================================
echo  STATION: Paper Proof Grader
echo  Non-interactive run. Drop papers into DROP_PAPERS_HERE first.
echo ============================================

set PYTHON_EXE=C:\Users\lowes\AppData\Local\Programs\Python\Python313\python.exe
if not exist "%PYTHON_EXE%" set PYTHON_EXE=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe
if not exist "%PYTHON_EXE%" set PYTHON_EXE=C:\Users\lowes\AppData\Local\Programs\Python\Python311\python.exe

if not exist "%~dp0pipeline.py" (
  echo Missing pipeline.py
  exit /b 1
)

if exist "%PYTHON_EXE%" (
  "%PYTHON_EXE%" "%~dp0pipeline.py"
) else (
  py -3 "%~dp0pipeline.py"
)
set RC=%ERRORLEVEL%

echo ============================================
echo  Done (rc=%RC%). See X:\Backside\_logs\workflow_paper-proof-grader_*.log
echo ============================================
exit /b %RC%


