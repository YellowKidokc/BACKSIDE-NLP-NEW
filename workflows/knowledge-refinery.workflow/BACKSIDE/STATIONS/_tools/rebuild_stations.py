"""
rebuild_stations.py — REWRITE every station.yml + the registry from scratch.

Use after a corrupted renormalize pass. Generates clean files from the template
and a hardcoded config table. Idempotent.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATIONS_DIR = ROOT / "stations"
TEMPLATE_YML = STATIONS_DIR / "_TEMPLATE" / "station.yml"
REGISTRY = ROOT / "stations_registry.yml"

# Per-lane, per-station config. Order matters for registry ordering.
STATIONS = [
    # --- model-wrapping substrate (8) ---
    dict(folder="01_sci_embed",         id="ST-EMBED-001",   lane="embed",
         name="Sci Embed", model="M-EMB-SCI-001", provider="local_wrapper",
         purpose="Embed scientific papers using SPECTER2 for similarity, dedup, and retrieval.",
         input_type="paper_markdown", input_file="source.md",
         output_json="result.json", output_md="result.md",
         gate_rule="non_empty_embedding: true", next_pass="ST-TBD-000", status="draft"),
    dict(folder="02_timeline",          id="ST-TIME-001",    lane="time",
         name="Timeline", model="M-TIME-001", provider="local_wrapper",
         purpose="Extract temporal information (dates, durations, ordering) from text. Stub until David provides recipe.",
         input_type="markdown_article", input_file="source.md",
         output_json="result.json", output_md="result.md",
         gate_rule="has_events: true", next_pass="ST-TBD-000", status="draft"),
    dict(folder="03_nli_strong",        id="ST-NLI-001",     lane="nli",
         name="NLI Strong", model="M-NLI-STRONG-001", provider="local_wrapper",
         purpose="Strong NLI via DeBERTa v3 large — entailment / contradiction / neutral on premise+hypothesis pairs.",
         input_type="claim_pairs_json", input_file="pairs.json",
         output_json="result.json", output_md="result.md",
         gate_rule="all_labels_present: true", next_pass="ST-TBD-000", status="draft"),
    dict(folder="04_nli_claim",         id="ST-NLI-002",     lane="nli",
         name="NLI Claim", model="M-NLI-CLAIM-001", provider="local_wrapper",
         purpose="Claim-verification NLI tuned on MNLI/FEVER/ANLI for fact-checking pipelines.",
         input_type="claim_pairs_json", input_file="pairs.json",
         output_json="result.json", output_md="result.md",
         gate_rule="all_labels_present: true", next_pass="ST-TBD-000", status="draft"),
    dict(folder="05_nli_alt",           id="ST-NLI-003",     lane="nli",
         name="NLI Alt (RoBERTa)", model="M-NLI-ALT-001", provider="local_wrapper",
         purpose="Secondary NLI (RoBERTa large) for adversarial cross-check against the strong NLI.",
         input_type="claim_pairs_json", input_file="pairs.json",
         output_json="result.json", output_md="result.md",
         gate_rule="all_labels_present: true", next_pass="ST-TBD-000", status="draft"),
    dict(folder="06_embed_general",     id="ST-EMBED-002",   lane="embed",
         name="Embed General (MiniLM)", model="M-EMB-GEN-001", provider="local_wrapper",
         purpose="General sentence embeddings (MiniLM) for dedup, routing, and quick similarity.",
         input_type="text_markdown", input_file="source.md",
         output_json="result.json", output_md="result.md",
         gate_rule="non_empty_embedding: true", next_pass="ST-TBD-000", status="draft"),
    dict(folder="07_nli_base",          id="ST-NLI-004",     lane="nli",
         name="NLI Base (legacy)", model="M-NLI-BASE-001", provider="local_wrapper",
         purpose="Baseline NLI (legacy) — kept as fallback / regression baseline.",
         input_type="claim_pairs_json", input_file="pairs.json",
         output_json="result.json", output_md="result.md",
         gate_rule="all_labels_present: true", next_pass="ST-TBD-000", status="draft"),
    dict(folder="08_rerank",            id="ST-RERANK-001",  lane="rerank",
         name="Rerank (cross-encoder)", model="M-RERANK-001", provider="local_wrapper",
         purpose="Cross-encoder reranker — score (query, passage) pairs for retrieval ranking.",
         input_type="query_passages_json", input_file="rerank.json",
         output_json="result.json", output_md="result.md",
         gate_rule="ranked_non_empty: true", next_pass="ST-TBD-000", status="draft"),

    # --- 9-station refinery spine ---
    dict(folder="09_7q_forward",        id="ST-SEVENQ-001",  lane="sevenq",
         name="7Q Forward (classification)", model="gpt-4o-mini", provider="openai",
         purpose="Forward 7-Question Scientific Method — classification pass on a paper (Q0..Q7). What is this paper saying?",
         input_type="paper_markdown", input_file="source.md",
         output_json="forward_7q.json", output_md="forward_7q.md",
         gate_rule="has_claim: true", next_pass="ST-SEVENQ-002", status="draft"),
    dict(folder="10_7q_reverse",        id="ST-SEVENQ-002",  lane="sevenq",
         name="7Q Reverse (kill test)", model="gpt-4o-mini", provider="openai",
         purpose="Reverse 7-Question Scientific Method — adversarial kill test (R1..R7). Find the weakest link, test if the claim survives.",
         input_type="paper_plus_forward_7q", input_file="source.md",
         output_json="reverse_7q.json", output_md="reverse_7q.md",
         gate_rule="has_verdict: true", next_pass="ST-SEVENQ-003", status="draft"),
    dict(folder="11_7q_evidence",       id="ST-SEVENQ-003",  lane="sevenq",
         name="7Q Evidence (pressure)", model="gpt-4o-mini", provider="openai",
         purpose="Evidence pressure pass — classify evidence as direct / indirect / analogical / weak / conflicting; identify gaps; prepare citation targets.",
         input_type="forward_plus_reverse", input_file="source.md",
         output_json="evidence_7q.json", output_md="evidence_7q.md",
         gate_rule="has_evidence_classes: true", next_pass="ST-GRAPH-001", status="draft"),
    dict(folder="12_route_classifier",  id="ST-ROUTE-001",   lane="route",
         name="Route Classifier", model="none", provider="local_wrapper",
         purpose="Inspect a dropped file, detect type (PDF/HTML/MD/DOCX/transcript/audio/video/JSON), assign workflow lane, produce routing.yml.",
         input_type="any_file", input_file="*",
         output_json="routing.yml", output_md="routing.md",
         gate_rule="route_assigned: true", next_pass="ST-CONV-001", status="draft"),
    dict(folder="13_document_converter", id="ST-CONV-001",   lane="conv",
         name="Document Converter", model="none", provider="local_wrapper",
         purpose="Convert source files to clean Markdown using MarkItDown / Docling / Marker dispatch. Extract text, tables, links, images.",
         input_type="routing_yml", input_file="routing.yml",
         output_json="conversion_report.yml", output_md="source.md",
         gate_rule="markdown_produced: true", next_pass="ST-CLAIM-001", status="draft"),
    dict(folder="14_claim_extractor",   id="ST-CLAIM-001",   lane="claim",
         name="Claim Extractor", model="gpt-4o-mini", provider="openai",
         purpose="Read source.md, extract durable claims, assumptions, equations, hypotheses, evidence statements. Assign claim IDs. Dedup against existing claim store.",
         input_type="markdown_article", input_file="source.md",
         output_json="claims.json", output_md="claims.md",
         gate_rule="claims_non_empty: true", next_pass="ST-SUM-001", status="draft"),
    dict(folder="15_lossless_summary",  id="ST-SUM-001",     lane="sum",
         name="Lossless Summary", model="gpt-4o-mini", provider="openai",
         purpose="Preserve the argument without flattening it — keeps claims, evidence, equations, assumptions, argument order, unresolved gaps. NOT a short summary.",
         input_type="source_plus_claims", input_file="source.md",
         output_json="summary.lossless.json", output_md="summary.lossless.md",
         gate_rule="preserves_argument_order: true", next_pass="ST-SEVENQ-001", status="draft"),
    dict(folder="16_knowledge_graph",   id="ST-GRAPH-001",   lane="graph",
         name="Knowledge Graph", model="none", provider="local_wrapper",
         purpose="Turn paper + claims + 7Q outputs + evidence into graph nodes (paper, claim, axiom_candidate, evidence, equation, domain, objection) and edges (supports, contradicts, depends_on, derives_from, maps_to, cites). Export JSON/CSV for Neo4j.",
         input_type="all_prior_artifacts", input_file="source.md",
         output_json="graph.json", output_md="graph.md",
         gate_rule="nodes_and_edges_non_empty: true", next_pass="ST-PUB-001", status="draft"),
    dict(folder="17_publication_gate",  id="ST-PUB-001",     lane="pub",
         name="Publication Gate", model="none", provider="local_wrapper",
         purpose="Read all artifacts. Check readiness (claims extracted, summary exists, reverse pass survived, evidence gaps acceptable, graph built, contradictions resolved). Recommend destination: website / Substack / Zenodo / Proof Explorer / Obsidian Canon / Review / Archive.",
         input_type="all_prior_artifacts", input_file="source.md",
         output_json="publication_status.yml", output_md="release_recommendation.md",
         gate_rule="readiness_threshold_met: true", next_pass="ST-TBD-000", status="draft"),
]


def render_station_yml(template: str, cfg: dict) -> str:
    """Substitute placeholders. Strips inline-comment hints from the template."""
    import re

    mapping = {
        "STATION_ID":       cfg["id"],
        "STATION_NAME":     cfg["name"],
        "LANE":             cfg["lane"],
        "STATUS":           cfg["status"],
        "FOLDER_NAME":      cfg["folder"],
        "PURPOSE":          cfg["purpose"],
        "MODEL_PRIMARY":    cfg["model"],
        "MODEL_FALLBACK":   "",
        "MODEL_PROVIDER":   cfg["provider"],
        "PROMPT_PRIMARY":   "PROMPT_SYSTEM.md",
        "PROMPT_FALLBACK":  "",
        "SCRIPT_RUNNER":    "scripts/03_run_prompt.bat",
        "INPUT_TYPE":       cfg["input_type"],
        "INPUT_FILE":       cfg["input_file"],
        "OUTPUT_FILE_JSON": cfg["output_json"],
        "OUTPUT_FILE_MD":   cfg["output_md"],
        "GATE_RULE":        cfg["gate_rule"],
        "NEXT_STATION_PASS": cfg["next_pass"],
    }
    out = template
    for k, v in mapping.items():
        out = out.replace("{{" + k + "}}", v)
    # Strip trailing inline-comment hints (e.g. "value              # e.g. foo")
    # but ONLY on lines that look like substituted scalar fields.
    cleaned_lines = []
    for line in out.splitlines():
        # match keys we know are scalars and may have a trailing hint
        m = re.match(r"^(\s*(?:station_id|name|lane|status|primary|fallback|provider|runner):\s+)(\S.*?)(\s{2,}#.*)$",
                     line)
        if m:
            cleaned_lines.append(m.group(1) + m.group(2))
        else:
            cleaned_lines.append(line)
    return "\n".join(cleaned_lines) + ("\n" if not out.endswith("\n") else "")


def write_registry(stations: list) -> None:
    lines = [
        "version: 1",
        "# Source of truth for stations. Regenerated by _tools/rebuild_stations.py.",
        "stations:",
    ]
    for cfg in stations:
        lines.extend([
            "",
            f"  - id: {cfg['id']}",
            f"    name: {cfg['name']}",
            f"    lane: {cfg['lane']}",
            f"    status: {cfg['status']}",
            f"    folder: stations/{cfg['folder']}",
            f"    model: {cfg['model']}",
            f"    provider: {cfg['provider']}",
            f"    inputs: [{cfg['input_file']}]",
            f"    outputs: [{cfg['output_json']}, {cfg['output_md']}]",
            f"    next: [{cfg['next_pass']}]",
        ])
    REGISTRY.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    if not TEMPLATE_YML.exists():
        print(f"ERROR: template missing at {TEMPLATE_YML}", file=sys.stderr)
        return 2

    template = TEMPLATE_YML.read_text(encoding="utf-8")

    for cfg in STATIONS:
        target = STATIONS_DIR / cfg["folder"] / "station.yml"
        if not target.parent.exists():
            print(f"WARN: folder missing for {cfg['folder']} — skipping", file=sys.stderr)
            continue
        target.write_text(render_station_yml(template, cfg), encoding="utf-8")
        print(f"  wrote {cfg['folder']:<24} -> {cfg['id']}")

    write_registry(STATIONS)
    print(f"\nRegistry: {REGISTRY}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
