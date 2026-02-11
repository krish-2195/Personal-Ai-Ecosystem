from __future__ import annotations

from fastapi import APIRouter

from backend.db.mongo import ping_mongo
from backend.db.neo4j_db import ping_neo4j


router = APIRouter(prefix="/v1/db", tags=["db"])


@router.get("/ping")
def ping_databases() -> dict:
	mongo = ping_mongo()
	neo4j = ping_neo4j()
	return {
		"mongo": {
			"connected": mongo.connected,
			"db": mongo.db_name,
		},
		"neo4j": {
			"connected": neo4j.connected,
			"info": neo4j.server_info,
		},
	}
