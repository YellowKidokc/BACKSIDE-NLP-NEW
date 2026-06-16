@echo off
REM new_station.bat -- thin wrapper around new_station.py
REM
REM Usage:
REM   new_station.bat name [--lane EMBED] [--model M-...] [--purpose "..."] [--status active]
REM
REM Example:
REM   new_station.bat claim_check --lane NLI --model M-NLI-STRONG-001 --status draft

setlocal

if "%~1"=="" (
    echo Usage: new_station.bat name [flags]
    echo Example: new_station.bat claim_check --lane NLI --model M-NLI-STRONG-001
    exit /b 1
)

set "SCRIPT_DIR=%~dp0"
python "%SCRIPT_DIR%new_station.py" %*
exit /b %ERRORLEVEL%
