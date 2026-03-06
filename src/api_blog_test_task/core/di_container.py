import logging

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from .settings import Settings
from api_blog_test_task.infrastructure.di_providers import (
    DatabaseProvider,
    MappersProvider,
    RepositoriesProvider
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
        RepositoriesProvider(),
    )

    setup_dishka(container=container, app=app)
