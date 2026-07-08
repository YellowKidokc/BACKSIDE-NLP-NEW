@echo off
echo Starting preference-engine-river preference engine...
cd /d %~dp0
python _front_door\health.py
echo.
echo P06 ready on port 20106
pause
