@echo off
setlocal
set PYTHONIOENCODING=utf-8
set OUT=X:\knowledge-refinery\06_HTML_REPORTS\7Q
if not exist "%OUT%" mkdir "%OUT%"
python "X:\knowledge-refinery\13_SOURCE_SYSTEMS\7Q\engine\main.py" test --output "%OUT%"
endlocal
