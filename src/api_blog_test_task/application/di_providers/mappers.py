from dishka import (
    Provider,
    Scope,
    provide
)

from api_blog_test_task.application.interfaces.cache.mappers import IPostsCacheMapper
from api_blog_test_task.application.interfaces.services.mappers import IPostsServiceMapper
from api_blog_test_task.application.services.mappers import PostsServiceMapper, PostsCacheMapper

class MappersServiceProvider(Provider):
    @provide(scope=Scope.APP)
    def posts_service_mapper(self) -> IPostsServiceMapper:
        return PostsServiceMapper()

    @provide(scope=Scope.APP)
    def posts_cache_mapper(self) -> IPostsCacheMapper:
        return PostsCacheMapper()
