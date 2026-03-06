from dishka import Provider, Scope, provide
from redis.asyncio import Redis
from api_blog_test_task.infrastructure.settings import RedisSettings
from api_blog_test_task.infrastructure.cache import create_cache_client

class CacheProvider(Provider):
    def __init__(self, redis_settings: RedisSettings, scope=None, component=None):
        super().__init__(scope, component)
        self._redis_settings = redis_settings

    @provide(scope=Scope.APP)
    def redis_client(self) -> Redis:
        return create_cache_client(self._redis_settings.url)
