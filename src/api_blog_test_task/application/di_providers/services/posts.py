from dishka import (
    Provider,
    Scope,
    provide
)

from api_blog_test_task.application.interfaces.database import ITransactionManager
from api_blog_test_task.application.interfaces.database.repositories import IPostsRepository
from api_blog_test_task.application.interfaces.services.mappers import IPostsServiceMapper
from api_blog_test_task.application.interfaces.services import IPostsService
from api_blog_test_task.application.services.mappers import PostsServiceMapper
from api_blog_test_task.application.services import PostsService

class PostsServiceProvider(Provider):
    @provide(scope=Scope.APP)
    def posts_service_mapper(self) -> IPostsServiceMapper:
        return PostsServiceMapper()

    @provide(scope=Scope.REQUEST)
    def users_service(
            self,
            repository: IPostsRepository,
            mapper: IPostsServiceMapper,
            transaction_manager: ITransactionManager,
    ) -> IPostsService:
        return PostsService(repository, mapper, transaction_manager)
