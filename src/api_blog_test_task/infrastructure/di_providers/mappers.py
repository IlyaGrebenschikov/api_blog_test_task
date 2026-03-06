from dishka import Provider, Scope, provide

from api_blog_test_task.application.interfaces.database.mappers import IPostsRepositoryMapper
from api_blog_test_task.infrastructure.database.mappers import PostsRepositoryMapper

class MappersProvider(Provider):
    @provide(scope=Scope.APP)
    def posts_repository_mapper(self) -> IPostsRepositoryMapper:
        return PostsRepositoryMapper()
