import logging
from dataclasses import dataclass
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

log = logging.getLogger(__name__)

class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="DB_",
        extra="ignore"
    )
    drivername: str = "postgresql+asyncpg"
    host: str
    port: int
    username: str
    password: str
    database: str

    @property
    def url_obj(self) -> URL:
        return URL.create(**self.model_dump())

    @property
    def url_str(self) -> str:
        return (
            f"{self.drivername}://"
            f"{self.username}:"
            f"{self.password}@"
            f"{self.host}:"
            f"{self.port}/"
            f"{self.database}"
        )


class UvicornServerSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="UVICORN_SERVER_",
        extra="ignore"
    )

    host: Optional[str] = "0.0.0.0"
    port: Optional[int] = 8080


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="REDIS_",
        extra="ignore",
    )

    host: Optional[str] = "0.0.0.0"
    port: Optional[int] = 6379
    password: Optional[str] = None
    db: int = 0
    post_ttl: int = 300  # SEC
    hits_ttl: int = 300  # SEC
    hits_threshold: int = 10  # View threshold for cache

    @property
    def url(self) -> str:
        return (
            f"redis://"
            f"{f'{self.password}@' if self.password else ''}"
            f"{self.host}:"
            f"{self.port}/"
            f"{self.db}"
        )


@dataclass
class InfrastructureSettings:
    database: DatabaseSettings
    server: UvicornServerSettings
    cache: RedisSettings


def load_database_settings(database_settings: Optional[DatabaseSettings] = None,) -> DatabaseSettings:
    return database_settings or DatabaseSettings()


def load_infrastructure_settings(
        database_settings: Optional[DatabaseSettings] = None,
        server_settings: Optional[UvicornServerSettings] = None,
        cache_settings: Optional[RedisSettings] = None,
    ) -> InfrastructureSettings:
    log.info("Loading infrastructure settings.")
    return InfrastructureSettings(
        database=database_settings or DatabaseSettings(),
        server=server_settings or UvicornServerSettings(),
        cache=cache_settings or RedisSettings(),
    )
