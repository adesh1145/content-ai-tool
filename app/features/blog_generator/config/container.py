"""
Dependency container for the Blog Generator V2 feature.

Wires together domain, application, and adapter layers following
the Dependency Inversion Principle: use cases depend on abstractions
(ports) that are satisfied by concrete adapters assembled here.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.features.blog_generator.adapter.outbound.ai.service import BlogAIService
from app.features.blog_generator.adapter.outbound.messaging.publisher import BlogEventPublisher
from app.features.blog_generator.adapter.outbound.persistence.repository import SQLAlchemyBlogRepository
from app.features.blog_generator.application.service.generate_blog_service import GenerateBlogService
from app.features.blog_generator.application.service.get_blog_service import GetBlogService
from app.features.blog_generator.application.service.list_blogs_service import ListBlogsService


class BlogContainer:
    """Factory that assembles all blog feature dependencies."""

    @staticmethod
    def blog_repository(db: AsyncSession) -> SQLAlchemyBlogRepository:
        return SQLAlchemyBlogRepository(db)

    @staticmethod
    def blog_ai_service() -> BlogAIService:
        return BlogAIService()

    @staticmethod
    def event_publisher() -> BlogEventPublisher:
        return BlogEventPublisher()

    @staticmethod
    def generate_blog_service(db: AsyncSession) -> GenerateBlogService:
        return GenerateBlogService(
            blog_repo=BlogContainer.blog_repository(db),
            blog_ai=BlogContainer.blog_ai_service(),
            event_publisher=BlogContainer.event_publisher(),
        )

    @staticmethod
    def get_blog_service(db: AsyncSession) -> GetBlogService:
        return GetBlogService(blog_repo=BlogContainer.blog_repository(db))

    @staticmethod
    def list_blogs_service(db: AsyncSession) -> ListBlogsService:
        return ListBlogsService(blog_repo=BlogContainer.blog_repository(db))
