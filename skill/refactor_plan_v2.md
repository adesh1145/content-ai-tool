# Refactor Plan v2: Spring Boot Enterprise Pattern → Python/FastAPI

## Problem Statement

The current codebase has **two architectures living side-by-side** (legacy 4-layer + a first hex attempt) and the hex attempt doesn't follow the canonical Spring Boot enterprise pattern. Key structural misalignments:

| Aspect | Spring Boot Reference | Current Python Codebase | Issue |
|--------|----------------------|------------------------|-------|
| Ports location | `domain/port/{in,out}/` | `application/port/{input,output}/` | Ports belong in domain, not application |
| Domain model structure | `domain/model/` (flat — aggregates, entities, VOs together) | `domain/aggregate/`, `domain/entity/`, `domain/value_object/` (split) | Over-fragmented |
| Application services | `application/service/XxxService.java` implements `port.in` | `application/usecase/xxx_usecase.py` | Naming + no port impl |
| CQRS DTOs | `application/command/`, `query/`, `result/` (flat) | `application/dto/command/`, `dto/query/`, `dto/response/` (nested under dto/) | Extra nesting |
| Adapter naming | `adapter/in/web/`, `adapter/out/persistence/` | `adapter/input/api/`, `adapter/output/persistence/` | Different naming |
| Web adapter | `adapter/in/web/dto/`, `adapter/in/web/mapper/` | `adapter/input/api/schemas.py` (single file) | Missing mapper, flat schemas |
| Persistence adapter | `adapter/out/persistence/entity/`, `repository/`, mapper/, adapter | `adapter/output/persistence/` (flat) | Missing entity/repository sub-structure |
| Shared kernel | `common/{config,exception,logging,observability,util}` | `core/{domain,application,entities,interfaces,port,...}` | Too many core sub-packages |
| Feature config | DI via Spring IoC | `config/dependency_container.py` per feature | Acceptable (Python has no IoC) |
| Legacy files | N/A | `drivers/`, `adapters/`, `entities/`, `use_cases/` still exist | Must be removed |

---

## Target Architecture

### Python-Specific Adaptations

- `in` is a Python keyword → use `inbound/` and `outbound/` for both ports and adapters
- No IoC container in Python → keep `config/` per feature with FastAPI `Depends()` wiring
- `controller` → `controller.py` (FastAPI router, but named "controller" to match enterprise pattern)

---

### Shared Kernel: `app/common/`

Replaces current `app/core/`. Follows Spring Boot's `common/` pattern.

```
app/common/
├── __init__.py
├── config/
│   ├── __init__.py
│   ├── settings.py              # [MOVE] from app/config.py — pydantic Settings
│   ├── security_config.py       # [NEW] JWT config, password hashing config
│   └── openapi_config.py        # [NEW] FastAPI app metadata
│
├── exception/
│   ├── __init__.py
│   ├── api_exception.py         # [RENAME] base DomainException
│   ├── not_found.py
│   ├── validation_error.py
│   ├── authentication_error.py
│   ├── authorization_error.py
│   ├── quota_exceeded.py
│   ├── llm_provider_error.py
│   ├── duplicate_error.py
│   └── global_exception_handler.py  # [MERGE] FastAPI exception handlers
│
├── domain/
│   ├── __init__.py
│   ├── aggregate_root.py        # [KEEP] Base AggregateRoot
│   ├── base_entity.py           # [KEEP] Base entity
│   ├── domain_event.py          # [KEEP] Base DomainEvent
│   ├── domain_service.py        # [KEEP] Base DomainService marker
│   └── value_objects.py         # [KEEP] Shared enums (Tone, Language, etc.)
│
├── application/
│   ├── __init__.py
│   ├── use_case.py              # [KEEP] IUseCase / BaseUseCase
│   ├── command.py               # [KEEP] BaseCommand
│   ├── query.py                 # [KEEP] BaseQuery
│   └── unit_of_work.py          # [KEEP] IUnitOfWork
│
├── port/
│   ├── __init__.py
│   ├── repository_port.py       # [KEEP] Generic IRepository[T]
│   ├── llm_port.py              # [KEEP] ILLMProvider
│   ├── event_publisher_port.py  # [KEEP] IEventPublisher
│   └── cache_port.py            # [KEEP] ICachePort
│
├── logging/
│   ├── __init__.py
│   └── logger.py                # [KEEP] Loguru setup
│
├── middleware/
│   ├── __init__.py
│   ├── cors.py
│   ├── request_logging.py
│   └── request_id.py
│
├── response/
│   ├── __init__.py
│   └── api_response.py          # [KEEP] APIResponse, PagedResponse
│
└── router/
    ├── __init__.py
    └── registry.py              # [KEEP] Centralized router registration
```

