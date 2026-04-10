# Workflow: Docker — Build, Run, and Deploy
---
description: How to build and run the project with Docker (dev + production)
---

## Prerequisites
- Docker installed: `docker --version`
- Docker Compose installed: `docker compose version`

---

## 🛠️ Development Mode (hot reload, SQLite)

```bash
# 1. Build the image
docker compose build

# 2. Start all services (docker-compose.override.yml auto-applied for dev)
docker compose up

# 3. Open Swagger UI
# → http://localhost:8000/docs

# With logs visible and in background:
docker compose up -d && docker compose logs -f app
```

### Dev URLs
| Service | URL |
|---------|-----|
| FastAPI API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| Flower (Celery monitor) | http://localhost:5555 |
| PostgreSQL | localhost:5432 |
| Redis | localhost:6379 |

---

## 🚀 Production Mode (PostgreSQL, multi-worker)

```bash
# 1. Set production environment variables in .env:
#    DATABASE_URL=postgresql+asyncpg://postgres:strongpassword@db:5432/content_tool_db
#    APP_ENV=production
#    DEBUG=false
#    SECRET_KEY=<32+ char random key>
#    OPENAI_API_KEY=sk-...
#    POSTGRES_PASSWORD=strongpassword

# 2. Run WITHOUT the dev override
docker compose -f docker-compose.yml up -d

# 3. Check all services are healthy
docker compose ps
```

---

## 🔧 Useful Docker Commands

```bash
# View running containers
docker compose ps

# View app logs (live)
docker compose logs -f app

# View celery worker logs
docker compose logs -f celery

# Restart only the app (after code changes in prod)
docker compose restart app

# Stop all services
docker compose down

# Stop and delete volumes (⚠️ deletes DB data)
docker compose down -v

# Open a shell inside the running app container
docker compose exec app bash

# Run database migrations inside container
docker compose exec app alembic upgrade head

# Run tests inside container
docker compose exec app pytest tests/ -v

# Rebuild image (after requirements.txt changes)
docker compose build --no-cache
docker compose up -d
```

---

## 📊 Service Architecture in Docker

```
┌─────────────────────────────────────────────────────┐
│                   content_ai_net                     │
│                 (Docker Bridge Network)              │
│                                                     │
│  ┌──────────────┐    ┌───────────┐    ┌───────────┐ │
│  │   app:8000   │───▶│  db:5432  │    │redis:6379 │ │
│  │  (FastAPI)   │    │ (Postgres)│    │  (Redis)  │ │
│  └──────┬───────┘    └───────────┘    └─────┬─────┘ │
│         │                                   │       │
│  ┌──────▼───────┐    ┌───────────┐          │       │
│  │  celery      │────│ flower    │          │       │
│  │  (worker)    │    │ :5555     │          │       │
│  └──────────────┘    └───────────┘          │       │
│         └─────────────────────────────────▶│       │
└─────────────────────────────────────────────────────┘
         │                                   │
    localhost:8000                     localhost:6379
    (exposed to host)              (exposed for dev tools)
```

---

## 🔐 Production Security Checklist

- [ ] `SECRET_KEY` is a random 32+ char string (`python -c "import secrets; print(secrets.token_hex(32))"`)
- [ ] `DEBUG=false` in `.env`
- [ ] `APP_ENV=production` in `.env`
- [ ] PostgreSQL password is strong (not `postgres`)
- [ ] DB port `5432` is NOT exposed in production (remove ports from docker-compose.yml)
- [ ] Redis port `6379` is NOT exposed in production
- [ ] App runs as non-root user ✅ (already in Dockerfile)
- [ ] HTTPS via reverse proxy (nginx/Traefik) in front of port 8000

---

## 🌐 Deploying to a VPS/Cloud (Example: Ubuntu server)

```bash
# 1. SSH into your server
ssh user@your-server-ip

# 2. Install Docker
curl -fsSL https://get.docker.com | bash
sudo usermod -aG docker $USER

# 3. Clone your repo
git clone <your-repo-url>
cd content_tool

# 4. Create and configure .env
cp .env.example .env
nano .env   # Set OPENAI_API_KEY, SECRET_KEY, POSTGRES_PASSWORD

# 5. Run production stack
docker compose -f docker-compose.yml up -d

# 6. Check health
curl http://localhost:8000/health
```
