import logging

import uvicorn
from fastapi import FastAPI

from api_blog_test_task.infrastructure.settings import UvicornServerSettings

log = logging.getLogger(__name__)

def run_uvicorn_server(
    app: FastAPI,
    settings: UvicornServerSettings,
    ) -> None:
    log.info("Running Uvicorn server.")
    uvicorn.run(app, **settings.model_dump())
