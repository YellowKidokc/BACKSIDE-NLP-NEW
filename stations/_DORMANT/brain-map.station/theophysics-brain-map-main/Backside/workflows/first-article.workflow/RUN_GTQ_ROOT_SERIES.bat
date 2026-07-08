@echo off
setlocal
cd /d D:\GitHub\theophysics-brain-map
python Backside\workflows\first-article.workflow\pipeline.py --input-root "\\dlowenas\HPWorkstation\Desktop\Master HTMl\K-Production-Ready\02-genesis-to-quantum" --glob "gtq-*.html" --export-root "X:\EXPORTS\first-article-workflow-series" --state-root "X:\Backside\_state\first-article-workflow-series" %*
pause
