from dishka import Provider, Scope, provide
from redis.asyncio import Redis

from api_blog_test_task.application.interfaces.cache.repositories import IPostsCacheRepository
from api_blog_test_task.infrastructure.cache.repositories import PostsCacheRepository

class CacheRepositoriesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def cache_posts_repository(self, client: Redis) -> IPostsCacheRepository:
        return PostsCacheRepository(client)
