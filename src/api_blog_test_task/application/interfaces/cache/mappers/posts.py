from typing import Protocol

from api_blog_test_task.application.dto import ResponsePostDTO
from api_blog_test_task.application.types import CachedPostType
from api_blog_test_task.domain.entities import Post


class IPostsCacheMapper(Protocol):
    def domain_to_cached_dto(self, domain_model_post: Post) -> CachedPostType: ...

    def cached_to_response_dto(self, cached_dto: CachedPostType) -> ResponsePostDTO: ...
