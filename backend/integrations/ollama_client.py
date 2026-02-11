from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

import requests

from backend.config import get_settings


@dataclass
class OllamaMessage:
    role: str
    content: str


@dataclass
class OllamaResponse:
    ok: bool
    model: str
    message: str


@dataclass
class OllamaPing:
    ok: bool
    models: int
    message: str


def chat_ollama(messages: List[OllamaMessage]) -> OllamaResponse:
    settings = get_settings()
    url = f"{settings.ollama_base_url.rstrip('/')}/api/chat"

    payload: Dict[str, object] = {
        "model": settings.ollama_model,
        "messages": [
            {"role": msg.role, "content": msg.content} for msg in messages
        ],
        "stream": False,
    }

    response = requests.post(url, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    return OllamaResponse(
        ok=True,
        model=settings.ollama_model,
        message=data.get("message", {}).get("content", ""),
    )


def ping_ollama() -> OllamaPing:
    settings = get_settings()
    url = f"{settings.ollama_base_url.rstrip('/')}/api/tags"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        models = len(data.get("models", []))
        return OllamaPing(ok=True, models=models, message="Ollama reachable")
    except requests.RequestException as exc:
        return OllamaPing(ok=False, models=0, message=str(exc))
