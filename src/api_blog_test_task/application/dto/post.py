from typing import Optional
from uuid import UUID

from pydantic import BaseModel

class PostDTO(BaseModel):
    title: str
    content: str


class CreatePostDTO(PostDTO): ...


class UpdatePostDTO(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class ResponsePostDTO(PostDTO):
    id: UUID
    created_at: str
    updated_at: str
