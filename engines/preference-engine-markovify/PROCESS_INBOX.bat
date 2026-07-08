@echo off
echo Processing inbox for preference-engine-markovify...
cd /d %~dp0
python _front_door\process_inbox.py
pause
