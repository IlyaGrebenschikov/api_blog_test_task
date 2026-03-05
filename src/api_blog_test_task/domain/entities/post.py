from dataclasses import dataclass

from .mixins import UUIDMixin, TimestampMixin

@dataclass
class Post(UUIDMixin, TimestampMixin):
    title: str
    content: str
