@echo off
setlocal
echo ============================================
echo  CONNECT: interactive Python with Database loaded
echo ============================================
echo.
echo The variable `db` is connected; try:
echo   db.query("SELECT COUNT(*) AS c FROM harvested_links_apologetics")
echo   db.query("SELECT COUNT(*) AS c FROM youtube_apologetics")
echo   exit()
echo.

set PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe
"%PYTHON%" -i -c "import sys; sys.path.insert(0, r'%~dp0'.rstrip('\\')); from db_utils import Database; db = Database().connect(); print('connected. db.query(...) ready')"
