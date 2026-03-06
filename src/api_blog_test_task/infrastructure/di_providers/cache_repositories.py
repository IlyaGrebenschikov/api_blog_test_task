from dishka import Provider, Scope, provide
from redis.asyncio import Redis

from api_blog_test_task.application.interfaces.cache.repositories import IPostsCacheRepository
from api_blog_test_task.infrastructure.cache.repositories import PostsCacheRepository
from api_blog_test_task.infrastructure.settings import RedisSettings


class CacheRepositoriesProvider(Provider):
    def __init__(self, redis_settings: RedisSettings, scope=None, component=None):
        super().__init__(scope, component)
        self._redis_settings = redis_settings

    @provide(scope=Scope.REQUEST)
    def cache_posts_repository(self, client: Redis) -> IPostsCacheRepository:
        return PostsCacheRepository(client, self._redis_settings.post_ttl, self._redis_settings.hits_ttl)
