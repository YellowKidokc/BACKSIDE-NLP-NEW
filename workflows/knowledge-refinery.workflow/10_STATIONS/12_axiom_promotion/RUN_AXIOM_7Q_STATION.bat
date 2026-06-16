@echo off
setlocal EnableDelayedExpansion
cd /d X:\paper-proof-grader

where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
  for /f "delims=" %%R in ('python run_axiom_7q_stations.py %*') do set "RUN_ROOT=%%R"
  if not "!RUN_ROOT!"=="" (
    echo !RUN_ROOT!
    echo !RUN_ROOT!>X:\paper-proof-grader\OUTPUT\station-runs\LATEST_AXIOM_7Q_RUN.txt
    echo !RUN_ROOT!>X:\knowledge-refinery\10_STATIONS\12_axiom_promotion\LATEST_OUTPUT_POINTER.txt
  )
  exit /b %ERRORLEVEL%
)

for /f "delims=" %%R in ('py -3.11 run_axiom_7q_stations.py %*') do set "RUN_ROOT=%%R"
if not "!RUN_ROOT!"=="" (
  echo !RUN_ROOT!
  echo !RUN_ROOT!>X:\paper-proof-grader\OUTPUT\station-runs\LATEST_AXIOM_7Q_RUN.txt
  echo !RUN_ROOT!>X:\knowledge-refinery\10_STATIONS\12_axiom_promotion\LATEST_OUTPUT_POINTER.txt
)
exit /b %ERRORLEVEL%