**Key change:** Rename `core/` → `common/`. Flatten sub-packages (e.g., `application/base_use_case.py` → `application/use_case.py`).

---

### Infrastructure: `app/infrastructure/` (unchanged)

```
app/infrastructure/
├── __init__.py
├── ai/
│   ├── __init__.py
│   ├── llm_registry.py
│   ├── model_config.py
│   └── providers/
│       ├── __init__.py
│       ├── openai_provider.py
│       ├── anthropic_provider.py
│       ├── google_provider.py
│       ├── huggingface_provider.py
│       └── ollama_provider.py
├── db/
│   ├── __init__.py
│   ├── base_model.py
│   ├── connection.py
│   └── unit_of_work.py
├── cache/
│   ├── __init__.py
│   └── redis_cache.py
├── celery/
│   ├── __init__.py
│   └── worker.py
└── messaging/
    ├── __init__.py
    └── in_memory_event_bus.py
```

---

### Bounded Context (Feature) Pattern

Every feature follows this **exact** structure. Example: `auth` (identity context)

```
app/features/auth/                          # bounded context
├── __init__.py
│
├── domain/                                 # INNERMOST — zero infra deps
│   ├── __init__.py
│   ├── model/                              # ALL domain objects in one folder
│   │   ├── __init__.py
│   │   ├── user.py                         # aggregate root
│   │   ├── user_id.py                      # strong-typed ID value object
│   │   ├── api_key.py                      # child entity
│   │   ├── email.py                        # value object
│   │   ├── hashed_password.py              # value object
│   │   └── user_plan.py                    # enum value object
│   ├── event/
│   │   ├── __init__.py
│   │   ├── user_registered.py              # domain event (past tense, no "Event" suffix)
│   │   ├── user_logged_in.py
│   │   └── api_key_created.py
│   ├── service/
│   │   ├── __init__.py
│   │   └── password_service.py             # pure domain service
│   └── port/                               # ⭐ PORTS LIVE IN DOMAIN
│       ├── __init__.py
│       ├── inbound/                        # driving ports (use case interfaces)
│       │   ├── __init__.py
│       │   ├── register_user_use_case.py   # ABC interface
│       │   ├── login_user_use_case.py
│       │   └── refresh_token_use_case.py
│       └── outbound/                       # driven ports (repo, gateway ABCs)
│           ├── __init__.py
│           ├── user_repository.py          # ABC
│           ├── token_service.py            # ABC
│           └── auth_event_publisher.py     # ABC
│
├── application/                            # ORCHESTRATION — depends only on domain
│   ├── __init__.py
│   ├── command/                            # CQRS commands (flat, no dto/ wrapper)
│   │   ├── __init__.py
│   │   ├── register_user_command.py
│   │   └── login_user_command.py
│   ├── query/                              # CQRS queries
│   │   ├── __init__.py
│   │   └── get_user_query.py
│   ├── result/                             # Result DTOs (not "response")
│   │   ├── __init__.py
│   │   ├── user_result.py
│   │   └── token_result.py
│   └── service/                            # ⭐ Services implement port.inbound
│       ├── __init__.py
│       ├── register_user_service.py        # implements RegisterUserUseCase
│       ├── login_user_service.py           # implements LoginUserUseCase
│       └── refresh_token_service.py        # implements RefreshTokenUseCase
│
├── adapter/                                # OUTERMOST — infra deps allowed
│   ├── __init__.py
│   ├── inbound/                            # driving adapters
│   │   ├── __init__.py
│   │   └── web/                            # ⭐ "web" not "api"
│   │       ├── __init__.py
│   │       ├── auth_controller.py          # ⭐ "controller" not "router"
│   │       ├── dto/                        # web-specific request/response
│   │       │   ├── __init__.py
│   │       │   ├── register_request.py
│   │       │   ├── login_request.py
│   │       │   ├── token_response.py
│   │       │   └── user_profile_response.py
│   │       └── mapper/                     # web DTO ↔ command/result mapper
│   │           ├── __init__.py
│   │           └── auth_web_mapper.py
│   └── outbound/                           # driven adapters
│       ├── __init__.py
│       ├── persistence/
│       │   ├── __init__.py
│       │   ├── entity/                     # ⭐ ORM entities in own folder
│       │   │   ├── __init__.py
│       │   │   ├── user_sa_entity.py       # SQLAlchemy model ("sa" = SQLAlchemy)
│       │   │   └── api_key_sa_entity.py
│       │   ├── repository/                 # ⭐ ORM repos in own folder
│       │   │   ├── __init__.py
│       │   │   └── user_sa_repository.py   # Raw SQLAlchemy queries
│       │   ├── user_persistence_adapter.py # ⭐ Implements port.outbound.UserRepository
│       │   └── mapper/
│       │       ├── __init__.py
│       │       └── user_persistence_mapper.py  # ORM entity ↔ domain model
│       ├── security/
│       │   ├── __init__.py
│       │   └── jwt_token_adapter.py        # Implements port.outbound.TokenService
│       └── messaging/
│           ├── __init__.py
│           └── auth_event_publisher_adapter.py  # Implements port.outbound.AuthEventPublisher
│
└── config/                                 # DI wiring (Python-specific, replaces Spring IoC)
    ├── __init__.py
    └── auth_container.py
```

