from __future__ import annotations

from fastapi import APIRouter

from backend.audit.store import cleanup_events
from backend.profiles.store import get_profile


router = APIRouter(prefix="/v1/maintenance", tags=["maintenance"])


@router.post("/cleanup")
def cleanup() -> dict:
    profile = get_profile()
    removed = cleanup_events(profile.data_retention_days)
    return {
        "retention_days": profile.data_retention_days,
        "audit_events_removed": removed,
    }
