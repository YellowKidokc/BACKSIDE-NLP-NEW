@echo off
setlocal
echo ============================================
echo  UPDATE: link-pull-drop dependencies
echo ============================================

set PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe
if not exist "%PYTHON%" (
  echo ERROR: Python not found at %PYTHON%
  pause
  exit /b 1
)

"%PYTHON%" -m pip install --upgrade requests beautifulsoup4 youtube-transcript-api yt-dlp
set RC=%ERRORLEVEL%

echo ============================================
echo  Update complete (rc=%RC%)
echo ============================================
pause
exit /b %RC%

