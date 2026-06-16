import argparse
import json
from datetime import datetime
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="input_path", required=True)
    parser.add_argument("--out", dest="output_path", required=True)
    args = parser.parse_args()

    input_path = Path(args.input_path)
    output_path = Path(args.output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    station_dir = Path(__file__).resolve().parent.parent
    logs_dir = station_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    payload = {
        "status": "todo",
        "station": "18_knowledge_graph_extractor",
        "note": "Runner stub only (graph extraction wiring pending).",
        "input": str(input_path),
        "generated": datetime.now().isoformat(timespec="seconds"),
    }
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    output_path.with_suffix(".md").write_text("# Result (stub)\n\n- status: todo\n", encoding="utf-8")
    (logs_dir / f"run_{datetime.now().strftime('%Y%m%d-%H%M%S')}.log").write_text(
        f"stub run wrote {output_path}\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

