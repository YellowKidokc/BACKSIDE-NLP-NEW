@echo off
echo ========================================
echo  ST_007 — evidence-map
echo  Map evidence to claims, identify gaps and unsupported claims
echo ========================================
cd /d "%~dp0"
python pipeline.py
if errorlevel 1 (
    echo [FAIL] Station evidence-map exited with errors.
    pause
) else (
    echo [OK] Station evidence-map complete.
    pause
)
