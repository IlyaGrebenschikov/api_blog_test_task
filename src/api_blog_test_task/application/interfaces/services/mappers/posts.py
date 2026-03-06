from typing import Protocol

from api_blog_test_task.application.dto import ResponsePostDTO
from api_blog_test_task.domain.entities import Post

class IPostsServiceMapper(Protocol):
    def domain_to_response_dto(self, domain_model_post: Post) -> ResponsePostDTO: ...
