from __future__ import annotations

from fastapi import APIRouter

from backend.config import get_settings
from backend.status.router import metrics
from backend.status.router import get_uptime_seconds


router = APIRouter(prefix="/v1/admin", tags=["admin"])


@router.get("/info")
def info() -> dict:
    settings = get_settings()
    uptime_seconds = get_uptime_seconds()
    return {
        "app": settings.app_name,
        "env": settings.app_env,
        "uptime_seconds": uptime_seconds,
        "ollama_model": settings.ollama_model,
        "cors_origins": settings.cors_origins,
        "api_key_configured": bool(settings.api_key),
        "admin_api_key_configured": bool(settings.admin_api_key),
    }
