import logging
from dataclasses import dataclass
from typing import Optional

from api_blog_test_task.infrastructure.settings import InfrastructureSettings, load_infrastructure_settings
from api_blog_test_task.presentation.settings import PresentationSettings, load_presentation_settings

log = logging.getLogger(__name__)


@dataclass
class Settings:
    infrastructure: InfrastructureSettings
    presentation: PresentationSettings


def load_settings(
        infrastructure_settings: Optional[InfrastructureSettings] = None,
        presentation_settings: Optional[PresentationSettings] = None,
) -> Settings:
    log.info("Loading core settings.")
    return Settings(
        infrastructure=infrastructure_settings or load_infrastructure_settings(),
        presentation=presentation_settings or load_presentation_settings()
    )
