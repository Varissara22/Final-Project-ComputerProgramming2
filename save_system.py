import json
import os
from typing import Optional

SAVE_PATH = "soul_steep_save.json"

def has_save() -> bool:
    return os.path.isfile(SAVE_PATH)

def save_game(current_day: int, ghosts_served_today: int) -> None:
    data = {
        "current_day":         current_day,
        "ghosts_served_today": ghosts_served_today,
    }
    with open(SAVE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def load_game() -> Optional[dict]:
    if not has_save():
        return None
    try:
        with open(SAVE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, KeyError):
        delete_save()
        return None

def delete_save() -> None:
    if os.path.isfile(SAVE_PATH):
        os.remove(SAVE_PATH)