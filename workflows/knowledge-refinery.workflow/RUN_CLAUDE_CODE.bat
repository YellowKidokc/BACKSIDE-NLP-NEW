@echo off
echo ============================================
echo  Knowledge Refinery v2 - CLAUDE CODE Engine
echo ============================================
set PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python313\python.exe
set SCRIPT=X:\knowledge-refinery\scripts\refinery_conductor_v2.py

if "%~1"=="" (
    echo Processing intake folder...
    "%PYTHON%" "%SCRIPT%" --engine claude-code
) else (
    "%PYTHON%" "%SCRIPT%" --engine claude-code %*
)
pause
