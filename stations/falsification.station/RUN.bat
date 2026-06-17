@echo off
echo ========================================
echo  ST_006 — falsification
echo  Test claims for falsifiability, generate kill conditions
echo ========================================
cd /d "%~dp0"
python pipeline.py
if errorlevel 1 (
    echo [FAIL] Station falsification exited with errors.
    pause
) else (
    echo [OK] Station falsification complete.
    pause
)
