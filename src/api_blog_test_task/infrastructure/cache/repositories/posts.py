import json
from typing import Optional
from uuid import UUID

from redis.asyncio import Redis

from api_blog_test_task.application.interfaces.cache.repositories import IPostsCacheRepository
from api_blog_test_task.application.types import CachedPostType


class PostsCacheRepository(IPostsCacheRepository):
    def __init__(self, cache_client: Redis, post_ttl: int = 300, hits_ttl: int = 300):
        self.cache = cache_client
        self.post_ttl = post_ttl
        self.hits_ttl = hits_ttl

    def _post_key(self, post_id: UUID) -> str:
        return f"post:{post_id}"

    def _hits_key(self, post_id: UUID) -> str:
        return f"post:hits:{post_id}"

    async def get_post(self, post_id: UUID) -> Optional[CachedPostType]:
        data = await self.cache.get(self._post_key(post_id))
        return json.loads(data) if data else None  # type: ignore[return-value]

    async def set_post(self, post_id: UUID, post_data: CachedPostType) -> None:
        await self.cache.setex(
            self._post_key(post_id),
            self.post_ttl,
            json.dumps(post_data),
        )

    async def delete_post(self, post_id: UUID) -> None:
        await self.cache.delete(self._post_key(post_id))

    async def increment_hits(self, post_id: UUID) -> int:
        result = await self.cache.incr(self._hits_key(post_id))
        await self.cache.expire(self._hits_key(post_id), self.hits_ttl)
        return result

    async def get_hits(self, post_id: UUID) -> int:
        hits = await self.cache.get(self._hits_key(post_id))
        return int(hits) if hits else 0
