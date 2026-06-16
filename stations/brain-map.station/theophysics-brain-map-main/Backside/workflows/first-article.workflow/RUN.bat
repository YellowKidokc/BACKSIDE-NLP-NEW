@echo off
setlocal
cd /d D:\GitHub\theophysics-brain-map
python Backside\workflows\first-article.workflow\pipeline.py --drop X:\Backside\workflows\first-article.workflow\00_DROP %*
pause
