# Architecture Overview

High-level design and data flow of the Personal AI Ecosystem.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (Streamlit)                    │
│        http://localhost:8501 - Interactive UI               │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/JSON
┌────────────────────────▼────────────────────────────────────┐
│                  BACKEND (FastAPI)                          │
│            http://localhost:8000/docs                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           16 Routers (42 Endpoints)                 │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │ Tasks │ Conv │ Agents │ Profile │ Audit │ Admin ... │   │
│  └───────┬──────┬────────┬────────┬──────┬─────────────┘   │
│          │      │        │        │      │                 │
│  ┌───────▼──────▼────────▼────────▼──────▼──────────────┐   │
│  │         Business Logic Layer                       │   │
│  │  (Routing, LLM calls, Data validation)            │   │
│  └───────┬──────┬────────┬────────┬──────┬──────────────┘   │
│          │      │        │        │      │                 │
│  ┌───────▼──────▼────────▼────────▼──────▼──────────────┐   │
│  │    Persistence Layer (Store modules)              │   │
│  │  Tasks│Conv│Profile│Audit + Fallback Cache       │   │
│  └───────┬──────┬────────┬────────┬──────┬──────────────┘   │
└──────────┼──────┼────────┼────────┼──────┼──────────────────┘
           │      │        │        │      │
      ┌────▼───┬──▼───┬────▼────┬───▼──┬──▼──┐
      │         │      │         │      │     │
┌─────▼─┐  ┌────▼┐ ┌──▼────┐ ┌──▼──┐ ┌▼────┐ │
│MongoDB│  │Neo4j│ │Ollama │ │Nylas│ │Plaid│ │
└───────┘  └─────┘ └───────┘ └─────┘ └─────┘ │
                                             │
                         External Services ──┘
```

---

## 📦 Core Components

### 1. **Frontend (Streamlit)**
- **File**: `frontend/app.py` (434 lines)
- **Role**: Interactive user interface
- **Features**: 50+ UI sections
  - Task management (CRUD, search, filter, stats)
  - Conversations (create, add messages, summarize)
  - Agent routing (manual + auto)
  - Profile management
  - Data export
  - Admin info
  - System health checks

**Key State Management:**
```python
st.session_state.api_key      # User's API key
st.session_state.chat_history # Conversation memory
```

---

### 2. **Backend (FastAPI)**
- **File**: `backend/main.py`
- **Framework**: FastAPI 0.115.0
- **Port**: 8000
- **Features**:
  - 16 routers (42 endpoints)
  - CORS middleware
  - API key authentication middleware
  - Auto-generated Swagger docs at `/docs`

**Request Flow:**
```
Request → CORS Check → API Key Validation → Router → Handler → Response
```

---

### 3. **Routers (16 modules)**

| Router | Endpoints | Purpose |
|--------|-----------|---------|
| `/tasks` | 7 | Task CRUD, search, filter, stats |
| `/conversations` | 7 | Conversation management, summarization |
| `/agents` | 3 | Agent routing, auto-routing |
| `/profile` | 2 | User profile management |
| `/audit` | 2 | Audit event logging |
| `/integrations` | 3 | Nylas, Plaid, Ollama status |
| `/export` | 1 | Full data export |
| `/admin` | 1 | Admin info endpoint |
| `/status` | 2 | System health metrics |
| `/planner` | 2 | Goal-to-tasks planning |
| `/llm` | 1 | Ollama chat endpoint |
| `/voice` | 1 | Text-to-speech |
| `/compression` | 1 | Conversation compression |
| `/analytics` | 1 | System analytics |
| `/demo` | 1 | Demo data seeding |
| `/maintenance` | 1 | Data cleanup |

---

### 4. **Data Storage Layer**

Each data model has its own store module (`backend/{module}/store.py`):

#### **Tasks Store** (`backend/tasks/store.py`)
```python
_TASKS: Dict[str, TaskItem]  # In-memory cache

# Dual-write pattern:
# 1. Write to MongoDB (if available)
# 2. Fallback write to _TASKS cache
```

**TaskItem:**
```python
@dataclass
class TaskItem:
    id: str                # UUID
    title: str            # Task name
    details: str          # Description
    priority: str         # low|medium|high
    status: str          # pending|in_progress|done
    created_at: str      # ISO timestamp
    updated_at: str      # ISO timestamp
```

#### **Conversations Store** (`backend/conversations/store.py`)
```python
@dataclass
class ConversationMessage:
    role: str            # user|assistant
    content: str         # Message text
    timestamp: str       # ISO timestamp + Z

@dataclass
class Conversation:
    id: str              # UUID
    title: str           # Conversation title
    messages: List[ConversationMessage]
