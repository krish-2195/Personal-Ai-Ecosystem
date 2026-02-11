from __future__ import annotations

from typing import Iterable

from fastapi import Request
from starlette.responses import JSONResponse

from backend.config import get_settings


_WRITE_METHODS: Iterable[str] = {"POST", "PUT", "PATCH", "DELETE"}


def is_protected(request: Request) -> bool:
    settings = get_settings()
    if not settings.api_key and not settings.admin_api_key:
        return False

    path = request.url.path
    if path.startswith("/docs") or path.startswith("/openapi"):
        return False

    if path.startswith("/v1/export"):
        return True

    if settings.admin_api_key and path.startswith("/v1/admin"):
        return True

    return request.method.upper() in _WRITE_METHODS


def api_key_guard(request: Request) -> JSONResponse | None:
    if not is_protected(request):
        return None

    settings = get_settings()
    provided = request.headers.get("x-api-key", "")
    if request.url.path.startswith("/v1/admin"):
        if not settings.admin_api_key:
            return JSONResponse(
                status_code=401,
                content={"detail": "Admin API key not configured"},
            )
        if not provided or provided != settings.admin_api_key:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid or missing admin API key"},
            )
        return None

    if not settings.api_key:
        return None

    if not provided or provided != settings.api_key:
        return JSONResponse(
            status_code=401,
            content={"detail": "Invalid or missing API key"},
        )

    return None
