from uuid import UUID

from fastapi import APIRouter, status
from dishka.integrations.fastapi import DishkaRoute, FromDishka

from api_blog_test_task.application.dto import (
    CreatePostDTO,
    UpdatePostDTO,
    ResponsePostDTO,
)
from api_blog_test_task.presentation.v1.docs import (
    NotFoundError,
)
from api_blog_test_task.application.interfaces.services import IPostsService

posts_router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    route_class=DishkaRoute
)


@posts_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponsePostDTO,
)
async def create_post(
        data: CreatePostDTO,
        service: FromDishka[IPostsService]
) -> ResponsePostDTO:
    return await service.create_post(data)


@posts_router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ResponsePostDTO,
    responses={
    status.HTTP_404_NOT_FOUND: {'model': NotFoundError},
}
)
async def get_post(
        post_id: UUID,
        service: FromDishka[IPostsService]
) -> ResponsePostDTO:
    return await service.get_post(post_id)


@posts_router.patch(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ResponsePostDTO,
    responses={
        status.HTTP_404_NOT_FOUND: {'model': NotFoundError},
    }
)
async def update_post(
        post_id: UUID,
        data: UpdatePostDTO,
        service: FromDishka[IPostsService],
) -> ResponsePostDTO:
    return await service.update_post(post_id, data)


@posts_router.delete(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ResponsePostDTO,
    responses={
        status.HTTP_404_NOT_FOUND: {'model': NotFoundError},
    }
)
async def delete_post(
        post_id: UUID,
        service: FromDishka[IPostsService],
) -> ResponsePostDTO:
    return await service.delete_post(post_id)