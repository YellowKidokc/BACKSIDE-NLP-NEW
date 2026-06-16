import json
from pathlib import Path

from brain_dashboard.data.state_reader import nlp_cards, read_state


def test_read_state_missing(tmp_path: Path):
    data = read_state(tmp_path / "missing.json")
    assert "nlps" in data


def test_nlp_cards(tmp_path: Path):
    path = tmp_path / "state.json"
    path.write_text(json.dumps({"nlps": {"a": {"status": "healthy", "queue_depth": 2, "recent_runs": [{"exit_code": 0}]}}}))
    state = read_state(path)
    cards = nlp_cards(state)
    assert cards[0]["name"] == "a"
    assert cards[0]["trend"] == [0]
