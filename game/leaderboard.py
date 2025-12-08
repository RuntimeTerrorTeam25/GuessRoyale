# game/leaderboard.py

import json
import os
from typing import List, Dict

from config import LEADERBOARD_FILE


def load_leaderboard() -> List[Dict]:
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    try:
        with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
    except Exception:
        pass
    return []


def save_leaderboard(entries: List[Dict]) -> None:
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)


def add_score(game_state) -> None:
    entries = load_leaderboard()
    entry = {
        "player": game_state.player_name,
        "mode": game_state.mode,
        "difficulty": game_state.difficulty_name,
        "score": game_state.score,
    }
    entries.append(entry)
    entries.sort(key=lambda e: e["score"], reverse=True)
    save_leaderboard(entries)


def show_leaderboard() -> None:
    entries = load_leaderboard()
    if not entries:
        print("\nNo scores saved yet.")
        return

    print("\n=== LEADERBOARD ===")
    print(f"{'Rank':<6}{'Player':<15}{'Mode':<10}{'Diff':<10}{'Score':<6}")
    print("-" * 50)

    for idx, entry in enumerate(entries[:10], start=1):
        print(
            f"{idx:<6}"
            f"{entry['player']:<15}"
            f"{entry['mode']:<10}"
            f"{entry['difficulty']:<10}"
            f"{entry['score']:<6}"
        )
    print()
