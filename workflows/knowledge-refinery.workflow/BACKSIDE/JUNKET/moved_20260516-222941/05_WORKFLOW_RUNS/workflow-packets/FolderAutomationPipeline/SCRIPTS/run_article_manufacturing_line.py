from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from core_transport import sha256, transport


ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / "CONFIG" / "fap_runtime.json").read_text(encoding="utf-8"))
FAP = Path(CFG["runtime_root"])
if not FAP.exists():
    FAP = ROOT
REFINERY = ROOT.parent / "GTQArticlePublicRefinery"
PAPER_GRADER = next(
    (
        parent / "Backside" / "workflows" / "paper-proof-grader.workflow"
        for parent in ROOT.parents
        if parent.name.lower() == "brain"
    ),
    Path(r"\\dlowenas\brain\Backside\workflows\paper-proof-grader.workflow"),
)


def now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def slug(path: Path) -> str:
    safe = "".join(ch.lower() if ch.isalnum() else "-" for ch in path.stem).strip("-")
    while "--" in safe:
        safe = safe.replace("--", "-")
    return safe or "article"


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def run(cmd: list[str], cwd: Path | None = None) -> dict:
    started = now()
    proc = subprocess.run(cmd, cwd=str(cwd) if cwd else None, capture_output=True, text=True)
    return {
        "command": cmd,
        "cwd": str(cwd) if cwd else None,
        "started": started,
        "finished": now(),
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def latest_files_since(folder: Path, since: set[str]) -> list[Path]:
    return [p for p in folder.rglob("*") if p.is_file() and str(p) not in since]


def create_lossless(job_dir: Path, source: Path, refinery_output: Path, refinery_review: Path) -> dict:
    extract = read_json(refinery_output / slug(source) / "article_extract.json")
    canon = read_json(refinery_output / slug(source) / "canon_candidates.json")
    math = read_json(refinery_output / slug(source) / "math_candidates.json")
    glossary = read_json(refinery_output / slug(source) / "glossary_candidates.json")
    blocks = extract.get("blocks", [])
    full_text = "\n\n".join(block.get("text", "") for block in blocks)
    lossless = {
        "schema_version": "fap.lossless_article.v1",
        "generated_at": now(),
        "source": str(source),
        "source_sha256": sha256(source),
        "title": extract.get("title"),
        "text_blocks": blocks,
        "full_text": full_text,
        "canon_candidates": canon,
        "math_candidates": math,
        "glossary_candidates": glossary,
        "refinery_output": str(refinery_output),
        "refinery_review": str(refinery_review),
    }
    write_json(job_dir / "lossless.article.json", lossless)
    write_text(job_dir / "lossless.article.md", f"# {extract.get('title') or source.stem}\n\n{full_text}\n")
    write_text(job_dir / "vector_source.txt", full_text)
    return lossless


def create_vectors(job_dir: Path, lossless: dict) -> None:
    chunks = []
    for block in lossless["text_blocks"]:
        chunks.append(
            {
                "id": block["id"],
                "text": block["text"],
                "source": lossless["source"],
                "title": lossless.get("title"),
                "relationships": [
                    {
                        "family": hit["family"],
                        "anchor": hit["anchor"],
                        "matched_terms": hit["matched_terms"],
                    }
                    for hit in lossless["canon_candidates"]
                    if hit["paragraph_id"] == block["id"]
                ],
            }
        )
    edges = [
        {
            "from": f"paragraph:{hit['paragraph_id']}",
            "to": f"{hit['family']}:{hit['anchor']}",
            "matched_terms": hit["matched_terms"],
            "source": lossless["source"],
        }
        for hit in lossless["canon_candidates"]
    ]
    write_text(job_dir / "chunks.jsonl", "\n".join(json.dumps(row, ensure_ascii=False) for row in chunks) + "\n")
    write_text(job_dir / "relationships.jsonl", "\n".join(json.dumps(row, ensure_ascii=False) for row in edges) + "\n")
    write_json(job_dir / "vector_manifest.json", {"schema_version": "fap.vector_manifest.v1", "chunks": len(chunks), "relationships": len(edges), "generated_at": now()})


def create_station_requests(review_dir: Path, article_slug: str, lossless_path: Path) -> None:
    stations = {
        "executive_summary": "Write a public-facing executive summary. Keep it accurate and shareable.",
        "explain_it_simply": "Explain the article to an everyday reader without academic framing.",
        "math_translation": "Use Math Translation Layer logic. Translate each equation structurally, then plainly.",
        "contradiction_check": "Find internal contradictions, overclaims, or claims that need a kill condition.",
        "bible_reference_check": "Check whether biblical references are used in context and flag weak links.",
        "master_equation_map": "Map paragraphs to Master Equation variables, operators, formal proof anchors, axioms, and derivation remnants.",
        "axiom_derivation_review": "Identify axiom/formal-study/derivation echoes and rate mapping strength.",
        "axiom_rigor_gate": "Apply the Axiom Rigor Protocol. Extract candidate axioms/theorems/mappings, dependency chains, false positives, evidence boundaries, kill conditions, and overclaim risks. Mark each candidate FORMALIZED, FORMALIZATION_CANDIDATE, AUDIT_READY, or NEEDS_RIGOR.",
        "seven_q_forward": "Run the forward 7Q grid over the paper: Q0 posture, Q1 identity, Q2 domain, Q3 claim/assertion, Q4 support/evidence, Q5 dependencies, Q6 consequences, Q7 falsification/kill conditions. Return paragraph evidence for every filled cell.",
        "seven_r_reverse": "Run the reverse 7Q/7R pass. Negate the central claim and major subclaims, then test whether the negation survives Q0-Q7 or self-refutes. Name downstream systems that collapse if the negation holds.",
        "seven_e_evidence": "Run the 7-series evidence pass. Grade evidence quality across the Q0-Q7 dimensions, separating textual support, formal support, empirical support, dependency support, and missing support.",
        "decision_tree_swap_test": "Build the paper's decision tree and swap test: identify branch points, required choices, what changes if the central claim is swapped for its strongest alternative, and which branch breaks first.",
        "post_summary": "Create short post-ready copy for publishing/social/email.",
    }
    for name, instruction in stations.items():
        write_text(
            review_dir / f"{name}.request.md",
            f"""# Station Request - {name}

Article slug: {article_slug}

Use lossless source:

```text
{lossless_path}
```

Task:

{instruction}

Return:

- PASS / REVIEW / FAIL
- output content
- evidence from the article
- exact paragraph ids where relevant
- blockers
""",
        )


def run_paper_grader(source: Path, graded_dir: Path) -> dict:
    drop = PAPER_GRADER / "DROP_PAPERS_HERE"
    output = PAPER_GRADER / "OUTPUT"
    before = {str(p) for p in output.rglob("*") if p.is_file()}
    drop.mkdir(parents=True, exist_ok=True)
    target = drop / source.name
    shutil.copy2(source, target)
    result = run([sys.executable, str(PAPER_GRADER / "pipeline.py")], cwd=PAPER_GRADER)
    new_files = latest_files_since(output, before)
    graded_dir.mkdir(parents=True, exist_ok=True)
    copied = []
    for item in new_files:
        dest = graded_dir / item.name
        shutil.copy2(item, dest)
        copied.append(str(dest))
    write_json(graded_dir / "paper_grader_station_run.json", {"run": result, "copied_outputs": copied})
    return {"returncode": result["returncode"], "copied_outputs": copied}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run FAP article manufacturing line.")
    parser.add_argument("--input", required=True, help="HTML/MD/TXT article file.")
    parser.add_argument("--skip-paper-grader", action="store_true")
    args = parser.parse_args()

    source = Path(args.input)
    if not source.exists():
        raise SystemExit(f"Input not found: {source}")

    article_slug = slug(source)
    job_id = f"{datetime.now():%Y%m%d-%H%M%S}_{article_slug}"
    manifest_dir = FAP / "logs" / job_id
    job_review = FAP / "_review" / job_id
    job_output = FAP / "output" / job_id
    job_lossless = FAP / "lossless" / job_id
    job_vectorized = FAP / "vectorized" / job_id
    job_graded = FAP / "graded" / job_id
    job_axiom = FAP / "axiom-mapped" / job_id
    job_queue = FAP / "_queue" / "pending" / job_id

    stages = []
    for lane in ["intake", "classified", "media-routed"]:
        dest = FAP / lane / job_id
        manifest = manifest_dir / f"{lane}.transport.json"
        records = transport(source, dest, "copy", False, "version", True, manifest)
        stages.append({"stage": lane, "manifest": str(manifest), "records": len(records)})

    classification = {
        "schema_version": "fap.classification.v1",
        "source": str(source),
        "job_id": job_id,
        "document_type": "html_article" if source.suffix.lower() in {".html", ".htm"} else "text_article",
        "routes": ["lossless", "vectorized", "graded", "axiom_mapped", "output"],
        "generated_at": now(),
    }
    write_json(FAP / "classified" / job_id / "classification.json", classification)
    stages.append({"stage": "classify", "status": "pass"})

    refinery_output = job_lossless / "refinery_output"
    refinery_review = job_review / "refinery_review"
    refinery_run = run(
        [
            sys.executable,
            str(REFINERY / "SCRIPTS" / "run_refinery.py"),
            "--input",
            str(source),
            "--output",
            str(refinery_output),
            "--review",
            str(refinery_review),
        ],
        cwd=REFINERY,
    )
    write_json(manifest_dir / "refinery_run.json", refinery_run)
    if refinery_run["returncode"] != 0:
        raise SystemExit(f"Refinery failed: {refinery_run['stderr']}")
    stages.append({"stage": "lossless_refinery", "returncode": refinery_run["returncode"]})

    lossless = create_lossless(job_lossless, source, refinery_output, refinery_review)
    create_vectors(job_vectorized, lossless)
    stages.append({"stage": "lossless", "status": "pass", "path": str(job_lossless / "lossless.article.json")})
    stages.append({"stage": "vectorized", "status": "pass", "path": str(job_vectorized)})

    job_axiom.mkdir(parents=True, exist_ok=True)
    shutil.copy2(job_lossless / "lossless.article.json", job_axiom / "canon_candidates.lossless.article.json")
    write_json(job_axiom / "axiom_mapping_manifest.json", {"schema_version": "fap.axiom_map.v1", "source": str(source), "canon_hits": len(lossless["canon_candidates"]), "status": "candidate_review_required"})
    stages.append({"stage": "axiom_mapped", "status": "review", "path": str(job_axiom)})

    grader = {"skipped": True}
    if not args.skip_paper_grader:
        grader = run_paper_grader(source, job_graded)
    stages.append({"stage": "paper_grader", **grader})

    create_station_requests(job_queue, article_slug, job_lossless / "lossless.article.json")
    shutil.copytree(job_queue, job_review / "station_requests", dirs_exist_ok=True)
    stages.append({"stage": "station_requests", "status": "queued", "path": str(job_queue)})

    final_manifest = {
        "schema_version": "fap.article_manufacturing_run.v1",
        "job_id": job_id,
        "generated_at": now(),
        "source": str(source),
        "source_sha256": sha256(source),
        "stages": stages,
        "outputs": {
            "lossless": str(job_lossless),
            "vectorized": str(job_vectorized),
            "graded": str(job_graded),
            "axiom_mapped": str(job_axiom),
            "review": str(job_review),
            "queue": str(job_queue),
            "output": str(job_output),
        },
    }
    write_json(job_output / "job_manifest.json", final_manifest)
    write_text(job_output / "README.md", f"# FAP Article Manufacturing Output\n\nJob: `{job_id}`\n\nSource: `{source}`\n\nLossless: `{job_lossless}`\n\nReview: `{job_review}`\n\nVectorized: `{job_vectorized}`\n\nGraded: `{job_graded}`\n")
    print(json.dumps(final_manifest, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