---

### All 9 Content Features — Same Pattern

Each bounded context follows the identical 3-layer structure:

| Bounded Context | Aggregate Root | Inbound Ports | Outbound Ports |
|----------------|---------------|---------------|----------------|
| `auth` | `User` | RegisterUser, LoginUser, RefreshToken | UserRepository, TokenService, AuthEventPublisher |
| `blog_generator` | `BlogContent` | GenerateBlog, GetBlog, ListBlogs | BlogRepository, BlogAIGateway, BlogEventPublisher |
| `article_writer` | `Article` | GenerateArticle, GetArticle | ArticleRepository, ArticleAIGateway, ArticleEventPublisher |
| `social_media` | `SocialPost` | GenerateSocialPost, ListSocialPosts | SocialPostRepository, SocialAIGateway |
| `ad_copy` | `Ad` | GenerateAdCopy | AdRepository, AdAIGateway |
| `product_description` | `ProductDescription` | GenerateProductDesc | ProductRepository, ProductAIGateway |
| `email_writer` | `Email` | GenerateEmail | EmailRepository, EmailAIGateway |
| `script_writer` | `Script` | GenerateScript | ScriptRepository, ScriptAIGateway |
| `seo_optimizer` | `SEOAnalysis` | AnalyzeSEO, GenerateMeta | SEORepository, SEOAIGateway |

---

## Structural Diff: What Changes

### Moves/Renames

| Current Path | Target Path | Action |
|-------------|-------------|--------|
| `app/core/` | `app/common/` | RENAME entire directory |
| `app/config.py` | `app/common/config/settings.py` | MOVE |
| `app/core/entities/base_entity.py` | `app/common/domain/base_entity.py` | MOVE |
| `app/core/entities/value_objects.py` | `app/common/domain/value_objects.py` | MOVE |
| `app/core/domain/aggregate_root.py` | `app/common/domain/aggregate_root.py` | MOVE |
| `app/core/domain/domain_event.py` | `app/common/domain/domain_event.py` | MOVE |
| `app/core/application/base_use_case.py` | `app/common/application/use_case.py` | MOVE+RENAME |
| `app/core/application/base_command.py` | `app/common/application/command.py` | MOVE+RENAME |
| `app/core/application/base_query.py` | `app/common/application/query.py` | MOVE+RENAME |
| `app/core/port/output/repository_port.py` | `app/common/port/repository_port.py` | MOVE (flatten) |
| `app/core/port/output/llm_port.py` | `app/common/port/llm_port.py` | MOVE (flatten) |
| `app/core/exception/*.py` | `app/common/exception/*.py` | MOVE |
| `app/core/exception_handler/fastapi_handlers.py` | `app/common/exception/global_exception_handler.py` | MOVE+RENAME |
| `app/core/middleware/*.py` | `app/common/middleware/*.py` | MOVE |
| `app/core/utils/logger.py` | `app/common/logging/logger.py` | MOVE |
| `app/core/response/api_response.py` | `app/common/response/api_response.py` | MOVE |
| `app/core/router/registry.py` | `app/common/router/registry.py` | MOVE |

### Per-Feature Restructuring

For **each** of the 9 features, the following structural changes apply:

