import logging

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from .settings import Settings
from api_blog_test_task.application.di_providers import MappersServiceProvider
from api_blog_test_task.application.di_providers.services import PostsServiceProvider
from api_blog_test_task.infrastructure.di_providers import (
    DatabaseProvider,
    MappersProvider,
    DBRepositoriesProvider,
    CacheProvider
)

log = logging.getLogger(__name__)


def setup_dependencies(
        app: FastAPI,
        settings: Settings,
) -> None:
    log.info("Setting up dependencies.")
    container = make_async_container(
        DatabaseProvider(settings.infrastructure.database),
        MappersProvider(),
        DBRepositoriesProvider(),
        PostsServiceProvider(),
        CacheProvider(settings.infrastructure.cache),
        MappersServiceProvider()
    )

    setup_dishka(container=container, app=app)
