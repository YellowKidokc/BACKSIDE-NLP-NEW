@echo off
echo === FIS - File Intelligence System ===
echo.

if "%1"=="--gui" (
    cd /d "%~dp0"
    python -m fis.gui
    exit /b 0
)

if "%1"=="" (
    echo Usage:
    echo   RUN.bat --gui                     Launch GUI
    echo   RUN.bat [folder_path]             Classify folder
    echo   RUN.bat --file [file_path]        Classify single file
    echo   RUN.bat --init-db                 Initialize SQLite
    echo   RUN.bat --no-bart --no-deberta    Skip heavy models
    exit /b 1
)

cd /d "%~dp0"
python -m fis %*
