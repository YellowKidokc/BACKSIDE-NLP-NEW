@echo off
echo ═══════════════════════════════════════
echo   PREFERENCE ENGINE HEALTH CHECK
echo ═══════════════════════════════════════
echo.
echo [P01] implicit...
python "X:\Models\preference-engine-implicit\_front_door\health.py"
echo.
echo [P02] recbole...
python "X:\Models\preference-engine-recbole\_front_door\health.py"
echo.
echo [P03] lightfm...
python "X:\Models\preference-engine-lightfm\_front_door\health.py"
echo.
echo [P04] paper_recommender...
python "X:\Models\preference-engine-paper-recommender\_front_door\health.py"
echo.
echo [P05] ppk...
python "X:\Models\preference-engine-ppk\_front_door\health.py"
echo.
echo [P06] river...
python "X:\Models\preference-engine-river\_front_door\health.py"
echo.
echo [P07] markovify...
python "X:\Models\preference-engine-markovify\_front_door\health.py"
echo.
echo.
echo Done.
pause
