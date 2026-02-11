from __future__ import annotations

from dataclasses import dataclass

from backend.config import get_settings


@dataclass
class PlaidStatus:
    ok: bool
    configured: bool
    message: str


def check_plaid() -> PlaidStatus:
    settings = get_settings()
    configured = bool(settings.plaid_client_id and settings.plaid_secret)
    if not configured:
        return PlaidStatus(
            ok=False,
            configured=False,
            message="Plaid credentials not set",
        )

    return PlaidStatus(ok=True, configured=True, message="Plaid configured")
