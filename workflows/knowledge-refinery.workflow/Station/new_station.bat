@echo off
REM new_station.bat -- thin wrapper around new_station.py
REM
REM Usage:
REM   new_station.bat LANE NUMBER name [extra flags]
REM
REM Example:
REM   new_station.bat AXIOM 002 canon_writer --next-pass ST-AXIOM-003
REM
REM Calls Python with whatever args you pass through. Run from anywhere; the
REM script resolves paths relative to its own folder.

setlocal

if "%~3"=="" (
    echo Usage: new_station.bat LANE NUMBER name [--purpose "..."] [--model-primary M-...] [--next-pass ST-...]
    echo Example: new_station.bat AXIOM 002 canon_writer
    exit /b 1
)

set "SCRIPT_DIR=%~dp0"
python "%SCRIPT_DIR%new_station.py" %*
set "EXIT_CODE=%ERRORLEVEL%"

endlocal & exit /b %EXIT_CODE%
