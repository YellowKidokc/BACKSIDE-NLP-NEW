from __future__ import annotations

from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class ConversionConfig(BaseModel):
    export_root: Path = Path(r"X:\EXPORTS\conversion-layer")
    state_root: Path = Path(r"X:\Backside\_state\conversion-layer")
    markitdown_enabled: bool = True
    youtube_prefer_transcript: bool = True
    metadata: dict[str, Any] = Field(default_factory=dict)


class ConvertResult(BaseModel):
    markdown: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)

