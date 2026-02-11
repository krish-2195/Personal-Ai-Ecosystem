# Personal AI Ecosystem - Documentation

Welcome to the **Personal AI Ecosystem** documentation. This is a privacy-first personal assistant backend with multi-agent coordination, conversational memory, and extensible architecture.

## 📚 Documentation Guide

### Getting Started
- **[Installation & Setup](01-setup.md)** - How to install and run locally or in the cloud
- **[Configuration](02-configuration.md)** - Environment variables and settings
- **[Quick Start](03-quickstart.md)** - Get running in 5 minutes

### Understanding the System
- **[Architecture Overview](04-architecture.md)** - System design, components, and data flow
- **[Database Design](05-database.md)** - MongoDB schema, Neo4j setup, caching strategy
- **[Security & Privacy](06-security.md)** - API keys, encryption, data retention, audit trails

### Development
- **[API Reference](07-api-reference.md)** - Complete endpoint documentation (42 endpoints)
- **[Features Guide](08-features.md)** - Overview of all 42 features by category
- **[Frontend UI Guide](09-frontend.md)** - Streamlit interface sections and interactions
- **[Testing](10-testing.md)** - How to run tests and add new ones

### Deployment
- **[Docker Setup](11-docker.md)** - Local Docker Compose and image building
- **[Cloud Deployment](12-render.md)** - Deploy to Render.com (free tier)
- **[Production Checklist](13-production.md)** - Before going to production

### Integration
- **[Integrations Guide](14-integrations.md)** - Nylas, Plaid, Ollama, External APIs
- **[Voice Features](15-voice.md)** - Whisper + XTTS voice pipeline
- **[LLM Integration](16-llm.md)** - Ollama setup and customization

### Advanced Topics
- **[Extending the System](17-extending.md)** - Add new agents, routers, features
- **[Performance Tuning](18-performance.md)** - Optimization tips and best practices
- **[Troubleshooting](19-troubleshooting.md)** - Common issues and solutions

---

## 🎯 Quick Links

### Popular Documents
- [Setup in 5 minutes](03-quickstart.md)
- [All 42 endpoints](07-api-reference.md)
- [Deploy to Render](12-render.md)
- [Add a new feature](17-extending.md)

### For Developers
- [API Reference (Postman-ready)](07-api-reference.md)
- [Frontend Component Guide](09-frontend.md)
- [Testing Framework](10-testing.md)
- [Adding Custom Agents](17-extending.md#adding-agents)

### For DevOps
- [Docker & Docker Compose](11-docker.md)
- [Environment Configuration](02-configuration.md)
- [Production Checklist](13-production.md)
- [Troubleshooting](19-troubleshooting.md)

---

## 📋 System Overview

**Personal AI Ecosystem** provides:
- ✅ **Privacy-first**: Local LLM (Ollama), optional encryption, configurable data retention
- ✅ **Multi-agent**: Routing system for scheduling, email, health, finance tasks
- ✅ **Conversational**: Memory with summarization and full message history
- ✅ **Extensible**: Modular architecture, easy to add features
- ✅ **Auditable**: Complete audit trail of all operations
- ✅ **Resilient**: In-memory cache fallback if database unavailable

**Tech Stack:**
- Backend: FastAPI (Python 3.10+)
- Frontend: Streamlit
- Databases: MongoDB + Neo4j
- LLM: Ollama (local)
- Deployment: Docker or Render

---

## 🚀 Get Started Now

### Option 1: Docker (Recommended)
```bash
cd personal-ai-ecosystem
docker-compose up
```
Then open http://localhost:8501

### Option 2: Local Setup
```bash
pip install -r requirements.txt
python -m uvicorn backend.main:app --reload &
streamlit run frontend/app.py
```
See [Setup Guide](01-setup.md) for details.

---

## 📊 Feature Coverage

The system includes **42 implemented features**:

| Category | Count | Examples |
|----------|-------|----------|
| Core Features | 8 | Task CRUD, Conversations, Profiles, Export |
| Agent System | 4 | Auto-routing, Multi-agent, Scheduling Agent |
| Data Ops | 5 | Search, Stats, Filtering, Cleanup, Compression |
| Integration | 6 | Ollama, Voice, Nylas, Plaid, External APIs |
| Audit & Admin | 5 | Audit logging, Admin info, Status metrics |
| Testing | 5+ | Unit tests, Integration tests |

See [Features Guide](08-features.md) for complete list.

---

## 🔗 Navigation

- **Previous Level**: [Back to main README](../README.md)
- **Next**: [Installation & Setup](01-setup.md)
- **API Docs**: [FastAPI Swagger](http://localhost:8000/docs) (when running)
- **Frontend**: [Streamlit UI](http://localhost:8501) (when running)

---

## ❓ Need Help?

1. **Setup issues?** → See [Setup Guide](01-setup.md) or [Troubleshooting](19-troubleshooting.md)
2. **API questions?** → See [API Reference](07-api-reference.md)
3. **Want to add a feature?** → See [Extending](17-extending.md)
4. **Deployment help?** → See [Deployment Guide](11-docker.md) or [Render Guide](12-render.md)

---

**Last Updated:** February 2026
**Version:** 1.0 (42 Features)
**Status:** Production-ready prototype
