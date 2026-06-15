def bars(value: int, width: int = 20) -> str:
    value = max(0, value)
    filled = min(width, value)
    return "#" * filled + "." * (width - filled)
