import argparse
import json
from datetime import datetime
from pathlib import Path


def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument("--in", dest="input_path", required=True)
    p.add_argument("--out", dest="output_path", required=True)
    a=p.parse_args()
    inp=Path(a.input_path)
    out=Path(a.output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    station_dir=Path(__file__).resolve().parent.parent
    (station_dir/"logs").mkdir(parents=True, exist_ok=True)
    payload={"status":"todo","station":station_dir.name,"note":"Runner stub only (no execution yet).","input":str(inp),"generated":datetime.now().isoformat(timespec="seconds")}
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    out.with_suffix(".md").write_text("# Result (stub)\n\n- status: todo\n", encoding="utf-8")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
