# API Reference - All 42 Endpoints

Complete reference for all FastAPI endpoints. Base URL: `http://localhost:8000`

---

## 🏥 Health & Status (3 endpoints)

### Health Check
```
GET /health
```
**Response:**
```json
{"status": "ok", "app": "Personal AI Ecosystem"}
```
**Use:** Verify API is running

---

### Agent Ping
```
GET /v1/agent/ping
```
**Response:**
```json
{"agent": "central-coordinator", "status": "online"}
```
**Use:** Check main agent status

---

### Database Ping
```
GET /v1/db/ping
```
**Response:**
```json
{
  "mongodb": {"ok": true, "host": "localhost:27017"},
  "neo4j": {"ok": true, "status": "connected"}
}
```
**Use:** Verify database connectivity

---

## 📝 Tasks (7 endpoints)

### List All Tasks
```
GET /v1/tasks/list
```
**Response:**
```json
[
  {
    "id": "uuid",
    "title": "Buy groceries",
    "details": "Milk, eggs, bread",
    "priority": "medium",
    "status": "pending",
    "created_at": "2026-02-12T10:00:00",
    "updated_at": "2026-02-12T10:00:00"
  }
]
```

---

### Create Task
```
POST /v1/tasks/create
Content-Type: application/json
X-API-Key: {api_key} (optional)

{
  "title": "Buy groceries",
  "details": "Milk, eggs, bread",
  "priority": "low|medium|high"
}
```
**Response:** Same as task object above
**Auth:** Requires API_KEY if configured
**Audit:** Logged as `task.create`

---

### Search Tasks
```
GET /v1/tasks/search?query=groceries
```
**Params:**
- `query` (string): Search in title and details

**Response:** Array of matching tasks

---

### Advanced Filter Tasks
```
GET /v1/tasks/filter?priority=high&status=pending&date_from=2026-02-01T00:00:00&date_to=2026-02-28T23:59:59&title_query=team
```
**Params (all optional):**
- `priority` (list): low, medium, high
- `status` (list): pending, in_progress, done
- `date_from` (ISO): Filter by created_at >= 
- `date_to` (ISO): Filter by created_at <=
- `title_query` (string): Text in title/details

**Response:** Filtered task array

---

### Update Task Status
```
PATCH /v1/tasks/{task_id}/status
Content-Type: application/json
X-API-Key: {api_key} (optional)

{"status": "in_progress"}
```
**Status options:** pending, in_progress, done
**Response:** Updated task object
**Auth:** Requires API_KEY if configured
**Audit:** Logged as `task.status`

---

### Delete Task
```
DELETE /v1/tasks/{task_id}
X-API-Key: {api_key} (optional)
```
**Response:**
```json
{"task_id": "uuid", "deleted": true}
```
**Auth:** Requires API_KEY if configured
**Audit:** Logged as `task.delete`

---

### Task Statistics
```
GET /v1/tasks/stats
```
**Response:**
```json
{
  "total": 15,
  "by_status": {"pending": 8, "in_progress": 5, "done": 2},
  "by_priority": {"low": 3, "medium": 10, "high": 2}
}
```

---

## 💬 Conversations (7 endpoints)

### Create Conversation
```
POST /v1/conversations/create
Content-Type: application/json
X-API-Key: {api_key} (optional)

{"title": "My Summer Plans"}
```
**Response:**
```json
{"id": "uuid", "title": "My Summer Plans", "messages": []}
```

---

### List Conversations
```
GET /v1/conversations/list
```
**Response:** Array of conversation objects

---

### Get Conversation
```
GET /v1/conversations/{conv_id}
```
**Response:**
```json
{
  "id": "uuid",
  "title": "My Summer Plans",
  "messages": [
    {
      "role": "user",
      "content": "I want to visit Japan",
      "timestamp": "2026-02-12T10:00:00Z"
    },
    {
      "role": "assistant",
      "content": "Great! Japan is amazing...",
      "timestamp": "2026-02-12T10:01:00Z"
    }
  ]
}
```

---

### Add Message
```
POST /v1/conversations/{conv_id}/message
Content-Type: application/json
X-API-Key: {api_key} (optional)

{
  "role": "user",
  "content": "I want to visit Japan"
}
```
**Role:** user, assistant
**Response:** Updated conversation object
**Audit:** Logged as `conversation.message`

---

### Search Conversations
```
GET /v1/conversations/search?query=Japan
```
**Response:** Array of matching conversations (by title)

---

### Get Conversation Summary
```
GET /v1/conversations/{conv_id}/summary
```
**Response:**
```json
{
  "id": "uuid",
  "summary": "User discussed summer vacation plans to Japan..."
}
```
**Note:** Uses LLM (Ollama) if available, otherwise heuristic

---