```

#### **Profiles Store** (`backend/profiles/store.py`)
```python
@dataclass
class Profile:
    id: str              # Always "default"
    display_name: str    # User's name
    timezone: str        # America/New_York
    privacy_mode: str    # strict|relaxed
    data_retention_days: int  # Audit cleanup threshold
    local_only: bool     # True = no external API calls
```

#### **Audit Store** (`backend/audit/store.py`)
```python
@dataclass
class AuditEvent:
    id: str              # UUID
    event_type: str      # task.create, task.update, etc.
    message: str         # Human-readable description
    timestamp: str       # ISO timestamp
    meta: Dict           # Additional context
```

---

### 5. **Persistence Strategy**

#### **Dual-Write Pattern**
```python
# Example from tasks/store.py
def create_task(...) -> TaskItem:
    task = TaskItem(...)
    
    # Try MongoDB first
    collection = _get_collection()
    if collection is not None:
        try:
            collection.insert_one(task.__dict__)
            return task
        except PyMongoError:
            pass  # Fail gracefully
    
    # Fallback to in-memory cache
    _TASKS[task_id] = task
    return task
```

**Benefits:**
- ✅ Works without MongoDB
- ✅ Data survives temporary DB outages
- ✅ Fast reads from cache
- ✅ Persistent writes to MongoDB when available

#### **Fallback Logic**
```python
def list_tasks():
    # Try MongoDB first
    collection = _get_collection()
    if collection is not None:
        try:
            docs = collection.find({}, {"_id": 0})
            return [TaskItem(**doc) for doc in docs]
        except PyMongoError:
            pass
    
    # Fallback: Return from cache
    return list(_TASKS.values())
```

---

### 6. **Security Architecture**

#### **API Key Middleware**
```python
async def api_key_middleware(request: Request, call_next):
    """
    Validates API keys for protected endpoints
    """
    path = request.url.path
    
    # Skip if no key configured
    if not API_KEY and not ADMIN_API_KEY:
        return await call_next(request)
    
    # Check protection rules
    if should_protect(path, method):
        key = request.headers.get("x-api-key")
        if not key_is_valid(key):
            return 401 Unauthorized
    
    return await call_next(request)
