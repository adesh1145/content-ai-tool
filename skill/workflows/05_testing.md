# Workflow: Writing and Running Tests
---
description: How to write unit and integration tests
---

## Test Architecture

```
tests/
├── conftest.py              # Shared fixtures (async client, test DB)
├── unit/features/           # No DB, no HTTP — mock everything external
└── integration/api/         # Real HTTP calls, test SQLite DB
```

## Run All Tests
```bash
pytest tests/ -v
```

## Run with Coverage
```bash
pytest tests/ --cov=app --cov-report=html
# Open htmlcov/index.html for browser report
```

## Unit Test Pattern (Mock interfaces)
```python
# tests/unit/features/test_blog_generator.py
import pytest
from unittest.mock import AsyncMock
from app.features.blog_generator.use_cases.generate_blog import (
    GenerateBlogUseCase, GenerateBlogInput
)
from app.features.blog_generator.entities.blog_content import SEOMetadata

@pytest.mark.asyncio
async def test_generate_blog_success():
    # Arrange: mock the interfaces
    mock_repo = AsyncMock()
    mock_repo.save.return_value = ...  # Return mock entity
    
    mock_ai = AsyncMock()
    mock_ai.generate.return_value = BlogGenerationResult(
        title="Test Title", outline=["Intro", "Main"], body="Content...",
        seo=SEOMetadata(meta_title="Test", meta_description="Desc", slug="test"),
        tokens_used=100
    )
    
    # Act
    use_case = GenerateBlogUseCase(blog_repo=mock_repo, blog_ai=mock_ai)
    result = await use_case.execute(GenerateBlogInput(
        user_id="user-1", topic="Python programming basics", word_count=800
    ))
    
    # Assert
    assert result.status == "completed"
    assert mock_ai.generate.called
```

## Integration Test Pattern
```python
# tests/integration/api/test_blog_api.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

## conftest.py Setup
```python
# tests/conftest.py
import pytest
import pytest_asyncio
from httpx import AsyncClient
from app.main import app

@pytest_asyncio.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c
```
