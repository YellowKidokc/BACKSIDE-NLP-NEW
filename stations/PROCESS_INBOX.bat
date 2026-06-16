@echo off
echo Processing inbox for 04_STATIONS...
cd /d X:\04_STATIONS
python _front_door\process_inbox.py 2>nul || echo No processor yet
pause
