@echo off
setlocal
echo ============================================
echo  STATION: reading-level-glossary
echo  Drop .txt/.md/.html files into DROP_HERE, then run this.
echo ============================================

set PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python313\python.exe
if not exist "%PYTHON%" set PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe
if not exist "%PYTHON%" set PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python311\python.exe
if not exist "%PYTHON%" set PYTHON=py -3

"%PYTHON%" "%~dp0pipeline.py" %*
set RC=%ERRORLEVEL%

echo ============================================
echo  Done (rc=%RC%). See EXPORTS\run_* reports.
echo ============================================
exit /b %RC%
