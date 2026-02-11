from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from backend.audit.store import log_event
from backend.tasks.store import TaskItem, advanced_filter, create_task, delete_task, list_tasks, update_status


router = APIRouter(prefix="/v1/tasks", tags=["tasks"])


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1)
    details: str = Field(default="")
    priority: str = Field(default="medium", pattern="^(low|medium|high)$")


class TaskUpdate(BaseModel):
    status: str = Field(..., pattern="^(pending|in_progress|done)$")


class TaskResponse(BaseModel):
    id: str
    title: str
    details: str
    priority: str
    status: str
    created_at: str
    updated_at: str


class TaskDeleteResponse(BaseModel):
    task_id: str
    deleted: bool


@router.get("/list", response_model=List[TaskResponse])
def get_tasks() -> List[TaskResponse]:
    return [TaskResponse(**task.__dict__) for task in list_tasks()]


@router.get("/search", response_model=List[TaskResponse])
def search_tasks(query: str) -> List[TaskResponse]:
    lowered = query.lower()
    matches = [
        task
        for task in list_tasks()
        if lowered in task.title.lower() or lowered in task.details.lower()
    ]
    return [TaskResponse(**task.__dict__) for task in matches]


@router.get("/filter", response_model=List[TaskResponse])
def filter_tasks(
    priority: List[str] = Query(None),
    status: List[str] = Query(None),
    date_from: str | None = None,
    date_to: str | None = None,
    title_query: str | None = None,
) -> List[TaskResponse]:
    """Advanced filter: priority, status, date range (ISO format), title search."""
    tasks = advanced_filter(
        priorities=priority if priority else None,
        statuses=status if status else None,
        date_from=date_from,
        date_to=date_to,
        title_query=title_query,
    )
    return [TaskResponse(**task.__dict__) for task in tasks]


@router.get("/stats")
def task_stats() -> dict:
    tasks = list_tasks()
    status_counts = {"pending": 0, "in_progress": 0, "done": 0}
    priority_counts = {"low": 0, "medium": 0, "high": 0}
    for task in tasks:
        if task.status in status_counts:
            status_counts[task.status] += 1
        if task.priority in priority_counts:
            priority_counts[task.priority] += 1

    return {
        "total": len(tasks),
        "by_status": status_counts,
        "by_priority": priority_counts,
    }


@router.post("/create", response_model=TaskResponse)
def create(request: TaskCreate) -> TaskResponse:
    task = create_task(request.title, request.details, request.priority)
    log_event(
        "task.create",
        f"Task created: {task.title}",
        {"task_id": task.id, "priority": task.priority},
    )
    return TaskResponse(**task.__dict__)


@router.patch("/{task_id}/status", response_model=TaskResponse)
def set_status(task_id: str, request: TaskUpdate) -> TaskResponse:
    task = update_status(task_id, request.status)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    log_event(
        "task.status",
        f"Task status updated: {task.title}",
        {"task_id": task.id, "status": task.status},
    )
    return TaskResponse(**task.__dict__)


@router.delete("/{task_id}", response_model=TaskDeleteResponse)
def remove_task(task_id: str) -> TaskDeleteResponse:
    deleted = delete_task(task_id)
    if deleted:
        log_event(
            "task.delete",
            "Task deleted",
            {"task_id": task_id},
        )
    return TaskDeleteResponse(task_id=task_id, deleted=deleted)
