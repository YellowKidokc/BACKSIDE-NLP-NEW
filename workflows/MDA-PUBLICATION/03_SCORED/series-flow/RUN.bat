@echo off
echo ============================================
echo MDA Series Flow Gate
echo ============================================
cd /d "%~dp0"

REM Use paper-intelligence-suite venv if available
if exist "X:\apps\paper-intelligence-suite-python\.venv\Scripts\activate.bat" (
    call "X:\apps\paper-intelligence-suite-python\.venv\Scripts\activate.bat"
)

python run_series_flow.py %*

echo.
echo Done. Check outputs in this folder.
pause
