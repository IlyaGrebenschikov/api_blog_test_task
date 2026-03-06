import logging
import sys

from .core.settings import load_settings
from .core.di_container import setup_dependencies
from .infrastructure.servers import run_uvicorn_server
from .presentation import init_app
from .presentation.v1 import init_app_v1

def main() -> None:
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    settings = load_settings()
    app = init_app(
        init_app_v1(
            settings.presentation.v1_api
        )
    )

    setup_dependencies(app, settings)
    run_uvicorn_server(app, settings.infrastructure.server)


if __name__ == "__main__":
    main()
