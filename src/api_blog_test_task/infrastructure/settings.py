import logging
from dataclasses import dataclass
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

log = logging.getLogger(__name__)

class UvicornServerSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="UVICORN_SERVER_",
        extra="ignore"
    )

    host: Optional[str] = "0.0.0.0"
    port: Optional[int] = 8080


@dataclass
class InfrastructureSettings:
    server: UvicornServerSettings


def load_infrastructure_settings(
        server_settings: Optional[UvicornServerSettings] = None,
    ) -> InfrastructureSettings:
    log.info("Loading infrastructure settings.")
    return InfrastructureSettings(
        server=server_settings or UvicornServerSettings(),
    )
