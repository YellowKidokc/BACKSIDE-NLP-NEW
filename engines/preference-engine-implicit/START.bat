@echo off
echo Starting preference-engine-implicit preference engine...
cd /d %~dp0
python _front_door\health.py
echo.
echo P01 ready on port 20101
pause
