from __future__ import annotations

import json
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from disk_packet_loader import DEFAULT_SITE_DATA_DIR, load_article_fixture


OUTPUT_ROOT = DEFAULT_SITE_DATA_DIR / "APIs" / "packet-bundles"
SUMMARY_ROOT = DEFAULT_SITE_DATA_DIR / "_summaries" / "by-source"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def find_summary_articles(summary_root: Path) -> list[tuple[str, str, Path]]:
    rows: list[tuple[str, str, Path]] = []
    for series_dir in sorted(summary_root.iterdir()):
        if not series_dir.is_dir():
            continue
        root_dir = series_dir / "root"
        if not root_dir.exists():
            continue
        for summary_path in sorted(root_dir.glob("*.summary.json")):
            article_slug = summary_path.name.removesuffix(".summary.json")
            rows.append((series_dir.name, article_slug, summary_path))
    return rows


def write_bundle(series_slug: str, article_slug: str, data: dict[str, Any], output_root: Path) -> str:
    series_dir = output_root / series_slug
    series_dir.mkdir(parents=True, exist_ok=True)
    out_path = series_dir / f"{article_slug}.bundle.json"
    out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return str(out_path)


def run_all(summary_root: Path = SUMMARY_ROOT, output_root: Path = OUTPUT_ROOT) -> dict[str, Any]:
    articles = find_summary_articles(summary_root)
    results: list[dict[str, Any]] = []
    success_count = 0
    failure_count = 0

    output_root.mkdir(parents=True, exist_ok=True)

    for series_slug, article_slug, summary_path in articles:
        try:
            data = load_article_fixture(series_slug, article_slug)
            out_path = write_bundle(series_slug, article_slug, data, output_root)
            bridge = data["bundle"]["bridge_packet"]
            integrity = data["bundle"]["integrity_packet"]
            results.append(
                {
                    "series_slug": series_slug,
                    "article_slug": article_slug,
                    "status": "ok",
                    "summary_path": str(summary_path),
                    "output_path": out_path,
                    "title": bridge.get("title"),
                    "primary_domain": bridge.get("classification", {}).get("primary_domain"),
                    "equation_count": len(bridge.get("formal_surfaces", {}).get("equation_refs", [])),
                    "claim_count": len(bridge.get("claims", [])),
                    "audio_count": len(bridge.get("media", {}).get("audio", [])),
                    "publish_recommendation": integrity.get("structural_verdict", {}).get("publish_recommendation"),
                }
            )
            success_count += 1
        except Exception as exc:
            results.append(
                {
                    "series_slug": series_slug,
                    "article_slug": article_slug,
                    "status": "error",
                    "summary_path": str(summary_path),
                    "error": str(exc),
                    "traceback": traceback.format_exc(),
                }
            )
            failure_count += 1

    report = {
        "generated_at": utc_now_iso(),
        "summary_root": str(summary_root),
        "output_root": str(output_root),
        "article_count": len(articles),
        "success_count": success_count,
        "failure_count": failure_count,
        "results": results,
    }
    report_path = output_root / "_run-report.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report


if __name__ == "__main__":
    watch = "--watch" in sys.argv
    interval = 60
    if "--interval" in sys.argv:
        idx = sys.argv.index("--interval")
        if idx + 1 < len(sys.argv):
            interval = int(sys.argv[idx + 1])

    def print_summary(report: dict[str, Any]) -> None:
        print(json.dumps(
            {
                "generated_at": report["generated_at"],
                "article_count": report["article_count"],
                "success_count": report["success_count"],
                "failure_count": report["failure_count"],
                "output_root": report["output_root"],
            },
            indent=2,
            ensure_ascii=False,
        ))

    if not watch:
        print_summary(run_all())
    else:
        try:
            while True:
                print_summary(run_all())
                time.sleep(interval)
        except KeyboardInterrupt:
            print("watch stopped")
