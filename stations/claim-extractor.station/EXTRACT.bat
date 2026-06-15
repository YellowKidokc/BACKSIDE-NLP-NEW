@echo off
setlocal enabledelayedexpansion
title Theophysics Claim Extractor
color 0A

:: ============================================================
:: PORTABLE: all paths resolve from this station folder (%~dp0)
:: All exports land in the station root EXPORTS\ folder ONLY.
:: ============================================================
cd /d "%~dp0"

:: Robust python detection (mirrors RUN.bat)
set "PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python313\python.exe"
if not exist "%PYTHON%" set "PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe"
if not exist "%PYTHON%" set "PYTHON=py -3"

set "EXTRACT=%~dp0extract.py"
set "EXPORT=%~dp0export_excel.py"
set "SEVENQ=%~dp0claims_7q_pass.py"
set "TARGETS=%~dp0targets.txt"
set "OUTPUT_DIR=%~dp0EXPORTS"

echo.
echo  ============================================
echo   THEOPHYSICS CLAIM EXTRACTOR - 08_CLAIMS
echo   POF 2828   ^|   exports -^> %OUTPUT_DIR%
echo  ============================================
echo.

if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

:: Check if targets file exists
if not exist "%TARGETS%" (
    echo  No targets.txt found. Creating template...
    echo # CLAIM EXTRACTOR TARGETS> "%TARGETS%"
    echo # One folder per line. Lines starting with # are ignored.>> "%TARGETS%"
    echo # Supports local drives, mapped drives, and UNC paths.>> "%TARGETS%"
    echo #>> "%TARGETS%"
    echo # === EXAMPLES ===>> "%TARGETS%"
    echo # K:\Folders\LEAN4\canonical>> "%TARGETS%"
    echo # O:\_Theophysics_v5\04_THEOPYHISCS>> "%TARGETS%"
    echo # T:\MASTER_EQUATION_TEST\theophysics-math>> "%TARGETS%"
    echo #>> "%TARGETS%"
    echo # === YOUR TARGETS (uncomment or add below) ===>> "%TARGETS%"
    echo K:\Folders\LEAN4\canonical>> "%TARGETS%"
    echo.
    echo  Created: %TARGETS%
    echo  Edit this file to add folders, then run again.
    echo.
    pause
    exit /b
)

echo  Menu:
echo.
echo  [1] Run extractor on targets.txt folders
echo  [2] Run extractor on a single folder (type path)
echo  [3] Export last extraction to Excel
echo  [4] Edit targets.txt
echo  [5] View recent outputs
echo  [6] Full pipeline (extract all targets + export Excel + 7Q pass)
echo  [0] Exit
echo.
set /p CHOICE="  Choose: "

if "%CHOICE%"=="1" goto :run_targets
if "%CHOICE%"=="2" goto :run_single
if "%CHOICE%"=="3" goto :export_last
if "%CHOICE%"=="4" goto :edit_targets
if "%CHOICE%"=="5" goto :view_outputs
if "%CHOICE%"=="6" goto :full_pipeline
if "%CHOICE%"=="0" exit /b
echo  Invalid choice.
pause
goto :eof

:run_targets
echo.
echo  Reading targets from: %TARGETS%
echo  ============================================

set "COUNT=0"
set "LAST_JSON="

for /f "usebackq tokens=* delims=" %%A in ("%TARGETS%") do (
    set "LINE=%%A"
    :: Skip comments and blank lines
    if not "!LINE!"=="" (
        if not "!LINE:~0,1!"=="#" (
            set /a COUNT+=1
            echo.
            echo  [Target !COUNT!] %%A
            echo  ------------------------------------------

            :: Detect format by checking what files exist
            dir "%%A\*.md" >nul 2>&1 && set "HAS_MD=1" || set "HAS_MD=0"
            dir "%%A\*.html" >nul 2>&1 && set "HAS_HTML=1" || set "HAS_HTML=0"

            if "!HAS_MD!"=="1" if "!HAS_HTML!"=="1" (
                set "FMT=both"
            ) else if "!HAS_MD!"=="1" (
                set "FMT=md"
            ) else if "!HAS_HTML!"=="1" (
                set "FMT=html"
            ) else (
                set "FMT=both"
            )

            %PYTHON% "%EXTRACT%" "%%A" --recursive --format !FMT!

            :: Find the most recent output
            for /f "delims=" %%F in ('dir /b /o-d "%OUTPUT_DIR%\claims_*.json" 2^>nul') do (
                set "LAST_JSON=%OUTPUT_DIR%\%%F"
                goto :found_json
            )
            :found_json
        )
    )
)

