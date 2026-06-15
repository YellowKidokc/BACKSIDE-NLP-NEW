@echo off
setlocal
chcp 65001 >nul
echo ============================================
echo  STATION: vault-rater-tsr100
echo  Guarded scorer launcher
echo ============================================

set PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe
if not exist "%PYTHON%" (
  set PYTHON=python
)

if "%OPENAI_API_KEY%"=="" (
  echo BLOCKED: OPENAI_API_KEY is not set in the environment.
  echo Set OPENAI_API_KEY, then run:
  echo   RUN.bat --mode tsr --input "path\to\papers"
  echo No files were scored.
  pause
  exit /b 2
)

"%PYTHON%" "%~dp0lowe_scorer.py" %*
set RC=%ERRORLEVEL%

echo ============================================
echo  Done (rc=%RC%). Output constrained under %~dp0EXPORTS
echo ============================================
pause
exit /b %RC%
