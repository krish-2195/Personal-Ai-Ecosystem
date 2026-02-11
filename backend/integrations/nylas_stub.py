from __future__ import annotations

from dataclasses import dataclass

from backend.config import get_settings


@dataclass
class NylasStatus:
    ok: bool
    configured: bool
    message: str


def check_nylas() -> NylasStatus:
    settings = get_settings()
    configured = bool(settings.nylas_client_id and settings.nylas_client_secret)
    if not configured:
        return NylasStatus(
            ok=False,
            configured=False,
            message="Nylas credentials not set",
        )

    return NylasStatus(ok=True, configured=True, message="Nylas configured")
