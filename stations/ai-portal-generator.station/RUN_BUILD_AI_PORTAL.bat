@echo off
setlocal
title Theophysics AI Portal Builder
cd /d "%~dp0"

echo.
echo Building the AI-facing portal...
echo Source: %~dp0config.json
echo.

py -3 generator.py
if errorlevel 1 (
  echo.
  echo Build failed. Run TROUBLESHOOT_AI_PORTAL.bat for checks.
  pause
  exit /b 1
)

echo.
echo Done.
echo Portal folder:
echo \\dlowenas\brain\proof-explorer\ai-portal
echo.
pause

