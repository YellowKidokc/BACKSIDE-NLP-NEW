"""
Scaffold the 8 core NLP pipeline stations (ST_001 through ST_008).
POF 2828 | 2026-06-17
Run once to create folder structures, config.json, pipeline.py, RUN.bat, README.md.
"""
import json, os, shutil, textwrap
from pathlib import Path
from datetime import datetime

STATIONS_ROOT = Path(__file__).resolve().parent.parent  # 04_STATIONS
TEMPLATE_PY   = Path(__file__).resolve().parent / "SSS_TEMPLATE_v1.py"

STATIONS = [
    {
        "id": "ST_001", "name": "exec-summary", "folder": "exec-summary.station",
        "desc": "Generate executive summary of a paper or article",
        "nlp": "M01_summarizer",
        "nlp_alt": "M13_bart_summarizer",
        "input_ext": [".md", ".txt", ".json", ".html"],
        "existing_ref": None,
        "notes": "Produces 3-5 sentence executive summary plus key claims list. Can use BART (local) or LLM (Ollama/OpenAI).",
    },
    {
        "id": "ST_002", "name": "plain-language", "folder": "plain-language.station",
        "desc": "Rewrite content at multiple reading levels (easy / standard / academic)",
        "nlp": "M06_llm",
        "nlp_alt": None,
        "input_ext": [".md", ".txt"],
        "existing_ref": "readability-rewriter.station",
        "notes": "LLM-based rewrite at 3 levels. Existing prompt in readability-rewriter.station/prompt.md.",
    },
    {
        "id": "ST_003", "name": "claim-extraction", "folder": "claim-extraction.station",
        "desc": "Extract all claims from text with section context",
        "nlp": "M09_claim_extract",
        "nlp_alt": None,
        "input_ext": [".md", ".txt", ".html"],
        "existing_ref": "claim-extractor.station",
        "notes": "Core logic in claim-extractor.station/extract.py. Outputs claim-audit CSV.",
    },
    {
        "id": "ST_004", "name": "claim-classification", "folder": "claim-classification.station",
        "desc": "Classify extracted claims by type, maturity, and domain",
        "nlp": "M02_embedder",
        "nlp_alt": "deberta-runner (DeBERTa NLI)",
        "input_ext": [".json", ".csv"],
        "existing_ref": "classify-documents.station + mda-citation-spine.station/claim_inventory.py",
        "notes": "Two-stage: SBERT embedding for similarity, then DeBERTa NLI for maturity labels. Triage logic in claim_inventory.py.",
    },
    {
        "id": "ST_005", "name": "load-bearing-claims", "folder": "load-bearing-claims.station",
        "desc": "Identify structurally load-bearing claims vs rhetoric/narrative/metadata",
        "nlp": "M06_llm",
        "nlp_alt": None,
        "input_ext": [".json", ".csv"],
        "existing_ref": "mda-citation-spine.station/claim_inventory.py (LOAD_BEARING_SECTION_WORDS, MODEL_CLAIM_TERMS)",
        "notes": "Separates claims into PAPER_CLAIM_QUEUE, CITATION_FACT_QUEUE, REVIEW_QUEUE, PARK. Key logic already in claim_inventory.py classify() function.",
    },
    {
        "id": "ST_006", "name": "falsification", "folder": "falsification.station",
        "desc": "Test claims for falsifiability, generate kill conditions",
        "nlp": "M07_fact_verify",
        "nlp_alt": "M06_llm",
        "input_ext": [".json"],
        "existing_ref": "fact-verifier.station",
        "notes": "For each load-bearing claim: generate explicit kill condition, evidence bar, falsification test. LLM reasoning required.",
    },
    {
        "id": "ST_007", "name": "evidence-map", "folder": "evidence-map.station",
        "desc": "Map evidence to claims, identify gaps and unsupported claims",
        "nlp": "M02_embedder",
        "nlp_alt": "M06_llm",
        "input_ext": [".json"],
        "existing_ref": None,
        "notes": "New station. Semantic matching (SBERT) between claims and evidence passages. Output: evidence coverage map with gap flags.",
    },
    {
        "id": "ST_008", "name": "contradiction-scan", "folder": "contradiction-scan.station",
        "desc": "Scan for internal contradictions between claims across articles",
        "nlp": "M03_contradiction",
        "nlp_alt": "M08_contradiction_deep",
        "input_ext": [".json"],
        "existing_ref": "contradiction-detector.station + contradiction-deep.station",
        "notes": "Two-pass: shallow DeBERTa NLI scan (M03), then deep LLM analysis on flagged pairs (M08). Cross-article scope.",
    },
]

