@echo off
REM Theophysics Paper Intake — local web server
REM Form: http://localhost:8088/

cd /d "%~dp0"
echo.
echo ===============================================
echo  Theophysics Paper Intake
echo  Open http://localhost:8088/ in your browser
echo  Ctrl+C to stop
echo ===============================================
echo.

python -m uvicorn app:app --host 0.0.0.0 --port 8088 %*
