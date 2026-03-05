from sqlalchemy import Column, String, Text

from .base import BaseModel
from .mixins import UUIDMixinModel, TimestampMixinModel

class PostModel(BaseModel, UUIDMixinModel, TimestampMixinModel):
    __tablename__ = 'posts'

    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
