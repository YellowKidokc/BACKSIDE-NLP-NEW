from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
SUITE_DIR = HERE.parent
PAPER_INTELLIGENCE_OUTPUT = SUITE_DIR / "OUTPUT" / "brain_alignment"
BRAIN_ARM_DIR = SUITE_DIR / "14_OBSIDIAN_BRAIN_ARM"

for path in (HERE, BRAIN_ARM_DIR):
    as_str = str(path)
    if as_str not in sys.path:
        sys.path.insert(0, as_str)

from run_pipeline import HAS_EXCEL, _aggregate_layer_health, analyze_paper, write_excel  # noqa: E402
from obsidian_pipeline import run_obsidian_sync  # noqa: E402


SKIP_DIRS = {
    ".git",
    ".obsidian",
    "__pycache__",
    "node_modules",
    "_paper_intelligence",
}


def _slugify(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_")
    return cleaned[:80] or "folder"


def _normalize_path(path: str) -> str:
    try:
        return str(Path(path).resolve()).lower()
    except Exception:
        return str(Path(path)).lower()


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _iter_markdown_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for current_root, dir_names, file_names in __import__("os").walk(root):
        dir_names[:] = [d for d in dir_names if d.lower() not in SKIP_DIRS]
        base = Path(current_root)
        for file_name in file_names:
            if file_name.lower().endswith(".md"):
                files.append(base / file_name)
    return sorted(files)


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, default=str), encoding="utf-8")


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return

    fieldnames: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row.keys():
            if key not in seen:
                seen.add(key)
                fieldnames.append(key)

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            flattened = {
                key: "; ".join(value) if isinstance(value, list) else value
                for key, value in row.items()
            }
            writer.writerow(flattened)


def _ensure_folder(folder_path: str | Path) -> Path:
    folder = Path(folder_path).expanduser()
    if not folder.exists() or not folder.is_dir():
        raise FileNotFoundError(f"Folder not found or not a directory: {folder}")
    return folder


def _run_paper_side(folder: Path, out_dir: Path, run_openai: bool = False) -> dict[str, Any]:
    paper_dir = out_dir
    paper_dir.mkdir(parents=True, exist_ok=True)
    snapshot_dir = paper_dir / "snapshots"
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_slug = _slugify(folder.name)
    papers = _iter_markdown_files(folder)
    series_id = f"BA-{hashlib.sha1(str(folder.resolve()).lower().encode('utf-8')).hexdigest()[:10]}"

    paper_rows: list[dict[str, Any]] = []
    for paper in papers:
        row = analyze_paper(
            str(paper),
            run_openai=run_openai,
            vault_output=str(paper.parent),
            series_id=series_id,
            run_id=run_id,
            snapshot_dir=str(snapshot_dir),
            identity_overrides={"series": folder.name},
        )
        paper_rows.append(row)

    try:
        import graph_builder as L7  # noqa: N812

        graph_result = L7.build_graph(paper_rows, str(paper_dir))
        for row in paper_rows:
            node_data = graph_result.get("node_data", {}).get(row.get("file", ""), {})
            row["L7_centrality_within_series"] = node_data.get("centrality", "")
            row["L7_cluster"] = node_data.get("cluster", "")
            row.setdefault("_layer_status", {})["L7"] = "ok"
    except Exception as exc:
        for row in paper_rows:
            row.setdefault("_layer_status", {})["L7"] = "error"
            row["L7_error"] = str(exc)

    paper_json = paper_dir / "paper_rows.json"
    _write_json(paper_json, paper_rows)

    excel_path = None
    if HAS_EXCEL and paper_rows:
        excel_path = paper_dir / f"{folder_slug}_paper_intelligence_{run_id}.xlsx"
        write_excel(paper_rows, excel_path)

    summary = {
        "markdown_files_analyzed": len(paper_rows),
        "rows_json": str(paper_json),
        "excel": str(excel_path) if excel_path else None,
        "snapshot_dir": str(snapshot_dir),
        "layer_health": _aggregate_layer_health(paper_rows),
        "run_id": run_id,
        "folder_path_requested": str(folder),
        "folder_path_resolved": str(folder.resolve()),
    }
    return {
        "paper_rows": paper_rows,
        "paper_json": paper_json,
        "excel_path": excel_path,
        "snapshot_dir": snapshot_dir,
        "summary": summary,
    }


