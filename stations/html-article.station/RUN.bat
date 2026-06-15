@echo off
setlocal
cd /d "%~dp0"

echo ============================================
echo  STATION: HTML Article
echo  Safe calibration run: lanes 02, 03, 07, 08
echo ============================================

set PYTHON_EXE=C:\Users\lowes\AppData\Local\Programs\Python\Python313\python.exe
if not exist "%PYTHON_EXE%" set PYTHON_EXE=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe
if not exist "%PYTHON_EXE%" set PYTHON_EXE=C:\Users\lowes\AppData\Local\Programs\Python\Python311\python.exe
if not exist "%PYTHON_EXE%" set PYTHON_EXE=py -3

set RUN_ID=%DATE:~-4%%DATE:~4,2%%DATE:~7,2%_%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%
set RUN_ID=%RUN_ID: =0%
set RUN_DIR=%~dp0EXPORTS\canary_runs\run_%RUN_ID%
set INPUT=%~dp000_DROP\CALIBRATION_pilot-preflight-checklist.md

mkdir "%RUN_DIR%" >nul 2>nul

echo [02] Section map
%PYTHON_EXE% "%~dp002_SECTION_MAP\run.py" --in "%INPUT%" --out "%RUN_DIR%\02_SECTION_MAP" --paper-uuid "html-article-calibration" --worker "RUN.bat"
if errorlevel 1 exit /b 1

echo [03] YAML metadata
%PYTHON_EXE% "%~dp003_YAML_METADATA\run.py" --in "%INPUT%" --section-map "%RUN_DIR%\02_SECTION_MAP\section-map.json" --out "%RUN_DIR%\03_YAML_METADATA" --worker "RUN.bat"
if errorlevel 1 exit /b 1

echo [07] Math translation
%PYTHON_EXE% "%~dp007_MATH_TRANSLATION\run.py" --input "%INPUT%" --output-dir "%RUN_DIR%\07_MATH_TRANSLATION" --loopback-dir "%RUN_DIR%\14_LOOPBACK_REVIEW"
if errorlevel 1 exit /b 1

echo [08] Section vectors using deterministic fallback
%PYTHON_EXE% "%~dp008_SECTION_VECTORS\run.py" --section-map "%RUN_DIR%\02_SECTION_MAP\section-map.json" --metadata "%RUN_DIR%\03_YAML_METADATA\metadata.json" --output-dir "%RUN_DIR%\08_SECTION_VECTORS" --prefer-fallback
if errorlevel 1 exit /b 1

echo ============================================
echo  Done. Output: %RUN_DIR%
echo ============================================
exit /b 0
