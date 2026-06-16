@echo off
setlocal
echo ============================================
echo  Installing dependencies for 03_DEBERTA
echo ============================================
echo.
echo NOTE: this pulls torch (~2GB on first install). Be patient.
echo.

set PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe
if not exist "%PYTHON%" (
    echo ERROR: Python not found at %PYTHON%
    pause & exit /b 1
)

"%PYTHON%" -m pip install --upgrade pip --quiet
"%PYTHON%" -m pip install transformers torch sentencepiece protobuf psycopg2-binary --quiet
if errorlevel 1 (
    echo ERROR: pip install failed. See TROUBLESHOOT.md.
    pause & exit /b 1
)

echo Done. Run TEST.bat to verify (will download ~1.6GB model on first run).
pause
