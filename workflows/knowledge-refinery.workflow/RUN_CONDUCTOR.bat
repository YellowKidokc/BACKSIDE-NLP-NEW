@echo off
echo ============================================
echo  Theophysics Knowledge Refinery Conductor
echo  Processing pipeline with Ollama (phi4)
echo ============================================
echo.

set PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python313\python.exe
set SCRIPT=X:\knowledge-refinery\scripts\refinery_conductor.py

REM If args passed, use them. Otherwise process intake folder.
if "%~1"=="" (
    echo Processing files from X:\knowledge-refinery\00_INTAKE\
    "%PYTHON%" "%SCRIPT%"
) else (
    echo Processing specified files...
    "%PYTHON%" "%SCRIPT%" %*
)

echo.
echo Pipeline complete. Check X:\knowledge-refinery\07_OBSIDIAN_EXPORT\ for output.
pause
