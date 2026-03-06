import asyncio
import pytest
import pytest_asyncio
from uuid import uuid4

from httpx import AsyncClient, ASGITransport

from api_blog_test_task.core.settings import load_settings
from api_blog_test_task.infrastructure.database import create_sa_engine, create_sa_session_factory
from api_blog_test_task.infrastructure.cache.client import create_cache_client
from api_blog_test_task.infrastructure.database.transactions_manager import TransactionManager
from api_blog_test_task.infrastructure.database.repositories.posts import PostsRepository
from api_blog_test_task.infrastructure.cache.repositories import PostsCacheRepository
from api_blog_test_task.application.services.mappers.posts import PostsServiceMapper
from api_blog_test_task.application.services.mappers.cache_posts import PostsCacheMapper
from api_blog_test_task.application.services.posts import PostsService
from api_blog_test_task.application.dto import CreatePostDTO
from api_blog_test_task.presentation import init_app
from api_blog_test_task.presentation.v1 import init_app_v1
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def settings():
    return load_settings()


@pytest_asyncio.fixture(scope="function")
async def redis_client(settings):
    client = create_cache_client(settings.infrastructure.cache.url)
    yield client
    await client.flushdb()
    await client.aclose()


@pytest_asyncio.fixture(scope="function")
async def db_session(settings):
    engine = create_sa_engine(settings.infrastructure.database.url_obj)
    session_factory = create_sa_session_factory(engine)
    session = session_factory()

    yield session

    await session.close()
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def transaction_manager(db_session):
    return TransactionManager(db_session)


@pytest_asyncio.fixture(scope="function")
async def posts_repository(db_session):
    return PostsRepository(db_session)


@pytest_asyncio.fixture(scope="function")
async def cache_repository(redis_client, settings):
    return PostsCacheRepository(
        redis_client,
        settings.infrastructure.cache.post_ttl,
        settings.infrastructure.cache.hits_ttl
    )


@pytest.fixture(scope="function")
def service_mapper():
    return PostsServiceMapper()


@pytest.fixture(scope="function")
def cache_mapper():
    return PostsCacheMapper()


@pytest_asyncio.fixture(scope="function")
async def posts_service(
    posts_repository,
    cache_repository,
    service_mapper,
    cache_mapper,
    transaction_manager,
    settings,
):
    return PostsService(
        repository=posts_repository,
        cache=cache_repository,
        cache_mapper=cache_mapper,
        mapper=service_mapper,
        transaction_manager=transaction_manager,
        hits_threshold=settings.infrastructure.cache.hits_threshold,
    )


@pytest.fixture(scope="function")
def create_post_dto():
    return CreatePostDTO(
        title="Test Post",
        content="Test Content"
    )


@pytest.fixture(scope="function")
def post_id():
    return uuid4()


@pytest_asyncio.fixture(scope="function")
async def app(settings):
    app = init_app(
        init_app_v1(settings.presentation.v1_api)
    )

    from api_blog_test_task.application.di_providers import MappersServiceProvider
    from api_blog_test_task.application.di_providers.services import PostsServiceProvider
    from api_blog_test_task.infrastructure.di_providers import (
        DatabaseProvider,
        MappersProvider,
        DBRepositoriesProvider,
        CacheProvider,
        CacheRepositoriesProvider,
    )

    container = make_async_container(
        DatabaseProvider(settings.infrastructure.database),
        MappersProvider(),
        DBRepositoriesProvider(),
        PostsServiceProvider(hits_threshold=settings.infrastructure.cache.hits_threshold),
        CacheProvider(settings.infrastructure.cache),
        CacheRepositoriesProvider(settings.infrastructure.cache),
        MappersServiceProvider()
    )

    setup_dishka(container=container, app=app)

    yield app

    await container.close()


@pytest_asyncio.fixture(scope="function")
async def client(app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
