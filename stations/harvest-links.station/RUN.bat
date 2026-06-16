@echo off
setlocal
echo ============================================
echo  WORKFLOW: harvest-links
echo  URLs -> fetch -> SBERT -> DeBERTa -> Postgres -> HDBSCAN
echo ============================================

set PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe
if not exist "%PYTHON%" (echo ERROR: Python not found at %PYTHON% & pause & exit /b 1)

REM Workflow-specific deps not covered by tool INSTALL.bats:
"%PYTHON%" -m pip install requests beautifulsoup4 readability-lxml openpyxl --quiet

"%PYTHON%" "%~dp0pipeline.py"
set RC=%ERRORLEVEL%

echo ============================================
echo  Done (rc=%RC%). See X:\Backside\_LOGS\workflow_harvest-links_*.log
echo ============================================
pause
exit /b %RC%
