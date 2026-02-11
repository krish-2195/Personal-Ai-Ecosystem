from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
import os


def load_dotenv(path: Path | None = None) -> None:
	"""Lightweight .env loader to keep local dev dependency-free."""
	env_path = path or Path(__file__).resolve().parents[1] / ".env"
	if not env_path.exists():
		return

	for raw_line in env_path.read_text(encoding="utf-8").splitlines():
		line = raw_line.strip()
		if not line or line.startswith("#") or "=" not in line:
			continue
		key, value = line.split("=", 1)
		key = key.strip()
		value = value.strip().strip("\"'")
		os.environ.setdefault(key, value)


@dataclass(frozen=True)
class Settings:
	app_name: str
	app_env: str
	api_host: str
	api_port: int
	api_base_url: str
	api_key: str
	admin_api_key: str
	cors_origins: str
	ollama_base_url: str
	ollama_model: str
	mongo_uri: str
	neo4j_uri: str
	neo4j_user: str
	neo4j_password: str
	nylas_client_id: str
	nylas_client_secret: str
	nylas_api_server: str
	plaid_client_id: str
	plaid_secret: str
	plaid_env: str
	scaledown_api_key: str


def _get_env(key: str, default: str) -> str:
	return os.getenv(key, default)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
	return Settings(
		app_name=_get_env("APP_NAME", "Personal AI Ecosystem"),
		app_env=_get_env("APP_ENV", "local"),
		api_host=_get_env("API_HOST", "0.0.0.0"),
		api_port=int(_get_env("API_PORT", "8000")),
		api_base_url=_get_env("API_BASE_URL", "http://localhost:8000"),
		api_key=_get_env("API_KEY", ""),
		admin_api_key=_get_env("ADMIN_API_KEY", ""),
		cors_origins=_get_env(
			"CORS_ORIGINS",
			"http://localhost:8501,http://127.0.0.1:8501",
		),
		ollama_base_url=_get_env("OLLAMA_BASE_URL", "http://localhost:11434"),
		ollama_model=_get_env("OLLAMA_MODEL", "llama3.1:8b"),
		mongo_uri=_get_env("MONGO_URI", "mongodb://localhost:27017/personal_ai"),
		neo4j_uri=_get_env("NEO4J_URI", "bolt://localhost:7687"),
		neo4j_user=_get_env("NEO4J_USER", "neo4j"),
		neo4j_password=_get_env("NEO4J_PASSWORD", "changeme"),
		nylas_client_id=_get_env("NYLAS_CLIENT_ID", ""),
		nylas_client_secret=_get_env("NYLAS_CLIENT_SECRET", ""),
		nylas_api_server=_get_env("NYLAS_API_SERVER", "https://api.nylas.com"),
		plaid_client_id=_get_env("PLAID_CLIENT_ID", ""),
		plaid_secret=_get_env("PLAID_SECRET", ""),
		plaid_env=_get_env("PLAID_ENV", "sandbox"),
		scaledown_api_key=_get_env("SCALEDOWN_API_KEY", ""),
	)
