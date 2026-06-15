from pathlib import Path

from theophysics_conversion.convert import convert
from theophysics_conversion.detect import Format


def test_convert_markdown_passthrough(tmp_path: Path) -> None:
    source = tmp_path / "note.md"
    source.write_text("# Title\r\n\r\nBody text.\r\n", encoding="utf-8")

    result = convert(source)

    assert result.markdown == "# Title\n\nBody text.\n"
    assert result.metadata["detected_format"] == Format.MARKDOWN.value


def test_convert_unknown_file_warns(tmp_path: Path) -> None:
    source = tmp_path / "unknown.bin"
    source.write_bytes(b"\x00\x01\x02\x03")

    result = convert(source)

    assert result.markdown == ""
    assert result.warnings
    assert "UNKNOWN" in result.warnings[0]
