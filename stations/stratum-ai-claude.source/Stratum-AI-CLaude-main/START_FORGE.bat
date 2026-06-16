@echo off
title FORGE Hub Launcher
echo ============================================
echo   FORGE - File-Oriented Research Graph Engine
echo ============================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [FAIL] Python not found. Install from python.org
    pause
    exit /b 1
)
echo [OK] Python found

REM Check PySide6
python -c "import PySide6" >nul 2>&1
if errorlevel 1 (
    echo [MISS] PySide6 not installed. Installing...
    pip install PySide6 --break-system-packages
)
echo [OK] PySide6

REM Check keyboard
python -c "import keyboard" >nul 2>&1
if errorlevel 1 (
    echo [MISS] keyboard not installed. Installing...
    pip install keyboard --break-system-packages
)
echo [OK] keyboard

REM Check pywin32
python -c "import win32clipboard" >nul 2>&1
if errorlevel 1 (
    echo [MISS] pywin32 not installed. Installing...
    pip install pywin32 --break-system-packages
)
echo [OK] pywin32

REM Check requests (for BIL client)
python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo [MISS] requests not installed. Installing...
    pip install requests --break-system-packages
)
echo [OK] requests

echo.
echo ============================================
echo   Dependency check complete. Launching...
echo ============================================
echo.

REM Launch FORGE Hub
cd /d "%~dp0"
python app.py %*

if errorlevel 1 (
    echo.
    echo ============================================
    echo   FORGE Hub crashed. Error above.
    echo ============================================
    pause
)
