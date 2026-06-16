@echo off
setlocal
cd /d "%~dp0"
python pipeline.py %*
echo.
echo Done. Outputs are under EXPORTS\runs.
pause