def make_config(s):
    return {
        "station_id": s["id"],
        "station_name": s["name"],
        "station_type": "one_for_one",
        "description": s["desc"],
        "input_extensions": s["input_ext"],
        "workers": {
            "default": [s["nlp"]],
            "optional": [s["nlp_alt"]] if s["nlp_alt"] else []
        },
        "outputs": {
            "artifact_type": "json",
            "update_job_card": False,
            "final_export": False
        },
        "templates": {}
    }


def make_pipeline(s, template_text):
    """Patch the SSS_v1 template with station-specific identity."""
    code = template_text
    code = code.replace('STATION_ID   = "ST_000"', f'STATION_ID   = "{s["id"]}"')
    code = code.replace('STATION_NAME = "template_station"', f'STATION_NAME = "{s["name"]}"')
    code = code.replace('STATION_DESC = "SSS_v1 template — replace with station description"',
                        f'STATION_DESC = "{s["desc"]}"')
    return code

def make_run_bat(s):
    return f"""@echo off
echo ========================================
echo  {s["id"]} — {s["name"]}
echo  {s["desc"]}
echo ========================================
cd /d "%~dp0"
python pipeline.py
if errorlevel 1 (
    echo [FAIL] Station {s["name"]} exited with errors.
    pause
) else (
    echo [OK] Station {s["name"]} complete.
    pause
)
"""

def make_readme(s):
    lines = [
        f"# {s['folder']}",
        f"",
        f"**{s['id']}** | Core NLP Pipeline Station",
        f"",
        f"## Purpose",
        f"",
        f"{s['desc']}",
        f"",
        f"## NLP Model",
        f"",
        f"- **Primary:** `{s['nlp']}`",
    ]
    if s["nlp_alt"]:
        lines.append(f"- **Alternative:** `{s['nlp_alt']}`")
    lines.extend([
        f"",
        f"## Existing Code Reference",
        f"",
        f"{'`' + s['existing_ref'] + '`' if s['existing_ref'] else 'New station — no prior implementation.'}",
        f"",
        f"## Notes",
        f"",
        f"{s['notes']}",
        f"",
        f"## Pipeline Position",
        f"",
        f"```",
        f"ST_001 -> ST_002 -> ST_003 -> ST_004 -> ST_005 -> ST_006 -> ST_007 -> ST_008",
        f"  exec     plain    claim     classify  load-     falsif   evidence  contradict",
        f"  summary  language extract   claims    bearing            map       scan",
        f"```",
        f"",
        f"## Standard Folders",
        f"",
        f"- `_inbox/` — inputs land here",
        f"- `_outbox/` — JSON artifacts go here",
        f"- `_processed/` — archived inputs",
        f"- `_logs/` — execution logs",
        f"- `_state/` — persistent state",
    ])
    return "\n".join(lines) + "\n"


