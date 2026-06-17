@echo off
echo ========================================
echo  ST_008 — contradiction-scan
echo  Scan for internal contradictions between claims across articles
echo ========================================
cd /d "%~dp0"
python pipeline.py
if errorlevel 1 (
    echo [FAIL] Station contradiction-scan exited with errors.
    pause
) else (
    echo [OK] Station contradiction-scan complete.
    pause
)
