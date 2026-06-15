@echo off
setlocal
echo ============================================
echo  TEST 05_YOUTUBE (uses 100 quota units)
echo ============================================
set PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe
"%PYTHON%" "%~dp0youtube_scraper.py" --self-test
set RC=%ERRORLEVEL%
if %RC%==0 (echo PASS) else (echo FAIL rc=%RC%)
pause
exit /b %RC%
