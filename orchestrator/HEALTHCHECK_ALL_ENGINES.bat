@echo off
echo ═══════════════════════════════════════
echo   PREFERENCE ENGINE HEALTH CHECK
echo ═══════════════════════════════════════
echo.
echo [P01] implicit...
python "X:\Models\P01_implicit\_front_door\health.py"
echo.
echo [P02] recbole...
python "X:\Models\P02_recbole\_front_door\health.py"
echo.
echo [P03] lightfm...
python "X:\Models\P03_lightfm\_front_door\health.py"
echo.
echo [P04] paper_recommender...
python "X:\Models\P04_paper_recommender\_front_door\health.py"
echo.
echo [P05] ppk...
python "X:\Models\P05_ppk\_front_door\health.py"
echo.
echo [P06] river...
python "X:\Models\P06_river\_front_door\health.py"
echo.
echo [P07] markovify...
python "X:\Models\P07_markovify\_front_door\health.py"
echo.
echo.
echo Done.
pause
