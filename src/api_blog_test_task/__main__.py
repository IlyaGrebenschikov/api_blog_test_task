import logging
import sys

from fastapi import FastAPI

from .core.settings import load_settings
from .core.di_container import setup_dependencies
from .infrastructure.servers import run_uvicorn_server

def main() -> None:
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    settings = load_settings()

    app = FastAPI()

    setup_dependencies(app, settings)
    run_uvicorn_server(app, settings.infrastructure.server)


if __name__ == "__main__":
    main()
