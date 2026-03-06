from api_blog_test_task.application.dto import ResponsePostDTO
from api_blog_test_task.application.interfaces.services.mappers import IPostsServiceMapper
from api_blog_test_task.domain.entities import Post

class PostsServiceMapper(IPostsServiceMapper):
    def domain_to_response_dto(self, data: Post) -> ResponsePostDTO:
        return ResponsePostDTO(
            id=data.id,
            title=data.title,
            content=data.content,
            created_at=data.created_at.isoformat(),
            updated_at=data.updated_at.isoformat()
        )
