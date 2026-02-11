# Quick Start - Get Running in 5 Minutes

The fastest way to get the Personal AI Ecosystem up and running.

---

## ⚡ 5-Minute Start (Docker)

### **Step 1: Install Docker** (2 min)
Download and install from: https://www.docker.com/products/docker-desktop

Verify:
```powershell
docker --version
```

### **Step 2: Clone/Navigate to Project** (30 sec)
```powershell
cd "c:\Users\Krish\project\New folder\GenAi4genz\personal-ai-ecosystem"
```

### **Step 3: Start Services** (30 sec)
```powershell
docker-compose up
```

Wait for output:
```
backend_1  | Application startup complete
frontend_1 | Local URL: http://localhost:8501
```

### **Step 4: Open Browser** (30 sec)
Open: **http://localhost:8501**

### **Step 5: Test** (1 min)
1. Click "Check API health" → Should show "ok | Personal AI Ecosystem"
2. Create a task:
   - Enter title: "My First Task"
   - Click "Create task"
3. Click "Refresh task list" → Should see your task

**Done!** You're running the system.

---

## 🎯 Basic Usage (Frontend)

### **Sidebar (Top Left)**
- Enter backend URL (default: localhost:8000)
- Optionally set API key
- Health check buttons
- Database ping

### **Main Sections**

#### **Chat with Ollama**
```
1. Type message: "What is AI?"
2. Click Send
3. See response from local LLM
```

#### **Task Coordinator**
```
1. Enter title: "Learn Rust"
2. Enter details: "Complete Rust book"
3. Priority: medium
4. Click "Create task"
5. See task in list
```

#### **Task Management**
```
- Refresh task list: See all tasks
- Search: Find tasks by keyword
- Advanced Filter: Filter by priority, status, date
- Load task stats: See breakdown by status
- Update status: Change task state
- Delete task: Remove task
```

#### **Conversations**
```
1. Enter title: "Vacation planning"
2. Click "Create conversation"
3. Add message: "I want to visit Japan"
4. See responses
5. Summarize conversation
```

#### **Profile & Privacy**
```
- Load profile: See current settings
- Update profile: Change name, timezone, retention
```

---

## 🧪 Quick Tests

### **Test 1: Create Multiple Tasks**
```
1. Create task 1: "Buy milk" (high)
2. Create task 2: "Buy eggs" (medium)
3. Create task 3: "Buy bread" (low)
4. Click "Refresh task list" → See all 3
```

### **Test 2: Task Filtering**
```
1. Click "Apply filters"
   - Priority: Select "high"
   - Status: Select "pending"
2. Should see only "Buy milk"
```

### **Test 3: Conversation**
```
1. Create conversation: "Meeting notes"
2. Add message: "Discussed Q1 goals"
3. Get summary: Should summarize the message
```

### **Test 4: Data Export**
```
1. Click "Export all data" button
2. Should download JSON with tasks, conversations, profile
```

---

## 📋 API Quick Reference

### **Check Health**
```powershell
curl http://localhost:8000/health
# {"status":"ok","app":"Personal AI Ecosystem"}
```

### **Create Task (curl)**
```powershell
curl -X POST http://localhost:8000/v1/tasks/create `
  -H "Content-Type: application/json" `
  -d '{"title":"My task","details":"Do this","priority":"high"}'
```

### **List Tasks**
```powershell
curl http://localhost:8000/v1/tasks/list
```

### **Interactive API Docs**
Open: **http://localhost:8000/docs**

This shows all 42 endpoints with live testing.

---

## 🔧 Configuration for Quick Start

Default `.env` should work. To customize:

```powershell
# Edit .env file
# Most important settings:
API_KEY=my_secret_key          # (optional) Require key for writes
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
```

See [Configuration Guide](02-configuration.md) for all options.

---

## 🛑 Stopping the System

### **From Docker Compose Terminal**
Press `Ctrl+C`

### **From Another Terminal**
```powershell
docker-compose down
```

---

## 🚨 Troubleshooting

### **"Connection refused"**
```
→ Docker is running, started services?
→ Run: docker ps
→ If mongo/neo4j missing, restart: docker-compose up
```

### **"Port 8501 already in use"**
```
→ Another app using port 8501
→ Either:
  a) Stop other app
  b) Change port in docker-compose.yml (ports: "8502:8501")
```

### **"Can't connect to backend"**
```
→ Click "Check API health" in UI
→ If fails, backend not started
→ Check docker logs: docker logs personal-ai-ecosystem_backend_1
```

### **"Ollama not responding"**
```
→ That's OK - system works without Ollama
→ Chat will use fallback responses
→ To enable: Start Ollama: ollama run llama3.1:8b
```

---

## 📚 Next Steps

After running locally:

1. **Learn the system**: Read [Architecture Overview](04-architecture.md)
2. **Explore all endpoints**: See [API Reference](07-api-reference.md)
3. **View all features**: See [Features Guide](08-features.md)
4. **Deploy to cloud**: See [Cloud Deployment](12-render.md)

---

## 💡 Pro Tips

### **Tip 1: Copy/Paste Task from UI**
Most API responses show in JSON viewer - easy to copy/work with

### **Tip 2: Use Swagger API Docs**
Visit http://localhost:8000/docs for interactive testing of all endpoints

### **Tip 3: Set API Key for Testing Auth**
Add to .env: `API_KEY=test_key_123`
Then use headers in curl:
```powershell
curl -H "X-API-Key: test_key_123" http://localhost:8000/v1/tasks/list
```

### **Tip 4: Seed Demo Data**
Click "Seed demo data" button to populate with sample tasks + conversation

### **Tip 5: Export Data Before Deleting**
Always export first: "Export all data" → saves JSON backup

---

## 📞 Common Questions

**Q: Where is my data stored?**
A: In MongoDB container (data lost on `docker-compose down -v`) or in-memory cache

**Q: Can I use it without Docker?**
A: Yes! See [Full Setup Guide](01-setup.md) for local Python setup

**Q: Do I need Ollama?**
A: No. System uses fallback responses if Ollama unavailable.

**Q: How do I add custom features?**
A: See [Extending Guide](17-extending.md)

**Q: Is it production-ready?**
A: Not yet. Add error handling, monitoring, rate limiting first.

---

## ✅ Verification Checklist

After starting, verify:

- [ ] Frontend loads (http://localhost:8501)
- [ ] "Check API health" button shows "ok"
- [ ] Can create a task
- [ ] Can list tasks
- [ ] Can search tasks
- [ ] Can create conversation
- [ ] Can add message to conversation
- [ ] API docs load (http://localhost:8000/docs)

All checked? **You're ready to use it!**

---

**Next:** [Full Setup Guide](01-setup.md) for more options, or [API Reference](07-api-reference.md) for endpoint details.

**Having issues?** See [Troubleshooting](19-troubleshooting.md)
