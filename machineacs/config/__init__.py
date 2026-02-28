import json
from pathlib import Path
from typing import Dict, Any

_settings_path = Path(__file__).parent / "settings.json"


def load_settings() -> Dict[str, Any]:
    """
    Load settings from settings.json.

    Returns:
        Dict containing the parsed settings.

    Raises:
        FileNotFoundError: If settings.json doesn't exist.
        json.JSONDecodeError: If settings.json contains invalid JSON.
    """
    with open(_settings_path, "r", encoding="utf-8") as f:
        return json.load(f)


settings = load_settings()
