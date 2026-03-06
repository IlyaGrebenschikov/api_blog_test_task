from typing import (
    Unpack,
    Type,
)
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
    delete,
    select,
    insert,
    update,
    exists
)

from api_blog_test_task.application.interfaces.database.repositories import IPostsRepository
from api_blog_test_task.application.interfaces.database.mappers import IPostsRepositoryMapper
from api_blog_test_task.application.types import CreatePostType, UpdatePostType
from api_blog_test_task.domain.entities import Post
from api_blog_test_task.infrastructure.database.models import PostModel

class PostsRepository(IPostsRepository):
    def __init__(
            self,
            session: AsyncSession,
            mapper: IPostsRepositoryMapper,
    ):
        self._session = session
        self._mapper = mapper

    @property
    def _model(self) -> Type[PostModel]:
        return PostModel

    async def create_post(self, data: Unpack[CreatePostType]) -> Post:
        stmt = insert(self._model).values(data).returning(self._model)
        return self._mapper.persistence_to_domain((await self._session.scalars(stmt)).first())

    async def update_post(self, post_id: UUID, data: Unpack[UpdatePostType],) -> Post:
        clause = self._model.id == post_id
        stmt = update(self._model).where(clause).values(**data).returning(self._model)
        return self._mapper.persistence_to_domain((await self._session.execute(stmt)).scalars().first())

    async def get_post(self, post_id: UUID) -> Post:
        clause = self._model.id == post_id
        stmt = select(self._model).where(clause)
        return self._mapper.persistence_to_domain((await self._session.execute(stmt)).scalars().first())

    async def delete_post(self, post_id: UUID) -> Post:
        clause = self._model.id == post_id
        stmt = delete(self._model).where(clause).returning(self._model)
        return self._mapper.persistence_to_domain((await self._session.execute(stmt)).scalars().first())

    async def exists_post(self, post_id: UUID) -> bool:
        clause = self._model.id == post_id
        stmt = exists(select(self._model).where(clause)).select()
        return await self._session.scalar(stmt)
