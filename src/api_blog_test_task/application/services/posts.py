import logging
from uuid import UUID

from api_blog_test_task.application.dto import (
    CreatePostDTO,
    UpdatePostDTO,
    ResponsePostDTO,
)
from api_blog_test_task.application.exceptions import NotFoundError
from api_blog_test_task.application.interfaces.database import ITransactionManager
from api_blog_test_task.application.interfaces.database.repositories import IPostsRepository
from api_blog_test_task.application.interfaces.services.mappers import IPostsServiceMapper
from api_blog_test_task.application.interfaces.services import IPostsService

log = logging.getLogger(__name__)


class PostsService(IPostsService):
    def __init__(
            self,
            repository: IPostsRepository,
            mapper: IPostsServiceMapper,
            transaction_manager: ITransactionManager,
    ):
        self._repository = repository
        self._mapper = mapper
        self._transaction_manager = transaction_manager

    async def create_post(self, data: CreatePostDTO) -> ResponsePostDTO:
        async with self._transaction_manager:
            await self._transaction_manager.create_transaction()
            result = await self._repository.create_post(data.model_dump())

        log.info("Post created with id: '%s'",result.id)
        return self._mapper.domain_to_response_dto(result)

    async def get_post(self, post_id: UUID) -> ResponsePostDTO:
        async with self._transaction_manager:

            if not await self._repository.exists_post(post_id):
                log.warning("Post not found: %s", post_id)
                raise NotFoundError(f"Post with ID: '{post_id}' not found")

            result = await self._repository.get_post(post_id)

        log.info("Post received with ID: %s", result.id)
        return self._mapper.domain_to_response_dto(result)

    async def update_post(self, post_id: UUID, data: UpdatePostDTO) -> ResponsePostDTO:
        async with self._transaction_manager:
            await self._transaction_manager.create_transaction()

            if not await self._repository.exists_post(post_id):
                log.warning("Post not found: %s", post_id)
                raise NotFoundError(f"Post with ID: '{post_id}' not found")

            result = await self._repository.update_post(
                post_id,
                data.model_dump(exclude_unset=True, exclude_none=True)
            )

        log.info("Post updated with ID: %s", result.id)
        return self._mapper.domain_to_response_dto(result)

    async def delete_post(self, post_id: UUID) -> ResponsePostDTO:
        async with self._transaction_manager:
            await self._transaction_manager.create_transaction()

            if not await self._repository.exists_post(post_id):
                log.warning("Post not found: %s", post_id)
                raise NotFoundError(f"Post with ID: '{post_id}' not found")

            result = await self._repository.delete_post(post_id)

        log.info("Post deleted with ID: %s", result.id)
        return self._mapper.domain_to_response_dto(result)
