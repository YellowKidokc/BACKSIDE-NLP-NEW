@echo off
echo Starting preference-engine-markovify preference engine...
cd /d %~dp0
python _front_door\health.py
echo.
echo P07 ready on port 20107
pause
