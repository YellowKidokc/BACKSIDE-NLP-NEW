@echo off
echo Processing inbox for preference-engine-recbole...
cd /d %~dp0
python _front_door\process_inbox.py
pause
