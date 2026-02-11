from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from neo4j import GraphDatabase

from backend.config import get_settings


@dataclass
class Neo4jStatus:
    connected: bool
    server_info: Dict[str, Any]


def get_neo4j_driver():
    settings = get_settings()
    return GraphDatabase.driver(
        settings.neo4j_uri,
        auth=(settings.neo4j_user, settings.neo4j_password),
    )


def ping_neo4j() -> Neo4jStatus:
    driver = get_neo4j_driver()
    with driver.session() as session:
        result = session.run("RETURN 1 as ok")
        record = result.single()
    driver.close()
    return Neo4jStatus(connected=True, server_info={"ok": record["ok"]})
