from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List
from uuid import uuid4

from pymongo import ReturnDocument
from pymongo.errors import PyMongoError

from backend.db.mongo import get_mongo_client


@dataclass
class TaskItem:
    id: str
    title: str
    details: str
    priority: str
    status: str
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


_TASKS: Dict[str, TaskItem] = {}


def _get_collection():
    try:
        client = get_mongo_client()
        db = client.get_default_database()
        return db["tasks"]
    except Exception:
        return None


def create_task(title: str, details: str, priority: str) -> TaskItem:
    task_id = str(uuid4())
    now = datetime.utcnow().isoformat()
    task = TaskItem(
        id=task_id,
        title=title,
        details=details,
        priority=priority,
        status="pending",
        created_at=now,
        updated_at=now,
    )
    collection = _get_collection()
    if collection is not None:
        try:
            collection.insert_one(task.__dict__)
            return task
        except PyMongoError:
            pass

    _TASKS[task_id] = task
    return task


def list_tasks() -> List[TaskItem]:
    collection = _get_collection()
    if collection is not None:
        try:
            docs = collection.find({}, {"_id": 0})
            return [TaskItem(**doc) for doc in docs]
        except PyMongoError:
            pass

    return list(_TASKS.values())


def update_status(task_id: str, status: str) -> TaskItem | None:
    collection = _get_collection()
    if collection is not None:
        try:
            result = collection.find_one_and_update(
                {"id": task_id},
                {"$set": {"status": status}},
                return_document=ReturnDocument.AFTER,
                projection={"_id": 0},
            )
            if result:
                return TaskItem(**result)
        except PyMongoError:
            pass

    task = _TASKS.get(task_id)
    if not task:
        return None
    task.status = status
    return task


def delete_task(task_id: str) -> bool:
    collection = _get_collection()
    if collection is not None:
        try:
            result = collection.delete_one({"id": task_id})
            if result.deleted_count:
                return True
        except PyMongoError:
            pass

    return _TASKS.pop(task_id, None) is not None


def advanced_filter(
    priorities: List[str] | None = None,
    statuses: List[str] | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
    title_query: str | None = None,
) -> List[TaskItem]:
    """Filter tasks by multiple criteria (priority, status, date range, title)."""
    tasks = list_tasks()
    results = tasks

    if title_query:
        lowered = title_query.lower()
        results = [
            t
            for t in results
            if lowered in t.title.lower() or lowered in t.details.lower()
        ]

    if priorities:
        results = [t for t in results if t.priority in priorities]

    if statuses:
        results = [t for t in results if t.status in statuses]

    if date_from or date_to:
        try:
            results_by_date = []
            for task in results:
                created = datetime.fromisoformat(task.created_at)
                if date_from and created < datetime.fromisoformat(date_from):
                    continue
                if date_to and created > datetime.fromisoformat(date_to):
                    continue
                results_by_date.append(task)
            results = results_by_date
        except (ValueError, AttributeError):
            pass

    return results