| Current | Target | Change |
|---------|--------|--------|
| `domain/aggregate/` | `domain/model/` | RENAME — aggregates, entities, VOs all go in `model/` |
| `domain/entity/` | `domain/model/` | MERGE into `model/` |
| `domain/value_object/` | `domain/model/` | MERGE into `model/` |
| `domain/factory/` | `domain/model/` or `domain/service/` | MERGE — factory is either in model or service |
| `domain/repository/` | `domain/port/outbound/` | MOVE — repo interface is an outbound port |
| `domain/exception/` | `domain/model/` or `app/common/exception/` | MERGE (feature exceptions can stay or move to common) |
| `application/port/input/` | `domain/port/inbound/` | MOVE — inbound ports belong in domain |
| `application/port/output/` | `domain/port/outbound/` | MOVE — outbound ports belong in domain |
| `application/usecase/` | `application/service/` | RENAME — services implement inbound ports |
| `application/dto/command/` | `application/command/` | FLATTEN — remove `dto/` wrapper |
| `application/dto/query/` | `application/query/` | FLATTEN |
| `application/dto/response/` | `application/result/` | FLATTEN + RENAME |
| `adapter/input/api/` | `adapter/inbound/web/` | RENAME — `input`→`inbound`, `api`→`web` |
| `adapter/input/api/xxx_schemas.py` | `adapter/inbound/web/dto/*.py` | SPLIT — one file per DTO |
| `adapter/input/api/xxx_router.py` | `adapter/inbound/web/xxx_controller.py` | RENAME — router → controller |
| (none) | `adapter/inbound/web/mapper/` | NEW — web mapper |
| `adapter/output/persistence/xxx_model.py` | `adapter/outbound/persistence/entity/xxx_sa_entity.py` | RENAME + MOVE |
| `adapter/output/persistence/xxx_repository_impl.py` | `adapter/outbound/persistence/repository/xxx_sa_repository.py` | RENAME + MOVE |
| (implicit) | `adapter/outbound/persistence/xxx_persistence_adapter.py` | NEW — adapter implementing port.outbound |
| `adapter/output/persistence/xxx_orm_mapper.py` | `adapter/outbound/persistence/mapper/xxx_persistence_mapper.py` | RENAME + MOVE |
| `adapter/output/ai/` | `adapter/outbound/ai/` | RENAME |
| `adapter/output/messaging/` | `adapter/outbound/messaging/` | RENAME |

### Deletions

All legacy files (the original 4-layer architecture) must be **deleted**:

- `app/features/*/drivers/` — old routes, models, AI chains
- `app/features/*/adapters/` — old schemas, gateways
- `app/features/*/entities/` — old domain entities
- `app/features/*/use_cases/` — old use cases + interfaces
- `app/core/entities/` — replaced by `app/common/domain/`
- `app/core/interfaces/` — replaced by `app/common/port/`
- `app/core/exceptions.py` — replaced by `app/common/exception/`
- `app/core/response.py` — replaced by `app/common/response/`
- `app/infrastructure/ai/llm_factory.py` — replaced by registry
- `app/infrastructure/ai/llm_factodry.py` — typo shim

---

## Dependency Rule (Enterprise Grade)

```
  ┌─────────────────────────────┐
  │         domain/             │  INNERMOST: pure Python, zero deps
  │  model/ event/ service/    │  - AggregateRoot, Value Objects
  │         port/              │  - Port interfaces (ABCs)
  │    inbound/  outbound/     │
  └─────────┬───────────────────┘
            │ depends on
  ┌─────────▼───────────────────┐
  │       application/          │  MIDDLE: orchestration only
  │  command/ query/ result/   │  - Implements port.inbound
  │         service/           │  - Depends on domain, never adapter
  └─────────┬───────────────────┘
            │ depends on
  ┌─────────▼───────────────────┐
  │        adapter/             │  OUTERMOST: infra deps
  │  inbound/   outbound/      │  - Implements port.outbound
  │  web/ messaging/           │  - SQLAlchemy, LangChain, JWT, etc.
  │  persistence/ ai/         │
  └─────────────────────────────┘
```

**Enforced rule:** domain/ NEVER imports from application/ or adapter/. application/ NEVER imports from adapter/.

---

## Execution Plan

### Phase 1: Shared Kernel (`common/`)
- Create `app/common/` with the new structure
- Move and rename all files from `app/core/`
- Update `app/main.py`, `app/dependencies.py` to import from `app.common.*`
- Add backward-compat shims in `app/core/` (temporary)
- **Est: ~30 files**