def _run_brain_side(folder: Path, out_dir: Path) -> dict[str, Any]:
    brain_dir = out_dir
    brain_dir.mkdir(parents=True, exist_ok=True)
    brain_result = run_obsidian_sync(
        vault_path=str(folder),
        data_root=str(brain_dir),
        publish_html_dirs=[],
    )
    brain_records = _load_json(Path(brain_result["outputs"]["classified_json"]))
    markdown_records = [
        record for record in brain_records
        if record.get("source_type") == "note" and str(record.get("source_path", "")).lower().endswith(".md")
    ]
    summary = {
        "total_docs": brain_result["total_docs"],
        "markdown_note_docs": len(markdown_records),
        "summary": brain_result["summary"],
        "classified_json": brain_result["outputs"]["classified_json"],
        "classified_jsonl": brain_result["outputs"]["classified_jsonl"],
        "digest_html": brain_result["outputs"]["digest_html"],
        "digest_csv": brain_result["outputs"]["digest_csv"],
        "folder_path_requested": str(folder),
        "folder_path_resolved": str(folder.resolve()),
    }
    return {
        "brain_result": brain_result,
        "brain_records": brain_records,
        "summary": summary,
    }


def run_paper_only(folder_path: str, output_path: str | None = None, run_openai: bool = False) -> dict[str, Any]:
    folder = _ensure_folder(folder_path)
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_slug = _slugify(folder.name)
    default_output = SUITE_DIR / "OUTPUT" / "paper_only" / f"{folder_slug}_{run_id}"
    out_dir = Path(output_path).expanduser() if output_path else default_output
    out_dir.mkdir(parents=True, exist_ok=True)

    paper_side = _run_paper_side(folder, out_dir / "paper_intelligence", run_openai=run_openai)
    summary = {
        "run_id": run_id,
        "folder_path_requested": str(folder),
        "folder_path_resolved": str(folder.resolve()),
        "output_dir": str(out_dir.resolve()),
        "openai_enabled": run_openai,
        "paper_intelligence": paper_side["summary"],
    }
    summary_path = out_dir / "paper_only_summary.json"
    _write_json(summary_path, summary)
    summary["summary_path"] = str(summary_path)
    return summary


def run_brain_only(folder_path: str, output_path: str | None = None) -> dict[str, Any]:
    folder = _ensure_folder(folder_path)
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_slug = _slugify(folder.name)
    default_output = SUITE_DIR / "OUTPUT" / "brain_only" / f"{folder_slug}_{run_id}"
    out_dir = Path(output_path).expanduser() if output_path else default_output
    out_dir.mkdir(parents=True, exist_ok=True)

    brain_side = _run_brain_side(folder, out_dir / "brain_arm")
    summary = {
        "run_id": run_id,
        "folder_path_requested": str(folder),
        "folder_path_resolved": str(folder.resolve()),
        "output_dir": str(out_dir.resolve()),
        "brain_arm": brain_side["summary"],
    }
    summary_path = out_dir / "brain_only_summary.json"
    _write_json(summary_path, summary)
    summary["summary_path"] = str(summary_path)
    return summary


