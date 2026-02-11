from __future__ import annotations

import time

from fastapi import APIRouter

from backend.config import get_settings
from backend.db.mongo import ping_mongo
from backend.db.neo4j_db import ping_neo4j
from backend.integrations.nylas_stub import check_nylas
from backend.integrations.plaid_stub import check_plaid


router = APIRouter(prefix="/v1/status", tags=["status"])
_START_TIME = time.time()


def get_uptime_seconds() -> int:
	return int(time.time() - _START_TIME)


@router.get("/overview")
def overview() -> dict:
	settings = get_settings()
	payload = {
		"app": settings.app_name,
		"env": settings.app_env,
		"ollama_model": settings.ollama_model,
		"integrations": {},
		"databases": {},
	}

	try:
		nylas = check_nylas()
		payload["integrations"]["nylas"] = {
			"configured": nylas.configured,
			"ok": nylas.ok,
		}
	except Exception:
		payload["integrations"]["nylas"] = {"configured": False, "ok": False}

	try:
		plaid = check_plaid()
		payload["integrations"]["plaid"] = {
			"configured": plaid.configured,
			"ok": plaid.ok,
		}
	except Exception:
		payload["integrations"]["plaid"] = {"configured": False, "ok": False}

	try:
		mongo = ping_mongo()
		payload["databases"]["mongo"] = {
			"connected": mongo.connected,
			"db": mongo.db_name,
		}
	except Exception:
		payload["databases"]["mongo"] = {"connected": False}

	try:
		neo4j = ping_neo4j()
		payload["databases"]["neo4j"] = {
			"connected": neo4j.connected,
			"info": neo4j.server_info,
		}
	except Exception:
		payload["databases"]["neo4j"] = {"connected": False}

	return payload


@router.get("/metrics")
def metrics() -> dict:
	return {"uptime_seconds": get_uptime_seconds()}
