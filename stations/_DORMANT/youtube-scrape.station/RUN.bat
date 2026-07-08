@echo off
setlocal
echo ============================================
echo  WORKFLOW: youtube-scrape
echo  scrape -> SBERT embed -> DeBERTa classify -> HDBSCAN cluster
echo ============================================

set PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe
if not exist "%PYTHON%" (echo ERROR: Python not found at %PYTHON% & pause & exit /b 1)

"%PYTHON%" "%~dp0pipeline.py" %*
set RC=%ERRORLEVEL%

echo ============================================
echo  Done (rc=%RC%). See X:\Backside\_LOGS\workflow_youtube-scrape_*.log
echo ============================================
pause
exit /b %RC%
