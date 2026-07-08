"""Consolidate every graded paper's metrics onto ONE Excel sheet.

Scans an export folder for ``*.paper-grade.json`` files (produced by the
paper-proof-grader engine) and writes a single-sheet workbook with one row per
paper and every metric as a column. Scoring logic (grade, 7Q coverage) is reused
directly from the engine so this never drifts from the per-paper reports.

Run standalone:
    python -m paper_grader.consolidate_metrics [EXPORT_DIR] [XLSX_PATH]
It is also called automatically at the end of ``python -m paper_grader``.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# 7Q columns, in canonical order.
_Q_KEYS = [
    ("Q1_identity", "Q1 Identity"),
    ("Q2_scope", "Q2 Scope"),
    ("Q3_mechanism", "Q3 Mechanism"),
    ("Q4_evidence", "Q4 Evidence"),
    ("Q5_falsifiability", "Q5 Falsifiability"),
    ("Q6_boundary", "Q6 Boundary"),
    ("Q7_listener_risk", "Q7 Listener Risk"),
]

HEADERS = (
    [
        "paper_id", "source_file", "generated_at",
        "grade", "grade_confidence", "rigor_verdict",
        "word_count", "section_count", "equation_count", "claim_count",
        "avg_claim_maturity", "max_claim_maturity", "mature_claims_ge4",
    ]
    + [f"{label} coverage %" for _, label in _Q_KEYS]
    + [f"{label} weak#" for _, label in _Q_KEYS]
    + ["top_terms"]
)


def _avg(values: list[float]) -> float:
    return round(sum(values) / len(values), 2) if values else 0.0


def _row(data: dict, grade_fn, coverage_fn) -> list[object]:
    claims = data.get("claims", [])
    metrics = data.get("metrics", {})
    maturities = [int(c.get("claim_maturity_level", 0) or 0) for c in claims]
    grade, confidence, verdict = grade_fn(data)

    coverage = {r["Q_LABEL"]: r for r in coverage_fn(data)}
    cov_pct = [coverage.get(label, {}).get("Q_COVERAGE_PCT", "0") for _, label in _Q_KEYS]
    cov_weak = [coverage.get(label, {}).get("Q_WEAK_COUNT", "0") for _, label in _Q_KEYS]

    return (
        [
            data.get("paper_id", ""),
            data.get("source_file", ""),
            data.get("generated_at", ""),
            grade, confidence, verdict,
            metrics.get("word_count", 0),
            metrics.get("section_count", 0),
            metrics.get("equation_count", 0),
            metrics.get("claim_candidate_count", len(claims)),
            _avg(maturities),
            max(maturities) if maturities else 0,
            sum(1 for m in maturities if m >= 4),
        ]
        + cov_pct
        + cov_weak
        + [metrics.get("top_terms", "")]
    )


def consolidate(output_dir: Path, xlsx_path: Path | None = None) -> Path | None:
    """Build the single consolidated metrics sheet. Returns the written path."""
    output_dir = Path(output_dir)
    xlsx_path = Path(xlsx_path) if xlsx_path else output_dir / "ALL_METRICS.xlsx"

    # Reuse the engine's scoring + xlsx writer (no duplicated logic).
    from pipeline import _dashboard_grade, _q_coverage, _write_minimal_xlsx

    files = sorted(output_dir.glob("*.paper-grade.json"))
    if not files:
        print(f"[consolidate] no *.paper-grade.json found in {output_dir}")
        return None

    rows = [HEADERS]
    for jf in files:
        try:
            data = json.loads(jf.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001 - skip unreadable, keep going
            print(f"[consolidate] skipping {jf.name}: {exc}")
            continue
        rows.append(_row(data, _dashboard_grade, _q_coverage))

    _write_minimal_xlsx(xlsx_path, [("All Metrics", rows)])
    print(f"[consolidate] {len(rows) - 1} paper(s) -> {xlsx_path}")
    return xlsx_path


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    here = Path(__file__).resolve().parent.parent  # the station folder
    output_dir = Path(argv[0]) if argv else here / "EXPORTS" / "paper_grade_runs"
    xlsx_path = Path(argv[1]) if len(argv) > 1 else None

    # The engine lives in the sibling proof-grader station; ensure it's importable.
    try:
        import pipeline  # noqa: F401
    except ModuleNotFoundError:
        from paper_grader.__main__ import _resolve_engine

        sys.path.insert(0, str(_resolve_engine()))

    result = consolidate(output_dir, xlsx_path)
    return 0 if result else 1


if __name__ == "__main__":
    raise SystemExit(main())
