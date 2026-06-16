# PROMPT 8: BUILD THE NLP WORKSTATION + LOAD ALL DATA
# Give this to Claude Code (Bill)

## YOUR MISSION
Build the complete NLP workstation at D:\brain\ and load all existing data into Postgres for processing.

## STEP 1: CREATE FOLDER STRUCTURE
Build this exact structure at D:\brain\:

D:\brain\
├── 00_WORKFLOWS\
│   ├── harvest-links\        (RUN.bat, config.json, pipeline.py)
│   ├── classify-documents\   (RUN.bat, config.json, pipeline.py)
│   ├── transcribe-and-classify\ (RUN.bat, config.json, pipeline.py)
│   └── youtube-scrape\       (RUN.bat, config.json, pipeline.py)
├── 01_WHISPER\               (INSTALL.bat, RUN.bat, TEST.bat, TROUBLESHOOT.md, config.json, whisper_runner.py)
├── 02_SBERT\                 (INSTALL.bat, RUN.bat, TEST.bat, TROUBLESHOOT.md, config.json, sbert_runner.py)
├── 03_DEBERTA\               (INSTALL.bat, RUN.bat, TEST.bat, TROUBLESHOOT.md, config.json, deberta_runner.py)
├── 04_HDBSCAN\               (INSTALL.bat, RUN.bat, TEST.bat, TROUBLESHOOT.md, config.json, cluster_runner.py)
├── 05_YOUTUBE\               (INSTALL.bat, RUN.bat, TEST.bat, TROUBLESHOOT.md, config.json, youtube_scraper.py)
├── 06_IMAGES\                (INSTALL.bat, RUN.bat, TEST.bat, TROUBLESHOOT.md, config.json, image_classifier.py)
├── 07_POSTGRES\              (CONNECT.bat, EXPORT.bat, IMPORT.bat, TROUBLESHOOT.md, config.json, db_utils.py)
├── _MODELS\                  (shared model cache)
└── _LOGS\                    (all output logs)

Every RUN.bat uses this Python path:
C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe

## STEP 2: POSTGRES CONNECTION
Host: 192.168.1.177
Port: 2665
User: root
Password: load from local `.env` as `BRAIN_PG_PASSWORD`
Database: crawlab_data

Existing tables you'll work with:
- harvested_links_apologetics (4,539 rows — graded web links)
- scraped_content_apologetics (growing — full page text being extracted now)
- youtube_apologetics (CREATE THIS — load the JSON file below)

## STEP 3: LOAD YOUTUBE DATA INTO POSTGRES
File location: user will provide youtube_apologetics_data.json (3,913 videos)
Create table:

CREATE TABLE IF NOT EXISTS youtube_apologetics (
    id SERIAL PRIMARY KEY,
    video_id VARCHAR(20) UNIQUE,
    title TEXT,
    channel_title TEXT,
    channel_id VARCHAR(30),
    description TEXT,
    published_at TIMESTAMP,
    search_query TEXT,
    thumbnail_url TEXT,
    sbert_embedding BYTEA,
    deberta_label TEXT,
    deberta_confidence FLOAT,
    cluster_id INT,
    scraped_at TIMESTAMP DEFAULT NOW()
);

Load the JSON into this table. Deduplicate on video_id.

## STEP 4: BUILD SBERT RUNNER (02_SBERT)
Model: all-MiniLM-L6-v2 (or all-mpnet-base-v2 if available in _MODELS)
Install: pip install sentence-transformers torch

sbert_runner.py should:
1. Read config.json for input source (postgres table or local directory)
2. Pull all rows where sbert_embedding IS NULL
3. Embed the title + description (for YouTube) or full_text (for scraped content)
4. Store embedding back to the same row as BYTEA
5. Process in batches of 100
6. Log progress to _LOGS/sbert_YYYYMMDD.log
7. Resume from where it left off if interrupted

## STEP 5: BUILD DEBERTA RUNNER (03_DEBERTA)
Model: cross-encoder/nli-deberta-v3-large (or facebook/bart-large-mnli)
Install: pip install transformers torch

Labels for zero-shot classification:
[
    "evidence for God existence",
    "resurrection of Jesus",
    "Bible contradictions",
    "evolution vs creation",
    "Old Testament violence",
    "religion as coping mechanism",
    "problem of evil and suffering",
    "Bible written by humans",
    "religion causes harm",
    "morality without God",
    "religious indoctrination",
    "intelligent design fine tuning",
    "which God is real",
    "ontological argument",
    "slavery in the Bible",
    "God is unfalsifiable",
    "God of the gaps",
    "cherry picking Bible",
    "prayer does not work",
    "cosmological argument",
    "divine hiddenness"
]

deberta_runner.py should:
1. Read config.json for input source
2. Pull all rows where deberta_label IS NULL
3. Run zero-shot classification on title + description
4. Store top label + confidence score back to the row
5. Process in batches of 50 (DeBERTa uses more memory than SBERT)
6. Log progress
7. Resume from where it left off

## STEP 6: BUILD HDBSCAN RUNNER (04_HDBSCAN)
Install: pip install hdbscan numpy

cluster_runner.py should:
1. Pull all SBERT embeddings from a specified table
2. Run HDBSCAN clustering (min_cluster_size=10)
3. Store cluster_id back to each row
4. Output cluster summary: cluster_id, count, representative titles
5. Flag any clusters that don't map to the 21 known labels (potential new attack vectors)

## STEP 7: BUILD YOUTUBE SCRAPER (05_YOUTUBE)
API Key: load from local `.env` as `BRAIN_YOUTUBE_API_KEY`
Store the env var name in config, never hardcode the live key in the script.

youtube_scraper.py should:
1. Read queries from config.json
2. Search YouTube Data API v3
3. Deduplicate against existing youtube_apologetics table
4. Insert new videos
5. Handle quota exceeded gracefully (save progress, exit clean)

## STEP 8: BUILD HARVEST-LINKS WORKFLOW (00_WORKFLOWS)
pipeline.py chains:
1. Input: Excel/CSV file with URLs OR Postgres query
2. Fetch each URL (requests + BeautifulSoup)
3. Extract text
4. Run SBERT embedding
5. Run DeBERTa classification
6. Run HDBSCAN clustering
7. Store to Postgres
8. Export summary report

## STEP 9: TEST EVERYTHING
After building:
1. Run each INSTALL.bat
2. Run each TEST.bat with sample data
3. Run SBERT on 10 YouTube titles as test
4. Run DeBERTa on 10 YouTube titles as test
5. Verify data writes back to Postgres correctly

## IMPORTANT NOTES
- Python path: C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe
- All scripts must handle interruption gracefully (checkpoint progress)
- All scripts must log to D:\brain\_LOGS\
- All config in config.json, never hardcoded
- Postgres credentials in 07_POSTGRES\config.json, referenced by all other scripts
- Process in batches to avoid memory issues
- If a row fails, skip it and log the error, never stop the pipeline
