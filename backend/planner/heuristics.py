from __future__ import annotations

from typing import List


def split_goal_to_tasks(goal: str) -> List[str]:
    clean = goal.strip()
    if not clean:
        return []

    if "," in clean:
        parts = [part.strip() for part in clean.split(",") if part.strip()]
        return parts[:5]

    words = clean.split()
    if len(words) > 12:
        return ["Outline the goal", "List requirements", "Draft first version"]

    return [clean]
