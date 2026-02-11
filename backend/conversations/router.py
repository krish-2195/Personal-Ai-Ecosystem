from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.audit.store import log_event
from backend.conversations.store import (
    Conversation,
    ConversationMessage,
    append_message,
    create_conversation,
    get_conversation,
    list_conversations,
)
from backend.integrations.ollama_client import OllamaMessage, chat_ollama


router = APIRouter(prefix="/v1/conversations", tags=["conversations"])


class ConversationCreate(BaseModel):
    title: str = Field(..., min_length=1)


class MessageCreate(BaseModel):
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str = Field(..., min_length=1)


class MessageResponse(BaseModel):
    role: str
    content: str
    timestamp: str


class ConversationResponse(BaseModel):
    id: str
    title: str
    messages: List[MessageResponse]


class SummaryResponse(BaseModel):
    conversation_id: str
    summary: str
    method: str


@router.post("/create", response_model=ConversationResponse)
def create(request: ConversationCreate) -> ConversationResponse:
    conversation = create_conversation(request.title)
    log_event(
        "conversation.create",
        f"Conversation created: {conversation.title}",
        {"conversation_id": conversation.id},
    )
    return ConversationResponse(
        id=conversation.id,
        title=conversation.title,
        messages=[],
    )


@router.get("/list", response_model=List[ConversationResponse])
def list_all() -> List[ConversationResponse]:
    conversations = list_conversations()
    return [
        ConversationResponse(
            id=conv.id,
            title=conv.title,
            messages=[MessageResponse(**msg.__dict__) for msg in conv.messages],
        )
        for conv in conversations
    ]


@router.get("/search", response_model=List[ConversationResponse])
def search(query: str) -> List[ConversationResponse]:
    lowered = query.lower()
    matches = []
    for conv in list_conversations():
        if lowered in conv.title.lower():
            matches.append(conv)
            continue
        for msg in conv.messages:
            if lowered in msg.content.lower():
                matches.append(conv)
                break

    return [
        ConversationResponse(
            id=conv.id,
            title=conv.title,
            messages=[MessageResponse(**msg.__dict__) for msg in conv.messages],
        )
        for conv in matches
    ]


@router.get("/stats")
def stats() -> dict:
    conversations = list_conversations()
    total_messages = sum(len(conv.messages) for conv in conversations)
    avg_messages = 0
    if conversations:
        avg_messages = total_messages / len(conversations)

    return {
        "total_conversations": len(conversations),
        "total_messages": total_messages,
        "avg_messages_per_conversation": round(avg_messages, 2),
    }


@router.get("/{conv_id}", response_model=ConversationResponse)
def get_one(conv_id: str) -> ConversationResponse:
    conversation: Conversation | None = get_conversation(conv_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    return ConversationResponse(
        id=conversation.id,
        title=conversation.title,
        messages=[MessageResponse(**msg.__dict__) for msg in conversation.messages],
    )


@router.post("/{conv_id}/message", response_model=ConversationResponse)
def add_message(conv_id: str, request: MessageCreate) -> ConversationResponse:
    conversation = append_message(conv_id, request.role, request.content)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    log_event(
        "conversation.message",
        "Message added to conversation",
        {"conversation_id": conversation.id, "role": request.role},
    )

    return ConversationResponse(
        id=conversation.id,
        title=conversation.title,
        messages=[MessageResponse(**msg.__dict__) for msg in conversation.messages],
    )


def _heuristic_summary(messages: List[ConversationMessage]) -> str:
    if not messages:
        return "No messages yet."
    tail = messages[-4:]
    lines = [f"{msg.role}: {msg.content}" for msg in tail]
    return " | ".join(lines)


@router.get("/{conv_id}/summary", response_model=SummaryResponse)
def get_summary(conv_id: str, prefer_llm: bool = True) -> SummaryResponse:
    conversation: Conversation | None = get_conversation(conv_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    method = "heuristic"
    summary = _heuristic_summary(conversation.messages)

    if prefer_llm and conversation.messages:
        try:
            joined = "\n".join(
                f"{msg.role}: {msg.content}" for msg in conversation.messages[-12:]
            )
            result = chat_ollama(
                [
                    OllamaMessage(
                        role="system",
                        content=(
                            "Summarize this conversation in 2-3 short sentences."
                        ),
                    ),
                    OllamaMessage(role="user", content=joined),
                ]
            )
            if result.message:
                summary = result.message
                method = "llm"
        except Exception:
            method = "heuristic"

    return SummaryResponse(
        conversation_id=conversation.id,
        summary=summary,
        method=method,
    )
