from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import requests

from backend.config import get_settings


@dataclass
class CompressionResult:
    ok: bool
    ratio: float
    original_size: int
    compressed_size: int
    summary: str


def compress_text(text: str) -> CompressionResult:
    settings = get_settings()
    if not settings.scaledown_api_key:
        original_size = len(text.encode("utf-8"))
        compressed_size = max(1, int(original_size * 0.15))
        return CompressionResult(
            ok=True,
            ratio=0.85,
            original_size=original_size,
            compressed_size=compressed_size,
            summary="Simulated compression (no API key)",
        )

    url = "https://api.scaledown.ai/v1/compress"
    headers = {"Authorization": f"Bearer {settings.scaledown_api_key}"}
    payload: Dict[str, str] = {"text": text}

    response = requests.post(url, json=payload, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()

    return CompressionResult(
        ok=True,
        ratio=float(data.get("ratio", 0.0)),
        original_size=int(data.get("original_size", 0)),
        compressed_size=int(data.get("compressed_size", 0)),
        summary="ScaleDown compression",
    )