### Conversation Statistics
```
GET /v1/conversations/stats
```
**Response:**
```json
{
  "total_conversations": 5,
  "total_messages": 32,
  "avg_messages_per_conversation": 6.4
}
```

---

## 🧠 Agents & Routing (3 endpoints)

### Route Task to Agent
```
POST /v1/agents/route
Content-Type: application/json

{
  "task_type": "schedule|email|health|finance",
  "data": {}
}
```
**Response:**
```json
{
  "agent": "ScheduleAgent",
  "status": "success",
  "summary": "Meeting scheduled...",
  "data": {}
}
```

---

### Auto-Route Task (LLM)
```
POST /v1/agents/auto_route
Content-Type: application/json

{
  "input": "Schedule a meeting with John tomorrow at 2pm",
  "context": {}
}
```
**Response:** Same as manual routing
**Note:** Uses Ollama to determine best agent

---

### Agent Ping
```
GET /v1/llm/ping
```
**Response:**
```json
{"ok": true, "model": "llama3.1:8b"}
```
**Use:** Check Ollama availability

---

## 👤 Profiles (2 endpoints)

### Get Profile
```
GET /v1/profile
```
**Response:**
```json
{
  "id": "default",
  "display_name": "Krish",
  "timezone": "America/New_York",
  "privacy_mode": "strict",
  "data_retention_days": 365,
  "local_only": true
}
```

---

### Update Profile
```
PATCH /v1/profile
Content-Type: application/json
X-API-Key: {api_key} (optional)

{
  "display_name": "Krish Kumar",
  "timezone": "America/Los_Angeles",
  "privacy_mode": "relaxed",
  "data_retention_days": 180,
  "local_only": false
}
```
**Auth:** Requires API_KEY if configured

---

## 🔍 Search & Filtering (2 endpoints)

See Tasks and Conversations sections above for:
- `/v1/tasks/search`
- `/v1/conversations/search`
- `/v1/tasks/filter` (advanced)

---

## 📊 Analytics (1 endpoint)

### System Analytics
```
GET /v1/analytics/summary
```
**Response:**
```json
{
  "tasks_total": 42,
  "conversations_total": 8,
  "messages_total": 156,
  "audit_events_sample": [
    {
      "id": "uuid",
      "event_type": "task.create",
      "message": "Task created: Buy groceries",
      "timestamp": "2026-02-12T10:00:00Z"
    }
  ]
}
```

---

## 📤 Export & Backup (1 endpoint)

### Export All Data
```
GET /v1/export/all
X-API-Key: {api_key} (required if API_KEY is set)
```
**Response:**
```json
{
  "profile": {...},
  "tasks": [...],
  "conversations": [...]
}
```
**Use:** Privacy-first data export, all user data in one JSON
**Auth:** Requires API_KEY if configured

---

## 🔐 Admin (1 endpoint)

### Admin Info
```
GET /v1/admin/info
X-API-Key: {admin_key} (required if ADMIN_API_KEY is set)
```
**Response:**
```json
{
  "app_name": "Personal AI Ecosystem",
  "environment": "local",
  "uptime_seconds": 3600,
  "ollama_model": "llama3.1:8b",
  "cors_origins": ["http://localhost:8501"],
  "api_key_configured": true,
  "admin_api_key_configured": true
}
```
**Auth:** Requires ADMIN_API_KEY if configured

---

## 📝 Audit Logging (2 endpoints)

### List Audit Events
```
GET /v1/audit/events?limit=50
```
**Response:**
```json
[
  {
    "id": "uuid",
    "event_type": "task.create",
    "message": "Task created: Buy groceries",
    "timestamp": "2026-02-12T10:00:00Z",
    "meta": {"task_id": "uuid", "priority": "medium"}
  }
]
```

---

### Cleanup Old Audit Events
```
POST /v1/maintenance/cleanup
X-API-Key: {api_key} (optional)
```
**Response:**
```json
{"deleted_count": 23}
```
**Use:** Remove audit events older than data_retention_days
**Note:** Called automatically or manually to clean old events

---

## 🗜️ Compression (1 endpoint)

### Compress Conversations
```
POST /v1/compression/conversations
X-API-Key: {api_key} (optional)

{
  "conversation_ids": ["uuid1", "uuid2"]
}
```
**Response:**
```json
{
  "original_size": 1245,
  "compressed_size": 856,
  "compression_ratio": 0.687,
  "summary": "Compressed conversation..."
}
```

---

## 📆 Planning (2 endpoints)

### Quick Plan
```
POST /v1/plan/quick
Content-Type: application/json

{
  "goal": "Plan a vacation: Find flights, Book hotel, Pack bags",
  "priority": "medium"
}
```
**Response:**
```json
{
  "created_task_ids": ["uuid1", "uuid2", "uuid3"],
  "titles": ["Find flights", "Book hotel", "Pack bags"]
}
```
**Use:** Convert a goal into subtasks automatically

