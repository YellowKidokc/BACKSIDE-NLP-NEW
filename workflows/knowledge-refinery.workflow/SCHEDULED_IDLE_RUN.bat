@echo off
REM Theophysics Knowledge Refinery - Idle Scheduler
REM Runs when computer has been idle for 60 minutes
REM Processes HTML DUMP first, then Obsidian vault
REM Skips already-processed files automatically

set PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python313\python.exe
set SCRIPT=X:\knowledge-refinery\scripts\refinery_conductor_v2.py
set LOG=X:\knowledge-refinery\12_HEALTH\scheduled_runs.log

echo [%date% %time%] Scheduled run starting >> "%LOG%"

REM Phase 1: HTML DUMP (27 files)
echo [%date% %time%] Phase 1: HTML DUMP >> "%LOG%"
"%PYTHON%" "%SCRIPT%" --engine ollama --folder "Z:\HTML DUMP" --skip-processed --limit 5 >> "%LOG%" 2>&1

REM Phase 2: C4C-wiki raw files (832 files)
echo [%date% %time%] Phase 2: C4C-wiki >> "%LOG%"
"%PYTHON%" "%SCRIPT%" --engine ollama --folder "D:\C4C-wiki\raw" --skip-processed --limit 5 >> "%LOG%" 2>&1

REM Phase 3: Obsidian v5 Theophysics core
echo [%date% %time%] Phase 3: Obsidian v5 core >> "%LOG%"
"%PYTHON%" "%SCRIPT%" --engine ollama --folder "Z:\_Theophysics_v5\04_THEOPYHISCS" --skip-processed --limit 5 >> "%LOG%" 2>&1

echo [%date% %time%] Scheduled run complete >> "%LOG%"
