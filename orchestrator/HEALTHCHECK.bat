@echo off
echo Health check 07_ORCHESTRATOR...
cd /d X:\07_ORCHESTRATOR
python _front_door\health.py 2>nul || echo No health script yet
pause
