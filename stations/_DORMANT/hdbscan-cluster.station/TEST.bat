@echo off
setlocal
echo ============================================
echo  TEST 04_HDBSCAN
echo ============================================
set PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe
"%PYTHON%" "%~dp0cluster_runner.py" --self-test
set RC=%ERRORLEVEL%
if %RC%==0 (echo PASS) else (echo FAIL rc=%RC%)
pause
exit /b %RC%