echo.
echo  ============================================
echo  Processed !COUNT! targets.
if defined LAST_JSON (
    echo  Last output: !LAST_JSON!
    echo.
    set /p DOEXPORT="  Export to Excel now? (y/n): "
    if /i "!DOEXPORT!"=="y" (
        %PYTHON% "%EXPORT%" "!LAST_JSON!"
        echo.
        echo  Excel saved next to JSON in: %OUTPUT_DIR%
    )
)
echo.
pause
goto :eof

:run_single
echo.
set /p FOLDER="  Enter folder path: "
if not exist "%FOLDER%" (
    echo  ERROR: Path not found: %FOLDER%
    pause
    goto :eof
)
set /p FMT="  Format (md/html/both) [both]: "
if "%FMT%"=="" set "FMT=both"
set /p RECURSE="  Recursive? (y/n) [y]: "
if "%RECURSE%"=="" set "RECURSE=y"

if /i "%RECURSE%"=="y" (
    %PYTHON% "%EXTRACT%" "%FOLDER%" --recursive --format %FMT%
) else (
    %PYTHON% "%EXTRACT%" "%FOLDER%" --format %FMT%
)

:: Find latest output
for /f "delims=" %%F in ('dir /b /o-d "%OUTPUT_DIR%\claims_*.json" 2^>nul') do (
    set "LAST_JSON=%OUTPUT_DIR%\%%F"
    goto :found_single
)
:found_single
if defined LAST_JSON (
    echo.
    set /p DOEXPORT="  Export to Excel now? (y/n): "
    if /i "!DOEXPORT!"=="y" (
        %PYTHON% "%EXPORT%" "!LAST_JSON!"
        echo  Excel saved next to JSON in: %OUTPUT_DIR%
    )
)
pause
goto :eof

:export_last
echo.
echo  Recent JSON outputs:
echo  ------------------------------------------
dir /b /o-d "%OUTPUT_DIR%\claims_*.json" 2>nul
echo.

for /f "delims=" %%F in ('dir /b /o-d "%OUTPUT_DIR%\claims_*.json" 2^>nul') do (
    set "LAST_JSON=%OUTPUT_DIR%\%%F"
    goto :got_last
)
:got_last
if not defined LAST_JSON (
    echo  No JSON files found. Run extraction first.
    pause
    goto :eof
)
echo  Using: !LAST_JSON!
%PYTHON% "%EXPORT%" "!LAST_JSON!"
echo.
echo  Saved to: %OUTPUT_DIR%
pause
goto :eof

:edit_targets
notepad "%TARGETS%"
goto :eof

:view_outputs
echo.
echo  Recent outputs in %OUTPUT_DIR%:
echo  ------------------------------------------
dir /b /o-d "%OUTPUT_DIR%\*.*" 2>nul | findstr /v "^$"
echo.
pause
goto :eof

:full_pipeline
echo.
echo  FULL PIPELINE: Extract all targets + Export Excel + 7Q pass
echo  ============================================

set "COUNT=0"

for /f "usebackq tokens=* delims=" %%A in ("%TARGETS%") do (
    set "LINE=%%A"
    if not "!LINE!"=="" (
        if not "!LINE:~0,1!"=="#" (
            set /a COUNT+=1
            echo.
            echo  [!COUNT!] Extracting: %%A
            %PYTHON% "%EXTRACT%" "%%A" --recursive --format both
        )
    )
)

:: Get the latest JSON
for /f "delims=" %%F in ('dir /b /o-d "%OUTPUT_DIR%\claims_*.json" 2^>nul') do (
    set "LAST_JSON=%OUTPUT_DIR%\%%F"
    goto :pipe_export
)
:pipe_export
if defined LAST_JSON (
    echo.
    echo  Exporting to Excel...
    %PYTHON% "%EXPORT%" "!LAST_JSON!"
    echo.
    echo  Running 7Q enrichment pass...
    %PYTHON% "%SEVENQ%" "!LAST_JSON!" --out-dir "%OUTPUT_DIR%"
    echo.
    echo  ============================================
    echo  DONE. !COUNT! targets processed.
    echo  All exports in: %OUTPUT_DIR%
    echo  ============================================
)
echo.
pause
goto :eof
