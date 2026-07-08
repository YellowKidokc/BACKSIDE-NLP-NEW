@echo off
setlocal
cd /d "%~dp0"
echo === Python ===
python --version
echo.
echo === edge-tts package ===
python -m pip show edge-tts
echo.
echo === Brian voices ===
python -m edge_tts --list-voices | findstr /i Brian
echo.
echo === Folder check ===
dir /b
echo.
echo === Inbox files ===
dir /b inbox
echo.
echo Press Enter to close.
pause >nul
