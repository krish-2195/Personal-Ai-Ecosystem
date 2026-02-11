from __future__ import annotations

from typing import List

from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.integrations.ollama_client import OllamaMessage, chat_ollama, ping_ollama


router = APIRouter(prefix="/v1/llm", tags=["llm"])


class ChatMessage(BaseModel):
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str = Field(..., min_length=1)


class ChatRequest(BaseModel):
    messages: List[ChatMessage]


@router.post("/chat")
def chat(request: ChatRequest) -> dict:
    messages = [
        OllamaMessage(role=msg.role, content=msg.content)
        for msg in request.messages
    ]
    result = chat_ollama(messages)
    return {
        "ok": result.ok,
        "model": result.model,
        "message": result.message,
    }


@router.get("/ping")
def ping() -> dict:
    result = ping_ollama()
    return {
        "ok": result.ok,
        "models": result.models,
        "message": result.message,
    }
