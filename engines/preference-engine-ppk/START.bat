@echo off
echo Starting preference-engine-ppk preference engine...
cd /d %~dp0
python _front_door\health.py
echo.
echo P05 ready on port 20105
pause
