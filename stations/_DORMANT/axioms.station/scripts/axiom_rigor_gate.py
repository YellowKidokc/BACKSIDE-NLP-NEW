from __future__ import annotations

import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FINAL = ROOT / "03_FINAL_READY"
RIGOR_ROOT = ROOT / "06_RIGOR_GATES"

REQUIRED_CLAIM_FIELDS = [
    "one_sentence_claim",
    "claim_maturity_label",
    "forward_test",
    "reverse_test",
    "evidence_bar",
    "kill_conditions",
    "not_claimed",
    "proof_boundary",
    "Q1_identity",
    "Q2_scope",
    "Q3_mechanism",
    "Q4_evidence",
    "Q5_falsifiability",
    "Q6_boundary",
    "Q7_listener_risk",
]

FORMAL_MARKERS = re.compile(r"\b(Lean|Lean4|lake build|theorem|lemma|def |structure |Prop|∀|->|sorry|admit)\b", re.I)
ANTI_RIGOR_MARKERS = re.compile(r"\b(obviously|clearly proves|undeniably proves|physics proves god|must be true)\b", re.I)


def clean_name(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._ -]+", "-", value).strip(" .-_")
    value = re.sub(r"\s+", "-", value)
    return value or "untitled"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def claim_failures(claim: dict) -> list[str]:
    failures = []
    for field in REQUIRED_CLAIM_FIELDS:
        value = str(claim.get(field, "")).strip()
        if not value:
            failures.append(f"missing:{field}")
    weak_values = {
        "Q3_mechanism": {"missing"},
        "Q4_evidence": {"missing"},
        "Q5_falsifiability": {"missing"},
        "Q6_boundary": {"missing"},
    }
    for field, bad in weak_values.items():
        if str(claim.get(field, "")).strip().lower() in bad:
            failures.append(f"weak:{field}")
    text = " ".join(str(claim.get(k, "")) for k in claim)
    if ANTI_RIGOR_MARKERS.search(text):
        failures.append("overclaim_language")
    return failures


def verdict_for(data: dict, failures: list[str], formal_marker_count: int) -> str:
    claims = data.get("claims", [])
    if formal_marker_count and not failures:
        return "FORMALIZATION_CANDIDATE"
    if not claims:
        return "NEEDS_RIGOR"
    if failures:
        return "NEEDS_RIGOR"
    return "AUDIT_READY"


