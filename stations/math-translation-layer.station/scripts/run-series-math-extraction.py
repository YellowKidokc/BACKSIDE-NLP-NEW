from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


def load_extractor(script_path: Path):
    spec = importlib.util.spec_from_file_location("extract_figures_math", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load extractor: {script_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_dictionary(paths: list[Path]) -> dict:
    merged = {"schema": "theophysics.math_dictionary_merged.v1", "equations": []}
    seen_ids: set[str] = set()
    for path in paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        for entry in data.get("equations", []):
            equation_id = str(entry.get("equationId") or "")
            if equation_id and equation_id in seen_ids:
                continue
            if equation_id:
                seen_ids.add(equation_id)
            merged["equations"].append(entry)
    merged["generated_at"] = datetime.now(timezone.utc).isoformat()
    merged["sources"] = [str(path) for path in paths]
    return merged


def article_id(path: Path) -> str:
    return path.stem.replace(" ", "-")


def render_index(results: list[dict]) -> str:
    rows = []
    for result in results:
        rel_appendix = result.get("relativeAppendix", "")
        matched = result.get("matchedEquationCount", 0)
        unmatched = result.get("unmatchedEquationCount", 0)
        total = result.get("equationCount", 0)
        rows.append(
            f"<tr><td>{result['articleId']}</td><td>{result['title']}</td>"
            f"<td>{total}</td><td>{matched}</td><td>{unmatched}</td>"
            f"<td><a href=\"{rel_appendix}\">open appendix</a></td></tr>"
        )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>MDA Series Math Extraction Index</title>
  <style>
    body {{ background: #090a0f; color: #d7d9df; font-family: Segoe UI, Inter, sans-serif; margin: 0; padding: 28px; }}
    main {{ max-width: 1180px; margin: 0 auto; }}
    h1 {{ color: #f4f0e8; }}
    table {{ border-collapse: collapse; width: 100%; font-size: 14px; }}
    th, td {{ border-bottom: 1px solid rgba(255,255,255,.12); padding: 9px 10px; text-align: left; vertical-align: top; }}
    th {{ color: #f4f0e8; background: rgba(255,255,255,.06); position: sticky; top: 0; }}
    a {{ color: #e8a912; }}
  </style>
</head>
<body>
<main>
  <h1>MDA Series Math Extraction Index</h1>
  <p>Generated: {datetime.now(timezone.utc).isoformat()}</p>
  <table>
    <thead><tr><th>Article</th><th>Title</th><th>Equations</th><th>Matched</th><th>Unmatched</th><th>Appendix</th></tr></thead>
    <tbody>{''.join(rows)}</tbody>
  </table>
</main>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Run math extraction across a whole HTML series.")
    parser.add_argument("--scan", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--dictionary", type=Path, action="append", required=True)
    parser.add_argument("--extractor", type=Path, default=Path(__file__).with_name("extract-figures-math.py"))
    args = parser.parse_args()

    extractor = load_extractor(args.extractor.resolve())
    dictionary = load_dictionary([path.resolve() for path in args.dictionary])
    output_dir = args.output_dir.resolve()
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    inputs = sorted(path for path in args.scan.resolve().glob("*.html") if path.is_file())
    results: list[dict] = []
    all_equations: list[dict] = []
    for html_path in inputs:
        aid = article_id(html_path)
        article_out = output_dir / aid
        result = extractor.process_file(html_path, article_out, dictionary)
        catalog_path = Path(result["outputs"][1])
        appendix_path = Path(result["outputs"][2])
        equations = json.loads(catalog_path.read_text(encoding="utf-8"))
        for eq in equations:
            all_equations.append({"articleId": aid, "articleTitle": result["title"], **eq})
        result["articleId"] = aid
        result["matchedEquationCount"] = sum(1 for eq in equations if eq.get("matched"))
        result["unmatchedEquationCount"] = sum(1 for eq in equations if not eq.get("matched"))
        result["relativeAppendix"] = str(appendix_path.relative_to(output_dir)).replace("\\", "/")
        results.append(result)

    unmatched_unique: dict[str, dict] = {}
    for eq in all_equations:
        if not eq.get("matched"):
            unmatched_unique.setdefault(eq.get("rawLatex", ""), eq)

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scan": str(args.scan.resolve()),
        "output_dir": str(output_dir),
        "dictionary_sources": [str(path.resolve()) for path in args.dictionary],
        "article_count": len(results),
        "equation_count": len(all_equations),
        "matched_equation_count": sum(1 for eq in all_equations if eq.get("matched")),
        "unmatched_equation_count": sum(1 for eq in all_equations if not eq.get("matched")),
        "unique_unmatched_equation_count": len(unmatched_unique),
        "documents": results,
    }
    (output_dir / "SERIES_MATH_EXTRACTION_MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (output_dir / "ALL_EQUATIONS.json").write_text(
        json.dumps(all_equations, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (output_dir / "UNMATCHED_EQUATIONS_TO_PROGRAM.json").write_text(
        json.dumps(list(unmatched_unique.values()), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (output_dir / "OPEN_ME_SERIES_MATH_INDEX.html").write_text(render_index(results), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
