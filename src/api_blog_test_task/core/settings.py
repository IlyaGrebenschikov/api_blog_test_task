import logging
from dataclasses import dataclass
from typing import Optional

from api_blog_test_task.infrastructure.settings import InfrastructureSettings, load_infrastructure_settings

log = logging.getLogger(__name__)


@dataclass
class Settings:
    infrastructure: InfrastructureSettings


def load_settings(
        infrastructure_settings: Optional[InfrastructureSettings] = None,
) -> Settings:
    log.info("Loading core settings.")
    return Settings(
        infrastructure=infrastructure_settings or load_infrastructure_settings(),
    )
