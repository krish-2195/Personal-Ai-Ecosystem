from __future__ import annotations

from typing import List

from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.planner.heuristics import split_goal_to_tasks
from backend.tasks.store import create_task, list_tasks


router = APIRouter(prefix="/v1/plan", tags=["planning"])


class PlanRequest(BaseModel):
    goal: str = Field(..., min_length=3)
    priority: str = Field(default="medium", pattern="^(low|medium|high)$")


class PlanResponse(BaseModel):
    created_task_ids: List[str]
    titles: List[str]


class PlanWithExistingResponse(BaseModel):
    created_task_ids: List[str]
    titles: List[str]
    existing_tasks: List[str]


@router.post("/quick", response_model=PlanResponse)
def quick_plan(request: PlanRequest) -> PlanResponse:
    titles = split_goal_to_tasks(request.goal)
    created_ids: List[str] = []
    for title in titles:
        task = create_task(title=title, details="", priority=request.priority)
        created_ids.append(task.id)

    return PlanResponse(created_task_ids=created_ids, titles=titles)


@router.post("/quick_with_existing", response_model=PlanWithExistingResponse)
def quick_plan_with_existing(request: PlanRequest) -> PlanWithExistingResponse:
    titles = split_goal_to_tasks(request.goal)
    created_ids: List[str] = []
    for title in titles:
        task = create_task(title=title, details="", priority=request.priority)
        created_ids.append(task.id)

    existing = [task.title for task in list_tasks()]
    return PlanWithExistingResponse(
        created_task_ids=created_ids,
        titles=titles,
        existing_tasks=existing,
    )