```

#### **Protection Rules**
- **Standard API_KEY protects:**
  - All POST/PUT/PATCH/DELETE
  - `/v1/export/*`
  - `/v1/maintenance/*`

- **Admin API_KEY protects:**
  - `/v1/admin/*`

- **Read endpoints** (GET): No auth required

---

### 7. **Agent Routing System**

#### **Architecture**
```
Input → Router Selection → Agent Execution → Result
         ├─ Manual (explicit task_type)
         └─ Auto (LLM-based selection)
```

#### **Agent Flow**
```python
# Manual routing
POST /v1/agents/route {"task_type": "schedule", "data": {...}}
                        ↓
                    Route lookup
                        ↓
                    ScheduleAgent.run()
                        ↓
                    Return result

# Auto-routing
POST /v1/agents/auto_route {"input": "Schedule meeting...", "context": {}}
                            ↓
                        Ollama inference
                        (determine agent)
                            ↓
                        Route agent
                            ↓
                        Return result
```

**Agents:**
- `ScheduleAgent`: Calendar/meeting management
- `EmailAgent`: Email composition and sending
- `HealthAgent`: Health tracking
- `FinanceAgent`: Budget and finance tracking

---

### 8. **Data Flow Example: Create Task**

```
1. UI (Streamlit)
   ├─ User clicks "Create task"
   ├─ Fills: title, details, priority
   └─ Submits form

2. Frontend (app.py)
   ├─ Validates inputs
   ├─ Makes POST request to /v1/tasks/create
   └─ Sets X-API-Key header if configured

3. Backend (main.py)
   ├─ CORS middleware checks origin
   ├─ API key middleware validates key
   └─ Routes to tasks router

4. Router (tasks/router.py)
   ├─ Validates with Pydantic schema
   ├─ Calls store.create_task()
   ├─ Logs audit event
   └─ Returns TaskResponse

5. Store (tasks/store.py)
   ├─ Creates TaskItem with timestamp
   ├─ Tries MongoDB.insert_one()
   ├─ Falls back to _TASKS cache
   └─ Returns created task

6. Response to Frontend
   ├─ Task ID, title, status, timestamps
   └─ UI displays success message

7. Persistence
   ├─ MongoDB: Document stored in tasks collection
   ├─ Audit: Event logged in audit_events collection
   └─ Cache: Task in-memory for quick access
```

---

## 🗄️ Database Design

### **MongoDB Database: `personal_ai`**

#### Collections:
```
personal_ai
├── tasks              # Task documents
│   ├── _id (ObjectId)
│   ├── id (UUID)
│   ├── title
│   ├── details
│   ├── priority
│   ├── status
│   ├── created_at (ISO string)
│   └── updated_at (ISO string)
│
├── conversations      # Conversation documents
│   ├── _id (ObjectId)
│   ├── id (UUID)
│   ├── title
│   └── messages (array)
│       ├── role (user|assistant)
│       ├── content
│       └── timestamp
│
├── profiles          # User profile (usually 1 document)
│   ├── _id (ObjectId)
│   ├── id ("default")
│   ├── display_name
│   ├── timezone
│   ├── privacy_mode
│   ├── data_retention_days
│   └── local_only
│
└── audit_events      # Audit trail (append-only)
    ├── _id (ObjectId)
    ├── id (UUID)
    ├── event_type
    ├── message
    ├── timestamp (ISO string)
    └── meta (object)
```

### **Neo4j Graph Database (optional)**

```
Nodes:
- Person (user profile)
- Task (work items)
- Conversation (chat history)
- Agent (AI agents)

Relationships:
- OWNS (person → task)
- PARTICIPATES_IN (person → conversation)
- ASSIGNED_TO (task → agent)
- CONTAINS (conversation → message)
```

---

## 🔄 Deployment Architecture

### **Development (Docker Compose)**
```
docker-compose.yml
├── backend (FastAPI)
├── frontend (Streamlit)
├── mongo (MongoDB)
└── neo4j (Neo4j)

All on localhost:
- API: http://localhost:8000
- UI: http://localhost:8501
- Mongo: localhost:27017
- Neo4j: http://localhost:7474
```

### **Production (Render)**
```
render.yaml
├── Backend Service
│   ├─ Build: pip install -r requirements.txt
│   ├─ Start: uvicorn backend.main:app
│   └─ Port: Render-assigned
│
└── Frontend Service
    ├─ Build: Same image
    ├─ Start: streamlit run frontend/app.py
    └─ Port: 10000
```

---

## 📊 Data Flow Diagram

```
┌─────────────┐
│  User (UI)  │
└──────┬──────┘
       │ Click/Type
       ▼
┌─────────────────────────────┐
│  Streamlit (frontend/app.py)│
│  - Form validation          │
│  - Session state management │
│  - API calls                │
└──────┬──────────────────────┘
       │ HTTP POST/GET/PATCH
       ▼
┌──────────────────────────────┐
│  FastAPI (backend/main.py)   │
│  - CORS check                │
│  - Auth validation           │
│  - Router dispatch           │
└──────┬───────────────────────┘
       │ Router selection
       ▼
┌──────────────────────────────┐
│  Handler (e.g., tasks.py)    │
│  - Business logic            │
│  - Data validation           │
│  - Audit logging             │
└──────┬───────────────────────┘
       │
   ┌───┴────────────┬──────────────┐
   │ Persist        │ Log          │
   ▼                ▼              │
┌────────────┐  ┌──────────────┐  │
│MongoDB     │  │Audit Event   │  │
│(tasks,     │  │Store         │  │
│conversations
   └────────────┘  └──────────────┘
   │
   │ Fallback
   ▼
┌────────────────────┐
│In-Memory Cache     │
│(_TASKS, _CACHE)    │
└────────────────────┘
```

---

## 🔗 integration Points

### **External Services**
- **Ollama**: Local LLM at http://localhost:11434
- **Nylas**: Email/calendar API (stub)
- **Plaid**: Finance API (stub)
- **MongoDB Atlas**: Cloud MongoDB (optional)

### **Extension Points**
1. Add new routers in `backend/`
2. Add new agents in `backend/agents/`
3. Add new store modules for data models
4. Add new Streamlit sections in `frontend/app.py`

---

## 🚀 Performance Characteristics

| Operation | Latency | Source |
|-----------|---------|--------|
| Create task | 10-50ms | MongoDB or memory |
| Search task | 50-200ms | MongoDB query or cache scan |
| Summarize conv | 1-5s | Ollama LLM inference |
| Auto-route | 500ms-2s | Ollama inference for agent selection |
| List all tasks | 10-100ms | Single MongoDB query |

---

## 📈 Scalability Considerations

**Current Design (Single User):**
- ✅ All data in-memory cache
- ✅ MongoDB single instance
- ✅ No load balancing needed

**For Multi-Tenant:**
- Partition data by user_id
- Add Redis for distributed cache
- Use MongoDB sharding
- Add API rate limiting
- Multi-instance backend behind load balancer

---

**Next:** See [Database Design](05-database.md) for more details, or [API Reference](07-api-reference.md) for endpoints.
