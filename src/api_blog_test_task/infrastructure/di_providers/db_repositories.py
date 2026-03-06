from dishka import Provider, Scope, provide

from api_blog_test_task.application.interfaces.database import ITransactionManager
from api_blog_test_task.application.interfaces.database.repositories import IPostsRepository
from api_blog_test_task.application.interfaces.database.mappers import IPostsRepositoryMapper
from api_blog_test_task.infrastructure.database.repositories import PostsRepository
from api_blog_test_task.infrastructure.database.models import PostModel

class DBRepositoriesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def posts_repository(
            self,
            transaction_manager: ITransactionManager,
            mapper: IPostsRepositoryMapper[PostModel]
    ) -> IPostsRepository:
        return PostsRepository(transaction_manager.session, mapper)
