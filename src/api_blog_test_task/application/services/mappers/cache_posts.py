from uuid import UUID

from api_blog_test_task.application.dto import ResponsePostDTO
from api_blog_test_task.application.interfaces.cache.mappers import IPostsCacheMapper
from api_blog_test_task.application.types import CachedPostType
from api_blog_test_task.domain.entities import Post


class PostsCacheMapper(IPostsCacheMapper):
    def domain_to_cached_dto(self, data: Post) -> CachedPostType:
        return CachedPostType(
            id=str(data.id),
            title=data.title,
            content=data.content,
            created_at=data.created_at.isoformat(),
            updated_at=data.updated_at.isoformat(),
        )

    def cached_to_response_dto(self, data: CachedPostType) -> ResponsePostDTO:
        return ResponsePostDTO(
            id=UUID(data["id"]),
            title=data["title"],
            content=data["content"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
        )
