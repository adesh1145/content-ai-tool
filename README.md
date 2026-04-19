# Content AI Tool 🚀

**Industry-grade AI Content Generation Backend**
Built with FastAPI + LangChain + LangGraph following Clean Architecture + SOLID principles.

---

## 🏛️ Architecture

**Clean Architecture (Feature-First) + SOLID Principles**

Each of the 9 features is a self-contained vertical slice with 4 layers:
```
Layer 1: entities/     ← Pure Python domain objects (zero deps)
Layer 2: use_cases/    ← Business logic + abstract interfaces
Layer 3: adapters/     ← Controllers, Gateways, Pydantic schemas
Layer 4: drivers/      ← FastAPI routes, SQLAlchemy models, LangChain chains
```

## 🔥 Features

| Feature | Endpoint | Description |
|---------|----------|-------------|
| **Blog Generator** | `POST /api/v1/content/blog` | SEO-optimised blogs with meta tags, readability score |
| **Article Writer** | `POST /api/v1/content/article` | Long-form via 5-step LangGraph agent |
| **Social Media** | `POST /api/v1/content/social` | LinkedIn, Twitter/X, Instagram posts |
| **Ad Copy** | `POST /api/v1/content/ad-copy` | Google Ads (AIDA) + Facebook Ads (PAS) |
| **Product Description** | `POST /api/v1/content/product-description` | F-A-B framework ecommerce copy |
| **Email Writer** | `POST /api/v1/content/email` | Cold email, newsletter, follow-up, welcome |
| **Script Writer** | `POST /api/v1/content/script` | YouTube, Reels, Podcast scripts |
| **SEO Optimizer** | `POST /api/v1/seo/analyze` | Full SEO analysis + AI recommendations |
| **Meta Generator** | `POST /api/v1/seo/meta` | Meta title, description, slug generation |
| **Auth** | `POST /api/v1/auth/register` | JWT auth + API key management |

## ⚡ Quick Start

### Option A — Local (venv)
```bash
source venv/bin/activate
cp .env.example .env        # Add OPENAI_API_KEY
uvicorn app.main:app --reload
# → http://localhost:8000/docs
```

### Option B — Docker (Recommended)
```bash
cp .env.example .env        # Add OPENAI_API_KEY
docker compose up --build   # Starts app + PostgreSQL + Redis + Celery
# → http://localhost:8000/docs
# → http://localhost:5555    (Celery Flower monitor)
```

### Production Deploy
```bash
docker compose -f docker-compose.yml up -d   # No dev override
```

## 🛠️ Tech Stack

- **FastAPI** — Async web framework
- **LangChain** — LLM chains and prompt management
- **LangGraph** — Multi-step AI agents (article writer)
- **SQLAlchemy** (async) — ORM (SQLite dev / PostgreSQL prod)
- **python-jose** — JWT authentication
- **textstat** — Readability analysis (Flesch-Kincaid)
- **Pydantic Settings** — Config management

## 📂 Structure

```
app/
├── core/              # Shared kernel (entities, interfaces, exceptions)
├── infrastructure/    # DB, Redis, LLM factory, Celery
├── features/          # 9 feature modules (Clean Architecture per feature)
│   ├── auth/
│   ├── blog_generator/
│   ├── article_writer/
│   ├── social_media/
│   ├── ad_copy/
│   ├── product_description/
│   ├── email_writer/
│   ├── script_writer/
│   └── seo_optimizer/
└── main.py            # App factory, router registration

skill/                 # Master workflow guide
├── SKILL.md           # Architecture + conventions + rules
└── workflows/         # Step-by-step development workflows
```

## 📖 Docs

- **Swagger UI**: http://localhost:8000/docs
- **Architecture Guide**: `skill/SKILL.md`
- **Add a Feature**: `skill/workflows/02_add_feature.md`
- **Run Locally**: `skill/workflows/03_run_local.md`




docker compose --env-file .env.dev -f docker-compose.dev.yml up -d


docker compose --env-file .env.dev -f docker-compose.dev.yml down


docker compose --env-file .env.dev -f docker-compose.dev.yml up -d --build


docker compose --env-file .env.prod -f docker-compose.prod.yml up -d


docker compose --env-file .env.prod -f docker-compose.prod.yml down