---

### Quick Plan with Existing Tasks
```
POST /v1/plan/quick_with_existing
Content-Type: application/json

{
  "goal": "Buy groceries: milk, eggs, bread",
  "priority": "high"
}
```
**Response:**
```json
{
  "created_task_ids": ["uuid1", "uuid2", "uuid3"],
  "titles": ["Get milk", "Get eggs", "Get bread"],
  "existing_tasks": ["Buy groceries", "Meal prep"]
}
```
**Use:** Plan while being aware of existing tasks

---

## 🗣️ Voice (1 endpoint)

### Text-to-Speech
```
POST /v1/voice/synthesize
Content-Type: application/json

{"text": "Hello, how are you today?"}
```
**Response:**
```json
{
  "text": "Hello, how are you today?",
  "synthesis": "base64-encoded-audio-or-path"
}
```
**Note:** Requires XTTS configuration

---

## 🔗 Integrations (3 endpoints)

### Nylas Status
```
GET /v1/integrations/nylas
```
**Response:**
```json
{
  "ok": false,
  "configured": false,
  "message": "Nylas not configured"
}
```

---

### Plaid Status
```
GET /v1/integrations/plaid
```
**Response:** Similar to Nylas

---

### Ollama Chat
```
POST /v1/llm/chat
Content-Type: application/json

{
  "messages": [
    {"role": "user", "content": "What is AI?"}
  ]
}
```
**Response:**
```json
{
  "message": "AI is artificial intelligence...",
  "model": "llama3.1:8b"
}
```

---

## 🧪 Demo (1 endpoint)

### Seed Demo Data
```
POST /v1/demo/seed
```
**Response:**
```json
{
  "tasks_created": 3,
  "conversations_created": 1,
  "messages_created": 2
}
```
**Use:** Populate database with sample data for testing

---

## 📊 System Status (2 endpoints)

### System Overview
```
GET /v1/status/overview
```
**Response:**
```json
{
  "nylas": {"ok": false},
  "plaid": {"ok": false},
  "mongodb": {"ok": true},
  "neo4j": {"ok": true}
}
```

---

### Uptime Metrics
```
GET /v1/status/metrics
```
**Response:**
```json
{"uptime_seconds": 7200}
```

---

## 🔑 Authentication

### API Key Protection

Two-level authentication:

**Standard API Key** (for write operations):
```
X-API-Key: {api_key}
```
Protects: POST, PATCH, DELETE, /export, /maintenance

**Admin API Key** (for admin operations):
```
X-API-Key: {admin_key}
```
Protects: /admin/*, /v1/admin/info

### How to Use

1. Set `API_KEY` and/or `ADMIN_API_KEY` in `.env`
2. Include in request headers:
   ```powershell
   curl -H "X-API-Key: your-key-here" http://localhost:8000/api/endpoint
   ```

### Rules

- ✅ GET requests: No key required
- ✅ POST/PATCH/DELETE: Requires standard `API_KEY` if set
- ✅ Admin endpoints: Requires `ADMIN_API_KEY` if set
- ✅ Export endpoint: Requires standard `API_KEY` if set

---

## 📈 Endpoint Summary

| Category | Count | Auth | Docs |
|----------|-------|------|------|
| Health | 3 | No | Above ↑ |
| Tasks | 7 | Optional | Above ↑ |
| Conversations | 7 | Optional | Above ↑ |
| Agents | 3 | No | Above ↑ |
| Profiles | 2 | Optional | Above ↑ |
| Analytics | 1 | No | Above ↑ |
| Export | 1 | Optional | Above ↑ |
| Admin | 1 | Required | Above ↑ |
| Audit | 2 | Optional | Above ↑ |
| Compression | 1 | Optional | Above ↑ |
| Planning | 2 | No | Above ↑ |
| Voice | 1 | No | Above ↑ |
| Integrations | 3 | No | Above ↑ |
| Demo | 1 | No | Above ↑ |
| Status | 2 | No | Above ↑ |
| **Total** | **42** | - | - |

---

## 🧪 Testing with curl/Postman

### Create Task Example
```bash
curl -X POST http://localhost:8000/v1/tasks/create \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "title": "Buy coffee",
    "details": "Arabica beans",
    "priority": "high"
  }'
```

### List Tasks Example
```bash
curl http://localhost:8000/v1/tasks/list
```

### Filter Tasks Example
```bash
curl "http://localhost:8000/v1/tasks/filter?priority=high&status=pending"
```

---

## 🔗 Interactive API Docs

When running locally, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Both auto-generated from FastAPI code.

---

**Next:** See [Frontend Guide](09-frontend.md) for UI documentation.
