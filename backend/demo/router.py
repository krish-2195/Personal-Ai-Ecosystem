from __future__ import annotations

from fastapi import APIRouter

from backend.conversations.store import append_message, create_conversation
from backend.tasks.store import create_task


router = APIRouter(prefix="/v1/demo", tags=["demo"])


@router.post("/seed")
def seed_demo() -> dict:
    tasks = [
        create_task("Prepare demo slides", "Deck for class demo", "high"),
        create_task("Test voice pipeline", "Run TTS and STT", "medium"),
        create_task("Clean data cache", "Remove old logs", "low"),
    ]

    conversation = create_conversation("Demo conversation")
    append_message(conversation.id, "user", "Hey, summarize my tasks.")
    append_message(
        conversation.id,
        "assistant",
        "Sure! You have 3 tasks: slides, voice tests, and cache cleanup.",
    )

    return {
        "tasks_created": len(tasks),
        "task_ids": [task.id for task in tasks],
        "conversation_id": conversation.id,
        "messages_added": 2,
    }
