from __future__ import annotations

from typing import Any, Dict

from backend.agents.base import AgentResult, BaseAgent


class EmailAgent(BaseAgent):
    name = "email"
    description = "Drafts and sends email messages."
    handles = ["email", "mail", "inbox"]

    def run(self, payload: Dict[str, Any]) -> AgentResult:
        subject = payload.get("subject", "(no subject)")
        return AgentResult(
            agent=self.name,
            status="ok",
            summary=f"Email drafted: {subject}",
            data={"subject": subject},
        )
