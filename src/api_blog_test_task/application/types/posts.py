from typing import TypedDict

class CreatePostType(TypedDict):
    title: str
    content: str


class UpdatePostType(CreatePostType): ...
