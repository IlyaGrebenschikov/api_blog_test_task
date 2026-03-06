from uuid import UUID
from typing import Protocol

from api_blog_test_task.application.dto import (
    CreatePostDTO,
    UpdatePostDTO,
    ResponsePostDTO,
)

class IPostsService(Protocol):
    async def create_post(self, data: CreatePostDTO) -> ResponsePostDTO: ...

    async def get_post(self, post_id: UUID) -> ResponsePostDTO: ...

    async def update_post(self, post_id: UUID, data: UpdatePostDTO) -> ResponsePostDTO: ...

    async def delete_post(self, post_id: UUID) -> ResponsePostDTO: ...
