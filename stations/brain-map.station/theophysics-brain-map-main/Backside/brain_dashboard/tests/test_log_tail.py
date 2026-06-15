from pathlib import Path

from brain_dashboard.data.log_tail import tail_lines


def test_tail_lines(tmp_path: Path):
    path = tmp_path / "a.log"
    path.write_text("\n".join([f"line{i}" for i in range(10)]), encoding="utf-8")
    out = tail_lines(path, 3)
    assert out == ["line7", "line8", "line9"]
