@echo off
setlocal
title Install Daily NLP Healthcheck
echo ============================================
echo  INSTALL: Daily NLP Healthcheck
echo ============================================
echo This creates a Windows scheduled task that runs the NLP
echo healthcheck every day at 7:30 AM.
echo.

set TASK=Brain NLP Healthcheck
set BAT=\\dlowenas\brain\models\RUN_NLP_HEALTHCHECK.bat

schtasks /Create /TN "%TASK%" /TR "\"%BAT%\"" /SC DAILY /ST 07:30 /F
set RC=%ERRORLEVEL%

echo ============================================
echo  Done (rc=%RC%).
echo ============================================
pause
exit /b %RC%
