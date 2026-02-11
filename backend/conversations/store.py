from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List
from uuid import uuid4

from pymongo import ReturnDocument
from pymongo.errors import PyMongoError

from backend.db.mongo import get_mongo_client


@dataclass
class ConversationMessage:
    role: str
    content: str
    timestamp: str


@dataclass
class Conversation:
    id: str
    title: str
    messages: List[ConversationMessage]


_CACHE: Dict[str, Conversation] = {}


def _get_collection():
    try:
        client = get_mongo_client()
        db = client.get_default_database()
        return db["conversations"]
    except Exception:
        return None


def create_conversation(title: str) -> Conversation:
    conv_id = str(uuid4())
    conversation = Conversation(id=conv_id, title=title, messages=[])

    collection = _get_collection()
    if collection is not None:
        try:
            collection.insert_one(
                {
                    "id": conversation.id,
                    "title": conversation.title,
                    "messages": [],
                }
            )
            return conversation
        except PyMongoError:
            pass

    _CACHE[conv_id] = conversation
    return conversation


def list_conversations() -> List[Conversation]:
    collection = _get_collection()
    if collection is not None:
        try:
            docs = collection.find({}, {"_id": 0})
            return [
                Conversation(
                    id=doc["id"],
                    title=doc["title"],
                    messages=[
                        ConversationMessage(**msg)
                        for msg in doc.get("messages", [])
                    ],
                )
                for doc in docs
            ]
        except PyMongoError:
            pass

    return list(_CACHE.values())


def get_conversation(conv_id: str) -> Conversation | None:
    collection = _get_collection()
    if collection is not None:
        try:
            doc = collection.find_one({"id": conv_id}, {"_id": 0})
            if doc:
                return Conversation(
                    id=doc["id"],
                    title=doc["title"],
                    messages=[
                        ConversationMessage(**msg)
                        for msg in doc.get("messages", [])
                    ],
                )
        except PyMongoError:
            pass

    return _CACHE.get(conv_id)


def append_message(conv_id: str, role: str, content: str) -> Conversation | None:
    timestamp = datetime.utcnow().isoformat() + "Z"
    message = ConversationMessage(role=role, content=content, timestamp=timestamp)

    collection = _get_collection()
    if collection is not None is not None:
        try:
            result = collection.find_one_and_update(
                {"id": conv_id},
                {"$push": {"messages": message.__dict__}},
                projection={"_id": 0},
                return_document=ReturnDocument.AFTER,
            )
            if result:
                return Conversation(
                    id=result["id"],
                    title=result["title"],
                    messages=[
                        ConversationMessage(**msg)
                        for msg in result.get("messages", [])
                    ],
                )
        except PyMongoError:
            pass

    conversation = _CACHE.get(conv_id)
    if not conversation:
        return None
    conversation.messages.append(message)
    return conversation
