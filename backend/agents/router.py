from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.agents.base import AgentResult, BaseAgent
from backend.agents.email_agent import EmailAgent
from backend.agents.finance_agent import FinanceAgent
from backend.agents.health_agent import HealthAgent
from backend.agents.schedule_agent import ScheduleAgent
from backend.integrations.ollama_client import OllamaMessage, chat_ollama


class AgentRequest(BaseModel):
    task_type: str = Field(..., description="High-level task category")
    payload: Dict[str, Any] = Field(default_factory=dict)


class AgentResponse(BaseModel):
    agent: str
    status: str
    summary: str
    data: Dict[str, Any]


class AutoRouteRequest(BaseModel):
    query: str = Field(..., min_length=3)
    payload: Dict[str, Any] = Field(default_factory=dict)
    prefer_llm: bool = True


class AutoRouteResponse(BaseModel):
    agent: str
    status: str
    summary: str
    data: Dict[str, Any]
    decision_source: str


router = APIRouter(prefix="/v1/agents", tags=["agents"])


AGENTS: List[BaseAgent] = [
    ScheduleAgent(),
    EmailAgent(),
    HealthAgent(),
    FinanceAgent(),
]


@router.get("/list")
def list_agents() -> List[Dict[str, Any]]:
    return [
        {
            "name": agent.name,
            "description": agent.description,
            "handles": agent.handles,
        }
        for agent in AGENTS
    ]


@router.post("/route", response_model=AgentResponse)
def route_agent(request: AgentRequest) -> AgentResponse:
    task_type = request.task_type.lower()
    for agent in AGENTS:
        if task_type in agent.handles:
            result: AgentResult = agent.run(request.payload)
            return AgentResponse(**result.__dict__)

    return AgentResponse(
        agent="router",
        status="no_match",
        summary=f"No agent found for task_type='{task_type}'",
        data={},
    )


def _heuristic_pick(query: str) -> BaseAgent | None:
    lowered = query.lower()
    for agent in AGENTS:
        if any(handle in lowered for handle in agent.handles):
            return agent
    return None


@router.post("/auto", response_model=AutoRouteResponse)
def auto_route(request: AutoRouteRequest) -> AutoRouteResponse:
    decision_source = "heuristic"
    picked: BaseAgent | None = None

    if request.prefer_llm:
        try:
            agent_names = ", ".join(agent.name for agent in AGENTS)
            system_text = (
                "You route user tasks to the correct agent. "
                "Only reply with one agent name from: "
                f"{agent_names}."
            )
            result = chat_ollama(
                [
                    OllamaMessage(role="system", content=system_text),
                    OllamaMessage(role="user", content=request.query),
                ]
            )
            reply = result.message.strip().lower()
            for agent in AGENTS:
                if reply == agent.name:
                    picked = agent
                    decision_source = "llm"
                    break
        except Exception:
            picked = None

    if not picked:
        picked = _heuristic_pick(request.query)
        decision_source = "heuristic"

    if picked:
        result: AgentResult = picked.run(request.payload)
        return AutoRouteResponse(
            agent=result.agent,
            status=result.status,
            summary=result.summary,
            data=result.data,
            decision_source=decision_source,
        )

    return AutoRouteResponse(
        agent="router",
        status="no_match",
        summary="No agent found for query",
        data={},
        decision_source="none",
    )
