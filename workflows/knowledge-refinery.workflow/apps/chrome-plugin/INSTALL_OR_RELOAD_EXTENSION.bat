@echo off
echo ============================================
echo  BIL Chrome Plugin - Install / Reload Helper
echo ============================================
echo.
echo 1. Chrome extensions will open.
echo 2. Click "Load unpacked".
echo 3. Select this folder:
echo.
echo    X:\chrome-plugin
echo.
echo Do NOT select dashboard.html or popup.html.
echo Select the whole chrome-plugin folder.
echo.
echo If it is already loaded, click Reload on:
echo Bill - Behavioral Intelligence Layer
echo.
start "" "chrome://extensions"
start "" explorer.exe "X:\chrome-plugin"
echo.
pause
