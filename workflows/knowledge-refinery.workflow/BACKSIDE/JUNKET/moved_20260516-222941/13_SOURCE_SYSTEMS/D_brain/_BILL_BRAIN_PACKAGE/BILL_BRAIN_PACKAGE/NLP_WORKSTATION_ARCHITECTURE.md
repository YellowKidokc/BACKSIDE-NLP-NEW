# NLP WORKSTATION — FOLDER ARCHITECTURE
# Location: D:\brain\
# Each model gets its own folder with install, run, troubleshoot scripts

## FOLDER STRUCTURE

D:\brain\
│
├── 00_WORKFLOWS\                    # Multi-model pipelines
│   ├── harvest-links\               # URL list → scrape → classify → store
│   │   ├── RUN.bat
│   │   ├── config.json
│   │   └── pipeline.py
│   │
│   ├── classify-documents\          # Folder of docs → tagged output
│   │   ├── RUN.bat
│   │   ├── config.json
│   │   └── pipeline.py
│   │
│   ├── transcribe-and-classify\     # Audio/video → transcript → classify
│   │   ├── RUN.bat
│   │   ├── config.json
│   │   └── pipeline.py
│   │
│   └── youtube-scrape\              # Search queries → titles → Postgres
│       ├── RUN.bat
│       ├── config.json
│       └── pipeline.py
│
├── 01_WHISPER\                      # Speech-to-text
│   ├── INSTALL.bat
│   ├── RUN.bat
│   ├── TEST.bat
│   ├── TROUBLESHOOT.md
│   ├── config.json
│   └── whisper_runner.py
│
├── 02_SBERT\                        # Sentence embeddings
│   ├── INSTALL.bat
│   ├── RUN.bat
│   ├── TEST.bat
│   ├── TROUBLESHOOT.md
│   ├── config.json
│   └── sbert_runner.py
│
├── 03_DEBERTA\                      # Zero-shot classification / NLI
│   ├── INSTALL.bat
│   ├── RUN.bat
│   ├── TEST.bat
│   ├── TROUBLESHOOT.md
│   ├── config.json
│   └── deberta_runner.py
│
├── 04_HDBSCAN\                      # Clustering
│   ├── INSTALL.bat
│   ├── RUN.bat
│   ├── TEST.bat
│   ├── TROUBLESHOOT.md
│   ├── config.json
│   └── cluster_runner.py
│
├── 05_YOUTUBE\                      # YouTube Data API scraper
│   ├── INSTALL.bat
│   ├── RUN.bat
│   ├── TEST.bat
│   ├── TROUBLESHOOT.md
│   ├── config.json
│   └── youtube_scraper.py
│
├── 06_IMAGES\                       # Image classification / OCR
│   ├── INSTALL.bat
│   ├── RUN.bat
│   ├── TEST.bat
│   ├── TROUBLESHOOT.md
│   ├── config.json
│   └── image_classifier.py
│
├── 07_POSTGRES\                     # Database utilities
│   ├── CONNECT.bat
│   ├── EXPORT.bat
│   ├── IMPORT.bat
│   ├── TROUBLESHOOT.md
│   ├── config.json
│   └── db_utils.py
│
├── _MODELS\                         # Downloaded model files (shared)
│   ├── whisper-large-v3\
│   ├── all-MiniLM-L6-v2\
│   ├── deberta-v3-large-mnli\
│   └── README.md
│
└── _LOGS\                           # All output logs
    ├── whisper_YYYYMMDD.log
    ├── sbert_YYYYMMDD.log
    ├── deberta_YYYYMMDD.log
    └── workflow_YYYYMMDD.log


## HOW EACH FOLDER WORKS

Every model folder has the same 6 files:
- INSTALL.bat  → installs dependencies, downloads model
- RUN.bat      → runs the model on input you specify
- TEST.bat     → quick test with sample data to verify it works
- TROUBLESHOOT.md → common errors and fixes
- config.json  → all settings in one place (change here, not in code)
- [model]_runner.py → the actual Python script


## HOW WORKFLOWS WORK

A workflow chains multiple models together:
1. You put input files in a directory (or give it a URL list / Excel file)
2. You edit config.json to set: input path, output path, which models to run
3. You double-click RUN.bat
4. The pipeline.py orchestrator calls each model in sequence
5. Output goes to Postgres AND to a local output folder

Example: harvest-links workflow
- Input: Excel file with URLs (or a Postgres query)
- Step 1: Fetch each URL (requests)
- Step 2: Extract text (BeautifulSoup)
- Step 3: Embed with SBERT
- Step 4: Classify with DeBERTa against 20 attack vector labels
- Step 5: Cluster with HDBSCAN
- Step 6: Store everything in Postgres
- Output: classified, clustered, embedded documents with tags


## BATCH SCRIPT TEMPLATE (every RUN.bat)

@echo off
echo ============================================
echo  Running [MODEL NAME]
echo ============================================
echo.

set PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe

REM Check Python exists
if not exist "%PYTHON%" (
    echo ERROR: Python not found at %PYTHON%
    echo Please install Python 3.12 or update this path
    pause
    exit /b 1
)

REM Run the script
"%PYTHON%" "%~dp0[model]_runner.py"

echo.
echo ============================================
echo  Done. Check _LOGS for output.
echo ============================================
pause


## INSTALL SCRIPT TEMPLATE (every INSTALL.bat)

@echo off
echo Installing dependencies for [MODEL NAME]...
set PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe
"%PYTHON%" -m pip install [packages] --quiet
echo Done. Run TEST.bat to verify.
pause


## CONFIG.JSON TEMPLATE

{
    "python_path": "C:\\Users\\lowes\\AppData\\Local\\Programs\\Python\\Python312\\python.exe",
    "input_dir": "",
    "output_dir": "",
    "postgres": {
        "host": "192.168.1.177",
        "port": 2665,
        "user": "root",
        "password": "",
        "password_env": "BRAIN_PG_PASSWORD",
        "database": "crawlab_data"
    },
    "model_settings": {},
    "log_dir": "D:\\brain\\_LOGS"
}


## WORKFLOW CONFIG TEMPLATE (harvest-links)

{
    "name": "harvest-links",
    "input_type": "excel",
    "input_path": "",
    "steps": [
        {"model": "requests", "action": "fetch_urls"},
        {"model": "02_SBERT", "action": "embed"},
        {"model": "03_DEBERTA", "action": "classify", "labels": "20_questions"},
        {"model": "04_HDBSCAN", "action": "cluster"},
        {"model": "07_POSTGRES", "action": "store"}
    ],
    "output_format": "postgres+csv",
    "output_path": "D:\\brain\\_LOGS\\harvest_YYYYMMDD"
}


## WHAT BILL BUILDS

Give this document to Bill (Claude Code). His job:
1. Create the folder structure on D:\brain\
2. Write the INSTALL.bat for each model
3. Write the runner scripts (whisper_runner.py, sbert_runner.py, etc.)
4. Write the workflow pipeline scripts
5. Write the config.json files with Postgres credentials
6. Test each INSTALL.bat and TEST.bat
7. Verify the full harvest-links workflow end-to-end

Bill should NOT touch the _MODELS folder — those models are already downloaded
or will be downloaded by the INSTALL.bat scripts on first run.
