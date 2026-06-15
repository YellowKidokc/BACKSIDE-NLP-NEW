@echo off
setlocal
echo ============================================
echo  D:\brain — Install ALL tool dependencies
echo ============================================
echo.

set TOOLS=01_WHISPER 02_SBERT 03_DEBERTA 04_HDBSCAN 05_YOUTUBE 06_IMAGES 07_POSTGRES

for %%T in (%TOOLS%) do (
    echo --------------------------------------------
    echo  %%T
    echo --------------------------------------------
    if exist "%~dp0%%T\INSTALL.bat" (
        call "%~dp0%%T\INSTALL.bat"
    ) else (
        echo SKIP: %%T\INSTALL.bat not found
    )
    echo.
)

echo ============================================
echo  Done. Run each tool's TEST.bat to verify.
echo ============================================
pause
