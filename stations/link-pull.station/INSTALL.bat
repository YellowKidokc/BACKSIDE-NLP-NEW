@echo off
setlocal
echo ============================================
echo  INSTALL: link-pull-drop
echo ============================================

set PYTHON_EXE=C:\Users\lowes\AppData\Local\Programs\Python\Python313\python.exe
if not exist "%PYTHON_EXE%" set PYTHON_EXE=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe

if exist "%PYTHON_EXE%" (
  "%PYTHON_EXE%" -m pip install requests beautifulsoup4 youtube-transcript-api yt-dlp
) else (
  py -3.13 -m pip install requests beautifulsoup4 youtube-transcript-api yt-dlp
)
set RC=%ERRORLEVEL%

echo ============================================
echo  Install complete (rc=%RC%)
echo ============================================
pause
exit /b %RC%