def run_alignment(folder_path: str, output_path: str | None = None, run_openai: bool = False) -> dict[str, Any]:
    folder = _ensure_folder(folder_path)
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_slug = _slugify(folder.name)
    default_output = PAPER_INTELLIGENCE_OUTPUT / f"{folder_slug}_{run_id}"
    out_dir = Path(output_path).expanduser() if output_path else default_output
    out_dir.mkdir(parents=True, exist_ok=True)

    paper_side = _run_paper_side(folder, out_dir / "paper_intelligence", run_openai=run_openai)
    paper_rows = paper_side["paper_rows"]
    paper_by_path = {_normalize_path(row["source_path"]): row for row in paper_rows}

    brain_side = _run_brain_side(folder, out_dir / "brain_arm")
    brain_result = brain_side["brain_result"]
    brain_records = brain_side["brain_records"]

    brain_by_path = {_normalize_path(record["source_path"]): record for record in brain_records}

    alignment_rows: list[dict[str, Any]] = []
    for row in paper_rows:
        normalized = _normalize_path(row["source_path"])
        brain_record = brain_by_path.get(normalized, {})
        alignment_rows.append(
            {
                "paper_id": row.get("paper_id", ""),
                "file": row.get("file", ""),
                "source_path": row.get("source_path", ""),
                "match_status": "matched" if brain_record else "missing_brain_record",
                "paper_word_count": row.get("L1_word_count", ""),
                "paper_text_standard": row.get("L1_text_standard", ""),
                "paper_fk_grade": row.get("L1_flesch_kincaid_grade", ""),
                "paper_chi_score": row.get("L3_chi_score", ""),
                "paper_ckg_tier": row.get("L3_ckg_tier", ""),
                "paper_claim_markers": row.get("L2_claim_marker_count", ""),
                "paper_claims_truth_engine": row.get("L6_claim_count", ""),
                "paper_claims_groundup": row.get("PA_a_claim_count", ""),
                "paper_truth_score": row.get("L6_truth_score", ""),
                "paper_combined_score": row.get("L6_combined_score", ""),
                "paper_snapshot_path": row.get("snapshot_path", ""),
                "brain_relative_path": brain_record.get("relative_path", ""),
                "brain_source_path": brain_record.get("source_path", ""),
                "brain_title": brain_record.get("title", ""),
                "brain_knowledge_type": brain_record.get("knowledge_type", ""),
                "brain_domain": brain_record.get("domain", ""),
                "brain_status": brain_record.get("status", ""),
                "brain_tags": brain_record.get("tags", []),
                "brain_summary": brain_record.get("summary", ""),
            }
        )

    alignment_csv = out_dir / "alignment_join.csv"
    alignment_json = out_dir / "alignment_join.json"
    _write_csv(alignment_csv, alignment_rows)
    _write_json(alignment_json, alignment_rows)

    brain_markdown_records = [
        record for record in brain_records
        if record.get("source_type") == "note" and str(record.get("source_path", "")).lower().endswith(".md")
    ]
    matched_markdown = sum(1 for row in alignment_rows if row["match_status"] == "matched")
    missing_from_brain = [
        row["source_path"] for row in alignment_rows
        if row["match_status"] != "matched"
    ]
    missing_from_paper = [
        record["source_path"] for record in brain_markdown_records
        if _normalize_path(record["source_path"]) not in paper_by_path
    ]

    summary = {
        "run_id": run_id,
        "folder_path_requested": str(folder),
        "folder_path_resolved": str(folder.resolve()),
        "output_dir": str(out_dir.resolve()),
        "openai_enabled": run_openai,
        "paper_intelligence": paper_side["summary"],
        "brain_arm": brain_side["summary"],
        "alignment": {
            "matched_markdown_docs": matched_markdown,
            "paper_docs_missing_in_brain_arm": missing_from_brain,
            "brain_markdown_docs_missing_in_paper_intelligence": missing_from_paper,
            "alignment_csv": str(alignment_csv),
            "alignment_json": str(alignment_json),
        },
    }

    summary_path = out_dir / "alignment_summary.json"
    _write_json(summary_path, summary)
    summary["summary_path"] = str(summary_path)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run Paper Intelligence and the Obsidian Brain Arm on the same folder, then compare outputs.",
    )
    parser.add_argument("--folder", required=True, help="Vault subfolder or paper folder to align.")
    parser.add_argument("--output", help="Optional explicit output directory.")
    parser.add_argument("--openai", action="store_true", help="Enable OpenAI-backed layers.")
    args = parser.parse_args()

    result = run_alignment(
        folder_path=args.folder,
        output_path=args.output,
        run_openai=args.openai,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
