from typing import Protocol, TypeVar

from api_blog_test_task.domain.entities.post import Post

PostModelT = TypeVar("PostModelT")


class IPostsRepositoryMapper(Protocol[PostModelT]):
    def persistence_to_domain(self, post_model: PostModelT) -> Post: ...
