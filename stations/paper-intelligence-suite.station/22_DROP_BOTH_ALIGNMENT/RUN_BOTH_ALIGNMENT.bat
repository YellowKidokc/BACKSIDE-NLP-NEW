@echo off
setlocal
cd /d "%~dp0.."
set "ZONE_DIR=%~dp0."
echo.
echo ================================================
echo  PAPER + BRAIN ALIGNMENT AUTONOMOUS RUN
echo ================================================
echo  Zone: %ZONE_DIR%
echo.
python 00_ORCHESTRATOR\run_drop_zone.py --zone "%ZONE_DIR%" --mode both %*
echo.
echo Finished. Check "%ZONE_DIR%\RUNS"
