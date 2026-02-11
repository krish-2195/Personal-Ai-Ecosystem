from __future__ import annotations

from fastapi import APIRouter

from backend.audit.store import list_events
from backend.conversations.store import list_conversations
from backend.tasks.store import list_tasks


router = APIRouter(prefix="/v1/analytics", tags=["analytics"])


@router.get("/summary")
def summary() -> dict:
    tasks = list_tasks()
    conversations = list_conversations()
    audit_events = list_events(limit=200)

    total_messages = sum(len(conv.messages) for conv in conversations)
    return {
        "tasks_total": len(tasks),
        "conversations_total": len(conversations),
        "messages_total": total_messages,
        "audit_events_sample": len(audit_events),
    }
