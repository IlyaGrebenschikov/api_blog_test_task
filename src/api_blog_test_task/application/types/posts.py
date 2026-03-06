from typing import TypedDict

class CreatePostType(TypedDict):
    title: str
    content: str


class UpdatePostType(CreatePostType): ...


class CachedPostType(TypedDict):
    id: str
    title: str
    content: str
    created_at: str
    updated_at: str
