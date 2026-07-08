@echo off
setlocal
cd /d D:\GitHub\theophysics-brain-map
python Backside\workflows\first-article.workflow\series_stack.py --batch-root "X:\EXPORTS\first-article-workflow-series\20260520-155258-gtq-root-series" %*
pause
