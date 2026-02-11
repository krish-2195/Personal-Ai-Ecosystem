from __future__ import annotations

from typing import Any, Dict

from backend.agents.base import AgentResult, BaseAgent


class HealthAgent(BaseAgent):
    name = "health"
    description = "Tracks health logs and reminders."
    handles = ["health", "fitness", "sleep"]

    def run(self, payload: Dict[str, Any]) -> AgentResult:
        metric = payload.get("metric", "steps")
        return AgentResult(
            agent=self.name,
            status="ok",
            summary=f"Health log noted: {metric}",
            data={"metric": metric},
        )
