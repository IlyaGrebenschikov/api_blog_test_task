from dataclasses import dataclass

from .mixins import UUIDMixin, TimestampMixin

@dataclass
class Post(UUIDMixin, TimestampMixin):
    __tablename__ = 'posts'

    title: str
    content: str
