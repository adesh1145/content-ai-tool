# Workflow: Add a New Content Generation Feature
---
description: Step-by-step guide to add a new feature following Clean Architecture
---

## Example: Adding a "Press Release Writer" feature

### Step 1: Create directory structure
```bash
mkdir -p app/features/press_release/{entities,use_cases/interfaces,adapters,drivers/ai}
touch app/features/press_release/__init__.py
touch app/features/press_release/entities/__init__.py
touch app/features/press_release/use_cases/__init__.py
touch app/features/press_release/use_cases/interfaces/__init__.py
touch app/features/press_release/adapters/__init__.py
touch app/features/press_release/drivers/__init__.py
touch app/features/press_release/drivers/ai/__init__.py
```

### Step 2: Create the Entity (Layer 1 — zero deps)
File: `app/features/press_release/entities/press_release.py`
```python
from dataclasses import dataclass
from app.core.entities.base_entity import BaseEntity

@dataclass
class PressRelease(BaseEntity):
    user_id: str = ""
    headline: str = ""
    sub_headline: str = ""
    body: str = ""
    quote: str = ""
    boilerplate: str = ""
```

### Step 3: Create the Repository Interface (Layer 2)
File: `app/features/press_release/use_cases/interfaces/press_release_repo.py`
```python
from abc import abstractmethod
from app.core.interfaces.base_repository import IRepository
from app.features.press_release.entities.press_release import PressRelease

class IPressReleaseRepository(IRepository[PressRelease]):
    @abstractmethod
    async def list_by_user(self, user_id: str) -> list[PressRelease]: ...
```

### Step 4: Create the AI Service Interface (Layer 2)
File: `app/features/press_release/use_cases/interfaces/press_release_ai.py`
```python
from abc import ABC, abstractmethod

class IPressReleaseAIService(ABC):
    @abstractmethod
    async def generate(self, topic: str, ...) -> dict: ...
```

### Step 5: Create the Use Case (Layer 2)
File: `app/features/press_release/use_cases/generate_press_release.py`
```python
from app.core.interfaces.base_use_case import IUseCase
# ... implement GeneratePressReleaseUseCase
```

### Step 6: Create Pydantic Schemas (Layer 3)
File: `app/features/press_release/adapters/schemas.py`

### Step 7: Create SQLAlchemy Model (Layer 4)
File: `app/features/press_release/drivers/models.py`

### Step 8: Create LangChain Chain (Layer 4)
File: `app/features/press_release/drivers/ai/press_release_chain.py`

### Step 9: Create FastAPI Routes (Layer 4)
File: `app/features/press_release/drivers/routes.py`
```python
router = APIRouter(prefix="/content/press-release", tags=["Press Release"])
```

### Step 10: Register router in app/main.py
```python
from app.features.press_release.drivers.routes import router as pr_router
app.include_router(pr_router, prefix=prefix)
```

### Step 11: Write unit tests
File: `tests/unit/features/test_press_release.py`

## ✅ Checklist
- [ ] entities/ created — pure Python, no external imports
- [ ] use_cases/interfaces/ created — abstract classes (ABC)
- [ ] use_case created — no SQLAlchemy, no FastAPI, no LangChain
- [ ] adapters/schemas.py created — Pydantic DTOs
- [ ] adapters/<name>_gateway.py created — SQLAlchemy impl
- [ ] drivers/models.py created — inherits from Base
- [ ] drivers/ai/<name>_chain.py created — LangChain or LangGraph
- [ ] drivers/routes.py created — FastAPI router
- [ ] Router registered in app/main.py
- [ ] Unit tests written
