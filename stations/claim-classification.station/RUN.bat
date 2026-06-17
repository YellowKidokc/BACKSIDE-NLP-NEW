@echo off
echo ========================================
echo  ST_004 — claim-classification
echo  Classify extracted claims by type, maturity, and domain
echo ========================================
cd /d "%~dp0"
python pipeline.py
if errorlevel 1 (
    echo [FAIL] Station claim-classification exited with errors.
    pause
) else (
    echo [OK] Station claim-classification complete.
    pause
)
