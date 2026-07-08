from __future__ import annotations

import argparse
import csv
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


STATION_DIR = Path(__file__).resolve().parent
CONFIG_PATH = STATION_DIR / "config.json"


def load_config() -> dict[str, Any]:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def article_id(path: Path) -> str:
    return path.stem


def slug_stamp() -> str:
    return datetime.now().strftime("run_%Y%m%d_%H%M%S")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run MDA citation spine NLP passes.")
    parser.add_argument("--article", help="Article filename or stem to run.")
    parser.add_argument("--all", action="store_true", help="Run all articles.")
    parser.add_argument("--limit", type=int, default=None, help="Run the first N articles.")
    parser.add_argument("--dry-run", action="store_true", help="Show OpenAI runner plan without API calls.")
    parser.add_argument("--tools", default=None, help="Comma-separated tools. Default from config.")
    parser.add_argument("--concurrent", type=int, default=3, help="Max concurrent OpenAI calls.")
    parser.add_argument("--python", default=sys.executable, help="Python executable to use.")
    return parser.parse_args()


def resolve_articles(articles_dir: Path, args: argparse.Namespace) -> list[Path]:
    articles = sorted(articles_dir.glob("MDA-*.md"))
    if args.article:
        wanted = args.article
        if not wanted.lower().endswith(".md"):
            wanted = wanted + ".md"
        matches = [path for path in articles if path.name.lower() == wanted.lower()]
        if not matches:
            matches = [path for path in articles if path.stem.lower() == args.article.lower()]
        if not matches:
            raise SystemExit(f"Article not found under {articles_dir}: {args.article}")
        return matches
    if args.all:
        return articles
    if args.limit:
        return articles[: args.limit]
    raise SystemExit("Choose --article, --limit, or --all.")


def run_openai_runner(
    python_exe: str,
    runner: Path,
    article: Path,
    raw_dir: Path,
    tools: str,
    concurrent: int,
    dry_run: bool,
) -> subprocess.CompletedProcess[str]:
    raw_dir.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["OPENAI_RUNNER_ANNOTATE_SOURCE"] = "0"
    cmd = [
        python_exe,
        str(runner),
        str(article),
        "--tools",
        tools,
        "--output",
        str(raw_dir),
        "--concurrent",
        str(concurrent),
    ]
    if dry_run:
        cmd.append("--dry-run")
    return subprocess.run(cmd, cwd=str(runner.parent), env=env, text=True, capture_output=True)


