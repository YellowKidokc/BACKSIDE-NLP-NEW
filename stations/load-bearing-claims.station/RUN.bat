@echo off
echo ========================================
echo  ST_005 — load-bearing-claims
echo  Identify structurally load-bearing claims vs rhetoric/narrative/metadata
echo ========================================
cd /d "%~dp0"
python pipeline.py
if errorlevel 1 (
    echo [FAIL] Station load-bearing-claims exited with errors.
    pause
) else (
    echo [OK] Station load-bearing-claims complete.
    pause
)
