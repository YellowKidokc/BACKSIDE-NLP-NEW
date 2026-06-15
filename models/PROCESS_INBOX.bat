@echo off
echo Processing inbox for 05_MODELS...
cd /d X:\05_MODELS
python _front_door\process_inbox.py 2>nul || echo No processor yet
pause