def main():
    template_text = TEMPLATE_PY.read_text(encoding="utf-8")

    for s in STATIONS:
        station_dir = STATIONS_ROOT / s["folder"]
        print(f"Creating {s['id']} — {s['folder']}...")

        # Create directories
        for sub in ["_inbox", "_outbox", "_processed", "_logs", "_state"]:
            (station_dir / sub).mkdir(parents=True, exist_ok=True)
            gitkeep = station_dir / sub / ".gitkeep"
            if not gitkeep.exists():
                gitkeep.write_text("")

        # config.json
        cfg = make_config(s)
        (station_dir / "config.json").write_text(
            json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )

        # pipeline.py
        pipeline = make_pipeline(s, template_text)
        (station_dir / "pipeline.py").write_text(pipeline, encoding="utf-8")

        # RUN.bat
        (station_dir / "RUN.bat").write_text(make_run_bat(s), encoding="utf-8")

        # README.md
        (station_dir / "README.md").write_text(make_readme(s), encoding="utf-8")

        print(f"  OK {station_dir}")

    # Write cheat sheet
    cheat = [
        "# Core 8 NLP Pipeline Stations - Cheat Sheet",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "## Pipeline Sequence",
        "",
        "```",
        "ST_001 exec-summary       ->  M01_summarizer / M13_bart_summarizer",
        "ST_002 plain-language      ->  M06_llm",
        "ST_003 claim-extraction    ->  M09_claim_extract",
        "ST_004 claim-classification -> M02_embedder + DeBERTa",
        "ST_005 load-bearing-claims ->  M06_llm (claim_inventory.py logic)",
        "ST_006 falsification       ->  M07_fact_verify + M06_llm",
        "ST_007 evidence-map        ->  M02_embedder + M06_llm",
        "ST_008 contradiction-scan  ->  M03_contradiction + M08_contradiction_deep",
        "```",
        "",
        "## NLP Model Registry (X:\\05_MODELS\\)",
        "",
        "| ID  | Model | Used By |",
        "|-----|-------|---------|",
        "| M01 | summarizer | ST_001 |",
        "| M02 | embedder (SBERT) | ST_004, ST_007, sbert-embedder.station |",
        "| M03 | contradiction (DeBERTa NLI) | ST_008, deberta-runner.station |",
        "| M04 | imager | image-processor.station |",
        "| M05 | transcriber | whisper-transcribe.station |",
        "| M06 | llm (Ollama/OpenAI) | ST_002, ST_005, ST_006, ST_007, llm-runner.station |",
        "| M07 | fact_verify | ST_006, fact-verifier.station |",
        "| M08 | contradiction_deep | ST_008, contradiction-deep.station |",
        "| M09 | claim_extract | ST_003, claim-extractor.station |",
        "| M10 | timeline | timeline-verifier.station |",
        "| M11 | math_verify | math-verify.station |",
        "| M12 | paper_review | paper-review.station |",
        "| M13 | bart_summarizer | ST_001 (alt) |",
        "| M14 | clip_vision | image-processor.station |",
        "| M15 | mistral_7b | (reserved) |",
        "| M16 | whisper_large_v3 | whisper-transcribe.station |",
        "",
        "## Existing Code to Migrate",
        "",
    ]
    for s in STATIONS:
        ref = s["existing_ref"] or "NEW — write from scratch"
        cheat.append(f"- **{s['id']} {s['name']}**: {ref}")
    cheat.append("")
    cheat.append("## What Codex Needs To Do")
    cheat.append("")
    cheat.append("For each station, implement ONLY sections 06 and 07 in pipeline.py:")
    cheat.append("- Section 06 (NLP_ROUTE): Load the correct model, handle fallbacks")
    cheat.append("- Section 07 (PROCESS): The actual processing logic")
    cheat.append("Everything else (ingest, validate, artifacts, archive) is already handled by SSS_v1.")
    cheat.append("")

    cheat_path = STATIONS_ROOT / "_shared" / "CORE_8_NLP_CHEAT_SHEET.md"
    cheat_path.write_text("\n".join(cheat) + "\n", encoding="utf-8")
    print(f"\nOK Cheat sheet: {cheat_path}")
    print(f"\nDONE - 8 stations scaffolded.")


if __name__ == "__main__":
    main()
