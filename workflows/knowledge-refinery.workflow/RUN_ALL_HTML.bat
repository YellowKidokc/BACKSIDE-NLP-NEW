@echo off
echo ============================================
echo  Knowledge Refinery v2 - FULL HTML DUMP
echo  Engine: Ollama (phi4)
echo ============================================
set PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python313\python.exe
set SCRIPT=X:\knowledge-refinery\scripts\refinery_conductor_v2.py

echo Processing all HTML files from Z:\HTML DUMP...
"%PYTHON%" "%SCRIPT%" --engine ollama --folder "Z:\HTML DUMP" --skip-processed
echo.
echo Done. Check X:\knowledge-refinery\07_OBSIDIAN_EXPORT\
pause
