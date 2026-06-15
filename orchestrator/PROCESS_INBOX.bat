@echo off
echo Processing inbox for 07_ORCHESTRATOR...
cd /d X:\07_ORCHESTRATOR
python _front_door\process_inbox.py 2>nul || echo No processor yet
pause
