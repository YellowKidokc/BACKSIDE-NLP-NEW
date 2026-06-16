@echo off
setlocal
echo ============================================
echo  TEST 01_WHISPER (smoke test, tiny model)
echo ============================================

set PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe
"%PYTHON%" "%~dp0whisper_runner.py" --self-test
set RC=%ERRORLEVEL%

echo.
if %RC%==0 (echo PASS) else (echo FAIL rc=%RC%)
pause
exit /b %RC%
