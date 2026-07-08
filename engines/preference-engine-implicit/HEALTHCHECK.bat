@echo off
echo Running health check for preference-engine-implicit...
cd /d %~dp0
python _front_door\health.py
pause
