import logging
from dataclasses import dataclass
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

log = logging.getLogger(__name__)

ENV_FILE = ".env"
ENV_FILE_ENCODING = "utf-8"

VERSION_ENV_PREFIX = "V1_"
APP_ENV_PREFIX = VERSION_ENV_PREFIX + "APP_"
CORS_ENV_PREFIX = VERSION_ENV_PREFIX + "CORS_"

class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding=ENV_FILE_ENCODING,
        env_prefix=APP_ENV_PREFIX,
        extra="ignore",
    )
    title: Optional[str] = "FastAPI"
    version: Optional[str] = "0.1.0"
    docs_url: Optional[str] = "/docs"
    redoc_url: Optional[str] = "/redoc"


class CORSSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding=ENV_FILE_ENCODING,
        env_prefix=CORS_ENV_PREFIX,
        extra="ignore"
    )
    methods: list[str] = ["*"]
    headers: list[str] = ["*"]
    origins: list[str] = ["*"]


@dataclass
class V1APISettings:
    app: AppSettings
    cors: CORSSettings


def load_v1_api_settings(
    app_settings: Optional[AppSettings] = None,
    cors_settings: Optional[CORSSettings] = None,
    ) -> V1APISettings:
    log.info("Loading v1 API settings.")
    return V1APISettings(
        app=app_settings or AppSettings(),
        cors=cors_settings or CORSSettings(),
    )
