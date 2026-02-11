import json
import os
from typing import Any, Dict

import requests

import streamlit as st


API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(page_title="Personal AI Ecosystem", page_icon="🤖")

st.title("Personal AI Ecosystem")
st.caption("Privacy-first personal assistant (prototype shell)")

def api_get(path: str) -> Dict[str, Any]:
	headers = _auth_headers()
	response = requests.get(f"{API_BASE_URL}{path}", timeout=5, headers=headers)
	response.raise_for_status()
	return response.json()


def api_post(path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
	headers = _auth_headers()
	response = requests.post(
		f"{API_BASE_URL}{path}",
		json=payload,
		timeout=20,
		headers=headers,
	)
	response.raise_for_status()
	return response.json()


def api_patch(path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
	headers = _auth_headers()
	response = requests.patch(
		f"{API_BASE_URL}{path}",
		json=payload,
		timeout=20,
		headers=headers,
	)
	response.raise_for_status()
	return response.json()


def api_delete(path: str) -> Dict[str, Any]:
	headers = _auth_headers()
	response = requests.delete(
		f"{API_BASE_URL}{path}",
		timeout=20,
		headers=headers,
	)
	response.raise_for_status()
	return response.json()



def _auth_headers() -> Dict[str, str]:
	api_key = st.session_state.get("api_key", "")
	if api_key:
		return {"x-api-key": api_key}
	return {}


with st.sidebar:
	st.subheader("Backend")
	st.write(API_BASE_URL)
	st.text_input("API key", type="password", key="api_key")
	if st.button("Check API health"):
		try:
			payload = api_get("/health")
			st.success(f"{payload.get('status')} | {payload.get('app')}")
		except requests.RequestException as exc:
			st.error(f"API unreachable: {exc}")

	if st.button("Ping databases"):
		try:
			payload = api_get("/v1/db/ping")
			st.json(payload)
		except requests.RequestException as exc:
			st.error(f"DB ping failed: {exc}")

st.subheader("Chat with Ollama")
if "chat_history" not in st.session_state:
	st.session_state.chat_history = []

if st.button("Ping Ollama"):
	try:
		response = api_get("/v1/llm/ping")
		st.json(response)
	except requests.RequestException as exc:
		st.error(f"Ollama ping failed: {exc}")

chat_input = st.text_input("Your message")
if st.button("Send") and chat_input:
	st.session_state.chat_history.append({"role": "user", "content": chat_input})
	try:
		payload = {"messages": st.session_state.chat_history}
		response = api_post("/v1/llm/chat", payload)
		assistant_text = response.get("message", "")
		st.session_state.chat_history.append(
			{"role": "assistant", "content": assistant_text}
		)
	except requests.RequestException as exc:
		st.error(f"LLM error: {exc}")

for msg in st.session_state.chat_history:
	label = "You" if msg["role"] == "user" else "Assistant"
	st.write(f"**{label}:** {msg['content']}")

st.subheader("Route a Task to Agent")
task_type = st.selectbox("Task type", ["schedule", "email", "health", "finance"])
payload_text = st.text_area("Payload (JSON)", value="{}", height=100)
if st.button("Route task"):
	try:
		payload_obj = json.loads(payload_text or "{}")
		response = api_post(
			"/v1/agents/route",
			{"task_type": task_type, "payload": payload_obj},
		)
		st.json(response)
	except json.JSONDecodeError:
		st.error("Payload must be valid JSON.")
	except requests.RequestException as exc:
		st.error(f"Agent route failed: {exc}")

st.subheader("Auto Route (LLM or Heuristic)")
auto_query = st.text_input("Describe your task")
auto_payload_text = st.text_area("Auto payload (JSON)", value="{}", height=80)
prefer_llm = st.checkbox("Prefer LLM", value=True)
if st.button("Auto route") and auto_query:
	try:
		payload_obj = json.loads(auto_payload_text or "{}")
		response = api_post(
			"/v1/agents/auto",
			{
				"query": auto_query,
				"payload": payload_obj,
				"prefer_llm": prefer_llm,
			},
		)
		st.json(response)
	except json.JSONDecodeError:
		st.error("Payload must be valid JSON.")
	except requests.RequestException as exc:
		st.error(f"Auto route failed: {exc}")

st.subheader("ScaleDown Compression")
compress_text = st.text_area("Text to compress", height=120)
if st.button("Compress") and compress_text:
	try:
		response = api_post("/v1/utils/compress", {"text": compress_text})
		st.json(response)
	except requests.RequestException as exc:
		st.error(f"Compression failed: {exc}")

st.subheader("Voice (Simulated)")
voice_text = st.text_input("Text to synthesize")
if st.button("Synthesize") and voice_text:
	try:
		response = api_post("/v1/voice/synthesize", {"text": voice_text})
		st.json(response)
	except requests.RequestException as exc:
		st.error(f"Synthesis failed: {exc}")

st.subheader("Task Coordinator")
task_title = st.text_input("Task title")
task_details = st.text_area("Task details", height=80)
task_priority = st.selectbox("Priority", ["low", "medium", "high"], index=1)

if st.button("Create task") and task_title:
	try:
		payload = {
			"title": task_title,
			"details": task_details,
			"priority": task_priority,
		}
		response = api_post("/v1/tasks/create", payload)
		st.success(f"Created task: {response.get('id')}")
	except requests.RequestException as exc:
		st.error(f"Create failed: {exc}")

if st.button("Refresh task list"):
	try:
		response = api_get("/v1/tasks/list")
		st.json(response)
	except requests.RequestException as exc:
		st.error(f"List failed: {exc}")

if st.button("Load task stats"):
	try:
		response = api_get("/v1/tasks/stats")
		st.json(response)
	except requests.RequestException as exc:
		st.error(f"Stats failed: {exc}")

search_query = st.text_input("Search tasks")
if st.button("Search") and search_query:
	try:
		response = api_get(f"/v1/tasks/search?query={search_query}")
		st.json(response)
	except requests.RequestException as exc:
		st.error(f"Search failed: {exc}")

st.write("**Advanced Filter**")
col1, col2 = st.columns(2)
with col1:
	filter_priority = st.multiselect("Filter by priority", ["low", "medium", "high"])
	filter_status = st.multiselect("Filter by status", ["pending", "in_progress", "done"])
with col2:
	filter_date_from = st.text_input("Date from (ISO)", placeholder="2026-01-01T00:00:00")
	filter_date_to = st.text_input("Date to (ISO)", placeholder="2026-12-31T23:59:59")

filter_title_query = st.text_input("Filter by title/details", placeholder="optional")

if st.button("Apply filters"):
	try:
		params = []
		if filter_priority:
			for p in filter_priority:
				params.append(f"priority={p}")
		if filter_status:
			for s in filter_status:
				params.append(f"status={s}")
		if filter_date_from:
			params.append(f"date_from={filter_date_from}")
		if filter_date_to:
			params.append(f"date_to={filter_date_to}")
		if filter_title_query:
			params.append(f"title_query={filter_title_query}")
		
		query_str = "&".join(params)
		response = api_get(f"/v1/tasks/filter?{query_str}")
		st.json(response)
	except requests.RequestException as exc:
		st.error(f"Filter failed: {exc}")

task_id = st.text_input("Task ID to update")
task_status = st.selectbox("New status", ["pending", "in_progress", "done"])
if st.button("Update status") and task_id:
	try:
		response = api_patch(
			f"/v1/tasks/{task_id}/status",
			{"status": task_status},
		)
		st.json(response)
	except requests.RequestException as exc:
		st.error(f"Update failed: {exc}")

if st.button("Delete task") and task_id:
	try:
		response = api_delete(f"/v1/tasks/{task_id}")
		st.json(response)
	except requests.RequestException as exc:
		st.error(f"Delete failed: {exc}")

st.subheader("Profile & Privacy")
if st.button("Load profile"):
	try:
		response = api_get("/v1/profile")
		st.json(response)
	except requests.RequestException as exc:
		st.error(f"Load failed: {exc}")

profile_name = st.text_input("Display name", value="User")
profile_timezone = st.text_input("Timezone", value="UTC")
profile_privacy = st.selectbox("Privacy mode", ["strict", "balanced", "open"])
profile_retention = st.number_input(
	"Data retention days",
	min_value=1,
	max_value=3650,
	value=365,
)
profile_local_only = st.checkbox("Local-only processing", value=True)

if st.button("Save profile"):
	try:
		payload = {
			"display_name": profile_name,
			"timezone": profile_timezone,
			"privacy_mode": profile_privacy,
			"data_retention_days": int(profile_retention),
			"local_only": profile_local_only,
		}
		response = api_patch("/v1/profile", payload)
		st.json(response)
	except requests.RequestException as exc:
		st.error(f"Save failed: {exc}")

st.subheader("Integrations")
if st.button("Check Nylas (Email/Calendar)"):
	try:
		response = api_get("/v1/integrations/nylas")
		st.json(response)
	except requests.RequestException as exc:
		st.error(f"Nylas check failed: {exc}")

if st.button("Check Plaid (Finance)"):
	try:
		response = api_get("/v1/integrations/plaid")
		st.json(response)
	except requests.RequestException as exc:
		st.error(f"Plaid check failed: {exc}")

st.subheader("System Overview")
if st.button("Load system overview"):
	try:
		response = api_get("/v1/status/overview")
		st.json(response)
	except requests.RequestException as exc:
		st.error(f"Overview failed: {exc}")

st.subheader("Status Metrics")
if st.button("Load uptime metrics"):
	try:
		response = api_get("/v1/status/metrics")
		st.json(response)
	except requests.RequestException as exc:
		st.error(f"Metrics failed: {exc}")

st.subheader("Quick Plan")
plan_goal = st.text_area("Goal", height=80)
plan_priority = st.selectbox("Plan priority", ["low", "medium", "high"], index=1)
if st.button("Create plan") and plan_goal:
	try:
		response = api_post(
			"/v1/plan/quick",
			{"goal": plan_goal, "priority": plan_priority},
		)
		st.json(response)
	except requests.RequestException as exc:
		st.error(f"Plan failed: {exc}")

if st.button("Create plan (with existing)") and plan_goal:
	try:
		response = api_post(
			"/v1/plan/quick_with_existing",
			{"goal": plan_goal, "priority": plan_priority},
		)
		st.json(response)
	except requests.RequestException as exc:
		st.error(f"Plan failed: {exc}")

st.subheader("Conversations")
conv_title = st.text_input("Conversation title")
if st.button("Create conversation") and conv_title:
	try:
		response = api_post("/v1/conversations/create", {"title": conv_title})
		st.success(f"Created conversation: {response.get('id')}")
	except requests.RequestException as exc:
		st.error(f"Create failed: {exc}")

conv_id = st.text_input("Conversation ID")
if st.button("Load conversation") and conv_id:
	try:
		response = api_get(f"/v1/conversations/{conv_id}")
		st.json(response)
	except requests.RequestException as exc:
		st.error(f"Load failed: {exc}")

message_role = st.selectbox("Message role", ["user", "assistant", "system"])
message_content = st.text_area("Message content", height=80)
if st.button("Add message") and conv_id and message_content:
	try:
		response = api_post(
			f"/v1/conversations/{conv_id}/message",
			{"role": message_role, "content": message_content},
		)
		st.json(response)
	except requests.RequestException as exc:
		st.error(f"Add failed: {exc}")

if st.button("List conversations"):
	try:
		response = api_get("/v1/conversations/list")
		st.json(response)
	except requests.RequestException as exc:
		st.error(f"List failed: {exc}")

if st.button("Load conversation stats"):
	try:
		response = api_get("/v1/conversations/stats")
		st.json(response)
	except requests.RequestException as exc:
		st.error(f"Stats failed: {exc}")

search_conv_query = st.text_input("Search conversations")
if st.button("Search conversations") and search_conv_query:
	try:
		response = api_get(
			f"/v1/conversations/search?query={search_conv_query}"
		)
		st.json(response)
	except requests.RequestException as exc:
		st.error(f"Search failed: {exc}")

st.subheader("Conversation Summary")
summary_conv_id = st.text_input("Conversation ID for summary")
summary_prefer_llm = st.checkbox("Prefer LLM summary", value=True)
if st.button("Summarize conversation") and summary_conv_id:
	try:
		response = api_get(
			f"/v1/conversations/{summary_conv_id}/summary?prefer_llm={str(summary_prefer_llm).lower()}"
		)
		st.json(response)
	except requests.RequestException as exc:
		st.error(f"Summary failed: {exc}")

st.subheader("Export Data")
if st.button("Export everything"):
	try:
		response = api_get("/v1/export/all")
		st.json(response)
	except requests.RequestException as exc:
		st.error(f"Export failed: {exc}")

st.subheader("Audit Log")
audit_limit = st.number_input("Show last N events", min_value=1, max_value=200, value=50)
if st.button("Load audit log"):
	try:
		response = api_get(f"/v1/audit/list?limit={int(audit_limit)}")
		st.json(response)
	except requests.RequestException as exc:
		st.error(f"Audit load failed: {exc}")

st.subheader("Compression Summary")
if st.button("Compress conversation summary"):
	try:
		response = api_post("/v1/compression/conversations", {})
		st.json(response)
	except requests.RequestException as exc:
		st.error(f"Compression summary failed: {exc}")

st.subheader("Analytics Summary")
if st.button("Load analytics summary"):
	try:
		response = api_get("/v1/analytics/summary")
		st.json(response)
	except requests.RequestException as exc:
		st.error(f"Analytics failed: {exc}")

st.subheader("Demo Data")
if st.button("Seed demo data"):
	try:
		response = api_post("/v1/demo/seed", {})
		st.json(response)
	except requests.RequestException as exc:
		st.error(f"Seed failed: {exc}")

st.subheader("Maintenance")
if st.button("Run data cleanup"):
	try:
		response = api_post("/v1/maintenance/cleanup", {})
		st.json(response)
	except requests.RequestException as exc:
		st.error(f"Cleanup failed: {exc}")

st.subheader("Admin Info")
if st.button("Load admin info"):
	try:
		response = api_get("/v1/admin/info")
		st.json(response)
	except requests.RequestException as exc:
		st.error(f"Admin info failed: {exc}")
