from api_blog_test_task.application.interfaces.database.mappers import IPostsRepositoryMapper
from api_blog_test_task.domain.entities.post import Post
from api_blog_test_task.infrastructure.database.models import PostModel

class PostsRepositoryMapper(IPostsRepositoryMapper[PostModel]):
    def persistence_to_domain(self, post_model: PostModel) -> Post:
        return Post(
            id=post_model.id,
            title=post_model.title,
            content=post_model.content,
            created_at=post_model.created_at,
            updated_at=post_model.updated_at,
        )
