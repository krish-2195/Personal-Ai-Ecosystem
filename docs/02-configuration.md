# Configuration Guide

Environment variables and settings for the Personal AI Ecosystem.

---

## 📄 .env File

Copy `.env.example` to `.env` and customize:

```bash
cp .env.example .env
# Edit .env with your settings
```

---

## ⚙️ Configuration Parameters

### **Application Settings**

| Variable | Default | Description | Example |
|----------|---------|-------------|---------|
| `APP_NAME` | Personal AI Ecosystem | Application display name | My AI Assistant |
| `APP_ENV` | local | Environment (local, staging, prod) | production |
| `API_HOST` | 0.0.0.0 | Backend bind address | 127.0.0.1 |
| `API_PORT` | 8000 | Backend port | 8000 |
| `API_BASE_URL` | http://localhost:8000 | Backend URL (public) | https://api.example.com |

### **Security**

| Variable | Default | Description | Example |
|----------|---------|-------------|---------|
| `API_KEY` | (empty) | Standard API key (optional) | sk_secret_12345 |
| `ADMIN_API_KEY` | (empty) | Admin API key (optional) | admin_secret_67890 |
| `CORS_ORIGINS` | localhost:8501,127.0.0.1:8501 | Allowed frontend origins (comma-separated) | https://app.example.com |

**How it works:**
- If `API_KEY` is set: POST/PATCH/DELETE/export require it in `X-API-Key` header
- If `ADMIN_API_KEY` is set: Admin endpoints require it
- If both are empty: No authentication (development only!)

---

### **LLM & AI**

| Variable | Default | Description | Example |
|----------|---------|-------------|---------|
| `OLLAMA_BASE_URL` | http://localhost:11434 | Ollama server URL | http://192.168.1.100:11434 |
| `OLLAMA_MODEL` | llama3.1:8b | LLM model name | mistral, neural-chat |

**Ollama Models:**
- `llama3.1:8b` - Fast, local (recommended)
- `mistral` - Smaller, faster
- `neural-chat` - Optimized for chat
- `phi` - Ultra-lightweight (<=3GB RAM)

---

### **Databases**

| Variable | Default | Description | Example |
|----------|---------|-------------|---------|
| `MONGO_URI` | mongodb://localhost:27017/personal_ai | MongoDB connection string | mongodb+srv://user:pass@cluster.mongodb.net/personal_ai |
| `NEO4J_URI` | bolt://localhost:7687 | Neo4j bolt connection | bolt://localhost:7687 |
| `NEO4J_USER` | neo4j | Neo4j username | neo4j |
| `NEO4J_PASSWORD` | changeme | Neo4j password | secure_password |

**MongoDB Connection Examples:**
```ini
# Docker Compose (default)
MONGO_URI=mongodb://localhost:27017/personal_ai

# MongoDB Atlas (cloud)
MONGO_URI=mongodb+srv://user:password@cluster0.mongodb.net/personal_ai?retryWrites=true&w=majority

# Docker with authentication
MONGO_URI=mongodb://db_user:db_pass@localhost:27017/personal_ai?authSource=admin
```

---

### **Integrations**

| Variable | Default | Description | Example |
|----------|---------|-------------|---------|
| `NYLAS_CLIENT_ID` | (empty) | Nylas email API key | your_nylas_id |
| `NYLAS_CLIENT_SECRET` | (empty) | Nylas secret | your_nylas_secret |
| `NYLAS_API_SERVER` | https://api.nylas.com | Nylas API endpoint | https://api.nylas.com |
| `PLAID_CLIENT_ID` | (empty) | Plaid finance API key | your_plaid_id |
| `PLAID_SECRET` | (empty) | Plaid secret | your_plaid_secret |
| `PLAID_ENV` | sandbox | Plaid environment | sandbox, development, production |
| `SCALEDOWN_API_KEY` | (empty) | ScaleDown compression API | your_scaledown_key |

**Integration Status:**
- Nylas & Plaid: Currently stubs (status endpoints only)
- Add credentials when ready to integrate
- System gracefully handles missing credentials

---

## 🚀 Configuration Scenarios

### **Scenario 1: Local Development (Minimal)**

```ini
APP_ENV=local
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
MONGO_URI=mongodb://localhost:27017/personal_ai
```

**Note:** No API keys = No authentication

---

### **Scenario 2: Development + Security**

```ini
APP_ENV=local
API_KEY=dev_key_12345
ADMIN_API_KEY=admin_key_67890
OLLAMA_BASE_URL=http://localhost:11434
MONGORITO_URI=mongodb://localhost:27017/personal_ai
CORS_ORIGINS=http://localhost:8501,http://127.0.0.1:8501
```

**Note:** Test API key protection

---

### **Scenario 3: Production Cloud (Render)**

```ini
APP_ENV=production
APP_BASE_URL=https://your-app.onrender.com
API_KEY=prod_key_long_random_string_here
ADMIN_API_KEY=admin_key_long_random_string_here
OLLAMA_BASE_URL=https://ollama.example.com  # Or local Ollama in same container
OLLAMA_MODEL=llama3.1:8b
MONGO_URI=mongodb+srv://user:password@cluster.mongodb.net/personal_ai
CORS_ORIGINS=https://your-app.onrender.com
```

**Note:** 
- Use strong random keys (32+ chars)
- Use MongoDB Atlas (cloud)
- Ollama can run in container or elsewhere

---

### **Scenario 4: With All Integrations**

