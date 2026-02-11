from __future__ import annotations

from typing import List

from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.audit.store import AuditEvent, list_events, log_event


router = APIRouter(prefix="/v1/audit", tags=["audit"])


class AuditResponse(BaseModel):
    id: str
    event_type: str
    message: str
    timestamp: str
    meta: dict


class AuditCreate(BaseModel):
    event_type: str = Field(..., min_length=2)
    message: str = Field(..., min_length=1)
    meta: dict = Field(default_factory=dict)


@router.get("/list", response_model=List[AuditResponse])
def get_audit(limit: int = 50) -> List[AuditResponse]:
    events = list_events(limit=limit)
    return [AuditResponse(**event.__dict__) for event in events]


@router.post("/log", response_model=AuditResponse)
def create_audit(request: AuditCreate) -> AuditResponse:
    event = log_event(request.event_type, request.message, request.meta)
    return AuditResponse(**event.__dict__)
