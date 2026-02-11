from __future__ import annotations

from typing import Any, Dict

from backend.agents.base import AgentResult, BaseAgent


class ScheduleAgent(BaseAgent):
    name = "schedule"
    description = "Handles calendar scheduling tasks."
    handles = ["schedule", "calendar", "meeting"]

    def run(self, payload: Dict[str, Any]) -> AgentResult:
        title = payload.get("title", "Untitled")
        return AgentResult(
            agent=self.name,
            status="ok",
            summary=f"Scheduled: {title}",
            data={"event": title},
        )