```ini
API_KEY=your_api_key
ADMIN_API_KEY=your_admin_key
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
MONGO_URI=mongodb://localhost:27017/personal_ai
NYLAS_CLIENT_ID=your_nylas_id
NYLAS_CLIENT_SECRET=your_nylas_secret
PLAID_CLIENT_ID=your_plaid_id
PLAID_SECRET=your_plaid_secret
SCALEDOWN_API_KEY=your_scaledown_key
```

---

## 🔑 How to Generate API Keys

### **Quick (Development)**
```bash
# Generate random key
echo $(openssl rand -hex 16)
```

### **Secure (Production)**
```bash
# 32-character random key
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### **Using environment echo**
```powershell
# PowerShell
-join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | % {[char]$_})
```

---

## 🔒 Security Best Practices

### **DO:**
- ✅ Use strong random keys (32+ characters)
- ✅ Store secrets in `.env` (git-ignored)
- ✅ Use HTTPS in production
- ✅ Rotate keys regularly
- ✅ Use separate keys for admin and standard operations
- ✅ Limit CORS origins to your domain

### **DON'T:**
- ❌ Commit `.env` to git
- ❌ Use simple passwords (12345, password, etc.)
- ❌ Share API keys with others
- ❌ Use same key for dev and prod
- ❌ Allow wildcard CORS origins in production
- ❌ Log API keys

---

## 🔍 Verify Configuration

### **Check Configuration Loaded**
```powershell
# If you're in Python shell or testing:
from backend.config import get_settings
settings = get_settings()
print(f"App: {settings.app_name}")
print(f"Env: {settings.app_env}")
print(f"API Key configured: {bool(settings.api_key)}")
```

### **Test Admin Endpoint (Check Config)**
```powershell
# With admin key:
curl -H "X-API-Key: your_admin_key" http://localhost:8000/v1/admin/info

# Returns configuration status including API keys and CORS origins
```

### **Test Database Connection**
```powershell
curl http://localhost:8000/v1/db/ping
# Should return {"mongodb": {"ok": true}, "neo4j": {"ok": true}}
```

---

## 🌐 CORS Configuration

### **What is CORS?**
Cross-Origin Resource Sharing - allows frontend to call backend API

### **Setting CORS Origins**

```ini
# Single origin (most common development)
CORS_ORIGINS=http://localhost:8501

# Multiple origins (comma-separated)
CORS_ORIGINS=http://localhost:8501,http://127.0.0.1:8501,https://app.example.com

# Production (specific domain)
CORS_ORIGINS=https://myapp.com,https://www.myapp.com
```

### **Common CORS Origins**

| Scenario | Value |
|----------|-------|
| Local dev | http://localhost:8501 |
| Local network | http://192.168.1.100:8501 |
| Production | https://myapp.com |
| Both www and root | https://myapp.com,https://www.myapp.com |

### **Troubleshooting CORS**

If you get "CORS error":
1. Check `CORS_ORIGINS` includes your frontend URL
2. Verify frontend is accessing correct backend URL
3. Frontend must use `http://` if backend is `http://`
4. Restart backend after changing `.env`

---

## 📊 Environment-Specific Configs

### **Development (.env)**
```ini
APP_ENV=local
# No API keys (development)
# Verbose logging
# Localhost addresses
```

### **Staging (.env.staging)**
```ini
APP_ENV=staging
API_KEY=staging_key_xyz
CORS_ORIGINS=https://staging.example.com
# Point to staging databases
```

### **Production (.env.production)**
```ini
APP_ENV=production
API_KEY=prod_key_live_random_secure_key_here
ADMIN_API_KEY=admin_key_live_random_secure_key_here
CORS_ORIGINS=https://example.com
# Point to production databases
# Use strong, rotated keys
```

---

## 🔄 Reloading Configuration

### **Backend Restart**
```powershell
# Configuration is reloaded on uvicorn restart
python -m uvicorn backend.main:app --reload

# Changes to .env take effect on next start
```

### **Docker Rebuild**
```bash
docker-compose down
docker-compose up --build
```

---

## 🚨 Common Configuration Issues

### **"Connection refused" on MongoDB**
```
Solution:
1. Ensure MongoDB is running (docker ps)
2. Check MONGO_URI is correct
3. Verify network connectivity
```

### **"CORS blocked" error**
```
Solution:
1. Check CORS_ORIGINS includes frontend URL
2. Verify frontend is calling correct backend URL
3. Restart backend after changing .env
```

### **"Ollama not found"**
```
Solution:
1. Ensure Ollama is running (http://localhost:11434/api/tags)
2. Check OLLAMA_BASE_URL is correct
3. System works without Ollama (uses fallbacks)
```

### **"API key required but not configured"**
```
Solution:
1. Set API_KEY in .env if you want authentication
2. Or remove requirement by leaving API_KEY empty
3. Restart backend after changes
```

---

## 📝 .env.example Template

```ini
# Application
APP_NAME=Personal AI Ecosystem
APP_ENV=local
API_HOST=0.0.0.0
API_PORT=8000
API_BASE_URL=http://localhost:8000

# Security
API_KEY=
ADMIN_API_KEY=
CORS_ORIGINS=http://localhost:8501,http://127.0.0.1:8501

# LLM
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b

# Databases
MONGO_URI=mongodb://localhost:27017/personal_ai
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=changeme

# Integrations (optional)
NYLAS_CLIENT_ID=
NYLAS_CLIENT_SECRET=
NYLAS_API_SERVER=https://api.nylas.com
PLAID_CLIENT_ID=
PLAID_SECRET=
PLAID_ENV=sandbox
SCALEDOWN_API_KEY=
```

---

**Next:** [Setup Guide](01-setup.md) or [API Reference](07-api-reference.md)
