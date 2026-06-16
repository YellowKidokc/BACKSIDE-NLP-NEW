@echo off
echo Health check 05_MODELS...
cd /d X:\05_MODELS
python _front_door\health.py 2>nul || echo No health script yet
pause
