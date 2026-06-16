@echo off
setlocal
echo ============================================
echo  Running 01_WHISPER
echo ============================================
echo.

if defined PYTHON_EXE (
    set PYTHON=%PYTHON_EXE%
) else (
    set PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe
)

if not exist "%PYTHON%" (
    echo ERROR: Python not found at %PYTHON%
    echo Edit RUN.bat or set PYTHON_EXE env var.
    pause & exit /b 1
)

"%PYTHON%" "%~dp0whisper_runner.py" %*
set RC=%ERRORLEVEL%

echo.
echo ============================================
echo  Done (rc=%RC%). Check _LOGS for output.
echo ============================================
pause
exit /b %RC%
