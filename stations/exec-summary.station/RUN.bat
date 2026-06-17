@echo off
echo ========================================
echo  ST_001 — exec-summary
echo  Generate executive summary of a paper or article
echo ========================================
cd /d "%~dp0"
python pipeline.py
if errorlevel 1 (
    echo [FAIL] Station exec-summary exited with errors.
    pause
) else (
    echo [OK] Station exec-summary complete.
    pause
)
