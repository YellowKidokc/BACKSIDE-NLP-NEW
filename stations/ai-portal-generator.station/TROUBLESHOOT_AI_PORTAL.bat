@echo off
setlocal
title Theophysics AI Portal Troubleshooter
cd /d "%~dp0"

echo.
echo Checking AI Portal Builder...
echo.

where py >nul 2>nul
if errorlevel 1 (
  echo Python launcher not found.
) else (
  py -3 --version
)

echo.
echo Checking config...
py -3 -m json.tool config.json >nul
if errorlevel 1 (
  echo Config JSON has a problem.
) else (
  echo Config JSON is valid.
)

echo.
echo Checking generator syntax...
py -3 -m py_compile generator.py
if errorlevel 1 (
  echo Generator has a syntax problem.
) else (
  echo Generator syntax is valid.
)

echo.
echo Checking important folders...
for %%D in ("\\dlowenas\brain\proof-explorer" "\\dlowenas\brain\proof-explorer\reports\gtq_docker_all25_20260507_191530" "C:\Users\lowes\OneDrive\Desktop\genesis-to-quantum" "\\dlowenas\brain\paper-proof-grader\OUTPUT\fruits_of_spirit\fruits_run_20260507_173715") do (
  if exist %%~D (
    echo OK     %%~D
  ) else (
    echo MISSING %%~D
  )
)

echo.
echo To rebuild, run RUN_BUILD_AI_PORTAL.bat
echo.
pause



