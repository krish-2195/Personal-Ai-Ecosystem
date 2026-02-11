from __future__ import annotations

from typing import Any, Dict

from backend.agents.base import AgentResult, BaseAgent


class FinanceAgent(BaseAgent):
    name = "finance"
    description = "Tracks expenses and budgets."
    handles = ["finance", "expense", "budget"]

    def run(self, payload: Dict[str, Any]) -> AgentResult:
        amount = payload.get("amount", 0)
        return AgentResult(
            agent=self.name,
            status="ok",
            summary=f"Expense captured: {amount}",
            data={"amount": amount},
        )
