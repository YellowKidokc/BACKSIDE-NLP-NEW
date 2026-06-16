@echo off
setlocal
echo ============================================
echo  WORKFLOW: classify-documents
echo  text files -> SBERT + DeBERTa -> JSON sidecars + CSV summary
echo ============================================

set PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe
if not exist "%PYTHON%" (echo ERROR: Python not found at %PYTHON% & pause & exit /b 1)

"%PYTHON%" "%~dp0pipeline.py"
set RC=%ERRORLEVEL%

echo ============================================
echo  Done (rc=%RC%). See D:\brain\_LOGS\workflow_classify-documents_*.log
echo ============================================
pause
exit /b %RC%
