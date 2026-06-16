@echo off
title FORGE Hub Debug
echo ============================================
echo   FORGE Hub - Debug Mode
echo ============================================
echo.

cd /d "%~dp0"

echo [1] Checking Python version...
python --version

echo.
echo [2] Checking installed packages...
python -c "import PySide6; print('  PySide6:', PySide6.__version__)"
python -c "import keyboard; print('  keyboard: OK')"
python -c "import win32clipboard; print('  pywin32: OK')"
python -c "import requests; print('  requests: OK')"

echo.
echo [3] Checking config files...
if exist config\settings.ini (echo   settings.ini: OK) else (echo   settings.ini: MISSING)
if exist config\commands.json (echo   commands.json: OK) else (echo   commands.json: MISSING)
if exist config\workflows.json (echo   workflows.json: OK) else (echo   workflows.json: MISSING)

echo.
echo [4] Compile check...
python -m py_compile app.py && echo   app.py: OK || echo   app.py: FAIL
python -m py_compile core\bil_client.py 2>nul && echo   bil_client.py: OK || echo   bil_client.py: MISSING or FAIL
python -m py_compile core\pipeline_runner.py 2>nul && echo   pipeline_runner.py: OK || echo   pipeline_runner.py: MISSING or FAIL
python -m py_compile core\tray.py 2>nul && echo   tray.py: OK || echo   tray.py: MISSING or FAIL
python -m py_compile core\web_server.py 2>nul && echo   web_server.py: OK || echo   web_server.py: MISSING or FAIL

echo.
echo [5] Testing BIL server connection...
python -c "import urllib.request; urllib.request.urlopen('http://localhost:8420/bil/status', timeout=3); print('  BIL: ONLINE')" 2>nul || echo   BIL: offline (not critical)

echo.
echo ============================================
echo   Debug complete.
echo ============================================
pause
