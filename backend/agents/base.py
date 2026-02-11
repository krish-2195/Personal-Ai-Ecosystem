from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class AgentResult:
    agent: str
    status: str
    summary: str
    data: Dict[str, Any]


class BaseAgent:
    name: str = "base"
    description: str = ""
    handles: List[str] = []

    def run(self, payload: Dict[str, Any]) -> AgentResult:
        raise NotImplementedError()
