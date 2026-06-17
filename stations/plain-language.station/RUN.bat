@echo off
echo ========================================
echo  ST_002 — plain-language
echo  Rewrite content at multiple reading levels (easy / standard / academic)
echo ========================================
cd /d "%~dp0"
python pipeline.py
if errorlevel 1 (
    echo [FAIL] Station plain-language exited with errors.
    pause
) else (
    echo [OK] Station plain-language complete.
    pause
)
