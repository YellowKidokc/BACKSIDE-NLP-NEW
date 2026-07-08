@echo off
setlocal
echo ============================================
echo  STATION: link-pull-drop
echo  Drop a txt or markdown file of links, then run this.
echo ============================================

set PYTHON_EXE=C:\Users\lowes\AppData\Local\Programs\Python\Python313\python.exe
if not exist "%PYTHON_EXE%" set PYTHON_EXE=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe

if exist "%PYTHON_EXE%" (
  "%PYTHON_EXE%" "%~dp0pipeline.py"
) else (
  py -3.13 "%~dp0pipeline.py"
)
set RC=%ERRORLEVEL%

echo ============================================
echo  Done (rc=%RC%). See X:\Backside\_LOGS\workflow_link-pull-drop_*.log
echo ============================================
exit /b %RC%

