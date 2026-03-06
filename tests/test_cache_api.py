import pytest
from uuid import uuid4

from httpx import AsyncClient, ASGITransport


@pytest.fixture(scope="function")
def api_v1_url():
    return "/api/v1"


@pytest.fixture(scope="function")
def posts_url(api_v1_url):
    return f"{api_v1_url}/posts"


@pytest.fixture(scope="function")
def post_payload():
    return {
        "title": "Test Post",
        "content": "Test Content"
    }


@pytest.fixture(scope="function")
def update_payload():
    return {
        "title": "Updated Title",
        "content": "Updated Content"
    }


class TestCacheIntegrationAPI:

    @pytest.mark.asyncio
    async def test_post_not_cached_below_threshold(
        self,
        client: AsyncClient,
        posts_url: str,
        post_payload: dict,
        redis_client,
    ):
        response = await client.post(posts_url, json=post_payload)
        assert response.status_code == 201
        post_id = response.json()["id"]

        for _ in range(9):
            response = await client.get(f"{posts_url}?post_id={post_id}")
            assert response.status_code == 200

        cached = await redis_client.get(f"post:{post_id}")
        assert cached is None

        hits = await redis_client.get(f"post:hits:{post_id}")
        assert hits is not None
        assert int(hits) == 9

    @pytest.mark.asyncio
    async def test_post_cached_at_threshold(
        self,
        client: AsyncClient,
        posts_url: str,
        post_payload: dict,
        redis_client,
    ):
        response = await client.post(posts_url, json=post_payload)
        assert response.status_code == 201
        post_id = response.json()["id"]

        for _ in range(10):
            response = await client.get(f"{posts_url}?post_id={post_id}")
            assert response.status_code == 200

        cached = await redis_client.get(f"post:{post_id}")
        assert cached is not None

        import json
        cached_data = json.loads(cached)
        assert cached_data["id"] == post_id
        assert cached_data["title"] == post_payload["title"]

        hits = await redis_client.get(f"post:hits:{post_id}")
        assert int(hits) == 10

    @pytest.mark.asyncio
    async def test_cache_hit_returns_cached_data(
        self,
        client: AsyncClient,
        posts_url: str,
        post_payload: dict,
        redis_client,
    ):
        response = await client.post(posts_url, json=post_payload)
        assert response.status_code == 201
        post_id = response.json()["id"]

        for _ in range(10):
            await client.get(f"{posts_url}?post_id={post_id}")

        response = await client.get(f"{posts_url}?post_id={post_id}")
        assert response.status_code == 200
        data = response.json()

        assert data["id"] == post_id
        assert data["title"] == post_payload["title"]

        hits = await redis_client.get(f"post:hits:{post_id}")
        assert int(hits) == 11

    @pytest.mark.asyncio
    async def test_cache_invalidated_on_update(
        self,
        client: AsyncClient,
        posts_url: str,
        post_payload: dict,
        update_payload: dict,
        redis_client,
    ):
        response = await client.post(posts_url, json=post_payload)
        assert response.status_code == 201
        post_id = response.json()["id"]

        for _ in range(10):
            await client.get(f"{posts_url}?post_id={post_id}")

        cached = await redis_client.get(f"post:{post_id}")
        assert cached is not None

        response = await client.patch(
            f"{posts_url}?post_id={post_id}",
            json=update_payload
        )
        assert response.status_code == 200

        import json
        cached_data = json.loads(await redis_client.get(f"post:{post_id}"))
        assert cached_data["title"] == update_payload["title"]
        assert cached_data["content"] == update_payload["content"]

    @pytest.mark.asyncio
    async def test_cache_and_hits_deleted_on_delete(
        self,
        client: AsyncClient,
        posts_url: str,
        post_payload: dict,
        redis_client,
    ):
        response = await client.post(posts_url, json=post_payload)
        assert response.status_code == 201
        post_id = response.json()["id"]

        for _ in range(10):
            await client.get(f"{posts_url}?post_id={post_id}")

        assert await redis_client.get(f"post:{post_id}") is not None
        assert await redis_client.get(f"post:hits:{post_id}") is not None

        response = await client.delete(f"{posts_url}?post_id={post_id}")
        assert response.status_code == 200

        cached = await redis_client.get(f"post:{post_id}")
        assert cached is None

        hits = await redis_client.get(f"post:hits:{post_id}")
        assert hits is None

    @pytest.mark.asyncio
    async def test_hits_counter_accumulates(
        self,
        client: AsyncClient,
        posts_url: str,
        post_payload: dict,
        redis_client,
    ):
        response = await client.post(posts_url, json=post_payload)
        assert response.status_code == 201
        post_id = response.json()["id"]

        for _ in range(5):
            await client.get(f"{posts_url}?post_id={post_id}")

        hits = await redis_client.get(f"post:hits:{post_id}")
        assert int(hits) == 5

        for _ in range(5):
            await client.get(f"{posts_url}?post_id={post_id}")

        hits = await redis_client.get(f"post:hits:{post_id}")
        assert int(hits) == 10

        cached = await redis_client.get(f"post:{post_id}")
        assert cached is not None

    @pytest.mark.asyncio
    async def test_cache_ttl_is_set(
        self,
        client: AsyncClient,
        posts_url: str,
        post_payload: dict,
        redis_client,
        settings,
    ):
        response = await client.post(posts_url, json=post_payload)
        assert response.status_code == 201
        post_id = response.json()["id"]

        for _ in range(10):
            await client.get(f"{posts_url}?post_id={post_id}")

        ttl = await redis_client.ttl(f"post:{post_id}")
        assert ttl > 0
        assert ttl <= settings.infrastructure.cache.post_ttl

    @pytest.mark.asyncio
    async def test_get_non_existent_post_returns_404(
        self,
        client: AsyncClient,
        posts_url: str,
    ):
        non_existent_id = str(uuid4())
        response = await client.get(f"{posts_url}?post_id={non_existent_id}")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_update_non_existent_post_returns_404(
        self,
        client: AsyncClient,
        posts_url: str,
        update_payload: dict,
    ):
        non_existent_id = str(uuid4())
        response = await client.patch(
            f"{posts_url}?post_id={non_existent_id}",
            json=update_payload
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_non_existent_post_returns_404(
        self,
        client: AsyncClient,
        posts_url: str,
    ):
        non_existent_id = str(uuid4())
        response = await client.delete(f"{posts_url}?post_id={non_existent_id}")
        assert response.status_code == 404
