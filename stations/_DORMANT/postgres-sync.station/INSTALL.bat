@echo off
setlocal
echo ============================================
echo  Installing dependencies for 07_POSTGRES
echo ============================================

set PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe
if not exist "%PYTHON%" (
    echo ERROR: Python not found at %PYTHON%
    pause & exit /b 1
)

"%PYTHON%" -m pip install --upgrade pip --quiet
"%PYTHON%" -m pip install psycopg2-binary numpy --quiet
if errorlevel 1 (
    echo ERROR: pip install failed.
    pause & exit /b 1
)

echo Pinging database...
"%PYTHON%" "%~dp0db_utils.py" test
set RC=%ERRORLEVEL%

if %RC%==0 (echo PASS) else (echo FAIL rc=%RC% — see TROUBLESHOOT.md)
pause
exit /b %RC%
