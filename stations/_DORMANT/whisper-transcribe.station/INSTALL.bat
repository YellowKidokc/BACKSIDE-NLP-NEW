@echo off
setlocal
echo ============================================
echo  Installing dependencies for 01_WHISPER
echo ============================================
echo.

set PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe
if not exist "%PYTHON%" (
    echo ERROR: Python not found at %PYTHON%
    pause & exit /b 1
)

echo Upgrading pip...
"%PYTHON%" -m pip install --upgrade pip --quiet

echo Installing faster-whisper + numpy...
"%PYTHON%" -m pip install faster-whisper numpy --quiet
if errorlevel 1 (
    echo ERROR: pip install failed. See TROUBLESHOOT.md.
    pause & exit /b 1
)

echo.
echo ffmpeg check (required for non-WAV audio):
where ffmpeg >nul 2>&1
if errorlevel 1 (
    echo   WARNING: ffmpeg not on PATH. WAV inputs will work; MP3/MP4 will not.
    echo            Install: winget install Gyan.FFmpeg
) else (
    echo   ffmpeg: OK
)

echo.
echo Done. Run TEST.bat to verify.
pause
