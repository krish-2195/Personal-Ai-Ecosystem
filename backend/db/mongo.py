from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from pymongo import MongoClient

from backend.config import get_settings


@dataclass
class MongoStatus:
    connected: bool
    db_name: str
    server_info: Dict[str, Any]


def get_mongo_client() -> MongoClient:
    settings = get_settings()
    return MongoClient(settings.mongo_uri, serverSelectionTimeoutMS=1500)


def ping_mongo() -> MongoStatus:
    client = get_mongo_client()
    info = client.server_info()
    db_name = client.get_default_database().name
    return MongoStatus(connected=True, db_name=db_name, server_info=info)
