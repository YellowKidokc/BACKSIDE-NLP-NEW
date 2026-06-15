@echo off
title THEOPHYSICS PAPER INTELLIGENCE — INSTALLER
color 0A
echo.
echo ============================================================
echo   THEOPHYSICS PAPER INTELLIGENCE SUITE v2.0
echo   Installer
echo ============================================================
echo.
echo Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found. Install Python 3.10+ and retry.
    pause
    exit /b 1
)
echo.
echo [1/5] Installing core packages...
pip install textstat keybert yake sumy semanticscholar python-louvain nltk openai openpyxl pandas scipy scikit-learn pyvis --quiet
echo      Done.
echo.
echo [2/5] Verifying sentence-transformers (embedding engine)...
python -c "from sentence_transformers import SentenceTransformer; print('  OK')" 2>nul || pip install sentence-transformers --quiet
echo      Done.
echo.
echo [3/5] Verifying spacy + English model...
python -c "import spacy; spacy.load('en_core_web_sm'); print('  OK')" 2>nul || (
    pip install spacy --quiet
    python -m spacy download en_core_web_sm --quiet
)
echo      Done.
echo.
echo [4/5] Verifying gensim (topic modeling)...
python -c "import gensim; print('  OK')" 2>nul || pip install gensim --quiet
echo      Done.
echo.
echo [5/5] Downloading NLTK data...
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True); nltk.download('averaged_perceptron_tagger', quiet=True); print('  OK')"
echo      Done.
echo.
echo ============================================================
echo   INSTALLATION COMPLETE
echo ============================================================
echo.
echo   Run the suite:  Double-click LAUNCH.bat
echo   Or from cmd:    python 00_ORCHESTRATOR\run_pipeline.py --help
echo.
echo   Set your OpenAI key for L4 (7Q layer):
echo   System env var:  OPENAI_API_KEY=sk-...
echo.
pause
