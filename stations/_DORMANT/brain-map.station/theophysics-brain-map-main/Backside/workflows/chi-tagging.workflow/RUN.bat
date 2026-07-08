@echo off
setlocal
cd /d D:\GitHub\theophysics-brain-map
python Backside\workflows\chi-tagging.workflow\pipeline.py %*
pause
