from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request

from backend.config import get_settings, load_dotenv
from backend.utils.security import api_key_guard
from backend.agents.router import router as agents_router
from backend.db.router import router as db_router
from backend.utils.router import router as utils_router
from backend.integrations.router import router as llm_router
from backend.integrations.voice_router import router as voice_router
from backend.integrations.external_router import router as external_router
from backend.tasks.router import router as tasks_router
from backend.profiles.router import router as profile_router
from backend.status.router import router as status_router
from backend.planner.router import router as planner_router
from backend.conversations.router import router as conversations_router
from backend.export.router import router as export_router
from backend.audit.router import router as audit_router
from backend.compression.router import router as compression_router
from backend.analytics.router import router as analytics_router
from backend.demo.router import router as demo_router
from backend.maintenance.router import router as maintenance_router
from backend.admin.router import router as admin_router


load_dotenv()
settings = get_settings()

app = FastAPI(title=settings.app_name)

app.include_router(agents_router)
app.include_router(db_router)
app.include_router(utils_router)
app.include_router(llm_router)
app.include_router(voice_router)
app.include_router(external_router)
app.include_router(tasks_router)
app.include_router(profile_router)
app.include_router(status_router)
app.include_router(planner_router)
app.include_router(conversations_router)
app.include_router(export_router)
app.include_router(audit_router)
app.include_router(compression_router)
app.include_router(analytics_router)
app.include_router(demo_router)
app.include_router(maintenance_router)
app.include_router(admin_router)

cors_origins = [origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()]
app.add_middleware(
	CORSMiddleware,
	allow_origins=cors_origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


@app.middleware("http")
async def api_key_middleware(request: Request, call_next):
	guard = api_key_guard(request)
	if guard:
		return guard
	return await call_next(request)


@app.get("/health")
def health() -> dict:
	return {
		"status": "ok",
		"app": settings.app_name,
		"env": settings.app_env,
	}


@app.get("/v1/agent/ping")
def agent_ping() -> dict:
	return {
		"message": "Agent router ready",
		"ollama": settings.ollama_model,
	}
