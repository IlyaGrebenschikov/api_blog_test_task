from dishka import (
    Provider,
    Scope,
    provide
)

from api_blog_test_task.application.interfaces.cache.mappers import IPostsCacheMapper
from api_blog_test_task.application.interfaces.cache.repositories import IPostsCacheRepository
from api_blog_test_task.application.interfaces.database import ITransactionManager
from api_blog_test_task.application.interfaces.database.repositories import IPostsRepository
from api_blog_test_task.application.interfaces.services.mappers import IPostsServiceMapper
from api_blog_test_task.application.interfaces.services import IPostsService
from api_blog_test_task.application.services import PostsService


class PostsServiceProvider(Provider):
    def __init__(self, hits_threshold: int, scope=None, component=None):
        super().__init__(scope, component)
        self._hits_threshold: int = hits_threshold

    @provide(scope=Scope.REQUEST)
    def posts_service(
            self,
            repository: IPostsRepository,
            cache: IPostsCacheRepository,
            cache_mapper: IPostsCacheMapper,
            mapper: IPostsServiceMapper,
            transaction_manager: ITransactionManager,
    ) -> IPostsService:
        return PostsService(repository, cache, cache_mapper, mapper, transaction_manager, self._hits_threshold)
