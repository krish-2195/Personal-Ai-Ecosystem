from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List
from uuid import uuid4

from pymongo.errors import PyMongoError

from backend.db.mongo import get_mongo_client


@dataclass
class AuditEvent:
    id: str
    event_type: str
    message: str
    timestamp: str
    meta: Dict[str, object]


_CACHE: Dict[str, AuditEvent] = {}


def _get_collection():
    try:
        client = get_mongo_client()
        db = client.get_default_database()
        return db["audit_events"]
    except Exception:
        return None


def log_event(event_type: str, message: str, meta: Dict[str, object]) -> AuditEvent:
    event = AuditEvent(
        id=str(uuid4()),
        event_type=event_type,
        message=message,
        timestamp=datetime.utcnow().isoformat() + "Z",
        meta=meta,
    )

    collection = _get_collection()
    if collection is not None:
        try:
            collection.insert_one(event.__dict__)
            return event
        except PyMongoError:
            pass

    _CACHE[event.id] = event
    return event


def list_events(limit: int = 50) -> List[AuditEvent]:
    collection = _get_collection()
    if collection is not None:
        try:
            docs = (
                collection.find({}, {"_id": 0})
                .sort("timestamp", -1)
                .limit(limit)
            )
            return [AuditEvent(**doc) for doc in docs]
        except PyMongoError:
            pass

    events = list(_CACHE.values())
    events.sort(key=lambda event: event.timestamp, reverse=True)
    return events[:limit]


def cleanup_events(retention_days: int) -> int:
    cutoff = datetime.utcnow() - timedelta(days=retention_days)
    cutoff_iso = cutoff.isoformat() + "Z"

    collection = _get_collection()
    if collection is not None:
        try:
            result = collection.delete_many({"timestamp": {"$lt": cutoff_iso}})
            return int(result.deleted_count)
        except PyMongoError:
            pass

    removed = 0
    for event_id, event in list(_CACHE.items()):
        if event.timestamp < cutoff_iso:
            _CACHE.pop(event_id, None)
            removed += 1
    return removed
