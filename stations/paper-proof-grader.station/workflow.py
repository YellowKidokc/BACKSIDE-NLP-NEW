from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import logging
import shutil
import sys
import zipfile
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).resolve().parent
DEFAULT_INBOX = HERE / "_inbox"
DEFAULT_OUTBOX = HERE / "_outbox" / "workflow"
DEFAULT_PROCESSED = HERE / "_processed" / "workflow"


def _load_module(name: str, path: Path):
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _logger() -> logging.Logger:
    log_dir = HERE / "_logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("paper-grader-workflow")
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    fh = logging.FileHandler(log_dir / f"workflow_{datetime.now():%Y%m%d}.log", encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    logger.addHandler(sh)
    return logger


def _rows_for_workbook(results: list[dict]) -> list[tuple[str, list[list[object]]]]:
    summary = [["paper_id", "claims", "equations", "sections", "proof_grade", "json", "xlsx"]]
    claims = [["paper_id", "claim_id", "section", "claim", "classification", "confidence", "lean_status"]]
    formal = [["paper_id", "proven", "formalizable", "counterexample_found", "not_attempted", "speculative"]]
    artifacts = [["paper_id", "kind", "path"]]
    for item in results:
        data = item["data"]
        metrics = data.get("metrics", {})
        grade = item.get("grade", {})
        summary.append([
            data.get("paper_id", ""), metrics.get("claim_count", len(data.get("claims", []))),
            metrics.get("equation_count", len(data.get("equations", []))), metrics.get("section_count", len(data.get("sections", []))),
            grade.get("grade", ""), item.get("paper_grade_json", ""), item.get("paper_grade_xlsx", ""),
        ])
        lean = data.get("formal_verification", {}).get("lean", {})
        formal.append([data.get("paper_id", ""), lean.get("proven", 0), lean.get("formalizable", 0), lean.get("counterexample_found", 0), lean.get("not_attempted", 0), lean.get("speculative", 0)])
        for claim in data.get("claims", []):
            fv = claim.get("formal_verification", {})
            claims.append([data.get("paper_id", ""), claim.get("claim_id", ""), claim.get("section", ""), claim.get("one_sentence_claim", claim.get("text", "")), claim.get("classification", ""), claim.get("confidence", ""), fv.get("lean", "")])
        for kind, path in item.get("artifacts", {}).items():
            artifacts.append([data.get("paper_id", ""), kind, path])
    return [("Summary", summary), ("Claims", claims), ("Formal", formal), ("Artifacts", artifacts)]


def _write_minimal_xlsx(path: Path, sheets: list[tuple[str, list[list[object]]]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content_types = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>', '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">', '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>', '<Default Extension="xml" ContentType="application/xml"/>', '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>']
    for i, _ in enumerate(sheets, 1):
        content_types.append(f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>')
    content_types.append('</Types>')
    workbook_sheets = ''.join(f'<sheet name="{escape(name[:31])}" sheetId="{i}" r:id="rId{i}"/>' for i, (name, _) in enumerate(sheets, 1))
    workbook = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>{workbook_sheets}</sheets></workbook>'
    rels = ''.join(f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>' for i, _ in enumerate(sheets, 1))
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", ''.join(content_types))
        zf.writestr("_rels/.rels", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>')
        zf.writestr("xl/workbook.xml", workbook)
        zf.writestr("xl/_rels/workbook.xml.rels", f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">{rels}</Relationships>')
        for i, (_, rows) in enumerate(sheets, 1):
            body = []
            for r, row in enumerate(rows, 1):
                cells = []
                for c, value in enumerate(row, 1):
                    col = chr(64 + c) if c <= 26 else f"A{chr(64 + c - 26)}"
                    cells.append(f'<c r="{col}{r}" t="inlineStr"><is><t>{escape(str(value or ""))}</t></is></c>')
                body.append(f'<row r="{r}">{"".join(cells)}</row>')
            zf.writestr(f"xl/worksheets/sheet{i}.xml", f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>{"".join(body)}</sheetData></worksheet>')


def _grade_summary(data: dict) -> dict:
    metrics = data.get("metrics", {})
    claims = data.get("claims", [])
    claim_count = metrics.get("claim_count", len(claims)) or 0
    equation_count = metrics.get("equation_count", len(data.get("equations", []))) or 0
    score = min(100, claim_count * 4 + equation_count * 8)
    return {"score": score, "grade": "A" if score >= 80 else "B" if score >= 60 else "C" if score >= 40 else "NEEDS_WORK"}


def run_workflow(input_path: Path, output_dir: Path = DEFAULT_OUTBOX) -> dict:
    log = _logger()
    legacy = _load_module("paper_grade_legacy", HERE / "pipeline_legacy.py")
    run_id = f"paper-grader-workflow-{datetime.now():%Y%m%d_%H%M%S}"
    output_dir.mkdir(parents=True, exist_ok=True)
    archive_dir = DEFAULT_PROCESSED
    archive_dir.mkdir(parents=True, exist_ok=True)
    archive_path = archive_dir / input_path.name
    if archive_path.exists():
        archive_path = archive_dir / f"{input_path.stem}_{datetime.now():%Y%m%d_%H%M%S}{input_path.suffix}"
    data = legacy._process(input_path, output_dir, log, run_id, archive_path)
    artifacts = {
        "paper_grade_json": str(output_dir / f"{data['paper_id']}.paper-grade.json"),
        "paper_grade_md": str(output_dir / f"{data['paper_id']}.paper-grade.md"),
        "paper_grade_html": str(output_dir / f"{data['paper_id']}.paper-grade.html"),
        "claim_audit_csv": str(output_dir / f"{data['paper_id']}.claim-audit.csv"),
        "paper_grade_xlsx": str(output_dir / f"{data['paper_id']}.paper-grade.xlsx"),
    }
    result = {"paper_id": data["paper_id"], "run_id": run_id, "data": data, "grade": _grade_summary(data), "artifacts": artifacts, **artifacts}
    return result


def run_inbox(input_dir: Path = DEFAULT_INBOX, output_dir: Path = DEFAULT_OUTBOX) -> dict:
    input_dir.mkdir(parents=True, exist_ok=True)
    files = sorted(p for p in input_dir.iterdir() if p.is_file() and p.suffix.lower() in {".md", ".txt", ".html", ".htm"})
    results = [run_workflow(path, output_dir) for path in files]
    workbook = output_dir / f"PAPER_GRADER_WORKFLOW_{datetime.now():%Y%m%d_%H%M%S}.xlsx"
    _write_minimal_xlsx(workbook, _rows_for_workbook(results))
    manifest = {"generated_at": datetime.now().isoformat(timespec="seconds"), "paper_count": len(results), "workbook": str(workbook), "papers": results}
    (output_dir / "workflow_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    return manifest


def main() -> int:
    ap = argparse.ArgumentParser(description="Run the 4-step paper grader workflow and unified workbook export.")
    ap.add_argument("paper", nargs="?", type=Path, help="Paper file to grade. Defaults to _inbox batch mode.")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUTBOX)
    args = ap.parse_args()
    manifest = {"papers": [run_workflow(args.paper, args.out)]} if args.paper else run_inbox(DEFAULT_INBOX, args.out)
    print(json.dumps({"paper_count": len(manifest.get("papers", [])), "workbook": manifest.get("workbook")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
