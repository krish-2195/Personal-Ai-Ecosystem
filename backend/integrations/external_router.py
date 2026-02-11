from __future__ import annotations

from fastapi import APIRouter

from backend.integrations.nylas_stub import check_nylas
from backend.integrations.plaid_stub import check_plaid


router = APIRouter(prefix="/v1/integrations", tags=["integrations"])


@router.get("/nylas")
def nylas_status() -> dict:
    status = check_nylas()
    return {
        "ok": status.ok,
        "configured": status.configured,
        "message": status.message,
    }


@router.get("/plaid")
def plaid_status() -> dict:
    status = check_plaid()
    return {
        "ok": status.ok,
        "configured": status.configured,
        "message": status.message,
    }
