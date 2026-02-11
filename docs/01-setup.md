# Setup & Installation Guide

Install and run the Personal AI Ecosystem locally or in the cloud.

## 📋 Prerequisites

Choose your platform:

- **Docker** (Recommended): [Install Docker Desktop](https://www.docker.com/products/docker-desktop)
- **Local Python**: Python 3.10+, pip, and MongoDB
- **Cloud**: Render.com account (free tier available)

---

## 🐳 Option 1: Docker (Easiest)

### 1. Install Docker Desktop

Download and install from: https://www.docker.com/products/docker-desktop

Then verify:
```powershell
docker --version
# Output: Docker version 25.x.x, build xxxxx
```

### 2. Clone/Navigate to Project

```powershell
cd "c:\Users\Krish\project\New folder\GenAi4genz\personal-ai-ecosystem"
```

### 3. Start All Services

```powershell
docker-compose up
```

This starts 4 containers:
- **Backend API**: http://localhost:8000
- **Frontend UI**: http://localhost:8501
- **MongoDB**: localhost:27017
- **Neo4j**: http://localhost:7474

### 4. Access the System

Open your browser to:
- **http://localhost:8501** - Streamlit UI (main interface)
- **http://localhost:8000/docs** - FastAPI/Swagger docs (API reference)
- **http://localhost:7474** - Neo4j Browser (graph database)

### 5. Stop Services

```powershell
# In the terminal running docker-compose, press Ctrl+C
# Or in another terminal:
docker-compose down
```

---

## 🖥️ Option 2: Local Python Setup

### 1. Install Python 3.10+

Verify:
```powershell
python --version
# Output: Python 3.10.x or higher
```

### 2. Install Dependencies

```powershell
cd "c:\Users\Krish\project\New folder\GenAi4genz\personal-ai-ecosystem"
pip install -r requirements.txt
```

Dependencies include:
- fastapi==0.115.0
- streamlit==1.39.0
- pymongo==4.8.0
- neo4j==5.24.0
- requests==2.32.3
- pytest==8.3.2

### 3. Start MongoDB

**Option A: Using Docker (just Mongo)**
```powershell
docker run -d -p 27017:27017 --name mongo mongo:6
```

**Option B: Using MongoDB locally** (if installed)
```powershell
mongod
```

**Option C: Skip MongoDB** (uses in-memory cache, data lost on restart)
```powershell
# Don't start Mongo - system will use fallback caching
```

### 4. Start Backend (Terminal 1)

```powershell
cd "c:\Users\Krish\project\New folder\GenAi4genz\personal-ai-ecosystem"
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

Access API at: http://localhost:8000/docs

### 5. Start Frontend (Terminal 2)

```powershell
cd "c:\Users\Krish\project\New folder\GenAi4genz\personal-ai-ecosystem"
streamlit run frontend/app.py
```

Output:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

Open browser to: http://localhost:8501

### 6. Stop Services

```powershell
# In each terminal, press Ctrl+C
# In a new terminal, if Mongo was running:
docker stop mongo  # (if using Docker for Mongo)
```

---

## ⚡ Option 3: Quick Test (API Only)

Test the API without starting the full system:

```powershell
# In one terminal, start backend only:
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# In another terminal, test endpoints:
curl http://localhost:8000/health
curl http://localhost:8000/v1/tasks/list
curl http://localhost:8000/v1/db/ping
```

---

## 🔧 Configuration

Create a `.env` file in the project root with any custom settings:

```ini
# Copy from .env.example and customize:
APP_NAME=Personal AI Ecosystem
APP_ENV=local
API_KEY=your-secret-key-here
ADMIN_API_KEY=your-admin-key-here

# Ollama (local LLM)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b

# MongoDB
MONGO_URI=mongodb://localhost:27017/personal_ai

# Integration credentials (optional)
NYLAS_CLIENT_ID=your-key-here
PLAID_CLIENT_ID=your-key-here
```

See [Configuration Guide](02-configuration.md) for all options.

---

## 🧪 Verify Installation

### 1. Health Check

```powershell
curl http://localhost:8000/health
# Expected output:
# {"status":"ok","app":"Personal AI Ecosystem"}
```

### 2. Create a Task

```powershell
curl -X POST http://localhost:8000/v1/tasks/create `
  -H "Content-Type: application/json" `
  -d '{"title":"My first task","details":"Test task","priority":"medium"}'
```

### 3. List Tasks

```powershell
curl http://localhost:8000/v1/tasks/list
```

### 4. Access Frontend

Open browser to: **http://localhost:8501**

Click "Check API health" button - should show "ok | Personal AI Ecosystem"

---

## 🚨 Troubleshooting

### Docker won't start
```powershell
# Check Docker is running:
docker ps

# If not, restart Docker Desktop

# Check for port conflicts (8000, 8501, 27017):
netstat -ano | findstr "8000\|8501\|27017"
```

### MongoDB connection failed
```powershell
# Option 1: System will use in-memory cache (data not persisted)
# Option 2: Start MongoDB manually
docker run -d -p 27017:27017 mongo:6

# Option 3: Use Atlas (cloud MongoDB)
# Update MONGO_URI in .env to use MongoDB Atlas connection string
```

### Port already in use
```powershell
# Change ports in docker-compose.yml or:
docker-compose -p myapp up  # Different project name
```

### Streamlit can't connect to backend
```powershell
# Check backend is running:
curl http://localhost:8000/health

# Check API_BASE_URL in frontend/app.py or set in env
```

See [Troubleshooting](19-troubleshooting.md) for more solutions.

---

## 📊 What's Running

After successful setup, you should have:

| Service | Port | URL | Status |
|---------|------|-----|--------|
| Backend API | 8000 | http://localhost:8000 | ✅ Check /health |
| Streamlit UI | 8501 | http://localhost:8501 | ✅ Interactive |
| MongoDB | 27017 | localhost:27017 | ✅ Or in-memory fallback |
| Neo4j | 7687 | bolt://localhost:7687 | ✅ Graph DB (optional) |
| Ollama | 11434 | http://localhost:11434 | ⚠️ Optional, for LLM |

---

## 🎯 Next Steps

1. **Learn the system**: Read [Architecture Overview](04-architecture.md)
2. **Explore features**: See [Features Guide](08-features.md)
3. **Test the API**: Check [API Reference](07-api-reference.md)
4. **Deploy to cloud**: See [Render Deployment](12-render.md)
5. **Add a feature**: See [Extending](17-extending.md)

---

## 📚 More Resources

- [Configuration Guide](02-configuration.md)
- [Docker Setup](11-docker.md)
- [Cloud Deployment](12-render.md)
- [API Reference](07-api-reference.md)
- [Troubleshooting](19-troubleshooting.md)

---

**Need help?** See [Troubleshooting](19-troubleshooting.md) or check the main [Documentation Index](README.md).
