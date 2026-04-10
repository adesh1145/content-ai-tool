# Workflow: Run Locally
---
description: How to run the Content AI Tool dev server
---

## Prerequisites
- venv activated: `source venv/bin/activate`
- `.env` file configured with at minimum: `OPENAI_API_KEY`

## Start Dev Server (Hot Reload)
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## URLs
| URL | Purpose |
|-----|---------|
| http://localhost:8000/docs | Swagger UI — interactive API explorer |
| http://localhost:8000/redoc | ReDoc — clean API docs |
| http://localhost:8000/health | Health check endpoint |
| http://localhost:8000/openapi.json | OpenAPI spec (JSON) |

## Testing an Endpoint (curl examples)
```bash
# Register a user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123", "full_name": "Test User"}'

# Generate a blog post
curl -X POST http://localhost:8000/api/v1/content/blog \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "How to Learn Python in 30 Days",
    "focus_keyword": "learn python",
    "tone": "educational",
    "word_count": 800
  }'

# Generate social media post
curl -X POST http://localhost:8000/api/v1/content/social \
  -H "Content-Type: application/json" \
  -d '{"topic": "AI productivity tips", "platform": "linkedin", "tone": "professional"}'

# Analyze SEO
curl -X POST http://localhost:8000/api/v1/seo/analyze \
  -H "Content-Type: application/json" \
  -d '{"content": "Your article content here...", "focus_keyword": "your keyword"}'
```

## Logs
Logs are written to `logs/app.log` and also printed to console.

## Common Issues
| Issue | Fix |
|-------|-----|
| `OPENAI_API_KEY not set` | Add key to `.env` file |
| `Module not found` | Run `pip install -r requirements.txt` in venv |
| `Port 8000 in use` | Use `--port 8001` |
| `DB error on startup` | Delete `content_tool.db` and restart |