### Phase 2: Reference Implementation — `auth`
- Rebuild `app/features/auth/` with the exact Spring Boot pattern
- Domain: `model/`, `event/`, `service/`, `port/{inbound,outbound}/`
- Application: `command/`, `query/`, `result/`, `service/`
- Adapter: `inbound/web/{controller,dto/,mapper/}`, `outbound/{persistence/{entity/,repository/,adapter,mapper/},security/,messaging/}`
- Delete old auth files (`drivers/`, `adapters/`, `entities/`, `use_cases/`)
- Delete current hex attempt (`adapter/`, `domain/`, `application/`, `config/`)
- Validate: all routes work, imports clean
- **Est: ~50 files**

### Phase 3: Reference Implementation — `blog_generator`
- Same pattern as auth but for content generation
- Includes AI gateway port + adapter
- **Est: ~50 files**

### Phase 4: Remaining 7 features
- `article_writer`, `social_media`, `ad_copy`, `product_description`, `email_writer`, `script_writer`, `seo_optimizer`
- Each follows the identical pattern
- Can be parallelized
- **Est: ~250 files**

### Phase 5: Cleanup
- Delete ALL `app/core/` backward-compat shims
- Delete `app/core/` entirely
- Delete `app/config.py` (moved to `app/common/config/settings.py`)
- Update `app/main.py` to final form
- Update `app/dependencies.py` to final form
- Update `app/infrastructure/` imports to use `app.common.*`
- **Est: ~20 files modified**

### Phase 6: Verification
- Syntax check all files
- Static import resolution
- No circular imports
- All routes match original API contract
- App loads successfully

---

## File Count Estimate

| Phase | New/Modified | Deleted | Net |
|-------|-------------|---------|-----|
| 1. Common | ~30 | 0 | +30 |
| 2. Auth | ~50 | ~65 (old hex) + ~15 (legacy) | -30 |
| 3. Blog | ~50 | ~62 (old hex) + ~10 (legacy) | -22 |
| 4. 7 Features | ~250 | ~350 (old hex) + ~70 (legacy) | -170 |
| 5. Cleanup | ~10 | ~50 (core/ shims) | -40 |
| **Total** | **~390 new** | **~620 deleted** | **~390 final** |

---

## Open Questions for Review

1. **Naming:** `inbound/outbound` vs `in_/out` for the Python-safe port/adapter directories?
2. **Controller vs Router:** Should we call them `xxx_controller.py` (Spring pattern) or `xxx_router.py` (FastAPI convention)?
3. **Skeleton features:** `project_manager`, `template_engine`, `usage_tracker` — include in refactor or skip?
4. **Test structure:** Should we create matching test directories (`tests/features/auth/domain/`, `tests/features/auth/application/`, etc.)?
5. **Alembic migrations:** Generate new migration for any new/renamed tables?

---

## Example: Import Chain After Refactor

```python
# Controller (adapter/inbound/web/)
from app.features.auth.domain.port.inbound.register_user_use_case import IRegisterUserUseCase
from app.features.auth.application.command.register_user_command import RegisterUserCommand
from app.features.auth.adapter.inbound.web.dto.register_request import RegisterRequest
from app.features.auth.adapter.inbound.web.mapper.auth_web_mapper import AuthWebMapper
from app.features.auth.config.auth_container import AuthContainer

# Application Service (application/service/)
from app.features.auth.domain.port.inbound.register_user_use_case import IRegisterUserUseCase
from app.features.auth.domain.port.outbound.user_repository import IUserRepository
from app.features.auth.domain.port.outbound.auth_event_publisher import IAuthEventPublisher
from app.features.auth.domain.model.user import User
from app.features.auth.domain.service.password_service import PasswordService
from app.features.auth.application.command.register_user_command import RegisterUserCommand
from app.features.auth.application.result.user_result import UserResult

# Persistence Adapter (adapter/outbound/persistence/)
from app.features.auth.domain.port.outbound.user_repository import IUserRepository
from app.features.auth.domain.model.user import User
from app.features.auth.adapter.outbound.persistence.entity.user_sa_entity import UserSAEntity
from app.features.auth.adapter.outbound.persistence.mapper.user_persistence_mapper import UserPersistenceMapper
```

Notice: **domain imports from domain only**. **Application imports from domain only**. **Adapter imports from both** (and infra).
