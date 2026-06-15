@echo off
echo Health check 04_STATIONS...
cd /d X:\04_STATIONS
python _front_door\health.py 2>nul || echo No health script yet
pause
