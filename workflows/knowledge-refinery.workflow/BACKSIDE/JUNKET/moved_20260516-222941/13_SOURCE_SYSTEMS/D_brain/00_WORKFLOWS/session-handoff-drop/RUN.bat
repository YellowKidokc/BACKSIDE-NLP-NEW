@echo off
setlocal
echo ============================================
echo  WORKFLOW: session-handoff-drop
echo  Drop a full page into DROP_HERE, then run this.
echo ============================================

set PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe
if not exist "%PYTHON%" (echo ERROR: Python not found at %PYTHON% & pause & exit /b 1)

"%PYTHON%" "%~dp0pipeline.py"
set RC=%ERRORLEVEL%

echo ============================================
echo  Done (rc=%RC%). See D:\brain\_LOGS\workflow_session-handoff-drop_*.log
echo ============================================
pause
exit /b %RC%
