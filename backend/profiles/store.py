from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from pymongo.errors import PyMongoError

from backend.db.mongo import get_mongo_client


@dataclass
class Profile:
    id: str
    display_name: str
    timezone: str
    privacy_mode: str
    data_retention_days: int
    local_only: bool


_DEFAULT = Profile(
    id="default",
    display_name="User",
    timezone="UTC",
    privacy_mode="strict",
    data_retention_days=365,
    local_only=True,
)

_PROFILE_CACHE: Dict[str, Profile] = {"default": _DEFAULT}


def _get_collection():
    try:
        client = get_mongo_client()
        db = client.get_default_database()
        return db["profiles"]
    except Exception:
        return None


def get_profile() -> Profile:
    collection = _get_collection()
    if collection is not None:
        try:
            doc = collection.find_one({"id": "default"}, {"_id": 0})
            if doc:
                return Profile(**doc)
        except PyMongoError:
            pass

    return _PROFILE_CACHE["default"]


def update_profile(values: Dict[str, object]) -> Profile:
    current = get_profile()
    updated = Profile(
        id="default",
        display_name=str(values.get("display_name", current.display_name)),
        timezone=str(values.get("timezone", current.timezone)),
        privacy_mode=str(values.get("privacy_mode", current.privacy_mode)),
        data_retention_days=int(
            values.get("data_retention_days", current.data_retention_days)
        ),
        local_only=bool(values.get("local_only", current.local_only)),
    )

    collection = _get_collection()
    if collection is not None:
        try:
            collection.update_one(
                {"id": "default"},
                {"$set": updated.__dict__},
                upsert=True,
            )
            return updated
        except PyMongoError:
            pass

    _PROFILE_CACHE["default"] = updated
    return updated