def load_json_if_exists(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def parse_extractor(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8", errors="replace").strip()
    if not text:
        return None
    if text.startswith("{"):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return None
    match = re.search(r"```json\s*(.*?)\s*```", text, flags=re.DOTALL | re.IGNORECASE)
    if not match:
        return None
    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError:
        return None


def write_claims(packet_dir: Path, aid: str, judge: dict[str, Any] | None) -> list[dict[str, Any]]:
    claims: list[dict[str, Any]] = []
    for idx, item in enumerate((judge or {}).get("claim_decomposition", []), start=1):
        kill = str(item.get("kill_condition") or "").strip()
        status = "NEEDS_KILL_CONDITION" if not kill else "MODEL_EXTRACTED"
        claims.append(
            {
                "article_id": aid,
                "claim_id": str(item.get("id") or f"claim_{idx:03d}"),
                "statement": str(item.get("statement") or "").strip(),
                "kill_condition": kill,
                "status": status,
                "source_stage": "7q_judge",
                "notes": "OpenAI model extraction; requires human review before canonical use.",
            }
        )
    (packet_dir / "claims.json").write_text(json.dumps(claims, indent=2, ensure_ascii=False), encoding="utf-8")
    return claims


def citation_rows(
    aid: str,
    academic: dict[str, Any] | None,
    extractor: dict[str, Any] | None,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    citation_check = (academic or {}).get("citation_check", {})
    for item in citation_check.get("suspect_citations", []) or []:
        rows.append(
            {
                "article_id": aid,
                "status": "SUSPECT",
                "source_stage": "academic",
                "citation": str(item.get("citation") or ""),
                "doi_or_arxiv": "",
                "title": "",
                "first_author": "",
                "relevance": str(item.get("reason") or ""),
                "priority": "",
                "notes": "Model flagged suspect citation; verify manually.",
            }
        )
    for item in citation_check.get("missing_citations", []) or []:
        rows.append(
            {
                "article_id": aid,
                "status": "MISSING_CANDIDATE",
                "source_stage": "academic",
                "citation": "",
                "doi_or_arxiv": str(item.get("doi_or_arxiv") or ""),
                "title": str(item.get("title") or ""),
                "first_author": str(item.get("author") or item.get("first_author") or ""),
                "relevance": str(item.get("relevance") or ""),
                "priority": str(item.get("priority") or ""),
                "notes": "Candidate only; not verified.",
            }
        )
    for item in (extractor or {}).get("missing_citations", []) or []:
        rows.append(
            {
                "article_id": aid,
                "status": "MISSING_CANDIDATE",
                "source_stage": "extractor",
                "citation": "",
                "doi_or_arxiv": str(item.get("doi") or item.get("doi_or_arxiv") or ""),
                "title": str(item.get("title") or ""),
                "first_author": str(item.get("first_author") or item.get("author") or ""),
                "relevance": str(item.get("relevance") or ""),
                "priority": str(item.get("priority") or ""),
                "notes": "Candidate only; not verified.",
            }
        )
    gaps = citation_check.get("evidence_claim_alignment", {}).get("gaps", []) if citation_check else []
    for item in gaps or []:
        rows.append(
            {
                "article_id": aid,
                "status": "EVIDENCE_GAP",
                "source_stage": "academic",
                "citation": str(item.get("evidence_cited") or ""),
                "doi_or_arxiv": "",
                "title": "",
                "first_author": "",
                "relevance": str(item.get("gap_description") or item.get("claim") or ""),
                "priority": "essential",
                "notes": "Claim-evidence gap from model review.",
            }
        )
    if not rows:
        rows.append(
            {
                "article_id": aid,
                "status": "NO_MODEL_CITATION_FLAGS",
                "source_stage": "academic/extractor",
                "citation": "",
                "doi_or_arxiv": "",
                "title": "",
                "first_author": "",
                "relevance": "",
                "priority": "",
                "notes": "This is not source verification; it only means the model did not flag citation gaps.",
            }
        )
    return rows


def write_citation_csv(packet_dir: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = [
        "article_id",
        "status",
        "source_stage",
        "citation",
        "doi_or_arxiv",
        "title",
        "first_author",
        "relevance",
        "priority",
        "notes",
    ]
    with (packet_dir / "citation-status.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_falsification(packet_dir: Path, aid: str, claims: list[dict[str, Any]], judge: dict[str, Any] | None) -> None:
    decisive = (judge or {}).get("decisive_untested_prediction", {})
    payload = {
        "article_id": aid,
        "source_stage": "7q_judge",
        "kill_conditions": [
            {
                "claim_id": item["claim_id"],
                "statement": item["statement"],
                "kill_condition": item["kill_condition"],
                "status": item["status"],
            }
            for item in claims
        ],
        "decisive_untested_prediction": decisive,
        "notes": "Model-generated falsification packet; requires human review.",
    }
    (packet_dir / "falsification.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def normalize_article(raw_dir: Path, packet_root: Path, article: Path) -> dict[str, Any]:
    aid = article_id(article)
    packet_dir = packet_root / aid
    packet_dir.mkdir(parents=True, exist_ok=True)

    judge = load_json_if_exists(raw_dir / f"{aid}_7Q_JUDGE.json")
    academic = load_json_if_exists(raw_dir / f"{aid}_ACADEMIC.json")
    extractor = load_json_if_exists(raw_dir / f"{aid}_EXTRACTOR.json")
    if extractor is None:
        extractor = parse_extractor(raw_dir / f"{aid}_extractor.md")

    claims = write_claims(packet_dir, aid, judge)
    crows = citation_rows(aid, academic, extractor)
    write_citation_csv(packet_dir, crows)
    write_falsification(packet_dir, aid, claims, judge)

    summary = {
        "article_id": aid,
        "claims": len(claims),
        "claims_needing_kill_conditions": sum(1 for item in claims if item["status"] == "NEEDS_KILL_CONDITION"),
        "citation_rows": len(crows),
        "citation_flags": sum(1 for item in crows if item["status"] != "NO_MODEL_CITATION_FLAGS"),
        "judge_parsed": judge is not None,
        "academic_parsed": academic is not None,
        "extractor_parsed": extractor is not None,
    }
    (packet_dir / "openai-summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def write_run_report(run_dir: Path, manifest: dict[str, Any]) -> None:
    lines = [
        "# MDA Citation Spine Run",
        "",
        f"- Run ID: {manifest['run_id']}",
        f"- Generated: {manifest['generated_at']}",
        f"- Dry run: {manifest['dry_run']}",
        f"- Articles requested: {len(manifest['articles'])}",
        f"- Total cost reported: ${manifest.get('total_cost_usd', 0):.6f}",
        "",
        "| Article | Status | Claims | Citation Flags | Notes |",
        "|---|---:|---:|---:|---|",
    ]
    for item in manifest["articles"]:
        lines.append(
            f"| {item['article_id']} | {item['status']} | {item.get('claims', 0)} | "
            f"{item.get('citation_flags', 0)} | {item.get('notes', '')} |"
        )
    (run_dir / "RUN_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    config = load_config()
    articles_dir = Path(config["inputs"]["articles_dir"])
    exports_dir = Path(config["outputs"]["exports_dir"])
    runner = Path(config["openai_runner"]["path"])
    tools = args.tools or config["openai_runner"]["default_tools"]
    articles = resolve_articles(articles_dir, args)

    run_id = slug_stamp()
    run_dir = exports_dir / "runs" / run_id
    raw_root = run_dir / "raw_openai"
    packet_root = run_dir / "packets"
    run_dir.mkdir(parents=True, exist_ok=True)

    manifest: dict[str, Any] = {
        "run_id": run_id,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "dry_run": bool(args.dry_run),
        "tools": tools,
        "articles": [],
        "total_cost_usd": 0.0,
    }

    for article in articles:
        aid = article_id(article)
        raw_dir = raw_root / aid
        result = run_openai_runner(args.python, runner, article, raw_dir, tools, args.concurrent, args.dry_run)
        (raw_dir / "runner.stdout.txt").write_text(result.stdout, encoding="utf-8", errors="replace")
        (raw_dir / "runner.stderr.txt").write_text(result.stderr, encoding="utf-8", errors="replace")

        if result.returncode != 0:
            manifest["articles"].append(
                {
                    "article_id": aid,
                    "status": "ERROR",
                    "notes": f"runner returned {result.returncode}",
                }
            )
            continue

        if args.dry_run:
            manifest["articles"].append({"article_id": aid, "status": "DRY_RUN", "notes": "No API calls made."})
            continue

        summary_path = raw_dir / f"{aid}_SUMMARY.json"
        run_summary = load_json_if_exists(summary_path)
        if run_summary:
            manifest["total_cost_usd"] += float(run_summary.get("total_cost_usd") or 0.0)
        packet_summary = normalize_article(raw_dir, packet_root, article)
        packet_summary["status"] = "OK"
        packet_summary["notes"] = "Packet generated; human review required."
        manifest["articles"].append(packet_summary)

    (run_dir / "run_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    write_run_report(run_dir, manifest)
    print(f"Wrote run: {run_dir}")
    print(f"Report: {run_dir / 'RUN_REPORT.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
