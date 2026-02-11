from __future__ import annotations

from fastapi import APIRouter

from backend.conversations.store import list_conversations
from backend.profiles.store import get_profile
from backend.tasks.store import list_tasks


router = APIRouter(prefix="/v1/export", tags=["export"])


@router.get("/all")
def export_all() -> dict:
	profile = get_profile()
	tasks = list_tasks()
	conversations = list_conversations()

	return {
		"profile": profile.__dict__,
		"tasks": [task.__dict__ for task in tasks],
		"conversations": [
			{
				"id": conv.id,
				"title": conv.title,
				"messages": [msg.__dict__ for msg in conv.messages],
			}
			for conv in conversations
		],
	}
