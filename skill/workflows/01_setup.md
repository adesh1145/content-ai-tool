# Workflow: Project Setup
---
description: How to set up the Content AI Tool project from scratch
---

## Step 1: Clone & Enter Project
```bash
git clone <repo-url>
cd content_tool
```

## Step 2: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
# venv\Scripts\activate    # Windows
```

## Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

## Step 4: Configure Environment
```bash
cp .env.example .env
# Edit .env and fill in:
# - OPENAI_API_KEY (required)
# - SECRET_KEY (change to 32+ char random string)
# - DATABASE_URL (default SQLite works for dev)
```

## Step 5: Run the Server
```bash
uvicorn app.main:app --reload
```

## Step 6: Verify
- Open http://localhost:8000/docs — Swagger UI with all endpoints
- Open http://localhost:8000/health — Health check

## Step 7: (Optional) Redis + Celery for async tasks
```bash
redis-server &                          # Start Redis
celery -A app.infrastructure.celery.worker.celery_app worker --loglevel=info
```
