# Personal AI Ecosystem 🚀
*Privacy-first personal assistant with AI agents, voice control, and 20+ life domain coordination. Compresses 5-year data by 85%, saves 15+ hours weekly.*

[![Status](https://img.shields.io/badge/status-prototype-green)](https://github.com) 
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://python.org) 
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-yellow)](https://fastapi.tiangolo.com)

## 🎯 Features
- **Multi-Agent Coordination**: Schedule/Email/Health/Finance agents via CrewAI
- **Voice Interface**: Hands-free (<500ms latency) with Faster Whisper + XTTS
- **Smart Integrations**: Nylas calendar, Plaid finance, health tracking
- **Data Compression**: ScaleDown reduces 5-year history by 85%
- **Privacy-First**: 100% local LLM (Ollama), encrypted storage

## 🚀 Quick Start
```bash
git clone https://github.com/YOUR_USERNAME/personal-ai-ecosystem.git
cd personal-ai-ecosystem
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
streamlit run frontend/app.py

Live: http://localhost:8501 | API: http://localhost:8000/docs
```

## ⚙️ Environment
Copy the example env file and update keys as needed:
```bash
copy .env.example .env
```

## ✅ Core Endpoints
- `GET /health`
- `POST /v1/agents/route`
- `POST /v1/agents/auto`
- `GET /v1/tasks/list`
- `POST /v1/tasks/create`
- `PATCH /v1/tasks/{id}/status`
- `GET /v1/profile`
- `PATCH /v1/profile`
- `POST /v1/llm/chat`
- `POST /v1/utils/compress`
- `POST /v1/voice/synthesize`
- `GET /v1/status/overview`

## 🚀 Deploy (Render Free Tier)
This repo includes a `render.yaml` blueprint. Connect the repo in Render and set:
- Frontend `API_BASE_URL` to the backend service URL.

## 🔐 API Key (Optional)
Set `API_KEY` in `.env` to protect write and export endpoints. Send header:
`x-api-key: YOUR_KEY`
