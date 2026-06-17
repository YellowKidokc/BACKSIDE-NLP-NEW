@echo off
echo ========================================
echo  ST_003 — claim-extraction
echo  Extract all claims from text with section context
echo ========================================
cd /d "%~dp0"
python pipeline.py
if errorlevel 1 (
    echo [FAIL] Station claim-extraction exited with errors.
    pause
) else (
    echo [OK] Station claim-extraction complete.
    pause
)