def write_report(bundle: Path, json_path: Path, data: dict, result: dict) -> None:
    series = bundle.parent.name
    paper_id = data.get("paper_id", bundle.name)
    out_dir = RIGOR_ROOT / clean_name(series) / clean_name(str(paper_id))
    out_dir.mkdir(parents=True, exist_ok=True)

    lines = [
        f"# Rigor Gate: {paper_id}",
        "",
        f"- Series: `{series}`",
        f"- Verdict: `{result['verdict']}`",
        f"- Generated: `{result['generated_at']}`",
        f"- Source JSON: `{json_path}`",
        f"- Claim count: {result['claim_count']}",
        f"- Failing claim count: {result['failing_claim_count']}",
        f"- Formal marker count: {result['formal_marker_count']}",
        "",
        "## Meaning",
        "",
        "- `FORMALIZED` is reserved for a verified Lean/Lake build artifact. This gate does not award it automatically.",
        "- `FORMALIZATION_CANDIDATE` means the paper has formal-looking material and no detected audit gaps.",
        "- `AUDIT_READY` means the paper has enough claim/evidence/boundary structure for downstream use, but is not Lean-formalized.",
        "- `NEEDS_RIGOR` means it should not be treated as accepted or reusable without repair.",
        "",
        "## Rejection-First Requirements",
        "",
        "- State the positive claim.",
        "- Name the exact dependency chain.",
        "- Name close false positives.",
        "- Explain why each false positive fails.",
        "- Keep evidence, boundary, and kill conditions separate.",
        "- Log mistakes and overclaims instead of smoothing them away.",
        "",
    ]
    if result["failure_counts"]:
        lines.extend(["## Failure Counts", ""])
        for key, count in sorted(result["failure_counts"].items()):
            lines.append(f"- {key}: {count}")
        lines.append("")
    lines.extend(["## Claim Checks", ""])
    for item in result["claim_results"]:
        lines.append(f"### Claim {item['index']}")
        lines.append("")
        lines.append(f"- Status: `{item['status']}`")
        lines.append(f"- Failures: {', '.join(item['failures']) if item['failures'] else 'none'}")
        lines.append(f"- Claim: {item['claim']}")
        lines.append("")

    (out_dir / "rigor-report.md").write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    (out_dir / "rigor-report.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    bundle_rigor = bundle / "RIGOR_GATE"
    bundle_rigor.mkdir(parents=True, exist_ok=True)
    (bundle_rigor / "rigor-report.md").write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    (bundle_rigor / "rigor-report.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> int:
    RIGOR_ROOT.mkdir(parents=True, exist_ok=True)
    rows = []

    for json_path in sorted(FINAL.rglob("JSON/*.paper-grade.json")):
        bundle = json_path.parents[1]
        data = load_json(json_path)
        text_surface = json.dumps(data, ensure_ascii=False)
        formal_marker_count = len(FORMAL_MARKERS.findall(text_surface))

        claim_results = []
        all_failures = []
        for idx, claim in enumerate(data.get("claims", []), 1):
            failures = claim_failures(claim)
            all_failures.extend(failures)
            claim_results.append({
                "index": idx,
                "status": "PASS" if not failures else "FAIL",
                "failures": failures,
                "claim": str(claim.get("one_sentence_claim", ""))[:800],
            })

        verdict = verdict_for(data, all_failures, formal_marker_count)
        result = {
            "paper_id": data.get("paper_id", bundle.name),
            "series": bundle.parent.name,
            "bundle": str(bundle),
            "source_json": str(json_path),
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "verdict": verdict,
            "claim_count": len(data.get("claims", [])),
            "failing_claim_count": sum(1 for item in claim_results if item["status"] == "FAIL"),
            "formal_marker_count": formal_marker_count,
            "failure_counts": dict(Counter(all_failures)),
            "claim_results": claim_results,
        }
        write_report(bundle, json_path, data, result)
        rows.append({
            "series": result["series"],
            "paper_id": result["paper_id"],
            "verdict": result["verdict"],
            "claim_count": result["claim_count"],
            "failing_claim_count": result["failing_claim_count"],
            "formal_marker_count": result["formal_marker_count"],
            "bundle": result["bundle"],
        })

    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "paper_count": len(rows),
        "verdict_counts": dict(Counter(row["verdict"] for row in rows)),
        "rows": rows,
    }
    (RIGOR_ROOT / "AXIOM_RIGOR_MANIFEST.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = [
        "# Axiom Rigor Manifest",
        "",
        f"- Generated: `{summary['generated_at']}`",
        f"- Papers checked: {summary['paper_count']}",
        "",
        "## Verdict Counts",
        "",
    ]
    for verdict, count in sorted(summary["verdict_counts"].items()):
        lines.append(f"- {verdict}: {count}")
    lines.extend(["", "## Papers", "", "| Series | Paper | Verdict | Claims | Failing | Formal Markers |", "|---|---|---|---:|---:|---:|"])
    for row in rows:
        lines.append(f"| {row['series']} | {row['paper_id']} | {row['verdict']} | {row['claim_count']} | {row['failing_claim_count']} | {row['formal_marker_count']} |")
    (RIGOR_ROOT / "AXIOM_RIGOR_MANIFEST.md").write_text("\n".join(lines).strip() + "\n", encoding="utf-8")

    print(f"Rigor gate checked {len(rows)} papers.")
    print(f"Manifest: {RIGOR_ROOT / 'AXIOM_RIGOR_MANIFEST.md'}")
    print(f"Verdicts: {summary['verdict_counts']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
