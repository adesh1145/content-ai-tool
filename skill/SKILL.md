# Content AI Tool — Master Skill Guide
---
name: content-ai-tool-skill
description: >
  Master guide for the Content AI Tool backend. Covers architecture,
  conventions, workflows, and everything needed to work on this project
  correctly and consistently.
---

# 🧠 Content AI Tool — Skill & Workflow Master Guide

> **This is the single source of truth for how we build, extend, and run this project.**
> Read this BEFORE writing any code. Follow these rules STRICTLY.

---

## 🏛️ Architecture: Clean Architecture (Feature-First)

We use **Uncle Bob's Clean Architecture** applied **per feature**.

### The 4 Layers (inner → outer)

```
Layer 1: entities/          ← Domain objects. ZERO imports from outside.
Layer 2: use_cases/         ← Business logic. Imports only entities + interfaces.
Layer 3: adapters/          ← Controllers, Gateways (DB), Serializers (Pydantic schemas).
Layer 4: drivers/           ← FastAPI routes, SQLAlchemy models, LangChain/LangGraph chains.
```

### The Golden Rule (Dependency Rule)
> **Inner layers NEVER import from outer layers. EVER.**

- `entities/` → imports nothing (stdlib only)
- `use_cases/` → imports only `entities/` and abstract `interfaces/`
- `adapters/` → imports `use_cases/` and `entities/`
- `drivers/` → imports everything (FastAPI, SQLAlchemy, LangChain)

### The Dependency Inversion
Use cases depend on **interfaces** (abstract classes), not concrete implementations:
- `GenerateBlogUseCase` → depends on `IBlogRepository, IBlogAIService` (interfaces)
- `BlogGateway` implements `IBlogRepository` (SQLAlchemy — in adapters/)
- `BlogAIService` implements `IBlogAIService` (LangChain — in drivers/ai/)

---

## 📁 Feature Structure (Required for EVERY feature)

```
app/features/<feature_name>/
├── __init__.py
├── entities/
│   └── <entity>.py           # Layer 1: Pure Python dataclass
├── use_cases/
│   ├── interfaces/
│   │   └── <repo/service>.py  # Abstract interfaces (ABC)
│   └── <action>_use_case.py  # Layer 2: Business logic
├── adapters/
│   ├── schemas.py            # Layer 3: Pydantic request/response models
│   ├── <entity>_gateway.py   # SQLAlchemy repository implementation
│   └── controller.py         # (optional) maps HTTP data → use case input
└── drivers/
    ├── routes.py             # Layer 4: FastAPI router
    ├── models.py             # SQLAlchemy ORM model
    └── ai/
        └── <feature>_chain.py  # LangChain chain or LangGraph graph
```

---

## 🔧 SOLID Principles — How We Apply Them

| Principle | Rule in This Project |
|-----------|---------------------|
| **S** — SRP | One file = one responsibility. `RegisterUserUseCase` only registers. `LoginUserUseCase` only logs in. |
| **O** — OCP | Add new features by creating new files, NOT modifying existing. |
| **L** — LSP | All gateways are interchangeable via their interface. | 
| **I** — ISP | `IBlogRepository` only has blog methods. `IUserRepository` only has user methods. No fat interfaces. |
| **D** — DIP | Use cases import `IBlogAIService`, not `BlogAIService`. Injection happens in `routes.py`. |

---

## ⚙️ Tech Stack Reference

| Component | Tool/Library | Location |
|-----------|-------------|---------|
| Web Framework | FastAPI | `app/main.py` |
| LLM Orchestration | LangChain | `drivers/ai/*.py` |
| Multi-step Agents | LangGraph | `drivers/ai/*_graph.py` |
| LLM Provider | OpenAI / Anthropic | `infrastructure/ai/llm_factory.py` |
| Database | SQLite (dev) / PostgreSQL (prod) | `infrastructure/db/` |
| ORM | SQLAlchemy (async) | `drivers/models.py` (per feature) |
| Auth | JWT (python-jose) + bcrypt | `features/auth/` |
| Config | Pydantic Settings | `app/config.py` |
| Logging | Loguru | `core/utils/logger.py` |
| SEO Analysis | textstat + LangChain | `features/seo_optimizer/` |
| Task Queue | Celery + Redis | `infrastructure/celery/worker.py` |

---

## 📂 Files for Workflows

See `skill/workflows/` for step-by-step guides:

| Workflow | File | When to Use |
|----------|------|-------------|
| Project Setup | `01_setup.md` | First time clone/setup |
| Add New Feature | `02_add_feature.md` | Adding a new content type |
| Run Locally | `03_run_local.md` | Day-to-day development |
| DB Migrations | `04_migrations.md` | Schema changes |
| Testing | `05_testing.md` | Writing and running tests |
| Add LLM Chain | `06_add_llm_chain.md` | New AI generation chain |

---

## 🚨 Rules — NEVER Break These

1. **Never import SQLAlchemy in use_cases/ or entities/**
2. **Never import FastAPI in use_cases/ or entities/**
3. **Never import LangChain directly in use_cases/** — use `IBlogAIService` interface
4. **Every new feature must have its own `IBlogRepository`-style interface** in `use_cases/interfaces/`
5. **All API responses must use `APIResponse[T]`** from `app/core/response.py`
6. **All exceptions from use cases must be domain exceptions** from `app/core/exceptions.py`
7. **Never hardcode API keys** — always use `get_settings().OPENAI_API_KEY`
8. **Every new DB model must inherit from `Base`** in `infrastructure/db/base_model.py`

---

## 🌊 Data Flow Example (Blog Generation)

```
POST /api/v1/content/blog
    │
    ▼
[routes.py]           Layer 4: Receives HTTP request, calls use case
    │ BlogGenerateRequest (Pydantic)
    ▼
[GenerateBlogUseCase] Layer 2: Validates, creates entity, calls services
    │ IBlogRepository.save(blog)
    │ IBlogAIService.generate(request)
    ▼
[BlogGateway]         Layer 3: SQLAlchemy → saves BlogContentModel to DB
[BlogAIService]       Layer 3: LangChain blog_chain.py → calls OpenAI
    │
    ▼
[BlogGenerateResponse] Layer 4: Serialized as APIResponse[BlogGenerateResponse]
```

---

## 🔑 Environment Variables Quick Reference

```bash
LLM_PROVIDER=openai              # Switch: openai | anthropic
OPENAI_API_KEY=sk-...            # Your OpenAI key
DATABASE_URL=sqlite+aiosqlite:///./content_tool.db  # Dev DB
SECRET_KEY=your-32-char-secret   # JWT secret
```
