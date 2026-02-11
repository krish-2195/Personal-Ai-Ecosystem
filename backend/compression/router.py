from __future__ import annotations

from fastapi import APIRouter

from backend.conversations.store import list_conversations
from backend.utils.scaledown import compress_text


router = APIRouter(prefix="/v1/compression", tags=["compression"])


@router.post("/conversations")
def compress_conversations() -> dict:
	conversations = list_conversations()
	raw_text = "\n".join(
		f"{conv.title}: {len(conv.messages)} messages" for conv in conversations
	)
	result = compress_text(raw_text or "(no conversations)")

	return {
		"ok": result.ok,
		"ratio": result.ratio,
		"original_size": result.original_size,
		"compressed_size": result.compressed_size,
		"summary": result.summary,
		"input_preview": raw_text[:200],
	}
