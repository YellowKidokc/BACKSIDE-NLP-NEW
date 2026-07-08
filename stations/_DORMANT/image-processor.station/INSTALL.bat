@echo off
setlocal
echo ============================================
echo  Installing dependencies for 06_IMAGES
echo ============================================
echo.
echo NOTE: easyocr pulls torch + opencv (~600MB). First install can be slow.
echo.

set PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe
if not exist "%PYTHON%" (
    echo ERROR: Python not found at %PYTHON%
    pause & exit /b 1
)

"%PYTHON%" -m pip install --upgrade pip --quiet
"%PYTHON%" -m pip install easyocr transformers torch pillow --quiet
if errorlevel 1 (
    echo ERROR: pip install failed.
    pause & exit /b 1
)

echo Done. Run TEST.bat to verify.
pause
