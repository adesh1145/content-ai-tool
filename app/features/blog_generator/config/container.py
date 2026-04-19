"""
Dependency container for the Blog Generator V2 feature.

Wires together domain, application, and adapter layers following
the Dependency Inversion Principle: use cases depend on abstractions
(ports) that are satisfied by concrete adapters assembled here.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

# Outbound Ports
from app.common.port.outbound.event_publisher_port import EventPublisherPort
from app.features.blog_generator.domain.port.outbound.blog_ai_port import IBlogAIService
from app.features.blog_generator.domain.port.outbound.blog_repository_port import IBlogRepository

# Inbound Ports (Use Cases)
from app.common.port.inbound.use_case import UseCase
from app.features.blog_generator.application.port.inbound.generate_blog_port import IGenerateBlog

# Commands, Queries, Results (for generic UseCase typing)
from app.features.blog_generator.application.query.get_blog_query import GetBlogQuery
from app.features.blog_generator.application.query.list_blogs_query import ListBlogsQuery
from app.features.blog_generator.application.result.blog_result import BlogResult

# Concrete Implementations (Adapters & Application Services)
from app.features.blog_generator.infrastructure.ai.service import BlogAIService
from app.features.blog_generator.infrastructure.messaging.publisher import BlogEventPublisher
from app.features.blog_generator.infrastructure.persistence.repository import SQLAlchemyBlogRepository
from app.features.blog_generator.application.service.generate_blog_service import GenerateBlogService
from app.features.blog_generator.application.service.get_blog_service import GetBlogService
from app.features.blog_generator.application.service.list_blogs_service import ListBlogsService


class BlogContainer:
    """Factory that assembles all blog feature dependencies."""

    @staticmethod
    def blog_repository(db: AsyncSession) -> IBlogRepository:
        return SQLAlchemyBlogRepository(db)

    @staticmethod
    def blog_ai_service() -> IBlogAIService:
        return BlogAIService()

    @staticmethod
    def event_publisher() -> EventPublisherPort:
        return BlogEventPublisher()

    @staticmethod
    def generate_blog_service(db: AsyncSession) -> IGenerateBlog:
        return GenerateBlogService(
            blog_repo=BlogContainer.blog_repository(db),
            blog_ai=BlogContainer.blog_ai_service(),
            event_publisher=BlogContainer.event_publisher(),
        )

    @staticmethod
    def get_blog_service(db: AsyncSession) -> UseCase[GetBlogQuery, BlogResult]:
        return GetBlogService(blog_repo=BlogContainer.blog_repository(db))

    @staticmethod
    def list_blogs_service(db: AsyncSession) -> UseCase[ListBlogsQuery, list[BlogResult]]:
        return ListBlogsService(blog_repo=BlogContainer.blog_repository(db))
